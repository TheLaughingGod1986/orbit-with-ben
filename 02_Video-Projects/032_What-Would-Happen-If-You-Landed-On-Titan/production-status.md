# Production status — 032 What Would Happen If You Landed on Titan?

| Field | Value |
|-------|-------|
| Slug | `032_What-Would-Happen-If-You-Landed-On-Titan` |
| Gate | not run (topic not locked; parked for Chief in J0294) |
| Script review | PASS 92.4 / 100 (`titan_landing_script_master_v00.md`, 6 chapters, J0294) |
| VO | locked `titan_landing_vo_v02b` (Chief h31, J1294, 31 Oct 2026). `v02a` is an unlocked failed-spec attempt |
| Picture | PASS (`J2378` / `J2089` £0 picture package on `studio-live` NAS: 39 harvested stills + 4 NASA SVS 20311 1080p MP4s, 62 ProRes 4444 alpha `.mov` exports, 62 moving-plate 1080p30 composite `.mp4` clips + 6 chapter cards, `0` `polish_gate` failures, `0` Short overlap) |
| Runtime target | 7–9 min |
| Shorts | 2 active + 1 reserve (`10_Shorts/SHORTS_PLAN_v01.md`, J2147/J2173, 5 Nov 2026): **Wed 25 Nov 11:30Z** go-public day Short (*Strike a Match on Titan?*, `23.64 s`, or Sat 28 Nov if `AR2` holds 25 Nov) & **Fri 27 Nov 11:30Z** Test A opening (`32.80 s` / `30.00 s`), reserve **Sat 28 Nov / Fri 18 Dec 11:30Z** (*28x Easier to Fly?*, `26.50 s`); standalone Short `RLSJm59OSzI` scheduled Tue 10 Nov 2026 |

## VO lock (Chief h31, J1294, 31 Oct 2026)

Locked stem `02_Voiceover/titan_landing_vo_v02b`. Built from the v02 parts only. ch00 fades out with `afade=t=out:st=50.30:d=0.18:curve=qsin`. ch02 fades out with `afade=t=out:st=107.66:d=0.02:curve=qsin`. No re-take, no ElevenLabs, no new STT.

| Check | Result |
|-------|--------|
| Duration | 582.440 s, 27,957,120 frames, pcm_s16le, 48 kHz stereo |
| Loudness | I −20.0 LUFS, LRA 4.8 LU, true peak −3.4 dBFS |
| ch00 tail | last 10 ms RMS −51.76 dBFS, last sample 0/0 |
| ch02 tail | last 10 ms RMS −62.53 dBFS, last sample 0/0 |
| Null vs v02 | max abs diff 0 outside 50.300–50.480 s and 245.140–245.160 s |
| wav sha256 | `55232eebb76b68639eee0681316a9e90443e36bf42892ba99c9a98735301abc5` (matches Chief sim) |
| mp3 sha256 | `944378a9c7caec4368217a481d35160cfb5621ed4de7dbe4a7787d813a6abff8` (libmp3lame 128k, same settings as v02) |
| Word timings | copied from `stt/titan_landing_vo_v02/` to `stt/titan_landing_vo_v02b/` |

`titan_landing_vo_v02a` stays unlocked. It is the failed 20 ms ch00 spec from J1289 (wav `56482edfe32ab6015033779d319ae3827f94c52ea5b89dcddc6d45127ccf0c35`, mp3 `a457adae2b5b23f20c4348fde76e0ac95332d649f98659307f863ac9b099f4fe`). v01, v02 and v02a were not modified.

## Blockers

- [ ] Chief topic lock + neighbour pass (≥3 education/space videos ≈1M+ views) + Pre-build vidIQ signed
- [x] Script v00 ≥ 90 (`review:script` PASS 92.4/100 on `titan_landing_script_master_v00.md`)
- [ ] Gemini `facts` quote check on `01_Script/SOURCES.md` + `CLAUDE_QUOTE_CHECK_v01.md`
- [ ] Stills locked before Veo/Omni spend

## `npm run review:script` (J0294, 15 Oct 2026)

```
# titan_landing_script_master_v00.md

**Decision:** PASS · **Score:** 92.4 / 100

| Dimension | Score |
|---|---:|
| hook | 9 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.2 |
| escalation | 8.8 |
| retentionPotential | 9 |
| searchPotential | 8.7 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.2 |

Words: 1621 · Est. min: 10.8 · Chapters: 6
Pass threshold: 90
```

## J1753 final verification — 3 November 2026

Codex independently verified the actual v02b WAV/MP3 hashes, timing, loudness, h31 tails, null and copied word timings: technical PASS. Final VO approval remains pending because this session has no audio listening input; no listening is claimed. [Evidence](02_Voiceover/review_J1753/REVIEW.md). Responsible reviewer: the elected Chief with actual Mini listening capability; resume J1753 for listening and a VO-only PASS/FIX. No media correction ordered and no picture approval.

