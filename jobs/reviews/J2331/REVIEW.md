# J2331 — Film 032 Row 18 (`r18_ruler`) Composite Candidate Layout & Same-Source Blurred Background Review

- **Job:** `J2331` (`032 R18: review composite candidate layout and source placement`)
- **Parent Job:** `J2089` (`032 picture: £0 harvest + code_graphics builds from SHOT_LIST_v02 (WIP film)`, `1/4`)
- **Film:** `OWB:032` (`02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan`)
- **Reviewer:** `gemini` (`gemini-argon`, specialist worker; full-size still-image visual review + composite layout/contrast/reuse audit — not Chief final `OK`, not moving-video or audio perception, not source rights clearance or film-stage `PASS`)
- **Reviewed Worktree & Commit:** `/private/tmp/codex-J2089` (`worker/J2089-r18-ruler` at local commit `948a33770a5eaa93518b4ec43eaa06557a6d37f4`, inherited automatic-review public-push restriction respected)
- **Reviewed Artefacts:**
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/J2089_R18_COMPOSITE_REVIEW_REQUEST_v01.md`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/J2089_CHECKPOINT_v24.md`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/composite_r18_preview.py`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/R18_COMPOSITE_PREVIEW_v01.json`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/R18_COMPOSITE_VERIFICATION_v01.json`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/R18_COMPOSITE_CUTS_v01.json`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/R18_COMPOSITE_POLISH_v01.json`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/PEBBLE_RULER_RENDER_MANIFEST_v01.json`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/SHOT_LIST_v07.md` (`d135834c03`)
  - `/Users/benjaminoats/_desk/cache/J2089/r18_composite_preview_v01/032_r18_composite_preview_v01.mp4` (`1920×1080`, `30 fps`, `108` frames, `3.600000 s`, `-an`, `664,795` bytes, SHA-256 `c5e70b74ec76f4af9ee0dc3bfba076be9803aac535b6397ca993db132588712d`)
  - `/Users/benjaminoats/_desk/cache/J2089/r18_composite_preview_v01/frame_012.png` (`1920×1080` RGB at `t = 0.40 s`, `1,436,455` bytes, SHA-256 `dc33974e3f6af0aa11e74a4ddd17121eb8fd291f2c1ae9c039f48f475d3298f5`, inspected full size)
  - `/Users/benjaminoats/_desk/cache/J2089/r18_composite_preview_v01/frame_054.png` (`1920×1080` RGB at `t = 1.80 s`, `1,436,978` bytes, SHA-256 `ac6316fda052e072ad60afc8fafe5a95cbc6dd78d4df8714fef0a9071a3e9ee9`, inspected full size)
  - `/Users/benjaminoats/_desk/cache/J2089/r18_composite_preview_v01/frame_072.png` (`1920×1080` RGB at `t = 2.40 s`, `1,436,374` bytes, SHA-256 `6d7ec4e623fa1cc710c676cf07b787b63c1e0df46ea0cc429ca3124c1e8027db`, inspected full size)
  - `/Users/benjaminoats/_desk/cache/J2089/r18_composite_preview_v01/frame_095.png` (`1920×1080` RGB at `t = 3.17 s`, `1,436,977` bytes, SHA-256 `e371a65756c76446dab3b56595f9a5b4223d07e32e41f64bbe5d084d9c7fd816`, inspected full size)

---

## 1. Verdict Summary

| Check Item | Ruling | Summary |
|---|---|---|
| **1. R18 Composite Candidate Layout & Full-Size Stills (`032_r18_composite_preview_v01.mp4`, `frame_012.png`, `frame_054.png`, `frame_072.png`, `frame_095.png`)** | **`KEEP` (Layout & Composite Placement Only)** | All four full-size (`1920×1080`) stills pass visual inspection: the unchanged `J2296` `449×900` px `PIA07232` portrait inset (`1.43084× <= 1.44× <= 2.0×`) sits cleanly at `(220, 90)`, the `GOLD` bracket `(265.76, 605.46) → (438.78, 605.46)` builds smoothly over the dark riverbed strip `44 px` above the left elongated `≈ 15 cm` cobble without touching the cobble itself, and the right-hand labels (`ABOUT 15 CENTIMETRES`, `PEBBLES`, `ESA/NASA/JPL/University of Arizona`) sit completely off the inset with strong measured WCAG contrast (`4.87:1` `GOLD` vs background, `8.09:1` `WHITE` vs background, `9.59:1` `GOLD` vs `#141C2A` stroke). |
| **2. Same-Source Feathered/Blurred Graded Background (`PIA07232` cropped `(116, 32, 430, 661)`, `GaussianBlur(65)`, `72%` `(37, 52, 73)` navy blend, `24 px` decorative pan, `±2` fine grain)** | **`KEEP` — Fits House Style & Preserves `PIA07232` `R18 + R20` Cap** | Using the heavily defocused, navy-graded `PIA07232` surround behind the `449×900` `PIA07232` portrait inset satisfies `AGENTS.md` Standing Lesson 2 (*Edit (v03b)*: *"fill 16:9 (feathered blur OK)"*), *Teach on screen* (*"never a flat black slab"*, passing `polish_gate.py` near-black with `mean_luma = 75.91..93.80 >= 28.0` and `p95 = 80.85..174.0 >= 50.0`), and *Polish pass* 3 (*GRAIN*: `±2` deterministic grain eliminates 8-bit gradient banding), while keeping the right-hand label area subdued and consuming **zero additional source appearances** beyond `PIA07232`'s approved `R18 + R20` (`MAX_REUSE = 2`) allocation. |
| **3. Tool Evidence, Decode, `polish_gate.py` & 62 Prior Exports** | **`VERIFIED` (Measurements Only — Not Film-Stage `PASS`)** | Independently verified `source_sha256`, `overlay_sha256` (`J2296`), `video` SHA-256, all 4 still SHA-256s, `108`-frame `ffmpeg` decode (`exit 0`), `scripts/polish_gate.py` (`PASS: 0 of 1 rows failed, 0 to look at`), and all **62** prior `.mov` export hashes in `J2089_EXPORT_HASHES_v22.json` + `verify_reviewed_exports.py`. |

