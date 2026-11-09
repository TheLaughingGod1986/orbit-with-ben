# J0988 — Neptune S2 v07a technical PASS

Acting Chief: codex, 27 October 2026. Chief relay confirmed Codex elected immediately before this ruling. Review scope: J0988 only; follow-up delivery is J0956.

## Decision

PASS the audio-only correction and authorize these exact new bytes for the already-authorized J0956 swap:

- Master `owb_sa_s2_neptune_v07a.mp4`: `de62264cbd89758d677c0426002b688e7ebbeceabc4c2eb56b962f44cb4ecb12`.
- PHONE `owb_sa_s2_neptune_v07a_PHONE.mp4`: `f11e35a282c74e9792d86bd6a1f72937eb07f05ab16b7e2f9f710275c1c24f69`.

Ben's [6411201182](https://github.com/TheLaughingGod1986/orbit-with-ben/issues/264#issuecomment-6411201182) approved the creative v07 swap, following [Chief c48](https://github.com/TheLaughingGod1986/orbit-with-ben/issues/264#issuecomment-6402300872). Both comments were read directly. This is Codex's technical acceptance of v07a, not a new Ben approval. Original v07 approval provenance is preserved on J0956.

## Evidence reviewed and independently checked

Worker evidence: commit `91019833c124f0cd50dab2bf7ff1e35f443c6785`, all eight report/meta files under `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/06_Final-Exports/owb_sa_s2_neptune_v07a_*`, plus J0988 body, result and full history and J0956 body, result and full history.

- Source master SHA256 independently matches `0919db03d4325aaedc364aeca9c8514345e65d61d857e5e78497c6001957af3d`. Both new SHA256 values above match.
- Fresh decoded framemd5 comparisons: all 618 frames and timestamps identical between v07 and v07a, and independently between their PHONE versions. Video remains 30 fps, 20.600 s, with both streams starting at zero and lasting 20.600 s. Master 1080x1920; PHONE 720x1280. The submitted frame sheet was inspected.
- Fresh `ebur128=peak=true`: master and PHONE each **-14.1 LUFS / -1.8 dBTP**, meeting c61. Independently reproduced before measurements: master -14.1/-1.4, PHONE -14.1/-1.1.
- Master and PHONE decoded float PCM are byte-identical (SHA256 `427c4d1b3b45d63c6e2d8fce947278340849e58febf6b140b06709caec6a2878`). 988,800 decoded samples at 48 kHz; finite throughout.
- Independent first-ten-second cross-correlation: zero samples lag against original premix; -239 samples against v07, correlation 0.999326. This agrees with the documented correction of the old uncompensated 5 ms limiter delay. No word or creative timing edit.
- Original VO, VO stem, bed stem, SFX stem and premix hashes independently verified against the worker evidence/c48. The exact recorded commands stream-copy picture and apply only gain/limiting to the original premix, with latency compensation. PHONE stream-copies corrected master audio.
- Fresh open-gate run for 2026-10-27: PASS. Duration 20.6 s uses the existing J0216 test exception. Motion 4.56 and old opening similarity are the c48-accepted warnings. Additional similarity warning against `oyRcrFTYyDY` is the original copy being replaced, not another new Short. No failed gate waived.
- Submitted fresh polish, music, SFX and loop reports all PASS. Their tail-detail and music-pace warnings are unchanged from c48; picture and source stems are unchanged. Worker report records no clicks, pops, pumping or truncation. This review relies on that reported listening check and independently validates the signal, alignment and encoded levels; Codex does not claim a new subjective listening pass.
- All eleven entries in the manifest independently match on BOTH iCloud and NAS, including master, PHONE, sheets, meta and five gates plus audio report. Original versions remain intact.

## Delivery paths and follow-up

iCloud: `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/standalone_shorts_v07a/`.

NAS: `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/standalone_shorts_v07a/`.

Mark J0988 done and reopen J0956 with its dependency on J0988 retained and satisfied. Preserve J0956's delivery progress **1/4**; this review does not complete the upload. Its active master/version now refer to v07a and the hashes above. The original Ben-approved v07 file, version, time and comment remain recorded as creative approval provenance.

Next eligible Studio worker performs J0956 now: fresh live read-back of `oyRcrFTYyDY`, verify v07a hashes and all current upload gates, then follow the existing new-private-copy swap procedure. No Related video or long description link (standalone). Do not start upload after **27 Oct 10:45 London**. Both read-backs by **11:15 London**, otherwise new copy private/unscheduled and original retained for **11:30 London**. If any new failed gate or state mismatch occurs, stop and return for a concrete Chief ruling; never override it. No external wait or retry date is needed: inputs are ready and J0956 is actionable.

This review made no YouTube, Studio, Buffer or privacy changes and spent GBP0. It is the only review performed this run. Safe Mini repair reclaimed clean pushed worktrees/caches: 17,581 MB -> 22,272 MB free; no NAS move or deletion was needed.
