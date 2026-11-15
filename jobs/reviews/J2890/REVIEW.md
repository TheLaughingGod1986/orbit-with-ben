# J2890 — 033 Uranus Long Master (`v04`) Review (`J2829` 5-Part Standard) & Ben UAT Staging

- **Reviewer:** `gemini` (`Gemini 4 Argon (High)`, specialist worker fallback)
- **Date:** 2026-11-15
- **Film:** `033_Why-This-Planet-Has-21-Year-Winters` (`Why Knocked-Sideways Uranus Has 21-Year Winters`)
- **Target Slot:** `Wed 09 Dec 2026 18:00 London`
- **Verdict:** **`KEEP` (`PASS`)** — `033_why_this_planet_has_21_year_winters_master_v04.mp4` (`J2889`) passes all 5 automated gates, resolves `FIX-A`, `FIX-B`, and `FIX-C` from `J2872`, passes all 5 parts of the `J2829` multimodal inspection standard (including complete `audio_input` audition across `0:00–10:29.42` and `moving_video_input` playback across 5 compact `360p` review proxies), and is staged for Ben's UAT watch (`https://board.oppti.dev/api/watch?v=owb-033-v04`).

---

## 1. Files & Hashes Verified

| Artifact | Path | Bytes | SHA-256 |
|---|---|---:|---|
| Master `v04` (`J2889`) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/09_Final-Export/033_why_this_planet_has_21_year_winters_master_v04.mp4` | `357,159,206` | `3712479ae852dd318c4d8d0dfd18f7df08c1a857068c24c3d3792a35a27f11c3` |
| Phone `v04` (`J2889`) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/09_Final-Export/033_why_this_planet_has_21_year_winters_master_v04_PHONE.mp4` | `48,345,183` | `3ef32f4b673431835449a590f2246de19d84ff32a330893709cb2ccf6b954a19` |
| NAS `OWB UAT` (`v04`) | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/033_why_this_planet_has_21_year_winters_master_v04.mp4` (+ `_PHONE.mp4`) | `357,159,206` / `48,345,183` | Identical SHA-256 on both files |
| iCloud `OWB UAT` (`v04`) | `~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/033_why_this_planet_has_21_year_winters_master_v04.mp4` (+ `_PHONE.mp4`) | `357,159,206` / `48,345,183` | Non-evicted local copies verified with identical SHA-256 |
| R2 Stream (`owb-033-v04`) | `watch/owb-033-v04/deac34c6bbb80dbc-033_why_this_planet_has_21_year_winters_master_v04_PHONE.mp4` (`https://board.oppti.dev/api/watch?v=owb-033-v04`) | `48,345,183` | `3ef32f4b673431835449a590f2246de19d84ff32a330893709cb2ccf6b954a19` |

---

## 2. Five-Part `J2829` Inspection Summary

### Part 1 — Automated Gates (`PASS` on `master_v04.mp4`)
All 5 automated gates and technical delivery checks pass on `033_why_this_planet_has_21_year_winters_master_v04.mp4` (`629.416667 s`, `15,106` frames at `24/1` fps CFR, `1920x1080` `h264` + `48 kHz` stereo AAC):
1. **`clip_check.py` (`rc=0`, `PASS`):** `67` rows, `0` fails. The two advisory `WARN` rows (`R04` at `17.97 s` and `R47` at `427.37 s`) land cleanly inside `540 ms` and `500 ms` spoken comma pauses.
2. **`picture_qa.py` (`rc=0`, `PASS`):** `147` cuts, `0` hard fails, **`0` `>15 s` reuse warnings** (maximum consecutive still run across the entire film is `14.12 s <= 15.0 s`, and every still appears `<= 2` times). The `9` advisory `WARN` items in `picture_qa_review.jpg` are smooth atmospheric Uranus crescents and globes (`PIA01391.jpg`, `PIA00346.jpg`, `PIA00032_falsecolor_disk_v03.jpg`, `PIA01279_left_globe.jpg`, `PIA01279_right_globe.jpg`), all inspected full size and verified sharp and clean.
3. **`polish_gate.py` (`rc=0`, `PASS`):** `147` cuts, `0` fails.
4. **`music_gate.py` (`rc=0`, `PASS`):** `uranus_score_bed_v01.mp3`, `629.4 s`, `70.6 BPM` (`66–76 BPM` target), `0` fails.
5. **`sfx_kit.py level` (`rc=0`, `PASS`):** `VO -20.2 LUFS`, `SFX -47.2 LUFS` (`-27.0 LU` relative to VO), `21` hits, `0` fails, `0` warns.
6. **Master Loudness & Technicals (`PASS`):** Integrated loudness `-14.5 LUFS` (`~-14 LUFS` target), true peak `-1.5 dBTP` (`<= -1.0 dBTP` target), `0` black frames.

