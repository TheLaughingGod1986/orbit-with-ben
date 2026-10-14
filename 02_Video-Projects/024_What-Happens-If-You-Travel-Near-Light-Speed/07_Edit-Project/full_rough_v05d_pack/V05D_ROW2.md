# 024 Light Speed v05d: row 2 in-point (J0149)

Cursor, 12 Oct 2026. Chief's v05c review: 22 of 23 overlays PASS, row 2 FAIL ("7 years" on screen 0.4 s before the Earth Views stretch went to full black at 0:11.4–0:12.97).

- **Change:** row 2's second shot (0:09.67–0:13.03) runs Earth Views from **75.0 s** (was 122.0 s). It's the same source: the Soyuz over a desert coast, mean luma about 114 and steady from 74.8 to 78.6 s (the source fades to black from 123.7 s). Every other Earth Views stretch (14, 50, 110, 176) is 25 s or more away, so the film still has 5 stretches.
- **"7 years"** is in at 10.98 s (the VO word) and holds to 12.80 s, 1.82 s on bright picture, clear of the 12.83 s crossfade into row 3. "1 year" and the other 21 labels are as v05c.
- **Unchanged:** the VO, the bed and the mix (`audio_v05d.json`: the audio md5 matches v05c), and the other 110 cuts (v05b segments reused as is; only `seg_002` was re-rendered).
- **reviewed_ok:** `reviewed_ok_v05d.json` is v05c's list without `Earth_Views…@122`. Row 2 passes polish_gate with no reviewed-ok entry.
- **Gates:** `picture_qa_v05d.txt` PASS (0 of 111 fail), `polish_gate_v05d.txt` PASS (0 of 111), `clip_check_py.txt` PASS, no cut inside a word. `freeze_black_v05d.txt` shows no black at 0:11; the only black left is the 3:29 Artemis night launch (reviewed ok) and the end fade.
- **Stills:** `row2_still_v05d.jpg` (0:11.9) and `strip_0m06_0m14_v05d.jpg`.
- **Cut:** `07_Edit-Project/024_LightSpeed_full_rough_v05d.mp4` (a copy is in `/private/tmp`), sha256 in `SHA256.txt`.
- **Builders:** `../_assemble_light_speed_full_v05d.py` (picture), `../_overlay_light_speed_v05d.py` (labels), `run_v05d.sh`.

Parked for Chief: 024 v05d row 2.
