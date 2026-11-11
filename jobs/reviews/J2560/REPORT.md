# J2560: the Shorts check and a full-frame shot with soft walls

11 Nov 2026, Claude (cloud). Follow-up to J2557 (#792). No Short was re-cut and nothing changed in Studio.

## The fault

The whole-Short check (J2546) failed one full-frame Short: History of Science `Wvjd8g0CpzE` (airs Sun 15 Nov), 3 of 26 sampled frames, one over the allowance. The shot at 5.0 to 8.0 s is a full-frame cartoon view inside living tissue: vessels and blood cells across the middle, soft shaded tissue walls above and below. The check read "detail in the middle, soft and varied above and below" as a picture band over a blurred copy. Both saved frames reproduce that on main.

## What was tried, on the frames

| Measure | Result on the 58 frames |
|---|---|
| The fill matches an enlarged, blurred copy of the band | Does not separate. The soft-walled frames score 0.55 to 0.67; real pads score from 0.05 to 1.00, because the fill is often a different frame, another zoom, or sits under a graphic. |
| How much fine detail the fill carries, at three strengths | Does not separate. The soft wall above the vessels is as smooth as a blurred fill. |
| Where fine detail switches on, row by row | Does not separate. A picture band whose own top is sky switches on as gently as the soft wall does. |
| **A straight edge: across one row the brightness steps far more than it changes just outside that row, on most columns** | Separates the clear cases. Soft-walled full frames: 0.54 at most. Padded frames with a visible edge: 0.69 at least. Eight padded frames fall between (feathered edges, a dark band on a dark fill, two end cards): 0.51 to 0.60. |

One frame cannot always tell a feathered blur pad from a soft part of a real picture. So the check now says which kind of evidence it has.

## The change

- Every padded-looking frame is marked `edge: true` (a straight edge where picture meets fill: the old seam finder, a mirror line, or the new one-sided measure at 0.65 or more) or `edge: false` (it only looks padded).
- **The opening:** a hard FAIL only when the padded frames at 0.0 to 0.5 s have an edge. Without one it is a warning that says to look at frame 0. This also stops a wrong FAIL on a full-frame smooth nebula with hook text across the middle (seen on `k2kEaA7ICjc` in J2557).
- **The whole Short:** a hard FAIL when more than 10% of the sampled frames are padded with an edge, or more than 15% look padded, edge or no edge. Under that it is a warning naming the seconds; when none of them has an edge the warning says so and asks the reviewer to look.
- Result rows written before this change carry no `edge` and are read as edged, so nothing old gets easier.

## On the labelled frames

| | Before | Now |
|---|---|---|
| Padded frames caught (of 28) | 24 | 24: 16 with an edge, 8 without |
| Full frames of the audit read as padded (of 28) | 0 | 0 |
| The two soft-walled frames | read as padded, Short failed | read as "looks padded, no edge": a warning, Short not failed |

The four padded frames still missed are the same four, named in the test file with why.

## What it now misses, plainly

- Nothing the audit found. In the Mini's run (J2557) every one of the nine padded Shorts has 19% or more of its sampled frames flagged, so each still fails on the 15% limit whatever its edges show.
- What is given up: a Short whose padding shows no straight edge and covers between 10% and 15% of it is now a warning, not a FAIL. The warning names the seconds, and the reviewer looks.
- Two real Shorts sit one frame above the 15% line: `kKN8Ale42sE` (4 of 21, and two of those four are a full-frame Sun shot wrongly read) and `xdurJQcoiGM` (4 of 19). Both are on the re-cut list already.
- The 15% figure is a judgement on few Shorts. It needs the Mini's run on the real files (below) before anyone leans on it.

## For the Mini

Run `gate_shorts_open.py check <file> --air-date <date> --id <id> --report-only --json` again on `Wvjd8g0CpzE`, `f17XCtUmN-g`, `cLKDiYP55J8`, `xgx2lYHhYZM`, `kKN8Ale42sE`, `xdurJQcoiGM`, `rvug71d7Dqk`, `C8lPx5N2DwM` and `k2kEaA7ICjc`, and paste for each: frames padded with an edge, frames without, and the verdict. Expected: the first four pass, with warnings at most; the last five still fail.

## Files

- `00_Brand/Channel-Setup/tools/gate_shorts_open.py` (shared core file; lock updated; the pair goes to history-of-science)
- `00_Brand/Channel-Setup/tools/test_gate_full_bleed.py`: 53 tests (37 before)
- `jobs/reviews/J2560/J2560_labelled_frames.json`: the two frames, grey 108 x 192, in the audit set's format
- `AGENTS.md`: the rule line says what fails and what warns
