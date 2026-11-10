# J2258 Review — HOS 006 Short B v01 and Short C v02 (Ref: J2169)

- **Reviewer**: `gemini` (`gemini-argon` / Gemini 4 Argon High, Mini specialist worker)
- **Date**: 2026-11-05
- **Reviewed Job**: `J2169` (`HOS 006: build active Short B and C for 18 and 21 Nov from existing media`)
- **Evidence Commit**: HOS branch `cursor/J2169-shorts-bc`, commit `699c359bf44ccda9d996dae4a2d6524be3774a03` (`02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/j2169_v01/ASSEMBLY.md`; parent commit `8b3796e3fcf41b727af81d0a064ef9884af0e5d2` records the `Short_C v01` centre-crop fail)
- **Verdict**: **`FIX`** (rebuild `Short_B` as `v02` and `Short_C` as `v03` from existing local/NAS plates and audio stems at **£0 / 0 credits**)
- **Approval / Gate Status**:
  - Neither cut is approved for publication (`awaits_ben` is **not** set).
  - `watched: false` and `heard: false` remain unchanged until Ben's watch.
  - Long `VbPubYd6Fbs` (*The Willow Tree That Was Made of Air*) must be public before either Short.
  - Target slots `2026-11-18 11:30` and `2026-11-21 11:30` Europe/London remain planning targets only, not a schedule.
  - Standalone `S7` (`hos_sa_s7_priestley_mint_v02`) was not built and stays planned.
  - **Spend**: £0 / 0 credits. No upload, schedule, privacy change, retitle, or Buffer write performed.

---

## 1. File Integrity, Hashes, Decode, and Repo Gate Verification

All rendered deliverables in `/Users/benjaminoats/_desk/renders/J2169/` and `/Volumes/data/mac-mini-archive/hos-worktrees/2026-10-22/hos-006-trees/02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/J2169/` were verified directly on the Mac mini:

| Artifact | SHA-256 | Desk vs NAS | Stream & Decode Check (`ffmpeg` + `freezedetect=n=0.003:d=0.5`) |
|---|---|---|---|
| `Short_B/hos006_short_b_v01.mp4` | `08e3d6036744da57ae3fce1d12b996f913cd1d180161eba18590cffd23aeee0f` | Exact match (`10,329,133` B) | `720×1280` (`9:16`), `h264`, `24 fps` CFR, `24.250000 s` (`582` frames), AAC `48 kHz` stereo, `0` decode errors, `0` freezes |
| `Short_B/picture.mp4` | `d1153d948ec85288fdc609c88ce93b7c071d53c489639a5f1cc06184790090c4` | Desk (`12,591,192` B) | `720×1280`, `24 fps` CFR, `24.250000 s` (`582` frames), `0` decode errors, `0` freezes |
| `Short_C/hos006_short_c_v02.mp4` | `3f8c1390523cbf05632abefb592b178b2b211c0e74ae31e9c4b7b96423091327` | Exact match (`16,704,003` B) | `720×1280` (`9:16`), `h264`, `24 fps` CFR, `25.166667 s` (`604` frames), AAC `48 kHz` stereo, `0` decode errors, `0` freezes |
| `Short_C/picture.mp4` | `a1ef55df1c7ea819a76b806d34bd3ce623ab589b4e6667129c58a9974f77d952` | Desk (`20,991,895` B) | `720×1280`, `24 fps` CFR, `25.166667 s` (`604` frames), `0` decode errors, `0` freezes |
| `Short_C/centre_crop_v01/hos006_short_c_v01.mp4` | `883cee08cb5e197ef6dfe5f44a1f8ae47cfeaa5c576a14f5aad2670fe516fbc2` | Exact match (`16,194,251` B) | Kept on disk/NAS for audit history; excluded from offer due to `S02` brick-course seam fail |
| `Short_B` VO (`t2_mint_fixed_vo_v03b.mp3`) | `0f109926527ddbd5e4471b758ab54ccdc84369e439decf966801841dfab0c2b4` | Locked take | 61 words (`0.00–23.24 s`); sentence 1 *"A sprig of mint repaired the air."* ends at `2.24 s` |
| `Short_C` VO (`t3_bubbles_sunlight_vo_v01.mp3`) | `5b5d84e57b5b49b03f5dc782c616c1b304f7510f7b0c276227f8c316e731de56` | Locked take | 64 words (`0.00–24.16 s`); sentence 1 *"Leaves only make oxygen in the light."* ends at `2.56 s` |
| Score bed (`trees006_score_bed_v01.mp3`) | `942c643850c6dc87ffbd12396984d3a7fa2318c78a7f6c9a55622a406875f854` | Locked bed | `66.7 BPM` (brief `Pace: 60-72 BPM`), full-runtime cover on both cuts |

