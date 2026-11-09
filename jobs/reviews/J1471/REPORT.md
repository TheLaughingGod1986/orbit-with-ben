# J1471 source inspection — 1 November 2026

Codex covering. Partial inspection only; remediation is blocked on an adequate approved ISS opening candidate. No corrected master, gate PASS, creative approval, full moving-picture review or audio audition is claimed. J1356 and all existing holds remain.

Read h40 VO lock, J1468 delivery, J1321 source provenance and accepted assemblers. All three repaired master hashes still match J1468 (`preserved_masters.json`). No media, manifest, audio, graphics, gate or YouTube/Buffer state changed. GBP0.

## Missing input

AR2 needs an approved moving ISS shot suitable for the 0–2.4 s opening and matching one-second loop preroll, with identifiable station detail, coherent fill, <=2.35x upscale, and enough sustained native motion to pass the unmodified 1.50% opening-difference threshold. The existing accepted station cache is `/Users/benjaminoats/_desk/cache/J1321/crew2_351_374.mp4`, NASA full-reel 351–374 s, SHA256 `593da478539edb1ea5c6038268704f31abeca4493393dbe9ffab159151490579`. No other approved station source was identified in the binding source records inspected. This is a scoped asset request for Chief, not permission to mint or waive a gate.

Diagnostic proxy scans at native speed sampled 18 one-second in-points (full-reel 352–369 s), each over 1.5 s. At 4 fps, scale to 72x40 grayscale; calculate adjacent quarter-second absolute mean differences / 255 * 100 and take the minimum adjacent-pair mean. Full-picture results range 0.156–0.321%. Three exploratory 460x258 crops at x=200/410/620, y=230 (roughly 2.35x when composed at 1080x608) peak at 0.704%. JSON contains all samples. These are **diagnostics, not final 9:16 gate results, approved framing, or proof that every possible crop fails**. They do not justify rendering an unreviewed crop or accelerating footage merely to pass a metric.

AR1's assembler already changes source at 2.4 s; J1468's real composite is first detected at 6.0 s. Its opening change therefore needs a visually distinct approved cut, not metadata relabelling. AR3's accepted NOAA crop is genuine moving imagery but measures 1.41% in the saved final gate; it still needs an appropriate opening interval and loop review. The NOAA source exists on the NAS (272,694,488 bytes; checked read-only with elevated filesystem access). An initial sandboxed NAS stat hung; this is not an absent-source finding.

## Resume

1. Chief supplies/identifies a suitable already-approved ISS interval (or separately scopes acquisition/another approach). Preserve AR2 v07 and the separate v10/v09 branch exclusion.
2. Correct only failing opening intervals in fresh versioned masters; stream-copy repaired AAC and preserve accepted remaining picture. Maintain h40 clocks, hook captions, graphic timing and loop continuity.
3. Run complete picture/polish/music/SFX/Shorts-open/loop checks with actual source metadata and pre-upload mappings. Review full moving cuts and audition full audio including pace WARN. No listening was performed in this run; ASR or stills do not replace it.
4. Hand evidence to J1356 for protected readiness review. No Ben watch, upload, schedule or other hold is released.
