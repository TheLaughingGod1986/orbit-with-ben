# J2640: relay metadata transaction rollback

Cause: the metadata transaction captured a base before another writer moved shared main, then rejected its own commit against that stale base without rolling it back; refill returned exit zero on the error, hiding it from the relay log.

## Evidence and limits

The retained relay log does not contain the exact error emitted by either refill invocation. `refill.run` printed transaction errors to stderr but returned an empty list; its CLI returned zero, and `chief_relay.keep_busy` only logged stderr on a nonzero exit. There is therefore no support for inventing a remote push rejection message. The reconstructed verification error is `metadata commit verification failed; not pushed, changes preserved`; it occurs before `git push` is called.

At 18:01:01Z the shared main reflog records the watchdog's `pull --ff-only -q origin main` fast-forward to ebf5480fbd. At 18:01:04Z refill committed b74cb5fcd4 with that parent. The watchdog log confirms its 18:01:01 run. This supports the lead's stale-parent race. Returning from a side branch was context, rather than a sufficient cause: metadata requires main, and the recorded parent is published main.

At 07:05:17Z the main reflog records the Buffer check commit d7821943b2, followed by refill's 1185238a0b at 07:05:40Z with d7821943b2 as parent. The watchdog ran at 07:01:01 and 07:16:01, so it was not the same watchdog pair. A stale captured base or shared FETCH_HEAD race with the other active writers is consistent with this history, but cannot be proved uniquely without the discarded stderr/base value. A separate pull updated remote refs at 07:05:42. Both rescue commits change only queue metadata. Rescue branches and stashes were only inspected, never changed.

## Change

- Fetch main into its named remote-tracking ref without relying on shared FETCH_HEAD; capture and verify the actual published parent after fast-forward.
- If another pull lands after that capture, retry only after rolling back the metadata-only commit to its proven published parent.
- Roll back a verified rejected-push commit on every attempt, including the final attempt; refresh main after the final rejection. Return failure to the caller.
- Refuse rollback if HEAD or the working tree changed concurrently, preserving the other writer's work for explicit reconciliation. This deliberate fail-closed case cannot promise a clean tree without destroying somebody else's work.
- Make refill CLI exit nonzero on transaction failure, allowing the relay to retain its error.

## Validation

Real local bare origin with a rejecting pre-receive hook, tested with one and three attempts: failure returned, clean index/worktree, HEAD equals origin/main, queue bytes unchanged, and the next write succeeds after removing the hook. Additional regressions cover a pull before merge, a pull after parent capture, overwritten FETCH_HEAD, remote push races, and preservation of another writer's commit.

Targeted metadata tests: 19 passed. Refill tests: 24 passed. All 65 `scripts/test_*.py` scripts exited zero, each in a fresh process against stable code; per-script results are in `TEST_RESULTS.json`. Core lock, email ratchet, private-network ratchet and `git diff --check` also pass. Integration skips remain those declared by the tests. An earlier shared-process discovery run overlapped the code edits and tripped the relay code-version refresh assertions; the stable full rerun passes.

## Handoff

Chief review and merge required. No worker PASS or final OK. No production media, YouTube, Buffer, rescue branch, stash, rule-file or HOS changes were made by this fix. Required startup HOS pull preceded receipt of the brief's leave-alone scope; no further HOS actions were taken.
