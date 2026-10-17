# Production status — 038 Why Will Voyager 1 and the Golden Record Outlive the Earth?

| Field | Value |
|-------|-------|
| Slug | `038_What-We-Left-In-Space-Voyager-Golden-Record` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-17_J0437.md` (scored 25/30, #1 of 5) |
| Topic lock | **Pending Chief decision** (`J0437` parked for Chief: lock 038 or pick #2 Planet Sounds / #3 Wrong Kind of Aliens / #4 Io Volcanoes; confirm whether scheduled standalone Short `kKN8Ale42sE` *Voyager 1 Is About to Be One Light-Day Away* airing 17 Nov 2026 satisfies Short-first) |
| Script draft | `01_Script/voyager_golden_record_script_master_v01.md` (v01 drafted 17 Oct 2026 in J0446; 1,221 spoken words / 1,299 reviewer words, ~8.7 min; notes in `01_Script/SCRIPT_NOTES_v01.md`; revised from v00 drafted in J0437) |
| Script review | **PASS — 95.4 / 100** (1,221 spoken words / 1,299 reviewer words, ~8.7 min, 6 chapters, 8/8 structure gates, 0 warnings; parked for Chief script review in `J0446`) |
| Sources | `01_Script/SOURCES.md` — 9 rows started and pre-checked with verbatim quotes (`NASA Science Voyager 1`, `NASA Voyager 1 What Is a Light-Day?`, `NASA Apollo 11`, `NASA Science Pioneer 10`, `NASA Voyager Golden Record Contents / Making / Cover`, `NASA Pale Blue Dot / Fast Facts`, `JPL Release Ed Stone`, `NASA Voyager Interstellar Mission / Q&A with Dr. Ed Stone / FAQ`, `NASA Perseverance Rover Components`, `LOC Name Authority Records n80008815 / n79064998 / n84081625 / n79092362 / n79021791 / n83017119`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| VO | Pending (wait for topic lock + Gemini `facts` + `CLAUDE_QUOTE_CHECK` + Chief script sign-off) |
| CG | Pending (NASA/JPL `PIA14113` Golden Record, `PIA23645` Pale Blue Dot, Pioneer 10 plaque, Voyager 1 & 2 spacecraft + code graphics + Omni Orbit) |
| Runtime target | 7–9 min (1,221 spoken words / 1,299 reviewer words, ~8.7 min est.) |
| Shorts | 3 episode Shorts on lock + standalone Short `kKN8Ale42sE` (*Voyager 1 Is About to Be One Light-Day Away*, airing 17 Nov 2026) |

## Marker counts (`voyager_golden_record_script_master_v01.md`)

- `DATA:` **7** (all ≥ 3 required; includes 3 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT:` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **6** (every named person in spoken narration at first mention: Neil Armstrong 1930–2012, Carl Sagan 1934–1996, Frank Drake 1930–2022, Ann Druyan born 1949, Jimmy Carter 1924–2024, Edward C. Stone 1936–2024; all verified in LOC Name Authority Records)
- `WHEN:` **7** (Hook: `5 September 1977, March 2012, 18 November 2026, 4.51 billion years`; Ch 1: `20 July 1969, 2 March 1972, 4 December 1973, 1977, 13 June 1983, 17 February 1998, 23 January 2003, 2 million years`; Ch 2: `6,000 years ago, 1977, 23 August 1977`; Ch 3: `0.70 billionths of a second, 8 milliseconds, 3.6 seconds, 1 hour, 4.51 billion years`; Ch 4: `1972, 20 August 1977, 5 September 1977, 15 December 1977, 5 March 1979, 1980, 12 November 1980, 1981, 14 February 1990, 25 August 2012, 2022`; Ch 5: `1970s, 1980, December 2004, March 2012, 25 August 2012, 13 months, April 2013, 5 November 2018`; Ch 6: `5 September 1977, 25 August 2012, 18 November 2026, 2036, 300 years, 30,000 years, 40,272 AD (40,000 years)`)
- `FACT:` **4** (`Last signal took 11 hours`, `Greetings in 55 languages`, `Uranium clock lasts billions of years`, `Cameras turned off in 1990`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6)
- **Subscribe beat line:** `"If you'd like more questions like this one, subscribing really helps a small channel."` (Line 1 from `templates/SUBSCRIBE_BEAT_LINES.md`, not used in `033`–`037`; 14 words at 36%).
- **First 30 seconds rule (`OWB_2026-10-17.md`):** first `[CHAPTER CARD]` is placed after a 3-paragraph cold open (~135 spoken words, ~0:54), so no full-frame chapter card appears in `0:00–0:30`.

## Pasted `npm run review:script` output (v01, J0446, 17 Oct 2026)

```text
# voyager_golden_record_script_master_v01.md

**Decision:** PASS · **Score:** 95.4 / 100

| Dimension | Score |
|---|---:|
| hook | 10 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 9.6 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1299 · Est. min: 8.7 · Chapters: 6

## Cold open excerpt

> Why Will Voyager 1 and the Golden Record Outlive the Earth? Already far beyond Neptune's orbit, nearly twenty-six billion kilometres from Earth in interstellar space, what secret message would you find bolted to Voyager 1? Launched on 5 September 1977 and cruising at nearly sixty

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.4/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (v01, J0446, 17 Oct 2026)

```text
# Episode gate — 038_What-We-Left-In-Space-Voyager-Golden-Record

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/038_What-We-Left-In-Space-Voyager-Golden-Record |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/voyager_golden_record_script_master_v01.md |
| script_review | OK | Script reviewer PASS 95.4/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 36% (14 words): "If you'd like more questions like this one, subscribing really helps a small channel." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.4/100** · PASS
```
