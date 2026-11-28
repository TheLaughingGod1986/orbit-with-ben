# Packaging Panel Decision — OWB 064 (*Every Planet Explained*) (`J3719`)

- **Date:** 2026-11-26
- **Job:** `J3719` (`macbook`; packaging panel synthesis — **the Chief's PASS stands on this `DECISION.md`**; ordinary worker synthesis does not issue Chief PASS, merge PRs, or arm YouTube Studio tests)
- **Ref:** `J3011`, `J3021`, `J3022`, `J3023`, `J3716`, `J3717`, `J3718`, `J3720`, `J3817`, `J3818`
- **Film / Schedule:** `OWB:064` — `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes` (unreleased; pre-assembly `J3022`/`J3023`; Ben watch deadline **Fri 11 Dec 2026 18:00 London**; planned air slot **Wed 16 Dec 2026 18:00 London**; £0 spend scope, zero Flow/Vertex credits)
- **Missing-Critic Notice (Chief, 26 Nov 2026 23:50Z):** The third independent critic (`cursor.md`, `J3718`) was **missing past the 24-hour cutoff and cancelled by Chief**. Per the brief, this decision weighs the two completed independent critiques on `main`, cross-checked directly against the `J3022` source files and all three `v01` NAS thumbnail JPEGs:
  - **`codex.md` (`J3716`):** `sha256=d8c8e2b8642c88e34c7553a910db954bf37f20d251cd9faecc6dac9bbdbd666d`
  - **`gemini.md` (`J3717`):** `sha256=00f8861ecf62529ef777122ffb6902398596991cf64561bfa10bebc9312206da`
  - **`cursor.md` (`J3718`):** **MISSING** (cancelled after 24 h cutoff)
- **Verified `v01` Artifacts Inspected (untouched on `studio-live`):**
  - `064_thumb_A_all_8_worlds_v01.jpg` (`sha256=8b70c45888cd030d3addcf1b5ba140b8720dce1149e7089f60157d1803b2955b`, sat `147.3`, near-black `3.7%`)
  - `064_thumb_B_464c_to_minus224c_v01.jpg` (`sha256=898576f023e394aad43fa2e2d691c705b8f94493854af5deb5ba3c8af3cd224f`, sat `242.3`, near-black `2.8%`)
  - `064_thumb_C_real_nasa_photos_v01.jpg` (`sha256=f9349d8fcb18297e1041374a2bf60a8632b7a353f9586a962ad6963588098cf4`, sat `149.4`, near-black `4.0%`)
  - `064_thumbs_ABC_v01_preview_sheet.jpg` (`sha256=73c7a0d253a74869b9bf74c38203b10ae933305c01229c4e1bccbbc8341be28a`)
  - Locked VO (`every_planet_explained_vo_v01.wav`, `4b478fcd`, `683.86 s` / `11:24`; total planned timeline `701.86 s` / `11:42` with `18 s` end-screen hold)

---

## Summary Table Across the Two Active Critics (`codex.md` & `gemini.md`; `cursor.md` missing)

| Element | `codex.md` (`J3716`) | `gemini.md` (`J3717`) | `cursor.md` (`J3718`) | 2-of-2 Panel Consensus & Decision |
|---|---|---|---|---|
| **1a. Title 1 (Primary)**<br>`Every Planet Explained in 10 Minutes (Mercury to Neptune)` (`57` chars) | **6/10** | **7/10** | Missing | **CHANGE (`2 of 2` flag false `10 Minutes` vs `11:42` timeline).** Replace with **`Every Planet Explained in 12 Minutes (Mercury to Neptune)`** (`57` chars; matches `#2` GB autocomplete `every planet explained in 12 minutes`, honest to `11:42`, preserves Ben's locked completeness-with-number format test, zero word overlap with all three `v02` thumbnails). |
| **1b. Title 2**<br>`Every Planet Explained: From Mercury's Ice to Neptune` (`53` chars) | **8/10** | **6/10** | Missing | **CHANGE / SPLIT RESERVES.** Promote sharpened contrast title **`Every Planet Explained: 430°C Ice to Supersonic Winds`** (`53` chars) as Option B reserve, and keep **`Every Planet Explained: From Mercury's Ice to Neptune`** (`53` chars) as Option C reserve (never pair Option B with a temperature-number cover). |
| **1c. Title 3**<br>`Every Planet Explained in 10 Minutes With Real NASA Footage` (`59` chars) | **5/10** | **6/10** | Missing | **CHANGE (`2 of 2` reject `"Footage"` over-promise, `10 Minutes` mismatch, and `REAL NASA` repeat with Thumb C).** Replace with **`Every Planet Explained: A Tour in NASA Images`** (`45` chars, Option D reserve; never pair with Thumb C `"REAL NASA PHOTOS"`). |
| **2a. Thumbnail A (`168×94`)**<br>`ALL 8 WORLDS` (`8b70c458…`) | **6/10** | **4/10** | Missing | **CHANGE (`2 of 2 < 8/10`).** Rebuild as `J3719_v02` Arm 1 (`064_thumb_A_extreme_worlds_v02.jpg`) in Codex job `J3817`: deep-navy backdrop (drop flat periwinkle gradient, white speckles, and black halos), clear Jupiter + Saturn hierarchy + NASA/NOAA Suomi NPP Blue Marble 2012 Earth scale cue, replace simulated `PIA00271` with real Mariner 10 Venus (`PIA23791` right globe), hook **`8 EXTREME WORLDS`** (`EXTREME` `#FFE000`). |
| **2b. Thumbnail B (`168×94`)**<br>`464°C TO -224°C` (`898576f0…`) | **3/10** | **6/10** | Missing | **CHANGE (`2 of 2 < 8/10`; FATAL factual error).** Rebuild as `J3719_v02` Test & Compare Challenger B (`064_thumb_B_venus_uranus_v02.jpg`) in `J3817`: replace simulated `PIA00271` (read as the Sun at `sat 242.3`) with real Mariner 10 Venus (`PIA23791` right globe, moderate `sat ~150–165`), replace Neptune (`PIA01492`) with real Voyager 2 Uranus (`PIA18182`) so `-224°C` matches the actual coldest atmosphere, move **`464°C`** (`#FFE000`) / **`-224°C`** (white) into a clean top band off both globes and clear of the white seam (drop `"TO"`), add NASA/NOAA Suomi NPP Blue Marble 2012 Earth scale cue. |
| **2c. Thumbnail C (`168×94`)**<br>`REAL NASA PHOTOS` (`f9349d8f…`) | **6/10** | **3/10** | Missing | **CHANGE (`2 of 2 < 8/10`; breaks Rule 19).** Rebuild as `J3719_v02` Challenger C (`064_thumb_C_real_nasa_saturn_v02.jpg`) in `J3817`: scrap the 3-panel vertical strip completely; use one large, uncropped, aspect-preserved real NASA Cassini Saturn-and-rings hero frame (`PIA11141.jpg` primary) + crisp NASA/NOAA Suomi NPP Blue Marble 2012 Earth (`PIA18033`) scale cue on lower-left + **`REAL NASA PHOTOS`** (`REAL` `#FFE000`) cleanly in a dark top band off Saturn and its rings. |
| **3. Title + Thumbnail Together** | Best pair: `T2 + C` (after C rebuild) | Best pair: `T1 + B` (after B rebuild) | Missing | **CHANGE.** Lead pairing for launch: **`Every Planet Explained in 12 Minutes (Mercury to Neptune)`** + 3-way thumbnail-only Test & Compare of rebuilt **`A_v02` (`8 EXTREME WORLDS`)** vs **`B_v02` (`464°C` \| `-224°C`)** vs **`C_v02` (`REAL NASA PHOTOS`)** — zero word repetition across all three arms. |
| **4. Opening / First 30 Seconds**<br>(`v04` script, `v01` VO, `SHOT_LIST_v01.md`) | **6/10** (VO **8/10**) | **6/10** | Missing | **KEEP locked VO `v01` (`4b478fcd`); CHANGE `SHOT_LIST_v01.md` → `SHOT_LIST_v02.md` (`2 of 2` flag every `0:00–0:33` row exceeds the `≤ 4 s` picture-change rule, plus `codex.md` verified NASA provenance bug on `PIA00271` in `R09`).** Split `R01–R04` into `≤ 4.0 s` beats alternating real Mercury plates with split temperature graphics, add unobtrusive `01 / 08 · MERCURY` 8-planet progress strip at frame 0, and replace `PIA00271` in `R09`. |
| **5a. Description First Line** | **1/10** (missing) | **0/10** (missing) | Missing | **CHANGE (`2 of 2` unanimous — missing).** Exact opening block locked below for `J3023` upload package (`Every planet explained in 12 minutes…`, explicit Venus surface vs Uranus atmospheric minimum distinction, 5-part `studio/RULES.md` order, `≤ 5,000` chars). |
| **5b. Chapters (`0:00–9:45`)** | **7/10** | **7/10** | Missing | **CHANGE (`2 of 2` score `7/10 < 8/10`).** Keep all 8 planet names and outward timestamps (rechecked against final `J3023` export); tighten Saturn/Uranus length, remove Jupiter midpoint-twist spoiler (`Metallic Hydrogen`), and remove over-definitive `"Knocked Sideways"` origin framing on Uranus. Exact 8-line block below. |

---

## Detailed Panel Decisions (`keep` / `change`) With Exact New Text

### 1. Titles (`11_Upload-Package/`): **CHANGE**

- **Why (`2 of 2` agree):**
  1. **False `10 Minutes` duration promise:** Locked VO (`every_planet_explained_vo_v01.wav`) is `683.86 s` (`11:24`) and the planned timeline is `701.86 s` (`11:42` with the `18 s` end-screen hold). Both critics flag that `"in 10 Minutes"` beside an `11:42` YouTube duration badge undermines trust before a click, and locked narration must not be sped up or trimmed to rescue `"10 Minutes"`.
  2. **Why `12 Minutes` over `11 Minutes`:** `11:42` is 42 seconds past 11:00 and only 18 seconds shy of 12:00, AND `TOPIC_GO_NO_GO_SHEET.md` §2.1 verified **`every planet explained in 12 minutes`** as the `#2` signed-out UK YouTube autocomplete suggestion (`9zaruOUM_0o`, `181K` views). *(Runtime check in `J3023`: use `12 Minutes` if final export lands `11:30–12:15`; shift to `11 Minutes` only if final export trims to `≤ 11:29`; never `10 Minutes`.)*
  3. **Remove `"Real NASA Footage"` over-promise:** Both critics reject Title 3 because the shot list is ~35% Python code graphics + NASA still mosaics + 2 Orbit Omni clips (under the altered-content disclosure), and `"REAL NASA"` duplicates Thumbnail C's cover text (`THUMBNAIL_AND_TITLE_RULES.md` §2.3).
  4. **Search-First & Title-First compliance (`LEARNINGS` Rule 26; 10 Nov 2026 rule):** Lead Title A opens with the exact `#1` search query (`Every Planet Explained`, `20,191/mo`), keeps the locked completeness-with-number format test (`studio/plan.json`), stays `≤ 60` chars, and has **zero word overlap** with all three rebuilt `v02` thumbnail hooks so a clean 3-way thumbnail Test & Compare can run under one fixed title.

- **Exact new title set (for `J3023` `11_Upload-Package/Titles/` and `PACKAGE_MANIFEST.json`):**
  ```text
  A (Lead, 57 chars): Every Planet Explained in 12 Minutes (Mercury to Neptune)
  B (Reserve — Contrast, 53 chars): Every Planet Explained: 430°C Ice to Supersonic Winds
  C (Reserve — Curiosity Journey, 53 chars): Every Planet Explained: From Mercury's Ice to Neptune
  D (Reserve — Imagery Proof, 45 chars): Every Planet Explained: A Tour in NASA Images
  ```
  *(Pairing guard: never pair Reserve B with temperature-number Thumbnail B, and never pair Reserve D with `"REAL NASA PHOTOS"` Thumbnail C.)*

---

### 2. Thumbnails A / B / C (`08_Thumbnail/` → `08_Thumbnail/J3719_v02/` via Codex `thumb` job `J3817`): **CHANGE (REBUILD ALL THREE)**

All three `v01` thumbnails scored `< 8/10` from **both** independent critics (`A`: `6/10`, `4/10`; `B`: `3/10`, `6/10`; `C`: `6/10`, `3/10`) and failed on factual accuracy, source provenance, layout clearance (`§2.B.2`), and Rule 19 compliance despite passing numeric `thumb_preview.py --score` checks.

**Verified provenance error affecting `v01` A, `v01` B, and `SHOT_LIST_v01.md` Row `R09`:**
- `BUILD_REPORT_v01.md` and `SHOT_LIST_v01.md` label **`PIA00271`** as real Mariner 10 Venus clouds. NASA's official Photojournal record identifies `PIA00271` as **"Venus – Computer Simulated Global View of the Northern Hemisphere"** (Magellan radar mosaic, computer-simulated global view: `https://science.nasa.gov/resource/venus-computer-simulated-global-view-of-the-northern-hemisphere/`). In both `A_v01` and `B_v01` (especially at `sat 242.3`), it reads as a close-up of the Sun.
- **Fix:** Drop `PIA00271` everywhere. Use real Mariner 10 Venus cloud imagery already harvested on `studio-live`: **`harvest_J3022_v01/PIA23791.jpg`** (`sha256=853268f7922ea572a0966df4a378e6b54221102d6740bdc78f4011708ee71007`), cropping strictly the **right-hand colour-enhanced globe** cleanly away from the central white divider.

**Codex `thumb` rebuild job `J3817` (`--kind thumb`, `--film 064`, `--stage thumbs`, `--after J3719`, `--due 2026-12-08 18:00`, £0 spend) builds `J3719_v02` into `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/08_Thumbnail/J3719_v02/` (leaving `v01` untouched) and updates proposed row `T045` in `05_Analytics/tests/THUMB_LEDGER.json`:**

1. **Variant A (Lead Arm 1 — Completeness & Hierarchy) — `064_thumb_A_extreme_worlds_v02.jpg`:**
   - **Exact hook text (`2 of 2` agree on `EXTREME WORLDS`):** **`8 EXTREME WORLDS`** (`EXTREME` in yellow `#FFE000`; `8` and `WORLDS` in white `#FFFFFF`), cleanly inside a deep-navy top band (`y = 0..21%`) completely off all globes.
   - **Layout & art fixes (`2 of 2` agree):**
     - Remove the flat periwinkle-blue gradient, speckled white dots, and thick hard black cutout halos around every planet; render over a deep-navy cosmic backdrop (`~15–22%` near-black) with clean feathered limbs.
     - Build clear visual hierarchy: make **Jupiter (`PIA22946`) + illuminated Saturn with full rings (`PIA11141`, rings cleanly clear of neighbours)** dominate `>35%` of the lower-centre/left frame, with a clearly readable **NASA/NOAA Suomi NPP Blue Marble 2012 Earth (`PIA18033`)** scale anchor (`§2.A.5`) and the remaining planets cleanly spaced along a depth arc (bottom-right duration zone `x > 75%, y > 78%` clear).
     - Replace simulated `PIA00271` with real Mariner 10 Venus (`PIA23791.jpg` right globe only). Note in `BUILD_REPORT_v02.md` that the editorial lineup is not to scale.

2. **Variant B (Test & Compare Challenger B — Hot vs Cold Extreme Split) — `064_thumb_B_venus_uranus_v02.jpg`:**
   - **Why rebuilt B is the top high-CTR challenger:** Both critics confirm B has the strongest colour contrast and thumb-stopping power; `gemini.md` identifies rebuilt B as the single highest-CTR change, and `codex.md` details the exact Venus/Uranus correction.
   - **Exact hook text:** **`464°C`** (yellow `#FFE000`, left above Venus) and **`-224°C`** (white `#FFFFFF`, right above Uranus, with an unmistakable bold minus sign legible at `168×94`; drop `"TO"` so zero characters cross the centre divider).
   - **Factual & layout fixes (`2 of 2` agree):**
     - **Left half (Venus):** Replace simulated `PIA00271` (`sat 242.3` Sun look) with real Mariner 10 Venus clouds (`PIA23791.jpg` right globe) graded warm golden-amber at **moderate saturation `~150–165`** (never `242` lava-orange) so it reads unmistakably as cloudy Venus.
     - **Right half (Uranus):** Replace Neptune (`PIA01492`) with real Voyager 2 **Uranus** (`PIA18182` from `033` shelf, crisp ice-cyan grade) so `-224°C` matches the actual coldest planetary atmosphere (`−224.2 °C`, Chapter 7).
     - **Top-band clearance (`§2.B.2`):** Shift both globes slightly downward below a clean dark-navy top band (`y = 0..21%`) so the vertical divider ends cleanly below the text band and zero letters touch either planet limb.
     - **Scale cue (`§2.A.5`):** Place a crisp small **NASA/NOAA Suomi NPP Blue Marble 2012 Earth (`PIA18033`)** on the lower-centre seam (clear of bottom-right) to anchor planetary scale.

3. **Variant C (Test & Compare Challenger C — Rule 19 Single Real NASA Hero) — `064_thumb_C_real_nasa_saturn_v02.jpg`:**
   - **Why rebuilt C is co-lead CTR challenger:** `codex.md` explicitly names rebuilding C around one large Saturn-and-rings image with Earth scale cue as the single highest-CTR change, and `gemini.md` independently recommends the exact same single-hero Rule 19 rebuild.
   - **Exact hook text:** **`REAL NASA PHOTOS`** (`REAL` in yellow `#FFE000`; `NASA PHOTOS` in white `#FFFFFF`), cleanly inside a dark-navy top band completely off Saturn and its rings (zero overlap with Lead Title A).
   - **Layout & art fixes (`2 of 2` agree):**
     - Scrap the 3-panel vertical strip composite completely (and remove the flat brown top-bar leak).
     - Use **one single uncropped, aspect-preserved real NASA Cassini Saturn-and-rings hero frame** filling `>40%` of the canvas — primary source **`PIA11141.jpg`** (`harvest_J3022_v01/PIA11141.jpg`, `sha256=f612f0f9…`, sunlit golden Saturn + complete rings that read instantaneously at `168×94`; full-width uncropped `PIA17172.jpg` permitted only if bright, clean, and free of dark-disc ambiguity at `168×94`).
     - Place a crisp **NASA/NOAA Suomi NPP Blue Marble 2012 Earth (`PIA18033`)** scale reference on the lower-left (clear of bottom-right; accurate proportions or clearly framed scale inset with a single thin white pointer per `§2.B.4`, documented in the build manifest).

- **Machine & phone verification required in `J3817` (then independently checked in `J3818`):**
  - `thumb_preview.py long --score` PASS on all three (`sat ≥ 120`, Variant B capped `≤ 175`, `near_black ≤ 28%`), zero Orbit, bottom-right clear, `064_thumbs_ABC_v02_preview_sheet.jpg` inspected at `168×94`.
- **No Studio job queued now:** `OWB:064` is pre-assembly (`J3023`) and has not yet gone to Ben's UAT watch (deadline Fri 11 Dec) or YouTube upload. `THUMB_LEDGER.json` row **`T045`** is logged as `status: "proposed"` (`video: null`) and will be armed in Studio only after Ben's UAT pass and upload.

---

### 3. Opening Hook & First 30 Seconds (`SHOT_LIST_v01.md` → `SHOT_LIST_v02.md`): **KEEP VO / CHANGE SHOT LIST**

- **KEEP locked VO (`every_planet_explained_vo_v01.wav`, `4b478fcd`, `683.86 s`):** Both critics confirm the spoken hook (Mercury's `430 °C` water-ice mystery in `0.16–6.52 s`, immediate polar-crater answer by `10.98 s`, `58M km / 7× / −180 °C` payoff by `25.04 s`) is strong and stays untouched (`£0`, zero re-voice).
- **CHANGE `SHOT_LIST_v01.md` (`2 of 2` unanimous — write `SHOT_LIST_v02.md` in `J3817`, leaving `v01` untouched):**
  1. **Enforce `≤ 4.0 s` picture change across `0:00–0:32.85` (`studio/RULES.md` Lesson 7, `J2428` rule 5):** Currently `R01` (`7.10 s`), `R02` (`4.35 s`), `R03` (`14.25 s` single code graphic), and `R04` (`7.15 s`) ALL exceed `4.0 s`. Exact replacement cut table (preserving locked VO word-for-word, £0 spend):
     - `R01a` (`0.00–3.50 s`, `3.50 s`): Real rotating Mercury (`PIA15162`) + sleek unobtrusive **8-planet progress strip highlighting `01 / 08 · MERCURY`** (sells the 8-world journey visually at frame 0 without a chapter card).
     - `R01b` (`3.50–7.10 s`, `3.60 s`): Hard cut to sunlit Mercury crater limb (`PIA17386`).
     - `R02a` (`7.10–9.30 s`, `2.20 s`): Wide MESSENGER north-polar mosaic (`PIA16523`).
     - `R02b` (`9.30–11.45 s`, `2.15 s`): Tight push-in on Prokofiev permanent-shadow floor (`PIA16523` / `PIA19411` polar region, `≤ 2.35×` upscale).
     - `R03a` (`11.45–15.00 s`, `3.55 s`): Real MESSENGER bright sunlit limb (`PIA17386` — `"58 million km / 7× brighter"`).
     - `R03b` (`15.00–18.80 s`, `3.80 s`): `code_graphic_064_r03a_mercury_sunlight.mp4` (`430 °C` day / `58M km` / `7×` sunlight animated graphic).
     - `R03c` (`18.80–22.10 s`, `3.30 s`): Real Mercury day/night terminator plate (`PIA19411` — real imagery separating full-screen graphics).
     - `R03d` (`22.10–25.70 s`, `3.60 s`): `code_graphic_064_r03b_mercury_night.mp4` (`−180 °C` night plunge animated contrast bar — `DATA #1` / `NUMBER OBJECT` Ch 1 without a `14.25 s` graphic block).
     - `R04a` (`25.70–29.25 s`, `3.55 s`): Real Mercury surface plate (`PIA11364`) with `WHO #1: Giuseppe Colombo (1920–1984) — Italian mathematician`.
     - `R04b` (`29.25–32.85 s`, `3.60 s`): Distinct Mercury surface plate (`PIA16853`) dropping `WHEN: 1965` onto the timeline.
  2. **Replace simulated `PIA00271` in Row `R09` (`82.20–93.80 s`):** Replace `PIA00271` (NASA Magellan computer-simulated global view, `picture_qa` `KIND_FAIL`) with real Mariner 10 Venus clouds (`PIA23791.jpg` right globe) and/or verified real `023` shelf Venus plates.

---

### 4. Description First Line & Chapters (`11_Upload-Package/`): **CHANGE**

- **Description First Line & Opening Block (`CHANGE` — `2 of 2` flag it was completely missing):**
  Exact opening text for `J3023` `11_Upload-Package/Descriptions/` (opens with exact `#1` search query `Every planet explained`, matches honest `12 minutes` runtime, explicitly distinguishes Venus's `464 °C` surface temperature from Uranus's `−224.2 °C` atmospheric minimum per `codex.md`, without spoiling the answers):
  ```text
  Every planet explained in 12 minutes — a fact-checked tour of all eight worlds in our Solar System from Mercury's hidden polar ice to Neptune's supersonic winds, built with real NASA, ESA, and spacecraft imagery alongside clear scale comparisons.

  Travel outward from 0.4 AU to 30 AU across all eight planets: compare Venus's 464 °C surface heat with Uranus's −224.2 °C atmospheric minimum, see why Jupiter has no solid ground, and trace the spacecraft missions that revealed each world.
  ```
  *(In `J3023`, append in `studio/RULES.md` Packaging §2's 5-part order: `Chapters` below → the exact 6-entry `Sources:` line from `01_Script/SOURCES.md` → full `Image credits:` matching every final asset → honest making-of line: `Pictures: Original animated explainers and two brief AI-animated Orbit scenes alongside NASA, JPL-Caltech, ESA, and archival spacecraft imagery. Facts: every number is checked against the sources listed above.` Verify total length `≤ 5,000` characters.)*

- **Chapters (`CHANGE` — `2 of 2` score `7/10 < 8/10`):**
  Keeps all 8 planet names in outward search order and `SHOT_LIST_v01.md` boundaries (rechecked against final `J3023` export), removes Jupiter's midpoint-twist spoiler (`The Ocean of Metallic Hydrogen`), removes the over-definitive `"Knocked Sideways"` origin framing on Uranus, and trims Saturn/Uranus for mobile Key Moments:
  ```text
  0:00 Mercury — Ice at 430 °C
  1:22 Venus — Why It Burns
  2:38 Earth — What Shields Our Oceans
  4:12 Mars — The Frozen Robot Desert
  5:25 Jupiter — What Happens If You Land?
  6:47 Saturn — Vanishing Rings & Polar Hexagon
  8:17 Uranus — Why Winter Lasts 21 Years
  9:45 Neptune — Supersonic Winds at the Edge
  ```
  *(Listing/description chapter headings only; locked narration is untouched.)*

---

## Queued Jobs & Handoff

1. **Codex `thumb` rebuild & shot-list repair (`J3817`, `--kind thumb`, `--needs mini`, `--film 064`, `--stage thumbs`, `--after J3719`, `--due 2026-12-08 18:00`, £0 spend):**
   - Builds `J3719_v02` (`A`, `B`, `C`, preview sheet, `THUMB_SCORES_v02.json`, `BUILD_REPORT_v02.md`) on `studio-live`, updates `THUMB_LEDGER.json` row `T045` with exact `v02` SHA-256s, and writes `SHOT_LIST_v02.md` with `≤ 4.0 s` opening beats (`0:00–0:32.85`) and `R09` `PIA00271` removed.
2. **Exact-file QA review (`J3818`, `--kind review`, `--needs mini`, `--film 064`, `--stage thumbs`, `--after J3817`, `--due 2026-12-09 18:00`, £0 spend):**
   - Independently inspects rebuilt `J3719_v02` thumbnails (full size + `168×94`) and `SHOT_LIST_v02.md`, writes `jobs/reviews/J3818/REVIEW.md` (`KEEP`/`FIX`), and hands off to Chief to clear `J3022`'s hold and advance `J3023` assembly ahead of Ben's **Fri 11 Dec 18:00 London** watch deadline.
3. **No YouTube Studio job queued yet:** Film is pre-assembly and pre-UAT; Studio Test & Compare (`T045`) arms only after Ben's watch and upload.
4. **Chief authority:** The Chief's PASS stands on this `DECISION.md` and on the PR merge (`macbook/J3719`).
