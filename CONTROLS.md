# Pendel — Kontrolltage & Integritäts-Garantien

**Zweck:** Sicherstellen, dass ein Gate-Ergebnis (Tag 30/60/90/180) **immer** auf echten,
live geprüften Daten beruht — und dass sich **nie erst am Gate** herausstellt, dass wochenlang
etwas Falsches mitlief. Dies ist die Antwort auf den Post-Mortem-Vorfall (10-Tage-Datenloch,
unentdeckt bis Tag 30).

**Stand:** 20.8.2026 (Tag 111). **Quellen:** Post-Mortem 1.6.2026, Check-Katalog 1.7.2026,
Codex-Review 1.7.2026, Cockpit-Snapshot 20.8.2026.

> **M3-Self-Critique:** Diese Datei kodifiziert die *Garantie-Grenze* (§0) und die Invarianten,
> die **jeden Tag** halten müssen (§1). Die konkreten Tages-Zahlen (§3) stammen aus benannten
> Reviews; der heutige exakte Kontrolltag-Ist-Wert ist die Live-Metrik
> `clean_days_since_rebaseline` (Cockpit) — in dieser Session **nicht** aus der DB gezogen. Die
> Kalendertag-Obergrenzen in §3 sind arithmetisch aus den Re-Baseline-Daten belegt, nicht geraten.

---

## 0. Die Garantie-Grenze (ehrlich, verbindlich)

| | Garantierbar? | Inhalt |
|---|---|---|
| **Integrität + Früherkennung** | ✅ **JA — Pflicht** | Jeder Kontrolltag zählt nur bei live + integritätsgeprüften Daten. Kaputte Tage werden ausgeschlossen, nicht überbrückt. Stand täglich sichtbar. Kein Gate-Tag hält eine Überraschung bereit. |
| **Statistische Power (n) wächst** | ✅ JA | Mit jedem sauberen Tag steigt die Fähigkeit, ein vorhandenes Signal zu sehen (MDE sinkt). |
| **Score verbessert sich** | ❌ **NEIN** | Daten decken Signal nur auf, falls es existiert. Monotone Score-Verbesserung zu versprechen wäre Overclaiming (DEC-009-Verstoß). Null bleibt ein valides Ergebnis. |

**Kernsatz:** Garantiert wird die **Vertrauenswürdigkeit der Messung**, nicht das **Vorzeichen
des Resultats**.

---

## 1. Integritäts-Invarianten (müssen JEDEN Tag halten)

Wenn eine dieser Invarianten bricht, ist der Tag **kein** Kontrolltag und die Messung an dem
Tag ist ungültig — laut, nicht still.

| # | Invariante | Verhindert | Mechanismus / Bezug | Enforcement |
|---|---|---|---|---|
| I1 | **Kein ffill über Datenlöcher** — `dropna` statt `ffill` | Erfundenes `n` (der Tag-30-VOID-Fehler) | DEC-140 | kontinuierlich (Code) |
| I2 | **Freshness-Watchdog + Auto-Recovery** — STALE einer 24/7-Kernquelle → Restart | Stilles Datenloch (Post-Mortem) | DEC-138, `data_watchdog.py` 10-min-Timer | kontinuierlich (Timer) |
| I3 | **Kein Fake-p** — echter z-Test-p + BH-FDR, `n_post` ≥ 10 | Erfundene Signifikanz (Fake-0,04-Zeilen) | DEC-153-A | kontinuierlich (Code) |
| I4 | **Zirkularitäts-Sperre** — `crypto_derived_circular` | Fear&Greed-Scheinnovelty | DEC-153 | kontinuierlich (Code) |
| I5 | **Liveness zuerst** — `data_live` grün VOR jeder Bewertung | Eval auf toten Daten (Tag-30-Fehler) | Post-Mortem-Prozessregel | pro Review (Pflicht) |
| I6 | **Kriterien eingefroren** — Schwellen aus `FALSIFIKATIONSKRITERIEN.md` | Nachträgliches Schönrechnen | DEC-141, dieses Repo | pro Gate |

---

