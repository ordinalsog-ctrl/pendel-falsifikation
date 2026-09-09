"""compute_gdelt_cluster_impact — GDELT-Cluster-Causal-Motor (H90-Prio 1).

WARUM: `compute_event_impact.py` (DEC-083) fährt SARIMAX-Counterfactual NUR auf
EVENT_SOURCES = fed/bls/ecb_calendar. GDELT wird nie eingespeist → die geopolitische
Achse der These (GDELT×Krypto) ist bislang UNGETESTET, nicht "getestet und null".
Dieser Motor erweitert die BESTEHENDE, getestete Methode (`compute_impact`) auf GDELT —
kein neues Werkzeug, eine Erweiterung.

METHODE:
1. GDELT-Events (source='gdelt', severity>=SHOCK_SEV) je UTC-Tag deduplizieren
   (COUNT(DISTINCT event_type,region)) → tägliche Schock-Intensität.
2. Schock-Tage = Tage mit deduped-Count >= datengetriebener Quantil-Schwelle.
3. Pro (Schock-Tag × Krypto-Symbol × Post-Window): SARIMAX-CF via `compute_impact`
   (60d pre-returns fitten → post forecasten → Actual−Counterfactual).
4. FDR (Benjamini-Hochberg) über den gesamten Batch; significant = FDR-reject UND
   n_post>=MIN_POST_OBS (identische Gates wie DEC-153).
5. NEGATIVKONTROLLE (Placebo): gleich viele zufällige NICHT-Schock-Tage, gleiche
   Prozedur. Echte Signifikanz-Rate muss die Placebo-Rate deutlich übersteigen,
   sonst ist ein Treffer ein Artefakt. Ohne diese Kontrolle kein verteidigbarer Claim.

SICHERHEIT (Karpathy/DEC-009):
- Default = DRY-RUN: rechnet + druckt Zusammenfassung, schreibt NICHTS. Erst `--write`
  schreibt in `gdelt_cluster_impact`. So sehen wir das Ergebnis, bevor irgendetwas
  in die Produktions-DB geht.
- Read-only auf allen bestehenden Tabellen; schreibt ausschließlich in die neue
  Tabelle `gdelt_cluster_impact` (Schema: motor/schema_gdelt_cluster_impact.sql).
- Reproduzierbar via --seed.

Aufruf (Dry-Run zuerst!):
    /opt/pendel/venv/bin/python compute_gdelt_cluster_impact.py            # dry-run
    /opt/pendel/venv/bin/python compute_gdelt_cluster_impact.py --write    # schreibt
"""
from __future__ import annotations
import argparse
import asyncio
import os
import sys
import warnings
import logging
from datetime import datetime, timezone, timedelta

import asyncpg
import numpy as np
import pandas as pd
import structlog
from dotenv import load_dotenv
from statsmodels.stats.multitest import multipletests

# Wiederverwendung der GETESTETEN Bausteine (kein Neuschrieb der SARIMAX-Logik):
from compute_correlations import SYMBOLS, fetch_series, RESAMPLE_FREQ
from compute_event_impact import compute_impact, MIN_PRE_OBS, PRE_WINDOW_DAYS

load_dotenv("/root/pendel.env")
DSN = (f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASS']}"
       f"@{os.environ.get('DB_HOST', 'localhost')}"
       f":{os.environ.get('DB_PORT', '5432')}"
       f"/{os.environ['DB_NAME']}?sslmode=disable")

# --- Parameter (datengetrieben, nicht handgetunt) --------------------------------------
CRYPTO_TARGETS = ["BTC", "ETH", "SOL", "XRP", "BNB", "DOGE", "ADA", "LINK", "HYPE", "TRX"]
SHOCK_SEVERITY_MIN = 4          # GDELT-Severity-Schwelle für "hoher Impact"
SHOCK_QUANTILE = 0.90           # Schock-Tag = Tag im Top-Dezil der deduped Tages-Intensität
SHOCK_MIN_FLOOR = 3             # absoluter Mindest-Dedup-Count, damit ein Tag Schock sein kann
POST_WINDOWS_DAYS = [7, 30]
MIN_POST_OBS = 10               # identisch zu DEC-153: unter 10 Post-Obs nie significant
FDR_ALPHA = 0.05
LOOKBACK_DAYS = 130             # ~gesamte Live-Periode
METHOD = "gdelt_cluster_sarimax_cf"


def setup_logging() -> None:
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)
    structlog.configure(
        processors=[structlog.processors.add_log_level,
                    structlog.processors.TimeStamper(fmt="iso"),
                    structlog.processors.JSONRenderer()],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO))


