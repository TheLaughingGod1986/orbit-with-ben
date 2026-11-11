# J2452 — observation grade checkpoint, 11 November 2026

Worker: macbook. Branch macbook/J2452, existing PR #789. Compilation incomplete: no finished master/reel, NAS delivery or UAT. No upload, Studio action, generation, sign-in or spend. HOS untouched.

## Latest silent chapter checkpoint

`/Users/ben/_desk/J2452-sleep-scratch/observation_grade_v02/029_picture_observation_grade.mp4`

SHA-256: `8496226aca2f3f37b62fd2ae0b09f648fc3f0d972ae43212a8fa43c1f1abe979`.

Full decode and frame count: 14,829 frames, 494.30 seconds. Starts from the hash-pinned Chajnantor-repaired chapter, retaining the earlier Orion and Orbit-cover repairs. The five sphere_dec / companion_speckle observation shots receive six 8-bit luma code values of display lift, with 0.3-second shoulders inside their endpoints and the existing Y=180 highlight cap. No observation geometry, timing or chroma edit. This is a presentation grade, not recovery of scientific detail. The inherited compressed source texture and baked labels remain; it is not a final picture recipe.

Normal saved-file polish PASS: **0 of 78 rows failed, 6 warned**, no overrides, no no-jitter flag, no sleep exemption, no changed threshold. Prior five near-black failures are removed. Warnings remain in the tracked POLISH_GATE.json and require review. This PASS does not approve the chapter or compilation.

Independent saved-file read-back checks 25 samples around/within all five windows plus four retained-repair midpoints. Inside-window mean full-range grayscale increases: 6.783–7.038. Maximum mean absolute difference outside windows/at retained repair samples: 0.525 (threshold 1.5). Hashes match. The comparison sheet was inspected: star/companion framing and baked text remain, with a modest brighter background; no scientific detail recovery or moving-picture/listening review is claimed. The sheet is local, beside the output.

The first encode (`observation_grade_v01`) evaluated the expression on every frame and was interrupted with SIGINT to keep this wake bounded. Its partial media is retained with REJECTED.md; never use it. v02 uses the filter's timeline enable over the five shots and completed. The builder refuses overwrites.

## Source gate is still FAIL

Normal source-only picture_qa with the original SOURCE_POOL_v03 plus the cover pool reports **13 reuse failures / 78 cuts, 2 warnings**. It has no video argument and is not a pixel gate. See observation_source_preflight_v02/PICTURE_QA.md and picture_qa.json. All source failures remain unwaived: third appearances of sphere_jan, sphere_dec, crab and visir; repeated stretches of La Silla, Chajnantor, Orion, ALMA and the astrolabe graphic. These inherited source rows must be replaced/remapped honestly; a polish PASS is insufficient. Normal combined picture_qa must run after the actual remaining recipe is finished.

## Resume

1. Continue from this v02 checkpoint and cuts.json. Preserve prior checkpoints. Resolve source reuse, the 22 original graphics and unwanted baked labels, sleep dissolves, quiet chapter title and inter-film breath. Use actual source/master coordinates and retain all gates.
2. Twelve other picture chapters and the initial darkening ramp still require assembly. Thirteen narration chapters, the 108:22.36 audio candidate and the NAS thumbnail are unchanged; use RESUME_2026-11-11_0415.md and picture_timeline_v01.json for those coordinates.
3. Final assembly without re-encoding the joined chapters, actual mux loudness/peak/silence/CTA/picture/join checks, ~12-minute spot-check reel, same-run NAS master/reel delivery with hash read-back, then finished-film watch card. Earliest air remains 12 December. No completion or UAT claim.

Reproduce to a new local directory with grade_observation_spans.py --out NEW_DIR, check_observation_grade.py NEW_DIR, then normal scripts/polish_gate.py with its cuts.json. Existing _desk/J2141-venv supplies numpy/Pillow. No process remains at release. Seven email ratchet tests pass, both helpers compile, diff check passes.

Thread read to #6788500828. Read displayed trusted messages, but the home-directory marker write is restricted; no attempt was made to change that location.