## J1773 sources reconciliation — 3 November 2026

Sources: **PASS retained from Chief J0301**, approved commit `97b7af4ee9`. The governing v01 sources table and script v01 are byte-identical to that approval; v02 only removes the agenda sentence. The older unchecked source blocker above is superseded by this evidence. Claude’s quote recheck is embedded in SOURCES.md; no separate quote-check file is claimed. [Reconciliation](01_Script/J1773_SOURCES_RECONCILIATION.md). J1753 still holds final VO listening review; no picture approval.

## J1810 capability validation — 4 November 2026

Fresh native Gemini audio fixture test failed: the first claimed perception contradicted the fixture, and independent recheck explicitly reported no reliable audio perception. J1753 retains technical PASS at 1/3; no VO was heard or approved. J1810 owns demonstrating a reliable native listening route before any specialist handoff. [Evidence](../../jobs/reviews/J1810/REPORT.md). No Ben production-review action.

## J2378 Chief picture review (`J2089` £0 picture package) — 7 November 2026

Picture: **PASS (`KEEP`)** by elected acting Chief (`gemini`, `J2378` reviewing `J2089` commit `c0bbf33088` and `studio-live` NAS `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/`):
- **Harvest (`03_Reference-Material/harvest_J2089_v01/`):** `39` NASA/ESA/STScI/Commons source stills (`36` active in `SHOT_LIST_v08.md`, all `<= 2` appearances) + `4` NASA SVS `20311` Dragonfly 1080p MP4 clips (`<= 3` stretches separated by `> 10 s`); `inventory_harvest_032.py` `0` errors; `verify_short_sources_032.py` `0` overlap with Short `RLSJm59OSzI`/`ffYKoNVPoqg`.
- **Overlay Exports (`04_Generated-Clips/graphics_exports_v01/`):** `62/62` ProRes 4444 alpha `.mov` exports (`CURRENT_EXPORT_INVENTORY_v31.json`) SHA-256 verified on NAS.
- **Moving-Plate Composites & Chapter Cards (`07_Edit-Project/composites_v01/`):** `62/62` `1920x1080` `30 fps` moving-plate composites (`3.60 s` / `108` frames each) + `6/6` chapter cards (`2.50 s` / `75` frames each) SHA-256 verified on NAS; `COMPOSITES_POLISH_VERIFICATION_v01.json` `0` hard failures; `composites_contact_sheet_v01.jpg` passes Teach on Screen (`DATA`, `WHO`, `WHEN`, `FACT`, `STYLE`, `MOTION`) and per-chapter `NUMBER`+`WORDS` gates.
- **Audio Staged for Edit (`05_Music/` & `06_Sound-Effects/kit_v01/`):** £0 chapter-shaped score bed `titan_score_bed_v01.mp3` (`585.44 s`, `70.6 BPM`, `music_gate.py` PASS, SHA-256 `02c7d95865f8b39de4f9d3dfda8aa85084ecea04fc56dbd6776268279dab8f9e`) and £0 house SFX kit (`rumble_low`, `whoosh_soft`, `tick_ui`) staged on `studio-live` NAS. [Review](../../jobs/reviews/J2378/REVIEW.md).


## J2379 Long Master v01 Assembly & 5-Gate Technical Verification — 7 November 2026

Assembled `09_Final-Export/032_what_would_happen_if_you_landed_on_titan_master_v01.mp4` (`585.440 s`, `17,563` frames at `30/1` fps CFR, `1920x1080`, `yuv420p`, `208,717,641` bytes, `sha256: 452ea3d7b5b2e7a02141072a3634163ce9f86e844f0d3e2637a64511c664d7a0`, `£0` spend) on `studio-live` NAS via `07_Edit-Project/_assemble_032_full_master_v01.py`. All 5 required gates print PASS:
1. `clip_check.py`: `clip_check: 52 rows — PASS (OK: sentence/card boundaries and end-after-VO checks clear.)`
2. `picture_qa.py`: `picture QA PASS: 0 of 127 cuts fail, 7 to look at -> 07_Edit-Project/full_master_v01_pack/PICTURE_QA.md`
3. `music_gate.py`: `music gate PASS: titan_score_bed_v01.mp3, 585.4 s, about 70.6 BPM, brief Pace: 68-78 BPM`
4. `sfx_kit.py level`: `SFX level PASS: VO -20.0 LUFS, SFX -46.2 LUFS, 13 hits`
5. Delivery: Integrated loudness `-14.5 LUFS`, true peak `-1.0 dBTP`, `1920x1080` `30/1` fps CFR, `0` black frames.

Ready for Chief / Claude review (`07_Edit-Project/full_master_v01_pack/ASSEMBLY_REPORT_v01.md`).

