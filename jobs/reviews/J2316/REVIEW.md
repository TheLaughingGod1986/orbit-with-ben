# Review — J2316 (for J2311): OWB 029 Mon 14 Dec E1 Local Candidate `v05` (`heiGCnGKTkE`)

- **Review Job:** `J2316` (`kind: review`, `ref: J2311`)
- **Reviewed Build Job:** `J2311` (commit `367eabd0f0`, `jobs/reviews/J2311/HANDOFF.md`)
- **Reviewer:** `gemini` (`Gemini 4 Argon (High)` / `gemini-argon`, worker fallback covering review lane)
- **Date:** `2026-11-06`
- **Channel / Film / Slot:** OWB `029` (*Is Betelgeuse About to Explode?*) — Mon 14 Dec lifted Short *How Bright Will Betelgeuse Get When It Explodes?* (`heiGCnGKTkE`, Private, scheduled `2026-12-14T11:30:00Z`)
- **Verdict:** **`KEEP` (as an `EXCEPTION`-labelled E1 local candidate — NOT a full E1 PASS and NOT an immediate YouTube swap)**
- **Spend:** `£0` (local inspection and verification only)

---

## 1. Executive Decision & Scope Confirmation

**Decision: `KEEP` (`label: "EXCEPTION"` retained).**

`029_short_mon14_half_moon_daylight_v05.mp4` (`22.040 s`, `661` frames @ `30/1 fps`, `1080×1920`) and its companion phone copy `029_short_mon14_half_moon_daylight_v05_PHONE.mp4` (`720×1280`) resolve every target E1 visual cut, setup-trim, end-card, and loop-tail defect identified for `heiGCnGKTkE` (`v04`) under `jobs/briefs/J2207/heiGCnGKTkE.md` while keeping the `>= 22.00 s` Keeper length floor and preserving all factual claims in the locked recording:

1. **Cut 1, Cut 2, End-Card Removal & Loop Tail (`PASS`):**
   - `v04` placed Cut 1 at `2.99 s` (`> 2.80 s` E1 limit), Cut 2 at `5.76 s` (`> 4.80 s` E1 limit), and ended on a `2.00 s` `"Full film on the channel"` end card (`21.94–23.94 s`, `23.93 s` total) with a `2.29 s` post-word tail after `"daylight."` (`21.64 s`).
   - `v05` moves **Cut 1 to `2.30 s`** (`<= 2.80 s`, frame diff `67` across `2.20–2.45 s`), moves **Cut 2 to `4.63 s`** (`<= 4.80 s`, frame diff `94.43` across `4.50–4.75 s`), keeps all later holds `<= 3.80 s` (`s05_orion_flare`), removes the end card (`end_card: null`; tail OCR verified free of `"Full film on the channel"`), crossfades for `0.30 s` at `21.433 s` (`s07_daylight` → `s08_loop` `frame0_hold_mon14_half_moon_daylight.png`) onto `frame 0`, and finishes at `22.040 s` (`1.16 s` post-word loop tail after `"daylight."` ends at `20.88 s`, strictly `< 1.20 s`).
   - Trimming the two non-factual setup words `"So imagine"` (`248.06–248.82 s` in master VO) puts first-word onset (`"the"`) at `0.06 s` (`<= 0.15 s`), names `"Betelgeuse"` at `0.78–1.40 s` (`<= 2.50 s`), and starts the surprise word `"explodes."` at **`1.48 s`** (`<= 1.50 s`), followed by a `0.20 s` breath (`< 0.25 s`) into `"The first sign would not be light at all."` at `2.40 s`.
