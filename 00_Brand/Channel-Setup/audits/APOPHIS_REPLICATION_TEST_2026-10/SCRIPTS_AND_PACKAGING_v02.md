# Apophis Replication Test (J1279): 3 Standalone Short Scripts + Packaging, v02 (DRAFT, parked for Chief)

**Job:** `J1279` · `v02` drafted by `gemini` (`gemini-argon`), 31 Oct 2026, implementing all 7 items from **Chief h28 (`#6533691867`)** (`SCRIPTS_AND_PACKAGING_v01.md` preserved). **Draft only — parked for Chief (`script PASS`).**
**Spend:** `£0.00` (no ElevenLabs VO, no Vertex/Flow mints).

---

## 1. Summary of Chief h28 (`#6533691867`) Fixes Applied in `v02`

1. **AR2 dates and place (`plan, not settled fact`):**
   - **Title:** Dropped `"in 2030"` → **`Where Will the International Space Station Crash?`**
   - **Line 1 (declarative `v13a` mould, grammatical forward loop):** **`"NASA plans to crash the Space Station into the ocean around 2031."`**
   - **Payoff (names the place):** **`"A deorbit craft steers the rest into the empty South Pacific."`**
   - **Last line:** **`"Look up and watch it cross the sky, because…"`**
   - **Hook caption (no hard `"2030"`):** **`OCEAN CRASH ~2031`** (yellow: `~2031`)
   - **Date call-out card:** **`RETIRES 2030 · DEORBIT BURN ~2031 · DECISION 2027`**
   - **Sources table:** Added **`GAO-26-107805`** (*Low-Earth Orbit: NASA Faces Impending Decisions for Replacing International Space Station with Commercial Stations*, June 2026) verbatim quotes on the `2027` launch/extend assessment and the `end of 2030 or early 2031` USDV re-entry burn into the uninhabited South Pacific.
2. **AR3 answers its own title:**
   - **Payoff:** **`"Totality crosses Spain and North Africa, peaking over Egypt at six minutes twenty-three seconds."`**
   - **Date/place card:** **`2 AUG 2027 · 258 KM PATH · LONGEST: 6M23S, LUXOR`**
3. **AR3 picture honesty:**
   - Removed `GSFC_20170720_August_m12669_EPICEclipse` (which showed the 2017 US eclipse shadow). Replaced `s02` with a **£0 code-drawn 2027 path map** plotted directly from NASA's path table (`SE2027Aug02Tpath.html`: Strait of Gibraltar / southern Spain / Morocco → Algeria → Tunisia → Libya → Egypt / Luxor) over graded NASA Blue Marble East (`GSFC_20171208_Archive_e002130.jpg`).
   - Every 2017 or 2024 eclipse plate (`NOAA_sat_eclipse_2024_notext.webm`, `NHQ201708210100.jpg`/`.tif`) is either uncaptioned (frame `0.0–2.4 s` carries only the hook caption) or stamped with its own archive year (`2017` / `2024`) when no other label is on screen.
   - `Gerst_Earth_timelapses_2017.webm` carries **no `"over Spain/Morocco"` claim** (used purely as a generic orbital Earth pass).
4. **AR1 educational call-outs:**
   - Opening date card (`2.1–5.4 s`, after frame-0 hook caption clears): **`22 DEC 2032`**.
   - On the `"four percent"` line (`5.8–9.0 s`): **`4.3% (early 2025) → 0% (Webb, Feb 2026)`**.
5. **Verified Asset Provenance (Mini / NAS paths + Free PD/CC Sources & Credits):**
   - Every single asset named across `AR1`–`AR4` in §8 below now has its **verified Mini or `/Volumes/data/mac-mini-archive` NAS path** (confirmed with `os.path.exists`) **plus** its free `images-api.nasa.gov` / Wikimedia Commons / ESO download URL, licence (`Public domain`, `CC0`, `CC BY 4.0`, or `CC BY-SA 3.0 IGO`), and exact credit string. Media stays off git.
6. **Timing realism (`~2.4 words/s`, `≤46 words`):**
   - At Ben Orbit Narrator's measured rate of **`~2.4 words/s`** (`031` take: `1,340 words` in `560.8 s`), each script is trimmed to **`≤46 words`** (`AR1`: **46 words**, `AR2`: **46 words**, `AR3`: **46 words**, `AR4` reserve: **45 words**) so the spoken take lands at `~17.8–18.2 s` (`~18.8–19.2 s` with the `1.0 s` forward-loop tail, squarely inside **`17–20 s`**).
   - All payoff `%`s are marked **`re-measure on VO`** (the `≥70%` check is enforced on the real recorded VO, not the pre-VO estimate).
7. **Manifests:**
   - Updated the four `PACKAGE_MANIFEST.json` files (`owb_ar1_2024_yr4_moon`, `owb_ar2_iss_2030_deorbit`, `owb_ar3_2027_eclipse`, `owb_ar4_halley_2061`) with the `v02` titles, GAO/NASA sources, and image credits. No schedule, no upload.

---

## 2. Cohort Summary (Primary Cohort `AR1 + AR2 + AR3`, Reserve `AR4`)

All four scripts keep the **declarative `v13a` Line 1** mould so the closing `"look up"` phrase loops grammatically into Line 1.

