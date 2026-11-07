# Production status — 036 Why Is There Ice on Mercury, the Planet Closest to the Sun?

| Field | Value |
|-------|-------|
| Slug | `036_Why-Is-There-Ice-On-Mercury` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-16_J0403.md` (scored 25/30, #1 of 5) |
| Topic lock | **DEFER — J1900; evidence J1977 then Chief J1978** (`J0403` cancelled without a 036 decision; originally parked for Chief: lock 036 or pick #2 Milky Way Centre / #3 Left in Space / #4 Planet Sounds; decide Short-first waiver vs standalone Short `vlkj8RQKmH8`) |
| Script draft | `01_Script/mercury_polar_ice_script_master_v01.md` (v01 drafted 16 Oct 2026 in J0411; 1,278 spoken words / 1,298 reviewer words, ~8.7 min; notes in `01_Script/SCRIPT_NOTES_v01.md`) |
| Script review | **FIX — J1900; historical automated score 95.8 / 100 only** (1,278 spoken words / 1,298 reviewer words, ~8.7 min, 6 chapters, 8/8 structure gates, 0 warnings) |
| Sources | `01_Script/SOURCES.md` — 10 rows started and pre-checked with verbatim quotes (`NASA Mercury Facts`, `NASA MESSENGER`, `NASA Mariner 10`, `NASA BepiColombo`, `NASA Mercury's Strange Hollows`, `NASA Release 15-079`, `JHU Gazette / MESSENGER Release`, `NSSDCA Mercury Fact Sheet`, `JPL Photojournal PIA19411 / PIA16523 / PIA18748 / PIA16522 / PIA15160`, `LOC Name Authority Records n88291472 / nr93014292 / n80020330 / n50054908`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| VO | Pending (wait for topic lock + Gemini `facts` + `CLAUDE_QUOTE_CHECK` + Chief script sign-off) |
| CG | Pending (NASA PIA19411 / PIA16523 / PIA18748 / PIA16522 / PIA15160 + code graphics + Omni Orbit) |
| Runtime target | 7–9 min (1,278 spoken words / 1,298 reviewer words, ~8.7 min est.) |
| Shorts | Paired with standalone Short `vlkj8RQKmH8` (*A Day on Mercury Lasts Two Years*, scheduled 24 Oct 2026) + 3 episode Shorts on lock |

## Marker counts (`mercury_polar_ice_script_master_v01.md`)

