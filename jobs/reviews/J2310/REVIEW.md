# Review — J2315 (for J2310): OWB 029 Fri 11 Dec E1 Tail Candidate `v05` (`k2kEaA7ICjc`)

- **Review Job:** `J2315` (`kind: review`, `ref: J2310`)
- **Reviewed Build Job:** `J2310` (commit `3f0b03bf50`, `jobs/reviews/J2310/HANDOFF.md`)
- **Reviewer:** `gemini` (`Gemini 4 Argon (High)` / `gemini-argon`, review lane under Rule H)
- **Date:** `2026-11-06`
- **Channel / Film / Slot:** OWB `029` (*Is Betelgeuse About to Explode?*) — Fri 11 Dec Test A opening Short (`k2kEaA7ICjc`, Private, scheduled `2026-12-11T11:30:00Z`)
- **Verdict:** **`KEEP` (as an `EXCEPTION`-labelled Test A E1 tail-only candidate — NOT a full E1 PASS and NOT an immediate YouTube swap)**
- **Spend:** `£0` (local inspection and verification only)

---

## 1. Executive Decision & Scope Confirmation

**Decision: `KEEP` (`status: "EXCEPTION"` retained).**

`029_short_fri11_opening_testA_v05.mp4` (`32.667 s`, `980` frames @ `30 fps`, `1080×1920`) and its companion phone copy `029_short_fri11_opening_testA_v05_PHONE.mp4` (`720×1280`) cleanly resolve the target E1 structural tail defect on `k2kEaA7ICjc` (`v04`) while preserving every locked spoken word, Test A experimental arm boundary, and `J0991` ruling:

1. **Loop Tail & End-Card Removal (`PASS`):**
   - `v04` carried a `2.00 s` `"Full film on the channel"` end card (`31.88–33.88 s`, `33.90 s` total) with a `2.32 s` tail after the last word `"when."` (`31.58 s`).
   - `v05` removes the end-card block, holds `s12_loop` (`es0204a_betelgeuse_16x9.jpg`) through the final word `"when."` (`30.98–31.58 s`), and crossfades for `0.30 s` starting at `31.70 s` (`0.12 s` after `"when."`) directly onto `frame 0` (`VISIBLE IN DAYLIGHT`, `betelgeuse_surface_convection.png`), ending at `32.667 s`.
   - Post-last-word loop tail is **`1.087 s` (`1.09 s`)**, strictly under the E1 `< 1.20 s` ceiling.
   - Tail OCR at `0.00 s`, `31.85 s`, `32.20 s`, and `32.50 s` reads `VISIBLE IN DAYLIGHT` with **zero** end-card text; frame-0-to-last-frame `loop_diff_mean_abs = 1.543` (`f0diff = 5.94` in `gate_shorts_open.py`).
   - Music bed (`betelgeuse_score_bed_v01.mp3`) runs continuously across the loop seam (`mean_volume = -32.6 dB` across `31.58–32.67 s`, fade-out shortened from `0.85 s` to `0.12 s`), calibrated to **`-14.1 LUFS` integrated / `-2.2 dBTP` true peak** in the AAC stream.
2. **Why `v05` stays labelled `EXCEPTION` (Not a Full E1 `PASS`, Not Sent Back for `FIX`):**
   - `v05` is **not** promoted to a full E1 `PASS` because four recorded-word/timing properties remain outside literal E1 thresholds (`"explode?"` surprise word at `6.70 s > 1.50 s`, internal sentence-1 pause `0.200 s > 0.15 s` between `"winter"` and `"at"`, spoken meta-clause `"In this film, I will show you"` at `18.76–20.14 s`, and `32.67 s` runtime outside `22–27 s`).
   - As resolved in **Section 4** below, all four are intrinsic properties of the locked `029` long opening VO slice (`0.08–31.58 s`) governed by the **Test A opening-Short exemption** (`AGENTS.md` Standing Lesson 5; `.cursor/rules/orbit-build-shorts.mdc` `OWB-2026-11-E1`; `SHORTS_TESTS.md` §A) and the **`J0991` ruling** (`jobs/reviews/J0991/RULING.md`, preserved by `jobs/briefs/J2207/k2kEaA7ICjc.md`). Splicing, reordering, or trimming the spoken lines to force those four metrics into non-Test-A thresholds would break the locked VO rule (`J2310` brief: *"Never invent, rewrite or re-order spoken lines"*) and invalidate the Test A arm.
   - Retaining `status: "EXCEPTION"` accurately records that the E1 loop/tail mechanics are fixed while the Test A / `J0991` spoken-VO exemptions remain in force.
