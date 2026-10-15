# Packaging Panel Decision — OWB 024 (`What Happens If You Travel Near Light Speed?`)

**Date:** 2026-10-15  
**Job:** J0249 (`gemini`, rerouted from Claude while out of usage; Chief's PASS stands on `DECISION.md`)  
**Critiques weighed:** `gemini.md` (J0247), `cursor.md` (J0248). *(Note: `J0246` for `codex.md` remains queued while Codex is marked down for usage/credit; the two completed critiques agree on every item below.)*

---

## 1. Title — **KEEP**
- **Decision:** Keep **`What Happens If You Travel Near Light Speed?`** (44 characters) in `11_Upload-Package/PACKAGE_MANIFEST.json`.
- **Why:** Scored 7/10 (`gemini.md`) and 8.5/10 (`cursor.md`). Exact high-intent search phrasing, well under 60 characters, zero clickbait, and answered directly in the first 15 seconds. (Only one critique scored it under 8, so under the 2-of-3 panel rule the existing search title stands.)

---

## 2. Thumbnail (`abc_v03` vs `j0143_v02`) — **KEEP `j0143_v02` Answer as Variant A + BUILD Codex Variant B (`J0250`, `T004`)**
- **Panel consensus (both scored `< 8`):**
  1. **Retire `abc_v03` Variants A and C:** Both critics flagged the dark-navy Voyager cutouts (`light_speed_thumb_A_7-years-gone.jpg`, `light_speed_thumb_C_one-way-trip.jpg`) for weak phone-size contrast, badge-zone crowding (`[920, 385, 1291, 600]`), and depicting a 0.006%-$c$ probe instead of relativistic flight. `PACKAGE_MANIFEST.json` already superseded `abc_v03` with `08_Thumbnail/j0143_v02/`.
  2. **Variant A (keep):** **`08_Thumbnail/j0143_v02/024_answer_j0143_v02.jpg`** (`YOU: 1 YEAR / EARTH: 7 YEARS` over the blue-shifted relativistic starship plate; `saturation=194.4`, `near_black=19%`). Both critics picked this as the strongest existing cover.
  3. **Variant B (build as Test & Compare B — queued as `J0250` for Codex, logged as `T004` in `05_Analytics/tests/THUMB_LEDGER.json`):**
     - **Single highest-CTR change agreed by both critics:** Combine the high-contrast `j0143_v02` relativistic starship plate (`08_Thumbnail/j0143_v02/024_ship_plate_j0143_v02.jpg`) with the 3-word numerical time-gap copy **`7 YEARS GONE`** (`7 YEARS` in house yellow, `GONE` in house white), and flip the ship horizontally (flying right-to-left) so the bright engine exhaust flare sits in the bottom-left corner, completely clear of YouTube's bottom-right duration badge.
     - **Output path:** `02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/08_Thumbnail/j0143_v02/024_panel_b_7_years_gone.jpg`.

---

## 3. Title + Thumbnail Together — **KEEP (with Variant B test)**
- **Decision:** Keep the question-title + time-cost-cover pairing (`What Happens If You Travel Near Light Speed?` + `YOU: 1 YEAR / EARTH: 7 YEARS` as A vs `7 YEARS GONE` as B). Zero word repetition between title and cover.

---

## 4. First 30 Seconds & Short Hooks — **KEEP**
- **Decision:** Keep the locked `v05d` long cut and locked VO as-is.
- **Why:** Both critics scored the 0:00–0:18 cold open 9/10 (`"You are gone for one year by your own watch. You land, and seven years have passed at home... The danger was never the speed. It was your own clock."`), and 024's VO and picture are locked under `AGENTS.md` ("No rework: 021 (live), 022 (scheduled), 023 (v05e approved) and 024 (v05 in review)").

---

## 5. Description (`11_Upload-Package/Descriptions/light_speed_long_description_v01.txt`) — **CHANGE**
- **Panel consensus (both scored `7.5 / 10`):**
  1. **Front-load the mobile search snippet (Paragraph 1):** Don't waste the first 51 characters repeating the title verbatim before the `1 year / 7 years` hook; lead immediately with the 1-year vs 7-years hook while keeping `travel near the speed of light`, `time dilation`, and `special relativity` in the opening lines.
  2. **Remove final-chapter climax spoiler (Paragraph 2 ending):** Replace the explicit `twenty years / hundred thousand years` spoiler at the end of paragraph 2 with a non-spoiling stakes clause.
  3. **Sharpen Chapter 4 label (`3:44`):** Change `3:44 The Trip` to `3:44 The Twin Paradox Trip`.
  4. **Add the house making-of disclosure line (`AGENTS.md` §Reference lessons 2.5):** Append the required honest line at the bottom of the description.

### Exact New Text (`11_Upload-Package/Descriptions/light_speed_long_description_v01.txt` lines 1–13 & footer)

```text
Leave Earth at ninety-nine percent of the speed of light for one year by your own watch, and seven years pass at home. What happens if you travel near the speed of light? That gap is time dilation, and special relativity says nobody cheated: a moving clock really runs slow.

Your phone already depends on it. GPS satellite clocks drift by about 38 millionths of a second a day, and left alone the map would wander by around ten kilometres a day. In 1971 atomic clocks flown around the world on airliners came home out of step, and muons from cosmic rays reach the ground only because their clocks run slow. We follow the twin paradox on a trip to a star ten light-years away, see why each extra nine of speed costs more energy than the last, and why a ship accelerating at one Earth gravity could cross the entire Milky Way within a single crew lifetime—at an irreversible cost to everyone left on Earth.

0:00 What Happens If You Travel Near Light Speed?
0:42 Your Clock Is Already Slow
1:50 Why Light Sets the Limit
3:44 The Twin Paradox Trip
5:24 The Price of Every Nine
6:39 A One-Way Ticket to the Future
```

And at the end of the file (after the image credits):

```text
Pictures: AI-generated scenes and custom code graphics alongside NASA, ESA and US Air Force imagery. Facts: every number is checked against the sources listed above.
```

---

## Queued Jobs & Ledger
- **`J0250` (`thumb`, `for: codex`):** Build `024_panel_b_7_years_gone.jpg` (`7 YEARS GONE` over horizontally mirrored `024_ship_plate_j0143_v02.jpg`), verify `thumb_preview.py long --score` PASS, and wire `[024_answer_j0143_v02.jpg, 024_panel_b_7_years_gone.jpg]` into `PACKAGE_MANIFEST.json`.
- **`T004` (`05_Analytics/tests/THUMB_LEDGER.json`):** Queued Test & Compare row for 024 (`a`: `house` `024_answer_j0143_v02.jpg` vs `b`: `codex` `024_panel_b_7_years_gone.jpg`, armed by `J0206` once 024 is uploaded).
