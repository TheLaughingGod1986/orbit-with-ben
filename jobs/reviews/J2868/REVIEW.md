# J2868 Review — 034 Pluto Long Master `v02` + Shorts 1 & 2 `v02` (`J2438`, `J2867`)

- **Reviewer:** `gemini` (`Gemini 4 Argon (High)`, `kind: review`, Rule H)
- **Date:** `2026-11-18`
- **Review Standard:** 5-part multimodal review standard (`jobs/reviews/J2829/RULING.md`) + verification of all `J2383` FIX items (`jobs/reviews/J2383/REVIEW.md @ 79c7174350`):
  1. Automated gates re-verified on the exact `v02` master files on `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/`, NAS `OWB UAT`, and iCloud `OWB UAT`.
  2. Full-film `0.5 s` (`2 fps`) contact-sheet grids with burned-in timestamps (`1,294` frames across 6 sheets for Long `v02`; `73` frames for Short 1 `v02`; `52` frames for Short 2 `v02`) plus full-resolution inspection of all `picture_qa_review.jpg` advisory `WARN` frames and a 16-frame high-resolution `j2383_fixes_verify.jpg` grid.
  3. Every frame at each internal cut (`±3` frames: `137 × 7 = 959` frames across 3 sheets for Long `v02`; `11 × 7 = 77` frames for Short 1 `v02`; `9 × 7 = 63` frames for Short 2 `v02`) and every frame of the final `3.0 s` (`90` consecutive frames each for all three files, `J2614` splice-strip standard).
  4. Complete soundtrack heard end-to-end via verified native `audio_input` (`read_file` on extracted `.mp3`/`.wav` stems/masters, including uncompressed `.wav` windows of the `-2.800 s` Sentence 1 splice and all 6 chapter-card silence boundaries).
  5. Compact `640×360` / `360×640` `.mp4` review proxy clips (`<= 5 MB` each) watched via verified native `moving_video_input` (`read_file`).
- **Overall Decision:** **`KEEP` (`PASS` on all three `v02` deliverables: `034_pluto_frozen_heart_master_v02.mp4`, `034_short01_testA_opening_v02.mp4`, and `034_short02_water_ice_mountains_v02.mp4`).** All `J2383` §5.1, §5.2, and §5.3 FIX items are 100% resolved. Staged in `OWB UAT` (iCloud Drive + NAS archive) and armed via `jobs.py awaits` for Ben's UAT watch.
- **Spend:** `£0.00`

---

## 1. Deliverables, SHA-256 Store Match & Automated Gate Verification (Part 1 of 5)

