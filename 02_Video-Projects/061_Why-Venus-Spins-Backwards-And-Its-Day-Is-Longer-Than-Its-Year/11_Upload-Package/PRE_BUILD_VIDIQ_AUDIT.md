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
| ID / slug | `061_Why-Venus-Spins-Backwards-And-Its-Day-Is-Longer-Than-Its-Year` |
| Working title | Why Venus Spins Backwards and Its Day Is Longer Than Its Year |
| Date pulled | 2026-10-21 (`J0789`) |
| Credits used (approx) | 0 (`v00` script draft + 16-row `SOURCES.md` verification only; no VO or picture spend) |
| Brand guardrails | Wonder over fearbait · no fake alien clickbait · Orbit DNA |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) |
| Primary keyword overall | `why venus spins backwards` / `venus day longer than year` / `venus retrograde rotation` |
| Hook promise | One sentence — Because solar heating (`2,601.3 W/m²`) of Venus's crushing `92-bar` carbon dioxide atmosphere creates powerful thermal tides that pull against solar gravitational tides and friction at its `3,500-kilometer` core-mantle boundary, Venus spins backwards once every `243 Earth days` (`−5,832.6 hours`, longer than its `224.7-day` year) so the Sun rises in the west and sets in the east every `116.75 Earth days` while `360 km/h` clouds race `60 times` faster overhead and wobble the day length by up to `20 minutes`. |
| Retention design | Chapters that earn the next minute (teach + turn) |
| Packaging | Thumb readable on mobile; one idea (`243-DAY BACKWARDS SPIN`) |

---

## 2. Keyword research (vidIQ)

Pull GB (or primary market) research for 5–8 terms.

| Keyword | Overall | Est./mo | Comp | Role (title / desc / chapter / Shorts) | Keep? |
|---------|--------:|--------:|-----:|----------------------------------------|-------|
| `why venus spins backwards` | High | High | Low | primary / title | Yes |
| `venus day longer than year` | High | High | Low | primary / title / description | Yes |
| `venus retrograde rotation` | High | Med | Low | primary / description / chapter 1 | Yes |
| `venus solar day 117 days` | Med | Med | Low | chapter 2 / Shorts | Yes |
| `venus atmospheric thermal tides` | Med | Low | Low | chapter 3 / description | Yes |
| `venus super rotation 60 times faster` | Med | Med | Low | chapter 4 / Shorts | Yes |
| `why does the sun rise in the west on venus` | High | Med | Low | description / Shorts | Yes |

**Decision:** Primary keyword for title lead = `Why Venus Spins Backwards and Its Day Is Longer Than Its Year`  
**Description first 100 chars must include:** `Why does Venus spin backwards every 243 Earth days — longer than its 224.7-day year around the Sun?`  

---

## 3. Title ABC (score before VO)

**Growth System v2:** one promise · prefer ≤ ~60 characters · **do not** append `| Orbit's Cosmic Journey` (or similar series suffix). Brand lives in the content.

| | Title | Score | Keep? |
|---|-------|------:|-------|
| A | Why Venus Spins Backwards and Its Day Is Longer Than Its Year | 96 | **Keep (Lead)** |
| B | Why a Day on Venus Lasts Longer Than Its Year Around the Sun | 95 | Backup |
| C | Why the Sun Rises in the West on Venus: The 243-Day Backwards Spin | 93 | Backup |
| Reject (fearbait / off-brand / series-suffix clutter even if high) | Something Flipped Earth's Twin Upside Down \| Orbit's Cosmic Journey | — | **Reject** |

