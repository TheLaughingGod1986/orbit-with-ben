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
| ID / slug | `056_Could-AI-Help-Humanity-Reach-The-Stars-How-Autonomous-Probes-Explore-Deep-Space` |
| Working title | Could AI Help Humanity Reach the Stars? How Autonomous Probes Explore Deep Space |
| Date pulled | 2026-10-20 (`J0711`) |
| Credits used (approx) | 0 (`v00` script draft + `SOURCES.md` verification only; no VO or picture spend) |
| Brand guardrails | Wonder over fearbait · no AI doom clickbait · Orbit DNA |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) |
| Primary keyword overall | `how autonomous probes explore deep space` / `could ai help humanity reach the stars` / `voyager 1 one light day` |
| Hook promise | One sentence — Because radio waves travel at `300,000 km/s` (`186,000 mi/s`), a one-way command takes `24 hours` to reach `Voyager 1` at `1 light-day` (`25.9 billion km` on `November 18, 2026`) and `4.24 years` to reach `Proxima Centauri`, which is why onboard AI autonomy (`Deep Space 1` `AutoNav`, `Perseverance` driving `>90%` of its record `45.22 km` autonomously, `Curiosity` `AEGIS` `>93%` laser targeting, `DART` `SMART Nav` `73-minute` asteroid intercept, and `0.2 c` `Starshot` / `Von Neumann` probes) is the physical bridge that lets humanity explore deep space. |
| Retention design | Chapters that earn the next minute (teach + turn) |
| Packaging | Thumb readable on mobile; one idea (`24-HOUR RADIO DELAY`) |

---

## 2. Keyword research (vidIQ)

Pull GB (or primary market) research for 5–8 terms.

| Keyword | Overall | Est./mo | Comp | Role (title / desc / chapter / Shorts) | Keep? |
|---------|--------:|--------:|-----:|----------------------------------------|-------|
| `how spacecraft navigate in deep space` | High | High | Low | primary | Yes |
| `voyager 1 one light day from earth` | High | High | Low | primary / cold open / Shorts | Yes |
| `perseverance rover autonomous driving record` | High | Med | Low | chapter / Shorts | Yes |
| `dart spacecraft autonomous navigation smart nav` | Med | Med | Low | chapter / Shorts | Yes |
| `breakthrough starshot laser sail alpha centauri` | High | High | Med | chapter | Yes |
| `von neumann probes self replicating spacecraft` | High | High | Med | chapter / description | Yes |
| `ai in space exploration nasa` | High | High | Med | primary / tags | Yes |

**Decision:** Primary keyword for title lead = `Could AI Help Humanity Reach the Stars? How Autonomous Probes Explore Deep Space`  
**Description first 100 chars must include:** `Could AI help humanity reach the stars, and how do autonomous probes explore deep space beyond radio control?`  

---

## 3. Title ABC (score before VO)

**Growth System v2:** one promise · prefer ≤ ~60 characters · **do not** append `| Orbit's Cosmic Journey` (or similar series suffix). Brand lives in the content.

| | Title | Score | Keep? |
|---|-------|------:|-------|
| A | Could AI Help Humanity Reach the Stars? How Autonomous Probes Explore Deep Space | 95 | **Keep (Lead)** |
| B | Why NASA Probes Must Think for Themselves Beyond Mars | 93 | Backup |
| C | How Autonomous Spacecraft Beat the Speed-of-Light Delay | 92 | Backup |
| Reject (fearbait / off-brand / series-suffix clutter even if high) | Terrifying AI Probes Are Taking Over Space \| Orbit's Cosmic Journey | — | **Reject** |

