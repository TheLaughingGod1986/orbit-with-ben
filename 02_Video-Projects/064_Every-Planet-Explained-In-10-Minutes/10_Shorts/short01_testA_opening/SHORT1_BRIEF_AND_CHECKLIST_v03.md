# OWB 064 Short 1 (Test A Opening) — Brief & Approved Learnings Checklist (`v03`, `J3922`)

- **Film:** `OWB:064` — *Every Planet Explained in 12 Minutes (Mercury to Neptune)* (planned long air: **Wed 16 Dec 2026 18:00 London**, unchanged)
- **Short:** Companion Short 1 of 2 — **Test A Opening Short** (`studio/RULES.md` Lesson 5)
- **Stem:** `064_short01_testA_opening_v03`
- **Proposed Candidate / Gate-Check Slot:** **Mon 28 Dec 2026 11:30Z** (unchanged non-colliding `Mon/Wed/Fri/Sat 11:30 London` Orbit Short slot strictly after 064 long goes public on Wed 16 Dec 18:00 London; **NOT scheduled yet — MUST NOT upload or air before 064 long is public**)
- **Canonical NAS Master (`v03`):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/10_Shorts/short01_testA_opening/06_Final-Exports/064_short01_testA_opening_v03.mp4`
- **Master SHA-256 (`v03`):** `538464b9addf45088affe5e09146cec7324351d2e18552a41d66bb4d89bac402`
- **Audio Stems & SRT SHA-256 (`v03`):**
  - VO stem: `8483ba3e5448c5506598149ad9f2b4fe33a80ce66ae05b9d30f0f2f4aa8d7393`
  - Bed stem: `7bb8302b7fbd219aecfcb50d84a13298169ab5c4c0ac64eb1f4830460dbd02dd`
  - SFX stem: `f4f13e907d76b5f6d7781396e770c3d4e809312a60976edf1ce710908135891c`
  - SRT (`064_short01_testA_opening_v03_en-GB.srt`): `a61a737048188667682e566a9f7ec78e08ca704dd836db231d86c6d2207fa603`
- **Preserved Prior Drafts on NAS (verified bit-for-bit untouched):**
  - `v01`: `064_short01_testA_opening_v01.mp4` (`b805c51d02acd0e43adf9c9645c993c91d148641e068e918d93136e20b25a4b6`)
  - `v02`: `064_short01_testA_opening_v02.mp4` (`8b7a218c73b1c790f722f4410e67e4fe04d7e06276e3d4a4bbcbceed38c38968`)
  - `v02` upload manifest preserved verbatim at `07_Upload-Package/PACKAGE_MANIFEST_v02.json`.
- **Source Provenance (exact locked hashes verified):**
  - Parent master v03: `d59057aed1590e7f6ef097513256a0548c4f9b1d7e544c4bade28aa83fef647a`
  - Locked VO WAV: `4b478fcded393890064ffd285a4121882dc26e0515f3cadc6569adf0465616aa` (71 verbatim words S1–S4; `0` new ElevenLabs chars)
  - Film score bed: `3e47e9d6da9aca6836a00c27a1fa58e53801190ae06ed445966ed51f5c0d75c6` (`every_planet_score_bed_v01.mp3`)
- **Spend:** `£0.00` cash, `0` ElevenLabs chars, `0` Flow/Vertex credits.
- **Upload / Scheduling Status:** Not uploaded, not scheduled, not added to `shorts_open_library`, not registered for Ben UAT. Ready for dependent independent audio & moving-video QA (`J3923`) and elected-Chief ruling.

## Audio Repair Applied (`v02` → `v03`, Chief Ruling on `J3918`)

1. **Restored all 4 narration segments (71/71 spoken words):** Fixed `build_audio()` in `_build_064_short01_testA_v03.py` to apply `atrim=start=...:end=...,asetpts=PTS-STARTPTS` strictly before `afade=t=in` / `afade=t=out`, eliminating the `v02` post-input `-ss` timestamp bug that silenced S2, S3 (tail), and S4 to the ±1 LSB PCM dither floor (`-90.31 dBFS`).
2. **Re-normalized, re-ducked, re-leveled, and remixed:** VO `-16.1 LUFS`, score bed `-34.1 LUFS`, 6 house SFX hits `-40.6 LUFS`, final AAC `48 kHz` stereo `256k` calibrated to `I = -14.10 LUFS`, `TP = -2.10 dBTP`.
3. **Stream-copied `v02` video unchanged with exact verification:** Verified both encoded `streamhash` (`0,v,SHA256=d7d5e684a9672dff62f5e0cfce669685549df86f6094b1eb817c495716fd40a0`) and all `738` decoded frames via `framemd5` (`a4965b6044acedc4716847498b373e3b936d03fd4f16bd58193d60c895d14723`). Per Chief ruling on `J3918`, this video reuse is strictly for repair and is **not** a visual/motion PASS.
4. **Added speech-coverage regression test (`v02` FAIL / `v03` PASS) + fresh decoded ASR check:** Verified `100.0%` source-active 200 ms window coverage, `0` unexpected dropouts, `0` missing words, and `0.9983–0.9999` envelope correlation across S1–S4 (while old `v02` fails S2/S3/S4), plus `1.0000` (`75/75` normalized tokens, `0` diffs) fresh `faster-whisper small.en` ASR recall on freshly decoded `v03.mp4` and `v03_vo.wav` (vs `0.28` on `v02.mp4`).
5. **SRT punctuation hygiene:** `064_short01_testA_opening_v03_en-GB.srt` covers all 71 words across 29 cues (`00:00:00,100 --> 00:00:29,639`) with clean punctuation preserved.

## Approved Learnings Checklist (`10_Shorts/README.md`)

- [x] **#1 · Title:** Positive question naming the subject: *"Why Does Water Ice Survive 430°C Heat on Mercury?"* (Alt: *"How Does Mercury Hide Water Ice at 430°C?"*).
- [x] **#2 · First-second rule (`0.0–1.5 s`, `J2429`):** Full-bleed `1080×1920` (`24/1` CFR, `0/62` padded frames, `visor_frac = 0.0`), `f0diff=5.66`, `motion=13.32`, hook caption `ICE AT / 430°C?` at `0.00 s`, VO word 1 at `0.07–0.10 s`.
- [x] **#3 · Motion:** 12 full-bleed shots, max shot `3.958 s <= 4.00 s`, zero split words across all 11 cut boundaries, zero jitter in `polish_gate`.
- [x] **#6 · Payoff (Test A opening exemption):** `30.750 s` verbatim cold-open reframe (`studio/RULES.md` Lesson 5), all 4 narration sentences intact through Colombo 1965 spin-mystery cliffhanger.
- [x] **#7 · Seam:** S1→S2 breath `0.240 s < 0.25 s`, full S2/S3/S4 narration restored.
- [x] **#8 · 60% stayed-to-watch:** `f0diff=5.66`, `motion=13.32`, `vo_onset=0.07 s`, `cut1=2.50 s`, `tail_gap=1.11 s`.
- [x] **#9 · 70% average viewed:** Exact long title at `9.00–14.00 s` and End Card `29.750–30.750 s`, single Teach overlay `1965 · GIUSEPPE COLOMBO` at `23.75–27.70 s`, matched Mercury loop return to Frame 0.

## Perceptual QA & UAT Boundary

- No self-PASS, no PR merge, and no Ben UAT registration (`jobs.py awaits`) are claimed here.
- Dependent independent QA (`J3923`, `kind: qa`) is required to actually hear the restored `v03` narration/mix and review moving-video playback before elected-Chief (`codex`) ruling and Ben's phone UAT watch.
