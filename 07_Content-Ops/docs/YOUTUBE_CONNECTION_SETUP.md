# YouTube Connection Setup

**Docs checked:** 2026-08-05 — see [PLATFORM_API_REQUIREMENTS.md](./PLATFORM_API_REQUIREMENTS.md) · full package flow: [YOUTUBE_PACKAGE_UPLOAD.md](./YOUTUBE_PACKAGE_UPLOAD.md)

## Default upload path

**YouTube Data API v3 is the default** for Orbit uploads and native schedules (`privacyStatus=private` + `publishAt`).

YouTube Studio CDP / Playwright is **fallback only** for API gaps (title/thumb ABC, long-form pin comment, Shorts Related pill, end screens). **No new Short pins** (28 Aug 2026).

### Package upload (preferred for episodes)

```bash
cd 07_Content-Ops
npm run youtube:package -- \
  --package ../02_Video-Projects/<NN_Slug>/11_Upload-Package \
  --video ../02_Video-Projects/<NN_Slug>/09_Final-Export/<master>.mp4 \
  --dry-run
```

Resolves Titles / Descriptions / Tags / Chapters / Pinned-Comments (or `PACKAGE_MANIFEST.json`), uploads via API, posts first comment + playlist when possible, then prints a **Studio finish checklist**.

Manifest template: `00_Brand/Channel-Setup/templates/YOUTUBE_PACKAGE_MANIFEST.json`

### Single-file upload

```bash
npm run youtube:upload -- --file /path/to.mp4 --title "Test" --dry-run

npm run youtube:upload -- --file /path/to.mp4 --title "Episode" \
  --format longform --schedule 2026-08-10T18:00:00Z \
  --thumbnail /path/to.jpg --made-for-kids false
```

Or enqueue a Content Ops `PlatformPost` and run `npm run worker` — YouTube jobs with a future `scheduledAt` are claimed **immediately** and uploaded with `publishAt`.

## Developer portal

1. Create a project in [Google Cloud Console](https://console.cloud.google.com/)
2. Enable **YouTube Data API v3**
3. Configure OAuth consent screen (External or Internal)
4. Create **OAuth 2.0 Client ID** → Web application
5. Add authorised redirect URI:
   `http://localhost:3000/api/oauth/google/callback`

## Scopes (minimum)

- `https://www.googleapis.com/auth/youtube.upload`
- `https://www.googleapis.com/auth/youtube.readonly`
- `https://www.googleapis.com/auth/youtube.force-ssl` (comments + playlists)

**Reconnect** the YouTube connection after scope changes so `force-ssl` is granted.

## Environment

```env
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:3000/api/oauth/google/callback
ORBIT_TOKEN_ENCRYPTION_KEY=
APP_BASE_URL=http://localhost:3000
```

## Connect

1. Open `/settings/connections`
2. Click **Connect** on YouTube
3. Sign in with the Google account that owns the Orbit channel
4. Confirm the channel title, ID, and thumbnail appear

## Validate

Use **Validate** on the connection card. Expired tokens refresh via stored refresh token when available.

## Safe test upload

1. Set `PUBLISHING_DRY_RUN=false` only when ready
2. Ensure post has:
   - export MP4 path
   - `privacyStatus=private` (default for tests)
   - explicit `madeForKids` (do not infer from animation)
3. Run `npm run youtube:package -- … --dry-run` then a private live upload
4. Confirm result shows a real YouTube video ID + `https://youtu.be/…`
5. Complete `studioFinish` items (ABC / pin / Related / end screen as listed)

**Do not claim autopublish operational until a private test succeeds.**

## Native schedule behaviour

| Step | Behaviour |
|------|-----------|
| Enqueue with future `scheduledAt` | Job `nextAttemptAt = now` (do not wait until air time) |
| Worker claim | Allowed before `scheduledAt` for YouTube |
| API payload | `status.privacyStatus=private` (or unlisted) + `status.publishAt` ISO |
| After upload | Job → `awaiting_platform_processing`; post → `uploadStatus=scheduled` |
| After go-live | Reconcile via `videos.list` → `uploadStatus=published` |

`publishAt` must be roughly **≥15 minutes** ahead; closer times upload immediately without native schedule.

## Limitations

- Service accounts cannot upload to a normal channel
- Thumbnail upload needs the same OAuth user (`thumbnails.set`)
- Shorts and long-form both use `videos.insert`; format is application-side (`--format longform` skips Shorts duration warnings)
- Local worker must be online **at upload time**, not at air time (YouTube holds the schedule)
- Title/thumb ABC, pin, Related, end screens → Studio finish checklist (not API)

## Manual fallback

Export package → YouTube Studio → record URL/ID in Content Ops. Prefer fixing OAuth / API errors over CDP automation.
