# J2452 — Saturn checkpoint, 11 November 2026

Worker macbook. Compilation incomplete; progress remains **1 of 15**, Moon saved. Saturn has not passed and has not been copied to the NAS. No final OK, master, reel, UAT, upload or spend.

## Resume this candidate

Local output: `/Users/ben/_desk/J2452-sleep-scratch/public_saturn_v03/021_saturn_undarkened_v03.mp4`.

SHA-256 `a7ed2909dd725133a6619637a000cf233f60bce8d09e6a35dd1a04ed810e62ee`. Duration **518.9 seconds**, full decode **15,567 frames**, exit 0. Read-back and all five brightest two-second windows with individual stills are local beside it. The build, read-back, classified full pixel findings and edit QA are tracked under `public_saturn_v03/`.

Measured AAC candidate audio: **−20.23 LUFS integrated**, **−5.93 dBTP**, **2.50 LU LRA**. The true peak exceeds the eventual −6 dBTP ceiling by 0.07 dB; this is not an audio PASS. Final mixing/limiting must resolve it and remeasure the encoded delivery. Narration-only candidate; continuous bed and final sound/silence/CTA gates remain. Saturn ends before the darkening ramp; identity darkening applies, and no dimming has been used to hide failures.

## Gates: FAIL, no waiver

- Full polish: **46 findings**, of which **3** are in new-edit neighbourhoods (73, 103 and 105 seconds); **43** are outside all changed windows plus their two-second margins and are recorded as “in the public film.”
- New-edit picture QA: **7 failures / 240 samples**, plus **50 warnings**. One low-detail sample at the first dissolve (row `change-0-17`, around 8.75 seconds), then near-black at rows `change-1-2`, `change-1-3`, `change-1-64` through `change-1-67` (around 72.25, 72.75, 103.25, 103.75, 104.25, 104.75 seconds). Use exact row intervals in `changed_dense_cuts.json`, not the rounded display times.
- These new-edit failures must be repaired; none is inherited or approved. The first dissolve and the outer edges of the extended Orbit cover are the remaining measured defects. Do not start Earth Spin or declare Saturn completed.

## Work retained

Finished-public-master picture cut at the corrected clean narration boundaries (0–9.6, 21–209.65, 219.55–540.2 seconds). Quiet chapter title; two-second dissolves only where this compilation cuts. Hook/Orbit/act-card covers follow the inspected actual master, not the plan's drifted picture estimates. See `SATURN_COVER_SCOPE.md` and the build JSON for source mappings.

Three versioned local candidates remain intact. Candidate 1 failed full polish (64) and edit QA (61). Candidate 2 still failed pixel checks; its redundant subsequent QA/read-back was interrupted after those failures were confirmed while candidate 3 rendered. Candidate 3 completed both gates and full decode/brightness/audio read-back. No original media or prior candidate was replaced or deleted. No external picture was used, and no further source searches or generation are authorized by this checkpoint. The last two repairs use this same master's neighboring pictures, including slowing picture only; narration timing is unchanged.

Next: use the exact saved failure frames/row windows to scope the first-dissolve and Orbit-cover boundary repair before another encode. Reuse the current sources and respect the cover investigation limit; do not restart an unbounded footage search or rebuild source films. Preserve the narration clock, all existing versions and all gates. Then repeat full polish/edit QA, decode/frame count and brightness read-back; resolve encoded audio peak for delivery. Only a passing chapter is saved additively with hash read-back, then recorded as step 2 of 15.

No completed Saturn chapter, full compilation, reel or UAT is claimed. Eventual watch card must say public charts/labels remain and dissolves are only on compilation cuts. Earliest air date remains 12 December. No upload or Studio operation. Python compilation, diff check, seven email-ratchet and five private-network tests passed. All launched processes ended before release. OWB returned to main; HOS stayed on main and was unchanged.

Thread read to #6793004210. The read command displayed that owner-trusted comment but could not update its home-directory checkpoint under the restricted filesystem; no account or sign-in change was attempted.
