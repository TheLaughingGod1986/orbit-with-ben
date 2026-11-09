# J1879 — Mars-night / Titan source recovery and candidate verification

Codex (3 November 2026, bounded search + Studio candidate download) and Gemini (`gemini-argon`, 4 November 2026, complete tool-provable checks + native multimodal video/audio inspection under `AGENTS.md` PR480). **Original uploaded 1080×1920 bytes not recovered. One current Studio Download per item recovered locally and independently verified as the exact YouTube 720×1280 H.264/AAC transcode of the canonical 10 Oct / 13 Oct uploaded cuts; both remain unapproved until elected-Chief decision `J1889`.** `UPLOADS.json`, all media originals, gates, dates and Buffer receipts remain unchanged. No hosting, posting, generation, render or YouTube state change.

## Provenance and bounded search

- Mars `iyvWYFP_ETA`, scheduled 9 November 11:30Z: original upload receipt `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/10_Shorts/mon09_night_cold/11_Upload-Package/PACKAGE_UPLOAD_RESULT_2026-10-10T21-37-44-890Z.json` records SHA `48466c33946ed4367d0569a299062e5953ec9e05c7f745d1b4b7a4c9f24162e1`. J1181 and J1320 explicitly retain the canonical YouTube copy, accepting the missing original and forbidding substitution of J0432's later seam fix.
- Titan `RLSJm59OSzI`, scheduled 10 November 11:30Z: original receipt `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/11_Upload-Package/owb_sa_s6_titan/PACKAGE_UPLOAD_RESULT_2026-10-13T11-11-14-779Z.json` records SHA `afe0e80f044aca2887b9a9ef1d2aaf9fee9098285315fdc5d667eaca0019ca6c`. J0216/J0164 upload authority and records PR174 establish original lineage. J1008 retains the scheduled copy and rejects substitution of the later local render. This recovery changes none of that.
- Existing J1181/J1320/J1008 investigations were read first; their negative evidence was preserved. This pass inspected recorded package paths, NAS project mirrors, UAT handoff names and the recorded `owbshorts.tar`. No open-ended archive/stock search. Active investigation remained below 20 minutes per item. Two media candidates per item: Mars archived seam-fix and Studio download; Titan known local overwrite and Studio download. Missing-path checks and later-version folder indexes were not treated as media candidates. This is the end of the original-location search; do not reset the budget on retry without a genuinely new source and Chief scope.
- Both recorded NAS project-prefix master paths are absent (`nas-source-checks.json`). Mars local original absent as in J1870. Relevant UAT folders contain only Mars v02–v04; indexed standalone v04–v07a folders contain Neptune/ISS, not an early Titan original (`handoff-index.json`). Later rejected Titan v02 is not an original candidate.
- NAS `/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/owbshorts.tar` Mars member reads 17,989,069 bytes, SHA `0195a5fb957ce8d9e5433724792080b4fa4259c659f4ef8cb40b936702dcf7a2`: the already documented J0432 seam fix, **not** the upload SHA. No Titan v01 member in that archive (`archive-check.json`).
- Local Titan v01 reads 74,375,781 bytes, SHA `3f2f51d4f8ffd1adfc0e9c0e91c25839198860e49c3085367ea876f341d606a2`, confirming known mismatch (`local-titan-check.json`). It must not be used.

## Current-upload Studio candidates and encoding differences

Studio CDP **9223** was opened on `/channel/UC_esArsDKd3GJvOkeO0DUog`, showing **Your channel / Orbit With Ben**. Each exact `/video/<id>/edit` page showed the matching title and Scheduled state. Only overflow **Download** was clicked. One transfer per item, each below the 150 MB cap; no signed download URL, cookies or credentials retained in evidence.

| Video | Local candidate | Bytes | SHA-256 | Stream creation_time (UTC) |
|---|---|---:|---|---|
| Mars night (`iyvWYFP_ETA`) | `/Users/benjaminoats/_desk/J1879/current-upload-candidates/Could a Robot Survive a Night on Mars_.mp4` | 3,667,108 | `70c0137661530df7397bdcfb883e5524f884f202d471d8cd73c5b613b80ddb7e` | `2026-10-10T21:38:08.000000Z` |
| Titan (`RLSJm59OSzI`) | `/Users/benjaminoats/_desk/J1879/current-upload-candidates/What Would Standing on Saturn's Moon Titan Feel Like_.mp4` | 1,000,998 | `68836fd5f65bfb768bab429fd2c46047136a7478d5aba87abdc7e36f5f96b575` | `2026-10-13T12:12:42.000000Z` |

### Encoding comparison vs original lineage / local comparators

