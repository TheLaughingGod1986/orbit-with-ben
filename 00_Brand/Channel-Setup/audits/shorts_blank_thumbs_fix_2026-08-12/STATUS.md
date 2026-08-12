# Blank Shorts thumbnails — fix report

Date: 2026-08-12  
Scope: custom thumbnail only (no title/desc/visibility/schedule changes)

## Targets (from Studio mobile screenshots)

| ID | Title | State | Issue |
|----|-------|-------|-------|
| `nAZRIBm5wJw` | Three Suns in the Sky — Real Alien Worlds | Scheduled 15 Aug 11:30 | Grey blank cover in Studio list |
| `KcKBixwmcV4` | Why the First Alien Clue Might Be a Pattern… | Public | Grey blank cover in Studio list |

## Fix

1. Extracted strong frames from source Shorts MP4s
2. Composed **1280×720** custom covers (letterboxed 9:16 → 16:9)
3. Applied via YouTube Data API `thumbnails.set`

### Assets

- `02_Video-Projects/003_Exoplanets-Strangest-Alien-Worlds/10_Shorts/08_Covers/exoplanets_short-03_three-suns_cover_v01.jpg` (Orbit + “not one sun”)
- `02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/08_Covers/aliens_short-04_hidden-clues_cover_v01.jpg` (bright control-room frame)

### Result

Both `thumbnails.set` calls returned `youtube#thumbnailSetResponse` with maxres URLs.  
Studio edit screenshots + CDN maxres captures saved under `after/`.

## Notes

- Auto-generated CDN thumbs existed but rendered as blank/grey in Studio mobile for these two.
- No other mutations performed.
- Pull-to-refresh Studio mobile if covers still look cached.

## Evidence

- `THUMB_SET_RESULT.json`
- `before/` · `after/` · `assets/`
