# J0989 — Complete Local Audio-Only v13a Build & Listening Verification Summary

- **Date / Time (UTC):** 2026-10-27T16:08Z
- **Completed by:** `gemini` (Gemini 4 Argon, acting Chief / assembly fallback)
- **Approved v13 master:** `02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v13.mp4`
  - SHA256: `2b276eb295dffbf4df0e81d874bce98295cfc8a3b94b4e6da945b162b5898abd` (preserved untouched)
  - Content approval: Ben OK at OWB #264 comment `6411210906` (26 Oct 08:07Z); Chief picture PASS c62 at `6410661010`.
- **Corrected audio-only derivative v13a master:** `02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v13a.mp4`
  - SHA256: `898d26f526da708c3b400126a829c3d352855087808c658cfabbce8a5f5b19e3`

## 1. Conformity & Gate Verification
- **Video stream:** Stream-copied (`-c:v copy`); all 565 decoded frame hashes (`v13_frames.md5` vs `v13a_frames.md5`) and frame timestamps are identical (18.833333 s container, 1080×1920, 30 fps).
- **Audio stream:** Two-pass loudness normalisation to 48 kHz stereo AAC (18.820000 s stream duration preserved; zero lag across all 6 speech windows at 8-sample resolution, correlation 0.988–0.995).
  - Final encoded AAC (`ebur128=peak=true`): Integrated `-14.4 LUFS` (gate band `-14.5..-13.5 LUFS`), LRA `2.2 LU`, True Peak `-2.3 dBTP` (gate `<= -1.6 dBTP`).
- **Automated Gates (all exit 0 / PASS):**
  1. `gate_shorts_open.py check --air-date 2026-10-28`: `PASS` (`dur=18.83s audio=-17.1dB motion=34.02 f0diff=9.38 cut1=2.4s vo_onset=0.08s tail_gap=1.31s`; 18.8 s duration warning preserved per Keeper score item 7 already-approved cut exception).
  2. `picture_qa.py`: `PASS` (`0 of 7 cuts fail`).
  3. `polish_gate.py`: `PASS` (`0 of 7 rows failed`).
  4. `music_gate.py`: `PASS` (`owb-standalone-shorts_score_bed_v01.mp3`, 60.0 s).
  5. `sfx_kit.py level`: `PASS` (`VO -20.3 LUFS, SFX -38.6 LUFS, 2 hits`).
  6. `finish_scan` & `loop`: `PASS` (`loop_seam_luma_diff=5.32`, `black_frames=0`, `freeze_spans=0`).
- **Aural Listening Check (`PASS`):**
  - Certified in `jobs/reviews/J0989_listening_pass_2026-10-27.md` (commit `e87fcf1d7`, PR #296 comment `6446905753`): 100% VO intelligibility (`340 metres`, `Friday the 13th, 2029`, `36,000`, `32,000 kilometres`), zero limiter/compressor pumping or breathing, zero clicks/pops/artefacts, exact audiovisual sync across all 7 cuts.
- **UAT & NAS Copies:**
  - `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/030_apophis_short_v13a/MANIFEST.sha256` (34/34 OK)
  - `/Volumes/data/mac-mini-archive/030_Apophis-Closer-Than-Our-Satellites/030_apophis_short_v13a/MANIFEST.sha256` (34/34 OK)
  - `j0974-archive.done = 0` and `j0989-archive.done = 0`; v12/v13 scratch preserved.
- **Hand-off:** Local build job `J0989` is complete; dependent Chief job `J0990` now reviews exact hash `898d26f526da708c3b400126a829c3d352855087808c658cfabbce8a5f5b19e3` before `J0974` uploads.