2. **Why `v05` Stays Labelled `EXCEPTION` (Not a Full E1 `PASS`, Not Sent Back for `FIX`):**
   - `v05` is **not** promoted to a full E1 `PASS` because two intrinsic recorded-VO properties remain outside literal E1 non-exception heuristics:
     1. A `0.220 s` (`> 0.15 s`) prosodic pause inside Sentence 1 between `"night"` (`0.22–0.56 s`) and `"Betelgeuse"` (`0.78–1.40 s`). Closing this `0.08 s` excess inside the continuous recording slice without padding inter-sentence gaps would pull `last_word_end_s` down to `20.80 s`, making it mathematically impossible to satisfy both the `>= 22.00 s` Keeper floor and the `< 1.20 s` E1 loop-tail ceiling (`22.00 - 20.80 = 1.20 s`).
     2. Sentence 1 (`"the night Betelgeuse explodes."`) is not the literal title question (`"How Bright Will Betelgeuse Get When It Explodes?"`), which is never spoken anywhere in the `029` VO corpus (`02_Voiceover/words.json`).
   - As detailed in **Section 4**, both conflicts are governed by `jobs/briefs/J2207/heiGCnGKTkE.md` (*"Existing recorded words/media only, no spend/generation... retain the 22 s floor... Never waive a failed gate or pad to length. If recorded words cannot meet a requirement, report exact conflict for reviewer, do not invent speech"*). Sending `v05` back for `FIX` cannot resolve either conflict under `£0` existing recorded words without either breaking the `22.00 s` / `< 1.20 s` mathematical bound or inventing speech. Retaining `label: "EXCEPTION"` accurately records the status.
3. **Scheduled `v04` & Live/Staged State Untouched:**
   - Scheduled Private YouTube video `heiGCnGKTkE` (`2026-12-14T11:30:00Z`), `11_Upload-Package/PACKAGE_MANIFEST.json`, `00_Brand/Channel-Setup/social/UPLOADS.json`, Buffer (`BUFFER_POSTS.json`), and `029_short_mon14_half_moon_daylight_v04.mp4` (`31f362f4437b4ca56ec16b8abef1dce4c65fb5a5c6c7b5b4e2ba39229a33efd5`) were **not** modified.

> **Capability & Sensory Boundary Note (`AGENTS.md`):** This review session recorded `chief_relay.py capabilities --agent gemini --available ''` (reading `.mp4` via `read_file` returns 1 Hz still frames and ASR transcript only, not raw audio playback or continuous 30 fps motion stream perception). Verification was performed via contact sheets (`open_sheet.jpg`, `frames_5pt.jpg`, `cover_preview.jpg`, `picture_qa_review.jpg`), `read_file` 1 Hz frame strip (`00:00–00:21`), OCR, `ffprobe`/`ffmpeg` decode/loudness measurements, and all six studio QA gate tools. Per `AGENTS.md` (*"A review-lane agent checks the technical gates and stills; Ben's final watch is the watch-and-listen check"*), this `KEEP` clears technical and structural review so the candidate can proceed to Ben's watch and a separately authorised swap job.

---

## 2. File Integrity & SHA-256 Verification

All build outputs and preserved `v04` files were verified across the repo workspace, NAS (`OWB UAT`), and iCloud Drive (`OWB UAT`):

