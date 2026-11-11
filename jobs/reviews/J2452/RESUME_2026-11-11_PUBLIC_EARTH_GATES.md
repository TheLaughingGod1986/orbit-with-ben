# J2452 — Earth Spin undarkened gates checked

Worker macbook, 11 November 2026. Progress stays **2 of 15**: Earth is not yet darkened or delivered. Full compilation, reel and UAT remain incomplete.

## Resume from this candidate

`/Users/ben/_desk/J2452-sleep-scratch/public_earth_v04/027_earth_undarkened_v04.mp4`

SHA-256: `6eb3c0fb72cd10f1b6ff4afa5fbd9be8a654810b9534d69f1e5ea596e689a819`.
Full decode exits 0 with **13,141 frames**, exactly the expected count. Duration 438.033333 seconds; prior narration/cut clock retained. Encoded narration measures **−20.73 LUFS**, **−6.50 dBTP**. Final continuous bed and whole-film sound checks are still owed.

The prior three near-black edit failures are repaired using master 54–57 seconds (daylight ISS Earth), slowed across chapter 57–66 seconds with one-second dissolves. The source interval was inspected at one-second spacing. This is the same film's neighboring master picture under the existing Chief fallback; no fresh source search or generation. The chapter quiet title was restored over the repaired opening. Encoded title frame at 3 seconds and the 55–68-second entry sheet were visually inspected. This is still inspection, not moving-picture/listening approval.

## Gates

- Full undarkened polish check completes, retaining FAIL with **12 findings**, all classified **in the public film** outside compilation edit windows and their two-second margins. No threshold or finding waived.
- Changed-window picture QA **PASS: 0 of 248 cuts fail**, **17 advisory samples** for review. The three previous near-black failures are gone.
- Complete build, cut list, pixel report, join report and read-back are in `public_earth_v04/` beside this note. Local review sheets remain in scratch; no media is committed.

## Next action

Use `/Users/ben/_desk/J2141-venv/bin/python jobs/reviews/J2452/darken_public_earth.py` only after verifying the preserved v04 hash and review evidence. The helper now points at v04 and keeps its gate/title guards. It applies the compilation 19:30–20:30 ramp and must finish the actual frame-count, duration, every-two-second brightness-ratio and brightest-window measurements. Then use `save_public_earth.py` for an additive NAS save with destination SHA-256 read-back. Neither helper ran in this wake. Inspect the 17 advisory samples before final delivery.

The run stopped at this checked point rather than starting another encode that could overrun its 25-minute limit. No NAS writes, upload, Studio change, sign-in or spend. Previous outputs retained. Public charts and labels remain; dissolves only on compilation edits. All launched processes ended.

Thread read to #6796521998.
