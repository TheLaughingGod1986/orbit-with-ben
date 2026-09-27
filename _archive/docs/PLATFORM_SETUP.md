# Platform setup

## Local app

```bash
cd 07_Content-Ops
cp .env.example .env
npm install
npx prisma migrate dev
npm run db:seed
npm run dev
```

Open http://localhost:3000

## Environment variables

Secrets never belong in Git or the browser.

```
DATABASE_URL="file:./dev.db"
# Optional future:
# YOUTUBE_CLIENT_ID=
# YOUTUBE_CLIENT_SECRET=
# TIKTOK_CLIENT_KEY=
# TIKTOK_CLIENT_SECRET=
# META_ACCESS_TOKEN=
# X_API_KEY=
# X_API_SECRET=
# X_ACCESS_TOKEN=
# X_ACCESS_SECRET=
```

## Connection status meanings

| Status | Meaning |
|--------|---------|
| manual_upload_required | Default v1 path |
| api_available | Credentials detected; publish still not auto-wired |
| api_unavailable | Credentials exist but unrestricted publish is not assumed |
| authentication_expired | Reserved for future OAuth refresh failures |

## Enabled platforms

Configure per-platform toggles, default hashtags, CTA, posting method, and visibility on **Settings**.
