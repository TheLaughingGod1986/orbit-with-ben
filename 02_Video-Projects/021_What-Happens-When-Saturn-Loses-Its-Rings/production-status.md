# Production status — 021 Saturn Loses Its Rings

Updated **1 Oct 2026 16:54 London** (matches disk after `shot_list_v03e` @ `056f847`).

> **Title note (Claude review):** `PLAN_2026-09-30.md` / VO may use **How Long Do Saturn's Rings Have Left?** while this file still listed *What Happens When Saturn Loses Its Rings?*. **NEEDS BEN** to lock which listing title ships — not changed here.

| Field | Value |
|-------|-------|
| Slug | What-Happens-When-Saturn-Loses-Its-Rings |
| Locked title | What Happens When Saturn Loses Its Rings? |
| Air target | Sun 11 Oct 2026, 18:00 UK (normal publish) |
| Upload history | **Clean** — never uploaded or scheduled |
| Gate | **PASS** (`11_Upload-Package/EPISODE_GATE_v01.md`) |
| Script review | **90 / 100 PASS** (`01_Script/SCRIPT_REVIEW_v01.md`) |
| Script | **LOCKED 2026-09-26** — Ben final notes; do not rewrite without Ben OK |
| VO | **LOCKED** `02_Voiceover/parts/saturn_rings_vo_v03b_tightened_LOCK.wav` — **523.62 s (8:43.6)** |
| Shot list | **`shot_list_v03g.csv`** — Ben OK 1 Oct evening; from v03f with row 93 temp NASA PIA12633 until Omni. Checker PASS. Assemble first cut v02 from this list. |
| NASA pool | **Fetched yes** — `nasa_pool_v01.json` (153 entries) + local stills under `07_Edit-Project/nasa_pool_v01/`. Re-run `fetch_nasa_pool.py` only after Ben OKs v03e if any IDs still missing on disk for assemble. |
| First cut | **Not started** — wait for Ben OK on v03e before assemble v02 |
| Thumbnails (long) | **ABC v01 started** (no Orbit) — `08_Thumbnail/abc_v01_no_orbit/` + iCloud `OWB UAT/saturn_thumbs_v01/`. Not yet Ben-OK / not in Studio. |
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
| **Mon 12 Oct 11:30 UK** | Saturn tease — *Saturn's Rings Are Already Falling* | Script `10_Shorts/monday_saturn_tease/MONDAY_SATURN_SHORT_RINGS_ALREADY_FALLING.md` · VO wav/mp3 (~23.4 s) · plate render `monday_ring_rain_ITS_FALLING_v03e.mp4` + contact in iCloud | Script still marked draft for Ben OK; plate OK'd for render 1 Oct | Assemble not started. Orbit @~1.5 s (propose tumble 0–3 s). 9–14 s ice→equator + title card (propose PIA17150 / PIA08990). Loop ending + Short cover not locked. Related → Saturn long id after long uploads. |
| **Wed 14 Oct 11:30 UK** | *Could Orbit Survive…?* Jupiter | Uploaded **`buaOI3QGm7U`** · private · `publishAt` **2026-10-14T10:30:00Z** = **Wed 14 Oct 2026 11:30 BST** | Scheduled (do not touch) | — |
| **Fri 16 Oct 11:30 UK** | Black Dwarf / Last Star | Script `005_…/friday_2026-10-16_last_star/FRIDAY_LAST_STAR_SHORT_BLACK_DWARF.md` (62 words) · still `021_…/shorts_stills_v02/friday_black_dwarf_cooling_v02.png` | **Needs Ben OK** on script (alt draft 30 Sep) | VO / assemble / upload after Ben OK |

## Blockers

- [x] Topic Ben OK (Candidate A)
- [x] Pre-build audit filled (vidIQ fields pending Studio)
- [x] Script ≥ 90 + gate PASS — **LOCKED**
- [x] VO locked 8:43.6
- [x] Shot list v03e checker PASS (committed `056f847`) — **await Ben OK before assemble**
- [ ] Row 93 bare Orbit Omni (daily Vertex retry) **or** Ben Tue decision (18 Oct / PIA12633 once)
- [ ] Ben OK on Mon/Fri Short scripts where still draft
- [ ] Long thumb ABC Ben OK → Studio Test & Compare after upload
- [ ] First-cut assemble v02 — **only after Ben OKs v03e**
