# J2846 read-back — Fermi Paradox thumbnail test T038

25 November 2026. Gemini (`gemini`, acting Chief). Video `Mo93x0fxB1Q`, Orbit With Ben (`UC_esArsDKd3GJvOkeO0DUog`), Orbit Studio CDP 9223 via `cdp_tabs.reuse_page`.

## Fresh read before any change

- Channel confirmed: Orbit With Ben (`UC_esArsDKd3GJvOkeO0DUog`).
- Video title: `Why Haven't We Found Aliens Yet? The Fermi Paradox Explained` (matches manifest).
- Visibility: `Public`.
- Live thumbnail: `SILENCE` (matches manifest).
- A/B test report modal (read-only before `New test -> Continue`):
  - `Thumbnail only` / `A/B test report` / `1 views during test period`
  - Verdict: `Not enough impressions to declare a winner`
  - Option A (`SILENCE`): `Now visible to all viewers`, watch-time share `—`
  - Option B (`ALIENS HIDING?`): watch-time share `—`
  - Footer: `Test finished. Ran from 15 October 2026 at 10:54 to 29 October 2026 at 10:19.`
- No test was running. That matches the preserved finished `T005` report in `05_Analytics/tests/THUMB_LEDGER.json`.
- Pre-change evidence saved locally: `/Users/benjaminoats/_desk/jobs/J2846/01_edit_page_before.png`, `01_edit_page_info.json`, `02_thumb_section_before.png`, `03_t005_report_modal.png`, `03_t005_report_modal.json`.

## What was set

- Under the J2844 one-off Chief authorization (`jobs/reviews/J2844/REVIEW.md`), clicked `New test` -> `Continue` over the confirmed finished `T005` report.
- Selected `Thumbnail only` (two-arm comparison; no title test, no straight thumbnail replacement).
- Slot 1 stayed the current live thumbnail `SILENCE`.
- Slot 2 uploaded exact approved B file `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/001_Will-We-Ever-Meet-Aliens/08_Thumbnails/repackage_2026-11/J2834_v03/Mo93x0fxB1Q_B_v05.jpg` (`ZERO SIGNALS`), pre-upload SHA-256 verified as `95d1a92bd988667743c068e4fe69d67b5d6eeea7097aad2a28de9151d7836578` (495,044 bytes).
- Slot 3 left empty.
- Clicked `Set test` and `Save` on Video details.
- Title, description (exact string match verified), visibility (`Public`), schedule, and live thumbnail outside the test were not changed. `T036` was not touched. £0 spend.

## After save and reload

- Reloaded `https://studio.youtube.com/video/Mo93x0fxB1Q/edit` and reopened the A/B test report modal.
- Confirmed: `Thumbnail only`, `Test running…`, `Estimated time remaining: 13 days 23 hours…`.
- Both arms display the unchanged live title `Why Haven't We Found Aliens Yet? The Fermi Paradox Explained` on `Orbit With Ben`.
- Arm 1 is `SILENCE`; Arm 2 is `ZERO SIGNALS`.
- Post-reload evidence saved locally: `/Users/benjaminoats/_desk/jobs/J2846/06_before_set_test.png`, `07b_after_reload.png`, `07b_after_reload_info.json`, `08_t038_running_modal.png`, `08_t038_running_modal.json`.
