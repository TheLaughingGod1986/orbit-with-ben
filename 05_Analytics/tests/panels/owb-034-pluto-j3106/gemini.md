2026-11-19 — Gemini (`gemini`)

# Packaging Critique: OWB 034 Pluto Long Upload Package & J3105 Thumbnails A/B/C

## 1. Title — **7/10** (Lead A: *Why Pluto's Frozen Heart Has Zero Craters*; Option B is **8.5/10**)
- **Critique:** `PACKAGE_MANIFEST.json` sets *Why Pluto's Frozen Heart Has Zero Craters* (41 chars) as Lead Title A and pushes *Why Does Pluto Have a Heart? (And Why It Has Zero Craters)* (58 chars) to Option B. Nobody types `"why pluto's frozen heart has zero craters"` into YouTube search; the package's own signed-out autocomplete check proves the actual search query is `"why does pluto have a heart"`. Under LEARNINGS Rule 26 (Search first, 9 Nov 2026) and the 10 Nov 2026 title-test rule, the search-led phrase must be Lead Title A from day one before any test is armed. Lead A also assumes the viewer already knows Pluto has a heart instead of hooking the general viewer with the famous feature first and the zero-crater anomaly second.
- **Concrete rewrite:**
  Promote Option B to Lead Title A (`titleIndex: 1`, `PACKAGE_MANIFEST.json` `"title"`):
  **`Why Does Pluto Have a Heart? (And Why It Has Zero Craters)`** (58 characters).

## 2. Thumbnail at phone size (168×94) — **6.5/10** (A: **7/10**, B: **6.5/10**, C: **4.5/10**)
- **Critique of A (`NITROGEN GLACIER`, PIA19952 globe — 7/10):**
  1. **Visible rectangular paste seam:** A darker-navy rectangular/octagonal bounding-box halo surrounds the Pluto cutout against the flat `#0d2544` background (visible above the northern limb, along the upper-right diagonal cut, and down the left edge).
  2. **Undersized globe:** Pluto spans only ~41% of frame width (~520 px of 1280 px), leaving wide empty navy margins while Sputnik Planitia occupies only ~15% of the 168×94 tile.
  3. **Misleading/unreadable secondary label at 168×94:** Bottom-left `2,377 km / PLUTO DIAMETER` has no caliper or scale line, `PLUTO DIAMETER` collapses into an illegible 3-pixel smear at 168×94, and pairing a floating `2,377 km` with `NITROGEN GLACIER` makes `2,377 km` read as the glacier's width (actual glacier width: `1,000 km`).
- **Critique of B (`ICE MOUNTAINS`, PIA19948 horizon — 6.5/10):**
  1. **Wrong temperature colour cue:** The warm golden-ochre duotone makes a −240 °C ice world look like Martian desert dust or Titan haze rather than frozen Pluto.
  2. **Dark lower-left shadow mass:** At 168×94, the mountain relief merges into dark shadow above the tiny `250 km` scale bar.
- **Critique of C (`FLOWING ICE`, PIA20726 cellular plain — 4.5/10):**
  1. **Unrecognizable as space imagery at 168×94:** The flat crop of convection polygons in acid lime-yellow and electric blue looks like a microscope slide of biological cells or stained tissue, with zero planetary limb or space context.
  2. **Flat UI header bar and cluttered scale bar:** The solid teal banner (`#3a849f`) creates a hard poster-style horizontal seam, reduces contrast under the yellow word `ICE`, and the bottom-left `100 km` bar sits over noisy blue-and-yellow blocks where it disappears at 168×94.
- **Concrete rewrite:**
  Rebuild **Thumbnail A** (`PIA19952`): feather/mask Pluto's circular limb cleanly onto a smoothly graded deep-navy background to eliminate the rectangular bounding-box seam; scale the Pluto globe up by 25–30% so Sputnik Planitia dominates the frame below the top text band; and replace the floating `2,377 km / PLUTO DIAMETER` corner text with a single crisp **`1,000 km`** caliper bar across Sputnik Planitia. Re-grade **Thumbnail B** from warm golden-amber to cold ice-blue/silver rim lighting, and replace **Thumbnail C** with a natural/cool-graded oblique view of Sputnik Planitia that preserves a recognizable planetary horizon and drops the solid teal header slab.

