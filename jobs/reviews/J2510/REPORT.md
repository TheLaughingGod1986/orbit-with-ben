# J2510 — 025 Mars Shorts (`N42gKBbD7tE` Thu 12 Nov & `bSjWiCbB7pY` Fri 13 Nov) End-Card & Rule-24 Re-Cuts

**Job:** `J2510`
**Branch:** `J2510-recut`
**Spend:** £0 (no generated picture, no new TTS or music spend)
**YouTube changes:** None (both scheduled uploads in YouTube Studio untouched pending Ben's watch and explicit OK).

---

## Summary Verdicts

1. `thu12_length_test_dust_v05.mp4` (`N42gKBbD7tE`, airs Thu 12 Nov 11:30Z): **KEEP** (`sha256: abb3c33e70c11fddd2455587b7685b1da7ffc2883fbbe125e715f38549d6fb1b`)
2. `fri13_ingenuity_72_v06.mp4` (`bSjWiCbB7pY`, airs Fri 13 Nov 11:30Z): **KEEP** (`sha256: 54929328bd18d8ef359bef490a9225fd62c2fcc388fa996d9f554caa1bd51cd7`)

---

## 1. `N42gKBbD7tE` — *How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years?* (Airs Thu 12 Nov 11:30Z)

- **Original scheduled build (`thu12_length_test_dust_v01.mp4`):**
  - Rendered raw YouTube video ID `Js6EQJ8qDi8` in yellow under `Could a Robot Survive on Mars?` on the end card (`52.12–54.62 s`).
  - Failed Rule 24 first-cut timing (`cut1 = 6.733 s > 3.0 s`) and 26 Oct audio gate (`-14.9 LUFS`, `-1.5 dBTP`).
- **Re-cut (`02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/thu12_length_test_dust/06_Final-Exports/thu12_length_test_dust_v05.mp4`):**
  - **Verdict:** **KEEP**
  - **SHA-256:** `abb3c33e70c11fddd2455587b7685b1da7ffc2883fbbe125e715f38549d6fb1b`
  - **Duration:** `54.63 s` (127 spoken words; Chief-OK'd 50–60 s Short length test, untouched locked VO `254.7–307.3 s` of `025_MarsRobot_full_rough_v03f.mp4`)
  - **What changed:**
    1. **End card (`52.12–54.62 s`):** Removed the raw video ID `Js6EQJ8qDi8` under `Could a Robot Survive on Mars?` (`title_png(..., with_id=False)`).
    2. **First-second Rule 24 cut (`<= 3.0 s`) & full-bleed `9:16`:** Kept the full-bleed `9:16` moving frame-0 opening push on `PIA22909.jpg` (`0.00–2.40 s`, zero blur-pad or letterbox bars, `f0diff = 4.63 >= 1.50`, `motion = 29.47 >= 10.0`) and moved the first cut forward from `6.733 s` to `2.40 s` (`<= 3.0 s`, in the sentence pause after `"Opportunity should have starved within months."` at `2.20–2.64 s`) onto `s02_r20` (`PIA17759.jpg` solar deck with continuous sub-pixel push matching `v03f` at the `6.533 s` crossfade).
    3. **Phone-safe captions (`max_w = 72% W`, `y = 78% H`):** Kept all lower-third captions clear of the right-side phone buttons and cleared the final caption (`SKY TURNING OFF.`) at `52.17 s` as the end-card title comes on.
    4. **Audio level (`-14.3 LUFS / -2.2 dBTP`):** Levelled the locked `v01` mix to the 26 Oct gate (`-14.0 ± 0.5 LUFS`, `<= -1.6 dBTP`).
  - **Watch folder & NAS copies (all byte-identical):**
    - `OWB UAT/025_mars_shorts_recut_J2510/thu12_length_test_dust_v05.mp4` (iCloud & NAS `OWB UAT`)
    - `/Volumes/data/mac-mini-archive/youtube-staging/025/thu12_length_test_dust_v05/thu12_length_test_dust_v05.mp4`
    - `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/thu12_length_test_dust/06_Final-Exports/thu12_length_test_dust_v05.mp4`

### Pasted Gate Outputs (`thu12_length_test_dust_v05.mp4`)

```text
PASS  thu12_length_test_dust_v05.mp4  dur=54.63s  audio=-17.3dB  motion=29.47  f0diff=4.63  cut1=2.4s  vo_onset=0.10s  tail_gap=2.51s  vo_src=/Volumes/MiniWork/scratch/J2510/wt/02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/thu12_length_test_dust/06_Final-Exports/thu12_length_test_dust_v05_stem_vo.wav  dhash=2353880d59b10637  visor=0.0015
   warn  gap from last word to end is 2.51s > 1.5s (last word 52.12s, duration 54.63s)
   warn  possible Orbit at 0 s (visor 0.0015) — eyeball the sheet
   sheet /Volumes/MiniWork/scratch/orbit_shorts_gate/thu12_length_test_dust_v05_open_sheet.jpg

SFX level PASS: VO -20.4 LUFS, SFX -38.3 LUFS, 1 hits

s01_r20     1.2s PIA22909.jpg                 ok
s02_r20     4.6s PIA17759.jpg                 ok
s03_r20     9.3s PIA18079.jpg                 ok
s04_r20    13.7s PIA18079.jpg                 ok
s05_r20    17.7s PIA06739.jpg                 ok
s06_r21    22.2s PIA22330.jpg                 ok
s07_r21    26.6s PIA17956.jpg                 ok
s08_r21    31.6s PIA22520.jpg                 ok
s09_r21    36.8s PIA26716.jpg                 ok
s10_r21    41.5s PIA22520.jpg                 WARN low detail: edge density 0.0069 < film p5 0.0073
s11_r22    46.5s PIA07372.jpg                 ok
s12_r22    50.8s PIA22928.jpg                 ok
s13_end_loop    53.6s end_card_loop_PIA22909.mp4   ok
polish gate PASS: 0 of 13 rows failed, 1 to look at -> 02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/thu12_length_test_dust/06_Final-Exports/thu12_length_test_dust_v05_polish.json

music gate PASS: mars-robot_score_bed_v02_full.mp3, 492.0 s, about 120.0 BPM, brief Pace: 60-72 BPM

WARN   0:27 row s07_r21 PIA17956.jpg: sharpness: upscaled 2.01x, may look soft
WARN   0:37 row s09_r21 PIA26716.jpg: sharpness: upscaled 2.08x, may look soft
WARN   0:42 row s10_r21 PIA22520.jpg: low detail: edge density 0.0069 < film p5 0.0073
picture QA PASS: 0 of 13 cuts fail, 3 to look at -> 02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/thu12_length_test_dust/06_Final-Exports/picture_qa_v05/PICTURE_QA.md, 02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/thu12_length_test_dust/06_Final-Exports/picture_qa_v05/picture_qa_review.jpg
```

### Viewing & Listening Notes (`thu12_length_test_dust_v05.mp4`)

- Watched and listened from `0:00.00` to `0:54.63` with verified `moving_video_input` + `audio_input` perception, and eyeballed `thu12_length_test_dust_v05_open_sheet.jpg` (`visor=0.0015` is warm orange Martian rock + dark caption outline, zero Orbit on screen) and `picture_qa_review.jpg`.
- **First second:** Full-bleed `9:16` Martian rock & sand (`PIA22909.jpg`) already moving at frame 0 (`f0diff = 4.63`, `motion = 29.47`), zero blur-pad or letterbox bands, `SAVED BY` (white) / `THE WIND` (yellow) on screen at `0:00.00`, VO onset `0.10 s` (`"Opportunity should have starved within months."`), clean hard cut at `0:02.40` (`<= 3.0 s`) to Opportunity's solar deck (`PIA17759.jpg`).
- **On-screen text read in full:**
  - `0:00.00–0:02.20` (top): `SAVED BY` / `THE WIND`
  - `0:09.00–0:14.00` (top): `Could a Robot` / `Survive on Mars?`
  - Lower-third captions (`0:00.10–0:52.17`, `max_w = 72% W`, `y = 78% H`, clear of phone buttons): `OPPORTUNITY SHOULD HAVE`, `STARVED WITHIN MONTHS.`, `INSTEAD,`, `AGAIN AND AGAIN,`, `MARTIAN WIND AND`, `PASSING DUST DEVILS`, `SWEPT ITS PANELS`, `CLEAN.`, `THE TEAM CALLED`, `THEM CLEANING EVENTS.`, `EACH ONE GAVE`, `THE ROVER BACK`, `ITS POWER,`, `AND IT KEPT`, `DRIVING.`, `NINETY DAYS BECAME`, `YEARS.`, `YEARS BECAME MORE`, `THAN FOURTEEN.`, `THEN,`, `IN 2018,`, `A STORM GREW`, `UNTIL IT WRAPPED`, `THE WHOLE PLANET.`, `THE SKY OVER`, `OPPORTUNITY GREW SO`, `DARK THAT ALMOST`, `NO SUNLIGHT REACHED`, `ITS PANELS.`, `ON THE 10TH`, `OF JUNE,`, `2018,`, `OPPORTUNITY SENT ITS`, `LAST SIGNAL.`, `ENGINEERS ON EARTH`, `SENT MORE THAN`, `A THOUSAND COMMANDS`, `OVER THE NEXT`, `EIGHT MONTHS ASKING`, `IT TO WAKE`, `UP.`, `IT NEVER ANSWERED.`, `WHAT FINALLY STOPPED`, `THE MOST SUCCESSFUL`, `ROVER OF ITS`, `TIME WAS NOT`, `COLD OR ROCK.`, `IT WAS THE`, `SKY TURNING OFF.`
  - **End card (`0:52.12–0:54.63`):** `Could a Robot` / `Survive on Mars?` over the full-bleed moving `PIA22909` Mars loop. Raw ID `Js6EQJ8qDi8` is completely gone; no stray letters, typos, or clipped edges.
- **Sound & picture:** Clear British VO over the Mars score bed (`-14.3 LUFS / -2.2 dBTP`), zero clicks, pops, or clipped words (`"off."` completes cleanly at `52.12 s`), smooth motion throughout with no frozen or flash frames.

---

## 2. `bSjWiCbB7pY` — *How Did a Helicopter Fly 72 Times on Mars?* (Airs Fri 13 Nov 11:30Z)

- **Original scheduled build (`fri13_ingenuity_72_v02.mp4`):**
  - Rendered raw YouTube video ID `Js6EQJ8qDi8` in yellow under `Could a Robot Survive on Mars?` on the end card (`20.54–26.40 s`).
  - Failed Rule 24 opening gate (`f0diff = 1.36 < 1.50`, `motion = 6.3 < 10.0`, `cut1 = 3.30 s > 3.0 s`, and opened on a `500x500` GIF with top/bottom blur-pad bands) and 26 Oct audio gate (`-15.0 LUFS`, `-1.5 dBTP`).
- **Re-cut (`02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/fri13_ingenuity_72/06_Final-Exports/fri13_ingenuity_72_v06.mp4`):**
  - **Verdict:** **KEEP**
  - **SHA-256:** `54929328bd18d8ef359bef490a9225fd62c2fcc388fa996d9f554caa1bd51cd7`
  - **Duration:** `26.40 s` (55 spoken words; untouched locked VO `fri13_ingenuity_72_vo_v01.wav`)
  - **What changed:**
    1. **End card (`20.54–26.40 s`):** Removed the raw video ID `Js6EQJ8qDi8` under `Could a Robot Survive on Mars?` (`wed.title_png(end_title, with_id=False)`) and replaced the blur-padded end-card plate with full-bleed `9:16` `PIA24593.jpg` gliding back into the opening framing.
    2. **First-second Rule 24 full-bleed `9:16` motion & first cut (`<= 3.0 s`):** Opened Shot 0 (`0.00–2.80 s`) full-bleed `9:16` (`upscale 0.70x`, zero blur-pad or letterbox bands) on `PIA24593.jpg` (Ingenuity's first aerial colour photograph in flight over Mars and Perseverance's rover tracks) with a front-loaded sub-pixel aerial swoop (`f0diff = 2.55 >= 1.50`, `motion = 11.87 >= 10.0`), and cut at `2.80 s` (`<= 3.0 s`, right after `"This helicopter was built for five flights"` at `2.76 s`) to `PIA24644.gif` (`2.80–5.88 s`, Ingenuity's animated shadow descending across the Martian sand during `"on Mars. It flew seventy-two."`, paced so the helicopter shadow stays in-frame throughout).
    3. **Phone-safe captions (`max_w = 72% W`, `y = 78% H`):** Placed all lower-third captions clear of the right-side phone buttons.
    4. **Audio level (`-14.3 LUFS / -2.1 dBTP`):** Levelled the locked mix to the 26 Oct gate (`-14.0 ± 0.5 LUFS`, `<= -1.6 dBTP`) and set the bed during speech to `-3 dB` below `0.134` (`0.095`, lifted `x10.5` in the post-VO hold) so `sfx_kit.py level` passes with `> 10 LU` margin under the VO.
  - **Watch folder & NAS copies (all byte-identical):**
    - `OWB UAT/025_mars_shorts_recut_J2510/fri13_ingenuity_72_v06.mp4` (iCloud & NAS `OWB UAT`)
    - `/Volumes/data/mac-mini-archive/youtube-staging/025/fri13_ingenuity_72_v06/fri13_ingenuity_72_v06.mp4`
    - `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/fri13_ingenuity_72/06_Final-Exports/fri13_ingenuity_72_v06.mp4`

### Pasted Gate Outputs (`fri13_ingenuity_72_v06.mp4`)

```text
PASS  fri13_ingenuity_72_v06.mp4  dur=26.4s  audio=-17.3dB  motion=11.87  f0diff=2.55  cut1=2.8s  vo_onset=0.09s  tail_gap=2.56s  vo_src=/Volumes/MiniWork/scratch/J2510/wt/02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/fri13_ingenuity_72/06_Final-Exports/fri13_ingenuity_72_v06_stem_vo.wav  dhash=ce179fcf3e1fdf5d  visor=0.0002
   warn  gap from last word to end is 2.56s > 1.5s (last word 23.84s, duration 26.40s)
   sheet /Volumes/MiniWork/scratch/orbit_shorts_gate/fri13_ingenuity_72_v06_open_sheet.jpg

SFX level PASS: VO -20.2 LUFS, SFX -44.7 LUFS, 1 hits

s01_PIA24593     1.4s PIA24593.jpg                 ok
s02_PIA24644     4.3s PIA24644.gif                 WARN low detail: edge density 0.0184 < film p5 0.0206
s03_PIA26237     7.9s PIA26237.jpg                 ok
s04_PIA24584    12.2s PIA24584.jpg                 ok
s05_PIA26244    16.6s PIA26244.gif                 ok
s06_PIA26243    19.7s PIA26243.jpg                 ok
s07_end_card_loop_PIA24593    23.5s end_card_loop_PIA24593.jpg   ok
polish gate PASS: 0 of 7 rows failed, 1 to look at -> 02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/fri13_ingenuity_72/06_Final-Exports/fri13_ingenuity_72_v06_polish.json

music gate PASS: mars-robot_score_bed_v02_full.mp3, 492.0 s, about 120.0 BPM, brief Pace: 60-72 BPM

WARN   0:04 row s02_PIA24644 PIA24644.gif: sharpness: upscaled 2.16x, may look soft; low detail: edge density 0.0184 < film p5 0.0206
picture QA PASS: 0 of 7 cuts fail, 1 to look at -> 02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/fri13_ingenuity_72/06_Final-Exports/picture_qa_v06/PICTURE_QA.md, 02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/fri13_ingenuity_72/06_Final-Exports/picture_qa_v06/picture_qa_review.jpg
```

### Viewing & Listening Notes (`fri13_ingenuity_72_v06.mp4`)

- Watched and listened from `0:00.00` to `0:26.40` with verified `moving_video_input` + `audio_input` perception, and inspected `fri13_ingenuity_72_v06_open_sheet.jpg` (`visor=0.0002`) and `picture_qa_review.jpg`.
- **First second:** Opens on full-bleed `9:16` aerial Mars sand and Perseverance rover tracks (`PIA24593.jpg`, zero blur-pad or letterbox bands), already moving at frame 0 (`f0diff = 2.55`, `motion = 11.87`), `72` (white) / `FLIGHTS` (yellow) on screen immediately (`0:00.00–0:02.20`), VO onset `0.09 s` (`"This helicopter was built for five flights on Mars."`), and clean hard cut at `0:02.80` (`<= 3.0 s`) to Ingenuity's animated shadow in flight (`PIA24644.gif`), which stays centred in-frame across `"on Mars. It flew seventy-two."`
- **On-screen text read in full:**
  - `0:00.00–0:02.20` (top): `72` / `FLIGHTS`
  - `0:09.00–0:14.00` (top): `Could a Robot` / `Survive on Mars?`
  - Lower-third captions (`0:00.10–0:23.89`, `max_w = 72% W`, `y = 78% H`, clear of phone buttons): `THIS HELICOPTER WAS`, `BUILT FOR FIVE`, `FLIGHTS ON MARS.`, `IT FLEW SEVENTY-TWO.`, `THE AIR THERE`, `IS ABOUT 1%`, `AS THICK AS`, `OURS.`, `ITS BLADES SPUN`, `MORE THAN 2,000`, `TIMES A MINUTE`, `TO LIFT IT.`, `IN 2024,`, `A DAMAGED BLADE`, `FINALLY GROUNDED IT.`, `IT'S STILL STANDING`, `THERE.`, `THE FULL FILM,`, `COULD A ROBOT`, `SURVIVE ON MARS?`
  - **End card (`0:20.54–0:26.40`):** `Could a Robot` / `Survive on Mars?` over the full-bleed `9:16` `PIA24593.jpg` aerial Mars glide. Raw ID `Js6EQJ8qDi8` is completely gone; no stray letters, typos, or clipped edges.
- **Sound & picture:** Clear British VO over the Mars score bed (`-14.3 LUFS / -2.1 dBTP`), zero clicks, pops, or level jumps, unclipped last word (`"Mars?"` ends `23.84 s`) with smooth `2.5 s` music lift and `1.0 s` fade, and continuous motion across all 7 cuts.
