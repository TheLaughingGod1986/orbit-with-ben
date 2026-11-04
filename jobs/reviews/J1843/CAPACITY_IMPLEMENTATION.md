# J1843 implementation checkpoint — 4 November 2026

This branch is an unfinished, observation-only implementation checkpoint. It
must not enable another execution lane or portable dispatch. J1914 authorizes
engineering now; fresh evidence and exact-head review still precede rollout.
The remainder needs a separate bounded run on **this same job**, not a duplicate.

## Implemented

- `chief_relay.py capacity` reports the process-validated Mini execution lease,
  canonical claimed/starting phase, owner, host, action, progress and recorded
  task estimate. A task ETA and lease expiry are never called a free-slot time.
  It exposes cached MacBook evidence and its age; capacity stays unverified.
- New leases carry host and observed machine name. MacBook heartbeats retain
  their old fields and add observed machine name, architecture, power, idle,
  free disk, load and CPU count. They explicitly leave registration, available
  memory, auth/quota readiness and media capability unverified.
- `dispatch_capacity.py` is a pure shadow planner, deliberately disconnected
  from launch/claim/reroute paths. It uses workflow deadlines/dependencies/holds,
  worker/model probes and capability requirements. Only explicitly scoped,
  CPU-only, no-spend/no-publish assembly/chart jobs can be proposed.
- Active leases occupy host, worker and shared-account capacity. Duplicate jobs
  and film/stages are excluded within a proposal. Legacy leases without account
  attribution cannot prove spare quota. Additional host lanes need matching
  reviewed and installed heads. MacBook overflow needs demonstrated occupied
  Mini capacity, registered/fresh host evidence, mains/idle/resource guards and
  an approved portable contract. Chief/review work is never overflowed.
- Portable input contracts require approved relative paths, exact SHA-256,
  fresh readable-host receipts and output receipts. Local preflight streams
  hashes and rejects changed bytes, path traversal and symlink escapes. No
  transfer implementation or receipt acceptance is implied.

## Evidence observed during this run

- Both checkouts pulled successfully. Tracked files in the shared checkout
  were clean, but many unrelated untracked assets exist; engineering was done
  in isolated `/private/tmp/J1843-wt`, branch `codex/J1843-capacity`.
- Mini relay PID 2179 held J1843, worker codex, lease
  `2026-11-04T00:20:35Z`–`2026-11-04T00:46:35Z`. This was the only execution
  record; the relay still has one serial lane.
- Cached MacBook heartbeat at `2026-11-04T00:12:07Z` says generic `macbook`,
  `idle`, `no MacBook job waiting`. It contains no registered machine identity,
  measured capacity, fresh auth/quota or media capability proof. No laptop
  availability or model identity was inferred from it.
- Cursor latest recorded execution J1847 at `2026-11-03T23:17:56Z` exited 1,
  `out_of_usage=true`. The relay log includes `Authentication required` failures.
  A fresh noninteractive `agent status` returned exit 0: `Login successful!`
  and `Logged in (unable to fetch user details)`. This supports a changed auth
  observation only; it is not a current model/quota-success proof. No interactive
  login or paid prompt was started. No account identity/token was printed.
- Codex Mini and laptop remain one shared account pool. Tool inventory supplied
  no demonstrated audio or moving-video perception; capability report is empty.
- Disk about 14 GB free. Required `nas_offload.py --apply` found no scratch old
  enough to move. No NAS content was removed or overwritten.

## Validation

- `python3 -m unittest discover -s scripts -p 'test*capacity*.py'`: **25 PASS**.
- `test_workflow_state.py`: **31 PASS**.
- `test_macbook_worker.py`: **17 PASS**.
- `test_chief_relay.py`: **74 PASS**, fake worker CLIs only.
- `test_jobs.py`: **30 PASS**.
- `git diff --check` and Python compilation: PASS.

These tests establish shadow calculations and existing serial behavior. They
**do not establish atomic cross-host claims, real concurrent launch, transfer
completion or rollout acceptance**. Synthetic J1834/J1841 cases exercise a busy
Chief, an independent specialist and preserving a delivered review; the actual
ISS review and candidate assets were untouched.

## Remaining implementation and acceptance

1. Continue step 2 of the existing three-step plan. Finish integrating reservations into
   the canonical Git queue transaction and stage claims; revalidate all guards
   there. A proposal must not be described as a claim or a launch. Competing
   hosts must race against the same canonical state, with idempotent reservation
   tokens and explicit rollback/expiry. Do not introduce a second job tracker.
2. Add bounded, process-validated per-host execution records, crash recovery and
   a launcher that can dispatch another independent job while Chief is busy.
   Preserve elected-Chief ownership and all existing browser/generation mutexes.
   Do not remove the global serial lock before the complete replacement passes.
3. Finish registered-host and per-model/account evidence collection. Verify
   actual MacBook identity, current mains/idle/disk/memory/load, supported paths
   and capabilities. Recheck power/idle immediately before laptop launch. Model
   quota/auth failures must walk a verified fallback without resetting shared
   account limits. Do not treat retry expiry as successful reauthentication.
4. Implement approved-input transfer and output receipt verification, rehash on
   each consuming host, then connect portable reservations to MacBook's existing
   identity/claim flow. Preserve the original routing and Chief review gates;
   portable inputs are not KEEP or stage approval.
