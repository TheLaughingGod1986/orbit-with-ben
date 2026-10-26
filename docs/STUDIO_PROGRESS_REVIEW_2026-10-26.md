# Studio progress and blockers — 26 October 2026

Read-only investigation of the Mac mini queue, board-data, page code, relay status and gate history, approximately 17:40–17:50 GMT. Queue and service availability continue to change. This review changes the dashboard presentation; it does not approve cuts, waive gates, spend credits or change YouTube schedules.

## Why progress appeared stuck

- The In progress badge counts **videos**, not completed jobs. The live board had five such videos while recording 15 completed jobs today. Finishing one task need not finish its video.
- All five of those video cards were paused. The server's generic progress line called blocked work “Queued”, so the page implied activity that was not happening.
- `tracker_app.js` returned uploaded videos directly to Done, even when `video_tracker.py` set `working=true` and placed them in progress for open/claimed work. The browser overrode the server's earlier fix.
- The top progress bar calculated completion from wall-clock time. It could show 95% despite no confirmed progress report. A worker reporting 1 of 4 steps could appear much further through merely because time passed.
- Work sent for Chief review remains blocked, not done. A completed worker phase can therefore be invisible in a completion-only summary.

## Presentation changes

- Label lane badges explicitly as videos, with a separate count of videos actively being worked on versus queued/waiting.
- Show studio-wide running, queued, waiting/review and completed-today **job** counts, a completion log with worker, date and result, and all waiting reasons. This section explicitly covers both channels, independent of video filters.
- Put each video's remaining tasks, current worker, confirmed steps, latest step note, wait reason and recent completions on its card. Broad backlog/audit jobs stay in studio activity, rather than inflating every film's task count.
- Preserve the server's actionable-work lane for uploaded videos. Once the server returns the video to Done, the browser does too.
- Only confirmed steps yield a completion percentage. No report means “Progress not reported”. Remaining time is labelled an estimate. Overdue claims are labelled stalled, rather than presented as live work.
- Keep expanded task/completion lists open across refreshes. Existing approve/change/watch actions remain in place.

## Blocker findings

The inspected queue held **35 blocked jobs**, plus three open jobs waiting on dependencies. These are distinct from the five video cards. The full live reasons are now inspectable in the proposed UI.

| Jobs | Recorded cause | What resolves it |
|---|---|---|
| J0302, J0345, J0862 | ElevenLabs exhausted: the recorded balance was 119 characters, versus 8,139 for Titan and 7,765 for Magnetic Field Flip. | Read the live balance after the recorded **30 October** reset, then resume in priority order. This investigation did not make a fresh provider-balance request. |
| J0863 | Flow picture generation awaits credit renewal, recorded as approximately **12 November**. | Verify renewed credit before generation; no paid overage. |
| J0123/J0124/J0135, J0241, J0317, J0861, J0875, J0910, J0923, J0958, J0960 | The remaining Related-video or pinned-comment step waits for a private scheduled long to become public. Some jobs already completed all other steps. | Resume only the unfinished step after go-public. Show a dated wait, not a rendering failure. |
| J0956 (Neptune, airs 27 October), J0974 (Apophis, airs 28 October), J0961 (three Betelgeuse Shorts) | Approved hash-locked exports fail the newer audio gate. Neptune is −1.4 dBTP against ≤−1.6. Apophis is −14.7 LUFS against −14.5…−13.5 and −1.4 dBTP. Betelgeuse is −1.5 dBTP; Wednesday also records −15.0 LUFS and a 44% opening-background match. | Chief must choose correction/approval handling. The safer technical route is corrected versioned exports, all gates rerun, and approval tied to the new hashes. Do not override the upload gate or reuse an old file approval for changed bytes. |
| J0935, J0936, J0966 | Recut batches are recorded as built/PASS, waiting for review and swap approval. | Chief reconciles the existing approval records against each exact export, then releases only eligible work. A worker PASS is not a final upload approval. |
| J0967, J0979, J0980/J0981/J0982, J0984/J0985, J0912 | Completed plans, audits, QA or a proposed extra Short await a protected Chief decision. | Review the recorded output and turn concrete repairs into worker jobs; close accepted review work rather than leave it indistinguishable from a failed render. |
| J0189, J0275, J0969, J0978 | Existing title/thumbnail experiments must finish before replacement tests are armed. | Read current Studio test state at the recorded due time. Some dates in J0275 have passed, so its old text needs reconciliation with the newer J0969 and ledger; elapsed dates alone do not prove the Studio test ended. |
| J0280 | Mixed job: older Related links are complete; future Blood links wait for 29 October, but its 26 October note adds qW2OsD4mujc → AL_-qlWko_g, whose long is already public. | Split the presently actionable follow-up from the future-public dependency after checking whether J0981 already covers it. A single blocked flag hides this distinction. |
| J0821 | A second light worker lane is held until two workers have been sustainably available. | Deliberate capacity decision, not a broken film. Revisit the recorded early-November checkpoint. |

## Why reviews accumulate

At approximately 17:45 the relay reported Grok down (no qualifying post for three hours) and Claude down (last heartbeat **23 October 20:51:35Z**). Cursor was selected as acting Chief, with Codex and Gemini available as workers. The board model status still marked Cursor's last run out of usage, while `chief_relay.py status` called it ready: these records are not synchronized observations. Neither proves a live session is currently running.

The authority policy in AGENTS.md reserves final approvals/PASS/merges for Grok or Claude acting as Chief; other stand-ins park those calls. Worker failover therefore keeps producing work without necessarily clearing the protected review queue. This review does not relax that policy. A live Chief review, or an explicit delegated authority decision from Ben, is needed for the protected calls.

## Verification

The changed JavaScript is exercised directly with Node for lane retention, confirmed progress, unknown progress, stale claims, dependencies, escaping, per-video attribution and completion/activity totals. Existing board and video tracker tests are also run. Phone layout is checked at 390 × 844 against the actual published board-data, without using approve/change controls. Final test counts and preview URL are recorded in the accompanying PR.
