# Gate Report — `034_short01_testA_opening_v02.mp4` (`J2438`)

- **File:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/034_short01_testA_opening_v02.mp4`
- **SHA-256:** `c9a02052ff7a33cba10adc52e440cfe793c6cca1f31e355262acf9fd9c4ba677`
- **Duration:** `36.500 s` (`1095` frames at `30/1` CFR)
- **AAC Loudness:** `-14.10 LUFS` integrated, `-2.10 dBTP` true peak

## 1. `gate_shorts_open.py` (rc=0)
```text
PASS  034_short01_testA_opening_v02.mp4  dur=36.5s  audio=-17.1dB  motion=29.06  f0diff=7.29  cut1=2.1s  vo_onset=0.07s  tail_gap=0.48s  vo_src=/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/034_short01_testA_opening_v02_stem_vo.wav  dhash=313011b111135110  visor=0.0
   full-bleed 0.00s  fills the frame  sharp above/middle/below=0.761/0.723/0.779  detail top/centre/bottom=17.62/8.42/8.32  spread top/bottom=34.56/17.49
   full-bleed 0.25s  fills the frame  sharp above/middle/below=0.776/0.744/0.789  detail top/centre/bottom=18.11/8.91/8.57  spread top/bottom=35.79/20.44
   full-bleed 0.50s  fills the frame  sharp above/middle/below=0.821/0.777/0.78  detail top/centre/bottom=18.69/9.23/8.56  spread top/bottom=36.57/23.91
   full-bleed whole Short  0/37 frames padded at one a second, 0/73 at two a second  padded stretches: none  end card 35.1-36.5s judged apart
   warn  duration 36.5s outside 22–27s band
   sheet /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/034_short01_testA_opening_v02_open_sheet.jpg
```

## 2. `picture_qa.py` (rc=0)
```text
WARN   0:19 row R03a File_Video_-_Nasa_s_New_Horizons_-_Pluto_Flyby_14_7_2015__51718116305_.webm.webm: low detail: luma std 14.24 < 18.0; low detail: edge density 0.0142 < film p5 0.0196
WARN   0:35 row R04c PIA19936.jpg: kind of picture: 'Northern Sputnik Planitia Mosaic (New Horizons)' (mosaic), look at it full size
picture QA PASS: 0 of 12 cuts fail, 2 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/picture_qa_v02/PICTURE_QA.md, /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/picture_qa_v02/picture_qa_review.jpg
```

## 3. `polish_gate.py` (rc=0)
```text
R01a     1.1s File_Video_-_Nasa_s_New_Hori ok
R01b     3.1s PIA20291.jpg                 ok
R01c     5.3s PIA20726.jpg                 ok
R02a     8.1s code_graphic_034_r02a_sputni ok
R02b    11.6s PIA19952.jpg                 ok
R02c    15.1s code_graphic_034_r02b_texas_ ok
R03a    18.6s File_Video_-_Nasa_s_New_Hori WARN low detail: luma std 14.24 < 18.0; low detail: edge density 0.0142 < film p5 0.0196
R03b    22.1s PIA20534.jpg                 ok
R03c    25.6s PIA20198.jpg                 ok
R04a    28.9s PIA20038.jpg                 ok
R04b    31.9s PIA20732.jpg                 ok
R04c    35.0s PIA19936.jpg                 ok
polish gate PASS: 0 of 12 rows failed, 1 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/polish_gate_v02.json
```

## 4. `music_gate.py` (rc=0)
```text
 reused: couldn't read monday_saturn_short_vo_v02_how_long.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v03_tightened.m4a to compare (OSError); download it or pass --others
WARN reused: couldn't read monday_saturn_short_vo_v01_LISTEN.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v03b_tightened_LOCK.m4a to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v03b_tightened_LOCK.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v01_LISTEN.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read monday_saturn_short_vo_v02_how_long.mp3 to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v03_tightened.wav to compare (OSError); download it or pass --others
music gate PASS: pluto_score_bed_v01.mp3, 646.9 s, about 66.7 BPM, brief Pace: 64-74 BPM
```

## 5. `sfx_kit.py level` (rc=0)
```text
SFX level PASS: VO -16.5 LUFS, SFX -40.1 LUFS, 7 hits
```
