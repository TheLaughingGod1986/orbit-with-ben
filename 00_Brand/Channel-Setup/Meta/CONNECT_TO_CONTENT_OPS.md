# Connect Orbit Facebook + Instagram to Content Ops

Brand: **Orbit with Ben** · YouTube pillar [@OrbitWithBen](https://www.youtube.com/@OrbitWithBen)

This wires Meta the same way TikTok is wired: Content Ops OAuth **and** the
brand-level auto-post mirror for live YouTube Shorts.

## What you need

| Piece | Requirement |
|-------|-------------|
| Facebook Page | Manageable Page named **Orbit with Ben** (or similar) |
| Instagram | **Professional** (Creator/Business) linked to that Page |
| Meta app | Facebook Login + Instagram Graph / Content Publishing products |
| Permissions | `pages_show_list`, `pages_read_engagement`, `pages_manage_posts`, `instagram_basic`, `instagram_content_publish`, `business_management` |

## Content Ops OAuth

1. In [Meta for Developers](https://developers.facebook.com/) create an app (or reuse Orbit Content Ops).
2. Valid OAuth redirect:

```text
http://localhost:3000/api/oauth/meta/callback
```

3. Fill `07_Content-Ops/.env`:

```env
META_APP_ID=
META_APP_SECRET=
META_REDIRECT_URI=http://localhost:3000/api/oauth/meta/callback
ORBIT_TOKEN_ENCRYPTION_KEY=   # openssl rand -base64 32
```

4. Start Content Ops → http://localhost:3000/settings/connections → **Connect** on Instagram / Facebook.
5. Select the Page + linked Instagram professional account.

Docs: `07_Content-Ops/docs/META_CONNECTION_SETUP.md`

## Brand auto-post credentials (shorts mirror)

Same tokens can power the TikTok-style watcher:

```bash
cp 00_Brand/Channel-Setup/Meta/META_CREDENTIALS.example.json \
   00_Brand/Channel-Setup/Meta/META_CREDENTIALS.json
```

Set:

- `page_id` — Facebook Page id
- `page_access_token` — Page token (preferred) or long-lived user token
- `instagram_business_account_id` — IG pro id from Page → Instagram business account
- `publish_instagram` / `publish_facebook` — both `true` by default
- `preferred_method` — `graph` (default) or `cdp`

`META_CREDENTIALS.json` is gitignored.

## Business portfolio

Orbit’s Facebook Page must live in the **Orbit with Ben** Meta business
portfolio (`business_id=1352434763139246`), not Benkay Creative.

| Asset | ID |
|-------|-----|
| Business portfolio | `1352434763139246` (Orbit with Ben) |
| Suite Page asset | `1285932871266399` |
| Facebook Page | `61592833318203` |

If Suite shows “Your Page is in the Benkay Creative business portfolio”, move
the Page (Settings → Pages → Remove from Benkay after disconnecting IG if
required → Add existing Page into Orbit). Audit notes:
`audit/portfolio_fix/PORTFOLIO_FIX.md`.

## CDP fallback (no App Review yet)

Until App Review unlocks content publishing for live users:

```bash
bash 00_Brand/Channel-Setup/Meta/auto/start_meta_chrome.sh
```

Log into Meta Business Suite under the **Orbit with Ben** portfolio as a Page
admin with Instagram linked. Cross-post both destinations in the Suite session
when possible. If Share spins with greyed audience radios, you are not on the
Orbit Page composer — see `PORTFOLIO.md` / `AUTO_POST.md`. The 5-minute
LaunchAgent must not open Create reel; Graph is the default.

## Identity checklist

| Field | Value |
|-------|-------|
| Display name | Orbit with Ben |
| Preferred IG | @orbitwithben |
| Preferred FB Page | Orbit with Ben |
| Bio | Space stories. Big questions. Full films on YouTube ↓ |
| Website | https://www.youtube.com/@OrbitWithBen |
| Avatar | Same Orbit mascot as YouTube / TikTok |

See `META_ACCOUNTS.json` and `AUTO_POST.md`.
