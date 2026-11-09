# J2260 — Film 032 Row 19 (`r19_distance`) Distance Draft Still & `PIA14602` Reuse Review

- **Job:** `J2260` (`032 R19 distance draft: review still and reuse`)
- **Parent Job:** `J2089` (`OWB 032: harvest licensed footage and render code graphics`, `1/4`)
- **Film:** `OWB:032` (`02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan`)
- **Reviewer:** `gemini` (specialist worker; still-image visual review + structural/reuse audit — not Chief final `OK`, not moving-video `PASS`)
- **Reviewed Worktree & Commit:** `/private/tmp/J2089-distance-wt` (`codex/J2089-distance` at local commit `c7a06bd8746404792154c1b1c6c390d32c95e4a3`)
- **Reviewed Artefacts:**
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/J2089_DISTANCE_REVIEW_REQUEST_v01.md`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/distance_graphic.py`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/verify_distance_graphic.py`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/DISTANCE_MANIFEST_v01.json`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/DISTANCE_CHECKS_v01.json`
  - `/Users/benjaminoats/_desk/cache/J2089/distance_previews_v01/r19_distance_review.jpg` (`1920×1080`, inspected full size)
  - `/Users/benjaminoats/_desk/cache/J2089/distance_previews_v01/code_graphic_032_r19_distance_v01.png` (`1920×1080` RGBA at `t = 2.4 s`, `preview_sha256: 0e0a54c0502f326fe5f0a549e177d6cb9fb8f399b551159bc23f10cbd6a2b60a`, inspected full size)
  - Pre-verified `< 2`-use Cassini Titan source-swap stills at `t = 2.4 s` (`1920×1080`, inspected full size):
    - Primary swap (`PIA14909`): `preview_sha256: 273b19ebae1b316a8c859550d0df0a6dcbee23ef6c3be91ef829e547687e1d6f` (`source_sha256: b72f5371622b0197f91a70a62b729e1e854dd91c511639f8055cf3d93f70ce74`)
    - Secondary swap (`PIA21610`): `preview_sha256: ec18f2b771e582952c7ce0c3ec46d814966e954eddf4653619b242bac7151d80` (`source_sha256: 16002a7019b80437475ed9dce93d818f7319bd0e51f3b4e9ac2a6e39eda6e620`)

---

## 1. Verdict Summary

| Item | Ruling | Summary |
|---|---|---|
| **1. Treatment vs Three-Body Scale Line (`r19_distance`)** | **`KEEP` / `APPROVED`** | The linear 2-bar heliocentric AU distance comparison (`DISTANCE FROM SUN` header; `EARTH 1 AU` vs `TITAN 9.5 AU` linear bars sharing `900 / 9.5 = 94.73684 px/AU` from zero; `9.5× EARTH’S DISTANCE` scale callout; real circular-cropped Cassini Titan globe on the left) **satisfies Row 19 (`184.60–197.20 s`) and is approved over the shot-list's `Sun–Earth–Saturn` three-body scale line**. |
| **2. `PIA14602` Reuse Allocation (`R03` / `R09` / `R19` / `R35`) & `R19` Source Swap** | **`KEEP` with `PIA14909` (or `PIA21610`) source swap — approved to render under `--approved r19_distance --review-ref J2260`** | Under `J2247` (`ce9282cb61`) and `J2264` (`8696af1d91`), `PIA14602` (`"Hazy Orange Orb"`) is already locked and rendered at its **maximum 2 appearances** across Film `032` (**Row 9 `r09_sizes` Use 1/2** + **Row 35 `r35_ocean` Use 2/2**, with Row 3 Cut 2 reassigned to `PIA21902` Use 1/2). Using `PIA14602` in Row 19 would create a **3rd appearance** (`R09`, `R19`, `R35`), which hard-FAILs `scripts/picture_qa.py` (`MAX_REUSE = 2`). Swap `SOURCE` and `CROP` in `distance_graphic.py` to **`PIA14909`** (`0` uses elsewhere; true-colour orange Titan globe; `preview_sha256: 273b19ebae1b316a8c859550d0df0a6dcbee23ef6c3be91ef829e547687e1d6f`) or **`PIA21610`** (`1` use elsewhere in `R28`; `<= 1.0×` downscale; `preview_sha256: ec18f2b771e582952c7ce0c3ec46d814966e954eddf4653619b242bac7151d80`) and render `code_graphic_032_r19_distance_v01.mov` under `--approved r19_distance --review-ref J2260`. |

---

## 2. Detailed Decisions & Rationale

### A. Decision 1 — Why the Linear 2-Bar Heliocentric AU Comparison Is Approved Over the Three-Body `Sun–Earth–Saturn` Scale Line

1. **Exact Match to Locked VO (`titan_landing_vo_v02b`) and `01_Script/SOURCES.md` Row 8:**
   - **Locked Row 19 VO (`184.60–197.20 s`, `12.60 s`):**
     - `184.60–186.62 s`: *"Except those pebbles are not stone."*
     - `187.30–192.36 s`: *"Out at Titan's distance from the Sun — about nine and a half times farther out than Earth —"*
     - `192.90–197.20 s`: *"the surface sits at minus one hundred and seventy-nine degrees Celsius."*
   - **Governing `01_Script/SOURCES.md` v01 Row 8:**
     - Claim: *"About nine and a half times farther from the Sun than Earth; −179 °C..."*
     - Exact verbatim quote (`https://science.nasa.gov/saturn/moons/titan/facts/`): *"Titan is about 886 million miles (1.4 billion kilometers) from the Sun, or about 9.5 astronomical units (AU)."*
   - The spoken sentence in Row 19 compares **Titan's distance from the Sun** directly against **Earth's distance from the Sun** (`1 AU` vs `9.5 AU`, `"about nine and a half times farther out than Earth"`). It never speaks the word `"Saturn"` in Row 19.

