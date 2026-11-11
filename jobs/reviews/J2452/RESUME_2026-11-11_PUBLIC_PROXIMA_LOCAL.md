# J2452 — Proxima locally verified, delivery checkpoint

Worker macbook; branch macbook/J2452, existing PR #789. The overall compilation is unfinished and is not ready for UAT. Previous delivered progress is 11/15. Do not advance to 12 until the NAS destination and its record are verified.

## Local chapter

Scratch relative to the worker's existing J2452-sleep-scratch folder:
- Undarkened: public_proxima_v05/026_proxima_undarkened_v05.mp4, SHA-256 ae5c675a2414209e2f114f20487a583f0878cbab9c79fdfd65761c8b39b2ba63.
- Darkened: public_proxima_dark_v01/026_proxima_darkened_v01.mp4, SHA-256 7eb93f84b40190bb944208e396e5ce9ccc2e77c28c3f00de8aa8b6bc24752ddd.
- 14,142 decoded frames; 471.4 seconds. Source master and clean narration hashes match their existing checked records. Narration remains unchanged, measured -20.72 LUFS / -6.54 dBTP, LRA 3.0 LU. The final continuous bed and full-film sound checks remain owed.

The finished film is cut at the existing narration boundaries. The two Orbit scenes use the plan's available ESO NGC 6752 and Hubble Omega Centauri alternatives, with hashes and credits in PROXIMA_PLATE_INPUTS.json. Cards use neighbouring finished-master picture. A repeated chart donor and a wrong-subject nebula donor were rejected, with candidates preserved. A local exposure correction fixes new near-black failures around the final card, with smooth one-second ramps. Source charts and teaching labels remain under Chief's version-one scope.

Full undarkened pixel scan completed. All 13 remaining findings are outside new edit neighbourhoods and recorded as 'in the public film'; no changed-window failure was waived. Fresh edit picture QA PASS: 190 samples, zero failures, 13 advisories. Cover-edge and advisory sheets were inspected as stills; no playback or listening claim. Native saved-pixel grade passes: same frames and duration; overall brightness 84.9864%; all 235 two-second windows 84.9429–84.9943% against unchanged 83–87% limits. Five brightest windows are 434–436, 420–422, 180–182, 418–420 and 432–434 seconds, with one saved frame each. Their sheet was inspected.

## Delivery and next wake

Destination relative to the working film store:
`_sleep_video_01/j2452/public_chapters_v01/026_proxima_v01/026_proxima_darkened_v01.mp4`.

The save process has a bounded time budget this wake. Until NAS_COPY.json exists and CHAPTER.json is read back, a destination file is only a copy checkpoint, not a delivered chapter. Existing destination bytes are never overwritten or deleted. The helper verifies the complete existing prefix before appending, then hashes the complete destination before writing the chapter record.

Resume with the existing J2452-asr312 Python environment and `jobs/reviews/J2452/save_public_proxima.py` if delivery remains pending. No re-render or repeated pixel scan is required for the locally verified file. Helpers contain the exact local and NAS paths; public evidence is film-relative. Record 12/15 only after destination SHA-256 verification, then release at the chapter boundary. Next chapter is 019 Andromeda; after it remain the continuous bed/mix and all final sound, CTA, silence and join checks, master/reel copies and Ben's watch card. Earliest air date remains 12 December. No upload, Studio change, generation, spend or deletion.

All launched processes must exit before release; restore OWB main, leave HOS untouched. Thread read to #6806397802.
