# Pre-build vidIQ audit — Orbit with Ben

**Hard gate:** Run **before** locking script, VO, prompts, or picture gen for any new long.  
**Goal:** Every episode is aimed at **views + full-video watch** using live data — not gut feel alone.  
**Also follow:** `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` and `FAMILIAR_DANGER_STRATEGY.md`.  

Copy into each project as:

`02_Video-Projects/NNN_Slug/11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | `033_Why-This-Planet-Has-21-Year-Winters` |
| Working title | `Why Knocked-Sideways Uranus Has 21-Year Winters` (47 chars, LEARNINGS rule 15) |
| Rule-18 real-imagery titles | `What Voyager 2 Saw in Just 6 Hours at Uranus` (44 chars) · `The Only Spacecraft Photos Ever Taken at Uranus` (47 chars) |
| Series (LEARNINGS rule 20) | `Real Worlds` |
| Date pulled | 4 Nov 2026, ~22:38 UTC (`yt-dlp` public search + `05_Analytics/owb/snapshots/2026-11-04.json`). Job J2148. |
| Credits used (approx) | 0 (no vidIQ; no spend) |
| Brand guardrails | Wonder over fearbait · no conspiracy · Orbit DNA |
| Neighbour pass | **Strong.** Ten education or space videos at 1.24M–7.63M views on Uranus, its sideways tilt, Voyager 2, and Miranda. Full table: `TOPIC_OPPORTUNITY_SCORE.md`. |
| Short proof | OWB Short `ZpEA8stoSPA` (*Why Does Uranus Have 21-Year Winters?*, public 3 Nov 2026) reached **461 views and 6 likes in day 1** (2.3× the 200-view benchmark). |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) |
| Primary keyword overall | Uranus / why is Uranus on its side / Voyager 2 Uranus |
| Hook promise | One sentence — 21-year polar winter on a planet tipped at 97.77° |
| Retention design | 6 chapters that earn the next minute (teach + midpoint turn at Ch 4) |
| Packaging | 3 distinct thumbnail concepts (Rule 12, 14, 19); readable at 168×94 |

---

## 2. Keyword research (public neighbour + channel analytics)

| Keyword | Overall | Est./mo | Comp | Role (title / desc / chapter / Shorts) | Keep? |
|---------|--------:|--------:|-----:|----------------------------------------|-------|
| Uranus | — | — | — | primary | Yes |
| why is Uranus on its side | — | — | — | primary / hook | Yes |
| Uranus 21-year winter | — | — | — | title / Short `ZpEA8stoSPA` (461 views d1) | Yes |
| Voyager 2 Uranus | — | — | — | Rule-18 title / Ch 3 | Yes |
| Miranda moon cliff | — | — | — | Ch 6 payoff | Yes |

**Decision:** Primary keyword for title lead = Uranus (subject word from the neighbour titles and our 461-view Short `ZpEA8stoSPA`)  
**Description first 100 chars must include:** Uranus, 21-year winters, knocked onto its side

Draft first line (no channel names): Why does Uranus have 21-year winters, and what did Voyager 2 find when it flew past a planet knocked onto its side?

**Tags (subject only):** uranus · why is uranus on its side · uranus 21 year winter · voyager 2 uranus · ice giant · miranda moon · william herschel · uranus rings

---

## 2b. Neighbour pass (J2148, 4 Nov 2026)

Channel names below are internal notes. They never go in the title, description or tags. Views via `yt-dlp`, 4 Nov 2026, ~22:38 UTC. Full table: `TOPIC_OPPORTUNITY_SCORE.md`.

| Views | Id | Title (channel, internal) |
|------:|----|---------------------------|
| 7.63M | `rHLifi-VzSQ` | Falling Into Uranus (Simulation) (Stargaze) |
| 2.89M | `Nru_XeafheY` | What If You Spent 5 Seconds on Uranus? (What If) |
| 2.63M | `ckdJ4945dHs` | Uranus is officially the weirdest planet in our solar system (Insider Tech) |
| 2.57M | `tCmC0XOKO5Q` | The Bizarre Characteristics Of Uranus \| Our Solar System's Planets (Astrum) |
| 2.12M | `1hIwD17Crko` | Uranus & Neptune: Crash Course Astronomy #19 (CrashCourse) |
| 1.96M | `UOUM1QT5GgU` | Voyager 2 Found Something Impossible at the Edge of Space (The Infographics Show) |
| 1.93M | `q7HMd2FyFqk` | Why is Uranus On Its Side? \| The Planets \| BBC Earth Science (BBC Earth Science) |
| 1.87M | `WJ1KJhC0SOo` | What Would You See If You Fell Into Uranus? (4K UHD) (V101 SPACE) |
| 1.45M | `wKcMvR2C0oA` | Is Uranus Actually a Rock Giant? (Astrum) |
| 1.24M | `pZh5BWCNmmE` | Uranus: The Weirdest Planet in the Solar System (Astrum, 2026-10-27 — 1.24M in 8 days) |

---

## 3. Title ABC (LEARNINGS Rules 15 & 18 — ≤ 50 chars)

| | Title | Chars | Rule | Keep? |
|---|-------|------:|------|-------|
| A | `Why Knocked-Sideways Uranus Has 21-Year Winters` | 47 | Rule 15 scenario/stakes | **Yes** |
| B | `What Voyager 2 Saw in Just 6 Hours at Uranus` | 44 | Rule 18 real-imagery | **Yes** |
| C | `The Only Spacecraft Photos Ever Taken at Uranus` | 47 | Rule 18 real-imagery (backed by `SOURCES.md` row 8) | **Yes** |
| Reject | `What Happened to Uranus? \| Orbit's Cosmic Journey` | 50 | Vague "What happened to X?" + series suffix | **Reject** |

