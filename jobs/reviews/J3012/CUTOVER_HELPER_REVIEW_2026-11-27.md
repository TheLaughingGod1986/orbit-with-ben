# MacBook handoff review — 27 November 2026

J3012 remains 3/4. Codex reviewed owner-authored PR 1385 at 1e08d97548b8ab7e06c73479b9172cf0dee3f2c6, based on main, including all helper code, tests and the machine-local mocked receipt. The existing 34 helper tests passed independently. No live handoff was launched.

CI had one failure: the new helper hardcoded the channel-named worker service label, breaking the existing channel ratchet. The correction reads that identity from the existing shared launcher template; neither the template's service identity nor its settings change. Preparation now also requires hashes for that renderer and template. No ratchet ceiling was raised.

The review also found that production freshness and the exact main/queue hashes did not prove the mandatory clean-root export. The helper now refuses a production commit with parents or absent parent evidence. A regression test proves history-bearing commits refuse before any service operation.

Validation after these changes: 66 tests passed across cutover, launcher, channel ratchet, private-network and email checks. The first test invocation mistyped the launcher module name; the corrected full invocation passed. Diff whitespace check passed. The earlier DRY_RUN.json remains the historical 34-test MacBook receipt, not a receipt for this revised source.

The helper's global freeze and elected authority are explicit attestations in the trusted exact activation command; they are not inferred from a local rehearsal branch. The future coordinator must pin the revised source, preserve private rollback originals, and launch outside its owning process group. The ordinary worker checks its pause between jobs and exits, allowing the recorded owner/group and both slot locks to drain. Live acceptance is still outstanding.

Next: merge the corrected helper after green CI; use a separate bounded MacBook coordination job to stage the private plan and detached supervisor. Do not post an activation until all writers are drained and a fresh parentless production export with the final queue has been verified. No service, pause, engine marker, deployment, production branch, tick store, film or spend changed in this review.
