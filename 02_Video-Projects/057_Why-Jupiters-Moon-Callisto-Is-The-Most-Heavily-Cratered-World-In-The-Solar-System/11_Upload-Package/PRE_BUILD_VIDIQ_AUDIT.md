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
| ID / slug | `057_Why-Jupiters-Moon-Callisto-Is-The-Most-Heavily-Cratered-World-In-The-Solar-System` |
| Working title | Why Jupiter's Moon Callisto Is the Most Heavily Cratered World in the Solar System |
| Date pulled | 2026-10-20 (`J0727` / `J0735`) |
| Credits used (approx) | 0 (`v01` script revision + 16-row `SOURCES.md` verification only; no VO or picture spend) |
| Brand guardrails | Wonder over fearbait · no fake alien clickbait · Orbit DNA |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) |
| Primary keyword overall | `jupiter moon callisto` / `most heavily cratered moon in the solar system` / `callisto subsurface ocean` |
| Hook promise | One sentence — Because `Callisto` (`4,821 km` across, `98.8%` the size of `Mercury`) orbits `1,883,000 km` from `Jupiter` outside the `4:2:1` Laplace orbital resonance that heats `Io`, `Europa`, and `Ganymede`, no volcanoes or tectonic plates ever erased `4 billion years` of impacts (including the `4,000 km` `Valhalla` multi-ring basin), yet `Galileo`'s `11-meter` magnetometer boom revealed an induced magnetic field from a salty ocean `250 km` (`155 miles`) beneath its battered ice crust. |
| Retention design | Chapters that earn the next minute (teach + turn) |
| Packaging | Thumb readable on mobile; one idea (`250 KM DEEP OCEAN`) |

---

## 2. Keyword research (vidIQ)

Pull GB (or primary market) research for 5–8 terms.

| Keyword | Overall | Est./mo | Comp | Role (title / desc / chapter / Shorts) | Keep? |
|---------|--------:|--------:|-----:|----------------------------------------|-------|
| `jupiter moon callisto` | High | High | Low | primary | Yes |
| `most heavily cratered world in the solar system` | High | Med | Low | primary / title | Yes |
| `callisto subsurface ocean galileo` | High | Med | Low | primary / chapter | Yes |
| `valhalla impact basin callisto` | Med | Med | Low | chapter / Shorts | Yes |
| `laplace orbital resonance jupiter moons` | Med | Med | Low | chapter / Shorts | Yes |
| `esa juice mission callisto ganymede` | High | High | Low | chapter / description | Yes |
| `callisto vs mercury size` | Med | Med | Low | cold open / Shorts | Yes |

**Decision:** Primary keyword for title lead = `Why Jupiter's Moon Callisto Is the Most Heavily Cratered World in the Solar System`  
**Description first 100 chars must include:** `Why is Jupiter's moon Callisto the most heavily cratered world in the solar system, and how does it hide a deep ocean?`  

---

## 3. Title ABC (score before VO)

**Growth System v2:** one promise · prefer ≤ ~60 characters · **do not** append `| Orbit's Cosmic Journey` (or similar series suffix). Brand lives in the content.

| | Title | Score | Keep? |
|---|-------|------:|-------|
| A | Why Jupiter's Moon Callisto Is the Most Heavily Cratered World in the Solar System | 95 | **Keep (Lead)** |
| B | Why Jupiter's Cratered Moon Callisto Hides a Deep Ocean | 94 | Backup |
| C | How Jupiter's Moon Callisto Kept 4 Billion Years of Craters | 92 | Backup |
| Reject (fearbait / off-brand / series-suffix clutter even if high) | Terrifying Alien Ocean Found Inside Callisto \| Orbit's Cosmic Journey | — | **Reject** |