| ID | Role | Topic & Date | Plain-Question Title | Frame-0 Hook Caption (yellow word) | Cover Text (no title words) | Spoken Words (`≤46`) | Est. Runtime (`@2.4 w/s + 1s loop`) | Payoff Start (`re-measure on VO`) | On-Screen Cards & `DATA` Overlay | Picture Spend |
|---|---|---|---|---|---|---:|---:|---|---|---:|
| **AR1** | Primary 1 | Asteroid `2024 YR4` & the Moon (`22 Dec 2032`) | **Will Asteroid 2024 YR4 Hit the Moon in 2032?** | HIT THE **MOON**? | **15-STOREY** / SPACE ROCK | **46** | `~19.2 s` (`18.2 s` VO + `1.0 s` loop) | Est. `~71–74%` (**re-measure on VO**) | Date: `22 DEC 2032` · Call-out: `4.3% (early 2025) → 0% (Webb, Feb 2026)` · `DATA` scale: `21,200 KM` safe pass | **£0.00** |
| **AR2** | Primary 2 | ISS Planned Deorbit (`~2031`, decision `2027`) | **Where Will the International Space Station Crash?** | OCEAN CRASH **~2031** | **FOOTBALL-FIELD** / DROP | **46** | `~19.2 s` (`18.2 s` VO + `1.0 s` loop) | Est. `~71–74%` (**re-measure on VO**) | Card: `RETIRES 2030 · DEORBIT BURN ~2031 · DECISION 2027` · `DATA` scale: `109 M (FOOTBALL FIELD) → SOUTH PACIFIC` | **£0.00** |
| **AR3** | Primary 3 | Total Solar Eclipse (`2 Aug 2027`, peak over Egypt) | **Where Will the 2027 Total Solar Eclipse Last Over Six Minutes?** | **SIX MINUTES** OF NIGHT | MIDDAY TURNS / **PITCH BLACK** | **46** | `~19.2 s` (`18.2 s` VO + `1.0 s` loop) | Est. `~71–74%` (**re-measure on VO**) | Card: `2 AUG 2027 · 258 KM PATH · LONGEST: 6M23S, LUXOR` · `DATA` bar: `2027: 6M 23S (EGYPT)` vs `2026: 2M 18S` | **£0.00** |
| **AR4** | Reserve | Halley's Comet Return (`July 2061`) | **Will You Live to See Halley's Comet Return in 2061?** | BACK IN **2061** | ONCE IN **76** YEARS | **45** | `~18.8 s` (`17.8 s` VO + `1.0 s` loop) | Est. `~73%` (**re-measure on VO**) | `DATA` scale/timeline: `1986 → 2061 (76 YRS)` · `15 KM CORE (3% LIGHT)` | **£0.00** |

---

## 3. Master Sources Table (`MUST QUOTE` Primary NASA & GAO Verification)

Every spoken number, date, scale comparison, and on-screen card across `AR1`–`AR4` is backed by exact primary quotes below.

