# Orbit Facebook + Instagram — Setup pack

Mirror of YouTube brand for Meta discovery. Pillar stays YouTube.

## Identity

| Field | Value |
|-------|-------|
| Display name | **Orbit with Ben** |
| Preferred IG | **@orbitwithben** |
| Fallbacks | `@orbit.with.ben` · `@orbitwithbenyt` |
| Facebook Page | **Orbit with Ben** |
| Bio | `Space stories. Big questions. Full films on YouTube ↓` |
| Website | https://www.youtube.com/@OrbitWithBen |
| Avatar | Same Orbit mascot (`TikTok/avatar_800x800.png`) |

## Soft CTA rule

Captions: “Full film on YouTube.” — never hard sell, never watermarked re-uploads.

## Auto-post

When a YouTube Short goes live, mirror to IG Reels + Facebook Page Reels:

→ **[AUTO_POST.md](./AUTO_POST.md)**

## Content Ops

OAuth + Page/IG selection:

→ **[CONNECT_TO_CONTENT_OPS.md](./CONNECT_TO_CONTENT_OPS.md)**

## Layout

```
00_Brand/Channel-Setup/Meta/
  META_ACCOUNTS.json
  META_CREDENTIALS.example.json   # copy → META_CREDENTIALS.json
  META_POSTED.json                # ledger (created at runtime)
  AUTO_POST.md
  CONNECT_TO_CONTENT_OPS.md
  META_SETUP.md
  auto/
    live_shorts_to_meta.py
    hooks.py
    graph_publish.py              # Graph API + resumable upload
    studio_upload.py              # Business Suite CDP fallback
    …
```
