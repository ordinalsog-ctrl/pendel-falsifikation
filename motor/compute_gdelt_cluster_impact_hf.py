"""compute_gdelt_cluster_impact_hf — GDELT×Krypto, v2: stündlich + Vola + Permutation.

WARUM v2: Der Tages-Motor (v1) fand null (real 3 ≤ placebo 11) — aber Krypto reagiert
in STUNDEN, nicht Tagen, und der parametrische SARIMAX-CI-p war antikonservativ (11
Placebo-Fehlalarme). `compute_correlations.py` sagt selbst: 7d-Fenster ist mit Daily nie
befüllt „bis hourly-Resampling kommt". v2 behebt beides:

  - STÜNDLICHE Returns aus trades_5min (pre 14d, post 24h/72h) — Krypto-Zeitskala.
  - ZWEI Kanäle: Mittelwert-Reaktion UND Volatilitäts-Reaktion (Literatur: Vola reagiert
    auf News, wo Rendite nicht reagiert).
  - PERMUTATIONSTEST (non-parametrisch): reale Schock-Tage vs. B zufällige Nicht-Schock-Tage
    → empirischer p je Kanal. Kein parametrischer p, keine Kalibrierungs-Falle.

REINES ANALYSE-TOOL: schreibt NICHTS in die DB (read-only). Es beantwortet eine Frage —
„bewegen Geopolitik-Schocks Krypto über das Zufallsniveau hinaus?" — und druckt das Urteil.

Verteidigbarkeit: Signal nur, wenn empirischer p < 0.05 (real-Effekt größer als das
Placebo-Niveau). p ≥ 0.05 = sauberer, non-parametrischer Null-Befund.

Aufruf (read-only):
    /opt/pendel/venv/bin/python compute_gdelt_cluster_impact_hf.py
"""
from __future__ import annotations
import argparse
import asyncio
import os
import sys
import warnings
from datetime import datetime, timezone, timedelta

import asyncpg
import numpy as np
import pandas as pd
from dotenv import load_dotenv

from compute_correlations import SYMBOLS, fetch_series

load_dotenv("/root/pendel.env")
DSN = (f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASS']}"
       f"@{os.environ.get('DB_HOST', 'localhost')}"
       f":{os.environ.get('DB_PORT', '5432')}"
       f"/{os.environ['DB_NAME']}?sslmode=disable")

CRYPTO_TARGETS = ["BTC", "ETH", "SOL", "XRP", "BNB", "DOGE", "ADA", "LINK", "HYPE", "TRX"]
SHOCK_SEVERITY_MIN = 4
SHOCK_QUANTILE = 0.90
SHOCK_MIN_FLOOR = 3
LOOKBACK_DAYS = 130
PRE_HOURS = 14 * 24          # 14 Tage stündlich als Baseline
POST_WINDOWS_H = [24, 72]    # Krypto-Reaktion in Stunden
MIN_PRE_OBS = 48             # >=2 Tage stündlich
MIN_POST_OBS = 10
B_PERM = 200                 # Permutationen
RESAMPLE = "1h"


async def fetch_daily_shock_intensity(pool, since, until) -> pd.Series:
    rows = await pool.fetch(
        """
        SELECT date_trunc('day', ts) AS day,
               COUNT(DISTINCT (event_type, region)) AS dedup_count
        FROM events
        WHERE source='gdelt' AND severity >= $1 AND ts >= $2 AND ts <= $3
        GROUP BY 1 ORDER BY 1
        """, SHOCK_SEVERITY_MIN, since, until)
    if not rows:
        return pd.Series(dtype=float)
    idx = pd.DatetimeIndex([r["day"] for r in rows])
    return pd.Series([r["dedup_count"] for r in rows], index=idx, dtype=float)


async def build_hourly_arrays(pool, since):
    """Pro Krypto-Symbol: (sortierte ts als int64-ns, stündliche Returns) — für
    schnelle searchsorted-Fensterschnitte (kein O(N)-Loop, Karpathy-#38)."""
    relevant = [sd for sd in SYMBOLS if sd[0] in CRYPTO_TARGETS]
    series_list = await asyncio.gather(*[fetch_series(pool, sd, since) for sd in relevant])
    out = {}
    for sd, s in zip(relevant, series_list):
        if len(s) == 0:
            continue
        hourly = s.resample(RESAMPLE).last()            # KEIN ffill (M9/DEC-140)
        ret = hourly.pct_change().dropna()
        if len(ret) < MIN_PRE_OBS:
            continue
        ts_int = ret.index.asi8                          # ns since epoch (UTC)
        out[sd[0]] = (ts_int, ret.values.astype(float))
    return out


def _slice(arr, ts_int, start_int, end_int, incl_start, incl_end):
    lo = np.searchsorted(ts_int, start_int, side="left" if incl_start else "right")
    hi = np.searchsorted(ts_int, end_int, side="right" if incl_end else "left")
    return arr[lo:hi]


