# J1204 Uranus v06 delivery — 29 Oct 2026

Worker: cursor. £0. No upload/swap/privacy/Buffer/UPLOADS.

## Ruling applied
`URANUS_V05_CHIEF_RULING_2026-10-29.md`: same Shot9, odd-phase from 60fps frame 53;
open 2.0167–4.7167 s / tail 0.8833–2.0167 s; loudness first; gates from final sha.

## Hashes
| Item | SHA-256 |
|---|---|
| `owb_sa_s4_uranus_v06.mp4` | `f0b4e0a0318f99ecbe38cdcb0525c8f869fba609d55194da75de45cb579b3ee5` |
| `vo_v05.wav` | `f59211a87311baf6fa265d9b3f10972a46fdd43cbe3f4d5925a698870b310919` |
| parent `vo_v02.wav` | `484a7d9ead015de266f6eb9937b6f6b9b5e8e9ec7c1b0124750ecea77f5410df` |
| Shot9 source | `f964c7f1dd92c5626135f9915ba5d532a3114284cf24115fd393a9756249fb3e` |
| preserved v05 | `6bcb32fa58635dc8574d6bc083c330587ae7867628e6f493d14958daf0c03cc4` |
| preserved rejected v02 | `fd6bfec832bfa84d951c6e8ac2deff6c07ada71a9025e06deb2d8affc0b6f314` |

## Loudness (master, before PHONE/gates)
I=-14.30 LUFS, TP=-1.80 dBTP (band −14.5..−13.5 / ≤−1.6)

## Spoken (S2-first, reused)
Uranus is tipped 97 degrees, so it rolls on its side. This planet has winters that last 21 years. One orbit takes 84 years. For about a quarter of that, the sun stares down on one pole while the other half sits in the dark

## Odd-phase
60fps indices 53..281 step 2 (n=115); all odd.

## Hitch window (timeline 0.30–0.55 s)
sha256=f0b4e0a0318f99ecbe38cdcb0525c8f869fba609d55194da75de45cb579b3ee5
open_median_step=6.2358
t=0.30s step=6.3869
t=0.33s step=6.5471
t=0.37s step=5.9254
t=0.40s step=7.0109
t=0.43s step=3.0388
t=0.47s step=6.2508
t=0.50s step=8.5269
t=0.55s step=6.4878
hitch_window_ok=True (none <0.35 or >2× median)


## Gates (all from sha `f0b4e0a0318f99ecbe38cdcb0525c8f869fba609d55194da75de45cb579b3ee5`)
| Gate | rc | note |
|---|---|---|
| gate_shorts_open | 0 | see `…_gate.txt` |
| sfx level | 0 | |
| polish_gate | 0 | |
| music_gate | 0 | |
| picture_qa | 0 | open/tail distinct source ids; title+1.778× in pool; artist WARN expected |
| finish_scan loop | 0 | PASS loop_diff_masked 8.28 open_median_step 6.24 head_matches [0, 0, 0, 0, 0] |

## Provenance
- Open/tail: Beauty shot of Uranus' rings (Shot9), NASA SVS 20390, Conceptual Image Lab artist animation
- Open source in/out: 2.0167–4.7167 s; tail 0.8833–2.0167 s
- Measured upscale: 1.778× (≤2.35)
- Full-size frames: `jobs/reviews/J1204/uranus_v06_t*.jpg` (+ hitch 0.33/0.40/0.47)
- UAT: `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/standalone_shorts_uranus_v06` and `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/standalone_shorts_uranus_v06` with MANIFEST.sha256

Parked for Chief cut review. No Ben card until PASS. If any gate FAIL: no further Shot9 windows (ruling stop rule).

## picture_qa recheck (metadata only, master sha unchanged)
PASS after distinct open/tail source ids (same as v05 pattern). Master sha untouched.