async def fetch_daily_shock_intensity(pool, since, until) -> pd.Series:
    """Deduplizierte hohe-Severity-GDELT-Events je UTC-Tag."""
    async with pool.acquire() as con:
        rows = await con.fetch(
            """
            SELECT date_trunc('day', ts) AS day,
                   COUNT(DISTINCT (event_type, region)) AS dedup_count
            FROM events
            WHERE source = 'gdelt' AND severity >= $1 AND ts >= $2 AND ts <= $3
            GROUP BY 1 ORDER BY 1
            """,
            SHOCK_SEVERITY_MIN, since, until,
        )
    if not rows:
        return pd.Series(dtype=float)
    idx = pd.DatetimeIndex([r["day"] for r in rows])
    return pd.Series([r["dedup_count"] for r in rows], index=idx, dtype=float)


async def build_crypto_returns(pool, series_since) -> pd.DataFrame:
    """Krypto-Return-Matrix — identische Bau-Logik wie compute_event_impact."""
    relevant = [sd for sd in SYMBOLS if sd[0] in CRYPTO_TARGETS]
    series_list = await asyncio.gather(*[fetch_series(pool, sd, series_since) for sd in relevant])
    non_empty = [(sd, s) for sd, s in zip(relevant, series_list) if len(s) > 0]
    if not non_empty:
        return pd.DataFrame()
    joined = pd.concat([s for _, s in non_empty], axis=1)
    joined.columns = [sd[0] for sd, _ in non_empty]
    joined = joined.resample(RESAMPLE_FREQ).last().ffill(limit=10)
    return joined.pct_change().dropna(how="all")


def run_batch(day_list, day_counts, returns, is_placebo: bool) -> list[dict]:
    """SARIMAX-CF für jede (Tag × Symbol × Window)-Kombi. Sammelt Roh-Ergebnisse."""
    out = []
    for day in day_list:
        event_ts = day.to_pydatetime().replace(tzinfo=timezone.utc)
        for symbol in CRYPTO_TARGETS:
            if symbol not in returns.columns:
                continue
            pre_start = event_ts - timedelta(days=PRE_WINDOW_DAYS)
            pre = returns[(returns.index >= pre_start) & (returns.index < event_ts)][symbol].dropna().values
            if len(pre) < MIN_PRE_OBS:
                continue
            for post_days in POST_WINDOWS_DAYS:
                post_end = event_ts + timedelta(days=post_days)
                post = returns[(returns.index > event_ts) & (returns.index <= post_end)][symbol].dropna().values
                if len(post) < 3:
                    continue
                res = compute_impact(pre, post)   # GETESTETE SARIMAX-CF (DEC-083/153)
                if res is None:
                    continue
                out.append({
                    "cluster_day": day.date(),
                    "n_cluster_events": int(day_counts.get(day, 0)),
                    "target_symbol": symbol,
                    "post_window_days": post_days,
                    "n_pre": len(pre), "n_post": len(post),
                    "p_value": res["p_value"], "is_placebo": is_placebo,
                    "res": res,
                })
    return out


def apply_fdr(batch: list[dict]) -> int:
    """BH-FDR über den Batch; setzt res['significant']. Gibt #significant zurück."""
    idx = [i for i, e in enumerate(batch) if e["p_value"] is not None]
    reject = {}
    if idx:
        rej, _, _, _ = multipletests([batch[i]["p_value"] for i in idx],
                                     alpha=FDR_ALPHA, method="fdr_bh")
        reject = {idx[j]: bool(rej[j]) for j in range(len(idx))}
    n_sig = 0
    for i, e in enumerate(batch):
        sig = bool(reject.get(i, False)) and e["n_post"] >= MIN_POST_OBS
        e["significant"] = sig
        n_sig += int(sig)
    return n_sig


