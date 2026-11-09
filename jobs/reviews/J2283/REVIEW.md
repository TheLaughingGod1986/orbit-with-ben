# J2283 Review: 024 Muons Short `fri06_muons_ground` v02 (for J2248)

- **Review Job:** `J2283` (`024 muons Short v02: review the tool-passed cut`)
- **Target Job:** `J2248` (`024 muons Short fri06: build from locked VO+graphics, review+Ben watch, then Private schedule (target Mon 9 Nov 11:30 if free)`)
- **Acting-Chief Scope Ruling:** `J2278` (`jobs/reviews/J2278/CHIEF_RULING.md`, `bfb438398c`)
- **Film / Stage:** `OWB:024` (`What Happens If You Travel Near Light Speed?`, `rVqgtkBV3jc`) · `edit`
- **Reviewer:** `gemini` (`gemini-argon` on the Mac mini; `image_input,audio_input,moving_video_input` recorded via `chief_relay.py capabilities` from direct `read_file` inspection of `fri06_muons_ground_v02.mp4`, `picture_qa_v02/picture_qa_review.jpg`, `fri06_muons_ground_v02_contact.jpg`, `fri06_muons_ground_v02_cover.jpg`, and `fri06_muons_ground_v02_cover_preview.jpg`)
- **Date:** `2026-11-06T14:49:00Z`
- **Verdict:** **FIX**
- **Spend / Publishing:** £0 / 0 credits. Not uploaded, not scheduled, and no Ben watch card (`awaits_ben`) set. `Mon 9 Nov 2026 11:30 London` remains `iyvWYFP_ETA`.

---

## 1. Asset & Tool-Gate Verification on the Mac mini

### A. File Integrity & Hashes
- **`v02` Cut:** `02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/10_Shorts/fri06_muons_ground/06_Final-Exports/fri06_muons_ground_v02.mp4` (also staged to iCloud `OWB UAT/024_fri06_muons_ground_v02/fri06_muons_ground_v02.mp4`, `12,046,470` bytes)
  - **SHA-256:** `768cf1a4f0ae603724eef13c690e0c9495c233b4ecc5f3af0f3d27b5c39a5f08` (verified on disk)
  - **Format:** `1080x1920`, `30 fps`, `22.2 s`, `55` spoken words
- **`v01` Cut (preserved on disk):** `02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/10_Shorts/fri06_muons_ground/06_Final-Exports/fri06_muons_ground_v01.mp4`
  - **SHA-256:** `9fc197dcdbcd16d3812a183779b2c8dcba38f67495d5738741b4c6e8f411fd28` (verified intact)
- **Locked VO (`fri06_muons_ground_vo_v01.mp3` / `/tmp/j2248-vo/vo.mp3`):** `3b17b23c8c476efa240375375ffe738fd8dacd254f622f2cef97152089779e8a` (not reminted)
- **Film Score Bed (`light-speed_score_bed_v01_full.mp3`):** `7859c2294b05250d24e733d22a971d5356fc6a92056f5fba0bf828035af8673b` (`526.0 s`, sliced from `48.0 s`)
- **NASA Source Plate (`Earth_Views_from_the_International_Space_Station.mp4`):** `caf71b75b1cd19816c55179384ea41e606d6ecd1088432b1e8e85e566917ce98` (`1280x720`, public domain, NASA images library)
- **Single Code Graphic (`code_graphic_024_fri06_muons_v02_scale.mp4`):** `e025b62957584e4688ec623093278c42c100e473f021df1ad83d2c9f27eae334` (`4.2 s`, streaks over `Earth_Views` at `21.6 s`)

