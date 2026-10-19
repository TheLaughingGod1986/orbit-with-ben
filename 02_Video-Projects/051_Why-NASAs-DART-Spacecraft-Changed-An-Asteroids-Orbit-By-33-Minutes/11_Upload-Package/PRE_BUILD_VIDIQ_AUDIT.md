# Pre-build vidIQ audit — Orbit with Ben

**Hard gate:** Run **before** locking script, VO, prompts, or picture gen for any new long.  
**Goal:** Every episode is aimed at **views + full-video watch** using live data — not gut feel alone.  
**Also follow:** `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` and `FAMILIAR_DANGER_STRATEGY.md`.  
**Listing path:** vidIQ keyword + title scoring, then `THUMBNAIL_AND_TITLE_RULES.md` — apply the same VidIQ optimize path to **longs and Shorts** (title, description, tags, thumbs/ABC; VidIQ generate thumbs if needed).

Copy into each project as:

`02_Video-Projects/NNN_Slug/11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | `051_Why-NASAs-DART-Spacecraft-Changed-An-Asteroids-Orbit-By-33-Minutes` |
| Working title | Why NASA's DART Spacecraft Changed an Asteroid's Orbit by 33 Minutes |
| Date pulled | 2026-10-19 |
| Credits used (approx) | 0 (`v00` script draft only; no VO or picture spend) |
| Brand guardrails | Wonder over fearbait · no conspiracy · Orbit DNA |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) |
| Primary keyword overall | `nasa dart mission` / `dart spacecraft dimorphos` / `planetary defense` |
| Hook promise | One sentence — NASA aimed a 570-kilogram spacecraft at the asteroid moon Dimorphos expecting a 10-minute orbit change, and moved it by 33 minutes because the ejected boulder cloud pushed back harder than the spacecraft hit. |
| Retention design | Chapters that earn the next minute (teach + turn) |
| Packaging | Thumb readable on mobile; one idea (`33 MIN` / `5× RECOIL`) |

---

## 2. Keyword research (vidIQ)

Pull GB (or primary market) research for 5–8 terms.

| Keyword | Overall | Est./mo | Comp | Role (title / desc / chapter / Shorts) | Keep? |
|---------|--------:|--------:|-----:|----------------------------------------|-------|
| `nasa dart mission` | High | High | Med | primary | Yes |
| `dimorphos asteroid` | High | Med | Low | primary | Yes |
| `dart spacecraft` | High | Med | Low | title | Yes |
| `didymos and dimorphos` | Med | Med | Low | secondary | Yes |
| `planetary defense` | High | High | Med | umbrella | Yes |
| `kinetic impactor` | Med | Low | Low | chapter | Yes |
| `asteroid deflection` | High | Med | Med | Shorts hooks | Yes |

**Decision:** Primary keyword for title lead = `Why NASA's DART Spacecraft Changed an Asteroid's Orbit by 33 Minutes`  
**Description first 100 chars must include:** `Why did NASA's DART spacecraft change the asteroid moon Dimorphos's orbit around Didymos by 33 minutes?`  

---

## 3. Title ABC (score before VO)

**Growth System v2:** one promise · prefer ≤ ~60 characters · **do not** append `| Orbit's Cosmic Journey` (or similar series suffix). Brand lives in the content.

| | Title | Score | Keep? |
|---|-------|------:|-------|
| A | Why NASA's DART Spacecraft Changed an Asteroid's Orbit by 33 Minutes | 95 | **Keep (Lead)** |
| B | How NASA's DART Spacecraft Moved an Asteroid Moon by 33 Minutes | 93 | Backup |
| C | Why Dimorphos Moved 5 Times More Than NASA's DART Spacecraft Hit It | 91 | Backup |
| Reject (fearbait / off-brand / series-suffix clutter even if high) | Can NASA Stop a Killer Asteroid From Destroying Earth? \| Orbit's Cosmic Journey | — | **Reject** |

**Locked title:** Why NASA's DART Spacecraft Changed an Asteroid's Orbit by 33 Minutes  
**Why it wins (score + brand + keyword):** Direct hand-off promised in `050` (`"Next week is how NASA's DART spacecraft moved an asteroid"`), names the hero spacecraft (`DART`), the target (`Asteroid's Orbit`), and the exact counter-intuitive measurement (`33 Minutes`).  

Regen sheet:

