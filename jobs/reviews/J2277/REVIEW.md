# J2277 — Film 032 Corrected Mechanism Stills Review (`r10_spectrum` & `r32_scalemap` under `J2177`)

- **Job:** `J2277` (`032: verify corrected J2177 spectrum and area stills`)
- **Parent Job:** `J2089` (`032 picture: £0 harvest + code_graphics builds from SHOT_LIST_v02 (WIP film)`, `1/4`)
- **Film:** `OWB:032` (`02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan`)
- **Reviewer:** `gemini` (`gemini-argon`, specialist worker; still-image visual review + structural audit — not Chief final `OK`, not moving-video or composite contrast `PASS`)
- **Reviewed Worktree & Commit:** `/private/tmp/J2089-mechanism-fix-wt` (`worker/J2089-mechanism-fix` at local commit `176a3ef889537984d814d752f01a989a2064adb6`, inherited automatic-review public-push rejection respected)
- **Reviewed Artefacts:**
  - `jobs/reviews/J2177/REVIEW.md` on `main` (`e54320112b`)
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/J2089_CHECKPOINT_v16.md`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/MECHANISM_FIX_MANIFEST_v02.json`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/MECHANISM_FIX_VERIFICATION_v02.json`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/mechanism_graphics.py`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/verify_mechanism_fixes.py`
  - `/Users/benjaminoats/_desk/cache/J2089/mechanism_previews_v02/code_graphic_032_r10_spectrum_v01.png` (`1920×1080` RGBA at `t = 1.8 s`, `20,141` bytes, `preview_sha256: 57576de51068f012d3790464010d661c38127d59bdbf343bc511fa162ec302e0`, inspected full size)
  - `/Users/benjaminoats/_desk/cache/J2089/mechanism_previews_v02/code_graphic_032_r32_scalemap_v01.png` (`1920×1080` RGBA at `t = 1.8 s`, `48,785` bytes, `preview_sha256: 9fabc50ef3a8dfcfd01e53edb6182816c83da4208540c8ec667ce424a9947124`, inspected full size)
  - `/Users/benjaminoats/_desk/cache/J2089/mechanism_previews_v02/mechanism_previews.jpg` (`1280×3240` contact sheet over `(40, 58, 79)`, inspected full size)

---

## 1. Verdict Summary: 2 of 2 `KEEP` (Approved to Export Under `--review-ref J2277`)

| # | Clip ID | Row | Kind | Verbatim On-Screen Labels | `SOURCES.md` v01 Row(s) | Corrected Preview SHA-256 (`mechanism_previews_v02`) | Verdict & Check Notes |
|---:|---|---:|---|---|---|---|---|
| 1 | `r10_spectrum` | 10 | `spectrum` | `LIGHT` · `METHANE` | Row 4 (`1944: Gerard Kuiper finds the fingerprint of methane in Titan's light`) | `57576de51068f012d3790464010d661c38127d59bdbf343bc511fa162ec302e0` | **`KEEP`** — Upright white-outlined triangle prism `[(580, 650), (720, 360), (860, 650)]`; incoming blue ray `(200, 510) → (648, 510)` meets the left sloped face (`x ≈ 647.6` at `y = 510`); dispersed rays (`BLUE`, `WHITE`, `GOLD`) exit the right sloped face at `(792, 510)` (`x ≈ 792.4` at `y = 510`) and fan rightward; gold-outlined absorption notch `(1106, 480, 1134, 650)` (`fill=(20, 28, 42, 255)`, `outline=GOLD`, `width=4`), vertical gold pointer `(1120, 655) → (1120, 720)`, and `METHANE` label at `(960, 735)` reveal only once rays arrive at `x = 1120` (`p >= 0.75`, `t >= 1.20 s`). Bounds `[161, 190, 1246, 794]` inside 5% safe area `[96, 54, 1824, 1026]` across all 109 samples. |
| 2 | `r32_scalemap` | 32 | `area` | `KRAKEN MARE` · `≈ 400,000 KM²` · `≈ 5× LAKE SUPERIOR` | Row 11 (`Kraken Mare about 400,000 km², almost five times the size of Lake Superior`) | `9fabc50ef3a8dfcfd01e53edb6182816c83da4208540c8ec667ce424a9947124` | **`KEEP`** — Retains the approved five-part area comparison rectangle `(210, 390, 1110, 750)` with 4 white vertical dividers (`210 + 180*n`) and animated blue fill (`216 + 888*p`); `lines[1]` updated to `"≈ 400,000 KM²"` and drawn in `WHITE` (`size=76`) with standard 3 px dark stroke `(20, 28, 42, 255)`, keeping the superscript `²` sharp and legible over both dark background before fill arrival and the blue fill across all frames. Bounds `[161, 191, 1111, 868]` inside 5% safe area `[96, 54, 1824, 1026]` across all 109 samples. |

