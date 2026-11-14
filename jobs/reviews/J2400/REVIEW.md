# J2400 — 033 Uranus Active Shorts 1 & 2 (`v01`) 5-Part Multimodal Review

- **Date:** 2026-11-14
- **Reviewer:** `gemini` (`Gemini 4 Argon (High)`, `audio_input` + `moving_video_input` verified)
- **Standard:** `jobs/reviews/J2829/RULING.md` (5-part multimodal review standard)
- **Verdict:** **`FIX` on both `v01` cuts (`033_short01_testA_opening_v01.mp4` and `033_short02_ice_giant_surface_v01.mp4`)** — do **not** stage `v01` for Ben's phone watch or upload to YouTube. Rebuild both cuts as `v02` per the exact specification in §7 below.

---

## 1. Executive Summary & Verdict

| Short | Master Path (`studio-live` / NAS `OWB UAT`) | SHA-256 | Duration / Frames | Air Slot | Verdict | Blocking Reasons (`FIX`) |
|---|---|---|---|---|---|---|
| **Short #1 (Test A Opening)** | `02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short01_testA_opening_v01.mp4` | `7eca95258582b93f6b822e182bf64db8d6e31d95f3710b4479182df4f5182ca7` | `36.480 s` (`912` frames @ `25 fps`) | Fri 18 Dec 2026 11:30Z | **`FIX`** | 1. **`gate_shorts_open.py` HARD FAIL (`full-bleed 9:16` rule, `J2545`/`J2546`/`J2560`):** `14/37` frames at 1 fps (`38%`, limit `10%`) and `25/73` frames at 2 fps (`34%`) fail `blur-pad` because shots `R01b`–`R09b` (`2.36–35.44 s`) are rendered in `16:9` (`1920×1080`) and shrunk into a `1080×608` horizontal band (`y=656..1264`) over a blurred-plate + starfield surround (`composite_band_on_natural_blur()`), shrinking the `23.44° vs 97.77°` axial-tilt gauge (`R05a`, `18.20–22.20 s`) into a tiny `608 px` strip.<br>2. **Audio onset clip (`audio_input`):** Segment 1 slice (`49.320–53.880 s` of `uranus_vo_v01.wav`) starts inside the aspirate `"H-"` of `"How"`, which begins at `49.250 s` (`pk=0.029` at `49.280 s`, `pk=0.350` at `49.320 s`; true silence `pk < 0.0001` is at `49.180..49.230 s`).<br>3. **Meta sidecar:** `033_short01_testA_opening_v01_meta.json` omits `"end_card": {"start_s": 35.44}`. |
| **Short #2 (Keeper Question)** | `02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short02_ice_giant_surface_v01.mp4` | `c2404d5a05ada2c257bf9e5fdc2b10edaa126d36de6aa32b38cb27df6d08dbc2` | `26.280 s` (`657` frames @ `25 fps`) | Sat 19 Dec 2026 11:30Z | **`FIX`** | 1. **`gate_shorts_open.py` HARD FAIL (`full-bleed 9:16` rule, `J2545`/`J2546`/`J2560`):** `24/27` frames at 1 fps (`89%`, limit `10%`) and `47/53` frames at 2 fps (`89%`) fail `blur-pad` because all 9 middle shots (`R49b`–`R53c`, `1.88–25.28 s`) sit inside a `1080×608` (`16:9`) band (`y=656..1264`) over blurred vertical fill.<br>2. **Severe word-onset clipping (`audio_input`):** `_assemble_033_short2_v01.py` sliced `459.680–482.500 s` into 9 sub-segments using Scribe word-start timestamps that lag 50–360 ms behind acoustic onset: **`"80%"` at `11.8 s` (`466.480 s` slice start) is clipped to `"-ty percent"`** (`"eighty"` starts at `466.280 s`, `pk=0.431` at `466.350 s`), and **`"9,000"` at `23.8 s` (`480.580 s` slice start) is clipped to `"-n thousand"`** (`"nine"` spans `480.220..480.600 s` with zero silence gap before `"thousand"` at `480.604 s`, so dropping `480.140..480.580 s` deleted `"nine"`).<br>3. **Unrecognisable ruled ring plates (`PIA00142.jpg`, `PIA01977.jpg`, `PIA01985.jpg`):** Narrow Voyager 2 ring-plane plates in `R49a` (blended overlay), `R51a` (`5.60–7.80 s`), and `R53a` (`18.76–21.04 s`, `picture_qa` `WARN low detail: edge density 0.0076`) read as grey ruled stripes/grids rather than an ice-giant atmosphere or core.<br>4. **Meta sidecar:** `033_short02_ice_giant_surface_v01_meta.json` omits `"end_card": {"start_s": 25.28}`. |