**Proposed title (awaiting Chief topic lock):** Why Jupiter's Moon Callisto Is the Most Heavily Cratered World in the Solar System  
**Why it wins (score + brand + keyword):** Direct hand-off promised in `056`'s subscribe beat (`"why Jupiter's moon Callisto hides a deep ocean"`) and closing line (`"why Jupiter's moon Callisto is the most heavily cratered world in the solar system, and how its ice shell hides a deep ocean"`), and ranks #1 among unscaffolded candidates in the 2026-10-20 weekly audit (`J0722`).  

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/057_Why-Jupiters-Moon-Callisto-Is-The-Most-Heavily-Cratered-World-In-The-Solar-System/01_Script/callisto_cratered_ocean_script_master_v01.md
```

- [x] Score ≥ **90 / 100** (**PASS 95.8 / 100**, Structure gates 8/8, `1,253` spoken words / `1,395` reviewer words, ~`9.3 min`)  
- Scorecard: `templates/SCRIPT_REVIEW_SCORECARD.md`  
- Reject / rewrite if below threshold  

---

## 4. Outlier / competitive patterns (on-brand only)

Pull outliers for the primary topic (≤80K–mid sub channels preferred, plus 1M+ neighbour proof). Ignore meme/movie noise.

| Outlier / pattern | Views / multiple | Steal (structure) | Do **not** copy |
|-------------------|------------------|-------------------|-----------------|
| Astrum — *Callisto: The Dead Moon That Hides an Ocean* & *Could Neptune's Moon Triton Be Habitable?* (`MGQcrX7DMYw`) | ~1.8M / 772k | Contrast between a 4-billion-year cratered exterior (`4,000 km` Valhalla basin) and a magnetically detected subsurface ocean (`250 km` deep) | Long static shot holds |
| SEA / PBS Space Time — *The Galilean Moons & Laplace Orbital Resonance* | 1M–3M+ | Visualising why Callisto sits at `1,883,000 km` (`16.689 days`) outside the `4:2:1` resonance of Io, Europa, and Ganymede | Dry textbook narration |
| SciShow Space / NASA JPL — *How Galileo Discovered Oceans Under Europa and Callisto* | 1.2M+ | Explaining electromagnetic induction via Galileo's `11 m` magnetometer boom (`Khurana, Kivelson & Stevenson 1998`) and `100 km` `CO2` airglow (`Carlson 1999`) | Talking-head studio format |

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
| Primary keyword (`Why Jupiter's Moon Callisto Is the Most Heavily Cratered World in the Solar System`) | Title lead + 0:00 spoken question + description first 100 chars |
| High-volume related term (`Valhalla impact basin`, `Laplace resonance`, `Callisto ocean`, `ESA JUICE`) | Cold open compares `4,821 km` Callisto (`15,144 km` / `9,410 mi` circumference) with `4,879 km` Mercury (`98.8%` width, `1,830` vs `5,427 kg/m³`, `1.24 m/s²` gravity) and names the `4,000 km` Valhalla basin and `250 km` deep ocean |
| Winning outlier structure | Hook + 5-chapter escalation: `Galileo Galilei` (`Jan 7, 1610`) & `Pierre-Simon Laplace`'s `4:2:1` resonance (`1,883,000 km`, `16.689 d` isolated orbit) → `4,000 km` `Valhalla` basin (`Nov 4, 1996` `60 m` Galileo view) & `Anderson/Schubert` (`June 5, 1998`) partial differentiation (`<350 km` ice, `<25%` core) → Midpoint flip (`Wrong.`) on `Khurana, Kivelson & Stevenson` (`Oct 22, 1998`) induced magnetic field & `250 km` salty ocean → `Carlson` (`Feb 5, 1999`) `100 km` `CO2` airglow (`7.5 × 10⁻¹² bar`, `4-year` lifetime) & `ESA/NASA JUICE` (`April 14, 2023`–`July 2031`) → Synthesis & hand-off to `058` (`Magnetar & Quasar Jet`) |
| Weak competition angle | Most videos call Callisto "boring" without showing the exact `C3/C9/C10` gravity data, `11 m` magnetometer eddy currents, and `4-year` `CO2` airglow replenishment |
| Thumb pattern that works | Glittering crater-saturated Callisto cutaway showing the `4,000 km` Valhalla rings above a glowing blue `250 KM DEEP OCEAN` (no Orbit on thumb) |

**Chapter list after audit** (5 acts, each with a teach-point):

