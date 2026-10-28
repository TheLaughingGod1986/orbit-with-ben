# J1084 — acting-Chief ruling, 28 October 2026

**FIX — v06 is not approved for Ben's watch or a swap.** Codex is the elected acting Chief; authority checked immediately before this ruling. J1084 stayed blocked throughout review. J1059's Ben-approval hold remains in force; do not restore its v05 approval card or point it at v06.

## Evidence checked

- Original J1084 body, result and full history; J1059 rejection/hold history; J0935 prior rulings; worker branch `codex/J1084`, evidence commit `8379c457f` and assembler.
- Actual local v06 master SHA256 independently matched `de60a9b18d497b59a7777d77767d9080da8fb22959f17913b31bb0256fda4eb9`.
- Full-runtime 2 fps sheet, full-size frames at 0, 7.3, 10.5, 13.8, 20.2, 24.8, 25.5 and 25.95 seconds, plus all five saved gate reports and the source-aligned/Whisper transcript.
- Recorded gates: opening PASS (26.03 s, cut 1 at 2.5 s); picture PASS (0 FAIL, 3 WARN); polish PASS (0 FAIL, 1 WARN); music PASS with unavailable comparison-file warnings; SFX PASS. Recorded delivered AAC is -14.4 LUFS / -2.0 dBTP. These are worker measurements, not fresh reruns in this review.

## Decision

1. **Opening structure accepted:** the locked-long sentence is complete: “A robot built to last ninety days on Mars kept going for more than fourteen years.” Do not return to the rejected fragment. Accept the resulting fourteen-years reveal at 5.16 s and wind explanation at 9.224–11.304 s for this revision: the 9–14 s long-title banner is separate from the readable captions and does not obscure them. This is a specific timing decision for Ben's requested complete opening, not a general rule change.
2. **Picture correction required at 24.8 s:** the final body shot (`s07`, JPL-20200303-MSLf-0001 at source 8 s, crop 608:1080:1200:0) visibly includes a rover wheel and hardware along the right/bottom edge and a black wedge at the top. It is not the neutral ground claimed by the pool/metadata. The Opportunity story must not imply this MSL footage is Opportunity. Correct the crop or choose an existing verified neutral moving plate; inspect the entire shot, not only its midpoint. The clean reverse loop at 25.5 s does not cure the preceding frame. This applies the picture/words match rule and the prior rover-deck correction, without overriding an automated gate.
3. **Softness warnings reviewed:** terrain is recognisable at 7.3, 13.8 and 20.2 s, though soft. These warnings alone are not this rejection. Keep the existing upscale ceiling; no new generation is requested.
4. **Audio acceptance still needs an audible check:** the transcript supports a full sentence but Whisper says “from more” where source alignment says “for more.” This session did not audition the audio and makes no listening claim. The follow-up must actually audition the opening and joins, recording the method and outcome. Do not regenerate or rewrite speech merely to match ASR.

## Concrete follow-up

Queue one `assembly` job linked to OWB:025: make v07 with only the offending picture corrected, preserve v01–v06 and the complete opening/remaining VO, rerun J1084's gates and delivery checks, and return to elected-Chief review by 6 November 20:00 London. No paid generation, TTS, upload or schedule change. Start from `codex/J1084` at `8379c457f` in a clean worktree; media remain in the main checkout/NAS/UAT.

J1084 stays blocked on that follow-up, with a concrete dependency and verification time. After a corrected version earns Chief PASS, update J1059's exact filenames/hashes and Ready for OK card for Ben. Ben's deadline remains 11 November 10:30 London; absent approval, scheduled v02 `TtgHNLXfDSs` airs at 11:30 unchanged. No prior Ben, date or credit hold is released by this ruling.

Disk housekeeping: prescribed NAS offload was attempted; it stopped on a checksum-verification mismatch for `j0935_wed18_v03` and kept the Mini copy. About 12 GB remains free. No media was deleted or committed.
