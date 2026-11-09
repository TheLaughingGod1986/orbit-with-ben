# J2311 handoff — Mon 14 Dec local candidate

Label: **EXCEPTION**. This is not an E1 PASS and not a swap.

Scheduled copy `heiGCnGKTkE` is still private for 2026-12-14 11:30Z (today's snapshot, title unchanged). `UPLOADS.json` still points at v04. v04 sha256 `31f362f4437b4ca56ec16b8abef1dce4c65fb5a5c6c7b5b4e2ba39229a33efd5` still matches. No YouTube, Studio, Buffer, privacy, schedule or title change.

## Candidate

`02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/10_Shorts/mon14_half_moon_daylight/06_Final-Exports/029_short_mon14_half_moon_daylight_v05.mp4`

- sha256 `f16e0e3c1c0bacdcbac6cc90739ece96fa56fd2cee03e9006feab842bea89852`
- 22.04 s. Last word `daylight.` ends at 20.88 s. Tail 1.16 s.
- The v04 end card is gone. From 21.43 s the picture crossfades for 0.30 s onto frame 0 and holds it. Tail OCR does not read "Full film on the channel".
- The setup words "So imagine" are trimmed. The remaining recorded lines are unchanged. £0. No new speech or pictures.

## What the tools measured

| Check | Result |
|---|---|
| Cut 1 | 2.30 s (gate 2.3 s; frame diff 67 from 2.20 to 2.45) |
| Cut 2 | 4.63 s (frame diff 94 from 4.50 to 4.75) |
| Frame 0 | motion 32.38, frame diff 8.74, visor 0, near-black 3.6% |
| First word | 0.06 s (`the`) |
| Surprise | `explodes` at 1.48 s |
| Sentence-1 breath | 0.20 s (`explodes.` to `The`) |
| Later holds | longest is `s05_orion_flare` at 3.80 s |
| Loop tail | 1.16 s, crossfade 0.30 s |
| Shorts gate | PASS |
| SFX level | PASS |
| Music gate | PASS |
| Polish / picture QA / cover | PASS, with one low-detail warning on Chajnantor |

This session did not watch the moving picture or listen to the mix. The times above are from the word file, ffmpeg and the gates.

## Conflicts for the reviewer

1. Inside sentence 1, `night` to `Betelgeuse` is a 0.220 s gap, over 0.15 s. Closing that recorded silence would put the last word near 20.80 s, and a 22.00 s file would then leave a 1.20 s tail. The gap is left as recorded.
2. Line 1 is `the night Betelgeuse explodes.` The recording does not ask `How bright will Betelgeuse get when it explodes?` No new line was written.
3. `So imagine` was trimmed so `explodes` could start by 1.5 s. Those two words are not a fact.
4. Polish and picture QA warn that the Chajnantor plate is low detail. Both tools still PASS. The same plate was in v04.

Do not swap this onto `heiGCnGKTkE` from this handoff. A later authorised swap has to update Buffer and `UPLOADS.json` together. 14 Dec is after the 3 Dec readout, so this cut is follow-up only.

Copies with checksums verified on both sides: iCloud `OWB UAT/J2311_029_mon14_v05` and NAS `YouTube/orbit-with-ben/OWB UAT/J2311_029_mon14_v05`.
