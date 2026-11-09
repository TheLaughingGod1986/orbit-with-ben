# J0135 — 025 Length-Test Short (`N42gKBbD7tE`) Related Video Set to `Js6EQJ8qDi8`

- **Job**: `J0135` (`025 length-test Short (J0134): set Related to Js6EQJ8qDi8 once the long is public, before Thu 12 Nov 11:30 London`)
- **Agent**: `macbook`
- **Completed At**: `2026-11-09T22:51Z`
- **Spend**: `£0.00`

## Verification Summary

1. **Prerequisites**:
   - `J0123` (`025 date gate`): `done` (`2026-11-09T10:52Z`).
   - `Js6EQJ8qDi8` (*The Mars Robot Meant to Die in 90 Days (It Lasted 14 Years)* / film 025 Mars robot long): `public` since `2026-11-08T18:00:15Z`.
   - Target length-test Short (`"lengthTest": true` in `00_Brand/Channel-Setup/social/UPLOADS.json`): `N42gKBbD7tE` (*How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years?*, `55` s, scheduled for `2026-11-12T11:30:00Z`).
2. **Orbit Studio (`CDP 9223`) Action & Read-Back**:
   - Reused existing `studio.youtube.com` tab on `CDP 9223` and verified channel ID `UC_esArsDKd3GJvOkeO0DUog` (`@OrbitWithBen`).
   - Opened `https://studio.youtube.com/video/N42gKBbD7tE/edit`.
   - Selected `Js6EQJ8qDi8` (*The Mars Robot Meant to Die in 90 Days (It Lasted 14 Years)*) in `ytcp-shorts-content-links-picker` (`#linked-video-editor-link`) and clicked `Save`.
   - Reloaded `https://studio.youtube.com/video/N42gKBbD7tE/edit` (`ignoreCache: true`) and verified read-back:
     - `channelId`: `UC_esArsDKd3GJvOkeO0DUog`
     - `pickerText`: `Related video The Mars Robot Meant to Die in 90 Days (It Lasted 14 Years)` (`videoId: Js6EQJ8qDi8`)
     - `visibilityText`: `Visibility Scheduled` (`2026-11-12T11:30:00Z` untouched)
     - `titleText`: `How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years?` (untouched)
     - `saveDisabled`: `true` (saved state persisted)
     - No pinned comment added; no `/go/` link added.
