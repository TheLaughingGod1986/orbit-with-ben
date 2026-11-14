# J2222 — Cut & Packaging Review: `J01` Journey Film 01 (`J01_Journey_v03.mp4` + `j01_v03_pack` + 3 Thumbnails)

- **Job**: `J2222` (`J01 Journey Film 01: review v03 cut and three thumbnails before Ben watch`)
- **Film / Stage**: `J01` (`02_Video-Projects/J01_Journey-To-Every-World`, stage `edit`)
- **Predecessors**: `J2146` (`1e9ba89b33`), `J2784` / `J2786` (`J2784_PACE_v01.json`), `J2799` (`905fe020ec`), `J2221` & `J2815` (`9ebb517772`, `jobs/reviews/J2815/CHIEF_CLOSEOUT.md`; Grok Bot PASS Option A `#6874618419`, reiterated `#6874993329`)
- **Reviewed By**: `gemini` (`gemini-argon` specialist worker on Mac mini)
- **Reviewed At**: `2026-11-14T10:59Z`
- **Capabilities & Perception Disclosure**:
  - Recorded via `python3 scripts/chief_relay.py capabilities --agent gemini --available ""`: **no `audio_input` or `moving_video_input` is claimed by this worker session.**
  - All findings below come from deterministic tool checks (`ffprobe`, `ffmpeg ebur128` / `loudnorm`, `picture_qa.py`, `polish_gate.py` metrics, `music_gate.py`, `sfx_kit.py level`, `thumb_preview.py --score`, word-timestamp boundary verification) and direct visual inspection of rendered still contact sheets (`sheet_7_cards.jpg`, `sheet_7_maps.jpg`, `picture_qa_review.jpg`, `thumb_preview_long.jpg`, and the three `1920×1080` thumbnails).
  - Under `AGENTS.md` and `jobs/reviews/J2815/CHIEF_CLOSEOUT.md` (`9ebb517772`), Ben's final UAT supplies the human watch/listen check; absent worker perception alone does not stall this review. All tool gates PASS (`0` blocking failures).

---

## 1. Summary Table of Reviewed Artifacts & Gate Results

