# 029 Is Betelgeuse About to Explode? — Full Rough v03 Review (`J0885`, 23 Oct 2026)

**Cut:** `029_Betelgeuse_full_rough_v03.mp4` (`542.23 s`, `84` cuts, max single picture `13.66 s`, `-14.0 LUFS` / `-1.2 dBTP`, **£0 spend**)
**SHA-256 (all 3 master copies identical):** `044104c5cefd6d68db21d21446a78f10bed564cf801b2d6a49ef415f200ee508`
**Phone Copy (`< 120 MB`):** `029_Betelgeuse_full_rough_v03_PHONE.mp4` (`91.50 MB`, sha256 `a1ce6d7bf3e7bc9d6df6b8111b510e04282baf6737cda94c7c300db4a8f96172`)

## 1. Ben's Two Changes + Two Standing Lessons from 028 (Before vs After — see `sheet_fixes_v03.jpg` & `per_row_sheet_v03.jpg`)

| Item | Before (`full_rough_v02` / `J0828`) | After (`full_rough_v03` / `J0885`) | Verification |
|---|---|---|---|
| **1. `3:53 Diagram needs rebuilt` (`r21_hero`, `228.95–233.00 s`)** | Abstract line-triangle outline and oval spoon over radar rings with only `'a mountain'` at top (`code_graphic_029_r21_hero_v01.mp4`). | Rebuilt `Renderer.teaspoon` in `build_code_graphics_v01.py` into a school-child-readable balance-scale comparison diagram in house style (`#121F34` stage, gold/white/ice typography, 100% inside title-safe):<br>• Header (`y=118`): **`A teaspoon of it would weigh as much as a mountain`** (VO's own words)<br>• Left pan (`cx=480`): **`Neutron star`** callout + arrow into a silver metallic teaspoon holding a glowing golden neutron-star scoop; card below: **`1 teaspoon`** / **`5 ml · 1 tsp`**<br>• Fulcrum (`cx=960, y=650`): level beam + **`=`** badge<br>• Right pan (`cx=1440`): snow-capped three-peak mountain range; card below: **`1 mountain`** / **`1 billion tonnes · 1.1 billion US tons`** | Checked against `01_Script/SOURCES.md` Row 13 (Lattimer & Prakash 2004 *Science* 304:536; NASA GSFC *"A teaspoon of neutron star material would weigh about 1 billion to 4 billion tons on Earth"*, `5 mL = 1–2.5 × 10⁹ tonnes`). |
| **2. `5:08 Let's draw the line between the stars to show the constellation` (`r27_orion_b` `303.32–309.46 s`, `r27_orion_a`, `r25_orion`, `r09_finder`, `r03_promise_a`)** | Unlabelled star dots over random background dots; no constellation lines connecting Orion's stars. | Replaced random background dots with real J2000 cataloged stars from the Hipparcos / Yale Bright Star Catalog (`ORION` + `ORION_CATALOG_FIELD`, zero invented stars, matching the real sky geometry in the ESO Paranal plates) and animated thin constellation stick-figure lines (`ORION_LINES`) joining **`Betelgeuse`**, **`Bellatrix`**, the belt (**`Alnitak`** / **`Alnilam`** / **`Mintaka`**), **`Saiph`**, and **`Rigel`** as the VO names Orion, with **`Betelgeuse`**, **`Bellatrix`**, **`Orion's Belt`**, **`Saiph`**, and **`Rigel`** labelled (shoulder lines become dashed gold with an open shoulder ring when Betelgeuse fades out at `5:03–5:09`). | Positions match J2000 RA/Dec coordinates (`orion_px`) and the real ESO Paranal sky plates (`sheet_fixes_v03.jpg`). |
| **3. Standing lesson from 028: No text clipped at the top anywhere** | Audited all text-bearing plates and overlays. | Verified every code-graphic label (`y=150` top / `y=900` bottom), diagram header (`y=118`), constellation star label (`y in [110, 835]`), all 22 teaching pills (`overlays_v01.json`), all 5 chapter cards, subscribe pill, and closing card across every frame of slide-in and hold. | `title_safe_audit_v03.json` **PASS**: 100% inside `[90, 54, 1830, 1026]` (`>= 5%` top/bottom margin). |
| **4. Standing lesson from 028: Proper ending (closing card naming next film + 20 s moving picture)** | Film stopped at `517.26 s` (`8:37.26`) only `3.00 s` after the last spoken word (`514.26 s`), with no closing card and no 20 s end screen. | Kept the `3.00 s` post-VO breathe (`514.26–517.26 s`) on `r39_return` (`lasilla_mw.mp4` without early fade); added `r40_closing_card` (`517.26–522.26 s`, `5.00 s` over moving `orion_over_paranal.mp4`) with the house closing card (`NEXT ON ORBIT WITH BEN` / **`What Happens When Earth's Magnetic Field Flips?`** / `@OrbitWithBen`, `517.76–521.56 s` + soft whoosh & UI tick); followed by `20.00 s` (`522.26–542.26 s`) of moving picture across 3 cuts (`r41_end_screen_a` `orion_rise_vlt.mp4`, `r41_end_screen_b` `blue_marble.jpg` push-in, `r41_end_screen_c` `chajnantor_mw.m4v`) and a `1.5 s` video + audio fade to black (`540.76–542.26 s`). | Full runtime `542.26 s` (`9:02.26`), `-14.0 LUFS` / `-1.2 dBTP`, 0 new VO, £0 spend. |

## 2. Gate Results (All PASS)

- **`clip_check.py`:** `clip_check: 84 rows — PASS
OK: sentence/card boundaries and end-after-VO checks clear.`
- **`picture_qa.py`:** `picture QA PASS: 0 of 84 cuts fail, 6 to look at -> /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/full_rough_v03_pack/picture_qa_v03/PICTURE_QA.md` (`0` holds over 15 s)
- **`polish_gate.py`:** `polish gate PASS: 0 of 84 rows failed, 4 to look at -> /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/full_rough_v03_pack/polish_gate_v03.json`
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
- **`sfx_kit.py level`:** `PASS (vo -15.1 LUFS, sfx -32.0 LUFS, 39 hits, 0 fails)` (`sfx_level_v03.json`)
- **Title-safe audit (`title_safe_audit_v03.json`):** `PASS` (100% of labels, pills, and cards inside `[90, 54, 1830, 1026]`)
- **Per-chapter teaching gate (`TEACHING_GATE_v03.md`):** `6/6` chapters PASS on `NUMBER` and `WORDS` (all 22 pills intact on their exact spoken words).
- **Back-to-back code graphics:** `0`.
