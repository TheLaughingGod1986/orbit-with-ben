# Retention Autopsy (7 d) — Orbit With Ben · `c5AdqQsnnys`

- **Film:** OWB 026 — *How Far Is the Nearest Star? (You Can't See It, and It Has a Planet)* (`c5AdqQsnnys`)
- **Published:** `2026-11-15T18:00:37Z` · **Duration:** `8:15` (`495 s`)
- **Autopsy date:** `2026-11-22` (`J3388`; daily snapshot `2026-11-22` taken `2026-11-22T06:40:09Z` [`156.7 h` age], Studio reach/AVD read `2026-11-22T07:12:37Z` [`05_Analytics/owb/studio_ctr.json`], YTA through `2026-11-20`)
- **Prior autopsy:** `05_Analytics/owb/autopsy/c5AdqQsnnys_48h.md` (`2026-11-20`, `J3256`)
- **Reviewer:** Gemini (`gemini`, Gemini 4 Neon — moving video + audio verified via `read_file` on three `40 s` clips extracted from `/Volumes/data/mac-mini-archive/youtube-staging/026/026_NearestStar_v06_cfr18.mp4`, `SHA-256: 6e587bb5ac33552cef55ac897d89f5516a90acef9473155254dd313fc73e09d3`)

---

## 1. Relative-Strength Score (RSI)

> **RSI (vs ch / niche):** `Showings 20↓↓/0↓↓ · CTR 81↑↑/67↑ · Views 67↑/0↓↓ · Avg% 47→/36↓ · 0:30 —/— · Subs/1k —/0↓↓`

*(Scale: `0–100` where `50→` = on benchmark; `70+ ↑↑` strong, `55–69 ↑` above, `45–54 →` inline, `31–44 ↓` below, `0–30 ↓↓` weak. Formula: `100 × value / (value + benchmark)`.)*

| Metric | Film (7 d / latest) | 48 h -> 7 d change | Channel median | Baseline basis | RSI (ch) | Niche outlier (`<50k`) | RSI (niche) |
|---|---:|---|---:|---|---:|---:|---:|
| Showings (Impressions) | `24` | `9` (48 h) -> `23` (d5) -> `24` (d7; `+1` in 48 h) | `95.5` | lifetime Studio longs (`n=16`) | `20↓↓` | `80,000` | `0↓↓` |
| Click-through (CTR) | `8.3%` (`2/24` clicks) | `11.1%` (48 h) -> `4.4%` (d5) -> `8.3%` (d7) | `1.9%` | lifetime Studio longs (`n=16`) | `81↑↑` | `4.0%` | `67↑` |
| Views | `14` *(13 Studio; 12 YTA)* | `8` (48 h) -> `12` (d5) -> `14` (d7) | `7.0` | same-age 7 d snapshots (`n=7`) | `67↑` | `5,000` | `0↓↓` |
| Average % viewed | `19.4%` *(Studio `1:36`; YTA `12.2%` / `1:00`)* | `12.12%` (48 h Studio) -> `19.4%` (d7 Studio) | `21.6%` | lifetime Studio/YTA longs (`n=16`) | `47→` | `35.0%` | `36↓` |
| 0:30 retention | `—` *(suppressed at 12–14 views)* | unchanged (`0` YTA curve points) | `38.3%` | lifetime YTA curves (`n=8`) | `—` | `60.0%` | `—` |
| Subscribers / 1,000 views | `0.0` (`0` subs, `0` likes) | unchanged (`0` subs) | `0.0` | lifetime YTA longs (`n=16`) | `—` | `10.0` | `0↓↓` |

- **Niche outlier source:** `05_Analytics/new_channel_research/SUMMARY.md` (`<50k` space/science peers: Stellar `4,964` median, Simple Science `1,631`, Science Into Sleep `1,323`, Orbitra `21k–38k`) and `05_Analytics/LEARNINGS.md` rules 10, 23, 34, 37.
- **Traffic sources (YTA through `2026-11-20`, `12` views / `11` watch minutes):** `NO_LINK_OTHER: 10`, `YT_SEARCH: 2`, `0` Browse, `0` Suggested, **`0` `SHORTS_CONTENT_LINKS`**.
- **Linked Shorts transfer check (Rule 17 early signal):** Two public 026 Shorts with `Related -> c5AdqQsnnys` verified in `J0861` accumulated **`503` combined views** by 22 Nov — `aEfdxex__Bo` (*If You Can't See the Nearest Star, How Far Away Is It?*, `476` views, `37.1%` stayed, `151.7%` avg viewed `LOOP`) and `dH_yCRmzkMo` (*If Voyager Needs 75,000 Years, How Far Is the Nearest Star?*, `27` views, `92.3%` stayed, `79.5%` avg viewed) — yet drove **`0` tracked `SHORTS_CONTENT_LINKS` views** to `c5AdqQsnnys` through 20 Nov (third Short `aAUgIGEuPwQ` moved to `2026-11-27T11:30Z` under Rule 35).

---

## 2. Funnel Diagnosis (Strict Priority Order)

**Primary bottleneck: Step 1 — Showings (Topic / Search)** *(secondary confirmed bottlenecks: Step 4 Mid-Film Pacing/Picture at `19.4%` Studio AVD, plus watched-cut Hook and End-Handoff faults).*

1. **Showings (Topic / Search) — `PRIMARY BOTTLENECK`:** Only `24` impressions at 7 d (far below the `500`-impression 7 d floor, `95.5` channel median `RSI 20↓↓`, and `80,000` niche outlier `RSI 0↓↓`). Impressions effectively stalled after day 5 (`23 -> 24`, only `+1` impression in ~48 h), with just `2` search views, `0` Browse/Suggested, and `0` Shorts-link views. The upload description (`Descriptions/nearest_star_long_description_v01.txt`) already leads line 1 with `"How far is the nearest star? Proxima Centauri..."` and tags include `"how far is the nearest star"`, so this is not a missing-keyword fault — it confirms **Rule 34** (single-question longs on a small channel do not trigger Browse/Suggested discovery) and **Rule 37** (search-led demand & results-page gap verification required before topic lock from 1 Jan 2027).
2. **Click-through (Packaging) — `UNMEASURED (low sample)`:** `8.3%` CTR (`2` clicks on `24` impressions) is well above benchmarks (`RSI 81↑↑ / 67↑`), but `24` impressions is far below the `100`-impression minimum sample needed to diagnose packaging. Title & Thumbnail Test & Compare **`T027`** (`J2497`, armed `2026-11-10`: Arm A *"How Far Is the Nearest Star? (You Can't See It, and It Has a Planet)"* + `11-DAY YEAR` vs Arm B *"The Star Next Door Is Invisible (And It Will Outlive Our Sun)"* + `TRILLIONS OF YEARS`) is **still running** and cannot reach significance at `24` impressions (confirming Rules 5 & 13). **Guard: do not touch or replace `T027`.**
3. **First 30 seconds (Hook) — `UNMEASURED (curve suppressed) / WATCHED BOTTLENECK`:** YouTube Analytics returned `0` retention points at `12–14` views. Re-watching `0:00–0:40` with audio confirms the Rule 10 / Lesson 7 opening violations: generic Milky Way + ISS B-roll (`0:00–0:07`), Proxima Centauri withheld until `0:17`, a **12-second table-of-contents meta-promise** (`0:20–0:32`: *"In this film, I will show you which star it is..."*), and a chapter card (`"The Star You Cannot See"`) at **`0:33`** (violating the `<0:45` card lock).
4. **Mid-film cliffs (Pacing / Picture) — `SECONDARY BOTTLENECK`:** Studio average viewed rose from `12.12%` (`1:00`) at 48 h to **`19.4%` (`1:36` / `96 s`)** at 7 d (`RSI 47→ / 36↓`), still below the `25%` funnel floor (YTA through 20 Nov is `12.2%` / `1:00`). Because Studio AVD shifted to `1:36`, this 7 d autopsy inspected the **new typical-exit window `1:16–1:56` (`76–116 s`)** directly with moving video + audio and found four concrete pacing/visual issues clustering around the `1:36` exit: a literal visual mismatch (crescent exoplanet over *"brightest points in the whole night sky"* at `1:19–1:22`), repeated generic nebula plates (`1:22–1:28`, `1:44–1:48`), an orbital diagram (`1:28–1:33`) visually duplicating `0:20–0:24`, and a **direct repeat of the `0:38` globular-cluster still at `1:33–1:38` right across the `1:36` typical exit**, followed by a textbook `"A light-year is a distance, not a time"` detour at `1:48` while the title's promised planet (`"(And It Has a Planet)"`) is held back until chapter 5 (`6:18`, 76% into the film).
5. **End (End Screen / Handoff) — `UNMEASURED (curve suppressed) / WATCHED BOTTLENECK`:** End curve is suppressed at low views. Watching `7:35–8:15` confirms a crisp `2016 -> 2031 -> 2035` timeline (`7:35–7:38`), followed by a `27 s` open-ended philosophical reflection (`7:48–8:15`) fading to black at `8:14` with **zero spoken handoff** to the next Orbit film or series playlist. In addition, `PACKAGE_MANIFEST.json` records `"playlistId": null` and `J2497` did not read back individual end-screen elements.

---

## 3. Gemini 4 Neon Watch Notes (Moving Video + Audio)

YouTube Analytics suppressed the retention curve (`0` points at `12` YTA / `14` live views). Rather than inferring from stills or text, Gemini 4 Neon extracted all three 7 d proxy windows via `scripts/retention_autopsy.py clips` from the verified uploaded master `026_NearestStar_v06_cfr18.mp4` and watched every clip with full moving video and audio via `read_file`:

1. **Window 1 — `0:00–0:40` (`owb_c5AdqQsnnys_drop1_0000_0040.mp4`, Opening hook; proxy for 0:30 drop):**
   - **0:00–0:07:** Generic Milky Way horizon time-lapse (`0:00–0:03`, *"Look up on a clear night and the stars seem close, scattered just above the rooftops"*) cuts to ISS solar panels over Earth's airglow (`0:04–0:07`, *"So how far away is the nearest one?"*). Neither shot shows the titled star or planet.
   - **0:08–0:19:** Dark desert sky with overlay `LIGHT FROM PROXIMA: More than 4 years` (`0:08–0:13`), VLT observatory domes (`0:13–0:16`), and finally Hubble's Proxima Centauri still at **`0:17–0:19`** (*"You cannot see that star at all. Not without a telescope."*).
   - **0:20–0:32 (Rule 10 violation):** Animated orbital diagram (`Which star it is` — Alpha Centauri A, B + Proxima Centauri, `0:20–0:24`), generic red/blue nebula (`0:24–0:28`), and animated speed-comparison bars (`How long it takes` — Walk / Car / Jet / Voyager 1 / Light, `0:28–0:32`) play under a **12-second table-of-contents meta-promise**: *"In this film, I will show you which star it is, how anyone measured a distance that large, what that gap looks like if you shrink the whole thing down to fit on Earth, and how long it would take to get there."*
   - **0:33–0:40:** Chapter card `"The Star You Cannot See"` lands at **`0:33`** over the reused Hubble Proxima still (`<0:45` violation), cutting at `0:38` to a bright globular-cluster still as VO introduces Proxima as a red dwarf.

2. **Window 2 — `1:16–1:56` (`owb_c5AdqQsnnys_drop2_0076_0116.mp4`, New 7 d typical-exit zone around `1:36` Studio AVD):**
   - **1:16–1:19 (`clip 0:00–0:03`):** Hubble still of `ALPHA CENTAURI A, B` (`About 4.37 light-years`).
   - **1:19–1:22 (`clip 0:03–0:06`, Visual mismatch):** While VO says *"From the southern hemisphere, they shine as one of the brightest points..."*, the cut shows a **dark crescent planet in the upper-right corner** rather than the southern night sky.
   - **1:22–1:28 (`clip 0:06–0:12`, Generic filler):** `6 s` slow push on a pink/blue star-forming nebula still over *"...in the whole night sky. From Britain, they never rise."*
   - **1:28–1:33 (`clip 0:12–0:17`, Repeated diagram look):** `One family: 3 stars` orbital animation (`Proxima loops around`, `Bright pair (A, B)`, `Half a million years`) — visually almost identical to the `Which star it is` orbital diagram already shown 68 seconds earlier at `0:20–0:24`.
   - **1:33–1:38 (`clip 0:17–0:22`, Exact `1:36` AVD — Reused still):** Cuts back to the **exact same globular-cluster still already used at `0:38`** (`5 s` static push) while VO explains *"at a vast distance, and one orbit takes it about half a million years."*
   - **1:38–1:44 (`clip 0:22–0:28`, Second observatory exterior):** `6 s` VLT telescope dome with yellow laser guide star (second VLT exterior in the first two minutes, after `0:13–0:16`) over *"When anyone says the nearest star, they mean the faint one..."*
   - **1:44–1:51 (`clip 0:28–0:35`, Fact repetition + textbook detour):** Another generic pink/teal nebula still (`PROXIMA CENTAURI / 4.24 light-years away`, repeating the `4+ light-years` fact from `0:08–0:12`), then ISS airglow limb (`1:48–1:51`) while VO detours into *"A light-year is a distance, not a time."* Still zero spoken or visual payoff on the title's promised planet (`Proxima b` does not arrive until `6:18`).
   - **1:51–1:56 (`clip 0:35–0:40`):** Clean `Travels in a year` light-pulse animation (`Proxima -> Earth`, `1 year` progress bar). Audio bed stays a uniform calm ambient piano/synth throughout the entire `40 s` window with no tempo shift or SFX accents.

3. **Window 3 — `7:35–8:15` (`owb_c5AdqQsnnys_drop3_0455_0495.mp4`, End screen & next-video handoff):**
   - **7:35–7:38 (`clip 0:00–0:03`):** Daytime radio telescope dish with crisp animated timeline (`2016 Proxima b found -> 2031 Message arrives -> 2035 Earliest reply`).
   - **7:38–7:48 (`clip 0:03–0:13`):** Nighttime radio array (`7:38–7:43`) cuts to a stark high-contrast white-lit antenna truss (`7:43–7:48`) as VO summarises *"So this is the nearest star. A faint red sun you cannot see, more than four light-years away, with a world we cannot yet know."*
   - **7:48–8:15 (`clip 0:13–0:40`):** Milky Way panorama (`7:48–7:53`), VLT laser exterior reused a third time (`7:53–7:56`), telescope star-trails (`7:56–8:07`), and dome time-lapse (`8:07–8:13`) fading to black at `8:14`. VO spends the final `27 s` on an open-ended philosophical coda (*"What if the most important thing about the nearest star is not how close it is, but how far... and we have only just begun to measure the gap."*) with **no spoken next-video handoff** or playlist bridge.

---

## 4. Concrete Fixes (Max 3)

1. **`[this video — Playlist & End-Screen Audit Only; Keep T027 Untouched]`:** Leave running Title & Thumbnail Test & Compare `T027` strictly undisturbed (never replace a running test; `24` impressions is simply too small for any test to decide). The live description already leads with the exact search phrase (`"How far is the nearest star? Proxima Centauri..."`). The only safe `this video` clean-up is **Rule 20 wiring**: `PACKAGE_MANIFEST.json` has `"playlistId": null` and `J2497` did not verify individual end-screen elements — add `c5AdqQsnnys` to the Orbit *Real Worlds* / Space series playlist (playlist addition does not disturb `T027`) and, once `T027` ends, confirm its end screen points to that playlist + `VBaYRPp85Sw` (*What Happened to Venus?*, `232` views).
2. **`[next film — Early Title-Payoff + Zero Visual Mismatches or Repeats in Minutes 0–2]`:** Extending Rule 38 (no `"In this film, I will show you…"` agendas and no `<0:45` chapter cards), enforce two watched-picture checks across `0:00–2:00` on every upcoming cut: (a) **tease or show every title hook within the first 60–90 s** (never withhold a titled planet like `"(And It Has a Planet)"` until `6:18` while detouring into textbook definitions like `"A light-year is a distance, not a time"` at `1:48`); and (b) **zero literal visual mismatches, generic nebula filler, or B-roll/diagram repeats in minutes 0–2** (caught directly across `1:16–1:56`: crescent planet over "southern night sky" at `1:19`, duplicate orbital diagram at `1:28`, and the `0:38` globular-cluster still repeated directly across the `1:36` AVD).
3. **`[next film — Spoken End-Screen Bridge & Search-Led Topic Gate]`:** Replace open-ended `25–30 s` philosophical codas (`7:48–8:15`) with an explicit `10–15 s` spoken handoff naming the clickable end-screen video/playlist (`Rule 20`), and keep single-question Orbit longs paused (`Rule 34`) until December's format tests read out and the 1 Jan 2027 search-led topic method (`Rule 37`) takes effect — reinforced by `026`'s two linked Shorts (`503` combined views) transferring `0` tracked `SHORTS_CONTENT_LINKS` views into the long.

---

## 5. Repeatable Lesson for `LEARNINGS.md`

- Appended to **Rule 38** evidence in `05_Analytics/LEARNINGS.md`: on `c5AdqQsnnys` at `7 d` (`24` impressions, `+1` in 48 h, `19.4%` / `1:36` Studio AVD), watching the shifted `1:16–1:56` typical-exit window with moving video + audio revealed that **early B-roll/diagram repetition (`0:38` globular-cluster still reused at `1:33–1:38` right across `1:36` AVD; `0:20` orbital diagram look repeated at `1:28`), literal visual mismatches (crescent planet over "southern night sky" at `1:19`), and withholding a title promise (`"(And It Has a Planet)"` delayed until `6:18`) cluster directly at the typical viewer exit**, while `503` combined views on its two linked Shorts drove `0` tracked `SHORTS_CONTENT_LINKS` views (early signal on Rule 17 alongside HOS Rule 29's `0/5` readout).
