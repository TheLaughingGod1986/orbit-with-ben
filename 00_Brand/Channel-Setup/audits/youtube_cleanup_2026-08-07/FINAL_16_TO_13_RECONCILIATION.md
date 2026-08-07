# Final 16→13 Reconciliation (PLANNING ONLY — QUOTA BLOCKED)

Generated: `2026-08-07T16:02:16Z`

**Quota gate:** WAITING FOR YOUTUBE API QUOTA

**Mutations:** 0

Stale source: `FINAL_SCHEDULE_APPLY_BEFORE.json` — NOT authoritative. Fresh live fetch required after quota reset.

Stale live scheduled count: **16**
Approved target: **13**
Obsolete candidates (stale): `YsyPMhNmHMk`, `gPCpMsB0w2E`, `w1ej9u0rPTA`

| YouTube ID | Live current publishAt (stale) | Approved publishAt | Action |
|---|---|---|---|
| `6QFGAFZk264` | `2026-08-16T10:30:00Z` | `2026-08-15T10:30:00Z` | UPDATE_TIME |
| `AeFm7gWyWik` | `2026-08-24T10:30:00Z` | `2026-08-23T10:30:00Z` | UPDATE_TIME |
| `B2STcIAF1lY` | `2026-08-10T10:30:00Z` | `2026-08-12T10:30:00Z` | UPDATE_TIME |
| `PcP64way3xA` | `2026-08-22T10:30:00Z` | `2026-08-21T10:30:00Z` | UPDATE_TIME |
| `YsyPMhNmHMk` | `2026-08-26T10:30:00Z` | `None` | UNSCHEDULE |
| `aoR-dA_g7eI` | `2026-08-15T10:30:00Z` | `2026-08-14T10:30:00Z` | UPDATE_TIME |
| `b8-X_FyJnHM` | `2026-08-14T17:00:00Z` | `2026-08-13T17:00:00Z` | UPDATE_TIME |
| `bLv0RfidjSg` | `2026-08-21T19:00:00Z` | `2026-08-20T19:00:00Z` | UPDATE_TIME |
| `eOOFVrJ2Ojc` | `2026-08-17T10:30:00Z` | `2026-08-16T10:30:00Z` | UPDATE_TIME |
| `gPCpMsB0w2E` | `2026-08-25T10:30:00Z` | `None` | UNSCHEDULE |
| `ho9VJxp7f3A` | `2026-08-14T19:00:00Z` | `2026-08-13T19:00:00Z` | UPDATE_TIME |
| `pjIevt27Svo` | `2026-08-23T10:30:00Z` | `2026-08-22T10:30:00Z` | UPDATE_TIME |
| `svYOx07OrIM` | `2026-08-09T10:30:00Z` | `2026-08-11T10:30:00Z` | UPDATE_TIME |
| `tUAdhOnMW2g` | `2026-08-08T10:30:00Z` | `2026-08-10T10:30:00Z` | UPDATE_TIME |
| `tfTkMdE7qqw` | `2026-08-21T17:00:00Z` | `2026-08-20T17:00:00Z` | UPDATE_TIME |
| `w1ej9u0rPTA` | `2026-08-11T10:30:00Z` | `None` | UNSCHEDULE |

## Next action after quota reset

1. Re-run quota probe
2. Fresh live schedule capture → FINAL_RECONCILIATION_LIVE_BEFORE.*
3. Rebuild this reconciliation from live data
4. Hv serialized stability gate
5. Unschedule obsolete → apply 13 transactionally
