# J2546 handover (MacBook, 11 Nov 2026): not finished, released

Nothing in `gate_shorts_open.py` is changed yet. This folder holds a probe and what it measured, so the next
worker starts from numbers and not from zero.

## Where the current check stands on the 56 labelled frames

`full_bleed_frame()` on main calls **32 of 56 right, 24 wrong**:

- 13 padded frames missed: `ffYKoNVPoqg` 14.0; `bSjWiCbB7pY` 4.0, 10.0; `HZGTovJu_TQ` 24.0; `kKN8Ale42sE` 6.0;
  `cwU_0WWeNZ4` 20.0, 22.0; `rvug71d7Dqk` 0.0, 2.0, 20.0; `C8lPx5N2DwM` 6.0, 28.0; `k2kEaA7ICjc` 10.0;
  `heiGCnGKTkE` 6.0.
- 11 full frames wrongly failed: `ChbsigHD5_o` 0.0; `cLKDiYP55J8` 0.5; `Wvjd8g0CpzE` 22.0; `xzKoHg0E0_U` 6.0;
  `MScK2CK2ZFg` 16.0; `QEoYKIVvKBA` 6.0; `f17XCtUmN-g` 22.0; `xdurJQcoiGM` 14.0; `bSjWiCbB7pY` 22.0;
  `ffYKoNVPoqg` 8.0 (called bars).

## The brief's idea, measured (`probe_copy_match.py`)

The outer bands are compared with the picture band enlarged about the frame centre (cover scale, and 1.25 times it),
on 6x6 block means, Pearson correlation, the worst fifth of blocks dropped (a caption over the fill). Score = the
lower of the top and bottom correlations, best over band positions.

- Padded frames: 18 of 28 score 0.80 or more. The low ones: `C8lPx5N2DwM` 6.0 (0.12) and `k2kEaA7ICjc` 10.0 (0.36)
  are a graphic over a backdrop that is not a copy (ruling 2), so no copy match can catch them: they need the
  flat or very soft outside plus a straight seam. `ffYKoNVPoqg` 4.0 and 14.0 (dark-blue canvas) are the same case.
  `rvug71d7Dqk` (0.61, 0.74, 0.65), `ffYKoNVPoqg` 0.0 (0.71), `kKN8Ale42sE` 6.0 (0.64), `bSjWiCbB7pY` 14.0 (0.60, one
  side 0.91) and `C8lPx5N2DwM` 10.0 (0.76) match on one side or with the standard 16:9 band at about 0.7 to 0.9.
- Full frames: 24 of 28 score 0.72 or less. Over that: `QEoYKIVvKBA` 0.0 (0.97, a smooth graphic that matches its own
  enlargement), `Wvjd8g0CpzE` 22.0 (0.82), `MScK2CK2ZFg` 16.0 (0.81).
- So the copy match alone does not split the set: there is no single threshold. One-side scores are worse (full
  frames reach 0.96).

## What to try next

1. Copy match AND softness together: fill rows carry row detail 0 to 3 in almost every padded frame, while the
   high-scoring full frames have real detail outside (`QEoYKIVvKBA` 0.0: 2 to 25; `MScK2CK2ZFg` 16.0: 20+ in the
   top caption rows, check the rest). `rvug71d7Dqk` is the exception (5 to 8 in the upper fill).
2. A separate "flat backdrop" kind for ruling 2: outside median row detail under 1, a straight seam (every column
   steps within one row), with the step threshold lower than `FB_SEAM_DIFF` 12 (the canvas steps are 5 to 10 grey
   levels). The Titan globe on black (`ffYKoNVPoqg` 8.0) must not pass as this: its limb is curved, so ask for
   straightness per column.
3. Restrict the copy-match band to the measured seam where there is one, and to the standard 16:9 band (rows 66 to
   126) where the seam is feathered.
4. Then parts 2 to 4 of the brief (one frame a second, the 10% rule with the meta end-card stretch left out, tests
   from the JSON, `core_sync.py lock` and the HOS pull request: the gate file is core-locked).

## Running the probe

It is written as a unittest so it runs where plain scripts are not allowed:

    python3 -m unittest discover -s jobs/reviews/J2546 -p "probe_copy_match.py"
