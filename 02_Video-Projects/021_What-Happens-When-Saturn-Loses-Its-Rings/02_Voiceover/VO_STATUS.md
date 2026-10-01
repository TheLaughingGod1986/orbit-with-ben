# VO status — Saturn rings

| Field | Value |
|---|---|
| Status | **v03 tightened — STOP for Ben voice sign-off** (1 Oct 13:39 London) |
| Spoken text | `parts/saturn_rings_vo_v02.txt` (words unchanged) |
| Voice | Ben Orbit Narrator (`kDch6ACCIpqgQ0NsU9kk`) |
| Model | `eleven_v3` via `orbit_voice.py` (source v02) |
| Source duration (v02) | 563.42s (9:23) |
| **Tightened duration (v03)** | **523.27s (8:43)** |
| Tempo factor | **1.000** (pause trim alone landed in 8:30–8:50) |
| Pitch method | n/a this pass — would use `ffmpeg atempo` (pitch-preserving) if needed, max 1.05 |
| Master wav | `parts/saturn_rings_vo_v03_tightened.wav` |
| Master m4a | `parts/saturn_rings_vo_v03_tightened.m4a` |
| Listen wav | `OWB UAT/saturn_long_vo_v03_tightened.wav` |
| Listen m4a | `OWB UAT/saturn_long_vo_v03_tightened.m4a` |
| Report | `parts/VO_V03_TIGHTEN_REPORT.md` |
| Meta | `parts/_tighten_v03/TIGHTEN_META.json` |
| Updated | 2026-10-01 13:44 BST |

v02 masters kept on disk for rollback. Do not force-commit audio (gitignored).

**Next:** Ben voice sign-off → then shot list v02 on v03 timings. No downloads / generation until then.
