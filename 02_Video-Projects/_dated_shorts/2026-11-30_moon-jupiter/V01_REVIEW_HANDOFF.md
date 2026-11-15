# J2916 v01 Review Handoff — 30 November 2026 Moon–Jupiter Close Conjunction Dated-Event Short

- **Job:** `J2916` (`Moon-Jupiter 30 Nov dated-event Short (airs Thu 26 Nov): voice-over, build from free NASA footage, all Shorts gates, park for review`, `kind: assembly`)
- **Approved Plan:** `02_Video-Projects/_dated_shorts/2026-11-30_moon-jupiter-conjunction.md` (`Script PASS` in `jobs/reviews/J2830/REVIEW.md`, `15 Nov 2026`, `64e889aafd`)
- **Target Slot:** **Thursday, 26 November 2026 at 11:30 UTC (London)** (`4` days before `2026-11-30 08:25 UTC` Moon–Jupiter `1.05°` conjunction; Related video `-jmMROGoZCM` *Why You Can't Stand On Jupiter*; requires Ben's OK on the board by **Wednesday, 25 November 2026 at 18:00 London**)
- **Master Export (`studio-live` NAS):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_dated_shorts/2026-11-30_moon-jupiter/06_Final-Exports/owb_dated_2026_11_30_moon_jupiter_v01.mp4` (`1080×1920`, `30.00 fps` CFR, `585` frames = `19.500 s`: `18.480 s` VO + `1.020 s` forward-loop tail)
- **Cover Image (`studio-live` NAS):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_dated_shorts/2026-11-30_moon-jupiter/11_Upload-Package/moon_jupiter_2026_11_30_cover_v01.jpg` (`**2,000X** / FARTHER`)
- **Spend:** `1` ElevenLabs TTS take (`275` chars on subscription credits via `04_Audio/tools/vo_take.py`, logged in `04_Audio/elevenlabs_ledger.jsonl` and `05_Analytics/ai_spend/ledger.jsonl`); **`£0`** image/video/music/SFX spend.
- **Upload / Studio / Buffer Changes:** **None** (not uploaded, not scheduled, parked for review per Step 4).

---

## 1. Voice-Over & Timing (`vo_check.py` PASS + Direct Audio Listening Check)

