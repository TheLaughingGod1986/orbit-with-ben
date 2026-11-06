# J2297 — 033 picture handoff repair

Date: 6 November 2026. Reviewer: codex, elected acting Chief (chief_relay.py status confirmed).

**FIX — picture remains unapproved.** This is a workflow and documentary finding, not a media review. J2238/h94 approved planning; J2256/h175 approved the stills plan and £0 Option B. Neither establishes that the subsequently harvested assets depict the planned subjects or that the opening moves. Accepted script and VO remain unchanged. The picture-plan mappings affected below require correction before use; retain previous files as history.

## Evidence inspected

- Current film status: picture was review, referencing J2256/h175 and completed J2290, with no live review handoff.
- J2238 and J2256 review records, their queue histories, SHOT_LIST_v01, STILLS_LOCK_v01 and STILLS_POOL_STATUS_v01.
- Open PR #578, exact head `adab48f716e066f57e2e1c9f56c3de789dda854e`: STILLS_POOL_STATUS_v02.json, CODE_GRAPHICS_J2290.json and renderer source. No merge or media approval of that PR in this task.
- Manifest reports 39 harvested assets, 32 caption/title differences, 17 explicit `do_not_treat_as_lock_subject` entries and `keep_assigned: 0`. Wording differences alone do not prove a wrong subject; the 17 exclusions and unresolved mapping are concrete blockers. Examples recorded in the manifest: PIA00141 = Miranda rather than Uranus limb; PIA01361 = moon montage rather than polar haze; PIA00271 = simulated Venus rather than Blue Marble Earth. The correction worker must verify official records and usage terms directly.
- Frame-0 manifest entry for PIA01283 is a 737×256 JPEG, 18,803 bytes, SHA-256 `16e1fdbc4ad6c4661e7a79bd3461514afc6a476e1b7c87e1e974f55734cc8049`. This does not supply R01's 0.00–6.22 s native motion. The manifest's no-video finding is not proof that no alternative exists anywhere. Preserve the excluded standalone Short opener.
- Graphics manifest contains 14 files, all DRAFT_NOT_KEEP, rendered at 12 fps. It records R26 aliases, R46/R52 naming ambiguity and an R55 source substitution needing row reconciliation. Metrics and source code are not evidence of acceptable moving playback.
- Five of six graphic source paths point into `/Users/ben/_desk/worker/...` and do not exist on the Mini at the recorded paths; the NAS Uranus path does exist. This is not a claim that copies cannot exist elsewhere. No binary transfer or media viewing was performed.

## Required correction and handoff

1. **J2299**, OWB:033 / picture / assembly, after J2290: reconcile all source-to-row mappings and terms; correct the opening input under the bounded missing-footage rule; preserve locked narration/timing; deliver checksum-verified Mini-readable assets and corrected graphics with applicable picture/polish evidence. Reconcile summary counters and graphic naming. £0 only, no generation or publishing. This job's detailed brief is the correction checklist.
2. **J2300**, OWB:033 / picture / QA, after J2299, requires `moving_video_input`: inspect every picture and directly view opener/graphics against the locked narration, record hash-specific KEEP/FIX and queue any further correction. Chief final decisions and Ben watch remain required.

Picture is FIX/blocked pending this chain, not waiting for Ben. Planning approval cannot waive actual subject, motion, reuse, upscale, graphic or finishing gates. No assembly release is granted by this repair. No credit spent; no YouTube or social changes; no NAS deletion.

## Verification and limitations

Both repositories pulled successfully after sandbox access escalation. Thread read through #6693748441; HOS inbox empty. Tool inventory provided no demonstrated audio or moving-video perception; capability record was left empty. This task could establish FIX from incomplete and contradictory documentary evidence without pretending to hear or watch media. Dependent QA carries the explicit moving-video requirement.

NAS offload was invoked at approximately 19 GB free; it correctly deferred to the 01:00–06:00 window. No render or large download was started.
