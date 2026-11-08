# J2296 — Film 032 Row 18 (`r18_ruler`) Registered Pebble Ruler Still & `PIA07232` Source Allocation Review

- **Job:** `J2296` (`032 R18 pebble ruler: review registered still and source allocation`)
- **Parent Job:** `J2089` (`032 picture: £0 harvest + code_graphics builds from SHOT_LIST_v02 (WIP film)`, `1/4`)
- **Film:** `OWB:032` (`02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan`)
- **Reviewer:** `gemini` (`gemini-argon`, specialist worker; still-image visual review + structural/reuse audit — not Chief final `OK`, not moving-video or audio perception, not composite or film-stage `PASS`)
- **Reviewed Worktree & Commit:** `/private/tmp/codex-J2089` (`worker/J2089-r18-ruler` at local commit `1638fd13c1187993b2b1173ea7e533a9f8110cf4`, inherited automatic-review public-push rejection respected)
- **Reviewed Artefacts:**
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/J2089_R18_REVIEW_REQUEST_v01.md`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/J2089_CHECKPOINT_v19.md`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/PEBBLE_RULER_MANIFEST_v01.json`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/PEBBLE_RULER_CHECKS_v01.json`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/pebble_ruler_graphic.py`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/verify_pebble_ruler_graphic.py`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/SHOT_LIST_v05.md` (`8ff3ddc7d6`)
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/01_Script/SOURCES.md` (governing v01 Row 8)
  - `/Users/benjaminoats/_desk/cache/J2089/pebble_ruler_previews_v03/r18_ruler_review.jpg` (`1920×1080` RGB over `(37, 52, 73)` preview backdrop, `141,156` bytes, SHA-256 `1b6cba0fc14d7f6efc867bcb4c658d5c489f25061cb7c462dea81a27c6c78cb0`, inspected full size)
  - `/Users/benjaminoats/_desk/cache/J2089/pebble_ruler_previews_v03/code_graphic_032_r18_ruler_v01.png` (`1920×1080` RGBA at `t = 2.4 s`, `334,335` bytes, `preview_sha256: 3c5a2f296be594fd161062a548e9e970962c8b5dbae630d542da0cc7a09c0517`, inspected full size)
  - `/Users/benjaminoats/_desk/cache/J2089/harvest_v03/PIA07232.jpg` (`546×693` RGB, `23,891` bytes, `source_sha256: 4221ee7a4588a6ea169a0b438b5526e26c68827cb717a31ef1f81284b39cd3e8`, inspected full size)

---

## 1. Verdict Summary

