# J2872 — 033 Uranus Long Master (`v03`) Review (`J2829` 5-Part Standard)

- **Reviewer:** `gemini` (`Gemini 4 Argon (High)`, specialist worker fallback)
- **Date:** 2026-11-15
- **Film:** `033_Why-This-Planet-Has-21-Year-Winters` (`Why This Planet Has 21-Year Winters`)
- **Target Slot:** `Wed 09 Dec 2026 18:00 London`
- **Verdict:** **`FIX`** (`033_why_this_planet_has_21_year_winters_master_v03.mp4` passes all 5 automated gates, fixes `FIX-1` across all 12 code-graphic pills, fixes `FIX-2` on full globes/crescents/portraits, and replaces all 12 literal `PIA01985`/`PIA01977`/`PIA00142`/`PIA01984` cuts plus `R57` `mcdonald_domes_v03.jpg`; however, Parts 2, 3, and 5 expose 3 remaining visual QA defects — `FIX-A`, `FIX-B`, `FIX-C` below — that must be fixed in `master_v04.mp4` before staging for Ben's UAT watch)

---

## 1. Files & Hashes Audited

| Artifact | Path | Bytes | SHA-256 |
|---|---|---:|---|
| Master `v03` (`J2871`) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/09_Final-Export/033_why_this_planet_has_21_year_winters_master_v03.mp4` | `368,015,084` | `2eb6455414b768fcff4b083107395fe41bd5950c77adc35522eb908585900833` |
| Phone `v03` (`J2871`) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/09_Final-Export/033_why_this_planet_has_21_year_winters_master_v03_PHONE.mp4` | `51,122,408` | `a730c7126394c5295d2f1280b5a41518fbeba70395ba1c8d79369a4eaa1e78d8` |
| NAS `OWB UAT` (`v03`) | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/` | Matches above | Identical SHA-256 on both files |
| iCloud `OWB UAT` (`v03`) | `~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/` | `368,015,084` / `51,122,408` | Local materialised copies verified |

---

## 2. Five-Part `J2829` Inspection Summary

### Part 1 — Automated Gates (`PASS` on `v03`)
All 5 automated gates and technical delivery checks pass on `master_v03.mp4` (`629.416667 s`, `15,106` frames at `24/1` fps CFR, `1920x1080` `h264` + `48 kHz` stereo AAC):
1. **`clip_check.py` (`rc=0`, `PASS`):** 67 rows, `0` fails. The two advisory `WARN` rows (`R04` at `17.97 s` and `R47` at `427.37 s`) land cleanly inside `540 ms` and `500 ms` spoken comma pauses (verified in `J2404`).
2. **`picture_qa.py` (`rc=0`, `PASS`):** `147` cuts, `0` hard fails, `9` advisory `WARN` lines — notably `WARN 7:21 row 49 ... weic2332a_hires.jpg: reuse: on screen 25.3s in a row (look at it: 15s is a lot for one picture)` (addressed in `FIX-C` below).
3. **`polish_gate.py` (`rc=0`, `PASS`):** `147` cuts, `0` fails, `0` warns.
4. **`music_gate.py` (`rc=0`, `PASS`):** `uranus_score_bed_v01.mp3`, `629.4 s`, `70.6 BPM` (`66–76 BPM` target), `0` fails.
5. **`sfx_kit.py level` (`rc=0`, `PASS`):** `vo_integrated: -20.2 LUFS`, `sfx_integrated: -47.2 LUFS` (`-27.0 LU` relative to VO), `21` hits, `0` fails, `0` warns.
6. **Master Loudness & Technicals (`PASS`):** Integrated loudness `-14.5 LUFS`, true peak `-1.5 dBTP` (`<= -1.0 dBTP` target), `0` black frames.

### Part 2 — Full-Film `0.5 s` (`2 fps`) Contact-Sheet Grid (`1,259` Frames Inspected)
Rendered and inspected `/Volumes/MiniWork/scratch/J2872_review/v03_2fps_01.jpg`..`v03_2fps_06.jpg` (`1,259` frames at `0.5 s` intervals across `00:00.0–10:29.0` with burned-in `mm:ss.d`, `t`, and `f` labels), plus dedicated full-resolution verification contact sheets `fix1_12_pills_v03.jpg`, `fix3_replaced_rows_v03.jpg`, and `inspect_suspect_cuts_v03.jpg`:
- **`J2404` `FIX-1` (`100% FIXED`):** `_assemble_033_full_master_v03.py` (line 732) sets `crop = None` for all `J2299_code_graphics_v01` / `code_graphic_033_` clips. All 12 previously mutilated pills (`R03` `21 EARTH YEARS`, `R05` `EARTH 23.44° TILT` & `URANUS 97.77° TILT`, `R08` `−224.2 °C RECORD COLD`, `R09` `COLDER THAN NEPTUNE`, `R23` `DARK AS CHARCOAL` & `2% REFLECTED LIGHT`, `R25` `28 LITERARY MOONS`, `R29` `84-YEAR ORBIT` & `21-YEAR WINTER`, `R30` `POLE FACES SUN`, `R35` `82.5% HYDROGEN`, `R38` `30 AU VS 19 AU`, `R43` `900 KM/H WINDS` & `560 MPH JETS`, `R54` `CORE NEAR 5,000 °C`) render 100% intact within safe margins.
- **`J2404` `FIX-2` on Full Globes, Crescents, `PIA01354.jpg`, and Portraits/Documents (`FIXED`):** All full globes, crescents (`PIA01391`, `PIA00346`, `PIA00143` via `build_opaque_crescent`), `PIA01354.jpg` (via `cover_soft(trim_straight_void(im))`), and archival portraits/documents (`stars=False` behind feathered mask) have `0%` synthetic starfield bleed across foreground subjects and zero rectangular inset boxes.
- **`J2404` `FIX-3` on `PIA01985`, `PIA01977`, `PIA00142`, `PIA01984`, and `R57` (`FIXED` on `R12, R16, R21, R28, R53, R57`):** All 12 literal occurrences of `PIA01985.jpg`, `PIA01977.jpg`, `PIA00142.jpg`, and `PIA01984.jpg` are removed from `cuts_033_v03.json`, and `R57` (`C123–C124`, `514.60–520.83 s`) uses the clean exterior dome crop `mcdonald_domes_v03.jpg` with zero indoor window-blind glare.
- **Remaining Visual Defects Caught in Part 2 (`FIX-A`, `FIX-B`, `FIX-C`):** Detailed in §3 below.

### Part 3 — Cut-Boundary Strips (`±3` Frames Across All `146` Internal Boundaries) & Final `3.0 s` (`72` Frames, `f15035..f15106`)
Rendered and inspected `/Volumes/MiniWork/scratch/J2872_review/cuts_pm3_01.jpg` (`C001–C050`), `cuts_pm3_02.jpg` (`C051–C100`), `cuts_pm3_03.jpg` (`C101–C146`), and `final_3s_72f.jpg` (`f15035..f15106`, `626.458–629.417 s`):
- **First-30s Rule (`PASS`):** 13 cuts in `0:00–0:38.67` (`2.15–3.83 s <= 4.00 s`; 10 cuts in `0:00–0:30.0`).
- **Cut Transitions (`PASS`):** All 146 internal cut boundaries transition cleanly with zero flash frames, black frames, or mid-word VO collisions.
- **Final `3.0 s` (`f15035..f15106`, `626.458–629.417 s`, `PASS`):** Smooth continuous push-in on `R67` (`PIA18182.jpg` full Miranda mosaic, seamlessly blended into deep space with zero box seam and `0%` star bleed on the moon) with zero freeze, flash, or black tail frames.

### Part 4 — Complete Soundtrack Audition via Verified `audio_input` (`0:00–10:29.42`)
Extracted and listened to the complete soundtrack via `read_file` on `/Volumes/MiniWork/scratch/J2872_review/audio_first45s.wav` (`0:00–0:45`), `audio_part1_000_315s.mp3` (`0:00–5:15`), `audio_part2_315_629s.mp3` (`5:15–10:29.42`), and `audio_final25s.wav` (`10:04.40–10:29.42`), and recorded demonstrated `audio_input,moving_video_input` via `chief_relay.py capabilities --agent gemini`:
- **Audio Verdict (`PASS`):** Identical locked soundtrack to `v02` — clean narration cadence, natural `0.70 s` inter-chapter breaths, supportive ambient bed (`-26 dB` under VO) and house SFX (`-27.0 LU` under VO), and a smooth `18.08 s` post-VO music hold (`611.32–629.42 s`) fading cleanly at `629.42 s`. Zero audio pops, clicks, or clipping.

### Part 5 — Moving Video Proxy Inspection via Verified `moving_video_input`
Encoded and watched 4 compact `640x360` `.mp4` review proxies (`0.44–3.75 MB` each) via `read_file`:
1. `v03_proxy_first45s_360p.mp4` (`0:00–0:49.5`, `R01–R09`): Smooth motion, uncropped pills (`R03`, `R05`, `R08`, `R09`), seamless globe integration.
2. `v03_proxy_r21_r31_360p.mp4` (`180.0–252.0 s`, `R21–R31`): Confirmed uncropped pills (`R23`, `R25`, `R29`, `R30`) and clean `R21`/`R28` replacements, while exposing the unfeathered straight cutout edge on `PIA00037.jpg` in `C054` (`212.56–217.95 s`, `FIX-A`) and the stair-step trajectory diagram `PIA01487.jpg` in `C064` (`252.30–255.70 s`, `FIX-B`).
3. `v03_proxy_r47_r58_360p.mp4` (`422.0–522.0 s`, `R47–R58`): Confirmed clean `R53` (`r55_01_r55a_100x_silent.mp4`), `R54` pill, `C122` (`PIA01354.jpg` full-bleed Miranda terrain), and `R57` (`mcdonald_domes_v03.jpg`), while confirming in motion the noisy B&W streak plate `PIA01350.jpg` (`C105–C106`, `427.37–438.19 s`, `FIX-B`), the `25.31 s` unbroken 5-cut repeat of `weic2332a_hires.jpg` (`C107–C111`, `438.19–463.50 s`, `FIX-C`), and the floating straight vertical cutout edge on `PIA00141.jpg` (`C121`, `505.35–509.60 s`, `FIX-A`).
4. `v03_proxy_final20s_360p.mp4` (`609.40–629.42 s`, `R66–R67`): Clean final VO cadence and `18.08 s` post-VO hold over Miranda (`PIA18182.jpg`).

---

## 3. Required `FIX` Items for `v04` Assembly (`£0` Credit Spend — Local Python/FFmpeg Re-Render Only)

### `FIX-A` — Fix 3 Partial-Limb Moon Stills (`PIA00037.jpg`, `PIA00141.jpg`, `PIA00042.jpg`) With Unfeathered Straight Cutout Edges Floating in Mid-Space (7 Cuts: `C054, C086, C087, C121, C130, C134, C141`)
- **Root Cause:** In `_assemble_033_full_master_v03.py` (line 539), `J2871` handled `PIA01354.jpg` (a close-up partial limb of Miranda) via `cover_soft(trim_straight_void(im))`, which fills `1920x1080` cleanly in `C122` and `C126`. However, three other `800x800` Voyager 2 moon close-ups in `cuts_033_v03.json` also have their bright moon surface sliced off by 1–2 straight edges of the source photo while 3 borders are black space (`dark_border = sum(sides) >= 3`):
  1. **`PIA00037.jpg` (Ariel partial quadrant, `800x800`):** Used in **`C054 R25`** (`212.56–217.95 s`, `ARIEL & UMBRIEL · 1851`) and **`C086–C087 R39`** (`342.65–351.51 s`, `1986 SOUTH POLE IN SUN`). The bright moon occupies the top-right quadrant (`x: 416..799, y: 0..643`) and is sliced straight off by the top and right edges of the `800x800` photo, plus there is a vertical black scanline calibration artifact bar on the left (`x ~ 300..330`). Centered in `1920x1080`, the top and right straight edges float in mid-space as a sharp right-angled cutout, and the left black bar sits visible in the blue background.
  2. **`PIA00141.jpg` (Miranda partial limb with Verona Rupes, `800x800`):** Used in **`C121 R56`** (`505.35–509.60 s`) and **`C134 R62`** (`565.10–569.97 s`, `10-MINUTE CLIFF DROP`). The bright moon terrain runs right into the left border (`x = 0`) of the `800x800` source frame (`y: 121..609`) while top/bottom/right are black space. Centered at `x = 420` inside `1920x1080`, the moon is sliced vertically in half at `x = 420` with blue starfield to its left.
  3. **`PIA00042.jpg` (Miranda false-colour wedge, `800x800`):** Used in **`C130 R60`** (`546.50–552.01 s`, `PATCHWORK ICE MOON`) and **`C141 R65`** (`595.40–600.28 s`). The bright wedge touches the left edge (`x = 0`) and has straight diagonal geometric mosaic edges floating in the center of the `1920x1080` starfield.
- **Fix for `v04` (in `_assemble_033_full_master_v04.py` `build_still_base()`):**
  - Never leave a clipped photo edge (`luma > 32` along a source border) floating unfeathered inside the middle of the `1920x1080` frame:
    - For **`PIA00037.jpg`**: zero out the left scanline calibration bar (`x < 350`), scale by `<= 2.25x` (`picture_qa.py` limit `<= 2.35x`), and **anchor the image flush to the top-right corner `(W - nw, 0)`** of the `1920x1080` canvas (with a soft cosine feather on any interior border) so Ariel's clipped top and right edges sit flush against the physical top-right frame boundary while its natural curved terminator faces the center-left of the screen!
    - For **`PIA00141.jpg`**: either anchor the scaled (`2.25x`) image **flush to the left frame edge (`ox = 0`)** so Miranda's clipped left edge sits flush at `x = 0` while its curved limb arcs across the frame, OR add `"PIA00141.jpg"` alongside `"PIA01354.jpg"` in `cover_soft(trim_straight_void(im))` (verifying `picture_qa.py` upscale passes).
    - For **`PIA00042.jpg`**: anchor flush to the left frame edge (`ox = 0`) with a wide (`64 px`) cosine alpha feather along its straight interior mosaic boundaries, OR replace `C130` and `C141` with full-disc moon plates / crops that have no clipped interior edges.

### `FIX-B` — Replace Remaining Unreplaced `PIA01487.jpg` (Stair-Step Mosaic With Drawn White Parabolic Curve in `C064` & `C136–C137`) and `PIA01350.jpg` (Noisy B&W Streak Plate in `C073–C074` & `C105–C106`)
- **Root Cause:** In `J2404/REVIEW.md` `FIX-3`, rows `R30` (`04:12.2–04:15.8`, `C064`), `R47–R48` (`07:07.3–07:19.1`, `C105–C106`), and `R63` (`09:36.3–09:43.0`, `C136–C137`) were flagged by row/timecode for replacement, and `R33` (`C074`) was replaced by `J2871` with `PIA01350.jpg`. Because `J2871` matched only the literal filenames `PIA01985`/`PIA01977`/`PIA00142`/`PIA01984`:
  1. **`PIA01487.jpg` in `C064 R30` (`252.30–255.70 s`) and `C136–C137 R63` (`576.50–583.14 s`, `2023–2032 DECADAL SURVEY` / `TOP PRIORITY MISSION`):** `pool_033_v03.json` mislabels `PIA01487.jpg` as *"Voyager 2 false-colour view of Uranus ring system"*, but the actual image is a B&W stair-stepped Miranda cutout with a **drawn white parabolic curve** across black space (`studio/RULES.md` Lesson 7 violation: never use a plot/diagram plate with drawn lines as a scenic planet shot).
  2. **`PIA01350.jpg` in `C073–C074 R33` (`284.39–293.78 s`, `9.39 s`, `SIX HOURS AT URANUS` / `10 MOONS · 2 RINGS`) and `C105–C106 R48` (`427.37–438.19 s`, `10.82 s`, `AURORAS MISS POLES` / `CORKSCREW MAGNETOTAIL`):** `PIA01350.jpg` is a heavily speckled, low-SNR B&W Voyager ring-streak frame that reads as grey diagonal TV static for `9.39 s` and `10.82 s`.

### `FIX-C` — Break the `25.31 s` Unbroken 5-Cut Repeat of `weic2332a_hires.jpg` (`C107 R49` Through `C111 R51`, `438.19–463.50 s`)
- **Root Cause:** In `J2871`, cuts `C107` (`R49`), `C110` (`R50 c3`), and `C111` (`R51` `NO SOLID SURFACE`) were all replaced with `weic2332a_hires.jpg`, which was already on `C108` (`R50 c1`) and `C109` (`R50 c2`). This created a **5-cut, `25.31 s` consecutive run (`438.19–463.50 s`) of the exact same JWST Uranus image**, triggering `picture_qa.py` `WARN 7:21 row 49 ... reuse: on screen 25.3s in a row (look at it: 15s is a lot for one picture)`.

### Pre-Verified `picture_qa.py`-Compliant Replacement Plan for `FIX-B` & `FIX-C` (`<= 2` Appearances Per Still Across All 147 Cuts)
`picture_qa.py` enforces a hard maximum of `2` non-consecutive appearances per still path (`MAX_STILL_REUSE = 2`) and `<= 15.0 s` consecutive hold. Using under-used plates already in `03_Reference-Material/harvest_J2299_v01/` and `07_Edit-Project/full_master_v03_pack/plates/` (plus one clean crop of the right-hand 2019 Hubble globe from `stsci-h-p1906a-f-1028x543.png` -> `stsci_p1906a_right_globe_v04.png`, `514x543`), apply this exact replacement mapping so every still in the 147-cut timeline stays at `<= 2` appearances and `<= 12 s` consecutive duration:

| Cut(s) | Row | Timecode (`s`) | Pill / Context | Current `v03` Asset | `v04` Replacement Asset | Still Appearance Count After `v04` |
|---|---|---|---|---|---|---|
| `C064` | `R30` | `252.30–255.70` | *(post-`POLE FACES SUN`)* | `PIA01487.jpg` (stair-step curve) | `PIA00346.jpg` (extend `C065`'s Voyager 2 Uranus crescent with distinct camera move so `C064–C065` is one `6.83 s` 2-cut run) | `PIA00346.jpg`: **2 appearances** (`C041–C042`, `C064–C065`) |
| `C073` | `R33` | `284.39–289.20` | `SIX HOURS AT URANUS` | `PIA01350.jpg` (B&W static) | `PIA01356.jpg` (extend `C072`'s Oberon full disc across `C072–C073`, `9.20 s` 2-cut run) | `PIA01356.jpg`: **2 appearances** (`C072–C073`, `C089–C090`) |
| `C074` | `R33` | `289.20–293.78` | `10 MOONS · 2 RINGS` | `PIA01350.jpg` (B&W static) | `PIA01280.jpg` (extend `C075–C076`'s Hubble false-colour Uranus rings & clouds across `C074–C076`, `13.43 s` 3-cut run) | `PIA01280.jpg`: **2 appearances** (`C047–C048`, `C074–C076`) |
| `C105` | `R48` | `427.37–432.60` | `AURORAS MISS POLES` | `PIA01350.jpg` (B&W static) | `GSFC_20171208_Archive_e000100_right_globe.jpg` (extend `C104 R47`'s Hubble Uranus UV aurora globe across `C104–C105`, `10.17 s` 2-cut run directly matching the aurora narration!) | `GSFC_..._right_globe.jpg`: **2 appearances** (`C099–C100`, `C104–C105`) |
| `C106` | `R48` | `432.60–438.19` | `CORKSCREW MAGNETOTAIL` | `PIA01350.jpg` (B&W static) | `PIA00032_falsecolor_disk_v03.jpg` (Voyager 2 false-colour Uranus atmospheric bands globe) | `PIA00032_falsecolor_disk_v03.jpg`: **2 appearances** (`C059–C060`, `C106`) |
| `C107–C108` | `R49–R50` | `438.19–448.33` | `ICE GIANT MISCONCEPTION` | `weic2332a_hires.jpg` | Keep `weic2332a_hires.jpg` on `C107–C108` only (`10.14 s <= 15.0 s`, removing the `25.3 s` `WARN`) | `weic2332a_hires.jpg`: **2 appearances** (`C045–C046`, `C107–C108`) |
| `C109–C110` | `R50` | `448.33–458.27` | *(water/ammonia/methane mantle)* | `weic2332a_hires.jpg` | `PIA01279_left_globe.jpg` (Hubble NICMOS Uranus globe & rings, `9.94 s` 2-cut run) | `PIA01279_left_globe.jpg`: **2 appearances** (`C093`, `C109–C110`) |
| `C111` | `R51` | `458.27–463.50` | `NO SOLID SURFACE` | `weic2332a_hires.jpg` | `stsci_p1906a_right_globe_v04.png` (crop right-hand 2019 Hubble Uranus globe `x:514..1028, y:0..543` from `stsci-h-p1906a-f-1028x543.png`) | `stsci_p1906a_right_globe_v04.png`: **2 appearances** (`C111`, `C136–C137`) |
| `C136–C137` | `R63` | `576.50–583.14` | `2023–2032 DECADAL SURVEY` / `TOP PRIORITY MISSION` | `PIA01487.jpg` (stair-step curve) | `stsci_p1906a_right_globe_v04.png` (`6.64 s` 2-cut run showing Uranus's bright northern polar hood) | `stsci_p1906a_right_globe_v04.png`: **2 appearances** (`C111`, `C136–C137`) |

---

## 4. Next Steps & Queue Actions
1. **Queue `v04` Assembly Job (`kind: assembly`):** Build `033_why_this_planet_has_21_year_winters_master_v04.mp4` on top of `_assemble_033_full_master_v03.py`, applying `FIX-A`, `FIX-B`, and `FIX-C` (`£0` spend), running all 5 automated gates (`0` fails and `0` `>15 s` reuse warnings), and exporting `master_v04.mp4` + `master_v04_PHONE.mp4` to `09_Final-Export/`, NAS `OWB UAT`, and iCloud `OWB UAT`.
2. **Queue Follow-Up `v04` Review & UAT Staging Job (`kind: review`):** Verify `FIX-A..C` under the 5-part `J2829` standard, upload `master_v04_PHONE.mp4` to R2 (`scripts/watch_upload.mjs`), call `jobs.py awaits` for Ben's UAT watch (`Wed 09 Dec 2026 18:00 London`), and advance `033` `edit` / `jobs/WIP.json` on `KEEP`.
