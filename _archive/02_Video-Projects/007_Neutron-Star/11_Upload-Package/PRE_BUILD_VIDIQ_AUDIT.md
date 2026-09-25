# Pre-build vidIQ audit — Orbit with Ben

**Hard gate:** Run **before** locking script, VO, prompts, or picture gen for any new long.  
**Goal:** Every episode is aimed at **views + full-video watch** using live data — not gut feel alone.  
**Also follow:** `RETENTION_AND_GROWTH_LOCKED.md` (punch-first opens, Shorts funnel, teach-per-chapter).  
**Listing path (mandatory):** `.cursor/rules/orbit-vidiq-source-of-truth.mdc` + `VIDIQ_LISTING_OPTIMIZATION_PLAYBOOK.md` — apply the same VidIQ optimize path to **longs and Shorts** (title, description, tags, thumbs/ABC; VidIQ generate thumbs if needed).

Copy into each project as:

`02_Video-Projects/NNN_Slug/11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | |
| Working title | |
| Date pulled | |
| Credits used (approx) | |
| Brand guardrails | Wonder over fearbait · no conspiracy · Orbit DNA |

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

**Only then:** full script → ElevenLabs VO → Gemini Veo picture → edit.

---

## Tools

- Title Analyzer / Keyword: https://app.vidiq.com  
- Script reviewer: `cd 07_Content-Ops && npm run review:script -- --file <script.md>`  
- Channel audit puller (optional refresh): `00_Brand/Channel-Setup/audits/_pull_vidiq_full_audit.py`  
- Story / VO–picture gate: `LONGFORM_STORY_AND_VO_PICTURE_GATE.md`  
- Growth system: `YOUTUBE_GROWTH_SYSTEM_V2.md`  
- Brand: wonder over clickbait — data informs structure, never overrides Orbit DNA
