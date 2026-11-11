# J2452 — late observatory replacement checkpoint

Worker macbook. Continue branch macbook/J2452, PR #789 (base main). Compilation incomplete; no finished master, reel, NAS delivery or UAT card. No upload, Studio action, generation, sign-in, paid download or spend. HOS untouched.

## Adopted silent chapter

`/Users/ben/_desk/J2452-sleep-scratch/late_observatory_v04/029_picture_observatory_repaired_framefixed.mp4`

SHA-256 `4037046cbea93cbc2ad02b468016b5ec90def570122de11fad850e6a13e19760`.

Full decode and frame-clock checks: 14,829 frames, 494.30 seconds. This continues the closing-sky checkpoint and preserves its earlier repairs. Chapter seconds 330.00–338.8667 (source-master 350.50–359.36) replace the repeated La Silla footage with the film's own cleared `gemini_night.jpg`, its second appearance. The source is the actual Gemini North photograph, not VLT. The spoken window says “That is the answer most astronomers would give you. Not in our lifetimes, almost certainly.” No observatory is named there. Source identity, full credit, CC BY 4.0 licence, official page, and hashes are in REPORT.json, inherited from SOURCE_POOL_v03. No new asset was downloaded.

The real panoramic photograph is cropped to 16:9 with a gentle continuous push, 15% sleep darkening and the existing luma cap. Two-second endpoint dissolves use the previous and following shot frames, fully removing the repeated La Silla picture while preserving the narration clock. Those neighbouring original code graphics remain and still require their own replacement under the sleep plan; this does not approve them. The source master and narration are unchanged.

Normal combined `picture_qa` on the saved chapter: **FAIL, 11 of 78 rows, seven warnings**. All hard failures are remaining source reuse; none was waived. The replaced late observatory row no longer fails. No sampled pixel hard failure is reported. `late_observatory_qa_framefixed_v01/` contains the full results; its review sheet remains local. Normal QA sampled cut midpoints, not every video frame.

The independent checker verifies the full frame clock, source/output hashes, seven unchanged-chapter still samples, three opaque replacement samples, and the entire 266-frame replacement window at 320×180 against its separately encoded dissolved patch. READBACK.json records maximum replacement-frame mean error 0.646 (threshold 2); unchanged sample errors are at most 0.775. The seven-frame transition sheet was inspected: inherited constellation graphic dissolves into the real observatory/sky, then into the inherited stellar interior graphic. No moving-picture or listening review is claimed.

Only the framefixed output in v04 is adopted. The original v04 integration leaked one old-source frame due to the floating-point enable endpoint; the full-window check caught it without any relaxed threshold. The corrected enable endpoint lies halfway between the final included and next frame. v01 failed its panorama crop before producing frames; v02 used half-second fades; v03 used two-second fades but retained some repeated-shot pixels beneath them. All are explicitly marked rejected locally. Every process launched in this run finished; nothing is left encoding.

## Resume

1. Continue picture work from v04 and its cuts.json. `REMAINING_REUSE_CONTEXT.json` now lists all eleven remaining failed windows, exact source/master coordinates and their master-ASR spoken words. It is a locator, not factual approval. Replace actual picture, never just rename sources or adjust metadata to hide reuse.
2. Resolve the retained graphics/baked labels, quiet title and inter-film breath. Twelve other picture chapters and the initial darkening ramp remain. Preserve the thirteen narration chapters and measured 108:22.36 audio candidate described in RESUME_2026-11-11_0415.md.
3. Final assembly/mux, actual loudness/peak/silence/CTA/picture/join gates, ~12-minute reel, same-run NAS master/reel delivery with independent hashes, then Ben's finished-film watch card. Earliest air remains 12 December. Do not mark done or UAT.

Reproduce to a NEW local directory with repair_late_observatory.py --out NEW_DIR in the existing _desk/J2141-venv. Run check_late_observatory.py NEW_DIR, then normal scripts/picture_qa.py with the saved chapter and cuts.json, original SOURCE_POOL_v03 and betelgeuse_covers_pool_v01. Builders refuse overwrites. Python compile, seven email-ratchet tests and diff check pass.

Release because the remaining full assembly exceeds this unattended run's 25-minute limit. Thread read to #6789245666; trusted messages displayed, home-directory marker persistence remains restricted.
