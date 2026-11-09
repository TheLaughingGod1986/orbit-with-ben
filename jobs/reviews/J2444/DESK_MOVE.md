# J2444 — Move Heavy `~/_desk` Folders (`worktrees`, `renders`, `scratch`, `cache`) onto `MiniWork` SSD

**Date:** 2026-11-09  
**Worker:** `gemini`  
**Job:** `J2444` (`repo: owb`, `needs: mini`, `kind: qa`)  
**Status:** DONE — all 4 directories copied via `rsync -a`, verified with `rsync -a --checksum --dry-run --itemize-changes` (0 diffs) and `find | wc -l` (exact match), symlinked from `~/_desk/<n>` to `/Volumes/MiniWork/desk/<n>`, `.moving` backups removed, all git worktrees verified via `git worktree list`, and `~/_desk/state/chief-relay.pause` removed.

---

## 0. Device Verification (`stat -f %d`)

Verified `/Volumes/MiniWork` is mounted on its own external SSD volume (SanDisk Extreme APFS `/dev/disk6s1`) distinct from `~` (`/System/Volumes/Data` on `/dev/disk3s5`):

```text
stat -f %d /Volumes/MiniWork -> 16777242 (/dev/disk6s1)
stat -f %d /Users/benjaminoats -> 16777234 (/dev/disk3s5)
```

---

## 1. Relay Pause & Active Worker Check

- Created `/Users/benjaminoats/_desk/state/chief-relay.pause` before starting moves so `chief_relay.py` launched no new jobs.
- Verified via `ps` that no other agent CLI (`codex`, `agy`, `agent`, `claude`) was running a job during the directory moves and atomic symlink swaps.
- Removed `/Users/benjaminoats/_desk/state/chief-relay.pause` at job completion (`exists=False`).

---

## 2. Per-Folder `rsync`, Checksum & File-Count Verification, Symlink Swap, and Cleanup

Only the four heavy folders (`worktrees`, `renders`, `scratch`, `cache`) were moved to `/Volumes/MiniWork/desk/<n>`. Other `~/_desk` directories (`state`, `logs`, `venvs`, `jobs`) remain on the internal disk (`st_dev=16777234`).

| Folder | Approx. Size | `rsync -a --checksum --dry-run --itemize-changes` | Source `find . \| wc -l` | Dest `find . \| wc -l` | Symlink `~/_desk/<n>` Target | Target `st_dev` | `.moving` Removed |
|---|---:|---|---:|---:|---|---:|---|
| `cache` | 2.3 GiB | `0 lines` (`DIFF_OUT_LEN=0`, `rc=0`) | `942` | `942` | `/Volumes/MiniWork/desk/cache` | `16777242` | Yes (`exists=False`) |
| `scratch` | 4.0 GiB | `0 lines` (`DIFF_OUT_LEN=0`, `rc=0`, under `publish.lock`) | `89,549` | `89,549` | `/Volumes/MiniWork/desk/scratch` | `16777242` | Yes (`exists=False`) |
| `renders` | 4.6 GiB | `0 lines` (`DIFF_OUT_LEN=0`, `rc=0`) | `3,858` | `3,858` | `/Volumes/MiniWork/desk/renders` | `16777242` | Yes (`exists=False`) |
| `worktrees` | 13.0 GiB | `0 lines` (`DIFF_OUT_LEN=0`, `rc=0`) | `359,608` | `359,608` | `/Volumes/MiniWork/desk/worktrees` | `16777242` | Yes (`exists=False`) |

### Symlink & Untouched Directory Check (`lstat` / `stat`)

```text
/Users/benjaminoats/_desk/worktrees: exists=True islink=True -> /Volumes/MiniWork/desk/worktrees (target_dev=16777242) | .moving_exists=False
/Users/benjaminoats/_desk/renders:   exists=True islink=True -> /Volumes/MiniWork/desk/renders   (target_dev=16777242) | .moving_exists=False
/Users/benjaminoats/_desk/scratch:   exists=True islink=True -> /Volumes/MiniWork/desk/scratch   (target_dev=16777242) | .moving_exists=False
/Users/benjaminoats/_desk/cache:     exists=True islink=True -> /Volumes/MiniWork/desk/cache     (target_dev=16777242) | .moving_exists=False
/Users/benjaminoats/_desk/state:     exists=True islink=False dev=16777234
/Users/benjaminoats/_desk/logs:      exists=True islink=False dev=16777234
/Users/benjaminoats/_desk/venvs:     exists=True islink=False dev=16777234
/Users/benjaminoats/_desk/jobs:      exists=True islink=False dev=16777234
```

