# J2870 — 033 Uranus Active Shorts 1 & 2 (`v02`) 5-Part Multimodal Review

- **Date:** 2026-11-15
- **Reviewer:** `gemini` (`Gemini 4 Argon (High)`, `audio_input` + `moving_video_input` verified via `scripts/chief_relay.py capabilities`)
- **Standard:** `jobs/reviews/J2829/RULING.md` (5-part multimodal review standard)
- **Prerequisite Fix Job:** `J2869` (resolving all blocking items from `jobs/reviews/J2400/REVIEW.md`)
- **Verdict:** **`KEEP` (`PASS` on all 5 parts for both `033_short01_testA_opening_v02.mp4` and `033_short02_ice_giant_surface_v02.mp4`)** — staged in `OWB UAT/033_shorts_v02/` and armed via `jobs.py awaits J2870` for Ben's phone watch. Zero YouTube uploads until Ben approves.

---

## 1. Executive Summary & Staging Verification

| Short | Master Path (`studio-live` / NAS `OWB UAT` / iCloud `OWB UAT`) | Byte Size | SHA-256 | Duration / Frames | Air Slot | Verdict |
|---|---|---:|---|---|---|---|
| **Short #1 (Test A Opening)** | `02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short01_testA_opening_v02.mp4` | `44,005,614 B` | `db6a23420952151244161c7be209cdebd0440f3ce4aef314c1ce9fc6a3f9d203` | `36.480 s` (`912` frames @ `25 fps` CFR) | Fri 18 Dec 2026 11:30Z | **`KEEP` (`PASS`)** |
| **Short #2 (Keeper Question)** | `02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short02_ice_giant_surface_v02.mp4` | `25,844,387 B` | `279c9531f2c89d16fb37e285b6ef981e8db7bf8d2dd1c297b2940bf07daf5468` | `27.480 s` (`687` frames @ `25 fps` CFR) | Sat 19 Dec 2026 11:30Z | **`KEEP` (`PASS`)** |

### Three-Location Staging Parity (`studio-live` vs NAS vs iCloud Drive)
All three copies of both `.mp4` files were hashed and byte-checked directly:
1. **Working store (`studio-live`):**
   - `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short01_testA_opening_v02.mp4` — `44,005,614` bytes (`db6a23420952151244161c7be209cdebd0440f3ce4aef314c1ce9fc6a3f9d203`)
   - `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short02_ice_giant_surface_v02.mp4` — `25,844,387` bytes (`279c9531f2c89d16fb37e285b6ef981e8db7bf8d2dd1c297b2940bf07daf5468`)
2. **NAS UAT (`/Volumes/data/mac-mini-archive/OWB UAT/033_shorts_v02/`):**
   - `033_short01_testA_opening_v02.mp4` — `44,005,614` bytes (`db6a23420952151244161c7be209cdebd0440f3ce4aef314c1ce9fc6a3f9d203`)
   - `033_short02_ice_giant_surface_v02.mp4` — `25,844,387` bytes (`279c9531f2c89d16fb37e285b6ef981e8db7bf8d2dd1c297b2940bf07daf5468`)
3. **iCloud Drive UAT (`~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/033_shorts_v02/`):**
   - `033_short01_testA_opening_v02.mp4` — `44,005,614` bytes (`db6a23420952151244161c7be209cdebd0440f3ce4aef314c1ce9fc6a3f9d203`)
   - `033_short02_ice_giant_surface_v02.mp4` — `25,844,387` bytes (`279c9531f2c89d16fb37e285b6ef981e8db7bf8d2dd1c297b2940bf07daf5468`)

---

## 2. Part 1 — Automated Gate Verification on Exact `v02` Masters

All 7 automated gate tools were executed directly on the `studio-live` `v02` master files:

| Gate Tool | Short #1 (`033_short01_testA_opening_v02.mp4`) | Short #2 (`033_short02_ice_giant_surface_v02.mp4`) | Result |
|---|---|---|---|
| `gate_shorts_open.py check <mp4> --air-date YYYY-MM-DD` | **`PASS` (rc=0):** `dur=36.48s audio=-17.0dB motion=13.11 f0diff=4.64 cut1=2.36s vo_onset=0.08s tail_gap=0.96s dhash=192a812022030b07 visor=0.0` · `full-bleed whole Short: 0/37 frames padded at one a second, 0/73 at two a second · padded stretches: none · end card 35.6-36.5s judged apart` (`test_a: true` in `_meta.json`, `"end_card": {"start_s": 35.56, "len_s": 0.92}`). | **`PASS` (rc=0):** `dur=27.48s audio=-16.6dB motion=16.81 f0diff=4.26 cut1=1.88s vo_onset=0.15s tail_gap=0.56s dhash=ffc1d4614ee15e31 visor=0.0` · `full-bleed whole Short: 0/28 frames padded at one a second, 0/55 at two a second · padded stretches: none · end card 27.0-27.5s judged apart` (`"end_card": {"start_s": 27.0, "len_s": 0.48}` in `_meta.json`). | **`PASS` (both)** |
| `picture_qa.py <mp4> --cuts <cuts.json> --pool <pool.json>` | **`PASS` (rc=0):** `0 of 14 cuts fail` (`max upscale 1.98x <= 2.35x`, `0` repeated stills). Relative 5th-percentile advisory `R06b weic2310a_unannotated.png` (`edge density 0.0115`, well above the `0.0080` absolute floor) inspected full-size via `read_file` on `picture_qa_review.jpg`: sharp JWST NIRCam Uranus ring system and bright polar cap. | **`PASS` (rc=0):** `0 of 11 cuts fail` (`max upscale 1.95x <= 2.35x`, `0` repeated stills). Relative 5th-percentile advisory `R51a PIA18182.jpg` (`edge density 0.0111`, well above the `0.0080` floor) inspected full-size via `read_file` on `picture_qa_review.jpg`: crisp Hubble/Voyager Uranus globe. | **`PASS` (both)** |
| `polish_gate.py <mp4> --cuts <cuts.json> --out <json>` | **`PASS` (rc=0):** `0 of 14 rows failed` (`14` shots, avg `2.6 s`, max `4.00 s`, `0` split panels, `0` near-black failures, `0` jitter/wobbly pushes). | **`PASS` (rc=0):** `0 of 11 rows failed` (`11` shots, avg `2.5 s`, max `3.92 s`, `0` split panels, `0` near-black failures, `0` jitter/wobbly pushes). | **`PASS` (both)** |
| `sfx_kit.py level --vo <vo> --sfx <sfx> --bed <bed> --minutes <m>` | **`PASS` (rc=0):** `SFX level PASS: VO -16.3 LUFS, SFX -38.3 LUFS, 6 hits` (`22.0 LU` below VO integrated loudness; bed `-34.0 LUFS`; encoded AAC `-14.1 LUFS`, `-2.1 dBTP`). | **`PASS` (rc=0):** `SFX level PASS: VO -16.7 LUFS, SFX -38.7 LUFS, 6 hits` (`22.0 LU` below VO integrated loudness; bed `-34.7 LUFS`; encoded AAC `-14.1 LUFS`, `-2.1 dBTP`). | **`PASS` (both)** |
| `music_gate.py <film_dir> --bed <bed> --video <mp4>` | **`PASS` (rc=0):** `uranus_score_bed_v01.mp3, 629.4 s, about 70.6 BPM, brief Pace: 66-76 BPM`, covers full `36.48 s` runtime with zero dropouts. | **`PASS` (rc=0):** `uranus_score_bed_v01.mp3, 629.4 s, about 70.6 BPM, brief Pace: 66-76 BPM`, covers full `27.48 s` runtime with zero dropouts. | **`PASS` (both)** |
| `thumb_preview.py short <frame0.jpg> / <cover.jpg> --score` | **`PASS` (rc=0):** `frame0.jpg`: `PASS saturation=98.4 near_black=1%`; `cover.jpg`: `PASS saturation=128.1 near_black=2%`. | **`PASS` (rc=0):** `frame0.jpg`: `PASS saturation=125.2 near_black=1%`; `cover.jpg`: `PASS saturation=159.8 near_black=2%`. | **`PASS` (both)** |

---

## 3. Part 2 — Full-Film `0.5 s` (`2 fps`) Contact-Sheet Grid Inspection

