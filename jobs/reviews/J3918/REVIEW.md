# J3918 — Independent QA Review of OWB:064 Short 1 (`Test A` Opening `v02`, PR #1399)

- **Job:** `J3918` (`kind: qa`, `ref: J3903`, `board: 064 edit`)
- **Film:** `OWB:064` — *Every Planet Explained in 12 Minutes (Mercury to Neptune)* (`02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes`, planned long air **Wed 16 Dec 2026 18:00 London**)
- **Candidate PR:** `TheLaughingGod1986/orbit-with-ben#1399` (branch `gemini/J3903-owb064-short1-testa-v02`, HEAD `1faedeab317a396119e2dbf33bb81eee691289a8`, base `main`; CI `Rules check` green, `Studio core check` skipped)
- **Canonical NAS Master Reviewed (`v02`):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/10_Shorts/short01_testA_opening/06_Final-Exports/064_short01_testA_opening_v02.mp4` (`sha256: 8b7a218c73b1c790f722f4410e67e4fe04d7e06276e3d4a4bbcbceed38c38968`)
- **Preserved Prior Draft (`v01`):** `064_short01_testA_opening_v01.mp4` (`sha256: b805c51d02acd0e43adf9c9645c993c91d148641e068e918d93136e20b25a4b6`, verified untouched on NAS)
- **Reviewer:** `gemini` (specialist worker on the Mac mini, dispatched via fallback chain while `claude` is out of usage until `2026-11-27T17:50:00Z`; `chief_relay.py status` elects **Chief: Codex (`codex` UP)**). Note for transparency: `J3903` was assembled by a prior `gemini` worker run; this fresh `gemini` session re-verified every artifact from scratch and routes the `FIX` ruling to elected Chief (`codex`).
- **Timestamp:** `2026-11-27T15:48Z`
- **Spend / Publishing Guard:** **£0 cash, 0 ElevenLabs chars, 0 Flow/Vertex credits.** Zero uploads, scheduling, privacy edits, Buffer changes, PR merges, or Ben UAT watch registration.
- **Honest Capability Scope:** Recorded via `chief_relay.py capabilities --agent gemini --available "audio_input"`. In this session, `read_file` natively decoded `064_short01_testA_opening_v02_vo.wav`, `v02_mix.mp3`, and `vo_6p5_to_30p75.mp3` and directly heard missing narration after `6.6 s` and `11.5 s`, which was then confirmed sample-exact (`-180.0 dBFS`, `peak=0.000`) via Python `wave`/`numpy`. Video `read_file` returns 1 fps sampled keyframes only, so **`moving_video_input` is NOT claimed**; visual verification used 24 independently extracted frame-exact PNGs plus the NAS contact sheets, and Ben's phone UAT watch remains required for final moving-video and full-playback approval once `v03` is rebuilt.

---

## Verdict & Recommendation to Elected Chief (`codex`)

**VERDICT: `FIX` — DO NOT PASS OR MERGE PR #1399, AND DO NOT REGISTER `v02` FOR BEN'S UAT WATCH.**

- **Picture & Packaging (`v02` video stream + metadata/SRT/covers): `KEEP`-grade** — full-bleed `9:16` framing, Frame 0, title/graphic non-overlap, animated `7.0× SUNLIGHT` and `-180 °C NIGHT` explainers, `1965 · GIUSEPPE COLOMBO` teach pill, matched Mercury loop return, 29-cue `en-GB.srt`, `PACKAGE_MANIFEST.json`, security/privacy checks, and all 7 automated gates + canonical 13-bed MP3 music check are clean.
- **Audio / Voiceover (`v02` VO stem & muxed MP4): CRITICAL `FIX` (blocking)** — **22 of 31 seconds of narration are dead digital silence (`-180.0 dBFS`, `peak=0.000`)** in both `064_short01_testA_opening_v02_vo.wav` and the final muxed `064_short01_testA_opening_v02.mp4` (and the same bug was present in preserved `v01`). Only ~7.9 seconds of speech survived (`0.1–6.53 s` and `10.17–11.52 s`); Sentences 2, 3 (after `"At fifty-eight million"`), and 4 are completely silent, leaving music-only playback underneath burned-in captions from `6.53–10.17 s` and `11.52–30.75 s`.

---

## 1. Critical Blocking Defect — Exact Root Cause & Measured Proof

### Measured Audio Evidence (`064_short01_testA_opening_v02_vo.wav` & `v02.mp4`)

1. **Direct audio check (`audio_input` via `read_file` on `064_short01_testA_opening_v02_vo.wav`, `v02_mix.mp3`, and `vo_6p5_to_30p75.mp3`):**
   - Heard narration from `0–6.5 s` (*"On Mercury, the Sun's closest planet, why does water ice survive 430-degree heat?"*), followed by **complete voice silence** where Sentence 2 should be, then only *"At 58 million"* around `10–11.5 s`, followed by **music-only silence (zero voice)** for the entire remaining ~19 seconds.
2. **Sample-level DSP proof (`wave` + `numpy`, 1-second RMS & peak across all 31 seconds):**
   - **Locked parent VO (`every_planet_explained_vo_v01.wav`, SHA-256 `4b478fcd…`, `48 kHz` stereo):** `35/35` active seconds across `0–35 s` (`0` zero-peak seconds).
   - **Short 1 `v02` VO stem (`064_short01_testA_opening_v02_vo.wav`, `30.750 s`, `48 kHz` stereo):** **Only `9/31` active seconds (`0–6 s`, `10–11 s`); `22/31` seconds are exact zero (`rms = -180.0 dBFS`, `peak = 0.000`)**:
     - `0–7 s`: active (`-16.6` to `-28.9 dBFS`, `peak 0.358–0.841`) — S1 (*"On Mercury ... heat?"*)
     - `7–10 s`: **`-180.0 dBFS`, `peak=0.000`** — S2 (*"The ice hides in polar craters that never see sunlight."*) **completely missing**
     - `10–12 s`: active (`-17.7` to `-21.6 dBFS`, `peak 0.478–0.833`) — only *"At fifty-eight million"* of S3
     - `12–31 s`: **`-180.0 dBFS`, `peak=0.000`** — rest of S3 (*"kilometres out ... minus one hundred and eighty degrees Celsius."*) and all of S4 (*"In 1965, Italian mathematician Giuseppe Colombo solved its spin mystery."*) **completely missing**
   - **Final muxed `v02.mp4` audio (`aac 48 kHz stereo`):** shows speech energy only at `0–7 s` (`-12.5` to `-21.0 dBFS`) and `10–12 s` (`-13.8 dBFS`), dropping to bed-only levels (`-21` to `-29 dBFS`, swelling to `-14 dBFS` during a louder music passage at `22–23 s`) everywhere else.
   - **Bed & SFX stems (`v02_bed.wav`, `v02_sfx.wav`):** Verified non-silent (`bed.wav` `0/31` zero seconds, `-31.4` to `-45.4 dBFS`; `sfx.wav` has its 6 expected hits at `0.00`, `0.20`, `9.00`, `14.08`, `20.04`, `23.75 s`). Note: `bed.wav` used `-ss 0.0` **before** `-i`, so the bed did not trigger the bug.
   - **Why all 7 automated gates still printed `PASS`:** `gate_shorts_open.py` only checks `vo_onset` (`0.07 s`), overall audio loudness (`-16.1 dB`), and `tail_gap` against `words.json` (which was computed from parent `stt_raw.json`, NOT re-transcribed from `v02_vo.wav`); `sfx_kit.py level` only checks VO-vs-SFX loudness on the `speaking` frames that exist; `music_gate.py` checks the bed, not speech coverage.

### Exact Code Bug (`_build_064_short01_testA_v02.py`, lines `1068–1073`)

```python
        run([
            "ffmpeg", "-y", "-v", "error", "-i", str(VO_WAV),
            "-ss", f"{sl['a']:.3f}", "-t", f"{seg:.3f}",
            "-af", f"afade=t=in:d=0.008,afade=t=out:st={max(0.0, seg - 0.008):.3f}:d=0.008",
            "-ar", str(SR), "-ac", "2", str(p),
        ])
