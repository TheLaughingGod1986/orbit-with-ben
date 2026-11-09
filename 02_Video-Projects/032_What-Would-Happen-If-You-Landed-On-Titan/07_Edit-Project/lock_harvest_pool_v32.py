#!/usr/bin/env python3
"""Lock Step 2 of 4 for J2089 under CHIEF_SCOPE_v31.md:
- Writes SHOT_LIST_v08.md with the 52-row £0 allocation (<=2 uses per still, <=3 stretches per SVS clip)
- Updates HARVEST_POOL_v01.json with full SHA-256 provenance, dimensions, credits, and source evidence
- Verifies all invariants (<=2 uses per still, <=5 stretches per video, 0 excluded Short assets, 0 excluded sources in active rows)
"""
import hashlib
import json
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
NAS_SVS = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "032_What-Would-Happen-If-You-Landed-On-Titan/03_Reference-Material/"
    "harvest_J2089_v01/svs_20311"
)
NAS_REF = NAS_SVS.parent


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


SHOT_LIST_V08 = """# 032 What Would Happen If You Landed on Titan? — SHOT_LIST v08

7 Nov 2026 · J2089 Step 2/4 lock under `jobs/reviews/J2089/CHIEF_SCOPE_v31.md` (£0 harvest + 62 preserved `code_graphics.py` / overlay exports).
Supersedes `SHOT_LIST_v07.md`. The locked VO, all 52 row word spans, durations, and cut counts are unchanged.

## Locked Allocation Summary (`CHIEF_SCOPE_v31.md`)
- **Zero spend (£0):** All 62 existing `code_graphics.py` / DATA / mechanism / process / real-body overlays in `CURRENT_EXPORT_INVENTORY_v31.json` are preserved unchanged.
- **Excluded / retired sources (0 active appearances):** `huygens_descent.wmv` (reconstructed ESA movie), `dragonfly_at_titan.mp4` (`dragonfly.jhuapl.edu` gallery clip without NASA media release), `PIA07870`, `PIA07871`, `PIA10008` (multi-panel collision diagram), `PIA07233`, `PIA16638`, `PIA19051`, and all Short `RLSJm59OSzI` / `ffYKoNVPoqg` assets (`PIA14925`, `PIA06230`, `PIA09739`, `PIA21625`).
- **Dragonfly rows (`R05`, `R37`, `R44`, `R45`, `R46`, `R47`, `R48`, `R49`, `R50`):** Allocated to NASA Goddard Scientific Visualization Studio release **SVS 20311** (`https://svs.gsfc.nasa.gov/20311`, Credit: `NASA/Johns Hopkins APL/Goddard Space Flight Center`) and NASA's official Dragonfly mission page (`https://science.nasa.gov/mission/dragonfly/`, `NASA_Dragonfly_BannerFactSheet_2024.jpg`, Credit: `NASA/Johns Hopkins APL/Steve Gribben`).
- **North polar seas (`R31`, `R32`):** Allocated to `PIA20021_right_panel` (`1440×1144` right-panel crop `(420, 36, 1860, 1180)` of `PIA20021.jpg` with all left-strip insets and border wedges excluded) paired with `PIA17031` (`R31`, `R33`).
- **Reuse caps:** Every still has `≤ 2` appearances across Rows 1–52; every SVS video clip has `≤ 3` stretches separated by `> 10 s`.

| # | Ch | VO in–out (s) | Dur | Source | Asset | Cuts | Notes |
|---:|---|---|---:|---|---|---:|---|
| 1 | 0 Open | 0.16–5.24 | 5.1 | NASA/JPL | Graded multi-plane atmospheric descent push through Titan's golden haze (`PIA20016`, use 1 of 2, 0.0–2.6 s) → upper-haze limb drift (`PIA08167`, use 1 of 2, 2.6–5.1 s), already moving at frame 0 | 2 | **Frame 0 lock (`CHIEF_SCOPE_v31.md` §1).** Continuous moving multi-plane composite; no title card, no Orbit, distinct from Short `RLSJm59OSzI`/`ffYKoNVPoqg`. |
| 2 | 0 Open | 6.38–9.36 | 3.0 | CODE | `survive_check`: body outline over graded hazy amber plate with animated ticks: `"WON'T EXPLODE ✓"`, `"BLOOD WON'T BOIL ✓"` | 1 | Calm, quick (3.0 s). |
| 3 | 0 Open | 10.06–22.50 | 12.4 | NASA/JPL / CODE | Cassini in orbit above Saturn's backlit rings (`PIA22766`, use 1 of 2, slow push) → Titan's glowing orange limb haze (`PIA21902`, use 1 of 2, slow push) → CODE `pressure`: bar rising from `"EARTH 1 BAR"` to `"TITAN 1.47 BAR (≈ 1.5×)"` | 3 | **VISUAL MUST, DATA:** `"1 bar vs 1.47 bar (≈ 1.5×)"` (`SOURCES.md` row 1). |
| 4 | 0 Open | 23.34–31.58 | 8.2 | NASA/JPL / CODE | Cassini upper-haze limb plate (`PIA08167`, use 2 of 2, reframed push between code graphics) → CODE `cold_no_o2`: thermometer dropping to `"−179 °C"` alongside `"ALMOST NO OXYGEN"` bar | 2 | **DATA:** `"−179 °C"` and `"almost no O₂"` (`SOURCES.md` rows 1, 8, 9). Real plate separates R3 and R4 CODE graphics. |
| 5 | 0 Open | 32.76–44.56 | 11.8 | ESA/NASA / CODE / NASA APL | Promise beat: Huygens DISR descent floodplain view (`PIA07231`, use 1 of 2, inset `≤2.0×` over graded moving plate) → CODE `rain_preview` slow-motion drop → Dragonfly soaring over Titan dunes (`NASA_Dragonfly_BannerFactSheet_2024`, use 1 of 2, slow pan) | 3 | One cut per question. Uses `PIA07231` (`≤2.0×` inset) and `science.nasa.gov` Dragonfly banner (`NASA/Johns Hopkins APL/Steve Gribben`). |
| 6 | 0 Open | 45.62–50.44 | 4.8 | NASA/JPL | Natural-colour orange Titan beside ringed Saturn (`PIA14922`, use 1 of 2, Cassini ISS, natural colour), slow push | 1 | Bridge into ch1. |
| 7 | 1 A Moon With a Sky | 51.26–60.92 | 9.7 | Commons / CODE | Christiaan Huygens portrait (`huygens_portrait_1671`, use 1 of 1, PD-Art) with gentle parallax over starry navy plate + CODE `WHO` lower-third `"Christiaan Huygens / (1629–1695) — Dutch astronomer"` → CODE `timeline` stamp `"25 MARCH 1655"` | 2 | **WHO/WHEN:** sourced years `1629–1695` (`SOURCES.md` rows 2, 17). Ends cleanly on `"Saturn,"` (`60.92 s`). |
| 8 | 1 A Moon With a Sky | 61.32–68.06 | 6.7 | NASA/JPL / CODE | Cassini Saturn ring-plane plate (`PIA14922`, use 2 of 2, reframed) → reviewed `r08_orbit_period` real-photo period graphic (J2262) | 2 | **DATA:** `"about every 16 days"` (`SOURCES.md` row 2). Starts cleanly on `"hoping"` (`61.32 s`). |
| 9 | 1 A Moon With a Sky | 68.98–79.82 | 10.8 | NASA/JPL / CODE | Cassini distant Titan crescent plate (`PIA08733`, use 1 of 2) → CODE `r09_sizes` (J2247): real-photo scaled bodies, Titan `PIA14602` (use 1 of 2) / Mercury `PIA15162` (use 1 of 1) / Moon `PIA00405` (use 1 of 1); comparing `"MOON 3,475 KM"`, `"MERCURY 4,879 KM"`, `"TITAN 5,150 KM"` | 2 | **VISUAL MUST, DATA:** exact diameters from `SOURCES.md` row 3. Real plate separates R8 and R9 CODE graphics. |
| 10 | 1 A Moon With a Sky | 81.02–93.80 | 12.8 | NASA/JPL / CODE | Cassini Saturn/Titan backlit panorama (`PIA17172`, use 1 of 2, wide crop pan) + CODE `WHO` lower-third `"Gerard Kuiper / (1905–1973) — Dutch-born astronomer"` & `timeline` stamp `"1944"` → CODE `spectrum` prism splitting light → tight on `"CH₄ METHANE"` band | 3 | **WHO/WHEN + VISUAL MUST:** sourced years `1905–1973` (`SOURCES.md` rows 4, 17). No unsourced portrait. |
| 11 | 1 A Moon With a Sky | 94.80–99.82 | 5.0 | NASA/JPL | Titan's detached blue-orange haze layers at the limb (`PIA21902`, use 2 of 2, reframed Cassini ISS push) | 1 | `"A moon has an atmosphere of its own."` |
| 12 | 1 A Moon With a Sky | 101.22–111.94 | 10.7 | NASA/JPL / CODE | Voyager 1 orange Titan flyby view (`PIA02238`, use 1 of 2, inset `≤1.55×` over graded moving plate, wide framing) → CODE `timeline` marker `"NOVEMBER 1980 · VOYAGER 1"` over flyby trajectory | 2 | **WHEN:** `"November 1980"` added to timeline (`SOURCES.md` row 5). |
| 13 | 1 A Moon With a Sky | 112.78–124.76 | 12.0 | NASA/JPL / CODE | Voyager 1 enhanced orange Titan image (`PIA02238`, use 2 of 2, inset `≤1.55×` over graded moving plate, reframed, caption `"VOYAGER 1 · 1980"`) → CODE `photolysis`: UV sunlight arrow splitting `"N₂ + CH₄ → HAZE"` | 2 | **VISUAL MUST** (`SOURCES.md` row 5). J2090: inset only, `≤1.55×` native size, over graded moving plate. |
| 14 | 1 A Moon With a Sky | 126.02–136.68 | 10.7 | CODE / NASA/JPL | CODE `methane`: CH₄ reservoir gauge draining under UV light and refilling from `"?"` below → Cassini VIMS Titan cloud band image (`PIA21450`, use 1 of 2, slow push) | 2 | Question bridge into ch2 (`SOURCES.md` row 6). |
| 15 | 2 The Huygens Landing | 137.56–151.98 | 14.4 | NASA/JPL / ESA / CODE | Cassini–Huygens Titan IV launch (`PIA01050`, use 1 of 1, `"7 YEARS"`) → Huygens DISR descent terrain inset (`PIA07231`, use 2 of 2, reframed inset `≤2.0×`) → CODE `timeline` marker `"14 JANUARY 2005"` | 3 | **WHEN:** `"14 January 2005"` added to timeline (`SOURCES.md` row 7). |
| 16 | 2 The Huygens Landing | 153.08–158.64 | 5.6 | NASA/JPL / CODE | Graded moving Cassini Titan cloud/haze plate (`PIA21610`, use 1 of 2) + reviewed CODE `r16_descent_147m` counter `"147 MIN (2 H 27 M)"` (`032_r16_cassini_counter_draft_v01.mp4`) | 1 | **DATA:** `"2 hours and 27 minutes / 147 minutes"` (`SOURCES.md` row 7). Approved `KEEP` under `CHIEF_SCOPE_v31.md` §1 (`J2363`). |
| 17 | 2 The Huygens Landing | 159.48–171.18 | 11.7 | ESA/NASA | Huygens DISR aerial mosaic (`PIA07236`, use 1 of 2): bright icy highlands with dark branching river channels draining to a dark plain; wide push then slow pan along channels | 2 | **VISUAL MUST:** `"Dark branching channels"` (`SOURCES.md` row 7). |
| 18 | 2 The Huygens Landing | 172.16–183.54 | 11.4 | ESA/NASA / CODE | Huygens surface pebbles photograph (`PIA07232`, use 1 of 2, inset `≤1.43×` over graded moving plate, wide slow push) → CODE scale bracket `"≈ 15 CM"` over foreground cobble (`J2331` KEEP) | 2 | **VISUAL MUST, DATA:** `"up to about 15 cm"` (`SOURCES.md` row 8). |
| 19 | 2 The Huygens Landing | 184.60–197.20 | 12.6 | CODE / NASA/JPL | Reviewed CODE `r19_distance`: linear 1 AU / 9.5 AU comparison over `PIA14909` (use 1 of 2, J2260) → Cassini Saturn/Titan backlit ring plate (`PIA22766`, use 2 of 2, reframed pan) → CODE `temp_scale`: thermometer dropping from `"0 °C"` to `"−179 °C"` | 3 | **VISUAL MUST, DATA:** `"9.5 AU"` and `"0 °C to −179 °C"` (`SOURCES.md` row 8). Real plate `PIA22766` separates the two CODE graphics. |
| 20 | 2 The Huygens Landing | 198.02–205.82 | 7.8 | ESA/NASA / CODE | Huygens surface pebbles photograph (`PIA07232`, use 2 of 2, tight reframe within `≤1.43×` inset cap) + CODE `FACT` card `"WATER ICE IS ROCK"` | 2 | **FACT:** `"Water ice is rock"` (4 words; `SOURCES.md` row 8). Final use of `PIA07232`. |
| 21 | 2 The Huygens Landing | 206.64–219.36 | 12.7 | CODE / ESA/NASA | CODE `cycle` (part 1): Earth H₂O cycle vs Titan `"CH₄ / C₂H₆"` cloud & rain → Huygens DISR channel mosaic (`PIA07236`, use 2 of 2, tight reframe on mouth) → CODE `cycle` (part 2): river channels filling lakes | 3 | **VISUAL MUST:** methane/ethane hydrological cycle (`SOURCES.md` row 8). |
| 22 | 2 The Huygens Landing | 220.54–228.72 | 8.2 | NASA/JPL / CODE | Cassini Titan golden haze crescent (`PIA21445`, use 1 of 2, slow push) → CODE `surface_72m`: `"72 MIN ON TITAN"` counter as Cassini relay arc sets below horizon | 2 | **DATA, FACT:** `"72 minutes"` surface transmission (`SOURCES.md` row 7). |
| 23 | 2 The Huygens Landing | 229.78–239.50 | 9.7 | NASA/JPL / CODE | Graded moving Cassini Titan crescent plate (`PIA08733`, use 2 of 2, reframed) + reviewed CODE `r23_landing_record` (`032_r23_composite_preview_v02.mp4`, J2304/J2346): qualitative `"MOST DISTANT LANDING · HUYGENS · FROM EARTH → TITAN · NOT TO SCALE"` connector with `PIA14909` (use 2 of 2, native 408×408 crop) | 2 | **FACT:** `"Most distant landing"` (`SOURCES.md` row 7). Approved `KEEP` under `CHIEF_SCOPE_v31.md` §3 (`J2346`). |
| 24 | 2 The Huygens Landing | 240.84–245.10 | 4.3 | — | House mid-roll subscribe card (existing asset, short version) | 1 | Mid-film subscribe beat (`240.84–245.10 s`). |
| 25 | 3 Standing on Titan | 246.00–258.48 | 12.5 | NASA/JPL / CODE | 246.00–250.20: reviewed `r25_heated_suit` over graded moving `PIA17163` (use 1 of 2) → 250.20–254.68: real moving `PIA21450` (use 2 of 2) → 254.68–258.48: reviewed `r25_pressure` over continuing plate | 3 | Re-establishes `"about 1.5× Earth's"` pressure (`SOURCES.md` row 1) with J2177 plate allocation. |
| 26 | 3 Standing on Titan | 259.18–268.10 | 8.9 | NASA/JPL / CODE | £0 Fallback (`CHIEF_SCOPE_v31.md`): Cassini Titan orange haze plate (`PIA21445`, use 2 of 2, reframed pan) + CODE `airmix` ring (`"95% N₂ · 5% CH₄"`, vs `"EARTH 78% N₂"`) | 2 | **£0 Fallback active.** No Omni spend. |
| 27 | 3 Standing on Titan | 269.04–286.96 | 17.9 | CODE / NASA/JPL | CODE `airmix` (`"95% N₂ · 5% CH₄"`) → Cassini Saturn/Titan atmospheric limb plate (`PIA17172`, use 2 of 2, reframed crop on Titan limb) → CODE `densegrav`: `"AIR DENSITY ≈ 4×"` vs `"GRAVITY ≈ 1/7"` → CODE `"ALMOST NO O₂"` gauge | 4 | **VISUAL MUST, DATA:** `"95% N₂, 5% CH₄, 4× denser, 1/7 gravity"` (`SOURCES.md` row 9). |
| 28 | 3 Standing on Titan | 288.12–298.28 | 10.2 | NASA/JPL / CODE | Cassini VIMS storm cloud over Titan (`PIA21610`, use 2 of 2, tight reframe) → CODE `rain` (part 1): Earth raindrop `"6.5 MM"` falling fast at `"9.2 M/S (≈ 9 M/S)"` | 2 | **DATA:** Earth drop `"6.5 mm"` at `"9.2 m/s"` (`SOURCES.md` row 10). Real cloud plate separates R27 and R28 CODE graphics. |
| 29 | 3 Standing on Titan | 298.94–313.92 | 15.0 | CODE / NASA/JPL | CODE `rain` (part 2, wide): Titan methane drop `"9.5 MM (MARBLE)"` drifting at `"1.6 M/S"` → Cassini radar dune strip (`PIA09182`, use 1 of 2, left/centre window) → CODE `rain` (part 3, tight): `"1.6 M/S ≈ SNOWFLAKE"` side by side with Earth drop | 3 | **VISUAL MUST, DATA:** `"9.5 mm at 1.6 m/s"` (`SOURCES.md` row 10). |
| 30 | 3 Standing on Titan | 314.86–324.44 | 9.6 | NASA/JPL / CODE | Titan equatorial Belet dunes radar strip (`PIA09182`, use 2 of 2, right-window pan) → CODE overlay `"CENTURIES BETWEEN SHOWERS"` over dunes | 2 | `"Centuries between showers"` (`SOURCES.md` row 10). |
| 31 | 4 Seas of Natural Gas | 325.32–337.84 | 12.5 | NASA/JPL | Cassini radar mosaic of Titan's north polar seas (`PIA20021_right_panel`, use 1 of 2, `1440×1144` right-panel crop with left insets excluded, wide push) → Ligeia Mare drowned coastline (`PIA17031`, use 1 of 2, bays and islands pan) | 3 | **VISUAL MUST (`CHIEF_SCOPE_v31.md` §4):** `"Bays and islands"` (`SOURCES.md` row 11). Replaces rejected `PIA10008`. |
| 32 | 4 Seas of Natural Gas | 338.92–354.22 | 15.3 | NASA/JPL / CODE | North polar seas radar mosaic (`PIA20021_right_panel`, use 2 of 2, tight reframe on Kraken Mare) → CODE `scalemap` (wide): `"KRAKEN MARE ≈ 400,000 KM²"` → CODE `scalemap` (tight): `"≈ 5× LAKE SUPERIOR"` | 3 | **VISUAL MUST, DATA:** `"400,000 km², almost 5× Lake Superior"` (`SOURCES.md` row 11). Final use of `PIA20021_right_panel`. |
| 33 | 4 Seas of Natural Gas | 355.14–366.88 | 11.7 | NASA/JPL / CODE | Cassini radar map of Ligeia Mare (`PIA17031`, use 2 of 2, slow push, `"FALSE COLOUR"`) → CODE `depth_ligeia` + `timeline` marker `"2013"`: radar beam bouncing off seabed at `"≈ 160 M"` | 2 | **WHEN, DATA:** `"2013"` and `"about 160 m"` (`SOURCES.md` row 12). J2090 disclosure: FALSE COLOUR. |
| 34 | 4 Seas of Natural Gas | 367.92–372.42 | 4.5 | NASA/JPL / CODE | Cassini near-infrared Kraken/Ligeia mosaic (`PIA21434`, use 1 of 2, tight reframe) with animated CODE depth bar plunging from `"LIGEIA 160 M"` to `"KRAKEN ≥ 300 M"` | 1 | **DATA:** `"at least 300 m (1,000 ft)"` (`SOURCES.md` row 12). Graded plate behind graphic avoids back-to-back slabs. |
| 35 | 4 Seas of Natural Gas | 373.10–385.06 | 12.0 | NASA/JPL / CODE | Graded real Titan plate → reviewed `r35_ocean` (J2264), using `PIA14602` (use 2 of 2, final appearance after R09); `55–80 KM ICY CRUST / WATER, SALTS, AMMONIA` | 2 | **VISUAL MUST, DATA:** our own CODE cutaway (`SOURCES.md` row 13). |
| 36 | 4 Seas of Natural Gas | 386.06–388.92 | 2.9 | NASA/JPL | Cassini VIMS specular sunglint reflecting off Kraken Mare (`PIA12481`, use 1 of 2), slow push | 1 | `"Wait, that raises a terrifying question."` |
| 37 | 5 Would It Explode? | 389.76–401.44 | 11.7 | NASA SVS / CODE | Dragonfly descending over Titan terrain (`SVS20311_DF_End_Pan_1080`, stretch 1 of 3, `0.0–5.8 s`, Credit: `NASA/Johns Hopkins APL/Goddard Space Flight Center`) → CODE `spark_question`: thruster plume icon + `"?"` spark over dark sea plate | 2 | **SVS 20311 (`CHIEF_SCOPE_v31.md` §2).** No real fire or explosion stock. |
| 38 | 5 Would It Explode? | 402.02–411.64 | 9.6 | NASA/JPL / CODE | Cassini near-infrared full-disc view showing Kraken Mare (`PIA14584`, use 1 of 2) → CODE `reserves`: Titan liquid hydrocarbons bar towering `"HUNDREDS OF TIMES"` over Earth oil & gas reserves | 2 | **DATA:** `"hundreds of times more liquid hydrocarbons"` (`SOURCES.md` row 14). NEAR-INFRARED VIEW. |
| 39 | 5 Would It Explode? | 412.62–424.92 | 12.3 | NASA / CODE | Blue Marble Earth (`AS17-148-22727`, use 1 of 1, Apollo 17 NASA JSC, inset over graded moving plate) → CODE `fire` (part 1): fuel + oxygen triangle → oxygen-only bars `"EARTH 21%"` / `"TITAN ≈ 0%"` on linear 0–25% axis | 3 | **VISUAL MUST, DATA:** `"21% O₂"` (`SOURCES.md` rows 9, 14). Real Earth plate separates R38 and R39 CODE graphics. |
| 40 | 5 Would It Explode? | 425.66–432.96 | 7.3 | NASA/JPL / CODE | Cassini near-infrared Titan plate with Kraken Mare visible (`PIA14584`, use 2 of 2, reframed) → CODE `fire` (part 2): `"TITAN: 95% N₂ · 5% CH₄ · ALMOST NO O₂"` with oxygen side greyed out | 2 | **DATA:** `"95% N₂, 5% CH₄, almost no O₂"` (`SOURCES.md` rows 9, 14). |
| 41 | 5 Would It Explode? | 433.82–446.86 | 13.0 | CODE / NASA/JPL | CODE `no_flame`: match & thruster in N₂ sky (spark goes out) → Cassini VIMS specular sea glint (`PIA12481`, use 2 of 2, tight reframe) → CODE `FACT` card `"NO OXYGEN TO BURN"` | 3 | **VISUAL MUST, FACT:** `"No oxygen to burn"` (4 words; `SOURCES.md` row 14). |
| 42 | 5 Would It Explode? | 447.74–455.56 | 7.8 | NASA / CODE | NASA RS-25 rocket engine hot-fire test plume in Earth air (`SSC20210116_GR8438`, use 1 of 1, 3.8 s pan) → CODE `flipfire` (part 1): `"EARTH: FUEL TANK + O₂ AIR"` | 2 | Real NASA Stennis rocket test plume (`SSC20210116_GR8438`) separates R41 and R42 CODE graphics. |
| 43 | 5 Would It Explode? | 456.16–463.26 | 7.1 | CODE | CODE `flipfire` (part 2, wide → tight): `"TITAN: O₂ TANK + CH₄ SKY"` with small flame at oxygen nozzle | 2 | **VISUAL MUST:** reversed combustion graphic (`SOURCES.md` row 14). |
| 44 | 5 Would It Explode? | 464.44–474.10 | 9.7 | NASA/JPL / NASA SVS | Cassini crescent Titan in golden haze (`PIA17163`, use 2 of 2, reframed) → Dragonfly entry/flight animation in Titan's nitrogen sky (`SVS20311_DF_Open_1080`, stretch 1 of 3, `0.0–4.8 s`) | 2 | Bridge into ch6 (`SVS 20311`). |
| 45 | 6 Wings for Titan | 474.94–494.52 | 19.6 | CODE / NASA SVS | CODE `densegrav` (part 1: `"AIR ≈ 4× DENSER"`) → NASA SVS Dragonfly rotor flight clip (`SVS20311_DF_Open_1080`, stretch 2 of 3, `6.0–11.5 s`, `>10 s` after R44 stretch) → CODE `lift` (part 2: `"GRAVITY ≈ 1/7"`) → CODE `lift` gauge feeding wing icon | 4 | **VISUAL MUST, DATA:** `"4× denser"` and `"1/7 gravity"` (`SOURCES.md` row 15). SVS 20311 clip separates CODE segments. |
| 46 | 6 Wings for Titan | 495.24–501.70 | 6.5 | NASA SVS / CODE | £0 Fallback (`CHIEF_SCOPE_v31.md`): CODE `lift_28x` gauge (`"4× AIR ÷ 1/7 WEIGHT ≈ 28× EASIER · OUR ROUGH SUM"`) over NASA SVS Dragonfly dune pan (`SVS20311_DF_End_Pan_1080`, stretch 2 of 3, `3.0–9.5 s`) | 2 | **ORBIT ACTS £0 Fallback, DATA:** `"≈ 28× easier (our rough sum)"` (`SOURCES.md` row 15). |
| 47 | 6 Wings for Titan | 503.20–516.86 | 13.7 | NASA / CODE | Dragonfly soaring over Titan dunes (`NASA_Dragonfly_BannerFactSheet_2024`, use 2 of 2, reframed wide-to-medium push) → landed rotorcraft perspective (`SVS20311_Dragonfly_Landed_Closeup`, use 1 of 2, wide pan) + CODE `FACT` card `"IDEAL WAY TO TRAVEL"` | 3 | **FACT:** `"Ideal way to travel"` (4 words, verbatim from `SOURCES.md` row 15). |
| 48 | 6 Wings for Titan | 517.68–527.30 | 9.6 | NASA SVS / CODE | Dragonfly octocopter 8-rotor close-up in flight (`SVS20311_DF_Open_1080`, stretch 3 of 3, `14.0–19.0 s`, `>10 s` after R45 stretch) → CODE `timeline` marker `"NET JULY 2028"` + `"8 ROTORS · NUCLEAR-POWERED"` | 2 | **WHEN, DATA:** `"NET July 2028"` and `"8 rotors"` (`SOURCES.md` row 16). |
| 49 | 6 Wings for Titan | 528.38–540.56 | 12.2 | NASA SVS / CODE | Dragonfly over Titan dunes (`SVS20311_DF_End_Pan_1080`, stretch 3 of 3, `6.0–12.0 s`, `>10 s` after R46 stretch) → CODE `timeline` marker `"LATE 2034"` → CODE day/night bar `"DAYTIME ≈ 8 EARTH DAYS"` | 3 | **WHEN, DATA:** `"Late 2034"` and `"8 Earth days"` (`SOURCES.md` row 16). |
| 50 | 6 Wings for Titan | 541.82–556.06 | 14.2 | NASA SVS / CODE | Dragonfly landed on Titan surface (`SVS20311_Dragonfly_Landed_Closeup`, use 2 of 2, reframed) + Dragonfly surface drill (`SVS20311_Dragonfly_Drill_1080`, stretch 1 of 1, `0.0–5.0 s`) with CODE map pin `SELK CRATER` / `DRAGONFLY TARGET` → CODE `selk_soup`: `"WATER + ORGANICS → PRIMORDIAL SOUP"` | 3 | **VISUAL MUST:** Selk target only on CODE map + SVS 20311 Dragonfly surface/drill; `"primordial soup"` (`SOURCES.md` row 16). |
| 51 | 6 Wings for Titan | 557.32–566.50 | 9.2 | NASA/JPL | Cassini near-infrared northern lakes view (`PIA21434`, use 2 of 2, wide reframed pan) → Cassini multi-spectral golden Titan globe (`PIA20016`, use 2 of 2, slow pull-back) | 2 | `"A time capsule of early Earth."` Replaces rejected `PIA07870`/`PIA07871` mosaics (`CHIEF_SCOPE_v31.md` §1). |
| 52 | 6 Wings for Titan | 567.66–582.38 | 14.7 | NASA / STScI / CODE | Hand-off to 033: JWST NIRCam Uranus `weic2310a` (use 1 of 1, INFRARED VIEW; full credit in harvest pool) → reviewed duration-only `r52_uranus_21y` (J2251), containing `PIA18182` (use 1 of 1) as its sole appearance; no 2D tilt-axis line | 3 | **DATA:** `"21-year dark winter"` (`SOURCES.md` row 18). Holds moving picture 2–3 s past `582.38 s` as music fades. |
"""


