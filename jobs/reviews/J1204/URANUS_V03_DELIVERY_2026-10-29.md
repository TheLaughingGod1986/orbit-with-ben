# J1204 Uranus v03 delivery + gate blocker — 29 Oct 2026

Worker: cursor. £0. No upload/swap/privacy/Buffer/UPLOADS. S5/S6 not built (delegated J1208).

## Ruling applied
`SOURCE_PLAN_RULING_2026-10-29.md`: S2-first VO; Shot4 artist-animation open; honest provenance; if truthful path FAILs a gate, return for resolution (do not rename metadata / alter thresholds).

## Built
| Item | Value |
|---|---|
| File | `00_Brand/…/06_Final-Exports/owb_sa_s4_uranus_v03.mp4` |
| SHA-256 | `87a6a091fc85e81fe453fca37ef0367ed63ceeb4234e58675290b63f70009ac3` |
| Duration | 18.0 s |
| VO | S2→S1→S3→S4 from `vo_v02` (`484a7d9e…`); first word **Uranus**; surprise **97** at ~1.18 s |
| Open | SVS 20390 Shot4 Beauty Pass, centre crop 608×1080→1080×1920, upscale **1.778×**; source open 1.15–3.85 s (forward-loop runway; continuous with tail 0.00–1.15) |
| Shot4 sha | `32370afa93cb69570ec05ee9abd1e9670171deb2ab33ceed6807d63dde716526` |
| Preserved v02 | `fd6bfec832bfa84d951c6e8ac2deff6c07ada71a9025e06deb2d8affc0b6f314` (untouched) |
| UAT | iCloud + NAS `OWB UAT/standalone_shorts_uranus_v03/` + `MANIFEST.sha256` |
| Frames | `jobs/reviews/J1204/uranus_v03_t0_0.00s.jpg`, `_t2_2.00s.jpg`, `_t_cut_2.70s.jpg` |
| Assembler | `_assemble_uranus_v03.py` |

Spoken: *Uranus is tipped 97 degrees, so it rolls on its side. This planet has winters that last 21 years. One orbit takes 84 years. For about a quarter of that, the sun stares down on one pole while the other half sits in the dark*

## Gate results (v03 as delivered)

| Gate | rc | Result |
|---|---|---|
| `gate_shorts_open` | **1 FAIL** | f0diff **0.36 < 1.50** (pushed still); loudness −14.6 (outside −14.5..−13.5); duration/tail_gap warns (same class as passing v02) |
| `sfx_kit level` | 0 | PASS |
| `polish_gate` | 0 | PASS |
| `music_gate` | 0 | PASS |
| `picture_qa` | 0 | PASS with WARNs (artist animation + pool title fields — see `…_picture_qa.txt`) |
| `finish_scan` loop | **1 FAIL** | `loop_diff_masked 2.51 > 2× open step 0.79` (open motion too small; 2× rule bites) |

## Blocker: Shot4 cannot clear FRAME0_DIFF_FAIL=1.50 honestly

Probed with `gate_shorts_open.frame0_diff_0_1_5s` on silent 2.7 s crops of Shot4:

| Source start | Speed | Crop height (upscale) | Gate f0diff |
|---|---|---|---|
| 0.00 | 1.0× | 1080 (1.778×) | **0.20** |
| 1.15 | 1.0× | 1080 (1.778×) | **0.34** |
| 4.50 | 1.0× | 1080 (1.778×) | **0.77** (best natural) |
| 4.50 | 1.0× | 817 (2.35× max) | **0.79** |
| 1.15 | 3.0× | 834 (2.30×) | **1.52** (only case ≥1.50; 3× time-compress) |

Natural Shot4 camera move tops out ~**0.8** on the gate’s own metric. Clearing 1.50 needs ~3× speed-up plus near-max upscale — that is not “existing moving footage” at truthful pace, and the ruling forbids synthetic band/ring motion, JPEG pans, stronger jitter, and altered thresholds as substitutes.

Loudness is a mix tweak only; **not** the stop. Loop FAIL is a consequence of the same low open step.

## Decision needed from Chief (no Ben card yet)

1. **Exception:** accept Shot4 artist-animation open with f0diff below 1.50 for this one Short (document as Chief OK / Never-list style exception for the 60% open gate), then worker re-mixes loudness and re-checks loop with that policy; or
2. **Authorize** a named motion assist on top of Shot4 (what kind, within Never list); or
3. **Reject Shot4** and require a different moving Uranus source that clears 1.50 at 1.0×; or
4. **Authorize** time-compression ≥3× (not recommended — distorts the Beauty Pass).

Assembler + v03 files + UAT copies stay as evidence. No swap of scheduled `ZpEA8stoSPA`. J1199 remains held.
