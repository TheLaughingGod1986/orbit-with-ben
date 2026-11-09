# J1887 — Mini dispatcher rollout validation

Codex, 3 November 2026, actual host `Benjamins-Mac-mini.local`. Operational checks sampled 20:28–20:30Z. This validates the bounded serial-dispatch rollout; J1843 remains open for measured parallel capacity and portable MacBook overflow.

## Source and runtime: verified

- PR425 reviewed head: `64e8332e17e27dbd1649480d2f1d449e21b2d735`. GitHub reports MERGED at 20:23:23Z as `c9b3e24f79e7eba53767b580cdc314eb4d40ce36`. That exact head has Rules check SUCCESS (20:18:10Z) and Studio core check SUCCESS (20:06:41Z), plus the recorded elected-Chief PASS and predecessor J1886 completion.
- Mini initial pull: already up to date. Source at first milestone: `1b06353e0b` (queue-progress commit descended from the merge). Tracked checkout was clean; many existing untracked production artifacts were present and left untouched. Report written from a separate clean worktree.
- All six fingerprint inputs (`chief_relay.py`, `workflow_state.py`, `workflow_handoffs.py`, `studio.py`, `jobs.py`, `routing.py`) and `board_publish.py` byte-match the merged source.
- Installed, loaded and desired runtime versions all equal `672fbdd6a32d7c9c`. Runner PID 64182 is live under launchd (PPID 1). `execution.json` names J1887, worker codex, start 20:28:04Z, expiry 20:54:04Z, matching version. `current_execution()` validated the lease with a host process probe. The initial sandbox probe could not inspect processes; repeating with authorized host access succeeded. No worker was interrupted or lock forced.

## Actual dispatch and claim history

The relay log, canonical queue and runtime lease establish separate events:

| UTC | Observed event |
|---|---|
| 20:26 | J1886 canonical done, with exact-head PASS and narrowly typed listening holds |
| 20:26:20 | Relay logs J1886 Codex exit 0, checks remaining jobs, then yields at a safe boundary for fresh source |
| 20:27:41 | Fresh runner launches Cursor for J1887 |
| 20:27:44 | Cursor exits 1 with authentication failure; marked temporarily unavailable |
| 20:27:47 | Same runner reroutes J1887 to Codex on gpt-6.1-sol |
| 20:28:03–04 | Codex launched; current execution lease created |
| 20:28 | J1887 actually claimed by codex; ETA 20:43Z |

This proves safe-boundary reload, real next-job pickup, and immediate failure fallback. The approximately one-minute launchd boundary was required to load new code, not an unexplained dispatch stall. It does **not** prove a live released-job continuation under the new version: J1887 is still running during this observation. That behavior is covered by isolated tests. `runs.jsonl` currently records the earlier launches/outcomes; its `at` is launch time, not completion time. No completion row for this active Codex run is claimed.

## Tests and board: verified

Executed on installed matching source:

```text
PYTHONPATH=scripts python3 -m unittest scripts.test_dispatcher_handoffs
Ran 17 tests in 0.050s
OK
```

These tests use temporary queues/fake CLIs. They cover released/terminal-task continuation, ordinary worker failure fallback, task-local recorded outcomes, capability/role waits and progress preservation. Their fixture log includes the legacy repeated-check stop deliberately; it is not production evidence.

The existing board publisher refreshed `board.json`: workflow at 20:29:17Z shows J1887 running under codex, with actual progress timestamp 20:29Z. A read-only recomputation through `board_publish.dispatch_snapshot` agrees. The existing board check at 20:28:17Z reports `ok: true`, no problems, site 200. No board deployment was manually triggered.

J1752 and J1753 both remain blocked/waiting, technical progress 1/3, with `hold.type=capability`, `hold.requires=[audio_input]` and `required_capabilities=[audio_input]`. Their full listening conditions, history and prior evidence remain present; next checks remain 4 November 00:55Z and 01:20Z respectively. Neither was reopened, listened to, approved or completed. A read-only eligibility probe rejects Codex for both: `Waiting for verified capability: audio_input`.

Session tool inspection demonstrated text execution and still-image viewing only. Codex recorded an empty available-capabilities report at 20:28:34Z, expiring 20:58:34Z, with that evidence. No audio or moving-video perception is asserted. Missing/expired/future/different-owner capability/outcome handling is covered by the installed tests and exact merged code, not fabricated live capability reports.

## Remaining limits and next owner

Bounded rollout verification is complete. Normal report PR review/merge remains with the elected Chief; existing relay continues after this one-job run exits. No second task was selected by this worker. J1843 remains open; concurrent host capacity and MacBook spillover are unimplemented/unvalidated by this job. Cursor's real authentication failure remains an existing availability issue; no sign-in was attempted. Actual listening still requires an audio-capable elected Chief for J1752/J1753. No media, Buffer, publishing, spend, approval or film-stage state changed.
