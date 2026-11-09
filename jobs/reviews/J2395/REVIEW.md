# Review — `031` Magnetic Field Flip Shorts 1 & 2 (`J2388` + `J2394` `v02`) & UAT Handoff (`J2395`)

- **Film:** `031_What-Happens-When-Earths-Magnetic-Field-Flips` (`OWB:031`)
- **Stage:** `edit`
- **Reviewer:** `gemini` (`J2395`, `kind: review`, elected acting Chief)
- **Date:** `2026-11-08`
- **Verdict Summary:**
  - **Long Master `v02` (`J2387` / `J2390`):** **KEEP** (`031_what_happens_when_earths_magnetic_field_flips_master_v02.mp4`, `SHA-256: 680598ae3420afa9fd40efc954cf06cefcfff234044a62e90af6a143fdf4de43`, `570.80 s` / `14,270` frames @ `25 fps` CFR; 720p UAT watch proxy `031_what_happens_when_earths_magnetic_field_flips_master_v02_PHONE.mp4`, `SHA-256: a8c748f68cf2215f224f0d616b145ec45ffe04db4b0bfd305a9541bbc9931c9d`, uploaded to R2 `owb-031-v02`).
  - **Active Short #1 (`J2388`, Test A opening cut):** **KEEP** (`031_short_testA_opening_flip_v01.mp4`, `SHA-256: ebe11bb730ccfab8681d564d3588d17011a28629c7b6f926eba952bfc98c4bcd`, `33.00 s` / `825` frames @ `25 fps` CFR, uploaded to R2 `owb-j2395-2-v01`).
  - **Active Short #2 `v02` (`J2394`, Keeper question cut):** **KEEP** (`031_short_sat12_solar_wind_air_v02.mp4`, `SHA-256: 4f25b1cd9d2c806367a98f3a7e173bbd0d16dc3390e0c882c223c23af6f10450`, `24.48 s` / `612` frames @ `25 fps` CFR, uploaded to R2 `owb-j2395-3-v02`; `v01` preserved untouched on NAS).

---

## 1. Active Short #1 (`J2388`, `031_short_testA_opening_flip_v01.mp4`) — **KEEP**

- **Master File (NAS `studio-live`):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/testA_opening_flip/06_Final-Exports/031_short_testA_opening_flip_v01.mp4` (`SHA-256: ebe11bb730ccfab8681d564d3588d17011a28629c7b6f926eba952bfc98c4bcd`)
- **Frame 0 (`1080x1920`):** `031_short_testA_opening_flip_v01_frame0.jpg` (`SHA-256: aa0763c2f1e553ac373e6596c684c115242afcac0c9fa15d8eaf0030ada`, `saturation=105.4`, `near_black=1%`)
- **Custom Cover (`1080x1920`, no Orbit):** `031_short_testA_opening_flip_v01_cover.jpg` (`SHA-256: 8f5be5cd1e41b0b5df695d6fbbe6e69682965f010ddc70f2e70b9bb053caee5d`, `saturation=138.1`, `near_black=2%`)
- **UAT & R2 Verification:**
  - NAS `OWB UAT`: `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/031_shorts_v02/031_short_testA_opening_flip_v01.mp4` (`SHA-256: ebe11bb730ccfab8681d564d3588d17011a28629c7b6f926eba952bfc98c4bcd`)
  - iCloud `OWB UAT`: `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/031_shorts_v02/031_short_testA_opening_flip_v01.mp4` (`SHA-256: ebe11bb730ccfab8681d564d3588d17011a28629c7b6f926eba952bfc98c4bcd`)
  - R2 Watch Stream: `https://studio-kanban.vercel.app/api/watch?v=owb-j2395-2-v01` (`33,663,285` bytes)