- **HOS CI check (`00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/006_Trees-Are-Made-Of-Air`)**: `ALL CHECKS PASS` (`durable desk handoffs: PASS`, `no media: PASS`, `status board in sync: PASS`, `ElevenLabs guard tests: PASS`, `vo_check word tests: PASS`, `atempo check tests: PASS`, `voice speed (atempo <= 1.06): PASS`, `contract tests: PASS`, `package-lint: PASS`, `review:script trees_script_master_v02.md: PASS (93.7/100)`, `gate:episode: PASS`).
- **Automated Gate Exit Codes on `Short_B v01` and `Short_C v02`**: `picture_qa.py` (`PASS`), `polish_gate.py` (`PASS`), `sfx_kit.py level` (`PASS`: `Short_B` VO `-18.1 LUFS`, SFX `-36.1 LUFS`, bed `-36.4 LUFS`; `Short_C` VO `-17.6 LUFS`, SFX `-35.6 LUFS`, bed `-35.8 LUFS`), `music_gate.py` (`PASS`), and `gate_shorts_open.py check` (`PASS` for air dates `2026-11-18` and `2026-11-21`).

---

## 2. Explicit Rulings on Every Tool `WARN` and Source Plate (No `WARN` Waived by Silence)

Every row of `Short_B v01` (`S01..S07`, `loop_tail`) and `Short_C v02` (`S01..S08`, `loop_tail`) was inspected at full resolution on `Short_B/picture_qa_picture/picture_qa_review.jpg`, `Short_B/picture_qa_master/picture_qa_review.jpg`, `Short_C/picture_qa_picture/picture_qa_review.jpg`, `Short_C/picture_qa_master/picture_qa_review.jpg`, and per-row start/mid/end 9:16 contact sheets:

1. **WARN — `Short_B` Row `S07` (`19.500–23.250 s`, `0:21`, `01_soil_to_sky_t1.mp4` crop `[600, 0, 608, 1080]`) — `low detail: edge density 0.0225 < film p5 0.0293` (`picture_qa_picture`) / `0.0259 < film p5 0.0327` (`polish_gate`)**:
   - **Ruling: `KEEP` source plate and crop.** Full-size visual inspection confirms a crisp, well-lit 3D-cartoon close-up of a green plant stem and leaves rising against an open blue sky with soft clouds (`luma std = 61.26`, `edge8 = 0.224`, `max_upscale = 1.184×`). The lower full-frame Canny edge density comes from the smooth sky gradient behind the smooth 3D plant leaves, not blur, softness, or compression artefacts. It clearly illustrates the spoken beat (*"Every green leaf on Earth does the same trick..."*) with the sound off.
2. **WARN — `Short_C v02` Row `S05` (`12.042–15.000 s`, `0:14`, `03_pot_jar_leaf_t1.mp4` crop `[1120, 0, 608, 1080]`) — `low detail: edge density 0.0339 < film p5 0.0359` (`picture_qa_picture`) / `0.0498 < film p5 0.0507` (`polish_gate`)**:
   - **Ruling: `KEEP` source plate and crop.** Full-size visual inspection confirms a sharp, sunlit glass jar containing a green leaf with tiny rising silver bubbles on a wooden table before a warm sunlit window (`luma std = 55.30`, `edge8 = 0.264`, `max_upscale = 1.184×`). Its edge density (`0.0498`) sits `0.0009` below the film's 5th percentile (`0.0507`) only because the remaining cuts in `Short_C` are high-frequency macro bubble plates (`edge = 0.0968–0.1614`) and Georgian brickwork (`0.1064`). It matches *"Tiny silver bubbles rose from the green leaves."* with the sound off.
3. **`Short_C v02` Row `S02` (`2.583–5.708 s`, `01_villa_t1.mp4` corner crop `[144, 0, 608, 1080]`)**:
   - **Ruling: `KEEP` source plate and crop.** Shifting from the `v01` centre crop `[656, 0, 608, 1080]` (`883cee08...`, which failed `polish_gate` on full-width horizontal brick courses) to `[144, 0, 608, 1080]` (`3f8c1390...`) frames the trees on the left, the Georgian brick villa facade, stone quoins, windows, and specimen jars on the windowsill, clearing `polish_gate` (`seams: []`, `edge: 0.1064`, `std: 32.75`) while matching *"In seventeen seventy-nine, Jan Ingenhousz rented a quiet brick villa outside London."*
