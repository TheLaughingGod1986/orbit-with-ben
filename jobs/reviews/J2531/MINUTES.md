# J2531: check minutes, before and after

MacBook worker, 10 Nov 2026. Window: 3 Nov 20:30Z to 10 Nov 20:30Z, `origin/main`, first-parent.

**Answer: the target is not reached.** The change cuts push runs from about 5,900 minutes a week to about 105, but
pull requests alone used at least 635 minutes in the same week (about 2,700 a month). The estimate after the change
is about **3,400 minutes a month** against a target of 1,200 and a free cap of 2,000. See "What is left".

## How this was counted (read this first)

The brief asks for a count from the workflow runs. **This run could not read them**: `gh run list` and `gh api`
need approval on the unattended MacBook. So:

- **Push runs are derived from `git log`**, by matching each commit's files against each workflow's path list. One
  run per commit is an upper bound (a push of several commits starts one run). Not measured: failed or cancelled
  runs, re-runs.
- **Pull-request runs are a lower bound**: `gh pr list --json statusCheckRollup` shows only the latest head of each
  pull request, and the list stopped at its limit of 300 pull requests. Earlier pushes to the same pull request
  are not counted.
- **Minutes per run** are the real durations of those pull-request runs, each rounded up to a whole minute.

Whoever has `gh run list` (the Mini, the Chief) should replace the tables with the true count:
`gh run list --limit 1000 --created ">=2026-11-03" --json workflowName,event,createdAt,updatedAt,conclusion`.
`count_minutes.py` in this folder does the push count in one go (it was written here but not run: running it needs
approval too; the figures below came from the equivalent `git log -- <paths> | wc -l` calls).

## 1. The 7 days

Commits on main: **4,501**.

| What the commit changed | Commits | Share |
|---|---|---|
| Only data: `jobs/**`, `JOBS.md`, `STATUS.md`, `02_Video-Projects/*/status.json`, `05_Analytics/**` | 4,306 | 95.7% |
| Something else, landed by a merged pull request | 127 | 2.8% |
| Something else, pushed straight to main (mostly film records, gate reports, upload records) | 68 | 1.5% |

Inside the data commits: 4,124 touched the queue (`jobs/`, `JOBS.md`), 480 touched `STATUS.md` or a `status.json`,
183 touched `05_Analytics/` (28 of them the board's film notes).

Measured on pull-request heads (lower bound, see above):

| Workflow | Runs | Average | Longest | Billed minutes | Minutes a run |
|---|---|---|---|---|---|
| Studio core check | 298 | 15 s | 62 s | 299 | 1.0 |
| Rules check | 136 | 109 s | 2,169 s | 325 | 2.4 |
| Content Ops checks | 7 | 54 s | 66 s | 10 | 1.4 |
| Notes check | 1 | 12 s | 12 s | 1 | 1.0 |
| **Pull requests, total** | 442 | | | **635** | |

Push to main, before the change (derived, upper bound):

| Workflow | Runs | Of them data-only | Minutes |
|---|---|---|---|
| Studio core check (every push) | 4,501 | 4,306 | 4,501 |
| Rules check | 571 | 479 | 1,370 |
| Notes check (it began on 10 Nov; counted as if live all week) | 29 | 28 | 29 |
| Content Ops checks | 5 | 0 | 7 |
| **Push, total** | 5,106 | 4,813 | **5,907** |

Week before the change: about 6,540 minutes. A month: about **28,000**.

## 2. What changed

All four workflows:

- **Once a day on main** (`schedule`, 04:40 UTC) and a manual button (`workflow_dispatch`). A scheduled run ignores
  the path lists, so each workflow's whole suite runs daily whatever was pushed.
- **A merged pull request is not run a second time.** The job has an `if` that skips a push whose head commit is a
  pull-request merge (message starts `Merge pull request #` or holds `(#`). A skipped job uses no runner and no
  minutes. Nothing in the steps changed.
- **A newer push to a pull request cancels the older run of that pull request** (`concurrency`). Runs on main are
  never cancelled.

| Check | On data commits before | Where it runs now |
|---|---|---|
| `core_sync.py check` + `test_weekly_public_audit.py` (Studio core check) | every push | every pull request; push to main that changes anything other than data; daily |
| `studio.py status --check` (Rules check) | every `STATUS.md` / `status.json` push | pull requests that touch them; daily |
| `sync_rules.py --check` and the three test folders (Rules check) | every `STATUS.md` / `status.json` push | pull requests and pushes on the same code paths as before; daily |
| `notes_push.py --check` (Notes check) | every push of `film_briefs.json` | `scripts/notes_push.py` runs the same checks before it pushes (already the case); pull requests that touch the notes; daily |
| Content Ops (typecheck, lint, test) | never ran on data | unchanged paths; daily |

A data-only commit now starts no workflow. No test was removed, skipped or weakened; no repo setting was touched.

**Three things the Chief should weigh before merging:**

1. **The merge test is by commit message.** A commit pushed straight to main whose message holds `(#611)` is
   skipped as if it were a merge, and is then covered only by the daily run. And the `if` trusts that the pull
   request's head passed; it does not look it up (looking it up would cost the minute it saves). If branch
   protection does not require the checks, a red pull request merged anyway is caught only by the daily run.
2. **`STATUS.md` drift and a bad notes file are now found within a day, not within minutes**, unless the writer
   checks first. `notes_push.py` does. `studio.py status --check` is not run by the script that writes
   `status.json`; if that matters, add it there (a script the Mini already runs) rather than back in a workflow.
3. **A pull request merged on a stale head** (main moved on underneath it) is no longer re-run on main. The daily
   run is the net.

## 3. A month after the change

| Source | Minutes a week | How |
|---|---|---|
| Push: Studio core check | 68 | 195 non-data commits, 127 merges skipped |
| Push: Rules check | 29 | 92 commits on its paths, 80 merges skipped, 12 × 2.4 |
| Push: Notes + Content Ops | 8 | 1 + 5 × 1.4 |
| Daily run, four workflows | 49 | 7 a day (3 + 1 + 1 + 2) |
| Pull requests (lower bound, unchanged) | 635 | measured |
| **Total** | **about 790** | |

A month (× 30 / 7): about **3,400 minutes**. Before: about 28,000. Target: 1,200. **Not reached.**

## What is left

Pull requests are now 80% of the bill: 300 or more a week, most paying 1 minute for a 15-second core check and
many paying 2 to 3 for the rules check. To get under 1,200 a month, pull requests must fall to about 150 minutes
a week. Ways there that drop no test (each is a job of its own, none done here):

- Run the core check's two steps inside the rules-check job when both would run (one rounding, not two).
- Shorten the rules check (109 s on average; the `apt-get install ffmpeg` step is the likely place to look, not
  measured here). Under 60 s halves that workflow's bill.
- Fewer pull requests: 300 a week is mostly agents opening one per job. Data-only pull requests could skip the
  core check the same way data pushes now do.

If that is not enough, the two fallbacks from the brief:

1. **A runner on one of Ben's own machines** (the Mini). Minutes on it are free and unlimited. Needs Ben's OK; not
   set up here. It runs pull-request code on that machine, so it should only ever serve a private repo.
2. **A public repo.** Checks are free. Loses the reason for private (decision 8: nobody outside can post where
   agents take instructions).
