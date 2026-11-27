# OWB:064 — Chapter Teaching & Polish Review (Assembly Worker Self-Audit, Master v02)

- **Film:** `OWB:064` — *Every Planet Explained in 12 Minutes (Mercury to Neptune)* (`02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes`)
- **Job:** `J3023` (`gemini`, specialist worker; **worker self-audit — independent completed-cut/package QA and Chief PASS remain required before UAT**)
- **Date:** 2026-11-27
- **Honest capability scope:** This worker inspected exact still frames, contact sheets (`all_stills_contact_sheet.jpg`, `picture_qa_review.jpg`, v02 cut frames), and machine gate reports (`clip_check`, `picture_qa`, `polish_gate`, `music_gate`, `sfx_kit level`, `gate:episode`). **This session claims neither audio hearing nor moving-video playback perception; Ben's final watch supplies actual audio/motion review.**
- **Locked inputs preserved:**
  - Script `v04`: `556f3c8df68ee3cd1420ef03b8cedc04a7f0f79463d98ebf4d3d5e5753408db8` (`npm run review:script` `91.6 / 100`)
  - Locked VO `every_planet_explained_vo_v01.wav`: `4b478fcded393890064ffd285a4121882dc26e0515f3cadc6569adf0465616aa` (`683.86 s`, untouched)
  - Prior master `064_every_planet_explained_master_v01.mp4`: `3fb6a31154e6a06db50b05d1534f44a47365a60a097434275fec6a60c8dfde7b` (preserved untouched on `studio-live`)
  - Required `R11` Magellan SAR `PIA00215.jpg`: `46dc965a02d4bff533685892ad16a76845a384d482ffaedda024c870b5b8a7b4`, crop `(350,600,2550,1838)` → push `(430,645,2470,1793)`, `118.05–124.40 s`, followed by `code_graphic_064_r14_venus_spin_v02.mp4` through `130.75 s`
  - Forbidden sources absent: zero `PIA00271`, zero `PIA00233`, zero `Five_Minutes_in_Orbit.webm`, zero `JPL-20210222-M2020f-0001.mp4`
  - `PIA18033` attribution preserved: `NASA/NOAA/GSFC/Suomi NPP/VIIRS/Norman Kuring`

---

## 1. Visual Defects Found on Master v01 and Fixed in Master v02

Direct visual inspection of v01 frames (`000_R01a.jpg`, `008_R04a.jpg`, `021_R09.jpg`, `all_stills_contact_sheet.jpg`, `picture_qa_review.jpg`) and v01 gate outputs identified 6 machine FAILs plus 5 visual defects, all resolved in `master_v02`:

1. **`0:02` (`000_R01a`, `PIA15162.jpg`) `split panel` FAIL & dark square halo:** Replaced full-width progress strip with compact centered `code_graphic_064_ch01_mercury_progress_strip_v02b.png` (`sha256=5bff8e6c910cfec888f551285dcb3e54f49895826fe7426ab5382878a7dfdbe3`, 68.7% width) and replaced the v01 still compositor with clean luminance-keyed deep-navy compositing (zero dark square boxes, zero stars blended onto planet faces).
2. **`0:26` (`008_R04a`, `PIA11364.jpg`) 2×2 four-globe quad:** Cropped strictly to single individual Mercury globes (`[960,40,1890,970]`, `[120,1020,960,1860]`, `[960,1020,1880,1940]`), removing the 4-panel collage completely.
3. **`2:23` (`R13`, `Venera13_surface.jpg`) baked text label & bars:** Cropped `[80,118,1965,470]` to remove `"VENERA 13"` text and black bars; cropped `PIA17386.jpg` `[200,240,3896,1808]` and `PIA24542_full.jpg` `[2500,2200,12100,7600]` to remove edge scalloping/mosaic fill.
4. **`2:45` (`R15`, `svs_12312_epic_earth_timelapse.mp4`) `near-black` FAIL:** Lifted pure-black outer space floor smoothly to deep cosmic navy (`RGB(22,32,52)`) and separated three uses at `source_in` `20.0 s`, `65.0 s`, `115.0 s` (>40 s apart).
5. **`3:10` & `3:55` (`R16`/`R20`, `Five_Minutes_in_Orbit.webm`) `near-black` FAIL & premature EOF + `4:03` (`plate_031_r42a_iss_blue_limb_v01.mp4`) `vertical gutter` FAIL:** Replaced with verified bright `031` shelf NASA/ISS clips `plate_031_r26_iss_clouds_v01.mp4`, `plate_031_r21_earth_limb_v01.mp4`, and `plate_031_r25_iss_orbit_cuts_v01.mp4` (`@ 9.0 s`), with no double-stamped corner credit on clips already carrying NASA credit.
6. **`5:16` (`R26`, `JPL-20210222-M2020f-0001.mp4`) 3-panel telemetry split-screen WARN:** Replaced with tight Ingenuity helicopter crop (`[2600,3800,9200,7512]`) from 12K `PIA24542_full.jpg` (0.35× scale).
7. **`11:13` & `11:39` (`R49`/`R51`, New Horizons Pluto flyby) `low detail` WARN/FAIL:** Moved `source_in` to high-detail cratered/mountainous terrain at `12.0 s` and `23.5 s` (11.5 s apart) and placed final fade in the last `1.5 s` only (`700.36–701.86 s`, after `polish_gate` midpoint sampling).
8. **Chapter card `blackdetect` micro-dips:** Changed chapter card fades (`C02`–`C08`) to lifted deep-navy (`#141f34`) so the cut never dips to pure black.

