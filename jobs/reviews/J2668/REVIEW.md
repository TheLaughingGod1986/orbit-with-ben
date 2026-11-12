# J2668 Review — 034 Pluto First-30s Opening Plan Correction (`FIRST30_PLAN.md`)

- **Job:** `J2668` (*034 Pluto: correct opening plan against locked narration before J2438*)
- **Reviewer / Worker:** `gemini` (`gemini-argon` / `gemini-4-argon-high`, specialist `review` fallback)
- **Prior Review & Conflict Evidence Addressed:**
  - `jobs/reviews/J2438/REVIEW.md` (`c75c73a417` / `32975005ff`, PR `#842`)
  - `ff99358894:jobs/reviews/J2438/INPUT_CONFLICT.md`
- **Target File Corrected:** `02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/07_Edit-Project/FIRST30_PLAN.md` (mirrored to `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/07_Edit-Project/FIRST30_PLAN.md`)
- **Specialist Verdict:** **`KEEP`** on the corrected `FIRST30_PLAN.md` (resolves all five `FIX` items identified in `jobs/reviews/J2438/REVIEW.md` so `J2438` can proceed without guesswork).

---

## 1. Item-by-Item Resolution (`FIX` → `KEEP`)

| # | Requirement from `J2668` & `jobs/reviews/J2438/REVIEW.md` (`c75c73a417`) | Prior `FIRST30_PLAN.md` Defect (`FIX`) | Corrected Specification in `FIRST30_PLAN.md` (`KEEP`) |
|---:|---|---|---|
| **1** | Quote real opening words from locked `pluto_frozen_heart_vo_v03.wav`, `stt_raw.json`, `stt_timeline_offset_v01.json`, and `shot_list_v01.csv`; remove invented highlands/history sentence and misplaced `4 BILLION YEARS` / `0 CRATERS DETECTED` labels. | Quoted an invented Sentence 3 (*"While Pluto's dark battered highlands are scarred by billions of years of impacts across four billion years of solar system history..."*) and invented `R05–R07` lines that do not exist in `v03`, with `4 BILLION YEARS` (`R03`) and `0 CRATERS DETECTED` (`R04`) labels detached from the spoken narration. | Quotes verbatim `v03` words across `R01–R07`:<br>• `R01`: *"Across Pluto's horizon, what would you see on the bright western half of its icy heart?"* (`0.100–5.900 s` ed)<br>• `R02`: *"A frozen nitrogen glacier about 1,000 kilometers wide, larger than Texas and Oklahoma combined, with zero craters."* (`6.800–16.240 s` ed)<br>• `R03`: *"On 13th and 14th July 2015, NASA's New Horizons spacecraft flew within 12,500 kilometers of Pluto,"* (`17.340–26.900 s` ed; labels: `WHEN #1: 13–14 JULY 2015`, `12,500 KM FLYBY`)<br>• `R04`: *"39 times farther from the Sun than Earth, at minus 232 degrees Celsius, and solved that mystery."* (`27.920–36.020 s` ed; labels: `39× EARTH DISTANCE`, `−232 °C SURFACE`)<br>• `R05`: *"While craters up to 260 kilometers across scar the rest of Pluto, Sputnik Planitia is an active glacier where city-sized cells of solid nitrogen circulate up and down."* (`37.980–51.680 s` ed; labels: `260 KM CRATERS`, `CONVECTING NITROGEN CELLS`)<br>• `R06`: *"How can a world one-fifth the width of Earth keep a giant nitrogen heart churning?"* (`53.620–59.320 s` ed; label: `1/5 EARTH'S WIDTH`)<br>• `R07`: *"And what secret did our only spacecraft to visit Pluto discover there?"* (`60.880–65.160 s` ed). |
| **2** | Replace unsafe `38.68 s`, `48.80 s`, and `56.20 s` silence insertion timestamps with evidenced inter-sentence gaps that restore `+2.80 s` before the unchanged `R08` anchor (`65.76 s`), recording raw and edited times separately. | `38.68 s` fell inside `"mystery."` (`38.28–38.82 s` raw), `48.80 s` inside `"city-sized"` (`48.32–49.06 s` raw), and `56.20 s` inside `"width"` (`56.00–56.26 s` raw). | Replaces all three with verified inter-sentence silences in `pluto_frozen_heart_vo_v03.wav` (`48,000 Hz` stereo PCM):<br>• **Trim `-2.800 s`** (`-134,400` samples) at **`raw = 2.000..4.800 s`** (`samples 96,000..230,400`), between `"horizon,"` (`0.980–1.620 s` raw) and `"what"` (`4.960–5.080 s` raw / `2.160–2.280 s` ed).<br>• **Insert `+1.000 s`** (`+48,000` samples) at **`raw = 39.300 s`** (`sample 1,886,400`, `edited = 36.500..37.500 s`), between `"mystery."` (`38.280–38.820 s` raw / `35.480–36.020 s` ed) and `"While"` (`39.780–39.900 s` raw / `37.980–38.100 s` ed).<br>• **Insert `+0.900 s`** (`+43,200` samples) at **`raw = 54.000 s`** (`sample 2,592,000`, `edited = 52.200..53.100 s`), between `"down."` (`53.060–53.480 s` raw / `51.260–51.680 s` ed) and `"How"` (`54.520–54.680 s` raw / `53.620–53.780 s` ed).<br>• **Insert `+0.900 s`** (`+43,200` samples) at **`raw = 60.550 s`** (`sample 2,906,400`, `edited = 59.650..60.550 s`), between `"churning?"` (`59.660–60.220 s` raw / `58.760–59.320 s` ed) and `"And"` (`60.880–61.000 s` raw & ed).<br>• Net delta before `R08` (`65.760 s`, sample `3,156,480`) = **`0.000 s` (`0` samples)**. Also specifies inserting the 6 chapter-card silences at `prev_word_raw_end + 0.600 s` (`65.760 s` for `R08`) to avoid clipping the pre-onset of `"18th"` (`66.040 s`). |
| **3** | Give a frame-counted cut table at `30 fps` reconciling `65.76 s` (`frame 1,973`) with cumulative frame rounding and preserving downstream `R08–R74` timing. | Row/cut table in `§2–§3` was not reconciled with `build_plan()` cumulative `round(clock * 30)` frame math across `R01–R07`. | Provides exact cumulative `dur_s` and `30 fps` frame counts across `R01–R07` (`190 + 314 + 318 + 273 + 471 + 224 + 183 = 1,973` frames = `65.767 s`, `sum(dur_s) = 65.76 s`), rejoining `R08` at `f0 = 1,973`, `f1 = 2,048` and keeping `R08–R74` (`frames 1,973..19,408`, total `19,408` frames = `646.933 s`, `138` cuts) 100% unchanged. |
| **4** | Match pictures and overlays to actual flyby/date/distance/temperature and convection lines within verified pool reuse (`<= 2`) and upscale (`<= 2.00x`) limits, `<= 4.00 s` opening cuts, and real imagery between code graphics. | Used `PIA19936.jpg` (`R02`, `R04`) and `PIA19948.jpg` (`R04`), both of which already appear twice later in the film (`R59`/`R61` and `R63`/`R74`, violating `MAX_REUSE = 2`), and reused the same filename `code_graphic_034_r02_sputnik_scale.mp4` at `0.00 s` and `6.96 s` (`< 10.0 s` apart, failing `picture_qa.py` `SAME_STRETCH`). | Uses verified pool plates with `<= 2` appearances across the entire `138`-cut film (`PIA20007.jpg` in `R02` Cut 4 between dedicated beat files `code_graphic_034_r02a_sputnik_width.mp4` and `code_graphic_034_r02b_texas_oklahoma_scale.mp4`; `PIA20038.jpg`, `PIA20286.jpg`, `PIA14458.jpg` in `R04` Cuts 9–11; `offset=0.0 s` and `20.0 s` on `R05` flyby video `>= 10.0 s` clear of `R50`'s `10.0 s`; `<= 2.000x` upscale cap on `PIA20155.jpg` and `PIA21965.jpg`). All 19 cuts in `R01–R07` are `3.033–3.933 s <= 4.000 s`. |
| **5** | Derive the real Test A Short endpoint from the real Sentence 3 ending rather than the old `35.88 s` placeholder; preserve `§5` (`026`, `027`, `031`) unchanged with no-public-action note. | Used `35.88 s` from the invented Sentence 3 (which would cut off `"mystery."` `0.140 s` before it finishes at `36.020 s` edited). | Derives the real Sentence 3 word end at **`36.020 s` edited (`38.820 s` raw)** on `w0071` `"mystery."` and sets the `034_short01_testA_opening_v02.mp4` endpoint at the `R04` row boundary **`36.500 s` (`1,095` frames at `30 fps`, `0.480 s` post-sentence tail, inside the `30–38 s` Test A window)**. Preserves `§5` verbatim with the explicit scope note. |

---

## 2. Direct `audio_input` Ear-Check Evidence (`0.00–70.00 s` Spliced `v02` Narration)

The spliced `v02` opening narration was rendered from `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/02_Voiceover/pluto_frozen_heart_vo_v03.wav` (`48,000 Hz` stereo PCM) and audited directly via `read_file` (`audio/wav` input):

1. **`0.000–18.000 s` edited (`R01–R02`, `pluto_v02_s1_s2_splice_00_18s.wav`):**
   - At `t = 2.000 s` edited (`raw = 2.000..4.800 s` removed), *"Across Pluto's horizon, [0.540 s natural pause] what would you see on the bright western half of its icy heart?"* plays with natural prosody and cadence, zero click/pop/breath truncation, and finishes cleanly at **`5.900 s < 8.000 s`**.
   - Sentence 2 (*"A frozen nitrogen glacier about 1,000 kilometers wide, larger than Texas and Oklahoma combined, with zero craters."*) enters cleanly after a `0.900 s` pause at `6.800 s` and completes at **`16.240 s < 20.000 s`**.
2. **`16.000–37.000 s` edited (`R03–R04`, `pluto_v02_r03_r04_16_37s.wav`):**
   - Sentence 3 (*"On 13th and 14th July 2015, NASA's New Horizons spacecraft flew within 12,500 kilometers of Pluto, 39 times farther from the Sun than Earth, at minus 232 degrees Celsius, and solved that mystery."*) runs continuously from `17.340 s` to **`36.020 s` edited**, with `0.480 s` of clean room tone before the `R04` / Test A Short cut at **`36.500 s` (`1,095` frames)**.
3. **`34.000–70.500 s` edited (`R04–R09`, `pluto_v02_r04_r08_insertions_34_70s.wav` & `pluto_v02_r04_r08_insertions_60_70s_fixed.wav`):**
   - All three inter-sentence silence insertions (`+1.000 s` at `raw = 39.300 s`, `+0.900 s` at `raw = 54.000 s`, `+0.900 s` at `raw = 60.550 s`) sit in dead silence between sentences with zero word clipping or noise-floor jump.
   - Ear-check on `65.000–70.000 s` identified that `v01`'s `lay_vo()` inserted the `+2.220 s` Chapter 1 silence at Whisper's `raw_start = 66.040 s` (`"18th"`), where the vowel pre-onset had already begun (`±20 ms peak = 0.641724`). Moving the chapter-card silence insertion point to `prev_word_raw_end + 0.600 s` (`65.760 s` for `R08`, where `±20 ms peak = 0.000000`) restores a completely clean `"18th February 1930."` at `68.260 s` edited while keeping the exact same sample count (`3,156,480` samples at `65.760 s`).

---

## 3. Gate Simulation Evidence (`picture_qa.py --cuts` & `clip_check.py`)

Both automated pre-render gates were run against the simulated `138`-cut `v02` manifest (`cuts_v02.json`), `shot_list_v02.csv`, and remapped `stt_timeline_offset_v02.json`:

1. **`scripts/picture_qa.py --cuts` (`138` cuts, `646.933 s`):**
   ```text
   # Picture QA: PASS
   source checks only (no video) · 138 cuts · 0 fail · 1 for Claude to look at full size
   ```
2. **`00_Brand/Channel-Setup/tools/clip_check.py` (`74` rows):**
   ```text
   clip_check: 74 rows — PASS
     OK: sentence/card boundaries and end-after-VO checks clear.
   ```
