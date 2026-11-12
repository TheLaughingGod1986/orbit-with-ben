# J2512 — 026 Mon 16 (`v06`) & Wed 18 (`v07`) Shorts: Fix J2508 Craft Faults, Gate, Watch & Offer Fixed Cuts

**Job:** `J2512`
**Branch:** `gemini/J2512`
**Spend:** £0 (no generated picture, no TTS/ElevenLabs spend, no paid service)
**YouTube / Studio changes:** None. Scheduled uploads `HZGTovJu_TQ` (Mon 16 Nov 11:30Z) and `cwU_0WWeNZ4` (Wed 18 Nov 11:30Z) are untouched; Ben's 10 Nov approved cuts (`mon16_cant_see_nearest_star_v05.mp4` and `wed18_robot_reach_nearest_star_v06.mp4`) remain the fallback for `J2513` and `J2514` if he does not OK the newer cuts before their deadlines.

---

## 1. Fixes Built (`_recut_026_shorts_J2512.py`)

### A. Mon 16 Short — `HZGTovJu_TQ` (*If You Can't See the Nearest Star, How Far Away Is It?*, airs Mon 16 Nov 11:30 London)
- **File:** `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/mon16_cant_see_nearest_star/06_Final-Exports/mon16_cant_see_nearest_star_v06.mp4`
- **SHA-256:** `7eb4f03d58e9738f8b10f865d098e4239e5a634ddc9bab58dcaad69e36e33349` (`22,126,866` bytes)
- **Copies verified bit-for-bit (`sha256`):**
  - Mini checkout: `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/mon16_cant_see_nearest_star/06_Final-Exports/mon16_cant_see_nearest_star_v06.mp4`
  - NAS `studio-live`: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/mon16_cant_see_nearest_star/06_Final-Exports/mon16_cant_see_nearest_star_v06.mp4`
  - NAS staging: `/Volumes/data/mac-mini-archive/youtube-staging/026/shorts_j2512/mon16_cant_see_nearest_star_v06.mp4`
  - iCloud watch copy: `OWB UAT/026_shorts_fixes_J2512/mon16_cant_see_nearest_star_v06.mp4`
- **Fallback (Ben OK'd 10 Nov 14:47Z):** `mon16_cant_see_nearest_star_v05.mp4` (`sha256: 5a2a4c2af8fb2148ad0975ed0d3cc88d329b3bd20ed071eb3626ba1d874d14f3`)
- **What changed (and nothing else):**
  - At `0:20.23–0:22.63` (`s06`, `2.40 s` immediately before the end card), replaced the repeated opening Paranal shot (`uhd_bt_paranal_07`, `v06_98.17`) with `026_NearestStar_v06.mp4` `13.80–16.20 s` (`uhd_bt_paranal_06`, ESO Paranal VLT Unit Telescope rotating smoothly under the Milky Way, free of `v06` overlays and unused elsewhere in `mon16`).
  - Motion check on `s06` (`72` frames): `min_diff = 0.2359`, `median_diff = 3.769`, `repeated_interior_frames = 0`.
  - Unchanged: voice, words, duration (`26.5 s`), captions, clean end card without YouTube ID, and audio level (`-14.2 LUFS / -2.2 dBTP`).

#### Pasted Gate Outputs (`mon16_cant_see_nearest_star_v06.mp4`)
```text
PASS  mon16_cant_see_nearest_star_v06.mp4  dur=26.5s  audio=-17.9dB  motion=26.34  f0diff=2.08  cut1=2.4s  vo_onset=0.03s  tail_gap=1.40s  vo_src=mix  dhash=400e0616020c3978  visor=0.0
   sheet /Volumes/MiniWork/scratch/orbit_shorts_gate/mon16_cant_see_nearest_star_v06_open_sheet.jpg

 s01     1.2s v06_98.17.mp4                ok
 s02     4.7s v06_152.73.mp4               WARN low detail: edge density 0.0247 < film p5 0.0257
 s03     9.2s v06_157.57.mp4               ok
 s04    13.7s v06_68.33.mp4                ok
 s05    18.1s v06_200.50.mp4               ok
 s06    21.4s v06_13.80.mp4                ok