| Artifact / Check | Path & Checksum | Measured Result | Verdict |
|---|---|---|---|
| **Final Master Cut (`v03`)** | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/J01_Journey-To-Every-World/07_Edit-Project/J01_Journey_v03.mp4`<br>(`1,984,936,766` B, SHA-256 `bb93ea1343acde3f9f2f438e04b471e4c13044892b6b0861453839e14c71bb32`) | `3502.300 s` (`58:22.30`), `1920×1080` `h264`, `24/1` fps (`84,055` video packets), stereo `aac` `48 kHz` (`164,170` frames), clean decode (`exit 0`) | **`PASS`** |
| **Final Encoded Loudness & True Peak** | Independent full-file `ebur128=peak=true` + `loudnorm` pass on `J01_Journey_v03.mp4` | **`I = -14.0 LUFS`** (`loudnorm input_i = -14.02 LUFS`), **`TPK = -0.7 dBFS`** (`loudnorm input_tp = -0.75 dBTP`), **`LRA = 4.1 LU`** *(supersedes pre-normalization `-14.33 LUFS / -0.44 dBTP` input readout)* | **`PASS`** |
| **Seven Joins & Linking VO Boundaries** | `07_Edit-Project/J01_Journey_v01_timeline.json` + `J2784_PACE_v01.json` + source `vo_words.json` / `stt_raw.json` (`023–029`) | All 8 linking VO takes have `>= 0.55 s` lead-in (except Cold Open at `0.00 s`) and `0.65–18.22 s` tail silence (`> 0.50 s` `xfade`); all 19 master slice boundaries have `0.32–1.16 s` sentence-end breath padding (`0` clipped words) | **`PASS`** |
| **Single Subscribe Beat (Part 1 Only)** | Word-timestamp scan across all 7 part slices (`027`, `023`, `025`, `028`, `026`, `024`, `029`) | Exactly **1** subscribe beat in the film: Part 1 (`027`) at `164.90–169.42 s` (`03:37.56 – 03:42.08` film time). All 6 duplicate beats in Parts 2–7 and all standalone agenda/outro lines are trimmed out | **`PASS`** |
| **18-Second End Hold** | Segment 22 (`close`, `3463.229–3502.300 s`) vs `j01_vo_08_closing` word end | Last spoken word (`"us."`) ends at `20.66 s` of Take 8 (`3484.44 s` film time), leaving **`17.86 s` (`~18.0 s`)** of picture + music hold (`3484.44–3502.30 s`) for YouTube end screens | **`PASS`** |
| **7 Chapter Cards & 7 Distance Maps** | Visual inspection of `sheet_7_cards.jpg` & `sheet_7_maps.jpg` (`code_graphic_J01_map_00`..`06`, `seg_card_1`..`7`) | Lifted navy background (`mean luma 49.30–189.92 >= 28.0`), real NASA Blue Marble Earth cutout + `NASA` credit, `<= 4` words per label, `0` typos or back-to-back full-frame graphics | **`PASS`** |
| **Linking SFX & Bed Level (`sfx_kit.py level`)** | `07_Edit-Project/j01_v03_pack/sfx_level.json` (`linking_{vo,sfx,bed}.wav`) | **`PASS`**: `vo_integrated: -16.7 LUFS`, `sfx_integrated: -44.1 LUFS` (`27.4 LU` below VO), `hits: 9`, `fails: []`, `warns: []`; linking music ducked `-15.5 dB` (`13.8–17.3 LU` under VO) | **`PASS`** |
| **Laid Score & Provenance (`music_gate.py`)** | `05_Music/j01_journey_laid_score_v02.wav` (`3502.378 s`, SHA-256 `0fd2c87674d99cb462f02eb3f3773bae297dd2c8a6c525fa9b6c4d79f9136ad4`) + `j01_journey_laid_score_v02_manifest.json` | **`PASS`**: `3502.4 s`, `-34.25 LUFS`, longest gap `3.9 s <= 6.0 s`, `fail: []`, waiver `music_gate_J01_chief_waiver.json` (`reused` only). `80.0 BPM` first-120s readout vs `Pace: 66-70 BPM` & 13 iCloud-evicted UAT warnings documented below | **`PASS`** |
| **Picture QA & Polish Checks (`22 rows`)** | `07_Edit-Project/j01_v03_pack/PICTURE_QA.md`, `picture_qa.json`, `picture_qa_review.jpg` | **`PASS`**: `0` fails, `15` macro-row warnings inspected full size; `53:37` (`3216.81 s`) luma lift verified (`mean = 44.55 >= 28.0`, `p95 = 68.0 >= 50.0`); `0` split seams across all 22 rows | **`PASS`** |
| **Three Thumbnails (`1920×1080` & `168×94`)** | `08_Thumbnail/j01_v01/thumb_{A,B,C}*.jpg` + `thumb_preview.py long --score` | **`PASS`** on all 3: `thumb_A` (`sat=120.1, nb=10%`), `thumb_B` (`sat=120.5, nb=2%`), `thumb_C` (`sat=155.6, nb=4%`); no Orbit, top-band 3-token hooks, legible at `168×94` | **`PASS`** |

---

## 2. Detailed Verification Findings

### 2.1 Final Encoded Loudness & True Peak (`J01_Journey_v03.mp4`)

As noted in `jobs/reviews/J2815/CHIEF_CLOSEOUT.md` (`9ebb517772`), the values stored in `REPAIR.json` (`input_i: "-14.33"`, `input_tp: "-0.44"`) were pass-1 measurements of the pre-normalized mux (`J01_Journey_v03_preloud.mp4`) before `repair_v03.py` applied two-pass linear `loudnorm` (`I=-14:TP=-1.5:LRA=11:linear=true`).

Running a full-file measurement directly on the final encoded `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/J01_Journey-To-Every-World/07_Edit-Project/J01_Journey_v03.mp4`:

```text
[Parsed_ebur128_0] Summary:
  Integrated loudness:  I:         -14.0 LUFS   (Threshold: -24.7 LUFS)
  Loudness range:       LRA:         4.1 LU     (LRA low: -17.0 LUFS, LRA high: -12.9 LUFS)
  True peak:            Peak:       -0.7 dBFS

