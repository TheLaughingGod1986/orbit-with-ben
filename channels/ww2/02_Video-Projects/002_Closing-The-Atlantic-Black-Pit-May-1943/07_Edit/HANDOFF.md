# J2996 picture-polish continuation — 18 November 2026 17:08 UTC

Progress remains **2/5**. A separate full-film footer-cleanup render is running; no music, perceptual QA, approval or Ben-watch delivery is claimed.

- `polish_footer.py` verifies the full v01 source hash and creates **07_Edit/picture_polish_v02/atlantic_picture_polish_DRAFT_v02.mp4** on the same NAS film root. It removes internal sentence IDs/production footers below y=990 from 21.60 seconds onward using the existing paper colour. The opening, schematic caveats, diagram content and archive rights captions remain. Original draft and source clips are retained. Still sample at 30s inspected: footer removal and retained caveat confirmed; existing low-contrast carrier label remains an editorial issue for finishing.
- Detached session **j2996-polish-v02**. Log: `/Users/benjaminoats/_desk/logs/j2996/picture-polish-v02.log`. Completion marker: same folder **picture-polish-v02.done**. Runner: **run-polish-v02.sh**. Missing marker means still running: do not start a duplicate. If marker is 0, inspect `TECHNICAL_CHECK.json` in the new output folder. If nonzero, read the log before resuming; the script refuses to overwrite any existing render.
- Completion checks built into the runner: complete decode, 36,076 frames, 1080p25, full output hash, and unchanged encoded AAC audio-packet hash. No measurements are a watch/listen approval. Copy successful technical evidence into git next run, after inspecting still samples across archive/map sections.
- Voice review **PR #1014 is still OPEN** as checked this session. No voice PASS inferred. Draft edit PR #1018 also remains open.
- Session tool inspection demonstrated no audio_input or moving_video_input. Full perceptual review will need a worker with demonstrated inputs; continue independent music/package/editorial work first. No credits spent, media reused, upload or account change.

Next: check this render, finish original/licensed film-specific music and sound, fix remaining label/pacing issues, reconcile the voice review, complete one capable quality pass and package, then send the finished cut to Ben. The picture-polish version remains a silent-bed editorial draft with narration only.

---

# J2996 resume checkpoint — 18 November 2026, full editorial draft

This checkpoint supersedes the incomplete picture counts below. **Unfinished editorial draft; no music, full watch/listen QA, Chief PASS or Ben-watch submission.** Progress is 2/5: picture coverage complete, full-film finishing still needed.

## Delivered this run

- Added **169 sentence clips** across the remaining 39 paragraph briefs. Total: **243 sentence clips plus the four-sentence opening = all 247 sentences / 58 paragraphs**. Eight sequence manifests, source clip hashes, exact locked narration and v01 timings cross-checked. No missing sentence or duplicate output path.
- Full editorial draft: `07_Edit/full_draft_v01/atlantic_full_editorial_DRAFT_v01.mp4` under the NAS film root. **1443.04 seconds (24:03.04), 36,076 frames, 1920×1080, 25 fps, H.264/AAC.** Full ffmpeg decode and counted-frame ffprobe checks succeed. SHA256: `f060fb652acd8d26b69e092bbb1f0026cd715899a4fe7c027d043544c43a3941`. Entire original WAV muxed once, unchanged; two-second end hold. There is **no music**.
- `FULL_DRAFT_v01.json` records full-draft hash, EDL hash, source voice hash and all final picture paths/hashes/frame counts. `PICTURE_BUILD_v01.json` checks the eight source sequences. All media remains on NAS; no media committed.
- `EDL_v02.json` and `TIMING_CONFORM_v02.json`: all nine lexical boundary flags traced to Scribe acronym/digit formatting or US spelling (HX229, SC122, 1943, ONS5, SC130, defense/defence, organization/organisation, center/centre). Word timestamps inspected directly; cuts recomputed in inter-sentence gaps. Fifteen picture rows conformed by trimming/padding final picture frames. This is transcript/timing verification, **not hearing the take** or approving speech content. v01 retained for source clip manifests.
- P1 / P2 archive treatments show real Aldergrove photographs at reduced size with collection, date and rights captions. P4 / Bogue is a native 800×519 inset explicitly dated Norfolk, 20 June 1943. P3 remains unavailable: its existing sentence-specific map alternatives are used, no repeated retry. Recovered P5 is retained but unused. Description credits now match actual usage.
- Still contact sheets inspected for each new batch, plus full-size archive, command diagram and engineering panel checks. Four L010 frames were rebuilt after inspection caught a label/icon overlap; replacements are under `03_Picture/maps/early_layout_fixes_v01/`. The final assembler checks and uses them. Reused archive picture IDs now get **unique sentence-based output paths**, preventing captions from overwriting one another.
- Nine decoded full-draft still samples inspected; retained as `07_Edit/full_draft_v01/STILL_SAMPLE_CONTACT.jpg`. This is still-image evidence only. No claim to hearing audio or perceiving motion.
- Draft title, chapters, sources, actual archive credits, tags and honest AI-assisted narration how-made line updated in `11_Upload-Package`. It remains explicitly non-uploadable.

