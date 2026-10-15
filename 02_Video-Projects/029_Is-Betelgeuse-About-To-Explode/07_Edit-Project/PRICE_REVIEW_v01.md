# 029 price review v01

Cursor, 15 Oct 2026, J0311. Source plates and prices only. **No mint. No spend.** Parked for Chief's price pass.

Locked VO: `betelgeuse_vo_v01` (J0040, 8 Oct, 515.2 s). Shot list: `SHOT_LIST_v01.md` (Claude, 8 Oct). The shot list's old £5 Vertex floor is not the rule any more. This table is Flow-first, on the same rates as HOS 009 J0261 and 028 J0310.

## Readings

- Flow: **23730** credits at 2026-10-15T12:58:32Z. No spend logged after that.
- Vertex promo: **£71.02** at 2026-10-15T07:30:31Z. Usable **£70.02** after the £1 margin. No spend logged after it. Free Trial is £0. J0107 is done, so the HOS 006 Part 03 reserve is not holding this.

## Totals

| | plates | Quality | Fast | Omni | code | harvest | gap | hold | Flow try-1 | Flow expected | Vertex try-1 | Vertex expected |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Film** | **73** | **0** | **0** | **2** | **17** | **26** | **25** | **2** | **0** | **0** | **£0.00** | **£0.00** |

The shot list names no Veo prop, and none was added. Flow expected is 0, which fits 23730 left.
Vertex Veo expected is £0.00, which fits the usable promo.
The two Orbit plates are Omni only. They are not in either total. Omni is unpriced and billed late.
Code graphics, the subscribe card and the harvest plates are £0. Nothing is authorised to generate.

Rates are 006/008/009/028's: Flow Fast 10 / Quality 100 a take; expected uses 005's takes-per-KEEP (Quality 2.59, Fast 1.96). Vertex is list price, 1080p, £0.80 per dollar, clip length 8 s.

## What the picture actually is

Most of the locked picture is credited ESO, ESA/Hubble or NASA, or a graphic already in `code_graphics.py`. There is no night-road equivalent: the shot list's moving plates are real night-sky films, not generated props.

| Plate | Route | Why |
|---|---|---|
| `orbit_thumb_omni_v01`, `orbit_flare_omni_v01` | Omni | Orbit never goes through Flow or Veo. No planet in either start frame. |
| `scale` `dip` `shells` `orion` `finder` `twins` | £0 code | Already in `code_graphics.py`. Text-free. A later row of the same graphic is not a second mint. |

## Harvest stretches

A still may appear twice. Footage may not come back in more than five stretches.

- `orion_rise_vlt` × 2 second use; still cap reached: r01_orion_rise, r39_return
- `orion_over_paranal` × 2 second use; still cap reached: r02_orion_b, r36_orion_b
- `sphere_jan` × 2 second use; still cap reached: r06_sphere_jan, r07_sphere_jan
- `westerlund` × 2 second use; still cap reached: r08_westerlund_w, r08_westerlund_t
- `mass_ejection` × 2 second use; still cap reached: r14_ejection, r32_ejection
- `visir_flames` × 2 second use; still cap reached: r16_visir, r36_visir
- `crab` × 2 second use; still cap reached: r20_crab, r35_crab
- `companion_orion` × 2 second use; still cap reached: r33_pair, r34_pair
- `sdo_aia335` × 1: r07_sdo
- `tarantula` × 1: r08_tarantula
- `sphere_compare` × 1: r13_compare
- `dust_impression` × 1: r14_dust
- `sphere_dec` × 1: r32_sphere_dec
- `companion_speckle` × 1: r33_speckle
- `m42` × 1: r38_m42
- `alma_orion_set` × 1: r38_night
- `hl_tau` × 1: r39_hltau
- `blue_marble` × 1: r39_marble

## Holds, before any cut

1. **eso1726a is Antares.** The shot list uses it as the ALMA surface of Betelgeuse at rows 2 and 5. The page title is the VLTI view of Antares. It is rejected. Those two beats are gaps.
2. **Only two Orion clips.** `vlttimelapseorion` (6 s, rising Orion, span A) and `bt-paranal-orion135mm` (9 s, Orion over Paranal, span B). Spans C, D, E, F and G were not found. The 6 s rise cannot supply a later unused part for the row 39 return, and the hold past the last word is longer than the clip.
3. **SDO is ultraviolet.** The file is the one J0310 read as AIA 335. This run only checked HEAD 200. The limb framing for row 17 was not gathered.
4. **DSCOVR was not found.** PIA18033 is a Suomi NPP VIIRS montage. It is rejected. Both EPIC beats are gaps.
5. **Super-Kamiokande is on hold.** No ICRR file, and no monetised-use term, was gathered. IceCube was not gathered either.
6. **Met API returned HTTP 410.** The astrolabe and the Northern Song object are gaps.
7. **JWST Pillars and Cassiopeia A are gaps.** The Hubble Pillars (`heic1501a`) are rejected as a substitute.
8. **Neutron-star illustration, black-hole visualisation, SVS half Moon and the 007 hero callback** have no file pinned this run.
9. **Gemini North at night and the dome** are not in the noirlab2523 images that were opened. The companion images are `noirlab2523c` (non-annotated) and `noirlab2523b` (in Orion). Confirm `noirlab2523b` is not a labelled chart. `noirlab2523a` is annotated and rejected. `noirlab2523f` is credited to IAU and Sky & Telescope and is rejected.
10. **Dust impression is heic2014a**, not an eso2109 still. The eso2109 frames checked are SPHERE photos. `eso2109b` is annotated and rejected.
11. **Tarantula plate.** `heic0416a` is 30 Doradus. The title does not say R136.
12. **Code graphics stacked in the shot list.** Scale, dip and shells sit together in row 4. Dip continues into row 11. Shells run through rows 17–20 and return at row 31 beside twins. Two code graphics never run back to back unless a real plate sits between them, or the Chief accepts each stack as one beat.
13. **NOIRLab licence.** The image pages link the usage page. The default was not re-read this run. Treat them as CC BY 4.0 only if that page still says so.

## For the price pass

- There is no Flow plate to waive from Quality to Fast. Expected Flow is 0.
- The two Omni takes are extra, unpriced, and not part of the £0.00 Veo total. They wait on a Vertex reading the day they are minted.
- Whether row 2 and row 5 stay gaps until a real Betelgeuse surface (not Antares) is gathered.
- Whether spans C–G block the cut, and whether the 6 s Orion rise is allowed to return at the end.
- Super-K versus IceCube versus dropping row 24 to a night-sky plate.
- Who fills DSCOVR, the Met objects, JWST, Cassiopeia A, the GSFC illustrations, the half Moon, and Gemini North.

Files: `SOURCE_POOL_v01.json`, `PLATE_BOARDS_v01.json`. Rebuild with `python3 _build_plate_boards_v01.py`.
