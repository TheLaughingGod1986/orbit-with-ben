# J1932: condition check for J0979 (Short cut from a locked long)

Reviewer: claudecode (Mini worker, review lane, rule H). 12 Nov 2026, about 06:40Z. £0, nothing uploaded or scheduled.

## Verdict: FIX (keep J0979 held). One of the three inputs is still missing.

J0979 is held (J2173, 683e49e96a) until 032 Titan has (1) its picture complete, (2) its own score bed and (3) an approved long master. It would then assemble the 032 Test A opening Short (VO s01-s05, 0.060-31.580 s) as the reserve for Fri 27 Nov 11:30Z.

| Input | State now | Evidence |
|---|---|---|
| Locked voice | Met | `status.json` vo done, lock `titan_landing_vo_v02b`; J1753 done under Ben's 4 Nov rule. Stem on studio-live re-hashed today: wav sha256 `55232eeb...5301abc5`, same as the lock record. |
| Picture | Met | J2089 done 4/4; J2378 Chief PASS (KEEP) on the picture package (7920d0f777); `status.json` picture done. |
| Score bed | Met | `05_Music/titan_score_bed_v01.mp3` on studio-live (sha256 `02c7d958...9dab8f9e`), `music_gate_bed_v01.json` verdict PASS, no fails. |
| Approved long master | **Not met** | Master v02 exists (J2436; re-hashed today, sha256 `51986972...c80ed073`, matches J2436 and the J2477 brief). Its review J2477 is still open and unclaimed, has no REVIEW.md, and no `awaits_ben` entry exists for 032. `status.json` edit is `review`, not done. Ben has not watched it. |

So J0979 stays blocked. It is not reopened.

## Notes for whoever restarts J0979

- The J2173 cut still fits master v02. `FIRST30_PLAN.md` (J2435) kept the locked words and their timings for s01-s05 (0.16-31.58 s) and re-cut the picture only; the preview questions start at 32.76 s. The Short must be cut from v02 (or whichever version is approved), not v01, and its EDL re-read against that version's cut manifest.
- Slot. Fri 27 Nov 11:30Z is held by AR1 v06 `93JL_IK57EM` (Private, scheduled). J2173 allows this Short there only as an approved replacement, never as a second Short that day, and gave a watch-pack date of 20 Nov 18:00Z. J2477 is due 14 Nov 18:00Z and Ben's watch target is 16 Nov, which leaves about four days. Whether the reserve is still wanted for 27 Nov, or moves to a later free slot, is the Chief's call once the master is approved; nothing here changes a schedule.
- 032 carries two Shorts (J2147 plan: go-public-day Short plus this Test A opening). No third Short and no second Test A.
- 029 reserve v01 stays shelved (J1042).

## What was done

`jobs.py wait J0979 --type dependency --recheck J1932`, next check 2026-11-14T18:30Z (just after J2477's deadline). J1932 closed with this verdict.