## Resume without rerendering unchanged work

NAS root: `/Volumes/data/studio-live/ww2/02_Video-Projects/002_Closing-The-Atlantic-Black-Pit-May-1943/`.
Worktree: `/Volumes/MiniWork/scratch/j2996-atlantic-edit`, branch `codex/j2996-atlantic-edit`, draft PR #1018.
All six new sequence jobs and the full draft are **complete**, no render remains running. Completion markers under `/Users/benjaminoats/_desk/logs/j2996/`: `early-v01.done`, `geography-v01.done`, `aircraft-v01.done`, `synthesis-v01.done`, `carrier-v01.done`, `ending-v01.done`, `full-draft-v01.done` are all **0**. Matching `.log` files retain the actual run output. Existing detection/convoy/opening batches remain complete.

New renderers: `early_maps.py`, `geography_maps.py`, `aircraft_maps.py`, `bridge_maps.py` with `synthesis_maps.py` and `carrier_maps.py`, `ending_maps.py`. `assemble_full_draft.py` checks all source hashes/timings, applies the four layout overrides and v02 picture lengths, then muxes the full voice and decodes/counts the result. Python: `/opt/homebrew/opt/python@3.14/bin/python3.14`.

## Remaining work in this same job

1. **Polish picture/editorial treatment.** The cut is diagram-heavy by its signed shot plan. Review pacing and comprehension at full size; replace/reposition any small labels that cross coastlines, standardise the opening with the later map style, and remove sentence/file debug IDs from the final film. Camera moves and layer timing require actual motion perception; frozen end-frame conforms are draft treatments. Do not infer exact historical positions or numeric coverage from schematic geometry.
2. **Film-specific music and sound.** Select/create a licensed score within the £0 brief. No OWB/HOS media reuse, paid API, credit top-up or unapproved generation. No music has been selected or approved by this run.
3. **Capable quality pass.** Run applicable technical gates against the finished mix, then a real full watch/listen with a worker whose input capabilities are demonstrated. This session has no audio_input or moving_video_input. Record typed capability holds if that input blocks the next assigned step; do not turn still sampling or decode success into perceptual PASS.
4. Reconcile actual VO review/status and finish package; do not change locked narration. Review references below are historical until checked against current records.
5. Elected Chief decides ordinary final review under channel rules, then deliver the **finished** cut to Ben's board for watch. No upload until that watch passes; verification/account eligibility is checked only in a later authorised upload job. No money, account changes or upload performed here.

---

# J2996 resume checkpoint — 18 November 2026, second run

This checkpoint supersedes the counts and P5 status in the initial preparation note below. The film is unfinished. No full-film QA, audio/motion perception, Chief approval or Ben-watch submission.

## This run delivered

- **74 sentence clips across 18 paragraph briefs**: L030–L038 detection mechanisms and L040–L048 ONS 5 / SC 130 comparison. Together **437.04 seconds**, 10,926 frames at 1920×1080, 25 fps. Each row has its own video, still, exact locked narration, frame count and hash. Both narrated sequences decode fully; source WAV hash matches the EDL. `PICTURE_BUILD_v01.json` records checked media hashes, timing coverage and outstanding work.
- Detection draft: `03_Picture/maps/detection_v01/detection_with_vo_DRAFT_v01.mp4`, source time **746.40–960.00 s**, duration **213.60 s**, SHA256 `550c345abc5dbb7ead117224b3c74e59b20228d8db436adf770ea72e038c212f`.
- Convoy comparison draft: `03_Picture/maps/convoys_v01/convoys_v01_with_vo_DRAFT_v01.mp4`, source time **986.88–1210.32 s**, duration **223.44 s**, SHA256 `938a937f3e9a4308a1e67ae7c39f5e5fe9e5cf57b590b0e007c0cd05683d7980`.
- Geometry is explicitly schematic. Earlier radar/Metox is separate from centimetric radar; HF/DF has no Allied transmitted pulse; bearings are directions/areas, not exact positions; sonar is below water. ONS 5 fog operations show surface radar, with air operations limited. SC 130's eight sightings appear as a boxed observation counter, not eight destroyed or unique submarines. The convoy symbols are not historical ship counts.
- **P5 / Bainbridge recovered**, 740×565 archived Naval Historical Center distribution copy, catalogue and hash retained. Full still inspected: the embedded caption names ship, photograph ID, New York Harbor and 19 August 1943. Inset only; never an ONS 5 ship. `ARCHIVE_PROVENANCE.md` and `ARCHIVE_HARVEST.json` carry the details. **P3 remains unavailable** after bounded alternate searches; use its existing map alternatives instead of repeatedly retrying the broken Navy endpoint.
- Built **thumbnail B: LIBERATOR**, real P1 monochrome photo, black object label in clear sky; inspected full size and at 168 pixels. On NAS: `03_Picture/previews/thumbnail_B_candidate_v01.jpg` and `thumbnail_B_phone_v01.jpg`. A remains the no-text alternative. No test armed, no upload.

