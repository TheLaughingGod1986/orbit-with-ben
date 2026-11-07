# J2235 — Orbit With Ben Cleanup Audit (`orbit-with-ben` Engine & Tools)

- **Job:** `J2235` (`Cleanup audit: orbit-with-ben engine and tools (dead code, duplicates, bugs)`)
- **Agent:** `macbook-2` (`gemini`)
- **Date:** 2026-11-07 UTC
- **Mode:** Read-only audit (`jobs/reviews/J2235/AUDIT.md` only; zero source, media, or NAS files modified)
- **Scope Inspected:**
  1. `scripts/` (engine, dispatch, gates, tests; `capacity_mode.py` already archived 5 Nov)
  2. `05_Analytics/kanban/` (`board_site/build.py`, `board_site/studio_app.js`, retired `/classic` artifacts)
  3. `04_Audio/tools/` (VO, music, Veo/Omni, CFR delivery, legacy helpers)
  4. `00_Brand/Channel-Setup/tools/` (gates, weekly audit, one-off thumbnail builders)
  5. `07_Content-Ops/` (`scripts/*.ts`, `src/lib/**`, `tests/*`)
  6. `02_Video-Projects/` (615 `.py` scripts across 48 film folders + template, totaling **8,854,294 bytes**) and `jobs/reviews/` (50 one-off `.py` scripts totaling **547,911 bytes**)

---

## Executive Summary & Top 5 Findings (Ranked by Value and Risk)

1. **`[F-01]` Active Unit Test & Engine Bugs in `scripts/` (`chief_relay.py`, `test_chief_succession.py`, `test_macbook_worker.py`, `routing.py`, `macbook_worker.py`) — *High Value / Low Risk (`fix bug` + `merge duplicates into one shared helper`)*:**
   - `scripts/chief_relay.py:317` (`find_bin`) and its duplicate `scripts/macbook_worker.py:185` ignore an explicit non-existent environment override (e.g., `CODEX_BIN=/tmp/.../missing`) and fall back to `/opt/homebrew/bin/codex` on disk, causing `test_chief_succession.py:61` (`test_missing_codex_cli_uses_gemini_and_all_chiefs_out_does_not_elect_cursor`) to **FAIL** on any host with Homebrew Codex installed.
   - `scripts/test_chief_succession.py:172` declares `class AutomaticChiefDuties(ChiefSuccession):`, inheriting 11 `test_*` methods from `ChiefSuccession` and running them **twice** on every test run.
   - `scripts/test_macbook_worker.py:251` (`test_checkouts_are_the_workers_own_never_bens`) **FAILS** whenever run from MacBook slot 2 (`MACBOOK_SLOT=2` in `os.environ`) because `AllAgents.setUp()` clears `MACBOOK_AGENT` (`line 206`) but leaves `MACBOOK_SLOT=2`, while `mw.SLOT` is bound at import time (`macbook_worker.py:52`) and compared against `mw.WORKER_DIR / "history-of-science"` (`slot 1`).
   - `scripts/routing.py:168` (`json.load(open(path))`) and `scripts/macbook_worker.py:523,535` leak unclosed file descriptors (`ResourceWarning`s on every test run).

2. **`[F-02]` Retired `/classic` Kanban Board Pipeline, Dead Functions in `studio_app.js`, and Broken/Unwired Browser Tests (`~405 KB` dead code) — *High Value / Low Risk (`delete dead branch` + `archive to _archive/`)*:**
   - `/classic` was retired via `vercel.json` redirects (`lines 2–6`) and `05_Analytics/kanban/board_site/build.py:9`, yet `build.py` still runs `release_record(film)` over every `02_Video-Projects/*/status.json` **at module import time** (`lines 49–54`) solely to populate `RELEASE_RECORDS` for `PATCHES` (`lines 36–65`) and dead `build_classic()` (`lines 176–195`). Meanwhile `05_Analytics/kanban/studio_kanban.html` (`261,375 B`), `board_site/shim.js` (`11,095 B`), `board_site/live.js` (`7,185 B`), and `scripts/test_kanban_page.py` (`59,025 B`, 48 Node-spawning tests) remain active in CI.
   - `05_Analytics/kanban/board_site/studio_app.js` contains **15 dead functions (`~215 lines`)** from superseded Overview/Agents layouts (`miniLine`, `featureVideo`, `featuredOutlook`, `featuredCard`, `nextVideoTask`, `nextVideoWorkCard`, `activityVideoLine`, `p24BlockedWhy`, `p24FocusFilms`, `p24NextLive`, `progressCard`, `plainWhy`, `agentLines`, `agentTraffic`, `agentsCards`).
   - `scripts/test_studio_video_dispatch.cjs` (`7,511 B`) is unwired from CI and **FAILS** immediately (`AssertionError` at line 27 on removed `data-category="analytics"`), and 11 `scripts/test_studio_*_browser.cjs` files (`51,589 B`) hardcode Linux `/usr/bin/chromium` + `http://127.0.0.1:8765` and assert removed DOM classes.

