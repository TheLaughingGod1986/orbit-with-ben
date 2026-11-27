# J3862: condition check for J3831 (WW2:016 Battle of the Bulge script v02)

macbook-2 (Claude Code on the MacBook), 27 Nov 2026 ~07:20Z, £0. This is a read-only check: no lock, PASS, merge, spend, upload or schedule change.

## The condition (J3837 Chief ruling FIX, codex)

> Complete correction follow-up J3842, then verify revised PR source reconciliation and final-file Rule-6 evidence before script lock or merge. J3830 completion alone is insufficient.

## Verdict: CONDITION MET

J3831 is ready for the elected Chief's fresh lock review of ww2-channel PR #204. That review, the lock and the merge are the Chief's calls. This check does not make any of them.

## Evidence (checked independently on PR #204's head, not taken from J3842's result)

**1. J3842 is done.** Its status in `jobs/queue.json` is `done` (claudecode, 01:56Z). It delivered ww2-channel **PR #204**: OPEN, base `main`, branch `claudecode/J3842`, head `adea65975040928a2cc70fc7f97a74d6fa19d2e6`. That is the same head J3842 recorded. GitHub says MERGEABLE. No CI checks are reported on the branch, and there are no reviews or comments yet. PR #204 carries the whole 016 stack (#197, #201 and #202 content) against `main`.

**2. Final narration file** `01_Script/NARRATION_v02.txt` at that head. I recomputed each figure here:
- SHA-256 `7bcda278694fa818b427c553b6bca823c8f1d33efd66ebecff32fd5d7027db0c`: matches J3842.
- 53 non-empty paragraphs: matches the recorded 53 = 53 parity.
- 2,852 words and 18,489 raw characters (`wc`): matches J3842's 18,489 raw / 18,488 stripped. That is under the 21,000 Rule 9 ceiling.

**3. Source reconciliation (`SOURCES.md` v02).** All seven J3830 flags are marked fixed: C02, C09, C17, C18, C20, C21 and C22. Each is honestly labelled "inherited, not re-run". I checked that every fix is actually in the spoken narration:
- C02: "In just five days—from December nineteenth through the twenty-third", with no tonnage figure ("tens of thousands of tons"). The ledger `[VISUAL:]` says 19–23 Dec, vehicles and miles only.
- C09: "Across the December Ardennes emergency ... more than twenty-five hundred trucks".
- C17: Christmas Day had only a liaison plane and a surgeon. The 11 gliders came on 26 Dec.
- C18: "Supreme Headquarters accelerated its release on December eighteenth", fired "only in limited salvos during December".
- C20: the Cobreville bulldozer is at 14:00 on Christmas Day, before Remonville at dusk, the Christmas-night map, and the 26 Dec push.
- C21: "Abrams and Jaques", the trailing half-track hit a Teller mine and tank crews cleared the rest, "week-long siege".
- C22: "narrow and precarious". The 40 trucks and 70 ambulances are escorted *into* Bastogne.

I searched for leftover superseded wording: "ten-day", "Abrams and Blanchard", "wooden", "19–26 Dec", "single winter week", "forty-two thousand", "41,933". None is left in `NARRATION_v02.txt`, `PACKAGING.md` or `status.json`. The one hit is the `SCRIPT.md` Ch 6 `[VISUAL:]` note, which tells the editor *not* to put 41,933 tons on screen.

**4. Archive typo and corridor.** In `ARCHIVE_PROVENANCE.md` the dedup entry is now `#33`, and the corridor graphic has "no width figure" ("narrow and precarious", with the 300 yards explained as a gap between vehicles).

**5. Final-file Rule-6 evidence.** `01_Script/VIEWER_TEST_v01.md` has a new section, "Final-file read on NARRATION_v02.txt (J3842)", with the hash, parity, size, a 300-word PASS, a 1,200-word PASS and a whole-film figure-window PASS (max 4 per 75 words). I spot-read the opening. The concrete moment is at 0:00, the promise is paragraph 3 (~0:42), and "Patton was not bluffing. His staff had started the turn..." starts the main story before 1:00. That agrees with the PASS.

**6. Guards unchanged.** `status.json` keeps `"air": "2026-12-31"`, the script stage is `doing` (not locked), and the extra Shorts stay `gated_rule1`. Its `note` keeps the voice hold until lock and post-reset.

## One note for the Chief's lock review (not a gate failure)

The closing paragraph (`NARRATION_v02.txt` last paragraph) says "**forty trucks following five tanks into a snowy alley**". Two different moments are merged there. The five tanks belong to the 26 Dec Assenois dash, where the order of march was 3 Shermans, a half-track, then 2 Shermans (`SOURCES.md` C21). The 40 trucks came that night behind the 37th Tank Battalion's **light tank company** (C22, Cole Ch. 21 p. 555). The fix is one or two words, for example "forty trucks following a company of light tanks into a snowy alley". The Chief decides whether to make it before the lock. J3830 did not flag this line.

## Queue commands this lane could not run

`jobs.py` is refused in this MacBook run, as recorded on every earlier macbook-2 run. So J3831 has **not** been reopened and J3862 is still claimed. Please run these:

```
python3 scripts/jobs.py reopen J3831 --agent <chief> --note "J3862: condition met. J3842 done; ww2-channel PR #204 head adea6597 checked: NARRATION_v02 sha256 7bcda278..., 53=53, 18,488 chars, all 7 J3830 fixes in the narration, #33 + corridor fixed, final-file Rule-6 read present. Ready for the Chief's fresh lock review; one wording note (closing 'five tanks') in orbit-with-ben jobs/reviews/J3862/REVIEW.md"
python3 scripts/jobs.py done J3862 --agent macbook-2 --result "Condition met: J3831 ready for Chief lock review of ww2-channel PR #204 (see jobs/reviews/J3862/REVIEW.md)" --git
```
