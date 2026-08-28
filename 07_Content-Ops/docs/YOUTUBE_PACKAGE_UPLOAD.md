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

Requires Google reconnect after scope update so `youtube.force-ssl` is granted (comments + playlists).

## Studio finish (required gaps)

Printed in the CLI result as `studioFinish` and saved to  
`11_Upload-Package/Schedule/PACKAGE_UPLOAD_RESULT_*.json`.

| Step | Why Studio |
|------|------------|
| Title + thumbnail **ABC** Test & Compare | No Data API |
| **Pin** the first comment (**long-form only** going forward) | No official pin endpoint |
| Shorts **Related video pill** → that week’s Thursday long | Studio only · **desktop** · required; **no new Short pins** (see `orbit-shorts-related-video.mdc`) |

| End screen + cards (long-form) | Studio only |

Use existing CDP helpers only as fallback for those Studio steps — do **not** reintroduce Studio as the primary uploader.

Canonical Related lock: `.cursor/rules/orbit-shorts-related-video.mdc` · `00_Brand/Channel-Setup/SHORTS_FUNNEL_AND_CROSSPOST.md`.

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

`--related-video-id` must be **that Short’s / that week’s Thursday long** (never another Short / dead id). Related still must be set in **desktop** Studio after the long is public: Content → Short → Related video → pick the long → Save. Related pill = only Short → long CTA. Do **not** add new Short pins. Pin is not required when Related is set. Zero `/go/` on Shorts. Longs do not get this field.

