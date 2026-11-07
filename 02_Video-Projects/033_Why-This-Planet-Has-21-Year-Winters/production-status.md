# Production status — 033 Why Knocked-Sideways Uranus Has 21-Year Winters

**Current ruling, 4 November 2026 (J2148, Rule-E review by `gemini`): GO — topic and script (`uranus_21_year_winter_script_master_v02.md`) LOCKED; VO job queued.** Supersedes the earlier Chief topic jobs (`J1896`, `J1969`, `J1970`) under `AGENTS.md` Rule E (WIP raised to 8, Ben 4 Nov 2026). Full review: `jobs/reviews/J2148/REVIEW.md`.

| Field | Value |
|-------|-------|
| Slug | `033_Why-This-Planet-Has-21-Year-Winters` |
| Working title (Rule 15, 47 chars) | `Why Knocked-Sideways Uranus Has 21-Year Winters` |
| Rule-18 real-imagery variants | `What Voyager 2 Saw in Just 6 Hours at Uranus` (44 chars) · `The Only Spacecraft Photos Ever Taken at Uranus` (47 chars) |
| Series (Rule 20) | `Real Worlds` |
| Rule-19 real-frame thumb (Concept A) | NASA/ESA/CSA JWST NIRCam real frame `PIA25770` (`STScI-01GWQ3`, 2023 sideways Uranus + vertical rings) or NASA/JPL Voyager 2 real frame `PIA18182` (24 Jan 1986), graded, hook `21-YEAR WINTER` |
| Gate | `npm run gate:episode` **PASS** (VO / Gemini Veo allowed) |
| Script review | `npm run review:script` **PASS 95.2 / 100** on locked `uranus_21_year_winter_script_master_v02.md` (1,290 spoken words / 1,347 reviewer words, ~9.0 min, 6 chapters; subscribe beat line 6 at 43%) |
| Sources | 15 / 15 MUST QUOTE rows **VERIFIED** live in `01_Script/SOURCES.md` + `01_Script/CLAUDE_QUOTE_CHECK_v01.md` |
| VO | **DONE** (`J2155` / `J2164` KEEP, `02_Voiceover/uranus_vo_v01.wav`, SHA-256 `3d73576e0c20be9030546db7bc71ea0107602d5e5fbdde37cba28c7d5b43f460`, `611.40 s` / `10:11.4`, `-23.3 dB` mean, `-20.22 LUFS`, `-3.77 dBTP`; review: `jobs/reviews/J2164/REVIEW.md`) |
| Shot list | **PASS (Chief `h94`, `J2238` / `d67daf94`)** (`07_Edit-Project/SHOT_LIST_v01.md` — 67 Scribe-timed rows `0.00–629.40 s`, `4.53 s/cut` mean, 0 split words, 0 adjacent `CODE` rows, `≤ 2` still appearances across 43 NASA/JWST/ESA/Wikimedia assets; `05_Music/MUSIC_BRIEF_v01.md` & `06_Sound-Effects/SFX_PLAN_v01.md`) |
| Picture / Stills lock | **STILLS LOCK + OMNI R29/R55 PRICE-PASS BRIEF DRAFTED (`J2256` — parked for Chief)** (`07_Edit-Project/STILLS_LOCK_v01.md`, `07_Edit-Project/STILLS_POOL_STATUS_v01.json`, `07_Edit-Project/OMNI_PRICE_PASS_BRIEF_v01.md`, `jobs/reviews/J2256/REVIEW.md`: 5/43 pool assets + 2 aux verified on disk/NAS with SHA-256; 38 missing IDs + `PIA00271` listed for £0 harvest; every still locked to `≤ 2` appearances; Frame 0 locked to `PIA01283` + `PIA01280`; £0 spend) |
| CG | pending Chief price pass (`07_Edit-Project/OMNI_PRICE_PASS_BRIEF_v01.md`: 2 `[ORBIT ACTS]` rows `R29` & `R55` flagged `OMNI (flag)` with complete £0 `CODE`/`NASA` fallbacks; no Veo/Omni minted) |
| Runtime target | `10:29.4` (`611.40 s` locked VO + `18.00 s` moving end-screen hold `611.40–629.40 s`) |
| Long air slot | **Wed 9 Dec 2026 18:00 Europe/London (`2026-12-09T18:00:00Z`)** (`J2023` / `J2223`) |
| Shorts | **`10_Shorts/SHORTS_PLAN_v01.md` LOCKED (`J2223` · 2 Active Shorts queued in `J2317` & `J2318`):** **Short #1 (Test A Opening Short, `J2317`):** *Why Does Knocked-Sideways Uranus Have 21-Year Winters?* — **Fri 18 Dec 2026 11:30 London** [Path A Default] / **Sat 12 Dec 11:30 London** [Path B]; **Short #2 (Keeper Question Short, `J2318`):** *What Happens If a Spacecraft Tries to Land on Ice Giant Uranus?* — **Sat 19 Dec 2026 11:30 London** [Path A Default] / **Fri 18 Dec 11:30 London** [Path B]; Reserve Short #3 (*Why Would a Rock Take 10 Minutes to Fall Off a Cliff on Uranus's Moon Miranda?*) held under 4 Nov 2-Short cap; standalone Short `ZpEA8stoSPA` public 3 Nov 2026 (461 views day 1) |

