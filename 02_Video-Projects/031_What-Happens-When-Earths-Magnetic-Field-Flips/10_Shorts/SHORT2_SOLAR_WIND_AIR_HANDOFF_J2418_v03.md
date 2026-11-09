# 031 Active Short #2 (`sat12_solar_wind_air`) v03 True Full-Bleed Vertical Assembly & Gate Handoff (`J2418`, 9 Nov 2026)

## 1. Summary, `ffprobe` Verification & SHA-256 Hashes

- **Parent Long (`031`):** *What Happens When Earth's Magnetic Field Flips?* (Uploaded Private as `G5uMANXHtNU` for **Wed 02 Dec 2026 18:00Z**)
- **Short Title:** *What If the Solar Wind Blew Earth's Atmosphere Into Space?*
- **Planned Air Slot (`SHORTS_PLAN_v01.md`):** Path A **Sat 12 Dec 2026 11:30Z** (or Path B **Sat 05 Dec 2026 11:30Z** if Chief shifts `028` `v6euXX2omz4`). **No YouTube upload** per `J2418` (`J2402` uploaded only the Long and Short 1).
- **Spend:** £0 (lifted verbatim from locked master VO `magnetic_field_flip_vo_v02a.wav`, `magnetic_field_flip_score_bed_v01.mp3`, house SFX `kit_v01`, and clean NASA SVS / HDEV / DSCOVR EPIC / Viking / VIIRS plates).
- **Assembler Script:** `02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/_assemble_031_short2_v03.py`
- **`v01` & `v02` Preserved Untouched on NAS:**
  - `031_short_sat12_solar_wind_air_v01.mp4` (`SHA-256: 2f0f7e82e7d4c36d484d3bbf1ba7516118b3d1cdf61b788119996dc5ca85547c`)
  - `031_short_sat12_solar_wind_air_v02.mp4` (`SHA-256: 4f25b1cd9d2c806367a98f3a7e173bbd0d16dc3390e0c882c223c23af6f10450`)

