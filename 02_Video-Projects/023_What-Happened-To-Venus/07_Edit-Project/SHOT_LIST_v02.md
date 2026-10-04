# Venus 023 — SHOT_LIST_v02 (Claude PASS 5982425011)

**Episode:** 023 What Happened to Venus?  
**Air target:** Sun 25 Oct 2026 18:00 UK (not Studio-scheduled yet)  
**Script lock:** `01_Script/venus_script_master_v02.md` (+ Earth-as-point prompt fix per Claude `090fcdd` / PASS note)  
**VO lock:** `02_Voiceover/venus_vo_v01.mp3` — Claude VO-PASS (comment 5982369937); `vo_check` PASS  
**VO duration:** **509.58 s** (~8.49 min) · 1247 words · 6 chapters · 0.7 s gaps (spoken cards skipped in VO)  
**Drafted:** 4 Oct 2026 ~18:15 London · Grok Bot from Claude PASS 5982425011  
**Status:** **v02 — Omni generate + NASA harvest green; edit waits on Omni frame-sheet PASS + rendered `code_graphics.py` outputs**

**Note:** Claude’s `code_graphics.py` landed on main as `f32afd4` (albedo / deuterium / line). Render on Mini when Omni sheets PASS; do not invent alternate Python.

---

## Meta / credit rules

| Rule | Value |
|---|---|
| Claude PASS | Comment **5982425011** — Omni queue + NASA harvest OK; edit after v02 |
| Spend | Free **Vertex** only; **Omni only** for Orbit / invented worlds; **never past £0**; £5 lag floor |
| No | ElevenLabs website gen; Veo/Flow for Orbit; merge/close of #99 |
| Frame 0 | Magellan flyover video if harvested; else **PIA00254** already pushing — no fade, no title, no Orbit |
| Cut pace | **4–6 s** per cut (VISUAL MUST). Long holds from v01 split below |
| Mariner 10 PIA23791 | **≤3 uses** total in this list |
| Venera | **Omit** (reuse unclear). Row 50 → Magellan plains under VO |
| Chapter cards | Remotion **lower-third** ~**2.5 s** over first shot of each chapter; keep **0.7 s** breath; **no** full-screen card; **no** VO retime |
| Code graphics | Slots for Claude’s upcoming `07_Edit-Project/code_graphics.py` — **do not invent Python**; rows marked **READY — code_graphics.py on main (`f32afd4`)** |

**Preferred plate families:** Magellan (radar / perspectives / flyover), Mariner 10 (≤3), SDO 2012 transit, ESA Venus Express (credit ESA), Parker WISPR, Pioneer Venus, DAVINCI/VERITAS/EnVision art, NASA EO/ISS chalk-or-reef, NASA twilight Venus-in-sky.

---

## Summary counts (v02)

| Source type | Rows (approx) | Notes |
|---|---:|---|
| **NASA / ESA** | ~95+ | More Magellan + SDO transit + Express + EO chalk/reef + twilight Venus; Ken Burns ~5–6% |
| **GENERATE (Omni)** | 4 assets | early ocean, steam lid, Orbit between, Orbit→Earth point (prompt fixed) |
| **CODE GRAPHIC** | 3 slots | albedo / deuterium / line — awaiting Claude file |
| **CARD (lower-third)** | 5 | Ch1–Ch5 titles ~2.5 s over first chapter shot |
| **BREATH** | 5 | 0.7 s gaps kept |
| **vs VO** | 509.58 s | Align ±1 s after Omni + graphics land |

**Generate budget:** 4 Omni × ~6–8 s · one take (+1 remint if sheet fails) · frame sheets for Claude PASS before edit insert.

---

## Chapter wall-clock (unchanged from VO)

| Ch | Title | vo_in | vo_out | Dur (s) |
|---:|---|---:|---:|---:|
| 0 | Open | 0.00 | 42.88 | 42.88 |
| — | breath | 42.88 | 43.58 | 0.70 |
| 1 | The Twin Next Door | 43.58 | 142.22 | 98.64 |
| — | breath | 142.22 | 142.92 | 0.70 |
| 2 | A Blanket With No Way Out | 142.92 | 223.80 | 80.88 |
| — | breath | 223.80 | 224.50 | 0.70 |
| 3 | Where Did the Water Go? | 224.50 | 347.54 | 123.04 |
| — | breath | 347.54 | 348.24 | 0.70 |
| 4 | The Line Earth Hasn't Crossed | 348.24 | 416.88 | 68.64 |
| — | breath | 416.88 | 417.58 | 0.70 |
| 5 | Going Back | 417.58 | 509.58 | 92.00 |
| | **Total** | | | **509.58** |

