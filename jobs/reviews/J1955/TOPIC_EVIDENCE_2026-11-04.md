# J1955 — `OWB:059` Olympus Mons Topic Neighbours, Competition & Audience Evidence Report (4 November 2026)

- **Job:** `J1955` (`059 Olympus Mons: verify topic neighbours and audience evidence`)
- **Film / Stage:** `OWB:059` (`02_Video-Projects/059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons`, stage `topic`)
- **Worker:** `gemini` (Gemini 4 Argon High, specialist review worker on Mac mini)
- **Preceding Chief Rulings Inspected:**
  - `jobs/reviews/J1801/CHIEF_TOPIC_RULING_2026-11-04.md` (`FIX / topic not locked`)
  - `jobs/reviews/J1800/CHIEF_HANDOFF_2026-11-04.md` (`FIX / script not locked`)
  - `jobs/reviews/J1802/CHIEF_SOURCES_RULING_2026-11-04.md` (`FIX / sources not approved`)
- **Dependent Elected-Chief Job:** `J1953` (`059 Olympus Mons: restore script review and dependent lock checks`)
- **Linked Sources Verification Jobs:** `J1956` (formal Gemini `facts` via `agy`) → `J1957` (direct `MUST QUOTE` verification)
- **Spend:** **£0 / 0 credits** (no paid vidIQ API, no ElevenLabs, no Vertex/Flow generation, no YouTube/Studio writes)
- **Capabilities:** No `audio_input` or `moving_video_input` required or claimed (`chief_relay.py capabilities --agent gemini --available ''`)

---

## 1. Executive Recommendation to Dependent Chief Job (`J1953`)

**Recommendation: `DEFER` topic lock and script advancement for `OWB:059` Olympus Mons (retain `059` as an unlocked candidate with `topic: review/blocked` and `script: review/blocked`; allow already-queued no-spend diagnostics `J1956` Gemini `facts` and `J1957` direct quote check to complete as ordered by `J1802`, but DO NOT lock the topic/script or advance to VO/picture production now).**

### Why `DEFER` (and Neither `LOCK NOW` Nor `REJECT`)

