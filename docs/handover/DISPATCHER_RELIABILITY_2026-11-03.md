# Dispatcher reliability repair — 3 November 2026

Ben asked to repair dispatch before further production work. This changes scheduling/monitoring only; it grants no media approvals, publishing, credit spend, extra concurrent execution slots or automatic MacBook migration.

## Fixed paths

- A recently released task yields behind other ready work even if its deadline is old. The relay excludes already-attempted released/done/blocked tasks for the rest of the current run and continues immediately to other eligible work. It never drops an unfinished claim or interrupts a process-validated execution lease.
- A specialist exiting with an ordinary error is marked down under the existing retry policy; healthy workers can continue in that same run. Existing usage/model failover still applies.
- Automatically created condition-verification tasks cannot use their synthetic one-hour deadline to outrank real production. Checks for a parent with a recorded production deadline retain its actual inherited deadline. Chief decisions and manual urgent requests retain their gates.
- Required capabilities are filtered before choosing the preferred worker, including immediate requests, rerouted-worker failover, direct queue claims and board projections. Online/model names are insufficient proof. Named independent assignments and Chief authority remain intact.

## Capability contract

New tasks can specify `jobs.py add ... --requires audio_input,moving_video_input`. Declare only actual requirements. Existing jobs without explicit requirements retain their eligibility.

When input capability prevents a claimed task from progressing, use:

```
python3 scripts/jobs.py wait JOB --agent AGENT --type capability --requires audio_input \
  --condition 'Actual listening tool is unavailable; describe observed capability check' \
  --check-at FUTURE_UTC --git
```

For a verification task, update its parent with `--recheck CHECK_JOB`, then finish the check. Requirements remain on the parent and its deduplicated verification task; elapsed time never supplies the missing capability or approval. Future due dates do not stop requirements being propagated to an already-open check.

A worker records its actually demonstrated input tools on the host:

```
python3 scripts/chief_relay.py capabilities --agent AGENT --available audio_input \
  --evidence 'Actual observed input-tool probe/result reference' --minutes 30
```

Use `--available ''` if none are demonstrated. Reports expire within at most60 minutes; a heartbeat, player launch, ffmpeg/ASR output, model capability claim or still image is not listening/motion evidence. Worker prompts request this check once per ordinary session. Expired/missing capability evidence leaves the requirement waiting, not queued as executable, and does not mark the entire agent down. A qualified worker may perform the condition verification; only the elected Chief may perform a protected Chief task. Capability reporting never elects a different Chief or grants stage PASS.

The local `~/_desk/state/chief/capabilities.json` is an execution eligibility cache, not another production-state database. Job requirements, holds, ownership, approvals and progress stay in canonical `jobs/queue.json`. The board uses the same selector and invalidates its quick cache when capability reports change or expire.

## Rollout and limits

Merge through the normal exact-head checks. The existing runtime fingerprint includes the modified relay/workflow/jobs code and forces restart only at a safe boundary. On Mini, verify loaded and desired versions match, one actual claim follows a prior terminal/released job without a launchd gap, and unavailable media reviews remain waiting while useful work runs. Retype only explicitly evidenced listening holds (J1752/J1753); preserve their technical progress, complete hold history and all approvals. Do not broadly convert external-input, date, Ben, credits or publication-approval holds.

The single Mini execution lane remains. J1843 separately owns measured parallel capacity and portable MacBook overflow; its host/asset/identity guards must not be bypassed by relabeling Mini-only work. This repair does not invent audio-input support. When no qualified reviewer exists, report that concrete capability shortage instead of repeatedly dispatching the same impossible review.
