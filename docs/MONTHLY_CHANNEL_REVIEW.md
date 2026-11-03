# Monthly channel improvement reviews

Ben's standing instruction, 3 November 2026: use channel performance every month to improve the films, rather than simply reporting numbers.

## Schedule and delivery

The existing Mini relay calls `refill.py` on every cycle. Two calendar items in `jobs/backlog.json` queue on the first of each month at 09:00 Europe/London, after the daily snapshot. Each covers the previous complete calendar month. If the machine misses that time it catches up on its next refill; this is a queue time, not a guaranteed finish time. Each report has a target of the third at 09:00 London. The first run catches up October 2026. No separate scheduler service or production database.

One job per channel and reporting month, including while production queues are full. Failed work is resumed through the same job; a blocked old report must not prevent the next month's review. Run records remain in the existing queue. A report is not complete until a readable artifact and Chief handoff exist. Publishing private analytics to a public repository still requires the established permission; never retry a previously rejected publication implicitly.

## Required analysis, separately for each channel

1. Inventory evidence: source locations, retrieval dates, reporting windows, coverage and missing data. Inspect all available video and channel metrics, including traffic sources, impressions, subscribers and audience signals where recorded. Do not imply unavailable data was analyzed.
2. Scorecard: views, views per video, watch hours, average view duration, average percentage viewed, retention drop-offs and impressions CTR. For Shorts include stayed-to-watch and replay signals where available. Separate Shorts, long films and compilations; compare like lengths and publication ages. Separate monthly performance of the whole catalogue from new-upload cohorts. Use the same elapsed measurement window when comparing uploads.
3. Compare with the previous month, show absolute values and changes, account for upload volume, traffic mix and small samples. Weight CTR by impressions and duration by views where appropriate; never average percentages blindly. Lifetime CTR snapshots do not establish monthly CTR. Missing figures are unavailable, not zero. Avoid causal claims unsupported by an experiment.
4. Identify what worked and what failed: topics, packaging, openings, pacing, length, visual clarity and endings, supported by specific video IDs and evidence. Note external/distribution effects and uncertainty.
5. Review last month's experiments: hypothesis, actual changes, measurement window, results and retain/iterate/stop decision. Respect existing experiment end dates and locked Test & Compare variants.
6. Recommend at most three prioritized experiments for the next month, plus material urgent corrections. Each needs evidence, hypothesis, channel/format, exact change, owner/required reviewer, baseline, success metric, target, minimum evidence window/sample caveat, review date and stop condition. Balance CTR with retention and watch time; do not optimize clicks at the expense of delivery.
7. Deliver an executive readout, per-video appendix, evidence index and action register. Keep reports in the approved private analytics handoff area by default; use `05_Analytics/monthly_audit/<channel>/<YYYY-MM>/` only when publication permissions permit. Link the readable report in the Chief review task. On approval create linked implementation jobs in the existing queue and reference their IDs in the action register; next month's report checks their results. The Chief must explicitly record a decision on recommended changes; a report alone is not a completed improvement loop.

## Failures and permissions

Missing credentials, stale snapshots or inaccessible retention data produce a partial report with explicit gaps and a linked recovery job, never invented metrics. The scheduled analyst uses the existing capability-aware routing. Recommendations do not automatically authorize spend, uploads, visibility/date changes, production-rule rewrites or live packaging changes. Ben and Chief approval gates remain unchanged.
