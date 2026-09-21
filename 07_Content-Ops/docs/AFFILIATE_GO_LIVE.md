# Affiliate go-live

Code for the Affiliate Monetisation System is on `main`. This runbook is what remains to take tracked links live.

## What this repo can do for you

```bash
cd 07_Content-Ops
npx prisma migrate deploy
npm run affiliate:apply-urls    # write public destination URLs into the DB
npm run affiliate:verify        # readiness checklist (exit 1 if blocking fails)
npm run affiliate:verify -- --probe   # also HTTP-probe the /go base
```

Or in the dashboard: **Affiliate → Go-live readiness → Apply live destination URLs**.

API: `GET /api/affiliate/go-live` · `POST /api/affiliate/go-live` `{ "action": "apply-urls" }`

Destination URLs come from `src/lib/affiliate/live-product-urls.ts` (confirmed Amazon UK ASINs + Brilliant / FLO public pages; LEGO stays inactive until programme access). **Affiliate tags are never committed** — they are applied at `/go` redirect from env.

## What only you can do

1. **Amazon Associates UK** — approve account → set `AMAZON_ASSOCIATE_TAG` in production env (Vercel; never commit). Website URL for Associates: **`https://orbit-content-ops.vercel.app/go`** (public HTML landing — not a blank redirect). Do **not** use `orbitwithben.com`.
2. **Brilliant** — approve affiliate → set `BRILLIANT_AFFILIATE_ID`  
3. **Deploy Content Ops** with migrate + those env vars (Vercel project `orbit-content-ops`, root `07_Content-Ops`)  
4. Confirm **`https://orbit-content-ops.vercel.app/go` returns HTTP 200** with real HTML, and `/go/{slug}` still 302s  
5. **Smoke-test** `https://orbit-content-ops.vercel.app/go/jwst-book` → 302 → Amazon.co.uk with `tag=` from env · click row appears  
6. On a long-form video: regenerate → approve trust-gated placement → publish description with `/go/` links  
7. When reports exist: CSV import on `/affiliate/import`

## Env (production)

```bash
APP_BASE_URL=https://orbit-content-ops.vercel.app
# Optional; defaults to ${APP_BASE_URL}/go
AFFILIATE_REDIRECT_BASE_URL=https://orbit-content-ops.vercel.app/go
AMAZON_ASSOCIATE_TAG=<uk-tag>   # e.g. orbitgo-21 — set in Vercel only
BRILLIANT_AFFILIATE_ID=<brilliant-id>
```

Never commit real IDs. Prefer host secrets / Cursor environment secrets.

## After first film

- Goals clock starts on first approved placement (or first click if earlier)  
- Keep Amazon destinations on confirmed `amazon.co.uk` ASINs only (no search/category placeholders)  
- Keep LEGO programme inactive until Affiliate access exists  
- Shorts stay zero affiliate description links  

Canonical system doc: `docs/AFFILIATE_MONETISATION_SYSTEM.md`
