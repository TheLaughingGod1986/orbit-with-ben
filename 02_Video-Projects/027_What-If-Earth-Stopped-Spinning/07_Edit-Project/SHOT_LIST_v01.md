# 027 What If Earth Stopped Spinning? SHOT_LIST v01 (Claude, 8 Oct 2026)

Timed to `02_Voiceover/stt/earth_spin_vo_v01/stt_raw.json` (VO `earth_spin_vo_v01`, 460.38 s; VO PASS 6002694271; text files in a413bbe). Times are sentence spans from Scribe, and the chapter gaps are 0.7 s (`chapters_index.json`). Each row is a beat. **`cuts` is the number of 4–6 s cuts to split it into.** After the cut, check every row with `align_shot_list.py` and `clip_check.py`.

**Venus lessons, applied from the start** (the EPIC/ISS opening footage appears at rows 1, 15 and 37; 37 is the deliberate return):
- No still more than twice in the film, and the second use gets a new framing.
- Upscale ≤ 2.35×, asserted in the assembler.
- Every cut sits in a VO pause.
- The pack carries `row_###.jpg` frames and the per-row sheet.
- Every harvested item gets its **title and licence checked** before it enters the pool.

**Spend:** free Vertex only, with a £5 floor.
- **Omni Orbit beats:** two (the North Pole spin, the hilltop sunset). Neither has a planet in frame.
- **Veo Fast props:** two (a smooth-airliner cabin pour, a phone at midnight). Everyday scenes, one take each.
- Everything else is £0.

**Sources:**
- **CODE** = `07_Edit-Project/code_graphics.py` (text-free; this commit).
- NASA, NOAA, USGS and NIST are US government, public domain.
- The Met Museum and Smithsonian Open Access are CC0.
- Wikimedia Commons files only if CC BY or CC BY-SA, credited by name.
- ESA/Hubble and ESO are CC BY 4.0.
- **No disaster footage, no damaged cities, no branded airline or phone.**

