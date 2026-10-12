# 027 Earth Spin v01h: NUMBER overlays on chapter 5, "Keeping Score" (J0154)

Cursor (stand-in for Codex on a `chart` job), 12 Oct 2026. Advisory: Chief scores the gate.

- **Why this chapter.** A per-chapter scan of v01g against *Reference lessons* item 6 and Chief's J0145 rulings (a to-scale graphic with no numeral is not a NUMBER): "The Sudden Stop" has BRITAIN 1,000 KM/H (1:00), "The Speed You Cannot Feel" has 43 KM WIDER (2:12), "A Slow Stop" has 1 DAY = 1 YEAR (3:24) and "Earth Is Already Slowing" has 4 CM A YEAR (4:30) and 22 HOURS (5:52). "Keeping Score" (5:57–7:26) had only the two text-free clocks (rows 30 and 33), so it FAILed NUMBER. It's the only chapter changed.
- **Cut:** `/private/tmp/027_EarthSpin_rough_v01h.mp4` (sha256 in `SHA256.txt`). It's v01g's picture with the labels added; the audio stream is copied from the v01g master (`audio_v01h.json`). No cut, VO, bed or graphic change, no spend.
- **Builder:** `../_overlay_earth_spin_v01h.py` (`--plan` lists every label with its time, place and source check). Renders are `code_graphic_027_row<row>_<k>.png`, one per label (the timeline is a strip plus the date that drops onto it), listed per cut in `cuts_v01h.json` (`overlays`) and in `overlays_v01h.json`.
- **Style:** the 026 v05c house pill (navy 23,36,55 at 86%, white Arial Bold 72–84 px). Each label comes in on the VO word's start with a 0.35 s fade and rise and goes out with a 0.3 s fade, is never up more than 4 s, and ends before its own shot's cut. Every label is 4 words or fewer, the VO's own words, with spoken numbers as numerals. On the timeline the new date is yellow and drops 40 px onto the strip; dates already said stay white.
- **Gates:** see `picture_qa_v01h.txt`, `polish_gate_v01h.txt`, `audio_v01h.json`. Before/after stills: `overlay_stills_v01h.jpg`.

| Film time | Row | Label | Source check (`01_Script/SOURCES.md`) |
|---|---|---|---|
| 6:02.0 | 32 | Late 1960s (WHEN) | row 16: caesium SI second, 13th CGPM 1967 |
| 6:12.5 | 33 | 1972 (WHEN, first timeline date) | row 17: leap seconds since 1972 |
| 6:16.7 | 33 | 27 times | row 17: exactly 27 leap seconds, 1972–2016 |
| 6:22.5 | 33 | timeline: 1972 · 2016 | row 17: last leap second 31 Dec 2016 |
| 6:36.9 | 34 | More than a millisecond | row 18: shortest days 1.47–1.66 ms short (2020–2024) |
| 6:42.3 | 35 | timeline: 1972 · 2016 · 2035 | row 19: CGPM 2022 Resolution 4, by 2035 |
| 7:14.5 | 37 | 4.5 billion years ago | row 21: 4.54 ± 0.05 Gyr (VO "about four and a half billion years ago") |

## For Chief

1. **"1972" and "27 times" sit beside the row 33 clock**, which is itself a code graphic. They add the numeral the clock lacks in the same window; they don't make two graphics back to back. The dial fills the frame height at 6:12, so "1972" shows as a pill on the right, and the strip only appears from 2016 on, over real footage.
2. **"24 hours"** (7:18, "Your days will stay twenty-four hours") isn't labelled: no `SOURCES.md` row carries it. Add a row if you want the label.
3. **Short holds:** "More than a millisecond" is up 1.96 s and the 2035 step 2.04 s, because each one's shot ends soon after the word (cuts at 6:38.97 and 6:44.37; 6:44.37 opens the row 35 tides graphic, so the label doesn't run into it).
4. **Existing, not changed here:** the 6:25 crossfade into the Pāhoehoe plate shows a faint NASA Earth Observatory watermark for about half a second (row 34, `commons_Pahoeoe_fountain_original.jpg`). Worth a look at the next picture version.
5. 027 is VO-locked and has no bed (held to 30 Oct), so `music_gate` isn't run.
