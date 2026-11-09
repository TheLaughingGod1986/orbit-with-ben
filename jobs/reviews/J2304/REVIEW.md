# J2304 — Film 032 Row 23 (`r23_landing_record`) Qualitative Landing-Record Still, Alternative & `PIA14909` Allocation Review

- **Job:** `J2304` (`032 R23: review qualitative landing record and second PIA14909 allocation`)
- **Parent Job:** `J2089` (`032 picture: £0 harvest + code_graphics builds from SHOT_LIST_v02 (WIP film)`, `1/4`)
- **Film:** `OWB:032` (`02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan`)
- **Reviewer:** `gemini` (`gemini-argon`, specialist worker; still-image visual review + source/allocation/shot-list audit — not Chief final `OK`, not moving-video or audio perception, not composite or film-stage `PASS`)
- **Reviewed Worktree & Commit:** `/private/tmp/codex-J2089` (`worker/J2089-r18-ruler` at local commit `510197ffe4ad1e3d8f12568c5143f551de557187`, inherited automatic-review public-push rejection respected)
- **Reviewed Artefacts:**
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/J2089_R23_REVIEW_REQUEST_v01.md`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/J2089_CHECKPOINT_v21.md`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/LANDING_RECORD_MANIFEST_v01.json`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/LANDING_RECORD_CHECKS_v01.json`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/LANDING_RECORD_SOURCE_v01.json`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/landing_record_graphic.py`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/verify_landing_record_graphic.py`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/SHOT_LIST_v05.md` (`8ff3ddc7d6`)
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/HARVEST_POOL_v01.json` (`0f8491731f`)
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/01_Script/SOURCES.md` (governing v01 Rows 7 & 8)
  - `/Users/benjaminoats/_desk/cache/J2089/landing_record_previews_v02/r23_landing_record_review.jpg` (`1920×1080` RGB over `(37, 52, 73)` preview backdrop, `135,686` bytes, SHA-256 `a7c0ad89bfe9d0b9d84c20a7571af14f877ebda4ee1173cce04ad878d6aa120a`, inspected full size)
  - `/Users/benjaminoats/_desk/cache/J2089/landing_record_previews_v02/code_graphic_032_r23_landing_record_v01.png` (`1920×1080` RGBA at `t = 2.4 s`, `124,892` bytes, `preview_sha256: 8a2de4177dff150ecb24e70d2e64422241f729fde5537ca5deedb540a51a9d2c`, inspected full size)
  - `/Users/benjaminoats/_desk/cache/J2089/harvest_v01/PIA14909.jpg` (`993×1017` RGB, `37,000` bytes, `source_sha256: b72f5371622b0197f91a70a62b729e1e854dd91c511639f8055cf3d93f70ce74`, inspected full size)
  - `/Users/benjaminoats/_desk/cache/J2089/landing_record_previews_v02/nasa_huygens_2026-11-06.html` (SHA-256 `656df709dfb4e6fc594d27fc4a09c5b0f7a219bb6dea0b7c9f86b821f06a3d8d`)

---

## 1. Verdict Summary

