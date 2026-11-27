# J3308 — T041 thumbnail Test & Compare armed on NbW5G1BpPY0 (OWB:006)

27 November 2026. Gemini covering as Mini Studio worker.

## Preconditions verified before any Studio click

- Dependencies complete and published on `main`: `J3307` (`jobs/reviews/J3307/REVIEW.md`) and `J3382` (`jobs/reviews/J3382/REVIEW.md`, exact-file PASS + conditional one-test reversible successor authorization over finished inconclusive `T006`).
- Exact file hashes verified immediately before upload:
  - Live A (unchanged): `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/08_Thumbnails/repackage_2026-11/J3302_v01/NbW5G1BpPY0_live_A.jpg` (1280×720, 115,997 bytes, SHA-256 `3f0350155a6136d7576fce8c4a9cc4e56293ce0f202a4afabd594e8f93dad698`, hook `A HIDDEN OCEAN`).
  - Approved B (`v03`): `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/08_Thumbnails/repackage_2026-11/J3302_v03/NbW5G1BpPY0_B_v03.jpg` (1280×720, 289,363 bytes, SHA-256 `aaaaef79e7834fc28233b2b990473cbba7e993b3ba3d79865ebc295d297be91f`, hook `2× EARTH'S WATER`). No `v01`/`v02` files used.
- Browser port note: CDP 9223 was checked read-only first and currently holds Field Order History (`UCu94mInMFosxu3W0H6jlI6Q`, returning `Oops` on `NbW5G1BpPY0`) following Ben's 26 Nov browser sign-in swap (recorded in J3794/J3799/J3808). Orbit With Ben (`UC_esArsDKd3GJvOkeO0DUog`) is live on CDP 9224; this job reused the existing `studio.youtube.com` tab on CDP 9224 via `reuse_page` without opening new tabs or switching accounts.
- Fresh read-only Studio check at `2026-11-27T18:10:31Z` confirmed:
  - Channel: **Orbit With Ben** (`UC_esArsDKd3GJvOkeO0DUog`).
  - Video: `NbW5G1BpPY0`, Title: `Could Life Exist Under The Ice Of Europa?`, Visibility: `Public`.
  - Prior test `T006`: `Thumbnail only`, `Not enough impressions to declare a winner`, watch-time shares `—` on both options, Option A (`A HIDDEN OCEAN`) `Now visible to all viewers`, `Test finished. Ran from 15 October 2026 at 10:49 to 29 October 2026 at 10:07.` No running or newly set test.
  - Preserved finished `T006` report text in `NbW5G1BpPY0_T006_preserved_report.txt` and screenshot in `_desk/jobs/J3308/08_t006_report_modal_20261127T181024Z.png` before clicking `New test`.

## Action and post-reload verification

- Clicked `New test` -> `Continue` under `J3382` one-test authorization over finished `T006`.
- Selected **Thumbnail only** (`Title only=false`, `Thumbnail only=true`, `Title and thumbnail=false`), kept Slot 1 as unchanged live A (`A HIDDEN OCEAN`), uploaded exact verified `NbW5G1BpPY0_B_v03.jpg` (`2× EARTH'S WATER`) into Slot 2, left Slot 3 empty, inspected preview screenshot (`14_ab_populated_20261127T181511Z.png`), clicked `Set test`, verified title/description/Public unchanged, and clicked `Save` at `2026-11-27T18:15:26Z`.
- Hard-reloaded `https://studio.youtube.com/video/NbW5G1BpPY0/edit` and opened `View test report` at `2026-11-27T18:15:39Z`:
  - Studio shows: **`Thumbnail only` / `A/B test report` / `Test running…`**, Option 1 `A HIDDEN OCEAN`, Option 2 `2× EARTH'S WATER`, both watch-time shares `—`, **`Estimated time remaining: 13 days 23 hours…`**.
  - Verified Title (`Could Life Exist Under The Ice Of Europa?`), Description (1,332 chars), Visibility (`Public`), and Audience (`not 'Made for Kids'`) unchanged.
  - Exact reload report saved in `NbW5G1BpPY0_T041_armed_report.txt`; screenshots indexed in `EVIDENCE.json`.

## Guards and next step

- No title, description, schedule, privacy, upload, spend or other-video changes. Round 2 titles remain parked. Historical `T006` ledger record preserved intact.
- Next read-back: **11 December 2026** (after 14-day run finishes). Do not replace the running test.
