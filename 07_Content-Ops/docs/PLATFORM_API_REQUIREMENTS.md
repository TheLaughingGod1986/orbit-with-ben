# Platform API Requirements

**Documented:** 2026-07-31  
**Purpose:** Official references and constraints for Orbit Content Ops autopublishing.  
**Rule:** Re-check developer portals before production enablement — scopes and review rules change.

---

## YouTube (Google)

| Item | Value |
|------|-------|
| Auth | OAuth 2.0 web server flow |
| Docs | https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps |
| Upload | https://developers.google.com/youtube/v3/guides/uploading_a_video |
| Resumable | https://developers.google.com/youtube/v3/guides/using_resumable_upload_protocol |
| Insert | https://developers.google.com/youtube/v3/docs/videos/insert |
| Schedule | `status.publishAt` + `privacyStatus` private/unlisted on insert |
| Thumbnails | https://developers.google.com/youtube/v3/docs/thumbnails/set |
| Minimum scopes | `youtube.upload`, `youtube.readonly`, `youtube.force-ssl` (comments + playlists) |
| Upload type | Resumable `videos.insert` |
| Package CLI | `npm run youtube:package` — see [YOUTUBE_PACKAGE_UPLOAD.md](./YOUTUBE_PACKAGE_UPLOAD.md) |
| Test default privacy | `private` |
| Orbit default path | **Data API package** (`youtube:package` / `youtube:upload` / publishing worker) |
| Studio finish only | Title/thumb ABC · pin comment (**long-form**) · Shorts Related pill (**no new Short pins**) · end screens/cards |
| Fallback | Studio CDP only for those gaps or if OAuth/API unavailable |
| Notes | Do not use a service account for a normal channel. Require explicit `privacyStatus` and `madeForKids`. Upload scheduled videos immediately with `publishAt` — do not wait until air time on the local worker. Reconnect OAuth after adding `force-ssl`. |

---

## Meta — Instagram Reels + Facebook Page Reels

| Item | Value |
|------|-------|
| Auth | Facebook Login / Facebook Login for Business |
| IG publishing | https://developers.facebook.com/docs/instagram-platform/content-publishing |
| IG media | https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media/ |
| Flow | Create container → poll `status_code` → `media_publish` |
| Account type | Instagram **professional** account linked to a Facebook Page |
| Media | Public `video_url` **or** resumable upload (`upload_type=resumable`) |
| Review | `instagram_content_publish` / related permissions typically require App Review |
| FB Reels | Publish to a **Page**, not a personal profile |

---

## TikTok

| Item | Value |
|------|-------|
| Getting started | https://developers.tiktok.com/doc/content-posting-api-get-started |
| Direct Post | https://developers.tiktok.com/doc/content-posting-api-reference-direct-post |
| Upload to Inbox (draft) | https://developers.tiktok.com/doc/content-posting-api-reference-upload-video |
| Guidelines | https://developers.tiktok.com/doc/content-sharing-guidelines |
| Draft scope | `video.upload` → inbox init — **not published** |
| Direct scope | `video.publish` — requires Direct Post config + approval |
| Unaudited clients | Direct posts restricted to `SELF_ONLY` / private viewing |
| Rule | Never mark draft uploads as `published` |

---

## X

| Item | Value |
|------|-------|
| Auth | OAuth 2.0 with PKCE preferred (`tweet.read tweet.write users.read offline.access`) |
| Create post | `POST https://api.x.com/2/tweets` |
| Media | Chunked upload INIT / APPEND / FINALIZE (verify current upload host in portal docs) |
| Access | New apps typically pay-per-use (2026); posting fails without eligible write access |
| Gate | Disable publish capability when plan/endpoints unavailable |

---

## Threads

| Item | Value |
|------|-------|
| Official API | Yes — Threads Graph API (`graph.threads.net`) |
| Docs | https://developers.facebook.com/docs/threads/posts/ |
| Publishing ref | https://developers.facebook.com/documentation/threads/reference/publishing |
| Flow | Create container → `threads_publish` |
| Scopes | `threads_basic`, `threads_content_publish` (confirm in Meta portal) |
| Practicality | Requires Meta app + Threads product / verification; treat as optional until connected |
| Fallback | Manual export remains if app not approved |

---

## Shared Orbit constraints

- Tokens encrypted with `ORBIT_TOKEN_ENCRYPTION_KEY` (AES-256-GCM).
- Local worker must be running for scheduled publish.
- Dry-run (`PUBLISHING_DRY_RUN=true`) never creates external posts.
- Manual export packages always available.