1. **Container & stream provenance (`studio-downloads.json`, `tool-checks.json`):**
   - Both Studio downloads are YouTube's standard MP4 (`isommp42`, `encoder: Google`) Studio Download transcodes: **H.264 High@L3.1 (`avc1.64001f`), 720×1280 (9:16), yuv420p, bt709, 30 fps CFR**, with **AAC LC stereo 44.1 kHz (~128 kbps)** audio.
   - By contrast, the local 1080×1920 CFR masters (e.g. overwritten local Titan `v01` in `local-titan-probe.json`: 1080×1920, 74,375,781 bytes, ~27.1 Mbps H.264 + 48 kHz AAC; archived J0432 Mars `v01`: 1080×1920, 17,989,069 bytes) are high-bitrate 1080p mezzanine exports.
   - **Timestamp proof of pre-J0432 upload lineage:** Both Studio downloads carry embedded Google MP4 stream `creation_time` tags matching their original upload receipts (Mars `2026-10-10T21:38:08Z` vs upload receipt `2026-10-10T21:37:44.890Z`; Titan `2026-10-13T12:12:42Z` vs upload receipt `2026-10-13T11:11:14.779Z`), days before J0432 ran on `2026-10-17T04:01Z`.
2. **Decode, loudness, waveform correlation, ASR & frame-0 identity (`tool-checks.json`):**
   - **Full `ffmpeg` decode:** `ffmpeg -v error -i <candidate> -f null -` exited **0 with empty stderr** for both.
   - **Loudness (`ebur128` + `volumedetect`):**
     - Mars `iyvWYFP_ETA`: `-14.8 LUFS` integrated, `3.3 LU` LRA, `-1.5 dBTP` true peak, `-17.4 dB` mean volume (`25.500 s` video / `25.518730 s` audio, `765` frames).
     - Titan `RLSJm59OSzI`: `-15.4 LUFS` integrated, `3.5 LU` LRA, `-1.4 dBTP` true peak, `-18.1 dB` mean volume (`21.966667 s` video / `21.966077 s` audio, `659` frames; local `v01` comparator is `-15.5 LUFS`, `3.7 LU` LRA, `-1.4 dBTP` true peak, `-18.0 dB` mean).
   - **Lag-aligned 16 kHz PCM audio correlation:**
     - Mars Studio candidate vs `owbshorts.tar:mon09_night_cold_v01.mp4`: **Pearson `r = 0.993319`** at `+580` samples (`36.25 ms`, standard 44.1 kHz AAC priming delay).
     - Titan Studio candidate vs local `owb_sa_s6_titan_v01.mp4`: **Pearson `r = 0.992454`** at `+580` samples (`36.25 ms`).
   - **Word-level ASR (`faster-whisper` via `.venv_vo_check_py312`):**
     - Mars `iyvWYFP_ETA` (56 words, `0.00 s`–`23.16 s`, followed by `2.34 s` music hold/fade to `25.50 s`): *"On Mars, the night can fall to minus 90 degrees. Could a robot survive one? Batteries hate deep cold, like your phone on a frozen day. So rovers burn power just to keep their insides warm. In 2009, Spirit got stuck and couldn't catch the winter sun. The full film could a robot survive on Mars?"* — 100% word-for-word match.
     - Titan `RLSJm59OSzI` (47 words, `0.00 s`–`18.82 s`, followed by `3.15 s` music tail to `21.97 s`): *"Standing on Titan feels like being 15 metres underwater. Stay, and I'll show you why NASA's going. The air on Saturn's biggest moon presses 60% harder than ours, so NASA is sending Dragonfly a flying robot. It launches in 2028 and lands in 2034."* — 100% word-for-word match.
   - **Open-plate `dHash` identity (`gate_shorts_open.py`):**
     - Mars `iyvWYFP_ETA`: `dhash=0f065b3870c787fe`, matching its own registered open-library entry `iyvWYFP_ETA` within **2 bits**.
     - Titan `RLSJm59OSzI`: `dhash=f4fdfefffffe7d70`, matching its own registered open-library entry `RLSJm59OSzI` at **0 bits**.
     - As documented in `J1181`/`J1320` and `J1008`, the 10 Oct and 13 Oct uploaded cuts pre-date later opening-motion/question-first rules (`f0diff=0.14` and `0.07`, `cut1=4.1s` and `4.3s`, plus `J0216` ~20 s standalone test exception on Titan) and were explicitly locked by Chief to air as scheduled without recut or gate waiver.

## Independent multimodal audiovisual review (`gemini-argon`)

Capabilities `audio_input,moving_video_input` were verified and recorded via `chief_relay.py capabilities` using native multimodal `read_file` inspection of both MP4 files and their opening contact sheets:

1. **Mars night (`iyvWYFP_ETA`, `Could a Robot Survive a Night on Mars_.mp4`, SHA `70c0137661530df7397bdcfb883e5524f884f202d471d8cd73c5b613b80ddb7e`):**
   - **0:00–0:03:** Rocky Martian plain (Curiosity/Spirit terrain) with slow zoom push; upper hook caption `ONE` (white) / `NIGHT` (yellow) holds 0:00–0:02; lower captions `ON MARS,` / `THE NIGHT CAN` / `FALL TO MINUS` / `90 DEGREES.`
   - **0:04–0:05:** Blue Martian sunset over crater rim (`COULD A ROBOT` / `SURVIVE ONE?`).
   - **0:06–0:10:** Rover trench exposing bright subsurface material (`BATTERIES HATE DEEP` / `COLD,` / `LIKE YOUR PHONE` / `ON A FROZEN` / `DAY,`); upper title card `Could a Robot Survive on Mars?` appears cleanly at 0:09–0:13.
   - **0:11–0:14:** Top-down Spirit/Opportunity solar deck (`SO ROVERS BURN` / `POWER JUST TO` / `KEEP THEIR INSIDES` / `WARM.`).
   - **0:15–0:16:** Greyscale rover tracks across Martian plain (`IN 2009,` / `SPIRIT GOT STUCK`).
   - **0:17–0:19:** Spirit hazcam view of wheel bogged in Troy sand (`AND COULDN'T CATCH` / `THE WINTER SUN.`).
   - **0:20–0:25.5:** End card over rocky Martian plain showing `Could a Robot Survive on Mars?` (white) / `Js6EQJ8qDi8` (yellow) with the subtle pre-J0432 top-band darkening (`0.087` gutter step before J0432 feathered it), confirming this is the exact 10 Oct uploaded cut. British VO and ambient synth pad are clean and intelligible throughout, fading smoothly at 0:25.5. At 720×1280 (~1.01 Mbps video), rock textures and typography remain crisp for mobile social feeds.
2. **Titan (`RLSJm59OSzI`, `What Would Standing on Saturn's Moon Titan Feel Like_.mp4`, SHA `68836fd5f65bfb768bab429fd2c46047136a7478d5aba87abdc7e36f5f96b575`):**
   - **0:00–0:03:** Golden-orange Titan limb with blue upper atmospheric haze; upper hook caption `15 M` (yellow) / `UNDERWATER` (white) holds 0:00–0:02; lower captions `STANDING ON TITAN` / `FEELS LIKE BEING` / `15 METRES UNDERWATER.`
   - **0:04–0:08:** Full golden Titan globe centred with top/bottom blurred fill bands (showing the pre-J0432 unfeathered horizontal fill boundary that proves this is the original 13 Oct upload, not the 17 Oct J0432 local overwrite `3f2f51d4...`); lower captions `STAY,` / `AND I'LL SHOW` / `YOU WHY NASA'S` / `GOING.` / `THE AIR ON` / `SATURN'S BIGGEST MOON`.
   - **0:09–0:13:** Greyscale Cassini Titan disk; upper title card `Standing on Titan Feels Like` / `Diving 15 Metres Down`; lower captions `PRESSES 60% HARDER` / `THAN OURS,` / `SO NASA IS` / `SENDING DRAGONFLY,`.
   - **0:14–0:18:** Backlit golden atmospheric ring around eclipsed Titan (`A FLYING ROBOT.` / `IT LAUNCHES IN` / `2028 AND LANDS` / `IN 2034`), with centre overlay `2034` (yellow) / `LANDS` (white) at 0:17–0:19.
   - **0:19–0:21.97:** Return to golden Titan limb tail while the rhythmic pluck/pad score completes cleanly. Despite the compact 1.0 MB file size (~233 kbps video due to smooth planetary gradients and black space), typography is sharp and audio (`128 kbps` AAC) is clean.

## Specific social-source exception proposal and handoff to `J1889`

- **Proposal to elected Chief (`J1889`):** Authorize a narrow, hash-pinned social-source exception for `iyvWYFP_ETA` (9 Nov 11:30Z) and `RLSJm59OSzI` (10 Nov 11:30Z) to mirror from these exact verified Studio Download candidates:
  - `iyvWYFP_ETA`: `/Users/benjaminoats/_desk/J1879/current-upload-candidates/Could a Robot Survive a Night on Mars_.mp4` (`3,667,108` bytes, SHA-256 `70c0137661530df7397bdcfb883e5524f884f202d471d8cd73c5b613b80ddb7e`)
  - `RLSJm59OSzI`: `/Users/benjaminoats/_desk/J1879/current-upload-candidates/What Would Standing on Saturn's Moon Titan Feel Like_.mp4` (`1,000,998` bytes, SHA-256 `68836fd5f65bfb768bab429fd2c46047136a7478d5aba87abdc7e36f5f96b575`)
- **Explicit holds retained:** `00_Brand/Channel-Setup/social/UPLOADS.json`, all local/NAS files, YouTube schedules (`9 Nov 11:30Z` and `10 Nov 11:30Z`), `J1008`, `J1181`, `J1320`, `J0216` test exceptions, and Buffer queues remain unchanged by `J1879`. Linked Chief decision job `J1889` is already queued to rule on this evidence and scope any registry update / R2 hosting / Buffer post creation.
