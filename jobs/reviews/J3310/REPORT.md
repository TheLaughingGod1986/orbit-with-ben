# J3310 — T043 thumbnail Test & Compare armed on REXYxuLOBoI (OWB:005)

27 November 2026. Gemini covering as Mini Studio worker.

## Preconditions verified before any Studio click

- Dependencies complete and published on `main`: `J3307` (`jobs/reviews/J3307/REVIEW.md`) and `J3382` (`jobs/reviews/J3382/REVIEW.md`, exact-file PASS + conditional one-test reversible successor authorization over finished inconclusive `T016`).
- Exact file hashes verified immediately before upload:
  - Live A (unchanged): `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J3302_v01/REXYxuLOBoI_live_A.jpg` (1280×720, 140,213 bytes, SHA-256 `bd150e73af713c133b4c326dae05eea087a9d090f6dcac59e836ce759f48a4f0`, hook `LAST LIGHT`).
  - Approved B (`v03`): `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnails/repackage_2026-11/J3302_v03/REXYxuLOBoI_B_v03.jpg` (1280×720, 204,117 bytes, SHA-256 `445cbfd3c41af95f99e621609157e7aec6f2a99b91b7926db2100c9bf6df5c3c`, hook `OUTLIVES OUR SUN`). No `v01`/`v02` files used.
- Browser port note: CDP 9223 was checked read-only first and currently holds Field Order History (`studio.youtube.com/video/9YeKm3e2xto/edit`) following Ben's 26 Nov browser sign-in swap (recorded in J3794/J3799/J3808/J3308). Orbit With Ben (`UC_esArsDKd3GJvOkeO0DUog`) is live on CDP 9224; this job reused the existing `studio.youtube.com` tab on CDP 9224 via `reuse_page` without opening new tabs or switching accounts.
- Fresh read-only Studio check at `2026-11-27T19:23:00Z` confirmed:
  - Channel: **Orbit With Ben** (`UC_esArsDKd3GJvOkeO0DUog`).
  - Video: `REXYxuLOBoI`, Title: `The Last Star: What Happens When a Red Dwarf Dies?`, Visibility: `Public`, Audience: `not 'Made for Kids'`.
  - Prior test `T016`: `Thumbnail only`, `Not enough impressions to declare a winner`, watch-time shares `—` on both options, Option A (`LAST LIGHT`) `Now visible to all viewers`, Option B (`10 TRILLION YEARS`), `Test finished. Ran from 28 October 2026 at 21:33 to 11 November 2026 at 21:47.` No running or newly set test.
  - Preserved finished `T016` report text in `REXYxuLOBoI_T016_preserved_report.txt` and screenshot in `_desk/jobs/J3310/04_t016_report_modal_20261127T192252Z.png` before clicking `New test`.

## Action and post-reload verification

- Re-verified matching finished inconclusive `T016` report immediately before clicking `New test` -> `Continue` under `J3382` one-test authorization over finished `T016`.
- Selected **Thumbnail only** (`Title only=false`, `Thumbnail only=true`, `Title and thumbnail=false`), kept Slot 1 as unchanged live A (`LAST LIGHT`), uploaded exact verified `REXYxuLOBoI_B_v03.jpg` (`OUTLIVES OUR SUN`) into Slot 2, left Slot 3 empty, visually inspected preview screenshot (`09_ab_populated_20261127T192627Z.png`), clicked `Set test`, verified title/description/Public unchanged, and clicked `Save` at `2026-11-27T19:28:19Z`.
- Hard-reloaded `https://studio.youtube.com/video/REXYxuLOBoI/edit` and opened `View test report` at `2026-11-27T19:28:33Z`:
  - Studio shows: **`Thumbnail only` / `A/B test report` / `Test running…`**, Option 1 `LAST LIGHT`, Option 2 `OUTLIVES OUR SUN`, both watch-time shares `—`, **`Estimated time remaining: 13 days 23 hours…`**.
  - Verified Title (`The Last Star: What Happens When a Red Dwarf Dies?`), Description (1,131 chars), Visibility (`Public`), and Audience (`not 'Made for Kids'`) unchanged.
  - Exact reload report saved in `REXYxuLOBoI_T043_armed_report.txt`; screenshots indexed in `EVIDENCE.json`.

## Guards and next step

- No title, description, schedule, privacy, upload, spend or other-video changes. Round 2 titles remain parked. Historical `T016` ledger record preserved intact.
- Next read-back: **11 December 2026** (after 14-day run finishes). Do not replace the running test.
