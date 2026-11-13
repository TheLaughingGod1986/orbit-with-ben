# 066 — Why Do We Only See One Side of the Moon? (The Hidden Far Side)

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

#### A. Three Best Longs (`VBaYRPp85Sw`, `55AEQwvs36g`, `Js6EQJ8qDi8` — plus CTR leaders `-jmMROGoZCM` `5.17%` & `h8HGfyShEHI` `3.70%`)
1. **`VBaYRPp85Sw` — *What Happened to Venus?*** (`514 s` / `8:34`, `19d`): **230 views**, **12.11 views/day (#1)**, **1,324 impressions (#1)**, **1.96% CTR**, **25.24% Studio avg viewed (`129 s`)**, retention `84%` at `0:15` / `51%` at `0:30` / `24%` halfway / `16%` end.
2. **`55AEQwvs36g` — *How Long Do Saturn's Rings Have Left?*** (`560 s` / `9:20`, `33d`): **218 views**, **6.61 views/day (#2)**, **1,269 impressions (#2)**, **2.05% CTR**, **15.23% avg viewed (`85 s`)**, retention `55% / 33% / 10% / 8%`.
3. **`Js6EQJ8qDi8` — *Could a Robot Survive on Mars? (One Lasted 14 Years)*** (`491 s` / `8:11`, `5d`): **11 public views (`9` Studio)**, **2.20 views/day (#3)**, **56 impressions**, **1.79% CTR**, **27.66% Studio avg viewed (`135 s` — #1 among 8–9 min planetary films)**.
- **What the 3 Best Longs Share:**
  - **Subject:** Named Solar System worlds and hardware (`Venus`, `Saturn's Rings`, `Mars Rover`) with a concrete physical change, countdown, or survival test (`LEARNINGS.md` Rule 15 & Rule 23). Together, `VBaYRPp85Sw` and `55AEQwvs36g` generate **67.5% (`448 / 664`) of all public Long views** on the channel.
  - **Title Shape:** Short positive questions (`23–52 chars`) or Rule 26 search phrase + bracketed story/stakes tail (`Could a Robot Survive on Mars? (One Lasted 14 Years)`).
  - **Opening:** `VBaYRPp85Sw` (`84%` at `0:15`, `51%` at `0:30`) and `Js6EQJ8qDi8` (`27.66%` avg viewed) open immediately on the planetary stakes and physical proof rather than throat-clearing (`Rule 10` & `J2428`).
  - **Thumbnail Concept:** High-contrast planetary consequence (`1–3` words, zero character clutter, bright readable focal object per Rules 11, 12, 14, 18, 19).
  - **Length:** **`8.2–9.3 minutes` (`491–560 s`)** — inside the `8–10 min` trust window (`Rule 16`).

#### B. Three Worst Longs (`rVqgtkBV3jc`, `3xrxdmaOwJI`, `2fsQcea-voM` / `ojk-dfOpAmw`)
1. **`rVqgtkBV3jc` — *What Happens If You Travel Near Light Speed?*** (`492 s`, `12d`): **0 views**, **0.00 views/day (#16 worst)**, `40` impressions, `0.00%` CTR.
2. **`3xrxdmaOwJI` — *What Happens If You Fall Into a Black Hole?*** (`1,273 s` / `21:13`, `100d`): **6 views**, **0.06 views/day (#15)**, `72` impressions, `1.39%` CTR.
3. **`2fsQcea-voM` — *Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone*** (`519 s`, `57d`): **5 views**, **0.09 views/day (#13)**, `67` impressions, `1.49%` CTR, **1.72% avg viewed (`8 s` — worst retention on the channel)**; alongside **`ojk-dfOpAmw` — *What Happens During the Milky Way Andromeda Collision?*** (`621 s`, `50d`, **4 views**, **0.08 vpd (#14)**, `52` impr, `0.00%` CTR).
- **What the 3 Worst Longs Share:**
  - **Subject:** Either abstract textbook relativity/black-hole topics with no named Solar System anchor (`rVqgtkBV3jc`, `3xrxdmaOwJI`) where mega-channels already own every browse slot (`Rule 15`), or billion-year abstract drift (`ojk-dfOpAmw`, `2fsQcea-voM`).
  - **Title Shape:** Either generic textbook questions (`What Happens If You Travel Near Light Speed?`) or two-part dash-split titles (`Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone`, `67 chars`) that give away the answer in the first clause (`Rule 1` & `Rule 10`).
  - **Opening:** `2fsQcea-voM` lost viewers at `8 s` (`1.72%` avg viewed) because it opened on an abstract agenda line (`3.8 cm/year`) instead of an immediate visual contradiction (`Rule 10` & `J2428`).
  - **Length:** Early `18–21 min` films (`3xrxdmaOwJI` `1,273 s`, `Mo93x0fxB1Q` `1,112 s`, `b8-X_FyJnHM` `1,289 s`) average `0.11 vpd`, and the `47:38` compilation `m09jUdwC5hk` got `0.00%` CTR (`Rule 9` & `Rule 16`).

#### C. Three Best Shorts (`iyvWYFP_ETA`, `T9fVlG3CCzU`, `VfDm3E2bUgU` — plus Stayed/Loop leaders `y-SPHQ0-VjQ` `56.82%`, `1OCNzhkiBuc` `42.64%`, `ZpEA8stoSPA` `306.81%`)
1. **`iyvWYFP_ETA` — *Could a Robot Survive a Night on Mars?*** (`26 s`, `4d`): **1,074 views**, **268.50 views/day (#1 velocity)**, **38.77% stayed**, **62.64% avg viewed (`16 s`)**, `96%` d1 Shorts feed.
2. **`T9fVlG3CCzU` — *What Are Shooting Stars Really Made Of?*** (`21 s`, `6d`): **1,285 views (#1 all-time views)**, **214.17 views/day (#2 velocity)**, **49.79% stayed (#2 among `≥100`v Shorts)**, **66.35% avg viewed (`13 s`)**, `92%` d1 feed + **84 YouTube search views (#1 search Short on the channel)**.
3. **`VfDm3E2bUgU` — *Why Do Astronauts See 16 Sunrises a Day?*** (`19 s`, `13d`): **1,090 views (#2 all-time views)**, **83.85 views/day (#3 velocity)**, `31.60%` stayed, **66.73% avg viewed (`12 s`)**, `96%` d1 feed.
- **What the 3 Best Shorts Share:**
  - **Subject:** **Visible-from-the-ground sky wonders (`Rule 31`)** (`Shooting Stars`, `ISS 16 Sunrises`) and **real Solar System hardware survival (`iyvWYFP_ETA`, `n_4XskX0yZk` `891` views)** or **planetary weather extremes (`1OCNzhkiBuc` `495` views / `42.64%` stayed; `ZpEA8stoSPA` `481` views / `306.81%` loop)**.
  - **Title Shape:** Question-titled (`Why / What / Could / How`, `38–52 chars`). Across all 84 Shorts, question-titled Shorts earn `98%+` of total Shorts views (`Rule 2`).
  - **Opening & Visuals:** Full-bleed `9:16` (`mode: "cover"`, `0%` blur bars), `2–3` word top-safe hook text on Frame 0 (`t = 0.0 s`) with one `#FFE000` keyword, 5–6 word spoken surprise in `0.0–1.5 s`, and a single mid-Short stat overlay at `5.5–8.5 s` (`Rules 3–8, 22, 24` + `OWB-2026-11-E1`).
  - **Length:** **`18–26 seconds`** (`T9fVlG3CCzU` `21 s`, `VfDm3E2bUgU` `19 s`, `iyvWYFP_ETA` `26 s`, `1OCNzhkiBuc` `21 s`, `ZpEA8stoSPA` `22 s`) — delivering one surprising visual turn (`Rule 8` & `Rule 16`).

#### D. Three Worst Shorts (`TE_HDKAnqms`, `23KZK7OjsEE` / `lbW2iQ9YvqA`, `n2WbOfJhOwc`)
1. **`TE_HDKAnqms` — *If Life Starts Under Ice, It's Everywhere*** (`27 s`, `65d`): **2 views**, **0.03 views/day (#84 worst)**, **0.00% stayed**, `0%` d1 feed.
2. **`23KZK7OjsEE` — *Jupiter Has No Ground*** (`23 s`, `27d`: **8 views**, **0.30 vpd**, `33.33%` stayed, `34.24%` avg viewed / `7 s`) & **`lbW2iQ9YvqA` — *Saturn's Rings Are on a Clock*** (`24 s`, `24d`: **12 views**, **0.50 vpd**, `25.00%` stayed, `30.86%` avg viewed / `7 s`).
3. **`n2WbOfJhOwc` — *Star Recycling Isn't Perfect*** (`28 s`, `72d`: `213` views, `2.96 vpd`, **15.38% stayed — #1 worst Stayed-to-Watch among `≥100`v Shorts**, `38.99%` avg viewed / `10 s`).
- **What the 3 Worst Shorts Share:**
  - **Title Shape:** Declarative statements (`If Life Starts Under Ice...`, `Jupiter Has No Ground`, `Saturn's Rings Are on a Clock`, `Star Recycling Isn't Perfect`) with zero open search question (`Rule 2`).
  - **Opening & Visuals:** Abstract thesis statements or mid-sentence long-form extracts (`Rule 21`) that give away the conclusion in the title and fail the `0–2 s` swipe gate.

---

## 2. Film `OWB:066` — Topic, Packaging, Hook, Data Proof, Neighbours & Short Angles

### 2.1 Non-Overlap Verification (`02_Video-Projects/`, `ideas/`, `VIDEO_BACKLOG.json`, `jobs/WIP.json`)
- Checked all folders in `02_Video-Projects/` (`001`–`063` + `064` Shooting Stars & `065` ISS Deorbit in PR `#853`), all shortlist files in `00_Brand/Channel-Setup/ideas/`, `VIDEO_BACKLOG.json`, and `jobs/WIP.json`:
  - **`0` existing films or idea cards** cover **why we only see one side of the Moon (tidal locking) and why the lunar far side looks like a completely different world** (almost zero dark basaltic maria, a crust up to `37 miles / 60 km` thick vs `25 miles / 40 km` on the near side, first seen by Soviet **Luna 3** in **1959**, photographed by **Apollo 8** in **1968**, and mapped by NASA's **Lunar Reconnaissance Orbiter (LRO)** and **GRAIL**).
  - Note on `013_Why-The-Moon-Is-Slowly-Leaving-Us` (`2fsQcea-voM`): `013` was strictly about the Moon's future outward drift (`1.5 inches / 3.8 cm` per year) and total solar eclipses millions of years from now. It did not explain why the Moon is tidally locked (`27`-day spin matching its `27`-day sidereal orbit) or what spacecraft found on the hidden far side. Even better, `066` directly fixes the two flaws that hurt `013` (`2fsQcea-voM` had a `67-char` dash-split title and an abstract opening that dropped to `1.72%` AVD) by using our proven **Rule 26 search-first question (`why do we only see one side of the moon`) + Rule 18 real NASA LRO / Apollo far-side comparison on Frame 0 (`J2428`)**.

### 2.2 Working Title & Packaging Variants (`LEARNINGS.md` Rules 1, 15, 18, 23, 26, 31)
- **Locked Working Title (Rule 26 Search-Led Phrase First + Bracketed Story/Stakes Tail, `62 chars ≤ 70`):**  
  **`Why Do We Only See One Side of the Moon? (The Hidden Far Side)`**
  - **Exact YouTube Collision Check (`2026-11-13`, signed-out `gl=GB`):** **`0` exact matches**.
  - **Rule 26 Signed-Out YouTube Autocomplete Verification (`suggestqueries.google.com`, `gl=gb`):**
    - Query `"why do we only see one side of the moon"` returns:
      1. `why do we only see one side of the moon`
      2. `why do we only see one side of the moon animation`
      3. `why do we see only one side of the moon always`
      4. `why we see only one side of the moon always`
    - Query `"what is on the far side of the moon"` returns:
      1. `what is on the far side of the moon`
      2. `what is on the other side of the moon`
      3. `what nasa found on the far side of the moon`
      4. `what does the other side of the moon look like`
  - **Top 2 Ranking Videos on `"why do we only see one side of the moon"` (`gl=GB`, `2026-11-13`):**
    1. `6jUpX7J7ySo` — *Tidal Locking | Why Do We Only See One Side of the Moon?* | MinuteEarth | **4,213,040 views** | `2:01` (`11y ago`)
    2. `j91XTV_p9pc` — *Earth's Moon: Why One Side Always Faces Us* | Conceptual Academy | **2,072,539 views** | `7:59` (`11y ago`)
    - **Search Gap:** Both top-ranking videos are **11 years old** (`2015`), and neither combines the tidal-locking mechanism with NASA's LRO / GRAIL crustal-thickness solution (`25 miles / 40 km` near-side crust vs `37 miles / 60 km` far-side crust) in our `8.5–9.0 min` trust window!
- **Alternative Title Variants (for Packaging Panel & Test & Compare):**
  - **Title B (`LEARNINGS.md` Rule 15 Positive Question `≤50 chars`, `40 chars`, `0` exact collisions):**  
    `Why Does the Moon Only Show Us One Side?`
  - **Title C (`LEARNINGS.md` Rule 18 Real Spacecraft Imagery Variant, `50 chars`, `0` exact collisions):**  
    `What NASA Photographed on the Far Side of the Moon`
  - **Title D (`LEARNINGS.md` Rule 23 Story + Stakes Variant, `57 chars`, `0` exact collisions):**  
    `Why the Far Side of the Moon Looks Like a Different World`

### 2.3 One-Line Cold-Open Hook (`0:00–0:08` Proof-First Open per `J2428` & Rule 10, Zero Agenda Line)
> *"Every human who has ever looked up from Earth has seen the exact same face of the Moon — because the Moon takes twenty-seven Earth days to spin once on its axis and twenty-seven days to orbit the Earth, locking a hidden far side with a crust up to sixty kilometres thick forever out of our view."*

- **First-30-Second Retention Architecture (`J2428` / `AGENTS.md` Lesson 7):**
  - **`0:00` (Frame 0):** Real moving split-screen comparison from **NASA's Lunar Reconnaissance Orbiter (LRO)** showing the familiar dark basaltic maria of the lunar near side beside the bright, battered, almost completely maria-free highlands of the lunar far side (no Orbit character, no title card, no fade-from-black).
  - **`0:00–0:08`:** Spoken Sentence 1 states the title mystery (`why we only see one side of the Moon`), the `27-day` synchronous spin-orbit lock, and the `60-km` (`37-mile`) far-side crust contrast.
  - **`0:08–0:20`:** Concrete payoff hint + `DATA` #1 (`27.3 days` spin = `27.3 days` sidereal orbit; `40 km / 25 mi` near-side crust vs `60 km / 37 mi` far-side crust) showing how Soviet **Luna 3** (`1959`) and **NASA LRO** revealed a hemisphere with almost no dark volcanic seas (`maria`). Zero agenda or meta-promise lines (`"In this video..."` banned).
  - **`0:20–0:45`:** Visual turn every `≤4 s` contrasting the "dark side" myth (during a New Moon, the hidden far side is in full blazing sunlight at up to `390 K / +240 °F`) before the first chapter card at `≥0:45`.

### 2.4 Why It Should Work (Past Winners + `LEARNINGS.md` Rules Mapping)
1. **Matches Our #1 & #2 All-Time Shorts (`Rule 31` Visible-From-The-Ground Discovery Bonus):**
   - `T9fVlG3CCzU` (*What Are Shooting Stars Really Made Of?* — **1,285 views**, **214.17 vpd**, **49.79% stayed**, **84 YT search views**) and `VfDm3E2bUgU` (*Why Do Astronauts See 16 Sunrises a Day?* — **1,090 views**, **83.85 vpd**) proved that questions about objects a viewer can walk outside and see tonight outperform deep-space abstractions by `10×–50×`. The Moon's unchanging face is the single most visible naked-eye sky puzzle on Earth (`Rule 31`).
2. **Matches Our Top Day-And-Night / Rotation Paradox Shorts (`vlkj8RQKmH8`, `OVLv9dxTcpE`, `ZpEA8stoSPA`):**
   - `OVLv9dxTcpE` (*What If Earth Stopped Spinning?* — **892 views**, **49.56 vpd**, **75.86% avg viewed**), `vlkj8RQKmH8` (*Why Does a Day on Mercury Last Two of Its Years?* — **851 views**, **42.55 vpd**, **76.07% avg viewed**), and `ZpEA8stoSPA` (*Why Does Uranus Have 21-Year Winters?* — **481 views**, **48.10 vpd**, **306.81% loop**) prove that planetary spin-and-orbit paradoxes drive elite completion and looping.
3. **Matches Our #1 & #2 Longs (`VBaYRPp85Sw` `230` views / `12.11 vpd` & `55AEQwvs36g` `218` views / `6.61 vpd`):**
   - Like *What Happened to Venus?* (`25.24%` Studio avg viewed, `84%` at `0:15`, `51%` at `0:30`), `066` pairs a side-by-side world comparison (near side vs far side) with a clear physical mechanism (Earth's gravity pulling a tidal football bulge until the Moon's spin locked, plus why lava flooded the thinner `25-mile / 40-km` near-side crust between `4.2` and `1.2 billion years ago` while the `37-mile / 60-km` far-side crust stayed sealed).
4. **Thumbnail 3-Way Test & Compare (`Rules 11, 12, 14, 18, 19`):**
   - **Thumb A (Consequence / Split-World Contrast):** Side-by-side real LRO globe of the dark-plain Near Side vs the heavily cratered Far Side; `2–3` bold words top-left: `HIDDEN HALF` (`#FFE000` + `#FFFFFF`, zero Orbit character).
   - **Thumb B (`Rule 14` Bright-Background Variant):** Bright sunlit far-side lunar highlands from Apollo / LRO with Earth rising on the limb; text: `NEVER TURNS`.
   - **Thumb C (`Rules 18 & 19` Graded Real NASA LRO / Apollo Frame):** High-contrast NASA LRO elevation/albedo photograph of the lunar far side; text: `60 KM CRUST`.

### 2.5 Verified NASA Primary-Source Fact Base (`0` Unverified Numbers)
- **NASA Science — Moon Facts (`https://science.nasa.gov/moon/facts/`):**
  - *"With a radius of about 1,080 miles (1,740 kilometers), the Moon is less than a third of the width of Earth... The Moon is an average of 238,855 miles (384,400 kilometers) away. That means 30 Earth-sized planets could fit in between Earth and the Moon."*
  - *"The Earth and Moon are tidally locked. Their rotations are so in sync we only see one side of the Moon. Humans didn't see the lunar far side until a Soviet spacecraft flew past in 1959."*
  - *"The Moon is rotating at the same rate that it revolves around Earth (called synchronous rotation), so the same hemisphere faces Earth all the time. Some people call the far side – the hemisphere we never see from Earth – the 'dark side', but that's misleading. As the Moon orbits Earth, different parts are in sunlight or darkness at different times... And a 'new moon' occurs when the far side of the Moon has full sunlight, and the side facing us is having its night."*
  - *"The Moon makes a complete orbit around Earth in 27 Earth days and rotates or spins at that same rate, or in that same amount of time. Because Earth is moving as well – rotating on its axis as it orbits the Sun – from our perspective, the Moon appears to orbit us every 29 days."*
  - *"The solid, iron-rich inner core is 149 miles (240 kilometers) in radius. It is surrounded by a liquid iron shell 56 miles (90 kilometers) thick."*
  - *"The crust is about 25 miles (40 kilometers) thick on the Moon’s near-side hemisphere and up to about 37 miles (60 kilometers) thick on the far-side."*
  - *"The light areas of the Moon are known as the highlands. The dark features, called maria (Latin for seas), are impact basins that were filled with lava between 4.2 and 1.2 billion years ago."*
  - *"More than 105 robotic spacecraft have been launched to explore the Moon... Apollo astronauts brought back a total of 842 pounds (382 kilograms) of lunar rocks and soil to Earth."*
- **NASA Science — Tidal Locking (`https://science.nasa.gov/moon/tidal-locking/`):**
  - *"Earth’s Moon rotates, but it takes precisely as long for the Moon to spin on its axis as it does to complete its monthly orbit around Earth. As a result, the Moon never turns its back to us, like a dancer circling ― but always facing ― its partner. This phenomenon, called 'synchronous tidal locking,' sounds like a weird coincidence ― but it’s actually quite common. All the solar system’s large moons are tidally locked with their planets."*
  - *"Earth’s gravitational pull distorts the Moon into a slight football shape even today, but this distortion would have been much more dramatic when the Moon was both closer to Earth and less solid... As the Moon bent and fluxed in this tug of war, energy was released in the form of heat. As the energy dissipated, the Moon’s rotation slowed until a single spin on its axis took the same amount of time as one trip around Earth."*
- **NASA NSSDCA — Moon Fact Sheet (`https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html`):**
  - Volumetric mean radius: `1,737.4 km`; Mass: `0.07346 × 10^24 kg` (`0.0123` Earth); Sidereal orbit & rotation period: `27.3217 days` (`655.72 hours`); Synodic period: `29.53 days`; Perigee to apogee range: `357,000 km to 407,000 km`; Equatorial diurnal surface temperature range: `95 K to 390 K (~ -290 °F to +240 °F)`.

### 2.6 Verified Neighbour Pass (`≥3` Big Videos `≥1M` Views — Live Verified `2026-11-13`)

| # | Verified Views (`2026-11-13`) | Channel (Internal Note Only) | YouTube ID | Length | Title | Subject Words to Reuse (Never Channel Names) |
|---:|---:|---|---|---:|---|---|
| **1** | **4,213,040** | MinuteEarth | `6jUpX7J7ySo` | `2:01` (`121 s`) | *Tidal Locking \| Why Do We Only See One Side of the Moon?* | `why do we only see one side of the moon`, `tidal locking`, `synchronous rotation`, `moon rotation`, `tidal bulge` |
| **2** | **3,758,505** | NASA Goddard | `jdkMHkF7BaA` | `1:54` (`113 s`) | *NASA \| A View From The Other Side* | `far side of the moon`, `lunar reconnaissance orbiter`, `moon far side`, `lunar highlands`, `lunar maria` |
| **3** | **3,317,802** | Science Channel | `kJkVegBsNyE` | `4:19` (`258 s`) | *The Secret of the Dark Side of the Moon* | `dark side of the moon`, `far side of the moon`, `lunar crust`, `moon craters`, `lunar basins` |
| **4** | **2,072,539** | Conceptual Academy | `j91XTV_p9pc` | `7:59` (`478 s`) | *Earth's Moon: Why One Side Always Faces Us* | `why one side always faces us`, `earth's moon`, `tidal locking`, `moon orbit and rotation`, `27 days` |
| **5** | **1,876,903** | Cosmicus | `kfAm6unVOX4` | `25:27` (`1,527 s`) | *What Artemis II Saw On the Moon's Dark Side is Terryifing* | `far side of the moon`, `artemis`, `moon far side craters`, `lunar far side` |
| **6** | **671,786** | StarTalk | `MXpdGNh-IgM` | `12:00` (`720 s`) | *Is There Actually A Dark Side of the Moon?* | `dark side of the moon`, `new moon sunlight`, `tidal locking`, `far side of the moon` |

- **Pool Strength:** **5 verified education/science videos over `1.8M` views** (`4.21M`, `3.76M`, `3.32M`, `2.07M`, `1.88M`).

### 2.7 Two Short Angles (`LEARNINGS.md` Rules 1–8, 16, 22, 24, 31 + `OWB-2026-11-E1`)

1. **Short `S01` (`19–21 s` Single-Fact Loop Cut):**
   - **YouTube Title (`50 chars`, verified `0` exact YouTube collisions):**  
     **`Why Does the Moon Always Show Earth the Same Face?`**
   - **Frame 0 (`t = 0.0 s`) Top-Safe Hook Text (`2–3` words, `#FFE000` keyword):**  
     `ONE SINGLE FACE` (`SINGLE` in `#FFE000`, `ONE` / `FACE` in `#FFFFFF`, dark bar, `mode: "cover"` full-bleed `9:16` animated LRO Moon spin-orbit diagram, `0%` blur bars).
   - **First Spoken Sentence (`0.0–1.5 s` Surprise per Rule 24, `6 words`):**  
     *"The Moon DOES spin in space."*
   - **Mid-Short Stat Overlay (`5.5–8.5 s`, `≤4 words` per Rule 24):**  
     `27-DAY SPIN LOCK`
   - **Single Fact & Payoff (`≥70%` duration):**  
     It takes `27 Earth days` for the Moon to spin once on its axis — and `27 Earth days` to complete one orbit around the Earth. Because Earth's gravity stretched the young Moon into a slight football bulge and braked its spin until both clocks matched, the Moon turns at the exact rate it circles us — keeping its far side forever hidden from the ground (`<1.2 s` tail after final word for seamless loop).

2. **Short `S02` (`20–22 s` Single-Fact Loop Cut):**
   - **YouTube Title (`61 chars`, verified `0` exact YouTube collisions):**  
     **`Why Does the Far Side of the Moon Have Almost No Dark Plains?`**
   - **Frame 0 (`t = 0.0 s`) Top-Safe Hook Text (`2–3` words, `#FFE000` keyword):**  
     `TWO DIFFERENT MOONS` (`DIFFERENT` in `#FFE000`, full-bleed `9:16` NASA LRO side-by-side Near Side vs Far Side globe).
   - **First Spoken Sentence (`0.0–1.5 s` Surprise per Rule 24, `6 words`):**  
     *"The Moon's back looks completely wrong."*
   - **Mid-Short Stat Overlay (`5.5–8.5 s`, `≤4 words` per Rule 24):**  
     `60 KM THICK CRUST`
   - **Single Fact & Payoff (`≥70%` duration):**  
     When Soviet spacecraft **Luna 3** (`1959`) and **NASA's Lunar Reconnaissance Orbiter** photographed the hidden far side, the dark lava seas (`maria`) we see from Earth were almost completely missing. NASA gravity maps revealed why: the Moon's crust is about `25 miles (40 km)` thick on our side, so ancient asteroid impacts cracked through and flooded with dark lava — but on the far side the crust is up to `37 miles (60 km)` thick, sealing the magma underground (`<1.2 s` loop tail).
