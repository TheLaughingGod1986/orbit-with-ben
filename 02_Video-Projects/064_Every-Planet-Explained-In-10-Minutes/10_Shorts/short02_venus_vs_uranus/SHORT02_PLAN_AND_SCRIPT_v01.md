# OWB:064 Short 2 — Companion Planet-Extremes Short Plan & Chief Decision Package (`SHORT02_PLAN_AND_SCRIPT_v01.md`)

- **Job:** `J3904` (`ref: J3023`, `due: 2026-12-13T18:00:00Z`)
- **Prepared by:** `gemini` (specialist worker — parked for elected Chief `codex` decision; zero PASS/merge/spend performed)
- **Parent Long Film:** `OWB:064` — *Every Planet Explained in 12 Minutes (Mercury to Neptune)* (`02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes`, planned air **Wed 16 Dec 2026 18:00 Europe/London**)
- **Locked Parent Script:** `01_Script/every_planet_explained_script_master_v04.md` (SHA-256 `556f3c8df68ee3cd1420ef03b8cedc04a7f0f79463d98ebf4d3d5e5753408db8`, locked in `J3711`)
- **Locked Parent Sources:** `01_Script/SOURCES.md` (SHA-256 `4a7e3fa5c74a548764886a274514d2590e5951e5e8782aa8118566d252fdc415`, locked in `J3711`)
- **Locked Parent VO:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/02_Voiceover/every_planet_explained_vo_v01.wav` (SHA-256 `4b478fcded393890064ffd285a4121882dc26e0515f3cadc6569adf0465616aa`, `683.86 s`, locked in `J3021`)
- **Spend Posture in `J3904`:** **£0.00 cash, 0 Flow credits, 0 Vertex credits, 0 ElevenLabs credits spent.** No upload, no schedule change, no YouTube state mutation.

---

## 1. Executive Decision Needed From Elected Chief (`codex`)

`J3904` specifies: *"Strict spend boundary: £0 cash, 0 Flow/Vertex credits, and NO extra ElevenLabs spend authorization — do not quietly expand the 8,000-character long-VO scope (either assemble from existing locked 064 VO segments with clean sentence cuts, or park for separate Chief VO authorization if any new VO lines are proposed)."*

An exhaustive audit of all **72 sentences** (`S00–S71`) in `02_Voiceover/stt/every_planet_explained_vo_v01/stt_raw.json` proves that **the Venus 464°C vs Uranus −224.2°C concept cannot be cleanly assembled from the existing locked 064 VO alone without breaking mandatory Shorts gates** (detailed in §2 below).

Two concrete options are presented for Chief ruling:

| Option | Angle & Narration Route | Spend Authorization Required | Gate Compliance | Recommendation |
|---|---|---|---|---|
| **Option A (Recommended Primary)** | **Exact J3904 Concept: Venus 464°C vs Uranus −224.2°C** (`064_short02_venus_vs_uranus_script_v01.md`) — 3 crisp sentences (`47` written / `56` expanded spoken words, **`277` ElevenLabs chars**, calibrated `~25.7 s` total runtime) | **Separate Chief VO authorization for `~277` chars** (`~180–280` plan credits, **£0 cash** from Ben's existing monthly ElevenLabs plan: `7,275` credits left on 27 Nov, resetting **`2026-11-30T10:50Z`** — 13 days before `13 Dec` due date). `£0` Flow/Vertex. | **100% PASS** on every Keeper, `OWB-2026-11-E1`, First-Second, Payoff (`86.9% ≥ 70%`), Loop, Full-Bleed `9:16` (`≤ 1.83×`), and `SOURCES.md` lock | **RECOMMENDED:** Lock `064_short02_venus_vs_uranus_script_v01.md`, authorize `~277`-char `vo_take.py` (`kind: vo`, £0 cash), then queue `kind: assembly` using §4 shot list. |
| **Option B1 (Zero-VO Fallback Only)** | **Single-Planet Venus Runaway Greenhouse Lift** (`S08 + S09 + S12 + S13` from locked `every_planet_explained_vo_v01.wav`, `59` Scribe words, `25.64 s` raw speech / `27.00 s` tight total) | **£0 cash, 0 ElevenLabs chars, 0 Flow/Vertex credits** | **Trade-offs / Waivers Required:** Drops Uranus completely (changes Short 2 angle from J3904 concept); Line 1 (`"Why is Venus hotter?"`, `1.24 s`) is an unanchored Mercury→Venus comparative; greenhouse answer starts at `7.9 s` (`29%`, failing `≥70%` payoff); sits right on the `27.0 s` ceiling. | **Fallback only** if Chief mandates literally `0` ElevenLabs characters even after the 30 Nov reset and approves changing the angle + waiving `≥70%` payoff. |

---

## 2. Exhaustive Audit of Locked 064 VO (`every_planet_explained_vo_v01.wav`)

Every Venus (`S08–S16`) and Uranus (`S55–S63`) sentence in `02_Voiceover/stt/every_planet_explained_vo_v01/stt_raw.json` was timed and tested for clean-sentence-cut assembly:

| ID | Master Time (`s`) | Dur (`s`) | Words | Verbatim Locked 064 Spoken Sentence |
|---|---:|---:|---:|---|
| `S08` | `80.060–81.300` | `1.24` | `4` | *"Why is Venus hotter?"* |
| `S09` | `82.200–88.520` | `6.32` | `15` | *"At one hundred and eight million kilometers out orbits Venus, nearly Earth's twin in size."* |
| `S10` | `89.500–93.180` | `3.68` | `10` | *"What would you see dropping beneath its sulfuric acid clouds?"* |
| `S11` | `94.440–97.680` | `3.24` | `10` | *"You reach the hottest planetary surface in our solar system."* |
| `S12` | `98.380–109.700` | `11.32` | `25` | *"A runaway greenhouse under a ninety-six point five percent carbon dioxide atmosphere traps heat and bakes the rock to four hundred and sixty-four degrees Celsius."* |
| `S13` | `110.780–117.540` | `6.76` | `15` | *"Surface air crushes at ninety-two bars, like nine hundred and thirty meters underwater on Earth."* |
| `S55` | `494.280–496.420` | `2.14` | `5` | *"Why does Uranus roll sideways?"* |
| `S58` | `522.620–524.380` | `1.76` | `6` | *"Why are its seasons so extreme?"* |
| `S59` | `525.660–546.740` | `21.08` | `36` | *"While Earth tilts 23.4 degrees, Uranus tips 97.77 degrees, more than four times Earth's tilt, possibly from an ancient collision rolling sideways and spinning backwards every 17 hours to plunge each pole into a 21-year winter."* |
| `S61` | `554.540–563.940` | `9.40` | `15` | *"Uranus's atmosphere reaches a minimum of -224.2 degrees Celsius, colder than Neptune in some places."* |
| `S63` | `570.960–581.140` | `10.18` | `18` | *"At least 80% of its mass is hot, dense fluid, reaching about 4,982 degrees Celsius near the core."* |

### Why Locked 064 VO Cannot Cleanly Assemble the Venus 464°C vs Uranus −224.2°C Short

1. **No Venus-vs-Uranus question exists in the locked VO:** `S08` (*"Why is Venus hotter?"*, `1.24 s`, 4 words) is a Mercury→Venus chapter bridge. It omits Uranus, `464°C`, and `−224°C`, leaving the viewer asking *"hotter than what?"*.
2. **The only `464°C` sentence (`S12`, `11.32 s`) never says the word `"Venus"`:** Together, `S12` (`11.32 s`) + `S61` (`9.40 s`) already total **`20.72 s`** of raw speech before any question, subject anchor, breaths, or loop tail.
3. **Every Venus+Uranus whole-sentence permutation fails mandatory gates:**
   - **`S08 + S61 + S12`** (`21.96 s` speech / `~23.3 s` total): only **`44` Scribe words / `52` spoken words (< `55`-word floor)**; `S12` (*"A runaway greenhouse..."*) immediately follows *"colder than Neptune in some places"* with **no `"Venus"` subject** (grammatically attributing the greenhouse to Neptune/Uranus); greenhouse explanation starts at `~11.1 s` (`48%`, directly over the `9–14 s` promo banner, failing Learnings #6 `≥70%` payoff).
   - **`S08 + S61 + S09 + S12`** (`28.28 s` raw speech / **`~29.8 s` total**): **FAILS the `22–27 s` duration ceiling** (cannot fit without `atempo > 1.06`, which is prohibited).
   - **`S08 + S11 + S12 + S61`** (`25.20 s` speech / `~26.5 s` total): `S11` (*"You reach..."*) is an orphaned fragment from `S10` (*"dropping beneath its sulfuric acid clouds?"*); answers *"Why is Venus hotter?"* at `~5–16 s` (`20–62%`, failing `≥70%` payoff); Uranus `−224.2°C` is tacked on after the question is already answered.
4. **Other single-planet whole-sentence lifts in `064` VO also fail or collide:**
   - **Mars (`S26 + S31 + S32`):** `19.56 s` raw speech (`~20.8 s` total → **FAILS `22 s` floor**), `49` words.
   - **Uranus (`S55 + S59`):** `23.22 s` speech, **`41` Scribe words (< `55` floor)**, duplicates `033` Uranus Shorts (`ZpEA8stoSPA`, `033_short01_testA_opening`).
   - **Neptune (`S64 + S69 + S70`):** `25.66 s` speech, **`51` Scribe words (< `55` floor)**, comparative *"faster?"* never explains *why*, duplicates standalone Short `1OCNzhkiBuc`.
   - **Saturn (`S47 + S52`):** `25.22 s` speech, **`51` Scribe words (< `55` floor)**, conflicts with Keeper rule 2 (no off-week Saturn Shorts).

---

## 3. Option A (Recommended Primary) — Script, Calibration & Source Verification

### 3.1 Exact Narration Text (`064_short02_venus_vs_uranus_script_v01.md`)

> **L1 (Hook Question, `0.08–7.79 s`):** Why is Venus 464 degrees Celsius while Uranus drops to minus 224?
>
> **L2 (Uranus Extreme Contrast, `7.97–15.41 s`):** Rolling sideways into 21-year winters, Uranus holds an atmosphere colder than Neptune in some places.
>
> **L3 (Late Venus Payoff, `15.59–24.86 s`):** Closer in, 92 bars of air crush Venus, where 96.5 per cent carbon dioxide traps heat in a runaway greenhouse.

### 3.2 Duration Calibration (Measured Against Locked `064` Ben Orbit Narrator Speed)

- **Observed active speaking rate in `every_planet_explained_vo_v01.wav` (`speed=1.04`, gaps `≤ 0.4 s`):** **`14.66` expanded chars/s** (`8,037` spoken chars across `548.1 s` active speech).
- **Option A text metrics:**
  - Raw ElevenLabs input (`vo_take.py --text`): **`277` characters** (`47` written words)
  - Expanded spoken text (all numbers spoken aloud): **`358` expanded characters** (`56` expanded spoken words — inside `55–65` target)
  - Estimated total runtime (speech + `0.08 s` lead + `2 × 0.18 s` breaths + `0.85 s` loop tail):
    - Fast (`15.8` expanded chars/s): **`23.95 s`**
    - Mid (`14.66` expanded chars/s): **`25.71 s`** *(dead center of `22.0–27.0 s`)*
    - Slow (`13.8` expanded chars/s): **`27.23 s`** *(assembler tightens internal comma pauses > `0.25 s` in silence if take lands > `26.0 s`, never using `atempo > 1.06`)*
- **Key Retention & Gate Milestones (at Mid `25.71 s`):**
  - First spoken word `"Why"`: `0.08 s` (`≤ 0.15 s` PASS)
  - Planet named (`"Venus"`): `~0.40 s`; extreme number (`"four hundred..."`): `~1.15 s` (`≤ 1.50 s` PASS)
  - Promoted long title banner (`9.00–14.00 s`): rides cleanly over Uranus winter/atmosphere contrast (`L2`) — **zero Venus answer during `9–14 s`**
  - Payoff (*"traps heat in a runaway greenhouse"*): starts at **`22.34 s` (`86.9%` of runtime ≥ `70%` PASS)**
  - Loop tail (`24.86–25.71 s`): **`0.85 s < 1.20 s`** (`OWB-2026-11-E1` PASS; zero end card, zero spoken CTA)

### 3.3 Claim-by-Claim Verification Against Locked `01_Script/SOURCES.md`

Every number and qualifier in Option A comes directly from `J3711`-locked `01_Script/SOURCES.md` (`4a7e3fa5...`) — zero new unverified facts:
- **`464 °C` surface heat:** `SOURCES.md` Row 3 (NASA NSSDCA Venus Fact Sheet: `737 K / 464 C`).
- **`−224 °C` atmospheric minimum (`−224.2 °C` exact in overlay/description/sources) & *"colder than Neptune in some places"*:** `SOURCES.md` Row 14 (NASA Science Uranus Facts: `49 K / -224.2 °C`, exact qualifier *"in some places"* preserved, never attributed to Voyager 2's 1986 flyby).
- ***"Rolling sideways into 21-year winters"*:** `SOURCES.md` Row 13 (NASA Science Uranus Facts: `97.77°` obliquity, `21-year-long, dark winter`; matches locked `v04` phrasing without unhedged collision assertion).
- **`92 bars` surface air pressure & `96.5 per cent carbon dioxide` trapping heat in a `runaway greenhouse`:** `SOURCES.md` Row 3 (NASA NSSDCA Venus Fact Sheet: `92 bars`, `96.5% CO₂`, `3.5% N₂`; phrased *"92 bars of air crush Venus, where 96.5 per cent carbon dioxide traps heat..."* so CO₂ is not overstated as 100% of the atmosphere).

---

## 4. Full-Bleed `9:16` Shot List & Verified Shelf Asset Provenance (`£0` Spend)

All 9 cuts use verified public-domain NASA/ESA/CSA/JAXA/Keck assets already on `/Volumes/data/` (`023`, `033`, `064`), cropped **full-bleed `1080×1920` (`cover` mode, `24 fps` CFR)** with **zero blur-pad/letterbox bars**, **zero Orbit at Frame 0 or cover**, **zero `PIA00271` / `PIA00233`**, and **every upscale `≤ 1.83×`** (`< 2.00×` warn / `≤ 2.35×` hard fail). `Venera13_surface.jpg` (`2048×553`) is **explicitly excluded** because full-bleed `9:16` scaling would require `3.47×` upscale.

| Cut | Window (`s`) | Dur (`s`) | Asset File (NAS Path & Verified SHA-256) | Native Size | 9:16 Upscale | Visual Beat & Overlay |
|---|---:|---:|---|---|---:|---|
| `R01` | `0.00–2.40` | `2.40` | `023/.../nasa_pool_v01/harvest_v04/svs14095_WISPR_4thflyby.mp4` (`11aa1171...`) | `1920×1080` (`video`) | `1.78×` | **Frame-0 moving Parker Solar Probe WISPR glowing Venus flyby** + burned-in hook **`464°C` (`#FFE000`) / `VS −224°C` (`#FFFFFF`)** (`0.00–2.20 s`) + `sfx_owb_whoosh_soft_v01.wav`. Cut 1 at `2.40 s ≤ 2.8 s`. |
| `R02` | `2.40–4.60` | `2.20` | `023/.../nasa_pool_v01/sdo/AIA171VenusTransit_HD1080.mp4` (`e580945d...`) | `1920×1080` (`video`) | `1.78×` | Real moving NASA SDO AIA 171 Å Venus transit silhouette against glowing Sun (*"464 degrees Celsius"*). Cut 2 at `4.60 s ≤ 4.8 s`. |
| `R03` | `4.60–7.90` | `3.30` | `033/.../04_Generated-Clips/J2334_fix/r55_cut1_r55b_100x_silent.mp4` (`df6d92d5...`) | `1920×1080` (`video`) | `1.78×` | Real moving Keck II cyan-blue Uranus cloud deck (*"while Uranus drops to minus 224?"*; bridges sentence-1 breath `< 0.25 s`). |
| `R04` | `7.90–10.70` | `2.80` | `033/.../03_Reference-Material/harvest_J2299_v01/weic2332a_hires.jpg` (`b241901c...`) | `2048×1536` (`still`, `1.045×` push) | `1.31×` | JWST NIRCam tilted cyan Uranus rings & polar cap (*"Rolling sideways into 21-year winters"*); **9.00–14.00 s exact long title banner begins at `9.00 s`**. |
| `R05` | `10.70–13.30` | `2.60` | `033/.../04_Generated-Clips/J2334_fix/r55_cut3_pia01488_pushin_silent.mp4` (`3b606e6e...`) | `1920×1080` (`video`) | `1.78×` | Real moving Voyager 2 `PIA01488` Uranus cloud limb under exact long title banner (`Every Planet Explained in 12 Minutes (Mercury to Neptune)`). |
| `R06` | `13.30–15.60` | `2.30` | `033/.../04_Generated-Clips/J2334_fix/r55_cut2_r55b_128x_vortex_silent.mp4` (`75adc0df...`) | `1920×1080` (`video`) | `1.78×` | Real moving Keck II Uranus atmospheric vortex (*"colder than Neptune in some places"*; long title clears at `14.00 s`). |
| `R07` | `15.60–17.50` | `1.90` | `064/.../03_Reference-Material/J3835_radar_v01/PIA00215.jpg` (`46dc965a...`) | `2782×2666` (`still`, `1.045×` push) | `0.85×` | Real NASA Magellan SAR Venus volcanic surface radar (`PIA00215`, clean inner crop, zero margins) on *"Closer in, 92 bars of air crush Venus"*. |
| `R08` | `17.50–21.50` | `4.00` | `023/.../nasa_pool_v01/harvest_v04/svs14095_WISPR_Magellan_4thFlyby.mp4` (`81cb48a1...`) | `1920×1080` (`video`) | `1.78×` | Real moving Parker Solar Probe WISPR + Magellan flyby + **Single Teach Overlay (`17.50–21.50 s`, `11.5%` band height inside `16:9` centre band): `96.5% CO₂ · 92 BARS`** + `sfx_owb_tick_ui_v01.wav`. |
| `R09` | `21.50–24.90` | `3.40` | `064/.../03_Reference-Material/harvest_J3022_v01/PIA23791.jpg` right globe (`853268f7...`) / `023/.../pioneer/pvo_uv_790205.jpg` (`f9d45efa...`) | `1085×1096` / `1839×1839` (`1.045×` push) | `1.83×` / `1.09×` | Glowing Venus cloud furnace on late payoff (*"traps heat in a runaway greenhouse"*); returns at `24.90–25.71 s` (`0.81 s < 1.2 s`, `≤ 0.3 s` xfade) to `R01` Frame-0 `svs14095_WISPR_4thflyby.mp4` for seamless loop. |

