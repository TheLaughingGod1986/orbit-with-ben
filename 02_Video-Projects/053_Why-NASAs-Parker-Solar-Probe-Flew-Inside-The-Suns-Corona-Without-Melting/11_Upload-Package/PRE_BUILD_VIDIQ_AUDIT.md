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
| ID / slug | `053_Why-NASAs-Parker-Solar-Probe-Flew-Inside-The-Suns-Corona-Without-Melting` |
| Working title | Why NASA's Parker Solar Probe Flew Inside the Sun's Corona without Melting |
| Date pulled | 2026-10-19 |
| Credits used (approx) | 0 (`v01` script draft only; no VO or picture spend) |
| Brand guardrails | Wonder over fearbait · no conspiracy · Orbit DNA |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) |
| Primary keyword overall | `parker solar probe` / `why parker solar probe doesn't melt` / `sun corona` |
| Hook promise | One sentence — NASA's Parker Solar Probe survives flying at 430,000 mph within 3.8 million miles of the Sun inside a several-million-degree corona because low particle density transfers relatively little heat, and a 4.5-inch carbon-foam shield keeps the spacecraft bus in an 85°F shadow. |
| Retention design | Chapters that earn the next minute (teach + turn) |
| Packaging | Thumb readable on mobile; one idea (`2,500°F SHIELD`) |

---

## 2. Keyword research (vidIQ)

Pull GB (or primary market) research for 5–8 terms.

| Keyword | Overall | Est./mo | Comp | Role (title / desc / chapter / Shorts) | Keep? |
|---------|--------:|--------:|-----:|----------------------------------------|-------|
| `parker solar probe` | High | High | Med | primary | Yes |
| `why parker solar probe doesn't melt` | High | High | Low | primary | Yes |
| `sun corona` | High | High | Med | primary / chapter | Yes |
| `touching the sun` | High | High | Med | secondary / Shorts | Yes |
| `parker solar probe speed` | High | Med | Low | chapter / Shorts | Yes |
| `alfven critical surface` | Med | Low | Low | chapter | Yes |
| `solar wind switchbacks` | Med | Low | Low | chapter | Yes |

**Decision:** Primary keyword for title lead = `Why NASA's Parker Solar Probe Flew Inside the Sun's Corona without Melting`  
**Description first 100 chars must include:** `Why did NASA's Parker Solar Probe fly inside the Sun's million-degree corona at 430,000 mph without melting?`  

---

## 3. Title ABC (score before VO)

**Growth System v2:** one promise · prefer ≤ ~60 characters · **do not** append `| Orbit's Cosmic Journey` (or similar series suffix). Brand lives in the content.

| | Title | Score | Keep? |
|---|-------|------:|-------|
| A | Why NASA's Parker Solar Probe Flew Inside the Sun's Corona without Melting | 95 | **Keep (Lead)** |
| B | How a 4.5-Inch Heat Shield Survived the Sun's Million-Degree Corona | 94 | Backup |
| C | Why NASA's Fastest Spacecraft Didn't Melt When It Touched the Sun | 93 | Backup |
| Reject (fearbait / off-brand / series-suffix clutter even if high) | Did NASA's Sun Probe Just Burn Up Inside the Corona? \| Orbit's Cosmic Journey | — | **Reject** |

**Locked title:** Why NASA's Parker Solar Probe Flew Inside the Sun's Corona without Melting  
**Why it wins (score + brand + keyword):** Direct hand-off promised in `052`'s subscribe beat (`"how NASA's Parker Solar Probe touched the Sun"`) and closing line (`"why NASA's Parker Solar Probe flew straight inside the Sun's million-degree corona without melting"`), pairs the mission name (`NASA's Parker Solar Probe`) with the physical paradox (`Flew Inside the Sun's Corona without Melting`).  

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/053_Why-NASAs-Parker-Solar-Probe-Flew-Inside-The-Suns-Corona-Without-Melting/01_Script/parker_solar_probe_script_master_v01.md
```

- [x] Score ≥ **90 / 100** (**PASS 95.8 / 100**)  
- Scorecard: `templates/SCRIPT_REVIEW_SCORECARD.md`  
- Reject / rewrite if below threshold  

---

## 4. Outlier / competitive patterns (on-brand only)

Pull outliers for the primary topic (≤80K–mid sub channels preferred). Ignore meme/movie noise.

| Outlier / pattern | Views / multiple | Steal (structure) | Do **not** copy |
|-------------------|------------------|-------------------|-----------------|
| Veritasium / Real Engineering — *How NASA's Parker Solar Probe Touched the Sun Without Melting* | 3.2M+ | Temperature vs heat oven/water analogy + TPS carbon-foam cutaway | Talking-head presenter segments |
| Smarter Every Day / NASA Goddard — *Parker Solar Probe Heat Shield & Solar Probe Cup Engineering* | 2.1M+ | Tungsten/TZM Faraday cup + 1-gallon deionized water cooling loop | Long unscripted interview stretches |
| SciShow Space — *Parker Solar Probe Enters the Solar Corona (Alfvén Critical Surface)* | 1.1M+ | Alfvén critical surface at 18.8 solar radii + magnetic switchback funnels | Studio host on camera |
| Astrum — *What Parker Solar Probe Saw Inside the Sun's Atmosphere* | 1.4M+ | WISPR coronal streamer imagery + Venus gravity-assist ladder | 10-second static shot holds |

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
| Primary keyword (`Parker Solar Probe`, `Sun's Corona`, `without Melting`) | Title lead + 0:00 spoken question + description first 100 chars |
| High-volume related term (`430,000 mph`, `heat shield`, `touching the Sun`) | Cold open pairs 3.8M-mile perihelion (4 inches on a 1-yard Earth–Sun stick) and 430,000 mph speed with the 4.5-inch carbon-foam TPS keeping the spacecraft bus at 85°F |
| Winning outlier structure | Hook + 6-chapter engineering & physics journey: 1950s Eugene Parker solar wind & 7 Venus flybys → temperature vs heat in the corona → 4.5-in / 160-lb TPS carbon foam → 6,192°F tungsten Solar Probe Cup → 1-gallon water loop & 7 sun sensors across 8-min light delay → Apr. 28, 2021 Alfvén surface, magnetic switchbacks & Sept. 4, 2026 Encounter 29 / 2029 extension |
| Weak competition angle | Older videos stop at the 2018 launch or 2021 first coronal crossing; we include the Dec. 24, 2024 record 3.8M-mile / 430,000-mph pass, the June 19, 2025 24th baseline orbit, the Sept. 4, 2026 29th close approach (~1,700°F shield, zero degradation), and the 2026 Heliophysics Senior Review extension into 2029 |
| Thumb pattern that works | NASA/JHUAPL Parker Solar Probe behind its glowing 8-foot white ceramic heat shield against a coronal streamer (`2,500°F SHIELD`, no Orbit) |