## J2436 Long Master v02 Assembly (First-30s Re-Cut `FIRST30_PLAN.md` / `J2435`) & 5-Gate Technical Verification — 9 November 2026

Assembled `09_Final-Export/032_what_would_happen_if_you_landed_on_titan_master_v02.mp4` (`585.440 s`, `17,563` frames at `30/1` fps CFR, `1920x1080`, `yuv420p`, `389,705,443` bytes, `sha256: 519869728d51b42b98435bc971361994d61780c02e2daa3bc0d23f27c80ed073`, `£0` spend) on `studio-live` NAS (`07_Edit-Project/_assemble_032_full_master_v02.py`) and mirrored to NAS `OWB UAT` (`/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/032_what_would_happen_if_you_landed_on_titan_master_v02.mp4`) and iCloud `OWB UAT` (`/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/032_what_would_happen_if_you_landed_on_titan_master_v02.mp4`):
- **First-30s Hook Re-Cut (`07_Edit-Project/FIRST30_PLAN.md`):** Upgraded `render_still_cut()` to symmetric sub-pixel `PIL.Image.Transform.EXTENT(..., Image.Resampling.BICUBIC)` zoom (`1.000 -> 1.045`) so Frame 0 (`PIA20016.jpg`) moves continuously from frame 0 (`polish_gate.py` `0` frozen pairs across all `131` cuts); re-cut `R03` (`9.73–22.93 s`) into 4 cuts `<= 3.60 s` (`3.40 s` `PIA22766`, `3.40 s` `PIA21902`, `3.60 s` `r03_pressure` at `16.53–20.13 s` before `0:20`, `2.80 s` `PIA21890` `u1`), `R04` (`22.93–32.17 s`) into 3 cuts `<= 3.60 s` (`2.83 s` `PIA08167` `u2`, `2.80 s` `PIA21890` `u2`, `3.60 s` `r04_cold`), `R05` (`32.17–45.10 s`) into 4 cuts `<= 3.60 s` (`3.50 s` `PIA07231`, `3.60 s` `r05_rain_preview`, `2.90 s` `PIA12621`, `2.93 s` `NASA_Dragonfly_BannerFactSheet_2024`), and `R06` (`45.10–50.87 s`) into 2 cuts `<= 3.60 s` (`2.90 s` `PIA14922`, `2.87 s` `PIA17177`).
- **All 5 Required Gates Print PASS:**
  1. `clip_check.py`: `clip_check: 52 rows — PASS (OK: sentence/card boundaries and end-after-VO checks clear.)`
  2. `picture_qa.py`: `picture QA PASS: 0 of 131 cuts fail, 7 to look at -> 07_Edit-Project/full_master_v02_pack/PICTURE_QA.md`
  3. `polish_gate.py`: `polish gate PASS: 0 of 131 rows failed, 7 to look at -> 07_Edit-Project/full_master_v02_pack/polish_gate_v02.json`
  4. `music_gate.py`: `music gate PASS: titan_score_bed_v01.mp3, 585.4 s, about 70.6 BPM, brief Pace: 68-78 BPM`
  5. `sfx_kit.py level`: `SFX level PASS: VO -20.0 LUFS, SFX -46.2 LUFS, 13 hits`
  6. Delivery: Integrated loudness `-14.5 LUFS`, true peak `-1.0 dBTP`, `1920x1080` `30/1` fps CFR, `0` black frames.

Ready for Chief / Claude review (`07_Edit-Project/full_master_v02_pack/ASSEMBLY_REPORT_v02.md`).

## J2477 Chief Long Master v02 Review & Ben UAT Staging — 14 November 2026

Edit: **PASS (`KEEP`)** by elected acting Chief (`gemini`, `J2477` reviewing `J2436` `09_Final-Export/032_what_would_happen_if_you_landed_on_titan_master_v02.mp4`, SHA-256 `519869728d51b42b98435bc971361994d61780c02e2daa3bc0d23f27c80ed073`, `389,705,443` bytes, `585.440 s`, `1920x1080` `30/1` fps CFR, `-14.5 LUFS` / `-1.0 dBTP`, `0` black frames):
- **Five-Part Multimodal Inspection (`J2829` Standard):** Full audio listen (`audio_input` across `0:00–9:45.44`), compact `360p` video proxy playback (`moving_video_input` on `0:00–0:45` and `9:30–9:45.44`), `1,171` full-film `2 fps` contact frames, `910` `±3` cut-boundary frames across all `130` internal cuts, and `90` consecutive tail frames (`f17473`–`f17562`) all PASS cleanly.
- **First-30s Rule (`FIRST30_PLAN.md`):** Frame 0 moves continuously (`PIA20016.jpg` zoom `1.000 -> 1.045`), no Orbit/title/logo/fade before `0:30` (first Orbit at `40.40 s`), Sentence 1 ends at `5.24 s <= 8.00 s`, zero agenda lines, concrete numerical/visual card (`r03_pressure`, `1 BAR vs 1.47 BAR`) at `16.53–20.13 s` before `0:20`, all 10 cuts in `0:00–0:32.17` are `2.80–3.67 s <= 4.00 s`, and Chapter 1 (`R07`) enters at `50.87 s >= 45.00 s`.
- **UAT Staging & WIP Advancement:** Verified identical SHA-256 across `09_Final-Export`, NAS `OWB UAT`, and iCloud `OWB UAT`; rendered and uploaded `720p` `_PHONE.mp4` proxy to R2 (`owb-032-v02`); armed `jobs.py awaits` on `J2477` (target Sun 16 Nov 18:00; airs Wed 25 Nov 18:00 London); advanced `jobs/WIP.json` (`OWB:032` out of `active`, `OWB:062` promoted into `active`). [Review](../../jobs/reviews/J2477/REVIEW.md).

