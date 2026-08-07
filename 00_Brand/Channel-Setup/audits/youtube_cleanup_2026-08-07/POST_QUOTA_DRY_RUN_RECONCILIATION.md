# Post-Quota Dry-Run Reconciliation

Generated: `2026-08-07T21:09:45Z`

## Verdict

**WAITING FOR YOUTUBE API QUOTA**

Fresh live schedule was captured, then quota exhausted before Hv 3-read confirm + shelf-verify. **Zero schedule mutations.** Plan below is from the fresh capture — not approval-ready.

## Live schedule before (fresh)

- fetchedAt: `2026-08-07T21:08:27.677Z`
- count: **16**
- IDs: `6QFGAFZk264`, `AeFm7gWyWik`, `B2STcIAF1lY`, `PcP64way3xA`, `YsyPMhNmHMk`, `aoR-dA_g7eI`, `b8-X_FyJnHM`, `bLv0RfidjSg`, `eOOFVrJ2Ojc`, `gPCpMsB0w2E`, `ho9VJxp7f3A`, `pjIevt27Svo`, `svYOx07OrIM`, `tUAdhOnMW2g`, `tfTkMdE7qqw`, `w1ej9u0rPTA`

## Dynamic obsolete IDs

`OBSOLETE = LIVE − APPROVED` (not hard-coded)

- obsolete (3): `YsyPMhNmHMk`, `gPCpMsB0w2E`, `w1ej9u0rPTA`
- missing targets (0): none
- already correct (0): none
- need time update (13): `6QFGAFZk264`, `AeFm7gWyWik`, `B2STcIAF1lY`, `PcP64way3xA`, `aoR-dA_g7eI`, `b8-X_FyJnHM`, `bLv0RfidjSg`, `eOOFVrJ2Ojc`, `ho9VJxp7f3A`, `pjIevt27Svo`, `svYOx07OrIM`, `tUAdhOnMW2g`, `tfTkMdE7qqw`

## Planned mutations (NOT applied)

- obsolete unschedules: **3**
- target schedule updates: **13**
- already correct: **0**
- total writes: **16**

| Action | ID | Current privacy | Current publishAt | Target privacy | Target publishAt | Reason |
|---|---|---|---|---|---|---|
| UNSCHEDULE | `YsyPMhNmHMk` | private | `2026-08-26T10:30:00Z` | private | `None` | LIVE_SCHEDULED_IDS - APPROVED_TARGET_IDS |
| UNSCHEDULE | `gPCpMsB0w2E` | private | `2026-08-25T10:30:00Z` | private | `None` | LIVE_SCHEDULED_IDS - APPROVED_TARGET_IDS |
| UNSCHEDULE | `w1ej9u0rPTA` | private | `2026-08-11T10:30:00Z` | private | `None` | LIVE_SCHEDULED_IDS - APPROVED_TARGET_IDS |
| SET_PUBLISH_AT | `6QFGAFZk264` | private | `2026-08-16T10:30:00Z` | private | `2026-08-15T10:30:00Z` | UPDATE_TIME |
| SET_PUBLISH_AT | `AeFm7gWyWik` | private | `2026-08-24T10:30:00Z` | private | `2026-08-23T10:30:00Z` | UPDATE_TIME |
| SET_PUBLISH_AT | `B2STcIAF1lY` | private | `2026-08-10T10:30:00Z` | private | `2026-08-12T10:30:00Z` | UPDATE_TIME |
| SET_PUBLISH_AT | `PcP64way3xA` | private | `2026-08-22T10:30:00Z` | private | `2026-08-21T10:30:00Z` | UPDATE_TIME |
| SET_PUBLISH_AT | `aoR-dA_g7eI` | private | `2026-08-15T10:30:00Z` | private | `2026-08-14T10:30:00Z` | UPDATE_TIME |
| SET_PUBLISH_AT | `b8-X_FyJnHM` | private | `2026-08-14T17:00:00Z` | private | `2026-08-13T17:00:00Z` | UPDATE_TIME |
| SET_PUBLISH_AT | `bLv0RfidjSg` | private | `2026-08-21T19:00:00Z` | private | `2026-08-20T19:00:00Z` | UPDATE_TIME |
| SET_PUBLISH_AT | `eOOFVrJ2Ojc` | private | `2026-08-17T10:30:00Z` | private | `2026-08-16T10:30:00Z` | UPDATE_TIME |
| SET_PUBLISH_AT | `ho9VJxp7f3A` | private | `2026-08-14T19:00:00Z` | private | `2026-08-13T19:00:00Z` | UPDATE_TIME |
| SET_PUBLISH_AT | `pjIevt27Svo` | private | `2026-08-23T10:30:00Z` | private | `2026-08-22T10:30:00Z` | UPDATE_TIME |
| SET_PUBLISH_AT | `svYOx07OrIM` | private | `2026-08-09T10:30:00Z` | private | `2026-08-11T10:30:00Z` | UPDATE_TIME |
| SET_PUBLISH_AT | `tUAdhOnMW2g` | private | `2026-08-08T10:30:00Z` | private | `2026-08-10T10:30:00Z` | UPDATE_TIME |
| SET_PUBLISH_AT | `tfTkMdE7qqw` | private | `2026-08-21T17:00:00Z` | private | `2026-08-20T17:00:00Z` | UPDATE_TIME |

## Gates

- `quotaAvailableAtStart`: `true`
- `quotaExhaustedMidRun`: `true`
- `liveStateCapturedFresh`: `true`
- `liveStateFetchedAt`: `2026-08-07T21:08:27.677Z`
- `publicShelfVerify`: `NOT_RUN_QUOTA`
- `hvStability`: `{"initialFromLiveCapture": {"privacy": "private", "publishAt": null}, "threeConsecutiveConfirm": "NOT_COMPLETED_QUOTA", "pass": false, "note": "Capture showed private+null; serialized 3-read confirm blocked by quotaExceeded"}`
- `targetValidation`: `13/13`
- `obsoleteAmbiguous`: `[]`
- `duplicateMinuteCollisions`: `0`
- `placeholderDates`: `0`
- `excludedCurrentlyScheduled`: `["w1ej9u0rPTA", "gPCpMsB0w2E", "YsyPMhNmHMk"]`

## Next action

After quota reset: complete Hv 3 consecutive reads + `npm run youtube:shelf-verify`, then re-run dry-run gates. Apply only after explicit approval.

