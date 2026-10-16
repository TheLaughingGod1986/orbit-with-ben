# 029 Betelgeuse — Per-Chapter Teaching Gate & Overlay Sheet (`J0375`)

Prepared by Gemini (`gemini-agy`, 16 Oct 2026) for Chief and the Orbit Auditor. **Advisory only: Chief scores the gate.** Rule: `AGENTS.md` *Reference lessons* item 6 (Chief ruling 12 Oct: a to-scale graphic with no numeral does NOT count as `NUMBER`; a numeral for a spoken number is a `WORDS` pass; labels are 4 words or fewer from the VO's own words, checked against `01_Script/SOURCES.md`).

- **Average % viewed:** `UNKNOWN` (nobody has read Studio; the film is not uploaded yet).
- **Builder:** `07_Edit-Project/_overlay_betelgeuse_v01.py` (`--plan` prints the rows and checks; full run renders the before/after overlay reel to `/private/tmp/029_teaching_overlays_v01_{before,after}.mp4`, house pill PNGs `code_graphic_029_row*.png`, before/after contact sheet `teaching_overlays_v01_pack/overlay_stills_029_v01.jpg`, and runs `picture_qa.py` + `polish_gate.py`).

---

## 1. Chapter-by-Chapter Teaching Gate Audit (`PLATE_BOARDS_v02.json` + `code_graphics_v01`)

All timings come from `07_Edit-Project/PLATE_BOARDS_v02.json`, `07_Edit-Project/build_code_graphics_v01.py`, and the locked Scribe transcript `02_Voiceover/words.json`.

| Chapter | Film time (s) | Existing numeral-bearing object(s) in `code_graphics_v01` (`J0347`) | `NUMBER` (before) | `NUMBER` (with `v01` overlays) | `WORDS` |
|---|---|---|---|---|---|
| **0 Open** | `0.08–36.94` | `r03_r04_promise` (`13.96–36.94 s`): `"in 2019"` at `+13.10–15.10 s` (`27.06–29.06 s`) | **PASS** | **PASS** (`27.06–29.06 s`) | **PASS** |
| **1 The Star in Orion's Shoulder** | `37.74–105.48` | None with a numeral. `r05_scale` (`41.90–48.58 s`) is text-free (per Chief FIX 16 Oct); `r09_finder` (`92.92–105.48 s`) uses spelled-out `"three stars"` (`96.52–99.12 s`). Spoken numbers `"seven hundred light-years away"`, `"four and a half billion years old"`, `"fifteen to twenty times"`, and `"around a hundred thousand"` sit on harvest plates. | **FAIL** (needs numeral overlay) | **PASS** (`51.16–53.60 s`, `63.36–66.20 s`, `78.06–79.90 s`, `84.30–85.92 s`) | **PASS** |
| **2 The Great Dimming** | `106.38–168.98` | `r10_r11_dip` (`109.50–123.16 s`): `"February 2020"` at `+5.50–7.70 s` (`115.00–117.20 s`) | **PASS** | **PASS** (`115.00–117.20 s`) | **PASS** |
| **3 How a Giant Star Dies** | `170.00–247.18` | None with a numeral. `r17_r20_shells` (`175.40–224.02 s`) uses spelled-out `"less than a second"` (`212.00–215.20 s`, local `36.60–39.80 s`); `r21_hero` uses `"a mountain"`. | **FAIL** (needs numeral overlay) | **PASS** (`211.94–215.20 s` `"Less than 1 second"`) | **PASS** |
| **4 The Night It Goes** | `248.06–350.00` | None with a numeral. `r29_span_astrolabe` (`326.56–350.00 s`) uses spelled-out `"five hundred years"` (`337.66–340.86 s`, local `11.10–14.30 s`) and `"hundred thousand years"` (`348.06–350.00 s`, local `21.50–23.44 s`). | **FAIL** (needs numeral overlay) | **PASS** (`337.66–340.86 s` `"500 years"`) | **PASS** |
| **5 So When?** | `350.00–517.26` | `r31_shells_twins` (`359.36–378.30 s`): `"100,000 years"` at `+13.00–15.60 s` (`372.36–374.96 s`); `r35_song` (`432.60–442.00 s`): `"1054"` at `+3.50–6.00 s` (`436.10–438.60 s`) | **PASS** | **PASS** (`372.36–374.96 s`, `436.10–438.60 s`) | **PASS** |

---

## 2. Rendered Teaching Overlay Rows (`teaching_overlays_v01_pack/`)

Every rendered label uses the house pill style (`NAVY = (23, 36, 55, 220)`, white Arial Bold `76–78 px`, `0.35 s` fade+rise in on the VO word's start, `0.30 s` fade out before the shot's cut, duration `1.62–3.26 s` ≤ `4.0 s`), uses consecutive spoken words from `02_Voiceover/words.json` (`≤ 4` words, numerals for spoken numbers), stays in the lower/upper safe band clear of the central subject and the 512×512 jitter patch, and is verified against `01_Script/SOURCES.md` and `01_Script/CLAUDE_QUOTE_CHECK_v02.md`:

| Chapter | Row / Plate (`PLATE_BOARDS_v02.json`) | Film Window (s) | Overlay Window (s) | Label (`≤ 4` words, VO verbatim) | Scribe Word Timing | `01_Script/SOURCES.md` Check |
|---|---|---|---|---|---|---|
| **1 The Star in Orion's Shoulder** | `r06_paranal` (`harvest`, `lasilla_startrails.mp4`) | `49.46–55.00` | `51.16–53.60` (`2.44 s`) | **`700 light-years away`** | `"seven"` `51.16` · `"hundred"` `51.46` · `"light-years"` `51.90` · `"away."` `52.38–52.68` | **Row 3:** Joyce et al. (2020, *ApJ* 902, 63) $168^{+27}_{-15}\text{ pc} = 548^{+88}_{-49}\text{ ly}$; Harper et al. (2017, *AJ* 154, 11) $222^{+48}_{-34}\text{ pc} = 724^{+156}_{-111}\text{ ly}$ (VO: *"between five and seven hundred light-years away"*). |
| **1 The Star in Orion's Shoulder** | `r07_sdo` (`harvest`, `sdo_hmi_continuum.jpg`) | `62.46–67.50` | `63.36–66.20` (`2.84 s`) | **`4.5 billion years old`** | `"four"` `63.36` · `"and"` `63.52` · `"a"` `63.62` · `"half"` `63.68` · `"billion"` `64.04` · `"years"` `64.46` · `"old"` `64.78–65.08` | **Row 4:** Connelly et al. (2012, *Science* 338, 651) Solar System CAI age `"4567.30 ± 0.16 Myr"`. |
| **1 The Star in Orion's Shoulder** | `r08_westerlund_w` (`harvest`, `westerlund.jpg` wide) | `73.86–80.00` | `78.06–79.90` (`1.84 s`) | **`15 to 20 times`** | `"fifteen"` `78.50` · `"to"` `79.02` · `"twenty"` `79.18` · `"times"` `79.64–80.18` | **Row 5 (MUST QUOTE):** Joyce et al. (2020, *ApJ* 902, 63) verbatim: *"We report a present-day mass of 16.5--19 M_sun... Estimates of Betelgeuse's mass are derived from models and range from roughly 15--25 M_sun"*. |
| **1 The Star in Orion's Shoulder** | `r08_westerlund_t` (`harvest`, `westerlund.jpg` tight) | `80.00–86.00` | `84.30–85.92` (`1.62 s`) | **`Around 100,000`** | `"around"` `85.02` · `"a"` `85.30` · `"hundred"` `85.44` · `"thousand"` `85.92–86.34` | **Row 6:** Joyce et al. (2020, *ApJ* 902, 63) verbatim: *"luminosity of our model star is 10^5 L_sun"* ($\log_{10} L/L_{\odot} = 4.94^{+0.06}_{-0.04}$). |
| **3 How a Giant Star Dies** | `r17_r20_shells` (`code`, `shells`, `210.50–216.50 s` collapse stretch) | `210.50–216.50` | `211.94–215.20` (`3.26 s`) | **`Less than 1 second`** | `"In"` `211.94` · `"less"` `212.10` · `"than"` `212.34` · `"a"` `212.50` · `"second,"` `212.64–213.10` | **Row 12:** Janka (2012, *ARNPS* 62, 407) verbatim: *"The dynamic collapse of the stellar iron core takes only a few hundred milliseconds"*. |
| **4 The Night It Goes** | `r29_span_astrolabe` (`code`, `orion_astrolabe`, `336.00–341.80 s` astrolabe stretch) | `336.00–341.80` | `337.66–340.86` (`3.20 s`) | **`500 years`** | `"five"` `337.70` · `"hundred"` `338.04` · `"years"` `338.42–338.64` | **Rows 3 & 18:** Joyce et al. (2020) $168^{+27}_{-15}\text{ pc} = 548^{+88}_{-49}\text{ ly}$ ($>500\text{ yr}$ light travel time). |

---

## 3. Gate Verification (`picture_qa.py` + `polish_gate.py`)

```
WARN   0:26 row r17_r20_shells code_graphic_029_r17_r20_shells_v01.mp4: low detail: edge density 0.0141 < film p5 0.0152
WARN   0:32 row r29_span_astrolabe code_graphic_029_r29_span_astrolabe_v01.mp4: low detail: luma std 16.78 < 18.0
picture QA PASS: 0 of 6 cuts fail, 2 to look at -> 02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/teaching_overlays_v01_pack/picture_qa_v01/PICTURE_QA.md, 02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/teaching_overlays_v01_pack/picture_qa_v01/picture_qa_review.jpg
polish gate PASS: 0 of 6 rows failed, 2 to look at -> 02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/teaching_overlays_v01_pack/polish_gate_v01.json
```

