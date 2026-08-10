# SHORTS_VISIBILITY_ROOT_CAUSE

Generated: 2026-08-10T12:42:21.545253+00:00

## Primary question

Why do so many Studio Shorts appear Private while only a handful look Public?

## Proven causes (multi-factor)

### A. Scheduled holds look private in API / sometimes in list filters

Future approved Shorts are stored as `privacyStatus=private` + `publishAt`.
Studio Shorts tab correctly shows many as **Scheduled**, but the Private filter and raw API both look “private”.

Evidence: `PRE_REPAIR_SCHEDULE.json` — 12 scheduled IDs including 10 Shorts; live `publishAt` matches approved calendar.

### B. Catalogue repair deliberately kept duplicates private

Aug 7 smooth-canon / cleanup privatized superseded uploads (`old_video_id`, `previous_video_id`, `smooth_cfr_*`, `historical_duplicate_ids`) so one canonical wins.

Evidence: episode `SHORTS_UPLOAD_INDEX.json` historical_duplicate_ids + `FINAL_RECONCILIATION_MUTATION_LOG.json` KEEP_PRIVATE patterns.

### C. 16→13 schedule reduction left unique assets private on purpose

Obsolete IDs `w1ej9u0rPTA`, `gPCpMsB0w2E`, `YsyPMhNmHMk` were **removed from the approved calendar** (`FINAL_16_TO_13_RECONCILIATION.json` · `obsoleteClassification=REMOVED_FROM_APPROVED_SCHEDULE`).

These are UNIQUE content that must remain private until explicitly re-approved — **not** overdue.

### D. Accidental-early uniques intentionally re-privatized

`dPMJQp2gMNc`, `rFJoOdQAc9c` — KEEP_PRIVATE after early public; must not be auto-republished.

### E. Reserves / legacy holds

`HvAKGjx4lv0`, `icedH_gK8JE`, exo reserves, old JWST cluster — production `reserve=true` or CDP hold to Dec 31 / private.

### F. Studio list chip bug (new finding this run)

For `z-DLqoSoEBo` and `UWwNKYf_aU8`, Content → Shorts list labeled **Private** while video edit + Data API show **Public**.

This can make the catalogue look “healthier” (only 5 Public) than API reality (7 Public Shorts).

Root cause of the **chip mismatch**: `STUDIO_LIST_VISIBILITY_CHIP_STALE_OR_MISLABELED` (UI). Not a publishing-plan failure.

## Overdue canonical failure?

```text
NO_OVERDUE_CANONICAL_FAILURE
```

expected public by now = 5 · correctly public = 5 · overdue repaired = 0

## Did cleanup scripts demote the wrong copies?

For the five approved public Shorts: **No** — they remain public.

For two superseded Fermi-era uploads (`z-DLqoSoEBo`, `UWwNKYf_aU8`): they remain public when they were expected to stay/be private after replacement. That is an **incomplete privatize** of superseded IDs, not a missed publish of canonicals.

```text
ROOT_CAUSE_FOR_PRIVATE_VOLUME: INTENTIONAL_DUPLICATE_AND_HOLD_POLICY + SCHEDULED_HOLDS
ROOT_CAUSE_FOR_UNEXPECTED_PUBLIC_SUPERSEDED: INCOMPLETE_SUPERSEDED_PRIVATIZE (UI list also mislabels them Private)
ROOT_CAUSE_UNCONFIRMED: none for overdue path — overdue path confirmed empty
```
