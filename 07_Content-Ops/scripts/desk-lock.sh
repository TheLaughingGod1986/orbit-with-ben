#!/bin/bash
# desk-lock — atomic per-task lock for Mini YouTube/Buffer writers.
#
# Lock path:  ~/_desk/locks/<name>.lock/   (mkdir is atomic; no flock required)
# Metadata:   ~/_desk/locks/<name>.lock/owner.txt
#
# Usage:
#   desk-lock <lock-name> -- <command...>     # acquire, run, release
#   desk-lock acquire <lock-name>             # acquire only (prints lock dir)
#   desk-lock release <lock-name>             # release if we own it (or --force)
#   desk-lock status  <lock-name>             # 0=free/stale-cleared info, 1=held
#   desk-lock held-by <lock-name>             # print owner.txt or "free"
#
# Exit codes:
#   0   ok
#   2   usage error
#   75  lock held by another live process (EX_TEMPFAIL)
#   other: underlying command exit
#
# Env:
#   DESK_LOCK_ROOT   override lock root (default: ~/_desk/locks)
#   DESK_LOCK_FORCE=1  release even if pid looks alive (dangerous; ops only)

set -euo pipefail

LOCK_ROOT="${DESK_LOCK_ROOT:-$HOME/_desk/locks}"
mkdir -p "$LOCK_ROOT"

usage() {
  cat >&2 <<'U'
usage:
  desk-lock <lock-name> -- <command...>
  desk-lock acquire|release|status|held-by <lock-name>
U
  exit 2
}

sanitize() {
  # Keep alnum, dash, underscore, dot; collapse other runs to _
  printf '%s' "$1" | tr -c 'A-Za-z0-9._-' '_' | sed 's/__*/_/g; s/^_//; s/_$//'
}

lock_dir_for() {
  local name
  name="$(sanitize "$1")"
  [ -n "$name" ] || { echo "desk-lock: empty lock name after sanitize" >&2; exit 2; }
  printf '%s/%s.lock' "$LOCK_ROOT" "$name"
}

