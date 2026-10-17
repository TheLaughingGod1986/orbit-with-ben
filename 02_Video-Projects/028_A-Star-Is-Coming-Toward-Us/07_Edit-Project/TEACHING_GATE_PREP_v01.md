# 028 Gliese 710 — Per-Chapter Teaching Gate & Overlay Prep Sheet (`J0360` / `J0375` / `J0408` / `J0425` / `J0443`)

Prepared by Gemini (`gemini-agy`, 17 Oct 2026) for Chief and the Orbit Auditor. **Advisory only: Chief scores the gate.** Rule: `AGENTS.md` *Reference lessons* item 6 (Chief ruling 12 Oct: a to-scale graphic with no numeral does NOT count as `NUMBER`; a numeral for a spoken number is a `WORDS` pass; labels are 4 words or fewer from the VO's own words, checked against `01_Script/SOURCES.md`).

---

## 1. Eligibility Audit Across Unuploaded OWB Longs (`024`–`032`)

| Film | VO Locked? | Rough Cut Exists? | Uploaded? | Teaching Overlays Status |
|---|---|---|---|---|
| **024** Near Light Speed | Yes | Yes (`v05d`) | No (Private dry-run PASS) | **Chief PASS** (`J0147`, `39733487`; `v05d` `J0149`). Every chapter (`Open` + `1`–`5`) has a numeral-bearing object. |
| **025** Mars Robot | Yes | Yes (`v03f`) | **Yes** (`Js6EQJ8qDi8`, `J0084`) | Uploaded and designated control (`AGENTS.md`: *"025 Mars stays the control"*). |
| **026** Nearest Star | Yes | Yes (`v05d`) | No (Private dry-run PASS) | **Chief PASS** (`J0148`, `6130700438`). Every chapter (`Open` + `1`–`5`) has a numeral-bearing object + Bessel WHO card. |
| **027** Earth Stopped Spinning | Yes | Yes (`v01l`) | No (Private dry-run PASS) | **Chief PASS** (`J0154` Ch `1`–`5`, `6874d711`; `J0256` `Open`, `3e0c8dab`; `v01l` corner credits `J0319`). Every chapter (`Open` + `1`–`5`) has a numeral-bearing object. |
| **028** A Star Is Coming Toward Us | **Yes** (`star_coming_vo_v01`) | **No** (boards `v02` `J0337`, code graphics `v02` `J0338` PASS, harvest `v01` `J0350` PASS; awaits 2 Flow Veo + 2 Omni plates) | No | Chapters `0`–`6` covered by `code_graphics_v02` + 13 rendered house pill overlays across 12 rows in `028/07_Edit-Project/teaching_overlays_v01_pack/`. |
| **029** Is Betelgeuse About to Explode | **Yes** (`betelgeuse_vo_v01`) | **No** (boards `v02` `J0346`, code graphics `v01` `J0347` PASS; harvest `v01` `J0353` parked for Chief; awaits 2 Omni plates) | No | Chapters `0`–`5` covered by `code_graphics_v01` + 15 rendered house pill overlays across 13 rows in `029/07_Edit-Project/teaching_overlays_v01_pack/`. |
| **030** Apophis | No (script `v02` locked) | No | No | Awaits VO after 30 Oct ElevenLabs reset. |
| **031** Magnetic Field Flip | No (script `v03` locked, `J0340` PASS) | No | No | `J0345` blocked on 30 Oct ElevenLabs reset (119 chars left vs 7,765 needed). |
| **032** Titan Landing | No (script `v01` locked, `J0301` PASS) | No | No | `J0302` blocked on 30 Oct ElevenLabs reset (119 chars left vs 8,139 needed; noted in `J0300`). |

---

## 2. `028` Gliese 710 — Chapter-by-Chapter Teaching Gate Audit (`PLATE_BOARDS_v02.json` + `code_graphics_v02`)

All timings come from `07_Edit-Project/PLATE_BOARDS_v02.json`, `07_Edit-Project/build_code_graphics_v02.py`, and the locked Scribe transcript `02_Voiceover/stt/star_coming_vo_v01/star_coming_vo_v01_scribe_v2.json`.

| Chapter | Film time (s) | Existing numeral-bearing object(s) in `code_graphics_v02` (`J0338`) | `NUMBER` (before) | `NUMBER` (with `v01` overlays) | `WORDS` |
|---|---|---|---|---|---|
| **0 Open** | `0.12–41.86` | `r04_shower_shell` (`18.02–30.14 s`): `"1.3 million years"` at `+0.9–4.0 s` (`18.92–22.02 s`) | **PASS** | **PASS** (`18.92–22.02 s`) | **PASS** |
| **1 The Star Heading Our Way** | `42.78–126.04` | `r07_kdwarf` (`54.30–57.54 s`): `"60% Sun’s mass"` at `+0.1–3.2 s` (`54.40–57.50 s`) + calibrated mass bars; plus `r06_milky_way` pill `"62 light-years away"` (`45.08–48.00 s`) | **PASS** | **PASS** (`45.08–48.00 s`, `54.40–57.50 s`) | **PASS** |
| **2 How Close Will It Come?** | `126.90–209.44` | `r14_hipparcos_card` (`134.58–146.98 s`): `"Late 1990s"`, `"About 1 light-year"`; `r15_16_path` (`154.00–169.80 s`): `"1/5 light-year"`; `r17_scale_a` (`175.50–181.50 s`): `"Sun–Earth: 1 cm"`; `r18_shell` (`195.68–203.76 s`): `"100 metres"`; plus harvest pills `"In 1 million years"` (`128.08–130.80 s`), `"1 billion stars"` (`151.54–153.80 s`), `"5 times closer"` (`172.40–175.10 s`), `"30 centimetres away"` (`184.54–186.35 s`) | **PASS** | **PASS** (`128.08–203.76 s`) | **PASS** |
| **3 Into the Oort Cloud** | `210.34–280.58` | None with a numeral. `r20_21_oort_shell` (`210.34–232.84 s`) has `"Trillions of frozen bodies"` (word, no digit); `r24_25_shower` (`257.00–280.58 s`) has text-only labels. Spoken numbers `"100,000"` (`248.74 s`, `r23_orbit_ice`) and `"eight minutes"` (`253.00 s`, `r24_sunrise`) sit on non-code plates. | **FAIL** (needs overlay) | **PASS** (`252.76–255.20 s` `"In 8 minutes"`) | **PASS** |
| **4 The Comet Shower** | `281.74–335.00` | None with a numeral. `r27_shower` (`294.48–305.00 s`) and `r28_hale_bopp_2` (`328.80–335.00 s`) have text-only labels. Spoken numbers `"about 10 extra comets a year"` (`285.02–287.06 s`, `r26_hale_bopp`) and `"three to four million years"` (`291.38–293.52 s`, `r26_a3`) sit on harvest plates. | **FAIL** (needs overlay) | **PASS** (`285.02–287.45 s` `"About 10 extra comets"`, `291.38–293.40 s` `"3 to 4 million"`) | **PASS** |
| **5 A New Brightest Star** | `335.84–377.30` | None with a numeral. `r29_sky`, `r31_sky`, `r31_sky_fade` carry text-only labels (`"Brightest star"`, `"Creep across the sky"`, `"Fade and drift away"`). Spoken numbers `"about three times brighter"` (`348.14–349.38 s`, `r29_twilight`) and `"every 35 years"` (`371.50–372.96 s`, `r31_moon_2`) sit on harvest plates. | **FAIL** (needs overlay) | **PASS** (`348.20–351.20 s` `"About 3 times brighter"`, `371.04–373.05 s` `"Every 35 years"`) | **PASS** |
| **6 It Has Happened Before** | `378.30–472.84` | None with a numeral. `r33_traffic`, `r34_traffic`, `r37_shell` carry text-only labels. Spoken numbers `"About 70,000 years ago"` (`387.72–389.46 s`, `r33_wise_craft`) and `"about 2.8 million years ago"` / `"HD 7977"` (`403.46–411.16 s`, `r34_sky_wide`) sit on harvest plates. | **FAIL** (needs overlay) | **PASS** (`387.72–391.20 s` `"About 70,000 years ago"`, `403.46–407.20 s` `"2.8 million years ago"`, `408.80–411.50 s` `"HD 7977"`) | **PASS** |

---

## 3. Rendered House Pill Overlays for `028` Chapters `1`–`6` (`teaching_overlays_v01_pack/`, 12 rows / 13 pills)

Each rendered overlay uses the house pill style (`NAVY = (23, 36, 55, 220)`, white Arial Bold `76–78 px`, `0.35 s` fade+rise in on the VO word's start, `0.30 s` fade out before the shot's cut, duration `1.81–3.74 s` ≤ `4.0 s`), sits on a `harvest` plate (never creating back-to-back code graphics), uses the VO's own consecutive words (`≤ 4` words, numerals for spoken numbers), and is verified against `01_Script/SOURCES.md`:

| Chapter | Plate (`PLATE_BOARDS_v02.json`) | Plate Window (s) | Overlay Window (s) | Label (`≤ 4` words, VO verbatim) | Scribe Word Timing | `01_Script/SOURCES.md` Check |
|---|---|---|---|---|---|---|
| **1 The Star Heading Our Way** | `r06_milky_way` (`harvest`, `eso_mw_lasilla.mp4`) | `42.78–50.10` | `45.08–48.00` (`2.92 s`) | **`62 light-years away`** | `"62"` `45.42` · `"light-years"` `46.08` · `"away,"` `46.54–46.90` | **Row 2:** Bailer-Jones (2022, *ApJL* 935, L9) Gaia DR3 parallax $52.433\text{ mas}$ ($19.072\text{ pc} = 62.20\text{ ly}$ in Serpens). |
| **2 How Close Will It Come?** | `r13_star_trails` (`harvest`, `eso_startrails.mp4`) | `126.90–133.84` | `128.08–130.80` (`2.72 s`) | **`In 1 million years`** | `"in"` `128.08` · `"a"` `128.18` · `"million"` `128.28` · `"years?"` `128.66–129.00` | **Row 1:** Bailer-Jones (2022, *ApJL* 935, L9) closest approach in $1.292\text{ Myr}$ (90% CI $1.257\text{--}1.334\text{ Myr}$). |
| **2 How Close Will It Come?** | `r15_gaia_craft` (`harvest`, `gaia_craft.jpg`) | `147.76–154.00` | `151.54–153.80` (`2.26 s`) | **`1 billion stars`** | `"a"` `151.96` · `"billion"` `152.10` · `"stars"` `152.50–152.90` | **Row 9:** Gaia Collaboration, Vallenari et al. (2023, *A&A* 674, A1) Gaia DR3 1.806 billion sources. |
| **2 How Close Will It Come?** | `r16_sunrise_break` (`harvest`, `iss_sunrise.jpg` horizon crop) | `169.80–175.50` | `172.40–175.10` (`2.70 s`) | **`5 times closer`** | `"five"` `172.56` · `"times"` `172.92` · `"closer"` `173.26–173.65` | **Row 10:** Bailer-Jones (2022, *ApJL* 935, L9) Hipparcos $\sim 0.311\text{ pc}$ vs Gaia DR3 $0.0636\text{ pc}$ ($\sim 4.89\times$, five times closer). |
| **2 How Close Will It Come?** | `r17_neptune` (`harvest`, `neptune.jpg`) | `181.50–186.50` | `184.54–186.35` (`1.81 s`) | **`30 centimetres away`** | `"30"` `184.84` · `"centimeters"` `185.28` · `"away."` `185.92–186.30` | **Row 11:** NASA *Neptune Fact Sheet* $a = 30.07\text{ AU} \implies 30.1\text{ cm}$ at $1\text{ AU} = 1\text{ cm}$ scale. |
| **3 Into the Oort Cloud** | `r24_sunrise` (`harvest`, `iss042e214635`) | `251.18–257.00` | `252.76–255.20` (`2.44 s`) | **`In 8 minutes`** | `"in"` `252.76` · `"eight"` `253.00` · `"minutes,"` `253.30–253.74` | **Row 13 (MUST QUOTE):** NASA *Oort Cloud: Facts* verbatim: *"When light leaves the Sun, it takes a little over eight minutes to reach Earth"* ($\tau = 499.0\text{ s} = 8.32\text{ min}$ at $1\text{ AU}$). |
| **4 The Comet Shower** | `r26_hale_bopp` (`harvest`, `c2023a3_beletsky`) | `281.74–287.60` | `285.02–287.45` (`2.43 s`) | **`About 10 extra comets`** | `"about"` `285.02` · `"10"` `285.32` · `"extra"` `285.80` · `"comets"` `286.18–286.52` | **Row 15 (MUST QUOTE):** Berski & Dybczyński (2016, *A&A* 595, L10) verbatim: *"an observable cometary shower with a mean density of approximately ten comets per year, lasting for 3 to 4 Myr."* |
| **4 The Comet Shower** | `r26_a3` (`harvest`, `c2023a3_landsat`) | `287.60–293.52` | `291.38–293.40` (`2.02 s`) | **`3 to 4 million`** | `"three"` `291.38` · `"to"` `291.84` · `"four"` `292.06` · `"million"` `292.50–292.90` | **Row 15 (MUST QUOTE):** Berski & Dybczyński (2016) verbatim: *"lasting for 3 to 4 Myr."* |
| **5 A New Brightest Star** | `r29_twilight` (`harvest`, `uhd_tl_paranal`) | `348.20–354.40` | `348.20–351.20` (`3.00 s`) | **`About 3 times brighter`** | `"about"` `348.14` · `"three"` `348.44` · `"times"` `348.74` · `"brighter"` `349.06–349.38` | **Row 18:** Berski & Dybczyński (2016) perihelion $V = -2.7\text{ mag}$ vs Sirius $V = -1.46\text{ mag}$ ($\Delta m = 1.24\text{ mag} \implies 3.13\times$ brighter). |
| **5 A New Brightest Star** | `r31_moon_2` (`harvest`, `GSFC_20171208_Archive_e001982`) | `369.00–373.20` | `371.04–373.05` (`2.01 s`) | **`Every 35 years`** | `"every"` `371.50` · `"35"` `371.96` · `"years."` `372.50–372.96` | **Row 20:** Berski & Dybczyński (2016) proper motion $52.28''\text{/yr}$; full Moon mean diameter $\sim 1,860'' \implies 35.58\text{ yr}$ per lunar width. |
| **6 It Has Happened Before** | `r33_wise_craft` (`harvest`, `PIA17254`) | `387.72–394.00` | `387.72–391.20` (`3.48 s`) | **`About 70,000 years ago`** | `"About"` `387.72` · `"70,000"` `388.22` · `"years"` `388.88` · `"ago,"` `389.12–389.46` | **Row 21:** Mamajek et al. (2015, *ApJL* 800, L17) verbatim: *"passed within only 52+23-14 kAU (0.25+0.11-0.07 parsec) of the Sun 70+15-10 kya"*. |
| **6 It Has Happened Before** | `r34_sky_wide` (`harvest`, `eso0932a`, pill 1) | `403.30–412.00` | `403.46–407.20` (`3.74 s`) | **`2.8 million years ago`** | `"about"` `403.46` · `"2.8"` `403.94` · `"million"` `404.66` · `"years"` `405.06` · `"ago,"` `405.30–405.62` | **Row 22:** Bailer-Jones (2022, *ApJL* 935, L9) verbatim: *"The new second closest encounter took place 2.8 Myr ago: this was the G3 dwarf HD 7977"* ($t_{\text{ph}}^{\text{med}} = -2.761\text{ Myr}$). |
| **6 It Has Happened Before** | `r34_sky_wide` (`harvest`, `eso0932a`, pill 2) | `403.30–412.00` | `408.80–411.50` (`2.70 s`) | **`HD 7977`** | `"called"` `408.52` · `"HD"` `409.04` · `"7977,"` `409.84–410.50` | **Row 22:** Bailer-Jones (2022, *ApJL* 935, L9) solar-type G3 dwarf `HD 7977` passed within $<0.05\text{ pc}$ ($P = 1/3$) $2.8\text{ Myr}$ ago. |

---

## 4. Gate Verification (`picture_qa.py` + `polish_gate.py`)

Rendered by `07_Edit-Project/_overlay_gliese_v01.py` (`J0443`): 13 house pill overlays across 12 rows (`code_graphic_028_r*.png`) across Chapters `1`–`6`, before/after reel (`/private/tmp/028_teaching_overlays_v01_{before,after}.mp4`), before/after contact sheet (`teaching_overlays_v01_pack/overlay_stills_028_v01.jpg`), and QA gate outputs:

```
WARN   0:17 row r15_gaia_craft gaia_craft.jpg: kind of picture: 'The Gaia spacecraft (artist's impression)' (artist), look at it full size
WARN   0:29 row r17_neptune neptune.jpg: low detail: edge density 0.0017 < film p5 0.0108
WARN   1:02 row r33_wise_craft wise_craft.jpg: kind of picture: 'NEOWISE spacecraft, artist concept (PIA17254)' (artist), look at it full size
picture QA PASS: 0 of 12 cuts fail, 3 to look at -> 02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/teaching_overlays_v01_pack/picture_qa_v01/PICTURE_QA.md, 02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/teaching_overlays_v01_pack/picture_qa_v01/picture_qa_review.jpg
polish gate PASS: 0 of 12 rows failed, 1 to look at -> 02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/teaching_overlays_v01_pack/polish_gate_v01.json
```


