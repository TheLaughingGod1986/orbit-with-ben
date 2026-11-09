# 033 Uranus — Shorts Plan & Slot Schedule (`SHORTS_PLAN_v01.md`)

- **Job:** `J2223` (`macbook` worker · 7 Nov 2026)
- **Parent Long Film:** `033_Why-This-Planet-Has-21-Year-Winters` (*Why Knocked-Sideways Uranus Has 21-Year Winters* · Variant B: *Why This Planet Has 21-Year Winters*)
- **Parent Long Air Slot:** **Wed 9 Dec 2026 at 18:00 Europe/London (`2026-12-09T18:00:00Z`)** (mid-week Wednesday 18:00 London slot per `AGENTS.md` *"Two OWB longs a week (4 Nov 2026)"* and `jobs/reviews/J2023/PLAN.md`)
- **Active Shorts Cap:** **2 Shorts per long** (`AGENTS.md` *"Two OWB longs a week (4 Nov 2026)"*: *"Every long has 2 Shorts, not 3, so two longs a week fit the four Short slots (`Mon/Wed/Fri/Sat 11:30` London, never two Shorts a day)."*)
- **Queued Build Jobs (`jobs/queue.json`):**
  - **Short #1 (Test A Opening Short):** `J2317` (`--film 033 --stage edit --after J2300 --needs mini --kind assembly`)
  - **Short #2 (Keeper Question Short):** `J2318` (`--film 033 --stage edit --after J2300 --needs mini --kind assembly`)
- **Spend / Upload Lock:** **£0 / 0 credits** in `J2223` and in `J2317`/`J2318` (reuses locked `02_Voiceover/uranus_vo_v01.wav`, `033` house music bed, house SFX kit, and `033` plates/code graphics from `J2300`). **No uploads in `J2223` or the build jobs.**

---

## 1. December 2026 Slot Audit (`UPLOADS.json`, `BUFFER_POSTS.json`, `snapshots/2026-11-06.json`, `J2147`)

Checked against `00_Brand/Channel-Setup/social/UPLOADS.json`, `00_Brand/Channel-Setup/social/BUFFER_POSTS.json`, `05_Analytics/owb/snapshots/2026-11-06.json`, and `031`/`032`'s `10_Shorts/SHORTS_PLAN_v01.md` (`J2147`):

1. **`BUFFER_POSTS.json`:** Zero Buffer posts have `dueAt >= 2026-11-15` (all late-Nov and Dec Shorts are `bufferStatus: deferred_7_day_window` in `UPLOADS.json`).
2. **Existing Scheduled YouTube Shorts (`UPLOADS.json` & `snapshots/2026-11-06.json`):** Every `Mon/Wed/Fri 11:30Z` slot from **Mon 30 Nov through Wed 16 Dec 2026** (`8` slots) is already occupied on YouTube by scheduled `028` Gliese 710 (`5` Shorts) and `029` Betelgeuse (`3` Shorts) cuts, and `Sat 05 Dec` / `Sat 12 Dec 11:30Z` are assigned by `J2147` (`031` Path A):

