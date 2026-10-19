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
| ID / slug | `054_Are-We-Living-Inside-A-Simulation-What-Physics-Actually-Says` |
| Working title | Are We Living Inside a Simulation? What Physics Actually Says |
| Date pulled | 2026-10-19 |
| Credits used (approx) | 0 (`v00` script draft only; no VO or picture spend) |
| Brand guardrails | Wonder over fearbait · no conspiracy · Orbit DNA |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) |
| Primary keyword overall | `simulation hypothesis` / `are we living in a simulation` / `quantum physics simulation` |
| Hook promise | One sentence — Every finite computer must chop continuous space and time into discrete steps, and across cosmic-ray grid tests (`10^-27 m`), Fermilab's twin 40-meter Holometer lasers (`10^-18 m`), and the 2017 quantum sign-problem proof (`~300 electrons` exceeding the atoms in the universe), physics shows our cosmos is not running inside a classical computer. |
| Retention design | Chapters that earn the next minute (teach + turn) |
| Packaging | Thumb readable on mobile; one idea (`NO PIXELS FOUND`) |

---

## 2. Keyword research (vidIQ)

Pull GB (or primary market) research for 5–8 terms.

| Keyword | Overall | Est./mo | Comp | Role (title / desc / chapter / Shorts) | Keep? |
|---------|--------:|--------:|-----:|----------------------------------------|-------|
| `are we living in a simulation` | High | High | Med | primary | Yes |
| `simulation hypothesis` | High | High | Med | primary | Yes |
| `simulation theory physics` | High | Med | Low | primary / description | Yes |
| `nick bostrom simulation argument` | Med | Med | Low | chapter | Yes |
| `fermilab holometer` | Med | Low | Low | chapter / Shorts | Yes |
| `planck length pixel universe` | Med | Med | Low | chapter / Shorts | Yes |
| `quantum monte carlo sign problem` | Med | Low | Low | chapter | Yes |

**Decision:** Primary keyword for title lead = `Are We Living Inside a Simulation? What Physics Actually Says`  
**Description first 100 chars must include:** `Are we living inside a simulation, and what do cosmic rays, laser interferometers, and quantum physics actually say?`  

---

## 3. Title ABC (score before VO)

**Growth System v2:** one promise · prefer ≤ ~60 characters · **do not** append `| Orbit's Cosmic Journey` (or similar series suffix). Brand lives in the content.

| | Title | Score | Keep? |
|---|-------|------:|-------|
| A | Are We Living Inside a Simulation? What Physics Actually Says | 95 | **Keep (Lead)** |
| B | Why Quantum Physics Proves We Are Not Inside a Computer Simulation | 94 | Backup |
| C | How Physicists Tested Whether the Universe Has Digital Pixels | 92 | Backup |
| Reject (fearbait / off-brand / series-suffix clutter even if high) | Scientists Just Proved Reality Is Fake \| Orbit's Cosmic Journey | — | **Reject** |

