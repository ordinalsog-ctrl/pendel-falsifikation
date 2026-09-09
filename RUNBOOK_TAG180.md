# Runbook — Tag-180-Prüfung (~5.11.2026)

**Zweck:** Turnkey-Ausführung der vorab-registrierten Tag-180-Charter-Gate-Prüfung
(`FALSIFIKATIONSKRITERIEN.md` §4). Ausführen **am/nach ~5.11.2026 (Tag 180)** — nicht früher
(Checkpoint, keine Ziellinie). Ergebnis wird append-only ins Gate geschrieben.

> Vor jeder Reaktion auf die Zahlen: `NORDSTERN.md` §2 lesen. Ein Null-Befund ist ein valides,
> erwartetes Ergebnis, kein Anlass für Kurswechsel.

## Schritt 0 — Liveness zuerst (Pflicht, Post-Mortem-Regel)
Auf `pendel-prod`:
```bash
sudo -u postgres psql -P pager=off -d pendel -c "SELECT exchange,status,round(EXTRACT(EPOCH FROM(now()-last_message_at))/3600,1) AS h_stale FROM connector_health ORDER BY h_stale DESC;"
sudo -u postgres psql -P pager=off -d pendel -c "SELECT exchange,started_at,ended_at,reason FROM connector_gaps WHERE started_at>now()-interval '35 days' ORDER BY started_at DESC LIMIT 30;"
systemctl --failed --no-legend | grep . || echo "0 failed"
```
**Regel:** Nur weiter, wenn Kernquellen (kraken/hyperliquid/yahoo) frisch (≤ ~0.1 h) und
`connector_gaps` **kein Kernquellen-Loch** im Bewertungszeitraum zeigt. Sonst: Datenintegrität
zuerst klären (kritisch), Gate-Bewertung stoppen.

## Schritt 1 — Frische Gate-Metriken ziehen
```bash
curl -s http://127.0.0.1:8080/evidence/falsification | python3 -m json.tool
```
Relevante Felder: `current_day`, `strict_novel_leadlag`, `cross_method_triple`,
`macro_regimes_non_unclear`, `gdelt_crypto_impact`, `crypto_pcmci_significant`.

## Schritt 2 — GDELT-Ast re-testen (compounding — wird mit n stärker)
```bash
sudo -u pendel /opt/pendel/venv/bin/python /opt/pendel/daemon/compute_gdelt_cluster_impact_hf.py
sudo -u pendel /opt/pendel/venv/bin/python /opt/pendel/daemon/compute_gdelt_cluster_impact.py    # v1 daily (Kontext)
```
**Regel:** Signal nur, wenn empirischer p **< 0.025** (Bonferroni, 2 Kanäle) UND real ≫ placebo.
Sonst weiterhin Null. (Stand 9.9.: p=0.935 / 0.652 → Null.)

## Schritt 3 — H180.1/.2/.3 gegen die EINGEFRORENEN Kriterien werten
| ID | Kriterium (eingefroren) | Quelle/Regel |
|---|---|---|
| H180.1 | ≥ 3 Pendel-spezifische Patterns, Cross-Method-validiert | `strict_novel_leadlag` ≥ 3 **mit** `cross_method_triple` ≥ 1; **verified**, nicht `unknown`. GDELT-Ast (Schritt 2) muss dafür ≥ 1 verteidigbaren Treffer liefern. |
| H180.2 | Robuste Performance über ≥ 2 Macro-Regimes | `macro_regimes_non_unclear` ≥ 2 |
| H180.3 | Pattern-of-the-Week ≥ 20 high-confidence akkumuliert | **FDR + WF-stabil**, nicht deskriptive PoW-„qualifiziert". Braucht Novelty-Lock-Bridge (offen). |

**Score = erfüllte / 3.**

## Schritt 4 — Verdikt + Charter-Konsequenz
- **0/3 oder 1/3** → Falsifikation: BD-4 + BD-5 blockiert, **Charter-Pivot zur Null-Befund-Studie**
  (der erwartete, valide, publizierbare Ausgang — kein Scheitern).
- **≥ 2/3 mit verified-novel** → CEO-Review; Cross-Method-Bestätigung Pflicht **vor** jedem
  Discovery-Anspruch. Kein „causal"-Wording außerhalb L4.
- **Kein Goalpost-Shift.** Fallback (vorab registriert, Codex 1.7.): falls die n-Voraussetzung
  für einen Test am 5.11. knapp ist, den *bindenden Entscheid* daten-konditioniert leicht nach
  Tag 180 legen — **ohne** Kriterien zu senken.

## Schritt 5 — Append-only dokumentieren
Ergebnis als datierten Abschnitt in `gates/tag-180-charter-gate.md` (Vorlage: der Readiness-Block).
`STATUS.md` + `NORDSTERN.md` §5 aktualisieren. Commit + push.

---

## Referenz — was auf dem Server liegt (Stand 9.9.2026)
- `/opt/pendel/daemon/compute_gdelt_cluster_impact.py` (v1, Dry-Run-Default) + `_hf.py` (v2, read-only)
  — GDELT-Ast getestet **null**, **nicht** als Timer geplant (manuell/Runbook re-run).
- `/opt/pendel/daemon/pattern_of_the_week_fast.py` — Crash-Fix **verifiziert** (7,5 min < Timeout),
  Timer **geparkt** bis Novelty-Lock-Filter steht.
- `readiness_check.sh` (Mac via `ssh`, oder Server lokal).

## Optional vor dem langen Soak bis 5.11.
Bewussten **Reboot** in ruhigem Fenster legen (44 Updates, „restart required") — verhindert einen
ungeplanten Neustart, der ein Datenloch reißt. Danach `systemctl --failed` = 0 prüfen.
