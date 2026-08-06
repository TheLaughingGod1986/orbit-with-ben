# FINAL PUBLISHING ENTRYPOINTS

Audited on branch `cursor/youtube-channel-cleanup-9055` @ `edddb72`.

## Approved primary path (ONLY for new catalogue uploads)

```bash
cd 07_Content-Ops
npm run youtube:package -- --package <11_Upload-Package> --video <mp4> [--schedule ISO] [--dry-run]
```

Implements: metadata validation, source fingerprint, content-ID / fingerprint / historical-dupe checks, schedule collision checks, recovery gates, single insert, immediate registry persist, ambiguous-response stop, post-upload `assertYouTubeVideoState`, Studio finish notes. Does **not** invoke CDP replace.

Code: `07_Content-Ops/scripts/youtube-package-upload.ts` → `YouTubePublishingAdapter` (`videos.insert`, optional `videos.update` when force-ssl present).

## Alternate API path (NOT recovery-gated — residual risk)

```bash
npm run youtube:upload
```

`07_Content-Ops/scripts/youtube-api-upload.ts` — still callable; **no** recovery / fingerprint / registry gates found. Treat as **disabled for production use** until gated or removed from workflow docs.

## Read-only / ops commands (non-mutating or verify)

| Command | Purpose |
|---|---|
| `npm run youtube:shelf-verify` | Compare live privacy/publishAt to `FINAL_SHELF_VERIFY.json` |
| `npm run youtube:verify-oauth` | Scope + safe videos.update probe |
| `npm run youtube:recovery-status` | Recovery window + public checkpoint |

## API mutation surface (code capable)

| API | Where | Active? |
|---|---|---|
| `videos.insert` | `adapters/youtube.ts` via `youtube:package` / `youtube:upload` | YES (package approved; upload ungated) |
| `videos.update` | adapter + verify-oauth | BLOCKED live (missing force-ssl) |
| `videos.delete` | not in normal workflow | Not used by package path |
| `playlistItems.insert/delete` | adapter helpers | Requires force-ssl |

## Quarantined scripts (hard exit)

| Path | Status |
|---|---|
| `02_Video-Projects/002_.../Schedule/DISABLED__upload_smooth_cfr_v01.py` | `SystemExit` on import/run |
| `.../DISABLED__upload_smooth_cfr_continue_v01.py` | `SystemExit` |
| `.../DISABLED__replace_smooth_cfr_v01.py` | `SystemExit` |
| `.../DISABLED__replace_smooth_cfr_v02.py` | `SystemExit` |

Tests in `07_Content-Ops/tests/youtube-recovery.test.ts` assert these remain DISABLED and are not referenced by npm scripts.

## Still-reachable historical CDP / replace / upload scripts (NOT fully disabled)

Examples (non-exhaustive; full search hit many under audits/ + Upload-Package/Schedule):

- `00_Brand/Channel-Setup/audits/_replace_shorts_v02_youtube.py`
- `00_Brand/Channel-Setup/audits/_privatize_old_duplicates_cdp.py`
- `00_Brand/Channel-Setup/audits/_cleanup_visibility_cdp.py` (folder)
- `00_Brand/Channel-Setup/audits/youtube_cleanup_2026-08-07/_cleanup_visibility_cdp.py`
- `02_Video-Projects/002_.../Schedule/_upload_normal_speed_and_micros_v01.py`
- `02_Video-Projects/002_.../Schedule/_upload_bh_normal_shorts_micros_v02.py`
- `02_Video-Projects/002_.../Schedule/_upload_schedule_bh_nf_v01.py`
- `02_Video-Projects/002_.../Schedule/_upload_shorts_private_v02.py`
- `02_Video-Projects/002_.../Schedule/_upload_schedule_longform_v02.py`
- `02_Video-Projects/004_.../Schedule/_replace_and_schedule_jwst_v01.py`
- `02_Video-Projects/004_.../Schedule/_upload_longform_cdp_nativedialog_v01.py`
- `02_Video-Projects/004_.../Schedule/_upload_jwst_v03_*.py`

Cursor rule `.cursor/rules/orbit-youtube-one-upload.mdc` forbids using DISABLED__ / CDP as uploader, but **filesystem reachability remains**.

## Background processes

| Process | YouTube mutate? |
|---|---|
| LaunchAgent `dev.orbit.meta-live-shorts` | No (Meta) |
| LaunchAgent `dev.orbit.threads-live-shorts` | No (Threads) |
| LaunchAgent `dev.orbit.tiktok-*` | No (TikTok) |
| crontab Orbit YouTube | None found |
| GitHub Actions | None |
| PM2 | None |
| Content Ops worker for youtube:package | None running |

## Recovery config

Source: `00_Brand/Channel-Setup/YOUTUBE_RECOVERY_MODE.json`

- recoveryMode: true
- startedAt: 2026-08-07T00:00:00+02:00
- endsAt: ~2026-08-13 (durationDays 7)
- maxShortsPerDay: 1
- maxLongsDuringRecovery: 0
- replacementUploadsAllowed: false
- duplicateUploadsAllowed: false
- bulkMetadataUpdatesAllowed: false
- deleteAndReuploadAllowed: false

Do **not** silently extend or end recovery in this audit.