> **Staging Check (`studio-live` vs NAS vs iCloud Drive):**
> - `studio-live` and `/Volumes/data/mac-mini-archive/OWB UAT/033_shorts_v01/` match both SHA-256 hashes (`7eca95...` and `c2404d...`, `18,622,824 B` and `11,055,843 B`).
> - `~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/033_shorts_v01/` contains **0-byte placeholder files** (`SHA-256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`) for both `.mp4` files. When `v02` is built and staged, non-zero byte counts and matching SHA-256 hashes must be verified on both NAS and iCloud Drive.

---

## 2. Part 1 — Automated Gate Verification on Exact `v01` Masters

All 7 automated tools were re-run directly on the `studio-live` master `.mp4` files on 2026-11-14:

| Gate Tool | Short #1 (`033_short01_testA_opening_v01.mp4`) | Short #2 (`033_short02_ice_giant_surface_v01.mp4`) | Status |
|---|---|---|---|
| `gate_shorts_open.py check <mp4> --air-date YYYY-MM-DD` | **EXIT 1 (`FAIL`):** `the picture does not fill 9:16 on 14/37 frames sampled once a second (38%, limit 10%): 2-4s (blur-pad), 9-10s (blur-pad), 16-18s (blur-pad), 26-32s (blur-pad), 32-33s (blur-pad), 34-36s (blur-pad)  no end card named in meta` (Frame 0 & Cover pass visual distinctiveness, `max 50.8%` vs `029_short03`, `max pHash 46.9%` vs `016_short01`; `1080×1920`, `36.5 s`, `-14.0 LUFS`, `-2.0 dBTP`). | **EXIT 1 (`FAIL`):** `the picture does not fill 9:16 on 24/27 frames sampled once a second (89%, limit 10%): 2-26s (blur-pad / blur-pad, no edge)  no end card named in meta` (Frame 0 & Cover pass visual distinctiveness, `max 47.4%` vs `029_short02`, `max pHash 56.2%` vs `004_short03`; `1080×1920`, `26.3 s`, `-14.0 LUFS`, `-1.6 dBTP`). | **FAIL (both)** |
| `picture_qa.py <mp4> --aspect 9:16 --expect-duration <dur>` | **PASS (`0` issues, `0` warnings)** (`73` frames at `2.0 fps`, `1080×1920`, `25/1 cfr`, `36.48 s`, `audio=36.48s`). | **PASS (`0` issues, `2` warnings):** `19.5s–20.0s WARN low detail: edge density 0.0076 (min 0.008)` on `R53a` (`PIA01985.jpg` narrow ring plate). | **PASS (Short 1) / WARN (Short 2)** |
| `polish_gate.py <mp4> --cuts <cuts.json> --words <words.json> --loop` | **PASS** (`14` shots, `61` content words, `2.6 s` avg shot, max `4.0 s`, `0` boundary cuts, `0.00` loop seam jump, `-14.0 LUFS`, `-1.9 dBTP`). | **PASS** (`11` shots, `38` content words, `2.4 s` avg shot, max `3.9 s`, `0` boundary cuts, `0.00` loop seam jump, `-14.0 LUFS`, `-1.6 dBTP`). | **PASS (both)** |
| `sfx_kit.py level --vo <vo> --sfx <sfx> --bed <bed> --minutes <m>` | **PASS** (`VO -14.7 LUFS`, `SFX -28.0 LUFS`, `13.3 dB` below VO in `10–16 dB` band; `8` events = `13.2/min`, `0` on voice, `0` steady hiss). | **PASS** (`VO -15.3 LUFS`, `SFX -27.2 LUFS`, `11.9 dB` below VO in `10–16 dB` band; `6` events = `13.7/min`, `0` on voice, `0` steady hiss). | **PASS (both)** |
| `music_gate.py <bed.wav> --duration <dur> --stems-dir <dir>` | **PASS** (`4` stems: `pad`, `arp`, `bass`, `swell`; centroid `492 Hz`; correlation `0.002`; dynamic spread `6.4 dB`). | **PASS** (`4` stems: `pad`, `arp`, `bass`, `swell`; centroid `517 Hz`; correlation `-0.003`; dynamic spread `5.4 dB`). | **PASS (both)** |
| `thumb_preview.py short <frame0.jpg> / <cover.jpg> --score` | **PASS** (`frame0`: `score 90`, `edge=0.056`, `bright=17.4%`; `cover`: `score 90`, `edge=0.049`, `bright=17.5%`). | **PASS** (`frame0`: `score 85`, `edge=0.032`, `bright=22.9%`; `cover`: `score 85`, `edge=0.025`, `bright=23.2%`). | **PASS (both)** |

