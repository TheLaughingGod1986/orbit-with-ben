# J1825 — OWB 026 upload finish evidence

Codex, 3 November 2026. Result: captions corrected; upload completion remains FIX.

## Caption correction

Validated the existing approved `nearest_star_long_v06_en-GB.srt`: 129 cues, first starts 0.080 s, final cue ends 490.964 s, inside v06 picture runtime 494.476 s. These anchors agree with the approved v06 summary and caption builder. All cues have positive duration and monotonic starts. SHA-256 is recorded in CAPTION_VALIDATION.json. No caption wording or timing was edited.

Before insertion, captions.list returned only the automatic en ASR track. Installed the packaged SRT once as a standard en-GB, non-draft track. Insert returned HTTP 200 and serving; a subsequent independent captions.list confirms both the new manual track and preserved ASR track, each serving (CAPTIONS_FINAL.json). The immediate list response lagged the insert; it was not treated as completion proof and no second insertion occurred.

## Studio verification (Orbit CDP 9223)

- Confirmed Orbit channel ID UC_esArsDKd3GJvOkeO0DUog.
- End-screen editor shows the template picker and an empty element timeline; Save disabled. No existing target/timing to report.
- Cards editor says “Select a type of card to begin”; no existing cards or timings. Both dialogs closed with Discard changes; no editor save.
- Existing thumbnail A visually remains YOU CAN’T SEE IT. No Test & Compare opened or changed. Screenshots are outside git with paths and hashes in SCREENSHOTS.json.
- Not Made for Kids selected; AI-use Yes selected. Video language and title/description language both English (United Kingdom).
- API readback preserves title, description, tags, status, en-GB defaults and thumbnails. Long remains Private, scheduled 15 November 18:00Z. Old A6TW_6CXhcs remains Private, unscheduled. Before/after video records compare identical.
- Buffer registry requires no reconciliation: schedule and media unchanged; no Buffer mutation or post was made.

## Specific FIX returned for elected-Chief review

Proposed end screen: one specific video `rVqgtkBV3jc`, *What Happens If You Travel Near Light Speed?*, plus Subscribe to Orbit, both 07:54.533–08:14.533 (last 20 s; Studio frame quantisation may round within one frame). Video tile on the left, Subscribe on the right, kept off the main pictured subject. This is the related long that answers the journey-speed question, verified Public in TARGET_VIDEO.json.

Proposed single video card: same `rVqgtkBV3jc` at 05:55.220, the locked VO’s “Even light…” line (word timestamp 355.220 s). Default video title; no invented teaser text. This supplies a relevant travel-speed explanation at its spoken context.

These are new proposals, not prior approvals. The job authorises caption correction and read-only finish verification only, so neither proposal was installed. Upload stage must remain incomplete pending the explicit finish decision and implementation/readback. This scoped FIX is the required review handoff, not a claim that a higher Chief must return.

J0861 retains its Public condition and 15 November 18:05Z check for the three replacement Shorts’ Related links and long pinned comment. J1823 remains separate; no thumbnail correction or test attempted here. No new media PASS, video upload, credit spend, deletion, or privacy/schedule change.

## Operational notes

Both repositories pulled successfully after sandbox permission was obtained. HOS inbox: no new messages for Codex. Free space below 20 GB triggered prescribed NAS offload; no /private/tmp scratch was old enough to move. Work performed and evidence committed from clean isolated worktree /private/tmp/J1825-wt. Other checkout files untouched.