1. **The Outer Moon Outside the Resonance** — Discovered `Jan. 7, 1610` by `Galileo Galilei` (`1564–1642`), why `Callisto` (`1,883,000 km`, `16.689 days`, `8.2 km/s`, `0.007` eccentricity) sits `1.8x` farther than `Ganymede`, `2.8x` farther than `Europa`, and `4.5x` farther than `Io` outside `Pierre-Simon Laplace`'s (`1749–1827`) `4:2:1` orbital resonance, escaping tidal resurfacing.  
2. **Valhalla and Four Billion Years of Scars** — How `Voyager` (`1979`) and `Galileo` (`1995–2003`, `34` orbits, `8` Callisto flybys, `Nov. 4, 1996` `60 m` resolution from `1,219 km`) mapped the `4,000 km` (`2,500 mi`) `Valhalla` multi-ring basin at `-155 °C`, and how `John D. Anderson` and `Gerald Schubert` (`1939–2025`, *Science*, `June 5, 1998`) proved Callisto is only partially differentiated (`<350 km` outer clean-ice shell, `<25%` core radius).  
3. **Why the "Ugly Duckling Moon" Hides an Ocean** — Midpoint flip (`Wrong.`): how `Krishan Khurana`, `Margaret Kivelson` (`born 1928`), and `David J. Stevenson` (`born 1948`, *Nature*, `Oct. 22, 1998`) used Galileo's `11 m` magnetometer boom to detect induced magnetic fields from eddy currents in a subsurface salty ocean `250 km` (`155 mi`) deep.  
4. **The Four-Year Atmosphere and Europe's Icy Moon Explorer** — `Robert W. Carlson`'s (`born 1941`, *Science*, `Feb. 5, 1999`) discovery of `100 km` `CO2` `nu3` airglow at `150 K` and `7.5 × 10⁻¹² bar` with a `4-year` sweeping lifetime (plus `O2` and `H`), and `ESA/NASA`'s `6,000 kg` (`2,400 kg` dry) `JUICE` spacecraft (`85 m²` solar panels, arriving `July 2031`).  
5. **The Time Capsule That Hid a Sea** — Synthesis across the `1610–2031` timeline showing why a crater-saturated exterior can still hide an ocean, handing off to `058` (*What Is the Most Dangerous Place in the Universe? Inside a Magnetar and Quasar Jet*).  

---

## 6. Retention plan (whole-video watch)

Design for **watching through**, not just CTR (Growth System v2):

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| 0–0:05 | Curiosity spike | Real graded NASA Galileo global color mosaic of Callisto (`PIA03456`) + `4,821 km` vs `4,879 km` Mercury scale comparison |
| ~0:15 | Stakes | `4 billion years` of un-erased craters on the outside vs a `250 km` (`155 mi`) salty ocean hidden underneath |
| ~0:30 | Journey clear | Standing beside the `4,000 km` `Valhalla` rings at `778 million km` (`43 min` sunlight) where density is `1,830 kg/m³` vs Mercury's `5,427 kg/m³`; cold open runs ~0:55 before Chapter 1 card |
| Chapter starts | Re-hook + chapter card | Each chapter ends on a question answered by the next chapter |
| Mid | Teach while story continues | Orbit projects a cross-section of Valhalla's `4,000 km` rings and `<350 km` ice shell (Ch 2) and looks up through the `100 km` `CO2` airglow as `JUICE`'s `85 m²` solar wings glide overhead (Ch 4) |
| Final chapter | Payoff + bigger question | Complete `1610–2031` Callisto discovery timeline (`4 billion years`, `4,000 km` Valhalla, `<350 km` ice, `250 km` ocean, `4-year` `CO2` renewal, `July 2031` `JUICE`) + hand-off to `058` |
| Outro | Soft return CTA | Hand-off to magnetars and quasar jets (`058`) |

- [x] No 30s+ stretch without a new teach or turn  
- [x] Every chapter earns the next one  
- [x] Runtime target **8–12 min** in trust-building window (~9.3 min, 1,253 spoken words / 1,395 reviewer words)  

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
