# J2445 — Mac mini Disk Cleanup: Stale Chrome `code_sign_clone` Copies & Worktree Removal Audit

- **Date:** 2026-11-09T20:50Z
- **Job:** `J2445` (`qa`, follow-on to `J2443` and `J2444`)
- **Worker:** `gemini` (`gemini-4-argon-high`)
- **Authorisation:** Ben's go 9 Nov 2026 (*"get it all sorted"*), relayed in `J2445`.
- **Spend:** £0.00. No Chrome instance quit; no Chrome profile folder (`~/.orbit-chrome-youtube-studio`, `~/.hos-chrome-*`, `~/Library/Application Support/Google`), NAS folder, media folder, or `~/YouTube` file touched.

---

## 1. Before & After Disk Usage (`df -h ~` and `df -h /Volumes/MiniWork`)

*(Note: Immediately prior to `J2445`, `J2444` completed moving `~/_desk/{worktrees,renders,scratch,cache}` (`~25.9 GiB`) from the internal disk onto `/Volumes/MiniWork/desk/`, increasing internal disk free space from `6.7–7.3 GiB` to `38 GiB`.)*

### Reference Baseline at `J2443` Audit (`2026-11-09T16:25Z`, before `J2444` + `J2445`)
```text
Filesystem        Size    Used   Avail Capacity iused ifree %iused  Mounted on
/dev/disk3s5     228Gi   195Gi   6.7Gi    97%    4.2M   70M    6%   /System/Volumes/Data
/dev/disk6s1     233Gi   3.7Mi   233Gi     1%     570  2.4G    0%   /Volumes/MiniWork
```

### Before `J2445` (`2026-11-09T20:29Z`, immediately after `J2444`)
```text
$ df -h ~ && df -h /Volumes/MiniWork
Filesystem      Size    Used   Avail Capacity iused ifree %iused  Mounted on
/dev/disk3s5   228Gi   163Gi    38Gi    82%    3.8M  399M    1%   /System/Volumes/Data
Filesystem      Size    Used   Avail Capacity iused ifree %iused  Mounted on
/dev/disk6s1   233Gi    26Gi   207Gi    12%    468k  2.2G    0%   /Volumes/MiniWork

$ df -k ~ /Volumes/MiniWork
Filesystem   1024-blocks      Used Available Capacity iused      ifree %iused  Mounted on
/dev/disk3s5   239362496 170660984  39898836    82% 3787325  398988360    1%   /System/Volumes/Data
/dev/disk6s1   243993560  27190036 216669080    12%  467936 2166690800    0%   /Volumes/MiniWork
```

### After `J2445` (`2026-11-09T20:47Z` / `20:50Z`)
```text
$ df -h ~ && df -h /Volumes/MiniWork
Filesystem      Size    Used   Avail Capacity iused ifree %iused  Mounted on
/dev/disk3s5   228Gi   162Gi    38Gi    81%    2.9M  402M    1%   /System/Volumes/Data
Filesystem      Size    Used   Avail Capacity iused ifree %iused  Mounted on
/dev/disk6s1   233Gi    26Gi   207Gi    12%    468k  2.2G    0%   /Volumes/MiniWork

$ df -k ~ /Volumes/MiniWork
Filesystem   1024-blocks      Used Available Capacity iused      ifree %iused  Mounted on
/dev/disk3s5   239362496 170391496  40168324    81% 2867844  401683240    1%   /System/Volumes/Data
/dev/disk6s1   243993560  27187352 216671764    12%  467938 2166717640    0%   /Volumes/MiniWork
```

### Space & Inode Summary
- **Combined `J2444` + `J2445` effect on `/System/Volumes/Data` (`~`):**
  - **Used:** `195 GiB` (`97%`) → **`162 GiB` (`81%`)** (`-33 GiB` used).
  - **Available:** `6.7 GiB` → **`38 GiB` (`40,168,324 KiB` / `38.31 GiB`)** (`+31.6 GiB` free space gained).
  - **Inodes (`iused`):** `4.2M` (`3,787,325` before `J2445`) → **`2.9M` (`2,867,844`)** (**`-919,481` inodes freed in `J2445` alone**, `-24.3%` of all inodes on the internal disk).
