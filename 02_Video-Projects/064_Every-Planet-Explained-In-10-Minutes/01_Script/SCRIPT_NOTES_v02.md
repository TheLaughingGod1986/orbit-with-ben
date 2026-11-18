# Script Notes, Exact Hashes, Reproducible Spoken-Count Extraction, Section Timings & Shelf Verification (`SCRIPT_NOTES_v02.md`) — `OWB:064`

- **Film:** `064_Every-Planet-Explained-In-10-Minutes` (`OWB:064` — *Every Planet Explained in 10 Minutes (Mercury to Neptune)*)
- **Job:** `J3036` (*OWB 064: Correct script facts and rerun Gemini checks*) · **Ref:** `J3027` (Elected-Chief `FIX` ruling on `18 Nov 2026`)
- **Author / Fact-Check Worker:** `gemini` (`gemini-4-argon-high` on the Mac mini)
- **Planned Air Slot Preserved:** Wednesday 16 December 2026 at 18:00 London (finished cut on Ben's watch board no later than Friday 11 December 2026 at 18:00 London; Ben topic approval from `J3011` preserved; zero dated films moved)
- **Spend:** **£0.00 cash · 0 Flow/Vertex credits · 0 ElevenLabs credits spent in `J3036`** (`J3020` remains blocked and `J3021` narration does not run until `J3037` independent review locks the exact hash)

---

## 1. Resolution of All `J3027` Ruling Blockers & Findings (`v01` → `v02`)

1. **Historical Evidence Preserved (`v01` untouched):**
   - `01_Script/every_planet_explained_script_master_v01.md` and `01_Script/episode_script_draft_v01.md` (`SHA-256: c9945afa744db370a1601e96395e8add391cf45439c5ee16a624d342e7902aae`), `01_Script/SOURCES_v01.md`, `01_Script/GEMINI_QUOTE_PASS_v01.md`, `01_Script/CLAUDE_QUOTE_CHECK_v01.md`, and `01_Script/SCRIPT_NOTES_v01.md` are preserved byte-identical as historical evidence.
2. **Confirmed Blocker (1) — Neptune Wind Speed Ratio (`2,000 ÷ 400 = 5`, not `9`):**
   - **Fixed in spoken text, `[VISUAL MUST]`, `DATA:`, `SCALE:`, `NUMBER OBJECT`, `[TEACH]`, and `SOURCES.md` Row 16:**
     Spoken narration now states: *"When Voyager 2 made the only flyby on 25 August 1989, it found our windiest world: methane clouds whipped past two thousand kilometres per hour — over five times faster than Earth's strongest four-hundred-kilometre-per-hour winds — while backwards-orbiting Triton fires icy geysers over eight kilometres high."*
     Both the narration and the code graphic compare `>2,000 km/h` (`1,200 mph`) against Earth's strongest `400 km/h` (`250 mph`) winds as **`>5×` faster (`2,000 ÷ 400 = 5`)**, without conflating NASA's separate general comparison (*"three times stronger than Jupiter's and nine times stronger than Earth's"*).
3. **Confirmed Blocker (2) — Earth Liquid-Iron Outer Core Depth vs Size (`3,000 km` to Top of Outer Core):**
   - **Fixed in spoken text, `[VISUAL MUST]`, `DATA:`, `NUMBER OBJECT`, `[TEACH]`, and `SOURCES.md` Row 6:**
     Spoken narration now states: *"Some three thousand kilometres beneath our feet, below the rocky mantle, begins Earth's swirling liquid-iron outer core, generating a magnetic shield that deflects the solar wind and flipped one hundred and eighty-three times in eighty-three million years."*
     The `[VISUAL MUST]` and `DATA:` notes specify an interior depth cutaway locating the **top of the liquid-iron outer core some `3,000 km` beneath our feet below the rocky mantle**, matching BGS (`https://geomag.bgs.ac.uk/education/reversals.html`: *"At the top of the liquid core, some 3000 km beneath our feet and below the rocky mantle"*).
4. **New Horizons Trajectory vs Neptune Flyby:**
   - **Fixed in spoken text, `[VISUAL MUST]`, `[TEACH]`, and `SOURCES.md` Row 16:**
     Explicitly states that Voyager 2 made the **only flyby** of Neptune on `25 August 1989`, and distinguishes crossing beyond Neptune's orbit into the Kuiper Belt from a Neptune encounter: *"Beyond Neptune's orbit in the Kuiper Belt, New Horizons flew past Pluto in July 2015, revealing a thousand-kilometre nitrogen-ice heart with no craters."* (`https://science.nasa.gov/mission/new-horizons/`).
5. **Jupiter Great Red Spot Chronology vs Galileo's `1610` Moon Discovery:**
   - **Fixed in spoken text, `[VISUAL MUST]`, `[TEACH]`, and `SOURCES.md` Row 10:**
     Separates Galileo's `1610` moon discovery from Great Red Spot storm measurements: *"In 1610, Italian astronomer Galileo Galilei spotted its four largest moons. Meanwhile, in Jupiter's southern sky swirls the Great Red Spot — a storm wider than Earth measured since the late 1800s as it shrank from about forty-one thousand kilometres to under sixteen thousand five hundred in 2014."* (`https://www.esahubble.org/news/heic1410/`).
6. **Saturn Ring Age Uncertainty & Answering Why Saturn's Rings Are Vanishing:**
   - **Fixed in spoken text, `[VISUAL MUST]`, `DATA:`, `[TEACH]`, and `SOURCES.md` Row 11:**
     Directly answers the transition question (*"Why are Saturn's rings vanishing?"*) with Cassini's `2017` Grand Finale in-situ D-ring mass-inflow measurement (`Waite et al. 2018`, *Science* 362, `PMID 30287634`: `4,800 to 45,000 kilograms per second` pouring into Saturn), and preserves the uncertainty qualifier from `Iess et al. 2019` (*Science* 364, `PMID 30655447`): *"During 2017 dives between the innermost D ring and cloud tops, Cassini measured ring material pouring into Saturn at four thousand eight hundred to forty-five thousand kilograms per second, while six gravity crossings weighed the rings at zero point four one Mimas masses — indicating they may have formed ten million to one hundred million years ago."*
7. **Mercury `3:2` Spin-Orbit Resonance vs Solar Day:**
   - **Fixed in spoken text, `[VISUAL MUST]`, `DATA:`, `SCALE:`, `[TEACH]`, and `SOURCES.md` Row 1:**
     Explicitly distinguishes three axial rotations per two orbital revolutions from the solar day: *"In 1965, Italian mathematician Giuseppe Colombo solved its spin mystery: Mercury rotates on its axis three times — once every fifty-nine Earth days — for every two eighty-eight-day orbits, so one solar day lasts one hundred and seventy-six Earth days, just over two Mercury years."* Added primary citation `Colombo, G. (1965), Nature 208, 575` (`doi:10.1038/208575a0`).
8. **Venus Hottest Surface Scope:**
   - **Fixed in spoken text (`Ch 2` line 16):**
     Explicitly scoped to *"You reach the hottest planetary surface in our Solar System: a runaway greenhouse under a ninety-six point five per cent carbon dioxide atmosphere traps heat and bakes the rock to four hundred and sixty-four degrees Celsius."*
9. **Less Number-Dense Narration With Mechanisms Explained & Verified Shelf `[ORBIT ACTS]`:**
   - Removed secondary clutter numbers across the script (dropped Prokofiev's `112-km` spoken width, Venus's `95%` spoken width and `2021` Parker pass, Earth's `6,378 km` spoken radius and `780,000 yr` / *Homo sapiens* tangent, Mars's `3,390 km` spoken radius, `0.64 mSv/day` radiation tangent, and `5,111 sols`, Jupiter's `69,911 km` spoken radius and `2016` date, Saturn's `120,500 km` spoken diameter, `2,000 km` eye width, `27 Nov 2012` date, and `330 mph` eyewall speed, Uranus's `51,118 km` spoken diameter, and Neptune's `49,528 km` spoken diameter) while explaining the physical mechanisms (runaway greenhouse and hydrogen escape on Venus, liquid-iron geodynamo shielding on Earth vs early cooling and solar-wind stripping plus stationary-crust hotspot volcanism on Mars, pressure squeezing electrons off hydrogen into a conducting liquid metal on Jupiter, D-ring gravitational infall and seasonal photochemical haze on Saturn, and impact-tilted `21-year` polar winters on Uranus).
   - Replaced `v01`'s two unverified `[ORBIT ACTS]` prompts (Venus surface umbrella and Saturn north-pole protractor) with **two verified shelf Omni clips** already approved in finished OWB films:
     1. **Venus (`Ch 2`):** `023_What-Happened-To-Venus` shelf clip `orbit_looks_back_earth_omni_v01_t0-5s.mp4` (`SHA-256: 0ee73142a0faf6670bb5d8e2c7b97a961d57fe709c9547f1f0235bd5e9aa3818`, Claude PASS `5984886311`).
     2. **Earth (`Ch 3`):** `027_What-If-Earth-Stopped-Spinning` shelf clip `orbit_northpole_omni_v01.mp4` (`SHA-256: 5d49b8e84d2903d0a6f589ea66a82f84c5a5212a6d10bf6ee6512fa80ae03393`, verified PASS in `027` `picture_qa_v01m` and `polish_gate_v01m`).

---

## 2. Exact `v02` File Hashes, Reproducible Spoken-Count Extraction & Section Timings

### 2.1 Exact File Hashes (`SHA-256`)
- `01_Script/every_planet_explained_script_master_v02.md`: `0dd5ea6c3d8db1a48e46394c04737cd5c990895142aa5f5bb24642cfa8c8c11b` (`27,029` bytes)
- `01_Script/episode_script_draft_v02.md`: `0dd5ea6c3d8db1a48e46394c04737cd5c990895142aa5f5bb24642cfa8c8c11b` (`27,029` bytes, byte-identical copy)
- `01_Script/every_planet_explained_script_master_v01.md`: `c9945afa744db370a1601e96395e8add391cf45439c5ee16a624d342e7902aae` (`25,243` bytes, preserved)

### 2.2 Reproducible Spoken-Count Extraction Command & Output

```bash
python3 -c '
import re, hashlib
p = "02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/01_Script/every_planet_explained_script_master_v02.md"
t = open(p).read()
lines = [l.strip() for l in t.splitlines() if l.strip() and not l.strip().startswith("#") and not l.strip().startswith("[") and not l.strip().startswith("<!--")]
spoken = " ".join(lines)
ws = spoken.split()
alpha = [w for w in re.split(r"\s+", spoken) if re.search(r"[A-Za-z0-9]", w)]
print("spoken_alpha_words:", len(alpha), "whitespace_tokens:", len(ws), "spoken_chars:", len(spoken), "sha256:", hashlib.sha256(t.encode()).hexdigest())
'
# Output:
# spoken_alpha_words: 1257 whitespace_tokens: 1300 spoken_chars: 8200 sha256: 0dd5ea6c3d8db1a48e46394c04737cd5c990895142aa5f5bb24642cfa8c8c11b
```

### 2.3 Per-Planet Section Lengths & Timings

| # | Section / Chapter Card | Spoken Words (`spokenWords` Alpha) | Whitespace Tokens (incl. `—`) | Spoken Characters (incl. spaces) | Est. Narration (`@145 wpm`) | Target Assembled Window (incl. card breaths & transitions) |
|---:|---|---:|---:|---:|---:|---:|
| **1** | **Mercury** (Cold Open — no chapter card before `0:45`) | `159` | `163` | `1,008` | `~65.8 s` | `0:00–1:12` (`72.3 s`) |
| **2** | `[CHAPTER CARD: Venus — The Backwards Furnace]` | `151` | `153` | `942` | `~62.5 s` | `1:12–2:21` (`69.0 s`) |
| **3** | `[CHAPTER CARD: Earth — The Shielded Ocean World]` + `[SUBSCRIBE BEAT]` (`15 words` at `35%`) | `147` | `151` | `969` | `~60.8 s` | `2:21–3:28` (`67.3 s`) |
| **4** | `[CHAPTER CARD: Mars — The Frozen Robot Desert]` | `134` | `142` | `874` | `~55.4 s` | `3:28–4:30` (`61.9 s`) |
| **5** | `[CHAPTER CARD: Jupiter — The Ocean of Metallic Hydrogen]` (Midpoint twist at `~55%`) | `174` | `179` | `1,142` | `~72.0 s` | `4:30–5:49` (`78.5 s`) |
| **6** | `[CHAPTER CARD: Saturn — Disappearing Rings and the Hexagon Storm]` | `172` | `179` | `1,104` | `~71.2 s` | `5:49–7:06` (`77.7 s`) |
| **7** | `[CHAPTER CARD: Uranus — Knocked Sideways Into 21-Year Winters]` | `151` | `157` | `1,003` | `~62.5 s` | `7:06–8:15` (`69.0 s`) |
| **8** | `[CHAPTER CARD: Neptune — Supersonic Winds at the Edge]` + `18 s` End-Screen Hold | `169` | `176` | `1,151` | `~69.9 s` | `8:15–9:53` (`79.9 s` VO/transitions + `18.0 s` end hold = `97.9 s`) |
| **Total** | **8 Planets (Mercury → Neptune) + Subscribe Beat + End Hold** | **`1,257` spoken words** | **`1,300` ws tokens** (`1,350` reviewer words) | **`8,200` spoken chars** | **`~520.1 s` speech** | **`~593.6 s` (`9 min 54 s`)** |

### 2.4 Automated Gate Results (`review:script` & `gate:episode`)
- **`npm run review:script -- --file 02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/01_Script/every_planet_explained_script_master_v02.md`:**
  **`PASS · 93.1 / 100`** (`hook: 10`, `curiosity: 9.5`, `storytelling: 8`, `scientificAccuracy: 10`, `emotion: 9.2`, `escalation: 10`, `retentionPotential: 9`, `searchPotential: 8.7`, `visualOpportunities: 9.5`, `narrationFlow: 9.2`).
- **`npm run gate:episode -- --project 02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes --script 02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/01_Script/every_planet_explained_script_master_v02.md --require-checklist`:**
  **`PASS — VO / Gemini Veo allowed`** (`prebuild_vidiq` OK, `script_file` OK, `script_review` `93.1/90` OK, `orbit_acts` `2` OK, `subscribe_beat` at `35%` (`15 words`) OK, `visual_must` `8` OK, `teach` `8` OK, `chapters` `7` OK, `production_checklist` OK).
- **Teach on Screen, Scale & Per-Chapter Number Objects (`studio/RULES.md`):**
  - `DATA:`: `8` (`≥3`)
  - `SCALE:`: `8` (`= DATA`)
  - `WHO:`: `7` (`100%` of named people at first mention: Colombo, Gauss, Galileo, Herschel, Le Verrier, Galle, Lassell)
  - `WHEN:`: `8` (all spoken dates/eras mapped)
  - `FACT:`: `4` (`2–4`, all `≤4 words`: `Second densest planet`, `Hottest planetary surface`, `Less dense than water`, `Coldest planetary atmosphere`)
  - `NUMBER OBJECT`: `8` (`8/8` chapters)