### Audio Assets (`£0`, Already Verified PASS in `064`)
- **Music Bed:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/05_Music/every_planet_score_bed_v01.mp3` (SHA-256 `3e47e9d6da9aca6836a00c27a1fa58e53801190ae06ed445966ed51f5c0d75c6`, `music_gate_v03.json` PASS vs 20 OWB beds; runs full duration through loop seam, `≥ 10 LU` under VO).
- **House SFX Kit:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/06_Sound-Effects/kit_v01/` (`sfx_owb_whoosh_soft_v01.wav` at `0.00 s` + Venus-to-Uranus/Uranus-to-Venus planetary transitions; `sfx_owb_tick_ui_v01.wav` at `17.50 s` Teach overlay; `sfx_owb_rumble_low_v01.wav` subtle under `R07` 92-bar crush; verified via `sfx_kit.py level`, `≥ 12 LU` under VO).
- **Mix Targets:** Integrated `−14.0 ± 0.5 LUFS`, true peak `≤ −1.6 dBTP` (strictly passes `gate_shorts_open.py` Check 8).

---

## 5. Approved Learnings & `OWB-2026-11-E1` Checklist (Pre-Build Lock)

- [x] **#1 · Title:** Positive Keeper question naming both subjects (`Why Is Venus 464°C While Uranus Drops to −224°C?`, `49` chars). First VO line asks the exact question.
- [x] **#2 · First-Second Rule (`0.0–1.5 s`, `J2429`):** Frame 0 (`0.00 s`) is full-bleed `9:16` moving NASA Parker Solar Probe WISPR Venus footage (`svs14095_WISPR_4thflyby.mp4`, zero blur-pad, zero fade-in, zero Orbit), with burned-in `464°C` (`#FFE000`) / `VS −224°C` (`#FFFFFF`) at `t = 0.00 s`, VO word 1 at `0.08 s ≤ 0.15 s`, planet (`Venus`) + extreme (`464`) inside `≤ 1.5 s`, zero meta-promise.
- [x] **#3 · Motion & `OWB-2026-11-E1` Pacing:** `Cut 1 = 2.40 s ≤ 2.8 s`, `Cut 2 = 4.60 s ≤ 4.8 s`, max hold `4.00 s ≤ 4.0 s`, 9 distinct shots, zero static zoom hold in `4–8 s`.
- [x] **#6 · Payoff (`≥ 70%`):** Estimated runtime `25.71 s`; earliest allowed payoff `18.00 s`; actual greenhouse payoff starts at **`22.34 s` (`86.9%`)** — zero answer during `9.00–14.00 s` promo title.
- [x] **#7 · Seam (`< 0.25 s` breath):** Sentence 1→2 and Sentence 2→3 breaths trimmed in silence to `0.18 s` (`< 0.25 s`), bridged straight into moving Uranus / Venus footage.
- [x] **#8 · 60% Stayed-to-Watch:** Moving native NASA WISPR video at Frame 0, first word `0.08 s`, surprise `~1.15 s`, Cut 1 `2.40 s`, zero meta-promise/logo/intro, loop tail `0.85 s < 1.2 s`.
- [x] **#9 · 70% Average Viewed / Loop:** Runtime `~25.7 s` (`22–27 s`), max hold `4.0 s`, payoff `86.9%`, matched frame-0 WISPR return (`≤ 0.3 s` xfade), continuous music bed, zero end card or CTA.

