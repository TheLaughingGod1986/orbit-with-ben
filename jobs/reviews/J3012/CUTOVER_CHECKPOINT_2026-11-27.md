# J3012 cutover checkpoint — 27 November 2026

Codex, elected acting Chief at the session status check. Progress stays 3/4. No live cutover or spend.

## Verified prerequisites

- Token grant: prior successful production verification in #7159250002 (25 November); not re-probed.
- Preceding-day notice: #7186248983 (26 November), for 27 November from 10:00 London.
- Official split streak: 14 consecutive zero-result days. The new checks do not modify that history.
- Private Studio remote still has the two rehearsal branches and no production main.
- No active-studio marker on the Mini. Orbit remains the authoritative engine.

## Current preparation

Clean isolated source: `5afd1f712135a9463b873b09330de68842d9dc3f`.
Worktree: `/Volumes/MiniWork/scratch/J3012-cutover-1127`, branch `codex/j3012-cutover-1127`.
This source is a rehearsal snapshot, not a frozen production queue. Other workers were active.

- Required scratch offload ran detached and exited 0: no eligible files; internal free space remained about
  13 GB. MiniWork had about 140 GB free and holds this work. No files moved or deleted.
- Saved 17 original installed service definitions privately, mode 0600, under
  `/Volumes/MiniWork/scratch/J3012-service-backups-1127/`, with source hashes. These contain local configuration
  and must never be committed. This does not replace loaded-settings reconciliation.
- Re-read installed and loaded service state. The malformed missed-runs definition is still loaded; a parse
  failure must not be interpreted as a stopped monitor. Inventory is local at
  `/Volumes/MiniWork/scratch/J3012-services-1127.json`.
- Prepared eight supported service proposals under `/Volumes/MiniWork/scratch/J3012-proposals-1127/`.
  All eight pass `plutil -lint`. Missed-runs required stripping invalid XML comments from the in-memory proposal
  only, preserving all configured values. Analytics required the existing local credential path in its proposed
  environment; credential values were neither read nor copied. No installed source changed.
- Proposals target the isolated layout. Regenerate for the real runtime checkout after final source staging;
  do not install these scratch-path proposals.
- Prepared four adapted workflows plus their core lock under `/Volumes/MiniWork/scratch/J3012-ci-1127/`, pinned
  to the full source SHA above. Nothing installed or enabled.
- 52 focused tests pass: 16 CI/inventory tests and 36 service/guard/MacBook launcher tests. An earlier invocation
  used incorrect import paths and produced two loader errors; the corrected `PYTHONPATH=scripts` invocations
  are the results counted here.

## Detached checks — inspect before resuming

1. `tmux` session `J3012-split` runs the complete split against the clean source, keeping
   `/Volumes/MiniWork/scratch/J3012-layout-1127/`.
   Log: `~/_desk/logs/J3012-split-1127.log`; exit: `~/_desk/logs/J3012-split-1127.done`;
   result: `/Volumes/MiniWork/scratch/J3012-split-1127.json`.
2. `tmux` session `J3012-future` waits for baseline exit 0, then changes only the isolated engine identity to
   private Studio, applies the staged CI files, supplies independent sibling channel paths, links existing
   ignored Node dependencies, and runs core/rule checks plus full Python discovery. It does not start services.
   Runner: `/Volumes/MiniWork/scratch/J3012-future-identity-1127.py`.
   Log/exit: `~/_desk/logs/J3012-future-1127.log` and `.done`; individual logs end in `-0.log`, `-1.log`, `-2.log`;
   result: `/Volumes/MiniWork/scratch/J3012-future-1127.json`.

Results were pending when this checkpoint was written. Missing `.done` means still running; do not duplicate.
A nonzero baseline prevents the second phase. Inspect named failures, not merely the count. The helper retains
all logs and never publishes its rehearsal queue. No successful full-suite result is claimed here.

## Next action

Finish the detached verification, then follow the runbook's coordinated drain/freeze/switch/acceptance sequence
on both machines. No pause file has been created, so live work continues normally. Re-read Chief status before
protected decisions. Final cutover must export fresh source and queue after draining, preserve the retained
stores first, prove relay/board/tick/both-slot operation, then implement the separately ordered private store
and thread move and test all three channels. Keep J3012 open until that evidence exists. Nothing requires Ben now.
