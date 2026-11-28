# J3012: additional record writers and Mini service inventory

20 November 2026. Continues PR 1011 from 48da2447da. Progress remains 3/4; no live move.

## Change and validation

- Added retirement refusal to `thumb_ledger.main` and `thumb_ledger.save`, and to `launch_check.main` and
  `launch_check.save_record`. Direct imports and commands without Git can no longer bypass the guard.
- Regression checks prove refusal preserves an existing thumbnail ledger byte for byte and never resolves a
  launch record target. Unarmed imported saves still create the expected records in temporary directories.
- 84 guard and launch-check tests pass. Another 26 channel-ratchet, address and private-network tests pass.
  `git diff --check` passes. No full split rerun is claimed for these two additional guards.
- Read installed Mini plist labels/command targets without printing environment values. The Grok watchdog
  references the former engine and has no marker/pause check. The Cursor target remains unresolved by this
  limited static inspection. Browser services and HOS-local desk/reminder need the retain/adapt audit described
  in the runbook; MacBook service inspection is not complete.

## Workspace and limits

A full worktree attempt exhausted external scratch capacity and Git did not retain its registration. Work
continued in a sparse clean worktree on internal disk (`/private/tmp/j3012-0620`), which had about 31 GiB free.
No NAS file, source film, installed service, marker, credential or live queue behavior was changed. No spend.
The assigned queue record was claimed and progressed through the normal metadata command only.

## Resume

Continue PR 1011 at its new head, preserving 3/4. Remaining: deployed board credential Contents probe; local
watchdog/worker and other exporter guards; both-machine service inventory; refreshed private rehearsal. The
inspected official history has six full zero days through 19 November; no official row was added by this run.
Seven daily passes, a preceding-day notice, and live relay/board/tick/both-worker acceptance remain mandatory.
Do not recreate the runbook or mark the migration done.
