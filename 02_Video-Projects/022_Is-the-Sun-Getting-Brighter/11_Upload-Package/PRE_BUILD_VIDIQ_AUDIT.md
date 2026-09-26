# Pre-build vidIQ audit — Orbit with Ben

**Hard gate:** Run **before** locking script, VO, prompts, or picture gen for any new long.
**Goal:** Every episode is aimed at **views + full-video watch** using live data — not gut feel alone.
**Also follow:** `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` and `FAMILIAR_DANGER_STRATEGY.md`.

VidIQ was **not available** in this session (25 Sep 2026). No `VIDIQ` credential in the environment. `04_Audio/tools/vidiq_title_score_sheet.py` only writes a blank sheet. It does not call VidIQ. **No title score, keyword overall, volume, or competition number below is from VidIQ. None were invented.**

Ben picked the topic anyway. The studio topic score in the 25 Sep pick is a ten-row average, not a VidIQ score.

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | 022 / Is-the-Sun-Getting-Brighter |
| Working title | Is the Sun Getting Brighter? |
| Date pulled | 2026-09-25 |
| Credits used (approx) | 0. VidIQ was not opened. |
| Brand guardrails | Wonder over fearbait · no conspiracy · Orbit DNA |
| Cluster | `cluster_sun_brighter_022` |
| Intended air | Sunday 11 October 2026, 18:00 UK. Not scheduled. |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** once VidIQ is open. **Not scored. Not invented.** |
| Primary keyword overall | Unknown until VidIQ. Do not treat the topic-pick search as a VidIQ volume. |
| Hook promise | The Sun is getting brighter — why, what the fainter sky was like, and what the climb does next. |
| Retention design | Five acts. Prominence is the wrong clock. Core ash makes the star brighter. Fainter young Sun. Ten percent more. You are in the middle. |
| Packaging | One Sun, prominence already moving. Two to four words. No Orbit. Not designed as a file in this step. |

---

## 2. Keyword research (vidIQ)

Not pulled. VidIQ was unavailable. The table is empty on purpose.

| Keyword | Overall | Est./mo | Comp | Role (title / desc / chapter / Shorts) | Keep? |
|---------|--------:|--------:|-----:|----------------------------------------|-------|
| is the sun getting brighter | — | — | — | intended primary | pending VidIQ |
| sun getting brighter | — | — | — | secondary | pending VidIQ |
| faint young sun | — | — | — | chapter / desc | pending VidIQ |
| sunspot cycle brightness | — | — | — | chapter, so the film is not misunderstood | pending VidIQ |
| solar luminosity | — | — | — | description science | pending VidIQ |

**Decision:** Primary keyword for the title Ben locked = the exact question **Is the Sun Getting Brighter?**
**Description first 100 chars must include:** the Sun getting brighter, and that this is the long life of the star, not the sunspot cycle.

Signed-out YouTube search on 25 Sep 2026 is recorded in the topic pick, not here as VidIQ data. Closest on-topic neighbour found that hour: *Why is the Sun getting brighter?* (Bright Side, 239,947 views). The exact yes/no in that top five had 449 views (The Bluebox).

---

## 3. Title ABC (score before VO)

One promise. No series suffix. Scores blank until VidIQ.

| | Title | Score | Keep? |
|---|-------|------:|-------|
| A | Is the Sun Getting Brighter? | — | Ben locked this shape. Score unknown. |
| B | Why Is the Sun Getting Brighter? | — | Near-synonym. Bright Side already uses “why”. Not locked. |
| C | The Sun Is Getting Brighter | — | Statement, not the yes/no shape that won. Not locked. |
| Reject (fearbait / off-brand / series-suffix clutter even if high) | What Happens When the Sun Dies? | — | **Reject.** Crowds Last Star and a search already held by much larger channels. |
| Reject | Is the Sun Getting Brighter? \| Orbit's Cosmic Journey | — | **Reject.** Series suffix. |

**Locked title:** Is the Sun Getting Brighter?
**Why it wins (score + brand + keyword):** Ben locked the yes/no. VidIQ has not scored it. A higher fear title would not replace it.

---

## 3b. Script reviewer (blocking before VO)

```bash
cd 07_Content-Ops && npm run review:script -- --file \
  ../02_Video-Projects/022_Is-the-Sun-Getting-Brighter/01_Script/sun_brighter_script_master_v01.md
```

- [x] Script reviewer ≥ 90 — **PASS 90.4 / 100** on 25 Sep 2026. See `01_Script/SCRIPT_REVIEW_v01.md`. This tick is the reviewer only. It is not a VidIQ sign-off.

