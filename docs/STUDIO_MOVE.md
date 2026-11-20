# Studio repository move — J3012

Prepared 18 November 2026. This is the phase 3 execution runbook, not permission to move early.
The latest J3012 brief supersedes the original history-rewrite dependency: create a clean root commit; do not
copy Orbit's Git history. J2537's history rewrite is not a prerequisite. The source history remains in Orbit.

## Resume here (20 November, probe request isolation verified)

PR 1011 is the existing delivery branch; do not recreate the runbook or reset J3012's **3/4** progress.
Its queue history and the newest `jobs/reviews/J3012/` evidence describe completed preparation.
The current integration retains main's guarded former-resident manifest cache and the PR's stronger
missing-browser-port refusal test. The split checker now rejects failed, interrupted, missing-summary and
empty test runs rather than counting an unrecognized process failure as a zero day.

The detached timer shell, bounded supervisor, cache fallback and proposed analytics plist are prepared.
The actual TypeScript collectors and report builder now pass offline CLI checks and the real timer/session/Git
record path against four temporary bare remotes. These tests also pass inside the full split export. See
`jobs/reviews/J3012/COLLECTOR_ACCEPTANCE_2026-11-20.md` for exact coverage and limits.
The installed AI-spend daily reader was found outside the prepared service list; its CLI and direct ledger writer
now refuse a retired engine, and its service can be staged with the same renderer. Nothing was installed.
The Mini inventory now resolves the legacy Cursor launcher and watchdog, and identifies a malformed missed-runs
plist. The repeatable, value-free inventory tool and cutover handling are documented below. No service was changed.
Claude heartbeat publication, board-health reports and board-note publishing now also refuse a retired engine,
including imported writer calls. See `jobs/reviews/J3012/BOARD_WRITERS_2026-11-20.md`.
The snapshot CLI and its imported watch-copy uploader now also refuse a retired engine before output or credential access. See `jobs/reviews/J3012/SNAPSHOT_EXPORTER_2026-11-20.md`.
The direct HOS Flow exporters are covered by merged HOS PR #688, commit `f3188f03b9e5a727d5cdf57bc19da760b6746ac6`.
The Mini shared checkout is on another worker branch with local edits; its three runners still lack the guards.
A successful pull on that branch does not install the main-branch patch. Preserve its edits and drain writers before
propagating reviewed code. The three canonical NAS working paths were absent, not verified safe. See
`jobs/reviews/J3012/COMPANION_REVIEW_2026-11-20.md` for the review and installation boundary.
The Cloudflare session was refreshed and the production project inspected read-only. Its GitHub token exists as
an unreadable secret; preview has no token. A disabled-by-default authenticated runtime probe is now prepared,
not deployed. Its worker route now passes the current request bindings explicitly, so removal of the enable flag, board key or GitHub token cannot reuse values retained in process.env. See **Board credential probe** below and `jobs/reviews/J3012/BOARD_ACCESS_2026-11-20.md`.
Next: propagate the merged guard patch after draining affected writers; deploy and run the prepared board credential probe; remaining wrapper replacements; MacBook inventory;
refreshed private rehearsal. Do not equate installed-service inventory with loaded-service or guard verification.
Keep the live switch gated on the timing and acceptance below. This run does not change the official daily
history or send the day-before notice.

## Timing and acceptance

The original target was Monday 23 or Tuesday 24 November. The current official history inspected on
19 November at 22:05 UTC records six consecutive full zero-result days, 14–19 November. The corrected
19 November row is source `fa47f48872`, recorded at 21:54 UTC. Earlier continuation notes below describe a
superseded same-day nonzero result; they are historical evidence, not the current streak. Seven days and
preceding-day notice are still required. No cutover date is established by this preparation run.

- `python3 scripts/studio_split.py --streak jobs/reviews/studio_split/history.jsonl` must read at least 7.
  Each day must have `left: 0` and `tests: run`. Run the full dry run again on the frozen cutover source.
- The moving files must have zero address and credential findings. No account addresses, credentials, filled-in
  environment files, video/audio or source Git objects enter the new repository.
- Post one notice on the current thread on the preceding calendar day: the actual move date, expected unchanged
  board/film experience, brief maintenance window, and any proven credential change. Do not send a date promise
  before rehearsing and checking access. This is notice, not a request for a second approval.
- Re-read `chief_relay.py status` before the cutover decision. The elected Chief owns this move and its rollback.
- £0. No live YouTube, Buffer, NAS or film changes belong to this migration. No old files are deleted.

Completion means: one authoritative queue in studio, one complete relay cycle, one successful board publication,
one harmless tick round-trip, both MacBook slots using the right engine, and recorded rollback evidence.
A passing split test alone is not completion. Keep J3012 open until those conditions hold.

## What moves

`scripts/studio_split.py:ROUTES` is the executable inventory. Use its generated layout, never a recursive copy of
the working checkout (which holds local secrets). Record source commit, file counts and content hashes.

| Destination | Tracked content |
| --- | --- |
| Studio | `scripts/`, `jobs/`, `JOBS.md`, registry/cache/template under `channels/`, `docs/`, `.github/`, agent settings, `AGENTS.md`, `CLAUDE.md`, `HANDOVER.md`, `README.md` |
| Studio | `07_Content-Ops/`, `04_Audio/tools/`, shared `00_Brand/Channel-Setup/tools/`, the shared playbook and Studio browser launcher |
| Studio | Shared `05_Analytics/` (board source, tests, spend ledger and learnings), `studio/board_site.json`, `studio/plan.json`, temporary `studio-core/` compatibility lock |
| Each channel | Its `05_Analytics/<slug>/` records; its films, brand, character, own audio, `studio/channel.json`, `studio/RULES.md`, archive and evidence |
| Both | `.gitignore` |
| Rebuilt only | `STATUS.md` |

Do not retire copied tools/core locks until replacement channel checks work. Retain old engine copies for at least
one green week; old entry points must forward or refuse mutation after cutover, never operate a second queue.
The NAS path renaming mentioned in the broader plan is a separate operation, not part of this window.

## Identity, queue and thread decisions

The new remote is `TheLaughingGod1986/studio`, private. The initial 18 November probe found no populated default branch; after publishing the rehearsal,
the remote default became `rehearsal/j3012`. It is not production. Set the default to `main` only at cutover. Rehearsal goes only to `rehearsal/j3012`; production `main` is created at cutover from
an independently scanned, fresh root commit. Never merge Orbit history into either branch.

In the new `channels/channels.json`:

- Remove every `home` property. Keep `default_channel: owb` for legacy queue rows.
- Set `studio.github` to `TheLaughingGod1986/studio`, `studio.env` to `STUDIO_REPO`, and `studio.checkouts` to
  `["studio"]`. Set each channel checkout independently; `OWB_REPO` must mean the Orbit content checkout.
- Keep `studio.prefix: owb` during the first cutover. It is a compatibility namespace, not a home channel.
  Renaming it now would also rename lock/state files, environment variables, thread cursors and launchd labels.
  A later, separately tested rename can change them together; never run both prefixes at once.
