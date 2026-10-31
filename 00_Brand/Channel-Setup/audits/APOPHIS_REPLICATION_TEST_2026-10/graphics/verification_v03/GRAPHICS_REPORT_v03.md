# J1307 — h38 graphics revision v03 for Chief review

Worker: codex · 31 October 2026 · £0. No VO, mint, upload or channel changes.
Status: **parked for Chief; picture QA has unresolved findings. No PASS.**
This revision is on top of `1faade493`, branch `codex/j1307-graphics`.
Binding instructions: Chief h38 in J1307 history, following h37. Spoken words unchanged.

## Delivery

Ten straight-RGBA PNG sequences, 1080×1920, 30 fps, 108 frames / 3.6 seconds each.
Durations remain provisional parameters (`--duration`, `--fps`, `--only`).
Media is off git under:

`/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/07_Edit-Project/graphics_j1307_v03/`

Each `code_graphic_<name>_v03/` contains frames and three previews.
`qa/all_stills.jpg` is the review sheet; `qa/still_review.mp4` is the diagnostic reel.
v02 is preserved. Its report and evidence are in `graphics/verification/`.
Current manifests, frame hashes and QA evidence are in `graphics/verification_v03/`.

## Six requested changes

1. **AR3 path:** shadow is alpha-composited at 140/255 (54.9%) over the map. Coastlines and borders remain visible. Northern/southern limits and centre line remain.
2. **AR3 countries:** removed all hollow country dots. The named Natural Earth polygon is tinted while its label is displayed, in Spain → Morocco → Algeria → Tunisia → Libya → Egypt order.
3. **AR3 Greatest Duration:** the only dot appears at 26°49′N, 031°08′E only when q ≥ 5/6, under EGYPT. It is absent during LIBYA.
4. **AR1 odds:** `4.3% (JUNE 2025)` stays on screen as `→ 0% (WEBB, FEB 2026)` builds below it. No fully transparent internal handover. The verifier checks first-line visibility on every interior frame.
5. **AR2 station:** `109 M` stays above `(FOOTBALL FIELD)`, with the parenthetical wrapped across two lines. One accumulated call-out, no orphaned replacement.
6. **AR1 size:** the second label is `SCALE: 15-STOREY BUILDING`, wrapped across three lines. Each line stays within 980 px. The same 96 px house font is retained; compact line spacing keeps the label above the silhouettes.

Other source geometry and numbers are unchanged from the accepted v02: NASA path rows; Moon radius 1,737 km and surface miss 21,200 km; Point Nemo; equal-scale duration bars. Source files remain in `graphics/`. All content stays inside y=656..1264.

## Verification and unresolved findings

`verify_graphics.py` decoded all 1,080 frames: correct RGBA dimensions, band bounds, frame counts, animation and no static hold over four seconds. The persistent odds-line check succeeds. All 30 representative stills were inspected on the sheet; the Egypt map and accumulated odds card were also inspected at full size.

The unmodified `picture_qa.py` reports **4 FAIL and 1 WARN** on the neutral-navy diagnostic reel:

- AR1 odds samples 1 and 2: vertical gutter at 0.642.
- AR2 station samples 1 and 2: horizontal gutter at 0.833.
- AR3 date sample 0: low detail, edge density 0.0143 below film p5 0.0157.

These findings are retained verbatim, with no exemption, threshold change or sampling adjustment. The reviewed images show the requested accumulated text and station schematic; Chief must adjudicate the findings or request another revision. These are alpha assets, so the actual moving-plate composites must also run through picture/polish QA during assembly. The neutral background is diagnostic only, not a film plate.

The verifier now invokes picture QA with its own Python interpreter and propagates its nonzero exit status; it cannot report a successful command exit when picture QA fails.

## Reproduce

Use the existing Pillow/NumPy environment, ffmpeg and macOS Arial Black:

```bash
/Users/benjaminoats/_desk/venv-graphics/bin/python graphics/render_graphics.py --out 07_Edit-Project/graphics_new_version --moon <NAS-pool>/moon/GSFC_20171208_Archive_e000868.jpg --duration 3.6 --fps 30
/Users/benjaminoats/_desk/venv-graphics/bin/python graphics/verify_graphics.py 07_Edit-Project/graphics_new_version --qa-script <repo>/scripts/picture_qa.py
```

Completed detached render: `J1307-render-v03`; `_desk/logs/J1307-render-v03.done` = 0. No render remains active.
Required NAS offload found no eligible old scratch; no NAS file was changed or removed.

Next: Chief reviews v03 and the four diagnostic FAILs. Assembly fits approved assets to measured VO and reruns final composite gates. Nothing requires Ben for this worker task.
