# Independent Script & Source Review — `J3037` (`OWB:064` · *Every Planet Explained in 10 Minutes (Mercury to Neptune)* `v02`)

- **Job:** `J3037` (*OWB 064: Verify corrected script and decide the narration lock*, `kind: review`, `ref: J3027`, `after: J3036`)
- **Independent Reviewer:** `macbook-2` (`Gemini 4 Argon (High)` on the MacBook Pro, reviewing independently of the Mini `gemini` producer for `J3036`)
- **Timestamp (UTC):** `2026-11-18T09:17:00Z`
- **Target Film & Stage:** `OWB:064` (*Every Planet Explained in 10 Minutes (Mercury to Neptune)*, folder `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes`), stage `script` (parent `J3020`, downstream VO `J3021`)
- **Reviewed Script (`v02`):** `01_Script/every_planet_explained_script_master_v02.md` and byte-identical `01_Script/episode_script_draft_v02.md`
- **Exact Locked Script SHA-256:** **`0dd5ea6c3d8db1a48e46394c04737cd5c990895142aa5f5bb24642cfa8c8c11b`** (`27,029` bytes)
- **Versioned Direct Quote Check:** `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/01_Script/CLAUDE_QUOTE_CHECK_v02.md` (`16 / 16` `MUST QUOTE` rows `PASS`, `0 FLAG`)
- **Verdict:** **`PASS — EXACT-HASH SCRIPT LOCK APPROVED (`0dd5ea6c3d8db1a48e46394c04737cd5c990895142aa5f5bb24642cfa8c8c11b`)`**

---

## 1. Independent Verification of `J3020` Scope & `J3027` Chief `FIX` Ruling

All blockers and findings raised by the elected Chief (`codex`) in `J3027` (`2026-11-18T07:11Z`) and addressed in `J3036` (`commit 4c8e91e3f5`) were verified independently against `01_Script/every_planet_explained_script_master_v02.md`, `01_Script/SOURCES.md`, `01_Script/GEMINI_QUOTE_PASS_v02.md`, `01_Script/SCRIPT_NOTES_v02.md`, and live primary sources:

1. **Historical `v01` Evidence Preserved Untouched (`PASS`):**
   - `01_Script/every_planet_explained_script_master_v01.md` and `01_Script/episode_script_draft_v01.md` (`25,243` bytes, `SHA-256: c9945afa744db370a1601e96395e8add391cf45439c5ee16a624d342e7902aae`), `01_Script/SOURCES_v01.md` (`e9ebc64b2eb3de74fba52286467f6b1432c022d8c6119f11fafc37f4a2c62552`), `01_Script/GEMINI_QUOTE_PASS_v01.md` (`4fc1b9e8f551c7cdcf330c276e124dd77a6ec0ddf4386e3391789ad3387eb691`), `01_Script/CLAUDE_QUOTE_CHECK_v01.md` (`18bd20b2b2ed8e8f2f9cc45c5efa5de61f2c1608f3b72eba643c1b7dfbf7ed1e`), and `01_Script/SCRIPT_NOTES_v01.md` (`3e20f51ffcb2697cd50fc990cd165218e0bf7a1bf67a7c90e54e6bede5547079`) remain byte-identical on disk.
2. **Confirmed Blocker (1) — Neptune Wind Speed Ratio (`>2,000 ÷ 400 = >5×`, not `9×`) (`PASS`):**
   - **Spoken text (line 89):** *"When Voyager 2 made the only flyby on 25 August 1989, it found our windiest world: methane clouds whipped past two thousand kilometres per hour — over five times faster than Earth's strongest four-hundred-kilometre-per-hour winds — while backwards-orbiting Triton fires icy geysers over eight kilometres high."*
   - **Graphics notes (`[VISUAL MUST]`, `DATA:`, `SCALE:`, `NUMBER OBJECT (ch 8)` line 91) & `SOURCES.md` Row 16:** Explicitly state `>2,000 km/h (1,200 mph)` vs Earth's `~400 km/h (250 mph)` = **`>5×` faster (`2,000 ÷ 400 = 5`)**, keeping NASA Science Neptune Facts' general `"nine times stronger"` comparison separate and uncombined.
3. **Confirmed Blocker (2) — Earth Liquid-Iron Outer Core Depth (`~3,000 km` Beneath Our Feet) (`PASS`):**
   - **Spoken text (line 30):** *"Some three thousand kilometres beneath our feet, below the rocky mantle, begins Earth's swirling liquid-iron outer core, generating a magnetic shield that deflects the solar wind and flipped one hundred and eighty-three times in eighty-three million years."*
   - **Graphics notes (`[VISUAL MUST]`, `DATA:`, `NUMBER OBJECT (ch 3)` line 32) & `SOURCES.md` Row 6:** Specify an interior depth cutaway locating the **top of the liquid-iron outer core some `3,000 km` beneath our feet below the rocky mantle**, matching British Geological Survey (`https://geomag.bgs.ac.uk/education/reversals.html`: *"At the top of the liquid core, some 3000 km beneath our feet and below the rocky mantle"*).
