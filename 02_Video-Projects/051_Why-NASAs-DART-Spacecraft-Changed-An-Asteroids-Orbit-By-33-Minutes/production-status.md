# Production status — 051 Why NASA's DART Spacecraft Changed an Asteroid's Orbit by 33 Minutes

| Field | Value |
|-------|-------|
| Slug | `051_Why-NASAs-DART-Spacecraft-Changed-An-Asteroids-Orbit-By-33-Minutes` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-19_J0636.md` (scored 17/30, #1 of 5; direct hand-off from `050`) |
| Topic lock | **Pending Chief decision** (`J0636` parked for Chief: lock `051` *Why NASA's DART Spacecraft Changed an Asteroid's Orbit by 33 Minutes* or pick #2 *Why Uranus's Moon Miranda Has a 12-Mile-High Ice Cliff* / #3 *Why NASA's Parker Solar Probe Flew Inside the Sun's Corona without Melting* / #4 *Are We Living Inside a Simulation? What Physics Actually Says* / #5 *What Will Humans Become in 1,000 Years?*; confirm Short-first waiver) |
| Script draft | `01_Script/dart_asteroid_orbit_script_master_v00.md` (`v00` drafted 19 Oct 2026 in `J0636`; 1,235 spoken words / 1,290 reviewer words, ~8.6 min; notes in `01_Script/SCRIPT_NOTES_v00.md`) |
| Script review | **PASS — 95.6 / 100** (1,235 spoken words / 1,290 reviewer words, ~8.6 min, 6 chapters, 8/8 structure gates, 0 warnings) |
| Sources | `01_Script/SOURCES.md` — 7 rows pre-checked with verbatim quotes across 9 primary NASA/JPL/ASI/Hubble/LOC sources (`NASA 2022 Oct 11 Orbit Change Release`, `NASA Science DART Mission Overview`, `NASA/JPL Photojournal PIA25558, PIA25563, PIA25566, PIA25567, PIA26273`, `NASA/JPL 2023 Dec 13 Ejecta Momentum Release`, `NASA/Hubble 2023 Jul 20 STScI-01H445334R672T2B7GPF2M015M`, `NASA/JPL 2024 Mar 19 Shape Change Release`, `LOC Name Authority Records no2016110011 / n00006943`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| VO | Pending (wait for topic lock + Gemini `facts` + `CLAUDE_QUOTE_CHECK` + Chief script sign-off) |
| CG | Pending (NASA/JPL/APL DRACO frames `PIA25558`, ASI LICIACube `PIA25563`, Webb/Hubble `PIA25566`, Hubble tail `PIA25567`, Hubble 37-boulder swarm, JPL shape model `PIA26273` + code graphics + Omni Orbit) |
| Runtime target | 7–9 min (1,235 spoken words / 1,290 reviewer words, ~8.6 min est.) |
| Shorts | 3 episode Shorts on lock |

## Marker counts (`dart_asteroid_orbit_script_master_v00.md`)

- `DATA:` **7** (all ≥ 3 required; includes 4 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT:` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **2** (every named person in spoken narration at first mention: Steve Chesley born 1965, David Jewitt born 1958; verified in LOC Name Authority Records `no2016110011`, `n00006943`)
- `WHEN:` **7** (Hook: `September 26, 2022, October 11, 2022, 11 hours 55 minutes, 11 hours 22 minutes`; Ch 1: `November 24, 2021, September 26, 2022, 11 hours 55 minutes`; Ch 2: `September 11, 2022, September 26, 2022, 167 seconds`; Ch 3: `September 26, 2022, December 2023`; Ch 4: `September 26, 2022, October 8, 2022, December 19, 2022, July 20, 2023`; Ch 5: `September 26, 2022, October 11, 2022, 32 minutes, 33 minutes`; Ch 6: `November 24, 2021, September 26, 2022, October 11, 2022, March 19, 2024`)
- `FACT:` **4** (`Fifteen days before impact`, `Thirty thousand times greater`, `Oblong watermelon`, `Thirty-seven free-flung boulders`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6)
- **Subscribe beat line:** `"Stay for the rest of this one, and subscribe for Uranus's moon Miranda and its giant ice cliff."` (Line 7 from `templates/SUBSCRIBE_BEAT_LINES.md`, rotated from `046`–`050`; 18 words at 41%).
- **First 30 seconds rule (`OWB_2026-10-19.md`):** first `[CHAPTER CARD]` is placed after a 3-paragraph cold open (~142 spoken words, ~0:57), so no full-frame chapter card appears in `0:00–0:30`.

## Pasted `npm run review:script` output (`v00`, `J0636`, 19 Oct 2026)

```text
# dart_asteroid_orbit_script_master_v00.md

**Decision:** PASS · **Score:** 95.6 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 10 |
| retentionPotential | 9 |
| searchPotential | 9.4 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1290 · Est. min: 8.6 · Chapters: 6

## Cold open excerpt

> Why Did NASA's DART Spacecraft Change an Asteroid's Orbit by Thirty-Three Minutes? Seven million miles from Earth on September twenty-sixth, two thousand and twenty-two, NASA deliberately steered a five-hundred-and-seventy-kilogram spacecraft head-on into the asteroid moon Dimorp

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.6/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (`v00`, `J0636`, 19 Oct 2026)

```text
# Episode gate — 051_Why-NASAs-DART-Spacecraft-Changed-An-Asteroids-Orbit-By-33-Minutes

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/051_Why-NASAs-DART-Spacecraft-Changed-An-Asteroids-Orbit-By-33-Minutes |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/dart_asteroid_orbit_script_master_v00.md |
| script_review | OK | Script reviewer PASS 95.6/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 41% (18 words): "Stay for the rest of this one, and subscribe for Uranus's moon Miranda and its giant ice cliff." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.6/100** · PASS
```