---

## 4. Outlier / competitive patterns (on-brand only)

From the signed-out search in the topic pick. Not a VidIQ outlier pull. Views are what that search returned on 25 Sep 2026.

| Outlier / pattern | Views / multiple | Steal (structure) | Do **not** copy |
|-------------------|------------------|-------------------|-----------------|
| Why is the Sun getting brighter? (Bright Side) | 239,947 | The “why” is the second act: brighter while it runs down | Their title. Dread packaging. |
| What's happened to the sun? (Richard Vobes) | 233,061 | Nothing. Different question (a recent change). | Any claim that the Sun changed lately. |
| Is The Sun Getting Brighter? (The Bluebox) | 449 | Exact yes/no can exist without a giant film on it | Their episode numbering. |
| The Night Sky Should Be Brighter Than the Sun (Action Lab) | 1,515,421 | Nothing. Olbers’ paradox. | That subject. |
| The Sun Gets 10% Brighter — What Happens to Earth? | 354 | The forward beat can be the ten-percent chapter | A death-of-Earth poster. |

**Patterns we will use in this script:**

- [x] Assumption-flip / open-loop title
- [ ] Numbered layers or chapter journey
- [ ] Body-scale anchor
- [x] Slow reveal / delayed answer — the prominence is the wrong clock; the core is the answer
- [ ] Engineering roadmap (if topic fits)
- [x] Other: yes/no about a familiar thing, same shape as the Moon film

---

## 5. Incorporate into the build (required)

| Data finding | Change to script / chapters / visuals / packaging |
|--------------|-----------------------------------------------------|
| Exact yes/no is the open search, not a VidIQ volume | Title stays *Is the Sun Getting Brighter?* Sentence one says it. |
| “Why” is the crowded neighbour | The why is chapter 2, not a second title. |
| Recent-change films sit next to this query | The open says it is not the spots and not a human century. |
| Ten-percent Earth films exist and are small | Chapter 4 uses the 2008 moist-greenhouse limit and stops before the red giant. |
| No Sun Short on this channel | Cluster seeds are listed. No Short is scripted here. |

**Chapter list after audit** (4–6, each with a teach-point):

1. The Climb You Cannot See — 1% / 110 million years, not the sunspot cycle.
2. Brighter While It Runs Down — helium ash, hotter core, brighter star.
3. When the Light Was Less — faint young Sun, oceans anyway.
4. Ten Percent More — about a billion years, moist greenhouse, no red giant.
5. The Sun You Already Have — the middle of the climb, then a handoff.

---

## 6. Retention plan (whole-video watch)

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| 0–0:05 | Curiosity spike | “The Sun is getting brighter. Why does it brighten while it runs down?” Sun already moving. |
| ~0:15 | Stakes | The light on your face. The ribbon is the wrong danger. |
| ~0:30 | Journey clear | Why, the fainter sky, and what happens as the climb goes on. |
| Chapter starts | Re-hook + chapter card | After the open only. No card on frame 0. |
| Mid | Teach while the story continues | Core, then young Sun, then ten percent. Orbit in two beats. |
| Final chapter | Payoff + bigger question | Yes. How long can the blue last? |
| Outro | Handoff, no goodbye | Moving Sun. No baked subscribe. |

- [x] No 30s+ stretch without a new teach or turn
- [x] Every chapter earns the next one
- [x] Runtime target **7–9 min** in the current playbook (the old 8–12 line in this template is history)

---

## 7. Sign-off (block production until checked)

- [ ] Keywords pulled and primary locked — **not pulled. VidIQ unavailable.**
- [ ] Title ≥90 locked — **title is locked by Ben. VidIQ score was not measured.**
- [x] Script reviewer ≥ 90 — PASS 90.4 / 100 on 25 Sep 2026. The VidIQ pull is still open.
- [x] Outlier patterns mapped into chapter arc — from the signed-out search, not from VidIQ
- [ ] Thumb concepts match title promise — concept only, no file
- [x] Chapter teach-points listed (4–6 acts)
- [x] Cold-open clock (5 / 15 / 30s) written
- [x] Retention plan filled
- [x] Production checklist path noted: `11_Upload-Package/PRODUCTION_CHECKLIST_V2.md`

**Signed off by:**
**Date:**

Not signed. A name here would look like a VidIQ pass. It is not one.

**Only then:** full script → ElevenLabs VO → AI Studio picture. Voice and picture stay stopped.
