# Pendel — Nordstern & Klarer Weg

**Der Anker. Zuerst lesen — vor jeder Reaktion auf ein neues Testergebnis.**
Stand: 9.9.2026 (Tag 132) · Fortschreibung append-only.

## 0. Warum dieses Dokument
Wiederkehrendes Muster: Jedes neue Testergebnis (ein 0/3-Gate, ein scheinbar fehlendes Tool,
ein Null-Befund, ein verlockendes +30 %-Pattern) hat Kurs und Fokus gekippt und Mini-Krisen
ausgelöst. Das ist der eigentliche Fehler — **nicht** die Ergebnisse. Dieses Dokument registriert
Mission, das Erwartbare und den Weg **vorab**, damit kein einzelnes Resultat mehr aus dem Konzept
bringt. **Regel: Bei jedem neuen Befund zuerst §2 lesen, dann handeln.**

## 1. Mission (Nordstern) — unveränderlich
Quelle: `Stufe1_Implementierungsplan.md`. Pendel ist ein **dauerhafter, append-only, günstiger
Daten-Asset** an der Schnittstelle **Geopolitik × Krypto × Makro**, der **über Jahre compoundet**.

- **Das Produkt IST** der wachsende, saubere Datenbestand + die ehrliche Auswertung.
- **Das Produkt ist NICHT** ein Signal-/Trading-/Prognose-Dienst, und **NICHT** „einen Treffer
  bis Tag X erzwingen".
- **Payoff-Kurve (Original-Plan):** ~6 Monate → erste Cluster · 12–18 Monate → belastbare
  Hypothesen · 3–5+ Jahre → echte Cluster-Library. Der Wert liegt **Jahre** voraus.
- **Erfolg heißt:** die Daten fließen sauber und günstig weiter; mit steigendem n werden die
  immer gleichen Tests **stärker**; Kausalitäten/Korrelationen tauchen auf, *falls* es sie gibt —
  und wenn nicht, ist der saubere Null-Befund selbst das Ergebnis.

## 2. Was IMMER WIEDER auftauchen wird — und die stehende Deutung (KEIN Kurswechsel)

| Beobachtung | Warum das normal ist | Stehende Regel — nicht derailen |
|---|---|---|
| **Null** auf thesenkritischen Metriken | Frühphase; Cross-Domain-Effekte sind schwach; Tests werden mit n stärker | Weiterlaufen lassen. Keine Krise. Kein Cramming. |
| **Verlockende Deskriptiv-Patterns** (+30 % HYPE, große μ) | `crypto_beta`/klassisch + Confounding (Bull-Trend fällt mit häufigem Event zusammen) | **Nie** als Fund präsentieren. Nur mit Caveat; zählt erst nach Novelty + FDR + WF. |
| **Gates fallen** (0/3, 1/3, falsification_triggered) | Gates sind das Ehrlichkeits-Geländer, nicht das Produkt | Dokumentierter Null = valider Output (Charter Plan B). Kein Alarm. |
| **„Uns fehlt ein Tool"** | Toolset ist vollständig + sorgfältig gewählt; GDELT-Erweiterung war Extension, kein fehlendes Tool | Erst **BEREITS-UMGESETZT** prüfen (Karpathy-#65), bevor „Lücke" behauptet wird. |
| **Kosten-/Ops-Rauschen** (Reboot-Hinweis, stale Kalender-Konnektoren, Funding-Gaps) | Sekundär; berührt das Kernziel nicht | Kein Kurswechsel. Nur **echte Kernquellen-Stale** oder stilles Datenloch ist kritisch. |
| **Cost-Warnungen** | Weekly-Jobs / Session-Kosten sind nicht die Mission | Nicht davon treiben lassen; Infrastruktur ist ~€15,50/Mo. |

## 3. Der klare Weg (stehendes Programm)
- **A — Fundament schützen:** Liveness/Integrität grün halten (CONTROLS.md I1–I6), ~€15,50/Mo.
  Dauerpflicht, großteils automatisch. **Wichtigste Aufgabe** — der Asset compoundet nur sauber.
