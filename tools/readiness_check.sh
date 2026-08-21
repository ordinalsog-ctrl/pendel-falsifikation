#!/usr/bin/env bash
# Pendel — Readiness-Check für den nächsten Kontrollpunkt (Tag 180, ~5.11.2026)
#
# Zweck: Prüft die 7 Voraussetzungen für eine ERSTE SERIÖSE Auswertung an Tag 180
#        (siehe gates/tag-180-charter-gate.md §Readiness). READ-ONLY.
#
# Läuft in BEIDEN Umgebungen — automatisch erkannt an /opt/pendel:
#   - DIREKT AUF DEM SERVER (root@pendel-prod): alle Checks lokal, kein SSH.
#   - VOM MAC AUS: alle Checks via `ssh $PENDEL_SSH` (Default-Alias: pendel).
#   Override: PENDEL_MODE=local|remote
#
# WICHTIG: NUR LESEND — curl GET, ls, df, systemctl is-enabled/list. Keine Writes,
#          keine Restarts, keine DB-Änderung.
#
# Feldnamen stammen aus den Live-Zitaten in PENDEL_H90_REVIEW_2026-08-02.md und dem
# Codex-Live-Check (1.7.2026). Der JSON-Parser sucht Felder REKURSIV (Schema-Drift-sicher).
# Ist ein Wert "n/a", steht das Feld unter anderem Namen im Schema -> Rohschlüssel am Ende.
#
# Server-Nutzung:
#   curl -fsSL https://raw.githubusercontent.com/ordinalsog-ctrl/pendel-falsifikation/main/tools/readiness_check.sh -o /root/readiness_check.sh
#   bash /root/readiness_check.sh
# Mac-Nutzung:
#   PENDEL_SSH=pendel ./tools/readiness_check.sh

set -uo pipefail

HOST="${PENDEL_SSH:-pendel}"
API="${PENDEL_API:-http://127.0.0.1:8080}"
TMP="$(mktemp -t pendel_falsif.XXXXXX.json 2>/dev/null || mktemp)"
trap 'rm -f "$TMP"' EXIT

# --- Mode-Detection: bin ich auf dem Server oder auf dem Mac? ----------------------------
if [ -n "${PENDEL_MODE:-}" ]; then MODE="$PENDEL_MODE"
elif [ -d /opt/pendel ] || [ "$(hostname 2>/dev/null)" = "pendel-prod" ]; then MODE="local"
else MODE="remote"; fi

run() { if [ "$MODE" = "remote" ]; then ssh "$HOST" "$1"; else bash -c "$1"; fi; }

line() { printf '%s\n' "----------------------------------------------------------------------"; }
echo "Pendel Readiness-Check — Ziel-Kontrollpunkt: Tag 180 (~5.11.2026)"
echo "Mode: $MODE   API: $API   Stand: $(date -u +%Y-%m-%dT%H:%MZ)"
line

# --- 0. Liveness zuerst (Post-Mortem-Regel) ---------------------------------------------
if [ "$MODE" = "remote" ]; then
  if ! ssh -o ConnectTimeout=8 -o BatchMode=yes "$HOST" true 2>/dev/null; then
    echo "ABBRUCH: SSH zu '$HOST' nicht möglich. Setze PENDEL_SSH=<alias> oder laufe auf dem Server."
    exit 1
  fi
fi
run "curl -s --max-time 15 $API/evidence/falsification" > "$TMP" 2>/dev/null
if [ ! -s "$TMP" ]; then
  echo "WARN: /evidence/falsification lieferte keine Daten (API down? Endpoint umbenannt?)."
  echo "      Gate-Metriken (Items 1,2,3,6) sind ohne diese Antwort nicht auswertbar."
fi

