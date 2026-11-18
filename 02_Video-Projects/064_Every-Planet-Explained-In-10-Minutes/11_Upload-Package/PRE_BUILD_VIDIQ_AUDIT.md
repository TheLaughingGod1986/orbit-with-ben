# Pre-build vidIQ audit — Orbit with Ben (`OWB:064`)

**Hard gate:** Prepared under `J2863` before any script, VO, or picture work. Nothing is built until Ben locks `OWB:064` on the board.  
**Full Go/No-Go & Shelf Audit:** `05_Analytics/owb/EVERY_PLANET_EXPLAINED_GO_NO_GO.md`

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | `064_Every-Planet-Explained-In-10-Minutes` (`OWB:064`) |
| Working title | `Every Planet Explained in 10 Minutes (Mercury to Neptune)` (`57 chars`) |
| Date pulled | `2026-11-14` (`J2863`) |
| Credits used | `£0.00` |
| Brand guardrails | Completeness promise with a number · real NASA/ESA spacecraft imagery · `60–75 s` per planet · Mercury on screen by `0:05` · zero agenda line · not a Shorts compilation (`LEARNINGS.md` Rule 9) |

---

## 1. Keyword & Small-Channel Breakout Evidence (`vidIQ`, 14 Nov 2026)

| Keyword | Search Volume / Mo | Competition | Role | Keep? |
|---------|-------------------:|------------:|------|-------|
| `every planet explained` | `20,191` | `45 / 100` (Medium) | Primary title prefix (`Titles 1, 2, 3`) + first 100 chars of description | **Keep** |
| `space explained` | `129,513` | `46 / 100` (Medium) | Secondary description + tags | **Keep** |
| `every planet in the solar system` | High | Medium | Description + chapter markers (`Mercury to Neptune`) | **Keep** |

**Small-channel breakout proof (`<5,000` subscribers, last 6 months):**
1. *Every Type Of Solar System Explained in 9 Minutes* — **172,800 views** (`1,700` subscribers, `101×` multiple)
2. *Every Star System Closest To Earth Explained in 10 Minutes* — **68,000 views** (`1,700` subscribers)
3. *Every major Solar System object in 5 minutes* — **35,000 views** (`1,100` subscribers, `31×` multiple)
4. *What the Sun Looks Like From Every Planet* — **10,800 views** (`93` subscribers, `116×` multiple)

---

## 2. Neighbour Pass (`≥3` Big Videos `≥1M` Views — Verified `2026-11-15` in `J2875`)

- **YouTube GB Autocomplete (`gl=GB&hl=en-GB`, `2026-11-15`):** `#1: "every planet explained"`, `#2: "every planet explained in 12 minutes"`, `#3: "every dwarf planet explained"`.
- **Two Ranking Videos for `"every planet explained"` (`LEARNINGS.md` Rule 26, `2026-11-15`):**
  1. `lVdYYpoozZU` — *Every Planet From Our Solar System Explained in 20 Minutes* (`Jaydone History`, **888,006 views**, `20:29`, ranks `#1`)
  2. `oytUCOzAYpo` — *Every Planet in the Solar System Explained in 6 Minutes* (`Mr. Ask`, **99,049 views**, `5:49`, ranks `#2`, alongside `#3` `iqJjTeYv5-M` at **3,676,506 views** and `9zaruOUM_0o` *Every Type Of Planet Explained in 12 Minutes* at **181,027 views**)