[Parsed_loudnorm_1]
{
  "input_i" : "-14.02",
  "input_tp" : "-0.75",
  "input_lra" : "4.10",
  "input_thresh" : "-24.74",
  "output_i" : "-14.17",
  "output_tp" : "-1.50",
  "output_lra" : "4.00",
  "output_thresh" : "-24.88",
  "normalization_type" : "dynamic",
  "target_offset" : "0.17"
}
```

- **Result**: Final encoded master sits right on the house target at **`-14.02 LUFS` integrated** (`-14.0 LUFS` EBU R128) and **`-0.75 dBTP` true peak** (`-0.7 dBFS` EBU R128), with a tight **`4.10 LU`** loudness range across all 58 minutes.

---

### 2.2 Decode, Frame Timing, and 18-Second End Hold

1. **Container & Stream Timing**:
   - Video stream (`#0:0`): `h264 (High)`, `1920×1080`, `SAR 1:1 DAR 16:9`, `r_frame_rate = 24/1`, `time_base = 1/12288`, `84,055` packets (`3502.291667 s`).
   - Audio stream (`#0:1`): `aac (LC)`, `48,000 Hz`, stereo, `164,170` frames (`3502.300000 s`, `196.6 kbps`).
   - Inter-packet PTS intervals: across `84,054` steps, `84,052` are exact `1/24 s` (`0.041667 s`). At the `v02` stream-copy splice entry (`3215.791667 s`–`3215.916667 s`, just before the `3216.55–3217.10 s` Betelgeuse luma-lift patch), packets `77179` and `77181` have a one-frame B-pyramid boundary step (`+0.083333 s` and `0.000000 s`, logging two non-monotonic DTS lines when demuxed to `-f null`), which decodes with **exit code `0`** and zero dropped or corrupted frames.
2. **18-Second End Hold**:
   - Segment 22 (`close`) spans `3463.229 s → 3502.300 s` (`39.071 s` on screen).
   - Take 8 (`j01_vo_08_closing.wav`, `20.88 s`, placed after a `0.55 s` lead-in at segment start) ends its last word (`"us."`) at `20.66 s` into the WAV = `21.21 s` into Segment 22 (`3484.44 s` film time).
   - From `3484.44 s` to `3502.30 s`, the master holds moving picture and ambient score for **`17.86 s` (`~18.0 s`)** (`18.22 s` nominal before container tail alignment) with clean decode (`exit 0`).

---

### 2.3 Seven Part Joins, Linking VO Word Boundaries & Single Subscribe Beat

1. **8 Linking VO Takes vs `0.50 s` Crossfades (`J2784_PACE_v01.json`)**:
   - Every linking take starts after the `0.50 s` incoming `xfade` (except Take 1 at `0.00 s` film start) and finishes with `0.65 s – 18.22 s` of clean breath before the outgoing `0.50 s` `xfade` into its `3.0 s` Chapter Card:
     - **Take 1 (`cold`, `0.000–50.162 s`)**: first word `"Every"` at `0.00 s`; last word `"sitting."` ends `0.84 s` before cut (`> 0.50 s`).
     - **Take 2 (`bridge1`, `495.662–515.642 s`)**: first word `"Earth's"` at `0.55 s`; last word `"sky."` ends `0.75 s` before cut (`> 0.50 s`).
     - **Take 3 (`bridge2`, `1008.059–1029.635 s`)**: first word `"On"` at `0.55 s`; last word `"decade."` ends `0.98 s` before cut (`> 0.50 s`).
     - **Take 4 (`bridge3`, `1496.385–1517.445 s`)**: first word `"Beyond"` at `0.55 s`; last word `"way."` ends `0.65 s` before cut (`> 0.50 s`).
     - **Take 5 (`bridge4`, `1971.278–1989.848 s`)**: first word `"Gliese"` at `0.55 s`; last word `"dark."` ends `0.71 s` before cut (`> 0.50 s`).
     - **Take 6 (`bridge5`, `2462.265–2483.401 s`)**: first word `"At"` at `0.55 s`; last word `"home."` ends `0.70 s` before cut (`> 0.50 s`).
     - **Take 7 (`bridge6`, `2947.234–2967.896 s`)**: first word `"Even"` at `0.55 s`; last word `"possible."` ends `0.84 s` before cut (`> 0.50 s`).
     - **Take 8 (`close`, `3463.229–3502.300 s`)**: first word `"From"` at `0.55 s`; last word `"us."` ends at `21.21 s` into segment (`17.86 s` end hold).

