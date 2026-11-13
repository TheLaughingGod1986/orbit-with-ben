2026-11-13 — Gemini (`gemini`, Gemini 4 Argon High)

# Packaging Panel Critique — OWB 019 Andromeda Whole-Galaxy Revision (`J2729_v02` / `J2734`)

## Verified Evidence & Hashes (`META_v02.json`)
- **Video ID:** `ojk-dfOpAmw` (OWB 019 — Andromeda × Milky Way Collision)
- **Proposed Title:** `Milky Way Andromeda Collision (What Happens to Our Sun?)` (56 characters)
- **Proposed Cover Text:** `STARS RARELY HIT` (`RARELY` in yellow, `STARS` and `HIT` in white)
- **Candidate File (`019_andromeda_package_A_v02_ojk-dfOpAmw.jpg`):**
  - Path: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/019_Andromeda-Milky-Way-Collision/08_Thumbnails/repackage_2026-11/J2729_v02/019_andromeda_package_A_v02_ojk-dfOpAmw.jpg`
  - SHA-256: `8371a323ea5bc3b856c9409d10115d7d8fb1bd5d095ba534bcd95f472df1935c` (1280×720, 692,954 bytes; `saturation=158.3`, `near_black=7%`)
- **True 168×94 Comparison (`019_v02_comparison_168x94.png`):**
  - Path: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/019_Andromeda-Milky-Way-Collision/08_Thumbnails/repackage_2026-11/J2729_v02/019_v02_comparison_168x94.png`
  - SHA-256: `5daddbed420925df0ef740fffd2d7ab5f2e3e8734ef4fae7e3b593142a613fe4`
- **Phone Tile (`019_v02_phone.png`):**
  - SHA-256: `5afbb61b79b361d6cb4b329229db2d612742fc4705b7cde9b7a309d95842c7e1`
- **Preserved Live Baseline (`thumb_packaging_v01_ojk-dfOpAmw.jpg`):**
  - Title: `What Happens During the Milky Way Andromeda Collision?` (54 characters)
  - Cover Text: `THIS IS ANDROMEDA` (`ANDROMEDA` in yellow)
  - SHA-256: `250c9980986f2b5e3faca5399e7a8ce19e6711ca5de7d6f05bf78140b2bb2515`
- **Source Plate:** NASA/JPL-Caltech GALEX ultraviolet M31 mosaic (`PIA15416`, local SHA-256 `88ed2cf29704895a32427c02be2daea6204f113e30f11aac4ff789c0de29a87d`, decoded 9400×7000 RGB pixels identical to official JPEG `c5d235a4425db34d7ffd652d249ad8059ff47f558d401f148e0d5ea37d135261`, mean absolute difference `0.0`). Small `NASA/JPL-Caltech` credit included at bottom-left.

---

## Scores (1–10) & Concrete Rewrites for Anything Under 8

### 1. Title — **8/10**
- **Critique:** `Milky Way Andromeda Collision (What Happens to Our Sun?)` (56 characters) obeys the search-first rule (`LEARNINGS` rule 26) by opening with the exact head phrase (`Milky Way Andromeda Collision`) and adding a concrete, familiar stake in the bracketed tail (`(What Happens to Our Sun?)`). It stays under 60 characters, avoids fear-bait, and pays off directly in `[CHAPTER CARD: Would We Survive?]` (script lines 103–115: the Solar System likely survives stellar pass-through, keeping its planets under a reshaped Milkomeda sky). Its only slight friction is the split noun-stack + parenthesis format rather than a single natural question, and no measured search demand is claimed.

### 2. Thumbnail at phone size (168×94) — **7/10**
- **Critique:** Looking directly at `019_v02_comparison_168x94.png` and `019_v02_phone.png`, the whole-galaxy reframing fixes the earlier cropping issues: the bright core and both ends of the spiral disk sit cleanly in the frame (>1/3 area), `STARS RARELY HIT` is crisp in the top band off the galaxy disk, contrast/saturation are strong (`saturation=158.3`, `near_black=7%`), and the bottom-right duration badge corner is completely clear. However, two weaknesses keep it below an 8:
  1. **Deflating qualifier hook (`STARS RARELY HIT`):** Making the adverb `RARELY` the yellow focal word tells the viewer that nothing dramatic happens before they click, softening the visual stakes.
  2. **No visual encounter or scale cue (`THUMBNAIL_AND_TITLE_RULES.md` §2.A.5):** The plate shows a single isolated spiral galaxy floating calmly in dark blue space. At 168×94 there is no visual cue of a *collision*, a second galaxy, or *our Sun*.
- **Concrete rewrite:** Keep the whole-galaxy `PIA15416` framing and strictly qualified script truth (lines 73 and 105: *"Stars Almost Never Hit"* / *"Stars rarely collide"*), but replace the low-energy adverb `RARELY` with a sharper 3-word top-band contradiction—**`ALMOST NO CRASHES`** (`NO` in yellow) or **`GRAVITY, NOT CRASHES`** (`GRAVITY` in yellow)—or add a small house-style pointer/scale marker for `OUR SUN?` so the thumbnail visually connects to the title's question.

