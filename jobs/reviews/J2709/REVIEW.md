# J2709 Condition Verification Review — J2704 (`HOS tooling: validate Next upgrade in preview and diagnose home page error`)

- **Verification Job:** `J2709` (`recheck_of: J2704`)
- **Parent Job:** `J2704` (`HOS tooling: validate Next upgrade in preview and diagnose home page error`, `needs: mini`, `repo: hos`, `kind: assembly`, `by: codex`, `status: blocked`, `step 2 of 3`, `ref: 6813294950`)
- **Verified By:** `macbook-2` (`gemini-argon`)
- **Verified At:** `2026-11-12T14:38:41Z`
- **Verdict:** **CONDITION NOT YET SATISFIED (`HOLD / WAIT`) — Keep `J2704` blocked at step 2 of 3 (`Production remains HELD`). Local Next 16.4.6 validation on HOS `main` (`2f8835325b5c634f9b421456e6b6f12bf90fec33`) against a fresh isolated loopback PostgreSQL 17 database (`j2704_disposable`) is complete and documented in open HOS PR `#569` (`7420a24bd9f3a09b51cd3a1f077e9a47b0f7a4de`), and the public home-page `500` root cause is proven (`PrismaClientInitializationError: Environment variable not found: DATABASE_URL` in `schema.prisma:7`). However, the hosted Vercel Preview prerequisite job `J2708` (*"HOS app: establish isolated hosted PostgreSQL for Preview validation"*, added `2026-11-12T14:29Z`) is still `open` and unclaimed, so no isolated hosted PostgreSQL endpoint, Preview-scoped environment configuration, or Vercel Preview deployment / smoke check exists yet. Recommended next check: `2026-11-12T20:30:00Z` (+6 h, or earlier when `J2708` completes). Zero spend (`£0.00`), no uploads, deployments, or schedule changes.**

---

## 1. Original Job, Chief Ruling & Recorded Waiting Condition

1. **Chief Ruling (`#6813294950` on `orbit-with-ben #478`, `2026-11-12T03:14:38Z`, owner-authored by `TheLaughingGod1986`):**
   - Squash-merged `orbit-with-ben #841` (`39e03469`, dev-only `minimatch` override) and `history-of-science #558` (`e67c54f7`, `next` 15.5 -> 16.4.6).
   - Ruled **Deploy of HOS `07_Content-Ops`: not yet.** Required running full `npm run build` (`prisma generate && prisma migrate deploy && next build`) against a non-live database, deploying a Vercel **Preview** (never `--prod`), checking `/login` and an operator-gated route there without triggering publishing, and diagnosing the pre-existing public home-page `500`. Production deployment remains held until Preview passes and Chief explicitly authorizes `vercel --prod`.

2. **Recorded Hold on `J2704` (`2026-11-12T14:30Z`, `step 2 of 3` by `codex`):**
   - **Condition:** `Dependency J2708: establish isolated hosted PostgreSQL and safe HOS Preview configuration; then complete hosted build and auth/home smoke checks. Evidence HOS PR569. Production remains HELD.`
   - **Remaining Action:** `Complete hosted Preview validation after the isolated database setup`
   - **Why `J2709` triggered immediately at `14:30Z`:** `J2704` retained `"after": "J2483"` (`done`) when `codex` blocked it with `hold.type = "dependency"` and `last_recheck` unset, causing `workflow_state.hold_due()` (`hold.type == "dependency" and not hold.get("last_recheck") and by_id[j["after"]].status == "done"`) to evaluate `True` immediately. Recording `wait J2704 --recheck J2709` sets `last_recheck: "J2709"` so future checks wait until `check_at`.

---

## 2. Direct Verification Evidence (`2026-11-12T14:38Z`)

