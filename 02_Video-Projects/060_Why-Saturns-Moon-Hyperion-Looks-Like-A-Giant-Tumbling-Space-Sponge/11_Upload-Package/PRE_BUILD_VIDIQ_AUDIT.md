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
| ID / slug | `060_Why-Saturns-Moon-Hyperion-Looks-Like-A-Giant-Tumbling-Space-Sponge` |
| Working title | Why Saturn's Moon Hyperion Looks Like a Giant Tumbling Space Sponge |
| Date pulled | 2026-10-21 (`J0773`) |
| Credits used (approx) | 0 (`v00` script draft + 16-row `SOURCES.md` verification only; no VO or picture spend) |
| Brand guardrails | Wonder over fearbait · no fake alien clickbait · Orbit DNA |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) |
| Primary keyword overall | `hyperion moon saturn` / `why hyperion looks like a sponge` / `saturn sponge moon` |
| Hook promise | One sentence — Because Saturn's potato-shaped moon `Hyperion` (`410 × 260 × 220 km`) is an icy rubble pile with a mean density of just `544 kg/m³` and `42 percent` empty space inside, incoming impactors compress its porous ice into razor-sharp `2-to-10-kilometer` honeycomb craters coated in dark hydrocarbons while a `3:4` resonance with `Titan` keeps it tumbling chaotically with a `30-day` Lyapunov time and a `−200-volt` electrostatic charge. |
| Retention design | Chapters that earn the next minute (teach + turn) |
| Packaging | Thumb readable on mobile; one idea (`42% EMPTY SPACE`) |

---

## 2. Keyword research (vidIQ)

Pull GB (or primary market) research for 5–8 terms.

| Keyword | Overall | Est./mo | Comp | Role (title / desc / chapter / Shorts) | Keep? |
|---------|--------:|--------:|-----:|----------------------------------------|-------|
| `hyperion moon` | High | High | Low | primary / title | Yes |
| `saturn moon hyperion` | High | High | Low | primary / title | Yes |
| `why hyperion looks like a sponge` | High | Med | Low | primary / title / description | Yes |
| `chaotic rotation hyperion` | Med | Med | Low | chapter 1 / Shorts | Yes |
| `cassini hyperion flyby` | Med | Med | Low | chapter 2 / description | Yes |
| `hyperion static charge` | Med | Low | Low | chapter 4 / Shorts | Yes |
| `strangest moons of saturn` | High | High | Med | description / tags | Yes |

**Decision:** Primary keyword for title lead = `Why Saturn's Moon Hyperion Looks Like a Giant Tumbling Space Sponge`  
**Description first 100 chars must include:** `Why does Saturn's moon Hyperion look like a giant tumbling space sponge with 42% empty space inside?`  

---

## 3. Title ABC (score before VO)

**Growth System v2:** one promise · prefer ≤ ~60 characters · **do not** append `| Orbit's Cosmic Journey` (or similar series suffix). Brand lives in the content.

| | Title | Score | Keep? |
|---|-------|------:|-------|
| A | Why Saturn's Moon Hyperion Looks Like a Giant Tumbling Space Sponge | 96 | **Keep (Lead)** |
| B | Why Saturn's Sponge Moon Hyperion Tumbles Chaotically Through Space | 95 | Backup |
| C | Inside Hyperion: Saturn's Chaotic Moon That Is 42% Empty Space | 93 | Backup |
| Reject (fearbait / off-brand / series-suffix clutter even if high) | Saturn's Alien Sponge Moon Just Zapped a NASA Spacecraft \| Orbit's Cosmic Journey | — | **Reject** |