| # | Views (`2026-11-15` GB read) | Channel (internal only) | Video ID | Title | Words we may reuse |
|---|------:|-------------------------|----------|-------|--------------------|
| 1 | `39,831,294` | National Geographic | `libKVRa01L8` | *Solar System 101 \| National Geographic* | `solar system`, `every planet explained`, `mercury to neptune`, `eight planets`, `gas giants`, `ice giants` |
| 2 | `10,558,560` | BBC Earth Science | `wkQuOrsgVGY` | *Eight Wonders Of Our Solar System \| The Planets \| BBC Earth Science* | `eight planets`, `solar system tour`, `every planet in the solar system`, `mercury`, `venus`, `mars`, `jupiter`, `saturn`, `uranus`, `neptune` |
| 3 | `5,006,819` | Beyond Nature | `lcZTcfdZ3Ow` | *The Planets In Our Solar System* | `planets in our solar system`, `every planet explained`, `real nasa images`, `solar system documentary` |
| 4 | `3,676,506` | Science Channel | `iqJjTeYv5-M` | *Everything You Want to Know About Planets \| How the Universe Works \| Science Channel* | `planets explained`, `how planets work`, `gas giants`, `rocky planets`, `ice giants` |
| 5 | `2,231,803` | What If | `WOgatB4daq8` | *What If You Spent a Day on Every Planet, from 800 °F Mercury to Neptune?* | `every planet`, `mercury to neptune`, `surface conditions on every planet`, `solar system` |

---

## 3. Three Titles (`≤70 Chars`, Starting With Search Phrase) & Three Thumbnails

- **Title 1 (57 chars — Primary):** `Every Planet Explained in 10 Minutes (Mercury to Neptune)`
- **Title 2 (53 chars):** `Every Planet Explained: From Mercury's Ice to Neptune`
- **Title 3 (59 chars):** `Every Planet Explained in 10 Minutes With Real NASA Footage`
- **Thumb A:** `ALL 8 WORLDS` (`8 WORLDS` in `#FFE000`) — All 8 real NASA planetary disks in a diagonal perspective lineup across deep space
- **Thumb B:** `464°C TO -224°C` (`464°C` in `#FFE000`) — Rule 14 bright high-contrast split: golden-orange `464 °C` Venus/Mercury vs electric ice-blue `-224 °C` Uranus/Neptune
- **Thumb C:** `REAL NASA PHOTOS` (`REAL` in `#FFE000`) — Rules 18 & 19 colour-graded NASA Cassini/Juno/Voyager spacecraft montage with Earth scale

---

