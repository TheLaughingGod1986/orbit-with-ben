# 067 — What Would Happen If You Fell Into Neptune? (2,000 km/h Winds)

> **Job:** `J2778` (`macbook`, 2026-11-13)  
> **Stage:** Topic & Pre-Build Data Brief (appended to `jobs/WIP.json` `next` under Rule G: starts only when an active OWB WIP slot frees up; queued for Rule-E topic go/no-go review)  
> **Primary Sources Read Before Writing:**
> - `05_Analytics/owb/snapshots/2026-11-13.json` (pulled `2026-11-13T06:40:09Z`; `100` public videos = `16` longs + `84` Shorts; `17` subscribers, `16,605` total public views)
> - `05_Analytics/owb/studio_ctr.json` (pulled `2026-11-12T07:09:40Z`; Studio impressions, CTR, average view duration, average % viewed, Shorts `stayedToWatch`, and d1 feed share)
> - `05_Analytics/owb/channel_daily.json` (YouTube Analytics retention quartiles `r15`, `r30`, `r50`, `r90`, traffic sources, and daily channel totals)
> - `05_Analytics/owb/REPORT.md` (daily/weekly/monthly channel report + 28-day traffic source split: Shorts `92%` Shorts feed / `7%` YT search; Longs `80%` Browse features / `9%` YT search / `4%` Direct / `4%` Suggested)
> - `05_Analytics/LEARNINGS.md` (Rules 1–31 + active Short experiment `OWB-2026-11-E1`)

---

## 1. Learn From Our Data First (`2026-11-13` Snapshot + `studio_ctr.json` + `channel_daily.json`)

### 1.1 All 16 Public OWB Longs Ranked by Views/Day Since Publish, CTR, and Average % Viewed

