# J2384 — Build Report: £0 R01 97.77° Sourced Composite & R55 3-Cut Cloud Passage (OWB 033 Uranus)

- **Job**: `J2384` (`033: build £0 R01 97.77-deg sourced composite and R55 r55b+PIA01488 cloud passage`, `kind: assembly`, `film: 033`, `stage: picture`, `needs: mini`)
- **Agent**: `gemini` (`gemini-agy`)
- **Date**: `2026-11-08T05:44Z`
- **Upstream Ruling**: `J2334` (`jobs/reviews/J2334/CHIEF_RULING.md`, commit `4ddd1058a0`)
- **Spend & Generation Compliance**: `£0.00` cash, `0` Flow/Veo/Vertex/Omni credits, `0` new AI takes generated.
- **NAS Delivery Locations**:
  - Live project clip store: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/04_Generated-Clips/J2334_fix/`
  - Archive staging store: `/Volumes/data/mac-mini-archive/studio-staging/033_Uranus/J2334_fix/`
  - Local build workspace: `/Users/benjaminoats/_desk/cache/J2384_work/`

---

## 1. Verified Source Inputs

| Source ID | Role | Local Path | Resolution | SHA-256 |
|---|---|---|---|---|
| `PIA18182` | NASA Voyager 2 natural-colour cyan Uranus globe (`R01`) | `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/03_Reference-Material/harvest_J2089_v01/PIA18182.jpg` | `1720x1720` | `3dcc83114f1a25caa1ae1a1436830fffaa15a3e429666dbf4c68bcf035e8932b` |
| `weic2310a` | NASA / ESA / CSA / STScI JWST NIRCam Uranus ring radial profile & polar cap (`R01`) | `/Users/benjaminoats/_desk/cache/J2089/jwst_v01/uranus_nircam_unannotated.png` | `1400x1400` | `e5f7a1a0e10a6e6c769b40ecbb2f4dd78ea2ada65f2e96efd69c113ea29f52a7` |
| `r55b_flow_t1_silent.mp4` | Accepted `J2332`/`J2334` blue-green Uranus cloud-top vortex world plate (`R55` Cuts 1 & 2) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/04_Generated-Clips/J2332/r55b_flow_t1_silent.mp4` | `1280x720` (`24/1` fps, `7.917 s`) | `1e71287f9abaafc8c3f586dc7a9cb195ea2193cd3b9d041e5b8c95715cb34fba` |
| `PIA01488` | NASA Voyager 2 Uranus upper-atmosphere plate (`R55` Cut 3) | `/Users/benjaminoats/_desk/cache/J2299/harvest/PIA01488.jpg` | `2118x2618` | `9c49e13d8da1c052f8bda283a4df0d2a054840b03bb175c90454d2049d80a86b` |

---

## 2. Delivered Video Assets & SHA-256 Manifest

All deliverables are `1920x1080`, `24/1` fps (`h264`, `yuv420p`), silent (`video_streams = 1`, `audio_streams = 0`), with `0` frozen frame pairs:

