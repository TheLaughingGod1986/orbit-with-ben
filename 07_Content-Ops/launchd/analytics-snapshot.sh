#!/bin/bash
# Daily channel tracker on the posting Mac (LaunchAgent dev.orbit.analytics-snapshot, 06:40 London).
#   1. Works in its own worktree (~/_desk/worktrees/analytics, detached at origin/main), never in
#      the shared checkout, so nobody's work in progress gets swept into its commit.
#   2. Snapshots both channels (read only) with the shared checkout's .env and node_modules.
#   3. Gates every Short scheduled in the next 14 days (gate_upcoming.py: report only, and adds any
#      missing one to the open-gate library), rebuilds 05_Analytics/<channel>/REPORT.md and the
#      dashboard, commits only 05_Analytics/ and library.json, and pushes to main.
#      launchd can't read the NAS (macOS privacy): a Short whose files are there is checked from the copy an agent
#      staged with `gate_upcoming.py --stage` (~/_desk/cache/gate-media), else it reads NOT CHECKED (26 Oct 2026). A failed channel still lets the other one through, then notifies.
#   4. Runs scripts/board_publish.py once, so the tracker web app (studio-kanban.pages.dev/tracker) shows the new data.
# Wrapped in a function so a pull that changes this file can't change it mid-run.

# Run a command with a time limit in seconds (macOS has no `timeout`). The alarm survives the exec, so a command that
# never returns is stopped and reads as a failure.
within() {
  local secs=$1; shift
  perl -e 'alarm shift; exec @ARGV' "$secs" "$@"
}

# True when a folder exists (or can be made) and can be written, inside 5 s. launchd cannot open a removable volume
# without a macOS permission click that nobody is there to make; a call into one just sits there.
# 11 Nov 2026: `mkdir -p` and `test -w` both passed on the removable SSD while every file on it stayed unreadable to
# launchd, so the run chose a worktree it then could not open. The check now writes a file and reads it back.
usable() {
  within 5 /bin/sh -c 'mkdir -p "$1" && f="$1/.usable.$$" && echo ok > "$f" && cat "$f" >/dev/null && rm -f "$f"' \
    sh "$1" >/dev/null 2>&1
}

# True when a worktree that is already there can be read (its .git pointer opens), or when there is none yet.
readable_worktree() {
  [[ ! -e "$1" ]] && return 0
  within 5 /bin/sh -c 'cat "$1/.git" >/dev/null' sh "$1" >/dev/null 2>&1
}

# Where the tracker's own worktree goes. 10 Nov 2026: no snapshot was made, because ~/_desk/worktrees had moved to
# the removable SSD on 9 Nov and the first git call never came back. A folder that does not answer is not used:
# the tracker keeps a worktree on the internal disk instead.
pick_worktree() {
  local want="${ANALYTICS_WORKTREE:-$HOME/_desk/worktrees/analytics}"
  local safe="${ANALYTICS_SAFE_DIR:-$HOME/Library/Application Support/owb-analytics}"
  if usable "$(dirname "$want")" && readable_worktree "$want"; then
    echo "$want"
  else
    echo "worktree folder $(dirname "$want") did not answer or cannot be written; using $safe/worktree" >&2
    echo "$safe/worktree"
  fi
}

# Run the Shorts gate with a time limit and say so when it runs out. Gives back the gate's own exit code, or 142.
# 10 Nov 2026: with the worktree fixed, the hand run got as far as the gate, which hung until someone stopped it.
# The gate comes before the commit, so a gate that hangs would cost the day's snapshot as well.
gate_with_limit() {
  local limit=$1; shift
  within "$limit" "$@"
  local rc=$?
  if (( rc == 142 )); then
    echo "Shorts gate did not finish inside ${limit}s and was stopped; the gate report is from an earlier day. The snapshot and reports still go out."
  fi
  return $rc
}

