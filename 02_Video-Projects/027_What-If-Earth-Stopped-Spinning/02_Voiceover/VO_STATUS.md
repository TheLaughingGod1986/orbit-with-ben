# VO status — 027 long (What If Earth Stopped Spinning?)

| Field | Value |
|---|---|
| Status | PASS |
| Script | 01_Script/earth_spin_script_master_v01.md |
| Claude PASS | #99 6002694271 (long + 3 Shorts) |
| Voice | Ben Orbit Narrator (`kDch6ACCIpqgQ0NsU9kk`) |
| Model | `eleven_v3` |
| Settings | {"stability": 0.34, "similarity_boost": 0.78, "style": 0.42, "speed": 1.04, "use_speaker_boost": true} |
| Chapters | 6 (gap 0.7s) |
| Words | 1178 |
| Spoken chars | 6328 |
| Duration | 460.38s (7.67 min) |
| LUFS integrated | -19.7 |
| mean / peak | -22.9 / -3.7 dB |
| Credits before / after | 132400 / 135184 of 209536 (delta 2784) |
| Scribe match | 98.9% (13 mismatches: British spellings and spoken years) |
| SHA-256 mp3 | `e340171affc03dac5156094a9c8a37be58638c154a01ec47dbd4b2df04aeaf44` |
| Audio (Mini only, not in git) | `02_Voiceover/earth_spin_vo_v01.mp3`, `.wav`, `parts/earth_spin_vo_v01/ch00–ch05.wav` |
| Made | 2026-10-05T21:46:37+0100 |

## Text files (J0035, 8 Oct 2026)

`vo_take.py` wrote only the TAKE json and `stt/earth_spin_vo_v01/`. `words.json`, `chapters_index.json`, `vo_check.*` and `script_whisper_diff.json` are built from those two files, with no new take and no spend. Chapter start and end times come from the TAKE chapter durations plus the 0.7 s gaps in `parts_concat.txt` (they sum to 460.38 s).
