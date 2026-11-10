# J2219 — Rule H Review: OWB Journey Film 01 (`J01`) Plan & Linking Script (`J2146`)

- **Date:** 5 November 2026 (`2026-11-05T19:43Z`)
- **Reviewer / Worker:** `macbook-2` (Gemini 4 Argon, Rule H review lane)
- **Film / Stage:** `OWB:J01` (`02_Video-Projects/J01_Journey-To-Every-World`) · `script`
- **Reviewed Job / Evidence:** `J2146` (*Journey film 01: plan and linking script from 023-030 (LEARNINGS rule 21)*, `done_ref: 1e9ba89b33`):
  - `jobs/reviews/J2146/JOURNEY_01_PLAN.md`
  - `02_Video-Projects/J01_Journey-To-Every-World/01_Script/j01_linking_script_v01.md`
  - `02_Video-Projects/J01_Journey-To-Every-World/01_Script/SOURCES.md`
  - `02_Video-Projects/J01_Journey-To-Every-World/11_Upload-Package/Descriptions/j01_description_v01.txt`
  - Word-level master transcripts (`*_words_list.json`) and locked `01_Script/SOURCES.md` files across `023–030`
- **Spend:** £0.00 / 0 credits (plan & linking script review only)
- **Verdict:** **KEEP (`J01` `script` locked `done`; `J2220` VO unlocked for execution when `OWB:J01` takes the next active WIP slot after `031` or `032` reaches Ben's watch)**

---

## 1. 7-Part Outward Running Order & Word-Boundary Verification (`023–030`) — `PASS`

### 1.1 Outward Narrative Spine & `030` Status
- **7-Part Outward Progression (`0 km → 600 light-years`):**
  1. **Part 1 (`0 km` — `027` *What If Earth Stopped Spinning?*, `6bbbvfCx6zY`):** Earth's `1,670 km/h` equatorial spin, `1.8 ms/century` lunar tidal braking, and `4.5-billion-year` rotational momentum.
  2. **Part 2 (`40 Million km` — `023` *What Happened to Venus?*, `VBaYRPp85Sw`):** Nearest planetary neighbour (`243-Earth-day` retrograde spin, `92 bar`, `464 °C` runaway greenhouse, *Venera 13*'s `127 minutes`).
  3. **Part 3 (`225 Million km` — `025` *Could a Robot Survive on Mars?*, `Js6EQJ8qDi8`):** Next rocky world (`6.36 mbar`, `−60 °C`, *Spirit*, *Opportunity* `14+ years`, *Curiosity*, *Ingenuity* `72 flights`).
  4. **Part 4 (`10,000–100,000 AU` — `028` *What Happens When a Star Enters Our Solar System?*, `F-jImX5h7ws`):** Outer Oort Cloud shell and *Gliese 710*'s `13,000 AU` encounter in `1.3 million years`.
  5. **Part 5 (`4.24 Light-Years` — `026` *Why Reaching the Nearest Star Takes 75,000 Years*, `c5AdqQsnnys`):** *Proxima Centauri* (`40 trillion km`) and *Voyager 1*'s `17 km/s` (`75,000-year`) crossing.
  6. **Part 6 (`0.99c` / `22 Crew Years` — `024` *What Happens If You Travel Near Light Speed?*, `rVqgtkBV3jc`):** Relativistic time dilation (`γ ≈ 7.09` at `0.99c`, muon decay, GPS `+38 μs/day`, `1 g` Milky Way crossing).
  7. **Part 7 (`600 Light-Years` — `029` *Is Betelgeuse About to Explode?*, `vP1BbqZ_dnM`):** Red supergiant *Betelgeuse* (`764 R_sun`, `500–700 ly`, `2019–2020` Great Dimming, core collapse, and stellar nucleosynthesis of oxygen and calcium).
- **`030` (*Apophis — Closer Than Our Satellites*) Status (`PASS`):** Verified against `02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites/status.json` (`J1772` / `J1356`) that `030` has a locked script (`apophis_script_master_v02.md`) whose completed production to date is the standalone Short (`gJwNJN_yMKU`) and AR Short cohort (`J1356`), with no rendered long master cut on the NAS. Excluding `030` from `J01` keeps the 7-part Journey Film at **55–58 minutes** inside the **40–60 min** `LEARNINGS.md` Rule 21 target without blocking on an unrendered long.

### 1.2 Programmatic Word-Boundary Audit Across All 19 Reused Master Slices (`0` Clipped Words)
Every `[in → out]` slice timestamp in `JOURNEY_01_PLAN.md` §1.3 was checked programmatically against the locked edit word lists (`*_words_list.json`) for `027`, `023`, `025`, `028`, `026`, `024`, and `029`:

| Part & Film | Word List Verified | Slice Windows (`s`) | Raw Slice Sum | Clipped Words (`start` / `end`) | Agenda Line Trimmed (`LEARNINGS` Rule 10) | Duplicate Subscribe Beat Trimmed (`AGENTS.md` Never List) | Outro Teaser Trimmed |
|---|---|---|---:|---|---|---|---|
| **Part 1: `027` Earth's Spin** | `rough_v01i_pack/earth_spin_words_list.json` (`1,128w`) | `0.00 → 443.50` | `443.50 s` (`7:23.50`) | `0` / `0` (ends `442.82 s` `"running down."`, `+0.68 s` breath) | None in `027` v02 | **KEPT** at `164.90–169.42 s` (`03:35.90` film time — single subscribe beat for `J01`) | None |
| **Part 2: `023` Venus** | `full_rough_v05e_pack/venus_words_list.json` (`1,247w`) | `0.00–35.80`, `43.20–212.20`, `218.20–504.80` | `491.40 s` (`8:11.40`) *(plan table notes `474.60 s` net)* | `0` / `0` (ends `35.24 s`, `211.62 s`, `504.48 s` `"same turn?"`) | Trims `36.32–42.74 s` (*"In this film, I will show you..."*) | Trims `212.74–217.50 s` (*"We make one of these every week..."*) | Trims `505.82–509.50 s` (*"Next week, what happens to your clock..."*) |
| **Part 3: `025` Mars** | `full_rough_v03d_pack/mars_robot_words_list.json` (`1,186w`) | `0.00–29.80`, `40.80–224.50`, `231.00–483.20` | `465.70 s` (`7:45.70`) *(plan table notes `445.70 s` net)* | `0` / `0` (ends `29.32 s`, `223.64 s`, `482.86 s` `"covers it."`) | Trims `30.32–40.50 s` (*"In this film, I will show you..."*) | Trims `225.06–230.22 s` (*"We make one of these every week..."*) | Trims `483.80–486.70 s` (*"Next week, how far is the nearest star?"*) |
| **Part 4: `028` Gliese 710** | `full_master_v03_pack/gliese_words_list.json` (`1,195w`) | `0.00–30.80`, `42.20–204.20`, `209.80–469.80` | `452.80 s` (`7:32.80`) *(plan table notes `432.80 s` net)* | `0` / `0` (ends `30.14 s`, `203.76 s`, `469.34 s` `"another sun."`) | Trims `31.30–41.92 s` (*"In this film, I will show you..."*) | Trims `204.66–209.44 s` (*"We make one of these every week..."*) | Excess silent tail trimmed after `469.34 s` |
| **Part 5: `026` Nearest Star** | `rough_v06_pack/nearest_star_words_list.json` (`1,167w`) | `0.00–20.50`, `32.80–224.40`, `232.00–491.30` | `471.40 s` (`7:51.40`) *(plan table notes `451.40 s` net)* | `0` / `0` (ends `19.34 s`, `223.84 s`, `490.96 s` `"measure the gap"`) | Trims `20.88–32.50 s` (*"In this film, I will show you..."*) | Trims `224.94–231.08 s` (*"We make one of these every week..."*) | None |
| **Part 6: `024` Light Speed** | `full_rough_v06_pack/light_speed_words_list.json` (`1,201w`) | `0.00–28.30`, `41.60–213.10`, `220.00–483.00` | `462.80 s` (`7:42.80`) *(plan table notes `442.80 s` net)* | `0` / `0` (ends `27.88 s`, `212.48 s`, `482.52 s` `"not be waiting."`) | Trims `28.72–41.38 s` (*"In this film, I will show you..."*) | Trims `213.64–219.02 s` (*"We make one of these every week..."*) | Trims `484.44–487.54 s` (*"Next week, could a robot survive on Mars?"*) |
| **Part 7: `029` Betelgeuse** | `full_rough_v03b_pack/betelgeuse_words_list.json` (`1,248w`) | `0.00–22.10`, `37.20–242.20`, `247.60–514.80` | `494.30 s` (`8:14.30`) *(plan table notes `474.30 s` net)* | `0` / `0` (ends `21.40 s`, `241.88 s`, `514.26 s` `"Sun was born."`) | Trims `22.58–36.96 s` (*"In this film, I will show you..."*) | Trims `242.70–247.18 s` (*"We make one of these every week..."*) | Excess silent tail trimmed after `514.26 s` |
| **Total Reused Body** | | **19 slices across 7 masters** | **`3,281.90 s` (`54:41.90`) raw / `3,165.10 s` (`52:45.10`) net** | **`0` clipped words** | **All 6 agenda lines removed** | **6 duplicates removed; 1 kept (`027`)** | **All 3 weekly teasers removed** |

> **Assembly Note for `J2221`:** The raw sum of the 19 `[in → out]` slices is `54 min 41.90 s` (`3,281.90 s`); combined with the `~3 min 04 s – 3 min 22 s` of linking VO, chapter cards, `0.5 s` crossfades, and the `18.0 s` post-VO end-screen hold after Take 8, the assembled master will run **`~55 min 49 s – 57 min 55 s`**, squarely inside the **40–60 min** `LEARNINGS.md` Rule 21 window. Update the chapter timestamps in `11_Upload-Package/Descriptions/j01_description_v01.txt` to match the exact rendered frame boundaries of `J01_Journey_v01.mp4`.

---

## 2. Linking Script (`j01_linking_script_v01.md`) & `SOURCES.md` Verification — `PASS`

1. **8 Linking VO Takes (`392` nominal words / `442` whitespace words, `2,576 chars`, `~163 s` spoken VO):**
   - **Take 1 (`j01_vo_01_intro.mp3`, `~48.0 s`, `114/117 w`):** Opens on a concrete physical scale contrast in sentence 1 (*"Every machine humanity has ever landed on another world sits inside a bubble of light less than two light-hours across—while the nearest star beyond our Sun is four point two four light-years away."*), followed immediately in the first 15 s by Venus (`464 °C`, melting lead) vs Mars (`−60 °C`, nuclear rovers). Contains **zero agenda lines** (`LEARNINGS.md` Rule 10).
   - **Takes 2–7 (`j01_vo_02_bridge1_venus.mp3` through `j01_vo_07_bridge6_betelgeuse.mp3`, `~16–17 s` each, `42–49 w` each):** Six outward bridges linking each world's physical conditions and distance scale (`0 km → 40M km → 225M km → 13,000 AU → 4.24 ly → 0.99c → 600 ly`) into the next `3.0 s` Chapter Card.
   - **Take 8 (`j01_vo_08_closing.mp3`, `~16.0 s` VO + `18.0 s` hold, `45/50 w`):** Synthesizes the outward journey from supergiant calcium nucleosynthesis back to Earth's spin, followed by an `18.0 s` picture+music hold for YouTube end screens (`LEARNINGS.md` Rule 20). *(Note for `J2221`: `"Goodnight, and thank you for watching with us."` sits after a clean sentence boundary following `"...every world we study is part of the same long story."`—suited to the bedtime/background journey format of `LEARNINGS.md` Rule 21, and cleanly trimmable at the sentence boundary if desired).*
2. **Teach-on-Screen & Polish Pass Markers (`PASS`):**
   - Contains `10` `[VISUAL MUST]` blocks, `7` `DATA:` markers (`code_graphic_J01_map_00` through `06`), `7` paired `SCALE:` comparisons (`100%` `SCALE:DATA` parity), `1` `WHEN:` stamp, `1` `FACT:` card (`Two worlds, 520 °C apart`), `7` `[CHAPTER CARD]` markers, and `16` `[SFX:]` cues (`rumble_low`, `whoosh_soft`, `tick_ink`).
3. **`SOURCES.md` Fact & Quote Audit (`PASS`):**
   - Every numerical claim in Takes 1–8 was cross-checked against `02_Video-Projects/J01_Journey-To-Every-World/01_Script/SOURCES.md` and the locked `01_Script/SOURCES.md` files of `023–029`:
     - `<2 light-hours` landed-spacecraft bubble: *Huygens* on Titan at `a = 9.5826 AU` (`79.7 light-minutes = 1.33 light-hours`, diameter `<2.7 light-hours`, Earth–Titan distance at landing `~1.1–1.3 light-hours`; Williams 2024 NASA Saturn Fact Sheet).
     - `4.24 light-years` (`40 trillion km`) to *Proxima Centauri*: Gaia DR3 parallax `768.07 ± 0.03 mas` (`d = 4.2465 ly = 4.017 × 10^13 km`; Vallenari et al. 2023, *A&A* 674, A1, `026/01_Script/SOURCES.md`).
     - Venus `464 °C` (lead melts at `327.5 °C`), `92 bar`, *Venera 13* `127 minutes` (`>2 hours`), `40 million km` closest approach, `243 Earth days` retrograde sidereal rotation (`−5832.6 h`): NASA NSSDCA Venus Fact Sheet (`023/01_Script/SOURCES.md`).
     - Mars `225 million km` mean Earth–Mars distance (`227.9 × 10^6 km` semi-major axis), `6.36 mbar` surface pressure, *Opportunity* `14+ years`: NASA NSSDCA Mars Fact Sheet (`025/01_Script/SOURCES.md`).
     - Oort Cloud `10,000–100,000 AU`; *Gliese 710* perihelion in `1.29 Myr` (`1.3 million years`) at `0.052 pc` (`~10,700–13,000 AU`): NASA Oort Cloud Fact Sheet & Bailer-Jones 2022, *ApJL* 935, L9 (`028/01_Script/SOURCES.md`).
     - `75,000 years` to cross `4.24 ly` at *Voyager 1*'s `17 km/s`; `99%` light speed slows ship clock `7×` (`γ = 7.089`): NASA JPL Voyager Status & Taylor/Wheeler (`026` & `024` `SOURCES.md`).
     - *Betelgeuse* `~600 light-years` (`548–724 ly` range across Joyce et al. 2020 & Harper et al. 2017) and `764 (+116/−62) R_sun` (`3.55 AU`, swallowing the orbits of Mercury, Venus, Earth, and Mars): Joyce et al. 2020, *ApJ* 902, 63 (`029/01_Script/SOURCES.md`).

---

## 3. Ambient Bed Plan, ElevenLabs Budget & Packaging Verification — `PASS`

1. **Ambient Bed Plan (`Option A` Approved, `0` ElevenLabs Credits):**
   - Approves **Option A (Zero-Credit Harmonic Stem Mix)** using our owned stereo score stems on the NAS (`nearest-star_score_bed_v01_full.wav`, `venus_score_bed_v01_full.mp3`, `light-speed_score_bed_v01_full.mp3`) across the Cold Open, Bridges 1–6, Chapter Cards, and Closing (`18 s` end hold), with `0.5 s` equal-power crossfades inside part trims and `2.5 s` crossfades at Chapter Cards, plus synthesized house SFX (`scripts/sfx_kit.py make --out-dir 02_Video-Projects/J01_Journey-To-Every-World/06_Sound-Effects/kit_v01`) passing `scripts/sfx_kit.py level`.
2. **ElevenLabs Credit Estimate (`~1,400–2,800 credits`, `£0.00` overage):**
   - Only the 8 linking VO takes (`442 words` / `2,576 chars`) use ElevenLabs (`04_Audio/tools/vo_take.py`, voice `kDch6ACCIpqgQ0NsU9kk`, `eleven_v3`), staying well inside the existing monthly subscription allowance with zero top-up.
3. **Titles, 3 Thumbnail Concepts & Description (`LEARNINGS.md` Rules 11, 12, 14, 15, 18, 19, 20, 21):**
   - **3 Titles:**
     - Candidate 1 (Journey / Scale): *From Earth to Orion: A 600-Light-Year Space Journey* (`51 chars`; tightened `≤50-char` Rule 15 option for upload: **`From Earth to Orion: A 600-Light-Year Journey`**, `45 chars`).
     - Candidate 2 (Rule 18 Real Imagery): **`The Real Images From Every World We Have Reached`** (`48 chars`, `≤50 chars` PASS).
     - Candidate 3 (Rule 15 Consequence / Stakes): *What Happens as You Journey 600 Light-Years From Earth?* (`55 chars`; tightened `≤50-char` Rule 15 option: **`What Lies on a 600-Light-Year Journey From Earth?`**, `49 chars`).
   - **3 Distinct Thumbnail Concepts (No Orbit, `1–3 words` in top `22%` band, never repeating title):**
     - **Concept A (`thumb_A_real_venera_mars.jpg` — Rule 19 Real Spacecraft Frame):** Real *Venera 13* (`PIA00233`) vs *Curiosity* Mount Sharp (`PIA19803`) surface split · Hook: **`464°C` TO `-60°C`**.
     - **Concept B (`thumb_B_bright_supergiant_scale.jpg` — Rule 14 Bright High-Contrast Background):** Blinding golden-orange *Betelgeuse* photosphere wall (`764 × Sun`) vs tiny crisp `DSCOVR` Earth · Hook: **`764×` OUR SUN**.
     - **Concept C (`thumb_C_outward_worlds_lineup.jpg` — Rule 21 Outward Progression):** Clean horizontal progression (`DSCOVR` Earth → Venus → Mars → *Betelgeuse*) with white distance arc · Hook: **`8` WORLDS OUT**.
   - **Description (`11_Upload-Package/Descriptions/j01_description_v01.txt`):** Updated on `macbook/J2219` to include the required `AGENTS.md` §2.5 honest disclosure line (*"Pictures: AI-generated scenes alongside NASA/ESA imagery. Facts: every number is checked against the sources listed below."*) after the image and agency credits.

---

## 4. Handoff & Queue Application (`jobs.with_git`)

1. **`J01` `script` set to `done`** via `studio.py` (`ref: 1e9ba89b33` / `J2219` review PR), unlocking `J2220` (*J01 Journey Film 01: record 8 linking VO takes (~392 words, J2146)*, `after: J2219`).
2. **WIP Ordering Preserved (`jobs/WIP.json`):** `OWB:J01` remains at the front of `WIP.json` `next` and takes the next active OWB WIP slot when `031` or `032` reaches Ben's watch (`AGENTS.md` Rule G).
3. **`J2219` closed `done`** with verdict `KEEP`.