| Date (Europe/London = UTC) | Day & Slot | Status in `UPLOADS.json` / `BUFFER_POSTS.json` / `J2147` | Assigned Video / Plan |
|---|---|---|---|
| `2026-12-02T11:30:00Z` | **Wed 2 Dec 11:30** | **TAKEN (`UPLOADS.json`)** | `028` Short 2 `v6euXX2omz4` (*Is a Star Really Coming Towards Us?*, Test A) |
| `2026-12-02T18:00:00Z` | **Wed 2 Dec 18:00** | **PLANNED (`J2023` / `J2147`)** | **`031` Long** (*What Happens When Earth's Magnetic Field Flips?*) |
| `2026-12-04T11:30:00Z` | **Fri 4 Dec 11:30** | **TAKEN (`UPLOADS.json`)** | `028` Short 3 `BTuL_QBbEgY` (*How Close Will Gliese 710 Come to the Sun?*) |
| `2026-12-05T11:30:00Z` | **Sat 5 Dec 11:30** | **TAKEN (`J2147` `031` Short #1)** | `031` Short #1 (*What Happens When Earth's Magnetic Field Flips?*, Test A) |
| `2026-12-06T18:00:00Z` | **Sun 6 Dec 18:00** | **TAKEN (`UPLOADS.json`)** | **`029` Long** `vP1BbqZ_dnM` (*Is Betelgeuse About to Explode?*) |
| `2026-12-07T11:30:00Z` | **Mon 7 Dec 11:30** | **TAKEN (`UPLOADS.json`)** | `028` Short 4 `lsOCcIYCud0` (*What Will the Night Sky Look Like When Gliese 710 Arrives?*) |
| `2026-12-09T11:30:00Z` | **Wed 9 Dec 11:30** | **TAKEN (`UPLOADS.json`)** | `029` Short 1 `SWDCZfWZVao` (*Why Did Betelgeuse Suddenly Lose Two-Thirds of Its Light?*) |
| `2026-12-09T18:00:00Z` | **Wed 9 Dec 18:00** | **PLANNED (`J2023` / `J2223`)** | **`033` Long** (*Why Knocked-Sideways Uranus Has 21-Year Winters*) |
| `2026-12-11T11:30:00Z` | **Fri 11 Dec 11:30** | **TAKEN (`UPLOADS.json`)** | `029` Short 2 `k2kEaA7ICjc` (*Is Betelgeuse Really About to Explode?*, Test A) |
| `2026-12-12T11:30:00Z` | **Sat 12 Dec 11:30** | **TAKEN (`J2147` `031` Path A)** *(free if `031` uses Path B)* | `031` Short #2 (*What If the Solar Wind Blew Earth's Atmosphere Into Space?*) under `031` Path A; **or `033` Short #1 under Path B** |
| `2026-12-13T18:00:00Z` | **Sun 13 Dec 18:00** | **PLANNED (`J2023` / `J2223`)** | **`034` Long** (*Why Pluto's Frozen Heart Has Zero Craters*) |
| `2026-12-14T11:30:00Z` | **Mon 14 Dec 11:30** | **TAKEN (`UPLOADS.json`)** | `029` Short 3 `heiGCnGKTkE` (*How Bright Will Betelgeuse Get When It Explodes?*) |
| `2026-12-16T11:30:00Z` | **Wed 16 Dec 11:30** | **TAKEN (`UPLOADS.json`)** | `028` Short 5 `f17XCtUmN-g` (*What Happens When Gliese 710 Passes Through the Oort Cloud?*) |
| `2026-12-18T11:30:00Z` | **Fri 18 Dec 11:30** | **FREE (Active Slot)** | **`033` Short #1 (Test A Opening Short — `J2317`, Path A Default)** *(Note: `J2147` listed `Fri 18 Dec` only as an inactive 3rd reserve slot held under the 2-Short cap)* |
| `2026-12-19T11:30:00Z` | **Sat 19 Dec 11:30** | **FREE (Active Slot)** | **`033` Short #2 (Keeper Question Short — `J2318`, Path A Default)** |
| `2026-12-21T11:30:00Z` | **Mon 21 Dec 11:30** | **FREE (Active Slot)** | **`034` Short #1 (Test A Opening Short — `J2319`, Path A Default)** |
| `2026-12-23T11:30:00Z` | **Wed 23 Dec 11:30** | **FREE (Active Slot)** | **`034` Short #2 (Keeper Question Short — `J2320`, Path A Default)** |

---

## 2. Two-Path Slot Assignment for `033` Uranus Shorts

Per `AGENTS.md` Lesson 6 (*"YouTube state changes leave a record"*), workers never alter existing YouTube `publishAt` dates without Chief's explicit order. Both **Path A (Zero-Reschedule Default)** and **Path B (Chief In-Week Swap Option)** are locked below:

### Path A — Default (Zero Reschedule of Existing `UPLOADS.json` IDs or `031` Path A)
- **Active Short #1 (`033_short01_testA_opening`, build job `J2317`):** **Fri 18 Dec 2026 at 11:30 Europe/London (`2026-12-18T11:30:00Z`)**
- **Active Short #2 (`033_short02_ice_giant_surface`, build job `J2318`):** **Sat 19 Dec 2026 at 11:30 Europe/London (`2026-12-19T11:30:00Z`)**
- *Advantages:* Zero YouTube reschedule required; both Shorts air after `033` Long goes public on **Wed 9 Dec 18:00 London**, so the Related-video link and description link to `033` Long are immediately live on day 1; strictly 1 Short per day on `Mon/Wed/Fri/Sat 11:30` London.

### Path B — Chief In-Week Swap Option (Airs Inside `033`'s Air Week)
- If Chief adopts `031` Path B (`Wed 2 Dec` + `Sat 5 Dec 11:30Z` by retiring/shifting `028`'s extra 4th/5th lifts `lsOCcIYCud0` and `f17XCtUmN-g` under the 4 Nov 2-Short cap), **`Sat 12 Dec 2026 11:30Z`** opens inside `033`'s own air week (3 days after `033` Long airs `Wed 9 Dec 18:00Z`):
  - **Active Short #1 (`033_short01_testA_opening`, `J2317`):** **Sat 12 Dec 2026 at 11:30 Europe/London (`2026-12-12T11:30:00Z`)** *(or **Wed 9 Dec 2026 11:30Z** go-public day if Chief also shifts `029` Short 1 `SWDCZfWZVao` to `Fri 18 Dec`)*
  - **Active Short #2 (`033_short02_ice_giant_surface`, `J2318`):** **Fri 18 Dec 2026 at 11:30 Europe/London (`2026-12-18T11:30:00Z`)** *(or **Sat 12 Dec 2026 11:30Z**)*

---

## 3. Active Short #1 — Test A Opening Short (`033_short01_testA_opening` · `J2317`)

- **Slot:** **Fri 18 Dec 2026 11:30 London (`2026-12-18T11:30:00Z`)** [Path A Default] / **Sat 12 Dec 2026 11:30 London** [Path B]
- **Format:** Test A Opening Short (`05_Analytics/tests/SHORTS_TESTS.md` + `LEARNINGS.md` #17: first `30–38 s` of the long master reframed to `9:16`, ending on the central question the long answers so viewers tap the Related video)
- **Title (Listing + `9.0–13.5 s` On-Screen Card):** **Why Does Knocked-Sideways Uranus Have 21-Year Winters?**
  - *Alt Title:* *What Would You See at the North Pole of Knocked-Sideways Uranus?*
- **Frame-0 Hook Caption (`0.00–2.00 s`):** `21-YEAR **NIGHT**` (yellow word `NIGHT`, distinct from standalone Short `ZpEA8stoSPA`'s `21-YEAR **WINTER**`)
- **Frame-0 Visual (`0.00 s`, Non-Overlapping with `ZpEA8stoSPA`):**
  - Native moving Hubble rotation time-lapse of sideways Uranus (`PIA01283` + `PIA01280` from `SHOT_LIST_v01.md` Row `R01`, graded on `#050814` navy space).
  - Zero overlap with standalone Short `ZpEA8stoSPA` (*Why Does Knocked-Sideways Uranus Have 21-Year Winters?*, aired Sat 31 Oct), which opened on `svs20390_shot9_beauty_rings.mp4`.
  - No Orbit at frame 0, cover, or end frame.
- **Spoken VO Lift (`02_Voiceover/uranus_vo_v01.wav`, Scribe-aligned from `SHOT_LIST_v01.md`):**
  - `R01` (`0.100–4.059 s`): *"At the North Pole of Uranus, the seventh planet in orbit around our sun,"*
  - `R02` (`4.640–7.780 s`): *"what would you see when the sun sinks below the horizon?"*
  - `R03` (`8.580–12.760 s`): *"A single winter night that lasts twenty-one Earth years."*
  - `R04` (`13.980–17.700 s`): *"While Earth spins at a twenty-three point four four degree tilt,"*
  - `R05` (`18.240–24.800 s`): *"Uranus is tipped at ninety-seven point seven seven degrees, more than four times Earth's tilt,"*
  - `R06` (`25.260–30.980 s`): *"and nearly at a right angle to its orbit, rolling around the sun on its side like a ball."*
  - `R09` central question (`49.320–53.300 s`, per `LEARNINGS.md` #17): *"How did an entire giant planet get knocked onto its side?"* *(or contiguous `R01`–`R07` `0.100–38.440 s` pause-trimmed to `~35.5–37.0 s`)*.
  - **Runtime:** **`34.5–36.5 s`** (`82 spoken words`, inside the `30–38 s` Test A window, cut cleanly in a Scribe pause).
- **Single Teach Overlay (`18.2–22.0 s`, inside 16:9 centre band, `11–12%` height, clear of `0–2 s` and `9–14 s` title):**
  - `DATA: URANUS TILT: 97.77° (> 4× EARTH)` (`code_graphic_033_r05_tilt_gauge.mp4`).
- **Related Video & Description:** Links to `033` Long (*Why Knocked-Sideways Uranus Has 21-Year Winters*). Zero `/go` affiliate links.

---

## 4. Active Short #2 — Keeper Question Short (`033_short02_ice_giant_surface` · `J2318`)

- **Slot:** **Sat 19 Dec 2026 11:30 London (`2026-12-19T11:30:00Z`)** [Path A Default] / **Fri 18 Dec 2026 11:30 London** [Path B]
- **Format:** Keeper-Score Question Short (`22–27 s`, `51–64 words`, one question in title and Line 1, single Teach overlay inside 16:9 band)
- **Title (Listing + `9.0–13.5 s` On-Screen Card):** **What Happens If a Spacecraft Tries to Land on Ice Giant Uranus?**
- **Frame-0 Hook Caption (`0.00–2.00 s`):** `NO **SURFACE**` (yellow word `SURFACE`)
- **Frame-0 Visual (`0.00 s`):**
  - Native moving push into Uranus's swirling cyan-teal cloud deck (`PIA00142` / `stsci-h-p1906c-f-514x514.a` from `SHOT_LIST_v01.md` Rows `R49`/`R51`, distinct from `033` Short #1 and standalone Short `ZpEA8stoSPA`). No Orbit at frame 0, cover, or end frame.
- **Spoken VO Lift (`02_Voiceover/uranus_vo_v01.wav`, Scribe-aligned Ch 5 lift):**
  - `R49` (`438.584–443.944 s`, `5.36 s`): *"What happens if a spacecraft dives beneath those clouds to land on the ice below?"* (**Literal spoken question in Line 1**)
  - `R51` (`459.704–463.164 s`, `3.46 s`): *"As an ice giant, Uranus has no true surface."*
  - `R52` (`463.844–476.984 s`, `13.14 s`): *"Beneath the hydrogen and helium clouds, 80% or more of the planet's mass is a hot, dense fluid of water, methane, and ammonia above a small rocky core."*
  - `R53` (`477.824–486.904 s`, optional pause-trimmed payoff): *"Near that core, Uranus heats up to 9,000 degrees Fahrenheit, 4,982 degrees Celsius."*
  - **Runtime:** **`24.5–26.5 s`** (`51–64 spoken words`, inside the `22–27 s` Keeper window).
- **Single Teach Overlay (`15.0–18.8 s`, inside 16:9 centre band, `11–12%` height, clear of `0–2 s` and `9–14 s` title):**
  - `DATA: ≥ 80% HOT DENSE FLUID` (`code_graphic_033_r52_interior_mantle.mp4`).
- **Related Video & Description:** Links to `033` Long (*Why Knocked-Sideways Uranus Has 21-Year Winters*). Zero `/go` affiliate links.

---

## 5. Reserve Short #3 (Held Under 4 Nov 2-Short Cap — Ch 6 Miranda Lift)

Held inactive per the 4 Nov 2026 two-Shorts-per-long cap (available as an instant zero-spend alternate for Short #2 if preferred at review):
- **Slug:** `033_short03_miranda_cliff_drop`
- **Title:** **Why Would a Rock Take 10 Minutes to Fall Off a Cliff on Uranus's Moon Miranda?**
- **Hook Caption (`0.00–2.00 s`):** `10-MINUTE **FALL**`
- **Frame-0 Visual:** Voyager 2 high-resolution view of Miranda's towering fault scarp (`PIA00044` / `PIA00141` from `R62`).
- **Spoken VO Lift (`02_Voiceover/uranus_vo_v01.wav`, Scribe-aligned Ch 6 lift `541.624–569.344 s`):**
  - `R60` (`541.624–551.524 s`): *"When Voyager 2 flew past in January 1986, Miranda looked like Frankenstein's monster pieced together from parts that did not merge properly."*
  - `R61` (`552.504–559.864 s`): *"Carving across its surface are giant fault canyons as much as 12 times as deep as Earth's Grand Canyon."*
  - `R62` (`560.904–569.344 s`): *"Because of Miranda's low gravity and towering cliffs, a rock dropped off the highest cliff would take 10 minutes to reach the foot of the cliff."*
  - **Runtime:** **`25.5 s`** (`54 words`, pause-trimmed with `< 1.0 s` loop tail).
- **Single Teach Overlay (`15.0–18.8 s`):** `DATA: 10-MINUTE CLIFF DROP (12× GRAND CANYON)` (`code_graphic_033_r61_canyon_depth_scale.mp4`).

---

## 6. `OWB-2026-11-E1` + Keeper + House Gates Checklist (`J2317` & `J2318`)

- **Pacing (`OWB-2026-11-E1`, `LEARNINGS.md` #15–16):** `Cut 1 <= 2.8 s`, `Cut 2 <= 4.8 s`, moving frame 0, visual surprise `<= 1.5 s`, zero meta-promise (`"Stay and I'll show you..."`) or spoken CTA, loop tail `< 1.2 s`, no `3.5–5.5 s` post-sentence-1 pause.
- **No Reuse vs Standalone Short `ZpEA8stoSPA`:** Frame 0, hook caption, and cut sequence are 100% distinct from `ZpEA8stoSPA` (`gate_shorts_open.py check` enforces `< 0.90` pHash against the last 10 Shorts).
- **Tool Gates Required Before Review:** `gate_shorts_open.py check`, `picture_qa.py`, `polish_gate.py`, `sfx_kit.py level`, `thumb_preview.py short`.
