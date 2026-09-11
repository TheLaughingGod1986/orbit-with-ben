# Social cross-post audit — 2026-09-11 (read-only)

**Verdict:** YouTube is ahead. Instagram / Facebook / Threads are **not** caught up with Europa week + Neutron week. TikTok is correctly paused.

No posts were made during this audit.

## Sources of truth checked

| Source | Role | Freshness |
|--------|------|-----------|
| YouTube RSS + Shorts tab + oEmbed | What is actually live | Live 2026-09-11 |
| `audits/shorts_open_library/library.json` | Live + scheduled Short IDs | 2026-09-10 |
| `Meta/META_POSTED.json` | IG + FB Reel ledger | Last write **2026-09-04** |
| `Threads/THREADS_POSTED.json` | Threads Short ledger | Through JWST / early Last Star |
| `social/LONGS_POSTED.json` | Long soft-link ledger | **4** older films only (2026-09-04) |
| `TikTok/TIKTOK_UPLOAD_BLOCK.json` | Upload ban | `paused: true` since 2026-08-25 |
| `*/10_Shorts/SHORTS_UPLOAD_INDEX.json` | Meta/Threads discover input | Europa rows still `visibility: scheduled` |
| `social/live_longs.py` `KNOWN_LONGS` | Long share queue | Missing Neutron; Europa/Last Star still non-public flags |
| Meta auto log | Runner health | Still logging `nothing pending` every 5 min |

## Platform presence (live checks)

