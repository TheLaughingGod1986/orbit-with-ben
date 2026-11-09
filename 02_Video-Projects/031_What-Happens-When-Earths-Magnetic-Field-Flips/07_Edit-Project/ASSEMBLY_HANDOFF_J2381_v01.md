# 031 Assembly Handoff — Long Master `v01` (J2381, 8 Nov 2026)

## Master Export & Audio Assets (on `studio-live` NAS)

- **Long Master `v01`:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/09_Final-Export/031_what_happens_when_earths_magnetic_field_flips_master_v01.mp4`
  - **SHA-256:** `1b90d78270d4f06b436b42e1a31d700171850511cb7790e43a546da2e20bc69b`
  - **Specs:** `1920x1080`, `25 fps` CFR (`14,270` frames, `570.80 s`), `yuv420p`, `libx264` (`-crf 17`), AAC stereo `48 kHz` (`192 kbps`), `+faststart`
  - **Timeline:** `568.28 s` locked VO (`magnetic_field_flip_vo_v02a.wav`, `SHA-256: 3444635a3efa951a1031d6681390053abd9cdd3cc1ed97d537086ee7de86b3c6`) + `2.52 s` post-VO hold on `R54` after the final spoken word (`"begins."` at `568.28 s`), with `2.0 s` audio fade out at `568.60–570.60 s`.
- **£0 Chapter-Shaped Score Bed:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/05_Music/magnetic_field_flip_score_bed_v01.mp3`
  - **SHA-256:** `9fe2f87876f9b0bbf1a80fb58d14f2ded4fddf4437efc3a83dfa4e321d0ec71f`
  - **Plan & Brief:** `05_Music/MUSIC_BRIEF_v01.md` (`Pace: 66-74 BPM` with `NOT:` exclusions), `05_Music/magnetic_field_flip_score_bed_v01_plan.json`, `05_Music/_build_031_score_bed_v01.py`
- **£0 House SFX Kit (`kit_v01`):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/06_Sound-Effects/kit_v01/`
  - `sfx_owb_rumble_low_v01.wav`, `sfx_owb_whoosh_soft_v01.wav`, `sfx_owb_tick_ui_v01.wav`
- **Review Pack & Contact Sheet:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/full_master_v01_pack/`
  - `PICTURE_QA.md`, `picture_qa.json`, `picture_qa_review.jpg` (NAS only), `cuts_v01.json`, `music_gate_v01.json`, `sfx_level_v01.json`, `mix_report_v01.json`, `gate_results_v01.json`

## Required Gate Outputs (All 5 PASS)

1. **`clip_check.py`:**
   ```
   clip_check: 54 rows — PASS
   OK: sentence/card boundaries and end-after-VO checks clear.
   ```
2. **`picture_qa.py`:**
   ```
   picture QA PASS: 0 of 115 cuts fail, 11 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/full_master_v01_pack/PICTURE_QA.md, /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/full_master_v01_pack/picture_qa_review.jpg
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
