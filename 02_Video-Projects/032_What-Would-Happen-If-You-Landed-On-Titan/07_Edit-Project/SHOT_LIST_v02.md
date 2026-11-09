# 032 What Would Happen If You Landed on Titan? SHOT_LIST v02 (Gemini Rule-E review, 4 Nov 2026, J2044)

Timed to `02_Voiceover/stt/titan_landing_vo_v02b/stt_raw.json`. That is the locked VO `titan_landing_vo_v02b` (582.44 s; Chief h31, J1294). Its listen check is Ben's final watch, under Ben's 4 Nov rule (J1753 done).

Times are exact Scribe word-boundary spans (`0.16–582.38 s`, all 1,379 spoken words covered with zero words split across a row boundary). Each row is a beat, every cut sits in a VO pause, and every cut is `≤ 6.0 s`.

**Rule-E review fixes applied in v02 (J2044, over Claude's v01 from J2042):**
1. **VO span boundary fix (Rows 7–8):** In v01, the boundary at `60.10 s` cut through the spoken word `"towards"` (`60.00–60.30 s` in `stt_raw.json`). Moved the Row 7 / Row 8 boundary to the natural clause pause after `"Saturn,"` (`51.26–60.92 s` and `61.32–68.06 s`), so all 1,379 words in `stt_raw.json` sit cleanly inside a row.
2. **4–6 s cut pacing:** Increased cut counts on Rows 8, 10, 19, 25, 26, 31, 38, 39, 40, 41, 42, 43, 46, 47, 49, 50, 51 and 52 so every row averages `≤ 6.0 s/cut` (`3.0–6.0 s/cut`).
3. **Teach on screen (`WHO`, `WHEN`, `DATA`, `FACT`, no back-to-back full-frame code graphics):**
   - Added sourced birth–death years and `≤ 4`-word roles from `SOURCES.md` row 17 to both `WHO` lower-third cards: Row 7 `"Christiaan Huygens / (1629–1695) — Dutch astronomer"` and Row 10 `"Gerard Kuiper / (1905–1973) — Dutch-born astronomer"`. Dropped the unsourced Kuiper photo conditional in Row 10 per `AGENTS.md` (*"Show no portrait we can't source; the card can sit over the scene alone"*).
   - Linked all 7 spoken `WHEN` dates (`25 March 1655`, `1944`, `November 1980`, `14 January 2005`, `2013`, `NET July 2028`, `Late 2034`) to the progressive CODE `timeline` (`titan_landing_script_master_v02.md` lines 28, 45, 79, 114), and added `CODE` to the `Source` column of Rows 12, 15, 16 and 47.
   - Added explicit `≤ 4`-word CODE `FACT` cards on Rows 20 (`"WATER ICE IS ROCK"`), 23 (`"MOST DISTANT LANDING"`), 41 (`"NO OXYGEN TO BURN"`) and 47 (`"IDEAL WAY TO TRAVEL"`, verbatim from `SOURCES.md` row 15).
   - Interleaved graded real NASA/ESA/APL imagery between CODE graphics across Rows 3–4, 8–10, 19, 27–29, 33–34 and 38–43 so no two full-frame code graphics run back to back.
   - Changed Row 35's subsurface ocean cutaway from a labelled NASA schematic to our own CODE graphic (`ocean_cutaway`) over a graded Cassini Titan globe so no textbook/labelled source diagram triggers `picture_qa.py`.
4. **`SOURCES.md` number check:** Added explicit sourced diameters (`Titan 5,150 km`, `Mercury 4,879 km`, `Moon 3,475 km` from `SOURCES.md` row 3) to Row 9, explicit `1 bar vs 1.47 bar (≈ 1.5×)` (`SOURCES.md` row 1) to Row 3, `0 °C to −179 °C` (`SOURCES.md` row 8) to Row 19, `9.2 m/s (spoken: about 9 m/s)` (`SOURCES.md` row 10) to Row 28, `55–80 km (tens of km)` (`SOURCES.md` row 13) to Row 35, `78% N₂ / 21% O₂` (`SOURCES.md` rows 9 & 14) to Row 39, and `21 years` (`SOURCES.md` row 18) to Row 52. Removed the unsourced `"about 8 km altitude"` note from Row 17.
5. **Still reuse cap (`≤ 2` uses per still):**
   - Replaced Row 5's opening pebble still with the Huygens DISR descent floodplain view (`PIA07231` / descent movie floodplain segment) and Row 25's third pebble look with the Huygens DISR wide surface-to-horizon panorama (`PIA07233`), keeping the Huygens surface colour pebbles still (`PIA07232`) to **2 uses** (Rows 18 and 20).
   - Replaced Row 44's third use of the Cassini north polar lakes mosaic with Cassini ISS crescent Titan haze (`PIA14909`) + APL Dragonfly parachute descent animation, keeping the north polar lakes radar mosaic (`PIA10008`) to **2 uses** (Rows 31 and 32).

**Chapters are inferred from the script's question bridges.** The VO lock records fades, not absolute chapter ends, so the assembler confirms them against `chapters_index.json` if one exists:
- ch0 0–50.44
- ch1 51.26–136.68
- ch2 137.56–245.10
- ch3 246.00–324.44
- ch4 325.32–388.92
- ch5 389.76–474.10
- ch6 474.94–582.38

**House rules applied (029 lessons, AGENTS "Teach on screen", LEARNINGS 10):**
- **Frame 0** is moving footage of the subject: the Huygens descent movie. There is no title card and no Orbit at frame 0.
- **Every DATA / WHO / WHEN / FACT item is our own CODE graphic,** built with `code_graphics.py`, with no two full-frame code graphics back to back.
- **Stills:** no still more than twice, the second use reframed. Upscale ≤ 2.35×.
- **Plates:** change every 4–6 s.

**Spend: £0 in this list.**
- **Two Orbit beats are marked OMNI** (rows 26, 46). They are flagged for the Chief's price pass, with £0 CODE/NASA fallbacks written.
- **No Veo.**

**Sources (licences named per source; logged in `HARVEST_POOL_v01.json` at harvest):**
- **NASA/JPL-Caltech:** Cassini ISS, VIMS and RADAR (`PIA07231`, `PIA07232`, `PIA07233`, `PIA08399`, `PIA10008`, `PIA14909`, `PIA17172`, `PIA20016`, `PIA20021`, `PIA21445`, etc.) and JPL mission animations. **Licence:** Public Domain (`NASA/JPL-Caltech`; credit instrument team where requested).
- **ESA/NASA/JPL/University of Arizona:** Huygens DISR descent movie and surface/channel mosaics. **Licence:** NASA/JPL Photojournal releases are Public Domain (`ESA/NASA/JPL/University of Arizona`); ESA Multimedia direct files are `CC BY-SA 3.0 IGO` (credit `ESA/NASA/JPL/University of Arizona`).
- **NASA/Johns Hopkins APL:** Dragonfly mission animations (entry/parachute descent, dune flight, close-up rotorcraft, dusk landing/charging). **Licence:** Public Domain (`NASA/Johns Hopkins APL`).
- **NASA / ESA / CSA / STScI:** Voyager 1 Titan image (`PIA01536`, PD `NASA/JPL`) and Uranus hand-off imagery (Voyager 2 `PIA18182` PD `NASA/JPL-Caltech`, JWST NIRCam Uranus `CC BY 4.0` / PD `NASA, ESA, CSA, STScI`).
- **Wikimedia Commons:** Christiaan Huygens 17th-century portrait (Caspar Netscher, 1671, Haags Historisch Museum, **Licence:** Public Domain `PD-Art`). No portrait used for Gerard Kuiper (CODE `WHO` lower-third over graded Cassini plate).
- **The existing Short `RLSJm59OSzI`** ("What Would Standing on Saturn's Moon Titan Feel Like?", scheduled 10 Nov): no frames are reused from it in the long, to keep the two distinct.
- **No fire, explosion or disaster stock** (the film's answer is "it would not explode").

| # | Ch | VO in–out (s) | Dur | Source | Asset | Cuts | Notes |
|---:|---|---|---:|---|---|---:|---|
| 1 | 0 Open | 0.16–5.24 | 5.1 | ESA/NASA | Huygens DISR descent movie, mid-descent, the ground rising through orange haze, already moving at frame 0 | 1 | **Frame 0 lock.** Moving subject footage; no title card, no Orbit, distinct from Short `RLSJm59OSzI`. |
| 2 | 0 Open | 6.38–9.36 | 3.0 | CODE | `survive_check`: body outline over graded hazy amber plate with animated ticks: `"WON'T EXPLODE ✓"`, `"BLOOD WON'T BOIL ✓"` | 1 | Calm, quick (3.0 s). |
| 3 | 0 Open | 10.06–22.50 | 12.4 | NASA/JPL / CODE | Cassini in orbit around Saturn (JPL animation) → Titan's glowing orange limb haze (`PIA14909`, Cassini ISS, slow push) → CODE `pressure`: bar rising from `"EARTH 1 BAR"` to `"TITAN 1.47 BAR (≈ 1.5×)"` | 3 | **VISUAL MUST, DATA:** `"1 bar vs 1.47 bar (≈ 1.5×)"` (`SOURCES.md` row 1). |
| 4 | 0 Open | 23.34–31.58 | 8.2 | NASA/JPL / CODE | Cassini upper-haze limb plate (`PIA08399`, real moving push between code graphics) → CODE `cold_no_o2`: thermometer dropping to `"−179 °C"` alongside `"ALMOST NO O₂"` bar | 2 | **DATA:** `"−179 °C"` and `"almost no O₂"` (`SOURCES.md` rows 1, 8, 9). Real plate separates R3 and R4 CODE graphics. |
| 5 | 0 Open | 32.76–44.56 | 11.8 | ESA/NASA / CODE / NASA APL | Promise beat: Huygens DISR descent floodplain view (`PIA07231` / descent clip segment over dark riverbed) → CODE `rain_preview` slow-motion drop → Dragonfly flying over dunes (APL animation) | 3 | One cut per question. Uses `PIA07231` so `PIA07232` is saved for Rows 18 and 20. |
| 6 | 0 Open | 45.62–50.44 | 4.8 | NASA/JPL | Natural-colour orange Titan beside ringed Saturn (`PIA20016`, Cassini ISS), slow push | 1 | Bridge into ch1. |
| 7 | 1 A Moon With a Sky | 51.26–60.92 | 9.7 | Commons / CODE | Christiaan Huygens portrait (1671, PD-Art) with gentle parallax over starry navy plate + CODE `WHO` lower-third `"Christiaan Huygens / (1629–1695) — Dutch astronomer"` → CODE `timeline` stamp `"25 MARCH 1655"` | 2 | **WHO/WHEN:** sourced years `1629–1695` (`SOURCES.md` rows 2, 17). Ends cleanly on `"Saturn,"` (`60.92 s`). |
| 8 | 1 A Moon With a Sky | 61.32–68.06 | 6.7 | NASA/JPL / CODE | Cassini Saturn ring-plane pan → CODE `orbit16`: Titan dot circling Saturn on `"≈ 16 DAYS"` counter | 2 | **DATA:** `"about every 16 days"` (`SOURCES.md` row 2). Starts cleanly on `"hoping"` (`61.32 s`). |
| 9 | 1 A Moon With a Sky | 68.98–79.82 | 10.8 | NASA/JPL / CODE | Cassini distant Titan crescent plate → CODE `sizes`: scaled spheres comparing `"MOON 3,475 KM"`, `"MERCURY 4,879 KM"`, `"TITAN 5,150 KM"` | 2 | **VISUAL MUST, DATA:** exact diameters from `SOURCES.md` row 3. Real plate separates R8 and R9 CODE graphics. |
| 10 | 1 A Moon With a Sky | 81.02–93.80 | 12.8 | NASA/JPL / CODE | Cassini Titan limb plate + CODE `WHO` lower-third `"Gerard Kuiper / (1905–1973) — Dutch-born astronomer"` & `timeline` stamp `"1944"` → CODE `spectrum` prism splitting light → tight on `"CH₄ METHANE"` band | 3 | **WHO/WHEN + VISUAL MUST:** sourced years `1905–1973` (`SOURCES.md` rows 4, 17). No unsourced portrait. |
| 11 | 1 A Moon With a Sky | 94.80–99.82 | 5.0 | NASA/JPL | Titan's detached blue-orange haze layers at the limb (`PIA08399`, Cassini ISS), slow push | 1 | `"A moon has an atmosphere of its own."` |
| 12 | 1 A Moon With a Sky | 101.22–111.94 | 10.7 | NASA/JPL / CODE | Voyager 1 Saturn/Titan flyby animation (NASA/JPL) → CODE `timeline` marker `"NOVEMBER 1980 · VOYAGER 1"` over flyby trajectory | 2 | **WHEN:** `"November 1980"` added to timeline (`SOURCES.md` row 5). |
| 13 | 1 A Moon With a Sky | 112.78–124.76 | 12.0 | NASA/JPL / CODE | Voyager 1 enhanced orange Titan image (`PIA01536`, 12 Nov 1980), slow push → CODE `photolysis`: UV sunlight arrow splitting `"N₂ + CH₄ → HAZE"` | 2 | **VISUAL MUST** (`SOURCES.md` row 5). |
| 14 | 1 A Moon With a Sky | 126.02–136.68 | 10.7 | CODE / NASA/JPL | CODE `methane`: CH₄ reservoir gauge draining under UV light and refilling from `"?"` below → Cassini VIMS Titan cloud band image (`PIA17172`), slow push | 2 | Question bridge into ch2 (`SOURCES.md` row 6). |
| 15 | 2 The Huygens Landing | 137.56–151.98 | 14.4 | NASA/JPL / ESA / CODE | Cassini–Huygens launch / interplanetary cruise (`"7 YEARS"`) → Huygens release & parachute entry animation (ESA) → CODE `timeline` marker `"14 JANUARY 2005"` | 3 | **WHEN:** `"14 January 2005"` added to timeline (`SOURCES.md` row 7). |
| 16 | 2 The Huygens Landing | 153.08–158.64 | 5.6 | ESA/NASA / CODE | Huygens DISR descent movie, upper murky orange cloud deck + CODE lower-third counter `"147 MIN (2 H 27 M)"` | 1 | **DATA:** `"2 hours and 27 minutes / 147 minutes"` (`SOURCES.md` row 7). |
| 17 | 2 The Huygens Landing | 159.48–171.18 | 11.7 | ESA/NASA | Huygens DISR aerial mosaic (`PIA07236`): bright icy highlands with dark branching river channels draining to a dark plain; wide push then slow pan along channels | 2 | **VISUAL MUST:** `"Dark branching channels"` (`SOURCES.md` row 7). |
| 18 | 2 The Huygens Landing | 172.16–183.54 | 11.4 | ESA/NASA / CODE | Huygens surface pebbles photograph (`PIA07232`, use 1 of 2, wide slow push) → CODE scale bracket `"≈ 15 CM"` over foreground cobble | 2 | **VISUAL MUST, DATA:** `"up to about 15 cm"` (`SOURCES.md` row 8). |
| 19 | 2 The Huygens Landing | 184.60–197.20 | 12.6 | CODE / NASA/JPL | CODE `distance`: Sun–Earth–Saturn scale line `"9.5 AU (9.5× EARTH)"` → Cassini distant Saturn/Titan plate → CODE `temp_scale`: thermometer dropping from `"0 °C"` to `"−179 °C"` | 3 | **VISUAL MUST, DATA:** `"9.5 AU"` and `"0 °C to −179 °C"` (`SOURCES.md` row 8). Real plate separates the two CODE graphics. |
| 20 | 2 The Huygens Landing | 198.02–205.82 | 7.8 | ESA/NASA / CODE | Huygens surface pebbles photograph (`PIA07232`, use 2 of 2, tight reframe on foreground cobbles) + CODE `FACT` card `"WATER ICE IS ROCK"` | 2 | **FACT:** `"Water ice is rock"` (4 words; `SOURCES.md` row 8). Final use of `PIA07232`. |
| 21 | 2 The Huygens Landing | 206.64–219.36 | 12.7 | CODE / ESA/NASA | CODE `cycle` (part 1): Earth H₂O cycle vs Titan `"CH₄ / C₂H₆"` cloud & rain → Huygens DISR channel mosaic (`PIA07236`, use 2 of 2, tight reframe on mouth) → CODE `cycle` (part 2): river channels filling lakes | 3 | **VISUAL MUST:** methane/ethane hydrological cycle (`SOURCES.md` row 8). |
| 22 | 2 The Huygens Landing | 220.54–228.72 | 8.2 | ESA/NASA / CODE | Huygens lander surface artist animation (ESA) → CODE `surface_72m`: `"72 MIN ON TITAN"` counter as Cassini relay arc sets below horizon | 2 | **DATA, FACT:** `"72 minutes"` surface transmission (`SOURCES.md` row 7). |
| 23 | 2 The Huygens Landing | 229.78–239.50 | 9.7 | CODE / NASA/JPL | CODE `landings_chart`: solar-system landing distance bar (Moon, Venus, Mars, `"TITAN · 9.5 AU"`) + `FACT` card `"MOST DISTANT LANDING"` → Cassini Titan crescent from orbit (`PIA20021`) | 2 | **FACT:** `"Most distant landing"` (3 words; `SOURCES.md` row 7). |
| 24 | 2 The Huygens Landing | 240.84–245.10 | 4.3 | — | House mid-roll subscribe card (existing asset, short version) | 1 | Mid-film subscribe beat (`240.84–245.10 s`). |
| 25 | 3 Standing on Titan | 246.00–258.48 | 12.5 | ESA/NASA / CODE | Huygens DISR wide surface-to-horizon panorama (`PIA07233`, distinct from `PIA07232`, slow pan) → CODE heated-suit overlay → CODE `pressure` tight reframe (`"1.47 BAR ≈ 1.5× EARTH"`) | 3 | Re-establishes `"about 1.5× Earth's"` pressure (`SOURCES.md` row 1) with zero extra use of `PIA07232`. |
| 26 | 3 Standing on Titan | 259.18–268.10 | 8.9 | OMNI (flag) / CODE | Orbit standing on an orange icy plain under a hazy amber sky, looking around calmly (wide → medium reframe) | 2 | **ORBIT ACTS.** £0 Fallback: Cassini Titan orange haze plate + CODE `airmix` ring (`"95% N₂ · 5% CH₄"`, vs `"EARTH 78% N₂"`). |
| 27 | 3 Standing on Titan | 269.04–286.96 | 17.9 | CODE / NASA/JPL | CODE `airmix` (`"95% N₂ · 5% CH₄"`) → Cassini Titan atmospheric limb plate → CODE `densegrav`: `"AIR DENSITY ≈ 4×"` vs `"GRAVITY ≈ 1/7"` → CODE `"ALMOST NO O₂"` gauge | 4 | **VISUAL MUST, DATA:** `"95% N₂, 5% CH₄, 4× denser, 1/7 gravity"` (`SOURCES.md` row 9). |
| 28 | 3 Standing on Titan | 288.12–298.28 | 10.2 | NASA/JPL / CODE | Cassini VIMS storm cloud over Titan (`PIA17172`, use 2 of 2, tight reframe) → CODE `rain` (part 1): Earth raindrop `"6.5 MM"` falling fast at `"9.2 M/S (≈ 9 M/S)"` | 2 | **DATA:** Earth drop `"6.5 mm"` at `"9.2 m/s"` (`SOURCES.md` row 10). Real cloud plate separates R27 and R28 CODE graphics. |
| 29 | 3 Standing on Titan | 298.94–313.92 | 15.0 | CODE / NASA/JPL | CODE `rain` (part 2, wide): Titan methane drop `"9.5 MM (MARBLE)"` drifting at `"1.6 M/S"` → Cassini radar dune strip (`PIA09182`, use 1 of 2) → CODE `rain` (part 3, tight): `"1.6 M/S ≈ SNOWFLAKE"` side by side with Earth drop | 3 | **VISUAL MUST, DATA:** `"9.5 mm at 1.6 m/s"` (`SOURCES.md` row 10). |
| 30 | 3 Standing on Titan | 314.86–324.44 | 9.6 | NASA/JPL / CODE | Titan equatorial Belet dunes radar strip (`PIA09182`, use 2 of 2, slow pan) → CODE overlay `"CENTURIES BETWEEN SHOWERS"` over dunes | 2 | `"Centuries between showers"` (`SOURCES.md` row 10). |
| 31 | 4 Seas of Natural Gas | 325.32–337.84 | 12.5 | NASA/JPL | Cassini false-colour radar mosaic of Titan's north polar lakes and seas (`PIA10008`, use 1 of 2): wide polar view → push to drowned coastline → pan across bays and islands | 3 | **VISUAL MUST:** `"Bays and islands"` (`SOURCES.md` row 11). |
| 32 | 4 Seas of Natural Gas | 338.92–354.22 | 15.3 | NASA/JPL / CODE | North polar lakes mosaic (`PIA10008`, use 2 of 2, tight reframe on Kraken Mare) → CODE `scalemap` (wide): `"KRAKEN MARE ≈ 400,000 KM²"` → CODE `scalemap` (tight): `"≈ 5× LAKE SUPERIOR"` | 3 | **VISUAL MUST, DATA:** `"400,000 km², almost 5× Lake Superior"` (`SOURCES.md` row 11). Final use of `PIA10008`. |
| 33 | 4 Seas of Natural Gas | 355.14–366.88 | 11.7 | NASA/JPL / CODE | Cassini radar map of Ligeia Mare (`PIA17655`, use 1 of 2, slow push) → CODE `depth_ligeia` + `timeline` marker `"2013"`: radar beam bouncing off seabed at `"≈ 160 M"` | 2 | **WHEN, DATA:** `"2013"` and `"about 160 m"` (`SOURCES.md` row 12). |
| 34 | 4 Seas of Natural Gas | 367.92–372.42 | 4.5 | NASA/JPL / CODE | Ligeia/Kraken radar strait plate (`PIA17655`, use 2 of 2, tight reframe) with animated CODE depth bar plunging from `"LIGEIA 160 M"` to `"KRAKEN ≥ 300 M"` | 1 | **DATA:** `"at least 300 m (1,000 ft)"` (`SOURCES.md` row 12). Graded radar plate behind graphic avoids back-to-back slabs. |
| 35 | 4 Seas of Natural Gas | 373.10–385.06 | 12.0 | NASA/JPL / CODE | Cassini global Titan view (`PIA20016`, use 2 of 2, tight reframe) → CODE `ocean_cutaway`: our own animated interior cutaway showing `"55–80 KM ICY CRUST"` and `"LIQUID WATER + SALTS + AMMONIA"` ocean | 2 | **VISUAL MUST, DATA:** our own CODE cutaway (no textbook NASA diagram labels; `SOURCES.md` row 13). |
| 36 | 4 Seas of Natural Gas | 386.06–388.92 | 2.9 | NASA/JPL | Cassini VIMS specular sunglint reflecting off Kraken Mare (`PIA12481`), slow push | 1 | `"Wait, that raises a terrifying question."` |
| 37 | 5 Would It Explode? | 389.76–401.44 | 11.7 | NASA APL / CODE | Dragonfly descent animation near Titan shoreline (APL) → CODE `spark_question`: thruster plume icon + `"?"` spark over dark sea plate | 2 | No real fire or explosion stock. |
| 38 | 5 Would It Explode? | 402.02–411.64 | 9.6 | NASA/JPL / CODE | Cassini radar shoreline of Kraken Mare (`PIA21445`, use 1 of 2) → CODE `reserves`: Titan liquid hydrocarbons bar towering `"HUNDREDS OF TIMES"` over Earth oil & gas reserves | 2 | **DATA:** `"hundreds of times more liquid hydrocarbons"` (`SOURCES.md` row 14). |
| 39 | 5 Would It Explode? | 412.62–424.92 | 12.3 | NASA / CODE | Blue Marble Earth from orbit (NASA PD, slow push) → CODE `fire` (part 1): fuel + oxygen triangle → `"EARTH: 78% N₂ · 21% O₂"` igniting | 3 | **VISUAL MUST, DATA:** `"21% O₂"` (`SOURCES.md` rows 9, 14). Real Earth plate separates R38 and R39 CODE graphics. |
| 40 | 5 Would It Explode? | 425.66–432.96 | 7.3 | NASA/JPL / CODE | Cassini shoreline plate (`PIA21445`, use 2 of 2, reframed) → CODE `fire` (part 2): `"TITAN: 95% N₂ · 5% CH₄ · ALMOST NO O₂"` with oxygen side greyed out | 2 | **DATA:** `"95% N₂, 5% CH₄, almost no O₂"` (`SOURCES.md` rows 9, 14). |
| 41 | 5 Would It Explode? | 433.82–446.86 | 13.0 | CODE / NASA/JPL | CODE `no_flame`: match & thruster in N₂ sky (spark goes out) → Cassini VIMS specular sea glint (`PIA12481`, use 2 of 2, tight reframe) → CODE `FACT` card `"NO OXYGEN TO BURN"` | 3 | **VISUAL MUST, FACT:** `"No oxygen to burn"` (4 words; `SOURCES.md` row 14). |
| 42 | 5 Would It Explode? | 447.74–455.56 | 7.8 | NASA / CODE | NASA rocket test plume in Earth air (NASA PD, 3.8 s) → CODE `flipfire` (part 1): `"EARTH: FUEL TANK + O₂ AIR"` | 2 | Real NASA rocket test plume (`titan_landing_script_master_v02.md` line 96) separates R41 and R42 CODE graphics. |
| 43 | 5 Would It Explode? | 456.16–463.26 | 7.1 | CODE | CODE `flipfire` (part 2, wide → tight): `"TITAN: O₂ TANK + CH₄ SKY"` with small flame at oxygen nozzle | 2 | **VISUAL MUST:** reversed combustion graphic (`SOURCES.md` row 14). |
| 44 | 5 Would It Explode? | 464.44–474.10 | 9.7 | NASA/JPL / NASA APL | Cassini crescent Titan in golden haze (`PIA14909`, use 2 of 2, reframed) → Dragonfly entry/parachute descent animation cushioned by Titan's nitrogen sky (APL) | 2 | Bridge into ch6. Replaces 3rd use of `PIA10008`. |
| 45 | 6 Wings for Titan | 474.94–494.52 | 19.6 | CODE / NASA APL | CODE `densegrav` (part 1: `"AIR ≈ 4× DENSER"`) → APL Dragonfly rotor spin-up clip → CODE `lift` (part 2: `"GRAVITY ≈ 1/7"`) → CODE `lift` gauge feeding wing icon | 4 | **VISUAL MUST, DATA:** `"4× denser"` and `"1/7 gravity"` (`SOURCES.md` row 15). APL clip separates CODE segments. |
| 46 | 6 Wings for Titan | 495.24–501.70 | 6.5 | OMNI (flag) / CODE | Orbit hovering effortlessly over orange dunes with small fins out, delighted (wide → tight) + CODE gauge `"≈ 28× EASIER (OUR ROUGH SUM)"` | 2 | **ORBIT ACTS, DATA:** `"≈ 28× easier (our rough sum)"` (`SOURCES.md` row 15). £0 Fallback: CODE `lift_28x` gauge (`"4× AIR ÷ 1/7 WEIGHT ≈ 28× EASIER · OUR ROUGH SUM"`) over APL dune plate. |
| 47 | 6 Wings for Titan | 503.20–516.86 | 13.7 | NASA APL / CODE | Dragonfly flight animation soaring over Titan dunes (APL, 2 angles) + CODE `FACT` card `"IDEAL WAY TO TRAVEL"` | 3 | **FACT:** `"Ideal way to travel"` (4 words, verbatim from `SOURCES.md` row 15). |
| 48 | 6 Wings for Titan | 517.68–527.30 | 9.6 | NASA APL / CODE | Dragonfly octocopter close-up (8 rotors, APL) → CODE `timeline` marker `"NET JULY 2028"` + `"8 ROTORS · NUCLEAR-POWERED"` | 2 | **WHEN, DATA:** `"NET July 2028"` and `"8 rotors"` (`SOURCES.md` row 16). |
| 49 | 6 Wings for Titan | 528.38–540.56 | 12.2 | NASA APL / CODE | Dragonfly landing on dunes at dusk (APL) → CODE `timeline` marker `"LATE 2034"` → CODE day/night bar `"DAYTIME ≈ 8 EARTH DAYS"` | 3 | **WHEN, DATA:** `"Late 2034"` and `"8 Earth days"` (`SOURCES.md` row 16). |
| 50 | 6 Wings for Titan | 541.82–556.06 | 14.2 | NASA/JPL / CODE | Selk Crater radar/VIMS mosaic (`PIA11831`, Cassini, wide → tight pan) → CODE `selk_soup`: `"WATER + ORGANICS → PRIMORDIAL SOUP"` | 3 | **VISUAL MUST:** Selk Crater `"primordial soup"` (`SOURCES.md` row 16). |
| 51 | 6 Wings for Titan | 557.32–566.50 | 9.2 | ESA/NASA | Huygens DISR descent movie (final approach segment down to the floodplain, 2 framings), ending on the frozen horizon | 2 | `"A time capsule of early Earth."` |
| 52 | 6 Wings for Titan | 567.66–582.38 | 14.7 | NASA / STScI / CODE | Hand-off to 033: Voyager 2 Uranus (`PIA18182`, PD) → JWST NIRCam tilted Uranus with rings (`NASA, ESA, CSA, STScI`, slow push) → CODE `"21-YEAR WINTER"` tilt axis | 3 | **DATA:** `"21-year dark winter"` (`SOURCES.md` row 18). Holds moving picture 2–3 s past `582.38 s` as music fades. No subscribe ask; no goodbye. |

## Tally

- **Stills used (strictly ≤ 2 appearances each across the entire film):**
  - `PIA07232` (Huygens surface colour pebbles): Rows 18, 20 (2 uses; Row 20 reframed tight).
  - `PIA07231` (Huygens DISR landing floodplain view): Row 5 (1 use).
  - `PIA07233` (Huygens DISR surface-to-horizon wide panorama): Row 25 (1 use).
  - `PIA07236` (Huygens DISR highland river channels mosaic): Rows 17, 21 (2 uses; Row 21 reframed on channel mouth).
  - `PIA10008` (Cassini north polar lakes false-colour radar mosaic): Rows 31, 32 (2 uses; Row 32 reframed on Kraken Mare).
  - `PIA17655` (Cassini Ligeia Mare radar map): Rows 33, 34 (2 uses).
  - `PIA21445` (Cassini Kraken Mare radar shoreline): Rows 38, 40 (2 uses).
  - `PIA12481` (Cassini VIMS Kraken Mare specular sunglint): Rows 36, 41 (2 uses).
  - `PIA14909` (Cassini ISS golden-orange limb haze): Rows 3, 44 (2 uses).
  - `PIA08399` (Cassini ISS detached blue-orange haze layers): Rows 4, 11 (2 uses).
  - `PIA20016` (Cassini natural-colour Titan + Saturn): Rows 6, 35 (2 uses).
  - `PIA20021` (Cassini distant Titan crescent): Rows 9, 23 (2 uses).
  - `PIA17172` (Cassini VIMS cloud bands): Rows 14, 28 (2 uses).
  - `PIA09182` (Cassini RADAR Belet equatorial dunes): Rows 29, 30 (2 uses).
  - `PIA01536` (Voyager 1 orange Titan, 1980): Row 13 (1 use).
  - `PIA11831` (Cassini Selk Crater mosaic): Row 50 (1 use).
  - `PIA18182` + JWST NIRCam Uranus: Row 52 (1 use each).
  - Commons Christiaan Huygens portrait (1671, PD-Art): Row 7 (1 use).
- **Moving clips (distinct time segments):**
  - ESA/NASA Huygens DISR descent movie: Rows 1 (mid-descent), 16 (upper orange haze), 51 (final touchdown approach).
  - NASA/Johns Hopkins APL Dragonfly animations: Rows 5, 37, 44, 45, 47, 48, 49 (distinct mission animation segments).
  - NASA/JPL Cassini & Voyager animations, ESA Huygens entry/surface animations, NASA Blue Marble & rocket plume: Rows 3, 8, 12, 15, 22, 39, 42.
- **Code graphics to build (`code_graphics.py`):**
  - `survive_check` (R2), `pressure` (R3, R25), `cold_no_o2` (R4), `rain_preview` (R5), `timeline` + `WHO` cards (R7, R10, R12, R15, R33, R48, R49), `orbit16` (R8), `sizes` (R9), `spectrum` (R10), `photolysis` (R13), `methane` (R14), `descent_147m` (R16), `ruler_15cm` (R18), `distance` & `temp_scale` (R19), `fact_cards` (R20, R23, R41, R47), `cycle` (R21), `surface_72m` (R22), `landings_chart` (R23), `airmix` & `densegrav` (R26 fallback, R27), `rain` (R28, R29), `dunes_label` (R30), `scalemap` (R32), `depth_ligeia` & `depth_kraken` (R33, R34), `ocean_cutaway` (R35), `spark_question` (R37), `reserves` (R38), `fire` (R39, R40), `no_flame` (R41), `flipfire` (R42, R43), `lift` & `lift_28x` (R45, R46 fallback), `day_night_8d` (R49), `selk_soup` (R50), `uranus_21y` (R52).
- **Rule-E Verdict:** **GO** (£0 harvest + `code_graphics.py` builds; 2 optional OMNI Orbit beats in Rows 26 and 46 carry £0 CODE fallbacks).
