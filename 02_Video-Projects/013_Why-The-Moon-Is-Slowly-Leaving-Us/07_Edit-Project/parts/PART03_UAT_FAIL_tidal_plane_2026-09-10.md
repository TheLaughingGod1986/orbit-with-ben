# Part 03 UAT FAIL — nonsense tidal “water plane” plate

**Date:** 2026-09-10  
**Rough:** `OWB UAT/moon_leaving_part-03_rough_v01.mp4`  
**Verdict:** **FAIL** one (or more) tidal-bulge world plates. Do **not** lock Part 03 on this rough.

## What Ben saw

Still attached in chat / saved as UAT reject reference:

- Earth + Moon in space
- A **flat horizontal water sheet** cutting through the middle of the frame
- A dark water **dome / mound** rising from that sheet
- Earth looks **bisected** by the water plane (continent above, “submerged” below)

Reads as a broken composite / bad metaphor — **not** a readable Earth–Moon tidal bulge.

## Why it fails house

- Not VO-literal science picture: tidal bulge is an **ocean heap on Earth’s surface** ahead of the Moon, not a infinite water table floating in vacuum
- Env honesty break: ocean plane in vacuum with planets clipped through it
- Feels glitchy / pasted — premium CGI bar fail

## Likely culprits (regen candidates)

From `part-03_plates_v01.json` / tidal prompts — prefer regen these first:

| Stem / prompt | Why suspect |
|---------------|-------------|
| `p03_00` … exaggerated ocean tidal bulge | Open bulge setup |
| `p03_01` … bulge ahead of Moon | Torque/bulge beat |
| `p03_02` … oceans heaping into leading bulge | Same |
| `p03_06` … cross-section ocean layer + lunar pull | Cross-section often over-literalises into flat plane |

Also spot-check gallery/harvest/click plates used in the rough — any with the same water-plane look → quarantine.

## Regen lock (replacement prompt shape)

**Wanted:** whole Earth from space; oceans slightly **piled toward a leading bulge** on the globe’s surface; Moon beyond; continuous slow motion; silent CGI; no text; no people; no Orbit.

**Forbidden in prompt + reject if seen:**

- flat infinite water plane / table in space
- water cutting through planet interiors as a horizon sheet
- mirror twin Earth below a waterline
- cartoon “ocean floor in vacuum”

Example replacement prompt:

> Silent cinematic CGI. Whole Earth from deep space with realistic continents and clouds. Oceans on the globe surface are slightly exaggerated into a soft leading tidal bulge facing ahead of the Moon’s position. Moon beyond in clean vacuum. Continuous slow camera drift. No flat water plane in space. No cross-section table. No text. No people. No mascot. Premium documentary look.

## Next (Mac mini only)

1. Quarantine failing mp4(s) under `04_Generated-Clips/part03/_rejected_*`
2. Flow-mint replacement(s) with the lock above (x1)
3. Swap in `part-03_plates_v01.json`
4. Re-assemble `_assemble_part03_rough_v01.py` → new rough id if needed (`rough_v02`)
5. Copy to `OWB UAT/moon_leaving_part-03_rough_v02.mp4` (leave v01 for compare)
6. Do **not** remint Part 01 LOCKED v04 or Part 02 LOCKED v01

## Status

Part 03 rough **v01 is not UAT-pass**. Picture bug only — VO/music can stay.
