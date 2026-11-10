# J2492 — Browser Smoke Test of Studio Board Build with PR #715 vs `main`

**Verdict: PASS.**

OWB PR #715 (`gemini/J2464-board`, repo clean-up part 2: archive retired `/classic` board, remove ~15 unused functions from `05_Analytics/kanban/board_site/studio_app.js`, and archive unwired browser tests) builds cleanly and renders identically to `main` across every tab, lane, filter, sort mode, disclosure, and detail view on both `/index.html` and `/board.html` in a real Chrome browser (`Chrome/156.0.8078.81` via Playwright).

- **Reviewer:** `macbook` running **Gemini 4 Argon (High)** (`gemini-argon`) on 10 Nov 2026 (`2026-11-10T07:57:14.361Z`).
- **Worktree & builds:**
  - `dist_main`: built from `origin/main` (`074d6dd29`) via `cd 05_Analytics/kanban/board_site && python3 build.py` (served on `http://127.0.0.1:18801`).
  - `dist_715`: built from `origin/main` + `refs/pull/715/head` (`9829302cb`) merged cleanly (`ort` strategy) via `cd 05_Analytics/kanban/board_site && python3 build.py` (served on `http://127.0.0.1:18802`).
- **Live / Deployment:** Nothing on the live site changed; PR #715 was not merged and nothing was deployed. **£0.**

---

## 1. Built Artifact Comparison (`dist_main` vs `dist_715`)

