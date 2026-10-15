# 028 price review v01

Cursor, 15 Oct 2026, J0310. Source plates, prompts and prices only. **No mint. No spend.** Parked for Chief's price pass.

Locked VO: `star_coming_vo_v01` (J0032, 8 Oct). Shot list: `SHOT_LIST_v01.md` (Claude, 8 Oct). The shot list's old £5 Vertex floor is not the rule any more. This table is Flow-first, on the same rates as HOS 009 J0261.

## Readings

- Flow: **23730** credits at 2026-10-15T12:58:32Z. No spend logged after that.
- Vertex promo: **£71.02** at 2026-10-15T07:30:31Z. Usable **£70.02** after the £1 margin on that reading. No spend logged after it. Free Trial is £0. J0107 is done, so the HOS 006 Part 03 reserve is not holding this.

## Totals

| | plates | Quality | Fast | Omni | code | harvest | gap | blocked | Flow try-1 | Flow expected | Vertex try-1 | Vertex expected |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Film** | **62** | **1** | **1** | **2** | **22** | **28** (+2 on licence hold) | **4** | **1** | **110** | **279** | **£1.92** | **£4.57** |

All on Flow, for the two Veo plates only: FITS (279 expected vs 23730 left).
Those two plates on Vertex: FITS (£4.57 expected vs £70.02 usable).
The two Orbit plates are Omni only. They are not in either total. Omni is unpriced and billed late.
Code graphics, the subscribe card and the harvest plates are £0. Nothing is authorised to generate.

Rates are 006/008/009's: Flow Fast 10 / Quality 100 a take; expected uses 005's takes-per-KEEP (Quality 2.59, Fast 1.96). Vertex is list price, 1080p, £0.80 per dollar, clip length 8 s.

## What the picture actually is

Most of the film is credited NASA, ESA or ESO footage, or a graphic we already draw in `code_graphics.py`. Flow is only the night road and the football pitch. That is the Flow-first split this shot list supports.

| Plate | Route | Why |
|---|---|---|
| `night_road_veo_v01` | Quality | Headlights on a night road. The shot list said Fast. Fragile light stays Quality unless the Chief waives it. |
| `football_pitch_veo_v01` | Fast | Empty pitch at dusk, no glow. The Chief can lift it to Quality. |
| `orbit_binoculars_omni_v01`, `orbit_ice_omni_v01` | Omni | Orbit never goes through Flow or Veo. No planet in either start frame. |
| `drift` `path` `scale` `shell` `shower` `sky` `traffic` | £0 code | Already in `code_graphics.py`. Text-free. Not a second mint when a later row uses the same graphic. |

## Harvest stretches

A still may appear twice. Footage may not come back in more than five stretches.

- `gaia_motion_1_6my` × 6 OVER THE FIVE-STRETCH CAP: r01_stars_streaming, r02_gaia_span_2, r12_stars_move, r27_leaving, r35_gaia_wide, r38_return
- `gaia_edr3_sky` × 2 second use; still cap reached: r03_serpens_sky, r34_sky_wide
- `eso_mw_lasilla` × 1: r06_milky_way
- `sdo_aia335` × 1: r07_sun
- `gaia_gliese_encounter` × 1: r10_gliese_approach
- `proxima` × 1: r12_proxima
- `eso_startrails` × 1: r13_star_trails
- `gaia_craft` × 1: r15_gaia_craft
- `neptune` × 1: r17_neptune
- `neowise_dc` × 2 second use; still cap reached: r22_neowise, r38_neowise_2
- `iss_sunrise` × 1: r24_sunrise
- `hale_bopp` × 2 second use; still cap reached: r26_hale_bopp, r28_hale_bopp_2
- `comet_a3` × 1: r26_a3
- `jupiter_juno` × 1: r28_jupiter
- `saturn` × 1: r28_saturn
- `eso_chajnantor` × 1: r29_night
- `conjunction` × 1: r29_twilight
- `moon_lro` × 2 second use; still cap reached: r30_moon, r31_moon_2
- `wise_sky` × 1: r32_wise_sky
- `wise_craft` × 1: r33_wise_craft
- `ngc3603` × 1: r37_cluster

## Holds, before any cut

1. **Gliese motion, six stretches.** `gaia_motion_1_6my` is on r01, r02, r12, r27, r35 and r38. Five is the cap. r38 is the visual-must return to the opening. Drop r35, or the Chief waives the sixth.
2. **K dwarf blocked.** The Hubble 2020 release the shot list names (`opo2006a`) is a labelled chart. It does not go in. No clean unlabelled K-dwarf plate was found.
3. **SDO is ultraviolet.** `GSFC_20171208_Archive_e002035` is AIA 335, not visible light. The second framing (the limb) is not gathered.
4. **Hale-Bopp licence.** `phot-mar14-hbs-2` is on the ESO site (CC BY 4.0 default). The 1997 event page says © Eckhard Slawik. Both uses wait on the Chief.
5. **Three files are pages only.** Hipparcos art, the Oort Cloud illustration (do not use the Feild inset diagram), and the Tafreshi La Silla lapse (`bt_lasilla_fd2`, page 200, file 404 on the usual paths).
6. **WISE all-sky** is a map. Look for axis labels before it is cut.
7. **Gaia animations** are data films. `picture_qa` can fail a diagram. They are the moving source the shot list names. The annotated 'Tracking stellar motions' cut was not taken.
8. **Juno PIA21974** is colour-enhanced. **PIA01492** is green and orange filters. Say so in the corner credit.
9. **No DSS2, no Aladin, no Rochester Scholz's-star art.** None of those were gathered.
10. **Code graphics stacked in the shot list.** These sit against the rule that two code graphics never run back to back: shower then shell (row 4), drift then path then sky (row 5), path then path (rows 15–16), shower then shower (rows 24–25). The cut needs a real plate between them, or the Chief accepts each stack as one beat.

## For the price pass

- Whether the night road stays Quality (100 credits try-1, 259 expected, £1.28 / £3.32 on Vertex) or drops to Fast.
- Whether the dusk pitch stays Fast (10 / 20, £0.64 / £1.25).
- The two Omni takes are extra, unpriced, and not part of the £4.57. They wait on a Vertex reading the day they are minted.
- Which of the six Gliese-motion stretches is cut so the film stays inside five.
- The Hale-Bopp licence, and who fills the three gaps (Hipparcos, Oort, Tafreshi) plus a visible-light Sun.

Files: `SOURCE_POOL_v01.json`, `PLATE_BOARDS_v01.json`. Rebuild with `python3 _build_plate_boards_v01.py`.