4. **New Horizons Trajectory vs Neptune Flyby (`PASS`):**
   - **Spoken text (line 89), `[VISUAL MUST]` (line 91), `[TEACH]` (line 92) & `SOURCES.md` Row 16:** Credit Voyager 2 with the **only flyby** of Neptune (`25 August 1989`, `"Only one spacecraft has visited distant Neptune"`) and explicitly place New Horizons in the Kuiper Belt beyond Neptune's orbit (`~30 AU`), flying past Pluto in July 2015 (`14 July 2015`, `https://science.nasa.gov/mission/new-horizons/`).
5. **Great Red Spot Chronology vs Galileo's `1610` Moon Discovery (`PASS`):**
   - **Spoken text (line 54), `[VISUAL MUST]` (line 58), `[TEACH]` (line 59) & `SOURCES.md` Row 10:** Separate Galileo Galilei's `1610` discovery of Jupiter's four largest moons from the Great Red Spot width measurements recorded since the late 1800s (`~41,000 km` shrinking to `<16,500 km` in `2014`, `https://www.esahubble.org/news/heic1410/`).
6. **Saturn Ring Age Uncertainty (`may have formed`) & Why Saturn's Rings Vanish (`4,800–45,000 kg/s`) (`PASS`):**
   - **Spoken text (line 65), `[VISUAL MUST]` (line 69), `DATA:`, `[TEACH]` (line 70) & `SOURCES.md` Row 11:** Directly answer *"Why are Saturn's rings vanishing?"* / *"Why are they vanishing?"* with Cassini's `2017` Grand Finale in-situ D-ring inflow measurement of `4,800 to 45,000 kilograms per second` (`Waite et al. 2018`, *Science* 362, `PMID 30287634`), and preserve the uncertainty qualifier from `Iess et al. 2019` (*Science* 364, `PMID 30655447`): *"weighed the rings at zero point four one Mimas masses — indicating they may have formed ten million to one hundred million years ago."*
7. **Mercury `3:2` Spin-Orbit Resonance vs Solar Day & Venus Hottest Planetary Surface Scope (`PASS`):**
   - **Mercury (line 5):** Explicitly distinguishes `3` axial rotations (`59 Earth days` each) per `2` orbital revolutions (`88 days` each) from one `176-Earth-day` solar day (`just over two Mercury years`), backed by `Colombo, G. (1965), Nature 208, 575` (`doi:10.1038/208575a0`).
   - **Venus (line 16 & `FACT`):** Explicitly scoped to *"the hottest planetary surface in our Solar System"* (`464 °C` / `737 K`).
8. **Coherent Less Number-Dense Narration With Mechanisms & Verified Shelf `[ORBIT ACTS]` (`PASS`):**
   - Narration explains the physical mechanisms across all eight worlds while staying within channel word/character limits (`1,257` spoken alpha words, `1,300` whitespace tokens, `8,200` spoken characters).
   - Both `[ORBIT ACTS]` (lines 21 & 33) use existing approved shelf Omni clips whose files and SHA-256 hashes were independently verified on the NAS during this review:
     - **Venus (`Ch 2`):** `023_What-Happened-To-Venus` shelf clip `orbit_looks_back_earth_omni_v01_t0-5s.mp4` (`SHA-256: 0ee73142a0faf6670bb5d8e2c7b97a961d57fe709c9547f1f0235bd5e9aa3818`).
     - **Earth (`Ch 3`):** `027_What-If-Earth-Stopped-Spinning` shelf clip `orbit_northpole_omni_v01.mp4` (`SHA-256: 5d49b8e84d2903d0a6f589ea66a82f84c5a5212a6d10bf6ee6512fa80ae03393`).

---

## 2. Independent Verification of Preserved `agy` Output, Counts, and Automated Gates

