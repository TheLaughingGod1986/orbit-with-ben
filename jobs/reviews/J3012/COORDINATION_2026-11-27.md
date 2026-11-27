# J3012 coordination checkpoint — 27 November 2026

Codex, elected acting Chief. Parent remains 3/4. This checkpoint resolves the early rehearsal heartbeat and reviews the MacBook readiness evidence; live migration acceptance is still outstanding.

## Reviewed readiness

Reviewed the complete two-file diff of PR #1379 at `43145157be08387815ac6327c24333930f928027`: machine-local observations, sanitized hashes and explicit limits. Its author is the owner and its base is main. No CI checks were reported for this evidence-only branch. Checked the exact files locally: eight email-ratchet and five private-network tests passed, and diff whitespace check passed. Re-read Chief status (Codex elected, Claude down), then merged PR #1379 as `e2c2b9b1e781ba3e84155ddd8c067a00fdf1ef39`.

Confirmed PR #1380, the two unsafe loop-test fixes, already merged as `191e362d4bffa35316e4491e11d1a1582d97e0f5`; Rules check SUCCESS, core check SKIPPED. Do not repeat the old unsafe tests or the unchanged full rehearsal suite.

## Heartbeat originated on the Mini

J3890 correctly ruled out the later MacBook preparation run. Read the Mini's retained local slot-2 worker log and clone reflog without publishing raw host/environment data:

- The detached future-identity suite ran on the Mini from about 10:17 to 10:24. Its log records the loop-budget test at 10:22:52.
- The Mini's `~/_desk/worker/slot2/studio` reflog records its clone at 10:22:55 from the private Studio repository, at original rehearsal root `534cf0f70852e06414cbe39f6a01efe9024c8a91`.
- The Mini's slot-2 log at 10:22:56 records refusal because this checkout was on `rehearsal/j3012`, not main. This matches the private error-heartbeat commit `08715bd2077bf69c1fc40bc0a532c70ae912806c` and predates creation of the actual MacBook's staged clones.
- The Mini test clone remains clean on that original rehearsal branch; queue path history contains only its root commit and its queue is unchanged against HEAD. A privileged process-table check found no surviving worker against the test export or this staged clone.

This establishes the Mini test-spawn route; the heartbeat's hardcoded host label was not machine provenance. The retained logs do not identify which of the two adjacent unsafe loop tests emitted the particular child, so no finer attribution is asserted. No production claim or queue mutation was found in that clone. The clone and heartbeat were preserved, not reset or deleted. The merged isolation fix addresses both spawn paths.

## Concrete next work

J3892 is now queued through the existing MacBook worker, with no dependency on parent completion. It implements and tests the external installer handoff from J3890: an installer outside the process group being replaced, terminal coordination job plus actual process/lock/claim drain, exact-source authorization from the elected Chief, bounded lifetime, preserved service policy, two independent slot roots, fail-closed activation and rollback evidence. The preparation job may not pause or switch live services. Its exact production commit can be authorized only after the global freeze; the existence of main is not authorization.

Review and merge that implementation, then have the installed worker stage its detached coordinator, let the owning worker exit, and coordinate the Mini/MacBook drain. Export a NEW frozen queue and run the existing cutover order. Do not rerun a stale rehearsal queue or synchronously boot out the coordinator's own ancestor. Keep one authoritative queue. Full relay, board publication, harmless tick and both-slot acceptance precede the private thread/tick-store migration and three-channel tick round trips.

The required scratch offload found no eligible old scratch; internal space remains about 13 GB and this checkpoint uses MiniWork. No service, pause file, activation marker, default branch, production engine branch, board deployment, approval store, film or spend changed. No Ben action is required. This coordinated move needs more than one bounded run; release the parent at this clean checkpoint, retaining its 3/4 plan.
