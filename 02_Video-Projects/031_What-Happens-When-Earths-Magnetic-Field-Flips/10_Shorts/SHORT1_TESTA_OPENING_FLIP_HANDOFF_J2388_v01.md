# 031 Active Short #1 (`testA_opening_flip`) v01 Assembly & Gate Handoff (`J2388`, 8 Nov 2026)

## 1. Summary & Hashes

- **Parent Long (`031`):** *What Happens When Earth's Magnetic Field Flips?* (Wed 02 Dec 2026 18:00Z)
- **Short Title (Test A Opening Short):** *What Happens When Earth's Magnetic Field Flips?*
- **Planned Air Slot (`SHORTS_PLAN_v01.md`):** Path A **Sat 05 Dec 2026 11:30Z** (or Path B **Wed 02 Dec 2026 11:30Z** go-public day if Chief shifts `028` `v6euXX2omz4` to Sat 05 Dec). Zero collision against scheduled `026–029` Shorts; **no YouTube upload** per `J2388`.
- **Spend:** £0 (lifted verbatim from locked master VO `magnetic_field_flip_vo_v02a.wav`, `magnetic_field_flip_score_bed_v01.mp3`, house SFX `kit_v01`, and repaired `031` `v02` opening cuts `R01–R04` free of any synthetic bullseye overlay, sine-wave plaid, painted dots, or cartoon arcs, and with honest `R03` DSCOVR EPIC pixels).
- **Assembler Script:** `02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/_assemble_031_short1_v01.py`

