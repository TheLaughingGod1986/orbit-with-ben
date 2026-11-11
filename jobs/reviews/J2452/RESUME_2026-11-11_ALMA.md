# J2452 — ALMA observation checkpoint

Worker macbook. Continue macbook/J2452, PR #789. Compilation incomplete: no final master/reel, delivery or UAT. Earliest air remains 12 December. HOS untouched.

## Adopted silent picture chapter

`/Users/ben/_desk/J2452-sleep-scratch/alma_betelgeuse_v02/029_picture_alma_betelgeuse.mp4`

SHA-256: `85d0090af6bb829b314b7a10dcdb703dce3565eb216c7114802016f8ef29c73b`.

Preserves the checked Earth/Crab and earlier repairs. Replaces third appearances of sphere_jan (chapter 51.90–58.2667 s) and visir_flames (438.60–445.8667 s) with a distinct real ALMA submillimetre observation of Betelgeuse, potw1726a. Used only under general age/lifetime and closing statements; it is not a 2019 before/after comparison or visible-light photograph. No script or narration changes. The emitting surface remains fully in frame in a 4000×2250 crop, with a 1.2% push, 15% darkening and inherited luma cap. Full official credit is overlaid visibly. Two appearances total.

Official page and terms checked live: https://www.eso.org/public/images/potw1726a/ and https://www.eso.org/public/outreach/copyright/. ESO labels it Observation, 4000×4000, credit ALMA (ESO/NAOJ/NRAO)/E. O’Gorman/P. Kervella; CC BY 4.0 allows adaptation with visible credit. Source, midpoint and transition-sheet stills inspected: unlabelled observation, complete emitting surface, no panels. No moving-picture/listening approval claimed. The candidate eso2109g was rejected from its official page because it is a sourced Chart; no download.

Source retained locally at `/Users/ben/_desk/J2452-sleep-scratch/alma_betelgeuse_source_v01/potw1726a.jpg`. SHA-256 `3f75e8b1df70dca7f0e828e8fd640880a7bfcbdef0945304792bace2eb243bbe`. No NAS writes were attempted: this run's direct worker instruction restricts files to checkouts and _desk, despite the later thread clarification of general NAS policy. Additive authorized transfer remains outstanding; do not mark delivered.

## Checks

Full decode and exact 14,829-frame clock PASS, 494.30 seconds. Every replacement frame compared at 320×180 against its independently encoded dissolved patch: 191 and 218 frames; maximum mean errors 0.973 and 0.893, threshold 2. Seven sparse unchanged samples PASS (maximum 0.649). These are sampled-resolution comparisons, not full-film perceptual approval.

Normal combined picture QA remains FAIL: **seven reuse rows** (down from nine), seven warnings, no sampled pixel hard failure. Both replacement rows pass. No override or threshold change. Full QA uses the flattened original SOURCE_POOL_v03, betelgeuse_covers_pool_v01, crab_reuse_v02/pool and alma_betelgeuse_v02/pool. Reports and cuts are tracked beside this note; media and sheets stay local.

The first local alma_betelgeuse_v01 output is rejected: its before-frame still contained the old SPHERE image. v02 starts both windows 15 frames earlier, shortening the preceding cut, and uses exact-index before frames. Both inspected before frames show only the preceding Sun/Orion shot. Never continue v01.

## Resume

Use `/Users/ben/_desk/J2452-sleep-scratch/alma_betelgeuse_v02/029_picture_alma_betelgeuse.mp4` and alma_betelgeuse_v02/cuts.json. Reproduce with _desk/J2141-venv/bin/python repair_alma_betelgeuse.py --out NEW_DIRECTORY, then check_alma_betelgeuse.py NEW_DIRECTORY. Builders refuse overwrites and pin base/source hashes.

REMAINING_REUSE_CONTEXT.json lists the seven failed windows. Retained graphics/baked labels also require the sleep-plan pass. Twelve other picture chapters, ramp, quiet titles, breaths, final AV assembly, loudness/peak/silence/CTA/picture/join checks, ~12-minute reel and hash-verified delivery remain before Ben's finished-film watch. Preserve the measured 108:22.36 audio candidate and all source masters.

Scripts compile, seven email-ratchet tests and diff check PASS. Release at this verified checkpoint because the remaining full assembly exceeds this unattended wake. All launched processes finished; checkout returned to main. No upload, Studio change, generation, sign-in or spend. Thread read to #6790451971 (trusted message displayed; home marker persistence restricted).
