# J2540 — Frame-0 Full-Bleed Gate Results Across All Scheduled Shorts (OWB + HOS)

- **Job:** `J2540` (second half of `J2505`, following `J2539` merge in OWB `#771` and HOS `#486`)
- **Check run:** `00_Brand/Channel-Setup/tools/gate_shorts_open.py check <file> --air-date <YYYY-MM-DD> --id <id> --report-only --json`
- **Execution:** Detached `tmux` session `J2540-gate` (`~/_desk/logs/J2540-gate.log`, `~/_desk/logs/J2540-gate.done` = `0`)
- **YouTube / Studio / Exports:** Nothing re-cut, nothing changed in Studio, £0.

## 1. Summary for Chief

- **Scope:** 36 rows across both channels:
  - **Orbit With Ben (`OWB`):** 23 scheduled Shorts (`2026-11-11` to `2026-12-16`), 1 reference Short that aired today (`ffYKoNVPoqg`, `2026-11-10` — the trigger for `J2505`), **all 3 `J2494` first-second re-cuts** (`gmzaCfJF1gA` v02, `HZGTovJu_TQ` v05, `cwU_0WWeNZ4` v06), plus the 2 `J2512` follow-up re-cuts (`HZGTovJu_TQ` v06, `cwU_0WWeNZ4` v07) and the `J2510` Mars Ingenuity re-cut (`bSjWiCbB7pY` v06, queued for swap in `J2520`).
  - **History of Science (`HOS`):** All 6 scheduled Shorts (`2026-11-13` to `2026-11-21`).
- **Which rows are the three `J2494` re-cuts (re-cut today for their first second):**
  1. **Row 7 — `gmzaCfJF1gA (J2494 v02)`** (airs Sat `2026-11-14`, `owb_sa_s7_pluto_heart_v02.mp4`, swap queued in `J2511`; its currently scheduled original `v01` is Row 6): **PASS** (`detail_top/ctr/bot = 16.08 / 7.87 / 5.35`, `std_top/bot = 87.84 / 26.14`, `seam_rows = None`).
  2. **Row 9 — `HZGTovJu_TQ (J2494 v05)`** (airs Mon `2026-11-16`, `mon16_cant_see_nearest_star_v05.mp4`, swap queued in `J2513`; its `J2512` follow-up `v06` is Row 10, and its currently scheduled original `v01` is Row 8): **PASS** (`detail_top/ctr/bot = 13.87 / 10.21 / 12.23`, `std_top/bot = 34.34 / 19.68`, `seam_rows = None`).
  3. **Row 13 — `cwU_0WWeNZ4 (J2494 v06)`** (airs Wed `2026-11-18`, `wed18_robot_reach_nearest_star_v06.mp4`, swap queued in `J2514`; its `J2512` follow-up `v07` is Row 14, and its currently scheduled original `v01` is Row 12): **PASS** (`detail_top/ctr/bot = 8.29 / 6.91 / 0.53`, `std_top/bot = 37.66 / 2.76`, `seam_rows = None`).
  *(Note: the 4th `J2494` candidate, `kKN8Ale42sE` on `2026-11-17`, Row 11, was not re-cut in `J2494` because the uploaded SHA-256 is not on disk; the local `v01` file on disk also PASSes the frame-0 full-bleed check.)*
