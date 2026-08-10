# Audit Failure Root Cause — "Studio Drafts: 0"

Generated: `2026-08-10T11:55:29.774Z`

## What the previous audit reported

- Studio Drafts: **0**
- "No matching videos" on Draft filter

## What Studio actually shows (2026-08-10 forensic)

- Content → **Shorts** → Visibility: Draft → **15 rows**
- Content → **Videos** → Visibility: Draft → **0 rows** ("No matching videos")

## Proven technical cause

```text
WRONG_STUDIO_TAB_FILTER
```

Draft filter on Content → Videos (/videos/upload) is empty, but Content → Shorts (/videos/short) has Draft rows. Shorts drafts are tab-scoped.

Evidence:

1. Playwright Draft filter on `/videos/upload` → empty (screenshots `12_videos_upload_drafts.png`).
2. Playwright Draft filter on `/videos/short` → 15 Draft rows (screenshots `11_shorts_drafts.png`, `17_all_drafts_loaded.png`).
3. Draft list rows often **omit** `/video/{id}` anchors; Edit draft uses `?udvid=VIDEO_ID` linking to API-visible private uploads.
4. Therefore an API-only uploads playlist inventory also **cannot** see a separate "draft object" — drafts are a **Studio UI state** over existing video IDs (or unfinished UI wrappers), not a distinct Data API privacy enum.

## Secondary nuance

- YouTube Data API `privacyStatus` values are `public | private | unlisted` — there is **no** `draft` privacy enum.
- Studio Private filter includes scheduled holds (`private` + `publishAt`), so Private count ≠ "leftover junk".

## Fix applied (local tooling only — no live mutations)

- New module: `07_Content-Ops/src/lib/publishing/youtube-studio-visibility.ts`
- Taxonomy: PUBLIC / SCHEDULED / PRIVATE / DRAFT / PROCESSING / FAILED_UPLOAD / UNKNOWN
- Draft enumeration must use **Content → Shorts** path
- `udvid` extraction for draft→video id linkage
- Regression tests: `07_Content-Ops/tests/youtube-studio-visibility.test.ts`

## Regression

Tests reproduce:

- Draft detection without list videoId
- Wrong-tab gap diagnosis (Videos=0, Shorts>0 → WRONG_STUDIO_TAB_FILTER)
- Delete proposal gating / unknown→protect
