# Pre-build vidIQ audit — Orbit with Ben

**Hard gate:** Run **before** locking script, VO, prompts, or picture gen for any new long.  
**Also follow:** `RETENTION_AND_GROWTH_LOCKED.md` · `CONTENT_INTELLIGENCE_STRATEGY.md`

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | 007 / What-Happens-To-Your-Body-Near-A-Neutron-Star |
| Working title | What Happens to Your Body Near a Neutron Star? |
| Date pulled | 2026-08-13 |
| Credits used (approx) | 0 (VidIQ MCP unavailable this session — Ben to score ABC in app.vidiq.com) |
| Brand guardrails | Wonder over fearbait · no conspiracy · Orbit DNA · experiential framing |
| Cluster | `cluster_neutron_star_001` |
| Queue | After current slate (JWST live week · Last Star finishing) |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) — **pending Ben vidIQ confirm** |
| Primary keyword overall | neutron star / what happens neutron star (Browse/Suggested primary) |
| Hook promise | What happens to YOUR body as you approach — see, feel, survive limits |
| Retention design | 6 acts · Orbit experiences density → light → tides → crust → BH edge |
| Packaging | Thumb: Orbit + compact star + lensing ring |

---

## 2. Keyword research (vidIQ)

Pull GB research for 5–8 terms in app.vidiq.com (fill scores when available).

| Keyword | Overall | Est./mo | Comp | Role | Keep? |
|---------|--------:|--------:|-----:|------|-------|
| what happens if you fall into a neutron star | | | | title / primary variant | yes |
| neutron star | | | | umbrella | yes |
| what happens to your body neutron star | | | | title lead | yes |
| teaspoon of neutron star | | | | Shorts / chapter | yes |
| magnetar | | | | secondary | maybe |
| pulsar explained | | | | secondary | maybe |
| spaghettification | | | | caution — BH overlap | light touch |
| space documentary | | | | umbrella | yes |

**Decision:** Primary keyword for title lead = **what happens to your body near a neutron star** (experiential)  
**Description first 100 chars must include:** neutron star + what happens to your body / what you would see  

**Note:** Search is secondary to Browse/Suggested per content intelligence strategy.

---

## 3. Title ABC (score before VO)

**Growth System v2:** one promise · prefer ≤ ~60 characters · **no** series suffix.

| | Title | Score | Keep? |
|---|-------|------:|-------|
| A | What Happens to Your Body Near a Neutron Star? | _pending_ | **Locked working** |
| B | What Would You See Near a Neutron Star? | _pending_ | alt |
| C | Could You Survive Near a Neutron Star? | _pending_ | alt |
| Reject | Deadliest Star Will Crush You Instantly (fearbait) | — | **Reject** |

**Locked title:** What Happens to Your Body Near a Neutron Star?  
**Why it wins (score + brand + keyword):** Matches experiential hypothesis (LOW confidence early BH Short signal); one promise; body stakes; distinct from V002 BH long.

Regen sheet:

```bash
python3 04_Audio/tools/vidiq_title_score_sheet.py \
  --project-dir 02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star
```

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file \
  ../02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/01_Script/neutron_star_script_master_v01.md
```

**Result:** **PASS 91.1 / 100** (2026-08-13) · artifact `01_Script/SCRIPT_REVIEW_v01.md`

---

## 4. Outliers / comps (directional)

Experiential neutron-star Shorts/longs exist in the wild (touch / stand on / marshmallow density). Orbit differentiator: documentary depth ~18 min · Orbit-in-scene · cluster Shorts · British VO · no fearbait.

---

## 5. Cold open / retention plan

| Beat | Line |
|------|------|
| 0–5s | Ordinary-looking star → numbers kill ordinary |
| ~15s | You wouldn’t feel “falling”; space tears you into a line of atoms |
| ~30s | Light bends into a ring — what happens to you? |

Chapters: Corpse of a Star · Density · What You Would See · What You Would Feel · Surface Isn’t a Floor · Not a Black Hole / Bigger Question

---

## 6. Shorts cluster (4–8)

See `EPISODE_CLUSTER_PLAN.md` + `10_Shorts/SHORTS_CLUSTER_SEEDS.md`

---

## Sign-off

- [x] Keywords direction locked (scores pending Ben in vidIQ UI)
- [x] Title working lock (ABC scores pending)
- [x] Script reviewer ≥ 90
- [x] Experiential / cluster plan filled
- [ ] Ben confirms title ≥90 in vidIQ before VO spend

**Signed off by:** Cursor agent (scaffold + script PASS) — **Ben final title score before VO**  
**Date:** 2026-08-13
