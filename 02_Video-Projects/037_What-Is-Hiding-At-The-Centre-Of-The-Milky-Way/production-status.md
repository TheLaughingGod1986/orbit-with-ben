# Production status — 037 What Lies Hiding at the Centre of the Milky Way?

| Field | Value |
|-------|-------|
| Slug | `037_What-Is-Hiding-At-The-Centre-Of-The-Milky-Way` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-17_J0420.md` (scored 25/30, #1 of 5) |
| Topic lock | **Pending Chief decision** (`J0420` parked for Chief: lock 037 or pick #2 Left in Space / Voyager / #3 Planet Sounds / #4 Wrong Kind of Aliens; decide Short-first waiver based on Milky Way cluster #1 subscriber conversion and Astrum's 907k Milky Way Centre breakout) |
| Script draft | `01_Script/milky_way_centre_script_master_v00.md` (v00 drafted 17 Oct 2026 in J0420; 1,306 spoken words / 1,326 reviewer words, ~8.8 min; notes in `01_Script/SCRIPT_NOTES_v00.md`) |
| Script review | **PASS — 95.4 / 100** (1,306 spoken words / 1,326 reviewer words, ~8.8 min, 6 chapters, 8/8 structure gates, 0 warnings) |
| Sources | `01_Script/SOURCES.md` — 10 rows started and pre-checked with verbatim quotes (`NASA Sagittarius A*`, `NRAO Milky Way's Black Hole Was Birth Cry of Radio Astronomy`, `2020 Nobel Prize in Physics Press Release`, `ESO Release eso1825`, `ESO Release eso2208-eht-mw`, `NASA Fermi Bubbles / SVS 10688`, `NASA IXPE Sgr A* 200-Year Echo`, `NASA Voyager 1`, `LOC Name Authority Records n50022197 / n84228492 / n86813595 / n84176562 / n95070019 / n79022889`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| VO | Pending (wait for topic lock + Gemini `facts` + `CLAUDE_QUOTE_CHECK` + Chief script sign-off) |
| CG | Pending (NASA Chandra/Hubble `sgr_lg.jpg`, ESO EHT `eso2208-eht-mwa`, ESO VLT `eso1825a`, NASA Fermi `svs.gsfc.nasa.gov/10688`, NASA IXPE + code graphics + Omni Orbit) |
| Runtime target | 7–9 min (1,306 spoken words / 1,326 reviewer words, ~8.8 min est.) |
| Shorts | 3 episode Shorts on lock (building on our Milky Way / Andromeda cluster's #1 subscriber conversion: +5 subs in 28d) |

## Marker counts (`milky_way_centre_script_master_v00.md`)

- `DATA:` **7** (all ≥ 3 required; includes 2 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT:` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **6** (every named person in spoken narration at first mention: Harlow Shapley 1885–1972, Karl Jansky 1905–1950, Bruce Balick born 1943, Reinhard Genzel born 1952, Andrea Ghez born 1965, Albert Einstein 1879–1955; all verified in LOC Name Authority Records)
- `WHEN:` **7** (Hook: `1932 to 2022`; Ch 1: `1918, 1932, April 1933, February 1974`; Ch 2: `1990s, 2002, 2020`; Ch 3: `May 2018, 26 July 2018`; Ch 4: `April 2017, 2019, 12 May 2022`; Ch 5: `2012`; Ch 6: `September 1977, 2010, February and March 2022`)
- `FACT:` **4** (`Found as telephone static`, `S2 orbits every 16 years`, `Star hits 3% light speed`, `Ejects 99% of captured gas`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6)
- **Subscribe beat line:** `"If you've enjoyed the ride so far, subscribing is the best way to help Orbit keep going."` (Line 6 from `templates/SUBSCRIBE_BEAT_LINES.md`, not used in `032`–`036`; 17 words at 41%).
- **First 30 seconds rule (`OWB_2026-10-16.md`):** first `[CHAPTER CARD]` is placed after a 3-paragraph cold open (~148 spoken words, ~0:55), so no full-frame chapter card appears in `0:00–0:30`.

## Pasted `npm run review:script` output (v00, J0420, 17 Oct 2026)

```text
# milky_way_centre_script_master_v00.md

**Decision:** PASS · **Score:** 95.4 / 100

| Dimension | Score |
|---|---:|
| hook | 10 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 9.6 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1326 · Est. min: 8.8 · Chapters: 6

## Cold open excerpt

> What Lies Hiding at the Centre of the Milky Way? If you peered through the thick clouds of cosmic dust in the constellation Sagittarius — twenty-six thousand light-years from Earth in orbit around the heart of our Milky Way galaxy — what secret signal would you see whipping aroun

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.4/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (v00, J0420, 17 Oct 2026)

```text
# Episode gate — 037_What-Is-Hiding-At-The-Centre-Of-The-Milky-Way

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/037_What-Is-Hiding-At-The-Centre-Of-The-Milky-Way |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/milky_way_centre_script_master_v00.md |
| script_review | OK | Script reviewer PASS 95.4/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 41% (17 words): "If you've enjoyed the ride so far, subscribing is the best way to help Orbit keep going." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.4/100** · PASS
```