| Check | Requirement | Independent Verification Result (`macbook-2`) | Verdict |
|---|---|---|---|
| **Exact Script Hash (`v02`)** | Identical master & draft files | `01_Script/every_planet_explained_script_master_v02.md` & `01_Script/episode_script_draft_v02.md` (`27,029` bytes each), `SHA-256: 0dd5ea6c3d8db1a48e46394c04737cd5c990895142aa5f5bb24642cfa8c8c11b`. | **PASS** |
| **Spoken Counts & Timings** | `1,200–1,300` spoken words, `~8,000` spoken chars, `~10 min` | `1,257` spoken alpha words · `1,300` whitespace tokens (`1,350` reviewer words) · **`8,200` spoken characters** · `~520.1 s` speech + card breaths + `18.0 s` end-screen hold = **`~593.6 s` (`9 min 54 s`)** across 8 balanced planetary chapters (`61.9 s` to `79.9 s` each). | **PASS** |
| **Preserved `agy` Facts Pass** | `01_Script/GEMINI_QUOTE_PASS_v02.md` | Verified present (`35,622` bytes, `SHA-256: 1d857bd76015e6efdd414569a2f33c18f429cf894ba2aac22ac9e771c2f08be3`): checks units, arithmetic ratios, uncertainty preservation, and exact quote support across all `16 / 16` rows (`PASS`). | **PASS** |
| **Versioned Direct Quote Check** | `01_Script/CLAUDE_QUOTE_CHECK_v02.md` | Independently verified all `16 / 16` `SOURCES.md` rows (`SHA-256: 9d46f553...`) against live NASA Science, NSSDCA, Photojournal, ESA/Hubble, BGS, WMO, PubMed, OpenAlex, and LOC primary sources (`0 FLAG`). | **PASS** |
| **`review:script` Gate (`≥90`)** | `npm run review:script` | **`PASS · 93.1 / 100`** (`hook: 10`, `curiosity: 9.5`, `storytelling: 8`, `scientificAccuracy: 10`, `emotion: 9.2`, `escalation: 10`, `retentionPotential: 9`, `searchPotential: 8.7`, `visualOpportunities: 9.5`, `narrationFlow: 9.2`). | **PASS** |
| **`gate:episode` Gate** | `npm run gate:episode -- --require-checklist` | **`PASS — VO / Gemini Veo allowed`** (`prebuild_vidiq` OK, `script_file` OK, `script_review` `93.1/90` OK, `orbit_acts` `2` OK, `subscribe_beat` at `35%` / `15` words OK, `visual_must` `8` OK, `teach` `8` OK, `chapters` `7` OK, `production_checklist` OK). | **PASS** |
| **Teach on Screen & Polish Markers** | `DATA ≥ 3`, `SCALE = DATA`, `WHO`, `WHEN`, `FACT 2–4`, `NUMBER OBJECT 8/8` | `DATA: 8`, `SCALE: 8`, `WHO: 7` (Colombo, Gauss, Galileo, Herschel, Le Verrier, Galle, Lassell), `WHEN: 8`, `FACT: 4` (`≤4 words` each), `NUMBER OBJECT: 8` (`8/8` chapters). | **PASS** |
| **No-Generation Picture & Film-Specific Music Plan** | `£0` cash, `0` Flow/Vertex credits, passes `music_gate.py` | Verified in `SCRIPT_NOTES_v02.md`, `05_Music/MUSIC_BRIEF_v01.md`, and `05_Music/every_planet_score_bed_v01_plan.json` (`Pace: 68-76 BPM`, full `NOT:` list, `explain`/`awe` chapter shifts). | **PASS** |

---

## 3. Explicit Exact-Hash Lock Verdict & Next Step for Elected Chief (`codex`)

- **Reviewer-Lane Verdict (`studio/RULES.md` Rules E & H, `J3037`):**
  **`PASS — LOCKED`** on `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/01_Script/every_planet_explained_script_master_v02.md` (`SHA-256: 0dd5ea6c3d8db1a48e46394c04737cd5c990895142aa5f5bb24642cfa8c8c11b`, `1,257` spoken words / `8,200` spoken characters).
- **Guardrails Preserved:**
  - Ben's `J3011` topic approval (`"Lock it."`, 17 Nov 2026) and reserved slot (`Wed 16 Dec 2026 18:00 London`, watch board by `Fri 11 Dec 2026 18:00 London`) are retained; zero dated films moved.
  - `£0.00` cash, `0` Flow/Vertex credits, `0` ElevenLabs credits spent; no upload, schedule, or privacy changes.
  - `J3021` (VO) is **not** released directly by this review job; it remains gated by `after: J3020`.
- **Handoff to Elected Chief (`codex`) to Complete `J3020` and Release `J3021`:**
  Because `scripts/jobs.py` restricts `wait --recheck`, `reopen`, and completing a held parent job to its holder or the elected Chief (`codex`), `J3037` is closed **`done`** with this `PASS` verdict (`--ref jobs/reviews/J3037/REVIEW.md`, setting `064` `script` on the board to `review`). The elected Chief (`codex`) may now:
  1. Merge the `macbook/J3037` PR (`CLAUDE_QUOTE_CHECK_v02.md` & `jobs/reviews/J3037/REVIEW.md`).
  2. Set `02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/status.json` `stages.script` to `"state": "done"`, `"ruling": "PASS"`, `"ref": "jobs/reviews/J3037/REVIEW.md"`, `"locked": {"by": "codex", "at": "2026-11-18", "sha256": "0dd5ea6c3d8db1a48e46394c04737cd5c990895142aa5f5bb24642cfa8c8c11b"}`.
  3. Reopen and mark `J3020` **`done`** (`jobs.py reopen J3020 --agent codex --note "J3037 PASS: v02 (SHA-256 0dd5ea6c...) independently verified and locked" --git && jobs.py next --id J3020 --agent codex --can mini,any --git && jobs.py done J3020 --agent codex --result "PASS & locked: OWB:064 every_planet_explained_script_master_v02.md (SHA-256 0dd5ea6c3d8db1a48e46394c04737cd5c990895142aa5f5bb24642cfa8c8c11b, 1,257 spoken words / 8,200 chars, 93.1/100 review:script, 16/16 SOURCES & CLAUDE_QUOTE_CHECK_v02 PASS); J3021 VO released" --ref jobs/reviews/J3037/REVIEW.md --git`), which automatically unblocks `J3021` (`after: J3020`).
