# Packaging Brief — Space Mysteries Explained in 10 Minutes (`J3251` Draft `v01`)

- **Draft script:** `jobs/reviews/J3219/SPACE_MYSTERIES_DRAFT_SCRIPT_v01.md`
- **Sources:** `jobs/reviews/J3219/SPACE_MYSTERIES_SOURCES_v01.md`
- **Search evidence:** `jobs/reviews/J3219/SEARCH_LED_PICK_2027-01.md`
- **Status:** **Draft only** — nothing is locked, voiced, built, uploaded, or scheduled before the 22 / 26 / 30 Dec 2026 format readouts (`LEARNINGS.md` rule 34).
- **Planned slot (if Every-X wins on 30 Dec, or as the best-scoring format under the all-three-under-230 branch):** **Sunday 10 January 2027, 18:00 London** (`studio/plan.json` → `orbit-search-2027-01` step `first`).

---

## 1. Ben's July Illustrated Style Test (Mandatory Visual Lock for Sun 10 Jan 2027)

Per Ben's 20 Nov 2026 instruction and `jobs/reviews/J3219/CHIEF_REVIEW.md` §3 (`05_Analytics/tests/FORMAT_TESTS_READOUT_2026-12.md`), **Orbit's first January long (Sun 10 Jan 2027, 18:00 London)** is also Ben's **July illustrated style test**, scored on the same 14-day bars on **Sun 24 Jan 2027** (`500+` views keep style / `230–499` one more / `<230` drop):

- **Reference look:** Orbit `001` (`02_Video-Projects/001_Will-We-Ever-Meet-Aliens/production-status.md`):
  - Timing / audio / Orbit look reference: `09_Final-Export/aliens_BOLD_EXPLAINER_v06_FINAL_POLISHED_MASTER.mp4`
  - Animated-beds rebuild reference: `09_Final-Export/aliens_BOLD_EXPLAINER_v07_ANIMATED_BEDS_MASTER.mp4`