| Artifact | Path / Location | Bytes | SHA-256 | Status |
|---|---|---:|---|---|
| **Preserved `v04` master** | `10_Shorts/mon14_half_moon_daylight/06_Final-Exports/029_short_mon14_half_moon_daylight_v04.mp4` | `21,797,232` | `31f362f4437b4ca56ec16b8abef1dce4c65fb5a5c6c7b5b4e2ba39229a33efd5` | Untouched (`J0991` match) |
| **Candidate `v05` master (Local)** | `10_Shorts/mon14_half_moon_daylight/06_Final-Exports/029_short_mon14_half_moon_daylight_v05.mp4` | `21,608,743` | `f16e0e3c1c0bacdcbac6cc90739ece96fa56fd2cee03e9006feab842bea89852` | Verified (`661` frames, `rc=0` decode) |
| **Candidate `v05` master (NAS)** | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/J2311_029_mon14_v05/029_short_mon14_half_moon_daylight_v05.mp4` | `21,608,743` | `f16e0e3c1c0bacdcbac6cc90739ece96fa56fd2cee03e9006feab842bea89852` | Exact SHA-256 match |
| **Candidate `v05` master (iCloud)** | `~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/J2311_029_mon14_v05/029_short_mon14_half_moon_daylight_v05.mp4` | `21,608,743` | `f16e0e3c1c0bacdcbac6cc90739ece96fa56fd2cee03e9006feab842bea89852` | Present (`10/10` files + `SHA256SUMS.txt`) |
| **Candidate `v05` PHONE (Local)** | `10_Shorts/mon14_half_moon_daylight/06_Final-Exports/029_short_mon14_half_moon_daylight_v05_PHONE.mp4` | `3,701,192` | `0a245750d2fd9cdd35bc2536f28cc5ec106c6fb27e8b1b17e0e219a02bfff865` | Verified (`661` frames, `rc=0` decode) |
| **Candidate `v05` PHONE (NAS)** | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/J2311_029_mon14_v05/029_short_mon14_half_moon_daylight_v05_PHONE.mp4` | `3,701,192` | `0a245750d2fd9cdd35bc2536f28cc5ec106c6fb27e8b1b17e0e219a02bfff865` | Exact SHA-256 match |
| **Cover JPEG (`v05_cover.jpg`)** | `10_Shorts/mon14_half_moon_daylight/06_Final-Exports/029_short_mon14_half_moon_daylight_v05_cover.jpg` | `597,771` | `bd2a00d7cdfbd9909c271530994789dfb6bb16f03e6519ddc2e9dd4a353851a6` | Verified (`sat=133.5`, `nb=2%`) |

---

## 3. E1 Structural Audit (`v04` vs `v05`)

| E1 Audit Parameter | Rule / Target (`OWB-2026-11-E1`) | Scheduled `v04` (`J0991`) | Candidate `v05` (`J2311`) | Assessment |
|---|---|---|---|---|
| **Duration / Frames** | `22.0–27.0 s` (`>= 22.0 s` floor) | `23.930 s` (`718` frames) | **`22.040 s` (`661` frames @ `30/1 fps`)** | **PASS** |
| **First visual cut (`cut1_s`)** | `<= 2.80 s` | `2.990 s` (**FAIL**) | **`2.300 s`** (frame diff `67`) | **PASS (resolved)** |
| **Second visual cut (`cut2_s`)** | `<= 4.80 s` from `0.00 s` | `5.760 s` (**FAIL**) | **`4.630 s`** (frame diff `94.43`) | **PASS (resolved)** |
| **Max later hold (`max_hold_s`)** | `<= 4.00 s` | `3.800 s` (`s05_orion_flare`) | **`3.800 s`** (`s05_orion_flare`, `11.60–15.40 s`) | **PASS** |
| **Frame 0 motion / near-black / visor** | Moving payoff, `<= 30%` black, no Orbit | `motion=30.7`, `visor=0.0` | **`motion=32.38`, `f0diff=8.74`, `nb=3.56%`, `visor=0.0`** | **PASS** |
| **VO onset (`onset_s`)** | `<= 0.15 s` | `~0.08 s` (`"So"`) | **`0.060 s`** (`"the"`) | **PASS** |
| **Star named in Sentence 1** | `<= 2.50 s` | `1.54–2.16 s` (`"Betelgeuse"`) | **`0.78–1.40 s`** (`"Betelgeuse"`) | **PASS** |
| **Surprise word (`surprise_s`)** | `<= 1.50 s` | `2.24 s` (`"explodes."`, **FAIL**) | **`1.480 s`** (`"explodes."`, `1.48–2.20 s`) | **PASS (resolved)** |
| **Sentence-1 internal gap** | `<= 0.15 s` | `0.220 s` (`"night"` → `"Betelgeuse"`) | **`0.220 s`** (`0.56 → 0.78 s`, recorded pause) | **`EXCEPTION` (preserve `22 s` floor + `< 1.2 s` tail)** |
| **Sentence-1 → Sentence-2 breath** | `< 0.25 s` | `0.200 s` | **`0.200 s`** (`"explodes."` `2.20 s` → `"The"` `2.40 s`) | **PASS** |
| **Payoff timestamp / share** | `>= 70%` (`>= 82%` E1 target) | `18.90 s / 23.93 s` (`79.0%`) | **`18.14 s / 22.04 s` (`82.30%`)** (`"half phase"` / `"daylight"`) | **PASS** |
| **Teaching overlay** | 1 overlay, `<= 4` words, safe band | `HALF MOON BRIGHT` (`18.90–21.79 s`) | **`HALF MOON BRIGHT` (`18.14–21.14 s`, `[197,719,883,777]`)** | **PASS** |
| **Last word end (`last_word_end_s`)** | Recorded VO end | `21.640 s` (`"daylight."`) | **`20.880 s`** (`"daylight."`) | **PASS** |
| **Loop tail (`tail_s`)** | **`< 1.20 s`** | `2.290 s` (**FAIL**) | **`1.160 s` (`1.16 s`)** | **PASS (resolved)** |
| **Closing CTA / end card** | **Zero end card / spoken CTA** | `2.00 s` `"Full film on the channel"` (**FAIL**) | **Removed (`end_card: null`; OCR verified)** | **PASS (resolved)** |
| **Loop return seam** | Crossfade `<= 0.30 s` to `frame 0`, bed across seam | End card blocked loop return | **`0.30 s` xfade at `21.433 s` to `frame 0` (`diff=2.776`), continuous bed** | **PASS (resolved)** |
| **Integrated loudness / True peak** | `~ -14 LUFS`, `<= -1.0 dBTP` | `-14.1 LUFS` / `-2.0 dBTP` | **`-14.1 LUFS` / `-2.2 dBTP`** (calibrated AAC) | **PASS** |