5. Add adversarial concurrent claim/stage/race tests, expired-reservation tests,
   integration tests for launch failures and real host transition evidence. Have
   elected Chief review the exact final head, then perform bounded observed
   rollout. No second lane or portable execution is enabled by this checkpoint.

No spend, regeneration, upload, schedule, visibility or policy change occurred.

## Resume checkpoint — 4 November, 01:05–01:10 UTC

Added `portable_transfer.py`, a local filesystem transport adapter, disconnected
from worker launch and queue mutation. It copies an explicit SHA-256 manifest
into a new unique bundle, enforces total byte/file budgets, rejects traversal,
noncanonical/duplicate/colliding paths, symlinks and nonregular files, and hashes
the destination again. Failed copies remove only their newly created bundle.
Existing source files and bundles are never overwritten. No network transport
or unsupported laptop access is inferred: callers must supply readable local
roots, then verify on each consuming host.

Input/output receipts bind the complete contract digest, job, reservation token,
registered host identifier, direction, exact file manifest and byte count. They
expire after five minutes and require a local rehash on receipt consumption.
Input paths must match the contract; output paths must be scoped explicitly.
The shadow planner now rejects portable contracts without valid explicit output
paths. These receipts are integrity checks, not authenticated host registration,
KEEP, launch authorization or stage approval.

Validation: **188 tests PASS** (11 transfer, 25 capacity/observation, 31 workflow,
17 MacBook, 74 relay with fake CLIs, 30 queue), plus `git diff --check`. Transfer
tests include a local simulated outbound/return trip and changed returned bytes;
this is not real cross-host acceptance evidence.

Fresh observations: both repos pulled; HOS inbox had no new Codex messages.
`agent status` exited 0 with `Login successful!` and `Logged in (unable to fetch
user details)`. This does not prove current model/quota readiness and does not
clear the recorded execution authentication failure. Cached laptop heartbeat
was `2026-11-04T00:57:59Z`, generic `macbook`, idle, with no identity/resources/
account/capability proof. The initial sandboxed capacity observation could not
validate the process. Repeating with process visibility validated the Mini lease
for J1843, Codex, PID 44640, 01:04:22–01:30:22 UTC. It has legacy host/account
attribution (host defaults to Mini; machine name absent), so it cannot establish
shared-account spare capacity. Free-slot outlook remains unknown. Required
NAS offload ran with writable access and found nothing old enough to move;
about 13.4 GB remains free. No file was deleted on the NAS.

Existing plan remains **1/3**. Step 2 is incomplete: canonical cross-host
reservations/stage claims, process-validated per-host launches, host/account
probes and connecting verified bundles/receipts to the laptop worker still need
implementation. Continue on this same branch/job, preserving all current gates.
No extra lane, remote transfer, portable execution or rollout has been enabled.
Finish implementation before exact-head Chief review and observed transitions.

## Resume checkpoint — 4 November, 01:58 UTC onward

Continued the **same draft PR #437 and original branch** after merging current
main. The existing three-step plan remains **1/3**; no implementation or rollout
completion is claimed.

Added `capacity_reservations.py`: its `reserve_with_git` adapter uses the existing
canonical `jobs.with_git` compare-and-push retry transaction. Each attempt calls
the supplied evidence collector again. Reservations are stored on the original
job, with a two-minute lifetime, identity/head-bound idempotency token and an
explicit `reserved` phase. They do not claim a job, launch a worker or approve a
film stage. The planner recomputes host/account/worker/job/stage occupancy inside
the callback, includes other canonical reservations, and excludes current board
stage claims supplied by the collector. Exact-head review is mandatory even
for a single portable overflow lane. Rollback checks the token and owner and
cannot release an actual claimed job.

`workflow_state.claimable` now excludes a reserved job and other jobs on its
reserved film/stage, including ordinary `jobs.py next` calls. Expiry removes only
the capacity restriction; dependency, external, capability and Chief gates still
apply. **No production reservation caller exists yet.** The guarded transition
from reservation to an actual claim must still be implemented, including the
MacBook's `macbook` agent identity while preserving original routing eligibility.

Added `execution_leases.py`, a bounded, locked local process-receipt registry.
It binds PID to OS start time/command, rejects duplicate launches, validates the
host, writes atomically, and recovers confirmed dead or reused PIDs. A live
supervisor beyond its cap remains occupied/overdue: timer expiry alone never
proves spare capacity. Corrupt state fails closed. This is process evidence,
not a second production-state tracker. **No supervisor/launcher is connected.**
The existing relay still uses its original serial execution record and lock.

New tests cover transaction retries against a winning competing claim, exact
token replay, same-job and same-stage exclusion, board claims, reservation
expiry/rollback, a busy Chief plus independent specialist, portable reservation,
unavailable audio capability, local process identity, dead/reused PIDs, duplicate
supervisors, corrupt state, and a live supervisor beyond its cap. These are
synthetic transaction/lifecycle tests, **not actual two-host Git races or real
parallel launch acceptance**.

Validation on this continuation: **222 tests PASS** across capacity/observation/
reservation (36), local process leases (7), portable transfer (11), workflow (31),
handoffs (16), queue (30), relay with fake CLIs (74), and laptop worker (17).
`core_sync.py check` and `git diff --check` PASS. The local real-process test
initially failed because sandbox process visibility was denied; the complete
process suite passed with OS process visibility. No media perception inferred.