Full-film `2.0 fps` contact sheets with burned-in `t=MM.Ss (fNNN)` timestamps (`/tmp/j2870_review/short1_v02_2fps.jpg`, `73` frames `0.0–36.0 s`; `/tmp/j2870_review/short2_v02_2fps.jpg`, `55` frames `0.0–27.0 s`) were generated and inspected via `read_file`:

1. **Short #1 (`033_short01_testA_opening_v02.mp4`, `73` frames at `2 fps`):**
   - **Full-bleed `9:16` (`1080×1920`) across every shot (`R01a` through `R01_loop`):** Zero `16:9` (`1080×608`) horizontal bands or blurred pads anywhere (`0/73` padded frames at 2 fps). High-res planetary stills (`PIA01280`, `PIA01391`, `PIA00032_left_globe`, `PIA00346`, `PIA18033`, `PIA00143`, `weic2310a_unannotated`, `PIA02963_borderless`, `PIA18182`) sit seamlessly inside a continuous, moving JWST deep-field starfield surround (`_bleed_033_v02.py`) with zero horizontal seams or artificial bars.
   - **Vertical `9:16` `R05a` Axial-Tilt Gauge (`18.20–22.20 s`, `t=18.5s..22.0s`):** Natively rendered on `1080×1920` with `EARTH 23.4°` (`y=210..600`) stacked vertically above `URANUS 97.77°` (`y=710..1120`), animated protractor arcs (`23.44°` cyan vs `97.77°` yellow), and the single teach overlay `URANUS TILT: 97.77° (> 4× EARTH)` at `y=1174`, completely clear of the word-by-word captions at `y=1300`.
2. **Short #2 (`033_short02_ice_giant_surface_v02.mp4`, `55` frames at `2 fps`):**
   - **Full-bleed `9:16` (`1080×1920`) across every shot (`R49a` through `R49_loop`):** Zero horizontal bands or blur-padding (`0/55` padded frames at 2 fps).
   - **All 3 narrow Voyager 2 ring plates (`PIA00142.jpg`, `PIA01977.jpg`, `PIA01985.jpg`) replaced:**
     - `R49a` (`0.00–1.88 s`) uses the clean full-bleed `r55_cut1_r55b_100x_silent.mp4` Uranus cloud-deck dive with the `32%` `PIA00142.jpg` diagonal ring-line overlay removed.
     - `R51a` (`5.60–7.80 s`) replaces `PIA01977.jpg` with the full-bleed Hubble/Voyager Uranus globe (`PIA18182.jpg`, `1.31×` upscale).
     - `R53a` (`18.85–21.20 s`) replaces `PIA01985.jpg` with the full-bleed JWST NIRCam Uranus & polar-cap plate (`weic2310a_unannotated.png`, `1.11×` upscale).
   - **Vertical `9:16` `R52` Interior Cutaway (`14.85–18.85 s`, `t=15.0s..18.5s`):** Natively rendered on `1080×1920` with `ICE GIANT CUTAWAY` / `CLOUDS · HOT FLUID · ROCKY CORE` at the top (`y=175..260`), a large `720 px` animated cutaway globe (`y=360..1080`) sweeping open from `20°` to `160°` to reveal the cyan cloud deck, deep blue-cyan superheated fluid mantle, and glowing rocky core, and the single teach overlay `≥ 80% HOT DENSE FLUID` at `y=1174` above the spoken captions at `y=1300`.

---

## 4. Part 3 — Cut-Boundary (`±3` Frames) & Final `3.0 s` (`75` Frames) Strip Inspection

Cut-boundary splice strips (`±3` frames = `7` frames per internal cut) and `75`-frame (`25 fps`) final `3.0 s` strips plus Frame `0` loop target (`/tmp/j2870_review/short1_v02_cuts_pm3.jpg`, `short1_v02_final_3s.jpg`, `short2_v02_cuts_pm3.jpg`, `short2_v02_final_3s.jpg`) were generated and inspected via `read_file`:

