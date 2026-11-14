2026-11-14 — gemini (`Gemini 4 Argon (High)`)

# Independent Packaging Critique: OWB Weekly Audit (`J2834_v02` — `m09jUdwC5hk`, `Mo93x0fxB1Q`, `ziKBPJ6FY0U`)

---

## Overall Panel Scores Across the 3-Video Bundle

1. **Title:** **7/10** (Live A average `7.2/10`; Proposed B average `7.5/10` — `Mo93x0fxB1Q` Title B is strong at `9/10`, while `m09jUdwC5hk` Title A/B and `ziKBPJ6FY0U` Title B fall under 8).
   - **Concrete rewrite (<8):**
     - `m09jUdwC5hk`: `How Long Will the Universe Last? (Until the Last Star Dies)` (`59` chars — replaces non-search phrasing *"Anything/Everything in Space"* with the actual head query *How Long Will the Universe Last?* without spoiling the 10-trillion-year number in the title).
     - `ziKBPJ6FY0U`: `James Webb Telescope: The Galaxies That Shouldn't Exist Yet` (`59` chars — front-loads the spelled-out `James Webb Telescope` search query under Rule 26 while preserving the anomaly curiosity gap and avoiding verbatim repetition of `300 Million Years` against Thumbnail B).
2. **Thumbnail at phone size (`168×94`):** **7/10** (`m09jUdwC5hk_B_v04` `6.5/10`, `Mo93x0fxB1Q_B_v04` `7.5/10`, `ziKBPJ6FY0U_B_v05` `7.5/10`; all three beat Live A and pass `thumb_preview.py --score` with clear bottom-right duration-badge zones, but each has one concrete phone-size flaw below).
   - **Concrete rewrite (<8):** On `m09jUdwC5hk_B_v04.jpg`, swap the flat cyan-on-blue UV plate (`PIA09178`) for the high-contrast optical+infrared crimson-and-navy Helix Nebula plate (`PIA15416`) with a sharp central white-dwarf point and change the passive top-band hook from `ALL STARS FADE` to **`10 TRILLION YEARS`** (`10 TRILLION` in `#FFE600`, `YEARS` in `#FFFFFF`).
3. **Title + thumbnail together:** **8/10** for Live Title A + Proposed Thumbnail B (`m09jUdwC5hk` `7.5/10`, `Mo93x0fxB1Q` `9/10`, `ziKBPJ6FY0U` `8.5/10`); **6.5/10** if Proposed Title B is paired with Proposed Thumbnail B on `ziKBPJ6FY0U` (`4/10` on `ziKBPJ6FY0U` because Proposed Title B and Proposed Thumbnail B both say `300 Million Years`).
   - **Concrete rewrite (<8):** Pair `ziKBPJ6FY0U` Thumbnail B (`300 MILLION YEARS`) only with Live Title A (`JWST Found Galaxies That Shouldn't Exist Yet`) or with the rewritten Title B (`James Webb Telescope: The Galaxies That Shouldn't Exist Yet`), never with a title containing `300 Million Years`.
4. **First 30 seconds / Short hook:** **4.5/10** (`m09jUdwC5hk` `6.5/10`, `Mo93x0fxB1Q` `4/10`, `ziKBPJ6FY0U` `3.5/10` — both `001` and `004` scripts open with Orbit on frame 0, a title card inside 0:15, and *"I'm Orbit — and today we're asking..."* / *"Today, Orbit is going to learn..."* meta-agenda before the first concrete fact).
   - **Concrete rewrite (<8):** Cut all `"I'm Orbit / Today we're going to..."` agenda lines and early title cards from the first 30 seconds; open cold at `0:00` on the real NASA subject plate with the concrete payoff number in sentence one (see per-video rewrites below).
5. **Description first line and chapters:** **6.5/10** (`m09jUdwC5hk` `8/10`, `Mo93x0fxB1Q` `6/10`, `ziKBPJ6FY0U` `5/10`).
   - **Concrete rewrite (<8):** Remove the trailing hashtags (`#FermiParadox ...`) from `001`, commit a canonical description + story-beat chapters file for `004` (`11_Upload-Package/Descriptions/`), and include the mandatory peer-reviewed `Sources:` line and honest AI/NASA imagery disclosure line on both `001` and `004`.

---

## Per-Video Breakdown

### 1. `T035` — `m09jUdwC5hk` (*How Long Will Anything in Space Last?* — `005` / `owb_compilation_v05`)

