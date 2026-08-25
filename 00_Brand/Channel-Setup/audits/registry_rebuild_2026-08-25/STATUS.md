# Registry rebuild — finished 25 Aug 2026 15:30 UK

## What was broken
`SHORTS_UPLOAD_INDEX.json` for 001–003 still pointed at deleted YouTube IDs. Social mirrors and `ensure-shorts-fullfilm-comments` read those files. JWST entries 02–06 had no `file`, so `pending_live_shorts()` skipped them (`_abs_file` required).

## What is live now
- Indexes rebuilt / refreshed to live IDs (`tools/rebuild_shorts_indexes.py`).
- JWST 02–06 have on-disk `file` paths. 06 (`68uTDP2esso`) uses `jwst_short-05_doesnt-add-up_v03.mp4` (no `*too-big*` export on disk).
- Social ledgers seeded so the rewrite does not dump old Shorts. Today’s Short was left unseeded.

## Dry-run (15:30)
Meta / Threads / TikTok each `pending=1`: `yt:68uTDP2esso` only. No live-unposted missing files.

## LaunchAgents
Reloaded 25 Aug 15:30 (`bootstrap gui/$UID`):

- `dev.orbit.meta-live-shorts`
- `dev.orbit.threads-live-shorts`
- `dev.orbit.tiktok-live-shorts`

`RunAtLoad` is true — they will try today’s Short on the next cycle.

## Still later
Studio punch-text covers: job `dev.orbit.shorts-covers` at 13:15. Confirm `upload_run.log` / `UPLOAD_RESULT.json` and `--verify-grid`. If Studio shows “Verify that it’s you”, Ben must complete it.