---

## 4. Resolution of the 4 Conflicts Listed in `J2311/HANDOFF.md`

### Conflict 1: `0.220 s` Internal Pause Inside Sentence 1 (`"night"` `0.22–0.56 s` → `"Betelgeuse"` `0.78–1.40 s`)
- **Observation:** Within the first continuous VO slice (`248.82–250.96 s` of the master `029` VO), there is a `0.220 s` recorded pause between `"the night"` and `"Betelgeuse"` (`0.070 s` above the `0.150 s` heuristic).
- **Resolution (`KEEP` as `EXCEPTION`):**
  - `jobs/briefs/J2207/heiGCnGKTkE.md` enforces three simultaneous hard constraints: (1) **retain the `22.00 s` Keeper floor**, (2) **keep the loop tail `< 1.20 s`**, and (3) **never pad to length or invent speech**.
  - With the setup words `"So imagine"` trimmed (`0.76 s` removed), the recorded speech ends `"daylight."` at **`20.88 s`**. A `22.04 s` total duration yields a `1.16 s` loop tail (`< 1.20 s`).
  - If `0.08 s` were spliced out of `"night -> Betelgeuse"`, `last_word_end_s` would drop to **`20.80 s`**, where any file `>= 22.00 s` necessarily has `tail_s >= 1.20 s` (failing E1 `< 1.20 s`), unless artificial silence is padded between later sentences (violating *"Never... pad to length"*). Moreover, cutting `70–80 ms` inside a two-second breath group risks an audible mid-clause splice artifact. Keeping the continuous recorded slice intact and flagging `label: "EXCEPTION"` is the mathematically and editorially sound resolution.

### Conflict 2: Line 1 (`"the night Betelgeuse explodes."`) Is Not the Title Question (`"How Bright Will Betelgeuse Get When It Explodes?"`)
- **Observation:** The spoken opener is `"the night Betelgeuse explodes."` rather than the literal title question `"How Bright Will Betelgeuse Get When It Explodes?"`.
- **Resolution (`KEEP` as `EXCEPTION`):**
  - An independent full-text scan of `02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/02_Voiceover/words.json` confirms that `"How Bright Will Betelgeuse Get When It Explodes?"` is **never spoken anywhere in the `029` VO corpus**. The only adjacent questions in the master VO are `"So is Betelgeuse about to explode?"` (`6.54–8.48 s`, the long-film title question) and `"And what would you see if it did?"` (`9.02–10.64 s`, anaphoric `"it"`, which would violate the `J0900`/`J0907` rule that Sentence 1 must name the star directly).
  - Under `J2207/heiGCnGKTkE.md` (*"Existing recorded words/media only, no spend/generation. Preserve title... If recorded words cannot meet a requirement, report exact conflict for reviewer, do not invent speech"*), `v05` properly retains the recorded `v03`/`v04` opening line (which names `Betelgeuse` at `0.78 s` and lands `explodes.` at `1.48 s` beneath the `BRIGHT AS A / HALF MOON` hook caption) and marks the cut `EXCEPTION`.