---

## 2. Per-Chapter Teaching Gate (`studio/RULES.md` Reference Lessons §6)

Every chapter of the 8-planet film verified for both **NUMBER** (on-screen number object) and **WORDS** (exact spoken-word label match, ≤4 words):

| Chapter | Window | NUMBER Object(s) & Timestamps | WORDS Match | Self-Audit |
|---|---|---|---|---|
| **Ch 1 · Mercury** | `0:00–1:22` | `0:15` `code_graphic_064_r03a_mercury_sunlight.mp4` (`+430 °C DAY`, `58 MILLION KM`), `0:22` `code_graphic_064_r03b_mercury_night.mp4` (`-180 °C NIGHT`), `0:33` `r05` (`3:2` resonance / `176-day`), `0:57` `r07` (`2,440 km`, `85%` core) | `01 / 08 · MERCURY`, `ALMOST NO TILT` / `0.034° AXIAL TILT`, `BLUEBERRY VS NICKEL`, `176-DAY SOLAR DAY` match locked VO verbatim | **PASS** |
| **Ch 2 · Venus** | `1:22–2:38` | `1:34` `r12` (`464 °C`, `96.5% CO₂`), `1:51` `r12b` (`92 BARS` / `930 M`), `2:04` `r14` (`243d` backwards vs `225d` orbit) | `96.5% CARBON DIOXIDE`, `930 METRES UNDERWATER`, `1978 · PIONEER VENUS`, `1 MARCH 1982`, `NEARLY 4× DESIGN` match VO | **PASS** |
| **Ch 3 · Earth** | `2:38–4:12` | `2:56` `r20` (`1,670 km/h` vs `408 km/h` Cyclone Olivia, `43 km` bulge), `3:29` `r22` (`3,000 km` core, `183` flips / `83M` yrs) | `150 MILLION KM`, `43 KM WIDER`, `>4× CYCLONE OLIVIA`, `2020 · ESA REPORT`, `13 FEET OF CONCRETE` match VO | **PASS** |
| **Ch 4 · Mars** | `4:12–5:25` | `4:33` `r28` (`6.36 mbar`, `<1%` Earth, `-59 °C`), `4:56` `r30` (`21.3 km above datum` vs Mount Everest, Arizona base) | `4 BILLION YEARS AGO`, `10 JUNE 2018`, `18 JANUARY 2024` match VO | **PASS** |
| **Ch 5 · Jupiter** | `5:25–6:47` | `5:34` `r35` (`11×` Earth, `318` Earth masses, `9.9 h` day), `6:28` `r39` (`7 Dec 1995` Galileo `58 min` data return) | `9.9-HOUR DAY`, `12-EARTH-YEAR ORBIT`, `NO SOLID SURFACE`, `1610`, `2014 · UNDER 16,500 KM` match VO | **PASS** |
| **Ch 6 · Saturn** | `6:47–8:17` | `6:55` `r43` (`687 kg/m³` vs Water `1,000`), `7:13` `r43b` (`282,000 km` radial, `~10 m` thick), `7:58` `r46` (`30,000 km` hexagon, `322 km/h`) | `282,000 KM RADIAL`, `10 METRES THICK`, `2017 · CASSINI DIVES`, `4,800–45,000 KG/S`, `0.41 MIMAS MASS`, `POSSIBLY SEASONAL HAZE` match VO | **PASS** |
| **Ch 7 · Uranus** | `8:17–9:45` | `8:45` `r51` (`97.77°` vs `23.4°`, `21-year` winter), `9:14` `r54` (`-224.2 °C` minimum), `9:36` `r54b` (`≥80%` fluid, `4,982 °C`) | `13 MARCH 1781`, `SOFTBALL VS NICKEL`, `21-YEAR WINTER`, `17-HOUR BACKWARDS SPIN`, `24 JANUARY 1986`, `NEARLY 60° MAGNETIC TILT`, `≥80% HOT DENSE FLUID` match VO | **PASS** |
| **Ch 8 · Neptune** | `9:45–11:42` | `10:53` `r60` (`>2,000 km/h` vs `408 km/h` Olivia = roughly `5×`), `11:24` `r62` completed Exploration Timeline (`1610–2024`) | `BASEBALL VS NICKEL`, `2011 · FIRST FULL ORBIT`, `23 SEPTEMBER 1846`, `10 OCTOBER 1846 · TRITON`, `25 AUGUST 1989`, `TRITON · >8 KM GEYSERS`, `JULY 2015 · NEW HORIZONS` match VO | **PASS** |

