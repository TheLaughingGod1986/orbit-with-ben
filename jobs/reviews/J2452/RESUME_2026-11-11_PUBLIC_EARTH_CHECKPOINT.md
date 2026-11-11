# J2452 — Earth Spin unfinished checkpoint, 11 November 2026

Worker macbook-2. **Progress remains 2 of 15.** Moon and Saturn are saved; Earth Spin is not delivered. No full compilation, reel, UAT, upload or spend. This run stops at its time limit with no encode left running.

## Current candidate

Local scratch: `/Users/ben/_desk/J2452-sleep-scratch/public_earth_v03/027_earth_undarkened_v03.mp4`.

The picture is cut from the finished 027 master, with its already checked clean narration. Used master ranges remain 0–164.45 and 169.90–443.50 seconds. The subscribe sentence is removed whole. No shot-list reconstruction or fresh source search. Public-source charts and labels stay; dissolves apply only to compilation edits.

The narration is 438.05 seconds. The build's floating-point cumulative rounding selected 13,141 frames / 438.033333 seconds: a 16.7 ms difference in the trailing breath, not a clipped word. Both candidates v02 and v03 have that recorded frame count. The original checker tried sampling a tiny tail interval after the last video PTS and its pixel gate crashed with an empty frame. This was a checker-boundary error, not evidence of a missing encoded frame. The checker now merges sub-frame tails into the preceding sampling bin and bounds edit sampling by the final PTS; full decode still counts every frame.

## What was changed and what remains

- Exact seeks in the actual master confirmed five chapter cards at 23.26–25.76, 93.50–96.00, 175.32–177.82, 248.38–250.88 and 356.78–359.28 seconds, and Orbit shots at 66.10–74.30 and 219.2667–225.9333. These are covered in the candidates. The five-second contact sheet is a guide, not exact boundary evidence.
- The plan's named EPIC file was absent at the planned footage path and archived edit root. J2548's named ISS pool file exists at `027_What-If-Earth-Stopped-Spinning/07_Edit-Project/pool_v01/iss/Five_Minutes_in_Orbit.webm`; its inspected 18-second frame is near-black and decoding warns of premature EOF. The Chief's explicit neighbouring-master-picture fallback was used. No extended search, generated footage or source film rebuild.
- v02 new-edit QA had 18 failed samples. v03 repairs the opening gutter, the cover's dark interior, the subscribe-join gutter and the clock-card neighbourhood using held/slowed neighbouring master picture. Its first edit QA has **three remaining near-black failures at 61.25, 61.75 and 62.25 seconds**, in the two-second neighbourhood before the expanded north-pole cover. These are not waived or reclassified as untouched source.
- **The opening repair also covers the quiet chapter title. Restore that title before delivery.** Inspect it and all cover boundaries, then rerun the whole undarkened pixel check and edit-neighbourhood picture QA. The next boundary repair should begin before the source's dark diagram (the adjacent daylight ISS stretch around 54 seconds is a candidate), rather than repeatedly moving a boundary inside that same diagram. Verify both two-second margins.
- No darkening was applied. The guarded darkening helper refuses delivery before a verified quiet title and successful edit QA. It calculates chapter start from the two saved NAS chapters and their four-second breaths, applies the 19:30–20:30 ramp, and checks frame count, duration and two-second brightness ratios. A three-frame probe of the pixel-based grade measured 85.02%, 85.00% and 85.06%; that is only a filter probe, not a graded chapter verification. The quick eq filter failed dim-picture ratios and is not used.
- Final sound/bed/silence/CTA/whole-film joins, the remaining chapters, NAS master/reel copies and Ben's watch card remain owed. Nothing from this Earth run was copied to the NAS or offered as a finished chapter.

## Resume commands and evidence

Use `/Users/ben/_desk/J2141-venv/bin/python` (Pillow/numpy installed). All outputs are additive and existing candidates are retained. Helpers are in this directory: `build_public_earth.py`, `repair_public_earth_cards.py`, `repair_public_earth_pixels.py`, `check_public_earth.py`; darkening/save helpers are guarded, unrun follow-up tools.

`public_earth_v03_checked_v04` is a separate read-back directory using the corrected endpoint sampler and the same v03 video, not a new encode. Its `BUILD.json` explicitly records `quiet_title_verified: false`. Read its gate logs and reports before resuming. Do not treat this checkpoint as a chapter PASS.

Candidate SHA-256: `6968fec618d9d160aab93469a79b1b252bfc63f17e65f36fcb4111834db55533`. The corrected pixel gate completes with 12 findings; the evidence record is `public_earth_checkpoint_v03.json`. Python compilation, diff check and all 12 privacy tests passed.

Thread read to #6794149539.
