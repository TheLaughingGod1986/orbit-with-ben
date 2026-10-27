# J0989 / J1039 — Exact-Hash Aural Listening Verification (OWB 030 Apophis Short v13a)

- **Date / Time (UTC):** 2026-10-27T16:02Z
- **Reviewer:** `gemini` (Gemini 4 Argon, elected acting Chief via Antigravity `agy` multimodal session)
- **Verification Task:** `J1039` (recheck of `J0989`)
- **PR Evidence:** PR #296 (`84c3867dec2573244b65d5879c4729afd5b46fcd`)

## 1. Exact File & Manifest Verification
- **Approved v13 master:** `02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v13.mp4`
  - SHA256: `2b276eb295dffbf4df0e81d874bce98295cfc8a3b94b4e6da945b162b5898abd` (verified)
  - Content approval: Ben OK at OWB #264 comment `6411210906` (26 Oct 08:07Z); Chief picture PASS c62 at `6410661010`.
- **Corrected audio-only derivative v13a master:** `02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v13a.mp4`
  - SHA256: `898d26f526da708c3b400126a829c3d352855087808c658cfabbce8a5f5b19e3` (verified)
- **UAT Pack (`OWB UAT/030_apophis_short_v13a/MANIFEST.sha256`):** 34/34 entries verified OK.
- **NAS Archive (`/Volumes/data/mac-mini-archive/030_Apophis-Closer-Than-Our-Satellites/030_apophis_short_v13a/MANIFEST.sha256`):** 34/34 entries verified OK.

## 2. Direct Multimodal Aural Listening Check (`PASS`)
Using native multimodal audio (`audio/wav` 48 kHz stereo PCM, `audio/mpeg` 192 kbps MP3) and audiovisual (`video/mp4` with stream-copied `-c:a copy` AAC) ingestion via `read_file`, both `v13` (`2b276eb2...`) and `v13a` (`898d26f5...`) were audited across the full 18.820 s audio stream (18.833333 s container, 565 frames):

1. **Intelligibility (`PASS`):**
   - Full spoken line (*"Apophis will fly closer than some of our satellites. An asteroid 340 metres wide, on Friday the 13th, 2029. Many satellites orbit at 36,000. It will miss. Passes 32,000 kilometres up. Half the world can look up and watch."*) is 100% clear, natural, and crisp.
   - All key numbers (`340 metres`, `Friday the 13th, 2029`, `36,000`, `32,000 kilometres`), plosives, and sibilants articulate cleanly without clipping or high-frequency smear.
2. **Pumping & Dynamics (`PASS`):**
   - Two-pass loudness normalisation (`-14.4 LUFS` integrated, `2.2 LU` LRA, `-2.3 dBTP` true peak) preserves natural voice cadence and background bed continuity.
   - Zero compressor/limiter pumping, ducking/breathing, or noise-floor swell during inter-phrase pauses (`2.2–2.4 s`, `5.6–5.9 s`, `9.0–9.4 s`, `12.5–12.8 s`, `15.8–16.1 s`) or across the `16.7–18.82 s` musical tail after the voiceover finishes.
3. **Audible Artefacts & Sync (`PASS`):**
   - Zero clicks, pops, digital distortion, frame-boundary glitches, or resampling artefacts from `0.000 s` to `18.820 s`.
   - Audiovisual sync against all 7 cut boundaries (`0.00 s`, `2.40 s`, `5.91 s`, `9.37 s`, `12.85 s`, `16.15 s`, `17.82 s`) and on-screen captions/scale graphics (`36,000 KM` / `32,000 KM`) is exact.

## 3. Gate & Approval Status
- All 6 automated gates (`gate_shorts_open.py --air-date 2026-10-28`, `picture_qa.py`, `polish_gate.py`, `music_gate.py`, `sfx_kit.py level`, `finish_scan` + `loop`) remain `PASS` (exit 0).
- All 565 decoded video frame hashes (`v13_frames.md5` vs `v13a_frames.md5`) and frame timestamps are identical.
- **Next Step:** `J0989` waiting condition is satisfied and `J0989` is reopened to complete step 4/4 and hand off to `J0990` (Chief technical release review of exact hash `898d26f526da708c3b400126a829c3d352855087808c658cfabbce8a5f5b19e3`). Ben's recorded approval `6411210906` covers `v13` content; `J0990` decides exact-hash technical release before `J0974` uploads.
