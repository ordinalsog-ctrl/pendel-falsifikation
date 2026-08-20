# Gate Tag 90 — Reproduktion

**Fälligkeit:** ~1.8.2026 (Tag 90 seit Live-Start 30.4.2026)
**Aggregat-Verdikt:** **0/3 · falsification_triggered** (vorab-registrierte, strenge Lesart)
**Formaler Review:** 2.8.2026 (Tag 93), `PENDEL_H90_REVIEW_2026-08-02.md` — CEO-Entscheidung
**Kanonische Kriterien:** [../FALSIFIKATIONSKRITERIEN.md](../FALSIFIKATIONSKRITERIEN.md) §3

> **M3-Self-Critique:**
> - **Quellen:** Formaler H90-Review 2.8.2026 (CEO/Science-Entscheidung) und Cockpit 20.8.2026.
> - **Diskrepanz (bewusst so gewertet):** Der Cockpit-Auto-Score zeigt „1/3 · partial", weil
>   er H90.3 mit 3316 Breakpoints ≥ 1 zählt. Die **vorab-registrierte** Schwelle verlangt aber
>   „≥ 1 Breakpoint **plus** Regime-Bestätigung"; reine Breakpoints reichen laut Kriterium
>   nicht. Der formale Review vom 2.8. wertet H90.3 korrekt als FAIL und das Gate als **0/3**.
>   Dieses Repo folgt der strengen, vorab-registrierten Lesart (kein Goalpost-Shift). Die
>   Cockpit-Zählung ist ein Anzeige-Artefakt, keine gültige Gate-Bewertung → siehe
>   [../STATUS.md](../STATUS.md) §Diskrepanz-Audit.
> - **Annahme:** „falsification_triggered" ist die verbindliche Bewertung; die CEO-Entscheidung
>   vom 2.8. hat sie ratifiziert (BD-4 blockiert, Null-Befund-Track).

---

## Vorab-registrierte Hypothesen (eingefroren)

| ID | Kriterium | Schwelle |
|---|---|---|
| H90.1 | ≥ 1 eingefrorenes Tag-60-Pattern nach 30 Tagen FDR + WF-robust (Out-of-Sample) | ≥ 1 frozen & reproduced |
| H90.2 | Cross-Method-Konsistenz: Granger UND VAR-Granger UND PCMCI sig (identisch) | ≥ 1 |
| H90.3 | Strukturbruch **plus** echte Regime-Bestätigung | ≥ 1 bestätigt |

---

## Auswertung an Fälligkeit (formaler Review 2.8.2026 + Cockpit 20.8.2026)

| ID | Ist-Wert | Ziel | Verdikt | Anmerkung |
|---|---|---|---|---|
| H90.1 | 0 | ≥ 1 | ❌ FAIL | Freeze-Datei `tag90_frozen_candidates_20260719.json` enthält keine reproduzierbaren Kandidaten. Keine nachträglichen Cherry-Picks. |
| H90.2 | 0 | ≥ 1 | ❌ FAIL | Keine identische cause/effect/time_window-Schnittmenge in Granger ∧ VAR ∧ PCMCI. `cross_method_triple` = 0. |
| H90.3 | 3316 Breakpoints / 0 bestätigt | ≥ 1 bestätigt | ❌ FAIL | Breakpoints allein zählen nicht; 0 bestätigte echte Regimewechsel. Cockpit zeigt hier fälschlich „partial". |

---

## Aggregat-Verdikt

**0/3 · falsification_triggered.** Regel: „Wenn 0/3 → Charter §3 BD-4 Public-Beta bleibt
blockiert." Ausgelöst und am 2.8.2026 per CEO-Entscheidung ratifiziert.

**CEO/Science-Entscheidung (2.8.2026):**
- BD-4 Public Beta bleibt blockiert.
- Pendel wird bis auf Weiteres als **Null-Befund-Track** geführt, nicht als Discovery-/Signal-Produkt.
- Keine Pendel-spezifischen Lead-Lag-Claims nach außen.
- Tag 180 bleibt Charter-Gate, aber nur mit echter externer Evidenz-Erweiterung.

Wichtige Einordnung: Die aktuelle Evidenz falsifiziert **nicht**, dass solche Strukturen
existieren *könnten*. Sie falsifiziert den **Produktanspruch**, dass Pendel nach 90 Tagen
bereits robuste, Pendel-spezifische Befunde oberhalb klassischem Equity-Yield-Vol-Wissen
liefert.

---

## Historie

- **2.8.2026 (Tag 93):** Formaler Review, 0/3, `BD-4_PUBLIC_BETA_BLOCKED_H90_FAILED_NULL_FINDING_TRACK`.
  Betriebsfix am selben Tag: `pendel-patterns.service` `DiskFullError` behoben
  (Timer 03:00 → 06:05 UTC, Backup-Retention bereinigt); Re-Run erfolgreich
  (n_patterns 1.002.148 → 1.040.493).
- **20.8.2026 (Tag 111):** Cockpit zeigt Auto-Score „1/3 partial" (Breakpoint-Zählung).
  Bindend bleibt die vorab-registrierte Lesart **0/3**.
