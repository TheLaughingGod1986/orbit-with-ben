# Threads Publishing Assessment

**Date:** 2026-07-31  
**Question:** Should Orbit Content Ops implement Threads autopublishing now?

## Official support

Yes — Meta provides an official **Threads API** (`graph.threads.net`) with:

- OAuth / login for Threads
- Container creation + `threads_publish`
- Docs: https://developers.facebook.com/docs/threads/posts/

## Practicality for this app

| Factor | Assessment |
|--------|------------|
| Official API | Available |
| Account type | Threads profile linked via Meta app + Threads product |
| App review | Likely required for production publishing scopes (`threads_basic`, `threads_content_publish`) |
| Local media | Same staging concerns as Instagram (public URL / upload constraints) |
| Orbit priority | Lower than YouTube / IG / TikTok for the short-form flywheel |

## Decision

**Implement adapter + capability gating; keep manual as default until credentials and product approval exist.**

- `ThreadsPublishingAdapter` is present
- `canPublishDirectly` is false until OAuth + scopes + successful validation
- Metadata generation, export packages, and calendar slots remain
- OAuth routes for Threads can be added when `THREADS_APP_ID` / `THREADS_APP_SECRET` are configured and product is enabled

## If not approved

Retain:

- Platform copy generation
- Export packages
- Manual publishing checklist
- `canPublishDirectly: false` with clear UI limitation text
