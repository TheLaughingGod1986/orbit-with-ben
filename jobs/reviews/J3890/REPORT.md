# J3890 — MacBook readiness reconciliation

27 November 2026, agent `macbook-2`. Investigation and preparation only. J3012 remains 3/4; this child does not authorize or perform a live switch.

## The early heartbeat is real; attribution to J3885 is contradicted

Read the exact private Studio Git commit `08715bd2077bf69c1fc40bc0a532c70ae912806c` through the existing GitHub API access. Its commit time and heartbeat time are 10:22:56Z. The document says slot 2, agent macbook-2, state error, empty job; the reason is that the slot-2 Studio checkout was on `rehearsal/j3012`, not main. Raw heartbeat observation/environment data were not published.

The retained local worker log and clone reflogs establish a different sequence:

| UTC | Local evidence |
|---|---|
| 10:22:45 / 10:22:46 | Ordinary old-engine slot logs report no MacBook job waiting. |
| 10:48:45 | Installed worker wakes the J3885 agent. |
| 10:49:52 / 10:49:55 | Slot 1 / slot 2 Studio clones are first created, from `rehearsal/j3012-20261127`. |
| 10:50:41 | Two test attempts to start slot 2 fail opening its real log: Operation not permitted. |
| About 10:50:50 | The 104-test suite completes successfully. |
| 10:51:23 | Both staged clones acquire local main branches at the same rehearsal commit. |
| 10:53:31 | J3885 finishes. |

Therefore J3885's local suite cannot have emitted the 10:22:56Z heartbeat. Its two attempted child launches were blocked before Popen. The earlier heartbeat also names a different rehearsal branch. No retained local evidence establishes its originating process or machine. The heartbeat's `host` field is hardcoded to `macbook` by `heartbeat_doc`, so that field alone cannot establish which machine ran it. Chief should inspect the private rehearsal-test logs/process timing from the earlier preparation run, including any other Darwin host, before attributing it.

There is nevertheless a real unsafe test boundary: in this exact source, `AllAgents.test_run_keeps_taking_jobs_until_idle` and `AllAgents.test_run_stops_at_its_loop_budget` call `run()` with fake STATE/run_one but without mocking `start_other_slots`. `run()` calls that function before acquiring its run lock; on Darwin, slot 1 can spawn a real child using the actual HOME, registry and environment. The brief's `RunLock` class name is absent in these staged files. A separate OnePublisher test does mock the function. Do not rerun the affected suite against live roots. Before any future run, isolate subprocess dispatch and HOME/log/registry roots; mock start_other_slots in every run-level test. This job changes no test code or staged clone.

## Runtime and staged queue evidence

Sanitized read-only inspection at 11:36–11:38Z is recorded in EVIDENCE.json. Both staged heads remain exact parentless rehearsal `eda81876dc28c11b6a0d7b6cb0281b801bfd00c9`, clean on local main. Both queue files hash to `f208a2a70a621be277aa81ede0a2406bec72ffac673bb986f6aa735aa335c969`, exactly the original rehearsal blob; path-limited all-ref history contains only that root commit. No staged queue mutation is present in the working trees or retained reachable history. This cannot prove absence of an unretained historical write, but the inspected error path returns before guards/queue selection, with an empty job.

A full process-table read found one worker-script invocation, using the retained old Orbit engine, started 11:34:19Z; zero staged-engine worker invocations. Slot 1's existing lock was not held; slot 2's was held. The authoritative queue includes this claimed J3890 under macbook-2, and parent J3012 under Codex. The service itself was loaded but `not running`: a launchd state alone does not prove its detached slot child has drained. No new long-lived process was started by this investigation. This is a point-in-time process observation, not future inactivity proof.

All six channel clones were clean on main at inspection. Slot 1 retains `~/_desk/worker/{orbit-with-ben,history-of-science,ww2-channel}` and slot 2 retains the independent equivalents under `~/_desk/worker/slot2/`. The two engine roots remain `~/_desk/worker/studio` and `~/_desk/worker/slot2/studio`. Old Orbit source heads have advanced since J3885 through normal queue/repository updates; exact observed heads are in the JSON. Worker bytes have not changed.

## Installed, loaded and proposal settings

