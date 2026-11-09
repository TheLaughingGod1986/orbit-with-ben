# J2443 — Mac mini Disk Report Part 2 (Read-Only): The ~135 GiB Outside J2439 & Worktree Cleanliness Audit

- **Date:** 2026-11-09T16:25Z
- **Job:** `J2443` (`qa`, read-only follow-on to `J2439`)
- **Worker:** `gemini` (`gemini-4-argon-high`)
- **Mode:** Strictly read-only (no files changed, moved, or deleted; no `sudo` used).

---

## Executive Accounting: Where the ~195–196 GiB Used Actually Lives

`df -h ~ /` on the 228 GiB APFS container (`/dev/disk3s5` `/System/Volumes/Data`):

```text
Filesystem        Size    Used   Avail Capacity iused ifree %iused  Mounted on
/dev/disk3s5     228Gi   195Gi   6.7Gi    97%    4.2M   70M    6%   /System/Volumes/Data
/dev/disk3s1s1   228Gi    12Gi   6.7Gi    64%    459k   70M    1%   /
```

`J2439` measured `~/YouTube/*` (`27G`), `~/_desk/*` (`29G`), `/private/tmp/*` (`~2.2G`–`7G`), `~/Downloads` (`1.2G`), `~/.npm` (`559M`), `~/.cache` (`464M`), and `~/Library/Caches` (`133M`) — totaling **~60 GiB**. The remaining **~135 GiB** on `/System/Volumes/Data` breaks down as follows:

1. **Uncovered inside `/Users/benjaminoats` (`~51 GiB`, bringing `~` total to `111 GiB`):**
   - **`~/Library` (`17G`):**
     - `~/Library/Application Support` (`14G`), led by `SynologyDrive` (`4.6G`: `data` `3.3G`, `log` `1.0G`, `SynologyDrive.app` `266M`), `Cursor` (`4.4G`: `User` `3.3G`, `IndexedDB` `795M`, `AgentStores` `277M`), `Google` (`3.7G`: `Chrome-OrbitStudio` `1.7G`, `Chrome` `1.3G`, `GoogleUpdater` `759M`), `com.portrait.Dell-Color-Management` (`482M`), `Claude` (`364M`), and `Grok Bot` (`152M`).
     - `~/Library/Containers` (`1.3G`) & `~/Library/Mobile Documents` (`1.3G`, iCloud Drive local cache).
     - `~/Library/Python` (`565M`), `~/Library/Logs` (`203M`), `~/Library/Group Containers` (`165M` readable without TCC).
   - **Agent/CLI dot-folders & Chrome CDP profiles in `~` (`~28.3 GiB` not in J2439):**
     - `~/.gemini` (`7.1G` → `~/.gemini/antigravity-cli`: `conversations` `4.3G`, `brain` `2.7G`, `log` `139M`)
     - `~/.cursor` (`4.3G`: `chats` `1.9G`, `extensions` `1.7G`, `projects` `607M`, `ai-tracking` `96M`)
     - `~/.codex` (`4.1G`: `sessions` `2.3G`, `packages` `815M`, `thread_history_1.sqlite` `675M`, `plugins` `71M`, `cache` `67M`, `generated_images` `63M`)
     - `~/.cursor-server` (`3.8G`: `data` `2.4G`, `bin` `1.4G`)
     - `~/.local` (`3.0G`: `share/disabled-gui` `1.3G`, `share/cursor-agent` `1.2G`, `share/cursor-mac-mini-hos-worker` `151M`, `share/uv` `71M`)
     - `~/.hos-chrome-flow-benoats-googlemail-cdp` (`2.1G`)
     - `~/.venvs` (`1.8G`: `hos-vl-precheck` `759M`, `orbit-omni` `513M`, `hos-vertex` `228M`, `hos-vo` `226M`, `orbit-code-graphics` `122M`)
     - `~/.orbit-chrome-youtube-studio` (`1.7G`)
     - `~/.hos-chrome-youtube-studio` (`1.3G`)
     - `~/.npm-global` (`673M`), `~/.orbit-chrome-meta-dev` (`224M`), `~/.rembg` (`168M`), `~/.hos_desk` (`125M`)
   - **Other non-dot folders in `~` (`~5.7 GiB` not in J2439):**
     - `~/code` (`2.8G`, incl. `WP-Alt-text-plugin` `2.2G`), `~/agent-tools` (`1.2G`, incl. `whisper-venv` `922M`, `whisper-venv-313` `217M`), `~/Desktop` (`862M`), `~/Tdarr` (`479M`), `~/_grok_scratch` (`398M`), `~/Removed-LaunchItems-20261003` (`318M`), `~/Music` (`97M`).