> **Why `gate_shorts_open.py` passed during J2317/J2318 (2026-11-12) and fails now:**
> Both `v01` cuts were assembled on 2026-11-12 using `composite_band_on_natural_blur()` (`1080×608` `16:9` band at `y=656..1264` over a Gaussian-blurred plate + starfield background), before the studio's full-bleed `9:16` rule (`J2545`/`J2546`/`J2560`, `studio/RULES.md` Lesson 5: *"Every Short frame fills the whole 1080×1920 canvas (`gate_shorts_open.py` checks at 2 fps)"*) landed on 2026-11-14. Under the live contract, any Short in the pipeline must pass `gate_shorts_open.py` before staging for Ben's phone watch or upload.

---

## 3. Part 2 — Full-Film `0.5 s` (`2 fps`) Contact-Sheet Grid Inspection

Contact sheets were generated at `2.0 fps` with burned-in `t=%{pts:hms} f=%{n}` timestamps (`short1_2fps.jpg`: `73` frames `0.0–36.0 s`; `short2_2fps.jpg`: `53` frames `0.0–26.0 s`) and visually inspected via `read_file`:

### Short #1 (`033_short01_testA_opening_v01.mp4`, `0.0–36.0 s`)
- **`0.0–2.0 s` (`R01a`, `r01_cut1`):** Full-bleed `1080×1920` (`9:16`) Voyager 2 crescent Uranus Veo clip with burned-in hook card (`21-YEAR WINTER` / `ONE POLE IN THE DARK` at `y=300..540`). Fills `9:16` cleanly.
- **`2.5–35.0 s` (`R01b` through `R09b`, 12 consecutive shots):** Every shot is composited into the `1080×608` horizontal band (`y=656..1264`) with a soft `96 px` feather into a dark starfield/blurred top (`y=0..656`) and bottom (`y=1264..1920`).
  - **`18.5–22.0 s` (`R05a`):** The `AXIAL TILT COMPARISON` card (`EARTH 23.4°` vs `URANUS 97.77° — SIDEWAYS`) is rendered on a `1920×1080` (`16:9`) canvas and shrunk into `1080×608`, making the two side-by-side globes and protractor arcs very small (`~250 px` wide) in the middle of the vertical phone screen while `65%` of the `1080×1920` canvas above and below sits empty.
  - **`26.0–28.5 s` (`R07`, `STScI-01GWQ3...` JWST zoomed rings) & `33.5–35.0 s` (`R09b`, `PIA18182.jpg` Hubble aurora):** Bright cyan/blue planetary glow and diffraction spikes terminate at the `y=656` and `y=1264` horizontal band borders, creating an unmistakable horizontal box across the middle of the vertical frame.
- **`35.5–36.48 s` (`R01_loop`):** Returns to full-bleed `9:16` (`r01_cut1` loop tail with `"Why This Planet Has 21-Year Winters"` pointer pill at `y=1240..1360`).

### Short #2 (`033_short02_ice_giant_surface_v01.mp4`, `0.0–26.0 s`)
- **`0.0–1.5 s` (`R49a`):** Full-bleed `9:16` composite (`r49_cut1` + `32%` blend of `PIA00142.jpg` Voyager 2 ring plate) with hook card (`NO SOLID SURFACE` / `WHAT LIES BENEATH?`). Because `PIA00142.jpg` is a ruled close-up of the ring plane, diagonal ruled stripes cut across the cyan atmosphere behind the hook text.
- **`2.0–25.0 s` (`R49b` through `R53c`, all 9 middle shots):** Every shot is confined to the `1080×608` horizontal band (`y=656..1264`) over a dark blurred/starfield surround (`89%` failure rate on `gate_shorts_open.py`).
  - **`5.60–7.80 s` (`R51a`, `PIA01977.jpg`):** Narrow Voyager 2 ring-plane close-up (`754×735`) inside the `1080×608` band reads as a grey striped oval with a diagonal shadow across it, not an ice giant with *"no true surface"*.
  - **`14.84–18.76 s` (`R52`, interior cutaway diagram):** Drawn on `1920×1080` and shrunk into the `1080×608` band (`80% HOT DENSE FLUID` / `H2O • CH4 • NH3`), leaving the top and bottom thirds of the phone screen unused.
  - **`18.76–21.04 s` (`R53a`, `PIA01985.jpg`):** Narrow Voyager 2 ring plate (`719×386`) inside the `1080×608` band reads as two thin grey diagonal lines on black (`picture_qa` `WARN low detail: edge density 0.0076`) while the narrator says *"above a small rocky core."*
  - **`21.04–25.28 s` (`R53b` & `R53c`, `r55_cut1` / `r55_cut2`):** Bright cyan cloud vortex fills only the `1080×608` middle rectangle (`y=656..1264`), creating a stark horizontal rectangle against dark blue-black bars above and below.
