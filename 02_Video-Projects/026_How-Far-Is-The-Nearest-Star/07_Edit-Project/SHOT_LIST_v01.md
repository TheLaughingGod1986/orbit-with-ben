# 026 How Far Is the Nearest Star? SHOT_LIST v01 (Claude, 5 Oct 2026)

Timed to `02_Voiceover/words.json` (VO `nearest_star_vo_v01`, 491.02 s, Claude VO PASS `c7ced8c`). Times are sentence spans from Scribe; chapter gaps are 0.7 s. Each row is a beat. **`cuts` is the number of 4–6 s cuts to split it into.** Check every row with `align_shot_list.py` after the cut.

**Spend:** free Vertex only, with a £5 floor.
- Two Omni Orbit beats, both on starfield starts, never a planet.
- Three Veo Fast props (grapefruit, pin, cherry). These are everyday objects, not planets, so the drift problem doesn't apply. One take each.
- Everything else is £0.

**Sources:** CODE = `07_Edit-Project/code_graphics.py` (text-free). ESO and ESA/Hubble are CC BY 4.0, credit them. ESA Gaia is CC BY-SA 3.0 IGO. NASA is public domain. The Tycho and Bessel portraits are public-domain paintings. **No Breakthrough artwork, no branded stock.**

| # | Ch | VO in–out (s) | Dur | Source | Asset | Cuts | Notes |
|---:|---|---|---:|---|---|---:|---|
| 1 | 0 Open | 0.08–7.44 | 7.4 | ESO | ESO night-sky time-lapse, already turning (CC BY 4.0, credit ESO) | 1 | **Frame 0 lock.** Already moving. No fade, no title, no Orbit. |
| 2 | 0 Open | 8.54–13.18 | 4.6 | ESO | ESO Milky Way time-lapse, a second angle | 1 |  |
| 3 | 0 Open | 13.90–19.34 | 5.4 | ESA/Hubble | Hubble image of Proxima Centauri (ESA/Hubble & NASA, CC BY 4.0), slow push | 1 | Small and red. "You cannot see that star at all." |
| 4 | 0 Open | 20.88–32.70 | 11.8 | CODE | `triple` → `parallax` → `journey` (about 4 s each) | 3 | Promise beat: one cut per promise. |
| 5 | 1 The Star You Cannot See | 33.54–49.24 | 15.7 | ESA/Hubble | Hubble Proxima, tighter crop | 2 | Red dwarf. |
| 6 | 1 The Star You Cannot See | 50.14–63.20 | 13.1 | NASA/ESA | NASA SDO full Sun, then Hubble Proxima (cut, no split) | 2 | Less than 1% of the Sun's light; outlives it. |
| 7 | 1 The Star You Cannot See | 64.30–87.80 | 23.5 | ESO | ESO/DSS2 Alpha Centauri wide field, then ESO southern-sky time-lapse with Alpha Cen bright | 3 | "From Britain, they never rise": hold on the southern sky. |
| 8 | 1 The Star You Cannot See | 88.88–107.74 | 18.9 | CODE | `triple` | 2 | Proxima looping slowly round the bright pair. |
| 9 | 1 The Star You Cannot See | 108.90–121.32 | 12.4 | CODE | `journey` light-only pass (a single photon streak, Proxima → Earth) | 2 | A light-year is a distance. |
| 10 | 2 Measuring the Gap | 122.14–127.22 | 5.1 | ESO | ESO starfield still, slow push | 1 |  |
| 11 | 2 Measuring the Gap | 128.10–143.36 | 15.3 | OMNI | `orbit_thumb_omni_v01`: Orbit holds up one small hand, closes one eye then the other, and watches a near star jump | 2 | **ORBIT ACTS.** Start frame: Orbit composited on a **starfield** (no planet). Vertex `global`, `orbit_shot=True`, one take. If it fails, `parallax` holds. |
| 12 | 2 Measuring the Gap | 144.36–166.12 | 21.8 | CODE | `parallax` | 4 | Earth at January, then July; the near star shifts against fixed background stars. |
| 13 | 2 Measuring the Gap | 167.18–181.08 | 13.9 | PD art | Portrait of Tycho Brahe (public domain painting) + ESO starfield | 2 | "Proof that Earth must stand still." |
| 14 | 2 Measuring the Gap | 182.32–204.46 | 22.1 | PD art/ESO | Portrait of Friedrich Bessel (public domain), then 61 Cygni field (ESO/DSS2) | 3 | The coin at 13 km is spoken only, not drawn. |
| 15 | 2 Measuring the Gap | 205.78–223.84 | 18.1 | ESA | ESA Gaia spacecraft art, then the Gaia all-sky map (CC BY-SA 3.0 IGO, credit ESA/Gaia/DPAC) | 3 |  |
| 16 | 2 Measuring the Gap | 224.94–231.08 | 6.1 | CARD | Remotion subscribe card (house) | 1 |  |
| 17 | 3 Shrink It Down | 232.96–239.06 | 6.1 | CODE | `starfield`-style empty field (reuse 024 `starfield` at β 0) | 1 | Bridge. |
| 18 | 3 Shrink It Down | 239.90–249.56 | 9.7 | VEO | `grapefruit_table_veo_v01` (a grapefruit on a plain wooden table, slow push); `pin_room_veo_v01` (a pin standing far across a long room) | 2 | **Not a planet, so Veo Fast is fine.** Free Vertex, one take each, no text, no hands, no brands. |
| 19 | 3 Shrink It Down | 250.48–262.78 | 12.3 | NASA | NASA Blue Marble, then NASA LRO Moon | 2 | "Every person… sits on that pin." |
| 20 | 3 Shrink It Down | 263.86–276.92 | 13.1 | VEO/NASA | `cherry_table_veo_v01`, then a NASA Blue Marble pull-back over Europe and North Africa with two glow dots (London, Cairo) added in Remotion, no text | 3 | 4,000 km. Dots only, no labels. |
| 21 | 3 Shrink It Down | 277.80–295.40 | 17.6 | ESO/CODE | ESO Alpha Centauri, then an empty starfield | 3 | "Between them, almost nothing." |
| 22 | 3 Shrink It Down | 296.40–311.36 | 15.0 | NASA | NASA Voyager 1 art, then the 1977 launch (NASA archive, muted) | 3 | "Barely left the town." |
| 23 | 4 The Walk | 312.28–314.40 | 2.1 | CODE | `journey` start frame | 1 |  |
| 24 | 4 The Walk | 315.26–336.16 | 20.9 | OMNI/CODE | `orbit_walk_omni_v01`: Orbit sets off with great determination, drifts forwards, looks back at how little he's covered, laughs; then `journey` walking/car/jet markers | 4 | **ORBIT ACTS.** Start frame: Orbit composited on a **starfield** with no planet in frame. One take. |
| 25 | 4 The Walk | 336.98–354.26 | 17.3 | NASA/CODE | NASA Voyager art, then `journey` Voyager marker | 2 | "It is not heading towards Proxima." |
| 26 | 4 The Walk | 355.22–361.44 | 6.2 | CODE | `journey` light streak | 1 |  |
| 27 | 4 The Walk | 362.16–378.10 | 15.9 | CODE | `lighttimes` | 3 | Moon, Sun, Proxima: three bars on a log scale, lit in turn, text-free. |
| 28 | 5 Is Anyone There? | 378.98–395.96 | 17.0 | ESO | ESO artist's impression of Proxima b (ESO/M. Kornmesser, CC BY 4.0). Keep it clearly an impression | 3 | Earth-mass, 11-day orbit. |
| 29 | 5 Is Anyone There? | 396.84–403.18 | 6.3 | ESO | A second ESO Proxima b impression (dry surface) | 2 | "Do not picture a second Earth yet." |
| 30 | 5 Is Anyone There? | 403.98–421.20 | 17.2 | NRAO/NASA | NRAO/AUI/NSF illustration of the 2019 Proxima flare (CC BY), then NASA SDO flare footage as a "what a flare looks like" reference | 3 | Flares; atmosphere may be stripped. |
| 31 | 5 Is Anyone There? | 421.90–441.56 | 19.7 | NASA | NASA solar-sail art (ACS3) as a generic light-pushed sail | 3 | **No Breakthrough artwork.** |
| 32 | 5 Is Anyone There? | 442.70–456.94 | 14.2 | NASA | NASA Deep Space Network dish (Goldstone or Canberra) | 2 | 2031 / 2035. |
| 33 | 5 Is Anyone There? | 457.86–490.96 | 33.1 | ESO | Return to the opening: ESO night-sky time-lapse, still turning | 3 | **VISUAL MUST return.** No Orbit, no goodbye card. The end screen is added in Studio; the 027 handoff is a pickup later. |