---

## Shot table

Columns: **#** · **vo_in–out** · **source** · **id / asset** · **move** · **VO / beat** · **notes**

### Ch 0 — Open (0.00–42.88) · Magellan already moving; 4–6 s; no Orbit

| # | vo_in | vo_out | source | id | move | VO / beat | notes |
|---:|---:|---:|---|---|---|---|---|
| 1 | 0.00 | 5.44 | NASA | **Magellan flyover video** (JPL) if harvested; else **PIA00254** Maat Mons | push 6% from frame 0 (or native flyover) | “Venus is the planet most like Earth…” | **Frame 0 lock.** Prefer real Magellan motion; fallback still+push. |
| 2 | 5.44 | 10.80 | NASA | PIA00254 continue / PIA00106 tighter | push 6% | radar / why radar | |
| 3 | 10.80 | 15.50 | NASA | **PIA00240** Lakshmi Planum | push 5% | hot enough to melt lead | |
| 4 | 15.50 | 20.80 | NASA | **PIA00241** Lakshmi + Maxwell edge | push 5% | air presses like deep sea | |
| 5 | 20.80 | 24.54 | NASA | PIA00087 Lavinia plains | push 5% | no machine survives long | No Venera. |
| 6 | 24.54 | 30.20 | NASA | **PIA23791** Mariner 10 globe (**use #1 of ≤3**) | push 5% | almost Earth’s size / same rock | |
| 7 | 30.20 | 36.32 | NASA | Magellan hemispheric / cloud mosaic (harvest PIA) | push 5% | less sunlight / still hottest | **Not** a 2nd Mariner hold. |
| 8 | 36.32 | 42.88 | NASA | Magellan global / Maat family | push 5% | promise: water / open answer | End open on Venus disk. |
| 9 | 42.88 | 43.58 | BREATH | — | — | (gap) | Keep 0.7 s breath. |

### Ch 1 — The Twin Next Door (43.58–142.22) · split long holds; Mariner ≤2 more; code graphic slots

| # | vo_in | vo_out | source | id | move | VO / beat | notes |
|---:|---:|---:|---|---|---|---|---|
| 10 | 43.58 | 46.10 | CARD | Remotion lower-third **“The Twin Next Door”** over row 11 | — | (title) | ~2.5 s overlay; house font; **not** full-screen. |
| 11a | 43.58 | 49.00 | NASA | PIA23791 (**use #2 of ≤3**) | push 5% | what the two share | Split former #11. |
| 11b | 49.00 | 55.00 | NASA | Magellan plains PIA00240 | push 5% | size/mass twin lines | New cut — diversify off Mariner. |
| 12a | 55.00 | 60.80 | NASA | **AS17-148-22727** Blue Marble | push 5% | closest thing to a second Earth | |
| 12b | 60.80 | 66.86 | NASA | Magellan Maat / global for scale match-cut | push 5% | same-scale intent Venus↔Earth | |
| 13a | 66.86 | 72.50 | NASA | **SDO 2012 Venus transit** (SVS 3941 / 10996, mute) | native / slow | closer to Sun / almost twice the sunlight | **New free real Venus.** Ties to 022. |
| 13b | 72.50 | 78.20 | NASA | SDO transit continue or still | — | nearer the fire | |
| 13c | 78.20 | 83.84 | **CODE** | `code_graphics.py` → **`albedo`** (awaiting Claude) | — | reflected / absorbed setup | **READY — code_graphics.py on main (`f32afd4`)** — rows #13–#14 family. Do not invent Python. |
| 14a | 83.84 | 90.00 | **CODE** | `albedo` continue / Earth beside Venus text-free | — | three-quarters reflected | **READY — code_graphics.py on main (`f32afd4`)** |
| 14b | 90.00 | 96.00 | NASA | Magellan cloud-top / Mariner **only if** still under 3 uses — prefer Magellan mosaic | push 5% | soaks up less | Prefer Magellan; save Mariner budget. |
| 15a | 96.00 | 102.80 | NASA | Magellan Maat Mons PIA00106 | push 6% | less light in / 465°C | Split former #15. |
| 15b | 102.80 | 109.66 | NASA | Magellan pancake / Alpha Regio **PIA00215** or **PIA00246** | push 5% | paradox | **New Magellan.** |
| 16a | 109.66 | 114.80 | NASA | Magellan plains PIA00240 | push 5% | heat not about light arriving | Split former #16. |
| 16b | 114.80 | 119.96 | NASA | Magellan Ishtar / Maxwell family (**PIA00093** or Magellan Ishtar PIA) | push 5% | cannot get out | **New Magellan.** |
| 17 | 119.96 | 130.00 | NASA | Magellan Sedna / lava perspective | push 5% | dim orange daylight | Orange grade OK (NASA/JPL). |
| 18 | 130.00 | 142.22 | NASA | Magellan low plains / haze | push 5% | never see Sun / slow wind | End chapter surface. |
| 19 | 142.22 | 142.92 | BREATH | — | — | (gap) | 0.7 s. |

### Ch 2 — A Blanket With No Way Out (142.92–223.80) · chalk HOLD cleared via NASA EO/ISS

| # | vo_in | vo_out | source | id | move | VO / beat | notes |
|---:|---:|---:|---|---|---|---|---|
| 20 | 142.92 | 145.50 | CARD | Remotion lower-third **“A Blanket With No Way Out”** over row 21 | — | (title) | ~2.5 s overlay. |
| 20b | 142.92 | 149.02 | NASA | Magellan global + haze | push 5% | air 96% CO₂ | |
| 21a | 149.02 | 154.50 | NASA | Magellan plains PIA00240 | push 5% | greenhouse | Split former #21 (was ~16 s). |
| 21b | 154.50 | 160.00 | NASA | Magellan crater field / plains (harvest PIA) | push 5% | ninety times thicker | |
| 21c | 160.00 | 165.00 | NASA | Magellan PIA00087 family | push 5% | heat in not out | |
| 22 | 165.00 | 177.56 | NASA | Magellan pole–equator mosaic | push 5% | day/night same T | Cut internally ~5–6 s if needed in assemble. |
| 23 | 177.56 | 184.64 | NASA | Magellan → Earth cut | push 5% | Earth has as much CO₂… | |
| 24 | 184.64 | 195.00 | NASA | **NASA EO / ISS White Cliffs of Dover** or **coral reef / carbonate** still | push 5% | limestone, chalk, seabed | **HOLD cleared** — public domain NASA. Credit EO/ISS. |
| 25 | 195.00 | 202.34 | NASA | NASA ocean / water-cycle still | push 5% | rain locks carbon | |
| 26 | 202.34 | 212.74 | NASA | Magellan plains return | push 5% | why no water to put CO₂ away | |
| 27 | 212.74 | 218.76 | CARD/SUB | Remotion subscribe (house) | — | weekly ask | No Vertex. |
| 28 | 218.76 | 223.80 | NASA | Magellan / **ESA Venus Express** still (credit **ESA**) | push 5% | water is the mystery | Prefer Express if harvested. |
| 29 | 223.80 | 224.50 | BREATH | — | — | (gap) | |

### Ch 3 — Where Did the Water Go? (224.50–347.54) · Omni early Venuses + Orbit between; deuterium graphic

| # | vo_in | vo_out | source | id | move | VO / beat | notes |
|---:|---:|---:|---|---|---|---|---|
| 30 | 224.50 | 227.00 | CARD | Remotion lower-third **“Where Did the Water Go?”** | — | (title) | ~2.5 s overlay. |
| 30b | 224.50 | 236.66 | NASA | Pioneer Venus probe/descent art (NASA) | push 5% | 1978 tasted the air | Harvest ID at pull. |
| 31 | 236.66 | 247.48 | **CODE** | `code_graphics.py` → **`deuterium`** (awaiting Claude) | — | heavy H ~100× Earth | **READY — code_graphics.py on main (`f32afd4`)** — rows #31–#32. |
| 32a | 247.48 | 254.00 | **CODE** | `deuterium` continue | — | fingerprint / light H escapes | Split former #32 (~21 s). |
| 32b | 254.00 | 261.00 | NASA | Magellan upper haze / Express | push 5% | Venus lost water | |
| 32c | 261.00 | 268.82 | NASA | Magellan global | push 5% | | |
| 33 | 268.82 | 275.70 | NASA | Magellan global | push 5% | ever an ocean? | |
| 34a | 275.70 | 283.70 | NASA | Magellan slow push | push 4% | spin 243 d retrograde | Split former #34. |
| 34b | 283.70 | 291.78 | NASA | Magellan / Express | push 4% | day longer than year | |
| 35 | 291.78 | 305.00 | **NASA ILLUS.** ~~GENERATE~~ | **`plates_v01/venus_ch3_plateA_ocean_nasa_v01.mp4` 0–13.22 s** (NASA GISS ancient-Venus ocean illustration, Way et al. 2016 release) | slow push, 3 cuts (4.6 / 4.3 / 4.32 s) | Way et al. 2016 | **Plan change per Claude 5984968873:** no Omni (planet starts drift to Jupiter/Mars). Credit **NASA**. £0. |
| 36 | 305.00 | 312.96 | **NASA ILLUS.** | same plate A **13.22–21.18 s** | slow push, 2 cuts (3.96 / 4.0 s) | shallow oceans for billions of years | Same NASA illustration, new framings. £0. |
| 37 | 312.96 | 320.54 | **STILL + HAZE** | **`plates_v02/venus_ch3_row37_plateB_steam_lid_sharp_v02.mp4`** (7.567 s; v02 steam-lid globe, **crisp limb**: texture blurred inside the disc only, haze masked to the disc) | slow push, **2 cuts** (3.80 / 3.77 s) + light drifting haze | Another model / Turbet 2021 | **Per Claude 5985076831:** plate B is a short beat only; sharp edge reads as a planet, not missed focus. Row ends on “found that clouds gathered…” (320.54). Haze in plate is a preview; final haze = Remotion noise. £0. |
| 38 | 320.54 | 331.34 | **CODE** | **`code_graphics.py nightlid`** (main `33a51f3`) → `graphics_v01/nightlid.mp4` **0–10.80 s** of 12 s | — (graphic animates) | clouds gather on the night side, trap heat like a lid; oceans may never have formed | **Per Claude 5985076831:** Turbet beat as code graphic: day side lit, steam rising, cloud building over the night side, heat arrows escape then turn back. Text-free. £0. |
| 39a | 331.34 | 335.06 | **SPLIT** | plate A globe left \| plate B globe right → **`plates_v02/venus_ch3_row39a_split_ocean_vs_steamlid_v02.mp4`** (3.733 s, preview; final split can be a Remotion composite) | slow 4% push both halves, no text | Both are careful models, and they disagree | **Per Claude 5985076831.** Was #39 Omni `orbit_between_two_venus` (dropped 5984886311, both takes drifted). £0. |
| 39b | 335.06 | 338.98 | NASA | Magellan **Alpha Regio tessera PIA00215** → **`plates_v02/venus_ch3_row39b_magellan_alpha_regio_tessera_PIA00215_v02.mp4`** (3.933 s) | push 5% | Nobody has yet read the rocks that could settle it | **Per Claude 5985076831.** Credit NASA/JPL. Row 15b should take **PIA00246** (Alpha Regio east edge) so PIA00215 isn't shown twice. |
| 40 | 338.98 | 347.54 | NASA | Magellan Maat / plains | push 5% | water gone / carbon in sky | Real Venus return. |
| 41 | 347.54 | 348.24 | BREATH | — | — | (gap) | |

### Ch 4 — The Line Earth Hasn't Crossed (348.24–416.88) · line graphic; Orbit→Earth **point**

| # | vo_in | vo_out | source | id | move | VO / beat | notes |
|---:|---:|---:|---|---|---|---|---|
| 42 | 348.24 | 350.92 | CARD | Remotion lower-third **“The Line Earth Hasn't Crossed”** + Blue Marble under | — | why Venus not Earth | Card over first shot. |
| 42b | 348.24 | 350.92 | NASA | Blue Marble | push 5% | | Under card. |
| 43a | 350.92 | 357.00 | **CODE** | `code_graphics.py` → **`line`** (awaiting Claude) | — | distance / vapour / line | **READY — code_graphics.py on main (`f32afd4`)** — rows #43–#44. Split former #43 (~23 s). |
| 43b | 357.00 | 365.00 | **CODE** | `line` continue | — | Venus wrong side | |
| 43c | 365.00 | 373.58 | NASA | Magellan + Earth alternate | push 5% | calm science | No disaster imagery. |
| 44a | 373.58 | 381.70 | NASA | Earth ocean + **022 Sun plate** / SDO | push 5% | Sun brightening | |
| 44b | 381.70 | 389.88 | **CODE** | `line` (Sun brightens; dots) | — | line reaches Earth ~1 Gyr | **READY — code_graphics.py on main (`f32afd4`)** |
| 45a | 389.88 | 396.50 | NASA | Blue Marble calm | push 5% | not next-century warning | Split former #45 (~20 s). |
| 45b | 396.50 | 403.00 | NASA | Blue Marble / ocean | push 5% | fossil-fuel runaway unlikely | |
| 45c | 403.00 | 409.60 | NASA | Magellan calm global | push 5% | Venus is deep time | |
| 46 | 409.60 | 416.88 | **GENERATE — PASS** | Omni **`orbit_looks_back_earth_omni_v01`**, **use 0–5 s only** (`…_t0-5s.mp4`) | — | thin difference | Claude PASS 5984886311: on-model, Earth a blue point, hand-raise at ~frame 4. After ~5 s the push-in fills the frame, so cut out on the wave. |
| 47 | 416.88 | 417.58 | BREATH | — | — | (gap) | |

### Ch 5 — Going Back (417.58–509.58) · no Venera; Magellan plains under lander VO; twilight Venus

| # | vo_in | vo_out | source | id | move | VO / beat | notes |
|---:|---:|---:|---|---|---|---|---|
| 48 | 417.58 | 420.88 | CARD | Remotion lower-third **“Going Back”** over tessera | — | (title) | ~2.5 s. |
| 48b | 417.58 | 420.88 | NASA | Magellan tessera / Maxwell PIA00241 | push 5% | answer on the ground | |
| 49 | 420.88 | 435.48 | NASA | Magellan lava + tessera | push 5% | rocks may remember water | Split in assemble to 4–6 s. |
| 50 | 435.48 | 445.00 | NASA | **Magellan plains** (PIA00240 / PIA00087) under VO | push 5% | people landed / 1982 / two hours | **Venera omitted.** VO only; no lander photo. |
| 51 | 445.00 | 454.82 | NASA | Parker WISPR nightside (NASA/APL/NRL) | push 5% | 2021 night-side glow | Mute if audio. |
| 52 | 454.82 | 465.00 | NASA | DAVINCI → Alpha Regio art | push 5% | NASA missions | No launch-date text on plate. |
| 53 | 465.00 | 475.72 | NASA/ESA | VERITAS art + **EnVision** (credit ESA) | push 5% | map / Europe | |
| 54 | 475.72 | 488.40 | NASA | Magellan Maat Mons PIA00254 | push 6% | clearest record | |
| 55 | 488.40 | 495.12 | NASA | Magellan match-cut (avoid 4th Mariner) | push 5% | twin not monster | Mariner budget exhausted if 3 used. |
| 56 | 495.12 | 505.82 | NASA | **Venus in twilight** NASA HQ / sky photo (public domain) | push 5% | morning/evening star | **New.** Not Magellan globe repeat. |
| 57 | 505.82 | 509.58 | NASA | **PIA00254** Maat Mons still moving | push 6% | next week light-speed clock | **No Orbit on last shot.** |

---

## Generate queue (Claude PASS — in flight)

| Priority | Asset | Model | Prompt lock |
|---:|---|---|---|
| 1 | `venus_early_ocean_cloud_omni_v01` | Vertex Omni | soft light, shallow sea, shining cloud; no cities/life/text |
| 2 | `venus_early_steam_lid_omni_v01` | Vertex Omni | hot dim sky, steam lid, bare rock, no shoreline, no text |
| 3 | ~~`orbit_between_two_venus_omni_v01`~~ **DROPPED** (v01 Jupiter, v02 Mars drift; Claude 5984886311) | Vertex Omni | one Orbit, one face, cream eyes+pupils, no legs, one bottom glow |
| 4 | `orbit_looks_back_earth_omni_v01` | Vertex Omni | **bright blue point of light** (Earth); Venus behind; **not** blue edge |

Paths: `04_Generated-Clips/01_Raw/omni_v01/`. Frame sheets: `…/sheets/*_6frame.jpg`. Report: `07_Edit-Project/omni_gen_report_v01.json`.

---

## Code graphics (Claude — free, no Veo)

| Slot | Function | Rows | Status |
|---|---|---|---|
| `albedo` | sunlight in / reflected / absorbed; Earth beside Venus; text-free | #13–#14 | **RENDERED** `graphics_v01/albedo.mp4` (12 s, 1920x1080, 4 Oct) |
| `deuterium` | water split; light H escapes; heavy share rises | #31–#32 | **RENDERED** `graphics_v01/deuterium.mp4` (12 s, 1920x1080, 4 Oct) |
| `line` | inner limit moves out as Sun brightens; Venus+Earth dots | #43–#44 | **RENDERED** `graphics_v01/line.mp4` (12 s, 1920x1080, 4 Oct) |
| `nightlid` | Turbet 2021: day side lit, steam rising, cloud lid over the night side, heat arrows escape then turn back; text-free | #38 | **RENDERED** `graphics_v01/nightlid.mp4` (12 s; row 38 uses 0–10.80 s) |

Render on Mini when Claude’s file lands; do **not** invent the Python here.

---

## NASA harvest targets (v02)

| Asset | Where | Notes |
|---|---|---|
| Magellan flyover video | JPL / Photojournal movie frames | Frame 0 preferred |
| PIA00254, PIA00106, PIA00240, PIA00241, PIA00087 | photojournal jpeg | Core plains/volcano |
| PIA23791 | Mariner 10 | ≤3 edit uses |
| PIA00215, PIA00246 | Alpha Regio / pancakes | |
| PIA00093 (+ Magellan Ishtar PIAs) | Ishtar | |
| Magellan crater-field PIAs | harvest | |
| SDO 2012 transit | SVS 3941 HD1080 (mute) | |
| ESA Venus Express stills | ESA licence | credit **ESA** |
| NASA EO/ISS White Cliffs or coral reef | EO / ISS gallery | clears chalk HOLD |
| Venus twilight sky photo | NASA HQ | row 56 |
| Parker WISPR, Pioneer, DAVINCI/VERITAS/EnVision | press / SVS | as v01 |
| NASA GISS ancient-Venus ocean illustration (Way et al. 2016 release, 11 Aug 2016) | `nasa.gov/wp-content/uploads/2016/08/ancient-venus-new.jpg` (4096², sha1 696b521b) | rows 35–36; credit **NASA** |

Pool dir: `07_Edit-Project/nasa_pool_v01/` (+ `nasa_pool_v01.json` / `fetch_nasa_pool.py`).

---

## Claude checklist (v02)

- [x] Omni queue PASS with prompt fixes (5982425011)
- [x] Venera omit; row 50 Magellan plains
- [x] Chapter cards = lower-third ~2.5 s; 0.7 s breath; no VO retime
- [x] Long holds split; Mariner ≤3
- [x] Chalk HOLD → NASA EO/ISS
- [ ] Omni frame sheets PASS before edit insert
- [x] `code_graphics.py` landed (`f32afd4`)
- [x] Render albedo/deuterium/line/nightlid on Mini (`04_Generated-Clips/01_Raw/graphics_v01/`, 4 Oct) — slot in assemble
- [ ] Edit assemble after Omni + graphics

---

## Paths

| Artifact | Path |
|---|---|
| This list | `…/023_…/07_Edit-Project/SHOT_LIST_v02.md` |
| v01 | `…/SHOT_LIST_v01.md` |
| Omni mint | `…/_mint_venus_omni_v01.py` |
| Omni out | `…/04_Generated-Clips/01_Raw/omni_v01/` |

*v02 — applies Claude PASS 5982425011. No merge of #99. No £ past free credit.*
