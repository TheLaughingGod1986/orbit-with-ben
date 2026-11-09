# J2385 — Moving-Video QA Review of £0 R01 97.77° Sourced Composite & R55 3-Cut Cloud Passage (OWB 033 Uranus)

- **Job**: `J2385` (`033: watch £0 R01 composite and R55 cloud passage against J2334 scope`, `kind: qa`, `film: 033`, `stage: picture`, `requires: moving_video_input`, `needs: mini`)
- **Reviewer**: `gemini` (`gemini-argon` / `gemini-agy`, with demonstrated native `moving_video_input` via `read_file` on `video/mp4`)
- **Date**: `2026-11-08T05:48Z`
- **Upstream References**:
  - `J2334` (`jobs/reviews/J2334/CHIEF_RULING.md`, commit `4ddd1058a0`)
  - `J2384` (`jobs/reviews/J2384/BUILD_REPORT.md`, commit `6ba68b05d8`)
- **Overall Verdict**: **PASS** (`R01` `r01_sourced_composite_v01_silent.mp4` **PASS**, `R55` `r55_passage_v01_silent.mp4` [Cuts 1, 2, 3] **PASS**, `£0.00` spend, `0` credits, `0` AI takes).

---

## 1. Demonstrated `moving_video_input` & Hash Verification

All NAS-delivered MP4 files under `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/04_Generated-Clips/J2334_fix/` and full-size review sheet `picture_qa_review.jpg` were ingested and watched directly via `read_file` (`video/mp4` and `image/jpeg`) during `J2385`:

| Asset | NAS Path Watched (`read_file` `video/mp4`) | SHA-256 | Stream / Frames / Duration | Motion (`mean` / `min` / `max` diff, `frozen_pairs`) | Verdict |
|---|---|---|---|---|---|
| `r01_sourced_composite_v01_silent.mp4` | `.../J2334_fix/r01_sourced_composite_v01_silent.mp4` | `aab9aa2af9dd8cd50195a0b91efe495abaf9f06be2daf72bd893014b56503e6d` | `1920x1080`, `24/1` fps, `144` frames (`6.0000 s`; active window `0.40–4.75 s` = `4.35 s`), `1` video / `0` audio | `1.1236` (`0.9353` / `1.1764`), `frozen_pairs = 0` | **PASS** |
| `r55_cut1_r55b_100x_silent.mp4` | `.../J2334_fix/r55_cut1_r55b_100x_silent.mp4` | `df6d92d5977fb7fdc6811f43918122abd08eed5f8f825fe67e0299d367808e8a` | `1920x1080`, `24/1` fps, `95` frames (`3.9583 s`, `493.010–496.968 s`), `1` video / `0` audio | `6.4906` (`5.3124` / `7.5914`), `frozen_pairs = 0` | **PASS** |
| `r55_cut2_r55b_128x_vortex_silent.mp4` | `.../J2334_fix/r55_cut2_r55b_128x_vortex_silent.mp4` | `75adc0df000568f359bb3b32c9f29ec6eb545f57fa204ce255b5632ec74edeb4` | `1920x1080`, `24/1` fps, `95` frames (`3.9583 s`, `496.968–500.927 s`), `1` video / `0` audio | `7.0018` (`4.7520` / `8.5514`), `frozen_pairs = 0` | **PASS** |
| `r55_cut3_pia01488_pushin_silent.mp4` | `.../J2334_fix/r55_cut3_pia01488_pushin_silent.mp4` | `3b606e6edf81365422f782643451d8479e45c4d7a7fab3e23661066b43e2647b` | `1920x1080`, `24/1` fps, `106` frames (`4.4167 s`, `500.927–505.350 s`), `1` video / `0` audio | `2.5302` (`2.4634` / `2.5534`), `frozen_pairs = 0` | **PASS** |
| `r55_passage_v01_silent.mp4` | `.../J2334_fix/r55_passage_v01_silent.mp4` | `4aa82d0e721988513eba44c38332b5537a9d6f41f9f406ab5d9623b04642483f` | `1920x1080`, `24/1` fps, `296` frames (`12.3333 s`, `493.010–505.350 s`), `1` video / `0` audio | `5.6313` (`2.4673` / `77.5851`), `frozen_pairs = 0` | **PASS** |