Fresh host observations:

- Both repos pulled. OWB thread read through #6620439840; HOS inbox had no new
  Codex messages. Disk had about 30 GiB free; no repair/offload was necessary.
- Process-visible capacity observation validated relay PID 12891 holding J1843,
  Codex, 01:58:09–02:24:09 UTC. Legacy lease has no registered machine/account
  attribution. The sandboxed observation cannot see that process and is not
  evidence of a free slot.
- A noninteractive `agent status` exited 0 and reported login success, with user
  details unavailable. No account details were printed. It did not test model
  quota or clear the latest execution authentication failure (recorded
  01:51:24 UTC, retry 02:51:24 UTC). No interactive login was opened.
- Refreshed `macbook-heartbeat`: 01:59:23 UTC, generic `macbook`, idle, no queued
  laptop job. It still lacks registered machine identity, power/idle/resource,
  per-model/account and media-capability evidence. No claim that the actual
  machine is an Air/Pro or that it is available. Free-slot outlook is unknown.

Remaining before review/rollout: connect a trusted fresh evidence collector;
consume reservations through canonical job and board claims with safe laptop
identity; connect capped per-host supervisors without removing the serial lock
early; integrate supported input/return transport and receipt checks into the
laptop worker; test actual Git races and launch failures; then obtain exact-head
Chief review and observe real host transitions. No default lane, service, spend,
generation, upload, schedule or visibility change was made. This remainder is
larger than the capped run and stays on J1843, ready for continuation.

## Resume checkpoint — 4 November, 03:10–03:18 UTC

Resumed the existing draft PR **#437**, branch `codex/J1843-capacity`, in a
clean worktree `/private/tmp/J1843-resume`; merged current main. The older
`/private/tmp/j1843-capacity` worktree has unrelated unfinished checkpoint
files and was left untouched. Existing plan remains **1/3**: the implementation
step is still incomplete, and this is not a rollout or approval.

Added `consume` / `consume_with_git` to `capacity_reservations.py`. The adapter
recollects evidence on every canonical Git transaction attempt, binds the
reservation token to its host, specialist, reviewed head and account, and
recomputes current priority, board-stage exclusions, host resources, laptop
power/idle, shared account quota, model readiness, dependencies, external holds
and capability requirements. It then uses the normal queue claim operation.
If a newly higher-priority eligible job wins, the old reservation must be
replanned rather than silently taking a different job.

A portable claim records **macbook** as its canonical owner while retaining
the actual specialist/account/host in reservation metadata. The original
`needs` and `for` routing restrictions are preserved. A busy specialist or
MacBook owner cannot gain another claim. Successful OWB stage claims use
`jobs.board_claim` and return the board path to the same Git transaction.
A stage conflict restores the queue candidate; exact claim acknowledgements
are idempotent and do not restart a board stage. HOS film claims are explicitly
rejected until there is a supported HOS board transaction adapter. Unmapped
HOS CPU work remains subject to the same no-spend/no-publish restrictions.

Also fixed reservation token replay: an existing token cannot be acknowledged
as a reservation after its job has been claimed or its reservation consumed.
Claim acknowledgement remains separate from supervisor/launch permission.
**No production caller, additional lane or launcher has been enabled.**

Validation:

- **236 tests PASS** in the full focused capacity/claims/local-Git-race/process/
  transfer/workflow/handoffs/queue/relay/MacBook suite, followed by one additional
  real OWB board-write test (**14 claim tests PASS** including that addition).
  Thus the current focused set contains **237 tests**; the full suite was not
  rerun merely for the added isolated board test.
- The new race test runs two processes against two disposable local clones
  and a real local bare Git remote. Both first attempts read the same head;
  one push wins and the other transaction retries/recollects evidence. It
  tests same-job and same-film/stage conflicts with distinct specialist workers
  and enough shared-account capacity to ensure the stage restriction matters.
  Only one reservation is committed; neither process claims or launches work.
  This is actual Git contention on one machine, **not real two-host rollout**.
- New claim tests cover normal claim/replay, competing ownership, changed
  priority, hold/dependency/capability/account/model/stage failures, MacBook
  identity and in-use rejection, real OWB board writes, board conflict rollback
  and a competing claim between transaction attempts. No paid CLIs or publishing.
- `core_sync.py check`: PASS (56 shared files); `git diff --check`: PASS.

Fresh observations: the process-visible capacity command validates the sole
Mini execution lease for J1843, owner Codex, through 03:35:59Z. Its machine and
account attribution remain legacy/unverified, so no spare shared-account slot
is inferred. Cached MacBook heartbeat 03:00:43Z says generic `macbook`, idle,
no queued laptop job, and still lacks registered identity/resource/account/
media proof. Actual laptop power/idle and Air/Pro identity remain unverified.
A noninteractive Cursor `agent status` exited 0 reporting login success and
unavailable user details; it did **not** prove current model quota or clear the
recorded execution authentication failure. No identity or secret was printed.
Disk has about 31 GiB free; no repair/offload needed. Audio/moving-video
capability report is empty. Free-slot outlook remains **unknown**.

