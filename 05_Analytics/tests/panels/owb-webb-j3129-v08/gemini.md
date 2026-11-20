2026-11-20 · gemini

# Packaging Panel Critique — OWB 004 Webb v08 (`ziKBPJ6FY0U`, J3129 / J3191)

- **Candidate inspected:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/08_Thumbnails/repackage_2026-11/J3088_v02/ziKBPJ6FY0U_B_v08.jpg`
- **Verified SHA-256:** `781435d9c557b1a18fbd3dba42d513f647d2a65fff2d5063b3829c7d2b522c68` (`1280×720`, `430,024` bytes)
- **Evidence inspected:** `PHONE_SHEET.jpg` (`168×94` actual pixels with `10:00` duration badge stress overlay), `SOURCE_REGISTRATION.jpg`, `REGISTRATION.json`, `DESIGN_MANIFEST.json`, `02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/01_Script/jwst_script_master_v01.md`, `jobs/reviews/J3096/REVIEW.md`, and live thumbnail A (`ziKBPJ6FY0U_live_A.jpg`, `TOO EARLY?`).
- **Colour gate (`thumb_preview.py long --score`):** `PASS` (`saturation=171.5`, `near_black=16%`).
- **Scope note:** J3129 is thumbnail-only; existing live title (`JWST Found Galaxies That Shouldn't Exist Yet`) and listing remain unchanged. No other critic files in `05_Analytics/tests/panels/owb-webb-j3129-v08/` were read.

---

## 1. Title — **7/10**
- **Live title (unchanged in J3129):** `JWST Found Galaxies That Shouldn't Exist Yet` (44 characters)
- **Critique:** At 44 characters, the title is crisp, sets an immediate curiosity gap (*"Galaxies That Shouldn't Exist Yet"*), and pays off honestly in Scene 04 (`~300 million years` after the Big Bang) without conspiracy framing. Its main weakness for a sub-1,000-subscriber channel (LEARNINGS Rule 26) is leading with the acronym `JWST` instead of the full search phrase `James Webb Telescope` that non-specialist viewers type into YouTube search.
- **Concrete rewrite (for a separate single-variable title test only; unchanged in J3129):**
  `James Webb Telescope: The Galaxies That Shouldn't Exist Yet` (59 characters)

## 2. Thumbnail at phone size (`168×94`) — **9/10**
- **Candidate text:** `GALAXIES TOO BRIGHT` (`GALAXIES TOO` white, `BRIGHT` yellow, top band `y=34..117`)
- **Critique:** Every J3096 fix landed cleanly and reads immediately at `168×94` on `PHONE_SHEET.jpg`:
  1. **Hook & band:** Three words across the top band (`GALAXIES TOO BRIGHT`, yellow `BRIGHT`), naming the subject (`GALAXIES`) and the specific astrophysics tension (`TOO BRIGHT`) from Scene 04 line 143 without touching the loupe or spacecraft inset.
  2. **Loupe, registration & pointer:** The wide JADES NIRCam deep field (`JADES_GS_z14_0_field.jpg`, rolled `-28°`) carries a clear yellow origin circle at `(468, 434, r=34)` joined by a thin white connector line without arrowhead `(512,431)–(714,379)` to the dominant `440 px` circular loupe at `(950, 373, r=220)`. The loupe is a `6.875×` linear resample (`64 -> 440 px`) of the rotated patch from the native `220×220` `JADES_GS_z14_0_cutout.png` (no new angular resolution claimed; the NASA annotated reference inset uses different framing and filter-colour assignments from the native cutout and is not byte-identical, while component geometry and orientation match). Inside the loupe, the single white pointer arrow (`tail=(1080,446)` to `tip=(982,393)`) aims directly at the right edge of the lower yellow-orange/redder target core (`JADES-GS-z14-0` centroid `(945.3, 373.8)`) without covering the core and clearly separates it from the bluer neighbour knot above-left (`(915.6, 297.4)`).
  3. **Webb inset & badge clearance:** Removing the unreadable micro-caption and enlarging the NASA JWST spacecraft illustration ~13% (`267×200 px`) inside the separate lower-left box (`[40, 475, 340, 700]`) makes the golden hexagonal mirror and sunshield unmistakable at `168×94`. The bottom-right `10:00` duration badge clears the loupe rim, pointer arrow, and inset completely.

