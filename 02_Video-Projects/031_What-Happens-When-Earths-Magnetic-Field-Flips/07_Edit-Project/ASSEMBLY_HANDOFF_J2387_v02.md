# 031 Assembly Handoff — Long Master `v02` (J2387, 8 Nov 2026)

## Master Export & Audio Assets (on `studio-live` NAS)

- **Long Master `v02`:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/09_Final-Export/031_what_happens_when_earths_magnetic_field_flips_master_v02.mp4`
  - **SHA-256:** `680598ae3420afa9fd40efc954cf06cefcfff234044a62e90af6a143fdf4de43`
  - **Specs:** `1920x1080`, `25 fps` CFR (`14,270` frames, `570.80 s`), `yuv420p`, `libx264` (`-crf 17`), AAC stereo `48 kHz` (`192 kbps`), `+faststart`
  - **Timeline:** `568.28 s` locked VO (`magnetic_field_flip_vo_v02a.wav`, `SHA-256: 3444635a3efa951a1031d6681390053abd9cdd3cc1ed97d537086ee7de86b3c6`) + `2.52 s` post-VO hold on `R54` after the final spoken word (`"begins."` at `568.28 s`), with `2.0 s` audio fade out at `568.60–570.60 s`.
- **Preserved Long Master `v01` (untouched):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/09_Final-Export/031_what_happens_when_earths_magnetic_field_flips_master_v01.mp4`
  - **SHA-256:** `1b90d78270d4f06b436b42e1a31d700171850511cb7790e43a546da2e20bc69b` (verified unchanged)
- **£0 Chapter-Shaped Score Bed:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/05_Music/magnetic_field_flip_score_bed_v01.mp3`
  - **SHA-256:** `9fe2f87876f9b0bbf1a80fb58d14f2ded4fddf4437efc3a83dfa4e321d0ec71f`
- **£0 House SFX Kit (`kit_v01`):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/06_Sound-Effects/kit_v01/`
  - `sfx_owb_rumble_low_v01.wav`, `sfx_owb_whoosh_soft_v01.wav`, `sfx_owb_tick_ui_v01.wav`
- **Review Pack & Contact Sheets:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/full_master_v02_pack/`
  - `PICTURE_QA.md`, `picture_qa.json`, `picture_qa_review.jpg` (NAS only), `v02_repaired_cuts_sheet.jpg` (NAS only), `cuts_v02.json`, `music_gate_v02.json`, `sfx_level_v02.json`, `mix_report_v02.json`, `gate_results_v02.json`

## Summary of `J2382` Review Fixes Applied in `v02`

1. **Removed Synthetic Concentric Bullseye/Grid Overlay (`cosmic_wave_ov.png`):**
   - Removed `ensure_wave_overlay()` from `_build_v02_fixes.py` and rebuilt `R01 c1`, `R15 c2`, `R25 c1..c4`, and `R50 c1` cleanly over pure NASA moving plates with house typography (`TODAY`, `100,000 YEARS`) and zero concentric ring/grid overlays.
2. **Honest `cuts_v02.json` Attribution & `<= 5` Stretches Cap:**
   - Replaced surplus `nasa_svs_3822_magfield_left.mp4` uses with distinct pool plates and recorded exact underlying sources in `cuts_v02.json`:
     - `R03 c1–c2` (`0:12–0:19`): `nasa_svs_20297_magnetosphere_earth_only.mp4`
     - `R39 c2` (`6:36`): `nasa_svs_4190_saa_flux_ropes.mp4`
     - `R50 c1` (`8:35`): `iss030e078095_aurora_timelapse.mp4`
     - `R53 c1` (`9:07`): `nasa_svs_3822_magfield_left.mp4` (honestly labeled in `cuts_v02.json`)
     - `R53 c2` (`9:12`): `nasa_svs_12312_dscovr_epic_earth.mp4`
   - Verified stretch counts across the entire 115-cut timeline (`<= 5` on every source):
     - `hdev_earth_views_iss_2019.mp4`: `5` stretches
     - `nasa_svs_3822_magfield_left.mp4`: `4` stretches (`R01`, `R08`, `R25`, `R53 c1`)
     - `nasa_svs_12312_dscovr_epic_earth.mp4`: `4` stretches
     - `nasa_svs_12296_earth_interior_cutaway.mp4`: `4` stretches
     - `iss030e078095_aurora_timelapse.mp4`: `3` stretches
     - `nasa_svs_20297_magnetosphere_earth_only.mp4`: `3` stretches
3. **Rebuilt `R32` (`5:29`) Paleointensity Bars & `R33 c3` (`LASCHAMP DIP`):**
   - `R32 c2` (`code_graphic_031_r32_paleo_v02.mp4`): Shifted the rotating Earth interior cutaway (`nasa_svs_12296_earth_interior_cutaway.mp4`) left and rendered animated paleointensity comparison bars (`TODAY'S FIELD`, `100,000 YEARS`, `TODAY` `2.0x` vs `MILLION-YEAR AVERAGE` `1.0x`, `TWICE ITS AVERAGE`) cleanly on the right (`x=1080..1700`) with zero overlap over the Earth cutaway.
   - `R33 c3` (`code_graphic_031_r33c_paleo_dip_v02.mp4`): Rendered the `LASCHAMP DIP` paleointensity curve over a softly blurred moving core plate (`gblur=sigma=32`) with zero overlap and zero vertical split-panel seams.
