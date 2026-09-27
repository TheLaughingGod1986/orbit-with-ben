# Autopublish Implementation Plan

**Date:** 2026-07-31  
**Scope:** `07_Content-Ops/` only  
**Status:** Active implementation plan

---

## Audit summary

Content Ops v1 is a strong **manual** distribution studio:

| Area | Current state |
|------|---------------|
| Adapters | `PublishingAdapter` in `src/lib/publishing/adapters.ts` — all manual placeholders |
| Schema | `PlatformPost`, `PlatformSettings` — no connections/jobs |
| Settings UI | `/settings` edits metadata; no OAuth |
| Schedule | `scheduledAt` stored; **no worker consumes it** |
| Duplicates | `detectDuplicates` on schedule/publish status change |
| Export | Manual upload packages under `content/exports/` |
| Status | Clip + post transition tables in `status.ts` |
| Env | `.env.example` incomplete vs adapter checks |
| Tests | 14 unit tests; no OAuth/worker/API publish coverage |

**Conclusion:** Extend, do not rebuild. Keep manual fallback. Never fake publish success.

---

## Design principles

1. Official OAuth + official APIs only.
2. Encrypt tokens at rest (AES-256-GCM).
3. Publish only after genuine platform confirmation + external ID.
4. Local worker required for schedule reliability — surface worker health honestly.
5. Capabilities derived from scopes + approval + account type — not from adapter existence.
6. Dry-run never hits publish endpoints.
7. Manual fallback always available.

---

## Phase 1 — Shared architecture + YouTube

### Schema

Add:

- `PlatformConnection`
- `PublishingJob`
- `PublishingAttempt`
- `OAuthState`
- `WorkerHeartbeat`
- Optional: `AppSetting` keys for `publishing_mode`, `dry_run`

### Shared modules

```
src/lib/security/token-crypto.ts
src/lib/oauth/state.ts
src/lib/oauth/providers/{google,meta,tiktok,x,threads}.ts
src/lib/env.ts
src/lib/publishing/types.ts          # extended adapter interface
src/lib/publishing/errors.ts
src/lib/publishing/idempotency.ts
src/lib/publishing/jobs.ts
src/lib/publishing/media/ffprobe.ts
src/lib/publishing/media/staging.ts
src/lib/publishing/adapters/*        # one file per platform
src/workers/publishing-worker.ts
```

### YouTube

- Google OAuth web-server flow
- Scopes: `youtube.upload` + `youtube.readonly` (channel identity)
- Resumable `videos.insert`
- Default test privacy: `private`
- Require explicit `privacyStatus` + `madeForKids`
- Record video ID + URL only after API success

### UI

- `/settings/connections`
- Job detail `/publishing/[jobId]`
- Worker health on overview
- Dry-run banner

### Validation

- Mocked OAuth/state/crypto/worker/YouTube tests
- Optional `RUN_YOUTUBE_INTEGRATION_TESTS=false`

---

## Phase 2 — Meta (Instagram + Facebook)

- Facebook Login OAuth
- Page discovery + IG professional account discovery
- Instagram Reels: container → poll → publish (resumable preferred for local files)
- Facebook Page Reels via official Page endpoints
- Media staging provider when public URL required
- Clear errors for missing Page / non-professional IG

---

## Phase 3 — TikTok

- Login Kit OAuth + PKCE
- **Draft** (`video.upload` / inbox init) → `manual_action_required`
- **Direct Post** (`video.publish`) only when configured + scoped
- Creator info query before direct post
- Never equate draft with published

---

## Phase 4 — X

- OAuth 2.0 PKCE (`tweet.write`, `users.read`, `offline.access`)
- Access-plan / capability gate before enabling publish
- Text post + media upload (INIT/APPEND/FINALIZE) when plan allows
- Warn when plan lacks posting/media

---

## Phase 5 — Threads

- Document feasibility (official Threads API exists at `graph.threads.net`)
- Implement adapter if Meta Threads product + scopes available
- Otherwise keep manual export + `canPublishDirectly: false`

---

## Non-goals

- Browser automation / password storage
- Third-party publisher SaaS (unless explicitly configured later)
- Claiming cloud-grade scheduling reliability on a sleeping laptop
- Public test publishes without confirmation

---

## Rollout commands (after implementation)

```bash
cd 07_Content-Ops
cp .env.example .env   # fill secrets + ORBIT_TOKEN_ENCRYPTION_KEY
npx prisma migrate dev
npm run db:seed
npm run dev:all        # Next + worker
npm test && npm run typecheck && npm run lint && npm run build
```
