# J3012 rehearsal evidence — 18 November 2026

Baseline full split result: see split-2026-11-18.json. This reports the split parser result, not an independently retained full unittest transcript. Source history is not imported.

Future-identity checks:

```text
channels:
FAIL: test_the_board_repo_and_its_github_name_come_from_the_home_channel (test_channels.StudioOwnRepo.test_the_board_repo_and_its_github_name_come_from_the_home_channel)
Ran 70 tests in 1.406s
FAILED (failures=1)
targeted:
FAIL: test_clones_urls_and_ports_come_from_the_channel_files (test_macbook_worker.AsksTheChannelLoader.test_clones_urls_and_ports_come_from_the_channel_files)
FAIL: test_the_names_it_runs_under_are_todays (test_owb_thread_post.TheOldNameIsTheSameTool.test_the_names_it_runs_under_are_todays)
Ran 164 tests in 12.456s
FAILED (failures=2, skipped=4)
```

Zero address/credential findings on 2345 export files after isolation changes (including generated test cache files; only tracked files are published). No live services or credentials changed. Rehearsal is not a cutover PASS.

Published isolated snapshot: [studio rehearsal/j3012](https://github.com/TheLaughingGod1986/studio/tree/rehearsal/j3012), commit `534cf0f70852e06414cbe39f6a01efe9024c8a91`. One parentless commit; no source Git history.

The fresh export initially omitted 49 tracked images under ignore rules, including board icons. Those exact existing PNG/JPG files were explicitly restored to the rehearsal index. No new video/audio was added. Active workflow YAML lives under docs/rehearsal-workflows, so the rehearsal cannot start scheduled CI.


## Independent resume verification, 18 November

Fetched the published rehearsal into a fresh scratch clone and verified root SHA
`534cf0f70852e06414cbe39f6a01efe9024c8a91` with zero parents. Re-scanned all 2223 tracked files:
zero addresses, zero key findings, zero active workflow YAML and zero video/audio files.
The existing runbook PR #1011 had one passing CI check and one skipped check before this update.

Ran `test_channels`, `test_macbook_worker`, and `test_owb_thread_post` with explicit studio/Orbit/HOS checkout
environments: **168 tests, four failures, exit 1**. Three reproduce the future-identity failures above. The fourth,
`test_channels.Films.test_each_channels_numbers_and_uploads_register_are_asked_for_by_slug`, fails because
HOS snapshots are not yet in the real HOS checkout. This probe uses today's channel checkouts rather than the
split's isolated sibling views, so this is a layout prerequisite, not an additional demonstrated engine defect.
An initial run without explicit checkout environments stopped during import because the Orbit settings cache
was absent; no tests ran in that attempt. Neither result is a cutover PASS.

Official daily evidence now has five consecutive zero days (14–18 November); latest source `58b6cf14e8`,
18 November 07:54Z, tests run, all eight groups zero. The earlier rehearsal evidence remains historical and is
not replaced with the daily snapshot. No live service, token, channel content or production branch was changed.


## Adapter continuation, 18 November 15:20Z

Updated the existing PR from `b83f93f3b7` in a clean, detached worktree. No live service, repository identity,
thread configuration, deployment or channel file was switched.

- Thread reads and posts now use `thread.json.repo` even when the engine moves to `studio`. Missing/empty repo
  retains the legacy engine fallback. Cursor, prefix and override names are unchanged. Chief election uses
  the same thread API; board_check already reads the explicit repository.
- Channel-loader and MacBook URL-map tests now check the registry instead of assuming the engine is Orbit.
  The clone-map test is outside the class that deliberately pins the legacy home-channel fixture.
- Legacy `/api/ref` delegates to the authenticated data handler, preserving the ref response shape and applying
  `BOARD_DATA_REPO`, sign-in and private cache rules. No deployment was made.
- Current-layout validation: 70 loader + 85 worker + 15 thread tests pass. Relay suite: 113 pass.
  Board-data suite: 25 run, 21 pass, four browser cases skipped. Site build passes.
- Independent future-identity targeted validation: **170 tests, exit 0**, with routed analytics in isolated
  sibling views, no home channel, studio GitHub identity, and explicit engine/channel checkout environments.
  This resolves the earlier 168-test compatibility failures without moving live analytics.
- First broad split started before the worker-test correction was copied and reported one worker-test failure.
  It is a superseded intermediate result, not a daily streak entry. The completed targeted probe uses the correction.
- Remaining before cutover: launcher/bootstrap and CI adaptations, exact deployed board credential access,
  old-entrypoint single-writer safeguards, seven official clean days and prior-day notice. Live relay/publish/tick
  acceptance is still outstanding. The published rehearsal root remains historical, not a deployable snapshot.