2. **7 Reused Master Parts & Single Subscribe Beat**:

| Part | Source Master | Slice Windows Kept (`s`) | Word Boundary Padding (`in` / `out`) | Trimmed Agenda & Outro Lines | Subscribe Beat Status |
|---|---|---|---|---|---|
| **Part 1 (`52.66–495.66 s`)** | `027` Earth's Spin | `[0.00..443.50]` | `in: +0.16s` (`"Right"`), `out: +0.68s` (`"down."`) | No agenda line in `027` v01m; tail `>443.50s` silent hold trimmed | **KEPT (1 of 1)**: `164.90–169.42 s` (`03:37.56–03:42.08` film time) |
| **Part 2 (`518.14–1008.06 s`)** | `023` Venus | `[0.00..35.80]`, `[43.20..212.20]`, `[218.20..504.80]` | `pad_in: 0.08–0.56s`, `pad_out: 0.32–0.58s` | Agenda `[35.80..43.20]` & outro `[>504.80]` (*"Next week, what happens to your clock..."*) trimmed | **TRIMMED** (`[212.20..218.20]`, `0` hits in kept slices) |
| **Part 3 (`1032.14–1496.39 s`)** | `025` Mars | `[0.00..29.80]`, `[40.80..224.50]`, `[231.00..483.20]` | `pad_in: 0.12–0.68s`, `pad_out: 0.34–0.86s` | Agenda `[29.80..40.80]` & outro `[>483.20]` (*"Next week, how far is the nearest star?"*) trimmed | **TRIMMED** (`[224.50..231.00]`, `0` hits in kept slices) |
| **Part 4 (`1519.95–1971.28 s`)** | `028` Gliese 710 | `[0.00..30.80]`, `[42.20..204.20]`, `[209.80..469.80]` | `pad_in: 0.12–0.58s`, `pad_out: 0.44–0.66s` | Agenda `[30.80..42.20]` & silent tail `[>469.80]` trimmed | **TRIMMED** (`[204.20..209.80]`, `0` hits in kept slices) |
| **Part 5 (`1992.35–2462.27 s`)** | `026` Nearest Star | `[0.00..20.50]`, `[32.80..224.40]`, `[232.00..491.30]` | `pad_in: 0.08–0.96s`, `pad_out: 0.34–1.16s` | Agenda `[20.50..32.80]` & silent tail `[>491.30]` trimmed | **TRIMMED** (`[224.40..232.00]`, `0` hits in kept slices) |
| **Part 6 (`2485.90–2947.23 s`)** | `024` Light Speed | `[0.00..28.30]`, `[41.60..213.10]`, `[220.00..483.00]` | `pad_in: 0.10–0.42s`, `pad_out: 0.42–0.62s` | Agenda `[28.30..41.60]` & outro `[>483.00]` (*"Next week, could a robot survive on Mars?"*) trimmed | **TRIMMED** (`[213.10..220.00]`, `0` hits in kept slices) |
| **Part 7 (`2970.40–3463.23 s`)** | `029` Betelgeuse | `[0.00..22.10]`, `[37.20..242.20]`, `[247.60..514.80]` | `pad_in: 0.08–0.54s`, `pad_out: 0.32–0.70s` | Agenda `[22.10..37.20]` & silent tail `[>514.80]` trimmed | **TRIMMED** (`[242.20..247.60]`, `0` hits in kept slices) |