2. **Mute-Test Clarity & `AGENTS.md` Lesson 7 Compliance:**
   - On a `1920×1080` canvas, a literal three-body `Sun–Earth–Saturn` diagram cannot simultaneously keep true body diameters and true `1 : 9.5` heliocentric orbital spacing without either (a) shrinking Earth and Titan below `1 px` at true scale, or (b) drawing a non-scale schematic with flat schematic circles/discs, which violates `AGENTS.md` Lesson 7 (*"Real bodies, not flat discs... FAIL: a computer model or reconstruction, simulation, diagram, chart, schematic or labelled image"*).
   - By pairing a real circular-cropped Cassini ISS Titan globe on the left (`460×460` px at `(170, 250)` with label `TITAN` at `(400, 770)`) with a linear 2-bar heliocentric distance comparison on the right (`DISTANCE FROM SUN` at `(830, 150)` in `GOLD` `54 pt`; `EARTH 1 AU` at `(830, 290)` above a `94.74 px` gold bar on a `900 px` track; `TITAN 9.5 AU` at `(830, 540)` above a full `900 px` gold bar on a `900 px` track; and `9.5× EARTH’S DISTANCE` at `(830, 810)` in `WHITE` `54 pt`), the graphic communicates the exact `1 : 9.5` scale comparison with the sound off while keeping a real NASA body on screen.

3. **House Type & `<= 4`-Word Label Lock:**
   - Every text element uses `HelveticaNeue.ttc` bold (`index=1`) and obeys the `≤ 4`-word house rule:
     - `TITAN` (`1` word, `52 pt` `WHITE`, anchor `mm` at `(400, 770)`)
     - `DISTANCE FROM SUN` (`3` words, `54 pt` `GOLD` `#FFB347`, at `(830, 150)`)
     - `EARTH 1 AU` (`3` words, `56 pt` `WHITE`, at `(830, 290)`)
     - `TITAN 9.5 AU` (`3` words, `56 pt` `WHITE`, at `(830, 540)`)
     - `9.5× EARTH’S DISTANCE` (`3` words, `54 pt` `WHITE`, at `(830, 810)`)

---

### B. Decision 2 — `PIA14602` Reuse Allocation Across `R03` / `R09` / `R19` / `R35` & Pre-Verified Source Swap for `R19`

