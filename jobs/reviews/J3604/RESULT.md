# J3604 correction

Views now come only from an exact-window launch reading or a target snapshot within the requested age bounds. The presence of unrelated snapshots no longer makes a wrong-window launch reading scoreable. A latest target snapshot outside the window is also unavailable rather than scored at the wrong age.

Before the fix, both mixed-snapshot regressions returned 123 views (6 h as 48 h; 48 h as 7 d). After the fix, views and both view RSI scores are unavailable, consistent with inspection's unscored-proxy statement. Historical in-window target snapshots still supply views when the latest snapshot omits the target. Exact-window launch readings, including zero values, still succeed for both windows.

Validation:
- `python3 -m unittest discover -s scripts -p test_retention_autopsy.py`: 15 tests, OK.
- `python3 -m unittest discover -s scripts -p test_launch_check.py`: 75 tests, OK.
- `git diff --check`: clean.

Renamed Window 2b to Engaged-viewer AVD proxy; all original media findings retained. No media rewatch, service changes, spend, rules edits, or additional review jobs. Existing J3598 reviews this correction; J3591 remains held.