**Locked title:** `Why Knocked-Sideways Uranus Has 21-Year Winters` (with Rule-18 variant `What Voyager 2 Saw in Just 6 Hours at Uranus` for Studio A/B)  
**Why it wins (score + brand + keyword):** Names the subject (`Uranus`), concrete cause (`Knocked-Sideways`), and concrete number/stakes (`21-Year Winters`) in 47 characters (≤ 50), matching our 461-view Short `ZpEA8stoSPA`.

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/01_Script/uranus_21_year_winter_script_master_v02.md
```

- [x] Score ≥ **90 / 100** (**PASS 95.2 / 100**, 1,290 spoken words / 1,347 reviewer words, 6 chapters)  
- Scorecard: `templates/SCRIPT_REVIEW_SCORECARD.md`  

---

## 4. Outlier / competitive patterns (on-brand only)

| Outlier / pattern | Views / multiple | Steal (structure) | Do **not** copy |
|-------------------|------------------|-------------------|-----------------|
| `pZh5BWCNmmE` (Astrum, 27 Oct 2026) | 1.24M in 8 days | Real Voyager 2 + Hubble/Webb plates, seasonal & magnetic paradoxes | 40-min slow holds |
| `q7HMd2FyFqk` (BBC Earth Science) | 1.93M | Clear geometric explanation of the 97.77° tilt and 1977 ring occultation | TV presenter cutaways |

**Patterns we will use in this script:**

- [x] Assumption-flip / open-loop title  
- [x] Numbered layers or chapter journey (6 acts)  
- [x] Body-scale anchor (nickel vs softball, 21-year night, 10-minute cliff fall)  
- [x] Slow reveal / delayed answer (midpoint twist at Ch 4: 2007 equinox wakes Uranus up)  

---

## 5. Incorporate into the build (required)

| Data finding | Change to script / chapters / visuals / packaging |
|--------------|-----------------------------------------------------|
| Primary keyword (`Uranus`, `21-year winter`) | Title lead + sentence 1 VO mention + description first line |
| High-volume related term (`Voyager 2 Uranus`, `Miranda`) | Ch 3 (Six Hours at the Ice Giant) & Ch 6 (The Ten-Minute Cliff on Miranda) |
| Winning outlier structure | 6-act arc with midpoint twist at Ch 4 (2007 equinox storms + corkscrew magnet) |
| Weak competition angle | Per-chapter animated number objects + real NASA/Voyager 2/Hubble/Webb plates |
| Thumb pattern that works (Rule 19 + 12 + 14) | A: Single clean real spacecraft frame (`PIA18182` / `PIA25770`), B: Miranda cliff scale, C: Bright equinox test |

**Chapter list after audit** (6 acts, each with a teach-point and number object):

1. `The Star That Moved` (1781 Herschel discovery, 51,118 km = 4× Earth, 19 AU / 2 h 40 m light travel)  
2. `The World Knocked Sideways` (1977 KAO ring occultation, 13 rings, 28 moons, 97.77° tilt, 84-yr orbit / 21-yr winter)  
3. `Six Hours at the Ice Giant` (24 Jan 1986 Voyager 2 flyby at 81,500 km, −224.2 °C / 49 K colder than Neptune)  
4. `The Corkscrew Magnet` (Dec 2007 equinox midpoint turn, 900 km/h winds vs 400 km/h Earth, 60° tilted / 1/3-offset magnet)  
5. `Why You Can't Land on Ice` (≥80% hot dense water-methane-ammonia fluid, 4,982 °C / 9,000 °F core, no solid surface)  
6. `The Ten-Minute Cliff on Miranda` (1948 Kuiper discovery, 500 km moon, canyons 12× Grand Canyon, 10-minute free-fall, Real Worlds hand-off to Pluto)  

---

## 6. Retention plan (whole-video watch)

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| 0–0:05 | Curiosity spike | Real graded Hubble/Keck sideways Uranus + 21-year winter night claim in sentence 1 |
| ~0:15 | Stakes | 97.77° vs Earth's 23.44° tilt gauge + −224.2 °C colder than Neptune |
| ~0:35 | Central question | How did a giant planet get knocked onto its side, and what did Voyager 2 find there? |
| Chapter starts | Re-hook + chapter card | Cold open on date/scene; ends on question the next chapter answers |
| Mid (~60%) | Midpoint twist | `"Wrong."` — 2007 equinox wakes Uranus with 900 km/h winds + corkscrew magnet |
| Final chapter | Payoff + series hand-off | Miranda's 12× Grand Canyon cliff (10-min fall) → Real Worlds hand-off to Pluto |
| Outro | 15–20 s end-screen hold | Moving Miranda cliff / Uranus shot for Real Worlds playlist + next film end screen |

- [x] No 30s+ stretch without a new teach or turn  
- [x] Every chapter earns the next one  
- [x] Runtime target **8–12 min** (~9.0 min, 1,290 spoken words)  

---

## 7. Sign-off (block production until checked)

- [x] Keywords pulled and primary locked  
- [x] Title ≥90 locked (fearbait / series-suffix clutter rejected)  
- [x] Script reviewer ≥ 90 (`PASS 95.2 / 100` on `uranus_21_year_winter_script_master_v02.md`)  
- [x] Outlier patterns mapped into chapter arc  
- [x] Thumb concepts match title promise (one object · one emotion · Rule 19 real frame included)  
- [x] Chapter teach-points listed (6 acts)  
- [x] Cold-open clock (5 / 15 / 35s) written  
- [x] Retention plan filled  
- [x] Production checklist path noted: `11_Upload-Package/PRODUCTION_CHECKLIST_V2.md`  

**Signed off by:** Gemini (`gemini`, Rule-E reviewer for J2148)  
**Date:** 2026-11-04  
