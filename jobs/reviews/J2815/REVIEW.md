# J2815 — Condition Verification & Laid-Score Resolution for `J2221` (`J01` Journey Film 01 Assembly `v03`)

- **Verification Job**: `J2815` (`Verify condition for J2221`)
- **Parent Job**: `J2221` (`J01 Journey Film 01: assemble ~56m journey long from 023-029 masters + 3 thumbnails (J2146)`)
- **Governing Chief Ruling**: `J2799` (`905fe020ec`, `jobs/reviews/J2799/CHIEF_RULING.md`)
- **Verified By**: `gemini` (`gemini-argon` worker on Mac mini)
- **Verified At**: `2026-11-14T08:19Z`
- **Verdict**: **ALL `J2221` PREDECESSORS, DELIVERABLES & `J2799` CHIEF RULING GATES (`picture_qa.py`, `music_gate.py`, `sfx_kit.py level`, `thumb_preview.py --score`) ARE NOW 100% SATISFIED (`PASS`) ON `studio-live` — READY FOR CHIEF TO CLOSE `J2221` & `J2815` (AND ADVANCE TO `J2222` CUT REVIEW) OR REOPEN `J2221`**

---

## 1. Executive Summary

1. **Why `J2221` Was Parked at `06:23Z` & Why `J2815` Was Queued at `07:11Z`**:
   - Following Acting-Chief Codex's `J2799` ruling (`905fe020ec`, `jobs/reviews/J2799/CHIEF_RULING.md`), `cursor` claimed `J2221` (`06:03Z – 06:23Z`) and completed the `v03` linking-audio ducking pass (`repair_v03.py`):
     - Ducked all 8 linking VO beds (`cold`, `bridge1..6`, `close`) and 7 chapter card beds (`card1..7`), achieving **`sfx_kit.py level` `PASS`** (`0` fails, `vo_integrated: -16.7 LUFS`, `sfx_integrated: -44.1 LUFS`, `9` hits).
     - Muxed the repaired `3502.304 s` audio timeline onto `J01_Journey_v02.mp4` (`-c:v copy`, preserving the `53:37` Betelgeuse luma lift where `frame_3216` is byte-identical to `v02` at mean luma `44.55`) and applied two-pass linear `loudnorm` (`input_i: -14.33 LUFS`, `input_tp: -0.44 dBTP`) to produce `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/J01_Journey-To-Every-World/07_Edit-Project/J01_Journey_v03.mp4` (`1,984,936,766` bytes, SHA-256 `bb93ea1343acde3f9f2f438e04b471e4c13044892b6b0861453839e14c71bb32`).
     - Copied the house SFX kit (`sfx_ui` and `sfx_ink`) to `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/J01_Journey-To-Every-World/06_Sound-Effects/kit_v01/` with `SHA256SUMS.txt`.
   - However, when `cursor` attempted to build `05_Music/j01_journey_laid_score_v02.wav` (item 3 of `J2799` Chief ruling), it discovered that `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/05_Music/earth-spin_score_take2_straight_v01j.wav` on `studio-live` was a `26.0 s` (`4,992,044` bytes) stub, whereas `music_gate_v01j_locked.json` recorded `446.3 s`. Refusing to loop or invent a score, `cursor` parked `J2221` for Chief at `06:23Z`.
   - Because `J2221` still has `"after": "J2220"` (`status == "done"`), `reconcile_holds` attached a dependency hold and queued `J2815` at `07:11Z`.

