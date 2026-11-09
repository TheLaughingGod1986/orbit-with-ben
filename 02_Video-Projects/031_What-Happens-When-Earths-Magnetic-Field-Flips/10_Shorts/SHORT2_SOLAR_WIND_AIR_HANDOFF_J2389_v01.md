# 031 Active Short #2 (`sat12_solar_wind_air`) v01 Assembly & Gate Handoff (`J2389`, 8 Nov 2026)

## 1. Summary & Hashes

- **Parent Long (`031`):** *What Happens When Earth's Magnetic Field Flips?* (Wed 02 Dec 2026 18:00Z)
- **Short Title:** *What If the Solar Wind Blew Earth's Atmosphere Into Space?*
- **Planned Air Slot (`SHORTS_PLAN_v01.md`):** Path A **Sat 12 Dec 2026 11:30Z** (or Path B **Sat 05 Dec 2026 11:30Z** if Chief shifts `028` `v6euXX2omz4`). Zero collision against scheduled `026–029` Shorts; **no YouTube upload** per `J2389`.
- **Spend:** £0 (lifted verbatim from locked master VO `magnetic_field_flip_vo_v02a.wav`, `magnetic_field_flip_score_bed_v01.mp3`, house SFX `kit_v01`, and verified `031` `v02` plates/graphics).
- **Assembler Script:** `02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/_assemble_031_short2_v01.py`

