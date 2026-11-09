2026-11-04 — Gemini (`gemini-argon`, covering `cursor` panel slot for J1922)

# Packaging Critique — OWB 026 (`How Far Is the Nearest Star?` / J1823 v03 Proxima-only thumbnail correction)

## 1. Title: `How Far Is the Nearest Star?` — **7/10**
- **What works:** Exact high-intent search phrasing, 29 characters (never truncates on mobile), puts the familiar noun (`Star`) in the first six words, and avoids hedges or threat clickbait.
- **What drags CTR down:** On Home/Suggested browse surfaces, a pure lookup question ("How far is X?") has a soft curiosity gap on its own because a viewer assumes the answer is a single dry textbook number they could Google in two seconds (`4.24 light-years`), rather than a physical paradox (`THUMBNAIL_AND_TITLE_RULES.md` §1.1). Because the title is locked for this scheduled upload, the thumbnail has to supply the entire contradiction/scale hook.
- **One concrete rewrite (if unlocked):** `Why You Can't See the Nearest Star to Earth` (43 chars — keeps `Nearest Star` and `Earth` in the first words for search while shifting from a lookup question to the proven "body impossibility / something hidden" shape).

## 2. Thumbnail at phone size (`168×94` comparison sheet: A `YOU CAN'T SEE IT`, B v03 `PROXIMA HIDES`, C v03 `HIDDEN STAR`) — **6/10** (A: 7/10 · B v03: 6/10 · C v03: 5.5/10)
- **What v03 fixes:** Both B v03 and C v03 replace the misidentified Alpha Centauri A/B pair (`GSFC_20171208_Archive_e000214`) with verified Hubble imagery of Proxima Centauri (`potw1343a`), pass `thumb_preview.py --score` (B v03: `saturation=186.4, near_black=3%`; C v03: `saturation=116.3, near_black=2%`), keep text to 2 words in a top band (`y=34..114`), and leave the bottom-right duration badge completely clear.
- **What fails at 168×94:**
  1. **Picture fights the words:** All three covers show a blazing, frame-filling star with giant diffraction spikes while the text claims `YOU CAN'T SEE IT` / `PROXIMA HIDES` / `HIDDEN STAR`. Adding the small circular Earth cut-out (`190×190 px` at `[55, 490, 245, 680]`) next to the giant diffraction cross in B v03 and C v03 makes Proxima read at a glance like a colossal supernova dwarfing Earth — the opposite of a faint red dwarf invisible to the naked eye.
  2. **Earth reads as an unblended sticker over a spike:** At `168×94`, the hard-edged Blue Marble circle sits directly on top of the lower-left orange diffraction spike with no dark rim or lighting integration.
  3. **Top-left spike cuts through the text band:** Because `potw1343a` (`604×592`) is cropped to `604×340` (`2.12×` upscale), the upper-left diffraction spike runs straight behind `OXI` in `PROXIMA HIDES` and `DDEN` in `HIDDEN STAR`, reducing letter contrast at phone size compared with A's dark upper-left corner.
  4. **Weak wording on B v03 and C v03:** `PROXIMA` (B v03) is astronomy jargon to a viewer who doesn't yet know which star is nearest, and `HIDDEN STAR` (C v03) repeats `STAR` from the title on a cooler blue background (`sat=116.3`) that clashes with the orange spikes.
- **One concrete rewrite:** Keep B v03's warm red-dwarf grade on `potw1343a`, darken the upper-left diffraction spike behind the top text band (`y=0..130`), add a subtle dark outer glow around Earth so it separates from the lower-left spike, and replace the B/C top-band text with **`4 YEARS OF LIGHT`** (B v03) and **`900M YEAR WALK`** (C v03).