**Chapter list after audit** (6 acts, each with a teach-point):

1. **The Sixty-Year Question and Seven Venus Slingshots** — Eugene Parker's (`1927–2022`) mid-1950s solar wind prediction, Oct. 3, 2017 visit, Aug. 12, 2018 Delta IV-Heavy launch (`1,510 lb`), and 7 Venus gravity assists shrinking perihelion from `93 million miles` (`1 AU`) to `3.8 million miles` (`475×` Earth solar intensity).  
2. **Temperature Versus Heat Inside the Corona** — Why the million-degree corona doesn't vaporize the spacecraft (`Wrong.`): temperature (particle speed) vs heat (total energy transfer in ultra-thin plasma), 400°F oven vs 212°F boiling water analogy, and `2,500°F` (`1,377°C`) design / `~1,700°F` actual shield temperature vs `1,300–2,200°F` volcanic lava.  
3. **Four and a Half Inches of Carbon Foam** — How Betsy Congdon's (`JHU APL`) `8-foot` (`2.4 m`), `4.5-inch` (`11.43 cm`), `160-pound` (`73 kg`) Thermal Protection System uses `97% air` carbon foam between carbon-carbon plates and white ceramic alumina paint (`tested to 3,000°F / 1,650°C`) to hold the spacecraft bus at `85°F` (`30°C`).  
4. **The Tungsten Cup That Looks Around the Shield** — How Justin Kasper's (`SWEAP`) `Solar Probe Cup` peers out from behind the shield using a `4,260°F` (`2,349°C`) Titanium-Zirconium-Molybdenum cup, acid-etched `6,192°F` (`3,422°C`) tungsten grids, sapphire crystal tubes, and niobium wires tested in the `10,000-mirror` Odeillo Solar Furnace.  
5. **One Gallon of Water and Seven Sun Sensors** — How two `17.2 sq ft` retractable solar wings (`388 watts`, a kitchen blender) stay cool with `1 gallon` (`3.7 L`) of deionized water (`50–257°F`, living-room cooling power) while cell-phone-sized limb sensors autonomously steer the probe across the `8-minute` radio delay.  
6. **Crossing the Alfvén Surface and the Magnetic Switchbacks** — Crossing Hannes Alfvén's (`1908–1995`) critical surface at `18.8 solar radii` (`8.127 million miles`) on April 28, 2021, tracing magnetic `switchbacks` with Stuart Bale's (`UC Berkeley`) team to helium-rich supergranule funnels, and completing the `24th` (June 19, 2025) and `29th close approach` on Sept. 4, 2026 (`40%` of solar circumference in 1 day, zero shield degradation, extended into `2029`).  

---

## 6. Retention plan (whole-video watch)

Design for **watching through**, not just CTR (Growth System v2):

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| 0–0:05 | Curiosity spike | NASA/JHUAPL Parker Solar Probe behind its 8-foot heat shield + WISPR coronal streamer imagery |
| ~0:15 | Stakes | 3.8 million miles (4 inches on a 1-yard Earth–Sun stick), 430,000 mph, million-degree corona vs 2,500°F shield vs 85°F spacecraft bus |
| ~0:30 | Journey clear | 475× Earth solar intensity + Eugene Parker's 1950s solar wind prediction & Aug. 12, 2018 launch; cold open runs ~0:55 before Chapter 1 card (no full-frame chapter card in first 30s) |
| Chapter starts | Re-hook + chapter card | Each chapter ends on a question answered by the next chapter |
| Mid | Teach while story continues | Orbit tucks inside the 85°F shadow cone behind the 8-foot heat shield (Ch 2) and peers around the bevelled rim at the glowing red tungsten grids of the Solar Probe Cup (Ch 4) |
| Final chapter | Payoff + bigger question | Alfvén surface crossing + magnetic switchbacks + Sept. 4, 2026 Encounter 29 / 2029 extension + hand-off to `054` (Are We Living Inside a Simulation?) |
| Outro | Soft return CTA | Hand-off to whether we are living inside a simulation |

- [x] No 30s+ stretch without a new teach or turn  
- [x] Every chapter earns the next one  
- [x] Runtime target **8–12 min** in trust-building window (~8.9 min)  

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