| Check Item | Ruling | Summary |
|---|---|---|
| **1. `r23_landing_record` Still (`code_graphic_032_r23_landing_record_v01.png`, SHA-256 `8a2de4177dff150ecb24e70d2e64422241f729fde5537ca5deedb540a51a9d2c`)** | **`KEEP` / `APPROVED` to Export Under `--render --approved r23_landing_record --review-ref J2304`** | Clean full-size (`1920×1080`) layout: native `1.0×` circular Cassini Titan crop (`408×408` px from `PIA14909.jpg` at `(1290, 350)` with zero ring bleed), animated horizontal `GOLD` connector arrow (`x = 200 → 1180`, `y = 560`), and `≤ 4`-word house labels (`MOST DISTANT LANDING`, `HUYGENS`, `FROM EARTH`, `TITAN`, `NOT TO SCALE`, plus `NASA/JPL-Caltech/Space Science Institute` credit) sitting completely clear of the Titan globe and strictly inside the 5% safe area `(159, 154, 1698, 975)`. Approved to export `code_graphic_032_r23_landing_record_v01.mov` (`1920×1080`, `30 fps`, `108` frames, `3.6 s`, `qtrle` RGBA, `-an`) under `--render --approved r23_landing_record --review-ref J2304`. |
| **2. Qualitative Landing-Record Alternative (`r23_landing_record` Replacing Quantitative `landings_chart`)** | **`KEEP` / `APPROVED`** | The locked Row 23 VO (`229.78–233.24 s`: *"It is still the most distant landing humanity has ever made"*) states only the qualitative record, and `01_Script/SOURCES.md` v01 Row 7 (`https://science.nasa.gov/mission/cassini-huygens/`, *Firsts*: *"the most distant landing from Earth"*) provides no numerical Moon/Venus/Mars landing distances. Row 8's `9.5 AU` is Saturn/Titan's **heliocentric** distance from the Sun (already shown in Row 19's `r19_distance`), so labelling `9.5 AU` as Earth-to-Titan landing distance on a Moon/Venus/Mars bar chart would be factually misleading. The qualitative `FROM EARTH → TITAN` (`NOT TO SCALE`) record graphic is approved in place of `landings_chart`. |
| **3. `PIA14909` Film-Wide Allocation (`R19 + R23` Only; `MAX_REUSE = 2`) & Row 23 Shot-List Amendment** | **`KEEP` / `APPROVED` — Capped at `R19` (Use 1 of 2) and `R23` (Use 2 of 2) Only (`0` Uses in Any Other Row)** | Confirmed across all 52 rows of `SHOT_LIST_v05.md`, `J2090` (`R03` → `PIA21902`, `R44` → `PIA17163`), `J2260` (`R19` → `PIA14909` Use 1/2), and all 61 rendered manifests: `PIA14909` appears only in **Row 19 (`184.60–197.20 s`, Use 1 of 2)** and **Row 23 (`229.78–239.50 s`, Use 2 of 2, separated by `32.58 s > 10 s`)**. In Row 23, `r23_landing_record` (`MOST DISTANT LANDING`) supersedes both `landings_chart` and the duplicate text-only `r23_fact` card (`code_graphic_032_r23_fact_v01.mov` stays preserved on disk in `J2089_EXPORT_HASHES_v20.json` but is not composited a second time in Row 23), and real moving imagery (`PIA08733` Use 2 of 2) must separate Row 22's `surface_72m` from Row 23's graphic so full-frame code graphics never run back-to-back. |

---

## 2. Detailed Evaluation of Required Check Items

### A. Qualitative Landing-Record Alternative vs Quantitative `landings_chart` (`KEEP`)
1. **Exact Match to Locked Row 23 VO (`229.78–239.50 s`, `9.72 s`) and `01_Script/SOURCES.md` v01 Row 7:**
   - **Word-by-Word Locked Row 23 VO (`stt/titan_landing_vo_v02b/stt_raw.json`):**
     - `229.78–233.24 s` (`3.46 s`): *"It (`229.78–229.84 s`) is (`229.88–229.98 s`) still (`230.08–230.32 s`) the (`230.36–230.44 s`) most (`230.48–230.72 s`) distant (`230.76–231.16 s`) landing (`231.22–231.66 s`) humanity (`231.74–232.30 s`) has (`232.32–232.52 s`) ever (`232.60–232.80 s`) made (`232.86–233.24 s`)."*
     - `233.96–239.50 s` (`5.54 s`): *"Yet (`233.96–234.10 s`) if (`234.16–234.24 s`) you (`234.28–234.38 s`) stepped (`234.48–234.74 s`) out (`234.82–234.96 s`) beside (`234.98–235.42 s`) it (`235.48–235.60 s`) in (`235.64–235.70 s`) a (`235.76–235.80 s`) heated (`235.84–236.16 s`) suit (`236.28–236.66 s`), what (`237.22–237.34 s`) would (`237.36–237.46 s`) you (`237.50–237.62 s`) feel (`237.70–237.98 s`) when (`238.00–238.14 s`) the (`238.18–238.26 s`) rain (`238.30–238.62 s`) began (`238.64–238.96 s`) to (`239.02–239.14 s`) fall (`239.18–239.50 s`)?"*
   - **Governing `01_Script/SOURCES.md` v01 Row 7 & `LANDING_RECORD_SOURCE_v01.json`:**
     - `SOURCES.md` v01 Row 7 claim: *"14 Jan 2005, after a seven-year journey aboard Cassini; 2 h 27 min descent (graphic: 147 minutes); lands softly on what looks like a dry riverbed; 72 minutes from the surface until Cassini sinks below the horizon; the most distant landing ever made."*
     - Verbatim NASA source quote (`https://science.nasa.gov/mission/cassini-huygens/`, *Firsts* section, saved at `/Users/benjaminoats/_desk/cache/J2089/landing_record_previews_v02/nasa_huygens_2026-11-06.html`, SHA-256 `656df709dfb4e6fc594d27fc4a09c5b0f7a219bb6dea0b7c9f86b821f06a3d8d`):
       *"Huygens' landing was the first by a spacecraft in the outer solar system, and the most distant landing from Earth."*
2. **Why `SHOT_LIST_v05.md`'s Quantitative `landings_chart` (`Moon, Venus, Mars, "TITAN · 9.5 AU"`) Cannot Be Used:**
   - `01_Script/SOURCES.md` v01 Row 7 contains no numerical distances for Moon, Venus, or Mars landings (`AGENTS.md` *Teach on screen*: *"Every DATA number is a MUST QUOTE row in SOURCES.md"*).
   - Furthermore, `9.5 AU` in `01_Script/SOURCES.md` v01 Row 8 (*"about 886 million miles (1.4 billion kilometers) from the Sun, or about 9.5 astronomical units (AU)"*) is Saturn/Titan's **heliocentric** distance from the Sun, which is already taught in Row 19 (`r19_distance`: `DISTANCE FROM SUN` · `EARTH 1 AU` vs `TITAN 9.5 AU`, approved under `J2260`). Presenting `9.5 AU` a second time in Row 23 as a `"landing distance from Earth"` bar against Moon, Venus, and Mars would conflate heliocentric orbital radius with geocentric distance at landing (`~1.2 billion km` / `~8.0 AU` on 14 January 2005).
   - Replacing `landings_chart` with the qualitative `r23_landing_record` graphic (`MOST DISTANT LANDING` · `HUYGENS` · `FROM EARTH` → `TITAN` · `NOT TO SCALE`) teaches the exact verified claim in Row 23 without inventing unsourced numbers or misrepresenting `9.5 AU`.

### B. Full-Size Still Inspection, Native `PIA14909` Crop, Labels & 109-Sample Audit (`KEEP`)
1. **Authentic `1.0×` Native Cassini ISS Titan Globe (`PIA14909`):**
   - `/Users/benjaminoats/_desk/cache/J2089/harvest_v01/PIA14909.jpg` (`993×1017` px, `source_sha256: b72f5371622b0197f91a70a62b729e1e854dd91c511639f8055cf3d93f70ce74`, NASA/JPL-Caltech/Space Science Institute, *"Titan Up Front"*) is cropped to `CROP = (295, 294, 703, 702)` (`408×408` native pixels, `upscale = 1.0`, identical to the reviewed `J2260` crop) with circular alpha mask `ellipse((0, 0, 407, 407), fill=255)` and placed at `(1290, 350)` (`x = 1290..1698, y = 350..758`).
   - Full-size (`1920×1080`) visual inspection of `code_graphic_032_r23_landing_record_v01.png` and `r23_landing_record_review.jpg` confirms a clean, natural-colour golden-orange Titan globe with zero Saturn ring pixels or background corners bleeding around the limb, and zero upscaling (`1.0× <= 2.0×`).
2. **House Typography, Subject-Safe Placement & `<= 4`-Word Label Lock:**
   - Every text element uses `HelveticaNeue.ttc` bold (`index=1`) with dark outline stroke (`stroke_width=3, stroke_fill=(20, 28, 42, 220)`), sits completely clear of the Titan globe (`x = 1290..1698, y = 350..758`), and obeys the `≤ 4`-word house rule:
     - `MOST DISTANT LANDING` (`3` words, `font(78)`, `GOLD` `#FFB347` at `(160, 140)`)
     - `HUYGENS` (`1` word, `font(62)`, `WHITE` `#F5F7FA` at `(160, 330)`)
     - `FROM EARTH` (`2` words, `font(54)`, `WHITE` at `(160, 750)`)
     - `TITAN` (`1` word, `font(62)`, `GOLD` at `(1330, 790)`, `32 px` below the bottom of the Titan globe)
     - `NOT TO SCALE` (`3` words, `font(38)`, `WHITE` at `(600, 640)`, below the connector line)
     - `NASA/JPL-Caltech/Space Science Institute` (agency credit line, `font(28)`, `WHITE` at `(160, 940)`)
3. **Animated Qualitative Connector & Reproducible 109-Sample Verification:**
   - The horizontal `GOLD` connector (`(200, 560) → (x, 560)`, `width = 6`, with arrowhead polygon `[(x, 560), (x - 22, 547), (x - 22, 573)]`, where `x = 200 + 980 * p` and `p = min(1, max(0, (t - 0.4) / 1.8))`) grows smoothly from `x = 200` (`t = 0.4 s`) to `x = 1180` (`t = 2.2 s`), stopping `110 px` left of Titan's limb (`x = 1290`).
   - Independently verified all measurements in `LANDING_RECORD_CHECKS_v01.json` and `verify_landing_record_graphic.py`:
     - `source_sha256`: `b72f5371622b0197f91a70a62b729e1e854dd91c511639f8055cf3d93f70ce74` (`MATCH`)
     - `preview_sha256`: `8a2de4177dff150ecb24e70d2e64422241f729fde5537ca5deedb540a51a9d2c` (`MATCH`, and `frame(2.4).tobytes()` matches `code_graphic_032_r23_landing_record_v01.png` byte for byte)
     - `sampled_frames`: `109` (`i = 0..108`, `t = i / 30.0 s`); active frames `i = 1..107` have alpha bounding box `(159, 154, 1698, 975)`, strictly inside the 5% safe area `[96, 54, 1824, 1026]`
     - `entry_exit_alpha_zero`: `frame(0.0)` and `frame(3.6)` have `getbbox() is None` (`alpha = 0`)
     - `changing_connector`: `ImageChops.difference(frame(0.8).convert("RGB"), frame(1.8).convert("RGB")).getbbox() == (395, 547, 963, 574)`
     - `unapproved_export_exit`: `2` (unapproved `--render` rejected with zero files written)
     - `preserved_exports`: all **61** prior `.mov` export hashes in `J2089_EXPORT_HASHES_v20.json` match byte for byte (`MATCH`).

### C. `PIA14909` Film-Wide Allocation (`R19 + R23` Only; `MAX_REUSE = 2`) & Shot-List Amendment (`KEEP`)
1. **Strict 2-Appearance Cap (`MAX_REUSE = 2`) Across All 52 Rows:**
   - Audited `SHOT_LIST_v05.md`, `J2090` (`jobs/reviews/J2090/REVIEW.md`), `J2260` (`jobs/reviews/J2260/REVIEW.md`), `HARVEST_POOL_v01.json`, and all 61 rendered manifests:
     - Earlier `SHOT_LIST_v02.md` references to `PIA14909` in Row 3 and Row 44 were replaced by `J2090` (`R03` → `PIA21902` Use 1/2 under `J2264`; `R44` → `PIA17163` Use 2/2).
     - **Use 1 of 2 — Row 19 (`184.60–197.20 s`, `12.60 s`):** `r19_distance` (`code_graphic_032_r19_distance_v01.mov`, approved under `J2260`, SHA-256 `07f4088a0f9907e1116c661df70bab106df9387759f65bf2e574848338e70bb6`).
     - **Use 2 of 2 — Row 23 (`229.78–239.50 s`, `9.72 s`, separated from Row 19 by Rows 20–22 = `32.58 s > 10 s`):** `r23_landing_record` (`code_graphic_032_r23_landing_record_v01.mov`, approved under `J2304`), using the native `408×408` crop (`1.0×` vs Row 19's `460×460` display) at right-hand origin `(1290, 350)` (vs Row 19's left-hand origin `(170, 250)`).
     - **Zero Other Uses:** `PIA14909` has **0** appearances in any other row (`R01–R18`, `R20–R22`, `R24–R52`).
2. **Row 23 Sequencing, Deduping Against `code_graphic_032_r23_fact_v01.mov`, & Shot-List Amendment:**
   - **No Duplicate `"MOST DISTANT LANDING"` Graphic in Row 23:** Because `r23_landing_record` (`code_graphic_032_r23_landing_record_v01.mov`) already features **`"MOST DISTANT LANDING"`** (`3` words, `78 pt GOLD`) as its headline (`FACT: "Most distant landing"`, `SOURCES.md` row 7) together with `HUYGENS`, `FROM EARTH → TITAN` (`PIA14909` Use 2/2), and `NOT TO SCALE`, it **supersedes and satisfies** both `landings_chart` and the standalone lower-third `FACT` card (`code_graphic_032_r23_fact_v01.mov`) in Row 23. Keep `code_graphic_032_r23_fact_v01.mov` (`5ed642b0d639a4ad1ca7f7a7e95bef4c4059057df127660caac33b25b0fcb04a`) untouched on disk in `J2089_EXPORT_HASHES_v20.json` so no prior export hash is altered, but **do not composite `code_graphic_032_r23_fact_v01.mov` in Row 23 alongside or after `r23_landing_record`**.
   - **No Back-to-Back Full-Frame Code Graphics Across Row 22 → Row 23 (`AGENTS.md` *Teach on screen*):** Row 22 (`220.54–228.72 s`) ends on `CODE surface_72m` (`"72 MIN ON TITAN"` counter). In Row 23 (`229.78–239.50 s`, `9.72 s`, 2 cuts), `r23_landing_record` (`3.60 s`) is an alpha overlay that must sit over a graded moving plate and must remain separated from Row 22's `surface_72m` by real moving imagery (e.g., opening Row 23 on the graded moving Cassini Titan crescent plate `PIA08733` [Use 2 of 2] or compositing `r23_landing_record` over the graded moving plate after a clean real-plate separation, with Cut 2 continuing on the reframed moving `PIA08733` crescent plate across *"Yet if you stepped out beside it in a heated suit, what would you feel when the rain began to fall?"* [`233.96–239.50 s`] into Row 24's mid-roll subscribe beat [`240.84–245.10 s`]).
   - **Exact Shot-List Amendment to Record When Updating `SHOT_LIST_v05.md` (`→ SHOT_LIST_v06.md`) and `HARVEST_POOL_v01.json`:**
     - Header allocation summary: add `PIA14909 to R19/R23 (2 appearances);`
     - Row 23 table entry (`229.78–239.50 s`, `9.7 s`, `2` cuts):
       `| 23 | 2 The Huygens Landing | 229.78–239.50 | 9.7 | NASA/JPL / CODE | Graded moving Cassini Titan crescent plate (PIA08733, use 2 of 2, reframed) + reviewed CODE r23_landing_record (J2304): qualitative "MOST DISTANT LANDING · HUYGENS · FROM EARTH → TITAN · NOT TO SCALE" connector with PIA14909 (use 2 of 2, native 408×408 crop; R19 use 1 of 2); supersedes quantitative landings_chart and duplicate r23_fact card | 2 | **FACT:** "Most distant landing" (3 words; SOURCES.md row 7). No 9.5 AU heliocentric label as Earth landing distance; real moving plate separates R22 surface_72m and R23 overlay. |`
     - `HARVEST_POOL_v01.json`: include `PIA14909` (`sha256: b72f5371622b0197f91a70a62b729e1e854dd91c511639f8055cf3d93f70ce74`, `width: 993`, `height: 1017`, `credit: "NASA/JPL-Caltech/Space Science Institute"`) with `referenced_rows: [19, 23]`.