2. **Outside `/Users/benjaminoats` on `/System/Volumes/Data` (`~84 GiB` physical blocks):**
   - **`/private/var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/X/com.google.Chrome.code_sign_clone` (`975G` logical `du -sh` across 458 cloned Chrome app bundles; ~60–62 GiB physical unique blocks):** macOS/Chrome creates APFS `clonefile` copies (`~2.1G` each) under `/private/var/folders/1z/.../X/com.google.Chrome.code_sign_clone` when launching/updating signed Chrome instances. Current-version clones share blocks with `/Applications/Google Chrome.app`, but old clones from prior Chrome updates retain unique physical extents once the main app updates.
   - **`/Applications` (`5.9G`)**, **`/System/Volumes/Data/System` (`5.1G`)**, **`/Library` (`4.7G`)**, **`/opt` (`3.3G`)**, **`/private/var/db` (`2.9G` readable without sudo)**, **`/private/var/folders/1z/.../C` (`639M`)**.
   - *(Note on APFS container siblings sharing the 228 GiB pool outside `/System/Volumes/Data`: `/System/Volumes/Preboot` is `28G`, `/` sealed System is `12G`, `/System/Volumes/VM` is `5.0G`. `tmutil listlocalsnapshots /` returned **0 snapshots**.)*

---

## Top 25 by Size

### Table A — Top 25 Newly Uncovered Directories (Excluding Folders Already Ranked in J2439)