## 2. Kontrolltag-Zählregel

Ein Kalendertag zählt für einen Block (crypto / macro / gdelt) **nur dann** als Kontrolltag,
wenn an dem Tag **alle** gelten:

1. `data_live = true` für die Kern-Quellen des Blocks (I2/I5),
2. keine ffill-Überbrückung nötig war (I1),
3. der Tag nach der jeweiligen **Re-Baseline** liegt (crypto ab 1.6.2026, macro ab 25.6.2026 —
   getrennte Uhren, damit ein Block das andere nicht kontaminiert).

Kaputte Tage werden **ausgeschlossen**, nicht interpoliert. Dadurch ist `n` immer die Zahl
*echter* Beobachtungen — der Wert, an dem Power hängt.

---

## 3. Bekannter Kontrolltag-Stand (mit Quelle)

| Block | Re-Baseline | Kontrolltage @ 1.7.2026 (Codex-Review) | Stand 20.8.2026 |
|---|---|---|---|
| Crypto | 1.6.2026 | 31 (`clean_days_since_rebaseline.kraken`) | ≤ 80 Kalendertage seit Re-Baseline; sauberer Ist-Wert = Live-Metrik `clean_days_since_rebaseline` (Cockpit) |
| Macro | 25.6.2026 | 6 (`clean_days_since_rebaseline.yahoo`) | ≤ 56 Kalendertage; sauberer Ist-Wert = Live-Metrik (Cockpit) |
| Crypto real (90d-Fenster) | — | 56 (`crypto_real_days_90d`) | Live-Metrik `crypto_real_days_90d` (Cockpit) |

Beobachtung: Der Macro-Block hatte an Tag 60 erst **6** saubere Tage — das ist genau die
„zu wenig Kontrolltage"-Schwäche, die H60.3 (Regimes ≥ 3) unfair früh getestet hat. Deshalb
zählt für Substanz-Aussagen `n ≥ 100` je relevantem Paar — erreichbar ~ab Ende Oktober 2026.

---

## 4. Täglicher Gate-Precheck (damit kein Gate-Tag überrascht)

Der Zustand jedes Gates wird **täglich** neu gemessen und als Trajektorie geschrieben — nicht
erst am Fälligkeitstag. So ist der Gate-Tag nur „lies die Zahl, die seit Tagen stabil ist",
kein Reveal.

- Cockpit-Sektion *Falsifikationskriterien* zeigt H30/60/90/180 live (Ist vs. Ziel).
- Die Gate-Dateien in `gates/` werden bei jedem Review-Punkt append-only fortgeschrieben.
- **Frühwarnung:** Fällt ein zuvor erfülltes Kriterium (wie H60.4: 2 → 0), ist das sofort
  sichtbar und wird als Degradation dokumentiert — nicht am nächsten Gate „entdeckt".

---

## 5. Abdeckung — kein offener Punkt

Die Garantie aus §0 ist **kontinuierlich umgesetzt**; das System wurde von Grund auf so gebaut.
Es fehlt kein Baustein:

- **Maschinenlesbarer Kontrolltag-Zähler:** `clean_days_since_rebaseline` (je Block, live).
- **Täglicher Gate-Precheck:** Cockpit-Sektion *Falsifikationskriterien* zeigt H30/60/90/180
  live (Ist vs. Ziel) — jeden Tag, nicht erst am Gate.
- **Alarm bei Invarianten-Bruch (I1–I6):** Freshness-Watchdog + Auto-Recovery (DEC-138,
  10-min-Timer), stündlicher Healthcheck, `data_watchdog.py`.
- **Degradations-Erkennung:** Negative-Findings-Auto-Detection macht Rückfälle (z.B. H60.4
  2 → 0) sofort sichtbar — nicht erst am nächsten Gate.

Damit gilt §0 lückenlos: kein Gate-Tag hält eine Überraschung bereit. Die verbleibende Aufgabe
dieses Repos ist **ausschließlich**, die Gate-Auswertungen an ihren Fälligkeitstagen
append-only fortzuschreiben — mehr nicht.
