# J3012 loaded-service inventory

20 November 2026, approximately 08:44 UTC. Existing PR 1011 and progress 3/4 retained.

The read-only service inventory now has an optional loaded-state probe. It validates labels,
uses only the current user's GUI domain and the absolute launchctl binary, applies a five-second
timeout, and suppresses the raw output and errors. Only the exact missing-service diagnostic
counts as not loaded. Unrecognized state text is reported as unknown. Missing GUI domains,
permission errors and timeouts remain unavailable. This does not run discovered wrappers,
start/stop services, change a marker or read credentials from their source files.

## Mini observation

18 installed definitions were inspected: 17 parsed, one malformed. All 18 loaded-state reads
resolved: 17 loaded, one not loaded. Seven loaded jobs reported running, ten not running.
The overall inventory returned 1 because the installed missed-runs plist is malformed; this
was not reported as a clean readiness pass.

- `com.owb.missed-runs`: installed XML unreadable, but loaded and not running at the read.
- `com.owb.cursor-worker` and `com.owb.grokbot-watchdog`: loaded, not running at the read.
- `com.owb.chief-relay`, `com.owb.board-publish`, `com.hos.desk`, and the separate Mini worker:
  loaded and running. Their active work was left alone.
- `com.cursor.mac-mini-repo-workers`: explicit not-loaded response.

Loaded state does not compare launchd's retained definition with the installed file, count
child processes, prove pause handling, or prove the worker has no pending schedule. Preserve
and reconcile both definitions at the drained cutover. Unrelated workers are not migration targets.

## MacBook observation

The existing connection inventory showed the MacBook online. A non-interactive SSH probe
with strict existing host-key checking and an eight-second connection bound was refused.
The first sandboxed attempt did not establish access; the authorized unsandboxed read-only
probe confirmed connection refusal. No remote command ran. No device address, network name,
credentials or raw diagnostic was printed or recorded. Remote installed/loaded state remains
unverified; obtain the sanitized inventory through an existing MacBook worker session.
Do not enable remote login or alter network/authentication settings as a shortcut.

## Validation

Twelve inventory tests pass: the original seven non-execution and disclosure checks, plus five
loaded-state tests covering exact argv/domain, top-level state parsing, environment suppression,
explicit missing-service matching, unknown state suppression, invalid labels, non-macOS refusal,
timeouts and launch errors. Live read confirms the malformed installed/loaded distinction.

## Remaining work

The prior production-probe deployment rejection remains unresolved and was not retried. It is
not a failed Contents-access check. Complete that approved probe, safe HOS guard propagation,
MacBook installed/loaded inventory and wrapper readiness before the preceding-day notice.
Then refresh the frozen export and perform the runbook's live relay, publication, tick and
both-slot acceptance. J3012 is not complete. No services, board deployment, films, credentials,
active-engine marker or spend changed in this continuation.
