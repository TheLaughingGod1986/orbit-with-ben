# Gate Report — `064_short01_testA_opening_v03` (`J3922`, ref `J3918` / `J3903`)

- **Date:** 2026-11-27
- **Builder:** `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/10_Shorts/short01_testA_opening/_build_064_short01_testA_v03.py`
- **Canonical NAS Master (`v03`):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/10_Shorts/short01_testA_opening/06_Final-Exports/064_short01_testA_opening_v03.mp4`
- **Master SHA-256 (`v03`):** `538464b9addf45088affe5e09146cec7324351d2e18552a41d66bb4d89bac402`
- **Audio Stems & SRT SHA-256 (`v03`):**
  - VO stem (`064_short01_testA_opening_v03_vo.wav`): `8483ba3e5448c5506598149ad9f2b4fe33a80ce66ae05b9d30f0f2f4aa8d7393` (`-16.1 LUFS`)
  - Score bed stem (`064_short01_testA_opening_v03_bed.wav`): `7bb8302b7fbd219aecfcb50d84a13298169ab5c4c0ac64eb1f4830460dbd02dd` (`-34.1 LUFS`)
  - SFX stem (`064_short01_testA_opening_v03_sfx.wav`): `f4f13e907d76b5f6d7781396e770c3d4e809312a60976edf1ce710908135891c` (`-40.6 LUFS`)
  - Captions (`064_short01_testA_opening_v03_en-GB.srt`): `a61a737048188667682e566a9f7ec78e08ca704dd836db231d86c6d2207fa603`
  - Frame 0 (`064_short01_testA_opening_v03_frame0.jpg`): `0e05827a32f3097658a33ce1d57c6edc0a26035dbf7715d738ba4dd9d6c41a2c`
  - Cover (`064_short01_testA_opening_v03_cover.jpg`): `0e5b993776582f461091268acec11f8c4a34c8a320428605898ae7b884a3054e`
- **Preserved Prior NAS Masters (verified untouched before & after build):**
  - `v01`: `064_short01_testA_opening_v01.mp4` (`b805c51d02acd0e43adf9c9645c993c91d148641e068e918d93136e20b25a4b6`)
  - `v02`: `064_short01_testA_opening_v02.mp4` (`8b7a218c73b1c790f722f4410e67e4fe04d7e06276e3d4a4bbcbceed38c38968`)
  - `v02` manifest preserved verbatim at `07_Upload-Package/PACKAGE_MANIFEST_v02.json`.
- **Format:** `1080×1920`, `24/1` CFR (`libx264`, `yuv420p`, `+faststart`, `738` frames = `30.750 s`), AAC `48 kHz` stereo `256k` (`I = -14.10 LUFS`, `TP = -2.10 dBTP`).
- **Video Stream Equivalence (`-c:v copy` from `v02`):**
  - Encoded bitstream `streamhash`: `0,v,SHA256=d7d5e684a9672dff62f5e0cfce669685549df86f6094b1eb817c495716fd40a0` (exact match to `v02`)
  - Decoded `framemd5` (`738` frames) SHA-256: `a4965b6044acedc4716847498b373e3b936d03fd4f16bd58193d60c895d14723` (exact match to `v02`)
  - *Note:* Reusing `v02`'s video stream via `-c:v copy` is solely for audio-repair efficiency under the Chief ruling on `J3918` and is **not** a visual or motion PASS; independent audio and moving-video QA remain delegated to `J3923`.
- **Result:** **7/7 automated gates PASS (`rc=0`) + Canonical 13-bed MP3 music uniqueness check PASS (`rc=0`, 0 warnings) + Speech-coverage regression (`v02` FAIL / `v03` PASS) + Fresh decoded 71-word ASR PASS (`1.00` recall, `0` diffs) + `youtube:package --dry-run` PASS (`ok: true`)**

---

## 0. Audio Defect Fix, Speech-Coverage Regression & Fresh ASR Verification

### Root Cause Repaired (`v02` → `v03`)
In `_build_064_short01_testA_v02.py`, `-ss` was placed after `-i` while `afade=t=out:st={seg - 0.008}` ran on input timestamps before output-seeking, silencing nonzero-source-offset segments S2, S3 (tail), and S4 down to the ±1 LSB PCM dither floor (`-90.31 dBFS`; bed and SFX remained in the final mix). In `_build_064_short01_testA_v03.py`, each segment is sliced with `atrim=start=...:end=...,asetpts=PTS-STARTPTS` strictly before `afade=t=in` / `afade=t=out`, then normalized (`-16.1 LUFS`), re-ducked (`bed -34.1 LUFS`), re-leveled (`SFX -40.6 LUFS`), remixed (`-14.8 LUFS`), and AAC-calibrated (`-14.10 LUFS`, `-2.10 dBTP`).

### Speech-Coverage Regression (`064_short01_testA_opening_v03_vo_coverage_regression.json`)
Compares 200 ms windows and locked-source word intervals against `every_planet_explained_vo_v01.wav` (`4b478fcd…`), allowing genuine source pauses (`src <= -45 dBFS`) and accounting for ±1 LSB PCM dither (`-90.31 dBFS`):

| Segment | Source Span (s) | Local Span (s) | `v02` Coverage / Dropouts / Missing Words / RMS | `v03` Coverage / Dropouts / Missing Words / RMS / Corr |
|---|---|---|---|---|
| **S1** | `0.060–6.600` | `0.000–6.540` | active (edge fade) | **100.0%** / `0` / `0` / `-18.81 dBFS` / `0.9983` |
| **S2** *(offset > 0)* | `7.560–11.050` | `6.600–10.090` | **FAIL:** `0.0%` / `16` / `10/10` / `-90.31 dBFS` | **100.0%** / `0` / `0` / `-19.18 dBFS` / `0.9997` |
| **S3** *(offset > 0)* | `11.890–25.140` | `10.170–23.420` | **FAIL:** `11.9%` / `49` / `31/34` / `-27.47 dBFS` | **100.0%** / `0` / `0` / `-19.36 dBFS` / `0.9993` |
| **S4** *(offset > 0)* | `26.280–32.600` | `23.440–29.760` | **FAIL:** `0.0%` / `30` / `10/10` / `-90.31 dBFS` | **100.0%** / `0` / `0` / `-18.37 dBFS` / `0.9999` |

- **Old `v02` VO stem:** `passed: false` (3/4 segments fail; proves regression catches the defect).
- **Repaired `v03` VO stem:** `passed: true` (`0` failures across all 4 segments).

### Freshly Decoded Speech ASR (`064_short01_testA_opening_v03_asr_verify.json`)
Local `faster-whisper small.en` (`int8` CPU, `local_files_only=True`) run on freshly decoded 16 kHz mono WAVs extracted directly from the muxed MP4 and VO stem:
- **`v03.mp4` (freshly decoded muxed audio):** `token_recall = 1.0000` (`75/75` normalized spoken tokens = all 71 words verified, `diffs: []`, span `0.00–29.56 s`):
  > *"On Mercury, the sun's closest planet, why does water ice survive 430 degree heat? The ice hides in polar craters that never see sunlight. At 58 million kilometers out, sunlight shines up to seven times brighter than on Earth. Yet without an atmosphere to retain heat, you would feel night plunge to minus 180 degrees Celsius. In 1965, Italian mathematician Giuseppe Colombo solved its spin mystery."*
- **`v03_vo.wav`:** `token_recall = 1.0000` (`75/75`, `diffs: []`).
- **`v02.mp4` (contrast):** `token_recall = 0.2800` (`17` ASR words, `last_word_end_s = 11.6 s`).
- *Perceptual boundary:* Automated DSP coverage and ASR do **not** replace actual listening; listening and moving-video QA are delegated to dependent capable reviewer job `J3923`.

---

## 1. `gate_shorts_open.py check` (canonical NAS copy, `--air-date 2026-12-28`, gate-check date only)

```text
PASS  064_short01_testA_opening_v03.mp4  dur=30.75s  audio=-17.0dB  motion=13.32  f0diff=5.66  cut1=2.5s  vo_onset=0.07s  tail_gap=1.11s  vo_src=/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/10_Shorts/short01_testA_opening/06_Final-Exports/064_short01_testA_opening_v03_vo.wav  dhash=c4170f2f6f2e89c7  visor=0.0
   full-bleed 0.00s  fills the frame  sharp above/middle/below=0.271/0.72/0.292  detail top/centre/bottom=8.78/10.21/3.28  spread top/bottom=44.46/8.51
   full-bleed 0.25s  fills the frame  sharp above/middle/below=0.28/0.724/0.316  detail top/centre/bottom=9.02/10.31/3.36  spread top/bottom=44.56/8.51
   full-bleed 0.50s  fills the frame  sharp above/middle/below=0.277/0.724/0.314  detail top/centre/bottom=8.97/10.41/3.43  spread top/bottom=44.56/8.61
   full-bleed whole Short  0/31 frames padded at one a second, 0/62 at two a second  padded stretches: none  end card 29.8-30.8s judged apart
   warn  duration 30.75s outside 16.0–19.0s band
   sheet /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/10_Shorts/short01_testA_opening/06_Final-Exports/064_short01_testA_opening_v03_open_sheet.jpg
