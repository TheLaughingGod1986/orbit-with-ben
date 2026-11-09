# 032 Titan Long Master v01 — Assembly & Gate Report (`J2379`)

- **Film:** `032_What-Would-Happen-If-You-Landed-On-Titan`
- **Assembled Master:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/09_Final-Export/032_what_would_happen_if_you_landed_on_titan_master_v01.mp4`
- **Master SHA-256:** `452ea3d7b5b2e7a02141072a3634163ce9f86e844f0d3e2637a64511c664d7a0`
- **Size:** `208,717,641` bytes (`199.0 MB`)
- **Format:** `1920x1080`, `30/1` fps CFR (`17,563` frames, `585.440 s`), `yuv420p` H.264 + `48 kHz` stereo AAC (`192 kbps`)
- **Assembler Script:** `07_Edit-Project/_assemble_032_full_master_v01.py`
- **Row Timing Sidecar:** `07_Edit-Project/shot_list_v08.csv` (`52` rows, `127` cuts)
- **Cut Manifest Sidecar:** `07_Edit-Project/full_master_v01_pack/cuts_v01.json`
- **Spend:** `£0`

## Inputs Verified

- **Locked Shot List:** `07_Edit-Project/SHOT_LIST_v08.md` (`sha256: efba940f89b8dc3ce5c2c41e461519e14b8af082b6473480b5787d1dc6129c9c`)
- **Locked VO Master:** `02_Voiceover/titan_landing_vo_v02b.wav` (`582.440 s`, `-20.0 LUFS`, `sha256: 55232eebb76b68639eee0681316a9e90443e36bf42892ba99c9a98735301abc5`, last spoken word ends at `582.380 s`, padded to `585.440 s` for `3.06 s` post-word hold)
- **Score Bed:** `05_Music/titan_score_bed_v01.mp3` (`585.44 s`, `70.6 BPM`, `sha256: 02c7d95865f8b39de4f9d3dfda8aa85084ecea04fc56dbd6776268279dab8f9e`)
- **House SFX Kit:** `06_Sound-Effects/kit_v01/` (`sfx_owb_rumble_low_v01.wav`, `sfx_owb_whoosh_soft_v01.wav`, `sfx_owb_tick_ui_v01.wav`)
- **Harvested Stills & SVS 20311 Clips:** `03_Reference-Material/harvest_J2089_v01/` (all stills `<= 2` appearances with distinct use-1/use-2 crop framing; SVS clips `<= 3` stretches separated by `>= 10.0 s`; `0` overlap with Short `RLSJm59OSzI`/`ffYKoNVPoqg`)
- **Composites:** `07_Edit-Project/composites_v01/` (`62` moving-plate 1080p30 composites, each `<= 3.60 s` / `108` frames, never back-to-back across the first 30 s)

## 5 Gate Outputs (All PASS)

### 1. `clip_check.py` — PASS (exit 0)
```
clip_check: 52 rows — PASS
OK: sentence/card boundaries and end-after-VO checks clear.
```

### 2. `picture_qa.py` — PASS (exit 0, 0 fails / 127 cuts)
```
WARN   0:02 row R01 PIA20016.jpg: low detail: edge density 0.0076 < film p5 0.0079
WARN   0:39 row R05 code_graphic_032_r05_rain_preview_v01.mp4: low detail: edge density 0.0077 < film p5 0.0079
WARN   2:09 row R14 PIA21450.jpg: low detail: edge density 0.0074 < film p5 0.0079
WARN   4:13 row R25 PIA21450.jpg: low detail: edge density 0.0076 < film p5 0.0079
WARN   6:40 row R37 code_graphic_032_r37_spark_question_v01.mp4: low detail: luma std 16.69 < 18.0; low detail: edge density 0.0068 < film p5 0.0079
WARN   7:26 row R41 code_graphic_032_r41_fact_v01.mp4: low detail: edge density 0.0057 < film p5 0.0079
WARN   9:24 row R51 PIA20016.jpg: low detail: edge density 0.0078 < film p5 0.0079
picture QA PASS: 0 of 127 cuts fail, 7 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/full_master_v01_pack/PICTURE_QA.md, /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/full_master_v01_pack/picture_qa_review.jpg
```

### 3. `music_gate.py` — PASS (exit 0)
```
music gate PASS: titan_score_bed_v01.mp3, 585.4 s, about 70.6 BPM, brief Pace: 68-78 BPM
```

### 4. `sfx_kit.py level` — PASS (exit 0)
```
SFX level PASS: VO -20.0 LUFS, SFX -46.2 LUFS, 13 hits
```

### 5. Delivery Spec — PASS
- **Integrated Loudness:** `-14.5 LUFS` (target `~-14 LUFS`)
- **True Peak:** `-1.0 dBTP` (limit `<= -1.0 dBTP`)
- **Resolution & Frame Rate:** `1920x1080`, `30/1` fps CFR (`17,563` frames)
- **Duration:** `585.440 s` (`3.06 s` post-word hold after last spoken word at `582.380 s`)
- **Black Frames (`blackdetect=d=0.04:pix_th=0.10`):** `0` (`[]`)
