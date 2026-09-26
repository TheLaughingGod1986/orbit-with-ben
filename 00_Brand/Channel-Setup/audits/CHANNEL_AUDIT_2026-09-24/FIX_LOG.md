# Channel audit fix log — 24 Sep 2026

## Retire Andromeda leftovers (26 Sep 2026) — **merged to main**

Eleven private, unscheduled, 0-view Andromeda Shorts (uploaded 19 Sep) marked **`retired`** in `audits/shorts_open_library/library.json`. **Nothing deleted. No Studio changes.** Landed on main as squash commit `346d3938ee2b3c80e60cb608ffa99a19fa5384e9` ([PR #85](https://github.com/TheLaughingGod1986/orbit-with-ben/pull/85)) so the Mac mini and every cloud agent share the same gate list.

| id | result |
|---|---|
| `H5_NNc4NerQ` | added as retired |
| `E9xOElWqdrw` | added as retired |
| `_UF-SIUTWhY` | added as retired |
| `7YFfY4MdB6c` | added as retired |
| `NQM6gmGl6T4` | added as retired |
| `k7s_ZAx51xA` | added as retired |
| `_ggpawFj1ms` | added as retired |
| `Mub_GCIVmjY` | added as retired |
| `K63TbhGNnOY` | added as retired |
| `Dg9BWDmLSYo` | added as retired |
| `GrT3wO_bdEU` | added as retired |

## Prepared, not applied (25–26 Sep 2026) — thumbnail branch

Studio / live YouTube were **not** touched for thumbs or titles. No deletes.

### Thumbnail refresh (see `../THUMBNAIL_TITLE_AUDIT_2026-09-25/REFRESH_LOG.md`)

- Batch A Shorts: 2 built (`9lLZMy8rBJo`, `CkSECfUfH2Y`); 6 **NEEDS PLATE**.
- Batch B longs: variants built; **apply mode = swap** for every long (T&C not available on `Yk1tLh23rko`; Jupiter Ineligible until public). Swap picks: Neutron **B**, Last Star **B**, Europa **B**, Black Hole **B** (after plate), Fermi **C**, Andromeda **REP WHEN THEY MEET**.
- Baselines (28 Aug–24 Sep Studio) in REFRESH_LOG with **swap date** / **day-14 CTR** columns (blank until Ben applies).
- Contact sheets page 1–2 mark each row `APPLY: SWAP` and yellow-border the pick.
- Left alone: `2fsQcea-voM`, `ziKBPJ6FY0U`, `b8-X_FyJnHM`.

### Titles (propose only — Ben approves before save)

| id | options | applied? |
|---|---|---|
| `P9Jiw-MwUEU` | (1) Is Andromeda Already in Our Sky? · (2) Andromeda Is Already Getting Bigger | no |
| `xQlV9G9lqLI` | (1) Stars Almost Never Hit When Galaxies Collide · (2) Why Stars Don't Crash When Galaxies Meet | no |
| `68uTDP2esso` | note only: The Early Universe Is Hiding a Massive Secret | no |

### Studio fix list from AUDIT.md §4

| # | item | status |
|---|---|---|
| 1 | Andromeda long retitle | not applied |
| 2–3 | scheduled Short retitles in `STUDIO_FIXES.json` | not applied |
| 4 | Andromeda thumb → WHEN THEY MEET | **file prepared**, not uploaded |
| 5–6 | Andromeda Short retitles | **2 options each**, propose only |
| 7 | phone sound check of Andromeda Shorts | not done here |

### Captions (backlog #4)

Jupiter and Andromeda locked VO scripts **not in this checkout** — caption txts not produced. See `captions/README.md`.

### Jupiter pinned comment (backlog #1)

Proposed final in `REFRESH_LOG.md` / `PINNED_COMMENTS.json`. `commentId` empty until `--create` after public.

### Shorts sweep

Graded other public Shorts; failures in `REFRESH_LOG.md` / `refresh/sweep/SWEEP_GRADE.json`. **Not built.**
