# OAuth repair — Orbit YouTube (`youtube.force-ssl`)

**Date:** 2026-08-07  
**Command:** `cd 07_Content-Ops && npm run youtube:verify-oauth`

## Scope configuration (code)

`YOUTUBE_SCOPES` / `REQUIRED_YOUTUBE_SCOPES` already request:

- `youtube.upload`
- `youtube.readonly`
- `youtube.force-ssl`

OAuth start: `/api/oauth/google/start`  
OAuth callback now stores **actual** scopes returned by Google (`tokenBody.scope`), not an assumed list.

## Before

Stored connection scopes (pre-reconnect): `youtube.upload` + `youtube.readonly` only.  
`videos.update` → **403 ACCESS_TOKEN_SCOPE_INSUFFICIENT**.

## After (this task)

| Item | Status |
|------|--------|
| Code requests `force-ssl` | PASS |
| Callback persists real granted scopes | PASS |
| `npm run youtube:verify-oauth` | Detects missing scope / prints reconnect guidance |
| Live `videos.update` | **Blocked until manual reconnect** |

## Reconnect workflow (user)

1. Start Content Ops: `cd 07_Content-Ops && npm run dev`
2. Open `/settings/connections`
3. Disconnect/reconnect YouTube (consent screen must show force-ssl)
4. Or: `npm run youtube:verify-oauth -- --print-auth-url` then complete consent via the app’s OAuth start route (preferred for CSRF state)
5. Re-run: `npm run youtube:verify-oauth`
6. Expect:
   - `PASS: youtube.force-ssl granted`
   - `PASS: videos.update permitted`
   - `PASS: video state unchanged` (safe same-value update on `3xrxdmaOwJI`)

## Failure kinds

| Kind | Meaning | Remediation |
|------|---------|-------------|
| `missing_scope` | Token lacks force-ssl | Reconnect with consent |
| `expired_token` | Access/refresh expired | Reconnect |
| `revoked_token` | User revoked app | Reconnect |
| `invalid_client` | Bad client id/secret | Fix `.env` |
| `no_connection` | No DB row | Connect first |

Tokens are never printed or committed.
