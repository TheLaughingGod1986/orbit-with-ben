# Packaging Panel Critique — OWB 064 (*Every Planet Explained*)

- **Date:** 2026-11-25
- **Critic:** Gemini (`gemini`, independent critic — `J3717`)
- **Reviewed files:** `BUILD_REPORT_v01.md`, `THUMB_SCORES_v01.json`, `SHOT_LIST_v01.md`, `TOPIC_GO_NO_GO_SHEET.md`, `every_planet_explained_script_master_v04.md`, and all four NAS thumbnail JPEGs (`064_thumbs_ABC_v01_preview_sheet.jpg`, `064_thumb_A_all_8_worlds_v01.jpg`, `064_thumb_B_464c_to_minus224c_v01.jpg`, `064_thumb_C_real_nasa_photos_v01.jpg`) inspected directly at full resolution and `168x94` phone size. Other critics' files in this folder were not read.

---

## 1. Titles — **6 / 10** overall

**Runtime mismatch across the set:** `SHOT_LIST_v01.md` locks the VO at `683.86 s` (`11:24`) and the total timeline at `701.86 s` (`11:42` with the 18 s end-screen hold). Putting `in 10 Minutes` right next to an `11:42` YouTube duration badge creates an immediate, unnecessary credibility gap before a click.

- **Title 1 — `Every Planet Explained in 10 Minutes (Mercury to Neptune)` (57 chars): 7 / 10**
  - Hits the `#1` search query (`Every Planet Explained`, 20,191/mo) and the proven small-channel completeness format, and stays under 60 chars.
  - Fails on curiosity gap and `LEARNINGS.md` Rule 26(b): the bracketed tail `(Mercury to Neptune)` is pure textbook padding—every searcher already knows the planets run Mercury to Neptune. Zero stakes, zero contrast, and `10 Minutes` understates the `11:42` badge.
  - **Concrete rewrite:** `Every Planet Explained in 11 Minutes (Real NASA Views)` *(54 chars — keeps search phrase + honest runtime, replaces redundant order list with our sharpest differentiator without over-claiming video "footage")*.

- **Title 2 — `Every Planet Explained: From Mercury's Ice to Neptune` (53 chars): 6 / 10**
  - Drops the `in N Minutes` completeness/runtime promise that drives small-channel breakouts (`6/9/10/20 Minutes` outliers in `TOPIC_GO_NO_GO_SHEET.md`).
  - Lopsided tail: Mercury gets a sharp contradiction (`Ice`), then the sentence dies flatly on `Neptune` with no second extreme.
  - **Concrete rewrite:** `Every Planet Explained: 430°C Ice to Supersonic Winds` *(53 chars — keeps exact search phrase, pairs Mercury's 0:05 hook with Neptune's finale, under 60 chars, avoids the 10-vs-11-minute clash)*.

- **Title 3 — `Every Planet Explained in 10 Minutes With Real NASA Footage` (59 chars): 6 / 10**
  - **Payoff / honesty risk:** `Real NASA Footage` over-promises on a shot list that is ~35% Python code graphics (`R03`, `R05`, `R10`, `R16`, `R23`, `R28`, `R31`, `R34`, `R37`, `R41`, `R43`, `R48`, `R50` + 7 chapter cards), relies mostly on NASA still photos/mosaics (`PIA*`), and includes two AI-generated Orbit Omni clips (`R14`, `R17`) under the altered-content disclosure. Also clashes with the `11:42` badge and repeats Thumbnail C's text verbatim.
  - **Concrete rewrite:** `Every Planet Explained in 11 Minutes (With Real NASA Views)` *(59 chars — honest about stills + clips, matches `11:42`, does not promise pure video footage)*.

---

## 2. Thumbnails at Phone Size (`168x94`) — **4.5 / 10** overall

All three pass `thumb_preview.py --score` numerically only by distorting the art (periwinkle-blue fake sky in A, nuked `242.3` saturation in B, clipped dark strips in C). None is ready to ship as built.

