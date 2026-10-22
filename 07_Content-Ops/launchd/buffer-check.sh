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
  local repo="${ORBIT_REPO:-$HOME/YouTube/orbit-with-ben}"
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
  echo "code: $(git log --oneline -1)"

  (
    cd 07_Content-Ops || exit 1
    unset DATABASE_URL GOOGLE_CLIENT_ID GOOGLE_CLIENT_SECRET YOUTUBE_REFRESH_TOKEN BUFFER_API_KEY BLOB_READ_WRITE_TOKEN \
      BUFFER_HOS_API_KEY YT_ANALYTICS_REFRESH_TOKEN_HOS
    bash scripts/desk-lock.sh youtube-buffer -- npx tsx --env-file=.env scripts/buffer-mirror.ts check
    owb=$?
    (( owb == 75 )) && exit 75
    echo "--- History of Science"
    bash scripts/desk-lock.sh youtube-buffer -- npx tsx --env-file=.env scripts/buffer-mirror.ts check --channel hos
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

  if [[ $branch == main ]] && [[ -n $(git status --porcelain -- "$social") ]]; then
    git add -- "$social"
    git commit -q -m "Buffer check $(date +%F): record what Buffer holds" -- "$social" &&
      { git push -q origin main || echo "record not pushed (it goes with the next push)"; }
  fi

  if (( code != 0 )); then
    osascript -e 'display notification "The Buffer check needs a look. See ~/Library/Logs/orbit-buffer-check.log" with title "Orbit With Ben"' 2>/dev/null
  fi
  return $code
}
main "$@"