1. **Public Neighbour Pool & Signed-Out Competition PASS (`4/5` — Do Not Reject):**
   - Although historic `J0757` (`IDEAS_2026-10-21_J0757.md` and the 21 Oct `PRE_BUILD_VIDIQ_AUDIT.md`) used fabricated/grouped titles and unsourced view ranges (*"Astrum — Olympus Mons & Valles Marineris: The Megastructures of Mars (1.5M+)"*, *"SciShow Space / Kurzgesagt — Why Mars Has the Largest Volcano in the Solar System (1.2M–4M+)"*, *"ESA Mars Express / National Geographic / BBC Earth — Mars Volcanoes & Hidden Glaciers (1.2M–3M+)"* — none of which exists on YouTube), independent `yt-dlp` verification on `2026-11-04 13:00–13:02 UTC` establishes **8 real education/space neighbour videos at `1.02M–3.39M` views**:
     - **2 standalone single-topic Olympus Mons videos >1M views:** `QXpzNNARzGI` (**2,547,315 views**, Dreksler Astral *Climbing Olympus Mons - Tallest Planetary Mountain in the Solar System*) and `XtyNUyiJPWI` (**1,015,622 views**, The Friendly Brain *TALLEST Mountain In The SOLAR SYSTEM*).
     - **2 solar-system mountain-scale explainers >1M views climaxing with Olympus Mons:** `OomsL_8Cd6E` (**3,388,084 views**, Corridor Crew *VFX Artist Reveals the TRUE SCALE of Mountains*, Ch. 11 *Olympus Mons* `08:15–09:50`) and `XKmbZdWZsXk` (**1,021,296 views**, Dreksler Astral *Tallest Mountains in the Solar System*).
     - **4 Mars geology/astronomy education longs >1.1M views with dedicated Olympus Mons / volcano sections:** `70Qi4Nk3aJc` (**1,590,589 views**, PBS Eons *A Natural History of Mars*), `I-88YWx71gE` (**1,474,151 views**, CrashCourse *Mars: Crash Course Astronomy #15*, Ch. 3 *Surface Features of Mars*), `wFTGP7-n3J8` (**1,428,732 views**, Astrum *What They Didn't Teach You in School About Mars*, Ch. 3 *Geology and differences*), and `NXbCNAIIAxw` (**1,108,660 views**, Astrum *Our Solar System's Planets: Mars - In 4K Resolution*, Ch. 8 *Canyons and volcanoes*).
   - Signed-out exact-title competition check shows **0 collisions** on YouTube.
2. **Strategy Short-First Prerequisite Is UNMET (`1/5` — Blocking Topic Lock):**
   - Under `FAMILIAR_DANGER_STRATEGY.md` (*Measure*: *"A new long is only made on a topic whose Short already cleared 200 views and 40% stayed"*) and `J1801` (*"Check the strategy prerequisite: an OWB Short on this topic with at least 200 views and 40% stayed, with id/date/analytics evidence. If absent, report it as unmet; no Short production is authorised by this brief. Do not substitute unrelated Mars performance or the draft 058 continuity promise for topic approval."*), `OWB:059` requires a matching channel Short with **both `>=200` views AND `>=40%` stayed-to-watch**.
   - Verification of `05_Analytics/owb/snapshots/2026-11-04.json` (184 videos), `05_Analytics/owb/studio_ctr.json` (`2026-11-03T07:03:36Z`), `05_Analytics/owb/REPORT.md` (`2026-11-04`), `00_Brand/Channel-Setup/social/UPLOADS.json`, and `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/TEST_LOG.md` confirms **0 OWB Shorts exist (public, private, or scheduled) on Olympus Mons or Martian volcanoes**.
   - Even OWB's unrelated `025` Mars rover/helicopter uploads (`Js6EQJ8qDi8` Long + Shorts `B1z2dv7m7Vk`, `TtgHNLXfDSs`, `bSjWiCbB7pY`, `iyvWYFP_ETA`) are all **Private ahead of `2026-11-08` with `0` public views**, and `mars_radiation_3months_v01` (cited in `J0757`) is an un-uploaded local `025` draft.
3. **Channel Balance & Focus Priority Put HOS and Earlier OWB Cohort First:**
   - `python3 scripts/channel_balance.py --hos "/Users/benjaminoats/YouTube/History Of Science"` on `2026-11-04T12:59Z` reports **History of Science first**: HOS has **2/4 complete for 2026-11** (`[006 007 008* 009*]`, plus `010*` for 2026-12), whereas Orbit With Ben has **5/4 complete for 2026-11** (`[024 025 026 027 028]`) and **1/4 complete for 2026-12** (`[029]`), plus `030` Apophis in AR finishing (`J1471`/`J1356`), `031`/`032` in VO listening review (`J1752`/`J1753`), and earlier unlocked candidates (`033` Uranus `ZpEA8stoSPA` at 461 day-1 views, `032` Titan `RLSJm59OSzI`, `034` Pluto `gmzaCfJF1gA`, `038` Voyager `kKN8Ale42sE`) with dedicated Shorts in the `24 Oct – 17 Nov` test cohort.
4. **Scientific & Editorial Prerequisites (`J1800` & `J1802`) Remain Outstanding:**
   - The working title's *"Three Times Taller Than Mount Everest"* comparison is provisional pending `J1956` (formal Gemini `facts` via `agy`) and `J1957` (direct `MUST QUOTE` verification) resolving MOLA datum height (`21.287 km` vs Everest's `8.848 km` = `2.41×`) against Amazonis Planitia relief (`26–27 km` = `~2.9–3.05×`) and Mauna Loa's ocean-floor base (`~9–10 km`), alongside the other `J1800`/`J1802` flags (`70 km` lithosphere/hotspot certainty, `600 Pa` vs `6.36 mbar` conversion, `2 Mya` lava vs last `20%` of Martian history, basalt composition provenance, missing `Sjogren`/`Garvin` `WHO:` years, claim-led `<0:30` cold open, single-idea `DATA:` graphics, and `15–20 s` end-screen hold).

---

## 2. Individually Verified Education / Space Neighbours (`yt-dlp`, `2026-11-04 13:01 UTC`)

Channel names are internal notes only and must never appear in public listings (`STUDIO_PLAYBOOK.md` §2).

### A. Verified Education / Space Videos at ≥1M Views

