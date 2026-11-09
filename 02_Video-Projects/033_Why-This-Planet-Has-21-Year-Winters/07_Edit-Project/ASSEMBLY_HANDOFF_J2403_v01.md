# 033 Assembly Handoff — Long Master `v01` (`J2403`, 8 Nov 2026)

## 1. Master Export & Audio Assets (`studio-live`, NAS `OWB UAT`, iCloud `OWB UAT`)

- **Long Master `v01`:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/09_Final-Export/033_why_this_planet_has_21_year_winters_master_v01.mp4`
  - **Mirrored to NAS `OWB UAT`:** `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/033_why_this_planet_has_21_year_winters_master_v01.mp4`
  - **Mirrored to iCloud `OWB UAT`:** `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/033_why_this_planet_has_21_year_winters_master_v01.mp4`
  - **SHA-256 (verified across all 3 paths):** `9e9712781a99ad07e6bc753728e716cbf5ef1dc4e4ad9b80ea45c1a55f785552`
  - **Specs:** `1920x1080`, `24/1` CFR (`15,106` frames, `629.416667 s`), `yuv420p`, `libx264` (`-crf 17`), AAC stereo `48 kHz` (`192 kbps`), `+faststart`
  - **Timeline:** `611.40 s` locked VO (`02_Voiceover/uranus_vo_v01.wav`, `SHA-256: 3d73576e0c20be9030546db7bc71ea0107602d5e5fbdde37cba28c7d5b43f460`) + `18.00 s` moving end-screen hold (`R67`, `611.40–629.40 s`) over real NASA/JPL Voyager 2 imagery (`PIA18182.jpg`, `PIA01391.jpg`, `PIA00032_left_globe.jpg`) with `2.0 s` audio fade out at `627.40–629.40 s`.
- **£0 Chapter-Shaped Score Bed:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/05_Music/uranus_score_bed_v01.mp3`
  - **SHA-256:** `47f68d66c4ef7b0287c4939b14e7d906582309ca2a3354c3c262daa7e21309f0` (`629.40 s`, `70.6 BPM`, `Pace: 66-76 BPM`)
- **£0 House SFX Kit (`kit_v01`):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/06_Sound-Effects/kit_v01/`
  - `sfx_owb_rumble_low_v01.wav`, `sfx_owb_whoosh_soft_v01.wav`, `sfx_owb_tick_ui_v01.wav` (21 hits laid per `06_Sound-Effects/SFX_PLAN_v01.md`)
- **Review Pack & Contact Sheet:** `07_Edit-Project/full_master_v01_pack/` (and NAS `studio-live` + NAS/iCloud `OWB UAT`)
  - `PICTURE_QA.md`, `picture_qa.json`, `picture_qa_review.jpg` (NAS/UAT), `polish_gate_v01.json`, `music_gate_v01.json`, `sfx_level_v01.json`, `mix_report_v01.json`, `gate_results_v01.json`

## 2. Locked Picture & Edit Architecture (`67` Rows / `144` Cuts)

- **Cut Plan:** `07_Edit-Project/cuts_033_j2299_v01.json` (`144` cuts across `67` Scribe-timed rows, `0.00–629.40 s`, max cut `6.00 s`, max upscale `1.92x <= 2.35x`, max still appearances `2`, `0` adjacent `CODE` rows, `0` split words).
- **Native Moving Plates (`J2386` / `J2300` / `J2398` KEEP):**
  - `R01` (`0.00–4.35 s`): `04_Generated-Clips/J2334_fix/r01_sourced_composite_v01_silent.mp4` (`SHA-256: aab9aa2af9dd8cd50195a0b91efe495abaf9f06be2daf72bd893014b56503e6d`, trimmed `0.40–4.75 s`).
  - `R55` (`493.01–505.35 s`, 3 cuts): `04_Generated-Clips/J2334_fix/r55_passage_v01_silent.mp4` (`SHA-256: 4aa82d0e721988513eba44c38332b5537a9d6f41f9f406ab5d9623b04642483f`, split across Cuts 88–90).
- **19 Active 24fps Code Graphics (`J2299_code_graphics_v01`):**
  - Integrated at `R04`, `R07`, `R10`, `R13`, `R17`, `R22`, `R26`, `R28`, `R31`, `R34`, `R37`, `R40`, `R43`, `R45`, `R48`, `R51`, `R53`, `R58`, `R62` with continuous background motion so `polish_gate.py` records `0` frozen pairs (`max_run=1` across all 144 cuts).
- **Stills & Overlays:**
  - All 42 active real NASA/ESA/CSA/ESO/Observatory/archive stills from `03_Reference-Material/harvest_J2299_v01/` rendered with smooth sub-pixel pan/zoom (`1920x1080`, `24 fps` CFR), fine grain over dark space gradients (`R41` `PIA01280.jpg`), house corner source credits on archive stills where no lower-third/teach label is active (one-label-at-a-time rule), and chapter/subscribe cards with `0.5–0.8 s` post-sentence breath.

## 3. All 5 Automated Gate Outputs (`PASS`)

### 1. `clip_check.py`
```
clip_check: 67 rows — PASS
 - WARN: row R04: may clip mid-sentence before next row ('wenty-three point four four degree tilt,' → 'Uranus is tipped at ninety-seven point s')
 - WARN: row R47: may clip mid-sentence before next row ('ed magnet spins sideways every 17 hours,' → "Uranus' auroras miss the poles, and the ")
