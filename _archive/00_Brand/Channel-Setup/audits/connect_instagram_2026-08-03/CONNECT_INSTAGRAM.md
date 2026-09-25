# Connect Instagram to Orbit Meta Business (2026-08-03)

Instagram `@orbitwithben` is **partially** linked to the Orbit Facebook Page, but **not** connected as a Business Suite asset. That is why the Meta Business app shows **Connect Instagram**.

## Current state

| Surface | State |
|---------|--------|
| Facebook Page → Connected Instagram | `@orbitwithben` listed, but **Review account connection** (needs IG password) |
| Meta Business Suite → Instagram accounts | **No Instagram accounts added** |
| Suite Home | **Connect Instagram** + alert **Confirm Instagram account management** |
| Meta Business mobile app | **Connect Instagram** (same gap) |

Portfolio IDs (Orbit with Ben):

- `business_id=1352434763139246`
- `asset_id=1285932871266399` (Page)
- Facebook Page `61592833318203`

## Fix on phone (Meta Business app) — recommended

1. Open **Meta Business Suite** app → **Orbit with Ben** Page.
2. Tap **Connect Instagram**.
3. Log in as **`@orbitwithben`** (Instagram password required).
4. Allow Page managers to manage Instagram when asked.
5. Confirm until the greyed Instagram avatar becomes active and an Instagram follower count appears.

## Fix on desktop (Business Suite)

1. Open Chrome CDP profile used for Meta, or normal Chrome logged into Facebook as Page admin:
   - Suite Home:  
     `https://business.facebook.com/latest/home?business_id=1352434763139246&asset_id=1285932871266399`
2. Click **Connect Instagram** (or **Get Started** on the confirm-management alert).
3. Or: Settings → **Instagram accounts** → **Add** → **Claim Instagram Account** → **Log in as orbitwithben**.
4. Alternate Page path: Facebook Page settings → **Connected Instagram** → **Review Connection** → **Confirm** → **Confirm connection** → message Inbox permission **Confirm** → complete Instagram login (password).

## Automation notes

- CDP on `:9222` can open Claim/OAuth and click **Log in as orbitwithben**, but the Suite `oidclink` callback does not finish adding the asset (popup closes on a blank callback page).
- **Review Connection** advances through modals, then loops back asking for the Instagram password; no password field is exposed without interactive login.
- `:9223` Meta Chrome profile was logged out / not running during this attempt.
- `META_CREDENTIALS.json` `business_id` / `business_suite_asset_id` were corrected to the Orbit portfolio IDs above.

## After it connects

Verify:

1. Suite → Settings → Instagram accounts shows **`@orbitwithben`**
2. Suite Home no longer shows **Connect Instagram**
3. Composer **Post to** lists Instagram (not only Facebook)

Then Graph/CDP Suite publishing can target both FB + IG under the Orbit portfolio.