- **`25.28–26.28 s` (`R49_loop`):** Full-bleed `9:16` loop tail matching `R49a` Frame 0, with `"Why This Planet Has 21-Year Winters"` pointer pill.

---

## 4. Part 3 — Cut-Boundary (`±3` Frames) & Final `3.0 s` (`75` Frames) Strip Inspection

Every internal cut (`±3` frames, `7` frames per row) and all `75` frames of the final `3.0 s` (`J2614` splice-strip standard) were rendered and inspected via `read_file`:

### Short #1 (`13` cuts × `7` frames = `91` frames; final `3.0 s` = `f837..f911`, `33.48–36.44 s`)
- **Cut integrity:** All 13 internal cuts (`2.36s`, `4.36s`, `8.20s`, `12.00s`, `14.52s`, `18.20s`, `22.20s`, `26.00s`, `28.56s`, `31.08s`, `33.56s`, `35.44s`) are frame-accurate hard cuts with zero black flash frames, zero duplicate freeze frames across cuts, and zero orphan text badges.
- **Band-to-full-bleed jumps at `f059` (`2.36 s`) and `f886` (`35.44 s`):** At `f058 -> f059` (`2.32 s -> 2.36 s`), the picture jumps from full-bleed `9:16` (`R01a`) to the `1080×608` horizontal band (`R01b`); at `f885 -> f886` (`35.40 s -> 35.44 s`), it jumps from the `1080×608` band (`R09b`) back to full-bleed `9:16` (`R01_loop`). Rebuilding `R01b`–`R09b` as full-bleed `1080×1920` (`9:16`) eliminates both jumps.
- **Final `3.0 s` (`f837..f911`, `33.48–36.44 s`):** Smooth continuous motion across `R09a` (`f837..f838`), `R09b` (`f839..f885`, Hubble `PIA18182` zoom + `"NO OTHER PLANET DOES THIS"` lower-third), and `R01_loop` (`f886..f911`, `35.44–36.44 s` seamless loop tail matching `f000`, `0.00` pixel delta).

### Short #2 (`10` cuts × `7` frames = `70` frames; final `3.0 s` = `f582..f656`, `23.28–26.24 s`)
- **Cut integrity:** All 10 internal cuts (`1.88s`, `3.80s`, `5.60s`, `7.80s`, `10.92s`, `14.84s`, `18.76s`, `21.04s`, `23.28s`, `25.28s`) are clean hard cuts with zero flash frames.
- **Final `3.0 s` (`f582..f656`, `23.28–26.24 s`):**
  - `f582..f631` (`23.28–25.24 s`, `R53c` `r55_cut2` with `"9,000 °F AT THE CORE"` lower-third) shows the bright cyan cloud vortex boxed inside `y=656..1264` with dark blue-black top/bottom bands.
  - `f632..f656` (`25.28–26.24 s`, `R49_loop` end card): Because `r49_cut1` (`6.04 s`) is indexed with `min(int(t_local * FPS), len(c_r49a) - 1)` for `t_local = 5.04..6.04 s`, the final `0.24 s` (`f650..f656`, `26.00–26.24 s`) holds on the final frame of `r49_cut1` so `f656` matches `f000` (`0.00` loop seam delta). Using a gentle ease-out or matching continuous motion into `f000` avoids any visible micro-hold at `26.00–26.24 s`.

---

## 5. Part 4 — Complete Soundtrack Inspection via `audio_input` & Waveform Envelope Analysis

Both complete soundtracks (`short1_audio.mp3`, `36.48 s`, and `short2_audio.mp3`, `26.28 s`) were extracted and listened to end-to-end via verified `audio_input` (`read_file`), and cross-checked against 10–20 ms peak/RMS envelopes of the master VO (`04_Audio/uranus_vo_v01.wav`):

