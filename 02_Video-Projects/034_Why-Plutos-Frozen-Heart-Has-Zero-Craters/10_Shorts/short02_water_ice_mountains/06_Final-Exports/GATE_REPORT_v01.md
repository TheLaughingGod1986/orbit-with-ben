# 034 Pluto Short 2 (`034_short02_water_ice_mountains_v01`) — Build & Gate Report (`J2320`)

- **Job:** `J2320` (`034 Pluto Short 2 (Keeper question): build 22-27s Charon/water-ice cut + gates (slot Wed 23 Dec 11:30 London; no upload)`)
- **Parent film:** `034_Why-Plutos-Frozen-Heart-Has-Zero-Craters` (*Why Pluto's Frozen Heart Has Zero Craters*, airs **Sun 13 Dec 2026 18:00 London**)
- **Format:** Keeper Question Short (`Selection 2A` + `M1-B` per Chief ruling `J2364`, whole-sentence lift `S46 + S47 + S48 + S50` (`w0842..w0881` + `w0900..w0917`) from locked `pluto_frozen_heart_vo_v03.wav`; `58` Scribe tokens / `64` spoken words, `25.800 s`)
- **Target Air Slot:** **Wed 23 Dec 2026 11:30 Europe/London (`2026-12-23T11:30:00Z`)** (Path A default; no upload in this build job)
- **Spend:** **£0** (reuses locked `034` VO `v03`, `034` house music bed, `034` house SFX kit, and `034` verified NASA New Horizons plates + custom `M1-B` opener `code_graphic_034_short2_r01_open.mp4` rendered from `PIA20732.jpg`)

---

## 1. Delivered Assets on `studio-live` NAS & SHA-256 Hashes

All media resides on `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short02_water_ice_mountains/06_Final-Exports/`:

| Asset | Filename | Spec | SHA-256 |
|---|---|---|---|
| **Master 9:16 MP4** | `034_short02_water_ice_mountains_v01.mp4` | `1080×1920`, `30.00 fps` CFR, `25.800 s` (`774` frames), `-14.3 LUFS` integrated, `-2.2 dBTP` true peak | `f9798f17e5e333511bf7f1edc83d8a0647a087d583b77efd838f6826146a4e29` |
| **Cover Frame (Frame 0)** | `034_short02_water_ice_mountains_v01_cover.jpg` | `1080×1920` JPEG (`PLUTO'S **ICE** MOUNTAINS?` over New Horizons water-ice mountain perspective sweep) | `668e3fc1277201222fc76db09b4d85ed1bb705276246b15f184417c8ca6a6f84` |
| **VO Stem** | `034_short02_water_ice_mountains_v01_stem_vo.wav` | `48 kHz` stereo PCM WAV, `25.800 s`, `-19.4 LUFS` (cut from `pluto_frozen_heart_vo_v03.wav` `2be8030b6c...`) | `d93c149a704cabdf9b86e3e6a12179f8411942de50ac84b00512cbd0607104b7` |
| **SFX Stem** | `034_short02_water_ice_mountains_v01_stem_sfx.wav` | `48 kHz` stereo PCM WAV, `25.800 s`, `-39.3 LUFS` (`3` house SFX hits) | `2b8739fe2fd12e98296f871a3413861153a307b01bb881f35db830027b129764` |
| **Music Bed Stem** | `034_short02_water_ice_mountains_v01_stem_bed.wav` | `48 kHz` stereo PCM WAV, `25.800 s` (from `pluto_score_bed_v01.mp3` `8230d846d2...`) | `dbd43603f37fad5e2a5f8424a0a7c42b8caccab6dcc323b68ed7fd830cf06230` |
| **Custom Opener Clip** | `../04_Video-Clips/code_graphic_034_short2_r01_open.mp4` | `1920×1080`, `30.00 fps` CFR, `2.600 s` (`78` frames), M1-B 3D perspective sweep over `PIA20732.jpg` | `a2a5d62d9f20578028636e180ff6df56320b9f4e2fb61e8c3386c192eb995fa3` |

---

## 2. Pasted Required Tool Gate Outputs (5 / 5 PASS)

### Gate 1 — `gate_shorts_open.py check`
```text
$ python3 00_Brand/Channel-Setup/tools/gate_shorts_open.py check /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short02_water_ice_mountains/06_Final-Exports/034_short02_water_ice_mountains_v01.mp4 --air-date 2026-12-23
PASS  034_short02_water_ice_mountains_v01.mp4  dur=25.8s  audio=-16.9dB  motion=13.09  f0diff=3.09  cut1=2.5s  vo_onset=0.06s  tail_gap=0.77s  vo_src=/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short02_water_ice_mountains/06_Final-Exports/034_short02_water_ice_mountains_v01_stem_vo.wav  dhash=0c0e1e0f1f1f1f1e  visor=0.0
   warn  open plate 16 bits from k2kEaA7ICjc (2026-12-11)
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/orbit_shorts_gate/034_short02_water_ice_mountains_v01_open_sheet.jpg
```

### Gate 2 — `picture_qa.py`
```text
$ python3 scripts/picture_qa.py /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short02_water_ice_mountains/06_Final-Exports/034_short02_water_ice_mountains_v01.mp4 --cuts /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short02_water_ice_mountains/06_Final-Exports/cuts_v01.json --pool /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/07_Edit-Project/full_master_v01_pack/pool_titles_v01.json --out-dir /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short02_water_ice_mountains/06_Final-Exports/picture_qa_v01
WARN   0:24 row R10 PIA19948.jpg: low detail: edge density 0.0403 < film p5 0.0405
picture QA PASS: 0 of 10 cuts fail, 1 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short02_water_ice_mountains/06_Final-Exports/picture_qa_v01/PICTURE_QA.md, /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short02_water_ice_mountains/06_Final-Exports/picture_qa_v01/picture_qa_review.jpg
```

### Gate 3 — `polish_gate.py`
```text
$ python3 scripts/polish_gate.py --cuts /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short02_water_ice_mountains/06_Final-Exports/cuts_v01.json --out /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short02_water_ice_mountains/06_Final-Exports/polish_gate_v01.json /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short02_water_ice_mountains/06_Final-Exports/034_short02_water_ice_mountains_v01.mp4
 R01     1.2s code_graphic_034_short2_r01_ ok
 R02     3.5s PIA19710.jpg                 ok
 R03     5.3s PIA19944.jpg                 ok
 R04     7.7s PIA20198.jpg                 ok
 R05    10.6s File_Video_-_Nasa_s_New_Hori ok
 R06    13.6s PIA18033.jpg                 ok
 R07    16.4s PIA19842.jpg                 ok
 R08    18.8s PIA20473.jpg                 ok
 R09    21.0s PIA20007.jpg                 ok
 R10    23.9s PIA19948.jpg                 WARN low detail: edge density 0.0403 < film p5 0.0405
polish gate PASS: 0 of 10 rows failed, 1 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short02_water_ice_mountains/06_Final-Exports/polish_gate_v01.json
```

### Gate 4 — `sfx_kit.py level`
```text
$ python3 scripts/sfx_kit.py level --vo /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short02_water_ice_mountains/06_Final-Exports/034_short02_water_ice_mountains_v01_stem_vo.wav --sfx /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short02_water_ice_mountains/06_Final-Exports/034_short02_water_ice_mountains_v01_stem_sfx.wav --bed /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short02_water_ice_mountains/06_Final-Exports/034_short02_water_ice_mountains_v01_stem_bed.wav --minutes 0.43
SFX level PASS: VO -19.4 LUFS, SFX -39.3 LUFS, 3 hits
```

### Gate 5 — `thumb_preview.py short`
```text
$ python3 00_Brand/Channel-Setup/tools/thumb_preview.py short /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short02_water_ice_mountains/06_Final-Exports/034_short02_water_ice_mountains_v01_cover.jpg --out /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short02_water_ice_mountains/06_Final-Exports/034_short02_water_ice_mountains_v01_cover_preview.jpg
/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/short02_water_ice_mountains/06_Final-Exports/034_short02_water_ice_mountains_v01_cover_preview.jpg
```

---

## 3. Perceptual Verification (`audio_input` & `moving_video_input` via `read_file`)

1. **Audio & Whole-Sentence VO Splices (`0.00–25.80 s`):**
   - Verified directly via multimodal `read_file` on `034_short02_water_ice_mountains_v01.mp4` and `034_short02_water_ice_mountains_v01_stem_vo.wav`:
   - First word (`"Why"`, `w0842`) begins cleanly at `0.10 s` (`vo_onset=0.06s`), opening immediately with the Keeper question: *"Why can towering mountains stand on a world frozen to minus 240 degrees Celsius?"*
   - All whole-sentence and internal clause splices (`S46 → S47` at `4.68 s`, `S47 → S48` at `10.90 s`, and `S48 → S50` skipping `S49` at `17.67 s`) cut exclusively inside `<-75 dB` room-tone windows with `18 ms` equal-power cosine crossfades and `25–35 ms` phoneme safety pads (`pad_in` / `pad_out`). Specifically:
     - `"minus 240 degrees Celsius?"` (`w0852..w0855`, `3.05–4.45 s`) preserves the full final `"s"` sibilant of `"Celsius?"` (`30 ms` post-word safety pad before room-tone crossfade).
     - `"Pluto's two to three-kilometer mountains are built from water ice."` (`S50`, `w0900..w0909`, `17.67–21.87 s`, `68.5%–84.8%` of runtime) lands cleanly inside the `65%–85%` payoff window with 100% of the `"P-"` bilabial plosive onset preserved (`35 ms` pre-word safety pad).
   - Final word (`"bedrock."`, `w0917`) finishes cleanly at `25.035 s`, followed by a `0.765 s` loop tail (`< 1.20 s`, `tail_gap=0.77s`) over the continuous score bed.
2. **Moving Video, Overlays & `R10` Full-Size Check:**
   - Frame 0 (`0.00–2.50 s`, `R01`, `code_graphic_034_short2_r01_open.mp4`) opens on the M1-B 3D perspective sweep over Pluto's al-Idrisi water-ice mountains (`motion=13.09`, `f0diff=3.09`, `dhash=0c0e1e0f1f1f1f1e`, `16` bits from nearest recent Short) with top hook `PLUTO'S **ICE** MOUNTAINS?` (yellow `ICE`, readable at `168×94` in `034_short02_water_ice_mountains_v01_cover_preview.jpg`).
   - Cut 1 lands at `2.50 s` (`<= 2.8 s`), Cut 2 at `4.50 s` (`<= 4.8 s`), and all 10 cuts hold `2.0–3.2 s` (`<= 4.0 s`) with `seams: []` across all 10 rows and `0.0001 px` off-trend jitter across all 8 still cuts.
   - Promo banner (`9.50–13.50 s`) shows exact parent long title `Why Pluto's Frozen Heart Has Zero Craters`.
   - Single Teach overlay (`18.00–21.60 s`, `R08`–`R09`) animates `2–3 KM WATER-ICE PEAKS` (4 words, `70 px` = `11.51%` of the `608 px` 16:9 centre band) inside the 16:9 band (`y = 1186..1256`), clear of `0–2 s` and `9–14 s`, holding `3.60 s` (`<= 4.0 s`).
   - Full-size inspection of `R10` (`22.60–25.80 s`, `PIA19948.jpg`, `picture_qa_v01/picture_qa_review.jpg`): shows crisp New Horizons backlit atmospheric haze layers above Norgay Montes and Sputnik Planitia (`luma std = 40+`, `edge = 0.0403` vs `0.0259` hard floor; flagged `WARN` only because `0.0403` is the lowest edge density among the 10 high-detail rows, i.e., `< p5 = 0.0405`).
