# Tag-180 Endspurt — Optimaler Einsatz (vorab-registriert)

**Erstellt:** 9.9.2026 (Tag 132) · **Zieldatum:** ~5.11.2026 (Tag 180) · **Fenster:** ~57 Tage
**Zweck:** Festlegen, **wo** wir bis zur Fälligkeit Aufwand investieren, damit Tag 180 die
bestmögliche Auswertung trägt.

> **M3-Self-Critique:** Dieser Plan registriert den **Einsatz** vorab — er ändert **nichts** an
> den eingefrorenen Falsifikationskriterien (`FALSIFIKATIONSKRITERIEN.md`). Das ist die
> Anti-Drift-Sicherung: Effort wird gegen diesen Plan gemessen, damit „optimaler Einsatz" nicht
> in nachträgliches Cherry-Picking kippt. Kein Item senkt eine Schwelle.

## 0. Was „bestes Ergebnis" heißt (verbindliche Definition)
Bei einem Falsifikationsprojekt ist das beste Ergebnis der **maximal fähige, maximal saubere
Test**: er findet ein echtes Signal, *wenn* eins existiert, und liefert sonst einen
wasserdichten, publizierbaren Null-Befund. **Garantierbar ist die Testqualität, nicht das
Vorzeichen.** Ein herbeigeschriebenes „signifikant" wäre der einzige echte Fehlschlag.

## 1. Einsatz nach ROI (absteigend)

| Prio | Einsatz | EV / Begründung | Gate | Deadline |
|---|---|---|---|---|
| **1** | **GDELT-Cluster-Motor + Negativkontrollen** — Cluster statt Einzelevent, deduplizierte Event-Keys, Crypto-Targets, stündliche Returns, SARIMAX-CF + FDR, Random-Window/Shuffled-Event-Controls | Höchster EV für einen *novel* Treffer (ungenutzter Kern der These); Controls machen Treffer verteidigbar | H60.4, H180.1 | Motor läuft ~20.9. |
| **2** | **Novelty-Lock** — Lehrbuch-/Klassik-Muster maschinenlesbar sperren; `unknown`→`verified` nur nach Evidenzprüfung | Einziger Pfad zu `strict_novel_leadlag`>0; behandelt die 471 unknowns ehrlich | H60.1, H180.1 | ~20.9. |
| **3** | **Kandidat vorab einfrieren** — n≥100 in-sample, VOR dem Out-of-Sample-Fenster | Ohne Pre-Freeze keine saubere Reproduktion/Cross-Method | H90.1, H180.1 | **~5.10.** |
| **4** | **PoW Crash-Fix + Reaktivierung** — Timeout-Crash beheben (Karpathy-#38), Promotion-Hürden aktiv (≥4 Methoden, n≥100, kein Klassiker, reproduzierbar) | Macht H180.3 zum fairen Test; berichtet, was 1+2 liefern | H180.3 | ~5.10. |
| **5** | **Power laufen lassen, Liveness grün halten, Reboot bewusst legen** | Passiv; kein Datenloch darf die Runway fressen | alle | laufend |

**Bewusst NICHT:** Funding-Gap-Fix (Sekundär-Layer, kein Gate-Bezug), Kosmetik,
Schwellen-Änderungen. Alles davon wäre Aufwand ohne Pfad-Beitrag oder Drift.

## 2. Kritischer Pfad
```
9.9. ──► GDELT-Motor + Novelty-Lock bauen (Prio 1+2) ──► ~20.9. Motor liefert Kandidaten
     ──► besten Kandidaten einfrieren (Prio 3) ~5.10. ──► OOS-Fenster ──► 5.11. Tag-180-Auswertung
PoW-Fix (Prio 4) parallel bis ~5.10., damit H180.3 4 Wochen akkumulieren kann.
```

## 3. Non-Negotiables (sonst ist der Test nicht „sauber")
- **Negativkontrollen** (Random-Windows, Shuffled-Events) in den Motor — sonst ist ein Treffer
  nicht von Artefakt unterscheidbar.
- **FDR / Multiple-Testing-Korrektur** auf allen Lead-Lag-/Impact-Tests.
- **Pre-Freeze vor OOS** — kein nachträgliches Cherry-Picking.
- **Kriterien eingefroren**, Liveness-zuerst vor jeder Bewertung (CONTROLS.md I1–I6).
- **Bau gegen echtes Schema**, mit Backup (DEC-070) und Dry-Run vor `enable`.

## 4. Ehrliche Erwartung
Die Anti-FOMO-Historie (14 Läufe konsistent nicht-signifikant auf den klassischen Paaren)
deutet auf einen **belastbaren Null-Befund** auf dem Bekannten hin. Der echte neue Schuss ist
die **GDELT-Cluster-Ebene** — dort ist die These bisher praktisch ungetestet. Ausgang offen;
beide Ausgänge (verteidigbarer Treffer ODER wasserdichter Null) sind das Ziel dieses Plans.

## 5. Fallback (vorab-registriert, kein Goalpost-Shift)
Falls die Datenreife für einen der Tests am 5.11. knapp ist: den *finalen Entscheid*
daten-konditioniert leicht nach Tag 180 legen (Codex-Empfehlung 1.7.), **ohne** Kriterien zu
senken. Nur der Zeitpunkt der bindenden Entscheidung wird an „n≥100 bestätigt" gekoppelt.

---
*Vorab-registriert 9.9.2026. Fortschreibung append-only. Änderungen an Prioritäten nur als
datierter Zusatz mit Begründung.*