## Code graphics (Claude, this commit)

`parallax`, `triple`, `journey`, `lighttimes` are in `026/07_Edit-Project/code_graphics.py`. The empty starfield reuses 024's `starfield`.

## Generation queue (after the 025 picture; frame sheets for Claude PASS)

1. `orbit_thumb_omni_v01` (row 11)
2. `orbit_walk_omni_v01` (row 24)
3. `grapefruit_table_veo_v01`, `pin_room_veo_v01`, `cherry_table_veo_v01` (rows 18 and 20): Veo Fast, one take each

Orbit locks as always: `orbit_shot=True`, a sidecar from `ORBIT_REF`, `global`.

## Shorts (VO PASS+LOCK `5994626502`; LOCK = untrimmed `_raw`) — Chief draft, **Claude PASS with edits 5 Oct 2026** (edits marked *Claude*)

House: no Orbit at frame 0; `gate_shorts_open.py` must pass; 22–27 s total with ~2 s loop hold; exact title on screen 9–14 s; last ~3 s loop to open. Timings below are **scaled to LOCK duration** from the trimmed `words.json` on main (Mon/Fri pause-trim was later turned OFF). Re-run Scribe on each `*_vo_v01_LOCK.wav` and `align_shot_list.py` before picture. Shorts reuse long plates; Veo props shared with the long.

