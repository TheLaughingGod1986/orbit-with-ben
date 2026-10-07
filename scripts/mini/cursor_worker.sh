#!/bin/bash
# cursor_worker.sh: wake Cursor's CLI agent on a schedule so it works through its queue while it covers as Chief.
# Ben, 7 Oct 2026: Grok Bot is out of credit; Cursor holds the write lane for both studios (AGENTS.md "Who does what";
# HOS AGENTS.md "The desk"). Cursor's `agent` only works while a session runs, so without this nothing picks up its
# tasks between Ben's prompts.
#
# Run by launchd every 30 min (com.owb.cursor-worker.plist). Each run does at most ONE job, then exits:
#   1. Only while ~/_desk/state/cursor-covers-chief exists (delete that file when Grok is back: two Chiefs collide).
#   2. Only 08:00-22:00 local, and never while another run (or a manual Cursor session using the lock) holds the lock.
#   3. Asks `agent` to read the OWB studio thread and the HOS desk inbox, pick the single oldest task addressed to it
#      (or a claim it holds), do the next step under each repo's AGENTS.md, post the result, and stop. 25-minute cap.
# Log: ~/Library/Logs/cursor-worker.log. Pause it: `touch ~/_desk/state/cursor-worker.pause`.
#
# CURSOR_AGENT_FLAGS (default "-p --force"): -p runs one prompt without a chat window; --force lets it run the shell
# commands its rules allow without asking. Check `agent --help` if your version names them differently.
set -u
STATE="${DESK_STATE:-$HOME/_desk/state}"
LOCKS="${DESK_LOCK_ROOT:-$HOME/_desk/locks}"
OWB="${OWB_REPO:-$HOME/YouTube/orbit-with-ben}"
HOS="${HOS_REPO:-$HOME/YouTube/history-of-science}"
AGENT_BIN="${CURSOR_AGENT_BIN:-$(command -v agent || echo "$HOME/.local/bin/agent")}"
FLAGS="${CURSOR_AGENT_FLAGS:--p --force}"
CAP_S="${CURSOR_WORKER_CAP_S:-1500}"
HOURS="${CURSOR_WORKER_HOURS:-8-22}"

log() { echo "$(date '+%F %T') $*"; }
[[ -f "$STATE/cursor-covers-chief" ]] || { log "skip: not covering as Chief (no $STATE/cursor-covers-chief)"; exit 0; }
[[ -f "$STATE/cursor-worker.pause" ]] && { log "skip: paused"; exit 0; }
h=$((10#$(date +%H))); lo=${HOURS%-*}; hi=${HOURS#*-}
(( h >= lo && h < hi )) || { log "skip: outside $HOURS"; exit 0; }
[[ -x "$AGENT_BIN" ]] || { log "FAIL: Cursor agent not found ($AGENT_BIN)"; exit 1; }

mkdir -p "$LOCKS"
LOCK="$LOCKS/cursor-worker.lock"
if ! mkdir "$LOCK" 2>/dev/null; then
  pid=$(cat "$LOCK/pid" 2>/dev/null || echo "")
  if [[ -n $pid ]] && kill -0 "$pid" 2>/dev/null; then log "skip: previous run $pid still working"; exit 0; fi
  rm -rf "$LOCK"; mkdir "$LOCK" || exit 0
fi
echo $$ > "$LOCK/pid"
trap 'rm -rf "$LOCK"' EXIT

read -r -d '' PROMPT <<TXT
You are Cursor, covering as Chief on the Mac mini while Grok Bot is out of credit. You run unattended: do ONE job, then stop.

1. Orbit With Ben ($OWB): git pull. Read AGENTS.md (the rules, the Never list, "Stop and ask Ben", "Who does what").
   Run: python3 scripts/owb_thread.py read   and   python3 scripts/studio.py board
2. History of Science ($HOS): git pull. Read its AGENTS.md ("The desk"). Run its desk inbox: hos_desk.py inbox --as cursor
3. First the job queue (AGENTS.md "Job queue"):  python3 scripts/jobs.py next --agent cursor --can mini,gemini,any --git
   If it prints a job, that job is yours: do it (step 4), then  jobs.py done|block|release <id> --agent cursor ... --git.
   Only if it exits 10 (nothing waiting): pick the single oldest task addressed to you that isn't in the queue (to=cursor
   on the HOS desk, or a Claude message on #99 asking Cursor/Chief for something with no reply from you yet).
   If nothing is waiting anywhere, stop without posting.
4. Do that one task, following that repo's AGENTS.md exactly: claim before work (studio.py claim --git, or the HOS
   desk's own rule), commit only from a clean worktree, never spend money or credit beyond the written rules, never
   upload, schedule, retitle or change privacy on YouTube unless Claude's message for that task says to, never delete
   anything on the NAS, and never print secrets. If a step needs Ben (money, a sign-in, a decision), say so in your
   report and stop.
5. Report: OWB with  python3 scripts/owb_thread.py post "..."  (start with "Cursor covering"); HOS with
   hos_desk.py post --from cursor --to claude ...  Say what you did, what's next, and what blocks you.
If a job will take longer than about 20 minutes, do a clean stopping point, release or extend your claim, report, and stop.
TXT

log "run: $AGENT_BIN $FLAGS (cap ${CAP_S}s)"
cd "$OWB" || { log "FAIL: no $OWB"; exit 1; }
# perl alarm = a timeout macOS ships with; the agent is killed at the cap.
perl -e 'alarm shift; exec @ARGV' "$CAP_S" "$AGENT_BIN" $FLAGS "$PROMPT"
code=$?
log "done: exit $code"
if (( code != 0 && code != 142 )); then
  osascript -e 'display notification "The Cursor worker run failed. See ~/Library/Logs/cursor-worker.log" with title "Studio"' 2>/dev/null
fi
exit 0
