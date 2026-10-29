# Packaging Panel Decision — J1106 weekly OWB thumbnail audit (three draft Bs)

**Date:** 2026-10-28
**Job:** J1117 (Claude). Advisory decision; the Chief's PASS stands on this file.
**Critiques weighed:** `codex.md` (J1114), `gemini.md` (J1115), `cursor.md` (J1116). All three are present and were written independently.
**Brief:** `05_Analytics/weekly_thumb_audit/OWB/2026-10-28_DESIGN_REVIEW.md` (branch `codex/j1106-weekly-thumbnails`).

Rule used: where two or more critics agree, act on it. These three longs had only 9, 16 and 49 impressions in 28 days, so the test is style-led, not proof of which cover loses clicks.

---

## 1. None of the three v01 Bs is armed. All three get rebuilt as v02.

All three critics agree, independently:
- **Remove the pasted Apollo 17 Earth from all three Bs.** On 005 it implies Earth survives to the end of stellar time, or that a red dwarf is about 3× Earth's size. On 019 it floats in intergalactic space as a fake scale. On the compilation it is a 10 px speck at 168×94.
- Gemini and Cursor agree on two more fixes:
  - **005:** fix the circular mask rind on the red star's left limb (blue starfield and flare trapped at 9–11 o'clock).
  - **019:** fix the rectangular border on the PIA15416 plate (hard edge plus the notch near the blue star at 7 o'clock). Make the galaxy full-bleed and feathered.
- No foreground reference object on any v02. If a builder wants one, the only one allowed is a dark night-side Earth horizon along the bottom edge, at least 18% of frame height, never a sunlit globe. Default is none.

### REXYxuLOBoI — OWB 005 The Last Star
- **Keep** the live title: *The Last Star: What Happens When a Red Dwarf Dies?* (Codex 8, Cursor 8, Gemini 7.5).
- **Thumbnail B v02 text: `10 TRILLION YEARS`**, with `TRILLION` in house yellow and the rest white (Gemini and Cursor).
  - Why it beats `RED DWARFS WIN`: it adds the timescale without repeating "red dwarf" from the title (THUMBNAIL_AND_TITLE_RULES §2.3). "WIN" framed heat death as a game, which goes against "wonder, not threat".
  - Codex's `RED DWARF END` repeats the title's noun, so it isn't used.
  - The ten-trillion-year line is the film's own (FRIDAY_LAST_STAR_SHORT TEACH beat).
- **Picture:** keep the existing illustrated last-star plate as the single subject, with the mask rind fixed. Pull back the white-hot flaring so it reads as a dim, long-lived red dwarf, not an eruption (all three critics).
- **Title B:** dropped (Codex 8, Cursor 7, Gemini 6). No title test on 005.

### ojk-dfOpAmw — OWB 019 Milky Way–Andromeda Collision
- **Keep** the live title: *What Happens During the Milky Way Andromeda Collision?* (Gemini 8.5, Cursor 8, Codex 7).
- **Thumbnail B v02 text: `STARS DON'T CRASH`**, with `CRASH` in house yellow.
  - All three agree the cover should carry the contradiction with "Collision" in the title. Two (Gemini and Cursor) word it as "crash", and all three call `STARS MISS STARS` clunky.
  - `STARS DON'T CRASH` keeps the film's own wording ("stars almost never hit", VO part 04, and the channel's Short "Why Stars Don't Crash When Galaxies Meet"). The VO explains the "almost".
  - Cursor's `NO STARS CRASH` is the absolute claim the brief warned against. Codex's `MOST STARS MISS` is accurate but loses the contradiction. Both are kept as reserves if `STARS DON'T CRASH` fails the 168 px check.
- **Picture:** keep the single diagonal Andromeda galaxy, full-bleed and feathered across 1280×720, with fewer bright foreground pinpoints. No Earth.
- **Title B:** rejected by all three. It duplicates two live channel titles (`7YFfY4MdB6c`, `xQlV9G9lqLI`) and drops "Andromeda" and "Milky Way". No title test on 019.

### m09jUdwC5hk — deep-time compilation
- **Thumbnail B v02 text: `FIVE COSMIC CLOCKS`**, with `CLOCKS` in house yellow (Codex and Gemini).
  - All three agree `SATURN TO STARLIGHT` reads as a Saturn-only film.
  - `10 TRILLION YEARS` (Gemini and Cursor) is now 005's B, and the compilation's live A is already a near-clone of 005's cover. Using it here would recreate the duplicate the audit is fixing.
- **Picture:** Saturn stays the one hero. Grade it `--pale` (saturation about 95–110) so the bands don't blow out to lemon yellow (Cursor, rule §2.B.3). No Earth speck.
  - Codex's optional small last-star inset, top-left under the text and clear of the badge, may be tried only if it stays a clearly separate vignette at 168 px; otherwise leave it out.
- **Title:** keep the live title for now. Title B, *How Long Do Moons, Rings and Stars Last?*, scored 8 / 7.5 / 8 against the live title's 8 / 6 / 7. It becomes a **separate title-only test after this thumbnail test ends**, with the thumbnail fixed: one variable at a time.

---

## 2. Descriptions

### 005: change line 1
Gemini and Cursor: line 1 gives away both answers, red dwarf and black dwarf, before the click.
- **New line 1** (Codex's wording): `What happens when the last red dwarf dies? Follow the longest-lived stars to the end of their light.`
- **Remove internal studio wording** from paragraph 3: "dreadbait" and "fearbait" (Gemini). These are house jargon, not viewer copy.
- Chapters: keep.

### 019: change
- Line 1 stays the film's claim. The 4-billion-year forecast is unchanged here; any wording change to it goes through the facts reviewer first (Codex).
- Chapter `0:47 The Second Spiral` → `0:47 Meet Andromeda` (Codex; Gemini and Cursor raised no objection).
- "Thursday films" → "weekly films" (Cursor; the schedule is no longer Thursday-only).

### Compilation: keep
Gemini 9, Cursor 9, Codex 8.

---

## 3. Jobs queued
1. **Thumb build (Codex):** three v02 Bs as above. House grade gate, a 168×94 phone sheet next to the live As, and builder `00_Brand/Channel-Setup/tools/build_weekly_thumbs_j1106.py` updated. No spend: existing plates only. Parks for the Chief with the phone sheet.
2. **Studio (Mini), after the build passes:** arm thumbnail-only Test & Compare A vs B v02 on all three. Recheck first that no test is running on each video, and never replace a running one. Add and start each row in `05_Analytics/tests/THUMB_LEDGER.json` (`thumb_ledger.py add` then `start`) only once Studio shows the test armed. Make the description edits in section 2 and read them back.
3. **After the compilation's thumbnail test ends:** title-only test on m09jUdwC5hk, live title vs *How Long Do Moons, Rings and Stars Last?*. Queued by the Studio job when it reads the result.

## 4. What this teaches (for PATTERNS.md)
- A pasted daylight Earth on a deep-space plate fails three ways (false survival, false scale, invisible at phone size). Don't add it by default.
- Each cover adds the scale or twist; it never repeats the title's noun.
- Two films' covers must never share a hook. The compilation's live A duplicated 005, and this round almost did it again with `10 TRILLION YEARS`.
