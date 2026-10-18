# 047 Why Is Jupiter's Great Red Spot Shrinking After 300 Years? — script v01 notes (J0583)

Drafted by Gemini (`gemini`, stand-in worker) for J0583, 18 Oct 2026. **Draft only.** Revised from `great_red_spot_shrinking_script_master_v00.md` (scaffolded in J0575 as #1 in `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-18_J0575.md`, 17/30, directly answering the subscribe promise and closing hand-off at line 90 of `046` `enceladus_geysers_script_master_v01.md`), because `030`, `031` and `032` have locked scripts (`030` v02 locked in J0227/J0222; `031` v03 locked in J0340; `032` v01 locked in J0301), `033`–`046` already have `v01` drafted and parked for Chief's script review (`J0363`, `J0378`, `J0395`, `J0411`, `J0428`, `J0446`, `J0461`, `J0477`, `J0492`, `J0507`, `J0522`, `J0538`, `J0553`, `J0568`), and `047` only had a `v00` draft from the ideas pass (`J0575`). The topic isn't locked (Chief locks it after the neighbour pass), and the script isn't locked (Chief's script review, then the Gemini `facts` pass and `CLAUDE_QUOTE_CHECK` before any VO). No spend.

## Result

- `npm run review:script`: **PASS 95.3 / 100** (9.5/10 hook, 9.5/10 curiosity, 9.5/10 storytelling, 10/10 scientificAccuracy, 9.6/10 emotion, 10/10 escalation, 9.0/10 retentionPotential, 9.1/10 searchPotential, 9.5/10 visualOpportunities, 9.6/10 narrationFlow; 8/8 structure gates).
- Spoken words: **1,275 spoken words** (**1,298 reviewer words**, ~8.7 min), 6 chapters — inside the 1,200–1,300 word / 7–9 min lock on both counts.
- Subscribe beat at 42% of spoken words (18 words: *"If you want the next one, why Ceres has glowing salt domes, subscribing is how you'll see it."* — Line 1 from `templates/SUBSCRIBE_BEAT_LINES.md`, rotated from `043`–`046`).
- Markers: **DATA 7 · SCALE 7 (SCALE count ≥ DATA count) · WHO 5 · WHEN 7 · FACT 4 · NUMBER OBJECT 7**.
- First concrete answer (*"In the late eighteen hundreds, astronomers gauged this crimson storm at twenty-five thousand five hundred miles across — wide enough to fit three Earths side by side — yet NASA's Voyager spacecraft measured it at fourteen thousand five hundred miles in 1979, and Hubble confirmed it shrank to ten thousand two hundred and fifty miles by 2014 and ten thousand miles by 2021"*) lands in the opening seconds; stakes and main question before 0:45; first chapter card (`[CHAPTER CARD: Three Earths Wide to One]`) held until after 0:30 (`OWB_2026-10-18.md` item 2); no agenda line (Lesson 7).

## Number object per chapter (per-chapter teaching gate)

| Chapter | Number object | People and dates |
|---|---|---|
| Hook | 25,500-mile (3 Earths) vs 14,500-mile (1979) vs 10,000-mile (1 Earth) Great Red Spot shrinkage gauge | WHEN 43 minutes, 9.9 hours, 300 years, late 1800s, 1979, 2014, 2021, 90 days (timeline starts) |
| 1 Three Earths Wide to One | 43,440.7-mile (11× Earth) Jupiter radius comparison, 9.9-hour rotation clock, and 25,500-mile (41,000 km, 3× Earth) 1800s storm scale bar | WHO Galileo Galilei (1564–1642), Giovanni Domenico Cassini (1625–1712); WHEN 1610, late 1600s, 4.6 billion years ago, 9.9 hours, late 1800s added to timeline; FACT Fit three Earths |
| 2 Losing Five Hundred Eighty Miles Yearly | 25,500 → 14,500 → 13,020 → 11,130 → 10,250 mile contraction staircase and 580 miles/year loss meter | WHO Edwin Hubble (1889–1953), Amy Simon (born 1971); WHEN 1930s, 1979, 1980, 1990, 1995, 2009, 2012, April 21, 2014, May 15, 2014 added to timeline; FACT Five hundred eighty miles |
| 3 Three Hundred Miles Below the Clouds | 44-mile cloud deck vs 200–300 mile (350–500 km) Great Red Spot root depth and 2,000-mile (3,200 km) jet-stream depth gauge | WHEN 2016, July 11, 2017, July 2019, October 28, 2021 added to timeline (midpoint twist *"Wrong."* opens chapter); FACT Three hundred miles deep |
| 4 The Four-Hundred-MPH Racing Ring | >400 mph outer high-speed ring speedometer (+8% from 2009 to 2020 at <1.6 mph/year) and 105-mile (2× Rhode Island) resolution scale | WHEN 1870s, 11 years, 2009 to 2020, 10-hour day, 2017, September 27, 2021 added to timeline; FACT Up to eight percent |
| 5 Hubble's Ninety-Day Stress-Ball Wobble | 90-day elliptical stress-ball oscillation clock (Dec 2023 – Mar 2024) and 391–512 million mile Hubble observation range | WHEN December 2023 to March 2024, 90 days, October 9, 2024 added to timeline |
| 6 Why the Storm Will Not Vanish | Over-filled vs stabilized latitude-band wind channel diagram and 300-year survival timeline | WHO Giuseppe Piazzi (1746–1826); WHEN 300 years, 10 years, 1801 completing timeline |

The timeline builds across the film, so it counts as one DATA moment. No two code graphics run back to back; real moving imagery sits between them in every chapter.

## What changed from v00

- Aligned every spoken claim, mechanism, person card, date, and `FACT:` label 100% verbatim with the quoted sources in `01_Script/SOURCES.md` while trimming reviewer word count from `1,362` (`9.1 min`) down to `1,298` (`8.7 min`; `1,275` spoken words) so both counts sit cleanly inside the 1,200–1,300 word / 7–9 min lock, maintaining `npm run review:script` at **95.3 / 100** (`scientificAccuracy` 10/10, `escalation` 10/10, 8/8 structure gates):
  - Hook & Chapter 1: replaced `"twice the combined mass of all other solar system bodies outside the Sun"` and `"no solid ground"` with `"twice the combined material of all other solar system bodies"` and `"no solid surface"` (matching Rows 1 & 2 of `SOURCES.md`), removed un-spoken dates (`4 billion years ago`, `12 Earth years`) from Chapter 1's `WHEN:` marker so every `WHEN:` date is spoken in its chapter, and updated the Chapter 1 `FACT:` card to `Fit three Earths` (3 words, exact word-for-word substring of the spoken VO per the per-chapter teaching `WORDS` gate).
  - Chapters 2 & 3: removed the unquoted image-caption date (`February 12, 2019`) from Chapter 3's `WHEN:` marker so every `WHEN:` date is both spoken in the narration and backed by a verbatim quote in `SOURCES.md`, and matched `FACT: Five hundred eighty miles` (Ch 2) and `FACT: Three hundred miles deep` (Ch 3) word-for-word with the spoken VO lines.
  - Chapter 4: added the spoken `"Studied since the eighteen seventies"` hook (backed by Row 5 of `SOURCES.md`: `"Astronomers have pursued ongoing studies of the "king" of solar system storms since the 1870s"`) so the `1870s` `WHEN:` marker is spoken in narration, and updated the Chapter 4 `FACT:` card to `Up to eight percent` (4 words, exact word-for-word substring of the spoken VO `"increased by up to eight percent"`).
  - Chapter 6: matched `"salt deposits"` verbatim with Row 8 of `SOURCES.md` (`"Ceres' crust is rocky and dusty with large salt deposits"`, `science.nasa.gov/dwarf-planets/ceres/facts/`).

## Open items

1. **Chief:** topic lock (`J0575`: lock `047` *Why Is Jupiter's Great Red Spot Shrinking After 300 Years?*, or pick another candidate from `IDEAS_2026-10-18_J0575.md`; confirm Short-first waiver; dispatch neighbour pass ≥3 education/space videos at ≈1M+ views on Jupiter's Great Red Spot / Juno & Hubble Jupiter Storm discoveries) and script review of `great_red_spot_shrinking_script_master_v01.md` (`J0583`).
2. **Gemini `facts` pass + `CLAUDE_QUOTE_CHECK`:** all 8 rows in `01_Script/SOURCES.md` were pre-checked against live NASA, ESA/Hubble, JPL Juno, and LOC Authority pages on 18 Oct 2026 with verbatim quotes; formal `facts` pass and Claude quote check still run before VO lock.
3. **Archive portraits:** confirm public-domain/NASA/wikimedia portrait files for Galileo Galilei (1564–1642), Giovanni Domenico Cassini (1625–1712), Edwin Hubble (1889–1953), Amy Simon (born 1971), and Giuseppe Piazzi (1746–1826) before the shot list.
4. **Hand-off line:** Chapter 6 hands off to `048` *Why Does Dwarf Planet Ceres Have Glowing Salt Domes in the Asteroid Belt?* (#2 in `IDEAS_2026-10-18_J0575.md`, 17/30); adjust if Chief picks a different `048` topic.