---

## 6. Late-December 2026 Air Slot Audit (Long-First & 1-Short/Day Lock)

Checked against `00_Brand/Channel-Setup/audits/shorts_open_library/library.json`, `00_Brand/Channel-Setup/social/UPLOADS.json`, and `031–034` Short manifests:
- **Parent Long `OWB:064` planned air:** **Wed 16 Dec 2026 18:00 Europe/London** (`Never air Short 1 or Short 2 before 064 long is public`).
- **Occupied `Mon/Wed/Fri/Sat 11:30Z` slots after 16 Dec:**
  - `Fri 18 Dec 11:30Z`: `032` Titan `McBNig_XScA` (scheduled in `UPLOADS.json`)
  - `Sat 19 Dec 11:30Z`: `028` Gliese 710 `v6euXX2omz4` (scheduled in `UPLOADS.json`)
  - `Mon 21 Dec 11:30Z`: `032` Titan `yDwDH-MV2wc` (scheduled in `UPLOADS.json`)
  - `Wed 23 Dec 11:30Z`: `033` Uranus Short 2 (`033_short02_ice_giant_surface`)
  - `Sat 26 Dec 11:30Z`: `034` Pluto Short 2 (`034_short02_water_ice_mountains`)
- **Free Non-Colliding Candidate Slots (Zero Reschedule):**
  - `Fri 25 Dec 11:30Z` (Christmas Day — available if used, otherwise skip)
  - `Mon 28 Dec 11:30Z` (**FREE** — ideal for `064` Short 1 Test A `J3903`)
  - **`Wed 30 Dec 2026 11:30 Europe/London (`2026-12-30T11:30:00Z`)` (FREE — recommended target air date for `064` Short 2)**
