# J1356 — Rule H Review & Final-Watch Handoff for AR Cohort (`AR1 v06`, `AR2 v12`, `AR3 v13`)

- **Date:** 5 November 2026 (`2026-11-05T15:58Z`)
- **Reviewer / Worker:** `gemini` (`gemini-argon`, review lane under `AGENTS.md` Rule H; demonstrated `audio_input,moving_video_input` recorded via `chief_relay.py capabilities`)
- **Target Job:** `J1356` (`AR cohort: verify finished cuts and prepare final-watch handoff`, `after: J1471`, `taskKeys: ["OWB:030"]`)
- **Spend:** £0.00 (no mint, credit spend, media rewrite, upload, schedule, retitle, privacy change, or Buffer post)
- **Verdict:** **KEEP** — all three repaired final masters (`owb_ar1_2024_yr4_moon_v06.mp4`, `owb_ar2_iss_2030_deorbit_v12.mp4`, `owb_ar3_2027_eclipse_v13.mp4`) and preserved original picture masters (`AR1 v01`, `AR2 v06`, `AR3 v05`) verified on disk/NAS/iCloud UAT; full moving video and mixed audio streams directly watched and listened to; all complete-metadata gates (`picture_qa.py`, `polish_gate.py`, `gate_shorts_open.py`, `music_gate.py`, `sfx_kit.py level`, `short_c37.finish_scan`, `ffmpeg` decode, AAC packet preservation) and `h37`/`h40`/`h42`/`J1849` locks pass; durable watch copies staged in `OWB UAT` with verified R2 Play links (`owb-j1356-1-v06`, `owb-j1356-2-v12`, `owb-j1356-3-v13`); and `jobs.py awaits` (`J1356.1`, `J1356.2`, `J1356.3`, due `2026-11-20 18:00` London) set for Ben's final watch.

---

## 1. Cohort Lineage & SHA-256 Verification (`J1321` → `J1355` → `J1468` → `J1471`/`J2016` → `J1918`)

All original picture masters (`AR1 v01`, `AR2 v06`, `AR3 v05`), audio-repaired intermediates (`AR1 v02`, `AR2 v07`, `AR3 v06`), opening-repaired intermediates (`AR1 v04`, `AR2 v11`, `AR3 v08`), and final complete-metadata masters (`AR1 v06`, `AR2 v12`, `AR3 v13`) are preserved and verified by SHA-256. The superseded `PR #363/#365/#369` (`AR2 v10 / AR3 v09`) branch remains excluded.

| Cut | Role | Verified Locations | SHA-256 | Bytes |
|---|---|---|---|---:|
| **AR1 v06** | Final watch master (`J2016`) | `06_Final-Exports/owb_ar1_2024_yr4_moon_v06.mp4` · `OWB UAT/owb_ar1_2024_yr4_moon_v06/owb_ar1_2024_yr4_moon_v06.mp4` · `/Volumes/data/mac-mini-archive/2026-11-05/desk-cache/J2016/ar1_v06/owb_ar1_2024_yr4_moon_v06.mp4` | `3e6803ba5630351515333dc51a406d2d7921dcba434bd6e65760e979e9694fd0` | `36,136,834` |
| **AR1 v06 PHONE** | Durable R2/UAT watch proxy (`owb-j1356-1-v06`) | `OWB UAT/owb_ar1_2024_yr4_moon_v06/owb_ar1_2024_yr4_moon_v06_PHONE.mp4` | `b5c0d46c98fdbca3830a9dbc500f96337a0af170a5e148424adce1ebdb81ae2e` | `10,536,093` |
| **AR2 v12** | Final watch master (`J2016`) | `06_Final-Exports/owb_ar2_iss_2030_deorbit_v12.mp4` · `OWB UAT/owb_ar2_iss_2030_deorbit_v12/owb_ar2_iss_2030_deorbit_v12.mp4` · `/Volumes/data/mac-mini-archive/2026-11-05/desk-cache/J2016/ar2_v12/owb_ar2_iss_2030_deorbit_v12.mp4` | `6b0aacb1529618fb1c4835f3dbd96a372303acecdd4943fd0bb3721194ecb4e7` | `50,673,454` |
| **AR2 v12 PHONE** | Durable R2/UAT watch proxy (`owb-j1356-2-v12`) | `OWB UAT/owb_ar2_iss_2030_deorbit_v12/owb_ar2_iss_2030_deorbit_v12_PHONE.mp4` | `dfb601dcf72198e2c18e2f545de52a45b960878a0376fc18aeae7b1b81cc3913` | `8,004,503` |
| **AR3 v13** | Final watch master (`J2016`) | `06_Final-Exports/owb_ar3_2027_eclipse_v13.mp4` · `OWB UAT/owb_ar3_2027_eclipse_v13/owb_ar3_2027_eclipse_v13.mp4` · `/Volumes/data/mac-mini-archive/2026-11-05/desk-cache/J2016/ar3_v13/owb_ar3_2027_eclipse_v13.mp4` | `3fce60c525eba31f3f014be9bd1c652ed37ad9fb2729ff38b776fbe826643a25` | `275,635,222` |
| **AR3 v13 PHONE** | Durable R2/UAT watch proxy (`owb-j1356-3-v13`) | `OWB UAT/owb_ar3_2027_eclipse_v13/owb_ar3_2027_eclipse_v13_PHONE.mp4` | `092dd71d5efb01671bcdb1fd3664bc89e2b61e509b225e2dfb6d9a8e85f5695a` | `7,904,880` |
| Preserved `AR1 v01` | `J1321`/`J1355` picture master | `.../07_Edit-Project/assembly_j1308_v01/ar1/owb_apophis_ar1_v01.mp4` | `49b3e4f0f7276885f942d3451978eba33c9a2fec68216fcafdd79466f877cd07` | Preserved |
| Preserved `AR2 v06` | `J1321`/`J1355` picture master | `.../07_Edit-Project/assembly_j1321_delivery_v02/ar2/owb_apophis_ar2_v06.mp4` | `6d517aad6c61a0f12d67b4f2f7990f94ea165e17e01055b56873e89415bf8e67` | Preserved |
| Preserved `AR3 v05` | `J1345`/`J1355` picture master | `.../07_Edit-Project/assembly_j1345_v05/ar3/owb_apophis_ar3_v05.mp4` | `3a2fc5b53e2cfafe4d55422f4f8ae7894ffdb81a727bf47f605e01070a58f13d` | Preserved |