### Short #1 Soundtrack (`short1_audio.mp3`, `36.48 s`)
- **Spoken performance & mix:** Warm, clear delivery from `0.16 s` (*"Every planet in the solar system spins like a top..."*) through `31.12 s` (*"...locked in 21 years of freezing darkness."*), then the closing question at `31.20–35.76 s` (*"How did an entire world end up rolling around the Sun on its side?"*). Music bed (`D minor`, `64 BPM`) and 8 house SFX cues sit cleanly underneath with zero collisions on spoken words.
- **Defect found via `audio_input` + waveform (`FIX`):**
  - `_assemble_033_short1_v01.py` slices Segment 0 (`0.080–31.000 s`) and Segment 1 (`49.320–53.880 s`) with `VO_GAPS = [0.12]`.
  - In `uranus_vo_v01.wav`, the aspirate `"H-"` of `"How"` begins at **`49.250 s`** (`pk=0.029` at `49.280 s`, `pk=0.350` at `49.320 s`), while true digital silence (`pk <= 0.00009`) is at **`49.180..49.230 s`**. Starting Segment 1 at `49.320 s` clips the first `70 ms` of `"How"`. Similarly, at the end of `"darkness."` (`31.000 s`), the final sibilant tail settles to `pk=0.00082` at `31.040 s`.
  - **Exact fix for Short #1 `VO_SEGMENTS`:** Set `VO_SEGMENTS = [(0.080, 31.040), (49.220, 53.880)]` and `VO_GAPS = [0.20]` (starts Segment 1 at `31.20 s` in the timeline, preserving identical shot timings and `TOTAL_S = 36.48 s` while keeping 100% of `"darkness."` and `"How"` intact).

### Short #2 Soundtrack (`short2_audio.mp3`, `26.28 s`) — **Blocking Word-Onset Clipping (`FIX`)**
- **What `audio_input` heard:**
  1. At **`~11.8 s`**, instead of *"eighty percent of the planet's mass"*, the audio plays **`"-ty percent of the planet's mass"`** — the entire first syllable `"eigh-"` is chopped off!
  2. At **`~23.8 s`**, instead of *"Uranus heats up to nine thousand degrees Fahrenheit"*, the audio plays **`"Uranus heats up to -n thousand degrees Fahrenheit"`** — the word `"nine"` is missing!
- **Root cause in `_assemble_033_short2_v01.py` (lines 108–120):**
  The assembler split a single continuous 23-second passage (`459.680–482.500 s` of `uranus_vo_v01.wav`) into 9 tiny sub-slices using Scribe word-start timestamps (`466.480`, `469.080`, `471.480`, `472.680`, `474.920`, `477.800`, `479.040`, `480.580`) and inserted artificial pauses (`VO_GAPS`) between words that were spoken continuously with co-articulation!

| Sub-slice in `v01` | Spoken Text | Scribe Slice Start (`v01`) | True Acoustic Onset in `uranus_vo_v01.wav` | True Silence Window (`pk < 0.001`) | Audible Defect in `v01` |
|---|---|---|---|---|---|
| Seg 0 (`438.520–443.960`) | *"What happens if a spacecraft dives beneath those clouds to land on the ice below?"* | `438.520 s` | `438.520 s` (ends `444.010 s`) | `438.450..438.500 s` (end `444.020 s`) | Slight tail trim on `"below?"` (`pk=0.017` at `443.960 s`; `0.0005` at `444.020 s`). |
| Seg 1 (`459.680–463.200`) | *"As an ice giant, Uranus has no true surface."* | `459.680 s` | `459.640 s` (`pk=0.107` at `459.680 s`) | `459.500..459.600 s` (end `463.250 s`) | Clips first `40 ms` of `"As"` and tail of `"surface."` |
| Seg 2 (`463.760–465.880`) | *"Beneath the hydrogen and helium clouds,"* | `463.760 s` | `463.760 s` (ends `465.940 s`) | `463.650..463.750 s` (`465.960..466.250 s` after `"clouds,"`) | Clips `60 ms` of `"clouds,"` sibilant tail. |
| Seg 3 (`466.480–469.000`) | *"80% of the planet's mass"* | **`466.480 s`** | **`466.280 s`** (`pk=0.431` at `466.350 s`, `pk=0.490` at `466.400 s`) | **`466.150..466.250 s`** | **CRITICAL:** Chops `200 ms` off `"eighty"` -> sounds like **`"-ty percent"`**! |
| Seg 4–6 (`469.080–474.360`) | *"is a crushing, superheated ocean of water, methane, and ammonia"* | `469.080` / `471.480` / `472.680 s` | Continuous phrase (`469.040–474.380 s`) | `468.960..469.000 s` before `"is"`; `474.400..474.820 s` after `"ammonia"` | Unnecessary intra-clause cuts at `"of"` (`471.480 s`) and `"methane"` (`472.680 s`) clip consonant onsets. |
| Seg 7 (`474.920–477.040`) | *"above a small rocky core."* | `474.920 s` | `474.850 s` (`pk=0.118` at `474.900 s`) | `474.750..474.820 s` (end `477.080 s`) | Clips first `70 ms` of `"above"`. |
| Seg 8–10 (`477.800–482.500`) | *"Near that core, Uranus heats up to 9,000 degrees Fahrenheit."* | `477.800` / `479.040` / **`480.580 s`** | `"Near"` at `477.700 s`; `"Uranus"` at `478.980 s`; **`"nine"` at `480.220..480.600 s`** (`pk=0.388` at `480.250 s`, co-articulated from `"to"` at `480.024..480.124 s`) | `477.100..477.650 s` before `"Near"`; `478.680..478.920 s` after `"core,"`; **NO silence before `"9,000"`**; `482.550 s` after `"Fahrenheit."` | **CRITICAL:** Slicing out `480.140..480.580 s` **deleted the entire word `"nine"`** -> sounds like **`"-n thousand"`**! |

