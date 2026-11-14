# 2026-11-12 — Gemini (Gemini 4 Argon High)
**Packaging Panel Critique: J2374 OWB Weekly Thumbnail Audit — 3 Draft Bs (`2fsQcea-voM`, `Yk1tLh23rko`, `b8-X_FyJnHM`)**

---

## Acting Chief Fact-Check: `2fsQcea-voM` (`NO MORE ECLIPSES`)

- **Fact check:** As the Moon recedes at ~3.8 cm/yr, its apparent angular diameter eventually falls below the Sun's minimum apparent angular diameter (~600 million years from now). **Total solar eclipses** end; **annular solar eclipses** ("ring of fire") and **lunar eclipses** (Earth's shadow on the Moon) continue. The film's own script science lock (`013_Why-The-Moon-Is-Slowly-Leaving-Us/01_Script/SUNDAY_MOON_LONG_WHY_THE_MOON_IS_LEAVING_US.md` L10) states: *"totals give way to annular eclipses."*
- **Verdict:** **Needs a word (`TOTAL` or `LAST TOTAL`).** While colloquial viewers often equate "eclipses" with totality, `NO MORE ECLIPSES` is literally false for both lunar and annular solar eclipses and invites easy "well actually" corrections in comments. Because the top band allows 3 words, swapping one word gives **100% factual accuracy with zero loss of punch**:
  - **Rewrite:** **`NO TOTAL ECLIPSES`** (yellow `TOTAL` or `ECLIPSES`, 3 words, 17 chars) or **`LAST TOTAL ECLIPSE`** (yellow `LAST`, 3 words, 18 chars).

---

## Cross-Batch Diagnosis: Rubber-Stamped Layout Breaks Scale & Story

Looking at `THUMB_PREVIEW_SCORE_SHEET.jpg` and `PHONE_SHEET_v01.jpg` side by side exposes a systemic flaw across all three Draft Bs: `build_weekly_thumbs_j2374.py` applies the **exact same mechanical template** to three completely different physical stories (1-line top band + small Apollo 17 Blue Marble Earth at bottom-left + large sphere at center-right on a smooth radial gradient). While all three pass the automated saturation (`124.4`, `132.5`, `213.8`) and near-black (`3%–5%`) numeric gates, **pasting a smaller Earth next to a larger hero sphere backfires on two of the three thumbnails** and leaves the third missing its promised weather effect at phone size:

1. **On `Yk1tLh23rko` (`20 KM WIDE`):** A neutron star is ~20 km across (city-sized) and Earth is 12,742 km across, yet Draft B draws the neutron star **3.9× wider than Earth** (`~576 px` vs `148 px`) in the same unframed space. Without a zoom callout cone or city comparison, the picture visually tells the viewer "this star is 4× larger than Earth" while the text says `20 KM WIDE`.
2. **On `2fsQcea-voM` (`NO MORE ECLIPSES`):** The Moon (`1,737 km` radius) is drawn **2.2× wider than Earth** (`490 px` vs `220 px` diameter) and graded blazing solar amber-gold (`R=1.28, G=0.94, B=0.52`). At `168×94`, a small Earth beside a giant glowing orange-yellow sphere reads as **Earth next to the Sun** (or a giant approaching body), not a receding Moon grown too small to cover the Sun.
3. **On `b8-X_FyJnHM` (`RAINS MOLTEN GLASS`):** The diagonal glass-rain streaks (`width=2`, `alpha=90`, Gaussian blur `1.0`) completely vanish at `168×94`, leaving a calm blue marble (`HD 189733 b`) next to a smaller blue marble (`Earth`).

---

## Per-Video Scores & Rewrites (1–10)

### 1. `2fsQcea-voM` — `013_Why-The-Moon-Is-Slowly-Leaving-Us`
- **Live Title:** `Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone` (67 chars)
- **Proposed Separate Title B:** `Why Does the Moon Drift 3.8 cm Farther Every Year?` (50 chars)
- **Live Thumb A:** `LEAVING US?` (`sat=25.0`, `near_black=79%` — FAIL)
- **Draft Thumb B:** `NO MORE ECLIPSES` (`sat=124.4`, `near_black=5%` — PASS)