### B. Automated Gate Outputs (Pasted)
```text
PASS  fri06_muons_ground_v02.mp4  dur=22.2s  audio=-17.8dB  motion=17.25  f0diff=3.94  cut1=3.0s  vo_onset=0.08s  tail_gap=1.03s  vo_src=/tmp/j2248-vo/vo.mp3  dhash=dc7360b603214413  visor=0.0
WARN   0:17 row s05_earth Earth_Views_from_the_International_Space_Station.mp4: low detail: edge density 0.0219 < film p5 0.0291
picture QA PASS: 0 of 6 cuts fail, 1 to look at -> /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/10_Shorts/fri06_muons_ground/06_Final-Exports/picture_qa_v02/PICTURE_QA.md, /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/10_Shorts/fri06_muons_ground/06_Final-Exports/picture_qa_v02/picture_qa_review.jpg
s01_earth     1.5s Earth_Views_from_the_Interna ok
s02_graphic   5.1s code_graphic_024_fri06_muons ok
s03_earth     9.2s Earth_Views_from_the_Interna ok
s04_earth    13.2s Earth_Views_from_the_Interna ok
s05_earth    16.7s Earth_Views_from_the_Interna WARN low detail: edge density 0.0219 < film p5 0.0291
s06_earth    20.2s Earth_Views_from_the_Interna ok
polish gate PASS: 0 of 6 rows failed, 1 to look at -> /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/10_Shorts/fri06_muons_ground/06_Final-Exports/polish_gate_v02.json
music gate PASS: light-speed_score_bed_v01_full.mp3, 526.0 s, about 150.0 BPM, brief Pace: 72-88 BPM
SFX level PASS: VO -19.3 LUFS, SFX -42.3 LUFS, 2 hits
Mix loudness: -14.4 LUFS, true peak -1.9 dBTP
```

### C. What `v02` Fixed from `J2250` (`v01`)
1. Preserved `fri06_muons_ground_v01.mp4` (`9fc197dc...`) untouched on disk.
2. Replaced the 7/7 procedural cyan-line wall with real NASA ISS Earth footage and reduced code graphics to 1 row (`s02_graphic`), eliminating the `s02_muons` flat vector clock WARN.
3. Removed the redundant `6.55–8.75 s` `TWO MILLIONTHS` text card and fixed the `9.92–11.32 s` caption from US `METERS OF FLIGHT` to British `METRES OF FLIGHT`.
4. Rebuilt `fri06_muons_ground_v02_cover.jpg` and `fri06_muons_ground_v02_cover_preview.jpg` (`SLOW` in yellow, `CLOCKS` in white) over the real opening nadir cloud frame (`s01_earth`, offset `36.0 s`).

---

## 2. Direct Visual & Audio Inspection (`FIX` Findings)

Direct inspection of `fri06_muons_ground_v02.mp4` (`00:00–00:22`), `picture_qa_v02/picture_qa_review.jpg`, and `fri06_muons_ground_v02_contact.jpg` identifies three picture/edit defects that fail visual QA and must be repaired in `v03` at `£0`:

### 1. Verdict on the `0:17` WARN (`s05_earth`, `15.2–18.2 s`, `Earth_Views` offset `46.0–49.0 s`): **FAIL (Viewer Would Not Trust Frame; Contains Docked Soyuz Hardware + Ghost Blur Blob)**
- `J2283` asks the reviewer to judge `0:17` (`row s05_earth`, `Earth_Views` offset `46.0 s`, `edge density 0.0219 < film p5 0.0291`) full size on `picture_qa_v02/picture_qa_review.jpg`.
- Direct inspection of `picture_qa_v02/picture_qa_review.jpg`, `fri06_muons_ground_v02_contact.jpg` (`16.6s`), and video frames `00:15–00:18` shows:
  1. **Station hardware is prominently in frame:** Despite `_assemble_fri06_muons_ground_v02.py`'s docstring (*"Station hardware, the Canadarm, and the limb horizon after 49 s are not used"*) and the `J2283` brief (*"Station and Canadarm are not used"*), offset `46.0–49.0 s` of `Earth_Views_from_the_International_Space_Station.mp4` has a **docked Soyuz spacecraft and solar array** occupying the right third of the 16:9 band (`y ≈ 660..1050`).
  2. **Floating blurred ghost artifact in the upper sky:** Because `portrait_vf()` scales the 16:9 frame by `2.67x` and blurs it (`sigma=18`) into `[bg]`, the Soyuz solar array from the zoomed background appears as a bright blurry grey/white rectangular blob floating in the top black sky (`y ≈ 100..350`) above a black band (`y ≈ 350..850`) and the sharp Soyuz below.
  3. **Washed-out low-detail lower fill (`edge density 0.0219`):** Below the horizon (`y > 1200`), the blurred pale cloud deck has virtually no edge detail, and the end card (`What Happens If You Travel Near Light Speed? rVqgtkBV3jc`, `16.90–21.05 s`) opens directly over this double-Soyuz / low-detail frame (`16.90–18.20 s`).

