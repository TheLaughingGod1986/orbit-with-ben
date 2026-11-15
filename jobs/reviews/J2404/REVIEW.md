# J2404 — 033 Uranus Long Master (`v01` & `v02`) Review (`J2829` 5-Part Standard)

- **Reviewer:** `gemini` (`Gemini 4 Argon (High)`, specialist worker fallback)
- **Date:** 2026-11-15
- **Film:** `033_Why-This-Planet-Has-21-Year-Winters` (`Why This Planet Has 21-Year Winters`)
- **Target Slot:** `Wed 09 Dec 2026 18:00 London`
- **Verdict:**
  - **`v01` (`033_why_this_planet_has_21_year_winters_master_v01.mp4`, `J2403`):** **`FIX`** (superseded by `v02` on opening pacing + shares all `v02` visual defects below)
  - **`v02` (`033_why_this_planet_has_21_year_winters_master_v02.mp4`, `J2437` / PR #840):** **`FIX`** (passes all 5 automated gates and fixes the `0:00–0:38.67` First-30s pacing & `R04->R05` cut boundary, but fails visual QA under `J2829` Parts 2, 3, and 5 due to three systemic compositor/asset defects across the 67-row timeline)

---

## 1. Files & Hashes Audited

| Artifact | Path | Bytes | SHA-256 |
|---|---|---:|---|
| Master `v01` (`J2403`) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/09_Final-Export/033_why_this_planet_has_21_year_winters_master_v01.mp4` | `470,321,850` | `9e9712781a99ad07e6bc753728e716cbf5ef1dc4e4ad9b80ea45c1a55f785552` |
| Phone `v01` (`J2403`) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/09_Final-Export/033_why_this_planet_has_21_year_winters_master_v01_PHONE.mp4` | `62,257,633` | `eb164151c98cf400e06e4cb0fb9dc75c55df2c72dd3a951a9d61d7eb18595df0` |
| Master `v02` (`J2437`) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/09_Final-Export/033_why_this_planet_has_21_year_winters_master_v02.mp4` | `443,162,041` | `fa285da159da9861e791c67d003dc048fc66ecd6a31f0aacc4e351bb36a50794` |
| Phone `v02` (`J2437`) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/09_Final-Export/033_why_this_planet_has_21_year_winters_master_v02_PHONE.mp4` | `62,261,464` | `d99c38ecdf00b822926d2a5c5c380c3df887b72db80c7c1d4f577eaa91d1fb37` |
| NAS `OWB UAT` (`v01` & `v02`) | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/` | Matches above | Identical SHA-256 on all 4 files |
| iCloud `OWB UAT` (`v01` & `v02`) | `~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/` | `dataless` (evicted) | Currently carries macOS `compressed,dataless` extended attribute (`Errno 11` until materialised on `KEEP`) |

---

## 2. Five-Part `J2829` Inspection Summary

### Part 1 — Automated Gates (`PASS` on `v02`)
All 5 automated gates and technical delivery checks pass on `v02` (`629.40 s`, `15,105` frames at `24.00 fps` CFR, `1920x1080` `h264` + `48 kHz` stereo AAC):
1. **`clip_check.py` (`rc=0`, `PASS`):** 67 rows, sentence/card boundaries and end-after-VO checks clear. Two advisory `WARN` rows (`R04` at `17.97 s` and `R47` at `427.37 s`) were verified against `02_Voiceover/stt/uranus_vo_v01/stt_raw.json`:
   - `R04 -> R05`: `"tilt,"` ends at `17.700 s` and `"Uranus"` starts at `18.240 s` (`540 ms` pause). In `v01` (`18.49 s`), the cut landed mid-word inside `"Uranus"`; in `v02` (`17.97 s`), it lands cleanly in the `540 ms` comma pause.
   - `R47 -> R48`: `"hours,"` ends at `427.124 s` and `"Uranus'"` starts at `427.624 s` (`500 ms` pause). The cut at `427.37 s` lands cleanly in the middle of the comma pause.
2. **`picture_qa.py` (`rc=0`, `PASS`):** `147` cuts (`v02`) / `144` cuts (`v01`), `0` fails.
3. **`polish_gate.py` (`rc=0`, `PASS`):** `147` cuts (`v02`), `0` low-detail, split-panel, near-black, or noise failures.
4. **`music_gate.py` (`rc=0`, `PASS`):** `uranus_score_bed_v01.mp3`, `629.40 s`, `70.6 BPM` (within `66–76 BPM` brief), `0` fails.
5. **`sfx_kit.py level` (`rc=0`, `PASS`):** `vo_integrated: -20.2 LUFS`, `sfx_integrated: -47.2 LUFS` (`-27.0 LU` relative to VO), `21` hits, `0` fails, `0` warns.
6. **Master Loudness & Technicals (`PASS`):** Integrated loudness `-14.12 LUFS`, true peak `-0.98 dBTP` (`<= -1.0 dBTP` target), LRA `2.72 LU`, `0` black frames, final VO word `"crater."` ends at `611.324 s` followed by an `18.08 s` music hold to `629.40 s`.

### Part 2 — Full-Film `0.5 s` (`2 fps`) Contact-Sheet Grid (`1,259` Frames Inspected)
Rendered and inspected `v02_2fps_01.jpg`..`v02_2fps_06.jpg` (`1,259` frames at `0.5 s` intervals across `0:00.0–10:29.0` with burned-in `mm:ss.d`, `t`, and `f` labels) plus `v01_open_2fps.jpg` (`80` frames across `0:00.0–0:39.5` of `v01`) and `picture_qa_review.jpg`.
- Exposed three major systemic visual defects across the film (`FIX-1`, `FIX-2`, `FIX-3` in §3 below) that automated pixel statistics cannot catch.

### Part 3 — Cut-Boundary Strips (`±3` Frames Across All `146` Internal Boundaries) & Final `3.0 s` (`72` Frames, `f15034..f15105`)
Rendered and inspected `cuts_pm3_01.jpg` (`C001–C050`), `cuts_pm3_02.jpg` (`C051–C100`), `cuts_pm3_03.jpg` (`C101–C146`), `v01_open_cuts_pm3.jpg` (`v01 C01–C08`), and `final_3s_72f.jpg` (`f15034..f15105`, `626.417–629.375 s`):
- **First-30s Rule (`v01` vs `v02`):**
  - `v01` (`J2403`) **FAILS**: 4 of its 7 cuts in `0:00–0:31.55` exceed `4.00 s` (`R01` `4.35 s`, `R03` `5.19 s`, `R04` `4.60 s`, `R05a` `4.45 s`).
  - `v02` (`J2437`) **PASSES**: re-cuts `0:00–0:38.67` (`R01–R07`, `f0..f927`) into 13 cuts (`2.15–3.83 s <= 4.00 s`; 10 cuts in the first `30.0 s`) and splices cleanly at `C013` (`f928`, `38.67 s`) into `R08` with zero duplicate, black, or flash frames.
- **Final `3.0 s` (`f15034..f15105`, `626.417–629.375 s`):** Smooth continuous zoom on `R67` (`PIA18182_miranda_mosaic.jpg`) with zero freeze-frame, flash, or black tail frames (though `R67` exhibits the `build_still_base()` square inset box and `28%` synthetic star bleed; see `FIX-2`).

### Part 4 — Complete Soundtrack Audition via Verified `audio_input` (`0:00–10:29.40`)
Listened to the complete `629.40 s` soundtrack via `read_file` on `audio_first45s.wav` (`0:00–0:45`), `audio_part1_000_315s.mp3` (`0:00–5:15`), `audio_part2_315_629s.mp3` (`5:15–10:29.40`), and `audio_final25s.wav` (`10:04.40–10:29.40`), and recorded `audio_input,moving_video_input` via `chief_relay.py capabilities --agent gemini`:
- **VO Pacing, Section Breath & Mix:** Natural narration cadence throughout (`1.04x` `eleven_v3`), clean `0.70 s` inter-chapter breaths at all 6 chapter joins, subtle supportive ambient bed (`-26 dB` under VO) and house SFX (`-27 LU` under VO), and a clean `18.08 s` post-VO music hold (`611.32–629.40 s`) fading smoothly to silence at `629.40 s`.
- **Previously Flagged Scribe Discrepancies (`J2155`):**
  - `~418.20 s` (`R46`): Narrator clearly speaks `"and offset from the planet's centre"` (Scribe's `"an offset"` was an ASR assimilation artifact).
  - `~573.80 s` (`R63`): Narrator speaks `"On 19th of April 2022"` (natural British spoken expansion of written `"On 19 April 2022"`).
  - `~601.52 s` (`R66`): Narrator speaks `"Next in our Real World series"` (singular `"World"` before `"series"` coarticulated `/s/`).
- **Audible Pronunciation Shift in Chapter 4 (`04:16.5–05:56.8`, `ch04.wav` first half):**
  - In `ch00` (`0:00–0:57`), `ch01` (`0:58–2:28`), `ch02` (`2:28–3:27`), `ch03` (`3:27–4:16`), the second half of `ch04` (`06:07–07:22`), `ch05` (`07:22–08:34`), and `ch06` (`08:34–10:11`), Ben Orbit Narrator (`eleven_v3`) pronounces `"Uranus"` as `/jʊˈreɪnəs/` (**"Yoo-RAY-nus"**).
  - In the first 6 sentences of `ch04.wav` (`04:16.5–05:56.8`, rows `R31–R40`), `eleven_v3` shifts to `/ˈjʊərənəs/` (**"YOOR-uh-nus"**) across 7 occurrences (`4:26`, `4:46`, `5:16`, `5:28`, `5:39`, `5:52`) before returning to **"Yoo-RAY-nus"** at `6:07` (`"21 years later, as Uranus reached its December 2007 equinox..."`). Both are standard dictionary pronunciations of Uranus (`J2155` locked VO without retake); noted here for Chief/Ben awareness (no VO credit spend is queued).

### Part 5 — Moving Video Proxy Inspection via Verified `moving_video_input`
Opened and watched compact `640x360` `.mp4` review proxies (`<= 1.5 MB` each) via `read_file`: `v01_proxy_first45s_360p.mp4` (`0:00–0:45` of `v01`), `v02_proxy_first45s_360p.mp4` (`0:00–0:45` of `v02`), `v02_proxy_r55_360p.mp4` (`490.0–510.0 s`, `R54–R57`), and `v02_proxy_final20s_360p.mp4` (`609.40–629.40 s`, `R66–R67`).
- Confirmed in motion that the `build_still_base()` square inset boxes, `28%` synthetic starfield bleed across dark planet/crater surfaces, and cropped code-graphic pills (`R03`, `R05`, `R08`, `R09`, `R54`) are immediately visible during normal playback.

---

## 3. Required `FIX` Items for `v03` Assembly (`0` Credit Spend — Local Python/FFmpeg Re-Render Only)

### `FIX-1` — Uncrop / Reposition 12 Burned-In Code-Graphic Pills Mutilated by `upscale` + `crop=` (`R03, R05, R08, R09, R23, R25, R29, R30, R35, R38, R43, R54`)
- **Root Cause:** In `_assemble_033_full_master_v01.py` (lines 421–435) and `_render_j2437_v02.py`, when `cuts_033_j2299_v01.json` applies `"upscale": 1.2` and `"crop": "w:h:x:y"` to pre-rendered `1920x1080` code-graphic `.mp4` clips in `04_Generated-Clips/J2299_code_graphics_v01/`, the crop window slices right through the burned-in text pills near the top/left/right margins.
- **Exact Timecodes & Mutilated Text Observed on Screen (`v02` & `v01`):**
  1. **`R03` (`00:11.0–00:13.9`, `C004`):** Pill `21 EARTH YEARS` is left-cropped to **`"ARTH YEARS"`** (`crop=1580:888:210:96`).
  2. **`R05` (`00:18.0–00:25.1`, `C007–C009`):** Pill `EARTH 23.44° TILT` is sliced along the top edge (`00:18.0–00:20.4`), and `URANUS 97.77° TILT` is left-cropped down to **`"LT"`** in `C008` (`00:20.4–00:22.8`, `crop=1540:866:240:108`) and top-sliced in `C009` (`00:22.8–00:25.1`).
  3. **`R08` (`00:38.7–00:43.9`, `C013–C014`):** Pill `−224.2 °C RECORD COLD` is left-cropped to **`"RECORD COLD"`** (the spoken number `−224.2 °C` is cut off screen!).
  4. **`R09` (`00:43.9–00:48.9`, `C015`):** Pill `COLDER THAN NEPTUNE` is left-cropped to **`"TUNE"`**.
  5. **`R23` (`03:06.6–03:13.0`, `C049–C050`):** Pills `DARK AS CHARCOAL` and `2% REFLECTED LIGHT` are clipped against the top-right edge.
  6. **`R25` (`03:22.4–03:27.5`, `C053`):** Pill `28 LITERARY MOONS` is left-cropped down to **`"05"`**.
  7. **`R29` (`03:56.8–04:08.5`, `C061–C063`):** Pill `84-YEAR ORBIT` is left-cropped to **`"-YEAR ORBIT"`**, and `21-YEAR WINTER` is left-cropped to **`"YEAR WINTER"`**.
  8. **`R30` (`04:08.5–04:12.2`, `C064`):** Pill `POLE FACES SUN` is left-cropped to **`"LE FACES SUN"`**.
  9. **`R35` (`05:04.0–05:08.2`, `C078`):** Pill `82.5% HYDROGEN` is sliced in half at the top edge.
  10. **`R38` (`05:34.8–05:43.0`, `C085–C086`):** Pill `30 AU VS 19 AU` is left-cropped to **`"FLUX"`**.
  11. **`R43` (`06:22.4–06:29.0`, `C096–C097`):** Pill `900 KM/H WINDS` is left-cropped to **`"KM/H WINDS"`**, and `560 MPH JETS` is left-cropped to **`"0 MPH JETS"`**.
  12. **`R54` (`08:07.3–08:13.0`, `C117–C118`):** Pill `CORE NEAR 5,000 °C` is left-cropped to **`"5,000 °C"`** at the top edge.
- **Fix for `v03`:** Never crop across burned-in text pills on `J2299_code_graphics_v01` clips. Either render the `J2299_code_graphics_v01` clips at full `1920x1080` (`upscale: 1.0`, no `crop` that intersects the pill safe zone `y < 140` or `x > 1200`), or apply sub-cut camera motion only to the diagram layer *before* compositing the pill overlay in the safe zone (`5%–10%` title-safe margin).

### `FIX-2` — Fix `build_still_base()` Harsh Rectangular Inset Boxes & `28%` Synthetic Starfield Bleed Across Still Rows
- **Root Cause:** In `_assemble_033_full_master_v01.py` (lines 352–399) and `_render_j2437_v02.py` (lines 72–113), `build_still_base()`:
  1. Pastes non-`16:9` square/portrait astronomical photographs (`PIA00032_left_globe.jpg`, `apollo17_blue_marble.jpg`, `stsci-h-p1906a-f_uranus_globe.png`, `PIA01391.jpg`, `PIA18182_miranda_mosaic.jpg`, `nh-pluto-in-true-color_2x_1080p.jpg`, etc.) centered inside a bright blurred background halo with an unfeathered rectangular border (`2px` stroke + sharp box step), creating a conspicuous grey/black square box floating in the middle of the screen (`R02`, `R04`, `R06`, `R07`, `R14`, `R16`, `R18`, `R21`, `R24`, `R25`, `R27`, `R31`, `R32`, `R33`, `R34`, `R39`, `R40`, `R42`, `R44`, `R45`, `R50`, `R56`, `R59`, `R60`, `R62`, `R63`, `R65`, `R66`, `R67`).
  2. Executes `arr_fg = np.clip(arr_fg * 0.72 + bg_patch * 0.28, 28.0, 224.0)`, which blends `28%` of `bg_canvas` (including `1,800` bright 2×2-pixel synthetic white stars and sinusoidal wave bars!) directly **over the foreground subject**, stamping white star dots across the dark night side of Uranus, Miranda's craters, Pluto, Herschel's 1781 paper (`R12`), and William Herschel's coat (`R10`, `R13`).
- **Fix for `v03`:**
  - **Never blend `bg_patch` (`1,800` synthetic stars) on top of the foreground subject (`arr_fg`).** Keep `arr_fg` at `100%` opacity inside the subject area.
  - **For astronomical globes/crescents on black space (`PIA00032`, `apollo17_blue_marble`, `stsci-h-p1906a-f`, `PIA01391`, `PIA18182`, `nh-pluto-in-true-color`, `PIA00032_uranus_full`, `voyager2_uranus_crescent`, etc.):** Either scale-to-fill `1920x1080` where the composition permits, or feather the dark space border of the square plate (`48–64 px` cosine alpha ramp + black-level match to the surrounding deep-space canvas) so the planet/moon floats seamlessly in continuous deep space with **zero visible rectangular box seam** while keeping subtle star/nebula texture strictly in the background surround (outside the planet disc) to satisfy `polish_gate.py`.
  - **For historical portraits & documents (`william_herschel_portrait`, `johann_bode_portrait`, `gerard_kuiper_portrait`, `herschel_1781_comet_paper`, `herschel_40ft_telescope`):** Present the clean `100%` opaque portrait/document frame (with a subtle feathered vignette or clean archival frame) over the dark background without stamping synthetic stars onto the portrait face, coat, or paper text.

### `FIX-3` — Replace 12 Narrow Voyager 2 Ring-Strip Diagnostic Plates (`PIA01985`, `PIA01977`, `PIA00142`, `PIA01984`) & `R57` Indoor Window-Glare Still (`mcdonald_observatory_dome.jpg`)
- **Root Cause:** As already ruled `FIX` in `J2400` (`033 Uranus Short 2` review), `PIA01985.jpg`, `PIA01977.jpg`, `PIA00142.jpg`, and `PIA01984.jpg` are narrow Voyager 2 ring-strip / starfield-streak diagnostic crops that read on screen as flat grey rectangles with diagonal ruled lines rather than recognizable planetary imagery:
  - `PIA01985.jpg` (flat white/grey rectangle with 5 ruled black lines): used in **`R22`** (`03:03.4–03:06.6`, `13 FAINT RINGS`) and **`R53`** (`07:57.5–08:07.3`, `9,000 °F CORE` / `4,982 °C NEAR CORE` — 9.8 s of a grey ruled rectangle while discussing Uranus's superheated fluid mantle and core!).
  - `PIA01977.jpg` (dark grey square with two diagonal white lines): used in **`R28`** (`03:53.5–03:56.8`, `EARTH-SIZED IMPACT`), **`R47`** (`07:07.3–07:12.9`, `AURORAS MISS POLES`), **`R48`** (`07:12.9–07:19.1`, `CORKSCREW MAGNETOTAIL`), **`R50`** (`07:33.7–07:38.2`), and **`R51`** (`07:38.2–07:43.4`, `NO SOLID SURFACE`).
  - `PIA00142.jpg` (vertical stepped strip of false-color lines): used in **`R30`** (`04:12.2–04:15.8`), **`R33`** (`04:48.5–04:50.2`), **`R49`** (`07:19.1–07:22.0`), and **`R63`** (`09:36.3–09:43.0`, `2023–2032 DECADAL SURVEY` / `TOP PRIORITY MISSION`).
  - `PIA01984.jpg` (grainy grey starfield streak crop): used in **`R12`** (`01:20.8–01:27.9`, `1783`) and **`R17`** (`02:06.8–02:13.3`, `19 ASTRONOMICAL UNITS`).
  - `mcdonald_observatory_dome.jpg` in **`R57`** (`08:34.2–08:40.7`, `16 FEBRUARY 1948`): vertical portrait photo taken from indoors looking out through window blinds and bright window-pane reflection glare.
- **Fix for `v03` (using approved plates & code-graphics already in `03_Reference-Material/harvest_J2299_v01/` and `04_Generated-Clips/`):**
  - Replace the 12 narrow diagnostic strip rows with recognizable full-planet / ring-system / moon plates and diagrams already on disk:
    - **`R12` (`01:20.8–01:27.9`, `1783`):** Use `herschel_1781_comet_paper.png` (alternate pan/zoom framing) or `voyager2_uranus_true_false_color.jpg` (`PIA00032_left_globe.jpg` full globe).
    - **`R17` (`02:06.8–02:13.3`, `19 ASTRONOMICAL UNITS`):** Use `R17` orbital distance code-graphic or `stsci-h-p1906a-f_uranus_globe.png` / `weic2310a_jwst_uranus_wide.jpg`.
    - **`R22` (`03:03.4–03:06.6`, `13 FAINT RINGS`):** Use `weic2310a_jwst_uranus_rings.jpg` or `keck_uranus_rings_ir.jpg` (which clearly show the 13 rings around the planet).
    - **`R28` (`03:53.5–03:56.8`, `EARTH-SIZED IMPACT`):** Use `r01_sourced_composite_v01_silent.mp4` or a tilted-axis impact diagram / `stsci-h-p1906a-f_uranus_globe.png`.
    - **`R30` (`04:12.2–04:15.8`) & `R33` (`04:48.5–04:50.2`):** Use `voyager2_in_flight.jpg` / `PIA01391.jpg` / `weic2310a_jwst_uranus_rings.jpg`.
    - **`R47` (`07:07.3–07:12.9`, `AURORAS MISS POLES`), `R48` (`07:12.9–07:19.1`, `CORKSCREW MAGNETOTAIL`), `R49` (`07:19.1–07:22.0`):** Use `hubble_uranus_aurora_2017.jpg` and clean code-graphic dipole/corkscrew magnetotail diagrams (`R46` magnetic tilt graphic / `weic2310a_jwst_uranus_wide.jpg`).
    - **`R50` (`07:33.7–07:38.2`), `R51` (`07:38.2–07:43.4`, `NO SOLID SURFACE`), `R53` (`07:57.5–08:07.3`, `9,000 °F CORE` / `4,982 °C NEAR CORE`):** Use `R52` internal-structure cross-section graphic (`80% HOT DENSE FLUID` / `ICY FLUID MANTLE`), `R54` temperature-bar graphic (`CORE NEAR 5,000 °C`), and `J2332` `R55` atmospheric cloud-top clip (`r55_01.mp4`) — matching the approved `J2400` Short 2 remediation plan!
    - **`R57` (`08:34.2–08:40.7`, `16 FEBRUARY 1948`):** Crop `mcdonald_observatory_dome.jpg` tightly to the exterior telescope dome (excluding the upper/lower indoor window frame and blind glare) or use `gerard_kuiper_portrait.jpg` + `PIA18182_miranda_mosaic.jpg`.
    - **`R63` (`09:36.3–09:43.0`, `2023–2032 DECADAL SURVEY` / `TOP PRIORITY MISSION`):** Use `weic2310a_jwst_uranus_wide.jpg` / `weic2310a_jwst_uranus_rings.jpg` (showing Uranus and its moons in wide view).

---

## 4. Next Steps & Queue Actions
1. **Queue `v03` Assembly Job (`kind: assembly`):** Build `033_why_this_planet_has_21_year_winters_master_v03.mp4` on top of the `v02` (`J2437`) 147-cut timeline (`0:00–0:38.67` 13-cut opening preserved), applying `FIX-1`, `FIX-2`, and `FIX-3`, re-running all 5 automated gates, and exporting `v03` + `v03_PHONE.mp4` to `09_Final-Export/`, NAS `OWB UAT`, and iCloud `OWB UAT`.
2. **Queue Follow-Up `v03` Review & UAT Staging Job (`kind: review`):** Verify `FIX-1..3` under the 5-part `J2829` standard, materialise iCloud `OWB UAT` copies, upload `v03_PHONE.mp4` to R2, and arm `jobs.py awaits` for Ben's UAT watch (`Wed 09 Dec 2026 18:00 London`).
3. **Note on PR #840 (`codex/j2437-uranus-opening`):** PR #840 contains the `J2437` `v02` opening cut table (`FIRST30_PLAN.md` implementation), which is already on `/Volumes/data/studio-live/.../full_master_v02_pack/`. Merging or closing PR #840 remains a Chief call once `v03` lands.