3. **Scheduled `v04` & Live/Staged State Untouched:**
   - Scheduled Private YouTube video `k2kEaA7ICjc` (`2026-12-11T11:30:00Z`), `11_Upload-Package/PACKAGE_MANIFEST.json`, `00_Brand/Channel-Setup/social/UPLOADS.json`, Buffer (`BUFFER_POSTS.json`), and `029_short_fri11_opening_testA_v04.mp4` (`ff4194857a027cfc5f93551ef398125276e6bcfb9cd3ce2fd18d8ee1134e2405`) were **not** modified.

> **Capability & Sensory Boundary Note (`AGENTS.md`):** This review session recorded `chief_relay.py capabilities --agent gemini --available ''` (no direct `audio_input` or `moving_video_input` tool in this worker session). Verification was performed via contact sheets (`open_sheet.jpg`, `frames_5pt.jpg`, `cover_preview.jpg`, `picture_qa_review.jpg`, and extracted `31.50–32.63 s` tail frames), OCR, `ffprobe`/`ffmpeg` decode/ebur128/volumedetect measurements, and all six studio QA gate tools. Per `AGENTS.md` (*"A review-lane agent checks the technical gates and stills; Ben's final watch is the watch-and-listen check"*), this `KEEP` clears technical and structural review so the cut can proceed to Ben's watch and a separately authorised swap job.

---

## 2. File Integrity & SHA-256 Verification

All build outputs and preserved `v04` files were verified across the repo workspace, NAS (`OWB UAT`), and iCloud Drive (`OWB UAT`):

| Artifact | Path / Location | Bytes | SHA-256 | Status |
|---|---|---:|---|---|
| **Preserved `v04` master** | `10_Shorts/fri11_opening_testA/06_Final-Exports/029_short_fri11_opening_testA_v04.mp4` | `35,627,548` | `ff4194857a027cfc5f93551ef398125276e6bcfb9cd3ce2fd18d8ee1134e2405` | Untouched (`J0991` match) |
| **Candidate `v05` master (Local)** | `10_Shorts/fri11_opening_testA/06_Final-Exports/029_short_fri11_opening_testA_v05.mp4` | `34,629,944` | `d1c208d76aa4a675e6c07d091a6dba9fe29646cdf85b808b7814c659f1570f01` | Verified (`980` frames, `rc=0` decode) |
| **Candidate `v05` master (NAS)** | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/J2310_029_fri11_v05/029_short_fri11_opening_testA_v05.mp4` | `34,629,944` | `d1c208d76aa4a675e6c07d091a6dba9fe29646cdf85b808b7814c659f1570f01` | Exact SHA-256 match |
| **Candidate `v05` master (iCloud)** | `~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/J2310_029_fri11_v05/029_short_fri11_opening_testA_v05.mp4` | `34,629,944` | *(stat size/mtime match; staged)* | Present (`15/15` files staged) |
| **Candidate `v05` PHONE (Local)** | `10_Shorts/fri11_opening_testA/06_Final-Exports/029_short_fri11_opening_testA_v05_PHONE.mp4` | `7,398,203` | `e6613b6eeb23cf35663836ab5848566e4b4c1c059bacd1a5065f4bd8cdd3b930` | Verified (`980` frames, `rc=0` decode) |
| **Candidate `v05` PHONE (NAS)** | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/J2310_029_fri11_v05/029_short_fri11_opening_testA_v05_PHONE.mp4` | `7,398,203` | `e6613b6eeb23cf35663836ab5848566e4b4c1c059bacd1a5065f4bd8cdd3b930` | Exact SHA-256 match |
| **Cover JPEG (`frame 0`)** | `10_Shorts/fri11_opening_testA/06_Final-Exports/029_short_fri11_opening_testA_v05_cover.jpg` | `327,764` | `dc73a55f603f8c2a62ca9f62f261790cbcf460f6ab05a5d8e5c579bd82e9a4c6` | Verified (`sat=187.7`, `nb=3%`) |

