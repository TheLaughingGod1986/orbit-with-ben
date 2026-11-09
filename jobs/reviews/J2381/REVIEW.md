# Chief Review — `031` Edit Long Master `v01` (`J2381` / `J2382`)

- **Film:** `031_What-Happens-When-Earths-Magnetic-Field-Flips` (`OWB:031`)
- **Stage:** `edit`
- **Jobs Reviewed:** `J2381` (`33d08fea40`, branch `gemini/J2381-master-v01`), `J2382` (`orphan-review` resolution)
- **Reviewer:** `gemini` (elected Acting Chief under Ben's 26 Oct 2026 succession order; verified via `chief_relay.py status` at `2026-11-08T06:00:31Z`)
- **Master Inspected:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/09_Final-Export/031_what_happens_when_earths_magnetic_field_flips_master_v01.mp4` (`SHA-256: 1b90d78270d4f06b436b42e1a31d700171850511cb7790e43a546da2e20bc69b`, `570.80 s`, `14,270` frames at `25 fps` CFR)
- **Contact Sheet Inspected:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/full_master_v01_pack/picture_qa_review.jpg`
- **Verdict:** **FIX** (rebuild as `master_v02` + build active Shorts 1 & 2 from `SHORTS_PLAN_v01.md`)

---

## 1. Summary of Findings

While `J2381` delivered a 570.80 s (`14,270`-frame) 1080p25 master with locked VO (`magnetic_field_flip_vo_v02a.wav`, `568.28 s`), a chapter-shaped £0 score bed (`magnetic_field_flip_score_bed_v01.mp3`), £0 house SFX (`kit_v01`), and passing automated gate metrics (`clip_check`, `picture_qa`, `music_gate`, `sfx_kit.py level`, `-14.6 LUFS`, `-1.0 dBTP`, `0` black frames), visual inspection of `picture_qa_review.jpg` and code review of `_assemble_031_full_master_v01.py` (`33d08fea40`) revealed **five concrete visual/data defects** that fail channel quality rules (`AGENTS.md` §Standing lessons 7, §Teach on screen, §Reference lessons 1) plus **missing active Shorts 1 & 2 builds**:

1. **Synthetic concentric bullseye / grid overlay (`ensure_wave_overlay()` / `cosmic_wave_ov.png`) burned over dark/low-detail cuts (FAIL — `AGENTS.md` §Reference lessons 1 & §Standing lessons 7):**
   - In `_assemble_031_full_master_v01.py` (`render_video_cut`), any cut whose mid-frame had `mean < 30.0 or p95 < 56.0 or (std < 18.2 and edge < 0.028) or seams` had a static `1920x1080` concentric sine-wave bullseye/grid (`cosmic_wave_ov.png`, `alpha=125`) alpha-composited across the entire frame to artificially pass `polish_gate` luma std / edge density checks.
   - Visually confirmed on `picture_qa_review.jpg` at `0:22` (`R03 c2`), `4:07` (`R25 c1`), `5:29` (`R32 c1`), and `9:10` (`R53 c1`), and by correlation scan (`corr > 0.79`) on `000_R01_c1.mp4` (`R01 0:02`), `032_R15_c2.mp4` (`R15 2:31`), `054_R25_c3.mp4` (`R25 4:18`), `081_R39_c2.mp4` (`R39 6:43`), and `104_R50_c1.mp4` (`R50 8:36`).
   - **Fix required in `v02`:** Remove `ensure_wave_overlay()` and `cosmic_wave_ov.png` completely. Re-render all affected cuts cleanly in `full_master_v02_work/cuts/` using real graded imagery (`eq` / gamma / crop / compositing over real space/Earth plates) without synthetic ripple or grid patterns.

2. **Mislabelled source IDs in `ROW_PLAN` / `cuts_v01.json` masking `> 5` stretches of `nasa_svs_3822_magfield_left.mp4` (FAIL — `AGENTS.md` §Standing lessons 7):**
   - `ROW_PLAN` in `_assemble_031_full_master_v01.py` labels `R03 c2` (`0:22`, `plate_031_r03_epic_magnetosphere_v01.mp4` `2.60–5.16 s`) and `R53 c2` (`9:16`, `plate_031_r53_svs_glowing_field_lines_v01.mp4` `4.72–9.42 s`) as `nasa_svs_12312_dscovr_epic_earth.mp4`, when `_build_missing_mini_composites_v01.py` actually built those segments from `svs_3822_magfield_left.mp4` (visible on `picture_qa_review.jpg` at `0:22 R03`).
   - Counting its real appearances (`R01 c1`, `R03 c2`, `R15 c2–c3`, `R39 c1`, `R47 c2`, `R50 c2`, `R53 c1–c2`), `svs_3822_magfield_left.mp4` appears in **7 stretches** (exceeding `picture_qa.py`'s `max_stretches = 5` cap).
   - **Fix required in `v02`:** Keep `nasa_svs_3822_magfield_left.mp4` to at most **5 stretches** across the film; replace the surplus stretches (e.g. `R03 c2` and `R50 c2` / `R53`) with honest, distinct approved pool plates (`nasa_svs_12312_dscovr_epic_earth.mp4`, `nasa_svs_20297_magnetosphere_earth_only.mp4`, `iss030e078095_aurora_timelapse.mp4`, or `eol-aurora_iss_20110911.mp4` within their own `<= 5` stretch caps) and ensure `cuts_v02.json` records the true source of every single cut.

3. **Empty axis graphic on `R32 c1` (`5:29`, `code_graphic_031_r32a_paleo_high_v01.mp4`) (FAIL — `AGENTS.md` §Teach on screen):**
   - At `5:29` (`R32`), `picture_qa_review.jpg` shows the heading `TODAY'S FIELD` above an empty white L-axis with no bars, no curve, no data values, and the concentric bullseye pattern behind it.
   - **Fix required in `v02`:** Render `R32` using the sourced paleointensity comparison bars from `paleo_comparison_graphics.py` (`TODAY` vs `MILLION-YEAR AVERAGE`, `100,000 YEARS`, `TWICE ITS AVERAGE` synced to `334.02 s`) composited over a graded moving Earth/core background plate so the chart animates and reads with the sound off.

4. **Cropped burned-in source caption on `R54 c2` (`9:27`, `PIA20016.jpg`) (FAIL — `AGENTS.md` §Polish pass 5 & §Standing lessons 7):**
   - At `9:27` (`R54 c2`), the bottom-left corner of the Titan VIMS sphere (`PIA20016.jpg`) includes a truncated burned-in caption from the source JPEG: `...iv. of Idaho (PIA20016)`.
   - **Fix required in `v02`:** Crop or mask `PIA20016.jpg` cleanly above its burned-in bottom caption before building the 16:9 Titan handoff frame on `R54 c2`, and render the clean house corner credit (`NASA/JPL-Caltech/Univ. of Idaho`).

5. **Outdated weekday text on `R22` subscribe card (`3:27`) (FIX — `AGENTS.md` §Locked weekly targets):**
   - `render_sub_card_cut()` renders `"NEW SPACE MYSTERIES EVERY SUNDAY"`, whereas `031` airs in the Wednesday 18:00 London slot (`Wed 02 Dec 2026`) under the 2-longs/week (`Sunday and Wednesday`) schedule.
   - **Fix required in `v02`:** Update line 1 of the `R22` subscribe card to `"NEW SPACE MYSTERIES EVERY WEEK"` (or `"NEW SPACE MYSTERIES SUNDAYS & WEDNESDAYS"`).

6. **Active Shorts 1 & 2 (`SHORTS_PLAN_v01.md`) not yet built:**
   - Per `031` `status.json` (`next: "edit: assemble 54-row 031 Magnetic Field Flip long master v01 (568.28 s) + Shorts"`) and `10_Shorts/SHORTS_PLAN_v01.md` (`J2147`), `031` requires its two active Shorts built and gated (`gate_shorts_open.py check`) before the `031` edit package goes to review and Ben's UAT watch:
     - **Short 1 (Test A Opening Short):** *What Happens When Earth's Magnetic Field Flips?* (`s00–s08`, `0.14–35.32 s` lifted from the clean `v02` master, reframed to `9:16` `1080x1920`, `--test-a`).
     - **Short 2 (Keeper Question Short):** *What If the Solar Wind Blew Earth's Atmosphere Into Space?* (`24.48 s` / `25.00 s`, `s65, s67, s70, s74` from `magnetic_field_flip_vo_v02a.wav` + 9:16 vertical cuts + score bed + `gate_shorts_open.py check`).

---

## 2. Action & Queue Resolution (`J2382`)

1. Set `031` `stages.edit` in `status.json` to `state: "doing"` with `ruling: "FIX"` (`review_job: "J2382"`, `review_evidence: "jobs/reviews/J2381/REVIEW.md"`), preserving `v01` untouched on the NAS (`031_what_happens_when_earths_magnetic_field_flips_master_v01.mp4`).
2. Queue linked `031` `edit` successor jobs:
   - **Long Master `v02` repair & assembly (`--film 031 --stage edit --kind assembly --needs mini`):** Fix all 5 visual/data items above into `031_what_happens_when_earths_magnetic_field_flips_master_v02.mp4` + `full_master_v02_pack/` and pass all 5 gates honestly.
   - **Short 1 (Test A opening) build (`--film 031 --stage edit --kind assembly --needs mini --after <v02_job>`):** Build and gate `031` Short 1 (`What Happens When Earth's Magnetic Field Flips?`) from `SHORTS_PLAN_v01.md` and `master_v02`.
   - **Short 2 (Keeper question) build (`--film 031 --stage edit --kind assembly --needs mini --after <v02_job>`):** Build and gate `031` Short 2 (`What If the Solar Wind Blew Earth's Atmosphere Into Space?`) from `SHORTS_PLAN_v01.md`.
   - **`031` Edit Review (`--film 031 --stage edit --kind review --needs mini --after <short2_job>`):** Review `031` long master `v02` + Shorts 1 & 2 and prepare UAT handoff for Ben's watch.
