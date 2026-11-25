# J3307 — FIX all three exact v02 thumbnails

Publication reconciliation, 22 November 2026: this is the historical v02 decision from the earlier J3307 run, preserved below without reruling. J3381 has since delivered v03 and J3382 approved it in merged PR #1184. The historical queue/ledger status below describes the earlier review time, not current state. Current authority is jobs/reviews/J3382/REVIEW.md: only the exact v03 hashes have conditional one-test permission. J3308–J3310 retain their J3307 dependency, fresh matching finished-report and no-running-test guards, unchanged live A and title, and parked Round 2 titles.

This publication contains only the thumbnail decision and technical file checks. It excludes the old branch’s bulk audit exports, signed thumbnail URLs, queue changes, and machine/storage notes. Current ledger already preserves complete v01 and v02 history under v03; no ledger or film-stage rollback is needed. The original owner PRs #1118/#1180/#1182 remain evidence references; this change does not merge their stale ledger rows.

## Historical review (17:37 UTC)

22 November 2026, Codex acting Chief. Authority re-read at 17:33 and 17:37 UTC: Codex elected; Claude and Grok unavailable. This is a completed review with corrective successors, not creative approval or approval of a film stage.

Reviewed owner-authored main-base PRs #1118 (fe8c0886cdd6fbefa3a360c7817bb3b3ac1f8ad3), #1180 (3b52ce72571a98c910199481d453195d019d7581), and #1182 (c44d27c22ace78bf63e4e550e1446412d0555174); all three original critic files and DECISION.md; thread through #7082879509. No prior final J3307 ruling found. All three original critic slots were Gemini fallback runs, not three different model families. Codex inspected the actual v02 pixels independently.

## Exact-file decisions

| Candidate | SHA-256 | Decision | Reason and required correction |
|---|---|---|---|
| T041 / Europa | 901b210f7636309dcff97453f54a08326c12405e12fb7cfd548b0b6792cab9dd | FIX | Correct Earth > Europa direction and readable hook, but Europa is now a small secondary object (~327 px diameter / 43 px at phone size), while the cropped 850 px Earth dominates. The panel's combined-subject-mass instruction does not waive the house hero-size/whole-subject requirement (§2.1, §2.A.4). Enlarge Europa as the recognizable hero with a larger partial Earth reference; preserve the real terminator and size direction. Remove residual bright nebula contours, which resemble scratches. |
| T042 / Light Speed | 7a66560e03fb7959d416db47cdd70aa3a8a76cafe4de5b9e04eee83d3d17aee8 | FIX | Concrete 7× hook and dark separation are improved, but the astronaut is visibly soft at full size and phone size, abruptly cut through the torso by the bottom edge. Motion cues become almost invisible at 168 px, leaving an ordinary EVA impression. Use a sharper real subject/crop with whole recognizable silhouette and visible smooth photographic travel cues; do not fix subject area by enlarging a soft crop. |
| T043 / Last Star | c90e92072dccadbb01530ab6e1b4e603722eef57639ab3d035a435e096115ff7 | FIX | Earth inset correctly removed and the Sun comparison now matches the hook. However the 310 px red dwarf (~41 px at phone size) is secondary to the cropped 850 px pale Sun; this still misses the hero-size requirement. Enlarge the dwarf, restrain the partial Sun reference and remove residual nebula contours. Differentiate layout from Europa. Keep transparent solar-texture illustration provenance. |

HOOK, BAND and colour GRADE pass on all three. PHONE text and duration clearance pass; PHONE subject hierarchy/finish fails as above. Full-size and independently regenerated 168×94 / 360×202 badge sheets were actually viewed, with 9:19, 8:55 and 8:38 badges. No audio or motion perception claimed. These are still thumbnails.

All files match the exact manifest SHA-256 values, are 1280×720 and below 2 MB. Independently rerun saturation / near-black: T041 134.2 / 15.5%; T042 129.0 / 15.9%; T043 130.3 / 13.0%. Detailed output: CHECKS.json. Passing colour checks do not clear the visual defects.

## Source/provenance verification

Queried the official NASA Images API by all five IDs and downloaded the official asset variants. All five source hashes match the builder manifest:

- Apollo 17 Earth: `as17-148-22727~orig.jpg`, cb4c3d2da98ee72130ebfd2ea472fc84ede6726002c2a8c9cabd86e4deea9f0f.
- Europa: `PIA19048~medium.jpg`, 9a16941ce72791857431c2c4d2bf57000167ddc0b425663f32385225070c0705. The archive's original has different bytes; the medium variant matches. NASA identifies the Galileo color mosaic and its real geometry; no claim that the dark terminator is an editing defect.
- EVA: `S84-27018~orig.jpg`, bd5fae489f60b49c9636aed77dea851d8284d50d23a3031a8217b24b0218c23f. NASA identifies Bruce McCandless/MMU aboard STS-41B; this was not relativistic flight.
- Solar texture: `GSFC_20171208_Archive_e002069~orig.jpg`, e13524641873a6ec38798932ff3823f2f9fa33e27caf6c309d0f0fbe3eb4af34. NASA identifies SDO AIA 304-band launching filament. The smaller red star is a documented solar-texture illustration, not a resolved red-dwarf photograph.
- Mystic Mountain field: `GSFC_20171208_Archive_e002064~medium.jpg`, 5094dfb82561d2c5f618af9f5b83ef7fd5ac06c1f67341d2baebaef2db44a2b5. NASA identifies the Hubble pillar scene. The builder suppresses diffuse signal but leaves visible contours; it is not purely isolated star pixels. Public-domain release is linked in J3378's manifest; exact-variant URLs should be retained in v03 provenance.

Asset base: https://images-assets.nasa.gov/image/<NASA-ID>/<variant filename>. Source page URLs and credits remain in the DESIGN_MANIFEST.json in owner PR #1182. No source fabrication or hash mismatch remains unresolved.

## Successor-test decision and preserved state

**NO successor-test authorization for any of these v02 hashes.** Explicitly refused T041 over finished inconclusive T006 (15–29 Oct), T042 over finished inconclusive T004 (1–15 Nov), and T043 over finished inconclusive T016 (28 Oct–11 Nov). Recorded reports support the historical finished/inconclusive state; no fresh Studio state was read or changed in this review. The follow-up must still check the matching finished report and absence of a running test immediately before a permitted action.

J3381 is the linked £0 rebuild of all three compositions; J3382 is the gated Chief review after J3381. J3308/J3309/J3310 are explicitly blocked with those successors named, retaining their original dependency on J3307. They must not run merely because this review is done. J3382 must update final paths/hashes and grant both exact-file PASS and explicit one-test authorization before reopening; no partial batch release. No title, description, upload, schedule, privacy or live-thumbnail changes. Round 2 titles and the separate later listing pass remain parked.

Ledger reconciliation retains v02 active proposals plus each complete v01 proposal under history; original audit result updates for T004/T019 retained. None is marked running/approved. Independent film states for 024/005 are untouched. Only 006 thumbs is owned; it returns for corrective work, not to an approved state.

