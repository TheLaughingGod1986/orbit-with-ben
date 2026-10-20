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
| ID / slug | `055_What-Will-Humans-Become-In-1000-Years-What-Spaceflight-Does-To-The-Human-Body` |
| Working title | What Will Humans Become in 1,000 Years? What Spaceflight Does to the Human Body |
| Date pulled | 2026-10-20 (`J0696`) |
| Credits used (approx) | 0 (`v00` script draft only; no VO or picture spend) |
| Brand guardrails | Wonder over fearbait · no body-horror clickbait · Orbit DNA |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) |
| Primary keyword overall | `what spaceflight does to the human body` / `what will humans become in 1000 years` / `nasa twins study` |
| Hook promise | One sentence — Removing Earth's `9.82 m/s²` gravity and magnetic shield strips `1% to 2%` of weight-bearing bone mineral density per month, shifts fluids into the head, and exposes Mars travelers to `0.66 sieverts` of cosmic radiation, yet NASA's `340-day` Twins Study (`91.3%` gene-expression recovery) and high-altitude human genetics (`78%` *EPAS1* selection) show how humanity will adapt over `1,000 years` without ceasing to be human. |
| Retention design | Chapters that earn the next minute (teach + turn) |
| Packaging | Thumb readable on mobile; one idea (`1,000 YEARS IN SPACE`) |

---

## 2. Keyword research (vidIQ)

Pull GB (or primary market) research for 5–8 terms.

| Keyword | Overall | Est./mo | Comp | Role (title / desc / chapter / Shorts) | Keep? |
|---------|--------:|--------:|-----:|----------------------------------------|-------|
| `what happens to the human body in space` | High | High | Med | primary | Yes |
| `what will humans look like in 1000 years` | High | High | Med | primary | Yes |
| `nasa twins study scott kelly` | High | Med | Low | chapter / Shorts | Yes |
| `bone loss in space microgravity` | Med | Med | Low | chapter / Shorts | Yes |
| `mars radiation curiosity rad` | Med | Low | Low | chapter / Shorts | Yes |
| `human evolution on mars` | High | Med | Low | primary / description | Yes |
| `spaceflight neuro ocular syndrome` | Med | Low | Low | chapter | Yes |

**Decision:** Primary keyword for title lead = `What Will Humans Become in 1,000 Years? What Spaceflight Does to the Human Body`  
**Description first 100 chars must include:** `What does spaceflight do to the human body, and what will humans become after 1,000 years in space and on Mars?`  

---

## 3. Title ABC (score before VO)

**Growth System v2:** one promise · prefer ≤ ~60 characters · **do not** append `| Orbit's Cosmic Journey` (or similar series suffix). Brand lives in the content.

| | Title | Score | Keep? |
|---|-------|------:|-------|
| A | What Will Humans Become in 1,000 Years? What Spaceflight Does to the Human Body | 95 | **Keep (Lead)** |
| B | What Happens to the Human Body Over 1,000 Years in Space? | 94 | Backup |
| C | Why Living in Space Rewrites Your DNA, Bones, and Eyes | 92 | Backup |
| Reject (fearbait / off-brand / series-suffix clutter even if high) | Space Turns Humans Into Horrifying Mutants \| Orbit's Cosmic Journey | — | **Reject** |

