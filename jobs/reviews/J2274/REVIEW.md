# J2274 — Independent Review of OWB:032 Real Huygens Surface Thumbnail A v04 (`J2249`)

- **Date:** 2026-11-06
- **Reviewer:** `gemini` (Gemini 4 Argon, independent review lane — Rule H; builder `codex` did not review its own work)
- **Film / Stage:** `OWB:032` (*What Would Happen If You Landed on Titan?*) · `032 thumbs`
- **Reviewed Delivery:** `J2249` · PR #574 (`466352adfe01387c62cdc53662048171ef9242df`, `codex/j2249-real-surface`)
- **Governing Decisions & Rules:** `J2162` (`05_Analytics/tests/panels/owb-032-j2144/DECISION.md`), `05_Analytics/LEARNINGS.md` (Rules 12, 14, 19, 22), `00_Brand/Channel-Setup/THUMBNAIL_AND_TITLE_RULES.md` (§2, §2.A, §2.B), `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` (§8)
- **Spend:** £0 / 0 credits

---

## 1. Verdict Summary

| Item | Verdict | Summary |
|---|---|---|
| **Thumbnail Variant A v04 (`032_A_real_surface_v04.jpg`, SHA-256 `ba7662b11da2756759d2977af55ff793d9e128bb2fa8dd7141b571b95d27f489`)** | **`KEEP`** | Passes `HOOK`, `BAND`, `GRADE` (`saturation = 200.8`, `near_black = 0.016 / 1.6%`), `PHONE` (`168×94` and `360×202`), `J2162`, and `LEARNINGS.md` Rule 19 (*single real spacecraft frame, graded, 0–3 words, no composite*). Approved as the **third Test & Compare variant (Slot C)** behind Lead **B (`METHANE SHORE` v02)** and second slot **C (`ICE IS ROCK` v03)**. |
| **Intrinsic DISR Softness & `4.21×` Crop Enlargement (`304×171` → `1280×720`)** | **Resolved (`PASS` for Thumbnail Only; No Film QA Waiver)** | `PIA07232` is natively `546×693` with a `~314×628` interior photograph (`2005` Huygens DISR telemetry). At actual YouTube thumbnail browse sizes, the `304×171` crop scales **`0.55×` at `168×94`** and **`1.18×` at `360×202`** (both well within `≤ 2.35×`), where the foreground water-ice cobbles and crisp `1280×720` `REAL SURFACE` type read cleanly. The `≤ 2.35×` cap in `scripts/picture_qa.py` governs `1920×1080` moving film cuts, not `1280×720` still thumbnails; this ruling grants **no waiver or PASS** for `PIA07232` in `032 picture` / `032 edit`. |
| **Retained Variants B v02 & C v03 and Test & Compare Order (`J2162`)** | **`KEEP` (Unchanged; B Remains Lead)** | `032_B_bright_methane_shore_v02.jpg` (`4e4faf31...`) and `032_C_scale_ice_is_rock_v03.jpg` (`a0a67a7e...`) verified byte-identical on disk. Under `J2162`, **B (`METHANE SHORE` v02) remains the Lead (Studio Variant A)**, **C (`ICE IS ROCK` v03) is Studio Variant B**, and **`032_A_real_surface_v04.jpg` (`REAL SURFACE` v04) is Studio Variant C**. |

---

## 2. Verified Inputs & SHA-256 Hashes

All files in `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/09_Thumbnails/J2144_v02/` and PR #574 (`466352adfe`) were independently hashed and inspected:

| Asset / File | Dimensions / Spec | Verified SHA-256 | Status |
|---|---|---|---|
| `032_A_real_surface_v04.jpg` | `1280×720` JPEG | `ba7662b11da2756759d2977af55ff793d9e128bb2fa8dd7141b571b95d27f489` | Exact match to `MANIFEST_v04.json`; visually inspected at full `1280×720` |
| `PHONE_PREVIEW_v04.jpg` | `168×94` + `360×202` sheet | `1cb84dd4403e8274cb95232072f7f0892821da49c76075322cf4ea64bbd23bc2` | Exact match to `MANIFEST_v04.json`; visually inspected at phone & browse tile sizes |
| `MANIFEST_v04.json` | JSON manifest | `5d671b6882e31d3134aed080d75e9c8babfc5140e758ff1ac167b90721b7955c` | Byte-identical between local `09_Thumbnails/J2144_v02/MANIFEST_v04.json` and `466352adfe:jobs/reviews/J2249/MANIFEST_v04.json` |
| `PIA07232_surface_source.jpg` | `546×693` JPEG (`PIA07232`) | `e5be019e4175c1d81d61651ff77e83f070df6fc12cf09df52a11c9fe82282ee6` | Verified official NASA/JPL/ESA/University of Arizona Huygens DISR surface release (*First Color View of Titan's Surface*) |
| `032_B_bright_methane_shore_v02.jpg` | `1280×720` JPEG (Lead) | `4e4faf3155fba42aa7120a1682ba2d1eb46a95a0cc9a48fe5ac37a7bbfab02a0` | Unchanged byte-for-byte from `J2162`; visually re-verified |
| `032_C_scale_ice_is_rock_v03.jpg` | `1280×720` JPEG (Slot 2) | `a0a67a7e1f192d09aabeaa991c9f3f4ef064a2e81234f3a5b66c75de1be1c7af` | Unchanged byte-for-byte from `J2162`; visually re-verified |

---

## 3. Gate-by-Gate Thumbnail Evaluation (`THUMBNAIL_AND_TITLE_RULES.md` §2.B)

1. **SOURCE & PROVENANCE (`PASS`):**
   - Source asset `PIA07232` (`https://science.nasa.gov/photojournal/first-color-view-of-titans-surface/`) is the authentic single-frame ESA/NASA/University of Arizona Huygens Descent Imager/Spectral Radiometer (DISR) surface photograph acquired on 14 January 2005, colored from reflection spectra.
   - Credit (`NASA/JPL/ESA/University of Arizona`) and JPL image use policy (`https://www.jpl.nasa.gov/jpl-image-use-policy/`) are recorded in `MANIFEST_v04.json` to carry into the upload description.
   - Complies strictly with `LEARNINGS.md` Rule 19 (*"a single striking real spacecraft frame, graded, with 0-3 words, no composite"*) and `J2162` (*"rebuild it as the single real Huygens DISR surface photograph (the flood plain with rounded ice pebbles), graded, no composite (LEARNINGS rule 19, J2212), with the hook `REAL SURFACE`"*).

2. **HOOK (`PASS`):**
   - Hook text is **`REAL SURFACE`** (2 words), matching `J2162` verbatim.
   - Directly names the depicted object/scene, adds concrete documentary proof to the lead title (`"What Would Happen If You Landed on Titan?"`) without repeating `"Titan"` or any other title word (`THUMBNAIL_AND_TITLE_RULES.md` §2.3), and uses no vague teaser or threat framing.

3. **BAND (`PASS`):**
   - Single-line top band (`left_px: 60`, `visible_top_px: 42`, `visible_cap_height_px: 82` = `11.4%` of `720 px` frame height, within `THUMBNAIL_AND_TITLE_RULES.md` §2.A.3's `11–12%` target).
   - Deterministic `Arial Black` `112 px` with `5 px` `#20180f` outline; hook word **`REAL`** in house yellow (`#ffe347`) and **`SURFACE`** in white (`#ffffff`).
   - Completely clear of the hero foreground water-ice cobbles (`y ≈ 280–700`) and completely clear of the bottom-right YouTube duration badge corner.

4. **GRADE (`PASS`):**
   - Independently re-ran `/Users/benjaminoats/_desk/venvs/thumbs/bin/python 00_Brand/Channel-Setup/tools/thumb_preview.py long 032_A_real_surface_v04.jpg --out /tmp/j2274_preview_check.jpg --score`:
     - **`PASS  032_A_real_surface_v04.jpg  saturation=200.8  near_black=2%`** (`0.016` / `1.6%` exact).
   - Exceeds the `≥ 120` mean HSV saturation target (`≥ 100` floor) and stays well below the `≤ 30%` near-black cap (`THUMBNAIL_AND_TITLE_RULES.md` §2.B.3).

5. **PHONE (`PASS`):**
   - Direct visual inspection of `PHONE_PREVIEW_v04.jpg` at `168×94` and `360×202` confirms that **`REAL SURFACE`** reads at a glance with high stroke-to-background separation, and the central pair of rounded orange water-ice cobbles (`10–15 cm` cobbles on Titan's flood plain) occupies more than one-third of the frame with distinct sunlit highlights and dark crevices.

---

## 4. Explicit Resolution of Intrinsic DISR Softness & `4.21×` Crop Enlargement

1. **Why the `4.21×` enlargement is intrinsic to `J2162` and `LEARNINGS.md` Rule 19:**
   - The official NASA/JPL archival release of `PIA07232` is `546×693 px` including white publication margins; the usable interior DISR photograph is `~314×628 px` (the native resolution of the 2005 Huygens DISR surface sub-frame; no higher-resolution uncomposited single-frame exposure exists, as `PIA06438` is a descent mosaic and `PIA08115` is a multi-panel poster).
   - Because `LEARNINGS.md` Rule 19 and `J2162` prohibit compositing, blurred sidebars, or AI-generated detail, filling a `16:9` (`1280×720`) thumbnail from a single contiguous landscape crop (`crop_xyxy = [120, 330, 424, 501]`, `304×171 px`) necessarily requires a **`4.2105×` Lanczos resize** to the `1280×720` container.
   - Cropping to `y = 330..501` (excluding the distant upper horizon of the portrait frame) is the right compositional trade-off for a thumbnail: it makes the two rounded foreground water-ice cobbles large enough (`> 1/3` of the frame) to read as distinct 3D objects at `168×94` (`THUMBNAIL_AND_TITLE_RULES.md` §2.1 & §2.A.4).

2. **Why `032_A_real_surface_v04.jpg` complies with applicable thumbnail rules:**
   - The **`≤ 2.35×` upscale limit** (`AGENTS.md` Standing lessons 2 & 7, `docs/ORBIT_PLAYBOOK_LESSONS.md` §2, `STUDIO_PLAYBOOK.md` §7, `scripts/picture_qa.py`) is an **edit / `picture_qa.py` gate for `1920×1080` moving video cuts** held full-screen for `4–6 s`. Neither `THUMBNAIL_AND_TITLE_RULES.md` (§2, §2.A, §2.B) nor `STUDIO_PLAYBOOK.md` (§8) sets a `2.35×` source-crop cap on `1280×720` still thumbnails.
   - While `J2196` earlier declined `PIA07232` when applying the film upscale cap to the pre-panel `THIS IS TITAN` repair, acting-Chief synthesis **`J2162`** (`05_Analytics/tests/panels/owb-032-j2144/DECISION.md`, 5 Nov 2026) evaluated all three panel critiques of the `PIA21890` haze crop and explicitly directed building Variant A from the single real Huygens DISR surface photograph with the hook `REAL SURFACE`.
   - At actual YouTube thumbnail display sizes, the `304×171` source crop is scaled **`0.55×` at `168×94`** (phone search/compact feed) and **`1.18×` at `360×202`** (browse cards) — both below `1.2×` and well inside `2.35×`.
   - At full `1280×720` container size, the soft low-frequency pebble texture is honest 2005 spacecraft optics without AI hallucination, blocky JPEG artifacts, or oversharpening halos, while the vector `REAL SURFACE` hook is razor-sharp and immediately frames the historical photograph for the viewer.

3. **Strict Boundary — No Implied Waiver or Film Picture-QA PASS:**
   - This `KEEP` decision applies **exclusively** to thumbnail variant `032_A_real_surface_v04.jpg` as **Test & Compare Variant C (third slot)** for `OWB:032`.
   - It **does not waive** `scripts/picture_qa.py`'s `≤ 2.35×` upscale gate for `OWB:032` video assembly (`032 picture` / `032 edit`), and it **does not grant** a film picture-QA `PASS` for full-frame `4.21×` enlargement of `PIA07232` inside the `1920×1080` film master.

---

## 5. Approved `OWB:032` Thumbnail Set & Next Steps

Per `J2162` and this independent review (`J2274`), the `032 thumbs` stage is **approved (`done`)** with the following locked 3-way Studio Test & Compare line-up (to be armed when `OWB:032` is uploaded and has a video ID, logged via `thumb_ledger.py add` with tags `rule19,tentpole,rule14,rule12`):

1. **Studio Test Variant A (Lead):** `032_B_bright_methane_shore_v02.jpg` (`METHANE SHORE`, SHA-256 `4e4faf3155fba42aa7120a1682ba2d1eb46a95a0cc9a48fe5ac37a7bbfab02a0`)
2. **Studio Test Variant B (Slot 2):** `032_C_scale_ice_is_rock_v03.jpg` (`ICE IS ROCK`, SHA-256 `a0a67a7e1f192d09aabeaa991c9f3f4ef064a2e81234f3a5b66c75de1be1c7af`)
3. **Studio Test Variant C (Slot 3, Rule 19 Real Image):** `032_A_real_surface_v04.jpg` (`REAL SURFACE`, SHA-256 `ba7662b11da2756759d2977af55ff793d9e128bb2fa8dd7141b571b95d27f489`, credit `NASA/JPL/ESA/University of Arizona`)
