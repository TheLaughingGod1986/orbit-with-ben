# J2551 — Short 2 Review (`029` Great Dimming `v06`, `SWDCZfWZVao`, Wed 9 Dec 2026)

- **Reviewer / Builder:** `gemini` (Acting Chief)
- **Date:** `2026-11-15`
- **Video ID / Schedule:** `SWDCZfWZVao` — `"Why Did Betelgeuse Suddenly Lose Two-Thirds of Its Light?"` (Wed `2026-12-09 11:30` London; watch card due `2026-12-06 18:00` London)
- **Master Export:** `02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/10_Shorts/wed09_great_dimming/06_Final-Exports/029_short_wed09_great_dimming_v06.mp4`
  - `v04_untouched_sha256` (verified before and after against `UPLOADS.json`): `e0459b017ddafdf84229784c5694507140523e92043ab2109b8f3c3` -> exact full digest `e0459b017ddafdf84229784c170285d4c5694507140523e92043ab2109b8f3c3`
  - `v06 mp4_sha256`: `5251b3fc9aace716cfef19c2354dcc4ed1aed64f5966da779ec520397f1c1982` (`20,742,002` bytes, `1080x1920`, `30 fps` CFR, `22.73 s`)
  - `frame0_jpg_sha256`: `076b6e94f8c72047f2be0327a173b85e8d77326eb9e8287eaf155d74f6ede92c`
  - `cover_jpg_sha256`: `b24b0f0dddfee433dda519cd80d65a2a5c464ea4abd959717774b88076a56b82`
  - **UAT Staged Copies (with `SHA256SUMS.json`):** `OWB UAT/029_short_wed09_great_dimming_v06/029_short_wed09_great_dimming_v06.mp4` (both studio UAT archive and iCloud `OWB UAT`)

## What Changed vs `v04` (`J2545` Padded-Shot Fix)
1. **`2.72–5.10 s` (`s02_dip_a`):** Replaced the 16:9 `code_graphic_029_r15_dip` band-over-blurred-copy with a newly rendered native upright `1080x1920` `code_graphic_029_wed_r15_dip_v06.mp4` light-curve graphic (`"that point fades"` + orange brightness dip curve drawn full-bleed inside caption-safe bounds).
2. **`12.40–15.14 s` (`s07_eject`) and remaining 16:9 plates:** Replaced padded 16:9 plates with full-bleed `1080x1920` `orion_over_paranal.mp4` (`up=1.778`), full-bleed starfield-composited VLT SPHERE / VISIR plates (`s01`, `s03`, `s06`), and smooth symmetric centre-zoomed ESO dust plates (`s08`, `s09`, `up=1.182`). Zero blurred, mirrored, or flat bands anywhere (`0/23` at 1 fps, `0/46` at 2 fps).
3. **Audio & Words Unchanged:** Identical 68-word Ben Orbit Narrator VO (`0.05–20.41 s`), identical `22.73 s` duration, identical captions, calibrated AAC loudness `I=-14.1 LUFS`, `TP=-2.0 dBTP`.

## Part 1 — Automated Gates (Non-Report-Only, All `PASS` / `rc=0`)

### `gate_shorts_open.py check`
```text
PASS  029_short_wed09_great_dimming_v06.mp4  dur=22.73s  audio=-16.9dB  motion=15.94  f0diff=4.62  cut1=2.7s  vo_onset=0.05s  tail_gap=2.32s  dhash=80310209297020f4  visor=0.0
   full-bleed 0.00s  fills the frame  sharp above/middle/below=0.591/0.736/0.176  detail top/centre/bottom=16.66/8.98/2.28  spread top/bottom=47.95/20.05
   full-bleed 0.25s  fills the frame  sharp above/middle/below=0.596/0.723/0.183  detail top/centre/bottom=16.63/8.95/2.45  spread top/bottom=47.75/23.67
   full-bleed 0.50s  fills the frame  sharp above/middle/below=0.593/0.725/0.183  detail top/centre/bottom=16.64/8.92/2.54  spread top/bottom=47.62/27.26
   full-bleed whole Short  0/23 frames padded at one a second, 0/46 at two a second  padded stretches: none  end card 20.7-22.7s judged apart
```

