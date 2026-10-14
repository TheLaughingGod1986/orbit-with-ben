# 024 Light Speed v05c: NUMBER overlays (J0147)

Cursor (stand-in for Codex on a `chart` job), 12 Oct 2026. Advisory: Chief scores the gate.

- Cut: `/private/tmp/024_LightSpeed_full_rough_v05c.mp4` (sha256 in `SHA256.txt`). v05b's picture (`light024_full_work_v05b/picture.mp4`, with its chapter cards and subscribe cue) plus 23 labels; audio stream copied from v05b (`audio_v05c.json`: same md5). No cut, VO, bed or graphic change, no spend.
- Builder: `../_overlay_light_speed_v05c.py` (`--plan` lists every label with its time, place and source check). Renders: `code_graphic_024_row<row>_<k>.png`, one per label, listed per cut in `cuts_v05c.json` (`overlays`) and in `overlays_v05c.json`.
- Style: the chapter-card pill (navy 23,36,55 at 86%, white Arial Bold 60–84 px), in on the VO word's start with a 0.35 s fade and rise, out with a 0.3 s fade by the next cut or 4 s. Every label is 4 words or fewer, the VO's own words, with spoken numbers as numerals.
- Gates: `picture_qa_v05c.txt` PASS (0 of 111 cuts fail), `polish_gate_v05c.txt` PASS (0 of 111). Stills: `overlay_stills_v05c.jpg`.

## Every row of the prep table

| Film time | Row | Label(s) | Source check |
|---|---|---|---|
| 0:07.7, 0:11.0 | 2 | 1 year → 7 years | SOURCES: 7.09 Earth years per ship year at 0.99c |
| 0:53.4, 1:01.0, 1:03.6 | 8 | 7 millionths · about 46 · 38 millionths a day | Ashby 2003: 7.2 / 45.9 / 38.7 µs a day |
| 1:15.7 | 9 | 10 kilometers every day | **FLAG:** Ashby gives about 11.6 km a day; the VO says "around ten" (label matches the VO) |
| 1:25.2 | 11 | 1971 | Hafele & Keating (flights 1971) |
| 2:37.4–2:55.6 | 16 | 10% · 90% · 99% + 7 to 1 · 99.99% + 70 to 1, under each dial | SOURCES gamma 2.294 and 7.089; 0.1c and 0.9999c are formula only (1.005, 70.7), with no SOURCES row |
| 3:13.0 | 17 | 660 meters | Frisch & Smith 1963: about 660 m |
| 3:19.7 | 18 | 1963 | Frisch & Smith 1963 |
| 3:58.5, 4:01.3 | 22 | 20 years (over the blue home dial) · about 3 years | formula: 10 ly at 0.99c gives 20.2 yr on Earth and 2.85 yr on the ship; no SOURCES row |
| 4:36.7, 4:38.9 | 25 | 10 light-years → one and a half | 10/7.09 = 1.41 ly (VO "about one and a half") |
| 5:42.2, 5:44.4 | 30 | 90 to 99% → nearly five times | SOURCES: 4.7×. The prep table's "five times as much" dropped the VO's "nearly", so the label keeps it |
| 6:53.6 | 35 | over 20 years | SOURCES: 22.4 yr crew time |
| 7:02.3 | 36 | 100,000 years | SOURCES: about 100,000 yr on Earth |

## For Chief

1. **0:11.4–0:12.97 is full black in v05b** (row 2's Earth Views stretch runs into the source's own fade). It's already in `freeze_black_v05b.txt`, and the gates pass it under `reviewed_ok`. It leaves "7 years" on screen for only 0.4 s, on a shot already fading out. Fixing it means a new offset for row 2 (a picture change, not an overlay). Chief to decide.
2. **The dial labels** in row 16 come in on the spoken speed. Each dial lights about 1–2 s later, so a label shows briefly under a grey dial before it lights.
3. **"660 meters" sits low over the clouds.** A top pill on the black sky tripped polish_gate's split-panel gutter check at 3:14 (first render), so it was moved.
4. **Three spoken numbers have no SOURCES row,** only the formula: 10% and 99.99% (with "70 to 1"), and the twin's 20 and 3 years. Worth a Gemini row before upload.
5. **"10 kilometers every day"** under-states the source's 11.6. The VO is locked, so the label follows it.