## J2884 Chief Upload Package Resolution & Pre-Upload Dry-Run — 15 November 2026

Upload Package (`11_Upload-Package/`): **PASS (`KEEP`)** by elected acting Chief (`gemini`, resolving `J2884` pre-upload package blocker after Ben OK'd `032` Long Master `v02` and thumbnails A/B on `14 Nov 22:46Z`):
- **Release Package Built (`PACKAGE_MANIFEST.json`):** Promoted `metadata_DRAFT_v01.json` to `ready_for_upload` and wrote `PACKAGE_MANIFEST.json` targeting `032_what_would_happen_if_you_landed_on_titan_master_v02.mp4` (`sha256: 519869728d51b42b98435bc971361994d61780c02e2daa3bc0d23f27c80ed073`, `585.440 s`), `schedule: 2026-11-25T18:00:00.000Z` (`Wed 25 Nov 2026 18:00 London`), `privacy: private`, `madeForKids: false`, `syntheticDisclosure: true`, `defaultLanguage: en-GB`, `defaultAudioLanguage: en-GB`, `captionsLanguage: en-GB`, Rule-26 search-first title `What Would Happen If You Landed on Titan? (Seas of Liquid Gas)` (`62` chars), and Ben-approved thumbnails A (`032_j2417_A_water_deep_below_v01.jpg`, `sha256: e8c86bd181fb7196ab62bf95ec19b9ce6f1096f27e06ac13fd2ff97d640eb534`) and B (`032_j2417_B_72_minutes_v01.jpg`, `sha256: 68d8d57187bee9284c0b276f817cf90256bece8e62c829f5ea6d3ddb18b55390`).
- **Chapters, Description, Credits, Captions, Pinned Comment, Tags & Trailer:**
  - `Chapters/titan_landing_chapters_v02.txt` & `Descriptions/titan_landing_long_description_v01.txt`: exact `cuts_v02.json` chapter timestamps (`0:00 Beneath the Orange Sky`, `0:50 The Moon With a Sky`, `2:17 Where Water Is Rock`, `4:05 Rain in Slow Motion`, `5:24 The Seas of Kraken Mare`, `6:29 Why a Match Won't Burn`, `7:54 The World Where You Could Fly`), 5-source `Sources:` block, complete verified `Image credits:` across all 36 agency/Commons sources in `cuts_v02.json` (`HARVEST_POOL_v01.json` + `_assemble_032_full_master_v02.py`), and honest making-of line (`Pictures: ... Facts: ...`).
  - `Captions/titan_landing_long_v02_en-GB.srt`: `211` `en-GB` cues (`<= 42` chars/line, `0` overlaps, ending at `582.384 s <= 585.440 s`) built from `02_Voiceover/stt/titan_landing_vo_v02b/words.srt`.
  - `Pinned-Comments/titan_landing_pinned_v01.txt`, `Tags/titan_landing_long_tags_v01.txt`, `Titles/titan_landing_titles_v01.txt`.
  - `Trailer/titan_landing_trailer_v01.mp4` (`608x1080`, `25/1` fps CFR, `45.120 s`, `1,128` frames, `6,608,542` bytes, `sha256: 8039f1651c48ebb4af3d78c95c9d6f01cc9d7e4f265f9781ac2d5b94986ff073`) rendered on `studio-live` NAS from `master_v02.mp4` cold open.
- **Gates (`PASS`):**
  - `npm run gate:episode`: `Decision: PASS — VO / Gemini Veo allowed` (`Script score: 92.5/100 · PASS`, all 10 checks `OK`).
  - `npm run youtube:package -- --dry-run`: `"ok": true, "dryRun": true, "scheduledFor": "2026-11-25T18:00:00.000Z"`.
