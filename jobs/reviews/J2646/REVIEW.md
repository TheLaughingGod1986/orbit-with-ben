# J2646 — Perceptual Review of Rebuilt 24 November 2026 Supermoon Dated-Event Short `v03` (`J2478`)

- **Reviewer**: `gemini` (`gemini-argon`)
- **Date**: 2026-11-11
- **Parent Job**: `J2478` (`Supermoon dated-event Short (airs Thu 19 Nov): voice-over, build from free NASA footage, all Shorts gates, park for review`)
- **Build Branch & PR**: `codex/J2478-natural-speed` (`f5c5821bc6`, Draft PR `#834`)
- **NAS Delivery Folder**: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_dated_shorts/2026-11-24_supermoon/natural_speed_v03_delivery_20261111/` (all 33 files verified byte-for-byte and by SHA-256 against `DELIVERY_v03_SHA256.json`)
- **Reviewed Master Cut**: `06_Final-Exports/owb_dated_2026_11_24_supermoon_v03.mp4`
  - **SHA-256**: `9b1993364a2858d875b33a97898931a458f084c72711db96c29fe0831aa0b501`
  - **Specs**: `1080×1920` (9:16 vertical), `30 fps`, `551` frames, `18.366667 s` (`17.36 s` natural-speed VO + `1.00 s` forward-loop tail), `45,501,565` bytes
- **Reviewed Cover**: `11_Upload-Package/supermoon_2026_11_24_cover_v03.jpg` (`1080×1920`, `sha256: dd0cd9f6958800c10cef308854f839d6c05f48ecbd4ad266683f3ddbdfc70869`)
- **Advisory Verdict for Chief (`claude`)**: **`KEEP` (0 Fails, 0 Re-edit Items; Ready for Chief `KEEP` Ruling, PR `#834` Merge, and Staging to OWB UAT Watch Folders for Ben's Watch)**

---

## 1. Media Actually Perceived in This Session

Unlike the `v03` assembly session (which inspected stills and ran ASR/gate measurements), this session directly perceived both the moving video and the audio tracks via `read_file`:

1. **Moving Video + Final Soundtrack Mix**:
   - Watched the full `18.367 s` moving video cut (`owb_dated_2026_11_24_supermoon_v03.mp4` via a `540×960` H.264/AAC proxy transcode `v03_proxy.mp4`) and listened to the full-length final audio mix (`v03_mix_24k.wav`) extracted from `owb_dated_2026_11_24_supermoon_v03.mp4`.
2. **Isolated Audio Stems**:
   - Listened to the isolated natural-speed narration stem `02_Voiceover/supermoon_2026_11_24_vo_v02d.wav` (`17.36 s`, `sha256: 75bf38d6eacd20791c6d8fdddd39f288b31fb76e2af6e434bd63a78483aee2f4`).
   - Listened to the isolated SFX stem `07_Edit-Project/assembly_j2478_v03/stem_sfx.wav` (`sha256: 37c5c5dc45d18094e187ccaabc6b0b794c96f91c81f96e4de0e45041f3cf725c`).
   - Listened to the isolated score bed stem `07_Edit-Project/assembly_j2478_v03/stem_bed.wav` (`sha256: ccf574126854e4bf5aea51eb3ea855dc910d318356659be260fc307d1f67e426`).
3. **Full-Resolution `1080×1920` Frame Stills & QA Sheets**:
   - Viewed native `1080×1920` frames extracted across every shot and transition of `owb_dated_2026_11_24_supermoon_v03.mp4`: `0.00 s` (`s01` frame 0), `1.00 s`, `2.00 s`, `2.80 s` (`s01_date`), `4.30 s` (`s02`), `6.00 s` (`s03`), `6.40 s` (`s03`), `8.00 s` (`s04` with title banner), `9.60 s` (`s04` after title banner clears), `11.40 s` (`s06` with shrinking scale bar), `14.10 s` (`s06b` with final scale bar), `16.40 s` (`s07`), `17.90 s` (`loop`), and `18.33 s` (final frame before loop seam).
   - Viewed `11_Upload-Package/supermoon_2026_11_24_cover_v03.jpg`, `qa/cover_thumb_preview.jpg`, `qa/picture/picture_qa_review.jpg`, and `qa/shorts_gate/owb_dated_2026_11_24_supermoon_v03_open_sheet.jpg`.

