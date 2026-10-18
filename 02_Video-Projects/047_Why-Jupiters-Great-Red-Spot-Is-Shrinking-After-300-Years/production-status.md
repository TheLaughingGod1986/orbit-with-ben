# Production status — 047 Why Is Jupiter's Great Red Spot Shrinking After 300 Years?

| Field | Value |
|-------|-------|
| Slug | `047_Why-Jupiters-Great-Red-Spot-Is-Shrinking-After-300-Years` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-18_J0575.md` (scored 17/30, #1 of 5; direct hand-off from `046`) |
| Topic lock | **Pending Chief decision** (`J0575` parked for Chief: lock 047 Why Jupiter's Great Red Spot Is Shrinking After 300 Years or pick #2 Ceres Salt Domes / #3 Simulation Physics / #4 Self-Replicating AI Probes / #5 Humans in 1,000 Years; confirm Short-first waiver) |
| Script draft | `01_Script/great_red_spot_shrinking_script_master_v00.md` (v00 drafted 18 Oct 2026 in J0575; 1,338 spoken words / 1,362 reviewer words, ~9.1 min; notes in `01_Script/SCRIPT_NOTES_v00.md`) |
| Script review | **PASS — 95.3 / 100** (1,338 spoken words / 1,362 reviewer words, ~9.1 min, 6 chapters, 8/8 structure gates, 0 warnings; parked for Chief topic/script review in `J0575`) |
| Sources | `01_Script/SOURCES.md` — 8 rows pre-checked with verbatim quotes (`NASA Science Jupiter Facts`, `NASA & ESA/Hubble Great Red Spot Shrinking Releases May 15, 2014 / heic1410`, `NASA JPL Juno 3D Atmosphere Release Oct 28, 2021 / Bolton et al. & Parisi et al. Science 374`, `NASA Hubble Wind Speed Acceleration Release Sep 27, 2021 / Wong et al. GRL 48`, `NASA Hubble 90-Day Stress-Ball Oscillation Release Oct 9, 2024 / Simon et al. PSJ 5`, `NASA Science Ceres Facts`, `LOC Name Authority Records n79003254 / nr96009532 / n81114174 / no2013066536 / n87803467`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| VO | Pending (wait for topic lock + Gemini `facts` + `CLAUDE_QUOTE_CHECK` + Chief script sign-off) |
| CG | Pending (NASA Juno Great Red Spot `PIA22946` / `PIA21775`, NASA/ESA Hubble 1995–2014 shrinkage `heic1410a`, 2009–2020 OPAL wind map, Dec 2023–Mar 2024 90-day oscillation sequence + code graphics + Omni Orbit) |
| Runtime target | 7–9 min (1,338 spoken words / 1,362 reviewer words, ~8.9–9.1 min est.) |
| Shorts | 3 episode Shorts on lock |

## Marker counts (`great_red_spot_shrinking_script_master_v00.md`)

- `DATA:` **7** (all ≥ 3 required; includes 3 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT:` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **5** (every named person in spoken narration at first mention: Galileo Galilei 1564–1642, Giovanni Domenico Cassini 1625–1712, Edwin Hubble 1889–1953, Amy Simon born 1971, Giuseppe Piazzi 1746–1826; verified in LOC Name Authority Records `n79003254`, `nr96009532`, `n81114174`, `no2013066536`, `n87803467`)
- `WHEN:` **7** (Hook: `1610, late 1600s, late 1800s, 1930s, 1979, 1995, 2009, May 15, 2014, October 28, 2021, October 9, 2024`; Ch 1: `4.6 billion years ago, 4 billion years ago, 1610, late 1600s, late 1800s, 43 minutes, 9.9 hours, 12 Earth years`; Ch 2: `1930s, 1979, 1980, 1990, 1995, 2009, 2012, April 21, 2014, May 15, 2014`; Ch 3: `2016, July 11, 2017, February 12, 2019, July 2019, October 28, 2021`; Ch 4: `1870s, 10 Earth hours, 2009 to 2020, 11 years, 2017, September 27, 2021`; Ch 5: `December 2023 to March 2024, 90 days, October 9, 2024`; Ch 6: `1801, 10 years, 300 years`)
- `FACT:` **4** (`Three Earths side-by-side`, `Five hundred eighty miles`, `Three hundred miles deep`, `Exceeds four hundred mph`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6)
- **Subscribe beat line:** `"If you want the next one, why Ceres has glowing salt domes, subscribing is how you'll see it."` (Line 1 from `templates/SUBSCRIBE_BEAT_LINES.md`, rotated from `043`–`046`; 18 words at 42%).
- **First 30 seconds rule (`OWB_2026-10-18.md`):** first `[CHAPTER CARD]` is placed after a 3-paragraph cold open (~194 spoken words, ~1:15), so no full-frame chapter card appears in `0:00–0:30`.

## Pasted `npm run review:script` output (v00, J0575, 18 Oct 2026)

```text
# great_red_spot_shrinking_script_master_v00.md

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

Words: 1362 · Est. min: 9.1 · Chapters: 6

## Cold open excerpt

> Why Is Jupiter's Great Red Spot Shrinking After 300 Years? Orbiting four hundred and eighty-four million miles from the Sun where sunlight takes forty-three minutes to arrive and a planet eleven times wider than Earth spins once every nine point nine hours, as you cross equatoria

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.3/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (v00, J0575, 18 Oct 2026)

```text
# Episode gate — 047_Why-Jupiters-Great-Red-Spot-Is-Shrinking-After-300-Years

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/047_Why-Jupiters-Great-Red-Spot-Is-Shrinking-After-300-Years |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/great_red_spot_shrinking_script_master_v00.md |
| script_review | OK | Script reviewer PASS 95.3/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 42% (18 words): "If you want the next one, why Ceres has glowing salt domes, subscribing is how you'll see it." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.3/100** · PASS
```
