# J3071 — MacBook Local HOS Studio Fallback Verification (`ChbsigHD5_o`)

- **Worker:** `macbook-2` on the MacBook
- **For job:** `J3070` (prerequisite verification for held `J3063`)
- **Observed window:** `2026-11-18T20:30:31Z` – `2026-11-18T20:38:54Z` (analytics readback observed at **`2026-11-18T20:37:02.820251+00:00`**)
- **Result:** **VERIFIED RESPONSIVE** — local MacBook HOS Studio browser (`http://127.0.0.1:9222`) answers `cdp_tabs.reuse_page` and `Runtime.evaluate` in `<20 ms`, is signed into **`HistoryOfScienceYT`** (`UCXp7HkBIl1LgaznXuZHJyRg`, *History of Science*), and loads **Since published** Analytics for `ChbsigHD5_o` (*How Do Plants Clean the Air?*).

## 1. Pre-Check & Browser Activity

1. **Queue and browser activity (`2026-11-18T20:30:31.520336+00:00`):** `J3071` was the only claimed job in `jobs/queue.json`. On the MacBook, `:9223` (Orbit Studio) was up with 1 tab, while `:9222` (`~/.hos-chrome-cdp`) returned `ConnectionRefusedError` with `0` running `:9222` processes and no `Singleton*` lock files (cleanly closed earlier at `13:01Z`).
2. **Non-destructive profile reopen (`2026-11-18T20:35:13.638483+00:00`):** Per `AGENTS.md` (*"A signed-in browser profile that isn't open (Studio, Flow) is reopened by the worker itself"*), reopened the existing `~/.hos-chrome-cdp` profile in the background via macOS LaunchServices (`open -g -n -a "Google Chrome"` with the standard `scripts/macbook/start_cdp_browsers.sh` flags on `:9222`). Zero processes were killed, `:9223` was untouched, and no profile, extension, or login state was modified. `http://127.0.0.1:9222/json/version` (`Chrome/157.0.8103.79`) answered in `0.55 s`.

## 2. CDP Attachment, Prompt DOM Reads & Signed-In Channel Verification

Using `scripts/cdp_tabs.py` (`reuse_page(ctx, "studio.youtube.com")`) against `http://127.0.0.1:9222`:

- **Studio dashboard (`2026-11-18T20:35:59.286106+00:00`):**
  - `connect_over_cdp`: `0.0662 s`
  - `cdp_tabs.reuse_page`: `0.0079 s` (reused single tab `EA394E247B8CE3D31BDC9C7D3C8291D6`; 1 tab total)
  - `Runtime.evaluate` (`document.title` + `document.body.innerText`): `0.0189 s` (`1,375` chars)
  - `url`: `https://studio.youtube.com/channel/UCXp7HkBIl1LgaznXuZHJyRg`
  - `document.title`: `Channel dashboard - YouTube Studio` (`Your channel: History of Science`; Orbit channel ID absent)
- **Literal handle verification (`2026-11-18T20:36:57.790469+00:00`):**
  - Read-only check of `/channel/UCXp7HkBIl1LgaznXuZHJyRg/editing/profile` (`eval_s`: `0.0095 s`) confirmed channel name `History of Science`, handle `HistoryOfScienceYT`, and channel URL `https://www.youtube.com/channel/UCXp7HkBIl1LgaznXuZHJyRg`.

## 3. `ChbsigHD5_o` Since Published Analytics Verification

- **Exact observed time:** `2026-11-18T20:37:02.820251+00:00` (chip state re-confirmed at `2026-11-18T20:38:54.212534+00:00`)
- **Timings:** `connect_over_cdp` `0.0298 s`, `reuse_page` `0.0023 s`, `page.goto(..., wait_until="domcontentloaded")` `0.3716 s`, `Runtime.evaluate` `0.0097 s` (`readyState: "complete"`, `856` chars; single tab `EA394E247B8CE3D31BDC9C7D3C8291D6` preserved)
- **Resolved URL:** `https://studio.youtube.com/video/ChbsigHD5_o/analytics/hub_overview` (from `/video/ChbsigHD5_o/analytics/tab-overview/period-since_publish`)
- **Document title:** `Video analytics - YouTube Studio`
- **Active chips:** `Insights`, `Since published`
- **Observed read-only Studio fields at `20:37:02Z` (for J3070/J3063 handoff; no `launch_check.py` verdict recorded here):**
  - Video: `How Do Plants Clean the Air?` (`0:25`, `ChbsigHD5_o`), chart axis `18 Nov 2026, 11:30` – `18 Nov 2026, 20:36`
  - `Views`: `0` (`Watch time (hours)`: `0.0`, `Subscribers`: `0`, `Likes` Since published: `0`)
  - `Audience retention` (Since published): `Not enough data`
  - `How viewers engaged` (Since published): `Not enough data`
  - Channel dashboard *Latest Short performance* card (`20:35:59Z`, `First 9 hours 5 minutes`): `Ranking by views: 9 of 10`, `Views: 0`, `Average percentage viewed: 0%`, `Likes: 0`

## 4. Guardrails & Scope Compliance

- Read-only verification only: no upload, schedule, title, privacy, metadata, extension, profile, or login change; £0 / 0 credits spent; no remote host or private network address used.
- Neither `J3063` nor `J3064` was claimed or modified, and no `launch_check.py` record or performance verdict was written (`J3063` stays held until `J3070`'s worker / Chief verifies this fallback and reopens `J3063` for its remaining setup checks and analytics).
- Structured probe data saved in `jobs/reviews/J3071/evidence.json`.