- The current live registry already plugs WW2 in externally through `WW2_REPO` with checkout names `ww2` /
  `ww2-channel`; its manifest names the existing `TheLaughingGod1986/ww2-channel` repository. Earlier rehearsal
  snapshots used `local: channels/ww2`. Refresh the export from current main before final testing; do not restore
  that stale local entry over the live configuration.

Copy the complete frozen `jobs/` tree, including queue histories, plans, dependencies, holds, approval card IDs,
WIP/backlog and review evidence. Compare the ordered job IDs, statuses, claims, progress, holds and `awaits_ben`
values before/after; preserve the entire queue JSON, not just open rows. Do not renumber cards or replay done jobs.
Git-level history is linked by the old remote and full source commit in the migration evidence; it is not imported.

**Keep the existing thread and tick store for this move.** The thread is Orbit issue 954 as of this inspection
(resolve `scripts/thread.json` again at cutover), the tick store is Orbit issue 219, and the HOS desk is HOS PR 180.
Keep old threads readable and open; preserve the existing read cursor and board pairing/signing keys.
This avoids migrating approvals or changing the board token's Issues repositories.

The PR now makes `studio_thread.py` honor the explicit `repo` in `thread.json`, falling back to
`channels.studio_github()` only for a legacy configuration with no repository. The existing prefix, cursor and
thread-number override remain unchanged. Chief election's `fetch_comments` uses this same module/API;
`board_check.py` already reads the repository from `thread.json`. Regression tests cover both reads and posts
after changing the engine identity. `api/checks.js` names the retained store/thread repositories explicitly;
keep those synchronized with `thread.json` at later rollovers. Do not post to issue 954 in the new repository.

## Access and hosting

| Credential or service | Required access / action |
| --- | --- |
| Mini and MacBook Git/`gh` credentials | Read and push branches in private studio, plus existing channel access. Probe repository metadata and branch push without printing tokens. An installed CLI is not access proof. |
| Claude/Gemini/Cursor/Codex integrations | Studio repo visibility, read rules from studio then the selected channel. Claude app access was reported in J3012; verify the actual integration used at cutover. |
| `BOARD_GH_TOKEN` on the active board host | Existing Issues write on Orbit/HOS remains. Private studio **Contents read** is additionally needed for `api/data.js`. Probe it using that exact server credential, not the CLI token. |
| Board authentication | Keep `BOARD_KEY`, pairing cookie/signing configuration, watch signing and R2 credentials unchanged. Never copy values into Git, logs or this runbook. |
| Cloudflare/board deployment login | Cloudflare Pages `studio-kanban` is the current source deployment route (`board_site/build.py`, `wrangler.jsonc`); verify the deployed project before cutover. `BOARD_PRIVATE_DATA.md` still describes the old Vercel route. |
| Content Ops / voice / cloud credentials | Local-only credentials remain local. Link or securely copy only required ignored credential files to the new runtime location with restrictive permissions. Preserve OAuth scopes, accounts and credit ledgers. |
| GitHub Actions | Studio's own `GITHUB_TOKEN` covers its own repository. Public channels can be checked out read-only. A public channel's token does not automatically read private studio; keep its existing checks until a read-only cross-repo mechanism is proven. |

Keeping ticks and the thread on Orbit does **not** eliminate the private board-data read requirement. The simpler
supported design is `BOARD_DATA_REPO=TheLaughingGod1986/studio`, `BOARD_PRIVATE=1`, with Contents read added to the
existing board credential if it lacks it. First check whether that grant is already present. If Ben alone must change
it, finish the runbook/rehearsal first and request precisely that single credential change. Do not expose private
board data on a public branch as a workaround. No new token/account/service or paid plan is needed by design.

Keep `studio/board_site.json` at `https://board.oppti.dev`; preserve any live `readUrl` and env overrides. Deploy the
existing `05_Analytics/kanban/board_site` build from studio to the existing board project only after preview passes.
Do not deploy or reconnect the separate `/go` affiliate project. Retain the old deployment ID for rollback.
Update `05_Analytics/kanban/board_site/wrangler.jsonc` too: its current `BOARD_DATA_REPO` still names Orbit. Build with `python3 05_Analytics/kanban/board_site/build.py`; from that site folder use the existing Cloudflare Pages deployment procedure (`npx wrangler pages deploy dist --project-name studio-kanban`) only at the approved cutover.
The PR routes legacy `/api/ref` through `/api/data` with `f=ref`, so it shares the configured repository,
authentication and private cache rules. Check stale client public fallbacks before cutover.
Verify signed-out reads return 401, paired reads return current studio data, and private replies have private cache
headers. Check the Tracker's embedded public snapshot policy explicitly before deploying a private-data page.

### Board credential probe (prepared, not deployed)

The 20 November read-only Cloudflare project inspection confirmed that production has `BOARD_GH_TOKEN` as
`secret_text`, with no readable value; preview has no such binding. The existing Wrangler login refreshed normally.
This proves neither private Studio Contents access nor a missing permission. Do not substitute a CLI GitHub token,
copy the production secret into preview, rotate a token, or ask Ben to change permissions on that evidence.

`api/migration.js`, routed at `/api/migration`, checks inside the actual server runtime. It is off unless
`BOARD_MIGRATION_PROBE=1`. It requires the existing board key or paired cookie even when the board is public or open
taps are enabled. It only makes authenticated GET requests to the fixed private Studio repository, then reads
`rehearsal/j3012` and `channels/channels.json` at that exact commit. It never falls back to anonymous reads, follows
redirects, accepts a caller-selected target, writes GitHub state, or returns the file or token. Responses are no-store;
upstream failures return only a stage and status. Each upstream read has an eight-second timeout.

To finish this gate, the elected Chief should review and deploy this small additive handler and worker route from
an otherwise current production board build, retaining the existing production configuration and deployment for
rollback. Do not deploy this whole unmerged migration branch just to run the probe. Add only the temporary enable
flag, without replacing existing secrets or changing `BOARD_DATA_REPO`, private mode, ticks, cookies or the board key.
Read the endpoint through the paired board session (or the existing key in a header, never in a URL or printed shell
argument). Verify anonymous requests return 401, and authenticated requests return `ok: true`, `private: true`,
`contentsRead: true` and the rehearsal commit. Record deployment ID, UTC time and sanitized response, not credentials.
A 403/404 is an unresolved access/ref result: check the rehearsal ref exists independently before concluding a grant
is missing. A missing binding is configuration, not a reason to create another token. Only a proven access change
that the existing tools cannot make goes to Ben.

Disable the flag immediately after the observation and verify 404. Remove the temporary handler in the final
cleanup once live acceptance is recorded. Its passing mocked tests are not a deployed credential test. No production
build, binding or deployment changed during preparation, and the move still waits on all other timing/acceptance gates.

## Machine changes and cutover order

1. **Inventory and stage, with live work running.** Record a local, restricted backup of installed plist files,
   executable paths, relevant non-secret environment names, runner hashes, source commits and deployment IDs.
   Do not publish machine names, addresses, secret values or full environment dumps. Prepare clean studio and
   channel checkouts on both machines, with no service enabled against the staged engine.
