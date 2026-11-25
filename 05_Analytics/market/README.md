# Market Intelligence (`05_Analytics/market/`)

Tracks a verified watchlist of ~90 competitor and rising channels across our three niches (**WW2 / Field Order History**, **Space / Orbit With Ben**, **History of Science**) so we spot breakouts every day and feed winning packaging patterns straight into `studio/RULES.md` rule 2 and topic checks.

## What Each Part Does

| File / Command | Purpose |
|---|---|
| `05_Analytics/market/watchlist.json` | ~90 Data-API-verified channels (~30 per niche: rising `<6m / <20k subs` plus proven benchmarks). Every row stores channel ID, creation date, subscribers, uploads playlist, niche, and `rising` / `benchmark` tier. |
| `scripts/market_track.py daily` | Read-only YouTube Data API v3 sweep (`playlistItems.list` + batched 50-ID `videos.list`, **never `search.list` daily**). Computes each channel's 20-long-upload median, captures ~6h / 24h / 72h snapshots, flags breakouts (`>=3x` median at 24h or `>=100k` views within 72h on `<20k`-sub channels), separates long-form (`>4 min`) from Shorts, filters AI content farms (`likes/views < 0.015` or templated `"What X said when..."` titles) into `farms.json`, enforces a **1,500-unit daily quota cap** (`quota.json`), rolls up daily JSONs older than 14 days into compact weekly roll-ups, and refreshes `05_Analytics/market/board.json`. |
| `scripts/market_track.py weekly` | Runs Mondays. Tags each breakout's title (searched subject first, How/Why opener, number, word count) and thumbnail (image URL only, 168 px phone metrics + optional vision tags: subject, frame fill %, words, face, grade), writes `05_Analytics/market/weekly/<YYYY-MM-DD>.md` with one **"The angle we could take"** line per breakout, and updates `board.json`. |
| `scripts/market_track.py discover` | Runs the first Monday of each month. Enforces a hard **<= 40 vidIQ credit cap** (never buys credits) and writes swap-out / swap-in watchlist proposals to `05_Analytics/market/proposals/<YYYY-MM>.md`. |
| `05_Analytics/market/board.json` | Compact summary published by `scripts/board_publish.py` (`board["market"]`) to the Studio board's **Market** tab (`#market`). |

## Schedule

Wired into the Mac mini's existing daily analytics LaunchAgent (`dev.orbit.analytics-snapshot`, **06:40 London**, `07_Content-Ops/launchd/analytics-snapshot.sh`):
- **Every day:** `python3 scripts/market_track.py daily`
- **Mondays:** `python3 scripts/market_track.py weekly`
- **First Monday of each month:** `python3 scripts/market_track.py discover`
- The same job commits `05_Analytics/` to `main` and triggers `scripts/board_publish.py`.

## How to Read the Market Tab

Open the **Market** tab (`#market`) on the Studio board:
1. **Patterns this week:** shows which title openers (e.g. searched subject first, How/Why, numbers) and 168 px thumbnail traits (grade, subject fill %, faces) are winning across the current week's breakouts.
2. **Filters:** filter by niche (**All / WW2 / Space / History of Science**) and format (**All / Long / Shorts**). Long-form breakouts (`>4 min`) always sort ahead of Shorts.
3. **Breakout cards:** each card shows the thumbnail, title, channel name and subscriber size (with a `Rising` tag for sub-20k emerging channels), video age, views per hour, multiple of that channel's 20-long median, Long/Short badge, and **"Angle we could take"** adapted to our channel format and rules (never copying competitor title wording).

## Guards

- **Metadata and thumbnail image URLs only:** no agent opens or plays any public video.
- **No revenue estimates.**
- **No changes to any YouTube channel.**
- **£0 beyond existing subscriptions** (never buys YouTube quota or vidIQ credits).
