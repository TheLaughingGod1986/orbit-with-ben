# J2803 — owned-bed validation of the J2795 music candidate (14 November 2026)

Worker record for the elected Chief. This is J2795-V. It follows HOS desk comment 6867889512 and draft OWB PR 908 at `838773d2d4`. The diagnosis stays accepted only as grounds for a general correction. This run is not a gate PASS, not a film PASS, and not a deployment.

`scripts/music_gate.py` is byte-unchanged. Its SHA-256 is still `62b5159f95598eaca5256b30ba66144812bad97dc86fd0c9de4618e4a1dd5385`, the same hash J2795 recorded. The candidate file in this folder is byte-identical to PR 908 `jobs/reviews/J2795/candidate.py` (`7c5a915cc2e55911c7d080cc05eac418d770298e5e0d6e64b746f6087ecfba54`). Threshold stays 0.8 (`music_gate.SIM_FAIL`). No file was dropped from the saved 77-file inventory. No music was generated, downloaded, or spent. No YouTube or Buffer state was changed. J2035 was not released.

This session did not listen to the beds. Style labels come from each plan's own prompt. A different file hash is recorded and is not treated as proof of a different composition.

## Corpus, recorded before scoring

`CORPUS.json` was written with `"measured": false` before any similarity call. `RESULTS.json` stores that file's SHA-256. Both features then saw the same decoded audio, capped at the production 300 seconds.

| Id | Work | Own-prompt words | Role in the bar |
|---|---|---|---|
| hos009-wonder | HOS:009 | chamber, drone; "sustained" and "no drum beat"; also "sparse plucks" | Stationary/drone positives. Plan SHA matches the file (`95dfe11d7c21…`, J2664). |
| hos006-trees | HOS:006 | chamber, drone | Chamber positives. Own synthesis, £0. |
| owb028-gliese | OWB:028 | ambient | Ambient positives. Own synthesis, £0. |
| owb029-betelgeuse | OWB:029 | ambient | Ambient positives. |
| owb031-magnetic | OWB:031 | drone | Drone-chapter positives. The plan also describes a rhythmic pulse, so this bed is not the stationary control. |
| hos009-teach | HOS:009 | chamber | Same score as wonder (separate song id). Unresolved against wonder. |
| owb026-nearest | OWB:026 | none of ambient, chamber, drone | Extra independent bed. Its plan does not use those style words. |
| owb-j01-linking | OWB:J01 | drone; "reused from the owned 026 nearest-star stem" | Not an independent negative. |

Positives, fixed before the run, on every admitted source bed: trim 0.37 s; gain −12 dB; fade-in 0.8 s and fade-out 1.2 s; 64 kbps mp3 round-trip; all four of those together. Independent negatives are pairs from different films whose plans do not say one reuses the other. J01 stays unresolved against every other bed because its plan says it is reused. Wonder against teach stays unresolved because they are two cues of one score.

## Validation bar

**Not met.**

The candidate had to score every positive at 0.8 or above, every independent negative below 0.8, and still catch the stationary/drone positives. Counts: 25 positives, 20 independent negatives, 8 unresolved pairs, 5 stationary positives.

Two stationary positives of HOS 009 wonder are under 0.8. The reported window is the long alignment, lag 0, overlap 179 seconds, not a 21-second edge:

| Pair | Candidate | Production | Lag | Overlap |
|---|---:|---:|---:|---:|
| wonder, trim 0.37 s | 0.693 | 0.736 | 0 | 179 s |
| wonder, trim + gain + fades + mp3 | 0.633 | 0.685 | 0 | 179 s |

Production misses the same two. The candidate is lower on both. The other three wonder positives stay above the bar: gain 0.933, fades 1.000, mp3 0.9998, all at lag 0 and 180 seconds. Fractional trims of the other beds also stay above it: trees 0.952, Gliese 0.895, Betelgeuse 0.871, magnetic 0.920. Their combined transforms do too (lowest of those is Betelgeuse at 0.847).

All 20 independent negatives fall below 0.8 on the candidate. The highest candidate score in that set is 0.294 (Gliese against Betelgeuse). The highest production score in that set is 0.638 (wonder against the nearest-star bed), still under 0.8. This full-bed set does not reproduce the three short-edge production hits from the 77-file inventory. Those hits remain in the regression file below.

Unresolved, and not used for the bar: J01 against the nearest-star bed scores 0.914 (candidate) and 0.940 (production) at lag 0 over 180 seconds. That agrees with the written "reused from" line. It is not an ear confirmation. Wonder against teach scores 0.088 on the candidate and 0.314 on production.

## Integer-offset diagnostic, not part of the bar

After the bar failed, the same wonder cue was trimmed by whole seconds. `DIAGNOSTIC_INTEGER_TRIM.json` records it. Candidate scores: 1.000 at a 1 s trim (lag −1, overlap 179), 0.996 at 17 s (lag −17), 0.987 at 37 s (lag −37). The matched-window fields name those offsets. A 0.37 s trim stays on lag 0, because the frame hop is one second, and the mean cosine over that nearest window is under 0.8. Whole-second reuse of this cue is still detected. The required fractional-second reuse is not.

## 77-file regression context

`regression_j2795_77.json` copies all 77 comparison scores and match windows from PR 908 `RESULTS.json`. It does not rerun that gate. Prototype figures there are not production results.

Production still has 3 scores at or above 0.8, each a 21-second overlap: moon-leaving part 02 at 0.821 (lag 129, candidate window starts at 0 s and the other bed at 129 s); HOS 002 workshop v01 at 0.804 (lag 89); HOS 002 workshop v02 at 0.811 (lag 89). The isolated candidate's saved scores on those three are 0.450, 0.278 and 0.355. None of the 77 prototype scores reach 0.8. The highest is 0.450.

## Matched-window proposal

`windows.py` reports score, lag in seconds, overlap in seconds, and both source windows as `[start, end)` on the one-second frame grid. The score is `music_gate.similarity` on the same frames. `test_windows.py` is the focused regression: five tests, OK, including a 17 s offset (lag −17, window A starts at 17 s), a 0.37 s synthetic trim still at or above 0.8, and the J2795 shared-envelope noise pair (production at or above 0.8, candidate below 0.8). The proposal is not connected to `scripts/music_gate.py`.

## What this means for the ruling

The concrete correction is not ready for the approval that comment 6867889512 requires before any deploy. The candidate rejects the independent owned beds in this set, and it keeps gain, fade, and lossy copies of the wonder cue, but it misses a fractional-second trim of that stationary/drone cue, including when gain, fades, and mp3 are added. Whole-second trims of the same cue do not show that miss. Deploying the prototype, retuning 0.8, or dropping a library file would not be justified by this run.

PR 908 stays draft and unmerged. This validation and that diagnosis are for one records review. No waiver. No assembly release. No revised-music generation: the ruling leaves any fallback scope to the Chief, with bounded takes, the subscription cap, and fresh meter checks. J2035 stays on its dependency hold.

## Reproduction

```
/tmp/j2803-py/bin/python jobs/reviews/J2803/test_windows.py
/tmp/j2803-py/bin/python jobs/reviews/J2803/validate.py
```

The corpus run reads the studio-live music paths listed in `CORPUS.json` and rewrites `CORPUS.json` and `RESULTS.json` in this folder only.
