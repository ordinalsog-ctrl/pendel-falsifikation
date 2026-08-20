#!/usr/bin/env bash
# Pendel — Readiness-Check für den nächsten Kontrollpunkt (Tag 180, ~5.11.2026)
#
# Zweck: Prüft die 7 Voraussetzungen für eine ERSTE SERIÖSE Auswertung an Tag 180
#        (siehe gates/tag-180-charter-gate.md §Readiness). Read-only.
#
# WICHTIG:
#   - NUR LESEND. Fasst den Server nicht an: curl GET, ls, df, systemctl is-enabled/list.
#     Keine Writes, keine Restarts, keine DB-Änderung.
#   - Muss in einer Session MIT SSH-Zugang zum Pendel-Host laufen.
#   - Feldnamen stammen aus den Live-Zitaten in PENDEL_H90_REVIEW_2026-08-02.md und dem
#     Codex-Live-Check (1.7.2026). Bei Schema-Drift: Namen an api.py / current_manifest.yaml
#     anpassen. Der JSON-Parser sucht Felder REKURSIV, damit Verschachtelung ihn nicht bricht.
#
# Nutzung:
#   PENDEL_SSH=pendel ./tools/readiness_check.sh
#   (Default-SSH-Alias: "pendel". Endpoint: http://127.0.0.1:8080/evidence/falsification)

set -uo pipefail

HOST="${PENDEL_SSH:-pendel}"
API="${PENDEL_API:-http://127.0.0.1:8080}"
TMP="$(mktemp -t pendel_falsif.XXXXXX.json)"
trap 'rm -f "$TMP"' EXIT

line() { printf '%s\n' "----------------------------------------------------------------------"; }
echo "Pendel Readiness-Check — Ziel-Kontrollpunkt: Tag 180 (~5.11.2026)"
echo "Host: $HOST   API: $API   Stand: $(date -u +%Y-%m-%dT%H:%MZ)"
line

# --- 0. SSH-Konnektivität + Liveness zuerst (Post-Mortem-Regel) -------------------------
if ! ssh -o ConnectTimeout=8 -o BatchMode=yes "$HOST" true 2>/dev/null; then
  echo "ABBRUCH: SSH zu '$HOST' nicht möglich. Ohne Live-Zugang kein Readiness-Status."
  echo "Setze PENDEL_SSH=<alias> oder starte die Session mit SSH-Zugang."
  exit 1
fi

ssh "$HOST" "curl -s --max-time 15 $API/evidence/falsification" > "$TMP" 2>/dev/null
if [ ! -s "$TMP" ]; then
  echo "WARN: /evidence/falsification lieferte keine Daten (API down? Endpoint umbenannt?)."
  echo "      Gate-Metriken (Items 1,2,3,6) sind ohne diese Antwort nicht auswertbar."
fi

# --- Helfer: rekursive Feldsuche im JSON -------------------------------------------------
getf() { # getf <feldname[.subkey]>  -> Wert oder leer
  python3 - "$1" < "$TMP" 2>/dev/null <<'PY'
import json,sys
key=sys.argv[1]
try: data=json.load(sys.stdin)
except Exception: sys.exit(0)
def find(o,k):
    if isinstance(o,dict):
        if k in o: return o[k]
        for v in o.values():
            r=find(v,k)
            if r is not None: return r
    elif isinstance(o,list):
        for v in o:
            r=find(v,k)
            if r is not None: return r
    return None
if '.' in key:
    p,sub=key.split('.',1); parent=find(data,p)
    val=parent.get(sub) if isinstance(parent,dict) else None
else:
    val=find(data,key)
if val is not None: print(val)
PY
}
na() { [ -z "$1" ] && echo "n/a (Feld im Schema prüfen)" || echo "$1"; }

# --- Item 1: Datenreife / Power (n>=100, data_live) --------------------------------------
line; echo "[1] DATENREIFE / POWER  (Ziel: clean days >= 100 je Block, data_live=true)"
dl=$(getf data_live); ck=$(getf clean_days_since_rebaseline.kraken)
cy=$(getf clean_days_since_rebaseline.yahoo); cr=$(getf crypto_real_days_90d)
echo "    data_live: $(na "$dl")"
echo "    clean_days crypto (kraken): $(na "$ck")   [Schwelle >=100]"
echo "    clean_days macro (yahoo):   $(na "$cy")   [Schwelle >=100]"
echo "    crypto_real_days_90d:       $(na "$cr")"

# --- Item 2: GDELT-Cluster-Causal-Motor (Outcome-Proxy) ----------------------------------
line; echo "[2] GDELT-CLUSTER-CAUSAL-MOTOR  (H90-Prio 1; Outcome-Proxy)"
gci=$(getf gdelt_crypto_impact)
echo "    gdelt_crypto_impact: $(na "$gci")   [>=1 = Motor liefert echte GDELT->Crypto-Signifikanz]"
echo "    Hinweis: 0 kann 'Motor nicht gebaut' ODER 'gebaut, aber null' heißen -> im Zweifel"
echo "             Tabelle/Job auf dem Server verifizieren (ls /opt/pendel/daemon | grep -i gdelt)."

