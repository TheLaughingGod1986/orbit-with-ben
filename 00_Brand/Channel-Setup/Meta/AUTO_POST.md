# Auto-post YouTube Shorts → Instagram Reels + Facebook Reels

When a short goes **live on YouTube**, Orbit mirrors it to Instagram and the
Facebook Page — same pattern as TikTok (`TikTok/AUTO_POST.md`).

**One unique post (25 Aug 2026):** each Short is **one** Instagram Reel and **one** Facebook Reel. Remakes, new YouTube IDs, or the same file/title do not get a second post. A watcher pass posts **at most one** new unique Short. TikTok is paused separately.

## How it fires

1. **Watcher (every 5 min)** — reads each `10_Shorts/SHORTS_UPLOAD_INDEX.json`
   - `published_now: true` / `visibility: public`, **or**
   - `schedule_iso` already due (+2 min) and `video_id` present
   - Skips anything already in `META_POSTED.json`
2. **Publish-now hook** — YouTube publish scripts call `hooks.notify_short_live`
   right after setting Public (alongside the TikTok hook).

## Preferred method: Graph API

1. Create / reuse a Meta app (see `CONNECT_TO_CONTENT_OPS.md`)
2. Copy credentials:

```bash
cp 00_Brand/Channel-Setup/Meta/META_CREDENTIALS.example.json \
   00_Brand/Channel-Setup/Meta/META_CREDENTIALS.json
# fill page_id, page_access_token, instagram_business_account_id
```

3. Check:

```bash
python3 00_Brand/Channel-Setup/Meta/auto/live_shorts_to_meta.py --check-creds
```

Graph uses **resumable upload** so local short files work without a public CDN URL.

## Fallback: Meta Business Suite CDP

If Graph credentials are missing (or `preferred_method` is `cdp`):

```bash
bash 00_Brand/Channel-Setup/Meta/auto/start_meta_chrome.sh
# Log into the Orbit Facebook Page + Instagram pro account once in that window.
```

Chrome profile: `~/.orbit-chrome-meta-dev` on port **9223** (TikTok stays on 9222).

## One-time setup

```bash
# Seed already-posted / already-live shorts so they aren't re-uploaded
python3 00_Brand/Channel-Setup/Meta/auto/live_shorts_to_meta.py --seed-all \
  --seed-project 001_Will-We-Ever-Meet-Aliens \
  --seed-project 003_Exoplanets-Strangest-Alien-Worlds

# Install macOS LaunchAgent (every 5 minutes)
cp 00_Brand/Channel-Setup/Meta/auto/dev.orbit.meta-live-shorts.plist \
  ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/dev.orbit.meta-live-shorts.plist
```

## Commands

```bash
cd 00_Brand/Channel-Setup/Meta/auto

python3 live_shorts_to_meta.py --list
python3 live_shorts_to_meta.py --dry-run
python3 live_shorts_to_meta.py --once
python3 live_shorts_to_meta.py --watch
python3 live_shorts_to_meta.py --check-creds
```

## Notes

- Soft CTA only: “Full film on YouTube.”
- Instagram must be a **professional** account linked to the Facebook Page.
- Future `schedule_iso` wins over stale `published_now` / `visibility: public` in the index (`discover.is_live`) — same rule as TikTok. Do not mirror until YouTube actually goes live.
- Unload: `launchctl unload ~/Library/LaunchAgents/dev.orbit.meta-live-shorts.plist`

## Share step spinner (not a broken computer)

If Meta Business Suite **Create reel → Share** spins forever, audience radios stay
grey, and the page says options are **only available for posts to a Facebook
Page**, the composer is on the wrong asset (Instagram-only or the old Benkay
Creative portfolio). Extra Suite tabs make it worse. Close them.

Open the Orbit **Page** composer, then retry:

```
https://business.facebook.com/latest/reels_composer?asset_id=1285932871266399&business_id=1352434763139246
```

CDP now pins that URL, refuses Benkay IDs in `META_CREDENTIALS.json`, and aborts
with `share_step_hung` instead of clicking the spinning **Share** step. Graph
API remains the preferred publish path.

## 2026-08-20 catch-up

If IG/FB went quiet after the 17 Aug Suite batch, follow the Mac runbook (YT-first,
delete premature exo 12–17 schedules, reload watchers, BH catch-up, arm exo 21–26):

`audits/social_catchup_2026-08-20/CATCHUP_PLAN.md`
