# Production status — 034 Why Pluto's Frozen Heart Has Zero Craters

| Field | Value |
|-------|-------|
| Slug | `034_Why-Plutos-Frozen-Heart-Has-Zero-Craters` |
| Series (LEARNINGS rule 20) | `Real Worlds` |
| Idea pack | `00_Brand/Channel-Setup/ideas/IDEAS_2026-10-16_J0370.md` (scored 25/30, #1 of 5) |
| Topic lock | **DONE (`J2149` Rule-E GO, 4 Nov 2026)** — 12 verified education/space neighbours at 1.03M–21.20M views (`TOPIC_OPPORTUNITY_SCORE.md`); zero OWB/HOS duplicates |
| Script master | **DONE (`J2149` Rule-E GO, 4 Nov 2026; `v03` locked in `J2343`, 7 Nov 2026)** — `01_Script/pluto_frozen_heart_script_master_v03.md` (1,291 spoken words, 1,324 reviewer words, ~8.8 min, 6 chapters; `v00.md`–`v02.md` preserved byte-identical) |
| Script review | **PASS — 95.8 / 100** (1,324 reviewer words, ~8.8 min, 6 chapters, 8/8 structure gates, 0 warnings) |
| Subscribe beat | Line 9 of `templates/SUBSCRIBE_BEAT_LINES.md` (14 words at 42% of spoken words: *"If you'd like more questions like this one, subscribing really helps a small channel."* — not used in `030`–`033`) |
| Sources | **DONE (`J2149`, 4 Nov 2026)** — `01_Script/SOURCES.md` (15/15 rows `VERIFIED` against live NASA Science, NSSDCA, and LOC pages) + `01_Script/CLAUDE_QUOTE_CHECK_v01.md` (15/15 PASS, 0 FLAG) |
| Gate | **PASS — VO / Gemini Veo allowed** (`npm run review:script` + `npm run gate:episode` pasted below) |
| VO | **DONE (`J2352` elected-Chief full VO PASS, 7 Nov 2026, PR #623)** — `02_Voiceover/pluto_frozen_heart_vo_v03.wav` (SHA-256 `2be8030b6c42b673530351014c71bca1a6c31a10af9746539bb2a1ce7dcf7685`, `616.160 s`, `-19.9 LUFS` integrated, `-23.0 dB` mean, `-3.7 dBTP` true peak) + reconciled `02_Voiceover/stt/pluto_frozen_heart_vo_v03/stt_raw.json` |
| Shots | **DONE (`J2368` PASS, 7 Nov 2026)** — `07_Edit-Project/SHOT_LIST_v01.md` + `07_Edit-Project/shot_list_v01.csv` (`74` rows across `646.94 s`, `clip_check.py` **PASS** with 0 errors and 0 warnings; opening `R01–R07` updated in `07_Edit-Project/FIRST30_PLAN.md` `J2668`/`J2754` to 19 cuts `<= 3.93 s`) |
| CG | **DONE (`J2370`/`J2371`/`J2372` PASS, 7 Nov 2026)** — £0 harvest (`07_Edit-Project/HARVEST_POOL_v01.json`) + `07_Edit-Project/graphics_v03/` |
| Edit / Master Review | **Long `v02` + Short 1 `v02` + Short 2 `v02` ASSEMBLED (`J2438` + `J2867`, 17 Nov 2026, all automated gates PASS on all three); ready for 5-part review (`J2868`)** — `09_Final-Export/034_pluto_frozen_heart_master_v02.mp4` (`370,954,641` B, SHA-256 `e5a886dfef208774cce8ae987e658fba5d7a96cbb5c99a44aadf63516949ba62`, `19,408` frames = `646.933 s` at `30` fps, `-14.7 LUFS`, `-1.0 dBTP`, `0` black frames) executes `FIRST30_PLAN.md` (`-2.800 s` Sentence 1 splice ending at `5.900 s < 8.000 s`; Sentence 2 payoff ending at `16.240 s < 20.000 s`; `+2.800 s` restored across `R04–R07` silences so `R08–R74` stay locked at `65.760–646.933 s`; `19` opening cuts `<= 3.933 s` across `R01–R07` / `11` cuts `<= 3.533 s` across `R01–R04`; `138` total cuts) AND all `J2383` §5.1 finishing fixes (all 6 chapter-card silences inserted at `prev_word_raw_end + 0.600 s`, sub-pixel PIL BICUBIC zoom `1.000->1.045` + 2D separable `min(fx, fy)` `48 px` feather, word-boundary `row_assets()` + `off >= 2.0 s` on `ksc_011906_*.mp4`, full `WHO` card names on `R10/R11/R58`, duplicate `Credit:` pills stripped). `10_Shorts/short01_testA_opening/06_Final-Exports/034_short01_testA_opening_v02.mp4` (`53,859,275` B, SHA-256 `c9a02052ff7a33cba10adc52e440cfe793c6cca1f31e355262acf9fd9c4ba677`, `36.500 s` = `1,095` frames at `30/1` CFR, `-14.10 LUFS`, `-2.10 dBTP`) passes all 5/5 gates (`0/37` frames padded). `10_Shorts/short02_water_ice_mountains/06_Final-Exports/034_short02_water_ice_mountains_v02.mp4` (`59,262,118` B, SHA-256 `f3e3d47d0c86be1d297fbf5fade3383126f9c01d94ab2b78444d60dd6a66be73`, `25.800 s` = `774` frames at `30/1` CFR, `-14.10 LUFS`, `-2.00 dBTP`, reusing locked `v01` stems byte-for-byte) passes all 6/6 gates (`0/26` frames padded, `0` edge bars, `0` loop cross-fade). Next: `J2868` runs the 5-part multimodal review. |
| Runtime target | 7–9 min (~1,285 spoken narration words after `-2.80 s` appositive splice, `646.933 s` = `10:46.9` master) |
| Shorts | Paired with standalone Short `gmzaCfJF1gA` (*Why Does Pluto's Giant Ice Heart Have Zero Craters?*) + 2 episode Shorts (`034_short01_testA_opening_v02.mp4` **DONE 5/5 gates PASS**; `034_short02_water_ice_mountains_v02.mp4` **DONE 6/6 gates PASS** in `J2867`) |

## Marker counts (`pluto_frozen_heart_script_master_v02.md`)

- `DATA:` **7** (all ≥ 3 required; includes 1 before `[SUBSCRIBE BEAT]`, 1 build-up timeline, and 7 `SCALE:` comparisons + 7 `NUMBER OBJECT:` labels)
- `SCALE:` **7** (`grep -c "SCALE:"` = 7 = `DATA:` count)
- `WHO:` **3** (every named person in spoken narration at first mention: Clyde Tombaugh 1906–1997, Venetia Burney 1919–2009, Alan Stern born 1957; all verified in LOC Name Authority Records)
- `WHEN:` **6** (Hook: `13 July 2015, 14 July 2015`; Ch 1: `18 February 1930, 14 March 1930`; Ch 2: `June 1978`; Ch 3: `4.5 billion years ago, 1979–1999, 19 January 2006, 2006, 28 February 2007, 14 July 2015, 25 October 2016`; Ch 5: `5 August 2026`; Ch 6: `1 January 2019, 1 October 2024`)
- `FACT:` **4** (all ≤ 4 words: `Named at age eleven`, `Charon never sets`, `Closer than Neptune`, `Water-ice bedrock`)
- `NUMBER OBJECT:` **7** (Hook + Chapters 1–6)
- **First 30 seconds rule (`OWB_2026-10-16.md` & `LEARNINGS` rule 10):** immediate claim and causal answer (`Sputnik Planitia is an active glacier where city-sized cells of solid nitrogen circulate up and down`) in the opening sentences; no negative opener, no multi-question agenda; first `[CHAPTER CARD]` placed after the 3-paragraph cold open (~125 spoken words, ~0:50).
- **Reference-channel packaging (`LEARNINGS` rules 15, 18, 19, 20):** recorded in `11_Upload-Package/metadata_DRAFT_v01.json` and `description_DRAFT_v01.txt` (`Real Worlds` series; Rule-18 variants `What New Horizons Saw Inside Pluto's Frozen Heart` and `The Only Spacecraft Photos Ever Taken of Pluto`; Rule-19 single clean real spacecraft frame `PIA20291` / `PIA19952` with 2-word top-band hook `ZERO CRATERS`).

## Pasted `npm run review:script` output (v02, J2149, 4 Nov 2026)

```text
# pluto_frozen_heart_script_master_v02.md

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

Words: 1324 · Est. min: 8.8 · Chapters: 6

## Cold open excerpt

> Why Pluto's Frozen Heart Has Zero Craters Across Pluto's horizon, in distant orbit around our Sun, what would you see on the bright western half of its icy heart? A frozen nitrogen glacier about one thousand kilometres wide — larger than Texas and Oklahoma combined — with zero cr

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 95.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```

## Pasted `npm run gate:episode` output (v02, J2149, 4 Nov 2026)

```text
# Episode gate — 034_Why-Plutos-Frozen-Heart-Has-Zero-Craters

**Decision:** PASS — VO / Gemini Veo allowed

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /tmp/J2149-wt/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters |
| prebuild_vidiq | OK | Pre-build vidIQ audit present and looks signed off. |
| script_file | OK | Script: 01_Script/pluto_frozen_heart_script_master_v02.md |
| script_review | OK | Script reviewer PASS 95.8/90 (need ≥90). |
| orbit_acts | OK | [ORBIT ACTS] count 2 (need ≥1). |
| subscribe_beat | OK | Subscribe beat at 42% (14 words): "If you'd like more questions like this one, subscribing really helps a small channel." |
| visual_must | OK | [VISUAL MUST] count 7 (need ≥4). |
| teach | OK | [TEACH] count 7 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 6 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **95.8/100** · PASS
```

## Pasted `clip_check.py` output (`shot_list_v01.csv` vs `stt_timeline_offset_v01.json`, `J2367`, 7 Nov 2026)

```text
$ python3 00_Brand/Channel-Setup/tools/clip_check.py 02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/07_Edit-Project/shot_list_v01.csv --words 02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/02_Voiceover/stt/pluto_frozen_heart_vo_v03/stt_timeline_offset_v01.json --vo-end 628.94
clip_check: 74 rows — PASS
OK: sentence/card boundaries and end-after-VO checks clear.
```

## Pasted Long Master `v02`, Short 1 `v02` & Short 2 `v02` Gate Outputs (`J2438` + `J2867`, 17 Nov 2026)

- **Long Master `v02`:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/09_Final-Export/034_pluto_frozen_heart_master_v02.mp4` (`370,954,641` B, SHA-256 `e5a886dfef208774cce8ae987e658fba5d7a96cbb5c99a44aadf63516949ba62`, `1920×1080`, `19,408` frames = `646.933 s`, `-14.7 LUFS`, `-1.0 dBTP`, `black_frames=[]`)

```text
clip_check: 74 rows — PASS
OK: sentence/card boundaries and end-after-VO checks clear.

picture QA PASS: 0 of 138 cuts fail, 10 to look at -> .../full_master_v02_pack/PICTURE_QA.md, .../full_master_v02_pack/picture_qa_review.jpg

polish gate PASS: 0 of 138 rows failed, 9 to look at -> .../full_master_v02_pack/polish_gate_v02.json

music gate PASS: pluto_score_bed_v01.mp3, 646.9 s, about 66.7 BPM, brief Pace: 64-74 BPM

SFX level PASS: VO -19.9 LUFS, SFX -46.8 LUFS, 8 hits
```

- **Short 1 `v02` (Test A Opening):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/034_short01_testA_opening_v02.mp4` (`53,859,275` B, SHA-256 `c9a02052ff7a33cba10adc52e440cfe793c6cca1f31e355262acf9fd9c4ba677`, `1080×1920`, `1,095` frames = `36.500 s` at `30/1` CFR, `-14.10 LUFS`, `-2.10 dBTP`)

```text
PASS  034_short01_testA_opening_v02.mp4  dur=36.5s  audio=-17.1dB  motion=29.06  f0diff=7.29  cut1=2.1s  vo_onset=0.07s  tail_gap=0.48s  dhash=313011b111135110  visor=0.0
   full-bleed whole Short  0/37 frames padded at one a second, 0/73 at two a second  padded stretches: none  end card 35.1-36.5s judged apart
picture QA PASS: 0 of 12 cuts fail, 2 to look at
polish gate PASS: 0 of 12 rows failed, 1 to look at
music gate PASS: pluto_score_bed_v01.mp3, 646.9 s, about 66.7 BPM, brief Pace: 64-74 BPM
SFX level PASS: VO -16.5 LUFS, SFX -40.1 LUFS, 7 hits
```

- **Short 2 `v02` (Keeper Question: Water-Ice Mountains):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short02_water_ice_mountains/06_Final-Exports/034_short02_water_ice_mountains_v02.mp4` (`59,262,118` B, SHA-256 `f3e3d47d0c86be1d297fbf5fade3383126f9c01d94ab2b78444d60dd6a66be73`, `1080×1920`, `774` frames = `25.800 s` at `30/1` CFR, `-14.10 LUFS`, `-2.00 dBTP`, locked `v01` stems reused byte-for-byte: VO `d93c149a704c`, SFX `2b8739fe2fd1`, Bed `dbd43603f37f`)

```text
PASS  034_short02_water_ice_mountains_v02.mp4  dur=25.8s  audio=-16.7dB  motion=25.13  f0diff=4.72  cut1=2.4s  vo_onset=0.06s  tail_gap=0.77s  dhash=2e4f353f3b276936  visor=0.0
   full-bleed whole Short  0/26 frames padded at one a second, 0/52 at two a second  padded stretches: none  no end card named in meta
picture QA PASS: 0 of 10 cuts fail, 1 to look at
polish gate PASS: 0 of 10 rows failed, 1 to look at
music gate PASS: pluto_score_bed_v01.mp3, 646.9 s, about 66.7 BPM, brief Pace: 64-74 BPM
SFX level PASS: VO -19.4 LUFS, SFX -39.3 LUFS, 3 hits
thumb_preview.py short: 034_short02_water_ice_mountains_v02_cover_preview.jpg
```