- `DATA:` **7** (all ≥ 3 required; includes 2 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT:` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **4** (every named person in spoken narration at first mention: Giuseppe Colombo 1920–1984, Sean Solomon born 1945, Sergei Prokofiev 1891–1953, Sergei Rachmaninoff 1873–1943; all verified in LOC Name Authority Records)
- `WHEN:` **7** (Hook: `2011 to 2015`; Ch 1: `1965`; Ch 2: `3 November 1973, 5 February 1974, 29 March 1974, 21 September 1974, 16 March 1975`; Ch 3: `1991, 3 August 2004, August 2005, October 2006, June 2007, 2008, 2009, 18 March 2011`; Ch 4: `August 2012`; Ch 5: `4 billion years ago, 100,000 years ago`; Ch 6: `30 April 2015, 20 October 2018, October 2021, January 2025, November 2026`)
- `FACT:` **4** (`A day lasts 2 years`, `Core is 85% of radius`, `2-degree tilt traps ice`, `Hollows 100,000 years old`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6)
- **Subscribe beat line:** `"We make one of these every week. Subscribing is how the next one finds you."` (Line 4 from `templates/SUBSCRIBE_BEAT_LINES.md`, not used in `031`–`035`; 15 words at 42%).
- **First 30 seconds rule (`OWB_2026-10-16.md`):** first `[CHAPTER CARD]` is placed after a 3-paragraph cold open (~148 spoken words, ~0:55), so no full-frame chapter card appears in `0:00–0:30`.

## Pasted `npm run review:script` output (v01, J0411, 16 Oct 2026)

```text
# mercury_polar_ice_script_master_v01.md

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

Words: 1298 · Est. min: 8.7 · Chapters: 6

## Cold open excerpt

> Why Is There Ice on Mercury, the Planet Closest to the Sun? If you stood on the cratered rim of Mercury's north pole — in orbit closest to the Sun — what would you see glittering inside the darkness below its horizon? At an average distance of fifty-eight million kilometres from 

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (v01, J0411, 16 Oct 2026)

```text
# Episode gate — 036_Why-Is-There-Ice-On-Mercury

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/036_Why-Is-There-Ice-On-Mercury |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/mercury_polar_ice_script_master_v01.md |
| script_review | OK | Script reviewer PASS 95.8/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 42% (15 words): "We make one of these every week. Subscribing is how the next one finds you." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.8/100** · PASS
```

## Workflow repair — J1777, 3 November 2026

J1900 now owns the Chief topic/editorial decision on OWB:036/script, after J1777. J0403/J0411 were cancelled citing J0789/J0802, which reviewed only 061. J0804 deferred 035–061 locks; the credit reset does not itself approve a topic. Mercury remains an unlocked candidate.

The 95.8 score and pasted gate output above are historical automated results, not a current editorial or scientific PASS. The pre-build audit is unsigned and blank; all ten source rows remain TO VERIFY, and formal Gemini facts plus direct MUST QUOTE checks are outstanding. J1900 must resolve neighbour/Short-first evidence, the opening and graphics issues, and queue any rewrite and dependent facts/lock work if advancing. The 24 October Short schedule above is historical, not a current readback. No VO, media or publishing approval.

Evidence and handoff: `jobs/reviews/J1777/CHIEF_HANDOFF_2026-11-03.md`. No spend or Ben action required by this repair.

## Chief editorial decision — J1900, 4 November 2026

**DEFER topic advancement; FIX script.** Retain the unlocked polar-ice candidate. HOS November is 2/4 complete against OWB 5/4; focus unchanged. No Short-first waiver or production approval.

The 4 November stored snapshot records `vlkj8RQKmH8` public with 851 views. The 3 November 07:03:36Z lifetime Studio read records 32.1% stayed-to-watch (below 40%) and 76.1% average viewed (a different metric). Its day-length promise is not automatic polar-ice-topic proof. The old scheduling prose above is historical.

J1977 owns verified neighbours, topic opportunity/pre-build audit and matching Short evidence. J1978 then owns advancement after evidence and capacity checks: HOS November reaches four completed films, or Chief records a fresh specific priority rationale without displacing focus. No approval from elapsed time, dependency completion or credit reset.

If advanced, J1978 must queue specialist v02 rewrite, formal Gemini facts via agy on all ten source rows/revised claims, and dependent Chief direct quotes and explicit script lock with current gates. Preserve v00/v01. No VO before the whole chain passes.

Full editorial FIX and release conditions: `jobs/reviews/J1900/CHIEF_EDITORIAL_RULING_2026-11-04.md`. Nothing required from Ben; no spend or publishing changes.


## Topic go/no-go package prepared — 7 November 2026 (J2327)

- **Scope:** Plans and pre-build evidence only (`£0` / `0` credits; `036` remains in `next` #2 behind the 5-film `active` cap `030`–`034`; `v00`/`v01` and `SOURCES.md` untouched).
- **Files prepared in `11_Upload-Package/`:**
  - `TOPIC_OPPORTUNITY_SCORE.md` (**91 / 100 — CONDITIONAL GO**)
  - `PRE_BUILD_VIDIQ_AUDIT.md` (filled with `2026-11-07` signed-out YouTube GB data; Section 7 left **UNSIGNED** until `036` enters `active` and passes `v02` rewrite + `facts` pass per `J1900`)
  - `TOPIC_GO_NO_GO_SHEET.md` (one-page decision summary + entry checklist)
- **Key evidence (`2026-11-07 01:44 UTC`):** `7` verified education/space neighbours `≥1M` views (`1.16M–4.07M`, led by Astrum's *What They Didn't Teach You at School about Planet Mercury* `B588JHKSlEE` at **4,071,155 views** and Astrum's 2 Sep 2026 *Why Is the Closest Planet to the Sun So Cold?* `YQ7DWNhjOpk` at **2,703,364 views**); Mercury day-length Short `vlkj8RQKmH8` at **851 views / 32.1% stayed-to-watch (<40%) / 76.1% avg viewed** (`0` polar-ice OWB Shorts, so entry uses Rule E comparable-video waiver via `YQ7DWNhjOpk` `2.70M` or 1 polar-ice Short test); 0-collision `≤50`-char titles locked (`Why Mercury's Shadowed Craters Are Full of Ice`, 46 chars [Rule 15] / `What MESSENGER Saw Inside Mercury's Polar Craters`, 49 chars [Rule 18], replacing 59-char `v01` H1 and 1-collision `Why Is There Ice on Mercury?`); real NASA MESSENGER `PIA19411` + `PIA16523` thumbnail concept (no Orbit, Rule 19). Consolidated report: `jobs/reviews/J2327/REVIEW.md`.
