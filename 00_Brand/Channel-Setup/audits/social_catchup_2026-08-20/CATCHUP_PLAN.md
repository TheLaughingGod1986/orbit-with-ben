# Social catch-up — 20 Aug 2026

**Why nothing went live “the last few days”:** ledgers last wrote on **3 Aug**. TikTok was banned from posting. Meta’s Suite batch ended **17 Aug**. Exo YouTube Shorts do not start until **21 Aug**. Threads/TikTok/Meta watchers are Mac LaunchAgents + Chrome CDP — they do not run from this cloud repo.

**Rules (locked):** YouTube-first · TikTok = YT **T0 + 1h** · Shorts **zero** `/go/` · JWST film = YouTube URL only (no `/go/jwst-book`) · never dump a full cluster in one day · do not invent ASINs / merchant URLs.

Canonical refs: `TikTok/AUTO_POST.md` · `Meta/AUTO_POST.md` · `Threads/AUTO_POST.md` · `SHORTS_FUNNEL_AND_CROSSPOST.md` · `PLATFORM_STATUS.json` (3 Aug).

---

## Phase 0 — diagnose on Ben’s Mac (15 min)

Run on the Orbit Mac (not cloud):

```bash
# 1) LaunchAgents present?
launchctl list | grep -E 'orbit\.(tiktok|meta|threads)' || true

# 2) Recent watcher logs
tail -n 80 ~/code/Orbit-YouTube/00_Brand/Channel-Setup/TikTok/auto_launchd.err.log 2>/dev/null
tail -n 80 ~/code/Orbit-YouTube/00_Brand/Channel-Setup/Meta/auto_post.log 2>/dev/null
tail -n 80 ~/code/Orbit-YouTube/00_Brand/Channel-Setup/Threads/auto_post.log 2>/dev/null

# 3) What watchers think is due
cd ~/code/Orbit-YouTube
python3 00_Brand/Channel-Setup/TikTok/auto/live_shorts_to_tiktok.py --list
python3 00_Brand/Channel-Setup/Meta/auto/live_shorts_to_meta.py --list
python3 00_Brand/Channel-Setup/Threads/auto/live_shorts_to_threads.py --list
```

**TikTok ban check (blocking):** open TikTok mobile → Notifications. If still “temporarily prevented from posting” / check-limit, **stop TikTok uploads** until it clears. Meta + Threads can still catch up.

Mark `STATUS.json` → `phase0_done`.

---

## Phase 1 — restore watchers (before any catch-up posts)

```bash
# Chrome CDP profiles (log into @orbitwithben once if needed)
bash 00_Brand/Channel-Setup/TikTok/auto/start_tiktok_chrome.sh   # :9222
bash 00_Brand/Channel-Setup/Meta/auto/start_meta_chrome.sh       # :9223
bash 00_Brand/Channel-Setup/Threads/auto/start_threads_chrome.sh # :9222 shared OK if TT idle

# Reload LaunchAgents
cp 00_Brand/Channel-Setup/TikTok/auto/dev.orbit.tiktok-live-shorts.plist ~/Library/LaunchAgents/
cp 00_Brand/Channel-Setup/Meta/auto/dev.orbit.meta-live-shorts.plist ~/Library/LaunchAgents/
cp 00_Brand/Channel-Setup/Threads/auto/dev.orbit.threads-live-shorts.plist ~/Library/LaunchAgents/
launchctl unload ~/Library/LaunchAgents/dev.orbit.tiktok-live-shorts.plist 2>/dev/null; true
launchctl unload ~/Library/LaunchAgents/dev.orbit.meta-live-shorts.plist 2>/dev/null; true
launchctl unload ~/Library/LaunchAgents/dev.orbit.threads-live-shorts.plist 2>/dev/null; true
launchctl load ~/Library/LaunchAgents/dev.orbit.tiktok-live-shorts.plist
launchctl load ~/Library/LaunchAgents/dev.orbit.meta-live-shorts.plist
launchctl load ~/Library/LaunchAgents/dev.orbit.threads-live-shorts.plist
launchctl list | grep orbit
```

Dry-run once (no publish):

```bash
python3 00_Brand/Channel-Setup/Meta/auto/live_shorts_to_meta.py --dry-run
python3 00_Brand/Channel-Setup/Threads/auto/live_shorts_to_threads.py --dry-run
python3 00_Brand/Channel-Setup/TikTok/auto/live_shorts_to_tiktok.py --dry-run
```

Mark `STATUS.json` → `phase1_watchers_loaded`.

---

## Phase 2 — fill the 18–20 Aug hole (do not dump)

Today is **Thu 20 Aug**. Cadence expects a daily Short; socials mirror Shorts, not the long alone.

| Day | Hole fill (pick ONE) | Do not |
|-----|----------------------|--------|
| **18 Aug** (past) | If YT aliens-03 `rFJoOdQAc9c` is public and Threads/Meta missing → one soft mirror only | Do not re-post assets already live on IG/FB from 3 Aug sync |
| **19 Aug** (past) | Catch up **one** overdue black-hole Short already public on YT (see Phase 3 order) | Do not post exo before YT T0 |
| **20 Aug** (today) | JWST long only if public: **one** soft Threads + IG caption with **YouTube film URL** · no Short · no `/go/` | Do not invent JWST Shorts or affiliate doors |

Soft JWST social line (film URL only):

> JWST keeps finding galaxies that shouldn’t be there yet. Full film on YouTube → https://youtube.com/@OrbitWithBen

(Replace with the exact JWST watch URL once Studio shows it public.)

Mark `STATUS.json` → `phase2_hole_filled`.

---

## Phase 3 — catch up overdue black-hole mirrors (YT already due)