## Blockers

- [x] Topic lock + neighbour pass (10 education/space videos at 1.24M–7.63M views in `TOPIC_OPPORTUNITY_SCORE.md`) + Pre-build vidIQ signed (`J2148`)
- [x] Script v02 ≥ 90 (`review:script` PASS 95.2/100 on `uranus_21_year_winter_script_master_v02.md`, 1,290 spoken words)
- [x] Direct quote check on `01_Script/SOURCES.md` + `CLAUDE_QUOTE_CHECK_v01.md` (15/15 PASS)
- [x] VO take (`vo_take.py` from `uranus_21_year_winter_script_master_v02.md` — `uranus_vo_v01.wav`, `611.40 s`, accepted in `J2164` / `jobs/reviews/J2164/REVIEW.md`)
- [x] Timed shot list + music brief + SFX plan (`J2165` / Chief `h94` PASS in `J2238`: `07_Edit-Project/SHOT_LIST_v01.md`, `05_Music/MUSIC_BRIEF_v01.md`, `06_Sound-Effects/SFX_PLAN_v01.md`)
- [x] Stills-lock & picture-plan note + OMNI `R29`/`R55` price-pass brief (`J2256`: `07_Edit-Project/STILLS_LOCK_v01.md`, `07_Edit-Project/STILLS_POOL_STATUS_v01.json`, `07_Edit-Project/OMNI_PRICE_PASS_BRIEF_v01.md`, `jobs/reviews/J2256/REVIEW.md` — 5/43 pool assets + 2 aux verified with SHA-256, 38 missing IDs listed for £0 harvest, all stills locked `≤ 2` appearances, £0 spend)
- [x] Shorts slots & two-Short build plan locked (`J2223`: `10_Shorts/SHORTS_PLAN_v01.md`; Path A Default `Fri 18 Dec` & `Sat 19 Dec 11:30 London` / Path B `Sat 12 Dec` & `Fri 18 Dec 11:30 London`; build jobs `J2317` & `J2318` queued after `J2300`)
- [ ] Chief price-pass decision on `R29`/`R55` (`J2299` / `J2300`), long assembly, and Shorts builds (`J2317` & `J2318`)

## `npm run review:script` & `npm run gate:episode` (J2148, 4 Nov 2026)

```
# uranus_21_year_winter_script_master_v02.md

**Decision:** PASS · **Score:** 95.2 / 100

| Dimension | Score |
|---|---:|
| hook | 10 |
| curiosity | 9.1 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 9.8 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1347 · Est. min: 9 · Chapters: 6

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.2/100 — proceed to VO after production checklist.

Pass threshold: 90

# Episode gate — 033_Why-This-Planet-Has-21-Year-Winters

**Decision:** PASS — VO / Gemini Veo allowed

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /tmp/J2148-wt/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters |
| prebuild_vidiq | OK | Pre-build vidIQ audit present and looks signed off. |
| script_file | OK | Script: 01_Script/uranus_21_year_winter_script_master_v02.md |
| script_review | OK | Script reviewer PASS 95.2/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 43% (17 words): "If you've enjoyed the ride so far, subscribing is the best way to help Orbit keep going." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.2/100** · PASS
```
