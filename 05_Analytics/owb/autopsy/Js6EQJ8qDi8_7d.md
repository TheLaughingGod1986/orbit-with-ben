# Retention Autopsy (7 d) — Orbit With Ben · `Js6EQJ8qDi8`

- **Film:** OWB 025 — *Could a Robot Survive on Mars? (One Lasted 14 Years)* (`Js6EQJ8qDi8`)
- **Published:** `2026-11-08T18:00:15Z` · **Duration:** `8:11` (`491 s`)
- **Autopsy date:** `2026-11-20` (`J3256`, full 100-point retention-curve test on Orbit's newest long with an unsuppressed YTA curve; snapshot `2026-11-20`, YTA through `2026-11-18`)
- **Reviewer:** Gemini (Gemini 4 Neon, moving video + audio verified via `read_file` on four `40 s` clips from `/Volumes/data/mac-mini-archive/youtube-staging/025/025_MarsRobot_full_rough_v03f.mp4`)

---

## 1. Relative-Strength Score (RSI)

> **RSI (vs ch / niche):** `Showings 66↑/0↓↓ · CTR 62↑/44↓ · Views 76↑↑/0↓↓ · Avg% 42↓/30↓↓ · 0:30 46→/36↓ · Subs/1k —/0↓↓`

*(Scale: `0–100` where `50→` = on benchmark; `70+ ↑↑` strong, `55–69 ↑` above, `45–54 →` inline, `31–44 ↓` below, `0–30 ↓↓` weak. Formula: `100 × value / (value + benchmark)`.)*

| Metric | Film (7 d / latest) | Channel median | Baseline basis | RSI (ch) | Niche outlier (`<50k`) | RSI (niche) |
|---|---:|---:|---|---:|---:|---:|
| Showings (Impressions) | `192` *(55 at 48 h)* | `97.0` | lifetime Studio longs (`n=15`) | `66↑` | `80,000` | `0↓↓` |
| Click-through (CTR) | `3.1%` *(1.8% at 48 h)* | `1.9%` | lifetime Studio longs (`n=15`) | `62↑` | `4.0%` | `44↓` |
| Views | `19` *(24 by day 11)* | `6.0` | same-age 7 d snapshots (`n=6`) | `76↑↑` | `5,000` | `0↓↓` |
| Average % viewed | `15.0%` *(Studio 1:16; YTA 13.02% / 1:03)* | `21.0%` | lifetime Studio/YTA longs (`n=15`) | `42↓` | `35.0%` | `30↓↓` |
| 0:30 retention | `33.3%` *(YTA 100-pt curve, rel `0.054`)* | `39.1%` | lifetime YTA curves (`n=7`) | `46→` | `60.0%` | `36↓` |
| Subscribers / 1,000 views | `0.0` (`0` subs) | `0.0` | lifetime YTA longs (`n=15`) | `—` | `10.0` | `0↓↓` |

- **Niche outlier source:** `05_Analytics/new_channel_research/SUMMARY.md` (`<50k` space/science peers) and `05_Analytics/LEARNINGS.md` rules 10, 23, 34, 37.
- **Traffic sources (YTA through 18 Nov):** `SUBSCRIBER: 6`, `RELATED_VIDEO: 6`, `YT_SEARCH: 5`, `NO_LINK_OTHER: 4`, `EXT_URL: 2`.

---

## 2. Funnel Diagnosis (Strict Priority Order)

**Primary bottleneck: Step 1 — Showings (Topic / Search)** *(with severe confirmed retention cliffs at Step 3 Hook and Step 4 Picture/Pacing).*

1. **Showings (Topic / Search) — `PRIMARY BOTTLENECK`:** `192` impressions is above OWB's own low median (`97`, `RSI 66↑`) but far under the `500`-impression 7 d floor and niche outlier scale (`80,000`, `RSI 0↓↓`). Only `5` search views in 11 days.
2. **Click-through (Packaging) — `OK (vs channel) / WATCH (vs niche)`:** `3.1%` CTR on `192` impressions beats OWB's `1.9%` median (`RSI 62↑`) and clears the `2.5%` bar, though still below the `4.0%` niche bar (`RSI 44↓`).
3. **First 30 seconds (Hook) — `SEVERE SECONDARY BOTTLENECK`:** `0:30` retention collapses to **`33.3%`** (`RSI 36↓` vs `60%` target; relative retention `0.054` — bottom 5% of YouTube). Two-thirds of viewers leave before `0:30` (`-33.3 pp` at `0:04–0:09`, `-20.0 pp` at `0:14–0:19`, `-6.7 pp` at `0:24–0:29`).
4. **Mid-film cliffs (Pacing / Picture) — `SEVERE SECONDARY BOTTLENECK`:** Average viewed is only **`15.0%`** (`RSI 42↓ / 30↓↓`), with distinct `-6.7 pp` cliffs at `0:49–0:54`, `1:38–1:43`, and `3:36–3:40` (cutting remaining viewers in half from `13.3%` to `6.7%`).
5. **End (End Screen / Handoff) — `BOTTLENECK`:** Finishes at only `6.7%` retention (`491 s`).

---

## 3. Gemini 4 Neon Watch Notes (Moving Video + Audio on Steepest Curve Drops)

Pulled the full 100-point YTA retention curve from `05_Analytics/owb/snapshots/2026-11-20.json` and watched `20 s` either side of the three steepest non-overlapping drops (plus the mid-film `3:36–3:40` subscribe-break cliff) directly from `025_MarsRobot_full_rough_v03f.mp4`:

1. **Drop #1 — `0:04–0:09` (`-33.3 pp`, `100.0% -> 66.7%`) & `0:14–0:19` (`-20.0 pp`, `66.7% -> 46.7%`) · Watched `0:00–0:40`:**
   - **0:00–0:09:** Opens on two consecutive **static top-down stills** of Opportunity's solar deck (slow Ken-Burns zoom only, zero moving video) while VO reads `"A robot built to last 90 days on Mars kept going for more than 14 years."` Flat hardware plates with no motion lose a third of viewers immediately.
   - **0:14–0:18 (exact `-20.0 pp` cliff):** Cuts to a **flat monochrome greyscale Mars terrain still** while VO says `"it wears them down slowly, in ways you already know from home."`
   - **0:26–0:39:** VO asks `"Could Orbit?"` without showing Orbit, then launches a **10-second meta-promise agenda** (`"In this film, I will show you what Mars does to the machines we send…"`) over the exact same Opportunity deck still reused from `0:00`, followed by another greyscale still (`0:37`).
2. **Drop #2 — `0:49–0:54` (`-6.7 pp`, `26.7% -> 20.0%`) · Watched `0:31–1:12`:**
   - **0:41–0:45:** Chapter card `"A Desert That Isn't"` appears at `0:41` (`<0:45` rule) over flat dark ripples.
   - **0:50–1:00 (exact drop window):** Cuts to **two back-to-back monochrome greyscale rock stills** while VO recites raw statistics (`"less than 1% of Earth's"`, `"minus 60 degrees"`) with **zero on-screen DATA graphics or scale bars**.
3. **Drop #3 — `1:38–1:43` (`-6.7 pp`, `20.0% -> 13.3%`) · Watched `1:20–2:00`:**
   - **1:20–1:37:** Five static Mars rover stills in a row (`4–5 s` holds each), zero moving footage, zero overlays.
   - **1:38–1:45 (exact drop window):** Two consecutive **washed-out greyscale hazard-camera stills** (including an overexposed white/grey horizon at `1:42–1:45`) while VO slows to single dramatic words with long pauses (`"The killers are quieter... cold... dust... wear."`).
4. **Bonus Mid-Film Cliff — `3:36–3:40` (`-6.7 pp`, `13.3% -> 6.7%`, losing half of remaining viewers) · Watched `3:18–3:58`:**
   - **3:34–3:38:** Low-contrast orbital cracked-ground photo with no callout/circle showing where the broken Phoenix lander is.
   - **3:45–3:51:** **Hard mid-roll subscribe interruption** (`"We make one of these every week. Subscribing is how the next one finds you."` + animated red `SUBSCRIBE` pill), followed immediately by a blank-horizon chapter card (`The Dust`) at `3:52`.

---

## 4. Concrete Fixes (Max 3)

1. **[this video — Packaging / Description]:** Keep `3.1%` CTR title/thumbnail baseline intact until impressions grow; check YouTube Studio for any active Test & Compare first (never replace a running test). Verify the description's top two lines target exact high-intent queries (`"Opportunity rover Mars"`, `"how long did Opportunity last on Mars"`) and link to the Real Worlds playlist on the end screen.
2. **[next film — Picture & Visual Rule]:** Ban consecutive monochrome/greyscale hazard-camera stills (`0:14`, `0:50–1:00`, `1:38–1:45` — **every single steepest drop on `Js6EQJ8qDi8` sat directly on a monochrome NASA still!**), enforce real moving imagery at `0:00–0:10`, and pair every spoken statistic (`<1%` pressure, `-60°C`, `3–20 min` delay) with an animated on-screen DATA/SCALE graphic (`studio/RULES.md` *Teach on screen*).
3. **[next film — Pacing & Subscribe Beat]:** Eliminate `"In this film, I will show you…"` agendas (`0:30`), never drop a chapter card before `0:45`, and never interrupt a story chapter with a standalone mid-roll subscribe ask (`3:45`) followed directly by a chapter card.

---

## 5. Repeatable Lesson for `LEARNINGS.md`

- Logged under **Rule 38** in `05_Analytics/LEARNINGS.md`: on `Js6EQJ8qDi8` (`100`-point retention curve), **all three steepest drops (`0:14`, `0:50`, `1:38`) coincided directly with flat monochrome/greyscale NASA stills**, static opening plates (`-33.3 pp` at `0:04`), `"In this film, I will show you…"` agendas (`0:30`), and a mid-roll subscribe interruption (`3:45` halving remaining retention `13.3% -> 6.7%`).
