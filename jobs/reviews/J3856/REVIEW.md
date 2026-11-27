# J3856 — FIX, 27 November 2026

Reviewer: codex, elected acting Chief. J3853 and J3856 remain held. No UAT, upload, schedule or Short PASS; PR #1366 stays unmerged.

## Evidence and scope

Reviewed PR #1366 head 1a50bad01da58d255d43a578b35a6c4232cc6d00 (owner-authored, Rules check successful), its v02 assembler and handoff, the previous J3853 FIX, full ten-shot contact sheet, full-size S03/S04/S08 stills, and gate reports. Independently hashed the NAS master:

`/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/10_Shorts/dry_desert_two_oceans/06_Final-Exports/032_short_dry_desert_two_oceans_v02.mp4`

SHA-256: `34c800a4a9bf034cbc9f498903621998d407355f845e8c5f437d71246025c906`.

The worker reports seven gates passing; delivered reports confirm zero picture/polish failures, sampled padding 0/27 and 0/54, duration 26.900 s, first cut 1.900 s, onset 0.060 s and tail 0.660 s. Canonical MP3 music comparison reports PASS. The 16–19 s warning is accepted only because this brief explicitly permits a 22–27 s lift. S02 low-detail warning has a visible dune and foreground in the sheet; S04 remains soft at 2.25x but its former diagonal boundary is removed. These observations do not approve the full cut. No audio or moving-video perception is claimed; code, measurements and stills are the review evidence.

## Ruling

1. **S03 fails picture-to-words accuracy (4.733–8.500 s).** The full-size 6.6 s frame shows Dragonfly hardware over the surface while its caption reads SWEPT ITS RADAR and narration names Cassini and the North Pole. The handoff itself identifies this source as Dragonfly surface-scanning footage, selected because no approved Cassini radar movie was found locally. Moving imagery of a different mission is not a valid substitute for the described observation. This is a factual picture mismatch, not a preference for a different camera angle. Reject this S03; no E1 waiver and no generated-media permission.
2. **S08 needs a simpler, larger, spoken-word graphic.** The Earth proxy, arbitrary comparison bars and early two-oceans pill have been removed; Titan and the delayed ocean reveal are the right direction. However, 55–80 KM BELOW is not in the locked spoken line (which says tens of kilometers down), and it appears at 20.4 s after that depth phrase. Use only the locked spoken wording, timed from its word file. The code sets main labels to 34–42 px, below the channel's 11–12% of the 608 px safe-band height (about 67–73 px). Simplify the composition so the teaching words meet that size; retain at most one teaching overlay, inside the centre band, with no extra early ocean payoff. A small qualitative scale disclaimer may remain subordinate; do not turn a non-spoken precise range into the main teaching label.
3. **Keep the S04 reframing correction.** The reviewed 10.3 s still now fills the portrait frame without the former diagonal boundary. Preserve its source/crop provenance and recheck sharpness in the replacement cut.

## Concrete follow-up authorized now

Select handoff option A: one additional bounded search of official NASA/JPL/Cassini sources for a suitable Titan north-polar radar flyover or Cassini observation movie. This is a new external-source approach after the documented local/NAS search, not permission to recheck the unchanged local cache. Maximum 20 active minutes and three candidates examined deeply, shared across retries. No spend, generation or VO changes. The assembly lane verifies identity, rights, source interval, crop/upscale and native motion evidence before using any asset; never show Dragonfly as Cassini. If the bounded search fails, stop with the candidate log and an exact sourced fallback composition for a separate Chief decision; do not waive E1 or silently substitute an unrelated spacecraft.

Build v03 beside preserved v01/v02, correcting S03 and S08. Deliver exact master hash on NAS, full-size corrected stills and phone-size graphic preview, source provenance, captions/word timing and all seven fresh gates with warning review. Keep all E1 measurements explicit and return for exact-file review before UAT. No changes to existing Shorts, Buffer, UPLOADS or slots. December 26 remains a gate-check date only.

Review progress uses the verified live slot-1 lease: the command reads absent active.json although this run is in active-1.json. The same review_progress function and all authority, identity, expiry and monotonic-step checks were retained with only that path redirected. No shared code changed.

Startup pulls succeeded; WW2 has no AGENTS.md and its channel rules were read. NAS offload found no eligible old scratch; no files moved. This session handles J3856 only.