---

### 2.4 Chapter Cards & Outward Distance Maps (`sheet_7_cards.jpg`, `sheet_7_maps.jpg`)

- **7 Chapter Cards (`seg_card_1.mp4` .. `seg_card_7.mp4`)**:
  - Visually verified on `/Volumes/MiniWork/scratch/J2221/qa/sheet_7_cards.jpg`:
    1. `PART ONE — THE GROUND MOVING UNDER YOUR FEET · 0 KM` (`mean=49.91, p95=65.0`)
    2. `PART TWO — THE TWIN THAT LOST ITS WATER · 40 MILLION KM` (`mean=49.41, p95=65.0`)
    3. `PART THREE — THE RED WORLD FULL OF QUIET MACHINES · 225 MILLION KM` (`mean=50.20, p95=65.0`)
    4. `PART FOUR — THE STAR HEADING FOR OUR OUTER EDGE · 13,000 AU` (`mean=50.06, p95=65.0`)
    5. `PART FIVE — FOUR LIGHT-YEARS THROUGH THE DARK · 4.24 LIGHT-YEARS` (`mean=50.00, p95=65.0`)
    6. `PART SIX — WHEN YOUR CLOCK SLOWS DOWN · 99% LIGHT SPEED` (`mean=49.66, p95=65.0`)
    7. `PART SEVEN — THE DYING GIANT THAT MADE US · 600 LIGHT-YEARS` (`mean=49.56, p95=65.0`)
- **7 Outward Distance Maps (`code_graphic_J01_map_00` .. `06`)**:
  - Visually verified on `/Volumes/MiniWork/scratch/J2221/qa/sheet_7_maps.jpg`:
    - Real Blue Marble Earth cutout at left (with `NASA` bottom-left corner credit), lifted dark-navy grid (`mean luma >= 49.3`), animated gold distance axis / clock-rate bars, and `<= 4`-word top labels matching the spoken VO (`OUTWARD FROM EARTH` / `SUNLIGHT 8 MINUTES`, `40 MILLION KM` / `95% EARTH'S WIDTH`, `225 MILLION KM` / `127 MINUTES`, `13,000 AU` / `1.3 MILLION YEARS`, `4.24 LIGHT-YEARS` / `75,000 YEARS`, `99% LIGHT SPEED` / `7× SLOWER`, `600 LIGHT-YEARS` / `764× THE SUN`).

---

### 2.5 Score Provenance, Unreadable Music-Comparison Warnings & `80 BPM` vs Brief `66–70 BPM`

1. **Reconstructed-Score Provenance (`05_Music/j01_journey_laid_score_v02.wav`)**:
   - SHA-256 `0fd2c87674d99cb462f02eb3f3773bae297dd2c8a6c525fa9b6c4d79f9136ad4` (`672,456,654` bytes, `3502.378 s`, `-34.25 LUFS` integrated, longest rolling gap `3.9 s` at `1228.6 s` <= `6.0 s`).
   - Built by `02_Video-Projects/J01_Journey-To-Every-World/07_Edit-Project/build_laid_score_v02.py` and documented in `05_Music/j01_journey_laid_score_v02_manifest.json`:
     - Uses the exact 15 ducked Option A linking/card beds (`026` `nearest-star_score_bed_v01_full.wav` on `cold`, `card1`, `bridge4`, `card5`, `bridge6`, `card7`, `close`; `023` `venus_score_bed_v01_full.mp3` on `bridge1`, `card2`, `bridge2`, `card3`; `024` `light-speed_score_bed_v01_full.mp3` on `bridge3`, `card4`, `bridge5`, `card6`) at `-15.5 dB` under VO and `-6.0 dB` on cards.
     - Uses the 7 inherited source score beds (`027` `earth-spin_score_take2_straight_v01j.wav` `446.3 s` SHA-256 `f63005243f5e140859e438305c1ec2365662d1e4511391fd9f04d7b53155c0b6` restored from `/Volumes/data/mac-mini-archive/owbextra.tar`, plus `023`, `025`, `028`, `026`, `024`, `029` beds) trimmed to the exact `PART_SLICES` windows and gains of the inherited master cuts, joined with `0.50 s` `acrossfade`. No source master is double-scored.

