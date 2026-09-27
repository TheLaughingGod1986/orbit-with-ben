# Channel audit fix log — 24 Sep 2026

## Retire Andromeda leftovers (26 Sep 2026) — gate library only

Eleven private, unscheduled, 0-view Andromeda Shorts (uploaded 19 Sep) marked **`retired`** in `audits/shorts_open_library/library.json` so the open gate stops comparing them. **Nothing deleted. No Studio / privacy / schedule changes.** Ben OK'd this merge to main so every machine sees the same list.

They were not already in the library, so each was added via `gate_shorts_open.py add … --status retired` (black placeholder frame; source `retired_leftover_19sep_placeholder`).

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

Known empty slots are not errors:

- Fri 9 Oct has no Short.
- The Saturn long is not scheduled for Sun 11 Oct 18:00.
- The week of 12/14/16 Oct only has Wednesday `buaOI3QGm7U`. Mon 12 Saturn tease and Fri 16 Last Star are not built.
