# X Connection Setup

**Docs checked:** 2026-07-31 — X API v2 posting + media upload.

## Access plan gate

New X developer apps typically require a paid access plan for write endpoints. If the configured plan cannot create tweets or upload media, Orbit sets `canPublishDirectly=false` and shows:

> Your X API access plan does not include the required posting endpoint.

## Developer portal

1. Create a project/app at [X Developer Portal](https://developer.x.com/)
2. Enable OAuth 2.0 with PKCE
3. Callback: `http://localhost:3000/api/oauth/x/callback`
4. Scopes: `tweet.read tweet.write users.read offline.access` (confirm in portal)
5. Verify media upload endpoints available on your plan

## Environment

```env
X_CLIENT_ID=
X_CLIENT_SECRET=
X_REDIRECT_URI=http://localhost:3000/api/oauth/x/callback
```

## Connect & publish

1. Connect from `/settings/connections`
2. Validate user identity
3. Enqueue text or video posts only when capabilities allow
4. Store genuine tweet ID + URL after success

## Manual fallback

Always available. Prefer manual until write access is confirmed with a private/test post.
