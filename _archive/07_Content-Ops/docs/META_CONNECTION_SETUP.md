# Meta Connection Setup (Instagram + Facebook Reels)

**Docs checked:** 2026-08-01 — Instagram Content Publishing + Facebook Page Reels APIs.

## Developer portal

1. Create an app at [Meta for Developers](https://developers.facebook.com/)
2. Add **Facebook Login** (and Instagram Graph / Content Publishing products as required)
3. Valid OAuth redirect:
   `http://localhost:3000/api/oauth/meta/callback`
4. Request permissions (App Review for live users beyond app roles):
   - `pages_show_list`
   - `pages_read_engagement`
   - `pages_manage_posts` (as required for Page Reels)
   - `instagram_basic`
   - `instagram_content_publish`
   - `business_management` (if needed for Page discovery)

## Account requirements

- A Facebook user who can **manage** at least one Page
- Instagram **professional** account linked to that Page
- Personal IG accounts cannot be API-published

## Environment

```env
META_APP_ID=
META_APP_SECRET=
META_REDIRECT_URI=http://localhost:3000/api/oauth/meta/callback
ORBIT_TOKEN_ENCRYPTION_KEY=
```

## Connect flow

1. Connect via `/settings/connections` → Meta OAuth
2. System lists manageable Pages (stored in connection `metadataJson`)
3. Select Page + linked Instagram professional account
4. Validate permissions

Missing Page → `requires_attention`  
Missing IG pro → Instagram capabilities stay manual

## Publishing

### Instagram Reels

Resumable upload (local file → container → poll → `media_publish`) is preferred.
Public `video_url` staging remains supported when `MEDIA_STAGING_MODE=existing_public_url`.

### Facebook Page Reels

`/{page-id}/video_reels` start → binary upload → finish (`video_state=PUBLISHED`).
Publish only to the selected Page. Personal profiles are not used.

## Brand shorts auto-post (TikTok-style mirror)

When a YouTube Short goes live, Orbit can also mirror to IG + Facebook:

→ `00_Brand/Channel-Setup/Meta/AUTO_POST.md`  
→ `00_Brand/Channel-Setup/Meta/CONNECT_TO_CONTENT_OPS.md`

Copy Page / IG ids + tokens into `META_CREDENTIALS.json` (gitignored), or use Meta
Business Suite CDP on port 9223 until App Review is complete.

## Safe test

Prefer the safest visibility Meta allows for your app mode. Confirm before any public feed post. Record genuine media IDs only after API success.

## Manual fallback

Always available via export packages when App Review or staging is incomplete.
