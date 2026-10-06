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

## Thumbnail refresh (25–26 Sep 2026) — see `../THUMBNAIL_TITLE_AUDIT_2026-09-25/REFRESH_LOG.md`

- **v02 (26 Sep):** rebuilt on Studio plate picks (`orbit-thumb-plates/picks/`). Full-bleed; no black scrub box; no ghost text. Builder `build_thumb_refresh_v02_plates.py`. v01 scrubbed builds discarded.
- Batch A Shorts: 6 built (`PV50PX-bE4g`, `M-VN84HCNls`, `68uTDP2esso`, `SC2WGTl_V5Q`, `9lLZMy8rBJo`, `CkSECfUfH2Y`); **NEEDS PLATE** only `DN4L1DkerMM` + `l1d1ypHxLk0` (burned-in captions).
- Batch B longs: all B/C (and Andromeda REP) built on pick plates including Black Hole. Swap picks: Neutron **B**, Last Star **B**, Europa **B**, Black Hole **B**, Fermi **C**, Andromeda **REP**. Jupiter pick held, not applied.
- **Rebuild follow-up:** `9lLZMy8rBJo` + `CkSECfUfH2Y` rebuild_v2 — crop-scale caption-free regions (no inpaint).
- **SWAPPED live 26 Sep 2026** (Studio desktop, outright replace): all 12 approved thumbs. Times/baselines in `../THUMBNAIL_TITLE_AUDIT_2026-09-25/SWAP_LOG.md`. Day-14 CTR compare **10 Oct 2026**. `9lLZ`/`CkSE` = rebuild_v2.
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
| 4 | Andromeda thumb → WHEN THEY MEET | **file prepared**, then **SWAPPED live 26 Sep** |
| 5–6 | Andromeda Short retitles | **2 options each**, propose only |
| 7 | phone sound check of Andromeda Shorts | not done here |

### Captions (backlog #4)

Jupiter and Andromeda locked VO scripts **not in this checkout** — caption txts not produced. See `captions/README.md`.

### Jupiter pinned comment (backlog #1)

Proposed final in `REFRESH_LOG.md` / `PINNED_COMMENTS.json`. `commentId` empty until `--create` after public.

### Shorts sweep

Graded other public Shorts; failures in `REFRESH_LOG.md` / `refresh/sweep/SWEEP_GRADE.json`. **Not built.**

## Schedule fix (27 Sep 2026, in Studio)

Three schedule changes were saved in YouTube Studio on 27 Sep 2026. They were not applied by the YouTube API. Titles were left as they were. Nothing was deleted.

| id | change |
|---|---|
| `k9pXeeJvLpc` | Set Private. Schedule date removed. Title unchanged: Our Galaxy's Final Destination #cosmos #astronomy #space |
| `e-7hzJv4c80` | Moved to Wednesday 30 Sep 2026, 11:30, GMT+0100. Title unchanged: How Long Until Andromeda Hits Us? |
| `CtllH6VOhEI` | Set Private. Schedule date removed. Title unchanged: What Happens When Galaxies Actually Collide? |

`k9pXeeJvLpc` and `CtllH6VOhEI` were not already in the open-gate library, so each was added via `gate_shorts_open.py add … --status retired` (black placeholder frame; source `retired_unscheduled_27sep_placeholder`). The library `date` is the air date from the 24 Sep sound check, before the schedule was removed (`k9pXeeJvLpc` 30 Sep, `CtllH6VOhEI` 1 Oct). `e-7hzJv4c80` was not retired and was not added.

| id | result |
|---|---|
| `k9pXeeJvLpc` | added as retired |
| `CtllH6VOhEI` | added as retired |

**Correction, 6 Oct 2026 (Claude, from the Chief's Data API read):** `CtllH6VOhEI` didn't stay private. On 1 Oct at 08:32 London it was set back to `private` with `publishAt 2026-10-01T10:30:00Z`, and it went public on that schedule at 11:30 London, the only Short that day. It stays public. In the open-gate library its placeholder was replaced with a real live entry (`2840c77`).

Known empty slots are not errors:

- Fri 9 Oct has no Short.
- The Saturn long is not scheduled for Sun 11 Oct 18:00.
- The week of 12/14/16 Oct only has Wednesday `buaOI3QGm7U`. Mon 12 Saturn tease and Fri 16 Last Star are not built.
