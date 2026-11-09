# J2175 — Rule H Review & Editorial/Source Lock for `J2170` (`HOS 008 Short C: How Does a Lightning Rod Work?`)

- **Review Job**: `J2175` (`HOS 008 Short C: Chief decision on J2170 paper hook lock & 1-sentence VO pickup scope (conditional 2 Dec slot held)`, `ref: J2170`, `kind: review`, `film: 008`, `stage: edit`, `repo: hos`)
- **Evidence Inspected**:
  - HOS PR `#429` (`gemini/J2170-short-c-paper-hook` @ `4eef1358`, rebased on `origin/main` `e908c3e2`; all 4 GitHub CI checks green; `check_all.sh 02_Video-Projects/008_Lightning-Franklin` **ALL CHECKS PASS**)
  - `02_Video-Projects/008_Lightning-Franklin/10_Shorts/J2170/SHORT_C_PAPER_PLAN.md`
  - `02_Video-Projects/008_Lightning-Franklin/10_Shorts/J2170/INPUT_INVENTORY.json` (`47/47` inputs existing and SHA-256 verified)
  - `02_Video-Projects/008_Lightning-Franklin/10_Shorts/J2170/source_qa_v03/` (`cuts_v03a.json`, `cuts_v03a_body.json`, `pool_v03.json`, `body_out/PICTURE_QA.md`)
  - Direct `audio_input` (`read_file`) inspection of `10_Shorts/vo_v02/hos_008_short_C_v02.mp3` (`ba8ffec9...`) and word-level Scribe alignment `10_Shorts/vo_v02/stt/hos_008_short_C_v02/stt_raw.json`
  - Direct `moving_video_input` (`read_file`) inspection of all 8 moving Flow Veo plates (`19_skyline_strike_t1.mp4`, `01_house_rod_t1.mp4`, `07_giant_spark_t1.mp4`, `12_steeple_fire_t1.mp4`, `18_rod_closeup_t1.mp4`, `06_rod_fitting_t1.mp4`, `06_rod_fitting_c1_t1.mp4`, `14_safe_towers_t1.mp4`) and `code_graphic_008_p5_11_safe_path.mp4`
- **Reviewer**: `gemini` (`gemini-4-argon-high`, demonstrated `audio_input,moving_video_input` registered via `chief_relay.py capabilities`)
- **Date**: 5 November 2026 (`2026-11-05T18:14Z`)
- **Spend**: **`£0.00` / `0` credits** (Rule H review & paper/source-QA lock only; no voiceover recorded, no Flow/Vertex generation, no media modified, no upload/schedule/Buffer writes)
- **Rule H Verdict**: **`KEEP` (with `C-Open-1` + `Layout C-v03a` locked, 4 `read_file`-verified clip-window/framing refinements applied in HOS PR `#429` @ `4eef1358`, and `picture_qa.py` source preflight `PASS` with `0` fails; parked for Chief only on the protected `47`-char ElevenLabs VO pickup spend authorization & HOS PR `#429` merge)**

---

## 1. Verification of Conditional 2 Dec Slot & Existing-Audio Proof (`£0` Check)

1. **Direct Audio & Word-Level Timing Audit (`hos_008_short_C_v02.mp3` `ba8ffec9...` / `hos_008_short_C_v02.wav` `0a25b6da...`)**:
   - Directly auditioned `10_Shorts/vo_v02/hos_008_short_C_v02.mp3` (`sha256: ba8ffec9c234c68961e5d7e3811d8104feb7d5485ab9d567c10ff91604803d08`) via `read_file` and verified `10_Shorts/vo_v02/stt/hos_008_short_C_v02/stt_raw.json`.
   - Sentence 1 (`w[00..12]`, 13 words: *"That thin metal rod on top of tall buildings was Benjamin Franklin's idea."*) spans `0.080–4.840 s` (`4.760 s` spoken span).
   - Pure speech across `w[00..12]` with `0.000 s` lead-in and `0.000 s` inter-word gaps is **`3.720 s` at `1.00x`**, which equals **`3.509 s > 2.850 s`** (`+0.659 s` over the `2.850 s` hook gate) even at the studio cap `atempo = 1.06x`.
   - Excising `w[04..08]` (*"on top of tall buildings"*) from `hos_008_short_C_v02.wav` is barred by `J1004` (`00b1e653`, HOS PR `#366`: `0 words changed`) and `AGENTS.md` Never list, and still leaves `3.240 s > 2.850 s` at `1.00x`.
   - In `02_Voiceover/hos_008_part05_the_rod_on_every_roof_v01b.mp3` (`sha256: e5e86140174f30164b9fd4856e982b0c2bfbb05b6d8858bf8d5c9bc491b4a6ae`), no sentence finishes `<= 2.850 s` with both the named subject (`"lightning rod"`) and surprise claim without anaphoric pronouns (`"It's..."`).
