# Studio exact-cut progress correction

Apophis appeared as Long while its recorded watch asset is a Short v13a. Its seven completed project milestones included AR cohort work, so78% did not establish completion of that cut.

The tracker now conservatively identifies Short watch files or explicit watch format, retaining stable keys/check IDs, links, review state and production records. Known YouTube video identities retain their recorded format. Forecasts keep mixed project records as projectHistory; the cut has no borrowed percentage or ETA. A canonical milestoneScope={type:cut,format:short,version:v13a} may restore its own milestones only when the card/watch version and format agree. No marker or completion was added to production data by this change.

The frontend handles both cached legacy and newly published payloads. Overview and Videos show Cut progress unconfirmed and identify Related work; detail keeps original project milestones collapsed and available. Ready, changes, scheduled and published workflows retain their existing behavior. Ranking does not treat borrowed project milestones as evidence of approaching QA.

Validation executed: JS syntax/unit regression checks; focused tracker/forecast unit tests; full scripts suite; new Playwright mixed-scope tests at375/390/430/768/1280px, cached/new publisher refresh with expanded history retained, format filter, deep links, all five tabs, no overflow/page errors/writes. Existing V2 UAT and delivered-cut browser suites passed at all five widths, including intercepted approval/changes actions. Core/rules/STATUS/diff checks passed. Screenshot artifacts remain local in /workspace/scratch/cut-scope-qa; no production media or signed watch URLs are published in this PR.

Page and data rollout are separate. The fallback fixes legacy board payloads immediately when the page is deployed; the normal Mini publisher emits the new structured scope afterward. Source records, approvals, jobs, dates, credits, watch assets and YouTube/Buffer behavior remain unchanged.
