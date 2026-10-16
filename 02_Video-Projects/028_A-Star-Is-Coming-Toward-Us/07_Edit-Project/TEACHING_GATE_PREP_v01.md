# 028 Gliese 710 — Per-Chapter Teaching Gate & Overlay Prep Sheet (`J0360`)

Prepared by Gemini (`gemini-agy`, 16 Oct 2026) for Chief and the Orbit Auditor. **Advisory only: Chief scores the gate.** Rule: `AGENTS.md` *Reference lessons* item 6 (Chief ruling 12 Oct: a to-scale graphic with no numeral does NOT count as `NUMBER`; a numeral for a spoken number is a `WORDS` pass; labels are 4 words or fewer from the VO's own words, checked against `01_Script/SOURCES.md`).

---

## 1. Eligibility Audit Across Unuploaded OWB Longs (`024`–`032`)

| Film | VO Locked? | Rough Cut Exists? | Uploaded? | Teaching Overlays Status |
|---|---|---|---|---|
| **024** Near Light Speed | Yes | Yes (`v05d`) | No (Private dry-run PASS) | **Chief PASS** (`J0147`, `39733487`; `v05d` `J0149`). Every chapter (`Open` + `1`–`5`) has a numeral-bearing object. |
| **025** Mars Robot | Yes | Yes (`v03f`) | **Yes** (`Js6EQJ8qDi8`, `J0084`) | Uploaded and designated control (`AGENTS.md`: *"025 Mars stays the control"*). |
| **026** Nearest Star | Yes | Yes (`v05d`) | No (Private dry-run PASS) | **Chief PASS** (`J0148`, `6130700438`). Every chapter (`Open` + `1`–`5`) has a numeral-bearing object + Bessel WHO card. |
| **027** Earth Stopped Spinning | Yes | Yes (`v01l`) | No (Private dry-run PASS) | **Chief PASS** (`J0154` Ch `1`–`5`, `6874d711`; `J0256` `Open`, `3e0c8dab`; `v01l` corner credits `J0319`). Every chapter (`Open` + `1`–`5`) has a numeral-bearing object. |
| **028** A Star Is Coming Toward Us | **Yes** (`star_coming_vo_v01`) | **No** (boards `v02` `J0337`, code graphics `v02` `J0338` PASS, harvest `v01` `J0350` PASS; awaits 2 Flow Veo + 2 Omni plates) | No | Chapters `0`–`2` carry numerals in `code_graphics_v02`; **Chapters `3`–`6` lack numeral-bearing objects** because their spoken numbers fall on `harvest`/`omni` plates. Prep table below. |
| **029** Is Betelgeuse About to Explode | **Yes** (`betelgeuse_vo_v01`) | **No** (boards `v02` `J0346`, code graphics `v01` `J0347` PASS; harvest `v01` `J0353` parked for Chief; awaits 2 Omni plates) | No | Chapters `0`, `2`, `5` carry numerals (`2019`, `2020`, `100,000 years`, `1054`); Chapters `1`, `3`, `4` use spelled-out number words in `code_graphics_v01` (note in §4). |
| **030** Apophis | No (script `v02` locked) | No | No | Awaits VO after 30 Oct ElevenLabs reset. |
| **031** Magnetic Field Flip | No (script `v03` locked, `J0340` PASS) | No | No | `J0345` blocked on 30 Oct ElevenLabs reset (119 chars left vs 7,765 needed). |
| **032** Titan Landing | No (script `v01` locked, `J0301` PASS) | No | No | `J0302` blocked on 30 Oct ElevenLabs reset (119 chars left vs 8,139 needed; noted in `J0300`). |

- **Why no video render or `picture_qa` runs in `J0360`:** Every VO-locked unuploaded long that already has a cut (`024`, `026`, `027`) has already received **Chief PASS** on all chapters (`Open` + `1`–`5`). The newest VO-locked longs (`028` and `029`) have no assembled rough cut yet (`picture_qa.py` and before/after cut stills require an assembled cut `.mp4` and `cuts.json`), and Mini free disk space is currently `15 GiB` (below the `20 GB` preflight threshold).

---

## 2. `028` Gliese 710 — Chapter-by-Chapter Teaching Gate Audit (`PLATE_BOARDS_v02.json` + `code_graphics_v02`)

All timings come from `07_Edit-Project/PLATE_BOARDS_v02.json`, `07_Edit-Project/build_code_graphics_v02.py`, and the locked Scribe transcript `02_Voiceover/stt/star_coming_vo_v01/star_coming_vo_v01_scribe_v2.json`.

| Chapter | Film time (s) | Existing numeral-bearing object(s) in `code_graphics_v02` (`J0338`) | `NUMBER` (current) | `WORDS` (current) |
|---|---|---|---|---|
| **0 Open** | `0.12–41.86` | `r04_shower_shell` (`18.02–30.14 s`): `"1.3 million years"` at `+0.9–4.0 s` (`18.92–22.02 s`) | **PASS** | **PASS** |
| **1 The Star Heading Our Way** | `42.78–126.04` | `r07_kdwarf` (`54.30–57.54 s`): `"60% Sun’s mass"` at `+0.1–3.2 s` (`54.40–57.50 s`) + calibrated mass bars | **PASS** | **PASS** |
| **2 How Close Will It Come?** | `126.90–209.44` | `r14_hipparcos_card` (`134.58–146.98 s`): `"Late 1990s"`, `"About 1 light-year"`; `r15_16_path` (`154.00–169.80 s`): `"1/5 light-year"`; `r17_scale_a` (`175.50–181.50 s`): `"Sun–Earth: 1 cm"`; `r18_shell` (`195.68–203.76 s`): `"100 metres"` | **PASS** | **PASS** |
| **3 Into the Oort Cloud** | `210.34–280.58` | None with a numeral. `r20_21_oort_shell` (`210.34–232.84 s`) has `"Trillions of frozen bodies"` (word, no digit); `r24_25_shower` (`257.00–280.58 s`) has text-only labels. Spoken numbers `"100,000"` (`248.74 s`, `r23_orbit_ice`) and `"eight minutes"` (`253.00 s`, `r24_sunrise`) sit on non-code plates. | **FAIL** (needs overlay) | **PASS** |
| **4 The Comet Shower** | `281.74–335.00` | None with a numeral. `r27_shower` (`294.48–305.00 s`) and `r28_hale_bopp_2` (`328.80–335.00 s`) have text-only labels. Spoken numbers `"about 10 extra comets a year"` (`285.02–287.06 s`, `r26_hale_bopp`) and `"three to four million years"` (`291.38–293.52 s`, `r26_a3`) sit on harvest plates. | **FAIL** (needs overlay) | **PASS** |
| **5 A New Brightest Star** | `335.84–377.30` | None with a numeral. `r29_sky`, `r31_sky`, `r31_sky_fade` carry text-only labels (`"Brightest star"`, `"Creep across the sky"`, `"Fade and drift away"`). Spoken numbers `"about three times brighter"` (`348.14–349.38 s`, `r29_twilight`) and `"every 35 years"` (`371.50–372.96 s`, `r31_moon_2`) sit on harvest plates. | **FAIL** (needs overlay) | **PASS** |
| **6 It Has Happened Before** | `378.30–472.84` | None with a numeral. `r33_traffic`, `r34_traffic`, `r37_shell` carry text-only labels. Spoken numbers `"About 70,000 years ago"` (`387.72–389.46 s`, `r33_wise_craft`) and `"about 2.8 million years ago"` / `"HD 7977"` (`403.46–411.16 s`, `r34_sky_wide`) sit on harvest plates. | **FAIL** (needs overlay) | **PASS** |

---

## 3. Proposed House Pill Overlays for `028` Chapters `3`–`6` (for Rough-Cut Assembly)

Each proposed overlay uses the house pill style (`NAVY = (23, 36, 55, 220)`, white Arial Bold `72–80 px`, `0.35 s` fade+rise in on the VO word's start, `0.30 s` fade out before the shot's cut, duration `1.8–3.8 s` ≤ `4.0 s`), sits on a `harvest` plate (never creating back-to-back code graphics), uses the VO's own consecutive words (`≤ 4` words, numerals for spoken numbers), and is verified against `01_Script/SOURCES.md`:

| Chapter | Plate (`PLATE_BOARDS_v02.json`) | Plate Window (s) | Overlay Window (s) | Label (`≤ 4` words, VO verbatim) | Scribe Word Timing | `01_Script/SOURCES.md` Check |
|---|---|---|---|---|---|---|
| **3 Into the Oort Cloud** *(next chapter without numeral)* | `r24_sunrise` (`harvest`, `iss042e214635`) | `251.18–257.00` | `252.76–255.20` (`2.44 s`) | **`In 8 minutes`** *(or `8 minutes` at `253.00–255.20`)* | `"in"` `252.76` · `"eight"` `253.00` · `"minutes,"` `253.30–253.74` | **Row 13 (MUST QUOTE):** NASA *Oort Cloud: Facts* verbatim: *"When light leaves the Sun, it takes a little over eight minutes to reach Earth"* ($\tau = 499.0\text{ s} = 8.32\text{ min}$ at $1\text{ AU}$). |
| **4 The Comet Shower** | `r26_hale_bopp` (`harvest`, `c2023a3_beletsky`) | `281.74–287.60` | `285.02–287.45` (`2.43 s`) | **`About 10 extra comets`** *(or `10 comets a year`)* | `"about"` `285.02` · `"10"` `285.32` · `"extra"` `285.80` · `"comets"` `286.18–286.52` | **Row 15 (MUST QUOTE):** Berski & Dybczyński (2016, *A&A* 595, L10) verbatim: *"an observable cometary shower with a mean density of approximately ten comets per year, lasting for 3 to 4 Myr."* |
| **4 The Comet Shower** | `r26_a3` (`harvest`, `c2023a3_landsat`) | `287.60–293.52` | `291.38–293.40` (`2.02 s`) | **`3 to 4 million`** | `"three"` `291.38` · `"to"` `291.84` · `"four"` `292.06` · `"million"` `292.50–292.90` | **Row 15 (MUST QUOTE):** Berski & Dybczyński (2016) verbatim: *"lasting for 3 to 4 Myr."* |
| **5 A New Brightest Star** | `r29_twilight` (`harvest`, `uhd_tl_paranal`) | `348.20–354.40` | `348.20–351.20` (`3.00 s`) | **`About 3 times brighter`** | `"about"` `348.14` · `"three"` `348.44` · `"times"` `348.74` · `"brighter"` `349.06–349.38` | **Row 18:** Berski & Dybczyński (2016) perihelion $V = -2.7\text{ mag}$ vs Sirius $V = -1.46\text{ mag}$ ($\Delta m = 1.24\text{ mag} \implies 3.13\times$ brighter). |
| **5 A New Brightest Star** | `r31_moon_2` (`harvest`, `GSFC_20171208_Archive_e001982`) | `369.00–373.20` | `371.04–373.05` (`2.01 s`) | **`Every 35 years`** | `"every"` `371.50` · `"35"` `371.96` · `"years."` `372.50–372.96` | **Row 20:** Berski & Dybczyński (2016) proper motion $52.28''\text{/yr}$; full Moon mean diameter $\sim 1,860'' \implies 35.58\text{ yr}$ per lunar width. |
| **6 It Has Happened Before** | `r33_wise_craft` (`harvest`, `PIA17254`) | `387.72–394.00` | `387.72–391.20` (`3.48 s`) | **`About 70,000 years ago`** | `"About"` `387.72` · `"70,000"` `388.22` · `"years"` `388.88` · `"ago,"` `389.12–389.46` | **Row 21:** Mamajek et al. (2015, *ApJL* 800, L17) verbatim: *"passed within only 52+23-14 kAU (0.25+0.11-0.07 parsec) of the Sun 70+15-10 kya"*. |
| **6 It Has Happened Before** | `r34_sky_wide` (`harvest`, `eso0932a`) | `403.30–412.00` | `403.46–407.20` (`3.74 s`) | **`2.8 million years ago`** | `"about"` `403.46` · `"2.8"` `403.94` · `"million"` `404.66` · `"years"` `405.06` · `"ago,"` `405.30–405.62` | **Row 22:** Bailer-Jones (2022, *ApJL* 935, L9) verbatim: *"The new second closest encounter took place 2.8 Myr ago: this was the G3 dwarf HD 7977"* ($t_{\text{ph}}^{\text{med}} = -2.761\text{ Myr}$). |

---

## 4. Note on `029` Betelgeuse (`code_graphics_v01`, `J0347`)

In `029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/build_code_graphics_v01.py`:
- **Chapter 0 (`Open`)**: `r03_r04_promise` carries `"in 2019"` (`NUMBER` PASS).
- **Chapter 1 (`The Star in Orion's Shoulder`)**: `r05_scale` is text-free (per Chief FIX 16 Oct) and `r09_finder` uses spelled-out `"three stars"` (`3.6–6.2 s`). At rough-cut overlay time (or via a 1-character numeral swap `"3 stars"` on `r09_finder`, or a house pill `"700 times wider"` / `"500 light-years"` on harvest plates `r06`/`r09`), Chapter 1 will need one numeral-bearing object.
- **Chapter 2 (`The Great Dimming`)**: `r10_r11_dip` carries `"February 2020"` (`NUMBER` PASS).
- **Chapter 3 (`How a Giant Star Dies`)**: `r17_r20_shells` carries `"less than a second"` (no digit) and `r21_hero` carries `"a mountain"`. At rough-cut overlay time, add a house pill with a numeral on a harvest plate (e.g. `"10 million years"` on `r17_sdo` `170.00–175.40 s`, or `< 1 second` / `"1 teaspoon"` if matching VO words).
- **Chapter 4 (`The Night It Goes`)**: `r29_span_astrolabe` carries spelled-out `"five hundred years"` (`11.1–14.3 s`) and `"hundred thousand years"` (`21.5–23.44 s`) — converting `"five hundred years"` to `"500 years"` (or `"100,000 years"`) in `LABELS["r29_span_astrolabe"]` gives Chapter 4 an immediate `NUMBER` PASS.
- **Chapter 5 (`So When?`)**: `r31_shells_twins` carries `"100,000 years"` and `r35_song` carries `"1054"` (`NUMBER` PASS).

---

## 5. Rendered Teaching Overlay Rows (`teaching_overlays_v01_pack/`, `J0375`)

Rendered by `07_Edit-Project/_overlay_gliese_v01.py` (`J0375`): 7 house pill overlays (`code_graphic_028_*.png`) across Chapters `3`–`6`, before/after reel (`/private/tmp/028_teaching_overlays_v01_{before,after}.mp4`), before/after contact sheet (`teaching_overlays_v01_pack/overlay_stills_028_v01.jpg`), and QA gate outputs:

```
WARN   0:09 row r26_hale_bopp comet_a3.jpg: low detail: edge density 0.0156 < film p5 0.0187
WARN   0:31 row r33_wise_craft wise_craft.jpg: kind of picture: 'NEOWISE spacecraft, artist concept (PIA17254)' (artist), look at it full size
picture QA PASS: 0 of 7 cuts fail, 2 to look at -> 02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/teaching_overlays_v01_pack/picture_qa_v01/PICTURE_QA.md, 02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/teaching_overlays_v01_pack/picture_qa_v01/picture_qa_review.jpg
polish gate PASS: 0 of 7 rows failed, 1 to look at -> 02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/teaching_overlays_v01_pack/polish_gate_v01.json
```

