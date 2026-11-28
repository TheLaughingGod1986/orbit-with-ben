# J3012: actual analytics collector acceptance and spend-writer guard

20 November 2026. Continues PR 1011 from 706c2da19c. Existing progress remains 3/4.

## Actual collector coverage

- Five CLI tests execute the real TypeScript snapshot/report scripts with the actual registry loader in isolated
  detached layouts. They cover all three channel destinations, private Analytics tables, Field Order detail/reads,
  the engine-owned dashboard, offline reporting, missing history, wrong manifest identity, a failed channel without
  suppressing successful channels, and an unconfigured Field Order channel making no requests.
- Fake fetch responds only to known OAuth/Data/Analytics endpoints and never delegates to real fetch. Raw Node
  network connections also refuse. Child environments contain only fixture credentials, never the live environment.
- A separate integration test runs the real Python timer worker, collector commands (including Node env-file
  loading), report builder, session lock, registry resolution and per-owner Git records with four temporary bare
  remotes. Local remote identities replace GitHub identity validation only inside this test. It verifies the changed
  paths in each pushed commit and that all source checkouts remain clean.
- Gate/dispatch and board publication are excluded from the actual-collector integration fixture and covered by
  the existing separate suites. This is not one live end-to-end timer run or a deployed credential proof.
- The five CLI checks and the actual-collector/Git integration also pass from the fresh full split export after
  linking the existing installed Content Ops dependencies. Python-only split CI may skip the integration test when
  those dependencies are absent; the explicit run here did not skip it.

## Validation

- 232 application tests and eight lock pretests pass; typecheck and lint pass.
- 67 analytics Python tests pass, including actual collectors and local Git.
- 73 spend-reader/writer tests, six engine-guard tests and nine service-renderer tests pass.
- 13 channel-ratchet, eight address-ratchet and five private-network tests pass. Core lock: 56 files, unchanged.
- Frozen baseline split at source 1ad93b8c40: clean, tests run, exit 0, left 0, all eight groups zero.
  Layout: 2,363 studio files, 12,857 Orbit files, 60 History of Science files, one Field Order file and one generated
  file. Local result: Mini scratch `J3012-collector-final-1120.json`; layout: `J3012-collector-final-1120/`.
  This is baseline identity, before the subsequent spend-writer guard. No official daily-history row was written.
- Future-identity full suite with the spend-writer guard: 1,450 tests, six skips, one failure in
  `test_a_stuck_mini_repairs_itself_once_and_says_so`. It used real scratch-volume free space after a fake repair;
  the SSD was down to 204 MB, so the throttle path correctly refused work. The test now supplies deterministic
  110/25,000 MB readings and explicit throttle/hard-floor settings. Both resident and future-layout relay suites
  then passed all 113 tests. The entire 1,450-test suite has not been repeated after this fixture-only correction.
- Low scratch space also exposed that ordinary relay tests could start the real offload helper. Their setup now
  sets its threshold to zero; the dedicated offload test overrides it and uses its own fake helper. Observed
  real-helper attempts failed on filesystem permissions; fake-helper reports are not real moves. This fixture
  isolation change passes the final future-layout relay recheck: 113 tests, exit 0. The retained log is
  `J3012-collector-final-1120/future-relay-isolated.log` under Mini scratch.
- Removed only this run's superseded generated baseline export, keeping its JSON/log and the final export;
  scratch free space rose to 830 MB. Check scratch capacity before another large rehearsal.

## Writer inventory finding and fix

Read installed Mini plist labels and executable names only; no environment values were printed or committed.
The prepared service renderer covered relay, publisher, Buffer and analytics, but omitted AI-spend daily.
Added its exact installed `ai_spend_daily.py --git` command to the proposal renderer. Schedule/log/environment
retention is tested, along with literal invocation in paths containing shell-special characters.

Added retired-engine refusal before both spend CLIs and before the imported ledger append operation. A new test
proves a refused append creates no ledger directory and invokes no Git. This remains inactive until the separately
gated activation marker is installed. Other ledger exporters and local worker/watchdog wrappers still require audit.

## Next

Resume this PR, not a replacement runbook. Probe private studio Contents using the deployed board credential;
finish the remaining writer inventory/guards, both-machine service inventory and refreshed private remote
rehearsal. Official history remains six clean days through 19 November in the inspected source. Require seven
official days, preceding-day notice and the actual relay/board/tick/both-worker acceptance before marking done.
No live service, marker, repository identity, credential, public video or schedule changed. No spend or Ben action.
