# J2333 Moving-Video QA Review — 033 R01 and R55 Fallback Motion Against J2306 Scope

- **Job**: `J2333` (`033: watch R01 and R55 fallback motion against J2306 scope`, `kind: qa`, `film: 033`, `stage: picture`)
- **Upstream Jobs & Rulings**:
  - `J2306` (`jobs/reviews/J2306/CHIEF_RULING.md`, PR #610 merged `daa2f24bd92eeccdfa24f32ba9f8a7fded7bc0f9`, acting-Chief ruling by `codex`)
  - `J2332` (`033: generate bounded R01 and R55 world-shot fallback`, completed by `cursor` at `2026-11-07T02:50Z`)
- **Dependent Job**:
  - `J2334` (`033: accept or reject J2306 fallback assets before J2299 resumes`, `kind: chief`, `after: J2333`)
  - `J2299` (`033 picture: correct source identities and deliver reviewable opener and graphics`, `status: blocked` at `0/5` pending `J2334`)
- **Reviewer**: `gemini` (`gemini-argon`, worker QA lane; demonstrated `moving_video_input` registered via `chief_relay.py capabilities`)
- **Date**: `2026-11-08T04:40Z`
- **Overall Recommendation for `J2334` (Elected Chief)**: **`FIX` (`r01_flow_t1_silent.mp4` = `FIX`; `r55a_flow_t1_silent.mp4` = `FIX`; `r55b_flow_t1_silent.mp4` = `PASS`)**
  - **Summary**: All three `J2332` Flow Veo 3.1 Fast takes and their exact proposed `R01` (`0.00–4.35 s`) and `R55` (`493.01–505.35 s`) intervals were directly watched with demonstrated `moving_video_input` (`default_api:read_file` native `video/mp4` ingestion) and inspected at native `1280x720` resolution alongside `polish_gate.py`, `picture_qa.py`, and `ffprobe` measurements.
  - **`r55b_flow_t1_silent.mp4` (`1e71287f9abaafc8c3f586dc7a9cb195ea2193cd3b9d041e5b8c95715cb34fba`) PASSES** every `J2306` and Lesson 7 requirement for `R55` Cut 3 (`500.927–505.350 s`, source `0.000–4.423 s`).
  - **`r01_flow_t1_silent.mp4` (`65776fa6565a606be8ec14f9f42b8573c598b9c6f18ba4546446d5c0458f1e90`) FAILS (`FIX`)** `J2306`'s Uranus identity and ring-geometry requirements: Flow Veo rendered a **nearly horizontal (`~10°–12°` tilt) wide, bright Saturn-style ring sheet and brown/grey Jovian equatorial cloud belts**, rather than Uranus tipped on its side (`97.77°` axial tilt) with narrow, faint upright rings. (Its lower-bitrate duplicate tile encode `r01_tile_flow_t1_silent.mp4` `942a8ab255...` also fails `polish_gate.py` near-black at `t = 0.45 s`, `mean = 24.81 < 28.0`.)
  - **`r55a_flow_t1_silent.mp4` (`51b26b122e5d574e9a8a9850ab0a448d1843c641e48e588e375b28d924a82378`) FAILS (`FIX`)** `J2306`'s *"No solid surface"* rule and `4–6 s` picture-change rule: the lower half of the frame (`y = 320..720`) is a **flat, mirror-smooth horizontal ocean/ice surface reflecting a second giant planet limb rising above a starry horizon on the right (`x = 700..1120`)**, visually contradicting the spoken VO (*"While a spacecraft has nowhere to land on Uranus..."*) and the `NO SOLID GROUND` overlay (`494.0–497.8 s`). In addition, cutting `r55a` at `3.958 s` into two contiguous `1.0x` slices (`0.000–3.958 s` and `3.958–7.917 s`) produces a single uninterrupted `7.917 s` shot with no picture change at `496.968 s`.

---

## 1. Capability & Direct Moving-Video Inspection Evidence

- **Capability Registration (`chief_relay.py capabilities`)**:
  - `python3 scripts/chief_relay.py capabilities --agent gemini --available 'moving_video_input' --evidence 'Demonstrated multimodal video/mp4 input via default_api:read_file on J2332 silent masters r01_flow_t1_silent.mp4 (65776fa656), r01_tile_flow_t1_silent.mp4 (942a8ab255), r55a_flow_t1_silent.mp4 (51b26b122e), and r55b_flow_t1_silent.mp4 (1e71287f9a), returning native video/mp4 part_0 sequences (00:00-00:07).'`
- **Media Directly Watched via `default_api:read_file` (`video/mp4` multimodal ingestion + native `1280x720` frame inspection)**:
  1. Full silent masters in `/Volumes/data/mac-mini-archive/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/04_Generated-Clips/J2332/` (and synced via `nice -n 15 rsync -a --partial --update` to `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/04_Generated-Clips/J2332/`):
     - `r01_flow_t1_silent.mp4` (`0.000–7.917 s`)
     - `r01_tile_flow_t1_silent.mp4` (`0.000–7.917 s`)
     - `r55a_flow_t1_silent.mp4` (`0.000–7.917 s`)
     - `r55b_flow_t1_silent.mp4` (`0.000–7.917 s`)
  2. Exact selected intervals trimmed for inspection:
     - `r01_selected_0.40_4.75.mp4` (source `0.400–4.750 s` → film `0.000–4.350 s`, `4.350 s`, `105` frames)
     - `r55_cut1_r55a_0.000_3.958.mp4` (source `0.000–3.958 s` → film `493.010–496.968 s`, `3.958 s`, `95` frames)
     - `r55_cut2_r55a_3.958_7.917.mp4` (source `3.958–7.917 s` → film `496.968–500.927 s`, `3.959 s`, `95` frames)
     - `r55_cut3_r55b_0.000_4.423.mp4` (source `0.000–4.423 s` → film `500.927–505.350 s`, `4.423 s`, `107` frames)

---

## 2. Exact File Hashes, Technical Probes & Budget/Take Audit

### 2.1 File Inventory & SHA-256 Hashes (Verified on Both `mac-mini-archive` and `studio-live`)

| Role | Filename | Bytes | SHA-256 | Stream / Format Probe | Upscale to `1920x1080` |
|---|---|---:|---|---|---|
| **R01 Canonical Silent** | `r01_flow_t1_silent.mp4` | `1,118,001` | `65776fa6565a606be8ec14f9f42b8573c598b9c6f18ba4546446d5c0458f1e90` | `h264` High, `1280x720`, `24/1 fps`, `190` frames, `7.916667 s`, `nb_streams=1` (`video` only, `0` audio) | `1.50x` (`<= 2.35x` PASS) |
| **R01 Tile Silent (2nd encode)** | `r01_tile_flow_t1_silent.mp4` | `651,258` | `942a8ab2556819120f1a4ee54b5b9a5b4e890322bef872a41a74ff165204763f` | `h264`, `1280x720`, `24/1 fps`, `190` frames, `7.916667 s`, `nb_streams=1` (`video` only, `0` audio) | `1.50x` (`<= 2.35x` PASS) |
| **R55a Canonical Silent** | `r55a_flow_t1_silent.mp4` | `1,125,888` | `51b26b122e5d574e9a8a9850ab0a448d1843c641e48e588e375b28d924a82378` | `h264` High, `1280x720`, `24/1 fps`, `190` frames, `7.916667 s`, `nb_streams=1` (`video` only, `0` audio) | `1.50x` (`<= 2.35x` PASS) |
| **R55b Canonical Silent** | `r55b_flow_t1_silent.mp4` | `1,825,626` | `1e71287f9abaafc8c3f586dc7a9cb195ea2193cd3b9d041e5b8c95715cb34fba` | `h264` Baseline, `1280x720`, `24/1 fps`, `190` frames, `7.916667 s`, `nb_streams=1` (`video` only, `0` audio) | `1.50x` (`<= 2.35x` PASS) |
| **Generation Manifest** | `generation.json` | `19,282` | `781d05d4f7aaa79832719147a0cdb5d265d5e3bc86d1625e39e126cc7937d4c5` | JSON metadata & `ffprobe` records | — |
| *(Raw with Veo audio, unused)* | `r01_flow_t1.mp4` | `1,267,209` | `ff18415d378e6bdba4f5bd628897aff48bd7f9d0ac807be3011ea822ef153841` | `1280x720`, `7.917 s` (raw Veo download before `-an` strip) | — |
| *(Raw with Veo audio, unused)* | `r01_tile_flow_t1.mp4` | `779,914` | `56679b127c52beb8c10be3c395efb77a630283379537d00fde43f49b9d06162a` | `1280x720`, `7.917 s` (raw tile download before `-an` strip) | — |
| *(Raw with Veo audio, unused)* | `r55a_flow_t1.mp4` | `1,254,528` | `b8ac30b30455a6e3caea155f5fabcb2c2a2a6d24caf9b26093638c2876c24563` | `1280x720`, `7.917 s` (raw Veo download before `-an` strip) | — |
| *(Raw with Veo audio, unused)* | `r55b_flow_t1.mp4` | `1,954,266` | `9f0f85acfaeccdd301676c07ccf2daea5af3de36d3637e93468c1416386fd1ee` | `1280x720`, `7.917 s` (raw Veo download before `-an` strip) | — |

### 2.2 Budget, Take & Credit Compliance (`05_Analytics/ai_spend/ledger.jsonl` lines 576–580)

- **Scope Authorised by `J2306`**: Flow Veo 3.1 only, `3` takes maximum, `<= 100` credits per take, `<= 300` existing subscription credits total, `£0.00` monetary spend, no Vertex, no Omni, no new VO/music.
- **Actual Execution Verified**:
  - **Pre-generation balance read** (`2026-11-07T02:41:35Z`, line 576): `14,890.0` Flow credits (the studio Ultra account, CDP `9222`, project `a1400a5e-916a-4c90-b6f2-15c0838500f8`; `Veo 3.1 - Fast 8s 16:9 x1` = `10` credits).
  - **Take 1 (`r01`)** (`2026-11-07T02:43:17Z`, line 577): `10.0` Flow credits (`text-to-video`, no start frame).
  - **Take 2 (`r55a`)** (`2026-11-07T02:44:19Z`, line 578): `10.0` Flow credits (`text-to-video`, no start frame).
  - **Take 3 (`r55b`)** (`2026-11-07T02:44:35Z`, line 579): `10.0` Flow credits (`text-to-video`, no start frame).
  - **Post-generation balance read** (`2026-11-07T02:49:45Z`, line 580): `14,860.0` Flow credits (`30.0` total credits spent; `0` monetary spend; no 4th `Create`).
  - **Status**: **PASS** (`3/3` takes, `10/100` credits per take, `30/300` total credits, `£0.00` cash).

---

## 3. Detailed Moving-Video & Gate Assessment by Row and Interval

### 3.1 `R01` (`0.00–4.35 s`) — `r01_flow_t1_silent.mp4` (`65776fa656...`) & `r01_tile_flow_t1_silent.mp4` (`942a8ab255...`) — **VERDICT: `FIX`**

- **Selected Interval & Scribe VO Alignment**:
  - Film span: `0.00–4.35 s` (`4.35 s`, `1` cut, `R02` starts at `4.35 s`).
  - Source span: `0.40–4.75 s` (`0.40 s` head handle, `3.167 s` tail handle out of `7.917 s`).
  - Spoken VO (`uranus_vo_v01.wav`, SHA-256 `3d73576e0c20be9030546db7bc71ea0107602d5e5fbdde37cba28c7d5b43f460`): *"At the North Pole of Uranus, the seventh planet in orbit around our sun,"* (`0.100–4.059 s`), followed by `"what"` at `4.640 s` (`0.581 s` inter-word silence; cut at `4.35 s` leaves `0.291 s` after `"sun,"` and `0.290 s` before `"what"` — **PASS on timing**).
- **Native Generated Motion & `polish_gate.py` Metrics**:
  - Motion: Smooth continuous camera push-in (`105` frames in `0.40–4.75 s`, `mean_frame_diff = 0.443`, `min_frame_diff = 0.287`, `0` frozen frame pairs, `0` replayed frames).
  - `polish_gate.py` on `r01_flow_t1_silent.mp4` (`65776fa656...`): `start` (`0.45 s`) `mean = 36.32`, `p95 = 166.0`, `std = 48.50`, `edge = 0.0331`; `mid` (`2.575 s`) `mean = 41.68`, `p95 = 177.0`, `std = 53.45`, `edge = 0.0337`; `end` (`4.65 s`) `mean = 48.30`, `p95 = 185.0`, `std = 58.26`, `edge = 0.0345`; `seams = []`; `near_black_fail = false`, `low_detail_fail = false`, `noise_fail = false`.
  - `polish_gate.py` on `r01_tile_flow_t1_silent.mp4` (`942a8ab255...`): **FAILS `near_black`** at `start` (`0.45 s`: `mean = 24.81 < 28.0`).
- **Visual & Scientific Inspection (`moving_video_input` + `1280x720` frames) — WHY `R01` IS `FIX`**:
  1. **Wrong Axial Tilt (`~10°–12°` Horizontal Instead of `97.77°` Sideways / Upright Rings)**:
     - `J2306` (`CHIEF_RULING.md`) requires: *"one 8-second take of recognisable blue-green Uranus and its narrow rings, with gentle continuous camera movement and stable geometry... Use the verified Uranus source identities in PR584 and accepted tilt/ring references in SOURCES.md/CLAUDE_QUOTE_CHECK_v01 to establish appearance and ring/axis relationship. No invented orbital geometry, giant Saturn rings, surface terrain or unexplained fast spinning."*
     - In `r01_flow_t1_silent.mp4`, the ring plane and equatorial cloud bands are oriented **nearly horizontally** across the screen (`~10°–12°` tilt from horizontal, running from left tip `(x=44, y=456)` to right tip `(x=1246, y=282)`), like Saturn or a conventionally upright planet, instead of Uranus's `97.77°` sideways axial tilt with upright/vertical rings (`SHOT_LIST_v01.md` `R01` answer image by `0:05`).
  2. **Giant Saturn-Style Rings & Jovian Dark Cloud Belts**:
     - Instead of Uranus's 13 faint, narrow dark rings (`R21–R22`), the video displays a **wide, bright, opaque Saturn-style concentric ring sheet with a prominent Cassini-like division**, explicitly prohibited by `J2306` (*"No... giant Saturn rings"*).
     - Across the illuminated disc, the planet displays **prominent horizontal brown/grey Jupiter/Saturn-like turbulent storm belts** rather than Uranus's pale cyan-turquoise methane haze.

---

### 3.2 `R55` Cuts 1 & 2 (`493.010–500.927 s`) — `r55a_flow_t1_silent.mp4` (`51b26b122e...`) — **VERDICT: `FIX`**

- **Selected Intervals & Scribe VO Alignment**:
  - Proposed Cut 1: source `0.000–3.958 s` → film `493.010–496.968 s` (`3.958 s`, `95` frames).
  - Proposed Cut 2: source `3.958–7.917 s` → film `496.968–500.927 s` (`3.959 s`, `95` frames).
  - Spoken VO (`493.404–504.884 s`): *"While a spacecraft has nowhere to land on Uranus, it could not fly through its atmosphere unscathed either. Extreme pressures and temperatures would destroy a metal spacecraft."* (`"tops."` ends `492.624 s`, `"While"` starts `493.404 s`, `"spacecraft."` ends `504.884 s`, `"If"` starts `505.824 s` — row boundaries `493.01 s` and `505.35 s` sit cleanly inside inter-word pauses).
- **Visual, Scientific & Editorial Inspection (`moving_video_input` + `1280x720` frames) — WHY `r55a` IS `FIX`**:
  1. **Flat Mirror/Ocean Surface Horizon & Second Giant Planet Globe in Sky (`J2306` "No solid surface" Violation)**:
     - `J2306` (`CHIEF_RULING.md`) mandates: *"two 8-second world takes providing distinct views of a blue-green atmospheric cloud passage. No solid surface, robot, spacecraft destruction, pressure measurement or claimed observation."*
     - Across all `7.917 s` of `r55a_flow_t1_silent.mp4`, the lower half of the frame (`y = 320..720`) is a **flat, mirror-smooth horizontal surface** (resembling calm water or polished flat ice) that reflects both the central storm clouds and a **second giant planet limb rising above the horizon on the right (`x = 700..1120`)**, separated from the upper cloud ceiling by a black starry space gap (`y = 255..305`).
     - Showing a flat horizontal surface/ocean horizon looking out at another giant planet in the sky while the narrator says *"While a spacecraft has nowhere to land on Uranus"* and the planned overlay (`494.0–497.8 s`) reads **`NO SOLID GROUND`** is a direct visual-verbal contradiction (`AGENTS.md` Channel Authority / Lesson 7).
  2. **No Visual Cut Between Cut 1 (`0.000–3.958 s`) and Cut 2 (`3.958–7.917 s`) (`7.917 s > 6.0 s` Hold)**:
     - Because `r55a_flow_t1_silent.mp4` is one uninterrupted slow forward camera push (`mean_frame_diff = 1.560` in Cut 1, `1.329` in Cut 2, `0` frozen frames) and `J2332` specified `"crop": "none"` on both consecutive slices, playing `0.000–3.958 s` followed immediately by `3.958–7.917 s` produces a **single unbroken `7.917 s` shot** with no picture change at `496.968 s`, violating the `4–6 s` picture-change rule.

---

### 3.3 `R55` Cut 3 (`500.927–505.350 s`) — `r55b_flow_t1_silent.mp4` (`1e71287f9a...`) — **VERDICT: `PASS`**

- **Selected Interval**:
  - Proposed Cut 3: source `0.000–4.423 s` → film `500.927–505.350 s` (`4.423 s`, `107` frames; full `0.000–7.917 s` clip is also clean).
- **Visual, Scientific & Technical Gate Inspection (`moving_video_input` + `1280x720` frames) — WHY `r55b` IS `PASS`**:
  1. **Subject & Cloud Continuity (`J2306` Scope)**:
     - High oblique orbital glide over a curved blue-green and turquoise ice-giant cloud deck with a large swirling cloud vortex and dark starry space beyond the upper-right atmospheric limb.
     - Continuous gas clouds only: **no solid surface**, no flat horizon reflection, no second planet in the sky, no robot, no spacecraft, no pressure gauge, no burned-in text or diagram.
  2. **Native Generated Movement**:
     - Smooth, continuous orbital camera slide across all `107` frames (`0.000–4.423 s`: `mean_frame_diff = 5.711`, `min_frame_diff = 4.696`, `max_frame_diff = 6.583`, `0` frozen frame pairs, `0` replayed frames; tail window `3.958–7.917 s` is equally smooth with `mean_frame_diff = 5.533`, `0` frozen pairs).
  3. **`polish_gate.py` & `picture_qa.py` Readiness**:
     - `start` (`0.05 s`): `mean = 105.53`, `p95 = 194.0`, `std = 55.41`, `edge = 0.0623`, `seams = []`.
     - `mid` (`2.212 s`): `mean = 115.70`, `p95 = 198.0`, `std = 55.52`, `edge = 0.0775`, `seams = []`.
     - `end` (`4.323 s`): `mean = 116.22`, `p95 = 198.0`, `std = 55.77`, `edge = 0.0670`, `seams = []`.
     - `near_black_fail = false`, `low_detail_fail = false`, `noise_fail = false`.
     - Upscale to `1920x1080`: `1.50x` (`<= 2.35x` PASS).
  4. **`R54` Chart-to-Moving-World Separation, Overlays, Grain & Disclosure**:
     - Separates `R54` (`code_graphic_033_r54_core_vs_cloud_temp.mp4`, `487.24–493.01 s` full-frame chart) from `R55` with a moving world cloud plate (chart-to-moving-world-plate, not chart-to-chart).
     - Carries no burned-in text; ready for edit-stage short overlays (`NO SOLID GROUND` at `494.0–497.8 s`, `3.8 s <= 4.0 s`, `3` words; `EXTREME PRESSURE & HEAT` at `500.5–504.3 s`, `3.8 s <= 4.0 s`, `4` words) and corner `CGI` disclosure credit (timed clear of the short overlays so only one label appears at a time), plus edit-stage fine grain on dark space gradients.

---

## 4. Checklist Against `J2333` & `J2306` Requirements

| Requirement | `r01_flow_t1_silent.mp4` (`65776fa656`) | `r55a_flow_t1_silent.mp4` (`51b26b122e`) | `r55b_flow_t1_silent.mp4` (`1e71287f9a`) |
|---|---|---|---|
| **Watched with demonstrated `moving_video_input`** | **PASS** (`default_api:read_file` `video/mp4`) | **PASS** (`default_api:read_file` `video/mp4`) | **PASS** (`default_api:read_file` `video/mp4`) |
| **Exact SHA-256 & silent stream (`0` audio)** | **PASS** (`65776fa656...`, `1` video stream) | **PASS** (`51b26b122e...`, `1` video stream) | **PASS** (`1e71287f9a...`, `1` video stream) |
| **Native generated movement (`24 fps`, `0` freezes)** | **PASS** (`mean_diff = 0.443`, `0` freezes) | **PASS** (`mean_diff = 1.560`, `0` freezes) | **PASS** (`mean_diff = 5.711`, `0` freezes) |
| **Uranus identity & `97.77°` narrow ring geometry** | **FAIL (`FIX`)** — `~10°–12°` horizontal wide Saturn-like rings & brown Jovian bands | N/A (`R55` cloud passage) | **PASS** (blue-green ice-giant cloud deck) |
| **Cloud continuity & "No solid surface"** | N/A (`R01` full-planet view) | **FAIL (`FIX`)** — flat reflective surface/ocean horizon + 2nd giant planet in sky | **PASS** (continuous atmospheric clouds only) |
| **Distinct from excluded Short opener (`svs20390`)** | **PASS** (`svs20390` not used) | **PASS** | **PASS** |
| **Locked VO timing (`R01` `0–4.35s`; `R55` `493.01–505.35s`)** | **PASS** (`0.40–4.75s` → `0.00–4.35s`) | **PASS** (`493.010–500.927s`) | **PASS** (`500.927–505.350s`) |
| **Nonreplaying intervals & `4–6 s` picture changes** | **PASS** (`4.35 s` single cut) | **FAIL (`FIX`)** — two contiguous `1.0x` slices of one shot = `7.917 s` unbroken hold | **PASS** (`4.423 s` cut; non-overlapping `3.958 s` + `3.959 s` windows available) |
| **`R54` chart-to-moving-world separation** | N/A (`R01`) | **FAIL (`FIX`)** (unsuitable horizon scene) | **PASS** (moving world cloud plate after `R54` chart) |
| **Upscale `<= 2.35x` (`1280x720` → `1080p` = `1.50x`)** | **PASS** (`1.50x`) | **PASS** (`1.50x`) | **PASS** (`1.50x`) |
| **No burned-in text; ready for `<= 4s`, `<= 4w` overlays & `CGI` disclosure** | **PASS** (clean plate, no text) | **PASS** (clean plate, no text) | **PASS** (clean plate, no text) |
| **`polish_gate.py` (detail, seams, near-black, noise)** | **PASS** on canonical `r01` (`FAIL` near-black on `r01_tile` at `0.45s`, `mean=24.81`) | **PASS** pixel floor (`mean=111–133`) | **PASS** (`mean=105–116`, `edge=0.062–0.078`, `0` seams) |
| **Budget/take cap (`<= 3` takes, `<= 300` credits, `£0`)** | **PASS** (`10` credits) | **PASS** (`10` credits) | **PASS** (`10` credits; `30/300` total, `£0`) |

---

## 5. Actionable Recommendation for Dependent Elected-Chief Job `J2334`

1. **Accept `r55b_flow_t1_silent.mp4` (`1e71287f9abaafc8c3f586dc7a9cb195ea2193cd3b9d041e5b8c95715cb34fba`)** as a verified moving-world atmospheric cloud asset for `R55` (`493.01–505.35 s`).
2. **Reject (`FIX`) `r01_flow_t1_silent.mp4` (`65776fa6565a606be8ec14f9f42b8573c598b9c6f18ba4546446d5c0458f1e90`), `r01_tile_flow_t1_silent.mp4` (`942a8ab2556819120f1a4ee54b5b9a5b4e890322bef872a41a74ff165204763f`), and `r55a_flow_t1_silent.mp4` (`51b26b122e5d574e9a8a9850ab0a448d1843c641e48e588e375b28d924a82378`)**.
3. **Keep `J2299` held at `0/5` and choose one of the two bounded fixes in `J2334`**:
   - **Option A (Bounded 2-take Flow Veo 3.1 replacement within the remaining `270 / 300` already-authorised subscription credits from `J2306`)**:
     - Because `J2332` used only `30` of `J2306`'s `300`-credit cap (`14,890 -> 14,860`), queue a bounded 2-take replacement (`20` credits on Fast or `200` on Quality, `£0` cash):
       1. **`R01` (`0.00–4.35 s`)**: Prompt for a featureless pale cyan-turquoise ice-giant globe with **thin, faint, dark vertical rings oriented straight up-and-down (12 o'clock to 6 o'clock, `98°` sideways tilt), explicitly banning horizontal rings, wide Saturn rings, Cassini divisions, and brown/tan Jovian stripes** (or generate a clean sideways cyan globe and orient its ring axis to `97.77°` so geometry is exact).
       2. **`R55a` (`493.01–500.93 s`)**: Prompt for a **top-down or oblique pass completely inside thick cyan-turquoise cloud tops filling 100% of the frame, explicitly banning any horizon line, water/ice reflection, flat ground, stars, or second planet in the sky**. To satisfy both the `4–6 s` picture-change rule and `picture_qa.py`'s `SAME_STRETCH = 10.0 s` check across the `12.34 s` row (`493.01–505.35 s`), pair the two non-overlapping halves of one take (`0.000–3.958 s` at `1.00x` wide and `3.958–7.917 s` at `1.30x` push crop = `1.95x <= 2.35x` total upscale, creating a clean visual cut at `496.968 s` inside a single `picture_qa.py` source run) with `r55b_flow_t1_silent.mp4` (`0.000–4.423 s` at `500.927–505.350 s`).
   - **Option B (Zero-generation / `0`-credit path inside `J2299`)**:
     - Use accepted `r55b_flow_t1_silent.mp4` (`0.000–3.958 s` at `1.00x` + `3.958–7.917 s` at `1.30x` crop for `493.010–500.927 s`, `<= 1.95x` upscale) followed by a graded real NASA Uranus cloud-limb plate (`PIA01280` / `PIA01985` / `PIA00142` for `500.927–505.350 s`) so `R55` is 100% compliant now with `0` extra takes, and scope only `R01` (`0.00–4.35 s`).
