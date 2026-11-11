# J2452 — bounded Betelgeuse shadow-grade investigation

Worker macbook. Branch macbook/J2452; existing PR #789. Compilation remains incomplete, with no final master, reel, NAS delivery or UAT claim. Existing thirteen narration chapters, 108:22.36 continuous audio and thumbnail are unchanged.

## What this continuation did

Tested three separate full-chapter grades against the six near-black failures in the saved 029 picture. Every treatment covers the entire mapped shot, preserves chapter timing, keeps the Y=180 highlight limiter, and uses the existing unchanged polish gate. Original media remains untouched.

- v02 gamma/brightness: rejected on comparison stills because the black backgrounds become grey and the surface looks washed out.
- v03 RGB curve: rejected because it shifts colours and accentuates chroma/compression structure in the Chajnantor sky.
- v04 luminance-only transfer: preserves chroma and reduces the colour-shift problem, but comparison stills still show lifted backgrounds and baked text. It is an **unapproved diagnostic candidate**, not a finished sleep-picture treatment. Do not adopt it on gate metrics alone.

All three local directories remain under `/Users/ben/_desk/J2452-sleep-scratch/betelgeuse_shadow_grade_v0N/`. Their reports, unchanged gate outcomes and read-back checks are kept beside this note. No further grade iteration was started. `grade_betelgeuse_checkpoint.py` reproduces v04 into a new directory and refuses overwrite. Its source checksum is pinned.

## Remaining work and concrete next action

The preceding 0510 resume note remains the baseline picture checkpoint. Retain the telescope gutter failure at chapter 435.79 s: the inspected still shows the telescope against the sky, but no worker override or threshold change was applied.

For the six dark spans, work from the film's original full-resolution photo/video assets and actual source framing/grade, rather than repeatedly grading the compressed checkpoint. Resolve the baked labels at the same time; the sleep plan permits only quiet chapter names. Check all replacement intervals against the locked narration and preserve source identity/provenance. Record the exact source interval, crop, scale and original/used cut times, then rerun saved-file checks and the normal gates. The current three diagnostic attempts belong to this input's history; a restart is not a reason to repeat them.

Beyond these findings: the 22 original code rows, source reuse, original scene dissolves, chapter name and inter-film breath remain unfinished. Twelve other picture chapters, initial darkening ramp, full assembly/mux, all CTA/audio/picture/join gates, NAS master and roughly 12-minute reel with independent hashes, and Ben's finished-film watch remain. Earliest air date remains 12 December. No upload, Studio change, generation, money/credit spend or NAS modification.

Release at this clean point because full assembly exceeds this unattended run. All launched builds/checks must exit before release and the checkout must return to main.

## Saved v04 evidence

Local picture: `/Users/ben/_desk/J2452-sleep-scratch/betelgeuse_shadow_grade_v04/029_picture_shadow_grade_v04.mp4`

SHA-256: `de8459b3dc18890e95813832260f80b70bf48f7722418953192ae2ac4eda4e0a`. Full decode passes; 14,829 frames on the constant 30 fps clock, 494.3 seconds. Both opaque cover checks pass the fixed error threshold 2: maxima 1.0008, 1.2356.

Normal polish verdict: **FAIL**, 1 failed rows and 5 warnings across 78 mapped rows. Failures: [{"row": "36", "cut": 69, "t": 435.79, "source": "orion_over_paranal.mp4", "why": ["split panel: vertical gutter at 0.826"]}]. No reviewed-ok override or threshold change. This remains a diagnostic checkpoint, not finished picture QA or AV delivery.
