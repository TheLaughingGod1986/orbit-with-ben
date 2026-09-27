# Troubleshooting

## App won't start

- Ensure `07_Content-Ops/.env` has `DATABASE_URL="file:./dev.db"`
- Run `npx prisma migrate dev` and `npm run db:seed`

## Distribution pack fails

- Script must be non-empty (≥ ~200 characters)
- Check API response error for validation messages

## Export blocked

- Clip must be approved (not `proposed` / `rejected`)
- Transcript and timestamps must be valid

## Duplicate publish blocked

Provide an intentional repost reason:

- New hook · New edit · Seasonal repost · Performance retest · Updated information

## Insights say “more data needed”

Need enough metric-bearing posts (default ≥ 5) before recommendations appear. This is intentional.

## Platform API “available” but publish fails

v1 does not auto-publish. Manual upload is still required. Adapters only report credential presence.

## Watermarked video

Never re-upload a TikTok/Instagram download. Always use the clean export from `content/exports/.../video/`.

## Smooth audio, glitchy / laggy picture

That is variable frame rate (usually Apple VideoToolbox Shorts encodes), not a
broken voiceover. Remaster with `04_Audio/tools/fix_published_playback_lag.py`
and **Replace** the file on the existing YouTube video. Do not upload a new
video — that resets views. Full runbook: `docs/PLAYBACK_LAG_FIX.md`.
