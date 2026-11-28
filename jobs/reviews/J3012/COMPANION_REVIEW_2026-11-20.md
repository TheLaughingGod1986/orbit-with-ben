# J3012 companion exporter review

20 November 2026. Continues PR 1011; existing progress remains 3/4.

Reviewed the complete HOS PR 688 diff at 9c0c6b5e4805c1d5f158241047314a321e40f38b.
The author and head repository belong to the studio owner; this is not a fork.
All five applicable CI checks passed (the desk reopen step was correctly skipped).
Independently reran tests/test_studio_spend_destination.py: five tests pass, exercising all three
standalone exporters, no-marker compatibility, retired/unknown destination refusal, invalid configuration,
unchanged prior ledger/account state and idempotent receipt replay. Inspected production call sites and
confirmed destination checks precede destination mutation. No generation or live ledger write was run.

Chief status immediately before merge elected codex. Merged with the exact-head constraint, producing
f3188f03b9e5a727d5cdf57bc19da760b6746ac6 on HOS main. This approves the code patch, not live migration.

## Installation is still outstanding

The shared HOS checkout is on grok/j2271-crop-sheets with local edits. Its requested git pull succeeded
on that branch and fetched the new main, but did not install main into the shared worktree. Do not switch
or reset that worktree or overwrite another worker's edits to make installation appear complete.

A read-only comparison found all three Mini runners still lack require_active_spend_destination and differ
from the merged versions. The corresponding exact canonical NAS working paths were absent. Absence at those
three names does not prove there are no other runnable copies, wrappers or in-flight imported programs.

Before activation, drain affected writers, locate the copies selected by current launchers/jobs, preserve any
local changes, and install the reviewed patch without replacing unrelated changes. Verify those copies against
the merged code and rerun the boundary tests. A fresh worktree alone would not protect existing launch paths.
Do not arm the active-studio marker while retained runnable copies remain unguarded.

The official split streak still reads six. No official daily row, service, activation marker, browser, film,
credential or ledger changed. The board server credential probe, remaining wrapper review, MacBook inventory,
refreshed private rehearsal, seven clean days, preceding-day notice and live acceptance remain.
