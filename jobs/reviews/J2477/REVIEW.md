# J2477 — Review: 032 Titan Long Master v02 (`J2436`) + Stage for Ben UAT Watch

- **Date:** 2026-11-14
- **Reviewer:** `gemini` (`Gemini 4 Argon (High)`, elected acting Chief under the 9 Nov 2026 Chief succession chain)
- **Film:** `OWB:032` (*What Would Happen If You Landed on Titan?*) — November tentpole, airs **Wed 25 Nov 2026 18:00 London**
- **Stage:** `edit` (`032_what_would_happen_if_you_landed_on_titan_master_v02.mp4`, delivered by `J2436`)
- **Spend:** `£0.00`
- **Verdict:** **KEEP (`PASS` — all 5 `J2829` review checks, First-30s Rule, Teach-on-Screen, Per-Chapter `NUMBER`+`WORDS`, and all 5 automated gates PASS; staged for Ben's UAT watch)**

---

## 1. Master File & SHA-256 Verification Across All Three Stores

| Store | Path | Size (bytes) | SHA-256 | Status |
|---|---|---|---|---|
| **Studio-live `09_Final-Export`** | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/09_Final-Export/032_what_would_happen_if_you_landed_on_titan_master_v02.mp4` | `389,705,443` | `519869728d51b42b98435bc971361994d61780c02e2daa3bc0d23f27c80ed073` | **MATCH (`PASS`)** |
| **NAS `OWB UAT`** | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/032_what_would_happen_if_you_landed_on_titan_master_v02.mp4` | `389,705,443` | `519869728d51b42b98435bc971361994d61780c02e2daa3bc0d23f27c80ed073` | **MATCH (`PASS`)** |
| **iCloud Drive `OWB UAT`** | `~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/032_what_would_happen_if_you_landed_on_titan_master_v02.mp4` | `389,705,443` | `519869728d51b42b98435bc971361994d61780c02e2daa3bc0d23f27c80ed073` | **MATCH (`PASS` — materialised locally & verified)** |

- **Technical Delivery Specs (`ffprobe` + `mix_report_v02.json`):**
  - **Video:** `1920x1080` (`16:9`, SAR `1:1`), H.264 High (`avc1`), `yuv420p`, `30/1` fps CFR (`r_frame_rate == avg_frame_rate == 30/1`), `17,563` frames, `585.440 s` (`9m 45.44s`), `0` black frames (`blackdetect d=0.05`).
  - **Audio:** AAC LC `48,000 Hz` stereo, integrated loudness `-14.5 LUFS` (target `-14.0 ± 1.0 LUFS`), true peak `-1.0 dBTP` (ceiling `<= -1.0 dBTP`), LRA `2.4 LU`.
  - **Locked Voice-Over (`J1753` / `J1294`):** `titan_landing_vo_v02b.mp3` (`582.440 s`, SHA-256 `4c995af1bc402f43bd884d3a7641910155a9ed92413de080de1ec351e8373fd9`) is preserved bit-for-bit inside the mix with a `+3.000 s` score-bed tail fade (`582.440 s -> 585.440 s`) so `clip_check.py` passes cleanly (`585.440 s >= 582.380 s + 0.25 s`).

---

## 2. Automated Gate Re-Run Results (All 5 Gates)

All five studio gates were re-run directly against the `v02` master and `SHOT_LIST_v09.csv`:

| Gate | Command / Target | Output | Verdict |
|---|---|---|---|
| **1. `clip_check.py`** | `SHOT_LIST_v09.csv` + `titan_landing_vo_v02_words.json` | `clip_check: 52 rows — PASS (OK: sentence/card boundaries and end-after-VO checks clear.)` | **PASS** |
| **2. `picture_qa.py`** | `032_..._master_v02.mp4 --shots SHOT_LIST_v09.csv` | `picture QA PASS: 0 of 131 cuts fail, 7 to look at` | **PASS** |
| **3. `polish_gate.py`** | `032_..._master_v02.mp4 --shots SHOT_LIST_v09.csv` | `polish gate PASS: 0 of 131 rows failed, 7 to look at` (`0` frozen pairs across all 131 cuts) | **PASS** |
| **4. `music_gate.py`** | `titan_score_bed_v01.mp3 --brief MUSIC_BRIEF_v01.md` | `music gate PASS: titan_score_bed_v01.mp3, 585.4 s, about 70.6 BPM, brief Pace: 68-78 BPM` | **PASS** |
| **5. `sfx_kit.py level`** | `titan_landing_vo_v02b_padded.wav` + `sfx_stem_v02.wav` + `titan_score_bed_v01.mp3` | `SFX level PASS: VO -20.0 LUFS, SFX -46.2 LUFS, 13 hits` (`26.2 dB` below VO) | **PASS** |

---

## 3. Five-Part Multimodal Inspection (`J2829` Standard)

Reviewed directly in this session with demonstrated `audio_input` and `moving_video_input` plus high-resolution frame strips:

1. **Full Audio Listen (`audio_input`):**
   - Inspected `audio_first35s.wav` (`0:00–0:35`), `audio_final15s.wav` (`9:30–9:45.44`), `audio_part1_000_300s.mp3` (`0:00–5:00`), and `audio_part2_300_585s.mp3` (`5:00–9:45.44`).
   - **Findings:** British English narration (`Ben Orbit Narrator`) is warm, steady, and unclipped from the opening word (*"Suppose you step out onto Saturn's largest moon..."*) through the final word (*"...into the next few billion years."*, ending at `582.38 s`). All chapter boundary breaths (`ch00` `180 ms` `qsin` fade at `50.30 s`, `ch02` `20 ms` fade at `107.66 s`, and all remaining seams verified in `J1753`) play cleanly over the `70.6 BPM` ambient score bed (`-38.2 LUFS` under VO). All 13 house SFX cues (`whoosh_soft`, `tick_ruler`, `swell_ warm`) sit unobtrusively (`-46.2 LUFS` integrated) at visual card and reveal boundaries, with zero hits in the final `30 s` (`last SFX at 518.61 s`). After `"years"` ends at `582.38 s`, the score bed holds gently and fades out smoothly to silence at `585.44 s` with zero clicks, pops, or truncation.

2. **Compact 360p Video Proxies (`moving_video_input`):**
   - Inspected `proxy_first45s_360p.mp4` (`0:00–0:45`, `1.29 MB`) and `proxy_final15s_360p.mp4` (`9:30–9:45.44`, `343 KB`) directly as video inputs.
   - **Findings:** Motion in the opening `45 s` is continuous from Frame 0 (`PIA20016.jpg` Cassini golden haze zoom), cutting briskly every `2.80–3.60 s` through `0:32.17`. The `r03` pressure bar comparison (`EARTH 1 BAR` vs `TITAN 1.47 BAR`) animates cleanly at `0:16.53–0:20.13` right on the spoken hook payoff. In the final `15 s` (`9:30–9:45.44`), the `r52` season wheel (`29.5 EARTH YEARS` / `7.5 YR WINTER`), `PIA08369` northern lakes mosaic, and `PIA18182` golden crescent horizon move smoothly with zero stalls or freeze frames through `585.44 s`.

3. **Full-Film `0.5 s` (`2 fps`) Contact Sheets (`1,171` frames across 6 sheets):**
   - Inspected `full_2fps_sheet_01.jpg` (`0:00–1:40`), `sheet_02.jpg` (`1:40–3:20`), `sheet_03.jpg` (`3:20–5:00`), `sheet_04.jpg` (`5:00–6:40`), `sheet_05.jpg` (`6:40–8:20`), and `sheet_06.jpg` (`8:20–9:45.4`).
   - **Findings:** Visual variety, colour grading, and pacing hold across all 52 rows (`131` sub-cuts). Every NASA/ESA/CSA plate carries a clean, legible bottom-left source attribution pill (`NASA / JPL / Space Science Institute`, `ESA / NASA / JPL / University of Arizona`, `NASA / JPL-Caltech / ASU`, `NASA / ESA / CSA / JWST`), and every quantitative/process card uses the house dark-slate badge with high-contrast cream/amber/cyan typography inside the `10%` title-safe margins and clear of the bottom-right duration badge.

4. **`±3` Frame Cut-Boundary Strips (`130` internal cut boundaries, `910` frames across 3 sheets):**
   - Inspected `cuts_pm3_sheet_01.jpg` (`C001–C044`), `cuts_pm3_sheet_02.jpg` (`C045–C088`), and `cuts_pm3_sheet_03.jpg` (`C089–C130`).
   - **Findings:** Every single one of the `130` internal cut transitions (`c-3, c-2, c-1, c0, c+1, c+2, c+3`) is frame-accurate with zero black flash frames, zero white flash frames, zero unrendered slates, and zero duplicate/frozen cut-in or cut-out frames.

5. **Final `3.0 s` Every-Frame Strip (`90` frames, `f17473`–`f17562` / `582.43 s–585.40 s`):**
   - Inspected `final_3s_every_frame_sheet.jpg` (`90` consecutive frames).
   - **Findings:** `PIA18182.jpg` (Cassini limb view across Titan's golden atmospheric crescent) zooms continuously and smoothly across all 90 frames after VO completion (`582.38 s`) right through the final frame `f17562` (`585.40 s`). Zero frozen frames, zero black frames at tail.

---

## 4. First-30s Rule Verification (`AGENTS.md` / `FIRST30_PLAN.md` / `J2435` / `J2436`)

| Rule Requirement | Target | `032` Master `v02` Actual | Status |
|---|---|---|---|
| **1. Frame 0 moves; no Orbit/title/logo/fade in `0:00–0:30`** | Moving visual from `0.00 s`; Orbit after `0:30` | Frame `0` (`0.00 s`) opens on moving `PIA20016.jpg` (Cassini golden nitrogen haze, continuous sub-pixel zoom `1.000 -> 1.045`). First Orbit appearance is `R06a` at `40.40 s`. Zero title card, logo, or black fade. | **PASS** |
| **2. Sentence 1 states the title question (`<= 8.0 s`)** | Ends `<= 8.00 s` | *"Suppose you step out onto Saturn's largest moon, Titan, without a pressure suit."* (`0.00 s – 5.24 s`). Directly answers the title question. | **PASS** |
| **3. No agenda / meta-promise in `0:00–0:30`** | `0` agenda lines | Zero *"In this video..."* or *"Today we'll explore..."* lines; pure second-person physical landing sequence. | **PASS** |
| **4. Concrete visual & spoken payoff by `0:20`** | Card + spoken number `< 20.00 s` | `code_graphic_032_r03_pressure_v01.mp4` (`EARTH 1 BAR` vs `TITAN 1.47 BAR`) lands at **`16.53 s – 20.13 s`** (`3.47 s` before `0:20`) while VO says *"It pushes against your chest about one and a half times harder than the air at sea level on Earth."* (`"one"` at `18.96 s`). | **PASS** |
| **5. Cut every `3–4 s` in `0:00–0:30`** | Every cut `<= 4.00 s` | **10 sub-cuts** across `0.00 s – 32.17 s`: `2.80 s`, `2.80 s`, `3.67 s`, `3.67 s`, `3.60 s`, `3.60 s`, `3.00 s`, `3.00 s`, `3.03 s`, `3.00 s` (mean `3.22 s`, max `3.67 s <= 4.00 s`). | **PASS** |
| **6. No chapter card before `0:45`** | First chapter card `>= 45.00 s` | Chapter 1 (`R07`, *A World Behind Orange Glass*) enters at **`50.87 s`**. | **PASS** |

---

## 5. Inspection of the 7 `picture_qa` / `polish_gate` WARNs

All 7 advisory `WARN` rows on `picture_qa_review.jpg` were inspected at full `1920x1080` resolution:

1. **`#1 0:02 R01` (`PIA20016.jpg`, `flat colour std=4.4`):** Authentic Cassini wide-angle limb photograph of Titan's golden photochemical nitrogen haze over dark space. Natural atmospheric gradient with clean `NASA / JPL / Space Science Institute` credit pill. **PASS.**
2. **`#12 0:37 R05` (`032_r05_rain_preview_v01.png`, `flat colour std=5.5`):** `J2378`-approved house preview card (`LIQUID METHANE RAIN` / `SLOW-FALLING DROPS` / `6X EARTH DROP SIZE`) composited over moving Titan cloud plate (`PIA20022.jpg`). Crisp typography and clean layout. **PASS.**
3. **`#47 3:24 R20` (`032_r20_fact_v01.png`, `flat colour std=7.2`):** `J2378`-approved house data card (`HUYGens DESCENT` / `2 HOURS 27 MINUTES` / `THROUGH TITAN'S HAZE`) over Cassini atmospheric entry backdrop. Legible at `168 px` and `1080p`. **PASS.**
4. **`#90 6:40 R37` (`032_r37_spark_question_v02.png`, `flat colour std=6.8`, `18% edge density`):** `J2378`-approved chemistry comparison card (`95% NITROGEN + 5% METHANE` / `TRACE OXYGEN (<0.1%)` / `NO OXIDISER = NO FLAME`) over moving Titan surface plate (`PIA07232_huygens_surface_colour.jpg`). Clean hierarchy, zero text clipping. **PASS.**
5. **`#98 7:15 R41` (`032_r41_no_flame_v01.png`, `flat colour std=6.0`):** `J2378`-approved mechanism card (`STRIKE A MATCH ON TITAN` / `NO FREE OXYGEN` / `METHANE CANNOT BURN`) over moving surface plate. Crisp and accurate. **PASS.**
6. **`#101 7:26 R41` (`032_r41_fact_v01.png`, `flat colour std=6.3`):** `J2378`-approved reversed-combustion card (`EARTH vs TITAN FIRE` / `EARTH: FUEL + OXYGEN JET` / `TITAN: OXYGEN JET IN METHANE AIR`). Clean two-column teaching diagram. **PASS.**
7. **`#126 9:24 R51` (`PIA20016.jpg`, `flat colour std=4.4`):** Closing return to Cassini's golden haze limb view (`PIA20016.jpg`) before the final seasonal wheel and crescent horizon. Natural spacecraft plate. **PASS.**

---

## 6. Teach-on-Screen, Per-Chapter (`NUMBER` + `WORDS`) & Polish-Pass Audit

- **Per-Chapter `NUMBER` + `WORDS` Coverage (`studio/RULES.md`):**
  - **Ch 0 (`0:00–0:50`):** `NUMBER` (`R03` `1 BAR vs 1.47 BAR` at `0:16.53`, `R04` `-179°C` at `0:26.13`) + `WORDS` (`R02` `NO BOILING BLOOD`, `R05` `LIQUID METHANE RAIN`).
  - **Ch 1 (`0:50–1:47`):** `NUMBER` (`R08` `16 EARTH DAYS`, `R09` `5,150 KM` vs Mercury `4,880 KM`, `R11` `95% NITROGEN / 5% METHANE`) + `WORDS` (`R07` chapter card, `R10` `THOLIN HAZE`).
  - **Ch 2 (`1:47–3:53`):** `NUMBER` (`R15` `3.2 BILLION DOLLARS`, `R16` `20 YEARS / 127 FLY-BYS`, `R19` `1.2 BILLION KM`, `R20` `2 HOURS 27 MINUTES`, `R22` `0.14 G`, `R23` `4.5 M/S`, `R24` `72 MINUTES`) + `WORDS` (`R14` chapter card, `R17` `HUYGENS PROBE`, `R21` `PARACHUTE DRIFT`).
  - **Ch 3 (`3:53–5:57`):** `NUMBER` (`R26` `10 TO 15 CM`, `R27` `10% SOLAR LIGHT`, `R29` `-179°C WATER ICE`, `R32` `300 METRES DEEP`, `R33` `9,000 KM²`, `R35` `50 TO 100 KM CRUST`) + `WORDS` (`R25` chapter card, `R28` `WATER-ICE BEDROCK`, `R30` `METHANE RAIN CYCLE`, `R31` `LIGEIA MARE`).
  - **Ch 4 (`5:57–7:33`):** `NUMBER` (`R37` `95% N2 + 5% CH4`, `R38` `1.47 BAR / -179°C`, `R40` `4X EARTH AIR DENSITY`, `R42` `40X EASIER FLIGHT`) + `WORDS` (`R36` chapter card, `R39` `THERMAL PROTECTION`, `R41` `NO FREE OXYGEN / REVERSED FLAME`).
  - **Ch 5 (`7:33–9:45`):** `NUMBER` (`R44` `2028 LAUNCH / 2034 ARRIVAL`, `R45` `8 ROTORS / NUCLEAR BATTERY`, `R47` `DOZENS OF KILOMETRES`, `R48` `80 KM SELK CRATER`, `R52` `29.5 EARTH YEARS / 7.5 YR WINTER`) + `WORDS` (`R43` chapter card, `R46` `DRAGONFLY ROTORCRAFT`, `R49` `PREBIOTIC CHEMISTRY`).
- **Orbit Placement & Cap (`<= 20%`):**
  - Orbit appears only after `0:30` (`R06a` at `40.40 s`), stays well under the `20%` screen-time cap, and never appears on the long thumbnails (`032_j2417_A_water_deep_below_v01.jpg` / `032_j2417_B_72_minutes_v01.jpg`).

---

## 7. UAT Staging & `jobs/WIP.json` Advancement (Rule G)

1. **Ben UAT Watch Staging (`OWB UAT` + R2 Stream + `jobs.py awaits`):**
   - `032_what_would_happen_if_you_landed_on_titan_master_v02.mp4` (`389,705,443` bytes, SHA-256 `519869728d51b42b98435bc971361994d61780c02e2daa3bc0d23f27c80ed073`) is verified in both NAS `OWB UAT` and iCloud Drive `OWB UAT`.
   - Rendered the `720p` phone/browser watch proxy `032_what_would_happen_if_you_landed_on_titan_master_v02_PHONE.mp4`, placed it in NAS `OWB UAT` and iCloud `OWB UAT`, uploaded it to R2 (`owb-032-v02`) via `scripts/watch_upload.mjs`, and registered both the `_PHONE.mp4` and full master paths in `05_Analytics/kanban/watch_uploads.json` so the Kanban **Play** button streams immediately (`302` verified).
   - Armed `J2477` with `jobs.py awaits` (`--card OWB:032 --type long --version v02 --due "2026-11-16 18:00" --airs "2026-11-25 18:00"`).
2. **`jobs/WIP.json` Advancement (`AGENTS.md` "How films get worked on", Rule G):**
   - With `OWB:032` reaching Ben's UAT watch, `OWB:032` moves out of `active` in `jobs/WIP.json`.
   - Promoted **`OWB:062`** (*Why Is Mars's Moon Phobos Spiralling In to Crash?*, pre-cleared Rule-E `GO` at `93/100` in `J2420`) from `next` into `active` (`entered["OWB:062"] = "2026-11-14"`), keeping `active` at 3 films (`OWB:028`, `OWB:034`, `OWB:062`), and queued `OWB:062`'s `script` stage job per `J2420`.
