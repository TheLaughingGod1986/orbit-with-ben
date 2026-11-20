# J3012 — standalone spend exporters

20 November 2026. Continues existing OWB PR 1011 at af5250ed94; progress stays 3/4.

Inventory found three direct SharedFlowAccounting.export_ai_spend implementations in HOS films 009, 010 and 013.
They bypass ai_spend.append and still selected the Orbit ledger in canonical_spend_ledger. The engine guard alone
therefore does not protect these destinations after the move.

Companion patch: https://github.com/TheLaughingGod1986/history-of-science/pull/688
Commit: 9c0c6b5e (isolated HOS worktree based on 90bea410).

The standalone runners now read the same local active-studio marker. With no marker, the existing path and offline
fixture destinations are unchanged. With a marker, production selects STUDIO_REPO or the new studio checkout,
requires an absolute root, and validates its registry identity. Every direct export validates the resolved ledger
path and destination registry before creating directories, taking the destination lock or appending receipts.
Symlink aliases to the retired root are refused. Malformed or unreadable configuration fails closed without
printing its contents. Confirmed charges and reserved liability stay in the account store for replay.

The small guard is deliberately repeated in these self-contained runners so retained NAS copies do not import
code from an assumed engine checkout. A test enforces identical ASTs across all three. This is not an inventory
of every historical script: use the installed-service/active-process inventory to identify copies that can run.

Validation:
- 29 focused migration, shared-accounting, replay and private-network tests pass. The new boundary suite executes
  each exporter with a real temporary marker and registry; stale ledger bytes and absent destination locks are
  checked, and valid receipts replay exactly once without changing liability.
- Broad suites: 167 tests, 3 failures and 12 errors. Restoring the three source files to the unmodified base and
  running the same existing suites gives 157 tests, the identical 3 failures and 12 errors. No new failing test
  cases. Missing style/reference fixtures and existing runner expectations remain; this is not a full-suite PASS.
- Whitespace and changed-file credential scans pass. No browser, generation, real account ledger or API was used.

Before cutover: review/merge HOS PR 688, refresh the actual HOS checkout and any retained runnable copies, and
verify the active destination on the Mini. Do not change an in-flight runner; drain first, as required by the
runbook. Do not arm the marker while a retained runnable copy lacks the guard. The marker is an identity check,
not an interprocess lock or a substitute for draining generation and accounting writers.

This continuation changes no live service, marker, official daily record, channel stage or film. No spend.
Still required: actual deployed board-token Contents probe, external wrappers, MacBook inventory, refreshed private
rehearsal, seven official clean days, preceding-day notice and live relay/board/tick/both-worker acceptance.
The current official history inspected still ends with six zero days through 19 November.