4. **All 6 `J2213` Flow Veo 3.1 Quality 720p Inserts in Context (`Short_B S02`, `Short_B S06`, `Short_C S01`/`loop_tail`, `Short_C S06`, `Short_C S07`, `Short_C S08`)**:
   - **Ruling: `KEEP` all 6 source plates.** Every plate matches its spoken sentence with the sound off:
     - `Short_B S02` (`short_b_s02_t01.mp4`, `2.250–6.292 s`): lit candle burning alone inside a sealed glass bell jar (no mint sprig), matching *"In seventeen seventy-one, Joseph Priestley sealed a burning candle inside a glass jar until the flame died."*
     - `Short_B S06` (`short_b_s06_t01.mp4`, `16.333–19.500 s`): candle flame burning bright and steady beside the green mint sprig inside the sealed bell jar, matching *"It burned bright and steady. The plant had remade what the fire had used up."*
     - `Short_C S01` / `loop_tail` (`short_c_s01_t01.mp4`): sunlit underwater green leaf with rising silver oxygen bubbles, matching *"Leaves only make oxygen in the light."*
     - `Short_C S06` (`short_c_s06_t01.mp4`, `15.000–18.458 s`, `offset = 4.375 s`): jar sitting in daytime room shade with still water and no bubbles, matching *"When he moved the same jars into the shade, the bubbles stopped."* *(Minor trim note for rebuild: at `offset = 4.375 s`, the fingertips of the gloved hand are still visible at the right frame edge for the first ~2 frames (`15.00–15.08 s`); shifting `offset` to `4.458 s` (`107 / 24`, running `4.458–7.917 s` of the `8.00 s` clip) starts the cut after the hand has completely cleared the frame.)*
     - `Short_C S07` (`short_c_s07_t01.mp4`, `18.458–20.875 s`): bare hands sliding the glass jar back into the warm sunbeam as tiny bubbles resume, matching *"Back in the sun, they started again."*
     - `Short_C S08` (`short_c_s08_t01.mp4`, `20.875–24.167 s`): sunlit underwater leaf releasing rising silver bubbles, matching *"Sunlight was the engine, and the green leaf was the machine."*
5. **WARN — `terminal_loop.py` (`status == 'rendered_correspondence' is a sample check and does not establish seamless motion`)**:
   - **Ruling: Addressed in `FIX 4` below** (fixing the `offset = 1.0 s` jump between `loop_tail` end at `source_t = 2.0 s` and `S01` start at `source_t = 1.0 s`); final real-time motion approval stays with Ben's watch.
6. **WARN — `music_gate.json` (`couldn't read saturn_long_vo_v02_LISTEN.wav...`)**:
   - **Ruling: `KEEP` / accepted.** These warnings refer to archived OWB Saturn/Jupiter WAVs not stored on local disk; `trees006_score_bed_v01.mp3` passes all `music_gate.py` checks (`fail: []`, `matches: []`).

---

## 3. Required Fixes (`FIX` List by Row)

Both `Short_B v01` and `Short_C v02` require an assembly/burn rebuild in `/Users/benjaminoats/_desk/renders/J2169/build_j2169.py` before they can be marked `KEEP`:

### FIX 1 — Missing Spoken Captions Across the Entire `9.00–14.00 s` Window + Dropped End-of-Hook Words + Single-Word Flashing
- **Affected Rows**:
  - `Short_B`: `S01` (`1.88–2.25 s`), `S03` (`9.000–9.417 s`), `S04` (`9.417–13.042 s`), `S05` (`13.042–14.000 s`) — plus caption chunking across `S02..S07`.
  - `Short_C`: `S01` (`2.12–2.583 s`), `S04` (`9.000–12.042 s`), `S05` (`12.042–14.000 s`) — plus caption chunking across `S02..S08`.
- **Rule Violated**:
  - `00_Brand/Channel-Setup/HOS_STRATEGY.md` line 65: *"The promoted film's exact live title is on screen at 9–14 s. ... Captions all the way through."*
  - `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` §3 line 93: *"Captions throughout."*
