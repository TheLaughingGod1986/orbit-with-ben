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
| ID / slug | 031_What-Happens-When-Earths-Magnetic-Field-Flips |
| Working title | What Happens When Earth's Magnetic Field Flips? |
| Date pulled | 16 Oct 2026 (`J0251` topic lock) & verified 8 Nov 2026 (`yt-dlp` public search, Mini, `J2401`) |
| Credits used (approx) | 0 (no vidIQ; waived since 022) |
| Brand guardrails | Wonder over fearbait · no conspiracy · Orbit DNA |
| Neighbour pass | Earth's magnetic field reversal **strong** (4 education/science videos at 1M+ views: `I6Ggs7nUjxA` 4.19M, `ridb9olnqLc` 2.84M, `sm4uHnnbg4Y` 1.61M, `51usJ74pPP8` 1.38M; plus `Ou1BiorYRNU` 663K). |

---

## 0. Neighbour pass (`yt-dlp` public search)

Channel names are internal notes; they never go in our title, description or tags.

| Views | Id | Title |
|------:|----|-------|
| 4.19M | `I6Ggs7nUjxA` | What Will Happen When Earth's North And South Pole Flip? |
| 2.84M | `ridb9olnqLc` | What the Upcoming Geomagnetic Reversal Will Do to Earth |
| 1.61M | `sm4uHnnbg4Y` | What the Upcoming Magnetic Flip Will Do to Earth |
| 1.38M | `51usJ74pPP8` | Is Earth's Magnetic Field Reversing? |
| 663K | `Ou1BiorYRNU` | What Happens When Earth's Magnetic Poles Reverse? |

Subject words: Earth magnetic field, magnetic pole reversal, geomagnetic reversal, north magnetic pole, magnetic north, South Atlantic Anomaly, Earth core, geodynamo, Brunhes Matuyama reversal, Laschamp event, aurora, Swarm satellites.

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) |
| Primary keyword overall | Earth magnetic field / magnetic pole reversal (4 neighbours at 1M+) |
| Hook promise | One sentence — must match thumb + open VO |
| Retention design | Chapters that earn the next minute (teach + turn) |
| Packaging | Thumb readable on mobile; one idea |

---

## 2. Keyword research (vidIQ)

Pull GB (or primary market) research for 5–8 terms.

| Keyword | Overall | Est./mo | Comp | Role (title / desc / chapter / Shorts) | Keep? |
|---------|--------:|--------:|-----:|----------------------------------------|-------|
| Earth magnetic field | — | — | — | primary | Yes |
| magnetic pole reversal | — | — | — | primary / description | Yes |
| geomagnetic reversal | — | — | — | secondary | Yes |
| north magnetic pole | — | — | — | opening hook / chapter 1 | Yes |
| South Atlantic Anomaly | — | — | — | chapter 4 / Shorts | Yes |
| Laschamp event | — | — | — | chapter 5 (kauri tree) | Yes |
| Earth core | — | — | — | chapter 3 | Yes |

**Decision:** Primary keyword for title lead = `Earth's Magnetic Field Flips`  
**Description first 100 chars must include:** `Earth's north magnetic pole`, `Siberia`, `magnetic field reversal`  

---

## 3. Title ABC (score before VO)

**Growth System v2:** one promise · prefer ≤ ~50 characters · **do not** append `| Orbit's Cosmic Journey` (or similar series suffix). Brand lives in the content.

| | Title | Score | Keep? |
|---|-------|------:|-------|
| A | What Happens When Earth's Magnetic Field Flips? | 96 | **Keep (Lead)** |
| B | Why Earth's Magnetic North Is Racing to Siberia | 93 | Backup |
| C | What Happens When Earth's Magnetic Poles Swap? | 92 | Backup |
| Reject (fearbait / off-brand / series-suffix clutter even if high) | Will a Magnetic Pole Flip Wipe Out Life on Earth? | — | **Reject** |

**Locked title:** `What Happens When Earth's Magnetic Field Flips?`  
**Why it wins (score + brand + keyword):** Direct `What Happens When...` question shape (`47` chars ≤ 50), familiar noun `Earth's` in the first 4 words, matches the 4.19M and 1.61M neighbour search terms with zero fearbait.

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/01_Script/magnetic_field_flip_script_master_v03.md
```

- [x] Score ≥ **90 / 100** (`95 / 100` PASS)  
- Scorecard: `templates/SCRIPT_REVIEW_SCORECARD.md`  
- Reject / rewrite if below threshold  

---

## 4. Outlier / competitive patterns (on-brand only)

**Patterns we will use in this script:**

- [x] Assumption-flip / open-loop title  
- [x] Numbered layers or chapter journey  
- [x] Body-scale anchor  
- [x] Slow reveal / delayed answer  

---

## 5. Incorporate into the build (required)

**Chapter list after audit** (7 acts, each with a teach-point):

1. `0:00` The Racing Pole (magnetic north moving from ~16 km/yr to ~55 km/yr toward Siberia; 1,100 km since 1831; immediate survival reassurance)  
2. `0:36` The Backwards Lava (Brunhes 1905 Pontfarein basalt & Matuyama 1929 reversed quaternary lava; 780,000-year Brunhes–Matuyama flip; 183 reversals in 83 million years)  
3. `2:05` The Ocean of Liquid Iron (Gauss 1839 internal origin; 2,889 km depth liquid iron-nickel outer core geodynamo; 9% drop since 1840)  
4. `3:46` The Dent Over South America (South Atlantic Anomaly, ESA Swarm 3-satellite constellation, Hubble SAA shutdowns & ISS radiation shielding)  
5. `5:19` The Tree That Remembered (42,000-year-old New Zealand kauri tree 1,700-ring radiocarbon record of the Laschamp excursion; field down to ~6%)  
6. `6:33` Why Our Air Stays Put (gravity + thick nitrogen-oxygen atmosphere vs Mars; zero mass extinction link in marine fossils)  
7. `8:00` Poles All Over the Sky (multi-pole transition over 1,000–10,000 years, migratory animals, and global auroras)  

---

## 6. Retention plan (whole-video watch)

- [x] No 30s+ stretch without a new teach or turn  
- [x] Every chapter earns the next one  
- [x] Runtime target **8–12 min** in trust-building window (`9:31` locked master `v02`, `570.80 s`)  

---

## 7. Sign-off (block production until checked)

- [x] Keywords pulled and primary locked  
- [x] Title ≥90 locked (fearbait / series-suffix clutter rejected)  
- [x] Script reviewer ≥ 90 (`magnetic_field_flip_script_master_v03.md`, `95/100` PASS)  
- [x] Outlier patterns mapped into chapter arc  
- [x] Thumb concepts match title promise (one object · one emotion)  
- [x] Chapter teach-points listed (7 acts)  
- [x] Cold-open clock (5 / 15 / 30s) written  
- [x] Retention plan filled  
- [x] Production checklist path noted: `templates/PRODUCTION_CHECKLIST_V2.md`  

**Signed off by:** Claude (`J0251` topic lock + `J0259` script `v03` `95/100` PASS) & Gemini (`J2401` acting Chief package verification)  
**Date:** 8 Nov 2026  

**Only then:** full script → ElevenLabs VO → AI Studio picture (stills first · Veo world · Omni Orbit-only) → edit.
