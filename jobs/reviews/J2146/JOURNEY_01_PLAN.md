# OWB Journey Film 01 (`J01`) — Production Plan & Linking Script (`023–030`)

- **Job**: `J2146` (`Journey film 01: plan and linking script from 023-030 (LEARNINGS rule 21)`)
- **Film ID**: `J01` (`02_Video-Projects/J01_Journey-To-Every-World`)
- **Rule Reference**: `05_Analytics/LEARNINGS.md` Rule 21 (test; Ben's go 4 Nov 2026) — one monthly **40–60 min** calm long stitched from our finished OWB longs (`023–030`) into one continuous story, with new linking VO lines, chapter cards, and one ambient bed plan. Built from longs, never a Shorts compilation (Rule 9).
- **WIP Slot Rule**: Enters `jobs/WIP.json` (`OWB:J01` at the front of `next`) and takes the next active WIP slot when `031` or `032` reaches Ben's watch.
- **Target Runtime**: **55 min 49.10 s** (`3,349.10 s`) — `52 min 45.10 s` reused from locked master cuts `023–029` + `3 min 04.00 s` of new linking material (Cold Open, 7 Chapter Cards, 6 Outward Bridges with animated distance-scale graphics, Closing, and 18 s end-screen hold).

---

## 1. Running Order & Exact Reused Cut Windows (`023–030`)

### 1.1 Narrative Spine: Outward From the Ground Under Your Feet to the Stars That Made Us

Rather than a random playlist, the seven finished longs from the `023–030` block arrange into a single outward journey measured in distance from Earth:

1. **Part 1 — `0 km` (Earth's Surface & Spin — `027`)**: Starts where the viewer is sitting right now—moving east at `1,000 km/h` in Britain (`1,670 km/h` at the equator), how the Moon's tides slow our day by `1.8 milliseconds` a century, and why every sunrise is a `4.5-billion-year-old` push still running down.
2. **Part 2 — `40 Million km` (The Twin That Lost Its Water — `023` Venus)**: Steps outward to our nearest planetary neighbour (`95%` of Earth's width), where the same budget of carbon sits in a `92-bar`, `464 °C` sky instead of limestone rock, and Soviet lander *Venera 13* lasted `127 minutes`.
3. **Part 3 — `225 Million km` (The Red World Full of Robots — `025` Mars)**: Steps outward to the next rocky world—`6 millibars` of air, `−60 °C` cold, and the machines (*Spirit*, *Opportunity* for `14+ years`, *Curiosity*, *Ingenuity*'s `72 flights`) that kept working until the dust covered their solar panels.
4. **Part 4 — `10,000 to 100,000 AU` (The Outer Edge & the Passing Star — `028` Gliese 710)**: Crosses past all eight planets into the frozen Oort Cloud, where orange dwarf *Gliese 710* will sail `13,000 AU` from the Sun in `1.3 million years` and send a slow shower of comets inward.
5. **Part 5 — `4.24 Light-Years` (Across the Gap to the Nearest Star — `026` Proxima Centauri)**: Leaves the Solar System behind across the four-light-year dark—where shrinking the Sun to a grapefruit in London puts the nearest star as a cherry beyond Cairo, and *Voyager 1*'s `17 km/s` speed takes `75,000 years`.
6. **Part 6 — `22 Crew Years / 100,000 Earth Years` (The Clock That Slows Near Light Speed — `024` Light Speed)**: Asks what happens to time itself when a spacecraft tries to cross those light-years fast—how `99%` of light speed slows your shipboard clock sevenfold, and how a `1 g` ship could cross the `100,000-light-year` Milky Way in `22 crew years` while `100,000 years` pass on Earth.
7. **Part 7 — `600 Light-Years` (The Dying Giant That Made Us — `029` Betelgeuse)**: Arrives at Orion's red supergiant shoulder—how a star `764 times` wider than the Sun fuses its core to iron in days, explodes as bright as a half-Moon in daylight, and scatters the oxygen and calcium that built the rocky worlds where our journey began.

> **Status of `030` (*Apophis — Closer Than Our Satellites*)**: `030` has a locked long script (`02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/01_Script/apophis_script_master_v02.md`), while its completed production to date is the standalone Short cohort (`gJwNJN_yMKU` / `J1772`); there is no rendered long master cut on the NAS. Because the seven finished longs `023–029` already provide **52 min 45.10 s** of locked body footage (**55 min 49.10 s** total film length), `J01` is complete at 7 parts without blocking on a `030` long render. If a `030` long master is ever cut before `J01` enters assembly, it slots naturally between Part 1 (`027` Earth's Spin) and Part 2 (`023` Venus) at the `32,000 km` geostationary ring.

---

### 1.2 Verified NAS Master Files & SHA-256 Checksums (`023–029`)

Every source master below was verified on `/Volumes/data/mac-mini-archive` via `ffprobe` (`1920x1080`, `24 fps` CFR, `h264`, stereo `aac` `48 kHz`):

| Part | Film | YouTube ID | Verified NAS Master Path | Master Duration | SHA-256 |
|---|---|---|---|---|---|
| **1** | `027` *What If Earth Stopped Spinning?* | `6bbbvfCx6zY` | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/027_EarthSpin_rough_v01m.mp4` | `446.30 s` (`7:26.30`) | `499e8edc06910cb646006a260fccbbbd9b9bc9e975f39940b0cbec2fc457b31d` |
| **2** | `023` *What Happened to Venus?* | `VBaYRPp85Sw` | `/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-13/loose_renders/023_Venus_full_rough_v05e.mp4` | `513.00 s` (`8:33.00`) | `5d8a8f73454f889a38590661885a21702690a42c8ebfd940868d033f0174e6fc` |
| **3** | `025` *Could a Robot Survive on Mars?* | `Js6EQJ8qDi8` | `/Volumes/data/mac-mini-archive/youtube-staging/025/025_MarsRobot_full_rough_v03f.mp4` | `490.20 s` (`8:10.20`) | `cce6268cbd571f1f404ee98b86e089bbe3cabed15017113bd9559951ee36e09f` |
| **4** | `028` *What Happens When a Star Enters Our Solar System?* | `F-jImX5h7ws` | `/Volumes/data/mac-mini-archive/youtube-staging/028/028_Gliese710_full_master_v03.mp4` | `497.83 s` (`8:17.83`) | `a9780e548a2775f4e7a1acecb6ac24308927f0b58ab1d606e67d27741e3db824` |
| **5** | `026` *Why Reaching the Nearest Star Takes 75,000 Years* | `c5AdqQsnnys` | `/Volumes/data/mac-mini-archive/youtube-staging/026/026_NearestStar_v06_cfr18.mp4` | `494.53 s` (`8:14.53`) | `6e587bb5ac33552cef55ac897d89f5516a90acef9473155254dd313fc73e09d3` |
| **6** | `024` *What Happens If You Travel Near Light Speed?* | `rVqgtkBV3jc` | `/Volumes/data/mac-mini-archive/youtube-staging/024/024_LightSpeed_v06.mp4` | `491.05 s` (`8:11.05`) | `8d0b131771c1e6bfc8b33f49f5c628e96ae3db3af7a890864f2239960a5bde02` |
| **7** | `029` *Is Betelgeuse About to Explode?* | `vP1BbqZ_dnM` | `/Volumes/data/mac-mini-archive/youtube-staging/029/029_Betelgeuse_full_rough_v03b.mp4` | `542.23 s` (`9:02.23`) | `54e04d3bfcb42bcf9066a0613254f10c978435b148d158468711e25908060c93` |

---

### 1.3 Exact Slice Windows & Cumulative Timeline (`55 min 49.10 s`)

To obey **AGENTS.md Never List** (*"Never more than one subscribe beat in a long, and never at the end"*) and **LEARNINGS Rule 10** (*"No agenda lines in the opening... don't spend 0:20–0:40 on 'In this film, I will show you three things'"*), each film's slice trims out:
1. Its standalone `"In this film, I will show you..."` agenda sentence (at `~0:22–0:42` of `023`, `024`, `025`, `026`, `028`, `029`), keeping the concrete opening hook and joining smoothly via a `0.5 s` crossfade into Chapter 1;
2. The duplicate mid-film `"We make one of these every week. Subscribing is how the next one finds you."` beat in Parts 2–7 (**keeping only Part 1 `027`'s subscribe beat at `03:35.90` of the Journey Film**); and
3. The standalone `"Next week: ..."` outro teaser at the tail of `023`, `024`, and `025`, cutting after the final substantive sentence + `0.8 s` breath.

| Timeline (`MM:SS.ss`) | Segment | Source / Reused Slice (`in` → `out` in source master) | Slice Duration | What Is Kept / Trimmed |
|---|---|---|---|---|
| `00:00.00 – 00:48.00` | **Cold Open** | **NEW** (`j01_vo_01_intro.mp3` + graded NASA plates + `code_graphic_J01_map_00_solar_to_stars.mp4`) | `48.00 s` (`0:48.00`) | Line-1 physical claim (`4 light-hours` vs `4.24 light-years`), concrete facts in first 15 s (Rule 10), no agenda line. |
| `00:48.00 – 00:51.00` | **Chapter Card 1** | **NEW** (`PART ONE — THE GROUND MOVING UNDER YOUR FEET`) | `3.00 s` (`0:03.00`) | Didot/clean house card + `tick_ink` (`0.5 s` xfade). |
| `00:51.00 – 08:14.50` | **Part 1: `027` Earth's Spin** | `027_EarthSpin_rough_v01m.mp4` **`0:00.00 → 7:23.50`** (`0.00–443.50 s`) | `443.50 s` (`7:23.50`) | Full `027` cut (v02 order, no agenda line). **Keeps the Journey Film's single `[SUBSCRIBE BEAT]` at `2:44.90–2:49.42` (`03:35.90` film time)**. Ends after *"Every sunrise you have ever seen is that first push still running down."* (`442.82 s` + `0.68 s` breath). |
| `08:14.50 – 08:30.50` | **Bridge 1 (`0 km → 40M km`)** | **NEW** (`j01_vo_02_bridge1_venus.mp3` + `code_graphic_J01_map_01_venus.mp4`) | `16.00 s` (`0:16.00`) | Connects Earth's `24-hour` spin & ocean carbon cycle to Venus (`243 Earth days` retrograde spin, `40M km` at closest approach). |
| `08:30.50 – 08:33.50` | **Chapter Card 2** | **NEW** (`PART TWO — THE TWIN THAT LOST ITS WATER`) | `3.00 s` (`0:03.00`) | House chapter card + `tick_ink`. |
| `08:33.50 – 16:28.10` | **Part 2: `023` Venus** | `023_Venus_full_rough_v05e.mp4`:<br>• **2A**: `0:00.00 → 0:35.80` (`35.80 s`)<br>• **2B**: `0:43.20 → 3:32.20` (`169.00 s`)<br>• **2C**: `3:38.20 → 8:24.80` (`266.60 s`)<br>*(+ two `1.60 s` visual bridges = `474.60 s`)* | `474.60 s` (`7:54.60`) | Trims `0:36.32–0:42.74` agenda line (*"In this film, I will show you..."*), trims duplicate `3:32.74–3:37.50` subscribe beat, and trims `8:25.82–8:29.50` *"Next week, what happens to your clock..."* teaser. Ends after *"How close did Earth come to the same turn?"* (`504.48 s`). |
| `16:28.10 – 16:44.10` | **Bridge 2 (`40M km → 225M km`)** | **NEW** (`j01_vo_03_bridge2_mars.mp3` + `code_graphic_J01_map_02_mars.mp4`) | `16.00 s` (`0:16.00`) | Contrasts *Venera 13*'s `127 minutes` under `92 bar` with going the other way from the Sun to Mars (`225M km` mean distance, `6 mbar`), where machines last for years. |
| `16:44.10 – 16:47.10` | **Chapter Card 3** | **NEW** (`PART THREE — THE RED WORLD FULL OF QUIET MACHINES`) | `3.00 s` (`0:03.00`) | House chapter card + `tick_ink`. |
| `16:47.10 – 24:12.80` | **Part 3: `025` Mars** | `025_MarsRobot_full_rough_v03f.mp4`:<br>• **3A**: `0:00.00 → 0:29.80` (`29.80 s`)<br>• **3B**: `0:40.80 → 3:44.50` (`183.70 s`)<br>• **3C**: `3:51.00 → 8:03.20` (`252.20 s`) | `445.70 s` (`7:25.70`) | Trims `0:30.32–0:40.50` agenda line, trims duplicate `3:45.06–3:50.22` subscribe beat, and trims `8:03.80–8:06.70` *"Next week, how far is the nearest star?"* teaser. Ends after *"and the dust slowly covers it."* (`482.86 s`). |
| `24:12.80 – 24:29.80` | **Bridge 3 (`225M km → 13,000 AU`)** | **NEW** (`j01_vo_04_bridge3_oort.mp3` + `code_graphic_J01_map_03_oort.mp4`) | `17.00 s` (`0:17.00`) | Moves past Mars and the giant planets to the Sun's outer shell (`10,000–100,000 AU`), where *Gliese 710* is heading straight toward our Oort Cloud. |
| `24:29.80 – 24:32.80` | **Chapter Card 4** | **NEW** (`PART FOUR — THE STAR HEADING FOR OUR OUTER EDGE`) | `3.00 s` (`0:03.00`) | House chapter card + `tick_ink`. |
| `24:32.80 – 31:45.60` | **Part 4: `028` Gliese 710** | `028_Gliese710_full_master_v03.mp4`:<br>• **4A**: `0:00.00 → 0:30.80` (`30.80 s`)<br>• **4B**: `0:42.20 → 3:24.20` (`162.00 s`)<br>• **4C**: `3:29.80 → 7:49.80` (`260.00 s`) | `432.80 s` (`7:12.80`) | Trims `0:31.30–0:41.92` agenda line, trims duplicate `3:24.66–3:29.44` subscribe beat, and trims excess silent end hold after `469.34 s` (*"Some of the ice falling in from the dark may have started out around another sun."*). |
| `31:45.60 – 32:01.60` | **Bridge 4 (`13,000 AU → 4.24 ly`)** | **NEW** (`j01_vo_05_bridge4_proxima.mp3` + `code_graphic_J01_map_04_proxima.mp4`) | `16.00 s` (`0:16.00`) | Steps from the Oort Cloud (`~0.2 light-years` where *Gliese 710* passes) across the `4.24-light-year` gulf to our true nearest stellar neighbour right now, *Proxima Centauri*. |
| `32:01.60 – 32:04.60` | **Chapter Card 5** | **NEW** (`PART FIVE — FOUR LIGHT-YEARS THROUGH THE DARK`) | `3.00 s` (`0:03.00`) | House chapter card + `tick_ink`. |
| `32:04.60 – 39:36.00` | **Part 5: `026` Nearest Star** | `026_NearestStar_v06_cfr18.mp4`:<br>• **5A**: `0:00.00 → 0:20.50` (`20.50 s`)<br>• **5B**: `0:32.80 → 3:44.40` (`191.60 s`)<br>• **5C**: `3:52.00 → 8:11.30` (`259.30 s`)<br>*(trimmed `451.40 s`)* | `451.40 s` (`7:31.40`) | Trims `0:20.88–0:32.50` agenda line and duplicate `3:44.94–3:51.08` subscribe beat. Ends after *"and we have only just begun to measure the gap."* (`490.96 s`). |
| `39:36.00 – 39:53.00` | **Bridge 5 (`75,000 Years → 0.99c`)** | **NEW** (`j01_vo_06_bridge5_lightspeed.mp3` + `code_graphic_J01_map_05_lightspeed.mp4`) | `17.00 s` (`0:17.00`) | Connects `026`'s `75,000-year` *Voyager 1* crossing to `024`: what happens to your shipboard clock if you push toward the speed of light to cross those light-years in a human lifetime? |
| `39:53.00 – 39:56.00` | **Chapter Card 6** | **NEW** (`PART SIX — WHEN YOUR CLOCK SLOWS DOWN`) | `3.00 s` (`0:03.00`) | House chapter card + `tick_ink`. |
| `39:56.00 – 47:18.80` | **Part 6: `024` Light Speed** | `024_LightSpeed_v06.mp4`:<br>• **6A**: `0:00.00 → 0:28.30` (`28.30 s`)<br>• **6B**: `0:41.60 → 3:33.10` (`171.50 s`)<br>• **6C**: `3:40.00 → 8:03.00` (`263.00 s`)<br>*(trimmed `442.80 s`)* | `442.80 s` (`7:22.80`) | Trims `0:28.72–0:41.38` agenda line, duplicate `3:33.64–3:39.02` subscribe beat, and `8:04.44–8:07.54` *"Next week, could a robot survive on Mars?"* teaser. Ends after *"where you would choose to land if you knew home would not be waiting."* (`482.52 s`). |
| `47:18.80 – 47:35.80` | **Bridge 6 (`0.99c → 600 ly`)** | **NEW** (`j01_vo_07_bridge6_betelgeuse.mp3` + `code_graphic_J01_map_06_betelgeuse.mp4`) | `17.00 s` (`0:17.00`) | Uses light's own travel time (`600 years` across the dark) to look out at Orion's red supergiant shoulder—a dying star whose core Forged the atoms of the rocky planets we just visited. |
| `47:35.80 – 47:38.80` | **Chapter Card 7** | **NEW** (`PART SEVEN — THE DYING GIANT THAT MADE US`) | `3.00 s` (`0:03.00`) | House chapter card + `tick_ink`. |
| `47:38.80 – 55:33.10` | **Part 7: `029` Betelgeuse** | `029_Betelgeuse_full_rough_v03b.mp4`:<br>• **7A**: `0:00.00 → 0:22.10` (`22.10 s`)<br>• **7B**: `0:37.20 → 4:02.20` (`205.00 s`)<br>• **7C**: `4:07.60 → 8:34.80` (`267.20 s`)<br>*(trimmed `474.30 s`)* | `474.30 s` (`7:54.30`) | Trims `0:22.58–0:36.96` agenda line, duplicate `4:02.70–4:07.18` subscribe beat, and excess silent tail after `514.26 s` (*"We are made of stars that lived and died before the Sun was born."*). |
| `55:33.10 – 55:49.10` | **Closing + End Hold** | **NEW** (`j01_vo_08_closing.mp3` `~16 s` + `18 s` picture/music end-screen hold overlapped) | `16.00 s` VO + `18.00 s` hold | Brings the `600-light-year` journey back to the spinning Earth under our feet; holds music and picture past the last word for YouTube end screens (`55:49.10` total). |

---

## 2. New Linking VO Script (`Cold Open`, `Bridges 1–6`, `7 Chapter Cards`, `Closing`)

All new linking VO lines use **Ben Orbit Narrator** (`kDch6ACCIpqgQ0NsU9kk`, `eleven_v3`, British English, `130–145 wpm`), recorded via `04_Audio/tools/vo_take.py`. Every number in the linking script is already verified in the locked `SOURCES.md` files of `023–029` (see Section 2.3).

### 2.1 Full Linking Script (`~392 spoken words`, `8 takes`)

```markdown
# Journey Film 01 — Linking Script (`J01`)

## Take 1 — Cold Open (`j01_vo_01_intro.mp3`, target ~48.0 s, 114 words)
[VISUAL MUST: Real Cassini Pale Blue Dot / DSCOVR full-disk Earth rotating in dark space; lower-left label "EARTH · 1,670 KM/H EQUATOR" · WHEN: Present Day]
[SFX: rumble_low — deep planetary sub-bass hum at -24 LUFS]
Every machine humanity has ever landed on another world sits inside a bubble of light less than two light-hours across—while the nearest star beyond our Sun is four point two four light-years away.

[VISUAL MUST: Split-frame real spacecraft surface panoramas: Venera 13 basalt slabs on Venus (464 °C) and Curiosity's Gale Crater ridges on Mars (−60 °C) · FACT: Two worlds, 520 °C apart]
Inside that small neighbourhood, we have set cameras down on a scorching twin where lead melts on the ground, and on a frozen red desert where nuclear rovers drive for years through the dust.

[VISUAL MUST: Animated outward logarithmic distance map (`code_graphic_J01_map_00_solar_to_stars.mp4`) drawing from Earth (0 km) -> Venus (40M km) -> Mars (225M km) -> Oort Cloud (13,000 AU) -> Proxima Centauri (4.24 ly) -> Betelgeuse (600 ly) · DATA: Outward journey scale from 0 km to 600 light-years · SCALE: Light takes 8 minutes from the Sun, 4.24 years from the nearest star]
[SFX: tick_ink — soft tick as each distance marker drops in]
This is one continuous journey outward from the ground moving under your feet—past the worlds our landers have touched, through the comet cloud at the edge of the Sun's reach, and out to the giant stars that forged the atoms in your hands.

It begins right where you are sitting.

[CHAPTER CARD 1: PART ONE — THE GROUND MOVING UNDER YOUR FEET · 0 KM]
[SFX: tick_ink]
```

*(→ Cuts into **Part 1: `027` What If Earth Stopped Spinning?**, `0:00.00 – 7:23.50`, ending on: "Every sunrise you have ever seen is that first push still running down.")*

```markdown
## Take 2 — Bridge 1: Earth to Venus (`j01_vo_02_bridge1_venus.mp3`, target ~16.0 s, 43 words)
[VISUAL MUST: Animated outward map (`code_graphic_J01_map_01_venus.mp4`) stepping from Earth (0 km, 24 h day) inward to Venus's orbit (40 million km closest approach, 243-Earth-day retrograde day) · DATA: Earth to Venus distance (40 million km) and spin (24 h vs 243 days) · SCALE: 95% as wide as Earth]
[SFX: whoosh_soft — gentle camera drift across the inner Solar System]
Earth's twenty-four-hour spin and liquid oceans kept its carbon locked safely in stone beneath the sea.

Step forty million kilometres inward to our closest planetary neighbour, where a single day lasts two hundred and forty-three Earth days—and that same carbon escaped into the sky.

[CHAPTER CARD 2: PART TWO — THE TWIN THAT LOST ITS WATER · 40 MILLION KM]
[SFX: tick_ink]
```

*(→ Cuts into **Part 2: `023` What Happened to Venus?**, slices `2A + 2B + 2C`, ending on: "How close did Earth come to the same turn?")*

```markdown
## Take 3 — Bridge 2: Venus to Mars (`j01_vo_03_bridge2_mars.mp3`, target ~16.0 s, 44 words)
[VISUAL MUST: Animated outward map (`code_graphic_J01_map_02_mars.mp4`) stepping outward past Earth to Mars (225 million km average distance; pressure gauge dropping from 92 bar on Venus to 0.006 bar on Mars) · DATA: Surface pressure comparison — Venus 92 bar vs Mars 0.006 bar · SCALE: 127 minutes on Venus vs 14 years on Mars]
[SFX: tick_ink — gauge needle drops from 92 bar to 6 mbar]
On Venus, ninety-two bars of crushing heat silenced our toughest lander in just over two hours.

Head the other way from the Sun—two hundred and twenty-five million kilometres out to Mars—and the problem flips: an air so thin and cold that our robots can roam for over a decade.

[CHAPTER CARD 3: PART THREE — THE RED WORLD FULL OF QUIET MACHINES · 225 MILLION KM]
[SFX: tick_ink]
```

*(→ Cuts into **Part 3: `025` Could a Robot Survive on Mars?**, slices `3A + 3B + 3C`, ending on: "Every robot that stops on Mars stays exactly where it stopped, and the dust slowly covers it.")*

```markdown
## Take 4 — Bridge 3: Mars to the Oort Cloud (`j01_vo_04_bridge3_oort.mp3`, target ~17.0 s, 46 words)
[VISUAL MUST: Animated outward map (`code_graphic_J01_map_03_oort.mp4`) zooming out past Mars and Neptune (30 AU) into the spherical Oort Cloud shell (10,000 to 100,000 AU) with Gliese 710's orange track · DATA: Mars (1.5 AU) to the Oort Cloud (13,000 AU closest approach of Gliese 710) · SCALE: 1 AU is Earth-to-Sun; 13,000 AU is 400 times past Neptune]
[SFX: whoosh_soft — deep pull-back past the planetary orbits into the dark Oort Cloud]
Beyond the rusty plains of Mars and the giant planets, the Sun's gravity still holds a vast shell of frozen comets ten thousand to a hundred thousand times further out than Earth.

And out there in the dark, another star is already heading our way.

[CHAPTER CARD 4: PART FOUR — THE STAR HEADING FOR OUR OUTER EDGE · 13,000 AU]
[SFX: tick_ink]
```

*(→ Cuts into **Part 4: `028` What Happens When a Star Enters Our Solar System?**, slices `4A + 4B + 4C`, ending on: "Some of the ice falling in from the dark may have started out around another sun.")*

```markdown
## Take 5 — Bridge 4: The Oort Cloud to Proxima Centauri (`j01_vo_05_bridge4_proxima.mp3`, target ~16.0 s, 44 words)
[VISUAL MUST: Animated outward map (`code_graphic_J01_map_04_proxima.mp4`) stepping from Gliese 710's future 13,000 AU (~0.2 ly) pass out to Proxima Centauri at 4.24 light-years (40 trillion km) · DATA: Oort Cloud (0.2 ly) to Proxima Centauri (4.24 ly / 40 trillion km) · SCALE: 75,000 years at Voyager 1's 17 km/s speed]
[SFX: tick_ink]
Gliese seven-ten will not reach our comet cloud for another one point three million years.

But right now, just beyond that outer shell of ice, sits our true nearest neighbour in the galaxy—a dim red star forty trillion kilometres across the dark.

[CHAPTER CARD 5: PART FIVE — FOUR LIGHT-YEARS THROUGH THE DARK · 4.24 LIGHT-YEARS]
[SFX: tick_ink]

## Take 6 — Bridge 5: Proxima Centauri to Near Light Speed (`j01_vo_06_bridge5_lightspeed.mp3`, target ~17.0 s, 45 words)
[VISUAL MUST: Animated outward map (`code_graphic_J01_map_05_lightspeed.mp4`) showing relativistic clock-rate bar (1.00x at 17 km/s -> 0.14x at 99% c) across the 4.24 ly to 100,000 ly Milky Way scale · DATA: Ship clock rate at 99% light speed (7x slower than Earth) · SCALE: 75,000 years at Voyager speed vs 22 crew years across the galaxy at 1 g]
[SFX: whoosh_soft]
At the speed of our fastest space probes, crossing even that first four-light-year gap takes seventy-five thousand years.

To reach the stars inside a single human lifetime, a ship would have to push toward the speed of light itself—where time stops behaving the way it does at home.

[CHAPTER CARD 6: PART SIX — WHEN YOUR CLOCK SLOWS DOWN · 99% LIGHT SPEED]
[SFX: tick_ink]

## Take 7 — Bridge 6: Near Light Speed to Betelgeuse (`j01_vo_07_bridge6_betelgeuse.mp3`, target ~17.0 s, 46 words)
[VISUAL MUST: Animated outward map (`code_graphic_J01_map_06_betelgeuse.mp4`) stepping out to 600 light-years in Orion's shoulder, scaling the Sun up 764x to Betelgeuse's swollen red photosphere · DATA: Distance to Betelgeuse (~600 light-years) and radius (764 × Sun) · SCALE: Swallows the orbits of Mercury, Venus, Earth and Mars]
[SFX: rumble_low — deep stellar convection rumble]
Even without a relativistic starship, light itself brings the deeper galaxy to our eyes.

Look six hundred light-years out to the shoulder of Orion, and you see a dying supergiant seven hundred and sixty-four times wider than the Sun—building the heavy elements that made our world possible.

[CHAPTER CARD 7: PART SEVEN — THE DYING GIANT THAT MADE US · 600 LIGHT-YEARS]
[SFX: tick_ink]

## Take 8 — Closing (`j01_vo_08_closing.mp3`, target ~16.0 s VO + 18.0 s hold, 45 words)
[VISUAL MUST: Slow pull-back from Orion's glowing nebula dust across the inner Solar System back to the real rotating night-and-day Earth limb; 18-second clean starfield + Earth horizon hold for YouTube end screens]
[SFX: rumble_low — gentle resolve into ambient drone]
From the calcium in our bones forged inside dying supergiants, back across the light-years to the red dust of Mars, the thick clouds of Venus, and the spinning Earth beneath your feet—every world we study is part of the same long story.

Goodnight, and thank you for watching with us.
```

---

### 2.2 Clean TTS-Ready Text for All 8 Linking Takes

```markdown
## Take 1 — Cold Open (`j01_vo_01_intro.mp3`, ~48.0 s, 114 words)
Every machine humanity has ever landed on another world sits inside a bubble of light less than two light-hours across—while the nearest star beyond our Sun is four point two four light-years away.

Inside that small neighbourhood, we have set cameras down on a scorching twin where lead melts on the ground, and on a frozen red desert where nuclear rovers drive for years through the dust.

This is one continuous journey outward from the ground moving under your feet—past the worlds our landers have touched, through the comet cloud at the edge of the Sun's reach, and out to the giant stars that forged the atoms in your hands.

It begins right where you are sitting.

## Take 2 — Bridge 1: Earth to Venus (`j01_vo_02_bridge1_venus.mp3`, ~16.0 s, 43 words)
Earth's twenty-four-hour spin and liquid oceans kept its carbon locked safely in stone beneath the sea.

Step forty million kilometres inward to our closest planetary neighbour, where a single day lasts two hundred and forty-three Earth days—and that same carbon escaped into the sky.

## Take 3 — Bridge 2: Venus to Mars (`j01_vo_03_bridge2_mars.mp3`, ~16.0 s, 44 words)
On Venus, ninety-two bars of crushing heat silenced our toughest lander in just over two hours.

Head the other way from the Sun—two hundred and twenty-five million kilometres out to Mars—and the problem flips: an air so thin and cold that our robots can roam for over a decade.

## Take 4 — Bridge 3: Mars to the Oort Cloud (`j01_vo_04_bridge3_oort.mp3`, ~17.0 s, 46 words)
Beyond the rusty plains of Mars and the giant planets, the Sun's gravity still holds a vast shell of frozen comets ten thousand to a hundred thousand times further out than Earth.

And out there in the dark, another star is already heading our way.

## Take 5 — Bridge 4: Oort Cloud to Proxima Centauri (`j01_vo_05_bridge4_proxima.mp3`, ~16.0 s, 44 words)
Gliese seven-ten will not reach our comet cloud for another one point three million years.

But right now, just beyond that outer shell of ice, sits our true nearest neighbour in the galaxy—a dim red star forty trillion kilometres across the dark.

## Take 6 — Bridge 5: Proxima Centauri to Near Light Speed (`j01_vo_06_bridge5_lightspeed.mp3`, ~17.0 s, 45 words)
At the speed of our fastest space probes, crossing even that first four-light-year gap takes seventy-five thousand years.

To reach the stars inside a single human lifetime, a ship would have to push toward the speed of light itself—where time stops behaving the way it does at home.

## Take 7 — Bridge 6: Near Light Speed to Betelgeuse (`j01_vo_07_bridge6_betelgeuse.mp3`, ~17.0 s, 46 words)
Even without a relativistic starship, light itself brings the deeper galaxy to our eyes.

Look six hundred light-years out to the shoulder of Orion, and you see a dying supergiant seven hundred and sixty-four times wider than the Sun—building the heavy elements that made our world possible.

## Take 8 — Closing (`j01_vo_08_closing.mp3`, ~16.0 s, 45 words)
From the calcium in our bones forged inside dying supergiants, back across the light-years to the red dust of Mars, the thick clouds of Venus, and the spinning Earth beneath your feet—every world we study is part of the same long story.

Goodnight, and thank you for watching with us.
```

---

### 2.3 `MUST QUOTE` Fact Verification Table for New Linking Claims

Every numerical and factual claim in Takes 1–8 derives directly from the locked, Gemini-verified `SOURCES.md` tables of `023–029`:

| Take | Spoken Claim in Linking Script | Verified Source in Locked `023–029` `SOURCES.md` | Exact Quote / Verified Number |
|---|---|---|---|
| **Take 1** | Every machine *landed* on another world is inside `<2 light-hours` (Titan is `~1.3 light-hours` / `~9.5 AU` from Earth; Mars/Venus `<20 light-minutes`) | NASA NSSDCA Saturn/Titan & Mars/Venus Fact Sheets (`023`, `025`, `032`) | Saturn/Titan semi-major axis `9.58 AU` (`~79.7 light-minutes` = `1.33 light-hours`; round-trip or diameter across Saturn's orbit `<2.7 light-hours`, distance from Earth `<1.5 light-hours`). |
| **Take 1 & 5** | Nearest star beyond the Sun is `4.24 light-years` (`40 trillion km`) away | `026/01_Script/SOURCES.md` — Gaia Collaboration, Vallenari et al. 2023 (*A&A* 674, A1) & NASA Imagine the Universe | Proxima Centauri parallax `768.07 mas` → `4.2465 ly` (`4.017 × 10^13 km` ≈ `40 trillion km`). |
| **Take 1 & 3** | Venus `464 °C` (melts lead, `327.5 °C`), `92 bar`; *Venera 13* lasted just over two hours (`127 minutes`) | `023/01_Script/SOURCES.md` — NASA NSSDCA Venus Fact Sheet & Venera 13 mission page | Surface temperature `464 °C`, pressure `92 bar`, *Venera 13* survived `127 minutes`. |
| **Take 2** | Earth `24-hour` spin; Venus `40 million km` closest approach, `243 Earth days` retrograde sidereal rotation | `027/01_Script/SOURCES.md` & `023/01_Script/SOURCES.md` — NASA NSSDCA Earth & Venus Fact Sheets | Venus minimum distance from Earth `38–40 × 10^6 km`; rotation period `−5832.6 hours` (`243.025 Earth days`). |
| **Take 3** | Mars `225 million km` average distance from Sun (`~6 mbar` surface pressure, rovers lasting `>10 years`) | `025/01_Script/SOURCES.md` — NASA NSSDCA Mars Fact Sheet & NASA Opportunity 2019 release | Mars mean distance from Sun `227.9 × 10^6 km` (Earth-Mars mean distance `225 million km`), surface pressure `6.36 mbar`, *Opportunity* operated `14+ years` (`2004–2018`). |
| **Take 4 & 5** | Oort Cloud `10,000 to 100,000 AU`; *Gliese 710* arrives in `1.3 million years` (`13,000 AU`) | `028/01_Script/SOURCES.md` — NASA Oort Cloud Fact Sheet & Bailer-Jones 2022 (*ApJL* 935, L9) | Oort Cloud inner edge `2,000–10,000 AU`, outer edge `100,000 AU`; *Gliese 710* perihelion `t = +1.29 Myr` (`1.3 million years`), `d = 0.052 pc` (`~10,700–13,000 AU`). |
| **Take 6** | `75,000 years` to cross `4.24 light-years` at *Voyager 1*'s speed (`17 km/s`) | `026/01_Script/SOURCES.md` — NASA JPL Voyager Mission Status | `4.2465 ly / (17.0 km/s) = 74,900 years` (`~75,000 years`). |
| **Take 7** | Betelgeuse `~600 light-years` (`500–700 ly`) away, `764 times` wider than the Sun | `029/01_Script/SOURCES.md` — Joyce et al. 2020 (*ApJ* 902, 63) | Radius `764 (+116/−62) R_sun`; distance range `500–700 ly`. |

---

## 3. Ambient Bed Plan & Chapter Cues

### 3.1 How Music Works Across the 55 min 49 s Journey Film

Per **STUDIO_PLAYBOOK.md**, **Polish Pass §2**, and the lessons proven in `J0167` (`compilation_bed_plan_v02.json`):
1. **Inside each of the 7 reused long slices (`027`, `023`, `025`, `028`, `026`, `024`, `029`)**:
   - Each locked master cut already carries its own bespoke, `music_gate.py`-approved score bed mixed under Ben's narration (`~−14 LUFS` integrated master, bed `≥10 LU` under VO during speech, `0` rolling gaps).
   - At the start and end of each slice (and across the micro-joins where the standalone agenda line and duplicate subscribe beat are trimmed), we apply a `0.5 s` equal-power audio crossfade (`acrossfade=d=0.5:c1=tri:c2=tri`) on sentence boundaries so the internal bed never clicks or drops out.
2. **Across the Cold Open (`0:00–0:51`), Bridges 1–6 + Chapter Cards (`~19–20 s` each), and Closing + 18 s End Hold (`55:33–55:49`)**:
   - We lay one cohesive **Journey Ambient Score Bed** (`Pace: 66 BPM`, warm C-minor/G-modal space drone with a soft celesta/plucked harmonic pulse on the chapter cards) under the new linking VO takes.
   - **Crossfades at Chapter Cards**: As each Bridge enters its `3.0 s` Chapter Card, the Journey Ambient Bed swells gently (`−18 LUFS` during the `3.0 s` card pause, `≥6 LU` under VO integrated loudness) and crossfades over `2.5 s` into the incoming part's master score bed.
   - **Level Rule Compliance (`scripts/sfx_kit.py level`)**:
     - Linking VO normalized to `−16.0 LUFS` integrated (`−21 dB` mean, true peak `≤ −1.5 dBTP`) to match `023–029` masters (`−14.2 to −15.8 LUFS`).
     - Journey Ambient Bed sits at `−28.5 LUFS` (`12.5 LU` below VO while speaking, swelling to `−22.5 LUFS` in pauses, with automatic `400 ms` window ducking wherever `vo - bed < 10.5 LU`).
     - House SFX stem (`06_Sound-Effects/kit_v01`: `rumble_low.wav`, `whoosh_soft.wav`, `tick_ink.wav` generated via `python3 scripts/sfx_kit.py make --out-dir 02_Video-Projects/J01_Journey-To-Every-World/06_Sound-Effects/kit_v01`) sits `≥14 LU` below VO integrated loudness, `≥11 LU` below VO during speech, and `≥7 LU` below VO in pauses.

### 3.2 Two Options for Sourcing the Journey Ambient Bed (`£0` / `0 Credits` Recommended)

- **Option A — Zero-Credit Harmonic Stem Mix from Owned NAS Score Stems (Recommended, `0 credits`)**:
  - Uses the pristine, 100%-owned stereo score stems already on the NAS from our `023–026` films:
    - `/Volumes/data/mac-mini-archive/2026-11-05/YouTube/orbit-with-ben/02_Video-Projects/026_How-Far-Is-The-Nearest-Star/05_Music/nearest-star_score_bed_v01_full.wav` (warm interstellar ambient pad, used for Cold Open, Bridge 4, Bridge 6, and Closing)
    - `/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/02_Video-Projects/023_What-Happened-To-Venus/05_Music/venus_score_bed_v01_full.mp3` (deep planetary drone, used for Bridge 1 & Bridge 2)
    - `/Volumes/data/mac-mini-archive/2026-11-05/YouTube/orbit-with-ben/02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/05_Music/light-speed_score_bed_v01_full.mp3` (subtle rhythmic pulse, used for Bridge 3 & Bridge 5)
  - Pitch-matched and low-pass filtered (`fc=3200 Hz` during VO, opening to full spectrum on Chapter Cards) so the linking bridges share the exact sonic palette of the films they connect while costing **0 ElevenLabs credits**.
- **Option B — Fresh ElevenLabs Ambient Cue (`~3,000 credits` for a `180,000 ms` stem)**:
  - If Chief prefers a newly generated stem for `05_Music/j01_journey_ambient_bed_v01.mp3`, run `04_Audio/tools/generate_music_bed.py --length-ms 180000 --generate` with prompt:
    - `Mood: Calm, vast, warm cinematic space ambient drone with a gentle celesta harmonic lift every 24 seconds. Pace: 66-70 BPM. NOT: no heavy percussion, no dark horror dissonance, no trailer brass hits, distinct from 023-029 beds.`

---

## 4. Packaging: Titles, Three Thumbnail Concepts, Description & Chapters

### 4.1 Title Candidates (Obeying `LEARNINGS.md` Rules 11, 15, 18, 20, 21 & `THUMBNAIL_AND_TITLE_RULES.md`)

All candidates are under `58 characters`, carry no series suffix (`Rule 20`), and pair a concrete physical journey/stakes angle (`Rule 11 & 15`) with a real-imagery variant (`Rule 18`):

| # | Title Candidate | Chars | Rule Alignment |
|---|---|---|---|
| **1 (Primary — Journey / Scale)** | **From Earth to Orion: A 600-Light-Year Space Journey** | `51` | `Rule 21` (calm 40–60 min journey film) + `Rule 11` (concrete physical places + `600-Light-Year` scale). |
| **2 (A/B Test — Real Imagery, Rule 18)** | **The Real Images From Every World We Have Reached** | `48` | `Rule 18` (*"Name real spacecraft or telescope imagery in the title when we have it"* — Venera 13, Curiosity, Cassini, Gaia/VLT). |
| **3 (A/B Test — Consequence / Stakes, Rule 15)** | **What Happens as You Journey 600 Light-Years From Earth?** | `55` | `Rule 15` (second-person consequence question across the full outward spine from Earth's spin to Betelgeuse). |

---

### 4.2 Three Distinct Thumbnail Concepts (`LEARNINGS.md` Rules 12, 14, 19 & Never List)

Per **AGENTS.md Never List** and **LEARNINGS Rules 12, 14, 19**:
- **Three genuinely different picture ideas** (not 3 crops of the same image);
- **No Orbit** on any long-form thumbnail;
- **One focal point** that still reads at `168×94` (`thumb_preview.py long`);
- **1–3 words** in the top `22%` band (`y = 6%–22%`), adding a concrete number or contrast that **never repeats the title**;
- Includes **Rule 19** (a single clean real spacecraft frame) and **Rule 14** (a bright high-contrast background breaking the dark brown template).

| Concept | Picture Idea & Composition (`1920×1080`) | Thumbnail Text (`1–3 words`, top `22%` band) | Rules Tested |
|---|---|---|---|
| **Concept A (`thumb_A_real_venera_mars.jpg`)** | **Rule 19 — Single Clean Real Spacecraft Surface Frame**: Full-bleed, high-contrast graded real *Venera 13* Venus surface panorama (`PIA00233` basalt slabs and lander camera teeth under amber sulfuric sky) split cleanly along a diagonal horizon line with *Curiosity*'s real Mount Sharp panorama (`PIA19803`). One immediate physical contrast: the hottest and coldest rocky surfaces our cameras have ever touched. | **`464°C` TO `-60°C`** *(3 tokens; yellow highlight on `464°C`)* | **Rule 19** (real spacecraft frame, no composite clutter) + **Rule 12** (concrete number contrast not in the title). |
| **Concept B (`thumb_B_bright_supergiant_scale.jpg`)** | **Rule 14 — Bright High-Contrast Background**: Blinding golden-orange photosphere of red supergiant *Betelgeuse* (`764 × Sun`) filling the right two-thirds of the frame (breaking the dark space template with a bright, glowing stellar wall), with a tiny crisp blue-and-white Earth (`DSCOVR` real disk) hanging on the left against deep indigo space. | **`764×` OUR SUN** *(3 words)* | **Rule 14** (bright background vs dark channel template) + **Rule 12** (single scale shock). |
| **Concept C (`thumb_C_outward_worlds_lineup.jpg`)** | **Outward Journey Progression**: Clean horizontal progression across dark space from left to right: real `DSCOVR` Earth → golden `Akatsuki/Magellan` Venus → rusty `Viking` Mars → glowing orange `Betelgeuse` on the far right, connected by a single crisp white distance arc (`0 KM → 600 LY`). | **`8` WORLDS OUT** *(3 words)* | **Rule 21** (visualises the multi-world journey arc at a glance at `168×94`). |

---

### 4.3 Full YouTube Description & Chapter Timestamps (`11_Upload-Package/Descriptions/j01_description_v01.txt`)

```text
Every spacecraft humanity has ever landed on another world sits inside a bubble of light less than two light-hours wide—while the nearest star beyond our Sun is 4.24 light-years away. In this 56-minute journey film, we travel outward from the spinning ground under your feet, to the crushing 464 °C surface of Venus, the nuclear rovers of Mars, the frozen comet cloud where another star is heading our way, across the four-light-year gap to Proxima Centauri, near the speed of light itself, and 600 light-years out to the dying supergiant Betelgeuse.

Chapters:
0:00 A Bubble Two Light-Hours Wide (Cold Open)
0:48 Part 1: What If Earth Stopped Spinning? (0 km)
8:14 Bridge: 40 Million Kilometres Inward
8:30 Part 2: What Happened to Venus? (40 Million km)
16:28 Bridge: From 92 Bars to 6 Millibars
16:44 Part 3: Could a Robot Survive on Mars? (225 Million km)
24:12 Bridge: Past the Planets to the Oort Cloud
24:29 Part 4: What Happens When a Star Enters Our Solar System? (13,000 AU)
31:45 Bridge: Across the Four-Light-Year Gap
32:01 Part 5: Why Reaching the Nearest Star Takes 75,000 Years (4.24 Light-Years)
39:36 Bridge: Pushing Toward the Speed of Light
39:53 Part 6: What Happens If You Travel Near Light Speed? (0.99c)
47:18 Bridge: 600 Light-Years to Orion's Shoulder
47:35 Part 7: Is Betelgeuse About to Explode? (600 Light-Years)
55:33 Back to the Ground Under Your Feet

Watch the individual films in our Space & Planetary Science playlist:
• What If Earth Stopped Spinning? — https://youtu.be/6bbbvfCx6zY
• What Happened to Venus? — https://youtu.be/VBaYRPp85Sw
• Could a Robot Survive on Mars? — https://youtu.be/Js6EQJ8qDi8
• What Happens When a Star Enters Our Solar System? — https://youtu.be/F-jImX5h7ws
• Why Reaching the Nearest Star Takes 75,000 Years — https://youtu.be/c5AdqQsnnys
• What Happens If You Travel Near Light Speed? — https://youtu.be/rVqgtkBV3jc
• Is Betelgeuse About to Explode? — https://youtu.be/vP1BbqZ_dnM

Sources: Williams 2024, NASA GSFC Earth/Venus/Mars Fact Sheets (planetary radii, spin periods, 464 °C / 92 bar Venus, 6.36 mbar Mars); Donahue et al. 1982, Science 216, 630 (Pioneer Venus D/H ratio ~100× Earth); Hassler et al. 2014, Science 343, 1244797 (Curiosity RAD Mars surface radiation 0.64 mSv/day); Bailer-Jones 2022, ApJL 935, L9 (Gaia DR3 Gliese 710 encounter in 1.29 Myr at 0.052 pc); Gaia Collaboration, Vallenari et al. 2023, A&A 674, A1 (Proxima Centauri distance 4.2465 ly); Ashby 2003, Living Reviews in Relativity 6, 1 (GPS relativistic clock shift +38 μs/day); Joyce et al. 2020, ApJ 902, 63 & Montargès et al. 2021, Nature 594, 365 (Betelgeuse radius 764 R_sun and 2019–2020 Great Dimming dust cloud).

Image and video credits: NASA / JPL-Caltech / GSFC / SDO / DSCOVR / MSSS / ASU / Cornell / Space.com / Roscosmos Venera 13 archive; ESO / M. Montargès et al. (VLT-SPHERE Betelgeuse); ESA / Gaia / DPAC. Narrated by Ben.
```

---

## 5. ElevenLabs Credit Estimate (Inside Existing Flat Fee, Zero Top-Up)

Per **AGENTS.md** (*"All subscription credit floors are zero... Only subscription or trial credit: never buy credits, top up, upgrade or enable paid overage"*):

| Item | Tool & Model | Volume | Estimated ElevenLabs Credits | Notes |
|---|---|---|---|---|
| **1. New Linking VO (`8 takes`: Cold Open, Bridges 1–6, Closing)** | `04_Audio/tools/vo_take.py` (`eleven_v3`, voice `kDch6ACCIpqgQ0NsU9kk`) | `392 words` / `2,240 characters` (plus `~25%` buffer for 1–2 retakes = `~2,800 chars`) | **`~1,400 – 2,800 credits`** *(1 credit/char list rate, or `~0.5×` counter delta observed on `025–029`)* | Tiny spend (`<1.5%` of a monthly Creator allowance); reuses 100% of the existing locked VO inside `023–029`. |
| **2. Word-Timestamp Alignment (`vo_words.json` / `.srt`)** | `faster-whisper` (`base.en` local on Mini) or `transcribe_vo.py` (`scribe_v2`) | `2 min 46 s` of linking VO | **`0 credits`** *(using local `faster-whisper` on the Mini)* | Zero ElevenLabs spend required for caption/cut alignment. |
| **3. Journey Ambient Bed (`Option A — Recommended`)** | `ffmpeg` harmonic stem builder from owned `023/024/026` NAS score stems | `3 min 04 s` across Cold Open, Bridges 1–6, Cards & Closing | **`0 credits`** | Reuses our owned ElevenLabs score stems already on the NAS (`nearest-star_score_bed_v01_full.wav`, `venus_score_bed_v01_full.mp3`, `light-speed_score_bed_v01_full.mp3`). |
| **4. House SFX (`rumble_low`, `whoosh_soft`, `tick_ink`)** | `python3 scripts/sfx_kit.py make` | 3 synthesized WAV cues | **`0 credits`** | Local Python synthesis, zero API spend. |
| **Total ElevenLabs Spend (`Option A`)** | | | **`~1,400 – 2,800 credits` (`£0.00` overage, no top-up)** | *(Even if Chief selects Option B for a fresh 180 s ambient bed cue, that adds `~3,000 credits`, keeping total spend under `5,800 credits` inside the flat fee.)* |

---

## 6. Downstream Production Pipeline (`--film J01`)

Per the `J2146` brief (*"It takes the next WIP slot when 031 or 032 reaches Ben's watch. Then queue the VO, assembly and review jobs with --film J01"*), `02_Video-Projects/J01_Journey-To-Every-World` is initialized with `status.json`, `01_Script/j01_linking_script_v01.md`, and `01_Script/SOURCES.md`, `"OWB:J01"` is placed at the front of `jobs/WIP.json` `next`, and four dependent jobs are queued with `--film J01`:

1. **Chief Script & Plan Review (`--film J01 --stage script`, `kind: chief`)**: Chief reviews `jobs/reviews/J2146/JOURNEY_01_PLAN.md` and `02_Video-Projects/J01_Journey-To-Every-World/01_Script/j01_linking_script_v01.md` and marks `J01` `script` `done` when `J01` takes the active WIP slot (after `031` or `032` reaches Ben's watch).
2. **Linking VO Recording (`--film J01 --stage vo`, `kind: vo`, `--after <script_review_id>`)**: Record the 8 linking VO takes (`j01_vo_01_intro.mp3` through `j01_vo_08_closing.mp3`, `~392 words`) via `04_Audio/tools/vo_take.py`, verify with `faster-whisper` (`0` repeated/stumbled phrases, `130–145 wpm`), and save `VO_STATUS.md`.
3. **Journey Film 01 Assembly & QA (`--film J01 --stage edit`, `kind: assembly`, `--after <vo_job_id>`)**: Render the 7 animated outward distance map code graphics (`code_graphic_J01_map_00` to `06`) and 7 chapter cards, build the Journey Ambient Bed + `sfx_kit.py` stems, stitch the verified NAS master slices of `027`, `023`, `025`, `028`, `026`, `024`, and `029` into `07_Edit-Project/J01_Journey_v01.mp4` (`~55m49s`, CFR 24 fps, `~−14 LUFS`), build the 3 thumbnail concepts (`thumb_A`, `thumb_B`, `thumb_C` + `thumb_preview.py`), and pass `picture_qa.py`, `music_gate.py`, and `sfx_kit.py level`.
4. **Chief Cut & Packaging Review (`--film J01 --stage edit`, `kind: review`, `--requires audio_input,moving_video_input`, `--after <assembly_job_id>`)**: Full watch/listen review of `J01_Journey_v01.mp4` and the 3 thumbnails before queuing Ben's watch (`awaits_ben`).
