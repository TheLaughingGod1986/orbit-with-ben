# J0991 — 029 Betelgeuse Shorts v04 Repair Report (27 Oct 2026)

- **Worker:** `gemini` (`gemini-agy`, worker mode; no final Chief OK/PASS, no upload, no YouTube/Buffer mutation)
- **Film:** `029_Is-Betelgeuse-About-To-Explode` (`vP1BbqZ_dnM`, Private, `publishAt` Sun 6 Dec 2026 18:00 London)
- **Prerequisite for:** `J0961` (remains blocked pending elected-Chief review of changed audio + Wednesday opening, applicable changed-picture watch card, and Chief's hash amendment on `J0961`)
- **Spend:** £0 (no ElevenLabs, Vertex, or Flow generation spend)
- **Assembler script:** `02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/10_Shorts/_assemble_029_shorts_v04.py`

---

## 1. Per-Cut Before (v03) vs After (v04)

| Cut | Air Date (11:30Z) | Metric | v03 (Before) | v04 (After) | Gate Requirement | Verdict |
|---|---|---|---|---|---|---|
| **Wed 9 Dec** (`wed09_great_dimming`) | `2026-12-09` | Encoded AAC Integrated Loudness | `-15.0 LUFS` (**FAIL**) | **`-14.1 LUFS`** | `-14.0 ± 0.5 LUFS` | **PASS** |
| | | Encoded AAC True Peak | `-1.5 dBTP` (**FAIL**) | **`-2.0 dBTP`** | `≤ -1.6 dBTP` | **PASS** |
| | | Opening Plate (`0.00–2.69 s`) | `sphere_jan.jpg` on flat navy (`44%` bg match to `f17XCtUmN-g`, 16 Dec — **FAIL**) | **`gemini_night.jpg`** (`0.675×` downscale NOIRLab Gemini North Orion night-sky starfield, approved `ok` in `PLATE_BOARDS_v03.json` & `cuts_v03b.json`) + **ESO VLT/SPHERE Betelgeuse** (`sphere_jan.jpg → sphere_dec.jpg`) dimming in centre (`max bg match 12.5%`, `< 3.9%` on `f17XCtUmN-g`) | `< 30%` warn / `< 40%` fail | **PASS** |
| | | Motion `0–1s` / Frame-0 Diff `0–1.5s` | `13.66` / `1.97` | **`15.95` / `4.62`** | `≥ 10.0` / `≥ 1.50` | **PASS** |
| | | First Cut (`scdet`) / Visor Frac | `2.70 s` / `0.0` | **`2.70 s` / `0.0`** | `≤ 3.0 s` / `< 0.001` | **PASS** |
| | | Loop Diff (`s10_end` vs Frame 0) | `1.19` | **`3.09`** | `≤ 15.0` | **PASS** |
| **Fri 11 Dec Test A** (`fri11_opening_testA`) | `2026-12-11` | Encoded AAC Integrated Loudness | `-14.4 LUFS` (PASS) | **`-14.1 LUFS`** | `-14.0 ± 0.5 LUFS` | **PASS** |
| | | Encoded AAC True Peak | `-1.5 dBTP` (**FAIL**) | **`-2.1 dBTP`** | `≤ -1.6 dBTP` | **PASS** |
| | | Video Stream | v03 approved stream | **Bit-copied from v03** (`-c:v copy`, identical picture/cuts/33.9s Test A exemptions) | Unchanged picture | **PASS** |
| **Mon 14 Dec** (`mon14_half_moon_daylight`) | `2026-12-14` | Encoded AAC Integrated Loudness | `-14.4 LUFS` (PASS) | **`-14.1 LUFS`** | `-14.0 ± 0.5 LUFS` | **PASS** |
| | | Encoded AAC True Peak | `-1.5 dBTP` (**FAIL**) | **`-2.0 dBTP`** | `≤ -1.6 dBTP` | **PASS** |
| | | Video Stream | v03 approved stream | **Bit-copied from v03** (`-c:v copy`, identical picture/cuts) | Unchanged picture | **PASS** |

---

## 2. Full Gate Verdicts on v04 Masters

| Gate / Check | Wed 9 Dec (`029_short_wed09_great_dimming_v04.mp4`) | Fri 11 Dec Test A (`029_short_fri11_opening_testA_v04.mp4`) | Mon 14 Dec (`029_short_mon14_half_moon_daylight_v04.mp4`) |
|---|---|---|---|
| `gate_shorts_open.py check --air-date <date>` | **PASS** (`dur=22.7s`, `I=-14.1 LUFS`, `TP=-2.0 dBTP`, `motion=16.0`, `f0diff=4.62`, `cut1=2.70s`, `vo_onset=0.05s`, `dhash=577131231b1b0f05`, `visor=0.0`, `near_opens=[]`) | **PASS** (`dur=33.9s` Test A exception, `I=-14.1 LUFS`, `TP=-2.1 dBTP`, `motion=13.2`, `f0diff=5.94`, `cut1=2.23s`, `vo_onset=0.08s`, `dhash=90f0f8f0f0f0f090`, `visor=0.0008`, `near_opens=[]`) | **PASS** (`dur=23.9s`, `I=-14.1 LUFS`, `TP=-2.0 dBTP`, `motion=30.7`, `f0diff=7.57`, `cut1=3.00s`, `vo_onset=0.06s`, `dhash=173b717179380f27`, `visor=0.0`, `near_opens=[]`) |
| `sfx_kit.py level` | **PASS** (`VO -16.4 LUFS`, `Bed -34.3 LUFS`, `SFX -42.0 LUFS`, `1 hits`) | **PASS** (`VO -16.6 LUFS`, `Bed -34.7 LUFS`, `SFX -38.6 LUFS`, `2 hits`) | **PASS** (`VO -15.7 LUFS`, `Bed -33.7 LUFS`, `SFX -37.7 LUFS`, `2 hits`) |
| `music_gate.py` | **PASS** (`betelgeuse_score_bed_v01.mp3`, full runtime, unique fingerprint) | **PASS** (`betelgeuse_score_bed_v01.mp3`, full runtime, unique fingerprint) | **PASS** (`betelgeuse_score_bed_v01.mp3`, full runtime, unique fingerprint) |
| `polish_gate.py` | **PASS** (`0 of 8 rows failed`, max upscale `1.90×`, `s01_orion_sphere` upscale `0.675×`) | **PASS** (`0 of 12 rows failed`, max upscale `1.90×`) | **PASS** (`0 of 8 rows failed`, max upscale `1.995×`) |
| `picture_qa.py` | **PASS** (`0 of 8 cuts fail`) | **PASS** (`0 of 12 cuts fail`) | **PASS** (`0 of 8 cuts fail`) |
| `ocr` (all frames @ 30 fps) | **PASS** (`681 frames`, `0 banned hits`) | **PASS** (`1016 frames`, `0 banned hits`) | **PASS** (`718 frames`, `0 banned hits`) |
| `thumb_preview.py short --score` | **PASS** (`saturation=195.7`, `near_black=2%`, byte-identical to v03 cover) | **PASS** (`saturation=190.4`, `near_black=0%`, byte-identical to v03 cover) | **PASS** (`saturation=31.9`, `near_black=5%`, byte-identical to v03 cover) |
| `caption_title_safe` & `loop_diff` | **PASS** (`loop_diff=3.09 ≤ 15.0`) | **PASS** (`loop_diff=1.19 ≤ 15.0`) | **PASS** (`loop_diff=2.62 ≤ 15.0`) |
| `npm run youtube:package -- --dry-run` | **PASS** (`PACKAGE_MANIFEST_v04.json` & `PACKAGE_MANIFEST.json`, `PACKAGE_MANIFEST_v03.json` preserved) | **PASS** (`PACKAGE_MANIFEST_v04.json` & `PACKAGE_MANIFEST.json`, `PACKAGE_MANIFEST_v03.json` preserved) | **PASS** (`PACKAGE_MANIFEST_v04.json` & `PACKAGE_MANIFEST.json`, `PACKAGE_MANIFEST_v03.json` preserved) |

---

## 3. Exact SHA256 Hashes (Verified Across All 5 Durable Paths)

All 6 files below are verified byte-identical across:
1. `02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/10_Shorts/<slug>/06_Final-Exports/`
2. `~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/`
3. `~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/<stem>/`
4. `/Volumes/data/mac-mini-archive/youtube-staging/029/shorts_v04/`
5. `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/029_shorts_v04/`

| File | SHA256 | Bytes |
|---|---|---:|
| `029_short_wed09_great_dimming_v04.mp4` | `e0459b017ddafdf84229784c170285d4c5694507140523e92043ab2109b8f3c3` | `20,762,566` |
| `029_short_wed09_great_dimming_v04_PHONE.mp4` | `eeb6196d5d474954eabbf8d87bbde041c97047948687af40eb544d83f8516d4d` | `2,673,832` |
| `029_short_fri11_opening_testA_v04.mp4` | `ff4194857a027cfc5f93551ef398125276e6bcfb9cd3ce2fd18d8ee1134e2405` | `41,552,231` |
| `029_short_fri11_opening_testA_v04_PHONE.mp4` | `b0511e06d8dcd8e5945a5aa3b458d70393080d2b75c2c3686ca14026a5f36c30` | `5,911,664` |
| `029_short_mon14_half_moon_daylight_v04.mp4` | `31f362f4437b4ca56ec16b8abef1dce4c65fb5a5c6c7b5b4e2ba39229a33efd5` | `23,611,451` |
| `029_short_mon14_half_moon_daylight_v04_PHONE.mp4` | `04947ca92e610b6bc6adb49f1ed5cc598a1e6e3607e6e29925b3b4a32496db22` | `3,296,201` |

All v03 files (`fc3c1b30be442e9a8853ba9f99c632f8e9fe3c1a23fa0860df6b24f6b0e9e5a4`, `c12dc1774e689b17f757f1b6c0e9ad58516f8dd4add4075e7316970196860939`, `1e3d9ba6830b4e28991216b1404b66cce4e4401f075bae06a7d7ee5624c63a4e` and their `_PHONE.mp4` copies) and `PACKAGE_MANIFEST_v03.json` manifests are verified untouched.

---

## 4. Next Steps for Elected Chief

1. Review changed audio on all three v04 cuts and the changed `0.00–2.69 s` opening + `20.71–22.71 s` end-card loop hold on `029_short_wed09_great_dimming_v04.mp4`.
2. Set any required changed-picture watch card for `029_short_wed09_great_dimming_v04_PHONE.mp4` (Ben's v03 approvals are preserved as v03 records and are not claimed as approval of v04).
3. Accept `J0991`, amend `J0961` with the exact v04 SHA256 hashes above, and release `J0961` after the watch resolves.