```

Because `-ss {sl['a']}` is placed **after** `-i` (output seeking), `ffmpeg` applies `-af afade=t=out:st={seg - 0.008}` on the **original input timestamps starting from `0.000 s`** *before* trimming at `-ss`:
- **Segment 0 (`0.060–6.600 s`, `seg=6.540 s`):** fades out at input `6.532 s` (68 ms early, clipping the tail margin after `"heat?"` ending at `6.520 s`).
- **Segment 1 (`7.560–11.050 s`, `seg=3.490 s`):** fades to `0.000` at input `3.482 s`, so the slice `7.560–11.050 s` is **100% silence**.
- **Segment 2 (`11.890–25.140 s`, `seg=13.250 s`):** fades to `0.000` at input `13.242 s`, keeping only `11.890–13.242 s` (`1.35 s`, *"At fifty-eight million"*) and **zeroing `13.250–25.140 s`**.
- **Segment 3 (`26.280–32.600 s`, `seg=6.320 s`):** fades to `0.000` at input `6.312 s`, so the slice `26.280–32.600 s` is **100% silence**.

*(Independent verification of `VO_SEGMENTS` against parent `stt_raw.json`: the segment intervals themselves are accurate — `16 + 10 + 35 + 10 = 71` exact words with `70–121 ms` clean tail margins and `700 ms` clearance before word 71 `"Mercury"` at `33.300 s`. Only the ffmpeg seek/fade ordering is broken.)*

---

## 2. Independent Verification of Everything Else (All Clean on `v02`)

Every non-audio requirement in the `J3918` brief was independently verified directly against NAS files and PR #1399 (`1faedeab31`):

1. **NAS SHA-256 & `v01` Preservation:**
   - Canonical NAS `064_short01_testA_opening_v02.mp4`: `8b7a218c73b1c790f722f4410e67e4fe04d7e06276e3d4a4bbcbceed38c38968` (`75,099,301` bytes; mirrored `10_Shorts/064_short01_testA_opening_v02.mp4` identical).
   - Preserved `064_short01_testA_opening_v01.mp4`: `b805c51d02acd0e43adf9c9645c993c91d148641e068e918d93136e20b25a4b6` (untouched).
   - `frame0.jpg` (`0e05827a…`), `cover.jpg` (`0e5b9937…`), and locked parent inputs (`master_v03` `d59057ae…`, `vo_v01` `4b478fcd…`, `bed_v01` `3e47e9d6…`) all match declared hashes byte-for-byte.
   - `ffprobe`: `1080×1920`, `h264`, `yuv420p`, `24/1` CFR (`r_frame_rate=avg_frame_rate=24/1`), `738` frames = `30.750 s`, AAC `48 kHz` stereo (`256 kbps`), full `ffmpeg` decode clean (`I = -14.1 LUFS`, `LRA = 7.5 LU`, `TP = -2.1 dBFS`).
2. **Visual Framing, Overlays, Graphics & Loop (24 Independently Extracted Frames + NAS Sheets):**
   - **Full-bleed 9:16:** `0/31` padded at 1 fps, `0/62` at 2 fps (`visor=0.0`).
   - **Exact Frame 0 (`f=0`):** Rotating MESSENGER Mercury globe, crisp `ICE AT` (white) / `430°C?` (`#FFE000`) above the planet, zero Orbit, zero premature subtitle (`MAD(mp4_f0, frame0_jpg) = 2.211`; clear rotation by `f=24`, `MAD = 17.441`). Separate `cover.jpg` centers `ICE AT / 430°C?` inside the 16:9/1:1 grid crop for phone legibility (`cover_preview.jpg` verified).
   - **Title vs `R03b` separation:** Title banner `Every Planet Explained / in 12 Minutes / (Mercury to Neptune)` (exact match to parent 064 `PACKAGE_MANIFEST.json`) runs `9.00–14.00 s` over `PIA19411`→`PIA15162`, fades out completely before `f=337` (`14.04 s`), and `R03b` enters cleanly at `f=338` (`14.083 s`) with **zero overlap**.
   - **Word-matched graphics & separation:** `R03b` (`14.083–16.417 s`) animates `58 MILLION KM` / `UP TO 7.0× SUNLIGHT` / `BRIGHTER THAN EARTH` (all labels ≤4 words), separated by real moving `PIA17386` (`R03c`, `16.417–20.042 s`) from `R03d` (`20.042–23.458 s`, `WITHOUT AN ATMOSPHERE` / `+430 °C HEAT` / `-180 °C NIGHT` / `NIGHT PLUNGE`).
   - **`1965 · GIUSEPPE COLOMBO` pill:** Appears `23.75–27.70 s` (`3.95 s <= 4.00 s`) at consistent lower-third height (`y_offset=-90`) across `R04a`→`R04b`, covering spoken `"1965"` (`23.70 s`) through `"Colombo"` (`27.64 s`), gone by `28.00 s`.
   - **Loop return & end card:** `R01_loop` (`29.750–30.750 s`) returns smoothly to the rotating Mercury globe with exact parent title + yellow `Full film on the channel`.
   - **Zero split words across all 11 cut boundaries** (independently verified against `words.json` and `cuts.json`).
