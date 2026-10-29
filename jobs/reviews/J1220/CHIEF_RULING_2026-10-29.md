# J1220 acting-Chief review — 29 Oct 2026

Reviewer: codex, elected Chief confirmed with chief_relay.py status.

## Ruling: FIX; no v07 PASS or card repoint

Ben requested a steady opening, not merely passing the existing numerical gates. The supplied v07 evidence does not establish that this request is resolved. Authorize one no-spend v08 correction through the assembly queue, preserving the existing fallback and deadline. J1212 stays blocked on Ben's approval; v07 is not approved for upload.

## Evidence checked

- Read J1220 and J1212 bodies, results and full histories, Ben's quoted request #264 6507250708, and J1204 v05 ruling/v06 delivery.
- Independently hashed NAS v06: f0b4e0a0318f99ecbe38cdcb0525c8f869fba609d55194da75de45cb579b3ee5; NAS v07: 21dda9ab1c636c70678404ebd8c0d2d82e8f20af20bec3ae427483d2bf51e609. Both match the worker records.
- Read all supplied final-sha reports: open, loop, polish, picture, music, SFX PASS. Worker reports I -14.30 LUFS / TP -1.80 dBTP. These are supplied gate results, not fresh reruns. Existing 18 s test duration and tail-gap warnings do not decide this review.
- Compared all 90 decoded frames at 30 fps over 0:00-0:03 for both versions, plus supplied contact strip. v07 changes framing and drift; still sheets alone do not establish steady playback. No claim of a normal-speed audiovisual watch is made.
- Code inspection: `_assemble_uranus_v07.py` lines 330-334 accumulate `-kill * mean_dx/dy`, a constant correction each frame. The measured individual steps are not used to smooth the path. `_smooth_path` is defined but unused by this implementation. Constant velocity correction cannot remove varying shake.
- Independent phase-correlation diagnostic on the decoded subject ROI (Hann window, excluding captions): vertical adjacent-shift standard deviation 1.46 px in v06 vs 2.81 px in v07; adjacent-shift-change RMS 0.64 vs 3.90 px. Horizontal shift-change RMS 0 vs 1.31 px. These are limited integer-resolution ROI estimates, affected by image content/crop, not a new gate; they provide no evidence of improved steadiness. Full method and arrays in CHIEF_MOTION_DIAGNOSTIC.json and measure_open_motion.py.
- v07 crop zoom 1.1285 means effective source upscale about 2.01x, rather than the inherited 1.778x. Correct QA provenance on the next render.
- Actual iCloud v06 and v07 master reads both failed with OSError 11 Resource deadlock avoided. NAS masters are readable. An existing pathname/manifest is not proof of a playable UAT delivery.

## Follow-up

Queue an assembly correction with actual measured-path stabilization (or a demonstrably steadier approved source window), verify transform signs, preserve intended moving subject footage, unchanged VO/edit, and forward loop. Require full final-sha gates and verified readable iCloud/NAS delivery before Chief review. No gate thresholds waived.

J1212 remains held. No YouTube/Buffer/UPLOADS changes. Do not repoint Ben's card to v07. Preserve Ben's Tue 3 Nov 10:30 London watch deadline, 11:30 airing, and v01 fallback; prior unsuccessful-branch cutoff 1 Nov 18:00Z remains.

Full-frame contact sheets are retained outside git at /Users/benjaminoats/_desk/reviews/J1220/v06_allframes_0.jpg through _2.jpg and v07_allframes_0.jpg through _2.jpg. No media committed. Review progress uses chief_relay review steps, not the worker's 4/5 steps.
