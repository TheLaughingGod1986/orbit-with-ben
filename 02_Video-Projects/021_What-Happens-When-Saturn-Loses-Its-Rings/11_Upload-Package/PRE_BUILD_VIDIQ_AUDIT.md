# Pre-build vidIQ audit — Orbit with Ben

**Hard gate:** Run **before** locking script, VO, prompts, or picture gen for any new long.  
**Also follow:** `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` and `FAMILIAR_DANGER_STRATEGY.md`.

**Data note (2026-09-26):** No vidIQ login in this session. Keyword overall / est./mo / competition cells marked **vidIQ not available - to fill in Studio**. Competition and packaging use signed-out YouTube search via `yt-dlp ytsearch10` (same pass as `audits/NEXT_LONG_TOPIC_2026-10-11.md`).

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | 021 / What-Happens-When-Saturn-Loses-Its-Rings |
| Working title | What Happens When Saturn Loses Its Rings? |
| Date pulled | 2026-09-26 |
| Credits used (approx) | 0 (no vidIQ) |
| Brand guardrails | Wonder over fearbait · no conspiracy · Orbit DNA · Familiar Danger |
| Cluster | `cluster_saturn_rings_021` |
| Queue | **Next long** — Sun 11 Oct 2026 18:00 UK (normal publish). Ben picked Candidate A. |
| Upload status | **Clean** — never uploaded or scheduled (no `11_Upload-Package` YouTube id; not in public longs snapshot 25 Sep; no Saturn title on `@OrbitWithBen` videos tab) |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) — **vidIQ not available - to fill in Studio** |
| Primary keyword overall | saturn loses rings / saturn rings disappearing — **vidIQ not available - to fill in Studio** |
| Hook promise | Saturn’s rings are already falling — why, what they were when new, what Saturn looks like without them |
| Retention design | 5 acts · falling sheet → ice not rock → ring rain (payoff) → when new → bare Saturn |
| Packaging | Thumb: one ring-plane subject · 2–4 words (e.g. FALLING IN? / NO RINGS?) · **no Orbit on thumb** · does not repeat the title |

---

## 2. Keyword research

| Keyword | Overall | Est./mo | Comp | Role | Keep? |
|---------|--------:|--------:|-----:|------|-------|
| saturn loses its rings / saturn losing rings | vidIQ not available - to fill in Studio | — | — | primary / title | yes |
| saturn rings disappearing | vidIQ not available - to fill in Studio | — | — | alt / tags | yes |
| saturn rings | vidIQ not available - to fill in Studio | — | — | umbrella | light |
| ring rain saturn | vidIQ not available - to fill in Studio | — | — | chapter / desc | yes |
| cassini grand finale | vidIQ not available - to fill in Studio | — | — | desc / teach | yes |
| space documentary | vidIQ not available - to fill in Studio | — | — | umbrella | yes |

**Signed-out YouTube competition (exact title *What Happens When Saturn Loses Its Rings?*):**

| # | Views | Subscribers | Channel | Result title |
|--:|------:|---|---|---|
| 1 | 1,397,631 | 10.6M | Insider Tech | Saturn Is Officially Losing Its Rings |
| 2 | 57,045 | 14.6M | BBC Earth Science | This Is Why Saturn's Rings Are Disappearing… |
| 3 | 1,527 | 15.6K | Cosmoknowledge | Saturn Is Losing Its Rings |
| 4 | 286,528 | 4.75M | AumSum's What-If | Why is Saturn losing its Rings? + more… |
| 5 | 7,310 | ~2.6M | euronews | Saturn 'losing its rings', new NASA research finds |

**Decision:** Primary keyword for title lead = **Saturn** + **loses its rings** (question shape).  
**Description first 100 chars must include:** Saturn losing / rings falling + ring rain / what remains.  
**Narrower angle?** Not required for an Orbit 8–9 min wonder cut; differentiate with ring-plane open + no fearbait. Optional alt if Studio CTR is weak: *What Would You See If Saturn Had No Rings?*

---

## 3. Title ABC (score before VO)

**Growth System v2:** one promise · **no** series suffix · no hashtags.