## 4. Script Reviewer & 8-Planet Chapter Plan (`J3020`, 18 Nov 2026)

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/01_Script/every_planet_explained_script_master_v01.md
```

- [x] Score ≥ **90 / 100** (**PASS 93.1 / 100**, 1,290 spoken words / 8,161 spoken characters / 1,352 reviewer words, 8 planet sections / 7 `[CHAPTER CARD]` markers)
- **8-planet section breakdown (`~64–77 s` per planet):**
  1. **Mercury (Cold Open):** `147 spoken words` (`939 chars`, `~65.3 s`) — 58M km, 430 °C day vs −180 °C night, Giuseppe Colombo (1965) 3:2 resonance (176-Earth-day solar day), 2,440 km radius with 85% metallic core, MESSENGER (2011–2015) water ice in 112-km Prokofiev crater
  2. **Venus (`Venus — The Backwards Furnace`):** `152 spoken words` (`925 chars`, `~67.6 s`) — 108M km, 464 °C under 96.5% CO₂ and 92 bars (930 m underwater on Earth), 243-day retrograde spin vs 225-day year, Pioneer Venus (1978) 100× D/H, Venera 13 (1 Mar 1982) 127-min survival, Parker Solar Probe (Feb 2021) nightside glow
  3. **Earth (`Earth — The Shielded Ocean World`):** `145 spoken words` (`921 chars`, `~64.4 s`) — 150M km (1 AU), 6,378 km radius, 23.4° tilt, 1,670 km/h equatorial spin (>4× 408 km/h wind record) & 43 km bulge, 3,000 km liquid-iron outer core (183 reversals in 83M yr, last 780,000 yr ago), Carl Friedrich Gauss (1830s, ~9% drop), atmosphere shielding like 13 feet of concrete
  4. **Mars (`Mars — The Frozen Robot Desert`):** `162 spoken words` (`986 chars`, `~72.0 s`) — 228M km (1.5 AU), 3,390 km radius, 6.36 mbar air (<1% Earth) at −59 °C, Curiosity (Aug 2012) 0.64 mSv/day radiation (~3 months of Earth yearly background per day), Olympus Mons 21.3 km MOLA elevation (>2× Everest across an Arizona-sized base), Opportunity 5,111 sols (10 Jun 2018), Ingenuity 72 flights (18 Jan 2024)
  5. **Jupiter (`Jupiter — The Ocean of Metallic Hydrogen`):** `174 spoken words` (`1,113 chars`, `~77.3 s`) — 778M km (5.2 AU), 318 Earth masses (>2× all other planets), 69,911 km radius (11× Earth, basketball vs grape), 9.9-h day, Galileo Galilei (1610), Great Red Spot shrinking from 41,000 km (late 1800s) to 16,500 km (2014), midpoint twist ("Case closed? Wrong — there is no solid surface"), Galileo probe (7 Dec 1995) 58-min / 153-km / 22.7-atm descent, Juno (2016) dilute core
  6. **Saturn (`Saturn — Disappearing Rings and the Hexagon Storm`):** `166 spoken words` (`1,031 chars`, `~73.8 s`) — 1.4B km (9.5 AU), 120,500 km diameter (9× Earth, volleyball vs nickel), 10.7-h day, 687 kg/m³ density (< water), 282,000 km rings only 10 m thick, Cassini 6 dives before Sep 2017 (0.41 Mimas mass, 10–100 Myr age), 30,000 km north-pole hexagon (322 km/h jet, >2 Earths wide) and 2,000 km central eye (330 mph clouds, 27 Nov 2012), 2012-to-2016 blue-to-gold seasonal shift
  7. **Uranus (`Uranus — Knocked Sideways Into 21-Year Winters`):** `156 spoken words` (`1,006 chars`, `~69.3 s`) — 2.9B km (19 AU), William Herschel (13 Mar 1781, first telescope planet), 51,118 km diameter (4× Earth, softball vs nickel), 84-yr orbit, 97.77° tilt (>4× Earth's 23.4° tilt), 17-h retrograde spin, 21-yr winter, Voyager 2 (24 Jan 1986), −224.2 °C (49 K) coldest planetary atmosphere, ~60° magnetic tilt, ≥80% hot fluid interior reaching 4,982 °C
  8. **Neptune (`Neptune — Supersonic Winds at the Edge`):** `173 spoken words` (`1,157 chars`, `~76.9 s`) — 4.5B km (30 AU, sunlight 900× dimmer), 49,528 km diameter (4× Earth, baseball vs nickel), 16-h day, 165-yr orbit (completed first orbit in 2011), Urbain Le Verrier & Johann Gottfried Galle (23 Sep 1846, first planet found by maths), William Lassell (10 Oct 1846, Triton), Voyager 2 (25 Aug 1989) >2,000 km/h methane winds (3× Jupiter, 9× Earth's 400 km/h winds), Triton >8 km nitrogen geysers, hand-off to `034` Pluto (New Horizons 1,000 km nitrogen-ice heart with zero craters)

---

## 5. Sign-off (Pre-build audit & automated script gate)

- [x] Keywords pulled and primary locked (`every planet explained`, `20,191/mo`, `45/100` comp)
- [x] Title ≥90 locked by Ben in `J3011` (`"Lock it."`, 17 Nov 2026: `Every Planet Explained in 10 Minutes (Mercury to Neptune)`)
- [x] Script reviewer ≥ 90 (`PASS 93.1 / 100` on `every_planet_explained_script_master_v01.md`)
- [x] Outlier patterns and 8-planet chapter teach-points mapped into script
- [x] Thumb concepts match title promise (`ALL 8 WORLDS`, `464°C TO -224°C`, `REAL NASA PHOTOS`)
- [x] Cold-open clock (Mercury on screen at Frame 0, question before 0:08, −180 °C payoff hint before 0:20, zero agenda line) written
- [x] Production checklist path noted: `11_Upload-Package/PRODUCTION_CHECKLIST_V2.md`

**Signed off by:** Ben (`J3011` topic lock, 17 Nov 2026) · Gemini (`gemini`, `J3020` pre-build & `review:script` `PASS 93.1/100`; final script lock & `CLAUDE_QUOTE_CHECK` pending reviewer/Chief before VO)  
**Date:** 2026-11-18

