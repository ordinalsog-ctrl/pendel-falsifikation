# Pendel — Falsifikationskriterien (vorab-registriert, eingefroren)

**Vorab-Registrierung:** 8.5.2026 (Tag 8), Quelle `PENDEL_FALSIFIKATIONS_KRITERIEN.md`
**Charter-Bezug:** §3 Plan B, §3a M3-Self-Critique, DEC-009 (Daten-Integrität oberste Constraint)
**Status dieser Datei:** ANKER. Schwellen sind eingefroren und werden nach Fälligkeit nicht geändert.

> **M3-Self-Critique:** Diese Datei ist die kanonische, unveränderliche Referenz der vorab
> festgelegten Schwellen. Sie enthält bewusst **keine** Ist-Werte — die stehen ausschließlich
> in den Gate-Auswertungen unter `gates/`. Trennung von Regel (hier) und Messung (dort)
> verhindert Goalpost-Shifting.

---

## 0. These und Nullhypothese

- **H₁ (Hauptthese):** An der Schnittstelle Geopolitik × Krypto × Makro existieren empirisch
  detektierbare, regimeabhängige Lead-Lag-Strukturen, die nach Multiple-Testing-Korrektur
  und Walk-Forward-Validierung robust bleiben — und nicht bereits klassisches Lehrbuchwissen
  reproduzieren.
- **H₀ (Null):** Pendel produziert keine Pendel-spezifischen Befunde, die über klassisches
  Equity-Yield-Vol-Wissen hinausgehen.
- **Reaktion bei H₀-Bestätigung nach Soak:** Charter §3 Plan B — Pendel wird als methodisch
  sauberer Null-Befund-Generator dokumentiert, nicht als gescheitertes Programm.

---

## 1. Tag 30 (~1.6.2026) — Methodik-Validierung

| ID | Kriterium | Schwelle |
|---|---|---|
| H30.1 | BTC-/Crypto-Block hat genügend Daten für Multivariat-Analyse | ≥ 30 daily Datapoints |
| H30.2 | Mindestens 1 PCMCI-Link im Crypto-Block ist FDR-signifikant (Lag ≥ 1) | ≥ 1 |
| H30.3 | SARIMAX-Counterfactual auf FOMC-Decision (17.6.2026) zeigt sig. Effekt (FDR/n_post-gegatet) | ≥ 1 |
| H30.4 | Walk-Forward-Validation hat ≥ 1 robusten Pattern (stability_adj ≥ 0.5, n_significant_adj > 0) | ≥ 1 |

**Falsifikationsregel:** Wenn **0/4** → methodische Spezifikation der Compute-Jobs prüfen.

> *Historie H30.3:* Ursprünglich als „SARIMAX-CF auf Pre-1.6.-Macro-Events" formuliert
> (Forward-Lookup-Bug: FOMC 17.6. liegt hinter dem Tag-30-Termin 1.6.). Der FOMC-17.6.-Test
> wurde zum Tag-60-Backlog (H60.5) verschoben und wird im Cockpit-Retest unter H30.3 mit
> jetzt vorliegenden Post-Event-Daten geführt.

---

## 2. Tag 60 (~1.7.2026) — Pattern-Substanz

| ID | Kriterium | Schwelle |
|---|---|---|
| H60.1 | Pendel-spezifische Lead-Lag-Beziehungen, nicht in Standard-Finanzliteratur (verified novelty, nicht „unknown") | ≥ 10 |
| H60.2 | Pattern-of-the-Week: high-confidence Patterns (n ≥ 100), FDR + Walk-Forward-stabil | ≥ 5 |
| H60.3 | Macro-Regime-Tagging klassifiziert unterschiedliche echte Regimes (nicht „unclear") | ≥ 3 |
| H60.4 | GDELT-Geopolitik-Cluster mit messbarem Causal-Impact auf Crypto (echte Signifikanz, nicht Makro-Release) | ≥ 1 |

**Falsifikationsregel:** Wenn **0/4 oder 1/4** → Hauptthese ist schwach; Pendel als
Null-Befund-Studie evaluieren.

---

## 3. Tag 90 (~1.8.2026) — Reproduktion

| ID | Kriterium | Schwelle |
|---|---|---|
| H90.1 | ≥ 1 eingefrorenes Tag-60-Pattern bleibt nach 30 Tagen FDR + WF-robust (Out-of-Sample, keine Cherry-Picks) | ≥ 1 frozen & reproduced |
| H90.2 | Cross-Method-Konsistenz: identisches cause/effect/time_window in Granger UND VAR-Granger UND PCMCI sig | ≥ 1 |
| H90.3 | Strukturbruch-Detektion erkennt echten Markt-Regime-Wechsel (Breakpoint **plus** Regime-Bestätigung) | ≥ 1 bestätigt |

**Falsifikationsregel:** Wenn **0/3** → Charter §3 BD-4 Public-Beta bleibt blockiert.

> *Präzisierung H90.3:* Reine Breakpoints (ruptures) reichen **nicht**. Es zählt nur ein
> Bruch, der zusätzlich durch ein Macro-Regime-Signal als echter Regimewechsel bestätigt ist.

---

## 4. Tag 180 (~5.11.2026) — Charter-Gate (intern, kein Public-Trigger)

| ID | Kriterium | Schwelle |
|---|---|---|
| H180.1 | Dokumentierte Pendel-spezifische Patterns mit Cross-Method-Validation (verified novelty) | ≥ 3 |
| H180.2 | Robuste Performance über unterschiedliche Macro-Regimes | ≥ 2 Regimes |
| H180.3 | Pattern-of-the-Week hat high-confidence Patterns akkumuliert | ≥ 20 |

**Falsifikationsregel:** Wenn **0/3 oder 1/3** → BD-4 + BD-5 blockiert; Charter-Pivot zur
Null-Befund-Studie.

**Public-Trigger-Klarstellung (DEC-124):** Tag 180 ist ein **interner** Methodik-Checkpoint.
Public-Aktivierung erfordert kumulativ (1) Tag-180-PASS **und** (2) ≥ 1 Jahr Stabilität —
frühester realistischer Termin **30.4.2027**.

---

## 5. Methodik-Hierarchie (Claim-Ebenen)

- **L0–L1 Deskriptiv:** Pearson/Spearman, data_quality, Strukturbrüche, event_reactions.
- **L2–L3 Predictive:** Granger + FDR (bivariat) → VAR + IRF + FEVD (multivariat) + Walk-Forward.
- **L4 Causal Hypothesis:** PCMCI + SARIMAX Event-Counterfactual + Macro-Regime (unter Annahmen).
- **L5 Causal Identification:** DAGs / IV / RCT — **bewusst NICHT in Pendel** (Anti-Scope DEC-003).

Sprachregel: Granger ≠ Kausalität. „X enthält prognostische Information für Y" statt
„X verursacht Y".

---

*Eingefroren 8.5.2026. Änderungen an Schwellen sind nur als neuer, datierter Abschnitt mit
Begründung zulässig (append-only) und heben eine bereits erfolgte Gate-Bewertung nicht auf.*
