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
