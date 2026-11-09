# J2148 — Rule-E Topic + Script Review: OWB 033 (*Why Knocked-Sideways Uranus Has 21-Year Winters*)

- **Date:** 4 November 2026
- **Reviewer:** `gemini` (`gemini-argon`, specialist Rule-E reviewer)
- **Film:** `OWB:033` (`02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters`)
- **Authority:** `AGENTS.md` Rule E (*"Topic and script calls are reviewer calls, not Chief calls... Go queues the next stage at once."*). Supersedes earlier Chief topic jobs (`J1896`, `J1969`, `J1970`) after `OWB:033` entered active production (`jobs/WIP.json`, limit raised to 8 by Ben on 4 Nov 2026).
- **Verdict:** **GO** — topic (`033 topic`) and script (`033 script`, `uranus_21_year_winter_script_master_v02.md`) **LOCKED** (`done`); VO job queued (`kind: vo`, `--film 033 --stage vo`).

---

## Rubric Evaluation

### (1) Neighbour Check & No Near-Duplicate (`PASS`)

- **No near-duplicate on OWB or HOS:** Checked all OWB (`001`–`032`) and HOS (`001`–`010`) live, scheduled, and active films. Neither channel has a live, scheduled, or active long on Uranus. (`033` directly follows `032` Titan's outer-solar-system exploration arc; unlocked draft `052` Miranda waits in `WIP.json` `next`.)
- **Qualifying 1M+ education/space neighbour pool (10 videos verified via `yt-dlp` on 4 Nov 2026, logged in `11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md` and `PRE_BUILD_VIDIQ_AUDIT.md`):**
  1. `rHLifi-VzSQ` — *Falling Into Uranus (Simulation)* (Stargaze) — **7,632,521 views** (`2024-02-09`, `5:38`)
  2. `Nru_XeafheY` — *What If You Spent 5 Seconds on Uranus?* (What If) — **2,891,295 views** (`2023-10-08`, `8:18`)
  3. `ckdJ4945dHs` — *Uranus is officially the weirdest planet in our solar system* (Insider Tech) — **2,632,734 views** (`2017-06-28`, `1:51`)
  4. `tCmC0XOKO5Q` — *The Bizarre Characteristics Of Uranus | Our Solar System's Planets* (Astrum) — **2,573,227 views** (`2021-01-05`, `13:38`)
  5. `1hIwD17Crko` — *Uranus & Neptune: Crash Course Astronomy #19* (CrashCourse) — **2,121,597 views** (`2015-05-28`, `12:19`)
  6. `UOUM1QT5GgU` — *Voyager 2 Found Something Impossible at the Edge of Space* (The Infographics Show) — **1,957,819 views** (`33:15`)
  7. `q7HMd2FyFqk` — *Why is Uranus On Its Side? | The Planets | BBC Earth Science* (BBC Earth Science) — **1,925,164 views** (`2021-12-05`, `6:29`)
  8. `WJ1KJhC0SOo` — *What Would You See If You Fell Into Uranus? (4K UHD)* (V101 SPACE) — **1,873,603 views** (`2019-11-23`, `8:47`)
  9. `wKcMvR2C0oA` — *Is Uranus Actually a Rock Giant?* (Astrum) — **1,451,014 views** (`2026-02-26`, `24:38`)
  10. `pZh5BWCNmmE` — *Uranus: The Weirdest Planet in the Solar System* (Astrum) — **1,243,196 views** (`2026-10-27`, `39:56`)

### (2) Audience Evidence (`PASS`)

- **Our own Short on the exact topic (`ZpEA8stoSPA`, *Why Does Uranus Have 21-Year Winters?*):** Went public on OWB on `2026-11-03T11:30:13Z` and reached **461 views and 6 likes in its first 24 hours** (`05_Analytics/owb/snapshots/2026-11-04.json`), more than **2.3×** the 200-view Short-first benchmark on day 1.
- **Recent reference-channel velocity:** Astrum's *Uranus: The Weirdest Planet in the Solar System* (`pZh5BWCNmmE`, uploaded 27 Oct 2026) accrued **1,243,196 views in 8 days**; BBC Earth Science's *Why is Uranus On Its Side?* (`q7HMd2FyFqk`) sits at **1,925,164 views**.

### (3) Script Master Polish (`v02`) & Every Number Sourced in `SOURCES.md` (`PASS`)

- **Small script points fixed in `01_Script/uranus_21_year_winter_script_master_v02.md` (with `v01.md` preserved byte-identical):**
  1. **Opening (LEARNINGS rule 10):** Removed the negative opener (*"Not for twelve hours."*) and the three-question agenda sentence; opens directly on the 21-year polar winter claim and immediate question (*"At the north pole of Uranus, the seventh planet in orbit around our Sun, what would you see when the Sun sinks below the horizon? A single winter night that lasts twenty-one Earth years."*), followed by the 97.77° vs Earth 23.44° tilt, −224.2 °C vs Neptune, and one central question before 0:45.
  2. **Spoken word count:** Trimmed from 1,338 spoken words (`v01`) to **1,290 spoken words** (`v02`, 1,347 reviewer words, ~9.0 min), strictly inside the `1,200–1,300` spoken word target.
  3. **Subscribe beat:** Updated to line 6 of `templates/SUBSCRIBE_BEAT_LINES.md` (*"If you've enjoyed the ride so far, subscribing is the best way to help Orbit keep going."*, 17 words at 43% of spoken words), avoiding lines 4 and 8 used in `029`–`032`.
  4. **Every spoken & visual number verified in `01_Script/SOURCES.md` and `01_Script/CLAUDE_QUOTE_CHECK_v01.md` (15/15 rows `VERIFIED` against live NASA Science, NSSDCA, and LOC pages on 4 Nov 2026):**
     - Hook: 7th planet, 21-Earth-year polar winter, 97.77° Uranus tilt vs 23.44° Earth tilt (>4× Earth's tilt), −224.2 °C (rows 1, 10).
     - Ch 1: 13 March 1781, William Herschel (1738–1822), two years later (1783), Johann Elert Bode (1747–1826), 51,118 km diameter (4× Earth; nickel vs softball), 2.9 billion km (19 AU / 19× Earth's distance), 2 h 40 min sunlight travel, 84 Earth years (rows 2, 3, 4).
     - Ch 2: 10 March 1977, star SAO 158687, 13 faint rings (9 dark grey inner + 2 found in 1986 + 2 outer discovered by Hubble on 22 Dec 2005 and imaged in 2006), 28 known moons, 97.77° tilt, ~17-hour day (17.24 h vs Earth's 24.0000 h, ~7 h shorter), quarter of 84-year orbit = 21-year winter (rows 1, 5, 6, 7).
     - Ch 3: 24 January 1986, >3 billion km in 9 years, Voyager 2 within 81,500 km of cloud tops, 6 hours, 10 new moons, 2 new rings, 82.5% H2 / 15.2% He / 2.3% CH4, 49 K (−224.2 °C), Neptune >30× Earth's distance vs Uranus 19× (rows 8, 9, 10).
     - Ch 4: Twenty-one years later, December 2007 equinox, winds up to 900 km/h (560 mph; >2× Earth's 400 km/h / 250 mph strongest winds), magnetic axis tilted nearly 60° (58.6°) and offset by 1/3 radius (0.352 Ru), 17-hour spin, millions of miles corkscrew magnetotail (rows 11, 12).
     - Ch 5: −224 °C sky, ≥80% hot dense fluid (water, methane, ammonia), 9,000 °F (4,982 °C, >5,000 °C hotter than the −224.2 °C cloud tops) (row 13).
     - Ch 6: 16 February 1948, Gerard Kuiper (1905–1973), January 1986, Miranda ~500 km diameter (1/7 of Earth's Moon), canyons up to 12× Grand Canyon depth, 10-minute cliff fall, 19 April 2022 Decadal Survey 2023–2032, October 2024 Hubble + New Horizons From 2 viewpoints (rows 14, 15).
  5. **Teach on screen & Polish pass markers:** `DATA: 7`, `SCALE: 7`, `WHO: 3` (all named people in VO have sourced WHO cards), `WHEN: 5` (all 11 spoken dates/spans mapped to the timeline), `FACT: 4` (all ≤ 4 words: `First telescope planet`, `28 literary moons`, `Six hours at Uranus`, `No solid surface`), `NUMBER OBJECT: 7` (hook + chapters 1–6), and 15–20 s moving end-screen picture at the close.

### (4) New Reference-Channel Rules (`LEARNINGS` 18, 19, 20) (`PASS`)

Recorded in `11_Upload-Package/metadata_DRAFT_v01.json`, `description_DRAFT_v01.txt`, and `PRE_BUILD_VIDIQ_AUDIT.md`:
1. **Series (`LEARNINGS` rule 20):** **`Real Worlds`**.
   - End screen: `Real Worlds` series playlist + next film in the series (`034` Pluto once public, else latest public `Real Worlds` long).
   - Description line: `Next in the series: Why Pluto's Frozen Heart Has Zero Craters` (and spoken hand-off in Ch 6).
2. **Real-imagery title variants (`LEARNINGS` rule 18, ≤ 50 chars per rule 15):**
   - Scenario/stakes title (Rule 15): `Why Knocked-Sideways Uranus Has 21-Year Winters` (**47 chars**)
   - Real-imagery variant 1 (Rule 18): `What Voyager 2 Saw in Just 6 Hours at Uranus` (**44 chars** — sells the real January 1986 Voyager 2 encounter imagery + sourced 6-hour flyby window)
   - Real-imagery variant 2 (Rule 18): `The Only Spacecraft Photos Ever Taken at Uranus` (**47 chars** — `"Only"` is proved verbatim by `SOURCES.md` row 8 from `science.nasa.gov/uranus/exploration/`: *"Only one spacecraft has visited distant Uranus"* / *"made the first – and so far the only – visit to Uranus"*).
3. **Real spacecraft frame for the Rule-19 thumbnail (Concept A):**
   - **NASA/ESA/CSA James Webb Space Telescope NIRCam real frame `PIA25770` (`STScI-01GWQ3`, 2023)** showing Uranus tipped on its side with its glowing vertical rings and bright polar cap in a single clean spacecraft exposure (or **NASA/JPL Voyager 2 real frame `PIA18182`**, 24 Jan 1986), graded to mean saturation ≥ 100 (target 120) and near-black ≤ 30%, no composite, with a 2-word top-band hook `21-YEAR WINTER` (yellow word `21-YEAR`). Paired in Test & Compare with Concept B (`10-MINUTE DROP`, Miranda cliff scale from Voyager 2 `PIA00141`) and Concept C (`KNOCKED SIDEWAYS`, Rule 14 bright high-contrast equinox background test).

---

## Pasted Gate Outputs

```
> content-ops@0.1.0 review:script
> tsx scripts/review-script.ts --file /tmp/J2148-wt/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/01_Script/uranus_21_year_winter_script_master_v02.md

# uranus_21_year_winter_script_master_v02.md

**Decision:** PASS · **Score:** 95.2 / 100

| Dimension | Score |
|---|---:|
| hook | 10 |
| curiosity | 9.1 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 9.8 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1347 · Est. min: 9 · Chapters: 6

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.2/100 — proceed to VO after production checklist.

Pass threshold: 90

> content-ops@0.1.0 gate:episode
> tsx scripts/gate-episode.ts --project /tmp/J2148-wt/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters --script /tmp/J2148-wt/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/01_Script/uranus_21_year_winter_script_master_v02.md

# Episode gate — 033_Why-This-Planet-Has-21-Year-Winters

**Decision:** PASS — VO / Gemini Veo allowed

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /tmp/J2148-wt/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters |
| prebuild_vidiq | OK | Pre-build vidIQ audit present and looks signed off. |
| script_file | OK | Script: 01_Script/uranus_21_year_winter_script_master_v02.md |
| script_review | OK | Script reviewer PASS 95.2/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 43% (17 words): "If you've enjoyed the ride so far, subscribing is the best way to help Orbit keep going." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.2/100** · PASS
```