| Check Item | Ruling | Summary |
|---|---|---|
| **1. `r18_ruler` Registered Still (`code_graphic_032_r18_ruler_v01.png`, SHA-256 `3c5a2f296be594fd161062a548e9e970962c8b5dbae630d542da0cc7a09c0517`)** | **`KEEP` / `APPROVED` to Export Under `--render --approved r18_ruler --review-ref J2296`** | Object identity, manual bracket endpoints `(148, 423)` and `(269, 423)`, soft `1.4308× <= 1.44×` portrait source inset (`449×900` px from `314×629` px crop), and house labels (`ABOUT 15 CENTIMETRES`, `PEBBLES`, `ESA/NASA/JPL/University of Arizona`) accurately teach Row 18 (`172.16–183.54 s`) and `01_Script/SOURCES.md` v01 Row 8 without obscuring the foreground cobble or inferring a false global perspective scale. Approved to export `code_graphic_032_r18_ruler_v01.mov` (`1920×1080`, `30 fps`, `108` frames, `3.6 s`, `qtrle` RGBA, `-an`) under `--render --approved r18_ruler --review-ref J2296`. |
| **2. `PIA07232` Film-Wide Source Allocation (`R18 + R20` Only; `MAX_REUSE = 2`)** | **`APPROVED` — Capped at `R18` (Use 1 of 2) and `R20` (Use 2 of 2) Only (`0` Uses in `R25` or Any Other Row)** | Confirms `J2177` (`e54320112b`) and `SHOT_LIST_v05.md` (`8ff3ddc7d6`): `PIA07232` is reserved strictly to **Row 18 (`172.16–183.54 s`, Use 1 of 2)** and **Row 20 (`198.02–205.82 s`, Use 2 of 2, separated by Row 19's `12.60 s`)**, with **no third appearance in Row 25** (`R25` uses `PIA17163` Use 1/2 + `PIA21450` Use 2/2) and no use in Row 5 (`PIA07231`). Update `HARVEST_POOL_v01.json` `referenced_rows` for `PIA07232` from `[18, 20, 25]` to `[18, 20]` when reconciling the harvest pool. |

---

## 2. Detailed Evaluation of Required Check Items

### A. Object Identity & Governing Source Agreement (`KEEP`)
1. **Authentic Huygens DISR Surface Frame (`PIA07232`):**
   - `/Users/benjaminoats/_desk/cache/J2089/harvest_v03/PIA07232.jpg` (`546×693`, SHA-256 `4221ee7a4588a6ea169a0b438b5526e26c68827cb717a31ef1f81284b39cd3e8`) is the unaltered 14 January 2005 ESA/NASA/JPL/University of Arizona Huygens Descent Imager/Spectral Radiometer (DISR) surface photograph (*"First Color View of Titan's Surface"*).
2. **Exact Match to ESA Caption and `01_Script/SOURCES.md` v01 Row 8:**
   - **Locked Row 18 VO (`172.16–183.54 s`, `11.38 s`):**
     - `172.16–175.38 s`: *"Huygens lands softly on what looks like a dry riverbed,"*
     - `175.98–180.36 s`: *"scattered with rounded pebbles (`177.18–177.66 s`) up to (`178.04–178.26 s`) about (`178.32–178.60 s`) fifteen (`178.68–179.08 s`) centimeters (`179.20–179.76 s`) across (`179.82–180.36 s`),"*
     - `180.94–183.54 s`: *"just like stones in a stream bed on Earth."*
   - **Governing `01_Script/SOURCES.md` v01 Row 8 & ESA Caption (`https://www.esa.int/ESA_Multimedia/Images/2005/01/First_colour_view_of_Titan_s_surface` / `https://www.esa.int/media/first-colour-view-of-titan-s-surface`):**
     - Verbatim quote: *"Initially thought to be rocks or ice blocks, they are more pebble-sized. The two rock-like objects just below the middle of the image are about 15 centimetres (left) and 4 centimetres (centre) across respectively, at a distance of about 85 centimetres from Huygens."*
   - Direct visual inspection of `PIA07232.jpg` and `r18_ruler_review.jpg` confirms that the two prominent foreground objects just below the vertical midpoint of the frame are (1) the flat, elongated light-orange cobble on the left (`x ≈ 148..269, y ≈ 395..450` in source coordinates) and (2) the smaller, more globular cobble immediately to its right (`x ≈ 269..335, y ≈ 395..480`). The gold bracket in `pebble_ruler_graphic.py` is registered over the **left elongated foreground cobble**, which is the exact `≈ 15 cm` object identified by ESA.

### B. Manual Endpoints & Non-Obstructing Bracket Placement (`KEEP`)
1. **Source-to-Canvas Endpoint Registration:**
   - `ENDPOINTS = ((148, 423), (269, 423))` in source coordinates (`121 px` span across the `314 px` interior width) map through `point(p)` onto the `1920×1080` canvas at:
     - Left endpoint `a = (265.76, 649.46)` (aligning cleanly with the left margin of the left elongated foreground cobble).
     - Right endpoint `b = (438.78, 649.46)` (aligning cleanly with the right margin of that same left elongated cobble where it meets the adjacent central cobble).
2. **Subject-Safe Vertical Offset (`y = a[1] - 44 = 605.46`):**
   - The horizontal `GOLD` bracket line (`width = 5`) and end ticks (`y - 12 .. y + 12`, `593.46..617.46`) are drawn `44 px` above `a[1]` (`y = 605.46` on canvas, corresponding to `y ≈ 392.25` in source coordinates).
   - Visually verified on `r18_ruler_review.jpg` and `code_graphic_032_r18_ruler_v01.png`: the bracket sits over the dark flat riverbed strip immediately above the left cobble's upper edge, leaving the entire cobble unobstructed (`AGENTS.md` *Teach on screen*: *"text stays off the subject"*).
   - The `WHITE` callout leader line (`(456.78, 605.46) → (780, 605.46) → (820, 410)`, `width = 3`) starts `18 px` clear of the right bracket tick (`b[0] + 18`), crosses the right edge of the inset cleanly, and angles up to the label block at `x = 850`.
   - `PEBBLE_RULER_MANIFEST_v01.json` and `pebble_ruler_graphic.py` explicitly document that this bracket is an approximate visual annotation of the left foreground cobble named in ESA's caption, never a photogrammetric calibration of the entire perspective image.

### C. Soft Source Inset & Scale Compliance (`KEEP`)
1. **Clean Removal of White Publication Surround (`CROP = (116, 32, 430, 661)`):**
   - `PIA07232.jpg` (`546×693` px) contains a white publication border around the native `314×629` px portrait DISR photograph. Cropping to `(116, 32, 430, 661)` removes 100% of the white surround while preserving the full vertical extent of the authentic DISR frame from foreground cobbles to horizon.
2. **Modest Portrait Inset Scale (`1.4308× <= 1.44×`):**
   - Resized via `Image.Resampling.LANCZOS` to `DISPLAY = (449, 900)` at `ORIGIN = (220, 90)` (`x = 220..669, y = 90..990`), the maximum enlargement factor is `max(449 / 314, 900 / 629) = 1.4308426073131955×` — well below `scripts/picture_qa.py`'s `2.0×` warning threshold and `2.35×` hard-fail limit (`J2150`: *"as an inset card at no more than 2× native size, cropped clear of the white surround"*).
   - Full-size (`1920×1080`) visual inspection confirms that the soft 2005 Huygens DISR telemetry texture reads honestly as an archival spacecraft photograph without blocky upscaling artifacts, synthetic sharpening halos, or painted pixels, while the vector bracket and typography on the right provide crisp high-contrast visual structure.

### D. Labels, Typography, Safe Area & Reproducible Checks (`KEEP`)
1. **House Typography & `<= 4`-Word Label Lock:**
   - All text elements use `HelveticaNeue.ttc` bold (`index=1`), sit completely outside the `449×900` photograph inset (`x = 850 > 669`), and obey the `≤ 4`-word house rule:
     - `ABOUT 15 CENTIMETRES` (`3` words, `font(62)`, `GOLD` `#FFB347`, `stroke_width=3`, `stroke_fill=(20, 28, 42, 220)` at `(850, 365)`)
     - `PEBBLES` (`1` word, `font(58)`, `WHITE` `#F5F7FA`, `stroke_width=3`, `stroke_fill=(20, 28, 42, 220)` at `(850, 465)`)
     - `ESA/NASA/JPL/University of Arizona` (`1` agency credit line, `font(27)`, `WHITE` at `(850, 840)`)
2. **Reproducible 109-Sample Verification:**
   - Independently verified all checks in `PEBBLE_RULER_CHECKS_v01.json` and `verify_pebble_ruler_graphic.py`:
     - `source_sha256`: `4221ee7a4588a6ea169a0b438b5526e26c68827cb717a31ef1f81284b39cd3e8` (`MATCH`)
     - `preview_sha256`: `3c5a2f296be594fd161062a548e9e970962c8b5dbae630d542da0cc7a09c0517` (`MATCH`, and `frame(2.4).tobytes()` matches `code_graphic_032_r18_ruler_v01.png` byte for byte)
     - `sampled_frames`: `109` (`i = 0..108`, `t = i / 30.0 s`); active frames `i = 1..107` have alpha bounding box `[220, 90, 1570, 990]`, strictly inside the 5% safe area `[96, 54, 1824, 1026]`
     - `entry_exit_alpha_zero`: `frame(0.0)` and `frame(3.6)` have `getbbox() is None` (`alpha = 0`)
     - `changing_bracket`: `ImageChops.difference(frame(0.8).convert("RGB"), frame(1.8).convert("RGB")).getbbox() == (310, 603, 418, 608)`
     - `render_guard_exit`: `2` (unapproved `--render` rejected with zero files written)

### E. `PIA07232` Film-Wide Allocation (`R18 + R20` Only; No Third Use in `R25`)
1. **Strict 2-Appearance Cap (`MAX_REUSE = 2`):**
   - Per `J2177` (`e54320112b`) and `SHOT_LIST_v05.md` (`8ff3ddc7d6`), `PIA07232` is allocated to **at most 2 appearances** across Film `032`:
     1. **Use 1 of 2 — Row 18 (`172.16–183.54 s`, `11.38 s`):** Huygens surface pebbles (`PIA07232`) + `r18_ruler` (`code_graphic_032_r18_ruler_v01.mov`, `3.60 s`, timed to *"scattered with rounded pebbles up to about fifteen centimetres across"* at `176.70–180.36 s`).
        - *Note on Row 18 Cut 1 + Cut 2 framing:* Because `PIA07232`'s usable interior is `314×629` px, any full-frame `1920×1080` crop (`6.11×` upscale) would hard-FAIL `picture_qa.py` (`≤ 2.35×`). Keep `PIA07232` within the `≤ 2.0×` inset cap (`1.4308×`) over an approved graded moving plate in Row 18; back-to-back cuts of `PIA07232` within Row 18 count as **1 appearance** under `picture_qa.py`.
     2. **Use 2 of 2 — Row 20 (`198.02–205.82 s`, `7.80 s`, separated from Row 18 by Row 19's `12.60 s > 10 s`):** Second and final appearance of `PIA07232` (distinctly framed within `≤ 2.35×` over a graded moving plate) with the `FACT` card `"WATER ICE IS ROCK"` (`code_graphic_032_r20_fact_v01.mov`).
     3. **No Appearance in Row 25 (`246.00–258.48 s`) or Row 5 (`32.76–44.56 s`):** Row 25 uses `PIA17163` (Use 1/2) + `PIA21450` (Use 2/2) per `J2177` and `SHOT_LIST_v05.md`; Row 5 uses `PIA07231`. When reconciling `HARVEST_POOL_v01.json`, update `PIA07232`'s `referenced_rows` from `[18, 20, 25]` to `[18, 20]`.

---

## 3. Export Implementation Instructions & Preserved Holds for `J2089`

1. **Upgrade `pebble_ruler_graphic.py` From Draft Guard to Reviewed Export Gate (`--render --approved r18_ruler --review-ref J2296`):**
   - Keep `frame(t)`, `SOURCE`, `SOURCE_HASH`, `CROP`, `DISPLAY`, `ORIGIN`, `ENDPOINTS`, and `preview_sha256` (`3c5a2f296be594fd161062a548e9e970962c8b5dbae630d542da0cc7a09c0517`) completely unchanged.
   - Replace the draft-only `if args.render: ap.error(...)` guard in `pebble_ruler_graphic.py` with the standard `--approved r18_ruler --review-ref J2296` `qtrle` RGBA `.mov` export block (matching `orbit_period_graphic.py` and `ocean_graphic.py`), writing to a **fresh output directory**:
     ```bash
     /Users/benjaminoats/_desk/venv-graphics/bin/python 02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/pebble_ruler_graphic.py \
       --out /Users/benjaminoats/_desk/cache/J2089/pebble_ruler_renders_v01 \
       --render \
       --approved r18_ruler \
       --review-ref J2296
     ```
   - Register `('pebble_ruler', pebble_ruler, 'J2296')` in `verify_reviewed_exports.py` so the rendered `.mov` (`code_graphic_032_r18_ruler_v01.mov`, `1920×1080`, `30 fps`, `108` frames, `3.6 s`, `qtrle` ARGB, `-an`) is verified byte-for-byte against `frame(i / 30)` and `3c5a2f296be594fd161062a548e9e970962c8b5dbae630d542da0cc7a09c0517` alongside the **60** preserved `.mov` exports.

2. **Preserved Holds, Rulings & Milestone (`1/4`, `£0`):**
   - **Inherited Automatic-Review Public-Push Rejection Respected:** Do not push `/private/tmp/codex-J2089` (`worker/J2089-r18-ruler`); integrate `pebble_ruler_graphic.py` cleanly in the local `J2089` checkpoint without bypassing the push rejection.
   - **Source Rights Hold Preserved:** ESA's page (`https://www.esa.int/media/first-colour-view-of-titan-s-surface`) lists `ESA Standard Licence` (`ESA/NASA/JPL/University of Arizona`) and NASA Photojournal (`https://science.nasa.gov/photojournal/first-color-view-of-titans-surface/`) cites the JPL image-use policy; per-asset rights clearance remains a distinct hold before final cut release.
   - **Composite, Moving-Plate, Contrast & Timing Hold Preserved:** The `(37, 52, 73)` navy background in `r18_ruler_review.jpg` is a preview backdrop only. Final assembly requires compositing `code_graphic_032_r18_ruler_v01.mov` over an approved graded moving plate, timed to the Row 18 spoken line, and passing `≥ 4.5:1` contrast, `≤ 30%` near-black (`polish_gate.py`), and `picture_qa.py`.
   - **All Other Existing Holds & 60 Exports Preserved:**
     - All **60** existing verified `.mov` exports (`J2089_EXPORT_HASHES_v17.json`) remain untouched.
     - Row 1 Frame-0 native-motion / Chief fallback hold (`J2177`), `R16`/`R51` Huygens DISR mosaic seam/crop hold (`J2089_CHECKPOINT_v18.md`), and `JHUAPL` Dragonfly animation written-permission hold (`J2089_CHECKPOINT_v05.md`) remain in force.
     - `J2247` (`r09_sizes` + `PIA15162`), `J2251` (`r52_uranus_21y`), `J2260` (`r19_distance` + `PIA14909`), `J2262` (`r08_orbit_period` + `PIA14922` `R06`/`R08`), `J2264` (`r35_ocean` + `PIA14602` `R09`/`R35`), and `J2277` (`r10_spectrum` + `r32_scalemap`) rulings remain in force.
   - **Parent `J2089` Milestone Remains `1/4` (`£0` spent):** Exporting `r18_ruler` under `--review-ref J2296`, building/reviewing `R23` (`landings_chart`), completing the licensed harvest, and assembling/verifying the graded composites remain on `J2089`.
