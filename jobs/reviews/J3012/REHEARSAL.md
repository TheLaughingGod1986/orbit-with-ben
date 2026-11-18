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
