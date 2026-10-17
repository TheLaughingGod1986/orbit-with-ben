# Production status — 040 Why Are We Looking for the Wrong Kind of Aliens on Titan and Europa?

| Field | Value |
|-------|-------|
| Slug | `040_Wrong-Kind-Of-Aliens` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-17_J0469.md` (scored 22/30, #1 of 5) |
| Topic lock | **Pending Chief decision** (`J0469` parked for Chief: lock 040 or pick #2 Io Volcanoes / #3 Sun Red Giant / #5 Boötes Void; confirm Short-first waiver) |
| Script draft | `01_Script/wrong_kind_of_aliens_script_master_v01.md` (v01 drafted 17 Oct 2026 in J0477; 1,225 spoken words / 1,299 reviewer words, ~8.7 min; notes in `01_Script/SCRIPT_NOTES_v01.md`; revised from v00 drafted in J0469) |
| Script review | **PASS — 95.8 / 100** (1,225 spoken words / 1,299 reviewer words, ~8.7 min, 6 chapters, 8/8 structure gates, 0 warnings; parked for Chief script review in `J0477`) |
| Sources | `01_Script/SOURCES.md` — 7 rows started and pre-checked with verbatim quotes (`WHOI Discovery of Hydrothermal Vents`, `NASA Enceladus & Enceladus Hydrothermal Activity`, `NASA Europa Clipper & Europa`, `NASA Titan Facts & Photojournal PIA20016`, `ESA Titan Facts & Organics`, `Cornell Chronicle Kraken Mare`, `Mastrogiuseppe et al. 2014 & Lorenz 1993`, `NASA/JHUAPL Dragonfly`, `Caltech News & CaltechAUTHORS Kan et al. 2016`, `NobelPrize.org Frances Arnold`, `NASA Io`, `LOC Name Authority Records n83073944 / n79083314 / n79134100 / n88666692`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| VO | Pending (wait for topic lock + Gemini `facts` + `CLAUDE_QUOTE_CHECK` + Chief script sign-off) |
| CG | Pending (NASA `PIA25690` Europa JunoCam, `PIA17184`/`PIA19061` Enceladus plumes, `PIA17655` Titan northern seas, Europa Clipper KSC launch & High Bay 1 antenna, JHUAPL Dragonfly rotorcraft + code graphics + Omni Orbit) |
| Runtime target | 7–9 min (1,225 spoken words / 1,299 reviewer words, ~8.7 min est.) |
| Shorts | 3 episode Shorts on lock |

## Marker counts (`wrong_kind_of_aliens_script_master_v01.md`)

- `DATA:` **7** (all ≥ 3 required; includes 3 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT:` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **4** (every named person in spoken narration at first mention: Robert Ballard born 1942, William Herschel 1738–1822, Christiaan Huygens 1629–1695, Frances Arnold born 1956; all verified in LOC Name Authority Records and NobelPrize.org)
- `WHEN:` **7** (Hook: `February 1977, April 2030`; Ch 1: `February 1977`; Ch 2: `28 August 1789, 32.9 hours, 2005, 28 October 2015`; Ch 3: `14 August 2023, 14 October 2024, 2025, 3 December 2026, April 2030`; Ch 4: `25 March 1655`; Ch 5: `billions of years ago, July 2028, late 2034, 3.3 years, 1 to 2 Titan days, 16 Earth days, 8 Earth days`; Ch 6: `1993, 24 November 2016, 2018`)
- `FACT:` **4** (`Life thrives without sunlight`, `Plume organics twenty times denser`, `Methane seas dwarf Earth's oil`, `Enzyme bonds silicon fifteen times faster`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6)
- **Subscribe beat line:** `"New space mysteries every Sunday. Subscribe and they'll come to you."` (Line 1 from `templates/SUBSCRIBE_BEAT_LINES.md`, rotated from `039`'s Line 3; 11 words at 41%).
- **First 30 seconds rule (`OWB_2026-10-17.md`):** first `[CHAPTER CARD]` is placed after a 3-paragraph cold open (~148 spoken words, ~0:59), so no full-frame chapter card appears in `0:00–0:30`.

## Pasted `npm run review:script` output (v01, J0477, 17 Oct 2026)

```text
# wrong_kind_of_aliens_script_master_v01.md

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

Words: 1299 · Est. min: 8.7 · Chapters: 6

## Cold open excerpt

> Why Are We Looking for the Wrong Kind of Aliens on Titan and Europa? High in orbit above the icy surface of Jupiter's moon Europa, before NASA's Europa Clipper reaches Jupiter in April 2030, what secret signal or ocean of alien life might you miss if you only searched for organis

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (v01, J0477, 17 Oct 2026)

```text
# Episode gate — 040_Wrong-Kind-Of-Aliens

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /tmp/j0477-wt/02_Video-Projects/040_Wrong-Kind-Of-Aliens |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/wrong_kind_of_aliens_script_master_v01.md |
| script_review | OK | Script reviewer PASS 95.8/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 41% (11 words): "New space mysteries every Sunday. Subscribe and they'll come to you." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.8/100** · PASS
```
