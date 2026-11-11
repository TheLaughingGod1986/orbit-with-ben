# J2556 — Rule H Review: 24 November 2026 Supermoon Dated-Event Short v01 (`J2478`)

- **Reviewer**: `gemini` (`gemini-argon`)
- **Date**: 2026-11-11
- **Parent Job**: `J2478` (`Supermoon dated-event Short (airs Thu 19 Nov): voice-over, build from free NASA footage, all Shorts gates, park for review`)
- **Deliverable Reviewed**:
  - Cut: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_dated_shorts/2026-11-24_supermoon/from_gemini_wt_J2478/owb_dated_2026_11_24_supermoon_v01.mp4` (`19.60 s`, `1080×1920`, 30 fps, `sha256: 868a1259ddb264e24022b41dbcd82ba63ed4f802d8197bc78d38e6bf5b3481aa`)
  - Branch & Records: `j2478-supermoon-short` (`a0bfd29c0e4ca4e5cc1f99de173381a5bf6cf674`), `02_Video-Projects/_dated_shorts/2026-11-24_supermoon/` (`VO_REPORT.md`, `splice_v02.py`, `assemble_j2478.py`, `cuts.json`, `pool.json`, `11_Upload-Package/PACKAGE_MANIFEST.json`, and QA reports)
  - Plan: `02_Video-Projects/_dated_shorts/2026-11-24_supermoon-two-earths-closer.md` (and `~/_desk/wt-J2478/02_Video-Projects/_dated_shorts/2026-11-24_supermoon-two-earths-closer.md`)
  - Voice (locked by Acting Chief ruling on 2026-11-10 12:45Z, `#6767568128`): `supermoon_2026_11_24_vo_v02` (plan C7 Trim 1, 41 words, spliced from `supermoon_2026_11_24_c7_trim1_vo_v01.wav`, `sha256: 95a24bc9c4b1352f333c121e96d88483afd7688229e037ba9a51958feeb9f385`). Zero new voice takes allowed (`1,072` chars spent across 4 takes vs `~600` cap).
- **Verdict**: **`FIX` — Reopen `J2478` (`£0` / 0 credits, zero new voice takes) to build `owb_dated_2026_11_24_supermoon_v02.mp4` with the 4 exact edit/plan fixes below.**

---

## 1. What Passes (`KEEP` in `v01`)

1. **Voice choice & credit lock (`VO_REPORT.md` & `#6767568128`)**:
   - Follows the Acting Chief's 10 Nov 12:45Z ruling: uses `supermoon_2026_11_24_c7_trim1_vo_v01.wav` (C7 Trim 1, 41 words, preserving the everyday nickel/coffee-bean scale comparison) while marking `supermoon_vo_v03` (Trim 2) as `NOT USED`.
   - `vo_check.py` passes (`0` fails; `18.60 s` VO, `-21.5 LUFS` integrated, `-24.6 dB` mean, `-5.6 dB` peak).
2. **Automated gate baseline & audio stems**:
   - `gate_shorts_open.py check ... --air-date 2026-11-19` passes (`0` fails, full-bleed `9:16` frame 0 verified, `motion_0_1s = 17.61`, `frame0_diff_0_1_5s = 4.76`, `vo_onset_s = 0.082 s`, `first_cut_s = 2.63 s`, `-14.2 LUFS` / `-2.0 dBTP`, zero Orbit at frame 0, `0` near-duplicate opens).
   - `sfx_kit.py level` passes (`VO -21.5 LUFS`, `SFX -38.7 LUFS`, `5` hits, `0` fails).
   - `music_gate.py` passes under `music_gate_j1468_chief_waiver.json` (`owb-standalone-shorts_score_bed_v01.mp3`, full runtime through the loop seam).
   - `short_c37.py` loop metrics pass (`loop_diff_masked = 5.304`, `open_median_step = 5.856`).