| Asset | Path (NAS `studio-live` / `mac-mini-archive`) | SHA-256 |
|---|---|---|
| **Short 2 Master MP4 (`1080x1920`, `25 fps` CFR, `24.48 s`, `612` frames)** | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v01.mp4` (also mirrored at `10_Shorts/031_short_sat12_solar_wind_air_v01.mp4` and `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/031_shorts_v01/031_short_sat12_solar_wind_air_v01.mp4`) | `2f0f7e82e7d4c36d484d3bbf1ba7516118b3d1cdf61b788119996dc5ca85547c` |
| **Frame 0 Still (`1080x1920`)** | `.../10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v01_frame0.jpg` | `525885ee2c836f8fb5114532de207a83c5a5409d0b200bad83b5d961fd09762d` |
| **Custom Short Cover (`1080x1920`, no Orbit)** | `.../10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v01_cover.jpg` | `b3f860ab6b94133c0bd637cdbba2ab6724f669876f61b5b9dee2c622c26a69d5` |
| **Locked Master VO Source** | `.../02_Voiceover/magnetic_field_flip_vo_v02a.wav` | `3444635a3efa951a1031d6681390053abd9cdd3cc1ed97d537086ee7de86b3c6` |
| **Chapter-Shaped Score Bed** | `.../05_Music/magnetic_field_flip_score_bed_v01.mp3` | `9fe2f87876f9b0bbf1a80fb58d14f2ded4fddf4437efc3a83dfa4e321d0ec71f` |

---

## 2. Spoken Lift & Timing Audit (`OWB-2026-11-E1` & `SHORTS_PLAN_v01.md`)

- **Spoken Sentences (`s65, s67, s70, s74` = `64` words):**
  1. `s65` (master `398.42–401.52 s`, local `0.08–3.18 s`, `3.10 s`, 10w): *"What if the solar wind blew Earth's atmosphere into space?"*
  2. `s67` (master `405.52–408.78 s`, local `3.40–6.66 s`, `3.26 s`, 7w): *"First, Earth's magnetic field never vanishes completely."*
  3. `s70` (master `423.96–433.60 s`, local `6.90–16.54 s`, `9.64 s`, 28w): *"The nitrogen and oxygen above your head weigh about a kilogram on every square centimeter, as much as a layer of water ten meters deep covering the planet."*
  4. `s74` (master `455.38–461.62 s`, local `16.78–23.02 s`, `6.24 s`, 19w): *"A flip on Earth takes only a few thousand years, far too brief to steal a heavy planet's atmosphere."*
- **Key Timing & E1 Metrics:**
  - **Frame-0 Source:** `nasa_svs_20297_magnetosphere_earth_only.mp4` (`@6.0 s`, moving solar-wind bow shock and geomagnetic field lines deflecting around Earth, `motion_0_1s = 37.63 >= 10.0`, `f0diff = 11.21`, `visor_frac = 0.0`, `near_opens = []`, zero synthetic bullseye overlay).
  - **VO Onset:** `0.08 s` (`0.09 s` detected by `gate_shorts_open.py`, `<= 0.15 s`).
  - **Spoken Subject & Surprise:** `"solar wind blew"` by `1.46 s <= 1.50 s`, `"Earth's"` at `1.82 s <= 2.50 s`.
  - **Sentence-1 Seam Breath:** `0.22 s < 0.25 s` (`3.18–3.40 s`), bridged across Cut 2 (`3.32 s`) into `"First, Earth's magnetic field never vanishes completely."`
  - **Cut 1 & Cut 2 Timestamps:** Cut 1 at `2.36 s <= 2.80 s`, Cut 2 at `3.32 s <= 4.80 s` (`8` cuts total across `9` shots; max shot hold `3.96 s <= 4.00 s`; every cut lands inside a verified word gap).
  - **Hook Caption (`0.00–2.20 s`):** `LOSE OUR` (white) / **`AIR?`** (yellow `#FFE000`, `132 px` Arial Black).
  - **`9–14 s` Parent-Title Banner (`9.00–14.00 s`):** `What Happens When / Earth's Magnetic / Field Flips?` (`58 px`, `y=841..1086` inside `16:9` centre band `y=656..1264`).
  - **Single Teaching Overlay (`16.80–19.60 s`):** **`= 10 M WATER SHIELD`** (`bbox=[169, 719, 910, 777]`, strictly inside `y=656..1264`, clear of `0–2 s` and `9–14 s`).
  - **Payoff Timing:** `16.78–23.02 s` (`68.5%–94.0%` of `24.48 s` runtime; final answer clause *"far too brief to steal a heavy planet's atmosphere"* at `19.92–23.02 s` = `81.4%–94.0% >= 70%`).
  - **Loop Preroll & End Card (`23.16–24.48 s`):** Last word ends at `23.02 s` (`tail_gap = 1.46 s <= 1.50 s`); matches frame 0 at `23.16 s` with house end card naming the exact long listing title (`What Happens When Earth's Magnetic Field Flips?`).
  - **Audio Loudness:** VO `-16.5 LUFS`, Music Bed `-34.3 LUFS`, SFX `-38.5 LUFS` (`5` hits), AAC stream integrated `-14.0 LUFS`, True Peak `-2.2 dBTP <= -1.0 dBTP`.

---

## 3. Cut Table (`9` Shots, `8` Cuts, `24.48 s` @ `25 fps` CFR)