Next on **this same job/PR**: implement the trusted host/account evidence path,
HOS stage transaction adapter where needed, capped supervisor integration and
failure recovery, and supported laptop outbound/return transport with consuming
host rehashes. The laptop must recheck guards immediately before launch. Retain
the serial lock until the full replacement has passed. Then obtain exact-head
Chief review and observe real host transitions before enabling capacity. This
remaining integration is larger than the capped run, so release J1843 at this
clean, tested checkpoint; do not close it or create a duplicate follow-up.
No spend, media regeneration or publishing state changed.


## Resume checkpoint — 4 November, 04:22 UTC

Recovered committed PR437 head c1fb2d0205 into the clean worktree
`/private/tmp/J1843-run` on the existing `codex/J1843-capacity` branch. The older
`/private/tmp/j1843-capacity` worktree contains uncommitted historical files and
was left untouched. Neither of the earlier documented temporary resume paths
still existed. The original plan remains **1/3**; implementation is unfinished.

Added `capacity_supervisor.py`, an internal local lifecycle adapter with no CLI,
production caller or change to the relay's serial lock. It requires a freshly
read canonical claimed reservation, matching host/account/owner, matching
reviewed and installed head, and the original unexpired launch window. It only
accepts explicitly scoped CPU assembly/chart work with no-spend/no-publish
flags; Chief/review work is excluded. Trusted guard and local input-rehash
callbacks are mandatory, with guards and ownership checked before launch and
while the child runs. This is not an operating-system sandbox: the eventual
caller still must select an approved command and prohibit detached child escapes.

A process-validated exclusive lease precedes spawn. Durable per-token launch
seals prevent replay after completion or launch failure. Child commands use an
explicit absolute executable, no shell, closed stdin, an exclusive log and a
new process session, capped at 1500 seconds. Timeout, guard loss, canonical
cancellation and exceptions clean up the process group before freeing the
local lease. Nonzero exits remain explicit receipts; no receipt completes a
queue job or accepts outputs. A failed attempt requires explicit reconciliation
and a new canonical reservation rather than deleting its seal to retry blindly.

`Registry.arm` persists possible-child state before spawning. If the supervisor
dies after that point, the slot remains quarantined with `recovery_required`
and `process_validated=false`, rather than becoming spare capacity. Automatic
orphan process-group reconciliation is **still unimplemented** and blocks
rollout; remote host evidence must also refuse quarantined/unknown capacity.
A real subprocess test kills a supervisor after its harmless child starts,
observes quarantine, and explicitly cleans up that test child. Other real
subprocess tests cover successful/nonzero exit, timeout, descendant cleanup,
guard loss, cancellation, launch failure and replay. No model or paid tool runs.

Validation: capacity suite (including the supervisor), execution leases,
portable transfer, workflow state, dispatcher handoffs, queue, relay (fake
worker CLIs) and MacBook worker suites all PASS. Supervisor has **16 tests**;
execution leases has **8**. Core sync check: PASS (56 shared files). Python
compilation and whitespace checks PASS. Initial sandboxed process probes were
rejected, then the process tests passed with OS process visibility enabled.
These remain local tests, not actual two-host rollout evidence.

Fresh observation: PR-only `chief_relay.py capacity` validated J1843's sole Mini
execution lease, Codex, ending 04:47:43Z, with legacy/unverified machine/account
attribution. Cached laptop heartbeat was 04:17:23Z, generic `macbook`, idle,
no laptop job waiting, already stale at observation (~494 seconds). It lacks
registered identity, resources, mains/idle and account/model/capability proof.
Current relay status still records Cursor's last execution authentication error;
no model/quota success, cleared sign-in or spare account slot is inferred. Free
slot availability is **unknown**. About 28 GB disk free; no repair/offload needed.
Audio/moving-video capabilities remain undemonstrated. Both repositories pulled;
HOS Codex inbox was empty; thread read to #6622443242.

Next on this same job/PR: trusted registered-host/account observations, capped
supervisor integration and automatic orphan reconciliation, supported laptop
outbound/return receipt consumption, and HOS stage transactions where needed.
Then exact-head Chief review and observed real host transitions. This remaining
integration exceeds the bounded run, so release J1843 at a clean checkpoint.
No extra lane, production launch, portable dispatch, spend or publishing enabled.

## Resume checkpoint — 4 November, 05:24 UTC onward

Continued the existing PR437 branch in `/private/tmp/J1843-run`, merged current
main, and preserved the original **1/3** plan. Step 2 remains unfinished.

Added conservative local orphan recovery to the internal supervisor adapter.
The registry durably attaches the child's PID and birth-time identity after
spawn. A later launch attempt can reconcile a confirmed dead supervisor's
recorded child group, signal only its matching live leader, and free the local
slot only after observing no executing group members. The real local regression
kills a supervisor, verifies quarantine, then launches a distinct canonical
token through recovery; both durable launch seals survive and the queue claim
remains unchanged. macOS Python's executable trampoline required child birth
time rather than command path as the stable identity across exec.

Recovery deliberately leaves unknown arm/spawn/attach gaps, a missing/reused
leader with surviving descendants, denied probes and unconfirmed cleanup
quarantined. It does not infer a child from command text or kill a live/overdue
supervisor. Invalid registry records now fail closed. Process probe failure is
distinct from confirmed absence. The planner's lease filter no longer discards
live overdue leases or stale remote evidence; uncertain occupancy blocks new
proposals on that host. Remote recovery must happen on that remote host.