1. **Title: 7/10 (Live) · 8.5/10 (Proposed Title B)**
   - *Critique:* The live title (67 chars) truncates on mobile after *"Why the Moon Is Slowly Leaving Us — and What..."* and its tail (*"When It's Gone"*) implies the Moon escapes Earth's gravity entirely, contradicting the script's science lock (*"The Moon stays bound"*). Proposed Title B (`Why Does the Moon Drift 3.8 cm Farther Every Year?`, 50 chars) uses the proven "One real number" shape (`THUMBNAIL_AND_TITLE_RULES.md` §1.1), starts with the search phrase, and fits mobile cleanly.
   - *Concrete rewrite (for Live Title < 8):* **`Why Does the Moon Drift 3.8 cm Farther Every Year?`** (50 chars) or **`Why Is the Moon Slowly Drifting Away From Earth?`** (48 chars).
2. **Thumbnail at phone size (`168×94`): 6/10**
   - *Critique:* Huge contrast and saturation upgrade over Live A (`sat 124.4` vs `25.0`), and the top-band typography is crisp at `168×94` and clear of the bottom-right duration badge. However, it fails visual logic in two ways: (a) coloring the Full Moon bright orange-yellow and sizing it **2.2× larger than Earth** makes it look like the Sun or a scorching giant planet rather than our Moon receding; (b) `NO MORE ECLIPSES` overstates the physics (only *total* solar eclipses end) and nothing in the image shows either an eclipse or outward motion.
   - *Concrete rewrite:* Change text to **`NO TOTAL ECLIPSES`** (or **`LAST TOTAL ECLIPSE`**) and either (a) show an **annular "ring of fire" solar eclipse** where the shrunk lunar silhouette fails to cover the solar disc (with small Earth in lower-left), or (b) make Earth larger in the foreground (`~340 px`) and the warm Moon smaller (`~260 px`) in the upper-right with a clean white recession arrow/arc between them.
3. **Title + thumbnail together: 8/10**
   - *Critique:* Unlike Live A (`LEAVING US?`, which repeated the title words), Draft B adds the concrete consequence (losing totality) to the title's cause (the Moon drifting away). Pairing Proposed Title B (*Why Does the Moon Drift 3.8 cm Farther Every Year?*) with **`NO TOTAL ECLIPSES`** creates a clean cause-and-payoff gap.
4. **First 30 seconds / Short hook: 5/10**
   - *Critique:* Line 1 of `SUNDAY_MOON_LONG_WHY_THE_MOON_IS_LEAVING_US.md` (L16) violates the 8 Nov 2026 long-hook rule (`studio/RULES.md` Lesson 7: *"no agenda or meta-promise"*): *"The Moon is leaving us. In this film I will show you why it is drifting, what Earth was like when it was close, and what happens when it is gone."* It spends the first 20 seconds on two "I will show you" agenda sentences before naming the Apollo mirrors or the 3.8 cm/yr measurement.
   - *Concrete rewrite (0:00–0:20 VO):* **"Every year, the Moon steps 3.8 centimetres farther from Earth—measured to the millimetre by lasers fired at mirrors Apollo astronauts left in the dust. It will never break free of Earth's gravity, but that quiet drift will eventually end every total solar eclipse on Earth."**
5. **Description first line and chapters: 6.5/10**
   - *Critique:* The snapshot description is currently empty (`''`) in the analytics snapshot, and the script's first chapter card (`A Measured Gap`) is a vague poetic label rather than a search/story beat.
   - *Concrete rewrite:*
     - *Description line 1:* **"Why is the Moon drifting away from Earth at 3.8 cm per year—and when will the Moon be too far away for a total solar eclipse?"**
     - *Chapters:* `0:00 The 3.8 cm Laser Proof` · `1:45 When the Moon Filled the Sky` · `3:50 How Ocean Tides Push the Moon Away` · `6:10 The Final Total Solar Eclipse`.

---

