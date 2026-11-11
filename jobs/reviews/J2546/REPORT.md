# J2546: the padded-frame check, set on real frames

Worker: Claude (cloud), 11 Nov 2026. Taken over from the MacBook by the acting Chief's ruling of 11 Nov 02:00Z. The
MacBook's two runs are on branch `macbook/J2546` (`HANDOVER.md`, `HANDOVER_2.md`, two probes): softness outside plus a
straight seam could not split the set, and neither could a copy match. This report starts from those findings.

## Result

`full_bleed_frame()` calls **52 of 56** labelled frames right: **28 of 28 full frames pass** and
**24 of 28 padded frames are caught**. The check on main before this called 32 right (13 padded missed, 11 full
wrongly failed). The seven frames the Chief's ruling 4 names as wrongly failed all pass.

Four padded frames are still missed. Each is left wrong because getting it right would fail full frames:

| Frame | Why it is missed |
|---|---|
| `rvug71d7Dqk` 0.0 s and 2.0 s | a light, feathered blur under a large hook caption; about a third of the upper fill still reads as sharp. Its sharp share above is 0.36 and 0.34; full frames start at 0.10. |
| `C8lPx5N2DwM` 6.0 s | a dark-blue graphic on a dark orange backdrop: one shade in grey at this size, with no edge to find. A planet on black space looks the same to the check, and must pass. |
| `k2kEaA7ICjc` 10.0 s | the same kind: a dark graphic on a dark backdrop of another colour. |

All three Shorts are still caught through their other frames (`rvug71d7Dqk` at 20 s; `C8lPx5N2DwM` at 10, 18, 22 and
28 s; `k2kEaA7ICjc` at 16 and 24 s), so the whole-Short rule fails each of them.

## What the check measures now

Fill has no fine detail. A blurred, enlarged copy is smooth at one-pixel spacing, and a flat band has nothing. A real
picture nearly always has some, even a soft wall behind a subject. So, on the 108 x 192 grey frame:

1. Sharp pixel = the second difference, left-right or up-down, is 8 grey levels or more.
2. Caption rows are left out: a row with 3 or more pixels both bright and very sharp, and 4 rows each side.
3. The outer top (rows 3 to 41) and the outer bottom (rows 150 to 188) lie outside the picture band of any picture
   from 16:9 to square. Each may have at most **8%** of its pixels sharp.
4. The middle (rows 76 to 115) must have at least **6%** sharp: there is a picture between them.
5. The outside must be fill and not the picture's own plain background. It is fill when it still holds a picture's
   brightness (spread of 6-pixel block means of 10 or more on a side), or its top and bottom differ in brightness by
   15 or more, or it is plain with a straight edge above and below the picture. One flat shade above and below
   with no straight edge is a subject on its own backdrop, and passes.
6. Mirrored fill is looked for on its own, as before.

The margins on the labelled set: the padded frames have at most 6.4% sharp outside; the full frames with a picture in
the middle have at least 10.2%. Two full frames have nothing sharp outside (an eclipse corona, a globe on black) and
pass on step 4: their middle is smooth too.

## The whole Short

`check` now samples one frame a second. It fails the Short when more than 10% of those frames are padded, and names
the stretches in seconds. The opening rule is unchanged (frame 0, or most frames to 0.5 s). A stretch the cut's own
meta file names as the end card (`end_card.start_s` with `len_s`, or `end_card_window_s`) is left out of the count
and reported as a warning if it sits on fill. With no meta, nothing is left out.

## Every labelled frame