| # | Views (`2026-11-04`) | Video ID & URL | Exact Title | Uploaded · Length | Channel (internal) | Coverage & Shared Subject Words |
|---|---------------------:|----------------|-------------|-------------------|--------------------|---------------------------------|
| 1 | **2,547,315** | `QXpzNNARzGI` (`https://www.youtube.com/watch?v=QXpzNNARzGI`) | *Climbing Olympus Mons - Tallest Planetary Mountain in the Solar System* | 2020-03-23 · 11:03 (663 s) | Dreksler Astral (181k subs) | **Direct single-topic Olympus Mons long.** 6 chapters (*Exploring Olympus Mons*, *The journey to Mars*, *Planning the climb*, *Landing and low gravity*, *The Martian trek*, *Reaching the summit*). Words: `Olympus Mons`, `tallest mountain`, `tallest planetary mountain in the solar system`, `tallest volcano`, `Mars`, `volcano`, `climbing Olympus Mons`. |
| 2 | **3,388,084** | `OomsL_8Cd6E` (`https://www.youtube.com/watch?v=OomsL_8Cd6E`) | *VFX Artist Reveals the TRUE SCALE of Mountains* | 2024-03-24 · 9:50 (590 s) | Corridor Crew (7.19M subs) | **Direct mountain-scale explainer climaxing with Chapter 11 *Olympus Mons* (`08:15–09:50`).** Compares Mount Everest (`01:36–02:25`), Earth's largest volcano base (`06:04–08:15`), and Olympus Mons's shield, cliff scarp, gentle slope, and caldera. Words: `true scale of mountains`, `Mount Everest`, `biggest mountain on Earth`, `Olympus Mons`. |
| 3 | **1,021,296** | `XKmbZdWZsXk` (`https://www.youtube.com/watch?v=XKmbZdWZsXk`) | *Tallest Mountains in the Solar System* | 2018-06-26 · 6:30 (390 s) | Dreksler Astral (181k subs) | **Direct solar-system mountain comparison.** Compares peaks across the Moon, Venus, Mars (Olympus Mons), Vesta, Io, Saturn's moons, and Pluto. Words: `tallest mountains in the solar system`, `highest mountains in the solar system`, `Mars`, `Olympus Mons`. |
| 4 | **1,015,622** | `XtyNUyiJPWI` (`https://www.youtube.com/watch?v=XtyNUyiJPWI`) | *TALLEST Mountain In The SOLAR SYSTEM* | 2017-12-15 · 4:21 (261 s) | The Friendly Brain (18.3k subs) | **Direct single-topic Olympus Mons vs. Everest & Mauna Loa explainer.** Chapters: *OLYMPUS MONS* (`0:25–0:46`), *2.5X MARIANAS TRENCH* (`0:46–2:56`), *TECHTONIC PLATES* (`2:56–4:21`). Words: `largest volcano in the solar system`, `tallest mountain`, `Olympus Mons`, `Mount Everest`, `Mauna Loa`, `biggest volcano`, `tectonic plates`. |
| 5 | **1,590,589** | `70Qi4Nk3aJc` (`https://www.youtube.com/watch?v=70Qi4Nk3aJc`) | *A Natural History of Mars* | 2023-05-09 · 12:27 (747 s) | PBS Eons (3.22M subs) | **Direct Martian geological history long.** Covers Mars's 4.5-billion-year geologic evolution, Tharsis/Olympus Mons volcanism, crustal cooling, and water loss. Words: `Mars`, `natural history of Mars`, `red planet`, `Mars water`, `orbiters`, `rovers`. |
| 6 | **1,474,151** | `I-88YWx71gE` (`https://www.youtube.com/watch?v=I-88YWx71gE`) | *Mars: Crash Course Astronomy #15* | 2015-04-30 · 10:11 (611 s) | CrashCourse (17.3M subs) | **Direct Mars astronomy & geology education long.** Chapter 3 *Surface Features of Mars* (`02:01–03:29`) covers Olympus Mons, Tharsis, Valles Marineris, and stationary-crust volcano growth. Words: `Mars`, `surface features of Mars`, `Olympus Mons`, `Tharsis`, `Valles Marineris`, `Martian atmosphere`. |
| 7 | **1,428,732** | `wFTGP7-n3J8` (`https://www.youtube.com/watch?v=wFTGP7-n3J8`) | *What They Didn't Teach You in School About Mars \| Our Solar System's Planets 4K* | 2024-07-08 · 18:31 (1,111 s) | Astrum (2.90M subs) | **Direct Mars geology & exploration long.** Chapter 3 *Geology and differences* (`04:00–07:20`) and Chapter 5 *Active surface phenomena* (`08:28–10:45`) cover Olympus Mons, Tharsis, Valles Marineris, and global dust storms. Words: `Mars`, `red planet`, `solar system`, `planets`, `Mars geology`, `dust storms`. |
| 8 | **1,108,660** | `NXbCNAIIAxw` (`https://www.youtube.com/watch?v=NXbCNAIIAxw`) | *Our Solar System's Planets: Mars - In 4K Resolution* | 2014-05-06 · 11:27 (687 s) | Astrum (2.90M subs) | **Direct Mars 4K overview tagged `Olympus Mons (Extraterrestrial Location)`.** Chapter 5 *Surface features* (`04:53–05:48`), Chapter 6 *Active geology* (`05:48–07:31`), and Chapter 8 *Canyons and volcanoes* (`07:58–09:42`). Words: `Mars`, `Olympus Mons`, `Valles Marineris`, `canyons and volcanoes`, `active geology`, `Viking missions`, `HiRISE`. |

### B. Dedicated Sub-1M Olympus Mons / Martian Volcano Education Videos (`123k–725k` views)

