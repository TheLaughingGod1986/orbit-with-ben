# J2795 — music reuse diagnosis (13 November 2026)

Worker proposal for elected Chief. J2035 remains held. No production gate, waiver, score acceptance, media, narration, diagram KEEP, YouTube or Buffer state changed. No spend. This session has no demonstrated audio input; all findings here are measurements. Gemini's J2783 listening testimony is separate evidence, not a numeric PASS.

## Finding

The complete 77-file comparison was reproduced with zero unreadable files. RESULTS.json records every path, mapped read path, SHA256, unrounded score, best lag and overlap. The three existing hits reproduce at 0.803806, 0.810553 and 0.821338. Each is only **21 seconds** long: candidate seconds 0–21 against HOS002 seconds 89–110 or OWB013 seconds 129–150. They do not represent 300 seconds of matching musical structure.

The earlier J2783 description of a time-averaged chroma metric is inaccurate. The implementation uses time-centred 24-band log energy in one-second frames, unit-normalizes each frame, and maximizes the aligned mean cosine across all lags with at least 20 seconds of overlap. It is not chroma and retains temporal alignment. However, temporal centering does not remove a broadband gain envelope shared by all bands. A slow opening or closing level trend can therefore dominate the feature direction. Searching many short edge overlaps compounds this problem.

A general false-positive mechanism is demonstrated independently of this film: two separately drawn random waveforms (fixed reproducible RNG seed, separate sample draws; no reused samples) sharing only a quadratic loudness envelope score **0.928436**, above the unchanged 0.8 threshold. Independent original tonal compositions with disjoint pitch sets score 0.497642. Positive controls on the real HOS009 recording score 1.000000 identical, 0.984327 at −12 dB, and 0.973770 after trimming 37 seconds and applying −12 dB. The latter correctly finds lag −37, overlap 263 seconds. Control PCM hashes and all results are saved.

The two tonal controls are original deterministic analytical compositions defined in probe.py, not public recorded music or an independent human listening corpus. The production comparisons are independently sourced recordings from the HOS002 and OWB013 archive paths, whose bytes are hashed in RESULTS.json; independent generation/musical distinctness is supported by the prior provenance and attributed Gemini testimony, not newly established by ear here. Different hashes alone never prove different composition. No new external composition corpus was licensed or downloaded in this bounded run.

## Concrete proposal

Draft only: candidate.py removes the common log-energy component from each frame before the existing temporal centering. It keeps the same bands, comparison horizon, offset search, overlap minimum and threshold. It is isolated under this investigation folder; scripts/music_gate.py is byte-unchanged. The three tests in test_candidate.py demonstrate the envelope confound and preserve genuine reuse detection through trim/gain and lossy re-encoding. The experimental scores for **all 77** production comparisons and the real-bed controls are retained, including any experimental failures. No comparison is silently dropped and no threshold was tuned to HOS009. The experimental maximums for the three old hits fall to 0.278080 / 0.354718 / 0.450138; none of the 77 exceeds 0.8. Real-bed experimental controls remain 1.000000 identical, 0.971540 gain, 0.974253 trim/gain. Independent noise falls to 0.106389 and independent tonal controls to 0.496223. These are experimental feature scores, not a production PASS.

Do not deploy this prototype or treat its scores as gate results. Removing broadband level information could lose evidence for genuine reuse in stationary or low-variation beds; log1p also limits exact gain invariance at low energy. A melody/rhythm fingerprint or complementary independent spectral check may be needed. Short or silent tracks and non-integer offsets need wider validation. Only the first 300 seconds are compared by either feature path; this probe does not establish full-recording nonreuse.

Recommend Chief review this draft as demonstrated grounds for a general correction, then scope a separate bounded validation: a labelled set of independently composed real recordings spanning ambient and chamber music, with known reused versions (fractional-second trim, gain, fades, lossy encoding) and stationary/drone controls. Require all positives detected and independent negatives rejected before choosing a correction. Preserve threshold and library coverage; improve gate reporting to retain matched windows. HOS studio/RULES.md's contract requires Ben's OK for a correction to a failed check; Chief should present the concrete validated correction for that required final approval. Only after authorised deployment, rerun the production gate on the complete inventory and obtain final score acceptance. This draft does not supply either approval.

Do not regenerate the score just to chase a weak metric while this specific defect is assessed. If Chief declines a correction, it must separately scope any revised music (bounded takes, cue lengths, subscription cap and fresh balance/guard checks); this investigation authorises no generation. Existing assembly deadline: 15 November 2026 18:00 UTC.

## Reproduction

From the proposal checkout, with Python + numpy and ffmpeg available:

```
/Volumes/MiniWork/scratch/J2563-pdf-env/bin/python jobs/reviews/J2795/probe.py
/Volumes/MiniWork/scratch/J2563-pdf-env/bin/python jobs/reviews/J2795/test_candidate.py
```

The probe reads the exact saved RESULTS.json inventory, uses the existing materialized UAT copies, and overwrites only its own report. The original discovery used J2664 comparison_files with same-film and AppleDouble exclusions, yielding the same 77 count as J2791; its roots are retained. Prior reports, audio files and the production gate are read-only. Test result: 3 tests, OK. The candidate-bed SHA256 is d7f5bf3d7553d7c611a913e93602b8ec83419821059294ddeaee32269a4f9572; the exact production gate source hash is retained in RESULTS.json.