### 2. Double-Horizon / Black-Band Sandwich Artifact Across All Limb Shots (`s02_graphic` `3.0–7.2 s`, `s03_earth` `7.2–11.2 s`, `s04_earth` `11.2–15.2 s`, `s05_earth` `15.2–18.2 s`)
- In `Earth_Views_from_the_International_Space_Station.mp4` at offsets `14.0 s`, `21.6 s`, `26.0 s`, and `46.0 s`, the top `~26–45%` (`y = 0..190` of `720`) of the 16:9 frame is pitch-black space (`#000000`) and the bottom `~55–74%` is the bright blue/white curved Earth limb.
- `portrait_vf()` places the sharp `0.84x` 16:9 band `[fg]` in the vertical centre (`y = 656..1264`), which puts `[fg]`'s black sky at `y = 656..816` and `[fg]`'s sharp Earth horizon at `y ≈ 816`. Simultaneously, `[bg]` scales the same 16:9 frame by `2.67x` (`3413x1920`) centred vertically, which pushes `[bg]`'s bright blue/white Earth horizon UP to `y ≈ 507`.
- Because `feather_mask()` fades `[fg]` to `alpha = 0` at `y < 680` (`dist >= 280` from `y = 960`), `[bg]`'s bright blurred Earth limb shows through at `y = 507..680`, followed by `[fg]`'s black space at `y = 680..816`, followed by `[fg]`'s sharp Earth horizon at `y = 816`.
- Across `00:03–00:13` (`3.0–15.2 s`, visible in `fri06_muons_ground_v02_contact.jpg` tiles `3.4s`, `6.8s`, `9.4s`, `12.8s`), the viewer sees **two stacked Earth horizons with a horizontal black gap sandwiched between them**. In `s02_graphic` (`3.0–7.2 s`), the cyan muon streaks fall through the upper ghost horizon, cross the black gap, and stop at the lower sharp horizon.

### 3. Same-Shot Jump Cuts Across `3.0–15.2 s` (`s02_graphic` -> `s03_earth` -> `s04_earth`), `4.2 s` Graphic Hold, and Uncut Internal Source Transition at `13.8 s`
- `s02_graphic` (`3.0–7.2 s`, `Earth_Views` offset `21.6–25.8 s`), `s03_earth` (`7.2–11.2 s`, offset `14.0–18.0 s`), and `s04_earth` (`11.2–15.2 s`, offset `26.0–30.0 s`) are all taken from the **same continuous locked-off camera shot** (`14.0–28.0 s` of `Earth_Views_from_the_International_Space_Station.mp4`).
  - At `7.2 s` (`s02_graphic` -> `s03_earth`), the camera angle does not change: the cyan streaks simply disappear and the identical cloud formation jumps backward by `11.8 s` (`25.8 s -> 14.0 s`).
  - At `11.2 s` (`s03_earth` -> `s04_earth`), the identical cloud formation jumps forward by `8.0 s` (`18.0 s -> 26.0 s`).
  - At `~13.8 s` (inside `s04_earth`, corresponding to offset `28.6 s` of `Earth_Views`), the NASA source video itself dissolves/cuts from the limb shot into the `31–38 s` nadir cloud shot (`00:14` in `fri06_muons_ground_v02.mp4`), creating an unscheduled mid-row transition `1.4 s` before `s05_earth` (`15.2 s`).
- In addition, `s02_graphic` runs `4.2 s` (`3.0–7.2 s`), exceeding the `4.0 s` maximum hold (`AGENTS.md` *Teach on screen* / `.cursor/rules/orbit-build-shorts.mdc`: *"Change the picture every 2.5–4 seconds"*).