# True when wt is a valid git worktree belonging to repo (same resolved git-common-dir).
same_repo_worktree() {
  local repo="$1" wt="$2"
  local repo_common wt_common
  repo_common="$(within 60 git -C "$repo" rev-parse --git-common-dir 2>/dev/null)" || return 1
  wt_common="$(within 60 git -C "$wt" rev-parse --git-common-dir 2>/dev/null)" || return 1
  repo_common="$(cd "$repo" && cd "$repo_common" && pwd -P)" || return 1
  wt_common="$(cd "$wt" && cd "$wt_common" && pwd -P)" || return 1
  [[ "$repo_common" == "$wt_common" ]]
}

# Remove a missing/corrupted worktree directory (never repo itself) and recreate it detached at origin/main.
recreate_tracker_worktree() {
  local repo="$1" wt="$2"
  local repo_real wt_real
  repo_real="$(cd "$repo" 2>/dev/null && pwd -P)" || return 1
  [[ -z "$wt" || "$wt" == "/" ]] && return 1
  if [[ -e "$wt" ]]; then
    wt_real="$(cd "$wt" 2>/dev/null && pwd -P || true)"
    [[ -n "$wt_real" && "$wt_real" == "$repo_real" ]] && return 1
    within 60 git -C "$repo" worktree remove --force "$wt" >/dev/null 2>&1 || true
    rm -rf "$wt" || return 1
  fi
  mkdir -p "$(dirname "$wt")" || return 1
  within 60 git -C "$repo" worktree prune >/dev/null 2>&1 || true
  git -C "$repo" fetch -q origin main && within 300 git -C "$repo" worktree add -q --detach "$wt" origin/main
}

