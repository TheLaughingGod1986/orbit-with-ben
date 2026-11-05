# J2251: 032 R52 real-photo winter-duration still review and tilt-axis scope (`J2089` / PR #538 `14b66b71c0`)

5 Nov 2026 · Gemini (`gemini-argon`, `macbook-2`, Rule H review lane) · £0.

Reviewed `uranus_graphic.py`, `URANUS_MANIFEST_v01.json`, `URANUS_CHECKS_v01.json`, `verify_uranus_graphic.py`, and `J2089_URANUS_REVIEW_REQUEST_v01.md` at `14b66b71c0` (PR #538) against `01_Script/titan_landing_script_master_v02.md`, `01_Script/SOURCES.md` (row 18), `02_Voiceover/stt/titan_landing_vo_v02b/stt_raw.json` (Row 52, `567.66–582.38 s`), `07_Edit-Project/SHOT_LIST_v04.md` (Row 52), and `07_Edit-Project/HARVEST_POOL_v01.json` (`PIA18182` and `weic2310a`).

This is a still-frame review and R52 geometry scope decision only; it is not motion perception, final composite contrast verification, or film-stage PASS.

---

## 1. Verdict Summary

1. **R52 Duration Still (`r52_uranus_21y`) — `KEEP` as built.**
   - Approved to render (`code_graphic_032_r52_uranus_21y_v01.mov`, `3.6 s`, `30 fps`, `108` frames, `1920×1080` `qtrle` RGBA, `-an`) under `--approved r52_uranus_21y --review-ref J2251` in a fresh version directory once the draft-only `--render` guard in `uranus_graphic.py` is replaced with the standard `qtrle` export block (matching `size_graphic.py`).
2. **R52 Tilt-Axis Scope — RETAIN `r52_uranus_21y` as the duration-only `CODE` variant for Row 52; do NOT draw a 2D tilt-axis line across `PIA18182` or build a second R52 `CODE` graphic.**
   - In Row 52 (`567.66–582.38 s`), the sideways-tilt clause (*"a giant world tipped onto its side, perhaps by an ancient collision,"* `572.04–576.68 s`) is shown directly by the real **JWST NIRCam tilted Uranus with vertical rings (`weic2310a`, `NASA, ESA, CSA, STScI, J. DePasquale (STScI)`, CC BY 4.0, with `INFRARED VIEW` disclosure tag)**, where Uranus's nearly vertical ring system and bright polar cap authentically demonstrate the sideways orientation without invented 2D axis geometry.
   - `r52_uranus_21y` then covers the final `DATA` clause (*"so that half of it plunges into a dark winter that lasts twenty-one years,"* `577.20–582.38 s`) as a single-idea duration graphic over an approved graded moving background plate.
3. **Single-Use Rule for `PIA18182` in R52:**
   - Use `PIA18182` **once** within R52 — inside `r52_uranus_21y` — and **never** a second time as a standalone R52 plate before or after the graphic.

---

## 2. Direct Verification Evidence

### A. Source Provenance, Crop & Full-Size Still Inspection
- **Source (`PIA18182`):** Verified original NASA/JPL-Caltech Voyager 2 Uranus image (`1720 × 1720`, `83,489` bytes, SHA-256 `3dcc83114f1a25caa1ae1a1436830fffaa15a3e429666dbf4c68bcf035e8932b`), matching `HARVEST_POOL_v01.json` and `URANUS_MANIFEST_v01.json`.
- **Crop & Scale (`CROP = (140, 160, 1560, 1580)`):** Crops a `1420 × 1420` square around the photographic limb of Uranus, applies an inscribed circular alpha mask (`ellipse((0, 0, 1419, 1419), fill=255)`), and downscales via `LANCZOS` to `620 × 620` px at `(180, 220)` (`upscale = 620 / 1420 = 0.4366× <= 1.0×`, well below the `2.35×` cap).
- **Visual Inspection:** Viewed the full-size `PIA18182.jpg` source, the full-size rendered still `r52_uranus_review.jpg` (`1920 × 1080` at `t = 2.6 s`), the transparent overlay `code_graphic_032_r52_uranus_21y_v01.png`, and the companion JWST NIRCam image `weic2310a` (`uranus_nircam_unannotated.png`, `2000 × 2000`, SHA-256 `e5f7a1a0e10a6e6c769b40ecbb2f4dd78ea2ada65f2e96efd69c113ea29f52a7`). The `1420 × 1420` crop preserves Uranus's real sunlit limb on the upper-right and natural terminator fade on the lower-left with no invented surface texture, artificial terminator, or seasonal illumination model.

### B. Spoken Line, `SOURCES.md` Row 18 & House Style Check
- **Locked VO (`titan_landing_vo_v02b`, Row 52 `567.66–582.38 s`, `14.72 s`):**
  - `567.66–571.48 s` (`3.82 s`): *"Next, we travel one planet further out to Uranus,"*
  - `572.04–576.68 s` (`4.64 s`): *"a giant world tipped onto its side, perhaps by an ancient collision,"*
  - `577.20–582.38 s` (`5.18 s`): *"so that half of it plunges into a dark winter that lasts twenty-one years."*
- **Source (`01_Script/SOURCES.md` row 18):**
  - `https://science.nasa.gov/uranus/facts/` — verbatim quotes: *"This may be the result of a collision with an Earth-sized object long ago."* and *"plunging the other half of the planet into a 21-year-long, dark winter"*.
- **Labels & Layout (`AGENTS.md` Lesson 7, *Teach on screen*, and Per-Chapter Teaching Gate `WORDS` / `NUMBER`):**
  - `DARK WINTER` (`font(57)`, `GOLD` `#FFCF40`, at `(1000, 350)`) — `2` words (`≤ 4` words), verbatim from the spoken line and `SOURCES.md` row 18.
  - `{round(21 * progress)} YEARS` (`font(86)`, `WHITE` `#F9F8F3`, at `(1000, 445)`) — `2` words (`≤ 4` words), counting linearly from `0 YEARS` to `21 YEARS` over `t = 0.4..2.6 s` and holding `21 YEARS` through `t = 3.2 s`.
  - Linear duration bar `(1010, 650)–(1690, 650)` (`680 px` span, `width = 8`, track `(130, 150, 180, 180)`, progress fill `GOLD`) with end ticks and labels `0` and `21`.
  - `URANUS` (`font(58)`, `GOLD`, at `(180, 900)`) — `1` word (`≤ 4` words), verbatim from the spoken line, paired with agency credit `NASA/JPL-Caltech` (`font(28)`, `WHITE`, at `(180, 980)`).
  - Single idea (`21-year dark winter` duration), real photographic body (`PIA18182`), zero unsourced numbers.

### C. 109-Sample Structural & Safe-Area Verification
- Re-ran `uranus_graphic.py` and `verify_uranus_graphic.py` across all `109` sample timestamps (`t = i / 30` for `i = 0..108`, `3.6 s` at `30 fps`):
  - **Transparent endpoints:** `i = 0` (`t = 0.0 s`) and `i = 108` (`t = 3.6 s`) return `bbox = None` (`alpha = 0`).
  - **Safe area (`[96, 54, 1824, 1026]`):** All active frames `i = 1..107` stay strictly inside the 5% safe area (`[180, 220, 1714, 1008]` on the Mini; `[180, 220, 1714, 1012]` under MacBook FreeType).
  - **Animation & guard:** `frame(0.7) != frame(2.6)`, `round(21 * min(1, (2.6 - 0.4) / 2.2)) == 21`, and unapproved `--render` exits `2` (`requires named still approval`).

---

## 3. Rationale for Retaining Duration-Only Variant (Tilt-Axis Scope)

1. **Viewing Geometry of `PIA18182`:** Voyager 2 acquired `PIA18182` in January 1986 near Uranus's southern summer solstice, looking nearly straight down the sunlit rotation pole (spin axis oriented predominantly along the camera's line of sight, not in the sky plane). Drawing a 2D diagonal "tilt axis" line across the featureless cyan disc of `PIA18182` without a 3D orbital-plane reference would be scientifically arbitrary and misrepresent where the pole lies in the photograph.
2. **Sourced Claims in `032` vs `033`:** Film `032` (`SOURCES.md` row 18) is a 14.7-second hand-off tease to Film `033` and neither speaks nor sources Uranus's `97.77°` obliquity (which is sourced and taught in Film `033`, rows 5–6 of `033/07_Edit-Project/SHOT_LIST_v01.md`). Adding unsourced degree numbers or off-script axis labels in `032` R52 would violate the Per-Chapter Teaching Gate (`WORDS`).
3. **One Idea per Graphic & Real-Image Demonstration in R52:**
   - **Cuts 1–2 (`567.66–577.20 s`, *"Next, we travel one planet further out to Uranus, a giant world tipped onto its side, perhaps by an ancient collision,"*):** Show the real **JWST NIRCam Uranus with vertical rings (`weic2310a`)** as a ring-preserving inset over a graded moving space background (wide establishing view → slow push on the vertical ring system and bright polar cap, credited `NASA, ESA, CSA, STScI, J. DePasquale (STScI)` with `INFRARED VIEW` disclosure tag; or a Titan-limb departure bridge into `weic2310a`). The vertical ring system visually proves Uranus is tipped onto its side in a real telescope image.
   - **Cut 3 (`577.20–582.38 s`, *"so that half of it plunges into a dark winter that lasts twenty-one years."*):** Composite `r52_uranus_21y` (`3.6 s`, real Voyager 2 `PIA18182` globe + `DARK WINTER / 21 YEARS` counter and `0–21` bar) over a graded moving background plate, then carry the moving end-screen picture for the required `15–20 s` post-VO hold (`docs/ORBIT_PLAYBOOK_LESSONS.md` §2) as the music fades.
   - This keeps `PIA18182` to **one appearance** in R52 (`r52_uranus_21y` only) and keeps `r52_uranus_21y` to **one idea**.

