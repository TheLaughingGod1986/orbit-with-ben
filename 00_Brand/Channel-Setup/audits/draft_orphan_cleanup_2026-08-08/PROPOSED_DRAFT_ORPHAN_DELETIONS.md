# Proposed Draft / Orphan Deletions

Generated: `2026-08-08T20:43:22.656Z`

**Stage A only — NO DELETIONS PERFORMED.**

## Summary counts

- Safe draft deletes (HIGH): **0**
- Safe orphan deletes (HIGH): **0**
- Safe confirmed duplicate deletes (HIGH): **0**
- Protected: **91**
- Historical duplicates protected: **63**
- Possible duplicates kept: **0**
- Unknown kept: **0**

## Proposed delete list

_None. No HIGH-confidence SAFE_TO_DELETE_* candidates under conservative rules._

## Rationale

- Prior Studio duplicate classification already marked EXACT/HIGH duplicates as KEEP_PRIVATE.
- Default for historical duplicates is HISTORICAL_DUPLICATE_PROTECTED (forensic + anti re-upload).
- Title+duration similarity alone is insufficient for SAFE_TO_DELETE_CONFIRMED_DUPLICATE.
- Explicit excluded/private assets (HvAKGjx4lv0, icedH_gK8JE, Web2otrTcT0, 1qts3tIsg9c, etc.) remain protected.
- Dead JWST parent 1wxUhF3XnwI retained as HISTORICAL_DUPLICATE_PROTECTED.
- No genuine unreferenced Studio Draft without a video ID was proven via API; Playwright discovery follows separately.
- Zero HIGH-confidence SAFE_TO_DELETE candidates under conservative rules.

## Recommendation

Do **not** proceed to Stage B unless you explicitly approve a non-empty HIGH-confidence delete list.
Visual clutter in Studio private leftovers is not sufficient grounds for deletion.
