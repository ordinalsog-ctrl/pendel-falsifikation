# Pattern-of-the-Week — Crash-Fix + Reaktivierung (H180.3)

**Zweck:** PoW war seit 6.5. disabled (DEC-119), weil der Job im 30-min-Timeout crasht. H180.3
(„≥20 high-confidence PoW-Patterns akkumuliert") kann so nie ein *fairer* Test werden — es steht
strukturell 0, egal ob Substanz da wäre. Dieser Fix macht H180.3 zu einem echten Test.

## Ursache (aus dem Code)
`pattern_of_the_week.py.run()` → `fetch_robust_patterns` liefert **alle ~217k** Patterns (n≥30),
dann `evaluate_robustness` **pro Pattern** (1 DB-Query + 1000er-Bootstrap). ~217k Round-Trips +
~217M Resamples ⇒ Timeout (Karpathy-#38, Service-Wachstum).

## Fix (chirurgisch)
`pattern_of_the_week_fast.py` importiert **alle** getesteten Funktionen aus `pattern_of_the_week.py`
und ändert nur die Orchestrierung: provisorischer Score ohne divergence (obere Schranke, `true ≤ prov`)
→ **Top-K=300** vorselektieren → teurer Cross-Check nur für die K. 217k → 300. Original-Datei bleibt
unangetastet. **Kein DB-Write** (schreibt nur einen Markdown-Bericht).

## Deploy — Reihenfolge Pflicht (Verify vor enable)
Auf `pendel-prod`:

```bash
# 1) Fix-Datei holen
curl -fsSL "https://raw.githubusercontent.com/ordinalsog-ctrl/pendel-falsifikation/main/pow/pattern_of_the_week_fast.py" -o /opt/pendel/daemon/pattern_of_the_week_fast.py
chown pendel:pendel /opt/pendel/daemon/pattern_of_the_week_fast.py

# 2) VERIFY: manueller Lauf nach /tmp (kein DB-Write). Muss in SEKUNDEN durch sein, nicht 30 min.
time sudo -u pendel /opt/pendel/venv/bin/python /opt/pendel/daemon/pattern_of_the_week_fast.py --out-dir=/tmp/pow-test 2>&1 | tail
head -40 /tmp/pow-test/*.md
```

**Erst wenn der Verify-Lauf schnell (< ~1 min) durchläuft und ein sinnvoller Bericht rauskommt** —
Reaktivierung:

```bash
# 3) Units installieren
for f in pendel-pattern-of-the-week.service pendel-pattern-of-the-week.timer; do
  curl -fsSL "https://raw.githubusercontent.com/ordinalsog-ctrl/pendel-falsifikation/main/pow/$f" -o "/etc/systemd/system/$f"
done
mkdir -p /opt/pendel/reports/pattern-of-the-week && chown -R pendel:pendel /opt/pendel/reports/pattern-of-the-week
systemctl daemon-reload
systemctl start pendel-pattern-of-the-week.service   # ein echter Lauf
systemctl status pendel-pattern-of-the-week.service --no-pager | head -5
# wenn sauber -> Timer scharf:
systemctl enable --now pendel-pattern-of-the-week.timer
systemctl list-timers --all | grep pattern-of-the-week
```

## Ehrliche Einordnung
Der Fix macht H180.3 **testbar**, er erzeugt **kein** Signal. PoW promotet nur, was die
Promotion-Hürden ohnehin passiert; bei aktuell 0 novel/robusten Pendel-Patterns wird der
Wochenbericht dünn sein — das ist korrekt und ehrlich (Anti-Hype). H180.3 wird damit ein
*fairer* Null-/Substanz-Test statt eines Klempnerei-Fails.
