# Production status — 042 What Happens When the Sun Becomes a Red Giant?

| Field | Value |
|-------|-------|
| Slug | `042_What-Happens-When-The-Sun-Becomes-A-Red-Giant` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-17_J0499.md` (scored 20/30, #1 of 5) |
| Topic lock | **Pending Chief decision** (`J0499` parked for Chief: lock 042 or pick #2 Boötes Void / #3 Terraform Mars / #4 Ganymede Bigger Than Mercury; confirm Short-first waiver) |
| Script draft | `01_Script/sun_red_giant_script_master_v01.md` (v01 drafted 18 Oct 2026 in J0507, revised from v00 in J0499; 1,277 spoken words / 1,299 reviewer words, ~8.7 min; notes in `01_Script/SCRIPT_NOTES_v01.md`) |
| Script review | **PASS — 95.6 / 100** (1,277 spoken words / 1,299 reviewer words, ~8.7 min, 6 chapters, 8/8 structure gates, 0 warnings; parked for Chief script review in `J0507`) |
| Sources | `01_Script/SOURCES.md` — 6 rows updated to v01 and pre-checked with verbatim quotes (`NASA Sun Facts`, `NASA Star Types`, `JPL News 3 May 2023 ZTF SLRN-2020`, `NASA Hubble Messier 57 Ring Nebula`, `NASA Webb NGC 3132 Southern Ring Nebula`, `NASA Exoplanets Life and Death Chapter 7`, `NASA Webb News 1 Jul 2026 WD 1856 b`, `NASA GSFC Blueshift Boötes Void`, `LOC Name Authority Records n86867046 / n87802277 / no2018042610 / n85220639 / no96049328`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| VO | Pending (wait for topic lock + Gemini `facts` + `CLAUDE_QUOTE_CHECK` + Chief script sign-off) |
| CG | Pending (NASA SDO/SOHO solar flare imagery, JPL NEOWISE & ZTF SLRN-2020 engulfment visuals, Hubble Messier 57 & Webb NGC 3132 planetary nebulae, Webb WD 1856 b transmission spectrum & transit visuals + code graphics + Omni Orbit) |
| Runtime target | 7–9 min (1,277 spoken words / 1,299 reviewer words, ~8.7 min est.) |
| Shorts | 3 episode Shorts on lock |

## Marker counts (`sun_red_giant_script_master_v01.md`)

- `DATA:` **7** (all ≥ 3 required; includes 3 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT:` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **5** (every named person in spoken narration at first mention: Richard Carrington 1826–1875, Edward Wright born 1947, Antoine Darquier de Pellepoix 1718–1802, Adriaan van Maanen 1884–1946, Walter Sydney Adams 1876–1956; verified in LOC Name Authority Records `n86867046`, `n87802277`, `no2018042610`, `n85220639`, `no96049328`)
- `WHEN:` **7** (Hook: `4.6 billion years ago, 3 May 2023, 1 July 2026, 5 billion years`; Ch 1: `4.6 billion years ago, 170,000 years, 1 September 1859, 5 billion years`; Ch 2: `2009, 2011, 2013, almost a year, 3 May 2023, more than 100,000 years`; Ch 3: `1779, thousands of years, more than 100,000 years`; Ch 4: `1917, 2015, 8 billion years, 10 billion years`; Ch 5: `2020, 34 hours, 3 to 5.5 billion years, 1 July 2026`; Ch 6: `230 million years, 5 billion years, more than 100,000 years, 8 to 10 billion years`)
- `FACT:` **4** (`Star caught eating planet`, `Teaspoon weighs pickup truck`, `Planet bigger than star`, `Outer giant planets survive`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6)
- **Subscribe beat line:** `"If you've enjoyed the ride so far, subscribing is the best way to help Orbit keep going."` (Line 6 from `templates/SUBSCRIBE_BEAT_LINES.md`, rotated from `038`–`041`; 17 words at 42%).
- **First 30 seconds rule (`OWB_2026-10-17.md`):** first `[CHAPTER CARD]` is placed after a 3-paragraph cold open (~148 spoken words, ~0:59), so no full-frame chapter card appears in `0:00–0:30`.

## Pasted `npm run review:script` output (v01, J0507, 18 Oct 2026)

```text
# sun_red_giant_script_master_v01.md

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

> What Happens When the Sun Becomes a Red Giant? High in orbit one hundred and fifty million kilometres from the photosphere of our four-point-six-billion-year-old Sun, as you follow the infrared data recorded when NASA's NEOWISE spacecraft caught an aging star swallowing a planet,

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.6/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (v01, J0507, 18 Oct 2026)

```text
# Episode gate — 042_What-Happens-When-The-Sun-Becomes-A-Red-Giant

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/042_What-Happens-When-The-Sun-Becomes-A-Red-Giant |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/sun_red_giant_script_master_v01.md |
| script_review | OK | Script reviewer PASS 95.6/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 42% (17 words): "If you've enjoyed the ride so far, subscribing is the best way to help Orbit keep going." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.6/100** · PASS
```