1. **Film-Wide `PIA14602` Allocation Under `J2247` (`ce9282cb61`) and `J2264` (`8696af1d91`):**
   - `AGENTS.md` Lesson 7 and `scripts/picture_qa.py` (`MAX_REUSE = 2`) enforce a hard FAIL if any still source appears in more than **2 non-adjacent stretches** across the film.
   - Across Film `032`, `PIA14602` (`"Hazy Orange Orb"`, `1024×1024`, `source_sha256: 3e893445ca67c27e51975eec92f943d43f7bf79ca65a1659f315d390cb20faed`) is already allocated and rendered (`J2089` checkpoint v14 `21cdd87bb5`) in two non-adjacent rows:
     - **Use 1 of 2 — Row 9 (`r09_sizes`, `68.98–79.82 s`):** Approved by `J2247` (`ce9282cb61`) and rendered at `/Users/benjaminoats/_desk/cache/J2089/size_renders_v01/code_graphic_032_r09_sizes_v01.mov` (`SHA-256: 29489143929ac689b80d7e39d8fd73ba715d0f2705a21d06675b91a9bcdecf32`).
     - **Use 2 of 2 — Row 35 (`r35_ocean`, `373.10–385.06 s`):** Approved by `J2264` (`8696af1d91`) and rendered at `/Users/benjaminoats/_desk/cache/J2089/ocean_renders_v01/code_graphic_032_r35_ocean_v01.mov` (`SHA-256: b3df01cf289c3b8e0ddac9966f0c9c6b435d3a7f57be5a68452db051cbcf9f61`).
     - **Row 3 (`17.08–26.90 s`, Cut 2):** Reassigned by `J2264` (`8696af1d91`) to `PIA21902` (*"Portrait of Titan"*, Use 1 of 2 in `R03`, paired with Row 11 Use 2 of 2).
   - Consequently, **Row 19 (`r19_distance`) MUST NOT use `PIA14602`**, because adding `PIA14602` at Row 19 (`184.60–197.20 s`) would create a 3rd appearance (`R09`, `R19`, `R35`).

2. **Pre-Verified `< 2`-Use Cassini Titan Source Swaps for `distance_graphic.py` (Approved to Render Immediately Under `--approved r19_distance --review-ref J2260`):**
   - To eliminate a second still-review round-trip and satisfy `verify_reviewed_exports.py` (`assert r['preview_sha256'] in review_text`), two already-harvested `< 2`-use Cassini ISS Titan globe stills on disk were tested in `distance_graphic.py` (`/Users/benjaminoats/_desk/venv-graphics/bin/python`, Pillow 12.3.0), inspected full size (`1920×1080`), and verified across all 109 sample timestamps (`0.00–3.60 s`). Either swap is approved to render under `--approved r19_distance --review-ref J2260`:

   #### Option 2A (Primary Recommended Swap — `PIA14909`, True-Colour Orange Titan Globe, `0` Uses Elsewhere in Film `032`)
   - **Why Recommended:** `PIA14909` (*"Titan Up Front"*, `https://science.nasa.gov/photojournal/titan-up-front/`, credit `NASA/JPL-Caltech/Space Science Institute`, metadata at `/Users/benjaminoats/_desk/cache/J2089/harvest_v01/PIA14909_metadata.json`) is a natural-colour Cassini narrow-angle camera image showing Titan's golden-orange atmosphere passing in front of Saturn and its rings (`993×1017` px, `0` uses elsewhere in Film `032`).
   - **Bonus Row 19 Plate Coherence:** In `SHOT_LIST_v04.md`, Row 19 calls for `"Cassini distant Saturn/Titan plate"` alongside the `r19_distance` overlay. Using the full `PIA14909.jpg` frame (`993×1017` px, `1.93× < 2.0×` upscale to `1920×1080`) as Row 19's underlying/adjacent Cassini Saturn-and-Titan plate and the circular crop of Titan (`408×408` px) inside `r19_distance` keeps both occurrences back-to-back within Row 19 (**1 appearance** under `picture_qa.py`, `0` uses in every other row).
   - **Exact Code Update in `distance_graphic.py`:**
     ```python
     SOURCE = Path('/Users/benjaminoats/_desk/cache/J2089/harvest_v01/PIA14909.jpg')
     CROP = (295, 294, 703, 702)
     ```
     *(With circular limb mask `mask_draw.ellipse((0, 0, src.width - 1, src.height - 1), fill=255)` = `(0, 0, 407, 407)` on the `408×408` crop, trimmed cleanly inside Titan's illuminated orange limb so Saturn's rings behind Titan are completely excluded, then resized via `Image.Resampling.LANCZOS` to `460×460` px at `(170, 250)`.)*
   - **Verified Metrics & Hashes (`PIA14909`):**
     - `source_id`: `PIA14909`
     - `source_path`: `/Users/benjaminoats/_desk/cache/J2089/harvest_v01/PIA14909.jpg`
     - `source_sha256`: `b72f5371622b0197f91a70a62b729e1e854dd91c511639f8055cf3d93f70ce74`
     - `crop_box`: `[295, 294, 703, 702]` (`408×408` px → `460×460` px, `max_upscale = 460 / 408 = 1.1274509803921569 < 2.0×`)
     - `preview_sha256` (`frame(2.4)` PNG): `273b19ebae1b316a8c859550d0df0a6dcbee23ef6c3be91ef829e547687e1d6f`

   #### Option 2B (Alternative Swap From `HARVEST_POOL_v01.json` — `PIA21610`, `<= 1.0×` Downscale, Use 1 of 2 Paired With Row 28)
   - **When to Use:** If the worker prefers a source already listed in `HARVEST_POOL_v01.json` (`harvest_v03`) with `<= 1.0×` downscale (`0.575×`), use `PIA21610` (*"Titan Northern Summer Clouds"*, `1121×1123` px, credit `NASA/JPL-Caltech/Space Science Institute`), which has only **1 other appearance** in Film `032` (Row 28 polar-cloud still, making `R19` + `R28` = **2 uses total**, `<= 2`).
   - **Exact Code Update in `distance_graphic.py`:**
     ```python
     SOURCE = Path('/Users/benjaminoats/_desk/cache/J2089/harvest_v03/PIA21610.jpg')
     CROP = (160, 161, 960, 961)
     ```
     *(With circular limb mask `mask_draw.ellipse((0, 0, src.width - 1, src.height - 1), fill=255)` = `(0, 0, 799, 799)` on the `800×800` crop, downscaled via `Image.Resampling.LANCZOS` to `460×460` px at `(170, 250)`.)*
   - **Verified Metrics & Hashes (`PIA21610`):**
     - `source_id`: `PIA21610`
     - `source_path`: `/Users/benjaminoats/_desk/cache/J2089/harvest_v03/PIA21610.jpg`
     - `source_sha256`: `16002a7019b80437475ed9dce93d818f7319bd0e51f3b4e9ac2a6e39eda6e620`
     - `crop_box`: `[160, 161, 960, 961]` (`800×800` px → `460×460` px, `max_upscale = 460 / 800 = 0.575 <= 1.0×`)
     - `preview_sha256` (`frame(2.4)` PNG): `ec18f2b771e582952c7ce0c3ec46d814966e954eddf4653619b242bac7151d80`

   #### Inspected `v01` Draft Hash (Layout/Geometry Approved; Do Not Assemble With `PIA14602` While `R09` + `R35` Use `PIA14602`)
   - `source_id`: `PIA14602` (`source_sha256: 3e893445ca67c27e51975eec92f943d43f7bf79ca65a1659f315d390cb20faed`)
   - `preview_sha256` (`code_graphic_032_r19_distance_v01.png` at `c7a06bd874`): `0e0a54c0502f326fe5f0a549e177d6cb9fb8f399b551159bc23f10cbd6a2b60a`

