# J2419 / J2248 v04 Build & Verification Report — `gemini`, 8 November 2026

## 1. Root Cause of Ben's 7 Nov Change (`"0:19 under light speed has a code"`)
- **Frames 0:18–0:21 inspected on `fri06_muons_ground_v03.mp4` (`be63a3d85cadfb4d0fd0387f62dd36dcf9200e5b51942fd91873f1cc677c902c`):**
  - At `16.90–21.05 s` (including `0:19`), the burned-in endcard overlay (`endcard.png`) rendered a 4th line containing the raw 11-character YouTube video ID `rVqgtkBV3jc` in white directly underneath the yellow line `"Light Speed?"`.
  - **Source layer:** `_assemble_fri06_muons_ground_v03.py` line 394:
    ```python
    text_png(WORK / "endcard.png", END_ROWS + [LONG_ID], 980, H * 0.046,
             [WHITE, WHITE, YELLOW, WHITE], stroke=6)
    ```
- **Fix in `_assemble_fri06_muons_ground_v04.py`:**
  - Removed `+ [LONG_ID]` from `endcard.png` so only the 3-line long title `END_ROWS = ["What Happens If", "You Travel Near", "Light Speed?"]` is rendered (`[WHITE, WHITE, YELLOW]`).
  - Changed nothing else: locked VO (`3b17b23c8c476efa240375375ffe738fd8dacd254f622f2cef97152089779e8a`), 22.20 s duration, 6-row plate schedule, captions, music bed, SFX stem, and loop to opening Earth nadir view are preserved identically.

## 2. Deliverables & SHA-256 Hashes
- **`v04` Master (`fri06_muons_ground_v04.mp4`):**
  - Local export: `02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/10_Shorts/fri06_muons_ground/06_Final-Exports/fri06_muons_ground_v04.mp4`
  - UAT path: `OWB UAT/024_fri06_muons_ground_v04/fri06_muons_ground_v04.mp4`
  - **SHA-256:** `06b935f706c8ac3b1ac4d576d22a20193eb0fd742047f36f0be534b7604b0554` (`22.20 s`, `1080x1920`, `30 fps` CFR)
- **Prior Cuts Preserved Intact:**
  - `v01`: `9fc197dcdbcd16d3812a183779b2c8dcba38f67495d5738741b4c6e8f411fd28`
  - `v02`: `768cf1a4f0ae603724eef13c690e0c9495c233b4ecc5f3af0f3d27b5c39a5f08`
  - `v03`: `be63a3d85cadfb4d0fd0387f62dd36dcf9200e5b51942fd91873f1cc677c902c`
- **All 24 UAT files verified in `06_Final-Exports/UAT_v04_SHA256SUMS.json` and `OWB UAT/024_fri06_muons_ground_v04/SHA256SUMS.json`.**

## 3. All 5 Shorts Tool Gates + Full-Video 666-Frame OCR Pass
1. **`gate_shorts_open.py`:** `PASS  fri06_muons_ground_v04.mp4  dur=22.2s  audio=-17.8dB  motion=17.25  f0diff=3.94  cut1=3.0s  vo_onset=0.08s  tail_gap=1.32s  vo_src=/tmp/j2248-vo/vo.mp3  dhash=dc7360b603214413  visor=0.0` (mix `-14.4 LUFS`, `-1.9 dBTP`).
2. **`sfx_kit.py level`:** `PASS: VO -19.3 LUFS, SFX -42.3 LUFS, 2 hits`.
3. **`music_gate.py`:** `PASS: light-speed_score_bed_v01_full.mp3, 526.0 s, about 150.0 BPM, brief Pace: 72-88 BPM`.
4. **`polish_gate.py`:** `PASS: 0 of 6 rows failed, 1 to look at` (same soft-cloud relative edge-density WARN `0.0328 < p5 0.0360` at `16.3 s` on `s05_nhq_b`, previously reviewed KEEP in `J2302`).
5. **`picture_qa.py`:** `PASS: 0 of 6 cuts fail, 1 to look at`.
6. **666-Frame Vision OCR Pass (`ocr_v04.json` / `ocr_v04.txt`):**
   - Ran macOS Vision `VNRecognizeTextRequest` across all 666 extracted frames (`0.000 s` to `22.167 s` at `30 fps`).
   - **`FLAGGED = 0`** (`0` instances of `rVqgtkBV3jc`, file IDs, `NHQ`, `.mp4`, `.png`, or row IDs `s01`–`s06`).
   - Direct visual inspection of `18.0 s`, `19.0 s`, `20.0 s`, `21.0 s` and `fri06_muons_ground_v04_contact.jpg` confirms the 3-line endcard (`What Happens If / You Travel Near / Light Speed?`) is clean above the captions (`THE FULL FILM`, `WHAT HAPPENS IF`, `THE SPEED OF`, `LIGHT?`).

## 4. Hand-Off to Ben's Watch
- Staged `OWB UAT/024_fri06_muons_ground_v04/fri06_muons_ground_v04.mp4` and set `awaits_ben` on `J2248` for `v04`, provisional slot **Sat 21 Nov 2026 11:30 London** (`due 2026-11-21T10:30Z`, `--if-not "do not upload or schedule"`).
- Spend: **£0 / 0 credits**. No upload or schedule performed.