3. **Upload Package Draft (`11_Upload-Package/PACKAGE_MANIFEST.json`) & Cover (`supermoon_2026_11_24_cover_v01.jpg`)**:
   - `schedule.publishAt` is `"2026-11-19T11:30:00Z"` (Thu 19 Nov 11:30 London, `leadTimeDays: 5`), `relatedVideoId` is `"2fsQcea-voM"` (*Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone*, OWB `013`), `title` is `"How Close Will the Supermoon Get on November 24?"` (48 chars), `frame0Caption` is `"**TWO EARTHS** CLOSER"`, `coverText` is `"**24,000 KM** / NEARER"`, and description/tags/sources/credits/social fields are complete.

---

## 2. Decisions on the Review Points & Exact `FIX` List for `J2478` (`v02`, `£0` Spend)

### Decision 1 — First-Second Rule (`LEARNINGS.md` Rule 24 & `OWB-2026-11-E1`) and Sentence-1 Timing: **`FIX` (Speed-Up + Micro-Gap Trim in `splice_v02.py`, Zero New Take)**
- **Finding**:
  - In `supermoon_2026_11_24_vo_v02_words.json`, Sentence 1 (*"The Moon swings two Earths closer on November twenty-fourth."*) runs `0.07 – 4.21 s` (`4.14 s` total):
    - `"The"` (`0.07–0.13 s`), `"moon"` (`0.21–0.53 s`), `"swings"` (`0.65–1.05 s`), `"two"` (`1.19–1.37 s`), `"Earths"` (`1.57–1.93 s`), `"closer"` (`2.05–2.53 s`), `"on"` (`2.77–2.87 s`), `"November"` (`2.91–3.33 s`), `"24th."` (`3.57–4.21 s`).
  - Because `"Earths closer"` lands at `1.57 – 2.53 s`, the spoken surprise finishes **`1.03 s` past the `≤ 1.50 s` Rule 24 / E1 bar** (`LEARNINGS.md` Rule 24: *"subject noun + surprise word completed `≤ 1.5 s`"*).
  - Equally important, because Sentence 1 runs until `4.21 s` while Cut 1 (`s01 → s02`) occurs at `2.633 s` (`≤ 2.8 s` gate), the second half of Sentence 1 (*"on November 24th."*, `2.77–4.21 s`) is spoken over `s02` (an Earth crop of Sumatra/Malaysia), and is then followed by a **`0.48 s` pause (`4.21 → 4.69 s`)** before Sentence 2 (*"If Earth were a nickel,"*), breaking `OWB-2026-11-E1` / Rule 7 (*"VO breath `< 0.25 s`"*).
- **Required Fix 1 (in `02_Voiceover/splice_v02.py` → `supermoon_2026_11_24_vo_v02b.wav` or updated `v02` stem for cut `v02`, `£0` spend)**:
  1. From the existing raw take `supermoon_2026_11_24_c7_trim1_vo_v01.wav` (`sha256: 95a24bc9c4b1352f333c121e96d88483afd7688229e037ba9a51958feeb9f385`), tighten the internal room-tone micro-gaps inside Sentence 1 (`1.40→1.60 s`, `1.96→2.08 s`, `2.56→2.80 s`, `3.36→3.60 s` down to `~0.04–0.05 s` each with `10 ms` qsin fades) **and** apply a clean pitch-preserving `atempo` speed-up (`~1.24–1.28×` on the opening phrase `"The Moon swings two Earths closer"`, and `~1.15–1.20×` on `"on November twenty-fourth"`) so that:
     - `"The"` starts at `≤ 0.08 s`;
     - **`"closer"` ends at `≤ 1.50 s`** (strict `LEARNINGS.md` Rule 24 PASS);
     - **`"twenty-fourth"` ends by `~2.45–2.55 s`** (completing Sentence 1 inside `s01` before Cut 1 at `2.63 s`!).
  2. Tighten the post-Sentence-1 breath before *"If Earth were a nickel,"* from `0.48 s` (`4.21 → 4.69 s`) to **`0.16–0.20 s` (`< 0.25 s` per `OWB-2026-11-E1` / Rule 7)**, and tighten the internal pause after *"nickel,"* (`5.89 → 6.25 s`, `0.36 s`) to `~0.14 s`. Keep total cut duration (`VO + 1.00 s loop tail`) inside the **`17.0 – 20.0 s`** dated-Short bar (`~17.5 – 18.2 s`) and re-run `vo_check.py`.

