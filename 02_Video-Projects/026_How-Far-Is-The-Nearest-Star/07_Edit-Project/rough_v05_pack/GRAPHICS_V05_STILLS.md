# 026 v05: two new code graphics, stills for the Chief (J0085)

Rendered by `code_graphics.py lightyear|lightrace code_out_v05/` (Mini). Sheet: `code_out_v05_sheet.jpg`; full-size stills in `code_out_v05_stills/`.

**Round 2 (10 Oct), after the Chief's FIX (#6090651546).** Both graphics now carry short labels in house type (Arial/Helvetica bold, 60 pt, about 100 px cap-to-descender at 1080), white with the number in yellow (#ffd23f), in the empty band above or below the path, each fading in on its spoken word. Every label is the spoken words, and none says 4.25.

## `lightyear` (row 9), 9.6 s, placed 112.20–121.73 (hold_ok)
- Proxima (code red-dwarf glow, as in `parallax`) left; real Earth right (`GSFC_20171208_Archive_e002130`), now 1.4x (140 px across); full-frame star field.
- Guide line 3 px at 35% white. Ticks 6 px wide and 44 px tall, grey until lit, then gold.
- One pulse leaves Proxima at 0.6 s (112.8 s film) and reaches Earth at 8.3 s (120.5 s, on "four years ago") at constant speed. Four ticks at 1/4.25 … 4/4.25 of the path.
- Labels: "Proxima" under the star from the row start; "1 year" (yellow) above the first tick as it lights at 2.41 s (114.61 s, "in a year" at 114.58); "More than **4 years**" above the path from 7.6 s (119.8 s, "more"), fully in by "four" (120.26 s).
- Stills: 0.3 s, 4.5 s, 8.6 s.

## `lightrace` (row 27), 16.8 s, timed from the row start (361.80 s)
- Real Earth disc right throughout (radius unchanged). Left, in turn:
  - Moon (`GSFC_20171208_Archive_e001982`, 2nd use), now 0.5x Earth's width. Pulse 3.3 → 4.3 s. Label "Just over **a second**" from 4.56 s ("just").
  - Sun, now `sun/GSFC_20171208_Archive_e000759.jpg` (gold, 2nd use), 1.5x Earth's width. It read bronze-orange next to Earth, so `disc()` grades it warm-white (that file only). Pulse 6.5 → 9.5 s. Label "About **8 minutes**" from 7.78 s ("eight").
  - Proxima (code red-dwarf glow) from 9.7 s, with the same 3 px guide line to Earth and a solid gold trail behind the pulse. The pulse sets out at 10.2 s and crawls to 3.5% of the way by the end. Label "More than **4 years**" from 11.34 s ("more").
- Timings unchanged otherwise (Moon 3.3→4.3, Sun 6.5→9.5, Proxima from 10.2).
- Stills: 4.9 s (Moon pulse landed, label in), 8.4 s (Sun pulse mid-trip, label in), 16.5 s (Proxima's sliver at the end).

## Row 9 placement (approved by the Chief)
`iss073e0982679` 108.33–112.20 ("A light-year is a distance, not a time."), then `lightyear` 112.20–121.73 (hold_ok). `eso1031a` leaves row 9; `journey` drops to 2 uses.

## Still to do on J0085
1. ~~Omni takes rows 11 and 24~~ (done: 4537e72, 59e3a17).
2. v05 render from v04's cached segments, rows 9, 11, 24 and 27 changed; picture_qa (both graphics added to `polish_reviewed_ok` as code graphics on black space), music_gate, clip_check; `OWB UAT/026_NearestStar_v05_PHONE.mp4`.
