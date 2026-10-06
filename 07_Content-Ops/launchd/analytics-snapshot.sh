#!/bin/bash
# Daily channel tracker on the posting Mac (LaunchAgent dev.orbit.analytics-snapshot, 06:40 London).
#   1. Works in its own worktree (~/_desk/worktrees/analytics, detached at origin/main), never in
#      the shared checkout, so nobody's work in progress gets swept into its commit.
#   2. Snapshots both channels (read only) with the shared checkout's .env and node_modules.
#   3. Rebuilds 05_Analytics/<channel>/REPORT.md and the dashboard, commits only 05_Analytics/,
#      and pushes to main. A failed channel still lets the other one through, then notifies.
# Wrapped in a function so a pull that changes this file can't change it mid-run.
main() {
  local repo="${ORBIT_REPO:-$HOME/YouTube/orbit-with-ben}"
  local wt="${ANALYTICS_WORKTREE:-$HOME/_desk/worktrees/analytics}"
  local data=05_Analytics
  echo "--- $(date)"
  if ! git -C "$wt" rev-parse --git-dir >/dev/null 2>&1; then
    mkdir -p "$(dirname "$wt")"
    git -C "$repo" fetch -q origin main && git -C "$repo" worktree add -q --detach "$wt" origin/main || return 1
  fi
  cd "$wt" || return 1
  ln -sfn "$repo/07_Content-Ops/node_modules" 07_Content-Ops/node_modules

  # Anything a failed run left behind is tracker data: keep it, then catch up with main.
  git add -A -- "$data"
  git diff --cached --quiet || git commit -q -m "Channel tracker: data from an earlier run" -- "$data"
  git fetch -q origin main
  if ! git rebase -q origin/main; then
    git rebase --abort
    echo "rebase onto main failed; nothing run"
    osascript -e 'display notification "The channel tracker could not catch up with main. See ~/Library/Logs/orbit-analytics.log" with title "Orbit With Ben"' 2>/dev/null
    return 1
  fi
  echo "code: $(git log --oneline -1)"

  (
    cd 07_Content-Ops || exit 1
    unset GOOGLE_CLIENT_ID GOOGLE_CLIENT_SECRET YOUTUBE_REFRESH_TOKEN YT_ANALYTICS_REFRESH_TOKEN_OWB YT_ANALYTICS_REFRESH_TOKEN_HOS
    npx tsx --env-file="$repo/07_Content-Ops/.env" scripts/analytics-snapshot.ts
  )
  local code=$?
  (cd 07_Content-Ops && npx tsx scripts/analytics-report.ts) || code=1

  if [[ -n $(git status --porcelain -- "$data") ]]; then
    git add -A -- "$data"
    git commit -q -m "Channel tracker $(date +%F): daily snapshot, reports and dashboard" -- "$data"
    local i
    for i in 1 2 3; do
      git push -q origin HEAD:main && break
      sleep $((i * 5))
      git pull -q --rebase origin main || { git rebase --abort 2>/dev/null; break; }
    done
  fi

  if (( code != 0 )); then
    osascript -e 'display notification "The channel tracker needs a look. See ~/Library/Logs/orbit-analytics.log" with title "Orbit With Ben"' 2>/dev/null
  fi
  return $code
}
main "$@"