| File | `dist_main` (`origin/main`) | `dist_715` (`main` + PR #715) | Delta |
|---|---|---|---|
| `index.html` | `201,033` B (`11461555bcd900aa`) | `185,199` B (`046e7807e322606b`) | `-15,834` B |
| `board.html` | `1,190,091` B (`231dfba2494e6940`) | `1,190,091` B (`a143c1e1d754f361`) | `+0` B |
| `tracker.html` | `171,267` B (`25fdd1e89d73b227`) | `171,267` B (`dc648cce30c1a04f`) | `+0` B |
| `ai.html` | `15,119` B (`da2ab7d75dedfcdf`) | `15,119` B (`e8a4d9360a926a9e`) | `+0` B |
| `updater.js` | `2,797` B (`269fde85cf599f0e`) | `2,797` B (`269fde85cf599f0e`) | `+0` B |
| `tracker.webmanifest` | `591` B (`e916bbbe193f8897`) | `591` B (`e916bbbe193f8897`) | `+0` B |
| `version.json` | `31` B (`4210c297e6586de4`) | `31` B (`3f785993f0d1ca9b`) | `+0` B |

- `index.html` is `15,834` bytes (`15.8 KB`) smaller in `dist_715` due to removing the unused functions in `studio_app.js` (plus the resulting `studio-version` meta hash change).
- `board.html`, `tracker.html`, and `ai.html` have identical byte sizes (`1,190,091` B, `171,267` B, and `15,119` B), differing only in the 16-char `<meta name="studio-version">` digest.

---

## 2. Page Errors (Uncaught Exceptions) & Console Errors Side by Side

| Metric | `dist_main` (`127.0.0.1:18801`) | `dist_715` (`127.0.0.1:18802`) | Result |
|---|---|---|---|
| **Page errors (`pageerror` / uncaught exceptions)** | **`0`** (`[]`) | **`0`** (`[]`) | **PASS** (zero uncaught exceptions in either build) |
| **Console errors (`console.error` / network errors)** | **`3`** (static `http.server` 404s on Vercel API routes) | **`3`** (identical static `http.server` 404s on Vercel API routes) | **PASS** (zero new console errors in `dist_715`) |

### Console error list side by side

| # | View | `dist_main` console error | `dist_715` console error | Notes |
|---|---|---|---|---|
| 1 | `index:overview` | `Failed to load resource: the server responded with a status of 404 (File not found)` at `http://127.0.0.1:18801/api/ref` | `Failed to load resource: the server responded with a status of 404 (File not found)` at `http://127.0.0.1:18802/api/ref` | Expected when serving static `dist/` via `python3 -m http.server`: `refFetch()` catches the local `/api/ref` 404 and falls back to GitHub `board-data` (`HTTP 200`). |
| 2 | `board:default` | `Failed to load resource: the server responded with a status of 404 (File not found)` at `http://127.0.0.1:18801/api/ref` | `Failed to load resource: the server responded with a status of 404 (File not found)` at `http://127.0.0.1:18802/api/ref` | Same expected `/api/ref` fallback to GitHub `board-data` (`HTTP 200`) on `/board.html`. |
| 3 | `board:default` | `Failed to load resource: the server responded with a status of 404 (File not found)` at `http://127.0.0.1:18801/api/checks?t=1794297434361` | `Failed to load resource: the server responded with a status of 404 (File not found)` at `http://127.0.0.1:18802/api/checks?t=1794297434361` | Expected on `python3 -m http.server` where Vercel serverless `/api/checks` is absent; `pollChecks()` ignores non-OK status and uses `board.json` checks. |

---

## 3. Side-by-Side View Content & Visible Text Length Comparison (36 Views)

Every tab, swim-lane chip, channel/type filter, sort option, disclosure drawer, video detail view (`#v=...`), and UAT screen (`#uat=...`) on `/index.html` (views `01`–`29`) and `/board.html` (views `30`–`36`) was clicked through in Chrome (`1280×900` viewport) after live `board-data` loaded. One screenshot per view per build (72 screenshots total) was captured to `/Users/ben/_desk/scratch/j2492-screenshots/` (kept outside git per the no-media-in-git rule) and verified by eye.

| View ID | Page / Tab / View | `dist_main` visible text length (`SHA256[:12]`) | `dist_715` visible text length (`SHA256[:12]`) | Screenshots (`main` / `pr715`) | Verdict |
|---|---|---|---|---|---|
| `01_index_overview` | /index.html — Overview tab (default load) | `979` chars (`51035f0ddcc4`) | `979` chars (`51035f0ddcc4`) | `main_01_index_overview.png` (`80,839` B) / `pr715_01_index_overview.png` (`80,913` B) | **PASS (exact match)** |
| `02_index_overview_checklist` | /index.html — Overview tab (first film checklist expanded) | `1,458` chars (`72803db4d016`) | `1,458` chars (`72803db4d016`) | `main_02_index_overview_checklist.png` (`101,915` B) / `pr715_02_index_overview_checklist.png` (`101,924` B) | **PASS (exact match)** |
| `03_index_videos_default` | /index.html — Videos tab (smart default landing) | `1,735` chars (`30b5d9a2b343`) | `1,735` chars (`30b5d9a2b343`) | `main_03_index_videos_default.png` (`98,792` B) / `pr715_03_index_videos_default.png` (`98,687` B) | **PASS (exact match)** |
| `04_index_videos_lane_backlog` | /index.html — Videos tab → lane: Backlog (backlog) | `8,747` chars (`cc3516122c3d`) | `8,747` chars (`cc3516122c3d`) | `main_04_index_videos_lane_backlog.png` (`84,142` B) / `pr715_04_index_videos_lane_backlog.png` (`84,145` B) | **PASS (exact match)** |
| `05_index_videos_lane_todo` | /index.html — Videos tab → lane: To do (todo) | `815` chars (`b273b0803ec5`) | `815` chars (`b273b0803ec5`) | `main_05_index_videos_lane_todo.png` (`89,082` B) / `pr715_05_index_videos_lane_todo.png` (`89,082` B) | **PASS (exact match)** |
| `06_index_videos_lane_progress` | /index.html — Videos tab → lane: In progress (progress) | `1,735` chars (`30b5d9a2b343`) | `1,735` chars (`30b5d9a2b343`) | `main_06_index_videos_lane_progress.png` (`98,730` B) / `pr715_06_index_videos_lane_progress.png` (`98,783` B) | **PASS (exact match)** |
| `07_index_videos_lane_qa` | /index.html — Videos tab → lane: QA (qa) | `1,123` chars (`e3938107a33f`) | `1,123` chars (`e3938107a33f`) | `main_07_index_videos_lane_qa.png` (`83,491` B) / `pr715_07_index_videos_lane_qa.png` (`83,491` B) | **PASS (exact match)** |
| `08_index_videos_lane_uat` | /index.html — Videos tab → lane: UAT (uat) | `397` chars (`ba32397eb467`) | `397` chars (`ba32397eb467`) | `main_08_index_videos_lane_uat.png` (`49,488` B) / `pr715_08_index_videos_lane_uat.png` (`49,488` B) | **PASS (exact match)** |
| `09_index_videos_lane_passed` | /index.html — Videos tab → lane: Passed (passed) | `382` chars (`0434c10a74aa`) | `382` chars (`0434c10a74aa`) | `main_09_index_videos_lane_passed.png` (`48,816` B) / `pr715_09_index_videos_lane_passed.png` (`48,816` B) | **PASS (exact match)** |
| `10_index_videos_lane_scheduled` | /index.html — Videos tab → lane: Scheduled (scheduled) | `7,732` chars (`e652d4b04339`) | `7,732` chars (`e652d4b04339`) | `main_10_index_videos_lane_scheduled.png` (`104,164` B) / `pr715_10_index_videos_lane_scheduled.png` (`104,164` B) | **PASS (exact match)** |
| `11_index_videos_lane_live` | /index.html — Videos tab → lane: Live (live) | `1,545` chars (`2df749f8f50b`) | `1,545` chars (`2df749f8f50b`) | `main_11_index_videos_lane_live.png` (`108,767` B) / `pr715_11_index_videos_lane_live.png` (`108,767` B) | **PASS (exact match)** |
| `12_index_videos_lane_postlive` | /index.html — Videos tab → lane: Post-live (postlive) | `800` chars (`742b22527b53`) | `800` chars (`742b22527b53`) | `main_12_index_videos_lane_postlive.png` (`117,485` B) / `pr715_12_index_videos_lane_postlive.png` (`117,485` B) | **PASS (exact match)** |
| `13_index_videos_lane_all` | /index.html — Videos tab → all lanes unfolded (seg=all) | `7,859` chars (`00f7054fbe16`) | `7,859` chars (`00f7054fbe16`) | `main_13_index_videos_lane_all.png` (`83,843` B) / `pr715_13_index_videos_lane_all.png` (`83,843` B) | **PASS (exact match)** |
| `14_index_videos_filter_owb` | /index.html — Videos tab → filter: Orbit (OWB) | `6,939` chars (`f3247825691d`) | `6,939` chars (`f3247825691d`) | `main_14_index_videos_filter_owb.png` (`78,205` B) / `pr715_14_index_videos_filter_owb.png` (`78,205` B) | **PASS (exact match)** |
| `15_index_videos_filter_hos` | /index.html — Videos tab → filter: HOS | `5,129` chars (`6a7f412ede05`) | `5,129` chars (`6a7f412ede05`) | `main_15_index_videos_filter_hos.png` (`83,211` B) / `pr715_15_index_videos_filter_hos.png` (`83,211` B) | **PASS (exact match)** |
| `16_index_videos_filter_longs` | /index.html — Videos tab → filter: Both + Longs | `5,220` chars (`73974518fd67`) | `5,220` chars (`73974518fd67`) | `main_16_index_videos_filter_longs.png` (`82,071` B) / `pr715_16_index_videos_filter_longs.png` (`82,071` B) | **PASS (exact match)** |
| `17_index_videos_filter_shorts` | /index.html — Videos tab → filter: Both + Shorts | `6,086` chars (`a18c7cd75ebb`) | `6,086` chars (`a18c7cd75ebb`) | `main_17_index_videos_filter_shorts.png` (`84,499` B) / `pr715_17_index_videos_filter_shorts.png` (`84,499` B) | **PASS (exact match)** |
| `18_index_videos_sort_updated` | /index.html — Videos tab → sort: updated | `8,016` chars (`7139667f2b1c`) | `8,016` chars (`7139667f2b1c`) | `main_18_index_videos_sort_updated.png` (`83,695` B) / `pr715_18_index_videos_sort_updated.png` (`83,695` B) | **PASS (exact match)** |
| `19_index_videos_sort_stage` | /index.html — Videos tab → sort: stage | `7,862` chars (`c0b2f553655c`) | `7,862` chars (`c0b2f553655c`) | `main_19_index_videos_sort_stage.png` (`84,249` B) / `pr715_19_index_videos_sort_stage.png` (`84,249` B) | **PASS (exact match)** |
| `20_index_videos_sort_blocked` | /index.html — Videos tab → sort: blocked | `8,127` chars (`1be01b868c9b`) | `8,127` chars (`1be01b868c9b`) | `main_20_index_videos_sort_blocked.png` (`83,629` B) / `pr715_20_index_videos_sort_blocked.png` (`83,629` B) | **PASS (exact match)** |
| `21_index_videos_sort_uat` | /index.html — Videos tab → sort: uat | `7,859` chars (`00f7054fbe16`) | `7,859` chars (`00f7054fbe16`) | `main_21_index_videos_sort_uat.png` (`83,843` B) / `pr715_21_index_videos_sort_uat.png` (`83,843` B) | **PASS (exact match)** |
| `22_index_video_detail` | /index.html — Video detail view (#v=HOS%3A012) | `874` chars (`e0e55b384cc5`) | `874` chars (`e0e55b384cc5`) | `main_22_index_video_detail.png` (`119,817` B) / `pr715_22_index_video_detail.png` (`119,817` B) | **PASS (exact match)** |
| `23_index_video_detail_tech` | /index.html — Video detail view (#v=HOS%3A012, technical details open) | `906` chars (`a136c43b0a4d`) | `906` chars (`a136c43b0a4d`) | `main_23_index_video_detail_tech.png` (`60,281` B) / `pr715_23_index_video_detail_tech.png` (`60,281` B) | **PASS (exact match)** |
| `24_index_videos_producing` | /index.html — Videos tab → Producing scope (#videos&view=producing) | `2,844` chars (`7da517c866b5`) | `2,844` chars (`7da517c866b5`) | `main_24_index_videos_producing.png` (`84,713` B) / `pr715_24_index_videos_producing.png` (`84,713` B) | **PASS (exact match)** |
| `25_index_review` | /index.html — Review tab | `1,194` chars (`33f274aec8a8`) | `1,194` chars (`33f274aec8a8`) | `main_25_index_review.png` (`127,573` B) / `pr715_25_index_review.png` (`127,573` B) | **PASS (exact match)** |
| `26_index_uat_view` | /index.html — UAT watch & review view (#uat=HOS:012) | `368` chars (`a1acc96f8742`) | `368` chars (`a1acc96f8742`) | `main_26_index_uat_view.png` (`55,271` B) / `pr715_26_index_uat_view.png` (`55,271` B) | **PASS (exact match)** |
| `27_index_agents` | /index.html — Agents tab | `1,107` chars (`fa192dad7692`) | `1,107` chars (`fa192dad7692`) | `main_27_index_agents.png` (`89,083` B) / `pr715_27_index_agents.png` (`89,083` B) | **PASS (exact match)** |
| `28_index_agents_queue` | /index.html — Agents tab (Job queue expanded) | `41,029` chars (`f70c8c2145ef`) | `41,029` chars (`f70c8c2145ef`) | `main_28_index_agents_queue.png` (`92,413` B) / `pr715_28_index_agents_queue.png` (`92,413` B) | **PASS (exact match)** |
| `29_index_schedule` | /index.html — Schedule tab | `3,879` chars (`764f864df5e3`) | `3,879` chars (`764f864df5e3`) | `main_29_index_schedule.png` (`126,645` B) / `pr715_29_index_schedule.png` (`126,645` B) | **PASS (exact match)** |
| `30_board_default` | /board.html — Default load (All channels, Long + Shorts, 6 lanes) | `41,233` chars (`518570fa6567`) | `41,233` chars (`518570fa6567`) | `main_30_board_default.png` (`182,573` B) / `pr715_30_board_default.png` (`182,573` B) | **PASS (exact match)** |
| `31_board_disclosures_open` | /board.html — Top strip Agents & services + Studio job activity expanded | `93,138` chars (`e61e12eef2f0`) | `93,138` chars (`e61e12eef2f0`) | `main_31_board_disclosures_open.png` (`292,196` B) / `pr715_31_board_disclosures_open.png` (`292,196` B) | **PASS (exact match)** |
| `32_board_filter_owb` | /board.html — Filter: Orbit (OWB) | `78,472` chars (`cd0625a3a3d6`) | `78,472` chars (`cd0625a3a3d6`) | `main_32_board_filter_owb.png` (`240,839` B) / `pr715_32_board_filter_owb.png` (`240,839` B) | **PASS (exact match)** |
| `33_board_filter_hos` | /board.html — Filter: HOS | `67,240` chars (`e08e862bab89`) | `67,240` chars (`e08e862bab89`) | `main_33_board_filter_hos.png` (`241,295` B) / `pr715_33_board_filter_hos.png` (`241,295` B) | **PASS (exact match)** |
| `34_board_filter_longs` | /board.html — Filter: All + Longs | `71,880` chars (`b6aa436dedd3`) | `71,880` chars (`b6aa436dedd3`) | `main_34_board_filter_longs.png` (`240,310` B) / `pr715_34_board_filter_longs.png` (`240,310` B) | **PASS (exact match)** |
| `35_board_filter_shorts` | /board.html — Filter: All + Shorts | `73,831` chars (`6ef64eac53b9`) | `73,831` chars (`6ef64eac53b9`) | `main_35_board_filter_shorts.png` (`240,696` B) / `pr715_35_board_filter_shorts.png` (`240,696` B) | **PASS (exact match)** |
| `36_board_show_old_public` | /board.html — On YouTube lane: Show older public expanded | `113,454` chars (`1ddc83028925`) | `113,454` chars (`1ddc83028925`) | `main_36_board_show_old_public.png` (`309,000` B) / `pr715_36_board_show_old_public.png` (`309,000` B) | **PASS (exact match)** |

---

## 4. Summary

- **Page errors:** `0` on `dist_main`, `0` on `dist_715`.
- **Console errors:** `3` on `dist_main`, `3` on `dist_715` (identical expected 404s on Vercel serverless endpoints `/api/ref` and `/api/checks` when served via `python3 -m http.server`).
- **Content & visible text length across all 36 views:** **36 / 36 exact matches** (100% identical character lengths and SHA256 text digests across every view on `/index.html` and `/board.html`).
- **Overall Verdict:** **PASS.** PR #715 is safe to merge.