1. **Short #1 (`13` internal cuts × `7` frames = `91` frames; final `3.0 s` = `f837..f911`, `33.48–36.44 s` + `f000`):**
   - Every internal cut (`2.36s f059`, `4.36s f109`, `8.16s f204`, `11.88s f297`, `13.88s f347`, `15.84s f396`, `18.20s f455`, `22.20s f555`, `25.00s f625`, `28.00s f700`, `31.08s f777`, `33.56s f839`, `35.56s f889`) is a clean hard cut on an exact `25 fps` frame boundary with zero black flash frames, zero duplicate freeze frames across cuts, and zero band-to-full-bleed jumps.
   - Across the final `3.0 s` (`f837..f911`), `R09a` (`f837..f838`) cuts cleanly to `R09b` (`f839..f888`, `33.56–35.52 s` pushing in on `PIA18182.jpg` as `"get knocked onto its side?"` completes at `35.52 s`), then cuts at `f889` (`35.56 s`) to `R01_loop` (`35.56–36.48 s`), which pushes continuously into the exact framing of `f000` (`R01a` Frame `0`).
2. **Short #2 (`10` internal cuts × `7` frames = `70` frames; final `3.0 s` = `f612..f686`, `24.48–27.44 s` + `f000`):**
   - Every internal cut (`1.88s f047`, `3.80s f095`, `5.60s f140`, `7.80s f195`, `11.56s f289`, `14.85s f371`, `18.85s f471`, `21.20s f530`, `23.28s f582`, `27.00s f675`) is a clean frame-accurate hard cut with zero flash frames or border jumps.
   - Across the final `3.0 s` (`f612..f686`), `R53c` (`r55_cut2_r55b_128x_vortex_silent.mp4`, `f612..f674`, `24.48–26.96 s`) swirls smoothly in full-bleed `9:16` while `"to 9,000 degrees Fahrenheit."` finishes at `26.924 s`, then cuts at `f675` (`27.00 s`) to `R49_loop` (`f675..f686`, `27.00–27.44 s`) with continuous motion matching `f000` (`0.00 s`) and zero static freeze hold.

---

## 5. Part 4 — Complete Soundtrack Inspection via Verified `audio_input` & Waveform Analysis

Both complete soundtracks (`/tmp/j2870_review/short1_v02_audio.mp3`, `36.48 s`, and `/tmp/j2870_review/short2_v02_audio.mp3`, `27.48 s`) were opened and listened to end-to-end via verified `audio_input` (`read_file`), and cross-checked against 20 ms peak envelopes on the exported VO stems (`033_short01_testA_opening_v02_vo.wav` and `033_short02_ice_giant_surface_v02_vo.wav`):

| Check Point | `v01` Defect (`J2400`) | `v02` Slice / Timeline (`J2869`) | `audio_input` Listening & 20 ms Waveform Verification (`J2870`) | Verdict |
|---|---|---|---|---|
| **Short #1 `"How"` (`~31.3 s`)** | Segment 1 started at `49.320 s`, clipping the first `70 ms` of the aspirate `"H-"` (`49.250 s`). | `VO_SEGMENTS = [(0.080, 31.040), (49.220, 53.880)]` with `VO_GAPS = [0.20]`. `"ball."` ends cleanly (`30.62–30.98 s`), followed by natural room breath (`pk=0.0099` at `31.340 s`) and full `"How"` (`31.34–31.54 s`). | Heard via `audio_input`: *"rolling around the Sun on its side like a ball. How did an entire giant planet get knocked onto its side?"* — the initial aspirate `"H-"` of `"How"` (`31.360 s`, `pk=0.215` -> `0.382` at `31.400 s`) is **100% unclipped**. | **`PASS`** |
| **Short #2 `"80%"` (`~12.0 s`)** | Sub-slice started at Scribe `466.480 s`, chopping `200 ms` off `"eighty"` (`"-ty percent"`). | `VO_SEGMENTS` starts Segment 3 at `466.200 s` inside verified silence (`466.150..466.250 s`), keeping `"80% or more of the planet's mass is a hot, dense fluid of water, methane, and ammonia"` unbroken (`466.200–474.400 s`). | Heard via `audio_input`: *"Beneath the hydrogen and helium clouds, eighty percent or more of the planet's mass is a hot, dense fluid..."* — the initial vowel `"eigh-"` (`11.840 s`, `pk=0.253` -> `0.712` at `12.100 s`, Scribe word `12.004–12.604 s`) is **100% unclipped**. | **`PASS`** |
| **Short #2 `"9,000"` (`~25.0 s`)** | Sub-slice dropped `480.140..480.580 s`, deleting `"nine"` (`"-n thousand"`). | `VO_SEGMENTS` keeps Segment 7 (`478.900–482.550 s`, *"Uranus heats up to 9,000 degrees Fahrenheit."*) completely unbroken. | Heard via `audio_input`: *"Near that core, Uranus heats up to nine thousand degrees Fahrenheit."* — `"nine"` (`24.660 s` onset `pk=0.140` -> `0.701` at `24.700 s`, Scribe `9,000` at `25.044–25.704 s`) is **100% unclipped**. | **`PASS`** |