- **What Happened in `build_j2169.py`**:
  - In `build_j2169.py` (`burn()`, lines 148–159 and 245–255), despite the comment `# Word line after the hook, held off the 9-14s title band by sitting at the bottom`, the code uses mutually exclusive `if t < 2.2: ... elif 9.0 <= t < 14.0: frame = plate("title", "title") else: ... and not (9.0 <= w["start"] < 14.0)`.
  - Consequently, **no spoken captions appear on screen for 5.0 full seconds (`9.00–14.00 s`)** while the top title card (`The Willow Tree / That Was Made of Air`) is displayed:
    - `Short_B` (`9.00–14.00 s`, rows `S03`, `S04`, `S05`): 13 spoken words (*"would light. He slid in a sprig of mint and waited. Ten days"*) are completely uncaptioned.
    - `Short_C` (`9.00–14.00 s`, rows `S04`, `S05`): 13 spoken words (*"of water by a sunny window. Tiny silver bubbles rose from the green"*) are completely uncaptioned.
  - Additionally, because the hook card turns off at hardcoded `t = 2.20 s` and the `else` branch requires `w["start"] >= 2.2`, the final word of sentence 1 (`"air."` in `Short_B S01`, `1.88–2.24 s`; `"light."` in `Short_C S01`, `2.12–2.56 s`) is dropped at `2.20 s`, leaving `2.20–2.56 s` in `Short_C S01` with no caption at all.
  - Finally, `build_j2169.py` flashes single words (`1` word at a time in `Georgia Bold`, leaving blank frames between words inside a sentence) instead of HOS house multi-word subtitle phrases (`Didot.ttc` bold, cream `(245, 232, 210)` with dark outline, 2–5 words per chunk as in `02_Video-Projects/007_The-First-Vaccine/10_Shorts/_build_short_s05_vacca_jesty_v05.py`).
- **Required Fix**:
  1. Hold the frame-0 hook caption through the actual end of sentence 1 (`0.00–2.250 s` in `Short_B S01`; `0.00–2.583 s` in `Short_C S01`) so sentence 1 is never left uncaptioned mid-word.
  2. Render HOS house multi-word subtitle chunks (`Didot.ttc` bold, cream `(245, 232, 210)` with dark stroke, 2–5 words per chunk, lower safe zone clear of YouTube Shorts bottom UI) continuously across all spoken sentences from sentence 2 (`2.62 s` in `Short_B`; `3.12 s` in `Short_C`) through the end of the VO (`23.24 s` in `Short_B`; `24.16 s` in `Short_C`), **including throughout `9.00–14.00 s`** while the promoted long title sits in the upper safe band.

### FIX 2 — Frame-0 Hook Caption Styling, Cap Height, and Vertical Placement
- **Affected Rows**:
  - `Short_B`: `S01` (`0.000–2.250 s`)
  - `Short_C`: `S01` (`0.000–2.583 s`)
- **Rule Violated**:
  - `00_Brand/Channel-Setup/THUMBNAIL_AND_TITLE_RULES.md` §3.3: *"A frame-0 caption: the promise in 2–4 words, cap height about 8–10% of the frame, yellow on the hook word, vertically centred and clear of the bottom UI."*
  - `AGENTS.md` line 192: *"The 22–27 s / under-40 s Shorts lock, and the yellow hook word on the frame-0 caption."*
- **What Happened in `build_j2169.py`**:
  - `build_j2169.py` (lines 189, 213–219) paints **every word** of `REPAIRED THE AIR` (`Short_B S01`) and `ONLY IN / THE LIGHT` (`Short_C S01`) in solid yellow `(255, 215, 0, 255)` (no cream/white vs yellow hook-word contrast), in `Georgia Bold` at `font_size = 64` (`cap height ≈ 44 px = 3.4%` of `1280` frame height, less than half the `8–10%` rule), positioned at the top edge (`y = 80`, `6.2%` from top) instead of vertically centred in the safe band.
- **Required Fix**:
  - Render the 2–4 word frame-0 hook caption in `Didot.ttc` bold with cap height `8–10%` of frame height, vertically centred in the safe band, with cream/white `(245, 232, 210)` on the setup words and **yellow `(246, 196, 69)` / `(255, 215, 0)` on the hook word(s) only** (e.g. `REPAIRED` in cream + `THE AIR` in yellow, or `MINT FIXED` in cream + `THE AIR` in yellow for `Short_B`; `ONLY IN` in cream + `THE LIGHT` in yellow for `Short_C`).

### FIX 3 — Cut Boundaries in `Short_B` Straddling Spoken Word Onsets + `Short_C S06` Hand-Exit Trim
- **Affected Rows**:
  - `Short_B`: `S05` (`13.042–16.333 s`), `S06` (`16.333–19.500 s`), `S07` (`19.500–23.250 s`)
  - `Short_C`: `S06` (`15.000–18.458 s`)
