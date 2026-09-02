# Social ↔ YouTube Studio parity — 1 Sep 2026

**Verdict: not in parity.** YouTube is ahead. Repo social ledgers and most Shorts indexes are stale. TikTok is intentionally paused.

| Surface | State | Evidence |
|---------|--------|----------|
| **YouTube Shorts** | **30 live** on channel Shorts tab | Playwright scrape + oEmbed OK |
| **YouTube longs** | 6 public (Fermi, BH, Alien Worlds, JWST, Last Star, Europa) | oEmbed OK |
| **Meta ledger** | **0 / 30** live Short IDs · last write **3 Aug** | `META_POSTED.json` |
| **Threads ledger** | **0 / 30** live Short IDs · last write **3 Aug** | `THREADS_POSTED.json` |
| **TikTok ledger** | **0 / 30** · paused since **25 Aug** | `TIKTOK_POSTED.json` + `TIKTOK_UPLOAD_BLOCK.json` |
| **Threads live profile** | Has posts (exo / JWST / Last Star soft links through ~28 Aug) | Public `@orbitwithben` — **ahead of ledger** |
| **Facebook Page** | At least Last Star soft post ~4d ago | Public page, 33 followers |
| **Instagram** | **Unverified** (login wall from this cloud) | Needs Mac/Suite check |
| **TikTok live** | Effectively empty (~2 followers / 0 likes) | Ban + pause |

Raw: `LIVE_YT_SHORTS.json` · `PARITY_MATRIX.json`

---

## Root causes

1. **Shorts indexes drift** — `001` / `002` / `003` `SHORTS_UPLOAD_INDEX.json` still carry **2–3 Aug** `video_id`s and many rows stay `visibility: scheduled`. Live remakes use **different IDs**. Overlap today: **9 / 30** live Shorts appear in any index; **21** live IDs are missing from indexes; **19** index IDs are not on the live Shorts tab.
2. **Watchers only trust the index** — `Meta/auto/discover.py` / Threads discover require `visibility: public` (or `published_now`). Stale `scheduled` rows never enqueue, even when YouTube already remade the Short.
3. **Ledgers frozen** — Meta/Threads posted maps still key the **old** aliens IDs from the 3 Aug sync. No ledger row matches any of today’s 30 live Short IDs.
4. **TikTok pause (locked)** — `TIKTOK_UPLOAD_BLOCK.json` `paused: true`. Do not lift until Ben says so.
5. **Longs ledger missing** — `social/LONGS_POSTED.json` is not in the repo, so long link-share state cannot be audited from git.
6. **Aug 20 catch-up never closed in repo** — `audits/social_catchup_2026-08-20/STATUS.json` still all `false`.

---

## What *is* working (outside the ledger)

- **Threads** public grid shows real orbit posts (glass rain, diamond worlds, three suns, JWST “shouldn’t be there”, Fermi zoo, Last Star CTA). So some Mac-side posting happened after 3 Aug — it just never updated `THREADS_POSTED.json` against live YT IDs.
- **Facebook Page** shows at least one recent Last Star soft post.
- **YouTube** catalogue is healthy (30 Shorts + 6 longs public).

---

## Mac fix order (do this on the posting Mac)

### A. Resync Shorts indexes to Studio (blocking)

For every live Short ID in `LIVE_YT_SHORTS.json`:

1. Confirm Public in YouTube Studio.
2. Update the matching `02_Video-Projects/*/10_Shorts/SHORTS_UPLOAD_INDEX.json` row: correct `video_id`, `visibility: public`, `published_now: true`, drop stale schedule if already live.
3. Retire / note old IDs that 403 (aliens/BH/exo remakes).

Until indexes match Studio, LaunchAgents cannot catch up Meta/Threads correctly.

### B. Confirm LaunchAgents + Chrome

```bash
launchctl list | grep -E 'orbit\.(meta|threads|live-longs)' || true
# Meta :9223 · Threads :9222 logged into Orbit accounts
```

Keep TikTok plists unloaded while `TIKTOK_UPLOAD_BLOCK.json` is paused.

### C. Catch up Meta (IG + FB) for missing live Shorts

```bash
VENV=00_Brand/Channel-Setup/.venv-social/bin/python
$VENV 00_Brand/Channel-Setup/Meta/auto/live_shorts_to_meta.py --list
$VENV 00_Brand/Channel-Setup/Meta/auto/live_shorts_to_meta.py --dry-run
$VENV 00_Brand/Channel-Setup/Meta/auto/live_shorts_to_meta.py --once
```

Pace: do **not** dump 30 Reels in one day — uniqueness window + brand quality. Prefer newest clusters first (Last Star → JWST → exo → BH → aliens), max a few per day unless Ben asks for a full backfill.

### D. Threads ledger reconcile

```bash
$VENV 00_Brand/Channel-Setup/Threads/auto/live_shorts_to_threads.py --list
$VENV 00_Brand/Channel-Setup/Threads/auto/live_shorts_to_threads.py --once
```

Where a Short is already on the Threads profile, **seed** the ledger to the live YT id (do not duplicate).

### E. Longs soft shares

Seed / create `social/LONGS_POSTED.json`, then:

```bash
$VENV 00_Brand/Channel-Setup/social/live_longs_to_social.py --list
$VENV 00_Brand/Channel-Setup/social/live_longs_to_social.py --once
```

Europa is already public on YouTube — include it if FB/Threads lack the soft link.

### F. Instagram Suite eyeball (cloud cannot)

In Meta Business Suite, confirm Orbit IG Reels count vs the 30 live YT Shorts. Note gaps in `VERIFY.md` (optional follow-up).

### G. TikTok

Leave paused. After Ben lifts the ban: clear `TIKTOK_UPLOAD_BLOCK.json`, then backfill from live indexes (YT T0 + 1h rule).

---

## Target state

| Check | Pass when |
|-------|-----------|
| Every public YT Short ID is in the correct `SHORTS_UPLOAD_INDEX` as `public` | indexes = Studio |
| Meta ledger has `yt:{id}` posted/seeded for each unique Short chosen for IG/FB | uniqueness respected |
| Threads ledger matches profile (no dupes) | seeded + watcher |
| `LONGS_POSTED.json` lists all 6 public longs on FB/Threads soft share | longs watcher |
| TikTok either still paused **or** ban lifted + backfill started | Ben gate |
| This audit’s `STATUS.json` phases flipped true | closed loop |

---

## Out of scope here

- Posting from this cloud agent (no Mac CDP / Suite session)
- Lifting TikTok ban
- Affiliate `/go/` on Shorts (still zero)
