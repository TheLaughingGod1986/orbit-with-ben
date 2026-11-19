#!/bin/bash
# Daily Buffer check on the posting Mac (LaunchAgent dev.orbit.buffer-check, STUDIO_PLAYBOOK.md §12).
#   1. Runs the latest main: pulls first, but only on main with no local code changes, so
#      work in progress in this checkout is never touched.
#   2. Runs buffer-mirror.ts check (keeps Buffer in step with YouTube, mirrors new uploads) for Orbit, then
#      for History of Science (--channel hos: HOS Shorts to HOS's Instagram/Facebook/TikTok, J0817).
#   3. Commits and pushes the Buffer record (social/) so GitHub and the Mac agree.
#   4. If the check failed, shows a notification. The details are in the log.
# Wrapped in a function so a pull that changes this file can't change it mid-run.
main() {
  # Guard the code being invoked, not a caller-supplied checkout environment.
  local engine
  engine="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)" || return 1
  python3 "$engine/scripts/engine_guard.py" || return 1
  local repo="${STUDIO_REPO:-${ORBIT_REPO:-$HOME/YouTube/orbit-with-ben}}"
  python3 "$repo/scripts/engine_guard.py" || return 1
  local social=00_Brand/Channel-Setup/social
  cd "$repo" || return 1
  echo "--- $(date)"
  local branch
  branch=$(git rev-parse --abbrev-ref HEAD)
  if [[ $branch == main ]] && git diff --quiet -- . ":(exclude)$social"; then
    git pull -q --ff-only origin main || echo "git pull skipped (not a fast-forward); running the code as it is"
  else
    echo "git pull skipped (on $branch, or local code changes); running the code as it is"
  fi
  # A pull or ORBIT_REPO override can select a different runtime: check that too.
  python3 "$repo/scripts/engine_guard.py" || return 1
  echo "code: $(git log --oneline -1)"

  # Resolve the records with the very same resolver as the CLI, before loading credentials.
  # Both channel registers stay in their existing content checkout after the engine moves.
  local records record_branch credentials
  records=$(cd "$repo/07_Content-Ops" && npx tsx scripts/buffer-mirror.ts record-root) || return 1
  [[ "$records" == /* && -d "$records/$social" ]] || { echo "Buffer record checkout unavailable" >&2; return 1; }
  record_branch=$(git -C "$records" rev-parse --abbrev-ref HEAD) || return 1
  credentials="${BUFFER_ENV_FILE:-$records/07_Content-Ops/.env}"
  [[ "$credentials" == /* && -f "$credentials" ]] || { echo "Buffer credential file unavailable" >&2; return 1; }

  (
    cd "$repo/07_Content-Ops" || exit 1
    unset DATABASE_URL GOOGLE_CLIENT_ID GOOGLE_CLIENT_SECRET YOUTUBE_REFRESH_TOKEN BUFFER_API_KEY BLOB_READ_WRITE_TOKEN \
      BUFFER_HOS_API_KEY YT_ANALYTICS_REFRESH_TOKEN_HOS
    # CLI owns the whole-operation lock; an outer npx lock self-deadlocks.
    npx tsx --env-file="$credentials" scripts/buffer-mirror.ts check
    owb=$?
    (( owb == 75 )) && exit 75
    echo "--- History of Science"
    npx tsx --env-file="$credentials" scripts/buffer-mirror.ts check --channel hos
    hos=$?
    (( owb != 0 )) && exit $owb
    exit $hos
  )
  local code=$?
  # Persist contention across LaunchAgent runs; never commit on a collision.
  local state_root="${DESK_LOCK_ROOT:-$HOME/_desk/locks}"
  local state="$state_root/buffer-check.last-exit"
  mkdir -p "$state_root"
  local previous=""
  [[ -f "$state" ]] && previous=$(cat "$state")
  printf '%s\n' "$code" > "$state"
  if (( code == 75 )); then
    if [[ "$previous" == 75 ]]; then
      osascript -e 'display notification "The Buffer check hit the desk lock twice in a row. See ~/Library/Logs/orbit-buffer-check.log" with title "Orbit With Ben"' 2>/dev/null
    fi
    return 75
  fi

  if [[ $record_branch == main ]] && [[ -n $(git -C "$records" status --porcelain -- "$social") ]]; then
    git -C "$records" add -- "$social"
    git -C "$records" commit -q -m "Buffer check $(date +%F): record what Buffer holds" -- "$social" &&
      { git -C "$records" push -q origin main || echo "record not pushed (it goes with the next push)"; }
  fi

  if (( code != 0 )); then
    osascript -e 'display notification "The Buffer check needs a look. See ~/Library/Logs/orbit-buffer-check.log" with title "Orbit With Ben"' 2>/dev/null
  fi
  return $code
}
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi
