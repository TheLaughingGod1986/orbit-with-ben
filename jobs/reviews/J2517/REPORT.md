# J2517 — Mac mini & MacBook Pro Always-On Check (Read-Only Report)

- **Date:** 2026-11-10
- **Job:** `J2517`
- **Mode:** Read-only (`£0`, no system settings, accounts, FileVault, or Tailscale settings modified)
- **Progress:**
  - **MacBook Pro (`bens-macbook-pro`) checks (Item 6, Item 9, and repo LaunchAgent plist audit for Items 2, 4, 8):** Completed by `macbook-2` at `2026-11-10T16:35Z`.
  - **Mac mini (`ben-mac-mini`) local host checks (Items 1–5, 7, and live `launchctl list` for Item 8):** Pending execution on `ben-mac-mini` (job pinned `mini_only: true` on release so the Mini worker claims it next and completes the `PENDING ON MINI` cells below before parking for Chief).

---

## 1. Sleep (Mac mini — `ben-mac-mini`)

> **To be filled on `ben-mac-mini`:** Run `pmset -g` and record `sleep`, `disksleep`, `displaysleep`, `womp`, `autorestart`, `powernap`.

- **Command:** `pmset -g`
- **Live output on `ben-mac-mini`:** `PENDING ON MINI`
- **Questions to answer on `ben-mac-mini`:**
  - *Does it ever sleep (`sleep`, `disksleep`, `displaysleep`)?* `PENDING ON MINI`
  - *Does it wake for network access (`womp`)?* `PENDING ON MINI`
  - *Does it start up by itself when power returns (`autorestart`)?* `PENDING ON MINI`

---

## 2. Login & Post-Restart Recovery (`ben-mac-mini`)

> **To be filled on `ben-mac-mini`:** Run `defaults read /Library/Preferences/com.apple.loginwindow autoLoginUser` (account name only) and `ls ~/Library/LaunchAgents`.

- **Automatic login (`defaults read /Library/Preferences/com.apple.loginwindow autoLoginUser`):** `PENDING ON MINI`
- **After a restart with nobody there, do the relay, the board publish, and the two Studio browsers come back without a person logging in?**
  1. **Before user login (at the macOS login window or FileVault pre-boot prompt):** **No.** Every studio service in the repo is installed as a per-user **LaunchAgent** in `~/Library/LaunchAgents` (`gui/$(id -u)` domain), not as a system-wide `/Library/LaunchDaemons` daemon. macOS only loads `~/Library/LaunchAgents` after the user account logs into a GUI session. If Automatic Login is off (or if FileVault stops the boot before macOS loads), **nothing in `~/Library/LaunchAgents` starts** until someone logs in.
  2. **Once the user session logs in (either via Automatic Login or manual login):**
     - **Chief relay (`com.owb.chief-relay`):** **Yes** — `scripts/mini/com.owb.chief-relay.plist` has `RunAtLoad = true` and `StartInterval = 60` (every 60 s).
     - **Board publish (`com.owb.board-publish`):** **Yes** — `scripts/mini/com.owb.board-publish.plist` has `RunAtLoad = true` and `StartInterval = 60` (every 60 s).
     - **Two Studio Chrome browsers (`9223` Orbit Studio, `9222` HOS Flow/Studio):**
       - In the tracked repo, `scripts/macbook/start_cdp_browsers.sh --install` creates `~/Library/LaunchAgents/com.owb.macbook-cdp.plist` (`RunAtLoad = true`) on the **MacBook**, and `07_Content-Ops/launchd/com.owb.tab-janitor.plist` (`RunAtLoad = true`, `StartInterval = 300`) tidies open tabs on the **Mini**, but **no LaunchAgent plist is tracked in `scripts/mini/` or `07_Content-Ops/launchd/` to launch the two Chrome CDP browsers at login on the Mini** (to be confirmed on `ben-mac-mini` by checking `ls ~/Library/LaunchAgents`). Note also that per `AGENTS.md` ("Stop and ask Ben"), workers reopen a closed Studio/Flow browser profile on demand when a job needs it.

---

## 3. Disk Encryption (`ben-mac-mini`)

> **To be filled on `ben-mac-mini`:** Run `fdesetup status`.

- **Command:** `fdesetup status`
- **Live output on `ben-mac-mini`:** `PENDING ON MINI`
- **What FileVault On means in plain English:**
  - If FileVault is **On**, the startup disk is encrypted until a user types their password at the pre-boot unlock screen.
  - After a power cut or cold restart, **the Mac mini waits at that password screen before macOS, Wi-Fi/Ethernet services, Tailscale, Remote Login (`sshd`), or any LaunchAgent can start** — and macOS disables Automatic Login whenever FileVault is enabled. (For a planned reboot while logged in, `sudo fdesetup authrestart` can bypass the prompt once, but it does **not** help after an unplanned power cut.)

---

## 4. Accounts

- **Mac mini (`ben-mac-mini`):** Agents run as `benjaminoats` (per `scripts/mini/*.plist` and `07_Content-Ops/launchd/*.plist`), which is the same account Ben uses himself (`PENDING ON MINI: confirm with id -un and ls /Users`).
- **MacBook Pro (`bens-macbook-pro`):** Agents run as `ben` (`id -un` = `ben`; `/Users` contains `Shared` and `ben`), which is the same account Ben uses himself.

---

## 5. Remote Login (`ben-mac-mini`)

> **To be filled on `ben-mac-mini`:** Run `systemsetup -getremotelogin` or `launchctl print system/com.openssh.sshd`.

- **Command:** `systemsetup -getremotelogin` / `launchctl print system/com.openssh.sshd`
- **Live output on `ben-mac-mini`:** `PENDING ON MINI`

---

## 6. The Private Network (`tailscale status`)

Recorded live on `2026-11-10T16:29Z` (account column redacted to `<tailscale-account>` per repo email/handle hygiene):

```text
100.88.13.103  bens-macbook-pro   <tailscale-account>  macOS  -
100.96.7.11    ben-mac-mini       <tailscale-account>  macOS  -
100.99.115.79  grokbot-box        <tailscale-account>  linux  offline, last seen 24d ago
100.86.131.62  iphone-14-pro-max  <tailscale-account>  iOS    -
100.86.193.52  oats-house-nas     <tailscale-account>  linux  idle, tx 95260 rx 92476
```

- **Is the Mini on it?** **Yes** (`ben-mac-mini`, `100.96.7.11`, online).
- **Is the MacBook on it?** **Yes** (`bens-macbook-pro`, `100.88.13.103`, online).

---

## 7. Last Restart and Why (`ben-mac-mini`)

> **To be filled on `ben-mac-mini`:** Run `uptime`, `last reboot | head -5`, and `pmset -g log | grep -i -E "shutdown cause|restart" | tail -5`.

- **`uptime`:** `PENDING ON MINI`
- **`last reboot | head -5`:** `PENDING ON MINI`
- **`pmset -g log | grep -i -E "shutdown cause|restart" | tail -5`:** `PENDING ON MINI`

---

## 8. `launchd` Agents

### 8a. Tracked Mini LaunchAgent plists in git (`scripts/mini/` & `07_Content-Ops/launchd/`)

| Label | Plist path in repo | Schedule | `RunAtLoad` | `KeepAlive` |
|---|---|---|---|---|
| `com.owb.chief-relay` | `scripts/mini/com.owb.chief-relay.plist` | `StartInterval = 60` (every 1 min) | **`true`** | Not set (`false`) |
| `com.owb.board-publish` | `scripts/mini/com.owb.board-publish.plist` | `StartInterval = 60` (every 1 min) | **`true`** | Not set (`false`) |
| `com.owb.missed-runs` | `07_Content-Ops/launchd/com.owb.missed-runs.plist` | `StartInterval = 1800` (every 30 min) | **`true`** | Not set (`false`) |
| `com.owb.tab-janitor` | `07_Content-Ops/launchd/com.owb.tab-janitor.plist` | `StartInterval = 300` (every 5 min) | **`true`** | Not set (`false`) |
| `com.owb.ai-spend-daily` | `07_Content-Ops/launchd/com.owb.ai-spend-daily.plist` | `StartCalendarInterval = 08:30` | Not set (`false`) | Not set (`false`) |
| `dev.orbit.analytics-snapshot` | `07_Content-Ops/launchd/dev.orbit.analytics-snapshot.plist` | `StartCalendarInterval = 06:40` | Not set (`false`) | Not set (`false`) |
| `dev.orbit.buffer-check` | `07_Content-Ops/launchd/dev.orbit.buffer-check.plist` | `StartCalendarInterval = 07:05` | Not set (`false`) | Not set (`false`) |

> **Live `launchctl list | grep -i -E "owb|orbit"` on `ben-mac-mini`:** `PENDING ON MINI`

### 8b. Live `launchctl list | grep -i owb` on MacBook Pro (`bens-macbook-pro`)

```text
30599   0   com.owb.macbook-worker
-       0   com.owb.macbook-cdp
```

| Label (MacBook) | Plist path | Schedule | `RunAtLoad` | `KeepAlive` |
|---|---|---|---|---|
| `com.owb.macbook-worker` | `~/Library/LaunchAgents/com.owb.macbook-worker.plist` | `StartInterval = 180` (every 3 min) | **`false`** | Not set (`false`) |
| `com.owb.macbook-cdp` | `~/Library/LaunchAgents/com.owb.macbook-cdp.plist` | Login only (`start_cdp_browsers.sh`) | **`true`** | Not set (`false`) |
| `com.local.tdarr-keepawake` | `~/Library/LaunchAgents/com.local.tdarr-keepawake.plist` | `StartCalendarInterval = 00:55` (`caffeinate -s -t 17400`) | **`false`** | Not set (`false`) |

---

## 9. The MacBook Pro (`bens-macbook-pro`) — `pmset -g` and Lid-Closed Behaviour

### 9a. `pmset -g` and `pmset -g custom` on `bens-macbook-pro`

```text
System-wide power settings:
Currently in use:
 standby              1
 Sleep On Power Button 1
 hibernatefile        /var/vm/sleepimage
 powernap             1
 networkoversleep     0
 disksleep            10
 sleep                0 (sleep prevented by ChatGPT, caffeinate, Claude)
 hibernatemode        3
 ttyskeepawake        1
 displaysleep         10
 tcpkeepalive         1
 lowpowermode         0
 womp                 1
```

Profile breakdown (`pmset -g custom` & `pmset -g sched`):
- **AC Power:** `sleep = 0`, `displaysleep = 10`, `disksleep = 10`, `womp = 1`, `powernap = 1`, `tcpkeepalive = 1`, `ttyskeepawake = 1`, `standby = 1`, `hibernatemode = 3`.
- **Battery Power:** `sleep = 1` (1 min), `displaysleep = 2` (2 min), `disksleep = 10`, `womp = 0`, `powernap = 1`. (`macbook_worker.py` also checks `on_mains_power()` and refuses to start jobs on battery.)
- **Repeating power events:** `wakepoweron at 0:54AM every day` (paired with `com.local.tdarr-keepawake` running `caffeinate -s -t 17400` from `00:55` to `05:45` on AC power).

### 9b. Does the MacBook worker stop when the lid is closed?

- **Clamshell setting (`ioreg -r -k AppleClamshellState -d 4`):**
  - `"AppleClamshellCausesSleep" = Yes`
  - `"AppleClamshellState" = No` (lid currently open)
  - System-wide `SleepDisabled` is **not** set.
- **How `macbook_worker.py` holds awake:**
  - `macbook_worker.py` starts each job under `caffeinate -i` (`PreventUserIdleSystemSleep`). That prevents **idle** sleep while the lid is open, and on AC power `sleep` is already `0`.
  - However, `caffeinate -i` (and `sleep = 0`) does **not** override macOS clamshell sleep when the lid is closed without an external display.
- **Result when the lid is closed:**
  1. **While docked on AC power with an active external display** (currently an external `5120 x 2160` Ultra-wide 5K display is connected and `Online: Yes`): macOS enters closed-display (clamshell) mode and **does NOT sleep**, because `sleep = 0` on AC power. **The worker keeps running.**
  2. **When undocked (no external display active), even on AC power:** closing the lid triggers `AppleClamshellCausesSleep = Yes`, putting the MacBook to sleep immediately and **stopping the worker** until the lid is opened (unless system-wide sleep is disabled via `sudo pmset -a disablesleep 1`, which is risky if the laptop is ever put into a bag without turning it back off).

