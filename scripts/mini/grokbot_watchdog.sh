#!/bin/bash
# grokbot_watchdog.sh: restart the Grok Bot desktop app on the Mini when it is open but has lost its server link.
# Ben OK'd 5 Oct 2026 (#99 6001876249). Free; touches nothing but the Grok Bot app.
#
# Run by launchd every 5 min (scripts/mini/com.owb.grokbot-watchdog.plist). Every run logs one line with ALL the
# candidate signals, so the log itself shows which one flips when the link drops:
#   tcp=N       ESTABLISHED TCP connections to non-loopback hosts from any Grok Bot process (Electron apps do their
#               networking in a helper process, so the whole app's process tree counts, not just the main PID)
#   status=...  scalar fields of ~/Library/Application Support/Grok Bot/desktop-status.json, plus its age in seconds
#   hb=S        age in seconds of the newest dune-reliability/sessions/*.running.json heartbeat
#
# GROKBOT_SIGNAL picks the signal that decides "disconnected":
#   tcp (default)  tcp == 0
#   status         the status line matches GROKBOT_STATUS_DOWN_REGEX
#   heartbeat      hb > GROKBOT_HB_MAX_S
# GROKBOT_MODE:
#   observe (default)  log only, including "WOULD RESTART". Start here. Switch to enforce once a real drop in the log
#                      shows the chosen signal flipping.
#   enforce            act: after GROKBOT_FAILS_NEEDED disconnected checks in a row, quit (osascript), hard-kill after
#                      30 s, relaunch (open -a), and post one line to the studio thread. If the app isn't running at
#                      all, relaunch it.
# While a TTS lock exists in ~/_desk/locks/ (name matches GROKBOT_LOCK_REGEX), it doesn't restart unless the app
# has been disconnected for more than GROKBOT_LOCK_GRACE_MIN minutes (default 15).
set -u

APP="${GROKBOT_APP:-Grok Bot}"
MODE="${GROKBOT_MODE:-observe}"
SIGNAL="${GROKBOT_SIGNAL:-tcp}"
FAILS_NEEDED="${GROKBOT_FAILS_NEEDED:-2}"
LOCK_GRACE_MIN="${GROKBOT_LOCK_GRACE_MIN:-15}"
HB_MAX_S="${GROKBOT_HB_MAX_S:-180}"
STATUS_DOWN_REGEX="${GROKBOT_STATUS_DOWN_REGEX:-disconnect|offline|connected=false|reconnecting}"
SUPPORT="${GROKBOT_SUPPORT_DIR:-$HOME/Library/Application Support/Grok Bot}"
LOCKS="${DESK_LOCK_ROOT:-$HOME/_desk/locks}"
LOCK_REGEX="${GROKBOT_LOCK_REGEX:-tts|elevenlabs|vo|pickup}"  # a false match only delays a restart by the grace period
STATE_DIR="${GROKBOT_STATE_DIR:-$HOME/_desk/state/grokbot_watchdog}"
LOG="${GROKBOT_LOG:-$HOME/_desk/logs/grokbot_watchdog.log}"
REPO="${OWB_REPO:-$HOME/YouTube/orbit-with-ben}"
# Commands are variables so the test can stub them.
PGREP="${GROKBOT_PGREP:-pgrep}"
LSOF="${GROKBOT_LSOF:-lsof}"
OSASCRIPT="${GROKBOT_OSASCRIPT:-osascript}"
OPEN="${GROKBOT_OPEN:-open}"
KILL="${GROKBOT_KILL:-kill}"
SLEEP="${GROKBOT_SLEEP:-sleep}"
NOTIFY="${GROKBOT_NOTIFY:-python3 $REPO/scripts/owb_thread.py post}"
NOW="${GROKBOT_NOW:-$(date +%s)}"