end_card    24.6s end_card_thumb_A.png         ok
polish gate PASS: 0 of 7 rows failed, 1 to look at -> /Volumes/MiniWork/scratch/J2512-wt/02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/mon16_cant_see_nearest_star/06_Final-Exports/polish_gate_v06.json

WARN   0:05 row s02 v06_152.73.mp4: low detail: edge density 0.0247 < film p5 0.0257
picture QA PASS: 0 of 7 cuts fail, 1 to look at -> 02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/mon16_cant_see_nearest_star/06_Final-Exports/picture_qa_v06/PICTURE_QA.md, 02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/mon16_cant_see_nearest_star/06_Final-Exports/picture_qa_v06/picture_qa_review.jpg

music gate PASS: nearest-star_score_bed_v01_full.wav, 494.5 s, about 66.7 BPM, brief Pace: 66-80 BPM
```

---

### B. Wed 18 Short — `cwU_0WWeNZ4` (*If Voyager Needs 75,000 Years, How Far Is the Nearest Star?*, airs Wed 18 Nov 11:30 London)
- **File:** `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/wed18_robot_reach_nearest_star/06_Final-Exports/wed18_robot_reach_nearest_star_v07.mp4`
- **SHA-256:** `c0e6a13865a6abce10503ffa7ea29116fa885de2da34072f771dc85c0f1a2888` (`16,921,738` bytes)
- **Copies verified bit-for-bit (`sha256`):**
  - Mini checkout: `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/wed18_robot_reach_nearest_star/06_Final-Exports/wed18_robot_reach_nearest_star_v07.mp4`
  - NAS `studio-live`: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/wed18_robot_reach_nearest_star/06_Final-Exports/wed18_robot_reach_nearest_star_v07.mp4`
  - NAS staging: `/Volumes/data/mac-mini-archive/youtube-staging/026/shorts_j2512/wed18_robot_reach_nearest_star_v07.mp4`
  - iCloud watch copy: `OWB UAT/026_shorts_fixes_J2512/wed18_robot_reach_nearest_star_v07.mp4`
