# Pre-build topic & packaging audit — Orbit With Ben (`048` Ceres)

**Hard gate:** Run **before** locking topic, script, VO, prompts, or picture generation for any new long.  
**Goal:** Every episode is aimed at **views + full-video watch** using verified public YouTube, neighbour, and channel analytics evidence — never invented numbers or paid API calls.  
**Docs in force (precedence order):** `AGENTS.md` → `00_Brand/Channel-Setup/FAMILIAR_DANGER_STRATEGY.md` → `THUMBNAIL_AND_TITLE_RULES.md` → `STUDIO_PLAYBOOK.md` → `docs/ORBIT_PLAYBOOK_LESSONS.md`.  
**Refreshed current rules (replacing obsolete Growth System v2 / AI Studio / paid vidIQ template lines):**
- **No spend on keyword/title tools:** Paid vidIQ fields stay `UNKNOWN` (no paid API or subscription top-up). Neighbour, search, and exact-title competition checks use signed-out public YouTube via `yt-dlp` and channel analytics snapshots (`05_Analytics/owb/`).
- **Short-first gate (`FAMILIAR_DANGER_STRATEGY.md` §Measure):** No new long topic is locked until a matching channel Short has cleared **≥200 views AND ≥40% stayed-to-watch** (not average % viewed), unless Chief explicitly rules otherwise. J1934 granted **no waiver** and authorised **no new Short production**.
- **Runtime & word count lock (`STUDIO_PLAYBOOK.md` §3):** **7–9 minutes** (about **1,200–1,300 spoken words**), 4–6 acts.
- **First 30–60 seconds (`STUDIO_PLAYBOOK.md` §3, `AGENTS.md` Lesson 7, J1934 FIX #1):** Frame 0–3 s shows the danger/subject moving (no Orbit, no title card, no whole planet as a Veo/Omni start frame). Short claim-led opening sentence; **concrete causal answer to the title before 0:30** (no multi-question stack or agenda); stakes by 0:15; one main question by ~0:45–0:50; no `[CHAPTER CARD]` before 0:30; never two code graphics back to back.
- **Teach on screen & per-chapter teaching gate (`AGENTS.md`, 11–12 Oct 2026, J1934 FIX #2):** `DATA ≥ 3` (each with `SCALE:`), `WHO` card at first mention of every named person with sourced years and in-period role, `WHEN` call-outs + one animated build-up timeline for `≥3` dates (historical dates as spoken, not bundling orbital periods into timeline events), `FACT` 2–4 (`≤4` words, exact word-for-word substring of spoken VO), and one `NUMBER OBJECT` per chapter (`WORDS` matching spoken VO word-for-word; one idea per graphic; real moving imagery between graphics).
- **Picture & compute locks (`STUDIO_PLAYBOOK.md` §5, `AGENTS.md` Lesson 3 & 7, J1934 FIX #3):** **Vertex AI only** (world plates via Vertex Veo; Orbit character motion only via Vertex Omni `gemini-omni-flash-preview` from location `global`, max 2 Orbit beats; stills from verified unlabelled NASA plates or Vertex image; code graphics via Codex `gpt-6-astra`; Test & Compare B thumbnails via Codex `gpt-image-2`). **Never AI Studio prepaid credit.** **No Orbit on any thumbnail.** Sourced diagrams, charts, topographic/gravity maps, simulated perspective views, elevation maps, and interior illustrations **FAIL `picture_qa.py`** and must not be used as plates.
- **Mid-film subscribe beat & end-of-film hold (`STUDIO_PLAYBOOK.md` §3 & §7, `ORBIT_PLAYBOOK_LESSONS.md` §2, J1934 FIX #5):** Exactly one `[SUBSCRIBE BEAT]` at 25–50% of spoken words (`≤20` words from `templates/SUBSCRIBE_BEAT_LINES.md`, no numbers, no stock phrases). **No outro, no goodbye, and no second subscribe ask.** The last spoken line hands off to the confirmed next film; moving picture holds **15–20 s** after the last VO word (end-screen space), music carries **2–3 s** past the last word then fades over **~10 s**, and picture fades over the last **2 s**.

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | `048_Why-Dwarf-Planet-Ceres-Has-Glowing-Salt-Domes-In-The-Asteroid-Belt` |
| Working title | Why Does Dwarf Planet Ceres Have Glowing Salt Domes in the Asteroid Belt? |
| Folder / listing variant | Why Dwarf Planet Ceres Has Glowing Salt Domes in the Asteroid Belt |
| Date pulled | `2026-11-04 10:23–10:25 UTC` (`yt-dlp` public YouTube search & watch pages + `05_Analytics/owb/snapshots/2026-11-04.json` + `studio_ctr.json` `2026-11-03T07:03:36Z`). Job **J2006** by `gemini`. |
| Credits used | **0** (no paid vidIQ API, no TTS, no Vertex/Flow spend) |
| Brand guardrails | Wonder over fearbait · no conspiracy · Orbit DNA · no channel names in listing |
| Neighbour pass | **Medium / Borderline.** 2 strict direct Ceres/Dawn videos >1M (`2.96M`, `1.38M`), 1 asteroid-belt/Ceres CrashCourse episode >1M (`1.34M`), 2 dwarf-planet explainers naming/covering Ceres >1M (`1.92M`, `1.59M`), 1 SEA dwarf-planet documentary with a Ceres chapter at `0.94M` (≈1M), 2 Astrum Ceres/Dawn videos at `0.82M`, and V101 SPACE's Oct 2025 Ceres long at `543k` in 18 days. Full tables: `TOPIC_OPPORTUNITY_SCORE.md`. |
| Short-first proof | **FAIL (1/5 — Not Met).** 0 channel Shorts exist on Ceres, Dawn, Occator Crater, or Ahuna Mons; adjacent asteroid (`gJwNJN_yMKU`, 458 views, **34.2% stayed**) and Europa (`pII09FbRYGc`, 291 views, **16.7% stayed**; `keXe1GNxWSU`, 206 views, **15.8% stayed**) Shorts all miss `≥40%` stayed-to-watch. No waiver granted in J1934. |
| J2006 Recommendation | **DEFER (`OWB:048` remains unlocked and blocked from advancement/production pending J2007 Chief decision).** |

---

## 1. Success targets (this episode)

| Metric | Target | Current Status (`2026-11-04`) |
|--------|--------|-------------------------------|
| Title shape & length | One of the 6 winning shapes (`THUMBNAIL_AND_TITLE_RULES.md` §1); familiar/clear subject noun + hook; prefer ≤ ~60 chars; no копия of live video | Candidate A (58 chars) / Working H1 (73 chars); **0 exact-title collisions on YouTube** (verified below). |
| Primary keyword overall | Public YouTube demand + neighbour subject words (paid vidIQ scores stay `UNKNOWN`) | `dwarf planet Ceres` / `Ceres bright spots` / `NASA Dawn Ceres` verified across 543k–2.96M peer videos. |
| Hook promise | Short claim-led sentence 1 + concrete causal answer before `0:30` + one main question by `~0:50` | **FIX required in v02 (J1934 FIX #1):** v01 cold open is 168 words (~67.2 s at 150 wpm) and stacks questions in paragraph 3. |
| Retention design | 6 acts (7–9 min / 1,200–1,300 spoken words), 1 idea per code graphic, 15–20 s end hold | **FIX required in v02 (J1934 FIX #2, #3, #5):** unbundle multi-metric DATA windows, replace sourced maps/diagrams, fix 2–3 s end hold to 15–20 s. |
| Packaging | Top-band 2–3 word hook (`THUMBNAIL_AND_TITLE_RULES.md` §2.B), no Orbit on thumb, HSV sat ≥100, near-black ≤30%, readable at 168×94 | Concept defined below; not rendered (blocked from production). |

---

## 2. Keyword & demand research (public YouTube + channel analytics; paid vidIQ `UNKNOWN`)

Paid vidIQ metrics (`Overall`, `Est./mo`, `Comp`) are **not pulled (`UNKNOWN`)** under the studio no-spend policy. Evidence below comes from signed-out YouTube search/watch pages (`2026-11-04T10:24Z`) and OWB channel analytics (`05_Analytics/owb/REPORT.md` `2026-11-04`, `OWB_2026-10-18.md`).

| Keyword / Search Phrase | Overall (paid vidIQ) | Est./mo (paid vidIQ) | Comp (paid vidIQ) | Observed Public YouTube & Channel Evidence (`2026-11-04`) | Role (title / desc / chapter / Shorts) | Keep? |
|-------------------------|---------------------:|---------------------:|------------------:|-----------------------------------------------------------|----------------------------------------|-------|
| `dwarf planet ceres` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | Top education/space results: `0w6KRajHMlo` (2.96M), `OGiEkHZZrIs` (1.92M), `nJiw2NxqoBU` (1.38M), `13eztn3RxQw` (824k), `7glhGmoneQo` (543k in 18 days, uploaded 2025-10-17). | Primary (title + desc line 1 + tags) | Yes |
| `ceres bright spots` / `occator crater` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | Core mystery hook of NASA's *Dawn* mission: `nJiw2NxqoBU` (1.38M), `13eztn3RxQw` (824k), `8er_0yY1S1o` (315k *Ceres Rotation and Occator Crater*), `Fs3fODU9P0w` (125k StarTalk *What Is The Bright Spot on Ceres?*), `ZVBHclVvJ7s` (115k Anton Petrov *Surprising New Findings Inside a Crater on Ceres*). | Secondary (open VO + Ch. 3 + thumb hook + tags) | Yes |
| `nasa dawn ceres` / `dawn spacecraft` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | Shared across `0w6KRajHMlo` (2.96M), `nJiw2NxqoBU` (1.38M), `13eztn3RxQw` (824k), `R1OICuZtypk` (824k), `7glhGmoneQo` (543k). | Secondary (desc + Ch. 2–3 + tags) | Yes |
| `asteroid belt` / `dwarf planets` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | Umbrella education cluster: `OGiEkHZZrIs` (1.92M), `evIsmxM5c7o` (1.59M), `auxpcdQimCs` (1.34M *Asteroids: Crash Course Astronomy #20*), `SOxAkOOqpKU` (942k *Dwarf Planets: The Lesser Worlds*). | Umbrella (title + Ch. 1 + tags) | Yes |
| `ahuna mons` / `ceres ice volcano` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | Featured in `nJiw2NxqoBU` (1.38M), `0w6KRajHMlo` (2.96M), `13eztn3RxQw` (824k), `lXU7nOv1UDA` (11.6k VideoFromSpace). | Chapter 5 + future Short hook | Yes |
| `ceres ocean` / `ceres subsurface brine` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `6V3WehjinAc` (285k SEA *Could Ceres be Home to Life?*), `Y4B6fqNlfAc` (36.1k *Dwarf Planet Ceres Is an Ocean World*), `kmepueX-rco` (28.4k), `MJ0ND61Exjg` (12.8k). Note: OWB `"space ice"` (2 views) and `006` Europa AVD (22.9%) are adjacent channel context only, **not** Ceres Short proof (J1934). | Chapter 4 & 6 + desc | Yes |

**Decision (draft for future lock):** Primary keyword for title lead = `Dwarf Planet Ceres` (paired with `Glowing Salt Domes` / `Bright Spots` and `Asteroid Belt`).  
**Description first 100 chars must include:** `dwarf planet Ceres`, `asteroid belt`, and `bright salt domes` / `Occator Crater`.

---

## 2b. Neighbour pass (blocking · verified 2026-11-04 in J2006)

Pulled via `yt-dlp` on **2026-11-04 10:23–10:25 UTC**. Full breakdown (Tiers A, B, and C) is in `11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md`. Channel names below are internal notes only — **never** include them in our public title, description, or tags.

| # | Views (`2026-11-04`) | Channel (internal) | YouTube ID & URL | Title | Uploaded · Length | Words we may reuse |
|---|------:|--------------------|------------------|-------|-------------------|--------------------|
| 1 | **2,957,410** | Astrum | `0w6KRajHMlo` (`https://www.youtube.com/watch?v=0w6KRajHMlo`) | *What NASA's Dawn Saw on Ceres and Vesta Stunned Me \| Supercut* | 2022-04-01 · 20:17 | `Ceres`, `Dawn`, `NASA Dawn mission`, `Vesta`, `dwarf planet`, `protoplanet` |
| 2 | **1,383,924** | NASA Jet Propulsion Laboratory | `nJiw2NxqoBU` (`https://www.youtube.com/watch?v=nJiw2NxqoBU`) | *Flight Over Dwarf Planet Ceres* | 2016-01-29 · 3:44 | `dwarf planet Ceres`, `Ceres`, `NASA`, `Dawn spacecraft`, `Occator Crater`, `bright spots` |
| 3 | **1,337,561** | CrashCourse | `auxpcdQimCs` (`https://www.youtube.com/watch?v=auxpcdQimCs`) | *Asteroids: Crash Course Astronomy #20* | 2015-06-04 · 11:33 | `asteroid belt`, `Ceres`, `asteroids`, `Vesta`, `dwarf planet` |
| 4 | **1,923,830** | Free School | `OGiEkHZZrIs` (`https://www.youtube.com/watch?v=OGiEkHZZrIs`) | *Guide to Dwarf Planets: Ceres, Pluto, Eris, Haumea and Makemake for Kids - FreeSchool* | 2017-02-15 · 8:53 | `dwarf planet`, `dwarf planets`, `Ceres`, `Ceres facts`, `Pluto`, `Eris` |
| 5 | **1,591,061** | SciShow Kids | `evIsmxM5c7o` (`https://www.youtube.com/watch?v=evIsmxM5c7o`) | *Meet the 5 Dwarf Planets!* | 2015-07-01 · 4:33 | `dwarf planets`, `Ceres`, `solar system` |
| 6 | **942,301** *(≈0.94M)* | SEA | `SOxAkOOqpKU` (`https://www.youtube.com/watch?v=SOxAkOOqpKU`) | *Dwarf Planets: The Lesser Worlds* (Ch. 3 `05:34–09:15`: *Ceres*) | 2020-12-19 · 27:59 | `dwarf planets`, `minor planets`, `Ceres`, `icy worlds`, `solar system` |
| 7 | **824,012** *(sub-1M peer)* | Astrum | `13eztn3RxQw` (`https://www.youtube.com/watch?v=13eztn3RxQw`) | *The Discoveries On Ceres That Shocked NASA Scientists \| Dawn Mission* | 2019-12-14 · 10:00 | `Ceres`, `Dawn`, `NASA Dawn`, `NASA Ceres`, `what did Dawn discover` |
| 8 | **824,008** *(sub-1M peer)* | Astrum Extra | `R1OICuZtypk` (`https://www.youtube.com/watch?v=R1OICuZtypk`) | *The Great Secret of the Smallest Worlds in Our Solar System* | 2025-04-24 · 1:09:10 | `Ceres`, `Vesta`, `Dawn mission`, `asteroid belt`, `planetesimals` |
| 9 | **543,061** *(18-day breakout)* | V101 SPACE | `7glhGmoneQo` (`https://www.youtube.com/watch?v=7glhGmoneQo`) | *The "Forgotten" Dwarf Planet Between Mars and Jupiter: What NASA Found on Ceres* | 2025-10-17 · 10:48 | `Ceres dwarf planet`, `NASA Ceres mission`, `Dawn spacecraft`, `asteroid belt`, `dwarf planet between Mars and Jupiter`, `Ceres water` |

**Proposed description first line(s)** (using neighbour subject language; wonder brand; no channel names):  
`Why does dwarf planet Ceres have over 300 bright salt spots in the asteroid belt between Mars and Jupiter? When NASA's Dawn spacecraft dipped under 22 miles above Occator Crater, it uncovered sodium carbonate salt domes fed by a 25-mile-deep subsurface brine reservoir and a 3-mile-high ice volcano called Ahuna Mons.`

**Proposed subject-only tags (8, no channel names):**  
`dwarf planet ceres`, `ceres`, `ceres bright spots`, `occator crater`, `nasa dawn mission`, `ahuna mons`, `asteroid belt`, `subsurface ocean`

**Locked title unchanged by this pass?** Topic is **not locked** (DEFERRED by Chief in J1934). Candidate titles below preserve the subject words (`Dwarf Planet Ceres`, `Salt Domes` / `Bright Spots`, `Asteroid Belt`).

---

## 3. Title ABC & Exact-Title Competition Check (`2026-11-04`)

**Rules (`THUMBNAIL_AND_TITLE_RULES.md` §1):** One concrete promise · one of the six winning shapes (or big subject + one hook) · prefer ≤ ~60 characters so it isn't cut off on mobile · no hashtags · no series suffix · no hedged claims · never copy an existing public video title. Paid vidIQ scores stay `UNKNOWN`.

| | Candidate Title | Char Count | Paid vidIQ Score | Shape & Competition Notes | Keep? |
|---|-----------------|-----------:|-----------------:|---------------------------|-------|
| **A** | **Why Does Dwarf Planet Ceres Have Glowing Salt Domes?** | 52 chars | `UNKNOWN` | Question shape ("Why Does…") + named subject (`Dwarf Planet Ceres`) + specific contradiction/hidden feature (`Glowing Salt Domes`). Fits cleanly under 60 chars on mobile. *(Note: J1934 FIX #4 flags checking "glowing" vs "reflective" salts against sources before locking.)* | **Candidate A (short mobile fit)** |
| **B** | **Why Does Ceres Have 300 Bright Salt Spots in Space?** | 51 chars | `UNKNOWN` | Question shape + one real number (`300 Bright Salt Spots`) + honest "reflective/bright" wording matching NASA's `"more than 300 bright features"` if J1934 FIX #4 retires `"glowing"`. | **Candidate B (reflective-salt safe)** |
| **C** | **Why Does Dwarf Planet Ceres Have Glowing Salt Domes in the Asteroid Belt?** | 73 chars | `UNKNOWN` | Current script v01 H1 (`folder: 67 chars`). Names both `Dwarf Planet Ceres` and `Asteroid Belt` (`OWB_2026-10-18.md` §4 item 1), but exceeds ~60 chars on mobile. | **Current draft H1** |
| **Reject** | *What If Dwarf Planet Ceres Hit Earth? \| Orbit's Cosmic Journey* | 62 chars | `UNKNOWN` | Off-lane impact dread (`8VB-jfqrtM4` / `7_sVAcX-ueE` clone) + banned series suffix. | **Reject** |

**Locked title:** *NONE — topic lock DEFERRED by Chief in J1934 (awaiting J2007).*

### Signed-out Exact-Title Competition Check (`yt-dlp`, `2026-11-04T10:23Z`)

Searched both `Why Does Dwarf Planet Ceres Have Glowing Salt Domes in the Asteroid Belt?` and `Why Dwarf Planet Ceres Has Glowing Salt Domes in the Asteroid Belt`. Top 5 results:

| # | Video ID | Views | Channel (internal) | Title | Collision? |
|---|----------|------:|--------------------|-------|------------|
| 1 | `gjd8-srK1qE` | 2 | Orbit Observer | *The Asteroid Belt Hides an Ocean World — and Part of It Is Still Glowing* | **No** (different title; 2-view micro-channel) |
| 2 | `lQCwI3ZO8Jc` | 42 | The Stars and the Night | *Building a Mining Outpost on Ceres \| Real Science Sleep Story* | **No** |
| 3 | `jxOo0-JkMMw` | 1,009 | Discover The Impossible | *The Entire Solar System in 1 Hour — Every Planet, Moon & Mystery* | **No** |
| 4 | `A_RREzgojOU` | 1,719 | Glitch Horizon | *Track 8: Luna DJ's ; Ceres // (Solar System Outward Journey)* | **No** |
| 5 | `jgJVkCtuTbU` | 47 | The Stars and the Night | *A City in the Clouds of Saturn \| Real Science Sleep Story* | **No** |

**Competition verdict:** **PASS (0 exact-title collisions).** Unlike `030` Apophis (where two public videos already used our working title word-for-word), no public YouTube video uses our working title or Candidate A/B. Top broad-topic competitors on Ceres (`0w6KRajHMlo` 2.96M, `13eztn3RxQw` 824k, `7glhGmoneQo` 543k) use general discovery framing (*"What NASA's Dawn Saw on Ceres"*, *"The Discoveries On Ceres That Shocked NASA Scientists"*, *"The 'Forgotten' Dwarf Planet Between Mars and Jupiter"*), leaving the specific **Occator Crater salt-dome / 25-mile-deep brine / Ahuna Mons cryovolcano** question angle open.

---

## 3b. Script reviewer & J1934 Editorial Ruling (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/048_Why-Dwarf-Planet-Ceres-Has-Glowing-Salt-Domes-In-The-Asteroid-Belt/01_Script/ceres_salt_domes_script_master_v01.md
```

- [ ] Score ≥ **90 / 100** **AND** Chief editorial/scientific approval *(Note: `ceres_salt_domes_script_master_v01.md` scored `95.3 / 100` on automated `review:script` on 18 Oct 2026, **but Chief J1934 ruled `script FIX / blocked from lock and production` on 4 Nov 2026** — automated score is not editorial or scientific approval; checkbox left unticked until v02 fixes and formal Gemini `facts` + direct quote checks pass).*

---

## 4. Outlier / competitive patterns (on-brand only)

| Outlier / peer video | Views (`2026-11-04`) | Steal (structure & packaging) | Do **not** copy |
|----------------------|---------------------:|-------------------------------|-----------------|
| `0w6KRajHMlo` *What NASA's Dawn Saw on Ceres and Vesta Stunned Me* (Astrum) | **2.96M** | Spacecraft detective arc: follow *Dawn* closer and closer as orbital altitude drops (`<22 miles` over Occator Crater) to solve the surface mystery. | 20-minute supercut runtime; long 6–15 s shot holds (`AGENTS.md` Polish pass: keep 4–6 s cuts). |
| `7glhGmoneQo` *The "Forgotten" Dwarf Planet Between Mars and Jupiter: What NASA Found on Ceres* (V101 SPACE, 2025-10-17) | **543k in 18 days** | Immediate geographic anchor ("between Mars and Jupiter") + contrast between a "forgotten rock" expectation and an active ocean/brine world. | Slow atmospheric intro; generic "Forgotten Dwarf Planet" label without naming the salt domes / ice volcano. |
| `13eztn3RxQw` *The Discoveries On Ceres That Shocked NASA Scientists \| Dawn Mission* (Astrum) | **824k** | Pair Occator Crater's bright carbonate deposits with Ahuna Mons's 3-mile-high cryovolcano as two surface expressions of the same subsurface brine physics. | Sponsor mid-roll break; unlabelled textbook interior diagrams. |
| `8VB-jfqrtM4` (Ridddle) / `7_sVAcX-ueE` (What If) *What If the Largest Asteroid Hit Earth?* | **5.70M / 1.93M** | Scale comparison of Ceres's ~585-mile (nearly 600-mile) diameter against familiar benchmarks. | **Reject Earth-impact disaster framing** (Ceres is in a stable 2.8 AU main-belt orbit; *Wonder, not dread*). |

**Patterns for a conditional v02 script (if Chief advances `048` in `J2007`):**

- [x] Assumption-flip / open-loop question title  
- [x] Spacecraft altitude-descent chapter journey (`2.8 AU` → `Hubble/Herschel` → `<22 miles` over Occator → `25 miles` deep brine → `3-mile-high` Ahuna Mons → `2.5–4 Ga` hydrothermal core)  
- [x] Everyday scale anchor (`SCALE:` on every `DATA:` marker, e.g., poppy seed vs nickel for 1/13 Earth radius)  
- [x] Midpoint misconception flip (`"Wrong."` at Chapter 3: sodium carbonate + hydrated chloride salts, not ancient pure surface ice)  

---

## 5. Incorporate into the build (including J1934 mandatory v02 fixes)

| Data / Chief J1934 finding | Required change to script v02 / chapters / visuals / packaging (when unlocked) |
|----------------------------|--------------------------------------------------------------------------------|
| **J1934 FIX #1 (Cold open timing & question stack)** | Trim the 168-word (~67.2 s) 3-paragraph cold open: open with a short claim-led sentence, deliver the **concrete causal answer before `0:30`** (sodium carbonate & hydrated salts percolating from subsurface brine, not exposed ice), and land **one main question by `~0:50`**, verified from spoken-word timing rather than text arithmetic. Remove the multi-question stack in paragraph 3. |
| **J1934 FIX #2 (Unbundle numerical catalogues)** | Unbundle the overloaded Hook and Chapter `DATA:` windows (which currently pack distance, radius, spin, mass %, chemistry, and age into single graphics). Each graphic must teach **one idea** with its sourced `SCALE:`, `≤4`-word labels matching spoken VO word-for-word, and real moving imagery between graphics. Animate historical dates (`1801`, `2003–2004`, `2011`, `2012–2013`, `2015`, `2017–2018`, `2020`, `2025`) as spoken; do not preload future dates into the hook or treat orbital periods (`1,682 days`, `9 hours`) as historical timeline markers. |
| **J1934 FIX #3 (Picture QA compliance & portraits)** | Remove all planned sourced topographic/gravity maps, simulated perspective views (`PIA20348`), elevation maps (`PIA20915`), and NASA's 2025 interior illustration from `[VISUAL MUST]` — agency provenance does not exempt diagrams/maps/renders from `picture_qa.py` FAIL. Use real unlabelled graded NASA Dawn imagery (`PIA20350`, `PIA21906`, `PIA22660`, `PIA21079`) + our own per-row animated code graphics (`code_graphic_048_...`). Verify actual public-domain portrait image files and rights for Piazzi, Hubble, and Herschel (LOC authority IDs alone do not license portraits). |
| **J1934 FIX #4 (Scientific verification & quote check)** | Before locking, run formal Gemini `facts` via `agy` and direct `MUST QUOTE` verification on all 7 `TO VERIFY` rows: (a) "glowing" vs "reflective" salts; (b) `>300` bright features globally on Ceres vs inside Occator Crater (note: v01 line 5 says *"inside the fifty-seven-mile-wide Occator Crater, Dawn discovered that more than three hundred bright features..."*, whereas NASA's quote says Ceres globally has `>300` bright features and Occator is home to the most extensive ones!); (c) `0.5-to-2-billion-year` post-formation interval vs a "two-billion-year" duration (`2.0 - 0.5 = 1.5 billion years`); (d) Dawn lowest orbit chronology (`<22 miles / 35 km` reached in June 2018 extended mission); (e) radius/diameter consistency (`296 mi` radius = `592 mi` vs `~585 mi` mean diameter); (f) water inventory and Hubble inference certainty; (g) pingo/freezing/salts causal chain; (h) Aug 20, 2025 Courville et al. model vs observation wording; (i) Bennu hand-off claims. |
| **J1934 FIX #5 (End-of-film hold & `047`/`049` continuity)** | Fix Chapter 6 `[VISUAL MUST]` line 92 (which currently says *"Hold that moving picture for 2–3 seconds past the last word"*) to match `STUDIO_PLAYBOOK.md` §7: **moving plate holds 15–20 s after the last VO word**, music carries **2–3 s** past the last word then fades over **~10 s**, and picture fades over the final **2 s**. Reconcile incoming `047` and outgoing `049` Bennu hand-off against actual locked schedule before VO. |
| **Thumbnail ABC concept (`THUMBNAIL_AND_TITLE_RULES.md` §2.B)** | **Subject:** Real graded NASA Dawn close-up of Occator Crater's gleaming white Cerealia Facula salt dome (`PIA20350`) filling ≥⅓ of frame, with Dawn spacecraft scale reference above the crater rim (no Orbit on thumb). **Top band (2–3 words, house sans, yellow hook word, off subject):** Variant A: **`GLOWING` (yellow) `SALT DOMES`** (or **`BRIGHT` (yellow) `SALT DOMES`** if "glowing" is retired) · Variant B: **`HIDDEN` (yellow) `BRINE OCEAN`** · Variant C: **`3-MILE` (yellow) `ICE VOLCANO`**. HSV saturation ≥120 (or ≥100), near-black ≤30%, verified at 168×94 via `thumb_preview.py long --score`. |

**Chapter list in draft v01 (6 acts, each with one primary `NUMBER OBJECT`):**

1. **The Embryonic Planet Between Giants** — Piazzi's 1801 discovery, 2006 dwarf-planet status, and why Ceres is `1/13` Earth's radius (`296 mi / 476 km`, poppy seed vs nickel) yet holds `25%–35%` of the asteroid belt's mass.  
2. **Twenty-Five Percent Water and Dawn** — Hubble (`2003–2004`) & Herschel (`2012–2013`) water clues, Dawn's `25,700 mph` ion journey via Vesta (`2011`) to Ceres (`2015`), and the global map of `>300` bright faculae. *(Followed by mid-film `[SUBSCRIBE BEAT]` at 44%).*  
3. **Twenty-Two Miles Above Occator Crater** — Midpoint twist (`"Wrong."`): Dawn's `<22-mile (35 km)` low orbit over `57-mile-wide` Occator Crater reveals sodium carbonate + hydrated chloride salts (`<2 Myr` old, dehydrating within `hundreds of years`), proving recent brine percolation.  
4. **A Brine Reservoir Twenty-Five Miles Deep** — Why liquid persists without giant-planet tidal heating: Dawn gravity data reveals a `~25-mile-deep (40 km)`, hundreds-of-miles-wide brine reservoir beneath Occator fractures, plus pingo hills and salt-depressed freezing.  
5. **The Three-Mile-High Lonely Ice Volcano** — Why no crater on Ceres exceeds `175 miles (280 km)` across, and how freezing-point-depressed brine extruded the `3-mile-high (5 km)` cryovolcano *Ahuna Mons*.  
6. **Two Billion Years of Chemical Energy** — Ernutet Crater aliphatic organics, Dawn's October 2018 planetary-protection quarantine orbit, and the Aug 20, 2025 *Science Advances* model showing radiogenic core heating (`0.5–2 Ga` after formation / `2.5–4 Ga` ago) fed a hydrothermal microbial buffet.  

---

## 6. Retention plan (refreshed to current 7–9 min & end-hold locks)

| Time zone | Job | Picture / VO requirement (`STUDIO_PLAYBOOK.md` §3, §5, §7 & J1934) |
|-----------|-----|--------------------------------------------------------------------|
| `0:00–0:05` | Answer image + curiosity claim | Frame 0 is graded NASA Dawn Occator Crater bright salt deposit (`PIA20350`), moving, no Orbit, no title card, no whole-planet start frame. Sentence 1 states the core claim/question cleanly. |
| `0:05–0:15` | Stakes | Why bright water-bearing features inside a dark asteroid-belt crater defied expectations. |
| `0:15–0:30` | Concrete causal answer | Deliver the concrete answer before `0:30` (reflective sodium carbonate and hydrated salts percolating from subsurface brine, not ancient surface ice). At most one code graphic in `0:00–0:30`, with real moving imagery between graphics. |
| `0:30–0:50` | One main question + Ch. 1 card | Land one clear overarching question by `~0:50` (no multi-question stack), then cut to `[CHAPTER CARD: The Embryonic Planet Between Giants]` (0.5–0.8 s breath after sentence end, ~0.4 s xfade). |
| Chapter starts | Re-hook + chapter card | Wait for VO sentence to finish → 0.5–0.8 s breath → ~0.4 s crossfade; never clip a spoken word. |
| `25%–50%` (`~44%`) | Mid-film `[SUBSCRIBE BEAT]` | One line ≤20 words from `templates/SUBSCRIBE_BEAT_LINES.md`, no numbers, no stock phrases, over moving picture. |
| Per chapter | Teach on screen (`NUMBER` + `WORDS`) | One single-idea `NUMBER OBJECT` code graphic per chapter with `≤4`-word labels matching spoken VO word-for-word, separated by real moving plates. |
| Final spoken line | Next-film hand-off (no goodbye) | Hands off to the confirmed next film (reconcile `049` Bennu before lock); no "in conclusion" or second subscribe ask. |
| Post-VO end hold (`+15–20 s`) | End-screen hold (`STUDIO_PLAYBOOK.md` §7) | Moving picture holds **15–20 s** past the last VO word; music carries **2–3 s** past the last word then fades over **~10 s**; picture fades over the last **2 s**. |

- [x] Picture changes every **4–6 s** (no hold >4 s on any card/graphic)  
- [x] Runtime target **7–9 min** (1,200–1,300 spoken words; v01 is 1,239 spoken words / ~8.6 min)  
- [ ] Cold-open timing (`<0:30` causal answer, `~0:50` single question) and 15–20 s end hold fixed in v02 *(pending J2007)*  

---

## 7. Sign-off (block production until checked by Chief)

- [ ] Keywords & demand evidence verified and primary locked by Chief *(J2006 evidence complete; topic lock DEFERRED in J1934; Short-first gate NOT MET)*  
- [ ] Title locked by Chief (zero exact-title collision verified; "glowing" vs "reflective" salt wording pending J1934 FIX #4)  
- [ ] Script reviewer ≥ 90 **plus** J1934 v02 editorial fixes, formal Gemini `facts` pass, and direct `MUST QUOTE` check complete  
- [x] Neighbour & outlier patterns mapped into chapter arc (`TOPIC_OPPORTUNITY_SCORE.md`)  
- [x] Thumb concepts match title promise (one object · top-band 2–3 words · no Orbit)  
- [x] Chapter teach-points listed (6 acts with per-chapter `NUMBER OBJECT`)  
- [ ] Cold-open clock (`0:05` / `0:15` / `0:30` / `0:50`) and `15–20 s` end hold revised in script v02  
- [x] Retention plan updated to current studio locks  
- [x] Production checklist path noted: `11_Upload-Package/PRODUCTION_CHECKLIST_V2.md`  

**Signed off by:**  
**Date:**  

*(Unsigned — `OWB:048` is retained as an unlocked candidate per Chief J1934, and J2006 recommends **DEFER** to dependent Chief job `J2007`. No VO, Vertex Veo/Omni generation, or credit spend is authorised.)*

---

## Tools & References

- Public search & neighbour verification (zero spend): `yt-dlp` watch pages + `11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md`  
- Script reviewer: `cd 07_Content-Ops && npm run review:script -- --file <script.md>`  
- Episode gate: `cd 07_Content-Ops && npm run gate:episode -- --project ../02_Video-Projects/048_Why-Dwarf-Planet-Ceres-Has-Glowing-Salt-Domes-In-The-Asteroid-Belt`  
- Latest channel numbers: `05_Analytics/owb/REPORT.md` & `05_Analytics/owb/studio_ctr.json`  
- Rules in force: `AGENTS.md`, `00_Brand/Channel-Setup/FAMILIAR_DANGER_STRATEGY.md`, `00_Brand/Channel-Setup/THUMBNAIL_AND_TITLE_RULES.md`, `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md`, `docs/ORBIT_PLAYBOOK_LESSONS.md`