**Proposed title (awaiting Chief topic lock):** What Will Humans Become in 1,000 Years? What Spaceflight Does to the Human Body  
**Why it wins (score + brand + keyword):** Direct hand-off promised in `054`'s subscribe beat (`"what spaceflight does to the human body"`) and closing line (`"what spaceflight does to the human body, and what humans will become in 1,000 years"`), and ranks #1 among unscaffolded backlog topics in the 2026-10-20 weekly audit (`J0693`, Backlog `008`).  

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/055_What-Will-Humans-Become-In-1000-Years-What-Spaceflight-Does-To-The-Human-Body/01_Script/human_spaceflight_evolution_script_master_v00.md
```

- [x] Score ≥ **90 / 100** (**PASS 95.6 / 100**, Structure gates 8/8, `1,318` spoken words / `1,342` reviewer words, ~`8.9 min`)  
- Scorecard: `templates/SCRIPT_REVIEW_SCORECARD.md`  
- Reject / rewrite if below threshold  

---

## 4. Outlier / competitive patterns (on-brand only)

Pull outliers for the primary topic (≤80K–mid sub channels preferred, plus 1M+ neighbour proof). Ignore meme/movie noise.

| Outlier / pattern | Views / multiple | Steal (structure) | Do **not** copy |
|-------------------|------------------|-------------------|-----------------|
| Astrum — *The Surprising Danger of Building a Human Colony on the Moon* (`UPWQimElMhQ`) | 1.97M+ | Concrete biological and radiation hazards broken down layer by layer from real agency instruments | Long static shot holds |
| Kurzgesagt — *What Happens If You Step Outside Without a Spacesuit / Humans Can Regrow an Organ* (`oNTaHYXQ4MM`) | 1.37M–15M+ | Visceral organ-by-organ progression (fluid shifts, bones, DNA) with crisp quantitative scale bars | Cartoon gore or off-brand tone |
| TED-Ed / SciShow Space — *How Spaceflight Changes the Human Body & The NASA Twins Study* | 1.5M–6M+ | Identical twin astronaut control (`Scott Kelly` 340 days vs `Mark Kelly` on Earth) explaining telomeres and `91.3%` gene-expression recovery | Classroom lecture framing |
| PBS Eons / Evolutionary Biology explainers — *How Fast Can Humans Evolve? (Tibetan EPAS1)* | 1.5M+ | Grounding multi-generational human evolution in the fastest measured human genetic sweep (`78%` *EPAS1* shift across `50` Tibetan exomes) | Speculative sci-fi monster art |

**Patterns we will use in this script:**

- [x] Assumption-flip / open-loop title  
- [x] Numbered layers or chapter journey  
- [x] Body-scale anchor  
- [x] Slow reveal / delayed answer  
- [x] Quantitative biomedical & evolutionary roadmap  
- [ ] Other:  

---

## 5. Incorporate into the build (required)

Translate data → creative decisions **before** writing the full script:

| Data finding | Change to script / chapters / visuals / packaging |
|--------------|-----------------------------------------------------|
| Primary keyword (`What Will Humans Become in 1,000 Years`, `What Spaceflight Does to the Human Body`) | Title lead + 0:00 spoken question + description first 100 chars |
| High-volume related term (`NASA Twins Study`, `Scott Kelly 340 days`, `bone loss in space`, `Mars radiation`) | Cold open pairs Scott and Mark Kelly's `340-day` ISS mission with `1%–2%` monthly bone loss (`6 months` in orbit = `10 years` of Earth aging) and Curiosity RAD's `0.66 Sv` Mars transit dose |
| Winning outlier structure | Hook + 5-chapter progression: NASA Twins Study (`340 days`, `10` teams, `7%` mass loss, telomeres, `91.3%` gene reset) → Microgravity fluid shift (`SANS`, `AQP2`) & Leigh Gabel's 2022 `61 μm` bone CT scans (`17` astronauts, `9/17` incomplete recovery at `12 months`, `-3.9%` vs `-0.4%`) → Curiosity RAD `253-day`, `560M km` Mars transit (`0.66 ± 0.12 Sv`) → Tibetan *EPAS1* exome sweep (`78%` shift across `50` exomes) & `35 generations` (`1,000 years`) at `0.380 g` → Synthesis & hand-off to `056` |
| Weak competition angle | Most videos either list short-term astronaut symptoms or invent sci-fi mutants; we connect real ISS multi-omics (`91.3%` reversible), `61 μm` tibial microarchitecture, Curiosity RAD `0.66 Sv` dosimetry, and the `78%` *EPAS1* human selection benchmark |
| Thumb pattern that works | Split / glowing human DNA & skeletal scale against Mars and the ISS (`1,000 YEARS IN SPACE`, no Orbit) |

**Chapter list after audit** (5 acts, each with a teach-point):

1. **Three Hundred and Forty Days in Orbit** — Identical twin astronauts Scott Kelly (`born 1964`, `340 days` on the ISS, March 2015–March 2016) and Mark Kelly (`born 1964`, Earth baseline), tracked by `10` research teams (*Science*, April 2019) and Weill Cornell PI Christopher Mason: `7%` body-mass loss (`30%` fewer calories), telomere lengthening in orbit and rapid shortening on return, and `91.3%` of gene-expression shifts reverting to baseline within `6 months`.  
2. **Dissolving Bones and Shifting Fluids** — Why removing Earth's `9.82 m/s²` loading causes cephalad fluid shifts (`AQP2` elevation, carotid artery wall thickening, and Spaceflight-Associated Neuro-Ocular Syndrome) and `1%–2%` monthly bone mineral density loss, and how Leigh Gabel's June 2022 `61-micrometer` 3D bone scans of `17 astronauts` (mean age `47 years`) proved that `9 of 17` had incomplete tibial recovery `12 months` after landing (`-3.9%` median bone-strength deficit on missions `>6 months` vs `-0.4%` on `<6 months`).  
3. **Five Hundred and Sixty Million Kilometers of Cosmic Rays** — Midpoint flip (`Wrong.`): how Cary Zeitlin and Donald Hassler used Curiosity's Radiation Assessment Detector (`RAD`) across its `253-day`, `560-million-kilometer` cruise to Mars (launched Nov. 26, 2011, landed Aug. 7, 2012, followed by `~300 days` of surface tracking) to prove that even the shortest round-trip Mars transit delivers `0.66 ± 0.12 sieverts` (`660 mSv`, equal to `>30` full-body CT scans).  
4. **Evolution Across Thirty-Five Generations** — From Charles Darwin (`1809–1882`, 1859 natural selection) and Hermann Joseph Muller (`1890–1967`, 1927 radiation mutagenesis) to Xin Yi and Rasmus Nielsen's July 2010 *Science* study (`50` Tibetan exomes covering `92%` of human genes at `18x` coverage): how a `78%` allele frequency shift in the hypoxia gene *EPAS1* occurred in just a few thousand years, modeling how `35 generations` (`1,000 years`) on Mars (`3.73 m/s²` = `0.380 g`) selects for DNA-repair and fluid-balance variants.  
5. **What Humans Will Actually Become in 1,000 Years** — Why `91.3%` epigenetic reversibility, rotating artificial-gravity habitats, subsurface lava-tube radiation shielding, and gradual *EPAS1*-style selection keep humans in `1,000 years` unmistakably human, handing off to `056` (*Could AI Help Humanity Reach the Stars? How Autonomous Probes Explore Deep Space*).  

---

## 6. Retention plan (whole-video watch)

Design for **watching through**, not just CTR (Growth System v2):

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| 0–0:05 | Curiosity spike | Real graded NASA ISS Cupola / Destiny laboratory frame looking out at Earth's sunlit limb |
| ~0:15 | Stakes | `1%–2%` monthly bone loss (`6 months` in space = `10 years` of Earth aging) and thousands of genes switching on and off across `340 days` |
| ~0:30 | Journey clear | `0.66 Sv` Mars transit dose + `0.380 g` Martian gravity across `35 generations` (`1,000 years`); cold open runs ~0:55 before Chapter 1 card (no full-frame chapter card in first 30s) |
| Chapter starts | Re-hook + chapter card | Each chapter ends on a question answered by the next chapter |
| Mid | Teach while story continues | Orbit spins a centrifuge wheel to restore a porous calcium bone cylinder (Ch 2) and compares Earth's `9.82 m/s²` vs Mars's `3.73 m/s²` gravity bars beside a golden DNA rung in a Martian greenhouse (Ch 4) |
| Final chapter | Payoff + bigger question | Synthesis of `1859–2022–3026` timeline (`340 days`, `91.3%` gene reset, `61 μm` bone scans, `0.66 Sv`, `0.380 g`, `78%` *EPAS1* shift) + hand-off to `056` |
| Outro | Soft return CTA | Hand-off to how autonomous AI probes explore deep space |

- [x] No 30s+ stretch without a new teach or turn  
- [x] Every chapter earns the next one  
- [x] Runtime target **8–12 min** in trust-building window (~8.9 min, 1,318 spoken words)  

---

## 7. Sign-off (block production until checked)

- [ ] Keywords pulled and primary locked  
- [ ] Title ≥90 locked (fearbait / series-suffix clutter rejected)  
- [x] Script reviewer ≥ 90 (**95.6 / 100**, Structure gates 8/8)  
- [x] Outlier patterns mapped into chapter arc  
- [x] Thumb concepts match title promise (one object · one emotion)  
- [x] Chapter teach-points listed (4–6 acts)  
- [x] Cold-open clock (5 / 15 / 30s) written  
- [x] Retention plan filled  
- [x] Production checklist path noted: `templates/PRODUCTION_CHECKLIST_V2.md`  

**Signed off by:**  
**Date:**  

**Only then:** full script → ElevenLabs VO → AI Studio picture (stills first · Veo world · Omni Orbit-only) → edit.
