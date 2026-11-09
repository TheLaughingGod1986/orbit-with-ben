# 032 Titan Long Master v02 — First-30s Re-Cut Assembly & Gate Report (`J2436` / `J2435`)

- **Film:** `032_What-Would-Happen-If-You-Landed-On-Titan` (*What Would Happen If You Landed on Titan?*)
- **Assembled Master (`studio-live` NAS):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/09_Final-Export/032_what_would_happen_if_you_landed_on_titan_master_v02.mp4`
- **Mirrored to NAS `OWB UAT`:** `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/032_what_would_happen_if_you_landed_on_titan_master_v02.mp4`
- **Mirrored to iCloud `OWB UAT`:** `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/032_what_would_happen_if_you_landed_on_titan_master_v02.mp4`
- **Master SHA-256 (verified across all 3 paths):** `519869728d51b42b98435bc971361994d61780c02e2daa3bc0d23f27c80ed073`
- **Size:** `389,705,443` bytes (`371.7 MB`)
- **Format:** `1920x1080`, `30/1` fps CFR (`17,563` frames, `585.440 s`), `yuv420p` H.264 + `48 kHz` stereo AAC (`192 kbps`), `+faststart`
- **Assembler Script:** `07_Edit-Project/_assemble_032_full_master_v02.py` (mirrored to `07_Edit-Project/_assemble_032_full_master_v01.py`)
- **Row Timing Sidecar:** `07_Edit-Project/shot_list_v08.csv` (`52` rows, `131` cuts)
- **Cut Manifest Sidecar:** `07_Edit-Project/full_master_v02_pack/cuts_v02.json`
- **Spend:** `£0`

## First-30s Re-Cut Changes Executed (`FIRST30_PLAN.md` / `J2435` / `J2428`)

1. **Frame 0 Continuous Motion (`render_still_cut`):** Upgraded `render_still_cut()` from static `-loop 1` PNG encoding to symmetric sub-pixel `PIL.Image.Transform.EXTENT(..., Image.Resampling.BICUBIC)` zoom (`z = 1.000 -> 1.045`) across every still cut so Frame 0 (`PIA20016.jpg`, Cassini natural-colour view of orange Titan in front of Saturn's rings) is visibly moving from frame 0 (`polish_gate.py` `0` frozen pairs across all `131` cuts).
2. **All Opening Cuts `<= 3.60 s` (`R01–R06`, `0.00–50.87 s`) & Payoff Before `0:20`:**
   - `R01` (`0.00–6.20 s`): `3.10 s` `PIA20016.jpg` (`u1`) + `3.10 s` `PIA08167.jpg` (`u1`). First sentence ends at `5.24 s < 8.00 s`.
   - `R02` (`6.20–9.73 s`): `3.53 s` `code_graphic_032_r02_survive_check_v01.mp4` (`NO EXPLOSION · BLOOD DOES NOT BOIL`).
   - `R03` (`9.73–22.93 s`, 4 cuts `<= 3.60 s`): `3.40 s` `PIA22766.jpg` (`9.73–13.13 s`), `3.40 s` `PIA21902.tif` (`13.13–16.53 s`), **`3.60 s` `code_graphic_032_r03_pressure_v01.mp4` (`16.53–20.13 s`, concrete `1.47 BAR · 1.5× EARTH'S AIR` payoff on screen `3.47 s` before `0:20`)**, `2.80 s` `PIA21890.jpg` (`20.13–22.93 s`, `u1`).
   - `R04` (`22.93–32.17 s`, 3 cuts `<= 3.60 s`): `2.83 s` `PIA08167.jpg` (`22.93–25.77 s`, `u2`), `2.80 s` `PIA21890.jpg` (`25.77–28.57 s`, `u2`), `3.60 s` `code_graphic_032_r04_cold_v01.mp4` (`28.57–32.17 s`, `-179 °C · NO OXYGEN TO BREATHE`).
   - `R05` (`32.17–45.10 s`, 4 cuts `<= 3.60 s`): `3.50 s` `PIA07231.jpg` (`u1`), `3.60 s` `code_graphic_032_r05_rain_preview_v01.mp4`, `2.90 s` `PIA12621.jpg` (`u1`), `2.93 s` `NASA_Dragonfly_BannerFactSheet_2024.jpg` (`u1`).
   - `R06` (`45.10–50.87 s`, 2 cuts `<= 3.60 s`): `2.90 s` `PIA14922.jpg` (`u1`) + `2.87 s` `PIA17177.jpg` (`u1`). Chapter 1 (`R07`, *1655 · Christiaan Huygens*) starts at `50.87 s > 45.00 s`.
   - *(Note on `HARVEST_POOL_v01.json` IDs: `FIRST30_PLAN.md` had a 1-digit typo `PIA21889` for `PIA21890` ("A Last Look at Titan", allocated to rows `[3, 4]` in `HARVEST_POOL_v01.json`) and `PIA21440` for `PIA12621`/`PIA17177` (allocated to row `[6]` in `HARVEST_POOL_v01.json`); using the verified `HARVEST_POOL_v01.json` plates passes `verify_picture_inputs_032.py` `39/39` SHA-256 checks with `0` errors.)*