---

## 2. Direct Full-Cut Moving Video & Mixed Audio Review (`read_file` on `video/mp4` and `audio/mpeg`)

All three full moving cuts (`owb_ar1_2024_yr4_moon_v06_watch_360p.mp4`, `owb_ar2_iss_2030_deorbit_v12_watch_360p.mp4`, `owb_ar3_2027_eclipse_v13_watch_360p.mp4`) and their full mixed audio streams (`*_mixed_audio.mp3`, identical AAC packet hashes to `J1468`) were directly watched and listened to in this session:

1. **`AR1 v06` (*Will Asteroid 2024 YR4 Hit the Moon in 2032?* · `19.37 s`, `581` frames @ 30fps):**
   - **Audio & Pace:** Locked `apophis_ar1_vo_v03` (`de70ed06...`) plays cleanly over the full-runtime score bed (`owb-standalone-shorts_score_bed_v01.mp3`) and house SFX (`rumble_low`, `whoosh_soft`, `tick_ink`) through the full `19.37 s` runtime including the `1.00 s` music-covered loop tail (`18.37–19.37 s`). Spoken words match `h40` word-for-word: *"Asteroid 2024 YR4 will skim past the Moon on December twenty-second, 2032. Early tracking gave a four percent chance of lunar impact. It will miss, passing twenty-one thousand two hundred kilometres up. Look up knowing…"* The `~120 BPM` arpeggiated bed sits well under the narration (`-14.5 LUFS`, `-1.9 dBTP`, SFX `-37.9 LUFS` vs VO `-21.2 LUFS`) and supports the brisk 19-second standalone test pace without crowding Ben's voice.
   - **Moving Picture & Overlays:** Opens at `0.00–2.40 s` on the moving 3D `2024 YR4` asteroid tumbling across the translating Apollo 11 Moon plate (`as11-44-6667.jpg`, `3 px/frame` smooth motion, `frame0_diff_0_1_5s = 4.95`) with top hook `HIT THE / MOON?` (`MOON?` in yellow) and bottom caption `ASTEROID 2024 YR4`. Cuts at `2.40 s` to `e001939` with date card `22 DEC 2032`, then full Moon limb at `5.20 s`, then `e000868` at `8.00 s` with `h37 C1` card `4.3% (JUNE 2025) → 0% (WEBB, FEB 2026)`, then animated `21,200 KM` trajectory arc at `12.00 s`, title banner `Will Asteroid 2024 YR4 Hit the Moon in 2032?` at `16.80–18.30 s` (`h42` end-window exception), and caption-free `18.37–19.37 s` loop tail matching frame 0.

