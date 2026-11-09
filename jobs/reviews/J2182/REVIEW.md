# J2182 — KEEP, checker only

5 November 2026. Codex, elected acting Chief; relay authority rechecked before merge.
Reviewed exact PR513 head `17b2ac5550c76012d709f2a6c578669e24eec922` in an isolated detached worktree. Merge: `e6d133d44d2f1946367b712607c7fa130b352996`.

Both J2180 P1 findings are fixed. Every opt-in row must resolve to readable regular-file bytes before its SHA-256 reuse identity is assigned. Absent files, broken symlinks, directories and read errors fail and cannot be waived by reviewed-ok. Missing/null/nonfinite/negative/boolean/string footage offsets fail; adjacent valid footage still detects within-run replay. Legitimate stills and legacy opt-out fixtures remain supported.

The narrow exemption remains limited to one final <=1s return after the hash-linked last VO word in a contiguous 22–27s Short, with actual opening source/hash, finite bounds, matching crop/output and decoded source evidence. Source-only exit 2 is PREFLIGHT, never rendered PASS. Render correspondence samples do not establish seamless motion; polish and all other rendered checks still run. B S04/S05 and C S05 in the original fixture still fail. No body reuse override or media approval.

## Verification at exact reviewed head

- `python3 -m unittest discover -s scripts -p test_picture_qa.py -v`: 12 tests PASS.
- `python3 -m unittest discover -s scripts -p test_terminal_loop.py -v`: 12 tests PASS, including mixed missing/null/NaN/infinity/negative/boolean/string offsets, unreadable identities, valid replay, aliases, and retained fixture failures.
- Original `ed5b8002ae:jobs/reviews/J2180/reproduce.py`, run against PR513: 14 tests PASS (two independent original regressions plus the imported 12). Missing body now reports cannot verify reuse identity; missing offset reports both metadata failure and tail within-run replay.
- py_compile for checker, contract and tests: PASS; git diff --check: PASS.
- sync_rules.py --check: rules OK. core_sync.py check: core OK (56 shared files). Changed checker files are not in the shared manifest; no HOS copy needed.
- Fresh GitHub read confirmed exact head and both CI checks SUCCESS: Rules run 41966738442; Studio core run 41966738659. No required checks configured/reported. Merge used --match-head-commit.

## Reconcile the unintended main landing

PR512 implementation and CI changes landed on main through the queue helper as 03e570eec / 1708dd233 before acceptance. Presence on main was not approval. J2182 reviews that original contract together with the PR513 repair and accepts only their repaired combination. PR512 is superseded by the reviewed repair; do not merge its stale branch. The paired playbook/rule now record actual acceptance, with no retrospective media approval. No force-push or removal of history.

## HOS006 handoff

Notify J2181 producer and J2183 mapping reviewer through the HOS desk. J2183 has delivered FIX; J2184 owns the remaining source decision. J2169 remains blocked at 1/3: source/crop fixes, separate mapping acceptance, complete exact inputs and all rendered gates are still required. Checker acceptance alone cannot reopen it. Preserve all locked VO, exclusions, collision holds, conditional dates and Ben final UAT. No spend, generation, production-stage or publishing change in this review. No audio or moving-video perception claimed.

Queue-helper branch publication is a separate system risk; this session kept all queue --git calls in the main checkout and all review commits in an isolated branch. The incident must be repaired by a separately scoped system job, not silently accepted as normal queue behavior.
