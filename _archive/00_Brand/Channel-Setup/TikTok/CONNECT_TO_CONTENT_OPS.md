# Connect Orbit TikTok to Content Ops

Account: **[@orbitwithben](https://www.tiktok.com/@orbitwithben)**  
Ops UI: http://localhost:3000/settings/connections

## Already done in Content Ops

- `PlatformSettings` for `tiktok` → profile URL + display name `OrbitWithBen`
- OAuth callback stores `accountUsername` / `profileUrl` and syncs settings
- Redirect URI expected: `http://localhost:3000/api/oauth/tiktok/callback`

## Credentials (done)

`07_Content-Ops/.env` already has `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET`, and
`TIKTOK_REDIRECT_URI=http://localhost:3000/api/oauth/tiktok/callback`.

App: **Orbit Content Ops** → https://developers.tiktok.com/app/7668773508012492817/pending

## Finish in TikTok Developer Portal (still needed)

1. **Basic info** (description max **120** chars), e.g.  
   `Private ops tool that drafts and posts Orbit with Ben space stories to TikTok (@OrbitWithBen).`
2. Category: **Education** · Platform: **Web** only · Web URL: `http://localhost:3000`
3. ToS / Privacy (local pages, Content Ops running):
   - `http://localhost:3000/legal/terms`
   - `http://localhost:3000/legal/privacy`  
   Then **Verify URL properties** for each (localhost / owned domains).
4. Upload app icon: `00_Brand/Channel-Setup/TikTok/app_icon_1024.png` → **Save**
5. **Products** → add **Login Kit** + **Content Posting API**
6. Login Kit → Redirect URI:

```text
http://localhost:3000/api/oauth/tiktok/callback
```

7. Restart Content Ops (`npm run dev:all`)
8. Open http://localhost:3000/settings/connections → **Connect** on TikTok
9. Approve scopes `user.info.basic`, `video.upload`, `video.publish`

Until Direct Post is audited, publishing uses **draft upload** (`manual_action_required` — finish in TikTok app).

## Avatar (still pending on TikTok)

Web profile edits are rate-limited (`Slow down, you are editing too fast`).

On phone: **Edit → photo →** `Desktop/OrbitTikTokAvatar.png` (or `00_Brand/Channel-Setup/TikTok/avatar_orbit_800.jpg`) → **Save**.
