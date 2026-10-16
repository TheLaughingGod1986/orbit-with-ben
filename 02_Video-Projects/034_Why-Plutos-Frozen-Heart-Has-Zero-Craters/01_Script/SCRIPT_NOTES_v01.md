# 034 Why Pluto's Frozen Heart Has Zero Craters — script v01 notes (J0378)

Drafted by Gemini (`gemini-argon`, stand-in worker) for J0378, 16 Oct 2026. **Draft only.** Revised from `pluto_frozen_heart_script_master_v00.md` (scaffolded in J0370 as #1 in `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-16_J0370.md`, 25/30, directly answering the closing hand-off at line 112 of `033` `uranus_21_year_winter_script_master_v01.md`), because `030`, `031` and `032` have locked scripts (`030` v02 locked in J0227/J0222; `031` v03 locked in J0340; `032` v01 locked in J0301), `033` Uranus `v01` is already drafted and parked for Chief's script review in J0363 (`56e8c332`), and `034` only had a `v00` draft at 1,523 spoken words (~10.3 min, over the 1,200–1,300 spoken-word lock) with no `status.json` entry on `STATUS.md`. The topic isn't locked (Chief locks it after the neighbour pass), and the script isn't locked (Chief's script review, then the Gemini `facts` pass and `CLAUDE_QUOTE_CHECK_v01.md` before any VO). No spend.

## Result

- `npm run review:script`: **PASS 95.8 / 100** (10/10 hook, 9.5/10 curiosity, 9.5/10 storytelling, 10/10 scientificAccuracy, 9.6/10 emotion, 10/10 escalation, 9.0/10 retentionPotential, 9.1/10 searchPotential, 9.5/10 visualOpportunities, 9.6/10 narrationFlow; 8/8 structure gates).
- Spoken words: **1,295 words** (1,328 reviewer words, ~8.9 min), 6 chapters — trimmed from `v00`'s 1,523 spoken words (~10.3 min) to sit cleanly inside the 1,200–1,300 spoken-word / 7–9 min lock.
- Subscribe beat at 42% of spoken words (11 words: *"New space mysteries every Sunday. Subscribe and they'll come to you."*).
- Markers: **DATA 7 · SCALE 7 (SCALE count ≥ DATA count) · WHO 3 · WHEN 6 · FACT 4 · NUMBER OBJECT 7**.
- First concrete answer (*"a frozen nitrogen glacier called Sputnik Planitia, about one thousand kilometres wide — shows zero craters"*) lands in the opening seconds; stakes and main question before 0:45; first chapter card (`[CHAPTER CARD: The Girl Who Named a World]`) held until after 0:30 (`OWB_2026-10-16.md` item 2); no agenda line (Lesson 7).

## Number object per chapter (per-chapter teaching gate)

| Chapter | Number object | People and dates |
|---|---|---|
| Hook | Sputnik Planitia crater comparison bar contrasting Pluto's scarred highlands (craters up to 260 km wide) with Sputnik Planitia (1,000 km wide, 0 craters) at 39 AU (−232 °C average; scale: larger than Texas and Oklahoma combined) | WHEN 13 July 2015, 14 July 2015 (timeline starts) |
| 1 The Girl Who Named a World | Diameter scale comparing Pluto (2,377 km, 1/5 of Earth, 2/3 of the Moon) with the United States and Earth + 5.9-billion-km (39 AU, 5.5-hour light-travel, 1/900 sunlight / 300× full Moon) distance bar | WHO Clyde Tombaugh (1906–1997), Venetia Burney (1919–2009); WHEN 18 February 1930, 14 March 1930 added to timeline; FACT Named by an 11-year-old |
| 2 The Moon That Never Sets | Pluto–Charon double-planet scale (Charon 1,214 km, ~1/2 of Pluto, orbiting at 19,640 km — 20× closer than Earth's Moon) + 153-hour (6.4-Earth-day) mutual tidal lock dial and 57° axial tilt | WHEN June 1978 added to timeline; FACT Charon never rises or sets |
| 3 Nine Years to the Kuiper Belt | Launch velocity bar at 58,536 km/h (+14,000 km/h Jupiter boost shortening trip by 3 years), 248-year orbit range (30 to 49.3 AU), and 6.25 GB data download gauge running 15 months at 1–2 kilobits/s across 4.5 light-hours | WHEN 1979–1999, 19 January 2006, 28 February 2007, 14 July 2015, 25 October 2016 added to timeline; FACT Closer than Neptune (1979–1999) |
| 4 The Glacier That Breathes | Sputnik Planitia width bar (1,000 km wide, 0 craters, largest known glacier in the solar system) + elevation gauge for Pluto's 2–3 km mountains, 600 km valleys, and 6% Earth gravity | — (midpoint twist *"Wrong."* opens chapter at ~60% runtime) |
| 5 Where Water Is Bedrock | Temperature and pressure cutaway gauge (−226 to −240 °C, ~13 microbars) comparing rock-hard water-ice mountains (2–3 km) with basal liquid nitrogen rising through cracks and a deep internal ocean | WHO Alan Stern (born 1957); WHEN August 2026 added to timeline; FACT Water ice acts like bedrock |
| 6 Beyond the Frozen Heart | Outbound Kuiper Belt distance bar from Pluto (39 AU, 200,000 km farewell shot) past Arrokoth (6.4 billion km, 35 km long, 3,500 km flyby) out to 60 AU on 1 October 2024 (2× Pluto's flyby distance, at 300 million miles/year) | WHEN 1 January 2019, 1 October 2024 completing timeline |

The timeline builds across the film, so it counts as one DATA moment. No two code graphics run back to back; real moving imagery sits between them in every chapter.

## What changed from v00

- Spoken word count tightened from **1,523 words (~10.3 min)** in `v00` to **1,295 spoken words (1,328 reviewer words, ~8.9 min)** in `v01`, bringing the script inside the 1,200–1,300 spoken-word / 7–9 min lock while keeping `review:script` at **95.8 / 100** (10/10 hook, 10/10 scientificAccuracy, 10/10 escalation, 8/8 structure gates).
- Removed the leftover template placeholder `01_Script/episode_script_draft_v01.md` so `gate:episode` and `review:script` point unambiguously to `pluto_frozen_heart_script_master_v01.md`.
- Reconciled `SCRIPT_NOTES_v01.md` and `production-status.md` with the exact `FACT:` (`Named by an 11-year-old`, `Charon never rises or sets`, `Closer than Neptune (1979–1999)`, `Water ice acts like bedrock`) and `WHEN:` markers in the script (`v00` notes had stale placeholder labels from an earlier outline).
- Registered `034` on `STATUS.md` (`status.json` `script: review`) so the pipeline board reflects `034` alongside `030`–`033`.

## Open items

1. **Chief:** topic lock (`J0370`: lock `034` Pluto or pick another candidate; decide Short-first waiver vs standalone Short `gmzaCfJF1gA`, airing 14 Nov 2026; neighbour pass ≥3 education/space videos at ≈1M+ views on Pluto / New Horizons / Sputnik Planitia) and script review of `pluto_frozen_heart_script_master_v01.md`.
2. **Gemini `facts` pass + `CLAUDE_QUOTE_CHECK_v01.md`:** all 15 rows in `01_Script/SOURCES.md` were pre-checked against live NASA (`science.nasa.gov/dwarf-planets/pluto/facts/`, `science.nasa.gov/mission/new-horizons/`, `science.nasa.gov/dwarf-planets/pluto/moons/charon/`, `science.nasa.gov/neptune/moons/triton/`, `science.nasa.gov/blogs/science-news/2026/08/05/nasas-new-horizons-finds-evidence-of-recent-liquid-on-plutos-surface/`), NSSDCA (`plutofact.html`) and LOC Authority pages on 16 Oct 2026 with verbatim quotes; formal `facts` pass and Claude quote check still run before VO lock.
3. **Archive portraits:** confirm public-domain/CC-licensed portrait files for Clyde Tombaugh (1906–1997), Venetia Burney (1919–2009) and Alan Stern (born 1957) before the shot list.
4. **Hand-off line:** Chapter 6 hands off to Neptune's moon Triton (*"Why Neptune's Largest Moon Orbits Backwards"*, #2 in `IDEAS_2026-10-16_J0370.md`, tied at 25/30); adjust if Chief picks a different `035` topic.
