# J2559: Mac mini housekeeping after the always-on check

Worker: Claude Code on the Mini (`claudecode`), 11 Nov 2026. Follow-up to J2517. Everything was done as the studio
user, with no sudo and no change to sleep, login, disk encryption, sharing or the network.

## Summary

| Item | Result |
|---|---|
| Daily tracker (`dev.orbit.analytics-snapshot`) | Cause found and fixed in this pull request. Today's run was done by hand (see below). |
| Daily Buffer check (`dev.orbit.buffer-check`) | One network failure on 10 Nov, nothing to fix. See the 11 Nov run below. |
| Daily credit reading (`com.owb.ai-spend-daily`) | Cause found, **not fixed**: three of its seven readings fail. Parked for the Chief. |
| Old 9223 browser agent | Its file is moved to `disabled/`. It is **still loaded** until the next restart, on purpose (see below). |
| September Cursor agents | **Not unloaded.** The reason given for unloading them does not hold. Parked for the Chief. |
| Browser agent in the repo | Added: `scripts/mini/com.hos.cdp-browsers.plist` and `scripts/mini/cdp_browsers.sh`. |

## 1. The three scheduled agents that showed exit code 1

### The daily tracker: fixed here

**Why it failed.** `~/_desk/worktrees` is a link to the removable working SSD. A scheduled job on the Mini cannot
open files on that drive until Python and the shell have Full Disk Access. The script already checks that the
folder "answers" before using it, but the check only made the folder and asked if it was writable. Both pass on
the SSD while every file on it stays unreadable. So the run picked the worktree on the SSD, could not open it,
tried to make it again, and stopped:

```
--- Wed Nov 11 06:40:05 GMT 2026
fatal: '/Users/benjaminoats/_desk/worktrees/analytics' already exists
could not make the tracker worktree at /Users/benjaminoats/_desk/worktrees/analytics; nothing run
```

The same two lines are in the log for 10 Nov 06:40. No snapshot was made by the scheduled run on either day.

**The fix** (`07_Content-Ops/launchd/analytics-snapshot.sh`): the folder check now writes a small file and reads it
back, and a worktree that is already there must have a readable `.git` pointer. If either fails, the tracker uses
its worktree on the internal disk (`~/Library/Application Support/owb-analytics/worktree`), as it already does
when the folder does not answer at all.

**Run by hand.** Started detached at about 06:54Z with the worktree set to the internal-disk one, which is the
path the fixed script picks under the scheduler: tmux session `J2559-tracker`, log `~/_desk/logs/J2559-tracker.log`,
exit code in `~/_desk/logs/J2559-tracker.done`. Result: see "Hand runs" at the end.

**Not shown.** The fix has not run under the scheduler itself. A hand run from a terminal can read the SSD, so it
cannot reproduce the failure. The first real proof is the 06:40 run on the morning after this is merged: the log
should say `using .../owb-analytics/worktree` and end without "nothing run".

**Tests.** `scripts/test_analytics_snapshot_sh.py` has two new tests (a worktree that cannot be read sends the
tracker to the internal disk; the check leaves no file behind). All 12 pass.

### The daily Buffer check: nothing to fix

**Why it failed.** On 10 Nov the Orbit half of the check printed one line, `fetch failed`, and stopped. That is a
network call that did not get through. The History of Science half ran normally in the same run, and the runs of
7, 8 and 9 Nov were complete. The script, its plist and its sign-ins are all sound.

It was not run a second time by hand: the scheduled 07:05 run was minutes away, and two runs at once collide on
the desk lock. Result of that run: see "Hand runs" at the end.

### The daily credit reading: cause found, not fixed

The script reads seven credit pools and exits 1 if any one fails. In the last three runs:

| Reading | 8 Nov | 9 Nov | 10 Nov | What the log says |
|---|---|---|---|---|
| ElevenLabs, Flow, Vertex, Gemini | read | read | read | |
| Cursor | read | read | FAIL | no usage line on the Cursor spending page (signed out, or the page changed) |
| Codex | FAIL | FAIL | FAIL | no `rate_limits` reading in the Codex session logs |
| Claude | FAIL | FAIL | FAIL | no usage line on the Claude usage page (signed out, or the page changed) |

