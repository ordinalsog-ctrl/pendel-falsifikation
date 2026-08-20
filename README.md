# Pendel — Falsifikations-Dokumentation

Sauberes, vorab-registriertes Falsifikations-Journal für **Pendel** — eine self-hosted,
append-only Pattern-Library an der Schnittstelle **Geopolitik × Krypto × Makro**.

Dieses Repo hat **einen Zweck**: die vor Projektstart festgelegten Falsifikationskriterien
an ihren **Fälligkeitstagen** ehrlich und nachvollziehbar zu dokumentieren — nach
Karpathy-Disziplin (Annahmen explizit, keine Goalpost-Verschiebung, Null-Befunde zählen).

Es ist **keine** Marketing-, Signal- oder Trading-Fläche (Charter §3 Plan B, Anti-Scope).

---

## Die These, die geprüft wird

> **Hauptthese (H₁):** An der Schnittstelle Geopolitik × Krypto × Makro existieren empirisch
> detektierbare, regimeabhängige Lead-Lag-Strukturen, die nach Multiple-Testing-Korrektur und
> Walk-Forward-Validierung robust bleiben — und **nicht** bereits klassisches Lehrbuchwissen
> reproduzieren.

> **Nullhypothese (H₀):** Pendel produziert keine Pendel-spezifischen Befunde, die über
> klassisches Equity-Yield-Vol-Wissen hinausgehen.

**Stand Tag 111 (20.8.2026): H₀ ist nicht abgelehnt.** Pendel liefert derzeit wertvolle
Null-Befunde, keine robusten Pendel-spezifischen Signale. Das ist wissenschaftlich sauber
und Charter-konform (Null-Befund-Track). BD-4 Public Beta bleibt blockiert.

---

## Gate-Kalender (Live-Start: 30.4.2026)

| Gate | Fälligkeit | Tag | Kriterien | Score | Status |
|---|---|---|---|---|---|
| [Tag 30 — Methodik-Validierung](gates/tag-030-methodik-validierung.md) | ~1.6.2026 | 30 | 4 | **2/4** | partial — Falsifikation nicht getriggert |
| [Tag 60 — Pattern-Substanz](gates/tag-060-pattern-substanz.md) | ~1.7.2026 | 60 | 4 | **0/4** | falsification_triggered |
| [Tag 90 — Reproduktion](gates/tag-090-reproduktion.md) | ~1.8.2026 | 90 | 3 | **0/3** ¹ | falsification_triggered |
| [Tag 180 — Charter-Gate](gates/tag-180-charter-gate.md) | ~5.11.2026 | 180 | 3 | 1/3 (Vorab-Check) | pending_precheck |

¹ Der Cockpit-Auto-Score zeigt für Tag 90 „1/3 partial". Die vorab-registrierte, strengere
Lesart und der CEO-Review vom 2.8.2026 werten **0/3** (falsification_triggered). Details und
Begründung: [STATUS.md](STATUS.md) §Diskrepanz-Audit.

---

## Aufbau

```
FALSIFIKATIONSKRITERIEN.md   Vorab-registrierte Kriterien (eingefroren, der Anker)
STATUS.md                    Aktuelle Scorecard (Tag 111) + Diskrepanz-Audit + Evidenzbasis
CONTROLS.md                  Kontrolltage + Integritäts-Invarianten (gegen stille Datenfehler)
gates/
  tag-030-methodik-validierung.md   Kriterien + Auswertung an Fälligkeit + Verdikt
  tag-060-pattern-substanz.md
  tag-090-reproduktion.md
  tag-180-charter-gate.md           Kriterien + Vorab-Check (noch nicht fällig)
```

Jede Gate-Datei ist **eigenständig** und identisch aufgebaut: vorab-registrierte Hypothesen →
Auswertung mit Quellenangabe → Aggregat-Verdikt → Historie → M3-Self-Critique.

---

## Karpathy-Disziplin (verbindlich für dieses Repo)

1. **Kriterien sind eingefroren.** Schwellen aus `FALSIFIKATIONSKRITERIEN.md` werden nach
   Fälligkeit nicht gesenkt. Wer eine Schwelle für unfair hält, dokumentiert das — verschiebt
   sie aber nicht rückwirkend.
2. **Null-Befunde zählen.** Ein sauber falsifizierter Befund ist wertvoller als ein
   herbei­interpretierter Treffer.
3. **„Nicht messbar" ≠ „bestanden" ≠ „gescheitert".** Datenlöcher (siehe Tag-30-Historie)
   werden als VOID markiert, nicht als Pass verbucht.
4. **Jede Zahl mit Quelle + Stand.** Kein Wert ohne Herkunft. Provenienz steht pro Datei
   im M3-Header.
5. **Liveness zuerst.** Vor jeder Bewertung gilt: fließen die Daten? (Lehre aus dem
   10-Tage-Datenloch, Post-Mortem 1.6.2026.)

---

## Wichtiger Provenienz-Hinweis

Die Zahlen in diesem Repo stammen aus dem **Cockpit-Snapshot vom 20.8.2026** (vom Betreiber
bereitgestellt) und den benannten Review-Dokumenten (Tag-30 VOID, Codex-Tag-60 1.7.2026,
Tag-90-Review 2.8.2026). Sie wurden in dieser Doku-Session **nicht** direkt aus der
Produktions-DB gezogen. Bei Abweichung gilt der Live-Server als Wahrheit; dann ist die
betreffende Gate-Datei mit neuem Stand und M3-Header fortzuschreiben (append-only).