Validation: **265 tests PASS** across the complete focused suite before the
last malformed-registry guard, then **18 lease tests and 16 supervisor tests
PASS** on the final code. Capacity planning/reservation/claim/Git-race tests are
included in the full run. Core sync (56 files), whitespace and compilation pass.
All subprocesses/worker CLIs in these tests are local harmless tests/fakes;
none spend credits, review media or establish real two-host rollout readiness.

Fresh observations: both repos pulled; HOS Codex inbox empty; Mini disk about
22 GiB free. Process-visible capacity report finds only this J1843 Codex lease,
ending 05:49:27Z, with legacy machine/account attribution. Cached generic
MacBook heartbeat 05:18:45Z was already stale (~592 seconds); identity,
power/idle/resources and account/model/capability readiness remain unverified.
Cursor's noninteractive status exits 0 and reports login success with user
details unavailable; model/quota execution was not tested. This does not prove
spare account capacity or clear an earlier execution failure. Audio/moving-video
capability remains undemonstrated. Free-slot outlook remains unknown.

Next on this same job/PR: trusted fresh registered-host/account evidence,
production supervisor/claim integration, supported laptop outbound/return
receipt consumption and HOS stage transactions where needed, then exact-head
Chief review and observed host transitions. Unidentifiable orphan gaps still
require an explicit recovery decision. The remaining integration exceeds the
capped run; release at this tested checkpoint. No production caller, extra lane,
portable execution, spend or publishing has been enabled.

## Resume checkpoint — 4 November, 06:24 UTC onward

Resumed the same branch and draft **PR437** at b07a54ea62 in clean worktree
`/private/tmp/J1843-resume`, merging current main. The initial progress command
mistakenly reset the plan; it was corrected immediately after recovering the
history. The original plan remains **1/3**, and implementation is unfinished.
The older dirty `/private/tmp/j1843-capacity` worktree was left untouched.

Added `capacity_evidence.py`, the read-only **local** evidence consumer. It reads
only explicit `registration.json` and `probes.json` files through directory file
descriptors. The directory and files must belong to the current OS user, with
no group/other permissions. Symlink roots/files, nonregular files, oversized
JSON, nonfinite values and malformed objects are rejected. This is an OS-user
trust boundary, **not remote authentication or protection against other code
running as that same user**. No registration or readiness receipt is created
automatically, no existing outage is cleared, and no sign-in/model call runs.

Registration is approval-reference-bound, expires within 30 days, and matches a
SHA-256 hardware fingerprint observed on the consuming Mac. The raw hardware
UUID is never returned. It explicitly binds host role, capacity/resource limits,
worker models and shared-account aliases/limits. Probe receipts have separate
freshness checks for host, worker and account, plus explicit auth, verified-model
and quota evidence. A login-only read cannot supply the model/quota success
receipt. Media capabilities additionally need their own fresh host/worker-bound
probe; text execution never becomes listening/motion proof. No laptop identity,
account, capability or spare slot is inferred from a generic heartbeat.

macOS measurements use local disk, load, mains power, HID idle time and a
**conservative** free-plus-speculative memory-page count. This excludes inactive,
compressed and purgeable RAM; it is not the machine's total usable memory.
Missing idle data now rejects the laptop rather than raising a comparison error;
malformed freshness receipts also fail closed.

`chief_relay.py capacity` now exposes sanitized local measurements and explicit
unverified/rejected evidence status. Optional `CAPACITY_EVIDENCE_ROOT` selects
an existing private evidence directory for this read-only command. Without it,
registration stays unverified. It never emits receipt contents, auth diagnostics,
hardware UUID/fingerprint, or private evidence paths. It never claims a slot:
`dispatch_enabled=false`, availability unknown and no free-slot timestamp remain
explicit even when evidence is observed. Installed-head lookup rejects dirty
tracked files and uses the full Git commit, never the truncated runner digest.
The runner digest now includes all capacity implementation dependencies so edits
to those modules cause the existing safe-boundary restart check to notice them.

### Local receipt contract (not an enabled configuration)

- `registration.json`: version 1; `at`/`expiresAt` (at most 30 days apart);
  `approved_by`/`approval_ref`; registered `host` and role `mini` or `macbook`;
  `machine_fingerprint` (SHA-256 of the locally observed hardware UUID);
  bounded `configured_limit` (1–8), positive `min_free_gb`, `max_load`,
  `min_memory_gb`; `workers` mapping each specialist to `account` and approved
  `models`; `accounts` mapping each shared-pool alias to its bounded limit.
  Additional lanes retain `capacity_review` and exact `reviewed_head` checks.
- `probes.json`: host/fingerprint binding, fresh `at`/`expiresAt`; `workers`
  mapping with its own fresh timestamps, `account`, `ready`, sanitized
  `auth_evidence` and `verified_models`; `accounts` mapping with separate fresh
  timestamps, `ready`, sanitized `quota_evidence` and matching `limit`.
  A producer must base these on actual observations and retain account/model
  failure chronology; no producer or outage reconciliation is installed here.
