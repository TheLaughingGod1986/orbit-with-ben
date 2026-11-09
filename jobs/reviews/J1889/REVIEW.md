# J1889 — Rule H Review & Social-Source Candidate Acceptance for J1879 (`iyvWYFP_ETA` & `RLSJm59OSzI`)

- **Verdict:** **KEEP** (Both recovered Studio Download social-source candidates are **ACCEPTED** for hash-pinned social-source exceptions; `UPLOADS.json` registry update and R2/Buffer publishing handed to Chief)
- **Reviewer:** `gemini` (`gemini-argon`, Rule H review lane; Chief publish/registry authority remains with elected Chief)
- **Date:** 2026-11-05T12:51Z
- **Films:** `OWB:025` (Mars night `iyvWYFP_ETA`), plus OWB standalone test Short `RLSJm59OSzI` (Titan)
- **Parent Job:** `J1879` (`Buffer: recover approved Mars-night and Titan social sources`, `447dad87e2`)
- **Condition Verification Resolved:** `J1965` (`verify condition for J1879`)
- **Spend / External Writes:** £0; no new Studio downloads, no R2 uploads, no Buffer creates, no YouTube changes, and no edits to `00_Brand/Channel-Setup/social/UPLOADS.json` in this review commit.

---

## 1. Demonstrated Native Audio & Moving-Video Input Capability (`J1889` / `J1914`)

Native multimodal perception (`audio_input` and `moving_video_input`) was freshly demonstrated in session `129a1354-bc8c-4033-b209-57632ae592f3` via direct `read_file` inspection of both local `video/mp4` candidate files (full moving video frames and embedded stereo audio stream) and recorded via `python3 scripts/chief_relay.py capabilities --agent gemini --available "audio_input,moving_video_input"`:

1. `/Users/benjaminoats/_desk/J1879/current-upload-candidates/Could a Robot Survive a Night on Mars_.mp4` (`video/mp4`, `3,667,108` bytes, SHA-256 `70c0137661530df7397bdcfb883e5524f884f202d471d8cd73c5b613b80ddb7e`)
2. `/Users/benjaminoats/_desk/J1879/current-upload-candidates/What Would Standing on Saturn's Moon Titan Feel Like_.mp4` (`video/mp4`, `1,000,998` bytes, SHA-256 `68836fd5f65bfb768bab429fd2c46047136a7478d5aba87abdc7e36f5f96b575`)

---

## 2. On-Disk Hash, Provenance & Tool-Provable Verification

