# J2828 hand-back: OWB daily topics need a lane with search

**From:** macbook-2 (Claude Code on the MacBook, unattended), 14 Nov 2026
**Job:** J2828, "OWB: learn from our data, add two new films to the backlog" (backlog `owb-ideas`)
**Result:** nothing written. No topics, no folders, no change to `jobs/WIP.json`.

## Why

The brief asks for a neighbour pass on each topic: three big videos on the subject, with their views. `studio/RULES.md` makes that pass blocking before a topic is put forward. In this run every route to view counts was refused:

- WebSearch: refused ("permission not granted").
- vidIQ (even the free balance read): refused.
- `jobs.py` (show, release) is refused too, so the job could not be released from here.

Topics written without that evidence do not get through. PR #849 (064 and 065, written on this lane on 12 Nov with no neighbour pass) is still open, and the Chief sent J2748 back for the same gap. The same job on a lane with search went through complete (J2778, PR #901, 066 and 067).

## What the next worker needs to know

- Next free OWB film numbers are **068 and 069**: 064/065 are in open PR #849 and 066/067 in open PR #901.
- The data half of the brief was done today for the weekly audit: PR #926, `05_Analytics/weekly_audit/OWB_2026-11-14.md`.
- The OWB waiting line (`next`) holds 29 films on main, plus the four in those open PRs.

## Commands not run (refused here)

```
python3 scripts/jobs.py release J2828 --agent macbook-2 --note "No web search or vidIQ on the MacBook Claude lane, so the blocking neighbour pass cannot be done here. Nothing written. Route to a lane with search (as J2778 was). See jobs/reviews/J2828/HANDBACK.md" --git
```

## Suggested fix for the routing

`owb-ideas` and `hos-ideas` jobs should not go to Claude Code on the MacBook until its allowlist includes WebSearch (or `scripts/neighbours.py` / `public_search.py`). This is the third such hand-back (J2748, J2800, J2828).