pid_alive() {
  local pid="$1"
  [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null
}

read_owner_pid() {
  local dir="$1"
  if [ -f "$dir/owner.txt" ]; then
    # first line: pid=NNN
    sed -n 's/^pid=//p' "$dir/owner.txt" | head -1
  fi
}

write_owner() {
  local dir="$1"
  {
    echo "pid=$$"
    echo "ppid=$PPID"
    echo "user=$(id -un)"
    echo "host=$(hostname -s 2>/dev/null || hostname)"
    echo "started_at=$(date '+%Y-%m-%dT%H:%M:%S%z')"
    echo "cwd=$(pwd)"
    echo "cmd=${DESK_LOCK_CMD:-$0 $*}"
  } > "$dir/owner.txt"
}

clear_stale() {
  local dir="$1"
  local pid
  [ -d "$dir" ] || return 0
  pid="$(read_owner_pid "$dir" || true)"
  if [ -n "$pid" ] && pid_alive "$pid"; then
    return 1  # live holder
  fi
  # A missing owner may be an acquisition in progress; fail closed.
  [ -n "$pid" ] || return 1
  # Explicit stale inspection only.
  rm -rf "$dir"
  return 0
}

show_held() {
  local dir="$1"
  echo "desk-lock: HELD  $dir" >&2
  if [ -f "$dir/owner.txt" ]; then
    echo "desk-lock: owner:" >&2
    sed 's/^/  /' "$dir/owner.txt" >&2
  else
    echo "desk-lock: (no owner.txt — another process may have just created the dir)" >&2
  fi
  echo "desk-lock: stop. Wait for the holder to finish, or if the pid is dead: desk-lock release $(basename "$dir" .lock)" >&2
}

do_acquire() {
  local name="$1"
  local dir
  dir="$(lock_dir_for "$name")"
  # Serialize reclaimers; missing/fresh metadata always fails closed.
  if ! mkdir "$dir" 2>/dev/null; then
    if mkdir "$dir.reclaim" 2>/dev/null; then
      local pid modified now
      pid="$(read_owner_pid "$dir" || true)"
      modified="$(stat -f %m "$dir/owner.txt" 2>/dev/null || stat -c %Y "$dir/owner.txt" 2>/dev/null || echo 0)"
      now="$(date +%s)"
      if [[ "$pid" =~ ^[1-9][0-9]*$ ]] && ! pid_alive "$pid" &&
          [[ "$modified" =~ ^[0-9]+$ ]] && (( modified > 0 && now - modified > 300 )); then
        echo "desk-lock: reclaiming stale lock (pid=$pid dead, owner.txt >5m)" >&2
        rm -rf "$dir"
      fi
      rmdir "$dir.reclaim"
    fi
    if ! mkdir "$dir" 2>/dev/null; then
      show_held "$dir"
      exit 75
    fi
  fi
  DESK_LOCK_CMD="${DESK_LOCK_CMD:-acquire $name}" write_owner "$dir"
  echo "$dir"
  return 0
}

do_release() {
  local name="$1"
  local force="${DESK_LOCK_FORCE:-0}"
  local dir
  dir="$(lock_dir_for "$name")"
  if [ ! -d "$dir" ]; then
    echo "desk-lock: already free  $dir"
    return 0
  fi
  local pid
  pid="$(read_owner_pid "$dir" || true)"
  if [ "$force" = "1" ]; then
    rm -rf "$dir"
    echo "desk-lock: force-released  $dir"
    return 0
  fi
  if [ -n "$pid" ] && [ "$pid" = "$$" ]; then
    rm -rf "$dir"
    echo "desk-lock: released  $dir"
    return 0
  fi
  # Parent wrappers: allow release if we are the recorded pid OR the recorded pid is dead
  if [ -n "$pid" ] && ! pid_alive "$pid"; then
    rm -rf "$dir"
    echo "desk-lock: released (stale)  $dir"
    return 0
  fi
  # Allow release from the same process tree when called as: desk-lock <name> -- cmd
  # (holder pid is the desk-lock wrapper itself)
  if [ -n "${DESK_LOCK_HELD_DIR:-}" ] && [ "$DESK_LOCK_HELD_DIR" = "$dir" ]; then
    rm -rf "$dir"
    echo "desk-lock: released  $dir"
    return 0
  fi
  echo "desk-lock: refuse release — live holder pid=$pid (set DESK_LOCK_FORCE=1 to override)" >&2
  show_held "$dir"
  exit 75
}

do_status() {
  local name="$1"
  local dir
  dir="$(lock_dir_for "$name")"
  if [ ! -d "$dir" ]; then
    echo "free  $dir"
    return 0
  fi
  if clear_stale "$dir"; then
    echo "free (cleared stale)  $dir"
    return 0
  fi
  echo "held  $dir"
  [ -f "$dir/owner.txt" ] && cat "$dir/owner.txt"
  return 1
}

# --- main ---
[ $# -ge 1 ] || usage

case "$1" in
  acquire)
    [ $# -eq 2 ] || usage
    do_acquire "$2"
    ;;
  release)
    [ $# -eq 2 ] || usage
    do_release "$2"
    ;;
  status)
    [ $# -eq 2 ] || usage
    do_status "$2"
    ;;
  held-by)
    [ $# -eq 2 ] || usage
    dir="$(lock_dir_for "$2")"
    if [ -f "$dir/owner.txt" ]; then cat "$dir/owner.txt"; else echo "free"; fi
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    # desk-lock <name> -- <command...>
    name="$1"; shift
    [ "${1:-}" = "--" ] || usage
    shift
    [ $# -ge 1 ] || usage
    export DESK_LOCK_CMD="$*"
    held="$(do_acquire "$name")"
    export DESK_LOCK_HELD_DIR="$held"
    release_on_exit() {
      DESK_LOCK_HELD_DIR="$held" DESK_LOCK_FORCE=0
      # Always release our own lock dir on exit
      rm -rf "$held" 2>/dev/null || true
    }
    trap release_on_exit EXIT
    child=""
    stop_child() {
      local signal="$1" code="$2"
      if [ -n "$child" ]; then
        kill -s "$signal" "$child" 2>/dev/null || true
        wait "$child" 2>/dev/null || true
      fi
      exit "$code"
    }
    trap 'stop_child INT 130' INT
    trap 'stop_child TERM 143' TERM
    trap 'stop_child HUP 129' HUP
    set +e
    "$@" &
    child=$!
    wait "$child"
    rc=$?
    set -e
    exit "$rc"
    ;;
esac
