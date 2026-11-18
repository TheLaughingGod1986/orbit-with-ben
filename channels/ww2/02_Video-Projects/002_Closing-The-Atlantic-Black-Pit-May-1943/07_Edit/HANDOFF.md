# J2996 — edit preparation, 18 November 2026

This is an unfinished film. No full-film QA, picture PASS, audio perception, motion review, or Ben-watch submission is claimed.

## Delivered

- `EDL_v01.json`: all 247 sentence picture rows timed against delivered Scribe words. Audio SHA-256 matches J2995's delivered WAV. Exact matching tokens anchor each sentence. Nine incomplete sentence boundaries carry `boundary_review: true`; check those before final assembly. Cut intervals are contiguous, positive and unique. Final two seconds are an intended end hold, not extra speech.
- `ARCHIVE_HARVEST.json`: three actual downloaded files with hashes and pixel sizes; two unresolved links. Catalogue snapshots and image files are on NAS only. P1/P2 are the published 1280-pixel Wikimedia derivatives because originals returned 429; do not describe these as full-resolution originals. P4 is only 800×519 and must remain an inset.
- P1 (CH 18035) is the Aldergrove Liberator lineup, P2 (CH 18031) an armourer cleaning the turret, and P4 (80-G-71314) Bogue in June 1943. Catalogue descriptions, dates and public-domain/Crown-expiry notices checked. Contact sheet inspected as a still: no graphic violence. Captions must preserve dates; none is an action photo of a named convoy.
- `opening_map.py`: Natural Earth public-domain coastline base and an animated opening schematic. The shore aircraft turns back at the 9.92-second spoken sentence; escort symbols remain with the convoy. The picture is labelled schematic, with no exact historical route, range radius or ship-count claim.
- Opening draft on NAS: `03_Picture/maps/M001/opening_with_vo_DRAFT_v01.mp4`, 1920×1080, H.264, 25 fps, AAC, 21.60 seconds including the first four sentences. Full ffmpeg decode passed. There is no music in this draft. Map stills inspected; motion/audio not perceived.
- `archive_previews.py`: archive inspection sheet, no-text archive thumbnail A candidate and 168-pixel phone image. Candidate inspected at full size: visible Liberator nose, wing and lineup, normal monochrome grade. Still a candidate, no final packaging approval.
- `11_Upload-Package`: incomplete draft metadata, six chapters timed from actual narration, 2,359-character description including six source references, image credits and how-made line. No upload manifest or upload job.

## Media and tools

Media root: `/Volumes/data/studio-live/ww2/02_Video-Projects/002_Closing-The-Atlantic-Black-Pit-May-1943/`.

Run the Python scripts with `/opt/homebrew/opt/python@3.14/bin/python3.14` (Pillow installed there; the worktree's default Python differs). Each script has `--help`. `prepare_edit.py --media <root>` rebuilds timing without making network requests; `--harvest` explicitly retries downloads.

The initial tmux attempt failed because the existing tmux server could not write the NAS. A direct permitted run finished successfully. `~/_desk/logs/j2996/opening.done` is **0**; `opening.log` has the output. No render remains running. Do not treat the old tmux failure as an unfinished render.

## Next actions in this same job

1. Recover P3 / 80-G-86005 and P5 / 19-N-50553 from an authoritative alternate distribution; both supplied Navy catalogue URLs returned 404 through curl. Do not retry the unchanged links indefinitely. P5 does not occur in the current shot rows: omit from the final used-image credits unless actually used. The line-specific map alternatives may replace an unavailable contextual photograph without changing narration.
2. Render the remaining 57 paragraph map briefs and sentence states with real geographic/tactical content. Do not reuse the opening as generic filler. Verify submarine/radar/HF-DF mechanisms and the ONS5 fog / SC130 distinctions against their exact spoken lines. Inspect all rendered states.
3. Resolve the nine EDL boundary flags, chapter pauses and full-film edit timing; VO words stay locked. Use slow moves on archive photographs within their actual resolution.
4. Select a properly licensed WW2-specific music bed within the £0 brief. No OWB/HOS media reuse. Do not generate music or spend credits without a separately checked authorised route and live subscription preflight.
5. Assemble the full 1080p film, finish thumbnail B (LIBERATOR), adapt applicable studio technical QA to this new channel's rules, and make one quality pass. Ben's finished-cut watch covers the actual watch/listen input this session cannot perceive. Do not import OWB/HOS aesthetic gates that contradict WW2 rules.
6. Only after the full cut and checks are ready, put it on Ben's board for his watch. No upload or schedule; channel remains prelaunch.

PR #1014 is still OPEN: its voice report is a worker submission, not a recorded voice-stage Chief PASS. Before final delivery inspect the actual voice records and reconcile that review/status. J3031 already locked the exact script. No additional claims-check run was started here.