### 1.1 Visual & Editorial Inspection (`13` Shots, `33.00 s`)
Inspected `031_short_testA_opening_flip_v01_review_13shots.jpg`, `031_short_testA_opening_flip_v01_open_sheet.jpg`, `031_short_testA_opening_flip_v01_picture_qa/picture_qa_review.jpg`, `031_short_testA_opening_flip_v01_frame0_preview.jpg`, `031_short_testA_opening_flip_v01_cover_preview.jpg`, and `_assemble_031_short1_v01.py`:
- **Spoken Lift & Pacing (`PASS`):** Verbatim lift of `s00–s08` (`96` words, `0.08–31.54 s`) from locked `magnetic_field_flip_vo_v02a.wav` (`SHA-256: 3444635a3efa951a1031d6681390053abd9cdd3cc1ed97d537086ee7de86b3c6`), answering the survival myth (`"No. We will survive. Life has lived through hundreds of magnetic flips."`) and ending cleanly on the three concrete questions `031` answers (`LEARNINGS 17`). Inter-sentence pauses tightened to `0.22 s < 0.25 s`; Cut 1 at `2.32 s <= 2.80 s`, Cut 2 at `4.72 s <= 4.80 s`; max shot hold `3.68 s <= 4.00 s`.
- **Zero Synthetic Patterns or Text Collisions (`PASS`):**
  - Zero `get_nebula_wave()`, `make_cosmic_backdrop()`, `cosmic_wave_ov.png`, or `od.arc()` cartoon curves anywhere across all 13 shots.
  - `R02a` (`8.40–11.40 s`, NASA ISS aurora timelapse) and `R02a2` (`11.40–14.12 s`, NASA SVS 3822 magnetosphere loops) are completely text-free under the `9.00–14.00 s` parent-title banner (`What Happens When / Earth's Magnetic / Field Flips?`); `R02b` (`POLES SWAP`) begins at `14.12 s` after the banner clears.
  - Single Teach overlay **`HUNDREDS OF FLIPS`** (`18.52–20.56 s` on `R03b`) sits cleanly inside the `16:9` centre band (`y=1187..1245`), clear of `0–2 s` and `9–14 s`.
  - The single `picture_qa` `WARN` (`0:30 R04c`, `iss030e078095_aurora_timelapse.mp4`, low edge density `0.0204 < p5 0.0237`) was inspected full-size on `picture_qa_review.jpg` and confirmed to be a clean, natural night-side aurora curtain over city lights.

### 1.2 Pasted Gate Outputs — Short 1 (`All 7 PASS`)
```
PASS  031_short_testA_opening_flip_v01.mp4  dur=33.0s  audio=-16.7dB  motion=27.25  f0diff=9.28  cut1=2.32s  vo_onset=0.08s  tail_gap=1.46s  vo_src=/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/testA_opening_flip/06_Final-Exports/031_short_testA_opening_flip_v01_vo.wav  dhash=982b074783078b06  visor=0.0
   warn  duration 33.0s outside 22–27s band

PASS  031_short_testA_opening_flip_v01_frame0.jpg  saturation=105.4  near_black=1%
PASS  031_short_testA_opening_flip_v01_cover.jpg  saturation=138.1  near_black=2%

SFX level PASS: VO -16.3 LUFS, SFX -40.2 LUFS, 6 hits
music gate PASS: magnetic_field_flip_score_bed_v01.mp3, 570.8 s, about 109.1 BPM, brief Pace: 66-74 BPM
polish gate PASS: 0 of 13 rows failed, 1 to look at
picture QA PASS: 0 of 13 cuts fail, 1 to look at
```

---

## 2. Active Short #2 `v02` (`J2394`, `031_short_sat12_solar_wind_air_v02.mp4`) — **KEEP**

- **Master File (NAS `studio-live`):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v02.mp4` (`SHA-256: 4f25b1cd9d2c806367a98f3a7e173bbd0d16dc3390e0c882c223c23af6f10450`; `v01` preserved untouched at `2f0f7e82e7d4c36d484d3bbf1ba7516118b3d1cdf61b788119996dc5ca85547c`)
- **Frame 0 (`1080x1920`):** `031_short_sat12_solar_wind_air_v02_frame0.jpg` (`SHA-256: f6b31eba43715fa776345296cbc51a1a6ef454865b3600b377e305535bd1a843`, `saturation=101.5`, `near_black=0%`)
- **Custom Cover (`1080x1920`, no Orbit):** `031_short_sat12_solar_wind_air_v02_cover.jpg` (`SHA-256: 63c43e387c209af75bea5d73c43b6c1556b8bbcbe7a69d90c31d2fc362d94e1f`, `saturation=111.2`, `near_black=0%`)
- **UAT & R2 Verification:**
  - NAS `OWB UAT`: `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/031_shorts_v02/031_short_sat12_solar_wind_air_v02.mp4` (`SHA-256: 4f25b1cd9d2c806367a98f3a7e173bbd0d16dc3390e0c882c223c23af6f10450`)
  - iCloud `OWB UAT`: `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/031_shorts_v02/031_short_sat12_solar_wind_air_v02.mp4` (`SHA-256: 4f25b1cd9d2c806367a98f3a7e173bbd0d16dc3390e0c882c223c23af6f10450`)
  - R2 Watch Stream: `https://studio-kanban.vercel.app/api/watch?v=owb-j2395-3-v02` (`30,249,815` bytes)