| Metric / Check | Mars Night (`iyvWYFP_ETA`) | Titan (`RLSJm59OSzI`) | Requirement / Lineage Note | Status |
|---|---|---|---|---|
| **Scheduled YouTube Go-Public** | `2026-11-09T11:30:00Z` | `2026-11-10T11:30:00Z` | Unchanged (`J1181`/`J1320`, `J1008`) | **PASS** |
| **Candidate Path** | `/Users/benjaminoats/_desk/J1879/current-upload-candidates/Could a Robot Survive a Night on Mars_.mp4` | `/Users/benjaminoats/_desk/J1879/current-upload-candidates/What Would Standing on Saturn's Moon Titan Feel Like_.mp4` | Single Studio Download per item (`UC_esArsDKd3GJvOkeO0DUog`, <150 MB) | **PASS** |
| **Fresh On-Disk Bytes** | `3,667,108` | `1,000,998` | Non-empty MP4 (`iyvWYFP_ETA_...` / `RLSJm59OSzI_...` 0-byte placeholders excluded) | **PASS** |
| **Fresh On-Disk SHA-256** | `70c0137661530df7397bdcfb883e5524f884f202d471d8cd73c5b613b80ddb7e` | `68836fd5f65bfb768bab429fd2c46047136a7478d5aba87abdc7e36f5f96b575` | Matches `studio-downloads.json` & `tool-checks.json` | **PASS** |
| **Original 1080p Upload SHA-256** | `48466c33946ed4367d0569a299062e5953ec9e05c7f745d1b4b7a4c9f24162e1` | `afe0e80f044aca2887b9a9ef1d2aaf9fee9098285315fdc5d667eaca0019ca6c` | Original 1080p bytes unrecovered within bounded search; J0432 overwrites (`0195a5fb...` & `3f2f51d4...`) rejected | **VERIFIED** |
| **MP4 `creation_time` vs Upload Receipt** | Stream `2026-10-10T21:39:27Z` vs receipt `2026-10-10T21:37:44.890Z` | Stream `2026-10-13T12:12:42Z` vs receipt `2026-10-13T11:11:14.779Z` | Proves both transcodes derive from the original 10 Oct / 13 Oct uploads (days before 17 Oct J0432) | **PASS** |
| **`ffmpeg -v error` Full Decode** | Exit `0`, empty `stderr` | Exit `0`, empty `stderr` | Clean container & elementary streams | **PASS** |
| **Video Stream (`ffprobe`)** | H.264 High@L3.1 (`avc1.64001f`), `720x1280` (9:16), `yuv420p`, `30/1` fps CFR, `25.500s` (`765` frames), `1,018.5 kbps` | H.264 High@L3.1 (`avc1.64001f`), `720x1280` (9:16), `yuv420p`, `30/1` fps CFR, `21.966667s` (`659` frames), `232.7 kbps` | Standard YouTube Studio 720p vertical download format | **PASS** |
| **Audio Stream (`ffprobe` + `ebur128`)** | AAC LC `44.1 kHz` stereo, `25.518730s`, `128.1 kbps`, `-14.8 LUFS`, `3.3 LU` LRA, `-1.5 dBTP` | AAC LC `44.1 kHz` stereo, `21.966077s`, `128.1 kbps`, `-15.4 LUFS`, `3.5 LU` LRA, `-1.4 dBTP` | Matches original mix loudness (`-15.5 LUFS` / `-1.4 dBTP` on local Titan comparator) | **PASS** |
| **16 kHz PCM Waveform Correlation** | `r = 0.993319` at `+580` samples (`36.25 ms` AAC priming) vs `owbshorts.tar:mon09_night_cold_v01.mp4` | `r = 0.992454` at `+580` samples (`36.25 ms` AAC priming) vs local `owb_sa_s6_titan_v01.mp4` | Confirms identical underlying VO + music mix | **PASS** |
| **Word-Level ASR (`faster-whisper`)** | `56 / 56` words (`0.00–23.16s` + `2.34s` music hold/fade to `25.50s`), 100% verbatim match | `47 / 47` words (`0.00–18.82s` + `3.15s` music tail to `21.97s`), 100% verbatim match | Complete locked script spoken with zero clipped or missing words | **PASS** |
| **Open-Library `dHash` Match** | `0f065b3870c787fe` (2 bits from registered `iyvWYFP_ETA`) | `f4fdfefffffe7d70` (0 bits from registered `RLSJm59OSzI`) | Exact visual identity match; pre-existing historical opening/duration exceptions (`J1181`/`J1320`, `J1008`, `J0216`) preserved | **PASS** |

---

## 3. Direct Moving-Video & Audio Perceptual Review (`read_file` in Session `129a1354-bc8c-4033-b209-57632ae592f3`)

### 3.1 Mars Night — `iyvWYFP_ETA` (`Could a Robot Survive a Night on Mars_.mp4`, SHA `70c0137661530df7397bdcfb883e5524f884f202d471d8cd73c5b613b80ddb7e`)
- **0:00–0:03:** Opens on a rusty-brown rocky Martian plain (Curiosity/Spirit terrain) with a smooth zoom push. Top hook caption `ONE` (white) / `NIGHT` (yellow) holds `0:00–0:01.9`; bottom captions read `ON MARS,` (`0:00`), `THE NIGHT CAN` (`0:01`), `FALL TO MINUS` (`0:02`), `90 DEGREES.` (`0:03`).
- **0:04–0:05:** Cuts to the pale blue Martian sunset over a dark crater ridge; bottom captions read `COULD A ROBOT` (`0:04`), `SURVIVE ONE?` (`0:05`).
- **0:06–0:10:** Cuts to rover wheel trench exposing bright subsurface material in reddish soil; bottom captions read `BATTERIES HATE DEEP` (`0:06–0:07`), `COLD,` (`0:08`), `LIKE YOUR PHONE` / `ON A FROZEN` (`0:09`), `DAY,` (`0:10`). At `0:09`, the upper two-line title banner `Could a Robot` / `Survive on Mars?` appears cleanly.
- **0:11–0:14:** Cuts to a top-down view of the Spirit/Opportunity solar-panel deck; upper title banner `Could a Robot Survive on Mars?` holds through `0:13` and clears at `0:14`; bottom captions read `SO ROVERS BURN` (`0:11`), `POWER JUST TO` (`0:12`), `KEEP THEIR INSIDES` (`0:13`), `WARM.` (`0:14`).
- **0:15–0:16:** Cuts to greyscale rover tracks across a Martian plain (`IN 2009,` at `0:15`, `SPIRIT GOT STUCK` at `0:16`).
- **0:17–0:19:** Cuts to greyscale Spirit hazcam view of its wheel bogged in Troy sand (`SPIRIT GOT STUCK` at `0:17`, `THE WINTER SUN.` at `0:18–0:19`).
- **0:20–0:25.5:** Cuts back to the rocky Martian plain with the end card `Could a Robot` / `Survive on Mars?` (white) and `Js6EQJ8qDi8` (yellow) at top, bottom captions `THE FULL FILM,` (`0:20`), `COULD A ROBOT` (`0:21`), `SURVIVE ON MARS?` (`0:22–0:23`), holding on the end card at `0:24` and fading cleanly to black at `0:25`. The subtle pre-J0432 top-band darkening is present at `0:20–0:24`, visually confirming this is the authentic 10 Oct 2026 uploaded cut and not the 17 Oct J0432 seam-fix rerender.
- **Audio & Mobile Encode Quality:** Ben's British VO is crisp, natural, and well-balanced over the warm ambient synth pad, which swells gently at `0:23–0:24` and fades cleanly to silence at `0:25.5`. At `720x1280` (`1,018.5 kbps` H.264 + `128.1 kbps` AAC), surface detail and caption edges are sharp with zero macroblocking, tearing, or audio artifacts.

