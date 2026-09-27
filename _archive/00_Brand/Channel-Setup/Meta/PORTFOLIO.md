# Meta business portfolio — Orbit with Ben

Orbit’s Facebook Page lives in the **Orbit with Ben** Meta business portfolio,
not Benkay Creative.

| Asset | ID |
|-------|-----|
| Business portfolio | `1352434763139246` |
| Suite Page asset | `1285932871266399` |
| Facebook Page | `61592833318203` |

Moved out of Benkay Creative (`1203116147241086`) on **2026-08-03**.

If Suite still shows a Benkay banner, switch portfolio to **Orbit with Ben** in
Business settings. After any Page move, reconnect Instagram (portfolio move
drops Suite IG asset linkage even when Page → Connected Instagram still lists
`@orbitwithben`).

### Reconnect Instagram (required for Meta Business app)

Suite currently shows **Connect Instagram** / **No Instagram accounts added**
until this is finished. Page settings also show **Review account connection**
(needs the Instagram password).

**Phone (Meta Business app):** Orbit with Ben → **Connect Instagram** → log in
as `@orbitwithben` → allow management → confirm until the IG avatar is active.

**Desktop:** Suite Home
(`business_id=1352434763139246&asset_id=1285932871266399`) →
**Connect Instagram** / **Continue**, or Settings → Instagram accounts →
**Add** → **Claim Instagram Account**. Alternate: Facebook Page settings →
Connected Instagram → **Review Connection** → **Confirm connection** → enter
IG password.

Details / automation notes:
`../audits/connect_instagram_2026-08-03/CONNECT_INSTAGRAM.md`

CDP / composer URLs should include
`business_id=1352434763139246&asset_id=1285932871266399` (see
`META_CREDENTIALS.example.json`, `auto/start_meta_chrome.sh`).

If **Create reel → Share** hangs on a spinner with greyed **Who can see this?**
and “only available for posts to a Facebook Page”, the tab is not the Orbit
Page composer (often leftover Benkay `business_id=1203116147241086` /
`asset_id=1251385088056874`). Close extra Suite tabs and reopen the Page URL
above. CDP refuses those stale IDs (`auto/suite_ids.py`).