| | Title | Score | Keep? |
|---|-------|------:|-------|
| A | What Happens When Saturn Loses Its Rings? | vidIQ not available - to fill in Studio (shape: ending; keyword in first five words) | **Locked** |
| B | What Would You See If Saturn Had No Rings? | vidIQ not available - to fill in Studio | alt if CTR weak |
| C | Why Saturn's Rings Are Already Falling | vidIQ not available - to fill in Studio | Shorts fuel |
| Reject | Saturn's Rings Will Destroy the Planet (fearbait) | — | **Reject** |

**Locked title:** What Happens When Saturn Loses Its Rings?  
**Why it wins:** Familiar Danger ending shape; searchable question; matches Moon/Last Star packaging; Ben picked Candidate A (26 Sep topic pass).

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file \
  ../02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings/01_Script/saturn_rings_script_master_v01.md
```

**Result:** **PASS 90 / 100** (2026-09-26) · artifact `01_Script/SCRIPT_REVIEW_v01.md` · gate `11_Upload-Package/EPISODE_GATE_v01.md` **PASS**

---

## 4. Outlier / competitive patterns (on-brand only)

| Outlier / pattern | Views / multiple | Steal (structure) | Do **not** copy |
|-------------------|------------------|-------------------|-----------------|
| Insider Tech / BBC Earth news clips | 57K–1.4M | Short “rings disappearing” hook | News VO, dread, talking-head only |
| Channel Moon long / Shorts | Moon leaving 290 / 253 Shorts | Familiar thing leaving · wonder · centimetre/age clock | Fearbait · duplicate title |
| Europa “hiding” Short | 291 | Something-is-changing reveal | Same ice-globe plate |

**Patterns we will use in this script:**

- [x] Assumption-flip / open-loop title  
- [x] Numbered layers or chapter journey  
- [x] Body-scale anchor (ten metres / Mimas mass)  
- [x] Slow reveal / delayed answer  
- [ ] Engineering roadmap (if topic fits)  
- [x] Other: Familiar Danger twin of Moon leaving  

---

## 5. Incorporate into the build (required)

| Data finding | Change to script / chapters / visuals / packaging |
|--------------|-----------------------------------------------------|
| Primary keyword Saturn + loses rings | Title + spoken title once after first payoff + desc |
| News-clip competition | Open on moving ring plane, not a NASA clip cut |
| Moon-leaving pattern won | Same “leaving” wonder; ~100 Myr honest clock |
| Low ring mass / Cassini | Teach beat + Cassini-only probe |
| Thumb | FALLING IN? or NO RINGS? — not the full title |

**Chapter list after audit** (5 acts):

1. The Rings Are Falling  
2. Ice, Not Rock  
3. The Rain Into Saturn *(first payoff + subscribe beat)*  
4. When the Rings Were New  
5. Saturn Without Them  

---

## 6. Retention plan (whole-video watch)

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| 0–0:03 | Danger on frame | Ring plane falling; no Orbit |
| ~0:15 | Stakes | Sheet will not last; ~100 Myr |
| ~0:30 | Journey clear | Why fall / when new / bare Saturn |
| Chapter starts | Re-hook + card | Soft starfield card |
| Mid | Ring rain payoff | Cassini in the rain; subscribe beat |
| Final chapter | Bare Saturn | Orbit tiny reaction |
| Outro | Bigger question | Hand off; moving end hold |

- [x] No 30s+ stretch without a new teach or turn  
- [x] Every chapter earns the next one  
- [x] Runtime target **8–9 min**  

---

## 7. Sign-off (block production until checked)

- [x] Keywords pulled and primary locked *(yt-dlp competition; vidIQ fields pending Studio)*  
- [x] Title locked (fearbait / series-suffix clutter rejected) — Ben Candidate A  
- [x] Script reviewer ≥ 90 *(see SCRIPT_REVIEW after run)*  
- [x] Outlier patterns mapped into chapter arc  
- [x] Thumb concepts match title promise (one object · one emotion) — concepts only; thumbs need Ben OK  
- [x] Chapter teach-points listed (5 acts)  
- [x] Cold-open clock (5 / 15 / 30s) written  
- [x] Retention plan filled  
- [x] Production checklist path noted: `11_Upload-Package/PRODUCTION_CHECKLIST_V2.md`  

**Signed off by:** Cloud Agent (step 2) after Ben topic pick Candidate A  
**Date:** 2026-09-26  

**Only then:** full script → Ben OK → ElevenLabs VO → AI Studio picture → edit.

**Stop:** No VO / picture / thumbs / uploads until Ben OKs this script package.
