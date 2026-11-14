# J2383 Review — 034 Pluto Long Master `v01` + Shorts 1 & 2 `v01` (`J2376`, `J2319`, `J2320`)

- **Reviewer:** `gemini` (`Gemini 4 Argon (High)`, `kind: review`, Rule H)
- **Date:** `2026-11-14`
- **Review Standard:** 5-part multimodal review standard (`jobs/reviews/J2829/RULING.md`):
  1. Automated gates re-verified on the exact master files on `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/`.
  2. Full-film `0.5 s` (`2 fps`) contact-sheet grids with burned-in timestamps (`1,294` frames across 6 sheets for long `v01`; `74` frames for Short 1 `v01`; `52` frames for Short 2 `v01`).
  3. Every frame at each internal cut (`±3` frames: `130 × 7 = 910` frames across 3 sheets for long `v01`; `11 × 7 = 77` frames for Short 1 `v01`; `9 × 7 = 63` frames for Short 2 `v01`) and every frame of the final `3.0 s` (`90` frames each for all three files, `J2614` splice-strip standard).
  4. Complete soundtrack heard end-to-end via verified `audio_input` (`read_file` on extracted `.mp3`/`.wav` stems/masters).
  5. Compact `640×360` / `360×640` `.mp4` review proxy clips (`<= 5 MB` each) watched via `read_file` (`moving_video_input`).
- **Overall Decision:** **`FIX` on all three `v01` deliverables** (`034_pluto_frozen_heart_master_v01.mp4`, `034_short01_testA_opening_v01.mp4`, and `034_short02_water_ice_mountains_v01.mp4`). Do not stage `v01` for Ben's UAT watch; rebuild as `v02` per the exact fix checklist in §6 below.
- **Spend:** `£0.00`

---

## 1. Deliverables & Automated Gate Verification (Part 1 of 5)

