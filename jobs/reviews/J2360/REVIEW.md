# J2360 Review — `034` Short 2: Repair Exact `v03` Lift and Deliver Reviewable No-Spend Plan

- **Job:** `J2360` (`034 Short 2: repair exact v03 lift and deliver reviewable no-spend plan`)
- **Ref:** `J2356` (`jobs/reviews/J2356/REVIEW.md`), `J2352` (`jobs/reviews/J2352/REVIEW.md`), `J2359` (`jobs/reviews/J2359/REVIEW.md`, PR #626 FIX ruling)
- **Worker:** `macbook` (`gemini-argon` covering `cursor-claude-opus-5-5` slot)
- **Date:** `2026-11-07`
- **Deliverable Written on Disk:** [`02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/SHORTS_PLAN_v01.md`](../../../02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/10_Shorts/SHORTS_PLAN_v01.md)

---

## 1. Executive Decision & Status of `J2320`

1. **`J2320` remains HELD (`status: blocked` at step `1/3`, `last_recheck: J2356`).** It does not reopen until:
   - the elected Chief approves `10_Shorts/SHORTS_PLAN_v01.md` (via the dependent Chief plan-decision job queued by `J2360`), **and**
   - `J2361` → `J2362` complete the corrected `034` shot-list approval and release, and the actual reviewed picture, code-graphic, native/composite opener, music (`05_Music/pluto_score_bed_v01.mp3`), and house SFX (`06_Sound-Effects/kit_v01/`) inputs are delivered on disk.
2. **Locked Long Script & VO Preserved with £0 Spend:**
   - `01_Script/pluto_frozen_heart_script_master_v03.md` (`SHA-256: f9852589a7ea9888165c5148c9d60196cb174d7a41104ad442d845f2dbde65cc`)
   - `02_Voiceover/pluto_frozen_heart_vo_v03.wav` (`SHA-256: 2be8030b6c42b673530351014c71bca1a6c31a10af9746539bb2a1ce7dcf7685`, `616.160 s`)
   - `02_Voiceover/stt/pluto_frozen_heart_vo_v03/stt_raw.json` (`SHA-256: af85f3b6fbcb4c0f549f19f0c526fed18f9454bdb9cfa27958ff5a2770d75df7`, `1,183` word tokens)
   - Zero new VO recording, zero ElevenLabs spend, zero Vertex/Veo/Omni spend, zero assembly/upload/schedule change, and zero unapproved speed-up (`1.00×` playback throughout).

---

## 2. Why Both `J2356` Candidate Intervals Failed

| `J2356` Proposal | Word Indices (`stt_raw.json`) | Scribe Words (`55–65` Rule) | Raw Speech Sum (`1.00×`) | Lead + Inter-Sentence Breaths (`<0.25s`) + Loop Tail (`<1.2s`) | Total Runtime (`22–27 s` Rule) | Verdict |
|---|---|---|---|---|---|---|
| **Charon (`S17 + S23 + S24 + S26`)** | `w0296–w0308` + `w0396–w0401` + `w0402–w0411` + `w0448–w0476` | `58` words (`PASS`) | `6.160 + 4.760 + 3.820 + 12.360 = 27.100 s` (untouched spans) | `0.060 s` lead + `0.540 s` breaths + `0.700 s` tail = `1.300 s` | **`28.400 s` (> `27.0 s`)** | **FAIL (Untouched):** Exceeds `27.0 s` before tail. *(See Selection 2C-i below for internal comma-pause silence trimming.)* |
| **Water-Ice Mountains (`S46 + S49 + S50`)** | `w0842–w0856` + `w0882–w0899` + `w0900–w0917` | **`51` words (< `55`)** | `9.300 + 11.660 + 7.620 = 28.580 s` | `0.060 s` lead + `0.400 s` breaths + `0.700 s` tail = `1.160 s` | **`29.740 s` (> `27.0 s`)** | **FAIL:** Under `55` words and over `27.0 s`. |

---

## 3. Compliant `v03` Selections Delivered in `SHORTS_PLAN_v01.md`

Full word-by-word timestamp tables and `OWB-2026-11-E1` shot plans (`Cut 1 = 2.50 s ≤ 2.8 s`, `Cut 2 = 4.60 s ≤ 4.8 s`, later plates `≤ 3.84 s ≤ 4.0 s`, promo title at `9.5–13.5 s`, single Teach overlay at `16.8–21.8 s`, payoff `≥ 70%`, loop tail `< 1.2 s`, zero end card/CTA) are in `10_Shorts/SHORTS_PLAN_v01.md` §4.2–§4.6:

1. **Selection 2A (Recommended Primary — Water-Ice Mountains Whole-Sentence Lift: `S46 + S47 + S48 + S50`):**
   - **Title (`52` chars, `≤ 60`):** `Why Can Towering Mountains Stand on Pluto at −240°C?`
   - **Verbatim Line-1 Question (`S46`, `w0842–w0856`, `441.760–451.060 s`, `9.300 s` raw / `8.820 s` E1-tightened, `15`w):** *"Why can towering mountains stand beside a flowing glacier between -226 and -240 degrees Celsius?"*
   - **Body & Payoff:**
     - `S47` (`w0857–w0863`, `451.960–454.380 s`, `2.420 s`, `7`w): *"Here is the biggest misconception about Pluto."*
     - `S48` (`w0864–w0881`, `455.100–460.660 s`, `5.560 s`, `18`w): *"On Earth, water ice is a soft glacier that melts, and rock is the solid ground beneath it."*
     - `S50` (`w0900–w0917`, `474.000–481.620 s`, `7.620 s`, `18`w): *"Pluto's two to three-kilometer mountains are big blocks of water ice, sometimes coated with frozen gases like methane."*
   - **Word Count:** **`58` Scribe words** (`15 + 7 + 18 + 18 = 58`, inside `55–65`; `64` expanded spoken words).
   - **Total Runtime (`1.00×` speed):** `0.060 s` lead + `24.900 s` speech (`24.420 s` E1-tightened) + `3 × 0.200 s` inter-sentence breaths (`0.600 s`, each `< 0.25 s`) + `0.740 s` loop tail (`< 1.2 s`) = **`26.300 s`** (`25.820 s` E1-tightened; **`22.0–27.0 s` PASS**).
   - **Structural Advantage & Disclosed Trade-off:** `100%` complete sentences with zero internal edits required (`S46–S48` contiguous in master VO; only **1** sentence splice `S48 → S50`); payoff lands at `79.1%–84.0%` of runtime (`≥ 70%` PASS). *Disclosed trade-off:* In locked `v03`, `S46` does not speak the word `"Pluto"` (`"Pluto."` is spoken at the end of `S47` at `w0863`, while `PLUTO'S ICE MOUNTAINS?` is on screen at Frame 0).

2. **Selection 2B (Alternative Whole-Sentence Lift — Charon Double-World: `S17 + S18 + S22 + S24`):**
   - **Title (`58` chars, `≤ 60`):** `Why Did a Secret 19,000 km Away Make Pluto a Double World?`
   - **Verbatim Line-1 Question (`S17`, `w0296–w0308`, `152.460–158.620 s`, `6.160 s` raw / `5.740 s` E1-tightened, `13`w):** *"Why did a secret 19,000 kilometers away turn Pluto into a double world?"*
   - **Body & Payoff:**
     - `S18` (`w0309–w0310`, `159.480–161.160 s`, `1.680 s`, `2`w): *"June 1978."*
     - `S22` (`w0366–w0395`, `192.900–206.700 s`, `13.800 s`, `30`w): *"At 1,214 kilometers across, Charon is about half the size of Pluto, the largest known satellite relative to its parent body in our solar system, often called a double planet."*
     - `S24` (`w0402–w0411`, `213.380–217.200 s`, `3.820 s`, `10`w): *"By comparison, our moon is 20 times farther from Earth."*
   - **Word Count:** **`55` Scribe words** (`13 + 2 + 30 + 10 = 55`, exact floor of `55–65`; `61` expanded spoken words).
   - **Total Runtime (`1.00×` speed):** `0.060 s` lead + `25.460 s` speech (`25.040 s` E1-tightened) + `3 × 0.180 s` inter-sentence breaths (`0.540 s`, each `< 0.25 s`) + `0.680 s` loop tail (`< 1.2 s`) = **`26.740 s`** (`26.320 s` E1-tightened; **`22.0–27.0 s` PASS**).
   - **Infeasibility Proof on Untouched Whole-Sentence Mutual Tidal Lock (`S26`):** Because `S26` (*"In mutual tidal locking..."*) is `29` words and `12.360 s` long, no untouched whole-sentence combination starting with `S17` (`6.160 s`, `13`w) that includes `S26` can reach `≥ 55` words inside `27.0 s` at `1.00×` speed.

3. **Selection 2C (Separately Scoped Charon Mutual Tidal-Lock Alternatives — Requires Chief Scope Approval + Demonstrated `audio_input`):**
   - **Variant 2C-i (4 Whole Sentences `S17 + S23 + S24 + S26` with Internal Comma-Pause Silence Trimming at `1.00×` Speed):** `58` Scribe words (`13 + 6 + 10 + 29`), ending on full sentence period `"Pluto's surface."` (`w0476`). Tightening 5 internal comma silences `≥ 0.420 s` in pure room tone (`155.960–156.420 s`, `214.240–214.660 s`, `237.660–238.080 s`, `242.140–242.740 s`, `244.700–245.180 s`) to `0.14–0.18 s` removes `1.560 s` of dead silence without touching any word (`27.100 → 25.540 s` speech), yielding `0.060 s` lead + `25.540 s` speech + `0.540 s` breaths + `0.660 s` loop tail = **`26.800 s` total runtime** (`26.300 s` if pauses `≥ 0.28 s` are tightened).
   - **Variant 2C-ii (Pause-Bounded Clause Lift `S17 + S22[w0370–w0395] + S26[w0448–w0468]` with Zero Internal Edits):** `60` Scribe words (`13 + 26 + 21`), `24.920 s` speech + `0.060 s` lead + `0.360 s` breaths + `0.720 s` loop tail = **`26.060 s` total runtime**, ending on `w0468` (`"so Charon neither rises nor sets,"` at `244.700 s` before `"hovering over the same spot..."`).

---

## 4. Source Identities, Rights & Missing Native-Moving Opener (Reconciled with `J2359`)

1. **Static Stills Prove Zero Motion:** `PIA19968`, `PIA19966`, `PIA19856`, `PIA19709`, `PIA20732`, `PIA19947`, `PIA20198`, `PIA19948`, and `PIA19952` are public-domain (`NASA/JHUAPL/SwRI`) **static still images** and cannot open `0.0–2.5 s` as a slow push (`≤ 1.10×`).
2. **DEM Computer Reconstructions Excluded (`J2359` Finding #1):** `PIA21863` (*Soaring over Pluto*), `PIA21864` (*Soaring over Charon*), and `File:Pluto-FlyoverAnimation-20150918.webm` (`R38`) are 3D digital-elevation-model reconstructions with 2–3× exaggerated relief and are **banned** under `AGENTS.md` Lesson 7.
3. **Missing Native-Moving Opener & Compliant `£0` Delivery Routes (`SHORTS_PLAN_v01.md` §3.3):**
   - **Opener Route M1-A (Real-Image Sequential Approach Movie `PIA11709`):** Close-in shoreline/mountain landing frames of NASA's `PIA11709` (*A Colorful Landing on Pluto*, >100 real New Horizons photographs without DEM relief exaggeration, verified in `jobs/reviews/J2359/NASA_EVIDENCE.json`), cropped to `≥ 60%` subject and `≤ 30%` sky.
   - **Opener Route M1-B (Fast-Move + Visible-Event Real-Body Composite `code_graphic_034_short2_open.mp4` under `.cursor/rules/orbit-build-shorts.mdc` §60% Rule 1):** Local `£0` render from unannotated NASA stills (`PIA20732` + `PIA19947` for Selection 2A; `PIA19968` Charon + `PIA19948` Pluto limb for Selection 2B/2C) executing a `1.00× → 1.18×` fast camera move in `0.0–1.0 s` **plus** a visible solar-terminator / cryo-haze sweep by `0.5 s` (`frame0_diff_0_1_5s ≥ 1.50`, `motion_0_1s ≥ 10.0`).

---

## 5. Modality Delegation & Coordinated Dependency Chain

- **Modality Capability Declaration (This Session):** This `macbook` planning session inspected text, word-timestamp JSON (`stt_raw.json`), and file hashes only; no `audio_input` listening or `moving_video_input` motion viewing is claimed here.
- **Audio splice acceptance requires demonstrated `audio_input`** on the rendered audio stem (`--requires audio_input`, delegated separately if unavailable).
- **Motion review requires demonstrated `moving_video_input`** on the rendered `.mp4` cut plus `gate_shorts_open.py` PASS (`--requires moving_video_input`, delegated separately if unavailable).
- **Coordinated Next Jobs (No Duplication of `J2361`/`J2362`):**
  1. Queuing **one** dependent `kind: chief` job (`--after J2360 --film 034 --stage script`) for the elected Chief to rule on `SHORTS_PLAN_v01.md` (`Selection 2A` vs `2B` vs `2C-i/ii`, Short 1 `Option 1A` vs `1B`, and Opener Route `M1-A` vs `M1-B`).
  2. Coordinating with existing `J2361` (repair `034` shot list) → `J2362` (Chief re-review and release of `034` picture harvest, code graphics, music bed, and SFX kit).
  3. `J2319` and `J2320` remain `blocked` until both the Chief Shorts plan ruling and `J2362`'s downstream media deliverables are complete on disk.
