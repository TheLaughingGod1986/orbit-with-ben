# Packaging Panel Decision — OWB 034 Pluto Long Upload Package & `J3105` Thumbnail Candidates A/B/C (`J3111`)

- **Date:** 2026-11-19
- **Job:** `J3111` (`macbook-2` running Gemini 4 Argon High; packaging panel synthesis — the Elected Chief's exact-file PASS/FIX and stage release stand via dependent Chief job `J3112` after queued Codex `thumb` rebuild job `J3114`)
- **Ref:** `J3103`, `J3105`, `J3106`, `J3107`, `J3108`, `J3109`, `J3110`, `J3112`, `J3114`, `J2868`, `J3087`, `J3066`, `J3065`
- **Film / Video:** OWB `034_Why-Plutos-Frozen-Heart-Has-Zero-Craters` (unreleased Long Master `v02`; planned slot `Sun 13 Dec 2026 18:00 London` / `2026-12-13T18:00:00.000Z`, gated on Ben UAT watch `J2868` due `8 Dec 2026 18:00 London`)
- **Independent Critiques Weighed (all 3 present in `05_Analytics/tests/panels/owb-034-pluto-j3106/`):**
  - **`J3108` (`codex.md`):** Codex, commit `8c285cf89`, `sha256=e418dc33973bd3cced45880811a2b0d0df623720463c9663324baeda33acb03f`
  - **`J3109` (`gemini.md`):** Gemini, commit `5a8a62a86`, `sha256=54b5447711456765bbc0badba2be579aa1c34c9e0c28a01a67dee68c04977d88`
  - **`J3110` (`cursor.md`):** Gemini 4 Argon High covering the `cursor.md` slot via failover, commit `84a1cf734`, `sha256=6e1642196f8e1821a216f64f9998303f2a496e47fa187a35379d02e28ac3dbe9`
- **Verified Evidence & Exact SHA-256 Hashes:**
  - **Reviewed Long Master `v02` (`J2868` / `J3087` `KEEP`, untouched):**
    - `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/09_Final-Export/034_pluto_frozen_heart_master_v02.mp4` (`sha256=e5a886dfef208774cce8ae987e658fba5d7a96cbb5c99a44aadf63516949ba62`, `646.933 s`, `19,408` frames @ `30/1` CFR)
  - **Vertical Trailer (`52.500 s`, untouched):**
    - `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/11_Upload-Package/Trailer/034_why_plutos_frozen_heart_has_zero_craters_trailer.mp4` (`sha256=01701660d2fcc3a1340fa8d6ffef2f8d1a96b87e049facf1d28905c4a05392fd`)
  - **`J3105_v01` Draft Thumbnails on Shared NAS (`/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/08_Thumbnail/J3105_v01/` & open PR `#1034` `codex/j3105-pluto-thumbs`):**
    - `034_pluto_A_j3105_v01.jpg` (`NITROGEN GLACIER`, source `PIA19952`, `sha256=b42bfb90b67752ed0ee58790b0697cf179e41b56e34c48425f0e7f26c17d4eb9`, `1280×720`, `saturation=166.0`, `near_black=3%`)
    - `034_pluto_B_j3105_v01.jpg` (`ICE MOUNTAINS`, source `PIA19948`, `sha256=91c88215c47fcc74d2648a004b76d6f5c251ee0e91c1b80bbdedff1c5a23a1fe`, `1280×720`, `saturation=133.1`, `near_black=1%`)
    - `034_pluto_C_j3105_v01.jpg` (`FLOWING ICE`, source `PIA20726`, `sha256=9f33ddab1696b92496e759d6a5559e4f8a479e841bd26f8d48d835f1e32f3ae9`, `1280×720`, `saturation=107.7`, `near_black=1%`)
    - `phone_review.jpg` (`168×94` and `360×202` contact sheet, `sha256=018175b98785362f8b8f97ce9f4827a48bcdf0fb88b67918fd1da52f46cbee40`)
  - **`J3106` Upload Package Text Inputs (`02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/11_Upload-Package/`, commit `de93b3f4be`):**
    - `PACKAGE_MANIFEST.json` (`sha256=bb035c5211acff7c3f3a9aa1b762b891e8f065c08e4f450b4bf78937e0beb01a`)
    - `metadata_DRAFT_v01.json` (`sha256=277a8a001c751028c54d4bd9c49007881b64bba34aabaf99c12ff18bfa1f6502`)
    - `Descriptions/pluto_frozen_heart_long_description_v01.txt` (`sha256=42cf871350ea964252845c909e29fa8bf186ee04561129ca76877d633d260bfc`, `6,025` chars / `6,061` UTF-8 bytes)
    - `Titles/pluto_frozen_heart_titles_v01.txt` (`sha256=9a5363c5d2b6ea1faa852326fc332c8007957a52990e6c1605190ad253e322b3`)
    - `Chapters/pluto_frozen_heart_chapters_v02.txt` (`sha256=fd327c13395300f30e07a3ed595757674cc63ff29ead7fb32ff63eb69fb1f797`)
    - `01_Script/pluto_frozen_heart_script_master_v03.md` (`sha256=f9852589a7ea9888165c5148c9d60196cb174d7a41104ad442d845f2dbde65cc`)

---

## Summary Table Across the Three Independent Critics

| Element | `codex.md` (`J3108`) | `gemini.md` (`J3109`) | `cursor.md` (`J3110`) | 2-of-3+ Panel Consensus & Decision |
|---|---|---|---|---|
| **1a. Current Lead Title A**<br>`Why Pluto's Frozen Heart Has Zero Craters` (`41` chars) | **7/10** | **7/10** | **7/10** | **CHANGE Lead Title A (`3 of 3 score 7/10 < 8`).** Move `Why Pluto's Frozen Heart Has Zero Craters` to Title Option B (Arm 2 reserve). |
| **1b. Title Option B (Search-First)**<br>`Why Does Pluto Have a Heart? (And Why It Has Zero Craters)` (`58` chars) | **8/10** | **8.5/10** | **9/10** | **PROMOTE TO LEAD TITLE A (`3 of 3 ≥ 8/10`).** Matches signed-out UK YouTube autocomplete #2 (`why does pluto have a heart`), obeys `LEARNINGS` Rule 26 + 10 Nov 2026 Title-First rule, avoids `fssbsdzMiaQ` collision, and has zero word overlap with thumbnail hooks. |
| **2a. Thumbnail A (`168×94`)**<br>`034_pluto_A_j3105_v01.jpg` (`NITROGEN GLACIER`, `PIA19952`) | **7/10** | **7/10** | **8/10** | **KEEP concept & `NITROGEN GLACIER` as Lead Arm 1; CHANGE layout in `J3114` (`2 of 3 < 8/10`, and `3 of 3` ask for the same two fixes):** scale Pluto globe ~20–25% larger with a clean feathered circular limb (removing the dark rectangular paste box) and replace the unreadable 19pt `2,377 km / PLUTO DIAMETER` micro-label with a bold phone-legible scale callout (`1,000 km / HEART WIDTH` or `PLUTO / 2,377 km`). |
| **2b. Thumbnail B (`168×94`)**<br>`034_pluto_B_j3105_v01.jpg` (`ICE MOUNTAINS`, `PIA19948`) | **6/10** | **6.5/10** | **7/10** | **CHANGE (`3 of 3 < 8/10`; rebuild as Test & Compare Challenger B in `J3114`):** re-grade `PIA19948` from warm sandy-gold/sepia to cold high-contrast ice-blue/silver rim lighting (`2/3` agree), crop ~15–20% tighter onto the jagged mountain/Sputnik-plain boundary (`3/3` agree), and recalculate/thicken the bottom-left scale bar. |
| **2c. Thumbnail C (`168×94`)**<br>`034_pluto_C_j3105_v01.jpg` (`FLOWING ICE`, `PIA20726`) | **5/10** | **4.5/10** | **5.5/10** | **CHANGE (`3 of 3 < 8/10`; rebuild in `J3114` or run 2-arm `A_v02` vs `B_v02`):** drop the flat top-down acid-lime/cyan false-colour grade and solid teal UI header banner (`#438fa8`); rebuild with natural warm-cream/charcoal contrast across Sputnik Planitia's convection cells meeting the dark mountain shoreline, a smooth dark-navy top vignette band, and a quiet-corner `100 km` scale bar. |
| **3. Title + Thumbnail Together**<br>(New Lead Title `Why Does Pluto Have a Heart? (And Why It Has Zero Craters)` + Thumb A `NITROGEN GLACIER`) | **8/10** | **7/10** | **9/10** | **KEEP Pairing (`2 of 3 ≥ 8/10`).** Question/anomaly in title + material/heart on real Pluto globe with zero repeated words. (`J3114` also renders an optional `STILL ALIVE` hook variant on A per `gemini.md` for Chief comparison in `J3112`.) |
| **4. First 30 Seconds / Short Hook**<br>(`pluto_frozen_heart_script_master_v03.md` & `v02` master) | **6/10** | **8.5/10** | **9/10** | **KEEP (`2 of 3 ≥ 8.5/10`).** Locked `v03` script, `v02` master (`e5a886df…`), and approved Shorts `J3066`/`J3065` pass `J2428` proof-first opening checks and stay untouched. `codex.md` editorial opening note recorded for future scripts. |
| **5a. Description Text & Length**<br>(`Descriptions/pluto_frozen_heart_long_description_v01.txt`) | **6/10** (line 1)<br>**4/10** (`6,025` chars > `5,000` max) | **7.5/10** | **7.5/10** | **CHANGE (`3 of 3 < 8/10`).** Current file is **`6,025` characters (`6,061` bytes)** — `1,025` characters over YouTube's `5,000`-character limit (`codex.md`), repeats `"why does Pluto"` twice in Line 1 (`2/3`), and spoils the Chapter 4/5 convection and basal-liquid payoffs above the fold (`3/3`). Exact `4,595`-character replacement text provided below. |
| **5b. Chapters (`0:00`–`9:05`)**<br>(`Chapters/pluto_frozen_heart_chapters_v02.txt`) | **8/10** | **8/10** (strong story beats) | **8/10** (verified story beats) | **KEEP (`3 of 3 agree`).** All 7 story-beat chapter names and verified `cuts_v02.json` timestamps (`0:00`, `1:06`, `2:41`, `4:26`, `6:15`, `7:41`, `9:05`) remain unchanged. |
| **Which Would You Click?** | **Thumb A + Title B** | **Thumb A + Title B** | **Thumb A + Title B** | **3 of 3 (`codex`, `gemini`, `cursor`) click Thumbnail A (`PIA19952` whole globe) paired with `Why Does Pluto Have a Heart? (And Why It Has Zero Craters)`.** |

---

## Detailed Panel Decisions (`keep` / `change`) with Exact New Text

### 1. Title (`PACKAGE_MANIFEST.json`, `Titles/pluto_frozen_heart_titles_v01.txt`, `metadata_DRAFT_v01.json`): **CHANGE**

- **Why (`3 of 3` unanimous):**
  - All three critics score current Lead Title A (`Why Pluto's Frozen Heart Has Zero Craters`, `41` chars) **`7/10`** because cold viewers do not type `"why pluto's frozen heart has zero craters"` into YouTube search, and all three score Option B (`Why Does Pluto Have a Heart? (And Why It Has Zero Craters)`, `58` chars) **`8/10`, `8.5/10`, and `9/10`**.
  - Under `LEARNINGS` Rule 26 (Search-First, 9 Nov 2026) and the 10 Nov 2026 Title-First rule (`studio/RULES.md` §Packaging), the search-led title must be set as Lead Title A before any test is armed.
  - All three critics also reject the provisional `J3105` title `Why Does Pluto Have a Heart? (A Glacier With No Craters)` (`7/10`, `6/10`, `6.5/10`) because `Glacier` repeats `GLACIER` on Thumbnail A.
- **Exact new text for `Titles/pluto_frozen_heart_titles_v01.txt`:**
  ```text
  A (Lead): Why Does Pluto Have a Heart? (And Why It Has Zero Craters)
  B: Why Pluto's Frozen Heart Has Zero Craters
  C: The Only Spacecraft Photos Ever Taken of Pluto
  D: New Horizons Pluto Images: A Heart With Zero Craters
  ```
- **Exact new title fields for `11_Upload-Package/PACKAGE_MANIFEST.json`:**
  ```json
  "titleIndex": 1,
  "title": "Why Does Pluto Have a Heart? (And Why It Has Zero Craters)",
  "titleAbc": [
    "Why Does Pluto Have a Heart? (And Why It Has Zero Craters)",
    "Why Pluto's Frozen Heart Has Zero Craters",
    "The Only Spacecraft Photos Ever Taken of Pluto",
    "New Horizons Pluto Images: A Heart With Zero Craters"
  ],
  ```
  *(Note: Option D adopts `codex.md`'s concrete rewrite replacing `"What New Horizons Saw Inside Pluto's Frozen Heart"` so the alternate title does not imply subsurface camera imagery.)*

---

### 2. Thumbnails A / B / C (`08_Thumbnail/J3105_v01/` → `J3105_v02/` via Codex `thumb` Job `J3114`): **CHANGE**

All three `J3105_v01` drafts pass `thumb_preview.py long --score` (`A`: `sat=166.0, near_black=3%`; `B`: `sat=133.1, near_black=1%`; `C`: `sat=107.7, near_black=1%`), use verified NASA/JHUAPL/SwRI New Horizons harvest plates (`PIA19952`, `PIA19948`, `PIA20726`), and keep the bottom-right duration badge clear. However, **2 of 3 score Candidate A `< 8/10` at `168×94` (`7/10`, `7/10`, `8/10`) while all 3 critics identify the exact same two layout flaws on A**, and **3 of 3 score Candidate B (`6/10`, `6.5/10`, `7/10`) and Candidate C (`5/10`, `4.5/10`, `5.5/10`) `< 8/10`**.

Per the brief (*"for the thumbnail, either 'keep' or the best alternative to build as Test & Compare B (a `thumb` job for Codex, logged in THUMB_LEDGER.json)"*), Codex `thumb` job **`J3114`** is queued to build `J3105_v02` into `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/08_Thumbnail/J3105_v02/` (leaving `J3105_v01/` untouched) and log the proposed `OWB:034` row in `05_Analytics/tests/THUMB_LEDGER.json`:

1. **Variant A (`034_pluto_A_j3105_v02.jpg` — Lead / Test & Compare Arm 1, `PIA19952` whole enhanced-colour Pluto globe):**
   - **Cover text (`KEEP` by 2-of-3 consensus: `codex.md` `8/10`, `cursor.md` `9/10`):**
     `NITROGEN GLACIER` (`GLACIER` in yellow `#FFE000`, `NITROGEN` in white `#FFFFFF`)
   - **Fix 1 — Enlarge Pluto globe & eliminate rectangular paste seam (`3 of 3` agree):**
     In `build_j3105.py`, `src.thumbnail((580,550))` leaves Pluto only ~66 px wide at `168×94` with wide empty navy margins, and `weight = np.clip(arr.max(2)/38, 0, 1)` blends residual non-zero dark background pixels (`15..38`) with `#102b4b`, creating a darker-navy rectangular bounding-box halo around the cutout. Scale the unobscured Pluto globe up by **~20–25%** (`~640–660 px` diameter at `1280×720`, `~74–76 px` across at `168×94`, shifted slightly right to `cx≈700, cy≈430` so Sputnik Planitia commands the frame below the top band and clear of the bottom-right duration corner), and use a clean circular planetary-disc alpha mask feathered over `3–4 px` at the limb onto the `#102b4b` navy background so no rectangular crop seam exists.
   - **Fix 2 — Replace illegible/misleading `2,377 km / PLUTO DIAMETER` micro-label (`3 of 3` agree):**
     In `v01`, `19 pt` `PLUTO DIAMETER` collapses to `~2.5 px` high at `168×94`, leaving `2,377 km` to be misread as the glacier's width (`1,000 km`). Replace the bottom-left label in the clear left navy area with a bold two-line callout where both lines use phone-legible house type (`≥44 pt` number, `≥32–36 pt` qualifier, with dark stroke):
     - **Primary callout (`gemini.md` + `cursor.md` — names the heart's own spoken scale):**
       Line 1: `1,000 km` · Line 2: `HEART WIDTH` (or single-line **`1,000 KM WIDE`**)
     - **Alternative callout (`codex.md` — if Pluto's planetary diameter is shown):**
       Line 1: `PLUTO` · Line 2: `2,377 km` (both lines `≥38 pt` Arial Black)
   - **Optional Hook Variant (`034_pluto_A_alive_j3105_v02.jpg`, per `gemini.md`):**
     Render a companion copy of the enlarged `A_v02` globe with top-band hook **`STILL ALIVE`** (`ALIVE` in yellow `#FFE000`, `STILL` in white `#FFFFFF`) and a crisp **`1,000 km`** caliper across Sputnik Planitia so the Elected Chief in `J3112` can either use `NITROGEN GLACIER` (`A_v02`) as Arm 1 and `STILL ALIVE` (`A_alive_v02`) / `ICE MOUNTAINS` (`B_v02`) as Arm 2, or pick between them by exact SHA-256.

2. **Variant B (`034_pluto_B_j3105_v02.jpg` — Test & Compare Arm 2 Challenger, `PIA19948` oblique mountain/plain horizon):**
   - **Cover text (`KEEP`):**
     `ICE MOUNTAINS` (`MOUNTAINS` in yellow `#FFE000`, `ICE` in white `#FFFFFF`)
   - **Fix 1 — Cold ice-blue/silver rim grade (`2 of 3` agree: `gemini.md` + `cursor.md`):**
     Replace the warm golden-ochre/sepia duotone (`#123349` → `#ffce8b`), which makes a `−240 °C` water-ice world look like warm desert sand or Titan haze, with a high-contrast cold ice-blue/silver rim grade (deep space-navy `#0d2238` shadows, crisp cyan-blue atmospheric haze layers, and bright frost-white/silver sunlit mountain peaks, keeping `thumb_preview.py long --score` `saturation ≥ 115`, `near_black ≤ 25%`).
   - **Fix 2 — Tighter mountain/Sputnik-plain crop & thicker scale bar (`3 of 3` agree: `codex.md` + `gemini.md` + `cursor.md`):**
     Instead of squeezing the entire `1,250 km` panorama width into `1280 px` (which flattens the 2–3 km peaks into a thin horizon strip at `168×94`), crop **~15–20% tighter** onto the rugged mountain shadow line bordering smooth Sputnik Planitia while preserving the curving backlit limb and haze layers. Recalculate the bottom-left scale bar width accurately for the cropped fraction of the `1,250 km` source (`200 km` or `250 km`) and thicken the bar stroke to `≥6 px` with a `≥42 pt` label so it stays crisp at `168×94`.

3. **Variant C (`034_pluto_C_j3105_v02.jpg` — Test & Compare Arm 3 Challenger or Reserve, `PIA20726` convection cells):**
   - **Why `v01` failed (`3 of 3` agree: `5/10`, `4.5/10`, `5.5/10`):**
     At `168×94`, the flat top-down crop of `PIA20726` in acid-lime and cyan false colour looks like a biology microscope slide of plant cells, the flat `#438fa8` steel-blue rectangle across the top looks like a slide-deck header banner, and the bottom-left `100 km` bar vanishes into busy blue-and-yellow mountain noise.
   - **Rebuild specification (`3 of 3` agree):**
     Drop the lime/cyan false-colour grade and solid teal header rectangle. Use a natural warm-cream/charcoal/rust high-contrast grade of `PIA20726` (or `PIA20291` showing Sputnik Planitia's polygonal convection cells meeting the dark cratered mountain shoreline), a smooth dark-navy top vignette band (`#0d2238` fading smoothly into the terrain, no hard horizontal slab), top-band hook **`FLOWING ICE`** (`ICE` in yellow `#FFE000`) or **`STILL ALIVE`** (`ALIVE` in yellow `#FFE000`), and a thickened `100 km` scale bar (`stroke ≥ 6 px`, `≥42 pt` text) over a darkened lower-left vignette pad.
   - **2-Arm vs 3-Arm Test Note for Chief (`J3112`):**
     Both `codex.md` and `cursor.md` note that a **2-arm Test & Compare (`A_v02` vs `B_v02`, or `A_v02 NITROGEN GLACIER` vs `A_alive_v02 STILL ALIVE`)** focuses impressions cleanly on a sub-1,000-subscriber channel, while `C_v02` is delivered in `J3114` if Chief prefers a 3-way `A/B/C` test.

---

### 3. First 30 Seconds / Short Hook (`01_Script/pluto_frozen_heart_script_master_v03.md` & Long Master `v02`): **KEEP**

- **Decision (`keep` — 2 of 3 score `≥ 8.5/10`: `cursor.md` `9/10`, `gemini.md` `8.5/10`; `codex.md` `6/10`):**
  - Keep locked `01_Script/pluto_frozen_heart_script_master_v03.md` (`sha256=f9852589…`), locked Long Master `v02` (`034_pluto_frozen_heart_master_v02.mp4`, `sha256=e5a886df…`, `646.933 s`, `J2868`/`J3087` `KEEP`), and Ben-approved Shorts `J3066` (`034_short01_testA_opening_v02.mp4`, `sha256=c9a02052…`) and `J3065` (`034_short02_water_ice_mountains_v02.mp4`, `sha256=f3e3d47d…`) **unchanged**.
  - **Why:** Frame 0 opens on a real moving New Horizons natural-colour close-up of Sputnik Planitia (`PIA20291`) with no Orbit, no title card, and the first chapter card held until `1:06`. Sentence 2 lands the concrete answer (`1,000 km wide — larger than Texas and Oklahoma combined — with zero craters`) by `~0:14`, and Sentence 3 delivers the July 2015 flyby (`12,500 km`), `−232 °C` temperature, `260 km` crater contrast, and convecting nitrogen cells before `0:30`.
  - **Editorial lesson recorded from `codex.md` (for future scripts only; no re-voice or re-cut of locked `034`):**
    > *"Pluto's frozen heart has no craters. Its solid nitrogen ice circulates in city-sized cells. How does a frozen world keep that ice moving?"*

---

### 4. Description & Chapters (`Descriptions/pluto_frozen_heart_long_description_v01.txt` & `Chapters/pluto_frozen_heart_chapters_v02.txt`): **CHANGE Description Text / KEEP Chapters**

- **Chapters (`KEEP` — 3 of 3 score `8/10`):**
  - Keep `Chapters/pluto_frozen_heart_chapters_v02.txt` (`sha256=fd327c13395300f30e07a3ed595757674cc63ff29ead7fb32ff63eb69fb1f797`) and the 7 story-beat chapter headings (`0:00` to `9:05`) unchanged:
    ```text
    0:00 The Heart With Zero Craters
    1:06 The Girl Who Named a World
    2:41 The Moon That Never Sets
    4:26 Nine Years to the Kuiper Belt
    6:15 The Glacier That Breathes
    7:41 Where Water Is Bedrock
    9:05 Beyond the Frozen Heart
    ```
- **Description (`CHANGE` — 3 of 3 score `< 8/10`: `codex.md` `6/10` & `4/10`, `gemini.md` `7.5/10`, `cursor.md` `7.5/10`):**
  - **Three issues resolved (`2 of 3` to `3 of 3` agreement):**
    1. **Hard YouTube length overflow (`codex.md`, verified `6,025` chars / `6,061` bytes > `5,000`-char YouTube limit):** `L18` (`Sources:`) alone ran `2,546` characters by repeating every spoken fact inline alongside `L20` (`Image credits:`, `2,215` chars). Compressing each of the 6 `Sources:` entries to `<Author/Agency> (<Year>), <Document Title> — <what it backs> (<URL>)` (matching `031` `magnetic_field_flip_long_description_v01.txt` and `AGENTS.md`) brings the complete description to **`4,595` characters (`4,615` UTF-8 bytes)** while preserving **100% of the 67 image credits, all 6 source citations and URLs, all 7 chapters, the `033` Real Worlds series line, and the making-of disclosure**.
    2. **Line 1 duplicate `"why does Pluto"` & spoiler (`3 of 3` agree):** Removes the repeated `"why does Pluto"` inside the first 11 words and leads with the exact search query (`Why does Pluto have a heart`) + the `1,000-kilometre` `zero craters` New Horizons anomaly.
    3. **Paragraph 3 above-the-fold spoilers & unqualified liquid claim (`3 of 3` agree):** Holds back the Chapter 4/5 convection and basal-melting mechanisms for the video and replaces the unqualified *"and liquid nitrogen rises from basal melting"* with *"and a 2026 analysis of New Horizons data uncovered evidence of activity deep beneath the ice"*.
- **Exact new text for `02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/11_Upload-Package/Descriptions/pluto_frozen_heart_long_description_v01.txt` (`4,595` chars / `4,615` UTF-8 bytes):**
  ```text
  Why does Pluto have a heart — and why did NASA's New Horizons spacecraft find zero craters across its 1,000-kilometre frozen heart?

  Follow the story of Pluto — from Clyde Tombaugh's 1930 discovery in Flagstaff and eleven-year-old Venetia Burney's breakfast-table name suggestion, to the 1978 discovery of its giant moon Charon and New Horizons' nine-year voyage across the solar system.

  Explore a world one-fifth the width of Earth where Sputnik Planitia — a basin larger than Texas and Oklahoma combined — borders water-ice mountains two to three kilometres tall at minus 240 degrees Celsius, an unmoving giant moon, and 2026 New Horizons evidence of activity deep beneath the ice.

  More in the Real Worlds series: Why Knocked-Sideways Uranus Has 21-Year Winters

  Chapters
  0:00 The Heart With Zero Craters
  1:06 The Girl Who Named a World
  2:41 The Moon That Never Sets
  4:26 Nine Years to the Kuiper Belt
  6:15 The Glacier That Breathes
  7:41 Where Water Is Bedrock
  9:05 Beyond the Frozen Heart

  Sources: NASA Science (2024), Pluto Facts — diameter, distance, rotation, orbit, temperatures, mountains and crater-free plains (https://science.nasa.gov/dwarf-planets/pluto/facts/); NASA Science (2024), New Horizons Mission — 2006 launch, 2007 Jupiter assist, July 2015 Pluto flyby, Sputnik Planitia, 2019 Arrokoth and 60 AU milestone (https://science.nasa.gov/mission/new-horizons/); NASA Science (2024), Charon — 1978 discovery, size, orbit and mutual tidal locking (https://science.nasa.gov/dwarf-planets/pluto/moons/charon/); Stern, S. A. et al. / NASA Science News (5 August 2026), NASA's New Horizons Finds Evidence of Recent Liquid on Pluto's Surface — northern Sputnik Planitia basal-melting evidence (https://science.nasa.gov/blogs/science-news/2026/08/05/nasas-new-horizons-finds-evidence-of-recent-liquid-on-plutos-surface/); Williams, D. R. (2024), NASA NSSDCA Pluto Fact Sheet — 1930 discovery and surface pressure (https://nssdc.gsfc.nasa.gov/planetary/factsheet/plutofact.html); NASA Science (2024), Triton — retrograde orbit and −235 °C nitrogen crust (https://science.nasa.gov/neptune/moons/triton/).

  Image credits: NASA/Johns Hopkins University Applied Physics Laboratory/Southwest Research Institute (New Horizons Pluto, Charon, Nix, Hydra, Jupiter/Io & Arrokoth imagery and sequences: PIA10103, PIA14458, PIA19710, PIA19842, PIA19856, PIA19932, PIA19933, PIA19934, PIA19936, PIA19944, PIA19946, PIA19948, PIA19952, PIA19954, PIA19957, PIA19964, PIA19966, PIA19968, PIA20007, PIA20038, PIA20155, PIA20198, PIA20286, PIA20287, PIA20291, PIA20362, PIA20473, PIA20534, PIA20726, PIA20727, PIA20732, PIA21590, PIA21965, NHQ201812310001 / Bill Ingalls, Sputnik Planum floating hills, Reworked Arrokoth composite, Jupiter&Io, Venetia Burney Student Dust Counter, The Pluto System As Seen By New Horizons Spacecraft, and New Horizons Approach to Arrokoth; plus LORRI/MVIC sequences processed by Andrea Luck and Roman Tkachenko, CC BY 2.0, https://creativecommons.org/licenses/by/2.0/); NASA/ESA/STScI/H. Weaver (JHU/APL) (Hubble Space Telescope Pluto system: PIA12453); NASA/JPL-Caltech (Voyager 2 Uranus, Neptune & Triton: PIA01492, PIA01536, PIA02215, PIA02234, PIA18182; Galileo Moon: PIA00405); NASA Kennedy Space Center (New Horizons assembly & Atlas V launch: KSC-05pd2555, KSC-05pd2581, KSC-06pd0099, New Horizons 1, New Horizons encapsulation, ksc_011906_nh_launch, ksc_011906_nh_launchchange, ksc_011906_nh_spacesep, ksc_011906_nh_srbjett); NASA Goddard Space Flight Center / Reto Stöckli & Apollo 11 Crew (Blue Marble Earth PIA18033, Apollo 11 Moon as11-44-6667); U.S. Naval Observatory / James Christy & Wikimedia Commons (1978 Charon Discovery plate, public domain); Lowell Observatory / Wikimedia Commons (Clyde W. Tombaugh portrait, public domain; Photo of Venetia Burney aged 11 c. 1929, public domain); Pretzelpaws / Wikimedia Commons (The Telescope that Discovered Pluto, CC BY 2.0, https://creativecommons.org/licenses/by/2.0/); J. M. Sexton (brewbooks) / Flickr / Wikimedia Commons (Abbot L. Lowell Astrograph, CC BY-SA 2.0, https://creativecommons.org/licenses/by-sa/2.0/); Eurocommuter / NASA/JHUAPL/SwRI / Wikimedia Commons (Nix e Hidra montage, CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/). Agency and Commons imagery is cropped, colour-graded and animated with slow camera moves.

  Pictures: Original animated explainers alongside NASA/JHUAPL/SwRI/ESA/STScI/JPL-Caltech/KSC/USNO/Lowell Observatory/Wikimedia Commons imagery, with AI-assisted voice and editing. Facts: every number is checked against the sources listed above.
  ```

---

## Queued Jobs & Handoff to Chief (`J3114` → `J3112`)

1. **Codex `thumb` rebuild & package text update job queued (`J3114`, `--kind thumb`, `--film 034`, `--stage thumbs`, `--after J3111`, `--due 2026-12-08T18:00:00Z`, £0 spend):**
   - Rebuilds `J3105_v02` (`034_pluto_A_j3105_v02.jpg`, `034_pluto_A_alive_j3105_v02.jpg`, `034_pluto_B_j3105_v02.jpg`, `034_pluto_C_j3105_v02.jpg`, `phone_review_v02.jpg`, `MANIFEST_J3105_v02.json`, `REVIEW_J3105_v02.md`) into `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/08_Thumbnail/J3105_v02/` without touching `J3105_v01/`.
   - Logs the proposed `OWB:034` Test & Compare row in `05_Analytics/tests/THUMB_LEDGER.json` (reconciling IDs with open PR `#1031` so there is no merge conflict).
   - Applies the exact Lead Title A (`Why Does Pluto Have a Heart? (And Why It Has Zero Craters)`) and `4,595`-character description text above to `11_Upload-Package/` and re-verifies `gate:episode` and `youtube:package --dry-run` PASS.
2. **Dependent Chief Job (`J3112` — `034 Pluto: Chief packaging decision and delivery handoff`):**
   - Stands on this `DECISION.md` and inspects the `J3114` `v02` thumbnail artifacts (or rules directly on `v01` vs `v02`) before locking `034 thumbs` and `034 upload`.
   - Preserves `J2868` Ben UAT watch (`watch-by 8 Dec 2026 18:00 London` for planned `Sun 13 Dec 2026 18:00 London` slot, `2026-12-13T18:00:00.000Z`) and `J3066`/`J3065` Shorts public-parent holds. No live YouTube upload or Studio change occurs until Ben's `J2868` UAT OK.
