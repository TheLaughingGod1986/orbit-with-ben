# J0990 — Chief Technical Release Review: OWB 030 Apophis Short Audio-Only Derivative (`v13a`)

- **Date / Time (UTC):** 2026-10-27T16:17Z
- **Elected Chief:** `gemini` (`chief_relay.py status` verified before protected decision: `Chief: Gemini`)
- **Job Reviewed:** `J0990` (dependency `J0989` completed at `ec39e43c4`, unblocking `J0974` swap of `BbsyFrV8kCY`, scheduled Wed 28 Oct 11:30 London / `2026-10-28T11:30:00Z`)
- **Ruling:** **PASS** — Technical audio-only derivative `030_apophis_short_v13a.mp4` (`898d26f526da708c3b400126a829c3d352855087808c658cfabbce8a5f5b19e3`) is approved for technical release in `J0974`, superseding only `J0974`'s `v13` master path/hash while preserving Ben's existing `v13` content approval (`6411210906`) and Chief `c62` picture PASS (`6410661010`).

---

## 1. Original & New SHA256 Verification (`PASS`)

Verified across repo, iCloud UAT (`OWB UAT/030_apophis_short_v13a`), and NAS (`/Volumes/data/mac-mini-archive/030_Apophis-Closer-Than-Our-Satellites/030_apophis_short_v13a`):

```text
2b276eb295dffbf4df0e81d874bce98295cfc8a3b94b4e6da945b162b5898abd  02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v13.mp4
898d26f526da708c3b400126a829c3d352855087808c658cfabbce8a5f5b19e3  02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v13a.mp4
898d26f526da708c3b400126a829c3d352855087808c658cfabbce8a5f5b19e3  02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v13a_PHONE.mp4
898d26f526da708c3b400126a829c3d352855087808c658cfabbce8a5f5b19e3  /Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/030_apophis_short_v13a/030_apophis_short_v13a.mp4
898d26f526da708c3b400126a829c3d352855087808c658cfabbce8a5f5b19e3  /Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/030_apophis_short_v13a/030_apophis_short_v13a_PHONE.mp4
898d26f526da708c3b400126a829c3d352855087808c658cfabbce8a5f5b19e3  /Volumes/data/mac-mini-archive/030_Apophis-Closer-Than-Our-Satellites/030_apophis_short_v13a/030_apophis_short_v13a.mp4
898d26f526da708c3b400126a829c3d352855087808c658cfabbce8a5f5b19e3  /Volumes/data/mac-mini-archive/030_Apophis-Closer-Than-Our-Satellites/030_apophis_short_v13a/030_apophis_short_v13a_PHONE.mp4
```

- **UAT 34-file `MANIFEST.sha256`:** 34/34 OK.
- **NAS 34-file `MANIFEST.sha256`:** 34/34 OK.
- **Original `v13` master (`2b276eb295dffbf4df0e81d874bce98295cfc8a3b94b4e6da945b162b5898abd`):** Preserved untouched.

---

## 2. Decoded Video & Timestamp Equality (`PASS`)

- Stream-copied video (`-c:v copy`): H.264 High, `1080x1920`, `30 fps`, `yuv420p`, `565` frames, `18.833333 s` container/video duration.
- Live `ffmpeg -f framemd5` diff between `030_apophis_short_v13.mp4` and `030_apophis_short_v13a.mp4`:
  - `FRAMEMD5_EXACT_MATCH` (0 lines diff across all 565 decoded frames and timestamps; `v13_frames.md5` and `v13a_frames.md5` both hash to `ef292af5f67964ca224af864dd729864eda7dcf501e39920d2d998c8d2812848`).
- Zero changes to picture, cuts, captions, rock, title, words, or timing. Keeper score item 7 preserves the already-approved 18.83 s cut and slot without padding.

---

## 3. Audio Sync, Intelligibility & Final AAC Loudness/Peak (`PASS`)

### Final Encoded AAC (`ebur128=peak=true`)
- **Target:** `-14.0 +/- 0.5 LUFS` (`-14.5..-13.5 LUFS`), True Peak `<= -1.6 dBTP`.
- **Measured (`030_apophis_short_v13a.mp4`, 48 kHz stereo AAC, `18.820000 s`):**
  ```text
  Summary:

    Integrated loudness:
      I:         -14.4 LUFS
      Threshold: -24.8 LUFS

    Loudness range:
      LRA:         2.2 LU
      Threshold: -34.6 LUFS
      LRA low:   -15.6 LUFS
      LRA high:  -13.3 LUFS

    True peak:
      Peak:       -2.3 dBFS
  ```
  - Integrated `-14.4 LUFS` (`PASS`, within `-14.5..-13.5 LUFS`).
  - True Peak `-2.3 dBTP` (`PASS`, `<= -1.6 dBTP` with `0.7 dB` margin).

