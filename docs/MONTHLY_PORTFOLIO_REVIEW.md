# Monthly portfolio review

J3490 implements Ben's 24 November portfolio plan. The first review is Monday
4 January 2027 at 09:00 London, then the first Monday monthly. The existing
refill job creates one review per report month, even when production fills the
queue, and catches up after a missed tick. No new daemon or paid service.

Read the board's Monthly channel scorecard (Overview / fuller Channels page).
Rebuild locally if needed with `channel_scorecard.section(root, now)`; production
uses the board publisher's fresh main worktree, catalogue and queue. Report the
specified complete calendar month against the preceding month. Save a dated
report under `05_Analytics/portfolio_reviews/`. Give Ben the numbers, coverage
limits, active tests, protection dates and these recommendations in plain words:

- Keep four Shorts only when the monthly publication cohort's median views rises
  and net channel subscribers per 1,000 Shorts views is at least one. Otherwise
  recommend two or three. This ratio is a channel conversion proxy, not claimed
  attribution of subscribers to Shorts. A channel with no Shorts keeps its own
  schedule.
- Rank all channels by (net subscribers + estimated public-long watch hours) /
  films published. Missing measures or tied extremes mean no ranking verdict.
  Recommend the lowest halves next month's schedule, moving effort to the top.
  Recommend stopping new films only on a second consecutive eligible lowest
  monthly review. Nothing is deleted. Check the previous saved review before
  endorsing that second-strike recommendation, including any Ben decision.
- Tests come first: never recommend either a Shorts cut or a channel cut while
  its own plan test is inside its read window. Show film, day of read, views,
  keep/drop bar and finish date. Actual linked publication dates override the
  plan date; unlinked views are unknown. Explicit portfolio protection dates in
  studio/plan.json remain in force (Orbit 14 February; HOS 18 February), even if
  other plans move their six-week review. Report the inconsistency to Chief;
  do not silently shorten the protection. Field Order History's film-20 check
  still stands.

Change no schedule, film, rule or plan. These are recommendations for Ben; record
his decision before implementation. Post the report through studio_thread.py
from a file and mark the review job done with a link to the report.

## Measurement contract

Daily channel Analytics must cover every date for net subscribers / total views.
Format totals subtract per-video lifetime Analytics at exact reporting-month
boundaries, using only public films published by month end. Public-long hours
are an estimate, never qualified Earn hours. Missing boundaries or per-film rows
produce U with a reason, never zero. Published film counts use the month-end
reporting snapshot catalogue. Typical views are the median views by month end
of public films published that month, not today's lifetime totals; film ages
within these cohorts differ. Return per film includes longs and Shorts in its
denominator. No rolling 28/30-day baseline is relabelled as a calendar month.