2. **Implement and test remaining cutover adapters on branches.** Thread repository routing above; private data
   access; installed service/bootstrap paths; CI rules below; old engine forwarding/refusal. The rehearsal export
   is not evidence these adaptations are already implemented. Rehearse with production-shaped registry values,
   no real credentials and no live command side effects before giving a cutover go.
3. **Drain writers.** Set the existing `~/_desk/state/chief-relay.pause` and MacBook
   `~/_desk/state/macbook-worker.pause`; check both slots. Stop new cloud dispatch and notify workers on the
   thread. Let claimed work and existing renders finish or release cleanly; never kill active media writes.
   Pause board publication, analytics, Buffer checks and any other queue/state writers during the final snapshot.
   A relay pause alone does not pause those services. Do not delete locks or claim leases.
4. **Freeze and export.** Fetch all source branches, record the exact clean source heads, take the final queue and
   tick-store version snapshot, run the full split and scans. Compare the frozen queue after export. Build the
   new production repository with a root commit and source pointer; verify parent count is zero. Use a neutral
   non-address Git author identifier. Never copy `.git`, `.env`, live logs or untracked files. Push `main` without
   force, only if no conflicting production branch exists. Preserve the rehearsal separately.
5. **Switch Mini.** Runtime checkout: `~/YouTube/studio`; channel checkouts stay where they are. Install
   `STUDIO_REPO`, `OWB_REPO` and `HOS_REPO` correctly in each service environment. Keep scratch and shared locks
   at their existing locations. Rebuild the publisher's sparse worktrees for the new studio origin; do not point
   an old worktree's origin at a different repository or copy an old board-data branch into the new queue.
6. **Switch MacBook, both slots.** Engine clones are `~/_desk/worker/studio` and
   `~/_desk/worker/slot2/studio`; retain separate channel clones beside each. Update the installed worker launcher
   and `setup_macbook.sh` fallback clone URL/path, not just `STUDIO_REPO`: the current plist bootstraps Orbit.
   The PR now separates `STUDIO_REPO`/`STUDIO_GIT_URL` from `OWB_REPO`/`HOS_REPO` in the launcher.
   At cutover, set `STUDIO_REPO` to the new engine path and `STUDIO_GIT_URL` to its remote explicitly when
   running the installer; without this opt-in, setup retains the existing Orbit engine. The recovery clone asks
   for `main`, so it cannot accidentally launch the default rehearsal branch. A failed clone stops the launcher.
   `render_worker_plist.py` can write a proposed plist to scratch for inspection without installing a service.
   Slot 2 now overrides an inherited engine path with its own `slot2/studio` clone, alongside its own channel
   paths. These are proposed adapters, not evidence of a live MacBook installation.
   Slot 2 must retain its own clone, lock and heartbeat. Preserve mains-power/idle policy, tool routing and NAS
   mounting. Run `macbook_worker.py check` from the new engine, with both slots still paused.
7. **Switch board server and workflows.** Enable the verified private-read config/deployment. Seed/publish fresh
   board data and heartbeat branches from the correct origin, using existing publisher behavior. Do not manually
   force-push source branches. Update the Claude/cloud entrypoint and all agent briefs to the new engine checkout.
8. **Resume in order.** Enable one new publisher, then one relay, then the MacBook slots, then analytics/social and
   other timers. Remove only the pause files created for this window. Every service must have one writer, never
   an old and new pair. Watch the first complete cycle and the acceptance checks before declaring live.

### Service inventory

On 18 November the Mini's installed plist scan found these references. Re-enumerate at cutover; source templates
are not a complete inventory of installed jobs. Inspect plists with `plistlib`, reporting labels/path classes only.

| Service | Change / preserve |
| --- | --- |
| `com.owb.chief-relay` | Point to studio `scripts/chief_relay.py`; inspect `~/_desk/bin` installed runner too. Check `chief_relay.py status` reports matching working/installed hash. |
| `com.owb.board-publish` | Point to studio `scripts/board_publish.py`; separate studio and all channel worktrees. |
| `dev.orbit.analytics-snapshot` | Point shared wrapper to studio; keep per-channel output roots and local auth. |
| `dev.orbit.buffer-check` | Point shared wrapper to studio; preserve both channel upload registers, R2, existing posts and local auth. |
| `com.owb.ai-spend-daily`, `com.owb.tab-janitor` | Repoint shared tools; preserve ledger, CDP ports/profiles and one-tab policy. |
| `com.hos.desk` | HOS-local desk stays in HOS; audit shared-engine references and keep its read markers. |
| `com.owb.missed-runs` | Template exists; include it if installed/enabled at cutover. Avoid false alarms during the recorded window. |
| `com.owb.macbook-worker` | Repoint worker plus fallback clone on MacBook; account for spawned slot 2. |
| Cloud runs, shell wrappers, launch agents not listed | Search installed files for old engine paths; explicitly classify each as channel-local, retained shim or migrated. Preserve unrelated services. |

Use `launchctl bootout gui/<uid>/<label>` followed by `bootstrap gui/<uid> <saved-or-updated-plist>` for a controlled
service replacement. Keep labels/prefix during this window. Save both old and proposed plist copies outside Git.

### Preparing Mini launchers without installing them

`scripts/mini/render_service_plist.py` reads an installed relay or publisher plist and writes a new proposal.
It preserves the label, timing, logs, priority and local environment, sets the independent engine/channel paths,
and launches the selected Python executable directly with an argument array. No shell interprets checkout paths.
It refuses unknown services, relative paths, missing engine scripts and an existing output file. The output is
mode 0600 because an installed environment may contain credentials; keep source and output outside Git.

For each of the two services, with the staged engine already present:

```sh
python3 scripts/mini/render_service_plist.py \
  --source "$HOME/Library/LaunchAgents/com.owb.chief-relay.plist" \
  --engine "$HOME/YouTube/studio" --python "$(command -v python3)" \
  --owb "$HOME/YouTube/orbit-with-ben" --hos "$HOME/YouTube/History Of Science" \
  --ww2 "$HOME/YouTube/ww2" --out "$STUDIO_SCRATCH/j3012-relay-proposed.plist"
```

Repeat with `com.owb.board-publish.plist` and a different output name. Validate both with `plutil -lint`.
Inspect any installed `~/_desk/bin` wrapper before replacement: the proposed launchers invoke the full engine
checkout, whose relay imports sibling modules, so copying only `chief_relay.py` is insufficient. Use a Python
executable with the existing runtime dependencies. Do not install or start these files until the drain/freeze
steps above. The renderer does not migrate other timers, remove pause files or prevent old entry points from
writing; those remain separate cutover requirements.

## Workflow adaptations required before production

- Preserve J2531's queue/data-only exclusions and one-run-per-code-PR behavior; no paid Actions overage.
- `rules-check.yml`: fetch the default channel beside studio for `sync_rules.py --check`, or separately move its
  generated channel quotes. This runbook chooses a read-only checkout of Orbit pinned to the recorded channel
  commit. Remove `studio.py status --check` only in the engine-with-no-home configuration: `STATUS.md` is generated.
