# J3012 — heartbeat and board writers refuse retired engines

20 November 2026; continues PR 1011 from fd135f13d6. Preserve progress 3/4.

Added retirement checks to Claude heartbeat publication, board-health reporting and board-note publishing.
The three command entrypoints refuse before argument parsing. Imported heartbeat push, board-health post and
notes push refuse independently, before Git object writes/network calls, or checking out an uncommitted notes
file. The health command therefore also refuses before creating or replacing local health state.

The tests exercise an actual mismatched registry/activation-marker pair for imported calls, assert no Git or
network invocation, preserve the original notes bytes, and check unchanged unarmed writer behavior with fake
transports. Existing notes tests cover transactions and recovery of concurrent edits. No marker was installed,
no heartbeat/report sent by these tests, and no installed service changed.

The first notes test run exposed a missing board fixture in the sparse worktree. Adding the tracked kanban
folder resolved it; the final focused run passed all 28 guard and notes tests. An attempted standalone
`test_board_check.py` discovery found no tests; the real board regressions are in the approved/awaits/progress/
uploaded modules and are reported separately below. Zero-test discovery is not a pass claim.

This process has no BOARD_GH_TOKEN environment binding. That observation does not inspect the deployed
Cloudflare credential or establish a missing grant. Private studio Contents access with the actual server
credential is still unverified. No credential values were read or printed; no credential change requested.

The official daily split streak read 6. No daily row was added, full split rerun claimed, preceding-day notice
sent, or cutover made. Remaining: deployed board credential probe, other exporter/wrapper coverage, MacBook
inventory, refreshed private rehearsal, then the gated relay/board/tick and both-worker live acceptance.

Validation completed: 94 tests passed across engine guards, notes, the four board regression modules, channel
ratchet, address ratchet and private-network checks. A further unarmed heartbeat/report compatibility test was
added while that run was active; the final guard-plus-notes rerun passed 28 tests (including that addition).
Changed-file credential/address scans found zero findings, and git diff --check passed.