---

## 3. Export Implementation Instructions & Preserved Holds for `J2089`

1. **Upgrade `landing_record_graphic.py` From Draft Guard to Reviewed Export Gate (`--render --approved r23_landing_record --review-ref J2304`):**
   - Keep `frame(t)`, `SOURCE`, `SOURCE_HASH` (`b72f5371622b0197f91a70a62b729e1e854dd91c511639f8055cf3d93f70ce74`), `CROP` (`(295, 294, 703, 702)`), and `preview_sha256` (`8a2de4177dff150ecb24e70d2e64422241f729fde5537ca5deedb540a51a9d2c`) completely unchanged.
   - Replace the draft-only `if a.render: ap.error(...)` guard in `landing_record_graphic.py` with the standard `--approved r23_landing_record --review-ref J2304` `qtrle` RGBA `.mov` export block (matching `pebble_ruler_graphic.py` and `distance_graphic.py`), writing to a **fresh output directory**:
     ```bash
     /Users/benjaminoats/_desk/venv-graphics/bin/python 02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/landing_record_graphic.py \
       --out /Users/benjaminoats/_desk/cache/J2089/landing_record_renders_v01 \
       --render \
       --approved r23_landing_record \
       --review-ref J2304
     ```
   - Register `('landing_record', landing_record, 'J2304')` in `verify_reviewed_exports.py` so the rendered `.mov` (`code_graphic_032_r23_landing_record_v01.mov`, `1920×1080`, `30 fps`, `108` frames, `3.6 s`, `qtrle` ARGB, `-an`) is verified byte-for-byte against `frame(i / 30)` and `8a2de4177dff150ecb24e70d2e64422241f729fde5537ca5deedb540a51a9d2c` alongside all **61** preserved `.mov` exports (`J2089_EXPORT_HASHES_v20.json`).