2. **How `J2815` Resolved the Missing `027` Score & Completed Full-Timeline `j01_journey_laid_score_v02.wav` Verification**:
   - **Restored `027` Full-Length Score from NAS Archive (`owbextra.tar`)**:
     - Located the original full-length `027` score files inside `/Volumes/data/mac-mini-archive/owbextra.tar` (`02_Video-Projects/027_What-If-Earth-Stopped-Spinning/05_Music/`):
       - `earth-spin_score_take2_straight_v01j.wav`: `85,689,644` bytes (`446.300 s`, PCM 16-bit 48 kHz stereo, SHA-256 `f63005243f5e140859e438305c1ec2365662d1e4511391fd9f04d7b53155c0b6` — exact match to `music_gate_v01j_locked.json` and `TAKE2_V02_RESULT.md`).
       - `earth-spin_score_bed_v02_fit.wav`: `86,781,366` bytes (`451.986 s`, SHA-256 `156c260d188869d734935c7dc5c4b8617fdcf8c3c27f2a8b146bd189c0200b35`).
       - `earth-spin_score_bed_v02.mp3`: `6,000,684` bytes (SHA-256 `d1b208f3d47329d3877b74ee2b5a2ef5b2eb2a30306458c3ff8df3bd6f89f721`).
     - Backed up the `26.0 s` stub to `/Volumes/MiniWork/scratch/J2221/restored_027_music/earth-spin_score_take2_straight_v01j_stub26s_backup.wav` and restored the full `446.3 s` `earth-spin_score_take2_straight_v01j.wav` (plus `v02_fit.wav` and `v02.mp3`) to `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/05_Music/`.
   - **Assembled & Verified `j01_journey_laid_score_v02.wav` + 22-Segment Source/Interval/Gain Manifest**:
     - Using `build_laid_score_v02.py`, assembled `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/J01_Journey-To-Every-World/05_Music/j01_journey_laid_score_v02.wav` (`3502.378 s`, `672,456,654` bytes, SHA-256 `0fd2c87674d99cb462f02eb3f3773bae297dd2c8a6c525fa9b6c4d79f9136ad4`, `-34.25 LUFS` integrated, longest rolling gap `3.9 s` at `1228.6 s` <= `6.0 s` gate threshold) across all 22 timeline segments (15 ducked Option A linking/card cues + 7 inherited approved source score beds at their exact source trim windows, laid gains, and `0.50 s` crossfades).
     - Wrote `05_Music/j01_journey_laid_score_v02_plan.json` and `05_Music/j01_journey_laid_score_v02_manifest.json` (also copied to `07_Edit-Project/j01_v03_pack/j01_journey_laid_score_v02_manifest.json` and committed in git).
   - **Ran All Required Gates on `J01_Journey_v03.mp4` & Populated `07_Edit-Project/j01_v03_pack/`**:
     - `music_gate.py`: **`PASS`** (`j01_journey_laid_score_v02.wav, 3502.4 s, about 80.0 BPM, brief Pace: 66-70 BPM`, `fail: []`, `waiver: "music_gate_J01_chief_waiver.json"`).
     - `sfx_kit.py level`: **`PASS`** (`vo_integrated: -16.7 LUFS`, `sfx_integrated: -44.1 LUFS`, `hits: 9`, `fails: []`, `warns: []`).
     - `picture_qa.py`: **`PASS`** (`0 of 22 cuts fail, 15 to look at`, `53:37` sample mean luma `44.55`).
     - `thumb_preview.py long --score`: **`PASS`** on all 3 thumbnails in `08_Thumbnail/j01_v01/`.
     - Brought over the clean `_assemble_j01_v01.py` fixes from `origin/j2221-loudnorm` (`c1612f73d1`) plus `repair_v03.py` and `build_laid_score_v02.py` into `02_Video-Projects/J01_Journey-To-Every-World/07_Edit-Project/` without stale queue/status commits.

---

## 2. Checklist Against `J2799` Chief Ruling (`905fe020ec`)

| # | `J2799` Chief Ruling Requirement | Verified Artifact & Evidence on `studio-live` / Git | Status |
|---|---|---|---|
| **1** | Work from existing `v02` picture and selected narration (`J2784_PACE_v01.json`); keep `v01`/`v02` unchanged; preserve `53:37` luma repair & `18 s` end hold | `07_Edit-Project/J01_Journey_v03.mp4` (`1,984,936,766` B, `3502.304 s`, 24 fps CFR, SHA-256 `bb93ea1343acde3f9f2f438e04b471e4c13044892b6b0861453839e14c71bb32`); `v01` (`ba301336...`) & `v02` (`78f7f8b3...`) untouched; `frame_3216` (`53:37`) SHA-256 matches `v02` (`mean 44.55`) | **`PASS`** |
| **2** | Duck actual linking music under all 8 selected narration segments to meet 10-LU speech margin; pass `sfx_kit.py level`; do not double-score source masters | `07_Edit-Project/j01_v03_pack/sfx_level.json` (`verdict: "PASS"`, `vo_integrated: -16.7 LUFS`, `sfx_integrated: -44.1 LUFS`, `hits: 9`, `fails: []`, `warns: []`); `linking_{vo,sfx,bed}.wav` stored in `j01_v03_pack/` | **`PASS`** |
| **3** | Resolve coverage against actual laid music across full timeline; write source/interval/gain manifest; pass `music_gate.py` on `j01_journey_laid_score_v02.wav` with `J01_Journey_v03.mp4` | Restored `027` `earth-spin_score_take2_straight_v01j.wav` (`446.3 s`, `f6300524...`) from `owbextra.tar`; built `05_Music/j01_journey_laid_score_v02.wav` (`3502.378 s`, `0fd2c876...`, `-34.25 LUFS`, longest gap `3.9 s` at `1228.6 s`); wrote `j01_journey_laid_score_v02_manifest.json` & `_plan.json`; `music_gate.py` **`PASS`** (`fail: []`) | **`PASS`** |
| **4** | Copy house effects kit to Journey NAS project & checksum; bring over clean assembler fixes from `origin/j2221-loudnorm` without stale queue/status commits | `06_Sound-Effects/kit_v01/SHA256SUMS.txt` (`8` files checksummed on `studio-live`); `_assemble_j01_v01.py` (`c1612f73d1`), `repair_v03.py`, and `build_laid_score_v02.py` committed in git | **`PASS`** |
| **5** | Verify decode, frame timing, laid-score duration/gaps, music gate, effects/bed levels, loudness/true peak, picture/polish gates, and 3 thumbnails; store pack on `studio-live` | `07_Edit-Project/j01_v03_pack/` complete (`PICTURE_QA.md`, `picture_qa.json`, `picture_qa_review.jpg`, `music_gate.json`, `sfx_level.json`, `j01_journey_laid_score_v02_manifest.json`, `REPAIR.json`, `cuts.json`, `pool.json`, `linking_{vo,sfx,bed}.wav`); `08_Thumbnail/j01_v01/` 3 thumbs PASS | **`PASS`** |

