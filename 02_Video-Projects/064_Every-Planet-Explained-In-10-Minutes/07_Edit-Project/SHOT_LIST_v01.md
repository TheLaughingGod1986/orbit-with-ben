# Shot List v01 — `OWB:064` Every Planet Explained in 10 Minutes (Mercury to Neptune)

- **Job:** `J3022` (Build Package 3 of 4)
- **Locked script:** `01_Script/every_planet_explained_script_master_v04.md` (`556f3c8d...`)
- **Locked VO:** `02_Voiceover/every_planet_explained_vo_v01.wav` (`683.86 s`, `4b478fcd...`)
- **Total timeline:** `701.86 s` (`683.86 s` VO + `18.00 s` end-screen hold, 24 fps CFR)
- **Spend:** `£0.00` cash, `0` Flow/Vertex credits, zero paid generation.
- **Rule compliance:** No chapter card before `0:45` (first chapter card `C02` at `81.90 s`), real imagery between every code graphic, every chapter satisfies the `NUMBER OBJECT` teaching gate, labels `<= 4` words verbatim from VO, zero Orbit on thumbnails, zero still used `> 2` appearances, zero upscale `> 2.35x`.

## Flagged / Rejected Shelf & Candidate Assets

- **`PIA00104`** (Venus - Computer Simulated Global View Centered at 180 Degrees East): NASA API title declares 'Computer Simulated Global View' — violates picture_qa KIND_FAIL; replaced by real Mariner 10 PIA23791 & PIA00271.
- **`PIA00257`** (Venus - Computer Simulated Global View Centered at 0 Degrees East): NASA API title declares 'Computer Simulated Global View' — violates picture_qa KIND_FAIL.
- **`PIA21974`** (Jupiter's Colorful Cloud Belts (1280x433)): Ultra-wide 1280x433 strip would upscale 2.49x vertically (>2.35x FAIL); replaced by Juno PIA21972 (1920x1630), PIA22946 (3000x3000), PIA21775 (1620x1440).
- **`PIA16949`** (An Extra Kidney? (wrong subject)): NASA ID does not depict Mercury; excluded.
- **`GSFC_20171208_Archive_e001435`** (Sun Emits a Solstice CME (wrong subject)): Solar CME, not Hubble Great Red Spot; excluded.
- **`Giuseppe_Colombo_wiki_mosaic`** (Famous Italians Mosaic.png): Not an individual portrait of Giuseppe Colombo; per studio/RULES.md ('Show no portrait we can't source; the card can sit over the scene alone'), WHO card rides over real Mercury imagery.
- **`PIA02215`** (Crescents of Neptune and Triton (800x600)): 800x600 would require 2.40x horizontal upscale full-frame (>2.35x FAIL); allowed only as framed inset <=1.25x inside code_graphic_064_r64_neptune_farewell.mp4, never full-bleed.
- **`PIA21049`** (Changing Colors in Saturn North (810x910)): 810x910 would exceed 2.35x horizontal upscale full-frame; embedded strictly as framed inset <=1.0x inside code_graphic_064_r49_saturn_hexagon.mp4.
- **`PIA00059`** (Triton South Polar Terrain (800x795)): 800x795 would require 2.40x horizontal upscale full-frame (>2.35x FAIL); replaced full-frame by PIA00317 (4500x3500) and used only as framed inset <=1.0x.
- **`020_jupiter_film_v05_shelf_music_etc`** (Shelf music beds & source-film code graphics (020/021/023/025/027/031/033)): Source-film code graphics are references only (every 064 graphic row has its own fresh render); shelf music beds are prohibited by music_gate.py.

## Timestamped Shot Table

| Row | In | Out | Dur | Kind | Assets | Teach Markers & Notes |
|---|---:|---:|---:|---|---|---|
| `R01` | `0.00` | `7.10` | `7.10s` | `NASA` | `PIA15162` | Frame 0 real Mercury globe rotating + lower-third '01 / 08 · MERCURY' (no chapter card < 0:45) |
| `R02` | `7.10` | `11.45` | `4.35s` | `NASA` | `PIA16523` | Immediate answer < 12 s: Prokofiev polar craters in permanent shadow |
| `R03` | `11.45` | `25.70` | `14.25s` | `CODE` | `code_graphic_064_r03_mercury_temp.mp4` | DATA #1: 430 °C day vs −180 °C night at 58M km (7× sunlight) · NUMBER OBJECT (Ch 1) |
| `R04` | `25.70` | `32.85` | `7.15s` | `NASA` | `PIA17386` | WHO #1: Giuseppe Colombo (1920–1984) — Italian mathematician (over real Mercury; no unverified portrait) · WHEN: 1965 (timeline start) |
| `R05` | `32.85` | `49.90` | `17.05s` | `CODE` | `code_graphic_064_r05_mercury_resonance.mp4` | DATA #1b: 3:2 spin-orbit dial (59d spin, 88d orbit -> 176d solar day) |
| `R06` | `49.90` | `64.30` | `14.40s` | `NASA+CODE` | `PIA11364 -> code_graphic_064_r07_mercury_core.mp4` | Real Mercury limb -> DATA #1c + SCALE: 2,440 km (blueberry vs nickel), 85% metallic core · FACT #1: Second densest planet |
| `R08` | `64.30` | `81.36` | `17.06s` | `NASA` | `PIA19411 -> PIA16853` | Edit label: 'Almost no tilt' (0.034° technical call-out, never 2°) · WHEN: Mar 2011–Apr 2015 (timeline) |
| `C02` | `81.90` | `82.20` | `0.30s` | `CARD` | `code_graphic_064_ch02_card_venus.mp4` | CHAPTER CARD 02 / 08 · VENUS — The Backwards Furnace (breath 0.60 s after S09) |
| `R09` | `82.20` | `93.80` | `11.60s` | `NASA` | `PIA00271 -> PIA23791` | Real Mariner 10 Venus sulfuric-acid clouds (023/033 shelf + API) |
| `R10` | `93.80` | `118.05` | `24.25s` | `CODE` | `code_graphic_064_r12_venus_greenhouse.mp4` | DATA #2 + SCALE: 464 °C, 92 bars (930 m underwater), 96.5% CO2 · FACT #2: Hottest planetary surface · NUMBER OBJECT (Ch 2) |
| `R11` | `118.05` | `130.75` | `12.70s` | `NASA+CODE` | `PIA00233 -> code_graphic_064_r14_venus_spin.mp4` | Real Magellan Venus radar surface -> DATA #2b: 243-day backwards spin vs 225-day orbit (Sun rises west) |
| `R13` | `130.75` | `154.80` | `24.05s` | `NASA` | `PIA23791 -> Venera13_surface` | WHEN: 1978 (Pioneer Venus 100× D/H) & 1 Mar 1982 (Venera 13, 127 min vs 32 min, ~4× design) on timeline |
| `R14` | `154.80` | `157.90` | `3.10s` | `OMNI` | `orbit_looks_back_earth_omni_v01_t0-5s` | ORBIT ACTS: Verified 023 shelf Omni clip (Orbit at Venus looking back at Earth) |
| `C03` | `158.36` | `158.72` | `0.36s` | `CARD` | `code_graphic_064_ch03_card_earth.mp4` | CHAPTER CARD 03 / 08 · EARTH — The Shielded Ocean World (breath 0.60 s after S18) |
| `R15` | `158.72` | `176.45` | `17.73s` | `NASA` | `svs_12312_epic_earth_timelapse -> PIA18033` | Real DSCOVR EPIC rotating Earth + Apollo 17 Blue Marble (031/033 shelf) |
| `R16` | `176.45` | `199.35` | `22.90s` | `CODE` | `code_graphic_064_r20_earth_spin_bulge.mp4` | DATA #3a + SCALE: 1,670 km/h equatorial spin (>4× Cyclone Olivia 408 km/h), 43 km bulge · NUMBER OBJECT (Ch 3) |
| `R17` | `199.35` | `217.50` | `18.15s` | `OMNI+CODE` | `orbit_northpole_omni_v01 -> code_graphic_064_r22_earth_core_flips.mp4` | ORBIT ACTS (027 shelf Omni) -> DATA #3b + WHEN: 3,000 km liquid-iron outer core · 183 reversals in 83 million years |
| `R19` | `217.50` | `226.85` | `9.35s` | `NASA` | `Carl_Friedrich_Gauss_1840_by_Jensen -> plate_031_r02a_iss_aurora_v01` | WHO #2: Carl Friedrich Gauss (1777–1855) — German mathematician (PD 1840 portrait) · WHEN: 1830s |
| `R20` | `226.85` | `244.70` | `17.85s` | `NASA` | `plate_031_r30a_iss_limb_v01 -> Five_Minutes_in_Orbit -> plate_031_r42a_iss_blue_limb_v01` | WHEN: 2020 (ESA ~9% weakening) · SCALE: 13 feet of concrete atmosphere shield |
| `R21` | `244.70` | `251.24` | `6.54s` | `NASA` | `svs_12312_epic_earth_timelapse` | SUBSCRIBE BEAT (35.9% runtime) — clean real Earth orbit footage, subtle subscribe pill |
| `C04` | `251.80` | `252.04` | `0.24s` | `CARD` | `code_graphic_064_ch04_card_mars.mp4` | CHAPTER CARD 04 / 08 · MARS — The Frozen Robot Desert (breath 0.60 s after S29) |
| `R22` | `252.04` | `272.70` | `20.66s` | `NASA` | `PIA00407 -> PIA19400` | Real Mars globe + Curiosity Gale Crater (025/031 shelf) · WHEN: 4 billion years ago (crustal traces) |
| `R23` | `272.70` | `285.85` | `13.15s` | `CODE` | `code_graphic_064_r28_mars_pressure.mp4` | DATA #4a: 6.36 mbar (<1% Earth) & −59 °C mean · NUMBER OBJECT (Ch 4) |
| `R24` | `285.85` | `301.25` | `15.40s` | `NASA+CODE` | `PIA00300 -> PIA02982 -> code_graphic_064_r30_mars_olympus.mp4` | Real Viking & MGS Olympus Mons -> DATA #4b + SCALE: 21.3 km above datum (>2× Everest, Arizona-sized base) |
| `R26` | `301.25` | `324.34` | `23.09s` | `NASA` | `JPL-20200303-MSLf-0001 -> PIA24542_full -> JPL-20210222-M2020f-0001 -> PIA19803` | WHEN: 10 Jun 2018 (Opportunity 60× design life) & 18 Jan 2024 (Ingenuity 72 flights) on timeline |
| `C05` | `324.80` | `325.12` | `0.32s` | `CARD` | `code_graphic_064_ch05_card_jupiter.mp4` | CHAPTER CARD 05 / 08 · JUPITER — The Ocean of Metallic Hydrogen (breath 0.60 s after S36) |
| `R27` | `325.12` | `333.80` | `8.68s` | `NASA` | `PIA22946 -> PIA21972` | Real Juno Jupiter Marble & swirling polar cyclones (intentional script callback 'beyond the asteroid belt') |
| `R28` | `333.80` | `356.15` | `22.35s` | `CODE` | `code_graphic_064_r35_jupiter_scale.mp4` | DATA #5a + SCALE: 11× wider (basketball vs grape), 318 Earth masses, 9.9-hour day · NUMBER OBJECT (Ch 5) |
| `R29` | `356.15` | `381.10` | `24.95s` | `NASA` | `Galileo_Galilei_Sustermans -> PIA21775 -> PIA01384` | WHO #3: Galileo Galilei (1564–1642) — Italian astronomer · WHEN: 1610, late 1800s, 2014 · Great Red Spot ~41,000 -> <16,500 km |
| `R30` | `381.10` | `388.15` | `7.05s` | `NASA` | `PIA04866` | MIDPOINT TWIST (~56%): 'Case closed? Wrong — there is no solid surface.' |
| `R31` | `388.15` | `398.30` | `10.15s` | `CODE` | `code_graphic_064_r39_jupiter_galileo.mp4` | DATA #5b + WHEN: 7 Dec 1995 Galileo probe 58-minute data return (no crushing event) |
| `R32` | `398.30` | `406.88` | `8.58s` | `NASA` | `PIA21972 -> PIA22946` | Real Juno swirling deep clouds for separate far-deeper metallic hydrogen region |
| `C06` | `407.44` | `407.70` | `0.26s` | `CARD` | `code_graphic_064_ch06_card_saturn.mp4` | CHAPTER CARD 06 / 08 · SATURN — Disappearing Rings and the Hexagon Storm (breath 0.60 s after S48) |
| `R33` | `407.70` | `414.60` | `6.90s` | `NASA` | `PIA17172 -> PIA11141` | Real Cassini backlit ring mosaic & Saturn globe |
| `R34` | `414.60` | `439.00` | `24.40s` | `CODE` | `code_graphic_064_r43_saturn_density_rings.mp4` | DATA #6a + FACT #3: Less dense (687 vs Water 1,000 kg/m³), 282,000 km radial rings (~10 m thick) · NUMBER OBJECT (Ch 6) |
| `R35` | `439.00` | `465.85` | `26.85s` | `NASA` | `PIA21046 -> PIA17172 -> PIA11141` | WHEN: 2017 Cassini dives (4,800–45,000 kg/s inflow, 0.41 Mimas mass, 10–100 Myr possible age) |
| `R36` | `465.85` | `477.65` | `11.80s` | `NASA` | `PIA17652 -> PIA14944` | Real Cassini north-pole hexagon & central eyewall · WHEN: early 1980s |
| `R37` | `477.65` | `493.50` | `15.85s` | `CODE` | `code_graphic_064_r46_saturn_hexagon.mp4` | DATA #6b + SCALE + WHEN: 30,000 km hexagon (>2 Earths, 322 km/h) + PIA21049 inset (2012–2016, Possibly seasonal haze) |
| `R38` | `493.50` | `496.46` | `2.96s` | `NASA` | `PIA21046` | Saturn transition out to Uranus |
| `C07` | `497.02` | `497.28` | `0.26s` | `CARD` | `code_graphic_064_ch07_card_uranus.mp4` | CHAPTER CARD 07 / 08 · URANUS — Knocked Sideways Into 21-Year Winters (breath 0.60 s after S56) |
| `R39` | `497.28` | `504.75` | `7.47s` | `NASA` | `r01_sourced_composite_v01_silent` | Real 033 verified Voyager 2 + JWST sideways Uranus clip |
| `R40` | `504.75` | `525.00` | `20.25s` | `NASA` | `William_Herschel01_hires -> PIA18182 -> weic2310a_unannotated` | WHO #4: William Herschel (1738–1822) — British astronomer · WHEN: 13 Mar 1781 · SCALE: Softball vs nickel |
| `R41` | `525.00` | `547.35` | `22.35s` | `CODE` | `code_graphic_064_r51_uranus_tilt.mp4` | DATA #7a + SCALE + FACT #4: 97.77° vs Earth 23.4° (>4×), 17h spin, 21-year winter on 84-year orbit · NUMBER OBJECT (Ch 7) |
| `R42` | `547.35` | `553.95` | `6.60s` | `NASA` | `PIA02963_borderless -> PIA01488` | WHEN: 24 Jan 1986 Voyager 2 only visit (kept distinct from atmospheric minimum) |
| `R43` | `553.95` | `581.75` | `27.80s` | `CODE` | `code_graphic_064_r54_uranus_cold_core.mp4` | DATA #7b: −224.2 °C minimum (in some places), ~60° magnetic tilt, >=80% hot dense fluid up to 4,982 °C |
| `R44` | `581.75` | `584.44` | `2.69s` | `NASA` | `r55_cut3_pia01488_pushin_silent` | Real 033 Voyager 2 cloud push-in transition to Neptune |
| `C08` | `585.00` | `585.22` | `0.22s` | `CARD` | `code_graphic_064_ch08_card_neptune.mp4` | CHAPTER CARD 08 / 08 · NEPTUNE — Supersonic Winds at the Edge (breath 0.60 s after S65) |
| `R45` | `585.22` | `613.55` | `28.33s` | `NASA` | `PIA01492 -> PIA00046` | Real Voyager 2 Neptune full azure globe & scooter clouds · SCALE: Baseball vs nickel · WHEN: 2011 full orbit |
| `R46` | `613.55` | `644.45` | `30.90s` | `NASA` | `Urbain_Le_Verrier -> Johann_Gottfried_Galle -> William_Lassell` | WHO #5–7: Le Verrier (1811–1877), Galle (1812–1910), Lassell (1799–1880) (framed PD portraits over starfield) · WHEN: 23 Sep 1846, 10 Oct 1846 |
| `R47` | `644.45` | `653.20` | `8.75s` | `NASA` | `PIA01492` | WHEN: 25 Aug 1989 Voyager 2 flyby (real Neptune plate before wind graphic) |
| `R48` | `653.20` | `669.90` | `16.70s` | `CODE` | `code_graphic_064_r60_neptune_winds.mp4` | DATA #8a + SCALE: >2,000 km/h winds vs 408 km/h Olivia (Roughly 5× gust), 30 AU / 900× dimmer, Triton >8 km geysers · NUMBER OBJECT (Ch 8) |
| `R49` | `669.90` | `683.86` | `13.96s` | `NASA` | `File_Video_NH_Pluto_Flyby -> PIA19952` | WHEN: Jul 2015 New Horizons Pluto Sputnik Planitia hand-off to OWB:034 |
| `R50` | `683.86` | `691.86` | `8.00s` | `CODE` | `code_graphic_064_r62_solar_comparison_timeline.mp4` | Completed 8-planet comparison + Exploration Timeline (1610–2024) + PIA02215 farewell crescent inset (first 8 s of hold) |
| `R51` | `691.86` | `701.86` | `10.00s` | `NASA` | `File_Sputnik_Planum_unannotated -> File_Video_NH_Pluto_Flyby` | [End screen hold & fade — moving picture + music 18 s past last word, zero goodbye/subscribe graphic] |
