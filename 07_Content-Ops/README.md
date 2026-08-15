# Orbit Content Ops

Local multi-platform distribution + autopublish dashboard for **Orbit with Ben**.

## Quick start

```bash
cp .env.example .env
# set ORBIT_TOKEN_ENCRYPTION_KEY=$(openssl rand -base64 32)
npm install
npx prisma migrate dev
npm run db:seed
npm run dev:all
```

Open http://localhost:3000 — connect accounts at `/settings/connections`.

## Scripts

| Command | Purpose |
|---------|---------|
| `npm run dev` | Dashboard only |
| `npm run worker` | Publishing worker |
| `npm run dev:all` | Dashboard + worker |
| `npm test` | Vitest suite |
| `npm run typecheck` | TypeScript |
| `npm run connections:validate` | Re-validate OAuth connections |
| `npm run publishing:reconcile` | Reconcile ambiguous jobs |
| `npm run db:seed` | Seed aliens episode + 4 clips |
| `npm run youtube:package` | YouTube Data API package upload |
| `npm run review:script -- --file <script.md>` | Growth System v2 script reviewer (≥90 to pass) |
| `npm run diagnose:youtube -- --file <metrics.json>` | Post-upload YouTube growth recommendations |
| `npm run gate:episode -- --project <…>` | Growth System v2 episode gate (blocks VO/Veo until PASS) |
| `npm run brief:next -- --file metrics.json` | Write `docs/NEXT_EPISODE_BRIEF.md` from diagnostics |
| `npm run verify:growth-v2` | Growth + episode-ops tests + sample diagnose + brief |

### Growth System v2 — first-time setup

```bash
cd 07_Content-Ops
cp -n .env.example .env   # set ORBIT_TOKEN_ENCRYPTION_KEY if empty
npx prisma migrate deploy
npx prisma generate
npm run verify:growth-v2
npm run gate:episode -- --project ../02_Video-Projects/_template_NNN_Episode-Slug
# (template draft should BLOCK until audit signed + strong script)
npm run brief:next -- --file content/samples/json/youtube_growth_metrics_sample.json
npm run dev               # open /analytics to import Studio CSV
```

New episodes: copy `02_Video-Projects/_template_NNN_Episode-Slug/`.

## Autopublish notes

- Official OAuth/APIs only; tokens encrypted at rest (AES-256-GCM)
- Posts are marked `published` only after a genuine platform ID/URL
- Local scheduling requires the worker process — not cloud-reliable
- Default `PUBLISHING_DRY_RUN=true` in `.env.example`
- Setup: `docs/ACCOUNT_CONNECTION_SETUP.md` and platform guides under `docs/`

## Affiliate monetisation

Integrated affiliate programmes, products, video matching, `/go/{slug}` click tracking, description blocks, CSV conversion import, and opportunity scoring.

- Docs: `docs/AFFILIATE_MONETISATION_SYSTEM.md` · go-live: `docs/AFFILIATE_GO_LIVE.md`
- UI: `/affiliate` · `/affiliate/products` · `/affiliate/programs` · `/affiliate/opportunities`
- Env: `AMAZON_ASSOCIATE_TAG`, `BRILLIANT_AFFILIATE_ID`, `AFFILIATE_REDIRECT_BASE_URL`
- CLI: `npm run affiliate:apply-urls` · `npm run affiliate:verify`
- Philosophy: relevance before revenue — card ≤4 candidates; description Auditor-capped

## Scope

- Does not replace video production under `02_Video-Projects/`
- Never commit secrets; use `.env`
