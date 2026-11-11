# Andromeda full decode and graded render checkpoint

Worker macbook. Progress remains 12/15; no NAS delivery and no UAT claim.

Fresh undarkened read-back completed: 18,145 decoded frames, 604.833 seconds, new-edit picture QA PASS. Eight pixel findings are in untouched public-film stretches. Narration -20.86 LUFS integrated, -9.41 dBTP. Cover-edge sheet re-inspected; no outgoing Orbit or chapter-card ghosts in sampled edges. This is still inspection, not full-speed playback or listening.

Native spatial grade uses the tested preceding-chapter method: exact LUT with spatial rounding, lossless H.264, narration copied. Local file is in the job scratch public_andromeda_dark_v01 folder, named 019_andromeda_darkened_v01.mp4. Render complete: 18,145 frames, SHA-256 749400c5ced259fa02dcf74f7e6019af67a9227ad2503a2385472caf7bd0adc1. File is about 12 GB. Graded output needs completed native measurement before delivery; do not rerender over it.

Resume darken_public_andromeda.py --verify-existing if DARKEN_READBACK.json is absent, then inspect the brightest-window sheet. Only after every two-second brightness measurement, duration and decoded frame count pass, save additively with save_public_andromeda.py and verify destination hashes. Allow enough time for the 12 GB copy and full destination read-back; do not mark 13/15 before CHAPTER.json and matching hashes exist.

Final continuous-bed assembly, full-film sound/CTA/silence/joins checks, master/reel copies and Ben watch card remain. PR #789 stays open; no merge. No upload, Studio, login, generation, spend or NAS deletion.
