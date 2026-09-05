# Scheduled Shorts — distribution risk audit

**Date:** Thu 3 Sep 2026 · ~17:10 UK  
**Trigger:** `FbRFvSApfOQ` (*Why Europa Is Hiding a Massive Ocean*) — **~2 views** in first ~5h vs **186** (*Star Recycling*, 29h) and **610** (*What Remains*, 2d).  
**Scope:** All **14** scheduled Shorts in Studio through **18 Sep** (Europa ×8 · Neutron ×5 · Last Star leftover ×1).  
**Packaging baseline:** VidIQ listings + `yellow_white_v04` thumbs + Related verified **3 Sep** (`audits/vidiq_optimize_2026-09-03/STATUS.json`).  
**Not a strike:** House bible (1 Sep Studio note) — dead Shorts = stacked stale ids + bad slotting, not penalty.

---

## Executive summary

| Verdict | Count | Meaning |
|---------|------:|---------|
| **FAIL — already spent** | 1 | `FbRFvSApfOQ` — live, ~zero feed; do not remint cut |
| **FAIL — fix before air** | 7 | Europa scheduled **today 20:00 → Wed 9 Sep** — stale **15 Aug** ids |
| **WARN — fix before air** | 5 | Neutron **10–14 Sep** — same stale-id risk + Thu **11:30 before Premiere** |
| **WARN — locked leftover** | 1 | `0j_pgYbCe5E` — expect cold start; bible says leave |

**Root cause (confirmed pattern):**

1. **Stale re-upload ids** — All eight Europa Shorts were uploaded **15 Aug 2026** as private scheduled assets (`cfr_reupload_at` in `SHORTS_UPLOAD_INDEX.json`). YouTube often suppresses ids indexed weeks before go-live. Working comparators this week (`n2WbOfJhOwc`, `9lLZMy8rBJo`) are **fresh Sep uploads**, not in the Aug batch.
2. **Pre-Premiere Thu 11:30 slot** — Short goes public while Related long is still a **Premiere wait** (Europa until **18:00** tonight; Neutron **10 Sep 18:00**). Hurts funnel + feed.
3. **Orbit-first open** — Only **`FbRFvSApfOQ`** (punch-01) — locked no remint; extra penalty on top of 1 + 2.
4. **Wrong punch in wrong slot** — Strongest Europa hook (`eVp9a7f4rWg`) is correctly at **20:00**, but the **weakest** Orbit-first punch opened the week at **11:30**.

**Fix for every still-scheduled Short:** **fresh-id supersede** (new upload → parity listing/thumb/Related → exact schedule → demote old id private). Do **not** swap files on an existing id. Studio finish only (Related pill — no API).

---

## Risk matrix (all scheduled Shorts)

