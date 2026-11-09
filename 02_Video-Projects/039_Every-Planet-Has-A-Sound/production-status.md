# Production status — 039 Why Do Mars and the Other Planets Sound So Strange?

| Field | Value |
|-------|-------|
| Slug | `039_Every-Planet-Has-A-Sound` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-17_J0453.md` (scored 23/30, #1 of 5) |
| Topic lock | **DEFER (J1905, 4 Nov): unlocked candidate; no Short-first waiver. J1984 evidence then J1985 capacity/advancement decision.** J1780 restored the handoff from cancelled J0453/J0461; `1OCNzhkiBuc` (*Why Are the Winds on Neptune Faster Than Sound?*) is Neptune wind speed (`494` views, `42.6%` 7d stayed MISS), and `bSjWiCbB7pY`/`iyvWYFP_ETA`/`RLSJm59OSzI` are private with `0` views, not measured Short-first proof. |
| Script draft | `01_Script/planet_sounds_script_master_v01.md` (v01 drafted 17 Oct 2026 in J0461; 1,251 whitespace spoken words / 1,222 notes / 1,299 reviewer words, ~8.7 min; notes in `01_Script/SCRIPT_NOTES_v01.md`; v00 retained) |
| Script review | **FIX (J1905, 4 Nov).** Historical automated score 95.8/100 from J0461 is not editorial, scientific or script-lock approval. See `jobs/reviews/J1905/CHIEF_EDITORIAL_RULING_2026-11-04.md` for required specialist fixes if advanced. |
| Sources | `01_Script/SOURCES.md` — 7 rows started and pre-checked with verbatim quotes (`NASA Perseverance Rover Components`, `NASA JPL Perseverance Sounds of Mars`, `NASA Perseverance Mars Speed of Sound Release`, `NASA InSight Mars Wind Resource`, `NASA/ESA Cassini-Huygens & Titan Audio`, `University of Iowa Donald Gurnett & Cassini RPWS`, `JPL Saturn-Enceladus Plasma Wave Audio`, `NASA Chandra Perseus Black Hole Sound Waves`, `LOC Name Authority Records n79134100 / n85087745 / n80131454 / n87929862`) |
| Gemini facts pass | Not started; J1985 owns the specialist rewrite → formal Gemini facts → direct quotes/lock chain if advanced. All seven rows remain TO VERIFY. |
| Gate | Production blocked: topic/neighbour and Short-first decision, unsigned prebuild audit, editorial fixes, formal Gemini facts, direct quote check and explicit script lock remain. Outputs below are historical J0461 evidence only. |
| VO | Pending (wait for topic lock + Gemini `facts` + `CLAUDE_QUOTE_CHECK` + Chief script sign-off) |
| CG | Pending (NASA/JPL `PIA24487` Perseverance SuperCam, `PIA24647` Ingenuity, `PIA07232` Huygens Titan descent, `PIA17184`/`PIA19061` Enceladus & Saturn, Chandra Perseus cluster ripples + code graphics + Omni Orbit) |
| Runtime target | 7–9 min (1,222 spoken words / 1,299 reviewer words, ~8.7 min est.) |
| Shorts | 3 episode Shorts on lock |

## Marker counts (`planet_sounds_script_master_v01.md`)

- `DATA:` **7** (all ≥ 3 required; includes 3 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT:` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **4** (every named person in spoken narration at first mention: Christiaan Huygens 1629–1695, Donald Gurnett 1940–2022, James Van Allen 1914–2006, Andrew Fabian born 1948; all verified in LOC Name Authority Records)
- `WHEN:` **6** (Hook: `14 January 2005, 1 minute, 5 hours`; Ch 1: `1 December 2018, 3.5 minutes, 5 hours, 216 Martian days, 30 April 2021`; Ch 3: `14 January 2005, 1 minute, 147 minutes, 2.5 hours, 72 minutes`; Ch 4: `September 1957, 31 January 1958, 13 March 1971, 20 August 1977, 5 September 1977, 60 years`; Ch 5: `November 1990, 15 October 1997, 1 July 2004, 20 October 2015, 2 September 2017, 2 weeks, 16 minutes, 28.5 seconds`; Ch 6: `2002, 53 hours, 9 September 2003, 10 million years, 2.5 billion years`)
- `FACT:` **4** (`Two speeds of sound on Mars`, `Huygens transmitted for 72 minutes`, `Gurnett joined 41 space missions`, `Black hole hums in B-flat`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6)
- **Subscribe beat line:** `"If this is your kind of question, subscribe. Next week is why we're looking for the wrong kind of aliens."` (Line 3 from `templates/SUBSCRIBE_BEAT_LINES.md`, not used in `035`–`038`; 20 words at 42%).
- **First 30 seconds rule (`OWB_2026-10-17.md`):** first `[CHAPTER CARD]` is placed after a 3-paragraph cold open (~143 spoken words, ~0:57), so no full-frame chapter card appears in `0:00–0:30`.

## Pasted `npm run review:script` output (v01, J0461, 17 Oct 2026)

```text
# planet_sounds_script_master_v01.md

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

> Why Do Mars and the Other Planets Sound So Strange? High in orbit above the Red Planet, before NASA landed two microphones on Mars, what secret signal or sound would you hear on the Martian surface or beneath the thick orange-brown atmosphere of Saturn's moon Titan? Equipped with

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (v01, J0461, 17 Oct 2026)

```text
# Episode gate — 039_Every-Planet-Has-A-Sound

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /tmp/j0461-wt/02_Video-Projects/039_Every-Planet-Has-A-Sound |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/planet_sounds_script_master_v01.md |
| script_review | OK | Script reviewer PASS 95.8/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 42% (20 words): "If this is your kind of question, subscribe. Next week is why we're looking for the wrong kind of aliens." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.8/100** · PASS
```

## Handoff repair — 3 November 2026 (J1780)

J0453/J0461 were cancelled as duplicates of J0789/J0802, whose decisions concern only unlocked 061 drafts. No 039 lock is established. J1905 restores topic/editorial review before formal Gemini facts and direct quote checks. See `jobs/reviews/J1780/CHIEF_HANDOFF_2026-11-03.md`. No production approval; v00/v01 and source evidence preserved.

## Chief ruling — 4 November 2026 (J1905)

DEFER topic advancement; FIX script. No Short-first waiver or production approval. J1984 owns neighbours, completed topic audit and matching Short-first evidence (`1OCNzhkiBuc`, *Why Are the Winds on Neptune Faster Than Sound?*, verified live 4 Nov as public with 494 views and 42.6% 7d stayed MISS on Neptune wind speed; `bSjWiCbB7pY`, `iyvWYFP_ETA` and `RLSJm59OSzI` verified live 4 Nov as private with 0 views); J1985 owns capacity/advancement and any specialist rewrite/facts/direct-quotes chain. HOS November is 2/4 complete against OWB 5/4. Reconsider when HOS reaches four completed November films or Chief records a fresh non-displacing capacity rationale, and topic evidence passes. Reconcile incoming 038 (`J1982`) and outgoing 040 (`J1906`) handoffs before script lock; any eventual audio/cut review requires a reviewer with demonstrated `audio_input` capability. Historical notes above are not approval; v00/v01 and SOURCES are unchanged. Full ruling: `jobs/reviews/J1905/CHIEF_EDITORIAL_RULING_2026-11-04.md`. Nothing for Ben.