- `core-check.yml`: fix its repository-name conditional for studio and coordinate retirement of hash-locked
  copies. Channel checks must remain working until replacements have passed; do not just delete the lock.
- `content-ops.yml`: retain Node dependency lock, typecheck, lint and tests without production secrets.
- `notes-check.yml`: ensure notes read each channel through the registry, with no home assumptions.
- Validate all checks on the production-shaped branch. A first rehearsal branch in an empty private repository can
  become the default branch: disable scheduled workflow execution for the rehearsal, or omit active workflow YAML
  from that published snapshot while retaining byte-identical files under a non-workflow rehearsal directory.
  Record that deliberate deviation; do not call it a full CI rehearsal. Restore adapted workflows only for cutover.

## Safe rehearsal

Run from the current clean Orbit source, using a new directory under `STUDIO_SCRATCH`:

```sh
python3 scripts/studio_split.py --keep "$STUDIO_SCRATCH/j3012-rehearsal" --json "$STUDIO_SCRATCH/j3012-split.json"
```

The split builds an isolated studio Git root and sibling channel views; it neither moves source files nor starts
services. Other channel views include symlinks: never run mutations in those views. Do not run `jobs next --git`,
`chief_relay run`, `board_publish`, uploads, deployments, desk posts or any timer in the rehearsal.

After tests finish, independently inspect process exit/test summary (the split's test parser returns only named
failures; a crash without a parsed unittest failure is not proof of PASS). Record omissions and failed tests.
In the isolated studio copy, set the future registry identity above and local scratch paths. Preserve thread config,
flag its adapter as unfinished, then run targeted loader/queue/board/worker/thread tests with mocked side effects.
No live credentials or network writes are required for those checks.

Before publishing the rehearsal, scan every tracked export file again, record hashes and source commit, and move
active workflow YAML to a non-workflow rehearsal directory. Use non-address commit metadata. Publish only the
rehearsal branch to the private studio repo. Verify the remote tree and root ancestry. No change to source main,
production services, board host or thread routing is part of this rehearsal. A later cutover uses a fresh snapshot,
not this now-stale queue.

## Acceptance evidence and rollback

Store a dated record under `jobs/reviews/J3012/` with source/new commit IDs, scan counts, test exit summaries,
service/runner checks, queue comparison, board commit/deployment ID and timestamps (no private addresses).

1. **Relay:** new engine sees all registered channels and elects Chief correctly. Observe one complete normal
   dispatch cycle with a legitimate queue job and its persisted result; no duplicate claims. If none is eligible,
   record a complete idle cycle and separately prove a mocked claim cycle. Do not invent production work.
2. **Board:** publisher reports success, private `board-data` advances, paired API reads agree with that SHA and
   display queue plus channel lanes. Signed-out private reads return 401. Check both MacBook heartbeats and watch
   links. Reuse `board_check.py` and board-data/auth tests; record actual results.
3. **Tick:** use a clearly labelled migration-only ID outside real film/job patterns, through the authenticated
   checks endpoint. Read it back, confirm publication/ingestion, then remove that test entry. Never submit a real
   Approve or impersonate a Ben watch. Preserve existing ticks/history/pairings. Test ID must not produce a Chief
   approval message; verify this with `benLine` before the live round-trip.
4. **Retention:** a week of green before considering retirement of old code. Cleanup is separately reviewed;
   no deletion of channels, history, NAS assets or source branches in this job.

Rollback on wrong queue origin, duplicate writers, lost/mismatched ticks, bad routing, private data exposure,
failed relay/publish or a service that cannot resume. Pause new writers immediately and save their state first.
If no queue writes occurred after cutover, restore the saved launchers, environments, board deployment/data repo
and resume the old engine. If writes occurred, reconcile the latest studio queue and approval state into the old
engine in a clean worktree before resuming it; compare IDs, histories, claims and card ordering. Never restore a
stale queue over completed work. The retained tick store remains authoritative. Restore old code with a normal
commit if needed, never a destructive reset or force-push. Post the outcome and new next step on the retained
thread; preserve studio and rehearsal branches for diagnosis.

## Rehearsal findings, 18 November

The baseline split at source `905b34ee0b` reported `left: 0`, `clean: true`, all eight groups zero and `tests: run`;
2220 files went to studio, 12709 to Orbit, 56 to HOS and one status page was rebuilt. This was an isolated check,
not a new daily-history entry. The official daily job subsequently recorded 18 November at 07:54Z, making five consecutive zero days; this rehearsal did not add a daily entry.

Changing the isolated registry to the actual future studio repository exposed a real acceptance gap:
`test_channels.StudioOwnRepo.test_the_board_repo_and_its_github_name_come_from_the_home_channel` still expects
Orbit's GitHub identity (69 of 70 tests passed). Adapt this test to both layouts before cutover; do not treat the
baseline split's zero as a production-shaped rehearsal PASS. The thread repository coupling described above is
also directly visible in the code. Neither is fixed by this documentation PR.

The export was independently scanned after the registry/workflow changes: zero address or credential findings.
Workflow YAML is retained under `docs/rehearsal-workflows/` on the rehearsal branch only, preventing scheduled
checks from running if GitHub makes this first branch the default. The branch is evidence, not a live engine.

The additional board/worker/thread/private-data suite ran 164 tests: two failures and four skips.
Failures were the worker URL-map identity expectation and retained-thread repository expectation; see
`jobs/reviews/J3012/REHEARSAL.md` for exact names. Combined with the loader check, this is 234 tests,
three failures and four skips. Adapt and rerun before production; do not waive them.

An export inventory comparison also found that `git add -A` in the split's fresh repository omits 49
already tracked PNG/JPG assets because the copied ignore rules ignore them (including board icons).
The published rehearsal explicitly preserves those exact existing assets; no video/audio is added. At cutover,
compare the ROUTES inventory to `git ls-files` and stage the already tracked allowlisted images explicitly.
Do not force-add arbitrary files or use the dry run's initial Git tree as a complete inventory.


## Resume checklist after the 18 November verification

PR #1011 already holds this runbook; update that PR rather than creating a duplicate. The published rehearsal
root was fetched independently and its 2223 tracked files rescanned: zero address/key findings, no active workflow
YAML, no video/audio files. Its root SHA matches the evidence above. The current daily result is a different,
newer snapshot (`58b6cf14e8`, 2247 studio files, 12711 Orbit files, 57 HOS files); never reuse the old rehearsal
queue for production.

The retained-thread adapter and two production-identity test assumptions are addressed in this PR, along with
the legacy board ref endpoint. The next work remains available before the date gate: prepare launcher/bootstrap
and workflow adaptations; verify private board Contents access. Keep these as J3012 work unless separately queued with explicit links. The actual
cutover remains gated; five daily zeros do not authorize it. Do not hold ready adapter work behind 20 November.

A clone of the rehearsal alone is not a complete split layout. Supply `STUDIO_REPO` and each channel's checkout
environment explicitly; the Orbit cache is not present in that snapshot. For a full rehearsal, rebuild isolated
sibling channel views with `studio_split.py`, including routed analytics, and retain those views with the test
logs. Pointing the new engine at today's real channel checkouts is a useful compatibility probe, but cannot prove
the post-move layout: HOS's routed analytics still live in Orbit today. Never move them in the live checkouts just
to make a rehearsal test pass. The independent compatibility probe's four failures are recorded in REHEARSAL.md.

