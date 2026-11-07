# J2353 — OWB 034 Pluto Shot List, Music Brief & SFX Plan from Accepted `v03` VO

- **Job:** `J2353` (`034 Pluto: shot list from approved v03 VO`)
- **Worker:** `gemini` (Gemini 4 Argon, worker covering `J2353`; not Chief — no stage PASS or merge claimed)
- **Date:** 7 November 2026
- **Inputs:**
  - Locked script master: `02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/01_Script/pluto_frozen_heart_script_master_v03.md` (`95.8/100 PASS`, `gate:episode PASS`, `SOURCES.md` 15/15 `VERIFIED`, `CLAUDE_QUOTE_CHECK_v01.md` 15/15 `PASS`)
  - Accepted VO master (`J2352` elected-Chief full VO PASS, PR #623): `02_Voiceover/pluto_frozen_heart_vo_v03.wav` (SHA-256 `2be8030b6c42b673530351014c71bca1a6c31a10af9746539bb2a1ce7dcf7685`, `616.160 s`, `-19.9 LUFS` integrated, `-23.0 dB` mean, `-3.7 dBTP` true peak)
  - Reconciled word timestamps (`J2157` PR #619): `02_Voiceover/stt/pluto_frozen_heart_vo_v03/stt_raw.json` (SHA-256 `af85f3b6fbcb4c0f549f19f0c526fed18f9454bdb9cfa27958ff5a2770d75df7`, `1,183` word tokens / `1,225` Scribe tokens across `0.100–616.040 s`)
- **Spend:** **£0 / 0 credits** (zero-spend planning only; no generation or assembly performed).

---

## 1. Deliverables Committed

1. **`02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/07_Edit-Project/shot_list_v01.csv`**
   - `68` timed rows (`R01`–`R67` covering `0.00–616.16 s` spoken narration + `R68` `616.16–634.16 s` `18.00 s` moving end-screen hold), `136` total cuts (`4.66 s/cut` mean, max `6.00 s/cut`, max spoken row duration `14.70 s`).
   - Every row boundary lands inside a verified `v03` Scribe inter-word pause (`≥ 0.400 s`), mapping all `1,183` word tokens with `0` split words and preserving both accepted pickups in full (`R58`: `pluto_ch05_looked_back_v03.wav` at `528.060–534.260 s`; `R66`–`R67`: `pluto_ch06_real_worlds_v05_request.wav` at `597.040–616.160 s`).
   - Verified with `00_Brand/Channel-Setup/tools/clip_check.py`:
     ```text
     clip_check: 68 rows — PASS
     OK: sentence/card boundaries and end-after-VO checks clear.
     ```
2. **`02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/07_Edit-Project/SHOT_LIST_v01.md`**
   - Chapter timing and mood map (`Ch 0`–`Ch 6` + `18.00 s` end hold), standing-rules audit, full 68-row table, 46-asset provenance/licence/upscale/reuse table (`≤ 2` raw and deduplicated appearances per still), complete Teach-on-Screen & Polish Pass matrix (`13` `CODE` renders across `7` chapter `NUMBER OBJECT`s + progressive 15-date timeline, `3/3` `WHO` cards, `15/15` `WHEN` markers, `4/4` `FACT` cards), and pasted `clip_check.py` output.
   - Multimodal visual inspection via `default_api:read_file` across contact sheets 1–8 verified that all 46 selected NASA and Wikimedia source assets are clean, single-subject plates free of embedded scale bars, text labels, callout boxes, or multi-panel diagrams (explicitly excluding `PIA20200`, `PIA19841`, `PIA20199`, `PIA20536`, `PIA20656`, `PIA20477`, `PIA21861`, `PIA21860`, `PIA19967`, `PIA20033`, `PIA19847`, `PIA07934`, `PIA09234`, `PIA09265`, `PIA20152`, `PIA22188`, and `File:Discovery Charon.jpg`).
   - Frame 0 (`R01`, `0.00–4.40 s`) uses graded NASA New Horizons MVIC natural-colour close-up `PIA20291`, keeping `PIA19952` out of Frame 0 so the long opener does not duplicate standalone Short `gmzaCfJF1gA` (`owb_sa_s7_pluto_heart`).
   - Two `[ORBIT ACTS]` beats (`R28` and `R52`) are flagged `OMNI (flag)` for Chief's price pass (`orbit-seedance-reference-16x9-v01.png`, Vertex `global`, no planet disc in start frame) with complete £0 NASA-plate + overlay fallbacks that maintain `0` adjacent `CODE` rows.
3. **`02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/05_Music/MUSIC_BRIEF_v01.md`**
   - Alternating `awe`/`explain` chapter mood map (`64–74 BPM`) with `2.5 s` crossfades across `0.70 s` inter-chapter gaps, full `634.16 s` runtime coverage (`2.5 s` full-level hold past `616.040 s`, `3.0 s` fade `631.16–634.16 s`), and exact API prompt carrying mandatory `Pace:` and `NOT:` lines for `scripts/music_gate.py`.
4. **`02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/06_Sound-Effects/SFX_PLAN_v01.md`**
   - Zero-spend house synthesis (`scripts/sfx_kit.py make`) with `8` low-rumble cues, `8` soft-whoosh camera/scale transitions (never on plain cuts), and `30` subtle label/data ticks (`≥ 0.5 s` apart), gated by `scripts/sfx_kit.py level --minutes 10.57`.
5. **`02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/production-status.md`**
   - Updated with `J2352` VO PASS and `J2353` shot-list deliverables + pasted `clip_check.py` PASS output.

---

## 2. Hand-Off

- Queuing dependent Chief shot-list review & picture-stage release job (`kind: chief`, `--film 034 --stage shots --after J2353`) to review PR, mark `034 shots` done, rule on the `£0` NASA fallback vs `OMNI` (`R28`/`R52`) price pass, and release the `£0` public harvest + 13 `code_graphic_034_*` builds.
