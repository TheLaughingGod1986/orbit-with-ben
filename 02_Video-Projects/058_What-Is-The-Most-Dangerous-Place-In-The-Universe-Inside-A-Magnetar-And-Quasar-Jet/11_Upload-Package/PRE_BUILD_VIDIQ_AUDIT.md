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
| ID / slug | `058_What-Is-The-Most-Dangerous-Place-In-The-Universe-Inside-A-Magnetar-And-Quasar-Jet` |
| Working title | What Is the Most Dangerous Place in the Universe? Inside a Magnetar and Quasar Jet |
| Date pulled | 2026-10-20 (`J0742`) |
| Credits used (approx) | 0 (`v00` script draft + 15-row `SOURCES.md` verification only; no VO or picture spend) |
| Brand guardrails | Wonder over fearbait · no fake alien clickbait · Orbit DNA |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) |
| Primary keyword overall | `most dangerous place in the universe` / `magnetar vs quasar` / `sgr 1806-20 giant flare` |
| Hook promise | One sentence — Because a `20 km` (`12 mi`, Manhattan-sized) `magnetar` packs `500,000` Earth masses into a `10¹⁵ gauss` (`1 quadrillion gauss`) magnetic field that unleashed `250,000 years` of solar energy in `0.2 seconds` during `SGR 1806-20`'s `December 27, 2004` flare while a supermassive black hole `quasar` (`800 million` to `12 billion` solar masses) fires relativistic jets across hundreds of thousands of light-years at `40 trillion` solar luminosities (`26-million-light-year` ionized zone), these cosmic engines form the deadliest environments in space. |
| Retention design | Chapters that earn the next minute (teach + turn) |
| Packaging | Thumb readable on mobile; one idea (`1 QUADRILLION GAUSS`) |

---

## 2. Keyword research (vidIQ)

Pull GB (or primary market) research for 5–8 terms.

| Keyword | Overall | Est./mo | Comp | Role (title / desc / chapter / Shorts) | Keep? |
|---------|--------:|--------:|-----:|----------------------------------------|-------|
| `most dangerous place in the universe` | High | High | Low | primary / title | Yes |
| `magnetar giant flare sgr 1806-20` | High | Med | Low | primary / chapter | Yes |
| `quasar jet supermassive black hole` | High | High | Low | primary / title | Yes |
| `neutron star collision gw170817` | Med | Med | Low | chapter / Shorts | Yes |
| `1 quadrillion gauss magnetic field` | Med | Med | Low | cold open / Shorts | Yes |
| `quasar 3c 273 m87 jet` | Med | Med | Low | chapter / description | Yes |
| `gamma ray burst neutron star merger` | High | Med | Low | chapter / Shorts | Yes |

**Decision:** Primary keyword for title lead = `What Is the Most Dangerous Place in the Universe? Inside a Magnetar and Quasar Jet`  
**Description first 100 chars must include:** `Why are magnetars and quasar jets the most dangerous places in the universe, and how do they work?`  

---

## 3. Title ABC (score before VO)

**Growth System v2:** one promise · prefer ≤ ~60 characters · **do not** append `| Orbit's Cosmic Journey` (or similar series suffix). Brand lives in the content.

| | Title | Score | Keep? |
|---|-------|------:|-------|
| A | What Is the Most Dangerous Place in the Universe? Inside a Magnetar and Quasar Jet | 95 | **Keep (Lead)** |
| B | Why Magnetars and Quasar Jets Are the Most Dangerous Places in Space | 94 | Backup |
| C | Inside a Magnetar Flare and a 40-Trillion-Sun Quasar Jet | 92 | Backup |
| Reject (fearbait / off-brand / series-suffix clutter even if high) | A Magnetar Flare Will Destroy Earth Soon \| Orbit's Cosmic Journey | — | **Reject** |