1. **Title — Live A: 5/10 | Proposed B (`How Long Will Everything in Space Last? (10 Trillion Years)`): 7/10**
   - **Critique:** Nobody types *"How Long Will Anything in Space Last?"* into YouTube search (`0.00%` CTR on 93 28d impressions). Proposed Title B fixes *"Anything"* to *"Everything"* and adds a scale tail, but *"Everything in Space"* is still weaker for search than *"the Universe"*, and putting `(10 Trillion Years)` in the title gives away the final countdown number when the thumbnail can carry the number instead.
   - **Concrete rewrite:** `How Long Will the Universe Last? (Until the Last Star Dies)` (`59` chars).
2. **Thumbnail at phone size (`168×94`) — Live A: 4/10 | Proposed B (`m09jUdwC5hk_B_v04.jpg`, `ALL STARS FADE`): 6.5/10**
   - **Critique:** Proposed B eliminates the synthetic red-dwarf illustration and the duplicate `THE LAST LIGHT` text (which collided with `REXYxuLOBoI`), passes `thumb_preview.py --score` (`sat=202.5`, `near_black=5%`), and leaves `x>980, y>600` clear. However, at `168×94` on `PHONE_SHEET_v02.jpg`, the UV/IR Helix Nebula (`PIA09178`) renders as a flat cyan smudge on a mid-blue background with low luminance separation, the white arrow points into a soft pink haze with no visible central white-dwarf point, and `ALL STARS FADE` is a passive statement rather than a curiosity gap.
   - **Concrete rewrite:** Use the optical+infrared Hubble/Spitzer Helix Nebula composite (`PIA15416`) so a deep crimson outer ring contrasts against dark navy around a visible white-dwarf pinpoint, and change the top-band text to **`10 TRILLION YEARS`** (`10 TRILLION` in `#FFE600`, `YEARS` in `#FFFFFF`).
3. **Title + thumbnail together — 7.5/10**
   - **Critique:** `How Long Will Anything in Space Last?` + `ALL STARS FADE` has zero word overlap, but both halves stay abstract and neither gives a concrete number or familiar entry point at `168×94`.
   - **Concrete rewrite:** Pair **`How Long Will the Universe Last? (Until the Last Star Dies)`** with Thumbnail hook **`10 TRILLION YEARS`** (or **`NOTHING LASTS`** if the `(10 Trillion Years)` title tail is kept).
4. **First 30 seconds / Short hook — 6.5/10**
   - **Critique:** The compilation (`owb_compilation_v05`) spends `0:00–0:53` (`Nothing in the sky is permanent`) on an overarching thematic intro before starting the first concrete countdown (`0:53 The Rings Are Leaving`).
   - **Concrete rewrite:** Open cold at `0:00` on Cassini footage of Saturn's rings: *"In 100 million years, Saturn's rings will vanish into the planet — and every other light in the night sky is on a countdown too, stretching ten trillion years into the future."*
5. **Description first line and chapters — 8/10**
   - **Critique:** `owb_compilation_v05_description.txt` has a strong hook line, story-beat chapters (`0:53 The Rings Are Leaving`, `10:12 The Moon Lets Go`, `18:47 Two Galaxies Meet`, `29:19 What Dead Stars Leave`, `39:04 The Last Light`), a complete peer-reviewed `Sources:` line, and the required honest AI/NASA disclosure.

---

### 2. `T036` — `Mo93x0fxB1Q` (*Why Haven't We Found Aliens Yet? The Fermi Paradox Explained* — `001_Will-We-Ever-Meet-Aliens`)

1. **Title — Live A: 8/10 | Proposed B (`Fermi Paradox: Why Haven't We Found Aliens Yet?`): 9/10**
   - **Critique:** Live Title A (`60` chars) is solid, and Proposed Title B (`47` chars) is even sharper under Rule 26: it front-loads the exact head search term `Fermi Paradox`, drops the filler word `Explained`, and saves 13 characters.
2. **Thumbnail at phone size (`168×94`) — Live A: 3/10 | Proposed B (`Mo93x0fxB1Q_B_v04.jpg`, `ZERO SIGNALS`): 7.5/10**
   - **Critique:** Proposed B is a dramatic upgrade over Live A (`SILENCE`, `near_black=42.1%`), pairing the real Goldstone 70m DSN dish (`PIA26716`) with the Milky Way Galactic Centre (`PIA12348`) and bold `ZERO SIGNALS` text (`sat=167.3`, `near_black=6%`). Two visual flaws hold it just under 8:
     1. There is a hard, unfeathered horizontal seam at `y≈72` where the dark navy top band cuts abruptly across the top of the nebula right through the middle of the letters `ZERO SIGNALS`.
     2. The yellow target reticle (`cx=875, cy=420`) is centered over the **blazing white-hot core** of the nebula, which at `168×94` visually reads as *"we locked onto a bright source"* rather than *"empty silence / zero signals"*, and the Goldstone dish highlights are clipped to flat white.
   - **Concrete rewrite:** Feather the top dark gradient smoothly over `y=0..180` to eliminate the hard horizontal line at `y=72`, pull highlights on the Goldstone dish down 15% to restore structural mesh contrast, and move the yellow reticle onto a dark dust pocket in the Milky Way (or add a small `0` / `?` callout beside the reticle) so the target reads as empty.