| Platform | Account | Present? | Evidence |
|----------|---------|----------|----------|
| YouTube | [@OrbitWithBen](https://www.youtube.com/@OrbitWithBen/shorts) | YES — current | Shorts tab shows Neutron teaspoon + Europa cluster; 7 longs oEmbed OK |
| Instagram | [@orbitwithben](https://www.instagram.com/orbitwithben/reels/) | PARTIAL — stale | Reels visible, but not Europa/Neutron week; `META_POSTED` last Sep 4 |
| Facebook | [Orbit with Ben](https://www.facebook.com/people/Orbit-with-Ben/61592833318203/) | PARTIAL — stale | Page live (34 followers); feed/Reels login-walled; same Meta ledger as IG |
| Threads | [@orbitwithben](https://www.threads.com/@orbitwithben) | PARTIAL — stale | Public feed shows Last Star soft post + Fermi/JWST/exoplanet; **no Europa/Neutron week** |
| TikTok | [@orbitwithben](https://www.tiktok.com/@orbitwithben) | INTENTIONALLY STALE | 3 early aliens videos only; upload block on |

Screenshots in this folder: `audit_youtube_shorts_tab.png`, `audit_instagram_reels.png`, `audit_facebook_page.png`, `audit_threads_feed.png`, `audit_tiktok_profile.png`.

## Long-form matrix

| Video | YT ID | YouTube | IG | FB | Threads | TikTok | Missing? |
|-------|-------|---------|----|----|---------|--------|----------|
| Fermi Paradox | `Mo93x0fxB1Q` | YES | n/a soft-link | ledger gap | YES (`LONGS_POSTED`) | paused | FB soft-link not logged |
| Black Hole | `3xrxdmaOwJI` | YES | n/a | ledger gap | YES | paused | FB soft-link not logged |
| Alien Worlds | `b8-X_FyJnHM` | YES | n/a | ledger gap | YES | paused | FB soft-link not logged |
| JWST | `ziKBPJ6FY0U` | YES | n/a | ledger gap | YES | paused | FB soft-link not logged |
| Last Star | `REXYxuLOBoI` | YES | n/a | NO ledger | LIVE on profile (not in `LONGS_POSTED`) | paused | Ledger drift; FB unclear |
| Europa | `NbW5G1BpPY0` | YES | n/a | NO | **NO** | paused | **Threads + FB** |
| Neutron Star | `Yk1tLh23rko` | YES | n/a | NO | **NO** | paused | **Threads + FB**; also absent from `KNOWN_LONGS` |

## Shorts matrix (live library IDs not in Meta/Threads ledgers)

Exact YouTube-ID overlap between live `shorts_open_library` and `META_POSTED` / Threads Short ledger: **0**.

All **17 live** library Shorts below are on YouTube and **missing** from Meta + Threads ledgers (TikTok paused for all):

| Date | YT ID | Title | YT | IG/FB | Threads | TikTok |
|------|-------|-------|----|-------|---------|--------|
| 08-27 | `SdNXS1PD_Yk` | Why the Night Sky Is Getting Darker | YES | NO | NO | paused |
| 08-28 | `IVbO9XkkDps` | The Day the Last Star Goes Out | YES | NO | NO | paused |
| 08-30 | `GjcZB8826J8` | It Rains Glass Sideways on This Alien World | YES | NO* | NO | paused |
| 09-01 | `9lLZMy8rBJo` | What Remains After the Last Star Dies? | YES | NO | NO | paused |
| 09-01 | `CkSECfUfH2Y` | The Sky Is Already Running Out of Light | YES | NO | NO | paused |
| 09-01 | `KX-XU_AODoI` | What Happens When the Last Star Furnace Goes Cold | YES | NO | NO | paused |
| 09-02 | `n2WbOfJhOwc` | Star Recycling Isn't Perfect | YES | NO | NO | paused |
| 09-03 | `QNTeou-w-gY` | There's an Ocean Under That Ice | YES | NO | NO | paused |
| 09-03 | `keXe1GNxWSU` | Those Ice Scars Are How You Find It | YES | NO | NO | paused |
| 09-04 | `8Bym-yrYhGc` | Why Europa's Ocean Shouldn't Exist | YES | NO | NO | paused |
| 09-05 | `1glQuYFSaYQ` | What Would Life Eat Under Europa? | YES | NO | NO | paused |
| 09-05 | `pII09FbRYGc` | Why Europa Is Hiding a Massive Ocean. | YES | NO | NO | paused |
| 09-06 | `Xza_jSHD4qw` | How Life Could Feed Under Europa With No Sun | YES | NO | NO | paused |
| 09-07 | `VE0f186WQZo` | Europa Sprays Its Ocean Into Space | YES | NO | NO | paused |
| 09-08 | `eVp9a7f4rWg` | We Could Kill the Life We're Looking For | YES | NO | NO | paused |
| 09-09 | `TE_HDKAnqms` | If Life Starts Under Ice, It's Everywhere | YES | NO | NO | paused |
| 09-10 | `fhJP6eMoU0Q` | Your Atoms Near a Neutron Star Do Not Survive | YES | NO | NO | paused |

\*Meta ledger has an older/different ID for a glass-rain title (`ho9VJxp7f3A`, still marked scheduled) — not this live ID.

### Already covered on Meta (ledger, pre-Europa)

Aliens punch set + JWST Shorts + `PV50PX-bE4g` (“Most of the Universe Gives Off No Light”) — IG/FB marked `posted`/`ok` on **2026-09-04**. Black-hole + exoplanet rows remain `scheduled` in the ledger (and still `scheduled` in indexes).

### Scheduled ahead (YouTube only for now)

Neutron mystery slots 11–17 Sep (RSS already shows `vCxXTYXSSqY` live today) — social will stay empty until indexes + autos are fixed (TikTok still paused).

## Root cause (why autos say “nothing pending”)

1. **Discover only trusts `SHORTS_UPLOAD_INDEX.json`.** Europa (and reminted Last Star) rows are still `visibility: "scheduled"` even though YouTube/RSS show them public → Meta/Threads treat them as not live.
2. **No Neutron `SHORTS_UPLOAD_INDEX.json`** under `007_…Neutron-Star/10_Shorts/` → Neutron Shorts never enter the Meta/Threads queue.
3. **`KNOWN_LONGS` is stale:** Neutron long missing; Europa still `scheduled`; Last Star still `premiere` → long soft-share watcher will not queue them.
4. **TikTok** correctly no-ops while `TIKTOK_UPLOAD_BLOCK.json` is paused.

## What is complete

- YouTube catalogue for published longs (7) and current Shorts cluster through 10 Sep (+ today’s teaspoon Short).
- Meta/Threads coverage for early aliens + JWST Shorts (ledger).
- TikTok pause respected (3 early videos only; no new uploads).

## What is missing (post next — do not auto-post without Ben)

**P0 — longs soft-links (Threads + FB):** Europa `NbW5G1BpPY0`, Neutron `Yk1tLh23rko` (and reconcile Last Star into `LONGS_POSTED`).

**P0 — Shorts IG + FB + Threads:** all 17 live library IDs above, starting with Europa week then Neutron `fhJP6eMoU0Q` / today’s teaspoon `vCxXTYXSSqY`.

**P1 — unblock autos (ops, not posting):** flip Europa/Last Star index rows to `public`; add Neutron Shorts index; update `KNOWN_LONGS`; then let watchers catch up (still skip TikTok).

**Do not:** upload to TikTok until Ben lifts the ban.