| Asset | Path (NAS `studio-live` / `mac-mini-archive` / iCloud `OWB UAT`) | SHA-256 |
|---|---|---|
| **Short 2 `v03` Master MP4 (`1080x1920`, `25 fps` CFR, `24.48 s`, `612` frames)** | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v03.mp4` (also mirrored with matching SHA-256 at `10_Shorts/031_short_sat12_solar_wind_air_v03.mp4`, `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/031_shorts_v03/031_short_sat12_solar_wind_air_v03.mp4`, and `~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/031_shorts_v03/031_short_sat12_solar_wind_air_v03.mp4`) | `a385834d7e81cc68b9f423922fbe3a7eed222585be7aec75f4efaf961dcfcab3` |
| **Frame 0 Still (`1080x1920`)** | `.../10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v03_frame0.jpg` | `916e1649b0a90c733fb58098a26f1b4311dbe5be93217ee5c7c438935e141a32` |
| **Custom Short Cover (`1080x1920`, no Orbit)** | `.../10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v03_cover.jpg` | `02851f7344b95867afaf346e515b57aa83f1d28b996d75356b330e241d4ccf86` |
| **9-Shot Mid-Frame Contact Sheet** | `.../10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v03_review_9shots.jpg` | `b1a8d07109739f6818439ce63a6bf1b9f8df736a81498e1ea1ca43c14d5dc507` |
| **Locked Master VO Source** | `.../02_Voiceover/magnetic_field_flip_vo_v02a.wav` | `3444635a3efa951a1031d6681390053abd9cdd3cc1ed97d537086ee7de86b3c6` |
| **Chapter-Shaped Score Bed** | `.../05_Music/magnetic_field_flip_score_bed_v01.mp3` | `9fe2f87876f9b0bbf1a80fb58d14f2ded4fddf4437efc3a83dfa4e321d0ec71f` |

### `ffprobe` Output (`v02` vs `v03`)
Both `v02` and `v03` have container dimensions `width=1080, height=1920, SAR=1:1, DAR=9:16, rotation=none, 25/1 fps, 612 frames (24.480000 s)`:
```json
{
  "streams": [
    {
      "width": 1080,
      "height": 1920,
      "sample_aspect_ratio": "1:1",
      "display_aspect_ratio": "9:16",
      "r_frame_rate": "25/1",
      "avg_frame_rate": "25/1",
      "duration": "24.480000",
      "nb_frames": "612"
    }
  ]
}
```

---

## 2. Which Builder Step Added the Blur-Pad Layout (Root Cause & Fix)

- **Root Cause (`_assemble_031_short2_v02.py` lines 334–384):**
  - `_assemble_031_short2_v02.py` defined `make_natural_blur_bg(src_16x9, zoom)` (lines 334–348), which stretched a `16:9` frame vertically to `1080x1920` and applied `ImageFilter.GaussianBlur(radius=42)`, and `composite_band_on_natural_blur(fg_16x9, bg_src_16x9, mask_credit, zoom)` (lines 351–384), which pasted the `16:9` picture into the central `1080x608` horizontal band (`BAND_Y0 = 656` to `BAND_Y1 = 1264`, with a 96-px cosine feather) over that blurred top/bottom background (`y = 0..656` and `y = 1264..1920`).
  - `composite_band_on_natural_blur()` was called on **8 of the 9 shots** in `v02`: `R39a` (line 424), `R40` (line 456), `R41` (line 464), `R42a` (line 472), `R42b` (line 480), `R44a` (line 490), `R44b` (line 498), and `R39_loop` (line 436 via `open_f0`). (In `_assemble_031_short2_v01.py`, `composite_band_on_backdrop()` similarly placed a `1080x608` 16:9 strip over `make_cosmic_backdrop()`).
  - Note: `BAND_Y0 = 656` / `BAND_Y1 = 1264` is the safe text zone for Short titles and teach overlays, **never** a picture crop box.
- **How `v03` Fixes It (`_assemble_031_short2_v03.py`):**
  - Completely deleted `make_natural_blur_bg()` and `composite_band_on_natural_blur()`.
  - Every single shot (all 9 shots) is reframed via `crop_affine_9x16()` to fill the entire `1080x1920` (`9:16`) canvas edge-to-edge with sharp, unblurred imagery (`upscale <= 1.96x <= 2.35x`).

---

## 3. Cut Table (`9` Shots, `8` Cuts, `24.48 s` @ `25 fps` CFR — 100% Full-Bleed `1080x1920`)

| Shot | Row | Local Time (s) | Dur (s) | Source | Full-Bleed `1080x1920` (`9:16`) Framing & Notes |
|---:|---|---:|---:|---|---|
| 1 | `R39a` | `0.00–2.36` | `2.36` | `nasa_svs_20297_magnetosphere_earth_only.mp4` | Native `3840x2160` 4K `9:16` vertical crop (`ch=1960->1840`, `cw=1102->1035`, `upscale=1.04x`, `motion=22.13`, `f0diff=5.01`, `visor=0.0`) panning from the solar CME eruption into Earth's magnetosphere bow shock. Hook caption `LOSE OUR / AIR?` (`0.00–2.20 s`). |
| 2 | `R39b` | `2.36–3.32` | `0.96` | `nasa_svs_3822_magfield_left.mp4` | Cut 1 at `2.36 s <= 2.80 s` (`scdet` confirmed) into full-bleed `9:16` vertical crop (`ch=1040->980`, `upscale=1.96x`) of NASA SVS 3822 geomagnetic field lines. |
| 3 | `R40` | `3.32–6.76` | `3.44` | `code_graphic_031_r40a_never_vanishes_v03.mp4` | Cut 2 at `3.32 s <= 4.80 s` into full-bleed `1080x1920` vertical multipole `"NEVER VANISHES"` graphic composited seamlessly over sharp full-height `9:16` NASA SVS 3822 geomagnetic field lines (`upscale=1.04x`, zero blur bands). |
| 4 | `R41` | `6.76–9.32` | `2.56` | `hdev_earth_views_iss_2019.mp4` | Full-bleed `9:16` vertical crop (`ch=760->724`, `upscale=1.92x`) of NASA ISS HDEV sunlit blue atmospheric limb crowning the top of the `1080x1920` frame with cumulus clouds and ocean filling the full height below. |
| 5 | `R42a` | `9.32–12.68` | `3.36` | `hdev_earth_views_iss_2019.mp4` | Full-bleed `9:16` vertical crop (`@128.0 s`, `ch=760->724`, `upscale=1.92x`) of sunlit Earth horizon & ISS Soyuz module under `9.0–14.0 s` parent-title banner (zero text collision, zero blur bands). |
| 6 | `R42b` | `12.68–16.64` | `3.96` | `nasa_svs_12312_dscovr_epic_earth.mp4` | Full-bleed `1080x1920` vertical DSCOVR EPIC rotating sunlit Earth (`upscale=1.48x`) with sharp unblurred NASA SVS 3822 polar geomagnetic field lines arching to the top and bottom of the `9:16` frame. |
| 7 | `R44a` | `16.64–19.92` | `3.28` | `PIA00407.jpg` | Full-bleed `9:16` vertical crop (`ch=4560->4180`, `cw=2565->2351`, `upscale=0.46x`) inside the `6787x6787` Viking Orbiter Mars mosaic filling all four corners of `1080x1920` + single Teach overlay **`= 10 M WATER SHIELD`** (`16.80–19.60 s`). |
| 8 | `R44b` | `19.92–23.16` | `3.24` | `code_graphic_031_r44c_duration_comparison_v03.mp4` | Full-bleed `9:16` vertical pan (`upscale=0.28x`) inside the `11500x11500` NASA VIIRS Eastern Hemisphere Blue Marble (`GSFC_20171208_Archive_e001788.jpg`) with animated `"EARTH FIELD FLIP / A FEW THOUSAND YEARS"` comparison bar graphic. |
| 9 | `R39_loop` | `23.16–24.48` | `1.32` | `frame0_hold_sat12_solar_wind_air_v03.png` | Seamless full-bleed `1080x1920` loop preroll matching frame 0 + end card (`What Happens When Earth's Magnetic Field Flips? / Full film on the channel`). |