4. **Cropped `PIA20016.jpg` (`R54 c2`, `9:27`) Burned-in Caption:**
   - Cropped `PIA20016.jpg` to `(0, 40, 1277, 758)` (`1277x718`, `16:9` aspect ratio, `upscale 1.504x <= 2.35x`), completely removing the burned-in bottom-right source caption (`...iv. of Idaho (PIA20016)`) and rendering the clean house corner credit (`NASA/JPL-Caltech/Univ. of Idaho`).
5. **Updated `R22` Subscribe Card (`3:27`):**
   - Updated the subscribe lower-third subtitle on `044_R22_c1.mp4` (`3:27`) from `"NEW SPACE MYSTERIES EVERY SUNDAY"` to `"NEW SPACE MYSTERIES EVERY WEEK"`.

## Required Gate Outputs (All 5 PASS)

1. **`clip_check.py`:**
   ```
   clip_check: 54 rows — PASS
   OK: sentence/card boundaries and end-after-VO checks clear.
   ```
2. **`picture_qa.py`:**
   ```
   WARN   2:21 row R14 code_graphic_031_r14b_sdo_hot_sun_fact_v01.mp4: low detail: edge density 0.0059 < film p5 0.0095
   WARN   7:01 row R41 iss042e267617.jpg: low detail: edge density 0.0048 < film p5 0.0095
   WARN   7:28 row R44 PIA00407.jpg: low detail: luma std 16.39 < 18.0
   WARN   7:33 row R44 code_graphic_031_r44b_gravity_bodies_v01.mp4: low detail: luma std 14.89 < 18.0
   WARN   7:51 row R46 svs_10929_x17_solar_flare.mp4: low detail: edge density 0.0071 < film p5 0.0095
   WARN   8:27 row R49 commons_usfws_tundra_swans.jpg: low detail: edge density 0.0051 < film p5 0.0095
   WARN   9:21 row R54 PIA14909.jpg: low detail: edge density 0.0091 < film p5 0.0095
   WARN   9:27 row R54 PIA20016.jpg: low detail: edge density 0.0043 < film p5 0.0095
   picture QA PASS: 0 of 115 cuts fail, 8 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/full_master_v02_pack/PICTURE_QA.md, /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/full_master_v02_pack/picture_qa_review.jpg
   ```
3. **`music_gate.py`:**
   ```
   music gate PASS: magnetic_field_flip_score_bed_v01.mp3, 570.8 s, about 109.1 BPM, brief Pace: 66-74 BPM
   ```
4. **`sfx_kit.py level`:**
   ```
   SFX level PASS: VO -19.9 LUFS, SFX -45.3 LUFS, 15 hits
   ```
5. **Delivery & Loudness:**
   - Integrated loudness: `-14.6 LUFS` (target `~-14 LUFS`)
   - True peak: `-1.0 dBTP`
   - Frame size & rate: `1920x1080`, `25 fps` CFR, `yuv420p`, `570.80 s` (`14,270` frames)
   - `blackdetect` (`d=0.04:pix_th=0.10`): `0` black frames (`[]`)
