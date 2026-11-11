# J2452 — closing sky checkpoint, 11 November 2026

Worker macbook. Continue branch macbook/J2452, existing PR #789. Build incomplete; no finished compilation, reel, NAS delivery or UAT. No upload, Studio change, generation, sign-in or spend. HOS untouched.

## Saved silent chapter

`/Users/ben/_desk/J2452-sleep-scratch/closing_integrated_v01/029_picture_closing_repaired.mp4`

SHA-256 `e98ee41b19755d7b42e0b96e28d9bcf1d83b4b43e4e1d33bc91a958dd0c3d8d8`. Full decode and frame-count verification: 14,829 frames, 494.30 seconds. This replaces the observation-grade checkpoint for future picture work; its previous Orion, Chajnantor, observation-grade and Orbit-cover work remains.

The last La Silla sky shot uses native source seconds 10.2–15.7333 instead of 9.5–15.0333. The earlier appearance uses 0–5.23, so these are non-overlapping intervals, without loops or retiming. Original ESO/S. Brunier credit, CC BY 4.0, is retained from SOURCE_POOL_v03; no new download. A two-second endpoint dissolve preserves the chapter clock. The film source/master and narration are unchanged.

Normal bounded join polish passes with two warnings (edge density and low detail). The first QA metadata omitted the transition's video offset, so the gate treated the dissolve as a still push and failed jitter. The corrected metadata explicitly identifies closing_join.mp4 at offset zero; no gate flags, thresholds or exemptions changed. The first render also used the wrong credit and is rejected; use v02 only.

Independent read-back compares three replacement samples with the original source at the intended times: correlations all above 0.998, mean grayscale errors 1.81–2.03 after grading. Six unchanged-chapter samples differ by at most 0.527 grayscale levels; three integrated patch samples match exactly. These are sparse still checks, not every-frame or moving-picture/listening review. Eight saved stills were inspected together; sky, observatory framing and credit are visible, with the incoming dissolve over the preceding Earth shot.

## Remaining work

Source-only QA on the proposed map has 12 failures rather than 13, with two warnings; this fixes just the last sky reuse. Twelve reuse failures, original code graphics/baked labels, other chapters, darkening ramp, quiet titles, inter-film breaths, final AV/CTA/picture/join gates, ~12-minute reel and same-run NAS delivery with hash read-back remain. Do not mark done or UAT. Earliest air remains 12 December.

Reproduce to fresh local directories with repair_closing_sky.py, check_closing_sky.py and integrate_closing_sky.py. Existing outputs are never overwritten. Whole-chapter combined QA is saved in closing_integrated_qa_v01: FAIL, 12 of 78 rows, all reuse; seven warnings. No pixel hard failures at the sampled cut midpoints. The gate review sheet stays local.

Thread read to #6788553056. Trusted posts displayed; home-directory marker persistence remains restricted.