---

## 3. Direct Verification Evidence

### A. Full-Size Visual Inspection (`1920×1080`)
- Inspected `/Users/benjaminoats/_desk/cache/J2089/distance_previews_v01/r19_distance_review.jpg` and `/Users/benjaminoats/_desk/cache/J2089/distance_previews_v01/code_graphic_032_r19_distance_v01.png` at full resolution (`1920×1080`), as well as the full-size rendered `t = 2.4 s` replacement stills for `PIA14909` (`273b19ebae1b...`) and `PIA21610` (`ec18f2b771e5...`):
  - **Left hemisphere (`x = 170..630, y = 250..710`):** Clean `460×460` circular Cassini Titan disc with zero square-crop corners or edge artefacts, and `TITAN` centered underneath at `(400, 770)` (`y = 745..795`).
  - **Right comparison column (`x = 830..1730`):**
    - `DISTANCE FROM SUN` (`GOLD` `#FFB347`, `54 pt`, `y = 162..203`) sits cleanly at the top.
    - `EARTH 1 AU` (`WHITE`, `56 pt`, `y = 302..343`) sits above the first `900 px` reference track (`y = 390..434`), with the `GOLD` bar extending `94.74 px` (`x = 830..925`).
    - `TITAN 9.5 AU` (`WHITE`, `56 pt`, `y = 552..593`) sits above the second `900 px` reference track (`y = 640..684`), with the `GOLD` bar extending the full `900 px` (`x = 830..1730`).
    - `9.5× EARTH’S DISTANCE` (`WHITE`, `54 pt`, `y = 822..878`) sits cleanly below the second bar with no overlap or crowding.