---

## 6. Part 5 — Compact `360×640` Moving-Video Proxy Review (`moving_video_input`) & Teach / Polish Gate Scores

Compact `360×640` (`<= 5 MB`) H.264/AAC review proxies (`/tmp/j2870_review/short1_v02_proxy_360p.mp4`, `1,308,205` bytes = `1.31 MB`; `/tmp/j2870_review/short2_v02_proxy_360p.mp4`, `999,969` bytes = `1.00 MB`) were generated and watched end-to-end via `read_file` (`moving_video_input`):

1. **Motion, Pacing & Visual Continuity (`moving_video_input`):**
   - **Short #1 (`36.48 s`):** Opens on the moving sideways Uranus crescent and rings (`R01a`, `0.00–2.36 s`) with `"21-YEAR NIGHT"` hook caption, transitions smoothly through full-bleed Hubble/Voyager/JWST plates and the animated `R03a` `21-year` polar night sweep (`8.16–11.88 s`), builds the vertical `R05a` Earth (`23.4°`) vs Uranus (`97.77°`) protractor gauge (`18.20–22.20 s`) in sync with the spoken tilt numbers, and closes on the central mystery question (*"How did an entire giant planet get knocked onto its side?"*) before looping cleanly at `35.56–36.48 s`.
   - **Short #2 (`27.48 s`):** Opens on the full-bleed `R49a` Uranus cloud dive (`0.00–1.88 s`, `"NO SURFACE"` hook caption), progresses across full-bleed Hubble WFC3, JWST NIRCam, and Voyager 2 upper-atmosphere push-in clips (`1.88–14.85 s`), animates the `R52` 3-layer interior cutaway (`14.85–18.85 s`) as the narrator explains the `80%` hot dense fluid ocean of water, methane, and ammonia, dives into the deep cyan cloud passage and core vortex (`21.20–27.00 s`) for the `9,000 °F` payoff, and loops seamlessly at `27.00–27.48 s`.
2. **Teach-on-Screen & Polish-Pass Gate Scores (Shorts Contract, `studio/RULES.md`):**
   - **DATA (1 single overlay per Short):** **`PASS`** — Short #1: `URANUS TILT: 97.77° (> 4× EARTH)` (`18.20–22.00 s`); Short #2: `≥ 80% HOT DENSE FLUID` (`15.00–18.72 s`). Both match `SOURCES.md` and spoken narration.
   - **STYLE (Item 5):** **`PASS`** — House Arial Black/Bold typography with yellow accent, `<= 4` words per label, positioned inside the vertical safe zone (`y=1174`), clear of `0–2 s` hook and `9.0–13.5 s` title card, zero black slabs, zero Orbit appearances (`visor=0.0`).
   - **MOTION (Item 6):** **`PASS`** — Both `R05a` and `R52` animate continuously with ease-in/out arcs and 0.25 s overlay fades, hold `<= 4.00 s`, and never run two code graphics back to back.
   - **SFX (Polish Item 1):** **`PASS`** — House `sfx_kit.py` synthesis (`6` cues each, `-38.3` / `-38.7 LUFS`, `22.0 LU` below VO, `0` collisions on speech).
   - **GRAIN (Polish Item 3):** **`PASS`** — Subtle temporal film grain (`noise=alls=2:allf=t`) and lifted navy floor (`RGB >= 28,38,58`) prevent banding across all dark space gradients.