**Proposed title (awaiting Chief topic lock):** Could AI Help Humanity Reach the Stars? How Autonomous Probes Explore Deep Space  
**Why it wins (score + brand + keyword):** Direct hand-off promised in `055`'s subscribe beat (`"how autonomous probes explore space"`) and closing line (`"whether AI can help humanity reach the stars, and how autonomous probes explore deep space"`), and ranks #1 among unscaffolded backlog topics in the 2026-10-20 weekly audit (`J0708`, Backlog `010`).  

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/056_Could-AI-Help-Humanity-Reach-The-Stars-How-Autonomous-Probes-Explore-Deep-Space/01_Script/autonomous_probes_script_master_v00.md
```

- [x] Score ≥ **90 / 100** (**PASS 95.8 / 100**, Structure gates 8/8, `1,315` spoken words / `1,394` reviewer words, ~`9.3 min`)  
- Scorecard: `templates/SCRIPT_REVIEW_SCORECARD.md`  
- Reject / rewrite if below threshold  

---

## 4. Outlier / competitive patterns (on-brand only)

Pull outliers for the primary topic (≤80K–mid sub channels preferred, plus 1M+ neighbour proof). Ignore meme/movie noise.

| Outlier / pattern | Views / multiple | Steal (structure) | Do **not** copy |
|-------------------|------------------|-------------------|-----------------|
| Kurzgesagt — *AI Just Crossed the Terrifying Line* (`ujkD4SxPKOI`) & *Von Neumann Probes — How We Could Explore the Galaxy* | 21.32M / ~11M+ | Concrete physical scaling of how self-directed probes overcome interstellar travel timescales (`100x–1,000x` speedup) | Doomsday / rogue-AI fear framing |
| Astrum — *NASA's Voyager 1 Journey Through Space* (`e7oLtaZIVaE` & long features) | 1.5M–3M+ | Grounding interstellar distance in the real `24-hour` one-way radio delay at `1 light-day` (`25.9 billion km` on `Nov 18, 2026`) | Long static shot holds |
| Cool Worlds (David Kipping) — *Interstellar Probes, Breakthrough Starshot & Autonomous Navigation* | 1.5M+ | Quantitative engineering breakdown of why `0.2 c` flybys at `4.24 light-years` require complete onboard autonomy | Talking-head lecture pacing |
| NASA JPL / SciShow Space — *How Perseverance & DART Navigate Autonomously* | 1.2M+ | Pairing `Perseverance`'s `45.22 km` `AutoNav` record (`600,000` points vs `20` on `Sojourner`) with `DART`'s `73-minute` `SMART Nav` lock at `6.1 km/s` | Dry press-release listing |

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
| Primary keyword (`Could AI Help Humanity Reach the Stars`, `How Autonomous Probes Explore Deep Space`) | Title lead + 0:00 spoken question + description first 100 chars |
| High-volume related term (`Voyager 1 one light day`, `Perseverance AutoNav record`, `DART SMART Nav`, `Breakthrough Starshot`, `Von Neumann probes`) | Cold open anchors on `Voyager 1` reaching `1 light-day` (`25.9B km`, `24-hour` delay) on `Nov 18, 2026` vs `4.24 years` to `Proxima Centauri` |
| Winning outlier structure | Hook + 5-chapter escalation: `Deep Space 1` (`1998–2001`, `12` technologies, `AutoNav`, `Remote Agent`, `16,265 hours` ion thrust) → `Perseverance` `45.22 km` record (`Oct 11, 2026`, `>90%` `AutoNav`, `600,000` points vs `20` on `Sojourner`) & `Curiosity` `AEGIS` (`>93%` vs `24%` laser hits) → Midpoint flip (`Wrong.`) on `DART` `SMART Nav` (`73-minute` detection of `170 m` `Dimorphos` at `6.1 km/s`, `33-minute` orbit shift) → `Breakthrough Starshot` (`4.1 m` sail, `9 min` laser push to `0.2 c`) & `Von Neumann` slingshot probes (`100x–1,000x` speedup) → Synthesis & hand-off to `057` (`Callisto`) |
| Weak competition angle | Most videos either sensationalise rogue AI or list sci-fi concepts without flight data; we unite verified JPL flight milestones (`DS1`, `Curiosity`, `DART`, `Perseverance`, `Voyager 1`) with peer-reviewed interstellar scaling |
| Thumb pattern that works | Deep-space probe / laser sail crossing a glowing `24-HOUR RADIO DELAY` signal boundary toward a distant star (no Orbit on thumb) |

**Chapter list after audit** (5 acts, each with a teach-point):

1. **The Spacecraft That Knew Where It Was** — NASA's `Deep Space 1` (launched `Oct. 24, 1998` to test `12 technologies`): how `Remote Agent` AI software and `Autonomous Optical Navigation` (`AutoNav`) triangulated against background stars and steered a xenon ion engine (`weight of a piece of paper`) across `16,265 hours` (`4.3 km/s` delta-v), flying within `26 km` (`16 mi`) of asteroid `9969 Braille` at `15.5 km/s` (`July 29, 1999`) and `2,171 km` (`1,350 mi`) of `Comet Borrelly` at `16.58 km/s` (`Sept. 22, 2001`).  
2. **Thinking While Driving Across Mars** — How `Perseverance` broke `Opportunity`'s `45.16 km` off-world driving record on `Oct. 11, 2026` (`Sol 2,006`) at `45.22 km` (`28.10 mi`) in `5.5 years` vs `~15 years` (`Steven Lee`, `Mark Maimone`), driving `>90%` of its route on `AutoNav` (`412 m/sol`, `600,000` points per look vs `20` on `Sojourner` in `1997`), while `Raymond Francis` and `Tara Estlin`'s `AEGIS` system on `Curiosity` (`May 2016`) lifted autonomous `ChemCam` laser hits over `2.5 km` from `~24%` to `>93%`.  
3. **Seventy-Three Minutes to Lock Onto an Asteroid** — Midpoint flip (`Wrong.`): how `Terik Daly` and `Nancy Chabot` (*Nature*, `April 2023`) showed `DART`'s `SMART Nav` took control `4 hours and 5 minutes` before impact on `Sept. 26, 2022` at `11 million km` from Earth, first spotted `170 m` `Dimorphos` beside `805 m` `Didymos` `73 minutes` out, manoeuvred from `50 minutes` to `2.5 minutes` out, and struck at `6.1 km/s` to shorten the `11 h 55 min` orbit by `32–33 minutes` (`>25x` NASA's `73-second` benchmark).  
4. **Laser Sails and Self-Replicating Probes** — `Kevin Parkin`'s `2018` `Breakthrough Starshot` system model (`1.06 μm` laser accelerating a `4.1 m` sail for `9 minutes` to `0.2 c` — plus a `19 cm` sail at `0.01 c` — reaching `4.24 ly` `Alpha Centauri` in `~21 years`), and `John von Neumann` (`1903–1957`) + `Arwen Nicholson` & `Duncan Forgan`'s `2013` proof that stellar slingshots run `100x` faster than powered flight and self-replicating probes cut galactic exploration timescales by `2 to 3 orders of magnitude` (`100x–1,000x`).  
5. **Why AI Is Humanity's Bridge to the Stars** — Why autonomous probes don't replace astronauts but scout the hazards ahead across the `1957–2026–interstellar` timeline, handing off to `057` (*Why Jupiter's Moon Callisto Is the Most Heavily Cratered World in the Solar System*).  

---

## 6. Retention plan (whole-video watch)

Design for **watching through**, not just CTR (Growth System v2):

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| 0–0:05 | Curiosity spike | Real graded NASA JPL Deep Space Network 70-meter dish + `Voyager 1` trajectory crossing `1 light-day` (`25.9 billion km`) on `November 18, 2026` |
| ~0:15 | Stakes | At `300,000 km/s` (`186,000 mi/s`), radio takes `24 hours` one-way (`48 hours` round-trip) to `Voyager 1` and `4.24 years` (`8.5 years` round-trip) to `Proxima Centauri` (`40.15 trillion km`) |
| ~0:30 | Journey clear | Lived stakes of dodging Martian boulders, hitting an asteroid at `6.1 km/s`, or flying past a star at `0.2 c` with zero help from Earth; cold open runs ~0:55 before Chapter 1 card |
| Chapter starts | Re-hook + chapter card | Each chapter ends on a question answered by the next chapter |
| Mid | Teach while story continues | Orbit compares `Sojourner`'s `20-dot` grid from `1997` with `Perseverance`'s `600,000-point` 3D hazard mesh on Jezero Crater rim (Ch 2) and watches a `4.1 m` light sail accelerate under a `9-minute` `1.06 μm` laser pulse before locking onto `Proxima Centauri` (Ch 4) |
| Final chapter | Payoff + bigger question | Complete `1957–2026–interstellar` autonomy timeline (`24 hr` light-day, `16,265 hr` DS1, `45.22 km` / `>90%` Perseverance AutoNav, `>93%` AEGIS, `73 min` DART SMART Nav, `0.2 c` / `100x–1,000x` interstellar scouts) + hand-off to `057` |
| Outro | Soft return CTA | Hand-off to Jupiter's moon Callisto and its hidden ocean |

- [x] No 30s+ stretch without a new teach or turn  
- [x] Every chapter earns the next one  
- [x] Runtime target **8–12 min** in trust-building window (~9.3 min, 1,315 spoken words)  

---

## 7. Sign-off (block production until checked)

- [ ] Keywords pulled and primary locked  
- [ ] Title ≥90 locked (fearbait / series-suffix clutter rejected)  
- [x] Script reviewer ≥ 90 (**95.8 / 100**, Structure gates 8/8)  
- [x] Outlier patterns mapped into chapter arc  
- [x] Thumb concepts match title promise (one object · one emotion)  
- [x] Chapter teach-points listed (4–6 acts)  
- [x] Cold-open clock (5 / 15 / 30s) written  
- [x] Retention plan filled  
- [x] Production checklist path noted: `templates/PRODUCTION_CHECKLIST_V2.md`  

**Signed off by:**  
**Date:**  

**Only then:** full script → ElevenLabs VO → AI Studio picture (stills first · Veo world · Omni Orbit-only) → edit.
