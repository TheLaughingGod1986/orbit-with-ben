# Production status — 050 Why Saturn's Moon Iapetus Is Half Black and Half White

| Field | Value |
|-------|-------|
| Slug | `050_Why-Saturns-Moon-Iapetus-Is-Half-Black-And-Half-White` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-19_J0620.md` (scored 17/30, #1 of 5; direct hand-off from `049`) |
| Topic lock | **Pending Chief decision** (`J0620` parked for Chief: lock `050` *Why Saturn's Moon Iapetus Is Half Black and Half White* or pick #2 *Why NASA's DART Spacecraft Changed an Asteroid's Orbit by 33 Minutes* / #3 *Why Uranus's Moon Miranda Has a 12-Mile-High Ice Cliff* / #4 *Why NASA's Parker Solar Probe Flew Inside the Sun's Corona without Melting* / #5 *Are We Living Inside a Simulation? What Physics Actually Says*; confirm Short-first waiver) |
| Script draft | `01_Script/iapetus_half_black_white_script_master_v00.md` (`v00` drafted 19 Oct 2026 in `J0620`; 1,280 spoken words / 1,298 reviewer words, ~8.7 min; notes in `01_Script/SCRIPT_NOTES_v00.md`) |
| Script review | **PASS — 95.3 / 100** (1,280 spoken words / 1,298 reviewer words, ~8.7 min, 6 chapters, 8/8 structure gates, 0 warnings) |
| Sources | `01_Script/SOURCES.md` — 7 rows pre-checked with verbatim quotes (`NASA Science Iapetus & Phoebe`, `NASA/JPL/SSI Cassini Photojournal PIA11690, PIA11689, PIA06166, PIA06145, PIA08371–PIA08384, PIA08387, PIA11116`, `LOC Name Authority Records nr96009532 / n50036903`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| VO | Pending (wait for topic lock + Gemini `facts` + `CLAUDE_QUOTE_CHECK` + Chief script sign-off) |
| CG | Pending (NASA/JPL/SSI Cassini Iapetus & Phoebe mosaics `PIA11690`, `PIA08384`, `PIA06166`, `PIA08372`, `PIA08378`, `PIA08382`, `PIA08387` + code graphics + Omni Orbit) |
| Runtime target | 7–9 min (1,280 spoken words / 1,298 reviewer words, ~8.7 min est.) |
| Shorts | 3 episode Shorts on lock |

## Marker counts (`iapetus_half_black_white_script_master_v00.md`)

- `DATA:` **7** (all ≥ 3 required; includes 3 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT:` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **2** (every named person in spoken narration at first mention: Giovanni Domenico Cassini 1625–1712, John Herschel 1792–1871; verified in LOC Name Authority Records `nr96009532`, `n50036903`)
- `WHEN:` **7** (Hook: `December 31, 2004, September 10, 2007, 79 days`; Ch 1: `October 25, 1671, 1980, 1981`; Ch 2: `2004, October 15, 2004, 9 hours, 18 Earth months`; Ch 3: `September 10, 2007, 1,904 hours, 79 days`; Ch 4: `September 10, 2007`; Ch 5: `December 25, 2004, December 31, 2004, September 10, 2007`; Ch 6: `September 10, 2007, 79 days`)
- `FACT:` **4** (`Three quarters ice`, `Only six percent`, `Seventy-nine days`, `Three times the height`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6)
- **Subscribe beat line:** `"If this is your kind of question, subscribe. Next week is how NASA's DART spacecraft moved an asteroid."` (Line 3 from `templates/SUBSCRIBE_BEAT_LINES.md`, rotated from `046`–`049`; 18 words at 45%).
- **First 30 seconds rule (`OWB_2026-10-19.md`):** first `[CHAPTER CARD]` is placed after a 3-paragraph cold open (~150 spoken words, ~1:00), so no full-frame chapter card appears in `0:00–0:30`.

## Pasted `npm run review:script` output (`v00`, `J0620`, 19 Oct 2026)

```text
# iapetus_half_black_white_script_master_v00.md

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

Words: 1298 · Est. min: 8.7 · Chapters: 6

## Cold open excerpt

> Why Is Saturn's Moon Iapetus Half Black and Half White? Orbiting two million two hundred and thirteen thousand miles from Saturn where a walnut-shaped moon of water ice and rock shows a leading hemisphere as dark as coal and a trailing hemisphere almost as bright as snow, as you 

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.3/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (`v00`, `J0620`, 19 Oct 2026)

```text
# Episode gate — 050_Why-Saturns-Moon-Iapetus-Is-Half-Black-And-Half-White

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/050_Why-Saturns-Moon-Iapetus-Is-Half-Black-And-Half-White |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/iapetus_half_black_white_script_master_v00.md |
| script_review | OK | Script reviewer PASS 95.3/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 45% (18 words): "If this is your kind of question, subscribe. Next week is how NASA's DART spacecraft moved an asteroid." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.3/100** · PASS
```
