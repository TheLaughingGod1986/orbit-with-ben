# J2760 Condition Verification — J2714 (`Move the Studio board from Vercel to Cloudflare Pages on the free plan: same pages, same five routes, one address setting`)

- **Verification Job:** `J2760` (`Verify condition for J2714`)
- **Parent Job:** `J2714` (`Move the Studio board from Vercel to Cloudflare Pages on the free plan: same pages, same five routes, one address setting`, `status: blocked`, `by: codex`, `needs: mini`, `kind: studio`, `repo: owb`, `due: 2026-11-13T18:00:00Z`)
- **Verifier:** `gemini` (`Gemini 4 Argon (High)`, specialist worker on the Mini; `Grok Bot` is elected Chief)
- **Checked At:** `2026-11-13T06:15Z`
- **Verdict:** **NOT YET MET — KEEP `J2714` BLOCKED (`BOARD_GH_TOKEN` is still absent from Cloudflare Pages `studio-kanban` production secrets and from the Mini's local env file; `GET /api/checks?stamp=1` returns HTTP 500 `{"error":"BOARD_GH_TOKEN isn't set"}` and `GET /api/data?f=ref` returns HTTP 502 `{"error":"GitHub 403"}`; no reply from Ben on the studio thread since comment `#6839530655` at `2026-11-12T23:58:52Z`).**

---

## 1. Recorded Waiting Condition on `J2714`

```text
Vercel refuses protected secret export. Ben must create the board GitHub token and set BOARD_GH_TOKEN in Cloudflare Pages studio-kanban production secrets. Fallback board/upload keys are set; report at thread comment 6839530655.
```

---

## 2. Element-by-Element Verification (`2026-11-13T06:15Z`)

| Requirement / Dependency | Status | Evidence Checked |
|---|---|---|
| **1. `BOARD_GH_TOKEN` set in Cloudflare Pages `studio-kanban` production secrets (or provided locally by Ben)** | **NOT MET (`BOARD_GH_TOKEN` absent)** | - `npx wrangler pages secret list --project-name studio-kanban` (run at `06:14Z`) lists 7 encrypted production secrets (`BOARD_KEY`, `R2_ACCESS_KEY_ID`, `R2_ACCOUNT_ID`, `R2_PUBLIC_URL`, `R2_SECRET_ACCESS_KEY`, `WATCH_LINK_SECRET`, `WATCH_UPLOAD_KEY`). `BOARD_GH_TOKEN` is **not** present.<br>- Key-name inspection of `07_Content-Ops/.env` shows `['BOARD_KEY', 'WATCH_UPLOAD_KEY']` only (no `BOARD_GH_TOKEN`).<br>- Studio thread (`#478`) read through `#6845665493`: no message from Ben since Codex's Part B fallback report at `#6839530655` (`2026-11-12T23:58:52Z`). |
| **2. Live API endpoints requiring `BOARD_GH_TOKEN` (`/api/checks?stamp=1` and `/api/data?f=ref`)** | **NOT MET (HTTP 500 / HTTP 502)** | - `curl -sS -i "https://studio-kanban.pages.dev/api/checks?stamp=1"` at `06:15:18Z` returned `HTTP/2 500` with body `{"error":"BOARD_GH_TOKEN isn't set"}`.<br>- `curl -sS -i "https://studio-kanban.pages.dev/api/data?f=ref"` at `06:15:19Z` returned `HTTP/2 502` with body `{"error":"GitHub 403"}`. |
| **3. Part A static pages & Part B fallback secrets (`BOARD_KEY`, `WATCH_UPLOAD_KEY`)** | **SATISFIED (verified intact)** | - Live probes on `https://studio-kanban.pages.dev` at `06:19Z`: `/` (`HTTP 200`), `/tracker` (`HTTP 200`), `/ai` (`HTTP 200`), `/version.json` (`HTTP 200`).<br>- `BOARD_KEY` and `WATCH_UPLOAD_KEY` remain encrypted in Cloudflare Pages `studio-kanban` production secrets and present by key name in `07_Content-Ops/.env`.<br>- PR `#858` remains `OPEN` at `911a5c112090d62663a1e2a6cb9942ae0bb97eca`. |

---

## 3. Queue Action for Elected Chief (`chief` / Grok Bot)

Because `scripts/jobs.py` (`set_wait`, lines 517–530) restricts updating another worker's hold with `--recheck` to the elected Chief (`ValueError: Only the holder or elected Chief may update this hold` / `Only the elected Chief may record a condition check`), `J2760` is parked for the elected Chief (`chief`, or whichever Chief is elected on the next pass) to record the updated hold on `J2714` (six hours out at `2026-11-13T12:18:00Z`, before the `18:00:00Z` due time) and close `J2760`:

```bash
python3 scripts/jobs.py wait J2714 --agent chief \
  --condition "J2760 verification at 2026-11-13T06:15Z: unmet. Vercel refuses protected secret export, and BOARD_GH_TOKEN is still not set in Cloudflare Pages studio-kanban production secrets (wrangler pages secret list shows 7 secrets: BOARD_KEY, R2_*, WATCH_LINK_SECRET, WATCH_UPLOAD_KEY; /api/checks?stamp=1 answers HTTP 500 'BOARD_GH_TOKEN isn'\''t set'; /api/data?f=ref answers HTTP 502 'GitHub 403'). Fallback BOARD_KEY and WATCH_UPLOAD_KEY remain set. Ben must create the board GitHub token and paste it as BOARD_GH_TOKEN in Cloudflare Pages -> studio-kanban -> Settings -> Variables and Secrets -> Production (thread comment 6839530655)." \
  --check-at "2026-11-13T12:18:00Z" \
  --type input \
  --recheck J2760 \
  --action "Add the missing GitHub token, then verify board ticks and phone linking" \
  --git

python3 scripts/jobs.py done J2760 --agent chief \
  --result "Condition checked by Gemini (jobs/reviews/J2760/REVIEW.md): BOARD_GH_TOKEN is still absent from Cloudflare Pages studio-kanban production secrets (7 secrets listed by wrangler; /api/checks?stamp=1 HTTP 500 'BOARD_GH_TOKEN isn't set'; /api/data?f=ref HTTP 502 'GitHub 403'), and no reply from Ben has landed since comment 6839530655. Part A pages (/, /tracker, /ai, /version.json HTTP 200) and Part B fallback keys (BOARD_KEY, WATCH_UPLOAD_KEY) remain intact. J2714 stays held until 2026-11-13T12:18:00Z." \
  --git
```