- **Direct `J2445` Part A (`com.google.Chrome.code_sign_clone`) effect:**
  - **Removed:** **`475` of `476` cloned Chrome app bundles** (`~998 GiB` of logical `du -sh` footprint removed; `du -sh` dropped from `~1,000G` across 476 bundles to `2.1G` for the single active bundle `code_sign_clone.c6s3Zc`).
  - **Physical APFS blocks & inodes:** Because the 475 removed `code_sign_clone.*` bundles were APFS copy-on-write (`clonefile`) clones of the currently installed Chrome `156.0.8078.80`, their file data extents were shared with `/Applications/Google Chrome.app` and the active `code_sign_clone.c6s3Zc` bundle. Removing the 475 inactive clones freed **`919,481` APFS file/directory inodes** and **`269,488 KiB` (`~263.2 MiB`)** of physical APFS directory/metadata blocks (`170,660,984 KiB` → `170,391,496 KiB` Used; capacity `82%` → `81%`), and means future Chrome updates will no longer leave 475 orphaned copies pinning the old version's physical extents.

---

## 2. Part (A) — Chrome `code_sign_clone` Cleanup (`/private/var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/X/com.google.Chrome.code_sign_clone`)

- **Total subfolders found at start of `J2445`:** `476` (`code_sign_clone.*`, `~2.1 GiB` logical each).
- **Active process check (`lsof +D` and `ps -axo pid,command`):**
  - Ran `lsof +D /private/var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/X/com.google.Chrome.code_sign_clone` and `ps -axo pid,command`.
  - Exactly **1 subfolder** (`code_sign_clone.c6s3Zc`) had open file descriptors (8 open `REG`/`txt` descriptors held by `tccd` PID `939` and running `Google Chrome` PIDs `8600`, `8881`, `76385`, `92779`).
- **Action taken:**
  - **Removed:** **`475` subfolders** (`failed=0`).
  - **Skipped:** **`1` subfolder (`code_sign_clone.c6s3Zc`)** — active in `lsof +D` (8 open file descriptors across `tccd` and 4 running Chrome browser instances).
- **Verification after cleanup:**
  ```text
  $ ls -la /private/var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/X/com.google.Chrome.code_sign_clone
  total 0
  drwx------@ 3 benjaminoats  staff  96 Nov  9 20:46 .
  drwxr-xr-x@ 3 benjaminoats  staff  96 Nov  5 11:20 ..
  drwx------@ 3 benjaminoats  staff  96 Nov  5 14:52 code_sign_clone.c6s3Zc
  ```
- **Chrome profiles & instances:** Untouched (`~/.orbit-chrome-youtube-studio`, `~/.hos-chrome-youtube-studio`, `~/.hos-chrome-flow-benoats-googlemail-cdp`, `~/Library/Application Support/Google` all intact; no Chrome process quit).

---

## 3. Part (B) — Audit & `git worktree remove` / `git worktree prune` on the 23 Worktrees from `J2443`

Per the `J2445` brief:
> *"Remove the 23 worktrees J2443 lists as done/cancelled + git-clean + nothing unpushed (19 in ~/_desk/worktrees, 4 in /private/tmp), with git -C <main repo> worktree remove <path> (never rm -rf a worktree), re-checking each is still clean and pushed first; skip any that isn't. Then git worktree prune in both checkouts."*

- **Removed:** **`0`**
- **Skipped:** **`23`** (`4` in `/private/tmp`, `19` in `~/_desk/worktrees` -> `/Volumes/MiniWork/desk/worktrees`)
- **`git worktree prune`:** Executed in both `/Users/benjaminoats/YouTube/orbit-with-ben` (`rc=0`) and `/Users/benjaminoats/YouTube/History Of Science` (`rc=0`).

### Why the 4 `/private/tmp` Entries Were Skipped (`~2.21 GB`)