| Deliverable | Path on `studio-live` NAS | Bytes / SHA-256 | Stream Spec (`ffprobe`) | Automated Gates (`picture_qa`, `polish_gate`, `music_gate`, `clip_check`, `gate_shorts_open`) | Verdict |
|---|---|---|---|---|---|
| **Long Master `v01`** (`J2376`, PR #646) | `09_Final-Export/034_pluto_frozen_heart_master_v01.mp4` | `244,856,833` B<br>`10ff89794493ec04453e0f3f08a2b42682d8955fecc7291b038989413bdb67e2` | `h264` `1920×1080`, `nb_frames=19407` (`646.900 s` video / `646.940 s` container, `avg_frame_rate=646900/21563`), `aac` `48 kHz` stereo | - `picture_qa.py`: `0 fail, 10 warn — PASS` (`130` cuts)<br>- `polish_gate.py`: `PASS` (`-16.5 LUFS`, `-1.0 dBTP`, `21.1 dB` music ducking, `0.0 px` p95 motion jitter because stills are static)<br>- `music_gate.py`: `PASS` (`score_bed_ratio=1.0`, `key_change_cents=46.6`)<br>- `sfx_kit.py level`: `PASS` (`median_below_vo_db=16.5`)<br>- `clip_check.py`: `74 rows — PASS`<br>- **First-30s Rule (`AGENTS.md` / `J2428` / `J2668`):** **FAIL** (static stills at Frame 0 and throughout; Sentence 1 ends at `8.700 s > 8.000 s`; all cuts in `0:00–1:05.76` are `4.53–10.43 s > 4.000 s`) | **`FIX`** |
| **Short 1 `v01` (Test A Cold Open)** (`J2319`, PR #647) | `10_Shorts/short01_testA_opening/06_Final-Exports/034_short01_testA_opening_v01.mp4` | `15,442,374` B<br>`d70031ea19943c70be46bf0084fd71fd4736aebdc730a199b0e83ff1fda402ac` | `h264` `1080×1920` (`9:16`), `30/1` CFR, `nb_frames=1110` (`37.000 s`), `aac` `48 kHz` stereo | - `picture_qa.py`: `0 fail, 1 warn — PASS` (`12` cuts)<br>- `polish_gate.py`: `PASS` (`-14.3 LUFS`, `-2.2 dBTP`, `23.5 dB` ducking)<br>- `music_gate.py`: `PASS`<br>- **`gate_shorts_open.py check --air-date 2026-12-21`:** **HARD FAIL (`full-bleed 9:16`)** — `the picture does not fill 9:16 on 21/37 frames sampled once a second (57%, limit 10%): 2-10s (blur-pad), 14-15s (blur-pad), 19-26s (blur-pad), 29-35s (blur-pad)` | **`FIX`** |
| **Short 2 `v01` (Keeper Water-Ice Mountains)** (`J2320`, PR #648) | `10_Shorts/short02_water_ice_mountains/06_Final-Exports/034_short02_water_ice_mountains_v01.mp4` | `7,540,985` B<br>`f9798f17e5e333511bf7f1edc83d8a0647a087d583b77efd838f6826146a4e29` | `h264` `1080×1920` (`9:16`), `30/1` CFR, `nb_frames=774` (`25.800 s`), `aac` `48 kHz` stereo | - `picture_qa.py`: `0 fail, 1 warn — PASS` (`10` cuts)<br>- `polish_gate.py`: `PASS` (`-14.3 LUFS`, `-2.2 dBTP`, `24.1 dB` ducking)<br>- `music_gate.py`: `PASS`<br>- **`gate_shorts_open.py check --air-date 2026-12-23`:** **HARD FAIL (`full-bleed 9:16`)** — `the picture does not fill 9:16 on 26/26 frames sampled once a second (100%, limit 10%): 0-26s (blur-pad / blur-pad, no edge)` | **`FIX`** |

---

## 2. Full-Film `2 fps` Contact Sheets & `±3` Frame Cut/End Strip Review (Parts 2 & 3 of 5)

### 2.1 Long Master `v01` (`1,294` frames at `2 fps`, `130 × 7 = 910` cut-boundary frames, `90` final frames `643.90–646.87 s`)
1. **Zero Motion on All Still Cuts (`0:00.0–10:46.9`):**
   - Inspected across `long_2fps_01.jpg`..`long_2fps_06.jpg`, `long_cuts_pm3_01.jpg`..`03.jpg`, and `long_final3s_90f.jpg` (`f19317`–`f19406`): every NASA/Wikimedia still (`PIA20291.jpg` at Frame 0 through `PIA02215.jpg` in the `18.0 s` end hold `R74`) is encoded with `-loop 1` and zero camera motion (`render_still()` lines 341–376 of `_assemble_034_full_master_v01.py`). Fails First-30s Rule #1 (Frame 0 must already be moving) and the 4 s still-motion lock.
2. **Opening Pacing Violations (`0:00.0–1:05.76`, `R01–R07`):**
   - `C001` (`4.57 s`), `C002` (`9.13 s`), `C003` (`19.60 s`, after an unbroken `10.43 s` `R02` scale graphic), `C004` (`24.90 s`), `C005` (`30.20 s`), `C006` (`34.73 s`), `C007` (`39.30 s`), `C008` (`44.20 s`), `C009` (`49.10 s`), `C010` (`54.00 s`), `C011` (`60.53 s`), `C012` (`65.77 s`): every single cut in `R01–R07` exceeds the `4.00 s` opening limit (`4.53–10.43 s`).
3. **Top-Left `48×48 px` Alpha-Feathering Corner Glitch on All Starfield-Framed Stills (`R06`, `R23`, `R30`, `R37`, `R40`, `R41`, `R66`, `R67`, `R72`, `R74`):**
   - Visible on `long_2fps_01.jpg` (`0:54.0–1:00.5` `R06` `PIA20155.jpg`), `long_2fps_02.jpg` (`3:08.5–3:12.0` `R23` `File_Nix_e_Hidra.jpg`), `long_2fps_03.jpg` (`3:59.0–4:08.0` `R30`, `5:07.0–5:11.5` `R37`, `5:34.5–5:38.0` `R40` `PIA10103.jpg`, `5:38.5–5:43.5` `R41`), `long_2fps_06.jpg` (`9:22.5–9:28.0` `R66`, `9:28.5–9:34.0` `R67`, `10:09.5–10:14.0` `R72`, `10:41.0–10:46.5` `R74` `PIA02215.jpg`), and `long_final3s_90f.jpg` (`f19317`–`f19406`): a bright grey/white `48×48 px` square artifact appears in the **top-left corner** of the inset image over the `#162238` starry background.
   - **Root cause in `_assemble_034_full_master_v01.py` lines 365–367:** `render_still()` used a nested 1D `geq` alpha expression `a='if(lt(X,48),X*255/48,if(gt(X,{tw}-48),({tw}-X)*255/48,if(lt(Y,48),Y*255/48,...)))'` and overlaid `rgba` onto `yuv444p` without `format=auto`. Where `X < 48` and `Y < 48`, the outer `if(lt(X,48),...)` short-circuits and ignores `Y`, leaving a hard horizontal step along `Y = 0` for `X in 1..47`, and the `yuv444p` overlay corrupts the top-left corner block.
4. **Black Fade-In Frames at KSC Archival Video Cut Entries (`C056` `272.77 s`, `C059` `292.57 s`, `C066` `326.43 s`) & `R34` Substring Asset Collision:**
   - On `long_cuts_pm3_02.jpg`:
     - **`C056 R34>R34 272.77s (+0f..+3f)` (`4:32.77 s`):** solid black frames at cut entry (`ksc_011906_nh_launchchange.mp4` started at `offset=0.0 s`, where `0.0–0.5 s` is a black fade-in, `luma = 28.0 -> 88.3`). Furthermore, `R34` in `shot_list_v01.csv` specifies `ksc_011906_nh_launchchange -> KSC-06pd0099` (`3000×1968` liftoff photo), but `row_assets()` used substring `.find(a["id"])`, matching `"ksc_011906_nh_launch"` inside `"ksc_011906_nh_launchchange"` at index `0` and dropping `KSC-06pd0099`!
     - **`C059 R36>R36 292.57s (+0f..+3f)` (`4:52.57 s`):** solid black frames at cut entry (`ksc_011906_nh_spacesep.mp4` started at `offset=0.0 s`, where `0.0–0.5 s` fades from black, `luma = 18.4 -> 65.3`).
     - **`C066 R39>R40 326.43s (+0f..+3f)` (`5:26.43 s`):** solid black frames at cut entry (`ksc_011906_nh_srbjett.mp4` started at `offset=0.0 s`, where `0.0–0.5 s` fades from black, `luma = 15.9 -> 55.7`).
5. **Truncated `WHO` Cards (`R10`, `R11`, `R58`) & Duplicate `Credit:` Callout Pills (`R10`, `R13`, `R21`):**
   - Because `LAB_RE` in `_assemble_034_full_master_v01.py` (line 45) matched only the last backticked string before `(start–end s)` and truncated to 4 words:
     - **`R10` (`1:11.6–1:15.3`, `C014`):** `WHO #1` card displays `(1906–1997) — American astronomer` with **`Clyde Tombaugh` missing**! Then at `1:15.7–1:19.0` (`C015`), a center-bottom callout pill displays `Wikimedia / CC BY-SA` while bottom-left already says `Wikimedia`.
     - **`R11` (`1:28.8–1:32.6`, `C018`):** `WHO #2` card displays `(1919–2009) — Oxford schoolgirl` with **`Venetia Burney` missing**!
     - **`R13` (`1:43.8–1:47.4`, `C021`):** `LOWELL OBSERVATORY CHOICE` and `Wikimedia / CC BY 2.0` have identical timestamps (`103.8–107.2 s`) and are drawn **on top of each other** at `(W-w)/2, H-130`!
     - **`R21` (`2:48.5–2:52.0`, `C034`):** `U.S. Naval Observatory /` is drawn as a center-bottom callout pill (`Credit:` marker).
     - **`R58` (`8:19.3–8:23.1`, `C101`):** `WHO #3` card displays `(born 1957) — New` (truncated after 4 words!) with **`Alan Stern` missing**!
6. **1-Frame Video Duration Drift (`19,407` vs `19,408` frames):**
   - `nb_frames = 19407` (`646.900 s`) against `646.940 s` audio (`avg_frame_rate = 646900/21563` instead of exact `30/1`). Allocating `19,408` frames (`646.933 s`) makes `avg_frame_rate = 30/1`.

### 2.2 Short 1 `v01` (`74` frames at `2 fps`, `11 × 7 = 77` cut-boundary frames, `90` final frames `34.00–36.97 s`)
1. **57% of Runtime Fails Full-Bleed `9:16` (`gate_shorts_open.py` FAIL):**
   - On `short1_2fps.jpg` and `short1_cuts_pm3.jpg`, 9 of the 12 cuts (`C001` `2.40 s` through `C005` `15.00 s`, and `C006` `18.60 s` through `C011` `34.80 s`) render a horizontal `16:9` band (`1080×608`) centred over a starfield/blurred pad instead of filling `1080×1920`.
   - In `R02a`/`R02b` (`8.80–15.00 s`), the `16:9` `code_graphic_034_r02_sputnik_scale.mp4` is shrunk into the middle band, making its small labels illegible on a phone screen.
2. **Final `3.0 s` (`short1_final3s_90f.jpg`, `f1020` `34.00 s` – `f1109` `36.97 s`) & Opening Timing:**
   - Cut `R04c` (`34.80–36.83 s`, `f1044`–`f1105`) uses a washed-out white section of `File_Video_-_Nasa_s_New_Horizons_-_Pluto_Flyby_14_7_2015__51718116305_.webm.webm`, followed by a 4-frame loop cross-fade (`f1106`–`f1109`, `36.87–36.97 s`) back to `R01a`.
   - Furthermore, `v01` uses the un-trimmed Sentence 1 (`8.700 s > 8.000 s`) rather than the `FIRST30_PLAN.md` `v02` opening (`-2.800 s` splice of `"in distant orbit around our sun,"`, ending Sentence 1 at `5.900 s < 8.000 s` and finishing the Test A Short at `36.500 s` = `1,095` frames after `"mystery."`).

### 2.3 Short 2 `v01` (`52` frames at `2 fps`, `9 × 7 = 63` cut-boundary frames, `90` final frames `22.80–25.77 s`)
1. **100% of Runtime Fails Full-Bleed `9:16` (`gate_shorts_open.py` FAIL):**
   - On `short2_2fps.jpg` (`0.0–25.5 s`), `short2_cuts_pm3.jpg` (`C001`–`C009`), and `short2_final3s_90f.jpg` (`f684`–`f773`), **all 10 cuts (`26/26` sampled seconds = `100%`)** are letterboxed inside a horizontal `16:9` band with blurred top/bottom padding instead of filling `1080×1920`.
2. **Vertical Black Edge Bar on `R01` (`0.00–2.50 s`) and Loop Seam (`25.60–25.77 s`):**
   - On `short2_2fps.jpg` (`00.0s`, `02.0s`, `25.5s`) and `short2_final3s_90f.jpg` (`f768` `25.60 s` – `f773` `25.77 s`), `code_graphic_034_short2_r01_open.mp4` has a hard vertical black bar on the left edge at `0.00–0.50 s` (and during the 6-frame loop cross-fade at `25.60–25.77 s`) and on the right edge at `2.00–2.47 s` (`gate_shorts_open.py` also flags `no edge` at `2s`).

---

## 3. Complete Soundtrack Review via Verified `audio_input` (Part 4 of 5)

All three soundtracks were inspected end-to-end via `read_file` (`audio_input`):
- **Long Master `v01` (`long_audio_part1_000_330s.mp3` `0:00–5:30`, `long_audio_part2_330_647s.mp3` `5:30–10:46.94`, plus uncompressed `.wav` windows `long_audio_first40s.wav`, `long_audio_ch1_64_71s.wav`, `long_audio_final15s.wav`):**
  1. **Pre-Onset Phoneme Blips at 4 of 6 Chapter-Card Silence Insertions (`lay_vo()` bug — `FIX`):**
     - Because `lay_vo()` in `_assemble_034_full_master_v01.py` (lines 535–539) inserted each chapter-card silence at `float(w["raw_start"])` of the first post-card word instead of in the inter-sentence silence before the card (`prev_word_raw_end + 0.600 s`), the speaker's pre-onset consonant/breath (`~30–60 ms` before Whisper's `raw_start`) was stranded *before* the 2.1–2.5 s chapter silence and clipped at the start of the post-card word:
       - **Ch 1 (`R08`, `1:05.76–1:08.26`):** audible vowel blip at `1:05.76` before the silence; `"18th February 1930"` at `1:08.26` has a hard-cut onset.
       - **Ch 2 (`R20`, `2:41.1–2:43.6`):** audible `"J-"` affricate blip right after `"double world?"` at `2:41.1`, and `"June 1978"` at `2:43.6` starts as `"-une 1978"`.
       - **Ch 3 (`R33`, `4:25.2–4:27.3`):** `"19th January 2006"` at `4:27.3` is intelligible, though cut at `raw_start`.
       - **Ch 4 (`R45`, `6:14.8–6:17.0`):** slight pre-onset blip after `"nothing changes?"` at `6:14.8` before `"Wrong."` at `6:17.0`.
       - **Ch 5 (`R54`, `7:40.2–7:42.3`):** clean pause before `"Here is the biggest misconception"`.
       - **Ch 6 (`R64`, `9:05.2–9:07.4`):** audible `"L-"` pre-onset blip after `"captured twin?"` at `9:05.2` before `"Looking back"` at `9:07.4`.
     - **Verified Fix (`FIRST30_PLAN.md` §2.2 & §4.1):** Inserting all 6 chapter-card silences at `prev_word_raw_end + 0.600 s` (`65.760 s`, `159.220 s`, `261.140 s`, `368.220 s`, `451.660 s`, `534.260 s`, where `±20 ms peak = 0.000000`) eliminates every pre-card blip and post-card clipping while keeping total samples and downstream word timestamps 100% unchanged.
  2. **Narration Prosody, Pronunciations & Mix Balance:**
     - Apart from the 6 chapter-card silence insertion points and the un-trimmed Sentence 1 (`8.700 s > 8.000 s`), the locked `pluto_frozen_heart_vo_v03.wav` narration (`1,291` words), the Ch 5 (`"water ice"`) and Ch 6 (`"Real Worlds."` at `10:28.5`) `v05` pickups (`J2347`/`J2352`), the `18.0 s` end-screen music tail (`10:28.94–10:46.94` fading cleanly to silence), and the SFX/score bed balance (`-16.5 LUFS`, `21.1 dB` ducking) are clean by ear.
- **Short 1 `v01` (`short1_audio.mp3`, `37.00 s`, `-14.3 LUFS`, `-2.2 dBTP`):**
  - Clean narration, music bed, and SFX mix by ear, ending cleanly after `"and solved that mystery."` (`36.02 s`). For `v02`, must use the `FIRST30_PLAN.md` spliced opening (`-2.800 s` removing `"in distant orbit around our sun,"` at `2.000–4.800 s` raw) so Sentence 1 ends at `5.900 s < 8.000 s` and the cut finishes at `36.500 s` (`1,095` frames).
- **Short 2 `v01` (`short2_audio.mp3`, `25.80 s`, `-14.3 LUFS`, `-2.2 dBTP`):**
  - **100% clean by ear (`KEEP` audio stems for `v02`):** *"Why can towering mountains stand beside a flowing glacier between minus 226 and minus 240 degrees Celsius? Here is the biggest misconception about Pluto. On Earth, water ice is a soft glacier that melts, and rock is the solid ground beneath it. Pluto's two to three kilometer mountains are big blocks of water ice, sometimes coated with frozen gases like methane."* Zero clicks, truncations, or bed clashes. `v02` should reuse the exact locked `25.800 s` audio stems (`034_short02_water_ice_mountains_v01_stem_vo.wav`, `stem_sfx.wav`, `stem_bed.wav`).

---

## 4. Compact `360p` Moving-Video Proxy Inspection via `read_file` (Part 5 of 5)

Watched via `read_file` (`moving_video_input`, all `< 5 MB`):
- `long_proxy_first45s_360p.mp4` (`0:00–0:45`, `1.44 MB`): confirmed motionless `PIA20291.jpg` at Frame 0 (`0:00–0:04.57`), unbroken `10.43 s` `R02` scale graphic (`0:09.15–0:19.59`), and `> 4.0 s` cuts throughout.
- `long_proxy_final15s_360p.mp4` (`10:31.94–10:46.94`, `292 KB`): confirmed motionless `PIA02215.jpg` end-screen hold with the `48×48 px` top-left corner alpha-feathering artifact over the starfield and clean audio fade-out.
- `short1_proxy_360p.mp4` (`0:00–0:37.0`, `1.88 MB`): confirmed `16:9` horizontal band (`1080×608`) over starfield/blur-pad on `R01b–R02b` (`2.4–15.0 s`) and `R03a–R04b` (`18.6–34.8 s`), plus over-exposed white `R04c` (`34.8–36.8 s`) and 4-frame loop cross-fade at `36.87–36.97 s`.
- `short2_proxy_360p.mp4` (`0:00–0:25.8`, `1.46 MB`): confirmed 100% blur-padded `16:9`-in-`9:16` framing across all 10 cuts, plus the black left/right edge bar on `R01` (`0.0–2.5 s`) and the 6-frame loop cross-fade at `25.60–25.77 s`.

---

## 5. Exact `v02` Fix Checklist (`J2438` + Shorts `v02` Follow-Up)

### 5.1 Long Master `v02` (`034_pluto_frozen_heart_master_v02.mp4` — `J2438`)
1. **Execute `FIRST30_PLAN.md` (`sha256: 0870bcdf52c6f6719babe991d399e2ebf24b5dde320d1cae89a82b639c7e5022`):**
   - Splice out `raw = 2.000..4.800 s` (`-2.800 s`, `"in distant orbit around our sun,"`) from `pluto_frozen_heart_vo_v03.wav` so Sentence 1 ends at **`5.900 s < 8.000 s`** and Sentence 2 payoff finishes at **`16.240 s < 20.000 s`**.
   - Restore `+2.800 s` via the three verified inter-sentence silence insertions (`+1.000 s` at `raw = 39.300 s`, `+0.900 s` at `raw = 54.000 s`, `+0.900 s` at `raw = 60.550 s`) so `R08` starts at `65.760 s` (`frame 1,973`) and `R08–R74` row timings remain 100% unchanged.
   - Re-cut `R01–R07` (`0.000–65.767 s`, frames `0..1,973`) into the **19 cuts (`3.033–3.933 s <= 4.000 s`)** specified in `FIRST30_PLAN.md` §3 (`138` cuts total across `19,408` frames = `646.933 s` at exact `30/1` CFR).
2. **Insert All 6 Chapter-Card Silences at `prev_word_raw_end + 0.600 s` (`lay_vo()`):**
   - Insert the `R08`, `R20`, `R33`, `R45`, `R54`, `R64` chapter-card silences (`2.220 s`, `2.520 s`, `2.080 s`, `2.200 s`, `2.040 s`, `2.180 s`) at **`raw = 65.760 s, 159.220 s, 261.140 s, 368.220 s, 451.660 s, 534.260 s`** (digital silence `±20 ms peak = 0.000000`) instead of `w["raw_start"]`, eliminating the pre-onset blips at Ch 1 (`1:05.8`), Ch 2 (`2:41.1`), Ch 4 (`6:14.8`), and Ch 6 (`9:05.2`).
3. **Sub-Pixel PIL BICUBIC Zoom + 2D Separable Edge Feather in `render_still()`:**
   - Replace static `-loop 1` still rendering with the `polish_gate`-verified symmetric sub-pixel PIL `Image.Transform.EXTENT(..., Image.Resampling.BICUBIC)` zoom (`z = 1.000 -> 1.045`).
   - For starfield-framed stills (`upscale > 1.01`, clamped to `<= 2.00x`), composite the zoomed still over `stars` (`1920×1080` RGB) directly in PIL/NumPy using a true **2D separable alpha feather (`alpha = np.minimum(fx[:, None], fy[None, :])` over `48 px` on all 4 edges)** instead of the broken `ffmpeg` `geq` filter (`lt(X,48)` top-left `48×48 px` corner glitch on `R06, R23, R30, R37, R40, R41, R66, R67, R72, R74`).
4. **Fix `R34` Word-Boundary Asset Matching & Skip `0.0–0.5 s` Black Fade-Ins on KSC Videos (`R34`, `R36`, `R40`):**
   - In `row_assets()`, match asset IDs with word boundaries (`re.search(r"(?<![A-Za-z0-9_.-])" + re.escape(a["id"]) + r"(?![A-Za-z0-9_.-])", text)`) so `R34` matches `ksc_011906_nh_launchchange -> KSC-06pd0099` (`3000×1968` liftoff photo) instead of colliding on substring `ksc_011906_nh_launch`.
   - In `build_plan()`, start `ksc_011906_*.mp4` native video clips at `off = 2.0 s` (instead of `0.0 s`) so `C056` (`R34`), `C059` (`R36`), and `C066` (`R40`) start on clean bright launch/separation footage with zero black fade-in frames.
5. **Fix `WHO` Card Names (`R10`, `R11`, `R58`) & Strip Duplicate `Credit:` Callout Pills (`R10`, `R13`, `R21`):**
   - In `labels_for()`, parse `WHO` markers so the person's name is included on the card:
     - `R10` (`71.6–75.3 s`): `Clyde Tombaugh (1906–1997) — American astronomer`
     - `R11` (`88.8–92.6 s`): `Venetia Burney (1919–2009) — Oxford schoolgirl`
     - `R58` (`499.3–503.1 s`): `Alan Stern (b. 1957) — New Horizons PI`
   - Ignore `Credit:` segments in `markers` (`R10` `Wikimedia / CC BY-SA 2.0`, `R13` `Wikimedia / CC BY 2.0`, `R21` `U.S. Naval Observatory / PD`) since bottom-left source attribution is already rendered by `credit_for()`, preventing duplicate credit pills and fixing the `R13` (`103.8–107.4 s`) double-pill collision.

### 5.2 Short 1 `v02` (`034_short01_testA_opening_v02.mp4`)
1. **Align to `FIRST30_PLAN.md` `v02` Opening (`0.000–36.500 s`, `1,095` frames at `30/1` CFR):**
   - Use the `v02` spliced opening audio (`-2.800 s` removing `"in distant orbit around our sun,"` at `2.000–4.800 s` raw) so Sentence 1 finishes at **`5.900 s < 8.000 s`** and the Short ends cleanly at **`36.500 s` (`1,095` frames, `0.480 s` after `"mystery."` at `36.020 s` edited)** with **no** 4-frame loop cross-fade at the end.
2. **100% Full-Bleed `1080×1920` (`9:16`) Framing Across All 11 Cuts (`gate_shorts_open.py` `0%` padded):**
   - Every visual cut (`Cuts 1–11`, `3.033–3.533 s <= 4.000 s`) must fill the entire `1080×1920` `9:16` canvas with **zero** blur-pad or starfield letterboxing (`<= 2.00x` upscale from high-res `>= 540×960` source regions, using upright `1080×1920` `9:16` renders for the two `R02` scale-graphic beats and replacing the washed-out white `R04c` flyby clip with `PIA14458.jpg` / high-res Pluto mosaic crop).
   - Must pass `gate_shorts_open.py check 034_short01_testA_opening_v02.mp4 --air-date 2026-12-21`, `picture_qa.py`, `polish_gate.py`, and `music_gate.py`.

### 5.3 Short 2 `v02` (`034_short02_water_ice_mountains_v02.mp4`)
1. **Keep Locked `25.800 s` (`774` frames) Audio Stems, Captions & Overlays:**
   - Reuse the verified `034_short02_water_ice_mountains_v01_stem_vo.wav`, `stem_sfx.wav`, and `stem_bed.wav` (`25.800 s`, `-14.3 LUFS`, `-2.2 dBTP`).
2. **100% Full-Bleed `1080×1920` (`9:16`) Framing Across All 10 Cuts (`gate_shorts_open.py` `0%` padded):**
   - Re-render all 10 cuts (`0.00–25.80 s`) to fill `1080×1920` full-bleed `9:16` (`<= 2.00x` upscale, zero blur-pad, zero black left/right edge bar on `R01`, and no 6-frame loop cross-fade to a black-edged frame at `25.60–25.80 s`).
   - Must pass `gate_shorts_open.py check 034_short02_water_ice_mountains_v02.mp4 --air-date 2026-12-23`, `picture_qa.py`, `polish_gate.py`, and `music_gate.py`.
