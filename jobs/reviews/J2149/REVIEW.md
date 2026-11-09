# J2149 — Rule-E Topic + Script Review: OWB 034 (*Why Pluto's Frozen Heart Has Zero Craters*)

- **Date:** 4 November 2026
- **Reviewer:** `gemini` (`gemini-argon`, specialist Rule-E reviewer)
- **Film:** `OWB:034` (`02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters`)
- **Authority:** `AGENTS.md` Rule E (*"Topic and script calls are reviewer calls, not Chief calls... Go queues the next stage at once."*). Supersedes earlier Chief topic jobs (`J1897`, `J1971`, `J1972`) after `OWB:034` entered active production (`jobs/WIP.json`, limit raised to 8 by Ben on 4 Nov 2026).
- **Verdict:** **GO** — topic (`034 topic`), script (`034 script`, `pluto_frozen_heart_script_master_v02.md`), and sources (`034 sources`) **LOCKED** (`done`); VO job queued (`kind: vo`, `--film 034 --stage vo`).

---

## Rubric Evaluation

### (1) Neighbour Check & No Near-Duplicate (`PASS`)

- **No near-duplicate on OWB or HOS:** Checked all OWB (`001`–`033`) and HOS (`001`–`010`) live, scheduled, and active films. Neither channel has a live, scheduled, or active long on Pluto (`033` Uranus directly hands off to `034` Pluto in the `Real Worlds` series; unlocked candidate `035` Triton waits in `WIP.json` `next`).
- **Qualifying 1M+ education/space neighbour pool (12 videos verified via `yt-dlp` on 4 Nov 2026, logged in `11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md` and `PRE_BUILD_VIDIQ_AUDIT.md`):**
  1. `EJxwWpaGoJs` — *The Year of Pluto - New Horizons Documentary Brings Humanity Closer to the Edge of the Solar System* (NASA) — **21,197,158 views** (`2015-06-12`, `58:34`)
  2. `D5XPuS-Y0fg` — *The Final Images We Will Ever See of Pluto and Arrokoth* (Astrum) — **18,428,563 views** (`2022-06-08`, `30:57`)
  3. `6l4kr36TzQ4` — *What did NASA's New Horizons discover around Pluto?* (Astrum) — **9,252,145 views** (`2018-01-28`, `13:44`)
  4. `1ozN_0gYTBk` — *What NASA Found on Pluto* (The Space Race) — **6,230,877 views** (`2025-08-23`, `15:29`)
  5. `epZ5_DVQzFE` — *The Facts Nearly Everyone Gets Wrong About Pluto* (Astrum) — **3,357,321 views** (`2023-12-17`, `17:27`)
  6. `g1fPhhTT2Oo` — *New Horizons Flyover of Pluto* (NASA Video) — **2,763,964 views** (`2017-07-14`, `2:00`)
  7. `FTx2O7Zm4Jc` — *We Finally Found Out Why Pluto's Moon Charon Is Broken* (Astrum) — **2,629,580 views** (`2025-11-19`, `24:21`)
  8. `jIxQXGTl_mo` — *Seeking Pluto’s Frigid Heart | 360 VR Video | The New York Times* (The New York Times) — **2,154,132 views** (`2016-05-17`, `7:43`)
  9. `yZsStj2yXXA` — *Absolutely Everything We Know About Pluto* (Astrum Extra) — **2,048,872 views** (`2025-03-21`, `58:36`)
  10. `QqSl7TVoCUQ` — *Bizarre Worlds NASA Discovered Beyond Pluto in the Kuiper Belt* (Astrum) — **1,435,773 views** (`2025-03-31`, `18:17`)
  11. `vPsQN7mp700` — *Pluto and Beyond (2019) | Full Documentary | NOVA* (PBS America) — **1,216,449 views** (`2023-11-25`, `52:51`)
  12. `MHsDI83dZ_s` — *The Discovery That Demoted Pluto* (Astrum) — **1,030,825 views** (`2025-12-19`, `20:25`)

### (2) Audience Evidence (`PASS`)

- **Comparable reference-channel views (`AGENTS.md` Rule E rubric item 2 & `LEARNINGS.md` row 18):**
  - Astrum's *The Final Images We Will Ever See of Pluto and Arrokoth* (`D5XPuS-Y0fg`) sits at **18,428,563 views** and is explicitly cited in `LEARNINGS.md` row 18 as the reference-channel benchmark for real-imagery titles;
  - NASA's *The Year of Pluto* (`EJxwWpaGoJs`) sits at **21,197,158 views**;
  - Astrum's *What did NASA's New Horizons discover around Pluto?* (`6l4kr36TzQ4`) sits at **9,252,145 views**;
  - The Space Race's recent *What NASA Found on Pluto* (`1ozN_0gYTBk`, uploaded 23 Aug 2025) sits at **6,230,877 views**;
  - NYT's *Seeking Pluto's Frigid Heart* (`jIxQXGTl_mo`) sits at **2,154,132 views**.
