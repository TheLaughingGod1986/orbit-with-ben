# Auto-post YouTube Shorts → Threads (@orbitwithben)

When a short goes **live on YouTube**, Orbit mirrors it to Threads — same pattern
as TikTok (`TikTok/AUTO_POST.md`) and Meta (`Meta/AUTO_POST.md`).

**One unique post (25 Aug 2026):** each Short is **one** Threads post. Remakes, new YouTube IDs, or the same file/title do not get a second post. A watcher pass posts **at most one** new unique Short. TikTok is paused separately.

Brand: **Orbit with Ben** · handle **@orbitwithben** · soft CTA *Full film on YouTube.*

## How it fires

1. **Watcher (every 5 min)** — reads each `10_Shorts/SHORTS_UPLOAD_INDEX.json`
   - `published_now: true` / `visibility: public`, **or**
   - `schedule_iso` already due (+2 min) and `video_id` present
   - Skips anything already in `THREADS_POSTED.json`
2. **Publish-now hook** — YouTube publish scripts call `hooks.notify_short_live`
   right after setting Public (alongside TikTok + Meta hooks).

## Preferred method: CDP (local)

Threads Graph video publish needs a **public** `video_url`. Until a staging CDN
is wired, use Chrome CDP on the shared IG/TikTok profile:

```bash
bash 00_Brand/Channel-Setup/Threads/auto/start_threads_chrome.sh
# Log into threads.com as @orbitwithben once in that window (port 9222).
```

`THREADS_CREDENTIALS.json`:

```json
{
  "preferred_method": "cdp",
  "cdp_port": 9222,
  "threads_username": "orbitwithben"
}
```

## Optional: Threads Graph API

1. Enable the Threads API product on the Meta app
2. Copy credentials:

```bash
cp 00_Brand/Channel-Setup/Threads/THREADS_CREDENTIALS.example.json \
   00_Brand/Channel-Setup/Threads/THREADS_CREDENTIALS.json
# fill access_token, threads_user_id, media_public_base_url
```

3. Check:

```bash
python3 00_Brand/Channel-Setup/Threads/auto/live_shorts_to_threads.py --check-creds
```

## One-time setup

```bash
# Seed already-live shorts so they aren't re-uploaded
python3 00_Brand/Channel-Setup/Threads/auto/live_shorts_to_threads.py --seed-all \
  --seed-project 001_Will-We-Ever-Meet-Aliens \
  --seed-project 003_Exoplanets-Strangest-Alien-Worlds

# Install macOS LaunchAgent (every 5 minutes)
cp 00_Brand/Channel-Setup/Threads/auto/dev.orbit.threads-live-shorts.plist \
  ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/dev.orbit.threads-live-shorts.plist
```

## Commands

```bash
cd 00_Brand/Channel-Setup/Threads/auto

python3 live_shorts_to_threads.py --list
python3 live_shorts_to_threads.py --dry-run
python3 live_shorts_to_threads.py --once
python3 live_shorts_to_threads.py --watch
python3 live_shorts_to_threads.py --check-creds
```

## Identity checklist

| Field | Value |
|-------|-------|
| Display name | Orbit with Ben |
| Handle | @orbitwithben |
| Bio | Space stories. Big questions. Full films on YouTube ↓ |
| Link | https://www.youtube.com/@OrbitWithBen |
| Avatar | Same Orbit mascot as YouTube / TikTok / IG |

Unload: `launchctl unload ~/Library/LaunchAgents/dev.orbit.threads-live-shorts.plist`

## 2026-08-20 catch-up

Ledger last wrote 3 Aug. Mac runbook for BH catch-up + exo 21–26 arming:

`audits/social_catchup_2026-08-20/CATCHUP_PLAN.md`
