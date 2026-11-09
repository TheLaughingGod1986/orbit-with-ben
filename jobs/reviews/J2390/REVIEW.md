# Review — `031` Magnetic Field Flip Long Master `v02` + Shorts 1 & 2 (`J2390`)

- **Film:** `031_What-Happens-When-Earths-Magnetic-Field-Flips` (`OWB:031`)
- **Stage:** `edit`
- **Reviewer:** `gemini` (`J2390`, `kind: review`)
- **Date:** `2026-11-08`
- **Verdict Summary:**
  - **Long Master `v02` (`J2387`):** **KEEP** (`031_what_happens_when_earths_magnetic_field_flips_master_v02.mp4`, `SHA-256: 680598ae3420afa9fd40efc954cf06cefcfff234044a62e90af6a143fdf4de43`, `570.80 s`, `14,270` frames at `25 fps` CFR — staged to NAS `OWB UAT` and iCloud `OWB UAT`).
  - **Active Short #2 `v01` (`J2389`):** **FIX** (rebuild as `031_short_sat12_solar_wind_air_v02.mp4` leaving `v01` untouched on NAS).
  - **Active Short #1 (`J2388`):** **PENDING BUILD** (`J2388` was still `open` because `J2390` only listed `after: J2389`; now strictly chained `J2388 -> Short 2 v02 repair -> Shorts 1 & 2 review + UAT handoff` at `due: 2026-12-02 18:00`).

---

## 1. Long Master `v02` Verification (`J2387`) — **KEEP**

- **Master File (NAS `studio-live`):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/09_Final-Export/031_what_happens_when_earths_magnetic_field_flips_master_v02.mp4`
- **SHA-256:** `680598ae3420afa9fd40efc954cf06cefcfff234044a62e90af6a143fdf4de43` (`master_v01.mp4` preserved untouched at `1b90d78270d4f06b436b42e1a31d700171850511cb7790e43a546da2e20bc69b`)
- **UAT Copies Staged & Verified (SHA-256 match):**
  - `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/031_what_happens_when_earths_magnetic_field_flips_master_v02.mp4`
  - `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/031_what_happens_when_earths_magnetic_field_flips_master_v02.mp4`

### 1.1 Verification of All 5 `J2382` FIX Items
Inspected `07_Edit-Project/full_master_v02_pack/v02_repaired_cuts_sheet.jpg`, `picture_qa_review.jpg`, `cuts_v02.json`, `_assemble_031_full_master_v02.py`, and extracted full-resolution mid-frames for `R44b` (`454.5 s`) and `R44c` (`458.5 s`):
1. **Zero `cosmic_wave_ov.png` concentric bullseye/grid overlays (`PASS`):** `ensure_wave_overlay()` and `cosmic_wave_ov.png` are completely removed from `_assemble_031_full_master_v02.py`. Visual inspection of `R01 c1` (`2.3 s`), `R15 c2` (`150.9 s`), `R25 c1..c4` (`246.8–263.1 s`), `R32 c1..c2` (`329.0–334.3 s`), `R39 c2` (`402.6 s`), `R50 c1` (`516.1 s`), and `R53 c1` (`550.4 s`) confirms clean, natural space and magnetosphere plates with zero synthetic bullseye/grid patterns.
2. **Honest `cuts_v02.json` source attribution & `<= 5` stretches cap (`PASS`):** `R03 c1–c2` (`19.5–22.4 s`) is genuinely rendered from `nasa_svs_12312_dscovr_epic_earth.mp4` and `R53 c2` (`555.8 s`) from `iss030e078095_aurora_timelapse.mp4`. Stretch counts across all 115 cuts in `cuts_v02.json` obey `<= 5`: `hdev_earth_views_iss_2019.mp4: 5`, `nasa_svs_3822_magfield_left.mp4: 4`, `nasa_svs_12312_dscovr_epic_earth.mp4: 4`, `nasa_svs_12296_earth_interior_cutaway.mp4: 4`, `iss030e078095_aurora_timelapse.mp4: 3`, `nasa_svs_20297_magnetosphere_earth_only.mp4: 3`.
3. **Animated paleointensity comparison bars on `R32` (`5:29`) & `R33 c3` (`PASS`):** `R32 c1` (`329.0 s`) and `R32 c2` (`334.3 s`) render animated comparison bars (`100,000 YEARS / TODAY` and `TWICE ITS AVERAGE / TODAY` `2.0x` vs `MILLION-YEAR AVERAGE` `1.0x`) on the right (`x=1080..1700`) over the rotating 3D Earth core cutaway (`nasa_svs_12296_earth_interior_cutaway.mp4`) shifted left with zero overlap; `R33 c3` (`347.8 s`) renders `NEARLY TO ZERO / LASCHAMP DIP` cleanly over a softly blurred moving core cutaway.
4. **Cropped `PIA20016.jpg` burned-in caption on `R54 c2` (`9:27`) (`PASS`):** `R54 c2` (`567.1 s`) crops `PIA20016.jpg` to `(0, 40, 1277, 758)` (`upscale 1.504x <= 2.35x`) above the source JPEG's truncated text (`...iv. of Idaho (PIA20016)`) and renders the clean house corner credit (`NASA/JPL-Caltech/Univ. of Idaho`).
5. **Updated `R22` subscribe card (`3:27`) (`PASS`):** `R22 c1` (`223.7 s`) reads `"NEW SPACE MYSTERIES EVERY WEEK / SUBSCRIBE TO ORBIT WITH BEN"` over the moving ISS Earth limb.

### 1.2 Automated Gates on `master_v02.mp4` (All 5 `PASS`)
```
clip_check: 54 rows — PASS
OK: sentence/card boundaries and end-after-VO checks clear.

