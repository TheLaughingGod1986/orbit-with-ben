# Packaging Panel Decision — OWB Weekly Thumbnail Audit (`J2834` / `J2843`)

- **Date:** 2026-11-17
- **Job:** `J2843` (`macbook` running Gemini 4 Argon High; packaging panel synthesis — the Chief's PASS stands on this file via `J2844`)
- **Ref:** `J2834` (PR #933, `macbook/J2834`), `J2840` (`codex.md`), `J2841` (`gemini.md`), `J2842` (`cursor.md`), `J2844`–`J2847`, `J2983`
- **Videos Covered:**
  1. `m09jUdwC5hk` (*How Long Will Anything in Space Last?* — Compilation `owb_compilation_v05` / `005`)
  2. `Mo93x0fxB1Q` (*Why Haven't We Found Aliens Yet? The Fermi Paradox Explained* — `001_Will-We-Ever-Meet-Aliens`)
  3. `ziKBPJ6FY0U` (*JWST Found Galaxies That Shouldn't Exist Yet* — `004_JWST-Discoveries-That-Change-Everything`)
- **Independent Critiques Weighed (all 3 present in `05_Analytics/tests/panels/owb-j2834-weekly-2026-11-14/`):**
  - `codex.md` (`J2840`, written by `claudecode` on the Mini after relay reroute)
  - `gemini.md` (`J2841`, written by `gemini`)
  - `cursor.md` (`J2842`, written by `cursor`)

---

## Executive Summary: CHANGE All Three Draft Thumbnail Bs Before Arming (`J2983`)

All three `J2834` draft thumbnails (`m09jUdwC5hk_B_v04.jpg`, `Mo93x0fxB1Q_B_v04.jpg`, `ziKBPJ6FY0U_B_v05.jpg`) pass `thumb_preview.py --score` (`sat=202.5/black=5%`, `sat=167.3/black=6%`, `sat=142.1/black=6%`), keep 2–3 words in the top band with one yellow word, and leave the bottom-right duration badge zone clear. However, **all three critics score all three thumbnails under `8/10` at `168×94`**, and two or more critics independently agree on concrete visual and factual fixes for each video before any YouTube Studio Test & Compare is armed:

| Video | Element | `codex.md` | `cursor.md` | `gemini.md` | 2-of-3+ Panel Consensus & Decision |
|---|---|---|---|---|---|
| **`m09jUdwC5hk`**<br>Compilation | Live Title A<br>Proposed Title B<br>Thumb B (`168×94`)<br>Title + Thumb Pair<br>First 30s<br>Description / Chapters | `4/10`<br>`5/10`<br>`3/10`<br>`4/10`<br>—<br>`7/10` | `6/10`<br>`3/10`<br>`5/10`<br>`5/10`<br>`6/10`<br>`5/10` | `5/10`<br>`7/10`<br>`6.5/10`<br>`7.5/10`<br>`6.5/10`<br>`8/10` | **Thumb B: CHANGE (`3/3 < 8`).** Rebuild on real Cassini Saturn rings (`RINGS ARE LEAVING`, yellow `LEAVING`).<br>**Live Title A: KEEP** during thumbnail-only test.<br>**Title B: CHANGE (`3/3 < 8`).** Drop `(10 Trillion Years)` spoiler; replace with search-first title for Round 2. |
| **`Mo93x0fxB1Q`**<br>Fermi (`001`) | Live Title A<br>Proposed Title B<br>Thumb B (`168×94`)<br>Title + Thumb Pair<br>First 30s<br>Description / Chapters | `6/10`<br>`7/10`<br>`7/10`<br>`8/10`<br>`6/10`<br>`7/10` | `6/10`<br>`8/10`<br>`6/10`<br>`7/10`<br>`6/10`<br>`7/10` | `8/10`<br>`9/10`<br>`7.5/10`<br>`9/10`<br>`4/10`<br>`6/10` | **Thumb B: KEEP concept & `ZERO SIGNALS` text, CHANGE compositing (`3/3 < 8`).** Feather `y≈72` seam, move reticle off bright core onto dark sky, fix dish corner/highlights.<br>**Live Title A: KEEP** during thumbnail-only test.<br>**Title B: KEEP (`2/3 ≥ 8`)** `Fermi Paradox: Why Haven't We Found Aliens Yet?` (`47` chars) for Round 2. |
| **`ziKBPJ6FY0U`**<br>JWST (`004`) | Live Title A<br>Proposed Title B<br>Thumb B (`168×94`)<br>Title + Thumb Pair<br>First 30s<br>Description / Chapters | `8/10`<br>`5/10`<br>`6/10`<br>`7/10`<br>`6/10`<br>— | `7/10`<br>`3/10`<br>`7/10`<br>`8/10`<br>`5/10`<br>`5/10` | `8.5/10`<br>`6.5/10`<br>`7.5/10`<br>`8.5/10`<br>`3.5/10`<br>`5/10` | **Thumb B: CHANGE loupe source & origin ring (`3/3 < 8`).** Circle and zoom a real compact high-redshift crimson galaxy (not empty sky / foreground `z~1–2` arc).<br>**Live Title A: KEEP (`2/3 ≥ 8`)** `JWST Found Galaxies That Shouldn't Exist Yet` (`44` chars).<br>**Title B: CHANGE (`3/3 < 8`).** Drop >60-char titles that repeat `300 Million Years`. |

- **Which would you click?** All three critics (`3/3`) pick **`Mo93x0fxB1Q` B (`ZERO SIGNALS`)** first (and `ziKBPJ6FY0U` B second), while all three reject `m09jUdwC5hk` B (`ALL STARS FADE`).
- **One variable per test (`RULES.md` / `J2834`):** All three initial Studio experiments remain **thumbnail-only** against the unchanged live baseline title and live thumbnail A. Separate Title-Only Bs are held for Round 2 after the 14-day thumbnail tests finish.

---

## Video-by-Video Decisions (`keep` / `change`)

### 1. `m09jUdwC5hk` — *How Long Will Anything in Space Last?* (Compilation `owb_compilation_v05` / `005`)

- **Live Title (Round 1 Thumbnail Test): KEEP**
  - **Exact text:** `How Long Will Anything in Space Last?` (`37` chars) — kept unchanged during the thumbnail-only Test & Compare so only one variable changes.
- **Separate Title-Only B (held for Round 2 after the thumbnail test ends): CHANGE**
  - **Why (`3/3` agree):** All three critics reject `How Long Will Everything in Space Last? (10 Trillion Years)` (`codex.md` `5/10`, `cursor.md` `3/10`, `gemini.md` `7/10`) because *"Anything/Everything in Space"* is not a search phrase and `(10 Trillion Years)` spoils the final red-dwarf countdown in the title while ignoring the first four chapters (Saturn's rings at 100–300 million years, the Moon, Milky Way–Andromeda, neutron stars).
  - **Exact new text (primary Round 2 Title B, `59` chars, `gemini.md`):**
    `How Long Will the Universe Last? (Until the Last Star Dies)`
  - **Exact new text (reserve named-objects Round 2 Title B, `57` chars, `codex.md`):**
    `When Will Saturn's Rings, the Moon and the Last Star Die?`
- **Thumbnail B (`m09jUdwC5hk_B_v04.jpg` → rebuild as `m09jUdwC5hk_B_v05.jpg`): CHANGE**
  - **Why (`3/3` agree):** At `168×94`, the UV/IR Helix Nebula (`PIA09178`) renders as a flat cyan smudge on a blue background with a soft pink dot (`3/10`, `5/10`, `6.5/10`), `ALL STARS FADE` is a passive truism that still collides conceptually with `005` (*The Last Star*), and no chapter of the compilation is about a Sun-like planetary nebula (`codex.md`). Both `codex.md` and `cursor.md` independently name **Saturn's rings** (Chapter 1 at `0:53 The Rings Are Leaving`, and sentence 1 of the description: *"Saturn's rings are raining into the planet right now"*) as the concrete rebuild subject.
  - **Best alternative to build as Test & Compare B (queued in `J2983` for Codex, logged in `THUMB_LEDGER.json`):**
    - **Output file:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J2834_v03/m09jUdwC5hk_B_v05.jpg` (`1280×720`, `< 2 MB`, `thumb_preview.py long --score` PASS).
    - **Plate & subject:** A real NASA/JPL-Caltech Cassini photograph of Saturn with its rings filling at least a third of the frame (e.g., Cassini backlit *"In Saturn's Shadow"* mosaic `PIA08329` or natural-colour Cassini Saturn plate, graded for high contrast and `saturation ≥ 100`, `near_black ≤ 30%`).
    - **Exact new cover text (top band, 3 words, off the planet/rings):**
      `RINGS ARE LEAVING` (`LEAVING` in yellow `#FFE600`, `RINGS ARE` in white `#FFFFFF`)
      *(2-word reserve if larger lettering is needed at `168×94`: `RINGS: GONE` with `GONE` in `#FFE600`.)*
    - **Pointer & badge zone:** One crisp white pointer arrow aimed at the inner ring rain toward Saturn's equator; bottom-right duration badge (`x>980, y>600`) completely clear.
- **First 30 Seconds / Script Opening: KEEP on live video (advice recorded)**
  - `m09jUdwC5hk` is already live (`Public`), so the video file is untouched. Future compilations open cold at `0:00` on the first countdown number rather than a 53-second thematic intro:
    > `"In 100 million years, Saturn's rings will vanish into the planet — and every other light in the night sky is on a countdown too, stretching ten trillion years into the future."`
- **Description & Chapters: KEEP during thumbnail test (optional listing tightenings recorded)**
  - `owb_compilation_v05_description.txt` already carries a strong hook, story-beat chapters (`0:53 The Rings Are Leaving` … `39:04 The Last Light`), `Sources:`, and the AI/NASA disclosure (`gemini.md` `8/10`, `codex.md` `7/10`). Left unchanged during the thumbnail test.

---

### 2. `Mo93x0fxB1Q` — *Why Haven't We Found Aliens Yet? The Fermi Paradox Explained* (`001_Will-We-Ever-Meet-Aliens`)

- **Live Title (Round 1 Thumbnail Test): KEEP**
  - **Exact text:** `Why Haven't We Found Aliens Yet? The Fermi Paradox Explained` (`60` chars) — kept unchanged during the thumbnail-only Test & Compare.
- **Separate Title-Only B (held for Round 2 after the thumbnail test ends): KEEP**
  - **Why (`3/3` agree; `2/3 ≥ 8/10`):** `cursor.md` (`8/10`), `gemini.md` (`9/10`), and `codex.md` (`7/10`) all endorse front-loading the head search query `Fermi Paradox` and dropping `Explained`.
  - **Exact text (`47` chars):**
    `Fermi Paradox: Why Haven't We Found Aliens Yet?`
  - **Reserve (`48` chars, `codex.md`):**
    `The Fermi Paradox: Why Is the Universe So Quiet?`
- **Thumbnail B (`Mo93x0fxB1Q_B_v04.jpg` → rebuild as `Mo93x0fxB1Q_B_v05.jpg`): KEEP Concept & Text, CHANGE Compositing**
  - **Why (`3/3` agree):** All three critics pick `ZERO SIGNALS` as the strongest concept in the bundle (Goldstone 70m DSN dish bottom-left + yellow search reticle + `ZERO SIGNALS` top band, `8/10`–`9/10` title+thumb pair), but all three hold the image just under `8/10` (`7/10`, `6/10`, `7.5/10`) for three specific compositing flaws visible in `Mo93x0fxB1Q_B_v04.jpg`:
    1. **Hard horizontal seam at `y≈72` (`codex.md` + `gemini.md`):** The dark navy top band ends abruptly in a straight horizontal line cutting right through the middle of the letters `ZERO SIGNALS`.
    2. **Reticle centered on the blazing white core (`3/3`: `codex.md` + `cursor.md` + `gemini.md`):** Centering the yellow crosshair on the brightest white-hot knot of the Galactic Centre (`cx=875, cy=420`) visually reads at `168×94` as *"we found a bright source"* rather than *"empty sky / zero signals"*.
    3. **Dish highlights & bottom-left corner cut (`codex.md` + `gemini.md`):** The Goldstone dish (`PIA26716`) is clipped flat white with no shadow/rim gradation and ends on a slanted cut at the bottom-left corner.
  - **Best alternative to build as Test & Compare B (queued in `J2983` for Codex, logged in `THUMB_LEDGER.json`):**
    - **Output file:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/001_Will-We-Ever-Meet-Aliens/08_Thumbnails/repackage_2026-11/J2834_v03/Mo93x0fxB1Q_B_v05.jpg` (`1280×720`, `< 2 MB`, `thumb_preview.py long --score` PASS).
    - **Exact cover text (top band, 2 words — KEEP):**
      `ZERO SIGNALS` (`ZERO` in yellow `#FFE600`, `SIGNALS` in white `#FFFFFF`)
    - **Three required image fixes on the existing `PIA12348` + `PIA26716` recipe:**
      1. Feather the top dark navy gradient smoothly across `y=0..180` so no horizontal seam exists near `y=72`.
      2. Move the yellow target reticle off the bright Galactic Centre core onto a dark dust pocket / empty sky patch on the right, and darken/desaturate the interior of the reticle by ~40% so the target visibly reads as **empty** at `168×94`.
      3. Anchor the Goldstone dish base cleanly into the bottom-left frame edge (eliminating the slanted corner gap) and pull dish highlights down 10–15% with a subtle blue sky-side rim light so the reflector mesh shows detail.
- **First 30 Seconds (`01_Script/aliens_script_v01.md`): KEEP on live video (advice recorded)**
  - `Mo93x0fxB1Q` is live (`Public`), so no re-cut is made. All three critics (`6/10`, `6/10`, `4/10`) note that the old `001` script opens with Orbit waving, an early title card, and `"I'm Orbit — and today we're asking..."` before the first number; future scripts follow the `J2428` proof-first opening rule:
    > `"Our galaxy holds over 100 billion stars, yet after more than sixty years of scanning the sky with our largest radio telescopes, we have confirmed zero alien signals. So where is everybody?"`
- **Description & Chapters (`001_Will-We-Ever-Meet-Aliens/11_Upload-Package/Descriptions/aliens_youtube_description_v01.txt`): CHANGE in repo / post-test listing pass**
  - Kept unchanged on YouTube while the thumbnail-only test runs (one variable per test). For the repo description file and any separate listing pass (`codex.md` + `gemini.md` consensus):
    - **Remove** trailing banned hashtags (`#FermiParadox #AreWeAlone #SpaceDocumentary #Aliens #OrbitWithBen`).
    - **Exact new first line:**
      `The Fermi Paradox explained: the Milky Way holds hundreds of billions of stars, so why have sixty years of radio searches heard zero alien signals?`
    - **Add `Sources:` + disclosure lines before credits:**
      `Sources: Cocconi & Morrison 1959 (Nature), searching for interstellar communications · Drake 1961 (Green Bank conference), the Drake Equation · Hart 1975 (QJRAS), explanation for the absence of extraterrestrials on Earth · Mayor & Queloz 1995 (Nature), 51 Pegasi b.`
      `Pictures: AI-generated scenes alongside NASA/ESA imagery. Facts: every number is checked against the sources listed below.`

---

### 3. `ziKBPJ6FY0U` — *JWST Found Galaxies That Shouldn't Exist Yet* (`004_JWST-Discoveries-That-Change-Everything`)

- **Live Title (Round 1 Thumbnail Test & Overall): KEEP**
  - **Why (`3/3` agree; `2/3 ≥ 8/10`):** `codex.md` (`8/10`), `gemini.md` (`8.5/10`), and `cursor.md` (`7/10`) all confirm that the 44-character live title leads with `JWST`, carries a genuine curiosity gap (`Shouldn't Exist Yet`), and pairs cleanly with a number/epoch thumbnail without repeating words.
  - **Exact text (`44` chars):**
    `JWST Found Galaxies That Shouldn't Exist Yet`
- **Separate Title-Only B: CHANGE (Drop Both `J2834` Drafts)**
  - **Why (`3/3` agree):** All three critics reject both `J2834` Title B drafts (`James Webb Telescope: Galaxies 300 Million Years After the Big Bang` at `67` chars and `JWST Found Giant Galaxies 300 Million Years After the Big Bang` at `62` chars; scored `5/10`, `3/10`, `6.5/10`) because both exceed the 60-character limit, replace the anomaly gap with a flat caption, and repeat `300 Million Years` verbatim from Thumbnail B (`studio/RULES.md` §2.2 violation).
  - **Exact new text (only if a Round 2 Title-Only test is later run after the thumbnail test ends):**
    - **Option 2A (Rule 26 spelled-out head phrase + anomaly hook, `59` chars, `gemini.md`):**
      `James Webb Telescope: The Galaxies That Shouldn't Exist Yet`
    - **Option 2B (Question-shape search phrasing, `52` chars, `codex.md`):**
      `Why Did JWST Find Galaxies That Shouldn't Exist Yet?`
- **Thumbnail B (`ziKBPJ6FY0U_B_v05.jpg` → rebuild as `ziKBPJ6FY0U_B_v06.jpg`): CHANGE Loupe Source & Origin Ring**
  - **Why (`3/3 < 8/10`; `2/3` flag the loupe/origin defect + script quote error):**
    1. **Origin circle & loupe mismatch (`gemini.md` + `codex.md`):** In `ziKBPJ6FY0U_B_v05.jpg`, the small yellow origin ring on the left (`x≈485, y≈610`) circles an empty dark patch of sky (just below a distracting bright white foreground diffraction-spiked star), while the `4.5×` zoom loupe actually displays the bright orange gravitationally lensed arc from the upper-middle of `SMACS 0723` (`x≈610, y≈200`).
    2. **Factual object mismatch (`codex.md`):** The bright orange gravitational lensing arc in `SMACS 0723` is a closer lensed galaxy billions of years after the Big Bang, not one of the `~300 million year` (`z≈13–14`) early galaxies discussed in Scene 04 (`"Some of the galaxies Webb confirmed are luminous when the universe was only about three hundred million years old"`). Putting `300 MILLION YEARS` over a zoom of a foreground lensed arc attaches a real script number to the wrong object. In addition, both `codex.md` and `cursor.md` note that `REVIEW.md` cited a non-existent "verbatim" sentence; the review note in `v03` must quote Scene 04 accurately.
  - **Best alternative to build as Test & Compare B (queued in `J2983` for Codex, logged in `THUMB_LEDGER.json`):**
    - **Output file:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/08_Thumbnails/repackage_2026-11/J2834_v03/ziKBPJ6FY0U_B_v06.jpg` (`1280×720`, `< 2 MB`, `thumb_preview.py long --score` PASS).
    - **Loupe & plate fix:** Keep the find-and-zoom layout on the real JWST NIRCam deep field (`SMACS 0723` or a confirmed `JADES` NIRCam cutout of a `z≈13–14` galaxy), **place the small yellow origin circle directly on the exact compact deep-red high-redshift galaxy source** that is magnified inside the `4.5×` zoom loupe (graded cleanly inside the loupe so the crimson high-redshift source reads at `168×94` without fake spiral structure), dim the central white foreground diffraction-spiked star by ~30%, and reduce background posterisation.
    - **Exact cover text (top band, 3 words, off the loupe and galaxy):**
      - **Primary (with the true high-redshift crimson galaxy in the loupe):**
        `300 MILLION YEARS` (`300` in yellow `#FFE600`, `MILLION YEARS` in white `#FFFFFF`, with slightly tighter letter tracking so `MILLION YEARS` has thicker strokes at `168×94`) or `300M YEARS OLD` (`300M` in `#FFE600`, `YEARS OLD` in `#FFFFFF`).
      - **Alternative (if the builder keeps the bright `SMACS 0723` lensed arc in the loupe for `168×94` contrast, with the origin ring moved onto that exact arc):**
        `WAY TOO EARLY` (`EARLY` in yellow `#FFE600`, `WAY TOO` in white `#FFFFFF`) — never pair a foreground `SMACS 0723` arc with `300 MILLION YEARS`.
- **First 30 Seconds (`01_Script/jwst_script_master_v01.md`): KEEP on live video (advice recorded)**
  - `ziKBPJ6FY0U` is live (`Public`), so the cut is untouched. All three critics (`6/10`, `5/10`, `3.5/10`) note the soft rhetorical opener, early title card, and `"Today, Orbit is going to learn beside the James Webb Space Telescope..."` meta-agenda before Scene 04's 300-million-year fact; future scripts open cold on the number:
    > `"Three hundred million years after the Big Bang, standard models expected a dark, cooling universe — instead, the James Webb Space Telescope found bright, grown-up galaxies already shining."`
- **Description & Chapters (`004_JWST-Discoveries-That-Change-Everything/11_Upload-Package/`): CHANGE in repo / post-test listing pass**
  - Kept unchanged on YouTube during the thumbnail-only test. For the repo package and any separate listing pass (`cursor.md` + `gemini.md` consensus):
    - **Exact new first line:**
      `The James Webb Space Telescope (JWST) confirmed luminous galaxies when the universe was only about 300 million years old — far bigger and brighter than standard models expected.`
    - **Story-beat chapters (preserving the live video's 8 chapter timestamps `0:00`–`15:09`) + `Sources:` & disclosure lines:**
      `Sources: Labbé et al. 2023 (Nature), candidate massive galaxies ~500–700 Myr after the Big Bang · Curtis-Lake et al. 2023 (Nature Astronomy), spectroscopic confirmation of four metal-poor galaxies at z=10.3–13.2 · Robertson et al. 2023 (Nature Astronomy), JADES high-redshift galaxy properties.`
      `Pictures: AI-generated scenes alongside NASA/ESA/CSA imagery. Facts: every number is checked against the sources listed below.`

---

## What Is Queued & Next Steps

1. **Codex `thumb` rebuild job queued (`J2983`, `--kind thumb`, `--ref J2843`, £0 spend):**
   - Rebuilds `m09jUdwC5hk_B_v05.jpg` (`RINGS ARE LEAVING` on real Cassini Saturn rings), `Mo93x0fxB1Q_B_v05.jpg` (`ZERO SIGNALS` with feathered top band, reticle on dark sky, and anchored Goldstone dish), and `ziKBPJ6FY0U_B_v06.jpg` (`300 MILLION YEARS` on a true high-redshift crimson galaxy source with the small origin ring centered on that source).
   - Runs `thumb_preview.py long <thumb> --out <sheet> --score` on each, writes `PHONE_SHEET_v03.jpg` and `DESIGN_MANIFEST.json` to `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/.../08_Thumbnails/repackage_2026-11/J2834_v03/`, and updates `05_Analytics/tests/THUMB_LEDGER.json` (reconciling IDs with `main`'s `T032`/`T033` rows from `J2884`/`J2899` so there is no ID collision when merging PR #933).
2. **Chief Gate (`J2844`):**
   - Stands on this `DECISION.md` and inspects the rebuilt `v05`/`v06` files from `J2983` before issuing an exact-file PASS and authorizing `New test -> Continue` over the already-recorded finished inconclusive `draw` reports (`T018`, `T005`, `T007`).
3. **Conditional Studio Arming (`J2845`, `J2846`, `J2847`):**
   - Remain gated behind `J2844`'s explicit exact-file PASS on the rebuilt `J2983` files. None of the `v04`/`v05` drafts from `J2834` is armed.