**Proposed title (awaiting Chief topic lock):** What Is the Most Dangerous Place in the Universe? Inside a Magnetar and Quasar Jet  
**Why it wins (score + brand + keyword):** Direct hand-off promised in `057`'s subscribe beat (`"why magnetars are the most dangerous objects in space"`) and closing line (`"what is the most dangerous place in the universe, inside a magnetar and a quasar jet"`), backlog item `011` in `VIDEO_BACKLOG.json`, and #1 among unscaffolded candidates in the 2026-10-20 weekly audit (`J0737`).  

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/058_What-Is-The-Most-Dangerous-Place-In-The-Universe-Inside-A-Magnetar-And-Quasar-Jet/01_Script/magnetar_quasar_jet_script_master_v00.md
```

- [x] Score ≥ **90 / 100** (**PASS 95.8 / 100**, Structure gates 8/8, `1,351` spoken words / `1,422` reviewer words, ~`9.5 min`)  
- Scorecard: `templates/SCRIPT_REVIEW_SCORECARD.md`  
- Reject / rewrite if below threshold  

---

## 4. Outlier / competitive patterns (on-brand only)

Pull outliers for the primary topic (≤80K–mid sub channels preferred, plus 1M+ neighbour proof). Ignore meme/movie noise.

| Outlier / pattern | Views / multiple | Steal (structure) | Do **not** copy |
|-------------------|------------------|-------------------|-----------------|
| Kurzgesagt — *Neutron Stars — The Most Extreme Things that are not Black Holes* & *Quasars* | ~22M / ~11M | Quantitative physical lethality ladder escalating from `20 km` magnetars (`10¹⁵ gauss`) to supermassive black hole quasars (`40 trillion` Suns) | Doom/fearbait tone |
| Astrum — *What Is It Like on the Surface of a Black Hole Planet?* (`PxJSOWyYWkc`) & *Birth of One of the Strangest Objects in the Universe* (`tlmj5ThgWbY`) | 1.34M / 808k | Immersive physical scale (`Manhattan Island` 20 km sphere vs `26-million-light-year` quasar ionized zone) | Long static shot holds |
| SEA / PBS Space Time — *Magnetars, SGR 1806-20 & Quasar Relativistic Jets* | 1.5M–4M+ | Explaining `SGR 1806-20`'s `Dec. 27, 2004` `0.2 s` flare (`2 × 10⁴⁶ ergs`), `GW170817`'s `1.7 s` GRB, and `M87` / `3C 273` / `ULAS J1342+0928` jets | Dry textbook narration |

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
| Primary keyword (`What Is the Most Dangerous Place in the Universe? Inside a Magnetar and Quasar Jet`) | Title lead + 0:00 spoken question + description first 100 chars |
| High-volume related term (`SGR 1806-20`, `1 quadrillion gauss`, `GW170817`, `quasar jet`, `M87`, `3C 273`) | Cold open compares a `20 km` (`12 mi`, Manhattan-sized) `10¹⁵ gauss` magnetar (`0.2 s` = `250,000` Sun-years) with a `40-trillion-Sun` quasar (`26-million-light-year` ionized zone) |
| Winning outlier structure | Hook + 5-chapter escalation: `20 km` (`500,000` Earths) magnetar (`Duncan 1942`, `Kouveliotou 1953`, `5–12 s` spin, `>10¹⁴–10¹⁵ G`, `SGR 1900+14` `Aug 1998` ring & `SGR 1935+2154` `Oct 2022` FRB) → `SGR 1806-20` `Dec 27, 2004` `380 s` giant flare (`Hurley`, `Palmer`, `Gehrels`, `Gaensler` `April 28, 2005` *Nature*: `0.2 s` = `250,000` Sun-years, `2 × 10⁴⁶ ergs`, `0.25c` nebula) → Midpoint flip (`Wrong.`) on `Aug 17, 2017` `GW170817` (`11.9 km` neutron stars, `2.74 M☉`, `1.7 s` `GRB 170817A` at `40 Mpc`) → Quasar `billion-degree` corona & relativistic jets (`Curtis 1918` M87 at `55 Mly`, `Schmidt 1963` `3C 273` at `2.4 Gly`, `Wu 2015` `12B M☉` `SDSS J0100+2802` `26 Mly` zone, `Bañados 2018` `4 × 10¹³ L☉` `ULAS J1342+0928` at `690 Myr`) → Synthesis & hand-off to `059` (`Olympus Mons`) |
| Weak competition angle | Most videos list "scary space objects" without the exact `Nature` / `PRL` / `Science` measurements (`0.2 s` = `250,000` Sun-years, `2 × 10⁴⁶ ergs`, `1.7 s` GRB delay, `26 Mly` proximity zone) |
| Thumb pattern that works | Blazing magnetar magnetic arcs and relativistic quasar jet with bold top-band hook `1 QUADRILLION GAUSS` (no Orbit on thumb) |

**Chapter list after audit** (5 acts, each with a teach-point):

1. **The Manhattan-Sized Star with a Quadrillion-Gauss Field** — How a supernova crushes `500,000` Earth masses into a `20 km` (`12 mi`, Manhattan Island) neutron star, and how `Robert C. Duncan` (`born 1942`) and `Chryssa Kouveliotou` (`born 1953`) showed that magnetars spin every `5–12 s` with `>10¹⁴–10¹⁵ gauss` fields (`SGR 1900+14`'s `August 1998` cavity ring & `SGR 1935+2154`'s `October 2022` fast radio burst).  
2. **The 0.2-Second Flare That Hit Earth's Atmosphere** — How `SGR 1806-20`'s `December 27, 2004` `380 s` giant flare (`Kevin Hurley`, `David M. Palmer`, `Neil Gehrels`, `Bryan M. Gaensler`, *Nature*, `April 28, 2005`) released `250,000 years` of solar energy in `0.2 s` (`2 × 10⁴⁶ ergs`), disturbed Earth's upper ionosphere, and drove a `4 × 10⁴³ erg` radio nebula at `0.25c` (`day 6–19`).  
3. **When Two Neutron Stars Collide in 1.7 Seconds** — Midpoint flip (`Wrong.`): how `LIGO`, `Virgo`, and `Fermi` observed `GW170817` and `GRB 170817A` on `August 17, 2017` (`12:41:04 UTC`) in `NGC 4993` (`40 Mpc`) as two `11.9 km` neutron stars (`2.74 M☉`, `3.5 × 10³⁴ dyn cm⁻²`) merged and fired a short gamma-ray burst `1.7 s` later.  
4. **Inside a Quasar's Billion-Degree Corona and 40-Trillion-Sun Jet** — How a supermassive black hole's `billion-degree` magnetic corona and accretion disk launch relativistic jets across hundreds of thousands of light-years (`Heber Curtis` `1918` M87 at `55 Mly`, `Maarten Schmidt` `1963` `3C 273` at `2.4 Gly`, `Xue-Bing Wu` `2015` `12B M☉` `SDSS J0100+2802` ionizing `26 Mly`, and `Eduardo Bañados` `2018` `ULAS J1342+0928` shining at `4 × 10¹³ L☉` at `690 Myr`).  
5. **Why Distance Is Our Greatest Shield** — Synthesis across the `1918–2022` cosmic lethality ladder showing how distance protects Earth while extreme physics forges heavy elements, handing off to `059` (*Why Mars Built a Volcano Three Times Taller Than Mount Everest — Olympus Mons*).  

---

## 6. Retention plan (whole-video watch)

Design for **watching through**, not just CTR (Growth System v2):

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| 0–0:05 | Curiosity spike | Real graded NASA Spitzer/Hubble composite of magnetar `SGR 1900+14` (`PIA10711`) and quasar jet (`PIA08617`) + `20 km` (`10¹⁵ G`) vs `26 Mly` scale |
| ~0:15 | Stakes | A `20 km` magnetar unleashing `250,000 years` of sunlight in `0.2 s` vs a `billion-degree` quasar corona and jet sterilizing `26 million light-years` |
| ~0:30 | Journey clear | Hovering near a `1-quadrillion-gauss` magnetar or looking down a relativistic quasar jet; cold open runs ~0:55 before Chapter 1 card |
| Chapter starts | Re-hook + chapter card | Each chapter ends on a question answered by the next chapter |
| Mid | Teach while story continues | Orbit projects the `0.2 s` `SGR 1806-20` flare and `0.25c` radio shell (Ch 2) and floats outside the `26-million-light-year` quasar ionized zone comparing it to the Milky Way (Ch 4) |
| Final chapter | Payoff + bigger question | Complete `1918–2022` cosmic lethality ladder (`20 km` / `10¹⁵ G` magnetar, `0.2 s` / `2 × 10⁴⁶ erg` flare, `1.7 s` GRB, `40-trillion-Sun` / `26 Mly` quasar) + hand-off to `059` |
| Outro | Soft return CTA | Hand-off to Mars's giant volcano Olympus Mons (`059`) |

- [x] No 30s+ stretch without a new teach or turn  
- [x] Every chapter earns the next one  
- [x] Runtime target **8–12 min** in trust-building window (~9.5 min, 1,351 spoken words / 1,422 reviewer words)  

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