### Decision 2 — Picture-to-Plan & Picture-to-VO Inspection from Stills and Contact Sheet: **`FIX` (3 Visual/Timing Corrections in `assemble_j2478.py`)**
Inspecting `owb_dated_2026_11_24_supermoon_v01_open_sheet.jpg`, `picture_qa_review.jpg`, `cover_thumb_preview.jpg`, and full-frame stills of all 8 rows (`s01`–`s07` + `loop`) against `2026-11-24_supermoon-two-earths-closer.md` §5 and `CHANNEL_AUTHORITY.md` (*"picture matches the words"*) shows three concrete visual defects in `assemble_j2478.py`:

- **Required Fix 2a — Re-time `SHOT_BOUNDS` (`s01`–`s07`) to the actual spoken word timestamps and fix `s02`/`s03`/`s04` framing so picture matches words**:
  1. **`s01` (`0.00 s → Cut 1 at ~2.60–2.65 s`, covering all of Sentence 1 *"The Moon swings two Earths closer on November twenty-fourth."*)**:
     - Sentence 1 now finishes inside `s01` before Cut 1 (`≤ 2.65 s`).
  2. **`s02` (`Cut 1 → Cut 2 at ~4.10–4.30 s ≤ 4.8 s`, covering *"If Earth were a nickel,"*)**:
     - In `v01` (`still_3.6s.jpg`), `s02` zoomed `1.55–1.63×` into Sumatra/Malaysia on `GSFC_20171208_Archive_e002130.jpg` while the voice was still saying *"on November 24th."*
     - Per Plan §5 (`s02`), render the **full Blue Marble Earth disc** (`e_disc_pair`, `612 px` diameter) on the left side of the `16:9` centre band over a graded dark starry space plate (with smooth scale/drift motion, zero text/badge overlay) while the voice says *"If Earth were a nickel,"*.
  3. **`s03` (`Cut 2 → Cut 3 at ~5.80–6.10 s`, covering *"the Moon is a coffee bean."*)**:
     - In `v01` (`still_5.5s.jpg`), `s03` ran during *"If Earth were a nickel,"* and composited `e_disc_pair` + `m_disc_pair` on top of `bg = lro_mover.frame(..., 1.25)` (a giant full-frame LRO Moon disc), putting **two Moons in the same shot** (a small Moon disc floating in front of a giant cratered Moon background).
     - Per Plan §5 (`s03`), cut in at the mid-sentence boundary right before *"the Moon is a coffee bean."* and show the **Blue Marble Earth disc (`612 px`) and LRO Moon disc (`167 px`, true `1 : 3.67` diameter scale) side by side over a graded dark starry space background** (never over a second Moon disc).
  4. **`s04` (`Cut 3 → Cut 4`, covering the first half of Sentence 3 *"Normally thirty Earths fit between us."*)**:
     - In `v01` (`still_7.6s.jpg`), `s04` ran during *"the Moon is a coffee bean."* (`6.25–7.91 s`) and cropped `as14-67-09386.jpg` directly onto **Apollo 14's metal Laser Ranging Retroreflector box on the lunar surface** (with a black Hasselblad reseau crosshair in the middle of the frame and the caption `A COFFEE BEAN.` sitting across the metal Apollo box).
     - Per Plan §5 (`s04`), align `s04` to Sentence 3 (*"Normally thirty Earths fit..."*) and use either the plan's **unlabelled true-scale Earth-to-Moon span render** (using real Blue Marble Earth and LRO Moon discs over graded dark space, zero text/labels) or a clean unlabelled lunar horizon/crater crop free of Apollo hardware and reseau crosshairs.
  5. **`s05` (`TITLE_WINDOW`) vs `s06` (Sentence 4 *"This Supermoon passes three hundred and sixty thousand kilometres up."* + sole `DATA` scale bar)**:
     - In `v01`, `s05` (`8.900–12.167 s`) and `TITLE_WINDOW` (`9.000–12.100 s`) held `1.06 s` past the start of Sentence 4 (`"This"` at `11.11 s`), so the answer sentence started while the Title Banner was still on screen and before `s06` cut in at `12.167 s`.
     - End `s05` and `TITLE_WINDOW` **before Sentence 4 begins** (e.g., if Sentence 4 starts at `~10.8–11.2 s` or if a natural room-tone breath places Sentence 4 at `~11.5–12.2 s`, keep `TITLE_WINDOW` on `s05` cleanly inside `~8.5–11.3 s` / `9.0–12.0 s` so it clears `≥ 0.15 s` before Sentence 4 starts), and cut to `s06` (`plain_frame_7864` + the animated `DATA` scale bar shrinking `384,400 KM (30 EARTHS)` → `360,000 KM (28 EARTHS)` / `TWO EARTHS CLOSER`) at the start of Sentence 4, followed by `s07` (`iss070e062746` twilight limb + rising Moon) at Sentence 5 (*"Look east at sunset, as…"*), and the `1.00 s` forward-loop tail (`loop`).

