# J2549 — v08 worker delivery

Chief-scoped two-window fix for Friday 13 November. Worker evidence only; Chief creative decision and Ben’s watch remain. £0. No YouTube, Buffer, register or schedule changes.

Master SHA-256: `cefdf28ffec9220d753875a8cf68b40370e1b70098e3b92c69002f5a0e0207bb`. NAS copies and still sheet are in `safety_copies_v08.json`.

Only frames 84–175 (2.800–5.867 s) and 298–431 (9.933–14.400 s) change: two distinct crops of PIA24542, a real 62-image WATSON photographic mosaic. The early wide crop includes Perseverance and Ingenuity; the rotor line has the tighter helicopter-and-blades crop. Maximum scale 0.3392x and 0.969143x. Full source 12341×9076, page/credit/terms/hash in `provenance_v08.json`; source added to pool and NASA/JPL-Caltech/MSSS added to metadata credit. Native PIA24547 close-up rejected at 1196 px high.

Same 26.4 s, 792 frames, 1080×1920, 30 fps. Same caption generator, words, title windows and end card. AAC payload copied from v07 and hash matched; full decode exit 0 (`verification_v08.json`). Video re-encoded, not bit-identical. Whole-cut 32-frame still sheet inspected; all captions and title read, no raw ID. Tight crop clearly shows the helicopter’s body, legs and rotor blades. Still-photo motion is editorial pan/zoom, not evidence of rotating blades. No audio listening or moving-video perception claimed; Ben’s final watch supplies that check under AGENTS.md.

The first draft’s terrain-like early crop failed first-cut detection; the delivered wider rover/helicopter crop passes at 2.8 s. Initial QA inherited timeline offsets from v07, incorrectly treating the two still crops as footage stretches. Corrected those two records to actual still-crop geometry, with no footage offset; no threshold change or waiver. Existing 0:08 panorama low-detail warning remains for Chief review. Existing 2.56 s tail retained. Music comparison warns that historical comparison files are inaccessible, as on v07; copied sound is unchanged.

Five gates ran without report-only:

## gate

```text
PASS  fri13_ingenuity_72_v08.mp4  dur=26.4s  audio=-17.3dB  motion=11.87  f0diff=2.54  cut1=2.8s  vo_onset=0.09s  tail_gap=2.56s  vo_src=/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/fri13_ingenuity_72/06_Final-Exports/fri13_ingenuity_72_v06_stem_vo.wav  dhash=ce579fcf3e3fdf5d  visor=0.0002
   full-bleed 0.00s  fills the frame  detail top/centre/bottom=7.97/4.17/3.84  spread top/bottom=32.95/15.12
   full-bleed 0.25s  fills the frame  detail top/centre/bottom=7.76/4.0/7.56  spread top/bottom=32.77/22.05
   full-bleed 0.50s  fills the frame  detail top/centre/bottom=7.82/4.11/7.23  spread top/bottom=32.71/20.72
   warn  gap from last word to end is 2.56s > 1.5s (last word 23.84s, duration 26.40s)
   sheet /Volumes/MiniWork/scratch/orbit_shorts_gate/fri13_ingenuity_72_v08_open_sheet.jpg
```

## sfx

```text
SFX level PASS: VO -20.2 LUFS, SFX -44.7 LUFS, 1 hits
```

## polish

```text
s01_PIA24593     1.4s PIA24593.jpg                 ok
s02_PIA24542     4.3s PIA24542_full.jpg            ok
s03_PIA26237     7.9s PIA26237.jpg                 WARN low detail: edge density 0.0502 < film p5 0.0655
s04_PIA24542    12.2s PIA24542_full.jpg            ok
s05_PIA26243    16.6s PIA26243.jpg                 ok
s06_PIA26243    19.7s PIA26243.jpg                 ok
s07_end_card_loop_PIA24593    23.5s end_card_loop_PIA24593.jpg   ok
polish gate PASS: 0 of 7 rows failed, 1 to look at -> /Volumes/MiniWork/scratch/J2549-v08/render/polish_v08.json
```

## music

```text
WARN reused: couldn't read saturn_long_vo_v02_LISTEN.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read jupiter-vo.mp3 to compare (OSError); download it or pass --others
WARN reused: couldn't read jupiter-music.mp3 to compare (OSError); download it or pass --others
WARN reused: couldn't read friday_black_dwarf_short_vo_v01_LISTEN.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v02_LISTEN.m4a to compare (OSError); download it or pass --others
WARN reused: couldn't read monday_saturn_short_vo_v02_how_long.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v03_tightened.m4a to compare (OSError); download it or pass --others
WARN reused: couldn't read monday_saturn_short_vo_v01_LISTEN.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v03b_tightened_LOCK.m4a to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v03b_tightened_LOCK.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v01_LISTEN.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read monday_saturn_short_vo_v02_how_long.mp3 to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v03_tightened.wav to compare (OSError); download it or pass --others
music gate PASS: mars-robot_score_bed_v02_full.mp3, 492.0 s, about 120.0 BPM, brief Pace: 60-72 BPM
```

## picture_qa

```text
WARN   0:08 row s03_PIA26237 PIA26237.jpg: low detail: edge density 0.0502 < film p5 0.0655
picture QA PASS: 0 of 7 cuts fail, 1 to look at -> /Volumes/MiniWork/scratch/J2549-v08/render/picture_qa_v08/PICTURE_QA.md, /Volumes/MiniWork/scratch/J2549-v08/render/picture_qa_v08/picture_qa_review.jpg
```

## Handoff

v08 watch card requested for Thu 12 Nov 18:00 London, air Fri 13 Nov 11:30; fallback “the cut you OK’d airs”. Chief reviews the source/crops and inherited warning, then rules on v08. J2520 remains the separate swap job after Ben’s approval. No worker approval, merge or upload.
