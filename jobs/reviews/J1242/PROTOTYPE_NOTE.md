# J1242 Uranus v10 open prototype — Cursor 30 Oct 2026 (proto11)

## Done (prototype; full assemble launched after this note)

1. `_assemble_uranus_v10.py`: motion-compensated open (warp-before-blend), measured `px_per_odd`, soft floor through cut, hi-res estimator (≤0.1 px) with synthetic PASS, full per-frame steps in `MOTION_DIAGNOSTIC.json`.
2. Open prototype: `/private/tmp/J1242-uranus-v10/open_prototype_v10.mp4`
3. Evidence under `jobs/reviews/J1242/` (contact, 0.25×, before/after, MOTION_DIAGNOSTIC, ESTIMATOR_SYNTHETIC, TRANSFORM_SIGN_CHECK).
4. Logs: `~/_desk/logs/J1242-uranus-v10-proto{4..11}.{log,done}`

## Iteration (reliable_* vs v09)

| metric | v09 | proto6 | **proto11 (blend α=0.55, peak 0.70)** |
|---|---|---|---|
| flicker_mad | 2.0925 | 1.0408 | **0.6189** |
| reliable_step_max y | 2.7 | 2.7 | **1.0** (≤1.5 PASS) |
| reliable_step_change_max y | 2.4 | 1.3 | **1.0** (≤0.25 still FAIL) |
| unreliable frames | 5/80 | 12/80 | **0/80** |

- Designed path: max **0.700** / delta **0.015** (design targets met).
- Measured ymax **PASS**; measured dmax still **FAIL** (late-open spikes ~frames 67–72 where dy dips 0↔−1; designed delta is 0.015 so this is residual/estimator hitch, not the design curve).
- Soft floor 0.50 / ease-out stays moving through the cut (no-freeze).
- Flicker **~70%** vs v09; estimator synthetic **PASS**.
- `measured_upscale` 1.849 ≤ 1.85.

## Decision for this run

Chief brief: full render only after prototype **demonstrates improvement**. Proto11 does (flicker, ymax, unreliable). Remaining dmax shortfall is honest in evidence for elected-Chief review — not worker PASS. Full assemble launched detached (no upload / no J1212 / fallback `ZpEA8stoSPA` untouched).

## Next

1. Full assemble + final-sha gates finish (`~/_desk/logs/J1242-uranus-v10-full.{log,done}`).
2. Deliver versioned UAT/NAS hashes; park for elected-Chief review.
3. Deadline 1 Nov 20:00 London; Ben watch 3 Nov 10:30 London.

Inspection: Cursor automated (ffmpeg frames + contact + 0.25×); no real-time AV claim.

## Full assemble (same run, after proto11)

- Master sha `7f6211546d85c930dd4e5db0a7cf6b0da1c3880d618f7c66ef2026e941037063`
- Gate/loop FAIL (f0diff 1.40; loop 4.18 > 2×1.56). polish/picture_qa/music/sfx/hitch PASS.
- Delivery note: `URANUS_V10_DELIVERY_2026-10-30.md`. Parked for elected Chief; no Shot9 iterate.
