# J2302 Review: 024 Muons Short `fri06_muons_ground` v03 (for J2248)

- **Review Job:** `J2302` (`024 muons v03: review verified UAT repair and detail warning`)
- **Target Job:** `J2248` (`024 muons Short fri06: build from locked VO+graphics, review+Ben watch, then Private schedule (target Mon 9 Nov 11:30 if free)`)
- **Prior Review & Scope Ruling:** `J2283` (`jobs/reviews/J2283/REVIEW.md`, `19cfce9eb0`) · `J2278` (`jobs/reviews/J2278/CHIEF_RULING.md`, `bfb438398c`)
- **Film / Stage:** `OWB:024` (`What Happens If You Travel Near Light Speed?`, `rVqgtkBV3jc`) · `edit`
- **Reviewer:** `gemini` (`gemini-argon` on the Mac mini; `image_input,audio_input,moving_video_input` demonstrated and recorded via `chief_relay.py capabilities` from direct `read_file` inspection of `fri06_muons_ground_v03.mp4`, `code_graphic_024_fri06_muons_v03_scale.mp4`, `picture_qa_v03/picture_qa_review.jpg`, `fri06_muons_ground_v03_contact.jpg`, `fri06_muons_ground_v03_cover.jpg`, and `fri06_muons_ground_v03_cover_preview.jpg`)
- **Date:** `2026-11-07T06:37:00Z`
- **Verdict:** **KEEP** (ordinary Rule-H review PASS; handed off to Ben's required final watch via `jobs.py awaits J2248` — no final publish OK, no upload or schedule before authorization)
- **Spend / Publishing:** £0 / 0 credits. Not uploaded, not scheduled. `Mon 9 Nov 2026 11:30 London` remains occupied by `iyvWYFP_ETA` (*Could a Robot Survive a Night on Mars?*). Next free provisional slot: `Sat 21 Nov 2026 11:30 London` (`2026-11-21T11:30:00Z`), subject to Ben's final watch and slot recheck at upload time.
- **Local Code Handoff Note:** As instructed in `J2302`, Codex's assembly commit `c34a0429d6` on local branch `codex/J2248-v03` (`/private/tmp/codex-J2248-v03`) remains parked locally for Chief authorization without bypassing automatic approval review. All 22 UAT files in `OWB UAT/024_fri06_muons_ground_v03/` are resident on disk and SHA-256 verified against `UAT_v03_SHA256SUMS.json`.

---

## 1. Asset, Hash & Tool-Gate Verification on the Mac mini

### A. File Integrity & SHA-256 Hashes (Independently Verified on Disk)
- **`v03` Master (`fri06_muons_ground_v03.mp4`):**
  - **Paths:** `02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/10_Shorts/fri06_muons_ground/06_Final-Exports/fri06_muons_ground_v03.mp4` and `OWB UAT/024_fri06_muons_ground_v03/fri06_muons_ground_v03.mp4`
  - **SHA-256:** `be63a3d85cadfb4d0fd0387f62dd36dcf9200e5b51942fd91873f1cc677c902c` (`11,071,340` bytes)
  - **Format:** `1080x1920` (9:16), `30 fps` CFR, `22.20 s`, `55` spoken words
- **`v02` Master (preserved intact):**
  - **SHA-256:** `768cf1a4f0ae603724eef13c690e0c9495c233b4ecc5f3af0f3d27b5c39a5f08` (`12,046,470` bytes)
- **`v01` Master (preserved intact):**
  - **SHA-256:** `9fc197dcdbcd16d3812a183779b2c8dcba38f67495d5738741b4c6e8f411fd28` (`27,146,050` bytes)
- **Single Code Graphic (`code_graphic_024_fri06_muons_v03_scale.mp4`):**
  - **SHA-256:** `766ead614c266be9b70eeb0727aae8640d7db7cc5b7ea32295d405dae74bccd3` (`2,005,602` bytes, `3.80 s`)
- **Contact Sheet (`fri06_muons_ground_v03_contact.jpg`):**
  - **SHA-256:** `0aeaeafb99a9db46a13f0b1a35986954c9bd586b1780bfefc08ba86890689758` (`164,437` bytes)
- **Custom Cover (`fri06_muons_ground_v03_cover.jpg`) & Preview (`fri06_muons_ground_v03_cover_preview.jpg`):**
  - **Cover SHA-256:** `57ea85742326a64508085b6a9e1bc275d58dfe7b542366035a2c228daa86ebed` (`280,250` bytes)
  - **Preview SHA-256:** `a02dff5722cb6a2a83ecd3c5e2f111af9f185d905c514ec70a4976e3d8aa704b` (`53,680` bytes)
- **Flagged Review Frame (`picture_qa_v03/picture_qa_review.jpg`):**
  - **SHA-256:** `c6c5cc887cb99da7d4c33e949904d3087103c29d677c5c383792e8ae1dcbe680` (`49,767` bytes)
- **Locked VO (`fri06_muons_ground_vo_v01.mp3` / `/tmp/j2248-vo/vo.mp3`):**
  - **SHA-256:** `3b17b23c8c476efa240375375ffe738fd8dacd254f622f2cef97152089779e8a` (not reminted; stem `stem_vo.wav` `35826bf888c6fa476ec981a4c33e2469bde249f94bf84f0389956e3097e1b828`)
- **Film Score Bed (`light-speed_score_bed_v01_full.mp3`):**
  - **SHA-256:** `7859c2294b05250d24e733d22a971d5356fc6a92056f5fba0bf828035af8673b` (`526.0 s`, sliced from `48.0 s`; stem `stem_bed.wav` `249efa50df3df3bbbd5f90f9d62510a038cc1d313be1dbb923472c05ccfbc7c9`)
- **House SFX Stem (`stem_sfx.wav`):**
  - **SHA-256:** `3315116f10d72d89788b8c0a15799c4e9a3695a7ba60a17353a8fa25339ba753`
- **Source Plates (`£0` local NASA public-domain files):**
  - `Earth_Views_from_the_International_Space_Station.mp4`: `caf71b75b1cd19816c55179384ea41e606d6ecd1088432b1e8e85e566917ce98`
  - `/tmp/j2248-v02/nhq_1740.mp4` (`NHQ_2019_0626_Earth_Views_from_the_ISS.mp4` @ `1740.0 s`, crop `1096:616:88:104`, upscale `0.985x`): `6df94ee00c4b322f3308d1978010cea76ec95fd10ff8887aae920f64f40adbca`
  - `/tmp/j2248-v02/nhq_560.mp4` (`NHQ_2019_0626_Earth_Views_from_the_ISS.mp4` @ `560.0 s`, crop `1096:616:88:104`, upscale `0.985x`): `db0c1cfc8e697221a499ab4c2fc52ee494838b3439b280074e650db7e1be1a82`
- **All 22 UAT Manifest Files (`UAT_v03_SHA256SUMS.json`):** Verified 22/22 matching in `OWB UAT/024_fri06_muons_ground_v03/`.

### B. Automated Gate Outputs (Pasted)
```text
PASS  fri06_muons_ground_v03.mp4  dur=22.2s  audio=-17.8dB  motion=17.25  f0diff=3.94  cut1=3.0s  vo_onset=0.08s  tail_gap=1.03s  vo_src=/tmp/j2248-vo/vo.mp3  dhash=dc7360b603214413  visor=0.0
WARN   0:16 row s05_nhq_b NHQ_2019_0626_Earth_Views_from_the_ISS.mp4: low detail: edge density 0.0328 < film p5 0.0360
picture QA PASS: 0 of 6 cuts fail, 1 to look at -> /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/10_Shorts/fri06_muons_ground/06_Final-Exports/picture_qa_v03/PICTURE_QA.md, /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/10_Shorts/fri06_muons_ground/06_Final-Exports/picture_qa_v03/picture_qa_review.jpg
s01_earth     1.5s Earth_Views_from_the_Interna ok
s02_graphic   4.9s code_graphic_024_fri06_muons ok
s03_nhq_a     8.7s NHQ_2019_0626_Earth_Views_fr ok
s04_earth    12.5s Earth_Views_from_the_Interna ok
s05_nhq_b    16.3s NHQ_2019_0626_Earth_Views_fr WARN low detail: edge density 0.0328 < film p5 0.0360
s06_earth    20.2s Earth_Views_from_the_Interna ok
polish gate PASS: 0 of 6 rows failed, 1 to look at -> /Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/10_Shorts/fri06_muons_ground/06_Final-Exports/polish_gate_v03.json
music gate PASS: light-speed_score_bed_v01_full.mp3, 526.0 s, about 150.0 BPM, brief Pace: 72-88 BPM
SFX level PASS: VO -19.3 LUFS, SFX -42.3 LUFS, 2 hits
Mix loudness: -14.4 LUFS, true peak -1.9 dBTP
```

---

## 2. Direct Multimodal Video, Audio & Image Review (`v03` Repairs & Flagged Frame)

### A. Verification of `J2283` Repairs (`v02` -> `v03`)
1. **Top-Black Limb Feather & Elimination of Double-Horizon / Black-Band Sandwich (`s02_graphic`, `s03_nhq_a`, `s04_earth`, `s05_nhq_b`):**
   - Direct inspection of `fri06_muons_ground_v03.mp4` (`00:03–00:18`), `code_graphic_024_fri06_muons_v03_scale.mp4`, and `fri06_muons_ground_v03_contact.jpg` (`3.4s`, `6.8s`, `9.4s`, `12.8s`, `16.6s`) confirms that blacking out the top half of `[bg]` and applying `feather_limb.png` (`v=255` for `y <= 1030`, linear fade `1030..1240`) completely removes the floating upper ghost horizon (`y = 507..680`) that appeared across all limb shots in `v02`.
   - Every limb shot now presents a single crisp curved Earth horizon against pure black space above (`y = 0..816`) and a smooth bottom feather into the lower Earth fill (`y > 1030`), with zero horizontal split-panel seam on `polish_gate.py`.
2. **Source Continuity, `<= 4.0 s` Graphic Duration, and Elimination of Station Hardware & Jump Cuts:**
   - `s01_earth` (`0.0–3.0 s`, `3.0 s`, `Earth_Views` @ `36.0 s`, upscale `0.84x`): Clean nadir fast cloud pass behind the `0.0–2.4 s` hook (`THEY LIVE`).
   - `s02_graphic` (`3.0–6.8 s`, `3.8 s` `<= 4.0 s`, `code_graphic_024_fri06_muons_v03_scale.mp4`, upscale `1.0x`): Shortened from `4.2 s` to `3.8 s`. Downward-moving cyan/gold cosmic-ray muon streaks enter Earth's upper atmosphere over `Earth_Views` @ `14.0–17.8 s` with a single clean horizon.
   - `s03_nhq_a` (`6.8–10.6 s`, `3.8 s`, `NHQ_2019_0626_Earth_Views_from_the_ISS.mp4` @ `1740.0 s`, crop `1096:616:88:104`, upscale `0.985x`): Cuts to a genuinely distinct ISS camera angle over deep blue ocean and scattered cumulus clouds, eliminating `v02`'s backward jump cut inside the `14–28 s` `Earth_Views` shot.
   - `s04_earth` (`10.6–14.4 s`, `3.8 s`, `Earth_Views` @ `50.0–53.8 s`, crop `1096:616:88:104`, upscale `0.985x`): Because the `71.0 s` and `140.0 s` windows suggested in `J2283` contained station hardware at frame edges, Codex replaced `s04_earth` with a cropped `50.0–53.8 s` bright storm-cloud Earth limb (`0.985x` upscale). Direct video inspection (`00:10–00:14`) confirms zero station hardware, zero mid-row source dissolve, and a clean visual change from `s03_nhq_a`.
   - `s05_nhq_b` (`14.4–18.2 s`, `3.8 s`, `NHQ_2019_0626_Earth_Views_from_the_ISS.mp4` @ `560.0 s`, crop `1096:616:88:104`, upscale `0.985x`): Completely replaces `v02`'s `46.0 s` docked Soyuz spacecraft and solar-array ghost artifact with a clean high-altitude limb pass.
   - `s06_earth` (`18.2–22.2 s`, `4.0 s`, `Earth_Views` @ `60.0–64.0 s`, upscale `0.84x`): Station-free full-frame nadir ocean/cloud pass returning to the opening nadir look for the loop.
3. **Title Placement at `y = 820` Over Earth (`9.0–14.0 s`):**
   - Moving the 3-line exact title (`Muons Shouldn't / Reach the Ground. / They Do.`) down to `y = 820` places it over the bright Earth limb (`00:09–00:13`), eliminating the tool-detected horizontal black gutter between text rows while keeping the white text + black stroke crisp and clear of the lower-third captions (`y = 1430`).

### B. Full-Size Inspection of Flagged Frame `0:16` (`row s05_nhq_b`, `picture_qa_v03/picture_qa_review.jpg`)
- **Flag:** `WARN 0:16 row s05_nhq_b NHQ_2019_0626_Earth_Views_from_the_ISS.mp4: low detail: edge density 0.0328 < film p5 0.0360`.
- **Direct Full-Size Assessment (`picture_qa_v03/picture_qa_review.jpg` + `fri06_muons_ground_v03.mp4` `00:14–00:18`):**
  - Replacing `v02`'s low-detail Soyuz frame (`0.0219`) raised the whole Short's 5th-percentile edge density (`p5`) from `0.0291` to `0.0360`. Row `s05_nhq_b` measures `0.0328` (49.8% higher than `v02`'s `0.0219`, and well above `v02`'s `p5` of `0.0291`) only because the top third of the limb frame is clean black space (`#000000`) and the bottom feather covers soft atmospheric cloud decks.
  - At full size on `picture_qa_v03/picture_qa_review.jpg`, the `0.985x` 16:9 band shows a sharp, natural Earth horizon with a distinct blue atmospheric airglow rim and detailed cloud streaks across the upper hemisphere above the caption `THE GROUND`. There is zero station hardware, zero compression blockiness, and zero double-horizon seam. A viewer would unquestionably trust this as a real, sharp NASA ISS view of Earth's atmosphere as the narrator says *"so they reach the ground."*
  - **Ruling on `0:16` WARN:** **ACCEPT / PASS.**

### C. Audio, Captions, Cover & Inherited Scope Assessment (`J2278` / `J2283`)
1. **Direct Audio & Mix Verification (`audio_input` on `fri06_muons_ground_v03.mp4`):**
   - Narration (`3b17b23c…779e8a`) is crisp, natural British delivery with zero stumbles or repeats (`vo_onset = 0.08 s`, ends `21.17 s`, `1.03 s` tail breath over music before `22.20 s` end).
   - Score bed (`light-speed_score_bed_v01_full.mp3` sliced from `48.0 s`) plays continuously across the full `22.20 s` cut (`-22.2 dB` bed gain) with a clean tail fade.
   - House SFX (`sfx_kit.py level` PASS: VO `-19.3 LUFS`, SFX `-42.3 LUFS`, 2 subtle ink ticks) and integrated loudness (`-14.4 LUFS`, `-1.9 dBTP`) pass all rules.
2. **Reading & Caption Timing (`55` words):**
   - All 55 caption words match `words.json` verbatim (with British `METRES OF FLIGHT` at `9.92–11.32 s`), positioned cleanly at `y = 1430` with no collision against the `0.0–2.4 s` hook (`THEY LIVE`), the `9.0–14.0 s` title (`y = 820`), or the `16.90–21.05 s` end card (`What Happens If You Travel Near Light Speed? rVqgtkBV3jc`).
3. **Cover & Small Preview (`fri06_muons_ground_v03_cover.jpg`, `fri06_muons_ground_v03_cover_preview.jpg`):**
   - Verified directly via `read_file`: `1080x1920` custom cover over the sharp opening nadir cloud frame (`s01_earth`), with `SLOW` in yellow (`#FFE438`) and `CLOCKS` in white (`#FFFFFF`), centered in the 16:9 crop band and legible at mobile preview size (`THUMBNAIL_AND_TITLE_RULES.md` §4).
4. **Explicit Assessment of Inherited Scope Exceptions (`J2278` Acting-Chief Ruling):**
   - **Locked statement title (*"Muons Shouldn't Reach the Ground. They Do."*) and statement line 1 (*"Particles from space are passing through you. They shouldn't get here."*, `"Muons"` first spoken at `4.82 s`):** Governed by `J2248`'s Chief brief (5 Nov 2026) and `J2278` (*"retains the locked title and locked VO, with no remint or new generation"*). Accepted.
   - **`0.68 s` VO pause at `4.14–4.82 s` (and `0.52 s` at `11.32–11.84 s`) not trimmed:** Governed by `J2278` (*"not authority to silently rewrite the script or trim VO"*). Accepted under locked VO hash `3b17b23c…779e8a`.
   - **Payoff *"their clocks run slow"* (`13.02–14.74 s`) overlaps the `9.0–14.0 s` title window:** Fixed by the locked VO timing and mandatory `9–14 s` title window. Accepted under `J2278`.
   - **Spoken end line says *"What Happens If You Travel Near The Speed Of Light?"* while the end card (`16.90–21.05 s`) displays the live long title *"What Happens If You Travel Near Light Speed?"* + `rVqgtkBV3jc`:** Complies with `J2278` (*"show the exact live long title and rVqgtkBV3jc on the end card as required"*). Accepted.
   - **Last plate (`s06_earth`, `18.2–22.2 s`, `Earth_Views` @ `60.0 s`) vs Frame 0 (`s01_earth`, `0.0–3.0 s`, `Earth_Views` @ `36.0 s`):** Returns to the same nadir ocean/cloud pass as Frame 0 while staying `24.0 s` apart (`>= 10 s` rule). Accepted.

---

## 3. Handoff to Ben's Final Watch (`awaits_ben` on `J2248`)

Per `J2302` (*"On KEEP hand off for required Ben final watch via awaits; no upload/schedule before authorization. Mon 9 Nov remains occupied by iyvWYFP_ETA. Preserve v01/v02"*), `J2248` is placed on `awaits_ben` pointing to `OWB UAT/024_fri06_muons_ground_v03/fri06_muons_ground_v03.mp4` (`version: v03`, provisional air slot `2026-11-21 11:30` London, `due: 2026-11-21 10:30` London, `ifNot: do not upload or schedule`), and remains blocked on Ben's final watch before any Private upload or scheduling.
