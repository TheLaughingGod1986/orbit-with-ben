# J1881 — Rule H Review: HOS 008 Franklin Eight-Item Correction Recipe (+ Film-Wide Captions)

- **Job:** `J1881` (`review Franklin eight-item correction recipe (+ film-wide captions) and scope production`)
- **Reviewer:** `gemini` (review lane)
- **Date:** 2026-11-05T13:11Z
- **Reviewed Deliverables & Evidence:**
  - `J2163` deliverable: HOS PR #411 (`codex/J2163-repair`, commit `50620e408667c6ec0c8a959acd051fcfa458fd8d`)
  - Ben 5 Nov second `v03` review: HOS PR #180 comment `6658371896`, Claude advisory `6658387533`, Chief fold-in commit `4e94001e37fb63b59a1879fd1953854bfbe951d4` (`02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/J1868_BEN_NOTES_2026-11-05.md` and `J1868_UAT_CORRECTIONS.md`)
  - Prior review record: `02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/J1881_SCOPE_REVIEW.md` (PR #410, `712e2abf`)
- **Verdict:** **FIX (Hold production splice/generation for `J2217` eight-item + film-wide caption amendment; KEEP `J2163` PR #411 `50620e40` base PTS/planner architecture)**

---

## 1. Executive Decision

1. **Base Planner & PTS Repair (`J2163` / HOS PR #411 `50620e40`) — KEEP as Foundation:**
   - `J2163` resolved all five engineering and house-style blocking findings identified in the 4 Nov `J1881` review of PR #409 (`bd530249`):
     - **Master PTS & non-uniform gap preservation:** `J2163_MASTER_FRAME_PTS.json` records all `12,923` decoded frames of verified master `cf1561c218bace7bc14ed3d625b0790a457027a90f392262f45ca7172723099b` (`393,139,693` bytes, timebase `1/12288`, start `1536` ticks = `0.125s`, end `6630912` ticks = `539.625s`, duration `539.500s`, `113` keyframes, `23` steps of `1024` ticks and `1` step of `1536` ticks).
     - **Unsafe renderer removed:** `_build_rough_v13_recipe.py` removes global `setpts=N/(24*TB)` CFR re-encoding, lossy unchanged-range extraction, frame-repeat/blank fallbacks, and silent Option A substitutions; it is a strict read-only planner that refuses execution (`returncode 2`).
     - **Truthful dry-run & input hash checks:** `J2163_DRY_RUN.json` verifies SHA256 and decoded frame counts for the four native candidate inputs (`03_table_three_t1.mp4`, `04_storm_mystery_t1.mp4`, `07_slow_news_t1.mp4`, `11_jar_crack_t1.mp4`) and reports output sync/frame delta as `UNMEASURED`.
     - **Unit test suite:** `python3 -m unittest -v test_j2163_recipe.py` ran cleanly in this review (`Ran 11 tests in 0.035s — OK`).

2. **Overall Recipe Scope (`50620e40` vs Ben 5 Nov Second Review `6658371896`) — FIX via `J2217`:**
   - Because `J2163` (`50620e40`) was completed at `00:02Z` prior to Ben's 5 Nov `12:47Z` second `v03` review (`6658371896`), `J2163_CORRECTION_MANIFEST.json` contains only the original **six rows** (`six_rows`) and treats `00:20` caption contrast as a single-cut change with `"no border or pill"`.
   - Per Ben's 5 Nov review (`6658371896`), Claude advisory (`6658387533`), and Chief's scope fold (`4e94001e` / `J2217`), the required scope before any splice or generation is now **eight defect items + film-wide bottom-caption background panels**.
   - **No production splice, replacement render, or Flow generation may be authorized from the six-only manifest.** `J1881` therefore records the exact technical specification below for `J2217` and waits on `after: J2217` (`step 3 of 4`).

---

## 2. Tool & Evidence Verification (`J2163` + `J1868_BEN_NOTES_2026-11-05.md`)

### 2.1 Master PTS & Keyframe Verification (`J2163_MASTER_FRAME_PTS.json` vs `cuts_rough_v12.json`)

Cross-referencing `J2163_MASTER_FRAME_PTS.json` (`12,923` frames, `113` keyframes, `time_base = 1/12288`) against `_desk/008/rough_v12/cuts_rough_v12.json` (`112` cuts) and the extracted 5 Nov stills (`~/_desk/008/ben_notes_2026-11-05/`) + UAT contact sheets confirms the exact frame and PTS mapping for all eight defect items:

| Item | Ben Timestamp & Verbatim Note | `cuts_rough_v12` Cut & Source Plate | Master Frame Window (GOP `kf_in..kf_out-1`) | Master PTS Ticks (`1/12288`) & Seconds | Verification Findings & Required `J2217` Disposition |
|---|---|---|---|---|---|
| **1** | **00:20** (3 Nov) + **Film-wide** (5 Nov): *"text on screen in readable needs maybe background colour"* / *"Also the bottom text needs a background colour it’s hard to read over a moving video"* | Cut `3` `P1:03_table_three` (`03_table_three_t1.mp4`, sha `482a254d7f7b…`) **+ all 27 `side_label` cuts film-wide** (see §2.2) | Cut `3` GOP: `423..544` (candidate `427..544`). Film-wide: **27 cuts** across Parts 1–5 | Cut `3` GOP: `218112..280064` (`17.750000–22.833333s`; `20.0s` = frame `477`, PTS `245760`) | Still `t0m20_caption.jpg` confirms `A KITE · A KEY · A JAR` at `y=940` has only a 4px shadow stroke over the key/wood grain. Amend `J2163` manifest: replace `"no border or pill"` on Note 1 with a **film-wide soft cream/umber background panel** behind white Didot italic on all 27 bottom `side_label` cuts over moving footage (no bordered UI chrome). |
| **2** | **0:30** (3 Nov): *"flash the next scene"* | Cut `5` `P1:03b_town_safe` (`663..743`) -> Cut `6` `P1:04_storm_mystery` (`744..839`, `04_storm_mystery_t1.mp4`, sha `e1b2de5d8cd4…`) | Unchanged: `663..743`; Candidate: `744..839` | `382976..431616` (`31.166667–35.166667s`; `30.0s` = frame `717`, PTS `368640`) | Retain `J2163` row 2 (`744..839` candidate, `663..743` untouched). Reconcile master-derived word alignment before boundary cut. |
| **3** | **0:51 (5 Nov NEW):** *"still have hair flying out the tube, this needs rebuilt"* | Exact `0:51`: Cut `9` `P1:07_hot_night` (`07_hot_night_t1.mp4`, sha `30da07fe8860…`) -> Cut `10` `P1:08_sky_flash`. Hair/tube plate: Cut `23` `P2:02_salon_spark` (ends at `1:51.33s`) | At `0:51`: GOP `1129..1231` (`103` frames). At `1:51`: GOP `2506..2665` (`160` frames) | `0:51` GOP: `580096..632832` (`47.208333–51.541667s`; `51.0s` = frame `1220`, PTS `626688`). `1:51` = frame `2658`, PTS `1363968` (`111.000000s`) | Still `t0m51_hair.jpg` (`51.0s`, frame `1220`) shows Part 1 hot-night street (no glass tube). Meanwhile `P2:02_salon_spark` spans `104.666667–111.333333s` (`1:44.67–1:51.33`), and `ctx_150_salon.jpg` (`1:50`–`1:51`, frames `2634..2658`) shows the detached white hair plume floating from the tube. **Keep `0:51` as a dedicated row in the 8-item manifest with Ben's verbatim wording**, mapping both `P1:07_hot_night` (`1129..1231`) and the `1:51` (`111.0s`, frame `2658`) end of `P2:02_salon_spark` (`2506..2665`), and enforcing **full rebuild (not trim)** of the hair/tube shot. |
| **4** | **1:49** (3 Nov): *"strange behaviour as hair flies out the tube"* | Cut `23` `P2:02_salon_spark` (`02_salon_spark_t1.mp4`, sha `4b61312e9416…`); adjacent Cut `22` `P2:01_salon_tube` (`2407..2505`) | GOP `2506..2665` (`160` frames; adjacent `2666..2717` unchanged) | `1286144..1367552` (`104.666667–111.333333s`; `1:49` = frame `2610`, PTS `1339392`) | Contact sheet `02_salon_spark_t1_sheet.jpg` confirms hair/smoke extrudes from the glass tube from panel 2 through panel 5 (`1:46–1:51`), while `01_salon_tube_t1_sheet.jpg` (`2407..2505`) is clean silk-rubbing on glass. Exact-match replacement asset missing; carry bounded Flow Veo 3.1 Quality retake proposal (`02_salon_spark_t1.png`, sha `aefd6338aded1037…`, max 3 takes, cap 300 credits, `authorized: false`). |
| **5 & 6** | **2:18 (5 Nov)** & **2:20 (3 Nov):** *"the jar flips upside down like magic"* / *"strange behaviour with the silver foil"* | Cut `28` `P2:07_foil_jar` (`07_foil_jar_t1.mp4`, sha `8e28cc24ed74…`); followed by Cut `29` `P2:08_jar_spark` (`3344..3404`) | Full GOP `3168..3343` (`176` frames): Keep `3168..3259` (`92` frames); Replace `3260..3343` (`84` frames) | Keep: `1625600..1672192` (`132.291667–136.083333s`, `2:12.29–2:16.08`). Replace: `1672704..1715200` (`136.125000–139.625000s`). **`2:18` (`138.0s`) = frame `3305`, PTS `1695744`** | **Verified:** `2:18` (`138.0s`, frame `3305`) is **38 frames (1.875s) OUTSIDE kept window `3168..3259`** and squarely **INSIDE replace window `3260..3343`**. Contact sheet `07_foil_jar_t1_sheet.jpg` and stills `ctx_216_jar.jpg` vs `t2m18_jar.jpg`/`ctx_2185_jar.jpg` confirm frames `0..91` (`3168..3259`) show the upright glass rim before the foil/jar inversion in `3260..3343`. Record `2:18` verbatim in the manifest alongside `2:20` with this frame-level proof. |
| **7** | **3:13 (5 Nov NEW):** *"strange behaviour as paper seems to roll out the globe"* | Cut `41` `P3:01_points_desk` (`01_points_desk_t1.mp4`, sha `a9a32aa475424a97…`) | GOP `4511..4670` (`160` frames; followed by Cut `42` `P3:02_sentry_box` at keyframe `4671`) | `2315264..2396672` (`188.416667–195.083333s`; **`3:13` (`193.0s`) = frame `4621`, PTS `2371584`**; `3:15` = frame `4669`, PTS `2396160`) | **New defect row not in PR #411.** Still `t3m13_paper_globe.jpg`, `ctx_315.jpg`, and contact sheet `01_points_desk_t1_sheet.jpg` confirm that while panels 1–4 (`~0.0–4.0s`, master frames `4511..~4606`, `188.42–192.38s`) show a thin linen indicator thread hanging from the brass sphere, in panels 5–6 (`~192.4–195.08s`, frames `~4607..4670`) the thread morphs into a wide marked paper strip unrolling out of the globe. `J2217` must add this row (`4511..4670`), verify exact clean frame cutoff vs native Part 3 bench coverage or bounded Flow Veo 3.1 retake proposal from `01_points_desk_t1.png` (`sha256: cc16a515a43e881c…`, max 3 takes, `authorized: false`). |
| **8** | **3:31** (3 Nov): *"the diagram/ map is not easy to understand"* | Cut `44` `P3:04_letter_crosses` (overlay over `07_slow_news_t1.mp4`, sha `775e6d72eeb9…`) | GOP `4977..5077` (`101` frames) | `2553856..2606080` (`207.833333–212.125000s`; `3:31` = frame `5053`, PTS `2592768`) | Retain `J2163` row 5 (`4977..5077`): single clear animated cream ink letter crossing over moving `07_slow_news_t1.mp4` (`4.291667s` actual duration), no bordered UI banner, no unsourced `3,600 MILES` claim. |
| **9** | **7:58 (3 Nov) / 7:59 (5 Nov):** *"the rods fall down for some reason"* / *"the rods on the church’s seem to fall right"* | Cut `100` `P5:13_rods_spread` (`13_rods_spread_t1.mp4`, sha `d9fa5f1329ad…`) | GOP `11358..11492` (`135` frames) | `5829120..5897728` (`474.375000–480.000000s`; `7:58` = frame `11445`, PTS `5873664`; **`7:59` = frame `11469`, PTS `5885952`**) | Still `t7m59_rods.jpg` (`479.0s`, frame `11469`) sits inside `11358..11492` (`P5:13_rods_spread`) and shows the church steeple and house lightning rods tilted/falling right. Retain `J2163` row 6 (`11358..11492`) with both `7:58` and `7:59` verbatim notes recorded; exact church/house/ship-mast asset missing, bounded Flow Veo 3.1 retake proposal (`13_rods_spread_t1.png`, sha `84a92bf6ce1abd1a…`, max 3 takes, `authorized: false`). |

---

### 2.2 Film-Wide Bottom-Caption Inventory (`cuts_rough_v12.json` `side_label` Cuts)

Inspection of `_assemble_rough_v02.py` (`draw_side_label`, line 156) and `_desk/008/rough_v12/cuts_rough_v12.json` confirms that **27 cuts** across Parts 1–5 render bottom-centre Didot italic captions (`y = 940`) directly over moving plates with no background panel:

| # | Cut Idx | Part & Row ID | Master GOP Frames (`kf_in..kf_out-1`) | Master PTS Range (s) | Bottom Caption (`side_label`) | Source Plate |
|---|---|---|---|---|---|---|
| 1 | `0` | `P1:01_kite_open` | `0..141` | `0.1250–6.0417` | `PHILADELPHIA · 1752` | `01_kite_open_t1.mp4` |
| 2 | `2` | `P1:02_tower_tilt` | `272..422` | `11.4583–17.7500` | `THE ANSWER IS ON THE ROOF` | `02_tower_tilt_t1.mp4` |
| 3 | `3` | `P1:03_table_three` | `423..544` | `17.7500–22.8333` | `A KITE · A KEY · A JAR` | `03_table_three_t1.mp4` |
| 4 | `14` | `P1:12_steeple_fire` | `1615..1692` | `67.5000–70.7500` | `LIGHTNING` | `12_steeple_fire_t1.mp4` |
| 5 | `15` | `P1:13_ring_the_bells` | `1693..1801` | `70.7500–75.2917` | `RING THE BELLS` | `13_ring_the_bells_t1.mp4` |
| 6 | `22` | `P2:01_salon_tube` | `2407..2505` | `100.5417–104.6667` | `ELECTRICITY · A PARTY TRICK` | `01_salon_tube_t1.mp4` |
| 7 | `25` | `P2:04_franklin_watches` | `2718..2887` | `113.5417–120.6250` | `BENJAMIN FRANKLIN · PHILADELPHIA` | `04_franklin_watches_t1.mp4` |
| 8 | `27` | `P2:06_leyden_jar` | `3049..3167` | `127.3333–132.2917` | `THE LEYDEN JAR` | `06_leyden_jar_t1.mp4` |
| 9 | `33` | `P2:12_notebook_list` | `3678..3812` | `153.5833–159.2083` | `7 NOVEMBER 1749` | `12_notebook_list_t1.mp4` |
| 10 | `38` | `P2:17_page_bottom` | `4212..4317` | `175.9167–180.3333` | `LET THE EXPERIMENT BE MADE` | `17_page_bottom_t1.mp4` |
| 11 | `42` | `P3:02_sentry_box` | `4671..4820` | `195.0833–201.3333` | `THE SENTRY-BOX` | `02_sentry_box_t1.mp4` |
| 12 | `45` | `P3:05_marly_garden` | `5078..5200` | `212.1250–217.2500` | `MARLY, FRANCE · MAY 1752` | `05_marly_garden_t1.mp4` |
| 13 | `52` | `P3:11_kite_build` | `5848..6021` | `244.2917–251.5417` | `SILK · CEDAR · WIRE` | `11_kite_build_t1.mp4` |
| 14 | `58` | `P3:16_keep_silk_dry` | `6483..6627` | `270.8750–276.9167` | `KEEP THE SILK DRY` | `16_keep_silk_dry_t1.mp4` |
| 15 | `60` | `P3:18_william_runs` | `6773..6904` | `282.9583–288.4583` | `JUNE 1752` | `18_william_runs_t1.mp4` |
| 16 | `68` | `P3:25_fibres_rise` | `7552..7640` | `315.5417–319.2500` | `THE THREADS STAND UP` | `25_fibres_rise_t1.mp4` |
| 17 | `70` | `P4:02_knuckle_spark` | `7748..7836` | `323.7083–327.4167` | `A SPARK` | `02_knuckle_spark_t1.mp4` |
| 18 | `72` | `P4:04_fill_the_jar` | `7946..8103` | `331.9583–338.5833` | `LIGHTNING IN A JAR` | `04_fill_the_jar_t1.mp4` |
| 19 | `79` | `P4:10_richmann_rod` | `8849..9003` | `369.7083–376.1667` | `ST PETERSBURG · 1753` | `10_richmann_rod_t1.mp4` |
| 20 | `82` | `P4:13_gazette_page` | `9161..9302` | `382.7500–388.6667` | `PENNSYLVANIA GAZETTE · 19 OCTOBER 1752` | `13_gazette_page_t1.mp4` |
| 21 | `83` | `P4:14_royal_society` | `9303..9429` | `388.6667–393.9583` | `THE ROYAL SOCIETY` | `14_royal_society_t1.mp4` |
| 22 | `84` | `P4:15_copley_medal` | `9430..9486` | `393.9583–396.3750` | `THE COPLEY MEDAL · 1753` | `15_copley_medal_t1.mp4` |
| 23 | `87` | `P5:01_house_rod` | `9810..9953` | `409.8750–415.8750` | `SEPTEMBER 1752` | `01_house_rod_t1.mp4` |
| 24 | `89` | `P5:03_bells_ring` | `10076..10191` | `420.9583–425.7917` | `THE BELLS THAT RING` | `03_bells_ring_t1.mp4` |
| 25 | `91` | `P5:05_almanac_page` | `10273..10415` | `429.1667–435.1250` | `POOR RICHARD · 1753` | `05_almanac_page_t1.mp4` |
| 26 | `94` | `P5:07_giant_spark` | `10626..10776` | `443.8750–450.1667` | `HOTTER THAN THE SUN` | `07_giant_spark_t1.mp4` |
| 27 | `107` | `P5:19_skyline_strike` | `12297..12461` | `513.5000–520.3750` | `20+ STRIKES A YEAR` | `19_skyline_strike_t1.mp4` |

*(Note: Three additional `side_label` entries in `parts/part-04_plates_v03.json` and `part-05_plates_v03.json` — `P4:06_same_thing`, `P4:08_teach_charge`, and `P5:11_safe_path` — are rendered as period-paper code graphics rather than `draw_side_label` over moving plates, so `cuts_rough_v12.json` records `side_label: null` on those three cuts. `J2217` must include all 27 moving-footage `side_label` cuts above in the film-wide caption background plan.)*

---

## 3. Exact Fix List for `J2217` (Required Before `J1881` Authorizes Production Scope)

`J2217` (`HOS 008: amend Franklin recipe to eight-item + film-wide captions (Ben 5 Nov)`) must deliver the following in a clean HOS worktree/PR on top of `50620e40` + `4e94001e`:

1. **Extend `J2163_CORRECTION_MANIFEST.json` and `_build_rough_v13_recipe.py` from six rows to eight defect rows + film-wide caption plan:**
   - **Row 1 (`00:20` + Film-Wide Bottom Captions):** Update Note 1 (`00:20`, `P1:03_table_three`, `423..544`) and add a `film_wide_bottom_captions` manifest section listing all **27 `side_label` cuts** (Table 2.2 above) with their exact GOP frame windows (`kf_in..kf_out-1`), master PTS intervals, source paths/SHA256s, and soft warm-umber/cream background panel specification (no bordered UI chrome, `<= 4` words per sequential label where required, animated fade-in/out `0.3–0.5s`, hold `<= 4s`, phone readability check).
   - **Row 2 (`0:30` flash next scene):** Keep `744..839` (`31.166667–35.166667s`) candidate window (`663..743` untouched).
   - **Row 3 (`0:51` NEW — `"still have hair flying out the tube, this needs rebuilt"`):** Add dedicated row preserving Ben's verbatim `0:51` wording. Record exact `0:51` master mapping (`P1:07_hot_night`, GOP `1129..1231`, PTS `580096..632832` = `47.208333–51.541667s`, `07_hot_night_t1.mp4` sha `30da07fe8860c36451632227b698a0929a2ebad34c912cf6a7ca5f8ea1df329c`, no glass tube in frame) alongside the `1:51` (`111.000000s`, frame `2658`, PTS `1363968`) tail of `P2:02_salon_spark` (`2506..2665`, `104.666667–111.333333s`), and specify **rebuild (not trim)** of the hair/tube shot.
   - **Row 4 (`1:49` — `"strange behaviour as hair flies out the tube"`):** Keep `P2:02_salon_spark` (`2506..2665`, `104.666667–111.333333s`, `160` frames) linked to Row 3's rebuild requirement (`02_salon_spark_t1.png`, sha `aefd6338aded1037c11306a99fc580d1a62a66d9367409f01e0edd993cc8cc58`, Flow Veo 3.1 Quality, max 3 takes, cap 300 credits, `authorized: false`).
   - **Row 5 (`2:18` & `2:20` — `"the jar flips upside down like magic"` / `"strange behaviour with the silver foil"`):** Record both `2:18` and `2:20` verbatim on `P2:07_foil_jar` (GOP `3168..3343`). Document frame-level proof that `2:18` (`138.000000s`, frame `3305`, PTS `1695744`) is outside kept frames `3168..3259` (`132.291667–136.083333s`) and inside replace frames `3260..3343` (`136.125000–139.625000s`, replaced by `11_jar_crack_t1.mp4` `4.000–7.500s`, sha `7629a5dfdc5b649535c9816ece5bf0acf250a13133bf294bf43cfb1f21588270`), and verify frame `3259` (source frame `91`) precedes the start of the jar tilt/inversion.
   - **Row 6 (`3:13` NEW — `"strange behaviour as paper seems to roll out the globe"`):** Add new row for Cut `41` `P3:01_points_desk` (GOP `4511..4670`, `160` frames, PTS `2315264..2396672` = `188.416667–195.083333s`; `3:13` = frame `4621`, PTS `2371584`, `01_points_desk_t1.mp4` sha `a9a32aa475424a97…`). Determine the exact frame in `01_points_desk_t1.mp4` where the linen indicator thread morphs into the wide paper strip (`~frame 96` / master frame `~4607`) and document whether an approved native Part 2/Part 3 bench clip can cover the tail under `picture_qa` repeat rules or whether `P3:01_points_desk` (`4511..4670`) requires a bounded Flow Veo 3.1 retake proposal from `01_points_desk_t1.png` (`sha256: cc16a515a43e881c…`, max 3 takes, `authorized: false`).
   - **Row 7 (`3:31` — `"the diagram/ map is not easy to understand"`):** Keep `P3:04_letter_crosses` (`4977..5077`, `207.833333–212.125000s`, `101` frames, single animated cream ink letter crossing over `07_slow_news_t1.mp4`, no unsourced `3,600 MILES` claim).
   - **Row 8 (`7:58` & `7:59` — `"the rods fall down for some reason"` / `"the rods on the church’s seem to fall right"`):** Record both `7:58` (frame `11445`, PTS `5873664`) and `7:59` (frame `11469`, PTS `5885952`) verbatim on `P5:13_rods_spread` (GOP `11358..11492`, `474.375000–480.000000s`, `135` frames), retaining the bounded Flow Veo 3.1 retake proposal (`13_rods_spread_t1.png`, sha `84a92bf6ce1abd1a5780c37ac2e8ae50ea6099f5cff5c7f728a70060b394819c`, max 3 takes, `authorized: false`).
2. **Update dry-run & unit tests (`test_j2163_recipe.py` / `J2163_DRY_RUN.json`):**
   - Extend unit tests to assert all **eight defect rows** + the **27-cut film-wide caption table**, non-overlapping GOP windows, `2:18` (`frame 3305`) outside kept `3168..3259`, and unconditional execution refusal (`returncode 2`).
3. **Preserve all locks and safety boundaries:**
   - Keep planner strictly read-only (`authorized: false`, no splice, no replacement render, no Flow spend, no R2/YouTube/schedule changes).
   - Do not merge PR #411 or #180; do not mark any Ben note resolved; preserve `J1297`, `h22`, `h35`, and `J1755` publication rejection. `GBP0`.
