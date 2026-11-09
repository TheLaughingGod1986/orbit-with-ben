# J1240 Uranus v09 delivery — 30 Oct 2026

Worker: cursor. £0. No upload/swap/privacy/Buffer/UPLOADS.

## Change
Acting Chief FIX on J1225: v08 still matched v06 shake (MOTION_DIAGNOSTIC). Ben's
*0:00 the image is shaky* (#264 6507250708). v09 keeps v06 VO/edit; Shot9 OPEN is
slow-eased (≤1.5 px/frame, ease-in/out, no dead stop) with sub-pixel resample and
180° shutter motion blur. Tail zoom-only for loop seam. measured_upscale ≤ 1.85.
Rule 8 holds. Tail last-8 frames ease toward open[0] so loop_diff
stays inside the 2× open-step band after the slow retiming (seam MAD
7.81 → 2.35). Designed step-change max 0.074 px; measured phase-corr
step_change_max 3.0 still beats v06's 4.0; flicker 2.76 beats 3.20.

## Stabilize
`{"method": "slow_ease_open_retiming_motion_blur", "max_step_px": 1.5, "max_step_delta": 0.25, "motion_blur_n": 3, "open_src_span_odd": 40, "zoom": 1.04, "crop_upscale": 1.7777777777777777, "measured_upscale": 1.8488888888888888, "designed_step_mean": -1.3975000000000004, "designed_step_max_abs": 1.5, "designed_step_change_max_abs": 0.07381468757064624, "open_only": true, "open_start": 34, "tail_shift": 0.0, "src_off_first_last": [0.0, 27.950000000000006], "seam_mad_before": 7.811653137207031, "seam_mad_after": 2.3453407287597656, "seam_alpha": 0.6927666963899406, "seam_target": 2.4000000000000004}`

## Motion (subject ROI 0:00-0:03)
`{
  "v06": {
    "label": "v06",
    "sha256": "f0b4e0a0318f99ecbe38cdcb0525c8f869fba609d55194da75de45cb579b3ee5",
    "method": "sub-pixel phase correlation (2\u00d7 upsample) on subject ROI x180:900 y776:1144 at full 1080x1920; flicker = MAD after motion compensation",
    "mean": [
      0.0,
      -3.3625
    ],
    "std": [
      0.0,
      1.459826616417169
    ],
    "acceleration_rms": [
      0.0,
      0.6935507611039354
    ],
    "step_change_max": [
      0.0,
      4.0
    ],
    "step_max_abs": [
      0.0,
      6.0
    ],
    "flicker_mad": 3.197769767045975
  },
  "v08": {
    "label": "v08",
    "sha256": "9888a2398282c2384290a09eb59a418f36c9960cf6d80036f2cad1cfb634bcf7",
    "method": "sub-pixel phase correlation (2\u00d7 upsample) on subject ROI x180:900 y776:1144 at full 1080x1920; flicker = MAD after motion compensation",
    "mean": [
      -0.025,
      -3.225
    ],
    "std": [
      0.22220486043288945,
      1.6276900810658022
    ],
    "acceleration_rms": [
      0.31822291367029204,
      1.0673521004472302
    ],
    "step_change_max": [
      2.0,
      6.0
    ],
    "step_max_abs": [
      2.0,
      5.0
    ],
    "flicker_mad": 3.112805376946926
  },
  "v09": {
    "label": "v09",
    "sha256": "458b1f67d08c567166b49e416fa3e8fefaec7c1a6cce8c3303305b853f8a3535",
    "method": "sub-pixel phase correlation (2\u00d7 upsample) on subject ROI x180:900 y776:1144 at full 1080x1920; flicker = MAD after motion compensation",
    "mean": [
      0.0,
      -0.1625
    ],
    "std": [
      0.0,
      0.5797359312652618
    ],
    "acceleration_rms": [
      0.0,
      0.656033342777212
    ],
    "step_change_max": [
      0.0,
      3.0
    ],
    "step_max_abs": [
      0.0,
      3.0
    ],
    "flicker_mad": 2.759156012535095
  },
  "note": "Sub-pixel phase correlation at full 1080x1920 on subject ROI; flicker = mean abs frame diff after motion compensation on ring ROI. v09 must beat v06 on step_change_max and flicker."
}`

## Hashes
| Item | SHA-256 |
|---|---|
| `owb_sa_s4_uranus_v09.mp4` | `458b1f67d08c567166b49e416fa3e8fefaec7c1a6cce8c3303305b853f8a3535` |
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
sha256=458b1f67d08c567166b49e416fa3e8fefaec7c1a6cce8c3303305b853f8a3535
open_median_step=2.3927
t=0.30s step=2.3227
t=0.33s step=2.6844
t=0.37s step=2.6721
t=0.40s step=2.3366
t=0.43s step=2.5105
t=0.47s step=2.5222
t=0.50s step=2.3831
t=0.55s step=2.6665
hitch_window_ok=True (none <0.35 or >2× median)


## Gates (all from sha `458b1f67d08c567166b49e416fa3e8fefaec7c1a6cce8c3303305b853f8a3535`)
| Gate | rc | note |
|---|---|---|
| gate_shorts_open | 0 | see `…_gate.txt` |
| sfx level | 0 | |
| polish_gate | 0 | |
| music_gate | 0 | |
| picture_qa | 0 | |
| finish_scan loop | 0 | PASS loop_diff_masked 4.08 open_median_step 2.39 head_matches [0, 0, 0, 0, 0] |

## Evidence
- Before/after strip: `/Users/benjaminoats/YouTube/orbit-with-ben/00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/06_Final-Exports/owb_sa_s4_uranus_v09_open_before_after.jpg` and `jobs/reviews/J1240/uranus_v09_open_before_after.jpg`
- Full-size frames: `jobs/reviews/J1240/uranus_v09_t*.jpg`
- UAT: `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/standalone_shorts_uranus_v09` and `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/standalone_shorts_uranus_v09` with MANIFEST.sha256
- Motion: `jobs/reviews/J1240/MOTION_DIAGNOSTIC.json`
- Transform sign check: `jobs/reviews/J1240/TRANSFORM_SIGN_CHECK.json`
- UAT playable: `jobs/reviews/J1240/UAT_PLAYABLE.json`

Park for elected Chief: do NOT repoint J1212 until Chief PASS on v09. No upload.