**Proposed title (awaiting Chief topic lock):** Why Saturn's Moon Hyperion Looks Like a Giant Tumbling Space Sponge  
**Why it wins (score + brand + keyword):** Direct hand-off promised in `059`'s subscribe beat (`"why Hyperion looks like a sponge"`) and closing line (`"why Saturn's moon Hyperion looks like a giant tumbling space sponge"`), and #1 among unscaffolded candidates in the 2026-10-21 weekly audit (`J0767`).  

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/060_Why-Saturns-Moon-Hyperion-Looks-Like-A-Giant-Tumbling-Space-Sponge/01_Script/hyperion_sponge_script_master_v00.md
```

- [x] Score ≥ **90 / 100** (**PASS 95.8 / 100**, Structure gates 8/8, `1,400` spoken words / `1,420` reviewer words, ~`9.5 min`)  
- Scorecard: `templates/SCRIPT_REVIEW_SCORECARD.md`  
- Reject / rewrite if below threshold  

---

## 4. Outlier / competitive patterns (on-brand only)

Pull outliers for the primary topic (≤80K–mid sub channels preferred, plus 1M+ neighbour proof). Ignore meme/movie noise.

| Outlier / pattern | Views / multiple | Steal (structure) | Do **not** copy |
|-------------------|------------------|-------------------|-----------------|
| Astrum — *Saturn's Strangest Moons: Hyperion, Iapetus & Pan* | 1.4M+ | Crisp Cassini close-up visual contrast (`PIA07740`, `PIA17194`) + physical breakdown of `544 kg/m³` density, `42%` porosity, and `3:4` Titan orbital resonance | Multi-moon anthology dilution |
| SciShow Space — *Why Hyperion Looks Like a Sponge* | 1.1M+ | Clear impact-compression mechanism (`Thomas et al. 2007 Nature`) + dark hydrocarbon crater floor sublimation trap (`Cruikshank et al. 2007 Nature`) | Talking-head studio format |
| SEA / NASA JPL — *Cassini's Strangest Discoveries at Saturn* | 1M–3M+ | Midpoint twist (`Wrong.`): `Nordheim et al. 2014 GRL` discovery of Hyperion's `−200 V` negative surface charge zapping Cassini with an electron beam `6 minutes` before closest approach | Long ambient holds |

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
| Primary keyword (`Why Saturn's Moon Hyperion Looks Like a Giant Tumbling Space Sponge`) | Title lead + 0:00 spoken question + description first 100 chars |
| High-volume related term (`Hyperion`, `Saturn`, `Cassini`, `Titan`, `Mimas`, `Phoebe`, `Iapetus`) | Cold open compares `Hyperion` (`410 × 260 × 220 km`, `270 km` mean diameter, `0.056 × 10²⁰ kg` = `15%` Mimas mass, `544 kg/m³` density, `42%` porosity) with `Mimas` (`0.379 × 10²⁰ kg`, `1,150 kg/m³`) and liquid water (`1,000 kg/m³`) |
| Winning outlier structure | Hook + 5-chapter escalation: `W. C. Bond (1789–1859)`, `G. P. Bond (1825–1865)` & `Lassell (1799–1880)` `Sept. 1848` discovery (`Herschel 1792–1871` `1847` naming), `Greenberg/Counselman/Shapiro (1972)` `3:4` Titan resonance, `Smith (1931–2018)` `1982` Voyager 2 & `Wisdom (born 1953)` `~30 d` Lyapunov chaotic tumble → `Cassini` `500 km` flyby (`Sept. 26, 2005`) & `Thomas (born 1946)` / `Burns (1941–2025)` `2007` *Nature* `544 ± 50 kg/m³` (`>40%` / `42%` porous) rubble pile from `350–1,000 km` proto-Hyperion → Impact compression preserving `2–10 km` honeycomb craters inside the `250 × 200 km` (`35 km` deep) giant crater (`Bond-Lassell Dorsum` `~300 km`) and `140 km` `Helios` crater → Midpoint flip (`Wrong.`) on `Cruikshank (born 1939)` `2007` *Nature* `4×` darker hydrocarbon pit floors (`−180 °C`) & `Nordheim` `2014` *GRL* `−200 V` electron beam → Synthesis & hand-off to `061` (`Venus`) |
| Weak competition angle | Most videos say "Hyperion looks like a sponge" without citing the exact `Nature` and `GRL` measurements (`544 ± 50 kg/m³`, `0.42 ± 0.06` porosity, `2–10 km` compressed craters, `250 × 200 km` / `35 km` deep giant crater, `4×` lower crater-floor albedo, and `−200 V` electron beam `6 min` before closest approach) |
| Thumb pattern that works | Crisp coral-toned Cassini portrait of spongy Hyperion (`PIA07740`) against dark space with bold top-band hook `42% EMPTY SPACE` (no Orbit on thumb) |