- **Thumbnail A (`064_thumb_A_all_8_worlds_v01.jpg` — `ALL 8 WORLDS`): 4 / 10**
  - **What fails at `168x94`:**
    1. **No single focal point** (`THUMBNAIL_AND_TITLE_RULES.md` §2.1): eight tiny circular stickers strung across the middle leave >60% dead background. Mercury and Mars collapse to tiny specks; Uranus blows out to a featureless white-cyan disc; Saturn's rings nearly disappear and collide awkwardly with Jupiter on the left and Uranus on the right.
    2. **Cheap PowerPoint look:** space has been painted a bright flat periwinkle/cornflower-blue gradient with speckled white paint dots just to beat the `≤30%` near-black check (`3.7%` near-black).
    3. **Sloppy cutouts:** thick harsh black rings/halos outline Mercury, Venus, Earth, Jupiter, Uranus, and especially Neptune (heavy black rim artifact), plus a blurry pale-blue rectangle glow around Saturn.
    4. **Zero emotion or danger:** `ALL 8 WORLDS` is a dry catalogue label.
    5. *(Minor positives: top-band text is readable at `168x94` and off the planets; bottom-right duration corner is clear.)*
  - **Concrete rewrite:** Replace the bright periwinkle background and speckled dots with a rich deep-navy cosmic backdrop (~15–22% near-black), strip every hard black cutout outline, let a large clean **Saturn + Jupiter** dominate >40% of the lower-centre/left with the remaining six worlds cleanly spaced in depth without overlapping Saturn's rings, and swap `ALL 8 WORLDS` for **`8 EXTREME WORLDS`** (`EXTREME` in `#FFE000`, top band off the globes).

- **Thumbnail B (`064_thumb_B_464c_to_minus224c_v01.jpg` — `464°C TO -224°C`): 6 / 10**
  - **Strength:** By far the best thumb-stopping power and colour contrast at `168x94`; fills the frame with instant hot-vs-cold drama and keeps the bottom-right corner safe.
  - **What fails:**
    1. **Factual subject error:** `-224°C` (`-224.2 °C`, 49 K) is **Uranus's** minimum atmospheric temperature (explicitly stressed as a surprise in Chapter 7 of the locked script: *"colder than Neptune in some places"*), yet `BUILD_REPORT_v01.md` and the image place `-224°C` directly over **Neptune** (`PIA01492`, unmistakable Great Dark Spot + white scooter clouds). Space viewers will spot and call out the mismatch immediately.
    2. **Oversaturated to the point of misidentification:** `sat 242.3` nukes Venus (`PIA00271` Magellan false-colour radar) into looking like a close-up of the **Sun**, and turns Neptune radioactive neon cyan. Without reading the title, a phone viewer reads "Sun vs Neptune", not "Every Planet".
    3. **Text placement violation (`§2.B.2`):** `464°C TO -224°C` sits directly on top of both planets and straddles the bright vertical white divider line right through `TO`, muddying the centre at `168x94`.
    4. **No scale/human reference** (`§2.A.5`).
  - **Concrete rewrite:** Swap the right half to real **Uranus** (`PIA18182` or JWST ringed cyan Uranus) so `-224°C` matches the actual planet (or keep Neptune and change the split text to `464°C` | `2,000 KM/H`); pull saturation down from `242` to **`~155–170`** so Venus clearly reads as a planet; shift both globes down slightly into a clean dark top band and place **`464°C`** (`#FFE000`) on the left and **`-224°C`** (white) on the right **completely off the globes and clear of the white divider**, with a tiny crisp Apollo 17 Earth scale reference sitting on the lower-centre seam (well clear of the bottom-right badge).