3. **Package, Captions, Security & Calendar Guard (`PR #1399` at `1faedeab31`):**
   - `22` changed files, **`0` media files in git**, **`0` privacy hits** (`test_email_ratchet.py`: 8/8 OK; `test_no_private_network.py`: 5/5 OK).
   - `064_short01_testA_opening_v02_en-GB.srt`: `29` cues, `71/71` words (`00:00:00,100 --> 00:00:29,639`), `0` timing overlaps, `6` cues covering `9–14 s` (zero caption gap). *(Minor non-blocking polish note: `srt_chunks_full()` strips commas and full stops from cue text while keeping `?`; optional to preserve punctuation in `v03`.)*
   - `PACKAGE_MANIFEST.json`: `npm run youtube:package --dry-run` resolved cleanly (`ok: true`, `privacyStatus: "private"`, `publishAt: null`, `madeForKids: false`, `containsSyntheticMedia: true`, `categoryId: "28"`, `format: "shorts"`, `8` tags, `1,553`-char description, `doNotUploadBeforeLongPublic: "2026-12-16T18:00:00Z"`). Candidate `2026-12-28` is a Monday (valid `Mon/Wed/Fri/Sat 11:30` Orbit Short day) strictly after Wed 16 Dec long air, and is not scheduled.
4. **All 7 Automated Gates + Canonical 13-Bed MP3 Music Check (Re-Run Independently on NAS `v02`):**
   - `gate_shorts_open.py --air-date 2026-12-28`: **PASS (`rc=0`)** (`0/62` padded, `f0diff=5.66`, `motion=13.32`, `cut1=2.5s`, `vo_onset=0.07s`, `tail_gap=1.11s`, `visor=0.0`; `30.75s` warn exempt for Test A).
   - `thumb_preview.py short --score`: **PASS (`rc=0`)** (`frame0` sat `118.3` / `1%` near-black; `cover` sat `145.3` / `1%` near-black).
   - `sfx_kit.py level`: **PASS (`rc=0`)** (`VO -16.0 LUFS`, `SFX -40.6 LUFS`, `6` hits).
   - `music_gate.py`: **PASS (`rc=0`)** default + **PASS (`rc=0`, `0` warnings)** against all 13 readable non-`._*` NAS OWB `.mp3` beds (`70.6 BPM` vs `68-76 BPM`).
   - `polish_gate.py`: **PASS (`rc=0`)** (`0/12` fail, 1 inspected WARN `R04a` `PIA11364.jpg`).
   - `picture_qa.py`: **PASS (`rc=0`)** (`0/12` fail, 5 inspected WARNs on `picture_qa_review.jpg` — all real NASA MESSENGER imagery, clean).
   - `orbit_cfr_delivery.assess_playback_health(probe_json(mp4))`: **PASS (`ok: true`, `0` errors, `0` warnings)**.

