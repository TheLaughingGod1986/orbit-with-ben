# Earth darkening checkpoint — 11 November 2026

Worker macbook. Progress stays **2 of 15**. Earth is not delivered; no NAS write, compilation master, reel or UAT.

Reviewed the 17 advisory stills from the undarkened v04 candidate; see EARTH_ADVISORY_REVIEW_2026-11-11.md. Changed-window picture QA retains zero failures. The public-film inherited findings remain listed, with no waiver.

The original per-pixel grade was too slow and its exact encoder was stopped with SIGINT. Its partial output remains in local public_earth_dark_v01. A faster FFmpeg eq per-frame lookup-table grade completed in public_earth_dark_v02, but actual post-20:30 brightness measured 0.8283394875783264, below the required 0.83–0.87. A one-code-value offset correction in public_earth_dark_v03 also completed, but measured 0.828339590290531. Neither passed. No threshold was changed and neither candidate was copied. Both full scans reached the expected 13,141 frames; duration is 438.033333 seconds. Failed assertion logs remain beside the local version directories.

The helper currently names v03, which already exists and FAILED. Do not rerun over it or use save_public_earth.py on it. Next worker must diagnose why the dynamic eq brightness correction did not change the measured ratio, validate the actual time-varying grade on short probes, then choose a new output version and run the full checks. Avoid another full encode until those probes demonstrate the correction. The NAS-save helper additionally requires every measured two-second window to pass.

Local scratch: /Users/ben/_desk/J2452-sleep-scratch/. Verified undarkened source remains public_earth_v04/027_earth_undarkened_v04.mp4, SHA-256 6eb3c0fb72cd10f1b6ff4afa5fbd9be8a654810b9534d69f1e5ea596e689a819.

All launched encodes and checks ended. Python compilation, all 12 privacy tests and diff check pass. No upload, Studio action, sign-in or spend. Full compilation, bed, sound/joins, reel, remaining chapters and Ben watch remain owed.

Thread read to #6797008820 (displayed trusted messages; home-directory checkpoint write denied).
