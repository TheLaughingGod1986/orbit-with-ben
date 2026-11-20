2026-11-19 — Gemini (Gemini 4 Argon High, covering the `cursor.md` packaging panel slot via J3110 failover)

# Packaging Critique: OWB 034 Pluto Long Upload Package & J3105 Thumbnails A/B/C

## 1. Title — **7/10** (for Lead Title A as Day-1 primary; **9/10** for Option B)

- **Lead Title A (`Why Pluto's Frozen Heart Has Zero Craters`, 41 chars): 7/10.** Sharp curiosity gap, under 50 characters, zero word overlap with thumbnails A/B/C, and paid off in the first two spoken sentences. However, for a sub-1,000-subscriber channel governed by LEARNINGS rule 26 (Search-First), nobody types `"why pluto's frozen heart has zero craters"` into cold YouTube search. Signed-out UK autocomplete for `why does pluto` ranks `"why does pluto have a heart"` at #2, and Lead Title A fails to open with that verbatim query.
- **Option B (`Why Does Pluto Have a Heart? (And Why It Has Zero Craters)`, 58 chars): 9/10.** Starts verbatim with the #2 YouTube autocomplete phrase (`Why Does Pluto Have a Heart?`), appends the zero-crater mystery in a bracketed tail under 60 characters, avoids colliding with the existing public video `Why Does Pluto Have a Heart?` (`fssbsdzMiaQ`), and shares zero words with `NITROGEN GLACIER`, `ICE MOUNTAINS`, or `FLOWING ICE`.
- **Option C (`What New Horizons Saw Inside Pluto's Frozen Heart`, 49 chars): 7/10.** Clear and targets the `new horizons pluto` cluster, but `"What X Saw"` has a weaker curiosity gap than the zero-craters paradox.
- **Option D (`The Only Spacecraft Photos Ever Taken of Pluto`, 46 chars): 8/10.** Strong real-imagery browse promise backed verbatim by NASA Pluto Facts, though it drops the heart/glacier anomaly that anchors the script and thumbnails.
- **Provisional J3105 title (`Why Does Pluto Have a Heart? (A Glacier With No Craters)`, 56 chars): 6.5/10.** Repeats `Glacier` against Thumbnail A's hook `NITROGEN GLACIER`.
- **Concrete rewrite (for anything under 8):** Promote Option B to Lead Title A in `PACKAGE_MANIFEST.json` (`"titleIndex": 2`, `"title": "Why Does Pluto Have a Heart? (And Why It Has Zero Craters)"`), and hold `"Why Pluto's Frozen Heart Has Zero Craters"` as Title Arm 2 if a two-arm title test is later run.

---

## 2. Thumbnail at phone size (168×94)

Inspected directly at 1280×720 and at 168×94 / 360×202 in `phone_review.jpg`:

- **Candidate A (`034_pluto_A_j3105_v01.jpg` — `NITROGEN GLACIER`, PIA19952 whole enhanced-colour globe): 8/10.**
  - **What works:** At 168×94, the single enhanced-colour New Horizons globe pops immediately against the lifted dark-navy background (saturation 166.0, near-black 3%). The bright cream heart of Tombaugh Regio / Sputnik Planitia on the lower-right face is unmistakable, the 2-word top band (`NITROGEN` white, `GLACIER` yellow `#ffe119`) is crisp and clear of the globe, and the bottom-right duration-badge zone is completely clear.
  - **Flaw to fix:** The globe sits in the middle ~54% of the horizontal frame with wide empty navy margins on both sides, and the bottom-left two-line label (`2,377 km / PLUTO DIAMETER`) reduces `PLUTO DIAMETER` to an unreadable 4-pixel smear at 168×94 while confusing Pluto's planetary diameter (`2,377 km`) with the width of the `NITROGEN GLACIER` (`1,000 km`).
  - **Concrete refinement:** Scale the Pluto globe up by ~18% so the bright heart commands the frame at 168×94, and replace `2,377 km / PLUTO DIAMETER` with a single bold `1,000 KM WIDE` callout (or remove the bottom-left sub-label entirely).

- **Candidate B (`034_pluto_B_j3105_v01.jpg` — `ICE MOUNTAINS`, PIA19948 oblique horizon panorama): 7/10.**
  - **Why it is under 8:** `ICE MOUNTAINS` is legible in the top band and the curving limb with backlit atmospheric haze layers is clean, with nothing under the bottom-right duration badge. However, at 168×94 in `phone_review.jpg`, the sepia-gold monochrome duotone makes Pluto look like a warm, sandy desert moon rather than −240 °C water-ice mountains, and the oblique mountain shadows flatten into generic limb texture where no individual mountain peak stands out. The thin horizontal line and end-ticks of the bottom-left `250 km` scale bar also nearly vanish at 168×94.
  - **Concrete rewrite (for B < 8):** Re-grade PIA19948 from warm sandy-gold to a cold high-contrast ice-blue/silver rim grade, crop ~15% tighter onto the jagged mountain shadow line bordering smooth Sputnik Planitia so vertical peak relief is visible at 168×94, and either drop the `250 km` scale bar or thicken its bar stroke to ≥6 px.

