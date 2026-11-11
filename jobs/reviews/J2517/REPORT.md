# J2517 — Mac mini & MacBook Pro Always-On Check (Read-Only Report)

- **Date:** 2026-11-11
- **Job:** `J2517`
- **Mode:** Read-only (`£0`, no system settings, accounts, FileVault, or Tailscale settings modified)
- **Progress:**
  - **MacBook Pro (`bens-macbook-pro`) checks (Item 6, Item 9, and repo LaunchAgent plist audit):** Completed by `macbook-2` at `2026-11-10T16:35Z`.
  - **Mac mini (`ben-mac-mini`) local host checks (Items 1–8):** Completed by `gemini` on `ben-mac-mini` at `2026-11-11T02:55Z`.

---

## 1. Sleep (Mac mini — `ben-mac-mini`)

- **Command:** `pmset -g`
- **Live output on `ben-mac-mini`:**

```text
System-wide power settings:
Currently in use:
 standby              0
 Sleep On Power Button 1
 autorestartatconnect 0
 autorestart          1
 powernap             1
 networkoversleep     0
 disksleep            0
 sleep                0 (sleep prevented by caffeinate, caffeinate, caffeinate, caffeinate, powerd, Claude, caffeinate, caffeinate, caffeinate, caffeinate)
 ttyskeepawake        1
 displaysleep         0 (display sleep prevented by caffeinate, caffeinate, caffeinate, caffeinate)
 tcpkeepalive         1
 lowpowermode         0
 womp                 1
```

- **Answers:**
  - **Does it ever sleep (`sleep`, `disksleep`, `displaysleep`)?** **No.** `sleep = 0`, `disksleep = 0`, `displaysleep = 0`, and `standby = 0` (plus active `caffeinate` assertions).
  - **Does it wake for network access (`womp`)?** **Yes** (`womp = 1`).
  - **Does it start up by itself when power returns (`autorestart`)?** **Yes** (`autorestart = 1`).

---

## 2. Login & Post-Restart Recovery (`ben-mac-mini`)

- **Automatic login (`defaults read /Library/Preferences/com.apple.loginwindow autoLoginUser`):**
  - **Enabled** for account: `benjaminoats`
- **After a restart with nobody there, do the relay, the board publish, and the two Studio browsers come back without a person logging in?**
  - **Yes.** Because FileVault is **Off** (Item 3) and Automatic Login is enabled for `benjaminoats`, the Mac mini boots straight into the `benjaminoats` GUI session (`gui/501`) without waiting at a password screen, and `launchd` starts all user `LaunchAgents` in `~/Library/LaunchAgents`:
    1. **Chief relay (`com.owb.chief-relay`):** **Yes** — `RunAtLoad = true`, `StartInterval = 60` (every 60 s).
    2. **Board publish (`com.owb.board-publish`):** **Yes** — `RunAtLoad = true`, `StartInterval = 60` (every 60 s).
    3. **Studio Chrome browsers (`9222` HOS Flow, `9223` Orbit Studio, `9460` HOS Studio):** **Yes** — `~/Library/LaunchAgents/com.hos.cdp-browsers.plist` is loaded on the Mini with `RunAtLoad = true` and `StartInterval = 300` (every 5 min), running `/Users/benjaminoats/_desk/bin/cdp_browsers.sh start`. That script removes stale Chrome lock files after a crash/power cut and starts any down browser on ports `9222`, `9223`, and `9460` using their persistent signed-in profiles (`~/.hos-chrome-flow-*`, `~/.orbit-chrome-youtube-studio`, `~/.hos-chrome-youtube-studio`).
       - *(Housekeeping note: an older `~/Library/LaunchAgents/com.orbit.studio-chrome-9223.plist` also exists with `RunAtLoad = true` pointing to `/tmp/start-orbit-studio-9223.sh`, which is wiped when `/tmp` clears on reboot, but `com.hos.cdp-browsers` already brings up port `9223` cleanly on boot and every 5 minutes.)*
    4. **System-level mounts & network (`/Library/LaunchDaemons`):** `sh.brew.tailscale.plist`, `com.local.mountnas.plist`, and `com.local.mountnas-staging.plist` are also installed in `/Library/LaunchDaemons`, so Tailscale and the NAS mounts come back at boot as well.

---

## 3. Disk Encryption (`ben-mac-mini`)

- **Command:** `fdesetup status`
- **Live output on `ben-mac-mini`:**

```text
FileVault is Off.
```

- **What this means in plain English:**
  - Because FileVault is **Off**, the Mini does **not** stop at a pre-boot password screen after a power cut or restart; it boots straight into macOS, auto-logs into `benjaminoats`, and brings the relay, board publisher, NAS mounts, Tailscale, and Studio browsers back up by itself.
  - Conversely, if FileVault were turned **On**, macOS would disable Automatic Login and after any power cut or cold restart the Mini would wait at a pre-boot password screen (before Wi-Fi/Ethernet, Tailscale, `sshd`, or any `LaunchAgent` loads) until someone physically (or via local KVM) typed the password in.

---

## 4. Accounts

- **One-line summary (account names only):** On `ben-mac-mini`, all agents run as `benjaminoats`, which is the same account Ben uses himself (other non-system local account on the Mini: `michelleoats`); on `bens-macbook-pro`, all agents run as `ben`, which is also the same account Ben uses himself.

---

## 5. Remote Login (`ben-mac-mini`)

- **Commands:** `systemsetup -getremotelogin` and `launchctl print system/com.openssh.sshd`
- **Live output on `ben-mac-mini`:**
  - `systemsetup -getremotelogin` requires administrator (`sudo`) privileges (`You need administrator access to run this tool... exiting!`).
  - `launchctl print-disabled system | grep ssh` and `launchctl print system/com.openssh.sshd` confirm Remote Login (`sshd`) is **On (enabled and listening on TCP port 22 via launchd socket activation)**:

```text
"com.openssh.sshd" => enabled
Connection to 127.0.0.1 port 22 [tcp/ssh] succeeded!

system/com.openssh.sshd = {
    path = /System/Library/LaunchDaemons/ssh.plist
    type = LaunchDaemon
    state = not running (socket-activated on demand)
    sockets = {
        "Listeners" = {
            type = stream
            service name = ssh
            passive = 1
        }
    }
}
```

---

## 6. The Private Network (`tailscale status`)

Recorded live on `ben-mac-mini` at `2026-11-11T02:52Z` (account column redacted to `<tailscale-account>` per repo hygiene):

```text
100.96.7.11    ben-mac-mini       <tailscale-account>  macOS  -
100.88.13.103  bens-macbook-pro   <tailscale-account>  macOS  -
100.99.115.79  grokbot-box        <tailscale-account>  linux  offline, last seen 25d ago
100.86.131.62  iphone-14-pro-max  <tailscale-account>  iOS    -
100.86.193.52  oats-house-nas     <tailscale-account>  linux  -
```

- **Is the Mini on it?** **Yes** (`ben-mac-mini`, `100.96.7.11`, online).
- **Is the MacBook on it?** **Yes** (`bens-macbook-pro`, `100.88.13.103`, online).

---

## 7. Last Restart and Why (`ben-mac-mini`)

- **`uptime`:**

```text
 2:52  up 38 days,  6:33, 3 users, load averages: 2.04 2.97 2.98
```

- **`last reboot | head -5`:**

```text
reboot   ~                         Sat Oct  3 21:19
shutdown ~                         Sat Oct  3 21:18
reboot   ~                         Fri Sep 25 08:39
reboot   ~                         Thu Sep  3 16:24
shutdown ~                         Thu Sep  3 16:19
```

- **`pmset -g log | grep -i -E "shutdown cause|restart" | tail -5`:**
  - Empty output (`pmset -g log` in `/var/log/powermanagement` only retains entries back to `2026-11-04 02:53:20 +0000` because the Mini has been up continuously for **38 days** since `Sat Oct 3 21:19`, and `caffeinate` assertions have rotated the powermanagement log buffer).
  - `last reboot` shows the Oct 3 restart was a clean planned `shutdown` at `21:18` followed by `reboot` at `21:19` (1 minute later), unlike the unplanned `Fri Sep 25 08:39` reboot which had no preceding `shutdown` entry.

---

## 8. `launchd` Agents

