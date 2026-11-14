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
| Edit / Master Review | **`v01` FIX (`J2383` 5-part multimodal review, 14 Nov 2026, `jobs/reviews/J2383/REVIEW.md`)** — `09_Final-Export/034_pluto_frozen_heart_master_v01.mp4` (`J2376`), `034_short01_testA_opening_v01.mp4` (`J2319`), and `034_short02_water_ice_mountains_v01.mp4` (`J2320`) all require `v02` rebuilds before Ben UAT: (1) Long `v02` (`J2438`): apply `FIRST30_PLAN.md` (`-2.800 s` Sentence 1 splice, `+2.800 s` inter-sentence pauses, 19 opening cuts `<= 3.93 s`), insert all 6 chapter-card silences at `prev_word_raw_end + 0.600 s` (`65.760 s, 159.220 s, 261.140 s, 368.220 s, 451.660 s, 534.260 s`) to eliminate pre-onset blips, upgrade `render_still()` to sub-pixel PIL BICUBIC zoom (`1.000->1.045`) with 2D separable edge feather (`min(fx, fy)` over `48 px`, fixing top-left `48×48 px` corner glitch on starfield-framed stills), match asset IDs on word boundaries in `row_assets()` (`R34` `ksc_011906_nh_launchchange -> KSC-06pd0099`), start `ksc_011906_*.mp4` clips at `off >= 2.0 s` (`R34/R36/R40`), and include full names on `R10/R11/R58` `WHO` cards while stripping duplicate `Credit:` callout pills (`R10/R13/R21`); (2) Shorts 1 & 2 `v02`: rebuild both full-bleed `1080×1920` `9:16` (`0%` blur-pad) so `gate_shorts_open.py check` passes (`v01` failed at `57%` and `100%` blur-padded frames). |
| Runtime target | 7–9 min (~1,291 spoken narration words, `646.933 s` = `10:46.9` master) |
| Shorts | Paired with standalone Short `gmzaCfJF1gA` (*Why Does Pluto's Giant Ice Heart Have Zero Craters?*) + 2 episode Shorts (`034_short01_testA_opening_v02.mp4` & `034_short02_water_ice_mountains_v02.mp4`, rebuilding for full-bleed `9:16`) |

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
