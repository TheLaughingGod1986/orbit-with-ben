# Grey Studio thumbnails — 2026-08-13 FIXED

## Problem

After private-dupe cleanup, Studio still showed **solid grey** covers for:

| ID | Title | State |
|----|-------|-------|
| `nAZRIBm5wJw` | Three Suns in the Sky — Real Alien Worlds | Scheduled 15 Aug |
| `f8V6wCjWwHA` | Why Haven't We Found Aliens Yet? | Public |
| `OlwENQcY-jg` | Why This Alien World Looks Like a Giant Eye | Scheduled 17 Aug (left grey bar) |

API/`i9.ytimg` already had maxres for some of these, but **Studio desktop edit** for Three Suns showed the grey placeholder icon in player + thumbnail rail — not just mobile cache.

## Fix

1. Built brighter **1280×720** blur-wing covers from source Shorts MP4s (`covers/*_v03.jpg`, Giant Eye `*_v04.jpg`).
2. Re-applied via Data API `thumbnails.set` (multipart).
3. Re-uploaded the same stills through Studio CDP (`ytcp-thumbnail-uploader input#file-loader`) + Save — this restored Studio’s own thumb display.

## Verified (Studio desktop)

- Three Suns edit: custom still visible (player + thumbnail rail + sidebar).
- Fermi public edit: player/sidebar show cover (no grey placeholder).
- Giant Eye edit: custom still visible after v04.
- Content search “Three Suns”: dropdown shows colour Orbit thumb (not grey).

## Assets

- `covers/nAZRIBm5wJw_cover_v03.jpg`
- `covers/f8V6wCjWwHA_cover_v03.jpg`
- `covers/OlwENQcY-jg_cover_v04.jpg`
- Project copy: `02_Video-Projects/003_…/08_Covers/exoplanets_short-03_three-suns_cover_v03.jpg`
- Scripts: `07_Content-Ops/scripts/youtube-fix-grey-studio-thumbs.ts`, `_studio_upload_covers.py`
- Evidence: `studio_after/*`, `MUTATION_JOURNAL.json`, `STUDIO_UPLOAD_RESULT.json`

## Note for mobile

Force-quit / pull-to-refresh Studio mobile if the list still shows stale greys — desktop Studio is source of truth here.
