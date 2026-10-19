# Production status — 053 Why NASA's Parker Solar Probe Flew Inside the Sun's Corona without Melting

| Field | Value |
|-------|-------|
| Slug | `053_Why-NASAs-Parker-Solar-Probe-Flew-Inside-The-Suns-Corona-Without-Melting` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-19_J0666.md` (scored 30/30 studio rubric / 16/30 audit rubric, #1 of 5; direct hand-off from `052`) |
| Topic lock | **Pending Chief decision** (`J0666` parked for Chief: lock `053` *Why NASA's Parker Solar Probe Flew Inside the Sun's Corona without Melting* or pick another candidate from `IDEAS_2026-10-19_J0666.md`; confirm Short-first waiver) |
| Script draft | `01_Script/parker_solar_probe_script_master_v00.md` (`v00` drafted 19 Oct 2026 in `J0666`; 1,397 reviewer words, ~9.3 min; notes in `01_Script/SCRIPT_NOTES_v00.md`) |
| Script review | **PASS — 92.5 / 100** (1,397 reviewer words, ~9.3 min, 6 chapters, 8/8 structure gates, 0 warnings; parked for Chief topic lock & script review in `J0666`) |
| Sources | `01_Script/SOURCES.md` — 12 claim rows verified verbatim across primary NASA Science, NASA Feature, Johns Hopkins APL, NASA Parker Solar Probe Blog, and LOC Name Authority sources (`science.nasa.gov/mission/parker-solar-probe/`, `nasa.gov/general/traveling-to-the-sun-why-wont-parker-solar-probe-melt/`, `parkersolarprobe.jhuapl.edu/Spacecraft/index.php`, `jhuapl.edu/news/news-releases/211214-parker-solar-probe-touches-the-sun`, `science.nasa.gov/blogs/parker-solar-probe/2026/09/10/after-latest-swing-past-sun-nasas-parker-solar-probe-checks-in/`, `science.nasa.gov/blogs/parker-solar-probe/2026/06/11/parker-solar-probe-makes-28th-close-pass-of-sun/`, `LOC Name Authority n78096083 / n50035250`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| VO | Pending (wait for topic lock + Gemini `facts` + `CLAUDE_QUOTE_CHECK` + Chief script sign-off) |
| CG | Pending (real NASA/JHUAPL Parker Solar Probe WISPR coronal imagery, TPS lab test footage, Solar Probe Cup Odeillo Solar Furnace test footage + 7 custom animated code graphics + Omni Orbit) |
| Runtime target | 7–9.5 min (1,397 reviewer words, ~9.3 min est.) |
| Shorts | 3 episode Shorts on lock |

## Marker counts (`parker_solar_probe_script_master_v00.md`)

- `DATA:` **7** (all ≥ 3 required; includes 3 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **5** (every named person in spoken narration at first mention: `Eugene Parker (1927–2022) — American solar astrophysicist`; `Betsy Congdon — TPS lead thermal engineer`; `Justin Kasper — SWEAP principal investigator`; `Hannes Alfvén (1908–1995) — Swedish plasma physicist`; `Stuart Bale — FIELDS principal investigator`)
- `WHEN:` **7** (Hook: `December 24, 2024, September 4, 2026`; Ch 1: `Mid-1950s, October 3, 2017, August 12, 2018, March 15, 2022`; Ch 2: `1950s`; Ch 3: `2018`; Ch 4: `Pre-launch Odeillo Solar Furnace test`; Ch 5: `8-minute one-way light travel time`; Ch 6: `April 28, 2021, 2019, December 24, 2024, June 19, 2025, September 4, 2026, 2029`)
- `FACT:` **4** (`Million-degree plasma, low heat`, `Tungsten melts at 6,192°F`, `Cooled by one gallon`, `Extended into 2029`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6)
- **Subscribe beat line:** `"If you want the next one, whether we are living inside a simulation, subscribing is how you'll see it."` (Line 3 from `templates/SUBSCRIBE_BEAT_LINES.md`, rotated from `052`'s Line 2; 19 words at 42%).
- **First 30 seconds rule (`OWB_2026-10-19.md`):** first `[CHAPTER CARD]` is placed after a 3-paragraph cold open (~155 spoken words, ~1:05), so no full-frame chapter card appears in `0:00–0:30`.

## Pasted `npm run review:script` output (`v00`, `J0666`, 19 Oct 2026)

```text
# parker_solar_probe_script_master_v00.md

**Decision:** PASS · **Score:** 92.5 / 100

| Dimension | Score |
|---|---:|
| hook | 10 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 7.6 |
| escalation | 10 |
| retentionPotential | 9 |
| searchPotential | 7.8 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1397 · Est. min: 9.3 · Chapters: 6

## Cold open excerpt

> Why Did NASA's Parker Solar Probe Fly Inside the Sun's Corona without Melting? Look at the glowing white rim of NASA's Parker Solar Probe hurtling through the outer atmosphere of the Sun on December 24, 2024, and again on its twenty-ninth close pass on September 4, 2026: it

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 92.5/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (`v00`, `J0666`, 19 Oct 2026)

```text
# Episode gate — 053_Why-NASAs-Parker-Solar-Probe-Flew-Inside-The-Suns-Corona-Without-Melting

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/053_Why-NASAs-Parker-Solar-Probe-Flew-Inside-The-Suns-Corona-Without-Melting |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/parker_solar_probe_script_master_v00.md |
| script_review | OK | Script reviewer PASS 92.5/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 42% (19 words): "If you want the next one, whether we are living inside a simulation, subscribing is how you'll see it." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **92.5/100** · PASS
```