All 4 entries in `/private/tmp` were re-checked and confirmed to belong to `done` jobs (`J1100`, `J2292`, `J2159`, `J2278`), with `git status --porcelain` empty (`clean`) and `HEAD` contained in `origin/main` (`pushed`). However, as noted in `J2443/DISK_REPORT_2.md`, all 4 are **standalone git clones** (each has its own full `.git/` directory, not a linked worktree of `/Users/benjaminoats/YouTube/orbit-with-ben`). Running `git -C /Users/benjaminoats/YouTube/orbit-with-ben worktree remove <path>` returns `rc=128` (`fatal: '<path>' is not a working tree`), and `J2445` explicitly forbids `rm -rf` on worktrees:

| # | Path | Size | Job Status | `git status --porcelain` | `branch -r --contains HEAD` | `git -C <owb> worktree remove <path>` Result / Skip Reason |
|---:|---|---:|---|---|---|---|
| 1 | `/private/tmp/gemini-J1100-wt` | `569M` | `J1100` (`done`) | Clean (`""`) | `origin/main` (`158fd4d83f`) | **Skipped:** `fatal: '/private/tmp/gemini-J1100-wt' is not a working tree` (standalone clone; `rm -rf` forbidden by brief) |
| 2 | `/private/tmp/codex-j2292-queue` | `550M` | `J2292` (`done`) | Clean (`""`) | `origin/main` (`daef1df666`) | **Skipped:** `fatal: '/private/tmp/codex-j2292-queue' is not a working tree` (standalone clone; `rm -rf` forbidden by brief) |
| 3 | `/private/tmp/codex-j2159-queue` | `545M` | `J2159` (`done`) | Clean (`""`) | `origin/main` (`03192ca741`) | **Skipped:** `fatal: '/private/tmp/codex-j2159-queue' is not a working tree` (standalone clone; `rm -rf` forbidden by brief) |
| 4 | `/private/tmp/codex-j2278-queue` | `545M` | `J2278` (`done`) | Clean (`""`) | `origin/main` (`290948f881`) | **Skipped:** `fatal: '/private/tmp/codex-j2278-queue' is not a working tree` (standalone clone; `rm -rf` forbidden by brief) |

### Why the 19 `~/_desk/worktrees` Entries Were Skipped (`~8.88 GB`, already on `/Volumes/MiniWork`)

1. **Already moved off the internal disk in `J2444`:** In `J2444` (completed at `2026-11-09T20:26Z`), `~/_desk/worktrees` was moved to `/Volumes/MiniWork/desk/worktrees` (`SanDisk Extreme SSD`, `/dev/disk6s1`, `207 GiB` free) and symlinked (`~/_desk/worktrees -> /Volumes/MiniWork/desk/worktrees`). These 19 worktrees therefore occupy `0 B` on the Mac mini's internal disk (`/System/Volumes/Data`).
2. **Internal `.git/worktrees/<name>` check passed:** Reading `<main_repo>/.git/worktrees/<name>/HEAD` on the internal disk confirmed all 19 worktrees still belong to `done` jobs and all 19 `HEAD` commits are pushed to `origin/*`.
3. **macOS TCC `Removable Volumes` block on unattended `Python.app`:** As documented in `J2444/DESK_MOVE.md` §5, under the unattended `chief_relay.py` daemon (`/Library/Frameworks/Python.framework/Versions/3.13/Resources/Python.app`), macOS `tccd` intercepts `open()`/`opendir()` syscalls on `/Volumes/MiniWork` (`kTCCServiceSystemPolicyRemovableVolumes`) and blocks waiting on a GUI prompt in `CoreServicesUIAgent`. Consequently, both `git -C <wt> status --porcelain` (the required pre-removal cleanliness check) and `git -C <main_repo> worktree remove <wt>` time out / fail with `EINTR` on `/Volumes/MiniWork/desk/worktrees/*` from an unattended worker. Per the brief (*"re-checking each is still clean and pushed first; skip any that isn't"*), all 19 were skipped until Ben grants **Removable Volumes** / **Full Disk Access** to `Python.app` in **System Settings → Privacy & Security**:

| # | Path (`~/_desk/worktrees/<name>`) | Size | Repo | Job Status | `HEAD` & Pushed Remote Branch (`.git/worktrees` check) | Skip Reason |
|---:|---|---:|---|---|---|---|
| 1 | `/Users/benjaminoats/_desk/worktrees/J2381-master-v01` | `538M` | OWB | `J2381` (`done`) | `33d08fea40` (`origin/gemini/J2381-master-v01`) | **Skipped:** On `/Volumes/MiniWork/desk/worktrees`; `git status` & `git worktree remove` blocked by macOS TCC (`Removable Volumes`) under unattended `Python.app` |
| 2 | `/Users/benjaminoats/_desk/worktrees/J2141-fossil` | `531M` | OWB | `J2141` (`done`) | `554cb6005d` (`origin/cursor/J2141-fossil-v01`) | **Skipped:** On `/Volumes/MiniWork/desk/worktrees`; `git status` & `git worktree remove` blocked by macOS TCC (`Removable Volumes`) under unattended `Python.app` |
| 3 | `/Users/benjaminoats/_desk/worktrees/J2141-hand-sample` | `531M` | OWB | `J2141` (`done`) | `a9bf593485` (`origin/cursor/J2141-fossil-v01`) | **Skipped:** On `/Volumes/MiniWork/desk/worktrees`; `git status` & `git worktree remove` blocked by macOS TCC (`Removable Volumes`) under unattended `Python.app` |
| 4 | `/Users/benjaminoats/_desk/worktrees/J2141-lava` | `531M` | OWB | `J2141` (`done`) | `95f4f3e1f6` (`origin/cursor/J2141-fossil-v01`) | **Skipped:** On `/Volumes/MiniWork/desk/worktrees`; `git status` & `git worktree remove` blocked by macOS TCC (`Removable Volumes`) under unattended `Python.app` |
| 5 | `/Users/benjaminoats/_desk/worktrees/J2141-lava-edge` | `531M` | OWB | `J2141` (`done`) | `1bd6d4d2ce` (`origin/cursor/J2141-fossil-v01`) | **Skipped:** On `/Volumes/MiniWork/desk/worktrees`; `git status` & `git worktree remove` blocked by macOS TCC (`Removable Volumes`) under unattended `Python.app` |
| 6 | `/Users/benjaminoats/_desk/worktrees/J2141-sediment` | `531M` | OWB | `J2141` (`done`) | `31e36efec3` (`origin/cursor/J2141-fossil-v01`) | **Skipped:** On `/Volumes/MiniWork/desk/worktrees`; `git status` & `git worktree remove` blocked by macOS TCC (`Removable Volumes`) under unattended `Python.app` |
| 7 | `/Users/benjaminoats/_desk/worktrees/J2141-commons` | `530M` | OWB | `J2141` (`done`) | `cb3ecfa51c` (`origin/worker/J2141-commons-v01`) | **Skipped:** On `/Volumes/MiniWork/desk/worktrees`; `git status` & `git worktree remove` blocked by macOS TCC (`Removable Volumes`) under unattended `Python.app` |
| 8 | `/Users/benjaminoats/_desk/worktrees/J2141-dynamo` | `530M` | OWB | `J2141` (`done`) | `a810377312` (`origin/worker/J2141-dynamo-v01`) | **Skipped:** On `/Volumes/MiniWork/desk/worktrees`; `git status` & `git worktree remove` blocked by macOS TCC (`Removable Volumes`) under unattended `Python.app` |
| 9 | `/Users/benjaminoats/_desk/worktrees/J2141-sky` | `530M` | OWB | `J2141` (`done`) | `8150ceb5f2` (`origin/worker/J2141-sky-v01`) | **Skipped:** On `/Volumes/MiniWork/desk/worktrees`; `git status` & `git worktree remove` blocked by macOS TCC (`Removable Volumes`) under unattended `Python.app` |
| 10 | `/Users/benjaminoats/_desk/worktrees/J2141-timeline` | `530M` | OWB | `J2141` (`done`) | `8ae3c85e09` (`origin/worker/J2141-timeline-v01`) | **Skipped:** On `/Volumes/MiniWork/desk/worktrees`; `git status` & `git worktree remove` blocked by macOS TCC (`Removable Volumes`) under unattended `Python.app` |
| 11 | `/Users/benjaminoats/_desk/worktrees/J2206-owb-reach` | `530M` | OWB | `J2206` (`done`) | `71672183b9` (`origin/cursor/J2206-owb-reach`) | **Skipped:** On `/Volumes/MiniWork/desk/worktrees`; `git status` & `git worktree remove` blocked by macOS TCC (`Removable Volumes`) under unattended `Python.app` |
| 12 | `/Users/benjaminoats/_desk/worktrees/J2141-field` | `529M` | OWB | `J2141` (`done`) | `5a2a23be28` (`origin/worker/J2141-field-v01`) | **Skipped:** On `/Volumes/MiniWork/desk/worktrees`; `git status` & `git worktree remove` blocked by macOS TCC (`Removable Volumes`) under unattended `Python.app` |
| 13 | `/Users/benjaminoats/_desk/worktrees/J2141-opening` | `529M` | OWB | `J2141` (`done`) | `d3377ec121` (`origin/worker/J2141-opening-v01`) | **Skipped:** On `/Volumes/MiniWork/desk/worktrees`; `git status` & `git worktree remove` blocked by macOS TCC (`Removable Volumes`) under unattended `Python.app` |
| 14 | `/Users/benjaminoats/_desk/worktrees/J2141-saa` | `529M` | OWB | `J2141` (`done`) | `e7e3774e63` (`origin/worker/J2141-saa-v01`) | **Skipped:** On `/Volumes/MiniWork/desk/worktrees`; `git status` & `git worktree remove` blocked by macOS TCC (`Removable Volumes`) under unattended `Python.app` |
| 15 | `/Users/benjaminoats/_desk/worktrees/J2275-hos` | `291M` | HOS | `J2275` (`done`) | `05c929c697` (`origin/codex/J2275-runner-safety`) | **Skipped:** On `/Volumes/MiniWork/desk/worktrees`; `git status` & `git worktree remove` blocked by macOS TCC (`Removable Volumes`) under unattended `Python.app` |
| 16 | `/Users/benjaminoats/_desk/worktrees/j0862-v04` | `291M` | HOS | `J0862` (`done`) | `cb18632da4` (`origin/main`) | **Skipped:** On `/Volumes/MiniWork/desk/worktrees`; `git status` & `git worktree remove` blocked by macOS TCC (`Removable Volumes`) under unattended `Python.app` |
| 17 | `/Users/benjaminoats/_desk/worktrees/J2254` | `290M` | HOS | `J2254` (`done`) | `17ed7310b7` (`origin/codex/J2254-vo-pickup`) | **Skipped:** On `/Volumes/MiniWork/desk/worktrees`; `git status` & `git worktree remove` blocked by macOS TCC (`Removable Volumes`) under unattended `Python.app` |
| 18 | `/Users/benjaminoats/_desk/worktrees/j1809-hos` | `290M` | HOS | `J1809` (`done`) | `5f3feb7753` (`origin/cursor/j1809-desk-role`) | **Skipped:** On `/Volumes/MiniWork/desk/worktrees`; `git status` & `git worktree remove` blocked by macOS TCC (`Removable Volumes`) under unattended `Python.app` |
| 19 | `/Users/benjaminoats/_desk/worktrees/j2169` | `290M` | HOS | `J2169` (`done`) | `699c359bf4` (`origin/cursor/J2169-shorts-bc`) | **Skipped:** On `/Volumes/MiniWork/desk/worktrees`; `git status` & `git worktree remove` blocked by macOS TCC (`Removable Volumes`) under unattended `Python.app` |
