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
