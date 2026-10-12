# 026 Nearest Star rough v05b — per-chapter teaching gate, prep sheet (J0145)

Prepared by Cursor (stand-in, 12 Oct 2026) for the Orbit Auditor and Chief. **Advisory only: every result below is a proposal. Chief scores the gate.** Rule: AGENTS.md *Reference lessons* item 6.

- Cut: rough v05b (this pack). The v05b MP4 isn't on the Mini's `/private/tmp` any more, so timings come from `cuts_v05b.json`, `overlays_v05b.json` and `nearest_star_words_list.json` (film time = VO time), and the label frames were pulled from the graphic renders the assembler lays in (`code_out_v05/lightyear.mp4`, `code_out_v05/lightrace.mp4`).
- Stills behind this sheet: `teaching_gate_stills_v05b.jpg` (5 frames, each stamped with its row and film time; on the Mini only, media stays out of git). The older `code_out_v05_stills/` jpgs (9 Oct 23:43) predate the labels and show none; the MP4s in the cut do carry them.
- **Average % viewed: UNKNOWN** (nobody has read Studio; the film isn't uploaded).

## What's on screen

Two graphics carry labels, both in house type with the number in yellow; every other code graphic (`triple`, `triple_b`, `parallax`, `journey`, `scale`) is text-free. The assembler's name-card list is empty in v05b (`LABELS=[]`), so there is no WHO card for Bessel. Other words on screen: five chapter cards (2.5 s each) and the subscribe cue.

**WORDS check, label by label** (label in time vs the VO word):

| Row | Label | On at | VO at that moment | Match |
|---|---|---|---|---|
| 9 `lightyear` | "Proxima" | 1:52.2 (whole row) | "towards Proxima" 1:57.0 | PASS (the name, said in the row) |
| 9 `lightyear` | "1 year" | 1:54.6 (first tick lights) | "in a year" 1:54.6 | **Chief to rule:** numeral for "a year". Proposed PASS; if strict, relabel "a year" |
| 9 `lightyear` | "More than 4 years" | 1:59.8 | "more than four years ago" 1:59.8 | PASS |
| 27 `lightrace` | "Just over a second" | 6:06.4 | "just over a second" 6:06.4 | PASS |
| 27 `lightrace` | "About 8 minutes" | 6:09.6 | "about eight minutes" ("eight" 6:09.6) | PASS |
| 27 `lightrace` | "More than 4 years" | 6:13.1 | "more than four years" 6:13.1 | PASS |

All six labels are 4 words or fewer.

## Chapter by chapter

| Chapter | Film time | Number object(s) on screen | NUMBER (proposed) | WORDS (proposed) |
|---|---|---|---|---|
| Open | 0:00.0–0:33.5 | none with a number. `triple` 0:20.1, `parallax` 0:24.6 and `journey` 0:28.7 are the agenda montage, text-free. VO "more than four years" (0:08–0:13.5, row 2) has no object. | FAIL | PASS (no labels) |
| 1 The Star You Cannot See | 0:33.5–2:02.1 | **`lightyear` 1:52.2–2:01.7**: four year ticks light as the pulse crosses, "1 year" at 1:54.6, "More than 4 years" at 1:59.8. (`triple_b` 1:28.3 is not to scale, no number.) | PASS | PASS ("1 year" for "a year": Chief to rule) |
| 2 Measuring the Gap | 2:02.1–3:53.0 | none with a number. `parallax` 2:23.9 and 3:01.7 is exaggerated on purpose (docstring), text-free. Spoken: "eighteen thirty-eight", "about thirteen kilometers", "more than a billion stars", "about five kilometers". | FAIL | PASS (no labels) |
| 3 Shrink It Down | 3:53.0–5:12.3 | `scale` 3:59.5–4:06.5: Sun and Earth sizes to scale, gap drawn short, no numeral. Spoken: "fifteen meters", "four centimeters", "four thousand kilometers", "nineteen seventy-seven", "two and a half kilometers". | FAIL (borderline only if a text-free size comparison counts; the distances it's about are not drawn to scale) | PASS (no labels) |
| 4 The Walk | 5:12.3–6:19.0 | **`lightrace` 6:01.8–6:18.5**: Moon, Sun, Proxima pulses with "Just over a second" 6:06.4, "About 8 minutes" 6:09.6, "More than 4 years" 6:13.1. (`journey` 5:23.6–5:29.1 has lanes at true relative speed, text-free.) | PASS | PASS |
| 5 Is Anyone There? | 6:19.0–8:14.5 | none. No code graphic in the chapter. Spoken: "2016", "every 11 days", "about 20 years", "early 2031", "2035". | FAIL | PASS (no labels) |

Proposed tally: NUMBER PASS in 2 of 6 chapters (1 and 4), FAIL in 4 (open, 2, 3, 5). WORDS PASS in all 6, with the one "1 year" ruling for Chief.

## Overlay fixes if Chief rules FAIL (VO locked: overlays only, a Codex `chart` render per row)

Each label is the VO's own words at that moment (4 words or fewer; numerals for spoken numbers, as in the existing labels), animated in with the word, house type, off the subject, over moving or blurred real picture. Chief checks each number against `01_Script/SOURCES.md` before render. Mind the film-wide rule of no two code graphics back to back: these sit on real plates, not new graphic shots.

| Chapter | Where (film time, row) | Label, from the VO |
|---|---|---|
| Open | 0:08.0–0:13.5, row 2 (Paranal) | "More than 4 years" |
| 2 (WHEN) | 3:01.7–3:06.6, row 14 (over `parallax`, on "eighteen thirty-eight") | "1838" |
| 2 | 3:10.9–3:15.4, row 14 (Bessel portrait) | "About 13 kilometers" (VO: "about thirteen kilometers away") |
| 2 | 3:29.5–3:34.9, row 15 (eso0844a) | "More than a billion" |
| 2 | 3:39.4–3:44.4, row 15 (Moon e001982) | "About 5 kilometers" |
| 3 | 4:06.5–4:10.0, row 18 (heic1007a) | "About 15 meters" |
| 3 | 4:28.3–4:32.1, row 20 (e001788) | "About 4,000 kilometers" |
| 3 (WHEN) | 4:55.9–5:00.8, row 22 (PIA17049) | "1977" |
| 3 | 5:06.5–5:11.8, row 22 (PIA21746) | "About 2.5 kilometers" |
| 5 | 6:27.4–6:36.4, row 28 (eso1629a / video) | "Every 11 days" |
| 5 | 7:12.2–7:16.6, row 31 | "About 20 years" |
| 5 (DATA + WHEN) | 6:22–7:37, rows 28 and 32 | one timeline that builds as each date is said: "2016" (6:22), "2031" (7:27), "2035" (7:34); 3 dates, so it counts as one DATA moment (*Teach on screen*) |

## Notes for Chief

- 026 is VO-locked and not on any no-rework list, so it gets these overlays at its next version, before OWB UAT.
- *Teach on screen* item, outside this gate: Friedrich Bessel is named at about 3:05 (row 14) with no WHO card (`LABELS=[]`), and the row 14 portrait is on screen. A WHO card (name; years and role from `SOURCES.md`) belongs in the same overlay pass.
- 027 has no rough cut yet (shot list v01 only), so its sheet waits for picture. That is the last part of J0145.
