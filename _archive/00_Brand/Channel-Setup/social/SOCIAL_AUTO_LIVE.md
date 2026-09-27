# Social auto-live (Shorts + longs)

**Locked 26 Aug 2026.** When a YouTube video goes public, Orbit mirrors it to social — without TikTok until Ben lifts the ban.

## What goes where

| YouTube | Instagram | Facebook Page | Threads | TikTok |
|---------|-----------|---------------|---------|--------|
| Short (live) | Reel (native) | Reel (native) | Video / link | **Paused** |
| Long (live) | — | Soft YouTube link post | Soft YouTube link post | **Paused** |

Uniqueness still applies to Shorts (`social/uniqueness.py`). Longs use `social/LONGS_POSTED.json`.

## Watchers (LaunchAgents)

| Agent | Every | Script |
|-------|------:|--------|
| `dev.orbit.meta-live-shorts` | 5 min | `Meta/auto/live_shorts_to_meta.py --once` |
| `dev.orbit.threads-live-shorts` | 5 min | `Threads/auto/live_shorts_to_threads.py --once` |
| `dev.orbit.live-longs-social` | 5 min | `social/live_longs_to_social.py --once` |

Python: `00_Brand/Channel-Setup/.venv-social/bin/python` (Playwright).

### Install / reload (posting Mac)

```bash
cp 00_Brand/Channel-Setup/Meta/auto/dev.orbit.meta-live-shorts.plist ~/Library/LaunchAgents/
cp 00_Brand/Channel-Setup/Threads/auto/dev.orbit.threads-live-shorts.plist ~/Library/LaunchAgents/
cp 00_Brand/Channel-Setup/social/dev.orbit.live-longs-social.plist ~/Library/LaunchAgents/

launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/dev.orbit.meta-live-shorts.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/dev.orbit.threads-live-shorts.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/dev.orbit.live-longs-social.plist
```

Keep TikTok plists **Disabled** / do not load.

### Chrome sessions

- Meta Reels CDP: `Meta/auto/start_meta_chrome.sh` → port **9223**, profile `~/.orbit-chrome-meta-dev`
- Threads CDP: `Threads/auto/start_threads_chrome.sh` → port **9222**, profile `~/.orbit-chrome-tiktok-dev`
- Long link posts: main Google Chrome with **View → Developer → Allow JavaScript from Apple Events**

## Manual one-shots

```bash
VENV=00_Brand/Channel-Setup/.venv-social/bin/python

# Shorts
$VENV 00_Brand/Channel-Setup/Meta/auto/live_shorts_to_meta.py --once
$VENV 00_Brand/Channel-Setup/Threads/auto/live_shorts_to_threads.py --once

# Longs (YouTube link cards)
$VENV 00_Brand/Channel-Setup/social/live_longs_to_social.py --list
$VENV 00_Brand/Channel-Setup/social/live_longs_to_social.py --once
```

## Indexes

Shorts discover reads every `02_Video-Projects/*/10_Shorts/SHORTS_UPLOAD_INDEX.json`.
A Short must be `visibility: public` (or due `schedule_iso`) **and** the mp4 must exist on disk.

Longs discover uses `social/live_longs.py` (`KNOWN_LONGS`). Premieres (`REXYxuLOBoI`, `NbW5G1BpPY0`) wait until watchable.

## Publish-now hooks

Existing Shorts publish scripts already call `hooks.notify_short_live` (Meta / Threads / TikTok). TikTok hook no-ops while paused. Long publish scripts should call:

```bash
00_Brand/Channel-Setup/.venv-social/bin/python \
  00_Brand/Channel-Setup/social/live_longs_to_social.py --once
```

after setting the long Public (or rely on the 5-minute LaunchAgent).