### Part 2 — Full-Film `0.5 s` (`2 fps`) Contact-Sheet Grid (`1,259` Frames) & `FIX-A` / `FIX-B` / `FIX-C` Verification (`PASS`)
Rendered and inspected `/Volumes/MiniWork/scratch/J2890_review/v04_2fps_01.jpg`..`v04_2fps_06.jpg` (`1,259` frames at `0.5 s` intervals across `00:00.0–10:29.0`) and the full-resolution verification sheet `/Volumes/MiniWork/scratch/J2890_review/fix_abc_verification_v04.jpg`:
- **`FIX-A` (`100% FIXED` across all 7 cuts: `C054, C086, C087, C121, C130, C134, C141`):**
  - `PIA00037.jpg` (`C054 R25` `212.56–217.95 s`, `C086–C087 R39` `342.65–351.51 s`): Left calibration bar zeroed out (`rgb[:, :2] = 0.0`) and anchored flush to the top-right frame corner `(W - nw, 0)` with cosine feathering along the limb, so Ariel's natural curved terminator faces center-left with zero floating straight cutout edges in mid-space.
  - `PIA00141.jpg` (`C121 R56` `505.35–509.60 s`, `C134 R62` `565.10–569.97 s`): Anchored flush to the left frame edge (`ox = 0`) with 48 px cosine feathering into the deep-navy starfield, eliminating the mid-screen vertical cutoff.
  - `PIA00042.jpg` (`C130 R60` `546.50–552.01 s`, `C141 R65` `595.70–600.00 s`): Anchored flush to the left frame edge (`ox = 0`) with 64 px cosine feathering into the starfield.
- **`FIX-B` (`100% FIXED` across all 7 cuts: `C064, C073, C074, C105, C106, C136, C137`):**
  - `PIA01487.jpg` (stair-step parabolic curve diagram) is completely removed from `C064 R30` (`252.30–255.70 s`, replaced by `PIA00346.jpg`) and `C136–C137 R63` (`576.50–583.14 s`, replaced by `stsci_p1906a_right_globe_v04.png`).
  - `PIA01350.jpg` (noisy B&W ring-streak static) is completely removed from `C073–C074 R33` (`284.39–293.78 s`, replaced by `PIA01356.jpg` on `C073` and `PIA01280.jpg` on `C074`, with `C076` using `PIA01280_tighter_v04.jpg` to keep `PIA01280.jpg` at `10.04 s <= 15.0 s`) and `C105–C106 R48` (`427.37–438.19 s`, replaced by `GSFC_20171208_Archive_e000100_right_globe.jpg` on `C105` matching `AURORAS MISS POLES` and `PIA00032_falsecolor_disk_v03.jpg` on `C106` matching `CORKSCREW MAGNETOTAIL`).
- **`FIX-C` (`100% FIXED` across `C107–C111`, `438.19–463.50 s`):**
  - The `25.31 s` 5-cut repeat of `weic2332a_hires.jpg` is broken into `C107–C108` (`weic2332a_hires.jpg`, `10.14 s <= 15.0 s`), `C109–C110` (`PIA01279_left_globe.jpg`, `10.91 s <= 15.0 s`, matching `ICE GIANT MISCONCEPTION`), and `C111` (`stsci_p1906a_right_globe_v04.png`, `4.26 s`, matching `NO SOLID SURFACE`).

