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
| ID / slug | 028_A-Star-Is-Coming-Toward-Us |
| Working title | A star is coming toward us (Gliese 710); backups: rogue planet passing the Solar System, what if Betelgeuse explodes |
| Date pulled | 7 Oct 2026, 21:55–22:10 UTC (`yt-dlp` public search, Mini) |
| Credits used (approx) | 0 (no vidIQ; waived since 022) |
| Brand guardrails | Wonder over fearbait · no conspiracy · Orbit DNA |
| Neighbour pass | Gliese 710 **medium** (4 adjacent at 1M+, none direct; top direct 613K) · rogue planet **strong** (5 at 1M+) · Betelgeuse **strong** (6 at 1M+). Full tables: `TOPIC_OPPORTUNITY_SCORE.md` (job J0027) |

---

## 0. Neighbour pass (J0027, 7 Oct 2026)

Channel names are internal notes; they never go in our title, description or tags.

**Gliese 710 (lead).** No video on the named star reaches 1M (Anton Petrov `Q2i4kcOjavM` 613K). Adjacent 1M+ neighbours:

| Views | Id | Title (channel) |
|------:|----|-----------------|
| 20.76M | `gLZJlf5rHVs` | What If Earth got Kicked Out of the Solar System? Rogue Earth (Kurzgesagt) |
| 2.91M | `q4mc-alL92U` | The Oort Cloud: The Solar System's Shell (SEA) |
| 2.73M | `K8Slss_lhAw` | The Invisible 1.5 Light-Year Wall Around Our Solar System (Astrum) |
| 1.97M | `bJXGt26f8ZI` | What If Another Sun Entered Our Solar System? (What If) |

Subject words: star entering the solar system, passing star, oort cloud, comets, kuiper belt, rogue star, gliese 710.

**Rogue planet (backup 1).** 1M+: `gLZJlf5rHVs` 20.76M, `M7CkdB5z9PY` 14.44M, `lV5XYfhLeaU` 1.99M, `VwcfkzxNre4` 1.95M, `IWL3VlwiTxU` 1.60M. Subject words: rogue planet, free floating planet, rogue planet entered our solar system, interstellar space, microlensing.

**Betelgeuse (backup 2).** 1M+: `evUfG3lrk5U` 14.58M, `5bvuwTuGnkc` 2.77M, `SbCHSYJfLu8` 2.46M, `RHKtnBeBHcU` 2.17M, `qkBoH5l-6EY` 1.69M, `k6uODhvkRh8` 1.11M. Subject words: betelgeuse, betelgeuse supernova, star explodes near earth, red supergiant, betelgeuse dimming.

Claude locks the topic from this. Description first lines and 5–8 tags get drafted from the locked topic's subject words.

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) |
| Primary keyword overall | Note score / volume / competition |
| Hook promise | One sentence — must match thumb + open VO |
| Retention design | Chapters that earn the next minute (teach + turn) |
| Packaging | Thumb readable on mobile; one idea |

---

## 2. Keyword research (vidIQ)

Pull GB (or primary market) research for 5–8 terms.

| Keyword | Overall | Est./mo | Comp | Role (title / desc / chapter / Shorts) | Keep? |
|---------|--------:|--------:|-----:|----------------------------------------|-------|
| | | | | primary | |
| | | | | secondary | |
| | | | | umbrella | |
| | | | | Shorts hooks | |

**Decision:** Primary keyword for title lead =  
**Description first 100 chars must include:**  

---

## 3. Title ABC (score before VO)

**Growth System v2:** one promise · prefer ≤ ~60 characters · **do not** append `| Orbit's Cosmic Journey` (or similar series suffix). Brand lives in the content.

| | Title | Score | Keep? |
|---|-------|------:|-------|
| A | | | |
| B | | | |
| C | | | |
| Reject (fearbait / off-brand / series-suffix clutter even if high) | | | **Reject** |

**Locked title:**  
**Why it wins (score + brand + keyword):**  

Regen sheet:

```bash
python3 04_Audio/tools/vidiq_title_score_sheet.py --project-dir 02_Video-Projects/<NN_Slug>
```

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file <path-to-script.md>
```

- [ ] Score ≥ **90 / 100**  
- Scorecard: `templates/SCRIPT_REVIEW_SCORECARD.md`  
- Reject / rewrite if below threshold  

---

## 4. Outlier / competitive patterns (on-brand only)

Pull outliers for the primary topic (≤80K–mid sub channels preferred). Ignore meme/movie noise.

| Outlier / pattern | Views / multiple | Steal (structure) | Do **not** copy |
|-------------------|------------------|-------------------|-----------------|
| | | journey / assumption-flip / roadmap | dread / fearbait |
| | | | |

**Patterns we will use in this script:**

- [ ] Assumption-flip / open-loop title  
- [ ] Numbered layers or chapter journey  
- [ ] Body-scale anchor  
- [ ] Slow reveal / delayed answer  
- [ ] Engineering roadmap (if topic fits)  
- [ ] Other:  

---

## 5. Incorporate into the build (required)

Translate data → creative decisions **before** writing the full script:

| Data finding | Change to script / chapters / visuals / packaging |
|--------------|-----------------------------------------------------|
| Primary keyword | Title lead + early VO mention + desc |
| High-volume related term | One chapter or Short dedicated to it |
| Winning outlier structure | Chapter arc shape |
| Weak competition angle | Our Orbit-unique hook (character / teach) |
| Thumb pattern that works | Thumb ABC concept |

**Chapter list after audit** (4–6, each with a teach-point):

1.  
2.  
3.  
4.  
5. *(opt)*  
6. *(opt)*  

---

## 6. Retention plan (whole-video watch)

Design for **watching through**, not just CTR (Growth System v2):

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| 0–0:05 | Curiosity spike | Mystery / danger on frame 1 |
| ~0:15 | Stakes | Why it matters now |
| ~0:30 | Journey clear | Viewer knows the ride |
| Chapter starts | Re-hook + chapter card | New question / turn |
| Mid | Teach while story continues | Orbit experiences the science |
| Final chapter | Payoff + bigger question | Answer loop · open next |
| Outro | Soft return CTA | Brand outro — don’t dump new science |

- [ ] No 30s+ stretch without a new teach or turn  
- [ ] Every chapter earns the next one  
- [ ] Runtime target **8–12 min** in trust-building window  

---

## 7. Sign-off (block production until checked)

- [ ] Keywords pulled and primary locked  
- [ ] Title ≥90 locked (fearbait / series-suffix clutter rejected)  
- [ ] Script reviewer ≥ 90  
- [ ] Outlier patterns mapped into chapter arc  
- [ ] Thumb concepts match title promise (one object · one emotion)  
- [ ] Chapter teach-points listed (4–6 acts)  
- [ ] Cold-open clock (5 / 15 / 30s) written  
- [ ] Retention plan filled  
- [ ] Production checklist path noted: `templates/PRODUCTION_CHECKLIST_V2.md`  

**Signed off by:**  
**Date:**  

**Only then:** full script → ElevenLabs VO → AI Studio picture (stills first · Veo world · Omni Orbit-only) → edit.

---

## Tools

- Title Analyzer / Keyword: https://app.vidiq.com  
- Script reviewer: `cd 07_Content-Ops && npm run review:script -- --file <script.md>`  
- Latest channel numbers: `00_Brand/Channel-Setup/audits/weekly/<date>/REPORT.md`  
- How to build: `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md`  
- Strategy: `00_Brand/Channel-Setup/FAMILIAR_DANGER_STRATEGY.md`  
- Brand: wonder over clickbait — data informs structure, never overrides Orbit DNA
