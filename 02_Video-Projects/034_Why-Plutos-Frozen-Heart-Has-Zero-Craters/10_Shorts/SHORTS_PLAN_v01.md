# 034 — Pluto Shorts Plan (`SHORTS_PLAN_v01.md`)

- **Film:** `034_Why-Plutos-Frozen-Heart-Has-Zero-Craters`
- **Parent Long Title:** *Why Pluto's Frozen Heart Has Zero Craters* (`41` chars)
- **Plan Job:** `J2360` (`ref: J2356`, reconciled with `J2352` full VO PASS and `J2359` Chief shot-list FIX ruling on PR #626)
- **Locked Parent Script:** `01_Script/pluto_frozen_heart_script_master_v03.md` (`SHA-256: f9852589a7ea9888165c5148c9d60196cb174d7a41104ad442d845f2dbde65cc`, `review:script 95.8/100 PASS`, `gate:episode PASS`, approved in `J2352`)
- **Locked Master VO:** `02_Voiceover/pluto_frozen_heart_vo_v03.wav` (`SHA-256: 2be8030b6c42b673530351014c71bca1a6c31a10af9746539bb2a1ce7dcf7685`, `616.160 s`, `48000 Hz` stereo PCM16, `-19.9 LUFS` integrated, `-23.0 dB` mean, `-3.7 dBTP` true peak; MP3 `SHA-256: 86cfc44247d0c8e7aee535c2fe50edb5038351041008e3f304e82fd84f124456`)
- **Locked Word-Level STT:** `02_Voiceover/stt/pluto_frozen_heart_vo_v03/stt_raw.json` (`SHA-256: af85f3b6fbcb4c0f549f19f0c526fed18f9454bdb9cfa27958ff5a2770d75df7`, `1,183` word tokens, `0` content diffs; `words.srt` `SHA-256: cd4168acc18022c764a13c501c576ad3d84a72f3b1e0944a23ee68a6d79d51b3`)
- **Upstream Shot-List / Media Pipeline Reference:** `J2359` (`jobs/reviews/J2359/REVIEW.md`, FIX ruling on PR #626 `50fa44c23e`) → `J2361` (repair shot-list source, reuse, and finishing defects) → `J2362` (Chief re-review of corrected shot plan and production release)
- **Spend / Publish Posture:** **£0 / $0 no-spend planning deliverable.** Preserves locked `v03` script and master VO with zero ElevenLabs TTS, ElevenLabs Music/SFX, or Vertex/Veo/Omni spend. No assembly, upload, schedule change, or gate waiver is performed by this plan.

---

## 1. Capability & Verification Gate Notice (`J2356` / `J2359` / `J2360` Rulings)

1. **`J2319` (Short 1) and `J2320` (Short 2) remain HELD (`status: blocked`)** until:
   - the elected Chief approves this `SHORTS_PLAN_v01.md` (selecting the approved Short 2 `v03` lift option in §4 and Short 1 Test A option in §5), **AND**
   - `J2361` → `J2362` complete the corrected `034` shot-list approval and release, and the actual reviewed picture, code-graphic, native/composite opener, music (`05_Music/pluto_score_bed_v01.mp3`), and house SFX (`06_Sound-Effects/kit_v01/`) inputs are delivered on disk.
2. **Explicit Modality Delegation Requirement (`audio_input` & `moving_video_input`):**
   - **Audio splice acceptance requires demonstrated `audio_input`:** Word-level timestamps in `stt_raw.json` prove silence boundaries and durations on paper, but cannot substitute for hearing whether a splice across non-adjacent sentences, internal comma-pause trims, or pause-bounded clauses has natural cadence, room-tone continuity, and falling terminal intonation. After the assembler cuts the audio stem from `pluto_frozen_heart_vo_v03.wav`, splice acceptance must be verified by an agent/reviewer with demonstrated `audio_input` capability (`--requires audio_input`, delegated separately if the building worker lacks `audio_input`), prior to Ben's final UAT watch.
   - **Motion and opener acceptance requires demonstrated `moving_video_input`:** Static NASA Photojournal PIA IDs prove zero motion, and DEM flyovers (`PIA21863`, `PIA21864`, `R38` `File:Pluto-FlyoverAnimation-20150918.webm`) are rejected computer reconstructions (`J2359`). After assembly, continuous motion (`0.0–2.8 s` opener motion, `Cut 1 ≤ 2.8 s`, `Cut 2 ≤ 4.8 s`, no hold `> 4.0 s`, no slow still push) must pass `gate_shorts_open.py` and be verified by an agent/reviewer with demonstrated `moving_video_input` capability (`--requires moving_video_input`, delegated separately if unavailable), prior to Ben's final UAT watch.

---

## 2. December 2026 Release Slot Schedule & Long-First Rule

Per `00_Brand/Channel-Setup/VIDEO_BACKLOG.json` and `AGENTS.md`:
- **Never more than one Short a day; never air a Short before its parent long is public.**
- Parent long `034` (*Why Pluto's Frozen Heart Has Zero Craters*) is slotted for **Sunday `2026-12-13 18:00Z`** in `J2319`/`J2320` (or **Sunday `2026-12-20 18:00Z`** if `033` Uranus airs 13 Dec; neither `J2319` nor `J2320` alters any scheduled calendar slot).

| Short Job | Format & Role | Default Air Slot (`J2319` / `J2320`) | Target Runtime & Word Window | Status & Condition |
|---|---|---|---|---|
| **Short 1 (`J2319`)** | **Test A Opening Short** (`SHORTS_TESTS.md`, exempt from `22–27 s` and Keeper 1-question rule until Jan 2027 readout) | **Mon `2026-12-21 11:30Z`** (Path A default, zero reschedule of `UPLOADS.json`) | **`30.0–38.0 s`** (cut cleanly on sentence end) | **Held (`blocked` at `1/3`)** awaiting Chief Short-plan approval + `J2361`/`J2362` media delivery. |
| **Short 2 (`J2320`)** | **Keeper Question Short** (`OWB-2026-11-E1` + `.cursor/rules/orbit-build-shorts.mdc`) | **Wed `2026-12-23 11:30Z`** (Path A default, zero reschedule of `UPLOADS.json`) | **`22.0–27.0 s`** (`55–65` Scribe words, loop tail `< 1.2 s`) | **Held (`blocked` at `1/3`)** awaiting Chief Short-plan approval + `J2361`/`J2362` media delivery. |
| **Reserve Short 3** | **Keeper Question Short (Convection Cells / Zero-Crater Glacier)** | Held in reserve (`2026-12-25 11:30Z` or later only if Chief schedules a 3rd lift) | **`22.0–27.0 s`** (`55–65` Scribe words, loop tail `< 1.2 s`) | Reserve plan only; no build job queued unless requested by Chief. |

---

## 3. True Source Identities, Rights & Missing Native-Moving Opener Audit

A core requirement of `J2360` (and `J2359` Finding #1) is auditing the **true media type and provenance** of every Pluto/Charon candidate asset, rejecting sourced 3D DEM computer reconstructions, and identifying why a **native-moving full-bleed opener is currently missing** on disk.

### 3.1 Static Stills (Prove Zero Native Motion — Prohibited as Slow-Push Openers)

Because New Horizons executed a single `~14 km/s` flyby on 14 July 2015 rather than entering orbit, its high-resolution close-ups of Pluto and Charon are **static LORRI/MVIC still images**. Under `.cursor/rules/orbit-build-shorts.mdc` (`gate_shorts_open.py` Check 5), a static still with a slow push (`≤ 1.10×` over `4–6 s`) counts as a still and **hard-fails** at Frame 0 (`0.0–2.8 s`):

| Identifier (`NASA` / `Wikimedia`) | Native Resolution | True Media Type | Rights / Credit | Permitted Role in `034` Shorts |
|---|---|---|---|---|
| `PIA19968` (*Charon in Enhanced Color*) | `2000×2000` | **Static still image** (`SHA-256` verified clean in `J2353`) | Public Domain (`NASA / JHUAPL / SwRI`) | Mid-Short cut or real-body cutout inside an animated `code_graphic_034_*`; **cannot** open `0.0–2.5 s` as a slow push. |
| `PIA19966` (*Charon and Pluto: Strikingly Different Worlds*) | `3000×3000` | **Static composite still** (wide black gap between disks) | Public Domain (`NASA / JHUAPL / SwRI`) | Real-body source cutout for `code_graphic_034_r22_double_planet_scale.mp4` (`R22`); **cannot** open `0.0–2.5 s` as a slow push. |
| `PIA19856` (*A Binary Planet in Color: True Scale Separation*) | `2526×501` | **Static wide still** | Public Domain (`NASA / JHUAPL / SwRI`) | Mid-Short orbital distance cut (`R18`/`R25`); **cannot** open `0.0–2.5 s` as a slow push. |
| `PIA19709` (*Charon Natural-Colour Globe*) | `1050×794` | **Static still image** | Public Domain (`NASA / JHUAPL / SwRI`) | Mid-Short Charon portrait (`1.36×` in 16:9 band); **cannot** open `0.0–2.5 s` as a slow push. |
| `PIA20732` (*The Jagged Shores of Pluto's Highlands*) | `2690×3412` | **Static still mosaic** | Public Domain (`NASA / JHUAPL / SwRI`) | Mid-Short water-ice mountain cut (`R50`/`R57`) or source texture for fast-move composite; **cannot** open `0.0–2.5 s` as a slow push. |
| `PIA19947` (*Closer Look: Majestic Mountains and Frozen Plains*) | `2055×1321` | **Static oblique still** | Public Domain (`NASA / JHUAPL / SwRI`) | Mid-Short Norgay/Hillary Montes cut (`R49`/`R50`); **cannot** open `0.0–2.5 s` as a slow push. |
| `PIA20198` (*Mountainous Shoreline of Sputnik Planum*) | `2520×2720` | **Static LORRI mosaic still** | Public Domain (`NASA / JHUAPL / SwRI`) | Mid-Short mountain/shoreline plate (`R51`/`R52`); **cannot** open `0.0–2.5 s` as a slow push. |
| `PIA19948` (*Pluto's Majestic Mountains, Frozen Plains and Foggy Hazes*) | `3420×1461` | **Static backlit limb panorama** | Public Domain (`NASA / JHUAPL / SwRI`) | Mid-Short backlit mountain/haze cut (`R58`); **cannot** open `0.0–2.5 s` as a slow push. |
| `PIA19952` (*The Rich Color Variations of Pluto*) | `5000×5000` | **Static full-disk still** | Public Domain (`NASA / JHUAPL / SwRI`) | Used at Frame 0 of standalone Short `gmzaCfJF1gA` (`owb_sa_s7_pluto_heart`); **prohibited at Frame 0 of `034` Long, Short 1, and Short 2** (`gate_shorts_open.py` Check 2). |
| `PIA20291` / `PIA19708` (*Color Image of Pluto* / *Pluto Big Heart in Color*, 13 July 2015) | `1024×1024` | **Static full-disk stills (canonical duplicate exposure per `J2359` Finding #3)** | Public Domain (`NASA / JHUAPL / SwRI`) | Canonical single July 13 LORRI/Ralph exposure (`SHA-256: 76065326...` / `79436741...`); **cannot** open a Short as a slow push. |

### 3.2 Rejected Computer Reconstructions (`J2359` Finding #1 — Banned Under `AGENTS.md` Lesson 7)

In `jobs/reviews/J2359/REVIEW.md` (`NASA_EVIDENCE.json`), the elected Chief explicitly rejected the following assets from `PR #626` because NASA/JPL captions identify them as **3D digital-elevation-model (DEM) computer reconstructions with topographic relief exaggerated 2–3×**:
- **`PIA21863` (*Soaring over Pluto*):** Rejected (`R06`, `R43`). DEM computer reconstruction with 2–3× exaggerated relief (`AGENTS.md` Lesson 7 hard fail). **Prohibited in `034` Shorts.**
- **`PIA21864` (*Soaring over Charon*):** Rejected (`R28` fallback). DEM computer reconstruction with 2–3× exaggerated relief (`AGENTS.md` Lesson 7 hard fail). **Prohibited in `034` Shorts.**
- **`File:Pluto-FlyoverAnimation-20150918.webm` (*New Horizons Pluto DEM Flyover Animation*, `R38`):** Rejected (`J2359` Finding #1). 3D DEM computer flyover render. **Prohibited as a Short opener or cut.**
- **`PIA20589` (*Post-Pluto KBO 1994 JR1*, `R64`):** Rejected (`J2359` Finding #2). Contains an embedded central arrow over severe background noise. **Prohibited.**

### 3.3 Authentic Public-Domain Motion Sources & Resolution of the Missing Native-Moving Opener

| Motion Asset / Route | Provenance & Rights | True Motion Mechanism | Frame-0 Opener Fitness (`0.0–2.5 s`) & Required Action |
|---|---|---|---|
| **1. `PIA11709` Movie (`http://photojournal.jpl.nasa.gov/catalog/PIA11709` / *A Colorful Landing on Pluto*)** | Public Domain (`NASA / JHUAPL / SwRI`, documented in `jobs/reviews/J2359/NASA_EVIDENCE.json` lines 43–49) | **Real-image sequential zoom movie** assembled from `> 100` actual New Horizons approach and close-flyby photographs taken over six weeks in summer 2015 (not a 3D DEM surface model), zooming from distant Pluto+Charon down to a "landing" on the mountainous shoreline of Sputnik Planitia. | **Compliant `£0` Native-Moving Opener Route M1-A (Short 1 & Short 2 Selection 2A):** Trim out the distant dark-space opening seconds and start mid-action (`t_source` where the zoom fills the `1080×608` 16:9 band with Sputnik Planitia's bright shoreline and bordering water-ice mountains: `subject ≥ 60%`, `sky ≤ 30%`, `frame0_diff_0_1_5s ≥ 1.50`, `motion_0_1s ≥ 10.0`, distinct dHash from `gmzaCfJF1gA`). |
| **2. `File:The Pluto System As Seen By New Horizons Spacecraft.webm` (`R03`, `R23`)** | Public Domain (`NASA / JHUAPL / SwRI`, `1920×1080`) | **Real time-series LORRI optical-navigation sequence** showing Pluto and Charon rotating and co-orbiting their shared barycentre during approach. | **Valid mid-Short real-motion cut (`Shot 2` or `Shot 3` in Charon Selection 2B/2C), NOT a raw full-bleed Frame-0 opener:** Raw approach frames have small bright discs in a dark starfield (`subject < 15%`, `sky > 80%`), which fails Frame 0's `≥ 60%` subject / `≤ 30%` sky lock unless composited inside Route M1-B below. |
| **3. `File:New Horizons Extreme Close-Up Of Pluto Surface (No Audio).ogv` (`R05`, `R46`)** | Public Domain (`NASA / JHUAPL / SwRI`, `788×720`, `1.50×` upscale in 16:9 band) | **Official NASA-rendered camera pan across the static LORRI close-approach mosaic strip** (`PIA20198`/`PIA20199`). | **Secondary mid-Short surface sweep only:** Per `J2359` Finding #1 (*"distinguish native motion from pans over stills or renders"*), this file is a continuous pan over a static LORRI mosaic strip rather than time-series spacecraft video. |
| **4. Fast-Move + Visible-Event Real-Body Opener Composite (`code_graphic_034_short2_open.mp4`, Route M1-B)** | Own `£0` local Python/FFmpeg render from unannotated NASA PD stills (`PIA20732` + `PIA19947` for Selection 2A; `PIA19968` Charon + `PIA19948` Pluto limb for Selection 2B/2C) | **Explicitly permitted by `.cursor/rules/orbit-build-shorts.mdc` §60% stayed-to-watch Rule 1:** *"If only a still exists, it needs a fast move (≥15% scale or a clear pan inside 1.0 s) and a visible event by 0.5 s (light sweeping, a shadow moving, particles)."* | **Compliant `£0` Opener Route M1-B (Required for Charon Selection 2B/2C; backup for Selection 2A):** Full-bleed (`≥ 65%` subject, `≤ 25%` lifted `#0a1026` sky, mean luma `≥ 28`) executing an immediate `1.00× → 1.18×` fast lateral/depth move in `0.0–1.0 s` **plus** a visible solar-terminator / cryo-haze particle sweep by `0.5 s` (`frame0_diff_0_1_5s ≥ 1.50`, `motion_0_1s ≥ 10.0`), followed at `Cut 1 ≤ 2.50 s` by a real NASA plate/video cut (never two `CODE` renders back-to-back). |

> **Current Disk Status (`2026-11-07`):** `03_Picture/` and `04_Generated-Clips/` contain zero media files (`J2359` returned PR #626 for repair in `J2361`). Both Opener Route M1-A (`PIA11709` landing movie harvest) and Opener Route M1-B (`code_graphic_034_short2_open.mp4`) are `£0` deliverables that must be produced once `J2362` approves the repaired `034` shot plan and the elected Chief approves this `SHORTS_PLAN_v01.md`.

---

## 4. Short 2 (`J2320`) — Repair of Exact `v03` Lift & Compliant Selections

### 4.1 Why the Earlier `J2320` and `J2356` Candidate Intervals Were Rejected

| Candidate | `stt_raw.json` Word Indices | Scribe Words (`55–65` Rule) | Raw Speech Sum (`1.00×`) | Lead + Breaths (`<0.25s`) + Loop Tail (`<1.2s`) | Total Runtime (`22–27 s` Rule) | Verdict & Reason |
|---|---|---|---|---|---|---|
| **Stale `J2320` Brief Prose** | *(Not in `v03`)* | `59` (unrecorded draft) | — | — | — | **REJECTED:** Quotes pre-`v03` unrecorded text (*"Why does Pluto's largest moon hang frozen..."*). |
| **`J2356` Charon (`S17 + S23 + S24 + S26`)** | `w0296–w0308` + `w0396–w0401` + `w0402–w0411` + `w0448–w0476` | `13 + 6 + 10 + 29 = 58`w (`PASS`) | `6.160 + 4.760 + 3.820 + 12.360 = 27.100 s` (untouched spans) | `0.060 s` lead + `0.540 s` breaths + `0.700 s` tail = `1.300 s` | **`28.400 s` (> `27.0 s`)** | **REJECTED (Untouched):** Exceeds `27.0 s` before tail (`27.100 s` raw). *(See Selection 2C-i below for internal comma-pause tightening.)* |
| **`J2356` Water-Ice (`S46 + S49 + S50`)** | `w0842–w0856` + `w0882–w0899` + `w0900–w0917` | `15 + 18 + 18 = 51`w (**< `55`w**) | `9.300 + 11.660 + 7.620 = 28.580 s` | `0.060 s` lead + `0.400 s` breaths + `0.700 s` tail = `1.160 s` | **`29.740 s` (> `27.0 s`)** | **REJECTED:** Fails both the `55`-word floor (`51`w) and the `27.0 s` ceiling (`28.580 s` raw). |

---

### 4.2 Summary of Repaired, Compliant `v03` Selections for Short 2 (`J2320`)

Exhaustive verification of all `1,183` word tokens in `02_Voiceover/stt/pluto_frozen_heart_vo_v03/stt_raw.json` establishes **two 100%-whole-sentence selections with zero internal sentence edits** (`Selection 2A` and `Selection 2B`) plus **two separately scoped Charon mutual-tidal-lock alternatives** (`Selection 2C-i` and `Selection 2C-ii`), presented for the elected Chief's ruling:

| Option | Subject & Verbatim Line-1 Question | `v03` Sentences (`stt_raw.json` Words) | Scribe Words (`55–65`) | Speech Sum (`1.00×`) | Lead + Breaths (`<0.25s`) + Tail (`<1.2s`) | Total Runtime (`22–27 s`) | Key Trade-Offs for Chief Decision |
|---|---|---|---|---|---|---|---|
| **Selection 2A (Recommended Primary — Whole Sentences)** | **Water-Ice Mountains at −240°C:** *"Why can towering mountains stand beside a flowing glacier between -226 and -240 degrees Celsius?"* | `S46` (`w0842–w0856`) + `S47` (`w0857–w0863`) + `S48` (`w0864–w0881`) + `S50` (`w0900–w0917`) | **`58` words** (`64` spoken) — **PASS** | `24.900 s` raw (`24.420 s` if 2 internal pauses in `S46` tightened to `0.14 s`) | `0.060 s` lead + `3 × 0.200 s` (`0.600 s`) + `0.740 s` tail | **`26.300 s`** (`25.820 s` E1-tightened) — **PASS** | **100% complete sentences; only 1 splice (`S48 → S50`).** Payoff at `80.2%` runtime. *Note:* `"Pluto."` is spoken in `S47` (`w0863`), while `PLUTO` is on screen at Frame 0 (`PLUTO'S ICE MOUNTAINS?`). |
| **Selection 2B (Alternative — Whole Sentences)** | **Charon Double World:** *"Why did a secret 19,000 kilometers away turn Pluto into a double world?"* | `S17` (`w0296–w0308`) + `S18` (`w0309–w0310`) + `S22` (`w0366–w0395`) + `S24` (`w0402–w0411`) | **`55` words** (`61` spoken) — **PASS** | `25.460 s` raw (`25.040 s` if 2 internal pauses in `S17` tightened to `0.12 s`) | `0.060 s` lead + `3 × 0.180 s` (`0.540 s`) + `0.680 s` tail | **`26.740 s`** (`26.320 s` E1-tightened) — **PASS** | **100% complete sentences; names `"Pluto"` in Sentence 1 (`w0304`).** Directly answers `"double world"` (`1,214 km`, `1/2` Pluto, `20×` closer than Moon). Omits `S26` (`12.360 s`) because untouched whole sentences with `S17 + S26` exceed `27.0 s`. |
| **Selection 2C-i (Separately Scoped — 4 Whole Sentences + Internal Pause Trim)** | **Charon Double World + Tidal Lock:** *"Why did a secret 19,000 kilometers away turn Pluto into a double world?"* | `S17` (`w0296–w0308`) + `S23` (`w0396–w0401`) + `S24` (`w0402–w0411`) + `S26` (`w0448–w0476`) | **`58` words** (`62` spoken) — **PASS** | `25.540 s` (tightening 5 internal comma pauses `≥0.42 s` in pure silence by `1.560 s` at `1.00×` speed) | `0.060 s` lead + `3 × 0.180 s` (`0.540 s`) + `0.660 s` tail | **`26.800 s`** (`26.300 s` if pauses `≥0.28 s` trimmed) — **PASS** | **100% complete sentences ending on `"Pluto's surface."` (`w0476`)**, keeping the full tidal-lock payoff. Requires Chief approval of internal comma-pause silence trimming + `audio_input` verification. |
| **Selection 2C-ii (Separately Scoped — Pause-Bounded Clause Lift)** | **Charon Double World + Tidal Lock:** *"Why did a secret 19,000 kilometers away turn Pluto into a double world?"* | `S17` (`w0296–w0308`) + `S22_clause` (`w0370–w0395`) + `S26_clause` (`w0448–w0468`) | **`60` words** (`64` spoken) — **PASS** | `24.920 s` (zero internal edits within clauses) | `0.060 s` lead + `2 × 0.180 s` (`0.360 s`) + `0.720 s` tail | **`26.060 s`** — **PASS** | Uses `≥0.480 s` silence gaps to include `"so Charon neither rises nor sets,"` (`w0468`), **but** ends on a comma boundary before `"hovering over..."` — requires Chief scope approval + `audio_input` cadence sign-off. |

---

### 4.3 Detailed Specification — Selection 2A (Recommended Primary: Water-Ice Mountains Whole-Sentence Lift)

- **Job ID:** `J2320`
- **Format:** Keeper Question Short (`22–27 s` target, `55–65` words, one question in title and Line 1, `OWB-2026-11-E1` pacing locks)
- **Title (`52` chars, `≤ 60`):** `Why Can Towering Mountains Stand on Pluto at −240°C?`
  - *Alternative matching title (`52` chars):* `Why Can Towering Water-Ice Mountains Stand on Pluto?`
- **Frame-0 Hook Caption (`0.00–2.50 s`, 3 words, `8–10%` cap height):** `PLUTO'S **ICE** MOUNTAINS?` (yellow word `ICE`)
- **Promoted Long Exact Listing Title Banner (`9.50–13.50 s`, during `S47`–`S48`):** `Why Pluto's Frozen Heart Has Zero Craters`
- **Single Teach Overlay (`18.20–21.80 s`, during `S50`, clear of `0–2.5 s` and `9.5–13.5 s`, inside 16:9 centre band, `11–12%` height):** `2–3 KM WATER-ICE PEAKS` (`4` words)
- **Loop Ending (`25.56–26.30 s`, `0.740 s < 1.2 s` loop tail, zero end card or CTA per `OWB-2026-11-E1`):**
  - Final shot (`22.50–26.30 s`) returns to the opening mountain shoreline framing (`crossfade ≤ 0.3 s` at the seam, music bed continuous through the loop point, zero end card or spoken CTA) so the final words (*"...blocks of water ice, sometimes coated with frozen gases like methane."*) loop directly back into Line 1 (*"Why can towering mountains stand beside a flowing glacier between -226 and -240 degrees Celsius?"*).

#### Exact Verbatim `v03` Word Timestamps — Selection 2A (`S46 + S47 + S48 + S50`)

| Segment | `v03` Sentence | Word Index Range (`stt_raw.json`) | Master WAV Start (`s`) | Master WAV End (`s`) | Speech Duration (`s`) | Scribe Words | Natural Pre / Post Silence in WAV | Verbatim Spoken Text (`pluto_frozen_heart_vo_v03.wav`) |
|---|---|---|---|---|---|---|---|---|
| **Lead-in** | Room tone | Before `w0842` | `441.700` | `441.760` | `0.060` | — | `1.100 s` pre-gap (`440.660–441.760 s`) | *(clean room-tone lead; `first_word = 0.060 s ≤ 0.15 s`)* |
| **Seg 1 (Line 1 Question)** | `S46` | `w0842–w0856` | `441.760` | `451.060` | `9.300` (`8.820` E1-trimmed) | `15` | Pre: `1.100 s` / Post: `0.900 s` | *"Why can towering mountains stand beside a flowing glacier between -226 and -240 degrees Celsius?"* |
| **Breath 1** | Tightened natural pause | `S46 → S47` | `451.060` | `451.260` | `0.200` | — | Trimmed from `0.900 s` (`451.060–451.960 s`) | *(natural inter-sentence breath `< 0.25 s`)* |
| **Seg 2** | `S47` | `w0857–w0863` | `451.960` | `454.380` | `2.420` | `7` | Pre: `0.900 s` / Post: `0.720 s` | *"Here is the biggest misconception about Pluto."* |
| **Breath 2** | Tightened natural pause | `S47 → S48` | `454.380` | `454.580` | `0.200` | — | Trimmed from `0.720 s` (`454.380–455.100 s`) | *(natural inter-sentence breath `< 0.25 s`)* |
| **Seg 3** | `S48` | `w0864–w0881` | `455.100` | `460.660` | `5.560` | `18` | Pre: `0.720 s` / Post: `0.720 s` | *"On Earth, water ice is a soft glacier that melts, and rock is the solid ground beneath it."* |
| **Breath 3 (Splice)** | Sentence boundary splice (`S48 → S50`, skipping `S49`) | Pre-`w0900` silence | `473.800` | `474.000` | `0.200` | — | Inside `0.960 s` silence (`473.040–474.000 s`) | *(15 ms equal-power crossfade inside clean silence `< 0.25 s`)* |
| **Seg 4 (Payoff)** | `S50` | `w0900–w0917` | `474.000` | `481.620` | `7.620` | `18` | Pre: `0.960 s` / Post: `1.000 s` | *"Pluto's two to three-kilometer mountains are big blocks of water ice, sometimes coated with frozen gases like methane."* |
| **Loop Tail** | Post-`S50` room tone + music ring-out | After `w0917` | `481.620` | `482.360` | `0.740` | — | Inside `1.000 s` post-gap (`481.620–482.620 s`) | *(hold matched opening framing + music bed `0.740 s < 1.2 s`)* |
| **TOTAL** | **4 whole sentences** | **58 Scribe words** (`64` spoken) | — | — | **`24.900 s` speech** (`24.420 s` E1) | **`58` words** | **`0.060 s` lead + `0.600 s` breaths + `0.740 s` tail** | **`26.300 s` total runtime (`25.820 s` E1-trimmed; `22.0–27.0 s` PASS)** |

#### Per-Word Timestamp Verification Table — Selection 2A (`stt_raw.json`)

- **`S46` (`w0842–w0856`, `441.760–451.060 s`, `15` words):**
  `w0842` Why (`441.760–442.000`) · `w0843` can (`442.040–442.200`) · `w0844` towering (`442.280–442.640`) · `w0845` mountains (`442.720–443.260`) · `w0846` stand (`443.320–443.620`) · `w0847` beside (`443.640–444.020`) · `w0848` a (`444.060–444.140`) · `w0849` flowing (`444.180–444.500`) · `w0850` glacier (`444.580–445.080`) · `w0851` between (`445.440–445.820`) · `w0852` -226 (`445.840–447.860`) · `w0853` and (`448.260–448.360`) · `w0854` -240 (`448.420–449.940`) · `w0855` degrees (`450.000–450.340`) · `w0856` Celsius? (`450.400–451.060`)
  *(Note on `OWB-2026-11-E1` internal sentence-1 pauses: `w0850→w0851` has a `0.360 s` silence gap `445.080–445.440 s`, and `w0852→w0853` has a `0.400 s` silence gap `447.860–448.260 s`. If tightened to `0.140 s` each in room tone per E1, `S46` runs `8.820 s` and total runtime is `25.820 s`; if kept untouched, `S46` runs `9.300 s` and total runtime is `26.300 s`.)*
- **`S47` (`w0857–w0863`, `451.960–454.380 s`, `7` words):**
  `w0857` Here (`451.960–452.120`) · `w0858` is (`452.180–452.320`) · `w0859` the (`452.360–452.440`) · `w0860` biggest (`452.460–452.720`) · `w0861` misconception (`452.800–453.540`) · `w0862` about (`453.600–453.840`) · `w0863` Pluto. (`453.880–454.380`)
- **`S48` (`w0864–w0881`, `455.100–460.660 s`, `18` words):**
  `w0864` On (`455.100–455.200`) · `w0865` Earth, (`455.260–455.580`) · `w0866` water (`455.700–456.020`) · `w0867` ice (`456.100–456.340`) · `w0868` is (`456.400–456.500`) · `w0869` a (`456.560–456.620`) · `w0870` soft (`456.660–456.880`) · `w0871` glacier (`456.960–457.420`) · `w0872` that (`457.480–457.620`) · `w0873` melts, (`457.680–458.100`) · `w0874` and (`458.540–458.660`) · `w0875` rock (`458.760–459.020`) · `w0876` is (`459.080–459.200`) · `w0877` the (`459.240–459.320`) · `w0878` solid (`459.380–459.620`) · `w0879` ground (`459.680–459.980`) · `w0880` beneath (`460.060–460.420`) · `w0881` it. (`460.500–460.660`)
- **`S50` (`w0900–w0917`, `474.000–481.620 s`, `18` words):**
  `w0900` Pluto's (`474.000–474.600`) · `w0901` two (`474.660–474.860`) · `w0902` to (`474.900–474.980`) · `w0903` three-kilometer (`475.020–475.740`) · `w0904` mountains (`475.780–476.340`) · `w0905` are (`476.380–476.520`) · `w0906` big (`476.560–476.720`) · `w0907` blocks (`476.860–477.220`) · `w0908` of (`477.280–477.400`) · `w0909` water (`477.440–477.780`) · `w0910` ice, (`477.880–478.140`) · `w0911` sometimes (`478.680–479.160`) · `w0912` coated (`479.200–479.620`) · `w0913` with (`479.660–479.800`) · `w0914` frozen (`479.820–480.160`) · `w0915` gases (`480.260–480.780`) · `w0916` like (`480.840–481.020`) · `w0917` methane. (`481.080–481.620`)

#### `OWB-2026-11-E1` Visual & Motion Plan — Selection 2A (`26.300 s`, 8 Cuts, `Cut 1 = 2.50 s ≤ 2.8 s`, `Cut 2 = 4.60 s ≤ 4.8 s`, Max Hold `3.80 s ≤ 4.0 s`)

| Shot | Short Time (`s`) | Duration (`s`) | Non-DEM Visual Asset & Motion Source (`J2359` Compliant) | On-Screen Text / Overlay (`16:9` Band) |
|---|---|---|---|---|
| **1 (Opener)** | `0.00–2.50` | `2.50` (`Cut 1 = 2.50 s ≤ 2.8 s`) | **Opener Route M1-A or M1-B:** Close-approach Sputnik Planitia shoreline/mountain landing sequence from NASA's real-image video `PIA11709` (*A Colorful Landing on Pluto*, >100 real New Horizons approach photos, zero DEM exaggeration) **OR** fast-move composite `code_graphic_034_short2_open.mp4` over graded `PIA20732` (`1.00× → 1.18×` in `1.0 s` + solar terminator sweep by `0.5 s`; `subject ≥ 65%`, `sky ≤ 25%`, `frame0_diff_0_1_5s ≥ 1.50`, `motion_0_1s ≥ 10.0`). | `0.00–2.50 s`: Frame-0 hook caption `PLUTO'S **ICE** MOUNTAINS?` + `whoosh_soft.wav` at `0.00 s` |
| **2** | `2.50–4.60` | `2.10` (`Cut 2 = 4.60 s ≤ 4.8 s`) | **Graded real New Horizons oblique plate with active lateral move:** `PIA19947` (*Closer Look: Majestic Mountains and Frozen Plains*, `2055×1321`, NASA/JHUAPL/SwRI PD) panning across the boundary between towering Norgay Montes peaks and smooth flowing Sputnik Planitia glacier. | Captions only (`"...stand beside a flowing glacier..."`) |
| **3** | `4.60–8.30` | `3.70` (`≤ 4.0 s`) | **Animated cryogenic thermometer code graphic over graded NASA plate:** `code_graphic_034_r51_water_bedrock_phase.mp4` (Phase 1, over colour-graded `PIA20198` *Mountainous Shoreline of Sputnik Planum*, `2520×2720`), animating the thermometer drop to `−226 TO −240 °C` as VO speaks `"between -226 and -240 degrees Celsius?"` | Animated graphic gauge (`−226 TO −240 °C`, `≤ 4` words) |
| **4** | `8.30–11.98` | `3.68` (`≤ 4.0 s`) | **Real New Horizons LORRI surface sweep (`R46`):** `File:New Horizons Extreme Close-Up Of Pluto Surface (No Audio).ogv` (`788×720`, `1.50×` in 16:9 band) + graded `PIA19954` (*Ice Mountains and Plains*, `1083×1007`) as VO transitions (`0.200 s` breath at `9.36–9.56 s`) into `S47` (*"Here is the biggest misconception about Pluto."*). | `9.50–13.50 s`: Exact parent long listing title banner `Why Pluto's Frozen Heart Has Zero Craters` |
| **5** | `11.98–15.74` | `3.76` (`≤ 4.0 s`) | **Graded NASA Earth vs Pluto comparison plate:** Real `PIA18033` Earth glacier/mountain margin transitioning across `PIA19842` (*Mountainous Shoreline of Sputnik Planum*, `1041×1039`) as VO speaks `S48` (*"On Earth, water ice is a soft glacier that melts..."*). | `9.50–13.50 s` promo title clears at `13.50 s` |
| **6** | `15.74–19.20` | `3.46` (`≤ 4.0 s`) | **Animated structural rigidity graphic over graded NASA plate:** `code_graphic_034_r51_water_bedrock_phase.mp4` (Phase 3, over colour-graded `PIA20198`), locking `WATER-ICE BEDROCK` as `S48` finishes (`"...solid ground beneath it."`) and `S50` begins (`"Pluto's two to three-kilometer mountains..."`). | `18.20–21.80 s`: Single Short Teach overlay `2–3 KM WATER-ICE PEAKS` (`4` words, `11–12%` of 16:9 band height) + `tick_ink.wav` |
| **7 (Payoff)** | `19.20–22.80` | `3.60` (`≤ 4.0 s`) | **Graded real New Horizons high-resolution mountain plate:** `PIA20732` (*The Jagged Shores of Pluto's Highlands*, `2690×3412`, reddish methane-frosted water-ice peaks) as the payoff (`"are big blocks of water ice"`, `20.80–22.08 s` = **`79.1%–84.0%` of runtime, `≥ 70%` PASS**) lands. | `18.20–21.80 s` single Teach overlay clears at `21.80 s` |
| **8 (Loop Seam)** | `22.80–26.30` | `3.50` (`≤ 4.0 s`) | **Backlit horizon sweep returning to matched Shot-1 framing (`PIA19948` *Pluto's Majestic Mountains, Frozen Plains and Foggy Hazes* → `0.25 s` crossfade into Shot-1 opening frame):** Spoken VO ends on `"methane."` at `25.560 s`, followed by `0.740 s` loop tail (`< 1.2 s`) with continuous music bed and **zero end card or CTA**. | Captions only (`"...coated with frozen gases like methane."`); **zero end card** |

---

### 4.4 Detailed Specification — Selection 2B (Alternative Whole-Sentence Lift: Charon Double-World)

If the elected Chief prefers the **Charon / Double-World** topic for Short 2 while keeping **100% whole sentences with zero internal sentence edits**:

- **Title (`58` chars, `≤ 60`):** `Why Did a Secret 19,000 km Away Make Pluto a Double World?`
  - *Alternative matching title (`53` chars):* `Why Did a Secret Moon Turn Pluto Into a Double World?`
- **Frame-0 Hook Caption (`0.00–2.50 s`, 3 words):** `PLUTO'S **DOUBLE** WORLD?` (yellow word `DOUBLE`)
- **Promoted Long Exact Listing Title Banner (`9.50–13.50 s`):** `Why Pluto's Frozen Heart Has Zero Craters`
- **Single Teach Overlay (`16.80–20.40 s`, inside 16:9 band, `11–12%` height):** `CHARON: 1,214 KM WIDE` (`4` words)
- **Payoff Timing (`≥ 70%` Rule):** `"often called a double planet"` (`w0391–w0395`) lands at `20.22–22.18 s` (`75.6%–82.9%` of `26.740 s` runtime, **`≥ 70%` PASS**), followed by the `S24` scale kicker (*"By comparison, our moon is 20 times farther from Earth."*, `22.36–26.06 s`) and `0.680 s` loop tail (`< 1.2 s`, zero end card).

#### Exact Verbatim `v03` Word Timestamps — Selection 2B (`S17 + S18 + S22 + S24`)

| Segment | `v03` Sentence | Word Index Range (`stt_raw.json`) | Master WAV Start (`s`) | Master WAV End (`s`) | Speech Duration (`s`) | Scribe Words | Natural Pre / Post Silence in WAV | Verbatim Spoken Text (`pluto_frozen_heart_vo_v03.wav`) |
|---|---|---|---|---|---|---|---|---|
| **Lead-in** | Room tone | Before `w0296` | `152.400` | `152.460` | `0.060` | — | `0.980 s` pre-gap (`151.480–152.460 s`) | *(clean room-tone lead; `first_word = 0.060 s ≤ 0.15 s`)* |
| **Seg 1 (Line 1 Question)** | `S17` | `w0296–w0308` | `152.460` | `158.620` | `6.160` (`5.740` E1-trimmed) | `13` | Pre: `0.980 s` / Post: `0.860 s` | *"Why did a secret 19,000 kilometers away turn Pluto into a double world?"* |
| **Breath 1** | Tightened natural pause | `S17 → S18` | `158.620` | `158.800` | `0.180` | — | Trimmed from `0.860 s` (`158.620–159.480 s`) | *(natural inter-sentence breath `< 0.25 s`)* |
| **Seg 2** | `S18` | `w0309–w0310` | `159.480` | `161.160` | `1.680` | `2` | Pre: `0.860 s` / Post: `0.620 s` | *"June 1978."* |
| **Breath 2 (Splice)** | Sentence boundary splice (`S18 → S22`) | Pre-`w0366` silence | `192.720` | `192.900` | `0.180` | — | Inside `0.940 s` silence (`191.960–192.900 s`) | *(15 ms equal-power crossfade `< 0.25 s`)* |
| **Seg 3** | `S22` | `w0366–w0395` | `192.900` | `206.700` | `13.800` | `30` | Pre: `0.940 s` / Post: `1.260 s` | *"At 1,214 kilometers across, Charon is about half the size of Pluto, the largest known satellite relative to its parent body in our solar system, often called a double planet."* |
| **Breath 3 (Splice)** | Sentence boundary splice (`S22 → S24`, skipping `S23`) | Pre-`w0402` silence | `213.200` | `213.380` | `0.180` | — | Inside `0.660 s` silence (`212.720–213.380 s`) | *(15 ms equal-power crossfade `< 0.25 s`)* |
| **Seg 4 (Payoff Kicker)** | `S24` | `w0402–w0411` | `213.380` | `217.200` | `3.820` | `10` | Pre: `0.660 s` / Post: `0.860 s` | *"By comparison, our moon is 20 times farther from Earth."* |
| **Loop Tail** | Post-`S24` room tone + music ring-out | After `w0411` | `217.200` | `217.880` | `0.680` | — | Inside `0.860 s` post-gap (`217.200–218.060 s`) | *(hold matched opening framing + music bed `0.680 s < 1.2 s`)* |
| **TOTAL** | **4 whole sentences** | **55 Scribe words** (`61` spoken) | — | — | **`25.460 s` speech** (`25.040 s` E1) | **`55` words** | **`0.060 s` lead + `0.540 s` breaths + `0.680 s` tail** | **`26.740 s` total runtime (`26.320 s` E1-trimmed; `22.0–27.0 s` PASS)** |

#### Per-Word Timestamp Verification Table — Selection 2B (`stt_raw.json`)

- **`S17` (`w0296–w0308`, `152.460–158.620 s`, `13` words):**
  `w0296` Why (`152.460–152.720`) · `w0297` did (`152.760–153.020`) · `w0298` a (`153.120–153.200`) · `w0299` secret (`153.280–153.820`) · `w0300` 19,000 (`154.020–155.060`) · `w0301` kilometers (`155.160–155.580`) · `w0302` away (`155.640–155.960`) · `w0303` turn (`156.420–156.600`) · `w0304` Pluto (`156.680–157.200`) · `w0305` into (`157.340–157.540`) · `w0306` a (`157.600–157.740`) · `w0307` double (`157.780–158.060`) · `w0308` world? (`158.160–158.620`)
  *(Note on `OWB-2026-11-E1` internal sentence-1 pauses: `w0299→w0300` has a `0.200 s` gap `153.820–154.020 s`, and `w0302→w0303` has a `0.460 s` gap `155.960–156.420 s`. Tightening both to `0.120 s` in room tone reduces `S17` to `5.740 s` and total runtime to `26.320 s`.)*
- **`S18` (`w0309–w0310`, `159.480–161.160 s`, `2` words):**
  `w0309` June (`159.480–159.840`) · `w0310` 1978. (`159.940–161.160`)
- **`S22` (`w0366–w0395`, `192.900–206.700 s`, `30` words):**
  `w0366` At (`192.900–193.060`) · `w0367` 1,214 (`193.260–194.960`) · `w0368` kilometers (`195.000–195.400`) · `w0369` across, (`195.460–196.020`) · `w0370` Charon (`196.540–197.020`) · `w0371` is (`197.160–197.240`) · `w0372` about (`197.320–197.600`) · `w0373` half (`197.680–197.960`) · `w0374` the (`198.000–198.100`) · `w0375` size (`198.140–198.380`) · `w0376` of (`198.420–198.520`) · `w0377` Pluto, (`198.560–199.040`) · `w0378` the (`199.700–199.800`) · `w0379` largest (`199.860–200.260`) · `w0380` known (`200.340–200.560`) · `w0381` satellite (`200.680–201.240`) · `w0382` relative (`201.340–201.720`) · `w0383` to (`201.760–201.840`) · `w0384` its (`201.860–202.020`) · `w0385` parent (`202.080–202.480`) · `w0386` body (`202.500–202.840`) · `w0387` in (`203.180–203.260`) · `w0388` our (`203.300–203.420`) · `w0389` solar (`203.480–203.720`) · `w0390` system, (`203.800–204.220`) · `w0391` often (`204.740–205.040`) · `w0392` called (`205.160–205.520`) · `w0393` a (`205.700–205.800`) · `w0394` double (`205.840–206.080`) · `w0395` planet. (`206.180–206.700`)
- **`S24` (`w0402–w0411`, `213.380–217.200 s`, `10` words):**
  `w0402` By (`213.380–213.500`) · `w0403` comparison, (`213.520–214.240`) · `w0404` our (`214.660–214.780`) · `w0405` moon (`214.860–215.100`) · `w0406` is (`215.160–215.300`) · `w0407` 20 (`215.500–215.720`) · `w0408` times (`215.800–216.160`) · `w0409` farther (`216.220–216.500`) · `w0410` from (`216.540–216.720`) · `w0411` Earth. (`216.800–217.200`)

#### `OWB-2026-11-E1` Visual & Motion Plan — Selection 2B (`26.740 s`, 8 Cuts, `Cut 1 = 2.50 s ≤ 2.8 s`, `Cut 2 = 4.60 s ≤ 4.8 s`, Max Hold `3.84 s ≤ 4.0 s`)

| Shot | Short Time (`s`) | Duration (`s`) | Non-DEM Visual Asset & Motion Source (`J2359` Compliant) | On-Screen Text / Overlay (`16:9` Band) |
|---|---|---|---|---|
| **1 (Opener)** | `0.00–2.50` | `2.50` (`Cut 1 = 2.50 s ≤ 2.8 s`) | **Opener Route M1-B (`code_graphic_034_short2_open.mp4`):** Full-bleed real-body Pluto–Charon composite (`PIA19968` Charon globe looming over `PIA19948` Pluto limb on lifted `#0a1026` sky, `subject ≥ 65%`, `sky ≤ 25%`) with a `1.00× → 1.18×` fast parallax move in `0.0–1.0 s` + solar terminator sweep by `0.5 s` (`frame0_diff_0_1_5s ≥ 1.50`, `motion_0_1s ≥ 10.0`). | `0.00–2.50 s`: Frame-0 hook caption `PLUTO'S **DOUBLE** WORLD?` + `whoosh_soft.wav` at `0.00 s` |
| **2** | `2.50–4.60` | `2.10` (`Cut 2 = 4.60 s ≤ 4.8 s`) | **Real New Horizons LORRI co-orbital video (`R03`/`R23`):** `File:The Pluto System As Seen By New Horizons Spacecraft.webm` (`1920×1080`, NASA/JHUAPL/SwRI PD) showing Pluto and Charon orbiting their shared barycentre. | Captions only (`"...19,000 kilometers away..."`) |
| **3** | `4.60–8.08` | `3.48` (`≤ 4.0 s`) | **Graded USNO 1978 discovery plate & high-res Charon reveal (`R19`):** `File:Charon Discovery.jpg` (`1416×1072` USNO PD) transitioning across the `0.180 s` breath (`6.22–6.40 s`) as VO speaks `"June 1978."` (`S18`). | Captions only (`"...turn Pluto into a double world? June 1978."`) |
| **4** | `8.08–11.92` | `3.84` (`≤ 4.0 s`) | **Animated double-planet caliper graphic (`R22`):** `code_graphic_034_r22_double_planet_scale.mp4` (using real `PIA19966` Pluto & Charon globes), drawing the `1,214 KM` caliper across Charon as `S22` begins (`"At 1,214 kilometers across, Charon is about half the size of Pluto..."`). | `9.50–13.50 s`: Exact parent long listing title banner `Why Pluto's Frozen Heart Has Zero Craters` |
| **5** | `11.92–15.60` | `3.68` (`≤ 4.0 s`) | **Graded real New Horizons Charon globe (`PIA19968`):** Active pan across `PIA19968` (*Charon in Enhanced Color*, `2000×2000`), showcasing Mordor Macula and Serenity Chasma (`"the largest known satellite..."`). | `9.50–13.50 s` promo title clears at `13.50 s` |
| **6** | `15.60–19.30` | `3.70` (`≤ 4.0 s`) | **Graded real New Horizons true-scale pair (`PIA19966`):** Lateral move across `PIA19966` (*Charon and Pluto: Strikingly Different Worlds*, `3000×3000`) with the single Short Teach overlay. | `16.80–20.40 s`: Single Short Teach overlay `CHARON: 1,214 KM WIDE` (`4` words, `11–12%` height) + `tick_ink.wav` |
| **7 (Payoff)** | `19.30–23.00` | `3.70` (`≤ 4.0 s`) | **Real New Horizons binary separation plate (`PIA19856`):** Pan across `PIA19856` (*A Binary Planet in Color*, `2526×501`) as `"often called a double planet"` (`20.22–22.18 s`, `75.6%–82.9%` runtime) lands and `S24` begins (`"By comparison..."`). | `16.80–20.40 s` single Teach overlay clears at `20.40 s` |
| **8 (Loop Seam)** | `23.00–26.74` | `3.74` (`≤ 4.0 s`) | **Earth–Moon distance contrast (`PIA00405`) returning to matched Shot-1 Pluto–Charon framing (`0.25 s` crossfade into Shot 1):** Spoken VO finishes `"20 times farther from Earth."` at `26.060 s`, followed by `0.680 s` loop tail (`< 1.2 s`, continuous music bed, **zero end card or CTA**). | Captions only; **zero end card** |

---

### 4.5 Separately Scoped Alternatives — Selection 2C-i & Selection 2C-ii (Charon Mutual Tidal Lock: *"Charon neither rises nor sets"*)

Because `S26` (*"In mutual tidal locking, the same surfaces of Charon and Pluto always face each other, so Charon neither rises nor sets, hovering over the same spot on Pluto's surface."*, `w0448–w0476`) is `29` Scribe words and `12.360 s` raw, no untouched whole-sentence combination starting with `S17` (`6.160 s`, `13`w) that includes `S26` fits inside `27.0 s` while reaching `≥ 55` words (`S17 + S23 + S24 + S26` = `58`w, `27.100 s` raw speech before breaths/tail). If the elected Chief specifically requires the **mutual tidal-locking payoff** in Short 2 without new VO spend, two separately scoped `1.00×`-speed solutions are established:

1. **Variant 2C-i (4 Whole Sentences `S17 + S23 + S24 + S26` with Internal Comma-Pause Silence Trimming at `1.00×` Speed):**
   - **Sentences (`58` Scribe words, `100%` complete sentences ending on period `w0476` `"surface."`):**
     - `S17` (`w0296–w0308`, `152.460–158.620 s`, `13`w)
     - `S23` (`w0396–w0401`, `207.960–212.720 s`, `6`w): *"Charon orbits Pluto at 19,640 kilometers."*
     - `S24` (`w0402–w0411`, `213.380–217.200 s`, `10`w): *"By comparison, our moon is 20 times farther from Earth."*
     - `S26` (`w0448–w0476`, `236.100–248.460 s`, `29`w): *"In mutual tidal locking, the same surfaces of Charon and Pluto always face each other, so Charon neither rises nor sets, hovering over the same spot on Pluto's surface."*
   - **Exact Internal Silence Gaps Trimmed (zero phoneme clipping, `1.00×` playback speed):**
     - `S17` (`w0302` `"away"` → `w0303` `"turn"`, `155.960–156.420 s`): trim `0.460 s → 0.140 s` (`-0.320 s`)
     - `S24` (`w0403` `"comparison,"` → `w0404` `"our"`, `214.240–214.660 s`): trim `0.420 s → 0.180 s` (`-0.240 s`)
     - `S26` (`w0451` `"locking,"` → `w0452` `"the"`, `237.660–238.080 s`): trim `0.420 s → 0.180 s` (`-0.240 s`)
     - `S26` (`w0462` `"other,"` → `w0463` `"so"`, `242.140–242.740 s`): trim `0.600 s → 0.180 s` (`-0.420 s`)
     - `S26` (`w0468` `"sets,"` → `w0469` `"hovering"`, `244.700–245.180 s`): trim `0.480 s → 0.140 s` (`-0.340 s`)
   - **Demonstrated Total Runtime:** `27.100 - 1.560 = 25.540 s` speech + `0.060 s` lead + `3 × 0.180 s` (`0.540 s`) inter-sentence breaths + `0.660 s` loop tail (`< 1.2 s`) = **`26.800 s` (`22.0–27.0 s` PASS)** *(or `26.300 s` if the remaining `0.20–0.28 s` pauses after `w0299`, `w0406`, `w0458`, `w0472` are also tightened to `0.14 s`)*.
   - **Per-Word Timestamps for `S23` & `S26` (`stt_raw.json`):**
     - `S23` (`w0396–w0401`, `207.960–212.720 s`, `6`w): `w0396` Charon (`207.960–208.400`) · `w0397` orbits (`208.500–208.900`) · `w0398` Pluto (`208.960–209.400`) · `w0399` at (`209.540–209.680`) · `w0400` 19,640 (`209.800–211.900`) · `w0401` kilometers. (`211.960–212.720`)
     - `S26` (`w0448–w0476`, `236.100–248.460 s`, `29`w): `w0448` In (`236.100–236.220`) · `w0449` mutual (`236.280–236.680`) · `w0450` tidal (`236.760–237.140`) · `w0451` locking, (`237.180–237.660`) · `w0452` the (`238.080–238.200`) · `w0453` same (`238.280–238.580`) · `w0454` surfaces (`238.660–239.180`) · `w0455` of (`239.240–239.320`) · `w0456` Charon (`239.380–239.760`) · `w0457` and (`239.820–239.920`) · `w0458` Pluto (`239.960–240.320`) · `w0459` always (`240.600–240.980`) · `w0460` face (`241.060–241.360`) · `w0461` each (`241.440–241.640`) · `w0462` other, (`241.680–242.140`) · `w0463` so (`242.740–242.900`) · `w0464` Charon (`242.980–243.400`) · `w0465` neither (`243.460–243.760`) · `w0466` rises (`243.840–244.240`) · `w0467` nor (`244.280–244.440`) · `w0468` sets, (`244.480–244.700`) · `w0469` hovering (`245.180–245.600`) · `w0470` over (`245.640–245.820`) · `w0471` the (`245.860–245.960`) · `w0472` same (`246.020–246.300`) · `w0473` spot (`246.500–246.840`) · `w0474` on (`246.920–247.040`) · `w0475` Pluto's (`247.100–247.600`) · `w0476` surface. (`247.660–248.460`)

2. **Variant 2C-ii (Pause-Bounded Clause Lift `S17 + S22[w0370–w0395] + S26[w0448–w0468]` with Zero Internal Edits):**
   - `S17` (`w0296–w0308`, `152.460–158.620 s`, `6.160 s`, `13`w) + `S22_clause` (`w0370–w0395`, `196.540–206.700 s`, `10.160 s`, `26`w, preceded by `0.520 s` silence after `"across,"`) + `S26_clause` (`w0448–w0468`, `236.100–244.700 s`, `8.600 s`, `21`w, followed by `0.480 s` silence after `"sets,"`) = **`60` Scribe words**, `24.920 s` speech + `0.060 s` lead + `0.360 s` breaths (`2 × 0.180 s`) + `0.720 s` loop tail = **`26.060 s` total runtime** (`22.0–27.0 s` PASS).
   - **Mandatory `audio_input` Gate:** Because `w0468` (`"sets,"`) is a comma boundary before `"hovering over the same spot on Pluto's surface."`, Variant 2C-ii may only be used if Chief approves clause-boundary cutting and a reviewer with demonstrated `audio_input` confirms natural sentence-final intonation at `244.700 s`.

---

### 4.6 Complete `OWB-2026-11-E1` & `.cursor/rules/orbit-build-shorts.mdc` Mandatory Brief Fields — Short 2 (`J2320`)

| Mandatory Brief Field (`OWB-2026-11-E1` & `orbit-build-shorts.mdc`) | Selection 2A (Water-Ice Mountains Primary) | Selection 2B (Charon Double-World Alternative) | Selection 2C-i / 2C-ii (Charon Tidal-Lock Alternatives) |
|---|---|---|---|
| **Listing & Promo Title (`≤ 60` chars)** | `Why Can Towering Mountains Stand on Pluto at −240°C?` (`52`c) | `Why Did a Secret 19,000 km Away Make Pluto a Double World?` (`58`c) | `Why Did a Secret 19,000 km Away Make Pluto a Double World?` (`58`c) |
| **Frame-0 Source & Motion Mechanism** | Route M1-A (`PIA11709` real-image landing sequence) or Route M1-B (`code_graphic_034_short2_open.mp4` fast `1.18×` move + terminator sweep over `PIA20732`); **zero DEM, zero slow still push** | Route M1-B (`code_graphic_034_short2_open.mp4` fast `1.18×` move + terminator sweep on `PIA19968` Charon over `PIA19948` Pluto limb); **zero DEM, zero slow still push** | Route M1-B (`code_graphic_034_short2_open.mp4` fast `1.18×` move + terminator sweep on `PIA19968` Charon over `PIA19948` Pluto limb) |
| **First-Word Onset (`≤ 0.15 s`)** | **`0.060 s`** (`w0842` `"Why"` at `441.760 s`, cut from `441.700 s`) | **`0.060 s`** (`w0296` `"Why"` at `152.460 s`, cut from `152.400 s`) | **`0.060 s`** (`w0296` `"Why"` at `152.460 s`, cut from `152.400 s`) |
| **Spoken Surprise Time (`≤ 1.50 s`)** | **`0.960–1.500 s`** (`"towering mountains"` at `+0.520..+1.500 s`) | **`0.820–1.360 s`** (`"secret"` at `+0.820..+1.360 s`) | **`0.820–1.360 s`** (`"secret"` at `+0.820..+1.360 s`) |
| **Cut 1 Timestamp (`≤ 2.80 s`)** | **`2.50 s`** | **`2.50 s`** | **`2.50 s`** |
| **Cut 2 Timestamp (`≤ 4.80 s` from `0.00 s`)** | **`4.60 s`** (Shot 2 duration `2.10 s`) | **`4.60 s`** (Shot 2 duration `2.10 s`) | **`4.60 s`** (Shot 2 duration `2.10 s`) |
| **Later Shot Beat Times & Max Hold (`≤ 4.00 s`)** | Cuts at `2.50, 4.60, 8.30, 11.98, 15.74, 19.20, 22.80 s`; **max hold `3.76 s`** (`≤ 4.00 s` PASS) | Cuts at `2.50, 4.60, 8.08, 11.92, 15.60, 19.30, 23.00 s`; **max hold `3.84 s`** (`≤ 4.00 s` PASS) | Cuts at `2.50, 4.60, 8.10, 11.80, 15.50, 19.20, 22.90 s`; **max hold `3.90 s`** (`≤ 4.00 s` PASS) |
| **Sentence-1 VO Breath (`< 0.25 s`)** | **`0.200 s`** (`S46 → S47` trimmed from `0.900 s`) | **`0.180 s`** (`S17 → S18` trimmed from `0.860 s`) | **`0.180 s`** (`S17 → S23` or `S22_clause`) |
| **Runtime & Earliest Allowed Payoff (`0.70 × runtime`)** | Runtime **`26.300 s`** (`25.820 s` E1); `0.70 × 26.300 =` **`18.410 s`** | Runtime **`26.740 s`** (`26.320 s` E1); `0.70 × 26.740 =` **`18.718 s`** | Runtime **`26.800 s` (2C-i) / `26.060 s` (2C-ii)**; `0.70 × =` **`18.760 s` / `18.242 s`** |
| **Actual Payoff Time (`≥ 0.70 × runtime`)** | **`20.80–22.08 s`** (`"big blocks of water ice"`, `79.1%–84.0%` — **PASS**) | **`20.22–22.18 s`** (`"often called a double planet"`, `75.6%–82.9%` — **PASS**) | **`21.10–22.90 s` (2C-i) / `22.90–25.34 s` (2C-ii)** (`"neither rises nor sets"`, **`≥ 78.7%` — PASS**) |
| **Last-Word & Loop-Point Timestamps / Tail (`< 1.20 s`)** | Last word `25.560 s` (`25.080 s` E1) → Loop `26.300 s` (`25.820 s` E1); **tail = `0.740 s`** (`< 1.20 s` PASS) | Last word `26.060 s` (`25.640 s` E1) → Loop `26.740 s` (`26.320 s` E1); **tail = `0.680 s`** (`< 1.20 s` PASS) | Last word `26.140 s` / `25.340 s` → Loop `26.800 s` / `26.060 s`; **tail = `0.660 s` / `0.720 s`** (`< 1.20 s` PASS) |
| **Last-Line → Line-1 Loop Sentence** | *"...coated with frozen gases like methane. → Why can towering mountains stand beside a flowing glacier between -226 and -240 degrees Celsius?"* | *"...By comparison, our moon is 20 times farther from Earth. → Why did a secret 19,000 kilometers away turn Pluto into a double world?"* | *"...hovering over the same spot on Pluto's surface. → Why did a secret 19,000 kilometers away turn Pluto into a double world?"* |
| **Meta-Promise / Spoken CTA / End Card Present?** | **NO** (`0` meta-promises, `0` spoken CTAs, `0` end cards; promo title at `9.5–13.5 s` only) | **NO** (`0` meta-promises, `0` spoken CTAs, `0` end cards; promo title at `9.5–13.5 s` only) | **NO** (`0` meta-promises, `0` spoken CTAs, `0` end cards; promo title at `9.5–13.5 s` only) |

---

## 5. Short 1 (`J2319`, Test A Opening Short) — Reconciled to Locked `v03`

Per `AGENTS.md` (*Standing lessons §5 — Test A, the opening Short*) and `jobs/reviews/J2354/CHIEF_RULING.md`, one of each long's Shorts is the long's own opening (`30–38 s` of the master, reframed to 9:16, cut cleanly on a sentence end, exempt from `22–27 s` and from the Keeper one-question rule until Test A's readout). In `v03`, Sentence 1 (`S01`) opens at `0.100 s` (`"Across Pluto's horizon..."`) and Sentence 3 (`S03`) ends at `38.820 s`:

- **Job ID:** `J2319` (`blocked` until Chief plan approval + `J2361`/`J2362` picture/music/SFX delivery)
- **Title (`54` chars, `≤ 60`):** `What Did New Horizons Find in Pluto's Frozen Heart?`
  - *Alternative matching Line-1 title (`57` chars):* `What Would You See on the Bright Half of Pluto's Heart?`
- **Frame-0 Hook Caption (`0.00–2.50 s`, 3 words):** `ZERO **CRATERS**` (distinct from standalone Short `gmzaCfJF1gA`'s `NO **CRATERS**` and `PIA19952` Frame 0)
- **Promoted Long Exact Listing Title Banner (`9.60–13.60 s`):** `Why Pluto's Frozen Heart Has Zero Craters`
- **Single Teach Overlay (`20.20–24.00 s`, inside 16:9 band):** `14 JULY 2015 · 12,500 KM` (`4` tokens)

| Option | `v03` Sentences (`stt_raw.json` Words) | Master WAV Span (`s`) | Scribe Words | Speech Sum (`s`) | Pauses + Loop Tail (`<1.2s`) | Total Runtime (`30–38 s` Test A Window) | Notes for Chief Ruling (`J2354`) |
|---|---|---|---|---|---|---|---|
| **Option 1A (Primary Continuous Cold Open: `S01 + S02 + S03`)** | `S01` (`w0000–w0021`, `0.100–8.700 s`) + `S02` (`w0022–w0038`, `9.600–19.040 s`) + `S03` (`w0039–w0071`, `20.140–38.820 s`) | `0.100–38.820` | `72` words | `36.720 s` (incl. internal clause pauses) | Tighten `S01→S02` (`0.900→0.200 s`), `S02→S03` (`1.100→0.200 s`), and `w0054→w0055` (`1.020→0.220 s`) in room tone + `0.700 s` tail | **`37.020 s` — PASS (`30–38 s`)** | Pure continuous `S01–S03` opening of the long (`R01–R04`), cut cleanly on the sentence end `"and solved that mystery."` (`w0071`). Requires `audio_input` verification of the 3 tightened silence gaps. |
| **Option 1B (Hook-to-Central-Question Cold Open: `S01 + S02 + S05 + S06`)** | `S01` (`w0000–w0021`, `0.100–8.700 s`) + `S02` (`w0022–w0038`, `9.600–19.040 s`) + `S05` (`w0100–w0114`, `54.520–60.220 s`) + `S06` (`w0115–w0126`, `60.880–65.160 s`) | `0.100–19.040` + `54.520–65.160` | `66` words | `28.020 s` | Keep natural internal pauses (`2.160 s`) + `0.720 s` tail | **`30.900 s` — PASS (`30–38 s`)** | Opens on `S01–S02` (`1,000 km`, zero craters) and splices across `S03–S04` to the central Ch 0 hook questions (`S05–S06`: *"How can a world one-fifth the width of Earth keep a giant nitrogen heart churning? And what secret did our only spacecraft to visit Pluto discover there?"*). |

---

## 6. Reserve Short 3 (Convection Cells / Zero-Crater Glacier) — Reconciled to Locked `v03`

Held in reserve if a third Short is scheduled after Short 1 and Short 2:
- **Title (`57` chars, `≤ 60`):** `How Can Tiny Pluto Keep a Giant Nitrogen Heart Churning?`
- **Verbatim `v03` Whole-Sentence Selection (`S05 + S41 + S42`, `56` Scribe words, `25.380 s` total runtime):**
  - `S05` (`w0100–w0114`, `54.520–60.220 s`, `5.700 s`, `15`w): *"How can a world one-fifth the width of Earth keep a giant nitrogen heart churning?"*
  - `S41` (`w0734–w0752`, `387.180–395.240 s`, `8.060 s`, `19`w): *"About 1,000 kilometers wide, larger than Texas and Oklahoma combined, and the largest known glacier in the solar system."*
  - `S42` (`w0753–w0774`, `396.600–407.120 s`, `10.520 s`, `22`w): *"While craters up to 260 kilometers across dot other parts of Pluto, the frozen nitrogen plains of Sputnik Planitia show no craters."*
  - **Totals (`S05 + S41 + S42`):** **`56` Scribe words** (`55–65` PASS), `24.280 s` speech + `0.060 s` lead + `0.360 s` breaths (`2 × 0.180 s`) + `0.680 s` loop tail (`< 1.2 s`) = **`25.380 s` total runtime** (`22.0–27.0 s` PASS), 100% whole sentences.

---

## 7. Actual Picture, Music & SFX Delivery Dependencies (Coordinated with `J2359` → `J2361` → `J2362`)

Neither `J2319` (Short 1) nor `J2320` (Short 2) may reopen until the following dependency chain completes in order (coordinating with `J2359`'s already-queued `J2361` and `J2362` rather than duplicating them):

| Step | Job / Stage | Deliverable Required on Disk | Coordination Note |
|---|---|---|---|
| **1. Chief Shorts Plan Decision** | **Queued by `J2360`** (`kind: chief`, `after: J2360`, `film: 034`, `stage: script`) | Elected Chief reviews and merges this `SHORTS_PLAN_v01.md`, selecting Short 2's approved `v03` lift (`Selection 2A` Water-Ice Mountains vs `Selection 2B` Charon Double-World vs `Selection 2C-i/ii` Tidal-Lock alternative), Short 1's Test A option (`Option 1A` vs `Option 1B`), and the `£0` native-moving opener route (`Route M1-A` `PIA11709` landing movie vs `Route M1-B` `code_graphic_034_short2_open.mp4` fast-move composite). | Independent planning decision; zero spend. |
| **2. Shot-List Repair & Production Release** | `J2361` (`open`, repair PR #626) → `J2362` (`open`, Chief re-review & release) | Repaired `SHOT_LIST_v01.md` / `shot_list_v01.csv` / `MUSIC_BRIEF_v01.md` / `SFX_PLAN_v01.md` (with DEM reconstructions `PIA21863`, `PIA21864`, and `R38` replaced per `J2359`), merged by `J2362`, which queues the `034` picture harvest, code-graphic renders, music bed, and SFX jobs. | Already queued by `J2359`; `J2360` coordinates with `J2361`/`J2362` without duplicating them. |
| **3. Picture Harvest, Opener & Code Graphics (`034 picture`)** | Queued by `J2362` upon shot-list approval | Harvested non-DEM public-domain video files (`PIA11709` *A Colorful Landing on Pluto* real-image sequence, `File:The Pluto System As Seen By New Horizons Spacecraft.webm`, `File:New Horizons Extreme Close-Up Of Pluto Surface (No Audio).ogv`), graded NASA stills (`PIA20732`, `PIA19947`, `PIA20198`, `PIA19948`, `PIA19968`, `PIA19966`, `PIA19856`), `code_graphic_034_short2_open.mp4` (if Route M1-B selected), and rendered 1080p code graphics (`R22`, `R51`) in `03_Picture/` and `04_Generated-Clips/`. | Supplies the missing native-moving/fast-move opener and mid-Short plates. |
| **4. Music Bed & House SFX Kit (`034 music` / `034 sfx`)** | Queued after `J2362` (`MUSIC_BRIEF_v01.md` & `SFX_PLAN_v01.md`) | `05_Music/pluto_score_bed_v01.mp3` (passing `scripts/music_gate.py`) and `06_Sound-Effects/kit_v01/{rumble_low.wav,whoosh_soft.wav,tick_ink.wav}` (`python3 scripts/sfx_kit.py make --out-dir 02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/06_Sound-Effects/kit_v01`, `£0` synthesis). | Shorts use a continuous slice of the parent film's own score bed (`lesson 7`) and house SFX (`sfx_kit.py level` PASS). |
| **5. Short Assembly + Delegated Perceptual Gate Verification (`J2319`, `J2320`)** | `J2319` and `J2320` (reopened only after Steps 1–4 complete) | Master `.mp4` cuts in `10_Shorts/`, `gate_shorts_open.py check` PASS, `picture_qa.py` PASS, `polish_gate.py` PASS, `sfx_kit.py level` PASS, `thumb_preview.py short` sheet, **plus** delegated `audio_input` splice check and `moving_video_input` motion check before Ben's phone watch. | No Short is uploaded or scheduled until Ben's final UAT watch OK. |
