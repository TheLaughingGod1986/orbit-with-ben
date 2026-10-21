# 027 rough v01m audio fix: music bed + house SFX (J0793, 21 Oct 2026)

Ben watched `OWB UAT/027_EarthSpin_rough_v01l.mp4` and flagged *"No music"* and *"No sound effects"*.

## 1. What happened in v01l (ffprobe + 30 s window loudness)

- **Streams (`ffprobe`):** Video `h264` 1920×1080 30 fps (446.233 s), Audio `aac` 48 kHz stereo 256 kbps (446.300 s). The audio track was copied unchanged from `v01j` → `v01k` → `v01l` (`041653dff8a90d3daeb98378b8152e8c`).
- **Why no music was heard:** It was **a bed mixed too low to hear** (not missing, and not the wrong file). In `v01j`, `earth-spin_score_take2_straight_v01j.wav` was built by applying a flat `-22 dB` attenuation to the `-17.5 LUFS` time-fit take (`earth-spin_score_bed_v02_fit.wav`), dropping the bed stem to **`-39.5 LUFS` integrated**. Across 30 s windows, the bed sat **`-22.5 to -32.6 dB` below the VO** (`-37.5 to -47.8 dB RMS` vs VO `-13.1 to -15.4 dB RMS`), which is practically inaudible on phone/laptop speakers and caused `music_gate`'s beat tracker to lose the pulse (`WARN pace: 54.5 BPM`).
- **Why no sound effects were heard:** `stem_sfx_v01i.wav` (`-32.5 LUFS`) had only 15 cues (8 ticks on the open and chapter 5 pill overlays, 4 pass whooshes, 4 rumbles). It had **zero whooshes on any of the 5 chapter cards** and **zero ticks on any of the 9 code-graphic number/label reveals** across chapters 1–4, leaving a 4-minute stretch (`90–356 s`) with almost no SFX at all.

## 2. How v01m fixes both (`_mix_earth_spin_v01m.py`, £0 spend)