So the four readings that matter for spend are recorded every day, and the exit code is 1 because of the three
usage-page readings. Not worked out in this job: whether the Claude and Cursor pages are signed out in the Mini's
browser (Ben's sign-in) or have changed their wording (a fix to the reader), and why the Codex logs carry no
reading. It needs a look at the two pages in the browser and at one Codex session log. Parked for the Chief as a
follow-up job; nothing was changed.

## 2. Leftover agents

Nothing else names them: a search of both repos' scripts, the launchd folder, `~/_desk/bin` and `~/.local/bin`
found only the agents' own plists and their own start scripts.

### `com.orbit.studio-chrome-9223`: file moved, agent left loaded

Its plist is now in `~/Library/LaunchAgents/disabled/`. Its start script in `/tmp` is already gone, so it could
not start again anyway, and with the plist moved it will not load at the next login.

It was **not** unloaded. The Orbit Studio browser that is running now was started by this agent a day and a half
ago, and the system counts that browser as the agent's own process. Unloading the agent quits the browser, in the
middle of whatever Studio job is using it. `com.hos.cdp-browsers` would bring it back within five minutes, signed
in, but a half-finished Studio edit would be lost. After the next restart the browser comes up under
`com.hos.cdp-browsers` alone and this agent is gone. If the Chief wants it out sooner:
`launchctl bootout gui/$(id -u)/com.orbit.studio-chrome-9223` at a moment when no Studio job is running, then
`~/_desk/bin/cdp_browsers.sh start`.

### The September `com.cursor.mac-mini-*` agents: not touched

The brief says they restart for ever on exit code 1. That is not what the Mini shows:

- Four of the five are loaded, and each has been running without a restart for 5 days 16 hours. The "1" in the
  list is the exit code of the run before that.
- They are Cursor's remote workers, connected and answering every 30 seconds. Their logs show real sessions served
  through them: hundreds of commands each, the most recent on the main worker at 21:45 on 10 Nov.
- Two of them work in folders outside the studio (other projects of Ben's under `~/code`). The fifth,
  `com.cursor.mac-mini-repo-workers`, is not loaded at all.

Unloading them would cut off something that is in use, partly outside the studio, for a reason that is not true
today. The plists are where they were. For the Chief to decide: leave them, or unload only the two that work in
the studio checkouts.

## 3. The browser agent in the repo

- `scripts/mini/com.hos.cdp-browsers.plist`: the installed plist, with a comment on how to install, check and
  remove it.
- `scripts/mini/cdp_browsers.sh`: the script it runs (`~/_desk/bin/cdp_browsers.sh`).

One change from the installed script: the Flow browser's profile folder is named after the account it is signed
into, so the repo copy reads that folder from `~/_desk/bin/cdp_browsers.env` (not in git) and the comment naming
channels and the account is cut down. The installed script on the Mini is unchanged. The copies hold no secret, no
account name and no network address; `scripts/test_email_ratchet.py` passes.

## Hand runs

- **Tracker:** started 06:54:55, **exit code 0** (`~/_desk/logs/J2559-tracker.done`). Both channels' snapshots
  for 11 Nov were written, the upcoming Shorts check covered 10 scheduled Shorts, both reports and the dashboard
  were rebuilt. The first push was refused because main had moved; the script's own retry got it through, and the
  commit is on main as `985b2c5bc6`. So the tracker has today's data even though the 06:40 run made none.
- **Buffer check:** not run by hand (see above). The scheduled 07:05 run on 11 Nov had not happened when this
  report was written. Whoever reviews this reads its result from `launchctl list | grep buffer-check` (0 is good)
  and the last block of `~/Library/Logs/orbit-buffer-check.log`.
- **Credit reading:** not run by hand; it would fail the same way until the three readings are looked at.

