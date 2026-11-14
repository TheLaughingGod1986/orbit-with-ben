# Packaging Panel Decision — OWB 019 Andromeda Whole-Galaxy Revision (`J2729_v02` / `J2736`)

- **Date:** 2026-11-13
- **Job:** `J2736` (`macbook` running `gemini-argon` / Gemini 4 Argon High; specialist worker covering packaging panel synthesis — the Elected Chief's exact-file PASS/FIX and release stand via dependent job `J2737`)
- **Ref:** `J2729`, `J2692`, `J2449`
- **Film / Video:** OWB `019_Andromeda-Milky-Way-Collision` (`ojk-dfOpAmw`)
- **Independent Critiques Weighed (all 3 completed in `05_Analytics/tests/panels/owb-019-andromeda-j2729-v02/`):**
  - **`J2733` (`codex.md`):** Codex, commit `501d591f5`, file `sha256=97299d65f2b4b562c70a0596207f77250733aa6e06734e2199355bfcc8992238`
  - **`J2734` (`gemini.md`):** Gemini, commit `65eaffbe0`, file `sha256=8642e59347f02276c243493619f371cc553d1914e39ec97833ffde5c37cbd47f`
  - **`J2735` (`cursor.md`):** Cursor, commit `582c4232f`, file `sha256=301d3e09bfd9db1d91f9fa234b63459ffe1798b4c6bd4c79c0fdf0a55784155f`
- **Verified Evidence & Exact Hashes (`META_v02.json` & Shared NAS `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/019_Andromeda-Milky-Way-Collision/08_Thumbnails/repackage_2026-11/J2729_v02/`):**
  - **Slot 1 (Arm 1 — Unchanged Live Baseline):**
    - Title: `What Happens During the Milky Way Andromeda Collision?` (`54` characters)
    - Cover Text: `THIS IS ANDROMEDA` (`ANDROMEDA` in yellow `#FFE600`)
    - File: `thumb_packaging_v01_ojk-dfOpAmw.jpg` (`sha256=250c9980986f2b5e3faca5399e7a8ce19e6711ca5de7d6f05bf78140b2bb2515`, `1280×720`, `253,868` bytes, `saturation=131.7`, `near_black=5%`)
  - **Slot 2 (Arm 2 — Proposed `J2729` v02 Whole-Galaxy Challenger):**
    - Title: `Milky Way Andromeda Collision (What Happens to Our Sun?)` (`56` characters)
    - Cover Text: `STARS RARELY HIT` (`RARELY` in yellow `#FFE600`, `STARS` and `HIT` in white `#FFFFFF`)
    - File: `019_andromeda_package_A_v02_ojk-dfOpAmw.jpg` (`sha256=8371a323ea5bc3b856c9409d10115d7d8fb1bd5d095ba534bcd95f472df1935c`, `1280×720`, `692,954` bytes, `saturation=158.3`, `near_black=7%`, bottom-left `NASA/JPL-Caltech` credit)
    - Source Plate: NASA/JPL-Caltech GALEX two-colour ultraviolet M31 mosaic (`PIA15416`, local `sha256=88ed2cf29704895a32427c02be2daea6204f113e30f11aac4ff789c0de29a87d`, official JPEG `sha256=c5d235a4425db34d7ffd652d249ad8059ff47f558d401f148e0d5ea37d135261`, decoded `9400×7000` RGB pixels verified identical with mean absolute channel difference `0.0`)
  - **Supporting Review Assets on Shared NAS (`J2729_v02/`):**
    - `019_v02_comparison_168x94.png` (two true `168×94` tiles, `sha256=5daddbed420925df0ef740fffd2d7ab5f2e3e8734ef4fae7e3b593142a613fe4`)
    - `019_v02_phone.png` (`168×94`, `sha256=5afbb61b79b361d6cb4b329229db2d612742fc4705b7cde9b7a309d95842c7e1`)
    - `019_v02_gate.jpg` (`sha256=bfb450b4f931b21bd73238e3bba186b9a3ce93101c6ab72682e1e9737d104743`)
    - `META_v02.json` (`sha256=3d15408f69c667a3be47c086f0298d907c859aa4f6c6ddb43e13b87b42c9d2b4`)
    - `REVIEW.md` (`sha256=c788494af51cb891b95cc8722f9ae7d2c3a1dfbbd7bb892c76323e5cb14106c1`)
    - `SOURCE_AND_TITLE.json` (`sha256=3473a37323e65e20f1c07a4c4486d7f253127a2aa94484c2d26b2de2b673bb1a`)
    - `SHA256SUMS.txt` (`sha256=2408cd0ef72f8715766f07143616d50fc0bdbd89bea83faddd4a99f7b85958f0`)
  - **Locked Script & Description Checked:**
    - `02_Video-Projects/019_Andromeda-Milky-Way-Collision/01_Script/andromeda_collision_script_master_v03.md` (`sha256=145d21344dc7f0ceacbcce44a3b47166c9eff2363d30b58285a609be69f0578c`)
    - `02_Video-Projects/019_Andromeda-Milky-Way-Collision/11_Upload-Package/description.txt` (`sha256=1ffa80e3f843726e39dc231946ec52c4ec181404372ef03b13fd5cc707326a14`)
  - **PR #866 (`codex/j2729-andromeda-v02` @ `d82edd601d895ab37a9b76dd200ea37e76668a7b`):** Open against `main`; verified to contain `02_Video-Projects/019_Andromeda-Milky-Way-Collision/08_Thumbnails/repackage_2026-11/META_v02.json` and `jobs/reviews/J2729/{BUILD_RECIPE.json,GATE.txt,REVIEW.md,SHA256SUMS.txt,SOURCE_AND_TITLE.json,build_thumbnail.py}` with no media binaries, no secrets, and exact hash parity with the shared NAS files. Ready for Elected Chief merge in `J2737`.

---

## Summary Table Across the Three Independent Critics

| Element | `codex.md` (`J2733`) | `gemini.md` (`J2734`) | `cursor.md` (`J2735`) | 2-of-3 Panel Consensus & Decision |
|---|---|---|---|---|
| **1. Title**<br>`Milky Way Andromeda Collision (What Happens to Our Sun?)` (`56` chars) | **8/10** | **8/10** | **6/10** | **KEEP (`2 of 3 ≥ 8/10`):** `codex.md` (`8/10`) and `gemini.md` (`8/10`) pass the 56-character search-first title (`LEARNINGS` rule 26 head phrase + personal Sun stake paid off in Chapter 6 `Would We Survive?`, lines 103–115). Zero-spend tightenings recorded below for Chief (`J2737`). |
| **2. Thumbnail at `168×94`**<br>`019_andromeda_package_A_v02_ojk-dfOpAmw.jpg` (`STARS RARELY HIT`) | **8/10** | **7/10** | **8/10** | **KEEP (`2 of 3 ≥ 8/10`):** `codex.md` (`8/10`) and `cursor.md` (`8/10`) pass the whole-galaxy `PIA15416` framing at `168×94` (bright core + both ends of spiral visible, `STARS RARELY HIT` crisp off the disk, `saturation=158.3`, `near_black=7%`, duration corner clear). |
| **3. Title + Thumbnail Together** | **9/10** | **7.5/10** | **7/10** | **3 of 3 agree** zero word repetition (`Collision` vs `STARS RARELY HIT`) and **3 of 3 prefer Proposed A v02 over Baseline**. Because `gemini.md` (`7.5/10`) and `cursor.md` (`7/10`) score the pair `< 8/10` (one on cover wording, one on title word order), exact zero-spend pair alternatives are provided below alongside the primary `KEEP`. |
| **4. First 30 Seconds / Short Hook**<br>(`andromeda_collision_script_master_v03.md`) | **5/10** | **6/10** | **5/10** | **3 of 3 score `< 8/10`** (early agenda line 9, chapter card at line 11, and `Our Sun` / `Stars Almost Never Hit` payoffs land at 5:44–7:11 rather than 0:00–0:30). **Live film & locked `v03` script stay unchanged per `J2692`/`J2729` scope**; exact concrete opening rewrite recorded below. |
| **5. Description First Line & Chapters**<br>(`11_Upload-Package/description.txt`) | **5/10** | **7.5/10** | **6/10** | **3 of 3 score `< 8/10`** (first line states *"in about 4 billion years"* as a settled clock, spoils *"don't smash into fireworks"*, and omits `Sun` from description/chapters). **No description edit in this job per `J2692`/`J2729` scope**; exact new text recorded below if a separate listing pass is ever opened. |
| **Which Would You Click?** | **Proposed A v02** | **Proposed A v02** | **Proposed A v02** | **3 of 3 (`codex`, `gemini`, `cursor`) click Proposed A v02 (`STARS RARELY HIT`) over Baseline (`THIS IS ANDROMEDA`).** |

---

## Detailed Panel Synthesis (`keep` / `change`)

### 1. Challenger Title: **KEEP** (Primary 2-of-3 Consensus) + Exact Text Alternatives for Chief (`J2737`)
- **Primary Decision (`keep` — 2 of 3 score `8/10`):**
  - **Exact text:** `Milky Way Andromeda Collision (What Happens to Our Sun?)` (`56` characters)
  - **Why:** Both `codex.md` (`8/10`) and `gemini.md` (`8/10`) confirm that it follows `LEARNINGS` rule 26 (plain topic phrase `Milky Way Andromeda Collision` first, personal stake `(What Happens to Our Sun?)` in the bracketed tail, under 60 characters, no duplicate detected across 200 channel snapshot titles or public exact-phrase search, and paid off in `andromeda_collision_script_master_v03.md` lines 73, 86, 98–115). No measured search demand is claimed.
- **Exact Title Change Alternatives (if Elected Chief in `J2737` acts on the 2-of-3 `< 8/10` pair score without rebuilding the thumbnail, £0):**
  - **Alternative Title 1A (`codex.md` single-change CTR hypothesis — keeps Rule 26 search-first head phrase and sharpens the parenthetical, `53` characters):**
    - **Exact new text:** `Milky Way Andromeda Collision (Will Our Sun Survive?)`
  - **Alternative Title 1B (`cursor.md` single-change CTR rewrite — moves `Our Sun` to word 2 so short browse rows never truncate the personal stake while preserving the exact search phrase, `45` characters):**
    - **Exact new text:** `Our Sun in the Milky Way Andromeda Collision?`

### 2. Challenger Thumbnail (`168×94` & Full Size): **KEEP** (`019_andromeda_package_A_v02_ojk-dfOpAmw.jpg`)
- **Primary Decision (`keep` — 2 of 3 score `8/10` on `168×94` thumbnail, 3 of 3 click v02 over Baseline):**
  - **Exact file:** `02_Video-Projects/019_Andromeda-Milky-Way-Collision/08_Thumbnails/repackage_2026-11/019_andromeda_package_A_v02_ojk-dfOpAmw.jpg` (shared NAS copy `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/019_Andromeda-Milky-Way-Collision/08_Thumbnails/repackage_2026-11/J2729_v02/019_andromeda_package_A_v02_ojk-dfOpAmw.jpg`, `sha256=8371a323ea5bc3b856c9409d10115d7d8fb1bd5d095ba534bcd95f472df1935c`, `1280×720`, `692,954` bytes, `saturation=158.3`, `near_black=7%`, cover text `STARS RARELY HIT` with `RARELY` in `#FFE600`).
  - **Why:** All three critics confirm that the `J2729` whole-galaxy `PIA15416` rebuild resolved the `J2692` close-crop defect: the bright core and both ends of the spiral disk read as one recognisable galaxy occupying over a third of the frame at `168×94`, the 3-word top-band hook sits completely off the galaxy, the bottom-right duration corner is empty sky, and `RARELY` accurately reflects the script's qualified claim (`v03` lines 73, 86, 105: *"Star-on-star crashes stay rare — a footnote, not the fireworks"*, *"Stars rarely collide"*).
- **Rule Issue Flagged for Explicit Elected-Chief Resolution in `J2737` (`codex.md` & `gemini.md`):**
  - `THUMBNAIL_AND_TITLE_RULES.md` §2.A.5 asks for a character or scale reference on every thumbnail. Because Orbit is banned on long thumbnails (`studio/RULES.md` Standing lesson 3) and the prior `019` panel ruling (`J1117` / `J2692` / `J2729`) explicitly banned a pasted Earth or misleading Sun inset inside Andromeda, this whole-galaxy plate (`PIA15416` with companion satellite galaxies M32/M110 visible in-frame) carries no separate artificial scale inset. `J2737` should explicitly note this approved whole-galaxy scope when issuing its exact-file ruling.
- **Best Alternative to Build as Test & Compare B (only if Elected Chief in `J2737` rules `FIX` instead of `PASS` — a `thumb` job for Codex, £0, logged in `05_Analytics/tests/THUMB_LEDGER.json`):**
  - Under the 2-of-3 panel consensus (`codex.md` `8/10`, `cursor.md` `8/10`), **no rebuild is required (`keep`)**.
  - However, if the Elected Chief in `J2737` elects to act on `gemini.md`'s `7/10` thumbnail note (`STARS RARELY HIT` highlights a softening adverb) before releasing `J2449`, the single bounded rebuild is a zero-spend text-layer swap on the exact same `J2729` `build_thumbnail.py` whole-galaxy `PIA15416` recipe (`1280×720`, `8°` clockwise, `scale=0.76`, `saturation=158.3`, `near_black=7%`, `NASA/JPL-Caltech` credit):
    - **Alternative Cover Text Option B1 (`gemini.md` primary rewrite, 3 words,verbatim from Chapter 5 sense):** `ALMOST NO CRASHES` (`NO` in yellow `#FFE600`, `ALMOST` and `CRASHES` in white `#FFFFFF`)
    - **Alternative Cover Text Option B2 (`gemini.md` secondary rewrite, 3 words, from `v03` line 76):** `GRAVITY, NOT CRASHES` (`GRAVITY` in yellow `#FFE600`, `NOT` and `CRASHES` in white `#FFFFFF`)

### 3. Title + Thumbnail Together: **KEEP `J2729_v02` Pair** (or Apply Zero-Spend Title Tightening in `J2737`)
- **Consensus assessment:**
  - **3 of 3 critics** confirm zero word repetition between `Milky Way Andromeda Collision (What Happens to Our Sun?)` and `STARS RARELY HIT`, and **all 3 critics** pick this challenger pair over the live baseline (`What Happens During the Milky Way Andromeda Collision?` + `THIS IS ANDROMEDA`).
  - While `codex.md` scores the pair **`9/10`**, `gemini.md` (**`7.5/10`**) and `cursor.md` (**`7/10`**) score it just under `8/10` from opposite angles (`cursor.md` keeps `STARS RARELY HIT` as an `8/10` cover and wants `Our Sun` earlier in the title; `gemini.md` keeps the 56-character title as an `8/10` title and wants `ALMOST NO CRASHES` on the cover).
  - **Synthesis:** Because both individual components pass `≥ 8/10` by 2-of-3 consensus (Title: `8/10`, `8/10`; Thumbnail: `8/10`, `8/10`) and match the locked `J2692`/`J2729` scope (`title Milky Way Andromeda Collision (What Happens to Our Sun?) (56 characters), cover STARS RARELY HIT`), the panel recommends **KEEP** on the exact `J2729_v02` pair for `J2737` PASS, with `Milky Way Andromeda Collision (Will Our Sun Survive?)` (`53` chars) and `Our Sun in the Milky Way Andromeda Collision?` (`45` chars) recorded above if the Chief prefers a shorter title string.

### 4. First 30 Seconds / Short Hook (`01_Script/andromeda_collision_script_master_v03.md`): **KEEP on Live Film** + Exact Rewrite Recorded (3 of 3 Score `< 8/10`)
- **Why 3 of 3 score `< 8/10` (`codex.md` `5/10`, `gemini.md` `6/10`, `cursor.md` `5/10`):**
  - The locked `v03` script opens with a night-sky smudge, a line-9 table-of-contents agenda (*"We ride the timeline: how the night changes first · what 'collision' actually means..."*), and an early `[CHAPTER CARD: The Second Spiral]` at line 11, while deferring the explicit rare-star-collision mechanism to Chapter 5 (`5:44`) and the Sun survival answer to Chapter 6 (`7:11`).
- **Action (`keep` on live cut; exact text recorded for future openings):**
  - Per `J2692`/`J2729`/`J2736` scope (`No Studio work or description/script edits`), the published video `ojk-dfOpAmw` and locked `v03` script are **not modified**.
  - **Exact synthesized opening rewrite (if an opening re-cut is ever scoped in the future):**
    > `"A second spiral galaxy is already in your night sky, 2.5 million light-years away — and it is closing in on our Sun at 110 kilometres a second. When the Milky Way and Andromeda meet, stars rarely hit each other, yet gravity can reshape our Sun's path and rewrite the entire night sky above Earth."`

### 5. Description First Line & Chapters (`11_Upload-Package/description.txt`): **KEEP in `J2729` Scope** + Exact Rewrite Recorded (3 of 3 Score `< 8/10`)
- **Why 3 of 3 score `< 8/10` (`codex.md` `5/10`, `gemini.md` `7.5/10`, `cursor.md` `6/10`):**
  - All three critics note that the current first line (*"The Milky Way Andromeda collision: in about 4 billion years, the Andromeda galaxy fills our sky — and the galaxies don't smash into fireworks."*) states *"in about 4 billion years"* as a settled clock (conflict with the script's explicit orbital uncertainty in Chapter 2), gives away the *"don't smash into fireworks"* twist before play, and never mentions **`our Sun`** in the description or chapter list to reinforce the new title's hook.
- **Action (`keep` in `J2729`/`J2449` test scope; exact text recorded if Chief opens a separate listing pass):**
  - Per `J2692`/`J2729`/`J2736` scope (`No Studio work or description/script edits`), `11_Upload-Package/description.txt` and the live YouTube description are **not modified** in this job.
  - **Exact new text (for future listing pass only, if ever scoped by Chief):**
    - **First line:**
      `The Milky Way Andromeda collision is already inbound — here is why stars rarely hit each other, why the merger clock is still uncertain, and what that meeting does to our Sun and the night sky.`
    - **Chapters (retaining existing cut timestamps):**
      ```text
      0:00 Andromeda Is Approaching
      0:47 Meet the Andromeda Galaxy
      2:03 Is the Collision Clock Certain?
      4:17 How the Night Sky Rewrites
      5:44 Why Stars Rarely Hit
      7:11 What Happens to Our Sun?
      8:50 Beyond the Andromeda Collision
      ```

---

## Handoff to Dependent Chief Job `J2737` (No Duplicate Jobs Queued)

1. **`J2737` (`019 Andromeda: elected-Chief exact-file release after revised packaging panel`, `kind: chief`, `after: J2736`) is already queued and `open` in `jobs/queue.json`.** Per the `J2736` brief, no duplicate build or Studio job is queued, and `J2449` is **not** reopened here.
2. **Recommended Chief Action in `J2737`:**
   - Review and merge open PR **`#866`** (`codex/j2729-andromeda-v02` @ `d82edd601d895ab37a9b76dd200ea37e76668a7b`) and this synthesis PR.
   - Issue explicit exact-file **PASS** on `019_andromeda_package_A_v02_ojk-dfOpAmw.jpg` (`sha256=8371a323ea5bc3b856c9409d10115d7d8fb1bd5d095ba534bcd95f472df1935c`, `STARS RARELY HIT`) + `Milky Way Andromeda Collision (What Happens to Our Sun?)` (`56` chars), explicitly noting the whole-galaxy no-pasted-Earth scope under `THUMBNAIL_AND_TITLE_RULES.md` §2.A.5.
   - Only after Chief PASS, reopen `J2449` narrowed strictly to a two-arm Test & Compare on `ojk-dfOpAmw`: Slot 1 unchanged live baseline (`250c9980986f2b5e3faca5399e7a8ce19e6711ca5de7d6f05bf78140b2bb2515`) vs Slot 2 approved `v02` challenger (`8371a323ea5bc3b856c9409d10115d7d8fb1bd5d095ba534bcd95f472df1935c`), with Package B and description edits excluded, fresh Studio read at execution, never replacing a running or newly set test, and never touching Black Hole `T002` or Jupiter `T030`.
