# J1220 Uranus v07 delivery — 29 Oct 2026

Worker: cursor. £0. No upload/swap/privacy/Buffer/UPLOADS.

## Change
Ben on J1212 (OWB #264 6507250708): *0:00 the image is shaky*.
v07 keeps v06 VO/edit; stabilises Shot9 OPEN only
(velocity damp keep=0.50; tail zoom-only so loop seam matches v06). Still moving subject (rule 8).

## Stabilize
`{"zoom": 1.1285266457680252, "keep_motion": 0.5, "mean_step_x": -1.3375, "mean_step_y": -0.025, "residual_step_x": -0.66875, "residual_step_y": -0.0125, "peak_abs_corr_x": 53.50000000000007, "peak_abs_corr_y": 0.9999999999999984, "open_only": true, "open_start": 34, "tail_shift": 0.0}`

## Hashes
| Item | SHA-256 |
|---|---|
| `owb_sa_s4_uranus_v07.mp4` | `21dda9ab1c636c70678404ebd8c0d2d82e8f20af20bec3ae427483d2bf51e609` |
| source v06 | `f0b4e0a0318f99ecbe38cdcb0525c8f869fba609d55194da75de45cb579b3ee5` |
| `vo_v05.wav` | `f59211a87311baf6fa265d9b3f10972a46fdd43cbe3f4d5925a698870b310919` |
| Shot9 source | `f964c7f1dd92c5626135f9915ba5d532a3114284cf24115fd393a9756249fb3e` |
| preserved v06 | `f0b4e0a0318f99ecbe38cdcb0525c8f869fba609d55194da75de45cb579b3ee5` |

## Loudness (master, before PHONE/gates)
I=-14.30 LUFS, TP=-1.80 dBTP (band −14.5..−13.5 / ≤−1.6)

## Spoken (unchanged)
Uranus is tipped 97 degrees, so it rolls on its side. This planet has winters that last 21 years. One orbit takes 84 years. For about a quarter of that, the sun stares down on one pole while the other half sits in the dark

## Hitch window (timeline 0.30–0.55 s)
sha256=21dda9ab1c636c70678404ebd8c0d2d82e8f20af20bec3ae427483d2bf51e609
open_median_step=7.2374
t=0.30s step=8.5105
t=0.33s step=8.5286
t=0.37s step=8.6253
t=0.40s step=9.0228
t=0.43s step=4.9588
t=0.47s step=8.5965
t=0.50s step=10.3531
t=0.55s step=8.3409
hitch_window_ok=True (none <0.35 or >2× median)


## Gates (all from sha `21dda9ab1c636c70678404ebd8c0d2d82e8f20af20bec3ae427483d2bf51e609`)
| Gate | rc | note |
|---|---|---|
| gate_shorts_open | 0 | see `…_gate.txt` |
| sfx level | 0 | |
| polish_gate | 0 | |
| music_gate | 0 | |
| picture_qa | 0 | |
| finish_scan loop | 0 | PASS loop_diff_masked 8.63 open_median_step 7.24 head_matches [0, 0, 0, 0, 0] |

## Evidence
- Before/after strip: `/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/06_Final-Exports/owb_sa_s4_uranus_v07_open_before_after.jpg` and `jobs/reviews/J1220/uranus_v07_open_before_after.jpg`
- Full-size frames: `jobs/reviews/J1220/uranus_v07_t*.jpg`
- UAT: `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/standalone_shorts_uranus_v07` and `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/standalone_shorts_uranus_v07` with MANIFEST.sha256

Park for Chief (Claude): re-point J1212 awaits_ben to v07. No upload.