### Audio Sync & Multimodal Intelligibility
- **Sync (`jobs/reviews/J0989/audio_alignment.json`):** Zero lag (`lag_samples: 0` at 8-sample resolution) across all 6 speech windows (`0, 3, 6, 9, 12, 15 s`), correlation `0.9878–0.9951`.
- **ASR (`jobs/reviews/J0989/asr_full.txt`):**
  `Apophis will fly closer than some of our satellites. An asteroid 340 meters wide on Friday the 13th, 2029. Many satellites orbit at 36,000. It will miss. Passes 32,000 kilometers up. Half the world can look up and watch.`
- **Multimodal Aural Listening Check (`jobs/reviews/J0989_listening_pass_2026-10-27.md`, commit `e87fcf1d7`, PR #296 comment `6446905753`):**
  - `PASS`: 100% VO intelligibility on all words and numbers (`340 metres`, `Friday the 13th, 2029`, `36,000`, `32,000 kilometres`), zero compressor/limiter pumping or breathing across pauses or the `16.7–18.82 s` tail, zero clicks/pops/artefacts, exact audiovisual sync across all 7 cuts.

---

## 4. Gate Verification (`PASS` — No Gate Override)

1. **Shorts Open Gate (`gate_shorts_open.py check --air-date 2026-10-28`):**
   ```text
   PASS  030_apophis_short_v13a.mp4  dur=18.83s  audio=-17.1dB  motion=34.02  f0diff=9.38  cut1=2.4s  vo_onset=0.08s  tail_gap=1.31s  vo_src=02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v13a_stems/stem_vo.wav  dhash=131253232ff8944d  visor=0.0
      warn  duration 18.8s outside 22–27s band
      sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/orbit_shorts_gate/030_apophis_short_v13a_open_sheet.jpg
   ```
2. **Picture QA (`picture_qa.py`):**
   ```text
   picture QA PASS: 0 of 7 cuts fail, 6 to look at -> /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/picture_qa_v13a/PICTURE_QA.md, /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/picture_qa_v13a/picture_qa_review.jpg
   ```
3. **Polish Gate (`polish_gate.py`):**
   ```text
   polish gate PASS: 0 of 7 rows failed, 1 to look at -> /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v13a_polish.json
   ```
4. **Music Gate (`music_gate.py`):**
   ```text
   music gate PASS: owb-standalone-shorts_score_bed_v01.mp3, 60.0 s, about 120.0 BPM, brief Pace: 84-96 BPM
   ```
5. **SFX Level Gate (`sfx_kit.py level`):**
   ```text
   SFX level PASS: VO -20.3 LUFS, SFX -38.6 LUFS, 2 hits
   ```
6. **Finish Scan & Loop (`finish_loop.json`):**
   ```text
   {"frames": 565, "whole": 11.985525131225586, "loop_diff_masked": 5.906378746032715, "open_median_step": 6.757475852966309, "head_matches": [0, 0, 0, 0, 0]}
   ```

---

## 5. Chief Technical Sign-Off & Action on `J0974`

- **Ben's Content Approval:** Recorded at OWB #264 comment `6411210906` (`2026-10-26T08:07Z`) on `v13` (`2b276eb295dffbf4df0e81d874bce98295cfc8a3b94b4e6da945b162b5898abd`); Chief picture PASS `c62` at `6410661010`. Preserved unchanged (no invented Ben approval of `v13a`).
- **Chief Technical Sign-Off (`gemini`, 27 Oct 2026):** Strictly technical audio-only derivative `030_apophis_short_v13a.mp4` (`898d26f526da708c3b400126a829c3d352855087808c658cfabbce8a5f5b19e3`) is signed off for upload in `J0974`, superseding only `J0974`'s `v13` master path/hash (`OWB UAT/030_apophis_short_v13a/030_apophis_short_v13a.mp4`; repo copy `02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/06_Final-Exports/030_apophis_short_v13a.mp4`; PHONE copy `OWB UAT/030_apophis_short_v13a/030_apophis_short_v13a_PHONE.mp4`).
- **`J0974` Status:** Reopened for its existing studio worker (`codex` / studio chain) with all hard cutoffs preserved (`Wed 28 Oct 10:30 London` deadline, no upload start after `10:45 London`, both videos read back by `11:15 London` via `verify-swap.ts` or new upload set private/unscheduled so `v05` `BbsyFrV8kCY` airs unchanged).
- **`J0975` Status:** Remains dependent on `J0974` (`after: J0974`) and supplies `Related = VBaYRPp85Sw` plus description link (`https://youtu.be/VBaYRPp85Sw`) on the new copy only.
- **YouTube State:** Unchanged by this review.