---

## 3. Git Worktree Resolution (`git -C <main repo> worktree list`)

All 29 moved worktrees in `~/_desk/worktrees/` (18 OWB + 11 HOS) and 6 moved worktrees in `~/_desk/scratch/` resolve cleanly at their unchanged paths through the `~/_desk/worktrees` and `~/_desk/scratch` symlinks (`st_dev=16777242` on every `.git` entry):

### Orbit With Ben (`/Users/benjaminoats/YouTube/orbit-with-ben`)
```text
$ git -C "/Users/benjaminoats/YouTube/orbit-with-ben" worktree list
/Users/benjaminoats/YouTube/orbit-with-ben                2cca3d9d83 [main]
/Users/benjaminoats/_desk/scratch/chief/board-wt/owb      24b5d6eb5e (detached HEAD)
/Users/benjaminoats/_desk/scratch/chief/j1067/wt          136270e8dd (detached HEAD)
/Users/benjaminoats/_desk/scratch/gemini-J2427            62739bc2fa (detached HEAD)
/Users/benjaminoats/_desk/scratch/j2427-wt                62739bc2fa (detached HEAD)
/Users/benjaminoats/_desk/worktrees/J2141-commons         80ccdf850f (detached HEAD)
/Users/benjaminoats/_desk/worktrees/J2141-dynamo          bc30a5574f (detached HEAD)
/Users/benjaminoats/_desk/worktrees/J2141-field           a1d1f9b760 (detached HEAD)
/Users/benjaminoats/_desk/worktrees/J2141-fossil          bc30a5574f (detached HEAD)
/Users/benjaminoats/_desk/worktrees/J2141-hand-sample     be5b0b6e4e (detached HEAD)
/Users/benjaminoats/_desk/worktrees/J2141-integrated      9bdde7710a (detached HEAD)
/Users/benjaminoats/_desk/worktrees/J2141-lava            e8cebd7d1b (detached HEAD)
/Users/benjaminoats/_desk/worktrees/J2141-lava-edge       ff3ba5eb46 (detached HEAD)
/Users/benjaminoats/_desk/worktrees/J2141-opening         bdac6005da (detached HEAD)
/Users/benjaminoats/_desk/worktrees/J2141-saa             bc30a5574f (detached HEAD)
/Users/benjaminoats/_desk/worktrees/J2141-sediment        a1d1f9b760 (detached HEAD)
/Users/benjaminoats/_desk/worktrees/J2141-sky             3943c3c987 (detached HEAD)
/Users/benjaminoats/_desk/worktrees/J2141-timeline        bc30a5574f (detached HEAD)
/Users/benjaminoats/_desk/worktrees/J2206-owb-reach       8046822d0c (detached HEAD)
/Users/benjaminoats/_desk/worktrees/J2381-master-v01      9dfbbde879 (detached HEAD)
/Users/benjaminoats/_desk/worktrees/J2387-master-v02      58d3e3ad11 (detached HEAD)
/Users/benjaminoats/_desk/worktrees/J2419-muons-v04       982493802f [j2419-muons-v04]
/Users/benjaminoats/_desk/worktrees/analytics             5579595c01 (detached HEAD)
```

### History Of Science (`/Users/benjaminoats/YouTube/History Of Science`)
```text
$ git -C "/Users/benjaminoats/YouTube/History Of Science" worktree list
/Users/benjaminoats/YouTube/History Of Science            8aa6fc34 [main]
/Users/benjaminoats/_desk/scratch/chief/board-wt/hos      abebef57 (detached HEAD)
/Users/benjaminoats/_desk/scratch/chief/hos-main-clean    a61ab1dd (detached HEAD)
/Users/benjaminoats/_desk/scratch/gemini-j0240-wt         d99d999e (detached HEAD)
/Users/benjaminoats/_desk/worktrees/J2199-residual        a61ab1dd [j2199-hos-009-residual]
/Users/benjaminoats/_desk/worktrees/J2230-vaccine         67f5ebdd [j2230-hos-010]
/Users/benjaminoats/_desk/worktrees/J2245-011-vo          fe124fb5 [j2245-hos-011-vo]
/Users/benjaminoats/_desk/worktrees/J2246-013-shorts-vo   fe124fb5 [j2246-hos-013-shorts-vo]
/Users/benjaminoats/_desk/worktrees/J2254                 fe124fb5 [j2254-hos-011-s01-vo]
/Users/benjaminoats/_desk/worktrees/J2255                 b2de8321 [j2255-hos-013-vo]
/Users/benjaminoats/_desk/worktrees/J2275-hos             2a173ba7 (detached HEAD)
/Users/benjaminoats/_desk/worktrees/j0862-v04             4d9a3d52 (detached HEAD)
/Users/benjaminoats/_desk/worktrees/j1809-hos             177b019c (detached HEAD)
/Users/benjaminoats/_desk/worktrees/j2169                 49e2736c (detached HEAD)
/Users/benjaminoats/_desk/worktrees/j2285                 89ab5019 [j2285-hos006-v04]
```

