# Rule 15 Title Audit & Rewrites — Every Non-Public Long (J2019, 4 Nov 2026)

- **Job:** `J2019` (`gemini`)
- **Rule 15 (`05_Analytics/LEARNINGS.md`, Ben, 4 Nov 2026):** Every long's title names the subject and a concrete scenario, number or stakes, fits in **≤ 50 characters**, and is never a vague *"What happened to X?"*.
- **Rule 12 (`05_Analytics/LEARNINGS.md`, 4 Nov 2026):** Thumbnail text (2–4 words) adds a concrete fact, stakes or number that the title does **not** already say.
- **Test & Compare guard:** Skip Data API title updates on any scheduled video with an armed Studio Title Test & Compare (`HOS 006 VbPubYd6Fbs` and `HOS 007 ETynHpIYLeY`).

---

## 1. Orbit With Ben — Scheduled Private Longs (`025`–`029`)

| Film | YouTube ID | Air (UTC) | Title Before J2019 | Chars | Rule 15 Check | Passing Title / Rewrite (≤ 50 chars) | Chars | Rule 12 Thumbnail Text Check | Action & Live Data API Readback |
|---|---|---|---|---:|---|---|---:|---|---|
| **OWB 025** | `Js6EQJ8qDi8` | Sun 8 Nov 18:00Z | *Could a Robot Survive on Mars?* | 30 | **PASS** — names subject (`Robot`, `Mars`) + concrete survival scenario; ≤ 50 chars | *Could a Robot Survive on Mars?* (unchanged) | 30 | **PASS** — Thumb A `BUILT FOR 90 DAYS`, B `PLANNED 5. FLEW 72`, C `MINUS 90° NIGHTS` add concrete facts not in title (`T002` thumbnail-only T&C) | Verified Private (`2026-11-08T18:00:00Z`), 30 chars |
| **OWB 026** | `c5AdqQsnnys` | Sun 15 Nov 18:00Z | *How Far Is the Nearest Star?* | 28 | **FAIL** — bare distance question with no concrete scenario, number or stakes | ***Why Reaching the Nearest Star Takes 75,000 Years*** | 48 | **PASS** — Keeps neighbour phrase `Nearest Star`, adds Voyager-speed journey scenario + `75,000 Years` (`01_Script` line 73); Thumbs A `YOU CAN'T SEE IT`, B `LIGHT TAKES 4 YEARS`, C `900M YEARS ON FOOT` add distinct facts | **Updated via Data API** (`J2019_retitle_RESULT.json`): read back `"Why Reaching the Nearest Star Takes 75,000 Years"`, Private, `2026-11-15T18:00:00Z`; updated `PACKAGE_MANIFEST.json`, `status.json`, `UPLOADS.json` |
| **OWB 027** | `6bbbvfCx6zY` | Sun 22 Nov 18:00Z | *What If Earth Stopped Spinning?* | 31 | **PASS** — names `Earth` + concrete physical scenario (`Stopped Spinning`); ≤ 50 chars | *What If Earth Stopped Spinning?* (unchanged) | 31 | **PASS** — Thumbs A `OCEANS MOVE`, B `ONE-YEAR DAYS`, C `AIR RACES ON` add concrete consequences (`T009` thumbnail-only T&C) | Verified Private (`2026-11-22T18:00:00Z`), 31 chars |
| **OWB 028** | `F-jImX5h7ws` | Sun 29 Nov 18:00Z | *What Happens When a Star Passes Through Our Solar System?* (`status.json`: *A Star Is Coming Into Our Solar System (Gliese 710)*, 51c) | 57 | **FAIL** — 57 chars (> 50-char cap) | ***What Happens When a Star Enters Our Solar System?*** | 49 | **PASS** — Names `Star` + `Solar System` entry scenario; Thumbs A `STAR VISITOR`, B `COMET NUDGE`, C `SUN'S NEIGHBOUR` (`J0894` thumbnail-only T&C) | **Updated via Data API** (`J2019_retitle_RESULT.json`): read back `"What Happens When a Star Enters Our Solar System?"`, Private, `2026-11-29T18:00:00Z`; updated `PACKAGE_MANIFEST.json`, `Titles/gliese_title_v01.txt`, `status.json`, `UPLOADS.json` |
| **OWB 029** | `vP1BbqZ_dnM` | Sun 6 Dec 18:00Z | *Is Betelgeuse About to Explode?* | 31 | **PASS** — names `Betelgeuse` + concrete supernova scenario; ≤ 50 chars | *Is Betelgeuse About to Explode?* (unchanged) | 31 | **PASS** — Thumbs A `BRIGHT AS MOON`, B `PAST MARS`, C `IT WAS DUST` add distinct facts (`T010` thumbnail-only T&C) | Verified Private (`2026-12-06T18:00:00Z`), 31 chars |

