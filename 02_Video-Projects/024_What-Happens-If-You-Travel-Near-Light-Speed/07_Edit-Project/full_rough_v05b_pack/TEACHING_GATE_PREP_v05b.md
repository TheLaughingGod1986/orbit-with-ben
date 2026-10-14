# 024 Light Speed v05b — per-chapter teaching gate, prep sheet (J0145)

Prepared by Cursor (stand-in, 12 Oct 2026) for the Orbit Auditor and Chief. **Advisory only: every result below is a proposal. Chief scores the gate.** Rule: AGENTS.md *Reference lessons* item 6.

- Cut: `/private/tmp/024_LightSpeed_full_rough_v05b.mp4` (pack 5511d7ea). Film time = VO time: the chapter cards are overlays and shift nothing (`overlays_v05b.json`, `cuts_v05b.json`).
- Stills behind this sheet: `teaching_gate_stills_v05b.jpg` (17 frames, each stamped with its film time).
- **Average % viewed: UNKNOWN** (nobody has read Studio; the film isn't uploaded).

## What's on screen

Every code graphic in 024 is **text-free by design** (`code_graphics.py` docstring: "Text-free by design"; "No numbers on the plate"). The stills confirm it: no numeral, unit or keyword appears on any graphic. The only words on screen are the five chapter cards (`card_0`–`card_4`, 2.5 s each) and the subscribe cue.

Several graphics are still **drawn to scale**: the GPS bars (−7.2 / +45.9 / +38.7 µs a day), five dials turning at 1/γ, the 15 km muon column with the 660 m line, the 10 ly bar shrinking to 1/7.09, the energy curve against the dashed c line. So the question for Chief is:

> **Does a to-scale graphic with no numeral on it count as "a number shown as an object"?** If yes, chapters 1–4 pass NUMBER as they stand and the open and chapter 5 are borderline. If no, every chapter FAILs NUMBER and needs a numeral overlay (fixes below).

**WORDS:** with no labels at all there is nothing that paraphrases or contradicts the VO, so WORDS is vacuous. The chapter cards are titles, not VO keywords ("Your Clock Is Already Slow" vs the VO's "their clocks run slow"). Proposed: WORDS = PASS (no labels), with a note that the gate's purpose (Jupiter `-jmMROGoZCM` went live with no teaching labels) is not met until the NUMBER overlays below go in, and each of those must quote the VO word for word.

## Chapter by chapter

| Chapter | Film time | Number object(s) on screen | NUMBER (proposed) | WORDS (proposed) |
|---|---|---|---|---|
| Open | 0:00.0–0:42.0 | energy curve `energy_a` 0:35.7–0:41.5 (no numeral; the VO there names no number). VO numbers "99%", "one year", "seven years" (0:00–0:13) have no object. | FAIL if a numeral is required; borderline otherwise (the curve doesn't sit under a spoken number) | PASS (no labels) |
| 1 Your Clock Is Already Slow | 0:42.0–1:50.7 | GPS bars to scale `gpsclocks_a/b/c` 0:44.3–0:49.8, 0:53.3–0:59.1, 1:02.1–1:07.1; map drift `mapdrift_a` 1:07.1–1:19.8 | PASS if to-scale counts (bars build with "seven-millionths", "forty-six", "thirty-eight-millionths"); else FAIL | PASS (no labels) |
| 2 Why Light Sets the Limit | 1:50.7–3:44.4 | five dials `gammaclocks_a` 2:36.7–2:56.0, lit one per spoken speed; muon column `muons_a–d` 2:56.0–3:29.3 (660 m line to scale) | PASS if to-scale counts; else FAIL | PASS (no labels) |
| 3 The Trip | 3:44.4–5:24.5 | twin clocks `twinclocks_a/b` 3:55.8–4:00.7, 4:08.7–4:13.7; shrinking distance bar `contraction_a/b` 4:29.1–4:46.9 | PASS if to-scale counts; else FAIL | PASS (no labels) |
| 4 The Price of Every Nine | 5:24.5–6:39.2 | energy curve `energy_b/c/d` 5:29.5–5:33.1, 5:42.0–5:56.3, 5:59.2–6:08.5 | PASS if to-scale counts; else FAIL | PASS (no labels) |
| 5 A One-Way Ticket to the Future | 6:39.2–8:11.0 | callbacks only: `twinclocks_e` 7:18.6–7:26.0, `gammaclocks_b` 7:26.0–7:28.6, `gpsclocks_d` 7:28.6–7:34.0, `muons_e` 7:34.0–7:37.4. The chapter's own numbers ("twenty years", "a hundred thousand years") play over the Gaia still and Earth views with no object. | FAIL (borderline even if to-scale counts: the objects don't show this chapter's numbers) | PASS (no labels) |

## Overlay fixes if Chief rules FAIL (VO locked: overlays only, a Codex `chart` render per row)

Each label is the VO's own words at that moment (4 words or fewer), animated in with the word, house type, off the subject. Numbers are the ones spoken; Chief checks each against `01_Script/SOURCES.md` before render.

| Chapter | Where (film time, row) | Label, word for word from the VO |
|---|---|---|
| Open | 0:06.5–0:13.0, row 2 (Earth views) | "one year" → "seven years" |
| 1 | 0:53.3–1:07.1, rows 8 (`gpsclocks_b/c`) | "seven-millionths" on the blue bar, "forty-six" on the gold, "thirty-eight-millionths" on the white |
| 1 | 1:11.7–1:17.5, row 9 (`mapdrift_a`) | "ten kilometers every day" |
| 1 (WHEN) | 1:24.7–1:28.0, row 11 | "1971" |
| 2 | 2:36.7–2:56.0, row 16 (`gammaclocks_a`) | "10%", "90%", "99%", "99.99%" under each dial as it lights; "seven to one", "seventy to one" |
| 2 | 3:12.9–3:15.1, row 17 | "660 meters" |
| 2 (WHEN) | 3:19.1–3:24.4, row 18 | "1963" |
| 3 | 3:55.8–4:00.7, row 22 (`twinclocks_a`) | "twenty years" (home dial) · "three years" (ship dial, at 4:00.7–4:05.9 on the next shot) |
| 3 | 4:34.1–4:40.0, row 25 (`contraction_a`) | "Ten light-years" → "one and a half" (VO says "about one and a half"; the plate is drawn to 1.41) |
| 4 | 5:42.0–5:46.3, row 30 (`energy_c`) | "90" and "99%" marks on the speed axis; "five times as much" |
| 5 | 6:52.5–6:56.1, row 35 (Gaia still) | "twenty years" |
| 5 | 7:00.5–7:05.2, row 36 (Earth views) | "a hundred thousand years" |

## Notes for Chief

- 024 is on *Teach on screen*'s no-rework list ("024 (v05 in review)"), but Chief's J0145 brief names 024 v05b first under item 6, which says a VO-locked film meets it with overlays only. Chief to confirm 024 gets the overlays before Ben's watch, or is scored and left as the record.
- Placing overlays on existing code graphics adds no new graphic, so it doesn't add to the back-to-back runs already in the cut (for example 4:29–5:06 and 7:18.6–7:37.4 run graphic to graphic; these predate the film-wide rule and aren't scored here).
- 026 and 027 follow in this job's scope; 027 has no picture yet (shot list v01 only), so its sheet waits for a rough cut.
