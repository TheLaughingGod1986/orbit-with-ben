---
description: TikTok uploads paused — account ban until Ben lifts
alwaysApply: true
---

# TikTok uploads — paused (Ben 25 Aug 2026)

**Do not upload, schedule, or mirror anything to TikTok** until Ben explicitly lifts this.

The account is banned from posting. Retrying uploads can worsen the ban.

## Do not

- Reload `dev.orbit.tiktok-live-shorts`, `dev.orbit.tiktok-upload-missing-v02`, or `dev.orbit.tiktok-reupload-missing`
- Run `live_shorts_to_tiktok.py --once` / `--watch` (except `--list` / seed)
- Run `_tt_upload_one_safe.py`, `_upload_missing_v02_cdp.py`, or other TikTok Studio CDP uploaders
- Publish via Content Ops TikTok adapter
- “Just try one” to see if the ban cleared

## Lock file

`00_Brand/Channel-Setup/TikTok/TIKTOK_UPLOAD_BLOCK.json` → `"paused": true`

YouTube, Meta, and Threads are unaffected.

## Lift

Only when Ben says so: set `paused` to `false`, then reload LaunchAgents if he asks.
