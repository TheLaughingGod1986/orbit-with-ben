# 034 Pluto — Shorts Plan & Slot Schedule (`SHORTS_PLAN_v01.md`)

- **Job:** `J2223` (`macbook` worker · 7 Nov 2026)
- **Parent Long Film:** `034_Why-Plutos-Frozen-Heart-Has-Zero-Craters` (*Why Pluto's Frozen Heart Has Zero Craters* · Variant B: *What New Horizons Found Inside Pluto's Heart*)
- **Parent Long Air Slot:** **Sun 13 Dec 2026 at 18:00 Europe/London (`2026-12-13T18:00:00Z`)** (Sunday 18:00 London slot per `AGENTS.md` *"Two OWB longs a week (4 Nov 2026)"* and `jobs/reviews/J2023/PLAN.md`)
- **Active Shorts Cap:** **2 Shorts per long** (`AGENTS.md` *"Two OWB longs a week (4 Nov 2026)"*: *"Every long has 2 Shorts, not 3, so two longs a week fit the four Short slots (`Mon/Wed/Fri/Sat 11:30` London, never two Shorts a day)."*)
- **Queued Build Jobs (`jobs/queue.json`):**
  - **Short #1 (Test A Opening Short):** `J2319` (`--film 034 --stage edit --after J2157 --needs mini --kind assembly`)
  - **Short #2 (Keeper Question Short):** `J2320` (`--film 034 --stage edit --after J2157 --needs mini --kind assembly`)
- **Spend / Upload Lock:** **£0 / 0 credits** in `J2223` and in `J2319`/`J2320` (reuses locked `034` VO from `J2157`, `034` house music bed, house SFX kit, and `034` plates/code graphics once built). **No uploads in `J2223` or the build jobs.**

---

## 1. December 2026 Slot Audit (`UPLOADS.json`, `BUFFER_POSTS.json`, `snapshots/2026-11-06.json`, `J2147`, `033` Plan)

Checked against `00_Brand/Channel-Setup/social/UPLOADS.json`, `00_Brand/Channel-Setup/social/BUFFER_POSTS.json`, `05_Analytics/owb/snapshots/2026-11-06.json`, `031`/`032`'s `10_Shorts/SHORTS_PLAN_v01.md` (`J2147`), and `033`'s `10_Shorts/SHORTS_PLAN_v01.md`:

1. **`BUFFER_POSTS.json`:** Zero Buffer posts have `dueAt >= 2026-11-15` (all late-Nov and Dec Shorts are `bufferStatus: deferred_7_day_window` in `UPLOADS.json`).
2. **Existing Scheduled YouTube Shorts (`UPLOADS.json` & `snapshots/2026-11-06.json`):** Every `Mon/Wed/Fri 11:30Z` slot from **Mon 30 Nov through Wed 16 Dec 2026** (`8` slots) is already occupied on YouTube by scheduled `028` Gliese 710 (`5` Shorts) and `029` Betelgeuse (`3` Shorts) cuts, `Sat 05 Dec` / `Sat 12 Dec 11:30Z` are assigned by `J2147` (`031` Path A), and `Fri 18 Dec` / `Sat 19 Dec 11:30Z` are assigned to `033` Uranus under Path A:

| Date (Europe/London = UTC) | Day & Slot | Status in `UPLOADS.json` / `BUFFER_POSTS.json` / `J2147` / `033` | Assigned Video / Plan |
|---|---|---|---|
| `2026-12-09T18:00:00Z` | **Wed 9 Dec 18:00** | **PLANNED (`J2023` / `J2223`)** | **`033` Long** (*Why Knocked-Sideways Uranus Has 21-Year Winters*) |
| `2026-12-11T11:30:00Z` | **Fri 11 Dec 11:30** | **TAKEN (`UPLOADS.json`)** | `029` Short 2 `k2kEaA7ICjc` (*Is Betelgeuse Really About to Explode?*, Test A) |
| `2026-12-12T11:30:00Z` | **Sat 12 Dec 11:30** | **TAKEN (`J2147` `031` Path A)** *(or `033` Short #1 under Path B)* | `031` Short #2 (*What If the Solar Wind Blew Earth's Atmosphere Into Space?*) |
| `2026-12-13T18:00:00Z` | **Sun 13 Dec 18:00** | **PLANNED (`J2023` / `J2223`)** | **`034` Long** (*Why Pluto's Frozen Heart Has Zero Craters*) |
| `2026-12-14T11:30:00Z` | **Mon 14 Dec 11:30** | **TAKEN (`UPLOADS.json`)** | `029` Short 3 `heiGCnGKTkE` (*How Bright Will Betelgeuse Get When It Explodes?*) |
| `2026-12-16T11:30:00Z` | **Wed 16 Dec 11:30** | **TAKEN (`UPLOADS.json`)** | `028` Short 5 `f17XCtUmN-g` (*What Happens When Gliese 710 Passes Through the Oort Cloud?*) |
| `2026-12-18T11:30:00Z` | **Fri 18 Dec 11:30** | **TAKEN (`033` Short #1 Path A)** | `033` Short #1 (*Why Does Knocked-Sideways Uranus Have 21-Year Winters?*, `J2317`) |
| `2026-12-19T11:30:00Z` | **Sat 19 Dec 11:30** | **TAKEN (`033` Short #2 Path A)** *(or `034` Short #1 under Path B)* | `033` Short #2 (*What Happens If a Spacecraft Tries to Land on Ice Giant Uranus?*, `J2318`) |
| `2026-12-21T11:30:00Z` | **Mon 21 Dec 11:30** | **FREE (Active Slot)** | **`034` Short #1 (Test A Opening Short — `J2319`, Path A Default)** |
| `2026-12-23T11:30:00Z` | **Wed 23 Dec 11:30** | **FREE (Active Slot)** | **`034` Short #2 (Keeper Question Short — `J2320`, Path A Default)** |

---

## 2. Two-Path Slot Assignment for `034` Pluto Shorts

Per `AGENTS.md` Lesson 6 (*"YouTube state changes leave a record"*), workers never alter existing YouTube `publishAt` dates without Chief's explicit order. Both **Path A (Zero-Reschedule Default)** and **Path B (Chief In-Week Swap Option)** are locked below:

### Path A — Default (Zero Reschedule of Existing `UPLOADS.json` IDs or `031` Path A)
- **Active Short #1 (`034_short01_testA_opening`, build job `J2319`):** **Mon 21 Dec 2026 at 11:30 Europe/London (`2026-12-21T11:30:00Z`)**
- **Active Short #2 (`034_short02_charon_locked_sky`, build job `J2320`):** **Wed 23 Dec 2026 at 11:30 Europe/London (`2026-12-23T11:30:00Z`)**
- *Advantages:* Zero YouTube reschedule required; both Shorts air after `034` Long goes public on **Sun 13 Dec 18:00 London**, so the Related-video link and description link to `034` Long are immediately live on day 1; strictly 1 Short per day on `Mon/Wed/Fri/Sat 11:30` London.

### Path B — Chief In-Week Swap Option (Airs Inside `034`'s Post-Air Week)
- If `033` uses Path B (`Sat 12 Dec` + `Fri 18 Dec 11:30Z`), **`Sat 19 Dec 2026 11:30Z`** opens inside the week immediately following `034` Long's `Sun 13 Dec 18:00Z` release (and if Chief retires/shifts `028`'s 5th lift `f17XCtUmN-g` from `Wed 16 Dec 11:30Z` under the 4 Nov 2-Short cap, `Wed 16 Dec` + `Fri 18 Dec` or `Sat 19 Dec` + `Mon 21 Dec` open):
  - **Active Short #1 (`034_short01_testA_opening`, `J2319`):** **Sat 19 Dec 2026 at 11:30 Europe/London (`2026-12-19T11:30:00Z`)** *(or **Wed 16 Dec 2026 11:30Z** if Chief retires/shifts `028` 5th lift `f17XCtUmN-g`)*
  - **Active Short #2 (`034_short02_charon_locked_sky`, `J2320`):** **Mon 21 Dec 2026 at 11:30 Europe/London (`2026-12-21T11:30:00Z`)** *(or **Fri 18 Dec / Sat 19 Dec 2026 11:30Z**)*

---

## 3. Active Short #1 — Test A Opening Short (`034_short01_testA_opening` · `J2319`)

- **Slot:** **Mon 21 Dec 2026 11:30 London (`2026-12-21T11:30:00Z`)** [Path A Default] / **Sat 19 Dec 2026 11:30 London** [Path B]
- **Format:** Test A Opening Short (`05_Analytics/tests/SHORTS_TESTS.md` + `LEARNINGS.md` #17: first `30–38 s` of the long master reframed to `9:16`, ending on the central question the long answers so viewers tap the Related video)
- **Title (Listing + `9.0–13.5 s` On-Screen Card):** **What Did New Horizons Discover Inside Pluto's Frozen Heart?**
  - *Alt Title:* *Why Does Pluto's Frozen Heart Have Zero Impact Craters?*
- **Frame-0 Hook Caption (`0.00–2.00 s`):** `ZERO **CRATERS**` (yellow word `CRATERS`, distinct from standalone Short `gmzaCfJF1gA`'s `NO **CRATERS**`)
- **Frame-0 Visual (`0.00 s`, Non-Overlapping with `gmzaCfJF1gA`):**
  - Native moving New Horizons LORRI/MVIC low-angle aerial sweep across Sputnik Planitia's polygonal nitrogen-ice cells (`PIA19857` / `PIA20016` / `PIA19952` northern cellular plain crop).
  - Zero overlap with standalone Short `gmzaCfJF1gA` (*Why Does Pluto's Frozen Heart Have Zero Craters?*, airs Tue 10 Nov 2026), which opens on full-disc `PIA19708`.
  - No Orbit at frame 0, cover, or end frame.
- **Spoken VO Lift (`034` VO master from `J2157`, Cold Open lines from `pluto_frozen_heart_script_master_v02.md`):**
  - *"On 14 July 2015, when NASA's New Horizons spacecraft flew within twelve thousand five hundred kilometers of Pluto, what did its cameras reveal inside the dwarf planet's bright heart-shaped basin? Across the vast nitrogen-ice plains of Sputnik Planitia, scientists counted zero detectable impact craters. In a rugged Kuiper Belt battered by four billion years of comet impacts, that smooth basin cannot be more than ten million years old… What is erasing the craters inside Pluto's frozen heart?"*
  - **Runtime:** **`33.5–36.5 s`** (`83 spoken words`, pause-trimmed inside the `30–38 s` Test A window, ending on the central question `034` answers per `LEARNINGS.md` #17).
- **Single Teach Overlay (`15.0–18.8 s`, inside 16:9 centre band, `11–12%` height, clear of `0–2 s` and `9–14 s` title):**
  - `DATA: ZERO IMPACT CRATERS (≤ 10 MILLION YRS OLD)`.
- **Related Video & Description:** Links to `034` Long (*Why Pluto's Frozen Heart Has Zero Craters*). Zero `/go` affiliate links.

---

## 4. Active Short #2 — Keeper Question Short (`034_short02_charon_locked_sky` · `J2320`)

- **Slot:** **Wed 23 Dec 2026 11:30 London (`2026-12-23T11:30:00Z`)** [Path A Default] / **Mon 21 Dec 2026 11:30 London** [Path B]
- **Format:** Keeper-Score Question Short (`22–27 s`, `59 words`, one question in title and Line 1, single Teach overlay inside 16:9 band)
- **Title (Listing + `9.0–13.5 s` On-Screen Card):** **Why Does Pluto's Giant Moon Charon Never Rise or Set?**
- **Frame-0 Hook Caption (`0.00–2.00 s`):** `FROZEN IN THE **SKY**` (yellow word `SKY`)
- **Frame-0 Visual (`0.00 s`):**
  - Native moving New Horizons Pluto–Charon crescent/family view (`PIA19968` / `PIA19966` high-resolution Charon globe hanging motionless over Pluto's horizon — zero overlap with `034` Short #1 or standalone Short `gmzaCfJF1gA`). No Orbit at frame 0, cover, or end frame.
- **Spoken VO Lift (`034` VO master from `J2157`, Ch 2 *The Moon That Never Moves* from `pluto_frozen_heart_script_master_v02.md`):**
  - *"Why does Pluto's largest moon hang frozen in one spot in the sky? Discovered in 1978, Charon is about twelve hundred kilometers across, roughly half the size of Pluto itself, making it the largest known moon relative to its parent body in our solar system. Both worlds are tidally locked, so Charon never rises or sets."* (**Literal spoken question in Line 1**)
  - **Runtime:** **`24.0–25.5 s`** (`59 spoken words`, inside the `22–27 s` Keeper window).
- **Single Teach Overlay (`15.0–18.8 s`, inside 16:9 centre band, `11–12%` height, clear of `0–2 s` and `9–14 s` title):**
  - `DATA: CHARON = 1/2 PLUTO WIDTH` (`1,212 KM vs 2,376 KM`).
- **Related Video & Description:** Links to `034` Long (*Why Pluto's Frozen Heart Has Zero Craters*). Zero `/go` affiliate links.

---

## 5. Reserve Short #3 (Held Under 4 Nov 2-Short Cap — Ch 5 Water-Ice Mountains Lift)

Held inactive per the 4 Nov 2026 two-Shorts-per-long cap (available as an instant zero-spend alternate for Short #2 if preferred at review):
- **Slug:** `034_short03_water_ice_mountains`
- **Title:** **Why Are Pluto's 3-Kilometre Mountains Made of Water Ice?**
- **Hook Caption (`0.00–2.00 s`):** `ICE **MOUNTAINS**`
- **Frame-0 Visual:** New Horizons close-up of the rugged water-ice peaks of Norgay Montes / Hillary Montes bordering Sputnik Planitia (`PIA19856` / `PIA19948`).
- **Spoken VO Lift (`034` VO master from `J2157`, Ch 5 *Mountains Made of Water Ice* from `pluto_frozen_heart_script_master_v02.md`):**
  - *"How can towering mountains stand beside a shifting glacier of nitrogen ice? Bordering the western edge of Sputnik Planitia rise jagged peaks two to three kilometers high, comparable to the Rocky Mountains on Earth. Nitrogen and methane ice are far too soft to support mountains that tall, so Pluto's mountains must be built from a bedrock of solid water ice."*
  - **Runtime:** **`24.0 s`** (`58 spoken words`).
- **Single Teach Overlay (`15.0–18.8 s`):** `DATA: 2 TO 3 KM WATER-ICE PEAKS`.

---

## 6. `OWB-2026-11-E1` + Keeper + House Gates Checklist (`J2319` & `J2320`)

- **Pacing (`OWB-2026-11-E1`, `LEARNINGS.md` #15–16):** `Cut 1 <= 2.8 s`, `Cut 2 <= 4.8 s`, moving frame 0, visual surprise `<= 1.5 s`, zero meta-promise (`"Stay and I'll show you..."`) or spoken CTA, loop tail `< 1.2 s`, no `3.5–5.5 s` post-sentence-1 pause.
- **No Reuse vs Standalone Short `gmzaCfJF1gA`:** Frame 0, hook caption, and cut sequence are 100% distinct from `gmzaCfJF1gA` (`gate_shorts_open.py check` enforces `< 0.90` pHash against the last 10 Shorts).
- **Tool Gates Required Before Review:** `gate_shorts_open.py check`, `picture_qa.py`, `polish_gate.py`, `sfx_kit.py level`, `thumb_preview.py short`.