| Deliverable | Path on `studio-live` NAS & `OWB UAT` (iCloud + NAS) | Bytes / SHA-256 | Stream Spec (`ffprobe`) | Automated Gates (`clip_check`, `picture_qa`, `polish_gate`, `music_gate`, `sfx_kit level`, `gate_shorts_open`) | Verdict |
|---|---|---|---|---|---|
| **Long Master `v02`** (`J2438`, PR #988) | `09_Final-Export/034_pluto_frozen_heart_master_v02.mp4`<br>`OWB UAT/034_pluto_frozen_heart_master_v02.mp4` | `370,954,641` B<br>`e5a886dfef208774cce8ae987e658fba5d7a96cbb5c99a44aadf63516949ba62` | `h264` `1920×1080`, `r_frame_rate=30/1`, `nb_frames=19408` (`646.933 s`), `aac` `48 kHz` stereo (`-14.7 LUFS`, `-1.0 dBTP`, `0` black frames) | - `clip_check.py`: `74 rows — PASS`<br>- `picture_qa.py`: `0 of 138 cuts fail, 10 to look at — PASS`<br>- `polish_gate.py`: `0 of 138 rows failed, 9 to look at — PASS`<br>- `music_gate.py`: `PASS (pluto_score_bed_v01.mp3, 646.9 s, ~66.7 BPM, Pace: 64-74 BPM)`<br>- `sfx_kit.py level`: `PASS (VO -19.9 LUFS, SFX -46.8 LUFS, 8 hits)`<br>- **First-30s Rule (`AGENTS.md` / `FIRST30_PLAN.md`):** **PASS** (Frame 0 moving sub-pixel zoom; Sentence 1 ends at `5.900 s < 8.000 s`; Sentence 2 payoff finishes at `16.240 s < 20.000 s`; 19 opening cuts `3.033–3.934 s <= 4.000 s` across `R01–R07`) | **`KEEP`** |
| **Short 1 `v02` (Test A Opening)** (`J2438`, PR #988) | `10_Shorts/short01_testA_opening/06_Final-Exports/034_short01_testA_opening_v02.mp4`<br>`OWB UAT/034_short01_testA_opening_v02.mp4` | `53,859,275` B<br>`c9a02052ff7a33cba10adc52e440cfe793c6cca1f31e355262acf9fd9c4ba677` | `h264` `1080×1920` (`9:16`), `30/1` CFR, `nb_frames=1095` (`36.500 s`), `aac` `48 kHz` stereo (`-14.10 LUFS`, `-2.10 dBTP`) | - `gate_shorts_open.py`: `PASS (dur=36.5s, audio=-17.1dB, motion=29.06, f0diff=7.29, cut1=2.1s, vo_onset=0.07s, tail_gap=0.48s, 0/37 frames padded at 1/s, 0/73 at 2/s)`<br>- `picture_qa.py`: `0 of 12 cuts fail, 2 to look at — PASS`<br>- `polish_gate.py`: `0 of 12 rows failed, 1 to look at — PASS`<br>- `music_gate.py`: `PASS`<br>- `sfx_kit.py level`: `PASS (VO -16.5 LUFS, SFX -40.1 LUFS, 7 hits)` | **`KEEP`** |
| **Short 2 `v02` (Keeper Water-Ice Mountains)** (`J2867`, PR #990) | `10_Shorts/short02_water_ice_mountains/06_Final-Exports/034_short02_water_ice_mountains_v02.mp4`<br>`OWB UAT/034_short02_water_ice_mountains_v02.mp4` | `59,262,118` B<br>`f3e3d47d0c86be1d297fbf5fade3383126f9c01d94ab2b78444d60dd6a66be73` | `h264` `1080×1920` (`9:16`), `30/1` CFR, `nb_frames=774` (`25.800 s`), `aac` `48 kHz` stereo (`-14.10 LUFS`, `-2.00 dBTP`) | - `gate_shorts_open.py`: `PASS (dur=25.8s, audio=-16.7dB, motion=25.13, f0diff=4.72, cut1=2.4s, vo_onset=0.06s, tail_gap=0.77s, 0/26 frames padded at 1/s, 0/52 at 2/s)`<br>- `picture_qa.py`: `0 of 10 cuts fail, 1 to look at — PASS`<br>- `polish_gate.py`: `0 of 10 rows failed, 1 to look at — PASS`<br>- `music_gate.py`: `PASS`<br>- `sfx_kit.py level`: `PASS (VO -19.4 LUFS, SFX -39.3 LUFS, 3 hits)` | **`KEEP`** |

---

## 2. Verification of All `J2383` §5.1, §5.2 & §5.3 FIX Items

### 2.1 Long Master `v02` (`J2383` §5.1 Items 1–5)
1. **`FIRST30_PLAN.md` Execution (`-2.800 s` Sentence 1 Splice & 19 Opening Cuts `<= 3.934 s`):**
   - Verified in `_assemble_034_full_master_v02.py` (`lay_vo()`, `build_opening_cuts()`), `cuts_v02.json`, `long_vo_seams_verify.wav`, and `long_proxy_first45s_360p.mp4`:
     - Raw `2.000..4.800 s` (`-2.800 s`, `"in distant orbit around our sun,"`) is cleanly spliced out with 8 ms linear silence fades (`<-74 dB`). Sentence 1 (*"Across Pluto's horizon, what would you see on the bright western half of its icy heart?"*) ends at **`5.900 s < 8.000 s`**, and the Sentence 2 payoff (*"A frozen nitrogen glacier about one thousand kilometres wide — larger than Texas and Oklahoma combined — with zero craters."*) finishes at **`16.240 s < 20.000 s`**.
     - The `+2.800 s` offset is restored across three inter-sentence silence insertions (`+1.000 s` at `raw = 39.300 s`, `+0.900 s` at `raw = 54.000 s`, `+0.900 s` at `raw = 60.550 s`) so `R08` starts at `65.760 s` (`frame 1,973`) and `R08–R74` stay 100% locked across `19,408` frames (`646.933 s` at `30/1` CFR).
     - `R01–R07` (`0.000–65.767 s`) are cut into **19 cuts of `3.033–3.934 s <= 4.000 s`** (11 cuts `3.033–3.534 s` in `R01–R04`), with the `R02` scale graphic split into `code_graphic_034_r02a_sputnik_width.mp4` (`6.333–9.833 s`), `PIA20007.jpg` (`9.833–13.300 s`), and `code_graphic_034_r02b_texas_oklahoma_scale.mp4` (`13.300–16.800 s`).
2. **All 6 Chapter-Card Silences Inserted at `prev_word_raw_end + 0.600 s` (`lay_vo()`):**
   - Verified in `_assemble_034_full_master_v02.py` (lines 889–899) and audited by ear in `long_vo_seams_verify.wav`, `long_audio_part1_000_330s.mp3`, and `long_audio_part2_330_647s.mp3`:
     - The 6 chapter-card silences (`R08` `2.220 s`, `R20` `2.520 s`, `R33` `2.080 s`, `R45` `2.200 s`, `R54` `2.040 s`, `R64` `2.180 s`) are inserted at `raw = 65.760 s, 159.220 s, 261.140 s, 368.220 s, 451.660 s, 534.260 s`.
     - All four pre-onset phoneme blips noted in `J2383` (Ch 1 at `1:05.8`, Ch 2 `"J-"` at `2:41.1`, Ch 4 at `6:14.8`, Ch 6 `"L-"` at `9:05.2`) are **100% eliminated**, and every post-card initial word (`"18th February 1930"`, `"June 1978"`, `"19th January 2006"`, `"Wrong."`, `"Here is the biggest misconception"`, `"Looking back"`) has a clean, unclipped onset.
3. **Sub-Pixel PIL BICUBIC Zoom (`1.000 -> 1.045`) + True 2D Separable `48 px` Feather in `render_still()`:**
   - Verified in `_assemble_034_full_master_v02.py` (`_prepare_still_base()` lines 620–633, `render_still()` lines 719–724), `j2383_fixes_verify.jpg`, `long_2fps_01..06.jpg`, and `long_final3s_90f.jpg`:
     - Every still cut moves smoothly from Frame 0 (`PIA20291.jpg`) through the final frame `f19407` (`PIA02215.jpg`) via sub-pixel `Image.Transform.EXTENT` (`Image.Resampling.BICUBIC`).
     - All starfield-framed inset stills (`R06`, `R23`, `R30`, `R37`, `R40`, `R41`, `R66`, `R67`, `R72`, `R74`) use the 2D separable cosine ramp `alpha = 0.5 - 0.5 * cos(pi * minimum(fx[None, :], fy[:, None]))` in RGB before YUV420p encoding. The `48×48 px` top-left corner glitch from `v01` is **100% resolved** on every inset still.
4. **Word-Boundary `row_assets()` Matching (`R34`) & `off = 2.0 s` on KSC Videos (`R34`, `R36`, `R40`):**
   - Verified in `cuts_v02.json`, `j2383_fixes_verify.jpg` (`268.2s`, `273.5s`, `292.6s`, `326.5s`), and `long_cuts_pm3_02.jpg` (`C062`, `C063`, `C066`, `C073`):
     - `R34` now plays `ksc_011906_nh_launchchange.mp4` (`268.100–272.767 s`, `offset=2.0 s`) followed by `KSC-06pd0099.jpg` (`272.767–277.433 s`, `478 KG SPACECRAFT` liftoff photo).
     - `R34` (`268.10 s`), `R36` (`ksc_011906_nh_spacesep.mp4` at `292.567 s`, `offset=2.0 s`), and `R40` (`ksc_011906_nh_srbjett.mp4` at `326.433 s`, `offset=2.0 s`) all enter on bright footage with **zero** black fade-in frames (`black_frames=[]`).
5. **Full `WHO` Card Names (`R10`, `R11`, `R58`) & Stripped Duplicate `Credit:` Callout Pills (`R10`, `R13`, `R21`):**
   - Verified on `j2383_fixes_verify.jpg` (`73.0s`, `77.0s`, `90.5s`, `105.5s`, `170.0s`, `501.0s`) and `long_2fps_01..05.jpg`:
     - `R10` (`71.6–75.3 s`): two-line card displays **`Clyde Tombaugh` / `(1906–1997) — American astronomer`**, and at `75.7–79.0 s` no duplicate `Wikimedia / CC BY-SA` pill appears.
     - `R11` (`88.8–92.6 s`): two-line card displays **`Venetia Burney` / `(1919–2009) — Oxford schoolgirl`**.
     - `R13` (`103.8–107.4 s`): displays a single clean **`LOWELL OBSERVATORY CHOICE`** pill with zero double-pill collision.
     - `R21` (`168.5–172.0 s`): displays the Charon discovery plate with bottom-left `Wikimedia` attribution only and no duplicate `U.S. Naval Observatory /` center-bottom pill.
     - `R58` (`499.3–503.1 s`): two-line card displays **`Alan Stern` / `(b. 1957) — New Horizons PI`**.

### 2.2 Short 1 `v02` (`J2383` §5.2 Items 1–2)
- Verified in `short1_2fps.jpg`, `short1_cuts_pm3.jpg`, `short1_final3s_90f.jpg`, `short1_audio.mp3`, and `short1_proxy_360p.mp4`:
  1. Uses the `FIRST30_PLAN.md` `v02` spliced opening audio (`-2.800 s`), ending Sentence 1 at `5.900 s < 8.000 s` and finishing cleanly at **`36.500 s` (`1,095` frames at `30/1` CFR, `0.480 s` after `"mystery."` at `36.020 s`)** with **zero** end-loop cross-fade.
  2. All 12 cuts fill `1080×1920` (`9:16`) full-bleed (`gate_shorts_open.py` `0/37` frames padded at `1/s`, `0/73` at `2/s`, `upscale <= 1.711x`), using upright `1080×1920` `9:16` renders (`code_graphic_034_r02a_sputnik_width_9x16.mp4` and `code_graphic_034_r02b_texas_oklahoma_scale_9x16.mp4`) for the two `R02` scale-graphic beats and replacing the over-exposed white `R04c` flyby clip with a full-bleed `9:16` crop of `PIA19936.jpg` (`33.47–36.50 s`).

### 2.3 Short 2 `v02` (`J2383` §5.3 Items 1–2)
- Verified in `short2_2fps.jpg`, `short2_cuts_pm3.jpg`, `short2_final3s_90f.jpg`, `short2_audio.mp3`, and `short2_proxy_360p.mp4`:
  1. Reuses the locked `v01` audio stems byte-for-byte (`25.800 s` = `774` frames at `30/1` CFR; VO `d93c149a704c`, SFX `2b8739fe2fd1`, Bed `dbd43603f37f`; `-14.10 LUFS`, `-2.00 dBTP`).
  2. All 10 cuts fill `1080×1920` (`9:16`) full-bleed (`gate_shorts_open.py` `0/26` frames padded at `1/s`, `0/52` at `2/s`, `upscale <= 1.988x`), with `code_graphic_034_short2_r01_open_9x16.mp4` (`0.00–2.40 s`) rendered full-bleed `1080×1920` (zero black left/right edge bars) and `R10` (`PIA19936.jpg`, `22.00–25.80 s`) finishing cleanly at `f773` (`25.77 s`) with **zero** loop cross-fade.

---

## 3. Full-Resolution Inspection of Advisory `picture_qa` / `polish_gate` WARNs (Parts 2 & 3 of 5)

All advisory `WARN` frames on `full_master_v02_pack/picture_qa_review.jpg` (10 items), Short 1 `picture_qa_v02/picture_qa_review.jpg` (2 items), and Short 2 `picture_qa_v02/picture_qa_review.jpg` (1 item) were inspected at full resolution:
- **Long Master `v02` (`picture_qa_review.jpg`):**
  1. `0:19 R03` (`File_The_Pluto_System_As_Seen_By_New_Horizons_Spacecraft.webm.webm`, low edge density `0.0049`): authentic New Horizons LORRI approach orbital animation showing Pluto and Charon rotating around their barycentre over dark space with `13–14 JULY 2015` pill. Clean and sharp. **PASS.**
  2. `2:32 R18` (`PIA20727.jpg`, low edge density `0.0044`): authentic New Horizons high-phase crescent haze silhouette of Pluto (`NASA` credit). **PASS.**
  3. `3:06 R23` (`PIA20287.jpg`, low luma std `17.61`): authentic New Horizons LORRI photograph of small moon Hydra with `5 KNOWN MOONS` pill. **PASS.**
  4. `3:10 R23` & `5:09 R37` (`File_Nix_e_Hidra.jpg.jpg`, low edge density `0.0011`): authentic New Horizons colour/LORRI portrait of Nix and Hydra against dark space (`Wikimedia` credit). **PASS.**
  5. `5:32 R40` (`File_Jupiter_Io.jpg.jpg`, low edge density `0.0051`): authentic New Horizons 2007 Jupiter/Io flyby montage (`Wikimedia` credit). **PASS.**
  6. `7:33 R53` (`File_Sputnik_Planum_floating_hills_-_unannotated.jpg.jpg`, luma std `17.42 < 18.0`): high-resolution unannotated New Horizons MVIC frame of nitrogen-ice convection plains and water-ice hills. **PASS.**
  7. `9:15 R65` & `10:27 R73` (`PIA21590.jpg`, low edge density `0.0055–0.0056`): authentic New Horizons blue atmospheric ring silhouette of Pluto (`NASA` credit). **PASS.**
  8. `9:37 R68` (`File_Reworked_composite_image_of_Arrokoth_rotated.png.png`, `composite` title keyword): authentic New Horizons colour composite of Kuiper Belt contact binary Arrokoth (`35 KM CONTACT BINARY`). **PASS.**
- **Short 1 `v02` (`picture_qa_review.jpg`):**
  1. `0:19 R03a` (`File_Video_-_Nasa_s_New_Horizons_-_Pluto_Flyby_14_7_2015__51718116305_.webm.webm`, luma std `14.24`): authentic New Horizons close-approach flyby footage over Sputnik Planitia (`14TH JULY 2015`). **PASS.**
  2. `0:35 R04c` (`PIA19936.jpg`, `mosaic` title keyword): crisp full-bleed `9:16` crop of New Horizons northern Sputnik Planitia polygonal nitrogen-cell mosaic under the `35.1–36.5 s` end card. **PASS.**
- **Short 2 `v02` (`picture_qa_review.jpg`):**
  1. `0:11 R05` (`File_Video_-_Nasa_s_New_Horizons_-_Pluto_Flyby_14_7_2015__51718116305_.webm.webm`, edge density `0.0312`): authentic New Horizons aerial flyby sequence over Pluto's ice mountains under the `Why Pluto's Frozen Heart Has Zero Craters` title card. **PASS.**

---

## 4. UAT Staging (`OWB UAT` + `jobs.py awaits`)

All three approved `v02` exports are copied and SHA-256 verified in both iCloud Drive `OWB UAT` (`~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/`) and NAS `OWB UAT` (`/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/`), and armed on `J2868` via `jobs.py awaits` for Ben's UAT watch ahead of `OWB:034`'s locked **Sun 13 Dec 2026 18:00 London** air slot.