| # | Live id | Title | Air UK | Related long | Long public when Short airs? | Stale id (15 Aug batch) | Open | Slot issue | Risk | Action |
|---|---------|-------|--------|--------------|------------------------------|-------------------------|------|------------|------|--------|
| 1 | `FbRFvSApfOQ` | Why Europa Is Hiding a Massive Ocean | **3 Sep 11:30** ✓ LIVE | `NbW5G1BpPY0` | **No** (Premiere 18:00) | Yes · `2Hslb_wz3YU` | **Orbit-first** | Pre-Premiere + wrong punch | **FAIL spent** | Leave public; no remint; monitor only |
| 2 | `eVp9a7f4rWg` | We Could Kill the Life We're Looking For | **3 Sep 20:00** | `NbW5G1BpPY0` | **Yes** (after 18:00) | Yes · `gN2qAv8m9Wc` | Picture-first | None — correct launch slot | **FAIL fix** | **P0 fresh-id replace before 20:00** |
| 3 | `8Bym-yrYhGc` | Why Europa's Ocean Shouldn't Exist | 4 Sep 11:30 | `NbW5G1BpPY0` | Yes | Yes · `EcsunqhN0jQ` | Picture-first | None | **FAIL fix** | P1 fresh-id replace before Fri |
| 4 | `1glQuYFSaYQ` | What Would Life Eat Under Europa? | 5 Sep 11:30 | `NbW5G1BpPY0` | Yes | Yes · `k0PjH2I0OxY` | Picture-first | None | **FAIL fix** | P1 fresh-id replace before Sat |
| 5 | `Xza_jSHD4qw` | Deep-Sea Vents Feed Life With No Sunlight | 6 Sep 11:30 | `NbW5G1BpPY0` | Yes | Yes · `0eqTVgrlU-s` | Picture-first | None | **FAIL fix** | P1 fresh-id replace before Sun |
| 6 | `VE0f186WQZo` | Europa Sprays Its Ocean Into Space | 7 Sep 11:30 | `NbW5G1BpPY0` | Yes | Yes · `Fv-lSwB_Z-o` | Picture-first | None | **FAIL fix** | P1 fresh-id replace before Mon |
| 7 | `D3KSYrqip5A` | Why We Are Heading to Europa Right Now | 8 Sep 11:30 | `NbW5G1BpPY0` | Yes | Yes · `KPO68c-U42E` | Picture-first | None | **FAIL fix** | P1 fresh-id replace before Tue |
| 8 | `TE_HDKAnqms` | If Life Starts Under Ice, It's Everywhere | 9 Sep 11:30 | `NbW5G1BpPY0` | Yes | Yes · `Vby0Tal8Z_w` | Picture-first | None | **FAIL fix** | P1 fresh-id replace before Wed |
| 9 | `92vmMxSNmlk` | Why You Can't Stand on a Neutron Star | **10 Sep 11:30** | `Yk1tLh23rko` | **No** (Premiere 18:00) | **Verify Studio** | Picture-first (assumed) | Pre-Premiere Thu slot | **WARN fix** | P2 fresh-id + **skip or move** Thu 11:30 |
| 10 | `vCxXTYXSSqY` | The Weight of a Mountain in Your Hand | 11 Sep 11:30 | `Yk1tLh23rko` | Yes | Verify Studio | Picture-first | None | **WARN fix** | P2 fresh-id if uploaded pre-1 Sep |
| 11 | `va5ATScn3rs` | The Sky Would Lean Near a Neutron Star | 12 Sep 11:30 | `Yk1tLh23rko` | Yes | Verify Studio | Picture-first | None | **WARN fix** | P2 fresh-id if stale |
| 12 | `o7ykyTDZKiE` | Your Last Clear Image Near a Neutron Star | 13 Sep 11:30 | `Yk1tLh23rko` | Yes | Verify Studio | Picture-first | None | **WARN fix** | P2 fresh-id if stale |
| 13 | `Rp_8J6_6IIk` | What Happens If You Touch a Neutron Star? | 14 Sep 11:30 | `Yk1tLh23rko` | Yes | Verify Studio | Picture-first | None | **WARN fix** | P2 fresh-id if stale |
| 14 | `0j_pgYbCe5E` | Why the Solar System Is Bigger Than You Were Taught | 18 Sep 11:30 | `REXYxuLOBoI` | Yes (old week) | Verify Studio | Picture-first | **Off-week leftover** | **WARN leave** | Bible lock — do not remint |

**Packaging (all 14):** Titles · descriptions · tags · Related · thumbs — **PASS** per 3 Sep audit. Problem is **distribution mechanics**, not listing copy.

---

## Standard fix — fresh-id supersede (one Short)

Run on **Mac mini** in desktop Studio (Chrome CDP `:9222`). **Never** use CDP to upload/replace video files — upload in Studio UI only.

### Before you start

- [ ] Confirm mp4 on disk (probe duration **22–27s**; abort if ≥40s).
- [ ] Listing copy: `audits/vidiq_optimize_2026-09-03/SHORTS_LISTING_UPDATES.json`.
- [ ] Cover: `10_Shorts/08_Thumbs/yellow_white_v04/cover_<OLD_ID>.jpg` (reuse art; new id gets same file).
- [ ] Related target from table above.
- [ ] **Demote old id first** if it is already public; for scheduled, unschedule old → private **before** new id goes public.

### Steps (per Short)

