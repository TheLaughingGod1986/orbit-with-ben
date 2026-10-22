# OWB 028 Gliese 710 — Part Roughs v01 Pack (`J0855`, 22 Oct 2026)

Prepared by Gemini (`gemini`) under `J0855` after Chief's `J0850` KEEP/FIX rulings. **Parked for Chief (`parked for Chief: 028 part roughs v01 review`).**

## 1. Minted Plates Ruling & `r17_pitch` Retake (`J0850` -> `J0855`)

- **KEEP `r08_orbit_binoculars`** (`orbit_binoculars_omni_v01.mp4`, Vertex Omni, `a7793cfce266c192`): canonical Orbit on dark hill under stars (no planet), sweeps sky with binoculars.
- **KEEP `r11_night_road`** (`night_road_veo_v01.mp4`, Flow Veo 3.1 Quality, `6dfb64f683998705`): straight empty night road, headlights approach and grow; `94.36–101.20 s` covered by the planned star cutaway (`eso_lasilla_ntt.mp4`) and `101.20–109.20 s` (`8.00 s`) on `night_road_veo_v01.mp4`.
- **KEEP `r23_orbit_ice`** (`orbit_ice_omni_v01.mp4`, Vertex Omni, `8c509d86cc18dbed`): canonical Orbit in deep space among dark grey Oort ice lumps (no planet).
- **FIX -> KEEP `r17_pitch` Take 2 (`football_pitch_veo_v02.mp4`, promoted to `football_pitch_veo_v01.mp4`)**:
  - Minted 1 Flow Veo 3.1 Fast retake (`10 cr`, `20,840 -> 20,830` on `benoats@googlemail.com`, `_mint_028_r17_retake_v02.py`).
  - SHA-256: `c2a0aa340d3a0486fe1fb9d553b69b3c88c8242ece6bcce015d780320d004450` (`8.0 s`, `5,449,736 B`, `0` freezes `>=0.8s`, audio stripped).
  - Camera glides low and slow along the white halfway line on empty dusk turf towards the centre circle; no goals or goal nets anywhere in frame, soft distant stands, no text/logos/people.
  - Contact sheet updated: `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/_evidence/028_keep_fix_v01_contact.jpg`.

---

## 2. Part Roughs v01 Summary (7 Parts, `0.00–472.84 s`, 62 Cuts, 22 Teaching Overlays)

All 7 chapter part roughs (`part00`–`part06`) were assembled by `_assemble_028_part_roughs_v01.py` from `PLATE_BOARDS_v02.json` on the locked VO (`02_Voiceover/star_coming_vo_v01.wav`, last spoken word at `469.34 s` + `2.5 s` hold + `1.0 s` fade = `472.84 s`), normalized to `-14 LUFS`:

- **No back-to-back code graphics anywhere** across the entire 62-cut timeline (including `r19_subscribe` on real moving star-trails footage + house `SUBSCRIBE` pill, and real moving cutaways breaking the two `>20 s` code beats `r20_21_oort_shell` and `r24_25_shower`).
- **Visual/camera/label change every 3–4 s** (internal sentence-pause reframes on multi-sentence code beats + all 22 `J0504` teaching overlay pills + 6 chapter lower-third cards).
- **First chapter card at `0:42.50`** (`The Star Heading Our Way` on `part01` `r06_milky_way`), strictly after `0:30` per Chief's `J0842` ruling (no chapter card in `0:00–0:30`).
- **Strict one-label-at-a-time**: harvest corner credits are suppressed whenever any teaching pill, chapter card, or `SUBSCRIBE` pill is on screen, and code graphics carry only their single bottom credit line (`NASA/SDO · CGI` or `NASA · CGI`).

| Part | Chapter | Span (`s`) | Dur (`s`) | Cuts | `picture_qa` | `polish_gate` | MP4 (`/private/tmp/028_part_roughs_v01/`) | SHA-256 (first 12) | Contact Sheet |
|---|---|---|---:|---:|---|---|---|---|---|
| `part00` | `0 Open` | `0.00–42.32` | `42.33` | `6` | **PASS** (`0 fail, 1 warn`) | **PASS** (`0 fail`) | `028_Gliese710_part00_rough_v01.mp4` | `1fcb12e72dec` | `part00_rough_v01_contact_sheet.jpg` |
| `part01` | `1 The Star Heading Our Way` | `42.32–126.47` | `84.13` | `10` | **PASS** (`0 fail, 2 warn`) | **PASS** (`0 fail`) | `028_Gliese710_part01_rough_v01.mp4` | `32df3789ef05` | `part01_rough_v01_contact_sheet.jpg` |
| `part02` | `2 How Close Will It Come?` | `126.47–209.89` | `83.43` | `11` | **PASS** (`0 fail, 2 warn`) | **PASS** (`0 fail`) | `028_Gliese710_part02_rough_v01.mp4` | `d468c4957ce3` | `part02_rough_v01_contact_sheet.jpg` |
| `part03` | `3 Into the Oort Cloud` | `209.89–281.16` | `71.27` | `9` | **PASS** (`0 fail, 1 warn`) | **PASS** (`0 fail`) | `028_Gliese710_part03_rough_v01.mp4` | `43feec0c5f15` | `part03_rough_v01_contact_sheet.jpg` |
| `part04` | `4 The Comet Shower` | `281.16–335.42` | `54.27` | `7` | **PASS** (`0 fail, 1 warn`) | **PASS** (`0 fail`) | `028_Gliese710_part04_rough_v01.mp4` | `3bf08604962d` | `part04_rough_v01_contact_sheet.jpg` |
| `part05` | `5 A New Brightest Star` | `335.42–377.80` | `42.37` | `8` | **PASS** (`0 fail, 1 warn`) | **PASS** (`0 fail`) | `028_Gliese710_part05_rough_v01.mp4` | `5c763f30503b` | `part05_rough_v01_contact_sheet.jpg` |
| `part06` | `6 It Has Happened Before` | `377.80–472.84` | `95.03` | `11` | **PASS** (`0 fail, 2 warn`) | **PASS** (`0 fail`) | `028_Gliese710_part06_rough_v01.mp4` | `263bbf38e661` | `part06_rough_v01_contact_sheet.jpg` |
| **Total** | **7 parts** | **`0.00–472.84`** | **`472.83`** | **62** | **7/7 PASS (`0 fail`)** | **7/7 PASS (`0 fail`)** | — | — | `part_roughs_v01_pack/` |