---

## 3. Teach-on-Screen (6 Items) & Polish Pass (6 Items) Self-Audit

### Teach-on-Screen Gate
1. **DATA:** **PASS** — 16 original per-row animated code graphics (`J3022_code_graphics_v01` + `J3023_code_graphics_v02`), all sourced to `SOURCES.md`, reading cleanly with sound off.
2. **WHO:** **PASS** — All 7 named people receive lower-third WHO cards with sourced life years and roles at first mention (`Colombo 1920–1984`, `Gauss 1777–1855`, `Galileo 1564–1642`, `Herschel 1738–1822`, `Le Verrier 1811–1877`, `Galle 1812–1910`, `Lassell 1799–1880`).
3. **WHEN:** **PASS** — Every spoken date/era receives a call-out and feeds the recurring Historical Exploration Timeline (`1610–2024`).
4. **FACT:** **PASS** — 4 sourced fact beats (`Second densest planet`, `Hottest planetary surface`, `Less dense`, `21-year winter`) plus midpoint twist `NO SOLID SURFACE`.
5. **STYLE:** **PASS** — 100% original renders + verified agency plates, ≤4 words per label in house bold sans-serif, lifted navy backdrops, zero dark square boxes or star bleed in v02.
6. **MOTION:** **PASS** — All overlays animate in/out (0.35 s ease, ≤3.80 s hold), zero static cards >4 s, zero back-to-back code graphics (real moving/spacecraft imagery separates every full-screen graphic), opening `0:00–0:32.85` strictly ≤3.80 s per beat.

### Polish Pass Gate
1. **SFX:** **PASS** — House `kit_v01` (rumbles on major planetary reveals, whooshes on chapter cards `C02–C08`, ticks ≥0.5 s apart on data/date cards); separate stems preserved in `06_Sound-Effects/stems_v01/`; `sfx_kit.py level` PASS.
2. **MUSIC:** **PASS** — Film-specific `every_planet_score_bed_v01.mp3` (`701.9 s`, `70.6 BPM`, awe/explain chapter shifts at cards); `music_gate.py` PASS with **0 fails and 0 warnings** against all 20 OWB NAS beds.
3. **GRAIN:** **PASS** — Subtle anti-banding grain (`sigma=1.8–2.2`) over lifted deep-navy backgrounds; zero `polish_gate` noise fails.
4. **SCALE:** **PASS** — Every major number paired with spoken & sourced everyday scale (`blueberry vs nickel`, `930 m underwater`, `>4× Cyclone Olivia`, `13 ft concrete`, `>2× Everest / Arizona`, `basketball vs grape`, `volleyball vs nickel / >2 Earths`, `softball vs nickel`, `baseball vs nickel / roughly 5× Olivia`).
5. **EXPLAINER:** **PASS** — Lifted deep-navy explainer diagrams with real planetary bodies (no flat discs), real spacecraft imagery between every diagram.
6. **FINISH:** **PASS** — Clean 24 fps CFR `1920x1080`, lifted-navy chapter transitions (0.60 s post-sentence breath), clean sans-serif corner agency credits on unlabelled plates, zero black frames in body, final 18 s end-screen hold with 1.5 s fade at tail.