2. **Preserved Holds, Rulings & Milestone (`1/4`, `£0`):**
   - **Inherited Automatic-Review Public-Push Rejection Respected:** Do not push `/private/tmp/codex-J2089` (`worker/J2089-r18-ruler`); integrate `landing_record_graphic.py` and the `SHOT_LIST` / `HARVEST_POOL` updates cleanly in the local `J2089` checkpoint without bypassing the push rejection.
   - **Source Rights Hold Preserved:** `PIA14909` (`https://science.nasa.gov/photojournal/titan-up-front/`, credit `NASA/JPL-Caltech/Space Science Institute`) is governed by the JPL image-use policy; per-asset rights and final `≤ 2`-appearance verification on the assembled cut manifest remain required before final cut release.
   - **Composite, Moving-Plate, Contrast & Timing Hold Preserved:** The `(37, 52, 73)` navy background in `r23_landing_record_review.jpg` is a preview backdrop only. Final assembly requires compositing `code_graphic_032_r23_landing_record_v01.mov` over an approved graded moving plate (`PIA08733` Use 2 of 2) with text off the background subject, separated from Row 22's `surface_72m` by real moving imagery, and passing `≥ 4.5:1` contrast, `≤ 30%` near-black (`polish_gate.py`), and `picture_qa.py`.
   - **All Other Existing Holds & 61 Exports Preserved:**
     - All **61** existing verified `.mov` exports (`J2089_EXPORT_HASHES_v20.json`) remain untouched.
     - Row 1 Frame-0 native-motion / Chief fallback hold (`J2177`), `R16`/`R51` Huygens DISR mosaic (`PIA07870`/`PIA07871`) seam/crop hold (`J2089_CHECKPOINT_v18.md`), and `JHUAPL` Dragonfly animation written-permission hold (`J2089_CHECKPOINT_v05.md`) remain in force.
     - `J2247` (`r09_sizes` + `PIA15162`), `J2251` (`r52_uranus_21y`), `J2260` (`r19_distance` + `PIA14909` Use 1/2), `J2262` (`r08_orbit_period` + `PIA14922` `R06`/`R08`), `J2264` (`r35_ocean` + `PIA14602` `R09`/`R35`), `J2277` (`r10_spectrum` + `r32_scalemap`), and `J2296` (`r18_ruler` + `PIA07232` `R18`/`R20`) rulings remain in force.
   - **Parent `J2089` Milestone Remains `1/4` (`£0` spent):** Exporting `r23_landing_record` under `--review-ref J2304`, reconciling `SHOT_LIST` and `HARVEST_POOL_v01.json`, completing the licensed harvest, and assembling/verifying the graded composites remain on `J2089`.
