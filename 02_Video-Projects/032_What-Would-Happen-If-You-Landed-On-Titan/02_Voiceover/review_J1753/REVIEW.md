# J1753 — OWB 032 VO verification, 3 November 2026

Reviewer: codex, elected acting Chief. Scope: `titan_landing_vo_v02b` only.

**Decision: FIX the missing listening review; final VO approval remains pending.** Technical checks against h31 PASS. No media correction is demonstrated or ordered. This session can read Mini media but has no audio listening input. **Nothing was heard by this reviewer.** Hashes, ASR and earlier reviewers' conclusions are not listening evidence.

Inputs: [Chief h31](https://github.com/TheLaughingGod1986/orbit-with-ben/issues/264#issuecomment-6536311192), J1294 result, lock commit `4a9a2e16b`, production-status.md and status.json. Chief relay confirmed codex elected.

## Independent actual-file verification

- WAV SHA256: `55232eebb76b68639eee0681316a9e90443e36bf42892ba99c9a98735301abc5`.
- MP3 SHA256: `944378a9c7caec4368217a481d35160cfb5621ed4de7dbe4a7787d813a6abff8`.
- Both match J1294; WAV matches the h31 simulation.
- WAV: 27,957,120 frames, 582.440 s, 48 kHz stereo s16 PCM.
- ffmpeg ebur128: I -20.0 LUFS, LRA 4.8 LU, true peak -3.4 dBFS. Within h31 limits (-20 ±1 LUFS; TP ≤ -1).
- ch00 last 10 ms: -51.7647 dBFS, final samples 0/0. ch02: -62.5252 dBFS, final samples 0/0. Both meet the specified below -50 requirement.
- Null versus v02: exactly zero outside 50.300–50.480 s and 245.140–245.160 s. All seven parts match their master segments, retain source frame counts, and the six intervening gaps are digital zero.
- Copied `words.srt` and `stt_raw.json` are byte-identical to v02. The extra COPIED_FROM_v02.txt is provenance, not a timing mismatch.
- Original v02 and failed-spec v02a WAV hashes still match J1294's recorded originals. No media, old take or source timing was modified.

`measurements.json` contains full hashes, PCM measurements, all part tails, MP3 probe and ebur128 summary. Method: Python wave and NumPy s16 samples, RMS over final 480 stereo frames using full scale 32768; sample-index null mask at 48 kHz; `ffmpeg -hide_banner -nostats -i <locked.wav> -af ebur128=peak=true -f null -`.

The h31 tail thresholds apply to ch00 and ch02, not all untouched parts. The additional measurements show ch04's final 10 ms at -34.33 dBFS and final samples 1729/1729, unchanged from v02. The next listener should specifically hear that join at 396.8 s as well as ch00 at 50.48 s, ch02 at 245.16 s, every other join and the ending. Measurement alone is not an audible defect ruling.

## Required follow-up — resume J1753

Responsible reviewer: the elected Chief in a session that can actually hear local Mini audio. Listen to the locked final take, record what was heard (including the complete “own?” ending and joins), then issue VO-only PASS or a concrete audible FIX. Only a complete PASS may set VO done. No new take or correction job is justified by these technical results.

Plan: 1/3 complete (technical verification); step 2 actual listening; step 3 final ruling and stage completion. The existing J1753 is the follow-up, avoiding a duplicate. No picture or whole-film approval; sources remain blocked. Sibling audit remains due after both J1752 and J1753 are completed, as the brief requests; neither listening review is complete yet.

Disk prerequisite: nas_offload.py --apply found no eligible old scratch; 12,368 MB free before/after, no files moved. No spend, uploads, schedules or visibility changes.
