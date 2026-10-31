# J1307 — h41 graphics revision v04 for Chief review

Worker: codex · 31 October 2026 · £0. No VO, mint, upload or channel changes.
Status: **ready for Chief review; no worker PASS or merge.**
Revision on top of `7e6dcb51f`, branch `codex/j1307-graphics`.
Binding scope: Chief h41 in J1307 history. Spoken words unchanged.

## Delivery

Ten straight-RGBA PNG sequences, 1080×1920, 30 fps, 108 frames / 3.6 seconds each.
Timing remains parameterized by `--duration`, `--fps`, `--only` for assembly to fit measured VO.
Media is off git:

`/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/07_Edit-Project/graphics_j1307_v04/`

Each `code_graphic_<name>_v04/` contains frames and three previews.
`qa/all_stills.jpg` is the review sheet; `qa/still_review.mp4` is a diagnostic reel.
V02 and v03 media remain untouched. Their reports and evidence are preserved in
`graphics/verification/` and `graphics/verification_v03/`.
V04 manifests, frame hashes and raw QA are in `graphics/verification_v04/`.

## h41 changes and measured results

- **AR1 size:** `SCALE: 15-STOREY` / `BUILDING`, 88 px Arial Black, 100 px baseline spacing.
  The minimum transparent gap between stroked lines is **27 px**; clearance above artwork is **37 px**.
- **AR2 station:** `109 M` followed by the single 88 px line `(FOOTBALL FIELD)`.
  Minimum stroked-line gap is **16 px**; clearance above artwork is **49 px**.
- **AR3 Morocco:** tint is clipped at **27.67°N**. The source's Morocco polygon includes western Western Sahara,
  while its `W. Sahara` feature only covers the eastern portion; drawing that feature last alone did not solve it.
  Final base-map measurement: **0 tinted pixels south of 27.67°N**, 6,244 tinted pixels north of it.
  Base geography remains unchanged; only the Morocco tint is clipped.
- **AR3 Greatest Duration:** dot uses `ci == 5`, the exact same country index as EGYPT; first appears at frame 90.
- Other source geometry, labels, translucent shadow and the accumulated odds call-out remain as accepted in h41.

`verify_graphics.py` checks actual stroked alpha pixels on every frame of the two affected sequences:
expected number of separate lines, each line ≤980 px wide, transparent line gaps ≥8 px, artwork clearance ≥12 px.
It also asserts that Morocco tint exists and does not extend south of the clipping latitude.
Regression check against v03 rejects both broken layouts: size has merged lines; station has a 1 px gap.
The v04 check decoded all **1,080 frames**, confirming RGBA, dimensions, centre band, frame counts and animation.
All 30 stills were viewed on the sheet; the two fixed labels and Morocco map were inspected at full size.

## Raw picture QA and Chief's prior ruling

Unmodified `picture_qa.py`: **2 FAIL, 1 WARN**, exit 1 (preserved, not suppressed).

- AR1 odds samples 1 and 2: vertical gutter at 0.642. Both corresponding source-still columns (x=693)
  are uniform RGB **45,64,87**, standard deviation **0**: the diagnostic navy background only.
  **Chief h41 explicitly ruled the v03 backdrop-only gutters false positives and instructed recording that ruling if they recur.**
  These two unchanged odds findings are that same recurrence; raw results remain in the pack.
- AR3 date sample 0: low-detail WARN, edge density 0.0143 below p5 0.0157; unchanged.
- The station's two former gutter findings no longer occur.

No thresholds, sampling, exit codes or gate code were changed. The verifier propagates picture QA exit 1.
These are alpha assets: actual composites over moving plates still require assembly picture/polish QA.
The navy backdrop is diagnostic, not a film plate.

## Reproduce and handoff

```bash
/Users/benjaminoats/_desk/venv-graphics/bin/python graphics/render_graphics.py --out 07_Edit-Project/graphics_new_version --moon <NAS-pool>/moon/GSFC_20171208_Archive_e000868.jpg --duration 3.6 --fps 30
/Users/benjaminoats/_desk/venv-graphics/bin/python graphics/verify_graphics.py 07_Edit-Project/graphics_new_version --qa-script <repo>/scripts/picture_qa.py
```

Detached render `J1307-render-v04` completed, followed by corrected-map rerender `J1307-map-v04`.
Logs and `.done` receipts are in `_desk/logs/`; both receipts contain 1 because the raw picture QA findings are retained.
All rendering and delivery checks completed; no render remains active.
Mini repair preserved the branch and removed its old clean temporary worktree; this run used `/private/tmp/j1307-v04-wt`.
The NAS offload check found no eligible old scratch. No NAS file was changed or removed.

Next: Chief reviews v04 and decides acceptance. Assembly then fits approved assets to measured VO and reruns composite gates.
Nothing requires Ben for this worker task.
