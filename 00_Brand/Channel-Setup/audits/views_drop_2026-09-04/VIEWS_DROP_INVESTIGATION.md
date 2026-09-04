# Views drop investigation — 2026-09-04

Channel: Orbit with Ben (`UC_esArsDKd3GJvOkeO0DUog`) · 5 subs · ~3.5k views / 28d

## Verdict

**Not a broken clock / not a channel ban.** Visibility and Related on live Shorts are fine. The drop lines up with a **Sep 3 Europa cluster dump** (4 Shorts in one day, two at the same minute) plus **Private remint siblings**, after a Last Star week that was still hitting 200–600.

## Evidence (public views at investigation)

| Date (UK) | # Shorts | Views | Notes |
|-----------|----------|-------|-------|
| 4 Sep | 1 | 2 | Europa Fri punch — still early, but cold |
| **3 Sep** | **4** | 2 / 62 / 35 / 17 | **Cadence breach** · two at **20:00 same minute** |
| 2 Sep | 1 | **205** | Same 11:30 slot as today’s dud — slot still works |
| 1 Sep | 3 | **613** / **288** / 5 | Last Star remints · double-post 14:39–14:40 |
| 31 Aug | 1 | 10 | Quiet day |
| 30 Aug | 1 | 6 | Quiet day |
| 29 Aug | 1 | **409** | Last Star title (later reminted 1 Sep) |

Studio check (CDP, logged in): recent Europa + Last Star Shorts are **Public**, Related set correctly (Europa → `NbW5G1BpPY0`, Last Star → Last Star long). No Checks/limited flag on those edit pages.

## Root causes (ranked)

1. **Cadence spam on Europa launch day** — house rule is **one Short / day**. 3 Sep published **four**. Two went out at **identical 20:00 BST**. YouTube Shorts feed treats same-channel bursts as low-quality / competitive with yourself.
2. **Remint / Private twin clutter** — checklist IDs for Europa punches are now **Private** (`eVp9a7f4rWg`, `1glQuYFSaYQ`, `Xza_jSHD4qw`, …) while different Public IDs carry the same titles. That matches the Sep 4 Private-restore incident. Twins split history and can confuse scheduling.
3. **Topic/packaging variance (secondary)** — Last Star “end of light / remains” hooks were the 200–600 winners. Europa “ocean under ice” cluster is softer so far. Variance is real; it is **not** the whole story when 4 posts land in 24h.
4. **Not the cause:** timezone clock, Related missing, Public→Private on the live keepers (those are Public), channel-wide strike/limited (no Studio signal).

## What to do (fix)

### Immediate (today)

1. **Do not publish another Short today.** Let 4 Sep breathe.
2. **Audit scheduled Europa leftovers (5–9 Sep):** one Public ID per day only; Private twins stay Private forever (or delete) — never re-schedule them.
3. **Hard lock:** never two `publishAt` timestamps on the same calendar day; never two at the same minute.

### Next 48–72h

4. Keep **one Short / day at 11:30 UK** only (skip Thu 20:00 launch Short this week if it would double-post).
5. Prefer the strongest Europa title still scheduled; skip weakest near-duplicates.
6. Watch **impressions** in Studio (not just views). If impressions ≈ 0 after 24h → packaging/feed. If impressions high / views low → retention.

### Process (so this doesn’t repeat)

7. Scheduler must refuse a second Short if another is already Public/Scheduled that UK day.
8. Remint rule: new file = new ID only when replacing; old ID stays Private and is **removed from all schedules / indexes**.
9. Don’t remint a winning title twice in 72h (Last Star “What Remains…” on 29 Aug **and** 1 Sep).

## Not recommended

- Mass reuploads to “reset” the algorithm
- Dumping more Europa Shorts tomorrow to compensate
- Changing niche off one cold cluster
- Blaming 11:30 UK — Sep 2 11:30 did 205

## Fix applied 2026-09-04 (Studio live)

| Action | ID | Result |
|--------|-----|--------|
| Private Sep 3 duplicate | `keXe1GNxWSU` | **Private** |
| Private Sep 3 extra | `QNTeou-w-gY` | **Private** |
| Move Neutron Touch off double-book | `Rp_8J6_6IIk` | **10 Sep 20:00 → 14 Sep 11:30** |
| Leave launch keeper Public | `MXrq1-ggtXo` | Public (twin `eVp9a7f4rWg` Private) |
| Confirm Europa 5–9 Sep | one each @ 11:30 | No collisions |
| Confirm Neutron 10–14 Sep | one each @ 11:30 | No collisions |
| Leftover | `0j_pgYbCe5E` | 18 Sep 11:30 only |

Verify artifact: `europa_week_fixed_verify.json`. Checklist updated.

## Artifacts

- `recent_shorts_public.json`
- `studio_recent_visibility.json`
- `europa_week_fixed_verify.json`
- This file
