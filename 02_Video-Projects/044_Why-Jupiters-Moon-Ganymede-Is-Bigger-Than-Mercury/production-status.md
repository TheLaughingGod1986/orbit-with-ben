# Production status — 044 Why Is Jupiter's Moon Ganymede Bigger Than the Planet Mercury?

| Field | Value |
|-------|-------|
| Slug | `044_Why-Jupiters-Moon-Ganymede-Is-Bigger-Than-Mercury` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-18_J0529.md` (scored 19/30, #1 of 5) |
| Topic lock | **Pending Chief decision** (`J0529` parked for Chief: lock 044 Ganymede Bigger Than Mercury or pick #2 Terraform Mars / #3 Enceladus Geysers / #4 Great Red Spot Shrinking / #5 Simulation Physics; confirm Short-first waiver) |
| Script draft | `01_Script/ganymede_bigger_than_mercury_script_master_v01.md` (v01 drafted 18 Oct 2026 in J0538, revised from v00 in J0529; 1,262 spoken words / 1,298 reviewer words, ~8.7 min; notes in `01_Script/SCRIPT_NOTES_v01.md`) |
| Script review | **PASS — 95.3 / 100** (1,262 spoken words / 1,298 reviewer words, ~8.7 min, 6 chapters, 8/8 structure gates, 0 warnings; parked for Chief script review in `J0538`) |
| Sources | `01_Script/SOURCES.md` — 17 rows updated to v01 and pre-checked with verbatim quotes (`NASA Ganymede Facts & Overview`, `NSSDCA Galilean Satellites Fact Sheet`, `NASA Mercury Facts`, `NASA Galileo Mission`, `NASA Margaret Kivelson Profile`, `NASA Hubble Ganymede Ocean 2015`, `NASA Juno Ganymede Salts 2023`, `NASA Hubble Ganymede Water Vapor 2021`, `ESA/NASA JUICE Factsheet`, `NASA Mars Facts`, `LOC Name Authority Records n79003254 / n79067868 / n79006997 / n83213689 / nb2017004412`) |
| Gemini facts pass | Pending topic lock (`SOURCES.md` pre-populated for Gemini `facts` job) |
| Gate | BLOCK on `prebuild_vidiq` sign-off only (all script/structure checks OK; `npm run review:script` + `npm run gate:episode` pasted below) |
| VO | Pending (wait for topic lock + Gemini `facts` + `CLAUDE_QUOTE_CHECK` + Chief script sign-off) |
| CG | Pending (NASA Juno `PIA24681`, Galileo & Voyager 2 Ganymede mosaics, Hubble STIS UV auroral ovals `STScI-01EVVCEB83XGWY8WFTS7R5FAQN`, MESSENGER Mercury, ESA JUICE + code graphics + Omni Orbit) |
| Runtime target | 7–9 min (1,262 spoken words / 1,298 reviewer words, ~8.7 min est.) |
| Shorts | 3 episode Shorts on lock |

## Marker counts (`ganymede_bigger_than_mercury_script_master_v01.md`)

- `DATA:` **7** (all ≥ 3 required; includes 3 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT:` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **5** (every named person in spoken narration at first mention: Galileo Galilei 1564–1642, Robert A. Heinlein 1907–1988, Arthur C. Clarke 1917–2008, Margaret Kivelson born 1928, John Grunsfeld born 1958; verified in LOC Name Authority Records `n79003254`, `n79067868`, `n79006997`, `n83213689`, `nb2017004412`)
- `WHEN:` **7** (Hook: `4.5 billion years ago, 1610, 1996, 2015, 2021, 2031`; Ch 1: `4.5 billion years ago, January 7, 1610`; Ch 2: `43 minutes, 7.155 Earth days, 12 Earth years, 1950, June 27, 1996, 2004`; Ch 3: `October 18, 1989, December 7, 1995, June 26, 1996, 1998`; Ch 4: `1970s, 2002, 2014, March 12, 2015`; Ch 5: `1998 to 2010, 2018, June 7, 2021, July 26, 2021, October 30, 2023`; Ch 6: `April 14, 2023, July 2031, 4 years`)
- `FACT:` **4** (`Wider than planet Mercury`, `Only moon with magnetosphere`, `Ocean ten times deeper`, `Eighty-five square metres`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6)
- **Subscribe beat line:** `"Stay for the rest of this one, and subscribe for why even a robot needs help on Mars."` (Line 2 from `templates/SUBSCRIBE_BEAT_LINES.md`, rotated from `040`–`043`; 18 words at 47%).
- **First 30 seconds rule (`OWB_2026-10-18.md`):** first `[CHAPTER CARD]` is placed after a 3-paragraph cold open (~148 spoken words, ~0:59), so no full-frame chapter card appears in `0:00–0:30`.

## Pasted `npm run review:script` output (v01, J0538, 18 Oct 2026)

```text
# ganymede_bigger_than_mercury_script_master_v01.md

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

Words: 1298 · Est. min: 8.7 · Chapters: 6

## Cold open excerpt

> Why Is Jupiter's Moon Ganymede Bigger Than the Planet Mercury? Orbiting six hundred and sixty-five thousand miles beyond Jupiter, as you cross the horizon of an icy world spanning three thousand two hundred and seventy miles across — wider than both Mercury and Pluto — why is Jup

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.3/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (v01, J0538, 18 Oct 2026)

```text
# Episode gate — 044_Why-Jupiters-Moon-Ganymede-Is-Bigger-Than-Mercury

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/044_Why-Jupiters-Moon-Ganymede-Is-Bigger-Than-Mercury |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/ganymede_bigger_than_mercury_script_master_v01.md |
| script_review | OK | Script reviewer PASS 95.3/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 47% (18 words): "Stay for the rest of this one, and subscribe for why even a robot needs help on Mars." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.3/100** · PASS
```
