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
| Credits used (approx) | 0 (`v01` script draft only; no VO or picture spend) |
| Brand guardrails | Wonder over fearbait · no conspiracy · Orbit DNA |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) |
| Primary keyword overall | `nasa dart mission` / `dart spacecraft dimorphos` / `planetary defense` |
| Hook promise | One sentence — NASA aimed a half-ton spacecraft at the 560-foot asteroid moonlet Dimorphos defining minimum success as a 73-second orbit change, and moved it by 33 minutes (33 minutes 15 seconds) because 35.3 million pounds of ejected rock pushed back like a rocket engine. |
| Retention design | Chapters that earn the next minute (teach + turn) |
| Packaging | Thumb readable on mobile; one idea (`33 MINUTES SHORTER`) |

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
| C | Why Dimorphos Moved 25 Times More Than NASA's Minimum DART Benchmark | 91 | Backup |
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
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/051_Why-NASAs-DART-Spacecraft-Changed-An-Asteroids-Orbit-By-33-Minutes/01_Script/dart_asteroid_orbit_script_master_v01.md
```

- [x] Score ≥ **90 / 100** (**PASS 95.8 / 100**)  
- Scorecard: `templates/SCRIPT_REVIEW_SCORECARD.md`  
- Reject / rewrite if below threshold  

---

## 4. Outlier / competitive patterns (on-brand only)

Pull outliers for the primary topic (≤80K–mid sub channels preferred). Ignore meme/movie noise.

| Outlier / pattern | Views / multiple | Steal (structure) | Do **not** copy |
|-------------------|------------------|-------------------|-----------------|
| Veritasium — *How NASA Will Save Earth From Asteroids* / planetary defense explainers | 3.0M+ | Momentum recoil breakdown (`~2×` spacecraft punch), binary eclipse clock | Long talking-head interviews |
| Scott Manley — *NASA's DART Spacecraft Successfully Hits Asteroid — What We Saw* | 1.4M+ | DRACO final approach + LICIACube flyby sequence | Raw livestream commentary format |
| Kurzgesagt — *Could We Stop An Asteroid?* | 11.0M+ | Clear kinetic-impactor vs rubble-pile physics contrast | Doomsday extinction focus |
| NASA / APL — *DART's Impact with Asteroid Dimorphos* | 2.1M+ | Real DRACO + Hubble + LICIACube visual progression | Unedited press-briefing pacing |

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
| High-volume related term (`planetary defense`, `kinetic impactor`) | Chapters 1, 3, and 6 explain binary eclipse timing, 35.3-million-lb ejecta recoil (`~2×`), and the 0.15-second solar orbit shift |
| Winning outlier structure | 6-chapter investigation from final DRACO frames → binary geology → terminal guidance → 35.3-million-lb LICIACube plume → 33m 15s orbit & watermelon shape change → 37 Hubble boulders & 0.15-second solar orbit shift |
| Weak competition angle | Most videos stop in 2022; we include the March 19, 2024 JPL reshaping study (`33m 15s`, `120 ft` closer, oblong watermelon), July 30, 2024 *Nature Communications* geology (`12.5 Myr` vs `<300,000 yr`, bearing capacity `≥1,000×` lower than dry sand), August 21, 2025 LICIACube plume study (`35.3 million lb` / `30,000×` spacecraft mass), and March 6, 2026 *Science Advances* solar-orbit shift (`0.15 s` / `11.7 µm/s` across `22` stellar occultations) |
| Thumb pattern that works | Real LICIACube + Hubble impact plume erupting from Dimorphos beside Didymos (`33 MINUTES SHORTER`) |

**Chapter list after audit** (4–6, each with a teach-point):

1. **The Twin Asteroid System of Didymos and Dimorphos** — How the 805-metre spinning-top parent Didymos (`2.26-hr` spin, `12.5-Myr` surface age, bearing capacity `≥1,000×` lower than dry sand) spun off the 170-metre (`560-ft`) moonlet Dimorphos (`<300,000-yr` surface age) orbiting 3,900 feet away.  
2. **Seven Miles and Two Seconds Before Impact** — How DART launched on Nov. 24, 2021, released the shoebox-sized LICIACube 15 days before impact, and steered via DRACO into Dimorphos at ~14,000 mph (`3.8 mi/s`), snapping a 100-foot boulder patch 7 miles (`12 km`) and 2 seconds before contact (`STScI-01H531Y476C3GF8RDHA1J3HBH7`).  
3. **Thirty-Five Million Pounds of Rocket Debris** — Why LICIACube's 18 flyby images from 53 miles away revealed 35.3 million pounds (`16 million kg`, `30,000×` spacecraft mass, `~45%` in the opaque inner plume) of ejecta acting like a rocket engine to double the spacecraft's momentum punch.  
4. **From Squashed Ball to Oblong Watermelon** — How the March 19, 2024 JPL study (Steve Chesley) proved the orbital period dropped 32m 42s immediately and settled 33 minutes and 15 seconds shorter (`11h 22m 03s`), pulling Dimorphos 120 feet closer (`3,900 ft` to `3,780 ft`) and reshaping it into an oblong watermelon.  
5. **Thirty-Seven Boulders Moving Like a Giant Tortoise** — How Hubble (`STScI-01H530K7QNQ9HYV7TVSD6KCV07`, David Jewitt) spotted 37 boulders (`3–22 ft` wide, from a ~160-ft football-field-wide circle) drifting away at >0.5 mph like a giant tortoise ahead of ESA's Hera arrival in late 2026.  
6. **Shifting an Asteroid's Orbit Around the Sun** — How 22 stellar occultations (Oct. 2022 – Mar. 2025, published Mar. 6, 2026 in *Science Advances*) proved DART altered the binary pair's 770-day solar orbit by 0.15 seconds (`11.7 µm/s` / `1.7 in/hr`) — the first human-made shift of a solar orbit.  

---

## 6. Retention plan (whole-video watch)

Design for **watching through**, not just CTR (Growth System v2):

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| 0–0:05 | Curiosity spike | Real DRACO final approach frame (`STScI-01H531Y476C3GF8RDHA1J3HBH7` / `Dimorphos-1.jpeg`) + LICIACube plume (`licia_cube_side_by_side.png`) |
| ~0:15 | Stakes | 73-second minimum threshold vs 33-minute actual orbit shift |
| ~0:30 | Journey clear | Cold open runs ~0:57 before Chapter 1 card (no full-frame chapter card in first 30s) |
| Chapter starts | Re-hook + chapter card | Each chapter ends on a question answered by the next chapter |
| Mid | Teach while story continues | Orbit braces by the DRACO viewfinder (Ch 2) and paces a 22-foot escaping boulder at >0.5 mph (Ch 5) |
| Final chapter | Payoff + bigger question | 0.15-second solar orbit shift across 22 stellar occultations + hand-off to `052` (Uranus's Moon Miranda 12-Mile Ice Cliff) |
| Outro | Soft return CTA | Hand-off to Miranda's Verona Rupes |

- [x] No 30s+ stretch without a new teach or turn  
- [x] Every chapter earns the next one  
- [x] Runtime target **8–12 min** in trust-building window (~8.7 min)  

---

## 7. Sign-off (block production until checked)

- [ ] Keywords pulled and primary locked  
- [ ] Title ≥90 locked (fearbait / series-suffix clutter rejected)  
- [x] Script reviewer ≥ 90 (**95.8 / 100**)  
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