---

## 2. Detailed Evaluation of Required Check Items

### A. Full-Size Visual Inspection of the Four Stills (`KEEP`)
1. **Unchanged `J2296` Scientific Inset (`449×900` px at `(220, 90)`, `1.43084×` Enlargement):**
   - Across `frame_012.png` (`t = 0.40 s`), `frame_054.png` (`t = 1.80 s`), `frame_072.png` (`t = 2.40 s`), and `frame_095.png` (`t = 3.17 s`), the `PIA07232` portrait inset (`CROP = (116, 32, 430, 661)`, `314×629` native interior pixels resized to `449×900` px via `LANCZOS`, `max_upscale = 1.4308426073× <= 1.44× <= 2.0×`) is byte-identical to the `J2296`-reviewed overlay (`overlay_sha256: 5f96154e31069b3ad3f5cd30fc9b476edbd770a728fc5cb3d45395103cf8ebc8`).
   - All white publication borders remain cropped out, and the soft 2005 Huygens DISR surface image is presented honestly as an archival portrait inset without synthetic sharpening, painted pixels, or excessive upscaling.
2. **Bracket Progression & Subject-Safe Registration:**
   - **`frame_012.png` (`t = 0.40 s`, SHA-256 `dc33974e3f6af0aa11e74a4ddd17121eb8fd291f2c1ae9c039f48f475d3298f5`):** End of the `0.0–0.4 s` alpha fade-in (`opacity = 1.0`, `p = 0.0`). The `449×900` inset, white leader line `(456.78, 605.46) → (780, 605.46) → (820, 410)`, `ABOUT 15 CENTIMETRES`, `PEBBLES`, and `ESA/NASA/JPL/University of Arizona` credit are cleanly established before the `GOLD` bracket begins drawing.
   - **`frame_054.png` (`t = 1.80 s`, SHA-256 `ac6316fda052e072ad60afc8fafe5a95cbc6dd78d4df8714fef0a9071a3e9ee9`):** Bracket extension at `p = (1.80 - 0.40) / 1.60 = 0.875` (`87.5%`). The left vertical tick at `x = 265.76, y = 593.46..617.46` and horizontal `GOLD` bar (`y = 605.46`, `44 px` above the left cobble's `y = 649.46` midline) draw smoothly across the dark riverbed strip above the left elongated foreground cobble.
   - **`frame_072.png` (`t = 2.40 s`, SHA-256 `6d7ec4e623fa1cc710c676cf07b787b63c1e0df46ea0cc429ca3124c1e8027db`):** Full bracket hold (`p = 1.0`, `opacity = 1.0`). Both left (`x = 265.76`) and right (`x = 438.78`) end ticks bracket the exact left foreground cobble identified as `"about 15 centimetres (left)"` in `01_Script/SOURCES.md` v01 Row 8 (`https://www.esa.int/media/first-colour-view-of-titan-s-surface`), leaving the cobble itself completely unobstructed.
   - **`frame_095.png` (`t = 3.17 s`, SHA-256 `e371a65756c76446dab3b56595f9a5b4223d07e32e41f64bbe5d084d9c7fd816`):** Late hold just before the `3.20–3.60 s` fade-out, with the background pan at `x = 21 px` of `24 px` and zero visual drift or registration loss on the foreground inset or labels.

### B. Background Style Decision: Same-Source Feathered/Blurred Graded `PIA07232` vs Separate Plate (`KEEP`)
1. **Why the Subdued Same-Source Feathered/Blurred Background Fits the House Style:**
   - **Rule Compliance (`AGENTS.md` Standing Lesson 2 & *Teach on screen*):** Standing Lesson 2 (*Edit (v03b)*) explicitly authorises feathered-blur 16:9 fill for non-16:9 archival stills (`"fill 16:9 (feathered blur OK); upscale ≤~2.35×"`), and *Teach on screen* requires that overlays *"ride over moving or blurred real picture, never a flat black slab or an empty black panel, and the frame passes polish_gate's near-black check"*.
   - **Visual Separation & Legibility:** Because the `449×900` `PIA07232` inset on the left is already a detailed orange-amber surface photograph and the right two-thirds of the canvas (`x = 456..1570`) carry the white callout leader line, `ABOUT 15 CENTIMETRES`, `PEBBLES`, and agency credit, placing a second sharp high-detail plate behind the inset would create competing horizon/feature lines behind the leader line and typography. The heavily blurred (`GaussianBlur(65)`), `72%` navy-graded (`(37, 52, 73)`) surround provides a warm slate-amber atmospheric tone (`mean RGB ≈ [77.0, 74.9, 74.6]`) that harmonises with the golden Huygens inset while keeping the right-hand teaching area clean and high-contrast:
     - `WHITE` (`#F5F7FA`) vs right-hand background (`rel_lum = 0.0709`): **`8.09:1`** (`≥ 4.5:1` PASS)
     - `GOLD` (`#FFB347`) vs right-hand background (`rel_lum = 0.0709`): **`4.87:1`** (`≥ 4.5:1` PASS), and **`9.59:1`** against its `3 px` dark navy stroke (`(20, 28, 42)`)
   - **Gradient Banding & Near-Black Compliance (`Polish pass` 3):** Adding deterministic `±2` fine grain after alpha compositing (`rng = np.random.default_rng(2089 + i)`) prevents 8-bit `yuv420p` banding across the soft background gradient, and every frame (`i = 0..107`) stays well clear of `polish_gate.py`'s near-black floor (`frame_luma_min = 75.91 >= 28.0`, `p95_min = 80.85 >= 50.0`).
   - **Zero Extra Source Appearance (`MAX_REUSE = 2` Preserved):** Using `PIA07232` as its own defocused 16:9 pillarbox fill within Row 18 introduces no third source asset and keeps `PIA07232` strictly at **2 film-wide appearances** (`R18` Use 1 of 2 and `R20` Use 2 of 2, separated by Row 19's `12.60 s > 10 s`). Note that back-to-back cuts of `PIA07232` within Row 18 (`172.16–183.54 s`) count as a single appearance under `scripts/picture_qa.py`, while neighbouring rows (`R17` `PIA07236` aerial channels and `R19` `PIA14909`/Cassini plate) supply distinct imagery before and after Row 18.

### C. Independent Verification of Tool Metrics & Preserved Exports (`VERIFIED`)
1. **Hashes & Stream Properties (`R18_COMPOSITE_PREVIEW_v01.json` & `R18_COMPOSITE_VERIFICATION_v01.json`):**
   - `source_sha256` (`PIA07232.jpg`): `4221ee7a4588a6ea169a0b438b5526e26c68827cb717a31ef1f81284b39cd3e8` (`MATCH`)
   - `overlay_sha256` (`code_graphic_032_r18_ruler_v01.mov`): `5f96154e31069b3ad3f5cd30fc9b476edbd770a728fc5cb3d45395103cf8ebc8` (`MATCH`)
   - `video` (`032_r18_composite_preview_v01.mp4`): `c5e70b74ec76f4af9ee0dc3bfba076be9803aac535b6397ca993db132588712d` (`1920×1080`, `h264` High, `yuv420p`, `30/1 fps`, `108` frames, `3.600000 s`, video-only `-an`, full `ffmpeg` decode exit `0`)
   - `polish_gate.py` (`scripts/polish_gate.py ... --cuts R18_COMPOSITE_CUTS_v01.json`): `polish gate PASS: 0 of 1 rows failed, 0 to look at` (`std = 36.14`, `mean = 93.8`, `p95 = 174.0`, `edge = 0.0227`, `hf = 9.43`, `lf = 32.6`, `std8 = 33.54`, `edge8 = 0.0842`, `seams = []`, `jitter.fail = false`).
2. **All 62 Prior `.mov` Exports Unchanged:**
   - Verified all **62** export SHA-256s in `J2089_EXPORT_HASHES_v22.json` and ran `verify_reviewed_exports.py --review-root /Users/benjaminoats/YouTube/orbit-with-ben` (`108 exact decoded frames` across all 21 registered custom/reviewed graphic scripts).

---

## 3. Preserved Holds & Next Steps for Parent `J2089` (`1/4`, `£0`)

1. **Candidate Layout `KEEP` Scope:**
   - `032_r18_composite_preview_v01.mp4` (`c5e70b74ec76f4af9ee0dc3bfba076be9803aac535b6397ca993db132588712d`) and its recipe in `composite_r18_preview.py` are **`KEEP`** for the `3.6 s` Row 18 measurement beat (`177.0–180.6 s` proposal around *"scattered with rounded pebbles up to about fifteen centimetres across"* within Row 18's `172.16–183.54 s` span).
   - Because this `3.6 s` clip is a silent video-only (`-an`) segment candidate, **never ship `032_r18_composite_preview_v01.mp4` standalone**; integrate it into Row 18 during full timeline assembly with locked VO (`titan_landing_vo_v02b`), music bed, and house SFX (`tick_ink` / subtle tick under `sfx_kit.py level`).
2. **All Film-Stage & Asset Holds Remain in Force:**
   - **Inherited Public-Push Restriction Respected:** Keep `/private/tmp/codex-J2089` (`worker/J2089-r18-ruler`) local; do not push that worktree to `origin` without explicit push clearance.
   - **Not Native Motion:** The `24 px` decorative pan over a blurred still is not native moving footage and does not satisfy or release the Row 1 Frame-0 native-motion / Chief fallback hold (`J2177`).
   - **Per-Asset Rights Holds Preserved:** `PIA07232` (`ESA Standard Licence` / JPL image-use policy) and all `JHUAPL` Dragonfly animation rows (`J2089_CHECKPOINT_v05.md`) retain their per-asset rights clearance holds before final cut release.
   - **Huygens DISR Mosaic Hold Preserved:** `PIA07870` and `PIA07871` (`R16`/`R51`) remain blocked from assembly pending seam/detail resolution (`J2089_CHECKPOINT_v18.md`).
   - **Final Gates Preserved:** Short `RLSJm59OSzI` frame exclusion, film-wide `≤ 2`-appearance enforcement (`PIA07232` strictly `R18 + R20`), neighbouring real moving imagery, full-cut `picture_qa.py`, `polish_gate.py`, `music_gate.py`, `sfx_kit.py level`, and `clip_check.py` remain required on the assembled film. Parent `J2089` remains at milestone `1/4` (`£0` spent).
