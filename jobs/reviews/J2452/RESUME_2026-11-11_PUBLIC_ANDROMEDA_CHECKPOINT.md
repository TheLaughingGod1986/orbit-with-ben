# J2452 — Andromeda local picture checkpoint

Worker macbook-2. Overall progress remains 12/15. Not UAT-ready; no NAS delivery or darkening this run.

Current candidate: `/Users/ben/_desk/J2452-sleep-scratch/public_andromeda_v05/019_andromeda_undarkened_v03.mp4`.
BUILD.json records its hash, exact slices, cover fallbacks and expected 18,145 frames / 604.833333 seconds. Container probe reports 18,145 frames and 604.833 seconds. A complete decoded frame count remains owed; do not treat the container count as a decode pass.

The v03 candidate was rejected despite automated edit QA PASS: visual review caught three outgoing Orbit ghosts, and full decode found two missing frames. v04 holds three outgoing tails on their preceding clean frame. v05 restores one frame at each of two short boundaries, where floating-point rounding had left a one-frame gap; no narration moved. Previous candidates retained. Builder rounding was corrected for future reruns.

Fresh v05 picture_qa PASS, no failed edit check waived. Advisory review sheet and exact cover-edge sheet inspected; no Orbit/card ghosts in those samples. Full pixel scan reports eight findings, all outside compilation edit neighbourhoods; listed as “in the public film” under the Chief ruling, with separate classification evidence. Charts/labels retained. This is still-sheet review, not full-speed playback or a listening pass.

Stopped the remaining read-back deliberately at the bounded run checkpoint after both gates finished. No READBACK.json produced: full decoded frame count, current loudness/peak and brightness scan still owed. Resume `check_public_andromeda.py --out /Users/ben/_desk/J2452-sleep-scratch/public_andromeda_v05` after preserving or using a new name for its existing gate reports; its final bright stills do not yet exist. Then inspect results, darken with darken_public_andromeda.py, measure all brightness windows, inspect brightest stills, and save via save_public_andromeda.py. Darkening helper points to v05. Do not set 13/15 until NAS copy hash read-back succeeds.

Then final single-bed assembly, whole-film sound/CTA/silence/join checks, master/reel copies and Ben watch card. No upload, Studio, login, generation, spend or NAS deletion. Python compilation, 13 privacy checks and diff check passed. Thread read to #6807472538.