# --- Helfer: rekursive Feldsuche im JSON -------------------------------------------------
getf() {
  [ -s "$TMP" ] || return 0
  python3 - "$TMP" "$1" 2>/dev/null <<'PY'
import json,sys
try: data=json.load(open(sys.argv[1]))
except Exception: sys.exit(0)
key=sys.argv[2]
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

# --- Item 1: Datenreife / Power ----------------------------------------------------------
line; echo "[1] DATENREIFE / POWER  (Ziel: n>=100 fuer 180d/1y-Fenster)"
echo "    crypto_daily_days:      $(na "$(getf crypto_daily_days)")   [>=100]"
echo "    descriptive_high_n100:  $(na "$(getf descriptive_high_n100)")"
echo "    descriptive_robust_n30: $(na "$(getf descriptive_robust_n30)")"
echo "    clean_days crypto (falls Feld vorhanden): $(na "$(getf clean_days_since_rebaseline.kraken)")"
echo "    (data_live/clean_days liefert die tag60-readiness-Harness, nicht dieser Endpoint)"

# --- Item 2: GDELT-Cluster-Causal-Motor --------------------------------------------------
line; echo "[2] GDELT-CLUSTER-CAUSAL-MOTOR  (H90-Prio 1; Outcome-Proxy)"
echo "    gdelt_crypto_impact: $(na "$(getf gdelt_crypto_impact)")   [>=1 = echte GDELT->Crypto-Signifikanz]"
echo "    Job auf dem Server:"
run "ls /opt/pendel/daemon 2>/dev/null | grep -iE 'gdelt.*(cluster|impact|motor)|cluster' | sed 's/^/      /' || echo '      (kein GDELT-Cluster-Job-File gefunden)'"

# --- Item 3: Novelty-Validierung ---------------------------------------------------------
line; echo "[3] EXTERNE NOVELTY-VALIDIERUNG  (H90-Prio 2)"
echo "    strict_novel_leadlag: $(na "$(getf strict_novel_leadlag)")   [H180.1 braucht >=3 verified]"
echo "    unknown_candidates:   $(na "$(getf unknown_candidates)")   [hängen bis Lehrbuch-Lock]"

# --- Item 4: Pattern-of-the-Week ---------------------------------------------------------
line; echo "[4] PATTERN-OF-THE-WEEK  (H180.3 braucht >=20 high-confidence; war disabled)"
run "systemctl list-timers --all 2>/dev/null | grep -iE 'pattern|pow' | sed 's/^/      /' || echo '      (kein PoW-Timer gefunden)'"
echo "    PoW high-confidence count: $(na "$(getf pattern_of_week_high_confidence)")   [Feldname ggf. anpassen]"

# --- Item 5: Eingefrorener Kandidat ------------------------------------------------------
line; echo "[5] EINGEFRORENER KANDIDAT  (H180.1/Reproduktion; n>=100 in-sample + OOS-Runway)"
run "ls -la /opt/pendel/state/ 2>/dev/null | grep -iE 'froze|tag180|tag-180' | sed 's/^/      /' || echo '      (keine Tag-180-Freeze-Datei)'"

# --- Item 6: Regime-Semantik -------------------------------------------------------------
line; echo "[6] REGIME-SEMANTIK  (H180.2 >=2; fragil solange non_unclear < total)"
echo "    macro_regimes_total:       $(na "$(getf macro_regimes_total)")"
echo "    macro_regimes_non_unclear: $(na "$(getf macro_regimes_non_unclear)")   [seriös erst >=2 non-unclear]"

# --- Item 7: Disk / Integrität -----------------------------------------------------------
line; echo "[7] DISK / INTEGRITÄT  (DiskFull-Vorfall 2.8.; kein Datenloch darf Runway fressen)"
run "df -h / | tail -1 | awk '{print \"    root-disk: \"\$5\" belegt, \"\$4\" frei (von \"\$2\")\"}'"
echo "    fehlgeschlagene Units:"
run "systemctl --failed --no-legend 2>/dev/null | sed 's/^/      /' | grep . || echo '      (0 failed)'"

# --- Aktuelle H180-Gate-Werte ------------------------------------------------------------
line; echo "[H180] Vorab-Werte (aus Metriken abgeleitet)"
echo "    H180.1 (>=3 verified novelty): strict_novel_leadlag=$(na "$(getf strict_novel_leadlag)"), cross_method_triple=$(na "$(getf cross_method_triple)")"
echo "    H180.2 (>=2 Regimes): macro_regimes_non_unclear=$(na "$(getf macro_regimes_non_unclear)")"
echo "    H180.3 (>=20 PoW): PoW-Timer siehe [4]"

# --- Roh-Schlüssel (falls oben Felder n/a sind: echte Namen sichtbar machen) -------------
line; echo "[schema] Alle Feld-Schlüssel im Endpoint (zur Namensprüfung bei n/a):"
python3 - "$TMP" 2>/dev/null <<'PY'
import json,sys
try: d=json.load(open(sys.argv[1]))
except Exception:
    print("    (JSON nicht parsebar)"); sys.exit(0)
ks=set()
def walk(o):
    if isinstance(o,dict):
        for k,v in o.items(): ks.add(k); walk(v)
    elif isinstance(o,list):
        for v in o: walk(v)
walk(d)
print("    "+", ".join(sorted(ks)))
PY

line
cat <<'EOF'
MARKDOWN-BLOCK für gates/tag-180-charter-gate.md (append-only; Verdikte oben ableiten):

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