| Shot | Row | Local Time (s) | Dur (s) | Source | Framing & Notes |
|---:|---|---:|---:|---|---|
| 1 | `R39a` | `0.00–2.36` | `2.36` | `nasa_svs_20297_magnetosphere_earth_only.mp4` | Moving solar wind bow shock deflecting around Earth (`upscale=0.9x`). Hook caption `LOSE OUR / AIR?` (`0.00–2.20 s`). |
| 2 | `R39b` | `2.36–3.32` | `0.96` | `nasa_svs_3822_magfield_left.mp4` | Cut 1 at `2.36 s <= 2.80 s` (`scdet` confirmed) into sunlit atmospheric horizon & golden magnetosphere (`upscale=1.4x`). |
| 3 | `R40` | `3.32–6.76` | `3.44` | `code_graphic_031_r40a_never_vanishes_v01.mp4` | Cut 2 at `3.32 s <= 4.80 s` into multipole `"NEVER VANISHES"` graphic (`upscale=1.0x`). |
| 4 | `R41` | `6.76–9.32` | `2.56` | `hdev_earth_views_iss_2019.mp4` | Real moving NASA ISS HDEV blue atmospheric limb separating CODE graphics (`upscale=1.15x`). |
| 5 | `R42a` | `9.32–12.68` | `3.36` | `code_graphic_031_r42b_column_mass_v01.mp4` | `"1 CM² AIR ≈ 1 KG"` atmospheric column mass graphic (`upscale=1.0x`) under `9.0–14.0 s` parent-title banner. |
| 6 | `R42b` | `12.68–16.64` | `3.96` | `nasa_svs_12312_dscovr_epic_earth.mp4` | Real moving NASA DSCOVR EPIC rotating sunlit Earth (`upscale=1.25x`); banner clears at `14.00 s`. |
| 7 | `R44a` | `16.64–19.92` | `3.28` | `PIA00407.jpg` | Viking Orbiter Mars hemisphere push (`upscale=0.65x`) + single Teach overlay **`= 10 M WATER SHIELD`** (`16.80–19.60 s`). |
| 8 | `R44b` | `19.92–23.16` | `3.24` | `code_graphic_031_r44c_duration_comparison_v01.mp4` | Mars atmosphere loss vs Earth flip duration comparison graphic (`upscale=1.0x`) over final payoff clause (`81.4%–94.0%`). |
| 9 | `R39_loop` | `23.16–24.48` | `1.32` | `frame0_hold_sat12_solar_wind_air.png` | Seamless loop preroll matching frame 0 + end card (`What Happens When Earth's Magnetic Field Flips?`). |

---

## 4. Pasted Gate Verdicts (All 7 Gates `PASS`)

### 4.1 `gate_shorts_open.py check --air-date 2026-12-12`
```
PASS  031_short_sat12_solar_wind_air_v01.mp4  dur=24.48s  audio=-16.9dB  motion=37.63  f0diff=11.21  cut1=2.36s  vo_onset=0.09s  tail_gap=1.46s  vo_src=/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v01_vo.wav  dhash=a917d9dbeb9d99db  visor=0.0
   sheet /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v01_open_sheet.jpg
```

### 4.2 `thumb_preview.py short` (Frame 0 & Custom Cover)
```
/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v01_frame0_preview.jpg
PASS  031_short_sat12_solar_wind_air_v01_frame0.jpg  1080x1920  223KB  sharp=303  bright=117

/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v01_cover_preview.jpg
PASS  031_short_sat12_solar_wind_air_v01_cover.jpg  1080x1920  458KB  sharp=767  bright=124
```

### 4.3 `sfx_kit.py level` & `music_gate.py`
```
SFX level PASS: VO -16.5 LUFS, SFX -38.5 LUFS, 5 hits
music gate PASS: magnetic_field_flip_score_bed_v01.mp3, 570.8 s, about 109.1 BPM, brief Pace: 66-74 BPM
```

### 4.4 `polish_gate.py` & `picture_qa.py`
```
R39a     1.2s nasa_svs_20297_magnetosphere ok
R39b     2.8s nasa_svs_3822_magfield_left. ok
 R40     5.0s code_graphic_031_r40a_never_ WARN low detail: edge density 0.047 < film p5 0.0493
 R41     8.0s hdev_earth_views_iss_2019.mp ok
R42a    11.0s code_graphic_031_r42b_column ok
R42b    14.7s nasa_svs_12312_dscovr_epic_e ok
R44a    18.3s PIA00407.jpg                 ok
R44b    21.5s code_graphic_031_r44c_duration_comparison_v01.mp4 ok
R39_loop    23.8s frame0_hold_sat12_solar_wind ok
polish gate PASS: 0 of 9 rows failed, 1 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v01_polish_gate.json

WARN   0:05 row R40 code_graphic_031_r40a_never_vanishes_v01.mp4: low detail: edge density 0.047 < film p5 0.0493
picture QA PASS: 0 of 9 cuts fail, 1 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v01_picture_qa/PICTURE_QA.md, /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v01_picture_qa/picture_qa_review.jpg
```
