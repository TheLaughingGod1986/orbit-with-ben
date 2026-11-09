# J1308 assembly report — AR1, AR2, AR3

31 Oct 2026. Cursor. £0. No mint, no upload, no schedule.
VO is the h40 lock. Graphics are the h42 v04 pack (`graphics_j1307_v04/`), re-timed with
`render_graphics.py --only/--duration` into `07_Edit-Project/graphics_j1308_v01/`.
v02, v03 and v04 were not overwritten. `ar1_size` is not used (h40).
Media stays under `07_Edit-Project/`.

AR1 is the v01 master. Its picture, polish, loop and SFX gates already passed, so it was not rebuilt.
AR2 and AR3 are v02. v01 of those two stays on disk: the map slabs failed picture_qa there.

## AR1

- Master: `07_Edit-Project/assembly_j1308_v01/ar1/owb_apophis_ar1_v01.mp4`
- sha256: `49b3e4f0f7276885f942d3451978eba33c9a2fec68216fcafdd79466f877cd07`
- Cut: VO 18.365 s + 1.0 s loop = **19.365 s** (inside 17–20).
- Payoff (C8): "miss" at 12.4 s, **64.0%** of the cut. First word 0.0 s. Last word 18.06 s.
- Title interval: 17.1–18.3 s, on "Look up knowing", with no graphic under it.
- Loudness −14.4 LUFS, true peak −1.5 dBTP.
- Loop: loop_diff_masked 8.99, open step 8.63, head [0, 0, 0, 0, 0]. Pass.
- picture_qa PASS, polish_gate PASS, sfx level PASS.

## AR2

- Master: `07_Edit-Project/assembly_j1308_v02/ar2/owb_apophis_ar2_v02.mp4`
- sha256: `73cbb7c0174fcbdf774a059f189ac5ce5b8f3e1274291bbb8e2f4fd47b023405`
- Cut: VO 18.4 s + 1.0 s loop = **19.4 s** (inside 17–20).
- Payoff (C8): "deorbit" at 11.14 s, **57.4%** of the cut. First word 0.12 s. Last word 18.32 s.
- Title interval: 9.2–10.9 s, in the gap before "A deorbit craft", with no graphic under it.
- Loudness −14.3 LUFS, true peak −1.4 dBTP.
- Loop: loop_diff_masked 6.71, open step 6.26, head [0, 0, 0, 0, 0]. Pass.
- picture_qa PASS, polish_gate PASS, sfx level PASS.

## AR3

- Master: `07_Edit-Project/assembly_j1308_v02/ar3/owb_apophis_ar3_v02.mp4`
- sha256: `cfcb23508be4c66bbb3ced01ab656512e1feb0b209fddd7a4f22f88da6ca5dad`
- Cut: VO 17.055 s + 1.0 s loop = **18.055 s** (inside 17–20).
- Payoff (C8): "Totality" at 7.04 s, **39.0%** of the cut. First word 0.0 s. Last word 17.02 s.
- Title interval: 14.7–16.9 s, on "Millions can look up", with no graphic under it.
- Loudness −14.7 LUFS, true peak −1.4 dBTP.
- Loop: loop_diff_masked 1.29, open step 0.86, head [0, 0, 0, 0, 0]. Pass.
- picture_qa PASS, polish_gate PASS, sfx level PASS.

## What v02 changed

- The Point Nemo map and the 2027 path map are full-width opaque bands. On the real plates those edges failed as split panels, and the flat ocean fill failed as a gutter. Assembly feathers the top and bottom 120 px and the side 32 px. The v04 pack is unchanged. Labels stay inside the fade (nemo text from x=155, path text from x=40).
- The 2017 eclipse cells are flat black under the corona. With the credit underneath, that row failed as a gutter. A small horizontal shade is added only on pixels under luma 36.
- The GOES clip holds a frame and then jumps about 8 luma every 7 frames. AR3 frame 0 is source index 32, and the loop tail ends on 31, one ordinary step (about 0.9). Index 30 sits on a jump and failed the seam.

## Plates

- AR2 frame 0 is a code-drawn station (truss, four arrays, modules) moving over the Blue Marble. No Crew-2 file was on the NAS. Five Minutes in Orbit, the Discovery sunrise, the KSC press video and the Bahamas flat are not used.
- NOAA GOES full-disk is cropped to the shadowed limb. The bottom-left NOAA mark is outside the crop.
- The 2017 corona and the 2017 sequence strip are stamped `2017` and credited NASA/Aubrey Gemignani.
- No new music bed. SFX are the house kit (whoosh at frame 0, a short rumble, one tick per graphic).

## Title vs the 9–14 s slot

h40 puts AR1's odds and miss lines, and AR3's path and duration bar, across 9–14 s.
Those graphics stay on the spoken line, so they are not also under a title.
AR2's title is 9.20–10.90 s. AR1's title is on "Look up knowing". AR3's title is on "Millions can look up".

Nothing for Ben. Parked for Chief.
