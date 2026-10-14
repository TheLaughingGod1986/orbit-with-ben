# Packaging Panel Critique — OWB 024 (What Happens If You Travel Near Light Speed?)
**Date:** 2026-10-14  
**Critic:** Gemini (`gemini`)

> **Packaging manifest discrepancy noted first:** `11_Upload-Package/PACKAGE_MANIFEST.json` currently points `thumbnail` and `thumbnailAbc` to `../08_Thumbnail/j0143_v02/024_answer_j0143_v02.jpg` and `024_tease_j0143_v02.jpg` (the rendered starship plates with `YOU: 1 YEAR / EARTH: 7 YEARS` and `OUTRUN EARTH'S CLOCK`), not `08_Thumbnail/abc_v03/`. Also, `PACKAGE_MANIFEST.json` uses the title `"What Happens If You Travel Near Light Speed?"` while `01_Script/light_speed_script_master_v02.md` and the spoken end-lines of all three Shorts use `"What Happens If You Travel Near the Speed of Light?"`. Below is the critique of the `abc_v03` set and package as briefed.

---

## 1. Title — **7 / 10**
- **Current:** `What Happens If You Travel Near Light Speed?` (44 chars in manifest; 51 chars with `the Speed of Light` in script/Shorts).
- **Critique:** High search intent—people literally type this exact question into YouTube, it sits comfortably under 60 characters, and the film pays it off honestly. However, in Browse/Suggested feeds it reads like a broad textbook question rather than a personal consequence, and it disagrees with the spoken end-line recorded for the three Shorts (`"What Happens If You Travel Near the Speed of Light?"`).
- **Concrete rewrite:**
  - If optimising for Browse curiosity while keeping the search keywords: **`What Travelling Near Light Speed Does to Your Clock`** (51 chars).
  - If keeping the exact search question to match the spoken Short handoffs: standardise `PACKAGE_MANIFEST.json` to **`What Happens If You Travel Near the Speed of Light?`** (51 chars) so the listing matches the spoken end-line word-for-word.

---

## 2. Thumbnail at Phone Size (168×94, `08_Thumbnail/abc_v03`) — **5.5 / 10**
- **Variant A (`7 YEARS GONE?`) — 4 / 10:** Fails the single-subject and phone-readability tests. It puts three competing elements in one frame (dark night-side Earth on the left, a tiny Voyager probe on the lower right, and a fuzzy horizontal blue-white band behind the probe). At 168×94, the Black Marble Earth (`near_black: 0.266`) sinks into the dark background, and the Voyager probe sits at `[920, 385, 1291, 600]`—right above/inside the bottom-right duration badge zone where YouTube's timestamp crowds it. Worse, Voyager moves at 0.006% of light speed, which contradicts a near-light-speed premise.
- **Variant B (`YOU AGE SLOWER`) — 7 / 10:** By far the clearest of the three at 168×94: one large human subject (EVA astronaut), strong brightness (`near_black: 0.087`), 3 punchy words, and nothing important under the bottom-right duration badge. Its flaw is text-to-background separation: the white top line `YOU AGE` sits directly over bright white clouds and the white suit backpack, losing crispness at phone size.
- **Variant C (`ONE-WAY TRIP`) — 5 / 10:** Two clean words and an unobstructed bottom-right corner, but the subject is a grey Voyager cutout floating statically against dark navy space with a small yellow dot. At 168×94, thin grey antennas on dark blue convey zero speed, zero relativistic weirdness, and no emotional stakes.
- **Concrete rewrite:** Drop the Voyager cutout from A and C entirely. Use **Variant B's close-up astronaut** (or the `j0143_v02` relativistic starship plate already linked in `PACKAGE_MANIFEST.json`), darken the upper-right sky/clouds behind the top text line by 35–40% so white letters pop instantly at 168×94, and replace `YOU AGE SLOWER` with the sharper numerical hook **`7 YEARS GONE?`** (or **`1 YEAR = 7 YEARS`**).

---

## 3. Title + Thumbnail Together — **7.5 / 10**
- **Critique:** None of the `abc_v03` thumbnails repeat the words of the title—each answers *"What Happens If You Travel Near Light Speed?"* from a distinct angle (`7 YEARS GONE?`, `YOU AGE SLOWER`, `ONE-WAY TRIP`). However:
  - **Title + B (`YOU AGE SLOWER`)** gives away the textbook answer (`time dilation = you age slower`) before the click instead of opening a curiosity loop.
  - **Title + C (`ONE-WAY TRIP`)** paired with a Voyager probe looks like a video about Voyager leaving the Solar System, not relativistic time dilation.
  - **Title + A (`7 YEARS GONE?`)** has the best verbal synergy with the title (provoking *"Why are 7 years gone?"*), but is let down by A's cluttered, dark visual execution.
