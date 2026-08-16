# Orbit with Ben — Channel Build System

Canonical creative-director playbook for the faceless animated science storytelling channel **Orbit with Ben**.

Live channel: https://www.youtube.com/@OrbitWithBen · `UC_esArsDKd3GJvOkeO0DUog`

**Feel:** Pixar meets space documentary.  
**Quality bar:** Kurzgesagt · PBS Space Time · Veritasium · Nat Geo docs · Pixar storytelling principles.

---

## Role (for every agent session)

Act as YouTube strategist, creative director, animation producer, AI content workflow architect, and growth marketer.

For every new video idea, deliver:

1. Title options  
2. Thumbnail concepts  
3. Full script  
4. Scene breakdown  
5. AI video prompts  
6. Voice instructions  
7. Editing plan  
8. SEO metadata  

Always protect the Orbit brand. Goal: build a recognisable space storytelling universe — not just isolated videos.

---

## Brand identity

| | |
|---|---|
| Channel name | Orbit with Ben |
| Handle | @OrbitWithBen |
| Mascot | Orbit — small orange exploration robot |
| Live banner line | Big questions. Bigger universe. |
| Core philosophy | Big questions. Deep universe. |
| Brand line | Space stories. Big questions. |

### Orbit character

Curious · friendly · intelligent · slightly humorous · wonder-driven · never childish · scientific explorer.

Orbit = emotional connection.  
*"A tiny robot asking the biggest questions in the universe."*

Use Orbit to introduce, react, explain hard ideas, add humour. **Not constantly** — guide, not wallpaper.

### Philosophy

Wonder over certainty · Curiosity over clickbait · Science over speculation · Exploration over fear.

**Avoid:** conspiracy, fake science, sensational misinformation.

---

## Audience

**Primary:** 18–45 · space, astronomy, AI, future tech, physics, evolution, alien life, civilisation.  
**Secondary:** families / younger viewers of animated educational content.

---

## Content pillars

1. **Cosmic Mysteries** — alone?, dark matter, black holes, beginning of the universe  
2. **Future Humanity** — Mars, AI + space, 1,000-year humans, interstellar species  
3. **Alien Civilisations** — Fermi, Great Filter, communication, advanced civs  
4. **Space Stories** — dying stars, heat death, strange planets, extreme events  

---

## Formats

### Long-form (pillar)

| | |
|---|---|
| Cadence | **1 / week** (Thu **19:00** UK · window 18:00–20:00) · BH cold-start exception allowed |
| Length now | **10–12 min** VO-locked (hard lock after V004) |
| Length later | 15–20 min only if retention earns it |
| Priority | Always first — Shorts never publish before the pillar is public |

**Structure (chapter story)**

1. **Hook (0–20s)** — mystery claim; picture proves it  
2. **Chapters (4–6)** — each is a mini-story with one **teach point** + visual must  
3. **Ending** — wonder takeaway + soft “next mystery” return energy + Orbit CTA  

Canonical gate: `Channel-Setup/LONGFORM_STORY_AND_VO_PICTURE_GATE.md`  
Rule: picture **shows or acts** the VO — no generic B-roll under specific narration.

### Shorts (support the pillar)

| | |
|---|---|
| Cadence | Launch **21:00** · supporting **12:30** · **3–5** scheduled + reserves · max 1/day · prefer 36–48h spacing |
| Length | Legacy baseline **41–45s** · experiment **22–30s** (JWST EXP-S01) |
| Job | Premium mini-docs that discover → funnel into **this week’s** long |

**Rules:** standalone value · hook **0–1.5s** spoken punch · one idea · curiosity ending · soft CTA (never an ad) · no random clip dumps · no welcome/logo open.

**Short arc:** 0–1.5s hook → 1.5–6s escalate → core evidence → payoff → optional 1–2s soft CTA.

Canonical: `Channel-Setup/PUBLISHING_AND_SHORTS_STRATEGY.md` · `docs/ORBIT_GROWTH_PLAYBOOK.md`

---

## Production stack

**CG (default):** Google **Gemini Veo API** — `04_Audio/tools/orbit_gemini_veo.py`  
**VO (locked):** **ElevenLabs TTS** — Ben Orbit Narrator only  
**Also:** Seedance (legacy/character refs) · Midjourney/image gen · CapCut / Premiere  

**Do not** use ElevenLabs Image & Video for new CG (cost + American speech + Explore contamination).

**Style:** premium animated documentary.  
**Avoid:** cheap AI slideshow, generic stock, random AI clip salad. Every scene intentional.

