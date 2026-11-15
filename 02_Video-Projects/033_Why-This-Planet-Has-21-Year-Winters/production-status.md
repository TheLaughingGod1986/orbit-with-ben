# Production status — 033 Why Knocked-Sideways Uranus Has 21-Year Winters

**Current ruling, 4 November 2026 (J2148, Rule-E review by `gemini`): GO — topic and script (`uranus_21_year_winter_script_master_v02.md`) LOCKED; VO job queued.** Supersedes the earlier Chief topic jobs (`J1896`, `J1969`, `J1970`) under `AGENTS.md` Rule E (WIP raised to 8, Ben 4 Nov 2026). Full review: `jobs/reviews/J2148/REVIEW.md`.

| Field | Value |
|-------|-------|
| Slug | `033_Why-This-Planet-Has-21-Year-Winters` |
| Working title (Rule 15, 47 chars) | `Why Knocked-Sideways Uranus Has 21-Year Winters` |
| Rule-18 real-imagery variants | `What Voyager 2 Saw in Just 6 Hours at Uranus` (44 chars) · `The Only Spacecraft Photos Ever Taken at Uranus` (47 chars) |
| Series (Rule 20) | `Real Worlds` |
| Rule-19 real-frame thumb (Concept A) | **DONE (`J2899` / `J2900` KEEP, £0 local Pillow grade)** (`08_Thumbnail/033_thumb_A_v01.jpg` `21-YEAR WINTER` SHA-256 `9c029267c0a80fbb13572c40cc7b42cf012f2582bfcc3d5c49bf7c8f7a325e6f` sat `131.1` nb `2.3%` on JWST `weic2332a_hires.jpg`; `033_thumb_B_v01.jpg` `COLDER THAN NEPTUNE` SHA-256 `1185ea680e5284c6f893769a94e1280c28a36828803671a445effdc8ed629a8e` sat `151.6` nb `4.4%`; `033_thumb_C_v01.jpg` `97.77° SIDEWAYS` SHA-256 `48abb438ed7a8de3fa0a7d5b1474c725efbc48198c4260b35da5dce5607bc1b2` sat `175.4` nb `2.2%`; `A` & `B` staged to NAS/iCloud `OWB UAT`; `T033` proposed in `THUMB_LEDGER.json`; review: `jobs/reviews/J2900/REVIEW.md`) |
| Gate | `npm run gate:episode` **PASS** (VO / Gemini Veo allowed) |
| Script review | `npm run review:script` **PASS 95.2 / 100** on locked `uranus_21_year_winter_script_master_v02.md` (1,290 spoken words / 1,347 reviewer words, ~9.0 min, 6 chapters; subscribe beat line 6 at 43%) |
| Sources | 15 / 15 MUST QUOTE rows **VERIFIED** live in `01_Script/SOURCES.md` + `01_Script/CLAUDE_QUOTE_CHECK_v01.md` |
| VO | **DONE** (`J2155` / `J2164` KEEP, `02_Voiceover/uranus_vo_v01.wav`, SHA-256 `3d73576e0c20be9030546db7bc71ea0107602d5e5fbdde37cba28c7d5b43f460`, `611.40 s` / `10:11.4`, `-23.3 dB` mean, `-20.22 LUFS`, `-3.77 dBTP`; review: `jobs/reviews/J2164/REVIEW.md`) |
| Shot list | **PASS (Chief `h94`, `J2238` / `d67daf94`); reconciled in `SHOT_LIST_v02.md` (`J2299`)** (`07_Edit-Project/SHOT_LIST_v01.md` & `SHOT_LIST_v02.md` — 67 Scribe-timed rows `0.00–629.40 s`, 144 cuts in `cuts_033_j2299_v01.json`, `4.35 s/cut` mean, 0 split words, 0 adjacent `CODE` rows, `≤ 2` still appearances; `05_Music/MUSIC_BRIEF_v01.md` & `06_Sound-Effects/SFX_PLAN_v01.md`) |
| Picture / Stills lock | **DONE — CHIEF STAGE SIGN-OFF PASS (`J2398`, `jobs/reviews/J2398/REVIEW.md`; moving-video & full-size stills QA `PASS` in `J2300`, `jobs/reviews/J2300/REVIEW.md` — £0 spend, 42 active stills + `R01` + `R55` + 19 code graphics + 1 alias verified KEEP)** (`07_Edit-Project/STILLS_LOCK_v02.md`, `STILLS_POOL_STATUS_v03.json`, `PICTURE_RECONCILIATION_J2299_v01.json`, `cuts_033_j2299_v01.json`, `pool_033_j2299_v01.json`: all 43 pool IDs + aux audited against official records; all 32 caption mismatches & 17 false-subject exclusions enforced; 72 harvest/crop/PDF-raster files synced to NAS `03_Reference-Material/harvest_J2299_v01`; `R01` `r01_sourced_composite_v01_silent.mp4` `aab9aa2af9` and `R55` `r55_passage_v01_silent.mp4` `4aa82d0e72` integrated under `J2386`; `144/144` cuts `≤ 6.00 s`, `0` split words, `picture_qa` PASS 0 fail / 0 warn) |
| CG | **DONE — 20 × 24fps renders KEEP (`J2300` / `J2398` PASS, `19` active + `1` `R26` alias, `0` frozen pairs, £0 Option B)** (`04_Generated-Clips/J2299_code_graphics_v01/` + `07_Edit-Project/CODE_GRAPHICS_J2299_v02.json`: all 20 files directly viewed with `moving_video_input` in `J2300`; `polish_gate` PASS 0 fail; `code_graphic_033_r55_pressure_gauge.mp4` retired per `J2386`; released for long master `v01` assembly in `J2398`) |
| Runtime target | `10:29.4` (`611.40 s` locked VO + `18.00 s` moving end-screen hold `611.40–629.40 s`) |
| Music & SFX | **DONE (`J2317`, £0 house synthesis)** (`05_Music/uranus_score_bed_v01.mp3` SHA-256 `47f68d66c4ef7b0287c4939b14e7d906582309ca2a3354c3c262daa7e21309f0`, `629.40 s`, `70.6 BPM`, `music_gate` PASS; `06_Sound-Effects/kit_v01` house SFX kit `sfx_kit.py make`) |
| Long Master `v04` (`J2889` / `J2890` / `J2893`) | **DONE — CHIEF STAGE SIGN-OFF PASS (`J2893`, `jobs/reviews/J2893/REVIEW.md`; 5-part moving-video/audio review `PASS` in `J2890`, `jobs/reviews/J2890/REVIEW.md`)** (`09_Final-Export/033_why_this_planet_has_21_year_winters_master_v04.mp4`, SHA-256 `3712479ae852dd318c4d8d0dfd18f7df08c1a857068c24c3d3792a35a27f11c3`, `1920x1080`, `24/1` CFR, `15,106` frames / `629.416667 s`, `-14.5 LUFS`, `-1.5 dBTP`, `0` black frames; `_PHONE.mp4` SHA-256 `3ef32f4b673431835449a590f2246de19d84ff32a330893709cb2ccf6b954a19` mirrored to NAS `OWB UAT`, iCloud `OWB UAT` & R2 stream `owb-033-v04`; `J2890` `awaits_ben` armed for Wed 09 Dec 18:00 London slot) |
| Shorts | Standalone Short `ZpEA8stoSPA` (*Why Does Uranus Have 21-Year Winters?*) public 3 Nov 2026 — **461 views, 6 likes on day 1**; **Active Short #1 `v02` (`033_short01_testA_opening_v02.mp4`, SHA-256 `db6a23420952151244161c7be209cdebd0440f3ce4aef314c1ce9fc6a3f9d203`, `36.48 s` Test A opening cut, slot Fri 18 Dec 11:30Z) & Active Short #2 `v02` (`033_short02_ice_giant_surface_v02.mp4`, SHA-256 `279c9531f2c89d16fb37e285b6ef981e8db7bf8d2dd1c297b2940bf07daf5468`, `27.48 s` Keeper question cut, slot Sat 19 Dec 11:30Z) — 5-PART REVIEW PASS (`J2870`, `jobs/reviews/J2870/REVIEW.md`) + BEN OK 15 Nov 10:37–10:41Z (`J2896` `96477b52d8` & `J2895` `5772c0c52d` `07_Upload-Package` dry-run PASS, held until `033` long is public)** |

