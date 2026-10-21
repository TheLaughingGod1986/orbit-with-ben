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
| ID / slug | `059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons` |
| Working title | Why Mars Built a Volcano Three Times Taller Than Mount Everest — Olympus Mons |
| Date pulled | 2026-10-21 (`J0757`) |
| Credits used (approx) | 0 (`v00` script draft + 16-row `SOURCES.md` verification only; no VO or picture spend) |
| Brand guardrails | Wonder over fearbait · no fake alien clickbait · Orbit DNA |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) |
| Primary keyword overall | `olympus mons mars volcano` / `largest volcano in the solar system` / `olympus mons vs mount everest` |
| Hook promise | One sentence — Because Mars lacks Earth's moving tectonic plates and pulls with just `38 percent` (`3.73 m/s²`) of Earth's surface gravity, a stationary `70-kilometer-thick` crust sat over a single mantle hotspot until basaltic lava piled into `Olympus Mons` — a `21.287-kilometer` (`27-kilometer` relief) shield volcano `600 kilometers` wide (`300,000 km²`, the size of Arizona or Italy) with an `8-kilometer` cliff scarp, a `72-pascal` summit, and lava flows as young as `2 million years`. |
| Retention design | Chapters that earn the next minute (teach + turn) |
| Packaging | Thumb readable on mobile; one idea (`3X MOUNT EVEREST`) |

---

## 2. Keyword research (vidIQ)

Pull GB (or primary market) research for 5–8 terms.

| Keyword | Overall | Est./mo | Comp | Role (title / desc / chapter / Shorts) | Keep? |
|---------|--------:|--------:|-----:|----------------------------------------|-------|
| `olympus mons` | High | High | Low | primary / title | Yes |
| `largest volcano in the solar system` | High | High | Low | primary / description | Yes |
| `olympus mons vs mount everest` | High | Med | Low | primary / title | Yes |
| `mars volcano olympus mons` | High | Med | Low | primary / description | Yes |
| `why is olympus mons so big` | High | Med | Low | cold open / chapter 2 | Yes |
| `is olympus mons still active` | Med | Med | Low | chapter 4 / Shorts | Yes |
| `tharsis volcanoes mars` | Med | Low | Low | chapter 2 / description | Yes |

**Decision:** Primary keyword for title lead = `Why Mars Built a Volcano Three Times Taller Than Mount Everest — Olympus Mons`  
**Description first 100 chars must include:** `Why did Mars build Olympus Mons — a volcano nearly three times taller than Mount Everest and wider than Arizona?`  

---

## 3. Title ABC (score before VO)

**Growth System v2:** one promise · prefer ≤ ~60 characters · **do not** append `| Orbit's Cosmic Journey` (or similar series suffix). Brand lives in the content.

| | Title | Score | Keep? |
|---|-------|------:|-------|
| A | Why Mars Built a Volcano Three Times Taller Than Mount Everest — Olympus Mons | 96 | **Keep (Lead)** |
| B | Why Olympus Mons on Mars Is Three Times Taller Than Mount Everest | 95 | Backup |
| C | How Mars Built the Largest Volcano in the Solar System — Olympus Mons | 93 | Backup |
| Reject (fearbait / off-brand / series-suffix clutter even if high) | Mars's Giant Volcano Is About to Erupt \| Orbit's Cosmic Journey | — | **Reject** |

