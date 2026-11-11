# J2549 — Mars helicopter Short v07

Worker delivery for Chief review; no final creative approval or motion/audio viewing claimed. £0. No YouTube, Buffer, upload register or schedule changes.

Built `fri13_ingenuity_72_v07.mp4`, SHA-256 `947f5c726d6686c3c8317c4b7e02be4953412c1ad15f574573190e9fe1f3a688`. Source v06 SHA `54929328bd18d8ef359bef490a9225fd62c2fcc388fa996d9f554caa1bd51cd7` matches the approved J2520 brief and J2510 record. UPLOADS still correctly names the older v02 / `bSjWiCbB7pY`, because J2520 has not yet swapped it. No register changes belong in this edit job.

## Changes

- Frames 84–175 (2.800–5.867 s): full-frame crop of existing real Navcam damaged-blade shadow photograph PIA26243, maximum scale 0.836x. It is a ground/shadow illustration, not footage of a flight.
- Frames 298–431 (9.933–14.400 s): full-frame crop of existing real PIA26237 Mars panorama, maximum scale 0.474x. This illustrates Mars terrain during the rotor-speed line rather than showing a rotor spinning; Chief should assess that loss of specificity.
- Frames 432–565 (14.400–18.867 s): full-frame damaged-blade shadow, maximum scale 0.836x. The following v06 shadow shot remains untouched; these are one contiguous appearance, plus one earlier appearance.
- Everything outside those windows derives from v06. Same 26.400 seconds, 792 frames, 1080×1920, 30 fps. Same caption generator, grouping, font, placement and timestamps, with the existing long-title overlay restored over the changed interval. Original AAC packets copied unchanged: both stream hashes `c2017ce0b8f52a058504aa90407a024971c6aaa908630bd5ae5c14efad8f05d8`. No sound remix.

The original 500×500 and 640×480 Navcam sources would need 3.84–4x enlargement to fill vertical 1080×1920. Existing 720-high JPL videos need 2.667x. Larger real photos were recovered from `2026-10-24/YouTube/orbit-with-ben/owb025.tar`; no download or generation. PIA26482 rejected after inspection because it is a labelled sourced reconstruction.

## Verification and limitations

All five gate commands below ran without report-only and reported PASS. Complete ffmpeg decode exit 0. Still sheet inspected across the whole cut, including captions, title and end card: no blurred/mirrored padding in either replacement window and no raw ID added. The existing low-detail panorama warning remains at about 0:08. The original 2.56-second post-word tail is retained. Music reuse comparisons report inaccessible historical comparison files; the music/audio are bit-identical to approved v06, not a new score.

No demonstrated `audio_input` or `moving_video_input` in this session; capability record was updated with empty availability. I did not watch motion or hear the cut. AGENTS.md “Ben’s final watch is the watch-and-listen check” applies: tool checks and still inspection are complete, Chief rules on evidence, Ben watches the finished cut. This is not a capability-only hold.

Unchanged-window compressed frames were spot-compared at 0, 1, 2, 6.5, 8, 19.5, 22 and 25 s: mean absolute grayscale differences at 270×480 were 0.325–0.583/255 after video re-encoding. Full-resolution SSIM across those windows was 0.903217, affected by compression of grain; do not describe the video stream as bit-identical. Audio is bit-identical.

Initial draft on grey terrain failed the first-cut detector; it was replaced by the visually distinct real shadow photo. Final opening gate detects 2.8 s. Initial music check against the archive failed because the plan lives in git; rerun with the archived bed beside the tracked plan in the isolated film worktree passed. No gate waiver or threshold change.

## Gates

### gate_v07.txt

```text
PASS  fri13_ingenuity_72_v07.mp4  dur=26.4s  audio=-17.3dB  motion=11.88  f0diff=2.54  cut1=2.8s  vo_onset=0.09s  tail_gap=2.56s  vo_src=/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/fri13_ingenuity_72/06_Final-Exports/fri13_ingenuity_72_v06_stem_vo.wav  dhash=ce57dfcf3e3fdf5d  visor=0.0001
   full-bleed 0.00s  fills the frame  detail top/centre/bottom=7.98/4.17/3.84  spread top/bottom=32.96/15.12
   full-bleed 0.25s  fills the frame  detail top/centre/bottom=7.78/4.02/7.56  spread top/bottom=32.78/22.06
   full-bleed 0.50s  fills the frame  detail top/centre/bottom=7.84/4.11/7.24  spread top/bottom=32.74/20.74
   warn  gap from last word to end is 2.56s > 1.5s (last word 23.84s, duration 26.40s)
   sheet /Volumes/MiniWork/scratch/orbit_shorts_gate/fri13_ingenuity_72_v07_open_sheet.jpg
```

### sfx_v07.txt

```text
SFX level PASS: VO -20.2 LUFS, SFX -44.7 LUFS, 1 hits
```

### polish_v07.txt

```text
s01_PIA24593     1.4s PIA24593.jpg                 ok
s02_PIA26243     4.3s PIA26243.jpg                 ok
s03_PIA26237     7.9s PIA26237.jpg                 WARN low detail: edge density 0.0505 < film p5 0.0616
s04_PIA26237    12.2s PIA26237.jpg                 ok
s05_PIA26243    16.6s PIA26243.jpg                 ok
s06_PIA26243    19.7s PIA26243.jpg                 ok
s07_end_card_loop_PIA24593    23.5s end_card_loop_PIA24593.jpg   ok
polish gate PASS: 0 of 7 rows failed, 1 to look at -> /Volumes/MiniWork/scratch/J2549/render/polish_v07.json
```

### music_v07.txt

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

### picture_qa_v07.txt

```text
WARN   0:08 row s03_PIA26237 PIA26237.jpg: low detail: edge density 0.0505 < film p5 0.0616
picture QA PASS: 0 of 7 cuts fail, 1 to look at -> /Volumes/MiniWork/scratch/J2549/render/picture_qa_v07/PICTURE_QA.md, /Volumes/MiniWork/scratch/J2549/render/picture_qa_v07/picture_qa_review.jpg
```

## Delivery and next action

Verified NAS copies and SHA-256 values are in `safety_copies.json`. Still sheet: `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/J2549_mars_helicopter/v07_text_sheet.jpg`.

Automatic approval review rejected the requested iCloud CloudDocs copy as sensitive synced egress not specifically authorized. No iCloud write occurred. NAS-only copies are the safe alternative, and the watch card uses the absolute NAS file path.

Chief: review the still warning and semantic compromises, then decide v07. Ben’s watch is due Thu 12 Nov 18:00 London, with “the cut you OK’d airs” as fallback. Per brief, if v07 is not ready and passed by Thu 12 Nov 12:00 London, retain v06. J2520 remains responsible for putting v06 in the slot first. Any v07 upload/swap requires a separate Chief job after Ben’s approval.
