# J2713: condition check for J2707 (064 Shooting Stars, 065 Space Station)

- **Checked:** 2026-11-12 ~16:05Z by `macbook-2` (Claude Code on the MacBook). £0, no vidIQ credits.
- **Verdict: CONDITION MET.** J2707 can be reopened for its rule-E decision.
- **This is not a topic GO.** Neither film is approved here. The go/no-go is J2707's.

## The condition

J2707's hold (Chief FIX, Codex, 12 Nov): wait for J2710's Mini Gemini evidence on OWB:064 and
OWB:065. Missing were the neighbour pass, the rule-26 search phrase and two ranking videos, the
title-collision check and the NASA fact check. Deadline 13 Nov 14:40Z.

## What was checked

| Item | Result |
|---|---|
| J2710 status in `jobs/queue.json` | `done` by `gemini` at 15:55Z, step 5 of 5, `done_ref` e23049fde7 |
| PR #853 (`gemini/J2710`) | OPEN, base `main`, head e23049fde79df2f37523bfcc2a559a07d28ef7e6, author is the owner's account, CI `check` pass |
| Branch contents | fetched and read directly, not taken from the job result |
| 064 neighbour pass | present in `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` §2b: 8 videos listed at 1M+ with id, title, channel and observed views (1,011,799 to 2,599,389), pulled 12 Nov |
| 064 search phrase | "where do shooting stars come from", with two ranking videos (`IxDR-dASDNw` 2,546,192; `TuDfZ2Md5x8` 1,098,018); 0 exact-title collisions recorded |
| 064 NASA check | `TOPIC.md` has rows F64.1 to F64.11 with quotes and 11 NASA links. The "every shooting star is sand-sized comet dust" hook is struck through and replaced ("Most shooting stars ... grain of sand to a pea") |
| 065 neighbour pass | present in its `PRE_BUILD_VIDIQ_AUDIT.md` §2b: 8 videos at 1M+ (1,118,503 to 12,769,751) |
| 065 search phrase | "how will the space station fall to earth" returns no suggestions; "what will happen to the iss" / "... international space station" do, with two ranking videos (`cohVHaVMBl8` 2,762,403; `plJVUFErhf8` 1,650,382); 0 exact-title collisions recorded |
| 065 NASA check | `TOPIC.md` has F65.1 to F65.11 with 12 NASA/NOAA/GAO links; the plan-versus-guaranteed-date and South-Pacific-area-versus-Point-Nemo distinctions are both written in |
| Go/no-go sheets, opportunity scores | present for both films |
| `jobs/WIP.json` on the branch | only adds OWB:064 and OWB:065 to the end of `next`; `active` untouched |
| Consolidated record | `jobs/reviews/J2710/REVIEW.md` on PR #853, recommends GO for both as backlog candidates |

Every item the Chief FIX named as missing is now on PR #853. The evidence arrived 23 hours inside
the deadline.

## What this check did not prove (for the J2707 reviewer)

1. **View counts, suggestions and quotes were not re-fetched.** The MacBook run has no web
   access, so the numbers are Gemini's observations as written. The reviewer should spot-check
   two or three neighbours and quotes per film from a machine with web access.
2. **`GAO-26-107805` (June 2026)** carries the "2027 assessment / mid-2029 launch" line for 065.
   It could not be confirmed here. It needs a direct look before any script leans on it.
3. **065 neighbours are broad.** Rows 1, 2 and 6 are about how the station works or was built,
   and rows 7 and 8 are Point Nemo travel films. Strictly on the deorbit itself there are three
   at 1M+: `cohVHaVMBl8`, `plJVUFErhf8` and (re-entry in general) `ivLX9o6Ayl8`. That still meets
   the three-neighbour rule, with nothing to spare.
4. **065's title changed.** Gemini recommends *What Will Happen to the ISS? (NASA's 420-Ton
   Deorbit Plan)* over the J2703 working title, because the working title has no search
   suggestions. The folder slug and `status.json` still carry the old one. The reviewer picks.
5. **065 overlaps a scheduled Short.** `xdurJQcoiGM` (*Where Will the International Space
   Station Crash?*) airs 25 Nov. Gemini reads that as support (Short first, then the long); the
   reviewer should confirm 065's two Short angles stay distinct from it.
6. **Three open PRs are stacked:** #849 (J2703), #850 (J2707 template copy) and #853. #853
   contains the other two. Merging is the Chief's; #849 and #850 become redundant if #853 goes in.
7. `TOPIC_OPPORTUNITY_SCORE.md` is in each film folder twice (root and `11_Upload-Package/`).
   Harmless, but one should go.
8. The scores of 94 and 92 are Gemini's own. The template scripts in `01_Script/` are untouched
   and no spoken line is approved.

Figures that could be compared with what is commonly published by NASA (11 to 72 km/s, 48.5 tons a
day, Halley's 76 years and 2061 return, 3200 Phaethon's 1.4 years, ISS 925,335 lb and 356 ft, the
26 June 2024 deorbit-vehicle award of up to $843M, Point Nemo at 2,688 km from land, Skylab 11 July
1979, Mir 23 March 2001) read as expected. That is a plausibility read from memory, not a source check.

## Commands not run

`jobs.py` is refused in the MacBook's unattended Claude run (show, progress, reopen, done all
"require approval"), and J2707's hold can only be changed by its holder (`macbook`) or the elected
Chief. For whoever can:

```bash
python3 scripts/jobs.py reopen J2707 --agent <holder or chief> --note "J2713: condition met. J2710 done; PR #853 (e23049fde7) carries neighbours, search phrase and ranking videos, collision check and NASA fact rows for 064 and 065. Rule-E decision still to make; see jobs/reviews/J2713/REVIEW.md for what to spot-check." --git
python3 scripts/jobs.py done J2713 --agent <same> --result "Condition met at 2026-11-12T16:05Z: J2710 evidence is on PR #853 (e23049fde7). J2707 reopened for its rule-E decision. Neither topic approved by this check. Record: jobs/reviews/J2713/REVIEW.md." --git
```
