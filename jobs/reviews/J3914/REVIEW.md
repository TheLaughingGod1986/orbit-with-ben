# J3914 — Review of OWB 064 Short 2 v02 (PR #1394 at 567850e9aa): FIX, one word

Claude Code (`claudecode`), reviewer lane (rule E), 27 November 2026. Parent: J3904. Writer job: J3913. Chief ruling: J3912.

## Ruling

**FIX. The script is not locked yet, and there is no VO decision.** Four of J3912's five fixes are met. Fix 1 is met in v02 but not yet in the chosen variant v02b. One spoken qualifier needs restoring. After that, a reviewer can lock without another source run, as long as no other words change.

## Evidence against J3912's five fixes

1. **Surface vs atmosphere: met in v02, one gap in v02b.** Both say "Venus's surface" and "Uranus's air". The winter clause and "Closer in" are gone. **Flag:** v02b line 2 reads "Uranus has no surface;", but NASA's wording is "doesn't have a true surface". J3912 asks for qualifiers to be preserved, so the writer restores "true".
2. **Claim and quote check: done.** Gemini (`gemini-4-argon-high` via agy) found C1 to C9 verbatim with 0 flags. I fetched all three URLs directly and every quote holds. Recorded in `064_short02_QUOTECHECK_v02.md` on PR #1394. Gemini rated C5 acceptable; I kept it as a flag because of fix 1.
3. **PASS claims withdrawn: met.** Plan v02 §5 turns every v01 checkbox into a target or a pending check.
4. **Provenance and licence: met, and honest.** R03 and R06 are now classed as Veo CGI (not Keck). R05 is a still-derived push-in. R01, R02 and R08 are recorded as not found. Licences are per source (ESA/Webb CC BY 4.0, PIA23791 JAXA/Kevin M. Gill). **This doesn't block the script lock, but it blocks assembly:** frame 0 still needs native moving subject footage that has been verified (R01 or a replacement). The Uranus beats must also be re-planned so that no Veo clip is presented as real footage.
5. **Duration: resolved for this Short as 16.0–19.0 s (v02b direction).** Reasons: Ben's 19 Nov 2026 rule (`studio/RULES.md` line 189, `gate_shorts_open.py` `DUR_BAND = (16.0, 19.0)`) is the newer rule and the gate's own band. v02's mid estimate of 27.3 s is already over even the brief's 27 s ceiling. J3912 left this choice to the reviewer. v02 is retired. The wider conflict in the rule text (RULES.md lines 67, 86 and 288 still say 22–27 s) is for the Chief.

## For the writer (exact)

- v02b line 2: restore NASA's qualifier ("Uranus has no true surface; that's its coldest air." or the writer's equivalent). Change nothing else.
- Recompute raw and expanded character counts and the fast/mid/slow estimate. Mid must stay at or below 19.0 s.

## Next

- Writer FIX job, then a dependent review job that locks the exact text and makes the bounded VO decision. That decision belongs to the elected Chief: live subscription balance, existing credit holds, approved voice, no cash/top-up/overage, and no reliance on dates alone.
- J3904 stays held, next check 2026-11-28T14:45:00Z.
- No spend, upload, schedule or privacy change was made. No audio or motion was reviewed; this was a text and source check only.
