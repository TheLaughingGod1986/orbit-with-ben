# Pre-build vidIQ audit — Orbit with Ben

**Hard gate:** Run **before** locking script, VO, prompts, or picture gen for any new long.

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | 013 / Why-The-Moon-Is-Slowly-Leaving-Us |
| Working title | Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone |
| Date pulled | 2026-09-03 |
| Credits used (approx) | 0 this session (reuse 2026-08-02 Moon title sheet · Ben to reconfirm ABC in app.vidiq.com before VO) |
| Brand guardrails | Wonder over fearbait · no conspiracy · Orbit DNA · experiential framing |
| Cluster | `cluster_moon_leaving_013` |
| Queue | **Next to make** after Neutron Star Premiere (`Yk1tLh23rko` · Thu 10 Sep 18:00) |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) — historical lock **99** (2026-08-02 sheet; drop series suffix for listing) |
| Primary keyword overall | moon leaving earth ~59.7 / ~5.0K / comp 33.6 |
| Hook promise | The Moon is already leaving — how fast, why, and what that does to eclipses |
| Retention design | 5 acts · centimetres → ancient closer Moon → tidal gearbox → last perfect eclipse → wonder window |
| Packaging | Thumb: Earth–Moon gap / ruler or eclipse coin · SEA hook · **no Orbit on thumb** |

---

## 2. Keyword research (vidIQ)

Source: `00_Brand/Channel-Setup/ideas/013_Moon-Leaving-Us/TITLE_SCORE_SHEET.md` (2026-08-02)

| Keyword | Overall | Est./mo | Comp | Role | Keep? |
|---------|--------:|--------:|-----:|------|-------|
| moon leaving earth | 59.7 | ~5.0K | 33.6 | primary / title | yes |
| moon drifting away | 58.2 | ~4.4K | 36.1 | alt / tags | yes |
| moon | 69.6 | huge | 66.5 | umbrella | light |
| space facts | 72.1 | — | 42.2 | Shorts / desc | yes |
| space documentary | 71.6 | ~428K | 47 | umbrella | yes |
| lunar recession | 33.6 | 0 | 16.1 | VO science only | no title |

**Decision:** Primary keyword for title lead = **moon leaving earth** / **moon is slowly leaving us**  
**Description first 100 chars must include:** moon leaving / drifting + what happens / eclipse

---

## 3. Title ABC (score before VO)

**Growth System v2:** one promise · **no** series suffix on the listing title.

| | Title | Score | Keep? |
|---|-------|------:|-------|
| A | Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone | **99** (2026-08-02 · with suffix historically) | **Locked working** |
| B | The Moon Is Leaving Earth — Here's What Happens Next | **97** | alt / Shorts |
| C | We Live in the Last Perfect Eclipse Window | **96** | wonder / thumb fuel |
| Reject | The Moon Will Destroy Earth When It Leaves (fearbait) | — | **Reject** |

**Locked title:** Why the Moon Is Slowly Leaving Us — and What Happens When It's Gone  
**Why it wins:** Highest score + assumption-flip + delayed payoff; wonder tone without fearbait.

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file \
  ../02_Video-Projects/013_Why-The-Moon-Is-Slowly-Leaving-Us/01_Script/moon_leaving_script_master_v01.md
```

**Result:** **PASS 90.4 / 100** (2026-09-03) · artifact `01_Script/SCRIPT_REVIEW_v01.md`

---

## 4. Outliers / comps (directional)

Moon-leaving / lunar recession explainers exist; Orbit differentiator: 7–9 min experiential journey · tidal gearbox acted in-scene · perfect-eclipse expiry · British VO · Shorts cluster · no fearbait.

---

## 5. Cold open / retention plan

| Beat | Line |
|------|------|
| 0–5s | What if the Moon is already leaving you? |
| ~15s | Centimetres a year — lasers on Apollo mirrors |
| ~30s | How fast / why / what about the last perfect eclipse? |

Chapters: The Moon Is Leaving · When It Was Closer · Why It Drifts · The Last Perfect Eclipse · The Wonder Window

---

## 6. Shorts cluster (4–8)

See `EPISODE_CLUSTER_PLAN.md` + seeds in that file.

---

## Sign-off

- [x] Keywords direction locked (reconfirm scores in vidIQ UI before VO)
- [x] Title working lock (ABC from 2026-08-02 sheet · Ben reconfirm ≥90 sans suffix)
- [x] Script reviewer ≥ 90 (**90.4 PASS**)
- [x] Experiential / cluster plan filled
- [ ] Ben confirms title ≥90 in vidIQ before VO spend

**Signed off by:** Cursor agent (scaffold + script PASS 90.4) — **Ben final title score before VO**  
**Date:** 2026-09-03
