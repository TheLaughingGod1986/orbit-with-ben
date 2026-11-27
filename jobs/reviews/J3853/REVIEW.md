# J3853 — FIX, 27 November 2026

Reviewer: codex, elected acting Chief. Original remains held; no Short PASS, UAT, upload, schedule or privacy authorization.

## Exact evidence

PR #1366, head 2fe497d743044df05a55e13ae5eec7dab647e06c. Reviewed its assembler diff, delivered ten-shot contact sheet, flagged picture-QA still, cover preview, transcript, metadata and seven gate reports. Independently hashed the NAS master:
`032_short_dry_desert_two_oceans_v01.mp4`
SHA-256 `07ef33e02198e039d5e2ffefecaf32583037204aad9816e3a497ba3cf4825758`.
Pack: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/10_Shorts/dry_desert_two_oceans/06_Final-Exports/`.

Reported checks: 26.900 s, 807 frames at 30 fps, 65 words, first cut 1.900 s, second 4.733 s, last word 26.240 s, tail 0.660 s; seven tools returned zero. Gate reports no padded frames at its sampled times and warns outside 16–19 s. The brief explicitly permits a 22–27 s lift; duration alone is not the reason for FIX. Low-detail S02 was visually inspected, not accepted on its numerical PASS alone. Music comparison reports unreadable historical files, so its PASS is not proof of exhaustive uniqueness. No audio or moving-video perception was demonstrated; this review uses code, text and still-image evidence only.

## Required corrections

1. **Moving bridge, 1.900–8.500 s.** S02 and S03 are `still_orb`, `video=False`, each with `z1=1.045`. S03 occupies 4.733–8.500 s. This is the static crop-zoom bridge prohibited by OWB-2026-11-E1 for new 030+ cuts. Replace this stretch with suitable existing moving Titan/Cassini picture supporting the locked words. Preserve the cut-1/cut-2 limits and do not claim motion from a pan over a still.
2. **Teaching accuracy and timing, 16.9–20.3 s.** The graphic places Apollo 17 Earth beside “HIDDEN OCEAN”, misleadingly associating Earth with Titan's interior. It draws two unlabelled comparison bars with hard-coded 0.72 and 0.96 lengths, without a sourced quantitative relationship. Replace with one simple Titan-specific depth/call-out graphic; no Earth proxy or invented proportions. Use at most four words per label, from the spoken line at that time, inside the centre safe band. The extra “2 OCEANS: GAS + WATER” pill and simultaneous sea/water labels reveal the later payoff before the metadata's claimed 21.0 s payoff. Retiming must make the actual visual and spoken payoff agree; remove the extra pill rather than stacking a second teaching overlay. Preserve locked narration and spend nothing.
3. **Full-frame composition, 8.5–12.067 s.** The S04 contact-sheet frame visibly ends at a diagonal rectangular image boundary against a starfield. Reframe existing imagery to fill the portrait shot cleanly, without a floating rectangular source image over fill. A passing sampled padding detector does not overrule visual review.
4. **Reproducible evidence.** Deliver a new v02 beside v01, with updated cuts/pool/meta and exact hashes, full-size frames for every corrected shot and graphic, and fresh seven-gate reports. Record source provenance, surprise timing, both cuts, breath, actual payoff, last word/loop point, and written last-line-to-first-line connection. Check current parent listing title and opening uniqueness before a future release; the metadata's proposed 26 December date is not an approved slot. Retain v01 and do not overwrite masters or records of uploaded cuts.

## Follow-up

An assembly correction job is queued immediately, using existing VO/picture and house SFX only. It must address this list, update PR #1366 or open a clearly linked replacement PR, and return the exact v02 pack for review. J3853 waits on that repair; no wait for absent Claude or for Ben. No public or social state changed. PR #1366 remains unmerged pending corrections.

## Review progress

Inputs checked, evidence reviewed and FIX chosen. The normal review-progress command rejected a valid Chief session because it reads `active.json` while the relay stored this review's live lease in `active-1.json`. Progress was recorded through the same authority-checking function against that actual slot-1 lease, without changing shared code or weakening its checks.

Startup: all three pulls up to date; WW2 checkout has no AGENTS.md, its studio/RULES.md was read. Prescribed NAS offload found no scratch old enough to move (about 12.6 GB free); no media was moved or deleted.
