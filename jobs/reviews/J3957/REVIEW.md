# Independent Audio & Moving-Video QA Review — OWB 064 Short 2 (`v01`, `J3957`)

- **Job:** `J3957` (`kind: qa`, `ref: J3904`, board: `064 edit`)
- **Reviewer:** `gemini` (specialist worker — NOT elected Chief; elected Chief is `codex`)
- **Date:** 2026-11-27
- **Reviewed Target:** `OWB:064` Companion Short 2 (*Venus 464°C vs Uranus −224°C*) **`v01`** on **PR #1416** (branch `gemini/J3904-owb064-short2-v01`, head `f67c2dcbe207ca34e3810da167ccfc8bfc56e51d`, parent `J3904`)
- **Verdict:** **`KEEP` (recommended to elected Chief `codex`)**
- **Authority Boundary:** This is independent specialist-worker QA evidence, **not** a Chief PASS, PR merge, or Ben UAT registration (`jobs.py awaits`). Only elected Chief (`codex`) PASS and merge of PR #1416 (`f67c2dcbe207ca34e3810da167ccfc8bfc56e51d`) may release `J3904` for Ben's phone UAT watch. Zero upload, scheduling, privacy, Buffer, generation, or spend actions were performed (`£0.00` cash, `0` credits).

---

## 1. Demonstrated Reviewer Capabilities (Recorded via `chief_relay.py capabilities`)

- **`audio_input` (demonstrated):** Directly listened via native `read_file` in this session to:
  - Raw VO take `02_Voiceover/064_short02_venus_vs_uranus_vo_v01.wav` (`78b17500…`)
  - Trimmed VO stem `06_Final-Exports/064_short02_venus_vs_uranus_v01_vo.wav` (`dd9c444d…`)
  - Ducked music bed stem `06_Final-Exports/064_short02_venus_vs_uranus_v01_bed.wav` (`f4c2e424…`)
  - House SFX stem `06_Final-Exports/064_short02_venus_vs_uranus_v01_sfx.wav` (`b08b5c56…`)
  - Full final mix inside canonical NAS `064_short02_venus_vs_uranus_v01.mp4` (`4eb7d943…`) and concatenated loop-seam playback (`16.375–18.375 s` → `0.000–2.000 s`).
  - Neither ASR nor DSP measurements were substituted for listening.
- **`moving_video_input` (demonstrated):** Directly watched via native `read_file` in this session:
  - Complete moving `1080×1920` `9:16` playback of canonical NAS `064_short02_venus_vs_uranus_v01.mp4` (`4eb7d943…`, `00:00–00:18`) with synchronized final audio mix
  - Phone-size (`360×640`) moving playback of the full `18.375 s` cut
  - Forward pre-roll return clip `frame0_return_064_short02_venus_vs_uranus_v01.mp4` (`279bcd84…`) and concatenated loop-seam moving video (`16.375–18.375 s` → `0.000–2.000 s`).
  - Still frames (`picture_qa_review.jpg`, `review_8shots.jpg`, `open_sheet.jpg`, `frame0_preview.jpg`, `cover_preview.jpg`, and full-res extractions at `6.0 s`, `11.25 s`, `12.2 s`, `13.4 s`, `16.0 s`) were inspected alongside moving playback, not in place of it.
- Recorded on the Mini via `python3 scripts/chief_relay.py capabilities --agent gemini --available "audio_input,moving_video_input" --evidence "…"`.

---

## 2. Exact Canonical Hashes, Locked Script/VO & Source Provenance (**MEASURED**)

### 2.1 Canonical NAS `v01` Deliverables (All Verified on NAS & Matching PR #1416 `f67c2dcbe2`)