---

## 2. Detailed Verification of `J2177` Fixes & Structural Checks

1. **`r10_spectrum` (`code_graphic_032_r10_spectrum_v01.png`, SHA-256 `57576de51068f012d3790464010d661c38127d59bdbf343bc511fa162ec302e0`):**
   - **Prism Geometry:** Upright triangle `[(580, 650), (720, 360), (860, 650)]` (`outline=WHITE, width=5`). At `y = 510`, the left edge passes through `x = 580 + (720 - 580) * (650 - 510) / (650 - 360) = 647.59` and the right edge passes through `x = 860 - 67.59 = 792.41`. The incoming `BLUE` ray `(200, 510) → (648, 510)` meets the left face cleanly, and the three dispersed rays (`BLUE`, `WHITE`, `GOLD`) exit from `(792, 510)` on the right face to `(792 + 438*p, 510 + (-120 + i*120)*p)`.
   - **High-Contrast Outlined Notch, Pointer & Arrival Timing (`p >= 0.75`):** At `p = 0.75` (`t = 1.20 s`), the dispersed rays reach `x = 792 + 438 * 0.75 = 1120.5`. Only for `p >= 0.75` does `frame()` draw the dark navy notch `rounded_rectangle((1106, 480, 1134, 650), radius=6, fill=(20, 28, 42, 255), outline=GOLD, width=4)`, the vertical `GOLD` pointer line `(1120, 655, 1120, 720)` (`width=5`), and `METHANE` in `GOLD` at `(960, 735)`. Independently verified `frame(s, 1.19).getpixel((1120, 680))[3] == 0` (no premature floating bar) and `frame(s, 1.21).getpixel((1120, 680))[3] > 0`.

2. **`r32_scalemap` (`code_graphic_032_r32_scalemap_v01.png`, SHA-256 `9fabc50ef3a8dfcfd01e53edb6182816c83da4208540c8ec667ce424a9947124`):**
   - **Approximate Value & Outlined White Typography:** `SPECS` row 32 updates `labels[1]` to `'≈ 400,000 KM²'` matching the locked Row 32 VO (*"covers about four hundred thousand square kilometres"*) and `SHOT_LIST_v04.md`, and draws it via `label(d, (240, 450), lines[1], 76, WHITE)` (`fill=WHITE`, `stroke_width=3`, `stroke_fill=(20, 28, 42, 255)`). Full-size visual inspection confirms the superscript `²` is clean and un-smudged, and the white glyphs with dark 3 px stroke maintain strong contrast both over the dark background before the animated blue bar reaches the right side of the text and over the `BLUE` `(102, 205, 245, 255)` fill.
   - **Five-Part Area Comparison Retained:** The `WHITE`-outlined outer rectangle `(210, 390, 1110, 750)` (`width=5`), animated `BLUE` fill `(216, 396, 216 + 888*p, 744)`, 4 vertical `WHITE` dividers at `x = 390, 570, 750, 930` (`width=3`), header `KRAKEN MARE` (`GOLD` at `(160, 180)`), and subtitle `≈ 5× LAKE SUPERIOR` (`GOLD`, `size=58` at `(210, 810)`) are unchanged.

