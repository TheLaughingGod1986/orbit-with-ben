# 031 Active Short #2 (`sat12_solar_wind_air`) v02 Assembly & Gate Handoff (`J2394`, 8 Nov 2026)

## 1. Summary & Hashes

- **Parent Long (`031`):** *What Happens When Earth's Magnetic Field Flips?* (Wed 02 Dec 2026 18:00Z)
- **Short Title:** *What If the Solar Wind Blew Earth's Atmosphere Into Space?*
- **Planned Air Slot (`SHORTS_PLAN_v01.md`):** Path A **Sat 12 Dec 2026 11:30Z** (or Path B **Sat 05 Dec 2026 11:30Z** if Chief shifts `028` `v6euXX2omz4`). Zero collision against scheduled `026–029` Shorts; **no YouTube upload** per `J2394`.
- **Spend:** £0 (lifted verbatim from locked master VO `magnetic_field_flip_vo_v02a.wav`, `magnetic_field_flip_score_bed_v01.mp3`, house SFX `kit_v01`, and clean NASA SVS / HDEV / DSCOVR EPIC plates).
- **Assembler Script:** `02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/_assemble_031_short2_v02.py`
- **`v01` Preserved Untouched on NAS:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v01.mp4` (`SHA-256: 2f0f7e82e7d4c36d484d3bbf1ba7516118b3d1cdf61b788119996dc5ca85547c`)

| Asset | Path (NAS `studio-live` / `mac-mini-archive` / iCloud `OWB UAT`) | SHA-256 |
|---|---|---|
| **Short 2 `v02` Master MP4 (`1080x1920`, `25 fps` CFR, `24.48 s`, `612` frames)** | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v02.mp4` (also mirrored with matching SHA-256 at `10_Shorts/031_short_sat12_solar_wind_air_v02.mp4`, `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/031_shorts_v02/031_short_sat12_solar_wind_air_v02.mp4`, and `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/031_shorts_v02/031_short_sat12_solar_wind_air_v02.mp4`) | `4f25b1cd9d2c806367a98f3a7e173bbd0d16dc3390e0c882c223c23af6f10450` |
| **Frame 0 Still (`1080x1920`)** | `.../10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v02_frame0.jpg` | `f6b31eba43715fa776345296cbc51a1a6ef454865b3600b377e305535bd1a843` |
| **Custom Short Cover (`1080x1920`, no Orbit)** | `.../10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v02_cover.jpg` | `63c43e387c209af75bea5d73c43b6c1556b8bbcbe7a69d90c31d2fc362d94e1f` |
| **9-Shot Mid-Frame Contact Sheet** | `.../10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v02_review_9shots.jpg` | `11ae22e5d48abb1b0c35dce55530c94107ad5f42ba1c424528eedf6fafa482f5` |
| **Locked Master VO Source** | `.../02_Voiceover/magnetic_field_flip_vo_v02a.wav` | `3444635a3efa951a1031d6681390053abd9cdd3cc1ed97d537086ee7de86b3c6` |
| **Chapter-Shaped Score Bed** | `.../05_Music/magnetic_field_flip_score_bed_v01.mp3` | `9fe2f87876f9b0bbf1a80fb58d14f2ded4fddf4437efc3a83dfa4e321d0ec71f` |

---

## 2. Resolution of All 4 `J2390` FIX Items (`jobs/reviews/J2390/REVIEW.md` §2)

1. **Removed `get_nebula_wave()` and `make_cosmic_backdrop()` completely (`PASS`):**
   - Zero synthetic diagonal sine-wave plaid and zero `ImageDraw.ellipse` star dots anywhere in `_assemble_031_short2_v02.py`.
   - Every shot uses either a full `9:16` (`1080x1920`) reframe (`R39b`, `upscale=1.40x <= 2.35x`) or `composite_band_on_natural_blur()` with a 96-px cosine feather over a clean, natural dark Gaussian-blurred vertical fill derived directly from real moving NASA pixels.
2. **Removed `od.arc()` cartoon curves, `plasma_wave` sine ripple, and dark-ring cutout on `R39a` (`0.00–2.36 s`), `frame0.jpg`, `cover.jpg`, and `R39_loop` (`23.16–24.48 s`) (`PASS`):**
   - `render_r39a_open()` renders directly from clean graded 4K NASA SVS 20297 footage (`svs_20297_van_allen_earth_only.mp4` @ `6.4 s`, `upscale=0.95x`), showing the solar wind CME eruption from the Sun on the left and Earth's magnetosphere bow shock and field lines on the right, with zero `od.arc()` curves, zero `plasma_wave` sine ripple, and zero pasted Earth cutout.
3. **Removed ghost double-exposed Earth on `R39b` (`2.36–3.32 s`) (`PASS`):**
   - `r39b_magfield` renders directly from a single clean moving NASA SVS 3822 geomagnetic field lines plate (`svs_3822_magfield_left.mp4` @ `28.0 s`, full `9:16` reframe `upscale=1.40x`), with zero blended `GSFC_20171208_Archive_e001788.jpg`.
