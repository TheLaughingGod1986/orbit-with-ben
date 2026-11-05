# J2180 — FIX, PR512 must not merge

Reviewed 5 November 2026 by Codex, elected acting Chief (relay status rechecked). Exact head: `be2c980ffaad0626266cd9010c89f540dfb1c6a4` (includes CI change after original handoff `203763e323`). PR: https://github.com/TheLaughingGod1986/orbit-with-ben/pull/512

## Blocking findings

1. **P1 — Missing body source gets an unverified unique identity.** In `scripts/picture_qa.py:156`, `p.is_file() == False` falls back to the resolved pathname without an error. A missing body file or broken symlink therefore cannot be hashed but is treated as distinct footage. The opt-in path returns source_preflight and no row failures for a missing body source. This does not prove body reuse checks ran against honest source identities. Fix: in opt-in mode require every source to resolve to readable file bytes before assigning its content identity; record a non-waivable row failure for absent, broken-link, directory or unreadable sources. Do not silently use a path as verified identity. Keep legacy opt-out behavior separately unchanged. Update synthetic fixtures to provide actual distinct body files.

2. **P1 — Missing video offset disables replay checks for adjacent footage.** `reuse_checks` at `scripts/picture_qa.py:111` chooses still handling for an entire run whenever any member has no offset. The new terminal contract validates only first/tail framing. A video body row on the opening source with its offset omitted makes the whole opening/body/tail run skip source-interval and within-run replay checks: no failures, still source_preflight. Fix: validate finite nonnegative offsets for every explicit footage row in opt-in mode, before run classification; incomplete video metadata must fail closed and cannot downgrade neighboring video rows to stills. Preserve legitimate still handling and default legacy behavior. Add mixed adjacent-run regressions (missing/null offset plus NaN/invalid offsets) and a valid same-source run that still catches within-run replay.

These are failures of the proposed fail-closed contract, not permission to waive pre-existing reuse rules. Both are reproduced using synthetic bytes only in `reproduce.py`; run against the reviewed PR checkout. `REPRO.txt` preserves the actual failing assertions (the imported original nine tests also ran and passed).

## Verification and accepted portions

- Existing 12 picture-QA tests and 9 terminal-loop tests pass independently. PR Rules and Studio core CI checks were green at inspected head.
- Two independent review assertions fail as described above: each returns `source_preflight` with `[[], [], []]` row failures.
- `sync_rules.py --check`: rules OK. `core_sync.py check`: core OK, 56 files. Neither changed checker file is listed in the core manifest; no HOS core copy is required.
- Positive contract coverage includes exact final-row role, duration, source/hash/crop identity, finite opening/tail interval, VO alignment hash, <=1s post-VO return, provisional source-only exit 2, rendered sample correspondence and retained J2169 body failures.
- Proposed playbook and Cursor rule are paired and clearly remain proposals. No rule is approved by this FIX.
- No actual production audio/motion reviewed; tests verify code and synthetic sample correspondence only. No credit, generation, render job, publishing or production-stage changes.

## Required handoff

Return J2179 for the exact corrections and regression tests above, using the existing PR512. A separate elected-Chief re-review of the corrected head must precede any merge or HOS006 use. No merge SHA exists: PR512 remains open and unmerged. J2181 can continue its independent existing-media mapping work; its subsequent mapping reviewer must also check the successful system re-review before reopening J2169. J2169 stays blocked at 1/3; checker acceptance alone never approves body mappings or rendered gates. No action required from Ben.
