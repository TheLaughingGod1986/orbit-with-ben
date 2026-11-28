# J3965 — channel Shorts band and terminal pre-roll

Implements the J3874 Chief ruling for HOS 009. This is checker work, not approval of a Short.

- `terminal_loop.validate` reads this checkout’s `gate_shorts_open.py DUR_BAND`; no copied duration limits. Current channel band accepts 16–19 seconds inclusively and rejects 15/20 seconds.
- A validated return is exactly one final `prescribed_terminal_loop` row, at most one second, after the locked VO, using the opening’s actual source and matching crop/output. Its source window is non-overlapping native pre-roll ending at the opening offset. Opening and tail rendered samples are checked against their respective source windows.
- SAME_STRETCH exemption applies only against the opening. A return close to another body occurrence still fails. Overlap, undeclared/multiple roles, body repeats, within-run replay, source identity/hash, picture-kind, upscale and pixel checks remain enforced. A fractional 17.1-second recipe covers floating-point join arithmetic.
- Source-only checks remain PREFLIGHT; no claim to perceive motion or hear audio is made.

## Core sync

Changed in the isolated canonical OWB worktree, ran `core_sync.py lock` and `push` to the isolated HOS checkout. HOS main lacked the picture/terminal checkers, so their existing polish runtime and two historical test fixtures were included and locked as core too. The new core files match byte-for-byte, and each checkout passes its own core lock check.

The full push also exposed two pre-existing HOS upload-file differences (`youtube-package-upload.ts`, `publishing/youtube-package.ts`). Those files and their previous HOS lock entries were preserved: this gate repair must not change HOS upload routing. `core_sync.py diff` therefore still names exactly those two pre-existing differences.

## Validation

Temporary HOME used for all suite runs. Final gate tests: 27/27 pass in OWB and HOS (15 terminal-loop, 12 picture checks). OWB tools: 96 pass with TMPDIR=/private/tmp; audio: 21 tests, one skip. HOS scripts: 65 pass; HOS tools: 94 pass. Remaining suite results are recorded in the PR/session handoff.

Initial tools run using MiniWork TMPDIR had two path-policy failures; repeating the complete tools suite with /private/tmp passed. No production files or gates were changed to suppress these failures.

## Handoff

Both PRs must merge before reopening J3871. Its owner then re-runs the exact unchanged v04 through the gates and supplies a truthful contract/evidence record. No media edits, spend, UAT approval, upload or scheduling are part of J3965.
