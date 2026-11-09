# J2257 — S6 Titan v11 Review Readiness for Ben's Watch (`J1199` Handoff)

- **Job**: `J2257` (`S6 Titan v11: review readiness for Ben's watch`)
- **Parent Assembly Job**: `J1199` (`OWB Shorts airing 3, 7 and 10 Nov: fix frame 0 and the meta-promise (rule 8) -> next version`, scoped to S6 Titan only per `jobs/reviews/J1208/CHIEF_SOURCE_DECISION_2026-11-05.md`)
- **Reviewer**: `macbook-2` (`Gemini 4 Argon (High)`)
- **Date**: `2026-11-05T21:47Z`
- **Verdict**: **`KEEP` — Ready for Ben's final watch (`OWB UAT/standalone_shorts_s6_v11/owb_sa_s6_titan_v11.mp4`, SHA-256 `8eead2f62fd3eda48674ed4c5ae667927d98ea69a03f3dc5ccd874c960121b31`, due `2026-11-10 10:30` London for the `2026-11-10 11:30` London air slot; scheduled `RLSJm59OSzI` `v01` preserved as fallback; `v01` and `v02` untouched; £0.00)**

---

## 1. Evidence Verified & Perception Boundary

1. **Reviewed Delivery & Ruling Artifacts:**
   - `jobs/reviews/J1199/DELIVERY_2026-11-05.md`, `jobs/reviews/J1199/REVIEW_BRIEF.md`, `jobs/reviews/J1199/PICTURE_QA.md`, `jobs/reviews/J1199/assemble_s6_v11.py`, `jobs/reviews/J1199/owb_sa_s6_titan_v11_meta.json`, and all six gate outputs (`owb_sa_s6_titan_v11_{gate,loop,music_gate,picture_qa,polish,sfx_level}.txt`).
   - Chief exact-source decision `jobs/reviews/J1208/CHIEF_SOURCE_DECISION_2026-11-05.md` (`PR #558`) and `jobs/reviews/J2167/REVIEW.md`.
2. **Independent Durable UAT Checksum & Stream Verification (`iCloud OWB UAT/standalone_shorts_s6_v11/`):**
   - Materialized and verified all 11 files in `~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/standalone_shorts_s6_v11/` via `shasum -a 256 -c MANIFEST.sha256` (`11/11 OK`):
     - `owb_sa_s6_titan_v11.mp4`: `8eead2f62fd3eda48674ed4c5ae667927d98ea69a03f3dc5ccd874c960121b31` (`81,327,495` bytes; identical SHA-256 recorded for the NAS copy `YouTube/orbit-with-ben/OWB UAT/standalone_shorts_s6_v11/owb_sa_s6_titan_v11.mp4`).
     - `owb_sa_s6_titan_v11_PHONE.mp4`: `f72f7e3d7adcdda9fddcbc49fa2c471e5e097cf1c200af44fad797dd0baa38bb` (`1,745,401` bytes).
     - `owb_sa_s6_titan_v11_frames.jpg`: `02d23072da57b80b9dc55c69d35e97dbc6e762526953e2b1b2d0333d72134f06`.
     - `owb_sa_s6_titan_v11_2fps.jpg`: `aa64aba43c3dd160c0622fc039c7a672732d6baa3701bcbd86d0c86277e581c3`.
     - `owb_sa_s6_titan_v11_meta.json`: `93c2048c88b16bc673ce43142210124d839c7c0676ccd723287448255b3ff219`.
   - Independent `ffprobe` and `ffmpeg -filter_complex ebur128=peak=true` on `owb_sa_s6_titan_v11.mp4`:
     - Video: `H.264 High`, `yuv420p`, `1080x1920` (`9:16`), `24/1 fps` CFR (`time_base=1/24000`), `start_time=0.000000`, `duration=18.000000 s`, `432` frames (`64 + 120 + 120 + 100 + 28 = 432`).
     - Audio: `AAC LC`, `48,000 Hz`, stereo, `duration=18.000000 s`, integrated loudness **`-14.5 LUFS`** (target `-14.0 ± 0.5 LUFS`), `LRA: 2.2 LU`, true peak **`-1.6 dBFS`** (`<= -1.5 dBTP`).
   - Independent `gate_shorts_open.py check` run on `owb_sa_s6_titan_v11.mp4` (`--air-date 2026-11-10 --id RLSJm59OSzI`):
     - `PASS  owb_sa_s6_titan_v11.mp4  dur=18.0s  audio=-17.0dB  motion=17.16  f0diff=4.72  cut1=2.67s  vo_onset=0.00s  tail_gap=1.87s  dhash=fcafede2a72fbdf5  visor=0.0021`