2. **Unreadable Music-Comparison Warnings (`music_gate.json`)**:
   - `music_gate.py` recorded `verdict: "PASS"`, `fail: []`, and `13` warnings of the form `reused: couldn't read <file> to compare (OSError); download it or pass --others` on old files in `~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT` (`saturn_long_vo_v02_LISTEN.wav`, `jupiter-vo.mp3`, `jupiter-music.mp3`, `friday_black_dwarf_short_vo_v01_LISTEN.wav`, `saturn_long_vo_v02_LISTEN.m4a`, `monday_saturn_short_vo_v02_how_long.wav`, `saturn_long_vo_v03_tightened.m4a`, `monday_saturn_short_vo_v01_LISTEN.wav`, `saturn_long_vo_v03b_tightened_LOCK.m4a`, `saturn_long_vo_v03b_tightened_LOCK.wav`, `saturn_long_vo_v01_LISTEN.wav`, `monday_saturn_short_vo_v02_how_long.mp3`, `saturn_long_vo_v03_tightened.wav`).
   - Those 13 files are iCloud-evicted dataless `.icloud` placeholders (`11` VO files + `1` legacy Jupiter music file). Direct chroma-similarity check against all readable `05_Music` beds on `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/` confirms `0` non-parent matches above `0.80` (max similarity is `0.742` on `027` `earth-spin_score_bed_v02_fit.wav` and `0.740` on `026` `nearest-star_score_bed_v01.mp3`, which are the Option A / Part 1 parent stems covered by `05_Music/music_gate_J01_chief_waiver.json`).

3. **`80.0 BPM` Estimate vs Brief `Pace: 66-70 BPM` (Existing Waiver Covers `reused` Only)**:
   - `music_gate.json` reports `"bpm": 80.0` against `"brief_pace": "Pace: 66-70 BPM"`, while `05_Music/music_gate_J01_chief_waiver.json` waives `"checks": ["reused"]` only (not `"pace"`).
   - Why `music_gate.py` measured `80.0 BPM` without a `pace:` warning: `music_gate.py` runs `tempo(decode(bed, 120))` on the first `120 s` of `j01_journey_laid_score_v02.wav`. In that `0–120 s` window, `0.0–52.66 s` is the Cold Open + Card 1 (`026` ambient pad, `66.7 BPM` on its own) and `52.66–120.0 s` is the opening `67.3 s` of Part 1 (`027` `earth-spin_score_take2_straight_v01j.wav`, `80.0 BPM` on its own). Because `80.0 BPM <= 70 * 1.15 = 80.5 BPM` (the 15% beat-tracker tolerance in `music_gate.py` line 210), `music_gate.py` did not emit a `pace:` warning. Per `CHIEF_CLOSEOUT.md` (`9ebb517772`), this `80.0 BPM` vs `66–70 BPM` readout is explicitly documented for Chief and Ben's watch/listen.

---

### 2.6 Review of All 15 `picture_qa.py` Warnings & Polish Metrics Across All 22 Rows

Because `cuts.json` lists the 22 macro-segments of the stitched Journey timeline (`seg_cold`, 7 `seg_card_N`, 7 `seg_partN_MMM`, 6 `seg_bridge_N`, `seg_close`), `picture_qa.py` emits a `reuse: on screen >15s in a row` warning on all 15 non-card macro-segments (the 7 `3.0 s` chapter cards are `<15 s`). Inside the linking segments, the animated maps (`code_graphic_J01_map_00`..`06`) alternate with graded NASA/spacecraft plates; inside Parts 1–7, each locked master (`023–029`) already passed its own per-shot `picture_qa.py` and `polish_gate.py`.