Index dates (Europe/London) — all **before** today, so if Studio made them public they are overdue on social:

| # | YT id | Title | YT T0 | Social catch-up |
|---|-------|-------|-------|-----------------|
| 01 | `2777WlMGM8M` | Cross This Line… | 5 Aug 21:00 | Meta + Threads now · TikTok now **or** schedule T0+1h if ban clear |
| 02 | `jyzrl9ueKq4` | Falling In… | 6 Aug 12:30 | same |
| 03 | `HvAKGjx4lv0` | Time Stops… | 7 Aug 12:30 | same |
| 04 | `t1hTGIH8O44` | Would You Look Back? | 8 Aug 12:30 | same |
| 05 | `icedH_gK8JE` | What Your Eyes Would See | 9 Aug 12:30 | same |
| 06 | `5jjJ5CHrbCs` | Point of No Return | 10 Aug 12:30 | same |

**Pace:** max **2** catch-up Shorts/day across platforms (one morning, one evening). Prefer monster-hook order: **01 → 02 → …**

### Meta (preferred Graph, else CDP)

```bash
python3 00_Brand/Channel-Setup/Meta/auto/live_shorts_to_meta.py --check-creds
python3 00_Brand/Channel-Setup/Meta/auto/live_shorts_to_meta.py --once
# If Suite still holds old Aug 12–17 exo schedules that beat YT T0, delete those drafts in Suite first (YT-first).
```

### Threads

```bash
python3 00_Brand/Channel-Setup/Threads/auto/live_shorts_to_threads.py --once
```

### TikTok (only after ban clears)

```bash
# Verify ban gone in Studio UI first, then:
python3 00_Brand/Channel-Setup/TikTok/_tt_upload_one_safe.py blackhole-01
# Confirm Studio schedule / Post-now + ledger row, then continue:
python3 00_Brand/Channel-Setup/TikTok/_tt_upload_one_safe.py blackhole-02
# … through blackhole-06
# Or when safe: python3 00_Brand/Channel-Setup/TikTok/_tt_upload_one_safe.py --all-remaining
# (script bumps past-due times to now+1h — still verify each Studio row)
```

If Studio returns `status_code: 21` again → stop, set `STATUS.json` `tiktok_still_banned: true`, continue Meta/Threads only.

Also finish **aliens-clue** `KcKBixwmcV4` on TikTok if still missing (blocked on 3 Aug).

Mark `STATUS.json` → `phase3_bh_catchup`.

---

## Phase 4 — lock exo cluster for 21–26 Aug (forward path)

YouTube SoT (`003` `SHORTS_UPLOAD_INDEX.json`):

| Short | YT id | YT T0 UK | TikTok | Meta / Threads |
|-------|-------|----------|--------|----------------|
| Glass rain | `ho9VJxp7f3A` | **21 Aug 21:00** | 22:00 | watcher at YT live (+ soft CTA) |
| Diamond | `aoR-dA_g7eI` | 22 Aug 12:30 | 13:30 | watcher |
| Three suns | `6QFGAFZk264` | 23 Aug 12:30 | 13:30 | watcher |
| Hot Jupiter | `eOOFVrJ2Ojc` | 24 Aug 12:30 | 13:30 | watcher |
| Eyeball | `Web2otrTcT0` | 25 Aug 12:30 | 13:30 | watcher |
| Habitable | `1qts3tIsg9c` | 26 Aug 12:30 | 13:30 | watcher |

**Before 21 Aug 21:00:**

1. Confirm Alien Worlds long `b8-X_FyJnHM` is public (or will be) before Short #1.
2. Delete any **premature** Meta Suite exo schedules dated **12–17 Aug** (those beat current YT T0).
3. Prefer **watchers at go-live** over pre-scheduling Meta ahead of YT.
4. TikTok: either pre-schedule at **YT T0 + 1h** with `_tt_upload_one_safe.py exoplanets-01` … `06` **after ban clears**, or let the TikTok watcher Post-now when YT is live (+1h grace is fine).
5. Seed ledgers only for assets already truly live — do not `--seed-all` overdue BH if you still need them posted.

```bash
# Night before / morning of 21 Aug — sanity
python3 00_Brand/Channel-Setup/TikTok/auto/live_shorts_to_tiktok.py --dry-run
python3 00_Brand/Channel-Setup/Meta/auto/live_shorts_to_meta.py --dry-run
python3 00_Brand/Channel-Setup/Threads/auto/live_shorts_to_threads.py --dry-run
```

Mark `STATUS.json` → `phase4_exo_armed`.

---

## Phase 5 — verify matrix + write ledger

After each catch-up day, update:

| Platform | Live BH 01–06? | Exo armed? | Notes |
|----------|----------------|------------|-------|
| YouTube | | 21–26 sched | Index vs Studio |
| Instagram | | | Reel codes |
| Facebook Page | | | Page Reels tab |
| Threads | | | Profile grid + permalink |
| TikTok | | | Ban cleared? |

Copy results into `VERIFY_MATRIX.json` and bump `META_POSTED.json` / `TIKTOK_POSTED.json` / `THREADS_POSTED.json` via the watcher scripts (preferred) — do not hand-edit unless a CDP confirm already shipped.

Mark `STATUS.json` → `phase5_verified` when BH catch-up + exo arming both done.

---

## Explicit non-goals

- Do **not** retrofit affiliate `/go/` onto JWST, Alien Worlds, Black Hole, or Fermi.
- Do **not** build JWST Shorts in this catch-up (leave JWST as-is per lock).
- Do **not** start 013 Moon or batch-generate 007 socials here.
- Do **not** run social CDP from the cloud agent — Mac only.

---

## Ordered checklist (copy into STATUS)

See `STATUS.json` + `QUEUE.json` in this folder.
