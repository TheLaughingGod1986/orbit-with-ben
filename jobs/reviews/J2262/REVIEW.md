# J2262 — Film 032 Row 8 (`r08_orbit_period`) Orbital-Period Draft Still & `PIA14922` Reuse Allocation Review

- **Job:** `J2262` (`032 R08 orbital-period draft: review still and source reuse allocation`)
- **Parent Job:** `J2089` (`032 picture: £0 harvest + code_graphics builds from SHOT_LIST_v02 (WIP film)`, `1/4`)
- **Film:** `OWB:032` (`02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan`)
- **Reviewer:** `gemini` (`gemini-argon`, specialist worker; still-image visual review + structural/reuse audit — not Chief final `OK`, not moving-video `PASS`)
- **Reviewed Worktree & Commit:** `/private/tmp/J2089-ruler-wt` (`worker/J2089-orbit` at local commit `c95c73b4f985cf1309ee9bbe1ae5886bd53cba9e`)
- **Reviewed Artefacts:**
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/J2089_ORBIT_PERIOD_REVIEW_REQUEST_v01.md`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/orbit_period_graphic.py`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/verify_orbit_period_graphic.py`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/ORBIT_PERIOD_MANIFEST_v01.json`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/ORBIT_PERIOD_CHECKS_v01.json`
  - `02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/J2089_CHECKPOINT_v12.md`
  - `/Users/benjaminoats/_desk/cache/J2089/orbit_period_previews_v01/r08_orbit_period_review.jpg` (`1920×1080`, inspected full size)
  - `/Users/benjaminoats/_desk/cache/J2089/orbit_period_previews_v01/code_graphic_032_r08_orbit_period_v01.png` (`1920×1080` RGBA at `t = 2.4 s`, `preview_sha256: a8fba9b555f4ef1e03ecc0a66dd36ef230dbad7cb99bbfac5f0df8b1b312d0f3`, inspected full size)
  - `/Users/benjaminoats/_desk/cache/J2089/harvest_v03/PIA14922.jpg` (`1417×1326`, `75,496` bytes, `source_sha256: 4513d54db42a8442deb0821bc309522b449e40534a5d5b235c8b2794a7269ff9`, inspected full size)

---

## 1. Verdict Summary

| Item | Ruling | Summary |
|---|---|---|
| **1. `r08_orbit_period` Still & Elapsed-Time Dial Design (`code_graphic_032_r08_orbit_period_v01.png`, SHA-256 `a8fba9b555f4ef1e03ecc0a66dd36ef230dbad7cb99bbfac5f0df8b1b312d0f3`)** | **`KEEP` / `APPROVED` as built** | Pairing the intact, uncropped natural-colour Cassini ISS photograph `PIA14922` (`715×669` px downscaled from `1417×1326` px, `0.5046× ≤ 1.0×`) on the left (`TITAN AND SATURN` / `NASA/JPL-Caltech/SSI`) with a separate 1-revolution elapsed-time dial on the right (`ONE FULL ORBIT` / `ABOUT 16 DAYS`) **accurately teaches Row 8 (`61.32–68.06 s`) and `01_Script/SOURCES.md` v01 governing Row 2** (`"15 days and 22 hours"`, spoken as `"about every sixteen days"`) without flat discs or invented non-scale orbital geometry. Approved to render (`code_graphic_032_r08_orbit_period_v01.mov`, `3.6 s`, `30 fps`, `108` frames, `1920×1080` `qtrle` RGBA, `-an`) under `--render --approved r08_orbit_period --review-ref J2262`. |
| **2. `PIA14922` Reuse Allocation Across Film `032` (`R06` + `R08`, `≤ 2` Appearances Cap)** | **`APPROVED` — Allocated to `R06` (Use 1 of 2) and `R08` (Use 2 of 2) Only (`0` Uses Elsewhere)** | `PIA14922` (*"Colorful Colossuses and Changing Hues"*, `1417×1326`, SHA-256 `4513d54db42a8442deb0821bc309522b449e40534a5d5b235c8b2794a7269ff9`, credit `NASA/JPL-Caltech/Space Science Institute`) is allocated to **at most 2 appearances** across Film `032`: **Row 6 (`45.62–50.44 s`, Use 1 of 2)** and **Row 8 (`61.32–68.06 s`, Use 2 of 2)**, separated by Row 7 (`51.26–60.92 s`, `9.66 s`). This exhausts `PIA14922`'s `MAX_REUSE = 2` allowance under `scripts/picture_qa.py`; do **not** use `PIA14922` in any other row (`R01–R05`, `R07`, `R09–R52`). |

---

## 2. Detailed Decisions & Verification Evidence

### A. Decision 1 — Why the Intact `PIA14922` Photograph + Separate Elapsed-Time Clock Dial Is Approved Over a Schematic Orbit Diagram

1. **Exact Match to Locked Row 8 VO (`titan_landing_vo_v02b`) and `01_Script/SOURCES.md` v01 Row 2:**
   - **Locked Row 8 VO (`61.32–68.06 s`, `6.74 s`):**
     - `61.32–62.84 s` (`1.52 s`): *"hoping to study its rings,"*
     - `63.34–68.06 s` (`4.72 s`): *"and spots a large moon circling the ringed planet about every sixteen days."* (`"about"` `66.28–66.56 s`, `"every"` `66.62–66.84 s`, `"sixteen"` `66.94–67.42 s`, `"days."` `67.52–68.06 s`)
   - **Governing `01_Script/SOURCES.md` v01 Row 2:**
     - Claim: *"25 March 1655: Christiaan Huygens points one of the telescopes he built himself at Saturn, hoping to study its rings, and finds a large moon circling it about every sixteen days."*
     - Verbatim quotes (`https://science.nasa.gov/saturn/moons/titan/facts/`): *"Dutch astronomer Christiaan Huygens discovered Titan on March 25, 1655."* and *"Titan takes 15 days and 22 hours to complete a full orbit of Saturn."* (also ESA `https://www.esa.int/Science_Exploration/Space_Science/Cassini-Huygens/Facts_about_Titan`: *"Titan's rotation period of about 16 days is synchronous to Saturn"* / *"Orbital period (Titanic day): 15.95 Earth days"*).
   - The spoken fact in Row 8 is the **orbital period** (`"about every sixteen days"` for one full orbit of Titan around Saturn).