def main():
    shot_list_path = HERE / "SHOT_LIST_v08.md"
    shot_list_path.write_text(SHOT_LIST_V08)
    shot_list_sha = sha256_file(shot_list_path)

    pool_path = HERE / "HARVEST_POOL_v01.json"
    pool = json.loads(pool_path.read_text())

    # Exact row allocation for existing stills in HARVEST_POOL_v01.json
    row_map = {
        "PIA02238": [12, 13],
        "PIA07231": [5, 15],
        "PIA07232": [18, 20],
        "PIA07233": [],
        "PIA07236": [17, 21],
        "PIA08167": [1, 4],
        "PIA08733": [9, 23],
        "PIA09182": [29, 30],
        "PIA10008": [],
        "PIA12481": [36, 41],
        "PIA14584": [38, 40],
        "PIA14602": [9, 35],
        "PIA14922": [6, 8],
        "PIA16638": [],
        "PIA17031": [31, 33],
        "PIA17163": [25, 44],
        "PIA19051": [],
        "PIA20016": [1, 51],
        "PIA21434": [34, 51],
        "PIA21450": [14, 25],
        "PIA21610": [16, 28],
        "PIA21902": [3, 11],
        "huygens_portrait_1671": [7],
        "PIA07870": [],
        "PIA07871": [],
        "PIA14909": [19, 23],
        "AS17-148-22727": [39],
    }

    excluded_ids = {"PIA07233", "PIA10008", "PIA16638", "PIA19051", "PIA07870", "PIA07871"}
    for asset in pool["assets"]:
        aid = asset["asset_id"]
        if aid in row_map:
            asset["referenced_rows"] = row_map[aid]
            if "allocated_rows" in asset:
                asset["allocated_rows"] = row_map[aid]
            if aid in excluded_ids:
                asset["review_status"] = "EXCLUDED_CHIEF_SCOPE_v31"
            else:
                asset["review_status"] = "ALLOCATED_STEP_2_OF_4_CHIEF_SCOPE_v31"

    # New still assets to add/update in pool["assets"]
    svs_evidence_path = str(NAS_SVS / "svs_20311_api.json")
    svs_evidence_sha = sha256_file(NAS_SVS / "svs_20311_api.json")
    dragonfly_page_path = str(NAS_SVS / "science_nasa_dragonfly.html")
    dragonfly_page_sha = sha256_file(NAS_SVS / "science_nasa_dragonfly.html")

    new_stills = [
        {
            "asset_id": "PIA20021_right_panel",
            "title": "Titan's Northern Lakes: Salt Flats? (Right-Panel Crop)",
            "description": "Clean 1440x1144 crop (420, 36, 1860, 1180) of the right-hand polar seas radar panel of PIA20021, excluding all left-strip inset boxes and border wedges per CHIEF_SCOPE_v31.md §4.",
            "credit": "NASA/JPL-Caltech/ASI/GSFC",
            "credit_required": "NASA/JPL-Caltech/ASI/GSFC",
            "source_page": "https://images.nasa.gov/details/PIA20021",
            "download_url": "https://images-assets.nasa.gov/image/PIA20021/PIA20021~orig.jpg",
            "local_path": str(NAS_SVS / "PIA20021_right_panel_1440x1144.jpg"),
            "parent_path": str(NAS_REF / "PIA20021.jpg"),
            "parent_sha256": sha256_file(NAS_REF / "PIA20021.jpg"),
            "crop_xyxy": [420, 36, 1860, 1180],
            "referenced_rows": [31, 32],
            "review_status": "ALLOCATED_STEP_2_OF_4_CHIEF_SCOPE_v31",
            "licence_status": "NASA_JPL_IMAGE_POLICY_CREDIT_REQUIRED",
            "source_evidence_path": str(NAS_SVS / "PIA20021_metadata.json"),
            "source_evidence_sha256": sha256_file(NAS_SVS / "PIA20021_metadata.json"),
        },
        {
            "asset_id": "PIA17172",
            "title": "The Day the Earth Smiled: Saturn and Titan Backlit Panorama",
            "description": "Cassini wide-angle backlit panorama of Saturn's rings and Titan's atmospheric limb.",
            "credit": "NASA/JPL-Caltech/Space Science Institute",
            "credit_required": "NASA/JPL-Caltech/Space Science Institute",
            "source_page": "https://images.nasa.gov/details/PIA17172",
            "download_url": "https://images-assets.nasa.gov/image/PIA17172/PIA17172~orig.jpg",
            "local_path": str(NAS_REF / "PIA17172.jpg"),
            "referenced_rows": [10, 27],
            "review_status": "ALLOCATED_STEP_2_OF_4_CHIEF_SCOPE_v31",
            "licence_status": "NASA_JPL_IMAGE_POLICY_CREDIT_REQUIRED",
            "source_evidence_path": str(NAS_SVS / "PIA17172_metadata.json"),
            "source_evidence_sha256": sha256_file(NAS_SVS / "PIA17172_metadata.json"),
        },
        {
            "asset_id": "PIA21445",
            "title": "Golden Titan Crescent in Haze",
            "description": "Cassini natural-color view of Titan's golden atmospheric haze and crescent.",
            "credit": "NASA/JPL-Caltech/Space Science Institute",
            "credit_required": "NASA/JPL-Caltech/Space Science Institute",
            "source_page": "https://images.nasa.gov/details/PIA21445",
            "download_url": "https://images-assets.nasa.gov/image/PIA21445/PIA21445~orig.jpg",
            "local_path": str(NAS_REF / "PIA21445.jpg"),
            "referenced_rows": [22, 26],
            "review_status": "ALLOCATED_STEP_2_OF_4_CHIEF_SCOPE_v31",
            "licence_status": "NASA_JPL_IMAGE_POLICY_CREDIT_REQUIRED",
            "source_evidence_path": str(NAS_SVS / "PIA21445_metadata.json"),
            "source_evidence_sha256": sha256_file(NAS_SVS / "PIA21445_metadata.json"),
        },
        {
            "asset_id": "PIA01050",
            "title": "Cassini Launches Carrying the Huygens Probe",
            "description": "Launch of the Cassini spacecraft and Huygens probe aboard a Titan IVB/Centaur on October 15, 1997.",
            "credit": "NASA/JPL/KSC",
            "credit_required": "NASA/JPL/KSC",
            "source_page": "https://images.nasa.gov/details/PIA01050",
            "download_url": "https://images-assets.nasa.gov/image/PIA01050/PIA01050~orig.jpg",
            "local_path": str(NAS_SVS / "PIA01050.jpg"),
            "referenced_rows": [15],
            "review_status": "ALLOCATED_STEP_2_OF_4_CHIEF_SCOPE_v31",
            "licence_status": "NASA_JPL_IMAGE_POLICY_CREDIT_REQUIRED",
            "source_evidence_path": str(NAS_SVS / "PIA01050_metadata.json"),
            "source_evidence_sha256": sha256_file(NAS_SVS / "PIA01050_metadata.json"),
        },
        {
            "asset_id": "PIA22766",
            "title": "Cassini's Grand Finale: Backlit Saturn and Rings",
            "description": "Cassini spacecraft view across Saturn's backlit rings and atmosphere.",
            "credit": "NASA/JPL-Caltech",
            "credit_required": "NASA/JPL-Caltech",
            "source_page": "https://images.nasa.gov/details/PIA22766",
            "download_url": "https://images-assets.nasa.gov/image/PIA22766/PIA22766~orig.jpg",
            "local_path": str(NAS_SVS / "PIA22766.jpg"),
            "referenced_rows": [3, 19],
            "review_status": "ALLOCATED_STEP_2_OF_4_CHIEF_SCOPE_v31",
            "licence_status": "NASA_JPL_IMAGE_POLICY_CREDIT_REQUIRED",
            "source_evidence_path": str(NAS_SVS / "PIA22766_metadata.json"),
            "source_evidence_sha256": sha256_file(NAS_SVS / "PIA22766_metadata.json"),
        },
        {
            "asset_id": "SSC20210116_GR8438",
            "title": "RS-25 Rocket Engine Hot-Fire Test at Stennis Space Center",
            "description": "NASA RS-25 engine hot-fire test plume burning in Earth's oxygen-rich atmosphere at Stennis Space Center.",
            "credit": "NASA/Stennis Space Center/Danny Nowlin",
            "credit_required": "NASA/Stennis Space Center/Danny Nowlin",
            "source_page": "https://images.nasa.gov/details/SSC-20210116-s00105",
            "download_url": "https://images-assets.nasa.gov/image/SSC-20210116-s00105/SSC-20210116-s00105~orig.jpg",
            "local_path": str(NAS_SVS / "SSC20210116_GR8438.jpg"),
            "referenced_rows": [42],
            "review_status": "ALLOCATED_STEP_2_OF_4_CHIEF_SCOPE_v31",
            "licence_status": "NASA_MEDIA_USAGE_GUIDELINES_PUBLIC_DOMAIN",
            "source_evidence_path": str(NAS_SVS / "SSC20210116_GR8438_metadata.json"),
            "source_evidence_sha256": sha256_file(NAS_SVS / "SSC20210116_GR8438_metadata.json"),
        },
        {
            "asset_id": "SVS20311_Dragonfly_Landed_Closeup",
            "title": "Dragonfly Landed on Titan Surface (SVS 20311)",
            "description": "High-resolution still from NASA Goddard SVS 20311 showing the Dragonfly rotorcraft lander on Titan's organic dunes.",
            "credit": "NASA/Johns Hopkins APL/Goddard Space Flight Center",
            "credit_required": "NASA/Johns Hopkins APL/Goddard Space Flight Center",
            "source_page": "https://svs.gsfc.nasa.gov/20311",
            "download_url": "https://svs.gsfc.nasa.gov/vis/a020000/a020300/a020311/Dragonfly_Landed_Closeup.png",
            "local_path": str(NAS_SVS / "SVS20311_Dragonfly_Landed_Closeup.png"),
            "referenced_rows": [47, 50],
            "review_status": "ALLOCATED_STEP_2_OF_4_CHIEF_SCOPE_v31",
            "licence_status": "NASA_SVS_MEDIA_USAGE_GUIDELINES_CREDIT_REQUIRED",
            "source_evidence_path": svs_evidence_path,
            "source_evidence_sha256": svs_evidence_sha,
        },
        {
            "asset_id": "NASA_Dragonfly_BannerFactSheet_2024",
            "title": "Dragonfly Rotorcraft Soaring Over Titan Dunes (NASA Mission Page)",
            "description": "Official NASA Dragonfly mission banner illustration showing the 8-rotor lander flying above Titan's dunes.",
            "credit": "NASA/Johns Hopkins APL/Steve Gribben",
            "credit_required": "NASA/Johns Hopkins APL/Steve Gribben",
            "source_page": "https://science.nasa.gov/mission/dragonfly/",
            "download_url": "https://assets.science.nasa.gov/content/dam/science/psd/solar/2023/09/b/BannerFactSheet_2024.jpg",
            "local_path": str(NAS_SVS / "NASA_Dragonfly_BannerFactSheet_2024.jpg"),
            "referenced_rows": [5, 47],
            "review_status": "ALLOCATED_STEP_2_OF_4_CHIEF_SCOPE_v31",
            "licence_status": "NASA_MISSION_PORTAL_MEDIA_USAGE_GUIDELINES_CREDIT_REQUIRED",
            "source_evidence_path": dragonfly_page_path,
            "source_evidence_sha256": dragonfly_page_sha,
        },
    ]

    existing_by_id = {a["asset_id"]: a for a in pool["assets"]}
    for item in new_stills:
        p = Path(item["local_path"])
        with Image.open(p) as im:
            w, h = im.size
        item["width"] = w
        item["height"] = h
        item["sha256"] = sha256_file(p)
        item["bytes"] = p.stat().st_size
        item["download_status"] = "downloaded"
        if item["asset_id"] in existing_by_id:
            existing_by_id[item["asset_id"]].update(item)
        else:
            pool["assets"].append(item)

    # Update motion_candidates: keep excluded history records with referenced_rows=[] and add SVS 20311 clips
    for mc in pool.get("motion_candidates", []):
        mc["referenced_rows"] = []
        if mc["asset_id"] == "dragonfly_at_titan":
            mc["review_status"] = "EXCLUDED_REPLACED_BY_NASA_SVS_20311_CHIEF_SCOPE_v31"

    svs_clips = [
        {
            "asset_id": "SVS20311_DF_End_Pan_1080",
            "title": "Dragonfly Over Titan Dunes Pan (SVS 20311)",
            "credit": "NASA/Johns Hopkins APL/Goddard Space Flight Center",
            "source_page": "https://svs.gsfc.nasa.gov/20311",
            "download_url": "https://svs.gsfc.nasa.gov/vis/a020000/a020300/a020311/DF_End_Pan_1080.mp4",
            "local_path": str(NAS_SVS / "SVS20311_DF_End_Pan_1080.mp4"),
            "width": 1920,
            "height": 1080,
            "duration_s": 12.52,
            "referenced_rows": [37, 46, 49],
            "intervals": [
                {"row": 37, "in_s": 0.0, "out_s": 5.8, "film_window_s": "389.76-395.56"},
                {"row": 46, "in_s": 3.0, "out_s": 9.5, "film_window_s": "495.24-501.70"},
                {"row": 49, "in_s": 6.0, "out_s": 12.0, "film_window_s": "528.38-534.38"},
            ],
            "review_status": "ALLOCATED_STEP_2_OF_4_CHIEF_SCOPE_v31",
            "licence_status": "NASA_SVS_MEDIA_USAGE_GUIDELINES_CREDIT_REQUIRED",
            "source_evidence_path": svs_evidence_path,
            "source_evidence_sha256": svs_evidence_sha,
        },
        {
            "asset_id": "SVS20311_DF_Open_1080",
            "title": "Dragonfly Flight and Rotor Spin-Up on Titan (SVS 20311)",
            "credit": "NASA/Johns Hopkins APL/Goddard Space Flight Center",
            "source_page": "https://svs.gsfc.nasa.gov/20311",
            "download_url": "https://svs.gsfc.nasa.gov/vis/a020000/a020300/a020311/DF_Open_1080.mp4",
            "local_path": str(NAS_SVS / "SVS20311_DF_Open_1080.mp4"),
            "width": 1920,
            "height": 1080,
            "duration_s": 24.45,
            "referenced_rows": [44, 45, 48],
            "intervals": [
                {"row": 44, "in_s": 0.0, "out_s": 4.8, "film_window_s": "469.30-474.10"},
                {"row": 45, "in_s": 6.0, "out_s": 11.5, "film_window_s": "479.80-485.30"},
                {"row": 48, "in_s": 14.0, "out_s": 19.0, "film_window_s": "517.68-522.68"},
            ],
            "review_status": "ALLOCATED_STEP_2_OF_4_CHIEF_SCOPE_v31",
            "licence_status": "NASA_SVS_MEDIA_USAGE_GUIDELINES_CREDIT_REQUIRED",
            "source_evidence_path": svs_evidence_path,
            "source_evidence_sha256": svs_evidence_sha,
        },
        {
            "asset_id": "SVS20311_Dragonfly_Drill_1080",
            "title": "Dragonfly Surface Sampling Drill on Titan (SVS 20311)",
            "credit": "NASA/Johns Hopkins APL/Goddard Space Flight Center",
            "source_page": "https://svs.gsfc.nasa.gov/20311",
            "download_url": "https://svs.gsfc.nasa.gov/vis/a020000/a020300/a020311/Dragonfly_Drill_1080.mp4",
            "local_path": str(NAS_SVS / "SVS20311_Dragonfly_Drill_1080.mp4"),
            "width": 1920,
            "height": 1080,
            "duration_s": 12.70,
            "referenced_rows": [50],
            "intervals": [
                {"row": 50, "in_s": 0.0, "out_s": 5.0, "film_window_s": "545.00-550.00"},
            ],
            "review_status": "ALLOCATED_STEP_2_OF_4_CHIEF_SCOPE_v31",
            "licence_status": "NASA_SVS_MEDIA_USAGE_GUIDELINES_CREDIT_REQUIRED",
            "source_evidence_path": svs_evidence_path,
            "source_evidence_sha256": svs_evidence_sha,
        },
        {
            "asset_id": "SVS20311_DF_Intake_shot_1080",
            "title": "Dragonfly Sample Intake Shot on Titan (SVS 20311 Reserve)",
            "credit": "NASA/Johns Hopkins APL/Goddard Space Flight Center",
            "source_page": "https://svs.gsfc.nasa.gov/20311",
            "download_url": "https://svs.gsfc.nasa.gov/vis/a020000/a020300/a020311/DF_Intake_shot_1080.mp4",
            "local_path": str(NAS_SVS / "SVS20311_DF_Intake_shot_1080.mp4"),
            "width": 1920,
            "height": 1080,
            "duration_s": 13.23,
            "referenced_rows": [],
            "intervals": [],
            "review_status": "RESERVE_STEP_2_OF_4_CHIEF_SCOPE_v31",
            "licence_status": "NASA_SVS_MEDIA_USAGE_GUIDELINES_CREDIT_REQUIRED",
            "source_evidence_path": svs_evidence_path,
            "source_evidence_sha256": svs_evidence_sha,
        },
    ]

    mc_by_id = {m["asset_id"]: m for m in pool["motion_candidates"]}
    for clip in svs_clips:
        p = Path(clip["local_path"])
        clip["sha256"] = sha256_file(p)
        clip["bytes"] = p.stat().st_size
        clip["download_status"] = "DOWNLOADED_AND_PROBED"
        if clip["asset_id"] in mc_by_id:
            mc_by_id[clip["asset_id"]].update(clip)
        else:
            pool["motion_candidates"].append(clip)

    pool["allocation_shot_list"] = "SHOT_LIST_v08.md"
    pool["shot_list_sha256"] = shot_list_sha
    pool["status"] = "STEP_2_OF_4_POOL_AND_SHOT_LIST_v08_LOCKED_UNDER_CHIEF_SCOPE_v31"
    pool["chief_scope_ref"] = "jobs/reviews/J2089/CHIEF_SCOPE_v31.md"
    pool["outstanding"] = [
        "Step 3 of 4: Render graded 1080p30 moving-plate composites across Rows 1-52 (R16 and R23 already KEEP)",
        "Step 4 of 4: Run picture_qa.py, polish_gate.py, and Short frame-exclusion check on final cuts",
    ]

    # Verify invariants before writing
    excluded_short = set(pool.get("excluded_short_asset_ids", []))
    for a in pool["assets"]:
        rows = a.get("referenced_rows", [])
        assert len(rows) <= 2, f"Still {a['asset_id']} exceeds 2 uses: {rows}"
        if rows:
            assert a["asset_id"] not in excluded_short, f"Excluded Short asset active: {a['asset_id']}"
            assert a["asset_id"] not in excluded_ids, f"Excluded asset active: {a['asset_id']}"

    for m in pool["motion_candidates"]:
        rows = m.get("referenced_rows", [])
        assert len(rows) <= 5, f"Motion clip {m['asset_id']} exceeds 5 stretches: {rows}"

    pool_path.write_text(json.dumps(pool, indent=2) + "\n")
    print("Successfully locked SHOT_LIST_v08.md and HARVEST_POOL_v01.json")
    print("SHOT_LIST_v08.md sha256:", shot_list_sha)


if __name__ == "__main__":
    main()