**Proposed title (awaiting Chief topic lock):** Why Venus Spins Backwards and Its Day Is Longer Than Its Year  
**Why it wins (score + brand + keyword):** Direct hand-off promised in `060`'s subscribe beat (`"starting with why Venus spins backwards"`) and closing line (`"why Venus spins backwards and its day is longer than its year"`), and #1 among unscaffolded candidates in the 2026-10-21 weekly audit (`J0784`).  

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/061_Why-Venus-Spins-Backwards-And-Its-Day-Is-Longer-Than-Its-Year/01_Script/venus_retrograde_script_master_v00.md
```

- [x] Score ≥ **90 / 100** (**PASS 95.8 / 100**, Structure gates 8/8, `1,499` reviewer words, ~`10.0 min`)  
- Scorecard: `templates/SCRIPT_REVIEW_SCORECARD.md`  
- Reject / rewrite if below threshold  

---

## 4. Outlier / competitive patterns (on-brand only)

Pull outliers for the primary topic (≤80K–mid sub channels preferred, plus 1M+ neighbour proof). Ignore meme/movie noise.

| Outlier / pattern | Views / multiple | Steal (structure) | Do **not** copy |
|-------------------|------------------|-------------------|-----------------|
| Astrum — *Why Venus Spins Backwards* | 1.6M+ | Clear distinction between `243-day` sidereal spin, `224.7-day` orbital year, and `116.75-day` west-to-east solar day + `92-bar` thermal-tide physics | Slow 10–15s static shot holds |
| SciShow Space — *Why Is a Day on Venus Longer Than Its Year?* | 1.3M+ | Crisp radar discovery arc (`1961–1967` Goldstone/Millstone Doppler radar) + `Correia & Laskar 2001 Nature` four rotation states | Talking-head studio format |
| PBS Space Time — *The Mystery of Venus's Retrograde Rotation* | 1.1M+ | Midpoint flip (`Wrong.`): Venus did not need an upside-down axial flip to spin backwards + `60×` cloud super-rotation (`Horinouchi et al. 2020 Science`) and `±20-minute` radar wobble (`Margot et al. 2021`) | Chalkboard lecture pacing |

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
| Primary keyword (`Why Venus Spins Backwards and Its Day Is Longer Than Its Year`) | Title lead + 0:00 spoken question + description first 100 chars |
| High-volume related term (`Venus`, `Earth`, `Goldstone`, `Magellan`, `Akatsuki`, `thermal tides`, `super-rotation`) | Cold open compares `Venus` (`6,051.8 km` radius / `12,104 km` diameter = `95%` Earth, `4.8673 × 10²⁴ kg` = `81.5%` Earth mass, `224.701 d` orbit, `243 d` / `−5,832.6 h` retrograde spin, `116.75 d` solar day, `177.36°` obliquity) with `Earth` (`6,378.1 km` radius, `365.256 d` orbit, `23.9345 h` prograde spin, `23.44°` tilt) |
| Winning outlier structure | Hook + 5-chapter escalation: `Galileo (1610)`, `Lomonosov (1761)`, `Schiaparelli (19th c.)`, `Pettengill (1961)`, `Goldstein & Carpenter (1963 Science)`, and `Shapiro (1967 Science)` `243.09 ± 0.18 d` radar breakthrough → `243 d` clockwise sidereal spin + `224.7 d` counterclockwise orbit = `116.75 d` (`2,802 h`) west-to-east solar day & `583.92 d` (`5.001444` solar days) Earth synodic alignment → `Gold & Soter (1969)` `92-bar` (`4.8 × 10²⁰ kg`, `65 kg/m³`) atmospheric thermal tides under `2,601.3 W/m²` sunlight opposing solid-body solar gravity → Midpoint flip (`Wrong.`) on `Correia & Laskar (2001 Nature)` `4` final rotation states without axial flip, `Horinouchi (2020 Science)` Akatsuki `60×` (`360 km/h`, `4 d`) super-rotation, & `Margot (2021)` `±20 min` radar wobble over a `3,500 km` core → Exoplanet synthesis (`Leconte 2015 Science`) & hand-off to `062` (`Asteroid 16 Psyche`) |
| Weak competition angle | Most videos repeat the old "giant impact flipped Venus upside down" myth without citing `Correia & Laskar (2001 Nature)`'s proof that prograde rotation can brake and reverse without an axial flip, `Horinouchi et al. (2020 Science)`'s Akatsuki thermal-tide momentum transport, or `Margot et al. (2021)`'s `±20-minute` radar day-length wobble |
| Thumb pattern that works | Golden Mariner 10 / Akatsuki cloud-top portrait of Venus (`PIA23791`) with bold reversed rotation arc and top-band hook `243-DAY BACKWARDS SPIN` (no Orbit on thumb) |

**Chapter list after audit** (5 acts, each with a teach-point):

1. **How Radar Pierced Venus's Clouds and Found a Backwards Spin** — How `Galileo Galilei` (`1564–1642`) (`1610` phases), `Mikhail Lomonosov` (`1711–1765`) (`1761` atmosphere), and `Giovanni Schiaparelli` (`1835–1910`) set the stage before `Gordon H. Pettengill` (`1926–2021`) (`1961`), `Richard M. Goldstein` and `Roland L. Carpenter` (`1963` *Science*, `PMID 17743054`), and `Irwin I. Shapiro` (`born 1929`) (`1967` *Science*, `PMID 17798698`) used Doppler radar to prove Venus spins retrograde every `243.09 ± 0.18 days`.  
2. **The 116.75-Day Solar Day and Where the Sun Rises in the West** — Why a `243.0226-day` (`−5,832.6-hour`) clockwise sidereal spin combined with a `224.701-day` counterclockwise orbit produces a `116.75-day` (`2,802.0-hour`) solar day (`1.92` solar days per year) with west-to-east sunrises and a `583.92-day` synodic period equal to `5.001444` Venusian solar days.  
3. **Crushing 92-Bar Thermal Tides vs Solar Gravity** — How `2,601.3 W/m²` of solar heating (`1.911×` Earth) on Venus's `92-bar`, `4.8 × 10²⁰ kg` (`96.5%` CO₂) atmosphere creates thermal mass bulges (`Thomas Gold` `1920–2004` & `Steven Soter`, `1969`) whose solar gravitational torque opposes solid-body tidal locking.  
4. **Four Final Rotation States, 60× Winds, and a 20-Minute Wobble** — Midpoint flip (`Wrong.`): how `Alexandre C. M. Correia` and `Jacques Laskar` (`born 1955`) (*Nature*, `June 14, 2001`, `PMID 11459048`) proved core-mantle friction and atmospheric tides drive Venus into one of `4` final rotation states without flipping its axis, while `Takeshi Horinouchi` et al. (*Science*, `April 24, 2020`, `PMID 32327594`) showed thermal tides maintain `60×` cloud super-rotation (`360 km/h`, `4-day` period) and `Jean-Luc Margot` (`born 1969`) (`2021`) measured up to `20-minute` day-length fluctuations and a `3,500 km` core.  
5. **What Venus's Backwards Clock Teaches Us About Rocky Worlds** — How `Jérémy Leconte` et al. (*Science*, `February 6, 2015`, `PMID 25592420`) showed thermal tides can prevent habitable-zone exoplanets from tidally locking, uniting the `1610–2023` timeline and handing off to `062` (*Why NASA Launched a Spacecraft to a Giant Metal World — Asteroid 16 Psyche*).  

---

## 6. Retention plan (whole-video watch)

Design for **watching through**, not just CTR (Growth System v2):

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| 0–0:05 | Curiosity spike | Real graded NASA Mariner 10 cloud portrait (`PIA23791`) and Magellan radar surface (`PIA00271`) + `243-day` retrograde spin vs `224.7-day` year scale |
| ~0:15 | Stakes | Why a `12,104 km` twin of Earth spins backwards under `92 bars` of pressure so the Sun rises in the west |
| ~0:30 | Journey clear | Hovering beneath `4-day` (`60×`) sulfuric acid clouds over a `464 °C` surface where sunrise to sunrise takes `116.75 days` and wobbles by `20 minutes`; cold open runs ~0:55 before Chapter 1 card |
| Chapter starts | Re-hook + chapter card | Each chapter ends on a question answered by the next chapter |
| Mid | Teach while story continues | Orbit hovers beside the `224.7-day` orbit + `243-day` spin dial showing the `116.75-day` west-to-east solar day (Ch 2) and dives from `70 km` (`360 km/h`) cloud tops toward the `3,500 km` core watching the `20-minute` wobble dial (Ch 4) |
| Final chapter | Payoff + bigger question | Complete `1610–2023` Venus timeline (`243 d` spin, `224.7 d` year, `116.75 d` solar day, `92-bar` thermal tides, `60×` super-rotation, `±20 min` wobble, `3,500 km` core) + hand-off to `062` |
| Outro | Soft return CTA | Hand-off to NASA's mission to metal asteroid `16 Psyche` (`062`) |

- [x] No 30s+ stretch without a new teach or turn  
- [x] Every chapter earns the next one  
- [x] Runtime target **8–12 min** in trust-building window (~8.6 min, 1,269 spoken words / 1,290 reviewer words)  

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
