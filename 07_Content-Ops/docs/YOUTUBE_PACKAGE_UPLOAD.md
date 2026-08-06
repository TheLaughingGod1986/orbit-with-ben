# YouTube package upload (API + Studio finish)

**Default path:** YouTube Data API for upload metadata. Studio (or CDP fallback) only for features the API cannot do.

## One command

```bash
cd 07_Content-Ops

# Dry-run — resolve package, prepare payload, print Studio checklist
npm run youtube:package -- \
  --package ../02_Video-Projects/<NN_Slug>/11_Upload-Package \
  --video ../02_Video-Projects/<NN_Slug>/09_Final-Export/<master>.mp4 \
  --dry-run

# Live private/scheduled upload
npm run youtube:package -- \
  --package ../02_Video-Projects/<NN_Slug>/11_Upload-Package \
  --video ../02_Video-Projects/<NN_Slug>/09_Final-Export/<master>.mp4 \
  --schedule 2026-08-20T18:00:00Z \
  --thumbnail ../02_Video-Projects/<NN_Slug>/08_Thumbnail/Selected/<primary>.png
```

Optional `11_Upload-Package/PACKAGE_MANIFEST.json` — copy from  
`00_Brand/Channel-Setup/templates/YOUTUBE_PACKAGE_MANIFEST.json`.

Single-file uploads without a package: `npm run youtube:upload`.

## What the API does

| Step | API |
|------|-----|
| Video file | yes |
| Title (A / recommended) | yes |
| Description + chapters text | yes |
| Tags | yes |
| Schedule (`publishAt`) | yes |
| Primary thumbnail | yes |
| First comment text | yes (`commentThreads.insert`) |
| Playlist add | yes (`playlistItems.insert`) |

Requires Google reconnect after scope update so `youtube.force-ssl` is granted (comments + playlists + **videos.update** for cleanup).

## Recovery + OAuth safeguards (2026-08-07)

```bash
# Detect force-ssl + safe no-op videos.update on canonical BH long
npm run youtube:verify-oauth

# Compare live shelf vs FINAL_SHELF_VERIFY.json (read-only)
npm run youtube:shelf-verify

# Non-destructive recovery checkpoint (24h|48h|72h|day7|live)
npm run youtube:recovery-status -- --checkpoint 72h
```

Config: `00_Brand/Channel-Setup/YOUTUBE_RECOVERY_MODE.json`  
Registry: `00_Brand/Channel-Setup/YOUTUBE_CANONICAL_REGISTRY.json`

`youtube:package` blocks: replacements, duplicate fingerprints, held mutations, >1 Short/day in recovery, schedule-minute collisions, and blind retries after uncertain uploads.

## Hard rules (2026-08-07 lock)

1. **ONE VIDEO = ONE UPLOAD** — never CDP-replace a live public ID.
2. Demote old IDs to private (or 31 Dec hold) before shipping a new ID.
3. Post-upload `assertYouTubeVideoState` runs automatically in the adapter.
4. Default category **Education (27)** · `defaultAudioLanguage=en-GB`.
5. `notifySubscribers=true` only for immediate public uploads (not scheduled `publishAt`).
6. Quarantined scripts live under `11_Upload-Package/Schedule/DISABLED__*` — do not run.

Stabilization plan: `00_Brand/Channel-Setup/audits/youtube_cleanup_2026-08-07/RECOVERY_7_DAY.md`.

## Studio finish (required gaps)

Printed in the CLI result as `studioFinish` and saved to  
`11_Upload-Package/Schedule/PACKAGE_UPLOAD_RESULT_*.json`.

| Step | Why Studio |
|------|------------|
| Title + thumbnail **ABC** Test & Compare | No Data API |
| **Pin** the first comment | No official pin endpoint |
| Shorts **Related / watch next** | Studio only |
| End screen + cards (long-form) | Studio only |

Use existing CDP helpers only as fallback for those Studio steps — do **not** reintroduce Studio as the primary uploader.

## Package layout

```
11_Upload-Package/
  PACKAGE_MANIFEST.json          # optional
  Titles/*title*abc*.txt
  Descriptions/*.txt
  Tags/*.txt
  Chapters/*.txt                 # merged into description if missing
  Pinned-Comments/*.txt
  Schedule/PACKAGE_UPLOAD_RESULT_*.json
```

## Shorts

```bash
npm run youtube:package -- \
  --package .../10_Shorts-or-Upload-Package \
  --video .../short.mp4 \
  --format shorts \
  --related-video-id <LONG_FORM_ID>
```

Related still must be confirmed in Studio after the long is public.
