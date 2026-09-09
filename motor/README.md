# GDELT-Cluster-Causal-Motor (H90-Prio 1)

Erweitert die bestehende, getestete SARIMAX-Counterfactual-Methode (`compute_event_impact.py`,
DEC-083/153) auf **GDELT×Krypto** — die geopolitische Achse der These, die bislang **nie** in
die Kausal-Pipeline eingespeist wurde (`EVENT_SOURCES` dort = nur fed/bls/ecb). Ziel: aus einer
*ungetesteten* Null einen *echten, verteidigbaren* Test machen.

> **Kein neues Werkzeug.** Der Motor importiert und nutzt `compute_impact` (die geprüfte
> SARIMAX-CF) unverändert. Neu ist nur: GDELT→Schock-Tage clustern, auf Krypto zielen,
> Placebo-Negativkontrolle, eigene Ergebnis-Tabelle.

## Methode (kurz)
1. GDELT-Events (`source='gdelt'`, `severity>=4`) je UTC-Tag **dedupliziert** (`COUNT(DISTINCT
   event_type,region)`) → tägliche Schock-Intensität. Dedup gegen GDELTs Mehrfachzählung.
2. **Schock-Tag** = Tag mit Intensität ≥ datengetriebener Quantil-Schwelle (Top-Dezil, Floor 3).
3. Pro (Schock-Tag × Krypto × Window 7/30d): SARIMAX-CF via `compute_impact`.
4. **FDR (BH)** über den Batch; `significant` = FDR-reject **und** `n_post≥10` (wie DEC-153).
5. **Negativkontrolle (Placebo):** gleich viele zufällige Nicht-Schock-Tage, gleiche Prozedur.

## Wie man das Ergebnis liest (entscheidend)
Der Motor druckt `real_sig` vs `placebo_sig`:
- **`real_sig >> placebo_sig`** → verteidigbares Signal (Geopolitik-Schocks bewegen Krypto über
  das Zufallsniveau hinaus). Kandidat für H60.4 / H180.1.
- **`real_sig ≤ placebo_sig`** → **kein** Signal (Artefakt/Null). Das ist ein sauberer,
  publizierbarer Null-Befund — genau so wertvoll, nur ehrlich.

## Deploy — Reihenfolge ist Pflicht (Karpathy: Dry-Run vor enable)
Alles auf `pendel-prod`, als root. **Nichts wird geschrieben ohne `--write`.**

```bash
# 0) Dateien auf den Server holen (aus dem public Repo)
cd /opt/pendel/daemon
for f in compute_gdelt_cluster_impact.py schema_gdelt_cluster_impact.sql; do
  curl -fsSL "https://raw.githubusercontent.com/ordinalsog-ctrl/pendel-falsifikation/main/motor/$f" -o "/opt/pendel/daemon/$f"
done
chown pendel:pendel /opt/pendel/daemon/compute_gdelt_cluster_impact.py

# 1) DRY-RUN (schreibt NICHTS, druckt real_sig vs placebo_sig + Top-Effekte)
sudo -u pendel /opt/pendel/venv/bin/python /opt/pendel/daemon/compute_gdelt_cluster_impact.py 2>&1 | tail -30
```

**Erst nach Review der Dry-Run-Ausgabe** und nur wenn sie plausibel ist:

```bash
# 2) Schema anlegen (idempotent)
sudo -u postgres psql -d pendel -f /opt/pendel/daemon/schema_gdelt_cluster_impact.sql

# 3) EINMAL schreiben
sudo -u pendel /opt/pendel/venv/bin/python /opt/pendel/daemon/compute_gdelt_cluster_impact.py --write 2>&1 | tail -20
```

Timer (`pendel-gdelt-cluster-impact.{service,timer}`, analog `pendel-event-impact`) kommt **erst**,
wenn der Write-Lauf sauber durch ist — nicht vorher.

## Offene Design-Entscheidungen (bewusst, für Review)
- **Daily returns** (wie `event_impact`) für die erste Version — reuse der geprüften Pipeline.
  Falls unterpowert: Upgrade auf **stündliche** Krypto-Returns (Krypto reagiert in Stunden,
  nicht Tagen) als v2. Bewusst nicht sofort, um sauber/reviewbar zu starten (Karpathy P2).
- **Schwelle** ist quantil-basiert (nicht handgetunt); die Placebo-Kontrolle ist der Schutz
  gegen schwellen-induzierte Scheinstruktur.
- **event_ts = Tagesbeginn** des Schock-Tags; pre 60d, post 7/30d.

Alle Zahlen, die dieser Motor erzeugt, sind erst nach Placebo-Vergleich + FDR belastbar.