**Voice:** calm, curious, warm, intelligent British documentary narrator (Attenborough × modern doc) via ElevenLabs clone.

Workspace pipeline lives in repo README + per-video folders under `02_Video-Projects/`.  
Publish slots: `00_Brand/Channel-Setup/OPTIMAL_PUBLISH_SCHEDULE.json`.

---

## Titles & thumbnails

**Title formula:** Question + Mystery + Emotion.

| Bad | Good |
|---|---|
| Understanding Black Holes | I Entered A Black Hole |
| The Search For Alien Life | Why Haven't Aliens Found Us? |

**Thumbs:** one idea · mobile-readable · curiosity · Orbit only when he strengthens the idea.

---

## Per-video pipeline

1. **Pre-build vidIQ audit (blocking)** — keywords · titles · outliers · retention plan (`PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md`)  
2. **Chapter outline** — 4–6 named chapters with teach-points, shaped by that audit  
3. Script with `[VISUAL MUST]` / `[TEACH]` / `[CHAPTER CARD]` on every scene  
4. Scene breakdown (number · duration · visual · camera · Orbit · AI prompt) — prompts derived from markers only  
5. Title already locked from audit (≥90); re-check thumb ABC against promise  
6. Voice (ElevenLabs · Ben clone) → **lock VO duration** → captions via `04_Audio/tools/transcribe_vo.py`  
7. Generate visuals **to VO timeline** (Orbit identity lock · unique plates · no loops)  
8. Edit — brand intro + chapter cards + subscribe outro; SFX/music from script cues  
9. **VO–picture QA gate** (watch once: no generic stretch under specific VO)  
10. Package (titles · thumb ABC · description · tags · chapters · SEO)  
11. Upload / schedule on `@OrbitWithBen` (long Thu 19:00 → Shorts cluster)  
12. Fill content flywheel (`CONTENT_FLYWHEEL_TEMPLATE.md`) · run `RELEASE_WEEK_CHECKLIST.md`  

**Do not** lock VO or spend Veo/Ultra credits until step 1 is signed off.  
Success = **views + higher % watched**, not packaging alone.

Package template: `00_Brand/Channel-Setup/VIDEO_PACKAGE_TEMPLATE.md`  
Audio tools: `04_Audio/tools/README.md`  
Publishing system: `00_Brand/Channel-Setup/PUBLISHING_AND_SHORTS_STRATEGY.md`

---

## First 10 videos (ordered backlog)

| # | Working title |
|---|---|
| 001 | Why Haven't We Found Aliens Yet? The Fermi Paradox Explained *(vidIQ 97 · metadata locked)* |
| 002 | What Happens If You Fall Into A Black Hole? |
| 003 | Alien Worlds: The Strangest Planets We've Ever Found *(locked · vidIQ 97)* |
| 004 | What the James Webb Telescope Discovered That Changes Everything |
| 005 | The Last Star In The Universe |
| 006 | Could Life Exist Under The Ice Of Europa? |
| 007 | **Neutron Star** *(next to make · script passed · Omni 1-min path)* |
| 008 | What Will Humans Become In 1,000 Years? |
| 009 | The Day The Sun Dies |
| 010 | Could AI Help Humanity Reach The Stars? |
| 011 | The Most Dangerous Place In The Universe |
| 012 | The Great Filter: Why Haven't We Found Aliens? *(deferred)* |

Backlog file: `00_Brand/Channel-Setup/VIDEO_BACKLOG.json`

---

## Growth & year-one targets

- Library-first · evergreen search + suggested + retention (not trend-chasing only)  
- CTR **5–10%** · AVD **40%+** · sub conversion **3–5%**  
- **100+** videos year one · recognisable Orbit universe · **50k–100k** subs  

**Monetisation (later):** ads · sponsorships (space/AI/edu) · memberships · Orbit merch · digital learning packs.

---

## Guardrails

- Never present outputs as certainty or “proof” of aliens/conspiracies  
- Preserve Orbit visual bible (`01_Orbit-Character/`)  
- Do not edit OpptiAI channel assets or Studio for Orbit work  
- Prefer wonder, humility, and current science over hype  

---

## Related docs

- Live channel: `Channel-Setup/CHANNEL_READY.md`  
- Publishing & Shorts: `Channel-Setup/PUBLISHING_AND_SHORTS_STRATEGY.md`  
- Cadence card: `Channel-Setup/CHANNEL_PUBLISH_CADENCE.md`  
- Brand snapshot: `Brand-Guidelines/ORBIT_BRAND_SNAPSHOT.md`  
- Character bible: `../01_Orbit-Character/`  
- Workspace rules: `../README.md`
