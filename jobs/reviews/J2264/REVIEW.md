# J2264: 032 R35 ocean-section still and source-allocation review (`J2089` / `f01ef6a65d`)

6 Nov 2026 · Gemini (`gemini-argon`, Mini review lane) · £0.

Reviewed `ocean_graphic.py`, `verify_ocean_graphic.py`, `OCEAN_MANIFEST_v01.json`, `OCEAN_CHECKS_v01.json`, `J2089_OCEAN_REVIEW_REQUEST_v01.md`, and `J2089_CHECKPOINT_v13.md` at local commit `f01ef6a65d5812c6780c828488d0aabb7da43923` (`worker/J2089-ocean` in `/private/tmp/J2089-ocean-wt`), together with the full-size review still `/Users/benjaminoats/_desk/cache/J2089/ocean_previews_v01/r35_ocean_review.jpg` and transparent PNG `code_graphic_032_r35_ocean_v01.png`, against `01_Script/titan_landing_script_master_v02.md`, `01_Script/SOURCES.md` (row 13), `02_Voiceover/stt/titan_landing_vo_v02b/stt_raw.json` (Row 35, `373.10–385.06 s`), `07_Edit-Project/SHOT_LIST_v04.md` (Row 35), and `07_Edit-Project/HARVEST_POOL_v01.json`.

This is an individual still-frame review and `PIA14602` source-allocation ruling only; it is not motion perception, final composite contrast verification, or film-stage PASS.

---

## 1. Verdict Summary

1. **R35 Ocean Cross-Section Still (`r35_ocean`, `code_graphic_032_r35_ocean_v01.png`, SHA-256 `20d31824409e835a4c9742e620907bd0fc07d4c94a16d45817634527323b3af4`) — `KEEP` as built.**
   - Accurately teaches the locked R35 spoken line (*"And far beneath Titan's icy crust, tens of kilometres down, Cassini's gravity measurements revealed a second, hidden ocean — of liquid water, likely mixed with salts and ammonia,"* `373.10–385.06 s`) and `SOURCES.md` row 13 (`https://science.nasa.gov/saturn/moons/titan/facts/`) and reads clearly at full size with the sound off.
   - Approved to render (`code_graphic_032_r35_ocean_v01.mov`, `3.6 s`, `30 fps`, `108` frames, `1920×1080` `qtrle` RGBA, `-an`) under `--approved r35_ocean --review-ref J2264` in a fresh version directory once the draft-only `--render` guard in `ocean_graphic.py` is replaced with the standard `qtrle` RGBA export block (matching `size_graphic.py` and `uranus_graphic.py`).
2. **Source Allocation for `PIA14602` in the Final `≤ 2`-Appearance Manifest:**
   - `PIA14602` (`"Hazy Orange Orb"`, `1024×1024`, SHA-256 `3e893445ca67c27e51975eec92f943d43f7bf79ca65a1659f315d390cb20faed`, credit `NASA/JPL-Caltech/Space Science Institute`) is allocated to **at most 2 appearances** across Film `032`:
     1. **Use 1 of 2 — Row 9 (`r09_sizes`, `68.98–79.82 s`, pending `J2247`):** natural-colour `TITAN 5,150 KM` full-disc globe alongside Moon (`PIA00405`, `3,475 km`) and Mercury (`PIA15162`, `4,879 km`).
     2. **Use 2 of 2 — Row 35 (`r35_ocean`, `373.10–385.06 s`, approved by `J2264`):** natural-colour `TITAN` (`480×480` px circular limb crop from `510×510` source crop `(265, 275, 775, 785)`, `upscale = 480 / 510 = 0.9412× ≤ 1.0×`) beside the magnified `ICY GROUND` (`55–80 KM BELOW`) / `LIQUID WATER` (`LIKELY SALTS + AMMONIA`) cross-section.
   - **No 3rd or 4th appearance of `PIA14602` in `R03` or `R19`:**
     - **Row 3 (`10.06–22.50 s`, Cut 2: *"Titan's glowing orange limb haze"*):** Use **`PIA21902`** (`"Twilight Haze"`, `997×1007`, SHA-256 `59d884af28ad86ef881bd76fb02248155a9351896fb5b3b1e5a17324258b7705`, credit `NASA/JPL-Caltech/Space Science Institute`) as **Use 1 of 2** (with `R11` `94.80–99.82 s` as Use 2 of 2). `PIA21902` directly depicts Titan's glowing orange-and-blue atmospheric limb haze, avoids repeating the full-disc `PIA14602` globe from `R09`/`R35`, and keeps both `PIA14602` and `PIA21902` within the `≤ 2` appearances rule. *(If `J2247` later replaces `PIA14602` in `R09`, `R03` + `R35` remains an equally compliant 2-use pair; under no circumstances may `PIA14602` appear in more than 2 rows.)*
     - **Row 19 (`184.60–197.20 s`, `r19_distance`, open under `J2260`):** Do **not** allocate a 3rd appearance of `PIA14602` to `R19` (`R19`'s spoken line *"Titan circles the Sun with Saturn, about nine and a half times farther out than Earth"* and `SHOT_LIST_v04.md`'s `Sun–Earth–Saturn scale line "9.5 AU (9.5× EARTH)"` do not require reusing the solo `PIA14602` globe).
   - **Row 35 Cut Structure (`373.10–385.06 s`):**
     - **Cut 1 (`373.10–381.46 s`, `8.36 s`):** Cassini VIMS global infrared view **`PIA20016`** (`"Peering Through Titan Haze"`, `2002×2002`, SHA-256 `966212365538525eccbc3c55334a86f53e962a5991b57f0d3dc8582022ad69d8`, credit `NASA/JPL/University of Arizona/University of Idaho`, with J2090 disclosure tag `"INFRARED VIEW"`, used only in R35).
     - **Cut 2 (`381.46–385.06 s`, `3.60 s`):** `r35_ocean` (`code_graphic_032_r35_ocean_v01.mov`) composited over a graded moving background plate with corner credit `NASA/JPL-Caltech/SSI`.