## CI preparation, 19 November

`scripts/studio_ci_prepare.py` now renders the four workflow files and their matching core hash lock into a
**new staging directory**. It changes no installed workflow, channel checkout or service. Run it from the source
checkout containing this PR, before the split; it needs that checkout's default-channel manifest. Supply the full
40-character commit of the default channel that will be present at cutover, not a moving branch:

```sh
python3 scripts/studio_ci_prepare.py --channel-sha <full-channel-commit> \
  --studio-repo TheLaughingGod1986/studio --out <new-staging-directory>
```

Review and apply those five files only to the isolated future-identity studio export. The renderer:

- checks out the default channel at the supplied immutable commit for Rules, Notes and Content Ops checks, with no persisted
  channel checkout credential, and sets its manifest's checkout environment variable;
- retains the rules-copy check, but removes the tracked `STATUS.md` check from the studio workflow;
- makes the separate core PR job skip the new studio repository, where Rules already runs its checks;
- preserves Content Ops lockfile installation, typecheck, lint and tests while supplying its pinned channel records;
- preserves queue/data-only exclusions, schedules and existing merge-skip conditions;
- updates only workflow members already present in the staged core lock. Existing channel locks remain unchanged.

It refuses an existing output directory, a non-SHA channel ref, invalid repository identifiers or a changed
workflow adaptation target. It deliberately does not install files or enable Actions. Keep active workflow YAML
out of the published rehearsal as above. Before production, run the generated Rules/Notes/Core/Content Ops
commands in the fresh split with the pinned channel available; inspect their actual exit codes. Passing renderer
and YAML checks alone is **not** a full GitHub Actions run or live cutover acceptance. Verify private repository
Actions remain within the free allowance before enabling schedules.

The pinned default-channel snapshot must match the exported rule copies. When those channel rules change later,
update the pin and regenerate the copies together in a reviewed studio change; otherwise Rules should fail.
The source channel's existing workflows and hash lock remain supported during the retention week. Do not copy
this studio-only workflow adaptation back into either channel via `core_sync.py push`.

## Executed CI rehearsal, 19 November 02:50Z

See `jobs/reviews/J3012/CI_EXECUTION_2026-11-19.md` before resuming. The fresh production-identity layout passed
Rules/Core/Notes, but the complete workflow tests did **not** pass. The former resident's missing manifest cache
is now generated by `studio_split.build`; include this extra generated file in the cutover inventory. CI renderer
tests now retain explicit pre-cutover inputs even when executed after adaptation. The affected 178 future-layout
tests pass after those fixes.

The Buffer record-root defect is addressed in this PR's next continuation: see
`jobs/reviews/J3012/BUFFER_ROOT_2026-11-19.md`. Both existing social registers remain in Orbit, including the
historical HOS subfolder. `ENGINE_ROOT` locates code; the compatibility `REPO_ROOT` now locates those records,
registered relative media, package metadata and the old project scan. Upload duplicate checks and registration
use the same record root. Credentials still load from the existing local Content Ops environment.

Every detached Buffer process must receive the absolute Orbit checkout through the registry's checkout variable
(`OWB_REPO` today). Missing configuration, a different channel's manifest, or the engine itself is a hard error
before a register can be written. The resident layout continues using its own root. Set the variable in the
Buffer timer and any upload wrapper, not only the relay. The staged Content Ops workflow now checks out pinned
channel records and sets that variable; no live workflow or timer was changed.

Content Ops passes in both tested layouts. The subsequent 06:15Z continuation below resolves the optional
browser-port assertion and passes the complete 1,495-test Python workflow suite (seven skips). See
`jobs/reviews/J3012/GUARDS_2026-11-19.md` for exact execution and limits. Deployed board access, complete
old-entrypoint protection and remaining timer adapters still gate migration.

## Retired-engine refusal and browser dispatch, 19 November 06:15Z

The optional Studio browser port is now tested as optional, matching `channel_check.py` and the loader contract.
A channel without `youtube.studio_port` must not take a MacBook browser job even when other channel browsers
answer. No port, sign-in or launch state was added to Field Order History.

`scripts/engine_guard.py` prepares a **local activation marker**, not a service switch. With no marker, existing
behavior is unchanged. During cutover, after draining writers and installing these adapters in every retained
engine checkout, atomically write `~/_desk/state/active-studio.json` on the Mini and MacBook with exactly:

```json
{"version": 1, "github": "TheLaughingGod1986/studio"}
```

Keep it outside Git, mode 0600. Write to a temporary sibling, flush it, and atomically replace the marker; never
leave a partly written activation file. The guard compares this identity with the executing code's own registry,
not `STUDIO_REPO`, so setting a new environment path cannot make old queue code authoritative. Malformed or
unreadable markers/registries refuse work. It does not print their contents. Copies/worktrees of the active
repository remain usable under the existing metadata locks.

The guard runs before the jobs, studio, relay, publisher and MacBook worker command parsers, and again before
`studio.git_transaction` reaches Git or its write callback. A retired invocation refuses even read-only commands;
use the active checkout for diagnostics. The marker does **not** forward commands, transfer queue state, stop
already running processes, or prevent independently written shell/Node timers from running. Thus the drain and
installed-service inventory remain mandatory. Old copies without this adapter cannot obey it: update them first
or disable their launchers. The Buffer/analytics timers and any direct writer outside these Python entry points
still need their own migration/guard verification before activation. This is not yet full single-writer acceptance.

Rollback restores the saved activation marker together with the saved services and reconciled queue. If this
window created the first marker, remove only that marker after all new writers are drained; otherwise restore its
previous bytes atomically. Never remove it while old and new writers may run concurrently. No marker was installed
by this preparation run.


## Daily timer entrypoint refusal, 19 November continuation

The daily Buffer and analytics shell entrypoints now invoke `engine_guard.py` before their first operation.
They check the wrapper's own engine location, independently of checkout environment overrides. They also
check the selected runtime repository; analytics checks its worktree before modifying it and after rebase,
and Buffer rechecks after its pull. The analytics entrypoint refuses a retired engine before starting its
watchdog. A missing guard fails closed. Install these updated copies before arming the cutover marker;
unmodified historical wrappers cannot observe it. No live wrapper was installed by this change.

These checks prevent a retired timer from starting. They do not drain a running timer, adapt the analytics
output/commit roots to separate channel repositories, or guard direct Node invocations. Those are still
prerequisites, alongside the installed timer inventory and the private board credential probe. Do not enable
these legacy wrappers in the detached production layout merely because their refusal tests pass.

The official source history on 19 November now records `left: 2` (`test_channels.py` and `test_jobs.py`),
so the current recorded streak is zero. The previous estimate of 20 November is no longer established.
The PR's passing future-layout tests do not replace an official daily result; never manufacture missing days.
A same-day corrected full run may replace today's row through the existing daily recorder, but only actual
recorded consecutive passes and the prior-day notice can authorize a move. Do not promise a new date yet.
See `jobs/reviews/J3012/TIMER_GUARDS_2026-11-19.md` for this continuation's scope and verification.

