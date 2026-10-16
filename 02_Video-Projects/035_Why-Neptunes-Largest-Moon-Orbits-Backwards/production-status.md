# Production status — 035 Why Neptune's Largest Moon Orbits Backwards

| Field | Value |
|-------|-------|
| Slug | `035_Why-Neptunes-Largest-Moon-Orbits-Backwards` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-16_J0387.md` (scored 25/30, #1 of 5) |
| Topic lock | **Pending Chief decision** (`J0387` / `J0395` parked for Chief: lock 035 or pick #2 Mercury Ice / #3 Milky Way Centre / #4 Left in Space; decide Short-first waiver vs standalone Short `oyRcrFTYyDY`) |
| Script draft | `01_Script/triton_backwards_moon_script_master_v01.md` (v01 revised 16 Oct 2026 in J0395 from v00; 1,218 spoken words / 1,271 reviewer words, ~8.5 min; notes in `01_Script/SCRIPT_NOTES_v01.md`) |
| Script review | **PASS — 95.8 / 100** (1,218 spoken words / 1,271 reviewer words, ~8.5 min, 6 chapters, 8/8 structure gates, 0 warnings) |
| Sources | `01_Script/SOURCES.md` — 12 rows started and pre-checked with verbatim quotes (`NASA Triton`, `NASA Neptune Facts`, `NASA Neptune Moons`, `NASA Nereid`, `NASA Voyager 2`, `NASA Mercury Facts`, `NSSDCA Neptune & Satellite Fact Sheets`, `JPL Photojournal PIA00317 / PIA00059 / PIA01538 / PIA02215`, `LOC Name Authority Records n86815998 / no2018094574 / no2008116237 / n50046182`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| VO | Pending (wait for topic lock + Gemini `facts` + `CLAUDE_QUOTE_CHECK` + Chief script sign-off) |
| CG | Pending (NASA PIA00317 / PIA00059 / PIA01538 / PIA02215 + code graphics + Omni Orbit) |
| Runtime target | 7–9 min (1,218 spoken words / 1,271 reviewer words, ~8.5 min est.) |
| Shorts | Paired with standalone Short `oyRcrFTYyDY` (*The Wind on Neptune Is Supersonic*, scheduled 27 Oct 2026) + 3 episode Shorts on lock |

## Marker counts (`triton_backwards_moon_script_master_v01.md`)

- `DATA:` **7** (all ≥ 3 required; includes 1 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT:` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **4** (every named person in spoken narration at first mention: Urbain Le Verrier 1811–1877, Johann Gottfried Galle 1812–1910, William Lassell 1799–1880, Gerard Kuiper 1905–1973; all verified in LOC Name Authority Records)
- `WHEN:` **6** (Hook: `25 August 1989`; Ch 1: `23 September 1846, 10 October 1846, 2011`; Ch 2: `1949, millions of years ago`; Ch 3: `20 August 1977, 1979, 1981, 24 January 1986, 14 February 1986, 25 August 1989`; Ch 5: `since 1989`; Ch 6: `28 August 1989, November 1998, 10 December 2018`)
- `FACT:` **4** (`Financed by a brewery`, `Captured from Kuiper Belt`, `Winds 9× stronger than Earth's`, `Only 4 active volcanic worlds`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6; per-chapter table in `01_Script/SCRIPT_NOTES_v01.md`)
- **First 30 seconds rule (`OWB_2026-10-16.md`):** first `[CHAPTER CARD]` is placed after a 3-paragraph cold open (~145 spoken words, ~0:55), so no full-frame chapter card appears in `0:00–0:30`.

## Pasted `npm run review:script` output (v01, J0395, 16 Oct 2026)

```text
# triton_backwards_moon_script_master_v01.md

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

Words: 1271 · Est. min: 8.5 · Chapters: 6

## Cold open excerpt

> Why Neptune's Largest Moon Orbits Backwards If you stood on the nitrogen frost of Neptune's moon Triton — in backwards orbit — what would you see erupting above its horizon? On 25 August 1989, NASA's Voyager 2 spacecraft capped a seven-billion-kilometre journey to Neptune — thirt

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (v01, J0395, 16 Oct 2026)

```text
# Episode gate — 035_Why-Neptunes-Largest-Moon-Orbits-Backwards

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/035_Why-Neptunes-Largest-Moon-Orbits-Backwards |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/triton_backwards_moon_script_master_v01.md |
| script_review | OK | Script reviewer PASS 95.8/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 47% (11 words): "New space mysteries every Sunday. Subscribe and they'll come to you." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.8/100** · PASS
```
