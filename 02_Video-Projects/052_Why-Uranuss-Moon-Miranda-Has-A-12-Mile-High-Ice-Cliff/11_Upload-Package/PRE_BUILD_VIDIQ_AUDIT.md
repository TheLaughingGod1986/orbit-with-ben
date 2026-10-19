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
| ID / slug | `052_Why-Uranuss-Moon-Miranda-Has-A-12-Mile-High-Ice-Cliff` |
| Working title | Why Uranus's Moon Miranda Has a 12-Mile-High Ice Cliff |
| Date pulled | 2026-10-19 |
| Credits used (approx) | 0 (`v01` script draft only; no VO or picture spend) |
| Brand guardrails | Wonder over fearbait · no conspiracy · Orbit DNA |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) |
| Primary keyword overall | `uranus moon miranda` / `verona rupes` / `tallest cliff in the solar system` |
| Hook promise | One sentence — Voyager 2 discovered a 12-mile-high (20 km) ice cliff on Uranus's tiny 293-mile moon Miranda not because the moon was shattered and reassembled, but because orbital resonances flexed its interior and melted a subsurface ocean at least 62 miles deep beneath a 19-mile ice crust. |
| Retention design | Chapters that earn the next minute (teach + turn) |
| Packaging | Thumb readable on mobile; one idea (`12-MILE DROP`) |

---

## 2. Keyword research (vidIQ)

Pull GB (or primary market) research for 5–8 terms.

| Keyword | Overall | Est./mo | Comp | Role (title / desc / chapter / Shorts) | Keep? |
|---------|--------:|--------:|-----:|----------------------------------------|-------|
| `uranus moon miranda` | High | High | Low | primary | Yes |
| `verona rupes` | High | Med | Low | primary | Yes |
| `tallest cliff in the solar system` | High | High | Med | secondary / Shorts | Yes |
| `miranda ocean` | Med | Med | Low | chapter | Yes |
| `voyager 2 uranus` | High | Med | Med | chapter | Yes |
| `frankenstein moon` | Med | Low | Low | chapter / Shorts | Yes |
| `uranus moons` | High | High | Med | umbrella | Yes |

**Decision:** Primary keyword for title lead = `Why Uranus's Moon Miranda Has a 12-Mile-High Ice Cliff`  
**Description first 100 chars must include:** `Why does Uranus's smallest major moon Miranda have a 12-mile-high ice cliff called Verona Rupes?`  

---

## 3. Title ABC (score before VO)

**Growth System v2:** one promise · prefer ≤ ~60 characters · **do not** append `| Orbit's Cosmic Journey` (or similar series suffix). Brand lives in the content.

| | Title | Score | Keep? |
|---|-------|------:|-------|
| A | Why Uranus's Moon Miranda Has a 12-Mile-High Ice Cliff | 95 | **Keep (Lead)** |
| B | How a 293-Mile Moon Grew a 12-Mile-High Cliff of Ice | 93 | Backup |
| C | What Tore Uranus's Moon Miranda Apart from the Inside? | 92 | Backup |
| Reject (fearbait / off-brand / series-suffix clutter even if high) | Did Aliens Build This 12-Mile Wall on Uranus's Moon? \| Orbit's Cosmic Journey | — | **Reject** |

**Locked title:** Why Uranus's Moon Miranda Has a 12-Mile-High Ice Cliff  
**Why it wins (score + brand + keyword):** Direct hand-off promised in `051` (`"subscribe for Uranus's moon Miranda and its giant ice cliff"`), names the planet and moon (`Uranus's Moon Miranda`) and the concrete extreme physical feature (`12-Mile-High Ice Cliff`, 54 chars).  

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/052_Why-Uranuss-Moon-Miranda-Has-A-12-Mile-High-Ice-Cliff/01_Script/miranda_ice_cliff_script_master_v01.md
```

- [x] Score ≥ **90 / 100** (**PASS 95.8 / 100**)  
- Scorecard: `templates/SCRIPT_REVIEW_SCORECARD.md`  
- Reject / rewrite if below threshold  

---

## 4. Outlier / competitive patterns (on-brand only)

Pull outliers for the primary topic (≤80K–mid sub channels preferred). Ignore meme/movie noise.

| Outlier / pattern | Views / multiple | Steal (structure) | Do **not** copy |
|-------------------|------------------|-------------------|-----------------|
| Astrum — *What Voyager Saw on Uranus's Moons* / Uranus moons deep dive | 1.5M+ | Voyager 2 close-approach trajectory + geological puzzle reveal | 10-second static shot holds |
| SciShow Space — *Miranda: The Frankenstein Moon* / Verona Rupes | 1.1M+ | 12-mile Grand Canyon scale comparison + low-gravity free-fall hook | Studio host on camera |
| SEA / History of the Universe — *The Strangest Moons in the Solar System* | 2.4M+ | Midpoint flip from shatter-and-reassemble myth to resonant tidal heating | Multi-hour anthology length |
| V101 Space / Kurzgesagt — *Voyager 2 at Uranus* & extreme solar system cliffs | 1.8M+ | Clear interior cutaway of ice shell vs subsurface ocean | Flat vector planet discs |

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
| Primary keyword (`Uranus's Moon Miranda`, `Verona Rupes`, `12-Mile-High Ice Cliff`) | Title lead + 0:00 spoken question + description first 100 chars |
| High-volume related term (`tallest cliff in the solar system`, `Miranda ocean`) | Cold open compares Verona Rupes (12 miles / 20 km, 10–12× Grand Canyon, 10-min rock fall, 12-min skydiver drop to 200 km/h) and Ch 5 reveals the Oct 2024 ≥62-mile ocean model |
| Winning outlier structure | Hook + 6-chapter investigation: Verona Rupes drop → 1948 Kuiper discovery & 1:7 Moon scale → Jan 24, 1986 22,500-mile Voyager 2 flyby → 3 coronae vs shatter myth → PIA00044 3-mile slickensides & orbital resonance → Oct 2024 ≥62-mile ocean model → unseen northern hemisphere |
| Weak competition angle | Older videos repeat the 1986 shatter-and-reassemble hypothesis; we center the Oct 16 / Oct 28, 2024 *Planetary Science Journal* / Johns Hopkins APL computer model (≥62-mile ocean beneath ≤19-mile ice crust 100–500 Myr ago) plus the 2023 particle reanalysis and 2024 JWST Ariel study |
| Thumb pattern that works | Voyager 2 sunlit fault wall of Verona Rupes (`PIA00044` / `PIA18185`) with 1-mile Grand Canyon scale silhouette (`12-MILE DROP`, no Orbit) |