**Chapter list after audit** (5 acts, each with a teach-point):

1. **The First Non-Rounded Moon and Its Chaotic Tumble** — How `William Cranch Bond` (`1789–1859`), `George Phillips Bond` (`1825–1865`), and `William Lassell` (`1799–1880`) discovered `Hyperion` in `September 1848` (named after `John Herschel`'s `1847` scheme), and how `Bradford A. Smith` (`1931–2018`) (`1982` *Science*) and `Jack Wisdom` (`born 1953`) showed that its `3:4` resonance with `Titan` and `0.1042` eccentricity drive chaotic rotation (`~13-day` spin, `~30-day` Lyapunov time).  
2. **Cassini's 500-Kilometer Flyby and the 544 kg/m³ Rubble Pile** — How `Cassini` swept within `500 km` of Hyperion on `September 26, 2005` (`PIA07740`) and how `Peter C. Thomas` (`born 1946`) and `Joseph A. Burns` (`1941–2025`) (*Nature*, `July 5, 2007`, `PMID 17611535`) measured a mean density of `544 ± 50 kg/m³` and `>40%` (`0.42 ± 0.06`) porosity inside a water-ice rubble pile from a `350–1,000 km` proto-Hyperion.  
3. **Impact Compression and the 35-Kilometer Giant Crater** — Why impactors compress `42%` porous ice instead of excavating ejecta blankets, preserving `2–10 km` polygon-rimmed honeycomb craters alongside the `140 km` `Helios` crater (`10–25 km` deep) and the `250 × 200 km` (`35 km` deep) giant crater rimmed by the `300 km` `Bond-Lassell Dorsum`.  
4. **Dark Hydrocarbon Pits and a 200-Volt Static Zap** — Midpoint flip (`Wrong.`): how `Dale P. Cruikshank` (`born 1939`) (*Nature*, `July 5, 2007`, `PMID 17611536`) found `4×` darker hydrocarbon and CO₂ crater floors at `−180 °C`, and how `Tom A. Nordheim` (*Geophys. Res. Lett.*, `October 28, 2014`, `PMID 26074639`) detected a `−200 V` electrostatic electron beam `6 minutes` before Cassini's closest approach.  
5. **What a Chaotic Rubble Pile Teaches Us About Planetary Moons** — Synthesis across the `1847–2026` timeline showing how porous rubble and orbital resonances sculpt chaotic moons, handing off to `061` (*Why Venus Spins Backwards and Its Day Is Longer Than Its Year*).  

---

## 6. Retention plan (whole-video watch)

Design for **watching through**, not just CTR (Growth System v2):

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| 0–0:05 | Curiosity spike | Real graded NASA Cassini false-color portrait of `Hyperion` (`PIA07740`) and spongy crater close-up (`PIA17194`) + `544 kg/m³` / `42% empty space` scale |
| ~0:15 | Stakes | Why a `410 × 260 × 220 km` moon is `42%` empty space and tumbles so chaotically you cannot predict sunrise |
| ~0:30 | Journey clear | Floating above `10 km` deep craters at `−180 °C` where a `−200 V` static charge fires electron beams; cold open runs ~0:55 before Chapter 1 card |
| Chapter starts | Re-hook + chapter card | Each chapter ends on a question answered by the next chapter |
| Mid | Teach while story continues | Orbit hovers `500 km` beside Hyperion projecting the `42%` porous rubble-pile cutaway (Ch 2) and glides over a honeycomb pit watching dark hydrocarbons and a `−200 V` electron stream (Ch 4) |
| Final chapter | Payoff + bigger question | Complete `1847–2026` Hyperion timeline (`410 × 260 × 220 km`, `544 kg/m³`, `42%` porosity, `3:4` Titan resonance, `30 d` Lyapunov chaos, `−200 V` charge) + hand-off to `061` |
| Outro | Soft return CTA | Hand-off to Venus's retrograde rotation (`061`) |

- [x] No 30s+ stretch without a new teach or turn  
- [x] Every chapter earns the next one  
- [x] Runtime target **8–12 min** in trust-building window (~9.5 min, 1,400 spoken words / 1,420 reviewer words)  

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