| File | Cut / Window | Duration (`nb_frames`) | SHA-256 | `mean_frame_diff` (`min` / `max`) | `frozen_pairs` |
|---|---|---|---|---|---|
| `r01_sourced_composite_v01_silent.mp4` | `R01` (`0.00–4.35 s` active interval `0.40–4.75 s` in `6.00 s` master) | `6.0000 s` (`144` frames) | `aab9aa2af9dd8cd50195a0b91efe495abaf9f06be2daf72bd893014b56503e6d` | `1.1236` (`0.9353` / `1.1764`) | `0` |
| `r55_cut1_r55b_100x_silent.mp4` | `R55` Cut 1 (`493.010–496.968 s`, `r55b` `0.000–3.958 s` @ `1.00x` full frame = `1.50x` upscale) | `3.9583 s` (`95` frames) | `df6d92d5977fb7fdc6811f43918122abd08eed5f8f825fe67e0299d367808e8a` | `6.4906` (`5.3124` / `7.5914`) | `0` |
| `r55_cut2_r55b_128x_vortex_silent.mp4` | `R55` Cut 2 (`496.968–500.927 s`, `r55b` `3.958–7.917 s` @ `1.28x` vortex crop `1000x562` = `1.92x` upscale) | `3.9583 s` (`95` frames) | `75adc0df000568f359bb3b32c9f29ec6eb545f57fa204ce255b5632ec74edeb4` | `7.0018` (`4.7520` / `8.5514`) | `0` |
| `r55_cut3_pia01488_pushin_silent.mp4` | `R55` Cut 3 (`500.927–505.350 s`, `PIA01488` `1.00x` native > `1080p` upper-atmosphere glide) | `4.4167 s` (`106` frames) | `3b606e6edf81365422f782643451d8479e45c4d7a7fab3e23661066b43e2647b` | `2.5302` (`2.4634` / `2.5534`) | `0` |
| `r55_passage_v01_silent.mp4` | `R55` Combined 3-Cut Passage (`493.010–505.350 s`) | `12.3333 s` (`296` frames) | `4aa82d0e721988513eba44c38332b5537a9d6f41f9f406ab5d9623b04642483f` | `5.6313` (`2.4673` / `77.5851`) | `0` |
| `j2384_r01_r55_reel_silent.mp4` | Combined `R01` (`0.00–4.35 s`) + `R55` (`493.01–505.35 s`) QA verification reel | `16.7083 s` (`401` frames) | `7ca09d4cd096a2ba610337012c920f508463ef2f417e294d77b52e3b99f65493` | `4.5958` (`0.8662` / `79.1008`) | `0` |

---

## 3. Scope & Technical Implementation Details

### 3.1 `R01` (`0.00–4.35 s` — `r01_sourced_composite_v01_silent.mp4`)
- **Sideways Axial Tilt (`97.77°`) & Upright Rings (`7.77°` from vertical)**:
  - Constructed from verified Voyager 2 natural-colour cyan Uranus globe `PIA18182` (`1720x1720`, `1.20x <= 2.35x` upscale) aligned with the polar haze hood and radial 13-ring profile extracted from JWST NIRCam `weic2310a`.
  - Uranus's spin axis sits nearly horizontal (`7.77°` below the orbital plane, `97.77°` axial obliquity), and the narrow concentric ring system (`zeta`, `6`, `5`, `4`, `alpha`, `beta`, `eta`, `gamma`, `delta`, `lambda`, `epsilon`, `nu`, `mu`) stands nearly vertical (`7.77°` from vertical), with rear ring arcs properly occluded behind the globe and front ring arcs passing cleanly across the cyan disc.
- **24fps Orbital Drift & Multi-Plane Deep-Space Parallax**:
  - Smooth 24fps orbital camera push-in (`1.00x -> 1.08x`) with 3-plane deep-space starfield parallax and subtle polar/equatorial rotation over a graded `#050814` navy sky with fine film grain (`mean_frame_diff = 1.1236 >= 0.35`, `frozen_pairs = 0`).
- **Disclosure & Framing Rules**:
  - Zero opening explanatory text in `0–3 s`; small lower-left corner credit in Didot italic (`NASA / JPL / ESA / CSA / STScI (composite)`) sits completely off the planet and rings. `svs20390` is excluded.

### 3.2 `R55` (`493.01–505.35 s` — `r55_passage_v01_silent.mp4`)
- **Cut 1 (`493.010–496.968 s`, `3.958 s`, `95` frames — `r55_cut1_r55b_100x_silent.mp4`)**:
  - Uses accepted `r55b_flow_t1_silent.mp4` source offset `0.000–3.958 s` at `1.00x` full frame (`1280x720 -> 1920x1080` = `1.50x <= 2.35x` upscale). Immediately follows `R54` (`487.24–493.01 s` `CODE` chart `code_graphic_033_r54_core_vs_cloud_temp.mp4`), guaranteeing strict **chart-to-moving-world-plate** separation across `R54 -> R55`.
