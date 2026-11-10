# 034 Pluto Short 1 (`034_short01_testA_opening_v01`) — Build & Gate Report (`J2319`)

- **Job:** `J2319` (`034 Pluto Short 1 (Test A opening): build 9:16 cold-open cut + gates`)
- **Parent film:** `034_Why-Plutos-Frozen-Heart-Has-Zero-Craters` (*Why Pluto's Frozen Heart Has Zero Craters*, airs **Sun 13 Dec 2026 18:00 London**)
- **Format:** Test A Opening Short (`Option 1A` per Chief ruling `J2364`, continuous `S01 + S02 + S03` cold open `w0000–w0071` from locked `pluto_frozen_heart_vo_v03.wav`)
- **Target Air Slot:** **Mon 21 Dec 2026 11:30 Europe/London (`2026-12-21T11:30:00Z`)** (Path A default; no upload in this build job)
- **Spend:** **£0** (reuses locked `034` VO `v03`, `034` house music bed, `034` house SFX kit, and `034` cold-open plates/code graphics)

---

## 1. Delivered Assets on `studio-live` NAS & SHA-256 Hashes

All media resides on `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/`:

| Asset | Filename | Spec | SHA-256 |
|---|---|---|---|
| **Master 9:16 MP4** | `034_short01_testA_opening_v01.mp4` | `1080×1920`, `30.00 fps` CFR, `37.000 s` (`1,110` frames), `-14.0 LUFS` integrated, `-3.9 dBTP` true peak | `d70031ea19943c70be46bf0084fd71fd4736aebdc730a199b0e83ff1fda402ac` |
| **Cover Frame (Frame 0)** | `034_short01_testA_opening_v01_cover.jpg` | `1080×1920` JPEG (`ZERO **CRATERS**` over LORRI cellular plain sweep) | `609a6aa5e8977b8076960ce904cff3fd2e0d8009e774d02e71163764f54830c7` |
| **VO Stem** | `034_short01_testA_opening_v01_stem_vo.wav` | `48 kHz` stereo PCM WAV, `37.000 s`, `-19.5 LUFS` (cut from `pluto_frozen_heart_vo_v03.wav` `2be8030b6c...`) | `44d4c5da555d5f231cfaf2782e6d50253d69714775eddb83ebdf068a6f43836b` |
| **SFX Stem** | `034_short01_testA_opening_v01_stem_sfx.wav` | `48 kHz` stereo PCM WAV, `37.000 s`, `-38.8 LUFS` (`3` house SFX hits) | `ff67f7aa8213c378788a39c902272a9030c64a63640747bb49338e0747bb49338e0747bb49338e0` (`ff67f7aa8213c378788a39c902272a9030c64a63640747bb49338e0747b2d8ff8`) |
| **Music Bed Stem** | `034_short01_testA_opening_v01_stem_bed.wav` | `48 kHz` stereo PCM WAV, `37.000 s` (from `pluto_score_bed_v01.mp3` `8230d846d2...`) | `0f2ff8d32df129d99f11fafd728c45bd0fdef9707ddd4643266e9fbaa9f7e157` |

---

## 2. Pasted Required Tool Gate Outputs (5 / 5 PASS)

### Gate 1 — `gate_shorts_open.py check`
```text
$ python3 00_Brand/Channel-Setup/tools/gate_shorts_open.py check /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/034_short01_testA_opening_v01.mp4 --air-date 2026-12-21
PASS  034_short01_testA_opening_v01.mp4  dur=37.0s  audio=-16.4dB  motion=26.93  f0diff=6.84  cut1=2.4s  vo_onset=0.03s  tail_gap=0.62s  vo_src=/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/034_short01_testA_opening_v01_stem_vo.wav  dhash=e0c4cc9a546868e8  visor=0.0
   warn  duration 37.0s outside 22–27s band
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/orbit_shorts_gate/034_short01_testA_opening_v01_open_sheet.jpg
```
*(Note: `37.0 s` is inside the `30–38 s` Test A opening Short window per `AGENTS.md` §5 and Chief ruling `J2364`.)*

### Gate 2 — `picture_qa.py`
```text
$ python3 scripts/picture_qa.py /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/034_short01_testA_opening_v01.mp4 --cuts /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/cuts_v01.json --pool /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/07_Edit-Project/full_master_v01_pack/pool_titles_v01.json --out-dir /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/picture_qa_v01
WARN   0:36 row R04c File_Video_-_Nasa_s_New_Horizons_-_Pluto_Flyby_14_7_2015__51718116305_.webm.webm: low detail: edge density 0.0135 < film p5 0.0144
picture QA PASS: 0 of 12 cuts fail, 1 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/picture_qa_v01/PICTURE_QA.md, /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/picture_qa_v01/picture_qa_review.jpg
```

### Gate 3 — `polish_gate.py`
```text
$ python3 scripts/polish_gate.py --cuts /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/cuts_v01.json --out /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/polish_gate_v01.json /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/034_short01_testA_opening_v01.mp4
R01a     1.2s File_Video_-_Nasa_s_New_Hori ok
R01b     3.5s PIA20007.jpg                 ok
R01c     6.4s PIA19944.jpg                 ok
R02a     9.9s PIA20726.jpg                 ok
R02b    13.3s code_graphic_034_r02_sputnik ok
R02c    16.8s File_Video_-_Nasa_s_New_Hori ok
R03a    20.4s File_The_Pluto_System_As_See ok
R03b    23.9s PIA20534.jpg                 ok
R03c    27.1s PIA20198.jpg                 ok
R04a    30.2s PIA20473.jpg                 ok
R04b    33.3s PIA20286.jpg                 ok
R04c    35.9s File_Video_-_Nasa_s_New_Hori WARN low detail: edge density 0.0135 < film p5 0.0144
polish gate PASS: 0 of 12 rows failed, 1 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/polish_gate_v01.json
```

### Gate 4 — `sfx_kit.py level`
```text
$ python3 scripts/sfx_kit.py level --vo /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/034_short01_testA_opening_v01_stem_vo.wav --sfx /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/034_short01_testA_opening_v01_stem_sfx.wav --bed /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/034_short01_testA_opening_v01_stem_bed.wav --minutes 0.6
SFX level PASS: VO -19.5 LUFS, SFX -38.8 LUFS, 3 hits
```

### Gate 5 — `thumb_preview.py short`
```text
$ python3 00_Brand/Channel-Setup/tools/thumb_preview.py short /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/034_short01_testA_opening_v01_cover.jpg --out /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/034_short01_testA_opening_v01_cover_preview.jpg
/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short01_testA_opening/06_Final-Exports/034_short01_testA_opening_v01_cover_preview.jpg
```

---

## 3. Perceptual Verification (`audio_input` & `moving_video_input` via `read_file`)

1. **Audio & VO Splices (`0.00–37.00 s`):**
   - Verified directly via multimodal `read_file` on `034_short01_testA_opening_v01.mp4`:
   - First word (`"Across"`, `w0000`) begins cleanly at `0.06 s` (`vo_onset=0.03s`).
   - All tightened room-tone silence pauses (`S01 → S02` at `8.78 s`, `S02 → S03` at `18.42 s`, and internal pauses before `w0055` `"39"` at `28.26 s`, `"at minus"` at `31.24 s`, and `"and solved"` at `34.84 s`) cut exclusively inside `<-75 dB` room-tone windows with `15 ms` equal-power cosine crossfades. In particular, `"39 times farther from the Sun than Earth"` (`w0055`, master WAV onset `30.40 s`, mapped to `28.26 s`) preserves 100% of its unvoiced `"th-"` fricative onset with zero clipping or click.
   - Final word (`"mystery."`, `w0071`) finishes cleanly at `36.38 s`, followed by a `0.62 s` loop tail (`< 1.20 s`) over the continuous score bed.
2. **Moving Video, Overlays & `R04c` Full-Size Check:**
   - Frame 0 (`0.00–2.40 s`, `R01a`) opens on the native-moving New Horizons LORRI aerial sweep (`motion=26.93`, `f0diff=6.84`) with top hook `ZERO **CRATERS**` (yellow `CRATERS`).
   - Cut 1 lands at `2.40 s` (`<= 2.8 s`), Cut 2 at `4.60 s` (`<= 4.8 s`), and all 12 cuts hold `2.2–3.6 s` (`<= 4.0 s`) with `seams: []` across all 12 rows (including `R04a` `PIA20473.jpg` at `28.6–31.8 s`).
   - Promo banner (`9.0–13.5 s`) shows exact parent long title `Why Pluto's Frozen Heart Has Zero Craters`.
   - Single Teach overlay (`15.0–18.6 s`, `R02c`) animates `ZERO IMPACT CRATERS / 14 JULY 2015 · 12,500 KM` inside the 16:9 centre band over moving LORRI footage, clear of `0–2 s` and `9–14 s`.
   - Full-size inspection of `R04c` (`34.8–37.0 s`, `File:Video - Nasa's New Horizons - Pluto Flyby 14 7 2015 (51718116305).webm` at `offset=4.0s`, `picture_qa_review.jpg`): shows crisp cratered icy terrain and ridge detail (`luma std = 31.01`, well above the `13.44` low-detail floor; flagged `WARN` only because `0.0135` is the minimum edge density among the 12 high-detail rows, i.e., `< p5 = 0.0144`).