### 8a. Live `launchctl list` and `~/Library/LaunchAgents` on `ben-mac-mini`

Live output of `launchctl list | grep -i owb` on `ben-mac-mini`:

```text
-       0   com.owb.missed-runs
-       0   com.owb.grokbot-watchdog
12847   0   com.owb.chief-relay
-       0   com.owb.cursor-worker
-       1   com.owb.ai-spend-daily
-       0   com.owb.board-publish
-       0   com.owb.tab-janitor
```

Additional studio LaunchAgents loaded in `gui/501` on `ben-mac-mini`:

```text
-       0   com.hos.cdp-browsers
14192   -15 com.hos.desk
8881    0   com.orbit.studio-chrome-9223
-       0   com.hos.local-wan-ltx-queue-reminder
-       1   dev.orbit.analytics-snapshot
-       1   dev.orbit.buffer-check
```

| Label (Mini) | Plist in `~/Library/LaunchAgents/` | Schedule | `RunAtLoad` | `KeepAlive` |
|---|---|---|---|---|
| `com.owb.chief-relay` | `com.owb.chief-relay.plist` | `StartInterval = 60` (every 1 min) | **`true`** | Not set (`false`) |
| `com.owb.board-publish` | `com.owb.board-publish.plist` | `StartInterval = 60` (every 1 min) | **`true`** | Not set (`false`) |
| `com.owb.missed-runs` | `com.owb.missed-runs.plist` | `StartInterval = 1800` (every 30 min) | **`true`** | Not set (`false`) |
| `com.owb.tab-janitor` | `com.owb.tab-janitor.plist` | `StartInterval = 300` (every 5 min) | **`true`** | Not set (`false`) |
| `com.owb.grokbot-watchdog` | `com.owb.grokbot-watchdog.plist` | `StartInterval = 300` (every 5 min) | **`true`** | Not set (`false`) |
| `com.owb.cursor-worker` | `com.owb.cursor-worker.plist` | `StartInterval = 1800` (every 30 min) | **`true`** | Not set (`false`) |
| `com.owb.ai-spend-daily` | `com.owb.ai-spend-daily.plist` | `StartCalendarInterval = 08:30` | Not set (`false`) | Not set (`false`) |
| `com.hos.cdp-browsers` | `com.hos.cdp-browsers.plist` | `StartInterval = 300` (every 5 min) | **`true`** | Not set (`false`) |
| `com.hos.desk` | `com.hos.desk.plist` | Daemon loop | **`true`** | **`true`** |
| `com.orbit.studio-chrome-9223` | `com.orbit.studio-chrome-9223.plist` | Login only (`/tmp/start-orbit-studio-9223.sh`) | **`true`** | **`false`** |
| `dev.orbit.analytics-snapshot` | `dev.orbit.analytics-snapshot.plist` | `StartCalendarInterval = 06:40` | Not set (`false`) | Not set (`false`) |
| `dev.orbit.buffer-check` | `dev.orbit.buffer-check.plist` | `StartCalendarInterval = 07:05` | Not set (`false`) | Not set (`false`) |

*(Note: legacy September Cursor GUI worker plists `com.cursor.mac-mini-*.plist` also still sit in `~/Library/LaunchAgents` with `RunAtLoad = true`, `KeepAlive = true` and exit code `1`.)*

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
- **Battery Power:** `sleep = 1` (1 min), `displaysleep = 2` (2 min), `disksleep = 10`, `womp = 0`, `powernap = 1`. (`macbook_worker.py` also checks `on_ac_power()` and refuses to start jobs on battery.)
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
  1. **While docked on AC power with an active external display** (an external `5120 x 2160` Ultra-wide 5K display is connected and `Online: Yes`): macOS enters closed-display (clamshell) mode and **does NOT sleep**, because `sleep = 0` on AC power. **The worker keeps running.**
  2. **When undocked (no external display active), even on AC power:** closing the lid triggers `AppleClamshellCausesSleep = Yes`, putting the MacBook to sleep immediately and **stopping the worker** until the lid is opened (unless system-wide sleep is disabled via `sudo pmset -a disablesleep 1`, which is risky if the laptop is ever put into a bag without turning it back off).

