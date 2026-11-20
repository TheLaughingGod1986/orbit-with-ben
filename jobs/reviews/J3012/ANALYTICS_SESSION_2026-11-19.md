# J3012: serialized analytics record session

19 November 2026. Continues PR 1011 from 48ee0d3952. Existing plan remains 3/4; no live move.

## Change

Added `analytics_session.py`, a context-managed preparation/publication layer over `analytics_worktree.py`.
The fixed machine lock prevents concurrent runs even when they choose different scratch folders. Preflight
checks registry identities, Git remote identities, channel manifests, staged histories, separate roots and unique
environment overrides before record worktree mutation. It checks the actual detached manifests/histories again
before yielding control. Child-process checkout overrides point at records while the shared queue remains in
the active studio checkout. Source paths stay separate, and no credentials are read by this layer.

Publication attempts every owner and returns failed owners; existing scoped Git recovery/retry remains in force.
The record helper now reads registered channels and `analytics.open_gate_library` ownership, with that setting
enabled in Orbit's channel manifest. This also fixes two pre-existing channel-ratchet findings in the helper.

## Checks

- 12 new offline session tests pass: routing, missing history before writes, wrong manifests, resident/retired
  engine, queue identity, unsafe scratch, environment aliasing, actual detached-history validation, contention and
  exception unlock, independent publication failures, registry-owned scopes and exact remote identity checks.
- The final analytics suite passes all 37 tests, including the 12 session tests, existing 13 real-local-Git
  worktree tests and 12 shell tests.
- Channel ratchet: 13 tests pass, with no ceiling increased. Registry loader: 70 tests pass. Channel schema checks: 32 tests pass.
- Address/network checks: 13 tests pass after staging; changed-file key scan and whitespace check are clean.
- These are local offline tests. Remote identity/preflight tests use mocked Git/registry boundaries; record
  recovery tests use real temporary local Git remotes. Neither constitutes full fake-API timer acceptance.

## Remaining

The session is intentionally not a runnable timer and is not installed. Connect the collector/report commands,
credential source, gate library and generated-frame destinations, timeouts and board publication inside its lock;
then exercise the complete timer using fake APIs and isolated repositories. Verify deployed board Contents
access, finish the writer inventory and refresh the private rehearsal. Seven official consecutive daily zero
results, preceding-day notice and live relay/publish/tick/both-worker acceptance remain required. The nonzero
19 November official split still resets the streak. No spend, live records, credentials or services changed.
