# J1240 elected Chief review — 30 October 2026

Reviewer: codex, elected acting Chief; authority rechecked with chief_relay.py status.

## Ruling: FIX, not PASS

Reviewed the job body/result/history, J1225 motion evidence, v09 delivery note, renderer, final-sha gate records, full opening contact sheet and full-size 0.40s frame. This is an implementation/evidence ruling; no claim of real-time audiovisual playback. The existing reported gate PASSes are retained, not overridden. No final OK or Ben-watch handoff.

Independently read and SHA-256 checked the actual iCloud and NAS masters: both match `458b1f67d08c567166b49e416fa3e8fefaec7c1a6cce8c3303305b853f8a3535`.

## Why another correction is necessary

1. `_assemble_uranus_v09.py` sample_open (lines 445–458) crossfades two displaced source frames. It does not spatially align them before interpolation. Its three shutter samples (lines 476–495) are averages of those same unaligned frames. This is temporal blending, not the requested sub-pixel resampling of moving detail. A nominal 1.5 px path does not establish actual ring motion; ghosting/shimmer remains a risk on these thin arcs.
2. The renderer assumes exactly 4 px per source interval (lines 394–398) and reports the designed source-time curve as pixel motion. It neither measures that mapping nor includes the final zoom in those reported steps. Delivered measurements disagree: v09 peak step 3.0 px and maximum step change 3.0 px, against requested 1.5 / 0.25. These are corroboration, not newly invented gates, and could include estimator error; that disagreement must be resolved before PASS.
3. The estimator uses a 2x image resize plus integer FFT peak: resolution is 0.5 px, too coarse to validate 0.25 px step changes. Flicker falls 3.19777 -> 2.75916 (13.7%), and step-change max 4 -> 3, but this alone cannot prove the requested path. Committed MOTION_DIAGNOSTIC.json contains summaries only, with no per-frame steps for any version.
4. The opening ends at a designed 0.70 px/frame rather than rest. Avoiding a gate-detected freeze is sensible, but this departure from the brief must be explicit. Chief clarification for the correction: retain a gentle continuously moving ease-out through the cut if reaching rest would violate the existing no-freeze gate; never weaken that gate.

## Authorized follow-up (assembly; GBP0)

Create a new v10, preserving v06/v07/v08/v09 and every uploaded file. Same approved NASA SVS 20390 Shot9, v06 narration, captions and timing. Prototype only the opening first: measure source motion; use motion-compensated temporal interpolation or a measured spatial sub-pixel warp of successive moving source frames. Do not crossfade unregistered displaced frames, use static/frozen replacement footage, or claim designed motion as measured motion. Use high-quality spatial resampling and 2–4 genuinely displaced shutter sub-samples; account for final crop/zoom and retain upscale <=1.85.

Validate the estimator on known synthetic fractional translations and ramps, at <=0.1 px resolution, before using it on the caption-free subject ROI. Supply full per-frame steps, step changes, confidence/ambiguity diagnostics, acceleration RMS and motion-compensated ring flicker for v06/v08/v09/v10. Investigate unreliable ROI estimates rather than silently treating them as compliance. Keep the existing requested slow path and step-change targets. Preserve every original gate. Inspect every opening frame and normal/quarter-speed playback; save the evidence and state who or what actually performed each inspection.

Only after the prototype demonstrates improvement should the worker render the full version and rerun the existing final-sha gate set (open/f0diff, loop/all finish, I/TP, polish, picture QA, music, SFX, hitch). Tail changes only for a documented forward loop, with no obvious double rings. Versioned repo-local/NAS/iCloud delivery, hashes and playable source check; no media committed to git. Park for elected-Chief review, not worker PASS. Deadline 1 November 20:00 London; if no compliant cut, explicitly report unsuccessful and preserve fallback. Ben watch deadline remains 3 November 10:30 London.

J1212 is untouched and remains held on Ben approval. No repoint, upload, scheduling, privacy, Buffer or UPLOADS mutation. Scheduled fallback ZpEA8stoSPA remains as is. No external wait is needed: correction is ready for the assembly lane.

Disk: required NAS offload was attempted with access available; no scratch met the safe 48-hour age threshold. About 13 GB free. No render started during this review.