## Detached Buffer timer, 19 November continuation

The Buffer timer now separates executable, records and credentials. `STUDIO_REPO` selects the engine;
`ORBIT_REPO` remains only the legacy engine fallback when that variable is unset. In the detached engine,
set the record checkout variable from the registry (`OWB_REPO` today). The CLI's new local `record-root`
command uses the same validated resolver as actual Buffer operations, without acquiring the desk lock or
calling an API. The timer uses that result for both channel registers and all record Git commands, while
running both checks from the engine's Content Ops directory. It does not run the old channel engine guard
against the content checkout: a retired engine can still hold authoritative channel records.

Credentials default to the record checkout's ignored `07_Content-Ops/.env`. `BUFFER_ENV_FILE` may select
another existing absolute local path. Preserve the installed credential location; never copy values into Git.
Both actual checks still own their operation lock; a 75 from the first check prevents the second and every
record commit. Missing record roots or credential files stop before API work. Record pushes still follow the
existing main-branch-only policy; this adapter does not promise atomicity across Git repositories.

Direct `buffer-mirror.ts` commands also run the Python identity guard from their own code root before their
operation lock. `record-root` obeys the same guard. This closes that direct Node entrypoint; it does not claim
coverage for other Node upload/metadata writers. Install Python on the service PATH, as already required by
the shell timer. No guard is armed by installing the code alone.

The Mini plist renderer additionally supports `dev.orbit.buffer-check`, proposing `/bin/bash` plus the exact
staged wrapper path and independent engine/channel environment. Its schedule, logs and credential environment
are preserved. Use the same staging command as above with that installed source plist and a fresh output path;
inspect and lint it locally, never commit its contents. Analytics is deliberately unsupported by the renderer
until its per-channel output and commit handling is adapted. No timer was installed or run against live services.

Verification and the next resume point are in `jobs/reviews/J3012/BUFFER_TIMER_2026-11-19.md`.

## Analytics cutover hold — 19 November

The official daily split recorded `left: 2` (one failure each in `test_channels.py` and `test_jobs.py`),
so its consecutive-pass count is **0**. The 20 November earliest-date estimate above is obsolete: the first
possible move is after seven new consecutive zero-result daily records and the preceding-day notice. A green
pull-request check is not a replacement for that recorded streak.

Do not start the analytics timer in the separate studio checkout until its full data flow is adapted and tested:

- The snapshot/report record-root adapter is now prepared (see continuation below). The timer must supply
  actual channel record worktrees through registry checkout overrides and stage their existing histories first.
- Report generation now supports separate channel roots and keeps the combined dashboard in the engine.
  End-to-end timer tests must still verify CTR/catalog sidecars and Git destinations in the full staged layout.
- `07_Content-Ops/launchd/analytics-snapshot.sh` currently uses one Orbit worktree for source code, snapshots,
  the Shorts gate and all Git commits. Separate the engine from each data worktree, run the gate against Orbit's
  actual upload registry and library, and commit only each repository's own generated files. Keep field-order
  queue writes directed to the studio queue. Preserve per-channel partial failure, lock/guard, timeout, retry,
  credentials and board-publish behavior; never commit one channel's records into the engine or another channel.
- Exercise the detached layout with isolated repositories and fake API/CLI calls: verify exact output and commit
  destinations for all registered channels, combined dashboard, gate library, failed-channel isolation, retry,
  retired-engine refusal and missing-root refusal. Also run the existing resident-layout tests. The checks must
  not push, publish, invoke the live timer, or write to channel checkouts.

The complete timer adapter remains a cutover prerequisite. The live timer
continues in its existing configuration until the single-writer cutover and successful acceptance checks.


### Snapshot and report adapter prepared — 19 November, 16:10 UTC

`07_Content-Ops/scripts/analytics-paths.ts` now resolves detached channel record directories with the existing
Python registry loader. It refuses missing histories, mismatched manifests and engine-local record destinations
before snapshot API calls. Snapshot/report direct commands also obey the engine retirement guard. Resident timer
paths remain unchanged. Reports and their sidecars use channel directories; the combined dashboard stays in the
engine. The separate existing Field Order report behavior is preserved.

Typecheck, lint, eight lock pretests and 222 application tests pass, including actual registry-loader fixtures and
separate report/CTR/dashboard destinations. Evidence and the precise next timer step:
`jobs/reviews/J3012/ANALYTICS_ROOTS_2026-11-19.md`. Do not activate the timer on this partial adapter: worktree,
commit/retry, gate-library and queue routing still need their end-to-end migration checks.

### Record worktree and dispatch preparation — 19 November, 17:30 UTC

`scripts/analytics_worktree.py` now supplies tested per-repository preparation, scoped record commits and bounded
push retries. It preserves local record commits after a failed push or conflicting rebase, including retry on a
later run with no new edits. Unrelated files/history, another repository, attached/shared checkouts and retired
engine code are refused. Studio's scope is the combined dashboard; each channel's scope is its own analytics,
plus Orbit's open-gate library JSON. The timer must validate source checkouts through the registry and serialize
this helper; the helper is not yet wired into the timer and does not acquire a service lock itself.

Field Order dispatch now uses the registry-aware analytics record root and validates the configured shared
queue's engine identity. At cutover set `FIELD_ORDER_QUEUE_REPO` to the active shared studio checkout, while
channel checkout overrides point to the analytics record worktrees. No queue belongs in a channel record tree.

Evidence: `jobs/reviews/J3012/ANALYTICS_WORKTREES_2026-11-19.md` (13 real-local-Git tests; eight lock pretests and
227 application tests; typecheck/lint). Full timer orchestration, gate-library routing and fake-API acceptance
remain before its plist can be prepared or installed. No live service or record location changed.

### Serialized analytics session prepared — 19 November

`scripts/analytics_session.py` supplies the next orchestration layer, without an installed entrypoint.
`locked_session` holds one machine-wide advisory lock across preparation, collection and publication (the caller
must keep its work inside the context). Its preflight validates the executing engine, shared queue and every
channel against the registry and credential-free GitHub remote identities, before creating record worktrees.
It refuses resident/retired engines, aliased checkout environment names, overlapping source/scratch roots,
wrong channel manifests and missing staged snapshot histories. Actual detached worktree manifests and histories
are checked again after preparation. Channel environment overrides target record worktrees; the Field Order
queue override targets the active shared studio checkout. Source paths remain available separately for media
and credentials, and the parent process environment is not changed. Publication attempts every repository,
returning failed owners while retaining the worktree helper's pending commits for retry.

Record ownership now follows registered slugs. The channel setting `analytics.open_gate_library` names the
owner of the open-gate library JSON; Orbit enables it. This replaces hard-coded channel-name rules in the helper.
Carry that setting into the channel checkout and its cached manifest during the split.