| Row | Short | Spoken / Card Claim | Exact Primary Quote | Official Source URL |
|---|---|---|---|---|
| **S1.1** | `AR1` | Asteroid `2024 YR4`; `22 December 2032`; `4%` (`4.3%` early 2025) → `0%` (`Webb, Feb 2026`) | *"Using data from NASA’s James Webb Space Telescope observations collected on Feb. 18 and 26, experts from NASA’s Center for Near-Earth Object Studies at the agency’s Jet Propulsion Laboratory in Southern California have refined near-Earth asteroid 2024 YR4’s orbit and are ruling out a chance of lunar impact on Dec. 22, 2032."* · *"Previous analyses, made before the incorporation of these new observations, suggested 2024 YR4 had a 4.3% chance of lunar impact on this date."* | https://science.nasa.gov/blogs/planetary-defense/2026/03/05/new-nasa-asteroid-observations-eliminate-chance-of-2032-lunar-impact/ |
| **S1.2** | `AR1` | `60 metres` wide (`53–67 m`); matches a `15-storey building` | *"And of course, our main goal was measuring the size of 2024 YR4, which we estimate at about 60 meters (200 feet). That’s just about the height of a 15-story building."* · *"New infrared observations from NASA’s James Webb Space Telescope have decreased the uncertainty of the asteroid’s size, and 2024 YR4 is now estimated to be 174-220 feet (53-67 meters), about the size of a 15-story building."* | https://science.nasa.gov/blogs/webb/2025/04/02/nasas-webb-finds-asteroid-2024-yr4-is-building-sized/ · https://science.nasa.gov/solar-system/asteroids/2024-yr4-facts/ |
| **S1.3** | `AR1` | It will miss; passes `21,200 kilometres` (`13,200 miles`) from the lunar surface; no risk to Earth | *"With the new data, 2024 YR4 is expected to pass by the lunar surface at a distance of 13,200 miles (21,200 km)."* · *"Over time with more observations collected by observatories around the world, NASA concluded the object poses no significant impact risk to Earth on Dec. 22, 2032, or through the next century."* | https://science.nasa.gov/blogs/planetary-defense/2026/03/05/new-nasa-asteroid-observations-eliminate-chance-of-2032-lunar-impact/ |
| **S2.1** | `AR2` | `GAO-26-107805`: NASA assesses in `2027` whether to launch USDV in `2029` or extend; USDV re-entry burn at `end of 2030 or early 2031` into remote `South Pacific` | *"In 2027, NASA will assess whether to launch the U.S. Deorbit Vehicle in 2029 to initiate the ISS's deorbit or to extend ISS operations. The U.S. Deorbit Vehicle is comprised of a SpaceX Dragon spacecraft with docking and rendezvous capabilities and a Dragon trunk with propulsion capability."* · *"Then, in mid-2029, NASA plans to launch the U.S. Deorbit Vehicle and attach it to the ISS. Finally, at the end of 2030 or early 2031, the U.S. Deorbit Vehicle will perform a re-entry burn, which will push the ISS out of orbit and into a controlled re-entry into an uninhabited area of the South Pacific Ocean."* | https://www.gao.gov/products/gao-26-107805 (GAO-26-107805, *Low-Earth Orbit: NASA Faces Impending Decisions for Replacing International Space Station with Commercial Stations*, June 2026) |
| **S2.2** | `AR2` | NASA plan to operate ISS through `2030`, then controlled deorbit avoiding populated areas | *"NASA has committed to fully use and safely operate the space station through 2030…"* · *"At the conclusion of the International Space Station Program, the station will be deorbited in a controlled manner to ensure avoidance of populated areas on Earth."* | https://www.nasa.gov/faqs-the-international-space-station-transition-plan/ |
| **S2.3** | `AR2` | `109 metres` (`356 feet`) end-to-end; size of a `football field` | *"The space station is 356 feet (109 meters) end-to-end, one yard shy of the full length of an American football field including the end zones."* · *"The space station covers an area about the size of a football field…"* | https://www.nasa.gov/international-space-station/space-station-facts-and-figures/ · https://www.nasa.gov/faqs-the-international-space-station-transition-plan/ |
| **S2.4** | `AR2` | Most hardware vaporises on re-entry; U.S. Deorbit Vehicle steers surviving pieces into uninhabited ocean | *"Most station hardware is expected to burn up or vaporize during the intense heating associated with atmospheric re-entry, whereas some denser or heat-resistant components like truss sections are expected to survive re-entry and splash down within an uninhabited region of the ocean."* · *"NASA announced SpaceX has been selected to develop and deliver the U.S. Deorbit Vehicle that will provide the capability to deorbit the space station and ensure avoidance of risk to populated areas."* | https://www.nasa.gov/faqs-the-international-space-station-transition-plan/ |
| **S2.5** | `AR2` | Flies over `90 percent` of Earth's population (visible from the ground) | *"The station’s orbital path takes it over 90 percent of the Earth’s population, with astronauts taking millions of images of the planet below."* | https://www.nasa.gov/international-space-station/space-station-facts-and-figures/ |
| **S3.1** | `AR3` | Total Solar Eclipse on `2 August 2027`; greatest duration `6 minutes 23 seconds` (`06m23.2s`) in `Egypt` (near `Luxor`) | *"This interactive Google map [1] shows the path of the Total Solar Eclipse of 2027 Aug 02 … In this case, the Greatest Duration is 06m23.2s ."* · *"2027 Aug 02 10:07:49 Total 136 1.079 06m23s Africa, Europe, Mid East, w & s Asia [Total:Morocco, Spain, Algeria, Libya, Egypt, Saudi Arabia, Yemen, Somalia]"* · Central line at `10:07:50 UT` (`25°30'N, 033°11'E`, Upper Egypt near Luxor): *"Central Line Duration: 06m23.2s"*. | https://eclipse.gsfc.nasa.gov/SEgoogle/SEgoogle2001/SE2027Aug02Tgoogle.html · https://eclipse.gsfc.nasa.gov/SEdecade/SEdecade2021.html · https://eclipse.gsfc.nasa.gov/SEpath/SEpath2001/SE2027Aug02Tpath.html |
| **S3.2** | `AR3` | Shadow path `258 kilometres` wide across Spain, North Africa, and Egypt | Path table at `10:04–10:18 UT` (Egypt): *"Path Width km: 258"* (`Central Line Duration: 06m23.0s`). Path crosses southern Spain and Morocco (`08:46–08:50 UT`), Algeria, Tunisia, Libya, and Egypt (`10:00–10:14 UT`). | https://eclipse.gsfc.nasa.gov/SEpath/SEpath2001/SE2027Aug02Tpath.html |
| **S3.3** | `AR3` | Nearly triples `2026`'s two-minute (`02m18s`) total solar eclipse | *"2026 Aug 12 17:47:05 Total 126 1.039 02m18s n N. America, w Africa, Europe [Total: Arctic, Greenland, Iceland, Spain]"* (`383.2 s / 138 s = 2.78×`, nearly triple). | https://eclipse.gsfc.nasa.gov/SEdecade/SEdecade2021.html |
| **S4.1** | `AR4` | Halley's Comet last seen `1986`; aphelion Dec `2023` beyond Neptune; returns in `2061` on its `76-year` orbit | *"Halley was last seen in Earth's skies in 1986 and was met in space by an international fleet of spacecraft. It will return in 2061 on its regular 76-year journey around the Sun."* · *"Halley's backward, or retrograde, motion is unusual among short-period comets, as its greatest distance from the Sun (aphelion) is beyond the orbit of Neptune."* | https://science.nasa.gov/solar-system/comets/1p-halley/ |
| **S4.2** | `AR4` | Nucleus `15 kilometres` long (`15 × 8 km`); reflects only `3%` of light (`albedo 0.03`) | *"Halley's dimensions are about 9.3 by 5 miles (15 kilometers by 8 kilometers). It is one of the darkest, or least reflective, objects in the solar system. It has an albedo of 0.03, which means that it reflects only 3% of the light that falls on it."* | https://science.nasa.gov/solar-system/comets/1p-halley/ |

---

## 4. Script 1 (`AR1`): Asteroid 2024 YR4 and the Moon in 2032

