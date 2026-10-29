# J1218 — Acting Chief Codex review

Ruling: **FIX / NOT APPROVED**. PR #376 stays open and unmerged. J1213, rough v01 and delivered rough v02 remain held from Ben watch, upload and scheduling. This review does not approve the film or spend. J1218 remains the sole repair job; resume it for a separate v03 diagnostic, preserving v01/v02 and their manifests.

## Evidence checked

- J1218 brief, result and complete history; J1213 hold; J1193 still open and assigned to Gemini.
- HOS PR #376 head `095ef62d4aaacdcb8f59a9762d8b19cdb3b4ff59`: reported checks successful, but they do not establish picture approval.
- Delivered local master SHA256 independently verified: `edebeaf7e71d29051135859d7ad7e87bb4ee73d7e52a37b8251ccfb951dcad06`.
- ffprobe: video 539.958333 s, audio 540.000000 s, container 540.021321 s. The 21 ms excess is a container-boundary issue, not evidence of extra spoken content. Fix export/report precision; do not cut a spoken line to meet it. The summary's `under_9min: true` is not literally true of the container.
- Read assembler, remapped cut list, gate reports, repair notes; inspected full-runtime contact sheet and full-size master frames at 460.5, 464 and 468 s. No claim of full motion/audio review or clearance of six WARNs.
- Automated reports: polish PASS, 0 FAIL / 6 WARN; picture PASS, 0 FAIL / 6 WARN. Music SKIPPED_NO_BED is explicitly not PASS. Episode-gate evidence for v02 is absent from this PR/pack.

## Required repair under the same J1218

1. **Teach MOTION FAIL:** P5 `09_wood_vs_metal` (452.9646–459.8396), `10_metal_easy` (459.8396–462.798), and `11_safe_path` (462.798–469.338) are three consecutive full-frame teach graphics. HOS requires moving plate between full-frame teach graphics. Recompose the middle explanation over an appropriate existing KEEP moving plate, with linework clear of worker/hero and legible on phone, or another compliant sequence. No new mint/spend. Recheck the whole film for this pattern.
2. **Assembler safety:** WORK is on NAS but `join_full` unlinks existing outputs and recursively deletes its old picture-QA folder; helper functions also delete NAS scratch files. Never execute these destructive branches. Make the next assembler non-destructive on NAS: fresh version/run directories, temporary files/cleanup on local scratch only, copy and verify durable deliverables without deleting/overwriting prior NAS records. Preserve the delivered v02 and hash.
3. **Review evidence:** contact-sheet labels use `film_t`, which can lie outside the row's actual interval (metal_easy label 467.419 s versus actual interval 459.8396–462.798 s). Use actual sampled master time for review labels. Gates use interval midpoints, so this finding does not by itself invalidate their reported PASS. Correct the misleading labels and validate all row intervals/sample times. Confirm `06_same_thing` still teaches its spoken explanation: its builder currently concatenates two plates without the former alpha graphic.
4. **Motion evidence remains required:** six low-detail WARNs and freeze detections need per-row full-size/motion findings, distinguishing real freezes from detector events. Do not assert they are detector-only merely because they occur on graphics. Record all Teach and Polish checks, including unresolved music/SFX, with honest FAIL/not-yet-checked outcomes.
5. **J1193 is a required final graphics dependency**, not an absent-Chief wait. Gemini must review the 11 graphics against locked VO, phone legibility, event timing and Atlantic geometry. Incorporate its findings before requesting picture PASS. Repairs above can begin without waiting; if J1193 is still open at delivery, use a dependency hold naming J1193 and a concrete recheck time. Do not claim or duplicate that specialist job in this review run.
6. Run unchanged picture, polish and episode gates on the new delivered version. Export comfortably within 540 s including container/audio padding while retaining all locked words and required ending. Check pause edits against locked VO. No music generation is authorized by J1218; music and SFX remain unfinished.
7. Update production-status plus HOS PIPELINE.json and generated STATUS/board in the repair PR; #376 currently omits the pipeline/board update. Commit from a clean worktree. Supply durable master SHA and accurate paths, contact sheet and flagged frames. No Ready-for-OK card.

## Dispatch and limits

Reopen J1218 for its existing assembly specialist chain with this ruling; no duplicate v02 repair job. Prior worker progress remains historical evidence, not Chief progress. J1213 remains blocked on repaired delivery plus J1193. Retain deadline 12 Nov 20:00Z. Give J1193 that deadline so its prerequisite work is visible to dispatch. No credit/date/Ben holds elsewhere change.

Disk: authorized NAS offload found no eligible old scratch; about 11 GB free. Use fresh mounted NAS render directories and local temporary cleanup; do not remove NAS files. No render started, no credit spent, no YouTube/Buffer changes. Nothing required from Ben for this review.