---

## 2. Direct Verification Evidence

### A. Full-Size Still Inspection, Source Provenance & Scale
- **Source (`PIA14602`):** Verified NASA/JPL-Caltech/Space Science Institute Cassini ISS natural-colour image (`1024×1024`, `29,547` bytes, SHA-256 `3e893445ca67c27e51975eec92f943d43f7bf79ca65a1659f315d390cb20faed`), matching `HARVEST_POOL_v01.json` and `OCEAN_MANIFEST_v01.json`.
- **Crop & Downscale (`CROP = (265, 275, 775, 785)`):** Crops the `510×510` Titan globe, applies an inscribed circular limb mask (`ellipse((0, 0, 509, 509), fill=255)`), and downscales via `LANCZOS` to `480×480` px at `(120, 265)` (`upscale = 480 / 510 = 0.9412× ≤ 1.0×`, well below the `2.0×` warn / `2.35×` fail caps). Pixels are untouched (no synthetic texture, artificial shading, or planetary wedge slice drawn on the photograph).
- **Visual Inspection:** Directly inspected `/Users/benjaminoats/_desk/cache/J2089/ocean_previews_v01/r35_ocean_review.jpg` (`1920×1080` at `t = 2.0 s`), `code_graphic_032_r35_ocean_v01.png` (SHA-256 `20d31824409e835a4c9742e620907bd0fc07d4c94a16d45817634527323b3af4`), `PIA14602.jpg`, and `PIA20016.jpg`. The warm golden-orange Titan globe (`PIA14602`) on the left (`x = 120..600, y = 265..745`) connects via two gold zoom callout lines (`(555, 400)–(760, 285)` and `(555, 620)–(760, 815)`) to the magnified qualitative local cross-section (`x = 780..1295, y = 285..815`) on the right.

### B. Spoken Line, `SOURCES.md` Row 13 & Scientific Accuracy Check
- **Locked VO (`titan_landing_vo_v02b`, Row 35 `373.10–385.06 s`, `11.96 s`):**
  - `373.10–377.26 s`: *"And far beneath Titan's icy crust, tens of kilometres down,"*
  - `377.68–382.58 s`: *"Cassini's gravity measurements revealed a second, hidden ocean — of liquid water,"*
  - `383.04–385.06 s`: *"likely mixed with salts and ammonia."*
- **Source (`01_Script/SOURCES.md` row 13):**
  - `https://science.nasa.gov/saturn/moons/titan/facts/` — verbatim quotes:
    - *"The Cassini spacecraft's numerous gravity measurements of Titan revealed that the moon is hiding an underground ocean of liquid water (likely mixed with salts and ammonia)."*
    - *"an ocean 35 to 50 miles (55 to 80 kilometers) below the icy ground"*