async def main(write: bool, seed: int) -> int:
    log = structlog.get_logger()
    rng = np.random.default_rng(seed)
    pool = await asyncpg.create_pool(DSN, min_size=1, max_size=2)

    now = datetime.now(timezone.utc).replace(microsecond=0)
    since = now - timedelta(days=LOOKBACK_DAYS)

    intensity = await fetch_daily_shock_intensity(pool, since, now)
    if intensity.empty:
        log.warning("gdelt_motor.no_gdelt_events"); await pool.close(); return 0

    threshold = max(SHOCK_MIN_FLOOR, float(intensity.quantile(SHOCK_QUANTILE)))
    shock_days = list(intensity[intensity >= threshold].index)
    non_shock_days = list(intensity[intensity < threshold].index)
    if not shock_days:
        log.warning("gdelt_motor.no_shock_days", threshold=threshold); await pool.close(); return 0

    # Placebo: gleich viele zufällige Nicht-Schock-Tage
    k = min(len(shock_days), len(non_shock_days))
    placebo_days = list(rng.choice(non_shock_days, size=k, replace=False)) if k > 0 else []

    series_since = since - timedelta(days=PRE_WINDOW_DAYS + max(POST_WINDOWS_DAYS) + 30)
    returns = await build_crypto_returns(pool, series_since)
    if returns.empty:
        log.warning("gdelt_motor.no_crypto_data"); await pool.close(); return 0

    day_counts = intensity.to_dict()
    real = run_batch(shock_days, day_counts, returns, is_placebo=False)
    placebo = run_batch(placebo_days, day_counts, returns, is_placebo=True)

    n_real_sig = apply_fdr(real)
    n_plac_sig = apply_fdr(placebo)

    # --- Zusammenfassung (immer, auch dry-run) -----------------------------------------
    top = sorted([e for e in real if e["significant"]],
                 key=lambda e: -abs(e["res"]["absolute_effect"]))[:10]
    print("=" * 70)
    print(f"GDELT-CLUSTER-MOTOR  (dry-run={'NEIN, --write' if write else 'JA'})")
    print(f"  Lookback: {LOOKBACK_DAYS}d | Severity>={SHOCK_SEVERITY_MIN} | "
          f"Schock-Schwelle(dedup>= q{SHOCK_QUANTILE}): {threshold:.1f}")
    print(f"  Schock-Tage: {len(shock_days)} | Placebo-Tage: {len(placebo_days)}")
    print(f"  Tests real: {len(real)} | Tests placebo: {len(placebo)}")
    print(f"  SIGNIFIKANT (FDR+n_post>=10)  real={n_real_sig}  placebo={n_plac_sig}")
    print(f"  -> Verteidigbar nur, wenn real >> placebo. real<=placebo = Artefakt/Null.")
    if top:
        print("  Top-Effekte (real, significant):")
        for e in top:
            r = e["res"]
            print(f"    {e['cluster_day']} {e['target_symbol']:5s} {e['post_window_days']}d "
                  f"eff={r['absolute_effect']:+.4f} p={r['p_value']:.4f} n_post={e['n_post']}")
    print("=" * 70)

    if not write:
        log.info("gdelt_motor.dry_run_complete", real=len(real), real_sig=n_real_sig,
                 placebo_sig=n_plac_sig)
        await pool.close()
        return 0

    # --- Schreiben (nur mit --write) ---------------------------------------------------
    rows = []
    for e in (real + placebo):
        r = e["res"]
        rows.append((now, e["cluster_day"], e["n_cluster_events"], e["target_symbol"],
                     PRE_WINDOW_DAYS, e["post_window_days"], e["n_pre"], e["n_post"],
                     r["actual_mean"], r["counterfactual_mean"], r["absolute_effect"],
                     r["relative_effect_pct"], r["ci_lower"], r["ci_upper"],
                     r["p_value"], e["significant"], e["is_placebo"], METHOD))
    async with pool.acquire() as con:
        await con.executemany(
            """
            INSERT INTO gdelt_cluster_impact
                (ts, cluster_day, n_cluster_events, target_symbol, pre_window_days,
                 post_window_days, n_pre, n_post, actual_post_mean, counterfactual_mean,
                 absolute_effect, relative_effect_pct, ci_lower, ci_upper, p_value,
                 significant, is_placebo, method)
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18)
            ON CONFLICT (cluster_day, target_symbol, post_window_days, is_placebo, method)
            DO UPDATE SET ts=EXCLUDED.ts, n_cluster_events=EXCLUDED.n_cluster_events,
                n_pre=EXCLUDED.n_pre, n_post=EXCLUDED.n_post,
                actual_post_mean=EXCLUDED.actual_post_mean,
                counterfactual_mean=EXCLUDED.counterfactual_mean,
                absolute_effect=EXCLUDED.absolute_effect,
                relative_effect_pct=EXCLUDED.relative_effect_pct,
                ci_lower=EXCLUDED.ci_lower, ci_upper=EXCLUDED.ci_upper,
                p_value=EXCLUDED.p_value, significant=EXCLUDED.significant,
                received_at=NOW()
            """, rows)
    log.info("gdelt_motor.written", rows=len(rows), real_sig=n_real_sig, placebo_sig=n_plac_sig)
    await pool.close()
    return len(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="in DB schreiben (Default: dry-run)")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    setup_logging()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        asyncio.run(main(args.write, args.seed))