---

## Summary Table: Current vs. Target Settings for an Unattended Machine

| Setting | What it is now (`ben-mac-mini` / `bens-macbook-pro`) | What it should be for a machine nobody sits at | Who can change it |
|---|---|---|---|
| **Mini: System sleep (`sleep`)** | `PENDING ON MINI` (`pmset -g`) | `0` (never sleep) | **Ben** (`sudo pmset -a sleep 0`) |
| **Mini: Disk sleep (`disksleep`)** | `PENDING ON MINI` (`pmset -g`) | `0` for internal SSD (`sudo pmset -a disksleep 0`) | **Ben** (`sudo pmset -a disksleep 0`) |
| **Mini: Display sleep (`displaysleep`)** | `PENDING ON MINI` (`pmset -g`) | `10` (or `5`–`15` min; screen can sleep while CPU stays awake) | **Ben** (`sudo pmset -a displaysleep 10`) |
| **Mini: Wake for network access (`womp`)** | `PENDING ON MINI` (`pmset -g`) | `1` (enabled) | **Ben** (`sudo pmset -a womp 1`) |
| **Mini: Restart automatically after a power failure (`autorestart`)** | `PENDING ON MINI` (`pmset -g`) | `1` (enabled so the Mini boots itself when mains power returns) | **Ben** (`sudo pmset -a autorestart 1` or System Settings → Energy) |
| **Mini: FileVault disk encryption (`fdesetup status`)** | `PENDING ON MINI` | **Trade-off for Ben:** **Off** if the Mini must boot unattended after a power cut; **On** if physical theft protection outweighs unattended power-cut recovery (with FileVault On, the Mini waits at a pre-boot password screen after every power cut) | **Ben** (System Settings → Privacy & Security → FileVault; requires password) |
| **Mini: Automatic Login (`autoLoginUser`)** | `PENDING ON MINI` | Enabled for `benjaminoats` (requires FileVault Off), because all studio `launchd` jobs are user `LaunchAgents` (`~/Library/LaunchAgents`) that only start after user GUI login | **Ben** (System Settings → Users & Groups → Automatically log in as) |
| **Mini: Studio `launchd` agents (`RunAtLoad` / `KeepAlive`)** | `chief-relay`, `board-publish`, `missed-runs`, `tab-janitor` have `RunAtLoad=true` (`StartInterval` polling, `KeepAlive` not needed); daily calendar jobs have `RunAtLoad=false`; live `launchctl list` `PENDING ON MINI` | Keep `StartInterval` + `RunAtLoad=true` on the periodic runners; add a login LaunchAgent for the Mini's two CDP Chrome browsers (`9223`/`9222`) like the MacBook's `com.owb.macbook-cdp.plist` so Studio browsers also come up at login | **Agents** (no `sudo` needed for `~/Library/LaunchAgents`) |
| **Mini: Account separation** | Agents run as `benjaminoats` on Mini and `ben` on MacBook (same account Ben uses himself) | Either keep as-is (simplest for shared Chrome/Studio profiles and Keychain) or move secrets out of shell env; a separate macOS user would require re-signing every browser and CLI | **Ben** (if a separate OS account is ever wanted) |
| **Mini: Remote Login (`sshd`)** | `PENDING ON MINI` | On (reachable over Tailscale IP `100.96.7.11`) so the Mini can be administered headlessly if the UI hangs | **Ben** (System Settings → General → Sharing → Remote Login) |
| **Private network (`tailscale status`)** | Both `ben-mac-mini` (`100.96.7.11`) and `bens-macbook-pro` (`100.88.13.103`) are online | Keep both online; no change needed | No change needed |
| **MacBook: AC sleep & lid-closed behaviour** | AC `sleep = 0`, `womp = 1`; `AppleClamshellCausesSleep = Yes`. Stays awake with lid closed **while docked to AC + external 5K display**; sleeps if lid is closed undocked | Keep as-is (docked to AC + external display keeps it awake with lid closed, while undocked lid-close still sleeps safely before going in a bag); optionally set `RunAtLoad = true` on `com.owb.macbook-worker.plist` | **Agents** (for `RunAtLoad = true` in `com.owb.macbook-worker.plist`); **Ben** if `disablesleep` is ever wanted |