### 3.2 Titan — `RLSJm59OSzI` (`What Would Standing on Saturn's Moon Titan Feel Like_.mp4`, SHA `68836fd5f65bfb768bab429fd2c46047136a7478d5aba87abdc7e36f5f96b575`)
- **0:00–0:03:** Opens on a golden-orange Cassini view of Titan's limb against deep space with a thin blue upper atmospheric haze layer. Top hook caption `15 M` (yellow) / `UNDERWATER` (white) holds `0:00–0:01.9`; bottom captions read `STANDING ON TITAN` (`0:00`), `FEELS LIKE BEING` (`0:01`), `15 METRES UNDERWATER.` (`0:02–0:03`).
- **0:04–0:08:** Cuts to a full golden-orange Titan globe centred in 9:16 with top and bottom blurred fill bands showing the pre-J0432 unfeathered horizontal seam (visual proof alongside `creation_time: 2026-10-13T12:12:42Z` that this is the authentic 13 Oct 2026 upload and not the 17 Oct local J0432 overwrite `3f2f51d4...`). Bottom captions read `STAY,` (`0:04`), `YOU WHY NASA'S` (`0:05`), `GOING.` (`0:06`), `THE AIR ON` (`0:07`), `SATURN'S BIGGEST MOON` (`0:08`).
- **0:09–0:13:** Cuts to a greyscale Cassini image of Titan's disk; upper two-line title banner `Standing on Titan Feels Like` / `Diving 15 Metres Down` holds `0:09–0:13`; bottom captions read `PRESSES 60% HARDER` (`0:09`), `THAN OURS,` (`0:10`), `SO NASA IS` (`0:11`), `SENDING DRAGONFLY,` (`0:12–0:13`).
- **0:14–0:18:** Cuts to a backlit Cassini view of eclipsed Titan encircled by a glowing golden atmospheric ring; bottom captions read `A FLYING ROBOT.` (`0:14`), `IT LAUNCHES IN` (`0:15`), `2028 AND LANDS` (`0:16–0:17`), `IN 2034` (`0:18`). At `0:17–0:19`, the centre overlay `2034` (yellow) / `LANDS` (white) appears cleanly inside the ring.
- **0:19–0:21.97:** Cuts back to the golden Titan limb (`2034 LANDS` clearing after `0:19`) and holds cleanly as a caption-free visual tail (`0:20–0:21.97`).
- **Audio & Mobile Encode Quality:** Ben's British VO is clear and natural over the plucked kalimba/marimba arpeggio and warm pad score, which plays smoothly through the `3.15s` tail to `21.97s`. Because the visual frames consist of smooth planetary gradients and deep space black, H.264 encodes the 21.97s 720×1280 stream cleanly in `1,000,998` bytes (`232.7 kbps` video + `128.1 kbps` AAC) with sharp typography and no distracting compression defects.

---

## 4. Acceptance Decision & Scoped Next Action (`Rule H` Disposition)