2. **`AGENTS.md` Lesson 7 & Missing-Footage Fallback #4 Compliance (No Flat Discs, No Invented Orbital Geometry):**
   - Under `AGENTS.md` Lesson 7 (*"Real bodies, not flat discs... FAIL: a computer model or reconstruction, simulation, diagram, chart, schematic or labelled image"*) and `AGENTS.md` Missing-footage fallback #4 (*"Do not... invent scientific geometry"*), drawing a flat schematic dot circling a disc or superimposing a fabricated, non-scale ellipse around a close-up photograph of Saturn (Titan's true orbital semi-major axis of `~1,221,870 km` is `~20.3` Saturn equatorial radii and cannot fit around a legible Saturn globe on `1920×1080` at true scale) would either violate the ban on flat discs or misrepresent physical scale.
   - `orbit_period_graphic.py` solves this cleanly and honestly:
     - **Left column (`x = 140..855`):** Displays the **intact, uncropped `PIA14922` natural-colour Cassini ISS photograph** (*"Colorful Colossuses and Changing Hues"*, `1417×1326` px downscaled via `Image.Resampling.LANCZOS` to `715×669` px at `PHOTO_XY = (140, 220)`, `upscale = 715 / 1417 = 0.5046× ≤ 1.0×`), preserving the entire native field and true perspective of golden-orange Titan in front of ringed Saturn, with header `TITAN AND SATURN` (`3` words, `font(54)` `GOLD` at `(140, 130)`) above and credit `NASA/JPL-Caltech/SSI` (`font(28)` `WHITE` at `(140, 930)`) below.
     - **Right column (`x = 1020..1591`):** Displays a **separate elapsed-time clock dial** centered at `DIAL = (1370, 520)` with `RADIUS = 220` (`box = (1150, 300, 1590, 740)`): a `4 px` muted ring `(140, 160, 180, 170)`, a `12 px` `GOLD` arc sweeping monotonically from `-90°` (`12 o'clock`) through `360°` over `t = 0.4..2.4 s`, a `7 px` `WHITE` clock hand of length `175 px` from the `GOLD` center hub (`r = 10 px`), header `ONE FULL ORBIT` (`3` words, `font(58)` `GOLD` at `(1020, 130)`), and readout `ABOUT 16 DAYS` (`3` words, `font(68)` `WHITE` at `(1040, 815)`).