- Optional worker `capabilities`: own fresh timestamps, `host`, `worker`, actual
  probe `evidence`, and demonstrated `available` identifiers. The only supported
  media identifiers are `audio_input` and `moving_video_input`.
- Producers must keep shared Codex Mini/laptop usage under **one** approved
  alias/limit. Changing host or relabeling a worker receipt cannot create quota.
  Remote receipt transport/authentication, input receipt consumption and the
  canonical queue/lease evidence collector remain separate unfinished work.
- Call `collect` again on each queue transaction attempt and immediately before
  launch. The caller must also collect current canonical claims, validated
  process occupancy, board stages, elected Chief and outage evidence. The
  internal host `state` is for resource-guard compatibility, **not proof that a
  machine is idle**; only the lease collector can establish occupancy.

Fresh observations in this continuation: both checkouts pulled, HOS Codex inbox
empty and OWB thread had no unread messages. The sole process-visible Mini lease
is J1843, Codex, ending 06:50:10Z, with legacy/unverified machine/account
attribution. The cached generic laptop heartbeat was 06:20:01Z and already stale
when inspected; it has no registered identity, power/idle/resources, account or
media proof. Mini measurements succeeded (arm64, approximately 28 GiB disk free,
load around 1.5–2.3, on mains, long HID idle); conservative free-plus-speculative
memory was about 0.44–0.47 GiB. These measurements authorize no extra lane.
Cursor's noninteractive status returned 0 and reported login success with user
details unavailable; no model/quota execution was tested or outage cleared.
No audio/moving-video perception was demonstrated. Free-slot outlook is unknown.

Remaining on **this same job/PR**: trusted receipt producers and outage chronology;
registered laptop evidence and supported authenticated transport; assembling
legacy plus new process occupancy and both channel board claims inside the
canonical transactions; production supervisor/claim integration; portable
outbound/return receipt consumption; explicit unknown-orphan recovery decisions;
then exact-head Chief review and observed real-host transitions. The serial lock
and disabled rollout remain. This remainder exceeds a bounded unattended run.
No production launcher, extra lane, portable execution, spend, media generation,
YouTube/Buffer write, policy change or approval occurred.

Validation on this checkpoint: **285 tests PASS** on final code: 88 capacity
(including 19 new evidence-reader/report tests) plus 197 execution-lease,
portable-transfer, workflow, handoff, queue, relay and MacBook tests. The relay
suite uses fake CLIs, and process/Git races use harmless local fixtures; none is
real host rollout proof. `core_sync.py check` PASS (56 shared files), Python
compilation PASS and `git diff --check` PASS. Final thread check: read through
#6624168164. No final implementation PASS, merge or rollout decision was made.

## Resume checkpoint — 4 November, 08:20–08:33 UTC (Gemini)

Resumed the existing draft **PR437**, branch `codex/J1843-capacity`, in clean
worktree `/private/tmp/J1843-gemini` and merged current `origin/main`. Completed
the remaining Step 2 engineering adapters while keeping rollout disabled by
default (`rollout_enabled=False`) pending exact-head Chief review and observed
real-host transitions:

1. **Trusted local receipt producer & outage chronology (`capacity_evidence.py`):**
   - Added `produce_probes(...)` to write identity-bound `probes.json` atomically
     (`0o600` inside the user-owned `0o700` evidence directory) from verified
     execution receipts and recorded outage chronology.
   - Enforces strict outage chronology: an active or newer outage timestamp
     (`obs_at <= outage_at`), an expired retry timer (`retryAt <= at`), or a
     login-only check (`login_only=True`) never produces a `ready=True` worker or
     account receipt.
   - Shared-account quota failures (`out_of_usage=True` or `account_wide=True`)
     taint the shared account pool across all workers bound to that account alias.
   - Scrubs and rejects secret-like strings (tokens, bearer strings, API keys,
     email addresses) before writing receipts.
   - Added `board_stage_claims(...)` and `transaction_evidence(...)` to assemble
     fresh timestamps, exact Git head, local host/account evidence, local
     `Registry.observe(at)` process leases, legacy serial `execution.json` leases
     (preserving unattributed legacy lease blocking of spare shared-account
     capacity), remote host/lease records, and both OWB and HOS board stage
     claims on every canonical Git transaction retry.
2. **Explicit unknown-orphan quarantine resolution (`execution_leases.py`):**
   - Added `Registry.resolve_quarantine(...)` requiring explicit `approved_by`,
     `approval_ref`, and `reason`, verifying that the supervisor PID is dead and
     any recorded `child_pid` process group has no executing members, and writing
     an immutable audit receipt under `<host>-quarantine-resolutions/` while
     preserving the durable launch seal in `<host>-launches/`.
3. **End-to-end portable outbound/inbound/return adapters (`portable_transfer.py`):**
   - Added `stage_outbound(...)`, `input_receipts_map(...)`, `preflight_inbound(...)`,
     `stage_return(...)`, and `consume_return(...)`.
   - Consuming-host preflight rehashes every approved input file and rejects any
     unexpected files before execution. Return consumption on Mini verifies the
     output receipt, rejects unexpected or missing files outside `contract["outputs"]`,
     and copies verified outputs into an isolated review bundle with
     `stage_approved=False`, `keep_approved=False`, and `job_completed=False`.
