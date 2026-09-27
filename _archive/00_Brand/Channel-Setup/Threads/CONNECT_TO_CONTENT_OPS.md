# Connect Orbit Threads to Content Ops

Brand: **Orbit with Ben** · YouTube pillar [@OrbitWithBen](https://www.youtube.com/@OrbitWithBen)

This wires Threads the same way TikTok and Meta are wired: Content Ops OAuth
**and** the brand-level auto-post mirror for live YouTube Shorts.

## What you need

| Piece | Requirement |
|-------|-------------|
| Threads account | **@orbitwithben** (same login as Instagram) |
| Meta app | Threads API product enabled |
| Permissions | Threads content publish scopes for the user |

## Content Ops OAuth

1. In [Meta for Developers](https://developers.facebook.com/) enable **Threads API**.
2. Valid OAuth redirect:

```text
http://localhost:3000/api/oauth/threads/callback
```

3. Fill `07_Content-Ops/.env`:

```env
THREADS_APP_ID=
THREADS_APP_SECRET=
THREADS_REDIRECT_URI=http://localhost:3000/api/oauth/threads/callback
```

4. Start Content Ops → Settings → Connections → Connect Threads when the UI ships.

Docs: `07_Content-Ops/docs/THREADS_PUBLISHING_ASSESSMENT.md`

## Brand auto-post credentials (shorts mirror)

```bash
cp 00_Brand/Channel-Setup/Threads/THREADS_CREDENTIALS.example.json \
   00_Brand/Channel-Setup/Threads/THREADS_CREDENTIALS.json
```

Until Graph App Review + a public media URL are ready, keep:

- `preferred_method`: `cdp`
- `cdp_port`: `9222` (shared with TikTok / Instagram login session)

`THREADS_CREDENTIALS.json` is gitignored.

## CDP fallback

```bash
bash 00_Brand/Channel-Setup/Threads/auto/start_threads_chrome.sh
```

Log into https://www.threads.com/ as **@orbitwithben** once.

## Identity checklist

| Field | Value |
|-------|-------|
| Display name | Orbit with Ben |
| Handle | @orbitwithben |
| Bio | Space stories. Big questions. Full films on YouTube ↓ |
| Website / link | https://www.youtube.com/@OrbitWithBen |
| Avatar | Same Orbit mascot as YouTube / TikTok |

See `AUTO_POST.md` for the watcher + LaunchAgent.
