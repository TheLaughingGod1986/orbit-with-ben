# 029 Is Betelgeuse About to Explode? SHOT_LIST v01 (Claude, 8 Oct 2026)

Timed to `02_Voiceover/stt/betelgeuse_vo_v01/stt_raw.json` (VO `betelgeuse_vo_v01`, 515.2 s, Scribe 99.2%, Claude VO PASS; text files in 9d64a3d). Times are sentence spans from Scribe, and the chapter gaps are 0.7 s (`chapters_index.json`). Each row is a beat. **`cuts` is the number of 4–6 s cuts to split it into.** After the cut, check every row with `align_shot_list.py` and `clip_check.py`.

**Venus lessons, applied from the start** (the Orion-rising opening appears at rows 1 and 39; 39 is the deliberate return):
- No still more than twice in the film, and the second use gets a new framing. The tally is at the foot of this file.
- Upscale ≤ 2.35×, asserted in the assembler.
- Every cut sits in a VO pause.
- The pack carries `row_###.jpg` frames and the per-row sheet.
- Every harvested item gets its **title and licence checked** before it enters the pool.

**Spend:** free Vertex only, with a £5 floor.
- **Omni Orbit beats:** two (the hilltop thumb, the field under the flare). Neither has a planet in frame.
- **Veo props:** none. The code graphics cover the gaps, so everything else is £0.

**Sources:**
- **CODE** = `07_Edit-Project/code_graphics.py` (text-free; this commit).
- NASA is public domain.
- ESO, ESA/Hubble, ESA/Webb and NOIRLab are CC BY 4.0. Credit them.
- The Met Museum is CC0.
- **No DSS2 or Aladin cut-outs** (licence). **No news footage or headlines**: the 2020 scare is told with the real ESO images, not the coverage. No branded stock.

**Orion time-lapses:** most rows below use ESO night-sky footage. Harvest at least **three different ESO clips with Orion in them**. Spans are lettered A–G. **No span is used twice**, except the deliberate return in row 39.

