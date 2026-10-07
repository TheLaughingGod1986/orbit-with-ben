# Upcoming Shorts: gate check

Written by `gate_upcoming.py` at 2026-10-07 11:45 London for Shorts scheduled in the next 14 days. Don't edit by hand.

| Airs (London) | Short | In library | Gate |
|---|---|---|---|
| 2026-10-12 11:30 | [Saturn's Rings Are Already Falling](https://youtu.be/Qn56D6TOi0k) `Qn56D6TOi0k` | yes | PASS |
| 2026-10-14 11:30 | [Could a Robot Survive Falling Into Jupiter?](https://youtu.be/buaOI3QGm7U) `buaOI3QGm7U` | yes | PASS |
| 2026-10-16 11:30 | [Why No Black Dwarf Exists Yet](https://youtu.be/1NeQFVnzO2Q) `1NeQFVnzO2Q` | yes | **FAIL** |

## Needs a look

### 1NeQFVnzO2Q: FAIL

```
FAIL  friday_black_dwarf_why_none_yet_v04.mp4  dur=26.9s  audio=-23.1dB  motion=0.8  dhash=820a0a1e1e1d0204  visor=0.0048
   FAIL  Orbit in frame at 0 s (visor 0.0048 ≥ 0.003) — picture-first lock
   warn  picture barely changes in the first second (motion 0.8 < 10) — trim the clip's ease-in so frame 0 is already mid-action
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/orbit_shorts_gate/friday_black_dwarf_why_none_yet_v04_open_sheet.jpg
```

