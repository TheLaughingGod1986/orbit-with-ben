# J2478 timing candidate — Chief ruling needed before picture rebuild

Codex covering, 11 November 2026. No new takes, API calls or credit spend. Existing v01 and locked voice v02 are unchanged.

## Concrete work

`02_Voiceover/splice_v02b.py` builds an isolated candidate from the SHA-verified locked Trim 1 raw take. All source Scribe word spans are asserted to remain inside retained chunks. It uses pitch-preserving ffmpeg atempo at 1.45x for the opening phrase and 1.25x for the date, with 10 ms qsin edge fades. Later speech retains normal speed; the nickel/coffee-bean gap maps to 0.140 s. The script emits a source/output edit map, SHA-256 and mapped word timings. These timings are estimates from the source alignment, not independently recognised output timestamps.

Demonstrated numeric checks: closer ends 1.4858 s; twenty-fourth ends 2.5402 s; first word starts 0.0501 s; sentence-1-to-2 gap 0.1954 s. Candidate VO lasts 16.3998 s (17.3998 s with one-second loop tail). Every original recognised word remains in a retained source interval. These assertions ran successfully. No claim of audible quality, vo_check PASS or motion review is made.

Carried the existing Gemini section-3 slot correction into the plan: Thursday 19 November, Saturday occupied by muons, five-day lead and matching Moon Related link.

## Protected decision

After the mandatory opening acceleration, sentence 4 (This Supermoon passes...) starts at 8.9206 s. J2556 also requires the title banner to clear at least 0.15 s before that sentence: therefore it must finish by 8.7706 s. AGENTS.md requires the 9–14 s title window. Those constraints cannot both hold on this edited timeline. J2556's example later answer windows do not follow from its prescribed opening compression, and a new take is prohibited.

Recommended Chief decision: permit the title banner at 7.2–8.75 s for this dated Short, retaining the early answer and 17.4-second duration; alternatively give an exact authorised re-timing plan that preserves the 9–14 s title without adding a long silent pause. Also arrange an actual listening review of the 1.45x opening before adoption: J2556 estimated 1.24–1.28x, which does not put the complete surprise before 1.5 s on these retained spans.

## Remaining production work

After that ruling, apply the picture changes from J2556: s02 full Earth at 2.633–4.067, s03 Earth/Moon pair over space at 4.067–6.20, s04 clean lunar plate during Normally, native 4K opening crop, title positioned as ruled, s06 at 8.921, s07 at 14.425, loop at 16.400. Rebuild v02, run every gate including independent output voice checks, copy and hash-check the master on NAS, then queue review. This candidate is not an approved voice or finished film stage.

No picture render started, so there is no detached process to duplicate. Working branch: j2478-supermoon-short, worktree /Volumes/MiniWork/scratch/j2478-wt. Runtime media links point to the preserved earlier Gemini worktree; do not clean it. Candidate audio and records are copied to the NAS timing_candidate_codex_20261111 folder and checksum checked this run.