mkdir -p "$STATE_DIR" "$(dirname "$LOG")"
stamp() { date -u -r "$NOW" '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date -u -d "@$NOW" '+%Y-%m-%dT%H:%M:%SZ'; }
log() { echo "$(stamp) $*" >> "$LOG"; }
mtime() { stat -c %Y "$1" 2>/dev/null || stat -f %m "$1" 2>/dev/null || echo 0; }  # GNU first: BSD-style -f means something else there

app_pids() { $PGREP -f "$APP.app/Contents/" 2>/dev/null | tr '\n' ' '; }

tcp_count() {
  local pids="$1" n=0 p
  for p in $pids; do
    n=$(( n + $($LSOF -a -p "$p" -i TCP -s TCP:ESTABLISHED -n -P 2>/dev/null \
            | awk 'NR>1 && $9 !~ /->(127\.|\[::1\]|localhost)/' | wc -l) ))
  done
  echo "$n"
}

status_line() {
  local f="$SUPPORT/desktop-status.json"
  [ -f "$f" ] || { echo "none"; return; }
  local age=$(( NOW - $(mtime "$f") ))
  python3 - "$f" "$age" <<'PY' 2>/dev/null || echo "unreadable age=$2"
import json, sys
d = json.load(open(sys.argv[1]))
flat = []
def walk(v, k=""):
    if isinstance(v, dict):
        for kk, vv in v.items():
            walk(vv, f"{k}.{kk}" if k else kk)
    elif not isinstance(v, list):
        flat.append(f"{k}={str(v).lower()}"[:60])
walk(d)
print(" ".join(flat[:12]) + f" age={sys.argv[2]}")
PY
}

hb_age() {
  local newest=0 f m
  for f in "$SUPPORT"/dune-reliability/sessions/*.running.json; do
    [ -e "$f" ] || continue
    m=$(mtime "$f"); [ "$m" -gt "$newest" ] && newest=$m
  done
  [ "$newest" -eq 0 ] && { echo "none"; return; }
  echo $(( NOW - newest ))
}

tts_lock_held() {
  local d
  for d in "$LOCKS"/*; do
    [ -e "$d" ] || continue
    basename "$d" | grep -Eiq "$LOCK_REGEX" && return 0
  done
  return 1
}

restart_app() {
  local pids="$1" p
  $OSASCRIPT -e "quit app \"$APP\"" >/dev/null 2>&1
  $SLEEP 30
  for p in $(app_pids); do $KILL -9 "$p" 2>/dev/null; done
  $SLEEP 3
  $OPEN -a "$APP"
}

notify() { $NOTIFY "[Chief] Grok Bot watchdog: $*" >/dev/null 2>&1 || log "notify failed"; }

# ---- one check ----
FAILS_FILE="$STATE_DIR/fails"; SINCE_FILE="$STATE_DIR/down_since"
fails=$(cat "$FAILS_FILE" 2>/dev/null || echo 0)
pids="$(app_pids)"

if [ -z "${pids// /}" ]; then
  log "app=not-running mode=$MODE"
  if [ "$MODE" = "enforce" ]; then
    $OPEN -a "$APP"; log "ACTION relaunched (was not running)"; notify "relaunched $APP at $(stamp) (it was not running)."
  else
    log "WOULD RELAUNCH (observe mode)"
  fi
  echo 0 > "$FAILS_FILE"; rm -f "$SINCE_FILE"; exit 0
fi

tcp=$(tcp_count "$pids"); status=$(status_line); hb=$(hb_age)
case "$SIGNAL" in
  tcp)       [ "$tcp" -eq 0 ] && down=1 || down=0 ;;
  status)    echo "$status" | grep -Eiq "$STATUS_DOWN_REGEX" && down=1 || down=0 ;;
  heartbeat) [ "$hb" != "none" ] && [ "$hb" -gt "$HB_MAX_S" ] && down=1 || down=0 ;;
  *)         log "unknown GROKBOT_SIGNAL=$SIGNAL"; exit 2 ;;
esac

if [ "$down" -eq 1 ]; then
  fails=$(( fails + 1 )); [ -f "$SINCE_FILE" ] || echo "$NOW" > "$SINCE_FILE"
else
  fails=0; rm -f "$SINCE_FILE"
fi
echo "$fails" > "$FAILS_FILE"
since=$(cat "$SINCE_FILE" 2>/dev/null || echo "$NOW"); down_min=$(( (NOW - since) / 60 ))
log "app=running pids=[${pids% }] tcp=$tcp hb=$hb status=[$status] signal=$SIGNAL down=$down fails=$fails down_min=$down_min mode=$MODE"

[ "$fails" -ge "$FAILS_NEEDED" ] || exit 0
if tts_lock_held && [ "$down_min" -le "$LOCK_GRACE_MIN" ]; then
  log "HOLD: TTS lock in $LOCKS and down only ${down_min} min (grace ${LOCK_GRACE_MIN})"; exit 0
fi
if [ "$MODE" != "enforce" ]; then
  log "WOULD RESTART (observe mode): $fails disconnected checks, down ${down_min} min"; exit 0
fi
restart_app "$pids"
log "ACTION restarted after $fails disconnected checks (down ${down_min} min, signal=$SIGNAL)"
notify "restarted $APP at $(stamp) after ${down_min} min disconnected (signal=$SIGNAL)."
echo 0 > "$FAILS_FILE"; rm -f "$SINCE_FILE"
exit 0
