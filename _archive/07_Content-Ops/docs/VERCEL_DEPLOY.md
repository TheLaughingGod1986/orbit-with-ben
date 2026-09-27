# Deploy Content Ops on Vercel (Postgres)

Public host for the affiliate landing **`/go`** (Amazon Associates website URL), `/go/{slug}` redirects, and click persistence. Production: `https://orbit-content-ops.vercel.app` (Vercel project `orbit-content-ops`, root directory `07_Content-Ops`). Do **not** use `orbitwithben.com` for Associates. SQLite file DB is **not** the production path.

## Vercel project setup

1. Import this monorepo into Vercel.
2. Set **Root Directory** to `07_Content-Ops` (Project Settings → General).
3. Framework Preset: Next.js (auto-detected).
4. Build Command (default from `package.json`):  
   `prisma generate && node scripts/prisma-migrate-deploy.mjs && next build`  
   Migrate resolves `DIRECT_URL` from Neon `DATABASE_URL_UNPOOLED` / `POSTGRES_URL_NON_POOLING` first, retries P1002, then retries with `PRISMA_SCHEMA_DISABLE_ADVISORY_LOCK=1` (Neon serverless).  
   Do **not** use `prisma migrate dev` in CI/build — it hangs waiting for input.
5. Install Command: `npm install` (runs `postinstall` → `prisma generate`).

No repo-root `vercel.json` is required; keep other folders out of this project’s root.

## Environment variables

Set these on the Vercel project for **Production** and **Preview**:

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | Pooled Postgres URL for the app (Neon pooler, Supabase pooler, Vercel Postgres, etc.) |
| `DATABASE_URL_UNPOOLED` / `POSTGRES_URL_NON_POOLING` | Neon integration non-pooled URLs. Prefer these for migrate (build script picks them automatically). |
| `DIRECT_URL` | Optional manual non-pooled URL. Used when Neon unpooled vars are absent. May equal `DATABASE_URL` if there is no pooler. |
| `APP_BASE_URL` | Public origin of this deploy, e.g. `https://YOUR-PROJECT.vercel.app` |
| `AMAZON_ASSOCIATE_TAG` | Set in the Vercel dashboard only (Production + Preview), e.g. the live Associates tag. Never commit the value. `/go` stamps `tag=` from this env at redirect time. |
| `AFFILIATE_REDIRECT_BASE_URL` | Optional. Defaults to `${APP_BASE_URL}/go`. |
| `ORBIT_TOKEN_ENCRYPTION_KEY` | Required in production for OAuth token encryption (see `.env.example`). |

Copy the rest of OAuth / publishing keys from `.env.example` as needed.

## After first deploy

Migrations run automatically during the Vercel build (`prisma migrate deploy`). Then seed and apply live Amazon destination URLs against the **hosted** DB (use your project’s env, not a fictional host):

```bash
cd 07_Content-Ops
# Point at the same DATABASE_URL / DIRECT_URL as the Vercel project
export DATABASE_URL="…"
export DIRECT_URL="…"   # or same as DATABASE_URL
npm run db:seed
npm run affiliate:apply-urls
```

Confirm `APP_BASE_URL/go` returns **HTTP 200** HTML (Associates crawl), `/go/{product-slug}` redirects with `tag=` from env, and `AffiliateClick` rows appear in Postgres.

## Local development

Local still uses **Postgres** (local Docker Postgres, Neon, etc.):

```bash
cd 07_Content-Ops
cp .env.example .env
# Set DATABASE_URL + DIRECT_URL (DIRECT_URL may equal DATABASE_URL for non-pooled local Postgres)
npm install
npx prisma migrate deploy   # or: npm run db:migrate
npm run db:seed
npm run dev
```

`npm run db:migrate` remains `prisma migrate dev` for local schema work. Production / Vercel always uses `prisma migrate deploy`.

## Notes

- Prisma provider is `postgresql` with `url = env("DATABASE_URL")` and `directUrl = env("DIRECT_URL")` (build fills `DIRECT_URL` from Neon unpooled env when present).
- The Prisma client is cached on `globalThis` for Vercel serverless.
- Affiliate Amazon `tag=` is stamped only from `AMAZON_ASSOCIATE_TAG` at redirect time — never hard-coded in source or seed.