| # | Ch | VO in–out (s) | Dur | Source | Asset | Cuts | Notes |
|---:|---|---|---:|---|---|---:|---|
| 1 | 0 Open | 0.08–5.70 | 5.6 | ESO | Orion rising over a real horizon (span A), already moving, Betelgeuse orange on the upper left | 1 | **Frame 0 lock.** The stars have visibly moved by 1 s. No fade, no title, no Orbit. |
| 2 | 0 Open | 6.54–13.34 | 6.8 | ESO | A tighter Orion span on the orange shoulder star (span B), then the ESO/ALMA surface image of Betelgeuse (eso1726a), tight | 2 | "So is Betelgeuse about to explode?" |
| 3 | 0 Open | 13.96–21.40 | 7.4 | CODE | `orion --seconds 10` (the flare lands on "daytime sky"), wide | 2 | A preview only. The full flare is rows 25–27, at a different framing. |
| 4 | 0 Open | 22.58–36.94 | 14.4 | CODE | Promise beat: `scale` → `dip` → `shells` (about 4.8 s each) | 3 | One cut per promise, in the sentence's pauses. |
| 5 | 1 The Star in Orion's Shoulder | 37.74–48.58 | 10.8 | ESO/CODE | ESO/ALMA eso1726a, a slow wide push (second use), then `scale --seconds 8` from 41.9 s | 2 | **VISUAL MUST.** The edge passes Mars's orbit at about 46 s, on "past the orbit of Mars". |
| 6 | 1 The Star in Orion's Shoulder | 49.46–61.74 | 12.3 | ESO | ESO Paranal night-sky time-lapse, then the ESO VLT/SPHERE January 2019 image (eso2003, the single panel) | 2 | "So big and so restless." |
| 7 | 1 The Star in Orion's Shoulder | 62.46–72.84 | 10.4 | NASA/ESO | NASA SDO full Sun, then eso2003 January 2019, a tight crop (second use) | 2 | 4.5 billion years against 10 million. |
| 8 | 1 The Star in Orion's Shoulder | 73.86–91.92 | 18.1 | NASA/ESA | Hubble Westerlund 2 (wide, then tight), then ESA/Hubble R136 in 30 Doradus | 4 | Heavy, bright stars: "live fast and die young". |
| 9 | 1 The Star in Orion's Shoulder | 92.92–105.48 | 12.6 | CODE | `finder --seconds 12.6`: the belt glows, the trail runs up and left, and Betelgeuse brightens | 2 | Cut at 100.04–100.78. The second cut is a tighter reframe on the orange star. |
| 10 | 2 The Great Dimming | 106.38–114.20 | 7.8 | ESO/CODE | Orion span C (the orange point), then `dip --seconds 15` starting at 109.5 s | 2 | The trough lands at about 117 s. |
| 11 | 2 The Great Dimming | 115.00–123.16 | 8.2 | CODE | `dip` continued (the trough, then the start of the climb) | 2 | Split by reframing (wide, then tight on the trough). "About a third"; "more than fifty years". |
| 12 | 2 The Great Dimming | 123.96–129.38 | 5.4 | OMNI | `orbit_thumb_omni_v01`: Orbit on a winter hilltop at night holds up a thumb towards Orion, squints, lowers it, a little worried, and waits | 1 | **ORBIT ACTS.** Start frame: Orbit on a dark hill under stars, **no planet in frame**. Vertex `global`, `orbit_shot=True`, one take. If it fails, Orion span C holds. |
| 13 | 2 The Great Dimming | 130.42–137.80 | 7.4 | ESO | ESO VLT/SPHERE January 2019 vs December 2019 (the eso2003 comparison image), side by side; then push into December | 2 | **VISUAL MUST.** The dim lower half is visible. "It was not." |
| 14 | 2 The Great Dimming | 138.44–147.16 | 8.7 | ESA/Hubble, ESO | The Hubble surface-mass-ejection illustration (2022), then the ESO dust-veil artist's impression (eso2109) | 2 | **VISUAL MUST.** Both are clearly illustrations. No Orbit. |
| 15 | 2 The Great Dimming | 148.04–157.76 | 9.7 | ESO/CODE | Orion span D, tight on the single point, then `dip` (second use, tight on the trough) | 2 | "All we see is a point of light." |
| 16 | 2 The Great Dimming | 158.58–168.98 | 10.4 | ESO | Orion span E (the star back to normal), then the ESO VLT/VISIR nebula around Betelgeuse (eso1121) | 2 | "It throws off pieces of itself." |
| 17 | 3 How a Giant Star Dies | 170.00–180.88 | 10.9 | NASA/CODE | NASA SDO Sun (second use, a limb or prominence framing), then the `shells` start frame held | 2 | The balance: gravity in, fusion out. |
| 18 | 3 How a Giant Star Dies | 181.70–199.08 | 17.4 | CODE | `shells --seconds 55`, 0 s at 181.70 (the iron core growing) | 4 | Split by reframing (wide, tight, wide, tight). One continuous render. |
| 19 | 3 How a Giant Star Dies | 199.78–211.06 | 11.3 | CODE | `shells` continued, tight on the grey iron core | 2 | "The end of the line is iron." |
| 20 | 3 How a Giant Star Dies | 211.94–225.58 | 13.6 | CODE/NASA | `shells` wide: the collapse lands at 211.95, on "In less than a second", and the shock ring follows; then Hubble Crab Nebula, tight on the filaments, at 224.02 | 3 | **VISUAL MUST.** "That is a supernova." The Crab's full frame is saved for row 35. |
| 21 | 3 How a Giant Star Dies | 226.64–241.88 | 15.2 | NASA | NASA GSFC neutron-star illustration, then the 007 hero plate (one line, a callback), then a NASA GSFC black-hole visualisation | 3 | A teaspoon weighs about a mountain. |
| 22 | 3 How a Giant Star Dies | 242.70–247.18 | 4.5 | CARD | Remotion subscribe card (house) | 1 |  |
| 23 | 4 The Night It Goes | 248.06–254.38 | 6.3 | ESO | ESO Paranal night-landscape time-lapse (a clip not used in row 6) | 1 | "Imagine the night." |
| 24 | 4 The Night It Goes | 255.30–273.10 | 17.8 | ICRR/NASA | The Super-Kamiokande inner tank with its photomultipliers (Kamioka Observatory, ICRR, The University of Tokyo), then NASA DSCOVR EPIC Earth, then a second Super-K plate | 4 | **VISUAL MUST.** **Licence gate:** use ICRR images only if their terms allow use on a monetised channel. Otherwise use IceCube (NSF) detector photos, if their licence clears. Otherwise use the ESO night sky, and tell Claude. |
| 25 | 4 The Night It Goes | 274.12–282.16 | 8.0 | CODE | `orion --seconds 41`, 0 s at 270.5 (use from 3.6 s): the shoulder flares to white on "Within days" (276.7) | 2 | **VISUAL MUST.** Split by reframing (wide, then tight on the flare). |
| 26 | 4 The Night It Goes | 282.92–290.04 | 7.1 | OMNI/NASA | `orbit_flare_omni_v01`: Orbit on a dark field at night looks up as one point of light swells into a brilliant white dot, lifts a hand to shade the visor, and stares; then a NASA SVS half Moon in a night sky | 2 | **ORBIT ACTS.** Start frame: Orbit on a dark field under stars, **no planet in frame**. One take. If it fails, the `orion` peak holds. |
| 27 | 4 The Night It Goes | 290.98–309.46 | 18.5 | CODE | `orion` continued (20.5–39 s of the render): the fade, until the shoulder is empty | 4 | Split by reframing. The fade runs exactly 290.98–309.5. "A different Orion." |
| 28 | 4 The Night It Goes | 310.80–325.46 | 14.7 | NASA/ESO | NASA DSCOVR EPIC Earth (second use, a new framing), then an ESO Milky Way time-lapse, then an ESO photo of people under the night sky | 3 | "The show, not the danger." No disaster imagery. |
| 29 | 4 The Night It Goes | 326.56–342.14 | 15.6 | ESO/Met | Orion span F, then a Met Open Access 15th-century astrolabe (CC0), slow push | 3 | "The late Middle Ages." |
| 30 | 5 So When? | 342.92–357.62 | 14.7 | ESO | Orion span G, then the ESO VLT under the night sky (telescopes, no lasers needed) | 3 | "About a hundred thousand years." |
| 31 | 5 So When? | 359.36–378.30 | 18.9 | CODE | The `shells` start frame (tight on the core), then `twins --seconds 16` from 362.6 s | 4 | The wedges open at about 367 s on "deep in the core" and close at about 376 s on "look almost the same". |
| 32 | 5 So When? | 379.44–392.00 | 12.6 | ESO/ESA-Hubble | eso2003 December 2019 (the single panel), then the Hubble mass-ejection illustration (second use, a new framing) | 3 | "The star keeps surprising us." |
| 33 | 5 So When? | 393.34–412.74 | 19.4 | NOIRLab | The Gemini North 'Alopeke speckle image from the 2025 companion release, then the NOIRLab illustration of the pair | 4 | **VISUAL MUST.** Credit NOIRLab/NSF/AURA. The illustration must read clearly as an illustration. |
| 34 | 5 So When? | 413.96–431.08 | 17.1 | NOIRLab | Gemini North at night, then the pair illustration (second use, wider), then the Gemini North dome | 3 | "Still tentative"; "late 2027". No Orbit. |
| 35 | 5 So When? | 432.60–452.30 | 19.7 | Met/NASA | A Met Open Access Northern Song (960–1127) painting or object (CC0), slow push, then Hubble Crab Nebula **in full** (second use), slow push | 4 | **VISUAL MUST.** The caption stays generic: don't claim the Met item shows the 1054 record. |
| 36 | 5 So When? | 453.84–465.82 | 12.0 | ESO | Orion span B (a later part of it, not the row 2 frames), then ESO VISIR eso1121 (second use) | 3 | "But it will." |
| 37 | 5 So When? | 466.92–484.26 | 17.3 | NASA/ESA | Cassiopeia A (Chandra or JWST), then the JWST Pillars of Creation | 4 | **VISUAL MUST.** |
| 38 | 5 So When? | 485.84–496.36 | 10.5 | NASA/ESO | Hubble Orion Nebula (M42, in Orion's sword), then an ESO night landscape | 2 | The bigger question. |
| 39 | 5 So When? | 497.42–514.26 (+hold) | 16.8 + 3 | ESO/NASA | ALMA HL Tau disc (ESO/NAOJ/NRAO), then the NASA Apollo 17 Blue Marble (AS17-148-22727), then **return to the opening: Orion rising (span A, a later part), Betelgeuse still orange**. Hold 2–3 s past the last word, then fade | 4 | **VISUAL MUST return.** No goodbye card and no Orbit in the last shot. The end screen is added in Studio; the 030 handoff is a pickup later. |

## Code graphics (Claude, this commit)

`029/07_Edit-Project/code_graphics.py` contains `scale`, `dip`, `shells`, `orion`, `finder` and `twins`. They're text-free and run at 30 fps. Claude checked stills of all six on 8 Oct, and fixed three problems on the way:
- `scale`: the orbits now draw over the star's fill.
- `orion`: the flare is a soft glow, not hard rings.
- `twins`: the halos are tight and the cutaways are readable.

Render each one with the `--seconds` value given in its row, so the key moment lands on its word (the Venus lesson: no freeze-padding).

| Graphic | Render | Starts at (VO s) | Key moment |
|---|---|---|---|
| `scale` | `--seconds 8` | 41.9 | Passes Mars about 46 |
| `dip` | `--seconds 15` | 109.5 | Trough about 117 |
| `shells` | `--seconds 55` | 181.70 | Collapse 211.95 |
| `orion` | `--seconds 41` | 270.5 | Flare 276.7–282.8, fade 291.0–309.5 |
| `twins` | `--seconds 16` | 362.6 | Open about 367, close about 376 |

## Generation queue (after the 028 picture; frame sheets for Claude PASS)

1. `orbit_thumb_omni_v01` (row 12)
2. `orbit_flare_omni_v01` (row 26)

Orbit locks, as always: `orbit_shot=True`, a sidecar from `ORBIT_REF`, `global`.

## Harvest list (free, licence-checked; pool in `nasa_pool_v01.json` like 022/023)

- **ESO:**
  - At least three Orion night-sky time-lapses (spans A–G).
  - Paranal night landscapes and the VLT under the sky.
  - eso1726a (ALMA surface).
  - eso2003 (January 2019 and December 2019 singles, plus the comparison).
  - eso2109 (dust-veil impression).
  - eso1121 (VISIR nebula).
  - The ALMA HL Tau disc.
- **ESA/Hubble and NASA:**
  - SDO Sun.
  - Westerlund 2 and R136.
  - The 2022 mass-ejection illustration.
  - The Crab Nebula.
  - Neutron-star and black-hole visualisations (GSFC).
  - DSCOVR EPIC Earth.
  - An SVS half Moon.
  - Cassiopeia A.
  - JWST Pillars of Creation.
  - M42.
  - Apollo 17 Blue Marble.
- **NOIRLab:** the 2025 Betelgeuse companion release (speckle image, illustration), plus Gemini North photos.
- **Met Open Access (CC0):** a 15th-century astrolabe, and a Northern Song painting or object.
- **Licence gate:** Super-Kamiokande (row 24), as described in that row.
- **Before each item goes in, Cursor checks its title and licence.**

## Still tally (cap two, the second with a new framing)

| Still | Rows |
|---|---|
| eso1726a | 2, 5 |
| eso2003 January | 6, 7 |
| eso2003 comparison | 13 |
| eso2003 December | 32 |
| Mass-ejection illustration | 14, 32 |
| eso2109 | 14 |
| eso1121 | 16, 36 |
| SDO | 7, 17 |
| Westerlund 2 | 8 (two framings in one row; count it as two) |
| Crab | 20, 35 |
| EPIC | 24, 28 |
| Pair illustration | 33, 34 |

Everything else is used once.

## Shorts

The three Shorts take their plates from this list. Their scripts come after the 028 Shorts. Shorts rows get drafted for Claude's review when the long's picture starts, as for 026–028.