All 15 warning frames on `picture_qa_review.jpg` were inspected full size alongside the 22-row polish metrics on `J01_Journey_v03.mp4`:

| Row | Film Time | Segment | `picture_qa.py` Warning(s) | Sampled Frame & Visual Inspection (`picture_qa_review.jpg`) | Polish Metrics (`mean`, `p95`, `std`, `edge`, `seams`) |
|---|---|---|---|---|---|
| **1** | `0:25` (`25.08 s`) | `seg_cold.mp4` | `on screen 50.2s` | `code_graphic_J01_map_00` (`OUTWARD FROM EARTH`), real Blue Marble Earth + `NASA` credit on lifted navy | `mean=49.67, p95=66.0, std=21.97, edge=0.0198, seams=[]` |
| **3** | `4:34` (`274.16 s`) | `seg_part1_027.mp4` | `on screen 443.0s` | Approved `027` Omni Orbit sunrise coastal hill shot with bottom-left `CGI` credit | `mean=134.12, p95=207.0, std=53.91, edge=0.0362, seams=[]` |
| **4** | `8:26` (`505.65 s`) | `seg_bridge_1.mp4` | `on screen 20.0s` | Graded Magellan radar / Venus surface terrain plate | `mean=128.04, p95=169.0, std=23.94, edge=0.1557, seams=[]` |
| **6** | `12:43` (`763.10 s`) | `seg_part2_023.mp4` | `on screen 489.9s` | Approved `023` Venus photodissociation graphic (`SUNLIGHT SPLITS WATER / ESCAPES TO SPACE / HEAVY STAYS`) | `mean=54.63, p95=191.0, std=46.67, edge=0.0418, seams=[]` |
| **7** | `16:59` (`1018.85 s`) | `seg_bridge_2.mp4` | `on screen 21.6s` | Deep Space Network dish under twilight clouds | `mean=49.30, p95=153.0, std=43.09, edge=0.0455, seams=[]` |
| **9** | `21:04` (`1264.26 s`) | `seg_part3_025.mp4` | `on screen 464.2s` | Approved `025` Mars Exploration Rover solar-deck hardware close-up | `mean=105.47, p95=196.0, std=49.20, edge=0.1131, seams=[]` |
| **10** | `25:07` (`1506.91 s`) | `seg_bridge_3.mp4` | `on screen 21.1s` | Solar System / Oort trajectory graphic on lifted navy grid | `mean=71.46, p95=115.0, std=27.94, edge=0.0731, seams=[]` |
| **12** | `29:06` (`1745.61 s`) | `seg_part4_028.mp4` | `on screen 451.3s` | Approved `028` Omni Orbit examining icy Oort Cloud comet | `mean=30.12, p95=108.0, std=31.94, edge=0.0453, seams=[]` |
| **13** | `33:01` (`1980.56 s`) | `seg_bridge_4.mp4` | `on screen 18.6s` | Graded Milky Way / Rho Ophiuchi dust lanes starfield plate | `mean=96.01, p95=201.0, std=52.88, edge=0.0755, seams=[]` |
| **15** | `37:07` (`2227.31 s`) | `seg_part5_026.mp4` | `on screen 469.9s` | Approved `026` high-resolution lunar craters plate | `mean=150.56, p95=223.0, std=42.69, edge=0.0517, seams=[]` |
| **16** | `41:13` (`2472.83 s`) | `seg_bridge_5.mp4` | `on screen 21.1s` | Relativistic clock-rate comparison graphic on lifted navy starfield | `mean=56.20, p95=94.0, std=25.64, edge=0.0614, seams=[]` |
| **18** | `45:17` (`2716.57 s`) | `seg_part6_024.mp4` | `on screen 461.3s` | Approved `024` `On Earth (16 years)` vs `On board (2.4 years)` clock graphic | `mean=56.15, p95=106.0, std=30.37, edge=0.0537, seams=[]` |
| **19** | `49:18` (`2957.57 s`) | `seg_bridge_6.mp4` | `on screen 20.7s`; `edge 0.0146 < p5 0.0149` | Bright solar photosphere disk (`How a Giant Star Dies`), naturally smooth solar limb (`std=42.27 >= 13.44`) | `mean=189.92, p95=208.0, std=42.27, edge=0.0146, seams=[]` |
| **21** | `53:37` (`3216.81 s`) | `seg_part7_029.mp4` | `on screen 492.8s`; `std 15.04 < 18.0`; `edge 0.0044 < p5` | Lifted ESO night-sky fade (`ESO · CC BY 4.0` credit); passes near-black (`mean=44.55 >= 28.0, p95=68.0 >= 50.0`) and `STD_FLOOR` (`15.04 >= 13.44`) | `mean=44.55, p95=68.0, std=15.04, edge=0.0044, seams=[]` |
| **22** | `58:03` (`3482.90 s`) | `seg_close.mp4` | `on screen 39.3s` | Concentric supergiant nucleosynthesis shells (`Less than 1 second`) on lifted navy starfield | `mean=103.11, p95=222.0, std=67.36, edge=0.0526, seams=[]` |

