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

## Result — rough v02 built 10 Sep 2026 (Mac mini)

Delivered: `OWB UAT/moon_leaving_part-03_rough_v02.mp4` (136.7 s, MD5 `0dd711c5e70511c52fbbe03ab0c5031a`). v01 left alongside. Parts 01/02 LOCKED untouched.

**Quarantined** (`04_Generated-Clips/part03/_rejected_tidal_plane_2026-09-10/`): the four named culprits `p03_00 / p03_01 / p03_02 / p03_06`, plus `p03_04` (Earth above a flat water horizon at frame 0) and `p03_gallery_07` (Moon sitting on a water plane mid-clip) found on the spot-check, plus `p03_00` take 1 of the regen (second Earth curve under the globe for ~3 s — twin Earth reject).
`_rejected_v02_sliced_planet_2026-09-10/`: `p03_05` (Saturn rings on the Moon), `p03_07` (Earth sliced by a lava seam), regen `p03_06` (lava cutaway table — the prompt's own forbidden look).

**Minted x1 in Google Flow** (new project `59f2b559-4391-48da-a01b-f75a2fd2ec95`, 720p/8 s), each QC'd first / mid / last frame: `p03_01` (bulge heaped on the sphere), `p03_02` (moonlit oceans, Moon beyond), `p03_04` (Moon with widening orbit rings), `p03_08` coral rings, `p03_09` shell cross-section, `p03_10` beach at dusk, `p03_11` translucent gears, `p03_12` orbital diagram, `p03_14` ocean → pull up to Moon. Contact sheets: `_uat_rejects/part03_v02_new_plates_sheet_{a,b}.jpg`; full v02 review: `_uat_rejects/part03_v02_review_sheet_2026-09-10.jpg`.

**Assembly change** (`_assemble_part03_rough_v02.py`): explicit cut list on VO paragraph gaps (silencedetect −35 dB) instead of blind 8 s beds; every bed is one unique plate at native speed (≤ 8 s in-point trim only — no freeze-pad, no loop, no slow-mo). Open = `p03_10` beach with the tide running under "the engine is still running under your feet". Map: `part-03_plates_v02.json`.

**Gen-tool notes.** The batch script's fresh-thumb capture races after a successful click (the next stem instantly "matches" the previous thumb → six renders left uncaptured and three saved under the wrong stem). `_harvest_part03_flow_project_v02.py` pulls every gallery render by thumb key so they can be identified by content. Also: `dev.orbit.live-longs-social` (every 5 min) sets the URL of Chrome's *active front tab* to Facebook via AppleScript and is failing every run ("Executing JavaScript through AppleScript is turned off") — it hijacked the Flow tab twice mid-batch; it was unloaded for the regen and reloaded after. Needs a fix or a pause before the next Flow session.

**Soft notes for Ben's watch** (not water-plane): beds 12–15 (79–109 s) are four consecutive Moon-over-stormy-sea plates (distinct files, similar look); `p03_14` opens on an odd splash object before it pulls up to the Moon. Swap if they bother you.

