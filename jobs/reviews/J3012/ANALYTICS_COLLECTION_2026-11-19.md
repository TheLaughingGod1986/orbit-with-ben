# J3012: analytics collection and publication preparation

19 November 2026. Continues existing PR 1011 from 8fbc6cdad1. Existing plan remains 3/4.

## Delivered

Added analytics_collection.py: independent per-channel collection, required auxiliary callback, reports,
scoped publication/retry and board refresh within the existing serialized session. Record and source checkout
environments remain separate. Credential selection rejects missing/relative files and record-tree locations;
inherited analytics credentials are removed before the selected local file is loaded. Existing installed Node
dependencies are linked into the record worktree without overwriting a directory. No dependency download.

The subprocess runner suppresses raw output and returns status codes. Its deadline kills the process group,
not just a wrapper that might leave API work running. Collector/report failures accumulate without dropping
other channels' records. Publication still runs when no new file changed, preserving pending-push retries.

## Verification

- Nine new offline tests pass. A real fake-node subprocess writes separate channel snapshots and the studio
  dashboard; source channel directories stay untouched. No live API, credential or remote is used.
- A real child-process timeout test proves a delayed child cannot write after its parent times out.
- Other tests cover independent failures, queue/source/record environments, credential refusal, inherited
  credential clearing, dependency-directory refusal, repeated publication and lock release on exceptions.
- The analytics suite passed 45 tests before the final fake-executable test was added; that final collection
  suite then passed all nine tests. Channel ratchet: 13 tests pass, no ceiling increased.

These checks are not full fake-API timer acceptance: the production gate/dispatch callback and shell entrypoint
are not connected. No live services, source records or media changed, and no spend occurred.

## Next

Implement the required auxiliary phase: gate library JSON and frame destinations, source media/cache and upload
registry, bounded gate and Field Order dispatch. Wire the complete collection session into the shell timer and
prepare its plist only after isolated end-to-end acceptance. Deployed board Contents access, remaining writer
inventory and refreshed private rehearsal remain. Keep the live move gated and J3012 open.

The official history now records six full zero days through 19 November, including the corrected 21:54 UTC
result at fa47f48872. Older handoffs citing a nonzero 19 November result are superseded. Still require seven
actual daily passes, preceding-day notice and the live relay/publish/tick/both-worker acceptance sequence.