- **Take 1 (`moon_jupiter_2026_11_30_vo_v01`, `eleven_v3`, Ben Orbit Narrator):** `275` chars, `47/47` words exact.
- **Room-Tone Splice (`moon_jupiter_2026_11_30_vo_v02`, `splice_v02.py`):** Natural speed (`1.00×`, zero `atempo`), tightening only verified room-tone inter-sentence silences (`<-70 dBFS` RMS, `10 ms` qsin joins, `12 ms` end fade after `"sky."`) to **`18.480 s`** (`887,040` samples at `48 kHz`).
  - Total runtime with `1.020 s` forward-loop tail = **`19.500 s`** (`585` frames at `30 fps`), squarely inside the `17.0–20.0 s` Rule 16 Apophis-mould bar (`C7` word trims not needed).
  - Answer start (Line 4: *"Yet Jupiter sits two thousand times farther, over seven hundred million kilometres away."*) = **`10.66 s`** (`<= 13.5 s` C7 guard), with `"2,000"` at `11.80 s` and `"over 700 million kilometers away."` at `13.92–16.44 s`.
  - Complete-sentence ending: *"Look south in the morning sky."* (`16.82–18.44 s`, unclipped `"sky."`, per Ben's `11 Nov` `J2478` v04 rule).
- **`vo_check.py` Output:**
  ```text
  PASS  moon_jupiter_2026_11_30_vo_v02.mp3  0:18.48  mean -23.3 dB  peak -4.3 dB  153 wpm
     warn  replace at ~0:12.42: script 'farther over million kilometres away look south' / heard 'farther over million kilometers away look south' — sounds alike (likely the transcriber); listen
  ```
- **Demonstrated Audio & Moving-Video Perception (`gemini` capability probe verified and recorded via `chief_relay.py capabilities`):**
  - Directly listened to `moon_jupiter_2026_11_30_vo_v02.mp3` and the final mixed audio track (`owb_dated_2026_11_30_moon_jupiter_v01.mp4`) and watched the moving video sequence (`0:00–0:19`): every word is clear, natural-speed British narration with no stumbles, clicks, or clipped consonants (`kilometres` vs US spelling `kilometers` in Whisper is spelling-only), clean speech-ducked score bed (`-14.0 LUFS` mix), and smooth continuous motion across all 9 cuts and the loop seam.

---

## 2. Full-Bleed `9:16` Visual Build & NASA Asset Provenance (`£0`)

- **Candidate Note (`Missing footage fallback` documentation):** Inspected `GSFC_20190808_HST_m13279_Jupiter~orig.mp4` (`1920×1080`) from `images-assets.nasa.gov` and verified via contact sheet that every scene carries burned-in Goddard text banners across top/bottom, and `comp.8001.tif` on SVS #5587 carries Dial-A-Moon annotations. Used the unlabelled 4K SVS #5587 Frame `8001` Moon layer (`moon.8001.tif`, `2026-11-30T08:00 UTC`), unlabelled 4K `phases_2026_plain_2160p30.mp4`, and high-resolution unlabelled NASA JunoCam Jupiter plates (`PIA22946~orig.jpg`, `PIA26077~orig.jpg`, `PIA21974~orig.tif`), plus NASA Blue Marble Earth (`GSFC_20171208_Archive_e002130.jpg`), LRO Moon (`GSFC_20171208_Archive_e001939.jpg`), Apollo 11 Moon (`as11-44-6667.jpg`), and ISS Expedition 70 twilight limb (`iss070e062746.jpg`).
- **9 Cuts (100% Full-Bleed `9:16` `mode: cover`, `0/20` and `0/39` Padded Frames, Max Hold `3.17 s <= 4.0 s`):**
  1. `s01` (`0.000–2.567 s`): Full-bleed Juno Jupiter cloud bands (`PIA22946`) + rotating 4K SVS 5587 Nov 30 Moon; Hook caption `0.00–2.00 s`: `**FORTY TIMES** WIDER`.
  2. `s02` (`2.567–4.200 s`): SVS 5587 Frame `8001` (`30 Nov 2026` waning gibbous Moon sunlit craters) on *"on November thirtieth."*
  3. `s03` (`4.200–5.733 s`): NASA Blue Marble Earth on *"If Earth were a grape,"* (zero badge/overlay).
  4. `s04` (`5.733–7.733 s`): Juno `PIA26077` belts & zones + true `11 : 1` Earth disc on *"Jupiter is a whole basketball."* (zero badge/overlay).
  5. `s05` (`7.733–10.500 s`): Unlabelled `40 : 1` real-body diameter scale (`PIA21974` + LRO Moon) on *"It is forty times wider than our Moon."* Title Banner `Why Is Jupiter Beside the Moon on November 30?` runs `9.10–12.60 s` (inside `9–14 s`, clearing the `DATA` overlay by `0.60 s`).
  6. `s06` (`10.500–13.667 s`): Sharp LRO Moon craters (`GSFC_20171208_Archive_e001939`) on *"Yet Jupiter sits two thousand times farther,"*.
  7. `s07` (`13.667–16.667 s`): Apollo 11 curved sunlit lunar horizon (`as11-44-6667`) with distant Jupiter shining in the starry space sky above the horizon + sole teach overlay (`13.20–16.30 s`, inside `16:9` centre band): animated `DATA` distance bar comparing `MOON: 373,000 KM` with `JUPITER: 754 MILLION KM` and `2,000 TIMES FARTHER`.
  8. `s08` (`16.667–18.500 s`): Pre-dawn twilight limb (`iss070e062746`) with the waning gibbous Nov 30 Moon and Jupiter shining `1.05°` beside it in the starry sky above Earth's horizon on *"Look south in the morning sky."*
  9. `loop` (`18.500–19.500 s`): `1.000 s` forward-loop tail (`7`-frame / `0.23 s` crossfade into `s01` pre-roll).

---

## 3. Automated Gate Verdicts (`gate_exit_codes.json`: All `0`)

- **`gate_shorts_open.py` (`0` — PASS):**
  ```text
  PASS  owb_dated_2026_11_30_moon_jupiter_v01.mp4  dur=19.5s  audio=-16.7dB  motion=10.65  f0diff=3.25  cut1=2.57s  vo_onset=0.05s  tail_gap=1.06s  dhash=bedd9cfc8ec6dfbf  visor=0.0
     full-bleed 0.00s  fills the frame  sharp above/middle/below=0.379/0.558/0.337  detail top/centre/bottom=17.58/6.09/2.95  spread top/bottom=44.32/21.45
     full-bleed whole Short  0/20 frames padded at one a second, 0/39 at two a second  padded stretches: none  no end card named in meta
  ```
  *(Note: `19.5 s` sits inside the approved `17.0–20.0 s` Rule 16 Apophis-mould dated-Short band.)*
- **`picture_qa.py` (`0` — PASS):** `0 of 9 cuts fail, 1 to look at` (`0:07` `moon_jupiter_03_s04` `PIA26077` gas-giant cloud bands `edge density 0.0304 < film p5 0.0348` because the 8 crater/starfield cuts set a high `p5`; inspected full size in `picture_qa_review.jpg`).
- **`polish_gate.py` (`0` — PASS):** `0 of 9 rows failed`.
- **`music_gate.py` (`0` — PASS):** `jupiter_no_crust_short_bed_v01.mp3, 30.0 s, about 66.7 BPM, brief Pace: 60-80 BPM` (reuse covered by `05_Music/music_gate_j2916_chief_waiver.json` per approved `J2830`/`J2916` §5 plan).
- **`sfx_kit.py level` (`0` — PASS):** `SFX level PASS: VO -20.3 LUFS, SFX -45.8 LUFS, 3 hits`.
- **`short_c37.py`:** `frames=585, loop_diff_masked=3.828, open_median_step=3.743, head_matches=[0, 0, 0, 0, 0]`.
- **`thumb_preview.py short` (`0` — PASS):** `qa/cover_thumb_preview.jpg`.

---

## 4. Next Step

1. Chief / Claude reviews `owb_dated_2026_11_30_moon_jupiter_v01.mp4`, `moon_jupiter_2026_11_30_cover_v01.jpg`, and `qa/picture/picture_qa_review.jpg`.
2. On `KEEP`, copy `v01` and its cover to the Orbit UAT watch folder and arm `jobs.py awaits` for Ben's watch (due **Wednesday, 25 November 2026 at 18:00 London** ahead of **Thursday, 26 November 2026 at 11:30 London** publish).
