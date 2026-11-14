# J2550 — Short 2 of 3: Muons (`rvug71d7Dqk`, `fri06_muons_ground_v05.mp4`)

Delivery and 5-part review evidence for Short 2 of `J2550` (`OWB:024`, Muons, `rvug71d7Dqk`, airs Sat 21 Nov 2026 11:30 London; watch card due Thu 19 Nov 2026 18:00 London), implementing the Chief rulings on `J2545`, `J2550`, and `J2829`. **£0 spent.** Nothing uploaded, nothing modified in YouTube Studio, `UPLOADS.json`, or Buffer; `fri06_muons_ground_v04.mp4` (`06b935f706c8ac3b1ac4d576d22a20193eb0fd742047f36f0be534b7604b0554`) is preserved untouched.

---

## 1. Hashes, Safety Copies & Audio Measurements

- **Base cut (`v04`, preserved untouched):** `02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/10_Shorts/fri06_muons_ground/06_Final-Exports/fri06_muons_ground_v04.mp4` (`22.20 s`, SHA-256 `06b935f706c8ac3b1ac4d576d22a20193eb0fd742047f36f0be534b7604b0554`, verified against `00_Brand/Channel-Setup/social/UPLOADS.json`).
- **Delivered `v05` master:** `fri06_muons_ground_v05.mp4` (`22.20 s`, `1080×1920`, `30 fps` CFR, `666` frames, SHA-256 `1232cb5041f9aae09e51cbf3895136142e19af379331e2b93a8607d593b331b8`).
- **Safety copies (SHA-256 verified in `safety_copies_v05.json`):**
  - NAS UAT: `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/J2550_muons_v05/fri06_muons_ground_v05.mp4`
  - iCloud UAT: `OWB UAT/J2550_muons_v05/fri06_muons_ground_v05.mp4`
  - Mini exports folder: `02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/10_Shorts/fri06_muons_ground/06_Final-Exports/fri06_muons_ground_v05.mp4`
- **Locked stems (`_work_v02/`):** Identical VO (`55` words, `0.08–20.88 s`), music bed (`light-speed_score_bed_v01_full.mp3`), SFX stem, duration (`22.20 s`), captions (`metres` British spelling), and clean 3-line endcard (`What Happens If / You Travel Near / Light Speed?`, no raw video ID).
- **Full `ffmpeg` decode:** `exit 0` (`0` errors, `0` warnings).
- **Loudness (`ebur128=peak=true`):** Integrated `-14.2 LUFS`, True Peak `-1.9 dBFS`.

---

## 2. Full-Frame 9:16 Shot Schedule (`cuts_v05.json`, `pool_v05.json`)

Every segment replaces `v04`'s `portrait_vf` feathered blur-pad with true full-bleed `9:16` framing (`612×1088` vertical crops from the `3840×2160` 4K ESA Alexander Gerst ISS orbital reel `Gerst_Earth_timelapses_2017.webm`, upscale `1.765× < 2.0×`):

| Row | Window (s) | Source | Offset / Mode | Upscale | Scene & Spoken Beat |
|---|---|---|---:|---:|---|
| `s01_gerst` | `0.00–3.00` | `Gerst_Earth_timelapses_2017.webm` | `ss=39.0 s`, `612×1088` | `1.765×` | Sunlit Earth cloud deck & blue limb (`THEY / LIVE`; `"Particles from space are passing through you."`) |
| `s02_graphic` | `3.00–6.80` | `code_graphic_024_fri06_muons_v05_scale.mp4` | `ss=12.0 s` aurora + animated cyan/gold muon streaks | `1.000×` | Animated falling muon tracks over real ISS green aurora (`"They shouldn't get here. Muons are born high up and"`) |
| `s03_gerst` | `6.80–10.60` | `Gerst_Earth_timelapses_2017.webm` | `ss=96.0 s`, `612×1088` | `1.765×` | Docked ISS craft & Canadarm2 over deep blue ocean (`"live two millionths of a second, barely six hundred"`) |
| `s04_gerst` | `10.60–14.40` | `Gerst_Earth_timelapses_2017.webm` | `ss=148.0 s`, `612×1088` | `1.765×` | Twilight coastline & city lights (`Muons Shouldn't / Reach the Ground. / They Do.`; `"metres of flight. At nearly light speed, their clocks run"`) |
| `s05_gerst` | `14.40–18.20` | `Gerst_Earth_timelapses_2017.webm` | `ss=114.0 s`, `612×1088` | `1.765×` | Dense golden night city lights from orbit (`"slow, so they reach the ground. The full film:"`) |
| `s06_gerst` | `18.20–22.20` | `Gerst_Earth_timelapses_2017.webm` | `ss=290.0 s`, `612×1088` | `1.765×` | Sunlit Canadarm2 over bright clouds & turquoise desert lakes (`What Happens If / You Travel Near / Light Speed?`) |