1. **Local Next 16 Validation & Home `500` Root Cause (`HOS PR #569`, head `7420a24bd9f3a09b51cd3a1f077e9a47b0f7a4de`, `OPEN` — `VERIFIED`):**
   - Checked `codex/j2704-evidence` (`docs/validation/J2704/{REVIEW.md,build.txt,typecheck.txt,lint.txt,tests.txt,check-all.txt,login.json,smoke.json}`) testing HOS `main` commit `2f8835325b5c634f9b421456e6b6f12bf90fec33` against a fresh loopback-only PostgreSQL 17 cluster (`j2704_disposable` on port `55474`, `DATABASE_URL` and `DIRECT_URL` verified identical and isolated, `PUBLISHING_DRY_RUN=true`, disposable secrets, zero live data/credentials):
     - `npm run build`: exit `0` (Prisma client generation + initial migration + Next `16.4.6` production build).
     - `npm run typecheck`: exit `0` (`tsc --noEmit`).
     - `npm run lint`: exit `0` (`eslint src`).
     - `npm test`: exit `0` (`19 passed` test files, `199 passed` tests).
     - `bash 00_Brand/Channel-Setup/tools/check_all.sh`: exit `0` (`ALL CHECKS PASS`).
     - Local production server smoke checks (`login.json`, `smoke.json`): `GET /` -> `200`, `GET /login` -> `200`, `GET /api/oauth/google/start` -> `307` to `/login?next=%2Fsettings%2Fconnections&error=Sign+in+as+operator+before+connecting+accounts`, unauthenticated operator `PATCH` -> `401`, authenticated operator `PATCH` (invalid body to prevent write) -> `400`, multipart password login -> `303` to `/` with session cookie issued, authenticated `GET /login` -> `307` to `/`.
   - **Root Cause of Public Home `500`:** Vercel runtime log (`2026-11-12T14:25:44.198Z`, production deployment `dpl_67ao5AXaWfQMehd3cyjGRNGWjdJF`) shows `PrismaClientInitializationError: Environment variable not found: DATABASE_URL` in `schema.prisma:7` on `longFormVideo.count()`. Read-only HTTP probe at `2026-11-12T14:38:41Z` confirms `https://history-of-science-content-ops.vercel.app/` returns `HTTP 500` and `/login` returns `HTTP 200` (Production untouched).

2. **Hosted Preview Prerequisite (`J2708`) — NOT YET COMPLETED (`UNMET`):**
   - Vercel project `history-of-science-content-ops` (`team_UPErYpfb3ww71LYTIWUoKvcH`) currently has **no Preview environment variables** configured.
   - Dependency job **`J2708`** (*"HOS app: establish isolated hosted PostgreSQL for Preview validation"*, `needs: mini`, `repo: hos`, `kind: assembly`, `ref: J2704`, added `2026-11-12T14:29Z`) is still **`open`** (unclaimed, `by: ""`, `result: ""`).
   - Consequently, no isolated hosted PostgreSQL database or safe Preview-scoped configuration has been provisioned yet, and step 3 of `J2704` (hosted Vercel Preview build + login/denial/authenticated smoke checks) cannot run yet.

---

## 3. Queue Update & Next Check (`2026-11-12T20:30:00Z`)

- Keep `J2704` `blocked` at `step 2 of 3` (`Complete hosted Preview validation after the isolated database setup`), with Production deployment **HELD**.
- Because `macbook-2` is neither the job holder (`codex`) nor the elected Chief (`codex`), `scripts/jobs.py` restricts `wait J2704 --recheck J2709` to `codex`. Elected Chief (`codex`) please run:

```bash
python3 scripts/jobs.py wait J2704 --agent codex \
  --condition "Dependency J2708 (open): establish isolated hosted PostgreSQL and safe HOS Preview configuration; then complete hosted build and auth/home smoke checks. Local build/migration, 199 tests, check_all, local auth smoke checks, and home-500 root cause (missing DATABASE_URL in Production) are documented in HOS PR #569 (7420a24b). Production remains HELD." \
  --check-at "2026-11-12T20:30:00Z" \
  --type input \
  --recheck J2709 \
  --action "Complete hosted Preview validation after J2708 establishes the isolated hosted PostgreSQL database and safe Preview configuration" \
  --git
python3 scripts/jobs.py done J2709 --agent codex \
  --result "Verified at 2026-11-12T14:38Z (jobs/reviews/J2709/REVIEW.md): condition not yet met. Local Next 16 build/migration, 199 tests, check_all, local auth smoke checks, and home-500 root cause (missing DATABASE_URL) are verified in open HOS PR #569 (7420a24b), but prerequisite J2708 (isolated hosted PostgreSQL + safe Preview config) is still open/unclaimed. Production remains HELD; next check 2026-11-12T20:30:00Z." \
  --git
```
