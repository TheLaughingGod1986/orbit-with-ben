# J1100 Batch C (`S2`, `S5`, `S6`) v07 Delivery & h43-LOOP Verification Report

- **Job:** `J1100` (`OWB:027`, `OWB:028`)
- **Worker:** `gemini` (demonstrated `audio_input` capability recorded via `chief_relay.py capabilities`)
- **Status:** Parked for Chief replacement review (`PARKED_FOR_CHIEF_REPLACEMENT_REVIEW`). No YouTube upload, swap, schedule/privacy change, or new spend beyond the approved S2/S5 pickup takes. `v01`–`v06` untouched.

---

## 1. Summary of Repairs & Rulings Addressed

### A. `h43-LOOP` Provenance & Caption-Free Loop Tail (`jobs/reviews/J1100/loop_h43.py`)
Implemented and passed the five-step `h43-LOOP` gate across all three Shorts (`S2_027_emwQsPxnRGM_v07.mp4`, `S5_028_jJ5LkFGyzLI_v07.mp4`, `S6_028_X768qs8sNQs_v07.mp4`):
1. **Step 1 (Provenance & Filtergraph Diff):** Each Short renders a text-free base (`*_v07_base.mp4`) and final (`*_v07.mp4`) from the identical `picture_raw.mp4` (`picture_sha256 == base_picture_sha256`) and identical filtergraph, differing solely by `overlay=0:0:enable='0'` vs `overlay=0:0:enable='1'`.
2. **Step 2 (Base Loop < 2.0):** Rebuilt the 1.0 s (30-frame) silent loop tail from the opening shot's first 30 frames (`[29..5, 2, 2, 2, 2, 0]`) with matched `bt709`/`tv` color space across `s00..s07`:
   - **S2 (`earth_equator_weight_v07`):** `base_f0_vs_last_180x320 = 0.5669`, `base_f0_vs_last_270x480 = 0.7975`, `c37_base = {"whole": 0.50, "masked": 0.57}`, `c37_final_masked = 0.57` (**PASS**, all `< 2.0`).
   - **S5 (`028_short_fri04_scale_v07`):** `base_f0_vs_last_180x320 = 0.6279`, `base_f0_vs_last_270x480 = 0.8687`, `c37_base = {"whole": 0.59, "masked": 0.62}`, `c37_final_masked = 0.62` (**PASS**, all `< 2.0`).
   - **S6 (`028_short_lift_night_sky_35yr_v07`):** `base_f0_vs_last_180x320 = 0.7214`, `base_f0_vs_last_270x480 = 0.9884`, `c37_base = {"whole": 0.65, "masked": 0.65}`, `c37_final_masked = 0.64` (**PASS**, all `< 2.0`).
3. **Step 3 (Final vs Base Pixel Consistency < 1.0):**
   - `final_last_vs_base_last_180x320 = 0.0` and `270x480 = 0.0` on all three (`< 1.0`).
   - `final_f0_vs_base_f0_outside_text_bboxes_pad8`: **S2** `0.6400`, **S5** `0.7112`, **S6** `0.6446` (all `< 1.0`).
4. **Step 4 (OCR on Frame 0, 30-Frame Silent Tail, and Word-for-Word Spoken Captions):**
   - Frame-0 OCR matches locked hooks (`0.5% LIGHTER AT THE EQUATOR`, `HOW CLOSE TO THE SUN?`, `3x BRIGHTER THAN SIRIUS`).
   - All 30 tail frames (`tail_frames_checked: 30`) on all three Shorts have `tail_nonempty_hits = []` (zero caption or hook text over the 1.0 s silent tail).
   - Spoken captions match final AAC word-for-word (`s5_caption_check = true`: `HOW CLOSE WILL` -> `GLIESE 710 COME` -> `TO THE SUN?`, no comma).
5. **Step 5 (Diagnostic Final Whole-Frame Diff):** Recorded in `h43_loop_report.json` (`6.4114` / `7.15` on S2, `6.9088` / `8.13` on S5, `7.9213` / `9.01` on S6, caused solely by the frame-0 hook + first caption vs the text-free last frame).