### 2. `Yk1tLh23rko` — `007_What-Happens-To-Your-Body-Near-A-Neutron-Star`
- **Live Title:** `What Happens If You Get Near a Neutron Star or Pulsar?` (54 chars)
- **Proposed Separate Title B:** `What Happens to Your Body Near a Neutron Star?` (46 chars)
- **Live Thumb A:** `CRUSHED FLAT` (`sat=102.6`, `near_black=42%` — FAIL; text touches star rim, inpainted smudge at centre)
- **Draft Thumb B:** `20 KM WIDE` (`sat=132.5`, `near_black=3%` — PASS)

1. **Title: 7.5/10 (Live) · 9/10 (Proposed Title B)**
   - *Critique:* Live title appends *"or Pulsar?"*, which dilutes the visceral personal stakes with a taxonomy term and softens "Your Body" into "You Get Near". Proposed Title B (`What Happens to Your Body Near a Neutron Star?`, 46 chars) restores the exact "body impossibility" winner shape (`THUMBNAIL_AND_TITLE_RULES.md` §1.1) and cuts 8 characters.
   - *Concrete rewrite (for Live Title < 8):* **`What Happens to Your Body Near a Neutron Star?`** (46 chars).
2. **Thumbnail at phone size (`168×94`): 5.5/10**
   - *Critique:* Using the clean un-inpainted `t=465.00s` plate and moving the text into the top band fixes Live A's central smudge, rim collision, and `42%` near-black fail. **However, `20 KM WIDE` next to a miniature Earth is a visual self-contradiction:** the neutron star is drawn nearly **4× the diameter of Earth** right beside it, so the viewer's eye reads "giant star dwarfing Earth" while the words say "20 KM WIDE". Furthermore, replacing `CRUSHED FLAT` with `20 KM WIDE` strips away the physical danger/body hook that makes a viewer click a "What happens to your body" video (`0.00%` CTR on 69 impressions needs visceral stakes, not a diameter stat).
   - *Concrete rewrite:* Keep the clean `t=465.00s` neutron star plate and lifted background (`sat=132.5`, `near_black=3%`), **remove the contradictory miniature Earth** (or replace it with an astronaut silhouette/city skyline scale bar), and use the top-band hook **`CRUSHED TO ATOMS`** (yellow `ATOMS`) or **`CRUSHED FLAT`** (yellow `FLAT`, positioned cleanly in the top band off the star rim).
3. **Title + thumbnail together: 6/10**
   - *Critique:* With the live title (*What Happens If You Get Near a Neutron Star or Pulsar?*) or Proposed Title B (*What Happens to Your Body Near a Neutron Star?*), the viewer is promised an extreme physical experience, but Draft B's thumbnail (`20 KM WIDE` + giant star dwarfing Earth) pivots to a confusing size claim that contradicts the graphic.
   - *Concrete rewrite:* Pair **`What Happens to Your Body Near a Neutron Star?`** with top-band hook **`CRUSHED TO ATOMS`** (or if keeping `20 KM WIDE`, show the 20 km neutron star hovering over a **city skyline / London / Manhattan silhouette** instead of a shrunk Earth).
4. **First 30 seconds / Short hook: 7/10**
   - *Critique:* In `neutron_star_script_master_v01.md` (L3–13), lines 7–8 are strong (*"Space itself would try to tear you into a line of atoms — and your eyes would see light bend into a ring before you could blink"*), but lines 3–5 open on Orbit hanging in the dark before the subject payoff, and lines 9–13 ask four consecutive rhetorical questions (*"So what actually happens... What would you see? What would you feel? And at what point..."*) instead of delivering the first concrete number (1.4 solar masses in 20 km) before 0:20.
   - *Concrete rewrite (0:00–0:20 VO):* **"Step near a neutron star and gravity wouldn't just pull you down—it would stretch your body into a stream of atoms while bending the star's own light into a glowing ring. That is what happens when the mass of our entire Sun is crushed into a sphere just 20 kilometres wide."**
