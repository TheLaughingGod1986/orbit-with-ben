# Orbit with Ben — full audit (YouTube + social + queue)

**Date:** Tuesday 25 Aug 2026, ~23:00 UK  
**Channel:** Orbit with Ben (`@OrbitWithBen` · `UC_esArsDKd3GJvOkeO0DUog`)  
**Age:** 29 days (created 27 Jul 2026)

Companion: evening narrative `CHANNEL_AUDIT.md` · raw `vidiq_raw.json` · night RSS `public_views.json`.

---

## Executive verdict

Still a **Shorts discovery engine with almost no long-form hold**. That is normal at **4 subscribers**. Do not rewrite the brand, chase fearbait, or recut shipped films to remove Orbit.

| Signal (night refresh) | Value | Confidence |
|---|---|---|
| Subscribers / lifetime views / videos (vidIQ 18:10 UTC) | **4 · 949 · 27** | HIGH |
| Public Shorts shelf (RSS, ~23:00 UK) | Top Short **141** views; today’s JWST Short **30** (was 17 earlier) | HIGH |
| Public longs combined | Fermi 10 · Alien Worlds 10 · JWST 7 · BH 4 · Last Star premiere **3** | HIGH |
| Shorts ≈ long catalogue | Shorts shelf still ~8–9× the live longs | HIGH |
| vidIQ analytics / title scores / keywords | Failed mid-pull — **4** add-on credits left; renews **30 Aug 22:23 UTC** | — |
| YouTube Data API catalogue | Quota blown earlier today | — |
| TikTok uploads | **Paused** (account ban) | HIGH |
| Meta / Threads auto-mirrors in this workspace | Agents **not installed**; ledgers stale vs YouTube | HIGH |

**Take into Neutron / Europa packaging:** punch-first Shorts, scene-first covers, VO-literal picture, Orbit in the scene, **7–9 min** longs. Fix ops hygiene (indexes + JWST Shorts index + social ledgers). Do not spend generation budget recutting old Shorts.

---

## 1. YouTube — what is working

### Shorts titles that look like a real shelf

Public views night refresh (RSS + watch-page for older longs). Age varies; rank is directional.

| Views | Title | ID | Why it fits |
|------:|-------|----|-------------|
| **141** | Three Suns in the Sky — Real Alien Worlds | `MDvAKtmKauw` | Concrete image. Remake of a weak original. Diamond-bar pattern. |
| **122** | Most of the Universe Gives Off No Light | `PV50PX-bE4g` | Strange fact, drawable, named subject. |
| **89** | These Galaxies Appeared Too Early | `l1d1ypHxLk0` | JWST launch Short. |
| **83** | Why JWST Pictures Don't Match the Textbook | `P-li_ZWk4lg` | Named subject + contradiction. |
| **69** | Why This Alien World Looks Like a Giant Eye | `OlwENQcY-jg` | Drawable object in the title. |
| **68** | Is the Universe Older Than We Thought? | `4-ZEpKD1yak` | Wrongness inside the question. |
| **63** | We Found Planets Made of Diamond | `M-VN84HCNls` | House winner / punch study. |
| **52** | What If They're Leaving Us Alone On Purpose | `03v4f1hlvtQ` | Fermi-cluster experiential. |
| **30** | JWST Keeps Finding Galaxies Too Big, Too Soon | `68uTDP2esso` | Posted today; climbing (17 → 30 same evening). |

Pattern lock: **image words first, subject named, no series suffix, no orphan “this/it.”**

### Craft locks that earned their keep

1. Punch-first **22–27s** Shorts (never ≥40s).
2. Picture tells the story (mute test; teaspoon vs mountains gold).
3. Orbit in the video is fine — scene-first is a **cover/thumb** rule, not a recut rule.
4. ≥2 pure-scenery plates per minute for native covers.
5. Shorts covers: **Studio desktop only** (Data API letterboxes 9:16).
6. Open/end: first 3s strange picture; Orbit after ~8s; last 10s real picture for Studio end screens.
7. One-minute Omni path + Ben UAT.

---

## 2. YouTube — what is not working (or not yet)

### Longs are cold — and the live ones are still too long

