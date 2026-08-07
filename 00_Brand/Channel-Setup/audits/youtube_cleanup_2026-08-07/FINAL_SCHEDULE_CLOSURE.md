# Final Schedule Closure

Generated: `2026-08-07T16:10:00Z` (approx)

## Verdict

**SCHEDULE APPLICATION FAILED**

Calendar was **not** applied. Channel left on the prior live schedule (16 IDs with superseded dates). No new uploads, deletes, or public-canonical changes.

---

## What ran

1. BEFORE snapshot written (`FINAL_SCHEDULE_APPLY_BEFORE.*`)
2. Pre-apply shelf verify: **PASS** (6/6 public canonicals, `unexpectedPublic=[]`, `escalateNow=false`)
3. Dry-run of `youtube:final-schedule-closure`: **PASS** (13/13 projected)
4. Live execute attempted with `--allow-emergency-unfreeze --execute`

---

## HvAKGjx4lv0 repair

| Field | Value |
|-------|-------|
| Before | `unlisted` / `publishAt=null` |
| `videos.update` response | `privacyStatus=private` (HTTP 200) |
| Immediate / concurrent `videos.list` | Oscillated `private` ↔ `unlisted` (split reads in parallel) |
| Sustained write campaign | ~90s; never reached 8/8 private samples |
| Gate at apply time | **FAIL** → batch stopped before any of the 13 schedule updates |
| Later single read (post-campaign) | briefly `private` / `null` once before quota hard-stop |
| publishAt | remained `null` throughout |

**PASS / FAIL:** **FAIL** (could not meet stable `videos.list` confirmation of `private` + `publishAt=null` before schedule apply)

Root cause (observed): YouTube Data API returns successful private updates for `HvAKGjx4lv0`, but `videos.list` continues to return a mix of `unlisted` and `private` for the same ID. Not a local registry bug. Not CDP. No second mutator found in Content Ops workers.

---

## Quota

Sustained verification writes/reads exhausted the YouTube Data API daily quota (`403 quotaExceeded`). Further apply/verify is blocked until quota resets (typically Pacific midnight).

---

## Public shelf (last successful pre-apply check)

| ID | State |
|----|-------|
| `Mo93x0fxB1Q` | public (Fermi long) |
| `1HuV8o3gOss` | public (Fermi Short) |
| `KcKBixwmcV4` | public (Fermi Short) |
| `3xrxdmaOwJI` | public (BH long) |
| `JRfhE6yWom4` | public (BH Short) |
| `L2OFjL4neOo` | public (BH Short) |

Shelf verify before repair attempt: **PASS**

---

## Applied schedule

**None.** Expected 13 slots were not written.

Live still carries the **previous** applied calendar on existing IDs (including Aug 8–9 BH Shorts and Fri-start Exo/JWST), which the revised proposal was meant to supersede.

---

## Excluded assets (intent unchanged)

| ID | Intent | Live note at stop |
|----|--------|-------------------|
| `HvAKGjx4lv0` | private + unscheduled | unstable list privacy; publishAt null |
| `icedH_gK8JE` | private + unscheduled | was private/null pre-apply |
| `Web2otrTcT0` | private + unscheduled | was private/null pre-apply |
| `1qts3tIsg9c` | private + unscheduled | was private/null pre-apply |
| `dPMJQp2gMNc` | private + unscheduled | was private/null pre-apply |
| `rFJoOdQAc9c` | private + unscheduled | was private/null pre-apply |
| `w1ej9u0rPTA` | BH_SHORT_HELD_FOR_LATER | still had prior `publishAt` (Aug 11) — clear pending |
| `gPCpMsB0w2E` | private + unscheduled | still had prior `publishAt` — clear pending |
| `YsyPMhNmHMk` | private + unscheduled | still had prior `publishAt` — clear pending |

---

## Duplicate / schedule health

| Check | Result |
|-------|--------|
| scheduled = 13 (revised) | **not applied** |
| public duplicates | none observed pre-apply |
| new IDs created | **0** |
| re-uploads | **0** |
| deletes | **0** |
| placeholder 31 Dec | **0** (not reintroduced) |

---

## Manual actions remaining

1. Wait for YouTube Data API **quota reset**.
2. Re-fetch `HvAKGjx4lv0` with multi-sample confirmation until stably `private` + `publishAt=null` (or escalate to Studio-only visibility fix if API remains split-brain).
3. Re-run:
   `cd 07_Content-Ops && npm run youtube:final-schedule-closure -- --allow-emergency-unfreeze --execute`
4. Then run shelf-verify / recovery-status / verify-oauth and tests.
5. Update `youtube-shelf-verify.ts` NF01 expected `publishAt` to `2026-08-10T10:30:00Z` only after revised calendar is live.

Do **not** schedule `w1ej9u0rPTA` on 9 Aug. Do **not** use CDP to compensate.

---

## Final recommendation

Leave the channel untouched until quota recovers and the Hv visibility gate can pass. Do not flood mutations. Do not apply the 13-slot calendar until `HvAKGjx4lv0` is confirmed private + unscheduled on stable `videos.list` reads.

First intended BH Short after a successful future apply remains:

**Monday 10 August 2026 · 12:30 Europe/Paris · `tUAdhOnMW2g`**