*(Leaf/distinct directories across `~`, `~/Library`, and `/System/Volumes/Data` that explain the ~135 GiB outside J2439's scope)*

| Rank | Path | Size (`du -sh`) | Category / Notes |
|---:|---|---:|---|
| 1 | `/private/var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/X/com.google.Chrome.code_sign_clone` | `975G` *(logical; ~60G physical)* | 458 APFS-cloned Chrome app bundles (`~2.1G` each); stale clones from old Chrome versions hold physical disk blocks |
| 2 | `/Users/benjaminoats/.gemini` (`~/.gemini/antigravity-cli`) | `7.1G` | `conversations` (`4.3G`), `brain` (`2.7G`), `log` (`139M`) |
| 3 | `/Applications` | `5.9G` | System-wide applications on `/System/Volumes/Data` |
| 4 | `/System/Volumes/Data/System` | `5.1G` | macOS Data-volume System assets |
| 5 | `/Library` | `4.7G` | System-level `/Library` (readable without `sudo`) |
| 6 | `/Users/benjaminoats/Library/Application Support/SynologyDrive` | `4.6G` | `data` (`3.3G`), `log` (`1.0G`), `SynologyDrive.app` (`266M`) |
| 7 | `/Users/benjaminoats/Library/Application Support/Cursor` | `4.4G` | `User` (`3.3G`), `IndexedDB` (`795M`), `AgentStores` (`277M`) |
| 8 | `/Users/benjaminoats/.cursor` | `4.3G` | `chats` (`1.9G`), `extensions` (`1.7G`), `projects` (`607M`), `ai-tracking` (`96M`) |
| 9 | `/Users/benjaminoats/.codex` | `4.1G` | `sessions` (`2.3G`), `packages` (`815M`), `thread_history_1.sqlite` (`675M`) |
| 10 | `/Users/benjaminoats/.cursor-server` | `3.8G` | `data` (`2.4G`), `bin` (`1.4G`) |
| 11 | `/Users/benjaminoats/Library/Application Support/Google` | `3.7G` | `Chrome-OrbitStudio` (`1.7G`), `Chrome` (`1.3G`), `GoogleUpdater` (`759M`) |
| 12 | `/opt` | `3.3G` | Homebrew installation (`/opt/homebrew`) |
| 13 | `/Users/benjaminoats/.local` | `3.0G` | `share/disabled-gui` (`1.3G`), `share/cursor-agent` (`1.2G`), `share/cursor-mac-mini-hos-worker` (`151M`), `share/uv` (`71M`) |
| 14 | `/private/var/db` | `2.9G` | macOS system databases (readable portion without `sudo`) |
| 15 | `/Users/benjaminoats/code` | `2.8G` | `WP-Alt-text-plugin` (`2.2G`), `beepbeep-titles` (`158M`), `youtube` (`113M`), `beepbeep-platform` (`112M`) |
| 16 | `/Users/benjaminoats/.hos-chrome-flow-benoats-googlemail-cdp` | `2.1G` | HOS Flow Chrome CDP profile |
| 17 | `/Users/benjaminoats/.venvs` | `1.8G` | `hos-vl-precheck` (`759M`), `orbit-omni` (`513M`), `hos-vertex` (`228M`), `hos-vo` (`226M`), `orbit-code-graphics` (`122M`) |
| 18 | `/Users/benjaminoats/.orbit-chrome-youtube-studio` | `1.7G` | OWB YouTube Studio Chrome CDP profile (port 9223) |
| 19 | `/Users/benjaminoats/.hos-chrome-youtube-studio` | `1.3G` | HOS YouTube Studio Chrome CDP profile |
| 20 | `/Users/benjaminoats/Library/Containers` | `1.3G` | `com.apple.AMPArtworkAgent` (`496M`), `com.apple.geod` (`244M`), `com.apple.NeptuneOneExtension` (`151M`), `com.apple.photoanalysisd` (`102M`) |
| 21 | `/Users/benjaminoats/Library/Mobile Documents` | `1.3G` | iCloud Drive local storage (`OWB UAT` / `HOS UAT` / CloudDocs) |
| 22 | `/Users/benjaminoats/agent-tools` | `1.2G` | `whisper-venv` (`922M`), `whisper-venv-313` (`217M`), text logs (`52M`) |
| 23 | `/Users/benjaminoats/Desktop` | `862M` | User Desktop folder |
| 24 | `/Users/benjaminoats/.npm-global` | `673M` | Global npm packages |
| 25 | `/private/var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/C` | `639M` | Per-user Darwin cache directory (`~/Library/Python` is #26 at `565M`; `Dell-Color-Management` #27 at `482M`; `~/Tdarr` #28 at `479M`) |

### Table B — Top 25 Overall Across J2443 Scanned Commands (1)–(4) in `/Users/benjaminoats`

*(Combining top-level `~/*`, `~/.[!.]*`, and the largest `~/Library/*` / `Application Support/*` children measured in commands 1–4)*

| Rank | Path | Size (`du -sh`) | Parent / Scope |
|---:|---|---:|---|
| 1 | `/Users/benjaminoats/_desk` | `29G` | Top-level `~/*` (covered in J2439: `worktrees` `13G`, `renders` `4.6G`, `scratch` `4.0G`, `cache` `2.3G`, `state` `891M`) |
| 2 | `/Users/benjaminoats/YouTube` | `27G` | Top-level `~/*` (covered in J2439: `orbit-with-ben` `16G`, `History Of Science` `8.9G`, `hos-008-lightning` `1.5G`) |
| 3 | `/Users/benjaminoats/Library` | `17G` | Top-level `~/*` (`Application Support` `14G`, `Containers` `1.3G`, `Mobile Documents` `1.3G`, `Python` `565M`) |
| 4 | `/Users/benjaminoats/Library/Application Support` | `14G` | Inside `~/Library/*` (`SynologyDrive` `4.6G`, `Cursor` `4.4G`, `Google` `3.7G`, `Dell-Color-Management` `482M`, `Claude` `364M`) |
| 5 | `/Users/benjaminoats/.gemini` | `7.1G` | Top-level `~/.[!.]*` (`~/.gemini/antigravity-cli`: `conversations` `4.3G`, `brain` `2.7G`) |
| 6 | `/Users/benjaminoats/Library/Application Support/SynologyDrive` | `4.6G` | Inside `~/Library/Application Support/*` |
| 7 | `/Users/benjaminoats/Library/Application Support/Cursor` | `4.4G` | Inside `~/Library/Application Support/*` |
| 8 | `/Users/benjaminoats/.cursor` | `4.3G` | Top-level `~/.[!.]*` |
| 9 | `/Users/benjaminoats/.codex` | `4.1G` | Top-level `~/.[!.]*` |
| 10 | `/Users/benjaminoats/.cursor-server` | `3.8G` | Top-level `~/.[!.]*` |
| 11 | `/Users/benjaminoats/Library/Application Support/Google` | `3.7G` | Inside `~/Library/Application Support/*` |
| 12 | `/Users/benjaminoats/.local` | `3.0G` | Top-level `~/.[!.]*` |
| 13 | `/Users/benjaminoats/code` | `2.8G` | Top-level `~/*` |
| 14 | `/Users/benjaminoats/.hos-chrome-flow-benoats-googlemail-cdp` | `2.1G` | Top-level `~/.[!.]*` |
| 15 | `/Users/benjaminoats/.venvs` | `1.8G` | Top-level `~/.[!.]*` |
| 16 | `/Users/benjaminoats/.orbit-chrome-youtube-studio` | `1.7G` | Top-level `~/.[!.]*` |
| 17 | `/Users/benjaminoats/.hos-chrome-youtube-studio` | `1.3G` | Top-level `~/.[!.]*` |
| 18 | `/Users/benjaminoats/Library/Containers` | `1.3G` | Inside `~/Library/*` |
| 19 | `/Users/benjaminoats/Library/Mobile Documents` | `1.3G` | Inside `~/Library/*` |
| 20 | `/Users/benjaminoats/Downloads` | `1.2G` | Top-level `~/*` (covered in J2439) |
| 21 | `/Users/benjaminoats/agent-tools` | `1.2G` | Top-level `~/*` |
| 22 | `/Users/benjaminoats/Desktop` | `862M` | Top-level `~/*` |
| 23 | `/Users/benjaminoats/.npm-global` | `673M` | Top-level `~/.[!.]*` |
| 24 | `/Users/benjaminoats/Library/Python` | `565M` | Inside `~/Library/*` |
| 25 | `/Users/benjaminoats/.npm` | `559M` | Top-level `~/.[!.]*` (covered in J2439) |

---

## Exact Command Outputs (1)–(6)

### (1) `du -sh ~/* ~/.[!.]* 2>/dev/null | sort -h | tail -30`

```text
 19M	/Users/benjaminoats/hosbl
 36M	/Users/benjaminoats/.wordpress-playground
 38M	/Users/benjaminoats/.wp-cli
 53M	/Users/benjaminoats/.turso
 97M	/Users/benjaminoats/Music
125M	/Users/benjaminoats/.hos_desk
168M	/Users/benjaminoats/.rembg
224M	/Users/benjaminoats/.orbit-chrome-meta-dev
318M	/Users/benjaminoats/Removed-LaunchItems-20261003
398M	/Users/benjaminoats/_grok_scratch
464M	/Users/benjaminoats/.cache
479M	/Users/benjaminoats/Tdarr
559M	/Users/benjaminoats/.npm
673M	/Users/benjaminoats/.npm-global
862M	/Users/benjaminoats/Desktop
1.2G	/Users/benjaminoats/Downloads
1.2G	/Users/benjaminoats/agent-tools
1.3G	/Users/benjaminoats/.hos-chrome-youtube-studio
1.7G	/Users/benjaminoats/.orbit-chrome-youtube-studio
1.8G	/Users/benjaminoats/.venvs
2.1G	/Users/benjaminoats/.hos-chrome-flow-benoats-googlemail-cdp
2.8G	/Users/benjaminoats/code
3.0G	/Users/benjaminoats/.local
3.8G	/Users/benjaminoats/.cursor-server
4.1G	/Users/benjaminoats/.codex
4.3G	/Users/benjaminoats/.cursor
7.1G	/Users/benjaminoats/.gemini
 17G	/Users/benjaminoats/Library
 27G	/Users/benjaminoats/YouTube
 29G	/Users/benjaminoats/_desk
```

### (2) `du -sh ~/Library/* 2>/dev/null | sort -h | tail -20`

```text
2.1M	/Users/benjaminoats/Library/KeyboardServices
4.2M	/Users/benjaminoats/Library/FrontBoard
5.3M	/Users/benjaminoats/Library/News
5.8M	/Users/benjaminoats/Library/MediaAnalysis
6.6M	/Users/benjaminoats/Library/Accessibility
7.3M	/Users/benjaminoats/Library/Finance
8.3M	/Users/benjaminoats/Library/Preferences
 13M	/Users/benjaminoats/Library/WebKit
 14M	/Users/benjaminoats/Library/Google
 43M	/Users/benjaminoats/Library/Passes
 51M	/Users/benjaminoats/Library/Keychains
 89M	/Users/benjaminoats/Library/HTTPStorages
 91M	/Users/benjaminoats/Library/CloudStorage
133M	/Users/benjaminoats/Library/Caches
165M	/Users/benjaminoats/Library/Group Containers
203M	/Users/benjaminoats/Library/Logs
565M	/Users/benjaminoats/Library/Python
1.3G	/Users/benjaminoats/Library/Containers
1.3G	/Users/benjaminoats/Library/Mobile Documents
 14G	/Users/benjaminoats/Library/Application Support
```

### (3) `du -sh ~/Library/Application\ Support/* ~/Library/Containers/* ~/Library/Group\ Containers/* 2>/dev/null | sort -h | tail -25`

```text
7.7M	/Users/benjaminoats/Library/Containers/ai.perplexity.mac
7.8M	/Users/benjaminoats/Library/Containers/com.apple.podcasts.widget
7.9M	/Users/benjaminoats/Library/Containers/com.apple.podcasts
8.0M	/Users/benjaminoats/Library/Application Support/LogiOptionsPlus
9.3M	/Users/benjaminoats/Library/Containers/com.apple.photolibraryd
 10M	/Users/benjaminoats/Library/Application Support/Logi
 10M	/Users/benjaminoats/Library/Containers/com.apple.Maps
 12M	/Users/benjaminoats/Library/Application Support/com.apple.wallpaper
 13M	/Users/benjaminoats/Library/Containers/com.apple.mediastream.mstreamd
 18M	/Users/benjaminoats/Library/Group Containers/group.com.apple.icloudMCCKit
 20M	/Users/benjaminoats/Library/Containers/com.apple.siri.media-indexer
 20M	/Users/benjaminoats/Library/Group Containers/group.ai.perplexity.app
 71M	/Users/benjaminoats/Library/Containers/com.apple.wallpaper.agent
 94M	/Users/benjaminoats/Library/Containers/com.apple.mediaanalysisd
102M	/Users/benjaminoats/Library/Containers/com.apple.photoanalysisd
119M	/Users/benjaminoats/Library/Group Containers/243LU875E5.groups.com.apple.podcasts
151M	/Users/benjaminoats/Library/Containers/com.apple.NeptuneOneExtension
152M	/Users/benjaminoats/Library/Application Support/Grok Bot
244M	/Users/benjaminoats/Library/Containers/com.apple.geod
364M	/Users/benjaminoats/Library/Application Support/Claude
482M	/Users/benjaminoats/Library/Application Support/com.portrait.Dell-Color-Management
496M	/Users/benjaminoats/Library/Containers/com.apple.AMPArtworkAgent
3.7G	/Users/benjaminoats/Library/Application Support/Google
4.4G	/Users/benjaminoats/Library/Application Support/Cursor
4.6G	/Users/benjaminoats/Library/Application Support/SynologyDrive
```

### (4) `du -sh ~/.ollama ~/.cache/* ~/.codex ~/.cursor ~/.gemini ~/.claude ~/Movies ~/Pictures ~/Music 2>/dev/null`

*(Note: `~/.ollama` does not exist on the Mac mini.)*

```text
  0B	/Users/benjaminoats/.cache/antigravity
448K	/Users/benjaminoats/.cache/gh
464M	/Users/benjaminoats/.cache/huggingface
4.0K	/Users/benjaminoats/.cache/owb-cdp-tabs.json
4.1G	/Users/benjaminoats/.codex
4.3G	/Users/benjaminoats/.cursor
7.1G	/Users/benjaminoats/.gemini
 15M	/Users/benjaminoats/.claude
 48K	/Users/benjaminoats/Movies
 20K	/Users/benjaminoats/Pictures
 97M	/Users/benjaminoats/Music
```

### (5) `tmutil listlocalsnapshots /`

```text
Snapshots for disk /:
```
*(Zero local Time Machine APFS snapshots exist on `/`.)*

### (6) Paths Blocked by macOS TCC / Permissions (No `sudo` Used)

- **Inside `~/Library` (145 TCC `Operation not permitted` / `Permission denied` paths skipped):**
  - `~/Library/Application Support/{CloudDocs,CallHistoryTransactions,CallHistoryDB,com.apple.sharedfilelist,Knowledge,com.apple.TCC,FileProvider,AddressBook,FaceTime,DifferentialPrivacy,com.apple.avfoundation/Frecents}`
  - `~/Library/{Messages,Mail,Safari,Calendars,IdentityServices,Daemon Containers,Autosave Information,HomeKit,Sharing,Trial,AppleMediaServices,DuetExpertCenter,Accounts,Biome,IntelligencePlatform,Shortcuts,Suggestions,Weather}`
  - `~/Library/Group Containers/group.com.apple.*` and `~/Library/Containers/com.apple.*` TCC-protected containers.
- **Outside `~` on `/System/Volumes/Data` (skipped without `sudo`):**
  - `/private/var/{audit,backups,agentx,OOPJit,root,install}`
  - `/private/var/db/{Spotlight,appinstalld,diskimagesiod,locationd,modelmanagerd,sysdiagnose,analyticsd,AppleIntelligencePlatform,coreml,nsurlsessiond}`
  - `/Library/{Trial,Bluetooth,Tailscale,Application Support/com.apple.TCC}`

---

## Worktree Audit (`~/_desk/worktrees/*` and `/private/tmp/*-wt` / `codex-*`)

Criteria checked against `jobs/queue.json` and git:
1. **Job status in `jobs/queue.json`:** job ID extracted from the folder name is `done` or `cancelled`.
2. **Git status empty (`clean`):** `git -C <path> status --porcelain` outputs 0 lines.
3. **Nothing unpushed (`pushed`):** `git -C <path> branch -r --contains HEAD` is non-empty (every commit in the worktree's `HEAD` is pushed to an `origin/*` branch or `origin/main`).

### A. Qualifying Worktrees (`done`/`cancelled` + `git status` empty + nothing unpushed): **23 Worktrees (`~11.09 GB` total)**

#### 1. Qualifying in `~/_desk/worktrees/*` — **19 worktrees (`~8.88 GB`)**

| # | Path | Size | Job ID (`queue.json` status) | Branch | `HEAD` | Remote Branch Containing `HEAD` |
|---:|---|---:|---|---|---|---|
| 1 | `/Users/benjaminoats/_desk/worktrees/J2381-master-v01` | `538M` | `J2381` (`done`) | `gemini/J2381-master-v01` | `33d08fea40` | `origin/gemini/J2381-master-v01` |
| 2 | `/Users/benjaminoats/_desk/worktrees/J2141-fossil` | `531M` | `J2141` (`done`) | `cursor/J2141-fossil-v01` | `554cb6005d` | `origin/cursor/J2141-fossil-v01` |
| 3 | `/Users/benjaminoats/_desk/worktrees/J2141-hand-sample` | `531M` | `J2141` (`done`) | `codex/J2141-hand-sample` | `a9bf593485` | `origin/cursor/J2141-fossil-v01` |
| 4 | `/Users/benjaminoats/_desk/worktrees/J2141-lava` | `531M` | `J2141` (`done`) | `cursor/J2141-usgs-lava-v01` | `95f4f3e1f6` | `origin/cursor/J2141-fossil-v01` |
| 5 | `/Users/benjaminoats/_desk/worktrees/J2141-lava-edge` | `531M` | `J2141` (`done`) | `cursor/J2141-lava-edge` | `1bd6d4d2ce` | `origin/cursor/J2141-fossil-v01` |
| 6 | `/Users/benjaminoats/_desk/worktrees/J2141-sediment` | `531M` | `J2141` (`done`) | `cursor/J2141-sediment` | `31e36efec3` | `origin/cursor/J2141-fossil-v01` |
| 7 | `/Users/benjaminoats/_desk/worktrees/J2141-commons` | `530M` | `J2141` (`done`) | `worker/J2141-commons-v01` | `cb3ecfa51c` | `origin/worker/J2141-commons-v01` |
| 8 | `/Users/benjaminoats/_desk/worktrees/J2141-dynamo` | `530M` | `J2141` (`done`) | `worker/J2141-dynamo-v01` | `a810377312` | `origin/worker/J2141-dynamo-v01` |
| 9 | `/Users/benjaminoats/_desk/worktrees/J2141-sky` | `530M` | `J2141` (`done`) | `worker/J2141-sky-v01` | `8150ceb5f2` | `origin/worker/J2141-sky-v01` |
| 10 | `/Users/benjaminoats/_desk/worktrees/J2141-timeline` | `530M` | `J2141` (`done`) | `worker/J2141-timeline-v01` | `8ae3c85e09` | `origin/worker/J2141-timeline-v01` |
| 11 | `/Users/benjaminoats/_desk/worktrees/J2206-owb-reach` | `530M` | `J2206` (`done`) | `cursor/J2206-owb-reach` | `71672183b9` | `origin/cursor/J2206-owb-reach` |
| 12 | `/Users/benjaminoats/_desk/worktrees/J2141-field` | `529M` | `J2141` (`done`) | `worker/J2141-field-v01` | `5a2a23be28` | `origin/worker/J2141-field-v01` |
| 13 | `/Users/benjaminoats/_desk/worktrees/J2141-opening` | `529M` | `J2141` (`done`) | `worker/J2141-opening-v01` | `d3377ec121` | `origin/worker/J2141-opening-v01` |
| 14 | `/Users/benjaminoats/_desk/worktrees/J2141-saa` | `529M` | `J2141` (`done`) | `worker/J2141-saa-v01` | `e7e3774e63` | `origin/worker/J2141-saa-v01` |
| 15 | `/Users/benjaminoats/_desk/worktrees/J2275-hos` | `291M` | `J2275` (`done`) | `codex/J2275-runner-safety` | `05c929c697` | `origin/codex/J2275-runner-safety` |
| 16 | `/Users/benjaminoats/_desk/worktrees/j0862-v04` | `291M` | `J0862` (`done`) | `codex/j0862-v04` | `cb18632da4` | `origin/main` |
| 17 | `/Users/benjaminoats/_desk/worktrees/J2254` | `290M` | `J2254` (`done`) | `codex/J2254-vo-pickup` | `17ed7310b7` | `origin/codex/J2254-vo-pickup` |
| 18 | `/Users/benjaminoats/_desk/worktrees/j1809-hos` | `290M` | `J1809` (`done`) | `cursor/j1809-desk-role` | `5f3feb7753` | `origin/cursor/j1809-desk-role` |
| 19 | `/Users/benjaminoats/_desk/worktrees/j2169` | `290M` | `J2169` (`done`) | `cursor/J2169-shorts-bc` | `699c359bf4` | `origin/cursor/J2169-shorts-bc` |

#### 2. Qualifying in `/private/tmp/*-wt` and `/private/tmp/codex-*` — **4 worktrees (`~2.21 GB`)**

| # | Path | Size | Job ID (`queue.json` status) | Branch | `HEAD` | Remote Branch Containing `HEAD` |
|---:|---|---:|---|---|---|---|
| 1 | `/private/tmp/gemini-J1100-wt` | `569M` | `J1100` (`done`) | `main` *(standalone clone)* | `158fd4d83f` | `origin/main` |
| 2 | `/private/tmp/codex-j2292-queue` | `550M` | `J2292` (`done`) | `main` *(standalone clone)* | `daef1df666` | `origin/main` |
| 3 | `/private/tmp/codex-j2159-queue` | `545M` | `J2159` (`done`) | `main` *(standalone clone)* | `03192ca741` | `origin/main` |
| 4 | `/private/tmp/codex-j2278-queue` | `545M` | `J2278` (`done`) | `main` *(standalone clone)* | `290948f881` | `origin/main` |

---

### B. Non-Qualifying Entries in `~/_desk/worktrees/*` and `/private/tmp/*-wt` / `codex-*` (Do Not Remove Automatically)

#### 1. Non-Qualifying in `~/_desk/worktrees/*` (10 folders)

| Path | Size | Job ID (`queue.json` status) | Clean (`git status`) | Pushed (`origin`) | Reason It Does Not Qualify |
|---|---:|---|---|---|---|
| `/Users/benjaminoats/_desk/worktrees/analytics` | `542M` | *(no job id)* | Yes | Yes (`origin/main`) | Standing launchd analytics worktree (`launchd/analytics-snapshot.sh`), no job ID |
| `/Users/benjaminoats/_desk/worktrees/J2419-muons-v04` | `541M` | `J2419` (`done`) | Yes | **No** | Local commit `2d10ba0e34` on `gemini/j2419-muons-v04` is not pushed to `origin` |
| `/Users/benjaminoats/_desk/worktrees/J2387-master-v02` | `538M` | `J2387` (`done`) | **No** (2 dirty) | Yes (`origin/main`) | Modified `HARVEST_POOL_v01.json` + untracked `shot_list_v02.csv` |
| `/Users/benjaminoats/_desk/worktrees/J2141-integrated` | `531M` | `J2141` (`done`) | **No** (1 dirty) | Yes (`origin/worker/J2141-integrated-v01`) | Untracked `02_Video-Projects/031.../07_Edit-Project/harvest_v01` |
| `/Users/benjaminoats/_desk/worktrees/J2245-011-vo` | `502M` | `J2245` (`blocked`) | Yes | Yes (`origin/cursor/J2245-011-vo`) | Job status is `blocked` (not `done`/`cancelled`) |
| `/Users/benjaminoats/_desk/worktrees/J2246-013-shorts-vo` | `311M` | `J2246` (`blocked`) | Yes | Yes (`origin/cursor/J2246-013-shorts-vo`) | Job status is `blocked` (not `done`/`cancelled`) |
| `/Users/benjaminoats/_desk/worktrees/J2255` | `295M` | `J2255` (`blocked`) | Yes | **No** | Job is `blocked` and commit `9631a14b31` (`cursor/J2255-short-c`) is not on `origin` |
| `/Users/benjaminoats/_desk/worktrees/J2230-vaccine` | `291M` | `J2230` (`blocked`) | Yes | Yes (`origin/codex/J2230-vaccine`) | Job status is `blocked` (not `done`/`cancelled`) |
| `/Users/benjaminoats/_desk/worktrees/J2199-residual` | `290M` | `J2199` (`blocked`) | Yes | Yes (`origin/cursor/J2199-099-residual`) | Job status is `blocked` (not `done`/`cancelled`) |
| `/Users/benjaminoats/_desk/worktrees/j2285` | `290M` | `J2285` (`done`) | **No** (1 dirty) | Yes (`origin/cursor/j2285-099-readback`) | Untracked `07_Content-Ops/scripts/_j2285_read_publishat.ts` |

#### 2. Non-Qualifying in `/private/tmp/*-wt` and `/private/tmp/codex-*` (19 folders)

| Path | Size | Job ID (`queue.json` status) | Clean (`git status`) | Pushed (`origin`) | Reason It Does Not Qualify |
|---|---:|---|---|---|---|
| `/private/tmp/j2427-wt` | `542M` | `J2427` (`done`) | **No** (1 dirty) | Yes (`origin/main`) | Modified `scripts/video_tracker.py` |
| `/private/tmp/J2404-wt` | `540M` | `J2404` (`open`) | **No** (4 dirty) | Yes (`origin/main`) | Job `J2404` is `open` (not `done`/`cancelled`) and has 4 modified files |
| `/private/tmp/codex-j2199-queue` | `538M` | `J2199` (`blocked`) | Yes | Yes (`origin/main`) | Job status is `blocked` (not `done`/`cancelled`) |
| `/private/tmp/codex-J2248-chief-review` | `531M` | `J2248` (`done`) | Yes | **No** | Local commit `1edaecaf60` on `codex/J2248-chief-review` is not on `origin` |
| `/private/tmp/codex-J2248-v03` | `531M` | `J2248` (`done`) | **No** (1 dirty) | **No** | Untracked `jobs/reviews/J2248/REVIEW_v03.md` + local commit `c34a0429d6` not on `origin` |
| `/private/tmp/codex-J2089` | `530M` | `J2089` (`done`) | **No** (1 dirty) | **No** | Modified `REVIEWED_EXPORTS_VERIFICATION_v01.json` + commit `948a33770a` not on `origin` |
| `/private/tmp/codex-j2200-record` | `530M` | `J2200` (`blocked`) | Yes | **No** | Job is `blocked` and commit `f2e60fc5d5` is not on `origin` |
| `/private/tmp/codex-j2246-state` | `51M` | `J2246` (`blocked`) | Yes | Yes (`origin/main`) | Job status is `blocked` (not `done`/`cancelled`) |
| `/private/tmp/codex-j0912-stills` | `500K` | `J0912` (`blocked`) | N/A (not git) | N/A | Stills scratch folder (not a git worktree); `J0912` is `blocked` |
| `/private/tmp/J1915-wt` | `4.0K` | `J1915` (`done`) | N/A (not git) | N/A | Already offloaded to NAS (`MOVED_TO_NAS.txt` stub only) |
| `/private/tmp/J2089-distance-wt` | `4.0K` | `J2089` (`done`) | N/A (not git) | N/A | Already offloaded to NAS (`MOVED_TO_NAS.txt` stub only) |
| `/private/tmp/J2089-mechanism-exports-wt` | `4.0K` | `J2089` (`done`) | N/A (not git) | N/A | Already offloaded to NAS (`MOVED_TO_NAS.txt` stub only) |
| `/private/tmp/J2089-mechanism-fix-wt` | `4.0K` | `J2089` (`done`) | N/A (not git) | N/A | Already offloaded to NAS (`MOVED_TO_NAS.txt` stub only) |
| `/private/tmp/J2089-ocean-wt` | `4.0K` | `J2089` (`done`) | N/A (not git) | N/A | Already offloaded to NAS (`MOVED_TO_NAS.txt` stub only) |
| `/private/tmp/J2089-r23-wt` | `4.0K` | `J2089` (`done`) | N/A (not git) | N/A | Already offloaded to NAS (`MOVED_TO_NAS.txt` stub only) |
| `/private/tmp/J2089-ruler-wt` | `4.0K` | `J2089` (`done`) | N/A (not git) | N/A | Already offloaded to NAS (`MOVED_TO_NAS.txt` stub only) |
| `/private/tmp/J2157-codex-wt` | `4.0K` | `J2157` (`done`) | N/A (not git) | N/A | Already offloaded to NAS (`MOVED_TO_NAS.txt` stub only) |
| `/private/tmp/j0912-short-a-wt` | `4.0K` | `J0912` (`blocked`) | N/A (not git) | N/A | Already offloaded to NAS (`MOVED_TO_NAS.txt` stub only) |
| `/private/tmp/codex-daemon-501` | `0B` | *(no job id)* | N/A (not git) | N/A | Empty daemon socket directory |
