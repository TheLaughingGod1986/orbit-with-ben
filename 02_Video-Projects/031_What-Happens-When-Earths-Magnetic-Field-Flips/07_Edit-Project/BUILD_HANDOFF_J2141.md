# J2141 resumable picture build — 4 Nov 2026

Worker: codex. Spend: £0. **Partial work, no KEEP, no Chief PASS, no film stage approval.**

## Landed in this worker branch

- `harvest_picture_v01.py`: resumable NASA API download and hash/evidence recorder.
- `HARVEST_POOL_v01.json`: four downloaded candidates with original API metadata, credits, file hashes, dimensions and individual pending rights/review states. Media and contact sheet live in the shared 031 `07_Edit-Project/harvest_v01/`, outside git. Not the complete licensed harvest.
- `code_graphics.py cards`: all three WHO and six FACT overlays named in SHOT_LIST_v02. Each gets a unique row-specific transparent 1920×1080/25 fps qtrle MOV; no baked black slab. Animation in/out: 0.4 s. WHO durations: 3.6 s. Labels and biography years follow the approved shot list/SOURCES row 19. Source-row links and exact Scribe cue starts are in `CODE_CARDS_v01.json`.
- `CODE_CARDS_TECHNICAL_CHECK_v01.json`: all nine hashes match, alpha format is argb, dimensions and durations match, and full ffmpeg decode completes without errors. These are encoding checks only. Static preview sheet/full-size WHO frame inspected; no claim to hearing audio or seeing moving video.
- Outputs live under shared 031 `07_Edit-Project/code_cards_v01/`; no media committed.

## Exact resume state

Queue plan remains **1/3**: brief/input review finished; build still partial; full package verification not started. Preserve that denominator. No other queue job taken.

Detached render was `tmux J2141-cards`, using `/private/tmp/J2141-render-cards.sh`. It **finished, exit 0**. Logs: `/Users/benjaminoats/_desk/logs/J2141-cards.log`, completion: `/Users/benjaminoats/_desk/logs/J2141-cards.done`. Do not mistake the completed nine-card batch for all graphics being complete.

Reproduce cards from this branch:

```sh
python3 02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/code_graphics.py cards --out <persistent-media-dir> --manifest <new-manifest-path>
```

## Observed issues for Chief/editor

1. NASA API ID verification contradicts R54's asset descriptions. **PIA20016 = Peering Through Titan Haze**, infrared composite, not natural-colour Titan beside Saturn. **PIA14909 = Titan Up Front**, true-colour Titan in front of Saturn/rings, not an isolated haze-limb photograph. Both are downloaded candidates, not admitted shots. Resolve R54 explicitly; no silent substitution. NASA metadata and the contact sheet preserve the evidence.
2. NASA institutional hosting alone is not a blanket per-asset licence. The two Titan credits include universities/Space Science Institute; their rights remain pending. Blue Marble texture also remains a candidate. PIA00407 credits NASA/JPL/USGS; its use is subject to NASA media conditions. Keep third-party rights checks open.
3. The shot list calls sourced simulations/maps “real” separators (e.g. R13, R15, R16, R18, R23/24, R39/47). AGENTS picture QA still forbids sourced simulations/maps/labelled graphics. Rule-E GO is recorded, but this job does not explicitly waive that gate. Chief needs to reconcile these rows before admission; do not turn a sourced map into an accepted code graphic by relabelling it.
4. R35's literal cue leaves only **1.24 s** inside its row. Its FACT card needs readability/timing review on the actual composite. Other FACT durations: R6 2.44 s, R14 1.92 s, R19 1.96 s, R27 3.6 s, R45 3.4 s. Do not mark legibility from encoding metrics.
5. The nine overlays require graded moving/blurred real plates. They have not been composited; near-black, subject clearance, timing fit and motion QA remain open. Preview backgrounds are transparent, not intended black picture.

## Work still unfinished

- Wider NASA/SVS, NOAA/NCEI, USGS/USFWS, ESA/DTU and Commons harvest, per-file terms/attribution verification, candidate inspection, interval/crop assignment, reuse tally and complete contact sheet. No active search budget was consumed on these unsearched missing inputs; do not repeatedly revisit the rejected Titan interpretation.
- Mechanisms: poledrift, flip, compass, timeline, grains, matuyama_map, strata, layers, dynamo, barcode, strength, belts, hubble_saa, sat_safe, saa, triptych, paleo, rings, multipole, column, mars_vs_earth, extinction_check, grid_shield, poles_map, aurora, generations. `code_graphics.py` intentionally exposes only the implemented cards mode; it does not fake unsupported modes.
- £0 R21 compass and R41 NASA atmosphere fallbacks; no OMNI or paid generation attempted.
- Full row renders, cue/composite review, actual motion-capable review and applicable picture/polish gates. The film has not been assembled.

Disk: NAS offload ran with elevated filesystem access before building; **nothing in /private/tmp was old enough**. Free space remained ~12.6 GB, so this run used a small media batch (~18 MB of cards), not a large scratch render. Restore headroom before larger work; never delete/overwrite NAS assets.

Next worker continues J2141 from this branch/PR. Chief decides the asset/gate conflicts; no Ben action requested by this partial handoff.
