# 028 A Star Is Coming Toward Us (Gliese 710) — Full Master v03 Review (`J0884`, 23 Oct 2026)

**Cut:** `028_Gliese710_full_master_v03.mp4` (`497.83 s`, `65` cuts, max single picture `14.66 s`, `-14.1 LUFS` / `-1.3 dBTP`, **£0 spend**)
**SHA-256 (all 3 master copies identical):** `a9780e548a2775f4e7a1acecb6ac24308927f0b58ab1d606e67d27741e3db824`
**Phone Copy (`< 120 MB`):** `028_Gliese710_full_master_v03_PHONE.mp4` (`82.53 MB`, sha256 `05529b28e0d89a48c40575b6048bc037857192e36576bfbd4bb3d0588f831774`)

## 1. Ben's Two Changes Applied on Top of Master v02 (Before vs After — see `sheet_fixes_v03.jpg` & `per_row_sheet_v03.jpg`)

| Change | Before (`full_master_v02` / `J0864`) | After (`full_master_v03` / `J0884`) | Verification |
|---|---|---|---|
| **1. `1:20 Top text cut off` + full scan of all text-bearing rows** | `render_code_segment` applied `reframe_at` crops after `r.frame()` had already drawn the HUD text (`cg.LABELS` at `y=125` and bottom credits at `y=986`). On `r09_drift` (`67.80–82.46 s`), `reframe_at` at `10.57 s` (`78.37–82.46 s`, across `1:20`) cropped `box=(0.12, 0.12, 0.88, 0.88)`, slicing off the top half of `'Hardly drifts'` (`top_y = -42.9 px`) and the bottom credits (`y = 1145 px`). On the other 8 `reframe_at` code plates (`r04_shower_shell`, `r14_hipparcos_card`, `r15_16_path`, `r20_oort_shell_a`, `r21_oort_shell_b`, `r25_shower_b`, `r27_shower`, `r34_traffic`), `box=(0.06, 0.06, 0.94, 0.94)` pushed the top label to `y = 36.6 px` (`3.4% < 5%` title-safe) and bottom credits to `y = 1062.7 px` (`98.4% > 95%`). | `render_code_segment` now reframes the scene/diagram layer first and draws the HUD top label (`y = 125 + 14*(1-alpha)`) and bottom credits (`x=100..1818, y=986`) directly in `1920×1080` screen space across all 9 `reframe_at` code plates. At `1:20` (`r09_drift` `'Hardly drifts'`) and across all 23 code labels, `top_y = 97..111 px` (`9.0%–10.3% >= 5.0%` title-safe) and bottom credits sit at `y = 972..1000 px` (`7.4%` bottom margin `>= 5.0%`). | `title_safe_audit_v03.json` **PASS** across all 23 code labels, all 22 teaching pills, all 6 chapter cards, subscribe pill, and closing card (`sheet_fixes_v03.jpg`). |
| **2. `7:53 Very prompt ending` (`469.34–497.84 s`)** | Film stopped at `472.84 s` (`7:52.84`) only `3.50 s` after the last spoken word (`469.34 s`), with no closing card and no 20 s YouTube end screen. | Kept the `3.50 s` post-VO breathe (`469.34–472.84 s`) on `r38_return` (removing the early fade-out) as the score resolves; added `r39_closing_card` (`472.84–477.84 s`, `5.00 s` over moving `eso_lasilla_ntt.mp4`) with the house closing card naming next week's film (`NEXT WEEK · SUNDAY 6 DECEMBER` / `'Is Betelgeuse About to Explode?'` / `@OrbitWithBen`, `473.34–477.15 s` + soft whoosh & UI tick); followed by `20.00 s` (`477.84–497.84 s`) of moving picture across 3 cuts (`r40_end_screen_a` `eso_mw_lasilla.mp4`, `r40_end_screen_b` `comet_a3.jpg` push-in, `r40_end_screen_c` `eso_startrails.mp4`) and a `1.5 s` video + audio fade to black (`496.34–497.84 s`). | All 4 Chief fixes from v02 preserved; full runtime `497.84 s` (`8:17.84`), `-14.1 LUFS` / `-1.3 dBTP`, 0 new VO, £0 spend. |

## 2. Gate Outputs (All PASS)

- **`clip_check.py`:** `clip_check: 65 rows — PASS
OK: sentence/card boundaries and end-after-VO checks clear.`
- **`picture_qa.py`:** `picture QA PASS: 0 of 65 cuts fail, 7 to look at -> /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/full_master_v03_pack/picture_qa_v03/PICTURE_QA.md`
- **`polish_gate.py`:** `polish gate PASS: 0 of 65 rows failed, 4 to look at -> /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/full_master_v03_pack/polish_gate_v03.json`
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
music gate PASS: gliese_score_bed_v03.mp3, 497.8 s, about 70.6 BPM, brief Pace: 64-74 BPM`
- **`sfx_kit.py level`:** `sfx level PASS: VO -14.7 LUFS, SFX -31.4 LUFS (37 hits), 0 fails` (`sfx_level_v03.json`)
- **`npm run gate:episode`:** `PASS — VO / Gemini Veo allowed · Script score: 91/100 · PASS` (`episode_gate_v03.txt`)
