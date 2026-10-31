# J1307 — AR1–AR3 code graphics for Chief review

Worker: codex · 31 October 2026 · £0. No VO, mint, upload or channel changes.
Status: built and verified; parked for Chief. This is not a creative PASS or film-stage approval.
Binding brief: J1307 and CHIEF_H37_CORRECTIONS.md. No spoken words changed.

## Delivery

Ten straight-RGBA PNG sequences, 1080×1920, 30 fps, 108 frames / 3.6 seconds each.
All durations are **provisional**, configurable with `--duration` (and `--only` per graphic).
Media is off git in:

`/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/07_Edit-Project/graphics_j1307_v02/`

Each `code_graphic_<name>_v02/` holds `frame_%05d.png` plus three preview PNGs.
`qa/all_stills.jpg` shows the 30 inspected samples; `qa/still_review.mp4` is the diagnostic still reel.
The delivered transparency has no background on cards, comparisons or the Moon diagram.
Maps use our own equirectangular ocean/land base. Content is confined to y=656..1264.
Typeface: Arial Black, 96 px / 69 px cap height (11.35% of the 608 px band), white with dark stroke.
Cards appear sequentially, one label at a time. They do not show all clauses simultaneously.

| Sequence name | Content |
|---|---|
| ar1_date | 22 DEC 2032 |
| ar1_odds | 4.3% (JUNE 2025), then → 0% (WEBB, FEB 2026) |
| ar1_size | 60 M rock width compared with illustrative 15-storey building silhouette |
| ar1_miss | Real NASA Moon disc; surface-to-arc bracket 21,200 KM |
| ar2_dates | RETIRES 2030; DEORBIT BURN ~2031; DECISION 2027 |
| ar2_station | Schematic station silhouette, 109 M bracket, then (FOOTBALL FIELD) |
| ar2_nemo | South Pacific map, Point Nemo target ring, EMPTY SOUTH PACIFIC |
| ar3_path | NASA northern/southern limits and centre line; six sequential country labels; greatest-duration marker |
| ar3_dates | 2 AUG 2027; 258 KM PATH; LONGEST: 6M23S, EGYPT |
| ar3_duration | Common-zero duration bars: 2026 ECLIPSE: 2M 18S; 2027 EGYPT: 6M 23S |

## Geometry and sources

- Eclipse: `graphics/SE2027Aug02Tpath.txt` is the NASA table; `eclipse_path.json` preserves 103 complete rows as longitude/latitude. The incomplete 11:48 row has no northern limit and is omitted from the parsed data, beyond the displayed Atlantic-to-Red-Sea region. Plot uses all three lines, not a guessed thick centre-line stroke. Source: https://eclipse.gsfc.nasa.gov/SEpath/SEpath2001/SE2027Aug02Tpath.html (Fred Espenak, NASA/GSFC). Projection bounds: 48°W–45°E, 12°N–55°N. The rendered band is animated progressively; timing is illustrative, not real-time shadow speed.
- Greatest Duration: solid yellow marker at 26°49′N, 031°08′E, per h37. The small hollow country marker is geographic context, not an eclipse maximum. Countries appear Spain → Morocco → Algeria → Tunisia → Libya → Egypt. No Luxor attribution.
- Basemap: own Pillow polygons from Natural Earth 1:110m public-domain geographic data. Source URL and credit embedded in `countries.json`; data downloaded from Natural Earth's maintainer repository. Boundaries/coastlines are illustrative, not navigation. No source map image or diagram was imported.
- Point Nemo: 48°53′S, 123°24′W, per job; South Pacific bounds 205°W–65°W, 72°S–7°N. This locates the region around Point Nemo; it does not promise an exact final ISS impact point. No Bahamas or city-lights plate.
- Moon: NASA/GSFC `GSFC_20171208_Archive_e000868.jpg`, read from the brief's NAS pool; source SHA-256 in manifest. Moon radius = 30 px = 1,737 km; surface separation = 30×21,200/1,737 = 366.1485 px. Closest centre-to-arc distance = 396.1485 px. Arc is an explanatory flyby, not a calculated asteroid ephemeris or closed orbit. The asteroid marker is symbolic, not size-scaled. Real lunar texture is clipped to a circular disc.
- Duration bars: 138 and 383 seconds, identical pixel scale, ratio 383/138 = 2.77536 (2.78× rounded). The labels are sequential to keep one label on screen.
- Rock/building: 300 px rock width and 300 px illustrative building height at completed reveal, 15 storeys at an illustrative 4 m/storey. This is the approved analogy, not a claim about all buildings. Station is a schematic silhouette with an overall 109 m bracket, not a detailed NASA 3D reconstruction.

## Checks and review limits

`verify_graphics.py` decoded all 1,080 delivery PNGs: RGBA, 1080×1920, exact centre-band bounds, expected frame counts, animation present, no identical-frame hold over 4 seconds. Per-file hashes are in `graphics/verification/SHA256SUMS.txt`. Source data and Moon geometry were checked against the brief and NASA table.

Automated still-review result (not Chief approval):

```
picture QA PASS: 0 of 30 cuts fail, 1 to look at
Delivery geometry/alpha/count checks succeeded: 10 sequences
```

The remaining WARN is AR3's `2 AUG 2027` card: low edge density relative to the other samples. Chief must look at it at full size. All 30 samples were visually inspected by the worker for clipping, geography, labels and layout; the full-size warning frame is included in the review sheet.

The original v01 diagnostic found grid-line seam flags on both maps and a low-detail flag at the exact fully transparent odds-card transition. v02 removes the map grid entirely. The v02 representative still is sampled at 60%, instead of exactly the 50% card handover. This does **not** remove the transparent transition from the delivery: the underlying moving plate must remain visible through it. The original QA report is retained. No gate override or reviewed-ok exemption was used.

The QA reel crops the centre band and composites over neutral navy **for inspection only**. It is not a film plate. Pixel/jitter/near-black/reuse checks on the real final composites remain required in assembly. No final VO timing has been assumed or approved.

Chief review needs: visual style/diagram acceptance, the sparse date-card WARN, and country-label readability at the final measured duration (six labels in the provisional 3.6 s map is brisk). The greatest-duration marker is identified here rather than by a second simultaneous on-screen label. Assemble each card and graphic only on its corresponding spoken line; exclude frame 0–2 s and the title interval; never stack the map labels and date cards. Split/re-time these parameterized pieces as needed and run the final Short gates. Do not treat this asset pack as a finished Short.

## Reproduce

Requires Python 3, Pillow, NumPy (Moon crop), ffmpeg and the macOS Arial Black font.
Run from the audit directory, with a **new** output directory (existing frame sequences are refused):

```bash
python3 graphics/render_graphics.py --out 07_Edit-Project/graphics_new_version --moon <NAS-pool>/moon/GSFC_20171208_Archive_e000868.jpg --duration 3.6 --fps 30
python3 graphics/verify_graphics.py 07_Edit-Project/graphics_new_version --qa-script <repo>/scripts/picture_qa.py
```

Use `--only ar3_path` (or another sequence name) to render one duration separately. Longer timings must still satisfy the four-second static-hold check. Preview-only mode: `--stills-only`.
Completed detached render: tmux `J1307-render-v02` exited; `_desk/logs/J1307-render-v02.done` = 0; log beside it. No active render needs resuming.

Disk: required NAS offload attempted first; no eligible old scratch existed. v02 pack is about 118 MB. No NAS file deleted or altered.

Next: Chief reviews this pack and accepts or requests revisions; assembly measures timing from VO. Nothing needed from Ben for this worker job.