### B. Reproducible 109-Sample Structural & Safe-Area Audit
Executed `/Users/benjaminoats/_desk/venv-graphics/bin/python verify_distance_graphic.py --manifest DISTANCE_MANIFEST_v01.json --out /private/tmp/test_distance_checks.json` (exit `0`, byte-identical to `DISTANCE_CHECKS_v01.json`) and ran the same 109-sample sweep (`i = 0..108`, `t = i / 30.0 s`) on both `PIA14909` and `PIA21610`:
- `samples`: `109` (`0.00 s` to `3.60 s` at `30 fps`)
- `transparent_endpoints`: `[true, true]` (`frame(0.0)` and `frame(3.6)` have `getbbox() is None`)
- `safe_area`: `[95, 54, 1825, 1026]` (`5%` horizontal, `5%` vertical margins on `1920×1080`)
- `max_bbox`: `[170, 162, 1731, 878]` — strictly inside `[95, 54, 1825, 1026]` across all 107 active samples (`min_x = 170 >= 95`, `min_y = 162 >= 54`, `max_x = 1731 <= 1825`, `max_y = 878 <= 1026`)
- `widths_at_2_4s`: `[94.73684210526316, 900.0]`, `ratio_at_2_4s = 9.5` (`abs(widths[1] / widths[0] - 9.5) < 1e-10` on every active frame)
- `unapproved_render_exit`: `2` (`distance_graphic.py --render` without approval refuses to write `.mov`)

---

## 4. Export Implementation Instructions & Preserved Holds for `J2089`

1. **Upgrade `distance_graphic.py` From Draft Guard to Reviewed Export Gate (`--approved r19_distance --review-ref J2260`):**
   - Apply the `SOURCE` and `CROP` swap (`PIA14909` primary or `PIA21610` alternative) with `mask_draw.ellipse((0, 0, src.width - 1, src.height - 1), fill=255)`.
   - Replace the unconditional draft-only `if args.render: raise SystemExit(...)` block with the standard `--approved r19_distance --review-ref J2260` `qtrle` RGBA `.mov` export pattern used in `ocean_graphic.py` and `orbit_period_graphic.py`, writing to a **fresh output directory**:
     - Render output: `/Users/benjaminoats/_desk/cache/J2089/distance_renders_v01/code_graphic_032_r19_distance_v01.mov`
     - Updated preview output (in a new preview dir or updated manifest): `/Users/benjaminoats/_desk/cache/J2089/distance_previews_v02/code_graphic_032_r19_distance_v01.png` (`273b19ebae1b...` or `ec18f2b771e5...`)
     - Register `r19_distance` in `verify_reviewed_exports.py` (`REVIEWS['r19_distance'] = ROOT / 'jobs/reviews/J2260/REVIEW.md'`) and `GRAPHICS_COVERAGE_v01.json` (`reviewed_rendered_rows: 17`, `draft_only_rows: 0`).

2. **Preserved Holds & Boundaries:**
   - **Do NOT push `/private/tmp/J2089-distance-wt` (`codex/J2089-distance`):** Its public branch push was rejected twice by automatic approval review; port the `distance_graphic.py` update cleanly into the active `J2089` integration worktree without pushing `codex/J2089-distance`.
   - **All 39+ existing reviewed `.mov` exports remain untouched** (`data_renders_v01`, `data_renders_v02_r22_fix`, `who_when_renders_v01`, `timeline_renders_v01`, `fact_renders_v01`, `mechanism_renders_v01`, `size_renders_v01`, `atmosphere_renders_v01`, `pressure_renders_v01`, `orbit_renders_v01`, `ocean_renders_v01`).
   - **Prior review gates remain in force:** `J2177` (`e54320112b`: fix `r13_radar_principles` and `r30_gravity_calc` before rendering those two `.mov` files), `J2247` (`ce9282cb61`), `J2262`, `J2264` (`8696af1d91`), Frame-0 native-motion gate, Huygens `PIA07232` provenance gate, and `JHUAPL` Dragonfly permissions gate.
   - **Composite contrast check remains open until cut assembly:** In `distance_graphic.py`, the dark reference tracks (`(45, 52, 68, 220)`) sit directly on the transparent RGBA canvas without a backing card; when composited over Row 19's Cassini Saturn/Titan background plate (`PIA14909`), verify that the background plate is darkened/graded behind `x = 800..1760` so all text and track lines pass `picture_qa.py` contrast and near-black checks.
   - **Spend:** `£0`.
