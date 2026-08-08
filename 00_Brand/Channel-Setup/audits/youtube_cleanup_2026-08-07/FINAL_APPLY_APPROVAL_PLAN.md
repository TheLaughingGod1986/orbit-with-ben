# Final Apply Approval Plan

Generated: `2026-08-08T07:35:42.588Z`

**Status:** AWAITING EXPLICIT APPLY APPROVAL

Do **not** apply automatically.

## Mutation totals

- obsolete unschedules: **3**
- target updates: **13**
- already correct: **0**
- total planned writes: **16**

## Proposed mutations

| ID | Current state | Target state | Action |
|---|---|---|---|
| `YsyPMhNmHMk` | private / `2026-08-26T10:30:00Z` | private / `null` | UNSCHEDULE |
| `gPCpMsB0w2E` | private / `2026-08-25T10:30:00Z` | private / `null` | UNSCHEDULE |
| `w1ej9u0rPTA` | private / `2026-08-11T10:30:00Z` | private / `null` | UNSCHEDULE |
| `6QFGAFZk264` | private / `2026-08-16T10:30:00Z` | private / `2026-08-15T10:30:00Z` | UPDATE_TIME |
| `AeFm7gWyWik` | private / `2026-08-24T10:30:00Z` | private / `2026-08-23T10:30:00Z` | UPDATE_TIME |
| `B2STcIAF1lY` | private / `2026-08-10T10:30:00Z` | private / `2026-08-12T10:30:00Z` | UPDATE_TIME |
| `PcP64way3xA` | private / `2026-08-22T10:30:00Z` | private / `2026-08-21T10:30:00Z` | UPDATE_TIME |
| `aoR-dA_g7eI` | private / `2026-08-15T10:30:00Z` | private / `2026-08-14T10:30:00Z` | UPDATE_TIME |
| `b8-X_FyJnHM` | private / `2026-08-14T17:00:00Z` | private / `2026-08-13T17:00:00Z` | UPDATE_TIME |
| `bLv0RfidjSg` | private / `2026-08-21T19:00:00Z` | private / `2026-08-20T19:00:00Z` | UPDATE_TIME |
| `eOOFVrJ2Ojc` | private / `2026-08-17T10:30:00Z` | private / `2026-08-16T10:30:00Z` | UPDATE_TIME |
| `ho9VJxp7f3A` | private / `2026-08-14T19:00:00Z` | private / `2026-08-13T19:00:00Z` | UPDATE_TIME |
| `pjIevt27Svo` | private / `2026-08-23T10:30:00Z` | private / `2026-08-22T10:30:00Z` | UPDATE_TIME |
| `svYOx07OrIM` | private / `2026-08-09T10:30:00Z` | private / `2026-08-11T10:30:00Z` | UPDATE_TIME |
| `tUAdhOnMW2g` | private / `2026-08-08T10:30:00Z` | private / `2026-08-10T10:30:00Z` | UPDATE_TIME |
| `tfTkMdE7qqw` | private / `2026-08-21T17:00:00Z` | private / `2026-08-20T17:00:00Z` | UPDATE_TIME |

## Next

Await Ben's explicit approval, then:

```bash
cd 07_Content-Ops && npm run youtube:reconcile-16-to-13 -- --allow-emergency-unfreeze --execute
```
