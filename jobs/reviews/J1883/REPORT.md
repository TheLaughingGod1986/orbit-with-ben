# J1883 — Read-Only Validation of Merged Buffer Repair (PR #422)

Gemini covering (elected acting Chief), authenticated Mac mini, 3 November 2026 (`19:18–19:22Z`).
Linked jobs: `J1870`, `J1874`, `J1878`.

## 1. Installed Source & LaunchAgent Verification

- **Installed repository checkout:** `/Users/benjaminoats/YouTube/orbit-with-ben` on `main`, fast-forward clean for tracked files (`git diff --stat` empty; `git merge-base --is-ancestor a65e83e53466bf33823e85cdba09d474f1b7a2b5 HEAD` PASS at `edb0a09fa1f9fb576c34119ebf9b7cd51e364778`).
- **LaunchAgent path:** `launchctl print gui/$(id -u)/dev.orbit.buffer-check` confirms `/Users/benjaminoats/Library/LaunchAgents/dev.orbit.buffer-check.plist` executes `/bin/zsh -lc /Users/benjaminoats/YouTube/orbit-with-ben/07_Content-Ops/launchd/buffer-check.sh`.
- **Installed `07_Content-Ops/launchd/buffer-check.sh`:**
  - SHA256: `961a5615a07b845712612fc2bb7f1ad1ad66f8411bb901184e0de10f1dd90808`
  - Git blob SHA: `ede04d12845d186a8156aae5c3cae90d8a8762d1`
  - Contains direct CLI invocations (`npx tsx --env-file=.env scripts/buffer-mirror.ts check` and `npx tsx --env-file=.env scripts/buffer-mirror.ts check --channel hos`) with the outer `desk-lock.sh` wrapper removed so the CLI owns the single whole-operation lock without self-deadlocking.
- **Unit & regression suites:**
  - `python3 07_Content-Ops/tests/desk-lock.test.py`: 6/6 PASS (`exit 0`).
  - `npx vitest run tests/buffer-recovery.test.ts`: 10/10 PASS (`exit 0`).
  - Live isolated contention check (`DESK_LOCK_ROOT` temp dir with an active holder on `youtube-buffer`): `npx tsx --env-file=.env scripts/buffer-mirror.ts check --dry-run` refused immediately with `exit 75` (`EX_TEMPFAIL`).

## 2. Direct Authenticated Read-Only Dry Runs (`--dry-run` only)

`buffer-check.sh` was **not** invoked and the daily LaunchAgent was **not** restarted. Both profiles were checked directly from `07_Content-Ops` in `--dry-run` mode:

| Profile | Command | Exit code | `checked` | `changes` | `autoMirrored` (`sent: false`) | `deferred` | `unmirrored` (explicit source holds) |
|---|---|---:|---:|---:|---|---:|---|
| **OWB** | `npx tsx --env-file=.env scripts/buffer-mirror.ts check --dry-run` | `1` | 24 | `[]` | `Js6EQJ8qDi8` (*Could a Robot Survive on Mars?*, discovered via `UPLOADS.json`) | 21 | `iyvWYFP_ETA` (*Could a Robot Survive a Night on Mars?* — approved original unavailable after `J0432` seam fix; `J1181`, `J1320`) and `RLSJm59OSzI` (*What Would Standing on Saturn's Moon Titan Feel Like?* — social source SHA256 mismatch) |
| **HOS** | `npx tsx --env-file=.env scripts/buffer-mirror.ts check --channel hos --dry-run` | `0` | 11 | `[]` | `PFj6172YU4Q` (*One Tight Band Proved Your Blood Goes Round*, via `social/hos/UPLOADS.json`) | 4 | `[]` |

Full redacted dry-run JSON outputs are saved in `owb-check-dry-run.json` and `hos-check-dry-run.json`.

## 3. Hold & Scope Preservation

- **Zero writes executed:** `sent: false` on both dry runs; `00_Brand/Channel-Setup/social/` and live R2/Buffer/YouTube states are untouched.
- **Explicit source holds verified:** Both expected OWB source holds (`iyvWYFP_ETA` Mars night Short and `RLSJm59OSzI` Titan Short) surfaced explicitly in `unmirrored` without planning, hosting, or creating from a missing or mismatched source.
- **Existing HOS back-post exceptions preserved:** `changes: []` on HOS confirms the four queued HOS items (`c2q7w0pgcn8`, `xHnIi9GqOsM`, `LCZRHUyTiq0`, `OnJ8MFu0Mi0`) are preserved at their approved dates without false takedowns or rehosts.
- **`J1878` approval boundary respected:** `J1878`'s external R2 uploads and six Buffer creates remain blocked pending direct trusted user authorization; this validation did not retry or execute them.
