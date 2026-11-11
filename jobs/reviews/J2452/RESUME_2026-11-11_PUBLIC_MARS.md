# J2452 — Mars undarkened checkpoint, 11 November 2026

Worker macbook-2. Progress stays **3 of 15**: Moon, Saturn and Earth are saved; Mars has not been darkened or delivered to the NAS. Full compilation, reel and UAT remain unfinished. No upload, Studio change, generation or spend.

## Build

Mars uses the existing corrected narration slices from picture_timeline_v01.json, chapter four: master 0–28.3, 40.8–224.5, 231–451.5 and 453.2–483.2 seconds. Total 462.5 seconds / 13,875 frames. Its clean narration hash is checked by the builder. Finished master is the plan's 025_MarsRobot_full_rough_v03f.mp4. No reconstruction of the source film.

Local candidates are under `/Users/ben/_desk/J2452-sleep-scratch/public_mars_v01` through `public_mars_v04`. Earlier candidates remain. v01 built the trims, cover pieces, quiet name and compilation-only dissolves. v02 covered the additional Cold act-card (observed master 133.5–136 seconds), using neighbouring master 137–144. v03 moved the quiet name to y=80 to avoid the source Opportunity caption; frame at chapter three seconds inspected and clear. Winter uses the named, copied PIA19400.tif; J2548/COPIED.md provides its existing hash/provenance. The missing wheel pool was checked at the named NAS and archived edit paths; own neighbouring finished-master rover picture used, no generation or extended source search.

v03 decoded all 13,875 frames. Narration measured -20.72 LUFS / -6.46 dBTP. Full pixel scan found five low-detail findings at chapter 373, 375, 377, 379 and 381 seconds (master 392–400), all outside compilation edits: in the public film under the Chief's ruling. Detailed edit QA FAILED one row at 213.5 seconds, inside the new subscribe-removal join. Its review sheet also showed residual Subscribe/Dust graphics nearby. No waiver and no darkening of that failed candidate.

v04 patches chapter 209–217 with finished-master 250–258 (solar-panel and ground picture), with one-second edge fades. Still contact sheet at chapter 215–222 confirms that the patch also removes the residual Dust graphic there. Run logs and final v04 gate results accompany this checkpoint when available. Other cover edges still need explicit still inspection before grading; do not infer this from machine PASS. The grade script now requires an explicit verified-covers flag.

## Next run

1. Read `public_mars_v04/READBACK.json` and its PICTURE_QA.md. Fix any new-edit failure; source-film exceptions apply only as recorded by the Chief.
2. Inspect the advisory sheet and all cover boundaries for remaining cards, Orbit or subscribe graphics, using the v04 output; inspect exact frames around anything uncertain. Record the actual observations. Set `unwanted_cards_removed_verified` only once established.
3. Grade and measure with darken_public_mars.py (constant 85 percent; Mars is entirely after compilation 20:30), then save_public_mars.py. Neither was executed this run. Save additively and verify destination hashes; only then record step 4 of 15.
4. Venus next in running order, then remaining chapters, continuous bed, final sound/CTA/join checks, full master and twelve-minute reel, hashes and Ben's watch card. Earliest air date 12 December.

Python compilation and twelve privacy tests passed; final diff check recorded at handoff. This is a local unfinished chapter candidate, not a finished master for Ben's watch, and is not UAT.

## Final read-back

v04 edit QA PASS: 0 failures / 219 cuts, 27 advisories. Full decode: 13875 frames, matching 462.5 seconds at 30 fps. Narration -20.72 LUFS / -6.46 dBTP. Full pixel scan retains the same five inherited source-film findings; none classified as a new edit. SHA-256 `e43a78d1b282ea6c4dd2b5fc8bc5f80f7b33fd81e6a8bbfa4bdc0ee97456e08e`. Final reports committed beside this checkpoint. No launched process remains.

Thread read to #6798873666.