---

## 4. Export Implementation & Preserved Holds for `J2089`

- **Export step for `J2089` (`codex` on `codex/J2089-size` / PR #538):**
  - Replace `if args.render: ap.error('Draft only: implement export after the still decision')` in `uranus_graphic.py` with the standard `ffmpeg` `qtrle` RGBA `.mov` export block (matching `size_graphic.py`, writing `code_graphic_032_r52_uranus_21y_v01.mov` into a fresh output directory when called with `--render --approved r52_uranus_21y --review-ref J2251`), and record the `.mov` path, SHA-256, and `review_ref: "J2251"` in `URANUS_MANIFEST_v01.json`.
- **Preserved exports and holds (unchanged by this review):**
  1. Preserve all **38** existing approved overlay, DATA, and process exports.
  2. **`J2177`** retains the 17 mechanism-still review and the frame-0 native motion / R25 `PIA07232` 3-use conflict rulings.
  3. **`J2247`** retains the R09 diameter-comparison still review and `PIA15162` Mercury rights ruling.
  4. **JHUAPL Dragonfly animation rights hold** (`J2089_CHECKPOINT_v05.md`) remains in force.
  5. **Composite & gate checks:** Final placement over a graded moving plate, `≥ 4.5:1` composite contrast, `≤ 2` still appearances across the final cut manifest, `picture_qa.py`, and `polish_gate.py` remain required at assembly. Parent `J2089` remains at `1/4` (`£0` spent).