def day_effects(days, sym_arrays):
    """Für jeden (Tag × Symbol × Post-Window): mean_effect + vol_effect (pre vs post)."""
    NS_H = 3_600_000_000_000
    mean_eff, vol_eff = [], []
    for day in days:
        ev = int(pd.Timestamp(day).value)   # UTC-ns, konsistent mit index.asi8
        for sym, (ts_int, vals) in sym_arrays.items():
            pre = _slice(vals, ts_int, ev - PRE_HOURS * NS_H, ev, True, False)
            if len(pre) < MIN_PRE_OBS:
                continue
            for h in POST_WINDOWS_H:
                post = _slice(vals, ts_int, ev, ev + h * NS_H, False, True)
                if len(post) < MIN_POST_OBS:
                    continue
                mean_eff.append(abs(float(np.mean(post)) - float(np.mean(pre))))
                vol_eff.append(float(np.std(post, ddof=1)) - float(np.std(pre, ddof=1)))
    return np.array(mean_eff), np.array(vol_eff)


def agg(mean_eff, vol_eff):
    m = float(np.mean(mean_eff)) if len(mean_eff) else float("nan")
    v = float(np.mean(vol_eff)) if len(vol_eff) else float("nan")
    return m, v, len(mean_eff)


async def main(seed: int) -> int:
    rng = np.random.default_rng(seed)
    pool = await asyncpg.create_pool(DSN, min_size=1, max_size=2)
    now = datetime.now(timezone.utc).replace(microsecond=0)
    since = now - timedelta(days=LOOKBACK_DAYS)

    intensity = await fetch_daily_shock_intensity(pool, since, now)
    if intensity.empty:
        print("Keine GDELT-Events."); await pool.close(); return 0
    threshold = max(SHOCK_MIN_FLOOR, float(intensity.quantile(SHOCK_QUANTILE)))
    shock_days = list(intensity[intensity >= threshold].index)
    non_shock = list(intensity[intensity < threshold].index)
    if len(shock_days) < 3 or len(non_shock) < len(shock_days):
        print(f"Zu wenige Schock-/Nicht-Schock-Tage: {len(shock_days)}/{len(non_shock)}")
        await pool.close(); return 0

    sym_arrays = await build_hourly_arrays(pool, since - timedelta(days=20))
    await pool.close()
    if not sym_arrays:
        print("Keine stündlichen Krypto-Daten."); return 0

    real_mean, real_vol = day_effects(shock_days, sym_arrays)
    r_m, r_v, n_real = agg(real_mean, real_vol)

    # Permutation: B zufällige Nicht-Schock-Tage-Sets gleicher Größe
    perm_m, perm_v = [], []
    k = len(shock_days)
    for _ in range(B_PERM):
        pdays = list(rng.choice(non_shock, size=k, replace=False))
        pm, pv = day_effects(pdays, sym_arrays)
        a_m, a_v, _ = agg(pm, pv)
        if not np.isnan(a_m):
            perm_m.append(a_m)
        if not np.isnan(a_v):
            perm_v.append(a_v)
    perm_m, perm_v = np.array(perm_m), np.array(perm_v)

    def emp_p(real, perm):
        if np.isnan(real) or len(perm) == 0:
            return float("nan")
        return (1 + int(np.sum(perm >= real))) / (len(perm) + 1)

    p_mean, p_vol = emp_p(r_m, perm_m), emp_p(r_v, perm_v)

    print("=" * 70)
    print("GDELT×KRYPTO v2 — stündlich, Vola-Kanal, Permutationstest (read-only)")
    print(f"  Lookback {LOOKBACK_DAYS}d | Schock-Tage {len(shock_days)} | "
          f"Symbole {len(sym_arrays)} | Tests real {n_real} | B={B_PERM}")
    print(f"  Pre {PRE_HOURS}h | Post {POST_WINDOWS_H}h")
    print("-" * 70)
    print(f"  MITTELWERT-Kanal:  real |Δμ|={r_m:.5f}  "
          f"placebo Ø={np.mean(perm_m):.5f} / 95%={np.quantile(perm_m,0.95):.5f}  "
          f"-> emp. p={p_mean:.3f}")
    print(f"  VOLA-Kanal:        real Δσ={r_v:+.5f}  "
          f"placebo Ø={np.mean(perm_v):+.5f} / 95%={np.quantile(perm_v,0.95):+.5f}  "
          f"-> emp. p={p_vol:.3f}")
    print("-" * 70)
    sig_m, sig_v = (p_mean < 0.05), (p_vol < 0.05)
    if sig_m or sig_v:
        print(f"  URTEIL: SIGNAL-KANDIDAT — "
              f"{'Mittelwert ' if sig_m else ''}{'Vola' if sig_v else ''} p<0.05.")
        print("  (2 Kanäle getestet -> Bonferroni: p<0.025 für harte Signifikanz. "
              "Cross-Method-Bestätigung Pflicht vor jedem Claim.)")
    else:
        print("  URTEIL: NULL — Schock-Tage bewegen Krypto NICHT über das Zufallsniveau. "
              "Sauberer, non-parametrischer Null-Befund (stärker als der Tages-Test).")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        asyncio.run(main(args.seed))