| Asset | Path (NAS `studio-live` / `mac-mini-archive`) | SHA-256 |
|---|---|---|
| **Short 1 Master MP4 (`1080x1920`, `25 fps` CFR, `33.00 s`, `825` frames)** | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/testA_opening_flip/06_Final-Exports/031_short_testA_opening_flip_v01.mp4` (also mirrored at `10_Shorts/031_short_testA_opening_flip_v01.mp4`, `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/031_shorts_v01/031_short_testA_opening_flip_v01.mp4`, and iCloud `OWB UAT/031_shorts_v01/031_short_testA_opening_flip_v01.mp4`) | `ebe11bb730ccfab8681d564d3588d17011a28629c7b6f926eba952bfc98c4bcd` |
| **Frame 0 Still (`1080x1920`)** | `.../10_Shorts/testA_opening_flip/06_Final-Exports/031_short_testA_opening_flip_v01_frame0.jpg` | `aa0763c2f1e553ac373e6596c684c1145b115242afcac0c9fa15d8eaf0030ada` |
| **Custom Short Cover (`1080x1920`, no Orbit)** | `.../10_Shorts/testA_opening_flip/06_Final-Exports/031_short_testA_opening_flip_v01_cover.jpg` | `8f5be5cd1e41b0b5df695d6fbbe6e69682965f010ddc70f2e70b9bb053caee5d` |
| **Locked Master VO Source** | `.../02_Voiceover/magnetic_field_flip_vo_v02a.wav` | `3444635a3efa951a1031d6681390053abd9cdd3cc1ed97d537086ee7de86b3c6` |
| **Chapter-Shaped Score Bed** | `.../05_Music/magnetic_field_flip_score_bed_v01.mp3` | `9fe2f87876f9b0bbf1a80fb58d14f2ded4fddf4437efc3a83dfa4e321d0ec71f` |

---

## 2. Spoken Lift & Timing Audit (`OWB-2026-11-E1`, `LEARNINGS 17` & `SHORTS_PLAN_v01.md`)

- **Spoken Sentences (`s00–s08` = `96` words):**
  1. `s00` (master `0.14–8.34 s`, local `0.08–8.28 s`, `8.20 s`, 23w): *"Right now, the invisible magnetic shield around our planet is weakening, and the north magnetic pole is racing across the Arctic towards Siberia."*
  2. `s01` (master `9.06–11.84 s`, local `8.50–11.28 s`, `2.78 s`, 8w): *"One day, north and south will swap places."*
  3. `s02` (master `12.54–17.08 s`, local `11.50–16.04 s`, `4.54 s`, 15w): *"Will life on Earth survive that danger, or will our air blow away into space?"*
  4. `s03` (master `18.12–18.36 s`, local `16.26–16.50 s`, `0.24 s`, 1w): *"No."*
  5. `s04` (master `19.02–20.08 s`, local `16.72–17.78 s`, `1.06 s`, 3w): *"We will survive."*
  6. `s05` (master `20.70–23.28 s`, local `18.00–20.58 s`, `2.58 s`, 8w): *"Life has lived through hundreds of magnetic flips."*
  7. `s06` (master `23.80–27.86 s`, local `20.80–24.86 s`, `4.06 s`, 15w): *"So why do satellites in orbit already have to shut down over the South Atlantic?"*
  8. `s07` (master `28.50–31.32 s`, local `25.08–27.90 s`, `2.82 s`, 10w): *"How do we know Earth's compass can turn upside down?"*
  9. `s08` (master `31.90–35.32 s`, local `28.12–31.54 s`, `3.42 s`, 13w): *"And what will the night sky look like when the poles trade places?"*
- **Key Timing & E1 / Test A Metrics:**
  - **Frame-0 Source:** `nasa_svs_3822_magfield_left.mp4` (`@21.2 s`, full-frame 9:16 reframe of moving blue/gold geomagnetic field lines around turning Earth, `motion_0_1s = 27.25 >= 10.0`, `f0diff = 9.28`, `visor_frac = 0.0`, `near_opens = []`, zero synthetic bullseye overlay, zero sine-wave plaid, zero painted dots, zero cartoon arcs).
  - **VO Onset:** `0.08 s <= 0.15 s` (`"test_a": true` recorded in `031_short_testA_opening_flip_v01_meta.json`).
  - **Inter-Sentence Breath Gaps:** All 8 sentence seams tightened to `0.22 s < 0.25 s`, compressing the 35.18 s raw span into `31.46 s` of continuous speech (`0.08–31.54 s`).
  - **Cut 1 & Cut 2 Timestamps:** Cut 1 at `2.32 s <= 2.80 s`, Cut 2 at `4.72 s <= 4.80 s` (`12` cuts total across `13` shots; max shot hold `3.68 s <= 4.00 s`; every cut lands on a 25 fps frame boundary inside a word gap).
  - **Hook Caption (`0.00–2.20 s`):** `POLES ARE` (white) / **`FLIPPING`** (yellow `#FFE000`, `132 px` Arial Black).
  - **`9–14 s` Parent-Title Banner (`9.00–14.00 s`):** `What Happens When / Earth's Magnetic / Field Flips?` (`58 px`, `y=841..1086` inside `16:9` centre band `y=656..1264`, over clean text-free NASA ISS aurora `R02a` and NASA SVS 3822 magnetosphere `R02a2` with zero graphic text collision; `R02b` CODE flip starts at `14.12 s` after the banner clears).
  - **Single Teaching Overlay (`18.52–20.56 s`):** **`HUNDREDS OF FLIPS`** (`bbox=[190, 1187, 889, 1245]`, `58 px` = `9.5%` / `11.5%` line target inside `y=656..1264`, clear of `0–2 s` and `9–14 s`).
  - **Payoff & `LEARNINGS 17` Question Handoff (`16.26–31.54 s`):** Answers the immediate survival myth (`"No. We will survive. Life has lived through hundreds of magnetic flips."`, `16.26–20.58 s`) and ends cleanly on the three concrete questions `031` answers (`s06–s08`, `20.80–31.54 s`).
  - **Loop Preroll & End Card (`31.68–33.00 s`):** Last word ends at `31.54 s` (`tail_gap = 1.46 s <= 1.50 s`); matches frame 0 at `31.68 s` with house end card naming the exact long listing title (`What Happens When Earth's Magnetic Field Flips?`).
  - **Audio Loudness:** VO `-16.3 LUFS`, Music Bed `-34.5 LUFS`, SFX `-40.2 LUFS` (`6` hits), AAC stream integrated `-14.1 LUFS`, True Peak `-2.1 dBTP <= -1.0 dBTP`.