- **What Happened**:
  - In `Short_B`, `S05` ends at `16.333 s` (`392 / 24`), which cuts `33 ms` after the start of the word `"bright"` (`16.30–16.76 s` in `words.json`), and `S06` ends at `19.500 s` (`468 / 24`), which cuts `40 ms` after the start of the word `"the"` (`19.46–20.12 s`).
  - In `Short_C S06`, `short_c_s06_t01.mp4` starts at `offset = 4.375 s`, leaving the fingertips of the exiting gloved hand visible at the right edge for the first ~2 frames (`15.00–15.08 s`).
- **Required Fix**:
  - In `Short_B`: set `S05` to `78` frames (`3.250 s`, `13.042–16.292 s`, ending right before `"bright"` at `16.30 s`), keep `S06` at `76` frames (`3.167 s`, `16.292–19.458 s`, ending right before `"the"` at `19.46 s`), and set `S07` to `91` frames (`3.792 s`, `19.458–23.250 s`) so total duration stays `24.250 s` (`582` frames) and no cut lands inside a word onset.
  - In `Short_C S06`: shift `short_c_s06_t01.mp4` source `offset` from `4.375 s` to `4.458 s` (`107 / 24`, running `4.458–7.917 s` of the `8.00 s` source clip) so the hand has completely exited before the cut-in.

### FIX 4 — Terminal-Loop Continuity (`S01` / `loop_tail`) and `1080×1920` vs `720×1280` Delivery Resolution
- **Affected Rows**:
  - `Short_B`: `S01`..`loop_tail` (specifically `S01` `0.000–2.250 s` and `loop_tail` `23.250–24.250 s`)
  - `Short_C`: `S01`..`loop_tail` (specifically `S01` `0.000–2.583 s` and `loop_tail` `24.167–25.167 s`)
- **What Happened**:
  1. **Terminal-loop `offset = 1.0 s` jump on wrap**: Because `terminal_loop.py` line 125 enforces `first['framing']['offset'] == start and tail['framing']['offset'] == start`, `build_j2169.py` set both `S01` and `loop_tail` to `offset = 1.0 s` (`source_t = 1.0–2.0 s`). While that makes the `0.00 s` and `0.50 s` correspondence sample pairs match (`MAD = 0.25–4.14 <= 12.0`), the end of `loop_tail` (`source_t = 2.0 s`) jumps backward by `1.0 s` when the player wraps to frame 0 of `S01` (`source_t = 1.0 s`).
     - **Fix**: Set `offset = 0.0 s` on `S01` and `loop_tail` (both `03_mint_t1.mp4` and `short_c_s01_t01.mp4` are clean moving plates from `0.0 s`), and cross-dissolve the final `0.30–0.40 s` of `loop_tail` (`t_rel = 0.65–1.00 s`, after the `0.00 s` and `0.50 s` `rendered_correspondence` sample points) back into `source_t = 0.0 s` so that `rendered_correspondence` passes (`MAD <= 12.0` at `0.00 s` and `0.50 s`) **and** the wrap from the last frame of `loop_tail` to frame 0 of `S01` is genuinely seamless.
  2. **`720×1280` output vs `1080×1920` Shorts standard**:
     - `00_Brand/Channel-Setup/YOUTUBE_FRAME_SIZES.md` (`Shorts: 1080 × 1920, 9:16`) and Chief decision HOS #180 comment `6655551386` (5 Nov 2026: *"Final Shorts/long delivery stays 1080×1920 / 1920×1080 in assembly. That is edit output, not a requirement that Flow mint native 1080 source. Existing approved HOS films already ship from 720p Flow plates."*) specify `1080×1920` delivery for Shorts masters.
     - `build_j2169.py` rendered at `720×1280` because `terminal_loop.py` / `picture_qa.py` check `output_w / crop_w <= 2.35` (`1080 / 405 = 2.667× > 2.35×` on raw `1280×720` Flow plates).
     - **Fix**: Pre-normalise the `1280×720` Flow source plates (`03_mint_t1.mp4`, `02_bell_jar_mouse_t1.mp4`, and the 6 `J2213` inserts) to `1920×1080` (`scale=1920:1080:flags=lanczos`, matching `01_villa_t1.mp4`, `03_pot_jar_leaf_t1.mp4`, `02_van_helmont_weighing_t2.mp4`, and `01_soil_to_sky_t1.mp4`, as done in `_build_short_s05_vacca_jesty_v05.py`) so all 17 rows crop `608×1080` -> `1080×1920` (`max_upscale = 1.776× <= 2.35×`) and pass `picture_qa.py`, `polish_gate.py`, `terminal_loop.py`, and `gate_shorts_open.py` at full `1080×1920` resolution.
