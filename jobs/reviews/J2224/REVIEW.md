# Review — J2224 (for J0912): HOS 008 Short A `v03` (`picture_qa` Key-Ribbon Reuse Decision)

- **Review Job:** `J2224` (`kind: review`, `review_of: J0912`)
- **Reviewed Build Job:** `J0912` (`Backlog HOS: next search-titled Short cut from a locked long (existing VO + picture only)`, local branch `cursor/j0912-short-a-v03`, commit `830f6b355da8dbeb6d73fb456c0cc758ca53437c`, HOS Desk `#180` comment `6661680750`)
- **Reviewer:** `gemini` (`Gemini 4 Argon (High)` / `gemini-argon`, Rule H review lane)
- **Date:** `2026-11-07`
- **Channel / Film / Asset:** History of Science (`HOS:008`, *Why Did Franklin Fly a Kite in a Storm?*) — Short A `v03` (`10_Shorts/hos_008_short_A_v03.mp4`, title draft *Why Was Franklin's Kite Experiment So Dangerous?*)
- **Verdict:** **`FIX` — Reopen `J0912` to build `hos_008_short_A_v04.mp4` (`£0`, existing approved HOS 008 KEEP plates only) by replacing `S06` (`15.76–19.52 s`, currently a duplicate slice of `13_key_ribbon_t1.mp4` that fails `picture_qa.py`) with the approved Part 4 storm-shed key/ribbon plate `04_Generated-Clips/part04/raw/v01/09_charge_string_c1_t1.mp4` (`in_s: 0.60`, or `09_charge_string_t1.mp4`).**
- **Spend:** `£0` (`0` Flow credits, `£0.00` Vertex, `0` ElevenLabs characters; local ffmpeg assembly and verification only)

---

## 1. Executive Decision & Rule H Verdict (`FIX`)

**Decision: `FIX` (reopen `J0912` with exact 1-row `S06` replacement recipe).**

1. **Why `hos_008_short_A_v03.mp4` Cannot Be Marked `KEEP`:**
   - Under `AGENTS.md` (*"Definition of done (the contract): A stage is done only when its check prints PASS... A check can't be skipped, edited to pass, or swapped for another tool"*) and Standing Lesson 7 (`picture_qa.py` must `PASS` with `0` failures), `hos_008_short_A_v03.mp4` (`sha256: f88315e04718366aa8446ce9aec6ea947b9ebfb7da566698132e8344d3bceab6`) **fails `picture_qa.py` (`exit 1`)** on row `s06` (`15.76–19.52 s`):
     ```text
     FAIL   0:18 row s06 13_key_ribbon_t1.mp4: reuse: same stretch as 0:07 (give it a new stretch, or a new render)
     ```
   - `13_key_ribbon_t1.mp4` is an `8.00 s` plate (`1280×720`, `24 fps`). Using it at `s03` (`5.76–9.14 s`, `in_s = 0.60 s`) and again at `s06` (`15.76–19.52 s`, `in_s = 4.10 s`) separates the two in-points by only `3.50 s` (`< 10.0 s` minimum source-offset separation in `picture_qa.py`). An `8.00 s` clip can never supply two stretches `>= 10.0 s` apart.
   - Visually and editorially, `13_key_ribbon_t1.mp4` is an indoor sunlit workshop bench shot of Franklin tying the knot before going out into the storm. Cutting back to the sunlit indoor table at `s06` (`15.76–19.52 s`, spoken: *"jumped across. If lightning had struck the kite,"*) between two storm scenes (`s05` `02_knuckle_spark_t1.mp4` at `12.10–15.76 s` and `s07` `10_richmann_rod_t1.mp4` at `19.52–22.24 s`) breaks weather/location continuity.

2. **Why This Is Solved at `£0` Without Generation or Rule Waiver:**
   - When `J0912` preflight (`commit 20502ef3`) inventoried Short A, it only listed the 6 plates from `SHORTS_PICTURE_PLAN_v02.json` (`01_kite_open_t1`, `19_kite_climb_t1`, `13_key_ribbon_t1`, `25_fibres_rise_t1`, `02_knuckle_spark_t1`, `10_richmann_rod_t1`).
   - However, the approved HOS 008 long picture lock (`rough_v12` / `master_v03`, Chief `h22` `6533306017` and `h35` `6537320070`, `cuts_rough_v12.json`) already has **approved KEEP plates on both the Mini and the NAS** for the exact Part 4 sequence immediately after `08_teach_charge` (`351.84–358.96 s`) and immediately before `10_richmann_rod` (`368.91–375.37 s`):
     - **Primary replacement for `s06` (`15.76–19.52 s`, `3.76 s`):** `04_Generated-Clips/part04/raw/v01/09_charge_string_c1_t1.mp4` (`sha256: 611e2633f2ea7f4417272b91af41b857bb6733d416363918a17a111be56f9c80`, `8.00 s`, `1280×720`, `24 fps`, `in_s: 0.60`). Shows a close-up in the open Philadelphia 1752 shed doorway in heavy storm rain on the heavy iron key and dry silk ribbon hanging from the wet hemp kite string (`rough_v12` row `09_charge_string_c1`, `364.25–368.91 s`).
     - **Alternate approved replacement for `s06`:** `04_Generated-Clips/part04/raw/v01/09_charge_string_t1.mp4` (`sha256: e2045b3626ae919e2086f9d3b7254d82fd67a2cc38d5e9673a5812674a1b9061`, `8.00 s`, `1280×720`, `24 fps`, `in_s: 0.60`, `rough_v12` row `09_charge_string`, `358.96–364.25 s`, showing charge travelling down the wet hemp string to the key and silk ribbon held by Franklin in the storm shed), or `04_Generated-Clips/part03/raw/v01/13_key_ribbon_c1_t1.mp4` (`sha256: 56769bf3c7e13a9cc1bfd85ee185b4355f685254e69c2a7f60108b8f971a6da7`, `rough_v12` row `13_key_ribbon_c1`, `258.62–262.43 s`).
   - Direct `polish_gate.py` testing on the `952×1692` (`2.35×` Lanczos) centre crop of `09_charge_string_c1_t1.mp4` (`in_s = 0.60 s`, `dur = 3.76 s`) confirms **`exit 0` (`PASS`) with zero warnings** (`std = 40.11`, `mean = 51.22`, `p95 = 145.0`, `edge = 0.0595 > 0.0297` film p5, `seams = []`, `fail = []`), and because `09_charge_string_c1_t1.mp4` is a distinct file used once in Short A, **`picture_qa.py` passes with `0` failures (`exit 0`)**.

> **Capability & Sensory Boundary Note (`AGENTS.md`):** This review session recorded `chief_relay.py capabilities --agent gemini --available ''` (reading `.mp4` via `read_file` returns 1 Hz still frames and ASR transcript only, not raw audio playback or continuous 30 fps motion perception). Verification was performed via 1 Hz frame inspection (`00:00–00:22`), `ffprobe`/`ffmpeg` measurements, SHA-256 verification across Mini and NAS, and the studio QA gate tools (`gate_shorts_open.py`, `polish_gate.py`, `picture_qa.py`, `music_gate.py`, `sfx_kit.py level`). Per `AGENTS.md`, Ben's final watch is the watch-and-listen check after all automated gates pass.

---

## 2. Technical Audit of `hos_008_short_A_v03.mp4` (`commit 830f6b35`)

### 2.1 File, VO, and Chief `h47` Recipe Compliance

| Check / Parameter | Requirement (`J0912` / Chief `h47` `2026-11-05T09:22Z` / `AGENTS.md`) | `hos_008_short_A_v03.mp4` (`830f6b35`) | Status |
|---|---|---|---|
| **Master SHA-256 (Mini & NAS)** | Identical on Mini & NAS; no media in git | `f88315e04718366aa8446ce9aec6ea947b9ebfb7da566698132e8344d3bceab6` (`14,613,668` B) | **PASS** |
| **Locked VO (`hos_008_short_A_v02.mp3`)** | Unchanged (`sha256: 40ed4c4e…a28e`), `22.24 s`, `59` words | `40ed4c4e2a1f2e58608cfe690bb8afd6e1d64c80eafb0a75f37d47648a7ba28e` (`22.24 s`, `59` words) | **PASS** |
| **Dimensions & Upscale Cap** | 9:16 vertical, upscale `<= 2.35×` from `1280×720` plates | `952×1692` @ `30/1 fps` (`2.35×` Lanczos scale `3008×1692`, centre crop `952×1692`) | **PASS** |
| **YouTube Title Draft (`h47`)** | *Why Was Franklin's Kite Experiment So Dangerous?* | `Why Was Franklin's Kite Experiment So Dangerous?` | **PASS** |
| **Payoff Timing (`>= 70%`)** | Danger question answered in final sentence starting `>= 70%` | `"If"` starts at `17.84 s / 23.24 s = 76.8%` (`>= 70%`) | **PASS** |
| **Opening & Hook (`0.0–2.0 s`)** | Frame 0 hook caption with yellow word, VO onset `<= 0.15 s`, cut 1 `<= 3.0 s` | `NEVER HIT IT` (`NEVER` in yellow `#FFD646`, `cap_pct = 9.04%`), VO onset `0.14 s`, cut 1 at `2.58 s` | **PASS** |
| **Single Teach Overlay (`h47`)** | `PHILADELPHIA · 1752` (`WHEN`) at `2.7–6.2 s`, inside 16:9 band, hold `<= 4.0 s`, no 2nd overlay | `PHILADELPHIA · 1752` (`2.70–6.20 s`, `3.50 s <= 4.0 s`, `0.40 s` fade in/out, `61 px = 11.4%` of band height, inside `y=563..1128`), `08_teach_charge` dropped | **PASS** |
| **Promoted Long Title (`9.0–14.0 s`)** | Exact long title at `9–14 s` | `Why Did Franklin Fly a Kite in a Storm?` (`9.0–14.0 s`, `58 px` Didot at `y=220`) | **PASS** |
| **Loop Tail (`22.24–23.24 s`)** | `<= 1.0 s` (`< 1.2 s` tail gap) returning to frame-0 plate (`01_kite_open_t1.mp4`) | `22.24–23.24 s` (`01_kite_open_t1.mp4` `0.20–1.20 s` leading into frame-0 `1.20 s`; `tail_gap = 1.13 s`) | **PASS** |
| **Loudness & Mix** | `-14.0 ± 0.5 LUFS`, true peak `<= -1.6 dBTP`, `sfx_kit.py level` PASS, `music_gate.py` PASS | `-14.3 LUFS`, `-1.9 dBTP`, `sfx_kit.py level` PASS (`VO -20.7 LUFS, SFX -50.6 LUFS`), `music_gate.py` PASS (`66.7 BPM`, brief `64–76 BPM`) | **PASS** |
| **Picture QA (`picture_qa.py`)** | `0` failures (`exit 0`) | **FAIL (`exit 1`)**: `0:18 row s06 13_key_ribbon_t1.mp4: reuse: same stretch as 0:07` | **FAIL (Fix Required)** |

---

## 3. Verification of Approved HOS 008 `KEEP` Replacement Plates for `S06` (`15.76–19.52 s`)

All candidate replacement plates from the approved HOS 008 long master (`rough_v12` / `master_v03`, `cuts_rough_v12.json`) were verified on both the Mini (`/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/`) and the NAS (`/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips/`) and tested through `polish_gate.py` at `952×1692` (`2.35×` centre crop, `in_s = 0.60 s`, `dur = 3.76 s`):

| Candidate Plate (`04_Generated-Clips/...`) | Approved Long Row (`cuts_rough_v12.json`) | SHA-256 (Verified on Mini & NAS) | `952×1692` `polish_gate.py` Metrics (`in_s = 0.60 s`, `3.76 s`) | Visual / Continuity Fit for `S06` (`15.76–19.52 s`, *"jumped across. If lightning had struck the kite,"*) |
|---|---|---|---|---|
| **`part04/raw/v01/09_charge_string_c1_t1.mp4` (Recommended Primary)** | `09_charge_string_c1` (`364.25–368.91 s`) | `611e2633f2ea7f4417272b91af41b857bb6733d416363918a17a111be56f9c80` | **PASS (`exit 0`, 0 warns)**: `std=40.11`, `mean=51.22`, `p95=145.0`, `edge=0.0595` (`> 0.0297` p5), `seams=[]` | Close-up in the Philadelphia 1752 storm shed doorway in pouring rain on the iron key and silk ribbon hanging from the wet hemp kite string. Preserves storm continuity between `s05` (`02_knuckle_spark_t1`) and `s07` (`10_richmann_rod_t1`). |
| **`part04/raw/v01/09_charge_string_t1.mp4` (Approved Alternate 1)** | `09_charge_string` (`358.96–364.25 s`) | `e2045b3626ae919e2086f9d3b7254d82fd67a2cc38d5e9673a5812674a1b9061` | **PASS (`exit 0`)**: `std=37.82`, `mean=80.15`, `p95=141.0`, `edge=0.0200`, `seams=[]` | Storm shed doorway: electrical charge/sparks run down the wet hemp kite string to the hanging iron key and dry silk ribbon held by Franklin. |
| **`part03/raw/v01/13_key_ribbon_c1_t1.mp4` (Approved Alternate 2)** | `13_key_ribbon_c1` (`258.62–262.43 s`) | `56769bf3c7e13a9cc1bfd85ee185b4355f685254e69c2a7f60108b8f971a6da7` | **PASS (`exit 0`, 0 warns)**: `std=49.16`, `mean=109.74`, `p95=205.0`, `edge=0.0551` (`> 0.0297` p5), `seams=[]` | Distinct continuation plate of Franklin lifting the iron key by the silk ribbon (`13_key_ribbon_c1_t1.mp4` vs `13_key_ribbon_t1.mp4`). |

---

## 4. Exact Fix List for `J0912` (`hos_008_short_A_v04.mp4`)

1. **Create `_build_short_A_v04.py` (preserving `_build_short_A_v03.py` and `hos_008_short_A_v03.mp4` untouched) and replace `S06` (`15.76–19.52 s`):**
   - In `PLATES`, add `"charge_key": MEDIA / "04_Generated-Clips/part04/raw/v01/09_charge_string_c1_t1.mp4"` (`sha256: 611e2633f2ea7f4417272b91af41b857bb6733d416363918a17a111be56f9c80`; or `"09_charge_string_t1.mp4"`, `sha256: e2045b3626ae919e2086f9d3b7254d82fd67a2cc38d5e9673a5812674a1b9061`).
   - In `BEATS`, change row `5` (`t0 = 15.76`) from `(15.76, "key", 4.10)` to `(15.76, "charge_key", 0.60)` (keeping all other 7 rows `s01..s05` and `s07..s08`, timings, `952×1692` 2.35× framing, `NEVER HIT IT` hook caption, `PHILADELPHIA · 1752` overlay at `2.7–6.2 s`, `Why Did Franklin Fly a Kite in a Storm?` title at `9.0–14.0 s`, locked VO `40ed4c4e…`, bed, SFX, and `-14.0 ± 0.5 LUFS` / `<= -1.6 dBTP` loudness calibration identical).
2. **Run and paste all 5 mandatory gates on `hos_008_short_A_v04.mp4`:**
   - `gate_shorts_open.py check` (`--air-date 2026-11-18`) -> must `PASS`.
   - `polish_gate.py` -> must `PASS` (`0` failed rows).
   - `picture_qa.py` -> must `PASS` (`0` failed cuts; `s06` reuse failure eliminated).
   - `music_gate.py` -> must `PASS`.
   - `sfx_kit.py level` -> must `PASS`.
3. **Stage and record `v04` (`£0`, no upload):**
   - Copy `hos_008_short_A_v04.mp4` (with verified SHA-256) to `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/10_Shorts/hos_008_short_A_v04.mp4` and `/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/10_Shorts/hos_008_short_A_v04.mp4` (never commit `.mp4` or `.wav` media to git).
   - Commit the `v04` build script and QA JSON/TXT records in a clean HOS worktree, post the `v04` gate report on HOS Desk `#180`, and block `J0912` with `'parked for Chief: Short PASS'` (which Rule H will route to review / Ben's watch). Never upload or schedule.
