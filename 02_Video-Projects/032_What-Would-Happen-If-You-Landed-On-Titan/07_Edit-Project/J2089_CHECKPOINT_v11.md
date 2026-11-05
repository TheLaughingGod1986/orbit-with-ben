# J2089 checkpoint v11

5 November 2026 · Codex worker · original partial 1/4 · GBP0.

Implemented the standard qtrle export for J2251-approved r52_uranus_21y,
without changing the reviewed frame function. Source and preview SHA-256 must
match the reviewed manifest before rendering; absent approval is rejected.
Use the existing house graphics environment:
`/Users/benjaminoats/_desk/venv-graphics/bin/python` (Pillow 12.3.0).
The temporary older-job environment has Pillow 13.0.0 and changed preview pixels;
the guard caught this before any MOV was written. Its v03 preview is unused.

Export: `/Users/benjaminoats/_desk/cache/J2089/uranus_renders_v04/code_graphic_032_r52_uranus_21y_v01.mov`.
URANUS_RENDER_MANIFEST_v01.json records hash, approval and compositing constraints.
URANUS_RENDER_CHECKS_v01.json verifies source/preview/render hashes, qtrle ARGB,
1920x1080, 30fps, 3.6s, 108 frames, full decode and exact RGBA equality of every
frame to the reviewed generator. Original 109 frame-layout/alpha checks rerun.
No audio or moving-image judgement is claimed. Final composites remain unverified.

J2251 scope: duration-only CODE graphic; no invented tilt-axis line on PIA18182.
Use PIA18182 once in R52, inside this graphic only. Earlier R52 cuts show sideways
tilt using weic2310a with INFRARED VIEW disclosure. Composite over reviewed graded
moving real imagery, then verify contrast/placement/reuse and final film gates.

Preserve 38 previous exports. J2177 and J2247 reviews, frame0 compliant native
motion, Huygens PIA07232 reuse and APL Dragonfly rights holds remain unchanged.
Licensed harvest, remaining real-body graphics and composites exceed this run.
No background process, spend, generation, publishing, locked script/VO changes,
film PASS, final OK or merge. NAS offload correctly deferred to 01:00–06:00
because disk free is 13.8GB, above the 8GB emergency exception.
