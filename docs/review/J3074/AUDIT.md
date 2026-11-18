# J3074 — restore Orbit records after foreign WW2 writes

18 November 2026. Records repair only; no production approval.

## Stage restoration

An absent stage means the board default, todo; it is not an approval or a claim that the shipped film was never made. Restore absence rather than invent a completed state. The status files for 001 and 002 were first created by the foreign jobs; retain their neutral identity shells with empty stages instead of deleting files. No later Orbit-owned stage writes were found on these restored keys.

| Film | Stage | Before repair | After repair | Original-state evidence |
|---|---|---|---|---|
| 001 | script | `{"state":"review"}` | absent (board: todo) | `d97a6247c8^` |
| 001 | vo | `{"state":"review","ref":"6ac5525f44"}` | absent (board: todo) | `d97a6247c8^` |
| 001 | edit | `{"state":"blocked","ref":"253aac9346"}` | absent (board: todo) | `d97a6247c8^` |
| 002 | script | `{"state":"review","ref":"https://github.com/TheLaughingGod1986/orbit-with-ben/pull/1009"}` | absent (board: todo) | `b515a6243a^` |
| 002 | vo | `{"state":"review","ref":"d37657e3f0"}` | absent (board: todo) | `b515a6243a^` |
| 002 | edit | `{"state":"doing","ref":"PR1018 checkpoint 5e034e2cb9; full edit unfinished"}` | absent (board: todo) | `b515a6243a^` |
| 003 | picture | `{"state":"review","ref":"5b00529"}` | absent (board: todo) | `ad280b2667^` |
| 005 | script | `{"state":"review","ref":"PR #1000"}` | absent (board: todo) | `4511f8301d^` |
| 006 | script | `{"state":"review"}` | absent (board: todo) | `4a121ca9ad^` |

003 script is already absent after J3013 (`4d78b30998`), matching `0e52d64724^`; unchanged. 004 script is explicitly todo with the J3000 correction reference (`36850a153f`), which correctly records no Orbit script work. It was absent before `add8dd87ef`; retain the existing truthful correction as the brief requests. Both files' other values are preserved.

002's edit claim is a foreign J2996 claim from `a807d1b95c`, removed. Its WW2-only next text was introduced by `fcc613300f`; restored to the preceding empty string. No Orbit claim or next instruction is removed. Existing 003/005 thumbnail decisions and 006 picture correction are byte-for-byte unchanged as JSON values.

## History coverage

Every path-changing commit from the first WW2 write through the branch base was compared. 001: J2991 created script; J2992 added vo; J2993 added edit and repeatedly claimed/released it, ending blocked. 002: J2994 created script; J2995 added vo; J2996 added edit, its refs, next text and repeated claims. 003: J2997 script was corrected by J3013; J2998 added picture. 004: J3000 added script and then corrected it. 005: J3001 added script. 006: J3002 added script. All restored keys were absent immediately before their first foreign write. No original stage is unproven or left unresolved. `EVIDENCE.json` records complete before/after objects and original snapshots. `HISTORY.json` records all 61 path-changing commits examined, with per-field before/after values.

Media, dates, tests and Ben approvals are untouched. The independent routing guard remains PR #1021, outside this repair.

## Validation

- `studio.py status --check`, `core_sync.py check`, `sync_rules.py --check` and `git diff --check`: pass.
- Preservation assertions: pass (unrelated stage values and metadata, including full 004, unchanged).
- Focused `test_studio`: 24 tests, pass.
- Full CI partitioned Python suite: 78 test modules, 1,464 tests run, 13 skipped. All four scripts groups and the audio group pass. Tools group 2 initially has two failures in `test_gate_upcoming`: this machine’s TMPDIR is under `/Volumes`, so missing test files are classified as inaccessible NAS rather than NO FILE/KNOWN. Rerun the entire `test_gate_upcoming` module with `TMPDIR=/private/tmp`: all 12 tests pass. No code changed to accommodate the environment. All other suite tests pass.

No unresolved repair or validation failure remains. PR delivery is for independent Chief review; no merge performed.