---

## 2. History of Science — Scheduled Private Longs (`006`–`007`, `099`) & Drafts (`008`–`010`, `013`)

| Film | YouTube ID / Status | Air (UTC) | Title / Variants Before J2019 | Chars | Rule 15 Check | Passing Title / Rewrite (≤ 50 chars) | Chars | Rule 12 & Neighbour Phrase Check | Action |
|---|---|---|---|---:|---|---|---:|---|---|
| **HOS 006** | `VbPubYd6Fbs` (Scheduled Private) | Thu 5 Nov 18:00Z | A: *The Willow Tree That Was Made of Air*<br>B: *Where Does a Tree's Weight Come From?* | 36<br>37 | **PASS (A & B)** — both name `Tree` + concrete claim/weight mystery; ≤ 50 chars | A: *The Willow Tree That Was Made of Air*<br>B: *Where Does a Tree's Weight Come From?* | 36<br>37 | **PASS** — Holds neighbour phrase `tree`; covers `WOOD / FROM / SKY?` and `DO PLANTS / EAT / SOIL?` add distinct hooks | **Skipped Data API write** (Studio Title & Thumbnail A/B Test & Compare armed in `J0958`) |
| **HOS 007** | `ETynHpIYLeY` (Scheduled Private) | Thu 12 Nov 18:00Z | A: *Why Vaccines Are Named After a Cow*<br>B: *How Was the First Vaccine Made?* | 34<br>31 | **A: PASS** (concrete cow/vaccine hook, 34c)<br>**B: FAIL** (bare "How was X made?" without concrete scenario/stakes) | A: *Why Vaccines Are Named After a Cow*<br>B rewrite (if re-armed): ***How Cowpox Made the First Smallpox Vaccine*** | 34<br>42 | **PASS** — Holds neighbour phrase `vaccines`; cover A `THE / MILKMAID'S / SECRET` adds distinct hook | **Skipped Data API write** (Studio Title & Thumbnail A/B Test & Compare armed in `J0959`) |
| **HOS 008** | Draft (`008_Lightning-Franklin`) | Thu 19 Nov 18:00Z (planned) | A: *Why Did Franklin Fly a Kite in a Storm?*<br>B: *How Does a Lightning Rod Work?* | 39<br>30 | **A: PASS** (names `Franklin`, `Kite`, `Storm`, 39c)<br>**B: FAIL** (textbook mechanism question with no concrete scenario/stakes) | A: *Why Did Franklin Fly a Kite in a Storm?*<br>B: ***How a Pointed Iron Rod Tamed Lightning*** | 39<br>38 | **PASS** — A holds `franklin`/`kite`, B holds `lightning` (`neighbours.phrases`) | Updated `titleAbc[1]` in `008` `PACKAGE_MANIFEST.json` & `LAUNCH_PLAN.md` (`lint:package` PASS) |
| **HOS 009** | Draft (`009_The-Falling-Moon-Gravity`) | Thu 26 Nov 18:00Z (planned) | A: *Why Doesn't the Moon Fall to Earth?*<br>B: *The Moon Is Falling Right Now* | 35<br>29 | **PASS (A & B)** — both name `Moon` + concrete falling/orbit scenario; ≤ 50 chars | A: *Why Doesn't the Moon Fall to Earth?*<br>B: *The Moon Is Falling Right Now* | 35<br>29 | **PASS** — Both hold neighbour phrase `moon` | No change needed (`lint:package` PASS) |
| **HOS 010** | Draft (`010_Alvarez-Clay-Line-Dinosaurs`) | Thu 3 Dec 18:00Z (planned) | A: *What Killed the Dinosaurs Was Hidden in a Line of Clay*<br>B: *How a 1-Centimetre Line of Clay Solved What Killed the Dinosaurs* | 54<br>64 | **FAIL (A & B)** — 54 and 64 chars both exceed 50-char cap | A: ***What Killed the Dinosaurs Was in a Line of Clay***<br>B: ***How a 1-cm Line of Clay Explained the Dinosaurs*** | 47<br>47 | **PASS** — Both hold neighbour phrase `dinosaurs`; cover text `300× TOO MUCH` adds iridium anomaly number not in title | Updated `010` `PACKAGE_MANIFEST.json`, `LAUNCH_PLAN.md`, and `PIPELINE.json` (`lint:package` PASS with 0 warnings) |
| **HOS 013** | Draft (`013_Darwin-Wallace-Evolution`) | TBD (VO locked) | A: *Evolution: The Letter That Forced Darwin to Publish*<br>B: *Why Darwin Kept Natural Selection Secret for 20 Years*<br>C: *How a Letter From the Jungle Forced Darwin to Publish* | 51<br>53<br>53 | **FAIL (A, B, C)** — 51, 53, 53 chars exceed 50-char cap | A: ***The Letter That Forced Darwin to Publish Evolution***<br>B: ***Why Darwin Kept Evolution Secret for 20 Years***<br>C: ***How a Jungle Letter Forced Darwin to Publish*** | 50<br>45<br>44 | **PASS** — Holds neighbour phrases `evolution` and `darwin` + concrete 1858 letter / 20-year secret scenario | Updated `013` `PRE_BUILD_VIDIQ_AUDIT.md` |
| **HOS 099** | `uAomPaOBrM8` (Compilation, Private) | Thu 10 Dec 18:00Z | *How Did Experiments Explain Blood, Germs and Atoms?* | 51 | **FAIL** — 51 chars (> 50-char cap); also note `LEARNINGS.md` Rule 9 on compilations and active `J0999` readback lock | ***How Six Experiments Proved Germs, Blood and Atoms*** | 49 | **PASS** — Names `Six Experiments` + `Germs, Blood and Atoms` | **Skipped Data API write** (`J0999` requires unchanged title/privacy/publishAt during Studio readback; Rule 9 also retires compilations) |

