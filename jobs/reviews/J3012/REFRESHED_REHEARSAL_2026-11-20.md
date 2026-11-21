# J3012: complete-source rehearsal, 20 November

Continues PR 1011 from `6fc69f748e`; current main merged at `ea19ec6fff` and source-completeness guard at `46aa863bf9`. Preserve progress 3/4. No live migration.

## Sparse-source failure and fix

The reused isolated worktree was sparse. Git listed files absent on disk; the split copy helper silently omitted them. Initial split at `ea19ec6fff` reported nine failing test modules. A targeted diagnostic ran 183 tests with three failures, 19 errors and one skip, including missing core lock, gates, voice tools and agent settings. This was an incomplete source export, not nine newly diagnosed runtime defects.

Materialized the isolated worktree with `git sparse-checkout disable`. Added a preflight to `studio_split.check`: any tracked source path absent as both file and symlink refuses before scans or export construction. A regression proves no scan, build or output directory creation occurs. The shared worker checkout was not changed.

Validation: 25 split tests, 13 channel-ratchet tests, eight address-ratchet tests and five private-network tests pass. Changed code has zero credential/address findings; diff whitespace check passes.

## Complete export

Full split at source `46aa863bf9` returned exit 0, `left: 0`, all eight groups zero and `tests: run`. Layout counts: 2,395 studio, 12,894 Orbit, 61 HOS and one Field Order routed files, plus one generated file. Source internal scratch was used because MiniWork had about 310 MB free; no scratch offload or NAS modification occurred.

The result records `clean: false` because the runbook was edited after export construction while tests ran. Independently compared all 2,394 routed engine files other than the deliberately rewritten registry against Git blobs at `46aa863bf9`: zero missing and zero differences. This comparison establishes exact engine snapshot provenance. Local logs and source comparison are under `/private/tmp/j3012-0820-logs`; the failed initial export/logs are under `/private/tmp/j3012-0815-layout` and `/private/tmp/j3012-0815-logs`.

The official daily history now records seven consecutive clean days, 14–20 November; the latest row is source `9f583d0a2b` at 07:54 UTC. This continuation did not alter that history. A passing daily history is separate from this unmerged branch's rehearsal and does not satisfy deployed acceptance or the preceding-day notice.

## Future-identity suite

Changed only the isolated registry to `TheLaughingGod1986/studio`, no home channel, explicit separate engine and channel paths; linked the existing ignored Content Ops dependencies. Full Python discovery completed with exit 0: **1,482 tests in 154.402 seconds, six skips**. The skips are not claimed as passed; this includes local mocked integrations, not deployed credential or live-service acceptance. The earlier baseline pass did not have those Node dependencies linked.

## Published private snapshot

Published [rehearsal/j3012-20261120](https://github.com/TheLaughingGod1986/studio/tree/rehearsal/j3012-20261120) at `a5759dc95f0bf8c02f9bd6050defb6c5bb5a41d9`. Remote read-back confirms zero parents, 2,397 tracked files and no active workflow YAML. The original `rehearsal/j3012` branch and default branch remain unchanged; no production `main` was created.

The scan covers every staged file: zero credentials, addresses, video/audio, active workflows or symlinks. Exact source-tracked images excluded by inherited ignore patterns were restored to the index. Workflow bytes are retained under `docs/rehearsal-workflows`; this does not prove hosted CI. `docs/REHEARSAL_SOURCE.json` records the source SHA and queue hash. Exported queue bytes exactly match the frozen source; this is a rehearsal snapshot, never the live authority. The remote retains only a new root commit, no Orbit history.

The temporary board access probe still reads the existing `rehearsal/j3012` branch intentionally; that remains a valid private Contents-access target. Its eventual access result is not evidence that this newer snapshot has been deployed.

## Remaining live gates

Exact deployed board credential Contents access; safe propagation of the merged HOS guards after writer drain; remaining local wrappers and both MacBook slot inventory; preceding-day notice; then actual relay, board publish, tick and both-worker acceptance. No marker, service, deployment, credential, media, public state or spend changed. Do not mark J3012 complete before live acceptance.