5. **Description first line and chapters: 7/10**
   - *Critique:* In `neutron_star_long_chapters_v02.txt`, `0:00 Orbit hangs in the dark` wastes the first chapter timestamp on character blocking instead of search/story keywords; the rest (`1:13 The Corpse of a Star`, `2:16 Density You Can't Imagine`, `3:36 What You Would See`, `5:46 What You Would Feel`, `7:40 The Surface That Isn't a Floor`) are strong experiential beats.
   - *Concrete rewrite:*
     - *Description line 1:* **"What would actually happen to your body if you got close to a neutron star or pulsar—from gravitational lensing and magnetic fields to extreme tidal forces?"**
     - *Chapter 0:00:* Change `0:00 Orbit hangs in the dark` to **`0:00 Approaching a 20 km Star`**.

---

### 3. `b8-X_FyJnHM` — `003_Exoplanets-Strangest-Alien-Worlds`
- **Live Title:** `Alien Worlds: The Strangest Planets We've Ever Found` (52 chars)
- **Proposed Separate Title B:** `What Are the Strangest Planets We've Ever Found?` (48 chars)
- **Live Thumb A:** `A GIANT EYE?` (`sat=33.0`, `near_black=16%` — FAIL; grey eyeball planet, white text over bright left limb)
- **Draft Thumb B:** `RAINS MOLTEN GLASS` (`sat=213.8`, `near_black=4%` — PASS)

1. **Title: 8/10 (Live) · 8.5/10 (Proposed Title B)**
   - *Critique:* Both titles are clean, under 55 chars, and match high-intent exoplanet search phrasing. Proposed Title B (`What Are the Strangest Planets We've Ever Found?`, 48 chars) converts the colon-catalogue prefix (`Alien Worlds:`) into the direct question shape (`THUMBNAIL_AND_TITLE_RULES.md` §1.8) and puts the search phrase first.
2. **Thumbnail at phone size (`168×94`): 7/10**
   - *Critique:* Best of the three Draft Bs by far. Replacing the dull grey eyeball (`sat=33.0`) with cobalt-blue `HD 189733 b` (`sat=213.8`) and top-band `RAINS MOLTEN GLASS` (yellow `GLASS`) creates instant verbal intrigue and high mobile contrast. **What holds it below an 8 at `168×94`:** the 28 diagonal glass-rain lines (`width=2`, `alpha=90` in `build_weekly_thumbs_j2374.py` L249–255) are **completely invisible at `168×94`**, and because `HD 189733 b` is blue/white swirl and `Earth` is blue/white swirl on a blue background, the thumbnail at phone size looks like **two calm blue Earths sitting in blue space**—nothing on screen looks like sideways molten glass rain.
   - *Concrete rewrite:* Make the sideways silicate rain **visibly dramatic at `168×94`**: draw 12–16 bright cyan-white/amber specular streaks (`width=5–8 px`, `alpha=210–245`, with bright leading tips) whipping horizontally across `HD 189733 b`'s terminator and trailing into space so the violent sideways storm reads at phone size, and darken the background navy (`base_rgb=(10, 16, 42)`) so the cobalt planet and bright rain streaks pop instead of blending into a blue-on-blue field.
3. **Title + thumbnail together: 9/10**
   - *Critique:* Textbook synergy. The title asks the broad search question (*Alien Worlds: The Strangest Planets We've Ever Found* / *What Are the Strangest Planets We've Ever Found?*), and the thumbnail answers with one shocking, concrete physical specimen (`RAINS MOLTEN GLASS`) without repeating a single word.
4. **First 30 seconds / Short hook: 5/10**
   - *Critique:* `exoplanets_script_master_v01.md` (L62–86) is an early-era script that violates almost every current 0:30 retention rule (`studio/RULES.md` Lesson 7): frame 0 is Orbit floating over a dark Earth hillside (`no alien planet yet`), there is a ~2 s brand title sting at ~0:08, and lines 76–86 are pure meta-agenda (*"Today, Orbit is going on a tour... This is exoplanets explained the Orbit way..."*) with **zero concrete exoplanet names or numbers in the first 30 seconds**.
   - *Concrete rewrite (for future openings; live video cannot be re-cut):* Open at frame 0 directly on cobalt-blue `HD 189733 b` whipped by 8,700 km/h winds pelting molten silicate glass sideways, naming the planet and wind speed before 0:15.
