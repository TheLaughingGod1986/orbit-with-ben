#!/bin/bash
# Daily Buffer check on the posting Mac (LaunchAgent dev.orbit.buffer-check, STUDIO_PLAYBOOK.md §12).
#   1. Runs the latest main: pulls first, but only on main with no local code changes, so
#      work in progress in this checkout is never touched.
#   2. Runs buffer-mirror.ts check (keeps Buffer in step with YouTube, mirrors new uploads).
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
    unset DATABASE_URL GOOGLE_CLIENT_ID GOOGLE_CLIENT_SECRET YOUTUBE_REFRESH_TOKEN BUFFER_API_KEY BLOB_READ_WRITE_TOKEN
    npx tsx --env-file=.env scripts/buffer-mirror.ts check
  )
  local code=$?

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