3. **Full-Size Visual Inspection (`1920×1080`), House Type & `<= 4`-Word Label Lock:**
   - Directly inspected `/Users/benjaminoats/_desk/cache/J2089/orbit_period_previews_v01/r08_orbit_period_review.jpg`, `/Users/benjaminoats/_desk/cache/J2089/orbit_period_previews_v01/code_graphic_032_r08_orbit_period_v01.png`, and `/Users/benjaminoats/_desk/cache/J2089/harvest_v03/PIA14922.jpg` at full resolution:
     - All 3 teaching labels + 1 agency credit line use `HelveticaNeue.ttc` bold (`index=1`), sit completely outside the `715×669` photograph (`x = 140..855, y = 220..889`), and obey the `≤ 4`-word house rule:
       - `TITAN AND SATURN` (`3` words, `54 pt` `GOLD`, `(140, 130)`)
       - `ONE FULL ORBIT` (`3` words, `58 pt` `GOLD`, `(1020, 130)`)
       - `ABOUT 16 DAYS` (`3` words, `68 pt` `WHITE`, `(1040, 815)`)
       - `NASA/JPL-Caltech/SSI` (`1` agency credit token, `28 pt` `WHITE`, `(140, 930)`)

4. **Reproducible 109-Sample Structural & Safe-Area Audit:**
   - Independently executed `/Users/benjaminoats/_desk/venv-graphics/bin/python 02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/verify_orbit_period_graphic.py --manifest 02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/ORBIT_PERIOD_MANIFEST_v01.json` in `/private/tmp/J2089-ruler-wt` (exit `0`, matching `ORBIT_PERIOD_CHECKS_v01.json`):
     - `source_sha256`: `4513d54db42a8442deb0821bc309522b449e40534a5d5b235c8b2794a7269ff9` (`PIA14922.jpg`, `1417×1326`) — `MATCH`.
     - `preview_sha256`: `a8fba9b555f4ef1e03ecc0a66dd36ef230dbad7cb99bbfac5f0df8b1b312d0f3` (`code_graphic_032_r08_orbit_period_v01.png`) — `MATCH`, and `frame(2.4).tobytes()` reproduces the PNG byte for byte.
     - `photo_dimensions`: `[715, 669] <= [1417, 1326]` (`source_not_upscaled = true`, `0.5046×` downscale).
     - `entry_exit_alpha`: `frame(0.0)` (`j = 0`) and `frame(3.6)` (`j = 108`) have `alpha_bounds = None` (`alpha = 0`).
     - `safe_area`: all 107 active samples (`j = 1..107`) have `alpha_bounds = [140, 141, 1591, 964]`, strictly inside the 5% safe area `[96, 54, 1824, 1026]`.
     - `progress(t)`: monotonic `0.0 → 1.0` across all 109 samples (`progress(0.4) == 0`, `progress(2.4) == 1`, `frame(0.8) != frame(1.5)`).
     - `render_guard`: unapproved `--render` exits `2` (`REJECTED_DRAFT`).

---

### B. Decision 2 — `PIA14922` Reuse Allocation (`R06` + `R08`, `≤ 2` Appearances Cap) & Row 8 Cut/Composite Rules

