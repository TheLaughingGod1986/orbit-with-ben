# Independent Audio & Moving-Video QA Review — OWB 064 Short 1 (`v03`, `J3923`)

- **Job:** `J3923` (`kind: qa`, `ref: J3918`, board: `064 edit`)
- **Reviewer:** `gemini` (specialist worker — NOT elected Chief; elected Chief is `codex`)
- **Date:** 2026-11-27
- **Reviewed Target:** `OWB:064` Companion Short 1 (Test A Opening Short) immutable **`v03`** on **PR #1399** (branch `gemini/J3903-owb064-short1-testa-v02`, head `961a0b19d5`, following `J3922` repair)
- **Prior Context Verified:** Read `J3918` Chief FIX ruling (`codex`) and **PR #1400** (`jobs/reviews/J3918/REVIEW.md`), explicitly confirming its numerical correction: `064_short01_testA_opening_v02_vo.wav` (`c27ed2ee…`) carries per-channel `±1 LSB` PCM dither near-silence at **`-90.31 dBFS`** (`max|i16| = 1`, `nonzero = 100%` of samples) across `S2`, `S3` tail, and `S4` — not literal exact digital zero (`-180.0 dBFS`) — while `v02.mp4` retained its score bed and SFX.
- **Verdict:** **`KEEP` (recommended to elected Chief `codex`)**
- **Authority Boundary:** This is independent specialist-worker QA evidence, **not** a Chief PASS, PR merge, or Ben UAT registration (`jobs.py awaits`). Only elected Chief (`codex`) PASS and merge of PR #1399 (`961a0b19d5`) may release `J3903` for Ben's phone UAT watch. Zero upload, scheduling, privacy, Buffer, generation, or spend actions were performed (`£0.00` cash, `0` credits).

---

## 1. Demonstrated Reviewer Capabilities (Recorded via `chief_relay.py capabilities`)

- **`audio_input` (demonstrated):** Directly listened to canonical NAS `064_short01_testA_opening_v03_vo.wav` (`8483ba3e…`) and `064_short01_testA_opening_v03.mp4` (`538464b9…`) via native `read_file` in this session. Neither ASR nor DSP waveforms were substituted for listening.
- **`moving_video_input` (demonstrated):** Directly watched the complete moving `9:16` playback of canonical NAS `064_short01_testA_opening_v03.mp4` (`538464b9…`) from `00:00` to `00:30` with its synchronized final audio mix via native `read_file` in this session. Sampled stills were used only to inspect flagged frames, phone-size previews, and exact cut/loop boundaries alongside moving-video review.
- Recorded on the Mini via `python3 scripts/chief_relay.py capabilities --agent gemini --available "audio_input,moving_video_input" --evidence "…"`.

---

## 2. Exact Canonical Hashes, Preserved Versions, Video Equivalence & Locked Sources (**MEASURED**)

### 2.1 Canonical NAS `v03` Deliverables (all verified on NAS and matching PR #1399 `961a0b19d5`)