### Summary & Brief Fields
- **Title (plain question):** **Will Asteroid 2024 YR4 Hit the Moon in 2032?**
- **Alt titles:** *How Close Will Asteroid 2024 YR4 Pass the Moon in 2032?* · *Could Asteroid 2024 YR4 Strike the Moon on December 22, 2032?*
- **Hook caption (frame 0, `0.0–2.0 s`):** `HIT THE **MOON**?` (yellow word: `MOON`)
- **Custom cover text (no title words):** `**15-STOREY** / SPACE ROCK` (yellow: `15-STOREY`)
- **Spoken words:** **46 words** (`≤46 words`, counted from `>` lines)
- **Estimated runtime (`@ ~2.4 words/s`):** **`~19.2 s`** (`~18.2 s` VO + `1.0 s` forward-loop tail; within `17–20 s`, **re-measure on VO**)
- **60% Stayed-to-Watch & 70% Viewed Brief Fields:**
  - `frame_0`: Moving 3D code-rendered blocky asteroid (`_render_apophis_rock_v13.py` adapted for 60 m `2024 YR4`, solid alpha, spinning broadside) sweeping across graded NASA Apollo 11 full-Moon plate `as11-44-6667.jpg` (`1920×1930`, verified on NAS). Full-bleed (`<5%` black), no Orbit at frame 0.
  - `first_word_s`: `~0.08 s` (`"Asteroid"`, re-measure on VO)
  - `surprise_s`: `~1.20 s` (`"skim past the Moon"`, re-measure on VO)
  - `first_cut_s`: `~2.50 s` (`≤3.0 s`)
  - `longest_plate_hold_s`: `≤3.50 s` (`≤4.0 s`; 6 cuts across `~19.2 s`)
  - `meta_promise`: `false` (no *"Stay, and I'll show you"*)
  - `payoff_start_s`: **re-measure on VO** (word 32 `"It will miss"` / word 35 `"passing twenty-one thousand two hundred kilometres up"`, estimated `~70–74%` of cut; `≥70%` gate checked on recorded VO)
  - `last_word_to_loop_s`: `1.00 s` (`≤1.5 s`)
  - `loop_sentence`: *"…Look up that night knowing Asteroid 2024 YR4 will skim past the Moon on December twenty-second, 2032."*

### Script (`AR1` · 46 spoken words)

Hook caption: HIT THE **MOON**? · Related: `VBaYRPp85Sw` (*What Happened to Venus?*, or `030` Apophis once public) · 46 words

[VISUAL MUST: 0.00–2.50 s (`s01_moon_rock_open`). Full-bleed moving 3D asteroid `2024 YR4` (`_render_apophis_rock_v13.py` mesh, fast broadside tumble) sweeping across graded NASA Moon plate `as11-44-6667.jpg` (`1920×1930`, on NAS). Frame-0 hook caption `HIT THE **MOON**?` clears at `2.00 s`; opening date card **`22 DEC 2032`** fades in at `2.05–2.50 s` (carrying across the cut to `5.20 s`, one card at a time). Low house rumble + soft whoosh at frame 0. No Orbit.]

> Asteroid 2024 YR4 will skim past the Moon on December twenty-second, 2032.

[VISUAL MUST: 2.50–5.80 s (`s02_scale_building`). Cut on `<0.20 s` breath to NASA Apollo 14 lunar horizon `as14-67-09386.jpg` (`4020 px`, on NAS, dynamic pan) with our code-rendered `60 M` rock silhouette compared against a clean 15-storey building outline (`SCALE: 15-STOREY BUILDING` after `22 DEC 2032` fades out, one label at a time, house style, no UI slab).]

> At sixty metres wide, it matches a fifteen-storey building.

[VISUAL MUST: 5.80–9.20 s (`s03_webb_track`). Cut to graded NASA full Moon `GSFC_20171208_Archive_e000868.jpg` (on NAS) with the tumbling rock crossing the terminator. Educational call-out card inside the `16:9` centre band (`5.90–8.90 s`, with house ink tick): **`4.3% (early 2025) → 0% (Webb, Feb 2026)`**.]

> Early tracking gave a four percent chance of lunar impact.

[VISUAL MUST: 9.20–12.90 s (`s04_title_banner`). Cut to NASA far-side lunar rotation video/plate `GSFC_20171208_Archive_e001939.jpg` (on NAS, or LRO flyover `GSFC_20190513_m4714_Lee_Lincoln_Scarp_Moon_Flyover` from `images-api.nasa.gov`) with the rock passing overhead. On-screen title banner (`9.20–12.90 s`, alone on screen): *Will Asteroid 2024 YR4 Hit the Moon in 2032?*]