---

## Summary Table: Current vs. Target Settings for an Unattended Machine

| Setting | What it is now (`ben-mac-mini` / `bens-macbook-pro`) | What it should be for a machine nobody sits at | Who can change it |
|---|---|---|---|
| **Mini: System sleep (`sleep`)** | **`0`** (never sleeps; also held awake by `caffeinate`) | `0` (already right) | No change needed (**Ben** via `sudo pmset -a sleep 0`) |
| **Mini: Disk sleep (`disksleep`)** | **`0`** (never sleeps) | `0` (already right) | No change needed (**Ben** via `sudo pmset -a disksleep 0`) |
| **Mini: Display sleep (`displaysleep`)** | **`0`** (prevented by `caffeinate`) | `0` or `10` (already fine for headless Mini) | No change needed (**Ben** via `sudo pmset -a displaysleep`) |
| **Mini: Wake for network access (`womp`)** | **`1`** (enabled) | `1` (already right) | No change needed (**Ben** via `sudo pmset -a womp 1`) |
| **Mini: Restart automatically after a power cut (`autorestart`)** | **`1`** (enabled) | `1` (already right — boots itself when mains power returns) | No change needed (**Ben** via `sudo pmset -a autorestart 1`) |
| **Mini: FileVault disk encryption (`fdesetup status`)** | **`FileVault is Off.`** | **Off** if unattended recovery after a power cut is priority (already right); **On** only if physical theft protection outweighs unattended boot | No change needed for unattended boot (**Ben** if ever changed) |
| **Mini: Automatic Login (`autoLoginUser`)** | **Enabled** for `benjaminoats` | Enabled for `benjaminoats` (already right — lets user `LaunchAgents` start after a power cut without human login) | No change needed (**Ben** via System Settings → Users & Groups) |
| **Mini: Studio `launchd` agents (`RunAtLoad` / `KeepAlive`)** | `chief-relay` (`60s`), `board-publish` (`60s`), `missed-runs` (`1800s`), `tab-janitor` (`300s`), and `com.hos.cdp-browsers` (`300s`, ports `9222`/`9223`/`9460`) all have **`RunAtLoad = true`** and self-heal on interval. Legacy `com.orbit.studio-chrome-9223` (`/tmp` script) and old `com.cursor.mac-mini-*` plists are redundant | Already self-healing after reboot; optionally unload legacy `com.orbit.studio-chrome-9223` and old Sep `com.cursor.mac-mini-*` plists, and check `com.hos.cdp-browsers.plist` into git under `scripts/mini/` | **Agents** (user `~/Library/LaunchAgents`, no `sudo` needed) |
| **Mini & MacBook: Account separation** | Agents run as `benjaminoats` on Mini and `ben` on MacBook (same account Ben uses himself) | Keep as-is (shares signed-in Chrome Studio profiles, Keychain, and agent CLIs without duplicate logins) | No change needed (**Ben** if a separate OS account is ever wanted) |
| **Mini: Remote Login (`sshd`)** | **On** (`system/com.openssh.sshd` enabled, listening on TCP port 22) | On (already right — reachable over Tailscale IP `100.96.7.11`) | No change needed (**Ben** via System Settings → Sharing) |
| **Private network (`tailscale status`)** | Both `ben-mac-mini` (`100.96.7.11`) and `bens-macbook-pro` (`100.88.13.103`) online (`sh.brew.tailscale.plist` in `/Library/LaunchDaemons` on Mini) | Keep both online (already right) | No change needed |
| **MacBook: AC sleep & lid-closed behaviour** | AC `sleep = 0`, `womp = 1`; `AppleClamshellCausesSleep = Yes`; `sshd` off (`port 22 Connection refused`). Stays awake with lid closed **while docked to AC + external 5K display**; sleeps if lid is closed undocked | Keep clamshell sleep as-is (docked to AC + external display keeps worker running with lid closed; undocked lid-close sleeps safely before going in a bag). Optionally set `RunAtLoad = true` on `com.owb.macbook-worker.plist` | **Agents** (for `RunAtLoad = true` in `com.owb.macbook-worker.plist`); **Ben** if `disablesleep` or MacBook Remote Login is ever wanted |