*(Note: `029_short_fri11_opening_testA_v05_meta.json` records `phone_bytes: 7398264` from a pre-rewrite stat while `phone_sha256` `e6613b6eeb23cf35663836ab5848566e4b4c1c059bacd1a5065f4bd8cdd3b930` and actual size `7,398,203` bytes match identically across Local, NAS, and iCloud UAT.)*

---

## 3. E1 Structural Audit (`v04` vs `v05`)

| E1 Audit Parameter | Rule / Target (`OWB-2026-11-E1`) | Scheduled `v04` (`J0991`) | Candidate `v05` (`J2310`) | Assessment |
|---|---|---|---|---|
| **Duration / Frames** | Test A `30–38 s` (`< 40 s` cap) | `33.900 s` (`1017` frames) | **`32.667 s` (`980` frames @ `30/1 fps`)** | **PASS (Test A exempt from `22–27 s`)** |
| **First visual cut (`cut1_s`)** | `1.80 s <= cut1 <= 2.50 s` | `2.230 s` | **`2.230 s`** | **PASS** |
| **Second visual cut (`cut2_s`)** | `cut2 <= 5.00 s` | `4.720 s` | **`4.720 s`** | **PASS** |
| **Max visual hold (`max_hold_s`)** | `<= 4.00 s` | `3.840 s` | **`3.840 s`** (`12` cuts, `2.23–3.84 s`) | **PASS** |
| **VO onset (`vo_onset_s`)** | `<= 0.25 s` | `0.080 s` | **`0.080 s`** (`"You"`) | **PASS** |
| **Sentence-1 → Sentence-2 gap** | `<= 0.15 s` (`<= 0.20 s` natural breath) | `0.200 s` (`3.86 → 4.06 s`) | **`0.200 s`** (`"tonight."` → `"And"`) | **PASS (natural sentence breath)** |
| **Payoff timestamp / share** | `>= 82%` of runtime | `28.82 s / 33.90 s` (`85.0%`) | **`28.82 s / 32.67 s` (`88.22%`)** (`"one hundred thousand years"`) | **PASS (`+3.2%` later share)** |
| **Last word end (`last_word_end_s`)** | Locked VO end | `31.580 s` (`"when."`) | **`31.580 s`** (`"when."`) | **PASS (verbatim VO preserved)** |
| **Loop tail (`tail_after_last_word_s`)** | **`< 1.20 s`** | `2.320 s` (**FAIL**) | **`1.087 s` (`1.09 s`)** | **PASS (resolved)** |
| **Closing CTA / end card** | **No end card / no spoken CTA** | `2.00 s` `"Full film on the channel"` (**FAIL**) | **Removed (`0` end cards; OCR verified)** | **PASS (resolved)** |
| **Loop return seam** | Crossfade to `frame 0`, bed across seam | End card blocked loop return | **`0.30 s` xfade at `31.70 s` to `frame 0` (`diff=1.543`), bed fade `0.12 s`** | **PASS (resolved)** |
| **Integrated loudness / True peak** | `~ -14 LUFS`, `<= -1.0 dBTP` | `-14.0 LUFS` / `-1.0 dBTP` | **`-14.1 LUFS` / `-2.2 dBTP`** (calibrated AAC) | **PASS** |

---

## 4. Resolution of the 4 Recorded-Word / Test A Conflicts

`jobs/reviews/J2310/HANDOFF.md` flagged four conflicts between literal E1 non-Test-A heuristics and the locked `029` opening recording (`029_short_fri11_opening_testA_v05_e1.json`). Each is resolved below:

### Conflict 1: Surprise / Contrast Word `"explode?"` Ends at `6.70 s` (`> 1.50 s`) & Line 1 Is Declarative
- **Observation:** Sentence 1 (`0.08–3.86 s`, *"You can walk outside tonight and find this star with your bare eyes."*) is a declarative visual invitation; the title question *"Is it about to explode?"* lands in Sentence 2 (`4.06–6.70 s`).
- **Resolution (`KEEP` as Test A `EXCEPTION`):**
  - Per `AGENTS.md` Standing Lesson 5 (*"Exception (Ben, 26 Oct 2026): Test A Shorts are exempt from the Keeper score one-question first line and from 22–27 s until Test A's own result is read"*), `.cursor/rules/orbit-build-shorts.mdc` (`OWB-2026-11-E1`), and `jobs/briefs/J2207/k2kEaA7ICjc.md`, Test A tests whether the long film's verbatim opening (`30–38 s`) converts viewers into the long film.
  - Furthermore, the frame-0 hook caption (`VISIBLE IN DAYLIGHT`, with `VISIBLE` in `#FFD400` yellow at `y = 330 px`) puts the visual surprise on screen at `0.00 s` while Sentence 1 grounds the naked-eye hook. Re-cutting or reordering Sentence 1 and Sentence 2 would violate both the Test A experimental design and the `J2310` ban on reordering spoken lines.

