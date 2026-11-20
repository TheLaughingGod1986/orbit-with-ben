# J3012: detached analytics timer wiring

20 November 2026. Continues PR 1011 from 0248664114. Existing progress remains 3/4.

Added the proposed detached shell entrypoint and a bounded Python supervisor connecting the existing serialized
collection and required gate/dispatch phase. Cache readability has a bounded internal-disk fallback. Persistent
record worktrees never silently change location, preserving failed-push recovery. The Mini plist renderer now
stages the analytics service with its original schedule and explicit local credential-file path.

Validation:
- All 66 analytics tests pass together, including the added local-Git orchestration test.
- Eight Mini plist tests pass; shell syntax and whitespace checks pass.
- 13 channel-ratchet, eight email-ratchet and five private-network tests pass.
- The integration test invokes the real worker/session/collection/record helpers with fake collector results and
  three temporary bare remotes. A channel push is deliberately rejected: other records publish, the failed commit
  survives, and a second identical run publishes it. Source checkouts remain unchanged. This is orchestration
  evidence, not an actual TypeScript collector fake-API contract test.
- The first fixture run exposed a missing fixture ignore rule for the dependency symlink. The fixture now carries
  the actual Content Ops `/node_modules` ignore rule; no production ignore rule was relaxed.

No live timer, service, account, credential, queue dispatch, publication or active-engine marker changed. No spend.
The official streak read six; official daily history was not modified. No preceding-day notice sent.

Next: actual collector fake-API acceptance in a refreshed full split; deployed board Contents access; remaining
writer inventory/guards; refreshed private rehearsal. Then seven official clean days, preceding-day notice and
live relay/board/tick/both-worker acceptance. Do not recreate the runbook or mark J3012 done early.

Full baseline split finished at 04:31 UTC on 20 November, source a87cb68bf5: clean true, tests run,
left 0, all eight groups zero (including addresses, credentials and tests), process exit 0. Layout: 2,360
studio files, 12,857 Orbit files, 60 History of Science files, one Field Order History file and one generated
file. This is local baseline verification, not refreshed future-identity or live acceptance. Result and log:
local scratch `/tmp/J3012-0428-split.json` and `/tmp/J3012-0428-split.log`. Official daily history unchanged.
