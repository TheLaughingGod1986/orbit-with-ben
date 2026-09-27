# Autopublish Troubleshooting

## Dry-run is on

Symptom: jobs end as `dry_run_complete`, no external posts.  
Fix: set `PUBLISHING_DRY_RUN=false` only after a private test is intended. Banner must be visible when dry-run is active.

## Worker offline

Symptom: scheduled jobs stay `scheduled` / `pending`.  
Fix: `npm run worker` or `npm run dev:all`. Wake the machine; local sleep stops publishing.

## Encryption key missing

Symptom: OAuth callback redirects with `encryption_key_required`.  
Fix: `openssl rand -base64 32` → `ORBIT_TOKEN_ENCRYPTION_KEY`.

## YouTube reconnect loops

- Refresh token missing (consent without `access_type=offline` / `prompt=consent`)
- Revoked Google access → reconnect
- Wrong Google account without a YouTube channel

## Meta: no Page / no IG

- User must manage a Facebook Page
- Instagram must be professional and linked to the Page
- Reconnect after granting missing permissions

## Instagram container fails

- Media URL not publicly reachable (localhost)
- Unsupported codec / duration
- Missing `instagram_content_publish`
- Container expired — recreate

## TikTok marked published incorrectly

Should never happen. Draft uploads must be `manual_action_required`. If you see `published` without a real publish_id, treat as a bug — do not trust the status.

## X plan errors

403 / plan messages → disable API publish; use manual export until write access is purchased/approved.

## Duplicate blocked

Same clip + platform already published/scheduled. Provide a repost reason only when intentionally reposting.

## Ambiguous timeout

Job may enter reconciliation rather than blind retry. Check external status before publishing again.

## Tokens in browser?

Never expected. If Network tab shows `accessToken`, stop and fix the API response — tokens must stay server-side encrypted fields only.
