# Instagram cleanup — 2026-08-03

## Goal
Remove legacy merch/animal graphics, drop duplicate Orbit reels, keep a clear YouTube follow + full-film path.

## Result
| Metric | Before | After |
|--------|--------|-------|
| Posts | 133 | ~9 (grid shows 3 Orbit reels + 1 rate-limited leftover) |
| Duplicate no-caption reels | 8–10 | 0 |
| Legacy `/p/` merch/art | ~117 | 1 remaining (IG delete rate-limit) |

### Kept (unique live shorts, Full film CTA)
- `DbkkmlLEwbH` — What If Aliens Are Watching Us?
- `DbkkMoxjwpt` — Space Is Rude About Distance
- `Dbkjz74gTje` — Where Is Everybody?

Captions include `Full film on YouTube.` + `https://youtu.be/Mo93x0fxB1Q`.

### YouTube path for viewers
- Bio: `Space stories. Big questions. Full films on YouTube ↓`
- Profile link: `www.youtube.com/@OrbitWithBen`
- Each reel caption: full-film URL above

### Leftover
- `/orbitwithben/p/Cq1MAN9I4pb/` — “DRAG IS NOT A CRIME” (Apr 2023). Delete UI returns **Couldn't delete post. Try again.** after mass cleanup (rate limit). Retry manually later from IG app/web.
- Post count may stay inflated briefly while IG finishes purging deleted media.

## Scripts
- `_ig_cleanup_legacy_dupes_v01.py` — classify + first pass
- `_ig_cleanup_legacy_dupes_v02.py` — fast resume delete
- Artifacts: this folder (`V02_RESULT.json`, `DONE.json`, screenshots)
