# 033 Uranus — Active Short #1 (`033_short01_testA_opening_v01.mp4`) Build & Gate Report (`J2317`)

- **Job:** `J2317` (`gemini` worker · 8 Nov 2026)
- **Parent Film:** `033_Why-This-Planet-Has-21-Year-Winters` (*Why Knocked-Sideways Uranus Has 21-Year Winters*, airs **Wed 9 Dec 2026 at 18:00 London**)
- **Format:** Test A Opening Short (`05_Analytics/tests/SHORTS_TESTS.md` + `LEARNINGS.md` #17: first `30–38 s` of the long master reframed to `9:16`, ending on the central question the long answers)
- **Target Air Slot:** **Fri 18 Dec 2026 at 11:30 Europe/London (`2026-12-18T11:30:00Z`)** [Path A Default] / **Sat 12 Dec 2026 at 11:30 London** [Path B in-week swap option]
- **Title (Listing & `9.0–13.5 s` On-Screen Card):** **Why Does Knocked-Sideways Uranus Have 21-Year Winters?**
  - *Alt Title:* *What Would You See at the North Pole of Knocked-Sideways Uranus?*
- **Spend:** **£0 / 0 credits** (reuses locked `02_Voiceover/uranus_vo_v01.wav`, £0 house-synthesised chapter-shaped score bed `05_Music/uranus_score_bed_v01.mp3`, £0 house SFX kit `06_Sound-Effects/kit_v01`, and `J2300`/`J2299` verified 033 cold-open plates and code graphics).
- **Upload Status:** **Not uploaded** (per `J2317` brief: build, run all tool gates, and hand to `kind: review`, then `jobs.py awaits` for Ben's phone watch).

---

## 1. Export & Asset Hashes (SHA-256)

| Asset | Path | SHA-256 |
|---|---|---|
| **Short #1 Master MP4 (`36.48 s`, `912` frames @ `25 fps` CFR, `1080×1920`)** | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short01_testA_opening_v01.mp4` (and `10_Shorts/033_short01_testA_opening/06_Final-Exports/033_short01_testA_opening_v01.mp4`) | `7eca95258582b93f6b822e182bf64db8d6e31d95f3710b4479182df4f5182ca7` |
| **Frame 0 Still (`0.30 s`)** | `.../10_Shorts/033_short01_testA_opening_v01_frame0.jpg` | `2843841116a8da0c7bb87c45277d3b19bc2fa07cb2c0257cafcb2b6292fd6a9a` |
| **Cover Still (`21-YEAR / WINTERS?`)** | `.../10_Shorts/033_short01_testA_opening_v01_cover.jpg` | `83a6685be7323dece7863b01c34380ce0e15ddcb4f5b34a4d200f1586bd0ea06` |
| **Locked Parent VO (`uranus_vo_v01.wav`)** | `.../02_Voiceover/uranus_vo_v01.wav` | `3d73576e0c20be9030546db7bc71ea0107602d5e5fbdde37cba28c7d5b43f460` |
| **033 Score Bed (`uranus_score_bed_v01.mp3`, `629.40 s`, `70.6 BPM`)** | `.../05_Music/uranus_score_bed_v01.mp3` | `47f68d66c4ef7b0287c4939b14e7d906582309ca2a3354c3c262daa7e21309f0` |
| **14-Shot Visual QA Sheet** | `.../10_Shorts/033_short01_testA_opening_v01_review_14shots.jpg` | Mirrored to `10_Shorts/` and `06_Final-Exports/` |
| **OWB UAT Mirror (NAS & iCloud)** | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/033_shorts_v01/033_short01_testA_opening_v01.mp4` & `~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/033_shorts_v01/033_short01_testA_opening_v01.mp4` | `7eca95258582b93f6b822e182bf64db8d6e31d95f3710b4479182df4f5182ca7` |

---

## 2. Spec & Pacing Compliance (`SHORTS_PLAN_v01.md` §3 + `OWB-2026-11-E1`)

- **Spoken VO Lift (`90 words`, `0.08–35.38 s`, `0` split words across all 13 cuts):**
  - Contiguous cold open `R01`–`R06` (`0.100–30.980 s` in `uranus_vo_v01.wav`): *"At the North Pole of Uranus, the seventh planet in orbit around our sun, what would you see when the sun sinks below the horizon? A single winter night that lasts twenty-one Earth years. While Earth spins at a twenty-three point four four degree tilt, Uranus is tipped at ninety-seven point seven seven degrees, more than four times Earth's tilt, and nearly at a right angle to its orbit, rolling around the sun on its side like a ball."*
  - Plus `0.24 s` breath and the central question from `R09` (`49.320–53.500 s`): *"How did an entire giant planet get knocked onto its side?"* (`LEARNINGS.md` #17).
- **Frame-0 Hook (`0.00–2.00 s`):** `21-YEAR` (white) / `NIGHT` (`#FFE000` yellow), `132 px` Arial Black over isotropic `9:16` moving sideways Uranus rotation composite (`r01_sourced_composite_v01_silent.mp4` + `PIA01280.jpg` + `weic2332a_hires.jpg`, `dhash=192a812022030b07`, zero overlap with standalone Short `ZpEA8stoSPA`).
- **On-Screen Parent/Short Title (`9.00–13.50 s`):** `Why Does Knocked-Sideways / Uranus Have / 21-Year Winters?` (`58 px` Arial Black, inside the `16:9` centre band `y=656..1264`, over text-free polar winter shadow sweep `R03a` and dark crescent `R03b` — zero background text collision).
- **Single Teach Overlay (`18.20–22.00 s`):** `URANUS TILT: 97.77° (> 4× EARTH)` (`bbox=[101, 1184, 978, 1241]`, inside `16:9` centre band, clear of `0–2 s` hook and `9–14 s` title) over clean 9:16-framed Earth `23.44°` vs Uranus `97.77°` axial tilt protractor gauge (`R05a`).
- **End Card (`35.44–36.48 s`, `1.04 s` tail `< 1.20 s` lock):** `Why Knocked-Sideways / Uranus Has / 21-Year Winters` (white) + `Full film on the channel` (yellow) over `frame0` loop hold.
- **Pacing Locks (`OWB-2026-11-E1`):**
  - `Cut 1 = 2.36 s <= 2.80 s`
  - `Cut 2 = 4.36 s <= 4.80 s`
  - Max shot duration `= 4.00 s <= 4.00 s` (`14` shots across `36.48 s`, mean `2.61 s/shot`)
  - `motion_0_1s = 13.11 >= 12.0`, `f0diff = 4.64 >= 3.5`, `visor_frac = 0.0`
  - Audio loudness: VO `-16.3 LUFS`, bed `-34.2 LUFS`, SFX `-38.3 LUFS` (`6` hits), AAC delivery `-14.1 LUFS` / `-2.2 dBTP`.

### 14-Shot Cut Table (`033_short01_testA_opening_v01_cuts.json`)

| # | Row | Timeline (`s`) | Dur (`s`) | Source | Visual Description |
|---:|---|---|---|---|---|
| 1 | `R01a` | `0.00–2.36` | `2.36` | `r01_sourced_composite_v01_silent.mp4` | Isotropic 9:16 reframe of sideways `97.77°` Uranus rotation time-lapse (`PIA18182` + `weic2310a` + `PIA01280` cloud motion) |
| 2 | `R01b` | `2.36–4.36` | `2.00` | `PIA01280.jpg` | Hubble Space Telescope false-colour view of Uranus cloud bands and vertical rings |
| 3 | `R02` | `4.36–8.16` | `3.80` | `PIA01391.jpg` | Voyager 2 Uranus turquoise crescent terminator in natural colour |
| 4 | `R03a` | `8.16–11.88` | `3.72` | `PIA00032_left_globe.jpg` | Text-free 21-year polar winter night shadow sweep across Voyager 2 cyan Uranus globe (under `9.0–13.5 s` title) |
| 5 | `R03b` | `11.88–13.88` | `2.00` | `PIA00346.jpg` | Voyager 2 parting view of Uranus dark winter hemisphere crescent |
| 6 | `R04a` | `13.88–15.84` | `1.96` | `PIA18033.jpg` | Apollo 17 Blue Marble Earth (`offset=0.0`) |
| 7 | `R04b` | `15.84–18.20` | `2.36` | `PIA18033.jpg` | Apollo 17 Blue Marble Earth closer push (`offset=12.0`) |
| 8 | `R05a` | `18.20–22.20` | `4.00` | `code_graphic_033_r05_tilt_gauge.mp4` | Animated Earth `23.44°` vs Uranus `97.77°` axial tilt gauge + single Teach pill `URANUS TILT: 97.77° (> 4× EARTH)` |
| 9 | `R05b` | `22.20–25.00` | `2.80` | `PIA00143.jpg` | Voyager 2 back-lit Uranus ring system |
| 10 | `R06a` | `25.00–28.00` | `3.00` | `weic2310a_unannotated.png` | JWST NIRCam sideways Uranus rings and bright north polar cap (`offset=0.0`) |
| 11 | `R06b` | `28.00–31.08` | `3.08` | `weic2310a_unannotated.png` | JWST NIRCam inner ring + polar cap push (`offset=12.0`) |
| 12 | `R09a` | `31.08–33.56` | `2.48` | `PIA02963_borderless.jpg` | Hubble Space Telescope Uranus outer rings and moons (borderless crop) |
| 13 | `R09b` | `33.56–35.44` | `1.88` | `PIA18182.jpg` | Voyager 2 Uranus full globe in natural colour |
| 14 | `R01_loop` | `35.44–36.48` | `1.04` | `frame0_hold_033_short01_testA_opening.png` | Frame-0 match hold under end card (`Why Knocked-Sideways Uranus Has 21-Year Winters`) |

---

## 3. Verbatim Tool Gate Outputs (All PASS)

### Gate 1: `gate_shorts_open.py check`
*(Note: `duration 36.5s outside 22–27s band` is an expected informational warning for a `30–38 s` Test A opening Short per `AGENTS.md` Lesson 5 & `SHORTS_TESTS.md`; exit code `0` PASS.)*
```
PASS  033_short01_testA_opening_v01.mp4  dur=36.48s  audio=-17.0dB  motion=13.11  f0diff=4.64  cut1=2.36s  vo_onset=0.08s  tail_gap=1.10s  vo_src=/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short01_testA_opening/06_Final-Exports/033_short01_testA_opening_v01_vo.wav  dhash=192a812022030b07  visor=0.0
   warn  duration 36.5s outside 22–27s band
   sheet /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short01_testA_opening/06_Final-Exports/033_short01_testA_opening_v01_open_sheet.jpg
```

### Gate 2: `picture_qa.py`
```
WARN   0:06 row R02 PIA01391.jpg: low detail: edge density 0.0097 < film p5 0.0102
picture QA PASS: 0 of 14 cuts fail, 1 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short01_testA_opening/06_Final-Exports/033_short01_testA_opening_v01_picture_qa/PICTURE_QA.md, /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short01_testA_opening/06_Final-Exports/033_short01_testA_opening_v01_picture_qa/picture_qa_review.jpg
```

### Gate 3: `polish_gate.py`
```
R01a     1.2s r01_sourced_composite_v01_si ok
R01b     3.4s PIA01280.jpg                 ok
 R02     6.3s PIA01391.jpg                 WARN low detail: edge density 0.0097 < film p5 0.0102
R03a    10.0s PIA00032_left_globe.jpg      ok
R03b    12.9s PIA00346.jpg                 ok
R04a    14.9s PIA18033.jpg                 ok
R04b    17.0s PIA18033.jpg                 ok
R05a    20.2s code_graphic_033_r05_tilt_ga ok
R05b    23.6s PIA00143.jpg                 ok
R06a    26.5s weic2310a_unannotated.png    ok
R06b    29.5s weic2310a_unannotated.png    ok
R09a    32.3s PIA02963_borderless.jpg      ok
R09b    34.5s PIA18182.jpg                 ok
R01_loop    36.0s frame0_hold_033_short01_test ok
polish gate PASS: 0 of 14 rows failed, 1 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short01_testA_opening/06_Final-Exports/033_short01_testA_opening_v01_polish_gate.json
```

### Gate 4: `sfx_kit.py level` & `music_gate.py`
```
SFX level PASS: VO -16.3 LUFS, SFX -38.3 LUFS, 6 hits
music gate PASS: uranus_score_bed_v01.mp3, 629.4 s, about 70.6 BPM, brief Pace: 66-76 BPM
```

### Gate 5: `thumb_preview.py short` (Frame 0 & Cover)
```
/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short01_testA_opening/06_Final-Exports/033_short01_testA_opening_v01_frame0_preview.jpg
PASS  033_short01_testA_opening_v01_frame0.jpg  saturation=98.4  near_black=1%
/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short01_testA_opening/06_Final-Exports/033_short01_testA_opening_v01_cover_preview.jpg
PASS  033_short01_testA_opening_v01_cover.jpg  saturation=128.1  near_black=2%
```