- **Our own Short on the exact topic (`gmzaCfJF1gA`, *Why Does Pluto's Giant Ice Heart Have Zero Craters?*):** Uploaded Private (`23 s`, `publishAt: 2026-11-14T11:30:00Z`, `0 views` pre-release in `05_Analytics/owb/snapshots/2026-11-04.json`), ready to point at Long `034` under `LEARNINGS` rule 17 when public.

### (3) Script Master Polish (`v02`) & Every Number Sourced in `SOURCES.md` (`PASS`)

- **Small script points fixed in `01_Script/pluto_frozen_heart_script_master_v02.md` (with `v00.md` and `v01.md` preserved byte-identical):**
  1. **Opening (`LEARNINGS` rule 10 & `J1897`):** Replaced the hypothetical opener and three-question agenda with an immediate subject + horizon question, concrete observation (`a frozen nitrogen glacier about 1,000 km wide — larger than Texas and Oklahoma combined — with zero craters`), **causal answer before 0:30** (`Sputnik Planitia is an active glacier where city-sized cells of solid nitrogen circulate up and down`), and one central question before 0:45.
  2. **Spoken word count:** Trimmed to **1,291 spoken words** (`v02`, 1,324 reviewer words, ~8.8 min), strictly inside the `1,200–1,300` spoken-word target.
  3. **Subscribe beat:** Updated to Line 9 of `templates/SUBSCRIBE_BEAT_LINES.md` (*"If you'd like more questions like this one, subscribing really helps a small channel."*, 14 words at 42% of spoken words), avoiding lines 4, 6, and 8 used in `030`–`033`.
  4. **Every spoken & visual number verified in `01_Script/SOURCES.md` and `01_Script/CLAUDE_QUOTE_CHECK_v01.md` (15/15 rows `VERIFIED` against live NASA Science, NSSDCA, and LOC pages on 4 Nov 2026):**
     - Hook: 13 & 14 July 2015 New Horizons flyby (only spacecraft to visit Pluto; within 12,500 km), 39× Earth's distance, −232 °C average, craters up to 260 km vs Sputnik Planitia (~1,000 km wide, larger than Texas & Oklahoma combined, 0 craters, city-sized convection cells) (rows 1, 11).
     - Ch 1: 18 February 1930, Clyde Tombaugh (1906–1997), 76 years as 9th planet (1930–2006), 14 March 1930, 11-year-old Venetia Burney (1919–2009), 2,377 km equatorial diameter (1/5 of Earth, 2/3 of Earth's Moon, half US width), 5.9 billion km (39 AU), 5.5 hours sunlight travel, 1/900 Earth noon brightness (300× full Moon) (rows 2, 3, 4).
     - Ch 2: June 1978, US Naval Observatory in Flagstaff (6 miles from Lowell Observatory), 6.39-day cycle, 5 moons (Charon, Nix, Hydra, Kerberos, Styx; 4 smaller <160 km wide), Charon 1,214 km (~1/2 Pluto), 19,640 km orbit (20× closer than Earth's Moon), ~153-hour (6.4-Earth-day) rotation and orbit, 57° tilt, mutual tidal locking (rows 5, 6, 7).
     - Ch 3: 19 January 2006 launch, 478 kg mass, 58,536 km/h highest launch velocity, 2006 IAU reclassification, Kuiper Belt 30–50 AU formed ~4.5 billion years ago, 248-year orbit (30–49.3 AU, closer than Neptune 1979–1999), 28 February 2007 Jupiter gravity assist (+14,000 km/h, saving 3 years), 11:49 UT on 14 July 2015 (>9 years in flight), 6.25 GB downloaded over >15 months (until 25 October 2016) across 4.5 light-hours at 1–2 kilobits/s (rows 8, 9, 10).
     - Ch 4: Sputnik Planitia named for Sputnik 1, ~1,000 km wide, 0 craters vs 260 km craters, city-sized convection cells, mountains 2–3 km high, valleys up to 600 km long, ~6% Earth gravity, −226 to −240 °C (rows 11, 12).
     - Ch 5: −226 to −240 °C (>200 °C below water's 0 °C freezing point), 2–3 km water-ice mountains, 5 August 2026 Alan Stern (born 1957) analysis providing evidence of liquid nitrogen rising through northern Sputnik Planitia cracks from basal melting under ~13-microbar atmosphere, hints of internal water-ice ocean deep inside today (rows 12, 13).
     - Ch 6: 200,000 km farewell crescent portrait on 14 July 2015, 1 January 2019 Arrokoth flyby at 6.4 billion km from Earth (within 3,500 km of 35 km target), 1 October 2024 passing 60 AU (2× Pluto's 2015 flyby distance) at 300 million miles/year, Triton retrograde orbit and −235 °C nitrogen-crust geysers (rows 14, 15).
  5. **Teach on screen & Polish pass markers:** `DATA: 7`, `SCALE: 7`, `WHO: 3` (all named people in VO have sourced WHO cards), `WHEN: 6` (all spoken dates/eras mapped to the timeline), `FACT: 4` (all ≤ 4 words: `Named at age eleven`, `Charon never sets`, `Closer than Neptune`, `Water-ice bedrock`), Orbit display text `WATER ICE BEDROCK` (3 words), `NUMBER OBJECT: 7` (hook + chapters 1–6), and 15–20 s moving end-screen picture at the close.

### (4) New Reference-Channel Rules (`LEARNINGS` 18, 19, 20) (`PASS`)

Recorded in `11_Upload-Package/metadata_DRAFT_v01.json`, `description_DRAFT_v01.txt`, and `PRE_BUILD_VIDIQ_AUDIT.md`:
1. **Series (`LEARNINGS` rule 20):** **`Real Worlds`**.
   - End screen: `Real Worlds` series playlist + next/latest public film in the series (`033` Uranus, or `035` Triton once public).
   - Description line: `Next in the series: Why Neptune's Largest Moon Orbits Backwards` (and spoken hand-off in Ch 6).
2. **Real-imagery title variants (`LEARNINGS` rule 18, ≤ 50 chars per rule 15):**
   - Scenario/stakes title (Rule 15): `Why Pluto's Frozen Heart Has Zero Craters` (**41 chars**)
   - Real-imagery variant 1 (Rule 18): `What New Horizons Saw Inside Pluto's Frozen Heart` (**49 chars** — sells the real July 2015 New Horizons close-up imagery of Sputnik Planitia)
   - Real-imagery variant 2 (Rule 18): `The Only Spacecraft Photos Ever Taken of Pluto` (**46 chars** — `"Only"` is proved verbatim by `SOURCES.md` row 1 from `science.nasa.gov/dwarf-planets/pluto/facts/`: *"The only spacecraft to explore Pluto up close was NASA's New Horizons. It flew by the dwarf planet and its moons in 2015."*).
3. **Real spacecraft frame for the Rule-19 thumbnail (Concept A):**
   - **NASA/JHUAPL/SwRI New Horizons real frame `PIA20291` (or `PIA19952`, July 2015 MVIC/LORRI enhanced natural-colour global portrait of Pluto and its bright heart Sputnik Planitia)** filling the frame in a single clean spacecraft exposure, graded to mean saturation ≥ 100 (target 120) and near-black ≤ 30%, no composite, with a 2-word top-band hook `ZERO CRATERS` (yellow word `ZERO`). Paired in Test & Compare with Concept B (`WATER IS ROCK`, 3 km water-ice mountains from New Horizons `PIA19948` / `PIA20027`) and Concept C (`STILL ALIVE`, Rule-14 bright electric-blue atmospheric haze crescent test from New Horizons `PIA19968`).

---

## Pasted Gate Outputs

```
> content-ops@0.1.0 review:script
> tsx scripts/review-script.ts --file /tmp/J2149-wt/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/01_Script/pluto_frozen_heart_script_master_v02.md

# pluto_frozen_heart_script_master_v02.md

**Decision:** PASS · **Score:** 95.8 / 100

| Dimension | Score |
|---|---:|
| hook | 10 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 10 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1324 · Est. min: 8.8 · Chapters: 6

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.8/100 — proceed to VO after production checklist.

Pass threshold: 90

> content-ops@0.1.0 gate:episode
> tsx scripts/gate-episode.ts --project /tmp/J2149-wt/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters --script /tmp/J2149-wt/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/01_Script/pluto_frozen_heart_script_master_v02.md

# Episode gate — 034_Why-Plutos-Frozen-Heart-Has-Zero-Craters

**Decision:** PASS — VO / Gemini Veo allowed

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /tmp/J2149-wt/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters |
| prebuild_vidiq | OK | Pre-build vidIQ audit present and looks signed off. |
| script_file | OK | Script: 01_Script/pluto_frozen_heart_script_master_v02.md |
| script_review | OK | Script reviewer PASS 95.8/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 42% (14 words): "If you'd like more questions like this one, subscribing really helps a small channel." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.8/100** · PASS
```
