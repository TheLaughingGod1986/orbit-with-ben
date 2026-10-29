# J1225 Uranus v08 delivery — 29 Oct 2026

Worker: cursor. £0. No upload/swap/privacy/Buffer/UPLOADS.

## Change
Acting Chief FIX on J1220: v07 constant-mean damp did not fix Ben's *0:00 shaky* request
(OWB #264 6507250708). v08 keeps v06 VO/edit; Shot9 OPEN uses measured path vs
Gaussian-smoothed path (HF residual cancelled; intentional motion kept). Tail
zoom-only for loop seam. First render failed loop (`loop_diff_masked 14.14`) because
Gaussian smooth pulled `corr[open_start]` off zero vs tail shift 0; re-render subtracts
that seam anchor (HF cancel unchanged). measured_upscale = centre-crop × stab zoom.
Rule 8 holds. Worker inspected 0:00–0:03 frames + normal-speed open clip; Chief judges
whether Ben's shake request is met (output HF ≈ v06, far below v07).

## Stabilize
`{"method": "path_vs_smooth", "smooth_sigma": 5.0, "zoom": 1.0431407200308267, "crop_upscale": 1.7777777777777777, "measured_upscale": 1.854472391165914, "mean_step_x": 0.0, "mean_step_y": -3.95, "path_std_x": 0.0, "path_std_y": 93.39515066946389, "hf_rms_x": 0.0, "hf_rms_y": 1.868800873578633, "peak_abs_corr_x": 0.0, "peak_abs_corr_y": 14.332546673049006, "seam_anchor_x": 0.0, "seam_anchor_y": 7.2714273684625645, "open_only": true, "open_start": 34, "tail_shift": 0.0}`

## Motion (subject ROI 0:00-0:03)
`{
  "v06": {
    "label": "v06",
    "sha256": "f0b4e0a0318f99ecbe38cdcb0525c8f869fba609d55194da75de45cb579b3ee5",
    "method": "adjacent frame phase correlation, Hann-windowed subject ROI x200:900 y600:1400, 540x960 decode; shifts at full 1080 width",
    "mean": [
      0.0,
      -3.4
    ],
    "std": [
      0.0,
      1.4628738838327793
    ],
    "acceleration_rms": [
      0.0,
      0.6364458273405841
    ]
  },
  "v07": {
    "label": "v07",
    "sha256": "21dda9ab1c636c70678404ebd8c0d2d82e8f20af20bec3ae427483d2bf51e609",
    "method": "adjacent frame phase correlation, Hann-windowed subject ROI x200:900 y600:1400, 540x960 decode; shifts at full 1080 width",
    "mean": [
      -1.25,
      -2.7
    ],
    "std": [
      1.0185774393731681,
      2.812472222085046
    ],
    "acceleration_rms": [
      1.312066685554424,
      3.903909108715766
    ]
  },
  "v08": {
    "label": "v08",
    "sha256": "9888a2398282c2384290a09eb59a418f36c9960cf6d80036f2cad1cfb634bcf7",
    "method": "adjacent frame phase correlation, Hann-windowed subject ROI x200:900 y600:1400, 540x960 decode; shifts at full 1080 width",
    "mean": [
      0.0,
      -3.325
    ],
    "std": [
      0.0,
      1.4471955638406304
    ],
    "acceleration_rms": [
      0.0,
      0.6750527405556144
    ]
  },
  "note": "Translation variation measures jitter; average drift alone does not measure shake."
}`

## Hashes
| Item | SHA-256 |
|---|---|
| `owb_sa_s4_uranus_v08.mp4` | `9888a2398282c2384290a09eb59a418f36c9960cf6d80036f2cad1cfb634bcf7` |
| source v06 | `f0b4e0a0318f99ecbe38cdcb0525c8f869fba609d55194da75de45cb579b3ee5` |
| source v07 | `21dda9ab1c636c70678404ebd8c0d2d82e8f20af20bec3ae427483d2bf51e609` |
| `vo_v05.wav` | `f59211a87311baf6fa265d9b3f10972a46fdd43cbe3f4d5925a698870b310919` |
| Shot9 source | `f964c7f1dd92c5626135f9915ba5d532a3114284cf24115fd393a9756249fb3e` |
| preserved v06 | `f0b4e0a0318f99ecbe38cdcb0525c8f869fba609d55194da75de45cb579b3ee5` |
| preserved v07 | `21dda9ab1c636c70678404ebd8c0d2d82e8f20af20bec3ae427483d2bf51e609` |

## Loudness (master, before PHONE/gates)
I=-14.30 LUFS, TP=-1.80 dBTP (band −14.5..−13.5 / ≤−1.6)

## Spoken (unchanged)
Uranus is tipped 97 degrees, so it rolls on its side. This planet has winters that last 21 years. One orbit takes 84 years. For about a quarter of that, the sun stares down on one pole while the other half sits in the dark

## Hitch window (timeline 0.30–0.55 s)
sha256=9888a2398282c2384290a09eb59a418f36c9960cf6d80036f2cad1cfb634bcf7
open_median_step=6.0486
t=0.30s step=6.0968
t=0.33s step=6.4274
t=0.37s step=5.9936
t=0.40s step=7.0626
t=0.43s step=5.0051
t=0.47s step=6.2487
t=0.50s step=7.2411
t=0.55s step=6.6082
hitch_window_ok=True (none <0.35 or >2× median)


## Gates (all from sha `9888a2398282c2384290a09eb59a418f36c9960cf6d80036f2cad1cfb634bcf7`)
| Gate | rc | note |
|---|---|---|
| gate_shorts_open | 0 | see `…_gate.txt` |
| sfx level | 0 | |
| polish_gate | 0 | |
| music_gate | 0 | |
| picture_qa | 0 | |
| finish_scan loop | 0 | PASS loop_diff_masked 8.45 open_median_step 6.05 head_matches [0, 0, 0, 0, 0] |

## Evidence
- Before/after strip: `/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/06_Final-Exports/owb_sa_s4_uranus_v08_open_before_after.jpg` and `jobs/reviews/J1225/uranus_v08_open_before_after.jpg`
- Full-size frames: `jobs/reviews/J1225/uranus_v08_t*.jpg`
- UAT: `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/standalone_shorts_uranus_v08` and `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/standalone_shorts_uranus_v08` with MANIFEST.sha256
- Motion: `jobs/reviews/J1225/MOTION_DIAGNOSTIC.json`
- Transform sign check: `jobs/reviews/J1225/TRANSFORM_SIGN_CHECK.json`
- UAT playable: `jobs/reviews/J1225/UAT_PLAYABLE.json`

Park for elected Chief: do NOT repoint J1212 until Chief PASS on v08. No upload.
