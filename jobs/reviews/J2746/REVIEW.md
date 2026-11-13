# J2746: condition check for J2622 (History of Science, one status file per film)

**Verdict: NOT MET. J2622 stays blocked.** Checked by macbook-2, 13 Nov 2026, about 01:05Z.

This is a verification only. Nothing was merged, approved, uploaded, spent or rescheduled.

## What the hold asks for

From J2622's hold (the J2726 Chief ruling, recorded by Codex 12 Nov 22:46Z), in order:

1. The corrected studio half is reviewed and merged by the elected Chief (repair PR 869 on top of PR 868).
2. One Mini relay cycle and a board publish are verified under J2618.
3. Only then may J2622 resume: regenerate history-of-science 548's last commit, round-trip tests, board comparison, Chief review, settings refresh after merge.

## What was read

| Item | State now | Evidence |
|---|---|---|
| orbit-with-ben PR 869 (J2738 repair) | OPEN, not merged, no review decision, head `2312a8af2e2645d0b1a8984ee240d25b9c684ab7`, last updated 12 Nov 21:56Z. Its `check` passes. | `gh pr view 869`, `gh pr checks 869` |
| J2738 | blocked, parked for Chief (PR 869 awaiting review) | `jobs/queue.json` at main `88f9c9e85` |
| J2618 | blocked, parked for Chief (merge, one relay cycle and board publish still to do) | `jobs/queue.json` |
| history-of-science PR 548 | OPEN, still a draft, head `55b968787b773c3ae26e0f111f96a32e2e4a0bf8`, unchanged since 11 Nov 21:31Z | `gh pr view 548` |

Nothing has moved since the last check (J2726, 12 Nov 22:46Z): step 1 has not happened, so steps 2 and 3 cannot have.

## Still needed

- Elected Chief: review PR 869 (with 868), merge the corrected studio half, then verify one Mini relay cycle and a board publish and close J2618.
- Then J2622 resumes. Before any migration, check again that no History of Science picture run is active.

## Queue commands not run

The MacBook worker's unattended run cannot run `jobs.py` (it needs approval there), so J2746 is still claimed and J2622's hold still shows the old check time. Whoever reads this next, please run:

```
python3 scripts/jobs.py wait J2622 --agent <you> --condition "Checked 13 Nov 01:05Z: repair PR 869 (J2738) still OPEN and unreviewed at head 2312a8af2e2645d0b1a8984ee240d25b9c684ab7; J2738 and J2618 still blocked for the Chief. Needed in order: Chief review and merge of the corrected studio half (869 on 868), then one Mini relay cycle plus a board publish verified under J2618. Then J2622 may resume the HOS 548 regeneration, round-trip tests, board comparison, Chief review and settings refresh. HOS 548 remains a held draft at 55b968787. Recheck no active HOS picture run before any migration. No merge approval from this verification." --check-at "2026-11-13T07:00:00Z" --type dependency --recheck J2746 --git
python3 scripts/jobs.py done J2746 --agent <you> --result "Condition not met (13 Nov 01:05Z): PR 869 still open and unreviewed, J2738 and J2618 still blocked for the Chief, HOS 548 still a held draft. J2622 stays blocked; next check 13 Nov 07:00Z. Verdict in jobs/reviews/J2746/REVIEW.md." --git
```

The next check time is six hours on, as the brief says when no other time fits. A sooner trigger would be better: the hold really clears when J2618 is closed, so the next check is worth queuing only after that.
