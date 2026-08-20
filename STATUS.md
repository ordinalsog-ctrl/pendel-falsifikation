# Pendel — Status & Falsifikations-Audit

**Stand:** 20.8.2026 (Tag 111 seit Live-Start 30.4.2026)
**Quelle:** Cockpit-Snapshot 20.8.2026 + Review-Dokumente (Tag-30 VOID, Codex-Tag-60 1.7.2026,
H90-Review 2.8.2026). Nicht in dieser Session aus der DB gezogen.

> **M3-Self-Critique:** Dieses Dokument aggregiert vier Gate-Auswertungen und macht drei
> Inkonsistenzen zwischen Cockpit-Auto-Score und vorab-registrierten Kriterien explizit
> (§2 Diskrepanz-Audit). Es fügt **keine** neuen Messungen hinzu; alle Zahlen stammen aus den
> verlinkten Gate-Dateien und dem Snapshot. Bewertungsregel bei Konflikt Cockpit vs.
> Vorab-Registrierung: **die vorab-registrierte, strengere Lesart gewinnt** (kein Goalpost-Shift).

---

## 1. Scorecard (alle Gates, alle Kriterien)

| Gate | Kriterium | Ist | Ziel | Verdikt |
|---|---|---|---|---|
| **Tag 30** (2/4, partial) | H30.1 Crypto-Block ≥ 30 daily | 111 | ≥ 30 | ✅ |
| | H30.2 PCMCI-Link sig (Lag ≥ 1) | 0 | ≥ 1 | ❌ |
| | H30.3 SARIMAX-CF FOMC 17.6. sig | 0 | ≥ 1 | ❌ |
| | H30.4 Walk-Forward robust | 530 | ≥ 1 | ✅ |
| **Tag 60** (0/4, falsified) | H60.1 Novel Lead-Lag | 0 | ≥ 10 | ❌ |
| | H60.2 PoW high-conf (n ≥ 100) | 0 | ≥ 5 | ❌ |
| | H60.3 Macro-Regimes | 2 | ≥ 3 | ❌ |
| | H60.4 GDELT→Crypto Causal | 0 | ≥ 1 | ❌ |
| **Tag 90** (0/3, falsified) | H90.1 Frozen Pattern reproduced | 0 | ≥ 1 | ❌ |
| | H90.2 Cross-Method triple | 0 | ≥ 1 | ❌ |
| | H90.3 Strukturbruch + Regime-Bestätigung | 3316 / 0 bestätigt | ≥ 1 bestätigt | ❌ |
| **Tag 180** (1/3, pending) | H180.1 Cross-Method novelty | 0 | ≥ 3 | ❌ |
| | H180.2 ≥ 2 Macro-Regimes | 2 | ≥ 2 | ⚠️ (fragil) |
| | H180.3 PoW akkumuliert | 0 | ≥ 20 | ❌ |

**Erfüllte Kriterien gesamt: 4 von 14** (Tag 30: H30.1, H30.4; Tag 180-Vorab: H180.2 fragil;
+ H30.1 volumetrisch). Kein einziger davon ist ein **Pendel-spezifischer Substanz-Befund** —
alle vier sind volumetrisch (Datenmenge), methodisch (der Job läuft) oder fragil (Regime-Zählung).

---

## 2. Diskrepanz-Audit (Cockpit-Auto-Score vs. Kriterien)

Drei Stellen, an denen der Cockpit-Auto-Score von der vorab-registrierten Lesart abweicht.
In allen dreien gilt die strengere, vorab festgelegte Bewertung.

**D1 — Tag 90: Cockpit „1/3 partial" vs. Kriterium „0/3".**
Cockpit zählt H90.3 mit 3316 Breakpoints ≥ 1 als Teilerfolg. Die Schwelle verlangt
„Breakpoint **plus** Regime-Bestätigung"; 0 bestätigte Regimewechsel → FAIL. Der formale
CEO-Review (2.8.2026) wertet korrekt **0/3, falsification_triggered**. → Anzeige-Artefakt im
Cockpit; die Gate-Datei folgt der Kriterien-Lesart.