| Short | t (s) | label | the check says | sharp above | sharp middle | sharp below | right |
|---|---|---|---|---|---|---|---|
| `ffYKoNVPoqg` | 0.0 | padded | blur-pad | 0.000 | 0.727 | 0.024 | yes |
| `ffYKoNVPoqg` | 4.0 | padded | blur-pad | 0.000 | 0.082 | 0.000 | yes |
| `ffYKoNVPoqg` | 14.0 | padded | blur-pad | 0.000 | 0.177 | 0.000 | yes |
| `bSjWiCbB7pY` | 4.0 | padded | blur-pad | 0.000 | 0.519 | 0.064 | yes |
| `bSjWiCbB7pY` | 10.0 | padded | blur-pad | 0.000 | 0.273 | 0.000 | yes |
| `bSjWiCbB7pY` | 14.0 | padded | mirror | - | - | - | yes |
| `bSjWiCbB7pY` | 16.0 | padded | blur-pad | 0.000 | 0.540 | 0.000 | yes |
| `HZGTovJu_TQ` | 24.0 | padded | blur-pad | 0.000 | 0.325 | 0.000 | yes |
| `kKN8Ale42sE` | 6.0 | padded | blur-pad | 0.000 | 0.206 | 0.000 | yes |
| `cwU_0WWeNZ4` | 20.0 | padded | blur-pad | 0.000 | 0.329 | 0.000 | yes |
| `cwU_0WWeNZ4` | 22.0 | padded | blur-pad | 0.000 | 0.329 | 0.000 | yes |
| `rvug71d7Dqk` | 0.0 | padded | fills the frame | 0.358 | 0.729 | 0.132 | no |
| `rvug71d7Dqk` | 2.0 | padded | fills the frame | 0.340 | 0.792 | 0.112 | no |
| `rvug71d7Dqk` | 20.0 | padded | blur-pad | 0.015 | 0.693 | 0.012 | yes |
| `xdurJQcoiGM` | 16.0 | padded | blur-pad | 0.000 | 0.392 | 0.000 | yes |
| `C8lPx5N2DwM` | 6.0 | padded | fills the frame | 0.000 | 0.273 | 0.000 | no |
| `C8lPx5N2DwM` | 10.0 | padded | blur-pad | 0.000 | 0.679 | 0.000 | yes |
| `C8lPx5N2DwM` | 18.0 | padded | blur-pad | 0.001 | 0.503 | 0.001 | yes |
| `C8lPx5N2DwM` | 22.0 | padded | blur-pad | 0.000 | 0.516 | 0.000 | yes |
| `C8lPx5N2DwM` | 28.0 | padded | blur-pad | 0.000 | 0.555 | 0.000 | yes |
| `SWDCZfWZVao` | 4.0 | padded | blur-pad | 0.000 | 0.484 | 0.000 | yes |
| `SWDCZfWZVao` | 14.0 | padded | blur-pad | 0.048 | 0.509 | 0.048 | yes |
| `k2kEaA7ICjc` | 10.0 | padded | fills the frame | 0.000 | 0.224 | 0.000 | no |
| `k2kEaA7ICjc` | 16.0 | padded | blur-pad | 0.000 | 0.112 | 0.000 | yes |
| `k2kEaA7ICjc` | 24.0 | padded | blur-pad | 0.000 | 0.492 | 0.000 | yes |
| `heiGCnGKTkE` | 6.0 | padded | blur-pad | 0.000 | 0.107 | 0.000 | yes |
| `heiGCnGKTkE` | 14.0 | padded | blur-pad | 0.000 | 0.139 | 0.000 | yes |
| `heiGCnGKTkE` | 20.0 | padded | blur-pad | 0.000 | 0.163 | 0.000 | yes |
| `ChbsigHD5_o` | 0.0 | full | fills the frame | 0.022 | 0.539 | 0.102 | yes |
| `ChbsigHD5_o` | 2.0 | full | fills the frame | 0.006 | 0.607 | 0.213 | yes |
| `ChbsigHD5_o` | 20.0 | full | fills the frame | 0.174 | 0.153 | 0.507 | yes |
| `ChbsigHD5_o` | 24.0 | full | fills the frame | 0.009 | 0.309 | 0.105 | yes |
| `cLKDiYP55J8` | 0.0 | full | fills the frame | - | 0.655 | - | yes |
| `cLKDiYP55J8` | 0.5 | full | fills the frame | 0.229 | 0.659 | 0.273 | yes |
| `cLKDiYP55J8` | 4.0 | full | fills the frame | 0.249 | 0.422 | 0.330 | yes |
| `cLKDiYP55J8` | 22.0 | full | fills the frame | - | 0.421 | - | yes |
| `Wvjd8g0CpzE` | 0.0 | full | fills the frame | - | 0.744 | - | yes |
| `Wvjd8g0CpzE` | 22.0 | full | fills the frame | 0.051 | 0.587 | 0.156 | yes |
| `xzKoHg0E0_U` | 0.0 | full | fills the frame | - | 0.796 | - | yes |
| `xzKoHg0E0_U` | 6.0 | full | fills the frame | 0.074 | 0.470 | 0.145 | yes |
| `xgx2lYHhYZM` | 0.0 | full | fills the frame | 0.108 | 0.701 | 0.908 | yes |
| `xgx2lYHhYZM` | 18.0 | full | fills the frame | 0.000 | 0.412 | 0.433 | yes |
| `Bks_JLId1ew` | 0.0 | full | fills the frame | - | 0.617 | - | yes |
| `Bks_JLId1ew` | 14.0 | full | fills the frame | 0.074 | 0.389 | 0.229 | yes |
| `MScK2CK2ZFg` | 0.0 | full | fills the frame | - | 0.820 | - | yes |
| `MScK2CK2ZFg` | 8.0 | full | fills the frame | - | 0.360 | - | yes |
| `MScK2CK2ZFg` | 16.0 | full | fills the frame | 0.000 | 0.035 | 0.001 | yes |
| `QEoYKIVvKBA` | 0.0 | full | fills the frame | 0.140 | 0.203 | 0.138 | yes |
| `QEoYKIVvKBA` | 6.0 | full | fills the frame | 0.344 | 0.752 | 0.213 | yes |
| `f17XCtUmN-g` | 0.0 | full | fills the frame | 0.246 | 0.363 | 0.058 | yes |
| `f17XCtUmN-g` | 22.0 | full | fills the frame | 0.218 | 0.669 | 0.061 | yes |
| `xvarZP2aYyE` | 10.0 | full | fills the frame | 0.162 | 0.434 | 0.196 | yes |
| `Dm4xsF1Ateg` | 4.0 | full | fills the frame | 0.000 | 0.761 | 0.886 | yes |
| `xdurJQcoiGM` | 14.0 | full | fills the frame | - | 0.211 | - | yes |
| `bSjWiCbB7pY` | 22.0 | full | fills the frame | 0.352 | 0.403 | 0.222 | yes |
| `ffYKoNVPoqg` | 8.0 | full | fills the frame | 0.046 | 0.000 | 0.040 | yes |

A dash means the frame was decided before that measure (mirror), or captions cover that zone.