- **Scientific & House-Style Verification:**
  1. **Depth semantics (`55–80 KM / BELOW`):** The gold vertical bracket (`x = 1330, y = 285..515`, with end ticks `x = 1320..1340`) spans strictly from the white top surface line (`y = 285`) down to the ice–water boundary (`y = 515`), matching NASA's `"55 to 80 kilometers below the icy ground"` (depth below surface / crust thickness, **never** the thickness of the ocean).
  2. **Open ocean bottom (no invented ocean thickness or core):** The lower `LIQUID WATER` block (`y = 515..815`, fill `(47, 145, 202, 200)`) has no bottom ocean-floor stroke or rocky core layer, avoiding any unsourced claim about ocean thickness or deep-interior structure.
  3. **Composition qualifier (`LIKELY SALTS / + AMMONIA`):** Explicitly retains NASA's `"likely"` qualifier (`font(43)`, `WHITE`, at `(820, 680)` and `(820, 738)`).
  4. **Qualitative schematic disclosure (`SCHEMATIC · NOT TO SCALE`):** Displayed at `(780, 880)` (`font(38)`, `WHITE`) so the magnified cross-section is never mistaken for a scale planetary radius cutaway.
  5. **Word-count cap (`≤ 4` words per label):** All 6 labels obey the `≤ 4`-word house rule: `TITAN` (`1` word), `ICY GROUND` (`2` words), `55–80 KM BELOW` (`3` words), `LIQUID WATER` (`2` words), `LIKELY SALTS + AMMONIA` (`4` words), and `SCHEMATIC · NOT TO SCALE` (`4` words excluding middle dot).

### C. Reproducible 109-Sample Structural & Safe-Area Verification
- Independently executed `python3 07_Edit-Project/verify_ocean_graphic.py --manifest 07_Edit-Project/OCEAN_MANIFEST_v01.json` in `/private/tmp/J2089-ocean-wt/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan`:
  - **Source & preview hashes:** `PIA14602.jpg` (`3e893445ca67...`) and `code_graphic_032_r35_ocean_v01.png` (`20d31824409e...`) match `OCEAN_MANIFEST_v01.json`, and `frame(2)` reproduces the exact RGBA bytes of `code_graphic_032_r35_ocean_v01.png`.
  - **Transparent endpoints:** `i = 0` (`t = 0.0 s`) and `i = 108` (`t = 3.6 s`) return `alpha_bounds = None` (`alpha = 0`).
  - **Safe area (`[96, 54, 1824, 1026]`):** All active frames `i = 1..107` stay strictly inside the 5% safe area (`alpha_bounds = [120, 265, 1618, 926]`).
  - **Monotonic build & animation:** `progress(t) = max(0, min(1, (t - 0.4) / 1.5))` increases monotonically over `t = 0.4..1.9 s` as the ocean fill and depth bracket animate in, `frame(0.8) != frame(1.4)`, and unapproved `--render` exits `2`.

---

## 3. Export Implementation & Preserved Holds for `J2089`

- **Export step for `J2089`:**
  - Replace the draft-only `--render` guard in `ocean_graphic.py` with the standard `ffmpeg` `qtrle` RGBA `.mov` export block (matching `size_graphic.py` and `uranus_graphic.py`), writing `code_graphic_032_r35_ocean_v01.mov` (`1920×1080`, `30 fps`, `108` frames, `3.6 s`, `qtrle` RGBA, `-an`) into a fresh output directory when invoked with `--render --approved r35_ocean --review-ref J2264`, and record the `.mov` path, SHA-256, and `review_ref: "J2264"` in `OCEAN_RENDER_MANIFEST_v01.json`.
- **Preserved exports and holds (unchanged by this review):**
  1. Preserve all **39** existing approved overlay, DATA, process, and Uranus exports.
  2. **`J2177`** retains the 17 mechanism-still review and the frame-0 native motion / R25 `PIA07232` 3-use conflict rulings.
  3. **`J2247`** retains the R09 diameter-comparison still review and `PIA15162` Mercury rights ruling.
  4. **`J2260`** retains the R19 distance-scale still review (with `PIA14602` excluded from `R19` per the `≤ 2`-appearance allocation above).
  5. **`J2262`** retains the R08 orbital-period clock still review and `PIA14922` (`R06` + `R08`) reuse ruling.
  6. **JHUAPL Dragonfly animation rights hold** (`J2089_CHECKPOINT_v05.md`) remains in force.
  7. **Local branch rule:** `/private/tmp/J2089-ocean-wt` (`worker/J2089-ocean` at `f01ef6a65d`) was not pushed and its inherited automatic-review public-push rejection is respected.
  8. **Composite & gate checks:** Final placement over a graded moving plate, corner agency credit (`NASA/JPL-Caltech/SSI`), `≥ 4.5:1` composite contrast, `≤ 2` still appearances across the final cut manifest, `picture_qa.py`, and `polish_gate.py` remain required at assembly. Parent `J2089` remains at `1/4` (`£0` spent).