3. **Title + thumbnail together — 9/10**
   - **Critique:** `Why Haven't We Found Aliens Yet?` + `ZERO SIGNALS` over the radio dish and sky reticle is an ideal complementary pair: zero repeated words, and the image immediately shows the physical instrument and the zero-result paradox.
4. **First 30 seconds / Short hook (`aliens_script_v01.md`) — 4/10**
   - **Critique:** Lines 29–41 violate every J2428 opening rule: `[ORBIT: intro_wave]` and `[TITLE: Will We Ever Meet Aliens?]` before `0:15`, followed by a meta-agenda speech (*"I'm Orbit — and today we're asking one of the biggest questions humans keep returning to: will we ever meet aliens? Not in a movie. Not as a meme..."*), delaying the first concrete number (`Alpha Centauri, four light-years away`) until line 46.
   - **Concrete rewrite:** Cut lines 29–41 from the opening; start at `0:00` on the Milky Way core and Goldstone 70m dish with: *"Our galaxy holds over 100 billion stars, yet after sixty years of scanning the sky with our largest radio telescopes, we have confirmed zero alien signals — and the closest star system is still four light-years away."*
5. **Description first line and chapters (`001_Will-We-Ever-Meet-Aliens/11_Upload-Package/Descriptions/`) — 6/10**
   - **Critique:** The opening question and story-beat chapters (`00:00 Are we alone?`, `02:36 Where is everybody? The Fermi Paradox`, `07:05 The Great Filter`) read well, but the description ends with banned hashtags (`#FermiParadox #AreWeAlone #SpaceDocumentary #Aliens #OrbitWithBen`) and is missing both the mandatory `Sources:` line and the honest AI/NASA disclosure line.
   - **Concrete rewrite:** Delete the trailing hashtags, start line 1 with `The Fermi Paradox explained: with hundreds of billions of stars in the Milky Way and sixty years of radio searches, why have we detected zero alien signals?`, and add `Sources: Cocconi & Morrison 1959 (Nature), searching for interstellar communications · Drake 1961 (Green Bank conference), the Drake Equation · Hart 1975 (QJRAS), explanation for the absence of extraterrestrials on Earth · Mayor & Queloz 1995 (Nature), 51 Pegasi b.` followed by `Pictures: AI-generated scenes alongside NASA/ESA imagery. Facts: every number is checked against the sources listed below.`

---

### 3. `T037` — `ziKBPJ6FY0U` (*JWST Found Galaxies That Shouldn't Exist Yet* — `004_JWST-Discoveries-That-Change-Everything`)

1. **Title — Live A (`JWST Found Galaxies That Shouldn't Exist Yet`): 8.5/10 | Proposed B (`James Webb Telescope: Galaxies 300 Million Years After the Big Bang`): 6.5/10**
   - **Critique:** Live Title A (`44` chars) is punchy, clear, and opens a strong curiosity gap. Proposed Title B (`67` chars) front-loads the full spelled-out `James Webb Telescope` search phrase, but drops the anomaly hook ("Shouldn't Exist Yet"), runs past 60 characters, and repeats `300 Million Years` from Thumbnail B.
   - **Concrete rewrite:** `James Webb Telescope: The Galaxies That Shouldn't Exist Yet` (`59` chars).
2. **Thumbnail at phone size (`168×94`) — Live A: 3.5/10 | Proposed B (`ziKBPJ6FY0U_B_v05.jpg`, `300 MILLION YEARS`): 7.5/10**
   - **Critique:** Live A (`TOO EARLY?`, `near_black=39.9%`) showed an exoplanet transmission spectrum instead of a galaxy. Proposed B (`sat=142.1`, `near_black=6%`) fixes the subject mismatch by using the real Webb First Deep Field (`SMACS 0723`) with a `4.5×` yellow-ringed zoom loupe on a crimson lensed galaxy, clear of the duration badge (`y_bottom=573`). Two issues keep it at `7.5/10` at `168×94`:
     1. The small yellow source ring on the left (`x≈485, y≈610`) circles an almost empty dark patch of sky (while the bright white diffraction-spiked star immediately above it steals the eye), rather than circling the actual bright orange/red lensed galaxy shown inside the zoom loupe.
     2. `300 MILLION YEARS` (`17` characters across `x=61..1210`) fills nearly the entire width and states a bare number without signaling *why* 300 million years is shocking to a casual viewer who doesn't know when galaxies should form.
   - **Concrete rewrite:** Place the small yellow origin circle directly on the lensed crimson arc that appears in the zoom loupe (and dim the central white foreground diffraction star by 30%), and tighten the top-band hook to **`TOO BIG TOO SOON`** (`TOO BIG` in `#FFE600`, `TOO SOON` in `#FFFFFF`) or **`300M YRS OLD`** (`300M YRS` in `#FFE600`, `OLD` in `#FFFFFF`).