## Blockers

- [x] Topic lock + neighbour pass (10 education/space videos at 1.24M–7.63M views in `TOPIC_OPPORTUNITY_SCORE.md`) + Pre-build vidIQ signed (`J2148`)
- [x] Script v02 ≥ 90 (`review:script` PASS 95.2/100 on `uranus_21_year_winter_script_master_v02.md`, 1,290 spoken words)
- [x] Direct quote check on `01_Script/SOURCES.md` + `CLAUDE_QUOTE_CHECK_v01.md` (15/15 PASS)
- [x] VO take (`vo_take.py` from `uranus_21_year_winter_script_master_v02.md` — `uranus_vo_v01.wav`, `611.40 s`, accepted in `J2164` / `jobs/reviews/J2164/REVIEW.md`)
- [x] Timed shot list + music brief + SFX plan (`J2165` / Chief `h94` PASS in `J2238`: `07_Edit-Project/SHOT_LIST_v01.md`, `05_Music/MUSIC_BRIEF_v01.md`, `06_Sound-Effects/SFX_PLAN_v01.md`)
- [x] Stills-lock & picture-plan note + OMNI `R29`/`R55` price-pass brief (`J2256`: `07_Edit-Project/STILLS_LOCK_v01.md`, `07_Edit-Project/STILLS_POOL_STATUS_v01.json`, `07_Edit-Project/OMNI_PRICE_PASS_BRIEF_v01.md`, `jobs/reviews/J2256/REVIEW.md` — 5/43 pool assets + 2 aux verified with SHA-256, 38 missing IDs listed for £0 harvest, all stills locked `≤ 2` appearances, £0 spend)
- [x] `J2386` Chief ruling on `R01` (`r01_sourced_composite_v01_silent.mp4` `aab9aa2af9`) and `R55` (`r55_passage_v01_silent.mp4` `4aa82d0e72`) (`jobs/reviews/J2386/CHIEF_RULING.md`)
- [x] `J2299` source-identity reconciliation (`43` pool IDs + aux, `32` caption mismatches, `17` false-subject exclusions), `72`-file NAS harvest (`03_Reference-Material/harvest_J2299_v01`), `20` × `24 fps` code graphics (`04_Generated-Clips/J2299_code_graphics_v01`), `SHOT_LIST_v02.md`, `STILLS_LOCK_v02.md`, `cuts_033_j2299_v01.json` (`picture_qa` PASS `0` fail / `0` warn), and opener+graphics review reel (`polish_gate` PASS `0` fail)
- [x] `J2300` moving-video QA of opener and graphics + full-size stills inspection (`PASS`, `jobs/reviews/J2300/REVIEW.md`: all 21 moving clips directly viewed with `moving_video_input`, all 42 active stills inspected full size, `144/144` cuts `≤ 6.00 s`, `0` split words)
- [x] `J2317` Active Short #1 (`033_short01_testA_opening_v01.mp4`, `36.48 s` Test A opening cut, SHA-256 `7eca95258582b93f6b822e182bf64db8d6e31d95f3710b4479182df4f5182ca7`) built & passed all 7 tool gates (`gate_shorts_open`, `picture_qa`, `polish_gate`, `sfx_kit level`, `music_gate`, `thumb_preview` frame 0 & cover)
- [x] `J2318` Active Short #2 (`033_short02_ice_giant_surface_v01.mp4`, `26.28 s` Keeper question cut, SHA-256 `c2404d5a05ada2c257bf9e5fdc2b10edaa126d36de6aa32b38cb27df6d08dbc2`) built & passed all 7 tool gates (`gate_shorts_open`, `picture_qa`, `polish_gate`, `sfx_kit level`, `music_gate`, `thumb_preview` frame 0 & cover)
- [x] Protected Chief picture stage sign-off & long master assembly release (`J2398` PASS, `jobs/reviews/J2398/REVIEW.md`)
- [x] `033` Long Master `v01` (`629.40 s`, `67` rows / `144` cuts) assembly + all 5 tool gates (`J2403` PASS, `07_Edit-Project/ASSEMBLY_HANDOFF_J2403_v01.md`: `clip_check` 67 rows PASS, `picture_qa` 0/144 fail 8 warn PASS, `polish_gate` 0/144 fail PASS, `music_gate` 629.4 s 70.6 BPM PASS, `sfx_kit level` VO -20.2 / SFX -47.2 LUFS 21 hits PASS, `-14.5 LUFS` / `-1.5 dBTP` / `24/1` CFR / `0` black frames)
- [x] `033` Long Master `v04` (`629.42 s`, `67` rows / `147` cuts) moving-video/audio review (`J2890` PASS `KEEP`, `jobs/reviews/J2890/REVIEW.md`, reviewing `J2889` `033_why_this_planet_has_21_year_winters_master_v04.mp4` SHA-256 `3712479ae852dd318c4d8d0dfd18f7df08c1a857068c24c3d3792a35a27f11c3`; R2 stream `owb-033-v04` live; `J2890` armed `awaits_ben` for Wed 09 Dec 18:00 London slot)
- [x] `033` Active Shorts 1 & 2 `v02` 5-part moving-video review (`J2870` PASS `KEEP`, `jobs/reviews/J2870/REVIEW.md`) + Ben phone watch OK'd 15 Nov 10:37–10:41Z (`J2896` `96477b52d8` & `J2895` `5772c0c52d` `07_Upload-Package` built & dry-run verified, held on `public` hold until `033` long airs Wed 09 Dec 18:00 London)
- [x] Protected Chief `033` `edit` stage sign-off (`J2893` PASS `KEEP`, `jobs/reviews/J2893/REVIEW.md`; `stages.edit.state = "done"`)
- [x] `033` long thumbnails `A`/`B`/`C` build & review (`J2899` -> `J2900` PASS `KEEP`, `jobs/reviews/J2900/REVIEW.md`: `033_thumb_{A,B,C}_v01.jpg` all PASS `thumb_preview.py long --score` + `HOOK/BAND/GRADE/PHONE`; `A` & `B` staged to NAS/iCloud `OWB UAT`; `T033` proposed in `THUMB_LEDGER.json`; `stages.thumbs.state = "done"`)
- [ ] `033` `11_Upload-Package` build & dry-run (`J2901`, after `J2900`; no live upload until Ben approves `J2890`)
- [ ] Ben UAT watch on `033` Long Master `v04` (`J2890` `awaits_ben`)

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
