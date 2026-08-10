# FINAL_SHORTS_VISIBILITY_REPAIR_REPORT

Generated: 2026-08-10T12:42:21.545253+00:00  
Channel: Orbit With Ben (`UC_esArsDKd3GJvOkeO0DUog`)  
Audit dir: `00_Brand/Channel-Setup/audits/shorts_visibility_forensic_repair_2026-08-10/`

## Before

| Metric | Count |
|--------|------:|
| Studio Shorts total | 62 |
| Public (Studio list chips) | 5 |
| Public (API authoritative Shorts) | 7 |
| Scheduled Shorts (Studio) | 10 |
| Scheduled all (API shorts+longs) | 12 |
| Private (Studio list) | 47 |
| Drafts | 0 |
| Public longs | 2 |

Public longs: `Mo93x0fxB1Q`, `3xrxdmaOwJI`

## Reconciliation

| Class | Count |
|-------|------:|
| UNIQUE_CONTENT rows | 25 |
| EXACT_DUPLICATE | 13 |
| SUPERSEDED_RENDER | 21 |
| INTENTIONAL_PRIVATE intended | 17 |
| UNKNOWN identity | 0 |
| Overdue canonical | **0** |

Intent reconstructed from `FINAL_APPROVED_RELEASE_CALENDAR.json` + production indexes + 16→13 obsoleteIds — **current visibility ignored for intent**.

## Repairs

| Action | Result |
|--------|--------|
| Published (PRIVATE→PUBLIC) | **0** (none eligible) |
| Kept private | 45 |
| Kept scheduled | 10 |
| Kept public | 7 (includes 2 unexpected superseded) |
| Investigate remaining | 0 |
| Deleted drafts | 0 |

## Root cause

See `SHORTS_VISIBILITY_ROOT_CAUSE.md`.

Private volume is explained by scheduled holds + intentional duplicate/hold policy + 16→13 exclusions — **not** by missed overdue canonical publishes.

Additional finding: two superseded Fermi uploads remain Public while Studio list mislabels them Private.

## Safety

| Check | Result |
|-------|--------|
| Schedule diff | `[]` |
| Long-form mutations | none |
| Uploads | none |
| Deletes | none |
| New IDs | none |
| Unexpected public | `z-DLqoSoEBo`, `UWwNKYf_aU8` (documented; not demoted) |

## Evidence

- `STUDIO_SHORTS_COMPLETE_INVENTORY.json` (62 rows, 3 pages)
- `API_LIVE_STATE.json`
- `LOCAL_SHORTS_PRODUCTION_INVENTORY.json`
- `RECONSTRUCTED_SHORTS_PUBLICATION_PLAN.json`
- `RECONCILIATION_MATRIX.json` / `.md`
- `OVERDUE_CANONICAL_SHORTS.md`
- `UNEXPECTED_PUBLIC_PROBE.json`
- `MUTATION_JOURNAL.json` (empty)
- `ROLLBACK_STATE.json`
- Screenshots under `screenshots/`
- Tooling: `07_Content-Ops/src/lib/publishing/youtube-studio-visibility.ts` + tests

## Verdict

```text
SHORTS RECONCILED — MANUAL REVIEW REQUIRED
```

Reason: overdue path healthy (0), but two unexpected public superseded Shorts need a **separate** authorised privatize decision. No catch-up dump required.