```bash
python3 04_Audio/tools/vidiq_title_score_sheet.py --project-dir 02_Video-Projects/051_Why-NASAs-DART-Spacecraft-Changed-An-Asteroids-Orbit-By-33-Minutes
```

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/051_Why-NASAs-DART-Spacecraft-Changed-An-Asteroids-Orbit-By-33-Minutes/01_Script/dart_asteroid_orbit_script_master_v00.md
```

- [x] Score ≥ **90 / 100** (**PASS 95.6 / 100**)  
- Scorecard: `templates/SCRIPT_REVIEW_SCORECARD.md`  
- Reject / rewrite if below threshold  

---

## 4. Outlier / competitive patterns (on-brand only)

Pull outliers for the primary topic (≤80K–mid sub channels preferred). Ignore meme/movie noise.

| Outlier / pattern | Views / multiple | Steal (structure) | Do **not** copy |
|-------------------|------------------|-------------------|-----------------|
| Veritasium — *How NASA Will Save Earth From Asteroids* / planetary defense explainers | 3.0M+ | Momentum recoil breakdown (`β = 3.61`), binary eclipse clock | Long talking-head interviews |
| Scott Manley — *NASA's DART Spacecraft Successfully Hits Asteroid — What We Saw* | 1.4M+ | DRACO final-60-seconds approach + LICIACube flyby sequence | Raw livestream commentary format |
| Kurzgesagt — *Could We Stop An Asteroid?* | 11.0M+ | Clear kinetic-impactor vs rubble-pile physics contrast | Doomsday extinction focus |
| NASA / APL — *DART's Impact with Asteroid Dimorphos* | 2.1M+ | Real DRACO + Hubble + Webb visual progression | Unedited press-briefing pacing |

**Patterns we will use in this script:**

- [x] Assumption-flip / open-loop title  
- [x] Numbered layers or chapter journey  
- [x] Body-scale anchor  
- [x] Slow reveal / delayed answer  
- [x] Engineering roadmap (if topic fits)  
- [ ] Other:  

---

## 5. Incorporate into the build (required)

Translate data → creative decisions **before** writing the full script:

| Data finding | Change to script / chapters / visuals / packaging |
|--------------|-----------------------------------------------------|
| Primary keyword (`DART spacecraft`, `Dimorphos`, `Didymos`) | Title lead + 0:00 spoken question + description first 100 chars |
| High-volume related term (`planetary defense`, `kinetic impactor`) | Chapters 1 and 3 explain binary eclipse timing and momentum enhancement factor `3.61` |
| Winning outlier structure | 6-chapter investigation from final DRACO frames → binary clock → rubble recoil → Hubble/Webb plumes → 33-minute orbit change → permanent craterless reshaping |
| Weak competition angle | Most videos stop on impact day; we include the March 2024 JPL reshaping study (`160 × 174 × 116 m` → `177 × 174 × 100 m`, `2–5%` orbit drop) and July 2023 Hubble 37-boulder swarm |
| Thumb pattern that works | Split contrast: DART spacecraft striking rubble-pile Dimorphos with radiant ejecta cone (`33 MIN` or `5× RECOIL`) |

**Chapter list after audit** (4–6, each with a teach-point):

1. **The Binary Target** — Why NASA tested deflection on a 151-metre moon orbiting a 780-metre parent asteroid 1.19 km apart, using mutual eclipses every 11 hours and 55 minutes as a natural stopwatch.  
2. **Sixty Seconds on SMART Nav** — How DART's autonomous optical navigation steered a 570 kg spacecraft at 22,530 km/h into a target it could only resolve in its final hour, while LICIACube watched 3 minutes behind.  
3. **Why Rubble Pushes Back Harder** — Why hitting a weakly bound rubble pile launched 16 million kg of rock and multiplied the spacecraft's momentum push by 3.61.  
4. **What LICIACube, Hubble, and Webb Saw** — How three space observatories and a CubeSat tracked supersonic ejecta filaments, a 10,000-km dust tail, and 37 boulders up to 6.7 metres wide escaping at half a walking pace.  
5. **The Thirty-Three-Minute Shift** — How Earth telescopes timed the new 11-hour-22-minute orbit to within ±1 minute and proved Dimorphos dropped 37 metres closer to Didymos.  
6. **The Moon That Changed Shape** — How the 2024 JPL shape reconstruction proved Dimorphos lost 2 to 5 percent of its orbital radius and deformed globally like an oblong watermelon instead of simply taking a bowl crater.  

---

## 6. Retention plan (whole-video watch)

Design for **watching through**, not just CTR (Growth System v2):

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| 0–0:05 | Curiosity spike | Real DRACO final approach frame (`PIA25558`) + LICIACube plume (`PIA25563`) |
| ~0:15 | Stakes | 73-second minimum threshold vs 33-minute actual orbit shift |
| ~0:30 | Journey clear | Cold open runs ~0:55 before Chapter 1 card (no full-frame chapter card in first 30s) |
| Chapter starts | Re-hook + chapter card | Each chapter ends on a question answered by the next chapter |
| Mid | Teach while story continues | Orbit braces in the ejecta plume (Ch 3) and paces a 1-mph escaping boulder (Ch 4) |
| Final chapter | Payoff + bigger question | Global reshaping of Dimorphos + hand-off to `052` (Uranus's Moon Miranda 12-Mile Ice Cliff) |
| Outro | Soft return CTA | Hand-off to Miranda's Verona Rupes |

- [x] No 30s+ stretch without a new teach or turn  
- [x] Every chapter earns the next one  
- [x] Runtime target **8–12 min** in trust-building window (~8.6 min)  

---

## 7. Sign-off (block production until checked)

- [ ] Keywords pulled and primary locked  
- [ ] Title ≥90 locked (fearbait / series-suffix clutter rejected)  
- [x] Script reviewer ≥ 90 (**95.6 / 100**)  
- [x] Outlier patterns mapped into chapter arc  
- [x] Thumb concepts match title promise (one object · one emotion)  
- [x] Chapter teach-points listed (4–6 acts)  
- [x] Cold-open clock (5 / 15 / 30s) written  
- [x] Retention plan filled  
- [x] Production checklist path noted: `templates/PRODUCTION_CHECKLIST_V2.md`  

**Signed off by:**  
**Date:**  

**Only then:** full script → ElevenLabs VO → AI Studio picture (stills first · Veo world · Omni Orbit-only) → edit.

---

## Tools

- Title Analyzer / Keyword: https://app.vidiq.com  
- Script reviewer: `cd 07_Content-Ops && npm run review:script -- --file <script.md>`  
- Latest channel numbers: `00_Brand/Channel-Setup/audits/weekly/<date>/REPORT.md`  
- How to build: `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md`  
- Strategy: `00_Brand/Channel-Setup/FAMILIAR_DANGER_STRATEGY.md`  
- Brand: wonder over clickbait — data informs structure, never overrides Orbit DNA
