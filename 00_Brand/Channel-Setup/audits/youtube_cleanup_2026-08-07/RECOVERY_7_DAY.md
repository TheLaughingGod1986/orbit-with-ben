# Orbit YouTube — 7-day stabilization plan

**Start:** 2026-08-07 (UK)  
**Goal:** Re-enter Shorts/Browse test buckets without duplicate-signal contamination.

## Rules (non-negotiable)

- Max **1 new public Short per day** (canonical scheduled go-lives count).
- **0** CDP reupload/replace jobs.
- **0** new long-form uploads this week (Alien/JWST stay on existing schedules only).
- After each go-live: verify **exactly one** public ID for that title fingerprint (API or oEmbed + Studio).
- Do not delete videos; keep holds on 31 Dec.

## Schedule

| Day | Date (UK) | Allowed publish | Action |
|-----|-----------|-----------------|--------|
| 0 | Thu 7 Aug | NF01 `tUAdhOnMW2g` @ 12:30 | Confirm only this ID goes public for “Time Appears…”. Pin + Related → `3xrxdmaOwJI`. |
| 1 | Fri 8 Aug | `svYOx07OrIM` @ 12:30 | Same finish checklist. No extras. |
| 2 | Sat 9 Aug | `B2STcIAF1lY` @ 12:30 | Same. |
| 3 | Sun 10 Aug | `w1ej9u0rPTA` @ 12:30 | Same. |
| 4–6 | 11–13 Aug | **No new BH Shorts** | Watch metrics. Alien long remains scheduled (do not pull forward). |
| 7 | ~13–14 Aug | Review | If any BH Short has impressions &gt; 0 → continue cadence. If all still 0 → Studio channel-status check + pause 48h before next long. |

## Monitoring checkpoints

| When | Check | Pass |
|------|-------|------|
| T+1h after each Short go-live | Studio: Public; Related set; no second public twin | Required |
| T+6h | Impressions &gt; 0 **or** views ≥ 1 | Soft |
| T+24h | Impressions &gt; 0 | Target |
| T+72h | At least one BH Short with views ≥ 10 | Strong signal channel re-entered seed |
| Daily | `videoCount` public and fingerprint audit | No surprise public IDs |

## Success indicators

1. Impressions &gt; 0 on at least one BH Short within 72h of clean shelf.  
2. CTR becomes measurable (any non-null CTR in Studio).  
3. No new duplicate public IDs created.  
4. Channel public count increases only via planned schedule (not replace scripts).

## If still 0 impressions after day 7

1. Confirm phone verification + Advanced features in Studio.  
2. Confirm no Community Guideline / limited features.  
3. Keep publishing **one** Short/day from next cluster only after OAuth force-ssl reconnect + API package path.  
4. Do **not** mass-reupload.

## Upload command (next episode)

```bash
cd 07_Content-Ops
npm run youtube:package -- \
  --package ../02_Video-Projects/<ep>/11_Upload-Package \
  --video ../02_Video-Projects/<ep>/09_Final-Export/<master>.mp4 \
  --schedule <ISO> \
  --dry-run
# then live, then Studio finish only
```