3. **Title + thumbnail together — Live Title A + Thumb B: 8.5/10 | Proposed Title B + Thumb B: 4/10**
   - **Critique:** Live Title A (`JWST Found Galaxies That Shouldn't Exist Yet`) + Proposed Thumbnail B (`300 MILLION YEARS`) work well together: the title supplies the anomaly and the thumbnail supplies the real deep-field galaxy zoom and the epoch number. However, Proposed Title B (`... Galaxies 300 Million Years After the Big Bang`) + Proposed Thumbnail B (`300 MILLION YEARS`) violates `studio/RULES.md` §2.2 by repeating `300 Million Years` verbatim on both.
   - **Concrete rewrite:** Keep `300 MILLION YEARS` paired only with `JWST Found Galaxies That Shouldn't Exist Yet` (Round 1 `T037`), and use `James Webb Telescope: The Galaxies That Shouldn't Exist Yet` for any Round 2 Title-B test.
4. **First 30 seconds / Short hook (`jwst_script_master_v01.md`) — 3.5/10**
   - **Critique:** Scene 01 (`lines 60–82`) opens on Orbit in the foreground asking a soft rhetorical question, cuts to a full title card and 2-second brand sting, and spends lines 77–81 on meta-commentary (*"Today, Orbit is going to learn beside the James Webb Space Telescope. Not to tear science down... This is JWST discoveries the Orbit way..."*), followed immediately by `CHAPTER CARD: card_01_begin` at Scene 02 (`<0:45`). The `300 million years` galaxy fact is buried in Scene 04 (line 143).
   - **Concrete rewrite:** Cut the title card, brand sting, and `"Today, Orbit is going to learn..."` intro; open at `0:00` zooming into the real SMACS 0723 crimson deep-field galaxy with: *"Just 300 million years after the Big Bang, the universe was supposed to be dark, cooling gas — instead, the James Webb Space Telescope found giant, fully-lit galaxies already shining with billions of stars."*
5. **Description first line and chapters (`004_JWST-Discoveries-That-Change-Everything/11_Upload-Package/`) — 5/10**
   - **Critique:** `004/11_Upload-Package/` has no committed `Descriptions/` or `Chapters/` file in git, and the script's chapter markers (`ACT I · BEGIN · WHAT WEBB SEES`, `ACT II · MIDDLE · THE TEXTBOOK GAP`) use internal act labels instead of viewer-facing story beats.
   - **Concrete rewrite:** Add `02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/11_Upload-Package/Descriptions/jwst_description.txt` starting with: *"The James Webb Space Telescope (JWST) discovered bright, massive galaxies just 300 million years after the Big Bang — far earlier than standard cosmological models predicted."* followed by story-beat chapters (`0:00 Galaxies That Shouldn't Exist Yet`, `2:15 Infrared Eyes on the Early Universe`, `5:40 Shining 300 Million Years After the Big Bang`, `9:20 Black Holes Too Big Too Soon`, `13:10 Why the Textbooks Need an Update`), a `Sources:` line (Labbé et al. 2023 *Nature*, Curtis-Lake et al. 2023 *Nature Astronomy*, Maiolino et al. 2024 *Nature*), and the honest AI/NASA disclosure line.

---

## Verdict

- **Which would you click, and why?** I would click **`Mo93x0fxB1Q` Proposed B (`ZERO SIGNALS` + `Fermi Paradox: Why Haven't We Found Aliens Yet?`)** because the real Goldstone 70m radio telescope aimed at a yellow target reticle over the Milky Way core turns an abstract question into an instant visual story at `168×94` (`ziKBPJ6FY0U` Proposed B `300 MILLION YEARS` with Live Title A is a close second).
- **The single change that would most raise CTR:** Replace the flat cyan-on-blue `ALL STARS FADE` plate on `m09jUdwC5hk_B_v04.jpg` with the high-contrast crimson-and-navy optical/IR Helix Nebula (`PIA15416`) + bold number hook **`10 TRILLION YEARS`**, while feathering the hard `y=72` top-band seam on `Mo93x0fxB1Q_B_v04.jpg` and rewriting `ziKBPJ6FY0U` Title B to **`James Webb Telescope: The Galaxies That Shouldn't Exist Yet`** so it never duplicates `300 MILLION YEARS` on Thumbnail B.