- **`dNz5J2hpuMU` (`https://www.youtube.com/watch?v=dNz5J2hpuMU`)** — *13 volcanoes seen from space* · **724,616 views** (2023-04-10, 12:12, European Space Agency, ESA; includes Mauna Loa `02:14–02:52`).
- **`HmEXbdLIG9A` (`https://www.youtube.com/watch?v=HmEXbdLIG9A`)** — *The Most Complete Video About Mars on YouTube* · **708,804 views** (2025-06-03, 4:18:30, Astrum Extra).
- **`ySFpJ-clnzU` (`https://www.youtube.com/watch?v=ySFpJ-clnzU`)** — *Mars' Largest Volcano - Olympus Mons* · **404,036 views** (2013-04-03, 2:49, Storm / Discovery *How the Universe Works*).
- **`zfSTsSijGpU` (`https://www.youtube.com/watch?v=zfSTsSijGpU`)** — *What If You Climbed the Highest Mountain in the Solar System?* · **240,001 views** (2022-02-25, 7:28, What If).
- **`Nug6iuKowRk` (`https://www.youtube.com/watch?v=Nug6iuKowRk`)** — *The Biggest Volcano in the Solar System* · **223,241 views** (2015-04-14, 3:55, SciShow Space — refutes `J0757`'s unsupported `1.2M–4M+` claim).
- **`hBLRfgFT7Xc` (`https://www.youtube.com/watch?v=hBLRfgFT7Xc`)** — *Inside Monster Martian Volcanoes* · **173,960 views** (2014-12-15, 4:02, Science Channel *Strip the Cosmos*).
- **`8qdYCpSW2eY` (`https://www.youtube.com/watch?v=8qdYCpSW2eY`)** — *The Biggest Volcano Ever is in Space! \| SciShow Kids* · **155,780 views** (2025-04-28, 5:48, SciShow Kids).
- **`1BPNVtCgAbk` (`https://www.youtube.com/watch?v=1BPNVtCgAbk`)** — *Traces of life on Mars: Olympus Mons* · **131,962 views** (2008-09-18, 0:47, European Space Agency, ESA).
- **`9CDMW_cnaTQ` (`https://www.youtube.com/watch?v=9CDMW_cnaTQ`)** — *Why Is Mars' Olympus Mons So Big?* · **124,381 views** (2021-11-21, 5:32, Cosmoknowledge).
- **`l_nfpDhj7JY` (`https://www.youtube.com/watch?v=l_nfpDhj7JY`)** — *Active Volcanoes on Mars?* · **123,565 views** (2021-05-21, 5:37, SciShow Space).

---

## 3. Updated Artifacts & Preserved Draft Integrity

### Updated / Created in `J1955`
1. `02_Video-Projects/059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons/11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md` (created from `00_Brand/Channel-Setup/templates/TOPIC_OPPORTUNITY_SCORE.md` with verified `2026-11-04` Tier A/B neighbour tables, refutation of unsupported `J0757` claims, Short-first analytics check, overlap matrix, and explicit `DEFER` recommendation to `J1953`).
2. `02_Video-Projects/059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons/11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` (repaired: unsupported historic `J0757` vidIQ scores `96`/`95`/`93` and `High`/`Med`/`Low` labels marked `UNKNOWN`; grouped placeholder neighbours replaced with individually verified URLs/views; signed-out exact-title competition table added; datum-safe backup title added alongside provisional `3× Everest` titles; `J1800` & `J1802` fixes mapped into Section 5; Section 7 left UNSIGNED).
3. `02_Video-Projects/059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons/11_Upload-Package/PRODUCTION_CHECKLIST_V2.md` (refreshed obsolete AI Studio / `8–9 min` template lines to current Vertex-only, `7–9 min`, `15–20 s` end-hold, and `J1800`/`J1801`/`J1802` gate requirements).

### Preserved Untouched (Verified SHA-256 Hashes)
- `bee43283101e4e9716d4f40ae4b9887dc10bd9d4150cfa7cc19bb99c2c2f1fd3  02_Video-Projects/059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons/01_Script/SCRIPT_NOTES_v00.md`
- `634fb966b8164039ffe196780256db5e12208d8c21d70f340ed49a4a517786e3  02_Video-Projects/059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons/01_Script/SCRIPT_NOTES_v01.md`
- `27c8cb446de9210e2fbaaf62ce1be11208ae15f8c9326470c95716f789a7ca19  02_Video-Projects/059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons/01_Script/SOURCES.md`
- `eb24e508f3927c34c39c0b797c9e78762753c736fc5ce3ddc5d8a10a209770df  02_Video-Projects/059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons/01_Script/episode_script_draft_v01.md`
- `b8643ff7fff6929692a3180dbe911ec47d720634f6ddb7fa380c3d4029d716aa  02_Video-Projects/059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons/01_Script/olympus_mons_script_master_v00.md`
- `eb24e508f3927c34c39c0b797c9e78762753c736fc5ce3ddc5d8a10a209770df  02_Video-Projects/059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons/01_Script/olympus_mons_script_master_v01.md`