| Rank (VPD) | Video ID | Published | Age (d) | Length | Title | Public Views | Views / Day | Impressions (`studio_ctr`) | CTR (`%`) | Avg % Viewed (Studio / YTA) | Retention (`0:15` / `0:30` / `50%` / `90%`) |
|---:|---|---|---:|---:|---|---:|---:|---:|---:|---|---|
| **1** | `VBaYRPp85Sw` | 2026-10-25 | 19 | `514 s` (`8:34`) | *What Happened to Venus?* | **230** | **12.11** | **1,324** | `1.96%` | **25.24%** (`129 s`) / `17.9%` | `84%` / `51%` / `24%` / `16%` |
| **2** | `55AEQwvs36g` | 2026-10-11 | 33 | `560 s` (`9:20`) | *How Long Do Saturn's Rings Have Left?* | **218** | **6.61** | **1,269** | `2.05%` | **15.23%** (`85 s`) / `15.2%` | `55%` / `33%` / `10%` / `8%` |
| **3** | `Js6EQJ8qDi8` | 2026-11-08 | 5 | `491 s` (`8:11`) | *Could a Robot Survive on Mars? (One Lasted 14 Years)* | **11** (`9` Studio) | **2.20** | `56` | `1.79%` | **27.66%** (`135 s`) / `27.7%` | `–` (5d old) |
| **4** | `REXYxuLOBoI` | 2026-08-27 | 78 | `518 s` (`8:38`) | *The Last Star: What Happens When a Red Dwarf Dies?* | **46** | **0.59** | `199` | `2.01%` | **24.23%** (`125 s`) / `25.1%` | `73%` / `42%` / `23%` / `14%` |
| **5** | `ziKBPJ6FY0U` | 2026-08-20 | 85 | `993 s` (`16:33`) | *JWST Found Galaxies That Shouldn't Exist Yet* | **33** | **0.39** | `131` | `1.53%` | **21.41%** (`212 s`) / `22.7%` | `98%` / `66%` / `19%` / `19%` |
| **6** | `h8HGfyShEHI` | 2026-10-18 | 26 | `519 s` (`8:39`) | *Is the Sun Getting Brighter?* | **9** | **0.35** | `135` | **3.70% (#2)** | **21.84%** (`113 s`) / `21.9%` | `–` |
| **7** | `m09jUdwC5hk` | 2026-10-21 | 23 | `2,858 s` (`47:38`) | *How Long Will Anything in Space Last?* *(compilation — banned by Rule 9)* | `6` | `0.26` | `92` | `0.00%` | `33.77%` (`965 s` Studio / `19 s` YTA) | `–` |
| **8** | `Yk1tLh23rko` | 2026-09-10 | 64 | `583 s` (`9:43`) | *What Happens If You Get Near a Neutron Star or Pulsar?* | `15` | `0.23` | `263` | `2.28%` | `2.89%` (`16 s`) / `4.3%` | `55%` / `26%` / `–` / `9%` |
| **9** | `NbW5G1BpPY0` | 2026-09-03 | 71 | `559 s` (`9:19`) | *Could Life Exist Under The Ice Of Europa?* | `15` | `0.21` | `80` | `1.25%` | `22.88%` (`127 s`) / `23.7%` | `–` |
| **10** | `b8-X_FyJnHM` | 2026-08-13 | 92 | `1,289 s` (`21:29`) | *Alien Worlds: The Strangest Planets We've Ever Found* | `13` | `0.14` | `112` | **2.68% (#3)** | `4.07%` (`52 s`) / `5.1%` | `53%` / `48%` / `9%` / `9%` |
| **11** | `-jmMROGoZCM` | 2026-10-04 | 40 | `594 s` (`9:54`) | *Why You Can't Stand On Jupiter* | `5` | `0.12` | `58` | **5.17% (#1)** | `9.32%` (`55 s`) / `9.4%` | `–` |
| **12** | `Mo93x0fxB1Q` | 2026-07-30 | 106 | `1,112 s` (`18:32`) | *Why Haven't We Found Aliens Yet? The Fermi Paradox Explained* | `13` | `0.12` | `97` | `0.00%` | `12.98%` (`144 s`) / `13.4%` | `86%` / `39%` / `10%` / `10%` |
| **13** | `2fsQcea-voM` | 2026-09-17 | 57 | `519 s` (`8:39`) | *Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone* | `5` | `0.09` | `67` | `1.49%` | **1.72%** (`8 s`) / `2.7%` | `–` |
| **14** | `ojk-dfOpAmw` | 2026-09-24 | 50 | `621 s` (`10:21`) | *What Happens During the Milky Way Andromeda Collision?* | `4` | `0.08` | `52` | `0.00%` | `26.42%` (`164 s`) / `26.4%` | `–` |
| **15** | `3xrxdmaOwJI` | 2026-08-05 | 100 | `1,273 s` (`21:13`) | *What Happens If You Fall Into a Black Hole?* | `6` | `0.06` | `72` | `1.39%` | `34.14%` (`434 s`) / `37.2%` | `–` |
| **16** | `rVqgtkBV3jc` | 2026-11-01 | 12 | `492 s` (`8:12`) | *What Happens If You Travel Near Light Speed?* | **0** | **0.00** | `40` | `0.00%` | `–` | `–` |

---

### 1.2 Top & Bottom Public OWB Shorts (`84` Public Shorts in `2026-11-13` Snapshot)

| Category | Video ID | Published | Age (d) | Length | Title | Public Views | Views / Day | Stayed to Watch (`%`) | Avg % Viewed (`AVD`) | d1 Feed Share |
|---|---|---|---:|---:|---|---:|---:|---:|---|---|
| **Top #1 VPD** | `iyvWYFP_ETA` | 2026-11-09 | 4 | `26 s` | *Could a Robot Survive a Night on Mars?* | **1,074** (`1,060` Studio) | **268.50** | **38.77%** | `62.64%` (`16 s`) | `96%` |
| **Top #2 VPD / #1 Views & Search** | `T9fVlG3CCzU` | 2026-11-07 | 6 | `21 s` | *What Are Shooting Stars Really Made Of?* | **1,285** (`1,282` Studio) | **214.17** | **49.79% (#2 ≥100v)** | `66.35%` (`13 s`) | `92%` (`84` YT search views) |
| **Top #3 VPD / #2 Views** | `VfDm3E2bUgU` | 2026-10-31 | 13 | `19 s` | *Why Do Astronauts See 16 Sunrises a Day?* | **1,090** | **83.85** | `31.60%` | `66.73%` (`12 s`) | `96%` |
| **Top #4 VPD** | `hZH0C7fpCk4` | 2026-11-02 | 11 | `20 s` | *How Big Is Venus Compared to Earth?* | **566** | **51.45** | `29.11%` | `66.24%` (`13 s`) | `98%` |
| **Top #5 VPD / #3 Views** | `OVLv9dxTcpE` | 2026-10-26 | 18 | `22 s` | *What If Earth Stopped Spinning?* | **892** | **49.56** | `30.69%` | `75.86%` (`16 s`) | `98%` |
| **Top #1 Loop % (`≥100v`)** | `ZpEA8stoSPA` | 2026-11-03 | 10 | `22 s` | *Why Does Uranus Have 21-Year Winters?* | **481** | **48.10** | `26.93%` | **306.81%** (`67 s` multi-loop) | `94%` |
| **Top #1 Stayed (`≥100v`)** | `y-SPHQ0-VjQ` | 2026-10-19 | 25 | `27 s` | *Why Is the Sun Getting Brighter as It Runs Out of Fuel?* | **109** | `4.36` | **56.82% (#1 ≥100v)** | **78.59%** (`21 s`; `132.34%` feed) | `54%` |
| **Top #3 Stayed (`≥100v`)** | `1OCNzhkiBuc` | 2026-10-27 | 17 | `21 s` | *Why Are the Winds on Neptune Faster Than Sound?* | **495** | **29.12** | **42.64% (#3 ≥100v)** | **74.98%** (`15 s`) | `94%` |
| **Top #2 Loop % (`≥100v`)** | `gJwNJN_yMKU` | 2026-10-28 | 16 | `19 s` | *How Close Will Asteroid Apophis Pass Earth on Friday the 13th?* | **462** | **28.88** | **34.46%** | **231.03%** (`43 s` loop; `214K` FB) | `93%` |
| **Worst #1 VPD / Views** | `TE_HDKAnqms` | 2026-09-09 | 65 | `27 s` | *If Life Starts Under Ice, It's Everywhere* | **2** | **0.03** | **0.00%** | `–` | `0%` |
| **Worst #2 Statement Short** | `23KZK7OjsEE` | 2026-10-17 | 27 | `23 s` | *Jupiter Has No Ground* | **8** | **0.30** | `33.33%` | `34.24%` (`7 s`) | `10%` |
| **Worst #3 Statement Short** | `lbW2iQ9YvqA` | 2026-10-20 | 24 | `24 s` | *Saturn's Rings Are on a Clock* | **12** | **0.50** | `25.00%` | `30.86%` (`7 s`) | `0%` |
| **Worst Stayed (`≥100v`)** | `n2WbOfJhOwc` | 2026-09-02 | 72 | `28 s` | *Star Recycling Isn't Perfect* | `213` | `2.96` | **15.38%** | `38.99%` (`10 s`) | `97%` |

---

### 1.3 Three Best vs Three Worst Longs & Shorts — Exact Numbers and Shared DNA

- **3 Best Longs:**
  1. `VBaYRPp85Sw` (*What Happened to Venus?*, `514 s` / `8:34`): **230 views**, **12.11 vpd (#1)**, **1,324 impr (#1)**, **1.96% CTR**, **25.24% Studio avg viewed (`129 s`)**, retention `84% / 51% / 24% / 16%`.
  2. `55AEQwvs36g` (*How Long Do Saturn's Rings Have Left?*, `560 s` / `9:20`): **218 views**, **6.61 vpd (#2)**, **1,269 impr (#2)**, **2.05% CTR**, **15.23% avg viewed (`85 s`)**, retention `55% / 33% / 10% / 8%`.
  3. `Js6EQJ8qDi8` (*Could a Robot Survive on Mars? (One Lasted 14 Years)*, `491 s` / `8:11`): **11 public / 9 Studio views**, **2.20 vpd (#3)**, `56` impr, `1.79%` CTR, **27.66% Studio avg viewed (`135 s`)** — plus CTR #1 `-jmMROGoZCM` (*Why You Can't Stand On Jupiter*, **5.17% CTR**) & CTR #2 `h8HGfyShEHI` (*Is the Sun Getting Brighter?*, **3.70% CTR**).
  - **Shared DNA:** Named Solar System planets (`Venus`, `Saturn`, `Mars`, `Jupiter`, `Sun`), short positive question or Rule 26 search phrase + bracketed stakes tail, `8.2–9.3 min` runtime (`Rule 16`), and immediate proof-first opening (`Rule 10` & `J2428`).

- **3 Worst Longs:**
  1. `rVqgtkBV3jc` (*What Happens If You Travel Near Light Speed?*, `492 s`): **0 views**, **0.00 vpd (#16)**, `40` impr, `0.00%` CTR.
  2. `3xrxdmaOwJI` (*What Happens If You Fall Into a Black Hole?*, `1,273 s`): **6 views**, **0.06 vpd (#15)**, `72` impr, `1.39%` CTR.
  3. `2fsQcea-voM` (*Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone*, `519 s`): **5 views**, **0.09 vpd (#13)**, **1.72% avg viewed (`8 s`)**; and `ojk-dfOpAmw` (*What Happens During the Milky Way Andromeda Collision?*, `621 s`, **4 views**, **0.08 vpd (#14)**, `0.00%` CTR).
  - **Shared DNA:** Abstract non-Solar-System textbook questions (`rVqgtkBV3jc`, `3xrxdmaOwJI`), overlong `18–21 min` runtimes (`Rule 16`), dash-split titles, or agenda openings (`Rule 10`).

- **3 Best Shorts:**
  1. `iyvWYFP_ETA` (*Could a Robot Survive a Night on Mars?*, `26 s`): **1,074 views**, **268.50 vpd (#1)**, **38.77% stayed**, **62.64% avg viewed**, `96%` d1 feed.
  2. `T9fVlG3CCzU` (*What Are Shooting Stars Really Made Of?*, `21 s`): **1,285 views (#1 all-time)**, **214.17 vpd (#2)**, **49.79% stayed (#2 ≥100v)**, **66.35% avg viewed**, `84` YT search views.
  3. `VfDm3E2bUgU` (*Why Do Astronauts See 16 Sunrises a Day?*, `19 s`): **1,090 views (#2 all-time)**, **83.85 vpd (#3)**, `31.60%` stayed, **66.73% avg viewed** — alongside Stayed #3 `1OCNzhkiBuc` (*Why Are the Winds on Neptune Faster Than Sound?*, `21 s`, **495 views**, **29.12 vpd**, **42.64% stayed**, **74.98% avg viewed**) and Loop #1 `ZpEA8stoSPA` (*Why Does Uranus Have 21-Year Winters?*, `22 s`, **481 views**, **306.81% avg viewed**).
  - **Shared DNA:** Positive search questions (`Why / What / Could`), `18–26 s` length, full-bleed `mode: "cover"` (`0%` blur bars), `t = 0.0 s` hook text (`#FFE000` keyword), `≤1.5 s` spoken surprise, and `5.5–8.5 s` stat overlay (`Rule 24`).

- **3 Worst Shorts:**
  1. `TE_HDKAnqms` (*If Life Starts Under Ice, It's Everywhere*, `27 s`): **2 views**, **0.03 vpd (#84)**, **0.00% stayed**.
  2. `23KZK7OjsEE` (*Jupiter Has No Ground*, `23 s`: **8 views**, **0.30 vpd**) & `lbW2iQ9YvqA` (*Saturn's Rings Are on a Clock*, `24 s`: **12 views**, **0.50 vpd**).
  3. `n2WbOfJhOwc` (*Star Recycling Isn't Perfect*, `28 s`: `213` views, **15.38% stayed — worst Stayed-to-Watch among `≥100`v Shorts**).

---

## 2. Film `OWB:067` — Topic, Packaging, Hook, Data Proof, Neighbours & Short Angles

### 2.1 Non-Overlap Verification (`02_Video-Projects/`, `ideas/`, `VIDEO_BACKLOG.json`, `jobs/WIP.json`)
- Checked all folders in `02_Video-Projects/` (`001`–`063`, `064`–`065` in PR `#853`, and `066` in this PR), all shortlist files in `00_Brand/Channel-Setup/ideas/`, `VIDEO_BACKLOG.json`, and `jobs/WIP.json`:
  - **`0` existing films or idea cards** cover **falling into ice giant Neptune — its supersonic `2,000+ km/h` (`1,200+ mph`) methane winds, disappearing Earth-sized Great Dark Spot (`1989` Voyager 2 & Hubble), superheated high-pressure water-ammonia-methane ocean (`80%+` of its mass), and solid diamond rain**.
  - Note on `035_Why-Neptunes-Largest-Moon-Orbits-Backwards`: `035` was strictly about Neptune's captured moon **Triton** and its retrograde orbit. Even better, `035` spawned our breakout Short `1OCNzhkiBuc` (*Why Are the Winds on Neptune Faster Than Sound?* — **495 views**, **29.12 vpd**, **42.64% stayed — #3 highest Stayed-to-Watch among all `≥100`-view Shorts on the entire channel**, **74.98% avg viewed**), proving massive audience appetite on our own channel for a dedicated Long film about Neptune itself!

### 2.2 Working Title & Packaging Variants (`LEARNINGS.md` Rules 1, 15, 18, 20, 23, 26)
- **Locked Working Title (Rule 26 Search-Led Phrase First + Bracketed Story/Stakes Tail, `61 chars ≤ 70`):**  
  **`What Would Happen If You Fell Into Neptune? (2,000 km/h Winds)`**
  - **Exact YouTube Collision Check (`2026-11-13`, signed-out `gl=GB`):** **`0` exact matches**.
  - **Rule 26 Signed-Out YouTube Autocomplete Verification (`suggestqueries.google.com`, `gl=gb`):**
    - Query `"what would happen if you fell into neptune"` returns:
      1. `what would happen if you fell into neptune`
      2. `what would happen if you went to neptune`
      3. `what would you see if you fell into neptune`
    - Query `"what is inside neptune"` returns:
      1. `what is inside neptune`
      2. `what is inside neptune planet`
      3. `what is the temperature in neptune`
    - Query `"why is neptune so windy"` -> `['why is neptune so windy']`
    - Query `"it rains diamonds on neptune"` -> `['it rains diamonds on neptune']`
  - **Top 2 Ranking Videos on `"what would happen if you fell into neptune"` (`gl=GB`, `2026-11-13`):**
    1. `B0v7MihXA-s` — *What Would You See If You Fell Into Neptune? (4K UHD)* | V101 SPACE | **4,581,734 views** | `6:25` (`8y ago`)
    2. `R5pYI0vjI6k` — *What If You Fell Into Neptune and Kept FALLING for 20,000 KM?* | What If | **3,110,527 views** | `6:56` (`5y ago`)
- **Alternative Title Variants (for Packaging Panel & Test & Compare):**
  - **Title B (`LEARNINGS.md` Rule 15 Positive Question `≤50 chars`, `42 chars`, `0` exact collisions):**  
    `Why Are Neptune's Winds Faster Than Sound?`
  - **Title C (`LEARNINGS.md` Rule 18 Real Spacecraft Imagery Variant, `52 chars`, `0` exact collisions):**  
    `What Voyager 2 Saw Inside Neptune's Giant Dark Storm`
  - **Title D (`LEARNINGS.md` Rule 23 Story + Stakes Variant, `55 chars`, `0` exact collisions):**  
    `Why Neptune Has 2,000 km/h Winds and Solid Diamond Rain`

### 2.3 One-Line Cold-Open Hook (`0:00–0:08` Proof-First Open per `J2428` & Rule 10, Zero Agenda Line)
> *"Three billion miles from the Sun, where sunlight is nine hundred times dimmer than on Earth, Neptune has no solid ground to stand on — and if you dropped into its freezing blue clouds, supersonic winds over two thousand kilometres an hour would hurl you across astorm as wide as the Earth before crushing pressure turned methane into solid diamond rain."*

- **First-30-Second Retention Architecture (`J2428` / `AGENTS.md` Lesson 7):**
  - **`0:00` (Frame 0):** Real moving **NASA Voyager 2 (`August 1989`) + Hubble** plate of Neptune's Great Dark Spot and bright white methane-ice scooter clouds whipping across the planet (no Orbit character, no title card, no fade-from-black).
  - **`0:00–0:08`:** Spoken Sentence 1 states the title descent question, the `900×` dimmer sunlight paradox (`30 AU` / `2.8 billion miles` / `4.5 billion km`), the `2,000+ km/h` (`1,200+ mph`) supersonic winds, and the diamond-rain interior payoff.
  - **`0:08–0:20`:** Concrete payoff hint + `DATA` #1 (`2,000 km/h` / `1,200 mph` winds on Neptune vs `400 km/h` / `250 mph` maximum on Earth — `3×` stronger than Jupiter's and `9×` stronger than Earth's) with zero agenda or meta-promise lines.
  - **`0:20–0:45`:** Step-by-step altitude-and-pressure preview from the `55 K (-218 °C)` cloud tops at `0.1 bar` down into the superheated `80%-mass` water-ammonia-methane fluid mantle before the first chapter card at `≥0:45`.

### 2.4 Why It Should Work (Past Winners + `LEARNINGS.md` Rules Mapping)
1. **Directly Converts Our #3 Highest-Stayed Short on the Entire Channel (`1OCNzhkiBuc`) Into a Full Long:**
   - `1OCNzhkiBuc` (*Why Are the Winds on Neptune Faster Than Sound?*, `21 s`) earned **495 views**, **29.12 vpd**, **42.64% stayed (#3 among all `≥100`-view Shorts on OWB)**, **74.98% avg viewed (`15 s`)**, and **94% d1 Shorts feed share** — proving that Neptune's supersonic winds in `900×`-dimmer sunlight is one of the strongest hooks we have ever tested.
2. **Fixes the Exact Lesson from Our #1 CTR Long (`-jmMROGoZCM` *Why You Can't Stand On Jupiter*, `5.17%` CTR):**
   - `-jmMROGoZCM` achieved **5.17% CTR (#1 highest CTR across all 16 public Longs)** because falling into a giant planet with no solid surface is an irresistible click concept, but it stalled at `9.32%` avg viewed (`55 s`) because of a negative statement title (`Why You Can't...`) and a slow early opening. `067` combines that `#1-CTR` planetary-descent hook with a **Rule 26 positive search-first question (`What Would Happen If You Fell Into Neptune? (2,000 km/h Winds)`)** and a **Rule 10 / `J2428` proof-first `0:00–0:30` opening** modeled on `VBaYRPp85Sw` (*What Happened to Venus?*, **230 views**, **12.11 vpd**, **25.24% avg viewed**, `84%` at `0:15`) and `Js6EQJ8qDi8` (*Could a Robot Survive on Mars?*, **27.66% avg viewed**).
3. **Pairs With Our #1 Multi-Loop Ice-Giant Short (`ZpEA8stoSPA` *Why Does Uranus Have 21-Year Winters?*, `481` views, `306.81%` avg viewed):**
   - Ice-giant atmospheric extremes (`ZpEA8stoSPA` `481` views / `306.81%` loop on Uranus + `1OCNzhkiBuc` `495` views / `42.64%` stayed on Neptune) are proven retention leaders on OWB.
4. **Thumbnail 3-Way Test & Compare (`Rules 11, 12, 14, 18, 19`):**
   - **Thumb A (Consequence / Descent Scale):** Spacesuit silhouette / probe plunging into Neptune's roaring blue methane vortex above a glowing diamond-rain layer; `2–3` bold words top-left: `NO SOLID GROUND` or `2,000 KM/H` (zero Orbit character).
   - **Thumb B (`Rule 14` Bright-Background Variant):** Bright cyan-and-white methane cloud deck backlit by diamond crystals; text: `RAINS DIAMONDS`.
   - **Thumb C (`Rules 18 & 19` Graded Real NASA Voyager 2 Frame):** High-contrast NASA Voyager 2 (`1989`) close-up of Neptune's Earth-sized Great Dark Spot and bright white cirrus streaks; text: `MACH 1.7 WINDS`.

### 2.5 Verified NASA Primary-Source Fact Base (`0` Unverified Numbers)
- **NASA Science — Neptune Facts (`https://science.nasa.gov/neptune/neptune-facts/`):**
  - *"Dark, cold, and whipped by supersonic winds, ice giant Neptune is more than 30 times as far from the Sun as Earth... In 2011 Neptune completed its first 165-year orbit since its discovery in 1846. Neptune is so far from the Sun that high noon on the big blue planet would seem like dim twilight to us. The warm light we see here on our home planet is roughly 900 times as bright as sunlight on Neptune."*
  - *"With an equatorial diameter of 30,775 miles (49,528 kilometers), Neptune is about four times wider than Earth... From an average distance of 2.8 billion miles (4.5 billion kilometers), Neptune is 30 astronomical units away from the Sun... From this distance, it takes sunlight 4 hours to travel from the Sun to Neptune."*
  - *"One day on Neptune takes about 16 hours (the time it takes for Neptune to rotate or spin once). And Neptune makes a complete orbit around the Sun (a year in Neptunian time) in about 165 Earth years (60,190 Earth days)... Neptune’s axis of rotation is tilted 28 degrees with respect to the plane of its orbit around the Sun... each of the four seasons lasts for over 40 years."*
  - *"Neptune is one of two ice giants in the outer solar system (the other is Uranus). Most (80% or more) of the planet's mass is made up of a hot dense fluid of 'icy' materials – water, methane, and ammonia – above a small, rocky core. Of the giant planets, Neptune is the densest. Scientists think there might be an ocean of super hot water under Neptune's cold clouds. It does not boil away because incredibly high pressure keeps it locked inside."*
  - *"Neptune does not have a solid surface. Its atmosphere (made up mostly of hydrogen, helium, and methane) extends to great depths, gradually merging into water and other melted ices over a heavier, solid core with about the same mass as Earth."*
  - *"Neptune is our solar system's windiest world. Despite its great distance and low energy input from the Sun, Neptune's winds can be three times stronger than Jupiter's and nine times stronger than Earth's. These winds whip clouds of frozen methane across the planet at speeds of more than 1,200 miles per hour (2,000 kilometers per hour). Even Earth's most powerful winds hit only about 250 miles per hour (400 kilometers per hour). In 1989 a large, oval-shaped storm in Neptune's southern hemisphere dubbed the 'Great Dark Spot' was large enough to contain the entire Earth. That storm has since disappeared, but new ones have appeared on different parts of the planet."*
  - *"The main axis of Neptune's magnetic field is tipped over by about 47 degrees compared with the planet's rotation axis... The magnetic field of Neptune is about 27 times more powerful than Earth's."*
- **NASA NSSDCA — Neptune Fact Sheet (`https://nssdc.gsfc.nasa.gov/planetary/factsheet/neptunefact.html`):**
  - Mass: `102.409 × 10^24 kg` (`17.15` Earths); Equatorial radius (`1 bar`): `24,764 km` (`3.883` Earths); Mean density: `1,638 kg/m^3`; Gravity (`1 bar` mean): `11.27 m/s^2` (`1.15` Earth); Sidereal rotation: `16.11 hours`; Temperature at `0.1 bar`: `55 K (-218 °C)`; Temperature at `1 bar`: `72 K (-201 °C)`; Wind speeds: `0–580 m/s` (`2,088 km/h`); Atmospheric composition by volume: `80.0% H2`, `19.0% He`, `1.5% CH4` (methane); Discovery: `23 September 1846` by Johann Gottfried Galle from mathematical predictions by Urbain Le Verrier and John Couch Adams.

### 2.6 Verified Neighbour Pass (`≥3` Big Videos `≥1M` Views — Live Verified `2026-11-13`)

| # | Verified Views (`2026-11-13`) | Channel (Internal Note Only) | YouTube ID | Length | Title | Subject Words to Reuse (Never Channel Names) |
|---:|---:|---|---|---:|---|---|
| **1** | **4,581,734** | V101 SPACE | `B0v7MihXA-s` | `6:25` (`385 s`) | *What Would You See If You Fell Into Neptune? (4K UHD)* | `what would happen if you fell into neptune`, `falling into neptune`, `neptune clouds`, `great dark spot`, `ice giant` |
| **2** | **3,494,586** | Astrum | `wHNC-RhmHZY` | `31:02` (`1,862 s`) | *James Webb's New Images of Neptune Have Left Scientists Confused* | `neptune`, `neptune atmosphere`, `neptune rings`, `ice giant neptune`, `neptune storms` |
| **3** | **3,110,527** | What If | `R5pYI0vjI6k` | `6:56` (`416 s`) | *What If You Fell Into Neptune and Kept FALLING for 20,000 KM?* | `fell into neptune`, `neptune interior`, `diamond rain`, `superheated water ocean`, `2000 km/h winds` |
| **4** | **2,938,289** | BBC Earth Science | `NwEZKjkRgeY` | `4:27` (`267 s`) | *The Planet With Supersonic Winds \| The Planets \| Earth Science* | `supersonic winds`, `neptune winds`, `voyager 2 neptune`, `fastest winds in the solar system` |
| **5** | **2,888,966** | Astrum | `faKnto4Pb6c` | `13:33` (`813 s`) | *Our Solar System's Planets: Neptune* | `neptune`, `voyager 2`, `great dark spot`, `neptune magnetic field`, `ice giant` |
| **6** | **2,232,271** | Astrum | `DhLm_4pBrso` | `16:01` (`961 s`) | *What They Didn't Teach You in School about Neptune \| Our Solar System's Planets* | `neptune`, `neptune facts`, `supersonic winds`, `diamond rain on neptune` |
| **7** | **1,485,572** | What If | `vC8fZSStdJQ` | `13:24` (`804 s`) | *What If You Fell Into Neptune?* | `what if you fell into neptune`, `neptune pressure`, `methane clouds`, `diamond rain` |

- **Pool Strength:** **7 verified education/space videos between `1.49M` and `4.58M` views** (`4.58M`, `3.49M`, `3.11M`, `2.94M`, `2.89M`, `2.23M`, `1.49M`).

### 2.7 Two Short Angles (`LEARNINGS.md` Rules 1–8, 16, 22, 24 + `OWB-2026-11-E1`)

1. **Short `S01` (`19–21 s` Single-Fact Loop Cut):**
   - **YouTube Title (`52 chars`, verified `0` exact YouTube collisions):**  
     **`What Would Happen If You Fell Into Neptune's Clouds?`**
   - **Frame 0 (`t = 0.0 s`) Top-Safe Hook Text (`2–3` words, `#FFE000` keyword):**  
     `NO SOLID GROUND` (`NO` or `GROUND` in `#FFE000`, dark bar, `mode: "cover"` full-bleed `9:16` descent into Neptune's blue methane cloud deck, `0%` blur bars).
   - **First Spoken Sentence (`0.0–1.5 s` Surprise per Rule 24, `6 words`):**  
     *"Neptune has zero ground to hit."*
   - **Mid-Short Stat Overlay (`5.5–8.5 s`, `≤4 words` per Rule 24):**  
     `2,000 KM/H WINDS`
   - **Single Fact & Payoff (`≥70%` duration):**  
     At the top of Neptune's clouds (`-218 °C` at `0.1 bar`), frozen methane clouds whip past at more than `1,200 miles per hour (2,000 km/h)` — nine times faster than Earth's strongest hurricanes. As you fall deeper, there is no solid surface at all: the hydrogen-and-methane sky thickens into a crushing, superheated ocean of water, ammonia, and methane locked inside by immense pressure (`<1.2 s` tail after final word for seamless loop).

2. **Short `S02` (`19–21 s` Single-Fact Loop Cut):**
   - **YouTube Title (`50 chars`, verified `0` exact YouTube collisions):**  
     **`Does It Really Rain Solid Diamonds Inside Neptune?`**
   - **Frame 0 (`t = 0.0 s`) Top-Safe Hook Text (`2–3` words, `#FFE000` keyword):**  
     `SOLID DIAMOND RAIN` (`DIAMOND` in `#FFE000`, full-bleed `9:16` cross-section of Neptune's high-pressure mantle).
   - **First Spoken Sentence (`0.0–1.5 s` Surprise per Rule 24, `6 words`):**  
     *"Deep inside Neptune, the sky crystallises."*
   - **Mid-Short Stat Overlay (`5.5–8.5 s`, `≤4 words` per Rule 24):**  
     `80% HOT ICE FLUID`
   - **Single Fact & Payoff (`≥70%` duration):**  
     Neptune's blue colour comes from methane (`1.5%` of its upper atmosphere), which absorbs red light. Deep inside the planet — where `80% or more` of Neptune's `17-Earth` mass is a hot, dense fluid of water, methane, and ammonia under millions of bars of pressure — extreme heat and pressure strip carbon atoms out of methane and squeeze them into solid diamonds that sink like hailstones toward the rocky core (`<1.2 s` loop tail).
