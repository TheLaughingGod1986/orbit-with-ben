# J3012 — detached Buffer timer, 19 November 2026

Continued existing PR #1011 from `19a110d1dd1e53f66b906b3962bcc61d5ae88902` in a clean isolated worktree.
The plan remains at step 3 of 4. No live engine, service, posting record or credential was changed.

## Delivered

- The Buffer timer selects studio code independently of its existing record checkout. Its local `record-root`
  probe uses the CLI's validated record resolver. Both channels' checks execute from the engine; Git add,
  commit and push target the record checkout, preserving the original main-only policy.
- Credentials stay in the existing ignored content environment by default, with an absolute local override.
  Missing roots or credential files stop before API work. Existing operation-lock collision handling remains.
- Direct Buffer CLI calls obey the repository identity marker before taking their operation lock. The root
  probe is read-only and does not take a lock. A missing/retired guard refuses the command.
- The Mini renderer can prepare the Buffer LaunchAgent without installing it or changing its schedule.

## Verification

- **37 Python tests pass**: timer layout, retired identity, Mini plist renderer, channel ratchet and private
  network checks. The first command omitted the scripts import path; the corrected command used
  `PYTHONPATH=scripts` and exited 0.
- **Eight desk-lock pretests pass**, including actual Node/tsx root resolution from an independently copied
  engine fixture, rejection without its channel variable, no record folder/lock created in the engine, and
  direct CLI rejection under a retired identity. Fixture files contain no credentials or real network writes.
- **217 application tests pass** across 21 files; TypeScript typecheck and ESLint pass.
- Existing lock fixtures now include the actual guard, an initial Git commit, an explicit engine selection and
  a read-only root response. They retain real operation-lock and repeated-collision assertions. The initial
  run exposed these fixture gaps; they were fixed, not skipped.
- Core lock check passes (56 files). Shell syntax and whitespace checks pass.

These are local checks, not a complete refreshed split, hosted Actions or live timer acceptance.

## Next resume

Finish analytics' detached per-channel snapshot/report/gate/commit roots; do not enable that legacy wrapper
in studio merely because its retirement guard passes. Inventory all installed writers and cover the remaining
Node entrypoints. Verify private Contents access with the deployed board credential, then refresh the private
rehearsal export and scans. Keep the current queue as the source; never restore a rehearsal queue over it.

The official 19 November split failure still means no seven-day streak is established. No history row was
changed here. Actual seven clean daily results and the preceding-day notice remain mandatory before the live
relay, board publication, tick and two-worker acceptance. No Ben-only action is established by this change.