[VISUAL MUST: 12.90–16.60 s (`s05_scale_miss`). Cut to our animated `DATA` scale graphic over graded NASA Moon limb: real-body Moon disc with `2024 YR4`'s trajectory arc drawing past at **`21,200 KM`** (with house ink tick SFX at `13.4 s`), inside the `16:9` centre band at `11.5%` band height.]

> It will miss, passing twenty-one thousand two hundred kilometres up.

[VISUAL MUST: 16.60–18.20 s (`s06_moon_watch`) → `18.20–19.20 s` (`s07_moon_loop`). Return to the opening `as11-44-6667.jpg` Moon + tumbling rock trajectory, ending one frame before frame 0 so `"knowing…"` loops seamlessly into `"Asteroid 2024 YR4…"`.]

> Look up that night knowing…

---

## 5. Script 2 (`AR2`): The International Space Station's Planned Deorbit

### Summary & Brief Fields
- **Title (plain question):** **Where Will the International Space Station Crash?**
- **Alt titles:** *Where Plans Say the International Space Station Will Crash* · *How Will NASA Bring Down the International Space Station?*
- **Hook caption (frame 0, `0.0–2.0 s`):** `OCEAN CRASH **~2031**` (yellow word: `~2031`; no hard `"2030"`)
- **Custom cover text (no title words):** `**FOOTBALL-FIELD** / DROP` (yellow: `FOOTBALL-FIELD`)
- **Spoken words:** **46 words** (`≤46 words`, counted from `>` lines)
- **Estimated runtime (`@ ~2.4 words/s`):** **`~19.2 s`** (`~18.2 s` VO + `1.0 s` forward-loop tail; within `17–20 s`, **re-measure on VO**)
- **60% Stayed-to-Watch & 70% Viewed Brief Fields:**
  - `frame_0`: Moving NASA ISS orbital video (`Five_Minutes_in_Orbit.webm` or `ISS_sunrise_to_sunset.ogv`, both verified on NAS in `027/pool_v01/iss/`, or NASA STS-114 ISS fly-around `ksc_071005_114_hire-12` free download from `images-api.nasa.gov`, full-bleed, `<5%` black, no Orbit at frame 0).
  - `first_word_s`: `~0.08 s` (`"NASA"`, re-measure on VO)
  - `surprise_s`: `~1.15 s` (`"crash the Space Station"`, re-measure on VO)
  - `first_cut_s`: `~2.60 s` (`≤3.0 s`)
  - `longest_plate_hold_s`: `≤3.50 s` (`≤4.0 s`; 6 cuts across `~19.2 s`)
  - `meta_promise`: `false`
  - `payoff_start_s`: **re-measure on VO** (word 27 `"A deorbit craft steers the rest"` / word 33 `"into the empty South Pacific"`, estimated `~70–74%` of cut; `≥70%` gate checked on recorded VO)
  - `last_word_to_loop_s`: `1.00 s` (`≤1.5 s`)
  - `loop_sentence`: *"…Look up and watch it cross the sky, because NASA plans to crash the Space Station into the ocean around 2031."*

### Script (`AR2` · 46 spoken words)

Hook caption: OCEAN CRASH **~2031** · Related: `VBaYRPp85Sw` (*What Happened to Venus?*) · 46 words

[VISUAL MUST: 0.00–2.60 s (`s01_iss_open`). Moving NASA video of the International Space Station orbiting over Earth's sunlit limb (`Five_Minutes_in_Orbit.webm` on NAS, or `ksc_071005_114_hire-12` from `images-api.nasa.gov`). Frame-0 hook caption `OCEAN CRASH **~2031**` clears at `2.00 s`. Low rumble + soft whoosh at frame 0. No Orbit.]

> NASA plans to crash the Space Station into the ocean around 2031.

[VISUAL MUST: 2.60–6.10 s (`s02_iss_truss`). Cut on `<0.20 s` breath to close NASA ISS structure & solar arrays over Earth (`ksc_071005_114_hire-12` / `iss070e062746.jpg` on NAS) with date call-out card inside the `16:9` band (`2.70–6.00 s`, with house ink tick): **`RETIRES 2030 · DEORBIT BURN ~2031 · DECISION 2027`**.]

> It spans a hundred and nine metres, like a football field.

[VISUAL MUST: 6.10–9.20 s (`s03_limb_glow`). Cut to `ISS_sunrise_to_sunset.ogv` (verified on NAS) showing fierce orange atmospheric glow along Earth's limb.]

> Most hardware vaporises.

[VISUAL MUST: 9.20–12.80 s (`s04_title_banner`). Cut to `Gerst_Earth_timelapses_2017.webm` (verified on NAS, orbital pass over sunlit ocean waters). On-screen title banner (`9.20–12.80 s`, alone on screen): *Where Will the International Space Station Crash?*]

> A deorbit craft steers the rest

[VISUAL MUST: 12.80–16.30 s (`s05_scale_deorbit`). Cut to our animated `DATA` scale graphic over graded NASA ocean limb (`iss026e005121.jpg` on NAS): `109 M (FOOTBALL FIELD)` station silhouette descending into the **`EMPTY SOUTH PACIFIC`** target zone with house ink tick SFX at `13.3 s`, inside the `16:9` centre band.]

> into the empty South Pacific.

[VISUAL MUST: 16.30–18.20 s (`s06_night_pass`) → `18.20–19.20 s` (`s07_iss_loop`). Cut to `iss070e062746.jpg` (verified on NAS, night city lights under Earth's airglow), then match-cut back to `s01_iss_open` ending one frame before frame 0 so `"because…"` runs straight into `"NASA plans to crash the Space Station into the ocean around 2031."`.]

> Look up and watch it cross the sky, because…

---

## 6. Script 3 (`AR3`): The 2 August 2027 Total Solar Eclipse (Spain, North Africa & Egypt)

### Summary & Brief Fields
- **Title (plain question):** **Where Will the 2027 Total Solar Eclipse Last Over Six Minutes?**
- **Alt titles:** *Where Will the 2027 Solar Eclipse Turn Day Into Night for Over Six Minutes?* · *Why Does the 2027 Total Solar Eclipse Peak Over Egypt at Six Minutes?*
- **Hook caption (frame 0, `0.0–2.0 s`):** `**SIX MINUTES** OF NIGHT` (yellow word: `SIX MINUTES`)
- **Custom cover text (no title words):** `MIDDAY TURNS / **PITCH BLACK**` (yellow: `PITCH BLACK`)
- **Spoken words:** **46 words** (`≤46 words`, counted from `>` lines)
- **Estimated runtime (`@ ~2.4 words/s`):** **`~19.2 s`** (`~18.2 s` VO + `1.0 s` forward-loop tail; within `17–20 s`, **re-measure on VO**)
- **60% Stayed-to-Watch & 70% Viewed Brief Fields:**
  - `frame_0`: Moving NOAA satellite eclipse shadow video (`NOAA_sat_eclipse_2024_notext.webm`, verified on NAS in `027/pool_v01/eclipse/`, uncaptioned besides the `0.0–2.0 s` hook caption so no false date is implied, full-bleed, `<10%` black, no Orbit at frame 0).
  - `first_word_s`: `~0.08 s` (`"The"`, re-measure on VO)
  - `surprise_s`: `~1.20 s` (`"turns midday into night"`, re-measure on VO)
  - `first_cut_s`: `~2.50 s` (`≤3.0 s`)
  - `longest_plate_hold_s`: `≤3.50 s` (`≤4.0 s`; 6 cuts across `~19.2 s`)
  - `meta_promise`: `false`
  - `payoff_start_s`: **re-measure on VO** (word 32 `"peaking over Egypt"` / word 35 `"at six minutes twenty-three seconds"`, estimated `~70–74%` of cut; `≥70%` gate checked on recorded VO)
  - `last_word_to_loop_s`: `1.00 s` (`≤1.5 s`)
  - `loop_sentence`: *"…Millions can look up as the 2027 solar eclipse turns midday into night for over six minutes."*

### Script (`AR3` · 46 spoken words)

Hook caption: **SIX MINUTES** OF NIGHT · Related: `VBaYRPp85Sw` (*What Happened to Venus?*, or `h8HGfyShEHI` after 1 Nov thumb test) · 46 words

[VISUAL MUST: 0.00–2.50 s (`s01_eclipse_open`). Moving full-frame satellite eclipse shadow video (`NOAA_sat_eclipse_2024_notext.webm`, verified on NAS; uncaptioned past the `0.0–2.0 s` hook caption `**SIX MINUTES** OF NIGHT`). Low rumble + soft whoosh at frame 0. No Orbit.]

> The 2027 solar eclipse turns midday into night for over six minutes.

[VISUAL MUST: 2.50–6.00 s (`s02_path_map_2027`). Cut on `<0.20 s` breath to our **£0 code-drawn 2027 totality path map** plotted from NASA's `SE2027Aug02Tpath.html` coordinates over graded NASA Blue Marble East (`GSFC_20171208_Archive_e002130.jpg`, verified on NAS), drawing the `258 KM` shadow band across southern Spain, Morocco, Algeria, Tunisia, Libya, and Egypt (Luxor). Date/place call-out card inside the `16:9` band (`2.60–5.90 s`, with house ink tick): **`2 AUG 2027 · 258 KM PATH · LONGEST: 6M23S, LUXOR`**.]

> The Moon's shadow spans two hundred and fifty-eight kilometres.

[VISUAL MUST: 6.00–9.20 s (`s03_corona_flare`). Cut to NASA totality corona plate (`NHQ201708210100.jpg`/`.tif`, verified on NAS, dynamic pull with diamond-ring flare, stamped `2017 ARCHIVE` in small house type so the archive year is explicit).]

> That nearly triples 2026's two-minute eclipse.

[VISUAL MUST: 9.20–12.90 s (`s04_title_banner`). Cut to ESA/NASA ISS orbital Earth pass (`Gerst_Earth_timelapses_2017.webm`, verified on NAS; generic orbital pass with no unverified Spain/Morocco ground-track claim). On-screen title banner (`9.20–12.90 s`, alone on screen): *Where Will the 2027 Total Solar Eclipse Last Over Six Minutes?*]

> Totality crosses Spain and North Africa,

[VISUAL MUST: 12.90–16.50 s (`s05_scale_duration`). Cut to our animated `DATA` scale bar over graded NASA totality plate (`NHQ201708210116.jpg` on NAS): `2026 ECLIPSE: 2M 18S` bar vs `2027 EGYPT (LUXOR): 6M 23S` bar growing nearly 3× longer (with house ink tick SFX at `13.4 s`), inside the `16:9` centre band.]

> peaking over Egypt at six minutes twenty-three seconds.

[VISUAL MUST: 16.50–18.20 s (`s06_look_up`) → `18.20–19.20 s` (`s07_eclipse_loop`). Cut to ESO La Silla twilight sky timelapse (`ESO_timelapse_La_Silla.webm`, verified on NAS), then match-cut back to `s01_eclipse_open` ending one frame before frame 0 so `"as…"` loops into `"the 2027 solar eclipse turns midday into night…"`.]

> Millions can look up as…

---

## 7. Reserve Script 4 (`AR4`): Halley's Comet Returning in 2061

Kept in reserve per Chief h28 (`AR4 Halley: PASS (reserve)`), trimmed to **45 words** (`≤46 words`).

### Summary & Brief Fields
- **Title (plain question):** **Will You Live to See Halley's Comet Return in 2061?**
- **Alt titles:** *When Will Halley's Comet Return to Earth's Skies?* · *Why Is Halley's Comet Already Falling Back Toward Earth for 2061?*
- **Hook caption (frame 0, `0.0–2.0 s`):** `BACK IN **2061**` (yellow word: `2061`)
- **Custom cover text (no title words):** `ONCE IN **76** YEARS` (yellow: `76`)
- **Spoken words:** **45 words** (`≤46 words`, counted from `>` lines)
- **Estimated runtime (`@ ~2.4 words/s`):** **`~18.8 s`** (`~17.8 s` VO + `1.0 s` forward-loop tail; within `17–20 s`, **re-measure on VO**)
- **60% Stayed-to-Watch & 70% Viewed Brief Fields:**
  - `frame_0`: Moving 3D code-rendered icy comet nucleus with active dust/gas jets (`_render_apophis_rock_v13.py` adapted with bright coma/tail particles) streaking across `lasilla_mw.mp4` (verified on Mini in `029`), full-bleed, no Orbit at frame 0.
  - `first_word_s`: `~0.08 s` (`"Halley's"`, re-measure on VO)
  - `surprise_s`: `~1.20 s` (`"already falling back"`, re-measure on VO)
  - `first_cut_s`: `~2.50 s` (`≤3.0 s`)
  - `longest_plate_hold_s`: `≤3.50 s` (`≤4.0 s`)
  - `meta_promise`: `false`
  - `payoff_start_s`: **re-measure on VO** (word 35 `"It will safely pass Earth"`, estimated `~73%` of cut; `≥70%` gate checked on recorded VO)
  - `last_word_to_loop_s`: `1.00 s` (`≤1.5 s`)
  - `loop_sentence`: *"…and you can look up knowing Halley's Comet is already falling back toward us for 2061."*

### Script (`AR4` · 45 spoken words)

Hook caption: BACK IN **2061** · Related: `VBaYRPp85Sw` · 45 words

[VISUAL MUST: 0.00–2.50 s (`s01_halley_open`). Moving code-rendered comet with streaming coma and tail streaking across graded ESO night-sky timelapse (`lasilla_mw.mp4`, verified on Mini). Soft whoosh at frame 0. No Orbit.]

> Halley's Comet is already falling back toward us for 2061.

[VISUAL MUST: 2.50–5.90 s (`s02_halley_core`). Cut on `<0.20 s` breath to NASA/JPL `PIA17485` (1986 Halley comet tail plate from `images-api.nasa.gov`, graded, dynamic pan) paired with our dark `15 KM` potato-shaped nucleus silhouette.]

> Its fifteen-kilometre icy core reflects just three percent of sunlight.

[VISUAL MUST: 5.90–9.20 s (`s03_neptune_turn`). Cut to `orion_over_paranal.mp4` (verified on Mini in `029`) as the comet's orbital arc rounds past Neptune's distance (aphelion Dec 2023).]

[VISUAL MUST: 9.20–12.80 s (`s04_title_banner`). On-screen title banner (`9.20–12.80 s`, alone on screen): *Will You Live to See Halley's Comet Return in 2061?*]

> Last seen in 1986, it takes seventy-six years to loop past Neptune and return.

[VISUAL MUST: 12.80–16.20 s (`s05_scale_halley`). Cut to our animated `DATA` timeline/scale bar over moving starfield (`ESO_timelapse_La_Silla.webm` on NAS): `1986 → 2061 (76 YEARS)` and `15 KM CORE (3% LIGHT)` with house ink tick SFX at `13.4 s`, inside the `16:9` centre band.]

> It will safely pass Earth,

[VISUAL MUST: 16.20–17.80 s (`s06_sky_look`) → `17.80–18.80 s` (`s07_halley_loop`). Match-cut back to `lasilla_mw.mp4` + streaming comet ending one frame before frame 0 so `"knowing…"` runs straight into `"Halley's Comet is already falling back…"`.]

> and you can look up knowing…

---

## 8. Verified Picture & Audio Asset Table (Mini / NAS Paths + Free PD/CC Sources & Credits)

Every asset named in `AR1`–`AR4` was checked against the Mac mini and `/Volumes/data/mac-mini-archive` NAS on 31 Oct 2026 (`os.path.exists == True`). Media stays off git.

> **Path shorthand below:**
> - `<MINI_OWB>` = `/Users/benjaminoats/YouTube/orbit-with-ben`
> - `<NAS_027_POOL>` = `/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/pool_v01`

| Asset File / ID | Used In | Verified Mini or NAS Path (`os.path.exists == True`) | Free Upstream URL (`images-api.nasa.gov` / Commons / ESO) | Licence & Required Credit |
|---|---|---|---|---|
| `_render_apophis_rock_v13.py` | `AR1`, `AR4` | `<MINI_OWB>/02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/10_Shorts/standalone_apophis/_render_apophis_rock_v13.py` | Own code-rendered 3D mesh script in repo | Own work (`£0.00`) |
| `owb-standalone-shorts_score_bed_v01.mp3` | `AR1`–`AR4` | `<MINI_OWB>/00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/05_Music/owb-standalone-shorts_score_bed_v01.mp3` | Own standalone Shorts score bed on disk | Own work (`£0.00`) |
| `sfx_kit.py` (`rumble_low`, `whoosh_soft`, `tick_ink`) | `AR1`–`AR4` | `<MINI_OWB>/scripts/sfx_kit.py` (pre-built kit at `<MINI_OWB>/00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/06_Sound-Effects/compilation_kit_v01`) | Own house synthesis script | Own work (`£0.00`) |
| `as11-44-6667.jpg` (`1920×1930`) | `AR1` (`s01`, `s06`, `s07`) | `<NAS_027_POOL>/moon/as11-44-6667.jpg` (`2,250,538 B`) | Free download, `images-api.nasa.gov` (`as11-44-6667`) | Public domain · Credit: `NASA` |
| `as14-67-09386.jpg` (`4020 px`) | `AR1` (`s02`) | `<NAS_027_POOL>/moon/as14-67-09386.jpg` (`4,231,948 B`) | Free download, `images-api.nasa.gov` (`as14-67-09386`) | Public domain · Credit: `NASA` |
| `GSFC_20171208_Archive_e000868.jpg` | `AR1` (`s03`, `s05`) | `<NAS_027_POOL>/moon/GSFC_20171208_Archive_e000868.jpg` (`777,580 B`) | Free download, `images-api.nasa.gov` (`GSFC_20171208_Archive_e000868`) | Public domain · Credit: `NASA/GSFC` |
| `GSFC_20171208_Archive_e001939.jpg` | `AR1` (`s04`) | `<NAS_027_POOL>/moon/GSFC_20171208_Archive_e001939.jpg` (`1,976,919 B`) | Free download, `images-api.nasa.gov` (`GSFC_20171208_Archive_e001939`; optional moving alt: `GSFC_20190513_m4714_Lee_Lincoln_Scarp_Moon_Flyover`) | Public domain · Credit: `NASA/GSFC/LRO` |
| `Five_Minutes_in_Orbit.webm` (`1920×1280`, `31.5 s`) | `AR2` (`s01`, `s07`) | `<NAS_027_POOL>/iss/Five_Minutes_in_Orbit.webm` (`7,973,947 B`) | Free download, Wikimedia Commons (`File:Five Minutes in Orbit (154728).webm`) / NASA Earth Observatory | Public domain · Credit: `NASA/JSC/Earth Observatory` |
| `ksc_071005_114_hire-12` *(optional close ISS fly-around)* | `AR2` (`s02` alt) | Not cached locally — free API download at build time (`£0`) | Free download, `images-api.nasa.gov` (`ksc_071005_114_hire-12`) | Public domain · Credit: `NASA` |
| `ISS_sunrise_to_sunset.ogv` (`1280×720`, `76 s`) | `AR2` (`s03`) | `<NAS_027_POOL>/iss/ISS_sunrise_to_sunset.ogv` (`60,898,356 B`) | Free download, Wikimedia Commons (`File:Sunrise To Sunset Aboard The ISS.ogv`) | Public domain · Credit: `NASA / Robert Simmon` |
| `Gerst_Earth_timelapses_2017.webm` (`3840×2160`, `357.8 s`) | `AR2` (`s04`), `AR3` (`s04`) | `<NAS_027_POOL>/iss/Gerst_Earth_timelapses_2017.webm` (`1,174,720,359 B`) | Free download, Wikimedia Commons (`File:Alexander Gerst’s Earth timelapses (2017 reissue).webm`) | `CC BY-SA 3.0 IGO` (silent picture only) · Credit: `ESA – European Space Agency / A. Gerst, CC BY-SA 3.0 IGO` |
| `iss026e005121.jpg` | `AR2` (`s05` ocean bg) | `<NAS_027_POOL>/tide/iss026e005121.jpg` (`900,804 B`) | Free download, `images-api.nasa.gov` (`iss026e005121`) | Public domain · Credit: `NASA` |
| `iss070e062746.jpg` (`5568×3712`) | `AR2` (`s02`, `s06`) | `<NAS_027_POOL>/iss/iss070e062746.jpg` (`8,610,795 B`) | Free download, `images-api.nasa.gov` (`iss070e062746`) | Public domain · Credit: `NASA` |
| `NOAA_sat_eclipse_2024_notext.webm` (`3840×2160`, `132.5 s`) | `AR3` (`s01`, `s07`) | `<NAS_027_POOL>/eclipse/NOAA_sat_eclipse_2024_notext.webm` (`272,694,488 B`) | Free download, Wikimedia Commons (`File:NOAA Satellites View Total Solar Eclipse (NESDIS 2024-04-12 2024-4-12-Total-Solar-Eclipse-NO-TEXT).webm`) | Public domain · Credit: `NOAA` |
| `GSFC_20171208_Archive_e002130.jpg` (Blue Marble East) | `AR3` (`s02` 2027 path map base) | `<NAS_027_POOL>/earth/GSFC_20171208_Archive_e002130.jpg` (`2,930,544 B`) | Free download, `images-api.nasa.gov` (`GSFC_20171208_Archive_e002130`) + NASA `SE2027Aug02Tpath.html` coordinates | Public domain · Credit: `NASA/GSFC` |
| `NHQ201708210100.jpg` / `.tif` & `NHQ201708210116.jpg` / `.tif` | `AR3` (`s03`, `s05`) | `<NAS_027_POOL>/eclipse/NHQ201708210100.tif` (`6,774,426 B`) & `NHQ201708210116.tif` (`10,903,248 B`) | Free download, `images-api.nasa.gov` (`NHQ201708210100`, `NHQ201708210116`) | Public domain · Credit: `NASA` |
| `ESO_timelapse_La_Silla.webm` (`1920×1090`, `33.9 s`) | `AR3` (`s06`), `AR4` (`s05`) | `<NAS_027_POOL>/stars/ESO_timelapse_La_Silla.webm` (`6,100,348 B`) | Free download, Wikimedia Commons (`File:Time-lapse Over La Silla.webm`) / ESO | `CC BY 4.0` · Credit: `R. Wesson/ESO, CC BY 4.0` |
| `lasilla_mw.mp4` & `orion_over_paranal.mp4` | `AR4` (`s01`, `s03`, `s07`) | `<MINI_OWB>/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/harvest_v01/lasilla_mw.mp4` & `orion_over_paranal.mp4` | Free download, ESO (`eso.org/public/videos/`) | `CC BY 4.0` · Credit: `ESO, CC BY 4.0` |
| `PIA17485` (1986 Halley Comet image) | `AR4` (`s02`) | Not cached locally — free API download at build time (`£0`) | Free download, `images-api.nasa.gov` (`PIA17485`) | Public domain · Credit: `NASA/JPL` |

### Optional Paid Mint Menu (Priced for Chief — Not Required)

As in `v01`, **`030_apophis_short_v13a` used zero Orbit clips and zero Veo clips** (`"spend": "none"`). All three primary Shorts (`AR1`, `AR2`, `AR3`) build at **`£0.00` picture spend** from the verified NAS/Mini assets and code graphics above.
- **Voiceover (after Chief stamps `script PASS`):** ~260–280 ElevenLabs credits per 46-word Short (~810 credits total across `AR1`–`AR3`; **£0 marginal**, subscription credit, no floor).
- **Optional Veo 2 / Flow UI hero plate:** **£0.00** via Flow UI (`orbit_flow_veo_ui.py`, AI Ultra subscription) or `~£1.20–£2.00` / 5 s clip on Vertex trial credit if Chief ever wants a synthetic atmospheric re-entry shot for `AR2`. **Recommended: £0 NASA/NAS + code graphics.**

---

## 9. Packaging Manifests (`11_Upload-Package/`)

Updated in `v02` (no schedule, no upload):
- `00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/11_Upload-Package/owb_ar1_2024_yr4_moon/PACKAGE_MANIFEST.json`
- `00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/11_Upload-Package/owb_ar2_iss_2030_deorbit/PACKAGE_MANIFEST.json`
- `00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/11_Upload-Package/owb_ar3_2027_eclipse/PACKAGE_MANIFEST.json`
- `00_Brand/Channel-Setup/audits/APOPHIS_REPLICATION_TEST_2026-10/11_Upload-Package/owb_ar4_halley_2061/PACKAGE_MANIFEST.json`

## 10. For Chief (Parked for `script PASS`)

1. All 7 fixes from **Chief h28 (`#6533691867`)** are in `SCRIPTS_AND_PACKAGING_v02.md` (`v01` kept alongside it).
2. Ready for Chief **`script PASS`** to unlock VO (`~810` ElevenLabs credits across `AR1`–`AR3`), £0 code graphics + assembly from the verified NAS pool, and gates (`gate_shorts_open.py check`, `picture_qa.py`, `sfx_kit.py level`).