**Proposed title (awaiting Chief topic lock):** Are We Living Inside a Simulation? What Physics Actually Says  
**Why it wins (score + brand + keyword):** Direct hand-off promised in `053`'s subscribe beat (`"whether we are living inside a simulation"`) and closing line (`"whether we are living inside a simulation, and what physics actually says"`), and ranks #1 among unscaffolded backlog topics in the 2026-10-19 weekly audit (`J0678`, Backlog `015`).  

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/054_Are-We-Living-Inside-A-Simulation-What-Physics-Actually-Says/01_Script/simulation_hypothesis_script_master_v00.md
```

- [x] Score ≥ **90 / 100** (**PASS 93.7 / 100**, Structure gates 8/8)  
- Scorecard: `templates/SCRIPT_REVIEW_SCORECARD.md`  
- Reject / rewrite if below threshold  

---

## 4. Outlier / competitive patterns (on-brand only)

Pull outliers for the primary topic (≤80K–mid sub channels preferred, plus 1M+ neighbour proof). Ignore meme/movie noise.

| Outlier / pattern | Views / multiple | Steal (structure) | Do **not** copy |
|-------------------|------------------|-------------------|-----------------|
| Kurzgesagt — *Is Reality Real? The Simulation Argument* | 25M+ | Clear visual breakdown of Bostrom's 3-proposition trilemma and planetary computing scale | Stopping at philosophical brain-in-a-vat arguments without hard experimental physics tests |
| PBS Space Time — *Are We Living in a Simulation? / Testing the Simulation Hypothesis* | 2.4M+ | Connecting Beane, Davoudi & Savage (2012) lattice QCD cosmic-ray anisotropy to testable sky observations | Heavy tensor-notation whiteboard segments |
| Veritasium / Fermilab — *Is the Universe a Hologram? (Fermilab Holometer)* | 3.1M+ | Twin 40-meter Michelson laser interferometers testing Craig Hogan's holographic spacetime jitter down to `10^-18 m` | Talking-head interview format |
| Astrum / Arvin Ash — *Why Quantum Mechanics Makes Simulating the Universe Impossible* | 1.5M+ | Ringel & Kovrizhin (2017 *Science Advances*) `2^N` exponential quantum sign problem where `~300 electrons` exceed the atoms in the observable universe | Long static shot holds |

**Patterns we will use in this script:**

- [x] Assumption-flip / open-loop title  
- [x] Numbered layers or chapter journey  
- [x] Body-scale anchor  
- [x] Slow reveal / delayed answer  
- [x] Experimental physics roadmap  
- [ ] Other:  

---

## 5. Incorporate into the build (required)

Translate data → creative decisions **before** writing the full script:

| Data finding | Change to script / chapters / visuals / packaging |
|--------------|-----------------------------------------------------|
| Primary keyword (`Are We Living Inside a Simulation`, `What Physics Actually Says`) | Title lead + 0:00 spoken question + description first 100 chars |
| High-volume related term (`Planck length`, `Fermilab Holometer`, `Nick Bostrom`, `quantum simulation`) | Cold open pairs Fermilab's `10^-18 m` (`1,000×` smaller than a proton) laser test at `10^-6 s` with the `1.616255 × 10^-35 m` Planck scale (proton inflated to observable universe = human hair width) |
| Winning outlier structure | Hook + 5-chapter physics progression: Nick Bostrom's 2003 trilemma (`10^14–10^17 ops/s` brain vs `10^42 ops/s` planetary computer) → Planck units (`1.616 × 10^-35 m`) & 2012 Beane-Davoudi-Savage cosmic-ray lattice test (`10^-27 m` at `6 × 10^20 eV`) → Dec 3, 2015 Fermilab Holometer (`40 m`, `1 kW`, `10^-18 m`) → Sept 2017 Ringel-Kovrizhin *Science Advances* quantum sign-problem proof (`~300 electrons` > atoms in universe) → Verdict vs Seth Lloyd's `1 kg` (`5 × 10^50 ops/s`, `10^31 bits`) bound |
| Weak competition angle | Most popular videos treat the simulation hypothesis as pure philosophy or stop at Bostrom (2003); we present the three decisive physical tests (2012 cosmic-ray lattice bound, 2015 Fermilab Holometer, 2017 Oxford quantum sign-problem proof) |
| Thumb pattern that works | Deep-space cosmic lattice dissolving under a crisp laser interferometer beam (`NO PIXELS FOUND`, no Orbit) |

**Chapter list after audit** (5 acts, each with a teach-point):

1. **The Trilemma of Nick Bostrom** — Nick Bostrom's (`born 1973`) 2003 *Philosophical Quarterly* paper (first circulated May 2001): `10^14` to `10^17` ops/s per human brain, `10^33` to `10^36` operations for `100 billion` humans across `50-year` lifespans (`30 million` s/yr), `10^42` ops/s planet-sized computer (`< 1 microsecond`), and the 3-part trilemma.  
2. **The Pixel Myth and the Cosmic-Ray Grid** — Why Max Planck's (`1858–1947`) natural length (`1.616255 × 10^-35 m`) does not prove space is a pixel grid, and how Silas Beane, Zohreh Davoudi, and Martin Savage (Oct. 2012 / 2014 *EPJA*) used ultra-high-energy cosmic rays (`~6 × 10^20 eV`) to prove any cubic spacetime lattice must be finer than `10^-12 fm` (`10^-27 m`) because cosmic rays arrive isotropically rather than clustering along cubic axes.  
3. **Twin Lasers in the Illinois Prairie** — Midpoint flip (`Wrong.`): how Aaron Chou's Fermilab Holometer tested Craig Hogan's holographic spacetime jitter using twin co-located `40-meter` (`39 m` optical) interferometers with `1-kilowatt` lasers at megahertz (`10^-6 s`) frequencies down to `10^-18 meters` (`1,000×` smaller than a single proton), ruling out pixel jitter on December 3, 2015.  
4. **The Quantum Wall of Three Hundred Electrons** — From Richard Feynman's (`1918–1988`) 1982 exponential quantum scaling law to Zohar Ringel and Dmitry Kovrizhin's September 2017 *Science Advances* proof: quantized gravitational responses (thermal Hall conductance) trigger an intractable Quantum Monte Carlo sign problem that doubles classical memory per added particle (`2^N`), so storing a few hundred electrons requires more atoms than exist in the observable universe.  
5. **What Physics Actually Says About Reality** — Why even Seth Lloyd's (`born 1960`) ultimate `1-kilogram` computer (`5 × 10^50` ops/s on `~10^31` bits) cannot overcome the `2^N` classical sign wall, uniting the `1982–2017` timeline (`10^-27 m` cosmic rays, `10^-18 m` Holometer, `2^N` sign problem) and handing off to `055` (*What Will Humans Become in 1,000 Years? What Spaceflight Does to the Human Body*).  

---

## 6. Retention plan (whole-video watch)

Design for **watching through**, not just CTR (Growth System v2):

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| 0–0:05 | Curiosity spike | Real graded Fermilab Holometer laser interferometer tunnel frame + deep-space starfield depth |
| ~0:15 | Stakes | Movements lasting `10^-6 s` across `10^-18 m` (`1,000×` smaller than a proton) testing whether space is chopped into digital steps |
| ~0:30 | Journey clear | Proton inflated to observable universe = Planck length (`1.616 × 10^-35 m`) width of a human hair; cold open runs ~0:55 before Chapter 1 card (no full-frame chapter card in first 30s) |
| Chapter starts | Re-hook + chapter card | Each chapter ends on a question answered by the next chapter |
| Mid | Teach while story continues | Orbit rolls a marble across a 3D cubic wire lattice until the grid vanishes into smooth isotropic space (Ch 2) and places electron spheres on a balance scale as server stacks double past the ceiling (Ch 4) |
| Final chapter | Payoff + bigger question | Synthesis of `10^-27 m` cosmic-ray isotropy, `10^-18 m` Holometer smoothness, and `2^N` quantum sign wall vs `10^31`-bit 1 kg limit + hand-off to `055` |
| Outro | Soft return CTA | Hand-off to what spaceflight does to the human body over 1,000 years |

- [x] No 30s+ stretch without a new teach or turn  
- [x] Every chapter earns the next one  
- [x] Runtime target **8–12 min** in trust-building window (~8.6 min)  

---

## 7. Sign-off (block production until checked)

- [ ] Keywords pulled and primary locked  
- [ ] Title ≥90 locked (fearbait / series-suffix clutter rejected)  
- [x] Script reviewer ≥ 90 (**93.7 / 100**, Structure gates 8/8)  
- [x] Outlier patterns mapped into chapter arc  
- [x] Thumb concepts match title promise (one object · one emotion)  
- [x] Chapter teach-points listed (4–6 acts)  
- [x] Cold-open clock (5 / 15 / 30s) written  
- [x] Retention plan filled  
- [x] Production checklist path noted: `templates/PRODUCTION_CHECKLIST_V2.md`  

**Signed off by:**  
**Date:**  

**Only then:** full script → ElevenLabs VO → AI Studio picture (stills first · Veo world · Omni Orbit-only) → edit.
