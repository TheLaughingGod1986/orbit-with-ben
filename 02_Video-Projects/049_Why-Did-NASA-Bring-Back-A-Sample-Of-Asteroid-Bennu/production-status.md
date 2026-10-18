# Production status — 049 Why Did NASA Bring Back a Sample of Asteroid Bennu?

| Field | Value |
|-------|-------|
| Slug | `049_Why-Did-NASA-Bring-Back-A-Sample-Of-Asteroid-Bennu` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-19_J0605.md` (scored 17/30, #1 of 5; direct hand-off from `048`) |
| Topic lock | **Pending Chief decision** (`J0605` parked for Chief: lock `049` *Why Did NASA Bring Back a Sample of Asteroid Bennu?* or pick #2 *Why Saturn's Moon Iapetus Is Half Black and Half White* / #3 *Why NASA's DART Spacecraft Changed an Asteroid's Orbit by 33 Minutes* / #4 *Why Uranus's Moon Miranda Has a 12-Mile-High Ice Cliff* / #5 *Why NASA's Parker Solar Probe Flew Inside the Sun's Corona without Melting*; confirm Short-first waiver) |
| Script draft | `01_Script/bennu_sample_return_script_master_v00.md` (`v00` drafted 19 Oct 2026 in `J0605`; 1,281 spoken words / 1,299 reviewer words, ~8.7 min; notes in `01_Script/SCRIPT_NOTES_v00.md`) |
| Script review | **PASS — 95.3 / 100** (1,281 spoken words / 1,299 reviewer words, ~8.7 min, 6 chapters, 8/8 structure gates, 0 warnings; parked for Chief topic lock & script review in `J0605`) |
| Sources | `01_Script/SOURCES.md` — 7 rows pre-checked with verbatim quotes (`NASA Science 101955 Bennu Facts & Exploration`, `NASA OSIRIS-REx Overview & In-Depth`, `NASA Surprising Phosphate Finding June 26, 2024 / Meteoritics & Planetary Science`, `NASA Asteroid Bennu Sample Reveals Mix of Life's Ingredients Jan 29, 2025 / Nature & Nature Astronomy`, `NASA Sugars, Gum, Stardust Found in Asteroid Bennu Samples Dec 2, 2025 / Nature Geoscience & Nature Astronomy`, `NASA Asteroid Bennu's Rugged Surface Baffled NASA Mar 17, 2026 / Nature Communications`, `LOC Name Authority Records n95003850 / n2005091257`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| VO | Pending (wait for topic lock + Gemini `facts` + `CLAUDE_QUOTE_CHECK` + Chief script sign-off) |
| CG | Pending (NASA OSIRIS-REx SamCam/PolyCam/MapCam/NavCam imagery, Utah SRC recovery photography, NASA Johnson cleanroom & XCT 3D fracture scans, SEM phosphate crystal & LBNL TEM space-gum imagery + code graphics + Omni Orbit) |
| Runtime target | 7–9 min (1,281 spoken words / 1,299 reviewer words, ~8.7 min est.) |
| Shorts | 3 episode Shorts on lock |

## Marker counts (`bennu_sample_return_script_master_v00.md`)

- `DATA:` **7** (all ≥ 3 required; includes 3 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT:` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **2** (every named person in spoken narration at first mention: Ivan Yarkovsky 1844–1902, Dante Lauretta born 1970; verified in LOC Name Authority Records `n95003850`, `n2005091257`)
- `WHEN:` **7** (Hook: `6 years, October 20, 2020, September 24, 2023`; Ch 1: `September 11, 1999, 2013, 10 million years, 4.5 billion years ago, 700 million to 2 billion years ago, 4.3 hours, 1.2 years, 6 years`; Ch 2: `2007, 2008, September 8, 2016, September 22, 2017, December 3, 2018, December 31, 2018, 1 year, December 12, 2019`; Ch 3: `October 20, 2020, March 2026`; Ch 4: `October 20, 2020, May 10, 2021, 7 minutes, 2.5 years, September 24, 2023, October 20, 2023, January 11, 2024, February 15, 2024`; Ch 5: `June 26, 2024, January 29, 2025, thousands of years, December 2, 2025`; Ch 6: `December 2, 2025`)
- `FACT:` **4** (`One-third of a mile`, `Three hundred occasions`, `Pit of plastic balls`, `Six times the amount`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6)
- **Subscribe beat line:** `"There's more to come after this, starting with Saturn's two-toned moon Iapetus. Subscribe so you don't miss it."` (Line 10 from `templates/SUBSCRIBE_BEAT_LINES.md`, rotated from `044`–`048`; 18 words at 41%).
- **First 30 seconds rule (`OWB_2026-10-18.md`):** first `[CHAPTER CARD]` is placed after a 3-paragraph cold open (~160 spoken words, ~1:04), so no full-frame chapter card appears in `0:00–0:30`.

## Pasted `npm run review:script` output (`v00`, `J0605`, 19 Oct 2026)

```text
# bennu_sample_return_script_master_v00.md

**Decision:** PASS · **Score:** 95.3 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 10 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1299 · Est. min: 8.7 · Chapters: 6

## Cold open excerpt

> Why Did NASA Bring Back a Sample of Asteroid Bennu? Orbiting one hundred and five million miles from the Sun where a diamond-shaped mountain of black rubble approaches within one hundred and eighty-six thousand miles of Earth every six years, as you cross near-Earth space with NA

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.3/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (`v00`, `J0605`, 19 Oct 2026)

```text
# Episode gate — 049_Why-Did-NASA-Bring-Back-A-Sample-Of-Asteroid-Bennu

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/049_Why-Did-NASA-Bring-Back-A-Sample-Of-Asteroid-Bennu |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/bennu_sample_return_script_master_v00.md |
| script_review | OK | Script reviewer PASS 95.3/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 41% (18 words): "There's more to come after this, starting with Saturn's two-toned moon Iapetus. Subscribe so you don't miss it." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.3/100** · PASS
```
