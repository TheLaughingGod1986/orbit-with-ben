# Orbit With Ben — YouTube Growth System v2

**Locked:** 2026-08-06  
**Status:** Canonical production system  
**Brand:** Do **not** redesign. Optimise distribution, retention, and session building.  
**Success metrics (in order of pipeline focus):** Impressions → CTR → AVD → APV → Session time → Returning viewers → Browse / Suggested / Search

Companion locks:

- `RETENTION_AND_GROWTH_LOCKED.md` — P0 checklist agents must follow  
- `LONGFORM_STORY_AND_VO_PICTURE_GATE.md` — story + VO–picture  
- `PUBLISHING_AND_SHORTS_STRATEGY.md` — cadence + Shorts funnel  
- `PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md` — pre-build data gate  
- Content Ops: script reviewer · analytics recommendations  

---

## What stays (not the bottleneck)

Visual / CGI quality · Orbit mascot · branding · educational accuracy · calm British narration · chapter system · thumbnail craft · SEO descriptions · metadata · tags.

Do not burn cycles “improving” these at the expense of hook, structure, length, Orbit agency, and funnel.

---

## Primary problems → locked fixes

### 1. Slow openings (biggest issue)

First 30–60s must not explain before the story begins.

| Forbidden open | Required open |
|----------------|---------------|
| “What is a black hole?” | “Orbit has just crossed the event horizon…” |
| “What is the Fermi Paradox?” | “If aliens exist… why has nobody ever arrived?” |
| Channel intro / history / background lecture | Immediate tension · mystery · stakes |

**Cold-open clock**

| Beat | Time | Job |
|------|------|-----|
| Curiosity spike | **0–5s** | Huge unanswered need |
| Stakes | **~15s** | Why it matters now |
| Journey promise | **~30s** | Viewer knows the ride they’re on |

Never begin with channel introductions, educational background, or history. Begin with the mystery.

### 2. Narrative structure

Stop: Introduction → Explanation → Story  

Use:

```
Question → Danger → Story begins → Explanation while story continues
  → Escalation → Ending
```

Explanation happens **while Orbit experiences events** — documentary × cinematic storytelling.

### 3. Runtime (next 6–10 videos)

| Phase | Target |
|-------|--------|
| Trust-building (now) | **8–12 minutes** VO |
| After audience trust | 15 → 18 → 20 → 25 min |

Shorter masters raise completion %, APV, return rate, and recommendation potential before the channel has earned long watch trust.

### 4. Orbit’s role

Orbit is not a passive narrator mascot. Orbit **actively experiences** the science:

- Falling into the black hole  
- Standing on Europa  
- Inside Jupiter’s atmosphere  
- Witnessing a supernova  
- Flying through a Dyson Sphere  

Audience emotion rides with Orbit.

### 5. Story framework (every script)

```
HOOK → QUESTION → ESCALATION → DISCOVERY → PAYOFF → BIGGER QUESTION
```

Each chapter increases curiosity. 4–6 **film-act** chapters — not 12–18 tiny ones.

### 6. Emotional engagement

Science stays strong; add lived stakes:

- “What would YOU see?”  
- “What would YOU feel?”  
- “What happens next?”  
- “What if everything we’ve assumed is wrong?”  

### 7. Titles

- Prefer **≤ ~60 characters**  
- **One promise**  
- No `| Orbit’s Cosmic Journey` (or similar series suffix) on every upload  
- Brand lives in the content; title sells the mystery  

Good: *What Really Happens When You Fall Into a Black Hole?*  
Bad: *What Happens If You Fall Into a Black Hole? | Orbit’s Cosmic Journey*

### 8. Thumbnails

Keep craft; tighten to **one question**:

- One object · one emotion · minimal text · immediate curiosity  
- Thumb answers the same promise as the title  

### 9. Shorts = discovery engine

Each long → **3–5 Shorts** (ops may hold reserves; cluster still funnels to the pillar).

Every Short:

1. Opens with the **strongest fact**  
2. Ends with an **unanswered question** / curiosity gap  
3. Links via YouTube **Related video pill** → that week’s Thursday long only (**no new Short pins**; see `orbit-shorts-related-video.mdc`)  

Never only “Watch the full video.”  
Prefer: *“There is one reason scientists fear the Great Filter. Orbit discovers it in the full documentary.”*

### 10. Long-video funnel & internal linking

```
Long → Shorts → Comments → Subscribers → Next long
```

Every long must ship with **no dead ends**:

- End screen → another Orbit documentary  
- Cards → related Orbit film  
- Pinned comment → next / companion mystery  
- Description links → series / next watch  

Build **sessions**, not single watches.

---

## Gates before production

1. **Pre-build vidIQ audit** (`PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md`)  
2. **AI Script Reviewer** — score ≥ **90 / 100** or reject/rewrite  
   - CLI: `cd 07_Content-Ops && npm run review:script -- --file <script.md>`  
3. **Production checklist** (`templates/PRODUCTION_CHECKLIST_V2.md`) before publish  

Dimensions (10 pts each → 100): Hook · Curiosity · Storytelling · Scientific accuracy · Emotion · Escalation · Retention potential · Search potential · Visual opportunities · Narration flow.

---

## Analytics loop

Import Studio / CSV metrics into Content Ops → **Analytics**.

Track and diagnose:

Impressions · CTR · AVD · APV · Retention graph signals · Returning / new viewers · Subs gained · Traffic (Browse % · Suggested % · Search %) · End screen CTR · Cards CTR · Avg session time · Top hooks / topics / Shorts.

Auto-flag: weak openings · retention drops · poor titles · weak thumbnails · videos needing updates.

Post-upload: actionable recommendations from `youtube-growth` insights (Content Ops).

---

## Future topic selection

Prioritise emotionally compelling questions. Rank on:

| Criterion | Why |
|-----------|-----|
| Search demand | Impressions / Search traffic |
| Curiosity | CTR + open loop |
| Visual potential | Orbit-in-scene CGI |
| Storytelling | Cold open + escalation |
| Series potential | Session → next long |

Template: `templates/TOPIC_OPPORTUNITY_SCORE.md`

Seed pool (examples — score before locking):

- What If Earth Lost the Moon?  
- The Last Day Before the Sun Dies  
- Could Humanity Survive on Mars?  
- What If We Detected an Alien Signal Tomorrow?  
- Could We Build a Dyson Sphere?  
- What Happens Inside Jupiter?  
- The Planet Where It Rains Glass  
- Could We Escape the Milky Way?  
- What If the Sun Suddenly Disappeared?  

---

## Long-term vision

Not a generic AI channel. A modern **BBC Earth / Nat Geo for space** with a recognisable animated host.

Orbit is the character viewers return for. Each upload is another chapter in one universe.

Measure success by **how each video grows the audience for the next one** — evergreen library + recommendation training for the ideal viewer.
