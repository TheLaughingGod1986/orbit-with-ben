# J3060 — channel-qualified film routing

18 November 2026. Advisory code change for Chief review; no production approval.

## Cause and fix

`studio.film_dir` discarded every prefix. `jobs.on_board` checked only `repo`,
so a row with `repo=owb, film=WW2:003` could claim and release Orbit 003.
The board resolver now rejects unknown and foreign prefixes. Job board paths,
claim, release and Chief-completion checks require a consistent registered
channel/film identity. Media lookup rejects inconsistent explicit identities
before trying folders or named paths, reads qualified numbers directly, and
never borrows a foreign key from prose. Bare film numbers and OWB:J01 remain valid.

This preserves the existing board scope: only the configured board channel
uses these job-to-stage links. Valid HOS and WW2 identities do not start writing
to another channel's board. This change does not introduce new stage routing.

## Queue reconciliation

The registry maps WW2 to `ww2` (Field Order History). Eleven rows had WW2 film
identities but `repo=owb`: J2991–J2998, J3000–J3002. Corrected only their `repo`
and appended an attributed correction to history. Nine were done; J2993 and
J2996 were open. None held an active claim. Original history, status, worker,
progress, dependencies, approval records, results and deadlines are preserved.
Assertions compared all other fields and all unrelated jobs before saving.
Completed rows are corrected too, so reopening one cannot restore the mismatch.

## Affected Orbit records — read only

| Orbit film | WW2 work / observed residue | Existing repair ownership |
|---|---|---|
| 001 Aliens | J2991 script review; J2992 VO review (6ac5525f44); J2993 edit doing (253aac9346), no stage claim | J3014 script and J3015 VO; Chief must also reconcile the edit residue against original history |
| 002 Black Hole | J2994 script review (PR1009); J2995 VO review (d37657e3f0); J2996 edit doing (PR1018 checkpoint), no stage claim; next text describes WW2 preparation | Chief review required for these residues; no approval inferred from the checkpoint |
| 003 Exoplanets | J2997 script removed by J3013 / PR1020; J2998 picture still review (5b00529) | J3013 owns script correction; J3019 owns picture correction; J3017 is an existing script orphan-review task and must consult J3013 rather than repeat it |
| 004 JWST | J3000 script now todo with an explicit WW2 correction note | Existing correction retained; no further change |
| 005 Last Star | J3001 script review (PR1000) | J3016 |
| 006 Europa | J3002 script review | J3018 |

J3060 changes none of these status files. Existing thumbnail approvals, media,
schedules and all active claims remain untouched. No duplicate repair jobs were
created. The additional 001 edit / 002 residues are called out for Chief to
scope alongside the existing repairs; changing them needs original-state evidence.

## Verification

Focused jobs and studio tests cover conflicting WW2 identities, unknown prefixes,
valid identities for every registered channel, claim/release/completion isolation,
and media roots. Existing bare-number board claim/release and OWB-prefixed folder
resolution remain covered. No generation, publishing or YouTube changes.
