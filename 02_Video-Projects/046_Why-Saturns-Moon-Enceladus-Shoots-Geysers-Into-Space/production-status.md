# Production status — 046 Why Does Saturn's Moon Enceladus Shoot Geysers Into Space?

| Field | Value |
|-------|-------|
| Slug | `046_Why-Saturns-Moon-Enceladus-Shoots-Geysers-Into-Space` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-18_J0560.md` (scored 18/30, #1 of 5; backlog id `005`) |
| Topic lock | **Pending Chief decision** (`J0560` parked for Chief: lock 046 Why Saturn's Moon Enceladus Shoots Geysers Into Space or pick #2 Great Red Spot Shrinking / #3 Ceres Salt Domes / #4 Simulation Physics / #5 Self-Replicating AI Probes; confirm Short-first waiver) |
| Script draft | `01_Script/enceladus_geysers_script_master_v00.md` (v00 drafted 18 Oct 2026 in J0560; 1,259 spoken words / 1,407 reviewer words, ~9.4 min; notes in `01_Script/SCRIPT_NOTES_v00.md`) |
| Script review | **PASS — 94.9 / 100** (1,259 spoken words / 1,407 reviewer words, ~9.4 min, 6 chapters, 8/8 structure gates, 0 warnings; parked for Chief topic lock + script review in `J0560`) |
| Sources | `01_Script/SOURCES.md` — 9 rows pre-checked with verbatim quotes (`NASA Science Enceladus & Dione`, `NSSDCA Saturnian Satellite Fact Sheet`, `NASA Cassini Global Ocean Release Sep 2015`, `NASA Enceladus Hydrothermal Activity & Ocean Worlds Release Apr 2017`, `Postberg et al. June 14, 2023 Nature 618, 489–493`, `NASA Webb Enceladus 6,000-Mile Plume Release May 2023`, `NASA Cassini Overview & Jupiter Facts`, `LOC Name Authority Records n79083314 / n50036903 / nr96009532 / n87820555 / no2011098659`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| VO | Pending (wait for topic lock + Gemini `facts` + `CLAUDE_QUOTE_CHECK` + Chief script sign-off) |
| CG | Pending (NASA Cassini Enceladus backlit geysers `PIA17184` / `PIA11133`, interior global ocean `PIA20013`, hydrothermal seafloor cutaway `PIA21442`, JWST NIRSpec 6,000-mile plume + code graphics + Omni Orbit) |
| Runtime target | 7–9 min (1,259 spoken words / 1,407 reviewer words, ~8.4–9.4 min est.) |
| Shorts | 3 episode Shorts on lock |

## Marker counts (`enceladus_geysers_script_master_v00.md`)

- `DATA:` **7** (all ≥ 3 required; includes 3 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT:` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **5** (every named person with a card at first mention: William Herschel 1738–1822, John Herschel 1792–1871, Giovanni Domenico Cassini 1625–1712, Peter Thomas born 1946, Carolyn Porco born 1953; verified in LOC Name Authority Records `n79083314`, `n50036903`, `nr96009532`, `n87820555`, `no2011098659`)
- `WHEN:` **7** (Hook: `August 28, 1789, 1847, 1980s, 2005, September 2015, October 28, 2015, May 2023, June 2023`; Ch 1: `August 28, 1789, 1847, 1980s, October 9, 2008`; Ch 2: `March 21, 1684, 32.9 hours, 2.7 days, 2005, November 30, 2010`; Ch 3: `mid-2004, 7 years, 2014, September 2015`; Ch 4: `March 2015, October 28, 2015, April 2017`; Ch 5: `June 14, 2023, 1,000 hours`; Ch 6: `2017, May 17, 2023, 33 hours, 2 weeks, 300 years`)
- `FACT:` **4** (`Most reflective solar body`, `Eight hundred miles hourly`, `Ninety-eight percent water`, `Hundredfold ocean phosphorus`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6)
- **Subscribe beat line:** `"Every Sunday Orbit goes somewhere new. Subscribe and you'll be there for why Jupiter's Great Red Spot is shrinking."` (Line 2 from `templates/SUBSCRIBE_BEAT_LINES.md`, rotated from `041`–`045`; 19 words at 43%).
- **First 30 seconds rule (`OWB_2026-10-18.md`):** first `[CHAPTER CARD]` is placed after a 3-paragraph cold open (~156 spoken words, ~1:00), so no full-frame chapter card appears in `0:00–0:30`.

## Pasted `npm run review:script` output (v00, J0560, 18 Oct 2026)

```text
# enceladus_geysers_script_master_v00.md

**Decision:** PASS · **Score:** 94.9 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 9.6 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1407 · Est. min: 9.4 · Chapters: 6

## Cold open excerpt

> Why Does Saturn's Moon Enceladus Shoot Geysers Into Space? Orbiting one hundred and forty-eight thousand miles from Saturn within the densest part of the planet's outermost E-ring, as you cross a frozen horizon where surface temperatures drop to minus three hundred and thirty deg

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 94.9/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (v00, J0560, 18 Oct 2026)

```text
# Episode gate — 046_Why-Saturns-Moon-Enceladus-Shoots-Geysers-Into-Space

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/046_Why-Saturns-Moon-Enceladus-Shoots-Geysers-Into-Space |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/enceladus_geysers_script_master_v00.md |
| script_review | OK | Script reviewer PASS 94.9/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 43% (19 words): "Every Sunday Orbit goes somewhere new. Subscribe and you'll be there for why Jupiter's Great Red Spot is shrinking." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **94.9/100** · PASS
```
