# Shorts grey-block thumbs — reapply 2026-08-12

## Verdict

Custom covers were already set on the API; mobile Studio list was still showing grey placeholders. Rebuilt punchier **v02** covers and re-ran `thumbnails.set` (multipart). CDN now serves **new** maxres images for both IDs.

| Video | ID | CDN maxres | Notes |
|-------|----|------------|-------|
| Three Suns | `nAZRIBm5wJw` | updated (Orbit + “not one sun”) | Scheduled/private — public `i.ytimg.com` 404s without `sqp`; Studio mobile often greys these until cache refreshes |
| Alien Clue | `KcKBixwmcV4` | updated (cyan waveform fill) | Public — maxres MD5 changed after multipart set |

## What you should do on the phone

1. Force-quit YouTube Studio (swipe away)
2. Reopen → Content → Shorts
3. Or open each Short’s edit page — list tiles can lag behind edit-page / CDN

If still grey after that, it is Studio mobile list cache, not a missing custom thumb.

## Files

- Covers (local, gitignored `*.jpg`):  
  - `…/exoplanets_short-03_three-suns_cover_v02.jpg`  
  - `…/aliens_short-04_hidden-clues_cover_v02.jpg`
- Script: `07_Content-Ops/scripts/youtube-fix-blank-shorts-thumbs.ts`
- Result: `THUMB_SET_RESULT.json`
