# J2452 — Light Speed cover fixed; darkening fails, 11 November 2026

Worker macbook. Progress stays **10/15**. PR #789 remains open on macbook/J2452. No NAS chapter delivered, no UAT, upload, Studio action, spend or deletion. All processes launched by this wake ended.

## Verified undarkened chapter

Local `/Users/ben/_desk/J2452-sleep-scratch/public_light_v06/024_light_undarkened_v04.mp4`.
SHA-256 `621f6d198475a1e02f240f56691e41f16794625850c25315fa0ae5b30d87fcae`.
Full decode: **13,900 frames / 463.333 seconds**. Narration **-20.73 LUFS / -6.56 dBTP**, LRA 3 LU. Final bed and mix are still owed.

Integrated the prepared finished-master 221–224s starfield cover at chapter 196–202s. The first attempt (public_light_v05) still exposed a faint “The Trip” card at 201.8s during its exit fade: rejected despite passing edit metrics. v06 adds a 0.6s cloned tail and moves the exit fade to 202.2–202.6s. Dense still review at 195.9–202.8s shows no old card at the sampled edges. Full edit sheet and advisory sheet inspected, plus the quiet-title frame at 3s. No playback/listening claim. Existing teaching charts/labels remain under Chief's version-1 scope.

Fresh edit QA: **PASS, 241 samples, zero failures, 30 advisories** (starfield, launch exhaust and retained teaching graphics). Full pixel scan: **21 inherited findings**, all outside compilation edit neighbourhoods, classified “in the public film” under the 09:29 ruling; full pixel verdict remains FAIL, not waived. Reports, cut lists and dense edge times are tracked in public_light_v06. Sheets remain local beside the build, no media in git.

## Darkening rejected — do not save it

Local rejected file `/Users/ben/_desk/J2452-sleep-scratch/public_light_dark_v01/024_light_darkened_v01.mp4`; hash and failure details in public_light_v06/DARKENING_FAILED.json. Normal ten-bit LUT then 8-bit CRF18 encode fails five two-second windows:

| Chapter start | Measured ratio | Required |
|---|---:|---:|
| 68s | 0.875184 | 0.83–0.87 |
| 398s | 0.880310 | 0.83–0.87 |
| 406s | 0.875663 | 0.83–0.87 |
| 440s | 0.829727 | 0.83–0.87 |
| 442s | 0.898221 | 0.83–0.87 |

No DARKEN_READBACK.json or NAS_COPY.json was produced. Do not use --verify-existing as a bypass.

Short local probes are recorded in grade_probes_v01.json (lossless and rounded 8-bit), v03 (explicit scale dither), and v04 (spatial rounding). None passes every tested window. Lossless alone and explicit swscale dithering do not solve the problem. Spatial rounding still fails 398, 440 and 442 seconds. The available ffmpeg has no zscale filter; that attempted probe stopped immediately. Quantization of very dark frames and the 8-bit downsampled measurement are a plausible cause, not proven. Do not loosen the tolerance or classify grade failures as inherited source findings.

## Next run

1. Keep this verified undarkened v06; do not rebuild its pictures or redo source searches.
2. Resolve the strict grade measurement failure on the five short windows first. Check whether full-resolution/high-precision Y measurement changes the result before another full encode; current scan downsamples to 8-bit 160×90 then subtracts legal black. A changed measurement must still measure actual saved pixels honestly, not hide failure. Preserve the two-point tolerance.
3. Write a new darkening version and output name (v01 remains rejected), run full before/after frame/duration and every-window brightness checks, inspect five brightest windows, then save additively with destination byte/hash read-back. Helpers currently target v06 source but rejected dark_v01 output; change output version before rerunning.
4. Only after a verified NAS copy advance to 11/15. Then 026 and 019, final bed/mix/CTA/silence/joins, master/reel copies and Ben's watch card remain.

Python helper compilation, 13 privacy tests and diff check pass. No long retry was started because encode plus two full measurement scans would exceed the remaining wake. OWB returned to main at handoff; HOS untouched. Thread read to #6804671657 at session start.
