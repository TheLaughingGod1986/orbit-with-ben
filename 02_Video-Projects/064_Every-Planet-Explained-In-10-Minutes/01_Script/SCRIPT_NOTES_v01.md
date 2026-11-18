# Script Notes, Exact Hashes, Section Lengths & No-Generation Picture/Music Plan (`SCRIPT_NOTES_v01.md`) — `OWB:064`

- **Film:** `064_Every-Planet-Explained-In-10-Minutes` (`OWB:064` — *Every Planet Explained in 10 Minutes (Mercury to Neptune)*)
- **Job:** `J3020` (*OWB 064: Write and check the script for the every-planet film*) · **Ref:** `J3011` (Ben chat lock on 17 Nov 2026: *"Lock it."*)
- **Author / Fact-Check Worker:** `gemini` (`gemini-4-argon-high` on the Mac mini)
- **Planned Air Slot:** Wednesday 16 December 2026 at 18:00 London (finished cut on Ben's watch board no later than Friday 11 December 2026 at 18:00 London; zero dated films moved)
- **Spend:** **£0.00 cash · 0 Flow/Vertex credits · 0 ElevenLabs credits spent in `J3020`**

---

## 1. Exact Script Metrics, File Hashes & Automated Gate Scores

### 1.1 Exact File Hashes (SHA-256)
- `01_Script/every_planet_explained_script_master_v01.md`: `c9945afa744db370a1601e96395e8add391cf45439c5ee16a624d342e7902aae` (`25,243` bytes)
- `01_Script/episode_script_draft_v01.md`: `c9945afa744db370a1601e96395e8add391cf45439c5ee16a624d342e7902aae` (`25,243` bytes, identical copy so `gate:episode` and downstream tools resolve the same text whether looking up `master` or `draft`)
- `01_Script/SOURCES.md`: `16` verified primary-source rows (`53 / 53` live HTTP 200 URLs)
- `01_Script/GEMINI_QUOTE_PASS_v01.md`: `16 / 16` rows `PASS` (`0 PARTIAL`, `0 FLAG`)
- `01_Script/CLAUDE_QUOTE_CHECK_v01.md`: `16 / 16` `MUST QUOTE` rows directly verified (`0 FLAG`)
- `05_Music/MUSIC_BRIEF_v01.md` & `05_Music/every_planet_score_bed_v01_plan.json`: Film-specific chapter-shaped score brief and plan (`Pace: 68-76 BPM`, full `NOT:` exclusion list)

### 1.2 Word Count, Spoken Character Count & Per-Planet Section Lengths

| # | Section / Chapter Card | Spoken Words (Whitespace) | Spoken Characters (incl. spaces) | Est. Narration (`@147 wpm`) | Target Assembled Window (incl. card breaths & transitions) |
|---:|---|---:|---:|---:|---:|
| **1** | **Mercury** (Cold Open — no chapter card before `0:45`) | `144` | `939` | `~58.8 s` | `0:00–1:05` (`65.3 s`) |
| **2** | `[CHAPTER CARD: Venus — The Backwards Furnace]` | `149` | `925` | `~60.8 s` | `1:05–2:13` (`67.6 s`) |
| **3** | `[CHAPTER CARD: Earth — The Shielded Ocean World]` + `[SUBSCRIBE BEAT]` (`15 words` at `35%`) | `155` | `997` | `~63.3 s` | `2:13–3:24` (`70.9 s`) |
| **4** | `[CHAPTER CARD: Mars — The Frozen Robot Desert]` | `153` | `986` | `~62.4 s` | `3:24–4:36` (`72.0 s`) |
| **5** | `[CHAPTER CARD: Jupiter — The Ocean of Metallic Hydrogen]` (Midpoint twist at `~55%`) | `169` | `1,113` | `~69.0 s` | `4:36–5:53` (`77.3 s`) |
| **6** | `[CHAPTER CARD: Saturn — Disappearing Rings and the Hexagon Storm]` | `160` | `1,031` | `~65.3 s` | `5:53–7:07` (`73.8 s`) |
| **7** | `[CHAPTER CARD: Uranus — Knocked Sideways Into 21-Year Winters]` | `150` | `1,006` | `~61.2 s` | `7:07–8:16` (`69.3 s`) |
| **8** | `[CHAPTER CARD: Neptune — Supersonic Winds at the Edge]` + `18 s` End-Screen Hold | `166` | `1,157` | `~67.8 s` | `8:16–9:52` (`77.8 s` VO + `18.0 s` end hold = `95.8 s`) |
| **Total** | **8 Planets (Mercury → Neptune) + Subscribe Beat + End Hold** | **`1,246` spoken words** (`1,290` split tokens · `1,352` reviewer words) | **`8,161` spoken chars** | **`~508.6 s` speech** | **`~592.0 s` (`9 min 52 s`)** |

- **Channel Word-Count & Character-Count Compliance:**
  - `1,246` spoken words (`1,290` alphanumeric tokens) sits squarely inside the `1,200–1,300` spoken-word lock (`studio/RULES.md` Polish pass §4).
  - `8,161` spoken characters matches the `J3020` / `J3021` target of *"roughly 8,000 spoken characters"* for the ElevenLabs `eleven_v3` VO budget.

### 1.3 Automated Gate Results (`review:script` & `gate:episode`)
- **`npm run review:script`:** **`PASS · 93.1 / 100`** (`hook: 10`, `curiosity: 9.5`, `storytelling: 8`, `scientificAccuracy: 10`, `emotion: 9.2`, `escalation: 10`, `retentionPotential: 9`, `searchPotential: 8.7`, `visualOpportunities: 9.5`, `narrationFlow: 9.2`).
- **`npm run gate:episode`:** **`PASS — VO / Gemini Veo allowed`** (`prebuild_vidiq` OK, `script_file` OK, `script_review` `93.1/90` OK, `orbit_acts` `2` OK, `subscribe_beat` at `35%` (`15 words`: *"We make one of these every week. Subscribing is how the next one finds you."*, Line 4 of `templates/SUBSCRIBE_BEAT_LINES.md`, unused in `031`–`034`), `visual_must` `8` OK, `teach` `8` OK, `chapters` `7` OK, `production_checklist` OK).

### 1.4 Teach on Screen, Polish Pass & Reference Lessons Coverage (`studio/RULES.md`)
- **`DATA:` markers:** `8` (one per planet; requirement `≥3`).
- **`SCALE:` markers:** `8` (one per `DATA:` marker; requirement `SCALE >= DATA`).
- **`WHO:` markers:** `7` (`100%` of named individuals at first mention, all with LOC-verified birth and death years and `≤4-word` roles: `Giuseppe Colombo (1920–1984) — Italian mathematician`, `Carl Friedrich Gauss (1777–1855) — German mathematician`, `Galileo Galilei (1564–1642) — Italian astronomer`, `William Herschel (1738–1822) — British astronomer`, `Urbain Le Verrier (1811–1877) — French mathematician`, `Johann Gottfried Galle (1812–1910) — German astronomer`, `William Lassell (1799–1880) — British astronomer`).
- **`WHEN:` markers:** `8` (every spoken date and era mapped across all 8 chapters).
- **`FACT:` markers:** `4` (`≤4 words` each: `Second densest planet`, `Hottest planetary surface`, `Less dense than water`, `Coldest planetary atmosphere`).
- **`NUMBER OBJECT` per-chapter gate:** `8 / 8` chapters have an explicit animated `NUMBER OBJECT` specified inside `[VISUAL MUST: ...]`.

---

## 2. No-Generation Picture Plan & Resolution of Shelf-Music Conflict (`J3020` → `J3022` / `J3023`)

### 2.1 Zero-Spend Picture & Code-Graphics Plan (`£0.00` Cash · `0` Flow/Vertex Credits)

Per `J3020` and `J3022`, **zero paid Flow or Vertex video/image generation** is used for `OWB:064`:
1. **Six Planets With Finished OWB Long Masters on Shelf (`Venus`, `Earth`, `Mars`, `Jupiter`, `Saturn`, `Uranus`):**
   - **Venus (`Ch 2`):** Pull graded NASA Mariner 10 / JAXA Akatsuki UV cloud footage (`PIA00271`), Magellan radar plains, Soviet `Venera 13` (`1982`) surface panorama, Parker Solar Probe WISPR (`2021`) nightside glow, and the approved Orbit scene from `023_What-Happened-To-Venus` (`/Volumes/data/studio-live` / `mac-mini-archive`).
   - **Earth (`Ch 3`):** Pull NASA DSCOVR EPIC rotating Earth, Apollo 17 Blue Marble (`AS17-148-22727`), ISS orbital limb (`Five_Minutes_in_Orbit.webm`), and ESA Swarm aurora/magnetosphere clips from `027_What-If-Earth-Stopped-Spinning` and `031_What-Happens-When-Earths-Magnetic-Field-Flips`.
   - **Mars (`Ch 4`):** Pull Curiosity & Perseverance Gale/Jezero surface panoramas (`PIA19400`, `PIA19803`), Mars Odyssey / Viking Olympus Mons plates (`PIA25476`, `PIA00300`), and `Ingenuity` flight footage from `025_Could-A-Robot-Survive-On-Mars`.
   - **Jupiter (`Ch 5`):** Pull NASA Juno Perijove polar cyclone flyby (`PIA21974`), Cassini/Voyager Great Red Spot time-lapse (`PIA02863`), and Hubble GRS plates from `020_What-Would-You-See-If-You-Fell-Into-Jupiter`.
   - **Saturn (`Ch 6`):** Pull NASA Cassini backlit ring plates (`PIA17172`), Grand Finale ring-dive clips, and the approved Orbit scene from `021_What-Happens-When-Saturn-Loses-Its-Rings` + download free public-domain NASA/JPL Photojournal Cassini polar hexagon plates (`PIA17652`, `PIA14944`, `PIA21049`).
   - **Uranus (`Ch 7`):** Pull NASA Voyager 2 (`1986`) cyan disk, Hubble dynamic cloud plates, and JWST NIRCam (`2022–2023`) glowing `13`-ring plates from `033_Why-This-Planet-Has-21-Year-Winters`.
2. **Two Planets With Breakout Shorts on Shelf + Free Public-Domain NASA Photojournal Plates (`Mercury` & `Neptune`):**
   - **Mercury (`Ch 1` Cold Open):** Pair existing Short `vlkj8RQKmH8` MESSENGER polar crater footage with free public-domain NASA Photojournal MESSENGER plates (`PIA19411` global colour mosaic at Frame 0, `PIA16523` Prokofiev radar-bright polar ice, `PIA17386` contraction scarp) + Wikimedia public-domain portrait of Giuseppe Colombo.
   - **Neptune (`Ch 8`):** Pair existing Short `1OCNzhkiBuc` Voyager 2 Great Dark Spot clip with free public-domain NASA Photojournal Voyager 2 plates (`PIA01492` full azure disk, `PIA00059` & `PIA00317` Triton nitrogen geyser plumes, `PIA02215` farewell Neptune–Triton crescent for the `15–20 s` end-screen hold) + public-domain portraits of Urbain Le Verrier, Johann Gottfried Galle, and William Lassell.
3. **Fresh Per-Row Python Code Graphics (`J3022`, `chart` kind, `£0.00` spend):**
   - Even where shelf films (`023`, `027`, `031`, `025`, `020`, `021`, `033`) have existing graphics, `studio/RULES.md` Lesson 7 requires **every code graphic in `064` to be freshly rendered for its own cut-list row** (`code_graphic_064_rNN_*.mp4`) with real planetary bodies (never flat discs), lifted navy background (`mean luma >= 28`), `≤4 words` per label matching the spoken words, and real moving spacecraft footage between any two code graphics (`0` back-to-back graphics).

### 2.2 Resolution of Concept-Sheet Music Conflict (`05_Music/MUSIC_BRIEF_v01.md`)

- **Conflict Identified in `J3020` Brief:** `TOPIC_GO_NO_GO_SHEET.md` §5.1 wrote *"Assemble ~10-min CFR 24 fps master with shelf music bed"*, whereas `studio/RULES.md` Lesson 7 and `scripts/music_gate.py` strictly forbid reusing any other film's music bed (`similarity >= 0.80` against any `02_Video-Projects/*/05_Music/*` stem is a hard FAIL).
- **Resolution Recorded (`05_Music/MUSIC_BRIEF_v01.md` & `05_Music/every_planet_score_bed_v01_plan.json`):**
  - `OWB:064` **will not reuse** any shelf music bed.
  - Instead, `05_Music/MUSIC_BRIEF_v01.md` and `05_Music/every_planet_score_bed_v01_plan.json` define a dedicated, film-specific chapter-shaped score (`05_Music/every_planet_score_bed_v01.mp3`, `Pace: 68-76 BPM`, with an explicit `NOT:` line excluding every prior OWB bed `020`–`034` and alternating `explain` and `awe` chapters across the 8 planets with `2.5 s` crossfades at chapter cards).
  - In `J3022`/`J3023`, the score stem `05_Music/every_planet_score_bed_v01.mp3` is synthesised locally in Python/NumPy (`_build_064_score_bed_v01.py`, matching the proven £0 synthesis workflow of `032`, `033`, and `034`) to match the exact locked VO duration + `18 s` end hold, passing `scripts/music_gate.py` (`own_file`, `brief`, `unique` `similarity < 0.50`, `full_length`, `no_gaps`) and `scripts/sfx_kit.py level` at **£0.00 spend**.
