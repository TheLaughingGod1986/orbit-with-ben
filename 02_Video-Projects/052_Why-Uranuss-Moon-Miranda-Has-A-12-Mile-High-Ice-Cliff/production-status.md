# Production status — 052 Why Uranus's Moon Miranda Has a 12-Mile-High Ice Cliff

| Field | Value |
|-------|-------|
| Slug | `052_Why-Uranuss-Moon-Miranda-Has-A-12-Mile-High-Ice-Cliff` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-19_J0651.md` (scored 30/30 studio rubric / 16/30 audit rubric, #1 of 5; direct hand-off from `051`) |
| Topic lock | **Pending Chief decision** (`J0651` parked for Chief: lock `052` *Why Uranus's Moon Miranda Has a 12-Mile-High Ice Cliff* or pick another candidate from `IDEAS_2026-10-19_J0651.md`; confirm Short-first waiver) |
| Script draft | `01_Script/miranda_ice_cliff_script_master_v01.md` (`v01` revised 19 Oct 2026 in `J0659` from `v00` in `J0651`; 1,231 spoken words / 1,284 reviewer words, ~8.6 min; notes in `01_Script/SCRIPT_NOTES_v01.md`) |
| Script review | **PASS — 95.8 / 100** (1,231 spoken words / 1,284 reviewer words, ~8.6 min, 6 chapters, 8/8 structure gates, 0 warnings; parked for Chief script review in `J0659`) |
| Sources | `01_Script/SOURCES.md` — 16 rows verified verbatim across 14 primary NASA/JPL/APOD/APL/LOC sources (`science.nasa.gov/uranus/moons/miranda/`, `science.nasa.gov/uranus/moons/facts/`, `science.nasa.gov/image-article/apod-2020-november-29-verona-rupes-tallest-known-cliff-in-the-solar-system/`, `PIA00044`, `PIA01490`, `PIA00039`, `PIA18185`, `PIA00042`, `PIA00141`, `PIA01354`, `PIA01361`, `jhuapl.edu/news/news-releases/241028-uranus-moon-miranda-with-ocean-beneath-surface-new-study`, `science.nasa.gov/people/gerard-kuiper/`, `LOC Name Authority n50046182 / n78095332`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| VO | Pending (wait for topic lock + Gemini `facts` + `CLAUDE_QUOTE_CHECK` + Chief script sign-off) |
| CG | Pending (real NASA/JPL Voyager 2 frames `PIA00044`, `PIA18185`, `PIA01490`, `PIA00042`, `PIA00141`, `PIA01354`, `PIA00039`, `PIA01361` + 7 custom animated code graphics + Omni Orbit) |
| Runtime target | 7–9 min (1,231 spoken words / 1,284 reviewer words, ~8.6 min est.) |
| Shorts | 3 episode Shorts on lock |

## Marker counts (`miranda_ice_cliff_script_master_v01.md`)

- `DATA:` **7** (all ≥ 3 required; includes 3 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **2** (every named person in spoken narration at first mention: `Gerard Kuiper (1905–1973) — Dutch-American planetary astronomer`; `William Shakespeare (1564–1616) — English playwright and poet`; verified in LOC Name Authority Records `n50046182`, `n78095332`)
- `WHEN:` **7** (Hook: `January 24, 1986, 10 minutes, 12 minutes`; Ch 1: `February 16, 1948, 38 years, 1986`; Ch 2: `January 24, 1986`; Ch 3: `January 1986`; Ch 4: `2024`; Ch 5: `October 16, 2024, October 28, 2024, 100 to 500 million years ago, 2004, 76 years, 1948`; Ch 6: `2023, 2024, January 24, 1986`)
- `FACT:` **4** (`Ten-minute rock fall`, `Reflects one-third of sunlight`, `Ocean filled half its radius`, `Half the moon unseen`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6)
- **Subscribe beat line:** `"Every Sunday Orbit goes somewhere new. Subscribe and you'll be there for how NASA's Parker Solar Probe touched the Sun."` (Line 2 from `templates/SUBSCRIBE_BEAT_LINES.md`, rotated from `047`–`051`; 20 words at 40%).
- **First 30 seconds rule (`OWB_2026-10-19.md`):** first `[CHAPTER CARD]` is placed after a 3-paragraph cold open (~151 spoken words, ~1:00), so no full-frame chapter card appears in `0:00–0:30`.

## Pasted `npm run review:script` output (`v01`, `J0659`, 19 Oct 2026)

```text
# miranda_ice_cliff_script_master_v01.md

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

Words: 1284 · Est. min: 8.6 · Chapters: 6

## Cold open excerpt

> Why Does Uranus's Moon Miranda Have a 12-Mile-High Ice Cliff? Look across the horizon of Miranda in orbit around Uranus in the images NASA's Voyager 2 captured on January 24, 1986, and you see the sunlit fault wall of Verona Rupes: a sheer cliff of water ice estimated at twenty k

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (`v01`, `J0659`, 19 Oct 2026)

```text
# Episode gate — 052_Why-Uranuss-Moon-Miranda-Has-A-12-Mile-High-Ice-Cliff

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/052_Why-Uranuss-Moon-Miranda-Has-A-12-Mile-High-Ice-Cliff |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/miranda_ice_cliff_script_master_v01.md |
| script_review | OK | Script reviewer PASS 95.8/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 40% (20 words): "Every Sunday Orbit goes somewhere new. Subscribe and you'll be there for how NASA's Parker Solar Probe touched the Sun." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.8/100** · PASS
```