---

## 2. Detailed Visual & Technical Gate Assessment Against `J2334` Scope

### 2.1 `R01` (`0.00–4.35 s` — `r01_sourced_composite_v01_silent.mp4`, SHA-256 `aab9aa2af9dd8cd50195a0b91efe495abaf9f06be2daf72bd893014b56503e6d`)
- **VO Line**: *"One planet in our solar system rotates almost completely on its side."* (`0.00–4.35 s`; followed by `R02` `4.35–8.18 s` *"Its north pole faces the Sun for twenty-one Earth years straight..."*).
- **Astronomical Accuracy (`97.77°` Sideways Axial Tilt & Upright Rings)**:
  - **PASS**: Watched full-frame across `00:00–00:05` via `moving_video_input` and inspected full-size on `picture_qa_review.jpg`. Unlike the rejected `J2332` `r01_flow_t1_silent.mp4` (which depicted a Saturnian horizontal ring belt at `~17°` tilt), `r01_sourced_composite_v01_silent.mp4` shows the real Voyager 2 cyan Uranus disc (`PIA18182`, `3dcc83114f...`) with its spin axis tilted `97.77°` (`7.77°` below horizontal) and its 13 narrow, faint concentric rings (`weic2310a`, `e5f7a1a0e1...`) standing nearly vertically (`7.77°` from vertical). Rear ring arcs are properly occluded behind the cyan globe and front ring arcs cross cleanly in front of the disc.
- **24fps Continuous Motion & Upscale (`<= 2.35x`)**:
  - **PASS**: Smooth 24fps orbital push-in (`1.00x -> 1.08x`) with 3-plane `#050814` starfield parallax and subtle atmospheric rotation (`mean_frame_diff = 1.1236 >= 0.35`, `min_frame_diff = 0.9353`, `frozen_pairs = 0`). Source resolution `1720x1720` (`PIA18182`) and `1400x1400` (`weic2310a`) sit at `<= 1.20x` effective scale (`<= 2.35x` lock).
- **Framing, Disclosure & First-30s Rule**:
  - **PASS**: Zero explanatory text in `0–3 s`, zero text over the planet or rings, and clean lower-left Didot italic credit `NASA / JPL / ESA / CSA / STScI (composite)`. `svs20390` is excluded. Separated from `R03` (`CODE` `8.18–13.37 s`) by `R02` (`4.35–8.18 s` Voyager 2 `PIA01391`).

### 2.2 `R55` (`493.01–505.35 s` — `r55_passage_v01_silent.mp4`, SHA-256 `4aa82d0e721988513eba44c38332b5537a9d6f41f9f406ab5d9623b04642483f`)
- **VO Line**: *"With no solid surface to land on, a descending probe would simply sink through the clouds until extreme pressure and heat crushed it."* (`493.01–505.35 s`, `12.34 s`).
- **Cut-by-Cut Moving-Video Verification**:
  1. **Cut 1 (`493.010–496.968 s`, `3.958 s`, `95` frames — `r55_cut1_r55b_100x_silent.mp4`, `df6d92d597...`)**:
     - **PASS**: Uses accepted `r55b_flow_t1_silent.mp4` (`1e71287f9a...`) offset `0.000–3.958 s` at `1.00x` full frame (`1280x720 -> 1920x1080` = `1.50x <= 2.35x` upscale). Shows deep cyan-aquamarine cyclonic cloud bands swirling continuously (`mean_frame_diff = 6.4906`, `frozen_pairs = 0`) with no solid surface. Immediately follows `R54` (`487.24–493.01 s` `CODE` chart `code_graphic_033_r54_core_vs_cloud_temp.mp4`), ensuring strict **chart-to-moving-world-plate** separation across `R54 -> R55`.
  2. **Cut 2 (`496.968–500.927 s`, `3.958 s`, `95` frames — `r55_cut2_r55b_128x_vortex_silent.mp4`, `75adc0df00...`)**:
     - **PASS**: Uses accepted `r55b_flow_t1_silent.mp4` (`1e71287f9a...`) offset `3.958–7.917 s` with a `1.28x` vortex-centre framing crop (`1000x562 -> 1920x1080` = `1.92x <= 2.00x` upscale). Watched across the `00:03 -> 00:04` boundary in `r55_passage_v01_silent.mp4`: the `1.28x` crop produces an unmistakable visual cut at `496.968 s` into the eye of the cyan vortex (`mean_frame_diff = 7.0018`, `frozen_pairs = 0`, `0` replayed frames, `picture_qa.py` `reuse_checks` PASS).
  3. **Cut 3 (`500.927–505.350 s`, `4.417 s`, `106` frames — `r55_cut3_pia01488_pushin_silent.mp4`, `3b606e6edf...`)**:
     - **PASS**: Uses verified NASA Voyager 2 upper-atmosphere plate `PIA01488` (`9c49e13d8d...`, `2118x2618`, `1.00x` native > `1080p` scale) showing the deep blue-green atmospheric haze limb over `#050814` navy starry space with fine grain and a smooth constant-velocity camera glide (`mean_frame_diff = 2.5302`, `frozen_pairs = 0`, `jitter.max_off_trend_px = 0.112 <= 0.35`, `jitter.reversals = 0`). Inspected full-size on `picture_qa_review.jpg`: the vintage 1986 JPL print halftone grid is cleanly de-screened while preserving natural Voyager 2 atmospheric limb graduation and sharp background starfield detail (`std = 43.52 >= 18.0`, `edge = 0.0343 >= 0.0259`).
