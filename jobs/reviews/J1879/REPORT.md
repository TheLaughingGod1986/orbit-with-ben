# J1879 — Mars-night / Titan source recovery

Codex, 3 November 2026. **Original uploaded bytes not recovered. One current Studio Download per item recovered locally; neither is approved for social use.** UPLOADS.json, all media originals, gates, dates and Buffer receipts remain unchanged. No hosting, posting, generation, render or YouTube state change.

## Provenance and bounded search

- Mars `iyvWYFP_ETA`, scheduled 9 November 11:30Z: original upload receipt `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/mon09_night_cold/11_Upload-Package/PACKAGE_UPLOAD_RESULT_2026-10-10T21-37-44-890Z.json` records SHA `48466c33946ed4367d0569a299062e5953ec9e05c7f745d1b4b7a4c9f24162e1`. J1181 and J1320 explicitly retain the canonical YouTube copy, accepting the missing original and forbidding substitution of J0432's later seam fix.
- Titan `RLSJm59OSzI`, scheduled 10 November 11:30Z: original receipt `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/11_Upload-Package/owb_sa_s6_titan/PACKAGE_UPLOAD_RESULT_2026-10-13T11-11-14-779Z.json` records SHA `afe0e80f044aca2887b9a9ef1d2aaf9fee9098285315fdc5d667eaca0019ca6c`. J0216/J0164 upload authority and records PR174 establish original lineage. J1008 retains the scheduled copy and rejects substitution of the later local render. This recovery changes none of that.
- Existing J1181/J1320/J1008 investigations were read first; their negative evidence was preserved. This pass inspected recorded package paths, NAS project mirrors, UAT handoff names and the recorded `owbshorts.tar`. No open-ended archive/stock search. Active investigation remained below 20 minutes per item. Two media candidates per item: Mars archived seam-fix and Studio download; Titan known local overwrite and Studio download. Missing-path checks and later-version folder indexes were not treated as media candidates. This is the end of the original-location search; do not reset the budget on retry without a genuinely new source and Chief scope.
- Both recorded NAS project-prefix master paths are absent (`nas-source-checks.json`). Mars local original absent as in J1870. Relevant UAT folders contain only Mars v02–v04; indexed standalone v04–v07a folders contain Neptune/ISS, not an early Titan original (`handoff-index.json`). Later rejected Titan v02 is not an original candidate.
- NAS `/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/owbshorts.tar` Mars member reads 17,989,069 bytes, SHA `0195a5fb957ce8d9e5433724792080b4fa4259c659f4ef8cb40b936702dcf7a2`: the already documented J0432 seam fix, **not** the upload SHA. No Titan v01 member in that archive (`archive-check.json`).
- Local Titan v01 reads 74,375,781 bytes, SHA `3f2f51d4f8ffd1adfc0e9c0e91c25839198860e49c3085367ea876f341d606a2`, confirming known mismatch (`local-titan-check.json`). It must not be used.

## Current-upload candidates

Studio CDP **9223** was opened on `/channel/UC_esArsDKd3GJvOkeO0DUog`, showing **Your channel / Orbit With Ben**. Each exact `/video/<id>/edit` page showed the matching title and Scheduled state. Only overflow **Download** was clicked. One transfer per item, each below the 150 MB cap; no signed download URL, cookies or credentials retained in evidence.

| Video | Local candidate | Bytes | SHA-256 |
|---|---|---:|---|
| Mars night | `/Users/benjaminoats/_desk/J1879/current-upload-candidates/Could a Robot Survive a Night on Mars_.mp4` | 3,667,108 | `70c0137661530df7397bdcfb883e5524f884f202d471d8cd73c5b613b80ddb7e` |
| Titan | `/Users/benjaminoats/_desk/J1879/current-upload-candidates/What Would Standing on Saturn's Moon Titan Feel Like_.mp4` | 1,000,998 | `68836fd5f65bfb768bab429fd2c46047136a7478d5aba87abdc7e36f5f96b575` |

Both are H.264/AAC **720×1280**; Mars video 25.500 s/audio 25.518730 s; Titan video 21.966667 s/audio 21.966077 s. Full `ffmpeg -v error -i <candidate> -f null -` decoding exited **0 with empty stderr** for both. Raw ffprobe data and actual paths/hashes are in `studio-downloads.json`. These are structural/readability checks, not audiovisual acceptance.

The current local overwritten Titan comparator is H.264/AAC 1080×1920, 30 fps, 74.4 MB (`local-titan-probe.json`); the Studio candidate is smaller and lower resolution. Original upload files are unavailable for direct encoding or pixel comparison; do not claim original byte or perceptual equivalence. Current download hashes differ from upload receipts, as expected for a transcode, but a differing hash does not itself establish acceptable quality or identity.

Playwright `save_as` created two zero-byte `<id>_studio_current_2026-11-03.mp4` placeholders while Chrome saved the actual transfer under its suggested title. Local download metadata identified the real completed files and sizes; actual files were then hashed and fully decoded. Empty placeholders are preserved and explicitly excluded. No second transfer occurred.

## Acceptance hold and next action

**No demonstrated `audio_input` or `moving_video_input` in this Codex session.** Available tools were inspected and this was recorded with `chief_relay.py capabilities`; a player, ffmpeg and stream presence do not prove perception. No listening, motion, phone-size, identity or quality PASS is claimed. No social-source exception is proposed as accepted.

A linked elected-Chief task must independently watch and hear these exact two candidates using verified capabilities, assess audiovisual identity and encoding quality against original lineage, and decide whether a narrowly recorded social-source exception is justified. Preserve J1008, J0216 test exceptions, all gates/Ben holds and existing exclusions. Rehash the actual nonempty files before review. Do not re-download, rerender, swap, approve by filename, or repeat the same source search. Any accepted exception must name these exact candidate hashes and be recorded before registry changes; hosting/post creation needs separate scope. Until that decision, Mars missing-original and Titan source-mismatch holds remain explicit.

J1879 is parked with a typed capability hold, rather than claiming completed acceptance. Nothing is required from Ben in this run.

Handoff queued as **J1889**, elected-Chief review requiring both `audio_input,moving_video_input`, due 4 November 07:00Z. Evidence PR: https://github.com/TheLaughingGod1986/orbit-with-ben/pull/427 . J1879 remains at 2/3 until independent acceptance review resolves the final step.