**Chapter list after audit** (6 acts, each with a teach-point):

1. **The Last Moon Found Before Voyager 2** — Gerard Kuiper's Feb. 16, 1948 telescope discovery at McDonald Observatory (`The Tempest` naming), 293.0-mile (`471.6 km`) diameter (`1/7` Earth's Moon), equal water ice and silicate rock, and ≤1/3 sunlight reflectivity at 1.8 billion miles from the Sun.  
2. **The Flyby at the Edge of the Sunlight** — Why Voyager 2 flew within 22,500 miles (`36,250 km`) of Miranda on Jan. 24, 1986 (vs 229,000 miles at Titania, `PIA00039`), and how JPL NAIF pointing and USGS Flagstaff registered 9 images (7 closest-approach frames, `PIA01490`) at 2,160-foot (`660 m`) resolution (`PIA00044`).  
3. **Three Coronae on a Frankenstein Moon** — Why the "dead frozen ball of ice" assumption failed (`Wrong.`), revealing 3 unique trapezoidal coronae and a bright chevron beside 3-to-20-mile (`5–30 km`) craters (`PIA00042` at 91,000 mi / 1.7 mi res; `PIA00141` at 700 m / 2,300 ft res).  
4. **Slickensides and the Tilted Orbit** — How `PIA00044`'s 3-mile (`5 km`) fault scarp with slickenside grooves and Verona Rupes's 12-mile (`20 km`) limb drop trace global stretching from past integer-ratio orbital resonances (like Io and Europa's 2:1 resonance).  
5. **The Sixty-Two-Mile Ocean Beneath the Ice** — How the Oct. 16 / Oct. 28, 2024 *Planetary Science Journal* / JHU APL study proved resonant tidal heating melted an ocean ≥62 miles (`100 km`) deep under an ice crust ≤19 miles (`30 km`) thick (filling nearly half Miranda's 146-mile radius, like Enceladus before Cassini in 2004).  
6. **The Unseen Half of Miranda** — Why scientists caution Miranda is not yet a confirmed ocean world despite 2023 Voyager 2 particle reanalysis and 2024 JWST Ariel findings: Voyager 2 imaged only 1 of Miranda's 2 hemispheres (`PIA18185`, `PIA01361`), leaving the northern half unmapped.  

---

## 6. Retention plan (whole-video watch)

Design for **watching through**, not just CTR (Growth System v2):

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| 0–0:05 | Curiosity spike | Real Voyager 2 fault scarp `PIA00044` + APOD Verona Rupes limb view |
| ~0:15 | Stakes | 12-mile (20 km) drop (10–12× Grand Canyon), ≥62-mile subsurface ocean under ≤19-mile ice shell |
| ~0:30 | Journey clear | 10-min rock fall & 12-min skydiver drop to 200 km/h; cold open runs ~1:00 before Chapter 1 card (no full-frame chapter card in first 30s) |
| Chapter starts | Re-hook + chapter card | Each chapter ends on a question answered by the next chapter |
| Mid | Teach while story continues | Orbit floats beside Voyager 2's narrow-angle camera (Ch 2) and braces his magnetic boots on the PIA00044 slickenside fault ridge (Ch 4) |
| Final chapter | Payoff + bigger question | 1 imaged southern hemisphere vs 1 unmapped northern hemisphere + hand-off to `053` (NASA's Parker Solar Probe Inside the Sun's Corona) |
| Outro | Soft return CTA | Hand-off to Parker Solar Probe's coronal dive |

- [x] No 30s+ stretch without a new teach or turn  
- [x] Every chapter earns the next one  
- [x] Runtime target **8–12 min** in trust-building window (~8.6 min)  

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