1. **Film-Wide `PIA14922` Allocation (`MAX_REUSE = 2`):**
   - `AGENTS.md` Lesson 7 and `scripts/picture_qa.py` (`MAX_REUSE = 2`) enforce a hard FAIL if any still source appears in more than **2 non-adjacent stretches** across the film.
   - `PIA14922` (*"Colorful Colossuses and Changing Hues"*, `1417×1326`, SHA-256 `4513d54db42a8442deb0821bc309522b449e40534a5d5b235c8b2794a7269ff9`, credit `NASA/JPL-Caltech/Space Science Institute`) is allocated to **2 appearances total** in Film `032`:
     1. **Use 1 of 2 — Row 6 (`45.62–50.44 s`, `4.82 s`, Chapter 0 bridge into Chapter 1):** Full-frame slow push on natural-colour orange Titan before ringed Saturn (`1417×797` 16:9 crop → `1920×1080`, `upscale = 1920 / 1417 = 1.355× < 2.0×`).
     2. **Use 2 of 2 — Row 8 (`61.32–68.06 s`, `6.74 s`, Cut 2: `r08_orbit_period`):** Intact `715×669` downscaled `PIA14922` (`0.5046× ≤ 1.0×`) inside `code_graphic_032_r08_orbit_period_v01.mov` (`3.60 s`, `64.46–68.06 s`), separated from Row 6 by Row 7 (`51.26–60.92 s`, `9.66 s`: `huygens_portrait_1671` + `WHO` lower-third + `25 MARCH 1655` timeline stamp).
   - **Strict Cap Exhausted:** Allocating `PIA14922` to `R06` and `R08` exhausts its 2-appearance limit. Do **not** use `PIA14922` in any other row (`R01–R05`, `R07`, `R09–R52`).

2. **Row 8 Cut Structure (`61.32–68.06 s`, `6.74 s`, 2 cuts) & Near-Black / Composite Contrast Requirements:**
   - **Cut 1 (`61.32–64.46 s`, `3.14 s`, *"hoping to study its rings, and spots..."*):** Real moving Cassini Saturn ring-plane pan separating Row 7's `25 MARCH 1655` timeline stamp from Row 8 Cut 2's `r08_orbit_period` graphic, and continuing underneath Cut 2 (`64.46–68.06 s`, `3.60 s`) as the graded moving backdrop.
     - *Recommended plate for Row 8's ring-plane pan:* Use `PIA17172` (*"The Day the Earth Smiled"*, `9000×3500`, `NASA/JPL-Caltech/SSI`, already downloaded in `/Users/benjaminoats/_desk/cache/J2089/harvest_v01/PIA17172.jpg`, `0` uses elsewhere in Film `032`, `upscale <= 1.0×`) for Cut 1 and as the graded moving plate behind Cut 2 (`r08_orbit_period`), so the viewer sees a wide Saturn ring-plane pan on *"hoping to study its rings"* before the `PIA14922` Titan-and-Saturn inset + clock dial enters on *"and spots a large moon circling the ringed planet about every sixteen days"*. *(Alternatively, if Row 8 Cut 1 and Cut 2 share `PIA14922` back-to-back within Row 8, `picture_qa.py` counts back-to-back cuts of one source as 1 appearance, keeping `PIA14922` at 2 appearances total: `R06` + `R08`.)*
   - **Near-Black & Contrast Budget at Composite Assembly:**
     - Inside `code_graphic_032_r08_orbit_period_v01.png`, the opaque near-black space corners of the uncropped `715×669` `PIA14922` rectangle (`x = 140..855, y = 220..889`) occupy **`16.00%`** of the `1920×1080` canvas (`16.12%` `luma < 16` on `r08_orbit_period_review.jpg`).
     - To keep the assembled Row 8 Cut 2 composite strictly below `polish_gate.py`'s **`≤ 30%` near-black cap** (with a `≤ 25%` safety target) and above **`≥ 4.5:1` text contrast**, the graded moving background plate outside `x = 140..855, y = 220..889` (`76.93%` of the frame) must be lifted above near-black (`luma >= 22`, with fine film grain and a darkened/evened right hemisphere `luma ≈ 24..45` behind `ONE FULL ORBIT`, the clock dial, and `ABOUT 16 DAYS`).