5. **Description first line and chapters: 7.5/10**
   - *Critique:* `exoplanets_long_description_v01.txt` has a strong keyword-rich opening line (*"Alien worlds — Orbit visits the strangest planets we've ever found: diamond crusts, glass rain sideways, three suns, hot Jupiters, and eyeball exoplanets"*), but the chapter list opens with generic filler (`0:00 — Orbit's question`, `0:55 — What is an exoplanet?`) and line 19 contains 11 hashtags (current rules cap or avoid hashtag clutter).
   - *Concrete rewrite:* Change the first two chapter labels to **`0:00 Worlds Beyond Our Solar System`** and **`0:55 Why Alien Planets Break the Rules`**, and strip the hashtag block on line 19 down to at most 3 relevant tags (or none).

---

## Explicit Answers to `2026-11-09_DESIGN_REVIEW.md` Questions

1. **`2fsQcea-voM` (`NO MORE ECLIPSES`):** It is a major colour/readability upgrade over Live A (`sat 124.4` vs `25.0`, `near_black 5%` vs `79%`) and eliminates title repetition (`LEAVING US?`). However, at `168×94` it **does not read as our Moon receding from Earth**: because the Moon is rendered **2.2× the diameter of Earth** and tinted blazing solar orange-gold with no recession arrow or eclipse ring, it reads as Earth beside the Sun. And factually, `NO MORE ECLIPSES` needs the word `TOTAL` (`NO TOTAL ECLIPSES`).
2. **`Yk1tLh23rko` (`20 KM WIDE`):** Moving the text to the top band and using the clean `t=465.00s` plate fixes Live A's rim overlap and inpaint smudge, **but `20 KM WIDE` paired with a miniature Earth (`148 px`) beside a giant neutron star (`~576 px`) fails the visual read at `168×94`**. Drawing the 20 km star nearly 4× larger than the 12,742 km Earth visually contradicts `20 KM WIDE`, and `20 KM WIDE` drops the visceral body-danger hook that matches the title.
3. **`b8-X_FyJnHM` (`RAINS MOLTEN GLASS`):** Yes on concept, colour (`sat=213.8`), and verbal hook—replacing the grey eyeball (`A GIANT EYE?`) with `HD 189733 b` and `RAINS MOLTEN GLASS` is a clear winner. Visually, however, the `width=2, alpha=90` rain streaks disappear completely at `168×94`, leaving two calm blue globes (Earth and `HD 189733 b`) on a blue gradient. Thickening and brightening the horizontal glass-rain streaks so they read at `168×94` will make the picture match the words.
4. **Separate Title-Only B Proposals:**
   - `2fsQcea-voM`: **`Why Does the Moon Drift 3.8 cm Farther Every Year?`** (**8.5/10**) — strong search phrasing, exact laser-ranging figure, under 55 chars, fixes the live title's misleading *"When It's Gone"* tail, and has zero word overlap with `NO TOTAL ECLIPSES`.
   - `Yk1tLh23rko`: **`What Happens to Your Body Near a Neutron Star?`** (**9/10**) — cleaner, shorter (46 chars), and higher-curiosity than `...Get Near a Neutron Star or Pulsar?`.
   - `b8-X_FyJnHM`: **`What Are the Strangest Planets We've Ever Found?`** (**8.5/10**) — clean direct search question (48 chars) with zero overlap with `RAINS MOLTEN GLASS`.

---

## Which would you click, and why?
**`b8-X_FyJnHM` Draft B (`RAINS MOLTEN GLASS`)**, because it pairs a broad high-curiosity planet search title with a specific, visceral, high-contrast physical phenomenon ("rains molten glass") that makes you want to see how a blue Earth-Looking world could rain liquid glass sideways.

## The single change that would most raise CTR
**Stop using the same "small Earth bottom-left + giant sphere right" template on objects smaller than Earth (`2fsQcea-voM` Moon and `Yk1tLh23rko` Neutron Star): fix the inverted scale (make the Moon smaller/receding or an eclipse ring under `NO TOTAL ECLIPSES`, and show the neutron star with a visceral hook like `CRUSHED TO ATOMS` or over a city scale instead of 4× larger than Earth), and make the sideways glass-rain streaks on `b8-X_FyJnHM` thick and bright enough (`5–8 px`) to actually read at `168×94`.**
