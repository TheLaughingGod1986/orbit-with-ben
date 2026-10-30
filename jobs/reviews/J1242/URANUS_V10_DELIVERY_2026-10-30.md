# J1242 Uranus v10 delivery — 30 Oct 2026

Worker: cursor. £0. No upload / swap / privacy / Buffer / UPLOADS. J1212 and fallback `ZpEA8stoSPA` untouched.

Ruling answered: elected-Chief FIX on J1240 (motion-compensated open + precise path evidence). Worker does **not** PASS.

## Outcome: delivered, gates not clean (unsuccessful for ship)

Chief brief: park for elected-Chief review; if no compliant cut, report unsuccessful and preserve fallback. Assembler stop note: do not iterate Shot9 further after this delivery.

| Item | Result |
|---|---|
| Master sha256 | `7f6211546d85c930dd4e5db0a7cf6b0da1c3880d618f7c66ef2026e941037063` |
| NAS UAT | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/standalone_shorts_uranus_v10` (playable, sha match) |
| iCloud UAT | `…/OWB UAT/standalone_shorts_uranus_v10` (playable, sha match) — see `UAT_PLAYABLE.json` |
| Local export | `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/06_Final-Exports/owb_sa_s4_uranus_v10.mp4` |
| Assembler | `_assemble_uranus_v10.py` (MC warp-before-blend; DESIGN_PEAK 0.70 / FLOOR 0.50 / START 0.62; path-blend α=0.55) |

## What changed vs v09

- Open uses **motion-compensated** temporal samples (warp to align, then blend / shutter average). No unregistered crossfade of displaced frames.
- Source `px_per_odd` is **measured** (then ambiguous flow cleaned), not assumed 4 px.
- Soft floor through the cut (designed end ~0.50–0.70 px/frame) so no-freeze gate is not weakened.
- Upscale measured ≤1.85 (`measured_upscale` ≈1.849).
- Estimator synthetic fractional translations / ramps: **PASS** (`ESTIMATOR_SYNTHETIC.json`). Transform sign check: **PASS**.

## Motion (subject ROI 0:00–0:03) — corrected keys v06/v08/v09/v10

Full per-frame steps, step changes, confidence, ambiguous/unreliable flags, acceleration_rms, reliable_* and MC flicker: `MOTION_DIAGNOSTIC.json`. Summary: `MOTION_SUMMARY.json`.

| version | flicker_mad | reliable ymax | reliable dmax | unreliable |
|---|---:|---:|---:|---:|
| v06 | 3.587 | 5.5 | 2.3 | 47/80 |
| v08 | 3.370 | 4.0 | 1.5 | 46/80 |
| v09 | 2.093 | 2.7 | 2.4 | 5/80 |
| **v10** | **1.809** | **1.0** | **1.0** | **0/80** |

- Flicker improved vs v09 (~13.5% lower on the full master; prototype open alone was ~0.62).
- Reliable ymax **≤1.5 PASS**; reliable dmax **1.0 vs ≤0.25 FAIL** (honest; late-open residual / estimator hitch, not treated as compliance).
- Designed path peak 0.70 / design delta 0.015 (design curve itself within targets).

Evidence fix this run: full assemble had written v10 measurements under key `v09`. Remeasured all four masters; assembler key bug patched for any future run. No media re-encode of the master.

## Gates (all from sha `7f621154…`)

| Gate | rc | note |
|---|---|---|
| gate_shorts_open | **FAIL** | f0diff **1.40** &lt; 1.50 (“pushed still at frame 0”); duration/tail_gap warns unchanged from v09 band |
| finish_scan loop | **FAIL** | loop_diff_masked **4.18** &gt; 2× open_median_step **1.56** (v09 passed with step 2.39; absolute loop_diff ~same as v09’s 4.08 — relative threshold tightened by slower open) |
| hitch window | **PASS** | hitch_ok=True |
| polish_gate | PASS | 0 fail, 1 WARN look-at |
| picture_qa | PASS | 0 fail, 3 WARN look-at |
| music_gate | PASS | pace WARN 120 vs brief 84–96 |
| sfx level | PASS | |

## Inspection

Cursor automated only: ffmpeg frame extracts, contact strip, 0.25× open, before/after strip, hitch/loop metrics, estimator synthetics. **No claim of real-time audiovisual playback.**

Paths: `jobs/reviews/J1242/uranus_v10_*.jpg`, `uranus_v10_open_contact_0-3s.jpg`, `uranus_v10_open_0.25x.mp4`, `uranus_v10_open_before_after.jpg`.

## Explicit unsuccessful report

v10 is **not** a compliant ship cut under the existing final-sha gate set (open + loop FAIL). Fallback scheduled id `ZpEA8stoSPA` preserved. Do **not** repoint J1212 until elected Chief rules.

## Ask for elected Chief

1. Accept v10 as evidence-only FIX progress (flicker/ymax/unreliable improved) and decide next: further path/loop work, or keep v09 / fallback.
2. No worker PASS. No Ben-watch handoff from this worker.
3. Deadline still 1 Nov 20:00 London; Ben watch 3 Nov 10:30 London if a compliant cut is later OK’d.