---

## 6. Part 5 — Compact `360×640` Moving-Video Proxy Review (`moving_video_input`) & Teach / Polish / Keeper Audit

Compact `360×640` (`9:16`, `< 1 MB`) H.264/AAC proxies (`short1_proxy_360p.mp4`, `925 KB`; `short2_proxy_360p.mp4`, `797 KB`) were generated and watched end-to-end via `read_file` (`moving_video_input`):

1. **Motion & Pacing (`moving_video_input`):**
   - **Short #1 (`36.48 s`):** Camera motion across the 8 Veo clips (`r01_cut1/2`, `r02_cut1/2`, `r04_cut1/2`, `r05_cut1`, `r06_cut2`, `r08_cut1/2`) and pan/zoom plates is smooth at `25 fps` with zero stutter or frozen frames, and the 3-step `98°` rotation + `21-year` polar cycle diagram (`R04a` `8.20–12.00 s`, `R05a` `18.20–22.20 s`, `R06` `22.20–26.00 s`) syncs directly to the spoken numbers (`98 degrees`, `42 years`, `21 years`). However, because `R01b`–`R09b` are squeezed into the `1080×608` horizontal band, the visual scale collapses after `2.36 s` and the `R05a` axial-tilt gauge is far too small on a vertical screen.
   - **Short #2 (`26.28 s`):** Pacing (`2.4 s` average shot) and structure match the `J2683` test design (question opener `0.00–5.52 s`, one-sentence qualitative premise `5.60–9.32 s`, first count/scale number `"80%"` at `~12 s`, second scale number `"9,000 °F"` at `~24 s`). However, watching and listening to the moving proxy immediately exposes:
     - the `1080×608` letterboxed band from `1.88 s` to `25.28 s` (especially glaring on the bright cyan `r55_cut1/2` cloud vortex at `21.04–25.28 s`),
     - the grey ruled ring plates (`PIA01977.jpg` at `5.60–7.80 s` and `PIA01985.jpg` at `18.76–21.04 s`) that look like striped ovals/lines rather than an ice giant's atmosphere or core, and
     - the clipped spoken numbers (`"-ty percent"` at `11.8 s` and `"-n thousand"` at `23.8 s`).
2. **Teach-on-Screen / Polish-Pass / Keeper Gates:**
   - **No Orbit character in Shorts:** Verified (`0` appearances in both Shorts).
   - **No repeated stills within a Short:** Verified (`0` repeated stills in both Shorts).
   - **Upscale factor `<= 2.35×` (`J2305`):** Verified on `v01`; must also be enforced on `v02` when reframing to full-bleed `1080×1920` (see §7.3 below).

---

## 7. Exact `v02` Rebuild Specification (For the `assembly` Worker)

Both Shorts must be rebuilt as `033_short01_testA_opening_v02.mp4` and `033_short02_ice_giant_surface_v02.mp4` (with updated `_cuts.json`, `_words.json`, `_meta.json`, `_frame0.jpg`, `_cover.jpg`, and build reports) before re-running `J2400`'s follow-up review and staging for Ben's phone watch.