This is still preparation, not full timer acceptance. Next wire the session into the timer's collector/report,
credential loading, gate library/frame paths, timeouts and board-publish calls; test the complete invocation with
fake APIs before adding its staged plist. No timer, service, active marker or live records changed.
Evidence: `jobs/reviews/J3012/ANALYTICS_SESSION_2026-11-19.md`.


### Collection and publication layer prepared — 19 November, 22:15 UTC

`scripts/analytics_collection.py` now runs each registered channel's snapshot independently, then the required
auxiliary phase, combined report, per-owner publication/retries and optional board refresh, all inside
`analytics_session.locked_session`. Child processes receive record checkout overrides while the publisher gets
source checkout paths. The queue override stays on the shared active studio checkout. Commands execute from
the detached studio record worktree so the combined dashboard belongs to that repository.

The caller must supply an existing absolute local credential file outside all record worktrees. Inherited
analytics OAuth and channel-ID variables are cleared before Node loads that file, preventing stale launchd
values from overriding it. Dependencies are reused through an ignored worktree-local link; an unexpected
existing directory is refused. Each subprocess has a timeout that kills its process group, including Node's
children. Only step names and exit statuses are returned, never credential-bearing child diagnostics.

A failed collector does not skip other channels, reports or publication. Publication runs even with no new
changes, to retry pending commits. The required auxiliary callback must implement the gate and dispatch phase;
there is deliberately no default callback or installed command that silently omits it. A callback exception
releases the lock and leaves generated records for the existing next-run recovery. The next continuation must
wire that callback, stage the gate library and frames correctly, provide bounded gate/dispatch commands, then
connect the shell entrypoint and staged plist. This is not full timer acceptance or cutover approval.

Evidence: `jobs/reviews/J3012/ANALYTICS_COLLECTION_2026-11-19.md`. No live timer, credential, channel record,
activation marker, board deployment or service was changed.

### Gate and dispatch adapter prepared — 20 November

`scripts/analytics_auxiliary.py` supplies the collection callback: bounded Studio-read dispatch against the
session's shared queue, then gates for registry-selected library owners. Each gate reads today's snapshot and
upload registry from its channel record worktree, media and channel profile from the source channel, and an
explicit cache. Missing current inputs are a named failure; yesterday's snapshot is not silently substituted.
A dispatch or gate failure still allows reports and publication of other collected records.

`scripts/analytics_gate.py` wraps the existing gate modules without changing their shared implementations or
core hashes. The adapter selects the source channel's profile, isolates library JSON and new frame files in
the persistent record worktree, preserves source-relative VO lookup and channel-relative frame links, and
refuses mismatched channel owners, symlink record targets and retired engines. Its subprocesses expose only
the add/check operations needed by the upcoming gate; the outer collection runner bounds the process group.
Frames remain ignored, disposable local comparison aids; thumbnail arrays and hashes in library JSON are the
durable comparison record. Existing source frames remain untouched. The split retains channel_profile.py in
the channel, with a temporary engine copy for legacy callers; the analytics adapter never uses that default.

This is preparation only. Timer shell/plist wiring, cache readability fallback and complete fake-API timer
acceptance with real record commits still remain; the installed timer is unchanged. No live gate, API,
queue dispatch, board publication or source-media mutation was run by these tests.


## Detached analytics timer wiring, 20 November continuation

`07_Content-Ops/launchd/analytics-detached.sh` is the proposed detached-engine entrypoint. It is separate from
the installed resident timer, which remains unchanged. The shell calls `scripts/analytics_timer.py`; its parent
bounds the entire worker process group to 45 minutes. The worker rejects resident/retired engines, probes the
media cache with a five-second child process, then runs the required dispatch/gate callback and collection under
the existing fixed record-session lock. Collection, per-owner commits/retries and board refresh retain their
individual time limits. Diagnostics containing API responses are suppressed; the launcher reports success or a
nonzero failure/timeout. Inspect record worktrees and pending commits before retrying a failure.

Configuration is local to the proposed plist, never a credential value in Git:

- `ANALYTICS_CREDENTIAL_FILE`: required absolute path to the existing local credential file outside record
  worktrees. Keeping it in its existing source checkout avoids a credential copy or permission change.
- `STUDIO_PYTHON`: the renderer sets the supplied absolute Python executable.
- `ANALYTICS_RECORDS_DIR`: persistent detached records; default is `records` under the internal safe directory.
  This deliberately does not reuse the old single resident worktree. Before first cutover, reconcile any pending
  old tracker commits and stage the channel histories. Never silently fall back or discard these record worktrees.
- `ANALYTICS_SAFE_DIR`: defaults to the internal Application Support tracker directory.
- `ANALYTICS_GATE_CACHE`: defaults to the existing staged gate-media cache. A failed five-second write/read probe
  chooses the internal safe directory's gate-media cache. If both probes fail, collection refuses. A missing cached
  NAS clip remains NOT CHECKED; no gate waiver is implied.
- `GATE_LIMIT_S`: defaults to 600, accepted range 1–1800; `BOARD_PUBLISH=0` disables board publication only for
  controlled tests. Normal cutover acceptance must publish.

To prepare the service, make a private scratch copy of the installed `dev.orbit.analytics-snapshot` plist and add
`ANALYTICS_CREDENTIAL_FILE` to that copy's EnvironmentVariables (path only). Run the existing
`render_service_plist.py` command with that copy as `--source` and a fresh private `--out`; it selects the detached
shell, preserves the 06:40 schedule/logs, and sets engine/channel roots. A missing credential path is refused.
Inspect and `plutil -lint` the proposal; do not install it before the drained cutover and complete acceptance.

Verification uses the real timer worker, collection/session and Git record helpers with fake command results and
three temporary bare remotes. It checks dispatch queue routing, source-media routing, channel-owned gate/report
records, dashboard ownership, publication despite a rejected channel push, retry on the next identical run, and
untouched source checkouts. Separate tests cover actual cache probes, bounded failures, literal shell arguments,
retired/resident refusal, supervisor time limit and service schedule preservation. These prove orchestration;
they do not claim actual TypeScript/API contract acceptance, deployed board access or a live relay/publish/tick.

## Collector acceptance and AI-spend service, 20 November continuation

The newer checks run the actual Node/TypeScript entrypoints, not replacement collector commands. A strict fake
fetch layer answers only known YouTube/OAuth endpoints; raw Node network connections are refused. Fake credentials
live outside the four temporary source repositories. The real timer worker, registry, record-session lock and Git
helpers publish the resulting records to temporary bare remotes. Every source checkout remains unchanged.

The gate/dispatch callback and board publication are deliberately excluded from that transport acceptance test;
their existing isolated tests remain separate. This does not prove deployed APIs, credentials or live scheduling.
See the evidence file above for baseline split and future-layout results, rather than treating mocked transport
as permission to activate the timer.

The read-only Mini service inventory found `com.owb.ai-spend-daily` calling `ai_spend_daily.py --git`. The plist
renderer now supports that service and preserves its schedule, logs and environment. Both `ai_spend.main` and
`ai_spend_daily.main` check the executing engine before parsing or pool reads; `ai_spend.append` checks again
before making a directory, taking a ledger lock or running Git, covering imported calls too. With no activation
marker, existing behavior is unchanged. The marker was not installed. Non-CLI exporters that write the ledger
directly still require inventory and guards; do not treat this addition as complete writer coverage.

