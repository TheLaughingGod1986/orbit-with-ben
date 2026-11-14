# Mini: use the SSD for the desk, 11 Nov 2026 (by Claude, on the Mac mini)

Ben, 11 Nov: "We need to utilize the SSD to save storage on the Mac Mini."

## Result

Internal disk free: **16.6 GiB before, 29.5 GiB after.** `~/_desk` on the internal disk went from 15.6 GiB to 2.9 GiB. SSD (`/Volumes/MiniWork`): 47 GiB used, 185 GiB free.

## What was done

1. **Relay paused** (`~/_desk/state/chief-relay.pause`), waited for the running Codex job to end, moved, then unpaused.
2. **24 folders moved from `~/_desk` to `/Volumes/MiniWork/desk/`,** each replaced by a link at its old path. Per folder: `rsync -a`, then `rsync --checksum --dry-run` (0 differences) and equal file counts, then swap, then the old copy removed. Folders: `wt` (4.2 GB), `worker` (1.4), `wt-J2478` (1.2), `jobs` (0.9), `J2470` (0.8), `J1924-records`, `008`, `j2613-spark-size`, `wt-hos-J2582`, `J2583-hos`, `J2583-reservation`, `J2607-hos`, `wt-J2481-hos`, `_share_test`, `tmp-item9`, `media`, `031`, `J2141-hubble-v01`, `tmp`, `J2141-aurora-v01`, `013`, `J2141-solar-v01`, `J2509`, `titles-ship-scratch`.
3. **Git worktrees checked** in both checkouts after the move: none prunable.
4. **Left on the internal disk on purpose:** `state`, `logs`, `bin`, `venvs`, `venv-graphics`, `venv-owb-gfx`, `handoff`, `rescue`, `shared`, `006` (launchd jobs read these, and launchd cannot read `/Volumes`), and about 200 folders under 50 MB each.
5. **Spotlight indexing turned off on the SSD** (`mdutil -i off`, index removed: 3.4 GiB back on the SSD). Undo: `sudo mdutil -i on /Volumes/MiniWork`.
6. **Earlier the same day:** agent history older than 3 days (about 6 GB) moved to `/Volumes/MiniWork/archive/agent-history-2026-11-10` and `-11`.
7. **AGENTS.md:** one rule added to the Render scratch entry: never make a new folder directly in `~/_desk`.

## Why the disk was filling

Between the morning of 10 Nov and the afternoon of 11 Nov (two full scans compared):

| Grew | GiB |
|---|---:|
| Spotlight index on the internal disk (`/.Spotlight-V100`) | +12.8 (6.1 to 18.9) |
| `~/_desk` (job folders made outside the SSD links) | +5.2 |
| `~/Library/Mobile Documents` (iCloud Drive) | +1.3 |

## Still open

- **The internal Spotlight index is 18.9 GiB and was not touched.** It is indexing job worktrees (hundreds of thousands of small files). With the work folders now on the unindexed SSD it should stop growing; it will only shrink if the index is rebuilt (`sudo mdutil -E /`), which is Ben's call because Mac search is slow for an hour or so while it rebuilds. Adding `~/YouTube` and `~/_desk` to System Settings, Spotlight, Search Privacy would keep it small for good.
- **The SSD is now load-bearing.** If it is unplugged, the linked folders stop resolving. The relay already falls back to `/private/tmp` for scratch; jobs that reach into `~/_desk/wt` or `~/_desk/jobs` would fail until it is plugged back in. Nothing on it is the only copy of a master (masters go to the NAS).
- **New top-level folders in `~/_desk` still land on the internal disk** until agents follow the rule. A relay-side check that moves or flags them would make it automatic.