OK: sentence/card boundaries and end-after-VO checks clear.
```

### 2. `picture_qa.py`
```
WARN   1:15 row 11 /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA00032_left_globe.jpg: low detail: edge density 0.0288 < film p5 0.0307
WARN   1:22 row 12 /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01984.jpg: low detail: edge density 0.0202 < film p5 0.0307
WARN   1:26 row 12 /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01984.jpg: low detail: edge density 0.0284 < film p5 0.0307
WARN   2:00 row 15 /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/weic2332a_hires.jpg: low detail: edge density 0.0279 < film p5 0.0307
WARN   3:05 row 21 /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01985.jpg: low detail: edge density 0.0306 < film p5 0.0307
WARN   4:35 row 32 /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01391.jpg: low detail: edge density 0.0307 < film p5 0.0307
WARN   5:14 row 36 /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/stsci-h-p1906a-f_uranus_globe.png: low detail: edge density 0.0289 < film p5 0.0307
WARN   7:31 row 50 /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/weic2332a_hires.jpg: low detail: edge density 0.0293 < film p5 0.0307
picture QA PASS: 0 of 144 cuts fail, 8 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/07_Edit-Project/full_master_v01_pack/PICTURE_QA.md, /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/07_Edit-Project/full_master_v01_pack/picture_qa_review.jpg
```

### 3. `polish_gate.py`
```
polish gate PASS: 0 of 144 rows failed, 8 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/07_Edit-Project/full_master_v01_pack/polish_gate_v01.json
```

### 4. `music_gate.py`
```
music gate PASS: uranus_score_bed_v01.mp3, 629.4 s, about 70.6 BPM, brief Pace: 66-76 BPM
```

### 5. `sfx_kit.py level`
```
SFX level PASS: VO -20.2 LUFS, SFX -47.2 LUFS, 21 hits
```

### 6. Delivery & Loudness Verification
- **Integrated loudness:** `-14.5 LUFS` (target `~-14 LUFS`)
- **True peak:** `-1.5 dBTP` (`<= -1.0 dBTP`)
- **Frame size & rate:** `1920x1080`, `24/1` CFR, `yuv420p`, `15,106` frames (`629.416667 s`)
- **Black frames (`blackdetect=d=0.04:pix_th=0.10`):** `0` (`[]`)
- **Total Spend:** `£0`
