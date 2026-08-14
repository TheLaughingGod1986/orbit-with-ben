# AGENTS.md

Orbit is a YouTube production workspace (mostly assets, prompts, and docs). The
one runnable application is the **Content Ops dashboard** in `07_Content-Ops/`
(a Next.js 15 app with Prisma + SQLite). See `README.md` and
`07_Content-Ops/README.md` for the product overview and full script list.

## Cursor Cloud specific instructions

### Runnable service: `07_Content-Ops` (Next.js dashboard)

- Stack: Next.js 15 (App Router, Turbopack) + React 19 + Prisma 6 on **SQLite**
  (file DB, no external database/service needed). Node 22, npm (uses
  `package-lock.json`).
- The update script runs `npm install` + `npx prisma generate` in
  `07_Content-Ops/` on every VM startup, so JS deps and the Prisma client are
  already refreshed. It intentionally does **not** create `.env`, run
  migrations, or seed.
- **First-run bootstrap** (needed once per fresh VM before the app can talk to
  the DB — `.env` and the SQLite file are git-ignored):
  ```bash
  cd 07_Content-Ops
  cp -n .env.example .env          # provides DATABASE_URL="file:./dev.db"
  # optional; only OAuth token encryption needs it (not the dev server):
  #   set ORBIT_TOKEN_ENCRYPTION_KEY=$(openssl rand -base64 32) in .env
  npx prisma migrate deploy        # apply migrations to dev.db
  npm run db:seed                  # load the "aliens" fixture episode + clips
  npm run dev                      # http://localhost:3000
  ```
- `ORBIT_TOKEN_ENCRYPTION_KEY` is **optional** in dev (only enforced in
  production, and only used by the OAuth `connect accounts` flows). The
  dashboard and the core "Create Distribution Pack" feature run without it.
- `npm run db:seed` is **destructive**: it wipes all tables and reloads the
  fixture. Do not run it against data you want to keep.
- Standard commands (see `07_Content-Ops/package.json` / `README.md`):
  `npm run dev` (dashboard), `npm run dev:all` (dashboard + publishing worker),
  `npm run lint`, `npm run typecheck`, `npm test` (vitest).

### Known pre-existing breakage (not an environment problem)

- Several `scripts/youtube-*.ts` and the `tests/youtube-recovery.test.ts` suite
  import `src/lib/publishing/youtube-freeze`, which does **not** exist on this
  base branch. This makes `npm run typecheck` fail and one vitest suite fail to
  import. It is unrelated to environment setup — the other **85 tests pass** and
  `npm run lint` is clean. The missing module is never imported by `src/app`, so
  the dev server and the dashboard are unaffected. Do not "fix" this as part of
  environment setup.

### Out of scope for the dev app: `04_Audio/tools` Python CLIs

- The Python tools (VO via ElevenLabs, CG via Google Flow/Veo Playwright,
  captions, SFX) require external API keys and/or a logged-in Playwright profile
  and paid credits. They are not part of running/testing the dashboard and are
  not exercised by the standard dev setup.