### `thumb_preview.py short` (`frame0` & `cover`)
```text
PASS  029_short_wed09_great_dimming_v06_frame0.jpg  saturation=59.9  near_black=3%
PASS  029_short_wed09_great_dimming_v06_cover.jpg   saturation=69.4  near_black=2%
```

### `sfx_kit.py level`, `music_gate.py`, `OCR`, `ffmpeg` Decode & Loop Diff
```text
SFX level PASS: VO -16.4 LUFS, SFX -42.0 LUFS, 1 hits
music gate PASS: betelgeuse_score_bed_v01.mp3, 542.3 s, about 75.0 BPM, brief Pace: 68-78 BPM
OCR: frames 682, hits 0 (PASS)
ffmpeg full decode: rc=0, stderr=''
loop_diff (last frame vs frame 0): 2.32 (<= 15.0 PASS)
```

### `polish_gate.py` & `picture_qa.py`
```text
s01_orion_sphere     1.3s gemini_night.jpg             ok
s02_dip_a            3.9s code_graphic_029_wed_r15_dip ok
s03_sphere_dec       6.9s sphere_dec.jpg               ok
s06_visir           10.6s visir_flames.jpg             ok
s07_eject           13.8s orion_over_paranal.mp4       ok
s08_dust_a          16.5s dust_impression.jpg          WARN low detail: edge density 0.0052 < film p5 0.0094
s09_dust_b          19.2s dust_impression.jpg          ok
s10_end             21.7s frame0_hold_wed09_great_dimm ok
polish gate PASS: 0 of 8 rows failed, 1 to look at
picture QA PASS: 0 of 8 cuts fail, 2 to look at
```

## Parts 2–5 — `J2829` Multimodal Inspection (`gemini`)
- **Part 2 (`0.5 s` / `2 fps` full-film contact sheet, 46 tiles `0.00–22.50 s`):** Inspected all 46 frames. Every shot fills `1080x1920` edge-to-edge with zero blurred/flat bands. Upright `r15_dip` curve (`2.72–5.10 s`), hook (`"LOST 2/3 OF / ITS LIGHT"`), title card (`"Is Betelgeuse / About to / Explode?"`), teach pill (`"CLOUD OF DUST"`), all captions, and the end card (`"Full film on the channel"`) are sharp, well-spaced, and clear of YouTube Shorts UI zones. Inspected `picture_qa_review.jpg` full-size on `s08_dust_a` / `s09_dust_b` (ESO artist's concept of dust cloud dimming Betelgeuse): clean, rich orange-red glow, zero artefacts.
- **Part 3 (`±3` frame splice strips at all 7 cuts + all 90 frames of final `3.0 s` `19.70–22.67 s`):** Every cut transitions cleanly between `f-1` and `f+0` with zero flash frames, black frames, or stray duplicate holds. Final `3.0 s` cuts cleanly at `20.71 s` to the frame-0 loop hold with smooth `0.28 s` end-card fade-in.
- **Part 4 (Complete soundtrack via `audio_input` on `029_short_wed09_great_dimming_v06_audio.mp3`):** Heard all `22.73 s` end-to-end. Clear, natural narration by Ben from `"Betelgeuse, normally one of the ten brightest stars in the sky..."` through `"...just blocked our view."` (`20.41 s`), subtle SFX ticks, clean score ducking, and smooth piano ring-out through `22.73 s` with zero clicks, clipping, or truncation.
- **Part 5 (Moving video proxy `029_short_wed09_great_dimming_v06_proxy_full_360x640.mp4`, `1.21 MB`):** Watched complete `22.73 s` moving cut. Smooth starfield parallax, crisp animated brightness dip curve, real Paranal night-sky motion at `12.40–15.14 s`, smooth dust push-in, and clean loop back to frame 0.

**Verdict:** **PASS** — Ready for Ben's UAT watch card (`SWDCZfWZVao`, due `2026-12-06 18:00` London).