| Film | Runtime | Views | Notes |
|------|--------:|------:|-------|
| Fermi `Mo93x0fxB1Q` | ~18:32 | **10** | Series-suffix era. |
| Alien Worlds `b8-X_FyJnHM` | ~21:29 | **10** | Same generation. |
| JWST `ziKBPJ6FY0U` | ~16:33 | **7** | Live 5 days; Shorts cluster 17–89 vs parent 7. |
| Black Hole `3xrxdmaOwJI` | ~21:13 | **4** | Weakest public long. |
| Last Star `REXYxuLOBoI` | premiere | **3** | **Do not judge.** Thu **27 Aug 18:00**. Title still has `\| Orbit's Cosmic Journey`. |
| Europa `NbW5G1BpPY0` | scheduled | — | Watch page unavailable (expected). Thu **3 Sept**. |
| Neutron `Yk1tLh23rko` | scheduled | — | Next to *make*, not next to air. Unavailable on watch page (expected). |

**Implication:** 18–21 min lives are catalogue, not template. New longs stay **7–9 min**.

### Shorts → long funnel not converting yet

Expected at 4 subs. Job remains: Short earns the click; listing + first 15s of the long earn the stay. No `/go/` or shop voice to “help.”

### Weak / orphan Shorts

| Views | Title | Lesson |
|------:|-------|--------|
| 19 | Black Holes Grew Too Big, Too Fast | Abstract process, not a picture. |
| 16 | This Planet's Night Never Cools Down | Superlative / weather, weak picture words. |
| **9** | Time Appears to Stop at a Black Hole (`tUAdhOnMW2g`) | Public, **not in Uploads-only walks**. Keep in inventory. |

### Indexes 001–003 are stale (reconfirmed night)

| Episode | Index problem |
|---------|----------------|
| **001** Fermi | Still points at deleted/unavailable IDs (`1HuV8o3gOss`, etc.). |
| **002** Black Hole | Six rows still `scheduled` with corpse IDs (`2777WlMGM8M` … `5jjJ5CHrbCs`) — TikTok hammered these tonight until pause. |
| **003** Alien Worlds | Still `scheduled` with old IDs while live remakes are `M-VN84HCNls` / `MDvAKtmKauw`. |
| **004** JWST | **No** `10_Shorts/SHORTS_UPLOAD_INDEX.json` in this repo tree — discover cannot queue today’s Short. |

Social mirrors and comment watchers read these files. Seeding alone is not enough; indexes need a **true live-ID rewrite**.

---

## 3. Social ops audit

### TikTok — correctly paused

| Check | State |
|-------|--------|
| `TikTok/TIKTOK_UPLOAD_BLOCK.json` | `"paused": true` since `2026-08-25T20:38:00+01:00` |
| `dev.orbit.tiktok-live-shorts.plist` | `Disabled=true` + `TIKTOK_UPLOADS_PAUSED=1` + new Mac path |
| `dev.orbit.tiktok-reupload-missing.plist` | `Disabled=true`; paths migrated to `benjaminoats/...` in this PR |
| Tonight’s failures | Black Hole **scheduled corpses** (`2777WlMGM8M` …), not JWST — until pause at 20:38 |
| Platform ban | Status **21** / CG temp ban still on record (3 Aug) |

**Do not** reload or run any TikTok uploader until Ben lifts the block.

### Uniqueness (Ben 25 Aug)

- Helper: `social/uniqueness.py` — one unique Short per IG / FB / Threads; remake / file / title fingerprints; ~30-post window.
- Meta / Threads discover already use it; TikTok discover/ledger now match (this PR).
- Ledgers themselves show **no** title/file collisions in the last ~30 done entries.
- Ledgers are **stale vs YouTube**: Meta/Threads last `updated_at` **3 Aug**; no `68uTDP2esso` on any social ledger in-repo.

### LaunchAgents (this cloud workspace)

`launchctl list | rg orbit` → **no matches**. Repo plists exist; **none** installed under `~/Library/LaunchAgents` here. Earlier “LaunchAgents reloaded” refers to Ben’s posting Mac, not this environment.

| Agent | Should load on posting Mac? |
|-------|------------------------------|
| `dev.orbit.meta-live-shorts` | Yes (after path copy) |
| `dev.orbit.threads-live-shorts` | Yes |
| `dev.orbit.tiktok-live-shorts` | **No** until ban lift |
| `dev.orbit.tiktok-reupload-missing` | **No** |

