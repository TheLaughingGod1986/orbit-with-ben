# J1204 Uranus v05 delivery — 29 Oct 2026

Worker: cursor. £0. No upload/swap/privacy/Buffer/UPLOADS. S5/S6 not in this job (J1208).

## Ruling applied
Chief FIX reopen 16:15Z: different genuinely moving Uranus clip at 1.0×, ≤2.35×; probe f0diff≥1.50 before assemble. Gate thresholds unchanged. No motion assist / no 3×.

## Source selection (see `URANUS_V04_PROBE_2026-10-29.md`)
| Candidate | result |
|---|---|
| Shot4 Beauty Pass | reject — max natural f0diff ~0.8 |
| CloudBRoll / Shot18 | reject — clouds only, no disc+rings |
| Shot5 / AltVoyager | reject — f0diff ~0 |
| Shot16 fly by | v04 built — f0diff PASS but polish/picture near-black FAIL (tiny planet) |
| **Shot9 Beauty shot of Uranus' rings** | **selected** — silent probe f0diff 3.38 @ 4.00–6.70 s; mean 41.8 |

Source: https://svs.gsfc.nasa.gov/20390/ — NASA GSFC Conceptual Image Lab artist animation. sha `f964c7f1dd92c5626135f9915ba5d532a3114284cf24115fd393a9756249fb3e`. Upscale 1.778×.

## Built
| Item | Value |
|---|---|
| File | `…/06_Final-Exports/owb_sa_s4_uranus_v05.mp4` |
| SHA-256 | `6bcb32fa58635dc8574d6bc083c330587ae7867628e6f493d14958daf0c03cc4` |
| Duration | 18.0 s |
| VO | S2→S1→S3→S4; first word **Uranus**; surprise **97** |
| Open | Shot9 4.00–6.70 s; tail runway 2.85–4.00 s |
| Preserved | v02 `fd6bfec8…`, v03 `87a6a091…`, v04 `87cf21c4…` (pre-loudness) |
| UAT | iCloud + NAS `standalone_shorts_uranus_v05/` |

## Gates
| Gate | rc | note |
|---|---|---|
| gate_shorts_open | **0 PASS** | f0diff **3.41**; loudness −14.1 / TP −1.8 after remux; duration/tail_gap warns only (same 18 s class as prior SA Shorts) |
| sfx level | 0 | PASS |
| polish_gate | 0 | PASS |
| music_gate | 0 | PASS |
| picture_qa | 0 | PASS (artist-animation WARN path) |
| finish_scan loop | **1 FAIL** | `loop_diff_masked 7.45 > 2× open step 3.44` (threshold 6.88; over by **0.57**) |

## Ask Chief
1. Accept hairline loop FAIL (0.57 over) for this artist-animation open, or
2. Authorize v06 with earlier Shot9 window (2.00–4.70, silent f0diff 4.74) aiming for higher open step so 2× clears, or
3. Other.

No Ben card until PASS. No swap of scheduled `ZpEA8stoSPA`. J1199 remains held.