- **Fallback (Ben OK'd 10 Nov 14:46Z):** `wed18_robot_reach_nearest_star_v06.mp4` (`sha256: 80e4c86df51417db71efb9eaef9097669d6201d41396585acafb8ecbacfd936b`)
- **What changed (and nothing else):**
  - At `0:13.45–0:16.55` (`s05`, `3.10 s`, ESO star trails at Paranal from `026_NearestStar_v06.mp4` at `346.50 s`), replaced the frozen `3.10 s` hold with a continuous horizontal drift (`-70 px -> +70 px` across the `1920x1080` plate over `93` frames at `30 fps`, upscale unchanged at `1.78x`) so every frame moves cleanly and zero frames repeat.
  - Motion check on `s05` (`93` frames): `min_diff = 17.3658`, `median_diff = 18.9618`, `repeated_interior_frames = 0`.
  - Unchanged: voice, words, duration (`23.6 s`), captions, clean end card without YouTube ID, and audio level (`-14.2 LUFS / -2.2 dBTP`).

#### Pasted Gate Outputs (`wed18_robot_reach_nearest_star_v07.mp4`)
```text
PASS  wed18_robot_reach_nearest_star_v07.mp4  dur=23.6s  audio=-17.4dB  motion=9.01  f0diff=1.89  cut1=2.6s  vo_onset=0.00s  tail_gap=0.46s  vo_src=mix  dhash=0b2303090c0b0802  visor=0.0
   warn  picture barely changes in the first second (motion 9.0 < 10) — trim the clip's ease-in so frame 0 is already mid-action
   warn  open plate 13 bits from bSjWiCbB7pY (2026-11-13)
   sheet /Volumes/MiniWork/scratch/orbit_shorts_gate/wed18_robot_reach_nearest_star_v07_open_sheet.jpg

 s01     1.3s v06_0.30.mp4                 ok
 s02     4.0s v06_296.75.mp4               ok
 s03     7.2s v06_337.45.mp4               ok
 s04    11.2s v06_408.25.mp4               ok
 s05    15.0s v06_346.50_drift.mp4         ok
 s06    18.1s v06_13.80.mp4                ok
end_card    21.7s end_card_thumb_A.png         WARN low detail: edge density 0.0286 < film p5 0.0306
polish gate PASS: 0 of 7 rows failed, 1 to look at -> /Volumes/MiniWork/scratch/J2512-wt/02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/wed18_robot_reach_nearest_star/06_Final-Exports/polish_gate_v07.json

WARN   0:22 row end_card end_card_thumb_A.png: low detail: edge density 0.0286 < film p5 0.0306
picture QA PASS: 0 of 7 cuts fail, 1 to look at -> 02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/wed18_robot_reach_nearest_star/06_Final-Exports/picture_qa_v07/PICTURE_QA.md, 02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/wed18_robot_reach_nearest_star/06_Final-Exports/picture_qa_v07/picture_qa_review.jpg

music gate PASS: nearest-star_score_bed_v01_full.wav, 494.5 s, about 66.7 BPM, brief Pace: 66-80 BPM
```

---

## 2. Full-Speed Viewing & Listening Check (Multimodal Video + Audio)

Both deliverable MP4s were watched and listened to end-to-end with sound via multimodal `video/mp4` input (`audio_input,moving_video_input` demonstrated and recorded via `chief_relay.py capabilities`):

1. **`mon16_cant_see_nearest_star_v06.mp4` (`0:00.00–0:26.48`):**
   - **Sound:** Clear British narration (*"The nearest star to the Sun is out there tonight. You can't see it. It's called Proxima Centauri, a small red dwarf. It gives out less than 1% of the Sun's light. Its light still takes more than four years to reach you. The full film: How Far Is the Nearest Star?"*) over the ambient score bed at `-14.2 LUFS / -2.2 dBTP`. Zero clicks, jumps or breaths; final word *"star"* ends cleanly with a smooth music tail fade.
   - **Picture:** Full-bleed `9:16` moving open at frame 0 (`uhd_bt_paranal_07`); every shot moves continuously; `0:20.23–0:22.63` (`s06`) now shows the rotating VLT Unit Telescope enclosure under the Milky Way (`uhd_bt_paranal_06`), completely distinct from `s01` and all earlier cuts.
   - **On-screen text (every line read):**
     - `0:00–0:01`: `TOO` (white) / `FAINT` (yellow).
     - Lower-third captions: `THE NEAREST STAR` -> `TO THE SUN` -> `IS OUT THERE` -> `TONIGHT` -> `YOU CAN'T SEE` -> `IT` -> `IT'S CALLED PROXIMA` -> `CENTAURI` (clears before `0:09`).
     - `0:09–0:14` centre title: `If You Can't See / the Nearest Star, / How Far Away / Is It?`
     - Lower-third captions: `OF THE SUN'S` -> `ITS LIGHT STILL` -> `TAKES MORE THAN` -> `FOUR YEARS TO` -> `REACH YOU` -> `THE FULL FILM`.
     - `0:22.63–0:26.48` end card: `YOU CAN'T` / `SEE IT` thumbnail + `How Far Is / the Nearest Star? / Your two eyes are a ruler.` — completely clean, zero raw YouTube ID, zero clipped or stray text.

2. **`wed18_robot_reach_nearest_star_v07.mp4` (`0:00.00–0:23.60`):**
   - **Sound:** Clear British narration (*"Our fastest robot leaving the solar system is Voyager 1. Could a robot like it reach the nearest star? Voyager moves 17 kilometres every second. At that speed, the trip would take about 75,000 years. And Voyager isn't even heading that way. The full film: How Far Is the Nearest Star?"*) over the score bed at `-14.2 LUFS / -2.2 dBTP`. Zero clicks, jumps or breaths; final word *"star"* unclipped with a `2.0 s` music fade.
   - **Picture:** Full-bleed `9:16` moving Milky Way open; `0:13.45–0:16.55` (`s05`, ESO star trails at Paranal) now drifts smoothly and continuously across the star trails and Paranal dome for all `3.10 s` with zero repeated frames; `0:16.55–0:19.75` (`s06`) rotates smoothly under the Milky Way before the end card.
   - **On-screen text (every line read):**
     - `0:00–0:01`: `75,000` (white) / `YEARS` (yellow).
     - Lower-third captions: `OUR FASTEST ROBOT` -> `LEAVING THE SOLAR` -> `SYSTEM IS VOYAGER` -> `1` -> `COULD A ROBOT` -> `LIKE IT REACH` -> `THE NEAREST STAR?` -> `VOYAGER MOVES 17` (clears at `0:09`).
     - `0:09–0:14` centre title: `If Voyager Needs / 75,000 Years, / How Far Is the / Nearest Star?`
     - Lower-third captions: `TAKE ABOUT 75,000` -> `YEARS` -> `AND VOYAGER ISN'T` -> `EVEN HEADING THAT` -> `WAY` -> `THE FULL FILM`.
     - `0:19.75–0:23.60` end card: `YOU CAN'T` / `SEE IT` thumbnail + `How Far Is / the Nearest Star? / Could we ever go and look?` — completely clean, zero raw YouTube ID, zero clipped or stray text.

---

## 3. Watch Cards Armed & Verified on Live Board (`Review` Tab)

1. **`J2512.1` (Mon 16 first):**
   - **Title:** `Nearest star Short for Mon 16 Nov (v06, one shot changed)`
   - **File:** `OWB UAT/026_shorts_fixes_J2512/mon16_cant_see_nearest_star_v06.mp4` (`v06`)
   - **Due:** `2026-11-14 18:00` London (`2026-11-14T18:00Z`) · **Airs:** `2026-11-16 11:30` London (`2026-11-16T11:30Z`)
   - **Fixed:** `At 0:20.23-0:22.63 (just before the end card), replaced the repeated opening Paranal shot with a different moving ESO Paranal observatory shot from the film; everything else is unchanged`
   - **If not:** `the cut you OK'd on 10 Nov airs`
2. **`J2512.2` (Wed 18 second, `--add`):**
   - **Title:** `Nearest star Short for Wed 18 Nov (v07, the still now moves)`
   - **File:** `OWB UAT/026_shorts_fixes_J2512/wed18_robot_reach_nearest_star_v07.mp4` (`v07`)
   - **Due:** `2026-11-16 18:00` London (`2026-11-16T18:00Z`) · **Airs:** `2026-11-18 11:30` London (`2026-11-18T11:30Z`)
   - **Fixed:** `At 0:13.45-0:16.55 (the ESO star trails), replaced the 3.1 s frozen still with a smooth horizontal drift across the star trails so no frame repeats; everything else is unchanged`
   - **If not:** `the cut you OK'd on 10 Nov airs`
3. **`board_check.py --no-post` & Live `Review` Tab Verification (`https://studio-kanban.vercel.app/#review`):**
   - `board_check.py` returned `"ok": true, "expected": 6, "problems": [], "site": 200`, with both `OWB:ASK:J2512.1` and `OWB:ASK:J2512.2` in `"lane": "ready"`, `"readyFor": "Ben"`, `"play": 302`.
   - Opened `https://studio-kanban.vercel.app/#review` in headless Chrome and verified both cards appear under **`Needs your review (2)`** in exact order (`Nearest star Short for Mon 16 Nov (v06, one shot changed)` first, `Nearest star Short for Wed 18 Nov (v07, the still now moves)` second) with active `▶ Watch & review v06` and `▶ Watch & review v07` buttons.
