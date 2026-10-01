# Production status — 021 Saturn Loses Its Rings

Updated **1 Oct 2026 evening** (Ben decisions 1–4; v03g assemble in progress).

> **Title note (Claude review):** `PLAN_2026-09-30.md` / VO may use **How Long Do Saturn's Rings Have Left?** while this file still listed *What Happens When Saturn Loses Its Rings?*. **NEEDS BEN** to lock which listing title ships — not changed here.

| Field | Value |
|-------|-------|
| Slug | What-Happens-When-Saturn-Loses-Its-Rings |
| Locked title | **How Long Do Saturn's Rings Have Left?** (Ben: Monday Short last line + card name this; long listing follows PLAN) |
| Air target | Sun 11 Oct 2026, 18:00 UK (normal publish) |
| Upload history | **Clean** — never uploaded or scheduled |
| Gate | **PASS** (`11_Upload-Package/EPISODE_GATE_v01.md`) |
| Script review | **90 / 100 PASS** (`01_Script/SCRIPT_REVIEW_v01.md`) |
| Script | **LOCKED 2026-09-26** — Ben final notes; do not rewrite without Ben OK |
| VO | **LOCKED** `02_Voiceover/parts/saturn_rings_vo_v03b_tightened_LOCK.wav` — **523.62 s (8:43.6)** |
| Shot list | **`shot_list_v03g.csv`** — Ben OK 1 Oct evening; from v03f with row 93 temp NASA PIA12633 until Omni. Checker PASS. Assemble first cut v02 from this list. |
| NASA pool | **Fetched yes** — `nasa_pool_v01.json` (153 entries) + local stills under `07_Edit-Project/nasa_pool_v01/`. Re-run `fetch_nasa_pool.py` only after Ben OKs v03e if any IDs still missing on disk for assemble. |
| First cut | **v02 delivered** — iCloud `OWB UAT/saturn_first_cut_v02/` (548.12 s · sha256 `90d18ded…` · contact12 + per-row). Row 93 temp PIA12633. |
| Thumbnails (long) | **ABC v02 ready for Ben pick** (no Orbit) — iCloud `OWB UAT/saturn_thumbs_v02/` (A ALREADY FALLING · B NOTHING LEFT sharper · C RAINING IN). Phone board = 16:9 row only. Not in git. |
| Runtime target | 8–9 min (locked VO 8:43.6 + end hold) |
| Subscribe line used | #4 — We make one of these every week. Subscribing is how the next one finds you. |

## AI / Goddard clips (as of v03e)

| Clip | Status |
|------|--------|
| `edit_ice_chunks_v07.mp4` (ice crowd open) | **Exists · in v03e row 1** (0–4.32 s). Treated as approved open in `NASA_POOL_v01.md`. No separate “edge fix done” note found in repo docs — Ben to confirm if a further edge pass was expected. |
| `veo_young_rings_v01.mp4` | **Exists · in v03e** (rows 4 + 74). Also `veo_approved_v03/veo_young_rings_v03.mp4` on disk (not the id in the list). |
| `veo_bare_saturn_v05.mp4` | **Exists · approved · in v03e** (rows 5 + 91) |
| `veo_orbit_tumble_v03_fallback_0-3s.mp4` | **Exists · approved 0–3 s only · in v03e row 22** as source **AI** (checker holds window) |
| `orbit_bare_omni.mp4` | **Missing · row 93 PENDING**. Vertex one-shot 1 Oct → 500 `api_error` (`04_Generated-Clips/omni_v03e_bare/OMNI_RETRY_v03e_bare.json`). Daily retry or Ben chooses Tue. |
| Goddard `SVS_12672_ring_rain.mp4` | **Local HD yes** · v03e rows 46 (22.6–28.2) + 50 (35.0–40.0), muted. No on-screen text on those stretches. |

## Shorts week (Mon 12 · Wed 14 · Fri 16)

| Day | Piece | Exists | Approved | Missing |
|-----|-------|--------|----------|---------|
| **Mon 12 Oct 11:30 UK** | Saturn tease — *Saturn's Rings Are Already Falling* | Script `10_Shorts/monday_saturn_tease/MONDAY_SATURN_SHORT_RINGS_ALREADY_FALLING.md` · VO wav/mp3 (~23.4 s) · plate render `monday_ring_rain_ITS_FALLING_v03e.mp4` + contact in iCloud | Last line re-recorded to name How Long… (`monday_saturn_short_vo_v02_how_long.wav`); plate OK'd | Full Short assemble still open (Orbit @1.5 s, 9–14 s card, loop). Orbit @~1.5 s (propose tumble 0–3 s). 9–14 s ice→equator + title card (propose PIA17150 / PIA08990). Loop ending + Short cover not locked. Related → Saturn long id after long uploads. |
| **Wed 14 Oct 11:30 UK** | *Could Orbit Survive…?* Jupiter | Uploaded **`buaOI3QGm7U`** · private · `publishAt` **2026-10-14T10:30:00Z** = **Wed 14 Oct 2026 11:30 BST** | Scheduled (do not touch) | — |
| **Fri 16 Oct 11:30 UK** | Black Dwarf / Last Star | Script `005_…/friday_2026-10-16_last_star/FRIDAY_LAST_STAR_SHORT_BLACK_DWARF.md` (62 words) · still `021_…/shorts_stills_v02/friday_black_dwarf_cooling_v02.png` | **Ben OK** on 62-word script (1 Oct evening) | VO / picture next; moving picture needs Ben OK before upload |

## Blockers

- [x] Topic Ben OK (Candidate A)
- [x] Pre-build audit filled (vidIQ fields pending Studio)
- [x] Script ≥ 90 + gate PASS — **LOCKED**
- [x] VO locked 8:43.6
- [x] Shot list v03e checker PASS (committed `056f847`) — **await Ben OK before assemble**
- [ ] Row 93 bare Orbit Omni (daily Vertex retry) **or** Ben Tue decision (18 Oct / PIA12633 once)
- [x] Ben OK on Fri Black Dwarf script; Mon last line re-recorded to How Long…
- [ ] Long thumb ABC Ben OK → Studio Test & Compare after upload
- [x] First-cut assemble v02 delivered to iCloud (Ben OK'd; contact12 + per-row)
