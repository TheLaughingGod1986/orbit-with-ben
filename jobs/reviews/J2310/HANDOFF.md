# J2310 handoff — Fri 11 Dec Test A local candidate

Label: **EXCEPTION**. This is not an E1 PASS and not a swap.

Scheduled copy `k2kEaA7ICjc` is still private for 2026-12-11 11:30Z (`PT34S`, title unchanged, API read 2026-11-06). `UPLOADS.json` still points at v04. v04 sha256 `ff4194857a027cfc5f93551ef398125276e6bcfb9cd3ce2fd18d8ee1134e2405` still matches. No YouTube, Studio, Buffer, privacy, schedule or title change.

## Candidate

`02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/10_Shorts/fri11_opening_testA/06_Final-Exports/029_short_fri11_opening_testA_v05.mp4`

- sha256 `d1c208d76aa4a675e6c07d091a6dba9fe29646cdf85b808b7814c659f1570f01`
- phone sha256 `e6613b6eeb23cf35663836ab5848566e4b4c1c059bacd1a5065f4bd8cdd3b930`
- 32.667 s. Last word `when.` still ends at 31.58 s. Tail 1.09 s.
- The v04 end card ("Full film on the channel", 31.88–33.88 s) is gone. From 31.70 s the picture crossfades for 0.30 s onto frame 0 and holds it. Tail OCR at 31.85, 32.20 and 32.50 reads `VISIBLE IN DAYLIGHT`, the same hook as frame 0.
- Spoken lines are the v04 lines, including the J0991 waiver line. Bed end fade is 0.12 s. £0. No new speech or pictures.

## What the tools measured

| Check | Result |
|---|---|
| Cut 1 | 2.23 s |
| Cut 2 | 4.72 s (unchanged plates) |
| Frame 0 | moving, diff 5.94, motion 13.2, visor 0.0007 |
| First word | 0.08 s |
| Sentence-1 breath (`shoulder.` to `That`) | 0.20 s |
| Later holds | longest is `s03_paranal` at 3.84 s |
| Loop tail | 1.09 s, crossfade 0.30 s |
| Shorts gate | PASS, one warn: 32.7 s outside 22–27 s |
| SFX level | PASS |
| Music gate | PASS |
| Polish / picture QA / cover | PASS |

This session did not watch the moving picture or listen to the mix. The times above are from the word file, ffmpeg and the gates.

## Conflicts for the reviewer

1. `explode?` starts at 6.70 s, after the 1.5 s surprise limit. The Test A opening was kept.
2. Inside sentence 1, `winter` to `at` is a 0.200 s gap, over 0.15 s. Those words were not cut.
3. `In this film, I will show you` stays under the J0991 Test A waiver.
4. 32.67 s is outside 22–27 s. Test A keeps this opening. Speech still runs 0.08–31.58 s. Only the end-card hold came off.

Do not swap this onto `k2kEaA7ICjc` from this handoff. A later authorised swap has to update Buffer and `UPLOADS.json` together. 11 Dec is after the 3 Dec readout, so this cut is follow-up only.

Copies with checksums: iCloud `OWB UAT/J2310_029_fri11_v05` and NAS `YouTube/orbit-with-ben/OWB UAT/J2310_029_fri11_v05`.