---

## 2. Perceptual Audio & Voice Review (`supermoon_2026_11_24_vo_v02d.wav` & Final Mix)

1. **Natural Recorded Speed (`1.0×` Throughout) & Chief's 11 Nov `05:54Z` Ruling**:
   - All 12 splice segments in `supermoon_2026_11_24_vo_v02d_EDIT.json` run at `tempo: 1.0` from the locked Trim 1 take `supermoon_2026_11_24_c7_trim1_vo_v01.wav` (`sha256: 95a24bc9c4b1352f333c121e96d88483afd7688229e037ba9a51958feeb9f385`).
   - By ear, Ben's British voice sounds completely natural, warm, and unhurried from frame 0 to the end (`145 WPM`, `-23.9 dB` mean, `-5.1 dB` peak on `vo_check.py`). There is no `atempo` artifact, pitch shift, or rushed syllable anywhere in Sentence 1 or the body.
   - Internal Sentence-1 micro-gaps are `≤ 0.15 s`, `"The"` begins at `0.07 s` (`gate_shorts_open` measures `vo_onset=0.08s`), `"closer"` finishes at **`2.095 s`** (covered by the Chief's explicit spoken-`1.5 s` waiver on `J2478`), the breath after Sentence 1 (*"twenty-fourth. / If Earth..."*) is **`0.18 s`** (`< 0.25 s`), and the pause after *"nickel,"* is **`0.14 s`**.
2. **Restored Date Onset (`"on November 24th"`, `v02d`)**:
   - Restoring `105 ms` (`source 3.475–3.580 s`) ahead of the late Scribe timestamp completely resolved the clipped `"twenty-"` onset that caused `v02c`/`v02` ASR to read `"November 4th"`.
   - Listening to both `supermoon_2026_11_24_vo_v02d.wav` and the final mix in `owb_dated_2026_11_24_supermoon_v03.mp4` at `2.10–3.55 s`, the spoken words **"on November twenty-fourth"** are crisp, natural, and unmistakable. Unprompted `faster-whisper small.en` transcribes `"The moon swings two Earths closer on November 24th."` on the final MP4 mix (`output_asr.json`).
3. **Sound-Alike Word-Check Warnings (`vo_check_v02d.json`)**:
   - `vo_check.py` passes with `0` fails and `2` `sounds_alike: true` warnings at `~0:09.06` and `~0:10.38` (`script 'between us this supermoon passes kilometres up'` vs `heard 'between us this super moon passes kilometers up'`).
   - Listening directly to `0:08.5–0:15.0` confirms two benign transcriber differences: (a) `faster-whisper small.en` normalizes `"Supermoon"` to `"super moon"` and UK `"kilometres"` to US `"kilometers"`, and (b) `vo_check.py` strips digits when diffing word tokens while the narrator clearly speaks **"three hundred and sixty thousand"** between `"passes"` and `"kilometres up"` (`output_asr.json` transcribes `"This super moon passes 360,000 kilometers up."` at `9.84–14.92 s`).
4. **Music Pace Warning (`~120.0 BPM` vs Brief `84–96 BPM`, `music_gate.txt`) & Legacy Comparison Warnings**:
   - `music_gate.py` passes `owb-standalone-shorts_score_bed_v01.mp3` under `music_gate_j1468_chief_waiver.json`.
   - Listening to `stem_bed.wav` and the mixed cut, the score bed is a calm, ambient space synth pad whose light subdivision pulse beat-tracks at double-time (`~120 BPM` = `60 BPM` half-time feel). Perceptually it sits smoothly underneath the voice at `-16.8 dB` integrated mix level with full-runtime coverage and no drop-out across the loop seam. The `OSError` lines in `music_gate.txt` are missing local copies of older Saturn/Jupiter/Black Dwarf files and do not affect this Short.
5. **SFX Stem (`stem_sfx.wav`, `sfx_level.txt`)**:
   - `sfx_kit.py level` passes (`SFX level PASS: VO -21.4 LUFS, SFX -44.8 LUFS, 5 hits`, `23.4 LU` below VO). Listening to `stem_sfx.wav` confirms subtle, low-level whooshes and ink ticks on the scale bar with zero harsh or cartoon stings.

---

## 3. Perceptual Moving-Picture, Shot-by-Shot, and Warning Review (`1080×1920`)

All 4 visual/timing fixes from `J2556` and all provisions of the Chief's 11 Nov `04:37Z` (full-bleed `1080×1920`) and `05:54Z` (natural speed + `s01_date` punch-in + proportional `6.5–9.5 s` title window) rulings are verified in `owb_dated_2026_11_24_supermoon_v03.mp4`:

| Shot | Window (s) | Frames | Spoken Words | Visual Plate & Upscale | Perceptual Inspection (`1080×1920` Stills + Moving Video) |
|---|---:|---:|---|---|---|
| **`s01`** | `0.000–2.100` | `0–63` (`2.10 s`) | *"The Moon swings two Earths closer"* | Native 4K `phases_2026_plain_2160p30.mp4` (`1.32×` upscale) | **PASS (`KEEP`)**: Crisp 4K lunar craters filling the frame (`polish_gate`: `ok`, clearing the `v01` downscale warning), smooth rotation/zoom from frame 0 (`motion=16.65`, `f0diff=4.37`), zero Orbit at frame 0 (`visor=0.0`), hook caption `**TWO EARTHS** CLOSER` at `0.00–2.00 s`. Cuts at `2.100 s` right after `"closer"` ends at `2.095 s` (`≤ 2.8 s`). |
| **`s01_date`** | `2.100–3.667` | `63–110` (`1.57 s`) | *"on November twenty-fourth."* | Tighter native 4K crop of `phases_2026_plain_2160p30.mp4` (`1.54×` upscale) | **PASS (`KEEP`)**: Clean punch-in on the western maria/ray craters (`1.54×` upscale, `polish_gate`: `ok`), continuous motion, lower-third caption `ON NOVEMBER 24TH.` synced to the restored date audio. |
| **`s02`** | `3.667–5.000` | `110–150` (`1.33 s`) | *"If Earth were a nickel,"* | NASA Blue Marble `GSFC_20171208_Archive_e002130` (`1.00×` upscale) on full-bleed dark space | **PASS (`KEEP`)**: Cuts in at `3.667 s` (`≤ 4.8 s`) on *"If Earth were a nickel,"*. Full Blue Marble Earth disc sits on the left with smooth continuous drift over a single unbanded dark-space field (`#182230`) reaching all four edges (`0/37` padded frames). **Full-size inspection of `picture_qa` / `polish_gate` warning (`edge density 0.046 < film p5 0.0462`)**: At `1080×1920` (`frame_4.30s.jpg` and `picture_qa_review.jpg`), the Earth disc itself is at native `1.0×` sharpness with crisp clouds and continents; the whole-frame edge density (`0.0460` vs `0.0462`) is `0.0002` below `p5` solely because the globe is surrounded by clean deep space rather than wall-to-wall lunar craters. |
| **`s03`** | `5.000–7.167` | `150–215` (`2.17 s`) | *"the Moon is a coffee bean."* | Blue Marble Earth + NASA LRO Moon `GSFC_20171208_Archive_e001939` (`1.00×` upscale) | **PASS (`KEEP`)**: Cuts in at `5.000 s` as *"the Moon is a coffee bean."* begins. True `1 : 3.67` diameter Earth+Moon pair side by side on the same full-bleed dark-space field, with **no second Moon behind them** (`polish_gate`: `ok`). Title banner fades in cleanly at `6.500 s`. |
| **`s04`** | `7.167–9.867` | `215–296` (`2.70 s`) | *"Normally thirty Earths fit between us."* | Clean Apollo 11 lunar surface `as11-44-6667` (`1.72×` upscale) | **PASS (`KEEP`)**: Replaces the `v01` Apollo 14 metal instrument box/crosshair with a clean, unlabelled Apollo 11 lunar crater plate (`polish_gate`: `ok`). Holds the Title Banner (`How Close Will the Supermoon Get on November 24?`) across `6.500–9.500 s` (`3.00 s` total) and clears Sentence 4 (`9.870 s`) by **`0.370 s`** (`≥ 0.15 s` Chief ruling). |
| **`s06`** | `9.867–12.867` | `296–386` (`3.00 s`) | *"This Supermoon passes three hundred..."* | Unlabelled NASA SVS 5587 Nov 24 perigee Moon `plain_frame_7864` (`1.24×` upscale) | **PASS (`KEEP`)**: Cuts in at `9.867 s` (`53.7%` of runtime) as the answer begins. The sole `DATA` scale bar animates in inside the `16:9` centre band, counting down from `384,400 KM (30 EARTHS)` toward `360,000 KM (28 EARTHS)` with sub-label `TWO EARTHS CLOSER` while the yellow bar contracts proportionally by the true distance ratio (`93.65%`, leaving a visible grey `2 Earths` delta segment on the right). |
| **`s06b`** | `12.867–15.367` | `386–461` (`2.50 s`) | *"...and sixty thousand kilometres up."* | Apollo 11 lunar surface `as11-44-6667` (`1.72×` upscale) | **PASS (`KEEP`)**: Keeps shot duration `≤ 3.00 s` while the `DATA` scale bar settles on `360,000 KM (28 EARTHS)` / `TWO EARTHS CLOSER` over moving lunar terrain (`polish_gate`: `ok`). |
| **`s07`** | `15.367–17.367` | `461–521` (`2.00 s`) | *"Look east at sunset, as…"* | ISS limb Moon `iss070e062746` (`0.95×` upscale) | **PASS (`KEEP`)**: Full Moon rising above Earth's glowing night/sunset atmosphere limb (`polish_gate`: `ok`), matching *"Look east at sunset, as…"* (last word ends at `17.22 s`). |
| **`loop`** | `17.367–18.367` | `521–551` (`1.00 s`) | *(1.00 s music/visual bridge)* | `phases_2026_plain_2160p30_loop_preroll` (`1.32×` upscale) | **PASS (`KEEP`)**: Smooth `1.00 s` visual and grammatical loop back into Frame 0 (`loop_diff_masked = 4.425`, `open_median_step = 4.849`, `tail_gap = 1.15 s`). |

---

## 4. Pasted Automated Gate Outputs (`v03`)

- **`gate_shorts_open.py check ... --air-date 2026-11-19`**:
  ```text
  PASS  owb_dated_2026_11_24_supermoon_v03.mp4  dur=18.37s  audio=-16.8dB  motion=16.65  f0diff=4.37  cut1=2.1s  vo_onset=0.08s  tail_gap=1.15s  vo_src=/Volumes/MiniWork/scratch/J2478-natural-speed/02_Video-Projects/_dated_shorts/2026-11-24_supermoon/07_Edit-Project/assembly_j2478_v03/stem_vo.wav  dhash=00081d1140401c00  visor=0.0
     full-bleed 0.00s  fills the frame  sharp above/middle/below=None/0.6/None  detail top/centre/bottom=17.44/6.22/7.45  spread top/bottom=61.19/29.46
     full-bleed 0.25s  fills the frame  sharp above/middle/below=None/0.602/None  detail top/centre/bottom=17.9/6.38/11.99  spread top/bottom=56.43/31.68
     full-bleed 0.50s  fills the frame  sharp above/middle/below=None/0.614/None  detail top/centre/bottom=18.06/6.41/11.77  spread top/bottom=51.73/29.9
     full-bleed whole Short  0/19 frames padded at one a second, 0/37 at two a second  padded stretches: none  no end card named in meta
     warn  duration 18.4s outside 22–27s band
  ```
- **`vo_check.py` (`vo_check_v02d.json`)**: `verdict: "PASS"`, `fails: []`, `duration_s: 17.36`, `mean_db: -23.9`, `peak_db: -5.1`, `wpm: 145`.
- **`sfx_kit.py level` (`sfx_level.txt`)**: `SFX level PASS: VO -21.4 LUFS, SFX -44.8 LUFS, 5 hits`
- **`music_gate.py` (`music_gate.txt`)**: `music gate PASS: owb-standalone-shorts_score_bed_v01.mp3, 60.0 s, about 120.0 BPM, brief Pace: 84-96 BPM` (waived under `music_gate_j1468_chief_waiver.json`).
- **`picture_qa.py` & `polish_gate.py`**: `Picture QA: PASS (9 cuts · 0 fail · 1 for Claude to look at full size: 0:04 row supermoon_02_s02 low detail 0.046 < 0.0462)` / `polish gate PASS: 0 of 9 rows failed, 1 to look at`.
- **`short_c37.py` (`short_c37.json`)**: `frames: 551`, `loop_diff_masked: 4.425`, `open_median_step: 4.849`, `head_matches: [0, 0, 0, 0, 0]`.
- **`thumb_preview.py short` (`thumb_preview.txt` & `cover_thumb_preview.jpg`)**: `PASS` (`supermoon_2026_11_24_cover_v03.jpg`, `**24,000 KM** / NEARER`).
- **Plan & Upload Manifest (`02_Video-Projects/_dated_shorts/2026-11-24_supermoon-two-earths-closer.md` & `11_Upload-Package/PACKAGE_MANIFEST.json`)**:
  - `publishAt`: `"2026-11-19T11:30:00Z"` (Thu 19 Nov 2026, 11:30 London, 5 days before the event).
  - `relatedVideoId`: `"2fsQcea-voM"` (*Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone*, OWB `013`).
  - `video`: `"02_Video-Projects/_dated_shorts/2026-11-24_supermoon/06_Final-Exports/owb_dated_2026_11_24_supermoon_v03.mp4"`.
  - `thumbnail`: `"02_Video-Projects/_dated_shorts/2026-11-24_supermoon/11_Upload-Package/supermoon_2026_11_24_cover_v03.jpg"`.

---

## 5. Next Steps for Elected Chief (`claude`)

Per `J2646` and `J2478` (*"Review may advise; Chief owns KEEP/FIX, final approval, packaging panel and merge. Write a review record and update original parent J2478. Only on Chief KEEP copy v03 and cover to the existing OWB UAT watch folders and call jobs.py awaits for Ben."*):

1. **Chief Ruling & Merge**: Rule **`KEEP`** on `J2646` / `J2478` and merge Draft PR `#834` (`codex/J2478-natural-speed`, commit `f5c5821bc6`).
2. **Stage for Ben's Watch (`jobs.py awaits`)**: On Chief `KEEP`, copy `owb_dated_2026_11_24_supermoon_v03.mp4` (`sha256: 9b1993364a2858d875b33a97898931a458f084c72711db96c29fe0831aa0b501`) and `supermoon_2026_11_24_cover_v03.jpg` (`sha256: dd0cd9f6958800c10cef308854f839d6c05f48ecbd4ad266683f3ddbdfc70869`) to the OWB UAT watch folders and call `jobs.py awaits J2478` for Ben's phone watch (deadline: **Wed 18 Nov 2026, 18:00 London** for target publish **Thu 19 Nov 2026, 11:30 London**, Related `2fsQcea-voM`; if missed, no upload).