### 2.1 Verification of All 4 `J2390` FIX Items (`9` Shots, `24.48 s`)
Inspected `031_short_sat12_solar_wind_air_v02_review_9shots.jpg`, `031_short_sat12_solar_wind_air_v02_open_sheet.jpg`, `031_short_sat12_solar_wind_air_v02_picture_qa/picture_qa_review.jpg`, `031_short_sat12_solar_wind_air_v02_frame0_preview.jpg`, `031_short_sat12_solar_wind_air_v02_cover_preview.jpg`, and `_assemble_031_short2_v02.py`:
1. **Zero `get_nebula_wave()` / `make_cosmic_backdrop()` synthetic plaid or painted dots (`PASS`):** Completely removed from `_assemble_031_short2_v02.py`. Every shot uses either a full `9:16` reframe (`R39b`, `upscale=1.40x`) or `composite_band_on_natural_blur()` with a 96-px cosine feather over a clean Gaussian-blurred vertical fill derived from that shot's real moving NASA pixels.
2. **Zero `od.arc()` cartoon curves, `plasma_wave` sine ripple, or dark-ring cutout on `R39a`, `frame0.jpg`, `cover.jpg`, and `R39_loop` (`PASS`):** `R39a` (`0.00–2.36 s`), `frame0.jpg`, `cover.jpg`, and `R39_loop` (`23.16–24.48 s`) render directly from clean graded 4K NASA SVS 20297 footage (`svs_20297_van_allen_earth_only.mp4` @ `6.4 s`, `upscale=0.95x`).
3. **Zero ghost double-exposed Blue Marble Earth on `R39b` (`2.36–3.32 s`) (`PASS`):** `R39b` renders directly from a single clean moving NASA SVS 3822 geomagnetic field lines plate (`svs_3822_magfield_left.mp4` @ `28.0 s`, full `9:16` reframe `upscale=1.40x`).
4. **Zero `9.00–14.00 s` parent-title banner text collision on `R42a` (`9.32–12.68 s`) (`PASS`):** `R42a` renders a clean text-free moving NASA ISS sunlit orbital pass (`hdev_earth_views_iss_2019.mp4` @ `128.0 s`, `upscale=1.25x`) followed by DSCOVR EPIC (`nasa_svs_12312_dscovr_epic_earth.mp4` @ `16.0 s` on `R42b`), so `What Happens When / Earth's Magnetic / Field Flips?` (`9.00–14.00 s`) sits over clean moving Earth footage with zero overlapping graphic text.
5. **Single `picture_qa` `WARN` inspected (`PASS`):** `0:05 R40` (`code_graphic_031_r40a_never_vanishes_v01.mp4`, low edge density `0.0331 < p5 0.0363`) was inspected full-size on `picture_qa_review.jpg` and confirmed to be a clean, sharp multipole magnetosphere graphic (`NEVER VANISHES`).

### 2.2 Pasted Gate Outputs — Short 2 `v02` (`All 7 PASS`)
```
PASS  031_short_sat12_solar_wind_air_v02.mp4  dur=24.48s  audio=-16.9dB  motion=22.1  f0diff=3.63  cut1=2.36s  vo_onset=0.09s  tail_gap=1.46s  vo_src=/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v02_vo.wav  dhash=bc17cffffe9fccd8  visor=0.0

PASS  031_short_sat12_solar_wind_air_v02_frame0.jpg  saturation=101.5  near_black=0%
PASS  031_short_sat12_solar_wind_air_v02_cover.jpg  saturation=111.2  near_black=0%

SFX level PASS: VO -16.5 LUFS, SFX -38.5 LUFS, 5 hits
music gate PASS: magnetic_field_flip_score_bed_v01.mp3, 570.8 s, about 109.1 BPM, brief Pace: 66-74 BPM
polish gate PASS: 0 of 9 rows failed, 1 to look at
picture QA PASS: 0 of 9 cuts fail, 1 to look at
```

---

## 3. UAT Handoff & `WIP.json` Advancement

1. **R2 Watch Streams & `jobs.py awaits J2395`:**
   - `J2395.1` (`OWB:031` Long `v02`): `OWB UAT/031_what_happens_when_earths_magnetic_field_flips_master_v02_PHONE.mp4` (`https://studio-kanban.vercel.app/api/watch?v=owb-031-v02`, airs `Wed 2026-12-02 18:00` London).
   - `J2395.2` (`031` Short 1 `v01`, Test A opening): `OWB UAT/031_shorts_v02/031_short_testA_opening_flip_v01.mp4` (`https://studio-kanban.vercel.app/api/watch?v=owb-j2395-2-v01`, airs `Sat 2026-12-05 11:30` London).
   - `J2395.3` (`031` Short 2 `v02`, Keeper question): `OWB UAT/031_shorts_v02/031_short_sat12_solar_wind_air_v02.mp4` (`https://studio-kanban.vercel.app/api/watch?v=owb-j2395-3-v02`, airs `Sat 2026-12-12 11:30` London).
2. **`jobs/WIP.json` Advancement (`AGENTS.md` §How films get worked on):**
   - `OWB:031` has reached Ben's watch (UAT) and leaves `active`.
   - `OWB:J01` (*From Earth to Orion: A 600-Light-Year Space Journey*, already `KEEP` on topic and script review under `J2219`, `PR #553 fab7cf9b61`) enters `active` from the head of `next` (`entered["OWB:J01"] = "2026-11-08"`), maintaining the 5 OWB + 4 HOS (`9` total) active production cap.