picture QA PASS: 0 of 115 cuts fail, 8 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/full_master_v02_pack/PICTURE_QA.md, /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/full_master_v02_pack/picture_qa_review.jpg

music gate PASS: magnetic_field_flip_score_bed_v01.mp3, 570.8 s, about 109.1 BPM, brief Pace: 66-74 BPM

SFX level PASS: VO -19.9 LUFS, SFX -45.3 LUFS, 15 hits

Delivery: 1920x1080, 25 fps CFR, 570.80 s (14,270 frames), integrated -14.6 LUFS, true peak -1.0 dBTP, 0 black frames
```
All 8 `picture_qa` `WARN` frames (`2:21 R14`, `7:01 R41`, `7:28 R44`, `7:33 R44`, `7:51 R46`, `8:27 R49`, `9:21 R54`, `9:27 R54`) were inspected full-size on `picture_qa_review.jpg` (plus mid-frames of `R44b` at `454.5 s` and `R44c` at `458.5 s`) and confirmed sharp, natural, and accurate.

---

## 2. Active Short #2 `v01` Verification (`J2389`, `031_short_sat12_solar_wind_air_v01.mp4`) — **FIX**

- **File Inspected:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/10_Shorts/sat12_solar_wind_air/06_Final-Exports/031_short_sat12_solar_wind_air_v01.mp4` (`SHA-256: 2f0f7e82e7d4c36d484d3bbf1ba7516118b3d1cdf61b788119996dc5ca85547c`, `24.48 s`, `612` frames at `25 fps` CFR)
- **Sheets Inspected:** `031_short_sat12_solar_wind_air_v01_open_sheet.jpg`, `031_short_sat12_solar_wind_air_v01_frame0_preview.jpg`, `031_short_sat12_solar_wind_air_v01_cover_preview.jpg`, `picture_qa_review.jpg`, and 9-shot mid-frame sheet `031_short_sat12_solar_wind_air_v01_review_9shots.jpg`.

While the spoken lift (`s65, s67, s70, s74`, `64` words, `24.48 s`), audio mix (`VO -16.5 LUFS`, `SFX -38.5 LUFS`, integrated `-14.0 LUFS`, `-2.2 dBTP`), and automated gate scripts passed, visual inspection of the 9-shot contact sheet and code review of `10_Shorts/_assemble_031_short2_v01.py` revealed **four visual defects** requiring a clean `v02` rebuild (`031_short_sat12_solar_wind_air_v02.mp4`, leaving `v01` untouched on NAS):

1. **Synthetic diagonal sine-wave plaid (`get_nebula_wave()`) + painted circle star-dots (`make_cosmic_backdrop()`) across the 9:16 top/bottom backdrop of all 9 shots (`FAIL` — `AGENTS.md` §Standing lessons 7 & §Reference lessons 1):**
   - `get_nebula_wave()` (`9*sin(...) + 6.5*cos(...) + 4.5*sin(...)`) and `make_cosmic_backdrop()` (`ImageDraw.ellipse` dots) paint a synthetic blue plaid/dot pattern across `y=0..656` and `y=1264..1920` with visible horizontal band seams on every shot.
   - **Required Fix in `v02`:** Remove `get_nebula_wave()` and `make_cosmic_backdrop()` completely. Reframe shots to full `9:16` (`1080x1920`) where source resolution permits (`upscale <= 2.35x`), or composite the `16:9` centre band over a clean, natural dark Gaussian-blurred vertical fill derived from that shot's own pixels (with subtle uniform film grain if needed, never synthetic sine waves or painted dots).
