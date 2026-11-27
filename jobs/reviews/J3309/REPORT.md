# J3309 — Studio Arm Report (T042 on OWB:024 `rVqgtkBV3jc`)

Date: 27 November 2026  
Worker: `gemini` (Mac mini)  
Authority: `J3307` (`done`, `jobs/reviews/J3307/REVIEW.md`) and `J3382` (`done`, `jobs/reviews/J3382/REVIEW.md`, exact-file PASS + conditional one-test reversible successor authorization over finished inconclusive `T004`).

## Pre-upload verification

- Exact bytes verified before upload:
  - Live A (unchanged): `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/08_Thumbnails/repackage_2026-11/J3302_v01/rVqgtkBV3jc_live_A.jpg` (1280×720, 173,510 bytes, SHA-256 `0df5e274de7bad4d3c1c771ca5f4c7afd629a0a89b2653bd23a5c91a62e6af98`, hook `YOU: 1 YEAR / EARTH: 7 YEARS`).
  - Approved B (`v03`): `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/08_Thumbnails/repackage_2026-11/J3302_v03/rVqgtkBV3jc_B_v03.jpg` (1280×720, 198,141 bytes, SHA-256 `0e643ed49990a38cfd8054dfdf9ea7e991805a43b0eb8f7c041a07bcd5192bba`, hook `EARTH AGES 7×`). No `v01`/`v02` files used.
- Browser port note: CDP 9223 was checked read-only first and currently holds Field Order History (`studio.youtube.com/video/9YeKm3e2xto/edit`) following Ben's 26 Nov browser sign-in swap (recorded in J3794/J3799/J3808/J3308/J3310). Orbit With Ben (`UC_esArsDKd3GJvOkeO0DUog`) is live on CDP 9224; this job reused the existing `studio.youtube.com` tab on CDP 9224 via `cdp_tabs.reuse_page` without opening new tabs or switching accounts.
- Fresh read-only Studio check at `2026-11-27T19:36:52Z` confirmed:
  - Channel: **Orbit With Ben** (`UC_esArsDKd3GJvOkeO0DUog`).
  - Video: `rVqgtkBV3jc`, Title: `What Happens If You Travel Near Light Speed?`, Visibility: `Public`, Description: 3,310 chars, Audience: `not 'Made for Kids'`.
  - Prior test `T004`: `Thumbnail only`, `Not enough impressions to declare a winner`, watch-time shares `—` on both options, Option A (`YOU: 1 YEAR / EARTH: 7 YEARS`) `Now visible to all viewers`, Option B (`7 YEARS GONE`), `Test finished. Ran from 1 November 2026 at 18:00 to 15 November 2026 at 18:39.` No running or newly set test.
  - Preserved finished `T004` report text in `rVqgtkBV3jc_T004_preserved_report.txt` and screenshot in `/Users/benjaminoats/_desk/jobs/J3309/04_t004_report_modal_20261127T193652Z.png` before clicking `New test`.

## Action and post-reload verification

- Re-verified matching finished inconclusive `T004` report immediately before clicking `New test` -> `Continue` under `J3382` one-test authorization over finished `T004`.
- Opened `A/B testing`, verified **Thumbnail only** (`Title only=false`, `Thumbnail only=true`, `Title and thumbnail=false`), kept Slot 1 as unchanged live A (`YOU: 1 YEAR / EARTH: 7 YEARS`), uploaded exact verified `rVqgtkBV3jc_B_v03.jpg` (`EARTH AGES 7×`) into Slot 2, left Slot 3 empty, visually inspected populated builder screenshot (`09_ab_populated_20261127T194251Z.png` / `09_ab_populated_final_20261127T194509Z.png`), clicked `Set test`, verified title/description/Public/audience unchanged, and clicked `Save` at `2026-11-27T19:45:25Z`.
- Hard-reloaded `https://studio.youtube.com/video/rVqgtkBV3jc/edit` and opened `View test report` at `2026-11-27T19:45:42Z`:
  - Studio shows: **`Thumbnail only` / `A/B test report` / `Test running…`**, Option 1 `YOU: 1 YEAR / EARTH: 7 YEARS`, Option 2 `EARTH AGES 7×`, both watch-time shares `—`, **`Estimated time remaining: 13 days 23 hours…`**.
  - Verified Title (`What Happens If You Travel Near Light Speed?`), Description (3,310 chars), Visibility (`Public`), and Audience (`not 'Made for Kids'`) unchanged.
  - Exact reload report saved in `rVqgtkBV3jc_T042_armed_report.txt`; screenshots and asset hashes indexed in `EVIDENCE.json`.

## Guards and next step

- No title, description, schedule, privacy, upload, spend or other-video changes. Round 2 titles remain parked. Historical `T004` finished result preserved in `THUMB_LEDGER.json` (`status: done`, `winner: draw`, `2026-11-01 18:00` to `2026-11-15 18:39`) alongside full `T042` v01/v02 history. Independent `024` stage states preserved unchanged.
- Next read-back: **11 December 2026** (after 14-day run finishes). Do not replace the running test.