2. **`AR2 v12` (*Where Will the International Space Station Crash?* · `19.40 s`, `582` frames @ 30fps):**
   - **Audio & Pace:** Locked `apophis_ar2_vo_v01` (`d0d0e4c4...`) plays cleanly with full-runtime score bed and house SFX through `19.40 s` (`18.40–19.40 s` music-covered loop tail; `-14.5 LUFS`, `-1.9 dBTP`, SFX `-38.1 LUFS` vs VO `-19.7 LUFS`). Spoken words match `h40` word-for-word: *"NASA plans to crash the Space Station into the ocean around 2031. It spans a hundred and nine metres, like a football field. Most hardware vaporises. A deorbit craft steers the rest into the empty South Pacific. Look up and watch it cross the sky, because…"*
   - **Moving Picture & Overlays:** Opens at `0.00–2.40 s` on the `J1849`-approved NASA IGOAL 3D ISS model orbiting over rotating Blue Marble Earth (`frame0_diff_0_1_5s = 7.54`) with top hook `OCEAN CRASH / ~2031` (`~2031` in yellow). Cuts at `2.40 s` to smooth Blue Marble ocean pan (`0.15 px/frame`) with sequential cards `RETIRES 2030` → `DEORBIT BURN ~2031` → `DECISION 2027`, then at `5.10 s` to the `109 M (FOOTBALL FIELD)` station scale diagram, then at `8.40 s` to orbital ocean pass with title banner `Where Will the Space Station Crash?` (`9.20–10.90 s`), then at `10.90 s` to the South Pacific / Point Nemo target map (`EMPTY SOUTH PACIFIC`) over `Gerst_Earth_timelapses_2017.webm`, then at `15.00 s` to real NASA Crew-2 ISS fly-around (`jsc2021m000259`), and at `18.40–19.40 s` to the `J1849` preroll loop tail matching frame 0.

3. **`AR3 v13` (*Where Will the 2027 Total Solar Eclipse Last Over Six Minutes?* · `18.07 s`, `542` frames @ 30fps):**
   - **Audio & Pace:** Locked `apophis_ar3_vo_v03` (`95ab6cf1...`) plays cleanly with full-runtime score bed and house SFX through `18.07 s` (`17.06–18.07 s` music-covered loop tail; `-14.1 LUFS`, `-2.1 dBTP`, SFX `-37.9 LUFS` vs VO `-20.9 LUFS`). Spoken words match `h40` word-for-word: *"The 2027 solar eclipse turns midday into night for over six minutes. Totality crosses Spain and North Africa, peaking over Egypt at six minutes twenty-three seconds. Millions can look up as…"*
   - **Moving Picture & Overlays:** Opens at `0.00–2.40 s` on NOAA satellite umbral shadow sweep (`NOAA_sat_eclipse_2024_notext.webm`, `frame0_diff_0_1_5s = 3.05`) with top hook `SIX MINUTES / OF NIGHT` (`MINUTES` in yellow). Cuts at `2.40 s` to smooth Blue Marble East (`0.15 px/frame`) with `h37 C2` sequential cards `2 AUG 2027` → `258 KM PATH` → `LONGEST: 6M23S, EGYPT` (no "LUXOR" on screen), then at `6.90 s` to the code-drawn 2027 path map over `Gerst_Earth_timelapses_2017.webm` stepping `SPAIN` → `ALGERIA` → `TUNISIA` → `LIBYA` → `EGYPT`, then at `11.40 s` to the animated `DATA` comparison bars (`2026 ECLIPSE: 2M 18S` vs `2027 EGYPT: 6M 23S`), then at `14.50 s` to the unobscured 2017 total solar eclipse corona (`NHQ201708210100`, `1 px/frame` smooth pan) with title banner `Where Will the 2027 Eclipse Last Over Six Minutes?` (`14.70–16.90 s`, `h42` exception), and at `17.07–18.07 s` to the caption-free NOAA loop tail (`loop_diff_masked = 1.398`, `open_median_step = 0.726`).

---

## 3. Complete-Metadata Tool-Gate & Packaging Summary