2. **Crude cartoon yellow/cyan `ImageDraw.arc` lines (`||||||`) + `plasma_wave` sine ripple + dark halo cutout on `R39a` (`0.00–2.36 s`), `frame0.jpg`, `cover.jpg`, and `R39_loop` (`23.16–24.48 s`) (`FAIL` — `AGENTS.md` §Standing lessons 7):**
   - `render_r39a_open()` draws 12 thick (`width=7..8`) yellow/cyan `od.arc(...)` curves and a 2D `plasma_wave` sine modulation over `svs_20297_van_allen_earth_only.mp4`, and pastes a dark-ringed circular Earth cutout over the existing Earth. Those cartoon arcs are also baked into `frame0.jpg`, `cover.jpg`, and `R39_loop`.
   - **Required Fix in `v02`:** Render `R39a` (`0.00–2.36 s`), `frame0.jpg`, `cover.jpg`, and `R39_loop` directly from clean graded NASA video (`svs_20297_van_allen_earth_only.mp4` or `svs_3822_magfield_left.mp4`) with zero `od.arc()` lines, zero `plasma_wave` sine ripples, and zero dark-ring cutout overlays.
3. **Ghost double-exposed Earth on `R39b` (`2.36–3.32 s`) (`FAIL` — `AGENTS.md` §Standing lessons 7):**
   - `r39b_bowshock` blends `0.42 * limb_arr` (a static whole-Earth Blue Marble globe `GSFC_20171208_Archive_e001788.jpg`) on top of `svs_3822_magfield_left.mp4`, creating a ghost oval Earth superimposed over the magnetic field lines.
   - **Required Fix in `v02`:** Render `R39b` from a single clean moving NASA plate (`svs_3822_magfield_left.mp4` or `iss030e078095_aurora_timelapse.mp4`) without blending a static Earth photograph over it.
4. **Title-card text collision on `R42a` (`9.32–12.68 s`) during the `9.00–14.00 s` parent-title banner (`FAIL` — `AGENTS.md` §Teach on screen):**
   - `R42a` plays `composite_031_r42_column_limb_v01.mp4`, whose burned-in `1 KILOGRAM` / `1 cm²` graphic text sits in the centre of the `16:9` band (`y=841..1086`) directly underneath the white `9.00–14.00 s` parent-title banner (`What Happens When / Earth's Magnetic / Field Flips?`).
   - **Required Fix in `v02`:** Use a clean text-free moving plate (e.g. `hdev_earth_views_iss_2019.mp4` or `nasa_svs_12312_dscovr_epic_earth.mp4`) throughout `9.00–14.00 s` so the parent-title banner never overlaps background graphic labels, or place the column-mass graphic outside `9.00–14.00 s`.
5. **Sync iCloud `OWB UAT` copy on completion:** Ensure the final `031_short_sat12_solar_wind_air_v02.mp4` is copied with matching SHA-256 to both NAS `10_Shorts/` and `OWB UAT/031_shorts_v02/` (in `J2389`, the iCloud `OWB UAT/031_shorts_v01` copy had an earlier `07:47` build `34,169,600 B` instead of the `08:06` `34,077,335 B` NAS file).

---

## 3. Active Short #1 (`J2388`) & Next Actions

- `J2388` (`031 Magnetic Field Flip Short 1 (Test A opening): build 9:16 cold-open cut from v02 + gates (no upload)`) was still `open` when `J2390` was dispatched because `J2390` only had `after: J2389` (`due: 2026-12-02`) while `J2388` had `due: 2026-12-05`.
- **Queue Resolution:**
  1. Set `J2388` `due` to `2026-12-02 18:00` so `J2388` runs immediately next (`J2388` must also use clean 9:16 framing / blurred backdrop from `master_v02` with zero `get_nebula_wave()`, `make_cosmic_backdrop()`, or synthetic arcs).
  2. Queued `031` Short 2 `v02` repair job (`--after J2388 --due "2026-12-02 18:00"`) to rebuild `031_short_sat12_solar_wind_air_v02.mp4` fixing all 4 items above.
  3. Queued `031` Shorts 1 & 2 review + UAT handoff job (`--after <short2_v02_job> --due "2026-12-02 18:00"`) to review both completed Shorts, stage them alongside the already-staged `KEEP` `master_v02.mp4` in `OWB UAT`, set `jobs.py awaits` for Ben's final watch (`Wed 02 Dec 2026 18:00` London slot), and advance `WIP.json`.
