# Content workflow

## 0. Long-form production helpers (pre–Content Ops)

Before a video is “completed” for distribution, use shared CLIs in `04_Audio/tools/`:

| Gate | Tool |
|------|------|
| vidIQ title score sheet | `vidiq_title_score_sheet.py` |
| VO → SRT captions | `transcribe_vo.py` |
| `[SFX:]` → ElevenLabs SFX | `generate_sfx_from_script.py` |
| `[MUSIC:]` → instrumental bed | `generate_music_bed.py` |
| **CFR remaster (playback lag)** | `orbit_cfr_delivery.py` / `fix_published_playback_lag.py` |

Laggy/glitchy picture with smooth audio is VFR + VideoToolbox. Remaster, then **Studio Replace** the original video id — never a new upload. Details: `docs/PLAYBACK_LAG_FIX.md`.

Package checklist: `00_Brand/Channel-Setup/templates/PRODUCTION_CHECKLIST_V2.md`. Other CLIs: `04_Audio/tools/README.md`.

## 1. Register a completed long-form video

1. Open Content Ops (`cd 07_Content-Ops && npm run dev`)
2. Seed includes **Will We Ever Meet Aliens?** — or insert via Prisma / future form
3. Ensure `script`, `youtubeUrl`, `publicationDate`, and `projectFolder` are set

## 2. Create Distribution Pack

On the video page, click **Create Distribution Pack**.

The planner:

- reads the script
- proposes 4–8 standalone moments
- scores quality
- drafts platform posts as `draft`

Exports are **not** created until clips are approved.

## 3. Approve / edit clips

- Approve or reject proposed clips
- Edit titles, hooks, timestamps, transcript in the DB/API (`PATCH /api/clips/:id`)
- Move: proposed → approved → editing → exported → scheduled → published

## 4. Generate platform copy

On the clip workspace: **Generate platform copy**.

Produces titles, captions, hashtags, CTAs, pinned comments, cover text, alternatives for X/Threads.

## 5. Export upload package

**Export upload package** writes:

```
content/exports/<slug>/clip-NN-<name>/
  video/ captions/ thumbnails/ metadata/
  upload-checklist.md
  manifest.json
```

Place the clean vertical MP4 in `video/`. Never use watermarked downloads.

## 6. Schedule & publish

Use **Calendar** to review the month/week. Update datetime + status via the post form. Record the published URL after manual upload.

## 7. Import analytics

Analytics page → paste CSV → preview → import. Insights generate only when enough rows exist.