4. **Canonical reservation rollback, HOS board adapter & launch pipeline (`capacity_reservations.py`, `capacity_supervisor.py`):**
   - Added `cancel_with_git(...)` and optional `hos_board_claim` transaction
     callback support in `consume_with_git(...)` (preserving fail-closed rejection
     of HOS film stages when no HOS board transaction adapter is supplied).
   - Added `dispatch_claimed(...)` in `capacity_supervisor.py` connecting
     `reserve_with_git` -> `consume_with_git` (with automatic `cancel_with_git`
     rollback on claim failure) -> supervised `run(...)` with portable inbound
     receipt preflight, gated behind `rollout_enabled=False` by default and
     requiring `installed_head == reviewed_head` plus `rollout_approval_ref`.

Validation on this checkpoint: **292 tests PASS** across the complete focused
capacity/evidence/claims/Git-race/supervisor (92), execution-lease (19),
portable-transfer (13), workflow (31), dispatcher-handoff (16), queue (30),
relay with fake CLIs (74), and MacBook worker (17) suites. `core_sync.py check`
PASS (56 shared files), `py_compile` PASS and `git diff --check` PASS.

Fresh observations at `08:31Z`:
- `chief_relay.py capacity` validated the sole Mini execution lease (`J1843`,
  owner `gemini`, ending `08:45:33Z`). Local Mini resource measurements succeeded
  (`arm64`, `27.76 GiB` free disk, load `2.04`, `1.38 GiB` free+speculative RAM,
  on AC power). Cached MacBook heartbeat (`08:22:38Z`, age ~548s) remains generic
  `macbook`, `idle`, unverified (`macbook_capacity_verified=false`,
  `availability="unknown"`, `free_slot_at=null`).
- `chief_relay.py status` shows Codex has recovered from its retry window and is
  once again the higher-priority elected acting Chief (`Chief: Codex`). Per the
  acting-Chief handback rule, Step 3 (`exact-head Chief review and observed real
  host transitions`) is handed back to Codex on this same job and PR #437 with
  progress advanced to **2/3**. No rollout, extra lane, spend or publishing was
  enabled.

## Re-verification and Chief review handoff — 4 November, 10:02 UTC (Gemini)

- Merged latest `origin/main` into `codex/J1843-capacity` in `/private/tmp/J1843-gemini`
  and re-verified all focused suites (**292 tests PASS**: 92 capacity/evidence/claims/Git-race/supervisor,
  19 execution-lease, 13 portable-transfer, 31 workflow, 16 dispatcher-handoff,
  30 queue, 74 relay with fake CLIs, and 17 MacBook worker tests), plus
  `core_sync.py check` PASS (56 shared files), `py_compile` PASS and
  `git diff --check` PASS.
- Fresh `10:01Z` observations from `chief_relay.py capacity`: sole process-validated
  Mini lease is `J1843` (`owner="gemini"`, `lease_expires_at="2026-11-04T10:22:44Z"`);
  local Mini resource measurements (`arm64`, `27.15 GiB` free disk, load `1.58`,
  `0.47 GiB` conservative free+speculative RAM, `on_ac=true`); cached MacBook
  heartbeat (`09:54:37Z`, age ~384s) remains generic `macbook`, `idle`,
  `macbook_capacity_verified=false`, `availability="unknown"`, `free_slot_at=null`.
- Parked `J1843` with `jobs.py block J1843 --agent gemini --reason "parked for Chief: ..."`
  so that `workflow.state(J1843)` transitions to `"review"` and enters `Chief duties`
  for the elected acting Chief (`Codex`) for Step 3 (`exact-head Chief review and
  observed real-host transitions`), instead of remaining `open` (`for: gemini`) in
  the specialist worker queue. Rollout remains disabled (`rollout_enabled=False`).

## J2010 exact-head review FIX and PR477 composition — 4 November, 11:46 UTC (Gemini)

- Addressed the J2010 review finding on `capacity_reservations.consume_with_git`:
  - Removed the one-way `hos_board_claim` callback from `consume_with_git` and
    `dispatch_claimed`, and excluded HOS film-stage jobs (`repo == "hos"` with
    `film` set) across `dispatch_capacity.propose`, `capacity_reservations.reserve`,
    `capacity_reservations.consume`, and `capacity_reservations.consume_with_git`
    until a cross-repo HOS transaction adapter exists. Unmapped HOS CPU work
    (`film=""`) remains subject to the normal no-spend/no-publish CPU guards.
  - Added retry-safe board-file rollback (`rollback_board`) inside
    `capacity_reservations.consume_with_git` for OWB film-stage claims so that if
    an attempt writes `status.json` via `jobs.board_claim` and the OWB push
    attempt is rejected or fails, `status.json` is restored to its pre-attempt
    bytes before the retry recollects `board_stage_claims` (and before returning
    if the transaction fails).
  - Added push-race regression tests in `scripts/test_capacity_claims.py`
    (`test_hos_stage_needs_explicit_board_adapter`,
    `test_owb_board_claim_push_race_rolls_back_before_retry_and_on_rejection`)
    and `scripts/test_capacity_git_race.py`
    (`test_consume_board_claim_push_race_rolls_back_and_succeeds_on_retry`,
    running two real Git clones against a local bare remote where a competing
    push forces `consume_with_git` attempt 1 to fail its push, roll back its
    board claim, pull/rebase, refresh `board_stage_claims` from disk, and
    succeed cleanly on attempt 2).
