# J2247: 032 R09 diameter graphic still review and Mercury (`PIA15162`) source rights ruling (`J2089` / `2c9182cb31`)

6 Nov 2026 · Gemini (`gemini-argon`, Mini review lane) · £0.

Reviewed `size_graphic.py`, `verify_size_graphic.py`, `SIZE_MANIFEST_v01.json`, `SIZE_SOURCES_v01.json`, `SIZE_CHECKS_v01.json`, `J2089_SIZE_REVIEW_REQUEST_v01.md`, and `J2089_CHECKPOINT_v08.md` at `2c9182cb31` (`codex/J2089-size`), together with the full-size review still `/Users/benjaminoats/_desk/cache/J2089/size_previews_v01/r09_sizes_review.jpg`, transparent PNG `/Users/benjaminoats/_desk/cache/J2089/size_previews_v01/code_graphic_032_r09_sizes_v01.png`, and original NASA source assets (`PIA00405.jpg`, `PIA15162.jpg`, `PIA14602.jpg`), against `01_Script/titan_landing_script_master_v02.md`, `01_Script/SOURCES.md` (row 3), `02_Voiceover/stt/titan_landing_vo_v02b/stt_raw.json` (Row 9, `68.98–79.82 s`), `07_Edit-Project/SHOT_LIST_v04.md` (Row 9), and `07_Edit-Project/HARVEST_POOL_v01.json`.

This is an individual still-frame review and Mercury source-rights ruling only; it is not motion perception, final composite contrast verification, or film-stage PASS.

---

## 1. Verdict Summary

1. **R09 Diameter Comparison Still (`r09_sizes`, `code_graphic_032_r09_sizes_v01.png`, SHA-256 `c756e9d600b56a130d27e66f696900282b31f03f5a984baa88d93b7e1dcb41a3`) — `KEEP` as built.**
   - Accurately teaches the locked Row 9 spoken line (*"For nearly three hundred years, nobody could tell whether this distant moon had any air at all, even though it is bigger than our own Moon and wider than the planet Mercury,"* `68.98–79.82 s`) and `SOURCES.md` row 3 (`3,475 km`, `4,879 km`, `5,150 km`) and reads clearly at full `1920×1080` resolution with the sound off.
   - Approved to render (`code_graphic_032_r09_sizes_v01.mov`, `3.6 s`, `30 fps`, `108` frames, `1920×1080` `qtrle` RGBA, `-an`) in a fresh version directory under `--render --approved r09_sizes --review-ref J2247 --rights-ref J2247-MESSENGER-USAGE-STATEMENT`.
2. **Separate Mercury (`PIA15162`) Source Rights Ruling — `CLEARED` under the Official MESSENGER Mission Image Use Grant (`--rights-ref J2247-MESSENGER-USAGE-STATEMENT`), Without Relaxing the Dragonfly APL Hold:**
   - **`PIA15162` Mission Grant:** `PIA15162` (*"Mercury Globe: 0°N, 180°E"*, `2147×2147`, SHA-256 `ee40946826c057c4d5a9706391b0a4899c8013373506b445e3c2d31bbb0031c3`, `Center: JPL`, `Mission: MESSENGER`, credit `NASA/Johns Hopkins University Applied Physics Laboratory/Carnegie Institution of Washington`) is an official NASA Science Photojournal / Planetary Data System release (`https://science.nasa.gov/photojournal/mercury-globe-0n-180e/`, saved at `/Users/benjaminoats/_desk/cache/J2089/size_sources_v01/PIA15162_photojournal.html`, SHA-256 `b2e5c141a8623ef63efd3cbee9862abad56773a6e4fb5561b644f099d70032b9`).
   - That NASA Photojournal page explicitly points to the **MESSENGER Mission Image Use Policy (`https://messenger.jhuapl.edu/Explore/Usage-Statement.html`, saved at `/Users/benjaminoats/_desk/cache/J2089/size_sources_v01/messenger_usage_statement.html`, SHA-256 `0dbf20924ad998607cec98a981c091749e8a765ccd101c018477bf466e6b1ae1`)**, which grants permission verbatim:
     > *"Using MESSENGER Images: MESSENGER images are generally available for non-commercial educational and public information purposes, so long as their use does not convey NASA's, the Johns Hopkins University Applied Physics Laboratory's or Carnegie Institution of Washington's implicit or explicit endorsement of any goods or services. **No fee or written permission is required for their use, but please credit images to NASA/Johns Hopkins University Applied Physics Laboratory/Carnegie Institution of Washington (unless otherwise noted in the image caption). MESSENGER is a NASA mission and adheres to the space agency's guidelines for image use and reproduction.** Visit the NASA Web site 'Using NASA Imagery and Linking to NASA Web Sites' (http://www.nasa.gov/audience/formedia/features/MP_Photo_Guidelines.html) for more information..."*
   - Under NASA's **Images and Media Usage Guidelines (`https://www.nasa.gov/nasa-brand-center/images-and-media/`, saved at `/Users/benjaminoats/_desk/cache/J2089/size_sources_v01/nasa_media_policy.html`, SHA-256 `1709ad975d94437c9adba14f649af72a2649cab39312d6e532a98a556d3161ce`)** — which state that *"NASA content used in a factual manner that does not imply endorsement may be used without needing explicit permission"* and under *Commercial Use* that *"NASA imagery can be generally used editorially within published works that are not promotional in nature. If the NASA material is to be used for commercial purposes... it must not explicitly or implicitly convey NASA's endorsement of commercial goods or services"* — `PIA15162` is cleared for `r09_sizes` with required credit `NASA/JHUAPL/Carnegie Institution of Washington` (and full `NASA/Johns Hopkins University Applied Physics Laboratory/Carnegie Institution of Washington` in the upload description/credits).
   - **Why `PIA15162` is retained over Mariner 10 (`NASA/JPL`) alternatives:** Probed Mariner 10 photomosaics (`PIA03101` `2743×2086`, `PIA03103` `2158×3300`, `PIA03104` `2209×3303`, credited `NASA/JPL`); because Mariner 10 imaged only ~45% of Mercury in 1974–1975, every Mariner 10 mosaic is an incomplete half-disc or has a missing polar/terminator mosaic wedge unsuitable for a full-diameter sphere comparison, whereas `PIA15162` is a complete circular orthographic globe cleared under MESSENGER's dedicated mission image policy.
   - **Dragonfly `dragonfly.jhuapl.edu` Hold Unchanged:** This mission grant applies strictly to MESSENGER Photojournal release `PIA15162` under `messenger.jhuapl.edu/Explore/Usage-Statement.html`. It does **not** override or relax the `J2089_CHECKPOINT_v05.md` rights hold on `DragonflyatTitan2025.mp4` from `dragonfly.jhuapl.edu`, which is not a NASA Photojournal `PIA` release, has an empty credit field, and links only to `jhuapl.edu/privacy`.

