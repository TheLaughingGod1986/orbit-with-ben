# TikTok Connection Setup

**Docs checked:** 2026-07-31 — Content Posting API.

## Modes (distinct)

| Mode | Scope | Outcome status |
|------|-------|----------------|
| Upload as Draft | `video.upload` | `manual_action_required` — finish in TikTok app |
| Direct Post | `video.publish` | `published` only after status confirms |

Never treat draft upload as published.

## Developer portal

1. Create an app at [TikTok Developers](https://developers.tiktok.com/)
2. Enable Content Posting API
3. Configure redirect:
   `http://localhost:3000/api/oauth/tiktok/callback`
4. Complete audit / Direct Post approval before enabling direct publish

## Environment

```env
TIKTOK_CLIENT_KEY=
TIKTOK_CLIENT_SECRET=
TIKTOK_REDIRECT_URI=http://localhost:3000/api/oauth/tiktok/callback
```

## Connect

OAuth uses PKCE. After connect, capability matrix shows draft vs direct based on granted scopes and app approval metadata.

## Safe test

- Draft: upload then open TikTok inbox — enter final URL manually after publish
- Direct: unaudited clients often limited to `SELF_ONLY` — use that for tests

## UI messaging

If Direct Post is unavailable:

> Direct Post unavailable. TikTok draft upload is available.

## Manual fallback

Export package + checklist remain the default when scopes are missing.
