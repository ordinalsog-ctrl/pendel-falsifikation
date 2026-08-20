# Gate Tag 180 — Charter-Gate (noch nicht fällig)

**Fälligkeit:** ~5.11.2026 (Tag 180 seit Live-Start 30.4.2026)
**Status:** **pending_precheck** — 69 Tage offen (Stand Tag 111)
**Vorab-Check-Stand:** 1/3 (Cockpit 20.8.2026, **nicht** bindend — Gate erst zur Fälligkeit)
**Kanonische Kriterien:** [../FALSIFIKATIONSKRITERIEN.md](../FALSIFIKATIONSKRITERIEN.md) §4

> **M3-Self-Critique:**
> - **Dies ist keine Gate-Bewertung.** Tag 180 ist erst am ~5.11.2026 fällig. Die Zahlen unten
>   sind ein **Vorab-Check** (Trajektorie), kein Pass/Fail. Die endgültige Auswertung wird an
>   der Fälligkeit hier append-only nachgetragen.
> - **Fragiler Vorab-Pass H180.2:** „2 Regimes" erfüllt die Schwelle (≥ 2) formal, steht aber
>   in Spannung zu H60.3 (dort „2" bei Schwelle ≥ 3 = FAIL) und zum H90-Snapshot
>   (`macro_regimes_non_unclear = 1`). Ob 2 echte, nicht-„unclear"-Regimes vorliegen, ist
>   nicht gesichert. Der Vorab-Pass ist daher schwach. Siehe [../STATUS.md](../STATUS.md).
> - **Quellen:** Cockpit 20.8.2026, H90-Review 2.8.2026.

---

## Vorab-registrierte Hypothesen (eingefroren)

| ID | Kriterium | Schwelle |
|---|---|---|
| H180.1 | Dokumentierte Pendel-spezifische Patterns mit Cross-Method-Validation (verified novelty) | ≥ 3 |
| H180.2 | Robuste Performance über unterschiedliche Macro-Regimes | ≥ 2 Regimes |
| H180.3 | Pattern-of-the-Week akkumuliert high-confidence Patterns | ≥ 20 |

---

## Vorab-Check (Cockpit 20.8.2026 — Trajektorie, nicht bindend)

| ID | Ist-Wert | Ziel | Tendenz | Anmerkung |
|---|---|---|---|---|
| H180.1 | 0 | ≥ 3 | ❌ weit | Verified novelty, nicht `unknown_unverified`. |
| H180.2 | 2 | ≥ 2 | ⚠️ fragil | Regime-Diversität; „unclear"-Abhängigkeit ungeklärt (siehe M3). |
| H180.3 | 0 | ≥ 20 | ❌ weit | Deskriptive Library zählt nicht als PoW-Akkumulation. |

**Vorab-Stand: 1/3** (davon der eine Treffer fragil).

---

## Falsifikationsregel & Konsequenz

Wenn zur Fälligkeit **0/3 oder 1/3** → BD-4 + BD-5 blockiert, Charter-Pivot zur
Null-Befund-Studie. Bei aktueller Trajektorie (1/3, fragil) ist der Charter-Pivot der
wahrscheinliche Ausgang.

**Public-Trigger (DEC-124):** Tag 180 ist ein **interner** Methodik-Checkpoint, **kein**
Public-Trigger. Public-Aktivierung braucht kumulativ (1) Tag-180-PASS und (2) ≥ 1 Jahr
Stabilität → frühestens **30.4.2027**.

---

## Voraussetzung für eine faire Auswertung an der Fälligkeit

Aus dem Tag-90-Review (Prioritäten für die nächsten 90 Tage) — bis 5.11.2026 nötig, damit
das Gate überhaupt PASS-fähig ist:

1. **GDELT-Cluster-Causal-Motor** bauen (Cluster statt Einzelevent, deduplizierte Event-Keys,
   Crypto-Targets, SARIMAX/Counterfactual mit FDR) → adressiert H60.4/H180.1.
2. **Externe Novelty-Validierung** operationalisieren (Lehrbuchmuster maschinenlesbar sperren;
   `unknown_unverified` nur nach Evidenzprüfung hochstufen) → adressiert H60.1/H180.1.
3. **Mindestens 1 echter Pendel-spezifischer Kandidat vorab eingefroren**, bevor Tag 180 als
   Produktentscheidung behandelt wird.

---

## Historie

- **20.8.2026 (Tag 111):** Vorab-Check 1/3 (fragil), pending_precheck. Endgültige Auswertung
  folgt an der Fälligkeit ~5.11.2026 (append-only unter diesem Abschnitt).