### B. S2 Instrumental Bed Proof (`owb-standalone-shorts_score_bed_v01.mp3`)
- Replaced `earth-spin_score_take2_straight_v01j.wav` with the approved house standalone Shorts instrumental bed (`02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/05_Music/owb-standalone-shorts_score_bed_v01.mp3`, `sha256: e47e855407b79fd8e3e1dc22c4a12db04df21889a24e87cc463ed9321b5c0c98`, 48.0 s, £0 spend, Chief waiver `music_gate_standalone_shorts_chief_waiver.json`).
- **`base.en` ASR proof (`S2_bed_ASR.json`):** `vad_filter=True` returns `[]` (`0` words); `vad_filter=False` returns `0` spoken narration words (only Whisper's non-speech `'Music'` tag at `p=0.0018`).
- **Direct ear audition (`audio_input`):** Auditioned `stem_bed.wav` across full 22.97 s runtime: 100% pure instrumental marimba/plucked strings over a soft synth pad; zero vocals, speech, or breath.

### C. Direct Ear Audition of Finished AACs (`0–5.5 s` and Full Runtime)
Auditioned the finished AAC audio tracks decoded from `S2_027_emwQsPxnRGM_v07.mp4`, `S5_028_jJ5LkFGyzLI_v07.mp4`, and `S6_028_X768qs8sNQs_v07.mp4` via native `read_file` (`audio/wav`):
- **S2 (`earth_equator_weight_v07`, 22.97 s, `I = -14.4 LUFS`, `TP = -2.0 dBTP`):**
  - `0.0–5.5 s`: Single pickup take (`S2_open_pickup_v07.mp3`, 89 chars) plays *"Why do you weigh less at Earth's equator?"* with natural question intonation and a clean sentence break (`~2.08–2.42 s`), followed by *"You weigh about half a percent less there."* as a separate sentence ending cleanly at `4.60 s`.
  - `16.90–19.86 s`: Continuous phrase from `027_earth_stopped_spinning_vo_v02_p02_clean.wav` (`128.18–131.18 s`) plays *"because the ground at the equator swings round so fast,"* with zero internal splice or `'at'/'but'` artifact, resolving into *"the whole planet bulges."* (`21.97 s`) + 1.0 s music-only loop tail (`22.97 s`).
- **S5 (`028_short_fri04_scale_v07`, 23.10 s, `I = -14.4 LUFS`, `TP = -1.7 dBTP`):**
  - `0.0–5.5 s`: Single pickup take (`S5_open_pickup_v07.mp3`, 42 chars) plays *"How close will Gliese 710 come to the Sun?"* (`0.12–3.32 s`), followed after a clean pause by *"The star will not come anywhere near the planets."* starting cleanly on *"The star"* (`3.60 s`, no *"So"*/*"Though"* artifact).
  - Full runtime ends cleanly on *"That is about a fifth of a light-year."* (`22.10 s`) + 1.0 s music-only loop tail (`23.10 s`).
- **S6 (`028_short_lift_night_sky_35yr_v07`, 23.10 s, `I = -14.4 LUFS`, `TP = -1.7 dBTP`):**
  - Stream-copied (`-c:a copy`) the accepted `v05` AAC track (`packet sha256 = e9de2a1a33fc292c8abfa7047eeab3ddfdaf0ca10ed951dc14a6e4d97047968a`).
  - `0.0–5.5 s`: *"What will the night sky look like when Gliese 710 arrives?"* plays at natural 1.0x recorded speed with a clean pause before *"Right now, Gliese 710..."*.

---

## 2. Gate Exit Codes & Measurements

| Short | `h43-LOOP` | `gate_shorts_open` | `picture_qa` | `polish_gate` | `sfx_kit level` | `music_gate` | Dark Run (`<3`) | OCR 3rd Frame | `I_LUFS` / `TP` |
|---|---|---|---|---|---|---|---|---|---|
| **S2 (`earth_equator_weight_v07`)** | **PASS** (`base=0.50`, `mask=0.57`) | **PASS** (`0`) | **PASS** (`0`) | **PASS** (`0`) | **PASS** (`0`) | **PASS** (`0`) | **PASS** (`0` frames) | **PASS** (`0` hits) | `-14.4` / `-2.0` |
| **S5 (`028_short_fri04_scale_v07`)** | **PASS** (`base=0.59`, `mask=0.62`) | **PASS** (`0`) | **PASS** (`0`) | **PASS** (`0`) | **PASS** (`0`) | **PASS** (`0`) | **PASS** (`0` frames) | **PASS** (`0` hits) | `-14.4` / `-1.7` |
| **S6 (`028_short_lift_night_sky_35yr_v07`)** | **PASS** (`base=0.65`, `mask=0.64`) | **PASS** (`0`) | **PASS** (`0`) | **PASS** (`0`) | **PASS** (`0`) | **PASS** (`0`) | **PASS** (`0` frames) | **PASS** (`0` hits) | `-14.4` / `-1.7` |

---

## 3. Delivered Files & SHA-256 Hashes

All files are delivered and SHA-256 verified across:
1. Repo `06_Final-Exports`
2. iCloud `~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/<stem>/`
3. NAS `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/<stem>/`
4. Render pack `/Users/benjaminoats/_desk/renders/J1100-v07/`

### S2 — `earth_equator_weight_v07` (`emwQsPxnRGM`, Film 027)
- `earth_equator_weight_v07.mp4`: `7d07deafbd4e242384aa35ffc8bf10d670c5e1f961c1f0c2ecc2b2159ea9c649`
- `earth_equator_weight_v07_PHONE.mp4`: `0a81bbf362961cad0572bfeef666f76e3fecbd34fccddea043fc8befe8d88981`
- `earth_equator_weight_v07_base.mp4`: `55c3f4ace6f4c2d488183e86f89f113a47c1997f18b9c1a87ef2a0d92774a687`
- `earth_equator_weight_v07_whole_runtime_2fps.jpg`: `f1f1cd48b63a351cd6cb79aa1bf9ba9c981270821bc395b20d5db5ba24d09b3a`

### S5 — `028_short_fri04_scale_v07` (`jJ5LkFGyzLI`, Film 028)
- `028_short_fri04_scale_v07.mp4`: `d5589ad4fa328ecf08ef737c272a32a3eef4bb4ddf28b420f8fb25cc1dfa626d`
- `028_short_fri04_scale_v07_PHONE.mp4`: `096580ca7820018274a86d7e0cb43a8295e626a63b9cfe090c98e0c29f3677b8`
- `028_short_fri04_scale_v07_base.mp4`: `8364ad6b21f6135304996b4a21425ae5ddc8ab556b9dd2a49ad96f22c38698ea`
- `028_short_fri04_scale_v07_whole_runtime_2fps.jpg`: `8fd62fc2df27f418cdbc6a3f039bc07160c296182c417d47dd5a6d7b9dbab407`

### S6 — `028_short_lift_night_sky_35yr_v07` (`X768qs8sNQs`, Film 028)
- `028_short_lift_night_sky_35yr_v07.mp4`: `2f399f3127bf4ba9a96fedabe0927a7aa9362a412c5a5d93d8c10473b6f83db3`
- `028_short_lift_night_sky_35yr_v07_PHONE.mp4`: `4259ba791312ac5a48e1d706d2c64c1584244cc0cfba3e1cd88f35cce6b3662b`
- `028_short_lift_night_sky_35yr_v07_base.mp4`: `d891c063855db748b06a15d1321aad56baacfc46a691748b27522fa762b1a0bc`
- `028_short_lift_night_sky_35yr_v07_whole_runtime_2fps.jpg`: `b3fb6354ec67fa1769d94093338e8cb8eb9bc17b42b932d6bd15106502d28340`
