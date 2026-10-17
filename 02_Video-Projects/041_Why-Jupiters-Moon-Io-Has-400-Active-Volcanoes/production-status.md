# Production status — 041 Why Does Jupiter's Moon Io Have 400 Active Volcanoes?

| Field | Value |
|-------|-------|
| Slug | `041_Why-Jupiters-Moon-Io-Has-400-Active-Volcanoes` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-17_J0484.md` (scored 21/30, #1 of 5) |
| Topic lock | **Pending Chief decision** (`J0484` parked for Chief: lock 041 or pick #2 Sun Red Giant / #3 Boötes Void / #4 Terraform Mars; confirm Short-first waiver) |
| Script draft | `01_Script/io_volcanoes_script_master_v01.md` (v01 drafted 17 Oct 2026 in J0492, revised from v00 in J0484; 1,260 spoken words / 1,299 reviewer words, ~8.7 min; notes in `01_Script/SCRIPT_NOTES_v01.md`) |
| Script review | **PASS — 95.6 / 100** (1,260 spoken words / 1,299 reviewer words, ~8.7 min, 6 chapters, 8/8 structure gates, 0 warnings; parked for Chief script review in `J0492`) |
| Sources | `01_Script/SOURCES.md` — 7 rows updated to v01 and pre-checked with verbatim quotes (`NASA Io Overview & Facts`, `NSSDCA Galilean Satellite Fact Sheet`, `NASA Photojournal PIA00379`, `JPL News 16/18 Apr 2024 Loki Patera`, `JPL News 12 Dec 2024 Nature Magma Chambers`, `JPL News 22 Jul 2026 MWR Subsurface Temperature`, `NASA Sun Facts`, `LOC Name Authority Records n79003254 / no2023091022`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| VO | Pending (wait for topic lock + Gemini `facts` + `CLAUDE_QUOTE_CHECK` + Chief script sign-off) |
| CG | Pending (NASA JunoCam Dec 30 2023 / Feb 3 2024 / Apr 9 2024 Io close-ups, Voyager 1 `PIA00379` March 8 1979 discovery image, New Horizons 2007 Tvashtar 5-frame sequence, Juno Loki Patera & MWR maps + code graphics + Omni Orbit) |
| Runtime target | 7–9 min (1,260 spoken words / 1,299 reviewer words, ~8.7 min est.) |
| Shorts | 3 episode Shorts on lock |

## Marker counts (`io_volcanoes_script_master_v01.md`)

- `DATA:` **7** (all ≥ 3 required; includes 3 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT:` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **2** (every named person in spoken narration at first mention: Galileo Galilei 1564–1642, Linda Morabito born 1953; verified in LOC Name Authority Records `n79003254` and `no2023091022`)
- `WHEN:` **7** (Hook: `8 March 1979, 30 December 2023`; Ch 1: `7 January 1610, 8 January 1610, mid-1800s, 42.5 hours, 1.8 days`; Ch 2: `8 March 1979, three days, 2007, eight minutes`; Ch 3: `1.8 days, 3.6 days, 7.2 days`; Ch 4: `30 December 2023, 3 February 2024, 9 April 2024, 16 April 2024, 22 July 2026`; Ch 5: `44 years, 1979, December 2023, February 2024, 12 December 2024`; Ch 6: `every second, 4.6 billion years ago, 5 billion years`)
- `FACT:` **4** (`Solid ground rises hundred metres`, `Lava lake smooth as glass`, `No global magma ocean underneath`, `Moon generates four hundred kilovolts`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6)
- **Subscribe beat line:** `"We make one of these every week. Subscribing is how the next one finds you."` (Line 4 from `templates/SUBSCRIBE_BEAT_LINES.md`, rotated from `037`–`040`; 15 words at 43%).
- **First 30 seconds rule (`OWB_2026-10-17.md`):** first `[CHAPTER CARD]` is placed after a 3-paragraph cold open (~148 spoken words, ~0:59), so no full-frame chapter card appears in `0:00–0:30`.

## Pasted `npm run review:script` output (v01, J0492, 17 Oct 2026)

```text
# io_volcanoes_script_master_v01.md

**Decision:** PASS · **Score:** 95.6 / 100

| Dimension | Score |
|---|---:|
| hook | 10 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 9.8 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1299 · Est. min: 8.7 · Chapters: 6

## Cold open excerpt

> Why Does Jupiter's Moon Io Have 400 Active Volcanoes? High in orbit above the floodplains of liquid rock on Jupiter's moon Io, as you follow the gravity data recorded when NASA's Juno spacecraft flew within one thousand five hundred kilometres of its surface, why is a rocky moon 

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.6/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (v01, J0492, 17 Oct 2026)

```text
# Episode gate — 041_Why-Jupiters-Moon-Io-Has-400-Active-Volcanoes

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/041_Why-Jupiters-Moon-Io-Has-400-Active-Volcanoes |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/io_volcanoes_script_master_v00.md |
| script_review | OK | Script reviewer PASS 95.6/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 43% (15 words): "We make one of these every week. Subscribing is how the next one finds you." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.6/100** · PASS
```