### Part 3 — Cut-Boundary Strips (`±3` Frames Across All `146` Internal Boundaries) & Final `3.0 s` (`72` Frames, `f15035..f15106`) (`PASS`)
Rendered and inspected `/Volumes/MiniWork/scratch/J2890_review/cuts_pm3_01.jpg` (`B001–B050`), `cuts_pm3_02.jpg` (`B051–B100`), `cuts_pm3_03.jpg` (`B101–B146`), and `final_3s_72f.jpg` (`f15035..f15106`, `626.417–629.375 s`):
- **First-30s Rule (`PASS`):** Frame 0 starts moving immediately on `R01` (`r01_sourced_composite_v01_silent.mp4`, Uranus + vertical rings); no Orbit, title, logo, or fade before `0:30`; Sentence 1 states the title mystery by `0:07.8`; concrete payoff counter (`R03`, `21 EARTH YEARS`) lands at `0:08.5–0:13.3` and tilt comparison (`R05`, `EARTH 23.44° TILT` vs `URANUS 97.77° TILT`) at `0:18.0–0:24.8`; all 13 cuts in the opening (`928` frames, `0:00–0:38.67`) are `<= 4.00 s` (`n_main <= 96` frames); first chapter card enters after `0:45`.
- **Cut Transitions (`PASS`):** All 146 internal cut boundaries transition cleanly with zero flash frames, black frames, or mid-word VO collisions.
- **Final `3.0 s` (`f15035..f15106`, `626.417–629.375 s`, `PASS`):** Smooth continuous push-in on `R67` (`PIA18182.jpg` full Miranda mosaic over deep-navy starfield) with zero freeze, flash, jitter, or black tail frames.

### Part 4 — Complete Soundtrack Audition via Verified `audio_input` (`0:00–10:29.42`, `PASS`)
Extracted and listened to the complete soundtrack via `read_file` on `/Volumes/MiniWork/scratch/J2890_review/audio_first45s.wav` (`0:00–0:45`), `audio_part1_000_315s.mp3` (`0:00–5:15`), `audio_part2_315_629s.mp3` (`5:15–10:29.42`), and `audio_final25s.wav` (`10:04.40–10:29.42`), and recorded demonstrated `audio_input,moving_video_input` via `chief_relay.py capabilities --agent gemini`:
- **Audio Verdict (`PASS`):** Bit-identical audio stream to `v03` — clear British narration (`Ben Orbit Narrator`), natural `0.70 s` inter-chapter breaths, supportive ambient/pulse score (`-26 dB` under VO) and house SFX (`-27.0 LU` under VO), clean mid-film subscribe beat at `4:19–4:25`, clean hand-off to Pluto (`034`) at `10:01–10:11.3`, and a smooth `18.08 s` post-VO music hold (`611.32–629.42 s`) fading cleanly at the end. Zero audio pops, clicks, stumbles, or clipping.

### Part 5 — Moving Video Proxy Inspection via Verified `moving_video_input` (`PASS`)
Encoded and watched 5 compact `640x360` `.mp4` review proxies (`0.44–2.84 MB` each) via `read_file`:
1. `v04_proxy_first45s_360p.mp4` (`0:00–0:49.5`, `1.09 MB`): Verified smooth opening motion, uncropped pills (`21 EARTH YEARS`, `EARTH 23.44° TILT`, `URANUS 97.77° TILT`, `−224.2 °C RECORD COLD`, `COLDER THAN NEPTUNE`), and fast `<4 s` cut pacing across the first 30 seconds.
2. `v04_proxy_fix_ab_210_305s_360p.mp4` (`210.0–305.0 s`, `1.94 MB`): Verified `C054` (`PIA00037.jpg` anchored top-right with curved limb), `C064–C065` (`PIA00346.jpg` replacing `PIA01487.jpg`), and `C073–C076` (`PIA01356.jpg` + `PIA01280.jpg` + `PIA01280_tighter_v04.jpg` replacing `PIA01350.jpg`) in motion.
3. `v04_proxy_fix_abc_425_512s_360p.mp4` (`425.0–512.0 s`, `2.84 MB`): Verified `C105–C106` (`GSFC_20171208_Archive_e000100_right_globe.jpg` + `PIA00032_falsecolor_disk_v03.jpg` replacing `PIA01350.jpg`), `C107–C111` (`weic2332a_hires.jpg` -> `PIA01279_left_globe.jpg` -> `stsci_p1906a_right_globe_v04.png` breaking the `25.3 s` repeat), and `C121` (`PIA00141.jpg` anchored left) in motion.
4. `v04_proxy_fix_ab_545_602s_360p.mp4` (`545.0–602.0 s`, `1.25 MB`): Verified `C130` & `C141` (`PIA00042.jpg` anchored left), `C134` (`PIA00141.jpg` anchored left), and `C136–C137` (`stsci_p1906a_right_globe_v04.png` replacing `PIA01487.jpg`) in motion.
5. `v04_proxy_final20s_360p.mp4` (`609.40–629.42 s`, `0.44 MB`): Verified final Pluto hand-off line and smooth `18.08 s` post-VO hold on Miranda (`PIA18182.jpg`).

