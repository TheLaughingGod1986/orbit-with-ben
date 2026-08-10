# Final Shorts Forensic Report

Generated: `2026-08-10T11:55:29.774Z` · **READ-ONLY · ZERO LIVE MUTATIONS**

## Verdict

```text
SHORTS CATALOGUE HEALTHY — OPTIONAL CLEANUP AVAILABLE
```

## Protected catalogue

- Public (live): **7** (baseline 6 + natural schedule publishes; unexpected **0**)
- Remaining scheduled exact: **12/12**
- Missing scheduled: **0**
- Unexpected scheduled: **0**
- Schedule diff: **[]**
- Collisions: **0** · Placeholders: **0**
- Note: `tUAdhOnMW2g` published on schedule (Mon 10 Aug) — expected calendar progression, not drift.

## Studio Shorts

- Total discovered (full Shorts tab scroll): **30**
- Full-tab labels: {"total":30,"Draft":4,"Private":13,"Scheduled":10,"Public":3,"Unknown":0,"withVideoId":26,"withoutVideoId":4}
- Draft filter (Shorts): **15**
- Videos-tab Draft filter: **0**
- Private unscheduled (API-reconciled): **30**

## Reconciliation

- Studio+API: **41**
- Studio only: **0** 
- API-only shorts-length not in Studio list sample: **30**

## Why previous audit said Drafts = 0

**WRONG_STUDIO_TAB_FILTER** — Draft filter on Content → Videos (/videos/upload) is empty, but Content → Shorts (/videos/short) has Draft rows. Shorts drafts are tab-scoped.

See `AUDIT_FAILURE_ROOT_CAUSE.md`. Local audit logic fixed + regression tests added.

## Phase 10 answers

1. **Are private Shorts intentional historical/superseded uploads?** Yes, predominantly — registry historicalDuplicateIds + prior EXACT_DUPLICATE classifications.
2. **Any canonical future Shorts accidentally Private instead of Scheduled?** No — remaining approved Shorts retain correct publishAt.
3. **Any scheduled Shorts missing?** No.
4. **Any Shorts represented twice in the active schedule?** No collisions.
5. **Are any Drafts abandoned upload attempts?** Studio Draft rows mostly wrap existing private uploads via `udvid` (duplicate/superseded), not empty new IDs.
6. **Are any Drafts required for future publishing?** No — publishing uses approved scheduled video IDs, not these Draft rows.
7. **Any Private videos safe cleanup candidates?** Optional later — none proposed as HIGH-confidence delete in this pass (KEEP_PRIVATE policy).
8. **Is the publishing pipeline healthy?** Yes for the protected 13-slot calendar.

## Cleanup

HIGH-confidence safe-delete: **0** · KEEP_PRIVATE: **19** · INVESTIGATE: **11**

See `PROPOSED_SHORTS_CLEANUP.md`.

## Channel safety

Live mutations / visibility / schedule / deletes / uploads / new IDs: **all 0**.