---

## 4. Pasted Gate Verdicts (All 7 Gates `PASS`)

### 4.1 `gate_shorts_open.py check --air-date 2026-12-12`
```
PASS  031_short_sat12_solar_wind_air_v03.mp4  dur=24.48s  audio=-16.9dB  motion=22.13  f0diff=5.01  cut1=2.36s  vo_onset=0.09s  tail_gap=1.46s  vo_src=/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v03_vo.wav  dhash=fff7ffff7effffff  visor=0.0
   sheet /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v03_open_sheet.jpg
```

### 4.2 `thumb_preview.py short --score` (Frame 0 & Custom Cover)
```
/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v03_frame0_preview.jpg
PASS  031_short_sat12_solar_wind_air_v03_frame0.jpg  saturation=136.7  near_black=0%

/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v03_cover_preview.jpg
PASS  031_short_sat12_solar_wind_air_v03_cover.jpg  saturation=145.7  near_black=0%
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
 R40     5.0s code_graphic_031_r40a_never_ ok
 R41     8.0s hdev_earth_views_iss_2019.mp ok
R42a    11.0s hdev_earth_views_iss_2019.mp ok
R42b    14.7s nasa_svs_12312_dscovr_epic_e ok
R44a    18.3s PIA00407.jpg                 ok
R44b    21.5s code_graphic_031_r44c_durati ok
R39_loop    23.8s frame0_hold_sat12_solar_wind WARN low detail: edge density 0.0325 < film p5 0.0355
polish gate PASS: 0 of 9 rows failed, 1 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v03_polish_gate.json

WARN   0:24 row R39_loop frame0_hold_sat12_solar_wind_air_v03.png: low detail: edge density 0.0325 < film p5 0.0355
picture QA PASS: 0 of 9 cuts fail, 1 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v03_picture_qa/PICTURE_QA.md, /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v03_picture_qa/picture_qa_review.jpg
```
