# Workflow audit: why videos stall (4 Nov 2026)

Ben, 4 Nov: "Ideally, we don't want blocks. We want a continuous workflow ... a new video almost daily ... agents to work in uniform, knocking off video after video."

Data: `jobs/queue.json` and board.json at 4 Nov ~17:00 UTC. 1,876 jobs; 85 open, 38 blocked.

## Findings, biggest first

| # | Problem | Evidence | Effect |
|---|---|---|---|
| 1 | **One Chief does almost all decisions, one at a time** | 60 of 85 open jobs are `kind: chief`. 27 of them are topic/advancement calls for films 033–061. Grok (main Chief) has been down for days, Claude was marked down, so Codex is Chief *and* the main worker. | 26 films sit at topic/script with nobody free to decide. |
| 2 | **Chief defers instead of deciding** | Topic calls for 033–048 were ruled "defer lock with owned evidence" and re-queued as more evidence jobs (J1928–J1934, J2000–J2007). | Films loop between "verify evidence" and "decide" without moving. |
| 3 | **Hourly re-check loop** (fixed today, PR #485) | 357 of 499 jobs since 1 Nov were "Chief: verify condition for X" on ~10 held jobs (J0936 ×70, J1100 ×66). | Ate the Chief slot. Now backs off 1→24 h. |
| 4 | **The Mini runs one short job at a time** | Idle 930–1,387 min/day on 31 Oct–3 Nov with 70 Mini jobs open. Each wake does one job (median 2 min) then exits. The capacity/parallel dispatcher (J1843, PR437, 313 tests pass) is built but `rollout_enabled=False`, parked for Chief. | Most of every day is idle. |
| 5 | **Codex's built-in safety reviewer refuses normal work** | 25 jobs hit "automatic approval review rejected": Buffer posts, R2 uploads, git pushes to our own repo (J2007, J1878, J1825). Runs use `codex exec --approve-for-me`. | Finished work can't be published or recorded; needs a human each time. |
| 6 | **"Can't watch or listen" holds** | J1752/J1753 (031/032 voice), J1880 (HOS 008), J1834, J1879. Ben's 4 Nov rule (final watch = the check) is queued as J2017, a Chief job, so it is stuck behind #1. | Two finished voices and an edit wait indefinitely. |
| 7 | **Jobs routed to lanes that can't run them** | Claude (cloud-only) is first in the qa/review/listing/script chains, even for Mini jobs; Cursor is out of credit to 6 Nov but first for vo/image/video/assembly/facts. 71 reroutes since 1 Nov; J2022/J2018 sat 3 h. | Delay before every such job starts. |
| 8 | **Work isn't tied to films** | 461 of 499 jobs since 1 Nov had no film id. | The board can't show progress; nobody sees a film stall. |
| 9 | **Release mistakes** (mine) | I released J2022/J2018/J1201 by editing fields by hand and left their `hold`; fixed 15:58. | 3 h lost on two jobs. |

## Fixes

**Done today:** #3 back-off (PR #485), "video share" on the home page (#8 visibility), #9 cleared.

**Agents can do without Ben (queued):**
- A. **Turn on parallel dispatch** (J1843): Chief exact-head review of PR437 + PR477, then `rollout_enabled=True` with Codex and Gemini as two Mini lanes, and let a woken agent keep taking jobs until its 25-min cap.
- B. **Routing:** a Mini job never waits on Claude (cloud) or a credit-flagged lane; pick the first lane that can actually run it at assignment time. PR with tests.
- C. **Film-first order:** production jobs for the 3 films nearest Ben's watch outrank all non-deadline work; every production job carries `--film/--stage` (jobs.py rejects a production job without them).
- D. **Apply Ben's final-watch rule now** (J2017), at the top of the queue.

**Need Ben's yes:**
- E. **Topic and script calls move off the Chief.** A reviewer agent (Gemini or Codex) decides go/no-go against a short written rubric (neighbour check, audience evidence, facts sourced). "Defer" is allowed only with one named missing fact and a 24 h deadline, else it's a no-go and the film is dropped. The Chief keeps publish, money, AGENTS.md.
- F. **Codex unattended permissions:** allow an exact list of destinations without the auto-reviewer: our two GitHub repos, the existing R2 bucket, the Buffer API, the YouTube Data API on our two channels. Anything else still needs approval. (Today every Buffer post, upload and some git pushes need a person.)
- G. **WIP limit:** at most 6 films in active production at once (topic → UAT), the rest wait in the idea list. With parallel lanes this targets one film to Ben's watch per day once the pipe is full.

## How we'll know it works

Daily on the home page: video jobs share (target > 60%), films that moved (target ≥ 3/day), and one film to UAT per day once the pipe is full (about a week after A–G).
