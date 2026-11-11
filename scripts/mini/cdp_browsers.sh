#!/usr/bin/env bash
# The Mini's three signed-in Chrome browsers that agents drive over CDP.
# Each one keeps its own profile, so its Google sign-in survives a restart.
#
#   9222  Google Flow browser
#   9223  Orbit With Ben Studio            ~/.orbit-chrome-youtube-studio
#   9460  History of Science Studio        ~/.hos-chrome-youtube-studio
#
# The 9222 profile folder is named after the account it is signed into, so its name is not kept in git.
# Put it in ~/_desk/bin/cdp_browsers.env (never committed), one line:
#   CDP_PROFILE_9222="$HOME/<the Flow browser's profile folder>"
#
# Usage:
#   cdp_browsers.sh status          which ports answer, and the page each one is on
#   cdp_browsers.sh start           start any browser that isn't answering (safe to repeat)
#   cdp_browsers.sh restart PORT    quit one frozen browser and start it again
#
# `start` never touches a browser that is up, so it can't interrupt an upload.
# com.hos.cdp-browsers.plist runs `start` every 5 minutes so a crash or a reboot
# heals itself. If a page lands on accounts.google.com, the profile was signed
# out and Ben has to sign in once in that window.
set -uo pipefail

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LOG_DIR="${HOME}/Library/Logs"
PORTS=(9222 9223 9460)

# Local settings that stay off git (the 9222 profile folder).
# shellcheck disable=SC1091
[[ -f "${HOME}/_desk/bin/cdp_browsers.env" ]] && . "${HOME}/_desk/bin/cdp_browsers.env"

profile_for() {
  case "$1" in
    9222) echo "${CDP_PROFILE_9222:-${HOME}/.hos-chrome-flow-cdp}" ;;
    9223) echo "${HOME}/.orbit-chrome-youtube-studio" ;;
    9460) echo "${HOME}/.hos-chrome-youtube-studio" ;;
    *) return 1 ;;
  esac
}

start_url_for() {
  case "$1" in
    9222) echo "https://labs.google/fx/tools/flow" ;;
    *) echo "https://studio.youtube.com/" ;;
  esac
}

is_up() {
  curl -sf --max-time 5 "http://127.0.0.1:$1/json/version" >/dev/null 2>&1
}

pages() {
  curl -sf --max-time 5 "http://127.0.0.1:$1/json/list" 2>/dev/null | python3 -c '
import json, sys
try:
    tabs = json.load(sys.stdin)
except Exception:
    sys.exit(0)
for t in tabs:
    if t.get("type") == "page":
        u = t.get("url", "")
        flag = "  <- SIGNED OUT, Ben to sign in" if "accounts.google.com" in u else ""
        print("      " + u[:120] + flag)
'
}

start_one() {
  local port="$1" profile
  profile="$(profile_for "$port")" || { echo "unknown port $port"; return 1; }
  if is_up "$port"; then
    echo "$port up"
    return 0
  fi
  if [[ ! -d "$profile/Default" ]]; then
    echo "$port DOWN: profile $profile is missing, so it was never set up here. Ben to sign in a fresh one."
    return 1
  fi
  # A crash leaves Chrome's lock files behind, and they block the next start.
  rm -f "$profile/SingletonLock" "$profile/SingletonSocket" "$profile/SingletonCookie"
  nohup "$CHROME" \
    --remote-debugging-port="$port" \
    --remote-allow-origins='*' \
    --user-data-dir="$profile" \
    --profile-directory=Default \
    --no-first-run \
    --no-default-browser-check \
    "$(start_url_for "$port")" \
    >>"$LOG_DIR/cdp-chrome-$port.log" 2>&1 &
  for _ in $(seq 1 20); do
    sleep 1
    if is_up "$port"; then
      echo "$port started ($(date -u +%FT%TZ))"
      return 0
    fi
  done
  echo "$port FAILED to start: see $LOG_DIR/cdp-chrome-$port.log"
  return 1
}

stop_one() {
  local port="$1" profile pids
  profile="$(profile_for "$port")" || { echo "unknown port $port"; return 1; }
  pids="$(pgrep -f -- "--user-data-dir=$profile" || true)"
  [[ -z "$pids" ]] && return 0
  # shellcheck disable=SC2086
  kill $pids 2>/dev/null || true
  for _ in $(seq 1 10); do
    sleep 1
    pgrep -f -- "--user-data-dir=$profile" >/dev/null || return 0
  done
  # shellcheck disable=SC2086
  kill -9 $(pgrep -f -- "--user-data-dir=$profile") 2>/dev/null || true
}

cmd="${1:-status}"
case "$cmd" in
  status)
    for p in "${PORTS[@]}"; do
      if is_up "$p"; then echo "$p up"; pages "$p"; else echo "$p DOWN"; fi
    done
    ;;
  start)
    rc=0
    for p in "${PORTS[@]}"; do start_one "$p" || rc=1; done
    exit "$rc"
    ;;
  restart)
    port="${2:?usage: cdp_browsers.sh restart PORT}"
    stop_one "$port" && start_one "$port"
    ;;
  *)
    echo "usage: cdp_browsers.sh status | start | restart PORT" >&2
    exit 2
    ;;
esac