---

## 3. Orbit With Ben — Later Long Drafts (`030`–`061`)

All 32 draft long projects in `02_Video-Projects/030_*` through `061_*` were audited against Rule 15 (`≤ 50` chars, names subject + concrete scenario/number/stakes). The 19 `status.json` files that carried `> 50`-char titles (`033`, `044`–`061`) were updated in `status.json` to their `≤ 50`-char Rule 15 rewrites.

| Film | Draft Title Before J2019 | Chars | Rule 15 Check | Passing Title / Rewrite (≤ 50 chars) | Chars |
|---|---|---:|---|---|---:|
| **030** | *The Asteroid That Will Fly Closer Than Our Satellites* | 53 | **FAIL** (53c > 50c; omits `Apophis`; duplicates 2 public titles) | ***Why Asteroid Apophis Passes Under Our Satellites*** | 48 |
| **031** | *What Happens When Earth's Magnetic Field Flips?* | 47 | **PASS** | *What Happens When Earth's Magnetic Field Flips?* | 47 |
| **032** | *What Would Happen If You Landed on Titan?* | 41 | **PASS** | *What Would Happen If You Landed on Titan?* | 41 |
| **033** | *Why Uranus Has 21-Year Winters After Being Knocked Sideways* | 59 | **FAIL** (59c > 50c) | ***Why Knocked-Sideways Uranus Has 21-Year Winters*** | 47 |
| **034** | *Why Pluto's Frozen Heart Has Zero Craters* | 41 | **PASS** | *Why Pluto's Frozen Heart Has Zero Craters* | 41 |
| **035** | *Why Neptune's Largest Moon Orbits Backwards* | 43 | **PASS** | *Why Neptune's Largest Moon Orbits Backwards* | 43 |
| **036** | *Why Is There Ice on Mercury, the Planet Closest to the Sun?* | 59 | **FAIL** (59c > 50c) | ***Why Sun-Scorched Mercury Has Craters Full of Ice*** | 48 |
| **037** | *What Lies Hiding at the Centre of the Milky Way?* | 48 | **FAIL** (vague "What lies hiding" without concrete scenario/number) | ***What 4-Million-Sun Monster Rules the Milky Way?*** | 47 |
| **038** | *Why Will Voyager 1 and the Golden Record Outlive the Earth?* | 59 | **FAIL** (59c > 50c) | ***Why Voyager 1's Golden Record Outlives the Earth*** | 48 |
| **039** | *Why Do Mars and the Other Planets Sound So Strange?* | 51 | **FAIL** (51c > 50c) | ***Why Do Mars and Other Worlds Sound So Strange?*** | 46 |
| **040** | *Why Are We Looking for the Wrong Kind of Aliens on Titan and Europa?* | 68 | **FAIL** (68c > 50c) | ***Are We Looking for the Wrong Life on Titan?*** | 43 |
| **041** | *Why Does Jupiter's Moon Io Have 400 Active Volcanoes?* | 53 | **FAIL** (53c > 50c) | ***Why Jupiter's Moon Io Has 400 Active Volcanoes*** | 46 |
| **042** | *What Happens When the Sun Becomes a Red Giant?* | 46 | **PASS** | *What Happens When the Sun Becomes a Red Giant?* | 46 |
| **043** | *Why the 330-Million-Light-Year Boötes Void Is Almost Empty* | 58 | **FAIL** (58c > 50c) | ***Why the 330M-Light-Year Boötes Void Is So Empty*** | 47 |
| **044** | *Why Is Jupiter's Moon Ganymede Bigger Than the Planet Mercury?* | 62 | **FAIL** (62c > 50c) | ***Why Jupiter's Moon Ganymede Is Bigger Than Mercury*** | 50 |
| **045** | *Can We Actually Terraform Mars, and Why Does Even a Robot Need Help?* | 68 | **FAIL** (68c > 50c) | ***Why Terraforming Mars Fails Without a New Sky*** | 45 |
| **046** | *Why Saturn's Moon Enceladus Shoots Geysers Into Space* | 53 | **FAIL** (53c > 50c) | ***Why Saturn's Moon Enceladus Shoots Ice Into Space*** | 49 |
| **047** | *Why Jupiter's Great Red Spot Is Shrinking After 300 Years* | 57 | **FAIL** (57c > 50c) | ***Why Jupiter's 300-Year Great Red Spot Is Shrinking*** | 50 |
| **048** | *Why Dwarf Planet Ceres Has Glowing Salt Domes in the Asteroid Belt* | 66 | **FAIL** (66c > 50c) | ***Why Dwarf Planet Ceres Has Glowing Salt Domes*** | 45 |
| **049** | *Why Did NASA Bring Back a Sample of Asteroid Bennu?* | 51 | **FAIL** (51c > 50c) | ***Why NASA Brought Back a Sample of Asteroid Bennu*** | 48 |
| **050** | *Why Saturn's Moon Iapetus Is Half Black and Half White* | 54 | **FAIL** (54c > 50c) | ***Why Saturn's Moon Iapetus Is Half Black and White*** | 49 |
| **051** | *Why NASA's DART Spacecraft Changed an Asteroid's Orbit by 33 Minutes* | 68 | **FAIL** (68c > 50c) | ***How NASA's DART Cut an Asteroid's Orbit by 33 Mins*** | 50 |
| **052** | *Why Uranus's Moon Miranda Has a 12-Mile-High Ice Cliff* | 54 | **FAIL** (54c > 50c) | ***Why Uranus's Moon Miranda Has a 20-km Ice Cliff*** | 47 |
| **053** | *Why NASA's Parker Solar Probe Flew Inside the Sun's Corona without Melting* | 74 | **FAIL** (74c > 50c) | ***How Parker Solar Probe Flew Inside the Sun's Crown*** | 50 |
| **054** | *Are We Living Inside a Simulation? What Physics Actually Says* | 61 | **FAIL** (61c > 50c) | ***Why Physics Says We Don't Live in a Simulation*** | 46 |
| **055** | *What Will Humans Become in 1,000 Years? What Spaceflight Does to the Human Body* | 79 | **FAIL** (79c > 50c) | ***How Spaceflight Reshapes Humans Over 1,000 Years*** | 48 |
| **056** | *Could AI Help Humanity Reach the Stars? How Autonomous Probes Explore Deep Space* | 80 | **FAIL** (80c > 50c) | ***How Autonomous AI Probes Could Reach the Stars*** | 46 |
| **057** | *Why Jupiter's Moon Callisto Is the Most Heavily Cratered World in the Solar System* | 82 | **FAIL** (82c > 50c) | ***How Cratered Moon Callisto Hides a Deep Ocean*** | 45 |
| **058** | *What Is the Most Dangerous Place in the Universe? Inside a Magnetar and Quasar Jet* | 82 | **FAIL** (82c > 50c) | ***Inside a Magnetar: Universe's Deadliest Place*** | 45 |
| **059** | *Why Mars Built a Volcano Three Times Taller Than Mount Everest: Olympus Mons* | 76 | **FAIL** (76c > 50c) | ***Why Mars Built Olympus Mons 3× Taller Than Everest*** | 50 |
| **060** | *Why Saturn's Moon Hyperion Looks Like a Giant Tumbling Space Sponge* | 67 | **FAIL** (67c > 50c) | ***Why Saturn's Moon Hyperion Looks Like a Sponge*** | 46 |
| **061** | *Why Venus Spins Backwards and Its Day Is Longer Than Its Year* | 61 | **FAIL** (61c > 50c) | ***Why a Day on Venus Is Longer Than Its Year*** | 42 |
