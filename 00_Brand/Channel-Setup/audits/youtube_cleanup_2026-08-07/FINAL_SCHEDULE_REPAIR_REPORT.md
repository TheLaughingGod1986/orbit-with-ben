# FINAL SCHEDULE REPAIR REPORT

Generated: `2026-08-07T14:13:15Z`

## 1. Verdict

**SCHEDULE CLEAN WITH MANUAL REVIEW**

Fake 31 Dec holding dates removed from live YouTube (33/33). All formerly held assets are private + unscheduled. Public canonicals unchanged. Proposed real calendar written but **not applied** (awaiting approval). Manual review: approve/reject `PROPOSED_CANONICAL_RELEASE_CALENDAR.md` before any re-schedule.

## 2. Fake holding dates removed

Count: **33**

IDs:
- `2C-eiSMsBLc`
- `IqII5mVGdrs`
- `lIHb_tyxQSM`
- `wOlnj7nZWJM`
- `2uT3wXJLybw`
- `tUAdhOnMW2g`
- `svYOx07OrIM`
- `B2STcIAF1lY`
- `w1ej9u0rPTA`
- `mGwSCdgxQO4`
- `8DxCTXUlw74`
- `YsyPMhNmHMk`
- `gPCpMsB0w2E`
- `AeFm7gWyWik`
- `pjIevt27Svo`
- `PcP64way3xA`
- `bLv0RfidjSg`
- `tfTkMdE7qqw`
- `oFzKgHbAw4M`
- `SGv-wH0XbtI`
- `Tw2OdQABU4E`
- `5MysOlOqLDY`
- `yTljUMV5Gms`
- `QW0cn-O9k5g`
- `eOOFVrJ2Ojc`
- `Web2otrTcT0`
- `icedH_gK8JE`
- `1qts3tIsg9c`
- `6QFGAFZk264`
- `aoR-dA_g7eI`
- `HvAKGjx4lv0`
- `ho9VJxp7f3A`
- `b8-X_FyJnHM`

## 3. Public canonicals

| ID | Expected | Shelf verify |
|---|---|---|
| `Mo93x0fxB1Q` | public | PASS |
| `1HuV8o3gOss` | public | PASS |
| `KcKBixwmcV4` | public | PASS |
| `3xrxdmaOwJI` | public | PASS |
| `JRfhE6yWom4` | public | PASS |
| `L2OFjL4neOo` | public | PASS |

Shelf overall ok: `True` · unexpectedPublic: `[]`

## 4. Private unscheduled content

All former Dec-31 assets are now private without publishAt.

Quarantine holds cleared: 20
Historical duplicates cleared: 13

## 5. Historical duplicates

| Duplicate ID | Classification | Action |
|---|---|---|
| `2C-eiSMsBLc` | HISTORICAL_DUPLICATE | private + unscheduled |
| `IqII5mVGdrs` | HISTORICAL_DUPLICATE | private + unscheduled |
| `lIHb_tyxQSM` | HISTORICAL_DUPLICATE | private + unscheduled |
| `wOlnj7nZWJM` | HISTORICAL_DUPLICATE | private + unscheduled |
| `2uT3wXJLybw` | HISTORICAL_DUPLICATE | private + unscheduled |
| `mGwSCdgxQO4` | HISTORICAL_DUPLICATE | private + unscheduled |
| `8DxCTXUlw74` | HISTORICAL_DUPLICATE | private + unscheduled |
| `oFzKgHbAw4M` | HISTORICAL_DUPLICATE | private + unscheduled |
| `SGv-wH0XbtI` | HISTORICAL_DUPLICATE | private + unscheduled |
| `Tw2OdQABU4E` | HISTORICAL_DUPLICATE | private + unscheduled |
| `5MysOlOqLDY` | HISTORICAL_DUPLICATE | private + unscheduled |
| `yTljUMV5Gms` | HISTORICAL_DUPLICATE | private + unscheduled |
| `QW0cn-O9k5g` | HISTORICAL_DUPLICATE | private + unscheduled |

## 6. Real scheduled content

**None** currently scheduled on YouTube after repair (`stillScheduled=0`).

Proposed calendar is NOT applied.

## 7. Proposed future calendar

See `PROPOSED_CANONICAL_RELEASE_CALENDAR.md` (16 items).

Clusters:
- BLACK_HOLE remaining Shorts: 2026-08-08 → 2026-08-11 @ 12:30 Europe/Paris
- EXOPLANETS: long Thu 2026-08-14 19:00 + Shorts through 2026-08-17
- JWST: long Thu 2026-08-21 19:00 + Shorts through 2026-08-26

## 8. Conflicts found

Proposed calendar conflicts: None

## 9. Registry consistency

- `YOUTUBE_CANONICAL_REGISTRY.json`: Dec-31 `scheduledAt` / `scheduledPublishTimestamp` cleared
- `YOUTUBE_RECOVERY_MODE.json`: `heldVideoIds=[]`, notes updated
- `placeholderHoldDatesForbidden` set on registry
- Local proposed calendar awaiting approval before any live publishAt

## 10. Tests

| Suite | Result |
|---|---|
| `tests/youtube-recovery.test.ts` | run after this report |
| OAuth verify | PASS (force-ssl) |
| Shelf verify | ok=True |

## 11. Manual review

1. **Approve or revise** `PROPOSED_CANONICAL_RELEASE_CALENDAR.md` before applying any schedules.
2. PRIVATE_NOT_READY omitted: `HvAKGjx4lv0`, `icedH_gK8JE`, `Web2otrTcT0`, `1qts3tIsg9c`, `dPMJQp2gMNc`, `rFJoOdQAc9c`.
3. Studio Draft-labeled private uploads remain private/unscheduled (unchanged by this repair).
4. Do not resume automatic scheduling until freeze is intentionally cleared AND proposed calendar is approved.

## 12. Final recommendation

Scheduling may **not** resume automatically yet.

Next step after human approval of the proposed calendar:
`videos.update` on existing IDs only with real publishAt values (never 2026-12-31 placeholders).

Freeze remains active. `youtube:upload` remains disabled. Placeholder holds are code-banned.
