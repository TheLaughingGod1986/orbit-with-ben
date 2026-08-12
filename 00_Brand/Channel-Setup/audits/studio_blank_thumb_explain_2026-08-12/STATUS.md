# Studio blank thumbs + “what's left” — 2026-08-12T11:38Z

## Live API truth (not Studio mobile list)

| ID | Title | API privacy | publishAt | Notes |
|----|-------|-------------|-----------|-------|
| `JRfhE6yWom4` | Why This Line Is a Point of No Return | **public** | — | Mobile lock icon is wrong |
| `KcKBixwmcV4` | Alien Clue | **public** | — | Custom maxres **exists** (90KB JPEG); mobile grey is cache/UI |
| `nAZRIBm5wJw` | Three Suns | private+scheduled | 15 Aug 10:30Z | Custom maxres **exists** via i9 sqp; mobile grey common for scheduled |
| `OlwENQcY-jg` | Giant Eye | private | **cleared** | Mobile “scheduled 17 Aug” is stale cache |
| `QRi6Dxq0hz0` | Host Life | private | **cleared** | — |
| `w1ej9u0rPTA` | The Point of No Return Explained | private | — | Old duplicate; public CDN 404 → true grey placeholder |
| `mGwSCdgxQO4` | It Rains Glass Sideways | private | — | Old hold; live scheduled copy is `SC2WGTl_V5Q` |

## Why grey blocks persist in Studio mobile

1. **Not missing on YouTube** for Alien Clue / Three Suns — CDN serves real custom covers.
2. **Studio mobile list** often shows a light-grey tile when: private/scheduled auth CDN lags, or the app caches the empty placeholder.
3. **True blank:** `w1ej9u0rPTA` (private duplicate) — public thumb URLs 404; never part of the cover fix set.
4. Screenshots with status-bar **12:07** predate P1 unschedule (Giant Eye still shown scheduled).

## What's left (ops)

- **Done:** P0 privatize/unschedule · P1 exo reserves unscheduled · core exo 13–16 + JWST/long protected
- **Optional:** set covers on private duplicates if you care about Studio list cosmetics (`w1ej9u0rPTA`, etc.)
- **Optional:** refresh `YOUTUBE_CANONICAL_LIVE_SCHEDULE.json` / registry (remove Olw/QRi air dates; new exo IDs)
- **Watch:** exo long + Shorts air 13–16 Aug; JWST from 20 Aug