---

## 2. Direct Verification Evidence

### A. Full-Size Still Inspection, Limb Crops & Source Provenance
- Directly inspected `/Users/benjaminoats/_desk/cache/J2089/size_previews_v01/r09_sizes_review.jpg` (`1920×1080` at `t = 1.8 s`), `code_graphic_032_r09_sizes_v01.png` (SHA-256 `c756e9d600b56a130d27e66f696900282b31f03f5a984baa88d93b7e1dcb41a3`), and the three original source files:
  1. **MOON (`PIA00405`, `3,475 km`):** NASA Galileo natural-colour image (`1986×1986`, `408,513` bytes, SHA-256 `fc93286c2d73a64f2b095c2e1f1df867b0e96ad0b9515987f9b38fd2ed91a641`, credit `NASA/JPL/USGS`, single appearance in `R09`). Crop `[0, 0, 1986, 1986]` (`1986×1986` px) downscaled via `LANCZOS` to `317×317` px (`upscale = 317 / 1986 = 0.1596× <= 1.0×`).
  2. **MERCURY (`PIA15162`, `4,879 km`):** NASA MESSENGER MDIS orthographic global mosaic (`2147×2147`, `881,547` bytes, SHA-256 `ee40946826c057c4d5a9706391b0a4899c8013373506b445e3c2d31bbb0031c3`, credit `NASA/JHUAPL/Carnegie Institution of Washington`, single appearance in `R09`). Crop `[95, 95, 2052, 2052]` (`1957×1957` px around the `[96, 96, 2054, 2055]` sunlit limb) downscaled via `LANCZOS` to `445×445` px (`upscale = 445 / 1957 = 0.2274× <= 1.0×`).
  3. **TITAN (`PIA14602`, `5,150 km`):** NASA Cassini ISS natural-colour image (`1024×1024`, `29,547` bytes, SHA-256 `3e893445ca67c27e51975eec92f943d43f7bf79ca65a1659f315d390cb20faed`, credit `NASA/JPL-Caltech/Space Science Institute`, **Use 1 of 2** in `R09`, paired only with **Use 2 of 2** in `R35` `r35_ocean` per `J2264`). Crop `[265, 275, 775, 785]` (`510×510` px around the `[263, 274, 777, 786]` visible haze limb) downscaled via `LANCZOS` to `470×470` px (`upscale = 470 / 510 = 0.9216× <= 1.0×`).
- All three globes retain their authentic photographic pixels (Moon/Mercury crater and mosaic texture, Titan's natural atmospheric haze softness where the visible haze limb represents Titan's nominal `5,150 km` surface diameter) with circular alpha limb masks (`ellipse((0, 0, w-1, h-1), fill=255)`) and zero synthetic surface textures.