- **Thumbnail C (`064_thumb_C_real_nasa_photos_v01.jpg` — `REAL NASA PHOTOS`): 3 / 10**
  - **What fails at `168x94`:**
    1. **Severe visual glitch on Saturn (left panel):** Cassini backlit Saturn (`PIA17172`) has a bizarre flat dark-grey circle with a thick bright/black cutout outline slapped across its globe, slicing straight through the ring plane. At `168x94` it looks like a censored blacked-out disc rather than Saturn.
    2. **Violates Rule 19 and `§2.1` / `§2.A.4`:** `BUILD_REPORT_v01.md` claims C tests Rule 19 (*"one clean real image thumbnail: a single striking real spacecraft frame, graded, with 0–3 words, no composite"*), yet C is a **three-panel vertical strip composite** that crops every planet into narrow slices.
    3. **Dead middle panel + top bar leak:** Juno's Great Red Spot reads as a blurry tan-orange smudge at `168x94`, with a flat dark-brown empty bar visible at the very top edge behind `"NASA"` because the crop did not reach the canvas top; the tiny Earth sticker sits awkwardly near the bottom edge.
    4. **Text violates `§2.B.2`:** `REAL NASA PHOTOS` crosses both vertical white dividers and sits on top of Jupiter and Neptune; it also carries zero emotional or curiosity hook.
  - **Concrete rewrite:** Scrap the 3-strip composite and actually run **Rule 19**: use **one uncropped, full-bleed, un-glitched real NASA hero frame**—either Cassini's full backlit Saturn (`PIA17172`, clean with no mask artifact) or Juno's full-bleed Great Red Spot (`PIA21775`) with a crisp Apollo 17 Earth scale inset on the lower-left and a thin white pointer (`§2.B.4`)—graded to `sat ~135–150` / `≤25%` near-black, with 2–3 words cleanly in the top edge off the planet: **`ACTUAL NASA VIEWS`** or **`REAL SPACE PHOTOS`** (only if the title does not repeat "NASA").

---

## 3. Title + Thumbnail Together — **5 / 10**

- **Title 1 + Thumb A (`Every Planet Explained in 10 Minutes (Mercury to Neptune)` + `ALL 8 WORLDS`):** Triple conceptual repetition ("Every Planet" + "Mercury to Neptune" + "ALL 8 WORLDS"). Neither adds curiosity or contrast to the other.
- **Title 3 + Thumb C (`...With Real NASA Footage` + `REAL NASA PHOTOS`):** Direct verbatim word repetition (`REAL NASA`), violating `THUMBNAIL_AND_TITLE_RULES.md` §2.3 and `studio/RULES.md` ("Cover text never repeats the title").
- **Title 1 + Thumb B (`Every Planet Explained...` + `464°C TO -224°C`):** The **only** genuinely complementary pair in the package—title gives the search query and completeness promise, thumbnail adds the visceral physical extreme with zero repeated words—but currently weakened by Title 1's dead tail and Thumb B's Neptune/`-224°C` factual error.
- **Concrete rewrite (lead pairing):** Pair **`Every Planet Explained in 11 Minutes (Real NASA Views)`** with the **rebuilt Thumbnail B** (`464°C` Venus | `-224°C` Uranus, text off the globes, saturation ~160)—zero repeated words, search query up front, honest runtime, authenticity in the title, visceral physical shock on the cover.

---

## 4. First 30 Seconds / Opening Hook (`v04` script + `SHOT_LIST_v01.md`) — **6 / 10**

- **What works:** No meta-agenda line, no Orbit before `0:30`, no chapter card before `0:45`, first line ends at `6.52 s` (`< 8 s`), and concrete numbers (`430 °C`, `58 million km`, `7×`, `-180 °C`) land by `25.04 s`.
- **What fails:**
  1. **Shot list breaks the `≤ 4 s` picture-change rule (`studio/RULES.md` Lesson 7, J2428 rule 5) on EVERY opening row:**
     - `R01` holds a single asset (`PIA15162`) for **`7.10 s`** (`0.00–7.10 s`).
     - `R02` holds `PIA16523` for **`4.35 s`** (`7.10–11.45 s`).
     - `R03` holds **one continuous code graphic** (`code_graphic_064_r03_mercury_temp.mp4`) for **`14.25 s`** (`11.45–25.70 s`) inside the first 30 seconds—directly contradicting `script v04` `[VISUAL MUST]` which required real MESSENGER terminator plates alternating with the graphic at 3.5–4 s cuts.
     - `R04` holds `PIA17386` for **`7.15 s`** (`25.70–32.85 s`).
  2. **Early loop closure + missing 8-planet confirmation in speech:** The title promises all 8 planets, yet the locked VO opens on a narrow Mercury ice question (`0:00–0:06.5`), answers it completely by `0:11` (closing the only open loop), and never mentions that we are sweeping outward through all eight worlds before diving into Colombo's 1965 spin resonance at `0:25`. (The `TOPIC_GO_NO_GO_SHEET.md` line *"Eight worlds orbit our Sun—and the closest one, Mercury..."* was lost in the locked VO.)