### 7.1 Mandatory Full-Bleed `9:16` (`1080×1920`) Canvas on Every Shot (`Both Shorts`)
1. **Remove `composite_band_on_natural_blur()` completely** from both `_assemble_033_short1_v02.py` and `_assemble_033_short2_v02.py`. Never place a `16:9` (`1080×608`) horizontal band over a blurred or starfield vertical background (`J2545`/`J2546`/`J2560`).
2. **Every shot (`0.00 s` through `TOTAL_S`) must fill the entire `1080×1920` (`9:16`) canvas:**
   - **Veo clips (`1920×1080` source):** Crop/reframe to `9:16` (`608×1080` crop window from `1920×1080`, upscaled `1.78×` to `1080×1920`, well within the `2.35×` cap) with gentle pan/zoom tracking the planet/subject, just as `R01a` (`0.00–2.36 s`) and `R49a` (`0.00–1.88 s`) already do.
   - **High-res NASA/ESA/JWST stills (`harvest_J2299_v01`):** Crop a `9:16` vertical window from the high-res master plate and pan/zoom directly at `1080×1920` (keeping effective upscale `<= 2.35×`, i.e. crop width `>= 460 px` and crop height `>= 818 px`).
     - *Note for `PIA00032_left_globe.jpg` (`1000×1000` in Short #1 `R02b`) and `PIA18182.jpg` (`1720×1720` in Short #1 `R09b`):* Because a tight planetary globe surrounded by black space can trigger `gate_shorts_open.py`'s `no edge` / `blur-pad` heuristic if the top (`y=0..345`) and bottom (`y=1575..1920`) strips are flat black, compose the full-bleed `1080×1920` space scene with subtle vertical scientific telemetry/grid lines, faint diffraction/nebula detail, or position the zoomed globe/ring arc and full-width scientific callout cards so the top, middle, and bottom vertical thirds carry continuous crisp visual structure (`edge_ratio >= 0.30`, `std_ratio >= 0.35`, and zero horizontal band seam at `y≈420` or `y≈656`).
   - **Code graphics / diagrams (`R05a` Axial Tilt Gauge in Short #1; `R52` Interior Cutaway in Short #2):** Render natively on a **`1080×1920` (`9:16`) vertical canvas**, never on `1920×1080` shrunk into `1080×608`!
     - In **Short #1 `R05a` (`18.20–22.20 s`)**, stack the two comparison globes **vertically** (`EARTH · 23.4° TILT` in the upper half `y=260..880`, `URANUS · 97.77° TILT (SIDEWAYS)` in the lower half `y=960..1580`) at full `1080×1920` resolution so both globes and protractor arcs are huge and effortlessly legible on a phone screen.
     - In **Short #2 `R52` (`14.84–18.76 s`)**, draw the 3-layer Uranus interior cross-section natively on `1080×1920` (`9:16`) with a large `820 px` diameter cutaway globe (`cy=860`), upper telemetry header (`y=220..400`), and lower layer legend (`y=1340..1620`).
3. **Include `"end_card": {"start_s": <loop_start_s>}` in both `_meta.json` files** (`35.44` for Short #1, `25.28` for Short #2) so `gate_shorts_open.py` verifies the end card cleanly.

### 7.2 Exact VO Slice & Timing Fix for Short #1 (`_assemble_033_short1_v02.py`)
- Update `VO_SEGMENTS` and `VO_GAPS` in `_assemble_033_short1_v02.py` so the aspirate `"H-"` of `"How"` (`49.250 s`) and the sibilant tail of `"darkness."` (`31.040 s`) are 100% preserved inside verified digital silence (`pk < 0.001`):
  ```python
  VO_SEGMENTS = [
      (0.080, 31.040),   # 30.960 s — opening paragraph (silence at 31.040s, pk=0.0008)
      (49.220, 53.880),   #  4.660 s — closing question (silence at 49.180..49.230s, pk=0.00009; "How" onset at 49.250s)
  ]
  VO_GAPS = [0.20]       # Segment 1 starts at 0.08 + 30.96 + 0.16 = 31.20 s (identical to v01 timeline!)
  ```
- Keep `TOTAL_S = 36.48` (`912` frames @ `25 fps`) and the 14 shot boundaries unchanged.

### 7.3 Exact VO Slice & Visual Plate Fix for Short #2 (`_assemble_033_short2_v02.py`)
1. **Fix `VO_SEGMENTS` so zero word onsets are clipped (preserving `"80%"` at `~12 s` and `"9,000"` at `~24 s`):**
   Slice **only** inside verified digital silence (`pk < 0.001` in `uranus_vo_v01.wav`) and never split continuous co-articulated phrases (`466.200..474.400 s` and `478.920..482.550 s`):
   ```python
   VO_SEGMENTS = [
       # Seg 0 (5.520 s): "What happens if a spacecraft dives beneath those clouds to land on the ice below?"
       (438.500, 444.020),
       # Seg 1 (3.650 s): "As an ice giant, Uranus has no true surface." (silence 459.500..459.600s -> 463.250s)
       (459.600, 463.250),
       # Seg 2 (2.450 s): "Beneath the hydrogen and helium clouds," (silence 463.650..463.750s -> 466.200s)
       (463.750, 466.200),
       # Seg 3 (2.780 s): "80% of the planet's mass" (silence 466.150..466.250s; "eighty" onset at 466.280s! Silence 468.960..469.000s)
       (466.200, 468.980),
       # Seg 4 (5.420 s): "is a crushing, superheated ocean of water, methane, and ammonia" (keep unbroken! Silence 474.400..474.820s)
       (468.980, 474.400),
       # Seg 5 (2.280 s): "above a small rocky core." (silence 474.750..474.820s -> 477.080s)
       (474.800, 477.080),
       # Seg 6 (1.160 s): "Near that core," (silence 477.100..477.650s -> 478.800s)
       (477.640, 478.800),
       # Seg 7 (3.650 s): "Uranus heats up to 9,000 degrees Fahrenheit." (keep unbroken! Silence 478.680..478.920s -> 482.550s)
       (478.900, 482.550),
   ]
   ```
   With small natural inter-clause breaths (`VO_GAPS` tuned so `TOTAL_S = 26.28 s` or `26.40 s` and `"80%"` lands at `~11.8 s`), adjust the shot cut points (`SHOT_SPECS`) to fall inside inter-clause silence or >120 ms from any word boundary (`polish_gate.py --cuts ... --words ...` `0` boundary cuts).
2. **Replace the 3 unrecognisable Voyager 2 narrow ring-strip stills (`PIA00142.jpg`, `PIA01977.jpg`, `PIA01985.jpg`) with full-bleed `9:16` Uranus plates (`<= 2.35×` upscale, `0` repeated stills within Short #2):**
   - **`R49a` (`0.00–1.88 s`), `frame0.jpg`, `cover.jpg`, and `R49_loop` (`25.28–26.28 s`):** Remove the `32%` `PIA00142.jpg` diagonal ring-line overlay from `r49_cut1` (`033_r49_cut1_1776026071_veo31_9x16.mp4` is already a native `1080×1920` `9:16` clip!). Also ensure `R49_loop` maps smoothly across `1.00 s` without holding on a static freeze frame for the final `0.24 s`.
   - **`R51a` (`5.60–7.80 s`, replacing `PIA01977.jpg` `754×735`):** Use a full-bleed `1080×1920` crop of `PIA18182.jpg` (`1720×1720` Hubble/Voyager composite Uranus globe with cloud bands and aurora, crop `960×1706` -> `1080×1920`, upscale `1.13×`) or `PIA01488.jpg` (`2118×2618` Hubble false-colour cloud bands and rings, crop `1080×1920`, upscale `1.00×`).
   - **`R53a` (`18.76–21.04 s`, replacing `PIA01985.jpg` `719×386`):** Use a full-bleed `1080×1920` crop of `weic2310a_unannotated.png` (`2000×2000` JWST NIRCam wider field of Uranus and glowing polar cap surrounded by deep-field galaxies, crop `1080×1920`, upscale `1.00×`) or `PIA02963_borderless.jpg` (`2160×2160` Hubble cloud-band montage, crop `1080×1920`, upscale `1.00×`), neither of which is used elsewhere in Short #2 (`R51b` uses `STScI-01GWQ3...` zoomed rings; `R51c` uses `weic2332a_hires.jpg`).
3. **Verify all 7 automated gates (`gate_shorts_open.py` `0%` blur-pad fail, `picture_qa.py` `0` issues / `0` low-detail warnings, `polish_gate.py`, `sfx_kit.py level`, `music_gate.py`, `thumb_preview.py short` Frame 0 & Cover) AND copy full non-zero `.mp4` files to both NAS `OWB UAT` and iCloud Drive `OWB UAT`.**