---

## 3. Explicit Assessment of Inherited Scope (`J2278` Acting-Chief Ruling)

Per `J2278` (`jobs/reviews/J2278/CHIEF_RULING.md`, `bfb438398c`), the reviewer must explicitly assess the inherited scope against the brief and rules:

1. **Locked statement title (*"Muons Shouldn't Reach the Ground. They Do."*) and statement line 1 (*"Particles from space are passing through you. They shouldn't get here."*, `"Muons"` first spoken at `4.82 s`):**
   - **Assessment:** Governed by `J2248`'s Chief brief (5 Nov 2026) and `J2278`'s acting-Chief ruling (*"The explicit Chief-created J2248 brief retains the locked title and locked VO, with no remint or new generation"*). Accepted as an explicit Chief-scoped exception for this 4 Oct / 6 Oct pre-Keeper asset; not a ground for `FIX`.
2. **`0.68 s` VO pause at `4.14–4.82 s` (and `0.52 s` at `11.32–11.84 s`) not trimmed:**
   - **Assessment:** Governed by `J2278` (*"This is a corrective picture build, not authority to silently rewrite the script or trim VO"*). Accepted under the locked VO hash (`3b17b23c…779e8a`).
3. **Payoff *"their clocks run slow"* (`13.02–14.74 s`) overlaps the `9.0–14.0 s` title banner:**
   - **Assessment:** Fixed by the locked VO (`3b17b23c…779e8a`) and the mandatory `9–14 s` title window (`THUMBNAIL_AND_TITLE_RULES.md`). Accepted under `J2278`.
4. **Spoken end line says *"What Happens If You Travel Near The Speed Of Light?"* while the end card (`16.90–21.05 s`) displays the live long title *"What Happens If You Travel Near Light Speed?"* + `rVqgtkBV3jc`:**
   - **Assessment:** Complies with `J2278` (*"show the exact live long title and rVqgtkBV3jc on the end card as required"*). Accepted.
