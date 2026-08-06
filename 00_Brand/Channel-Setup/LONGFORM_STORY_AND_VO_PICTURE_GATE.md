# Long-form story + VO–picture gate (Orbit with Ben)

**Status:** Hard rule · Growth System v2 (2026-08-06) · applies to **every long after JWST (V004)**  
**First target:** next new production after current ships  
**Length lock:** **8–12 minutes** spoken VO during trust-building (then grow toward 15–25)  
**System:** `YOUTUBE_GROWTH_SYSTEM_V2.md`

This is how we fix slow opens, passive Orbit, and “lots of picture / weak match” — and make each episode a **fascinating lesson** viewers return for.

---

## Promise to the viewer

Every long must deliver all three:

1. **Mystery** — an open question that pulls them through  
2. **Story** — chapters that feel like a journey, not a Wikipedia dump  
3. **Learning** — they leave knowing something concrete they didn’t know before  

If they only feel “wow CGI” without a takeaway, the episode failed.

---

## Cold open (non-negotiable)

| Beat | Time | Job |
|------|------|-----|
| Curiosity | **0–5s** | Huge unanswered need — speech + drama immediately |
| Stakes | **~15s** | Danger / consequence / why now |
| Journey | **~30s** | Viewer knows exactly what ride they’re on |

**Forbidden:** channel intro · educational background · history lecture · “What is X?” definition opens.

**Required pattern:** Question → Danger → Story begins → Explanation **while** the story continues → Escalation → Ending.

Example swaps:

- Not “What is a black hole?” → “Orbit has just crossed the event horizon…”  
- Not “What is the Fermi Paradox?” → “If aliens exist… why has nobody ever arrived?”

Brand intro sting may still exist as a **brief** plate, but it must not consume the curiosity window — prefer mystery first, sting as flash or after the hook lands.

---

## Length

| | |
|---|---|
| Trust-building (next 6–10 videos) | **8–12 min** VO-locked master |
| Words (guide) | ~1,200–1,900 spoken |
| Chapters | **4–6** story chapters (+ brand sting + subscribe outro) |
| Later growth | 15 → 18 → 20 → 25 min once trust is earned |
| Pad rule | Never pad picture or VO to hit length — cut instead |

---

## Story framework (required)

Every script follows:

```
HOOK → QUESTION → ESCALATION → DISCOVERY → PAYOFF → BIGGER QUESTION
```

### Chapter storytelling

Write **named chapters**. Each chapter is a mini-act:

| Beat | Job |
|------|-----|
| **Entry** | One clear question or claim |
| **Show** | Picture proves / acts the line (see VO–picture below) |
| **Teach** | One concrete fact or mechanism they can repeat |
| **Turn** | A small surprise / “but…” that opens the next chapter |
| **Exit** | Soft handoff — “so what does that mean for…?” |

### Orbit agency (required)

Orbit **experiences** the science in-scene: falls, stands, flies through, witnesses — emotionally connect the audience to Orbit. `[ORBIT ACTS: …]` must describe agency, not “Orbit floats nearby.”

### Emotional stakes

Include lived / “you” language without fearbait: what would you see, feel, do next — imagination with Orbit.

### Chapter card rule

- Locked still chapter plate at each chapter start (`[CHAPTER CARD: Title]`)  
- No Ken Burns / zoompan on text  
- Chapter title = story beat language (“When the Moon Was Closer”), not jargon (“Lunar Recession Dynamics”)

---

## VO–picture lock (non-negotiable)

**Picture must show or act what the narration is saying in that moment.**

### Script markers (required on every scene)

| Marker | Meaning |
|--------|---------|
| `[VISUAL MUST: …]` | Exact on-screen proof for this VO beat |
| `[ORBIT ACTS: …]` | What Orbit **does** (active, not wallpaper) |
| `[TEACH: …]` | The one fact this beat teaches |
| `[CHAPTER CARD: …]` | Chapter boundary |

### Assembly rules

1. Build timeline **from VO timestamps first**, then assign picture to beats.  
2. One VO idea → one picture intent. No “pretty space” fillers while VO is specific.  
3. If VO names an object/action, that object/action is on screen within ~1s.  
4. Unique plates only inside one episode (cutscene rules). Brand intro/outro + Orbit character beds may reuse across episodes.  
5. Motion clip plays **once**; remainder of beat = unique still pan for that scene — never loop.  
6. Reject / regen any clip that breaks Orbit identity or contradicts the VO beat.

### Edit QA gate (before upload)

Watch with VO only once, then picture+VO:

- [ ] Cold open hits 5 / 15 / 30s jobs  
- [ ] Every chapter teaches one clear thing  
- [ ] No 8s+ stretch of generic scenery while VO is concrete  
- [ ] Orbit reacts or **acts** on emotional turns  
- [ ] Ending: payoff + bigger question + soft next-mystery energy (not hard sell)

---

## Tone mix

| Ingredient | How it shows up |
|------------|-----------------|
| Mystery | Open loop in title + hook; delay full answer |
| Educational | Named mechanisms, honest numbers, repeatable takeaway |
| Wonder | Pixar-warm Orbit; awe without dread/fearbait |
| Return habit | Bigger question + “there’s always another layer” |

**Avoid:** conspiracy, fearbait, Wikipedia dumps, VO/picture drift, looping B-roll, passive Orbit.

---

## Pipeline order (tightened)

**0. Pre-build vidIQ audit (blocking)** — keywords · title ABC ≥90 · outliers · packaging  
   → `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`  
**0b. Script reviewer ≥ 90** — `npm run review:script` in Content Ops · reject otherwise  
1. **Chapter outline** with teach-points + Orbit experience beats  
2. Full script with `[VISUAL MUST]` / `[ORBIT ACTS]` / `[TEACH]`  
3. Scene board / prompts from those markers only  
4. ElevenLabs **VO** (Ben Orbit Narrator) → lock duration  
5. Picture gen via **Google Flow Veo UI / Ultra** (`orbit_flow_veo_ui.py`) / edit **matched to VO timeline** — not ElevenLabs Image & Video; AI Studio / API key only as fallback  
6. Chapter cards + brand sting + subscribe outro  
7. QA gate → `PRODUCTION_CHECKLIST_V2.md` → package → schedule  

**Do not** lock VO or spend **Flow Ultra / Veo** credits until steps 0 and 0b are signed off.

Templates: `PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md` · `SCRIPT_REVIEW_SCORECARD.md` · `PRODUCTION_CHECKLIST_V2.md` · `VIDEO_PACKAGE_TEMPLATE.md` · cutscenes: `CUTSCENE_RULES.md`

---

## Success test (creative + growth)

After watching, a viewer should be able to say:

> “I didn’t know X — and now I want the next Orbit mystery.”

Packaging + structure aim for:

- **More impressions + CTR** — one-promise title · thumb question  
- **Higher AVD / APV** — cold open + Orbit-in-story + chapter turns  
- **Session time** — end screen / cards / pin → next documentary  

If they only remember “nice animation,” regenerate the weak chapters.  
If CTR is fine but retention dies mid-film, fix open / escalation / Orbit agency — don’t just re-title.