4. **Eliminated title-card text collision on `R42a` (`9.32–12.68 s`) during the `9.00–14.00 s` parent-title banner (`PASS`):**
   - `R42a` (`9.32–12.68 s`) renders a clean text-free moving NASA ISS sunlit orbital pass (`hdev_earth_views_iss_2019.mp4` @ `128.0 s`, `upscale=1.25x`) followed by `R42b` (`12.68–16.64 s`, `nasa_svs_12312_dscovr_epic_earth.mp4` @ `16.0 s`, `upscale=1.25x`), so the `9.00–14.00 s` parent-title banner (*What Happens When / Earth's Magnetic / Field Flips?*) sits over clean moving Earth imagery with zero background graphic text collision.

---

## 3. Cut Table (`9` Shots, `8` Cuts, `24.48 s` @ `25 fps` CFR)

| Shot | Row | Local Time (s) | Dur (s) | Source | Framing & Notes |
|---:|---|---:|---:|---|---|
| 1 | `R39a` | `0.00–2.36` | `2.36` | `nasa_svs_20297_magnetosphere_earth_only.mp4` | Clean graded 4K NASA SVS 20297 solar-wind CME stream & magnetosphere bow shock (`@6.4 s`, `upscale=0.95x`, `motion=22.1`, `f0diff=3.63`, `visor=0.0`). Hook caption `LOSE OUR / AIR?` (`0.00–2.20 s`). |
| 2 | `R39b` | `2.36–3.32` | `0.96` | `nasa_svs_3822_magfield_left.mp4` | Cut 1 at `2.36 s <= 2.80 s` (`scdet` confirmed) into single clean moving NASA SVS 3822 geomagnetic field lines (`@28.0 s`, full `9:16` reframe `upscale=1.40x`). |
| 3 | `R40` | `3.32–6.76` | `3.44` | `code_graphic_031_r40a_never_vanishes_v01.mp4` | Cut 2 at `3.32 s <= 4.80 s` into multipole `"NEVER VANISHES"` graphic over natural Gaussian-blurred NASA magnetosphere (`upscale=1.0x`). |
| 4 | `R41` | `6.76–9.32` | `2.56` | `hdev_earth_views_iss_2019.mp4` | Real moving NASA ISS HDEV blue atmospheric limb (`@20.0 s`, `upscale=1.15x`) over *"The nitrogen and oxygen above your head..."* |
| 5 | `R42a` | `9.32–12.68` | `3.36` | `hdev_earth_views_iss_2019.mp4` | Clean text-free moving NASA ISS sunlit orbital pass (`@128.0 s`, `upscale=1.25x`) under `9.0–14.0 s` parent-title banner (zero text collision). |
| 6 | `R42b` | `12.68–16.64` | `3.96` | `nasa_svs_12312_dscovr_epic_earth.mp4` | Clean text-free moving NASA DSCOVR EPIC rotating sunlit Earth (`@16.0 s`, `upscale=1.25x`); banner clears at `14.00 s` over *"covering the planet"*. |
| 7 | `R44a` | `16.64–19.92` | `3.28` | `PIA00407.jpg` | Viking Orbiter Mars hemisphere push (`upscale=0.65x`) over natural Gaussian-blurred vertical fill + single Teach overlay **`= 10 M WATER SHIELD`** (`16.80–19.60 s`). |
| 8 | `R44b` | `19.92–23.16` | `3.24` | `code_graphic_031_r44c_duration_comparison_v01.mp4` | Mars atmosphere loss vs Earth flip duration comparison graphic (`upscale=1.0x`) over final payoff clause (`81.4%–94.0%`). |
| 9 | `R39_loop` | `23.16–24.48` | `1.32` | `frame0_hold_sat12_solar_wind_air_v02.png` | Seamless loop preroll matching clean frame 0 + end card (`What Happens When Earth's Magnetic Field Flips?`). |

---

## 4. Pasted Gate Verdicts (All 7 Gates `PASS`)

### 4.1 `gate_shorts_open.py check --air-date 2026-12-12`
```
PASS  031_short_sat12_solar_wind_air_v02.mp4  dur=24.48s  audio=-16.9dB  motion=22.1  f0diff=3.63  cut1=2.36s  vo_onset=0.09s  tail_gap=1.46s  vo_src=/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v02_vo.wav  dhash=bc17cffffe9fccd8  visor=0.0
   sheet /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v02_open_sheet.jpg
```

### 4.2 `thumb_preview.py short` (Frame 0 & Custom Cover)
```
/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v02_frame0_preview.jpg
PASS  031_short_sat12_solar_wind_air_v02_frame0.jpg  saturation=101.5  near_black=0%

/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v02_cover_preview.jpg
PASS  031_short_sat12_solar_wind_air_v02_cover.jpg  saturation=111.2  near_black=0%
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
 R40     5.0s code_graphic_031_r40a_never_ WARN low detail: edge density 0.0331 < film p5 0.0363
 R41     8.0s hdev_earth_views_iss_2019.mp ok
R42a    11.0s hdev_earth_views_iss_2019.mp ok
R42b    14.7s nasa_svs_12312_dscovr_epic_e ok
R44a    18.3s PIA00407.jpg                 ok
R44b    21.5s code_graphic_031_r44c_durati ok
R39_loop    23.8s frame0_hold_sat12_solar_wind ok
polish gate PASS: 0 of 9 rows failed, 1 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v02_polish_gate.json

WARN   0:05 row R40 code_graphic_031_r40a_never_vanishes_v01.mp4: low detail: edge density 0.0331 < film p5 0.0363
picture QA PASS: 0 of 9 cuts fail, 1 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v02_picture_qa/PICTURE_QA.md, /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v02_picture_qa/picture_qa_review.jpg
```