5. **Last plate (`s06_earth`, `18.2–22.2 s`, `Earth_Views` offset `60.0 s`) vs Frame 0 (`s01_earth`, `0.0–3.0 s`, offset `36.0 s`):**
   - **Assessment:** Both are clean full-frame nadir ocean/cloud passes from `Earth_Views_from_the_International_Space_Station.mp4` (`24.0 s` apart, satisfying `picture_qa.py`'s `>=10 s` same-stretch rule while visually returning to the nadir cloud opening for the loop). Accepted.
6. **Streak graphic length (`4.2 s` at `3.0–7.2 s`):**
   - **Assessment:** **Must be shortened to `<= 4.0 s` in `v03` (`FIX`).** The `4.2 s` duration is not required by the locked VO; it was only used so the remaining `15.0 s` (`7.2–22.2 s`) could be covered by 4 stretches of a single source file (`Earth_Views`). Adding the already-staged second NASA ISS source (`NHQ_2019_0626_Earth_Views_from_the_ISS.mp4` in `/tmp/j2248-v02/nhq_1740.mp4` and `nhq_560.mp4`) allows every row to stay `<= 4.0 s` (`3.0–4.0 s` each) while staying well under `picture_qa.py`'s 5-stretch cap.

---

## 4. Exact Repair List for `v03` (`J2248`, £0)

1. **Fix the Limb Feather Filter (`portrait_vf` / `feather_mask`) so Limb Shots Have Zero Double-Horizon and Zero `polish_gate` Seam:**
   - Full-frame nadir shots (`Earth_Views` offsets `31–38 s`, `60–72 s`, `138–146 s`, where `top_dark == 0`) can keep the symmetric `feather_mask()` (`opaque=70, fade=210`).
   - For **limb shots** (`Earth_Views` `14.0–25.0 s` or `50.0–58.0 s`, and `nhq_1740.mp4` / `nhq_560.mp4`), where the top of the 16:9 frame is pitch-black space (`#000000`) and the bottom is bright Earth:
     - Use a limb mask (`feather_limb.png`) that is fully opaque (`v = 255`) from `y = 0` down to `y = mid + 70` (`y <= 1030`), fades linearly from `255` to `0` across `y = 1030..1240`, and is `0` for `y >= 1240`.
     - In `portrait_vf()` for limb shots, black out the top half of `[bg]` (`drawbox=x=0:y=0:w=1080:h=960:color=black:t=fill` after `gblur=sigma=18`) so `[bg]` above `y = 960` is pure black space (`#000000`) matching the top of `[fg]`, while `[bg]` below `y = 960` provides the blurred Earth fill under the `y = 1030..1240` bottom feather.
     - This eliminates both the floating upper ghost horizon (`y = 507..680`) and any `polish_gate.py` horizontal split-panel seam.
2. **Replace `s05_earth` (`46.0 s` Soyuz + Low-Detail WARN) and Eliminate Same-Shot Jump Cuts Across `3.0–18.2 s`:**
   - Keep every row `<= 4.0 s` and cut between genuinely distinct camera angles (no back-to-back rows from the `14–28 s` limb shot, no source clip crossing the `28.6 s` internal transition, and no station hardware at `40–49 s` or `76–136 s`).
   - Verified clean `£0` 6-row schedule (`22.20 s` total) using the files already staged in `/tmp/j2248-v02/`:
     - `s01_earth` (`0.0–3.0 s`, `3.0 s`): `Earth_Views_from_the_International_Space_Station.mp4` offset `36.0 s` (nadir fast cloud pass, symmetric feather).
     - `s02_graphic` (`3.0–6.8 s`, `3.8 s` `<= 4.0 s`): `code_graphic_024_fri06_muons_v03_scale.mp4` — muon streaks over `Earth_Views` offset `14.0–17.8 s` built with the **limb feather** (`top_black=True`, single clean horizon, no ghost limb).
     - `s03_nhq_a` (`6.8–10.6 s`, `3.8 s`): `NHQ_2019_0626_Earth_Views_from_the_ISS.mp4` (`/tmp/j2248-v02/nhq_1740.mp4`, real source offset `1740.0 s`, pre-cropped `1096:616:88:104`, upscale `0.985x`, limb feather `top_black=True`).
     - `s04_earth` (`10.6–14.4 s`, `3.8 s`): `Earth_Views_from_the_International_Space_Station.mp4` offset `71.0 s` (station-free full-frame nadir ocean/clouds, `edge=5.80`, symmetric feather; or offset `51.0 s` bright storm limb with `top_black=True`).
     - `s05_nhq_b` (`14.4–18.2 s`, `3.8 s`): `NHQ_2019_0626_Earth_Views_from_the_ISS.mp4` (`/tmp/j2248-v02/nhq_560.mp4`, real source offset `560.0 s`, pre-cropped `1096:616:88:104`, upscale `0.985x`, limb feather `top_black=True`; or `Earth_Views` offset `140.0 s` station-free nadir clouds, `edge=8.25`, symmetric feather) — completely replacing the `46.0 s` Soyuz / `0:17` low-detail WARN.
     - `s06_earth` (`18.2–22.2 s`, `4.0 s`): `Earth_Views_from_the_International_Space_Station.mp4` offset `60.0 s` (station-free full-frame nadir ocean/clouds returning to the opening look, symmetric feather).
3. **Preserve `v01` and `v02` on Disk, Rerun All 5 Gates on `v03`, and Stage to `OWB UAT`:**
   - Leave `fri06_muons_ground_v01.mp4` (`9fc197dc...`) and `fri06_muons_ground_v02.mp4` (`768cf1a4...`) in place.
   - Export `fri06_muons_ground_v03.mp4`, verify `0` fails and `0` station-hardware / double-horizon WARNs across `gate_shorts_open.py`, `sfx_kit.py level`, `music_gate.py`, `polish_gate.py`, and `picture_qa.py`, copy `v03` and its reports to `OWB UAT/024_fri06_muons_ground_v03/`, and queue the Rule-H `v03` review before setting Ben's watch (`awaits_ben`) or scheduling.