### Mon 16 Nov — You Can't See the Nearest Star (LOCK 24.48 s)

| # | VO in–out (s) | Dur | Source | Asset | Notes |
|---:|---|---:|---|---|---|
| S1 | 0.12–5.60 | 5.5 | ESO | ESO night-sky time-lapse already turning (same as long row 1). Caption: **TOO FAINT**. | **Frame 0.** No Orbit. Whoosh. |
| S2 | 6.12–11.04 | 4.9 | ESA/Hubble / OMNI | Hubble Proxima (long row 3/5) slow push; optional Orbit peek. | *Claude:* Orbit only as the script says: peering through a tiny telescope. That means one new Omni take (`orbit_shot=True`, `global`, free credit) or stay on the sky. Never reuse a clip whose action doesn't match the line. |
| S3 | 11.50–20.14 | 8.6 | ESA/Hubble / CODE | Hubble Proxima tighter ("less than one percent of the Sun's light"), then the `journey` **light lane** crossing on "more than four years". Exact title on screen 9–14 s. | *Claude:* `journey` light lane, not `triple`, because the line is about light time. Reuse long plates. |
| S4 | 20.64–24.44 | 3.8 | ESO | Return to opening night-sky time-lapse. | Loop. Spoken end names the long. |

### Wed 18 Nov — Could a Robot Reach the Nearest Star? (LOCK 21.60 s)

| # | VO in–out (s) | Dur | Source | Asset | Notes |
|---:|---|---:|---|---|---|
| S1 | 0.14–3.62 | 3.5 | NASA | Voyager 1 art already moving against stars (long row 22/25). Caption: **75,000 YEARS**. | **Frame 0.** No Orbit. Whoosh. |
| S2 | 4.42–6.96 | 2.5 | NASA | 1977 Voyager launch archive (muted), long row 22. | |
| S3 | 8.02–18.26 | 10.2 | NASA / CODE | Voyager against deep starfield + `journey` Voyager marker. Exact title 9–14 s. | No Orbit needed (script). |
| S4 | 18.86–21.52 | 2.7 | NASA | Return to opening Voyager pass. | Loop. |

### Fri 20 Nov — If the Sun Were a Grapefruit, Where's the Nearest Star? (LOCK 20.64 s)

| # | VO in–out (s) | Dur | Source | Asset | Notes |
|---:|---|---:|---|---|---|
| S1 | 0.11–2.75 | 2.6 | VEO | `grapefruit_table_veo_v01` (long row 18), camera already sliding. Caption: **A CHERRY**. | **Frame 0.** No Orbit. Whoosh. |
| S2 | 3.30–8.39 | 5.1 | VEO | `pin_room_veo_v01` then `cherry_table_veo_v01` (long rows 18/20). | One take each, free Vertex. |
| S3 | 8.87–16.67 | 7.8 | NASA / Remotion | Blue Marble → London–Cairo glow-dot pull-back (long row 20). Exact title 9–14 s. | Dots only, no labels. *Claude:* code/Remotion over NASA imagery only. Never a Veo/Omni take started from a whole-Earth frame (planet drift). |
| S4 | 17.17–20.54 | 3.4 | VEO | Return to opening grapefruit slide. | Loop. |

## Shorts generation notes
- *Claude:* **Length.** Each file is 22–27 s including the loop hold, so Fri (VO 20.64 s) needs a hold of at least 1.4 s and Wed (21.60 s) at least 0.4 s. Aim for about 2 s on all three.
- *Claude:* **R3 (lessons §6).** Run `gate_shorts_open.py check … --last 10` on all three opens. Mon's night-sky open must not match the last 10 Shorts' frame 0.
- Mon may reuse `orbit_thumb_omni_v01` only after the long's Omni queue; otherwise stay on ESO/Hubble.
- Fri Veo props are the same three as the long (no remint).
- Wed is NASA-only.
