# Packaging Panel Critique — OWB 026 (`owb-026-nearest-star-j1823-v03`)

- **Date:** 2026-11-04
- **Critic:** Gemini (`gemini`, Gemini 4 Argon)
- **Job:** J1921 (review of J1823 v03 Proxima-only thumbnail correction, commit `80195a8a72`)

---

## 1. Title: `How Far Is the Nearest Star?` — **8 / 10**

- **What works:** 28 characters (well under the 60-character mobile cutoff), exact high-intent search query (`THUMBNAIL_AND_TITLE_RULES.md` §1.8), familiar noun (`Star`) in the first six words, zero hedging or threat clickbait.
- **Limitation:** Because the title is a straight search question ("How Far Is…") rather than a contradiction or impossibility hook, the thumbnail must carry the paradox or scale shock. Locked title unchanged per brief.

## 2. Thumbnail at phone size (`168×94`) — **6 / 10**

- **What works in v03:**
  - Astronomical accuracy is fixed: both `nearest_star_thumb_B_v03.jpg` and `nearest_star_thumb_C_v03.jpg` use the verified ESA/Hubble Proxima Centauri plate (`potw1343a`, upscale `2.12×`, within the `≤2.35×` limit) instead of the rejected Alpha Centauri A/B pair (`GSFC_20171208_Archive_e000214`).
  - At `168×94` (`comparison_true_168x94.png`), the 2-word top-band hooks (`PROXIMA HIDES` on B v03, `HIDDEN STAR` on C v03) are bold, high-contrast, and cleanly legible.
  - The NASA Blue Marble Earth inset (`[55, 490, 245, 680]`) provides an instant foreground reference (`§2.A.5`), and the bottom-right corner is completely clear of the duration badge.
- **What fails (why it scores 6/10):**
  1. **Picture-vs-text contradiction:** `potw1343a` renders Proxima as a blinding white-orange diffraction starburst filling the centre of the frame, while the hook says `PROXIMA HIDES` or `HIDDEN STAR`. A casual viewer scrolling at phone size sees a blazing Sun-like glare and wonders why the caption calls it "hidden".
  2. **Near-duplicate A/B/C test:** A (`YOU CAN'T SEE IT`), B v03 (`PROXIMA HIDES`), and C v03 (`HIDDEN STAR`) now all use the exact same `potw1343a` starburst plate and the same "it's invisible/hidden" angle. Worse, B v03 and C v03 share the exact same crop (`[0, 126, 604, 466]`) and Earth inset coordinates (`[55, 490, 245, 680]`), differing only in background colour grading (warm brown vs deep blue) and the two top words.
  3. **Diffraction spikes behind text and touching Earth:** The upper diffraction spikes cut directly behind the top text band, and the lower-left spike runs straight past the Earth cutout, visually collapsing the distance gap the film is about.
- **Concrete rewrite (for score < 8):** Keep one invisibility variant (A `YOU CAN'T SEE IT` or C's high-contrast blue background with B's non-repeating text), and rebuild the third slot (Variant C) to visually test **distance/scale**: place the Blue Marble Earth in the lower-left, reduce the `potw1343a` Proxima crop to a smaller red-orange pinpoint in the upper-right across a deep dark starfield gap, add one thin white arrow (`§2.B.4`) pointing to Proxima, and top-band the 3-word scale dare **`900M YEAR WALK`** (`900M` in yellow, `YEAR WALK` in white).

## 3. Title + thumbnail together — **7 / 10**

- **What fails (why it scores 7/10):**
  - **Title word repetition on C v03:** Title is *How Far Is the Nearest **Star**?* and C v03 reads **`HIDDEN STAR`**, directly violating `THUMBNAIL_AND_TITLE_RULES.md` §2.3 (*"The thumb adds to the title. It never repeats it"*).
  - **Unfamiliar proper noun on B v03:** **`PROXIMA HIDES`** leads with `PROXIMA`, an astronomy name the general viewer clicks to learn at `0:33`, rather than a plain-English hook (`YOU CAN'T SEE IT` on A hits harder because it addresses `YOU`).
  - **Missing distance payoff across the set:** The title asks *"How Far…?"*, yet all three thumbnails (A, B v03, C v03) state that the star is invisible/hidden; none of the three tests a distance/time hook against the invisibility hook.
- **Concrete rewrite (for score < 8):**
  - Keep **A** (`YOU CAN'T SEE IT`) as the invisibility baseline.
  - On **B v03**, keep `PROXIMA HIDES` (or swap its warm-brown sky to C v03's higher-contrast deep-blue grade so `PROXIMA HIDES` pops off the background without repeating `STAR`).
  - Rewrite **C v03**'s hook from `HIDDEN STAR` to **`900M YEAR WALK`** (yellow `900M`, white `YEAR WALK`) or **`4 YEARS AT LIGHTSPEED`** (`4 YEARS` yellow) so the title (*How Far Is the Nearest Star?*) + thumb (`900M YEAR WALK`) form an instant question-and-shock-answer pair with zero repeated words.

## 4. First 30 seconds / Short hook — **9 / 10**

- **Evidence (`Captions/nearest_star_long_v06_en-GB.srt`, `0:00–0:35`):**
  - Asks the title question by `0:07.8` (*"So how far away is the nearest one?"*).
  - Gives the first concrete answer by `0:13.5` (*"Light, the fastest thing there is, takes more than four years to cross the gap."*).
  - Lands the thumbnail's invisibility twist by `0:19.7` (*"And here is the strange part. You cannot see that star at all. Not without a telescope."*).
  - Names Proxima Centauri at `0:33.5` right after the 4-part roadmap.
- **Verdict:** Fast, concrete, and pays off both the title's distance question and the thumbnail's visibility paradox inside the first 20 seconds.

## 5. Description first line and chapters — **9 / 10**

- **First line (`nearest_star_long_description_v01.txt`):** Opens with the exact search question (*"How far is the nearest star?"*) and immediately packs the core entities (`Proxima Centauri`, `red dwarf`, `4.24 light-years away`, invisible without a telescope, four-year light travel time) into the two-line search snippet without giving away the grapefruit scale model or the 900-million-year walk numbers.
- **Chapters:** All six chapters (`0:00 How Far Is the Nearest Star?`, `0:33 The Star You Cannot See`, `2:02 Measuring the Gap`, `3:52 Shrink It Down`, `5:12 The Walk`, `6:18 Is Anyone There?`) are phrased as story beats (`AGENTS.md` Reference lessons §2) and match the locked v06 cards (`0:33, 2:02, 3:52, 5:12, 6:18`).

---

## Which would you click, and why?

**Variant A (`YOU CAN'T SEE IT`) overall—or C v03's deep-blue grade paired with B v03's non-repeating text among the new Proxima-only plates**—because `YOU CAN'T SEE IT` challenges the viewer directly in plain English, whereas `PROXIMA HIDES` assumes the viewer already knows what "Proxima" is and `HIDDEN STAR` repeats the word `STAR` from the title.

## The single change that would most raise CTR

Replace C v03's title-repeating `HIDDEN STAR` text with the 3-word distance shock **`900M YEAR WALK`** (`900M` in yellow) on the high-contrast deep-blue Proxima + Earth plate (with Proxima scaled down to a smaller pinpoint across the dark gap from Earth) so Test & Compare pits the invisibility hook (`YOU CAN'T SEE IT` / `PROXIMA HIDES`) against a visceral "How Far" answer instead of running three same-angle starbursts.