## 3. Title + thumbnail together — **9/10**
- **Critique:** Together, `JWST Found Galaxies That Shouldn't Exist Yet` and `GALAXIES TOO BRIGHT` reinforce rather than duplicate each other. Although the noun `GALAXIES` appears in both (required by J2844/J3096 so the cover hook names its subject), the title poses the existential puzzle (*"Shouldn't Exist Yet"*) while the thumbnail delivers the physical anomaly (*"TOO BRIGHT"*) and shows the exact magnified deep-field target plus the telescope that saw it.

## 4. First 30 seconds / Short hook (`01_Script/jwst_script_master_v01.md`) — **5/10**
- **Critique:** Evaluated against Lesson 7 (`studio/RULES.md`), Scene 01 of the locked script (`lines 62–82`) holds back the payoff image and number: it opens on CG Orbit asking a soft question (*"What if the universe was already… busy…"*), plays a 2-second brand title sting before `0:10`, and spends `lines 77–81` on an agenda promise (*"Today, Orbit is going to learn beside the James Webb Space Telescope... This is JWST discoveries the Orbit way"*). The concrete 300-million-year fact does not land until Scene 04 (`line 143`). (Published video; no re-cut in J3129.)
- **Concrete rewrite (for future openings; published cut unchanged):**
  `Three hundred million years after the Big Bang, the universe should have been dark—yet the James Webb Space Telescope just confirmed a galaxy shining there hundreds of times brighter than our models predicted.` *(Open at frame 0 directly on the real JADES-GS-z14-0 deep-field zoom with no Orbit, no title sting, and no meta-agenda in the first 30 seconds.)*

## 5. Description first line and chapters — **6/10**
- **Critique:** The `RANKING_STRATEGY_v01.md` description opener (*"What the James Webb Telescope discovered that changes everything: galaxies shining too early, black holes growing too fast... Orbit's Cosmic Journey through JWST discoveries — wonder, not clickbait"*) spends prime above-the-fold characters repeating the old working title and channel tagline instead of naming specific search entities (`JADES-GS-z14-0`, `300 million years after the Big Bang`, `Little Red Dots`), while the script's `ACT I · BEGIN · ...` chapter markers read like internal production labels rather than viewer story beats. (No listing changes in J3129.)
- **Concrete rewrite (for future listing polish; unchanged in J3129):**
  - **First line:** `The James Webb Space Telescope (JWST) confirmed luminous galaxies like JADES-GS-z14-0 shining just 300 million years after the Big Bang and overmassive black holes inside "Little Red Dots" that outgrew early-universe models.`
  - **Chapters:** `0:00 Galaxies That Shouldn't Exist Yet` · `1:18 How Webb Sees Infrared Light` · `3:11 Cosmic Dawn Timeline` · `4:58 Galaxies 300 Million Years After the Big Bang` · `8:00 Overmassive Black Holes & Little Red Dots` · `11:08 Textbook Models vs JWST Data` · `13:32 What Changes in Cosmology` · `15:09 What Else Is Hiding at Cosmic Dawn?`

---

## Which would you click, and why?
I would click candidate B v08 (`GALAXIES TOO BRIGHT`) over live A (`TOO EARLY?`) because B v08 shows a real magnified NASA JWST deep-field galaxy core pinpointed by a crisp arrow alongside a recognisable Webb telescope inset and high-contrast top-band hook text, whereas live A depicts an unrelated synthetic exoplanet-spectrum graphic with all-white lower-left text over the sunshield.

## The single change that would most raise CTR
Ship candidate B v08 (`GALAXIES TOO BRIGHT`, SHA-256 `781435d9c557b1a18fbd3dba42d513f647d2a65fff2d5063b3829c7d2b522c68`) as Test & Compare arm B against live A (`TOO EARLY?`) once the elected Chief issues the exact-file PASS.
