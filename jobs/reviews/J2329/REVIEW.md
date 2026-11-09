# J2329 — Weekly Cadence Calendar-Gap Readback for Both Channels (7 Nov 2026 – 10 Jan 2027)

- **Job:** `J2329` (`Weekly cadence calendar-gap readback for both channels`)
- **Kind / Repo:** `review` · `owb` (covers `@OrbitWithBen` and `@HistoryOfScienceYT`)
- **Agent:** `macbook` (7 November 2026)
- **Spend & Mutations:** **£0.00 / 0 credits.** Read-only calendar-gap check against the locked weekly publish cadence (Ben, 7 Nov 2026; commits `a7f77f52` in `orbit-with-ben` and `014b707c` in `history-of-science`). Zero uploads, zero YouTube/Studio changes, zero `UPLOADS.json` edits, and zero placeholder publishes proposed.
- **Evidence Sources Read:**
  - `05_Analytics/owb/snapshots/2026-11-06.json` and `05_Analytics/hos/snapshots/2026-11-06.json`
  - `00_Brand/Channel-Setup/social/UPLOADS.json` and `00_Brand/Channel-Setup/social/hos/UPLOADS.json`
  - `gate_shorts_open.py list` in both `orbit-with-ben` and `history-of-science`
  - `05_Analytics/kanban/film_briefs.json`, `jobs/WIP.json`, `00_Brand/Channel-Setup/VIDEO_BACKLOG.json` (OWB & HOS), and `00_Brand/Channel-Setup/PIPELINE.json` (HOS)
  - Queue jobs and plans: `J2023` (`jobs/reviews/J2023/PLAN.md`), `J2147` (`031`/`032` `10_Shorts/SHORTS_PLAN_v01.md`), `J2168`–`J2175`, `J2223` (PR #600), `J2228`, `J2229`, `J2230`, `J2231`, `J2239`, `J2240`, `J2248` (`jobs/reviews/J2248/REVIEW.md`, `J2283`, `J2302`), `J2259`, `J2272`, `J2273`, `J2317`–`J2320`, and `J2326`–`J2328`.

---

## 1. Locked Weekly Cadence Reference (Ben, 7 Nov 2026)

| Channel | Longs Cadence (UK / London) | Shorts Cadence (UK / London) | Standing Constraints |
|---|---|---|---|
| **Orbit With Ben** (`@OrbitWithBen`) | **2/week:** **Sunday 18:00** & **Wednesday 18:00** (normal publish, no Premiere; first Wednesday longs remain `032` Titan on **Wed 25 Nov 2026** and `031` Magnetic Field on **Wed 2 Dec 2026**) | **4/week:** **Monday, Wednesday, Friday, Saturday 11:30** | **2 Shorts per new long** (one is Test A's opening Short while Test A runs; films whose Shorts already exist keep them). Never two Shorts on the same day. Never a Short before its own long is public. Ready approved cuts only — no placeholders. |
| **History of Science** (`@HistoryOfScienceYT`) | **1/week:** **Thursday 18:00** (normal publish, no Premiere) | **4/week:** **Saturday, Friday, Sunday, Tuesday 11:30** | **Saturday 11:30** is the go-public-day Short slot for the new Thursday long because Thursday 11:30 would air 6.5 h *before* that day's 18:00 long. Never two Shorts on the same day. Never a Short before its own long is public. Ready approved cuts only — no placeholders. |

*(Note: Between 7 November 2026 and 10 January 2027, UK / `Europe/London` time is on GMT, i.e. `UTC+00:00`.)*

---

## 2. Mandatory Flags & Specific Rulings

### A. Already-Scheduled Shorts on Off-Pattern Days (Leave Where They Are — Listed Only)

Per the brief, already-scheduled Shorts sitting on off-pattern days are **left untouched** in their current YouTube `publishAt` slots:

#### Orbit With Ben (Pattern Days: `Mon · Wed · Fri · Sat 11:30`)
1. **Tue 10 Nov 2026 11:30Z (`Tue` — off-pattern):** `ffYKoNVPoqg` — *What Would Standing on Saturn's Moon Titan Feel Like?* (`19 s`, standalone test Short S6 `v11`, swapped in by `J2259` replacing `RLSJm59OSzI`). Leave in place.
2. **Thu 12 Nov 2026 11:30Z (`Thu` — off-pattern):** `N42gKBbD7tE` — *How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years?* (`55 s`, `025` Mars Chief-OK'd 50–60 s length-test Short, `AGENTS.md` Packaging §5). Leave in place.
3. **Tue 17 Nov 2026 11:30Z (`Tue` — off-pattern):** `kKN8Ale42sE` — *How Far From Earth Is Voyager 1 Right Now?* (`21 s`, standalone test Short S5). Leave in place.

#### History of Science (Pattern Days: `Sat · Fri · Sun · Tue 11:30`)
*(Historical note: `xHnIi9GqOsM` — *Why Do Veins Have Valves?*, `005` Short, already aired public on off-pattern **Thu 5 Nov 2026 11:30Z**.)*
Upcoming scheduled Private Shorts on off-pattern days:
1. **Mon 16 Nov 2026 11:30Z (`Mon` — off-pattern):** `xzKoHg0E0_U` — *What Is Dalton's Atomic Theory?* (`25 s`, `004` Atom Short). Leave in place.
2. **Wed 18 Nov 2026 11:30Z (`Wed` — off-pattern):** `ChbsigHD5_o` — *How Do Plants Clean the Air?* (`24.25 s`, `006` Willow Short B `v02`, uploaded Private on 6 Nov at `08:58Z` in `J2272` under the pre-7 Nov `Mon/Wed/Fri/Sat` fallback instruction; registered in `00_Brand/Channel-Setup/social/hos/UPLOADS.json`). Leave in place.

*(Unscheduled conditional HOS target dates in `J2023` that also sit on off-pattern days because `J2023` was drafted on 5 Nov before the 7 Nov `Sat/Fri/Sun/Tue` lock: **Mon 30 Nov 11:30Z** [`009` Short B in `J2171`], **Wed 2 Dec 11:30Z** [`008` Short C in `J2170`/`J2175`], **Mon 7 Dec 11:30Z** [`010` Short C in `J2172`], and **Thu 10 Dec 11:30Z** [`005` s07 reserve, already rejected in `J2168`]. Since none of those four is uploaded or scheduled, they should target adjacent free HOS pattern days — **Sat 28 Nov / Sun 29 Nov / Tue 1 Dec** and **Sat 5 Dec / Sun 6 Dec / Tue 8 Dec** — if and when their cuts pass gates and Ben's watch.)*

---

### B. `J2248` (`024` Muons Short — *Muons Shouldn't Reach the Ground. They Do.*) Slot Conflict & Proposed Free Pattern Day

- **Conflict Flagged:** `J2248` (`status: blocked`, with `v03` under review in `J2302`) still carries `(target Mon 9 Nov 11:30 if free)` in its title/brief. **Monday 9 November 2026 at 11:30 London is NOT free** — it is occupied by scheduled `025` Mars Short `iyvWYFP_ETA` (*Could a Robot Survive a Night on Mars?*, `publishAt: 2026-11-09T11:30:00Z`). Under the one-Short-per-day lock, `J2248` **must not** take Mon 9 Nov 11:30.
- **Parent Long Readiness:** Parent long `024` (`rVqgtkBV3jc` — *What Happens If You Travel Near Light Speed?*) has been **public since Sun 1 Nov 2026 18:00Z**, so `J2248` has no parent-long hold once `J2302` (`v03` review) and Ben's final watch clear.
- **Proposed Free Pattern Day (`Mon/Wed/Fri/Sat 11:30 London`):**
  1. **Primary Recommendation — Saturday 21 November 2026 at 11:30 London (`2026-11-21T11:30:00Z`):**
     - First completely free OWB pattern slot from today onward (all `Mon/Wed/Fri/Sat` slots in 7–20 Nov are already occupied on YouTube: Sat 7 Nov `T9fVlG3CCzU`, Mon 9 Nov `iyvWYFP_ETA`, Wed 11 Nov `B1z2dv7m7Vk`, Fri 13 Nov `bSjWiCbB7pY`, Sat 14 Nov `gmzaCfJF1gA`, Mon 16 Nov `HZGTovJu_TQ`, Wed 18 Nov `cwU_0WWeNZ4`, Fri 20 Nov `aAUgIGEuPwQ`).
     - Zero collision with `032` Titan or the `AR` cohort, and `gate_shorts_open.py check --air-date 2026-11-21` already passed in `J2283`.
  2. **Fallback Free Pattern Days (if `J2248` clears Ben's watch after 21 Nov):**
     - **Wednesday 25 November 2026 at 11:30 London (`2026-11-25T11:30:00Z`)** — open on YouTube, and `032` Titan Short 1 cannot use it (see Flag C below); available if `AR2` (`J2229` fix) does not take it.
     - **Saturday 5 December 2026 at 11:30 London** or **Saturday 12 December 2026 at 11:30 London** (whichever slot is not used by `031` Magnetic Field).

---

### C. `J2147` (`031` Magnetic Field & `032` Titan Shorts Plan) Flagged Against Locked Rules

1. **Violation of "Never a Short Before Its Own Long Is Public" (`Wed 25 Nov 11:30` and `Wed 2 Dec 11:30` Path B):**
   - **Titan (`032`):** `J2147` (`032/10_Shorts/SHORTS_PLAN_v01.md`) planned `032` Active Short #1 (*What Happens If You Strike a Match on Titan?*, `23.64 s`) at **Wednesday 25 November 2026 11:30 London**, which is **6.5 hours before** the `032` Titan long goes public at **Wednesday 25 November 2026 18:00 London**. That violates the locked rule (*"never a Short before its own long is public"* — the exact reason HOS uses Saturday 11:30 instead of Thursday 11:30 for a Thursday 18:00 long).
   - **Resolution for `032`:** `J2147` already noted **Saturday 28 November 2026 at 11:30 London** as a fallback if `AR2` held Wed 25 Nov 11:30. Under the locked rule, **no `032` Short may air at Wed 25 Nov 11:30**. `032`'s two Shorts (`fri27_opening_testA` and `wed25_strike_match`) must air *after* Wed 25 Nov 18:00 — specifically **Friday 27 November 11:30** and **Saturday 28 November 11:30** (or, where `AR1` [`J2228`, Ben-approved for Fri 27 Nov 11:30] and/or `AR3` [`J2229`] occupy Fri 27 / Sat 28 Nov, the open slot of Fri 27 / Sat 28 Nov plus the next free Saturday slot).
   - **Magnetic Field (`031` Path B):** `J2147` (`031/10_Shorts/SHORTS_PLAN_v01.md`) recorded a "Path B" option where Chief would shift `028`'s scheduled `v6euXX2omz4` off **Wednesday 2 December 2026 11:30 London** so `031` Short 1 could air at **Wed 2 Dec 11:30 London** — which is also **6.5 hours before** `031`'s long at **Wed 2 Dec 18:00 London**, and would move an already-scheduled `028` Short. **Flag & reject `031` Path B.** Keep `031` on **Path A** (**Saturday 5 December 11:30** and **Saturday 12 December 11:30**, both *after* the Wed 2 Dec 18:00 long goes public, with zero changes to `028`/`029`).
2. **Violation of the Two-Short Cap for New Longs (`J2147` Planned Three Shorts per Film):**
   - `J2147` scripted and slotted **three** Shorts for `032` (`Active #1` match, `Active #2` Test A opening, `Reserve #3` 28× easier to fly) and **three** Shorts for `031` (`Active #1` Test A opening, `Active #2` solar wind vs air, `Reserve #3` worldwide auroras).
   - Under the locked weekly cadence (`AGENTS.md` line 473, Ben 7 Nov 2026), **each new OWB long is capped at two Shorts** (one Test A opening Short + one Keeper question Short; only earlier films whose Shorts already exist keep more than two).
   - **Resolution:** Do not build or schedule the 3rd Short for `032` (`032_short_sat28_flying_28x_v01.mp4`) or the 3rd Short for `031` (`031_short_fri18_aurora_many_poles_v01.mp4`). Keeping `031` Short 3 unscheduled also leaves **Fri 18 Dec 2026 11:30 London** free for `033` Uranus Short 1 (`J2317`).

---

### D. Non-Duplication of `J2230` (HOS Shorts Gap 18 Nov – 6 Dec) & Remaining HOS Gaps After 6 December

1. **Status of `J2230` Window (18 Nov – 6 Dec 2026 — Do Not Duplicate):**
   - `J2230` (*HOS Shorts gap after 17 Nov: cut six search-titled Shorts from the locked Harvey, Willow and Vaccine longs, slot 18 Nov to 6 Dec*) remains `blocked` (`J2305` recheck open).
   - Since `J2230` was queued on 5 Nov, two HOS `006` (Willow) Shorts from `J2169` passed Ben's watch and were uploaded Private on 6 Nov:
     - `ChbsigHD5_o` (*How Do Plants Clean the Air?*, `006` Short B `v02`, `J2272`) — scheduled **Wed 18 Nov 2026 11:30Z** (off-pattern `Wed`; leave in place).
     - `Bks_JLId1ew` (*How Do Plants Make Oxygen?*, `006` Short C `v03`, `J2273`) — scheduled **Sat 21 Nov 2026 11:30Z** (on-pattern `Sat`).
   - That leaves **10 of the 11 HOS pattern Short slots** in the 18 Nov – 6 Dec window (**Fri 20 Nov, Sun 22 Nov, Tue 24 Nov, Fri 27 Nov, Sat 28 Nov, Sun 29 Nov, Tue 1 Dec, Fri 4 Dec, Sat 5 Dec, Sun 6 Dec**) **EMPTY on YouTube**, covered conditionally by the existing `J2023`/`J2230` pipeline (`008` Short A `J0912` & Short C `J2255`, `009` Shorts A/B `J2171`, `010` Shorts A/C `J2172`, each gated on its parent long going public first).
2. **Remaining HOS Gaps After 6 December (7 Dec 2026 – 10 Jan 2027):**
   - **HOS Longs (`Thu 18:00 London` — 5 Thursdays from 10 Dec to 7 Jan):**
     - **Thu 10 Dec 2026 18:00Z — DOUBLE-BOOKED / COLLISION FLAG:** `uAomPaOBrM8` (`099` Compilation: *How Did Experiments Explain Blood, Germs and Atoms?*, `2959 s`) is **already scheduled on YouTube** for `2026-12-10T18:00:00Z`, while `011` (*Anesthesia: The Day Surgery Stopped Hurting*) was also slotted for **Thu 10 Dec 2026 18:00Z** by `J2231`/`J2239` (VO in `J2245`/`J2286`). Chief will need to decide whether `uAomPaOBrM8` moves to another date or whether `011` shifts.
     - **Thu 17 Dec 2026 18:00Z — EMPTY on YouTube:** Planned for `013` (*Evolution: The Letter That Forced Darwin to Publish*, active in `WIP.json`, script & long VO locked, `J2240` done, Shorts VO in `J2246`).
     - **Thu 24 Dec 2026 18:00Z — EMPTY on YouTube:** Proposed for `012` (*Genetics: The Monk Who Counted 28,000 Pea Plants*, in `WIP.json` `next_hos`, topic go/no-go prep in `J2328`; not yet in active production).
     - **Thu 31 Dec 2026 18:00Z — EMPTY on YouTube:** Proposed for `014` (*Extinction: The 12-Year-Old Who Dug Up a Sea Dragon*, in `WIP.json` `next_hos`, topic go/no-go prep in `J2328`; not yet in active production).
     - **Thu 7 Jan 2027 18:00Z — EMPTY on YouTube:** Proposed for `015` (*Cell Theory: How Cork, a Microscope and a Stolen Idea Revealed Our Cells*, in `WIP.json` `next_hos`; not yet in active production).
   - **HOS Shorts (`Sat · Fri · Sun · Tue 11:30 London` — 20 pattern slots from Tue 8 Dec 2026 through Sun 10 Jan 2027):**
     - **0 of 20 HOS Short slots after 6 December are currently scheduled on YouTube.**
     - **Structural supply gap (2 Shorts/film vs. 4 Shorts/week):** Under Test B (`AGENTS.md` line 330), every new HOS film from `007` onward scripts **2 search-titled Shorts** (`010` has 2 in `J2172`; `011` has 2 scripted in `J2239`; `013` has 2 scripted in `J2240`, VO in `J2246`; `005` s07 reserve for 10 Dec was **rejected** in `J2168` for overlap with `BW_CFAX-mxc`).
     - Even if `010` places 1–2 Shorts in early Dec and `011` (after 10 Dec), `013` (after 17 Dec), `012` (after 24 Dec), `014` (after 31 Dec), and `015` (after 7 Jan) each deliver 2 Shorts on time, **2 Shorts per weekly long fills only 2 of the 4 weekly HOS Short slots**, leaving **at least 2 empty HOS Short slots per week (10–14 empty slots across 7 Dec – 10 Jan)**. Per the locked rule, those slots remain empty unless filled with ready, non-overlapping approved cuts (never placeholders).

---

### E. Read-Only Metadata Hygiene Flag in `00_Brand/Channel-Setup/social/UPLOADS.json`

- On **Mon 30 Nov 2026 11:30Z**, the live scheduled Private YouTube video is `xvarZP2aYyE` (*Why Will Gliese 710's Comets Arrive After It Has Gone?*, `028_short_mon30_comets_v04.mp4`), which has `publishAt: "2026-11-30T11:30:00Z"` in `05_Analytics/owb/snapshots/2026-11-06.json` but `publishAt: null` in `00_Brand/Channel-Setup/social/UPLOADS.json`. Meanwhile, the superseded `v01` upload `bizlhspnVvY` (now Private unscheduled on YouTube) still carries `publishAt: "2026-11-30T11:30:00.000Z"` in `UPLOADS.json`. Left untouched per the read-only brief.

---

## 3. Week-by-Week Calendar-Gap Readback (Sat 7 Nov 2026 – Sun 10 Jan 2027)

Legend:
- **`SCHEDULED (<id>)`**: Uploaded Private on YouTube with `publishAt` set (verified in `2026-11-06.json` snapshot or 6 Nov `UPLOADS.json` readback).
- **`EMPTY` — *(Planned: ...)*:** Empty on YouTube; shows any conditional/in-production candidate from queue jobs (`J2023`, `J2147`, `J2223`, `J2228`, `J2231`, `J2317`–`J2320`, `J2326`–`J2328`).
- **`EMPTY` — *(No candidate)*:** Empty cadence slot on YouTube with no ready or scoped cut assigned (do not publish placeholders).
- **`OFF-PATTERN SCHEDULED (<id>)`**: Already-scheduled Short sitting on a non-pattern day; **leave where it is**.

---

### Week 0 (Partial Current Weekend): Sat 7 Nov – Sun 8 Nov 2026

| Date | Day | Channel & Cadence Slot | YouTube Status / Video ID | Notes / Flags |
|---|---|---|---|---|
| **2026-11-07** | **Sat** | **OWB Short** (`11:30`) | **SCHEDULED** (`T9fVlG3CCzU`) | *What Are Shooting Stars Really Made Of?* (`21 s`, standalone test Short S7). |
| **2026-11-07** | **Sat** | **HOS Short** (`11:30`) | **EMPTY** *(No candidate)* | First Saturday after 7 Nov lock (`006` Willow aired Thu 5 Nov; `005` `xHnIi9GqOsM` aired Thu 5 Nov 11:30). Leave empty. |
| **2026-11-08** | **Sun** | **HOS Short** (`11:30`) | **SCHEDULED** (`PFj6172YU4Q`) | *One Tight Band Proved Your Blood Goes Round* (`27 s`, `005` Harvey Short s02). |
| **2026-11-08** | **Sun** | **OWB Long** (`18:00`) | **SCHEDULED** (`Js6EQJ8qDi8`) | `025` — *Could a Robot Survive on Mars?* (`491 s`). |

---

### Week 1: Mon 9 Nov – Sun 15 Nov 2026

| Date | Day | Channel & Cadence Slot | YouTube Status / Video ID | Notes / Flags |
|---|---|---|---|---|
| **2026-11-09** | **Mon** | **OWB Short** (`11:30`) | **SCHEDULED** (`iyvWYFP_ETA`) | *Could a Robot Survive a Night on Mars?* (`26 s`, `025` Short). **FLAG:** `J2248` (`024` muons) must **not** take this slot — move `J2248` target to **Sat 21 Nov 11:30**. |
| **2026-11-10** | **Tue** | *OWB Off-Pattern Short* (`11:30`) | **OFF-PATTERN SCHEDULED** (`ffYKoNVPoqg`) | *What Would Standing on Saturn's Moon Titan Feel Like?* (`19 s`, standalone S6 `v11`, `J2259`). **Leave in place.** |
| **2026-11-10** | **Tue** | **HOS Short** (`11:30`) | **EMPTY** *(Conditional: `J2168`/`J2174`)* | `005` s06 Blood Pressure Cuff failed opening/clinical-source qualification in `J2168` (`J2174` repair decision); remains empty unless approved & watched in time. |
| **2026-11-11** | **Wed** | **OWB Short** (`11:30`) | **SCHEDULED** (`B1z2dv7m7Vk`) | *Why Did a 90-Day Mars Rover Last 14 Years?* (`27 s`, `025` Test A opening Short `v07`). |
| **2026-11-11** | **Wed** | **OWB Long** (`18:00`) | **EMPTY** *(Pre-start of Wed longs)* | Locked rule: Wednesday longs start on **Wed 25 Nov** (`032` Titan). |
| **2026-11-12** | **Thu** | *OWB Off-Pattern Short* (`11:30`) | **OFF-PATTERN SCHEDULED** (`N42gKBbD7tE`) | *How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years?* (`55 s`, `025` Chief-OK'd length-test Short). **Leave in place.** |
| **2026-11-12** | **Thu** | **HOS Long** (`18:00`) | **SCHEDULED** (`ETynHpIYLeY`) | `007` — *Why Vaccines Are Named After a Cow* (`532 s`). |
| **2026-11-13** | **Fri** | **OWB Short** (`11:30`) | **SCHEDULED** (`bSjWiCbB7pY`) | *How Did a Helicopter Fly 72 Times on Mars?* (`27 s`, `025` Short). |
| **2026-11-13** | **Fri** | **HOS Short** (`11:30`) | **SCHEDULED** (`cLKDiYP55J8`) | *What Was the Edward Jenner Experiment?* (`23 s`, `007` Short s04; airs after `007` long is public on 12 Nov). |
| **2026-11-14** | **Sat** | **OWB Short** (`11:30`) | **SCHEDULED** (`gmzaCfJF1gA`) | *Why Does Pluto's Giant Ice Heart Have Zero Craters?* (`23 s`, standalone test Short S8). |
| **2026-11-14** | **Sat** | **HOS Short** (`11:30`) | **EMPTY** *(No candidate)* | Empty Saturday HOS slot (`007` only has 2 Shorts, scheduled Fri 13 Nov & Tue 17 Nov). |
| **2026-11-15** | **Sun** | **HOS Short** (`11:30`) | **SCHEDULED** (`Wvjd8g0CpzE`) | *The Blood Vessels Finer Than a Hair* (`26 s`, `005` Harvey Short s03). |
| **2026-11-15** | **Sun** | **OWB Long** (`18:00`) | **SCHEDULED** (`c5AdqQsnnys`) | `026` — *Why Reaching the Nearest Star Takes 75,000 Years* (`495 s`). |

---

### Week 2: Mon 16 Nov – Sun 22 Nov 2026

| Date | Day | Channel & Cadence Slot | YouTube Status / Video ID | Notes / Flags |
|---|---|---|---|---|
| **2026-11-16** | **Mon** | **OWB Short** (`11:30`) | **SCHEDULED** (`HZGTovJu_TQ`) | *If You Can't See the Nearest Star, How Far Away Is It?* (`27 s`, `026` Short). |
| **2026-11-16** | **Mon** | *HOS Off-Pattern Short* (`11:30`) | **OFF-PATTERN SCHEDULED** (`xzKoHg0E0_U`) | *What Is Dalton's Atomic Theory?* (`25 s`, `004` Atom Short s05). **Leave in place.** |
| **2026-11-17** | **Tue** | *OWB Off-Pattern Short* (`11:30`) | **OFF-PATTERN SCHEDULED** (`kKN8Ale42sE`) | *How Far From Earth Is Voyager 1 Right Now?* (`21 s`, standalone test Short S5). **Leave in place.** |
| **2026-11-17** | **Tue** | **HOS Short** (`11:30`) | **SCHEDULED** (`xgx2lYHhYZM`) | *Why Is It Called a Vaccine?* (`25 s`, `007` Short s05). Last HOS Short in `2026-11-06.json` snapshot. |
| **2026-11-18** | **Wed** | **OWB Short** (`11:30`) | **SCHEDULED** (`cwU_0WWeNZ4`) | *If Voyager Needs 75,000 Years, How Far Is the Nearest Star?* (`24 s`, `026` Short). |
| **2026-11-18** | **Wed** | *HOS Off-Pattern Short* (`11:30`) | **OFF-PATTERN SCHEDULED** (`ChbsigHD5_o`) | *How Do Plants Clean the Air?* (`24.25 s`, `006` Willow Short B `v02`, uploaded Private on 6 Nov in `J2272`). **Leave in place.** |
| **2026-11-18** | **Wed** | **OWB Long** (`18:00`) | **EMPTY** *(Pre-start of Wed longs)* | Locked rule: Wednesday longs start on **Wed 25 Nov** (`032` Titan). |
| **2026-11-19** | **Thu** | **HOS Long** (`18:00`) | **EMPTY** *(Planned: `HOS:008`)* | `008` Franklin (*Lightning*) — in active re-edit (`J2241`/`J2242`/`J2243` for `v04`, then Ben's watch). Not yet uploaded. |
| **2026-11-20** | **Fri** | **OWB Short** (`11:30`) | **SCHEDULED** (`aAUgIGEuPwQ`) | *The Nearest Star Is a Cherry Past Cairo. How Do We Know?* (`24 s`, `026` Short `v04`). |
| **2026-11-20** | **Fri** | **HOS Short** (`11:30`) | **EMPTY** *(Blocked `J2230` window)* | Empty on YouTube (within `J2230` 18 Nov – 6 Dec HOS gap window). |
| **2026-11-21** | **Sat** | **OWB Short** (`11:30`) | **EMPTY** *(Proposed for `J2248`)* | **PROPOSED SLOT FOR `J2248` (`024` Muons Short):** Earliest free OWB pattern slot (`gate_shorts_open.py` already checked for `2026-11-21` in `J2283`), subject to `J2302` (`v03` review) + Ben watch. |
| **2026-11-21** | **Sat** | **HOS Short** (`11:30`) | **SCHEDULED** (`Bks_JLId1ew`) | *How Do Plants Make Oxygen?* (`25.17 s`, `006` Willow Short C `v03`, uploaded Private on 6 Nov in `J2273`; on-pattern Saturday). |
| **2026-11-22** | **Sun** | **HOS Short** (`11:30`) | **EMPTY** *(Blocked `J2230` window)* | Empty on YouTube (within `J2230` 18 Nov – 6 Dec HOS gap window). |
| **2026-11-22** | **Sun** | **OWB Long** (`18:00`) | **SCHEDULED** (`6bbbvfCx6zY`) | `027` — *What If Earth Stopped Spinning?* (`447 s`). |

---

### Week 3: Mon 23 Nov – Sun 29 Nov 2026

| Date | Day | Channel & Cadence Slot | YouTube Status / Video ID | Notes / Flags |
|---|---|---|---|---|
| **2026-11-23** | **Mon** | **OWB Short** (`11:30`) | **SCHEDULED** (`Dm4xsF1Ateg`) | *Why Do You Weigh Less at Earth's Equator?* (`23 s`, `027` Short `v07`, swapped in by `J1100` replacing `emwQsPxnRGM`). |
| **2026-11-24** | **Tue** | **HOS Short** (`11:30`) | **EMPTY** *(Conditional: `008` Short A `J0912`/`J2224`)* | `J2023` target for `008` Short A (*Did Lightning Hit Franklin's Kite?*). Requires `008` long (`19 Nov` target) to be public first, plus `J2224` review & Ben watch. |
| **2026-11-25** | **Wed** | **OWB Short** (`11:30`) | **EMPTY** *(Conditional: `AR2` `J2229` or `J2248` fallback)* | **FLAG (`J2147` VIOLATION):** `J2147` planned `032` Titan Short 1 here at `11:30`, which is **6.5 h before** the `032` Titan long at `18:00` — **barred by the never-before-its-long rule**. Only a Short whose long is already public (or standalone `AR2` *Where Will the ISS Crash?* after `J2229` fix + Ben watch, or `J2248` `024` muons if not on 21 Nov) may use Wed 25 Nov 11:30. |
| **2026-11-25** | **Wed** | **OWB Long** (`18:00`) | **EMPTY** *(Planned: `OWB:032`)* | **First Wednesday OWB Long:** `032` — *What Would Happen If You Landed on Titan?* (November tentpole; picture in `J2089`, watch due ~16 Nov). Not yet uploaded. |
| **2026-11-26** | **Thu** | **HOS Long** (`18:00`) | **EMPTY** *(Planned: `HOS:009`)* | `009` — *Why Doesn't the Moon Fall to Earth?* (Tranche-2 picture runner in `J2275`/`J2200`/`J2033` → edit `J2035` → Ben watch `J2037`). Not yet uploaded. |
| **2026-11-27** | **Fri** | **OWB Short** (`11:30`) | **EMPTY** *(Queued: `AR1` `J2228` vs. `032` Short 2 `J2173`)* | **COLLISION / PRIORITY NOTE:** `J2228` is open to upload Ben-approved `AR1 v06` (*2024 YR4 Moon*) Private for **Fri 27 Nov 11:30**, while `J2147`/`J2173` also target Fri 27 Nov 11:30 for `032` Titan Test A opening Short. Never two Shorts the same day: if `J2228` books Fri 27 Nov 11:30 for `AR1`, `032`'s two Shorts take **Sat 28 Nov 11:30** + the next free Saturday (**Sat 5 Dec** or **Sat 12 Dec**). |
| **2026-11-27** | **Fri** | **HOS Short** (`11:30`) | **EMPTY** *(Conditional: `009` Short A `J2171`)* | `J2023` target for `009` Short A (*What Would Happen If the Moon Stopped Moving?*). Requires `009` long (`26 Nov` target) to be public first. |
| **2026-11-28** | **Sat** | **OWB Short** (`11:30`) | **EMPTY** *(Planned: `032` Short 1 or `AR3` `J2229`)* | Compliant post-long slot for `032` Short 1 (*What Happens If You Strike a Match on Titan?*, moved off Wed 25 Nov 11:30 per never-before-long rule) or `032` Test A Short 2; **drop `032` Reserve Short 3** per the 2-Short cap. (`AR3` eclipse in `J2229` also targets this window.) |
| **2026-11-28** | **Sat** | **HOS Short** (`11:30`) | **EMPTY** *(Blocked `J2230` window)* | On-pattern Saturday HOS slot (prefer this or **Sun 29 Nov / Tue 1 Dec** for `009` Short B instead of `J2023`'s off-pattern Mon 30 Nov). |
| **2026-11-29** | **Sun** | **HOS Short** (`11:30`) | **EMPTY** *(Blocked `J2230` window)* | Empty on YouTube (within `J2230` 18 Nov – 6 Dec HOS gap window). |
| **2026-11-29** | **Sun** | **OWB Long** (`18:00`) | **SCHEDULED** (`F-jImX5h7ws`) | `028` — *What Happens When a Star Enters Our Solar System?* (`498 s`). |

---

### Week 4: Mon 30 Nov – Sun 6 Dec 2026

| Date | Day | Channel & Cadence Slot | YouTube Status / Video ID | Notes / Flags |
|---|---|---|---|---|
| **2026-11-30** | **Mon** | **OWB Short** (`11:30`) | **SCHEDULED** (`xvarZP2aYyE`) | *Why Will Gliese 710's Comets Arrive After It Has Gone?* (`23 s`, `028` Short `v04`). *(Note: `UPLOADS.json` still lists `publishAt` on superseded `bizlhspnVvY` — read-only flag.)* |
| **2026-12-01** | **Tue** | **HOS Short** (`11:30`) | **EMPTY** *(Blocked `J2230` window / `008` Short C `J2255`)* | On-pattern Tuesday HOS slot (recommend moving `008` Short C *How Does a Lightning Rod Work?* [`J2170`/`J2175`/`J2255`] from off-pattern Wed 2 Dec to **Tue 1 Dec** or **Fri 4 Dec / Sat 5 Dec** once ready and after `008` long is public). |
| **2026-12-02** | **Wed** | **OWB Short** (`11:30`) | **SCHEDULED** (`v6euXX2omz4`) | *Is a Star Really Coming Towards Us?* (`25 s`, `028` Test A Short `v04`). **FLAG (`J2147` Path B REJECTED):** Do **not** swap `031` Short 1 into `Wed 2 Dec 11:30` — `031` long airs at `18:00` that evening, so a `11:30` `031` Short would violate the never-before-the-long rule. Leave `v6euXX2omz4` in place. |
| **2026-12-02** | **Wed** | **OWB Long** (`18:00`) | **EMPTY** *(Planned: `OWB:031`)* | **Second Wednesday OWB Long:** `031` — *What Happens When Earth's Magnetic Field Flips?* (picture in `J2141`, thumbs in `J2143`/`J2166`, watch due ~18 Nov). Not yet uploaded. |
| **2026-12-03** | **Thu** | **HOS Long** (`18:00`) | **EMPTY** *(Planned: `HOS:010`)* | `010` — *What Killed the Dinosaurs Was Hidden in a Line of Clay* (long VO & shot list done; picture & Shorts gated on `J2269`/`J2270`/`J2271`). Not yet uploaded. |
| **2026-12-04** | **Fri** | **OWB Short** (`11:30`) | **SCHEDULED** (`BTuL_QBbEgY`) | *How Close Will Gliese 710 Come to the Sun?* (`24 s`, `028` Short `v07`, swapped in by `J1100` replacing `jJ5LkFGyzLI`). |
| **2026-12-04** | **Fri** | **HOS Short** (`11:30`) | **EMPTY** *(Conditional: `010` Short A `J2172`)* | `J2023`/`J2172` target for `010` Short A (*What Killed the Dinosaurs?*). Held (`J2323`) on `010` plates and `010` long (`3 Dec` target) going public first. |
| **2026-12-05** | **Sat** | **OWB Short** (`11:30`) | **EMPTY** *(Planned: `031` Short 1 `J2147` Path A)* | `031` Active Short #1 (*What Happens When Earth's Magnetic Field Flips?*, Test A opening, `33.00 s`) — compliant post-long slot (3 days after Wed 2 Dec 18:00 `031` long). |
| **2026-12-05** | **Sat** | **HOS Short** (`11:30`) | **EMPTY** *(Blocked `J2230` window)* | Go-public-week Saturday HOS slot (can host `010` Short C from `J2172` instead of off-pattern Mon 7 Dec if `010` long is public on 3 Dec). |
| **2026-12-06** | **Sun** | **HOS Short** (`11:30`) | **EMPTY** *(Blocked `J2230` window)* | End of `J2230` (18 Nov – 6 Dec) HOS Shorts gap window. |
| **2026-12-06** | **Sun** | **OWB Long** (`18:00`) | **SCHEDULED** (`vP1BbqZ_dnM`) | `029` — *Is Betelgeuse About to Explode?* (`543 s`). **Last OWB long currently uploaded/scheduled on YouTube.** |

---

### Week 5: Mon 7 Dec – Sun 13 Dec 2026 (First Post-`J2230` HOS Week)

| Date | Day | Channel & Cadence Slot | YouTube Status / Video ID | Notes / Flags |
|---|---|---|---|---|
| **2026-12-07** | **Mon** | **OWB Short** (`11:30`) | **SCHEDULED** (`lsOCcIYCud0`) | *What Will the Night Sky Look Like When Gliese 710 Arrives?* (`24 s`, `028` 4th Short `v07`, swapped in by `J1100` replacing `X768qs8sNQs`). |
| **2026-12-08** | **Tue** | **HOS Short** (`11:30`) | **EMPTY** *(Post-`J2230` gap; conditional `010` Short C `J2172`)* | First HOS Short slot after 6 Dec. If `010` Short C (*Are Birds Really Dinosaurs?*, `J2172`) is moved off off-pattern Mon 7 Dec, **Tue 8 Dec 11:30** is the matching on-pattern day (after `010` long is public). |
| **2026-12-09** | **Wed** | **OWB Short** (`11:30`) | **SCHEDULED** (`SWDCZfWZVao`) | *Why Did Betelgeuse Suddenly Lose Two-Thirds of Its Light?* (`23 s`, `029` Short 1; E1 re-cut in `J2309`/`J2321`). |
| **2026-12-09** | **Wed** | **OWB Long** (`18:00`) | **EMPTY** *(Planned: `OWB:033` Uranus, `J2326`)* | `033` — *Why Knocked-Sideways Uranus Has 21-Year Winters* (`film_briefs.json` & `J2326`; VO locked `J2155`/`J2164`, picture in `J2299`/`J2300`). Must go public before `033` Shorts on 18–19 Dec. |
| **2026-12-10** | **Thu** | **HOS Long** (`18:00`) | **SCHEDULED** (`uAomPaOBrM8`) | **COLLISION FLAG:** `uAomPaOBrM8` (`099` Compilation: *How Did Experiments Explain Blood, Germs and Atoms?*, `2959 s`) is **scheduled on YouTube** for `Thu 10 Dec 18:00Z`, while `HOS:011` (*Anesthesia: The Day Surgery Stopped Hurting*) is also slotted for `Thu 10 Dec 18:00Z` (`J2231`/`J2239`, VO in `J2245`/`J2286`). |
| **2026-12-11** | **Fri** | **OWB Short** (`11:30`) | **SCHEDULED** (`k2kEaA7ICjc`) | *Is Betelgeuse Really About to Explode?* (`34 s`, `029` Test A Short 2; `v05` KEEP in `J2315`). |
| **2026-12-11** | **Fri** | **HOS Short** (`11:30`) | **EMPTY** *(Post-`J2230` gap)* | Empty on YouTube (`005` s07 reserve was rejected in `J2168` for overlap with `BW_CFAX-mxc`). |
| **2026-12-12** | **Sat** | **OWB Short** (`11:30`) | **EMPTY** *(Planned: `031` Short 2 `J2147` Path A)* | `031` Active Short #2 (*What If the Solar Wind Blew Earth's Atmosphere Into Space?*, `24.48 s`). **Cap at 2 Shorts for `031`** (do not schedule `031` Reserve Short 3). |
| **2026-12-12** | **Sat** | **HOS Short** (`11:30`) | **EMPTY** *(Planned: `011` Short A, `J2239`)* | Go-public-week Saturday slot for `011` *Anesthesia* Short A (*How Was Surgery Done Before Anesthesia?*, scripted in `J2239`), gated on `011` long being public on Thu 10 Dec. |
| **2026-12-13** | **Sun** | **HOS Short** (`11:30`) | **EMPTY** *(Planned: `011` Short B, `J2239`)* | Second slot for `011` *Anesthesia* Short B (*Who Invented Anesthesia?*, scripted in `J2239`), gated on `011` long being public on Thu 10 Dec. |
| **2026-12-13** | **Sun** | **OWB Long** (`18:00`) | **EMPTY** *(Planned: `OWB:034` Pluto, `J2326`)* | `034` — *Why Pluto's Frozen Heart Has Zero Craters* (`film_briefs.json` & `J2326`; VO in `J2157`). Must go public before `034` Shorts on 21 & 23 Dec. |

---

### Week 6: Mon 14 Dec – Sun 20 Dec 2026

| Date | Day | Channel & Cadence Slot | YouTube Status / Video ID | Notes / Flags |
|---|---|---|---|---|
| **2026-12-14** | **Mon** | **OWB Short** (`11:30`) | **SCHEDULED** (`heiGCnGKTkE`) | *How Bright Will Betelgeuse Get When It Explodes?* (`24 s`, `029` Short 3; `v05` KEEP in `J2316`). |
| **2026-12-15** | **Tue** | **HOS Short** (`11:30`) | **EMPTY** *(No candidate — post-6 Dec gap)* | Empty on YouTube (if `011` uses Sat 12 & Sun 13 Dec, no 3rd `011` Short exists under Test B's 2-Short rule). |
| **2026-12-16** | **Wed** | **OWB Short** (`11:30`) | **SCHEDULED** (`f17XCtUmN-g`) | *What Happens When Gliese 710 Passes Through the Oort Cloud?* (`23 s`, `028` 5th Short `v03`). **Last OWB Short currently uploaded/scheduled on YouTube.** |
| **2026-12-16** | **Wed** | **OWB Long** (`18:00`) | **EMPTY** *(Candidate: `OWB:030` Apophis or `J01`, `J2326`)* | Empty on YouTube (`J2326` maps `033`, `034`, and `030` onto Dec Wed/Sun slots). |
| **2026-12-17** | **Thu** | **HOS Long** (`18:00`) | **EMPTY** *(Planned: `HOS:013` Darwin & Wallace, `J2231`)* | `013` — *Evolution: The Letter That Forced Darwin to Publish* (in active production; script `v02` & long VO `v03a` locked, package/shot list done `J2240`, Shorts VO in `J2246`). Not yet uploaded. |
| **2026-12-18** | **Fri** | **OWB Short** (`11:30`) | **EMPTY** *(Planned: `033` Uranus Short 1, `J2223`/`J2317`)* | `033` Short 1 (*Why Does Knocked-Sideways Uranus Have 21-Year Winters?*, Test A opening, `J2317` open). Requires `033` long (`Wed 9 Dec` target) to be public first, and `031` Reserve Short 3 to stay unscheduled. |
| **2026-12-18** | **Fri** | **HOS Short** (`11:30`) | **EMPTY** *(No candidate — post-6 Dec gap)* | Empty on YouTube (unless `013` Short A takes Fri 18 Dec instead of Sun 20 Dec after `013` long goes public on Thu 17 Dec). |
| **2026-12-19** | **Sat** | **OWB Short** (`11:30`) | **EMPTY** *(Planned: `033` Uranus Short 2, `J2223`/`J2318`)* | `033` Short 2 (*What Happens If a Spacecraft Tries to Land on Ice Giant Uranus?*, Keeper question, `J2318` open). Requires `033` long to be public first. |
| **2026-12-19** | **Sat** | **HOS Short** (`11:30`) | **EMPTY** *(Planned: `013` Short A, `J2240`/`J2246`)* | Go-public-week Saturday slot for `013` *Darwin & Wallace* Short A (*How Did Darwin Discover Evolution?*, scripted in `J2240`, VO in `J2246`), gated on `013` long going public on Thu 17 Dec. |
| **2026-12-20** | **Sun** | **HOS Short** (`11:30`) | **EMPTY** *(Planned: `013` Short B, `J2240`/`J2246`)* | Second slot for `013` *Darwin & Wallace* Short B (*What Is Survival of the Fittest?*, scripted in `J2240`, VO in `J2246`), gated on `013` long going public on Thu 17 Dec. |
| **2026-12-20** | **Sun** | **OWB Long** (`18:00`) | **EMPTY** *(Candidate: `OWB:030` Apophis or `J01`, `J2326`)* | Empty on YouTube (`J2326` Dec long date map). |

---

### Week 7: Mon 21 Dec – Sun 27 Dec 2026

| Date | Day | Channel & Cadence Slot | YouTube Status / Video ID | Notes / Flags |
|---|---|---|---|---|
| **2026-12-21** | **Mon** | **OWB Short** (`11:30`) | **EMPTY** *(Planned: `034` Pluto Short 1, `J2223`/`J2319`)* | `034` Short 1 (*What Did New Horizons Discover Inside Pluto's Frozen Heart?*, Test A opening, `J2319` open). Requires `034` long (`Sun 13 Dec` target) to be public first. |
| **2026-12-22** | **Tue** | **HOS Short** (`11:30`) | **EMPTY** *(No candidate — post-6 Dec gap)* | Empty on YouTube (no 3rd `013` Short under Test B's 2-Short cap). |
| **2026-12-23** | **Wed** | **OWB Short** (`11:30`) | **EMPTY** *(Planned: `034` Pluto Short 2, `J2223`/`J2320`)* | `034` Short 2 (*Why Does Pluto's Giant Moon Charon Never Rise or Set?*, Keeper question, `J2320` open). Requires `034` long to be public first. |
| **2026-12-23** | **Wed** | **OWB Long** (`18:00`) | **EMPTY** *(Next wave `035`–`038`, `J2327`)* | Empty on YouTube; awaits next OWB production wave (`035` Triton / `036` Mercury Ice / `037` Sagittarius A* / `038` Golden Record; topic prep in `J2327`). |
| **2026-12-24** | **Thu** | **HOS Long** (`18:00`) | **EMPTY** *(Proposed: `HOS:012` Mendel, `J2231`/`J2328`)* | `012` — *Genetics: The Monk Who Counted 28,000 Pea Plants* (proposed in `VIDEO_BACKLOG.json`, topic go/no-go prep in `J2328`; not yet in `WIP.json` `active`). |
| **2026-12-25** | **Fri** | **OWB Short** (`11:30`) | **EMPTY** *(Unplanned — `030` or next wave)* | Empty on YouTube (if `030` Apophis airs on 16 or 20 Dec, its 2 Shorts can take **Fri 25 Dec & Sat 26 Dec 11:30**). |
| **2026-12-25** | **Fri** | **HOS Short** (`11:30`) | **EMPTY** *(No candidate — post-6 Dec gap)* | Empty on YouTube. |
| **2026-12-26** | **Sat** | **OWB Short** (`11:30`) | **EMPTY** *(Unplanned — `030` or next wave)* | Empty on YouTube. |
| **2026-12-26** | **Sat** | **HOS Short** (`11:30`) | **EMPTY** *(Unplanned — requires `012` public on 24 Dec)* | Go-public-week Saturday slot for `012` Short A (not yet scripted; `012` not yet in `active`). |
| **2026-12-27** | **Sun** | **HOS Short** (`11:30`) | **EMPTY** *(Unplanned — requires `012` public on 24 Dec)* | Second slot for `012` Short B (not yet scripted). |
| **2026-12-27** | **Sun** | **OWB Long** (`18:00`) | **EMPTY** *(Next wave `035`–`038`, `J2327`)* | Empty on YouTube. |

---

### Week 8: Mon 28 Dec 2026 – Sun 3 Jan 2027

| Date | Day | Channel & Cadence Slot | YouTube Status / Video ID | Notes / Flags |
|---|---|---|---|---|
| **2026-12-28** | **Mon** | **OWB Short** (`11:30`) | **EMPTY** *(No candidate)* | Empty on YouTube (awaits Shorts from `23 Dec` / `27 Dec` OWB longs). |
| **2026-12-29** | **Tue** | **HOS Short** (`11:30`) | **EMPTY** *(No candidate — post-6 Dec gap)* | Empty on YouTube. |
| **2026-12-30** | **Wed** | **OWB Short** (`11:30`) | **EMPTY** *(No candidate)* | Empty on YouTube. |
| **2026-12-30** | **Wed** | **OWB Long** (`18:00`) | **EMPTY** *(Next wave `035`–`038`, `J2327`)* | Empty on YouTube. |
| **2026-12-31** | **Thu** | **HOS Long** (`18:00`) | **EMPTY** *(Proposed: `HOS:014` Mary Anning, `J2231`/`J2328`)* | `014` — *Extinction: The 12-Year-Old Who Dug Up a Sea Dragon* (proposed in `VIDEO_BACKLOG.json`, topic go/no-go prep in `J2328`; not yet in `WIP.json` `active`). |
| **2027-01-01** | **Fri** | **OWB Short** (`11:30`) | **EMPTY** *(No candidate)* | Empty on YouTube. |
| **2027-01-01** | **Fri** | **HOS Short** (`11:30`) | **EMPTY** *(No candidate — post-6 Dec gap)* | Empty on YouTube. |
| **2027-01-02** | **Sat** | **OWB Short** (`11:30`) | **EMPTY** *(No candidate)* | Empty on YouTube. |
| **2027-01-02** | **Sat** | **HOS Short** (`11:30`) | **EMPTY** *(Unplanned — requires `014` public on 31 Dec)* | Go-public-week Saturday slot for `014` Short A (not yet scripted). |
| **2027-01-03** | **Sun** | **HOS Short** (`11:30`) | **EMPTY** *(Unplanned — requires `014` public on 31 Dec)* | Second slot for `014` Short B (not yet scripted). |
| **2027-01-03** | **Sun** | **OWB Long** (`18:00`) | **EMPTY** *(Next wave `035`–`038`, `J2327`)* | Empty on YouTube. |

---

### Week 9: Mon 4 Jan – Sun 10 Jan 2027

| Date | Day | Channel & Cadence Slot | YouTube Status / Video ID | Notes / Flags |
|---|---|---|---|---|
| **2027-01-04** | **Mon** | **OWB Short** (`11:30`) | **EMPTY** *(No candidate)* | Empty on YouTube. |
| **2027-01-05** | **Tue** | **HOS Short** (`11:30`) | **EMPTY** *(No candidate — post-6 Dec gap)* | Empty on YouTube. |
| **2027-01-06** | **Wed** | **OWB Short** (`11:30`) | **EMPTY** *(No candidate)* | Empty on YouTube. |
| **2027-01-06** | **Wed** | **OWB Long** (`18:00`) | **EMPTY** *(Next wave `035`–`038`, `J2327`)* | Empty on YouTube. |
| **2027-01-07** | **Thu** | **HOS Long** (`18:00`) | **EMPTY** *(Proposed: `HOS:015` Cell Theory, `J2231`)* | `015` — *Cell Theory: How Cork, a Microscope and a Stolen Idea Revealed Our Cells* (proposed in `VIDEO_BACKLOG.json` `next_hos #4`; not yet in `active`). *(Followed by proposed `018` Invisible Light on Thu 14 Jan 2027.)* |
| **2027-01-08** | **Fri** | **OWB Short** (`11:30`) | **EMPTY** *(No candidate)* | Empty on YouTube. |
| **2027-01-08** | **Fri** | **HOS Short** (`11:30`) | **EMPTY** *(No candidate — post-6 Dec gap)* | Empty on YouTube. |
| **2027-01-09** | **Sat** | **OWB Short** (`11:30`) | **EMPTY** *(No candidate)* | Empty on YouTube. |
| **2027-01-09** | **Sat** | **HOS Short** (`11:30`) | **EMPTY** *(Unplanned — requires `015` public on 7 Jan)* | Go-public-week Saturday slot for `015` Short A (not yet scripted). |
| **2027-01-10** | **Sun** | **HOS Short** (`11:30`) | **EMPTY** *(Unplanned — requires `015` public on 7 Jan)* | Second slot for `015` Short B (not yet scripted). |
| **2027-01-10** | **Sun** | **OWB Long** (`18:00`) | **EMPTY** *(Next wave `035`–`038`, `J2327`)* | Empty on YouTube. |

---

## 4. Summary Count of Pattern Slots & Gaps (Sat 7 Nov 2026 – Sun 10 Jan 2027)

| Channel & Format | Total Pattern Slots (7 Nov – 10 Jan) | Scheduled on YouTube (On-Pattern) | Empty Pattern Slots on YouTube | Scheduled on Off-Pattern Days (Left Untouched) | Key Actionable Takeaways |
|---|---:|---:|---:|---:|---|
| **Orbit Longs** (`Sun & Wed 18:00`) | **19** *(17 from Wed 25 Nov start of Wed longs)* | **5** (`025`–`029`, all Sundays through 6 Dec) | **14** *(12 active from Wed 25 Nov: `25 Nov`, `2 Dec`, and all 10 slots `9 Dec – 10 Jan`)* | **0** | `032` (25 Nov) & `031` (2 Dec) in production; `J2326` maps `033` (9 Dec), `034` (13 Dec), and `030` (16/20 Dec); 6 slots (`23 Dec – 10 Jan`) await `J2327` cohort (`035`–`038`). |
| **Orbit Shorts** (`Mon, Wed, Fri, Sat 11:30`) | **37** | **16** (through Wed 16 Dec `f17XCtUmN-g`) | **21** (`Sat 21 Nov`, `Wed 25 Nov`, `Fri 27 Nov`, `Sat 28 Nov`, `Sat 5 Dec`, `Sat 12 Dec`, plus all **15** slots `18 Dec – 9 Jan`) | **3** (`Tue 10 Nov` `ffYKoNVPoqg`, `Thu 12 Nov` `N42gKBbD7tE`, `Tue 17 Nov` `kKN8Ale42sE`) | Slot `J2248` (`024` muons) at **Sat 21 Nov 11:30** (not Mon 9 Nov). Do **not** air `032` Short 1 at **Wed 25 Nov 11:30** (before 18:00 long) or `031` Path B at **Wed 2 Dec 11:30**. Cap `032` & `031` at **2 Shorts each**. `033`/`034` Shorts (`J2317`–`J2320`) cover `18, 19, 21, 23 Dec`. |
| **HOS Longs** (`Thu 18:00`) | **9** | **2** (`12 Nov` `ETynHpIYLeY` [`007`], `10 Dec` `uAomPaOBrM8` [`099`]) | **7** (`19 Nov` [`008`], `26 Nov` [`009`], `3 Dec` [`010`], `17 Dec` [`013`], `24 Dec` [`012`], `31 Dec` [`014`], `7 Jan` [`015`]) | **0** | Resolve `Thu 10 Dec 18:00` collision between scheduled `099` compilation `uAomPaOBrM8` and planned `011` *Anesthesia*. |
| **HOS Shorts** (`Sat, Fri, Sun, Tue 11:30`) | **38** | **5** (`Sun 8 Nov` `PFj6172YU4Q`, `Fri 13 Nov` `cLKDiYP55J8`, `Sun 15 Nov` `Wvjd8g0CpzE`, `Tue 17 Nov` `xgx2lYHhYZM`, `Sat 21 Nov` `Bks_JLId1ew`) | **33** (**3** in `7–15 Nov` [`Sat 7, Tue 10, Sat 14`], **10** in `20 Nov – 6 Dec` [`J2230` window], and **all 20** in `8 Dec – 10 Jan`) | **2** (`Mon 16 Nov` `xzKoHg0E0_U`, `Wed 18 Nov` `ChbsigHD5_o` [`J2272`]) | Do not duplicate `J2230` (18 Nov – 6 Dec). After 6 Dec, all 20 HOS Short slots are empty on YouTube, and 2 Shorts per new weekly long leaves a structural gap of 2 HOS Short slots per week unless filled by approved back-catalogue cuts. |