---

## 3. Export Implementation Instructions & Preserved Holds for `J2089`

1. **Upgrade `orbit_period_graphic.py` From Draft Guard to Reviewed Export Gate (`--render --approved r08_orbit_period --review-ref J2262`):**
   - Keep `frame(t)`, `SOURCE`, `PHOTO_XY`, `PHOTO_SIZE`, `DIAL`, `RADIUS`, and `preview_sha256` (`a8fba9b555f4ef1e03ecc0a66dd36ef230dbad7cb99bbfac5f0df8b1b312d0f3`) completely unchanged.
   - Replace the draft-only `if a.render: ap.error(...)` guard in `orbit_period_graphic.py` with the standard `--approved r08_orbit_period --review-ref J2262` `qtrle` RGBA `.mov` export block (matching `ocean_graphic.py` and `verify_reviewed_exports.py`), writing to a **fresh output directory**:
     ```bash
     /Users/benjaminoats/_desk/venv-graphics/bin/python 02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/07_Edit-Project/orbit_period_graphic.py \
       --out /Users/benjaminoats/_desk/cache/J2089/orbit_period_renders_v01 \
       --render \
       --approved r08_orbit_period \
       --review-ref J2262
     ```
   - Register `('orbit_period', orbit_period, 'J2262')` in `verify_reviewed_exports.py` so the rendered `.mov` (`code_graphic_032_r08_orbit_period_v01.mov`, `1920×1080`, `30 fps`, `108` frames, `3.6 s`, `qtrle` ARGB, `-an`) is verified byte-for-byte against `frame(i / 30)` and `a8fba9b555f4ef1e03ecc0a66dd36ef230dbad7cb99bbfac5f0df8b1b312d0f3`.

2. **Preserved Exports, Reviews & Boundaries:**
   - **Do NOT push `/private/tmp/J2089-ruler-wt` (`worker/J2089-orbit`):** Its ancestor branch inherited an automatic-review public-push rejection; integrate `orbit_period_graphic.py` cleanly in the local `J2089` worktree without bypassing that rejection.
   - **All existing reviewed `.mov` exports remain untouched:** the 39 prior exports (`data_renders_v01`, `data_renders_v02_r22_fix`, `who_when_renders_v01`, `timeline_renders_v01`, `fact_renders_v01`, `process_renders_v01`, `uranus_renders_v01`) plus the 17 reviewed exports rendered at `21cdd87bb5` (`mechanism_renders_v01` 15 clips under `J2177`, `size_renders_v01` under `J2247`, `ocean_renders_v01` under `J2264`).
   - **Prior review rulings and holds remain in force:**
     - `J2177` (`e54320112b`): fix and review `r10_spectrum` and `r32_scalemap` before rendering those 2 mechanism clips; apply `R25` (`PIA17163` + `PIA21450`), `R16`/`R51` (`PIA07870`/`PIA07871`), and Row 1 Frame-0 native-motion / Chief fallback rulings.
     - `J2247` (`ce9282cb61`): `r09_sizes` `KEEP` and `PIA15162` MESSENGER usage-statement clearance.
     - `J2264` (`8696af1d91`): `r35_ocean` `KEEP` and `PIA14602` 2-use cap (`R09` + `R35` only; `R03` uses `PIA21902` Use 1/2).
     - `J2260` (`4261d05bb6`): `r19_distance` linear 2-bar AU comparison approved with pre-verified source swap to `PIA14909` (`273b19ebae1b...`) or `PIA21610` (`ec18f2b771e5...`) under `--approved r19_distance --review-ref J2260`.
     - `JHUAPL` Dragonfly animation permissions hold (`J2089_CHECKPOINT_v05.md`) remains in force.
   - **Parent `J2089` remains at `1/4` (`£0` spent):** Final licensed harvest, remaining real-body graphics (`R18` pebble ruler, `R23` landings chart), `r10_spectrum`/`r32_scalemap` fixes, and graded composite assembly (`picture_qa.py`, `polish_gate.py`) remain to complete.
