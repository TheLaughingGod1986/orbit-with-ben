# J2710 — OWB:064 & OWB:065 Topic Evidence Repair & Direct NASA Primary-Source Fact Audit (For Parent `J2707`)

- **Job:** `J2710` (`OWB 064 and 065: repair missing topic evidence for J2707`)
- **Parent Job:** `J2707` (`OWB 064 and 065: rule-E topic review and template copy`, currently blocked on `J2710`)
- **Source Brief PRs:** PR #849 (`macbook/J2703`, commit `7e168910da9f62f87525876c8eb7a3d761f0c5de`, OPEN) & PR #850 (`macbook/J2707`, commit `a12f996f990fd6dec36e73389bcb158e0606e1ee`, OPEN)
- **Specialist Worker:** `gemini` (`Gemini 4 Argon High`, Mini review/facts lane)
- **Date:** `2026-11-12` (within the 24-hour Chief repair deadline of `2026-11-13T14:40:00Z`)
- **Spend:** `£0.00` (`0` metered vidIQ credits; `0` ElevenLabs/Vertex/Flow spend; free signed-out YouTube GB public search/autocomplete + direct NASA, NOAA, and GAO primary pages)

---

## 1. Executive Summary & Per-Film Rule-E Recommendations for Parent `J2707`

| Film | Folder & Slug | Primary Search-Led Title (`Rule 26` + `Rule 1/15`) | Neighbour Gate (`≥3` at `≥1M` Views) | Direct NASA Fact Check (`J2710`) | Opportunity Score | Worker Recommendation for Parent `J2707` |
|---|---|---|---|---|---:|---|
| **`OWB:064`** | `02_Video-Projects/064_Where-Do-Shooting-Stars-Come-From` | **`Where Do Shooting Stars Come From?`** (`33 chars`, #1 YouTube GB autocomplete match, `0` collisions) | **PASS (`8` verified `≥1M` neighbours:** `2.60M`, `2.55M`, `1.77M`, `1.76M`, `1.34M`, `1.18M`, `1.10M`, `1.01M`) | **PASS with Hook Fix (`11/11` claims):** Rejected universal sand-sized comet-dust claim (`F64.1`); verified `3200 Phaethon` asteroid Geminids, Halley's dual showers, `11–72 km/s`, `50–100 km`, `48.5 tons/day`, and asteroid meteorites | **`94 / 100`** | **RECOMMEND `GO` as Backlog Candidate #1 in `jobs/WIP.json` `next` (Rule G; no active WIP promotion yet)** |
| **`OWB:065`** | `02_Video-Projects/065_How-Will-The-Space-Station-Fall-To-Earth` | **`What Will Happen to the ISS? (NASA's 420-Ton Deorbit Plan)`** (`58 chars`, #1 autocomplete lead, `0` collisions) / **`How Will the Space Station Fall to Earth?`** (`41 chars`, `0` collisions) | **PASS (`8` verified `≥1M` neighbours:** `12.77M`, `8.58M`, `4.11M`, `2.76M`, `1.65M`, `1.61M`, `1.57M`, `1.12M`) | **PASS with Mandatory Distinctions (`11/11` claims):** Enforced baseline `2030/2031` plan + `2027` GAO assessment vs guaranteed date (`F65.6`), and broad **South Pacific Oceanic Uninhabited Area (`SPOUA`)** vs single Point Nemo coordinate (`F65.8`) | **`92 / 100`** | **RECOMMEND `GO` as Backlog Candidate #2 in `jobs/WIP.json` `next` (behind `064` & coordinated with `25 Nov` Short `AR2` `xdurJQcoiGM`)** |

> **Worker Scope Note (`AGENTS.md`):** This delivery completes the `J2710` evidence repair and primary-source fact audit. It is **not** a Chief topic GO, script lock, or production approval. Both `OWB:064` and `OWB:065` remain in `jobs/WIP.json` `next` (`state: "todo"` in `status.json`), and `01_Script/episode_script_draft_v01.md` in both folders remains the untouched template file. Parent `J2707` (Chief) makes the final Rule-E decision.

---

## 2. Tool & Network Probe Record (Required Before Work by `J2710`)

Per the `J2710` brief (*"Probe your own access before work and record results"*):
1. **Input Capability Probe (`chief_relay.py capabilities`):** Recorded `--available ''` with evidence that this session has text/web tools (`read_file`, `search_web`, `run_command`) and makes no claim of `audio_input` or `moving_video_input` media perception.
2. **Signed-Out YouTube GB Autocomplete & Public Search Probe:** Verified direct HTTP `200` access from the Mini to:
   - `https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl=en-GB&gl=GB&q=...`
   - `https://www.youtube.com/results?hl=en-GB&gl=GB&search_query=...` (`ytInitialData` `videoRenderer` extraction returning exact video IDs, titles, channel names, observed view counts, lengths, and ages on `2026-11-12`).
3. **Direct NASA, NOAA & GAO Primary-Source Probe:** Verified direct HTTP `200` access and extracted verbatim quotes from:
   - `https://science.nasa.gov/solar-system/meteors-meteorites/`
   - `https://science.nasa.gov/solar-system/meteors-meteorites/facts/`
   - `https://science.nasa.gov/solar-system/meteors-meteorites/meteor-showers/`
   - `https://science.nasa.gov/solar-system/meteors-meteorites/geminids/`
   - `https://science.nasa.gov/solar-system/meteors-meteorites/perseids/`
   - `https://science.nasa.gov/solar-system/meteors-meteorites/eta-aquarids/`
   - `https://science.nasa.gov/solar-system/meteors-meteorites/orionids/`
   - `https://science.nasa.gov/solar-system/comets/1p-halley/`
   - `https://science.nasa.gov/solar-system/comets/109p-swift-tuttle/`
   - `https://spaceplace.nasa.gov/meteor-shower/en/`
   - `https://science.nasa.gov/earth/earth-atmosphere/earths-atmosphere-a-multi-layered-cake/`
   - `https://www.nasa.gov/blogs/watch-the-skies/2010/08/12/how-low-can-they-go/`
   - `https://www.nasa.gov/blogs/watch-the-skies/2020/12/09/the-geminids-best-meteor-shower-of-the-year/`
   - `https://www.nasa.gov/blogs/watch-the-skies/2026/03/26/its-fireball-season-answering-your-meteor-questions/`
   - `https://www.nasa.gov/international-space-station/space-station-facts-and-figures/`
   - `https://www.nasa.gov/faqs-the-international-space-station-transition-plan/`
   - `https://www.nasa.gov/news-release/nasa-selects-international-space-station-us-deorbit-vehicle/`
   - `https://www.nasa.gov/wp-content/uploads/2015/01/2022_iss_transition_report-final_tagged.pdf`
   - `https://spaceplace.nasa.gov/spacecraft-graveyard/en/`
   - `https://spaceplace.nasa.gov/whats-in-the-atmosphere/`
   - `https://www.nasa.gov/history/SP-4225/multimedia/deorbit.htm`
   - `https://www.nasa.gov/history/45-years-ago-skylab-reenters-earths-atmosphere/`
   - `https://oceanservice.noaa.gov/facts/nemo.html`
   - `https://www.gao.gov/products/gao-26-107805`
4. **Template Integrity Verification (`a12f996f990fd6dec36e73389bcb158e0606e1ee`):** Confirmed all 11 non-audit template files in each film (`01_Script/episode_script_draft_v01.md`, `02_Voiceover/README.md`, `04_Generated-Clips/01_Raw/.gitkeep`, `07_Edit-Project/.env.example`, `07_Edit-Project/_generate_veo_from_beats.py`, `07_Edit-Project/beats.json`, `08_Thumbnail/README.md`, `10_Shorts/README.md`, `11_Upload-Package/PRODUCTION_CHECKLIST_V2.md`, `README.md`, `production-status.md`) remain byte-for-byte identical to `02_Video-Projects/_template_NNN_Episode-Slug/`.

---

## 3. Summary of Evidence Repaired for `OWB:064` (*Where Do Shooting Stars Come From?*)

### 3.1 Repaired Files in `02_Video-Projects/064_Where-Do-Shooting-Stars-Come-From/`
- [`TOPIC.md`](../../../02_Video-Projects/064_Where-Do-Shooting-Stars-Come-From/TOPIC.md)
- [`TOPIC_OPPORTUNITY_SCORE.md`](../../../02_Video-Projects/064_Where-Do-Shooting-Stars-Come-From/TOPIC_OPPORTUNITY_SCORE.md) & [`11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md`](../../../02_Video-Projects/064_Where-Do-Shooting-Stars-Come-From/11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md)
- [`11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`](../../../02_Video-Projects/064_Where-Do-Shooting-Stars-Come-From/11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md)
- [`11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md`](../../../02_Video-Projects/064_Where-Do-Shooting-Stars-Come-From/11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md)

### 3.2 Key Findings (`OWB:064`)
1. **Rule 26 Search Phrase & Ranking Videos:**
   - Exact query `"where do shooting stars come from"` returns `["where do shooting stars come from", "where do meteors come from"]` in signed-out YouTube GB autocomplete (#1 match).
   - Two ranking videos: `IxDR-dASDNw` (*Has a shooting star ever landed on someone?*, Mystery Science, **2,546,192 views**) and `TuDfZ2Md5x8` (*Meteors: Crash Course Astronomy #23*, CrashCourse, **1,098,018 views**).
   - **0 exact-title collisions** across all 4 Long title candidates (`Where Do Shooting Stars Come From?`, `Where Do Shooting Stars Come From? (Not All of Them Are Comets)`, `Halley's Comet Left a Trail (And Earth Hits It Twice a Year)`, `What NASA's All-Sky Cameras Revealed About Meteor Showers`) and both Short titles.
2. **Neighbour Pass (`8` Verified `≥1M`-View Education/Space Videos):**
   - `EMRdV-3L1n0` (Astrum, **2,599,389 views**), `IxDR-dASDNw` (Mystery Science, **2,546,192 views**), `UHK-fbdbwF8` (Learn Bright, **1,773,101 views**), `O4QrnC9vLs8` (Peekaboo Kidz, **1,764,409 views**), `auxpcdQimCs` (CrashCourse, **1,339,005 views**), `yB9HHyPpKds` (CrashCourse, **1,180,437 views**), `TuDfZ2Md5x8` (CrashCourse, **1,098,018 views**), `dvd47rMYia0` (Astronimate, **1,011,799 views**), plus `xGQ_UjAsJPg` (**996,709 views**), `S_jdfyp8pL0` (ScienceAtNASA, **949,269 views**), `Eq5a6L7c_UY` (StarTalk, **641,651 views**), and `_zy4DVdfdsw` (NASA Science, **441,058 views**).
3. **Gemini Direct NASA Fact Check (`F64.1`–`F64.11`):**
   - **Rejected `J2703`'s universal hook (`F64.1`):** *"Every shooting star you have seen was a grain of comet dust about the size of a grain of sand"* is false both because meteoroids come from **both comets and asteroids** (including `064`'s own Beat 4 Geminids from asteroid `3200 Phaethon`, plus meteorites in Beat 5 which come almost exclusively from asteroids) and because comet shower debris ranges from **a grain of sand to a pea** (and sporadic meteoroids up to boulder/small-asteroid size).
   - **Verified all dates & speeds (`F64.2`–`F64.11`):** `11–72 km/s` (`25,000–160,000 mph`) entry speed; `48.5 tons` (`44 tonnes`) daily infall; `50–80 km` mesosphere burn-up (`76–104 km`, peaking near `90 km`, for bright Perseids); `1P/Halley` (`15 × 8 km` nucleus, `3%` albedo, `76-yr` orbit, `1986 → 2061`) producing both the **Eta Aquariids** (`peak May 5–6`, `65.4 km/s`, up to `50/hr` S. Hemisphere / `10/hr` N. Hemisphere) and **Orionids** (`peak Oct 21–22`, `66 km/s`, `10–20/hr`); **Perseids** (`peak Aug 12–13`, `59 km/s`, `50–100/hr`, from `26-km` Comet `109P/Swift-Tuttle`, `133-yr` orbit `1992 → 2125`, linked by Schiaparelli in `1865`); and **Geminids** (`active Dec 4–17`, `peak Dec 13–14`, `35 km/s`, up to `120/hr`, from near-Earth asteroid **`3200 Phaethon`**, `1.4-yr` orbit).

---

## 4. Summary of Evidence Repaired for `OWB:065` (*How Will the Space Station Fall to Earth?*)

### 4.1 Repaired Files in `02_Video-Projects/065_How-Will-The-Space-Station-Fall-To-Earth/`
- [`TOPIC.md`](../../../02_Video-Projects/065_How-Will-The-Space-Station-Fall-To-Earth/TOPIC.md)
- [`TOPIC_OPPORTUNITY_SCORE.md`](../../../02_Video-Projects/065_How-Will-The-Space-Station-Fall-To-Earth/TOPIC_OPPORTUNITY_SCORE.md) & [`11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md`](../../../02_Video-Projects/065_How-Will-The-Space-Station-Fall-To-Earth/11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md)
- [`11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`](../../../02_Video-Projects/065_How-Will-The-Space-Station-Fall-To-Earth/11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md)
- [`11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md`](../../../02_Video-Projects/065_How-Will-The-Space-Station-Fall-To-Earth/11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md)

### 4.2 Key Findings (`OWB:065`)
1. **Rule 26 Search Phrase & Ranking Videos:**
   - While `"how will the space station fall to earth"` returns `[]` in YouTube GB autocomplete, `"what will happen to the space station"` and `"what will happen to the iss"` immediately return **`"what will happen to the international space station"`** and **`"what will happen to the iss"`** (alongside `"iss deorbit"`, `"international space station deorbit"`, and `"point nemo spacecraft cemetery"`).
   - Two ranking videos: `cohVHaVMBl8` (*The End of The International Space Station*, The B1M, **2,762,403 views**) and `plJVUFErhf8` (*You Are Alive to Watch the Space Station Fall From the Sky*, What If, **1,650,382 views**).
   - Recommended Rule 26 lead title: **`What Will Happen to the ISS? (NASA's 420-Ton Deorbit Plan)`** (`58 chars`, `0` exact-title collisions) or **`What Will Happen to the International Space Station?`** (`52 chars`, `0` exact-title collisions), with `How Will the Space Station Fall to Earth?` (`41 chars`, `0` collisions) retained as Title C and in `status.json`.
2. **Neighbour Pass (`8` Verified `≥1M`-View Education/Space Videos):**
   - `oLrOnEmy_GA` (Jared Owen, **12,769,751 views**), `FhKOuxhGlmI` (Jared Owen, **8,577,690 views**), `ivLX9o6Ayl8` (Real Engineering, **4,112,913 views**), `cohVHaVMBl8` (The B1M, **2,762,403 views**), `plJVUFErhf8` (What If, **1,650,382 views**), `j0ZZfIz9R1I` (Real Engineering, **1,609,060 views**), `9I_pgS6-suc` (Chris Brown Explores, **1,569,715 views**), `QAOMtCzLKWE` (The Ocean Race, **1,118,503 views**), plus `7` specialist ISS-deorbit/Point-Nemo explainers (`B3ahPLhT_H4` **882,976**, `U5lidnLtO7c` **581,543**, `D4Un7qBjbkw` **537,390**, `T3bkyOxiqXE` **351,500**, `JO7HX3Irq14` **303,155**, `3DBxZvtMYm4` **276,993**, `AevLr16Bt3E` **245,691**).
3. **Current `main` Overlap Finding (`AR2` `xdurJQcoiGM`):**
   - Zero existing or planned **long** films cover the ISS deorbit, SpaceX USDV, Point Nemo, Mir, or Skylab.
   - However, `J2710` identified that Replication-Cohort Short **`AR2` (`xdurJQcoiGM`, *Where Will the International Space Station Crash?*)** is already uploaded and scheduled for **`Wed 25 Nov 2026 11:30Z`** (`J2426` / `J1356`). Under `STUDIO_PLAYBOOK.md` ("Short first, then the long"), `AR2` and public Short `VfDm3E2bUgU` (*16 Sunrises*) support building `OWB:065` as the full long film, provided `065`'s two new Shorts (`Where Do Dead Spacecraft Go?` and `Why Does the Space Station Keep Falling?`) stay distinct from `AR2`.
4. **Gemini Direct NASA / NOAA / GAO Fact Check (`F65.1`–`F65.11`):**
   - **Mass, Size, Speed & Altitude (`F65.1`–`F65.5`):** `419,725 kg` (`925,335 lbs` ≈ `420 tonnes`) on NASA's *Facts and Figures* and `>430,000 kg` (`>945,000 lbs`) on NASA's *Transition Plan FAQ*; `109 m` (`356 ft`) end-to-end (one yard shy of an American football field with end zones; `94 m` truss, `73 m` solar arrays, `67 m` module axis); `5 miles/s` (`~17,500 mph` / `~28,000 km/h`, `16 orbits/day` every `90 min`); `~400–415 km` (`257 miles`) altitude in the thermosphere; `1 to 2 years` natural orbital decay without reboosts; `<4 years` mean time between catastrophic debris impacts if boosted to `800 km` (`120–760 m/s` delta-V vs `57 m/s` for controlled deorbit).
   - **Mandatory Distinction #1 — Baseline Plan vs Guaranteed Date (`F65.6` & `F65.7`):** NASA, ESA, JAXA, and CSA committed to operate through **`2030`** (Roscosmos through at least `2028`), and on **June 26, 2024** NASA awarded SpaceX a contract worth up to **`$843M`** for the **U.S. Deorbit Vehicle (USDV)** to meet the `1-in-10,000` public risk standard. Per **`GAO-26-107805` (June 2026)**, **in `2027` NASA will assess whether to launch the USDV in mid-`2029` to initiate deorbit or extend ISS operations**, with the baseline final re-entry burn planned for **late `2030` or early `2031`**.
   - **Mandatory Distinction #2 — Remote South Pacific Disposal Area vs Single Point Nemo Coordinate (`F65.8`):** Operators target the broad **South Pacific Oceanic Uninhabited Area (`SPOUA`)** — the remote ocean region *around* **Point Nemo** (nicknamed the **"Spacecraft Cemetery"** by NASA Space Place) — for the elongated debris footprint, **not a guaranteed single-point impact at the exact coordinate of Point Nemo**. Within that region, NOAA verifies Point Nemo (`48°52.6′S, 123°23.6′W`) is **`2,688 km` (`1,670 miles`, `~2,700 km`)** from the nearest land (Ducie Island, Motu Nui, and Maher Island, Antarctica).
   - **Historical Re-Entries & 3-Stage Breakup (`F65.9`–`F65.11`):** Verified **Skylab** (`11 July 1979`, solar-expanded drag, debris over the Indian Ocean and Western Australia), **Mir** (`23 March 2001`, controlled 3-stage Progress-driven deorbit of the `15-year-old`, `143-ton` station into the South Pacific near Fiji/east of New Zealand, `95–85 km` breakup, `20–25 tons` of remnants), and NASA's **3-stage ISS breakup model** (`solar arrays/radiators` first, `intact modules/truss` second, `module skin melt & truss fragmentation` third).