- **Score bed (`05_Music/earth-spin_score_take2_straight_v01j.wav`):** Laid from the Chief-approved take-2 time-fit bed (`earth-spin_score_bed_v02_fit.wav`, `BED_BRIEF_take2.md`, Pace 76–88 BPM) using 024's J0079 envelope-ducking method: `-11.5 dB` base gain so the music rises in VO pauses, smoothly ducked across 100 ms windows during speech so `VO_M - Bed_M >= 11.3 LU` everywhere.
  - Integrated bed loudness: **`-31.9 LUFS`** (`+7.6 LU` louder than v01l).
  - Across all fifteen 30 s windows, the bed sits **`-15.7 to -22.8 dB` below VO** (`-16 to -20 dB` during normal chapters, `-22.4 to -22.8 dB` in the quiet intro and slow-stop transition).
  - Measured tempo on the laid bed is now **`80.0 BPM`** (right inside the brief's `Pace: 76-88 BPM`, clearing the old 54.5 BPM warning).
- **House SFX (`06_Sound-Effects/stem_sfx_v01m.wav`):** Synthesised via `scripts/sfx_kit.py make` (`kit_v01`, £0) with **30 cues** (`28` EBU R128 hits, integrated **`-29.8 LUFS`**, `+2.7 LU` louder than v01l):
  - **5 chapter-card whooshes:** `0:23.1` (The Sudden Stop), `1:33.4` (The Speed You Cannot Feel), `2:55.2` (A Slow Stop), `4:08.2` (Earth Is Already Slowing), `5:56.6` (Keeping Score).
  - **4 orbital/time-lapse pass whooshes:** `0:12.9`, `1:13.9`, `3:45.5`, `6:54.6`.
  - **17 number/label ticks:** all 8 edit pill/timeline dates (`0:06.9`, `6:02.0`, `6:12.5`, `6:16.7`, `6:22.6`, `6:36.9`, `6:42.4`, `7:14.5`) plus all 9 code-graphic number/label reveals (`0:35.5`, `0:39.7`, `1:02.3`, `2:12.0`, `3:11.0`, `3:14.7`, `3:25.1`, `4:29.3`, `5:51.8`).
  - **4 low rumbles:** `0:32.0` (supersonic winds), `0:44.6` (ocean surge), `6:25.6` (molten core), `7:11.4` (early Earth).
- **Picture:** Copied bit-for-bit (`-c:v copy`) from `027_EarthSpin_rough_v01l.mp4` (corner credits and fine grain preserved unchanged).

## 3. 30 s Window Comparison (v01l vs v01m)

| Window | VO RMS (dB) | v01l Bed RMS (Bed − VO) | v01m Bed RMS (Bed − VO) | v01l SFX Peak | v01m SFX Peak |
|---|---:|---:|---:|---:|---:|
| 0–30 s | -15.2 | -47.8 (-32.6 dB) | -38.0 (-22.8 dB) | -12.5 dB | -10.0 dB |
| 30–60 s | -14.8 | -42.0 (-27.2 dB) | -32.8 (-18.0 dB) | -17.5 dB | -9.9 dB |
| 60–90 s | -14.6 | -39.0 (-24.4 dB) | -31.4 (-16.8 dB) | -23.0 dB | -10.0 dB |
| 90–120 s | -15.4 | -37.9 (-22.5 dB) | -31.1 (-15.7 dB) | silent | -20.5 dB |
| 120–150 s | -14.4 | -37.7 (-23.3 dB) | -30.7 (-16.3 dB) | silent | -10.0 dB |
| 150–180 s | -14.4 | -37.5 (-23.1 dB) | -31.1 (-16.7 dB) | silent | -20.5 dB |
| 180–210 s | -14.5 | -37.5 (-23.0 dB) | -30.9 (-16.4 dB) | silent | -10.0 dB |
| 210–240 s | -15.4 | -42.7 (-27.3 dB) | -33.5 (-18.1 dB) | -23.0 dB | -21.5 dB |
| 240–270 s | -14.3 | -43.1 (-28.8 dB) | -36.7 (-22.4 dB) | silent | -10.0 dB |
| 270–300 s | -14.3 | -38.8 (-24.5 dB) | -31.3 (-17.0 dB) | silent | silent |
| 300–330 s | -14.6 | -38.7 (-24.1 dB) | -30.8 (-16.2 dB) | silent | silent |
| 330–360 s | -14.0 | -38.8 (-24.8 dB) | -30.9 (-16.9 dB) | silent | -10.0 dB |
| 360–390 s | -13.6 | -39.5 (-25.9 dB) | -32.0 (-18.4 dB) | -12.5 dB | -10.0 dB |
| 390–420 s | -13.1 | -41.7 (-28.6 dB) | -33.0 (-19.9 dB) | -12.5 dB | -10.0 dB |
| 420–446 s | -14.0 | -44.1 (-30.1 dB) | -34.3 (-20.3 dB) | -12.2 dB | -9.7 dB |

## 4. Gate Verdicts

- `sfx_kit.py level`: **PASS** (`SFX level PASS: VO -14.2 LUFS, SFX -29.8 LUFS, 28 hits`, 0 speech/pause/bed fails).
- `music_gate.py`: **PASS** (`music gate PASS: earth-spin_score_take2_straight_v01j.wav, 446.3 s, about 80.0 BPM, brief Pace: 76-88 BPM`; Chief waiver `music_gate_v01j_chief_waiver.json` applied for the short Mars stem).
- `picture_qa.py`: **PASS** (`0 of 88 cuts fail, 40 to look at`).
- `polish_gate.py`: **PASS** (`0 of 88 rows failed, 5 to look at`).
- Full mix: **`-13.9 LUFS` integrated, `-1.2 dBTP` true peak**, duration `446.300 s`.
- Masters (`sha256: 499e8edc06910cb646006a260fccbbbd9b9bc9e975f39940b0cbec2fc457b31d`):
  - `OWB UAT/027_EarthSpin_rough_v01m.mp4`
  - `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/027_EarthSpin_rough_v01m.mp4`