All media paths above are relative to `/Volumes/data/studio-live/ww2/02_Video-Projects/002_Closing-The-Atlantic-Black-Pit-May-1943/`. Maps carry their original code and the existing Natural Earth public-domain coastline basis. Both final contact sheets were inspected as still images; full-size checks caught and corrected missing arrow glyphs, overlapping symbols/text and the Newfoundland locator. No claim of watching animation or hearing narration is made. These are draft teaching states, not polished final-film approval. There is no music in either draft.

## Resume without duplicating work

Both batches are **complete**, no render remains running. `/Users/benjaminoats/_desk/logs/j2996/detection-v01.done` and `convoys-v01.done` are **0**; logs have matching names ending `.log`. No need to wait or re-render unchanged clips. The convoy batch's first attempt was deliberately stopped for a layout correction; the completed restart supersedes it.

`detection_maps.py` and `convoy_maps.py` render each state's still and video. `render_detection_draft.py --media <root> --done <marker>` renders/muxes/checks detection; add `--renderer convoy_maps.py --batch convoys_v01` for convoy comparison. Use the documented Pillow-enabled Python 3.14. `picture_inventory.py --media <root>` checks narration/timings and all clip/sequence hashes against the EDL.

Still unfinished: **39 paragraph briefs** outside these batches and the existing L001 opening; **169 sentence rows** after counting the separate four-sentence opening. Some are archive treatments rather than maps. L039 and L049 onward still need building; don't treat the two draft sequences as contiguous. Resolve all nine EDL boundary flags and chapter pauses; integrate archive insets and slow moves; select film-specific licensed music within the £0 brief; build the full edit; run technical QA and a capable watch/listen quality review; reconcile the voice review; only then send the finished cut to Ben's board. Keep job progress at **1/5** until the whole picture/map step is finished. The current partial work needs no new spend, account or publishing permission.

---

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

1. Recover P3 / 80-G-86005 and P5 / 19-N-50553 from an authoritative alternate distribution; both supplied Navy catalogue URLs returned 404 through curl. Do not retry the unchanged links indefinitely. P3 occurs in two shot rows and P5 in one; all three need recovery or their line-specific map alternatives. The line-specific map alternatives may replace an unavailable contextual photograph without changing narration.
2. Render the remaining 57 paragraph map briefs and sentence states with real geographic/tactical content. Do not reuse the opening as generic filler. Verify submarine/radar/HF-DF mechanisms and the ONS5 fog / SC130 distinctions against their exact spoken lines. Inspect all rendered states.
3. Resolve the nine EDL boundary flags, chapter pauses and full-film edit timing; VO words stay locked. Use slow moves on archive photographs within their actual resolution.
4. Select a properly licensed WW2-specific music bed within the £0 brief. No OWB/HOS media reuse. Do not generate music or spend credits without a separately checked authorised route and live subscription preflight.
5. Assemble the full 1080p film, finish thumbnail B (LIBERATOR), adapt applicable studio technical QA to this new channel's rules, and make one quality pass. Ben's finished-cut watch covers the actual watch/listen input this session cannot perceive. Do not import OWB/HOS aesthetic gates that contradict WW2 rules.
6. Only after the full cut and checks are ready, put it on Ben's board for his watch. No upload or schedule; channel remains prelaunch.

PR #1014 is still OPEN: its voice report is a worker submission, not a recorded voice-stage Chief PASS. Before final delivery inspect the actual voice records and reconcile that review/status. J3031 already locked the exact script. No additional claims-check run was started here.