- **Concrete rewrite:** Put **A's copy (`7 YEARS GONE?`)** onto **B's high-contrast astronaut subject** (or use `j0143_v02`'s `YOU: 1 YEAR / EARTH: 7 YEARS` starship frame). That pairs the high-contrast single subject with an unresolved numerical mystery that forces the click.

---

## 4. First 30 Seconds & Short Hooks — **7.5 / 10**
- **Long script (`light_speed_script_master_v02.md`):**
  - **0:00–0:18 (Lines 3–6) is 9/10:** Immediately answers the title with a concrete scenario (*"You are gone for one year by your own watch. You land, and seven years have passed at home... The danger was never the speed. It was your own clock."*) over a rushing relativistic starfield at Frame 0.
  - **0:19–0:28 (Lines 7–8) drags it down:** *"In this film I will show you why a moving clock runs slow, what a trip near light speed would do to you and the people you leave behind, and why you can never quite reach the limit."* This 34-word table-of-contents sentence stalls momentum in the first 30 seconds right before the GPS payoff.
- **Shorts scripts (`10_Shorts/LIGHT_SPEED_SHORTS_SCRIPTS_v01.md`):**
  - **Mon (`Why Are the Clocks Above Your Head Running Fast?`) & Fri (`Muons Shouldn't Reach the Ground. They Do.`):** Both open immediately on a sharp physical contradiction.
  - **Wed (`Could a Robot Reach the Speed of Light?`):** Spoils its own title question in the first five words (*"Nothing with mass can reach light speed. Could a robot do it?"*), killing suspense at 0:01.
- **Concrete rewrite:**
  - **Long (lines 7–8):** Cut the *"In this film I will show you..."* agenda sentence when editing/tightening and cut straight from *"Your phone already depends on it every day."* to *"Every GPS satellite over your head carries an atomic clock, and every one of them drifts."*
  - **Wed Short (lines 55–60):** Open on the escalating energy wall instead of a flat "no": *"Push a one-tonne robot to ninety percent of light speed, and it takes a fifth of all the energy humanity uses in a year. Push it to ninety-nine, and it takes the whole year."*

---

## 5. Description First Line and Chapters — **7.5 / 10**
- **Critique:**
  - **First line:** `"What happens if you travel near the speed of light? Leave Earth at ninety-nine percent of light speed for one year by your own watch, and seven years pass at home."` Repeating the full 51-character title question at character 0 wastes nearly half of the ~110-character mobile search preview before the viewer sees the `1 year / 7 years` hook.
  - **Chapters:** Clean, well-paced, and curiosity-led (`0:42 Your Clock Is Already Slow`, `5:24 The Price of Every Nine`, `6:39 A One-Way Ticket to the Future`) without spoiling the 100,000-year Milky Way payoff. `3:44 The Trip` is slightly vague for search/scrubbing.
- **Concrete rewrite:**
  - **First line:** `Leave Earth at 99% of the speed of light for one year by your own watch, and seven years pass at home — here is how time dilation and special relativity actually work.` (Front-loads the hook in the first 100 chars while keeping `speed of light`, `time dilation`, and `special relativity` in the snippet).
  - **Chapter 3:44:** Rename `3:44 The Trip` to `3:44 The Twin Paradox Trip`.

---

## Which would you click, and why?
Within `abc_v03`, **Variant B (`YOU AGE SLOWER`)**, because at 168×94 the close-up astronaut is the only image with instant contrast and a single recognisable subject, whereas A and C are dark navy frames with a tiny, slow-looking Voyager cutout—though **`j0143_v02` (`YOU: 1 YEAR / EARTH: 7 YEARS` over the relativistic starship)** beats all three `abc_v03` options on both visual speed and curiosity gap.

## The single change that would most raise CTR
Replace the static Voyager cutout thumbnails in `abc_v03` with a single high-contrast subject (either the `j0143_v02` relativistic starship already referenced in `PACKAGE_MANIFEST.json`, or Variant B's astronaut with a darkened top-right sky) paired with the numerical time-gap text **`7 YEARS GONE?`** (or **`YOU: 1 YEAR / EARTH: 7 YEARS`**) instead of `YOU AGE SLOWER`.