---

## 4. Before & After Disk Usage (`df -h ~` and `df -h /Volumes/MiniWork`)

### Before (`2026-11-09T16:39Z`)
```text
$ df -h /Users/benjaminoats /Volumes/MiniWork
Filesystem      Size    Used   Avail Capacity iused ifree %iused  Mounted on
/dev/disk3s5   228Gi   194Gi   7.3Gi    97%    4.2M   77M    5%   /System/Volumes/Data
/dev/disk6s1   233Gi   3.7Mi   233Gi     1%     570  2.4G    0%   /Volumes/MiniWork

$ df -k /Users/benjaminoats /Volumes/MiniWork
Filesystem   1024-blocks      Used Available Capacity iused      ifree %iused  Mounted on
/dev/disk3s5   239362496 203939556   7668900    97% 4180215   76689000    5%   /System/Volumes/Data
/dev/disk6s1   243993560      3812 243855304     1%     570 2438553040    0%   /Volumes/MiniWork
```

### After (`2026-11-09T20:24Z`)
```text
$ df -h /Users/benjaminoats /Volumes/MiniWork
Filesystem      Size    Used   Avail Capacity iused ifree %iused  Mounted on
/dev/disk3s5   228Gi   163Gi    37Gi    82%    3.8M  393M    1%   /System/Volumes/Data
/dev/disk6s1   233Gi    26Gi   207Gi    12%    468k  2.2G    0%   /Volumes/MiniWork

$ df -k /Users/benjaminoats /Volumes/MiniWork
Filesystem   1024-blocks      Used Available Capacity iused     ifree %iused  Mounted on
/dev/disk3s5   239362496 171287440  39272380    82% 3786255 392723800    1%   /System/Volumes/Data
/dev/disk6s1   243993560  27173580 216685536    12%  467941 2166855360    0%   /Volumes/MiniWork
```

### Summary of Space Gained
- **Internal disk (`/System/Volumes/Data` / `~`) free space:** `7.3 GiB` (`7,668,900 KiB`, 97% used) → **`37 GiB` (`39,272,380 KiB`, 82% used)** — **`+30.1 GiB` (`+31,603,480 KiB`) free space gained** (`~25.9 GiB` directly from the four moved `~/_desk` directories).
- **`/Volumes/MiniWork` usage:** `3.7 MiB` (`3,812 KiB`, 1% used) → **`26 GiB` (`27,173,580 KiB`, 12% used)**, with **`207 GiB` (`216,685,536 KiB`) available** and `467,941` inodes used across `/Volumes/MiniWork/desk/{worktrees,renders,scratch,cache}`.

---

## 5. Operational Note on macOS TCC (`Removable Volumes` / `Full Disk Access`)

During post-move verification under the unattended `chief_relay.py` daemon (`/Library/Frameworks/Python.framework/Versions/3.13/Resources/Python.app/Contents/MacOS/Python`), macOS `sandboxd`/`tccd` began intercepting `open()`/`opendir()` syscalls on `/Volumes/MiniWork` from child processes of `Python.app` (`kTCCServiceSystemPolicyAllFiles` returning `authValue=0` and waiting on a GUI prompt in `CoreServicesUIAgent`). Granting **Full Disk Access** (or **Files & Folders → Removable Volumes**) to `/Library/Frameworks/Python.framework/Versions/3.13/Resources/Python.app` (and `/usr/bin/python3` / `agy`) in **System Settings → Privacy & Security** will prevent unattended background workers spawned by `chief_relay.py` from blocking on `tccd` when opening files inside `~/_desk/{worktrees,renders,scratch,cache}` on `/Volumes/MiniWork`.