| # | Ch | VO in–out (s) | Dur | Source | Asset | Cuts | Notes |
|---:|---|---|---:|---|---|---:|---|
| 1 | 0 Open | 0.16–8.82 | 8.7 | NASA | NASA DSCOVR EPIC time-lapse of Earth turning, or the ISS terminator time-lapse, already moving | 2 | **Frame 0 lock.** The day-night line visibly moves by 1 s. No fade, no title, no Orbit. |
| 2 | 0 Open | 9.76–16.02 | 6.3 | NASA | NASA airborne-science jet at cruise (DC-8 or ER-2, NASA Armstrong), then the ISS night-city pass over Europe | 2 | "Faster than a jet airliner." No airline livery. |
| 3 | 0 Open | 17.36–22.56 | 5.2 | CODE | `speed` (the globe turning, arrows growing) | 1 | "What would happen if Earth stopped spinning?" |
| 4 | 0 Open | 23.80–39.50 | 15.7 | CODE | Promise beat: `speed` → `air` → `oceans` → `clock` (about 4 s each) | 4 | One cut per promise. |
| 5 | 1 The Speed You Cannot Feel | 40.38–50.72 | 10.3 | VEO | `cabin_pour_veo_v01`: a drink poured steadily in a calm airliner cabin, window light, no logos | 2 | "Pour a drink without spilling a drop." |
| 6 | 1 The Speed You Cannot Feel | 51.32–62.70 | 11.4 | NASA | ISS time-lapse of an orbital sunrise over Earth's limb | 2 | "The Sun does not rise. Your side of Earth turns towards it." |
| 7 | 1 The Speed You Cannot Feel | 63.32–72.20 | 8.9 | ESO | ESO star-trail or night-sky time-lapse turning | 2 | "Stars wheel across the sky." |
| 8 | 1 The Speed You Cannot Feel | 72.98–90.24 | 17.3 | CODE/NASA | `speed` (a tighter framing) → `bulge` → a NASA Blue Marble limb | 4 | Half a percent; 43 km wider. |
| 9 | 1 The Speed You Cannot Feel | 90.86–111.08 | 20.2 | Commons/PD | Real Foucault pendulum footage (the Panthéon or a museum pendulum knocking over pegs; CC BY or CC BY-SA, credited), then a public-domain portrait of Léon Foucault | 4 | **VISUAL MUST.** "The floor was." |
| 10 | 2 The Sudden Stop | 111.92–120.28 | 8.4 | CODE | `air` 0–8 s (the globe stops; the air keeps going) | 2 | "But the air does not." |
| 11 | 2 The Sudden Stop | 121.06–132.84 | 11.8 | CODE/NOAA | `air` 8–14 s → NOAA or NASA footage of high cirrus streaming (jet-stream clouds from the ISS) | 2 | Faster than sound. No storm damage. |
| 12 | 2 The Sudden Stop | 133.70–142.52 | 8.8 | NOAA | NOAA public-domain B-roll of wind-driven sea spray on a rocky coast | 2 | **VISUAL MUST.** Spray, not destruction. |
| 13 | 2 The Sudden Stop | 143.12–154.28 | 11.2 | NASA/CODE | ISS night pass over Britain → `speed` with London's gold arrow held | 2 | "Lurch forwards when a bus brakes" is spoken only. |
| 14 | 2 The Sudden Stop | 155.24–166.32 | 11.1 | OMNI | `orbit_northpole_omni_v01`: Orbit stands on Arctic sea ice, turns slowly on the spot once as if testing the idea, then shrugs, unbothered | 2 | **ORBIT ACTS.** Start frame: Orbit on Arctic ice under a pale sky, **no globe in frame**. Vertex `global`, `orbit_shot=True`, one take. If it fails, `speed` with the pole arrow at zero holds. |
| 15 | 2 The Sudden Stop | 167.16–181.46 | 14.3 | NASA | NASA SDO full Sun → the DSCOVR EPIC full Earth (a new framing vs row 1) | 3 | "No brake"; 40,000 years of sunlight. |
| 16 | 2 The Sudden Stop | 182.42–186.94 | 4.5 | CARD | Remotion subscribe card (house) | 1 |  |
| 17 | 2 The Sudden Stop | 187.84–192.02 | 4.2 | CODE | `oceans` start frame | 1 | Bridge: "What about a slow one?" |
| 18 | 3 A Slow Stop | 192.84–211.78 | 18.9 | CODE/NASA | `bulge` (a second framing) → NASA Blue Marble oceans → `oceans` 0–6 s | 4 | "The water would drain away towards the poles." |
| 19 | 3 A Slow Stop | 212.52–220.72 | 8.2 | CODE | `oceans` 6–12 s (the band of land) | 2 | Frączek's model, schematic. |
| 20 | 3 A Slow Stop | 221.96–236.24 | 14.3 | CODE | `dayyear` | 3 | One day = one year. |
| 21 | 3 A Slow Stop | 237.30–247.06 | 9.8 | OMNI | `orbit_sunset_omni_v01`: Orbit sits on a hilltop watching a sunset that never quite ends, checks a tiny pocket watch, puzzled, and settles in to wait | 2 | **ORBIT ACTS.** Start frame: Orbit on a grassy hilltop, low Sun, **no planet in frame**. One take. If it fails, `dayyear` holds. |
| 22 | 3 A Slow Stop | 248.76–265.04 | 16.3 | NASA | NASA Magellan Venus global view (S91-50688 or PIA00271; a Venus 023 plate, credited), then the Mariner 10 / Akatsuki cloud Venus (PIA23791) | 3 | One-line callback to 023. **No Orbit on the Venus plates.** |
| 23 | 4 Earth Is Already Slowing | 265.90–274.52 | 8.6 | NASA/NOAA | NASA LRO full Moon → NOAA tide footage (a harbour at high and low tide, time-lapse) | 2 | "Raises the tides." |
| 24 | 4 Earth Is Already Slowing | 275.10–287.20 | 12.1 | CODE | `tides` 0–12 s | 3 | Hand on a spinning wheel: spoken only. |
| 25 | 4 Earth Is Already Slowing | 287.98–306.42 | 18.4 | CODE/NASA | `tides` 12–14 s (the Moon backing away) → the NASA Apollo laser-ranging retroreflector (AS11-40-5952) | 4 | 3.8 cm a year; a callback to the Moon film 013. |
| 26 | 4 Earth Is Already Slowing | 307.52–322.28 | 14.8 | NASA | NASA LRO near side, then the LRO far side (two plates, one use each) | 3 | "It did not stop spinning. It got locked." |
| 27 | 4 Earth Is Already Slowing | 323.28–334.00 | 10.7 | Met CC0 | A Met Museum Open Access cuneiform tablet (CC0), slow push; then a NASA total-eclipse photo (2017 or 2024) | 2 | **VISUAL MUST:** a real clay tablet. Pick a tablet whose catalogue entry says astronomical if one is CC0; otherwise a plain tablet with the caption kept generic. |
| 28 | 4 Earth Is Already Slowing | 334.66–351.22 | 16.6 | NASA | NASA eclipse-path map animation (SVS: the 2024 path sweeping across North America) | 3 | "Seen from places hundreds or thousands of kilometres away." Text-free span. |
| 29 | 4 Earth Is Already Slowing | 352.16–368.82 | 16.7 | USGS/Smithsonian | A USGS or Smithsonian Open Access fossil coral (CC0/PD), growth lines visible, slow push; then a second coral plate | 3 | **VISUAL MUST.** |
| 30 | 4 Earth Is Already Slowing | 369.70–373.42 | 3.7 | CODE | `clock` (22 ticks → 24) | 1 | About 22 hours long. |
| 31 | 5 Keeping Score | 374.30–378.06 | 3.8 | VEO | `phone_midnight_veo_v01`: a phone face-up on a bedside table at night, the screen glowing, **no readable digits or logos** | 1 | "Your phone does." |
| 32 | 5 Keeping Score | 379.14–389.14 | 10.0 | NIST | NIST-F2 caesium fountain clock photo (NIST, public domain), then a NIST lab plate | 2 | **VISUAL MUST.** Atomic clocks. |
| 33 | 5 Keeping Score | 389.62–402.74 | 13.1 | CODE/NASA | `clock` (a tighter framing; one extra tick flashes) → the ISS orbital sunrise (a new span vs row 6) | 3 | 27 leap seconds since 1972. |
| 34 | 5 Keeping Score | 403.46–416.06 | 12.6 | NASA | NASA cutaway of Earth's interior (molten core art) → a NASA Greenland ice-sheet melt photo (Operation IceBridge) | 3 | "Running a touch fast." No disaster framing. |
| 35 | 5 Keeping Score | 416.88–437.84 | 21.0 | NASA/CODE | NASA SDO Sun (a second framing) → `tides` (a slow Moon pass) → `speed` (a wide framing, arrows steady) | 4 | "Never stop spinning", "within a blink". |
| 36 | 5 Keeping Score | 439.12–448.56 | 9.4 | ESO | ESO night-sky time-lapse (a second span vs row 7) | 2 | The bigger question. |
| 37 | 5 Keeping Score | 449.30–460.34 (+hold) | 11.0 + 3 | NASA | NASA art of the young Earth or the Moon-forming impact, then **return to the opening EPIC/ISS Earth, still turning, the day line still sweeping**. Hold 2–3 s past the last word, then fade | 3 | **VISUAL MUST return.** No goodbye card and no Orbit in the last shot. The end screen is added in Studio; the 028 handoff ("Next week: a star is coming into our solar system.") is a pickup later. |

## Code graphics (Claude, this commit)

`speed`, `bulge`, `air`, `oceans`, `dayyear`, `tides` and `clock` are in `027/07_Edit-Project/code_graphics.py`. They're text-free, at 30 fps, and their stills were checked on 8 Oct. Use `--seconds N` to fit a row exactly, rather than freeze-padding.

## Generation queue (after the 026 picture; frame sheets for Claude PASS)

1. `orbit_northpole_omni_v01` (row 14)
2. `orbit_sunset_omni_v01` (row 21)
3. `cabin_pour_veo_v01` (row 5) and `phone_midnight_veo_v01` (row 31): Veo Fast, one take each, no text, no brands

Orbit locks, as always: `orbit_shot=True`, a sidecar from `ORBIT_REF`, `global`.

## Shorts

The three Shorts (Mon 23 / Wed 25 / Fri 27 Nov) take their plates from this list. Their scripts and VO are in `10_Shorts/EARTH_SPIN_SHORTS_SCRIPTS_v01.md`. Shorts rows get drafted for Claude's review when the long's picture starts, like 026.
