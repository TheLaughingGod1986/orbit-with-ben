# Packaging Critique — OWB 024 (What Happens If You Travel Near Light Speed?)
**Date:** 2026-10-14  
**Critic:** Gemini (`gemini`, covering `cursor` panel slot for J0248)

---

## 1. Title — **8.5 / 10**
- **Current:** `What Happens If You Travel Near Light Speed?` (44 characters)
- **Critique:** Exact high-intent search phrasing, well under the 60-character ceiling, zero clickbait, and directly paid off in the first 15 seconds. It trades a little emotional edge for search clarity, which is the right call when paired with a time-dilation thumbnail hook.

## 2. Thumbnail at Phone Size (168×94) — **6.5 / 10 (`abc_v03`) · 7.5 / 10 (`j0143_v02` in manifest)**
> **Package note:** The job brief names `08_Thumbnail/abc_v03`, while `PACKAGE_MANIFEST.json` currently wires `08_Thumbnail/j0143_v02` (`024_answer_j0143_v02.jpg` and `024_tease_j0143_v02.jpg`). Both sets are scored below.

### `abc_v03` Variants
- **Variant A (`7 YEARS GONE?`) — 5 / 10:** Split between two competing subjects (a dark night-side Earth on the left and a tiny Voyager probe on the bottom right). At 168×94, Earth's dark oceans sink into the navy background, the horizontal blue starfield band looks like a pasted rectangle, and the probe (`[920, 385, 1291, 600]`) sits directly in the bottom-right duration-badge zone.
- **Variant B (`YOU AGE SLOWER`) — 7 / 10:** Best contrast and legibility in `abc_v03` at 168×94, with 3 punchy words and nothing critical under the duration badge. However, a routine ISS EVA suit reads as low-Earth-orbit maintenance rather than near-light-speed flight, muting the sense of speed and danger.
- **Variant C (`ONE-WAY TRIP`) — 6 / 10:** Clean silhouette and badge clearance, but Voyager (`PIA17049`) is an unmanned 1970s probe moving at 0.006% of light speed; nothing in the frame conveys "you" or relativistic motion.

### `j0143_v02` Variants (currently wired in `PACKAGE_MANIFEST.json`)
- **Answer (`YOU: 1 YEAR / EARTH: 7 YEARS`) — 7.5 / 10:** The relativistic starship racing left-to-right through blue-shifted star streaks is a much stronger single hero subject than `abc_v03`. Two flaws hold it under 8: (1) six tokens across two wide lines break the 2–3 word rule and crowd the top frame at 168×94, and (2) the bright engine exhaust plume sits in the bottom-right corner where the duration badge covers it.
- **Tease (`OUTRUN EARTH'S CLOCK`) — 7 / 10:** Cleaner 3-word copy, but "OUTRUN EARTH'S CLOCK" is more abstract than the concrete 1-year-vs-7-years time shock, and shares the same bottom-right engine-plume badge collision.

- **Concrete rewrite (for Thumbnail < 8):** Flip the `j0143_v02` relativistic starship horizontally so it flies right-to-left (putting the bright engine glow on the bottom-left, completely clear of the bottom-right duration badge) and cut the top copy to **3 words**: **`7 YEARS GONE`** (`7 YEARS` in yellow, `GONE` in white).

## 3. Title + Thumbnail Together — **8.5 / 10**
- **Critique:** Zero word repetition between title and thumbnail across all variants. The title asks the physics/search question (`What Happens If You Travel Near Light Speed?`) and the thumbnail immediately supplies the human consequence (time dilation / lost years at home).

## 4. First 30 Seconds / Short Hook — **9 / 10**
- **Critique:** Opens cold on Frame 0 with relativistic starfield aberration and lands the core twist in the first 15 seconds (`You are gone for one year by your own watch. You land, and seven years have passed at home... The danger was never the speed. It was your own clock.`), then grounds it in everyday GPS reality before 0:45. No wasted throat-clearing.

## 5. Description First Line and Chapters — **7.5 / 10**
- **Critique:** The first two sentences nail search keywords (`travel near the speed of light`, `time dilation`, `special relativity`) and hook the viewer with the 1-year vs 7-years premise. The 6 chapter titles (`0:00` to `6:39`) are clean and curiosity-driven. However, the end of paragraph 2 spoils the final chapter's climax (`why a ship at one Earth gravity could cross the Milky Way in a little over twenty years of the crew's time while a hundred thousand years pass at home`) before the viewer even starts watching.
- **Concrete rewrite (for Description paragraph 2 ending):** Replace the last clause of paragraph 2 with: `...and why a ship accelerating at one Earth gravity could cross the entire Milky Way within a single crew lifetime—at an irreversible cost to everyone left on Earth.`

---

## Which would you click, and why?
**`024_answer_j0143_v02.jpg` (`YOU: 1 YEAR / EARTH: 7 YEARS`)** (or `abc_v03` **Variant B `YOU AGE SLOWER`** if restricted strictly to `abc_v03`), because the concrete 1-year-vs-7-years time gap paired with a visibly fast relativistic ship creates an instant human stakes gap that a static Voyager dish cannot.

## The single change that would most raise CTR
**Use the `j0143_v02` relativistic starship plate (flipped so the engine flare clears the bottom-right duration badge) with the 3-word copy `7 YEARS GONE` (`abc_v03` A's short copy on `j0143_v02`'s high-speed ship plate).**
