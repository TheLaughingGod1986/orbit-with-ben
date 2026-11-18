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