- **Candidate C (`034_pluto_C_j3105_v01.jpg` — `FLOWING ICE`, PIA20726 cellular plain): 5.5/10.**
  - **Why it is under 8:** At 168×94 in `phone_review.jpg`, the flat top-down crop in lime-yellow and cyan false colour has zero planetary context (no curvature, limb, or space sky) and reads like a biology microscope slide of plant cells or a geologic map rather than a world in space. The flat steel-blue rectangle (`#387d99`) pasted across the top behind `FLOWING ICE` looks like a slide-deck header banner, and the bottom-left `100 km` scale bar sits directly over busy blue-and-yellow mountain noise that swallows the bar line and outline at phone size.
  - **Concrete rewrite (for C < 8):** Drop the flat top-down lime/cyan false-colour crop and solid blue header strip; replace with an oblique close-up across Sputnik Planitia's polygonal cells meeting the dark mountain shoreline in natural cream/charcoal contrast with a dark vignette top band, or test only A vs B.

---

## 3. Title + thumbnail together — **9/10** (Option B or Lead Title A + Thumbnail A)

- Pairing **`Why Does Pluto Have a Heart? (And Why It Has Zero Craters)`** (or **`Why Pluto's Frozen Heart Has Zero Craters`**) with **Thumbnail A (`NITROGEN GLACIER`)** scores **9/10**: zero overlapping words, the title asks the search question and states the crater anomaly, and the thumbnail shows the bright heart on the real spacecraft globe while naming the surprising material (`NITROGEN GLACIER`) that answers it.
- Pairing the provisional J3105 title (`Why Does Pluto Have a Heart? (A Glacier With No Craters)`) with Thumbnail A (`NITROGEN GLACIER`) scores **6/10** because `Glacier` repeats on both.
- **Concrete rewrite (for the provisional J3105 pairing < 8):** Drop `(A Glacier With No Craters)` and pair Thumbnail A exclusively with `Why Does Pluto Have a Heart? (And Why It Has Zero Craters)` or `Why Pluto's Frozen Heart Has Zero Craters`.

---

## 4. First 30 seconds / Short hook — **9/10**

- **Long opening (`pluto_frozen_heart_script_master_v03.md` lines 3–10): 9/10.** Frame 0 opens on a real graded New Horizons natural-colour close-up of Sputnik Planitia (PIA20291) with no Orbit, no title card, and no agenda padding. Sentences 1–2 immediately answer the title with concrete scale (*"A frozen nitrogen glacier about one thousand kilometres wide — larger than Texas and Oklahoma combined — with zero craters"*). Sentence 3 lands the July 2015 New Horizons flyby distance (`12,500 km`), temperature (`−232 °C`), highland crater contrast (`260 km`), and convection mechanism before 0:25, accompanied by the `1,000 km vs 0 craters` scale graphic, and Sentence 4 sharpens the central question before 0:35 while holding the first chapter card until `1:06`.
- **Active Shorts (`J3066` Test A opening `What Did New Horizons Discover Inside Pluto's Frozen Heart?` and `J3065` Short 2 `Why Can Towering Mountains Stand on Pluto at −240°C?`): 8.5/10.** Both use question titles that their opening lines answer immediately with real New Horizons imagery and hard numbers.

---

## 5. Description first line and chapters — **7.5/10**

- **What works:** Line 1 front-loads the core search phrases (`Why does Pluto have a heart`, `nitrogen glacier`, `zero craters`, `New Horizons`). The seven chapter names (`0:00 The Heart With Zero Craters` through `9:05 Beyond the Frozen Heart`) read as story beats with verified timestamps from `cuts_v02.json`, the paused 035 Triton hand-off was properly replaced in the description with `033 Why Knocked-Sideways Uranus Has 21-Year Winters` (per J2864), and the `Sources:`, `Image credits:`, and making-of disclosure lines are complete.
- **Why it is under 8 (7.5/10):**
  1. **Line 1 repeats `"Why does Pluto"` twice inside 11 words** (`Why does Pluto have a heart — and why does Pluto's giant heart-shaped nitrogen glacier...`), wasting part of the ~140-character search snippet window.
  2. **Paragraph 3 (line 5) spoils the Chapter 4 and Chapter 5 payoffs above the fold**, explicitly giving away *"city-sized convection cells"*, *"mountains of water ice ... at minus 240 degrees Celsius"*, and the August 2026 climax (*"liquid nitrogen rises from basal melting beneath the ice"*) before a viewer clicks play.
- **Concrete rewrite (for line 1 and paragraph 3 of `pluto_frozen_heart_long_description_v01.txt`):**
  - **Line 1:** `Why does Pluto have a heart — and why does its 1,000-kilometre frozen heart have zero craters in NASA's New Horizons close-up photos?`
  - **Paragraph 3 (Line 5):** `Explore a world one-fifth the width of Earth where Sputnik Planitia — a nitrogen glacier larger than Texas and Oklahoma combined — borders three-kilometre mountains, an unmoving giant moon, and 2026 evidence of activity deep beneath the ice.`

---

## Summary Verdicts

- **Which would you click, and why?** Thumbnail A (`NITROGEN GLACIER`) paired with Title B (`Why Does Pluto Have a Heart? (And Why It Has Zero Craters)`), because at 168×94 the real enhanced-colour Pluto globe makes the bright heart immediately recognisable while `NITROGEN GLACIER` deepens the zero-crater mystery without repeating a single title word.
- **The single change that would most raise CTR:** Make Search-First Title B (`Why Does Pluto Have a Heart? (And Why It Has Zero Craters)`) the Day-1 lead title paired with Thumbnail A—with Pluto's globe scaled ~18% larger and the illegible `"2,377 km / PLUTO DIAMETER"` micro-label replaced by a bold `"1,000 KM WIDE"` heart callout (or removed).
