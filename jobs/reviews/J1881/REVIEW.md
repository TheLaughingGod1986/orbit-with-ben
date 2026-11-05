# J1881 — Rule H Review: HOS 008 Franklin Eight-Item Correction Recipe (+ Film-Wide Captions)

- **Job:** `J1881` (`review Franklin eight-item correction recipe (+ film-wide captions) and scope production`)
- **Reviewer:** `gemini` (review lane)
- **Date:** 2026-11-05T16:42Z
- **Reviewed Deliverables & Evidence:**
  - `J2217` deliverable: HOS PR #428 (`cursor/J2217-eight-item`, commit `dfd365c7`, stacked on PR #411)
  - `J2163` deliverable: HOS PR #411 (`codex/J2163-repair`, commit `50620e408667c6ec0c8a959acd051fcfa458fd8d`)
  - Ben 5 Nov second `v03` review: HOS PR #180 comment `6658371896`, Claude advisory `6658387533`, Chief fold-in commit `4e94001e37fb63b59a1879fd1953854bfbe951d4` (`02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/J1868_BEN_NOTES_2026-11-05.md` and `J1868_UAT_CORRECTIONS.md`)
  - Prior review record: `02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/J1881_SCOPE_REVIEW.md` (PR #410, `712e2abf`)
- **Verdict:** **FIX (`J2217` HOS PR #428 `dfd365c7` reopened for cross-GOP frame-window and caption-frame-table repair; KEEP `J2163` PR #411 `50620e40` base PTS/planner architecture)**

---

## 1. Executive Decision

1. **Base Planner & PTS Repair (`J2163` / HOS PR #411 `50620e40`) — KEEP as Foundation:**
   - `J2163_MASTER_FRAME_PTS.json` records all `12,923` decoded frames of verified master `cf1561c218bace7bc14ed3d625b0790a457027a90f392262f45ca7172723099b` (`393,139,693` bytes, timebase `1/12288`, start `1536` ticks = `0.125s`, end `6630912` ticks = `539.625s`, duration `539.500s`, `113` keyframes, `23` steps of `1024` ticks and `1` step of `1536` ticks).
   - `_build_rough_v13_recipe.py` remains a strict read-only planner that refuses execution (`returncode 2`).

2. **Eight-Item Amend (`J2217` / HOS PR #428 `dfd365c7`) — FIX (Reopen `J2217`):**
   - `J2217` (`dfd365c7`) extended `J2163_CORRECTION_MANIFEST.json` with `eight_rows` and `caption_treatment`, correctly verified `2:18` (`frame 3305`, `138.0s`) is outside kept jar frames `3168..3259` and inside replace window `3260..3343`, preserved `six_rows`, kept execution refused (`returncode 2`), and passed 14 unit tests.
   - **However, `J2217` (`dfd365c7`) computed master frame windows for the two new rows (`0:51` and `3:13`) and all 27 `caption_treatment.labels` from `cuts_rough_v12.json`'s nominal `timeline_in`/`timeline_out` floats without accounting for the master's `0.125s` (`1536`-tick) start offset and the `23` inter-cut `1024`-tick steps in `J2163_MASTER_FRAME_PTS.json`:**
     - **Blocking Defect A (`0:51` `P1:07_hot_night` crosses cut boundary):** `eight_rows[2]` (`0:51`) sets `candidate_frames: [1124, 1227]` (`104` frames). In `J2163_MASTER_FRAME_PTS.json`, `P1:07_hot_night` is closed GOP **`[1129, 1231]`** (`103` frames; `frame 1129` has `key_frame=1`, PTS `580096` = `47.208333s`; `frame 1231` has `key_frame=0`, PTS `632832` = `51.500000s`, followed by `frame 1232` `key_frame=1` `P1:08_sky_flash`). Frames `1124..1128` (`key_frame=0`) are the last 5 frames of the previous cut `P1:06_heavens` (`1022..1128`). Because `1124 < 1129`, `build_plan()` expands `candidate_boundary_gop_envelope` backwards across the cut boundary to **`[1022, 1231]` (`210` frames spanning two cuts)** and leaves the last 4 frames (`1228..1231`) of `07_hot_night` outside `candidate_frames`.
     - **Blocking Defect B (`3:13` `P3:01_points_desk` crosses Part 2→3 boundary and leaves 11 defective frames untouched):** `eight_rows[5]` (`3:13`) sets `candidate_frames: [4500, 4659]` (`160` frames). In `J2163_MASTER_FRAME_PTS.json`, `P3:01_points_desk` is closed GOP **`[4511, 4670]`** (`160` frames; `frame 4511` has `key_frame=1`, PTS `2315264` = `188.416667s`; `frame 4670` has `key_frame=0`, PTS `2396672` = `195.041667s`, followed by `frame 4671` `key_frame=1` `P3:02_sentry_box`). Frame `4510` (`dur=1024` ticks) is the last frame of Part 2 (`P2:18_quill_down`, GOP `4405..4510`). Because `4500 < 4511`, `build_plan()` expands `candidate_boundary_gop_envelope` backwards across the Part 2→Part 3 boundary to **`[4405, 4670]` (`266` frames spanning two cuts)** and leaves frames **`4660..4670` (the final 11 frames of `01_points_desk`, `194.625–195.042s`, where the wide paper strip rolls out of the brass globe)** outside `candidate_frames`.
     - **Blocking Defect C (All 27 `caption_treatment.labels` `master_frames` drift by up to 22 frames / `0.917s`):** Every entry in `caption_treatment.labels` in `dfd365c7` uses non-keyframe `master_frames` derived from unadjusted `timeline_in`/`timeline_out` floats instead of the actual closed-GOP boundaries (`key_frame=1`) in `J2163_MASTER_FRAME_PTS.json` (Table 2.2 below). By Part 3 (`02_sentry_box`), `master_frames: [4659, 4820]` starts 12 frames early inside `01_points_desk`; by Part 5 (`19_skyline_strike`), `master_frames: [12275, 12440]` starts **22 frames (`0.917s`) early** inside `18_rod_closeup` (`12191..12296`) and ends 21 frames before `19_skyline_strike` (`12297..12461`) finishes.
     - **Blocking Defect D (Missing `required_inputs` entries, missing `3:13` retake reference/clean-frame cutoff, and missing GOP-alignment unit test):** `required_inputs` still lists only the 4 files from the 6-row plan (omitting `07_hot_night_t1.mp4` sha `30da07fe8860c3640fdb99a4439b858cfbd2460b94510e5e20d23da6b1b728c3` and `01_points_desk_t1.mp4` sha `a9a32aa475424a973ea6e75ad1b9e260897f554723b57e6a5fc3a946980cbf15`); `eight_rows[5]` (`3:13`, `01_points_desk`) `generation_proposal` omits the start-frame reference (`01_points_desk_t1.png`, `sha256: cc16a515a43e881c54a207eb2cb3f700ab9a4166bbb83a366dc09431db403e51`, `takes_max: 3`, `subscription_credit_cap: 300`, `authorized: false`) and the clean-vs-defect frame split (`4511..4606` clean thread vs `4607..4670` paper unroll); and `test_j2163_recipe.py` does not assert single-GOP envelopes (`candidate_boundary_gop_envelope == [kf_in, kf_out - 1]`) or keyframe alignment on `caption_treatment.labels`.
   - **Action Applied:** `J2217` is reopened with the exact 4-item fix list in §3 below, and `J1881` is released to wait on `after: J2217` before authorizing any production splice or bounded retake job.

---

## 2. Verified Master PTS & Closed-GOP Tables (`J2163_MASTER_FRAME_PTS.json`)

### 2.1 Eight Defect Rows (`eight_rows` Required GOP & Candidate Windows)

| Row # | Ben Timestamp & Verbatim Note | `cuts_rough_v12` Cut & Source Plate | Exact Master Closed GOP (`[kf_in, kf_out-1]`) | Exact `candidate_frames` | Master PTS Ticks (`1/12288`) & Seconds | PR #428 (`dfd365c7`) Status |
|---|---|---|---|---|---|---|
| **1** | **00:20** (3 Nov) + **Film-wide** (5 Nov): *"text on screen in readable needs maybe background colour"* / *"Also the bottom text needs a background colour it’s hard to read over a moving video"* | Cut `3` `P1:03_table_three` (`03_table_three_t1.mp4`, sha `482a254d7f7b…`) + **27 `side_label` cuts** | `[423, 544]` (`122f`) | `[427, 544]` (`118f`) | GOP: `218112..280064` (`17.750000–22.791667s`, end `22.833333s`; `20.0s` = frame `477`, PTS `245760`) | Row 1 OK (`[427, 544]`), but `caption_treatment.labels` has wrong `master_frames` on all 27 cuts (**FIX** — see §2.2). |
| **2** | **0:30** (3 Nov): *"flash the next scene"* | Cut `5` `P1:03b_town_safe` (`663..743`) -> Cut `6` `P1:04_storm_mystery` (`04_storm_mystery_t1.mp4`, sha `e1b2de5d8cd4…`) | `[744, 839]` (`96f`; `663..743` unchanged) | `[744, 839]` (`96f`) | `382976..431616` (`31.166667–35.125000s`, end `35.166667s`; `30.0s` = frame `717`, PTS `368640`) | **OK** (`[744, 839]`, single GOP `[744, 839]`). |
| **3** | **0:51 (5 Nov NEW):** *"still have hair flying out the tube, this needs rebuilt"* | Exact `0:51`: Cut `9` `P1:07_hot_night` (`07_hot_night_t1.mp4`, sha `30da07fe8860…`). Hair/tube plate: Cut `23` `P2:02_salon_spark` (ends `1:51.33s`) | **`[1129, 1231]`** (`103f`) | **`[1129, 1231]`** (`103f`) | `580096..632832` (`47.208333–51.500000s`, end `51.541667s`; `51.0s` = frame `1220`, PTS `626688`). `1:51` = frame `2658`, PTS `1363968` (`111.000s`) | **FIX:** `dfd365c7` has `candidate_frames: [1124, 1227]`, pulling `candidate_boundary_gop_envelope` into `[1022, 1231]` (`210f` across `06_heavens` + `07_hot_night`). Must be **`[1129, 1231]`**. |
| **4** | **1:49** (3 Nov): *"strange behaviour as hair flies out the tube"* | Cut `23` `P2:02_salon_spark` (`02_salon_spark_t1.mp4`, sha `4b61312e9416…`) | `[2506, 2665]` (`160f`) | `[2506, 2665]` (`160f`) | `1286144..1367552` (`104.666667–111.291667s`, end `111.333333s`; `1:49` = frame `2610`, PTS `1339392`) | **OK** (`[2506, 2665]`, full rebuild, `02_salon_spark_t1.png` sha `aefd6338aded1037…`, `takes_max: 3`, `cap: 300`, `authorized: false`). |
| **5** | **2:18 (5 Nov)** & **2:20 (3 Nov):** *"the jar flips upside down like magic"* / *"strange behaviour with the silver foil"* | Cut `28` `P2:07_foil_jar` (`07_foil_jar_t1.mp4`, sha `8e28cc24ed74…`) | `[3168, 3343]` (`176f`: keep `3168..3259` `92f`, replace `3260..3343` `84f`) | `[3260, 3343]` (`84f`) | Keep: `1625600..1672192` (`132.291667–136.083333s`). Replace: `1672704..1715200` (`136.125000–139.583333s`, end `139.625000s`). `2:18` = frame `3305`, PTS `1695744` | **OK** (`[3260, 3343]`, `jar_flip_2_18` at frame `3305` outside keep `3168..3259` and inside replace `3260..3343`). |
| **6** | **3:13 (5 Nov NEW):** *"strange behaviour as paper seems to roll out the globe"* | Cut `41` `P3:01_points_desk` (`01_points_desk_t1.mp4`, sha `a9a32aa47542…`) | **`[4511, 4670]`** (`160f`) | **`[4511, 4670]`** (`160f`) | `2315264..2396672` (`188.416667–195.041667s`, end `195.083333s`; `3:13` = frame `4621`, PTS `2371584`) | **FIX:** `dfd365c7` has `candidate_frames: [4500, 4659]`, pulling `candidate_boundary_gop_envelope` into `[4405, 4670]` (`266f` across `18_quill_down` + `01_points_desk`) and leaving frames **`4660..4670`** (paper unrolling from globe) outside `candidate_frames`. Must be **`[4511, 4670]`**, with `01_points_desk_t1.png` (`sha256: cc16a515a43e881c54a207eb2cb3f700ab9a4166bbb83a366dc09431db403e51`) in `generation_proposal`. |
| **7** | **3:31** (3 Nov): *"the diagram/ map is not easy to understand"* | Cut `44` `P3:04_letter_crosses` (`07_slow_news_t1.mp4`, sha `775e6d72eeb9…`) | `[4977, 5077]` (`101f`) | `[4977, 5077]` (`101f`) | `2553856..2606080` (`207.833333–212.083333s`, end `212.125000s`; `3:31` = frame `5053`, PTS `2592768`) | **OK** (`[4977, 5077]`, single animated cream ink letter crossing over `07_slow_news_t1.mp4`, no unsourced `3,600 MILES`). |
| **8** | **7:58 (3 Nov) / 7:59 (5 Nov):** *"the rods fall down for some reason"* / *"the rods on the church’s seem to fall right"* | Cut `100` `P5:13_rods_spread` (`13_rods_spread_t1.mp4`, sha `d9fa5f1329ad…`) | `[11358, 11492]` (`135f`) | `[11358, 11492]` (`135f`) | `5829120..5897728` (`474.375000–479.958333s`, end `480.000000s`; `7:58` = frame `11445`, `7:59` = frame `11469`) | **OK** (`[11358, 11492]`, `clock_7_59` at frame `11469`; add `"subscription_credit_cap": 300` to `generation_proposal`). |

---

### 2.2 Film-Wide Bottom-Caption Inventory (Exact Closed-GOP `master_frames` for All 27 `side_label` Cuts)

In `hos_008_master_v03.mp4` (`J2163_MASTER_FRAME_PTS.json`), every cut starts on a keyframe (`key_frame == 1`) and ends on the frame immediately preceding the next keyframe (Cut `74` `06_same_thing` spans two 80-frame GOPs `8189..8268` and `8269..8348`, so for `cut_idx <= 73` the cut GOP is `gop[cut_idx]`, and for `cut_idx >= 75` the cut GOP is `gop[cut_idx + 1]`). `J2217` must replace the drifted `master_frames` in `caption_treatment.labels` with the exact closed-GOP intervals below:

| # | Cut Idx | Row ID | PR #428 (`dfd365c7`) Drifted `master_frames` | Exact Master Closed GOP `master_frames` (`[kf_in, kf_out-1]`) | Exact `master_frame_count` | Master PTS Range (s) | Bottom Caption (`label`) |
|---|---|---|---|---|---|---|---|
| 1 | `0` | `01_kite_open` | `[0, 139]` (off by -2f) | **`[0, 141]`** | **`142`** | `0.1250–6.0417` | `PHILADELPHIA · 1752` |
| 2 | `2` | `02_tower_tilt` | `[269, 423]` (off by -3/+1f) | **`[272, 422]`** | **`151`** | `11.4583–17.7500` | `THE ANSWER IS ON THE ROOF` |
| 3 | `3` | `03_table_three` | `[423, 541]` (off by -3f) | **`[423, 544]`** | **`122`** | `17.7500–22.8333` | `A KITE · A KEY · A JAR` |
| 4 | `14` | `12_steeple_fire` | `[1609, 1687]` (off by -6f) | **`[1615, 1692]`** | **`78`** | `67.5000–70.7500` | `LIGHTNING` |
| 5 | `15` | `13_ring_the_bells` | `[1687, 1808]` (off by -6/+7f) | **`[1693, 1801]`** | **`109`** | `70.7500–75.2917` | `RING THE BELLS` |
| 6 | `22` | `01_salon_tube` | `[2400, 2499]` (off by -7f) | **`[2407, 2505]`** | **`99`** | `100.5417–104.6667` | `ELECTRICITY · A PARTY TRICK` |
| 7 | `25` | `04_franklin_watches` | `[2710, 2879]` (off by -8f) | **`[2718, 2887]`** | **`170`** | `113.5417–120.6250` | `BENJAMIN FRANKLIN · PHILADELPHIA` |
| 8 | `27` | `06_leyden_jar` | `[3040, 3158]` (off by -9f) | **`[3049, 3167]`** | **`119`** | `127.3333–132.2917` | `THE LEYDEN JAR` |
| 9 | `33` | `12_notebook_list` | `[3667, 3802]` (off by -11f) | **`[3678, 3812]`** | **`135`** | `153.5833–159.2083` | `7 NOVEMBER 1749` |
| 10 | `38` | `17_page_bottom` | `[4201, 4307]` (off by -11f) | **`[4212, 4317]`** | **`106`** | `175.9167–180.3333` | `LET THE EXPERIMENT BE MADE` |
| 11 | `42` | `02_sentry_box` | `[4659, 4820]` (off by -12f) | **`[4671, 4820]`** | **`150`** | `195.0833–201.3333` | `THE SENTRY-BOX` |
| 12 | `45` | `05_marly_garden` | `[5066, 5187]` (off by -12f) | **`[5078, 5200]`** | **`123`** | `212.1250–217.2500` | `MARLY, FRANCE · MAY 1752` |
| 13 | `52` | `11_kite_build` | `[5833, 6006]` (off by -15f) | **`[5848, 6021]`** | **`174`** | `244.2917–251.5417` | `SILK · CEDAR · WIRE` |
| 14 | `58` | `16_keep_silk_dry` | `[6469, 6612]` (off by -14f) | **`[6483, 6627]`** | **`145`** | `270.8750–276.9167` | `KEEP THE SILK DRY` |
| 15 | `60` | `18_william_runs` | `[6757, 6901]` (off by -16f) | **`[6773, 6904]`** | **`132`** | `282.9583–288.4583` | `JUNE 1752` |
| 16 | `68` | `25_fibres_rise` | `[7534, 7635]` (off by -18f) | **`[7552, 7640]`** | **`89`** | `315.5417–319.2500` | `THE THREADS STAND UP` |
| 17 | `70` | `02_knuckle_spark` | `[7730, 7819]` (off by -18f) | **`[7748, 7836]`** | **`89`** | `323.7083–327.4167` | `A SPARK` |
| 18 | `72` | `04_fill_the_jar` | `[7927, 8085]` (off by -19f) | **`[7946, 8103]`** | **`158`** | `331.9583–338.5833` | `LIGHTNING IN A JAR` |
| 19 | `79` | `10_richmann_rod` | `[8829, 8984]` (off by -20f) | **`[8849, 9003]`** | **`155`** | `369.7083–376.1667` | `ST PETERSBURG · 1753` |
| 20 | `82` | `13_gazette_page` | `[9141, 9283]` (off by -20f) | **`[9161, 9302]`** | **`142`** | `382.7500–388.6667` | `PENNSYLVANIA GAZETTE · 19 OCTOBER 1752` |
| 21 | `83` | `14_royal_society` | `[9283, 9410]` (off by -20f) | **`[9303, 9429]`** | **`127`** | `388.6667–393.9583` | `THE ROYAL SOCIETY` |
| 22 | `84` | `15_copley_medal` | `[9410, 9466]` (off by -20f) | **`[9430, 9486]`** | **`57`** | `393.9583–396.3750` | `THE COPLEY MEDAL · 1753` |
| 23 | `87` | `01_house_rod` | `[9789, 9932]` (off by -21f) | **`[9810, 9953]`** | **`144`** | `409.8750–415.8750` | `SEPTEMBER 1752` |
| 24 | `89` | `03_bells_ring` | `[10054, 10170]` (off by -22f) | **`[10076, 10191]`** | **`116`** | `420.9583–425.7917` | `THE BELLS THAT RING` |
| 25 | `91` | `05_almanac_page` | `[10251, 10394]` (off by -22f) | **`[10273, 10415]`** | **`143`** | `429.1667–435.1250` | `POOR RICHARD · 1753` |
| 26 | `94` | `07_giant_spark` | `[10604, 10755]` (off by -22f) | **`[10626, 10776]`** | **`151`** | `443.8750–450.1667` | `HOTTER THAN THE SUN` |
| 27 | `107` | `19_skyline_strike` | `[12275, 12440]` (off by -22f) | **`[12297, 12461]`** | **`165`** | `513.5000–520.3750` | `20+ STRIKES A YEAR` |

---

## 3. Exact Fix List for Reopened `J2217` (On HOS PR #428 `cursor/J2217-eight-item`)

1. **Fix `eight_rows[2]` (`0:51`, `07_hot_night`) and `eight_rows[5]` (`3:13`, `01_points_desk`) `candidate_frames` in `J2163_CORRECTION_MANIFEST.json`, `J2217_AMEND.md`, and `J1868_UAT_CORRECTIONS.md`:**
   - Change `eight_rows[2]["candidate_frames"]` from `[1124, 1227]` to **`[1129, 1231]`** (`103` frames, keyframe `1129` at PTS `580096` = `47.208333s` through frame `1231` at PTS `632832` = `51.500000s`, end `633344` = `51.541667s`) so `candidate_boundary_gop_envelope` is `[1129, 1231]` (`103` frames, single cut GOP) instead of `[1022, 1231]`. Also record `clock_1_51_frame: 2658` (`pts: 1363968`, `111.000s`) in `hair_tube_source`.
   - Change `eight_rows[5]["candidate_frames"]` from `[4500, 4659]` to **`[4511, 4670]`** (`160` frames, keyframe `4511` at PTS `2315264` = `188.416667s` through frame `4670` at PTS `2396672` = `195.041667s`, end `2397184` = `195.083333s`) so `candidate_boundary_gop_envelope` is `[4511, 4670]` (`160` frames, single cut GOP) instead of `[4405, 4670]`, covering all `160` frames of `01_points_desk` including `4660..4670`.
   - In `eight_rows[5]["recipe"]`, record the clean-vs-defect split (`4511..4606` = `96` frames clean linen indicator thread vs `4607..4670` = `64` frames paper-strip unroll) and populate `generation_proposal` with `"route": "Flow Veo3.1 Quality"`, `"reference": "/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/part03/refs/v03_flow_stills/01_points_desk_t1.png"`, `"reference_sha256": "cc16a515a43e881c54a207eb2cb3f700ab9a4166bbb83a366dc09431db403e51"`, `"takes_max": 3`, `"subscription_credit_cap": 300`, `"authorized": false`. Also add `"subscription_credit_cap": 300` to `eight_rows[7]["recipe"]["generation_proposal"]` (`7:58`, `13_rods_spread`).

2. **Fix all 27 `master_frames` and `master_frame_count` entries in `caption_treatment.labels` in `J2163_CORRECTION_MANIFEST.json`:**
   - Replace the nominal-float-derived `master_frames` (`[0, 139]`..`[12275, 12440]`) with the exact closed-GOP `[kf_in, kf_out - 1]` intervals from Table 2.2 above (`[0, 141]`..`[12297, 12461]`). Every entry's `master_frames[0]` must have `key_frame == 1` in `J2163_MASTER_FRAME_PTS.json`, and `master_frames[1] + 1` must either equal `12923` or have `key_frame == 1`.

3. **Extend `required_inputs` in `J2163_CORRECTION_MANIFEST.json`:**
   - Add `/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/part01/raw/v01/07_hot_night_t1.mp4` (`sha256: 30da07fe8860c3640fdb99a4439b858cfbd2460b94510e5e20d23da6b1b728c3`, `minimum_frames: 103`) and `/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/part03/raw/v01/01_points_desk_t1.mp4` (`sha256: a9a32aa475424a973ea6e75ad1b9e260897f554723b57e6a5fc3a946980cbf15`, `minimum_frames: 160`).

4. **Strengthen `test_j2163_recipe.py` and re-run `J2217_TESTS.txt`:**
   - Update `test_eight_item_amend_stays_unresolved_and_unbordered` to assert `[[427, 544], [744, 839], [1129, 1231], [2506, 2665], [3260, 3343], [4511, 4670], [4977, 5077], [11358, 11492]]`.
   - In `test_clocks_map_on_stored_master_pts`, assert that for every patch in `build_plan(timeline, d['eight_rows'])`, `p['candidate_boundary_gop_envelope']` spans exactly one closed GOP (`[423, 544]`, `[744, 839]`, `[1129, 1231]`, `[2506, 2665]`, `[3168, 3343]`, `[4511, 4670]`, `[4977, 5077]`, `[11358, 11492]`), and assert that for all 27 entries in `d['caption_treatment']['labels']`, `frames[lo]['key_frame'] == 1` and `(hi + 1 == len(frames) or frames[hi + 1]['key_frame'] == 1)`.
   - Keep execution refused (`returncode 2`), all notes unresolved, no render/spend/upload/YouTube change, `GBP0`.
