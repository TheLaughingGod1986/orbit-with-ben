# 029 Is Betelgeuse About to Explode? — Full Rough v01 Master Copies (`J0823`, 22 Oct 2026)

Cut is `029_Betelgeuse_full_rough_v01.mp4` (`517.10 s`, `63` cuts, `-14.0 LUFS` / `-1.2 dBTP`, **£0 spend**).
Same bytes verified in all three locations:

`b406543e6e5bdde2be93641454e46ea9df84050dd8366890f169e147c676e0ce`

| Copy | Path | SHA-256 |
|---|---|---|
| Local build | `/private/tmp/029_Betelgeuse_full_rough_v01.mp4` | `b406543e6e5bdde2be93641454e46ea9df84050dd8366890f169e147c676e0ce` |
| OWB UAT (Ben's watch) | `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/029_Betelgeuse_full_rough_v01.mp4` | `b406543e6e5bdde2be93641454e46ea9df84050dd8366890f169e147c676e0ce` |
| NAS youtube-staging | `/Volumes/data/mac-mini-archive/youtube-staging/029/029_Betelgeuse_full_rough_v01.mp4` | `b406543e6e5bdde2be93641454e46ea9df84050dd8366890f169e147c676e0ce` |

## Orbit Beats Restored from Existing Omni Renders (£0)

1. **`r12_orbit_thumb` (`123.16–130.42 s`, `7.26 s`, Ch 2 *The Great Dimming*):**
   - Reuses `022` `sun_orbit_row67_omni_v01.mp4` (`offset=1.80 s`, `1.50x` upscale).
   - Orbit floats above Earth's cloud horizon looking up at the huge orange-red giant star and lifting a hand (*"The question went all around the world. Was this it? Was Betelgeuse about to explode?"*).
2. **`r26_orbit_flare` (`282.16–286.08 s`, `3.92 s`, Ch 4 *The Night It Goes*):**
   - Reuses `026` `orbit_thumb_omni_v01.mp4` (`offset=1.50 s`, `1.50x` upscale).
   - Orbit in the night starfield raises his hand in front of his visor before a blazing white-blue flare star (*"You could see it in broad daylight. At night, it would outshine..."*).

## All Gates PASS

- **`clip_check.py`:** `clip_check: 63 rows — PASS`
- **`picture_qa.py`:** `PASS: 0 of 63 cuts fail, 12 to look at`
- **`polish_gate.py`:** `PASS: 0 of 63 rows failed, 4 to look at`
- **`music_gate.py`:** `music gate PASS: betelgeuse_score_bed_v01.mp3, 517.3 s, about 75.0 BPM, brief Pace: 68-78 BPM`
- **`sfx_kit.py level`:** `PASS (vo -14.9 LUFS, sfx -31.8 LUFS, 38 hits, 0 fails)`
- **Per-chapter teaching gate (`TEACHING_GATE_v01.md`):** `6/6` chapters PASS on `NUMBER` and `WORDS` (22 house pills).
- **Back-to-back code graphics:** `0` (`r21_neutron` Hubble Crab pulsar still separates `r21_hero` and `r21_bh`; `r22_subscribe` `gemini_night.jpg` push + Subscribe pill separates `r21_bh` and `r23_paranal`).
- **Full-frame card in `0:00–0:30`:** `0`.

Parked for Chief review before Ben's watch. Never uploaded.