---

## 3. Cut Table (`13` Shots, `12` Cuts, `33.00 s` @ `25 fps` CFR)

| Shot | Row | Local Time (s) | Dur (s) | Source | Framing & Notes |
|---:|---|---:|---:|---|---|
| 1 | `R01a` | `0.00–2.32` | `2.32` | `nasa_svs_3822_magfield_left.mp4` | Full 9:16 reframe of moving blue/gold geomagnetic field lines around turning Earth (`upscale=1.4x`, `ss=21.2s`). Hook caption `POLES ARE / FLIPPING` (`0.00–2.20 s`). |
| 2 | `R01a2` | `2.32–4.72` | `2.40` | `nasa_svs_20297_magnetosphere_earth_only.mp4` | Cut 1 at `2.32 s <= 2.80 s` into 4K NASA SVS 20297 magnetosphere bow shock & solar wind stream (`upscale=0.9x`). |
| 3 | `R01b` | `4.72–8.40` | `3.68` | `code_graphic_031_r01b_poledrift_v01.mp4` | Cut 2 at `4.72 s <= 4.80 s` into North Magnetic Pole drift (`1831 -> TODAY`, `55 KM/YR`) over natural Gaussian-blurred NASA magnetosphere (`upscale=1.0x`). |
| 4 | `R02a` | `8.40–11.40` | `3.00` | `iss030e078095_aurora_timelapse.mp4` | Real moving NASA ISS aurora timelapse (`002_R02_c1.mp4`, `upscale=1.5x`) under first half of `9.0–14.0 s` parent-title banner (zero text collision). |
| 5 | `R02a2` | `11.40–14.12` | `2.72` | `nasa_svs_3822_magfield_left.mp4` | Clean text-free NASA SVS 3822 magnetosphere loops (`ss=46.0s`, `upscale=1.35x`) under second half of `9.0–14.0 s` parent-title banner. |
| 6 | `R02b` | `14.12–16.16` | `2.04` | `code_graphic_031_r02b_flip_v01.mp4` | Magnetic poles swap (`N <-> S`, `POLES SWAP`) starting after the `14.00 s` banner clears (`upscale=1.0x`). |
| 7 | `R03a` | `16.16–18.44` | `2.28` | `nasa_svs_12312_dscovr_epic_earth.mp4` | Honest NASA DSCOVR EPIC sunlit rotating Earth (`004_R03_c1.mp4`, `upscale=1.25x`) over *"No. We will survive."* |
| 8 | `R03b` | `18.44–20.68` | `2.24` | `nasa_svs_12312_dscovr_epic_earth.mp4` | Closer NASA DSCOVR EPIC sunlit Earth (`005_R03_c2.mp4`, `upscale=1.5x`) + single Teach overlay **`HUNDREDS OF FLIPS`** (`18.52–20.56 s`). |
| 9 | `R04a` | `20.68–23.64` | `2.96` | `hdev_earth_views_iss_2019.mp4` | Real moving NASA ISS HDEV orbital pass (`006_R04_c1.mp4`, `upscale=1.5x`) over Question 1 (*"So why do satellites in orbit already have to shut down..."*). |
| 10 | `R04a2` | `23.64–24.96` | `1.32` | `hdev_earth_views_iss_2019.mp4` | Second NASA ISS HDEV orbital limb angle (`ss=128.0s`, `upscale=1.5x`) finishing Question 1 (*"...over the South Atlantic?"*). |
| 11 | `R04b` | `24.96–28.00` | `3.04` | `code_graphic_031_r04b_compass_v02.mp4` | Compass needle turning upside down (`007_R04_c2.mp4`, `upscale=1.0x`) over Question 2 (*"How do we know Earth's compass can turn upside down?"*). |
| 12 | `R04c` | `28.00–31.68` | `3.68` | `iss030e078095_aurora_timelapse.mp4` | Real moving NASA ISS aurora curtain (`008_R04_c3.mp4`, `upscale=1.5x`) over Question 3 (*"And what will the night sky look like when the poles trade places?"*). |
| 13 | `R01_loop` | `31.68–33.00` | `1.32` | `frame0_hold_testA_opening_flip.png` | Seamless loop preroll matching frame 0 + end card (`What Happens When Earth's Magnetic Field Flips?`). |