3. **`[F-03]` Rule-Violating & Obsolete Scripts in `scripts/` and `04_Audio/tools/` — *High Value / Low Risk (`archive to _archive/`)*:**
   - `scripts/apply_melodysheep_long_thumbs_v01.py` (`6,815 B`) and `scripts/apply_yellow_white_v04_thumbs.py` (`8,907 B`) hardcode **wrong CDP port `9222`** (HOS Flow browser signed into Ben's personal channel instead of Orbit Studio port `9223`) and call `ctx.new_page()` directly, violating Ben's 4 Nov 2026 one-tab rule (`from cdp_tabs import reuse_page`).
   - `04_Audio/tools/fix_published_playback_lag.py` (`7,809 B`) instructs pushing remastered files through YouTube Studio **Replace** (explicitly forbidden on the `AGENTS.md` Never list: *"Swap the file on an existing YouTube id (no Studio Replace)"*).
   - `04_Audio/tools/vidiq_title_score_sheet.py` (`8,784 B`) lives in `04_Audio/tools/` and hardcodes `BRAND_SUFFIX = "Orbit's Cosmic Journey"`, appending series suffixes to titles (explicitly forbidden on the `AGENTS.md` Never list: *"Titles: hashtags, series suffixes..."*).

4. **`[F-04]` Massive Per-Film Script Duplication in `02_Video-Projects/` (`615 .py` files, `8.85 MB`) & `jobs/reviews/` (`50 .py` files, `548 KB`) — *High Value / Low-to-Medium Risk (`merge duplicates into one shared helper` + `archive to _archive/` with receipts)*:**
   - **37 byte-for-byte identical copies** (`sha256=bc0546559c05`, `3,064 B` each = `113,368 B`) of `07_Edit-Project/_generate_veo_from_beats.py` are copied across `02_Video-Projects/013..061` and `_template_NNN_Episode-Slug` (29 of which are unstarted backlog stubs `033`–`061` containing no other code).
   - Unshipped/early backlog films `001` (`82 .py` files, `936,311 B`, including `07_Edit-Project/_backups/`), `002` (`21 .py` files, `261,560 B`), and `007` (`80 .py` files, `452,143 B`) hold **183 superseded v01–v29 experimental scripts (`1.65 MB`)** with zero upload receipts.
   - Shipped films `021`–`030` hold **349 `.py` scripts (`6.35 MB`)** across multiple iterative assembly versions (`_assemble_*_v01..v13.py`), linked to **112 provenance receipts** (`PACKAGE_UPLOAD_RESULT_*.json` and `status.json`).
   - `jobs/reviews/` holds **50 one-off `.py` build/verify scripts (`547,911 B`)**, including `build_j0936_prep_v04..v07.py` (`251,293 B`) and `verify_j0936_prep_v03..v07.py` (`133,360 B`) sitting at the top level of `jobs/reviews/`.

5. **`[F-05]` CI Blind Spots (`.github/workflows/rules-check.yml`), Worktree Test Failure (`desk-lock.test.py`), and Duplicated Helpers Across `scripts/`, `00_Brand`, and `07_Content-Ops` — *Medium-High Value / Low Risk (`fix bug` + `merge duplicates into one shared helper`)*:**
   - `.github/workflows/rules-check.yml` hardcodes explicit test filenames in `00_Brand/Channel-Setup/tools` and `04_Audio/tools`, silently skipping `00_Brand/Channel-Setup/tools/test_gate_stayed.py` (`9,465 B`, 7 tests) and `04_Audio/tools/test_orbit_cfr_delivery.py` (`2,487 B`, 2 tests) on every push/PR.
   - `07_Content-Ops/tests/desk-lock.test.py` (`lines 75, 91`) invokes `['node', '--import', 'tsx', ...]` assuming `07_Content-Ops/node_modules` exists locally in the checkout, whereas `macbook_worker.py` (`ensure_checkouts`) creates worker checkouts without `node_modules`, causing `npm test` (`pretest`) to fail with `ERR_MODULE_NOT_FOUND: Cannot find package 'tsx'` in MacBook worker slots (while `npx --no-install tsx` at line 40 succeeds).
   - `00_Brand/Channel-Setup/tools/` contains **15 one-off job-named thumbnail scripts (`build_*_jNNNN.py`, `167,833 B`)** that import from one another (`build_back_catalogue_tc_variants_j0099.py` / `build_packaging_long_thumbs_j0133.py`).
   - `07_Content-Ops/scripts/` duplicates YouTube Data API snippet read-modify-write boilerplate (`arg`, `WRITABLE_SNIPPET_KEYS`, `fetchVideo`, `putVideo`) across 5 scripts (`retitle-videos.ts`, `redescribe-videos.ts`, `set-private.ts`, `set-synthetic-disclosure.ts`, `update-shorts-listings.ts`), and `scripts/*.py` duplicates `now()`/`iso()`/`parse()`/`git()`/`find_bin()` across 6+ engine modules.

---

## Ranked Master Table of All Findings

| Rank | ID | Area | Target File(s) | Category | Proposed Action | Value | Risk |
|---:|---|---|---|---|---|---|---|
| 1 | `F-01a` | `scripts/` | `scripts/chief_relay.py:317`, `scripts/macbook_worker.py:185`, `scripts/test_chief_succession.py:61` | Bug + Duplicate | `fix bug` + `merge duplicates into one shared helper` | High | Low |
| 2 | `F-01b` | `scripts/` | `scripts/test_chief_succession.py:172` | Test Bug (duplicate test execution) | `fix bug` | High | Low |
| 3 | `F-01c` | `scripts/` | `scripts/test_macbook_worker.py:206,251`, `scripts/macbook_worker.py:52` | Test/Slot Bug (`MACBOOK_SLOT=2` failure) | `fix bug` | High | Low |
| 4 | `F-02a` | `05_Analytics/kanban` | `05_Analytics/kanban/board_site/build.py:28,36-65,176-195`, `studio_kanban.html`, `shim.js`, `live.js`, `scripts/test_kanban_page.py` | Dead Code (`~338 KB` retired `/classic` board) | `delete dead branch` + `archive to _archive/` | High | Low |
| 5 | `F-02b` | `05_Analytics/kanban` | `05_Analytics/kanban/board_site/studio_app.js` (15 dead functions, `~215 lines`) | Dead Code | `delete dead branch` | High | Low |
| 6 | `F-02c` | `scripts/` & `kanban` | `scripts/test_studio_video_dispatch.cjs` (`7.5 KB`) + 11 `scripts/test_studio_*_browser.cjs` (`51.6 KB`) | Broken / Unwired Tests (`59.1 KB`) | `archive to _archive/` (or rewrite into `test_board_activity.py`) | High | Low |
| 7 | `F-03a` | `scripts/` | `scripts/apply_melodysheep_long_thumbs_v01.py`, `scripts/apply_yellow_white_v04_thumbs.py` | Rule-Violating One-Offs (port `9222` + `ctx.new_page()`) | `archive to _archive/` | High | Low |
| 8 | `F-03b` | `04_Audio/tools` | `04_Audio/tools/fix_published_playback_lag.py`, `04_Audio/tools/vidiq_title_score_sheet.py` | Rule-Violating Legacy Tools (Studio Replace + title suffix) | `archive to _archive/` | High | Low |
| 9 | `F-04a` | `02_Video-Projects` | 37 identical copies of `07_Edit-Project/_generate_veo_from_beats.py` (`113.4 KB`) across `013..061` & `_template` | Exact Duplicate (`sha256=bc0546559c05`) | `merge duplicates into one shared helper` | High | Low |
| 10 | `F-05a` | `.github/workflows` | `.github/workflows/rules-check.yml:40-44` (`test_gate_stayed.py` & `test_orbit_cfr_delivery.py` skipped) | CI Blind Spot | `fix bug` | High | Low |
| 11 | `F-05b` | `07_Content-Ops` | `07_Content-Ops/tests/desk-lock.test.py:22,75,91` (`node --import tsx` fails without local `node_modules`) | Test Bug in Worker Slots | `fix bug` | Medium-High | Low |
| 12 | `F-04b` | `02_Video-Projects` | Unshipped early film scripts in `001` (`82 .py`, `936 KB`), `002` (`21 .py`, `262 KB`), `007` (`80 .py`, `452 KB`) | Superseded v01–v29 Scripts (`1.65 MB`, 0 upload receipts) | `archive to _archive/` | Medium-High | Low |
| 13 | `F-04c` | `jobs/reviews` | 50 one-off `.py` scripts in `jobs/reviews/` (`547.9 KB`, incl. `build_j0936_prep_v04..v07.py`) | One-Off Job Scripts (`548 KB`) | `archive to _archive/` | Medium | Low |
| 14 | `F-06` | `00_Brand/tools` | 15 `00_Brand/Channel-Setup/tools/build_*.py` one-off thumbnail builders (`167.8 KB`) | One-Off Scripts + Duplicated Helpers | `archive to _archive/` + `merge duplicates into one shared helper` | Medium | Low |
| 15 | `F-01d` | `scripts/` | `scripts/routing.py:168`, `scripts/macbook_worker.py:523,535` | Resource Leak (`ResourceWarning` unclosed files) | `fix bug` | Medium | Low |
| 16 | `F-07` | `scripts/` | `scripts/j0216-verify.ts` (`1.6 KB`), `scripts/sentence_sheet.py` (`11.8 KB`), `scripts/research_metadata.py` (`0.6 KB`) | Unused / One-Off Scripts (`14.1 KB`) | `archive to _archive/` | Medium | Low |
| 17 | `F-08` | `scripts/` | `now()`, `iso()`, `parse()`, `git()`, `last_seen()`, `_t()` duplicated across 6–12 `scripts/*.py` files | Duplicated Engine Helpers | `merge duplicates into one shared helper` | Medium | Low |
| 18 | `F-09a` | `07_Content-Ops` | `retitle-videos.ts`, `redescribe-videos.ts`, `set-private.ts`, `set-synthetic-disclosure.ts`, `update-shorts-listings.ts` | Duplicated YouTube Snippet CLI Boilerplate | `merge duplicates into one shared helper` | Medium | Low |
| 19 | `F-09b` | `07_Content-Ops` | `07_Content-Ops/src/lib/affiliate/*` (`12 files`, `98.3 KB`) + legacy v1/v2 CLIs (`create-export-package.ts`, etc., `~61 KB`) | Paused Affiliate `/go/` & Pre-Playbook V1/V2 Code (`CORE_FILES.json` locked) | `delete dead branch` / `archive to _archive/` (requires `core_sync.py` + HOS sync) | Medium | Medium |
| 20 | `F-03c` | `04_Audio/tools` | `04_Audio/tools/generate_sfx_from_script.py` (`6.1 KB`), `04_Audio/tools/strip_cg_native_audio.py` (`2.0 KB`) | Superseded Audio Helpers (`CORE_FILES.json` locked) | `archive to _archive/` (requires `core_sync.py` + HOS sync) | Low-Medium | Medium |
| 21 | `F-04d` | `02_Video-Projects` | Shipped film scripts (`004`–`006`, `013`–`030`: `390 .py` files, `6.99 MB`) + repeated `_generate_vo_v01.py`, `code_graphics.py` | Shipped Provenance + Duplicated Patterns | `archive to _archive/` (superseded `v01..vN-1` only, with receipts) + `merge duplicates into one shared helper` | Medium | Medium |

---

## Detailed Findings by Area

---

### Area 1: `scripts/` (Engine, Dispatch, Gates, and Tests)

> Note: `scripts/capacity_mode.py` was already archived on 5 Nov 2026 to `_archive/scripts/capacity_mode.py`.

#### `F-01a` — `find_bin` Ignores Explicit Non-Existent Env Overrides & Is Duplicated Across `chief_relay.py` and `macbook_worker.py`
- **Files:**
  - `scripts/chief_relay.py` (`lines 317–322`, `69,892 B`)
  - `scripts/macbook_worker.py` (`lines 185–190`, `23,822 B`)
  - `scripts/test_chief_succession.py` (`lines 61–67`, `11,015 B`)
- **Evidence:**
  - In `scripts/chief_relay.py:317–322`:
    ```python
    def find_bin(env: str, name: str):
        cands = [os.environ.get(env), shutil.which(name)] + [str(HOME / d / name) for d in (".npm-global/bin", ".local/bin")] \
            + [f"/opt/homebrew/bin/{name}", f"/usr/local/bin/{name}"]
        return next((c for c in cands if c and os.access(c, os.X_OK)), None)
    ```
  - `scripts/macbook_worker.py:185–190` contains an identical copy (`"""launchd's PATH misses npm-global and ~/.local: look in the usual install places too (as chief_relay.find_bin)."""`).
  - When `test_chief_succession.py:62` sets `os.environ['CODEX_BIN'] = str(self.tmp / 'missing')` and `os.environ['PATH'] = str(self.tmp / 'empty')`, `os.access(os.environ['CODEX_BIN'], os.X_OK)` is `False`, so `find_bin` falls through to `/opt/homebrew/bin/codex` or `/usr/local/bin/codex` on the host machine!
  - Running `python3 -m unittest scripts/test_chief_succession.py` on this machine fails twice with:
    ```text
    FAIL: test_missing_codex_cli_uses_gemini_and_all_chiefs_out_does_not_elect_cursor
    AssertionError: 'codex' != 'gemini'
    ```
- **Proposed Action:** `fix bug` + `merge duplicates into one shared helper`
  - If `env in os.environ` (and `os.environ[env]` is non-empty), treat `os.environ[env]` as authoritative (`return c if os.access(c, os.X_OK) else None`) instead of falling back to global system paths when a caller/test explicitly overrides `CODEX_BIN`. Extract `find_bin(env, name)` into a shared helper (or import from `chief_relay` / `workflow_state`).

#### `F-01b` — `AutomaticChiefDuties` Subclasses `ChiefSuccession` (`unittest.TestCase`), Running 11 Tests Twice
- **File:** `scripts/test_chief_succession.py` (`line 172`)
- **Evidence:**
  - `class ChiefSuccession(unittest.TestCase):` (`line 17`) defines 11 `test_*` methods (`lines 42–169`).
  - `class AutomaticChiefDuties(ChiefSuccession):` (`line 172`) subclasses `ChiefSuccession` to reuse `setUp`/`tearDown`/`beat`/`chief`/`queue`, which causes `unittest` discovery to execute all 11 `ChiefSuccession.test_*` methods a second time under `AutomaticChiefDuties` (running 26 tests instead of 15).
- **Proposed Action:** `fix bug`
  - Extract `class ChiefTestCase(unittest.TestCase):` with `setUp`, `tearDown`, `beat`, `chief`, and `queue` (no `test_*` methods), and have both `ChiefSuccession(ChiefTestCase)` and `AutomaticChiefDuties(ChiefTestCase)` inherit from it.

#### `F-01c` — `test_macbook_worker.py` Fails When Run Inside MacBook Slot 2 (`MACBOOK_SLOT=2`)
- **Files:**
  - `scripts/test_macbook_worker.py` (`lines 204–211, 251–256`, `17,841 B`)
  - `scripts/macbook_worker.py` (`lines 52, 58–74`)
- **Evidence:**
  - Running `python3 -m unittest scripts/test_macbook_worker.py` from `macbook-2` fails:
    ```text
    FAIL: test_checkouts_are_the_workers_own_never_bens (test_macbook_worker.AllAgents)
    AssertionError: PosixPath('/Users/ben/_desk/worker/slot2/history-of-science') != PosixPath('/Users/ben/_desk/worker/history-of-science')
    ```
  - Why: `macbook_worker.py:52` sets `SLOT = max(1, int(os.environ.get("MACBOOK_SLOT", "1") or 1))` at import time, and `own_checkout()` (`line 69`) returns `slot_dir(SLOT) / name`. In `test_macbook_worker.py:253`, the test asserts `mw.own_checkout("HOS_REPO", "history-of-science") == mw.WORKER_DIR / "history-of-science"` (assuming `SLOT == 1`), without patching `mw.SLOT = 1` or comparing against `mw.slot_dir(mw.SLOT) / "history-of-science"`.
- **Proposed Action:** `fix bug`
  - In `scripts/test_macbook_worker.py` (`AllAgents.setUp` or `test_checkouts_are_the_workers_own_never_bens`), patch `mw.SLOT = 1` (or compare against `mw.slot_dir(mw.SLOT) / "history-of-science"`).

#### `F-01d` — Unclosed File Handle `ResourceWarning`s in `routing.py` and `macbook_worker.py`
- **Files:**
  - `scripts/routing.py` (`line 168`)
  - `scripts/macbook_worker.py` (`lines 523, 535`)
- **Evidence:**
  - Running `python3 -m unittest discover -s scripts -p "test_*.py"` emits multiple `ResourceWarning: unclosed file`:
    - `scripts/routing.py:168`: `flags = json.load(open(path)).get("flags", {})` (called repeatedly by `test_routing.py`, `test_chief_succession.py`, `test_board_activity.py`).
    - `scripts/macbook_worker.py:523`: `out = open(logs / f"owb-macbook-worker-{n}.log", "a")` in `start_other_slots()` is never closed in the parent process after `popen(...)`.
    - `scripts/macbook_worker.py:535`: `lock = open(STATE / f"{slot_name(SLOT, 'macbook-worker')}.lock", "w")` in `run()` is never closed when `run()` returns (`lines 540, 550`).
- **Proposed Action:** `fix bug`
  - Use `with open(path) as f:` in `scripts/routing.py:168`, `with open(..., "a") as out:` around `popen(...)` in `scripts/macbook_worker.py:523`, and `with open(..., "w") as lock:` in `scripts/macbook_worker.py:535`.

#### `F-03a` — One-Off Thumbnail CDP Scripts Hardcoding Wrong Port `9222` & `ctx.new_page()`
- **Files:**
  - `scripts/apply_melodysheep_long_thumbs_v01.py` (`6,815 B`, last touched 2026-09-26)
  - `scripts/apply_yellow_white_v04_thumbs.py` (`8,907 B`, last touched 2026-09-25)
- **Evidence:**
  - Zero active call sites anywhere in the repo (referenced only in historical `00_Brand/Channel-Setup/THUMBNAIL_REFRESH_2026-09-25.md` and `THUMBNAIL_MELODYSHEEP_UPGRADE_2026-09-26.md`).
  - Both scripts violate two locked `AGENTS.md` rules:
    1. `apply_melodysheep_long_thumbs_v01.py:21` and `apply_yellow_white_v04_thumbs.py:24` set `CDP = "http://127.0.0.1:9222"` (`AGENTS.md`: *"The Orbit Studio browser is CDP port 9223. 9222 is the HOS Flow browser, signed into Ben's personal channel, and Orbit video pages fail there"*).
    2. `apply_melodysheep_long_thumbs_v01.py:130` and `apply_yellow_white_v04_thumbs.py:173` call `page = ctx.new_page()` and `page.close()` instead of `from cdp_tabs import reuse_page` (`AGENTS.md`, 4 Nov 2026: *"never `ctx.new_page()` or `Target.createTarget`"*).
- **Proposed Action:** `archive to _archive/`
  - Move both files to `_archive/scripts/`.

#### `F-07` — Unused / One-Off Scripts in `scripts/` (`j0216-verify.ts`, `sentence_sheet.py`, `research_metadata.py`)
- **Files:**
  - `scripts/j0216-verify.ts` (`1,650 B`)
  - `scripts/sentence_sheet.py` (`11,826 B`)
  - `scripts/research_metadata.py` (`621 B`) + `scripts/test_research_metadata.py` (`1,218 B`)
- **Evidence:**
  - `rg "j0216-verify"` -> **0 matches** anywhere in the repository. It is a one-off readback check for the Oct 2026 J0216 standalone Shorts batch with hardcoded video IDs (`["p_eM5f6NhtQ", ...]`).
  - `rg "sentence_sheet"` -> **0 matches** in `scripts/`, `00_Brand/`, `04_Audio/`, `07_Content-Ops/`, or `.github/workflows/` (only mentioned in historical `02_Video-Projects/025.../J0086_REPORT.md` and `docs/ORBIT_PLAYBOOK_LESSONS.md`). Superseded by `scripts/picture_qa.py` (`39,658 B`) and `00_Brand/Channel-Setup/tools/clip_check.py`.
  - `rg "research_metadata"` -> referenced **only** in its own unit test `scripts/test_research_metadata.py` (18-line stub function `build_research_metadata` with zero production callers).
- **Proposed Action:** `archive to _archive/`
  - Move `scripts/j0216-verify.ts` to `jobs/reviews/` or `_archive/scripts/`, and move `scripts/sentence_sheet.py`, `scripts/research_metadata.py`, and `scripts/test_research_metadata.py` to `_archive/scripts/`.

#### `F-08` — Duplicated Time, Git, and JSON Helpers Across `scripts/*.py`
- **Files:**
  - `now()` / `iso()` / `parse()` / `_t()` defined separately in 10 files:
    - `scripts/ai_spend.py:41` (`now`)
    - `scripts/board_check.py:54,58` (`now`, `iso`)
    - `scripts/board_publish.py:83,87` (`now`, `iso`)
    - `scripts/chief_relay.py:205,209,213` (`now`, `iso`, `parse`)
    - `scripts/jobs.py:76` (`now`)
    - `scripts/studio.py:35,39,43` (`now`, `iso`, `parse`)
    - `scripts/missed_runs.py:36` (`parse`)
    - `scripts/video_progress.py:26` (`parse`)
    - `scripts/kanban_snapshot.py:76`, `scripts/machines.py:27`, `scripts/progress24.py:47`, `scripts/queue_eta.py:43` (`_t`)
  - `git()` wrapper defined separately in 6 files:
    - `scripts/board_publish.py:100`, `scripts/claude_beat.py:20`, `scripts/mini_repair.py:59`, `scripts/missed_runs.py:40`, `scripts/studio.py:182`, `scripts/video_progress.py:33`
  - `last_seen()` defined separately in 3 files:
    - `scripts/chief_relay.py:248`, `scripts/missed_runs.py:44`, `scripts/owb_thread.py:85`
- **Evidence:** AST scan across `scripts/*.py` found 6 definitions of `now()`, 6 of `git()`, 4 of `iso()`, 4 of `parse()`, 4 of `_t()`, and 3 of `last_seen()`. Meanwhile `scripts/workflow_state.py:18,26` already provides `timestamp()` and `iso_timestamp()`.
- **Proposed Action:** `merge duplicates into one shared helper`
  - Consolidate UTC timestamp formatting/parsing (`now`, `iso`, `parse`) and `git()` into `scripts/workflow_state.py` (or a small `scripts/common.py`) and import across engine scripts.

---

### Area 2: `05_Analytics/kanban` (Board Build and `studio_app.js`)

#### `F-02a` — Retired `/classic` Board Still Runs at Import Time in `build.py` and Ships `338 KB` of Dead Artifacts & Slow Tests
- **Files:**
  - `05_Analytics/kanban/board_site/build.py` (`lines 9, 28, 36–65, 176–195`)
  - `05_Analytics/kanban/studio_kanban.html` (`261,375 B`)
  - `05_Analytics/kanban/board_site/shim.js` (`11,095 B`)
  - `05_Analytics/kanban/board_site/live.js` (`7,185 B`)
  - `scripts/test_kanban_page.py` (`59,025 B`, 924 lines, 48 tests)
- **Evidence:**
  - `05_Analytics/kanban/board_site/vercel.json` (`lines 2–6`) permanently redirects `/classic`, `/classic/`, and `/classic.html` to `/`.
  - `05_Analytics/kanban/board_site/build.py:9` states: `(/classic is retired and redirects to / in vercel.json.)`, and `build(out)` (`lines 223–233`) calls `build_simple`, `build_tracker`, `build_ai`, and `build_studio` — **never `build_classic(out)`**.
  - Despite `build_classic` being dead in `build()`, `build.py:49–54` still executes a filesystem glob and JSON parse over every `02_Video-Projects/*/status.json` **at module import time**:
    ```python
    RELEASE_RECORDS = {}
    for _p in sorted((REPO / "02_Video-Projects").glob("*/status.json")):
        try:
            _rec = release_record(json.loads(_p.read_text()))
        ...
    ```
    `RELEASE_RECORDS` is used only inside `PATCHES` (`line 57`), which is used only inside dead `build_classic()` (`line 178`).
  - `scripts/test_kanban_page.py` (`59,025 B`) is the single slowest unit test file in `scripts/` (`~7.1s`, spawning Node dozens of times to test `studio_kanban.html` and `build_classic()`).
- **Proposed Action:** `delete dead branch` + `archive to _archive/`
  - Delete `PAGE`, `FOOTER`, `RELEASE_RECORDS`, `PATCHES`, and `build_classic()` from `05_Analytics/kanban/board_site/build.py`.
  - Archive `05_Analytics/kanban/studio_kanban.html`, `05_Analytics/kanban/board_site/shim.js`, `05_Analytics/kanban/board_site/live.js`, and `scripts/test_kanban_page.py` to `_archive/05_Analytics/kanban/` (keeping any shared `release_record` unit tests in `scripts/test_release_record.py`, which already exists at `scripts/test_release_record.py`!).

#### `F-02b` — 15 Dead Functions (`~215 Lines`) in `05_Analytics/kanban/board_site/studio_app.js`
- **File:** `05_Analytics/kanban/board_site/studio_app.js` (`69,369 B`, 1,622 lines)
- **Evidence:**
  - Static call-graph analysis of `studio_app.js` (and `studio_shell.html`, `ai_app.js`, `board_app.js`, `tracker_loader.js`) shows **15 functions** that have **zero production call sites** (14 are referenced only in the `globalThis.test = { ... }` export object at `lines 1609–1621`, and 1 isn't even exported in `globalThis.test`):
    1. `miniLine(board, now)` (`line 256`, 1 line) — 0 production callers; only in `globalThis.test`.
    2. `featureVideo(board)` (`lines 641–655`, 15 lines) — only called by dead `featuredCard`.
    3. `featuredOutlook(v, now)` (`lines 656–663`, 8 lines) — only called by dead `featuredCard`.
    4. `featuredCard(board, now)` (`lines 664–677`, 14 lines) — removed from Overview on 6 Nov (see comment at `line 1329`: `Overview home shows only the four daily-progress blocks ... No Agents / Next live / feature card`).
    5. `nextVideoTask(v, board)` (`lines 724–764`, 41 lines) — only called by dead `nextVideoWorkCard`.
    6. `nextVideoWorkCard(v, board, now)` (`lines 765–769`, 5 lines) — 0 production callers; only tested by broken `test_studio_video_dispatch.cjs`.
    7. `activityVideoLine(j, board)` (`lines 770–775`, 6 lines) — **completely orphaned** (0 callers anywhere, not even in `globalThis.test`) after `activityJobCard` (`line 794`) switched to `activityJobVideoLabel(j, board)` on 6 Nov.
    8. `p24BlockedWhy(v, board)` (`lines 987–992`, 6 lines) — 0 callers anywhere (`not in globalThis.test`).
    9. `p24FocusFilms(board)` (`lines 1059–1062`, 4 lines) — superseded by `p24WorkingFilms(board)` (`line 1087`); 0 production callers.
    10. `p24NextLive(board, now)` (`lines 1163–1171`, 9 lines) — comment at `line 1162` notes `(not shown on Overview home)`; 0 production callers anywhere in `studio_app.js`.
    11. `progressCard(board, now)` (`lines 1201–1210`, 10 lines) — superseded by `workingOnNow` + `last24Section` + `p24Totals` in `overviewView` (`lines 1330–1335`); 0 production callers.
    12. `plainWhy(raw)` (`lines 1222–1240`, 19 lines) — only called by dead `agentLines` and dead `agentsCards`.
    13. `agentLines(board, now)` (`lines 1248–1259`, 12 lines) — 0 production callers.
    14. `agentTraffic(m)` (`lines 1270–1276`, 7 lines) — only called by dead `agentsCards`.
    15. `agentsCards(board, now)` (`lines 1307–1323`, 17 lines) — superseded by `agentsPageView` (`line 1278`); 0 production callers.
- **Proposed Action:** `delete dead branch`
  - Delete all 15 dead functions from `05_Analytics/kanban/board_site/studio_app.js`, remove their entries from `globalThis.test` (`lines 1609–1621`), and update the corresponding stale assertions in `scripts/test_board_activity.py` (which currently imports `featuredCard`, `progressCard`, `p24NextLive`, `agentLines`, `agentsCards` from `globalThis.test`).

#### `F-02c` — Broken & Unwired `scripts/test_studio_*.cjs` Test Files (`59,100 B`)
- **Files:**
  - `scripts/test_studio_video_dispatch.cjs` (`7,511 B`)
  - 11 Playwright browser scripts (`51,589 B` total):
    - `scripts/test_studio_activity_browser.cjs` (`7,580 B`)
    - `scripts/test_studio_blockers_browser.cjs` (`4,897 B`)
    - `scripts/test_studio_completion_browser.cjs` (`4,218 B`)
    - `scripts/test_studio_cut_scope_browser.cjs` (`2,422 B`)
    - `scripts/test_studio_hos_rows_browser.cjs` (`2,650 B`)
    - `scripts/test_studio_overview_browser.cjs` (`5,409 B`)
    - `scripts/test_studio_review_queue_browser.cjs` (`6,812 B`)
    - `scripts/test_studio_stage_explanations_browser.cjs` (`4,308 B`)
    - `scripts/test_studio_startup_browser.cjs` (`2,702 B`)
    - `scripts/test_studio_uat_browser.cjs` (`4,480 B`)
    - `scripts/test_studio_video_dispatch_browser.cjs` (`6,111 B`)
- **Evidence:**
  - `rg "test_studio_" .github/ scripts/` shows none of these 12 `.cjs` files are run by `.github/workflows/rules-check.yml` or any Python unittest suite (unlike `scripts/test_ai_page_cards.cjs`, which is called by `scripts/test_ai_page.py:44`).
  - Running `node scripts/test_studio_video_dispatch.cjs` **FAILS** at line 27:
    ```text
    AssertionError [ERR_ASSERTION]: The expression evaluated to a falsy value:
      assert(t.activityCard(board,NOW).includes('data-category="analytics"'))
    ```
    because `activityJobCard` (`studio_app.js:791–805`) was simplified on 6 Nov (`J2234`) to render `.activity-job-video`, `.activity-job-task`, `.activity-job-meta` without `data-category`, and the rest of `test_studio_video_dispatch.cjs` tests dead `nextVideoTask`/`nextVideoWorkCard`.
  - All 11 `test_studio_*_browser.cjs` scripts hardcode `executablePath: '/usr/bin/chromium'` (Linux-only path; does not exist on macOS) and `http://127.0.0.1:8765`, and assert DOM selectors removed in recent board updates (e.g., `.activity-video`, `.activity-category`, `+1 other active job`, `2 of 5 steps`, `.video-next-work`).Meanwhile `scripts/test_board_activity.py` (`75,375 B`, 62 tests) is the live, maintained test suite that runs in CI.
- **Proposed Action:** `archive to _archive/`
  - Archive all 12 `scripts/test_studio_*.cjs` files to `_archive/scripts/test_studio_cjs/` (moving any still-relevant dispatch assertions into `scripts/test_board_activity.py`).

---

### Area 3: `04_Audio/tools/`

#### `F-03b` — Legacy Tools in `04_Audio/tools/` That Violate Locked `AGENTS.md` Rules
- **Files:**
  - `04_Audio/tools/fix_published_playback_lag.py` (`7,809 B`, created Sep 2026)
  - `04_Audio/tools/vidiq_title_score_sheet.py` (`8,784 B`, created Sep 2026)
- **Evidence:**
  - Neither file is in `studio-core/CORE_FILES.json`, and neither has any active caller in `scripts/`, `04_Audio/`, `00_Brand/`, or `07_Content-Ops/`.
  - `04_Audio/tools/fix_published_playback_lag.py` (`lines 5–6, 211`) states:
    ```text
    Why: Viewers reported severe video lag on published YouTube videos even when narration audio continued normally. This script creates clean, YouTube-safe remasters to push through YouTube Studio "Replace video" or re-upload.
    ```
    `AGENTS.md` Never list explicitly forbids: *"Swap the file on an existing YouTube id (no Studio Replace). Upload a new video, schedule it on the slot, and set the old one Private with no publishAt."* Active CFR delivery is handled by `04_Audio/tools/orbit_cfr_delivery.py` (`14,327 B`).
  - `04_Audio/tools/vidiq_title_score_sheet.py` is a title-scoring markdown generator misplaced inside `04_Audio/tools/`, and `line 20` hardcodes:
    ```python
    BRAND_SUFFIX = "Orbit's Cosmic Journey"
    ```
    and `lines 106–115` append `: Orbit's Cosmic Journey` or `| Orbit's Cosmic Journey` to titles — directly violating `AGENTS.md` Never list (`"Titles: hashtags, series suffixes, brackets/parentheses, colons or dashes unless a tested variant wins"`).
- **Proposed Action:** `archive to _archive/`
  - Move `04_Audio/tools/fix_published_playback_lag.py` and `04_Audio/tools/vidiq_title_score_sheet.py` to `_archive/04_Audio/tools/`.

#### `F-03c` — Superseded `04_Audio/tools/` Scripts Locked in `studio-core/CORE_FILES.json`
- **Files:**
  - `04_Audio/tools/generate_sfx_from_script.py` (`6,051 B`)
  - `04_Audio/tools/strip_cg_native_audio.py` (`1,996 B`)
- **Evidence:**
  - `04_Audio/tools/generate_sfx_from_script.py` generates SFX via the paid ElevenLabs Sound Effects API. Per `AGENTS.md` (*Polish pass, 11 Oct 2026*), both channels switched to `scripts/sfx_kit.py` (free house synthesis of `rumble_low`, `whoosh_soft`, `tick_ink`). Zero active callers in `scripts/` or workflows.
  - `04_Audio/tools/strip_cg_native_audio.py` has zero callers anywhere in `orbit-with-ben` outside `studio-core/CORE_FILES.json` (Veo/Omni clips are stripped during assembly or `orbit_gemini_veo.py`).
  - **Constraint:** Both files are listed in `studio-core/CORE_FILES.json` (`lines 19, 25`). Removing or archiving them requires running `python3 scripts/core_sync.py lock` and syncing `history-of-science` in the same PR pair.
- **Proposed Action:** `archive to _archive/` (with `core_sync.py lock` across OWB + HOS)
  - Archive both to `_archive/04_Audio/tools/` in a coordinated `studio-core` update with HOS.

#### `F-05a` (Part 1) — `04_Audio/tools/test_orbit_cfr_delivery.py` Omitted from CI Workflow
- **Files:**
  - `.github/workflows/rules-check.yml` (`line 44`)
  - `04_Audio/tools/test_orbit_cfr_delivery.py` (`2,487 B`, 2 tests)
- **Evidence:**
  - `.github/workflows/rules-check.yml:44` runs:
    ```yaml
    python3 -m unittest discover -s 04_Audio/tools -p "test_vo_take.py"
    ```
    Because `-p` is hardcoded to `"test_vo_take.py"` instead of `"test_*.py"`, `04_Audio/tools/test_orbit_cfr_delivery.py` (which tests `orbit_cfr_delivery.py`) is never executed in CI.
- **Proposed Action:** `fix bug`
  - Change `-p "test_vo_take.py"` to `-p "test_*.py"` in `.github/workflows/rules-check.yml:44`.

---

### Area 4: `00_Brand/Channel-Setup/tools/`

#### `F-05a` (Part 2) — `00_Brand/Channel-Setup/tools/test_gate_stayed.py` Omitted from CI Workflow
- **Files:**
  - `.github/workflows/rules-check.yml` (`lines 40–43`)
  - `00_Brand/Channel-Setup/tools/test_gate_stayed.py` (`9,465 B`, 7 tests)
- **Evidence:**
  - `.github/workflows/rules-check.yml:40–43` explicitly enumerates 4 test files in `00_Brand/Channel-Setup/tools`:
    - `test_weekly_public_audit.py`
    - `test_gate_background.py`
    - `test_gate_upcoming.py`
    - `test_gate_duration.py`
  - It omits `test_gate_stayed.py` (`9,465 B`, 7 unit tests for the stayed-to-watch Shorts gate).
- **Proposed Action:** `fix bug`
  - Replace lines 40–43 in `.github/workflows/rules-check.yml` with `python3 -m unittest discover -s 00_Brand/Channel-Setup/tools -p "test_*.py"`.

#### `F-06` — 15 One-Off Job-Specific Thumbnail Builders (`167,833 B`) in `00_Brand/Channel-Setup/tools/`
- **Files (`15 files, 167,833 B total`):**
  1. `00_Brand/Channel-Setup/tools/build_andromeda_tc_b_j0234.py` (`14,193 B`) — 0 callers
  2. `00_Brand/Channel-Setup/tools/build_back_catalogue_tc_variants_j0099.py` (`22,894 B`) — imported as a helper library by 5 `build_*_tc_b_j0*.py` scripts below
  3. `00_Brand/Channel-Setup/tools/build_blackhole_tc_b_j0419.py` (`4,897 B`) — 0 callers; imports `build_back_catalogue_tc_variants_j0099` + `build_packaging_long_thumbs_j0133`
  4. `00_Brand/Channel-Setup/tools/build_crop_safe_short_covers_j0099.py` (`8,735 B`) — 0 callers
  5. `00_Brand/Channel-Setup/tools/build_jupiter_notext_tc_b_j0136.py` (`7,729 B`) — 0 callers
  6. `00_Brand/Channel-Setup/tools/build_laststar_tc_b_j0386.py` (`3,795 B`) — 0 callers; imports `build_back_catalogue_tc_variants_j0099` + `build_packaging_long_thumbs_j0133`
  7. `00_Brand/Channel-Setup/tools/build_melodysheep_long_thumbs_v01.py` (`18,225 B`) — 0 callers
  8. `00_Brand/Channel-Setup/tools/build_nasa_plate_short_covers.py` (`9,365 B`) — 0 callers
  9. `00_Brand/Channel-Setup/tools/build_neutronstar_tc_b_j0402.py` (`5,204 B`) — 0 callers; imports `build_back_catalogue_tc_variants_j0099` + `build_packaging_long_thumbs_j0133`
  10. `00_Brand/Channel-Setup/tools/build_packaging_long_thumbs_j0133.py` (`17,774 B`) — imported as a helper library by 5 `build_*_tc_b_j0*.py` scripts
  11. `00_Brand/Channel-Setup/tools/build_saturn_tc_b_j0152.py` (`3,395 B`) — 0 callers; imports `build_back_catalogue_tc_variants_j0099` + `build_packaging_long_thumbs_j0133`
  12. `00_Brand/Channel-Setup/tools/build_sun_venus_tc_b_j0908.py` (`7,264 B`) — 0 callers; imports `build_back_catalogue_tc_variants_j0099` + `build_packaging_long_thumbs_j0133`
  13. `00_Brand/Channel-Setup/tools/build_thumb_refresh_2026_09_25.py` (`14,619 B`) — 0 callers
  14. `00_Brand/Channel-Setup/tools/build_thumb_refresh_v02_plates.py` (`13,440 B`) — 0 callers
  15. `00_Brand/Channel-Setup/tools/build_weekly_thumbs_j1106.py` (`16,304 B`) — 0 callers
- **Evidence:**
  - None of these 15 scripts are in `studio-core/CORE_FILES.json`, and none are called by any active tool, gate, or CI check.
  - Five scripts (`build_blackhole_tc_b_j0419.py`, `build_laststar_tc_b_j0386.py`, `build_neutronstar_tc_b_j0402.py`, `build_saturn_tc_b_j0152.py`, `build_sun_venus_tc_b_j0908.py`) import shared image/grading/type helpers (`_fit`, `_contrast_grade`, `_vignette`, `_save_under_2mb`, `_draw_label`) straight out of `build_back_catalogue_tc_variants_j0099.py` and `build_packaging_long_thumbs_j0133.py`.
- **Proposed Action:** `merge duplicates into one shared helper` + `archive to _archive/`
  - Extract reusable thumbnail rendering primitives (`fit_16x9`, `contrast_grade`, `vignette`, `save_under_2mb`, `run_thumb_preview`) into one clean `00_Brand/Channel-Setup/tools/thumb_kit.py`, and archive the 15 completed job-specific `build_*.py` scripts to `_archive/00_Brand/Channel-Setup/tools/` (with their job IDs `J0099`, `J0133`, `J0136`, `J0152`, `J0234`, `J0386`, `J0402`, `J0419`, `J0908`, `J1106` preserved).

---

### Area 5: `07_Content-Ops/` (`scripts/`, `src/`, `tests/`)

#### `F-05b` — `07_Content-Ops/tests/desk-lock.test.py` Fails in Worker Checkouts Without Local `node_modules`
- **File:** `07_Content-Ops/tests/desk-lock.test.py` (`lines 22, 40, 75, 91`, `9,982 B`)
- **Evidence:**
  - Running `cd 07_Content-Ops && npm test` in `/Users/ben/_desk/worker/slot2/orbit-with-ben` fails in `pretest` (`python3 tests/desk-lock.test.py`) with 7 failures:
    ```text
    Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'tsx' imported from /Users/ben/_desk/worker/slot2/orbit-with-ben/07_Content-Ops/
    ```
  - Why: `test_npx_tsx_cli_owns_one_real_lock_without_outer_wrapper` (`line 40`) runs `['npx', '--no-install', 'tsx', ...]` and **PASSES** (finding `tsx` in the user's npm cache), whereas `test_writers_and_cleanup` (`lines 75, 91`) runs `['node', '--import', 'tsx', f'scripts/{name}.ts']`, which requires `07_Content-Ops/node_modules/tsx` to exist inside the current worktree (`OPS / 'node_modules'`). Neither `/Users/ben/_desk/orbit-with-ben/07_Content-Ops/node_modules` nor `/Users/ben/_desk/worker/slot2/orbit-with-ben/07_Content-Ops/node_modules` is present on the MacBook worker checkouts.
- **Proposed Action:** `fix bug`
  - In `07_Content-Ops/tests/desk-lock.test.py:75,91`, use `['npx', '--no-install', 'tsx', f'scripts/{name}.ts']` (matching line 40) when `(OPS / 'node_modules' / 'tsx').exists()` is false, so `desk-lock.test.py` passes consistently in both CI and MacBook worker checkouts.

#### `F-09a` — 5 YouTube Data API Mutation Scripts in `07_Content-Ops/scripts/` Duplicate Snippet Read-Modify-Write Boilerplate
- **Files (`23,717 B total`):**
  - `07_Content-Ops/scripts/retitle-videos.ts` (`4,513 B` — in `CORE_FILES.json`)
  - `07_Content-Ops/scripts/redescribe-videos.ts` (`4,913 B` — OWB-only)
  - `07_Content-Ops/scripts/set-private.ts` (`5,251 B` — OWB-only)
  - `07_Content-Ops/scripts/set-synthetic-disclosure.ts` (`4,616 B` — OWB-only)
  - `07_Content-Ops/scripts/update-shorts-listings.ts` (`4,424 B` — OWB-only)
- **Evidence:**
  - All 5 scripts copy-paste:
    1. CLI flag parsing (`function arg(name: string)` and `--dry-run` handling).
    2. `WRITABLE_SNIPPET_KEYS = ["title" / "description", "tags", "categoryId", "defaultLanguage", "defaultAudioLanguage"] as const`.
    3. Raw `fetch("https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=...")` and `PUT https://www.googleapis.com/youtube/v3/videos?part=...` error handling instead of sharing a helper in `07_Content-Ops/src/lib/youtube/data-api.ts`.
    4. Furthermore, `retitle-videos.ts` uses `./channel-youtube` (`beforeRun`, `afterRun`, `youtubeAccessToken`), whereas `redescribe-videos.ts`, `set-private.ts`, `set-synthetic-disclosure.ts`, and `update-shorts-listings.ts` bypass `./channel-youtube` and import `ensureDeskLock` + `getYouTubeAccessToken` directly.
- **Proposed Action:** `merge duplicates into one shared helper`
  - Extract `fetchVideoItem(token, id)`, `updateVideoParts(token, body, parts)`, `WRITABLE_SNIPPET_KEYS`, and CLI arg parsing into `07_Content-Ops/src/lib/youtube/data-api.ts` (and route all 5 scripts through `./channel-youtube`).

#### `F-09b` — Paused Affiliate `/go/` Tree (`12 files, 98,271 B`) and Pre-Playbook V1/V2 Content-Ops Scripts (`13 files, 61,010 B`)
- **Files:**
  - **Affiliate `/go/` tree (`07_Content-Ops/src/lib/affiliate/`, `12 files`, `98,271 B`):**
    - `creator-description-voice.ts` (`7,108 B`), `description.ts` (`13,896 B`), `editorial-trust-gate.ts` (`18,111 B`), `film-topic-book-map.ts` (`8,570 B`), `go-redirect-urls.ts` (`1,881 B`), `live-product-urls.ts` (`8,849 B`), `social-channels.ts` (`2,885 B`), `social-copy-rules.ts` (`10,837 B`, not in `CORE_FILES.json`), `social-copy.ts` (`8,106 B`), `topic-product-map.ts` (`9,300 B`), `types.ts` (`4,026 B`), `urls.ts` (`4,702 B`).
  - **Pre-playbook V1/V2 CLI scripts & modules (`13 files`, `61,010 B`):**
    - `scripts/create-export-package.ts` (`1,225 B`), `scripts/diagnose-youtube-growth.ts` (`1,017 B`), `scripts/generate-platform-copy.ts` (`436 B`), `scripts/generate-short-plan.ts` (`720 B`), `scripts/import-performance-data.ts` (`762 B`), `scripts/next-episode-brief.ts` (`1,538 B`), plus their backing modules `src/lib/analytics/csv-import.ts` (`6,302 B`), `src/lib/analytics/insights.ts` (`5,886 B`), `src/lib/analytics/next-episode-brief.ts` (`3,863 B`), `src/lib/analytics/youtube-growth.ts` (`10,108 B`), `src/lib/content/captions.ts` (`3,349 B`), `src/lib/content/export-package.ts` (`7,064 B`), `src/lib/content/generate-short-plan.ts` (`9,142 B`), `src/lib/content/quality-score.ts` (`4,158 B`), `src/lib/platforms/generate-platform-copy.ts` (`6,149 B`).
- **Evidence:**
  - `AGENTS.md` Never list states: *"Add a `/go/` link anywhere: its redirect app is retired, and affiliate links are paused."*
  - In production, the only active caller into `src/lib/affiliate/*` is `src/lib/publishing/youtube-package.ts:4` (`import { appendAffiliateSectionToDescription } from "@/lib/affiliate/description"`), which is only invoked when a manifest explicitly passes `affiliateLinks` (paused on both channels).
  - The 6 V1/V2 scripts (`create:export-package`, `diagnose:youtube`, `generate:platform-copy`, `generate:short-plan`, `import:performance`, `brief:next`) are never called by `AGENTS.md` commands, `launchd/`, or `scripts/` (only by `tests/growth-system-v2.test.ts` and `tests/episode-ops-v2.test.ts`).
  - **Constraint:** 11 of the 12 `src/lib/affiliate/*` files and all 6 V1/V2 CLI scripts are locked in `studio-core/CORE_FILES.json`.
- **Proposed Action:** `delete dead branch` / `archive to _archive/` (Medium risk — requires `core_sync.py lock` + HOS sync)
  - Keep a minimal stub for `appendAffiliateSectionToDescription` (or remove the optional `affiliateLinks` hook in `youtube-package.ts`) and archive `src/lib/affiliate/*` and the retired V1/V2 export/CSV CLIs to `_archive/07_Content-Ops/` in a dedicated `studio-core` sync PR across OWB and HOS.

---

### Area 6: Per-Film Scripts in `02_Video-Projects/` (`615 .py` files, `8.85 MB`) & `jobs/reviews/` (`50 .py` files, `548 KB`)

#### `F-04a` — 37 Byte-for-Byte Identical Copies of `07_Edit-Project/_generate_veo_from_beats.py` (`113,368 B`)
- **Files:**
  - `02_Video-Projects/_template_NNN_Episode-Slug/07_Edit-Project/_generate_veo_from_beats.py` (`3,064 B`, `sha256=bc0546559c05`)
  - **36 identical copies (`3,064 B` each, `sha256=bc0546559c05`)** in:
    - Shipped/active films: `013`, `022`, `028`, `029`, `030`, `031`, `032` (7 copies)
    - Unstarted backlog stub folders (`033` through `061`, 29 copies):
      `033_Why-This-Planet-Has-21-Year-Winters` .. `061_Why-Venus-Spins-Backwards-And-Its-Day-Is-Longer-Than-Its-Year`
  - Plus 1 modified copy in `02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings/07_Edit-Project/_generate_veo_from_beats.py` (`8,265 B`, `sha256=2eb30da68854`).
- **Evidence:**
  - Every new episode scaffolded from `_template_NNN_Episode-Slug` copies `_generate_veo_from_beats.py` (`3,064 B`) into `02_Video-Projects/<NNN_Slug>/07_Edit-Project/_generate_veo_from_beats.py`.
  - Furthermore, `_generate_veo_from_beats.py` calls `04_Audio/tools/orbit_gemini_veo.py` across a whole `veo_Script_Beats.md` table without Omni/Vertex routing guards (`AGENTS.md`: *"Orbit = Omni only... Vertex only"*).
- **Proposed Action:** `merge duplicates into one shared helper`
  - Move `_generate_veo_from_beats.py` to `04_Audio/tools/generate_veo_from_beats.py` (taking `--project 02_Video-Projects/<NNN_Slug>`), delete it from `_template_NNN_Episode-Slug/07_Edit-Project/_generate_veo_from_beats.py` and the 29 unstarted stub folders `033`–`061` (and `031`–`032`), leaving only shipped films' copies until archived with their receipts.

#### `F-04b` — 183 Superseded Experimental Scripts (`1,650,014 B`) in Unshipped Early Folders `001`, `002`, and `007`
- **Files:**
  1. `02_Video-Projects/001_Will-We-Ever-Meet-Aliens/` — **82 `.py` files (`936,311 B`)**, **0 upload receipts**, no `status.json` (in `VIDEO_BACKLOG.json` as `001` backlog topic, never published):
     - Includes `07_Edit-Project/_backups/` (`3 backup .py files`, `70,426 B`), `_build_bold_explainer_v05..v10.py`, `_build_full_video_v11..v29.py` (19 full-video builder versions!), `_build_audio_mix_v11..v19.py`, `_generate_seedance_clips_v11..v27.py` (15 seedance scripts), `_qa_check_v19..v28.py`.
  2. `02_Video-Projects/002_What-Happens-If-You-Fall-Into-A-Black-Hole/` — **21 `.py` files (`261,560 B`)**, **0 upload receipts**, no `status.json` (superseded by live film `018` / `020`):
     - Includes `_build_video_v01..v10.py`, `_generate_clips_v01..v09.py`, `_qa_v02..v10.py`.
  3. `02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/` — **80 `.py` files (`452,143 B`)**, **0 upload receipts**, no `status.json` (`VIDEO_BACKLOG.json` lists live Neutron Star video `fN9sB2kM6pQ`, uploaded before `PACKAGE_UPLOAD_RESULT` receipts existed, while `007/07_Edit-Project/` holds 80 July–Sept 2026 experimental `compile_master_v2..v8.py`, `fix_part1..4_*.py`, `regen_*.py`, `rebuild_*.py`, `verify_*.py` scripts).
- **Evidence:**
  - These 3 directories alone account for **183 of the 615 `.py` files (`30%` of count, `1.65 MB`)** in `02_Video-Projects/`.
  - All 183 scripts predate the current playbook (using retired Seedance API, CapCut draft generators, and elevenlabs-sfx pipelines).
- **Proposed Action:** `archive to _archive/`
  - Archive `02_Video-Projects/001_Will-We-Ever-Meet-Aliens/07_Edit-Project/*.py` (and `_backups/`) and `02_Video-Projects/002_What-Happens-If-You-Fall-Into-A-Black-Hole/07_Edit-Project/*.py` to `_archive/02_Video-Projects/`.
  - For `007_What-Happens-To-Your-Body-Near-A-Neutron-Star` (live on YouTube as `fN9sB2kM6pQ` per `VIDEO_BACKLOG.json` and `05_Analytics/owb/snapshots/`), keep the final `compile_master_v8.py` as provenance and archive the 79 intermediate `v2..v7` / `fix_*` / `test_*` scripts to `_archive/02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/` with a receipt pointer to `VIDEO_BACKLOG.json` (`video_id: fN9sB2kM6pQ`).

#### `F-04c` — 50 One-Off Job Scripts (`547,911 B`) in `jobs/reviews/`
- **Files:**
  - **15 top-level `.py` files in `jobs/reviews/` (`419,594 B`):**
    - `jobs/reviews/build_j0936_prep_v04.py` (`55,519 B`), `build_j0936_prep_v05.py` (`69,071 B`), `build_j0936_prep_v06.py` (`70,535 B`), `build_j0936_prep_v07.py` (`56,168 B`)
    - `jobs/reviews/verify_j0936_prep_v03.py` (`10,836 B`), `verify_j0936_prep_v04.py` (`21,210 B`), `verify_j0936_prep_v05.py` (`28,358 B`), `verify_j0936_prep_v06.py` (`33,969 B`), `verify_j0936_prep_v07.py` (`38,987 B`)
    - `jobs/reviews/generate_j0936_prep_v04_openings.py` (`22,369 B`), `jobs/reviews/inspect_j0936_prep_v04_source_windows.py` (`12,506 B`)
    - `jobs/reviews/check_j1032_final.py` (`6,707 B`), `correct_j1032_exposure.py` (`5,041 B`), `deliver_j1032_v04.py` (`15,039 B`), `finish_j1032_v04.py` (`3,836 B`), `render_j1032_v04.py` (`8,618 B`)
  - **35 per-job `.py` files in `jobs/reviews/J*/` (`128,317 B`):**
    - `J0935/strict_batch_checklist.py`, `J0989/j0989_{audioqa,build,gates}.py`, `J1075/verify_media.py`, `J1128/*.py` (9 scripts), `J1199/assemble_s6_v11.py`, `J1208/*.py` (5 scripts), `J1218/render_cg_strips.py`, `J1220/measure_open_motion.py`, `J1326/*.py` (3 scripts), `J1331/investigate.py`, `J1834/*.py` (3 scripts), `J2016/repair.py`, `J2144/*.py` (2 scripts), `J2176/build.py`.
- **Evidence:**
  - `jobs/reviews/build_j0936_prep_v04..v07.py` and `verify_j0936_prep_v03..v07.py` (`405 KB` for a single job `J0936`) are 4–5 near-duplicate versions of the same standalone Shorts prep builder/verifier sitting loose in `jobs/reviews/`.
- **Proposed Action:** `archive to _archive/`
  - Archive superseded intermediate versions (`build_j0936_prep_v04..v06.py` and `verify_j0936_prep_v03..v06.py`, saving `304 KB` immediately) to `_archive/jobs/reviews/J0936/`, and move top-level `j0936` / `j1032` scripts into `jobs/reviews/J0936/` and `jobs/reviews/J1032/` alongside their job review markdowns (`jobs/reviews/J0936_prep_v07.md`, `jobs/reviews/J1032_v04.md`).

#### `F-04d` — Shipped Film Build Scripts (`004`–`006`, `013`–`030`: `390 .py` files, `6.99 MB`) & Shared Per-Film Helpers (`code_graphics.py`, `_generate_vo_v01.py`, `_short_vo_pipeline_v01.py`)
- **Files & Provenance Receipts Table:**
  Per the J2235 brief (*"Per-film build scripts of shipped films are provenance: propose archiving only with the receipts that point at them"*), every shipped film below is mapped to its exact upload/status receipts:

  | Film Folder | `.py` Count | Total Bytes | Final Provenance Script(s) to Keep Live | Superseded Intermediate Scripts Eligible to Archive (with Receipt) | Provenance Receipts Pointing at Film |
  |---|---:|---:|---|---|---|
  | `004_JWST-Discoveries-That-Change-Everything` | 3 | `62,094 B` | `_build_jwst_master_v03.py` | `_build_jwst_master_v01.py`, `_build_jwst_master_v02.py` | `02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/status.json` + `VIDEO_BACKLOG.json` (`dM1OgGPAYvw`) |
  | `005_The-Last-Star-In-The-Universe` | 3 | `40,314 B` | `_build_last_star_v02.py` | `_build_last_star_v01.py` | `02_Video-Projects/005_The-Last-Star-In-The-Universe/status.json`, `10_Shorts/friday_2026-10-16_last_star/11_Upload-Package/PACKAGE_UPLOAD_RESULT_2026-10-04T11-53-31-527Z.json` |
  | `006_Could-Life-Exist-Under-The-Ice-Of-Europa` | 1 | `11,408 B` | `_build_europa_v01.py` | *(none — single script)* | `02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/status.json` |
  | `013_Why-The-Moon-Is-Slowly-Leaving-Us` | 24 | `214,214 B` | `_assemble_v03b.py`, `_build_shorts_v01.py` | 21 earlier `v01..v03` / `fix_*` scripts | `02_Video-Projects/013_Why-The-Moon-Is-Slowly-Leaving-Us/status.json` |
  | `019_Andromeda-Milky-Way-Collision` | 4 | `56,448 B` | `_assemble_v02.py` | `_assemble_v01.py` | `02_Video-Projects/019_Andromeda-Milky-Way-Collision/status.json` |
  | `020_What-Would-You-See-If-You-Fell-Into-Jupiter` | 4 | `56,043 B` | `_assemble_v02.py` | `_assemble_v01.py` | `02_Video-Projects/020_What-Would-You-See-If-You-Fell-Into-Jupiter/status.json`, `10_Shorts/lift_no_crust/11_Upload-Package/PACKAGE_UPLOAD_RESULT_2026-10-13T06-25-41-356Z.json` |
  | `021_What-Happens-When-Saturn-Loses-Its-Rings` | 27 | `472,539 B` | Latest long + short assemblers | Earlier `v01..v04` assemblers & one-off builders | `11_Upload-Package/Schedule/PACKAGE_UPLOAD_RESULT_2026-10-01T22-57-46-731Z.json` (+ 7 Short `PACKAGE_UPLOAD_RESULT_*.json` & `status.json`) |
  | `022_Is-the-Sun-Getting-Brighter` | 32 | `338,323 B` | Latest v05 long + short assemblers | Earlier `v01..v04` assemblers | `11_Upload-Package/PACKAGE_UPLOAD_RESULT_2026-10-09T12-29-50-786Z.json` (+ 3 Short `PACKAGE_UPLOAD_RESULT_*.json` & `status.json`) |
  | `023_What-Happened-To-Venus` | 42 | `721,532 B` | Latest v05e long + short assemblers | Earlier `v01..v05d` assemblers | `11_Upload-Package/PACKAGE_UPLOAD_RESULT_2026-10-14T23-20-06-686Z.json` (+ 5 Short `PACKAGE_UPLOAD_RESULT_*.json` & `status.json`) |
  | `024_What-Happens-If-You-Travel-Near-Light-Speed` | 37 | `506,870 B` | Latest long + short assemblers | Earlier `v01..v05` assemblers | `11_Upload-Package/PACKAGE_UPLOAD_RESULT_2026-10-22T11-24-10-617Z.json` (+ 2 earlier upload receipts & `status.json`) |
  | `025_Could-A-Robot-Survive-On-Mars` | 49 | `869,492 B` | Latest long + short assemblers | Earlier `v01..v08` assemblers | `11_Upload-Package/PACKAGE_UPLOAD_RESULT_2026-10-09T20-14-55-649Z.json` (+ 9 Short `PACKAGE_UPLOAD_RESULT_*.json` & `status.json`) |
  | `026_How-Far-Is-The-Nearest-Star` | 41 | `742,949 B` | Latest long + short assemblers | Earlier `v01..v07` assemblers | `11_Upload-Package/PACKAGE_UPLOAD_RESULT_2026-10-22T10-03-47-020Z.json` (+ 12 `PACKAGE_UPLOAD_RESULT_*.json` & `status.json`) |
  | `027_What-If-Earth-Stopped-Spinning` | 37 | `580,224 B` | Latest long + short assemblers | Earlier `v01..v06` assemblers | `11_Upload-Package/PACKAGE_UPLOAD_RESULT_2026-10-22T11-53-44-301Z.json` (+ 11 `PACKAGE_UPLOAD_RESULT_*.json` & `status.json`) |
  | `028_A-Star-Is-Coming-Toward-Us` | 32 | `1,071,377 B` | Latest long + short assemblers | Earlier `v01..v09` assemblers (`1.07 MB` total) | `11_Upload-Package/PACKAGE_UPLOAD_RESULT_2026-10-23T20-40-27-397Z.json` (+ 21 `PACKAGE_UPLOAD_RESULT_*.json` & `status.json`) |
  | `029_Is-Betelgeuse-About-To-Explode` | 22 | `799,963 B` | Latest long + short assemblers | Earlier `v01..v07` assemblers | `11_Upload-Package/PACKAGE_UPLOAD_RESULT_2026-10-25T02-57-29-461Z.json` (+ 5 `PACKAGE_UPLOAD_RESULT_*.json` & `status.json`) |
  | `030_Apophis-Closer-Than-Our-Satellites` | 36 | `539,809 B` | Latest long + standalone short assemblers (`v13a`) | Earlier `v01..v12` assemblers | `11_Upload-Package/PACKAGE_UPLOAD_RESULT_2026-10-25T02-57-32-270Z.json` (+ 22 `PACKAGE_UPLOAD_RESULT_*.json` & `status.json`) |

- **Repeated Per-Film Script Patterns Across `021`–`032`:**
  - `code_graphics.py` (9 films, `169,765 B` total) and `mechanism_graphics.py` (2 films, `19,966 B`): each re-implements PIL font loading (`/System/Library/Fonts/Supplemental/Arial Bold.ttf`), 1920×1080 canvas setup, feathering, alpha compositing, and `ffmpeg` MP4 encoding.
  - `_generate_vo_v01.py` (7 films, `85,874 B`) and `_short_vo_pipeline_v01.py` (5 films, `127,072 B`): each re-implements ElevenLabs chunking, silence trimming, and LUFS normalization around `04_Audio/tools/orbit_voice.py`.
  - `_build_captions_v01.py` (6 films, `27,007 B`) and `fetch_nasa_pool.py` / `fetch_pool_v01.py` (6 films, `22,163 B`): each re-implements SRT formatting and NASA Image API querying.
- **Proposed Action:**
  1. `merge duplicates into one shared helper`: Extract the shared canvas/type/MP4 encoding primitives from `code_graphics.py`, SRT caption generation from `_build_captions_v01.py`, and NASA pool fetching from `fetch_nasa_pool.py` into reusable modules under `scripts/` or `04_Audio/tools/` so future films (`031+`) pass data/config rather than cloning 20–40 KB of boilerplate per film.
  2. `archive to _archive/` (with provenance receipts): For shipped films `004`–`030`, keep the final shipped assembly script (`_assemble_vNN.py`), `code_graphics.py`, and all `PACKAGE_UPLOAD_RESULT_*.json` / `status.json` receipts in place, and archive only superseded intermediate assembly versions (`v01..v(N-1)`) into `_archive/02_Video-Projects/<NNN_Slug>/` with a `PROVENANCE.json` manifest linking each archived script to the film's `PACKAGE_UPLOAD_RESULT_*.json` and `status.json` receipt paths listed above.