1. **Studio → Create → Upload Short** — select canonical mp4 from `10_Shorts/06_Final-Exports/` (paths in `SHORTS_UPLOAD_INDEX.json` for Europa).
2. **Listing** — paste title, description, tags from `SHORTS_LISTING_UPDATES.json` (exact strings; zero `/go/`).
3. **Thumbnail** — Upload custom cover from `yellow_white_v04/` (image only; not “Select from video”).
4. **Related video** (desktop Studio) → that week’s Thursday long only. **Save.**
5. **Visibility** — Schedule as public at **exact** UK time from table (do not change dates while saving thumb).
6. **Made for kids** — Not made for kids.
7. **Old id** — Remove schedule → **Private** (no `publishAt`). Do **not** delete. Add old id to `historical_duplicate_ids` in `SHORTS_UPLOAD_INDEX.json`.
8. **Registry** — Update `SHORTS_UPLOAD_INDEX.json` with new `youtube_video_id`, `url`, drop `disk_only`, note `superseded_<date>`.
9. **Verify** (read-only):
   ```bash
   uv run --with playwright python scripts/_verify_shorts_seo_listings.py
   uv run --with playwright python scripts/_verify_shorts_dates.py
   ```
10. **Social** — After YouTube public: one unique mirror per platform (`orbit-social-no-duplicates.mdc`). TikTok paused.

### Europa mp4 map (Mac paths)

| Punch | File under `006_.../10_Shorts/06_Final-Exports/` |
|-------|-----------------------------------------------------|
| 01 | `europa_punch-01_ocean-we-cannot-see_v03_diamond.mp4` |
| 02 | `europa_punch-02_cold-should-win_v02_diamond.mp4` |
| 03 | `europa_punch-03_what-would-life-eat_v02_diamond.mp4` |
| 04 | `europa_punch-04_no-daylight-kitchen_v02_diamond.mp4` |
| 05 | `europa_punch-05_sample-without-drilling_v02_diamond.mp4` |
| 06 | `europa_punch-06_clipper-on-its-way_v02_diamond.mp4` |
| 07 | `europa_punch-07_do-not-contaminate_v02_diamond.mp4` |
| 08 | `europa_punch-08_life-under-ice_v02_diamond.mp4` |

Neutron exports: confirm on Mac under `007_.../10_Shorts/06_Final-Exports/` (not in cloud clone).

---

## Per-video fix plan

### 1 · `FbRFvSApfOQ` — **LEAVE (spent opener)**

| Field | Value |
|-------|-------|
| Status | **Public** since 3 Sep 11:30 |
| Problems | Stale id + Orbit-first + pre-Premiere — all three |
| Fix | **None.** House lock: cut is Orbit-first — **no remint**; thumb-only was allowed |
| Expect | May pick up a trickle after Europa Premiere **18:00**; do not reorder week around it |

---

### 2 · `eVp9a7f4rWg` — **P0 · FIX BEFORE 20:00 UK TONIGHT**

| Field | Value |
|-------|-------|
| Role | Europa **launch** Short (correct slot) |
| Problems | Stale **15 Aug** id — same suppression risk as `FbRFvSApfOQ` |
| Fix | **Fresh-id supersede** (playbook above) **before 20:00** |
| Priority | This is the real Europa week opener — monster hook, picture-first, long public after 18:00 |
| After | Privatize `eVp9a7f4rWg`; add to `historical_duplicate_ids` |

---

### 3–8 · Europa daily (`8Bym` → `TE_HDK`) — **P1 · FIX BEFORE EACH AIR DATE**

All seven share the **15 Aug stale id** problem. Picture-first cuts; parent long public — **lower risk than FbRF** but still likely suppressed vs fresh ids (compare Star Recycling).

| Old id | Air | Supersede deadline |
|--------|-----|-------------------|
| `8Bym-yrYhGc` | Fri 4 Sep 11:30 | Before Fri morning |
| `1glQuYFSaYQ` | Sat 5 Sep 11:30 | Before Sat morning |
| `Xza_jSHD4qw` | Sun 6 Sep 11:30 | Before Sun morning |
| `VE0f186WQZo` | Mon 7 Sep 11:30 | Before Mon morning |
| `D3KSYrqip5A` | Tue 8 Sep 11:30 | Before Tue morning |
| `TE_HDKAnqms` | Wed 9 Sep 11:30 | Before Wed morning |

**Batch option:** One Studio session **Thu evening after Premiere** — supersede all seven in order; schedule unchanged.

**Do not** point Related at leftover private ids (`EcsunqhN0jQ` … `gN2qAv8m9Wc`).

---

### 9 · `92vmMxSNmlk` — **P2 · NEUTRON THU UPCOMING**