### Today’s JWST Short mirror

| Item | Finding |
|------|---------|
| YouTube | `68uTDP2esso` live, **30** views tonight |
| In-repo ledgers | **Not** recorded on Meta / Threads / TikTok |
| Discoverability | JWST has no Shorts index/files in this tree → auto-mirror blind |
| Evening narrative | Threads succeeded on Ben’s Mac; TikTok `upload_error`; Meta in-flight — reconcile ledgers on the posting Mac |

---

## 4. Production queue

| Slot | Film | Status |
|------|------|--------|
| Live | Fermi · Black Hole · Alien Worlds · JWST | Public (cold longs) |
| Thu 27 Aug 18:00 | Last Star `REXYxuLOBoI` | Premiere — leave alone |
| Thu 3 Sept 18:00 | Europa | Scheduled |
| **Next to make** | **007 Neutron Star** | Folder `007_What-Happens-To-Your-Body-Near-A-Neutron-Star` · broadcast v02 builder present · **Ben watches before mint** · 7–9 min |
| After 007 | 013 Moon | Backlog only |
| 015 Simulation | Moved off 007 | Not next |

Empty scaffold `007_Neutron-Star/` — do not build there.

---

## 5. Lessons locked forward

### Picture / story

1. One VO idea → one literal image.
2. Mute test every minute.
3. Character in the world; one bottom glow; one face.
4. ≥2 no-Orbit scenery plates per ~60s.
5. **7–9 minutes now.** Expand only after impressions + hold past ~5 min.
6. You-beats + next-film Studio end screen (not shop, not logo void).

### Titles / thumbs / Shorts

7. Short titles from S1–S6 kill test only.
8. Object is the poster; Orbit off by default on covers.
9. Score in vidIQ **after 30 Aug** (credits).
10. Upload Shorts covers in Studio on a computer.
11. 4–8 punch Shorts, 22–27s, Related + pin, zero `/go/`.
12. Recut = new ID (Three Suns proof).

### Ops

13. After every upload: write **live** ID + file + visibility into the index.
14. Seed social ledgers before index rewrites.
15. Keep `tUAdhOnMW2g` in inventory.
16. TikTok stays paused until Ben says otherwise.

---

## 6. Priority actions

| # | Action | Why |
|---|--------|-----|
| 1 | Ben watches Neutron broadcast v02. Do not mint. | Next long already right length. |
| 2 | Leave Last Star premiere alone; strip series suffix after air if still present. | 3 views ≠ verdict. |
| 3 | On posting Mac: install/reload **Meta + Threads only**; leave TikTok Disabled. | Path migrate + uniqueness in this PR. |
| 4 | Add JWST `SHORTS_UPLOAD_INDEX.json` with live IDs (at least `68uTDP2esso`) + files. | Discover currently blind. |
| 5 | Reconcile Meta/Threads ledgers for today’s JWST Short if already posted. | Repo ledgers lag reality. |
| 6 | Rewrite 001–003 indexes to true live IDs (or mark dead rows non-live). | Stops corpse retries + mirror lies. |
| 7 | After 30 Aug: vidIQ title scores + Neutron/Europa keyword refresh. | Credits empty tonight. |
| 8 | Do **not** start Moon / Simulation. Do **not** recut old Shorts to remove Orbit. Do **not** upload to TikTok. | Queue + ban locks. |

---

## 7. What we are *not* changing

- Orbit character and British VO.
- Wonder over dread. No conspiracy / fearbait titles.
- One long / week; Shorts as discovery.
- Named-in-film affiliate gate.
- “Algorithm = audience.” Four subs is not a niche-pivot sample.

---

## Data notes

| Source | This run |
|--------|----------|
| vidIQ channel_stats + videos | Evening pull 18:10 UTC (`vidiq_raw.json`) — analytics/scores/keywords exhausted credits |
| YouTube RSS + watch pages | Night refresh 22:02 UTC (`public_views.json`) |
| Social ledgers / plists / uniqueness | Repo read + uncommitted WIP folded into this PR |
| LaunchAgents | Not loaded in cloud workspace |

Do not spend remaining **4** vidIQ add-on credits on generate/score until renew **30 Aug**.