## 3. Title + thumbnail together — **7/10**
- **Critique:** While J3106 removed literal word overlap between the titles and J3105 hooks (`NITROGEN GLACIER`, `ICE MOUNTAINS`, `FLOWING ICE`), **Thumbnail A (`NITROGEN GLACIER`) and Thumbnail C (`FLOWING ICE`) prematurely answer the title's "Why" mystery on the cover**. If the title asks *Why Pluto's Frozen Heart Has Zero Craters* (or *Why Does Pluto Have a Heart? (And Why It Has Zero Craters)*), telling the viewer `NITROGEN GLACIER` in a dry textbook noun phrase resolves the anomaly instead of heightening the contradiction. Meanwhile, Thumbnail B (`ICE MOUNTAINS`) shifts focus away from the craterless heart promised by the title.
- **Concrete rewrite:**
  Pair Lead Title **`Why Does Pluto Have a Heart? (And Why It Has Zero Craters)`** with a 2-word top-band hook on Thumbnail A that sharpens the anomaly rather than spoiling the mechanism: **`STILL ALIVE`** (yellow: `ALIVE`) or **`STILL MOVING`** (yellow: `MOVING`). Alternatively, if testing Title C (*What New Horizons Saw Inside Pluto's Frozen Heart*), change Thumbnail A's hook to **`ZERO CRATERS`** (yellow: `ZERO`).

## 4. First 30 seconds / Short hook — **8.5/10**
- **Critique:** The locked `v03` script and `v02` master open on a real moving New Horizons close-up of Sputnik Planitia (`PIA20291`) with no Orbit, no title card, and the first chapter card held until `1:06`. Sentence 1 takes 21 words (~7.5 s) of scene-setting (`"Across Pluto's horizon, in distant orbit around our Sun..."`) before landing `"icy heart"`, which is slightly wordy for Frame 0 of Test A Short 1 (`J3066`), but Sentence 2 immediately delivers the concrete payoff (`1,000 km wide — larger than Texas and Oklahoma combined — with zero craters`) by ~0:14 and stacks the July 2015 flyby, `12,500 km`, `−232 °C`, `260 km` craters, and convecting nitrogen cells before `0:30`. No rewrite required (VO and master v02 are locked and pass all J2428 first-30-second gates).

## 5. Description first line and chapters — **7.5/10**
- **Critique:** The seven chapter titles (`0:00` to `9:05`) are strong story beats rather than catalogue labels, timestamps match the final `v02` cut, and the series line properly points to `033 Why Knocked-Sideways Uranus Has 21-Year Winters` under the J2864 pause rule. However, Description Line 1 (`"...why does Pluto's giant heart-shaped nitrogen glacier have zero craters..."`) and Paragraph 3 (`"...where a thousand-kilometre nitrogen glacier called Sputnik Planitia churns with city-sized convection cells... and liquid nitrogen rises from basal melting..."`) spoil both the nitrogen-glacier answer and the Chapter 4/5 basal-melting twist inside the above-the-fold search snippet.
- **Concrete rewrite:**
  Rewrite Description Line 1 and Paragraph 3 so they capture the exact search terms (`why does Pluto have a heart`, `zero craters`, `New Horizons`, `Sputnik Planitia`) while holding back the convection and basal-liquid answers for the video:
  - **Line 1:** `Why does Pluto have a heart — and why did NASA's New Horizons spacecraft find zero craters inside a thousand-kilometre basin larger than Texas and Oklahoma combined?`
  - **Paragraph 3:** `Explore a world one-fifth the width of Earth where Sputnik Planitia shows not a single impact crater, towering mountains stand two to three kilometres tall at minus 240 degrees Celsius, and a 2026 analysis of New Horizons data uncovered a surprising new clue beneath the surface.`

---

## Which would you click, and why?
**Candidate A (`034_pluto_A_j3105_v01.jpg`)** — it is the only candidate immediately recognizable as Pluto at 168×94, with high crimson-vs-cream contrast around the heart-shaped Sputnik Planitia basin.

## The single change that would most raise CTR
Promote **`Why Does Pluto Have a Heart? (And Why It Has Zero Craters)`** to Lead Title A and rebuild Thumbnail A with the Pluto globe scaled 30% larger (cleaning the rectangular crop seam), a **`1,000 km`** caliper bar across the heart instead of the misleading `2,377 km` corner text, and the anomaly hook **`STILL ALIVE`** instead of the textbook spoiler `NITROGEN GLACIER`.