- **Verdict breakdown on the new frame-0 full-bleed check:**
  - **FAIL (2 rows):**
    1. **Row 1 — `OWB` `ffYKoNVPoqg` (`2026-11-10`, reference row — aired 10 Nov 11:30Z):** **FAIL** (`blur-pad` on `2/3` frames, `0.00s` & `0.25s`, band `38%–61%` at `seam_rows=[72, 117]`, `detail_outside=2.84` vs `detail_picture=7.30`, `std_outside=27.53` vs `std_picture=39.58`). True positive.
    2. **Row 35 — `HOS` `ChbsigHD5_o` (`2026-11-18`, *How Do Plants Clean the Air?*, `hos006_short_b_v02.mp4`):** **FAIL** (`blur-pad` on `3/3` frames, `0.00s`, `0.25s`, `0.50s`, band `33%–66%` at `seam_rows=[63, 127]`, `detail_outside=1.35` vs `detail_picture=15.25`, `std_outside=14.17` vs `std_picture=43.10`). **Visual false positive on contact-sheet inspection:** the 3D cartoon plate is genuinely full-bleed 9:16 (soft-focus wallpaper wall at top `detail_top=1.59`, glass bell jar + large stroked caption `"MINT FIXED THE AIR"` in the middle `detail_centre=15.99`, smooth wooden tabletop at bottom `detail_bottom=1.07`). It trips `full_bleed_frame()` because the top of `"MINT"` at row `63–64` (`33%`) creates a 3/4-segment detail jump (`up_step_share=0.269 < 0.70`, `up_detail_ratio=0.053 <= 0.40`) while the straight tabletop edge at row `127–129` (`66%`) creates a brightness step (`low_step_share=0.741 >= 0.70`, even though `low_detail_ratio=1.223 > 1.0`, i.e. detail increases below the seam rather than dropping into blur).
  - **PASS (33 rows) & NO FILE (1 row, Row 4 `bSjWiCbB7pY` v02 `knownNoFile`, whose `J2510` v06 replacement in Row 5 PASSes):**
    - **Visual calibration note on two PASS rows for Chief's threshold review (`gate_shorts_open.py` line 174):**
      1. **Row 16 — `OWB` `rvug71d7Dqk` (`2026-11-21`, *Muons Shouldn't Reach the Ground. They Do.*, `fri06_muons_ground_v04.mp4`):** **PASS** on the current check (`kinds=[None, None, None]`), **but visually opens on a feathered blur-pad (`0.0–1.5s`)** on its contact sheet (`detail_top/ctr/bot = 12.17 / 11.83 / 2.89`, `std_top/bot = 43.73 / 34.22`). Why it passed: (a) the seam at `y≈75, low≈117` (`39%–61%`) is feathered so `step_share = 0.50–0.64 < 0.70` and the 3-row adjacent detail ratio is `0.54–0.66 > 0.40`, and (b) the large 2-line hook caption `"THEY / LIVE"` in the upper band raises the upper row-median detail to `det_top_med = 7.87 > 4.20` while the uncaptioned lower blur band sits at `det_bot_med = 4.14 <= 4.20` (`detail_bottom = 2.89` vs `detail_centre = 11.83`).
      2. **Row 31 — `HOS` `cLKDiYP55J8` (`2026-11-13`, *What Was the Edward Jenner Experiment?*, `hos_007_s04_smallpox_test_v04.mp4`):** **PASS** (`kinds=[None, None, 'blur-pad']` — only `t=0.50s` flagged at `seam_rows=[38, 151]`, `detail_outside=3.50` vs `detail_picture=14.84`). Visually **full-bleed 9:16** (wooden desk & books with shallow depth of field at top `detail_top=3.67` and bottom `detail_bottom=2.66` vs `detail_centre=20.86` over the velvet lancet case and `"THE FIRST TEST"` title).

---

## 2. Full Table of Scheduled Shorts (Both Channels) & `J2494` Re-Cuts

Columns show the exact readings from `gate_shorts_open.py`: `kinds (0.00s / 0.25s / 0.50s)`, `detail_top / detail_centre / detail_bottom` and `std_top / std_bottom` at `0.00s` (on the `108x192` greyscale frame), plus `seam_rows`, `detail_outside / detail_picture`, `std_outside / std_picture`, `seam_step_share`, and `seam_detail_ratio` whenever a seam pair is detected on any of the three frames.

| # | Ch | Video ID | Air Date (UTC) | J2494 Re-Cut? | New Check (`frame0_full_bleed`) | Frame Kinds (`0.00 / 0.25 / 0.50s`) | `detail_top / ctr / bot` (`0.00s`) | `std_top / bot` (`0.00s`) | Detected Seam (`seam_rows`, `out vs pic detail`, `out vs pic std`, `step_share`, `det_ratio`) | Overall Gate (`--report-only`) & Notes |
|---:|:---:|---|---|---|:---:|---|---|---|---|---|
| 1 | OWB | `ffYKoNVPoqg` | 2026-11-10 | No | **FAIL** | `blur-pad` / `blur-pad` / `None` | `20.21 / 7.57 / 2.64` | `54.71 / 28.57` | t=`0.00s` rows=`[72, 117]` (23.4% H), det out/pic=`2.84 / 7.3`, std out/pic=`27.53 / 39.58`, step=`[0.926, 0.778]`, rat=`[0.381, 0.859]` | `FAIL` — Aired 10 Nov 11:30Z (reference trigger for J2505/J2539) |
| 2 | OWB | `B1z2dv7m7Vk` | 2026-11-11 | No | PASS | `None` / `None` / `None` | `9.87 / 5.99 / 11.15` | `44.25 / 29.06` | `None` | `PASS` — Scheduled upload |
| 3 | OWB | `uhZSRcvngvE` | 2026-11-12 | J2510 re-cut (v05, swapped in by J2519) | PASS | `None` / `None` / `None` | `23.55 / 15.17 / 16.21` | `53.17 / 26.19` | `None` | `PASS` — Scheduled upload (swapped in today by J2519 from J2510 v05; supersedes N42gKBbD7tE which had knownNoFile) |
| 4 | OWB | `bSjWiCbB7pY` | 2026-11-13 | No | **NO FILE** | — | — | — | — | `knownNoFile` (J1320); see Row 5 (`J2510 v06`) |
| 5 | OWB | `bSjWiCbB7pY (J2510 v06)` | 2026-11-13 | J2510 re-cut (v06, swap queued in J2520) | PASS | `None` / `None` / `None` | `7.98 / 4.18 / 3.85` | `32.97 / 15.13` | `None` | `PASS` — Ben-approved v06 re-cut queued for swap in J2520 |
| 6 | OWB | `gmzaCfJF1gA` | 2026-11-14 | J2494 target #1 (original v01) | PASS | `None` / `None` / `None` | `14.6 / 7.42 / 2.52` | `91.08 / 24.26` | `None` | `PASS` — Currently scheduled upload (v01); J2494 re-cut #1 (v02) below, swap queued in J2511 · stayed-gate warns: pushed still at frame 0 (mean 0–1.5 s frame diff 0.64 < 1.50) — use moving footage; first cut at 5.90s > 3.0s (scene-change detect); spoken text contains meta-promise ("stay, and i'll show you") |
| 7 | OWB | `gmzaCfJF1gA (J2494 v02)` | 2026-11-14 | YES — J2494 re-cut #1 (v02) | PASS | `None` / `None` / `None` | `16.08 / 7.87 / 5.35` | `87.84 / 26.14` | `None` | `PASS` — J2494 re-cut #1 of 3 (Ben OK'd, swap queued in J2511) |
| 8 | OWB | `HZGTovJu_TQ` | 2026-11-16 | J2494 target #2 (original v01) | PASS | `None` / `None` / `None` | `13.87 / 10.21 / 12.23` | `34.34 / 19.68` | `None` | `PASS` — Currently scheduled upload (v01); J2494 re-cut #2 (v05) and J2512 (v06) below · stayed-gate warns: first cut at 4.80s > 3.0s (scene-change detect) |
| 9 | OWB | `HZGTovJu_TQ (J2494 v05)` | 2026-11-16 | YES — J2494 re-cut #2 (v05) | PASS | `None` / `None` / `None` | `13.87 / 10.21 / 12.23` | `34.34 / 19.68` | `None` | `PASS` — J2494 re-cut #2 of 3 (Ben OK'd; swap in J2513) |
| 10 | OWB | `HZGTovJu_TQ (J2512 v06)` | 2026-11-16 | YES — J2494/J2512 re-cut #2 (v06) | PASS | `None` / `None` / `None` | `13.87 / 10.21 / 12.23` | `34.34 / 19.68` | `None` | `PASS` — J2512 follow-up to J2494 re-cut #2 (repeated Paranal shot replaced) |
| 11 | OWB | `kKN8Ale42sE` | 2026-11-17 | No (J2494 stopped: uploaded sha not on disk) | PASS | `None` / `None` / `None` | `18.46 / 4.49 / 1.65` | `56.63 / 7.06` | `None` | `PASS` — Scheduled upload (local file sha256 differs from uploaded sha256 per J2493/J2494; J2494 stopped on this one) · stayed-gate warns: pushed still at frame 0 (mean 0–1.5 s frame diff 0.33 < 1.50) — use moving footage; first cut at 4.60s > 3.0s (scene-change detect); spoken text contains meta-promise ("stay, and i'll show you") |
| 12 | OWB | `cwU_0WWeNZ4` | 2026-11-18 | J2494 target #3 (original v01) | PASS | `None` / `None` / `None` | `4.98 / 14.32 / 1.87` | `54.52 / 9.37` | `None` | `PASS` — Currently scheduled upload (v01); J2494 re-cut #3 (v06) and J2512 (v07) below · stayed-gate warns: pushed still at frame 0 (mean 0–1.5 s frame diff 0.46 < 1.50) — use moving footage |
| 13 | OWB | `cwU_0WWeNZ4 (J2494 v06)` | 2026-11-18 | YES — J2494 re-cut #3 (v06) | PASS | `None` / `None` / `None` | `8.29 / 6.91 / 0.53` | `37.66 / 2.76` | `None` | `PASS` — J2494 re-cut #3 of 3 (Ben OK'd; swap in J2514) |
| 14 | OWB | `cwU_0WWeNZ4 (J2512 v07)` | 2026-11-18 | YES — J2494/J2512 re-cut #3 (v07) | PASS | `None` / `None` / `None` | `8.29 / 6.91 / 0.53` | `37.66 / 2.76` | `None` | `PASS` — J2512 follow-up to J2494 re-cut #3 (3.1s still given motion) |
| 15 | OWB | `aAUgIGEuPwQ` | 2026-11-20 | No | PASS | `None` / `None` / `None` | `22.76 / 5.82 / 9.2` | `60.49 / 35.33` | `None` | `PASS` — Scheduled upload |
| 16 | OWB | `rvug71d7Dqk` | 2026-11-21 | No | PASS | `None` / `None` / `None` | `12.17 / 11.83 / 2.89` | `43.73 / 34.22` | `None` | `PASS` — Scheduled upload |
| 17 | OWB | `Dm4xsF1Ateg` | 2026-11-23 | No | PASS | `None` / `None` / `None` | `22.61 / 6.08 / 1.5` | `86.12 / 5.28` | `None` | `PASS` — Scheduled upload |
| 18 | OWB | `xdurJQcoiGM` | 2026-11-25 | No | PASS | `None` / `None` / `None` | `27.35 / 18.29 / 16.72` | `60.83 / 45.53` | `None` | `PASS` — Scheduled upload |
| 19 | OWB | `93JL_IK57EM` | 2026-11-27 | No | PASS | `None` / `None` / `None` | `24.7 / 9.47 / 13.03` | `57.69 / 30.81` | `None` | `PASS` — Scheduled upload |
| 20 | OWB | `MScK2CK2ZFg` | 2026-11-28 | No | PASS | `None` / `None` / `None` | `29.31 / 16.01 / 24.02` | `86.31 / 60.19` | `None` | `PASS` — Scheduled upload |
| 21 | OWB | `xvarZP2aYyE` | 2026-11-30 | No | PASS | `None` / `None` / `None` | `22.32 / 12.17 / 9.52` | `48.65 / 26.25` | `None` | `PASS` — Scheduled upload |
| 22 | OWB | `v6euXX2omz4` | 2026-12-02 | No | PASS | `None` / `None` / `None` | `19.19 / 5.88 / 5.79` | `49.75 / 36.88` | `None` | `PASS` — Scheduled upload |
| 23 | OWB | `BTuL_QBbEgY` | 2026-12-04 | No | PASS | `None` / `None` / `None` | `23.51 / 8.63 / 3.81` | `70.82 / 16.93` | `None` | `PASS` — Scheduled upload |
| 24 | OWB | `C8lPx5N2DwM` | 2026-12-05 | No | PASS | `None` / `None` / `None` | `11.64 / 16.73 / 4.48` | `61.09 / 16.4` | `None` | `PASS` — Scheduled upload |
| 25 | OWB | `lsOCcIYCud0` | 2026-12-07 | No | PASS | `None` / `None` / `None` | `26.36 / 5.59 / 3.27` | `66.5 / 27.23` | `None` | `PASS` — Scheduled upload |
| 26 | OWB | `SWDCZfWZVao` | 2026-12-09 | No | PASS | `None` / `None` / `None` | `16.68 / 8.98 / 2.3` | `47.95 / 20.03` | `None` | `PASS` — Scheduled upload |
| 27 | OWB | `k2kEaA7ICjc` | 2026-12-11 | No | PASS | `None` / `None` / `None` | `11.77 / 6.65 / 0.7` | `57.51 / 11.67` | `None` | `PASS` — Scheduled upload |
| 28 | OWB | `QEoYKIVvKBA` | 2026-12-12 | No | PASS | `None` / `None` / `None` | `11.3 / 3.04 / 1.94` | `44.54 / 30.73` | `None` | `PASS` — Scheduled upload |
| 29 | OWB | `heiGCnGKTkE` | 2026-12-14 | No | PASS | `None` / `None` / `None` | `17.21 / 11.53 / 5.75` | `62.68 / 22.39` | `None` | `PASS` — Scheduled upload |
| 30 | OWB | `f17XCtUmN-g` | 2026-12-16 | No | PASS | `None` / `None` / `None` | `11.23 / 6.64 / 1.47` | `47.41 / 5.43` | `None` | `PASS` — Scheduled upload |
| 31 | HOS | `cLKDiYP55J8` | 2026-11-13 | No | PASS | `None` / `None` / `blur-pad` | `3.67 / 20.86 / 2.66` | `50.73 / 53.13` | t=`0.50s` rows=`[38, 151]` (58.9% H), det out/pic=`3.5 / 14.84`, std out/pic=`49.4 / 66.3`, step=`[0.713, 0.833]`, rat=`[0.6, 1.51]` | `PASS` — Scheduled upload (HOS 007) |
| 32 | HOS | `Wvjd8g0CpzE` | 2026-11-15 | No | PASS | `None` / `None` / `None` | `5.95 / 25.49 / 7.01` | `67.36 / 64.62` | `None` | `PASS` — Scheduled upload (HOS 005) · stayed-gate warns: missing on-screen hook text at frame 0 (hook_edge 0.0000 < 0.005) — stamp 2–4 word hook caption at 0.0s |
| 33 | HOS | `xzKoHg0E0_U` | 2026-11-16 | No | PASS | `None` / `None` / `None` | `7.87 / 29.36 / 7.58` | `62.5 / 42.65` | `None` | `PASS` — Scheduled upload (HOS 004) |
| 34 | HOS | `xgx2lYHhYZM` | 2026-11-17 | No | PASS | `None` / `None` / `None` | `0.91 / 20.27 / 18.1` | `32.75 / 31.27` | `None` | `PASS` — Scheduled upload (HOS 007) |
| 35 | HOS | `ChbsigHD5_o` | 2026-11-18 | No | **FAIL** | `blur-pad` / `blur-pad` / `blur-pad` | `1.59 / 15.99 / 1.07` | `16.47 / 12.49` | t=`0.00s` rows=`[63, 127]` (33.3% H), det out/pic=`1.35 / 15.25`, std out/pic=`14.17 / 43.1`, step=`[0.269, 0.741]`, rat=`[0.053, 1.223]` | `FAIL` — Scheduled upload (HOS 006) · stayed-gate warns: missing on-screen hook text at frame 0 (hook_edge 0.0000 < 0.005) — stamp 2–4 word hook caption at 0.0s |
| 36 | HOS | `Bks_JLId1ew` | 2026-11-21 | No | PASS | `None` / `None` / `None` | `9.25 / 17.78 / 9.16` | `47.08 / 57.61` | `None` | `PASS` — Scheduled upload (HOS 006) |

---

## 3. Per-Frame (`0.00s`, `0.25s`, `0.50s`) Breakdown for Every Row With a Seam Hit or Visual Note

| Row | Ch | Video ID | Air Date | `t` (s) | `kind` | `detail_top` | `detail_centre` | `detail_bottom` | `std_top` | `std_bottom` | `seam_rows` | `detail_outside` | `detail_picture` | `std_outside` | `std_picture` | `seam_step_share` | `seam_detail_ratio` |
|---:|:---:|---|---|---:|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---|---|
| 1 | OWB | `ffYKoNVPoqg` | 2026-11-10 | 0.00 | `blur-pad` | 20.21 | 7.57 | 2.64 | 54.71 | 28.57 | `[72, 117]` | 2.84 | 7.3 | 27.53 | 39.58 | `[0.926, 0.778]` | `[0.381, 0.859]` |
| 1 | OWB | `ffYKoNVPoqg` | 2026-11-10 | 0.25 | `blur-pad` | 20.2 | 7.39 | 10.46 | 54.42 | 36.55 | `[72, 122]` | 3.03 | 7.64 | 28.43 | 39.45 | `[0.907, 0.741]` | `[0.337, 0.311]` |
| 1 | OWB | `ffYKoNVPoqg` | 2026-11-10 | 0.50 | `None` | 20.22 | 7.22 | 10.79 | 54.34 | 36.68 | `None` | — | — | — | — | `—` | `—` |
| 6 | OWB | `gmzaCfJF1gA` | 2026-11-14 | 0.00 | `None` | 14.6 | 7.42 | 2.52 | 91.08 | 24.26 | `None` | — | — | — | — | `—` | `—` |
| 6 | OWB | `gmzaCfJF1gA` | 2026-11-14 | 0.25 | `None` | 16.47 | 7.0 | 12.44 | 80.9 | 51.94 | `None` | — | — | — | — | `—` | `—` |
| 6 | OWB | `gmzaCfJF1gA` | 2026-11-14 | 0.50 | `None` | 16.85 | 6.72 | 12.29 | 70.89 | 51.84 | `None` | — | — | — | — | `—` | `—` |
| 7 | OWB | `gmzaCfJF1gA (J2494 v02)` | 2026-11-14 | 0.00 | `None` | 16.08 | 7.87 | 5.35 | 87.84 | 26.14 | `None` | — | — | — | — | `—` | `—` |
| 7 | OWB | `gmzaCfJF1gA (J2494 v02)` | 2026-11-14 | 0.25 | `None` | 17.0 | 7.58 | 9.38 | 79.75 | 34.24 | `None` | — | — | — | — | `—` | `—` |
| 7 | OWB | `gmzaCfJF1gA (J2494 v02)` | 2026-11-14 | 0.50 | `None` | 17.99 | 7.47 | 9.37 | 65.97 | 33.97 | `None` | — | — | — | — | `—` | `—` |
| 8 | OWB | `HZGTovJu_TQ` | 2026-11-16 | 0.00 | `None` | 13.87 | 10.21 | 12.23 | 34.34 | 19.68 | `None` | — | — | — | — | `—` | `—` |
| 8 | OWB | `HZGTovJu_TQ` | 2026-11-16 | 0.25 | `None` | 7.71 | 8.08 | 4.16 | 35.81 | 25.08 | `None` | — | — | — | — | `—` | `—` |
| 8 | OWB | `HZGTovJu_TQ` | 2026-11-16 | 0.50 | `None` | 7.71 | 8.08 | 4.53 | 35.81 | 26.57 | `None` | — | — | — | — | `—` | `—` |
| 9 | OWB | `HZGTovJu_TQ (J2494 v05)` | 2026-11-16 | 0.00 | `None` | 13.87 | 10.21 | 12.23 | 34.34 | 19.68 | `None` | — | — | — | — | `—` | `—` |
| 9 | OWB | `HZGTovJu_TQ (J2494 v05)` | 2026-11-16 | 0.25 | `None` | 7.71 | 8.08 | 4.16 | 35.81 | 25.08 | `None` | — | — | — | — | `—` | `—` |
| 9 | OWB | `HZGTovJu_TQ (J2494 v05)` | 2026-11-16 | 0.50 | `None` | 7.71 | 8.08 | 4.53 | 35.81 | 26.57 | `None` | — | — | — | — | `—` | `—` |
| 12 | OWB | `cwU_0WWeNZ4` | 2026-11-18 | 0.00 | `None` | 4.98 | 14.32 | 1.87 | 54.52 | 9.37 | `None` | — | — | — | — | `—` | `—` |
| 12 | OWB | `cwU_0WWeNZ4` | 2026-11-18 | 0.25 | `None` | 4.86 | 14.81 | 1.9 | 54.2 | 8.79 | `None` | — | — | — | — | `—` | `—` |
| 12 | OWB | `cwU_0WWeNZ4` | 2026-11-18 | 0.50 | `None` | 5.02 | 15.06 | 1.77 | 54.2 | 8.23 | `None` | — | — | — | — | `—` | `—` |
| 13 | OWB | `cwU_0WWeNZ4 (J2494 v06)` | 2026-11-18 | 0.00 | `None` | 8.29 | 6.91 | 0.53 | 37.66 | 2.76 | `None` | — | — | — | — | `—` | `—` |
| 13 | OWB | `cwU_0WWeNZ4 (J2494 v06)` | 2026-11-18 | 0.25 | `None` | 8.42 | 7.1 | 0.54 | 37.65 | 3.31 | `None` | — | — | — | — | `—` | `—` |
| 13 | OWB | `cwU_0WWeNZ4 (J2494 v06)` | 2026-11-18 | 0.50 | `None` | 8.63 | 7.13 | 0.41 | 37.72 | 3.22 | `None` | — | — | — | — | `—` | `—` |
| 16 | OWB | `rvug71d7Dqk` | 2026-11-21 | 0.00 | `None` | 12.17 | 11.83 | 2.89 | 43.73 | 34.22 | `None` | — | — | — | — | `—` | `—` |
| 16 | OWB | `rvug71d7Dqk` | 2026-11-21 | 0.25 | `None` | 12.3 | 11.8 | 3.14 | 43.59 | 34.17 | `None` | — | — | — | — | `—` | `—` |
| 16 | OWB | `rvug71d7Dqk` | 2026-11-21 | 0.50 | `None` | 12.26 | 11.71 | 3.2 | 43.46 | 34.06 | `None` | — | — | — | — | `—` | `—` |
| 31 | HOS | `cLKDiYP55J8` | 2026-11-13 | 0.00 | `None` | 3.67 | 20.86 | 2.66 | 50.73 | 53.13 | `None` | — | — | — | — | `—` | `—` |
| 31 | HOS | `cLKDiYP55J8` | 2026-11-13 | 0.25 | `None` | 3.64 | 21.05 | 3.41 | 51.22 | 52.37 | `None` | — | — | — | — | `—` | `—` |
| 31 | HOS | `cLKDiYP55J8` | 2026-11-13 | 0.50 | `blur-pad` | 3.71 | 21.18 | 3.69 | 51.48 | 56.15 | `[38, 151]` | 3.5 | 14.84 | 49.4 | 66.3 | `[0.713, 0.833]` | `[0.6, 1.51]` |
| 35 | HOS | `ChbsigHD5_o` | 2026-11-18 | 0.00 | `blur-pad` | 1.59 | 15.99 | 1.07 | 16.47 | 12.49 | `[63, 127]` | 1.35 | 15.25 | 14.17 | 43.1 | `[0.269, 0.741]` | `[0.053, 1.223]` |
| 35 | HOS | `ChbsigHD5_o` | 2026-11-18 | 0.25 | `blur-pad` | 1.1 | 15.94 | 1.05 | 14.94 | 16.23 | `[64, 128]` | 1.16 | 15.32 | 16.62 | 42.93 | `[0.389, 0.769]` | `[0.037, 1.242]` |
| 35 | HOS | `ChbsigHD5_o` | 2026-11-18 | 0.50 | `blur-pad` | 1.09 | 15.75 | 1.09 | 15.01 | 26.18 | `[64, 129]` | 1.1 | 15.13 | 18.08 | 42.59 | `[0.398, 0.806]` | `[0.034, 1.196]` |