| File | Exact SHA-256 | Size (bytes) |
|---|---|---|
| `06_Final-Exports/064_short01_testA_opening_v03.mp4` | `538464b9addf45088affe5e09146cec7324351d2e18552a41d66bb4d89bac402` | `75,099,108` |
| `06_Final-Exports/064_short01_testA_opening_v03_vo.wav` | `8483ba3e5448c5506598149ad9f2b4fe33a80ce66ae05b9d30f0f2f4aa8d7393` | `5,904,044` |
| `06_Final-Exports/064_short01_testA_opening_v03_bed.wav` | `7bb8302b7fbd219aecfcb50d84a13298169ab5c4c0ac64eb1f4830460dbd02dd` | `5,904,044` |
| `06_Final-Exports/064_short01_testA_opening_v03_sfx.wav` | `f4f13e907d76b5f6d7781396e770c3d4e809312a60976edf1ce710908135891c` | `5,904,044` |
| `06_Final-Exports/064_short01_testA_opening_v03_en-GB.srt` *(matches PR #1399 git `Captions/…`)* | `a61a737048188667682e566a9f7ec78e08ca704dd836db231d86c6d2207fa603` | `1,423` |
| `06_Final-Exports/064_short01_testA_opening_v03_frame0.jpg` | `0e05827a32f3097658a33ce1d57c6edc0a26035dbf7715d738ba4dd9d6c41a2c` | `448,809` |
| `06_Final-Exports/064_short01_testA_opening_v03_cover.jpg` | `0e5b993776582f461091268acec11f8c4a34c8a320428605898ae7b884a3054e` | `970,363` |

### 2.2 Preserved Prior Versions (Verified Untouched on NAS & in PR #1399)

- `064_short01_testA_opening_v01.mp4`: `b805c51d02acd0e43adf9c9645c993c91d148641e068e918d93136e20b25a4b6` (`75,409,388` bytes)
- `064_short01_testA_opening_v02.mp4`: `8b7a218c73b1c790f722f4410e67e4fe04d7e06276e3d4a4bbcbceed38c38968` (`75,099,301` bytes)
- `064_short01_testA_opening_v01_vo.wav` & `064_short01_testA_opening_v02_vo.wav`: `c27ed2eed91581f2bdc7167384d2a16dcd6b513f848d20784b1cdaefb7438873` (`5,904,044` bytes)
- `07_Upload-Package/PACKAGE_MANIFEST_v02.json`: preserved verbatim alongside `PACKAGE_MANIFEST_v03.json` and active `PACKAGE_MANIFEST.json`.

### 2.3 Locked Parent Source Identities (Verified on NAS)

- Parent long master `v03` (`09_Final-Export/064_every_planet_explained_master_v03.mp4`): `d59057aed1590e7f6ef097513256a0548c4f9b1d7e544c4bade28aa83fef647a` (`557,502,349` bytes)
- Locked VO WAV (`02_Voiceover/every_planet_explained_vo_v01.wav`): `4b478fcded393890064ffd285a4121882dc26e0515f3cadc6569adf0465616aa` (`131,301,198` bytes)
- Film score bed (`05_Music/every_planet_score_bed_v01.mp3`): `3e47e9d6da9aca6836a00c27a1fa58e53801190ae06ed445966ed51f5c0d75c6` (`16,846,514` bytes)
- NASA MESSENGER shelf plates (`03_Reference-Material/harvest_J3022_v01/`):
  - `PIA17386.jpg`: `d7160dfb9715e346b7bdbb82422dd4a376015919aadee182a911739df5842212`
  - `PIA16853.jpg`: `bdcb9569ddb0656befd16ab9a622b3de0791a58308adec64c7c6ce89b826e927`
  - `PIA19411.jpg`: `2e617e8a00dd16f3f9742de8cb3b7963a8eb9d82f332d30b748ff12562d8ba59`
  - `PIA15162.jpg`: `ee40946826c057c4d5a9706391b0a4899c8013373506b445e3c2d31bbb0031c3`
  - `PIA11364.jpg`: `8734f46ba6e438445a72764edcb2dcbf7b6c34116d224f2dd6860c4d1e9c826a`

### 2.4 Unchanged Copied Video Track Proof (`v02` → `v03`)

- Encoded video packet stream hash (`ffmpeg -map 0:v:0 -c copy -f hash -hash sha256`):
  - `v02.mp4`: `SHA256=d7d5e684a9672dff62f5e0cfce669685549df86f6094b1eb817c495716fd40a0`
  - `v03.mp4`: `SHA256=d7d5e684a9672dff62f5e0cfce669685549df86f6094b1eb817c495716fd40a0` (**bit-exact match**)
- Decoded `framemd5` across all `738` frames (`ffmpeg -map 0:v:0 -f framemd5`):
  - `v02.mp4`: `44486886b9e676501419057998895c973861c66f458b64bb6ac10961f671668d` (`738` frames)
  - `v03.mp4`: `44486886b9e676501419057998895c973861c66f458b64bb6ac10961f671668d` (`738` frames, **bit-exact match**)

---

## 3. Independent **HEARD** Evidence (`audio_input`)

Directly listened in full to both `064_short01_testA_opening_v03_vo.wav` (isolated narration stem) and `064_short01_testA_opening_v03.mp4` (full final AAC mix):

- **All 4 sentences & all 71 locked words heard verbatim** (matched word-for-word against `every_planet_explained_script_master_v04.md` opening):
  1. **S1:** *"On Mercury, the Sun's closest planet, why does water ice survive four hundred and thirty-degree heat?"* — clean entry, zero clipped onset, clear British narration.
  2. **S2:** *"The ice hides in polar craters that never see sunlight."* — completely restored (was missing in `v02`), natural brief breath after S1, zero pops or clicks at the splice.
  3. **S3:** *"At fifty-eight million kilometres out, sunlight shines up to seven times brighter than on Earth, yet without an atmosphere to retain heat, you would feel night plunge to minus one hundred and eighty degrees Celsius."* — completely restored from start to finish (previously dropped out after *"At fifty-eight million"* in `v02`), crisp articulation on every number and unit (*58 million kilometres*, *7 times*, *minus 180 degrees Celsius*).
  4. **S4:** *"In 1965, Italian mathematician Giuseppe Colombo solved its spin mystery."* — completely restored (was missing in `v02`), clear pronunciation of *Giuseppe Colombo*, clean finish on *"mystery"* with zero clipped tail.
- **No clipped words, stumbles, or unexpected gaps:** Every word across `00:00–00:30` is fully audible and clean; sentence-to-sentence pacing sounds natural and continuous.
- **VO / bed / SFX balance:** Narration sits clearly forward and intelligible throughout. The warm, gently pulsing ambient score bed (~70 BPM) stays cleanly tucked beneath the voice (never masking consonants or competing with speech) and lifts subtly in the brief ~1.1 s tail after *"spin mystery"*. House SFX (soft opening whoosh, subtle ticks on animated graphic/pill reveals) sit well beneath speech with zero harshness.
- **Full-runtime music & loop seam:** Music plays continuously from `00:00` through the final beat at `00:30`, with no sudden drop-out, click, or dead silence before looping back to the open.

---

## 4. Independent **WATCHED** Evidence (`moving_video_input` + Flagged/Boundary/Phone Inspection)

Directly watched the complete moving `064_short01_testA_opening_v03.mp4` (`00:00–00:30`), plus inspected `064_short01_testA_opening_v03_open_sheet.jpg`, `064_short01_testA_opening_v03_review_12shots.jpg`, `064_short01_testA_opening_v03_frame0_preview.jpg`, `064_short01_testA_opening_v03_cover_preview.jpg`, `picture_qa_review.jpg`, and exact extracted boundary frames (`f0`, `f337`, `f338`, `f570`, `f665`, `f737`):

- **Frame-0 motion & subject recognition:** Moving playback confirms Mercury's enhanced-colour MESSENGER globe is immediately recognizable and visibly rotating/pushing smoothly from frame 0 (`00:00` → `00:01` → `00:02`) over a full-bleed starfield, with crisp white/yellow `#FFE000` hook **`ICE AT / 430°C?`** above the planet and **zero Orbit**. Phone-size previews (`frame0_preview.jpg` and `cover_preview.jpg`) keep `ICE AT / 430°C?` sharp and legible in both `9:16` feed and `16:9` shelf crop.
- **Full-bleed `9:16` framing:** Every shot across all 12 cuts fills the entire `1080×1920` vertical frame cleanly — zero horizontal bars, zero blurred-copy padding, zero flat black panels.
- **Title, graphic & Colombo pill timings vs actually audible words:**
  - **Hook (`0.00–2.50 s`):** `ICE AT / 430°C?` holds over moving Mercury while VO speaks *"On Mercury, the Sun's closest planet"* (`0.10–2.67 s`), fading cleanly before the `R01b` crater closeup cut at `2.500 s`.
  - **Promoted Long Title (`9.00–14.00 s`):** **`Every Planet Explained / in 12 Minutes / (Mercury to Neptune)`** sits cleanly centered while VO speaks *"…that never see sunlight. At fifty-eight million kilometres out, sunlight shines up"*. Burned-in bottom captions stay suppressed during `9–14 s` (covered by `en-GB.srt`), avoiding visual clutter; frame `f337` (`14.042 s`) confirms the title is already gone before `R03b` cuts in at frame `f338` (`14.083 s`) — **zero title/graphic collision**.
  - **Code Graphic 1 (`R03b`, `14.083–16.417 s`):** Animated `58 MILLION KM` / real MESSENGER Mercury globe / `UP TO 1.0× → 7.0× SUNLIGHT` bar with blue `1×` Earth reference / `BRIGHTER THAN EARTH` builds directly in time with audible **"seven"** (`14.12 s`), **"brighter"** (`14.86 s`), **"Earth"** (`15.62 s`).
  - **Real imagery between graphics (`R03c`, `16.417–20.042 s`):** Full-bleed moving blue/gold MESSENGER cratered surface runs under *"yet without an atmosphere to retain heat, you would feel night"* — **no two code graphics back-to-back**.
  - **Code Graphic 2 (`R03d`, `20.042–23.458 s`):** `WITHOUT AN ATMOSPHERE` / real MESSENGER Mercury globe / `+430 °C HEAT` orange bar + animated blue bar plunging to `-180 °C NIGHT` (`NIGHT PLUNGE`) synchronizes cleanly with audible **"plunge"** (`20.10 s`) → **"minus"** (`20.66 s`) → **"eighty"** (`21.88 s`) → **"Celsius"** (`22.62–23.32 s`).
  - **Colombo Teach Pill (`1965 · GIUSEPPE COLOMBO`, `23.75–27.70 s`):** Enters right on audible **"1965"** (`23.70 s`), holds cleanly across **"Italian mathematician Giuseppe Colombo"** (`25.24–27.64 s`), and is confirmed off at frame `f665` (`27.708 s`) before **"solved its spin mystery"** (`28.08–29.64 s`). Duration `3.95 s <= 4.00 s`.
  - **End Card & Loop Return (`R01_loop`, `29.750–30.750 s`):** Enters cleanly after *"mystery"* ends (`29.639 s`) showing exact promoted long title + yellow **`Full film on the channel`** over the enhanced-colour Mercury globe whose position/lighting at frame `f737` matches frame `f0` for a clean visual loop.
- **All flagged frames visually verified clean:**
  - `picture_qa` 5 WARNs (`0:03 R01b PIA17386`, `0:07 R02a PIA19411`, `0:09 R02b PIA19411`, `0:18 R03c PIA17386`, `0:25 R04a PIA11364`): All five are genuine, crisp NASA MESSENGER images (enhanced surface mosaics, north-polar yellow water-ice crater mosaic, natural-colour globe); zero dated diagrams, zero textbook schematics, zero artifacts.
  - `polish_gate` 1 WARN (`0:25 R04a PIA11364`, edge density `0.1087 < film p5 0.1129`): Planet disk is sharp and crisp; lower frame-wide edge density comes solely from the clean starfield around the globe, with fine grain and zero banding.
- **Minor non-blocking polish observations (logged honestly, not blockers):**
  - During the first ~1.1 s of the `9–14 s` title (`R02b`, `9.00–10.125 s`), the title fades in over the brighter textured polar-crater mosaic before cutting to the high-contrast dark-starfield `R03a` Mercury globe (`10.125–14.00 s`); the thick black text outline keeps it readable throughout.
  - `064_short01_testA_opening_v03_en-GB.srt` cue 2 uses lowercase `the sun's closest` (carried from `words.json`) vs capitalised `the Sun's closest` in the script; minor cosmetic detail only.

---

## 5. Independent **MEASURED** Evidence (Gates, Regression, Package & Security)

### 5.1 Speech-Coverage Regression Proof (`old v02 FAILS` vs `new v03 PASSES`)

Independently measured against locked source `every_planet_explained_vo_v01.wav` (`4b478fcd…`, active 200 ms windows `src > -45 dBFS`) plus per-channel 16-bit PCM check on `v02_vo.wav`:

| Segment | Locked Source Span | Output Span | Old `v02_vo.wav` (Measured) | Repaired `v03_vo.wav` (Measured) |
|---|---|---|---|---|
| **S1** | `0.06–6.60 s` | `0.00–6.54 s` | `ch0 -18.72 dBFS`, `29/29` active | **`-18.81 dBFS`**, `29/29` (`100%`), `0` dropouts, `corr=0.9917` |
| **S2** *(offset > 0)* | `7.56–11.05 s` | `6.60–10.09 s` | **FAIL:** `ch0 -90.31 dBFS` (`max\|i16\|=1` `±1 LSB` dither), `0/17` active, `17` dropouts | **PASS:** **`-19.18 dBFS`**, `17/17` (`100%`), `0` dropouts, `corr=0.9997` |
| **S3** *(offset > 0)* | `11.89–25.14 s` | `10.17–23.42 s` | **FAIL:** tail `12.2–23.4 s` `ch0 -90.31 dBFS` (`max\|i16\|=1`), `7/60` active, `53` dropouts | **PASS:** **`-19.36 dBFS`**, `60/60` (`100%`), `0` dropouts, `corr=0.9998` |
| **S4** *(offset > 0)* | `26.28–32.60 s` | `23.44–29.76 s` | **FAIL:** `ch0 -90.31 dBFS` (`max\|i16\|=1` `±1 LSB` dither), `0/31` active, `31` dropouts | **PASS:** **`-18.37 dBFS`**, `31/31` (`100%`), `0` dropouts, `corr=0.9994` |

- **Total active speech coverage:** `v02` = `36/137` (`101` dropouts — **FAIL**); `v03` = **`137/137` (`100.0%`, `0` dropouts — PASS)**.
- **Independent loudnorm on decoded `v03.mp4`:** `I = -14.14 LUFS`, `TP = -2.05 dBTP`, `LRA = 2.40 LU`.
- **Full-runtime bed stem (`v03_bed.wav`):** `30.750 s`, min 0.5 s bin `-49.69 dBFS`, tail 1.0 s `-38.35 dBFS` (zero gaps).
- **Cut boundary split-word check:** `0` words split across all `11` cut boundaries (`words.json` vs `cuts.json`).
- **71-word verbatim lock check:** Normalized token match against `every_planet_explained_script_master_v04.md` = `True` (`71` whitespace words / `73` normalized tokens).

### 5.2 All 7 Automated Gates + Canonical 13-Bed NAS MP3 Music Check (Re-Run Independently)

1. **`gate_shorts_open.py check` (`--air-date 2026-12-28`):** **PASS (`rc=0`)** — `dur=30.75s` (Test A opening exemption), `audio=-17.0dB`, `motion=13.32`, `f0diff=5.66`, `cut1=2.5s`, `vo_onset=0.07s`, `tail_gap=1.11s`, `visor=0.0`, `0/31` (1 fps) and `0/62` (2 fps) padded frames.
2. **`thumb_preview.py short --score`:** **PASS (`rc=0`)** — `frame0`: `saturation=118.3`, `near_black=1%`; `cover`: `saturation=145.3`, `near_black=1%`.
3. **`sfx_kit.py level`:** **PASS (`rc=0`)** — `VO -16.1 LUFS`, `SFX -40.6 LUFS`, `6` hits.
4. **`music_gate.py` (default + canonical 13-bed NAS `.mp3` `--others` check):** **PASS (`rc=0`)** default AND **PASS (`rc=0`, `0` warnings)** against all `13` other canonical non-`._*` NAS OWB `.mp3` beds (`every_planet_score_bed_v01.mp3`, `701.9 s`, `70.6 BPM` vs `68-76 BPM`).
5. **`polish_gate.py`:** **PASS (`rc=0`)** — `0/12` rows failed, `1` WARN (`R04a PIA11364.jpg`, visually cleared above).
6. **`picture_qa.py`:** **PASS (`rc=0`)** — `0/12` cuts fail, `5` WARNs (all visually cleared above).
7. **`orbit_cfr_delivery.assess_playback_health`:** **PASS (`ok: true`, `0` errors, `0` warnings)** — `1080×1920`, `24/1` CFR (`libx264`, `yuv420p`), AAC `48 kHz` stereo, `video_duration=30.75`, `audio_duration=30.7`.

### 5.3 Upload Package, SRT, Dry-Run, Security & Calendar Guard

- **`youtube:package --dry-run` (against PR #1399 `PACKAGE_MANIFEST.json` + NAS `v03.mp4`):** **PASS (`rc=0`, `ok: true`, `dryRun: true`)** — `sha256: 538464b9addf45088affe5e09146cec7324351d2e18552a41d66bb4d89bac402`, `privacyStatus: "private"`, `publishAt: null`, `madeForKids: false`, `containsSyntheticMedia: true`, `categoryId: "28"`, `contentFormat: "shorts"`, `tagCount: 8`.
- **Captions (`064_short01_testA_opening_v03_en-GB.srt`):** `29` cues (`00:00:00,100 --> 00:00:29,639`), all `71` words covered with clean punctuation preserved and `6` cues covering `9–14 s`; git copy matches NAS SHA-256 `a61a7370…`.
- **Calendar & Policy Guard:** `doNotUploadBeforeLongPublic: "2026-12-16T18:00:00Z"`; candidate slot `2026-12-28T11:30:00.000Z` (Monday) is strictly after Wed 16 Dec 18:00 London long air and is **not scheduled**.
- **Privacy & Hygiene (PR #1399 `961a0b19d5`):** `52` changed files, **`0` media files in git**; `test_email_ratchet.py` + `test_no_private_network.py` = **13/13 tests OK (`rc=0`)**.

---

## 6. Routing to Elected Chief (`codex`)

`J3923` independent audio + moving-video QA on immutable **`v03`** (`sha256: 538464b9addf45088affe5e09146cec7324351d2e18552a41d66bb4d89bac402`) is complete with a **`KEEP`** recommendation:
1. Elected Chief (`codex`) reviews this exact-hash evidence for **PR #1399** (`961a0b19d5`) and decides PASS / merge.
2. Only after Chief PASS and merge may `J3903` register `064_short01_testA_opening_v03.mp4` (`538464b9…`) for Ben's phone UAT watch (`jobs.py awaits`).
3. No upload, scheduling, privacy, Buffer, or spend action has been taken; Short 1 must never upload or air before `OWB:064` long goes public on Wed 16 Dec 2026 18:00 London.