# --- Item 3: Novelty-Validierung (verified vs unknown) -----------------------------------
line; echo "[3] EXTERNE NOVELTY-VALIDIERUNG  (H90-Prio 2)"
sn=$(getf strict_novel_leadlag); uc=$(getf unknown_candidates)
echo "    strict_novel_leadlag: $(na "$sn")   [H180.1 braucht >=3 verified]"
echo "    unknown_candidates:   $(na "$uc")   [hängen, bis Lehrbuch-Lock sie klassifiziert]"

# --- Item 4: Pattern-of-the-Week reaktiviert ---------------------------------------------
line; echo "[4] PATTERN-OF-THE-WEEK  (H180.3 braucht >=20 high-confidence; PoW war disabled)"
echo "    systemd-Timer (Suche pattern/pow):"
ssh "$HOST" "systemctl list-timers --all 2>/dev/null | grep -iE 'pattern|pow' || echo '      (kein PoW-Timer gefunden)'"
for u in pendel-pattern-of-the-week pendel-patternweek pendel-pow; do
  st=$(ssh "$HOST" "systemctl is-enabled $u 2>/dev/null")
  [ -n "$st" ] && echo "    $u: $st"
done
powc=$(getf pattern_of_week_high_confidence)
echo "    PoW high-confidence count: $(na "$powc")   [Feldname ggf. anpassen]"

# --- Item 5: Kandidat vorab eingefroren --------------------------------------------------
line; echo "[5] EINGEFRORENER KANDIDAT  (H180.1/Reproduktion; braucht n>=100 in-sample + OOS-Runway)"
echo "    Freeze-Dateien in /opt/pendel/state:"
ssh "$HOST" "ls -la /opt/pendel/state/ 2>/dev/null | grep -iE 'froze|tag180|tag-180' || echo '      (keine Tag-180-Freeze-Datei gefunden)'"

# --- Item 6: Regime-Zähl-Semantik --------------------------------------------------------
line; echo "[6] REGIME-SEMANTIK  (H180.2 >=2; fragil solange non_unclear < total)"
mt=$(getf macro_regimes_total); mnu=$(getf macro_regimes_non_unclear)
echo "    macro_regimes_total:       $(na "$mt")"
echo "    macro_regimes_non_unclear: $(na "$mnu")   [seriöser Pass erst wenn >=2 non-unclear]"

# --- Item 7: Disk / Integrität -----------------------------------------------------------
line; echo "[7] DISK / INTEGRITÄT  (DiskFull-Vorfall am 2.8.; kein Datenloch darf Runway fressen)"
ssh "$HOST" "df -h / | tail -1 | awk '{print \"    root-disk: \"\$5\" belegt, \"\$4\" frei (von \"\$2\")\"}'"
echo "    fehlgeschlagene Units:"
ssh "$HOST" "systemctl --failed --no-legend 2>/dev/null | sed 's/^/      /' | grep . || echo '      (0 failed)'"

# --- Aktuelle H180-Gate-Werte (direkt aus dem Endpoint, falls vorhanden) -----------------
line; echo "[H180] Aktuelle Gate-Werte (Vorab-Check)"
for k in H180.1 H180.2 H180.3; do v=$(getf "$k"); echo "    $k: $(na "$v")"; done

line
cat <<'EOF'
MARKDOWN-BLOCK zum append-only Eintragen in gates/tag-180-charter-gate.md
(Verdikte aus den obigen Zeilen ableiten: PASS wenn Schwelle erreicht, sonst OFFEN):

## Readiness-Check <DATUM> (Tag <NNN>)
| # | Voraussetzung | Ist | Verdikt |
|---|---|---|---|
| 1 | Clean days >= 100 (crypto/macro), data_live | crypto=…, macro=…, live=… | … |
| 2 | GDELT-Cluster-Motor liefert Signifikanz | gdelt_crypto_impact=… | … |
| 3 | Verified novelty vorhanden | strict_novel_leadlag=… (unknown=…) | … |
| 4 | Pattern-of-the-Week reaktiviert | PoW=…, Timer=… | … |
| 5 | Kandidat eingefroren (OOS-Runway) | Freeze=… | … |
| 6 | Regime non-unclear >= 2 | non_unclear=… / total=… | … |
| 7 | Disk-Headroom + 0 failed units | frei=…, failed=… | … |
Gesamt-Readiness: <n>/7 — <bereit / nicht bereit für seriöse Tag-180-Auswertung>
EOF
