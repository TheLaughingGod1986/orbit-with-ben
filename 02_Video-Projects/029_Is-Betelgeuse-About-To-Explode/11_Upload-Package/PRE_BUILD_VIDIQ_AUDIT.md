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
| ID / slug | 029_Is-Betelgeuse-About-To-Explode |
| Working title | Is Betelgeuse About to Explode? |
| Date pulled | 7 Oct 2026, 21:55–22:10 UTC (`yt-dlp` public search, Mini, job J0027) |
| Credits used (approx) | 0 (no vidIQ; waived since 022) |
| Brand guardrails | Wonder over fearbait · no conspiracy · Orbit DNA |
| Neighbour pass | Betelgeuse **strong** (6 education/space videos at 1M+ views: `evUfG3lrk5U` 14.58M, `5bvuwTuGnkc` 2.77M, `SbCHSYJfLu8` 2.46M, `RHKtnBeBHcU` 2.17M, `qkBoH5l-6EY` 1.69M, `k6uODhvkRh8` 1.11M). Full tables: `028_A-Star-Is-Coming-Toward-Us/11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md` (job J0027) |

---

## 0. Neighbour pass (J0027, 7 Oct 2026)

Channel names are internal notes; they never go in our title, description or tags.

| Views | Id | Title |
|------:|----|-------|
| 14.58M | `evUfG3lrk5U` | What If Betelgeuse Exploded Right Now? |
| 2.77M | `5bvuwTuGnkc` | Something Strange Is Happening to Betelgeuse |
| 2.46M | `SbCHSYJfLu8` | When Will Betelgeuse Explode? |
| 2.17M | `RHKtnBeBHcU` | Betelgeuse Supernova: What Will It Look Like From Earth? |
| 1.69M | `qkBoH5l-6EY` | Why Did Betelgeuse Dim in 2019? |
| 1.11M | `k6uODhvkRh8` | The Red Supergiant in Orion's Shoulder |

Subject words: Betelgeuse, Betelgeuse supernova, red supergiant, Orion constellation, Great Dimming, star explosion, supernova near Earth, astronomy.

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) |
| Primary keyword overall | Betelgeuse / Betelgeuse supernova (6 neighbours at 1M+) |
| Hook promise | One sentence — must match thumb + open VO |
| Retention design | Chapters that earn the next minute (teach + turn) |
| Packaging | Thumb readable on mobile; one idea |

---

## 2. Keyword research (vidIQ)

Pull GB (or primary market) research for 5–8 terms.

| Keyword | Overall | Est./mo | Comp | Role (title / desc / chapter / Shorts) | Keep? |
|---------|--------:|--------:|-----:|----------------------------------------|-------|
| Betelgeuse | — | — | — | primary | Yes |
| Betelgeuse supernova | — | — | — | secondary | Yes |
| red supergiant | — | — | — | secondary | Yes |
| Orion constellation | — | — | — | umbrella | Yes |
| Great Dimming | — | — | — | chapter / Shorts hooks | Yes |

**Decision:** Primary keyword for title lead = `Betelgeuse`  
**Description first 100 chars must include:** `Betelgeuse`, `red supergiant`, `Orion`  

---

## 3. Title ABC (score before VO)

**Growth System v2:** one promise · prefer ≤ ~60 characters · **do not** append `| Orbit's Cosmic Journey` (or similar series suffix). Brand lives in the content.

| | Title | Score | Keep? |
|---|-------|------:|-------|
| A | Is Betelgeuse About to Explode? | 95 | **Keep (Lead)** |
| B | What Happens When Betelgeuse Finally Explodes? | 93 | Backup |
| C | Why Did Betelgeuse Suddenly Go Dim in 2019? | 91 | Backup |
| Reject (fearbait / off-brand / series-suffix clutter even if high) | Will Betelgeuse Destroy Earth When It Explodes? | — | **Reject** |

**Locked title:** `Is Betelgeuse About to Explode?`  
**Why it wins (score + brand + keyword):** Positive yes/no question shape on a searched named star (`Betelgeuse` in first 2 words, 31 chars), zero threat framing.

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/01_Script/betelgeuse_script_master_v02.md
```

- [x] Score ≥ **90 / 100** (`92.2 / 100` PASS)  
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

**Chapter list after audit** (5 acts, each with a teach-point):

1. The Star in Orion's Shoulder (scale past Mars, 500–700 light-years, ~10 million years old)  
2. The Great Dimming (late 2019–early 2020 drop by >60%, VLT/SPHERE & Hubble surface mass ejection dust cloud)  
3. How a Giant Star Dies (hydrogen → helium → carbon → iron core collapse in <1 second, neutrino surge)  
4. The Night It Goes (half-Moon brightness for ~3 months, visible by day, safe 500–700 ly distance vs <50 ly danger zone)  
5. So When Will It Explode? (core helium burning ~100,000 years left, 2025 companion star detection, light-travel time)  

---

## 6. Retention plan (whole-video watch)

- [x] No 30s+ stretch without a new teach or turn  
- [x] Every chapter earns the next one  
- [x] Runtime target **8–12 min** in trust-building window (`9:02` locked master)  

---

## 7. Sign-off (block production until checked)

- [x] Keywords pulled and primary locked  
- [x] Title ≥90 locked (fearbait / series-suffix clutter rejected)  
- [x] Script reviewer ≥ 90 (`betelgeuse_script_master_v02.md`, 92.2/100 PASS)  
- [x] Outlier patterns mapped into chapter arc  
- [x] Thumb concepts match title promise (one object · one emotion)  
- [x] Chapter teach-points listed (4–6 acts)  
- [x] Cold-open clock (5 / 15 / 30s) written  
- [x] Retention plan filled  
- [x] Production checklist path noted: `templates/PRODUCTION_CHECKLIST_V2.md`  

**Signed off by:** Claude (topic lock `82d0f3f` + script v02 `92.2/100` PASS)  
**Date:** 8 Oct 2026  

**Only then:** full script → ElevenLabs VO → AI Studio picture (stills first · Veo world · Omni Orbit-only) → edit.
