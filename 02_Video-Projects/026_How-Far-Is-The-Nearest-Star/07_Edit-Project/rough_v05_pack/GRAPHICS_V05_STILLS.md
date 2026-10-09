# 026 v05: two new code graphics, stills for Claude (J0085)

Rendered by `code_graphics.py lightyear|lightrace code_out_v05/` (Mini, 9 Oct). Text-free. Sheet: `code_out_v05_sheet.jpg`; full-size stills in `code_out_v05_stills/`.

## `lightyear` (row 9), 9.6 s
- Proxima (the code red-dwarf glow, as in `parallax`) left; real Earth right (LRO/Blue Marble `GSFC_20171208_Archive_e002130`, cut-out disc); full-frame star field; a very faint guide line.
- One pulse leaves Proxima at 0.6 s and reaches Earth at 8.3 s at constant speed. Four ticks at 1/4.25 … 4/4.25 of the path light gold as it passes (one per year; the last quarter year has no tick). Earth glows briefly on arrival.
- Stills: 0.3 s (start), 4.5 s (two ticks lit), 8.6 s (arrival).
- **Placement (needs Claude's call):** row 9 runs 108.33–121.73 s. An 8 s graphic that only takes the `journey` slot (108.33–112.20) can't land on "four years ago" (120.26–121.0). Proposed v05 row 9: `iss073e0982679` 108.33–112.20 ("A light-year is a distance, not a time."), then `lightyear` 112.20–121.73 (hold_ok, 9.5 s), so the pulse arrives at 120.5 s on "four years ago". `eso1031a` leaves row 9 (it stays in rows 13 and 24's neighbours).

## `lightrace` (row 27), 16.8 s, timed from the row start (361.80 s)
- Real Earth disc right throughout. Left, in turn, each a cut-out disc on black space:
  - Moon (`GSFC_20171208_Archive_e001982`, 2nd use): in at 1.9 s, pulse 3.3 → 4.3 s (1 s; "Moonlight" is at 3.12).
  - Sun (`GSFC_20171208_Archive_e002035`, 2nd use): in at 6.0 s, pulse 6.5 → 9.5 s (3 s; "Sunlight" is at 6.38).
  - Proxima (code red-dwarf glow): in at 9.7 s, pulse sets out at 10.2 s ("Light from the nearest star" is at 9.24) and crawls to 3.5% of the way by the end, holding that slow progress over "the shortest trip of its kind there is".
- Stills: 3.8 s (Moon pulse), 8.0 s (Sun pulse mid-trip), 16.5 s (Proxima's sliver at the end).
- **Flag:** `e002035` is SDO ultraviolet, so the Sun reads **blue**. Used as briefed. If Claude wants a yellow-white Sun, `e000790` or `e000759` are the alternatives in the pool (one constant change).

## Still to do on J0085
1. Claude OKs (or changes) the stills and the row 9 placement above.
2. Two Omni takes (rows 11 and 24), Vertex `global`, one take each, balance read before each.
3. v05 render from v04's cached segments, rows 9, 11, 24 and 27 changed; picture_qa, music_gate, clip_check; `OWB UAT/026_NearestStar_v05_PHONE.mp4`.
