# J1752 — OWB 031 VO final verification, 3 November 2026

Reviewer: codex, elected acting Chief. Scope: `magnetic_field_flip_vo_v02a` only.

**Decision: FIX the missing listening review; final VO approval remains pending.** Technical verification PASS. No media fault was demonstrated and no new take or assembly is requested. This session could read and measure the Mini files but had no local audio listening input. **Nothing was heard by this reviewer.** ASR, matching hashes and the prior ruling are not represented as listening.

Authority and inputs: [Chief h32](https://github.com/TheLaughingGod1986/orbit-with-ben/issues/264#issuecomment-6536440194), J1295 result and lock commit `c8ed778ab`, current production-status.md and status.json. Chief relay confirmed codex elected for this run.

## Independent local measurements

`measurements.json` records freshly read full hashes, PCM measurements and ffmpeg ebur128 output. Source media was opened read-only in the shared Mini checkout; no WAV, MP3, parts or STT was changed.

- PASS: v02a WAV SHA256 `3444635a3efa951a1031d6681390053abd9cdd3cc1ed97d537086ee7de86b3c6`.
- PASS: v02a MP3 SHA256 `334085b5f1eb1992a0fd7f31ff46f97b24b0443158551f2cf91476a9d9c31347`.
- PASS: both full hashes match J1295; WAV also matches h32 simulated output.
- PASS: 27,277,440 frames / 568.280 s, signed 16-bit PCM, 48 kHz stereo. Each part retains its source frame count.
- PASS: ffmpeg `ebur128=peak=true`: I -19.9 LUFS, LRA 4.8 LU, true peak -3.5 dBFS (h32 limits: -20 ±1 LUFS and ≤ -1 dBTP).
- PASS: WAV null against original v02 is exactly zero outside all seven h32 fade windows. Every faded part exactly matches its segment in the full output and every intervening gap is digital zero.
- PASS: each part ends 0/0; last-10 ms stereo RMS in ch00–ch06 order: -56.1084, -71.5486, -58.2220, -71.0942, -58.0680, -59.5154, -57.0759 dBFS. All below -50.
- MP3 probe: MPEG audio, 48 kHz stereo, 128 kbps; its encoded duration includes codec padding. File identity is verified by the full hash above.

Method: Python wave + NumPy decoded s16 samples; RMS = 20 log10(sqrt(mean((samples/32768)^2))) over last 480 stereo frames. Null mask uses 48 kHz sample indices for the exact h32 windows. Loudness command: `ffmpeg -hide_banner -nostats -i <v02a.wav> -af ebur128=peak=true -f null -`. Checks did not use STT as listening evidence.

## Required follow-up (same job J1752)

Responsible reviewer: the elected Chief in a session able to actually hear local Mini audio. Resume J1752; listen to the final locked output and record precisely what was heard, especially the seven joins/endings and the complete “way?” ending. A matching checksum is not a substitute. Then record explicit VO-only PASS or a concrete audible FIX; only a complete PASS may set this VO stage done. No additional correction job is warranted without an identified media fault.

Plan retained: 1/3 complete (technical verification); step 2 is actual listening; step 3 is final ruling and stage completion. J1752 remains unfinished and available for a capable reviewer. No picture or whole-film approval. No spend, publishing or visibility changes. Sibling handoff audit remains after both dispatched voice reviews, as requested; no sibling stages changed in this run.

Disk prerequisite: nas_offload.py --apply --json found NAS mounted but no eligible scratch; 12,908 MB free before/after, no files moved.
