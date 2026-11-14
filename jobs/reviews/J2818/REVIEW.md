# J2818 Condition Verification & Review — J2798 (`Board: stop an open board downloading its whole 2 MB data file every minute`)

- **Verification Job:** `J2818` (`Verify condition for J2798`, `kind: review`, `recheck_of: J2798`)
- **Parent Job:** `J2798` (`Board: stop an open board downloading its whole 2 MB data file every minute`, `status: blocked`, `by: codex`, `after: J2796`, `needs: mini`, `kind: studio`, `repo: owb`, `due: 2026-11-15T18:00:00Z`)
- **Verifier:** `gemini` (`Gemini 4 Argon (High)`, specialist worker on the Mini; `Grok Bot` is elected Chief)
- **Checked At:** `2026-11-14T08:41Z–09:03Z`
- **Verdict:**
  1. **Predecessor condition (`after: J2796`) & Detached Captures (`J2798-fixture-exact-v2`, `J2798-live-current`):** **SATISFIED / COMPLETE** (`J2796` is `done` since `2026-11-14T02:44Z`, commit `7060b03eb5`; both detached captures started by Codex at `08:35Z` have now finished with exit code `0`, and `J2798-fixture-exact-v2` **PASSES** the `< 20,000 bytes/min` target on both `/` and `/tracker`).
  2. **Production Rollout & Live Acceptance Gate:** **PENDING CHIEF MERGE/DEPLOY OF PR #924 + POST-DEPLOY 10-MINUTE LIVE CAPTURE** (`PR #924` at `680ed3ace10a48de00458e1d4e8ddef6c318f93a` is open with green CI and awaiting Chief merge/deploy; live production still runs the pre-PR-#924 code where `updates.json` lacks `publishedAt` and `/` transferred `201,892.3 bytes/min` in `J2798-live-current`).
  3. **Queue State Note:** When Codex parked `J2798` for Chief (`jobs.py block J2798 --reason "parked for Chief: review/merge/deploy PR 924..."`), `reconcile_holds` attached a synthetic dependency hold (`"Required predecessor is complete; verify remaining gates and approvals"`) because `J2798` still carries `"after": "J2796"`. That `hold` dict causes `workflow.external_hold(J2798)` to be truthy, which changes `workflow.state(J2798)` from `"review"` to `"waiting"` and hides `J2798` from `chief_relay.py` Chief duties. Reopening `J2798` (`Option A` below) clears the synthetic `hold` so the merge/deploy and post-deploy live capture can proceed without delay.

---

## 1. Element-by-Element Verification (`2026-11-14T08:41Z–09:03Z`)

| Item / Gate | Status | Evidence Checked |
|---|---|---|
| **1. Predecessor `J2796` (`after: "J2796"`)** | **SATISFIED (`done`)** | `J2796` completed at `2026-11-14T02:44Z` (`PR #910` merged as `7060b03eb5`; `jobs/reviews/J2796/CHIEF_REVIEW.md`). |
| **2. Original Ben Approval (`2026-11-14T00:35Z`) & Guards** | **VALID** | Ben in chat (`14 Nov 00:35Z`): `"Cool let's do all 6"`. £0 spend, Cloudflare Pages free plan only, no secret/email/private-network address in tracked files, R2 and ticks store untouched. |
| **3. Detached 20-Minute Exact-Byte Fixture Capture (`J2798-fixture-exact-v2`)** | **COMPLETE & PASS (`done = 0` at `08:56Z`)** | `/Users/benjaminoats/_desk/logs/J2798-fixture-exact-v2.done` = `0`; `J2798-fixture-exact-v2.json`:<br>- **`/` (Board):** `firstRenderMs = 340 ms`, 10-min `idleBytes = 15,338 B` (**`1,533.8 B/min`** < `20,000 B/min` target), 10-min `oneFilmChangeBytes = 25,450 B` (**`2,545.0 B/min`**), **`0` post-initial full `f=board` reads**.<br>- **`/tracker` (Tracker):** `firstRenderMs = 244 ms`, 10-min `idleBytes = 18,035 B` (**`1,803.5 B/min`** < `20,000 B/min` target), 10-min `oneFilmChangeBytes = 8,020 B` (**`802.0 B/min`**), **`0` post-initial full `f=board` reads**. |
| **4. Detached 10-Minute Pre-Deploy Live Capture (`J2798-live-current`)** | **COMPLETE (`done = 0` at `08:45Z`) — confirms PR #924 rollout is still needed** | `/Users/benjaminoats/_desk/logs/J2798-live-current.done` = `0`; `J2798-live-current.json` (measuring currently deployed pre-PR-#924 production at `https://studio-kanban.pages.dev`):<br>- **`/` (Board):** `firstRenderMs = 2,017 ms`, `errors = []`, 10-min `idleBytes = 2,018,923 B` (**`201,892.3 B/min`**; 8 total `f=board` downloads — initial + 7 post-initial fallbacks at minutes 1, 2, 5, 6, 7, 8, 9).<br>- **`/tracker` (Tracker):** `firstRenderMs = 723 ms`, `errors = []`, 10-min `idleBytes = 20,898 B` (**`2,089.8 B/min`** < `20,000 B/min` target; `0` full `f=board` downloads). |
| **5. PR #924 (`codex/j2798-measure-fix`, head `680ed3ace10a48de00458e1d4e8ddef6c318f93a`)** | **OPEN, CI GREEN, UNIT TESTS PASS (`47/47` Python + JS client suite)** | - GitHub Actions: `Rules check` `SUCCESS` (`2026-11-14T08:40:16Z`), `Studio core check` `SKIPPED`.<br>- Re-ran in `/Volumes/MiniWork/scratch/J2798-measure-fix`: `PYTHONPATH=scripts python3 -m unittest scripts/test_board_updates.py scripts/test_board_publish.py` (`47` tests `OK`) and `node scripts/test_board_updates_client.cjs` (`OK`). |

