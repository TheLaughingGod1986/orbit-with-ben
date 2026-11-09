# J2233 — Multi-channel engine code review

Codex, 7 November 2026. Overall verdict: **FIX** before further migration. Keep the shared-engine direction and one queue. This is an advisory code review, not permission to move services or change channel rules.

Reviewed `docs/MULTI_CHANNEL_PLAN.md` at isolated baseline `266d814476`. The plan landed in #543 (`1d53625de0`), but phase-one implementation already landed in #547 (`04f33f2f7f`) and board work in #550 (`85c6b22235`). Update the plan's “nothing has moved yet” status. `capacity_caller` is retired; inventory the current runtime rather than the original estimate of 16 scripts.

## Phase verdicts and machine risks

| Phase | Verdict | Required correction and failure mode |
| --- | --- | --- |
| 1: manifests in place | **FIX** | Keep the loader and adapters. Split manifest introduction from WIP schema migration, add validation and test actual third-channel execution. Mini: wrong channel inference can route a job to the wrong rules; changing `next` from list to object breaks old readers. MacBook: it still provisions only OWB/HOS and always claims in OWB, so a generic CLI choice does not supply a third checkout. |
| 2: manifests in channel repos | **FIX** | Add an engine-owned registry and a machine/slot checkout resolver, schema/version compatibility and revision pinning. Mini: a missing checkout or manifest must stop that channel's dispatch, not silently select home; board sparse worktrees must include manifests. MacBook: resolve every channel inside that slot's private worker directory, never Ben's checkout. A relative path must resolve against its documented root, not invocation cwd. |
| 3: engine extraction | **FIX** | Specify one authoritative queue, atomic writer handoff, root separation, runtime state and rollback before moving anything. Mini: queue/stage writes, Chief heartbeat, board publisher and repair jobs currently target OWB. MacBook: both slots would otherwise continue claiming the old queue or reset the wrong repository. A forwarding executable alone does not fix Python imports, `__file__` roots, credentials or Git remotes. |
| 4: plug-in ready | **FIX** | Keep the template goal; retire shared copies only after a consumer inventory and compatibility release. `CORE_FILES.json` includes audio, Python gates, TypeScript publishing and config outside `scripts/`; those remain dependencies even if the scheduler moves. Mini/MacBook: deleting their supported source/import location breaks production tools or CI. Require an end-to-end synthetic third-channel test before claiming plug-in readiness. |

No phase is rejected in principle. The low-risk/no-machine-change claim for phase one is too broad; the currently landed compatibility mapping is safer than the proposed immediate WIP rewrite.

## Concrete dependency inventory

Paths below refer to the baseline above. These are inspected dependencies, not a claim that every installed service was exhaustively audited.

- `scripts/studio.py:27-28`: `ROOT` is derived from the script, and `FILMS` lives under it. `scripts/jobs.py:66-68` takes that same root for the queue; `READBACKS` independently uses `__file__` at line 626. Extraction must distinguish **engine code**, **authoritative queue/state**, **channel checkout**, and **local runtime state**. Queue claims and film-stage updates can no longer assume one Git commit spans both repositories; define idempotent updates and reconciliation.
- `scripts/channel_films.py:59`: home-channel data defaults to the script's parent repository. After extraction this reads the engine's nonexistent film tree. Remove “home means engine owns channel content” from the data adapter.
- `scripts/chief_relay.py:79,170`: fixed OWB engine root and HOS lookup. It reads queue/flags, runs repairs/refill, creates agent prompts and sandbox directory grants, and reads/writes heartbeat branches through OWB. Its Claude heartbeat URL at line 997 names OWB. Port all of these together, retaining Chief election and capability/lease state.
- `scripts/macbook_worker.py:54-81,458-490,519-520`: two clone URLs, two per-slot roots, fixed prompt, OWB queue cwd and flags. `scripts/macbook/setup_macbook.sh:55-57` and `scripts/macbook/com.owb.macbook-worker.plist:23` bootstrap the same pair. Preserve `own_checkout`'s protection against touching Ben's folders, two independent slot clones, heartbeat refs, mains/idle guards and capped worker lifetime.
- `scripts/board_publish.py:56-75,281-288`: two sparse worktrees, fixed section names and OWB snapshot executable with required `--hos`; board data push and checker also use OWB. `scripts/kanban_snapshot.py:820,1030,1102` has main-checkout/watch-file fallbacks and `--hos`. `scripts/video_tracker.py:279,950,1225-1226` retains two-channel branches. A third channel card unit test does not prove its real files reach the published board or its watch action resolves correctly.
- `scripts/refill.py:34,81`: centralized backlog path and default `owb`; `review_lane.py:83` and `workflow_state.py:269-272` retain `owb` defaults. Migrate legacy records explicitly and preserve backlog deduplication and stage-claim identity.
- `scripts/mini_repair.py:43-44`, `core_sync.py`, and `studio-core/CORE_FILES.json` bind maintenance/canonical ownership to existing repositories. Recovery must still work when a channel checkout is broken or missing.
- Repo launch templates `scripts/mini/com.owb.chief-relay.plist` and `com.owb.board-publish.plist` execute the OWB path. Installed Mini definitions also reference it for `com.owb.missed-runs`, `com.owb.tab-janitor`, and `com.owb.ai-spend-daily`. Inventory installed definitions as well as templates: this checkout has no top-level `launchd/` directory despite older documentation. Do not infer loaded/running status from a plist file.

## Loader and test design

Keep `channels.py`, `channel_films.py` and manifest-based routing. Fix these before broadening use:

1. **Validate the entire contract.** `_load` currently checks six field names, slug/folder equality and one home channel. It accepts an empty repo object and malformed `title_match` regex. Validate types, unique labels and slugs, regex compilation, repository/YouTube identity, supported adapter kinds, stages, WIP bounds, cadence/timezone and schema version. Separate machine paths from portable channel policy; do not put credentials in manifests.
2. **Make identity explicit.** A direct probe of `of_job({'repo':'owb','title':'HOS comparison'})` returns `hos`; the current test deliberately preserves that historical behavior. Unknown `repo='missing'` returns `missing` and only fails later in label lookup. New records should require a known explicit channel; migrate old title-based records once and flag conflicts. Do not silently change legacy semantics during a loader-only release.
3. **Define film-key grammar.** Both key regexes accept only three digits. `film_keys('OWB:J01')` returns an empty set, while the live WIP line contains `OWB:J01`. Cover compilation/alphanumeric IDs consistently across claims, deadlines, WIP and board links.
4. **Keep WIP compatibility until all consumers move.** Actual manifests retain `wip.line = next / next_hos`, and `jobs/WIP.json` still uses lists. A versioned, idempotent migration needs reader compatibility, rollback and conservation checks: no missing/duplicate active or waiting films, unchanged per-channel capacity and ordering.
5. **Test behavior, not spelling alone.** `NoNewChannelNames` checks eight files and a few regex patterns. It permits literal defaults and does not cover the worker, relay or publisher. Keep an explicit engine/adapters boundary; allow channel names in fixtures/migration adapters. A broad text ban would reject documentation while missing semantic assumptions.
6. **Exercise the real boundary.** Use three temporary channel repos plus a separate engine root, shuffled working directory, a path with spaces, two worker slots and a sparse board checkout. Test third-channel claim → progress → stage write → review → completion → board/watch identity, with network/spend/upload subprocesses mocked. Add malformed/missing/stale manifests, duplicate identities, unavailable checkout, cache reload, old/new WIP versions, held jobs, active leases, Chief handback and concurrent queue writers. The current third-channel unit test mocks `channel_films.films`, so it bypasses disk resolution.

`_load`, `key_re` and `strict_key_re` are cached: define a validated registry snapshot per run and coordinated reload/version invalidation. A daemon must not combine old regexes with a newly read registry. Pin the channel policy/flow revision in a job's execution evidence.

## Answers to the four questions

1. **One authoritative queue.** Keep global job IDs, shared agent/credit locks and deadline ordering, with per-channel WIP. An engine-only job needs explicit studio scope rather than pretending to belong to the home channel. Do not split queues during extraction. State snapshots can be backed up, but there must never be two live claim authorities.
2. **Gate cwd is the channel checkout, at the recorded revision.** Use structured argv, a fixed environment/credential profile, timeouts and an allowlisted executable/adapter; avoid arbitrary shell strings. Validate manifest paths stay inside the intended checkout. An approved repository is not proof that every future command is safe. CI lint is necessary but insufficient: protected gates/approvals belong to engine policy, channel flows can add requirements and cannot erase them. Model dependencies as a validated DAG or explicit state machine, not only an ordered list: facts, script lock, VO, review and conditional publishing have joins and holds.
3. **Prefer filtered history**, from a disposable clone with explicit included paths and a provenance map from old to new SHAs. Do not rewrite or force-push either source repository. Audit the extracted history for secrets/media before publishing even privately. Keep source PR/thread links and job IDs. A fresh import with an exact source-SHA manifest is a defensible fallback if history dependencies cannot be cleanly separated; no new repository was created here.
4. **Much more than paths.** Provision private-repo read access on both machines and cloud runners; relocate engine dependencies, import paths, queue Git remote, heartbeat refs, agent prompts/sandbox roots, local locks/leases, shared-folder paths and per-slot checkout mappings. Board deployment requires its source paths, data branch, authorization/watch store, environment and cache keys to agree. Preserve channel-specific credentials and validate destination identities without printing secrets.

## Required cutover and rollback criteria

First classify every file as engine, channel adapter, channel content or shared production library. Record source/target revision compatibility and retain current channel Never rules; don't accidentally promote an Orbit-only restriction into a studio-wide rule or weaken HOS's film-watch requirement.

Before cutover, drain active writers and detached work or let them finish on the old engine; take a queue/WIP/holds/approvals snapshot and checksum it. Disable old dispatch, switch the authoritative remote/root and compatibility shims, then start one dispatcher and the isolated MacBook slots. Demonstrate exactly one claim authority and unchanged job IDs, histories, dependencies, holds, watch decisions and credit records. Verify the board and both channels with read-only/dry-run checks before allowing production writes. Rollback must retain any post-cutover queue changes, not restore a stale snapshot and lose completed work. Retire shims by measured absence of callers and a successful rollback drill, not merely a fortnight's elapsed time.

The next owner should revise the plan and scope the phase-one validation/identity tests before phase two. This review authorizes no implementation, service cutover, deployment or publishing.

## Verification

- `python3 -m unittest discover -s scripts -p test_channels.py`: **11 tests PASS** on the isolated baseline.
- `python3 -m unittest discover -s scripts -p test_macbook_worker.py`: **37 tests PASS**; existing ResourceWarnings and sandbox-denied real log-directory probes were printed, so this is not a live MacBook validation.
- Read-only probes reproduced unknown-repo acceptance, explicit-home title override, missing compilation key, and acceptance of an invalid regex/empty repository object.
- No code, channel rules, queue schema or production service was changed for this review. Tests and source inspection do not demonstrate audio or moving-video perception.
