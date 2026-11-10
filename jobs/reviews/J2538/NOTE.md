# J2538: the rules check job under a minute. Parked for the Chief (PR #776)

macbook-2, 10 Nov 2026. This note is in the branch because `gh pr edit`, `gh pr comment`, `jobs.py` and `owb_thread.py` are refused on the MacBook.

## The FIX list of 23:35Z (done in 4ae861f7d)

1. `scripts/uat_outlook.py` is back to main's version. The MacBook checkout is shallow too, so an old-against-new run over every status file would have proved nothing. As the FIX list says, what cannot be shown identical is taken out. `test_uat_outlook` (24 tests) takes 0.1 s without it.
2. `workflow_board.load_tracker` parses the board once per file version and returns a deep copy to every caller. New test: `test_each_caller_gets_its_own_copy_of_the_tracker`.
3. New test `test_every_key_shape_gets_past_the_quick_filter`: every key shape has a sample, each shape's pattern holds one of the quick-filter strings outside any group, class or repeat, and `key_findings` finds each sample through the filter. A new shape with no sample fails.
4. The whole suite ran with the new runner on this pull request's own runs and passed.

## Job times on this pull request's own runs

| Head | Rules check job | ffmpeg cache |
|---|---|---|
| ec4a3e88e | 64 s | empty (package installed) |
| 815f905f8 | 47 s | first run that could use it |
| 4ae861f7d | 57 s (run 42920801046) | not read |
| the commit adding this note | see the PR's checks | not read |

Before: 2 m 4 s (#765), then 63 s and 101 s after #767.

## Not done

- Step times. `gh run view` is refused on the MacBook, so the per-step times, and whether each run hit the cache, are for the Chief to read.
- The whole suite was not finished locally: tools 52 OK, audio 21 OK, the scripts folder was stopped at the time cap. CI ran all of it.
- J2538 is still claimed by macbook-2. The command to park it:
  `python3 scripts/jobs.py block J2538 --agent macbook-2 --reason "parked for Chief: PR 776, check green; FIX list 1-3 done, 4 needs the step times read" --git`

## Seen on the way, not part of this pull request

`test_studio_split` WholeRun fails on this Mac only, because history-of-science tracks a `.env` file in `02_Video-Projects/004_Whats-Really-Inside-An-Atom/07_Edit-Project/` (three lines: Google project and location names, no key or token; in since 31 Oct). CI has no second checkout, so it does not see it.

## What the pull request does

ffmpeg, ffprobe and their libraries kept in the Actions cache, with a fall-back to the package install; `scripts/` tests in 4 processes, tools in 3, audio in 1, with a check that every `test_*.py` is in exactly one group; faster code under the slowest tests (studio_split, workflow_board, test_channel_ratchet). No test skipped, weakened or deleted. `core-check.yml` untouched.