- **Concrete rewrite (edit-level, £0, preserving locked VO `4b478fcd`):** Re-cut `0:00–0:33` into strict `≤ 3.8 s` visual beats and sell the 8-planet scope visually at frame 0:
  - `0.00–3.50 s`: real rotating Mercury (`PIA15162`) with a sleek **8-planet progress strip highlighting `01 / 08 MERCURY`** at the top/lower-third so viewers immediately see the full 8-world journey ahead.
  - `3.50–7.10 s`: hard cut to high-contrast sunlit Mercury crater limb (`PIA17386`).
  - `7.10–11.45 s`: cut at `9.3 s` from wide polar mosaic (`PIA16523`) to tight Prokofiev permanent-shadow close-up (`2.2 s` + `2.15 s`).
  - `11.45–25.70 s`: break `R03` into **4 beats**—`11.45–15.00 s` real bright sunlit MESSENGER limb (`PIA17386`), `15.00–20.50 s` animated `430 °C vs −180 °C` code graphic (`5.5 s`, cut in half from `14.25 s`), `20.50–23.50 s` real Mercury day/night terminator plate (`PIA19411`), `23.50–25.70 s` shadowed crater floor (`PIA16523`).
  - `25.70–32.85 s`: split `R04` into two `≤ 3.6 s` Mercury plates carrying the Colombo WHO card and `1965` timeline tick.

---

## 5. Description First Line & Chapters — **5 / 10**

- **Description first line — MISSING (0 / 10 on delivery):** Neither `BUILD_REPORT_v01.md` nor `11_Upload-Package/` includes a drafted description or first line. `LEARNINGS.md` Rule 26(c) requires the exact search phrase (`every planet explained`) in line 1, and `studio/RULES.md` Packaging §2 requires the 5-part order (subject line, story-beat chapters, Sources line, agency credits, honest AI/fact-check line).
- **Chapters — 7 / 10 on their own:** Timestamps match `SHOT_LIST_v01.md` (`0:00`, `1:22`, `2:38`, `4:12`, `5:25`, `6:47`, `8:17`, `9:45`) and every planet name is clean for Google/YouTube Key Moments. However:
  1. `5:25 Jupiter — The Ocean of Metallic Hydrogen` **spoils the midpoint twist** (*"Case closed? Wrong — there is no solid surface"*) before viewers reach it.
  2. `6:47 Saturn — Disappearing Rings and the Hexagon Storm` (47 chars) and `8:17 Uranus — Knocked Sideways Into 21-Year Winters` (46 chars) run long for mobile Key Moments and give away the Uranus punchline up front.
- **Concrete rewrite:**
  - **Description first line:** `Every planet explained in 11 minutes — a fast, fact-checked tour of all eight worlds in our Solar System from Mercury to Neptune, built with real NASA, ESA, and spacecraft imagery.`
  - **Tightened chapters (search-clean, mobile-safe, zero midpoint spoiler):**
    - `0:00` Mercury — Ice at 430 °C
    - `1:22` Venus — The Backwards Furnace
    - `2:38` Earth — The Shielded Ocean World
    - `4:12` Mars — The Frozen Robot Desert
    - `5:25` Jupiter — What Happens If You Land?
    - `6:47` Saturn — Vanishing Rings & Polar Hexagon
    - `8:17` Uranus — The Planet Knocked Sideways
    - `9:45` Neptune — Supersonic Winds at the Edge

---

## Which would you click, and why?

**Title 1 (`Every Planet Explained in 10 Minutes (Mercury to Neptune)`) + Thumbnail B (`464°C TO -224°C`)** — it is the only combination whose cover actually stops a phone scroll with bold visual contrast and adds new stakes to the search promise instead of repeating "all planets" over pasted circular stickers or a glitched three-strip crop, even though B needs its Uranus/`-224°C` factual error fixed before upload.

## The single change that would most raise CTR

**Rebuild Thumbnail B as the lead cover—putting real Uranus on the `-224°C` half (fixing the Neptune mismatch), pulling saturation down from `242` to `~160` so Venus reads as a planet rather than the Sun, and moving `464°C` and `-224°C` cleanly off both globes into a dark top band split left/right of the centre seam—paired with an honest 11-minute title whose bracketed tail sells real NASA views instead of `(Mercury to Neptune)`.**
