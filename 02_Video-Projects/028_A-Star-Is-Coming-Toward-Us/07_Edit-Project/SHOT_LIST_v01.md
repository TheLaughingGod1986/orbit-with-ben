# 028 A Star Is Coming Into Our Solar System: SHOT_LIST v01 (Claude, 8 Oct 2026)

Timed to `02_Voiceover/stt/star_coming_vo_v01/stt_raw.json` (VO `star_coming_vo_v01`, 469.4 s, Claude VO PASS `38b1d86`). Times are sentence spans from Scribe. Each row is a beat. **`cuts` is the number of 4–6 s cuts to split it into.** After the cut, check every row with `align_shot_list.py` and `clip_check.py`.

**Venus lessons, applied from the start:**
- No still more than twice in the film, and the second use gets a new framing.
- Upscale ≤ 2.35×, asserted in the assembler.
- Every cut sits in a VO pause.
- The pack carries `row_###.jpg` frames and the per-row sheet.

**Spend:** free Vertex only, with a £5 floor.
- **Omni Orbit beats:** two, both on starfield or ice starts, never a planet.
- **Veo Fast props:** two (a night road, a football pitch). These are everyday scenes, not planets. One take each.
- Everything else is £0.

**Sources:**
- **CODE** = `07_Edit-Project/code_graphics.py` (text-free; this commit).
- NASA is public domain.
- ESA and ESA/Gaia/DPAC are CC BY-SA 3.0 IGO.
- ESO and ESA/Hubble are CC BY 4.0. Credit them.
- **No DSS2 or Aladin cut-outs** (licence). No branded stock. No University of Rochester Scholz's-star art (copyright).