The same inventory identified the local Cursor worker and Grok watchdog wrappers outside this checkout. Inspect
their installed commands and retirement behavior before cutover. The HOS desk, browser launcher, tab janitor and
local reminder/worker services also need explicit retain-or-adapt decisions. The MacBook inventory remains a
separate mandatory check. Keep secret-bearing plist backups local and restricted; publish names and decisions only.


## Additional record-writer guards, 20 November continuation

The thumbnail test ledger and first-day launch record tools also bypass the shared Git transaction when called
without `--git` or imported directly. Their command-line entrypoints and final save functions now call the same
retired-engine guard. Refusal happens before loading CLI records or resolving/creating a launch record path;
an existing thumbnail ledger remains byte-identical. With the activation marker absent, behavior is unchanged.
This is additional writer coverage, not proof that every old entrypoint is covered. No marker was installed.

The Mini installed-service inspection still finds the local Grok watchdog referring to the old engine and lacking
an active-engine marker or pause check. Audit its restart command before the drained window: pausing the relay
alone must not allow a watchdog to restart the retired engine. Keep its existing live configuration until that
replacement is tested. The Cursor worker launcher could not be resolved by the limited static plist inspection;
resolve its actual shell environment and target before cutover. The tab janitor and HOS browser launcher manage
browsers, not the shared queue: retain one instance, preserving ports and profiles. The HOS desk remains in its
channel checkout; review its dispatch behavior separately. The local HOS reminder is also retained pending that
audit. None of these observations constitutes MacBook acceptance; both slots still need actual machine checks.

See `jobs/reviews/J3012/RECORD_WRITERS_2026-11-20.md` for the bounded change and checks. Resume the existing PR;
deployed board Contents access, remaining wrappers/exporters, both-machine inventory and refreshed private
rehearsal are still required before giving the day-before notice and proceeding to live acceptance.


## Installed-service inventory and legacy launcher handling (20 November)

Run `scripts/mini/inventory_services.py` on **each machine** before the window. It only reads bounded plist/script
files: it never runs the configured program, shell, command substitution or a discovered worker. JSON contains
labels, source hashes and booleans, not command lines, environment names/values, paths or source text. A malformed
plist produces an unreadable row and a nonzero exit without suppressing the remaining rows. No matching files also
returns nonzero. Keep raw output local; the reviewed evidence belongs in the runbook.

```sh
python3 scripts/mini/inventory_services.py \
  --old-engine "$OWB_REPO" \
  --prefix com.owb. --prefix com.hos. --prefix dev.orbit. \
  --prefix com.cursor.mac-mini- --prefix com.ben.grok
```

Use the actual prior engine path and appropriate worker filename prefixes on the MacBook. Resolve every unknown
command manually; this deliberately bounded scanner does not follow scripts recursively or infer a service is
safe from its name. `guard_mentioned` and `pause_mentioned` are lexical observations (including comments), **not**
proof that any execution path checks them. Every row remains `needs_review: true`. Pair the inventory with
`launchctl` loaded-state inspection during cutover: an installed plist is not proof of an enabled/running job.

The Mini scan found **18 definitions: 17 parseable, one malformed**. Actual wrapper reads settle the previously
unresolved Cursor target. Handle the following before changing the active-engine marker:

| Installed service | Window handling and resumption condition |
| --- | --- |
| `com.owb.cursor-worker` | Its local wrapper still tells Cursor it is Chief and chooses old inbox work. It has a pause-file check but no retirement guard. Drain it, save its installed definition, and keep it booted out at cutover. Do not restart this obsolete prompt; the routed specialist worker supplied by the current relay replaces this legacy path. Retain files for rollback. |
| `com.owb.grokbot-watchdog` | Its wrapper can restart the desktop app through independent relaunch and updater modes as well as disconnect recovery. No pause/retirement check was found. Boot it out **before** draining the app/relay; retain its definition. Resume only after all restart paths obey the cutover pause and the app's engine context and notification route are verified. Changing the notification command alone does not migrate the app. |
| `com.ben.grok-bot` | The app's own launch agent can also start it. Include its loaded state and app processes in the drain so disabling the watchdog alone cannot reopen an old worker. Keep app state and login unchanged; restore only after the engine context is verified. |
| `com.cursor.mac-mini-worker` | The separate worker wrapper contains an old-engine reference; it is not the legacy scheduled Cursor wrapper above. Drain and inspect its working directory/prompt and child worker state before resuming it. |
| `com.cursor.mac-mini-hos-worker`, `com.cursor.mac-mini-repo-workers` | Direct worker wrappers resolved; absence of the old literal root proves nothing about remote prompts or children. Drain studio-capable work and verify channel versus engine roots. Do not change unrelated project workers. |
| `com.hos.desk`, `com.hos.local-wan-ltx-queue-reminder` | Channel-local programs resolved. Preserve channel roots; inspect subprocess/queue references before resumption. Keep their read markers. |
| `com.hos.cdp-browsers` | Preserve signed-in profiles and existing ports. This is not an engine writer; do not close Chrome as part of the move. |
| `com.owb.missed-runs` | The installed plist fails XML parsing. Establish loaded state separately (launchd may hold an earlier valid definition). Keep its old bytes for rollback and prepare a valid replacement before relying on it for post-move monitoring. Do not overwrite it during preparation. |
| `com.owb.ai-spend-daily`, `com.owb.tab-janitor` | Old-root references found; shell resolution remains incomplete in this bounded scan. Use the prepared spend service adapter; manually resolve the janitor and preserve the one-tab policy. |

The remaining inventory rows include the prepared relay, board, analytics and Buffer services and unrelated
Cursor project workers. Their configured script hashes are local evidence, not proof the staged adapters have
been installed. Preparation does not boot out any service or alter a marker. At cutover the operator records each
saved definition, loaded state, decision and replacement hash locally, drains children, then installs only the
reviewed replacements. Rollback restores those definitions and loaded states after draining the new writers.

Validation: seven inventory tests cover non-execution, value suppression, binary plists, direct and home-expanded
wrappers, unresolved dynamic shell, invalid labels, missing scripts, malformed XML and bounded input size. Nine
existing service-renderer tests pass. No live service, queue behavior, browser, credential or film was changed.


## Heartbeat and board writer guards, 20 November continuation

`claude_beat.py`, `board_check.py` and `notes_push.py` check engine retirement before CLI parsing.
Their imported `push` / `post` entrypoints check again before Git, network calls or moving an uncommitted
notes edit aside. This prevents a stale engine from publishing a Chief heartbeat, changing the board-health
state or posting its report, or checking out notes before the existing transaction guard can refuse the write.
Pure heartbeat construction and board inspection helpers remain usable. No activation marker was installed.

The process used for this continuation did not have `BOARD_GH_TOKEN`. This is not a test of the Cloudflare
runtime's credential, and does not show that its grant is missing. The deployed Contents probe remains unverified;
do not substitute the CLI's GitHub credential or ask Ben to change a grant on this evidence alone.
