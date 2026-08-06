# Smooth-CFR replace status — 2026-08-07

## YouTube Studio (canonical shelf)

| Role | ID | Visibility | Notes |
|------|-----|------------|-------|
| Long (smooth) | `RCs6MMxF3ko` | **Public** | Restored; keep this as the only public long |
| Launch Short | `IwpO33AJaPQ` | **Public** | Restored |
| Falling In | `IqII5mVGdrs` | Scheduled | Needs manual **Public** (schedule accordion blocks CDP radios) |
| Time Appears NF | `2C-eiSMsBLc` | Scheduled | Smooth file — keep |
| Look Back | `lIHb_tyxQSM` | Scheduled | Smooth file — keep |
| What You Would See NF | `wOlnj7nZWJM` | Scheduled | Smooth file — keep |
| Point of No Return | `2uT3wXJLybw` | Scheduled | Smooth file — keep |
| Old long (juddery) | `3xrxdmaOwJI` | **Private** | ABC Continue worked |
| Old launch Shorts | `JRfhE6yWom4`, `L2OFjL4neOo` | **Private** | Re-demoted after they flipped public |
| Older scheduled Shorts | `tUAdhOnMW2g`, `svYOx07OrIM`, `B2STcIAF1lY`, `w1ej9u0rPTA` | Still **Scheduled** | CDP cannot clear Schedule accordion reliably — **manual Private** in Studio |

## Meta (IG + Facebook Reels)

All 6 BH smooth lean files are on Meta:

- Live Share-now: `IwpO33AJaPQ`, `IqII5mVGdrs`
- Scheduled: `2C-eiSMsBLc`, `lIHb_tyxQSM`, `wOlnj7nZWJM`, `2uT3wXJLybw`

Ledger: `00_Brand/Channel-Setup/Meta/META_POSTED.json`  
Fix shipped: Share-now for `post_now`; Suite local-TZ vs London schedule floor.

## Threads

Link cards already present for live smooth IDs (`IwpO33AJaPQ`, `IqII5mVGdrs`). No video re-upload this pass (watcher/link-card path).

## TikTok

Apply failed this pass (`no file input` / `not_in_studio_after_schedule` / navigation abort). Upload UI was reachable earlier (ban appears lifted) but Studio upload automation is unstable — needs a clean TikTok Chrome tab retry.

## Manual finish (Studio)

1. Open `IqII5mVGdrs` → Visibility → **Public** → Save  
2. For each of `tUAdhOnMW2g`, `svYOx07OrIM`, `B2STcIAF1lY`, `w1ej9u0rPTA`: Visibility → **Private** (turn off Schedule) → Save  
3. Do **not** run old cleanup scripts that privatize `RCs6` / `IwpO`