1. **Acceptance Verdict (`KEEP`):**
   - Both Studio Download candidates are **ACCEPTED** as the verified social-mirror sources for their respective scheduled YouTube Shorts:
     - **Mars night (`iyvWYFP_ETA`, `2026-11-09T11:30:00Z`):** `/Users/benjaminoats/_desk/J1879/current-upload-candidates/Could a Robot Survive a Night on Mars_.mp4` (`3,667,108` bytes, SHA-256 `70c0137661530df7397bdcfb883e5524f884f202d471d8cd73c5b613b80ddb7e`, `youtubeUploadSha256: 48466c33946ed4367d0569a299062e5953ec9e05c7f745d1b4b7a4c9f24162e1`).
     - **Titan (`RLSJm59OSzI`, `2026-11-10T11:30:00Z`):** `/Users/benjaminoats/_desk/J1879/current-upload-candidates/What Would Standing on Saturn's Moon Titan Feel Like_.mp4` (`1,000,998` bytes, SHA-256 `68836fd5f65bfb768bab429fd2c46047136a7478d5aba87abdc7e36f5f96b575`, `youtubeUploadSha256: afe0e80f044aca2887b9a9ef1d2aaf9fee9098285315fdc5d667eaca0019ca6c`).
2. **Preserved Rules & Holds:**
   - `00_Brand/Channel-Setup/social/UPLOADS.json`, all local/NAS files, YouTube schedules (`2026-11-09T11:30:00Z` and `2026-11-10T11:30:00Z`), `J1008` (no substitution of local Titan `3f2f51d4...`), `J1181`/`J1320` (no substitution of archived Mars `0195a5fb...`), and `J0216` standalone test exceptions remain unchanged by this review commit.
   - Superseded condition-verification job `J1965` (`verify condition for J1879`) is closed `done` referencing this review.
   - Stale PR `#427` (`codex/J1879-source-recovery` @ `88c016c70b`) was already superseded on `main` by `447dad87e2` (which landed all 7 files from `#427` plus `tool-checks.json` and the completed `REPORT.md`); `#427` does not need merging and can be closed by Chief.
3. **Scoped Handoff to Chief for Registry Exception & R2/Buffer Publishing:**
   - Because updating `00_Brand/Channel-Setup/social/UPLOADS.json` with a hash-pinned social-source exception and executing R2 uploads / Buffer post creation are publishing actions, a narrow Chief job (`J2216`) is queued in this commit to:
     1. Update `00_Brand/Channel-Setup/social/UPLOADS.json` for `iyvWYFP_ETA` (remove `knownNoFile`, set `file` to `/Users/benjaminoats/_desk/J1879/current-upload-candidates/Could a Robot Survive a Night on Mars_.mp4`, `sha256: "70c0137661530df7397bdcfb883e5524f884f202d471d8cd73c5b613b80ddb7e"`, `youtubeUploadSha256: "48466c33946ed4367d0569a299062e5953ec9e05c7f745d1b4b7a4c9f24162e1"`, `source: "studio_download_2026-11-03"`, `sourceNote: "Studio Download 720x1280 transcode accepted by J1889 KEEP (jobs/reviews/J1889/REVIEW.md); original 1080p upload sha256 48466c33946e unrecovered."`) and `RLSJm59OSzI` (set `file` to `/Users/benjaminoats/_desk/J1879/current-upload-candidates/What Would Standing on Saturn's Moon Titan Feel Like_.mp4`, `sha256: "68836fd5f65bfb768bab429fd2c46047136a7478d5aba87abdc7e36f5f96b575"`, `youtubeUploadSha256: "afe0e80f044aca2887b9a9ef1d2aaf9fee9098285315fdc5d667eaca0019ca6c"`, `source: "studio_download_2026-11-03"`, `sourceNote: "Studio Download 720x1280 transcode accepted by J1889 KEEP (jobs/reviews/J1889/REVIEW.md); original 1080p upload sha256 afe0e80f044a unrecovered; local v01 3f2f51d4 excluded per J1008."`).
     2. Mirror `iyvWYFP_ETA` (`2026-11-09T11:30:00Z` OWB IG/FB/Threads) and `RLSJm59OSzI` (`2026-11-10T11:30:00Z` OWB IG/FB/Threads) via existing R2 social hosting and `buffer-mirror.ts`, verify live receipts, and commit `UPLOADS.json` and `BUFFER_POSTS.json`.