The installed plist is byte-identical to J3885's private backup, SHA-256 `804d9c80529c3502ececc36d1f01d27c19fff141edc6a722b80157bd581ff071`. Loaded argument and environment sections match the saved loaded definition; loaded arguments also match installed argv and all explicit installed environment entries match. The only additional loaded environment names are launchd bookkeeping (`OSLogRateLimit`, `XPC_SERVICE_NAME`). No MACBOOK policy override names occur in the loaded environment.

The proposal is unchanged, SHA-256 `901afa6a8d9665e4346b0edc5854b2f93811606d2c8744da31b21c15a7d42856`. All non-bootstrap service properties and installed environment values are preserved. Its only extra environment names are STUDIO_REPO and STUDIO_GIT_URL; the bootstrap targets the future engine rather than Orbit. The exact private files remain in `~/_desk/state/j3885-preparation/`: installed.plist, installed-bootstrap.zsh, loaded-private.txt, old-worker.py, future-renderer.py and proposed.plist. Do not commit them. The new private loaded snapshot is in `~/_desk/state/j3890-inspection/loaded-private.txt`.

Old and staged worker source SHA-256 in both slots is `1a436cb09d8fe20aac4b62d2a57777ee22afd2bd76f39b8e3370dcb00264511b`. All four engine-guard sources hash to `89aab43e68b1c5dc0803a3b0eae30abd69d79240b26e7e909c598b331fe14274`. Retirement enforcement precedes CLI parsing; the worker pause check exists. With no active marker, guards do not prohibit the rehearsal from launching: clean local main is staging convenience, not activation permission. The launcher must continue using old Orbit until coordinated cutover.

Policy stays mains-only, two slots, default round-the-clock, slot 1 background work allowed during user activity, slot 2 ten-minute idle requirement, existing tool routing, 15 GB free-space floor and 1500-second job cap. No pause or activation marker exists. No installer, setup script, service restart, bootout, default-branch change, rehearsal queue command or writer was run. No credential, film, board or spend changed.

## Concrete handoff through the installed worker

1. Chief reviews this PR and the timing discrepancy, fixes test isolation before further rehearsal suites, and resolves the remaining J3012 global prerequisites. Preserve the heartbeat commit and private logs. Do not reset either clone or use the stale rehearsal queue as production.
2. Chief queues a new coordination child through the existing authoritative Orbit queue, `needs macbook`, with no dependency on J3012 completion. The installed old worker receives it normally. The brief explicitly authorizes the coordinated window and identifies a separately supervised installer handoff; this investigation grants no installation authority.
3. That coordination child saves fresh installed/loaded hashes and both slot claims, coordinates with Chief's other-machine writer drain, and sets the existing worker pause only once authorized. An already running child is not stopped by that pause. Let every active job finish or release cleanly; preserve locks. The coordination job records its ready handoff, publishes its result through the old queue, returns all touched checkouts to main, and exits. Its owning worker must also exit and release its lock before service replacement.
4. The installer must be outside the service/slot process group that will be booted out. Prepare and review that one-shot handoff during the authorized coordination child; it must wait for that job's terminal state, the actual owner PID/process-group exit, both unheld worker locks and no remaining claims/agent children. Any failed condition stops the handoff. Do not have the coordination child synchronously boot out its own ancestor, and do not treat a terminal queue row or launchd `not running` alone as drain evidence. No such helper was created or launched here.
5. Only after Chief confirms the global freeze/export: refresh both engine clones from the exact production source and fresh authoritative queue, revalidate hashes, regenerate/review the proposal against actual installed settings, then perform the service replacement from that external handoff. Preserve all power/idle/tool settings. Do not run setup_macbook.sh, which also changes unrelated setup. Keep private rollback originals and loaded state.
6. With slots paused, verify installed and loaded roots, guard refusal from old engines and checks from both new slot contexts. Resume in the runbook's order; prove one controlled task per slot uses its own engine/content roots, lock and heartbeat, then verify relay/board/tick and rollback evidence. J3012 stays 3/4 until its own acceptance is complete.

This is a reviewable handoff design, not an installed unattended coordinator. The unresolved historical heartbeat origin and the need to implement/review that external installer handoff are explicit remaining work for Chief. No Ben action is required.

Validation for this evidence-only change: proposal `plutil -lint` and `git diff --check` passed; 8 email-ratchet and 5 private-network tests passed. The unsafe worker suite was not rerun.