**D2 — Tag 60: Degradation 1/4 → 0/4 wird im aktuellen Snapshot nicht sichtbar.**
Am 1.7.2026 stand H60.4 auf 2 (PASS, Gate 1/4). Bis 2.8./20.8. ist H60.4 auf 0 gefallen
(Gate 0/4). Ein Snapshot allein zeigt nur „0/4" — die *Verschlechterung über Zeit* ist die
eigentliche Nachricht und in [gates/tag-060-pattern-substanz.md](gates/tag-060-pattern-substanz.md)
§Historie dokumentiert. (Beide Werte triggern ohnehin die Falsifikationsregel.)

**D3 — Regime-Zählung inkonsistent zwischen Gates.**
H60.3 zeigt „2" bei Schwelle ≥ 3 (FAIL). H180.2 zeigt „2" bei Schwelle ≥ 2 (PASS). Der
H90-Snapshot nennt `macro_regimes_total = 2`, `non_unclear = 1`. Ob 2 echte (nicht-„unclear")
Regimes existieren, ist **nicht gesichert** → H180.2 ist ein fragiler Vorab-Pass, kein
belastbarer Treffer. Zu klären vor der Tag-180-Fälligkeit.

---

## 3. Evidenzbasis (Kontext, Cockpit 20.8.2026 / H90-Review 2.8.2026)

| Kennzahl | Wert | Bedeutung |
|---|---|---|
| Robuste Patterns (n ≥ 30) | 216.291 | Volumen-Indikator, **kein** Robustheits-Beleg |
| high-confidence (n100) | 100.659 | deskriptiv, nicht promotet |
| Korrelationen (n_pair ≥ 30) | 568 | deskriptiv |
| high-confidence **novel** Patterns | **0** | Evidence-Registry: kein Pendel-spezifischer Treffer |
| crypto_pcmci_significant | 0 | Kausal-Hypothese krypto-seitig leer |
| cross_method_triple | 0 | keine Granger∧VAR∧PCMCI-Schnittmenge |
| gdelt_crypto_impact | 0 | Geopolitik-Teil der These unbelegt |
| Top-Patterns Evidence-Registry | klassisch | SPY-QQQ-VIX-Triangle (Lehrbuch) |

**Anti-FOMO (was Pendel hart geprüft und *widerlegt* hat):** u.a. „BTC→SOL Walk-Forward robust"
(14 Läufe alle stability_adj < 0.3), „ETH→BTC Granger FDR-sig" (14 Läufe alle nicht-sig),
„FOMC hat Causal-Impact auf BTC/ETH" (SARIMAX konsistent nicht-sig). Diese Null-Befunde sind
der derzeit belastbarste Output des Systems.

---

## 4. Bottom Line

- **H₀ ist zu Tag 111 nicht abgelehnt.** Kein robuster, Pendel-spezifischer Befund oberhalb
  klassischem Equity-Yield-Vol-Wissen.
- **Gates:** Tag 30 partial (Methodik ok), Tag 60 falsified, Tag 90 falsified, Tag 180 auf
  1/3-Kurs (fragil).
- **Produktkonsequenz (steht):** BD-4 Public Beta blockiert; Null-Befund-Track; kein „causal"-
  Wording außerhalb L4-Hypothese; nach außen nur: Pendel ist eine frühe, strenge
  Falsifikations- und Beobachtungsmaschine.
- **Das ist kein Scheitern.** Ein methodisch sauberer Null-Befund über 111 Tage mit 17
  Konnektoren und 4-Ebenen-Methodik ist eine eigenständige, publizierbare Aussage
  (Charter §3 Plan B).

**Statistische Aussagekraft ab 6+ Monaten Daten** (≈ Ende Oktober 2026). Vor der
Tag-180-Fälligkeit sind die drei Prioritäten aus
[gates/tag-180-charter-gate.md](gates/tag-180-charter-gate.md) abzuarbeiten, sonst ist der
Charter-Pivot zur Null-Befund-Studie der erwartbare Ausgang.