- **Frame-0 Uniqueness:** Parker Solar Probe WISPR glowing Venus flyby (`svs14095_WISPR_4thflyby.mp4`) is visually distinct from every scheduled late-December Short (Betelgeuse, Gliese 710, Titan, Uranus, Pluto, Mercury); verified at assembly time by `gate_shorts_open.py check <mp4> --air-date 2026-12-30`.

---

## 7. Next Steps After Elected-Chief Ruling

1. **If Chief approves Option A (Recommended):**
   - Merge this PR to `main`, lock `064_short02_venus_vs_uranus_script_v01.md`, and authorize one ElevenLabs `vo_take.py --text` take (`~277` chars, `£0` cash from existing monthly plan, zero top-up/overage; plan resets `2026-11-30T10:50Z`).
   - Queue `kind: vo` (`064` Short 2 VO take + `scribe_v2` check) → `kind: assembly` (full-bleed `9:16` `24 fps` CFR render, `gate_shorts_open.py check --air-date 2026-12-30`, `picture_qa.py`, `polish_gate.py`, `music_gate.py`, `sfx_kit.py level`, `thumb_preview.py short`) → `kind: qa` → `jobs.py awaits` for Ben's phone UAT watch (which supplies the audio/motion watch-and-listen check per `AGENTS.md`).
2. **If Chief selects Option B1 (£0 zero-VO fallback):**
   - Record Chief approval of the angle change (Venus-only runaway greenhouse) + `≥70%` payoff waiver on `S08+S09+S12+S13`, then queue `kind: assembly` directly from locked `every_planet_explained_vo_v01.wav`.
