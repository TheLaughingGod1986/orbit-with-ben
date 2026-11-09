# J2234 — Risk & Cut-Over Review of `docs/MULTI_CHANNEL_PLAN.md` (Gemini)

- **Job:** `J2234` (`Review multi-channel plan: risk and cut-over (Gemini)`)
- **Reviewer:** `macbook-2` (`gemini-argon` / Gemini 4 Argon High)
- **Target:** [`docs/MULTI_CHANNEL_PLAN.md`](../../../docs/MULTI_CHANNEL_PLAN.md) (merged in PR #543, plus the initial Phase 1 scaffolding in [`scripts/channels.py`](../../../scripts/channels.py), [`scripts/channel_films.py`](../../../scripts/channel_films.py), [`scripts/test_channels.py`](../../../scripts/test_channels.py), and `channels/{owb,hos}/channel.json`)
- **Date:** 2026-11-07
- **Spend:** £0 / 0 credits (read-only code and architecture audit)

---

## 1. Executive Summary & Per-Phase Verdicts

- **Overall Verdict:** **FIX** — The architectural direction (one studio engine, one shared queue/board, per-channel `studio/` manifests, and studio-wide rules outranking channel rules) is sound, and Phase 1's initial loader (`scripts/channels.py`) is already proving the pattern cleanly. However, **Phases 2, 3, and 4 contain concrete operational showstoppers** that would blind the live Vercel board on Ben's phone, break `jobs.py --git` transactions across repo boundaries, stall the MacBook and Mini launchd workers during cut-over, and break `core-check.yml` / shared content-ops tooling if executed as currently written.

| Phase | Verdict | Summary of Ruling |
|---|---|---|
| **Phase 1: Channel manifests, in place** | **KEEP (with minor scope FIX)** | Safe in-repo refactor (`scripts/channels.py` and `channels/{owb,hos}/channel.json` are already live). Must expand scope beyond the 16 Python engine files to include the remaining 20+ Python references, the `jobs/WIP.json` schema transition (`next` / `next_hos` → `next: {owb: [...], hos: [...]}`), and the TypeScript channel maps in `07_Content-Ops/`. |
| **Phase 2: Manifests move into channel repos** | **FIX** | Moving `channels/<slug>/*` into `<channel-repo>/studio/` breaks **single-checkout execution** in GitHub Actions CI (`rules-check.yml`), Vercel static builds (`05_Analytics/kanban/board_site/build.py`), and `board_publish.py` sparse worktrees (`OWB_SPARSE` / `HOS_SPARSE`) unless a fallback/cached registry stays in the engine repo and sparse-checkout globs are updated first. |
| **Phase 3: The engine moves to its own `studio` repo** | **FIX (Critical Cut-Over Risks)** | **Five studio-stopping hazards:** (1) making `studio` **private** breaks unauthenticated browser reads of `raw.githubusercontent.com/.../board-data/board.json` on Ben's phone and burns GitHub's 2,000 free private Actions minutes/month on high-frequency `jobs.py --git` pushes; (2) `jobs.py` + `studio.py` currently commit `jobs/queue.json`, `02_Video-Projects/<film>/status.json`, and `STATUS.md` in **one atomic git commit** (`studio.git_transaction`), which fails across two repos; (3) a naive forwarding shim in `orbit-with-ben/scripts/` can cause split-brain queue/heartbeat commits if `cwd` or `ROOT` resolves to `orbit-with-ben`; (4) 7 Mini launchd jobs + MacBook multi-slot workers + `mini_repair.py` + `setup_macbook.sh` hardcode `orbit-with-ben`; (5) `BOARD_GH_TOKEN` and Codex's unattended allow-list (`Rule F`) are scoped only to `orbit-with-ben` and `history-of-science`. |
| **Phase 4: Plug-in ready (`core_sync.py` retirement)** | **FIX (Critical Misconception)** | **Do NOT retire `core_sync.py` in Phase 4 unless `07_Content-Ops/`, `04_Audio/tools/`, and `00_Brand/Channel-Setup/tools/` also move or become a shared package.** [`studio-core/CORE_FILES.json`](../../../studio-core/CORE_FILES.json) does **not** lock the studio engine (`jobs.py`, `chief_relay.py`, etc.); it locks **55 shared production, audio, and YouTube/Buffer publishing files** that live inside each channel repo. Retiring `core_sync.py` leaves all 55 files unlocked across `owb`, `hos`, and `<third-channel>`. |

---

## 2. Phase-by-Phase Risk Audit: What Breaks on the Mini and MacBook

### Phase 1 — Channel manifests in place (`orbit-with-ben/channels/<slug>/`)
- **Verdict:** **KEEP (with minor scope FIX)**
- **Current state:** `channels/owb/channel.json`, `channels/hos/channel.json`, [`scripts/channels.py`](../../../scripts/channels.py), [`scripts/channel_films.py`](../../../scripts/channel_films.py), and [`scripts/test_channels.py`](../../../scripts/test_channels.py) are already merged and working on `main`.
- **What would break on the Mini or MacBook during the rest of Phase 1:**
  1. **`jobs/WIP.json` key migration (`next` / `next_hos` → `next: {owb: [...], hos: [...]}`):**
     - Right now `channels/owb/channel.json` has `"wip": {"limit": 5, "line": "next"}` and `channels/hos/channel.json` has `"wip": {"limit": 4, "line": "next_hos"}`.
     - [`scripts/workflow_handoffs.py`](../../../scripts/workflow_handoffs.py) (`waiting_films()`, lines 24–32) and any Claude/Mini WIP reader expect `WIP.json[line]` to be a flat list. If `WIP.json` is switched to nested `next: {"owb": [...], "hos": [...]}` without updating `channels.wip_line()` and `workflow_handoffs.waiting_films()` in the same commit, `waiting_films()` returns `set()`, causing `workflow_handoffs.reconcile()` (run by `chief_relay.py` every tick) to treat waiting WIP films as orphaned production films and auto-queue bogus `Chief: resolve ...` repair jobs.
  2. **`board_publish.py` section keys (`SECTIONS = ("hos", "owb", "briefs", "credits", "tracker")`):**
     - [`scripts/board_publish.py`](../../../scripts/board_publish.py) (line 74 and line 572) and [`scripts/kanban_snapshot.py`](../../../scripts/kanban_snapshot.py) hardcode top-level `board["hos"]` and `board["owb"]` keys, and the client JS (`studio_app.js`, `tracker_app.js`, `shim.js`) reads `board.owb.jobs` and `board.hos.pipeline`. If Phase 1 renames or restructures those top-level keys in `board.json` without keeping `board.owb` / `board.hos` backward-compatible, the live Vercel board breaks immediately on next minute's `board_publish.py` run.
  3. **`NoNewChannelNames` lint test vs legitimate channel-specific adapters:**
     - A blanket test failing if *any* engine script names a channel will fail on [`scripts/channel_films.py`](../../../scripts/channel_films.py) docstrings/tests or on `chief_relay.py`'s legacy `hos_desk.py` fallback (lines 668–676, 1552–1554) unless `hos_desk.py` is either moved into `hos/flow.json` or explicitly allow-listed until retired.

---

### Phase 2 — Manifests move into the channel repos (`<channel-repo>/studio/`)
- **Verdict:** **FIX**
- **What would break on the Mini:**
  1. **`board_publish.py` sparse worktrees (`~/_desk/scratch/chief/board-wt/{owb,hos}`):**
     - [`scripts/board_publish.py`](../../../scripts/board_publish.py) (lines 67–73) runs `git sparse-checkout set --no-cone` on `WT / "owb"` and `WT / "hos"`.
     - Currently `OWB_SPARSE` includes `"/channels/"`, and `HOS_SPARSE` only includes `["/00_Brand/Channel-Setup/PIPELINE.json", "/00_Brand/Channel-Setup/social/UPLOADS.json"]`.
     - **Breakage:** As soon as `channels/owb/` moves to `orbit-with-ben/studio/` and `channels/hos/` moves to `history-of-science/studio/`, `WT / "owb"` and `WT / "hos"` will **not** check out `/studio/` unless `"/studio/"` is added to both `OWB_SPARSE` and `HOS_SPARSE` **before** moving the files. Otherwise `kanban_snapshot.py` (which runs inside `WT / "owb"`) and `channels._load()` will find 0 channels, raising `ValueError: exactly one channel must be home` every minute.
- **What would break on the MacBook Pro:**
  2. **Missing third-channel clone in `macbook_worker.py` and `setup_macbook.sh`:**
     - [`scripts/macbook_worker.py`](../../../scripts/macbook_worker.py) (lines 54–55, 80–81, 377) hardcodes `URLS = {"orbit-with-ben": ..., "history-of-science": ...}` and `for repo in (OWB, HOS):`.
     - If `channels.py` loads `<repo>/studio/channel.json` by iterating `channels.json` on the MacBook, any channel listed in `channels.json` whose repo has not yet been cloned into `~/_desk/worker/<slug>` and `~/_desk/worker/slot2/<slug>` will cause `channels._load()` to fail with `FileNotFoundError` (or `ValueError: missing channel`) on both MacBook slots, stopping all MacBook jobs.
     - **Fix required before Phase 2:** `macbook_worker.py` `pull_main()` must iterate `channels.json`, auto-cloning any missing channel checkout into `slot_dir(SLOT) / slug` before calling `channels._load()`.
- **What would break in GitHub Actions CI & Vercel:**
  3. **Single-repo checkouts in GitHub Actions (`rules-check.yml`) and Vercel (`build.py`):**
     - GitHub Actions on `orbit-with-ben` only checks out `orbit-with-ben` (there is no `../history-of-science` directory on the Ubuntu runner). Vercel's build container only checks out the connected repo.
     - When `python3 -m unittest discover -s scripts -p "test_*.py"` runs in CI (`rules-check.yml` line 30), `channels._load()` currently succeeds because both `channels/owb/channel.json` and `channels/hos/channel.json` live inside `orbit-with-ben`.
     - **Breakage:** Once `channels/hos/channel.json` moves exclusively to `history-of-science/studio/channel.json`, `channels._load()` in CI will only find `owb` (or fail when looking for `hos` at `~/YouTube/history-of-science`), breaking `test_channels.py`, `test_routing.py`, `test_kanban_snapshot.py`, `test_video_tracker.py`, and every PR check!
     - **Fix required before Phase 2:** `channels.json` in the engine repo must carry each channel's core identity (`slug`, `label`, `name`, `home`, `order`, `title_match`, `wip`, `picture_route`, `pipeline`, `repo`), or the engine repo must keep a cached snapshot of each channel's `studio/channel.json` so single-repo CI and Vercel builds never require sibling checkouts on disk.

---

### Phase 3 — The engine moves to its own `studio` repo
- **Verdict:** **FIX (Critical Cut-Over Risks)**
- **Focus: What could stop the studio during Phase 3 cut-over?**

#### Stopper 3A: Making `studio` a **Private** repo breaks the live Kanban board on Ben's phone & burns GitHub Actions quota
- The plan states (line 74): *"Create `studio` (private, free). Copy `scripts/` (engine files), `jobs/` and the board site with their history (`git filter-repo`)."*
- Currently, both `TheLaughingGod1986/orbit-with-ben` and `TheLaughingGod1986/history-of-science` are **PUBLIC** GitHub repositories (`"isPrivate": false`).
- **Why private breaks the board:**
  - All five browser apps on `studio-kanban.vercel.app` ([`studio_app.js`](../../../05_Analytics/kanban/board_site/studio_app.js) lines 5–18, [`tracker_app.js`](../../../05_Analytics/kanban/board_site/tracker_app.js) lines 5–11, [`ai_app.js`](../../../05_Analytics/kanban/board_site/ai_app.js) lines 5–11, [`shim.js`](../../../05_Analytics/kanban/board_site/shim.js) lines 9 & 60–61, and [`tracker_loader.js`](../../../05_Analytics/kanban/board_site/tracker_loader.js) lines 11–16) fetch `board.json`, `tracker.json`, and `macbook-heartbeat/heartbeat.json` **directly from `https://raw.githubusercontent.com/...` in Ben's mobile browser with no auth token**.
  - On a **private** GitHub repo, unauthenticated `raw.githubusercontent.com` requests return **HTTP 404 Not Found**. Moving `board-data` to a private `studio` repo will immediately black out `/`, `/board`, `/ai`, and `/tracker` on Ben's phone (`"can't reach the data"`).
  - Furthermore, [`scripts/mini_repair.py`](../../../scripts/mini_repair.py) (line 24) and [`scripts/macbook/setup_macbook.sh`](../../../scripts/macbook/setup_macbook.sh) (line 5) rely on unauthenticated `curl -fsSL https://raw.githubusercontent.com/...` for emergency recovery when git checkouts are wedged.
  - Finally, GitHub Free gives **unlimited** Actions minutes to **public** repos, but caps **private** repos at **2,000 minutes/month across the entire account**. Because every `jobs.py` claim, progress step, release, and completion pushes a commit to `main` (100–200+ pushes/day), running `rules-check.yml` (which runs `apt-get install ffmpeg` + full Python test suite) on a private `studio` repo will exhaust the 2,000-minute monthly cap in ~3–4 days and block all CI across Ben's account.
- **Required Fix:** Either create `studio` as a **PUBLIC** repo (matching `orbit-with-ben` and `history-of-science`, since no secrets are ever committed to git), **OR** serve `board.json` and `tracker.json` through a Vercel serverless proxy (`/api/board`, `/api/tracker`) authenticated with `BOARD_GH_TOKEN` (cached at the Vercel edge for 15–20 s like `/api/ref`) and disable push-triggered CI on queue-only commits (`paths-ignore: ["jobs/queue.json", "JOBS.md"]`). Making `studio` **public** is far simpler and eliminates all three failure modes at once.

#### Stopper 3B: Cross-repo atomic git commit failure in `jobs.py` + `studio.py`
- Today, [`scripts/jobs.py`](../../../scripts/jobs.py) (`with_git()`, lines 944–962; `on_board()`, lines 870–913) and [`scripts/studio.py`](../../../scripts/studio.py) (`git_transaction()`, lines 186–253) live in the same repository (`orbit-with-ben`) as `02_Video-Projects/<film>/status.json` and `STATUS.md`.
- Whenever an OWB job with `--film` and `--stage` is claimed, completed, blocked, or released via `jobs.py ... --git`, `jobs.py` mutates:
  1. `jobs/queue.json` and `JOBS.md`
  2. `02_Video-Projects/<film>/status.json` (via `board_claim()` / `board_release()`)
  3. `STATUS.md` (via `studio.write_status(studio.FILMS)`)
  and passes all four paths to `studio.git_transaction()`, which runs `pathlib.Path(p).resolve().relative_to(ROOT.resolve())` (`studio.py` line 240) and commits them in **one single git commit on `ROOT`**.
- **What breaks when `jobs/` moves to `studio/`:**
  - `studio/02_Video-Projects` does not exist, so `studio.film_dir(studio.FILMS, job["film"])` immediately calls `sys.exit(...)` or raises `FileNotFoundError`.
  - `handoffs.records(studio.FILMS)` in `jobs.py` lines 1153 & 1201 and `chief_relay.py` line 1454 also scans `02_Video-Projects/*/status.json`.
  - Even if `studio.FILMS` is pointed at `orbit-with-ben/02_Video-Projects`, `p.resolve().relative_to(ROOT.resolve())` raises `ValueError` because `orbit-with-ben/02_Video-Projects/...` is outside `studio/`, and a single `git commit` cannot span two git repositories!
- **Required Fix before Phase 3:** Decouple queue transactions from channel repo `status.json` commits **in Phase 1/2 before moving the repo**:
  - Either `jobs/queue.json` becomes the single source of truth for live stage claims (just as it already is for `HOS`, where `on_board(job)` is `False` and `stage_sync.py` / `video_tracker.py` derive stage state from `queue.json` + `PIPELINE.json`), **OR** `board_claim` / `board_release` must run a separate, non-blocking `studio.py` transaction inside `channels.repo_path(job["repo"])` after the `studio` queue commit succeeds.

#### Stopper 3C: Split-brain queue & heartbeat writes during the forwarding-shim window
- The plan states (line 76): *"Leave a forwarding shim in `orbit-with-ben/scripts/` for a fortnight, so old launchd jobs and agents still work."*
- **How a naive shim stops the studio:**
  - Many scripts determine which git repo to fetch/commit/push using `ROOT = Path(__file__).resolve().parent.parent` (`jobs.py`, `studio.py`, `missed_runs.py`, `ai_spend.py`, `refill.py`) or `cwd` (`claude_beat.py` runs `git hash-object` / `git push origin ...:refs/heads/claude-heartbeat` in the current working directory!).
  - If an agent or launchd job runs `cd ~/YouTube/orbit-with-ben && python3 scripts/claude_beat.py` or `python3 scripts/jobs.py ... --git`, and the shim in `orbit-with-ben/scripts/` doesn't `os.chdir(STUDIO_REPO)` AND `os.execv(sys.executable, [sys.executable, str(STUDIO_REPO / "scripts" / script_name), *sys.argv[1:]])`:
    - `claude_beat.py` will push `claude-heartbeat` to `orbit-with-ben` while `chief_relay.py` in `studio/` reads `claude-heartbeat` from `studio` — making `chief_relay.py` think Claude is permanently dead after 90 minutes!
    - Even worse, if any worker runs an un-shimmed `orbit-with-ben/scripts/jobs.py` against `orbit-with-ben/jobs/queue.json` while another worker runs `studio/scripts/jobs.py` against `studio/jobs/queue.json`, the studio suffers an immediate **split-brain queue**!
- **Required Fix for the shim:**
  - Every shim in `orbit-with-ben/scripts/<name>.py` must be a pure `os.chdir(STUDIO_REPO)` + `os.execv` wrapper pointing to `studio/scripts/<name>.py`, **AND** `orbit-with-ben/jobs/queue.json` must be replaced in the same cut-over commit with a stub or removed so `orbit-with-ben/scripts/jobs.py` can never mutate a stale copy of `queue.json` in `orbit-with-ben`.

#### Stopper 3D: Hardcoded repo & branch coordinates in `board_site/api/*`, `owb_thread.py`, `board_check.py`, and `ai_spend`
- Look at what is hardcoded to `"TheLaughingGod1986/orbit-with-ben"` outside the 16 engine scripts:
  1. [`05_Analytics/kanban/board_site/api/ref.js`](../../../05_Analytics/kanban/board_site/api/ref.js) (line 9): `const REF = "https://api.github.com/repos/TheLaughingGod1986/orbit-with-ben/git/ref/heads/board-data";`
  2. [`05_Analytics/kanban/board_site/api/checks.js`](../../../05_Analytics/kanban/board_site/api/checks.js) (lines 16, 26):
     - `const STORE = ["TheLaughingGod1986/orbit-with-ben", 219];` (Issue #219 holds all of Ben's board checks/pairs/audit history!)
     - `const THREADS = { OWB: ["TheLaughingGod1986/orbit-with-ben", 264], HOS: ["TheLaughingGod1986/history-of-science", 180] };` (Note: `THREADS.OWB` is still hardcoded to `264` even though `scripts/thread.json` rolled to `478` on 4 Nov!)
  3. [`scripts/owb_thread.py`](../../../scripts/owb_thread.py) (line 24) and [`scripts/thread.json`](../../../scripts/thread.json) (line 2): `"repo": "TheLaughingGod1986/orbit-with-ben", "number": 478`. (Note: GitHub issues cannot be transferred with the same issue number to a new repo; if the studio thread stays in `orbit-with-ben` #478 until the 1 Dec rollover, `thread.json` must explicitly keep `"repo": "TheLaughingGod1986/orbit-with-ben"`).
  4. [`scripts/board_check.py`](../../../scripts/board_check.py) (lines 42, 46, 64): fetches `board-data` from `OWB` and posts alerts to `("TheLaughingGod1986/orbit-with-ben", 264)`.
  5. [`history-of-science/04_Audio/tools/ai_spend_hook.py`](../../../../history-of-science/04_Audio/tools/ai_spend_hook.py) (lines 17–18): `OWB = Path(os.environ.get("OWB_REPO", Path.home() / "YouTube" / "orbit-with-ben")); AI_SPEND = OWB / "scripts" / "ai_spend.py"`. If `05_Analytics/ai_spend/ledger.jsonl` moves to `studio/`, HOS minters calling `ai_spend_hook.py` via `OWB_REPO` will either fail or write to the old `orbit-with-ben` ledger unless `ai_spend.py` in `orbit-with-ben` is shimmed to `studio/`.

#### Stopper 3E: Vercel Dual-Project Collision (`studio-kanban` vs `orbit-content-ops`)
- Currently `orbit-with-ben` is connected to **two** Vercel projects:
  1. `orbit-content-ops` (root `07_Content-Ops`, hosting `/go` redirects; git auto-deploy disabled via `NO_DEPLOY` in `board_publish.py` lines 401–422).
  2. `studio-kanban` (root `05_Analytics/kanban/board_site`, hosting `studio-kanban.vercel.app`).
- Look at [`05_Analytics/kanban/board_site/build.py`](../../../05_Analytics/kanban/board_site/build.py) (lines 28–34, 47–55, 101–140, 198–220):
  - `build.py` reads `HERE.parent.parent / "dashboard" / "template.html"` (`05_Analytics/dashboard/template.html`) and `05_Analytics/dashboard/data.json` to build `/tracker` (`tracker.html`)!
  - `build.py` also scans `(ROOT / "02_Video-Projects").glob("*/status.json")` and `05_Analytics/kanban/film_briefs.json`!
  - **Breakage:** If Phase 3 copies `05_Analytics/kanban/board_site` to `studio/` without `05_Analytics/dashboard/template.html` (or if `05_Analytics/dashboard/` stays in `orbit-with-ben` where `07_Content-Ops/scripts/analytics-report.ts` writes it daily at 06:40), `build.py` in `studio/` will **crash on line 199** (`FileNotFoundError: .../dashboard/template.html`) on every Vercel deploy!
  - Even worse: at 06:40 daily, [`07_Content-Ops/launchd/analytics-snapshot.sh`](../../../07_Content-Ops/launchd/analytics-snapshot.sh) writes `05_Analytics/dashboard/data.json` to `orbit-with-ben` `main`, and [`scripts/board_publish.py`](../../../scripts/board_publish.py) (line 305) reads `WT / "owb" / "05_Analytics/dashboard/data.json"` and pushes it as `tracker.json` to `board-data`. If `board_publish.py` moves to `studio/`, it must still read `05_Analytics/dashboard/data.json` from `WT / "owb"` (or `analytics-snapshot` must move too), and `05_Analytics/dashboard/template.html` must be copied to `studio/`.

---

### Phase 4 — Plug-in ready (`core_sync.py` retirement & `channel_new.py`)
- **Verdict:** **FIX (Critical Misconception)**
- The plan states (line 85): *"Retire `core_sync.py` and the `studio-core/` copies (channels no longer carry engine code)."*
- **Why this will break the studio if done as written:**
  - Inspect [`studio-core/CORE_FILES.json`](../../../studio-core/CORE_FILES.json): it tracks **55 files**, and **zero** of them are studio engine scripts (`jobs.py`, `chief_relay.py`, `macbook_worker.py`, `board_publish.py`, `kanban_snapshot.py`, `video_tracker.py` are not in `CORE_FILES.json` at all!).
  - Instead, `CORE_FILES.json` locks the **shared channel production & publishing toolchain** duplicated inside both `orbit-with-ben` and `history-of-science`:
    - `00_Brand/Channel-Setup/tools/{gate_shorts_open.py, weekly_public_audit.py, test_weekly_public_audit.py}`
    - `04_Audio/tools/{el_auth.py, generate_sfx_from_script.py, orbit_cfr_delivery.py, strip_cg_native_audio.py, transcribe_vo.py}`
    - `07_Content-Ops/scripts/*` (`review-script.ts`, `gate-episode.ts`, `youtube-package-upload.ts`, `retitle-videos.ts`, `update-pinned-comment.ts`, etc.) and `07_Content-Ops/src/lib/*` (30 TypeScript modules).
  - **What breaks:** If `core_sync.py` and `.github/workflows/core-check.yml` are retired in Phase 4 while `07_Content-Ops/`, `04_Audio/tools/`, and `00_Brand/Channel-Setup/tools/` remain per-channel copies in `orbit-with-ben`, `history-of-science`, and `<third-channel>`, those 55 files will immediately drift across channels with no CI guard.
  - **Required Fix:** Either **(a) keep `core_sync.py` and `studio-core/CORE_FILES.json`** (pointed at `studio/` or `orbit-with-ben` as canonical) for shared channel-level production/publishing tools across all N channel repos, **OR (b)** extract `07_Content-Ops`, `04_Audio/tools`, and `gate_shorts_open.py` into `studio/` (invoked via `flow.json` with `--project <channel-checkout> --config <channel-checkout>/studio/channel.json`). Option (a) is zero-risk for Phase 4; Option (b) can follow later.

---

## 3. Phase 3 Cut-Over Runbook & Exact Undo at Each Step

To guarantee the studio never stops for more than ~60 seconds during Phase 3 cut-over, execute the cut-over on the Mini in **7 atomic steps**, with a verified **1-command Undo** at every step:

| Step | Cut-Over Action | What Could Fail | Exact Undo Command / Action (< 60 s) |
|---|---|---|---|
| **Pre-flight** | Ensure `TheLaughingGod1986/studio` is **PUBLIC** (or proxy `board.json`/`tracker.json` via Vercel API), add `TheLaughingGod1986/studio` to `BOARD_GH_TOKEN` and Codex's allow-list (`docs/CODEX_ALLOWLIST.md`), and verify `studio.py` / `jobs.py` no longer require `02_Video-Projects/` inside `ROOT`. Clone `~/YouTube/studio` on the Mini and `~/_desk/worker/studio` + `slot2/studio` on the MacBook. | Missing repo access on `BOARD_GH_TOKEN` or Codex CLI sandbox refusal. | Nothing live touched yet; fix token/allow-list before proceeding. |
| **Step 1: Pause workers cleanly** | Touch pause files on Mini and MacBook:<br>`touch ~/_desk/state/chief-relay.pause ~/_desk/state/macbook-worker.pause`<br>Wait for any active `jobs.py` git transaction (1–2 s) to finish. | An agent is mid-job. (Pause files don't kill running jobs; they only stop the next tick from claiming a new one while `jobs/queue.json` moves.) | `rm -f ~/_desk/state/chief-relay.pause ~/_desk/state/macbook-worker.pause` |
| **Step 2: Sync final state to `studio` & push `board-data` / heartbeats** | Copy latest `jobs/queue.json`, `jobs/WIP.json`, `jobs/backlog.json`, `jobs/reviews/`, `05_Analytics/ai_spend/`, `05_Analytics/kanban/`, `05_Analytics/dashboard/template.html` into `~/YouTube/studio`, commit & push `main`, and push current `board-data`, `mini-heartbeat`, `claude-heartbeat`, `macbook-heartbeat{,-2}` refs to `studio`. | `board_publish.py --dry-run` in `~/YouTube/studio` fails on a missing sparse path or template. | Keep `orbit-with-ben` untouched; fix path in `~/YouTube/studio` and re-test `python3 ~/YouTube/studio/scripts/board_publish.py --dry-run` before touching any plist or shim. |
| **Step 3: Land exec-forwarding shims in `orbit-with-ben/scripts/`** | Replace the engine scripts in `orbit-with-ben/scripts/` (`jobs.py`, `chief_relay.py`, `board_publish.py`, `claude_beat.py`, `ai_spend.py`, `refill.py`, `owb_thread.py`, etc.) with `os.chdir(STUDIO_REPO)` + `os.execv` shims that forward to `STUDIO_REPO` (`$STUDIO_REPO` or `~/YouTube/studio` on Mini, `~/_desk/worker/.../studio` on MacBook). Keep `orbit-with-ben/jobs/queue.json` read-only / removed so no script can write a split-brain queue. | A cloud session or old script runs in an environment where `~/YouTube/studio` doesn't exist yet. (Guard the shim: if `STUDIO_REPO` is missing, auto-clone `https://github.com/TheLaughingGod1986/studio.git` with `--depth 50`, just like `com.owb.macbook-worker.plist` line 23 does!) | `git -C ~/YouTube/orbit-with-ben revert HEAD && git -C ~/YouTube/orbit-with-ben push origin main` (restores full engine scripts in `orbit-with-ben` immediately). |
| **Step 4: Re-point Vercel `studio-kanban` & client `DATA_REF`** | Update `DATA_REF` / `DATA` in `board_site/{studio_app.js,tracker_app.js,ai_app.js,shim.js,tracker_loader.js,api/ref.js}` to `TheLaughingGod1986/studio` (keep `STORE` in `api/checks.js` on `orbit-with-ben#219` so Ben's check history and open ticks don't move!). Redeploy `studio-kanban` to Vercel (`vercel --prod`). Run `python3 ~/YouTube/studio/scripts/board_check.py --no-post` to verify `200 OK` and all Ready-for-OK Play links. | `board_check.py` reports non-200 or missing cards. | Instant rollback in Vercel dashboard ("Promote to Production" on the previous deployment, takes ~5 s), and keep `board_publish.py` pushing `board-data` to **both** `studio` and `orbit-with-ben` remotes during the 7-day bake window! |
| **Step 5: Re-point Mini launchd plists** | Update `~/Library/LaunchAgents/{com.owb.chief-relay,com.owb.board-publish,com.owb.missed-runs,com.owb.ai-spend-daily,com.owb.tab-janitor}.plist` (and `STUDIO_REPO` in `analytics-snapshot.sh`) to `~/YouTube/studio`, reload with `launchctl bootout` + `launchctl bootstrap`, and remove `~/_desk/state/chief-relay.pause`. | A launchd job exits non-zero due to missing `STUDIO_REPO` or `PATH` env var. | Copy back the backup plists from `~/YouTube/orbit-with-ben/scripts/mini/` & `07_Content-Ops/launchd/` and run `launchctl bootout` + `launchctl bootstrap` (or rely on the Step 3 shims in `orbit-with-ben/scripts/`). |
| **Step 6: Re-point MacBook worker plist & slots** | Update `~/Library/LaunchAgents/com.owb.macbook-worker.plist` to bootstrap and run `studio/scripts/macbook_worker.py` (which manages `slot1` and `slot2` clones of `studio` + all channels in `channels.json`), reload launchd, and remove `~/_desk/state/macbook-worker.pause`. | MacBook worker fails `pull_main()` on a slot checkout. | Re-bootstrap the previous `com.owb.macbook-worker.plist` pointing at `orbit-with-ben`; Step 3 shims ensure it still talks to the live `studio` queue. |
| **Step 7: Dual-push `board-data` for 7 days, then archive old copies** | For 7 days, have `studio/scripts/board_publish.py` push `board-data` to both `studio` and `orbit-with-ben` (1 extra `git push -f` takes ~0.8 s). After 7 days of green `board_check.py` and `missed_runs.py`, move old files in `orbit-with-ben` to `_archive/`. | Any cached phone tab still polling `orbit-with-ben/board-data` before `updater.js` reloads it. | Dual-pushing `board-data` to both repos means even an un-reloaded phone tab sees live data with zero gap! |

---

## 4. Answers to the Four Open Questions (`docs/MULTI_CHANNEL_PLAN.md` §§96–102)

### Question 1: One queue for all channels, or one per channel?
- **Answer:** **Definitely ONE queue (`studio/jobs/queue.json`), as the plan proposes.**
- **Why:**
  1. All compute lanes (Mini `chief_relay.py`, MacBook `macbook_worker.py` slots 1 & 2, and Claude's hourly run) and all subscription pools (ElevenLabs, Google Flow AI Ultra, Vertex £ credit, Cursor, Codex, Claude) are shared across channels.
  2. Cross-channel scheduling rules — Rule G (`WIP.json` per-channel active caps: 5 OWB, 4 HOS, N for Channel 3), `channel_balance.py` (4 longs/month fairness rule), shared deadline ordering (`workflow_state.py`), and single-elected-Chief succession — require a single global view of ready, claimed, and blocked jobs.
  3. Separate queues per channel would reintroduce race conditions on `studio-metadata.lock`, duplicate `refill.py` / `review_lane.py` sweeps, and force `board_publish.py` to merge N queues every minute.

### Question 2: Should `flow.json` gate commands run inside the channel checkout, and how is a channel's tool trusted?
- **Answer:** **Yes — run inside the channel checkout (`cwd = channels.repo_path(slug)`), using an argument-list schema (`argv`, never `shell=True`), validated by CI and restricted to repo-relative paths.**
- **Concrete design & trust rules:**
  1. **No shell interpolation:** Store commands in `studio/flow.json` as structured arrays or known tool templates (e.g. `{"stage": "script", "gate": ["npm", "--prefix", "07_Content-Ops", "run", "review:script", "--", "--file", "{script}"]}` or `["python3", "00_Brand/Channel-Setup/tools/gate_shorts_open.py", "check", "{short}", "--air-date", "{air_date}"]`), executed with `subprocess.run(argv, cwd=channel_root, shell=False)`.
  2. **Path confinement:** A lint test (`test_channels.py`) in CI must verify that every `flow.json` executable inside the repo resolves inside `channel_root` (no `..`, no `/tmp`, no curl/network bootstrap) or is in the allow-listed system binaries (`python3`, `npm`, `npx`).
  3. **Rule hierarchy enforcement:** `flow.json` can add channel-specific gates (e.g., HOS `hos-contract` or `vo_check.py`; OWB `picture_qa.py` and `music_gate.py`), but **cannot disable studio-wide gates** enforced by `studio/scripts/jobs.py` (such as the Ben gate on `needs=ben`, no deletes, `PUBLISHING_DRY_RUN=true` default, and Chief authority checks).

### Question 3: Phase 3 history copy: `git filter-repo` with history, or a fresh repo with a pointer commit?
- **Answer:** **Use `git filter-repo` (preserving commit history of `scripts/`, `jobs/`, `channels/`, and `05_Analytics/kanban/`), PLUS a pointer tag/commit in `orbit-with-ben`.**
- **Why history is required (not just nice to have):**
  1. Look at [`scripts/kanban_snapshot.py`](../../../scripts/kanban_snapshot.py) line 18: *"every stage in hand gets a `since` (when it took its current state, from the file's git history) so the page can say 'in this stage 2 days'"*.
  2. Look at [`scripts/missed_runs.py`](../../../scripts/missed_runs.py) lines 24–27 & 49: `git log origin/main -1 --format=%cI -E --grep="^Channel tracker 20" --since="14 days ago"` and `"^Buffer check 20"`. A fresh repo with no commit history immediately triggers false `[alarm tracker]` and `[alarm buffer]` posts on the studio thread (`"no record in 14 days"`)!
  3. Auditability of `jobs/reviews/Jxxxx/REVIEW.md` and `05_Analytics/ai_spend/ledger.jsonl` depends on `git log` / `git blame` across the October–November 2026 studio history.

### Question 4: Anything the Mini launchd and the MacBook worker need beyond a path change?
- **Answer:** **Yes — 6 concrete items beyond changing paths:**
  1. **Dynamic `--add-dir` list for agent CLIs (`chief_relay.py` & `macbook_worker.py`):**
     - Currently [`scripts/chief_relay.py`](../../../scripts/chief_relay.py) (lines 363, 374) and [`scripts/macbook_worker.py`](../../../scripts/macbook_worker.py) (line 260) pass `--add-dir <HOS> --add-dir ~/_desk` to `codex`, `claude`, and `agy` (running with `cwd=OWB`).
     - Once `cwd` is `studio/`, neither `OWB`, `HOS`, nor `<third-channel>` is inside `cwd`! Both runners must dynamically construct `--add-dir` from `[channels.repo_path(s) for s in channels.slugs()] + [STATE.parent]` so sandboxed CLIs (`codex`, `claude`, `agy`) have write access to every registered channel checkout.
  2. **Multi-slot auto-clone of all registered channels in `macbook_worker.py`:**
     - `macbook_worker.py` (`URLS`, `own_checkout()`, `pull_main()`, `start_other_slots()`, lines 54–82, 374–414, 518–520) hardcodes `OWB` and `HOS`. It must loop over `channels.all_channels()` + `studio`, cloning `slot_dir(SLOT) / slug` for every channel in `channels.json` and checking that **every** checkout is returned to `main` after each job.
  3. **Self-healing bootstrap in `com.owb.macbook-worker.plist`:**
     - [`scripts/macbook/com.owb.macbook-worker.plist`](../../../scripts/macbook/com.owb.macbook-worker.plist) line 23 has a self-healing `test -f ... || git clone ... https://github.com/TheLaughingGod1986/orbit-with-ben.git`. That URL and path must be updated to `studio.git` so the MacBook worker never locks itself out if `~/_desk/worker/studio` is missing.
  4. **Mini `mini_repair.py` repo list (`scripts/mini_repair.py` lines 226, 237) and `chief_relay.py` line 1310:**
     - Currently repairs `(OWB, HOS)`. Must repair `(STUDIO, *[channels.repo_path(s) for s in channels.slugs()])` so a dirty worktree or diverged `main` in `studio` or any channel repo is auto-rescued.
  5. **Mini `board_publish.py` `quick_key()` (`ls-remote`) and sparse worktrees (`WT / <slug>`):**
     - [`scripts/board_publish.py`](../../../scripts/board_publish.py) (`quick_key()`, lines 465–474, and `build()`, lines 281–286) hardcodes `remote(OWB, ...)` and `remote(HOS, ...)` plus `OWB_SPARSE` and `HOS_SPARSE`. It must loop over `studio` + `channels.all_channels()`, creating `WT / slug` sparse worktrees per channel.
  6. **All 7 Mini launchd jobs (not just `chief-relay` and `board-publish`):**
     - On the Mini, there are **7** launchd plists across `scripts/mini/` and `07_Content-Ops/launchd/`:
       1. `com.owb.chief-relay.plist` → moves to `studio`
       2. `com.owb.board-publish.plist` → moves to `studio`
       3. `com.owb.missed-runs.plist` → moves to `studio` (reads `mini-heartbeat` and `claude-heartbeat` on `studio`, plus tracker/buffer commits!)
       4. `com.owb.ai-spend-daily.plist` → moves to `studio` (writes `ai_spend/ledger.jsonl`)
       5. `com.owb.tab-janitor.plist` → moves to `studio` (`cdp_tabs.py`)
       6. `dev.orbit.analytics-snapshot.plist` (`analytics-snapshot.sh`) → runs `07_Content-Ops` and commits `05_Analytics/` (if `05_Analytics` stays in `orbit-with-ben`, `missed_runs.py` in `studio` must check `orbit-with-ben` `origin/main` for `"^Channel tracker 20"`, not `studio` `origin/main`!)
       7. `dev.orbit.buffer-check.plist` (`buffer-check.sh`) → runs `07_Content-Ops/scripts/buffer-mirror.ts check` for each channel and commits `social/` (if `buffer-check.sh` commits to `orbit-with-ben`, `missed_runs.py` in `studio` must check `orbit-with-ben` `origin/main` for `"^Buffer check 20"`, or `missed_runs.py` will fire a false `[alarm buffer]` every day!).

---

## 5. Anything Missing from `docs/MULTI_CHANNEL_PLAN.md`

1. **TypeScript Channel Registries in `07_Content-Ops` (`channel-tracker.ts`, `buffer-profile.ts`, `hos-buffer-register.ts`):**
   - The plan mentions 16 Python scripts in `scripts/`, but `07_Content-Ops` has its own hardcoded `"owb" | "hos"` registries in TypeScript:
     - [`07_Content-Ops/src/lib/analytics/channel-tracker.ts`](../../../07_Content-Ops/src/lib/analytics/channel-tracker.ts) (lines 19–24): `export type ChannelKey = "owb" | "hos"; export const CHANNELS = { owb: ..., hos: ... };`
     - [`07_Content-Ops/src/lib/publishing/buffer-profile.ts`](../../../07_Content-Ops/src/lib/publishing/buffer-profile.ts) (lines 16–71): `export type ProfileId = "owb" | "hos"; export const PROFILES = { owb: ..., hos: ... };`
     - [`07_Content-Ops/launchd/buffer-check.sh`](../../../07_Content-Ops/launchd/buffer-check.sh) (lines 29–36): runs `buffer-mirror.ts check` then `buffer-mirror.ts check --channel hos`.
     - [`history-of-science/07_Content-Ops/src/lib/publishing/hos-buffer-register.ts`](../../../../history-of-science/07_Content-Ops/src/lib/publishing/hos-buffer-register.ts): registers HOS Shorts into `orbit-with-ben/00_Brand/Channel-Setup/social/hos/UPLOADS.json`.
   - **Recommendation:** Include `channel-tracker.ts`, `buffer-profile.ts`, and `buffer-check.sh` in Phase 1/2 so they read `channels.json` / `<channel>/studio/channel.json` (youtube channel ID, analytics token env var, Buffer org/channel IDs, social dir, R2 media prefix). Otherwise a third channel won't get daily analytics snapshots or Buffer mirroring when plugged in.

2. **Two-Tier `AGENTS.md` / `sync_rules.py` Enforcement:**
   - Currently [`scripts/sync_rules.py`](../../../scripts/sync_rules.py) syncs `<!-- SYNC: AGENTS.md#... -->` blocks inside one repo and scans `STALE` regexes.
   - With `studio/AGENTS.md` (studio-wide rules: Ben gate, Never list, Who does what) and `<channel>/studio/RULES.md` (channel rules: title shapes, voice, picture route, UAT hard fails), `sync_rules.py` should verify in CI that no channel's `AGENTS.md` or `studio/RULES.md` contradicts or drops the studio-wide `<!-- SYNC: studio/AGENTS.md#Never -->` and `#Stop and ask Ben` blocks.

3. **Unifying `hos_desk.py` into the Studio Queue for Channel 3:**
   - HOS still has a legacy desk script (`00_Brand/Channel-Setup/tools/hos_desk.py`) referenced in `chief_relay.py` (lines 668–676, 709, 1552–1554), while also using `jobs.py` (`repo: "hos"`).
   - The plan should explicitly state that **new channels use `studio/jobs/queue.json` and `studio/flow.json` exclusively** (no new per-channel `*_desk.py` scripts), and `hos_desk.py` is legacy HOS-only until retired.

4. **Codex Unattended Allow-List (`Rule F` / `docs/CODEX_ALLOWLIST.md`) & `BOARD_GH_TOKEN` Scope:**
   - Add an explicit pre-cutover checklist item in Phase 3 to:
     - Add `TheLaughingGod1986/studio` (and `<third-channel>` when created) to the Mini's Codex allow-list (`AGENTS.md` Rule F / `docs/CODEX_ALLOWLIST.md`).
     - Grant `BOARD_GH_TOKEN` (used by Vercel `api/checks.js` and `api/ref.js`) access to `TheLaughingGod1986/studio` (or keep issue `#219` in `orbit-with-ben`).
     - Update `THREADS` in [`05_Analytics/kanban/board_site/api/checks.js`](../../../05_Analytics/kanban/board_site/api/checks.js) so it reads thread issue numbers dynamically from `channels.json` / `thread.json` instead of hardcoding `OWB: 264, HOS: 180`.
