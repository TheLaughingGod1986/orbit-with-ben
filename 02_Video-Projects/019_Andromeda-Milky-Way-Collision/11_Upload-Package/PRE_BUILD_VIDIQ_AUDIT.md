# Pre-build vidIQ audit — Orbit with Ben

**Hard gate:** Run **before** locking script, VO, prompts, or picture gen for any new long.  
**Goal:** Every episode is aimed at **views + full-video watch** using live data — not gut feel alone.  
**Also follow:** `RETENTION_AND_GROWTH_LOCKED.md` (punch-first opens, Shorts funnel, teach-per-chapter).  
**Listing path (mandatory):** `.cursor/rules/orbit-vidiq-source-of-truth.mdc` + `VIDIQ_LISTING_OPTIMIZATION_PLAYBOOK.md` — apply the same VidIQ optimize path to **longs and Shorts** (title, description, tags, thumbs/ABC; VidIQ generate thumbs if needed).

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | **019** / `Andromeda-Milky-Way-Collision` |
| Working title (locked) | **What Happens When Andromeda Hits the Milky Way?** |
| Date pulled | 17 Sep 2026 (Channel Scout niche board) |
| Credits used (approx) | 0 — **no invented VidIQ title scores**; Ben confirm volumes/scores in VidIQ when signed in |
| Brand guardrails | Wonder over fearbait · no conspiracy · Orbit DNA |
| Cluster | `cluster_andromeda_collision_001` |
| Premiere | Thu 24 Sep 2026 18:00 Europe/London |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) — **pending Ben VidIQ confirm** (do not invent numeric scores) |
| Primary keyword overall | Scout seed **andromeda collision milky way** · opp **64** / demand **85** |
| Hook promise | A second Milky Way is already in the sky — and it’s getting closer (sky rewrite · honest clock · survive) |
| Retention design | 6 chapter cards · teach + turn each act · picture-first ~3s |
| Packaging | Thumb: dual spirals closing · one emotion (awe) · **no Orbit** on long thumb |

---

## 2. Keyword research (Channel Scout usable — VidIQ volumes blank)

Source: Channel Scout live scans 17 Sep 2026 (`agent-tools/channelscout-scans-2026-09-17/andromeda-collision-milky-way.json` + sibling `andromeda-milky-way-collision.json`).  
**Est./mo:** leave blank / Scout proxy — **Ben confirm in VidIQ**. Do **not** invent volumes.

| Keyword | Overall | Est./mo | Comp | Role | Keep? | Source |
|---------|--------:|--------:|-----:|------|-------|--------|
| andromeda collision milky way | Scout opp **64** / demand **85** | Scout proxy — Ben confirm in VidIQ | — | **primary** title/desc | yes | Scout usable |
| andromeda milky way collision | Scout opp **64** / demand **84** | Scout proxy — Ben confirm in VidIQ | — | primary sibling | yes | Scout usable |
| andromeda galaxy | — | Scout proxy — Ben confirm in VidIQ | — | secondary / umbrella | yes | Scout usable |
| andromeda collision milky way for beginners | — | Scout proxy — Ben confirm in VidIQ | — | desc / Soft chapter | yes | Scout usable |
| how andromeda collision milky way works | — | Scout proxy — Ben confirm in VidIQ | — | desc / chapter | yes | Scout usable |
| how andromeda milky way collision works | — | Scout proxy — Ben confirm in VidIQ | — | desc / chapter | yes | Scout usable |
| andromeda collision milky way mistakes | — | Scout proxy — Ben confirm in VidIQ | — | Shorts / assumption-flip | maybe | Scout usable |
| the milky | — | — | — | **noise** (too-short) | **no** | Scout hygiene discard |

