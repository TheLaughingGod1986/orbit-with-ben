# J2550 — Short 3 of 3: ISS Deorbit (`xdurJQcoiGM`, `owb_ar2_iss_2030_deorbit_v14.mp4`)

Delivery and 5-part review evidence for Short 3 of `J2550` (`OWB:030`, ISS 2030 deorbit `AR2`, `xdurJQcoiGM`, airs Wed 25 Nov 2026 11:30 London; watch card due Mon 23 Nov 2026 18:00 London), implementing the Chief rulings on `J2545`, `J2550`, and `J2829`. **£0 spent.** Nothing uploaded, nothing modified in YouTube Studio, `UPLOADS.json`, or Buffer; `owb_ar2_iss_2030_deorbit_v13.mp4` (`74aa35464bf26a6294608925a81e7a6029a82adc2c8333dc878b11311a9dac06`) is preserved untouched.

---

## 1. Hashes, Safety Copies & Audio Measurements

- **Base cut (`v13`, preserved untouched):** `00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/06_Final-Exports/owb_ar2_iss_2030_deorbit_v13.mp4` (`18.40 s`, SHA-256 `74aa35464bf26a6294608925a81e7a6029a82adc2c8333dc878b11311a9dac06`, verified against `00_Brand/Channel-Setup/social/UPLOADS.json`).
- **Delivered `v14` master:** `owb_ar2_iss_2030_deorbit_v14.mp4` (`18.40 s`, `1080×1920`, `30 fps` CFR, `552` frames, SHA-256 `e9f2c5330f4e57c066742e932774bc67d6af87399cd6ea3a53a0f6a085041287`).
- **Safety copies (SHA-256 verified in `safety_copies_v14.json`):**
  - NAS UAT: `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/J2550_iss_v14/owb_ar2_iss_2030_deorbit_v14.mp4`
  - iCloud UAT: `OWB UAT/J2550_iss_v14/owb_ar2_iss_2030_deorbit_v14.mp4`
  - Mini exports folder: `00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/06_Final-Exports/owb_ar2_iss_2030_deorbit_v14.mp4`
- **Scope of visual change:**
  - `0.000–14.767 s` (`frames 0..442`): Preserved unchanged from `v13` (already 100% full-bleed `9:16`).
  - `14.767–18.400 s` (`frames 443..551`): Replaced `v13`'s 720p Crew-2 band-over-blur shot with a full-frame `9:16` `612×1088` vertical crop (`upscale = 1.765× < 2.0×`) from the 4K ESA Alexander Gerst ISS orbital reel (`Gerst_Earth_timelapses_2017.webm` `ss = 290.0 s`, showing ISS Canadarm2 and docked hardware gliding above sunlit clouds and desert lakes), composited with the exact `J2229` captions (`SOUTH PACIFIC.`, `LOOK UP AND`, `WATCH IT CROSS`, `THE SKY.`) and mixed from the locked `J2229/ar2` VO, music-bed, and SFX stems.
- **Full `ffmpeg` decode:** `exit 0` (`0` errors, `0` warnings).
- **Loudness (`ebur128=peak=true`):** Integrated `-14.3 LUFS`, True Peak `-1.8 dBFS`.

---

## 2. All Five Automated Shorts Gates (Without Report-Only)

- **`gate_shorts_open.py` (`exit 0`):**
  ```text
  PASS  owb_ar2_iss_2030_deorbit_v14.mp4  dur=18.4s  audio=-17.5dB  motion=31.0  f0diff=7.52  cut1=2.4s  vo_onset=0.07s  tail_gap=1.24s  vo_src=/Users/benjaminoats/_desk/renders/J2229/ar2/stem_vo.wav  dhash=351dc3cb919ee9ce  visor=0.0
     full-bleed 0.00s  fills the frame  sharp above/middle/below=None/0.896/None  detail top/centre/bottom=27.3/18.26/16.7  spread top/bottom=60.8/45.53
     full-bleed 0.25s  fills the frame  sharp above/middle/below=None/0.91/None  detail top/centre/bottom=26.98/18.46/20.09  spread top/bottom=61.07/46.32
     full-bleed 0.50s  fills the frame  sharp above/middle/below=None/0.92/None  detail top/centre/bottom=26.59/18.85/20.35  spread top/bottom=61.71/46.19
     full-bleed whole Short  0/19 frames padded at one a second, 0/37 at two a second  padded stretches: none  no end card named in meta
     warn  duration 18.4s outside 22–27s band
  ```
  *(Note: `xdurJQcoiGM` is Apophis Replication Test Short `AR2`, locked at `18.40 s` under the standalone ~20 s test exception through 20 Nov 2026.)*
- **`sfx_kit.py level` (`exit 0`):** `SFX level PASS: VO -19.7 LUFS, SFX -38.1 LUFS, 4 hits`
- **`music_gate.py` (`exit 0`):** `music gate PASS: owb-standalone-shorts_score_bed_v01.mp3, 60.0 s, about 120.0 BPM, brief Pace: 84-96 BPM`
- **`polish_gate.py` (`exit 0`):** `polish gate PASS: 0 of 6 rows failed, 1 to look at` (`ar2_05_Gerst_ISS_arm_s5` bright white cloud deck relative edge density `0.0157 < film p5 0.0190`).
- **`picture_qa.py` (`exit 0`):** `picture QA PASS: 0 of 6 cuts fail, 2 to look at` (inherited `J1849` animated ISS opening + bright cloud deck warning on row 5).

---

## 3. J2829 5-Part Multimodal Verification (`gemini`)

1. **Automated gates:** All 5 gates + `ffmpeg` decode PASS (`exit 0`).
2. **Full `0.5 s` (`2 fps`) grid (`owb_ar2_iss_2030_deorbit_v14_2fps.jpg`, `0.0–18.0 s`):** All 37 tiles inspected; 100% full-bleed `9:16` (`0/19` at 1 fps, `0/37` at 2 fps), zero blur-pad, zero raw video IDs.
3. **Every cut (`±3` frames, `iss_v14_cuts_pm3.jpg`) & final `3.0 s` all-frames (`iss_v14_tail_3s_all_frames.jpg`, `f462..f551`):** All 5 cuts (`f72`, `f156`, `f245`, `f329`, and the patched splice `f442 -> f443` at `14.77 s`) transition cleanly with steady caption placement and zero flash/freeze; final `90` frames (`15.40–18.37 s`) glide smoothly across clouds and desert lakes (`max_identical_frame_pairs = 1` = `0.033 s`).
4. **Complete soundtrack heard (`audio_input` on `iss_v14_full_audio.mp3`, `295,443` bytes):** Verified Ben Orbit Narrator's complete 42-word narration and continuous arpeggiated score bed from `0.00 s` to `18.40 s` (`tail_gap = 1.24 s`) with zero clicks, pops, clipping, or dropouts.
5. **Compact moving proxy (`moving_video_input` on `360×640` `< 1.0 MB` full and `3.0 s` tail `.mp4` proxies):** Verified continuous full-frame motion across the patched `14.77 s` splice through `18.40 s`.
