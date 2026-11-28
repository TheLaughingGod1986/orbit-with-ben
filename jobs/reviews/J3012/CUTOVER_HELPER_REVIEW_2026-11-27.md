# MacBook handoff review — 27 November 2026

J3012 remains 3/4. Codex reviewed owner-authored PR 1385 at 1e08d97548b8ab7e06c73479b9172cf0dee3f2c6, based on main, including all helper code, tests and the machine-local mocked receipt. The existing 34 helper tests passed independently. No live handoff was launched.

CI had one failure: the new helper hardcoded the channel-named worker service label, breaking the existing channel ratchet. The correction reads that identity from the existing shared launcher template; neither the template's service identity nor its settings change. Preparation now also requires hashes for that renderer and template. No ratchet ceiling was raised.

The review also found that production freshness and the exact main/queue hashes did not prove the mandatory clean-root export. The helper now refuses a production commit with parents or absent parent evidence. A regression test proves history-bearing commits refuse before any service operation.

Validation after these changes: 66 tests passed across cutover, launcher, channel ratchet, private-network and email checks. The first test invocation mistyped the launcher module name; the corrected full invocation passed. Diff whitespace check passed. The earlier DRY_RUN.json remains the historical 34-test MacBook receipt, not a receipt for this revised source.

The helper's global freeze and elected authority are explicit attestations in the trusted exact activation command; they are not inferred from a local rehearsal branch. The future coordinator must pin the revised source, preserve private rollback originals, and launch outside its owning process group. The ordinary worker checks its pause between jobs and exits, allowing the recorded owner/group and both slot locks to drain. Live acceptance is still outstanding.

## Live handoff blocker

The current helper writes success/failure only to a private MacBook file and exits after installation with the worker pause retained. Its runbook says the Mini Chief resumes it, but existing SSH is unavailable and the paused ordinary worker cannot claim a follow-up. The Mini therefore has no implemented way to observe the remote outcome or resume the slots. Local result paths are useful rollback evidence, not a cross-machine control route. Do not launch this helper for live migration yet.

Complete the existing-thread result and resume/recovery protocol before the coordination child. It must report only a bounded sanitized receipt, preserve the exact activation identity, accept an explicit fresh elected-Chief resume command only after successful installation, remove only the pause created by this migration, and retain the pause on failure. A detached control process needs a bounded lifecycle and a verified recovery route if its deadline expires. Do not silently resume a stale engine or add SSH/sign-in requirements. Test successful and failed delivery, stale/edited/untrusted commands, exact pause ownership, timeout and both-slot resumption with all external effects mocked; obtain machine-local evidence through the installed worker before the live drain.

Next: merge the corrected helper as preparation after green CI, then finish this bounded control gap. Do not post an activation until that review passes, all writers are drained and a fresh parentless production export with the final queue has been verified. No service, pause, engine marker, deployment, production branch, tick store, film or spend changed in this review.