### B. Spoken Line, `SOURCES.md` Row 3, Linear Scale & House Style Check
- **Locked VO (`titan_landing_vo_v02b`, Row 9 `68.98–79.82 s`, `10.84 s`):**
  - `68.98–74.72 s` (`5.74 s`, Cut 1): *"For nearly three hundred years, nobody could tell whether this distant moon had any air at all,"* → Cassini distant Titan crescent plate **`PIA08733`** (*"Titan Crescent View"*, Use 1 of 2, separating `R08`'s `orbit16` graphic from `R09`'s `r09_sizes` graphic).
  - `75.40–79.82 s` (`4.42 s`, Cut 2): *"even though it is bigger than our own Moon and wider than the planet Mercury."* → **`r09_sizes`** (`3.60 s`) composited over the continuing graded moving background plate.
- **Source (`01_Script/SOURCES.md` v01 row 3):**
  - `https://science.nasa.gov/saturn/moons/titan/facts/` (*"Titan is bigger than Earth's moon, and larger than even the planet Mercury"*), `https://www.esa.int/Science_Exploration/Space_Science/Cassini-Huygens/Facts_about_Titan` (`"Diameter (surface): 5150 km"`), and `https://nssdc.gsfc.nasa.gov/planetary/factsheet/index.html` (`"Diameter (km) | MERCURY: 4879 | MOON: 3475"`).
- **Common Linear Scale & Word-Count Cap:**
  - At full growth (`t >= 1.6 s`, `growth = 1.0`), `diameters(1.8) = [317, 445, 470]` px (`round(470 * km / 5150)`), matching the exact horizontal white caliper brackets (`y = 765`, end ticks `y = 755..775`) beneath each globe at `x = 380, 950, 1520`.
  - All 7 on-screen text strings obey the `≤ 4`-word house rule: `DIAMETER` (`1` word), `MOON` (`1` word), `3,475 KM` (`2` words), `MERCURY` (`1` word), `4,879 KM` (`2` words), `TITAN` (`1` word), and `5,150 KM` (`2` words).

### C. Reproducible 109-Sample Structural & Safe-Area Verification
- Independently executed `/Users/benjaminoats/_desk/venv-graphics/bin/python verify_size_graphic.py --manifest SIZE_MANIFEST_v01.json`:
  - **Source & preview hashes:** `PIA00405.jpg`, `PIA15162.jpg`, `PIA14602.jpg`, and `code_graphic_032_r09_sizes_v01.png` match `SIZE_MANIFEST_v01.json`.
  - **Transparent endpoints:** `i = 0` (`t = 0.0 s`) and `i = 108` (`t = 3.6 s`) return `bbox = None` (`alpha = 0`).
  - **Safe area (`[95, 54, 1825, 1026]`):** All active frames `i = 1..107` stay strictly inside the 5% safe area (`bbox = [121, 111, 1756, 938]` at peak growth).
  - **Invariant ratios & animation:** `abs(diameter - diameters[-1] * km / 5150) < 1` across all 109 samples (`[228, 321, 338]` px at `i = 0` growing smoothly to `[317, 445, 470]` px by `i = 48` / `t = 1.6 s`), `frame(0.7) != frame(1.5)`, and unapproved `--render` exits `2`.

---

## 3. Exact Render Command & Preserved Holds for `J2089`

- **Exact render command for `J2089` (using the house Pillow 12.3.0 venv in a fresh version directory):**

```bash
/Users/benjaminoats/_desk/venv-graphics/bin/python 02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/size_graphic.py \
  --out /Users/benjaminoats/_desk/cache/J2089/size_renders_v01 \
  --render \
  --approved r09_sizes \
  --review-ref J2247 \
  --rights-ref J2247-MESSENGER-USAGE-STATEMENT
```

- **Preserved exports and holds (unchanged by this review):**
  1. Preserve all **39** existing approved overlay, DATA, process, and Uranus exports.
  2. **`J2177`** retains the 17 mechanism-still review (`15 KEEP`, `2 FIX` on `r10_spectrum` and `r32_scalemap`) and the frame-0 native motion / R25 `PIA07232` 3-use conflict rulings.
  3. **`J2264`** retains the `r35_ocean` `KEEP` approval and the 2-use cap on `PIA14602` (`R09` Use 1 of 2 + `R35` Use 2 of 2; excluded from `R03` and `R19`).
  4. **`J2260`** (`r19_distance` still) and **`J2262`** (`r08_orbit_period` still + `PIA14922` `R06`+`R08` reuse) remain with their respective review jobs.
  5. **JHUAPL Dragonfly animation rights hold** (`J2089_CHECKPOINT_v05.md`) remains in force.
  6. **Composite & gate checks:** Final placement over a graded moving plate (`PIA08733` in R09), corner agency credits (`NASA/JPL/USGS · NASA/JHUAPL/CIW · NASA/JPL-Caltech/SSI`), `≥ 4.5:1` composite contrast, `≤ 2` still appearances across the final cut manifest, `picture_qa.py`, and `polish_gate.py` remain required at assembly. Parent `J2089` remains at `1/4` (`£0` spent).