---

## 4. Pasted Gate Verdicts (All 7 Gates `PASS`)

### 4.1 `gate_shorts_open.py check --air-date 2026-12-05` (`test_a: true` in `_meta.json`)
```
PASS  031_short_testA_opening_flip_v01.mp4  dur=33.0s  audio=-16.7dB  motion=27.25  f0diff=9.28  cut1=2.32s  vo_onset=0.08s  tail_gap=1.46s  vo_src=/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/testA_opening_flip/06_Final-Exports/031_short_testA_opening_flip_v01_vo.wav  dhash=982b074783078b06  visor=0.0
   warn  duration 33.0s outside 22–27s band
   sheet /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/testA_opening_flip/06_Final-Exports/031_short_testA_opening_flip_v01_open_sheet.jpg
```

### 4.2 `thumb_preview.py short` (Frame 0 & Custom Cover)
```
/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/testA_opening_flip/06_Final-Exports/031_short_testA_opening_flip_v01_frame0_preview.jpg
PASS  031_short_testA_opening_flip_v01_frame0.jpg  saturation=105.4  near_black=1%

/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/testA_opening_flip/06_Final-Exports/031_short_testA_opening_flip_v01_cover_preview.jpg
PASS  031_short_testA_opening_flip_v01_cover.jpg  saturation=138.1  near_black=2%
```

### 4.3 `sfx_kit.py level` & `music_gate.py`
```
SFX level PASS: VO -16.3 LUFS, SFX -40.2 LUFS, 6 hits
music gate PASS: magnetic_field_flip_score_bed_v01.mp3, 570.8 s, about 109.1 BPM, brief Pace: 66-74 BPM
```

### 4.4 `polish_gate.py` & `picture_qa.py`
```
R01a     1.2s nasa_svs_3822_magfield_left. ok
R01a2     3.5s nasa_svs_20297_magnetosphere ok
R01b     6.6s code_graphic_031_r01b_poledr ok
R02a     9.9s iss030e078095_aurora_timelap ok
R02a2    12.8s nasa_svs_3822_magfield_left. ok
R02b    15.1s code_graphic_031_r02b_flip_v ok
R03a    17.3s nasa_svs_12312_dscovr_epic_e ok
R03b    19.6s nasa_svs_12312_dscovr_epic_e ok
R04a    22.2s hdev_earth_views_iss_2019.mp ok
R04a2    24.3s hdev_earth_views_iss_2019.mp ok
R04b    26.5s code_graphic_031_r04b_compas ok
R04c    29.8s iss030e078095_aurora_timelap WARN low detail: edge density 0.0204 < film p5 0.0237
R01_loop    32.3s frame0_hold_testA_opening_fl ok
polish gate PASS: 0 of 13 rows failed, 1 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/testA_opening_flip/06_Final-Exports/031_short_testA_opening_flip_v01_polish_gate.json

WARN   0:30 row R04c iss030e078095_aurora_timelapse.mp4: low detail: edge density 0.0204 < film p5 0.0237
picture QA PASS: 0 of 13 cuts fail, 1 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/testA_opening_flip/06_Final-Exports/031_short_testA_opening_flip_v01_picture_qa/PICTURE_QA.md, /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/testA_opening_flip/06_Final-Exports/031_short_testA_opening_flip_v01_picture_qa/picture_qa_review.jpg
```