| # | Ch | VO in–out (s) | Dur | Source | Asset | Cuts | Notes |
|---:|---|---|---:|---|---|---:|---|
| 1 | 0 Open | 0.12–5.60 | 5.5 | ESA | ESA Gaia stellar-motion animation (DR2, 2018, "close encounters" or "stellar motions over the next 1.6 million years"), already moving | 1 | **Frame 0 lock.** Stars already streaming. No fade, no title, no Orbit. |
| 2 | 0 Open | 6.64–13.18 | 6.5 | ESA/CODE | The same Gaia animation, a second span, then `drift` (the orange star holds still) | 2 | "Heading almost straight at the Sun." |
| 3 | 0 Open | 14.14–17.20 | 3.1 | ESA | Gaia DR3 all-sky map, crop on Serpens Cauda (the Milky Way core side), slow push | 1 | "Its name is Gliese 710." No label, no marker. |
| 4 | 0 Open | 18.02–30.14 | 12.1 | CODE | `shower` 0–6 s (the star crossing the shell), then `shell` end frame | 2 | "Sail right through the outer edge." |
| 5 | 0 Open | 31.30–41.86 | 10.6 | CODE | Promise beat: `drift` → `path` → `sky` (about 3.5 s each) | 3 | One cut per promise. |
| 6 | 1 The Star Heading Our Way | 42.78–50.10 | 7.3 | ESO | ESO Milky Way time-lapse towards Sagittarius/Serpens, turning | 2 | 62 light-years, Serpens. |
| 7 | 1 The Star Heading Our Way | 51.04–57.54 | 6.5 | NASA | NASA SDO full Sun (visible light), then the NASA/ESA K-dwarf illustration (Hubble 2020 release) | 2 | "Smaller and cooler than the Sun." Keep it clearly an illustration. |
| 8 | 1 The Star Heading Our Way | 58.64–66.52 | 7.9 | OMNI | `orbit_binoculars_omni_v01`: Orbit on a hill at night sweeps the sky with binoculars, finds a faint orange dot, lowers them, and checks a calendar far too long to read | 2 | **ORBIT ACTS.** Start frame: Orbit on a dark hill under stars, **no planet in frame**. Vertex `global`, `orbit_shot=True`, one take. If it fails, `drift` holds. |
| 9 | 1 The Star Heading Our Way | 68.02–81.92 | 13.9 | CODE | `drift` (full 12 s, then hold the motion) | 3 | Sideways stars against one that stays put. Split by reframing (wide, then tighter on the orange star). |
| 10 | 1 The Star Heading Our Way | 83.00–93.64 | 10.6 | ESA | ESA Gaia close-encounter animation, a span not used in rows 1–2 | 2 | 14 km/s, almost none of it sideways. |
| 11 | 1 The Star Heading Our Way | 95.08–109.20 | 14.1 | VEO | `night_road_veo_v01`: a long straight empty road at night, one car's headlights coming straight at the camera and growing | 3 | **Not a planet, so Veo Fast is fine.** No brands, no plates, no text. Cut on "They just grow." |
| 12 | 1 The Star Heading Our Way | 110.32–126.04 | 15.7 | ESA/Hubble, ESA | ESA/Hubble Proxima Centauri (CC BY 4.0), slow push; then the Gaia stellar-motion animation | 3 | 026 callback, one line only. "Stars move." |
| 13 | 2 How Close Will It Come? | 126.90–133.84 | 6.9 | ESO | ESO star-trail time-lapse (a span not used elsewhere) | 2 | "Where it will be in a million years?" |
| 14 | 2 How Close Will It Come? | 134.58–146.98 | 12.4 | ESA/CODE | ESA Hipparcos spacecraft art, then `path` step 1 (the wide band, about 1 ly) | 3 | "The uncertainty was huge." |
| 15 | 2 How Close Will It Come? | 147.76–161.04 | 13.3 | ESA/CODE | ESA Gaia spacecraft art (ESA/ATG medialab), then `path` steps 2–3 | 3 | "The star kept coming closer." |
| 16 | 2 How Close Will It Come? | 162.06–174.80 | 12.7 | CODE | `path` final (thin band inside the 1-ly ring), hold, slow push | 2 | About a fifth of a light-year. |
| 17 | 2 How Close Will It Come? | 175.50–194.82 | 19.3 | CODE/NASA/VEO | `scale` 0–6 s → NASA Voyager 2 Neptune (PIA01492) → `scale` 6–12 s → `football_pitch_veo_v01` (an empty grass pitch at dusk, high wide angle, white lines only) | 4 | Neptune on "outermost planet"; the pitch on "football pitch". No crowds, no club colours. |
| 18 | 2 How Close Will It Come? | 195.68–203.76 | 8.1 | CODE | `shell` 0–5 s (close on the planet orbits) | 2 | "Something we have never seen." Stop before the shell shows; row 20 pays it off. |
| 19 | 2 How Close Will It Come? | 204.66–209.44 | 4.8 | CARD | Remotion subscribe card (house) | 1 |  |
| 20 | 3 Into the Oort Cloud | 210.34–223.68 | 13.3 | CODE | `shell` full pull-back | 3 | "Wrapped in a vast cloud of ice." |
| 21 | 3 Into the Oort Cloud | 224.70–232.84 | 8.1 | NASA | NASA Oort Cloud illustration (science.nasa.gov Oort Cloud page), slow push | 2 | "Nobody has ever seen it directly": keep it clearly an illustration. |
| 22 | 3 Into the Oort Cloud | 234.16–241.04 | 6.9 | NASA | NASA photo of Comet NEOWISE (C/2020 F3), July 2020 | 2 | A long-period comet, so it fits. |
| 23 | 3 Into the Oort Cloud | 241.88–249.84 | 8.0 | OMNI | `orbit_ice_omni_v01`: Orbit floats among slow dark lumps of ice, taps one gently, and watches it turn very slowly | 2 | **ORBIT ACTS.** Start frame: Orbit on a starfield with grey ice lumps, **no planet**. One take. If it fails, `shell` end frame holds. |
| 24 | 3 Into the Oort Cloud | 251.18–264.00 | 12.8 | NASA/CODE | NASA ISS orbital sunrise over Earth (sunlight arriving) → `shower` 0–6 s (the star entering the shell) | 3 | "Months to reach…" then "straight through the Oort Cloud." |
| 25 | 4 The Comet Shower | 264.86–280.58 | 15.7 | CODE | `shower` full 16 s | 3 | Marbles: the nudge, flung out, falling in. |
| 26 | 4 The Comet Shower | 281.74–293.52 | 11.8 | ESO/NASA | ESO Hale-Bopp 1997 (E. Slawik/ESO, CC BY 4.0), then NASA C/2023 A3 Tsuchinshan-ATLAS (ISS or NASA photo) | 3 | About ten a year, for millions of years. |
| 27 | 4 The Comet Shower | 294.48–315.46 | 21.0 | CODE/ESA | `shower` 9–16 s (the late infall trails), then the Gaia stellar-motion animation (a new span) with the star moving away | 4 | "Shrinking back into the dark." |
| 28 | 4 The Comet Shower | 316.62–335.00 | 18.4 | NASA/ESO | NASA Juno or Hubble Jupiter → NASA Cassini Saturn → ESO Hale-Bopp over a landscape (a new framing vs row 26) | 4 | **No impact or disaster imagery.** |
| 29 | 5 A New Brightest Star | 335.84–354.40 | 18.6 | ESO/CODE/NASA | ESO night-sky time-lapse → `sky` full → a NASA photo of Jupiter bright in a twilight sky (NASA/Bill Ingalls conjunction series) | 4 | The orange star outshines Sirius. |
| 30 | 5 A New Brightest Star | 355.42–363.52 | 8.1 | NASA | NASA full Moon (LRO or a NASA photo), then NASA SDO Sun limb (the second SDO framing, max 2) | 2 | "Billions of times fainter than our Sun." |
| 31 | 5 A New Brightest Star | 364.50–377.30 | 12.8 | CODE/NASA | `sky` (a tighter framing on the orange star) → the NASA full Moon again (a crop, second use) → `sky` fade | 3 | "Width of the full Moon every 35 years." |
| 32 | 6 It Has Happened Before | 378.30–386.78 | 8.5 | NASA | NASA WISE all-sky infrared map (NASA/JPL-Caltech/UCLA), slow push | 2 | WISE found Scholz's star. |
| 33 | 6 It Has Happened Before | 387.72–402.52 | 14.8 | NASA/CODE | NASA WISE spacecraft art → `traffic` 0–8 s (one dim red pair crossing the outer shell) | 3 | "Too small and too faint to stir up much." |
| 34 | 6 It Has Happened Before | 403.30–422.98 | 19.7 | ESA/CODE | Gaia DR3 all-sky map (the second use, a wide crop vs row 3's Serpens push) → `traffic` 8–16 s | 4 | HD 7977: "cannot yet pin down." |
| 35 | 6 It Has Happened Before | 423.76–434.78 | 11.0 | ESA | The Gaia stellar-motion animation, the opening span replayed wider | 2 | "One star among billions, all of them moving." |
| 36 | 6 It Has Happened Before | 436.86–444.72 | 7.9 | ESO | ESO night-sky time-lapse (the second use, a new angle) | 2 | "A slow traffic of stars." |
| 37 | 6 It Has Happened Before | 445.90–456.98 | 11.1 | NASA/ESA, CODE | A Hubble open star cluster (NASA/ESA; e.g. NGC 3603 or the Pleiades), then the `shell` end frame | 2 | The Sun's birth cluster: "Some astronomers think." |
| 38 | 6 It Has Happened Before | 457.96–469.34 (+hold) | 11.4 + 3.5 | NASA/ESA | NASA NEOWISE (the second use, a new crop) → **return to the opening Gaia stellar-motion footage**, hold 2–3 s past the last word, then fade | 3 | **VISUAL MUST return.** No Orbit and no goodbye card in the last shot. The end screen is added in Studio; the 029 handoff is a pickup later. |

## Code graphics (Claude, this commit)

`drift`, `path`, `scale`, `shell`, `shower`, `sky` and `traffic` are in `028/07_Edit-Project/code_graphics.py`. They're text-free, at 30 fps. Run `python3 code_graphics.py all <out>/`, with `--seconds N` to fit a row exactly (the Venus lesson: no freeze-padding). Stills were checked on 8 Oct.

## Generation queue (after the 027 picture; frame sheets for Claude PASS)

1. `orbit_binoculars_omni_v01` (row 8)
2. `orbit_ice_omni_v01` (row 23)
3. `night_road_veo_v01` (row 11) and `football_pitch_veo_v01` (row 17): Veo Fast, one take each

Orbit locks, as always: `orbit_shot=True`, a sidecar from `ORBIT_REF`, `global`.

## Harvest list (free, licence-checked; pool in `nasa_pool_v01.json` like 022/023)

- **ESA/Gaia:** the DR2 stellar-motion / close-encounters animation, the DR3 all-sky map, Gaia spacecraft art, Hipparcos art. Credit "ESA/Gaia/DPAC" (CC BY-SA 3.0 IGO).
- **ESA/Hubble:** the Proxima Centauri image (CC BY 4.0).
- **ESO:** night-sky and Milky Way time-lapses, Hale-Bopp 1997 (CC BY 4.0).
- **NASA:**
  - Sun and Moon: SDO Sun (max two uses: rows 7 and 30), an ISS orbital sunrise, LRO full Moon.
  - Planets: Voyager 2 Neptune PIA01492, a Juno/Hubble Jupiter, a Cassini Saturn, and a Jupiter-in-twilight photo.
  - Comets: NEOWISE 2020, C/2023 A3.
  - Oort Cloud illustration.
  - WISE: the all-sky map and spacecraft art.
  - The K-dwarf illustration.
  - A Hubble open cluster.
- **Before each one goes in, Cursor checks the title and licence**, so we don't repeat the Venus "parker" folder mix-up.
