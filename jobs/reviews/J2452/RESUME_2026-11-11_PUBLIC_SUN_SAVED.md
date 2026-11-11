# J2452 — Sun saved, 11 November 2026

Worker macbook. Progress **8 of 15**; next chapter **028 Gliese 710**. One chapter finished this run; compilation is not UAT-ready. PR #789, branch macbook/J2452.

Sun undarkened v03 is unchanged, including the checked narration (−20.73 LUFS / −6.55 dBTP), existing new-edit QA PASS (144 samples, zero failures), and the 41 untouched source-film pixel findings recorded under the Chief's ruling. No new source pictures, downloads or generation. Prior rejected candidates remain.

## Brightness diagnosis and delivery

The implicit YUV-to-gray conversion gave misleading ratios in dark Sun windows. At 442 seconds the same round8 candidate measures 79.61% through implicit grayscale but 84.92% with explicitly extracted legal-range Y. The diagnostic and all new short-probe results are retained. Brightness now measures decoded Y directly, subtracting legal black 16 and clipping below black to zero, with area downsampling at 4 fps. This is an explicit luma measurement, not a changed tolerance. Grade scales legal-range luma by 0.85 and chroma about its neutral point by 0.85. Previous probes and failures are not rewritten.

New file: local public_sun_dark_v02/022_sun_darkened_v02.mp4. Full decode before and after: **14,410 frames**, **480.333333 seconds**; duration unchanged. Overall luma ratio **85.1789%**. All **240** complete two-second windows pass **83–87%**, actual range **83.4985–85.8113%**. Five brightest windows: 290–292, 454–456, 288–290, 452–454, 250–252 seconds. Their five extracted frames and sheet exist locally; the sheet was inspected as stills, showing Earth/cloud views. No playback or listening claim.

NAS: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01/j2452/public_chapters_v01/022_sun_v01/022_sun_darkened_v02.mp4`

SHA-256: `441ef23503e1e1895053c1fd1c2c122d1b0b6e77b46e7791dcf2f7cc0558fbbb`. Destination read-back matches all 192,871,571 bytes. CHAPTER.json and BRIGHTEST_WINDOWS.jpg saved beside it; NAS_COPY.json records hashes. Nothing replaced or deleted.

Python compilation, 13 repository privacy tests and diff check pass. Five picture chapters remain (028, 029, 024, 026, 019), then shared bed/final assembly and whole-film loudness/peak/silence/CTA/join checks, reel, final copies and Ben's watch card. No upload, Studio, login or spend. All launched processes ended. OWB returned to main; HOS untouched. Thread read to #6802366813 (read succeeded; writing the home state file was denied).