**Proposed title (awaiting Chief topic lock):** Why Mars Built a Volcano Three Times Taller Than Mount Everest — Olympus Mons  
**Why it wins (score + brand + keyword):** Direct hand-off promised in `058`'s subscribe beat (`"why Mars built a giant volcano"`) and closing line (`"why Mars built a volcano three times taller than Mount Everest, Olympus Mons"`), and #1 among unscaffolded candidates in the 2026-10-20 weekly audit (`J0752`).  

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons/01_Script/olympus_mons_script_master_v00.md
```

- [x] Score ≥ **90 / 100** (**PASS 95.8 / 100**, Structure gates 8/8, `1,349` spoken words / `1,369` reviewer words, ~`9.1 min`)  
- Scorecard: `templates/SCRIPT_REVIEW_SCORECARD.md`  
- Reject / rewrite if below threshold  

---

## 4. Outlier / competitive patterns (on-brand only)

Pull outliers for the primary topic (≤80K–mid sub channels preferred, plus 1M+ neighbour proof). Ignore meme/movie noise.

| Outlier / pattern | Views / multiple | Steal (structure) | Do **not** copy |
|-------------------|------------------|-------------------|-----------------|
| Astrum — *Olympus Mons & Valles Marineris: The Megastructures of Mars* | 1.5M+ | Physical scale comparisons (`21.287 km` MOLA / `27 km` relief vs Everest's `8,848 m` and Mauna Loa's `9 km`; `600 km` Arizona/Italy footprint; `8 km` perimeter cliff scarp) | Long static shot holds |
| SciShow Space / Kurzgesagt — *Why Mars Has the Largest Volcano in the Solar System* | 1.2M–4M+ | Clear tectonic mechanism: Earth's moving plates (`Hawaii` chain) vs Mars's stationary `70 km` lithosphere under `0.38 g` gravity | Cartoon comedy tone |
| ESA Mars Express / National Geographic — *Mars Volcanoes & Hidden Glaciers* | 1.2M–3M+ | Midpoint twist (`Wrong.`): `Mars Express HRSC` (`10–20 m/pixel`) discovery of `2-million-year-old` lava flows and `4-million-year-old` dust-covered rock glaciers at the scarp base | Dry textbook narration |

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
| Primary keyword (`Why Mars Built a Volcano Three Times Taller Than Mount Everest — Olympus Mons`) | Title lead + 0:00 spoken question + description first 100 chars |
| High-volume related term (`Olympus Mons`, `Mount Everest`, `Mauna Loa`, `Mariner 9`, `MOLA`, `Mars Express`) | Cold open compares `Olympus Mons` (`21.287 km` MOLA / `26–27 km` relief, `600 km` wide, `300,000 km²`, `8 km` scarp, `72 Pa` summit) with `Mount Everest` (`8,848 m`) and `Mauna Loa` (`9 km`) |
| Winning outlier structure | Hook + 5-chapter escalation: `Schiaparelli` (`1835–1910`) `Nix Olympica` dust-storm sightings (`Moore` `1923–2012`), `Mariner 9` (`1971`) reveal, & `Sjogren` (`1979` *Science*) `8.7 × 10²¹ g` `600 km` gravity disk → `MGS` MOLA & gravity (`Smith 1937`, `Zuber 1958`, `Solomon 1945`, `Phillips 1940–2020`, *Science* `1999–2001`): `0.38 g` gravity, `70 km` stationary lithosphere, `3 × 10⁸ km³` Tharsis magma, `6–8 km` scarp & `750 km` aureole → Summit experience (`5%` slope, `3 km` horizon, `60 × 80 km` / `3.2 km` six-caldera depression over `32 km` magma chamber, `72 Pa` pressure vs `32,000 Pa` Everest) → Midpoint flip (`Wrong.`) on `Neukum` (`1944–2014`) & `Head` (`born 1941`) `2004–2005` *Nature* `Mars Express HRSC` (`2 Mya` lava flows & `4 Mya` rock glaciers) → Synthesis & hand-off to `060` (`Hyperion`) |
| Weak competition angle | Most videos state "Olympus Mons is 3x Everest" without the exact `Science` / `Nature` measurements (`21.287 km` MOLA vs `26–27 km` Amazonis relief, `8.7 × 10²¹ g` disk, `3 × 10⁸ km³` Tharsis magma, `72 Pa` summit pressure, `2 Mya` lava & `4 Mya` glaciers) |
| Thumb pattern that works | Towering rusty shield and `8 km` cliff scarp of Olympus Mons dwarfing Mount Everest with bold top-band hook `3X MOUNT EVEREST` (no Orbit on thumb) |

**Chapter list after audit** (5 acts, each with a teach-point):

1. **The Snow Patch That Survived a Global Dust Storm** — How `Giovanni Virginio Schiaparelli` (`1835–1910`) spotted `Nix Olympica` above Martian dust storms (noted by `Patrick Moore`, `1923–2012`), how `Mariner 9` (`1971`) revealed a `27 km` high, `600 km` wide volcano across `300,000 km²`, and how `William L. Sjogren` (*Science*, `March 9, 1979`) weighed its `8.7 × 10²¹ g` disk with `Viking Orbiter 2`.  
2. **Why a Stationary Crust and 38 Percent Gravity Built a Giant** — How `David E. Smith` (`born 1937`), `Maria T. Zuber` (`born 1958`), `Sean C. Solomon` (`born 1945`), and `Roger J. Phillips` (`1940–2020`) (*Science*, `1999–2001`) mapped Mars's `70 km` stationary lithosphere, `3 × 10⁸ km³` Tharsis magmas, `2 km` crustal moat, `6–8 km` `Olympus Rupes` scarp, and `750 km` `Lycus Sulci` aureole under `3.73 m/s²` (`38%` Earth) gravity.  
3. **The Invisible Summit and Its 72-Pascal Near-Vacuum** — Why the `5%` flank slope hides the peak behind a `3 km` horizon while the `21.287 km` summit holds six nested calderas (`60 × 80 km`, `3.2 km` deep above a `32 km` magma chamber, `350–150 Mya`) at `72 pascals` (`12%` of Mars's `600 Pa` average vs `32,000 Pa` on Everest).  
4. **2-Million-Year-Old Lava and Hidden Tropical Glaciers** — Midpoint flip (`Wrong.`): how `Gerhard Neukum` (`1944–2014`) and `James W. Head` (`born 1941`) (*Nature*, `Dec. 23, 2004` & `Mar. 17, 2005`) used `Mars Express HRSC` (`10–20 m/pixel`) to find `115–2 Mya` lava flows and `4 Mya` dust-insulated rock glaciers at the scarp base.  
5. **How a One-Plate Planet Built the Solar System's Greatest Peak** — Synthesis across the `1835–2005` discovery timeline showing how gravity and a one-plate crust sculpted the solar system's tallest volcano, handing off to `060` (*Why Saturn's Moon Hyperion Looks Like a Giant Tumbling Space Sponge*).  

---

## 6. Retention plan (whole-video watch)

Design for **watching through**, not just CTR (Growth System v2):

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| 0–0:05 | Curiosity spike | Real graded NASA Viking/MGS mosaic of `Olympus Mons` (`PIA00300`) and summit caldera (`PIA25476`) + `21.287 km` (`27 km` relief) vs `8,848 m` Everest scale |
| ~0:15 | Stakes | Why a planet half Earth's width built a `600 km` Arizona-sized volcano with an `8 km` cliff scarp and `72 Pa` summit |
| ~0:30 | Journey clear | Standing below the `8 km` perimeter cliff scarp or looking into the `60 × 80 km` caldera; cold open runs ~0:55 before Chapter 1 card |
| Chapter starts | Re-hook + chapter card | Each chapter ends on a question answered by the next chapter |
| Mid | Teach while story continues | Orbit projects the `8 km` `Olympus Rupes` cliff scarp and `2 km` moat against Everest (Ch 2) and glides over the `4 Mya` scarp-base rock glaciers revealing buried water ice (Ch 4) |
| Final chapter | Payoff + bigger question | Complete `1835–2005` Olympus Mons timeline (`21.287 km` / `27 km` height, `600 km` / `300,000 km²` base, `8.7 × 10²¹ g`, `70 km` crust, `72 Pa`, `2 Mya` lava) + hand-off to `060` |
| Outro | Soft return CTA | Hand-off to Saturn's sponge-like moon Hyperion (`060`) |

- [x] No 30s+ stretch without a new teach or turn  
- [x] Every chapter earns the next one  
- [x] Runtime target **8–12 min** in trust-building window (~9.1 min, 1,349 spoken words / 1,369 reviewer words)  

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
