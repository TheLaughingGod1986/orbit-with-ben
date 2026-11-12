# J2034 review: HOS 009 tranche-2 picture evidence (review lane, not a picture PASS)

Reviewer: claudecode (worker, review lane), 11 Nov 2026 ~09:30Z. HOS main 1fb86005, evidence from HOS PR #501 (merged, J2033).
**Verdict: FIX on 3 of 20 rows, 17 of 20 ready for the Chief's picture ruling. No picture PASS is given here: only the Chief may give it.**
The full picture milestone stays open. Counts below are actual, nothing inferred.

## What was checked, and how

- Tool checks on every one of the 20 files (my own run, `technical_probe.json` beside this file): local SHA-256 and NAS SHA-256
  against the J2033 evidence, ffprobe, full decode, freeze detection, per-second luma-difference motion.
- Stills only for meaning and look: 4 frames per clip (frames 2, 63, 125, 187) read against the v05 board prompt and the
  board's forbidden list. **This is not watching motion.** No audio (clips are silent). The finished watch stays with Ben.
- Not re-reviewed: the 57 tranche-1 rows (J1237 PASS kept as is), the 12 code graphics (J0342), the long VO.

## Counts (v05 part files, re-counted)

| Group | Rows | State |
|---|---|---|
| Tranche 1 Flow | 57 | Chief PASS 30 Oct (J1192/J1237), unchanged |
| Tranche 2 Flow | 20 | generated 20, technically clean 20, KEEP 0 until the Chief rules |
| Code graphics | 12 | built (J0342), final composites not yet made |
| Reuse (P05:11) | 1 | trim conflict, see below |
| **Total** | **90** | |

## Technical result: 20 of 20 clean

All 20: local hash = NAS hash = evidence hash; full decode with no error; 1280x720, 24 fps, no audio stream;
7.917 s (190 frames), except P04:08_halley_visit_c1 take 2 at 8.000 s (192 frames); no frozen stretch of 0.5 s or more.
Sources are 720p like tranche 1, so the 1080p master needs the same upscale and grain pass at assembly (J2035); neither exists yet.
Two rows move very little (mean luma difference under 0.5): P02:10_how_high (0.27-0.63 per second) and
P01:07_night_field_c1 (0.24-0.41). They are not frozen, but a watcher should confirm they do not read as stills.

## Row findings from stills

FIX (3):

1. **P02:10_how_high t1** (sha 540cb366…). The Moon grows a bright ring like Saturn and by about 5 s has come down into the
   orchard beside the house. The line asks how high the pull reaches up to the Moon; the Moon landing in the field says the
   opposite. Frames at 0.1 s and 2.6 s are right. Fix: either the Chief locks a trim that ends before the ring forms (needs
   the exact frame from a motion check, somewhere between 2.6 s and 5.2 s, and must still cover the row's use), or one retake
   (2 takes left on this row, 100 credits each, inside the J2026 cap).
2. **P02:11_explorer_apple_c1 t1**. The apple is plain red; the board and every other apple plate say green with a red flush
   (P02:08, P04:05, P05:06 are green). The Explorer has no visible glasses in the first two frames and round glasses in the
   last two, and motion jumps between seconds 3 and 4 (3.0 then 11.3), so check for a reframe. Fix: one retake with the
   apple colour stated first, and check the Explorer against the explorer lock.
3. **P03:01_really_falling_c1 t1**. The Moon's face carries a three-armed spiral mark in the first half, then the Moon is
   gone and a small dark ball rides the curve instead. The line is about the Moon falling and never landing. Fix: one retake,
   or the Chief accepts a window only if the parent's join frame already shows the same Moon.

Notes for the Chief's ruling (not blocking in my reading):

- P02:01_cambridge_closes_c1: tricorn-style hats in 1665 are a few decades early. No gate notice, no sick people: forbidden list clear.
- P02:03_christmas_birth_c1: timber farmhouse, while the orchard plates show stone. It continues its tranche-1 parent, so it matches that.
- P04:05_minute_second_c2: the split frame's divider fades in the second half and the orbit line crosses into the room. Ruler has ticks, no numbers.
- P04:08_halley_visit_c1 (take 2) and c2: the two men look alike (both long dark hair). Take 1 was a policy refusal at 0 credits.
- P05:04_comet_1758_c1: frost on the grass, no snow. The board forbids snow in the 1758 scene; frost is the Chief's call.
- P05:05_iss_orbit_c1/c2: the station is close to the real one in shape. No flags, logos or letters seen in stills.
- P05:06_iss_apple_c1: apple shifts between green and red-flushed across the clip. Gold visors, no faces, no readable patches seen.
- Clear in stills: P03:07_ball_to_moon, P01:05_heavens_map_c1, P01:07_night_field_c1, P02:05_working_alone_c1,
  P02:08_the_apple_c1 (apple lands in grass, nobody under it), P03:05_shot_orbit_c1/c2, P04:05_minute_second_c1, P05:05, P05:06.
- Continuation joins (parent last frame to child first frame) were not measured in this run. That check is still owed.

## P05:11 callback trim (must be settled before the edit)

v05 says 1.20-7.90 s of P01:03_table_three. The J1237 lock says 0.000-7.000 s only. The lock wins: 7.00-7.90 s is not approved source.
The row needs 6.70 s. Recommended ruling: **use 0.30-7.00 s (6.70 s)**, fully inside the lock, no new media, no spend.
The alternative 1.20-7.00 s is 5.80 s and leaves the row 0.90 s short. This changes a board trim, so it is the Chief's to record.

## Code graphics

The 12 graphics were built on our own moving paper because the Flow plates did not exist (J0342). Rows marked as moving-plate
overlays (P04:04_dots_square is named in J2377) still need their final composite over the generated plate, then picture_qa and
polish_gate on the composite. None of that exists yet; it belongs in J2035 and must be checked before the picture milestone.

## Parked for Chief

1. Rule on the 17 rows without a FIX (KEEP each, with hash), using this evidence.
2. Rows 1-3 above: trim or retake (up to 3 retakes, 300 credits, inside the J2026 cap of 6,000 with 2,000 used).
3. Record the P05:11 trim as 0.30-7.00 s (or say otherwise).
4. Order the continuation-join check and the code-graphic composites.
J2035 stays behind J2034 until then. No spend, no upload, no schedule or VO change in this review.