---

## 2. Technical Audit of `J2798-live-current` & PR #924 (`board_updates.js` / `board_publish.py`)

Inspecting the request timeline of `J2798-live-current.json` (`08:35:38Z–08:45:39Z`) alongside `~/_desk/state/board/publish.log` and live `/api/data?f=updates` shows why the 7 post-initial `f=board` downloads occurred and highlights one remaining cache-skew case that should be guarded so the post-deploy 10-minute production capture has **zero** post-initial `f=board` downloads (since a single `~276 KB` Brotli `f=board` response during a 10-minute window adds `27,600 B/min` and immediately breaches the `< 20,000 B/min` ceiling):

1. **Why `f=updates` oscillates in live production:** Without `BOARD_GH_TOKEN` on Cloudflare Pages, `readFile()` in `05_Analytics/kanban/board_site/api/data.js` tries unauthenticated `api.github.com` first and falls back to `raw.githubusercontent.com` (Fastly CDN, up to 5-minute cache) whenever a Cloudflare egress IP hits GitHub's 403 rate limit. In `J2798-live-current.json`, consecutive minute polls of `/api/data?f=updates` returned wire sizes `8759 -> 7812 -> 8905 -> 381 (304) -> 9122 -> 8835 -> 10562 -> 8926 -> 336 (304) -> 8715 -> 8863`, alternating between fresh `api.github.com` reads and older `raw.githubusercontent.com` reads.
2. **Forward skew (`f=board` newer than `f=updates` on a full read leaves `revision = ""`):**
   - PR #924 guards backward skew (`if (Date.parse(update.publishedAt) < Date.parse(raw.publishedAt)) return new Response(JSON.stringify(raw));`).
   - However, when a full `f=board` fetch returns a snapshot (`etag = E2`, `publishedAt = T2`) that is **newer** than the `f=updates` response from that same poll (`snapshotEtag = E1`, `publishedAt = T1 < T2`), `board_updates.js` lines 65–71 set `revision = ""` (because `E2` is not yet in `T1`'s `update.edits`) and do not store `etag` (`E2`).
   - On a later poll when `f=updates` catches up to `T2` (`publishedAt == T2`, `snapshotEtag == E2`) or advances to `T3 > T2` (with `{from: R2, to: R3, fromEtag: E2}` in `update.edits`), `Date.parse(update.publishedAt) < Date.parse(raw.publishedAt)` is `false` and `at = revision` is still `""`, forcing an unnecessary second `276 KB` `f=board` download.
   - **Fix (6 lines in `05_Analytics/kanban/board_site/board_updates.js`):** Keep `rawEtag` alongside `raw` and `revision`. At the start of `if (update && raw)`, if `!revision && rawEtag`, resolve `revision` via `update.snapshotEtag === rawEtag ? update.revision : (update.edits.find(e => e.fromEtag && e.fromEtag === rawEtag) || {}).from || ""`; and change `<` to `<=` on `Date.parse(update.publishedAt) <= Date.parse(raw.publishedAt)` so a poll whose `update` matches `raw`'s timestamp returns `raw` immediately. When edits apply (`at === update.revision`), set `rawEtag = update.snapshotEtag || ""`.
3. **Unpushed local state in `scripts/board_publish.py` (`finish()`, lines 742–760):**
   - `finish()` currently writes `STATE / "updates.json"` and `STATE / "board.json"` **before** checking `if whole == prev.get("whole") and not a.force: return 0` and before `push()` succeeds. When `git push` fails (as logged at `2026-11-14T08:39:46Z: [remote rejected] f889c5f0... -> board-data (failed)`), local `STATE / "board.json"` and `STATE / "updates.json"` advance to a revision that never reached `origin/board-data`. Writing `STATE / "updates.json"` and `STATE / "board.json"` only when `whole != prev.get("whole") or a.force` and after `push()` succeeds keeps local state strictly aligned with `origin/board-data`.

---

## 3. Queue Commands for Elected Chief (`chief` / `codex`)

Because `scripts/jobs.py` (`set_wait` line 531 and `do_reopen` line 961) restricts `wait --recheck` and `reopen` on a held job to the elected Chief, `J2818` is parked for the elected Chief to run either **Option A (Recommended)** or **Option B**:

### Option A (Recommended — Clear the synthetic dependency hold by reopening `J2798` so PR #924 rollout + post-deploy 10-minute live measurement can run)

```bash
python3 scripts/jobs.py reopen J2798 --agent <chief_agent> \
  --note "J2818 verified at 2026-11-14T09:03Z (jobs/reviews/J2818/REVIEW.md): predecessor J2796 is done (7060b03eb5); Ben approval (14 Nov 00:35Z) is valid; both detached captures finished with exit 0 (J2798-fixture-exact-v2 PASS: / idle 15338 B = 1533.8 B/min, 1-change 25450 B, firstRender 340 ms; /tracker idle 18035 B = 1803.5 B/min, 1-change 8020 B, firstRender 244 ms; 0 post-initial f=board reads; J2798-live-current pre-deploy baseline: / 201892.3 B/min, /tracker 2089.8 B/min). Reopened to clear the synthetic dependency hold so PR #924 (680ed3ace1; plus rawEtag/<= skew guard in jobs/reviews/J2818/REVIEW.md) can be merged/deployed and verified with a 10-minute production capture <20000 B/min." \
  --git

python3 scripts/jobs.py done J2818 --agent <chief_agent> \
  --result "Verified J2798 waiting condition at 2026-11-14T09:03Z (jobs/reviews/J2818/REVIEW.md): predecessor J2796 is complete (7060b03eb5), J2798-fixture-exact-v2 (done=0: / idle 1533.8 B/min, /tracker idle 1803.5 B/min) and J2798-live-current (done=0) are complete, and 47 Python + JS tests pass on PR #924 (680ed3ace1). Reopened J2798 to clear the synthetic dependency hold for PR #924 rollout and post-deploy 10-minute live measurement. GBP 0." \
  --git
```

### Option B (If keeping `J2798` held while Chief merges & deploys PR #924 directly)

```bash
python3 scripts/jobs.py wait J2798 --agent <chief_agent> \
  --condition "Verified at 2026-11-14T09:03Z (J2818, jobs/reviews/J2818/REVIEW.md): predecessor J2796 is complete, and detached captures J2798-fixture-exact-v2 (done=0, PASS: / idle 15338 B, 1-change 25450 B; /tracker idle 18035 B, 1-change 8020 B) and J2798-live-current (done=0, pre-deploy live: / 201892.3 B/min, /tracker 2089.8 B/min) are complete. Remaining before J2798 completion: Chief review/merge/deploy of PR #924 (680ed3ace1; see rawEtag/<= skew guard in jobs/reviews/J2818/REVIEW.md) and a fresh post-deploy 10-minute production capture under 20000 B/min on both / and /tracker." \
  --check-at "2026-11-14T14:39:35Z" \
  --type input \
  --recheck J2818 \
  --action "Chief review and deploy PR 924, then measure ten minutes of corrected production traffic" \
  --git

python3 scripts/jobs.py done J2818 --agent <chief_agent> \
  --result "Verified J2798 condition at 2026-11-14T09:03Z (jobs/reviews/J2818/REVIEW.md): predecessor J2796 complete; J2798-fixture-exact-v2 (done=0, PASS) and J2798-live-current (done=0) complete; PR #924 (680ed3ace1) awaits Chief review/merge/deploy and post-deploy 10-minute production capture <20000 B/min. Recorded updated hold on J2798 with --recheck J2818. GBP 0." \
  --git
```