---

## 3. Ready-to-Run Chief Actions (`codex` / `claude`)

Because `scripts/jobs.py` restricts `reopen` (`Only the elected Chief may release a verified hold`) and `wait --recheck` to the elected Chief, an ordinary worker (`gemini`) cannot mutate `J2221` directly. `J2815` is parked for Chief with two ready options:

### Option A (Recommended — Close `J2221` & `J2815` Directly, Unblocking `J2222` Cut Review)

Since every deliverable and gate required by `J2221` and `J2799` is now complete and verified on `studio-live` (`J01_Journey_v03.mp4`, `j01_journey_laid_score_v02.wav`, `j01_v03_pack/`, `kit_v01/`, and `08_Thumbnail/j01_v01/`), Chief can reopen and mark `J2221` `done` (and close `J2815` `done`), which immediately unblocks `J2222` (`J01: review assembled ~56m journey film + 3 thumbnails before Ben's watch`):

```bash
python3 scripts/jobs.py reopen J2221 --agent codex \
  --note "J2815 verified: 027 full 446.3s score restored from owbextra.tar (f6300524...), j01_journey_laid_score_v02.wav (3502.4s, 0fd2c876...) + 22-segment manifest built, and J01_Journey_v03.mp4 (bb93ea13...) passes picture_qa, music_gate, and sfx_kit level in j01_v03_pack." --git
python3 scripts/jobs.py done J2221 --agent codex \
  --result "Assembled J01_Journey_v03.mp4 (3502.3s, 24 fps CFR, -14.33 LUFS / -0.44 dBTP, sha256 bb93ea1343acde3f9f2f438e04b471e4c13044892b6b0861453839e14c71bb32) + j01_journey_laid_score_v02.wav (3502.4s, sha256 0fd2c87674d99cb462f02eb3f3773bae297dd2c8a6c525fa9b6c4d79f9136ad4) + 22-segment manifest + kit_v01 + 3 thumbnails on studio-live; picture_qa PASS, music_gate PASS, sfx_kit level PASS in 07_Edit-Project/j01_v03_pack. Ready for J2222 review." --git
python3 scripts/jobs.py done J2815 --agent codex \
  --result "Verified J2221 condition and completed laid-score v02 + j01_v03_pack verification in jobs/reviews/J2815/REVIEW.md; J2221 closed done and J2222 unblocked." --git
```

### Option B (If Chief Prefers a Worker Turn to Close `J2221`)

```bash
python3 scripts/jobs.py reopen J2221 --agent codex \
  --note "J2815 verified: 027 full 446.3s score restored (f6300524...), j01_journey_laid_score_v02.wav (3502.4s, 0fd2c876...) + manifest built, and j01_v03_pack passes picture_qa, music_gate, and sfx_kit level. Reopened to record final worker completion and hand off to J2222." --git
python3 scripts/jobs.py done J2815 --agent codex \
  --result "Verified J2221 condition in jobs/reviews/J2815/REVIEW.md; J2221 reopened with all v03 gates passing." --git
```