- **What carries into this film:**
  1. **Bold illustrated, animated art** across the film (clean animated motion beds — never shaky `zoompan` Ken Burns on flat PNGs, and keeping real graded NASA/ESA plates at the cold open and key scientific proof beats so `picture_qa.py` and *Teach on screen* pass).
  2. **The Orbit mascot on screen in-film** (in the illustrated overlay/story beats, tagged in the script's 2 `[ORBIT ACTS: ...]` scenes — **still never on Frame 0 before 0:30, never in the final shot, and NEVER on any thumbnail** per `studio/RULES.md` Never list).
  3. **On-screen timestamp / chapter progress indicator** (matching Orbit 001's clean bold-explainer timestamp look, kept clear of the lower-third `WHO:` cards and YouTube's bottom-right duration badge).

---

## 2. Three Query-First Titles (`≤70` chars, exact query words at the front)

All three open directly with the exact winning search query **`Space Mysteries`** (`134,000/mo`, comp `43`, `6/10` top-10 gap, `Boring Space` `118.6×` small-channel breakout), obey `LEARNINGS.md` rules 15, 23, 26, and 37, avoid fearbait ("terrifying", "doomed"), avoid hedges ("may have", "might"), and copy no public video title:

| Option | Title | Chars | Search / Rule Check | Role |
|---|---|---:|---|---|
| **Title 1 (Lead / Test Arm A)** | **`Space Mysteries Explained in 10 Minutes (6 Cosmic Puzzles)`** | `56` | Starts with exact query `'Space Mysteries'` + US autocomplete `'Space Mysteries Explained'` + proven `'in 10 Minutes'` tour shape (`064` format) + concrete `(6 Cosmic Puzzles)` scope. Zero fear, zero hedge. | **Primary upload title (Arm A)** — set before arming any Test & Compare ("title first, test second"). |
| **Title 2 (Curiosity / Paradox Arm B)** | **`Space Mysteries Science Still Can't Solve (95% Is Missing)`** | `58` | Exact `'Space Mysteries'` at words 1–2 + concrete verified number hook `(95% Is Missing)` from the 5% ordinary matter vs 95% dark matter + dark energy payoff. | **Title Test Arm B** (distinct curiosity/number hook). |
| **Title 3 (Webb / Discovery Arm C)** | **`Space Mysteries Explained: 6 Signals & Worlds That Broke Physics`** | `64` | Exact `'Space Mysteries Explained'` at words 1–3 + concrete discovery stakes (FRBs, Hubble Tension, UHZ1). Fits `≤70` chars. | **Backup / Arm C** if testing a discovery-led tail. |

---

## 3. Two Distinct Thumbnail Concepts (`THUMBNAIL_AND_TITLE_RULES.md` §2.A & §2.B)

Both concepts obey every house thumbnail lock: **NO Orbit mascot on any thumbnail**, **1 big focal subject (`≥⅓` of frame)**, **2–3 words in a top band or clear edge off the subject**, **one `#FFE000` yellow hook word + white rest**, **heavy black outline**, **never repeats the title**, **near-black `≤30%`**, **mean HSV saturation `≥120`** (pass `thumb_preview.py long --score`), readable at **`168×94`**, and completely distinct visual ideas (`LEARNINGS.md` rule 12):

### Concept A — *The Invisible 95%* (Cosmic Scale / Mystery Split)
- **Visual:** One huge, high-saturation glowing spiral galaxy filling the lower two-thirds of the frame against a lifted deep-indigo/violet starfield (near-black `≤25%`). A clean glowing cutaway / slice cleanly peels back the outer spiral rim into shimmering violet-blue gravitational-lensing arcs, with a tiny glowing `"5% VISIBLE"` scale pin pointing to the bright core so the concept reads instantly with the sound off.
- **Top-band text (off the subject, 2 words):** **`95% MISSING`** (`95%` in `#FFE000` yellow, `MISSING` in white, heavy house sans + thick black outline, ~11–12% frame height).
- **Why it works at 168 px:** One bold spiral + huge yellow `95%` number; adds what the title doesn't say; contrasts sharply with every generic black-and-red "terrifying space" thumbnail in the top 10.
- **No Orbit:** Zero Orbit mascot anywhere on the cover.

### Concept B — *The Impossible Cosmic Gap* (Bright-Contrast / Discovery Variant · Rule 14)
- **Visual:** A bright, luminous cyan-and-gold **cosmic web** filament network (testing `LEARNINGS.md` rule 14's high-contrast bright-nebula look so we don't blend into dark-space competitors) parting sharply around a stark, glowing-rimmed circular void cavity in the centre, with a tiny bright Earth/Milky-Way scale dot (`"OUR GALAXY"`) and one thin white arrow (`§2.B.4`) pointing into the vast empty bubble.
- **Top-band text (off the subject, 3 words):** **`NOTHING IS HERE`** (`NOTHING` in `#FFE000` yellow, `IS HERE` in white, top clear band, out of bottom-right duration corner).
- **Why it works at 168 px:** Instantly readable bright-web vs dark-hole silhouette; completely different object, colour family, and hook from Concept A; pairs naturally with Title 1 or Title 2 in a 2–3 arm Studio Test & Compare.
- **No Orbit:** Zero Orbit mascot anywhere on the cover.

*(Optional Concept C if running a 3-way Test & Compare on launch: **Clean Real Image**, `LEARNINGS.md` rule 19 — graded NASA Chandra + Webb UHZ1 / Abell 2744 purple-and-gold gravitational-lensing frame with 2-word top-band text **`TOO EARLY`** in yellow/white, zero composite.)*

---

## 4. Draft Description & Cluster Links (Ready for `11_Upload-Package` After 30 Dec)

- **Line 1 (exact search phrase):** *Space mysteries explained in 10 minutes: from invisible dark matter holding spinning galaxies together to millisecond radio bursts, giant cosmic voids, the Hubble Tension, an impossible early black hole, and the dark energy accelerating our universe.*
- **Story-beat chapters (HOTU/SEA rule):**
  - `0:00 Why Galaxies Don't Fly Apart (Dark Matter)`
  - `1:30 Millisecond Signals From Deep Space (Fast Radio Bursts)`
  - `3:05 The Bubbles Where Galaxies Vanish (Cosmic Voids)`
  - `4:50 The Universe Disagrees With Itself (The Hubble Tension)`
  - `6:30 The Black Hole That Grew Too Fast (UHZ1)`
  - `8:10 The Force Pushing Space Apart (Dark Energy)`
- **Sources line:** Exact `Sources:` line from `jobs/reviews/J3219/SPACE_MYSTERIES_SOURCES_v01.md`.
- **Honest production line (`studio/RULES.md`):** *Pictures: illustrated animations and AI-generated scenes alongside NASA, ESA, Chandra, Hubble and James Webb imagery. Facts: every number and date is checked against the primary sources listed above.*
- **Cluster & Companion Shorts (`2` standalone question Shorts pointing to this long once live):**
  1. *Why Don't Spinning Galaxies Fly Apart?* (16–25 s, Dark Matter 5% vs 27% hook)
  2. *What Would You See Inside the Emptiest Void in Space?* (16–25 s, ~1 atom/m³ + 1960s horizon hook)
- **End-screen hand-off:** Points to Film 2 of the January search-led cluster (*Milky Way Galaxy Explained in 10 Minutes*) or `064` (*Every Planet Explained in 10 Minutes*) until Film 2 is live.