## All 5 Gate Outputs (`PASS`)

### 1. `clip_check.py` — PASS (exit 0)
```
clip_check: 52 rows — PASS
OK: sentence/card boundaries and end-after-VO checks clear.
```

### 2. `picture_qa.py` — PASS (exit 0, 0 fails / 131 cuts)
```
WARN   0:02 row R01 PIA20016.jpg: low detail: edge density 0.0052 < film p5 0.0103
WARN   0:37 row R05 code_graphic_032_r05_rain_preview_v01.mp4: low detail: edge density 0.0077 < film p5 0.0103
WARN   3:24 row R20 code_graphic_032_r20_fact_v01.mp4: low detail: edge density 0.0082 < film p5 0.0103
WARN   6:40 row R37 code_graphic_032_r37_spark_question_v01.mp4: low detail: luma std 16.69 < 18.0; low detail: edge density 0.0068 < film p5 0.0103
WARN   7:15 row R41 code_graphic_032_r41_no_flame_v01.mp4: low detail: edge density 0.0103 < film p5 0.0103
WARN   7:26 row R41 code_graphic_032_r41_fact_v01.mp4: low detail: edge density 0.0057 < film p5 0.0103
WARN   9:24 row R51 PIA20016.jpg: low detail: edge density 0.005 < film p5 0.0103
picture QA PASS: 0 of 131 cuts fail, 7 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/full_master_v02_pack/PICTURE_QA.md, /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/full_master_v02_pack/picture_qa_review.jpg
```

### 3. `polish_gate.py` — PASS (exit 0, 0 fails / 131 cuts)
```
polish gate PASS: 0 of 131 rows failed, 7 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/full_master_v02_pack/polish_gate_v02.json
```

### 4. `music_gate.py` — PASS (exit 0)
```
music gate PASS: titan_score_bed_v01.mp3, 585.4 s, about 70.6 BPM, brief Pace: 68-78 BPM
```

### 5. `sfx_kit.py level` — PASS (exit 0)
```
SFX level PASS: VO -20.0 LUFS, SFX -46.2 LUFS, 13 hits
```

### 6. Delivery Spec — PASS
- **Integrated Loudness:** `-14.5 LUFS` (target `~-14 LUFS`)
- **True Peak:** `-1.0 dBTP` (limit `<= -1.0 dBTP`)
- **Resolution & Frame Rate:** `1920x1080`, `30/1` fps CFR (`17,563` frames)
- **Duration:** `585.440 s` (`3.06 s` post-word hold after last spoken word at `582.380 s`)
- **Black Frames (`blackdetect=d=0.04:pix_th=0.10`):** `0` (`[]`)
