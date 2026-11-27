# Gate Report — `064_short01_testA_opening_v02` (`J3903`)

- **Date:** 2026-11-27
- **Builder:** `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/10_Shorts/short01_testA_opening/_build_064_short01_testA_v02.py`
- **Canonical NAS Master (`v02`):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/10_Shorts/short01_testA_opening/06_Final-Exports/064_short01_testA_opening_v02.mp4`
- **SHA-256 (`v02`):** `8b7a218c73b1c790f722f4410e67e4fe04d7e06276e3d4a4bbcbceed38c38968`
- **Preserved Prior Draft (`v01` untouched on NAS):** `064_short01_testA_opening_v01.mp4` (`b805c51d02acd0e43adf9c9645c993c91d148641e068e918d93136e20b25a4b6`)
- **Format:** `1080×1920`, `24/1` CFR (`libx264`, `yuv420p`, High@4.1, `+faststart`), `738` frames (`30.750 s`), AAC `48 kHz` stereo `256k` (`I = -14.10 LUFS`, `TP = -2.10 dBTP`)
- **Result:** **7/7 automated gates PASS (`rc=0`) + Canonical 13-bed MP3 music uniqueness check PASS (`rc=0`, 0 warnings)**

## 1. `gate_shorts_open.py check` (canonical NAS copy, `--air-date 2026-12-28`, gate-check date only)

```text
PASS  064_short01_testA_opening_v02.mp4  dur=30.75s  audio=-16.1dB  motion=13.32  f0diff=5.66  cut1=2.5s  vo_onset=0.07s  tail_gap=1.11s  vo_src=/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/10_Shorts/short01_testA_opening/06_Final-Exports/064_short01_testA_opening_v02_vo.wav  dhash=c4170f2f6f2e89c7  visor=0.0
   full-bleed 0.00s  fills the frame  sharp above/middle/below=0.271/0.72/0.292  detail top/centre/bottom=8.78/10.21/3.28  spread top/bottom=44.46/8.51
   full-bleed 0.25s  fills the frame  sharp above/middle/below=0.28/0.724/0.316  detail top/centre/bottom=9.02/10.31/3.36  spread top/bottom=44.56/8.51
   full-bleed 0.50s  fills the frame  sharp above/middle/below=0.277/0.724/0.314  detail top/centre/bottom=8.97/10.41/3.43  spread top/bottom=44.56/8.61
   full-bleed whole Short  0/31 frames padded at one a second, 0/62 at two a second  padded stretches: none  end card 29.8-30.8s judged apart
   warn  duration 30.75s outside 16.0–19.0s band
   sheet /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/10_Shorts/short01_testA_opening/06_Final-Exports/064_short01_testA_opening_v02_open_sheet.jpg
```
*(Duration warning is expected and explicitly exempt for Test A Opening Shorts per `studio/RULES.md` Lesson 5: 30–38 s reframed opening.)*

## 2. `thumb_preview.py short --score`

```text
PASS  064_short01_testA_opening_v02_frame0.jpg  saturation=118.3  near_black=1%
PASS  064_short01_testA_opening_v02_cover.jpg   saturation=145.3  near_black=1%
```

## 3. `sfx_kit.py level`

```text
SFX level PASS: VO -16.0 LUFS, SFX -40.6 LUFS, 6 hits
```

## 4. `music_gate.py` (default + canonical 13-bed NAS MP3 uniqueness check)

```text
music gate PASS: every_planet_score_bed_v01.mp3, 701.9 s, about 70.6 BPM, brief Pace: 68-76 BPM
```
*(Supplemental canonical uniqueness check against all 13 other readable NAS OWB `.mp3` beds in `064_short01_testA_opening_v02_music_gate_canonical_mp3.txt`: **PASS (`rc=0`, 0 warnings)**.)*

## 5. `polish_gate.py` (canonical NAS copy)

```text
R01a     1.2s code_graphic_064_short1_r01a ok
R01b     3.5s PIA17386.jpg                 ok
R01c     5.5s PIA16853.jpg                 ok
R02a     7.3s PIA19411.jpg                 ok
R02b     9.1s PIA19411.jpg                 ok
R03a    12.1s PIA15162.jpg                 ok
R03b    15.2s code_graphic_064_short1_r03b ok
R03c    18.2s PIA17386.jpg                 ok
R03d    21.8s code_graphic_064_short1_r03d ok
R04a    25.0s PIA11364.jpg                 WARN low detail: edge density 0.1087 < film p5 0.1129
R04b    28.1s PIA16853.jpg                 ok
R01_loop    30.2s frame0_return_064_short01_te ok
polish gate PASS: 0 of 12 rows failed, 1 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/10_Shorts/short01_testA_opening/06_Final-Exports/064_short01_testA_opening_v02_polish_gate.json
```

## 6. `picture_qa.py` (canonical NAS copy)

```text
WARN   0:03 row R01b PIA17386.jpg: kind of picture: 'Enhanced Color Mercury Map (MESSENGER global surface)' (map), look at it full size
WARN   0:07 row R02a PIA19411.jpg: kind of picture: 'Water Ice on Mercury (MESSENGER north polar mosaic)' (mosaic), look at it full size
WARN   0:09 row R02b PIA19411.jpg: kind of picture: 'Water Ice on Mercury (MESSENGER north polar mosaic)' (mosaic), look at it full size
WARN   0:18 row R03c PIA17386.jpg: kind of picture: 'Enhanced Color Mercury Map (MESSENGER global surface)' (map), look at it full size
WARN   0:25 row R04a PIA11364.jpg: low detail: edge density 0.1087 < film p5 0.1129
picture QA PASS: 0 of 12 cuts fail, 5 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/10_Shorts/short01_testA_opening/06_Final-Exports/064_short01_testA_opening_v02_picture_qa/PICTURE_QA.md
```
All 5 WARN frames plus transition stills (`0.00, 1.50, 9.50, 13.50, 14.30, 15.80, 22.80, 26.80 s`) were visually inspected full-size: authentic NASA MESSENGER Mercury surface/polar plates and single-globe crop (`PIA11364` top-right globe only, no 2×2 quad), razor-sharp, full-bleed, zero title/graphic collision, zero artifacts.

## 7. `orbit_cfr_delivery.assess_playback_health` (canonical NAS copy)

- `ok: true`, `variable_frame_rate: false`, `videotoolbox: false`, `r_frame_rate: "24/1"`, `avg_frame_rate: "24/1"`, `pix_fmt: "yuv420p"`, `encoder: "Lavc63.1.101 libx264"`, `width: 1080`, `height: 1920`, `audio_codec: "aac"`, `audio_rate: 48000`, `audio_channels: 2`, `video_duration: 30.75`, `audio_duration: 30.7`, `errors: []`, `warnings: []`.
