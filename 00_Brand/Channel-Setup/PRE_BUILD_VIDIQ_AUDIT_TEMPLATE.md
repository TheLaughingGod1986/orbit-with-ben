# Pre-build vidIQ audit — Orbit With Ben

**Hard gate:** Run **before** locking script, VO, prompts, or picture gen for any new long.  
**Method (effective for topics locked from 1 Jan 2027 · Ben, 20 Nov 2026 · `J3222`):** Search-led topic method (`00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` §2, `05_Analytics/LEARNINGS.md` rule 37). Replaces the 1 Oct 2026 neighbour pass as the blocking gate; the neighbour list below is a **tie-breaker only**.  
**Goal:** Every episode targets proven Anglosphere adult search demand with a real results-page gap and small-channel outlier proof — not gut feel or crowded giant-channel subjects.  
**Also follow:** `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md`, `studio/RULES.md`, `THUMBNAIL_AND_TITLE_RULES.md`, and `FAMILIAR_DANGER_STRATEGY.md`.

Copy into each project as:

`02_Video-Projects/NNN_Slug/11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | |
| Working title | |
| Cluster (3–4 active clusters × 5–10 films) | |
| Format fit (passing Dec format) | |
| Weekly research file | `05_Analytics/owb/search_research/<YYYY-MM-DD>.md` |
| Date pulled | |
| vidIQ credits used (approx) | |
| Brand guardrails | Wonder over fearbait · no conspiracy · Orbit DNA |

---

## 1. Search-led gate summary (steps 1–4 · blocking from 1 Jan 2027)

| Field | Value | Gate / pass bar | Pass? |
|-------|-------|-----------------|-------|
| **Query** (signed-out US YouTube autocomplete exact phrasing) | | Exact phrase adults type | |
| **Volume** (vidIQ monthly searches) | | **10k–150k / month** | |
| **Competition** (vidIQ competition) | | **≤ 45** | |
| **Growth & seasonality** (vidIQ growth + Google Trends) | | Steady / rising evergreen | |
| **Top countries** (Anglosphere) | | US, UK, Canada, Australia among top markets; not dominated by low-paying markets | |
| **Adult** (adult intent) | | **Yes** — no kids or made-for-kids queries; evergreen; 10–20 min + series fit | |
| **RPM / earnings proxy** (vidIQ sub-niche channel estimates) | | Healthy Anglosphere adult RPM proxy | |
| **Top-10 gap** (signed-out top 10 count) | / 10 | Count of old (3+ yr), weak, off-target or small-channel results | |
| **Small-channel outliers** (<50k subs, ≥5× usual, last 12 mo) | | **≥ 1 verified outlier** (none = **no real opening**) | |
| **Cluster** | | Active cluster with playlist/end-screen chain; Shorts → long | |
| **Shorts-as-test signal** *(if already tested)* | | Fed Short + high stayed-to-watch | |

---

## 2. Keyword demand & value (vidIQ + US autocomplete + Google Trends)

Pull vidIQ keyword research (US / Anglosphere), signed-out US YouTube autocomplete, and Google Trends for the primary query and 4–7 supporting terms.

| Query | Est./mo (Volume) | Comp (≤45) | Growth / Trends | Top countries (US/UK/CA/AU?) | Adult? | Role (primary / secondary / chapter / Short) | Keep? |
|-------|-----------------:|-----------:|-----------------|------------------------------|--------|----------------------------------------------|-------|
| | | | | | | primary | |
| | | | | | | secondary | |
| | | | | | | chapter | |
| | | | | | | Short | |

**Primary query (exact US autocomplete phrasing):**  
**Sub-niche RPM / earnings proxy (vidIQ channel estimates):**  
**Description first 100 chars must include:**  

---

## 2b. Signed-out top-10 results-page gap (step 3)

Run `vidIQ youtube_search` or signed-out YouTube for the exact primary query and score all top 10 results.

| Rank | Video title | Channel | Subs | Age | Views | Answers query? | Gap flag (3+ yr / weak / off-target / <50k)? |
|-----:|-------------|---------|-----:|----:|------:|----------------|----------------------------------------------|
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |
| 6 | | | | | | | |
| 7 | | | | | | | |
| 8 | | | | | | | |
| 9 | | | | | | | |
| 10 | | | | | | | |

**Top-10 gap score:** ____ / 10 *(count of old 3+ yr, weak, off-target or small-channel results)*

---

## 2c. Neighbour list (tie-breaker only from 1 Jan 2027; was blocking 1 Oct 2026)

Optional tie-breaker between close search-led candidates and source of **subject-only words** for descriptions and tags. **Never** put channel names in title, description, or tags.

| # | Views | Channel (internal) | id | Title | Subject words we may reuse |
|---|------:|--------------------|----|-------|----------------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

**Proposed description first line(s)** (starts with primary query; wonder brand):  
**Proposed subject-only tags (5–8):**  

---

## 3. Package first — Title ABC & Thumbnail concepts (step 5, before any script)

Title starts with the **query words plus one hook** (≤70 chars, no series suffix, no fearbait/hedging). Score **three titles and two thumbnail ideas** against the small-channel outlier set before writing any script.

| | Title (query words + one hook) | vidIQ score | Beats outlier set? | Keep? |
|---|--------------------------------|------------:|--------------------|-------|
| A | | | | |
| B | | | | |
| C | | | | |
| Reject (fearbait / off-brand / no query words) | | | No | **Reject** |

**Thumbnail ideas (2 concepts scored against the outlier set, 168 px readable, no Orbit):**
- **Thumb A:**
- **Thumb B:**

**Locked title:**  
**Why it wins (query lead + hook + outlier comparison):**  

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

## 4. Small-channel proof — vidIQ outliers (step 4 · blocking from 1 Jan 2027)

Pull last-12-month vidIQ outliers on the subject from channels **under 50k subscribers** achieving **≥5×** their channel's usual views. **None found = no real opening (NO-GO).** Ignore meme/movie/kids noise.

| Outlier video | Channel | Subs (<50k) | Views / multiple (≥5×) | Published (last 12 mo) | Steal (structure / packaging) | Do **not** copy |
|---------------|---------|------------:|-----------------------:|------------------------|-------------------------------|-----------------|
| | | | | | | dread / fearbait |
| | | | | | | |

**Patterns we will use in this script:**

- [ ] Assumption-flip / open-loop hook  
- [ ] Numbered layers or chapter journey  
- [ ] Body-scale anchor  
- [ ] Slow reveal / delayed answer  
- [ ] Engineering / mission roadmap (if topic fits)  
- [ ] Other:  

---

## 5. Incorporate into the build & cluster plan (step 6 · required)

Translate research → creative and cluster decisions **before** writing the full script:

| Data finding | Change to script / chapters / visuals / packaging |
|--------------|-----------------------------------------------------|
| Primary query | Title lead + early VO mention + description line 1 |
| Top-10 gap | What existing results miss or explain poorly that we nail |
| Winning small-channel outlier | Chapter arc + thumbnail contrast |
| Cluster & playlist chain | Playlist name, end-screen next film, 2 cluster Shorts pointing here |
| Monthly own search terms (step 8) | Confirms cluster search views are growing (or first test in cluster) |

**Chapter list after audit** (4–6, each with a teach-point):

1.  
2.  
3.  
4.  
5. *(opt)*  
6. *(opt)*  

---

## 6. Retention plan (whole-video watch)

Design for **watching through**, not just CTR:

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| 0–0:08 | Stakes in title's words | Most striking real moving image at frame 0; no Orbit/logo/fade |
| ~0:20 | Concrete payoff hint | Real number, date, or answer image; picture change ≤4 s |
| ~0:30 | Journey clear | Every sentence adds a new fact; zero agenda line |
| Chapter starts | Re-hook + chapter card | First card ≥0:45; new question / turn |
| Mid | Teach while story continues | DATA + SCALE + WHO/WHEN/FACT overlays |
| Final chapter | Payoff + bigger question | Answer loop · hand off to next film in cluster |
| Outro | Cluster hand-off | No goodbye / no subscribe ask; end screen → cluster playlist |

- [ ] No 30 s+ stretch without a new teach or turn  
- [ ] Every chapter earns the next one  
- [ ] Runtime target **10–20 min** (or passing December format runtime)  

---

## 7. Sign-off (block production until checked)

- [ ] Primary query verified via signed-out US autocomplete; volume **10k–150k/mo**, competition **≤45**
- [ ] Anglosphere (US/UK/CA/AU) top markets, **adult intent** (not kids), evergreen, RPM proxy checked
- [ ] Signed-out **top-10 gap** scored
- [ ] **Small-channel outlier proof** (<50k subs, ≥5× usual, last 12 mo) verified
- [ ] **Cluster** assigned (playlist + end screen + Shorts → long)
- [ ] **Package first:** 3 titles + 2 thumb concepts scored against outlier set; locked title starts with query words + hook (≥90 vidIQ)
- [ ] Script reviewer ≥ 90 & `gate:episode` PASS
- [ ] Production checklist path noted: `templates/PRODUCTION_CHECKLIST_V2.md`

**Signed off by:**  
**Date:**  

**Only then:** full script → ElevenLabs VO → picture → edit.

---

## Tools

- vidIQ Keyword / Outliers / Title Analyzer (Claude cloud lane, `search-research` weekly run)
- Script reviewer: `cd 07_Content-Ops && npm run review:script -- --file <script.md>`
- Weekly search research: `05_Analytics/owb/search_research/<date>.md`
- Latest channel numbers: `00_Brand/Channel-Setup/audits/weekly/<date>/REPORT.md`
- How to build: `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md`
- Brand: wonder over clickbait — data informs structure, never overrides Orbit DNA