2. **Slot & Hold Disposition**:
   - The conditional **Wed 2 Dec 2026 11:30Z** (Ben watch by **29 Nov**) slot is **EXPLICITLY NOT ACHIEVABLE on existing audio alone (`£0`)**.
   - The `Short_C` hold (`blocked_hook_and_missing_plates`) is retained and the conditional **2 Dec 11:30Z** slot remains **EMPTY / HELD** until (a) Chief authorizes the 1-sentence (`47`-char) ElevenLabs pickup, (b) `Short_C_v03` is assembled, gated, and passes Ben's final watch, and (c) HOS `008` Long (*Why Did Franklin Fly a Kite in a Storm?*) completes `J1881`/`J2163`/`J2217` corrections and is **Public on YouTube**.
   - `Short_A` (`J0912` / `J2224`, target 24 Nov, watch 20 Nov) remains separate and untouched.

---

## 2. Locked Script, Fact-Notes & Body Layout Decision (`C-Open-1` + `Layout C-v03a`)

### 2.1 Locked Sentence 1 Replacement (`C-Open-1`)
- **Approved Primary Sentence 1 (`S01`, `0.00–2.45 s`, 7 words, 47 characters, 10 syllables)**:
  > **`"That rooftop lightning rod was Franklin's idea."`**
  - **Empirical Token-Duration Proof (from `hos_008_short_C_v02/stt_raw.json`, `eleven_v3`, `speed=1.04`)**:
    - Measured word durations in `hos_008_short_C_v02`: `That` (`0.160 s`) + `rooftop` (`~0.380 s`) + `lightning` (`0.340 s`) + `rod` (`0.340 s`) + `was` (`0.240 s`) + `Franklin's` (`0.480 s`) + `idea.` (`0.360 s`) = **`2.300 s` pure speech** (saving `1.420 s` of pure speech vs `v02`'s `3.720 s`).
    - With `0.060 s` onset + `6 × 0.050 s` natural inter-word gaps (`0.300 s`): **`2.660 s <= 2.850 s` at `1.00x`**.
    - With `0.040 s` onset + `6 × 0.045 s` gaps (`0.270 s`) at `atempo = 1.06x`: **`2.462 s <= 2.850 s`** (`0.388 s` margin below `2.850 s`).
  - **Pre-Approved 6-Word Zero-Extra-Spend Trim Fallback (from the same single take if ElevenLabs inserts an unexpected pause after `"rooftop"`)**:
    > **`"That lightning rod was Franklin's idea."`** (`6` words, `39` chars, `8` syllables; `1.920 s` pure speech, `2.220 s <= 2.850 s` at `1.00x`, `2.057 s <= 2.850 s` at `1.06x`; keeps total Short word count at `6 + 49 = 55` words, inside `55–65`).
  - **`LEARNINGS.md` Rules 1, 2 & 8 Check**:
    - Positive search-question title (`How Does a Lightning Rod Work?`, `SHORTS_SCRIPTS_v02.md` line 49).
    - Frame 0 (`P5:19_skyline_strike` at `offset = 1.00 s`) shows the rooftop lightning rod being struck by lightning with hook caption `FRANKLIN'S **ROD**` (yellow `ROD`).
    - Sentence 1 names the concrete subject (`"rooftop lightning rod"`) by `~1.2 s` and delivers the surprise attribution (`"was Franklin's idea"`) by `~2.45 s <= 2.85 s`, with zero unresolved pronouns and zero meta-promise.

### 2.2 Locked Body Order (`Layout C-v03a` — Original Contiguous `w[13..61]`)
- **Why `Layout C-v03a` Is Locked Over `Layout C-v03b`**:
  1. **Zero Internal Audio Splices in the Body**: `Layout C-v03a` preserves the entire 49-word body (`w[13..61]`, `5.720–24.400 s`, `18.680 s`) of `10_Shorts/vo_v02/hos_008_short_C_v02.wav` (`sha256: 0a25b6dab1351e70fad717d96e066f0d6c1981bd2d17eba1b65db719acec0aa0`) as a **single contiguous, unmodified audio slice** (`atempo = 1.00x`, `0.220 s < 0.25 s` seam breath after `S01`), avoiding the two internal sentence-reorder splices of `Layout C-v03b`.
  2. **Payoff Timing (`>= 70%` Lock)**: In `Layout C-v03a` (`21.35 s` VO, `22.35 s` total duration with `1.00 s` terminal loop return), the `9.0–14.0 s` promoted-long title banner (*Why Did Franklin Fly a Kite in a Storm?*) sits over the problem/setup (*"A wooden roof is a terrible path, so it bursts into flame. A metal rod..."*, `6.21–12.75 s`), while the grounding completion (*"...round the building, and into the earth."*, `15.72–17.49 s`, **`70.3%–78.3%`**) and the scale payoff (*"Some towers are struck over twenty times a year."*, `18.39–21.35 s`, **`82.3%–95.5%`**) both land at **`>= 70%` of runtime**, leading directly into the `21.35–22.35 s` tower-strike loop return.
  3. **Full Locked `Short_C_v03` Spoken Text (`56` words / `55` words with 6w fallback; `55–65` lock PASS)**:
     > *"That rooftop lightning rod was Franklin's idea. Lightning takes the easiest path to the ground. A wooden roof is a terrible path, so it bursts into flame. A metal rod is an easy one. The lightning runs down the rod, round the building, and into the earth. Some towers are struck over twenty times a year."*

### 2.3 Primary Source Verification (`01_Script/FACT_NOTES_v01.md` `bab1bb38...`)
- Every spoken word and the single on-screen overlay (`DATA: 20+ STRIKES A YEAR`) are sourced in `01_Script/FACT_NOTES_v01.md`:
  - **Rows 25, 38, 39, 41, 42**: Benjamin Franklin, *"Opinions and Conjectures"* (1750), published in *Experiments and Observations on Electricity* (London, 1751); Sept 1752 pointed iron rod on his Philadelphia house (Franklin to Collinson, Sept 1753, Founders Online); *Poor Richard Improved* (1753, Founders Online: iron rod `6–8 ft` above roof peak, conductor wire down the exterior wall, foot `3–4 ft` in moist earth).
  - **Row 44**: NOAA / National Weather Service, *Lightning Myths and Facts* (Empire State Building struck an average of `23` times per year; Uman `~20–25`/yr; backs *"over twenty times a year"* and `DATA: 20+ STRIKES A YEAR`).

---

## 3. Direct Moving-Video (`read_file`) Audit of All 9 Visual Assets & Clip-Window Locks

All 8 moving Flow Veo plates (`1280x720`, `24/1 fps`, `192` frames, `8.000 s`) and `code_graphic_008_p5_11_safe_path.mp4` were inspected directly via `read_file` in `J2175`. Four concrete refinements were identified and locked in HOS PR `#429` (`4eef1358`):

1. **Exact `9:16` Integer Portrait Framing for `terminal_loop.py` v1 & `picture_qa.py` (`<= 2.35x`)**:
   - `scripts/terminal_loop.py` line 120 enforces `output[0] * 16 == output[1] * 9` (which rejects `952x1692` since `952 * 16 = 15232 != 1692 * 9 = 15228`), while `scripts/picture_qa.py` enforces `upscale <= 2.35x`.
   - Locked portrait framing across all 9 cuts: **`crop = [438, 0, 405, 720]`**, **`output = [936, 1664]`** (`936 * 16 == 1664 * 9 == 14976`, divisible by 8, **`upscale = 2.3111x <= 2.35x`**).
2. **`S05` (`11.15–13.95 s`, `2.80 s`) — `P5:18_rod_closeup` (`18_rod_closeup_t1.mp4`, `9535c72f...`) Smoke-Puff Artifact Exclusion**:
   - Direct `read_file` inspection revealed a Veo artifact at `00:05–00:06` (`4.80–6.50 s`) where white smoke/steam puffs out of the iron lightning rod tip.
   - `0.00–4.00 s` is a clean close-up of the pointed iron rod atop a cupola under moving storm clouds. `S05` is locked to **`offset = 0.00 s` (`0.00–2.80 s`, strictly `< 4.00 s`)**.
3. **`S06` (`13.95–16.75 s`, `2.80 s`) & `S07` (`16.75–19.45 s`, `2.70 s`) — Un-Swapped Wall vs Earth Plates & Clean `< 5.80 s` Windows**:
   - Direct `read_file` inspection showed `J2170`'s initial table had swapped the descriptions of `06_rod_fitting_t1.mp4` and `06_rod_fitting_c1_t1.mp4`:
     - `06_rod_fitting_t1.mp4` (`73c43fc2...`) shows a colonial workman on a wooden ladder fastening the iron conductor rod **down the exterior brick wall** (`0.00–6.00 s`; steps off ladder at `6.50–8.00 s`). Locked to **`S06`** (*"The lightning runs down the rod, round"*) at **`offset = 1.50 s` (`1.50–4.30 s < 6.00 s`)**.
     - `06_rod_fitting_c1_t1.mp4` (`de605071...`) shows a colonial workman kneeling at the stone foundation base driving the grounding rod **into the damp earth** (`0.00–5.80 s`; stands up with a spearhead morph at `6.50–8.00 s`). Locked to **`S07`** (*"the building, and into the earth. Some"*) at **`offset = 1.50 s` (`1.50–4.20 s < 5.80 s`)**.
4. **`S08` (`19.45–21.35 s`, `1.90 s`) — `P5:14_safe_towers` (`14_safe_towers_t1.mp4`, `0c7e98c2...`) Street-Spark Exclusion**:
   - Direct `read_file` inspection showed bright sparks splashing on the street at `1.00–2.20 s`, whereas `4.00–7.20 s` shows the church steeple and town towers standing calm and unharmed under storm clouds. Locked to **`offset = 4.20 s` (`4.20–6.10 s`)** with the single Short teach overlay **`DATA: 20+ STRIKES A YEAR`** (`18.50–21.20 s`, inside `[656, 1264]` 16:9 band).
5. **`S01` (`0.00–2.45 s`) & `loop_tail` (`21.35–22.35 s`) — `P5:19_skyline_strike` (`19_skyline_strike_t1.mp4`, `06caaeb6...`)**:
   - Locked to **`offset = 1.00 s`** (`1.00–3.45 s` for `S01`; `source_in = 1.00, source_out = 2.00` for `loop_tail` with `role: "prescribed_terminal_loop"`). At `t = 1.000 s` (Frame 0, `frame 024`), the lightning bolt actively strikes the rooftop rod (`top_luma = 130.3 -> 175.3`), and at `t = 2.000 s` (`frame 048`, `+1.000 s` into `S01`) the bolt channels down and extinguishes leaving the tower dark and calm (`top_luma = 53.6`).
6. **Cross-Check Against All 8 `J1881` / `J2163` / `J2217` (5 Nov 2026, `4e94001e`) Long UAT Notes & Film-Wide Caption Rule**:
   - All 8 Long UAT defect items (`00:20` `P1:03_table_three`, `0:30` `P1:03b_town_safe -> P1:04_storm_mystery`, `0:51` `P1:07_hot_night`/`P2:02_salon_spark`, `1:49` `P2:02_salon_spark`, `2:18` `P2:07_foil_jar`, `2:20` `P2:07_foil_jar`/`P2:08_jar_spark`, `3:13` `P3:01_points_desk`, `3:31` `P3:04_letter_crosses`, `7:58/7:59` `P5:13_rods_spread`) are **100% disjoint** from `Short_C`'s 8 moving plates.
   - Per Ben's 5 Nov 2026 note (`J2217` / `J1868_BEN_NOTES_2026-11-05.md`), all bottom on-screen text over moving footage in `Short_C_v03` must sit over a soft dark/warm background panel (never bordered UI chrome).

---

## 4. Pasted Tool & CI Gate Outputs

### 4.1 `picture_qa.py` Source Preflight (`10_Shorts/J2170/source_qa_v03/`)
```text
WARN   0:01 row S01 /Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/part05/raw/v01/19_skyline_strike_t1.mp4: sharpness: upscaled 2.31x, may look soft
WARN   0:04 row S02 /Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/part05/raw/v01/01_house_rod_t1.mp4: sharpness: upscaled 2.31x, may look soft
WARN   0:07 row S03 /Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/part05/raw/v01/07_giant_spark_t1.mp4: sharpness: upscaled 2.31x, may look soft
WARN   0:10 row S04 /Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/part01/raw/v01/12_steeple_fire_t1.mp4: sharpness: upscaled 2.31x, may look soft
WARN   0:13 row S05 /Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/part05/raw/v01/18_rod_closeup_t1.mp4: sharpness: upscaled 2.31x, may look soft
WARN   0:15 row S06 /Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/part05/raw/v01/06_rod_fitting_t1.mp4: sharpness: upscaled 2.31x, may look soft
WARN   0:18 row S07 /Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/part05/raw/v01/06_rod_fitting_c1_t1.mp4: sharpness: upscaled 2.31x, may look soft
WARN   0:20 row S08 /Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/part05/raw/v01/14_safe_towers_t1.mp4: sharpness: upscaled 2.31x, may look soft
picture QA PASS: 0 of 8 cuts fail, 8 to look at -> /private/tmp/j2175-hos-wt/02_Video-Projects/008_Lightning-Franklin/10_Shorts/J2170/source_qa_v03/body_out/PICTURE_QA.md
```

### 4.2 HOS Repository Checks (`bash 00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/008_Lightning-Franklin`) & GitHub PR `#429` CI
```text
-- durable desk handoffs: PASS
-- no media: PASS
-- status board in sync: PASS
-- ElevenLabs guard tests: PASS
-- vo_check word tests: PASS
-- atempo check tests: PASS
-- voice speed (atempo <= 1.06): PASS
-- contract tests: PASS
-- package-lint: PASS
-- review:script lightning_script_master_v01.md: PASS
-- gate:episode: PASS
ALL CHECKS PASS

gh pr checks 429:
All checks were successful (4 successful, 0 failing, 0 pending)
```

---

## 5. Rule H Disposition & Exact Protected Call Parked for Chief

- **Verdict**: **`KEEP`**
- **Action Taken in `J2175` (`£0`)**:
  - Locked `C-Open-1` (*"That rooftop lightning rod was Franklin's idea."*, `47` chars, `7` words, `10` syllables; with 6-word zero-extra-spend trim fallback *"That lightning rod was Franklin's idea."*) + `Layout C-v03a` (contiguous unmodified `w[13..61]`, `5.720–24.400 s` of `hos_008_short_C_v02.wav`).
  - Locked the `read_file`-verified 9-cut `936x1664` (`2.3111x`) moving-plate schedule (`source_qa_v03/cuts_v03a.json`, `pool_v03.json`, `0` `picture_qa.py` fails) and updated `10_Shorts/J2170/SHORT_C_PAPER_PLAN.md`, `10_Shorts/J2170/INPUT_INVENTORY.json`, and `02_Video-Projects/008_Lightning-Franklin/production-status.md` in HOS PR `#429` (`4eef1358`).
- **Protected Call Parked for Chief on `J2175` (`Rule H` item 4 — no spend or merge by worker)**:
  - `parked for Chief: review J2175 KEEP (jobs/reviews/J2175/REVIEW.md, HOS PR #429 4eef1358) — C-Open-1 ('That rooftop lightning rod was Franklin's idea.', 47 chars, 10 syllables; 6w fallback 'That lightning rod was Franklin's idea.') + Layout C-v03a (contiguous w[13..61] 5.720-24.400s of hos_008_short_C_v02.wav) + read_file 9-cut 936x1664 2.31x schedule locked (0 picture_qa fails, J2217 8-note disjoint, soft bottom-caption panel locked). Merge HOS PR #429, authorize 1-sentence 47-char ElevenLabs pickup via vo_take.py, and dispatch £0 Short_C_v03 assembly (conditional 2 Dec 11:30Z slot remains held; 008 Long must be public first).`
