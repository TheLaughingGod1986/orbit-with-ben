# J2494 — Scheduled Orbit Shorts First-Second Re-Cuts (Rule 24) & End-Card Audit

**Job:** `J2494`
**Branch / PR:** `J2494-recut` (PR #728)
**Spend:** £0 (no generated picture, no new TTS spend)
**YouTube changes:** None (all scheduled uploads untouched pending Ben's watch and explicit OK).

---

## 1. The Four Rule-24 Shorts (Soonest Air Date First)

### 1.1 `gmzaCfJF1gA` — *Why Does Pluto's Giant Ice Heart Have Zero Craters?* (Airs Sat 14 Nov 11:30Z)
- **Original export (`owb_sa_s7_pluto_heart_v01.mp4`):**
  - Failed rule 24 on three counts: still open (`f0diff=0.64 < 1.50`), first cut at `5.90s > 3.0s`, and meta-promise line (`"Stay, and I'll show you why that's strange."`), plus tail gap `3.01s > 1.5s`.
- **Re-cut (`00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/06_Final-Exports/owb_sa_s7_pluto_heart_v02.mp4`):**
  - **SHA-256:** `ab33a789dbb00411d5bb91cee362fa697a64072803ed9c2d7b422ede4fd8fdc2`
  - **Duration:** `17.6 s` (35 spoken words; J0216 standalone test Short)
  - **What changed:**
    1. Excised the cleanly separable sentence `"Stay, and I'll show you why that's strange."` (`3.02–5.48 s` in the locked VO) with a `0.15 s` breath join (`£0`, no new VO needed).
    2. Opened on continuous mid-action motion across Pluto's Giant Ice Heart (`PIA19952`, `5000x5000` New Horizons MVIC colour mosaic; `f0diff=4.48`, `motion=18.77`).
    3. Moved the first cut forward from `5.90 s` to `2.70 s` (`<= 3.0 s`) and tightened the tail loop gap from `3.01 s` to `1.29 s` (`<= 1.50 s`).
    4. No end card or YouTube video ID appears anywhere on screen.
  - **Watch folder copy:** `OWB UAT/026_shorts_first_second_recut_J2494/owb_sa_s7_pluto_heart_v02.mp4` (iCloud and NAS).

#### Pasted Gate Outputs (`owb_sa_s7_pluto_heart_v02.mp4`)
```text
PASS  owb_sa_s7_pluto_heart_v02.mp4  dur=17.6s  audio=-17.2dB  motion=18.77  f0diff=4.48  cut1=2.7s  vo_onset=0.07s  tail_gap=1.29s  vo_src=/Volumes/MiniWork/scratch/J2494/s7_v02/stem_vo.wav  dhash=0f7fff6347431183  visor=0.0
   warn  duration 17.6s outside 22–27s band
   sheet /Volumes/MiniWork/scratch/orbit_shorts_gate/owb_sa_s7_pluto_heart_v02_open_sheet.jpg

SFX level PASS: VO -19.9 LUFS, SFX -37.0 LUFS, 2 hits

   1     1.4s /Volumes/data/mac-mini-archi WARN low detail: edge density 0.1725 < film p5 0.1726
   2     4.5s /Volumes/data/mac-mini-archi ok
   3     8.0s /Volumes/data/mac-mini-archi ok
   4    11.5s /Volumes/data/mac-mini-archi ok
   5    14.9s /Volumes/data/mac-mini-archi ok
polish gate PASS: 0 of 5 rows failed, 1 to look at -> /Volumes/MiniWork/scratch/J2494/s7_v02/polish_gate.json

WARN pace: measured about 120.0 BPM against the brief's 84-96; Claude listens
music gate PASS: owb-standalone-shorts_score_bed_v01.mp3, 60.0 s, about 120.0 BPM, brief Pace: 84-96 BPM

WARN   0:01 row 1 /Volumes/data/mac-mini-archive/scratch/J1199/plates/s7_pluto/PIA19952.jpg: low detail: edge density 0.1725 < film p5 0.1726
picture QA PASS: 0 of 5 cuts fail, 1 to look at -> /Volumes/MiniWork/scratch/J2494/s7_v02/picture_qa/PICTURE_QA.md, /Volumes/MiniWork/scratch/J2494/s7_v02/picture_qa/picture_qa_review.jpg

{"frames": 528, "whole": 11.31484603881836, "loop_diff_masked": 9.015830039978027, "open_median_step": 9.089609146118164, "head_matches": [0, 0, 0, 0, 0], "pass": true}
```

---

### 1.2 `HZGTovJu_TQ` — *If You Can't See the Nearest Star, How Far Away Is It?* (Airs Mon 16 Nov 11:30Z)
- **Original export (`mon16_cant_see_nearest_star_v01.mp4`):**
  - Failed rule 24 on first cut at `4.80 s > 3.0 s`; also carried raw YouTube ID `c5AdqQsnnys` under the end-card title at `0:22–0:26` (Ben's 11:20Z board note).
- **Re-cut (`02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/mon16_cant_see_nearest_star/06_Final-Exports/mon16_cant_see_nearest_star_v05.mp4`):**
  - **SHA-256:** `5a2a4c2af8fb2148ad0975ed0d3cc88d329b3bd20ed071eb3626ba1d874d14f3`
  - **Duration:** `26.5 s` (same locked voice and mix, levelled per Chief ruling `#6765128508` to `-14.2 LUFS / -2.2 dBTP`)
  - **What changed:**
    1. Brought the first cut forward from `4.80 s` to `2.40 s` (`<= 3.0 s`).
    2. Removed the raw YouTube ID `c5AdqQsnnys` from the end card (`0:22.70–0:26.50`), leaving only `FULL VIDEO ON THE CHANNEL` above the listing title `The Nearest Star Is One You Can't See (And It Has a Planet)`.
  - **Watch folder copy:** `OWB UAT/026_shorts_first_second_recut_J2494/mon16_cant_see_nearest_star_v05.mp4` (iCloud and NAS).

#### Pasted Gate Outputs (`mon16_cant_see_nearest_star_v05.mp4`)
```text
PASS  mon16_cant_see_nearest_star_v05.mp4  dur=26.5s  audio=-17.9dB  motion=26.34  f0diff=2.08  cut1=2.4s  vo_onset=0.03s  tail_gap=1.40s  vo_src=mix  dhash=400e0616020c3978  visor=0.0
   sheet /Volumes/MiniWork/scratch/orbit_shorts_gate/mon16_cant_see_nearest_star_v05_open_sheet.jpg

WARN   0:05 row s02 v06_152.73.mp4: low detail: edge density 0.0247 < film p5 0.0257
picture QA PASS: 0 of 7 cuts fail, 1 to look at -> 02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/mon16_cant_see_nearest_star/06_Final-Exports/picture_qa_v05/PICTURE_QA.md, 02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/mon16_cant_see_nearest_star/06_Final-Exports/picture_qa_v05/picture_qa_review.jpg
```

---

### 1.3 `kKN8Ale42sE` — *How Far From Earth Is Voyager 1 Right Now?* (Airs Tue 17 Nov 11:30Z)
- **Status:** **Stopped per brief** (*"first find the export whose sha256 matches what is on YouTube and work from that. If none matches, say so and stop on this one."*).
- **Finding:**
  - `UPLOADS.json` and `J0216_UPLOAD_INDEX.json` record the uploaded file SHA-256 (uploaded `2026-10-13T11:11:35Z`) as:
    `9c45c0187274a777a16892b907eac8075950e2824d3748fff5e815ddeac3635a` (`53,755,050` bytes).
  - On `2026-10-17T05:44Z`, job `J0432` overwrote `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/06_Final-Exports/owb_sa_s8_voyager1_v01.mp4` in place with a new render (`sha256: eda8be53430e088f274e55ef9c3178666a9d0b1a4ab1507b9ebfc0f988c0a6e1`, `55,544,439` bytes).
  - Searched the entire Mini (`/Users/benjaminoats`, `/Volumes/MiniWork`), the NAS (`/Volumes/data/studio-live`, `/Volumes/data/mac-mini-archive`, including `owbshorts.tar`), and iCloud `OWB UAT`: every copy on disk and in `owbshorts.tar` has `sha256: eda8be53430e...`. The original `9c45c0187274...` bytes are not kept locally (same class as the `J1320` ruling on `N42gKBbD7pY` / `bSjWiCbB7pY`). Per the brief, stopped on `kKN8Ale42sE`.

---

### 1.4 `cwU_0WWeNZ4` — *If Voyager Needs 75,000 Years, How Far Is the Nearest Star?* (Airs Wed 18 Nov 11:30Z)
- **Original export (`wed18_robot_reach_nearest_star_v01.mp4`):**
  - Failed rule 24 on still open at frame 0 (`f0diff=0.46 < 1.50`); also carried raw YouTube ID `c5AdqQsnnys` under the end-card title at `0:19.80–0:23.60` (Ben's 11:20Z board note).
- **Re-cut (`02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/wed18_robot_reach_nearest_star/06_Final-Exports/wed18_robot_reach_nearest_star_v06.mp4`):**
  - **SHA-256:** `80e4c86df51417db71efb9eaef9097669d6201d41396585acafb8ecbacfd936b`
  - **Duration:** `23.6 s` (same locked voice and mix, levelled per Chief ruling `#6765128508` to `-14.2 LUFS / -2.2 dBTP`)
  - **What changed:**
    1. Replaced the static opening graphic (`0.00–2.83 s`) with the moving Milky Way time-lapse from the 026 long (`v06_11.40.mp4`, `f0diff=1.89 >= 1.50`, `cut1=2.6 s <= 3.0 s`).
    2. Removed the raw YouTube ID `c5AdqQsnnys` from the end card (`0:19.80–0:23.60`), leaving only `FULL VIDEO ON THE CHANNEL` above the listing title `The Nearest Star Is One You Can't See (And It Has a Planet)`.
  - **Watch folder copy:** `OWB UAT/026_shorts_first_second_recut_J2494/wed18_robot_reach_nearest_star_v06.mp4` (iCloud and NAS).

#### Pasted Gate Outputs (`wed18_robot_reach_nearest_star_v06.mp4`)
```text
PASS  wed18_robot_reach_nearest_star_v06.mp4  dur=23.6s  audio=-17.4dB  motion=9.01  f0diff=1.89  cut1=2.6s  vo_onset=0.00s  tail_gap=0.46s  vo_src=mix  dhash=0b2303090c0b0802  visor=0.0
   warn  picture barely changes in the first second (motion 9.0 < 10) — trim the clip's ease-in so frame 0 is already mid-action
   warn  open plate 13 bits from bSjWiCbB7pY (2026-11-13)
   sheet /Volumes/MiniWork/scratch/orbit_shorts_gate/wed18_robot_reach_nearest_star_v06_open_sheet.jpg

WARN   0:22 row end_card end_card_thumb_A.png: low detail: edge density 0.0286 < film p5 0.0306
picture QA PASS: 0 of 7 cuts fail, 1 to look at -> 02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/wed18_robot_reach_nearest_star/06_Final-Exports/picture_qa_v06/PICTURE_QA.md, 02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/wed18_robot_reach_nearest_star/06_Final-Exports/picture_qa_v06/picture_qa_review.jpg
```

---

## 2. Audit of All 24 Scheduled Orbit Shorts for End-Card Raw YouTube IDs

Per Ben's 11:20Z board notes (*"There seems to be a jumble of letters under the title at 0:22 to 0:23"*), all 24 scheduled Shorts were audited:
- **Now clean (`v05` / `v06` built in this job):**
  - `HZGTovJu_TQ` (Mon 16 Nov) — `mon16_cant_see_nearest_star_v05.mp4`: `c5AdqQsnnys` removed.
  - `cwU_0WWeNZ4` (Wed 18 Nov) — `wed18_robot_reach_nearest_star_v06.mp4`: `c5AdqQsnnys` removed.
- **No end card / no YouTube ID (loop-back standalone or clean builds):**
  - `ffYKoNVPoqg` (10 Nov), `B1z2dv7m7Vk` (11 Nov), `gmzaCfJF1gA` (14 Nov, `v01` & `v02`), `kKN8Ale42sE` (17 Nov), and **all 16 scheduled Shorts from 20 Nov (`aAUgIGEuPwQ`) through 16 Dec (`f17XCtUmN-g`)** are clean (none display a raw YouTube video ID on the end card).
- **Only remaining scheduled Shorts that carry a raw YouTube ID on the end card:**
  - `N42gKBbD7tE` (Thu 12 Nov 11:30Z, 025 Dust) and `bSjWiCbB7pY` (Fri 13 Nov 11:30Z, 025 Ingenuity): their `J0432` build scripts rendered `Js6EQJ8qDi8` under the listing title on the end card, and their uploaded MP4s are the `J1320` `knownNoFile` cuts (no kept local copy of the uploaded bytes).

---

## 3. Studio Readback & `UPLOADS.json` Fixes (Nothing Changed on YouTube)

1. **YouTube Studio readback on CDP 9223 (via `reuse_page`):**
   - `bizlhspnVvY` (*Why Will Gliese 710's Comets Arrive After It Has Gone?* `v01`): **Visibility = `Private`** (unscheduled).
   - `xvarZP2aYyE` (*Why Will Gliese 710's Comets Arrive After It Has Gone?* `v04`): **Visibility = `Scheduled`** (`2026-11-30T11:30:00Z`).
2. **`00_Brand/Channel-Setup/social/UPLOADS.json` updated:**
   - Removed the stale `"publishAt": "2026-11-30T11:30:00.000Z"` from `bizlhspnVvY` (`privacyStatus: "private"`).
   - Added the five missing `publishAt` values from `05_Analytics/owb/snapshots/2026-11-10.json`:
     - `B1z2dv7m7Vk`: `"2026-11-11T11:30:00Z"`
     - `bSjWiCbB7pY`: `"2026-11-13T11:30:00Z"`
     - `gmzaCfJF1gA`: `"2026-11-14T11:30:00Z"`
     - `kKN8Ale42sE`: `"2026-11-17T11:30:00Z"`
     - `xvarZP2aYyE`: `"2026-11-30T11:30:00Z"`