**Decision:** Primary keyword for title lead = **andromeda collision milky way** (Scout board #1 · KEEP)  
**Description first 100 chars must include:** Andromeda + Milky Way + collision / what happens  

---

## 3. Title ABC (score before VO)

**Growth System v2:** one promise · prefer ≤ ~60 characters · **do not** append `| Orbit's Cosmic Journey`.

| | Title | Score | Keep? |
|---|-------|------:|-------|
| A | What Happens When Andromeda Hits the Milky Way? | _(no invented VidIQ score)_ | **LOCKED** — Ben locked A **17 Sep 2026** |
| B | What Happens When the Milky Way Collides With Andromeda? | Scout proxy — Ben confirm in VidIQ | Scout alt (seed-family flip) |
| C | How the Andromeda–Milky Way Collision Works | Scout proxy — Ben confirm in VidIQ | Scout alt (usable “how … works”) |
| Reject | Andromeda Is Coming To Destroy Our Galaxy… (fearbait / doom) | — | **Reject** |

**Locked title:** What Happens When Andromeda Hits the Milky Way?  
**Why it wins (brand + keyword + Scout):** Matches Scout working-title angle; one promise; leads with Andromeda + Hits + Milky Way; wonder over fearbait; Ben locked **A** on **17 Sep 2026**.

Regen sheet:

```bash
python3 04_Audio/tools/vidiq_title_score_sheet.py --project-dir 02_Video-Projects/019_Andromeda-Milky-Way-Collision
```

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file \
  ../02_Video-Projects/019_Andromeda-Milky-Way-Collision/01_Script/andromeda_collision_script_master_v03.md
```

- [x] Score ≥ **90 / 100** — **PASS 90.4** on master **v03** (17 Sep 2026) · `01_Script/SCRIPT_REVIEW_v03.md`

---

## 4. Outlier / competitive patterns (on-brand only)

Scout breakouts (structure only — ignore fearbait / meme):

| Outlier / pattern | Steal (structure) | Do **not** copy |
|-------------------|-------------------|-----------------|
| Collision sim Shorts (sky rewrite / dual spirals) | Picture-first arrival · visual payoff | Doom captions / skull emoji |
| “What happens when galaxies collide?” | Experiential question title | Clickbait destroy framing |
| Night-sky when Andromeda arrives | Future Earth night as hero beat | Panic / end-of-world |

**Patterns we will use in this script:**

- [x] Assumption-flip / open-loop title  
- [x] Numbered layers or chapter journey (6 CHAPTER CARDs)  
- [x] Body-scale / sky-scale anchor (Earth night → Local Group)  
- [x] Slow reveal / delayed answer (honest clock uncertainty)  
- [ ] Engineering roadmap (if topic fits)  
- [x] Other: gravity-dance flip (stars almost never hit)

---

## 5. Incorporate into the build (required)

| Data finding | Change to script / chapters / visuals / packaging |
|--------------|-----------------------------------------------------|
| Primary keyword | Title lead + early VO (Andromeda smudge) + desc |
| High-demand Scout seed | Collision = gravity rewrite, not smash (assumption flip) |
| Winning outlier structure | Picture-first dual spirals · sky rewrite mid · Milkomeda payoff |
| Weak competition angle | Honest uncertainty clock (date still being sharpened) |
| Thumb pattern | Two spirals closing · awe · no Orbit |

**Chapter list after audit** (from script CHAPTER CARDs):

1. The Second Spiral  
2. The Honest Clock  
3. When the Night Sky Rewrites  
4. Stars Almost Never Hit  
5. Would We Survive?  
6. What Else Is Coming?  

---

## 6. Retention plan (whole-video watch)

From master **v03** cold open + house clock:

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| 0–0:03 | Picture-first | Dual spirals world still · **no Orbit** · no brand sting |
| 0–0:05 | Curiosity spike | “A second Milky Way is already in the sky — and it’s getting closer.” |
| ~0:15 | Stakes | Not tomorrow · not Hollywood smash · measurable clock · night sky won’t survive the meeting |
| ~0:30 | Journey clear | Timeline ride: sky changes · what collision means · Earth might live · galaxy left behind |
| Chapter starts | Re-hook + chapter card | New question / turn each act |
| Mid | Teach while story continues | Mid reset: Andromeda covering more sky → rivaling Milky Way band; smash→gravity flip |
| Final chapter | Payoff + bigger question | Inheritance under stranger night · Local Group / what else is changing |
| Outro | Soft return CTA | ≥10–15s hold for Studio end screens · no baked subscribe · no /go/ |

- [x] No 30s+ stretch without a new teach or turn  
- [x] Every chapter earns the next one  
- [x] Runtime target **7–9 min** (trust-building window; house lock)

---

## 7. Sign-off (block production until checked)

- [x] Keywords pulled and primary locked (Scout usable; Est./mo = Scout proxy — Ben confirm in VidIQ)  
- [x] Title locked (**A** Ben 17 Sep 2026) — VidIQ numeric score **not invented**; confirm ≥90 in app when signed in  
- [x] Script reviewer ≥ 90 — **PASS 90.4 v03**  
- [x] Outlier patterns mapped into chapter arc  
- [x] Thumb concepts match title promise (one object · one emotion) — dual spirals / awe  
- [x] Chapter teach-points listed (6 acts from CHAPTER CARDs)  
- [x] Cold-open clock (5 / 15 / 30s) written from v03  
- [x] Retention plan filled  
- [x] Production checklist path noted: `templates/PRODUCTION_CHECKLIST_V2.md`  

**Signed off by: Ben (verbal build go in CoS chat 17 Sep 2026 “Great let’s build it”)**  
**Date:** 17 Sep 2026  

**Only then:** full script → ElevenLabs VO → AI Studio picture (stills first · Veo world · Omni Orbit-only) → edit.

---

## Tools

- Title Analyzer / Keyword: https://app.vidiq.com  
- Script reviewer: `cd 07_Content-Ops && npm run review:script -- --file <script.md>`  
- Channel Scout scans: `agent-tools/channelscout-scans-2026-09-17/`  
- Story / VO–picture gate: `LONGFORM_STORY_AND_VO_PICTURE_GATE.md`  
- Growth system: `YOUTUBE_GROWTH_SYSTEM_V2.md`  
- Brand: wonder over clickbait — data informs structure, never overrides Orbit DNA