3. **Visual Inspection & Perception Boundary:**
   - Directly inspected the contact sheets (`owb_sa_s6_titan_v11_frames.jpg`, `owb_sa_s6_titan_v11_2fps.jpg`, `owb_sa_s6_titan_v11_open_sheet.jpg`) and full-size `1080x1920` extracted stills across Frame 0 (`0.00 s`), Row 1 (`1.29 s`), Row 2 (`5.21 s`), Row 3 (`10.21 s`), Row 4 (`14.79 s` and `15.83 s` fact overlay), and Row 5 (`17.42 s` forward preroll).
   - **Perception boundary:** This review does not claim real-time moving-picture playback or subjective audio mix listening; per `AGENTS.md` (*"Ben's final watch is the watch-and-listen check"*), Ben's final watch of the UAT cut supplies the subjective watch-and-listen check. Zero tool FAILs exist or are waived.

---

## 2. Tool Gates Summary (0 FAILs)

| Gate | Result | Key Measurements |
|---|---|---|
| `gate_shorts_open.py` | **PASS** (`0` fails) | `dur=18.0s`, `audio=-17.0dB`, `motion=17.16` (`>=10.0`), `f0diff=4.72` (`>=1.50`), `cut1=2.67s` (`<=3.00s`), `vo_onset=0.00s` (`first word 0.10s`), `tail_gap=1.87s`, `visor=0.0021` |
| `picture_qa.py` | **PASS** (`0` of `5` cuts fail) | `5` cuts (`0.00–2.67s`, `2.67–7.67s`, `7.67–12.67s`, `12.67–16.83s`, `16.83–18.00s`), `0` fails, `5` WARNs inspected full size below |
| `polish_gate.py` | **PASS** (`0` of `5` rows failed) | Rows `1, 3, 4, 5` `ok`; Row `2` (`5.2s`, `PIA06230`) low-detail WARN (`0.0149 < 0.0157`) inspected full size below |
| `short_c37.finish_scan` (`loop`) | **PASS** | `loop_diff_masked=7.05`, `open_median_step=5.60`, `head_matches=[0, 0, 0, 0, 0]` (contiguous `f27 -> f28` seam across `build_cycle`) |
| `music_gate.py` | **PASS** | `owb-standalone-shorts_score_bed_v01.mp3` (`60.0 s`, same locked standalone-shorts bed as `v01`/`v02`; pace warn `120.0 BPM vs 84–96 BPM` left to Ben's listen) |
| `sfx_kit.py level` | **PASS** | `VO -20.4 LUFS`, `SFX -36.9 LUFS` (`16.5 LU` below VO), `2 hits` (`rumble at 0.00 s`, `tick at 15.15 s`) |

---

## 3. Still-Sheet & Full-Size Inspection of All Flagged WARNs

1. **Artist's illustration on the opening (`0:01`, Row 1, `0.00–2.67 s`) and forward loop preroll (`0:17`, Row 5, `16.83–18.00 s`):**
   - **Recipe compliance (`CHIEF_SOURCE_DECISION_2026-11-05.md`):** Built from accepted `S6_flow_t2_silent.mp4` (`sha256: 2218c817e96a1444da45a7130e5cc8d0cc8824a322f4a16ed6078c85562dad2a`), opening frames `28..91` (`64` frames = `2.666667 s`) and forward loop preroll frames `0..27` (`28` frames = `1.166667 s`), `crop=720:405:0:875` scaled `1.50x` (`<= 2.35x`) to `1080x608` at `y=656` with `72 px` vertical alpha feathering over a moving `gblur=sigma=28` fill from the same crop.
   - **Full-size visual check:** The `16:9` centre band (`y=656..1264`) shows textured low-relief brownish-orange Titan terrain beneath opaque amber-orange atmospheric haze, with smooth `72 px` feathered edges into the blurred amber/brown fill above and below. There are no hard band edges, no celestial sky disc (Take 1's defect is completely absent), and no Veo text or watermarks. The top hook caption `15 M / UNDERWATER` (`yellow 15`, `0.0–2.2 s`) and lower-third subtitles (`STANDING ON TITAN` / `FEELS LIKE BEING`) sit on clean, high-contrast background areas clear of the horizon detail. Generated-illustration disclosure is recorded in `owb_sa_s6_titan_v11_meta.json` and `DELIVERY_2026-11-05.md` (not NASA footage, not a measured landing site, no Short corner credit). -> **KEEP**.

2. **Visor score `0.0021` at `0 s` (`gate_shorts_open.py` warn: `possible Orbit at 0 s (visor 0.0021) — eyeball the sheet`):**
   - **Full-size & open-sheet check:** Direct inspection of `frame_01.png` (`0.00 s`) and `owb_sa_s6_titan_v11_open_sheet.jpg` confirms **Orbit is not present** at Frame 0 or anywhere in the Short. The `0.0021` orange-hue fraction is a false positive triggered by the warm amber-orange colour of Titan's atmospheric haze. -> **KEEP**.

3. **`PIA06230` low detail (`0:05`, Row 2, `2.67–7.67 s`: `edge density 0.0149 < film p5 0.0157`):**
   - **Full-size visual check (`5.21 s`):** `PIA06230.jpg` is the official NASA/JPL/SSI Cassini global visible-light image of Titan's smooth golden-orange photochemical haze globe against space (unchanged from `v01` and `v02`). Because Titan's dense orange haze obscures surface features in visible light, the globe naturally has low high-frequency edge density (`0.0149` vs film 5th percentile `0.0157`). Full-size `1080x1920` inspection confirms clean limb definition, uniform `noise=alls=4:allf=t` grain on the navy surround, and zero compression blockiness or banding. -> **KEEP**.

4. **Body upscale `2.20x` (`Rows 2, 3, 4`: `PIA06230.jpg`, `PIA09739.jpg`, `PIA21625.jpg`):**
   - **Full-size visual check (`5.21 s`, `10.21 s`, `14.79 s`, `15.83 s`):** `2.20x` is strictly within the channel's `<= 2.35x` upscale ceiling (`picture_qa.py` WARN range `2.00x–2.35x`). Full-size `1080x1920` inspection of all three official Cassini plates (`PIA06230` global orange haze, `PIA09739` near-IR cloud/surface view under the `9.0–14.0 s` title banner `Standing on Titan Feels Like / Diving 15 Metres Down`, and `PIA21625` backlit detached haze ring with the `15.10–16.73 s` `2034 / LANDS` fact overlay centred inside the dark disk) confirms clean rendering with no pixelation, ringing, or text collision. -> **KEEP**.

5. **Tail gap `1.87 s` (`last word 16.13s, duration 18.00s`):**
   - **Timing check:** Locked `vo_v02.wav` (`sha256: 1298d4fbbe2be1d633546dd348212383c09cf868eb9c518bdbcd06cdd30a0e53`) ends the final word `"2034"` at `16.13 s`. The `2034 / LANDS` fact card holds through `16.73 s` (clearing before the `16.833 s` cut), and Row 5 (`16.833–18.000 s`) runs the Chief-mandated `28`-frame (`1.166667 s`) forward loop preroll (`frames 0..27`) that joins seamlessly into Frame 0 (`frame 28`). This `1.87 s` tail window is identical to `v02` and is a non-failing WARN. -> **KEEP**.

6. **Duration `18.0 s` (`outside 22–27s band`):**
   - **Rule check:** Explicitly covered by the `J0216` standalone Shorts test exception (`AGENTS.md` Standing Lesson 5 & 7) and the `J1199` brief (`keep 18-27 s` after excising the `"Stay, and I'll show you why NASA's going"` meta-promise sentence on a sentence boundary with no new VO). -> **KEEP**.

---

## 4. Preservation & Non-Destructive Guarantees

- **Original versions untouched:**
  - `v01` (`owb_sa_s6_titan_v01.mp4`, SHA-256 `3f2f51d4f8ffd1adfc0e9c0e91c25839198860e49c3085367ea876f341d606a2`) and its manifest remain untouched.
  - `v02` (`owb_sa_s6_titan_v02.mp4`, SHA-256 `be16daeb17284ea3d20148a1e6f8e3ea7ab6cdec64cf22e47f92b6167780b97d`) and its UAT folder (`OWB UAT/standalone_shorts_s6_v02/`) remain untouched.
- **No publishing/schedule/Buffer changes:** Scheduled YouTube Short `RLSJm59OSzI` (`2026-11-10T11:30:00Z`) remains untouched as the automatic fallback if `v11` is not watched and authorized before `2026-11-10 10:30` London.
- **Spend:** `£0.00` / `0` credits.

---

## 5. Recorded Ben Watch (`jobs.py awaits J1199`)

Recorded on parent job `J1199` via `jobs.py awaits`:
- **Job**: `J1199`
- **File**: `OWB UAT/standalone_shorts_s6_v11/owb_sa_s6_titan_v11.mp4` (SHA-256 `8eead2f62fd3eda48674ed4c5ae667927d98ea69a03f3dc5ccd874c960121b31`, matching NAS `YouTube/orbit-with-ben/OWB UAT/standalone_shorts_s6_v11/owb_sa_s6_titan_v11.mp4`)
- **Version**: `v11`
- **Due**: `2026-11-10 10:30` London (`2026-11-10T10:30Z`)
- **Airs**: `2026-11-10 11:30` London (`2026-11-10T11:30Z`)
- **If Not**: `Scheduled RLSJm59OSzI (v01) stays as the fallback and airs as scheduled; no swap`