# Ensure the tracker worktree exists, belongs to repo, preserves any leftover tracker data, and is updated
# onto origin/main before engine_guard.py or snapshot scripts run inside it.
prepare_tracker_worktree() {
  local repo="$1" wt="$2"
  local data="05_Analytics"
  local ww2_data="channels/ww2/05_Analytics"
  local lib="00_Brand/Channel-Setup/audits/shorts_open_library/library.json"

  if ! within 60 git -C "$wt" rev-parse --git-dir >/dev/null 2>&1; then
    recreate_tracker_worktree "$repo" "$wt" \
      || { echo "could not make the tracker worktree at $wt; nothing run"; return 1; }
    return 0
  fi

  if ! same_repo_worktree "$repo" "$wt"; then
    echo "tracker worktree at $wt does not belong to $repo; nothing run" >&2
    return 1
  fi

  local gitdir
  gitdir="$(git -C "$wt" rev-parse --git-dir 2>/dev/null)" || {
    recreate_tracker_worktree "$repo" "$wt" \
      || { echo "could not make the tracker worktree at $wt; nothing run"; return 1; }
    return 0
  }
  [[ "$gitdir" == /* ]] || gitdir="$wt/$gitdir"
  if [[ -d "$gitdir/rebase-merge" || -d "$gitdir/rebase-apply" ]]; then
    git -C "$wt" rebase --abort >/dev/null 2>&1 || true
  fi

  # Anything a failed run left behind is tracker data: keep it, then catch up with main.
  local p
  local stage_paths=()
  for p in "$data" "$lib" "$ww2_data"; do
    if [[ -e "$wt/$p" ]] || git -C "$wt" ls-files --error-unmatch -- "$p" >/dev/null 2>&1; then
      stage_paths+=("$p")
    fi
  done
  if (( ${#stage_paths[@]} > 0 )); then
    git -C "$wt" add -A -- "${stage_paths[@]}"
    git -C "$wt" diff --cached --quiet \
      || git -C "$wt" commit -q -m "Channel tracker: data from an earlier run" -- "${stage_paths[@]}"
  fi

  if ! git -C "$wt" fetch -q origin main; then
    echo "git fetch origin main failed in $wt; nothing run" >&2
    return 1
  fi

  if ! git -C "$wt" rebase -q origin/main; then
    git -C "$wt" rebase --abort >/dev/null 2>&1 || true
    # If there are no unpushed local commits and no dirty tracker files, recreate a stale/corrupted worktree cleanly.
    if [[ -z "$(git -C "$wt" log origin/main..HEAD --oneline 2>/dev/null)" ]] \
      && [[ -z "$(git -C "$wt" status --porcelain -- "${stage_paths[@]}" 2>/dev/null)" ]]; then
      echo "worktree at $wt could not rebase with no local commits; recreating cleanly" >&2
      recreate_tracker_worktree "$repo" "$wt" \
        || { echo "could not make the tracker worktree at $wt; nothing run"; return 1; }
      return 0
    fi
    echo "rebase onto main failed; nothing run"
    osascript -e 'display notification "The channel tracker could not catch up with main. See ~/Library/Logs/orbit-analytics.log" with title "Orbit With Ben"' 2>/dev/null
    return 1
  fi
  return 0
}

# Push detached HEAD to origin/main; on non-fast-forward rejection, fetch and rebase onto origin/main
# with bounded retries (default 3 attempts) before failing.
push_with_rebase_retry() {
  local max_attempts="${PUSH_RETRIES:-3}"
  local delay_base="${PUSH_RETRY_DELAY_S:-5}"
  local attempt=1
  while (( attempt <= max_attempts )); do
    if git push -q origin HEAD:main; then
      return 0
    fi
    if (( attempt == max_attempts )); then
      echo "git push to origin/main failed after ${max_attempts} attempts" >&2
      return 1
    fi
    if (( delay_base > 0 )); then
      sleep $((attempt * delay_base))
    fi
    if ! git fetch -q origin main || ! git rebase -q origin/main; then
      git rebase --abort 2>/dev/null || true
      echo "rebase onto origin/main failed during push retry (attempt ${attempt}/${max_attempts})" >&2
      return 1
    fi
    attempt=$((attempt + 1))
  done
  return 1
}

main() {
  local engine
  engine="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)" || return 1
  python3 "$engine/scripts/engine_guard.py" || return 1
  # launchd's login shell has no Homebrew on PATH: without it gate_upcoming.py can't find ffprobe/ffmpeg and every
  # scheduled Short reads FAIL (8 Oct 2026).
  export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
  local repo="${ORBIT_REPO:-$HOME/YouTube/orbit-with-ben}"
  python3 "$repo/scripts/engine_guard.py" || return 1
  local data=05_Analytics
  local ww2_data="channels/ww2/05_Analytics"
  local lib=00_Brand/Channel-Setup/audits/shorts_open_library/library.json
  echo "--- $(date)"
  local wt; wt="$(pick_worktree)"
  # Update/fetch/rebase (or recreate) the tracker worktree onto origin/main BEFORE running $wt/scripts/engine_guard.py,
  # so a stale worktree predating engine_guard.py updates first instead of failing with ENOENT.
  prepare_tracker_worktree "$repo" "$wt" || return 1
  cd "$wt" || return 1
  python3 "$wt/scripts/engine_guard.py" || return 1
  ln -sfn "$repo/07_Content-Ops/node_modules" 07_Content-Ops/node_modules
  echo "code: $(git log --oneline -1)"

  (
    cd 07_Content-Ops || exit 1
    unset GOOGLE_CLIENT_ID GOOGLE_CLIENT_SECRET YOUTUBE_REFRESH_TOKEN YT_ANALYTICS_REFRESH_TOKEN_OWB YT_ANALYTICS_REFRESH_TOKEN_HOS YT_ANALYTICS_REFRESH_TOKEN_WW2 YT_CHANNEL_ID_WW2
    npx tsx --env-file="$repo/07_Content-Ops/.env" scripts/analytics-snapshot.ts
  )
  local code=$?
  # The existing unattended Studio worker gathers fields absent from the Analytics API.
  # Keep queue commits in the shared checkout; the tracker worktree commits only analytics data.
  (
    cd 07_Content-Ops || exit 1
    unset YT_CHANNEL_ID_WW2 YT_ANALYTICS_REFRESH_TOKEN_WW2
    FIELD_ORDER_QUEUE_REPO="$repo" within 180 npx tsx --env-file="$repo/07_Content-Ops/.env" scripts/field-order-dispatch.ts
  ) || code=1
  # Gate every Short scheduled in the next 14 days and add any missing one to the open-gate library.
  # Report only: a FAIL is for Claude to act on at 07:10; nothing here touches YouTube.
  local snap="$data/owb/snapshots/$(TZ=Europe/London date +%F).json"
  # The staged copies of NAS files live in ~/_desk/cache. If that folder does not answer, point the gate at an
  # empty folder on the internal disk: those Shorts read NOT CHECKED today, and the run still finishes.
  local gate_cache=()
  if ! usable "$HOME/_desk/cache"; then
    local safe_cache="${ANALYTICS_SAFE_DIR:-$HOME/Library/Application Support/owb-analytics}/gate-media"
    echo "gate cache $HOME/_desk/cache did not answer; using $safe_cache (Shorts on the NAS read NOT CHECKED today)"
    mkdir -p "$safe_cache"
    gate_cache=(--cache "$safe_cache")
  fi
  if [[ -f $snap ]]; then
    gate_with_limit "${GATE_LIMIT_S:-600}" python3 00_Brand/Channel-Setup/tools/gate_upcoming.py --snapshot "$snap" \
      --uploads 00_Brand/Channel-Setup/social/UPLOADS.json --media-root "$repo" \
      --out "$data/owb/UPCOMING_SHORTS_GATE.md" --add "${gate_cache[@]}"
    (( $? == 142 )) && code=1   # a stopped gate is worth the "needs a look" notice; a normal gate result is not
  fi
  (cd 07_Content-Ops && npx tsx scripts/analytics-report.ts) || code=1

  local p
  local commit_paths=()
  for p in "$data" "$lib" "$ww2_data"; do
    if [[ -e "$p" ]] || git ls-files --error-unmatch -- "$p" >/dev/null 2>&1; then
      commit_paths+=("$p")
    fi
  done
  if (( ${#commit_paths[@]} > 0 )) && [[ -n $(git status --porcelain -- "${commit_paths[@]}") ]]; then
    git add -A -- "${commit_paths[@]}"
    git commit -q -m "Channel tracker $(date +%F): daily snapshot, reports, dashboard, upcoming Shorts gate" -- "${commit_paths[@]}"
  fi
  if [[ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ]]; then
    if push_with_rebase_retry; then
      # Put the new data on the board-data branch now: studio-kanban.pages.dev/tracker reads tracker.json from there.
      # board_publish.py never fails and is a no-op when nothing changed; its 5-minute launchd run would catch it anyway.
      if [[ ${BOARD_PUBLISH:-1} != 0 && -f $repo/scripts/board_publish.py ]]; then
        HOS_REPO="${HOS_REPO:-$HOME/YouTube/History Of Science}" python3 "$repo/scripts/board_publish.py" --quiet
      fi
    else
      code=1
    fi
  fi

  if (( code != 0 )); then
    osascript -e 'display notification "The channel tracker needs a look. See ~/Library/Logs/orbit-analytics.log" with title "Orbit With Ben"' 2>/dev/null
  fi
  return $code
}
# Not run when the file is sourced (the tests source it for the helpers above).
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  # Refuse retired entrypoints before even starting the watchdog.
  engine="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)" || exit 1
  python3 "$engine/scripts/engine_guard.py" || exit 1
  # A run that hangs must not block tomorrow's: launchd will not start a new run while this one is alive.
  # One process, so stopping it when the run ends first leaves nothing behind and runs nothing more.
  perl -e 'sleep 2700; print "tracker run still going after 45 minutes; stopping it\n"; kill "TERM", $ARGV[0]' $$ &
  watchdog=$!
  main "$@"; code=$?
  kill "$watchdog" 2>/dev/null
  exit $code
fi
