# J2954 — Whole 108-Minute Sleep Film Phone Copy & Ben Watch Card

- **Job**: `J2954` (*Sleep video: send Ben the whole 108-minute film to watch, not a 30-second clip*)
- **Worker**: `gemini`
- **Date**: `2026-11-16`
- **Spend**: `£0` (`0` credits; YouTube Studio untouched; Private upload `13q4_EoLEN4` left scheduled for `Sat 12 Dec 2026 21:00 London`)

---

## 1. Master Verification (`sleep_video_01_master_v02.mp4`)

Verified on the NAS working-film store before encoding:

- **Path**: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01/sleep_video_01_master_v02.mp4`
- **SHA-256**: `e6f1064dc83b2c48bb05898f90139a4a250da2b316d3d3086699518379481ec0` (exact match with `j2860_v02/SHA256SUMS.txt`, `j2860_v02/VERIFICATION_J2860_FINAL.json`, and `00_Brand/Channel-Setup/social/UPLOADS.json` entry `13q4_EoLEN4`)
- **Size**: `4,216,695,410` bytes
- **Video**: `1920x1080`, H.264 `High`, `30/1` fps, `195,070` frames, `6,502.333333 s` (`108 min 22.33 s`)
- **Audio**: AAC LC, `48,000 Hz`, stereo (`2` ch), `304,798` frames, `6,502.333000 s`, packet `streamhash` `SHA256=74f9ab69f926dee582179764d158a2af07e2c2523c38624d9a5068ecd45041d2` (`-20.1 LUFS`, `LRA 2.9 LU`)

---

## 2. Full-Length 720p Phone Copy (`sleep_video_01_master_v02_PHONE.mp4`)

Built one continuous full-runtime `720p` (`+faststart`) browser/phone streaming copy — no chapter split required:

- **NAS Path**: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01/sleep_video_01_master_v02_PHONE.mp4`
- **SHA-256**: `4cf4479719ac59eb99f69c904530b03ab0bed60e8552d82e18520188fa971001` (verified both before and after NAS copy; temporary build file in `$STUDIO_SCRATCH` removed after verification)
- **Size**: `564,468,035` bytes (`538.3 MiB`, `694.5 kbps` overall)
- **Video**: `1280x720`, H.264 `High`, `yuv420p`, `30/1` fps, `195,070` frames, `6,502.333333 s` (`108 min 22.33 s`), `moov` atom at file start (`+faststart`)
- **Audio**: Exact stream copy (`-c:a copy`) from `sleep_video_01_master_v02.mp4` — AAC LC `48,000 Hz` stereo, `304,798` frames, `6,502.333000 s`, packet `streamhash` `SHA256=74f9ab69f926dee582179764d158a2af07e2c2523c38624d9a5068ecd45041d2` (bit-for-bit identical to master)
- **Decode Check**: Full `6,502.333 s` decode (`ffmpeg -v error -i ... -f null -`) exited `0` with zero errors, including the `97:20–97:50` fixed window and closing fade.

---

## 3. R2 Watch Store Upload & Playback Check

- **Watch ID**: `owb-sleep-01-v02`
- **R2 Object Key**: `watch/owb-sleep-01-v02/66705e8c1e447dc6-sleep_video_01_master_v02_PHONE.mp4` (`564,468,035` bytes)
- **Registers Updated**:
  - `05_Analytics/kanban/watch_uploads.json` (both `_PHONE.mp4` and master `.mp4` NAS paths mapped to `owb-sleep-01-v02`)
  - `~/.config/studio-kanban/watch_uploads.json` on the Mini
- **HTTP Verification**:
  - Signed `/api/watch?v=owb-sleep-01-v02` status (`follow=False`): `HTTP 302`
  - Cloudflare R2 Range probe (`Range: bytes=0-65535`): `HTTP 206 Partial Content`, `Content-Type: video/mp4`, `Content-Range: bytes 0-65535/564468035`

---

## 4. Ben Watch Card (`jobs.py awaits`) & Capability Note

- **Watch Card**: Armed on `J2954` (`type: long`, `number: SLEEP01`, `title: "Space Documentary for Sleep: A Slow Journey From the Moon to Andromeda"`, `version: sleep_video_01_master_v02`, `airs: 2026-12-12 21:00` London, `due: 2026-12-10 18:00` London, `prev: OWB-J2898, OWB-J2452`), stating in plain words that this is the whole 108-minute film and that the `97:20` fix is inside it.
- **YouTube State**: Private upload `13q4_EoLEN4` left untouched and scheduled for `Sat 12 Dec 2026 21:00 London`.
- **Capability Note**: Worker session recorded `available=""` (`no audio_input or moving_video_input media probed`); length, frame count, decode integrity, and audio packet hash were verified directly by `ffprobe`/`ffmpeg`, and Ben's UAT watch card supplies the human watch-and-listen check.
