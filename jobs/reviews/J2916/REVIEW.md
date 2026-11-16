# J2916 Chief Review — 30 November 2026 Moon–Jupiter Close Conjunction Dated-Event Short (`v01`)

- **Job**: `J2916` (`Moon-Jupiter 30 Nov dated-event Short (airs Thu 26 Nov): voice-over, build from free NASA footage, all Shorts gates, park for review`, `kind: assembly`)
- **Reviewer & Elected Acting Chief**: `gemini` (`gemini-argon`, Elected Acting Chief for OWB and HOS per `chief_relay.py status` at `2026-11-16T02:14:26Z`: `claude` out until `2026-11-16T07:50:00Z`, `chief` Grok Bot down until `2026-11-16T02:20:07Z`, `codex` down until `2026-11-17T23:22:00Z`, `gemini` UP)
- **Approved Plan**: `02_Video-Projects/_dated_shorts/2026-11-30_moon-jupiter-conjunction.md` (`Script PASS` in `jobs/reviews/J2830/REVIEW.md`, `15 Nov 2026`, `64e889aafd`)
- **NAS Delivery Folder**: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_dated_shorts/2026-11-30_moon-jupiter` (`56/56` files verified byte-for-byte against `DELIVERY_v01_SHA256.json`)
- **Reviewed Master Cut**: `06_Final-Exports/owb_dated_2026_11_30_moon_jupiter_v01.mp4`
  - **SHA-256**: `b0050a0a3e3a83da004dc62f23fd220d2a7fdd316020b2c9b24b66fdedc11344`
  - **Specs**: `1080×1920` (`9:16` full-bleed `mode: cover`), `30.00 fps` CFR, `585` frames = `19.500 s` (`18.480 s` natural-speed VO + `1.020 s` forward-loop tail)
- **Reviewed Cover**: `11_Upload-Package/moon_jupiter_2026_11_30_cover_v01.jpg` (`1080×1920`, `sha256: ab1244c69986ac3556465229fc82ef7a5436f967edbe1171c73899b4014706dd`, `**2,000X** / FARTHER`)
- **Chief Ruling**: **`KEEP v01` (0 Fails, 0 Re-edit Items). Staged to `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/` and `OWB UAT/WATCH_FULL/` (SHA-256 verified) and armed on the Studio board (`jobs.py awaits J2916`) for Ben's watch by Wednesday, 25 November 2026 at 18:00 London ahead of Thursday, 26 November 2026 at 11:30 London publish (`Related`: `-jmMROGoZCM`).**

---

## 1. Media Directly Perceived in This Session (`audio_input` & `moving_video_input`)

1. **Moving Video + Mixed Soundtrack (`video/mp4`)**:
   - Watched the full `19.500 s` (`0:00–0:19`) moving video sequence and listened to its mixed soundtrack (`owb_dated_2026_11_30_moon_jupiter_v01.mp4` via `540×960` H.264/AAC proxy `v01_proxy.mp4`).
2. **Isolated Audio Stems (`audio/mpeg`)**:
   - Listened directly to the isolated natural-speed narration stem `02_Voiceover/moon_jupiter_2026_11_30_vo_v02.mp3` (`18.48 s`, `sha256: 9ec7411b223bc7d343f55f6aa91bf371d8644fcec9066af8baae9ede2c1f5eeb`), the isolated SFX stem `07_Edit-Project/assembly_j2916_v01/stem_sfx.wav`, and the isolated score bed stem `07_Edit-Project/assembly_j2916_v01/stem_bed.wav`.
3. **Full-Resolution QA Sheets & Cover (`image/jpeg`)**:
   - Inspected `07_Edit-Project/assembly_j2916_v01/qa/picture/picture_qa_review.jpg` (`s04` `PIA26077` full-size plate), `07_Edit-Project/assembly_j2916_v01/qa/shorts_gate/owb_dated_2026_11_30_moon_jupiter_v01_open_sheet.jpg`, `07_Edit-Project/assembly_j2916_v01/qa/cover_thumb_preview.jpg`, and `11_Upload-Package/moon_jupiter_2026_11_30_cover_v01.jpg`.

---

## 2. Perceptual Audio, Voice-Over & Mix Verification (`PASS`)

1. **Natural Recorded Speed (`1.00×`, Zero `atempo`) & Complete-Sentence Ending**:
   - Recorded in 1 take (`275` chars on subscription credits, `47/47` words exact) in Ben Orbit Narrator (`eleven_v3`) and tightened only at verified room-tone pauses (`<-70 dBFS` RMS, `10 ms` qsin joins) to **`18.480 s`** (`153 WPM`, `-23.3 dB` mean, `-4.3 dB` peak).
   - By ear, every word is warm, natural-speed British narration with zero clicks, stumbles, or clipped syllables:
     - `0:00–0:03.9`: *"Jupiter passes one finger from the Moon on November thirtieth."* (Date is crisp and unhurried).
     - `0:04.2–0:07.5`: *"If Earth were a grape, Jupiter is a whole basketball."*
     - `0:07.8–0:10.3`: *"It is forty times wider than our Moon."*
     - `0:10.66–0:16.44`: *"Yet Jupiter sits two thousand times farther, over seven hundred million kilometres away."* (Answer starts at **`10.66 s <= 13.5 s`** `C7` guard).
     - `0:16.82–0:18.44`: *"Look south in the morning sky."* (Complete sentence ending cleanly on `"sky."` with a natural tail fade, complying with Ben's `11 Nov` `J2478` v04 rule).
2. **`vo_check.py` Sound-Alike Note (`PASS`)**:
   - `vo_check.py` passes with `0` fails and `1` `sounds_alike: true` warning at `~0:12.42` (`script 'farther over million kilometres away look south'` vs `heard 'farther over million kilometers away look south'`), which is solely UK `'kilometres'` vs Whisper US `'kilometers'` spelling (`700` is stripped by `vo_check`'s digit tokenizer while spoken clearly as *"seven hundred"*).
3. **Score Bed & House SFX Mix (`PASS`)**:
   - `music_gate.py` passes `jupiter_no_crust_short_bed_v01.mp3` (`30.0 s`, `~66.7 BPM`, matching the `60–80 BPM` brief pace under `05_Music/music_gate_j2916_chief_waiver.json`).
   - `sfx_kit.py level` passes (`VO -20.3 LUFS, SFX -45.8 LUFS, 3 hits`, `25.5 LU` below VO). By ear, the three gentle transition/data ticks and the ambient synth bed sit cleanly under the voice (`-16.7 dB` integrated audio on `gate_shorts_open.py`) with smooth loop continuity across the `1.02 s` tail.

---

## 3. Perceptual Moving-Picture, Shot-by-Shot & Cover Verification (`PASS`)

| Shot | Window (s) | Spoken Words | Visual Plate & Action | Perceptual Verdict |
|---|---:|---|---|---|
| **`s01`** | `0.000–2.567` | *"Jupiter passes one finger from the Moon"* | Full-bleed Juno `PIA22946` cloud bands + rotating 4K SVS #5587 Nov 30 Moon; Hook `**FORTY TIMES** WIDER` (`0.00–2.00 s`) | **`KEEP`**: Fills 100% of the `9:16` frame (`motion=10.65`, `f0diff=3.25`, `visor=0.0`), crisp 3-word hook clear of Shorts chrome. |
| **`s02`** | `2.567–4.200` | *"on November thirtieth."* | SVS #5587 unlabelled 4K Frame `8001` (`2026-11-30T08:00 UTC` waning gibbous Moon) | **`KEEP`**: Sharp sunlit lunar craters with continuous drift (`polish_gate`: `ok`). |
| **`s03`** | `4.200–5.733` | *"If Earth were a grape,"* | NASA Blue Marble Earth (`GSFC_20171208_Archive_e002130`) | **`KEEP`**: Crisp cloud/ocean detail filling the frame with zero badge/overlay (`polish_gate`: `ok`). |
| **`s04`** | `5.733–7.733` | *"Jupiter is a whole basketball."* | Juno `PIA26077` belts & zones + true `11 : 1` Earth disc | **`KEEP`**: Inspected full size in `picture_qa_review.jpg`. The `picture_qa`/`polish_gate` warning (`edge density 0.0304 < film p5 0.0348`) occurs because smooth gas-giant cloud bands have softer gradients than the 8 sharp lunar-crater/starfield shots setting `p5`; visually the Juno swirls and `11:1` Earth disc are crisp and clean. |
| **`s05`** | `7.733–10.500` | *"It is forty times wider than our Moon."* | Unlabelled `40 : 1` real-body diameter scale (`PIA21974` + LRO Moon); Title Banner `9.10–12.60 s` | **`KEEP`**: Clear `40:1` scale contrast (`polish_gate`: `ok`). Title banner (`Why Is Jupiter Beside the Moon on November 30?`) sits inside `9–14 s` and clears the `13.20 s` `DATA` overlay by **`0.60 s`**. |
| **`s06`** | `10.500–13.667` | *"Yet Jupiter sits two thousand times farther,"* | NASA LRO Moon craters (`GSFC_20171208_Archive_e001939`) | **`KEEP`**: High-detail lunar highland craters (`polish_gate`: `ok`). |
| **`s07`** | `13.667–16.667` | *"over seven hundred million kilometres away."* | Apollo 11 curved sunlit lunar horizon (`as11-44-6667`) + distant Jupiter + sole `DATA` distance bar (`13.20–16.30 s`) | **`KEEP`**: Animated `DATA` bar inside the `16:9` centre band clearly contrasts `MOON: 373,000 KM` with `JUPITER: 754 MILLION KM` (`2,000 TIMES FARTHER`) (`polish_gate`: `ok`). |
| **`s08`** | `16.667–18.500` | *"Look south in the morning sky."* | ISS Expedition 70 twilight limb (`iss070e062746`) + Nov 30 waning gibbous Moon and Jupiter side by side | **`KEEP`**: Clean pre-dawn horizon view matching the skywatching call to action (`polish_gate`: `ok`). |
| **`loop`** | `18.500–19.500` | *(1.02 s music/picture loop tail)* | `PIA22946` loop pre-roll (`7`-frame crossfade into `s01` frame 0) | **`KEEP`**: Smooth visual and musical bridge back into Frame 0 (`loop_diff_masked=3.828`, `open_median_step=3.743`, `tail_gap=1.06s`, `0/20` & `0/39` padded frames). |
| **Cover** | `11_Upload-Package/` | `**2,000X** / FARTHER` | `moon_jupiter_2026_11_30_cover_v01.jpg` (`1080×1920`) | **`KEEP`**: Passes `thumb_preview.py short` (`qa/cover_thumb_preview.jpg`), legible at `168 px`, complements `**FORTY TIMES** WIDER` frame-0 hook without duplicating it. |

---

## 4. Follow-Up Executed

1. Copied `owb_dated_2026_11_30_moon_jupiter_v01.mp4` (`sha256: b0050a0a3e3a83da004dc62f23fd220d2a7fdd316020b2c9b24b66fdedc11344`) and `moon_jupiter_2026_11_30_cover_v01.jpg` (`sha256: ab1244c69986ac3556465229fc82ef7a5436f967edbe1171c73899b4014706dd`) to `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/` and `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/WATCH_FULL/` and verified all 4 SHA-256 checksums.
2. Armed `jobs.py awaits J2916` on the Studio board (due **Wednesday, 25 November 2026 at 18:00 London** for **Thursday, 26 November 2026 at 11:30 London** publish; if missed, do not upload).
