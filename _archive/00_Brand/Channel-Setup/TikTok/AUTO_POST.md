# Auto-post YouTube Shorts → TikTok

**PAUSED (25 Aug 2026):** TikTok account is banned from posting. **No uploads** until Ben lifts `TIKTOK_UPLOAD_BLOCK.json` and says so. Do not reload LaunchAgents. YouTube / Meta / Threads are unaffected.

When a short goes **live on YouTube**, Orbit mirrors it to **[@orbitwithben](https://www.tiktok.com/@orbitwithben)** via TikTok Studio (Chrome CDP).

## How it fires

1. **Watcher (every 5 min)** — reads each `10_Shorts/SHORTS_UPLOAD_INDEX.json`  
   - `published_now: true` / `visibility: public`, **or**  
   - `schedule_iso` already due (+2 min) and `video_id` present  
   - Skips anything already in `TIKTOK_POSTED.json`
2. **Publish-now hook** — `_publish_shorts_now_v003.py` / `_publish_short01_now_v01.py` call `hooks.notify_short_live` right after setting Public.

## One-time setup

```bash
# 1) Chrome logged into @orbitwithben on the CDP profile
bash 00_Brand/Channel-Setup/TikTok/auto/start_tiktok_chrome.sh
# Log in once in that window if needed.

# 2) Mark already-covered shorts so they aren't re-uploaded
# Prefer this after a manual / pre-scheduled Studio batch:
python3 00_Brand/Channel-Setup/TikTok/auto/live_shorts_to_tiktok.py --seed-scheduled

# Or mark by YouTube index (live only / all indexed):
python3 00_Brand/Channel-Setup/TikTok/auto/live_shorts_to_tiktok.py --seed-all \
  --seed-project 001_Will-We-Ever-Meet-Aliens \
  --seed-project 003_Exoplanets-Strangest-Alien-Worlds

# 3) Install macOS LaunchAgent (every 5 minutes)
cp 00_Brand/Channel-Setup/TikTok/auto/dev.orbit.tiktok-live-shorts.plist \
  ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/dev.orbit.tiktok-live-shorts.plist
```

## Commands

```bash
cd 00_Brand/Channel-Setup/TikTok/auto

python3 live_shorts_to_tiktok.py --list             # live vs posted
python3 live_shorts_to_tiktok.py --dry-run          # what would post
python3 live_shorts_to_tiktok.py --once             # single pass
python3 live_shorts_to_tiktok.py --watch            # loop (foreground)
python3 live_shorts_to_tiktok.py --seed-scheduled   # cover pre-scheduled batch
```

## Notes

- Needs Chrome CDP on `:9222` with profile `~/.orbit-chrome-tiktok-dev`.
- Caption is built from the index description (prose + hashtags + “Full film on YouTube”).
- **On-screen text style** (burn-in): `SHORTS_ONSCREEN_TEXT_STYLE.md` — yellow/white lowercase kinetic captions via `*_shorts_v02.py`.
- Black-hole shorts (scheduled Aug 6+) will auto-post when their `schedule_iso` passes.
- **Pre-scheduled Studio posts** are recorded in `TIKTOK_POSTED.json` (`yt:…` + `tt:…` keys, `mode: scheduled`). The watcher will **not** Post-now duplicates for those.
- If Studio shows *“You've reached your check limit for today”*, uploads fail until the next day. The watcher records failures and backs off (`check_limit`).
- Unload: `launchctl unload ~/Library/LaunchAgents/dev.orbit.tiktok-live-shorts.plist`

## 2026-08-03 restore notes

- LaunchAgent `dev.orbit.tiktok-live-shorts` reloads `auto/live_shorts_to_tiktok.py --once` every 5 minutes.
- `discover.is_live()` treats a future `schedule_iso` as not-live even if visibility says public.
- Pre-schedule batch uploads must use `_tt_upload_one_safe.py` → `_upload_missing_v02_cdp.py` (verifies schedule values + Studio needle). Do **not** trust CTA-click-only success.
- If Studio shows `Something went wrong. You can try again or replace it with a different video.`, stop and retry later — that is a platform-side publish failure, not a missing file.

## 2026-08-20 catch-up

Socials went quiet after the 3 Aug ban + Meta batch ending 17 Aug. Mac runbook (unban → watchers → BH catch-up → exo 21–26 arm):

`audits/social_catchup_2026-08-20/CATCHUP_PLAN.md`

