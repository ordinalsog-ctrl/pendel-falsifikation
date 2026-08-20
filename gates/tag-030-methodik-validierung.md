# Gate Tag 30 — Methodik-Validierung

**Fälligkeit:** ~1.6.2026 (Tag 30 seit Live-Start 30.4.2026)
**Aggregat-Verdikt:** **2/4 · partial** — Falsifikationsregel (0/4) nicht getriggert
**Letzte Auswertung:** 20.8.2026 (Tag 111), Cockpit-Retest
**Kanonische Kriterien:** [../FALSIFIKATIONSKRITERIEN.md](../FALSIFIKATIONSKRITERIEN.md) §1

> **M3-Self-Critique:**
> - **Quellen:** Ursprünglicher Tag-30-Review (`PENDEL_EVIDENCE_REVIEW_DAY_30.md`, 1.6.2026)
>   und Cockpit-Snapshot 20.8.2026. Nicht in dieser Session aus der DB gezogen.
> - **Caveat 1 (VOID):** Der eigentliche Fälligkeitstermin 1.6.2026 war **nicht messbar** —
>   ein ~10-Tage-Datenloch (22.–24.5. → 1.6.) hatte die Kern-Preisserien tot; das damalige
>   `n_obs=32` war ffill-erfunden (Post-Mortem 1.6.2026). Der Original-Review ist daher als
>   **VOID** annulliert, kein Gate-Resultat. Die hier gezeigten Werte sind der **Retest** auf
>   sauberen Daten (Re-Baseline ab 1.6.).
> - **Caveat 2 (schwacher Pass):** H30.1 misst faktisch die Datenmenge (Tag-Zähler 111), kein
>   inhaltliches Resultat. H30.4 „530 robust" steht in Spannung zu den konsistenten
>   Walk-Forward-**Null**-Befunden der Anti-FOMO-Liste (Headline-Paare stability_adj < 0.3) —
>   siehe Anmerkung H30.4.
> - **Annahme:** „partial" heißt: Pipeline läuft und ist krypto-seitig teilweise beweisfähig;
>   Substanz wird erst Tag 60 geprüft.

---

## Vorab-registrierte Hypothesen (eingefroren)

| ID | Kriterium | Schwelle |
|---|---|---|
| H30.1 | BTC-/Crypto-Block ≥ 30 daily Datapoints | ≥ 30 |
| H30.2 | ≥ 1 PCMCI-Link im Crypto-Block FDR-signifikant (Lag ≥ 1) | ≥ 1 |
| H30.3 | SARIMAX-CF auf FOMC 17.6. zeigt sig. Effekt (FDR/n_post-gegatet) | ≥ 1 |
| H30.4 | Walk-Forward ≥ 1 robust (stability_adj ≥ 0.5, n_significant_adj > 0) | ≥ 1 |

---

## Auswertung an Fälligkeit (Retest-Werte, Cockpit 20.8.2026)

| ID | Ist-Wert | Ziel | Verdikt | Anmerkung |
|---|---|---|---|---|
| H30.1 | 111 | ≥ 30 | ✅ PASS | Retest-Wert (Tag-Zähler). Schwacher, rein volumetrischer Pass. |
| H30.2 | 0 | ≥ 1 | ❌ FAIL | Crypto-PCMCI zählt erst mit Lag ≥ 1; kein Lag-0/Self-Loop-Erfolg. |
| H30.3 | 0 | ≥ 1 | ❌ FAIL | Nur echte FDR/n_post-gegatete Signifikanz zählt; FOMC-17.6.-CF 0 sig. |
| H30.4 | 530 | ≥ 1 | ✅ PASS | stability_adj ≥ 0.5 **und** n_significant_adj > 0 erfüllt. Siehe unten. |

**Anmerkung H30.4:** 530 walk-forward-robuste Patterns über die gesamte Library erfüllen die
Schwelle formal. Gleichzeitig sind die **Headline-Paare** (BTC→SOL, SPY→BTC, GLD→BTC über 180d/1y)
in der Anti-FOMO-Liste über 14 Läufe konsistent **nicht** robust (avg stability_adj 0.00–0.15).
Der Pass ist real, aber es ist Methodik-Validierung (der Job *kann* Robustheit erkennen),
**kein** Substanz-Beleg für ein Pendel-spezifisches Signal. Das prüft Tag 60/90.

---

## Aggregat-Verdikt

**2/4 · partial.** Die Falsifikationsschwelle „0/4 → Compute-Spezifikation prüfen" ist nicht
erreicht. Beide Passes (H30.1 volumetrisch, H30.4 methodisch) belegen: die deskriptive und die
Walk-Forward-Pipeline laufen. Beide Fails (H30.2, H30.3) zeigen: die **krypto- und
event-seitige Kausal-Hypothesen-Schicht** produziert bislang **keine** Signifikanz.

Die Hauptthese ist zu Tag 30 wie erwartet **unbelegt** — das Gate prüft Methodik, nicht Substanz.

---

## Historie

- **1.6.2026 (Tag 30, VOID):** Original-Review nicht als Gate zählbar (10-Tage-Datenloch,
  ffill-inflationiertes n). Re-Baseline auf saubere Daten ab 1.6. Post-Mortem: Liveness-zuerst
  als bindende Prozessregel etabliert.
- **20.8.2026 (Tag 111):** Retest auf sauberen Daten → 2/4.
