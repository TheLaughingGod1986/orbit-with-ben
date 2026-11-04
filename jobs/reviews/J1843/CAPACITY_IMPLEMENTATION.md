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

1. Continue step 2 of the existing three-step plan. Integrate reservations into
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