---

## 3. All Five Automated Shorts Gates (Without Report-Only)

- **`gate_shorts_open.py` (`exit 0`):**
  ```text
  PASS  fri06_muons_ground_v05.mp4  dur=22.2s  audio=-17.6dB  motion=29.49  f0diff=6.14  cut1=3.0s  vo_onset=0.08s  tail_gap=1.32s  vo_src=/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/10_Shorts/fri06_muons_ground/_work_v02/stem_vo.wav  dhash=00eae8d3e5cc557d  visor=0.0
     full-bleed 0.00s  fills the frame  sharp above/middle/below=0.226/0.488/0.093  detail top/centre/bottom=8.27/2.76/1.11  spread top/bottom=35.21/6.45
     full-bleed 0.25s  fills the frame  sharp above/middle/below=None/0.779/None  detail top/centre/bottom=8.46/4.47/0.97  spread top/bottom=36.32/5.77
     full-bleed 0.50s  fills the frame  sharp above/middle/below=None/0.772/None  detail top/centre/bottom=8.3/4.6/4.67  spread top/bottom=34.5/11.68
     full-bleed whole Short  0/23 frames padded at one a second, 0/45 at two a second  padded stretches: none  end card 16.9-22.2s judged apart
  ```
- **`sfx_kit.py level` (`exit 0`):** `SFX level PASS: VO -19.3 LUFS, SFX -42.3 LUFS, 2 hits`
- **`music_gate.py` (`exit 0`):** `music gate PASS: light-speed_score_bed_v01_full.mp3, 526.0 s, about 150.0 BPM, brief Pace: 72-88 BPM`
- **`polish_gate.py` (`exit 0`):** `polish gate PASS: 0 of 6 rows failed, 1 to look at` (`s02_graphic` smooth green aurora edge density `0.0282 < p5 0.0306`, above `EDGE_FLOOR`).
- **`picture_qa.py` (`exit 0`):** `picture QA PASS: 0 of 6 cuts fail, 2 to look at` (`s02_graphic` smooth aurora warning + `s03_gerst` `15.4s in a row` container-name warning across four distinct orbital passes changing every `3.8–4.0 s`).

---

## 4. J2829 5-Part Multimodal Verification (`gemini`)

1. **Automated gates:** All 5 gates + `ffmpeg` decode PASS (`exit 0`).
2. **Full `0.5 s` (`2 fps`) grid (`fri06_muons_ground_v05_2fps.jpg`, `0.0–22.0 s`):** All 45 tiles inspected; 100% full-bleed `9:16`, zero blur-pad, zero raw video IDs, clean house typography (`THEY / LIVE`, `Muons Shouldn't / Reach the Ground. / They Do.`, `What Happens If / You Travel Near / Light Speed?`, and all 22 captions).
3. **Every cut (`±3` frames, `muons_v05_cuts_pm3.jpg`) & final `3.0 s` all-frames (`muons_v05_tail_3s_all_frames.jpg`, `f576..f665`):** Every cut (`f90`, `f204`, `f318`, `f432`, `f546`) transitions cleanly with zero flash or black frame; final `90` frames glide smoothly over clouds and desert lakes (`max_identical_frame_pairs = 1` = `0.033 s`).
4. **Complete soundtrack heard (`audio_input` on `muons_v05_full_audio.mp3`, `356,115` bytes):** Verified Ben Orbit Narrator's complete 55-word narration and continuous ambient piano/pad score bed from `0.00 s` to `22.20 s` with zero clicks, pops, clipping, or dropouts.
5. **Compact moving proxy (`moving_video_input` on `360×640` `<= 1.4 MB` full and `3.0 s` tail `.mp4` proxies):** Verified continuous orbital motion, animated falling muon streaks (`3.0–6.8 s`), and clean endcard fade-out.