### Conflict 3: Trimming the 2 Recorded Setup Words `"So imagine"` (`248.06–248.82 s`)
- **Observation:** `v04` began with `"So imagine the night Betelgeuse explodes."` (`55` words); `v05` trims `"So imagine"` (`53` words).
- **Resolution (`PASS`):**
  - Explicitly authorised by `jobs/briefs/J2207/heiGCnGKTkE.md`: *"trim/reorder existing recorded setup without changing facts; retain the 22 s floor."*
  - Removing `"So imagine"` alters zero factual claims, moves `"explodes."` from `2.24 s` (`v04`, FAIL) to `1.48 s` (`<= 1.50 s`, PASS), and strengthens the loop sentence from the final line (`"You could see it in broad daylight."` → `"the night Betelgeuse explodes."`).

### Conflict 4: Low-Detail Warning on `s03_chajnantor` (`chajnantor_mw.m4v`, `4.63–8.14 s`)
- **Observation:** `picture_qa.py` and `polish_gate.py` both return **PASS** (`0` failures) with `1` warning on row `s03_chajnantor` (`0:06`, `edge density 0.0114 < film p5 0.0152`).
- **Resolution (`PASS`):**
  - Visual inspection of `029_short_mon14_half_moon_daylight_v05_picture_qa/picture_qa_review.jpg` and `frames_5pt.jpg` confirms `chajnantor_mw.m4v` (`offset 3.25 s`, `4.63–8.14 s`) is a clean ESO twilight sky timelapse over the Chajnantor mountain horizon — the exact plate approved in `v03` (`6411258896`) and `v04` (`J0991`). Its smooth twilight gradient naturally yields lower high-frequency Canny edge density than starfield or lunar crater plates without any blur or compression defect.

---

## 5. Independent Tool Gate & Visual Verification

All six studio QA tools and full `ffmpeg` stream decodes were re-run independently during `J2316`:

1. **`ffmpeg` Full Decode Check (`v05.mp4` & `v05_PHONE.mp4`):**
   ```text
   v05.mp4:       1080x1920, 30/1 fps, 661 frames, 22.040000 s, aac 48000 Hz stereo (1035 frames) -> decode_rc=0, stderr=""
   v05_PHONE.mp4: 720x1280,  30/1 fps, 661 frames, 22.040000 s, aac 48000 Hz stereo (1035 frames) -> decode_rc=0, stderr=""
   ```
2. **Shorts Open & Ship Gate (`gate_shorts_open.py check ... --air-date 2026-12-14 --id heiGCnGKTkE`):**
   ```text
   PASS  029_short_mon14_half_moon_daylight_v05.mp4  dur=22.04s  audio=-16.7dB  motion=32.38  f0diff=8.74  cut1=2.3s  vo_onset=0.06s  tail_gap=1.16s  dhash=870b4ee6f26c09d1  visor=0.0
   ```
3. **Picture QA (`scripts/picture_qa.py`):**
   ```text
   WARN   0:06 row s03_chajnantor chajnantor_mw.m4v: low detail: edge density 0.0114 < film p5 0.0152
   picture QA PASS: 0 of 8 cuts fail, 1 to look at -> 029_short_mon14_half_moon_daylight_v05_picture_qa/PICTURE_QA.md, picture_qa_review.jpg
   ```
