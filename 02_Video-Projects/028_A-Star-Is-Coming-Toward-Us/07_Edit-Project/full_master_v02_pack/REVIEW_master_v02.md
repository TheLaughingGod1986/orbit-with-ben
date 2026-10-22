# 028 A Star Is Coming Toward Us (Gliese 710) — Full Master v02 Review (`J0864`, 22 Oct 2026)

**Cut:** `028_Gliese710_full_master_v02.mp4` (`472.83 s`, `61` cuts, max single picture `14.66 s`, `-14.1 LUFS` / `-1.3 dBTP`, **£0 spend**)
**SHA-256 (all 3 copies identical):** `cde81a6aedd676f972f6f6547d4ae5fb4ffd874fa6836113c2d2ac967303f0c0`

## 1. Chief's Four £0 Picture Fixes Applied (Before vs After — see `sheet_fixes_v02.jpg` & `per_row_sheet_v02.jpg`)

| Fix | Before (`full_master_v01` / `J0859`) | After (`full_master_v02` / `J0864`) | Verification |
|---|---|---|---|
| **1. `7:48 r38_return` (`463.62–472.84 s`, `gaia_motion_1_6my.mp4`)** | `offset=31.0 s` (`[31.00, 40.22]`) ran into ESA's closing bumper (`29.0–45.48 s`), ending the film on the ESA logo + `"Copyright 2020"`. | Set `r38_return` to `offset=16.0 s` (`[16.00, 25.22]`, `vcrop=(2880, 1620, 480, 270)`, `1.33x` upscale, `fade_out=1.0`), ending at `25.22 s` on continuous moving starfield before the `25.50 s` dip and `29.00 s` ESA end slate. Also shifted `r12_stars_move` (`117.24–126.47 s`) to `offset=14.0 s` (`[14.00, 23.23]`, centered crop `vcrop=(2688, 1512, 576, 324)`, `1.43x`, cropping out the top-left corner bug). | Checked `468.23 s` (mid) and `471.50 s` / `472.50 s` (end frames): 100% moving starfield, no logo (`sheet_fixes_v02.jpg`). |
| **2. `3:57 r22_neowise` & `7:40 r38_neowise_2` (`neowise_dc.tif`)** | `r22_neowise` (`0.46x` wide) left Comet NEOWISE faint in the top corner; `r38_neowise_2` (`0.62x`) cropped below `y=0.22` and missed the comet (`(0.302, 0.217)`). | Re-framed `r22_neowise` (`233.50–241.46 s`) to `box=(0.18, 0.04, 0.50, 0.285)` (`1.27x` upscale, `pct=0.06` push-in, `comet_enhance=True`) and `r38_neowise_2` (`457.47–463.62 s`) to a tighter second crop `box=(0.16, 0.07, 0.42, 0.27)` (`1.56x` upscale, `pct=0.06` push-in, `comet_enhance=True`). | Comet nucleus and upward dust tail read clearly on phone/thumbnail scale (`std=18.8` and `18.5`, `0` low-detail luma warnings, `0` jitter reversals). |
| **3. `5:51 r29_twilight` (`conjunction.tif` under `'About 3 times brighter'`)** | `0.55x` wide crop (`box=(0.05, 0.10, 0.95, 0.70)`) left the Jupiter–Saturn pair at `(0.218, 0.255)` near-invisible, and the pill faded out `0.18 s` before the cut midpoint `351.385 s`. | Cropped tighter on the Jupiter–Saturn pair `box=(0.11, 0.16, 0.34, 0.36)` (`1.71x` upscale, `< 2.0x`, `pct=0.05` push-in, `planet_bloom=True` optical point-spread glow on the `luma > 110` planet cores) and added `tail_hold_s=0.60` so `'About 3 times brighter'` holds at 100% opacity across `351.385 s`. | Pair shines clearly in center-left twilight sky above `'About 3 times brighter'` (`std=20.6`, `p99=255.0`). |
| **4. `4:44 r26_hale_bopp` + `4:50 r26_a3` (comet repeat)** | `r26_hale_bopp` (`281.16–287.48 s`) and `r26_a3` (`287.48–294.00 s`) used `comet_a3.jpg` twice in a row. | Replaced `r26_hale_bopp` (`4:44.3`) with the £0 NASA/JSC Columbia photo of Comet Hale-Bopp (`sts083_hale_bopp.jpg`, `sts083-410-009`, `box=(0.12, 0.08, 0.88, 0.72)`, `0.84x` upscale, `pct=0.05`, credit `NASA/JSC`) and kept `r26_a3` (`4:50.7`) on `comet_a3.jpg` (`box=(0.14, 0.06, 0.74, 0.42)`, `0.57x` upscale, credit `NASA/Matthew Dominick`). | `picture_qa.py` **PASS** (`sts083_hale_bopp.jpg` used 1x, `comet_a3.jpg` used 1x, `neowise_dc.tif` used 2x at `3:57` and `7:40`). |

## 2. Gate Outputs (All PASS)

- **`clip_check.py`:** `clip_check: 61 rows — PASS
OK: sentence/card boundaries and end-after-VO checks clear.`
- **`picture_qa.py`:** `picture QA PASS: 0 of 61 cuts fail, 6 to look at -> /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/full_master_v02_pack/picture_qa_v02/PICTURE_QA.md`
- **`polish_gate.py`:** `polish gate PASS: 0 of 61 rows failed, 3 to look at -> /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/full_master_v02_pack/polish_gate_v02.json`
- **`music_gate.py --video`:** `WARN reused: couldn't read saturn_long_vo_v02_LISTEN.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read jupiter-vo.mp3 to compare (OSError); download it or pass --others
WARN reused: couldn't read jupiter-music.mp3 to compare (OSError); download it or pass --others
WARN reused: couldn't read friday_black_dwarf_short_vo_v01_LISTEN.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v02_LISTEN.m4a to compare (OSError); download it or pass --others
WARN reused: couldn't read monday_saturn_short_vo_v02_how_long.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v03_tightened.m4a to compare (OSError); download it or pass --others
WARN reused: couldn't read monday_saturn_short_vo_v01_LISTEN.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v03b_tightened_LOCK.m4a to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v03b_tightened_LOCK.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v01_LISTEN.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read monday_saturn_short_vo_v02_how_long.mp3 to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v03_tightened.wav to compare (OSError); download it or pass --others
music gate PASS: gliese_score_bed_v01.mp3, 472.8 s, about 70.6 BPM, brief Pace: 64-74 BPM`
- **`sfx_kit.py level`:** `sfx level PASS: VO -14.7 LUFS, SFX -31.6 LUFS (36 hits), 0 fails` (`sfx_level_v02.json`)
- **`npm run gate:episode`:** `PASS — VO / Gemini Veo allowed · Script score: 91/100 · PASS` (`episode_gate_v02.txt`)
