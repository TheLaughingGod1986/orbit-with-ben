---
description: VidIQ is mandatory source of truth for Orbit listings (longs + Shorts)
alwaysApply: true
---

# Orbit YouTube — VidIQ optimization path (mandatory)

**VidIQ is the source of truth** for packaging every Orbit upload: long-form **and** Shorts. Do not lock or ship a listing from gut feel alone.

## When this applies

- **New episode creation** (pre-build → upload → Studio finish)
- **Legacy / already-uploaded** videos (backfill the same path)
- **Reuploads** (e.g. normal-speed replacement) — optimize the **live** YouTube ID, not private duplicates
- Shorts, micros, and related-cluster items in each episode’s `SHORTS_UPLOAD_INDEX.json`

## Required path (every video)

### A. Research (VidIQ MCP)

1. `vidiq_balance` — note credits before/after
2. `vidiq_keyword_research` — primary + secondary (country `GB` unless strategy says otherwise)
3. `vidiq_score_title` / `vidiq_generate_titles` — long: `type=long`; Shorts: `type=short`
4. `vidiq_score_thumbnail` — current thumb; score ABC candidates when URLs/assets available
5. Optional: `vidiq_outliers`, `vidiq_generate_thumbnail` (22 credits) when house thumbs are weak or missing — **long = picture + SEA-style hook (no Orbit)**; Short = custom picture **no Orbit**; wonder brand; do not ship fearbait comps
6. Optional refine: `vidiq_refine_thumbnail` after a first VidIQ or house generate

### B. Decide (maximize score + brand)

| Surface | Target | Rules |
|---------|--------|-------|
| Title | ≥ **90**, prefer **95–98+** | Keep Orbit voice / `Orbit's Cosmic Journey` on longs. **Reject** fearbait/conspiracy even if score is higher |
| Description | Primary keyword in **first ~100 chars** | Chapters on longs; Shorts: punch + soft funnel to long URL |
| Tags | Fill toward **500** | VidIQ-backed terms only; drop weak generics (`fun facts`, `fall asleep fast`, etc.) |
| Thumbnails | Score ≥ house baseline | **Longs:** picture + SEA-style hook, **no Orbit**, no generic CTA — Studio **Thumbnail only** or **Title and thumbnail** A/B/C (3 distinct variants). **Shorts:** custom picture cover **no Orbit** — optimize cover/title/tags via VidIQ scores |
| Schedule | Channel cadence | Long Thu **19:00** UK; Shorts per `PUBLISHING_AND_SHORTS_STRATEGY.md` / `OPTIMAL_PUBLISH_SCHEDULE.json` — adjust only when VidIQ + cadence agree |

### C. Apply (live ID)

1. Update package files: `Titles/`, `Tags/`, `Descriptions/`, thumb assets under `08_Thumbnail/`
2. Write audit under `11_Upload-Package/Schedule/vidiq_optimize_YYYY-MM-DD/` (`vidiq_raw.json`, `STATUS.json`)
3. Push to YouTube (Data API where scoped; else Studio). Confirm on public watch page / Studio counter — not VidIQ cache alone
4. Longs: start or refresh **A/B/C** Test & Compare after custom thumbs exist
5. If Studio shows **Verify that it's you**, pause for human Verify, then resume — do not mark done without Save confirmed

### D. Shorts-specific

- Score **short** titles; lead with search/hook language under ~40–60 chars when possible
- Tags + description every Short (not long-only)
- Related video pill → that week’s Thursday long only; **no new Short pins**; pin not required when Related is set (see `orbit-shorts-related-video.mdc`)
- Prefer one strong **picture** cover frame (**no Orbit**); use `vidiq_generate_thumbnail` only if cover is weak and house assets missing

## New-video creation gate

Do **not** mark upload-ready until:

- [ ] Pre-build audit filled (`PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md`)
- [ ] Title ABC scored; winner locked in `Titles/`
- [ ] Description + tags written from VidIQ keywords
- [ ] Thumb A/B/C produced (house and/or VidIQ generate) and scored when possible
- [ ] After upload: listing applied to **live** ID + long-form ABC started
- [ ] Shorts cluster titles/tags scored and applied

Playbook: `00_Brand/Channel-Setup/VIDIQ_LISTING_OPTIMIZATION_PLAYBOOK.md`  
Batch helper: `00_Brand/Channel-Setup/audits/_vidiq_optimize_listing_batch.py`

## Brand non-negotiables (override raw score)

Wonder over dread · no conspiracy · Orbit DNA · British VO lock · cutscene no-reuse rules still apply.