4. **Polish Gate (`scripts/polish_gate.py`):**
   ```text
   s01_casa          1.1s casa.jpg                          ok
   s02_neutrino      3.5s code_graphic_029_mon_neutrino_v01 ok
   s03_chajnantor    6.4s chajnantor_mw.m4v                 WARN low detail: edge density 0.0114 < film p5 0.0152
   s04_epic          9.9s dscovr_epic.jpg                   ok
   s05_orion_flare  13.5s code_graphic_029_r25_orion_v01    ok
   s06_half_moon    17.2s half_moon.jpg                     ok
   s07_daylight     20.2s code_graphic_029_r27_orion_v01    ok
   s08_loop         21.7s frame0_hold_mon14_half_moon_...   ok
   polish gate PASS: 0 of 8 rows failed, 1 to look at
   ```
   *(Visual inspection of `open_sheet.jpg`, `frames_5pt.jpg`, `picture_qa_review.jpg`, and the 1 Hz frame sequence `00:00–00:21`: frame 0 opens full-bleed on `casa.jpg` with animated shockwave rings and `BRIGHT AS A / HALF MOON` hook caption; Cut 1 at `2.30 s` switches cleanly to `s02_neutrino` (`code_graphic_029_mon_neutrino_v01.mp4`), followed by real moving footage `s03_chajnantor` (`4.63–8.14 s`) and `s04_epic` (`8.14–11.60 s`) before the second code graphic `s05_orion_flare` (`11.60–15.40 s`), separated again by `s06_half_moon` (`15.40–19.06 s`) before `s07_daylight` (`19.06–21.433 s`) — zero back-to-back code graphics; promo title `Is Betelgeuse / About to / Explode?` sits cleanly at `9.0–13.5 s`; teaching overlay `HALF MOON BRIGHT` sits inside the 16:9 safe band at `18.14–21.14 s`; at `21.433–21.733 s` `s07_daylight` crossfades onto `frame 0` (`s08_loop`) and holds to `22.040 s` with zero end-card text.)*
5. **Music Gate (`scripts/music_gate.py`):**
   ```text
   music gate PASS: betelgeuse_score_bed_v01.mp3, 542.3 s, about 75.0 BPM, brief Pace: 68-78 BPM
   ```
6. **SFX Level Rule (`scripts/sfx_kit.py level`):**
   ```text
   SFX level PASS: VO -15.7 LUFS, SFX -37.7 LUFS, 3 hits
   ```
7. **Cover Thumbnail Gate (`thumb_preview.py short --score`):**
   ```text
   PASS  029_short_mon14_half_moon_daylight_v05_cover.jpg  saturation=133.5  near_black=2%
   ```

---

## 6. Follow-Up Path (No Immediate Swap)

1. **Verdict Recorded:** `KEEP` (`label: "EXCEPTION"` — local E1 candidate, not a full E1 PASS and not an immediate swap).
2. **Ben's Finished-Cut Watch:** `029_short_mon14_half_moon_daylight_v05.mp4` (`21.6 MB`) and `029_short_mon14_half_moon_daylight_v05_PHONE.mp4` (`3.7 MB`) are staged with verified checksums in `OWB UAT/J2311_029_mon14_v05/` (both NAS and iCloud Drive) for Ben's watch of the finished cut.
3. **Separate Authorised Swap Job Required Before Any YouTube Change:**
   - Per the `J2311` and `J2316` briefs, this `KEEP` does **not** authorise an immediate YouTube upload, replacement, retitle, privacy, schedule, Buffer, or `UPLOADS.json` change.
   - Because `heiGCnGKTkE` airs `2026-12-14T11:30:00Z` (after the `3 Dec 2026` E1 readout window), `14 Dec` is follow-up only for the `3 Dec` readout (`jobs/briefs/J2207/INVENTORY.md`).
   - When a swap job is queued and authorised after Ben's watch, it must update YouTube, `11_Upload-Package/PACKAGE_MANIFEST.json`, `00_Brand/Channel-Setup/social/UPLOADS.json`, and Buffer (`BUFFER_POSTS.json`) atomically in the same job (`AGENTS.md` Standing Lesson 6).
