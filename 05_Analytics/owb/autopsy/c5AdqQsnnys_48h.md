# Retention Autopsy (48 h) — Orbit With Ben · `c5AdqQsnnys`

- **Film:** OWB 026 — *How Far Is the Nearest Star? (You Can't See It, and It Has a Planet)* (`c5AdqQsnnys`)
- **Published:** `2026-11-15T18:00:37Z` · **Duration:** `8:15` (`495 s`)
- **Autopsy date:** `2026-11-20` (`J3256`, initial test run on Orbit's newest public long; snapshot `2026-11-20`, YTA through `2026-11-18`, 48 h Studio check `2026-11-17T19:38Z`)
- **Reviewer:** Gemini (Gemini 4 Neon, moving video + audio verified via `read_file` on cut clips from `/Volumes/data/mac-mini-archive/youtube-staging/026/026_NearestStar_v06_cfr18.mp4`)

---

## 1. Relative-Strength Score (RSI)

> **RSI (vs ch / niche):** `Showings 8↓↓/0↓↓ · CTR 85↑↑/74↑↑ · Views 80↑↑/1↓↓ · Avg% 40↓/26↓↓ · 0:30 —/— · Subs/1k —/0↓↓`

*(Scale: `0–100` where `50→` = on benchmark; `70+ ↑↑` strong, `55–69 ↑` above, `45–54 →` inline, `31–44 ↓` below, `0–30 ↓↓` weak. Formula: `100 × value / (value + benchmark)`.)*

| Metric | Film (48 h / latest) | Channel median | Baseline basis | RSI (ch) | Niche outlier (`<50k`) | RSI (niche) |
|---|---:|---:|---|---:|---:|---:|
| Showings (Impressions) | `9` *(23 by day 5)* | `106.0` | lifetime Studio longs (`n=16`) | `8↓↓` | `25,000` | `0↓↓` |
| Click-through (CTR) | `11.1%` *(4.4% by day 5)* | `1.95%` | lifetime Studio longs (`n=16`) | `85↑↑` | `4.0%` | `74↑↑` |
| Views | `8` *(12 by day 5)* | `2.0` | same-age 48 h snapshots (`n=7`) | `80↑↑` | `1,500` | `1↓↓` |
| Average % viewed | `12.12%` *(Studio 60 s; YTA 1.93% / 9 s)* | `18.0%` | lifetime Studio/YTA longs (`n=16`) | `40↓` | `35.0%` | `26↓↓` |
| 0:30 retention | `—` *(suppressed at 12 views)* | `36.2%` | lifetime YTA curves (`n=8`) | `—` | `60.0%` | `—` |
| Subscribers / 1,000 views | `0.0` (`0` subs) | `0.0` | lifetime YTA longs (`n=16`) | `—` | `10.0` | `0↓↓` |

- **Niche outlier source:** `05_Analytics/new_channel_research/SUMMARY.md` (`<50k` space/science peers: Stellar `4,964` median, Simple Science `1,631`, Science Into Sleep `1,323`, Orbitra `21k–38k`) and `05_Analytics/LEARNINGS.md` rules 10, 23, 34, 37.
- **Traffic sources (YTA through 18 Nov):** `NO_LINK_OTHER: 7`, `YT_SEARCH: 1` (`0` Browse/Suggested).

---

## 2. Funnel Diagnosis (Strict Priority Order)

**Primary bottleneck: Step 1 — Showings (Topic / Search)** *(secondary: Step 3 Hook & Step 4 Pacing/Picture, verified by watching the cut).*

1. **Showings (Topic / Search) — `PRIMARY BOTTLENECK`:** Only `9` impressions at 48 h (`23` by day 5) against a `200`-impression 48 h floor and `106` channel median (`RSI 8↓↓ / 0↓↓`). Only `1` view came from YouTube Search; `0` from Browse/Suggested. The single-question space topic has almost zero impressions on a 19-sub channel, matching Rule 34's pause on single-question longs and Rule 37's move to search-led clusters from 1 Jan 2027.
2. **Click-through (Packaging) — `UNMEASURED (low sample)`:** `11.1%` at 48 h (`1` click of `9` impressions) and `4.4%` by day 5 (`23` impressions) is too small a sample (`<100` impressions) to fault packaging. Note: Title & Thumbnail Test & Compare `T027` (`11-DAY YEAR` vs `TRILLIONS OF YEARS`) was armed on `2026-11-10` — **do not touch or replace** while running.
3. **First 30 seconds (Hook) — `SECONDARY BOTTLENECK`:** YouTube suppressed the 0:30 retention curve at `12` views, but YTA lifetime AVD is `9 s` (`1.93%`) and Studio AVD is `60 s` (`12.12%`). Watching `0:00–0:40` reveals a textbook Rule 10 hook violation (generic sky open + 12-second `"In this film, I will show you…"` agenda + chapter card at `0:33`).
4. **Mid-film cliffs (Pacing / Picture) — `SECONDARY BOTTLENECK`:** `12.12%` Studio average viewed (`RSI 40↓ / 26↓↓`, well under the `25%` floor). Watching `0:40–1:20` shows slow `5–8 s` static starfield holds and generic SDO solar footage standing in for Proxima, with zero payoff on the title's `"(And It Has a Planet)"` hook in the first 80 seconds.
5. **End (End Screen / Handoff) — `SECONDARY BOTTLENECK`:** Watching `7:35–8:15` shows a clean timeline (`2016 -> 2031 -> 2035`), followed by a philosophical sign-off over observatory star trails fading to black at `8:14` with **no spoken next-video handoff**.

---

## 3. Gemini 4 Neon Watch Notes (Moving Video + Audio)

YouTube Analytics returned `0` retention points at `12` views (curve suppressed below threshold). Rather than guessing from text or stills, Gemini 4 Neon watched three `40 s` proxy diagnostic windows extracted directly from `026_NearestStar_v06_cfr18.mp4` with full moving video and audio:

1. **Window 1 — `0:00–0:40` (Opening hook; proxy for 0:30 drop):**
   - **0:00–0:07:** Opens on a generic Milky Way night-sky time-lapse (`"Look up on a clear night and the stars seem close, scattered just above the rooftops. So how far away is the nearest one?"`) then ISS solar panels (`0:04–0:07`). Proxima Centauri does not appear until **`0:17`**.
   - **0:08–0:19:** Dark desert sky with overlay `LIGHT FROM PROXIMA: More than 4 years`, then VLT observatory exterior (`0:13–0:16`), then Hubble Proxima still (`0:17–0:19`: `"You cannot see that star at all. Not without a telescope."`).
   - **0:20–0:32 (Direct Rule 10 violation):** Over an orbital diagram (`Which star it is`) and bar chart (`How long it takes`), VO reads a **12-second table-of-contents meta-promise**: *"In this film, I will show you which star it is, how anyone measured a distance that large, what that gap looks like if you shrink the whole thing down to fit on Earth, and how long it would take to get there."*
   - **0:33–0:40:** Chapter card `"The Star You Cannot See"` lands at `0:33` (inside the first `45 s`), breaking momentum right as viewers decide whether to stay.
2. **Window 2 — `0:40–1:20` (Typical exit zone around `1:00` Studio AVD):**
   - **0:40–0:50:** Two consecutive dense starfield stills (globular cluster / Milky Way) with slow zooms (`5 s` holds) while explaining Proxima is dim. Visually generic.
   - **0:50–0:59:** Cuts to blue UV and red solar close-up footage (reads like our Sun, not a dim red dwarf) with `PROXIMA BRIGHTNESS: Less than 1%`, then another generic starfield (`0:59–1:07`, `RED DWARF LIFETIME: Trillions of years`).
   - **1:08–1:20:** Night mountain ridge (`1:08–1:13`), then Alpha Centauri A & B (`1:14–1:18`). Calm ambient piano stays flat; the title's planet promise (`"And It Has a Planet"`) still has zero visual or spoken presence by `1:20`.
3. **Window 3 — `7:35–8:15` (End screen & handoff):**
   - **7:35–7:48:** Radio telescope dishes with clean animated timeline (`2016 Proxima b found -> 2031 Message arrives -> 2035 Earliest reply`).
   - **7:49–8:15:** Philosophical reflection (`"What if the most important thing about the nearest star is not how close it is, but how far... and we have only just begun to measure the gap."`) over star trails, fading to black at `8:14`. **Zero spoken handoff** to the next Orbit film or series playlist.

---

## 4. Concrete Fixes (Max 3)

1. **[this video — Description / End Screen / Shorts Link, read-only check first]:** Leave running Title & Thumbnail Test & Compare `T027` untouched (never replace a running test). Verify the first two lines of the description repeat the exact search query `"how far is the nearest star"` + `"Proxima Centauri"`, confirm the end screen points to the Space/Real Worlds playlist + `VBaYRPp85Sw` (*What Happened to Venus?*, `230` views, `25%` AVD), and re-read at `7 d` (`2026-11-22`) once `T027` collects impressions.
2. **[next film — Hook & Structure]:** Enforce zero `"In this film, I will show you…"` meta-promises and zero chapter cards before `0:45` on every new script/cut (`studio/RULES.md` lesson 7 / `LEARNINGS.md` rule 10), and show the title's concrete visual payoff (e.g. the planet itself when the title promises `"And It Has a Planet"`) within the first `15 s` instead of generic Milky Way / observatory B-roll.
3. **[next film — End Screen Handoff]:** Replace open-ended philosophical fades with an explicit 10-second spoken bridge into the exact clickable next film/playlist in the final `15 s` (`LEARNINGS.md` rule 20), keeping narration active up to the end-screen cut instead of fading out silently.

---

## 5. Repeatable Lesson for `LEARNINGS.md`

- Logged under **Rule 38** in `05_Analytics/LEARNINGS.md`: confirmed on watched video (`c5AdqQsnnys` `0:20–0:32` and `Js6EQJ8qDi8` `0:30–0:40`) that legacy October scripts carrying `"In this film, I will show you…"` table-of-contents agendas and early (`<0:45`) chapter cards coincide directly with `12–15%` average view duration; future scripts and re-cuts must pass the watched-hook check with zero meta-promise and an active spoken next-video handoff.
