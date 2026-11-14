# J2800 hand-back: not done on the MacBook

**Job:** HOS daily topics (learn from our data, add two new films to the backlog).
**Worker:** macbook-2 (Claude Code, unattended), 14 Nov 2026 about 02:20Z.
**Result:** nothing written. No topic, folder, WIP line or review job was made.

## Why

The brief needs three things this lane cannot do in an unattended run:

1. **A neighbour pass with views for each topic.** Web search, `scripts/neighbours.py` and `scripts/public_search.py` were all refused in this run (checked again today). vidIQ search costs credits, so it was not used ("spend nothing").
2. **Queue each topic's rule-E review job.** `jobs.py add` is refused.
3. **Close or release the job.** `jobs.py release`, `done`, `progress` and `studio_thread.py post` are refused.

The same job on 13 Nov (J2748, PR #881 and history-of-science PR #572) was written from this lane without items 1 and 2, and the review sent it back FIX for exactly those: no three-video neighbour passes, no saved public-search evidence, no rule-E review jobs. Writing two more topics the same way would only add two more PRs to fix. J2748's FIX is still open, and 102 and 103 are not yet in `next_hos`.

## What the Chief should do

- Release J2800 and send it to a lane with search (a Mini worker):
  `python3 scripts/jobs.py release J2800 --agent macbook-2 --note "needs search for the neighbour pass; see jobs/reviews/J2800/HANDBACK.md" --git`
- Keep the `hos-ideas` backlog item off the MacBook's Claude lane until web search or `neighbours.py` is on its allowlist. The J2748 FIX has the same need.
- The next free HOS film numbers are 104 and 105 (102 and 103 are taken by PR #572).

Nothing was spent. No Studio, NAS or history-of-science change.
