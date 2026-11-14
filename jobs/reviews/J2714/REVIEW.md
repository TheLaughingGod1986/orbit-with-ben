# Chief Review: J2714 (Move the Studio board from Vercel to Cloudflare Pages)

- **Reviewer:** `gemini` (elected acting Chief)
- **Date:** 2026-11-14
- **Verdict:** **PASS on PR #925 (merged as `71be7cfcb8`) — REOPEN `J2714` for Mini `cursor`**

## Context & Evidence Reviewed
1. **Approvals:** Ben's approvals are recorded in `J2714` (`2026-11-12T16:42Z` migration request at £0; `2026-11-12T16:56Z` Wrangler CLI login; `2026-11-12T23:50Z` settings transfer approval; `2026-11-14T11:34Z` confirmation that `BOARD_GH_TOKEN` is added to Cloudflare Pages `studio-kanban` production secrets).
2. **Block Reason (`macbook-2`, `2026-11-14T12:38Z`):** When `J2714` (`needs: mini`, `kind: studio`, `for: cursor`) was rerouted to `cursor`, MacBook Studio worker `macbook-2` claimed it because `macbook_studio_ok` treated `kind: studio` jobs as portable when Studio CDP ports were open. Because Wrangler login and local `studio-kanban` keys (`BOARD_KEY`) live only on the Mini, `macbook-2` could not run the 11:34Z Cloudflare Pages secret check, production deploy, tick check, or 30x `/api/data?f=ref` verification.
3. **Fix Verified & Merged (`PR #925`, `456b3656d` → `71be7cfcb8`):**
   - Adds `\bwrangler\b|\bcloudflare pages\b|\bpages (?:deploy|secret)\b|\bvercel env\b|` to `STUDIO_BLOCK` in `scripts/jobs.py` so Cloudflare Pages and Wrangler deployment tasks stay on the Mini while genuine Studio browser tasks remain portable.
   - Adds regression test `test_cloudflare_pages_and_wrangler_jobs_stay_on_the_mini_even_when_studio_cdp_is_up` in `scripts/test_jobs.py`.
   - Verified `Rules check` passed on PR #925 and all 76 unit tests in `scripts/test_jobs.py`, `scripts/test_no_private_network.py`, and `scripts/test_email_ratchet.py` pass on `main`.

## Ruling & Next Step
1. **Merged PR #925 (`71be7cfcb8`)** to `main` so MacBook Studio workers no longer claim `J2714`.
2. **Reopen `J2714` (`needs: mini`, `for: cursor`)** on the Mini to execute the 11:34Z checklist:
   - List `studio-kanban` production secret names only (`wrangler pages secret list`) and confirm `BOARD_GH_TOKEN` is present.
   - Build and deploy `studio-kanban` from `main` (`build.py`, then `wrangler pages deploy dist --project-name studio-kanban --branch main`).
   - Verify `/api/checks` answers 200, write and remove one test tick with `BOARD_KEY`, and verify 30x `/api/data?f=ref` over two minutes on both `studio-kanban.pages.dev` and `board.oppti.dev` answer 200.
   - Post plain-English phone-linking steps for Ben on `#99` (no keys or codes) and note that `J2797` and `J2532` can be checked.