3. **218 Safe-Area Samples, Entry/Exit Alpha, Byte-Identical 15 Previews, Render Guard & Preserved Exports:**
   - Re-ran `/Users/benjaminoats/_desk/venv-graphics/bin/python 02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/verify_mechanism_fixes.py` in `/private/tmp/J2089-mechanism-fix-wt` (exit `0`, matching `MECHANISM_FIX_VERIFICATION_v02.json`):
     - All **218 safe-area samples** (`109` frames `n = 0..108` at `30 fps` for `r10_spectrum` and `109` frames for `r32_scalemap`) lie strictly inside the 5% safe area `[96, 54, 1824, 1026]`.
     - Entry (`t = 0.0 s`) and exit (`t = 3.6 s`) frames are fully transparent (`getbbox() is None`), and `frame(s, 0.8) != frame(s, 1.5)` for both clips.
     - `frame(s, 1.8).tobytes()` matches each saved PNG in `/Users/benjaminoats/_desk/cache/J2089/mechanism_previews_v02/` byte for byte.
     - All **15 other mechanism preview PNGs** in `/Users/benjaminoats/_desk/cache/J2089/mechanism_previews_v02/` have identical SHA-256 digests to `/Users/benjaminoats/_desk/cache/J2089/mechanism_previews_v01/` (already `KEEP` under `J2177`).
     - `mechanism_graphics.py --render` without `--approved` and `--review-ref` exits `2` (`Render requires named reviewed ids and a review reference`).
     - All **58 earlier `.mov` exports** under `/Users/benjaminoats/_desk/cache/J2089/` are preserved intact; no `.mov` was rendered prior to this review, and no motion or audio perception is claimed.

---

## 3. Export Command & Preserved Holds for `J2089`

1. **Exact Export Command for `r10_spectrum` and `r32_scalemap` (`--review-ref J2277`):**
   `J2089` is reopened to export `r10_spectrum` and `r32_scalemap` into a fresh output directory (leaving the 58 earlier exports untouched):
   ```bash
   /Users/benjaminoats/_desk/venv-graphics/bin/python 02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/mechanism_graphics.py \
     --out /Users/benjaminoats/_desk/cache/J2089/mechanism_renders_v02_fixes \
     --render \
     --approved r10_spectrum r32_scalemap \
     --review-ref J2277
   ```
   Verify the 2 new `.mov` exports (`code_graphic_032_r10_spectrum_v01.mov` and `code_graphic_032_r32_scalemap_v01.mov`, `1920×1080`, `30 fps`, `108` frames, `3.6 s`, `qtrle` RGBA, `-an`) alongside the 58 preserved exports (bringing the verified overlay export total to **60**).

2. **Preserved Holds, Rulings & Milestone (`1/4`, `£0`):**
   - **Inherited Public-Push Rejection Respected:** Do not push `/private/tmp/J2089-mechanism-fix-wt` (`worker/J2089-mechanism-fix`) directly if its ancestor carries an automatic-review push rejection; keep local checkpoint integration clean.
   - **No MOV, Composite Contrast, or Film Stage Approval:** This review approves the 2 corrected overlay stills (`r10_spectrum`, `r32_scalemap`) for `.mov` export only. Final graded moving real plates, `picture_qa.py`, `polish_gate.py`, and composite contrast checks remain required.
   - **All Existing Source, Frame-0, APL & Reuse Holds Remain in Force:**
     - `J2177` (`e54320112b`): `PIA07232` capped at 2 uses (`R18` + `R20` only; `R25` uses `PIA17163` Use 1/2 + `PIA21450` Use 2/2); `R16`/`R51` use real DISR mosaics `PIA07870`/`PIA07871` (or 1-use Cassini pool plates); Row 1 Frame-0 bounded `GSFC` native-motion check or separately scoped Chief fallback remains in force.
     - `J2247` (`ce9282cb61`): `r09_sizes` `KEEP` and `PIA15162` MESSENGER usage-statement clearance.
     - `J2264` (`8696af1d91`): `r35_ocean` `KEEP` and `PIA14602` capped at 2 uses (`R09` + `R35` only; `R03` uses `PIA21902` Use 1/2).
     - `J2260` (`4261d05bb6`): `r19_distance` linear 2-bar AU comparison with `PIA14909` or `PIA21610` swap (`PIA14602` excluded from `R19`).
     - `J2262` (`39d63bd8f9`): `r08_orbit_period` `KEEP` and `PIA14922` capped at 2 uses (`R06` + `R08` only).
     - `JHUAPL` Dragonfly animation written-permission hold (`J2089_CHECKPOINT_v05.md`) remains in force.
   - **Parent `J2089` Milestone Remains `1/4` (`£0` spent):** Exporting `r10_spectrum` and `r32_scalemap`, completing the licensed harvest, building the remaining real-body graphics (`R18` pebble ruler, `R23` landings chart), and assembling/verifying the graded composites remain on `J2089`.