| File | Exact SHA-256 | Size (bytes) |
|---|---|---|
| `06_Final-Exports/064_short02_venus_vs_uranus_v01.mp4` | `4eb7d94377a9e59b9319f7ccfd9ec96091f60dbebb034c2e9ed6d75a2c6c77ff` | `27,139,489` |
| `06_Final-Exports/064_short02_venus_vs_uranus_v01_vo.wav` | `dd9c444d6ae5a2638eeec063e6ddffacc9dbb7d4a4e8a97d0e68ce60aefaa41b` | `3,528,044` |
| `06_Final-Exports/064_short02_venus_vs_uranus_v01_bed.wav` | `f4c2e424c2fba19d0847aa40fe65c93cfff5e3169282888a3ce1100bc79d750a` | `3,528,044` |
| `06_Final-Exports/064_short02_venus_vs_uranus_v01_sfx.wav` | `b08b5c564ebae92e43d7dcce2cf066e62f8a1285d531addd724f77409066db9f` | `3,528,044` |
| `06_Final-Exports/064_short02_venus_vs_uranus_v01_en-GB.srt` *(matches PR #1416 git `Captions/…`)* | `2197ea8ca1761cb23f5802779ec9ce659f5162815719db54d19300925e91d8d8` | `667` |
| `06_Final-Exports/064_short02_venus_vs_uranus_v01_frame0.jpg` | `a484c2665c622ff09b285e245f00ce1df2a41c9679790deb72fc11195f4e3590` | `197,903` |
| `06_Final-Exports/064_short02_venus_vs_uranus_v01_cover.jpg` | `b9e390f15630ff52bef83a281d73b0d164f0573e1398b5a0e4e7f778a6c7af42` | `572,152` |
| `06_Final-Exports/frame0_return_064_short02_venus_vs_uranus_v01.mp4` | `279bcd84c7c223a279ffaa8e49c90af2236f4e8840bb788721c95a11120bfcc2` | `1,900,873` |
| `02_Voiceover/064_short02_venus_vs_uranus_vo_v01.wav` | `78b17500d6a233beaf1c57e9163681ad3c6c3a955253eec17cac0ce1e511ecce` | `3,686,478` |
| `02_Voiceover/064_short02_venus_vs_uranus_vo_v01.mp3` | `d6e490df1e00d296975e4ce71dd615c6bbc004e1f718e1f54d5098884c0471aa` | `308,012` |

### 2.2 Locked Script, Authorized VO Spend & Honest NASA/ESA Source Provenance (All Verified Byte-for-Byte)

- **Locked v03 script (`064_short02_venus_vs_uranus_script_v03.md`):** SHA-256 `634da1601232b9b8debb1880203228c4b98c95c354ae21711797f176e0c80ca0` (exact match to Chief Claude's `J3917` lock; restored `"true"` qualifier in Line 2).
- **VO take & spend ledger (`064_short02_venus_vs_uranus_vo_v01_TAKE.json`):** `Ben Orbit Narrator` (`kDch6ACCIpqgQ0NsU9kk`), `eleven_v3`, speed `1.04`, **`205` chars spent (`<= 600` Chief cap)**, live subscription balance before spend `7,275`, `vo_check: PASS`, Scribe `97.14%` (sole token diff `"minus 224?"` → `"-224?"`). Properly logged in both `04_Audio/elevenlabs_ledger.jsonl` and `05_Analytics/ai_spend/ledger.jsonl` (`£0.00` cash, `0` Flow/Vertex credits).
- **Score bed (`05_Music/every_planet_score_bed_v01.mp3`):** SHA-256 `3e47e9d6da9aca6836a00c27a1fa58e53801190ae06ed445966ed51f5c0d75c6`.
- **All 7 NASA/ESA visual sources verified on NAS (zero Veo CGI, zero Keck misattribution):**
  - `svs14095_14095_ParkerVenus_YouTube_NoText_NoMusic.mp4` (`R01`, `R08_loop`): `ebb967994b150bc878f31ccb36107adaf99bb1fa7f0217e7516556a40833849e`
  - `AIA171VenusTransit_HD1080.mp4` (`R02`): `e580945d4b767e7ed3524636d61520f1b03210c814e348727b18ed9e507d30fc`
  - `svs20390_Shot8_4k.mp4` (`R03`, native 4K Uranus, `1.18×` upscale): `8345caca2a6cc4291554f19f86f1c2b98ceb777817c1c82a17f15fe83f761726`
  - `weic2332a_hires.jpg` (`R04`, ESA/Webb JWST NIRCam, CC BY 4.0): `b241901c2754e811c0706480c17e6ea8899cd1cf9698ee2ac389c6c3d1ee320e`
  - `PIA01488.jpg` (`R05`, NASA/JPL Voyager 2 Uranus, `0.79×`): `9c49e13d8da1c052f8bda283a4df0d2a054840b03bb175c90454d2049d80a86b`
  - `svs14095_WISPR_Magellan_3rdFlyby.mp4` (`R06`, NASA/JHUAPL/NRL): `4b3d0c25e309e10da68dc4ca964ab6175875c8dd8313fe8b2b9d059005b27604`
  - `PIA00215.jpg` (`R07`, NASA/JPL Magellan SAR Venus): `46dc965a02d4bff533685892ad16a76845a384d482ffaedda024c870b5b8a7b4`

---

## 3. Independent **HEARD** Evidence (`audio_input`)

Directly listened in full to the raw VO take, trimmed VO stem, ducked music bed stem, house SFX stem, full final master mix (`064_short02_venus_vs_uranus_v01.mp4`), phone-size copy, and concatenated loop-seam playback (`16.375–18.375 s` → `0.000–2.000 s`):

- **All 3 sentences & all 35 spoken words heard verbatim (matching locked v03 script):**
  1. **S1 (`0.06–7.4 s`):** *"Why is Venus's surface four hundred and sixty-four degrees Celsius, while Uranus's air drops to minus two hundred and twenty-four?"* — clean, immediate entry on *"Why"*, crisp articulation of both temperatures, natural rising question intonation on *"224?"*, zero clipping or breath artifacts.
  2. **S2 (`8.3–11.9 s`):** *"Uranus has no true surface; that's its coldest air."* — the restored *"true"* qualifier is clearly spoken, natural 0.16 s breath before S2, zero pops or clipped edges.
  3. **S3 (`12.2–17.46 s`):** *"On Venus, thick carbon dioxide air traps heat in a runaway greenhouse."* — punchy delivery on the late payoff (*"traps heat in a runaway greenhouse"* starting at `14.92 s` / `81.2%`), clean consonant finish on *"greenhouse"* with zero trailing truncation.
- **VO / bed / SFX mix balance:**
  - Narration sits cleanly forward throughout (`VO -16.0 LUFS` stem; final master independently measured `-14.13 LUFS` / `-1.96 dBTP` via `ffmpeg loudnorm`).
  - Score bed (`every_planet_score_bed_v01.mp3`, `70.6 BPM`, `-34.3 LUFS` stem) is warm and atmospheric beneath speech, never masks consonants, and swells smoothly in the `0.915 s` tail after *"greenhouse"*.
  - House SFX (`-40.1 LUFS`, 7 restrained hits: soft opening whoosh, R03 whoosh, subtle ticks on the 9 s title and 14.9 s Teach pill, soft low rumbles) stay well under speech with zero harshness.
- **Music & loop seam continuity:** Direct audition of the concatenated loop-seam clip confirms continuous score bed across the `18.375 s → 0.000 s` wrap with zero clicks, pops, or silent dropouts; the soft opening whoosh bridges cleanly back into *"Why is Venus's surface…"*.

---

## 4. Independent **WATCHED** Evidence (`moving_video_input` + Phone-Size & Flagged-Frame Inspection)

Directly watched full `1080×1920` moving playback (`00:00–00:18`), full `360×640` phone-size moving playback, `frame0_return_064_short02_venus_vs_uranus_v01.mp4`, and the concatenated `loop_seam.mp4`, plus inspected `picture_qa_review.jpg`, `review_8shots.jpg`, `open_sheet.jpg`, `frame0_preview.jpg`, `cover_preview.jpg`, and full-res frames (`6.0 s`, `11.25 s`, `12.2 s`, `13.4 s`, `16.0 s`):

- **Frame-0 golden Venus motion (`R01`, `0.000–1.750 s`):** Full-bleed `9:16` moving NASA SVS 14095 sunlit golden Venus limb with Parker Solar Probe boom on the right edge, zero Orbit, zero padding. Burned-in hook **`464°C VENUS`** (`#FFE000`) / **`VS −224°C?`** (`#FFFFFF`) is bold, high-contrast, immediately readable at phone size (`360×640`), and fades cleanly by `2.1 s`.
- **Full-bleed `9:16` framing across all 8 shots:** Every shot (`R01–R08_loop`) fills `1080×1920` edge-to-edge with zero bars, zero blurred/mirrored padding, and zero flat black slabs.
- **R02 (`1.750–4.208 s`, SDO AIA 171 Å Venus transit):** Crisp moving golden solar corona with Venus clearly visible transiting in upper-left; timestamp cleanly cropped out.
- **R03 Flagged Frame Inspection (`4.208–8.167 s`, `svs20390_Shot8_4k.mp4`, WARN `edge density 0.0211 < film p5 0.0220`):**
  - **Result: FALSE POSITIVE — CRISP KEEP.** Native 4K (`1.18×` upscale) NASA Goddard SVS 20390 Uranus displays crisp tilted rings at top-left, sharp starfield, and smooth cyan cloud bands both in motion and full-res (`r03_6s.jpg`, `picture_qa_review.jpg`). Edge density is `0.0211` solely because Uranus's real cyan haze is naturally smooth, not because of blur or low resolution.
- **9–14 s Exact Long Title Banner (`9.00–14.00 s` across R04 JWST Uranus, R05 Voyager 2 Uranus, R06 WISPR/Magellan Venus):**
  - Exact verbatim parent long title **`Every Planet Explained / in 12 Minutes / (Mercury to Neptune)`** centered inside the `16:9` safe band (`y=833..1098`), crisp white bold type with heavy black outline, completely legible at phone size across all three shots. Burned-in bottom captions intentionally pause during `9.00–14.00 s` to prevent text collision (while `en-GB.srt` preserves all 14 cues across `0.060–17.460 s`).
- **R06 (`12.042–14.875 s`, NASA WISPR/Magellan 3rd flyby):** Smoothly cycles between false-color Magellan radar topography and WISPR night-side thermal glow with dust streaks; vivid and sharp.
- **R07 & Teach Pill (`14.875–17.500 s`, Magellan SAR `PIA00215.jpg`):** Crisp radar volcanic pancake domes filling `9:16`. Single Teach pill **`464°C · RUNAWAY GREENHOUSE`** enters at `14.90 s` (strictly after `14.00 s` title clears) and exits at `17.45 s` (`2.55 s <= 4.0 s`), centered cleanly inside the `16:9` band (`y=1179..1230`), 3 words (`<= 4`), verbatim match to VO, clearly separated above the lower captions (`AIR TRAPS HEAT` / `IN A RUNAWAY` / `GREENHOUSE`) with zero overlap and crisp legibility at phone size.
- **R08 Loop Return (`17.500–18.375 s` → `0.000 s`):** Watched live in `loop_seam.mp4` — smooth forward pre-roll on the exact NASA SVS 14095 golden Venus limb glides cleanly into Frame 0's exact geometry with zero jump cut.
- **Cover & Frame-0 Phone Previews (`cover_preview.jpg`, `frame0_preview.jpg`):** `464°C VENUS / VS −224°C?` fits cleanly inside both `9:16` feed and `16:9` shelf crop with zero clipping and crisp legibility at small tile size.
- **Minor non-blocking polish observations (logged transparently, not blockers):**
  1. `PACKAGE_MANIFEST.json` description places the `Pictures:` honesty line immediately before `Image credits:` rather than after it (`studio/RULES.md` §Reference lessons 2 lists `Image credits` then `Pictures:`; minor section-order hygiene only — all required sources, honest disclosure, and CC BY 4.0 URL are present).
  2. On the unlit left nightside terminator of Venus in `R01`/`R08_loop` (`svs14095`), dark compression/compositing stepping is faintly visible full-size, and on `R05` (`PIA01488.jpg`, `1.58 s` under the title banner) historical Voyager 2 scan grain plus faint star bleed through the dark limb are visible full-size; both are minor and read cleanly at phone size in motion.
  3. Cover JPG reuses the Frame 0 golden Venus plate (clean, high contrast, `sat=194.5, nb=2%`; `THUMBNAIL_AND_TITLE_RULES.md` §4.3 prefers a different plate when convenient, soft guidance only).
  4. `064_short02_venus_vs_uranus_v01_en-GB.srt` cue 14 ends `greenhouse` without a trailing period (harmless).
  5. `PACKAGE_MANIFEST.json` pre-populates candidate `"schedule": "2026-12-30T11:30:00.000Z"` (strictly after Wed 16 Dec 18:00 London long air) with `"privacy": "private"`; nothing is uploaded or scheduled.

---

## 5. Independent **MEASURED** Evidence (All 7 Automated Gates, Fresh ASR, Coverage & Hygiene)

1. **`gate_shorts_open.py check --air-date 2026-12-30`:** **PASS (`rc=0`, 0 warnings)** — `dur=18.38s` (inside `16.0–19.0 s`), `audio=-16.6dB`, `motion=10.18`, `f0diff=2.04`, `cut1=1.75s`, `vo_onset=0.05s`, `tail_gap=0.91s`, `visor=0.0004`, `0/19` (1 fps) & `0/37` (2 fps) padded frames.
2. **`thumb_preview.py short --score`:** **PASS (`rc=0`)** — Frame 0 `saturation=161.8, near_black=2%`; Cover `saturation=194.5, near_black=2%`.
3. **`sfx_kit.py level`:** **PASS (`rc=0`)** — `VO -16.0 LUFS, SFX -40.1 LUFS, 7 hits`.
4. **`music_gate.py` (default + canonical 13-bed NAS `.mp3` `--others`):** **PASS (`rc=0`, 0 warnings)** — `every_planet_score_bed_v01.mp3`, `701.9 s`, `70.6 BPM`, brief `Pace: 68-76 BPM`.
5. **`polish_gate.py`:** **PASS (`rc=0`)** — `0/8` rows failed, `1` WARN (`R03 svs20390_Shot8_4k.mp4`, visually cleared above).
6. **`picture_qa.py`:** **PASS (`rc=0`)** — `0/8` cuts fail, `1` WARN (`R03 svs20390_Shot8_4k.mp4`, visually cleared above).
7. **`youtube:package --dry-run` (against detached PR #1416 `f67c2dcbe2` worktree + canonical NAS master):** **PASS (`rc=0`, `ok: true`, `dryRun: true`)** — `privacy: "private"`, `tagCount: 9`, `madeForKids: false`, `syntheticDisclosure: true`, `scheduledAt: "2026-12-30T11:30:00.000Z"`, NOT uploaded, NOT scheduled.
8. **`orbit_cfr_delivery.assess_playback_health`:** **PASS (`ok: true`, `0` errors, `0` warnings)** — `1080×1920`, `24/1` CFR (`441` frames, `libx264`, `yuv420p`), AAC `48 kHz` stereo, `video_duration=18.375`, `audio_duration=18.35`.
9. **Independent `ffmpeg loudnorm` on canonical NAS mp4:** `input_i = -14.13 LUFS`, `input_tp = -1.96 dBTP`, `input_lra = 3.80 LU`.
10. **Independent speech coverage (6 segments vs raw VO WAV `78b17500…`):** **`82/82` active 200 ms windows (`100.0%`, `0` dropouts)**.
11. **Fresh independent `faster-whisper small.en` ASR on decoded PCM from canonical NAS mp4:** **`35/35` spoken words decoded verbatim** across all 3 sentences (`0.00–7.36 s`, `8.26–11.86 s`, `12.22–17.12 s`).
12. **Bed continuity & cut-boundary split-word checks:** Bed stem `18.375 s`, min 0.5 s bin `-47.82 dBFS`, tail 1.0 s `-38.36 dBFS`, head 0.2 s `-41.32 dBFS`, end 0.2 s `-44.26 dBFS` (zero gaps); **`0 / 7` split words** across cut boundaries.
13. **Git & Privacy Hygiene (PR #1416 `f67c2dcbe2`):** `28` changed files, **`0` media files committed to git**; `test_email_ratchet.py` (21 tests) + `test_no_private_network.py` (5 tests) = **26/26 OK (`rc=0`)**; PR #1416 `Rules check` CI = `SUCCESS`.

---

## 6. Routing to Elected Chief (`codex`)

`J3957` independent audio + moving-video QA on exact canonical NAS master `064_short02_venus_vs_uranus_v01.mp4` (`sha256: 4eb7d94377a9e59b9319f7ccfd9ec96091f60dbebb034c2e9ed6d75a2c6c77ff`) and **PR #1416** (`f67c2dcbe207ca34e3810da167ccfc8bfc56e51d`) is complete with a **`KEEP`** recommendation:
1. Elected Chief (`codex`) reviews this exact-hash evidence and decides PASS / merge on **PR #1416** and this review PR, and rules on **`J3904`**.
2. Only after Chief PASS and merge may `J3904` register `064_short02_venus_vs_uranus_v01.mp4` (`4eb7d943…`) for Ben's phone UAT watch (`jobs.py awaits`).
3. No upload, scheduling, privacy, Buffer, or spend action has been taken; Short 2 must never upload or air before `OWB:064` long goes public on Wed 16 Dec 2026 18:00 London.