```
*(Duration warning is expected and explicitly exempt for Test A Opening Shorts per `studio/RULES.md` Lesson 5.)*

## 2. `thumb_preview.py short --score`

```text
PASS  064_short01_testA_opening_v03_frame0.jpg  saturation=118.3  near_black=1%
PASS  064_short01_testA_opening_v03_cover.jpg   saturation=145.3  near_black=1%
```

## 3. `sfx_kit.py level` (canonical NAS stems)

```text
SFX level PASS: VO -16.1 LUFS, SFX -40.6 LUFS, 6 hits
```

## 4. `music_gate.py` (default + canonical 13-bed NAS MP3 uniqueness check)

```text
music gate PASS: every_planet_score_bed_v01.mp3, 701.9 s, about 70.6 BPM, brief Pace: 68-76 BPM
```
Canonical 13-bed NAS `.mp3` check (`064_short01_testA_opening_v03_music_gate_canonical_mp3.txt`): **PASS (`rc=0`, 0 warnings)**.

## 5. `polish_gate.py` (canonical NAS copy)

```text
polish gate PASS: 0 of 12 rows failed, 1 to look at -> .../064_short01_testA_opening_v03_polish_gate.json
```
(`R04a` `PIA11364.jpg` single WARN `edge density 0.1087 < film p5 0.1129`, unchanged from `v02`.)

## 6. `picture_qa.py` (canonical NAS copy)

```text
picture QA PASS: 0 of 12 cuts fail, 5 to look at -> .../064_short01_testA_opening_v03_picture_qa/PICTURE_QA.md
```
(Same 5 expected NASA map/mosaic/R04a WARNs as `v02`; 0 fails.)

## 7. `orbit_cfr_delivery.assess_playback_health` (canonical NAS copy)

- `ok: true`, `variable_frame_rate: false`, `videotoolbox: false`, `r_frame_rate: "24/1"`, `avg_frame_rate: "24/1"`, `pix_fmt: "yuv420p"`, `encoder: "Lavc63.1.101 libx264"`, `width: 1080`, `height: 1920`, `audio_codec: "aac"`, `audio_rate: 48000`, `audio_channels: 2`, `video_duration: 30.75`, `audio_duration: 30.7`, `errors: []`, `warnings: []`.

## 8. `youtube:package --dry-run` (`064_short01_testA_opening_v03_package_dry_run.txt`)

- **PASS (`ok: true`, `dryRun: true`)** against `07_Upload-Package/PACKAGE_MANIFEST.json` (`v03`) and canonical NAS `064_short01_testA_opening_v03.mp4` (`sha256: 538464b9addf45088affe5e09146cec7324351d2e18552a41d66bb4d89bac402`), `privacy: private`, `madeForKids: false`, `containsSyntheticMedia: true`, `categoryId: 28`, `contentFormat: shorts`. **No upload, scheduling, privacy, or Buffer action executed.**