*(Rows 2, 5, 8, 11, 14, 17, 20 are the seven `3.0 s` chapter cards, all with `mean=49.41–50.20, p95=65.0, std=22.69–25.31, seams=[]`.)*

---

### 2.7 Three Thumbnails at `1920×1080` and `168×94` (`08_Thumbnail/j01_v01/`)

Ran `python3 00_Brand/Channel-Setup/tools/thumb_preview.py long ... --score` and visually inspected all three `1920×1080` images and `thumb_preview_long.jpg` (`168×94` side-by-side):

| Thumbnail | `thumb_preview.py --score` | HOOK (`<= 3` tokens) | BAND (`y = 6%–22%`) | GRADE (`sat >= 100`, `nb <= 30%`) | PHONE (`168×94`) & House Rules |
|---|---|---|---|---|---|
| **`thumb_A_real_venera_mars.jpg`** | **`PASS`** (`sat=120.1, near_black=10%`) | **`464°C` TO `-60°C`** (yellow `464°C`) | Top-left/centre clear band, off main foreground | **`PASS`** (`120.1`, `10%`) | **`PASS`** — crisp split surface contrast (*Venera 13* amber Venus basalt left / grey planetary surface right), no Orbit, clear of bottom-right badge |
| **`thumb_B_bright_supergiant_scale.jpg`** | **`PASS`** (`sat=120.5, near_black=2%`) | **`764×` OUR SUN** (yellow `764×`) | Top-left clear band | **`PASS`** (`120.5`, `2%`) | **`PASS`** — bright orange/blue stellar nebula background breaking dark template, real Blue Marble Earth lower-left (`ESA/NASA, ESO and Danny LaCrue · CC BY 4.0`), no Orbit |
| **`thumb_C_outward_worlds_lineup.jpg`** | **`PASS`** (`sat=155.6, near_black=4%`) | **`EARTH` TO ORION** (yellow `EARTH`) | Top-left clear band | **`PASS`** (`155.6`, `4%`) | **`PASS`** — four circular worlds lined up left-to-right on lifted dark navy, legible at `168×94`, no Orbit *(uses `EARTH TO ORION` rather than draft `8 WORLDS OUT`, matching the 7-part film)* |

---

## 3. Ben Watch Queue (`awaits_ben`)

All tool gates PASS (`0` blocking failures). Per the `J2222` brief (*"After agent QA, queue Ben watch; no upload or scheduling authorization"*) and `jobs/reviews/J2815/CHIEF_CLOSEOUT.md` (`9ebb517772`), `J2222` is queued for Ben's final UAT watch (`awaits_ben`) with a 720p R2 streaming proxy (`owb-j01-v03`) registered in `05_Analytics/kanban/watch_uploads.json` and `~/.config/studio-kanban/watch_uploads.json`. No upload, scheduling, or privacy change is performed.
