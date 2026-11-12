# J2485 — HOS 008 Short C v03 First-Second Gate (Rule 24) & Listening/Visual Review

- **Reviewer:** `gemini` (`gemini-argon`)
- **Date:** 12 Nov 2026
- **Master inspected:** `02_Video-Projects/008_Lightning-Franklin/10_Shorts/hos_008_short_C_v03.mp4`
  - **SHA-256:** `9f25a16de5fc7d454be7adbc0e301614c7b060cd28b10cd076bcd2b4a6642161`
  - **Duration / Format:** `22.708333 s` (`545` frames at `24 fps`, `936×1664`, `-14.1 LUFS`, `-1.9 dBTP`)
- **Evidence PR (Step 1):** [`TheLaughingGod1986/history-of-science#555`](https://github.com/TheLaughingGod1986/history-of-science/pull/555) (`cursor/J2255-short-c` merged with `origin/main`, `check_all.sh` PASS, `02_Video-Projects/008_Lightning-Franklin/10_Shorts/J2255/gate_shorts_open.json` added)
- **Overall Verdict:** **`FIX`** (re-cut to `hos_008_short_C_v04.mp4` using existing voice and picture only, `£0`)

---

## 1. First-Second Gate (`gate_shorts_open.py`, Rule 24) & Sentence-1 Timing Numbers

Command run:
```bash
python3 00_Brand/Channel-Setup/tools/gate_shorts_open.py check \
  "02_Video-Projects/008_Lightning-Franklin/10_Shorts/hos_008_short_C_v03.mp4" \
  --air-date 2026-12-02
```

### Required First-Second & Sentence-1 Metrics

| Metric | Requirement | Measured Value (`hos_008_short_C_v03.mp4`) | Status |
|---|---|---|---|
| **Subject spoken** (`"lightning rod"` / `"rooftop lightning rod"`) | Spoken by `<= 1.50 s` | `"rooftop"` `0.340–0.780 s`, `"lightning"` `0.880–1.200 s`, `"rod"` `1.280–1.480 s` (subject completed at **`1.480 s`**) | **PASS** (`1.480 s <= 1.50 s`) |
| **Surprise word spoken** (`"Franklin's"` / `"Franklin's idea"`) | Spoken by `<= 1.50 s` | `"was"` `1.560–1.680 s`, `"Franklin's"` **`1.720–2.260 s`**, `"idea"` `2.340–2.680 s` | **FAIL** (`1.720–2.260 s > 1.50 s`) |
| **Voice onset** | `<= 0.15 s` | **`0.100 s`** word start (`"That"` `0.100–0.220 s`; acoustic `vo_onset_s = 0.088 s`) | **PASS** (`0.100 s <= 0.15 s`) |
| **Longest pause in sentence 1** | `<= 0.15 s` | **`0.120 s`** (between `"That"` `0.220 s` and `"rooftop"` `0.340 s`; all other sentence-1 inter-word gaps are `0.100 s`, `0.080 s`, `0.040 s`, `0.020 s`, `0.080 s`) | **PASS** (`0.120 s <= 0.15 s`) |
| **Something moves at frame 0** | Motion in `0–1.0 s` (`>= 10.0`) & `0–1.5 s` (`>= 1.50`) | **`PASS`** — `motion_0_1s = 44.49`, `frame0_diff_0_1_5s = 7.81`, `frame0_kick_0_0_5s = 7.81`, `frame0_luma_0s = 106.94 -> 136.77`, `frame0_hook_edge_0s = 0.0054 >= 0.0050` (`FRANKLIN'S / ROD` hook card on frame 0 over active lightning strike on tower spire) | **PASS** |
| **`gate_shorts_open.py` automated checks** | `0` fails, `0` stayed_fails | `verdict = PASS` (`duration = 22.71 s`, `cut1 = 2.833 s <= 3.0 s`, `tail_gap = 1.13 s <= 1.5 s`, `-14.1 LUFS`, `-1.9 dBTP`, `full_bleed = PASS` on `23/23` 1s and `46/46` 0.5s frames) | **PASS** |

---

## 2. Listening & 1 fps Visual Review (`00:00` to `00:22`)

Both the audio stream (`hos_008_short_C_s01_v03.mp3` and the muxed master audio in `hos_008_short_C_v03.mp4`) and all 23 one-frame-per-second frames (`00:00..00:22`) were inspected directly via native audio and video input.

- **Audio & Mix:**
  - Narrator voice (`Ben Orbit Narrator`, ElevenLabs `eleven_v3`) is clean, natural, and crisp throughout; splice between sentence 1 (`0.10–2.68 s`) and the body (`2.90–21.58 s`) is seamless with no click or room-tone jump.
  - Music bed (`lightning008_score_bed_v02` slice, ~66.7 BPM) and house SFX (`kit_v01`, `-37.5 LUFS` vs VO `-20.0 LUFS`) sit cleanly under the voice without masking any consonant.
- **Visual & Caption Defects Requiring Re-cut (`FIX`):**
  - While the automated gates pass, the 1.5 s surprise-word timing rule (`"Franklin's"` at `1.720–2.260 s`) and four concrete visual/caption issues found during the 1 fps inspection require a zero-spend re-cut (`hos_008_short_C_v04.mp4`).

---

## 3. Timecoded Fix List for `hos_008_short_C_v04.mp4` (Existing Voice & Picture Only, `£0`)

### FIX 1 — `00:00.00–00:02.68` (`S01` VO): Bring the surprise word (`"Franklin's"`) inside `1.50 s` using the existing sentence-1 take (`£0`)
- **Problem:** In the 7-word sentence 1 (`"That rooftop lightning rod was Franklin's idea."`), `"rooftop"` (`0.340–0.780 s`) pushes `"Franklin's"` out to **`1.720–2.260 s`**, missing the `<= 1.50 s` surprise-word target.
- **Zero-spend fix on existing VO (`02_Video-Projects/008_Lightning-Franklin/10_Shorts/vo_v02/hos_008_short_C_s01_v03.wav`):**
  - Apply Chief h94's pre-approved 6-word zero-spend edit (`"That lightning rod was Franklin's idea."`, 55 words total across the Short, inside the `55–65` word lock) by excising `"rooftop"` (`0.300–0.840 s` with a `15 ms` zero-crossing crossfade) from `hos_008_short_C_s01_v03.wav`, trimming `0.060 s` of leading silence (`voice onset = 0.040 s <= 0.15 s`), and applying `atempo=1.06` (`<= 1.06` cap) on sentence 1.
  - With this edit on the existing take:
    - `"That"`: `0.040–0.153 s`
    - `"lightning"`: `0.228–0.530 s`
    - `"rod"`: `0.606–0.794 s` (subject completed by **`0.794 s <= 1.50 s`**)
    - `"was"`: `0.870–0.983 s`
    - `"Franklin's"`: **`1.021–1.500 s`** (surprise word starts at **`1.021 s`** and finishes by **`1.500 s`**)
    - `"idea."`: `1.575–1.896 s`
  - Adjust `S01` cut1 from `2.833 s` to **`2.042 s`** (`49` frames, `<= 3.0 s`) and pull the body VO start from `2.900 s` to **`2.100 s`** (extending the final shot / keeping total duration inside `22.0–27.0 s` by holding `S08`/`loop_tail` or keeping total duration `>= 22.00 s`).
  - *(Note per Step 3 of J2485: if a brand-new 1-sentence ElevenLabs take is wanted instead of the zero-spend edit on `hos_008_short_C_s01_v03.wav`, park for the Chief's price pass first. Do not spend ElevenLabs credits.)*

### FIX 2 — `00:04.92–00:05.06`, `00:07.96–00:08.04`, `00:12.70–00:12.78`, `00:17.38–00:17.48`, and `00:20.70–00:20.76`: Fix overlapping double-rendered body captions and 1-word orphan captions
- **Problem:** In `02_Video-Projects/008_Lightning-Franklin/10_Shorts/J2255/_build_short_c_v03.py` (`render_captions()`), each caption chunk's end time is set to `t1 = min(parts[-1]["end"] + 0.18, TOTAL - 1.05)` without clamping to the start of the next caption chunk (`next_t0`). Because inter-chunk speech pauses are `< 0.18 s` at 5 boundaries, two caption PNGs render simultaneously on top of each other (most visibly at `00:17.38–00:17.48`, where `"round the building and into the"` and `"earth."` overlap into unreadable garbled text `"round the buiearth. and into the"`). In addition, splitting strictly at `len(parts) >= 6` leaves 1-word orphan captions (`"one."` at `10.16–10.72 s` and `"earth."` at `17.38–17.90 s`).
- **Fix (`£0` in `_build_short_c_v04.py`):**
  1. Clamp every caption chunk's `t1` to `min(parts[-1]["end"] + 0.18, next_chunk_t0 - 0.04, TOTAL - 1.05)` so two body captions never overlap on any frame.
  2. Avoid 1–2 word orphan chunks at the end of a sentence: if `< 3` words remain before a sentence-ending punctuation mark (`.` / `?` / `!`), keep them in the current caption chunk (up to 7–8 words across 2 balanced lines) or split the sentence into two balanced halves (e.g., `4 + 3` words instead of `6 + 1`).

### FIX 3 — `00:16.71–00:19.42` (`S07`, `06_rod_fitting_c1_t1.mp4`): Shift source offset from `1.50 s` to `3.10 s` to eliminate the mid-air shovel-blade morph at `00:18`
- **Problem:** `S07` uses `04_Generated-Clips/part05/raw/v01/06_rod_fitting_c1_t1.mp4` at `offset = 1.50 s` (`dur = 2.708 s`). At `t = 1.8–2.9 s` of that raw clip (landing at `00:17.5–00:18.5` in the Short), the workman lifts the iron rod out of the ground and its tip hallucinates into a giant triangular shovel/spearhead blade in mid-air before morphing back into a square bar when slammed down at `t = 3.0 s`.
- **Fix (existing picture, `£0`):** Change `S07` source offset in `06_rod_fitting_c1_t1.mp4` from `1.50 s` to **`3.10 s`** (`3.10–5.808 s` for a `2.708 s` window, or up to `6.00 s` if slightly longer). In `3.10–6.00 s` of `06_rod_fitting_c1_t1.mp4`, the square iron grounding bar is already driven straight into the soil and the workman kneels and packs damp earth firmly around its base with his hands — completely clean, zero morphing, and before the `7.0 s` top-spearhead artefact.

### FIX 4 — `00:13.92–00:16.71` (`S06`, `06_rod_fitting_t1.mp4`): Shift source offset from `1.50 s` to `4.00 s` to eliminate the vanishing hammer handle at `00:15`
- **Problem:** `S06` uses `04_Generated-Clips/part05/raw/v01/06_rod_fitting_t1.mp4` at `offset = 1.50 s` (`dur = 2.792 s`). At `t = 2.8–3.7 s` of the raw clip (landing at `00:15` in the Short), the hammer head detaches/loses its handle and the workman's right forearm blurs into his chin as he lowers his arm.
- **Fix (existing picture, `£0`):** Change `S06` source offset in `06_rod_fitting_t1.mp4` from `1.50 s` to **`4.00 s`** (`4.00–6.792 s`). In `4.00–6.792 s`, the hammer is out of frame and the workman cleanly holds and aligns the vertical iron conductor rod against the brick wall with both hands.

### FIX 5 — `00:00.00–00:05.58` & `00:21.75–00:22.71` (`S01`, `S02`, `loop_tail`): Per-shot horizontal `9:16` crop centering (`405×720 -> 936×1664`)
- **Problem:** `_build_short_c_v03.py` used a single hardcoded crop (`x = 438, y = 0, w = 405, h = 720`) on every shot:
  - In **`S02`** (`01_house_rod_t1.mp4`, `"Before him, people rang church bells..."`), the brick gable, chimney, and lightning rod on Franklin's house sit on the left side of the `1280×720` frame (`x ≈ 200..440`). Cropping at `x = 438..843` cropped the chimney and lightning rod completely off the left edge, leaving only empty dormer windows and sky.
  - In **`S01`** and **`loop_tail`** (`19_skyline_strike_t1.mp4`), the struck skyscraper spire and lightning bolt sit at `x ≈ 760..840` of the `1280×720` frame. Cropping at `x = 438..843` pushed the struck tower to the extreme right edge (`x ≈ 800..936` in the `936×1664` frame), directly under the YouTube Shorts right-rail UI icons.
- **Fix (existing picture, `£0`, keeping the exact `405×720 -> 936×1664` `2.3111×` scale factor):**
  - **`S02` (`01_house_rod_t1.mp4`):** Set `crop = [180, 0, 405, 720]` so Franklin's brick gable, chimney, and tall iron lightning rod are centred in the `9:16` frame.
  - **`S01` and `loop_tail` (`19_skyline_strike_t1.mp4`):** Set `crop = [600, 0, 405, 720]` so the lightning strike hitting the skyscraper rod is centred in the `9:16` frame.
