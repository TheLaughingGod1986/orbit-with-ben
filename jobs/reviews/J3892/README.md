# External MacBook cutover handoff — J3892

Preparation only. J3012 remains 3/4. No service, pause, marker or production branch is changed by this PR or its tests. Chief must review and merge the implementation before a separately authorized coordination window. This is a system change; this worker does not grant PASS or activation.

**27 November Chief review: not ready for live activation.** The helper still needs a cross-machine result and resume/recovery route. Its local result and retained pause cannot be operated from the Mini through an unavailable SSH connection or through the paused worker. See `jobs/reviews/J3012/CUTOVER_HELPER_REVIEW_2026-11-27.md`. The invocation below remains preparatory documentation until that gap is implemented and reviewed.

## Two phases, using the existing queue and thread

1. Chief assigns a coordination child through the installed worker's authoritative queue. Do not make it depend on J3012 completion. The child has explicit authorization to establish the existing worker pause, arrange the global writer drain/freeze with Chief, prepare the private plan and launch the external supervisor. J3892 itself is preparation and cannot do those live actions. The future child becomes `job` in the plan and terminal gate; every activation command is also anchored to implementation J3892.
2. The coordination child uses the reviewed helper from a durable checkout, records its actual agent and owning worker PID identities, generates the plan, launches the supervisor, publishes the result path/PID/plan digest/nonce, marks its coordination job done, returns every checkout to main, and exits. The detached supervisor waits for BOTH the terminal authoritative queue row AND disappearance of every recorded owner PID/process group, both unheld slot locks, no other MacBook claims, and no worker/agent children. PID reuse blocks rather than being mistaken for exit. It captures initial descendants and retains identities of detached descendants observed while waiting, excluding the external supervisor itself. Any surviving command that names a worker checkout or the working-film store also blocks, conservatively including unrelated work in those roots. It holds both existing lock file descriptors during the transaction and never deletes a lock or kills a process.
3. **After review and global freeze**, Chief exports the fresh private production Studio root and queue, confirms its exact commit and raw queue-blob SHA-256, and posts the one-line activation below through the existing studio thread. A main branch's existence, a rehearsal root, or a completed queue row grants no activation. A trusted human owner/collaborator posting this exact command attests that the named agent is the elected Chief and global freeze has occurred. This is the explicit authority boundary; the MacBook does not independently prove the Mini's election or global drain from a local heartbeat. Do not post on behalf of an unelected worker.
4. The supervisor verifies trusted association, human account, exact issue URL, unchanged creation/update timestamp, command grammar, job/nonce/plan digest and freshness (at most one hour). It pins the comment ID and canonical payload digest and reads that exact ID again at the replacement boundary. A second command, edit, changed production main, untrusted matching command, stale export or wrong blob fails closed. Reactions/other metadata changes also conservatively invalidate the pinned payload.
5. It verifies both engine clones are clean at the reviewed staged heads, fetches the exact production main from their existing private origin, checks queue and production source hashes/registry, preserves each old main under a unique backup branch, then creates a new main at the authorized commit. It never resets, force-pushes or executes a rehearsal queue. This safely handles the intentionally unrelated parentless rehearsal/production roots.
6. After repeating drain, source, installed/loaded settings, cancellation, deadline and immutable activation checks, it backs out **only** the worker LaunchAgent, atomically replaces that plist with the revalidated proposal, and bootstraps only that service. Proposal construction copies every property/environment value verbatim except the approved worker bootstrap and the two Studio engine environment entries. Loaded arguments and explicit environment values must match the proposal; only launchd bookkeeping additions are allowed. No power, idle, slot, content-root, heartbeat or interval default changes are introduced.
7. It creates the existing engine guard marker, checks that both old registries refuse as retired and both new engines accept the marker **without invoking any worker/queue**, writes its result and exits. The existing pause remains. Chief resumes only after J3012's other acceptance checks; this helper does not perform or claim those checks.

## Private plan and concrete invocation

The future coordinator supplies a mode-0600 JSON config inside a mode-0700 directory under `~/_desk/state`. Use absolute paths, never put raw settings or wrapper contents in git or a thread. The helper's `prepare` command reads/saves originals; it neither pauses nor installs anything.

Required config fields:

- `job`: actual coordination child ID, never J3012; `deadline`: UTC epoch within the next hour.
- `authority_repo`, `thread`, `issue_url`: the current installed authoritative queue/thread, copied from `scripts/thread.json`; URL form is `https://api.github.com/repos/<repo>/issues/<number>`.
- `production_repo`, `production_url`: private Studio owner/repository and its exact HTTPS `.git` URL. These are supplied from Chief's reviewed migration plan, never inferred from a rehearsal branch.
- `engines`: exactly `~/_desk/worker/studio` and `~/_desk/worker/slot2/studio` (expand `~`); `staged_heads`: map of those absolute paths to their exact current 40-character commit IDs. Both must be clean main; their origin must already be the production URL.
- `old_engines`: both retained installed Orbit engine roots; `owner_pids`: the actual coordinator agent and its owning worker PID, plus any separately grouped descendants known to belong to it. Inspect actual ancestry, do not substitute launchd's state/PID or the short-lived prepare CLI. Preparation captures PID, group and start identity; any reuse fails closed.
- `installed`: `~/Library/LaunchAgents/com.owb.macbook-worker.plist`; `locks`: both existing `~/_desk/state/macbook-worker{,-2}.lock` paths; `pause`: `~/_desk/state/macbook-worker.pause`; `marker`: `~/_desk/state/active-studio.json`.
- `installed_hash`, `loaded_hash`, `proposal_hash`: reviewed exact digests. `loaded_hash` hashes `canonical(loaded_settings(raw_launchctl_print))`; `proposal_hash` hashes `proposal(installed_bytes, engines, production_url)`. The helper exports those pure functions for the coordinator's read-only snapshot. It verifies supplied expectations rather than silently approving newly observed settings.
- `sources`: absolute file-to-SHA-256 map. Mandatory: installed plist, the helper itself, its sibling `engine_guard.py`, the shared `macbook/render_worker_plist.py` renderer and its plist template, and both old engines' worker/guard sources. Include every referenced on-disk bootstrap/wrapper and any other reviewed source. Originals are copied privately by numbered entry; the plan preserves their mapping.
- `production_sources`: production Git paths mapped to reviewed exact SHA-256 values. At least `scripts/macbook_worker.py` and `scripts/engine_guard.py`, including any other source required by the reviewed migration. These pins are independent of the future queue hash.

Use a fresh output directory for every attempt. The commands below are for the **future authorized coordinator**, not this preparation run:

```sh
python3 scripts/macbook_cutover.py prepare --config "$CONFIG" --out "$HANDOFF"
# Capture the printed SHA-256 as PLAN_SHA; no credential values are printed.
python3 scripts/macbook_cutover.py launch --plan "$HANDOFF/plan.json" --sha256 "$PLAN_SHA"
```

`launch` requires the already-authorized pause, verifies the helper digest and private modes, and permits one launch per directory. It uses `start_new_session=True`, null stdin, closed inherited descriptors and a mode-0600 log. `supervisor.json` records its PID/group/start, fixed deadline and result path. The CLI exits immediately; that new session's supervisor continues independently of the coordinator's worker service/group. Polling is every five seconds; every command has a 30-second timeout reduced to the remaining fixed budget. It does not launch a persistent daemon. Never start two supervisors. If the supervisor exits without `result.json`, treat that as failure, inspect its private log and preserve the directory; absence of a result is not success.

The exact activation body, with values from the private plan and new freeze/export, is one line with no trailing newline or surrounding prose:

```text
[Chief] MACBOOK-CUTOVER J3892 coordinator=<CHILD> <NONCE> <PLAN_SHA256> chief=<ELECTED_AGENT> commit=<PRODUCTION_COMMIT40> queue=<RAW_QUEUE_BLOB_SHA256> global-freeze=confirmed
```

Write that line to a file with no trailing newline and post with `env -u OWB_AGENT python3 scripts/studio_thread.py post -f <file>` in the current authority checkout. Unsetting the attribution variable prevents the thread helper inserting an extra `[Codex]`/`[Claude]` tag into the exact command grammar. Use the current existing thread; do not create another queue or use SSH. The allowed elected-agent values are `claude`, `codex`, `gemini`, `chief`. The helper reads trusted owner/member/collaborator comments only as authority and never accepts a bot's activation. The separate command is the recorded activation after review, not an implication from J3892 completion.

## Cancellation, failure and retry

Chief can post this exact trusted command on the same thread before replacement:

```text
[Chief] MACBOOK-CANCEL J3892 coordinator=<CHILD> <NONCE>
```

A local operator can also create the private handoff directory's `cancel` file. Never kill an agent or remove a lock. Cancellation is checked while waiting and again immediately before replacement; once the destructive boundary has begun, wait for the bounded result and keep the pause. Cancellation cannot undo a completed replacement.

`result.json` reports `installed-paused` or `stopped-paused`. Originals, loaded snapshots, proposed plist, preserved Git branches and the per-attempt `replacement-started` sentinel survive failures. No automatic restart of the stale service/queue occurs. If a clone update partly succeeds or bootstrap/guard fails, Chief inspects those receipts, leaves the pause, and prepares a new reviewed config with the observed heads/settings. A fresh directory/nonce/deadline is required; old activation cannot authorize retry. If the marker already exists, this helper refuses rather than deleting/replacing it. Marker/service recovery is a separate Chief decision using retained originals, not an automatic rollback that could restart stale jobs.

Private files and results are evidence of this one attempt, not a production status database. Existing queue/thread remain authoritative. Post only sanitized counts/hashes/result to the thread.

## Validation limits

Focused tests replace the entire command adapter; neither launchctl, Git operations nor process launches reach the real machine. Files are temporary fixture files, not live pauses/markers. Dry-run receipts include exact tested source hashes and fake-adapter transaction steps. These establish software refusal/transaction behavior, not a loaded production cutover, independent security review or J3012 acceptance. No full legacy suite, inventory or credential probe is repeated.
