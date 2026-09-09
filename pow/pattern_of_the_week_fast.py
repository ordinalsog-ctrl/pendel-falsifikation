"""Pattern of the Week — Crash-Fix (Karpathy-#38 / DEC-060 / DEC-119).

PROBLEM: `pattern_of_the_week.py.run()` holt ALLE ~217k robust patterns (n>=30) und
ruft dann PRO Pattern `evaluate_robustness` auf (1 DB-Query + 1000er-Bootstrap je Pattern)
=> 217k DB-Round-Trips + ~217M Resamples => 30-min-Timeout-Crash (seit 6.5., disabled DEC-119).

FIX (chirurgisch, reuse aller getesteten Funktionen aus pattern_of_the_week.py):
  1. Provisorischen Score OHNE divergence in-memory für alle Kandidaten
     (compute_score behandelt divergence=None als 0 => OBERE SCHRANKE, da true_score <= prov_score,
      weil der (1-divergence)-Faktor den Score nur senkt).
  2. Top-K=PRESELECT_K nach prov_score vorselektieren.
  3. Teuren Cross-Check (DB-Fetch + Bootstrap + echte divergence) NUR für diese K.
  => 217k -> 300 Round-Trips. Korrekt, weil die echten Top-Patterns garantiert in den Top-K
     nach prov_score liegen (true <= prov). Anzeige braucht ohnehin nur ~10-30 (max 3/Symbol).

Kein DB-Write (liest event_patterns/event_reactions, schreibt nur eine Markdown-Datei).
Import-only-Aenderung: das Original pattern_of_the_week.py bleibt unangetastet.

Usage:
    python pattern_of_the_week_fast.py [--out-dir=...] [--week=YYYY-WW] [--seed=42]
"""
from __future__ import annotations
import argparse
import asyncio
from datetime import datetime, timezone
from pathlib import Path

import asyncpg
import numpy as np

import pattern_of_the_week as base  # reuse: DSN, fetch_robust_patterns, evaluate_robustness,
                                    # compute_score, apply_diversity_filter, render_markdown, Konstanten

PRESELECT_K = 300   # obere Schranke; Anzeige braucht <=30 -> massiv Puffer


async def run(out_dir: str, week_label: str | None, seed: int) -> str:
    np.random.seed(seed)
    pool = await asyncpg.create_pool(base.DSN, min_size=1, max_size=4)
    try:
        async with pool.acquire() as conn:
            stats_row = await conn.fetchrow(
                """
                SELECT COUNT(*) AS total,
                       COUNT(*) FILTER (WHERE n_observations >= 30) AS robust,
                       COUNT(*) FILTER (WHERE n_observations >= 100) AS high
                FROM event_patterns
                """)
        pattern_lib_stats = dict(stats_row)

        candidates = await base.fetch_robust_patterns(pool)

        # (1) provisorischer Score ohne divergence (obere Schranke), in-memory, billig
        for p in candidates:
            p.cv = abs(p.std_pct / p.mean_pct) if p.mean_pct != 0 else float("inf")
            p.score = base.compute_score(p)  # divergence=None -> 0

        # (2) Top-K vorselektieren
        preselect = sorted(candidates, key=lambda p: -p.score)[:PRESELECT_K]

        # (3) teurer Cross-Check NUR fuer die K (setzt echte divergence + score + gates)
        for p in preselect:
            await base.evaluate_robustness(pool, p)

        qualified = [p for p in preselect if p.passes_gates]
        disqualified = [p for p in preselect if not p.passes_gates and p.disqualification_reason]

        qualified.sort(key=lambda p: -p.score)       # jetzt echte Scores
        disqualified.sort(key=lambda p: -abs(p.mean_pct))
        qualified = base.apply_diversity_filter(qualified, base.MAX_PATTERNS_PER_SYMBOL)

        now = datetime.now(timezone.utc)
        if week_label is None:
            iso = now.isocalendar()
            week_label = f"KW {iso.week:02d}/{iso.year}"
        md = base.render_markdown(qualified, disqualified, pattern_lib_stats, week_label, now)

        out_path = Path(out_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        iso = now.isocalendar()
        target = out_path / f"{iso.year}-{iso.week:02d}.md"
        target.write_text(md, encoding="utf-8")
        return str(target)
    finally:
        await pool.close()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="/tmp/pendel-pow-reports")
    ap.add_argument("--week", default=None)
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()
    out = asyncio.run(run(a.out_dir, a.week, a.seed))
    print(f"Pattern of the Week report written: {out}")


if __name__ == "__main__":
    main()
