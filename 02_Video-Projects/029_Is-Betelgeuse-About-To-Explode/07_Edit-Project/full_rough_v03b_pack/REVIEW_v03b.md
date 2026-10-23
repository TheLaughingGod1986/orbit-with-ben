# 029 Is Betelgeuse About to Explode? — Full Rough v03b Review (`J0891`, 23 Oct 2026)

**Cut:** `029_Betelgeuse_full_rough_v03b.mp4` (`542.23 s`, `84` cuts, max single picture `13.66 s`, `-14.0 LUFS` / `-1.2 dBTP`, **£0 spend**)
**SHA-256 (all 3 master copies identical):** `54e04d3bfcb42bcf9066a0613254f10c978435b148d158468711e25908060c93`
**Phone Copy (`< 120 MB`):** `029_Betelgeuse_full_rough_v03b_PHONE.mp4` (`91.46 MB`, sha256 `9e6452e4b6459c5962c231fb037d79f205cebaec8bbae66f624774a1b82119b7`)

## 1. Chief FIX on `J0885` v03 (`04bab9a9`: `r21_hero` 3:53 right card text on two 36 px lines)

See `r21_hero_before_after_v03b.jpg`, `sheet_fixes_v03b.jpg`, and `per_row_sheet_v03b.jpg`.

| Item | Before (`full_rough_v03` / `J0885`) | After (`full_rough_v03b` / `J0891`, `04bab9a9`) | Verification |
|---|---|---|---|
| **`r21_hero` (`228.95–233.00 s`, `3:48.95–3:53.00`) right-hand mountain card** | `'1 billion tonnes · 1.1 billion US tons'` on a single `40 px` line at `(1440, 852)`, which overran the `660 px` gold card border (`x=1110..1770`) on both sides. | Re-rendered `r21_hero` (`code_graphic_029_r21_hero_v01.mp4`, sha `84aae456b419`) from `04bab9a9`:<br>• Line 1 (`y=768`, `52 px` gold): **`1 mountain`**<br>• Line 2 (`y=836`, `36 px` white): **`1 billion tonnes`** (`x=1299..1581`, `189 px` left/right card padding)<br>• Line 3 (`y=880`, `36 px` white): **`1.1 billion US tons`** (`x=1274..1606`, `164 px` left/right card padding) | Both lines sit cleanly inside the gold card border `[1110, 710, 1770, 912]` with `>= 164 px` horizontal margin and `>= 18 px` bottom margin (`title_safe_audit_v03b.json` + `r21_hero_before_after_v03b.jpg`). Every other cut is identical to `v03`. |

## 2. Gate Results (All PASS)

- **`clip_check.py`:** `clip_check: 84 rows — PASS
OK: sentence/card boundaries and end-after-VO checks clear.`
- **`picture_qa.py`:** `picture QA PASS: 0 of 84 cuts fail, 6 to look at -> /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/full_rough_v03b_pack/picture_qa_v03b/PICTURE_QA.md` (`0` holds over 15 s)
- **`polish_gate.py`:** `polish gate PASS: 0 of 84 rows failed, 4 to look at -> /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/full_rough_v03b_pack/polish_gate_v03b.json`
- **`music_gate.py --video`:** `WARN reused: couldn't read saturn_long_vo_v02_LISTEN.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read jupiter-vo.mp3 to compare (OSError); download it or pass --others
WARN reused: couldn't read jupiter-music.mp3 to compare (OSError); download it or pass --others
WARN reused: couldn't read friday_black_dwarf_short_vo_v01_LISTEN.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v02_LISTEN.m4a to compare (OSError); download it or pass --others
WARN reused: couldn't read monday_saturn_short_vo_v02_how_long.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v03_tightened.m4a to compare (OSError); download it or pass --others
WARN reused: couldn't read monday_saturn_short_vo_v01_LISTEN.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v03b_tightened_LOCK.m4a to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v03b_tightened_LOCK.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v01_LISTEN.wav to compare (OSError); download it or pass --others
WARN reused: couldn't read monday_saturn_short_vo_v02_how_long.mp3 to compare (OSError); download it or pass --others
WARN reused: couldn't read saturn_long_vo_v03_tightened.wav to compare (OSError); download it or pass --others
music gate PASS: betelgeuse_score_bed_v01.mp3, 542.3 s, about 75.0 BPM, brief Pace: 68-78 BPM`
- **`sfx_kit.py level`:** `PASS (vo -15.1 LUFS, sfx -32.0 LUFS, 39 hits, 0 fails)` (`sfx_level_v03b.json`)
- **Title-safe & card-border audit (`title_safe_audit_v03b.json`):** `PASS` (100% of labels, pills, cards, and `r21_hero` card lines inside their borders and `[90, 54, 1830, 1026]`)
- **Per-chapter teaching gate (`TEACHING_GATE_v03b.md`):** `6/6` chapters PASS on `NUMBER` and `WORDS` (all 22 pills intact on their exact spoken words).
- **Back-to-back code graphics:** `0`.
