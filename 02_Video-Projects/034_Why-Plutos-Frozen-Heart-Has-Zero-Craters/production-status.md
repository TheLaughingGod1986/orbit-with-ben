# Production status — 034 Why Pluto's Frozen Heart Has Zero Craters

| Field | Value |
|-------|-------|
| Slug | `034_Why-Plutos-Frozen-Heart-Has-Zero-Craters` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-16_J0370.md` (scored 25/30, #1 of 5) |
| Topic lock | **Pending Chief decision** (`J0370` parked for Chief: lock 034 or pick #2 Triton / #3 Left in Space / #4 Mercury Ice; decide Short-first waiver vs standalone Short `gmzaCfJF1gA`) |
| Script draft | `01_Script/pluto_frozen_heart_script_master_v01.md` (v01 revised 16 Oct 2026 in J0378; 1,295 spoken words, 1,328 reviewer words, ~8.9 min) |
| Script review | **PASS — 95.8 / 100** (1,328 reviewer words, ~8.9 min, 6 chapters, 8/8 structure gates, 0 warnings) |
| Sources | `01_Script/SOURCES.md` — 15 rows started and pre-checked with verbatim quotes (`NASA Pluto Facts`, `NASA New Horizons`, `NASA Charon`, `NASA Triton`, `NASA Science News 5 Aug 2026`, `NSSDCA Pluto Fact Sheet`, `LOC Name Authority Records n80070368 / n2018039163 / n97019162`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| VO | Pending (wait for topic lock + Gemini `facts` + `CLAUDE_QUOTE_CHECK` + Chief script sign-off) |
| CG | Pending (NASA PIA19857 / PIA19952 / PIA19873 / PIA19968 / PIA20291 + code graphics + Omni Orbit) |
| Runtime target | 7–9 min (~1,295 spoken narration words, ~8.9 min est.) |
| Shorts | Paired with standalone Short `gmzaCfJF1gA` (*Pluto's Heart Has No Craters*, scheduled 14 Nov 2026) + 3 episode Shorts on lock |

## Marker counts (`pluto_frozen_heart_script_master_v01.md`)

- `DATA:` **7** (all ≥ 3 required; includes 1 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT:` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **3** (every named person in spoken narration at first mention: Clyde Tombaugh 1906–1997, Venetia Burney 1919–2009, Alan Stern born 1957; all verified in LOC Name Authority Records)
- `WHEN:` **6** (Hook: `13 July 2015, 14 July 2015`; Ch 1: `18 February 1930, 14 March 1930`; Ch 2: `June 1978`; Ch 3: `1979–1999, 19 January 2006, 28 February 2007, 14 July 2015, 25 October 2016`; Ch 5: `August 2026`; Ch 6: `1 January 2019, 1 October 2024`)
- `FACT:` **4** (`Named by an 11-year-old`, `Charon never rises or sets`, `Closer than Neptune (1979–1999)`, `Water ice acts like bedrock`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6)
- **First 30 seconds rule (`OWB_2026-10-16.md`):** first `[CHAPTER CARD]` is placed after a 3-paragraph cold open (~140 spoken words, ~0:55), so no full-frame chapter card appears in `0:00–0:30`.

## Pasted `npm run review:script` output (v01, J0378, 16 Oct 2026)

```text
# pluto_frozen_heart_script_master_v01.md

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

Words: 1328 · Est. min: 8.9 · Chapters: 6

## Cold open excerpt

> Why Pluto's Frozen Heart Has Zero Craters If you stood on the bright, heart-shaped glacier of Pluto — in distant orbit around our Sun — what would you see across its horizon? On 13 and 14 July 2015, NASA's New Horizons spacecraft flew within twelve thousand five hundred kilometre

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (v01, J0378, 16 Oct 2026)

```text
# Episode gate — 034_Why-Plutos-Frozen-Heart-Has-Zero-Craters

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/pluto_frozen_heart_script_master_v01.md |
| script_review | OK | Script reviewer PASS 95.8/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 43% (11 words): "New space mysteries every Sunday. Subscribe and they'll come to you." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.8/100** · PASS
```
