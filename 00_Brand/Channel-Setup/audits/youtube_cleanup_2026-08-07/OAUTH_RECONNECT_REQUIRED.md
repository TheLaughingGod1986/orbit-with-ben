# YouTube OAuth reconnect — RESOLVED (2026-08-07)

## Result

- **Connected:** `benoats86@gmail.com` → brand **Orbit with Ben** (`UC_esArsDKd3GJvOkeO0DUog`)
- **Scopes:** `youtube.force-ssl`, `youtube.upload`, `youtube.readonly`
- **Verify:** `npm run youtube:verify-oauth` PASS
- **en-GB:** applied on 6 canonical IDs — see `EN_GB_METADATA_APPLY.json`

## Pitfalls fixed

1. `APP_BASE_URL` must be `http://localhost:3000` for local reconnect (dead Cloudflare tunnel broke post-consent redirect).
2. Do **not** use `benoats@googlemail.com` / **iwillstream** Brand Account — that is not the Orbit YouTube channel (`youtubeSignupRequired` / wrong channel).
3. Correct path: account chooser → `benoats86@gmail.com` → **Orbit with Ben | YouTube** → Advanced → unsafe → Select all scopes → Continue.
