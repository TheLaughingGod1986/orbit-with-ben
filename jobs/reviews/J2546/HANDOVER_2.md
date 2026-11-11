# J2546 second run (MacBook, 11 Nov 2026): still not finished, parked for the Chief to split

Read `HANDOVER.md` first. `gate_shorts_open.py` is still unchanged: the check on main calls 32 of the 56 labelled
frames right. This run added one probe and its table, and no rule.

## What was added

- `probe_features.py`: for every labelled frame, the row-detail profile and the row pixel-spread profile in 16
  bins from top to bottom, and the straightest brightness step in each half.
- `probe_features_output.txt`: its output for the 56 frames (index, id, time, label, the kind main gives).

## What the table shows

Softness outside plus a straight seam cannot split the set, in either direction:

- Full frames that look padded on those two measures (soft or flat rows outside, a step across 0.94 to 1.00 of
  the columns on both sides): `Wvjd8g0CpzE` 22.0 (row 37), `xvarZP2aYyE` 10.0 (51), `xdurJQcoiGM` 14.0 (53),
  `ChbsigHD5_o` 0.0, 2.0 and 24.0 (28, 29, 31), `ffYKoNVPoqg` 8.0 (55). Of these, row 37 also scores 0.82 on the
  copy match in `HANDOVER.md`, so it is the hardest full frame in the set.
- Padded frames whose fill is not soft: `rvug71d7Dqk` 0.0 and 2.0 (rows 11, 12: row detail 5 to 10 and more in
  the upper bins, the hook caption and a sharper blur), `SWDCZfWZVao` 14.0 (21: 2 to 9 in the top bins),
  `bSjWiCbB7pY` 4.0 (3: 3 to 6 in the lower bins).
- Padded frames with no straight step to find: `kKN8Ale42sE` 6.0 (8: 0.54 and 0.51), `C8lPx5N2DwM` 6.0 (15: 0.35
  and 0.61), `k2kEaA7ICjc` 10.0 (22: 0.58 and 0.60).

So the rule needs a third measure. Not tried yet:

1. Sharpness as high-frequency energy, not left-right difference: a blurred copy has almost nothing at one or
   two pixels' spacing even where it has contrast, and a caption over it is a small share of the columns. Measure
   it per column segment and take the lower half of segments, so a caption does not hide the fill.
2. Copy match on the measured seam rows only, and with both outer bands tested against the same enlargement
   (same scale and same centre for top and bottom): a real room matches on one side by chance, not on both with
   one scale.
3. For the full frames in the first list, look at what the outer rows hold: a full-frame picture that is dark or
   flat at the top and bottom has no enlarged copy of its middle there, so the copy match should be near zero
   once the flat blocks (spread under 2 grey levels) are counted as no match and not skipped.

## Why it is parked

Two runs have now ended at the 25-minute limit on step 1 alone. The job is four pieces of work and step 1 is
open-ended. Suggested split:

- A. The frame rule only: change `full_bleed_frame()`, with a test that reads the labelled JSON and reports the
  count right out of 56. No whole-Short rule, no sync. It may need more than one run: each run should end by
  writing the count and the frames still wrong here.
- B. After A: one frame a second, the 10% rule with the meta end-card stretch left out, the report of padded
  stretches, the tests on made clips.
- C. After B: `core_sync.py lock`, push to history-of-science, the pair of pull requests, park for the Chief.
