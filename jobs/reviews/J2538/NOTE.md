# J2538: the rules check job under a minute. Parked for the Chief (PR #776)

macbook-2, 10 Nov 2026.

## The FIX list of 23:35Z (done in 4ae861f7d)

1. `scripts/uat_outlook.py` is back to main's version. The MacBook checkout is shallow too, so an old-against-new run over every status file would have proved nothing. As the FIX list says, what cannot be shown identical is taken out. `test_uat_outlook` (24 tests) takes 0.1 s without it.
2. `workflow_board.load_tracker` parses the board once per file version and returns a deep copy (`copy.deepcopy`) to every caller. New test: `test_each_caller_gets_its_own_copy_of_the_tracker`.
3. New test `test_every_key_shape_gets_past_the_quick_filter`: every key shape has a sample, each shape's pattern holds one of the quick-filter strings outside any group, class or repeat, and `key_findings` finds each sample through the filter. A new shape with no sample fails.
4. The whole suite was run with the new parallel runner both locally (63.1 s across all 8 parallel groups: `scripts` 62 files / 1,031 tests in 4 groups, `04_Audio/tools` 2 files / 21 tests in 1 group, `00_Brand/Channel-Setup/tools` 6 files / 52 tests in 3 groups) and on GitHub Actions CI (all 1,104 tests pass).

## Job and step times on this pull request's own runs

Before: 2 m 4 s (#765), then 63 s and 101 s after #767.

| Run ID | Head | Cache state | Total job | Checkout | Cache restore | Install media-test tools | Tests (parallel groups) | Post-cache save |
|---|---|---|---|---|---|---|---|---|
| `42916670873` | `ec4a3e88e` | Cold (miss) | **64 s** | 9 s | 1 s | 16 s (`apt-get` + bundle) | 31 s | 2 s |
| `42917472706` | `815f905f8` | Warm (hit) | **47 s** | 9 s | 2 s | 1 s (restored from cache) | 31 s | <1 s |
| `42920801046` | `4ae861f7d` | Warm (hit, FIX list) | **57 s** | 10 s | 3 s | 1 s (restored from cache) | 36 s | <1 s |
| `42921352927` | `f2f98128a` | Warm (hit, FIX list) | **37 s** (40 s elapsed) | 8 s | 2 s | 1 s (restored from cache) | 22 s | <1 s |

All three warm-cache runs (47 s, 57 s, 37 s) finish under the 60 s target (billed 1 minute instead of 2).

## Seen on the way, not part of this pull request

- `test_studio_split` `WholeRun` fails on this Mac locally only, because the sibling `history-of-science` checkout tracks a `.env` file in `02_Video-Projects/004_Whats-Really-Inside-An-Atom/07_Edit-Project/` (three lines: Google project and location names, no key or token; in since 31 Oct). CI has no second checkout, so it does not see it.
- 6 tests in `test_jobs.py` (`MacBookTakesTextJobs` and `Next`) fail locally on this Mac only when CDP port 9223 is open, `/Volumes/data/studio-live` is mounted, and `~/_desk/state/board/board.json` is present (same on `main`).

## What the pull request does

ffmpeg, ffprobe and their libraries kept in the Actions cache, with a safe restore (only missing libraries copied, never overwriting the runner's libc/system libraries) and a fall-back to the package install; `scripts/` tests in 4 processes, tools in 3, audio in 1, with a partition check that every `test_*.py` is in exactly one group; faster code under the slowest tests (`studio_split`, `workflow_board`, `test_channel_ratchet`). No test skipped, weakened or deleted. `core-check.yml` untouched.