- Composed with merged PR477 (`d12b004c67` / `b76bf04ba8`) on `origin/main`:
  - Composed runtime digest (`chief_relay.installed_version()`): `cfac198462093c03`
  - **313 focused tests PASS**: 94 capacity/evidence/claims/Git-race/supervisor
    (69 in the `test*capacity*.py` subset when excluding `test_capacity_evidence`
    or 94 across all 6 `test*capacity*.py` files), 19 execution-lease, 13
    portable-transfer, 34 workflow-state (including PR477's 3 `taskKeys`
    priority tests), 17 workflow-handoff, 17 dispatcher-handoff, 30 queue,
    15 MacBook worker, and 74 relay tests (fake worker CLIs).
  - `core_sync.py check` PASS (56 shared files), `py_compile` PASS, and
    `git diff --check` PASS.
- Fresh `11:46Z` observations from `chief_relay.py capacity` and `chief_relay.py status`:
  - Sole process-validated Mini lease is `J1843` (`owner="gemini"`,
    `lease_expires_at="2026-11-04T11:58:21Z"`); local Mini measurements (`arm64`,
    `24.28 GiB` free disk, load `1.83`, `0.59 GiB` conservative free+speculative
    RAM, `on_ac=true`, `state="unverified"` because private host registration and
    probe receipts are not configured).
  - Cached MacBook observation (`11:28:14Z`, age ~1123s, stale) reports
    `state="waiting"`, `why=["on battery", "in use (0 min idle, needs 10)"]`,
    `macbook_capacity_verified=false`, `availability="unknown"`, `free_slot_at=null`.
  - Preserve progress **2/3** (`rollout_enabled=False`) and park `J1843` for
    exact-head Chief review of the new composed head.

## Engineering continuation — 4 November, 19:41 UTC onward (Codex)

Continued only J1843 on existing PR437 in the clean worktree
`/private/tmp/J1843-callers`, merging current main. Plan remains **2/3**;
production caller integration and observed rollout are still unfinished. No
completion PASS, merge, second lane or enablement is claimed.

Two prerequisite defects are fixed in this checkpoint:

- `dispatch_claimed` now reconciles a consumed canonical claim after a
  supervisor/preflight/launch exception. `release_failed_with_git` requires the
  exact token/host/specialist/claimant and rereads local cleanup on every Git
  retry. It reopens the queue and releases the matching OWB board stage to todo
  only after the token has no occupying local lease. Changed ownership, uncertain
  cleanup or quarantine preserves the claim. A failed canonical cleanup leaves
  an immutable `<host>-reconciliation/<sha256(token)>.json` local receipt with
  `canonical_cleanup_required`; it contains exception types, not private error
  diagnostics. No output becomes approved or complete. HOS film stages remain
  excluded. Queue-push races roll back board-file writes before retrying.
- A real local bare-remote reproduction demonstrated that the reservation's own
  canonical commit changes literal Git HEAD, making the next claim reject its
  review identity. `reviewed_installation` keeps the full reviewed SHA as the
  code identity only for a clean descendant whose changes are confined to
  `jobs/queue.json`, `JOBS.md`, `STATUS.md`, and per-film `status.json` files.
  Source, rule, review, configuration and approved-input changes invalidate that
  identity. `transaction_evidence` now uses this checked identity on each retry.
  The real-Git reserve -> consume -> failed-attempt release regression succeeds;
  dirty tracked state and an unreviewed source commit are rejected. This is an
  engineering proposal for exact-head review, not authority to enable it.

Validation at this checkpoint: 98 focused capacity tests, 19 execution-lease,
12 portable-transfer and 30 canonical queue tests PASS. Core sync (56 files),
Python compilation, STATUS.md consistency and whitespace checks PASS. Capacity
process tests require process visibility; the initial sandboxed run could not
execute `ps`, and the process-visible rerun passed. Related serial-relay/laptop
and workflow regression results are recorded with the final report.

At about 19:45Z, the only observed Mini execution was this Codex J1843 run, with
configured lanes=1. Private host registration/probe receipts are absent. The
cached generic MacBook heartbeat (19:33Z) was stale and did not establish host
identity, power/idle, account or capability readiness. Availability/free-slot
outlook stays unknown. No audio/moving-video perception was demonstrated.
Both repos pulled; HOS Codex inbox empty. NAS scratch offload found nothing old
enough to move; disk remains about 11.5 GiB free. No NAS content was deleted.

Continue **this same J1843 / PR437**, without a duplicate job or timed hold:
implement the disabled production callers in `chief_relay.py` and
`macbook_worker.py`, with supported consuming-host input/output receipt
transport, fresh per-host account/capability evidence, failure-receipt
reconciliation, and preserved serial fallback. Use `reviewed_installation` for
both transaction and launch identity; do not pass raw post-reservation HEAD as
though it were the reviewed release. Add actual caller-level success,
launch-failure and changing-laptop-guard regressions. Then exact-head review,
green CI and observed real-host acceptance are required before enablement.
The remaining integration exceeds another bounded 20-minute work segment, so
release at this tested checkpoint. There is no external date/input hold on
engineering that can proceed now. No spend, media generation, YouTube/Buffer
write, publishing or policy change is authorized or performed.