---

## 3. Exact Required Fix List (Single Clean `v03` Audio Repair — £0, 0 Credits)

Do **not** overwrite `v01` or `v02` on the NAS (`AGENTS.md` version preservation rule). Produce **`064_short01_testA_opening_v03.mp4`** (and `v03` sidecars/manifest/reports on PR #1399) with:

1. **[Required] Fix `build_audio()` VO segment slicing** in `_build_064_short01_testA_v03.py` (replacing lines `1068–1073`):
   - Either slice directly in NumPy from `read_wav(VO_WAV)` using `int(round(a * SR)) : int(round(b * SR))` with exact 8 ms linear fade-in/fade-out ramps, **or** place `-ss` **before** `-i` (or use `atrim=start={a}:end={b},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.008,afade=t=out:st={seg-0.008}:d=0.008`).
   - Re-run VO normalization (`I=-16`), bed ducking against the *complete* 71-word VO stem, SFX level adjustment, final mix (`I=-14.0 LUFS`, `TP <= -1.85 dBTP`), and AAC `48 kHz` stereo encode.
   - **Fast & exact video reuse allowed:** Because `v02`'s video stream (`738` frames, `24/1` CFR, `1080×1920`, all visual overlays/captions/graphics/loop verified) is already clean, `v03` may either stream-copy `v02`'s video track (`-c:v copy`) with the repaired AAC audio track or re-run the fixed builder cleanly.
2. **[Required] Add an explicit VO-coverage assertion before finishing `v03`:**
   - Assert every one of the 4 VO segments in `064_short01_testA_opening_v03_vo.wav` has active speech energy (`RMS > -30 dBFS` and zero unexpected 1-second `-180 dBFS` drop-outs inside `0.1–6.5 s`, `6.6–10.0 s`, `10.2–23.4 s`, `23.5–29.6 s`), and record the per-segment RMS table in `GATE_REPORT_v03.md`.
3. **[Required] Re-run all 7 automated gates + canonical 13-bed MP3 music gate + `youtube:package --dry-run` on canonical NAS `v03`**, update `PACKAGE_MANIFEST.json` (`video`, `masterSha256`, `captionsFile`) and `SHORT1_BRIEF_AND_CHECKLIST_v03.md` (preserving `v01` and `v02` untouched on NAS), and submit for a quick independent recheck before Chief PASS / merge and Ben's phone UAT watch.
4. **[Optional hygiene, same pass]:** Preserve commas and full stops from `words.json` in `064_short01_testA_opening_v03_en-GB.srt` for cleaner closed captions.

---

## 4. Elected-Chief Next Steps

Because `gemini` is a specialist worker and **Codex (`codex`)** is elected Chief:
1. Elected Chief reviews this `FIX` report, withholds PASS and merge on PR #1399 (`1faedeab31`), and keeps `J3903` from registering `v02` for Ben's UAT watch.
2. Elected Chief queues/reopens the £0 `v03` audio-slicing repair on PR #1399 (preserving `v01` and `v02` on NAS), followed by a targeted `v03` audio + gate recheck before PASS, PR merge, and Ben's phone UAT watch (`jobs.py awaits`).