| Field | Value |
|-------|-------|
| Problems | (a) Pre-Premiere Thu **11:30** — same failure mode as `FbRFvSApfOQ`. (b) Possible stale id — **check Studio upload date**. |
| Recommended fix | **Option A (preferred):** Cancel Thu 11:30 — leave private/unscheduled. First Neutron Short = **Fri 11:30** `vCxXTYXSSqY` after long is public. **Option B:** Fresh-id supersede **and** move to **Fri 11:30**, shift rest +1 day (only if Ben wants daily cadence). |
| Add | Schedule **`Rp_8J6_6IIk`** (score **96**, strongest hook) at **Thu 10 Sep 20:00** launch — currently **missing** (checklist gap). Fresh upload. |

---

### 10–13 · Neutron daily — **P2 · VERIFY THEN SUPERSEDE IF STALE**

In Studio → each id → **Details → Upload date**. If uploaded **before 1 Sep 2026** or sitting scheduled since Aug:

- Fresh-id supersede before air date.
- Related → `Yk1tLh23rko` only.
- Covers in `007_.../10_Shorts/08_Thumbs/yellow_white_v04/`.

| Old id | Air |
|--------|-----|
| `vCxXTYXSSqY` | Fri 11 Sep 11:30 |
| `va5ATScn3rs` | Sat 12 Sep 11:30 |
| `o7ykyTDZKiE` | Sun 13 Sep 11:30 |
| `Rp_8J6_6IIk` | Mon 14 Sep 11:30 **or move to Thu 10 Sep 20:00 launch** |

---

### 14 · `0j_pgYbCe5E` — **LEAVE (locked leftover)**

| Field | Value |
|-------|-------|
| Air | 18 Sep 11:30 |
| Related | `REXYxuLOBoI` (Last Star — off-week by design) |
| Bible | Locked date + Related; thumb rebuilt; **do not remint** |
| Expect | Cold performance (leftover pattern). Accept or Ben explicitly lifts lock |

---

## Cadence fix (going forward)

| Rule | Old habit | New lock |
|------|-----------|----------|
| Upload timing | Batch private uploads **weeks ahead** (15 Aug) | Upload fresh id **≤48h before** `publishAt` |
| Thu morning | 11:30 Short **before** Premiere | **Skip** pre-Premiere Short OR accept as low-impression promo only |
| Thu evening | Launch Short after long | **Required** — strongest hook, fresh id, **20:00** |
| Week opener | Weakest / legacy punch | **Never** put Orbit-first or stale punch first |
| Supersede | Keep same id | Fresh id + privatize old (`orbit-shorts-punch-first.mdc`) |

Update `EUROPA_SHORTS_STUDIO_CHECKLIST.md` after first supersede with new ids.

---

## Verification checklist (after fixes)

| Check | How |
|-------|-----|
| Impressions | Studio Analytics → Reach → **Shorts feed** (target: non-zero in first 24h) |
| Related | Desktop Studio field → correct Thursday id |
| Duration | `ffprobe` ≤27s |
| Registry | `SHORTS_UPLOAD_INDEX.json` matches live ids |
| 48h funnel | `SHORTS_FUNNEL_CHECK_2026-09-05.md` — log views + traffic source |

**Review gate:** Europa week **10 Sep** (house bible) — compare cluster vs Last Star with these fixes applied.

---

## Priority queue (Mac mini tonight)

1. **Now → 18:00** — Europa long Premiere `NbW5G1BpPY0` (no Short work).
2. **18:00 → 19:30** — **P0** Supersede `eVp9a7f4rWg` → fresh id, schedule **20:00** exactly.
3. **Same session (optional)** — Batch supersede Europa **Fri–Wed** seven ids.
4. **Before 10 Sep** — Neutron: skip or move `92vmMxSNmlk`; add **Thu 20:00** launch; supersede if stale.

---

## References

- `02_Video-Projects/006_.../10_Shorts/SHORTS_UPLOAD_INDEX.json`
- `02_Video-Projects/006_.../10_Shorts/EUROPA_SHORTS_STUDIO_CHECKLIST.md`
- `00_Brand/Channel-Setup/audits/vidiq_optimize_2026-09-03/SHORTS_LISTING_UPDATES.json`
- `00_Brand/Channel-Setup/ORBIT_HOUSE_AND_UAT_BIBLE.md` (dead Shorts pattern · `FbRFvSApfOQ` lock)
- `.cursor/rules/orbit-shorts-punch-first.mdc` (replace rule)
- `.cursor/rules/orbit-shorts-related-video.mdc`