### Conflict 2: `0.200 s` Internal Pause in Sentence 1 (`"winter"` `1.34–1.76 s` → `"at"` `1.96–2.04 s`)
- **Observation:** `v04_words.json` / `v05_words.json` reports a `0.200 s` gap (`> 0.15 s` inter-sentence cut target) inside the first continuous VO slice `{"a": 0.08, "b": 3.86}` between *"in winter"* and *"at the shoulder of Orion"* (inherited from `v04`'s original `1.70 s` phrase trim of *"in winter"*, which `J0991` removed).
- **Resolution (`KEEP` as Test A `EXCEPTION`):**
  - The E1 `<= 0.15 s` rule targets dead-air gaps between sentence slices (`s1 → s2`), not natural prosodic phrasing inside a single continuous master VO slice (`0.08–3.86 s`).
  - Cutting `50–80 ms` out of the middle of Sentence 1 would alter word timestamps across cuts 1–12 and risk an audible mid-clause splice artifact for a `50 ms` micro-trim. Leaving the continuous slice intact is the right editorial call.

### Conflict 3: Spoken Meta-Line `"In this film, I will show you"` (`18.76–20.14 s`)
- **Observation:** Sentence 5 (`18.76–26.90 s`) begins with *"In this film, I will show you why the Great Dimming of two thousand and nineteen and two thousand and twenty fooled the world..."*, which matches the E1 `FORBIDDEN_SPOKEN_META` regex (`\bin this (?:film|video|short)\b`).
- **Resolution (`KEEP` as Test A `EXCEPTION` under `J0991` & `J2207`):**
  - `jobs/reviews/J0991/RULING.md` explicitly waived the `18.76 s` `"In this film, I will show you"` line for `k2kEaA7ICjc` because it is the verbatim long-film opening tested by Test A (`SHORTS_TESTS.md` §A).
  - `jobs/briefs/J2207/k2kEaA7ICjc.md` (authorised by Chief `h47`) explicitly instructed: *"Preserve `J0991`'s Test A waiver for the `18.76s` spoken `'In this film, I will show you'` line unless Chief explicitly orders a VO edit; only the closing `2.00s` end-card tail is targeted here."*
  - Excising `"In this film, I will show you"` without a fresh recording would leave the ungrammatical fragment *"why the Great Dimming..."*. Keeping the `J0991` waiver under `status: "EXCEPTION"` follows `J2207` and `J2310` to the letter.

### Conflict 4: Duration `32.667 s` (`32.7 s`) Outside the `22–27 s` Standard Short Band
- **Observation:** `gate_shorts_open.py` logs a non-fatal warning (`duration 32.7s outside 22–27s band`).
- **Resolution (`KEEP` as Test A `EXCEPTION`):**
  - Test A opening Shorts are defined in `AGENTS.md` Standing Lesson 5 and `SHORTS_TESTS.md` §A as `30–38 s` cuts of the long film's opening, capped under the `< 40 s` Never limit. Removing the `2.00 s` end card shortened `k2kEaA7ICjc` from `33.90 s` to `32.67 s`, keeping it squarely inside the `30–38 s` Test A band while eliminating the post-VO end-card hold.

---

## 5. Independent Tool Gate & Visual Verification

All six studio QA tools and full `ffmpeg` stream decodes were re-run independently during `J2315`:

1. **`ffmpeg` Full Decode Check (`v05.mp4` & `v05_PHONE.mp4`):**
   ```text
   v05.mp4:       1080x1920, 30/1 fps, 980 frames, 32.666667 s, aac 48000 Hz stereo -> decode_rc=0, stderr=""
   v05_PHONE.mp4: 720x1280,  30/1 fps, 980 frames, 32.666667 s, aac 48000 Hz stereo -> decode_rc=0, stderr=""
   ```
2. **Shorts Open & Ship Gate (`gate_shorts_open.py check ... --air-date 2026-12-11 --id k2kEaA7ICjc`):**
   ```text
   PASS 029_short_fri11_opening_testA_v05.mp4 (dur=32.67s, audio=-16.8dB, motion=13.2, f0diff=5.94, cut1=2.23s, vo_onset=0.08s, tail_gap=1.09s, visor=0.0007, 1 warn(s))
     WARN duration: 32.7s outside 22–27s band
   ```
3. **Picture QA (`scripts/picture_qa.py`):**
   ```text
   PASS: 0 of 12 cuts fail, 3 to look at -> 029_short_fri11_opening_testA_v05_picture_qa/picture_qa_review.jpg
   WARN 0:01 (row 1, s01_visir): upscale 2.06x over 2.0x (under 2.35x cap)
   WARN 0:10 (row 4, s04_sphere): low detail (edge density 0.0163; smooth Betelgeuse convection sphere render)
   WARN 0:20 (row 7, s07_alma): upscale 2.30x over 2.0x; soft/hazy (luma std 14.48; resolved ALMA sub-mm disc)
   ```
   *(Visual inspection of `picture_qa_review.jpg`, `open_sheet.jpg`, `frames_5pt.jpg`, and extracted tail strip `31.50–32.63 s`: all 12 cuts are identical to `J0991`-approved `v04` through `31.58 s`; single `1600 AD` WHEN overlay at `27.80–30.50 s` sits cleanly inside the 16:9 safe band; at `31.70–32.00 s` `s12_loop` crossfades smoothly into `frame 0` `VISIBLE IN DAYLIGHT` with no black flash and no end card.)*
4. **Polish Gate (`scripts/polish_gate.py`):**
   ```text
   PASS: 0 of 12 rows failed, 2 to look at
     row 4 (s04_sphere): WARN: low detail (edge density 0.0165)
     row 7 (s07_alma): WARN: soft/hazy (luma std 14.6)
   ```
5. **Music Gate (`scripts/music_gate.py`):**
   ```text
   PASS: betelgeuse_score_bed_v01.mp3, 542.3 s, about 75.0 BPM, brief Pace: 68-78 BPM
   ```
6. **SFX Level Rule (`scripts/sfx_kit.py level`):**
   ```text
   PASS: VO -16.6 LUFS, SFX -38.6 LUFS (22.0 LU under VO; speech 18.8 LU under VO; pauses 29.8 LU under VO; bed speech 17.6 LU under VO), 3 hits
   ```
7. **Cover Thumbnail Gate (`thumb_preview.py short --score`):**
   ```text
   PASS 029_short_fri11_opening_testA_v05_cover.jpg saturation=187.7 near_black=3%
   ```

---

## 6. Follow-Up Path (No Immediate Swap)

1. **Verdict Recorded:** `KEEP` (`status: "EXCEPTION"` — Test A E1 tail-only candidate).
2. **Ben's Finished-Cut Watch:** `029_short_fri11_opening_testA_v05.mp4` (`34.6 MB`) and `029_short_fri11_opening_testA_v05_PHONE.mp4` (`7.4 MB`) are staged in `OWB UAT/J2310_029_fri11_v05/` (both NAS and iCloud Drive) for Ben's watch of the finished cut.
3. **Separate Authorised Swap Job Required Before Any YouTube Change:**
   - Per the `J2310` and `J2315` briefs, this `KEEP` does **not** authorise an immediate YouTube swap.
   - Because `k2kEaA7ICjc` airs `2026-12-11T11:30:00Z` (outside the 21-day `3 Dec` cohort), `11 Dec` is follow-up after the `3 Dec` readout (`jobs/briefs/J2207/INVENTORY.md`).
   - When a swap job is queued and authorised after Ben's watch, it must update YouTube, `11_Upload-Package/PACKAGE_MANIFEST.json`, `00_Brand/Channel-Setup/social/UPLOADS.json`, and Buffer (`BUFFER_POSTS.json`) atomically in the same job (`AGENTS.md` Standing Lesson 6).