- **B — Compounding:** Tests wiederkehrend laufen lassen (GDELT-Motor, Granger/VAR/PCMCI,
  Walk-Forward, Negative-Findings-Retest). Ergebnisse über Zeit speichern → derselbe Test wird
  mit n stärker. „Wird über Jahre stärker" — wörtlich.
- **C — Breite (€0):** OpenSource-/Public-Substitute inkrementell anbinden (vorab analysiert in
  `PENDEL_PLUGIN_INVENTORY`): FRED-Credit-Spreads, OECD, BIS, ACLED (Geopolitik-Qualität), CFTC.
  Jede saubere Variable = eine neue Linse für künftige Kausalitäts-/Korrelations-Erkennung.
- **Gates (Tag 30/60/90/180):** laufen im Hintergrund als Ehrlichkeits-Geländer — **Checkpoints,
  keine Ziellinien.**

## 4. Stehende Regeln (Anti-Derail — gelten, egal was ein Test zeigt)
1. **Liveness zuerst** vor jeder Bewertung (Post-Mortem-Lehre).
2. **Kriterien eingefroren** — kein Goalpost-Shift nach Fälligkeit.
3. **Kein p-Hacking / Fishing.** Test erschöpft = Ergebnis akzeptieren. Urteil per
   real-vs-placebo/Permutation, nie per rohem Signifikanz-Count.
4. **Null ist valide.** Kein herbeigeschriebenes „signifikant" — das wäre der einzige echte GAU.
5. **Kritik → Erkenntnis, nicht reflexartig neue Doku** (DEC-135). Erst prüfen, was schon existiert.
6. **Kostengünstig:** OpenSource/Public zuerst; Lizenz nur mit klarem 3-Jahres-TCO-Nutzen.

## 5. Stand heute (9.9.2026, Tag 132) — Single Entry Point
- **Datenbasis wächst sauber:** Kernquellen frisch (9.9.), 0 failed units, Disk 61,5 %,
  ~€15,50/Mo. Pattern-Library **1.126.187 total / 221.600 robust / 103.747 high-n100**.
- **Gates:** T30 **2/4** · T60 **0/4** · T90 **0/3** · T180 pending (Vorab 1/3). **H₀ nicht abgelehnt.**
- **GDELT×Krypto: getestet → belastbarer Null** (v1 daily: real 3 ≤ placebo 11; v2 stündlich +
  Vola + Permutation: p=0.935 / 0.652). Geopolitik-Ast war vorher uncomputed, jetzt sauber null.
- **PoW-Crash behoben** (läuft 7,5 min < 30-min-Timeout). Output aktuell = `crypto_beta`-Artefakte
  → zählt **nicht** fürs Gate (braucht FDR + WF + Novelty). Timer noch nicht reaktiviert.
- **Erwartete Tag-180-Trajektorie:** dokumentierter Null → Charter-Pivot zur **Null-Befund-Studie**
  (valider, publizierbarer Output — kein Scheitern).
- **Repo** = Falsifikations-Journal (`gates/`) + Integrität (`CONTROLS.md`) + Endspurt-Plan
  (`PLAN_TAG180_ENDSPURT.md`) + Motoren (`motor/`) + PoW-Fix (`pow/`).

## 6. Offene Items — klar eingeordnet (kein Feuer, keine Eile)
Alle vier dienen dem Asset **mittelbar**, keines ist dringend, keines erzwingt ein Ergebnis:
- **Novelty-Lock** — 471 unknowns adjudizieren + `crypto_beta`/klassisch aus PoW filtern (Gate-Politur + Breite).
- **PoW-Timer reaktivieren** — erst *nach* Novelty-Filter (sonst Wochenbericht mit Artefakt-Aufmacher).
- **Kandidat einfrieren** — Reproduktion sauber prüfbar machen.
- **€0-Konnektor-Breite (Weg C)** — inkrementell, FRED-Credit-Spreads zuerst.

---
*Anker. Bei jedem neuen Testergebnis zuerst §2. Dieses Dokument steht über der Tagesaufregung.*