- **Cut 2 (`496.968–500.927 s`, `3.958 s`, `95` frames — `r55_cut2_r55b_128x_vortex_silent.mp4`)**:
  - Uses accepted `r55b_flow_t1_silent.mp4` source offset `3.958–7.917 s` with a distinct `1.28x` vortex-centre framing crop (`1000x562` at `x=160, y=90` scaled to `1920x1080` = `1.92x <= 2.00x` upscale), establishing a clear `<= 4–6 s` visual cut at `496.968 s` with `0` replayed frames.
- **Cut 3 (`500.927–505.350 s`, `4.417 s`, `106` frames — `r55_cut3_pia01488_pushin_silent.mp4`)**:
  - Uses verified NASA Voyager 2 upper-atmosphere plate `PIA01488` (`2118x2618`, `1.00x` native > `1080p` crop) showing the curved blue-green atmospheric haze deck over `#050814` navy starry space with fine grain and a smooth constant-velocity camera glide (`jitter.max_off_trend_px = 0.112 <= 0.35`, `reversals = 0`).

---

## 4. Gate Outputs (`polish_gate.py` & `picture_qa.py`)

### 4.1 `scripts/polish_gate.py` Output (`PASS`)
```text
   1     2.2s r01_sourced_composite_v01_si ok
  55     6.3s r55b_flow_t1_silent.mp4      ok
  55    10.3s r55b_flow_t1_silent.mp4      ok
  55    14.5s PIA01488.jpg                 WARN low detail: edge density 0.0343 < film p5 0.0358
polish gate PASS: 0 of 4 rows failed, 1 to look at -> /Users/benjaminoats/_desk/cache/J2384_work/polish_gate.json
```

Per-cut metrics from `jobs/reviews/J2384/polish_gate.json`:
- **Cut 0 (`R01` `r01_sourced_composite_v01_silent.mp4`)**: `std = 30.29` (`>= 18.0`), `mean = 43.46` (`>= 32.0`), `p95 = 100.0` (`>= 50.0`), `edge = 0.0446` (`>= 0.0259`), `seams = []`, `fail = []`, `warn = []`.
- **Cut 1 (`R55` Cut 1 `r55b_flow_t1_silent.mp4` @ `0.000 s`)**: `std = 56.17`, `mean = 118.78`, `p95 = 201.0`, `edge = 0.0743`, `seams = []`, `fail = []`, `warn = []`.
- **Cut 2 (`R55` Cut 2 `r55b_flow_t1_silent.mp4` @ `3.958 s`, `1.28x` crop)**: `std = 52.36`, `mean = 124.62`, `p95 = 206.0`, `edge = 0.0579`, `seams = []`, `fail = []`, `warn = []`.
- **Cut 3 (`R55` Cut 3 `PIA01488.jpg` `1.00x` native)**: `std = 43.52` (`>= 18.0`), `mean = 45.17` (`>= 28.0`), `p95 = 159.0` (`>= 50.0`), `edge = 0.0343` (`>= 0.0259` absolute floor), `seams = []`, `jitter.max_off_trend_px = 0.112` (`<= 0.35`), `jitter.reversals = 0`, `fail = []`.

### 4.2 `scripts/picture_qa.py` Output (`PASS`)
```text
WARN   0:02 row 1 r01_sourced_composite_v01_silent.mp4: kind of picture: 'Voyager 2 PIA18182 + JWST NIRCam weic2310a Uranus 97.77-deg sideways composite' (composite), look at it full size
WARN   0:14 row 55 PIA01488.jpg: low detail: edge density 0.0343 < film p5 0.0358
picture QA PASS: 0 of 4 cuts fail, 2 to look at -> /Users/benjaminoats/_desk/cache/J2384_work/qa_out/PICTURE_QA.md, /Users/benjaminoats/_desk/cache/J2384_work/qa_out/picture_qa_review.jpg
```
