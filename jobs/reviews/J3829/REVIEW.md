# J3829 — Chief condition review of J3818

2026-11-27 · codex, elected acting Chief (status rechecked before ruling).

## Ruling: FIX; condition not satisfied

Keep J3818 held. Do not clear J3022 or release J3023 on the current advisory KEEP. This is a bounded packaging/shot-list correction, not a request for Ben approval and not authority to publish, spend, change dates, or alter locked narration.

Reviewed J3829 and J3818 bodies, results and histories; J3719 DECISION.md; the studio thread through the J3829 worker report; PR #1358 at 2eb6fafcf66e3b03cb1b85c0a80231e6649e05c5; and PR #1359 at 7acecf7699da8598b6faa1f1e582403219a48bf4. Both PRs were OPEN against main, unmerged. No earlier Chief ruling on this hold was found. Gemini built and reviewed these inputs; its KEEP is advisory.

## Blocking evidence and exact correction

SHOT_LIST_v02.md retains PIA00233 in R11 (118.05–130.75 seconds), calls its reconstruction non-failing, and makes a nadir-image replacement optional. PR #1359 repeats this as a non-blocking execution note. This contradicts studio/RULES.md lesson 7: a computer model or reconstruction is a picture QA FAIL. The rule is broader than the phrase “Computer Simulated Global View”; a prior film using this asset does not exempt this new cut.

NASA identifies PIA00233 as a 3-D perspective view: https://science.nasa.gov/photojournal/venus-3-d-perspective-view-of-eistla-regio/ . NASA's full caption explains the computer-rendered radar/altimetry construction: https://flickr.com/photos/nasacommons/55130659601/ . The submitted shot list itself also identifies it as a 3-D terrain reconstruction.

Required follow-up:
1. Replace PIA00233 in executable R11 inputs with one verified real nadir radar plate from the proposed shelf alternatives (PIA00215, PIA00240 or PIA00241), after checking its official source, local hash, resolution and fit. Record the exact chosen file. Keep the reconstruction in the rejected-assets record; remove the optional/allowed wording. Preserve locked VO and timing.
2. Correct PIA18033 attribution in BUILD_REPORT_v02.md and related packaging records: NASA/NOAA Suomi NPP Blue Marble 2012, not Apollo 17. The existing pixels need not be rebuilt solely for this attribution correction; preserve their hashes.
3. Update J3818 REVIEW.md to reflect the correction and obtain independent review. Preserve proposed T045 and the verified v02 hashes when resolving the ledger conflict; do not merge the current unqualified KEEP as a release decision.
4. Once corrected evidence and the required PR merges are confirmed, record a new KEEP/FIX on J3818, then separately verify J3022 readiness before advancing J3023. Ben watch and publication gates remain intact.

## Checks actually performed

Viewed the combined thumbnail still sheet and recomputed NAS hashes; all match the submitted review:
- A: bc1b60dbacf405e9ef2c2bf169f5442cea1e5312dd56ceade96560c73fb2e393
- B: 29ea71dab31ab13efa723d5257856324be02a91e96f1aaa47783f3a395b34c75
- C: 4ec5544c4fd9a7e9338bb207be936c90ec2d0683eb307e45d3224aa7458903f1
- Combined sheet: 22ac3dfb600b8d514e76d923c2f05f697023d26e95405d01b2cdb798bad73160

Read the ten opening intervals and R09 repair in the submitted shot list. No blanket thumbnail, film, motion or audio PASS is claimed here. No demonstrated audio_input or moving_video_input was recorded for this session.

## Progress recording limitation

The requested chief_relay.py review-progress calls for steps 1 and 2 refused because the relay active.json record was absent, although status elected codex. No lease was fabricated. The claimed J3829 queue job records this Chief review's own three-step progress instead of reusing the worker's progress.

## Recorded follow-up

Correction job J3835 is queued (assembly lane, due 2026-11-27 12:00 London). J3818 remains on a dependency hold naming J3835, recorded with --recheck J3829; next verification 2026-11-27T12:15:00Z. J3022 and J3023 were not released.
