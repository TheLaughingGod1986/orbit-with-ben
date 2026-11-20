# Retention Autopsy (7 d) — History of Science · `ETynHpIYLeY`

- **Film:** HOS 007 — *How Was the First Vaccine Made? (And Why It's Named After a Cow)* (`ETynHpIYLeY`)
- **Published:** `2026-11-12T18:00:36Z` · **Duration:** `8:52` (`532 s`)
- **Autopsy date:** `2026-11-20` (`J3256`, initial test run on HOS's newest public long; snapshot `2026-11-20`, age `180.7 h` = `7.5 d`, YTA through `2026-11-18`)
- **Reviewer:** Gemini (Gemini 4 Neon, moving video + audio verified via `read_file` on cut clips from `/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v04_J0925/hos_007_master_v04.mp4`)

---

## 1. Relative-Strength Score (RSI)

> **RSI (vs ch / niche):** `Showings 46→/0↓↓ · CTR 53→/53→ · Views 56↑/0↓↓ · Avg% 44↓/35↓ · 0:30 —/— · Subs/1k —/0↓↓`

*(Scale: `0–100` where `50→` = on benchmark; `70+ ↑↑` strong, `55–69 ↑` above, `45–54 →` inline, `31–44 ↓` below, `0–30 ↓↓` weak. Formula: `100 × value / (value + benchmark)`.)*

| Metric | Film (7 d / latest) | Channel median | Baseline basis | RSI (ch) | Niche outlier (`<50k`) | RSI (niche) |
|---|---:|---:|---|---:|---:|---:|
| Showings (Impressions) | `44` *(13 at 48 h)* | `52.5` | lifetime Studio longs (`n=6`) | `46→` | `80,000` | `0↓↓` |
| Click-through (CTR) | `4.6%` *(15.4% at 48 h)* | `4.05%` | lifetime Studio longs (`n=6`) | `53→` | `4.0%` | `53→` |
| Views | `5` *(7 by day 7.5)* | `4.0` | same-age 7 d snapshots (`n=3`) | `56↑` | `4,700` | `0↓↓` |
| Average % viewed | `19.17%` *(Studio 1:42; YTA 28.49% / 2:31)* | `24.77%` | lifetime Studio/YTA longs (`n=6`) | `44↓` | `35.0%` | `35↓` |
| 0:30 retention | `—` *(suppressed at 7 views)* | `—` | insufficient history (`<3` curves) | `—` | `60.0%` | `—` |
| Subscribers / 1,000 views | `0.0` (`0` subs) | `0.0` | lifetime YTA longs (`n=6`) | `—` | `10.0` | `0↓↓` |

- **Niche outlier source:** `05_Analytics/hos/search_research/2026-11-20.md` (`<50k` discovery/history outliers `1.5k–61.9k`, anchored at `Industrial Case Files` 138-sub `4.7k`) & `HOS-2026-11-E2` (`60%` 0:30 target).
- **Traffic sources (YTA through 18 Nov):** `YT_SEARCH: 3`, `NO_LINK_OTHER: 1`, `EXT_URL: 1` (`0` Browse/Suggested; matches `05_Analytics/hos/AUDIT_2026-11.md` finding that all three Vaccine uploads received `0%` Suggested / near-zero feed distribution).

---

## 2. Funnel Diagnosis (Strict Priority Order)

**Primary bottleneck: Step 1 — Showings (Topic / Search)** *(secondary: Step 3 Hook, Step 4 Picture consistency, Step 5 End screen & tail — all caught directly on video watch).*

1. **Showings (Topic / Search) — `PRIMARY BOTTLENECK`:** Only `44` impressions in `7.5` days (`13` at 48 h) against a `500`-impression 7 d floor and `80,000` niche outlier bar (`RSI 46→ / 0↓↓`). `0%` Suggested/Browse traffic and both vaccine Shorts (`cLKDiYP55J8`, `xgx2lYHhYZM`) were unfed (`LEARNINGS.md` rule 36), pointing squarely to **topic/health-category suppression** rather than packaging failure.
2. **Click-through (Packaging) — `UNMEASURED (low sample)`:** `4.6%` CTR on `44` impressions is slightly above both HOS median (`4.05%`) and niche bar (`4.0%`, `RSI 53→ / 53→`), though sample `<100` impressions is too small to call packaging a win or loss. Title + Thumbnail Test & Compare was set at launch per `LAUNCH_PLAN.md`; do not disturb if running.
3. **First 30 seconds (Hook) — `SECONDARY BOTTLENECK`:** YouTube suppressed the 0:30 curve at `7` views. Direct watch of `0:00–0:40` reveals **two concrete defects**: (a) a missing-glyph tofu box **`VACCA □ VACCINE`** right at `0:01–0:03`, and (b) a **13-second meta-promise** (`"By the end of this film, you'll know how…"`, `0:09–0:22`), followed by a flat 2D map style break at `0:29`.
4. **Mid-film cliffs (Pacing / Picture) — `SECONDARY BOTTLENECK`:** Studio average viewed is `19.17%` (`1:42`, `<25%` floor, `RSI 44↓ / 35↓`), though YTA settled views (`n=5`) averaged `28.49%` (`2:31`). Watching `1:22–2:02` and `2:11–2:51` shows strong 3D storytelling overall, but `1:40` hits a flat brown chapter card right on Studio's `1:42` AVD, `2:11–2:15` opens with a slow `"Imagine being a milkmaid…"` walk, and the gentle piano bed stays completely monotone with zero rhythmic shift between tension and explanation.
5. **End (End Screen / Handoff) — `SECONDARY BOTTLENECK`:** Watching `8:12–8:52` exposes **21 full seconds of voice-free montage (`8:31–8:52`)** after the `Next film` card (`8:27–8:30`), PLUS a **target mismatch**: the spoken/card handoff promises *"Why Did Franklin Fly a Kite in a Storm? · Thursday 19 November"* (not yet live when `007` aired on `12 Nov`), while the clickable end screen in `PACKAGE_MANIFEST.json` points to `001 Germs` (`_C92tIJCk8A`).

---

## 3. Gemini 4 Neon Watch Notes (Moving Video + Audio)

YouTube Analytics returned `0` retention points at `7` views (curve suppressed). Gemini 4 Neon watched four `40 s` diagnostic windows cut directly from `hos_007_master_v04.mp4` with moving video and audio:

1. **Window 1 — `0:00–0:40` (Opening hook):**
   - **0:00–0:03:** Lush 3D cartoon cow in sunlit pasture (`"Every vaccine in the world is named after a cow."`) — strong frame-0 visual, **marred by a missing-glyph tofu square in the subtitle overlay: `VACCA □ VACCINE`** (missing Unicode arrow glyph in Didot/font).
   - **0:04–0:08:** 3D velvet-lined wooden medical case with lancet and vials (`"So how did a cow end up inside the most important medicine ever made?"`). Strong apparatus plate.
   - **0:09–0:22:** **13-second meta-promise** (*"By the end of this film, you'll know how a milkmaid's hand, a country doctor, and one careful test turned an old farmyard rumour into the medicine that wiped a disease off the face of the earth."*) over a bucket/box/book table pan (`0:12–0:18`, `A PAIL · A LANCET · A BOOK`) and spinning glowing globe (`0:19–0:22`).
   - **0:29–0:34:** Jarring **2D flat-vector brown map** (`THE SPECKLED MONSTER`) with black outlines and drifting brown ovals breaks the premium 3D cartoon house lock between the 3D church (`0:23–0:28`) and 3D wooden peg-doll fatality count (`0:35–0:38`, `3 in 10 died`).
2. **Window 2 — `1:22–2:02` (Around `1:42` Studio AVD):**
   - **1:22–1:39:** Smooth 3D village, mother at window, sleeping child in cradle (`"If it were your child, which would you choose?"`), steaming farmyard buckets. Good emotional pacing.
   - **1:40–1:42:** Flat brown chapter card (`The Milkmaids' Secret`) lands right at Studio's `1:42` average exit.
   - **1:43–2:02:** Milkmaid milking cow (`COWPOX`), inspecting spots (`A MILD ILLNESS`, slight uncanny wide grin while discussing sores), recovering and stretching (`1:55–1:59`), walking with friend (`2:00`).
3. **Window 3 — `2:11–2:51` (Around `2:31` YTA AVD):**
   - **2:11–2:15:** Slow `4.5 s` shot of milkmaid walking into a dark barn (`"Imagine being a milkmaid in a smallpox year"` — passive `"Imagine…"` framing).
   - **2:16–2:48:** Stronger sequence: market walk (`"WE NEVER CATCH IT"`), farmers at gate, Benjamin Jesty WHO card (`Benjamin Jesty / 1736–1816 · Dorset farmer`), tortoise-shell lancet scratching arm (`Dorset, 1774`), Jesty seated silently shaking head. Throughout `0:00–2:51`, the background piano stays uniformly soft and lullaby-paced — no rhythmic/arpeggiated shift for teach segments (`studio/RULES.md` Polish pass §2).
4. **Window 4 — `8:12–8:52` (End screen & handoff):**
   - **8:12–8:26:** Explorer beside cow, dark storm clouds and Franklin's kite in lightning (`"Long before Jenner, another mystery frightened people every summer. To solve it, a printer in Philadelphia flew a kite into a thunderstorm."`).
   - **8:27–8:30:** Cream-on-brown card: `Next film · Thursday 19 November · Why Did Franklin Fly a Kite in a Storm?`.
   - **8:31–8:52:** **21 full seconds of narration-free music montage** (grazing cow, village flyover, villagers entering cottage, hand pulling book off shelf, fade to black) — drags down average % viewed and leaves viewers with nothing clickable matching the Franklin card (end screen links to `001 Germs`).

---

## 4. Concrete Fixes (Max 3)

1. **[this video — End Screen, once HOS 008 Franklin is live]:** Keep health/vaccine off the 2027 topic slate (`05_Analytics/hos/search_research/2026-11-20.md` — non-health adult Anglosphere clusters only). On `ETynHpIYLeY` itself, once HOS 008 (*Why Did Franklin Fly a Kite in a Storm?*) is public, update the YouTube end-screen element from `001 Germs` (`_C92tIJCk8A`) to HOS 008 so the clickable card matches the film's spoken & on-screen Franklin handoff (read-only until 008 is public; leave any running Test & Compare untouched).
2. **[next film — Pre-render Glyph & Style QA (`009+`)]:** Add a hard font-glyph check before final render so missing Unicode symbols (`→` rendering as `□` in `VACCA □ VACCINE` at `0:01`) hard-fail QA, ban `"By the end of this film, you'll know…"` meta-promises in the first 30 s, and ban flat 2D black-outlined vector maps that break the 3D cartoon / inked-parchment house style.
3. **[next film — Ending Length & Music Contrast (`009+`)]:** Trim post-narration outro tails from `21 s` to **`≤ 5 s`** (narrate directly into the end-screen bridge pointing to an already-public film or series playlist so AVD is not diluted by a 21-second silent montage), and add distinct rhythmic/plucked music beds on teach parts (`studio/RULES.md` Polish pass §2).

---

## 5. Repeatable Lesson for `LEARNINGS.md`

- Logged under **Rule 38** in `05_Analytics/LEARNINGS.md`: (1) HOS `ETynHpIYLeY` (`0:01`) shipped a rendered tofu glyph box (`VACCA □ VACCINE`) and a `21 s` silent-voice outro (`8:31–8:52`) that dilutes AVD and mismatches the end screen — both immediately caught when Gemini 4 Neon watched moving video + audio; (2) confirms `AUDIT_2026-11.md` that vaccine/health topics receive `0%` Suggested reach on HOS (`44` impressions in `7.5 d`).