## 3. Title + thumbnail together — **6/10** (with A: 8/10 · with B v03: 6/10 · with C v03: 5/10)
- **What works:** Title + A (`How Far Is the Nearest Star?` + `YOU CAN'T SEE IT`) creates a sharp contradiction without repeating a single word.
- **What fails in v03:**
  - **C v03 (`HIDDEN STAR`) directly repeats `STAR` from a 6-word title**, violating `THUMBNAIL_AND_TITLE_RULES.md` §2.3 (*"The thumb adds to the title. It never repeats it"*).
  - **All three variants now test the exact same angle ("it's invisible/hidden") on the exact same `potw1343a` plate.** In v01, A tested invisibility (`YOU CAN'T SEE IT`), B tested light-travel distance (`LIGHT TAKES 4 YEARS`), and C tested human walk scale (`900M YEARS ON FOOT`). Turning B v03 and C v03 into `PROXIMA HIDES` and `HIDDEN STAR` destroys the test matrix: neither B v03 nor C v03 connects to the **"How Far"** question in the title, and both are strictly weaker phrasing of A's `YOU CAN'T SEE IT`.
- **One concrete rewrite:** Keep A (`YOU CAN'T SEE IT`) as the invisibility angle, and make B v03 and C v03 answer *How Far Is the Nearest Star?* on the corrected `potw1343a` Proxima plate without repeating `STAR`: **B v03: `4.2 LIGHT YEARS`** (yellow: `4.2`) and **C v03: `900M YEAR WALK`** (yellow: `900M`).

## 4. First 30 seconds / Short hook (`nearest_star_long_v06_en-GB.srt`) — **7.5/10**
- **What works (`0:00–0:20`):** Asks the title question by `0:07.8` (*"So how far away is the nearest one?"*), lands the concrete distance answer by `0:13.5` (*"Light, the fastest thing there is, takes more than four years to cross the gap"*), and pays off Thumbnail A's hook by `0:19.7` (*"You cannot see that star at all. Not without a telescope"*).
- **What drags (`0:20.8–0:33.1`):** Spends 12.2 seconds on a four-item table-of-contents agenda (*"In this film I will show you which star it is, how anyone measured a distance that large, what that gap looks like..., and how long it would take to get there"*) before naming Proxima Centauri at `0:33.5` (against Standing Lesson 7's no-agenda rule in the first 30 seconds).
- **One concrete rewrite (for Short cuts / future scripts, as v06 long VO is locked):** Cut `0:20.8–0:33.1` (*"In this film I will show you..."*) and go straight from *"Not without a telescope"* into the physical scale: *"Walk there and it takes nine hundred million years — and even our fastest spacecraft out of the Solar System would need seventy-three thousand years to arrive."*

## 5. Description first line and chapters (`nearest_star_long_description_v01.txt`) — **7/10**
- **Chapters (9/10):** Clean, curiosity-preserving labels (`0:00 How Far Is the Nearest Star?`, `0:33 The Star You Cannot See`, `2:02 Measuring the Gap`, `3:52 Shrink It Down`, `5:12 The Walk`, `6:18 Is Anyone There?`) that match the v06 chapter cards and hold back the payoff numbers.
- **First line (6/10):** *"How far is the nearest star? Proxima Centauri, a small red dwarf 4.24 light-years away, is so faint you can never see it without a telescope."* Giving away `4.24 light-years away` in the first 85 characters means the exact numerical answer to the title question appears directly inside YouTube's search snippet before the viewer clicks.
- **One concrete rewrite (Line 1):** `How far is the nearest star beyond the Sun? Proxima Centauri is so faint you can never see it without a telescope — and so distant that even light takes more than four years to cross the gap, while walking there would take nine hundred million years.`

---

**Which would you click, and why?**
Variant A (`YOU CAN'T SEE IT`): it delivers an instant plain-English contradiction to *How Far Is the Nearest Star?* on a clean dark upper-left corner without repeating `STAR` (like C v03's `HIDDEN STAR`), using unfamiliar jargon (`PROXIMA` in B v03), or pasting a hard-edged Earth circle over the lower-left diffraction spike.

**The single change that would most raise CTR:**
Stop using all three Test & Compare slots on synonyms for "invisible" (`YOU CAN'T SEE IT` / `PROXIMA HIDES` / `HIDDEN STAR`): keep the corrected `potw1343a` Proxima plate on B v03 and C v03, but change their top bands to **`4 YEARS OF LIGHT`** (B v03) and **`900M YEAR WALK`** (C v03) so the test compares invisibility against light-time and walk-time scale without repeating `STAR`.