- **4–6 s Picture-Change Cadence & No Static Hold `> 4 s`**:
  - **PASS**: All three cuts (`3.958 s`, `3.958 s`, `4.417 s`) sit cleanly within the `<= 4–6 s` picture-change rule (`mean = 4.11 s`), with continuous 24fps motion throughout (`0` static holds).

---

## 3. Pasted `polish_gate.py` & `picture_qa.py` PASS Outputs

### 3.1 `scripts/polish_gate.py` (`PASS`)
```text
   1     2.2s r01_sourced_composite_v01_si ok
  55     6.3s r55b_flow_t1_silent.mp4      ok
  55    10.3s r55b_flow_t1_silent.mp4      ok
  55    14.5s PIA01488.jpg                 WARN low detail: edge density 0.0343 < film p5 0.0358
polish gate PASS: 0 of 4 rows failed, 1 to look at -> /Users/benjaminoats/_desk/cache/J2384_work/polish_gate.json
```
*(Full-size visual inspection of the single non-failing `p5` relative-percentile notice on `PIA01488.jpg` in `picture_qa_review.jpg` **PASSES**: `std = 43.52 >= 18.0`, `edge = 0.0343 >= 0.0259` absolute floor, `mean = 45.17 >= 28.0`, `p95 = 159.0 >= 50.0`, `jitter.max_off_trend_px = 0.112 <= 0.35`, `reversals = 0`.)*

### 3.2 `scripts/picture_qa.py` (`PASS`)
```text
WARN   0:02 row 1 r01_sourced_composite_v01_silent.mp4: kind of picture: 'Voyager 2 PIA18182 + JWST NIRCam weic2310a Uranus 97.77-deg sideways composite' (composite), look at it full size
WARN   0:14 row 55 PIA01488.jpg: low detail: edge density 0.0343 < film p5 0.0358
picture QA PASS: 0 of 4 cuts fail, 2 to look at -> /Users/benjaminoats/_desk/cache/J2384_work/qa_out/PICTURE_QA.md, /Users/benjaminoats/_desk/cache/J2384_work/qa_out/picture_qa_review.jpg
```
*(Both full-size review frames in `picture_qa_review.jpg` were visually inspected and **PASS**.)*

---

## 4. Handoff to `J2386` (Elected-Chief Acceptance & Reopen `J2299` at `0/5`)

- All `J2334` technical, astronomical, motion, upscale, and QA requirements are satisfied with **PASS** at `£0.00` spend and `0` AI takes.
- Handing off to `J2386` (`033: accept J2384/J2385 R01+R55 correction and reopen J2299 at 0/5`) for elected-Chief acceptance and reopening of `J2299` at `0/5`.