- **Required Fix 2b — Fix the `s01` low-detail warning (`polish_gate` / `picture_qa` WARN `edge density 0.0584 < film p5 0.0597`)**:
  - In `assemble_j2478.py`, `decode_svs_4k_frames` downscaled `phases_2026_plain_2160p30.mp4` from `3840×2160` to `1920×1080` *before* `plate_at` cropped a `~410×730` window and upscaled it `2.63×` to `1080×1920`.
  - Decode `phases_2026_plain_2160p30.mp4` at native `3840×2160` (or crop in `ffmpeg` directly from the `3840×2160` source where the window is `~820×1460`, only `~1.31×` upscale to `1080×1920`) so `s01` retains full 4K lunar crater sharpness and clears the `polish_gate` / `picture_qa` low-detail warning.

- **Required Fix 2c — Reconcile the plan file (`02_Video-Projects/_dated_shorts/2026-11-24_supermoon-two-earths-closer.md`) and write `_v02` beside `_v01`**:
  - Carry Gemini's complete §3 slot update from `~/_desk/wt-J2478/02_Video-Projects/_dated_shorts/2026-11-24_supermoon-two-earths-closer.md` into `02_Video-Projects/_dated_shorts/2026-11-24_supermoon-two-earths-closer.md` on `j2478-supermoon-short` (updating the schedule bullet list to show `Thu 19 Nov 2026, 11:30 UTC` locked for this Short, `Sat 21 Nov 2026, 11:30 UTC` taken by `024` muons Short v04, `5 days (~123 hours)` lead time, and `At upload / on Thu 19 Nov: 2fsQcea-voM`).
  - Write the rebuilt export as `owb_dated_2026_11_24_supermoon_v02.mp4` (leaving `v01` untouched on the NAS), update `PACKAGE_MANIFEST.json` `"video"` to `owb_dated_2026_11_24_supermoon_v02.mp4`, re-run all Shorts gates (`vo_check`, `sfx_kit.py level`, `music_gate`, `picture_qa`, `polish_gate`, `short_c37`, `gate_shorts_open --air-date 2026-11-19`), copy `v02` + updated records to the NAS (`studio-live/orbit-with-ben/02_Video-Projects/_dated_shorts/2026-11-24_supermoon/`) and branch `j2478-supermoon-short`, and queue the follow-up review job.