| Check | `AR1 v06` | `AR2 v12` | `AR3 v13` | Status |
|---|---|---|---|---|
| `picture_qa.py` (complete metadata) | 7 cuts, **0 fail**, 1 accepted WARN (`0:10` `e000868` Moon low detail `0.0987`) | 7 cuts, **0 fail**, 3 accepted WARNs (`0:01` & `0:19` `J1849` ISS illustration; `0:17` Crew-2 low detail `0.0382`) | 7 cuts, **0 fail**, 1 accepted WARN (`0:16` `NHQ201708210100` corona low detail `0.0265`) | **PASS** |
| `polish_gate.py` (complete metadata) | **0 of 7 rows failed** | **0 of 7 rows failed** | **0 of 7 rows failed** | **PASS** |
| `gate_shorts_open.py` | **PASS** (`fails: []`, `stayed_fails: []`, `first_cut_s: 2.4`, `frame0_diff_0_1_5s: 4.95`, `motion_0_1s: 16.34`, `19.37 s` `h40` test WARN) | **PASS** (`fails: []`, `stayed_fails: []`, `first_cut_s: 2.4`, `frame0_diff_0_1_5s: 7.54`, `motion_0_1s: 31.06`, `19.40 s` `h40` test WARN) | **PASS** (`fails: []`, `stayed_fails: []`, `first_cut_s: 2.4`, `frame0_diff_0_1_5s: 3.05`, `motion_0_1s: 12.60`, `18.07 s` `h40` test WARN) | **PASS** |
| `music_gate.py` | **PASS** (`J1468` Chief test-bed reuse waiver; `~120 BPM` pace WARN retained and verified by ear) | **PASS** (same waiver + ear-verified pace WARN) | **PASS** (same waiver + ear-verified pace WARN) | **PASS** |
| `sfx_kit.py level` | **PASS** (`VO -21.2 LUFS, SFX -37.9 LUFS, 4 hits`) | **PASS** (`VO -19.7 LUFS, SFX -38.1 LUFS, 4 hits`) | **PASS** (`VO -20.9 LUFS, SFX -37.9 LUFS, 4 hits`) | **PASS** |
| `short_c37.finish_scan` (`loop.json`) | **PASS** (`loop_diff_masked: 8.134 <= open_median_step: 8.255`, `head_matches: [0,0,0,0,0]`) | **PASS** (`loop_diff_masked: 12.266 <= open_median_step: 12.414`, `head_matches: [0,0,0,0,0]`) | **PASS** (`loop_diff_masked: 1.398 < 2.0`, `open_median_step: 0.726`, `head_matches: [0,0,0,0,0]`) | **PASS** |
| `ffmpeg` decode & AAC preservation | Exit `0`, empty `stderr`; AAC packet hash `d0b91b47...` identical to `J1468` | Exit `0`, empty `stderr`; AAC packet hash `ab28bf5e...` identical to `J1468` | Exit `0`, empty `stderr`; AAC packet hash `4ddf24de...` identical to `J1468`; 354 unaffected YUV frames bit-identical to `v08` | **PASS** |
| Versioned pre-upload manifests | `jobs/reviews/J1356/PACKAGE_MANIFEST_ar1_v06.json` (original `11_Upload-Package` preserved) | `jobs/reviews/J1356/PACKAGE_MANIFEST_ar2_v12.json` (with `J1849` NASA IGOAL/Earth illustration credit; original preserved) | `jobs/reviews/J1356/PACKAGE_MANIFEST_ar3_v13.json` (original `11_Upload-Package` preserved) | **PASS** |

---

## 4. Final-Watch Handoff (`awaits_ben` & R2 Play Links)

All three durable watch copies and `_PHONE.mp4` proxies are staged in `~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/`, registered in `05_Analytics/kanban/watch_uploads.json` and `~/.config/studio-kanban/watch_uploads.json`, and verified over HTTPS (`206 Partial Content` from Cloudflare R2 via `/api/watch`):

| Ask ID | Short | Version | Watch ID | iCloud UAT Path (`file`) | Watch-By (`due`, London) |
|---|---|---|---|---|---|
| `J1356.1` | `AR1` — *Will Asteroid 2024 YR4 Hit the Moon in 2032?* | `v06` | `owb-j1356-1-v06` | `OWB UAT/owb_ar1_2024_yr4_moon_v06/owb_ar1_2024_yr4_moon_v06_PHONE.mp4` | `2026-11-20 18:00` (`2026-11-20T18:00Z`) |
| `J1356.2` | `AR2` — *Where Will the International Space Station Crash?* | `v12` | `owb-j1356-2-v12` | `OWB UAT/owb_ar2_iss_2030_deorbit_v12/owb_ar2_iss_2030_deorbit_v12_PHONE.mp4` | `2026-11-20 18:00` (`2026-11-20T18:00Z`) |
| `J1356.3` | `AR3` — *Where Will the 2027 Total Solar Eclipse Last Over Six Minutes?* | `v13` | `owb-j1356-3-v13` | `OWB UAT/owb_ar3_2027_eclipse_v13/owb_ar3_2027_eclipse_v13_PHONE.mp4` | `2026-11-20 18:00` (`2026-11-20T18:00Z`) |

No upload, schedule, retitle, privacy change, or Buffer action is performed; publishing waits for Ben's watch OK and Chief scheduling.