---

## 3. Studio Review Gates (`Teach on screen`, `Polish pass`, & `Per-chapter teaching`)

| Gate | Score | Evidence |
|---|---|---|
| **1. DATA** | **PASS** | `19` animated `24 fps` code graphics across all 6 chapters (`R03` 21-yr counter, `R05` tilt gauge, `R08/R09` temperature & Neptune bars, `R15` Earth-to-Uranus scale, `R16/R17` 19 AU distance & 84-yr orbit, `R18` sideways tilt, `R21/R22` 1977 occultation dips, `R23` 2% charcoal albedo, `R24` 13 rings, `R26` retrograde spin, `R29/R30` seasonal dial, `R36` atmosphere bars, `R38` heat flux, `R43` 900 km/h wind counter, `R46` 60° corkscrew magnetosphere, `R52` interior cutaway, `R54` 5,000 °C core bar, `R59` Miranda 1/7 Moon scale, `R61` 20 km cliff vs Grand Canyon, `R64` 2024 dual-viewpoint diagram). All match `SOURCES.md` and read with sound off. |
| **2. WHO** | **PASS** | All 3 named people have sourced lower-third WHO cards at first mention over feathered archival portraits: William Herschel (`1738–1822 — British astronomer`, `R11`), Johann Elert Bode (`1747–1826 — German astronomer`, `R13`), and Gerard Kuiper (`1905–1973 — Dutch-born astronomer`, `R58`). |
| **3. WHEN** | **PASS** | Every spoken date has a call-out (`13 MARCH 1781`, `1783`, `10 MARCH 1977`, `1851`, `24 JANUARY 1986`, `DECEMBER 2007`, `16 FEBRUARY 1948`, `19 APRIL 2022`, `OCTOBER 2024`). |
| **4. FACT** | **PASS** | Sourced fact beats shown as concise `<= 4`-word cards (`FIRST TELESCOPE PLANET`, `DARK AS CHARCOAL`, `28 LITERARY MOONS`, `AURORAS MISS POLES`, `NO SOLID SURFACE`, `10-MINUTE CLIFF DROP`). |
| **5. STYLE** | **PASS** | All overlays and graphics are house renders (`<= 4` words per label, large house type, lifted navy `luma >= 36`, graded real NASA/ESA/CSA/STScI plates, corner credit labels bottom-left). |
| **6. MOTION** | **PASS** | Every chart and card animates smoothly; no card holds still `> 4 s`; zero back-to-back code graphics (`0` adjacent `CODE` rows across all 67 rows). |
| **7. SFX / MUSIC / GRAIN / SCALE / EXPLAINER / FINISH** | **PASS** | `sfx_kit.py level` PASS (`-27.0 LU` under VO); `music_gate.py` PASS (`629.4 s`, `70.6 BPM`); fine film grain prevents dark-sky banding; every big number has a spoken and visual SCALE comparison (nickel vs softball, 19x Earth distance, >2x Earth winds, 1/7 Earth's Moon, 12x Grand Canyon); `0.42–0.50 s` crossfades and bottom-left agency credits verified. |
| **8. Per-Chapter NUMBER & WORDS** | **PASS** | Every chapter (`Ch 1–6`) contains multiple animated number objects, and every on-screen label matches the spoken VO words at that timestamp. |

---

## 4. UAT Staging & `WIP.json` Advancement

1. **R2 Upload & `watch_uploads.json`:** Uploaded `033_why_this_planet_has_21_year_winters_master_v04_PHONE.mp4` (`48,345,183` bytes) to R2 under watch ID `owb-033-v04` (`https://board.oppti.dev/api/watch?v=owb-033-v04`) and registered in `05_Analytics/kanban/watch_uploads.json`.
2. **Ben UAT Card (`jobs.py awaits`):** Armed `awaits_ben` on `J2890` (`--card OWB:033 --type long --version v04 --due "2026-11-29 18:00" --airs "2026-12-09 18:00"`).
3. **`jobs/WIP.json` Advancement:** Removed `OWB:033` from `active` as it enters Ben's UAT watch. Per Ben's 14 Nov 2026 decision in `studio/plan.json` and `J2864` (pause on new single-question Orbit longs after `034` Pluto until a test format has its result), no new single-question film from `next` is promoted into `active`.
