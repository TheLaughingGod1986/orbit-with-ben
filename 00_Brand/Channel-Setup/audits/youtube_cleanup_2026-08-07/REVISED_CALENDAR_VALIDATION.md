# Revised Calendar Validation

Generated: `2026-08-07T15:04:28Z`

Proposal-only. No YouTube mutations performed.

## Date validation (every proposed publishAt)

| ID | Local | Weekday | UTC | CEST+2 | Not past | No placeholder | Family | Result |
|----|-------|---------|-----|--------|----------|----------------|--------|--------|
| `tUAdhOnMW2g` | 2026-08-10 12:30 Paris | Monday | `2026-08-10T10:30:00Z` | PASS | PASS | PASS | PASS | **PASS** |
| `svYOx07OrIM` | 2026-08-11 12:30 Paris | Tuesday | `2026-08-11T10:30:00Z` | PASS | PASS | PASS | PASS | **PASS** |
| `B2STcIAF1lY` | 2026-08-12 12:30 Paris | Wednesday | `2026-08-12T10:30:00Z` | PASS | PASS | PASS | PASS | **PASS** |
| `b8-X_FyJnHM` | 2026-08-13 19:00 Paris | Thursday | `2026-08-13T17:00:00Z` | PASS | PASS | PASS | PASS | **PASS** |
| `ho9VJxp7f3A` | 2026-08-13 21:00 Paris | Thursday | `2026-08-13T19:00:00Z` | PASS | PASS | PASS | PASS | **PASS** |
| `aoR-dA_g7eI` | 2026-08-14 12:30 Paris | Friday | `2026-08-14T10:30:00Z` | PASS | PASS | PASS | PASS | **PASS** |
| `6QFGAFZk264` | 2026-08-15 12:30 Paris | Saturday | `2026-08-15T10:30:00Z` | PASS | PASS | PASS | PASS | **PASS** |
| `eOOFVrJ2Ojc` | 2026-08-16 12:30 Paris | Sunday | `2026-08-16T10:30:00Z` | PASS | PASS | PASS | PASS | **PASS** |
| `tfTkMdE7qqw` | 2026-08-20 19:00 Paris | Thursday | `2026-08-20T17:00:00Z` | PASS | PASS | PASS | PASS | **PASS** |
| `bLv0RfidjSg` | 2026-08-20 21:00 Paris | Thursday | `2026-08-20T19:00:00Z` | PASS | PASS | PASS | PASS | **PASS** |
| `PcP64way3xA` | 2026-08-21 12:30 Paris | Friday | `2026-08-21T10:30:00Z` | PASS | PASS | PASS | PASS | **PASS** |
| `pjIevt27Svo` | 2026-08-22 12:30 Paris | Saturday | `2026-08-22T10:30:00Z` | PASS | PASS | PASS | PASS | **PASS** |
| `AeFm7gWyWik` | 2026-08-23 12:30 Paris | Sunday | `2026-08-23T10:30:00Z` | PASS | PASS | PASS | PASS | **PASS** |

## Cadence rules

- max 1 Short/day: PASS
- max 1 long/week: PASS (Exo Thu 13 Aug; JWST Thu 20 Aug)
- no same-day unrelated family: PASS
- observation 7–9 Aug with no *new* proposed publishing: PASS (optional Sun 9 is recommendation only)
- not-ready excluded from schedule: PASS
- existing IDs only / no new IDs: PASS

## Not-ready confirmations

- `HvAKGjx4lv0` privacy=unlisted publishAt=None → **FAIL** (historical replacement / manual review)
- `icedH_gK8JE` privacy=private publishAt=None → **PASS** (edit not approved)
- `Web2otrTcT0` privacy=private publishAt=None → **PASS** (metadata incomplete)
- `1qts3tIsg9c` privacy=private publishAt=None → **PASS** (edit not approved)
- `dPMJQp2gMNc` privacy=private publishAt=None → **PASS** (duplicate / accidental early publication)
- `rFJoOdQAc9c` privacy=private publishAt=None → **PASS** (duplicate / accidental early publication)

## Recovery safety

- shelf PASS: True
- six canonicals public: yes (Mo93x0fxB1Q, 1HuV8o3gOss, KcKBixwmcV4, 3xrxdmaOwJI, JRfhE6yWom4, L2OFjL4neOo)
- no new IDs in proposal: yes
- recovery escalateNow: false
- historical duplicates not scheduled: yes
- live still has old applied publishAt on 16 IDs: noted (superseded; not cleared in this phase)

## Verdict: `CALENDAR NEEDS REVIEW`

**AWAITING APPROVAL — NO SCHEDULE APPLIED**