### 3. Title + thumbnail together — **7.5/10**
- **Critique:** The pair eliminates all word repetition (unlike the baseline, which repeated `Andromeda` in both title and `THIS IS ANDROMEDA` cover). However, the two elements partially short-circuit each other's curiosity loop: the title asks `What Happens to Our Sun?` during the collision, and the thumbnail immediately answers the collision threat with `STARS RARELY HIT`, lowering urgency before the click instead of making the viewer wonder *how* two galaxies can merge without smashing the Sun.
- **Concrete rewrite:** Pair `Milky Way Andromeda Collision (What Happens to Our Sun?)` with a 3-word top-band hook that heightens the paradox of a bloodless galactic merger—**`ALMOST NO CRASHES`** (`NO` in yellow) or **`TWO GALAXIES MERGE`** (`MERGE` in yellow)—so the viewer clicks to find out how the Sun survives when two entire galaxies pass through each other.

### 4. First 30 seconds / Short hook (`andromeda_collision_script_master_v03.md`) — **6/10**
- **Critique:** Although the VO is locked and out of edit scope for J2729, evaluating the script's opening against the current 30-second hook rules (`studio/RULES.md` Lesson 7, J2428) shows three clear weaknesses:
  1. Line 9 is an explicit table-of-contents agenda sentence (*"We ride the timeline: how the night changes first · what 'collision' actually means for stars and planets · why Earth might live through it..."*).
  2. `[CHAPTER CARD: The Second Spiral]` lands at line 11 (~0:20), well before the 0:45 chapter-card floor.
  3. The new title's specific hook (`Our Sun`) is not named in the first 30 seconds (the first concrete speed number, `110 km/s`, waits until line 34, and the Sun survival answer waits until line 105 / 7:11).
- **Concrete rewrite (for future openings; locked 019 VO unchanged):** Cut the line-9 agenda and the early chapter card, and front-load the concrete numbers and the Sun stake in the first 20 seconds:
  > *"A second spiral galaxy is already in your night sky, 2.5 million light-years away — and it is closing in on our Sun at 110 kilometres a second. When Andromeda and the Milky Way finally meet, stars almost never hit, yet gravity will completely rewrite the sky above Earth."*

### 5. Description first line and chapters (`11_Upload-Package/description.txt`) — **7.5/10**
- **Critique:** The first line (*"The Milky Way Andromeda collision: in about 4 billion years, the Andromeda galaxy fills our sky — and the galaxies don't smash into fireworks."*) front-loads the primary search phrase and sets up the core contradiction cleanly, and the chapters read as story beats (*The Honest Clock*, *When the Night Sky Rewrites*, *Stars Almost Never Hit*, *Would We Survive?*). However, the word **`Sun`** never appears anywhere in `description.txt`, leaving the new title's parenthetical hook (`What Happens to Our Sun?`) unreinforced in search metadata.
- **Concrete rewrite (if description edits are ever opened; excluded in J2729):**
  > *"The Milky Way Andromeda collision: in about 4–5 billion years, the Andromeda galaxy will fill our night sky — here is what actually happens to our Sun and Earth when two galaxies meet without smashing into fireworks."*
  (And update chapter `7:11 Would We Survive?` to `7:11 What Happens to Our Sun?`.)

---

## Which would you click, and why?
**Proposed A v02 (`Milky Way Andromeda Collision (What Happens to Our Sun?)` + `STARS RARELY HIT`)**, because it pairs a concrete personal stake (`Our Sun`) with a counter-intuitive claim over a well-framed whole galaxy, whereas the baseline (`What Happens During the Milky Way Andromeda Collision?` + `THIS IS ANDROMEDA`) wastes the thumbnail on a redundant museum label.

## The single change that would most raise CTR
Replace the tension-deflating yellow adverb in **`STARS RARELY HIT`** with a sharper 3-word contradiction still faithful to the locked script—**`ALMOST NO CRASHES`** (`NO` in yellow, from Chapter 4 *Stars Almost Never Hit*) or **`GRAVITY, NOT CRASHES`** (`GRAVITY` in yellow)—so the cover creates a paradox against `Collision` instead of telling the viewer nothing happens.

---

## Scope & Constraint Verification
- Independent critique only; no other critic files in `05_Analytics/tests/panels/owb-019-andromeda-j2729-v02/` were read.
- No Studio actions, no description or script edits, no spend. Package B remains excluded. `J2449` stays held until the panel synthesis (`J2736`) and separate elected-Chief exact-file decision (`J2737`). Baseline `thumb_packaging_v01_ojk-dfOpAmw.jpg` unchanged; Black Hole `T002` and Jupiter `T030` untouched.
