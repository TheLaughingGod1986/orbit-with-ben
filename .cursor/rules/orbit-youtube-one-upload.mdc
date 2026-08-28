---
description: YouTube one-video-one-upload lock (no CDP replace)
globs:
  - "**/11_Upload-Package/Schedule/**"
  - "**/07_Content-Ops/src/lib/publishing/adapters/youtube.ts"
  - "**/SHORTS_UPLOAD_INDEX.json"
alwaysApply: false
---

# Orbit YouTube — one video = one upload

## Hard rules

1. **Never** run `DISABLED__*` smooth-CFR / replace / CDP upload scripts.
2. **Never** upload a second YouTube ID for an asset that already has a public or scheduled canonical ID.
3. Demote (private / 31 Dec hold) the old ID **before** any new ID can go public.
4. Primary upload path: Content Ops `npm run youtube:package` (Data API) — **blocked while** `YOUTUBE_PUBLISHING_FREEZE.json` has `youtubePublishingFrozen: true`.
5. CDP is forbidden for upload/replace; Studio finish (Related video pill required on Shorts; no new Short pins) is manual only during emergency repair. See `orbit-shorts-related-video.mdc`.
6. After every ship: assert `privacyStatus` + `publishAt` + tags via API (`assertYouTubeVideoState`).
7. OAuth must include `youtube.force-ssl` for visibility updates.
8. `npm run youtube:upload` is permanently disabled.

Canonical cleanup audit: `00_Brand/Channel-Setup/audits/youtube_cleanup_2026-08-07/`.
Freeze: `00_Brand/Channel-Setup/YOUTUBE_PUBLISHING_FREEZE.json`.
