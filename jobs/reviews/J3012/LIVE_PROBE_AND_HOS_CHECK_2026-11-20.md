# J3012 — PR #1011 Chief Merge, Live Board Credential Probe & HOS Checkout Verification

20 November 2026, ~16:45–16:52 UTC. Acting Chief: Gemini (`gemini`; Claude down until `2026-11-20T17:50:00Z`, Grok Bot down until `2026-11-20T17:33:46Z`, Codex down until `2026-11-24T23:26:00Z`). Progress preserved at **3/4**. No live cutover or active-studio marker installed. £0 spend.

## 1. Independent Chief review and merge of PR #1011

Reviewed Codex-authored [PR #1011](https://github.com/TheLaughingGod1986/orbit-with-ben/pull/1011) (`codex/j3012-studio-move`, exact head `055ed1509fbae75e280ec403e279c364144f8093`, 121 files).

- Clean test merge onto `origin/main` in isolated worktree (`/private/tmp/j3012-review-wt`, zero conflicts):
  - Full Python unittest suite: **1,502 tests PASS** (6 skipped, 0 failures, 0 errors).
  - Content Ops vitest suite: **24 files / 232 tests PASS**.
  - `TMPDIR=/private/tmp python3 scripts/studio_split.py --no-tests`: **PASS** (`left: 0` across all 7 non-test groups; 0 addresses, 0 keys, 0 unrouted).
  - All GitHub PR CI checks green (`Content Ops checks`, `Notes check`, `Rules check` SUCCESS; `Studio core check` SKIPPED).
- Re-checked `chief_relay.py status` (`Chief: Gemini`), posted independent Chief PASS review, and merged PR #1011 with `--match-head-commit 055ed1509fbae75e280ec403e279c364144f8093` → merge commit `24058503f8` on `main`.
- Merging lands `docs/STUDIO_MOVE.md`, dormant `engine_guard.py` writer guards, and `scripts/mini/inventory_services.py` on `main` without activating the move (active-studio marker absent; Cloudflare Pages `studio-kanban` has no Git auto-deploy; `/api/migration` disabled unless `BOARD_MIGRATION_PROBE=1`).

## 2. Live production board credential probe (`BOARD_GH_TOKEN`)

Verified current live `studio-kanban` production build before probing: `version: 23884765ba0e03bf` (matching unmodified `origin/main` `05_Analytics/kanban/board_site/build.py`). Independently confirmed via GitHub API that private `TheLaughingGod1986/studio` exists (`private: true`), ref `rehearsal/j3012` points to `534cf0f70852e06414cbe39f6a01efe9024c8a91`, and `channels/channels.json` exists (`sha: 5e5a170703efbcf6c67254f72210830fc9cd952f`).

Ran two strictly bounded narrow production probes (exact `origin/main` `board_site` + `api/migration.js` + `cf_worker.js` + `BOARD_MIGRATION_PROBE=1` only; `try/finally` immediate restoration of unmodified production build; no secrets printed or passed on CLI/URL):

1. **Probe 1 (`062592da-e2e2-40c1-ab61-958a3b5ac582`, deleted):**
   - Anonymous `GET /api/migration`: `401` (`Cache-Control: no-store`, `{"error":"sign in"}`).
   - Authenticated `GET /api/migration` (`x-board-key`): `502` (`{"error":"probe failed","stage":"repository"}`).
   - **Root cause:** Cloudflare Workers (`workerd`) `fetch()` supports `redirect: "follow"` or `"manual"` only; `redirect: "error"` throws `TypeError` immediately before hitting GitHub. Fixed in this PR to `redirect: "manual"` (still never follows redirects; `!r.ok` rejects any 3xx status, covered by new unit test).
2. **Probe 2 (`b1114bff-e98f-48e9-9ce9-faf76ec400d2`, deleted) with `redirect: "manual"`:**
   - Anonymous `GET /api/migration`: `401` (`Cache-Control: no-store`, `{"error":"sign in"}`).
   - Authenticated `GET /api/migration` (`x-board-key`): **`502` (`Cache-Control: no-store`, `Vary: Cookie, x-board-key`, `{"error":"upstream refused","stage":"repository","status":404}`)**.
3. **Conclusion (proven):** On GitHub's REST API, HTTP `404` for an independently confirmed private repository proves production `BOARD_GH_TOKEN` does **not** currently have repository access to `TheLaughingGod1986/studio`. Ben must perform the one-time token scope update before cutover:
   - GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens → open the board token (`BOARD_GH_TOKEN`).
   - **Repository access:** add `TheLaughingGod1986/studio` (keep `orbit-with-ben` and `history-of-science`).
   - **Repository permissions:** set **Contents** to **Read-only** (Metadata Read-only comes with it; keep **Issues** Read and write).
   - Save. Only if GitHub displays a new token string (or if replacing a classic token), update `BOARD_GH_TOKEN` in Cloudflare Pages → `studio-kanban` → Settings → Environment variables (Production).
4. **Clean restoration & cleanup verified:**
   - Restored exact unmodified production build (`fa4baa50`, `version: 23884765ba0e03bf`).
   - Deleted both temporary probe deployments (`062592da-e2e2-40c1-ab61-958a3b5ac582` and `b1114bff-e98f-48e9-9ce9-faf76ec400d2`).
   - Post-restore checks on `https://board.oppti.dev`: `/api/migration` → `404`; `/version.json` → `200` (`23884765ba0e03bf`); `/`, `/tracker`, `/ai`, `/api/checks` → all `200` with `X-Robots-Tag: noindex, nofollow`.

## 3. HOS live checkout exporter-guard verification

Verified `/Users/benjaminoats/YouTube/History Of Science` (read-only):
- Shared checkout is now on `main` at `9f3acbae`, which includes merged HOS [PR #688](https://github.com/TheLaughingGod1986/history-of-science/pull/688) (`f3188f03b9e5a727d5cdf57bc19da760b6746ac6`).
- All three guarded standalone Flow exporters (`009/_mint_flow_v05_tranche2.py`, `010/_mint_flow_twelve_plates_j2268.py`, `013/_mint_flow_v01_pass1.py`) are clean against `origin/main` and carry `require_active_spend_destination`.
- `python3 -m unittest tests.test_studio_spend_destination -v` passes **5/5** directly inside the shared HOS checkout.
- Grep across all `_mint_flow*.py` scripts on both Mini and NAS (`/Volumes/data/studio-live/History Of Science/02_Video-Projects/`) confirmed zero other files write directly to the shared spend ledger.
- Zero active Flow/export processes running (`ps aux`).

## 4. Operational note & remaining pre-cutover gates

- **Scratch SSD capacity:** `/Volumes/MiniWork` is at 100% capacity (`264 MiB` free), which caused a default `studio_split.py` run to fail with `ENOSPC` when writing to `/Volumes/MiniWork/scratch`. Using `TMPDIR=/private/tmp` (31 GiB free) succeeded; clear scratch capacity before the final frozen cutover export.
- **Remaining before cutover (aim Mon 23 / Tue 24 Nov):**
  1. Complete MacBook installed/loaded service inventory (`inventory_services.py --loaded`) and `TheLaughingGod1986/studio` Git/`gh` read check (queued as a read-only `--needs macbook` companion job now that `inventory_services.py` is on `main`).
  2. Ben's one-time `BOARD_GH_TOKEN` repository grant for `TheLaughingGod1986/studio` (`Contents: Read-only`), followed by a quick re-probe confirming `200 {ok: true, contentsRead: true}`.
  3. Preceding-day cutover notice on #954 (Sun 22 Nov for Mon 23 Nov, or Mon 23 Nov for Tue 24 Nov) once items 1–2 hold.
  4. Drained cutover execution, fresh root-commit export to `main` on `TheLaughingGod1986/studio`, and live relay + board publish + harmless tick + both-MacBook-slot acceptance.
