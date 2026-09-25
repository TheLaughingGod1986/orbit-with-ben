---
description: Next Orbit video kickoff — Growth System v2 gate before VO/picture
alwaysApply: true
---

# Orbit — next video kickoff (Growth System v2)

**Locked next long (3 Sep 2026): 013 Moon Leaving Us at 7–9 min** in `013_Why-The-Moon-Is-Slowly-Leaving-Us` (script `moon_leaving_script_master_v01.md`, score 90.4). Neutron Star is Premiere-scheduled (`Yk1tLh23rko`). Simulation is 015. See `orbit-next-production.mdc`.

**Picture path (27 Aug 2026):** Google AI Studio — **Veo** for world plates, **Omni only** when Orbit must move. Stills first · 2–3 Veo Fast money shots. Do **not** Omni the whole film.

When the user asks to **build / start / plan the next video**, **new episode**, **next long**, or similar — **do this first**. Do not jump to VO, Veo, Omni, Seedance, or picture gen.

## Step 0 — gate (blocking)

1. Read `00_Brand/Channel-Setup/YOUTUBE_GROWTH_SYSTEM_V2.md` and `CONTENT_INTELLIGENCE_STRATEGY.md`
2. Topic score (or confirm locked topic) via `templates/TOPIC_OPPORTUNITY_SCORE.md` / `npm run intelligence:score-topics`
2b. Fill `templates/EPISODE_CLUSTER_PLAN_TEMPLATE.md` (experiential angle · 4–8 Shorts · cluster ID)
3. Pre-build vidIQ audit → project `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` from `PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md`
4. Cold-open outline: curiosity **5s** · stakes **15s** · journey **30s**
5. Chapter outline: **4–6** acts · **world does the science** · Orbit in **1–2** inquisitive / story-narrative beats only · Hook→Question→Escalation→Discovery→Payoff→Bigger question
6. Write/refine script with `[VISUAL MUST]` · `[ORBIT ACTS]` (only on those 1–2 Orbit beats) · `[TEACH]`
7. **Script reviewer ≥ 90** before any VO or picture:
   ```bash
   cd 07_Content-Ops && npm run review:script -- --file <script.md>
   ```
   Below 90 = **REJECT** — rewrite. Do not generate audio/video.
8. **Episode gate (blocking CLI)** before VO / picture gen:
   ```bash
   cd 07_Content-Ops && npm run gate:episode -- --project ../02_Video-Projects/<NNN_Slug>
   ```
   Must PASS (audit signed · script ≥90 · `[ORBIT ACTS]` / `[VISUAL MUST]` / `[TEACH]` counts).

## New episode scaffold

Copy `02_Video-Projects/_template_NNN_Episode-Slug/` → `02_Video-Projects/NNN_Your-Slug/`, then run the gate.

## Then produce (AI Studio picture economy — locked)

Follow `OMNI_LONGFORM_PLAYBOOK.md` / `orbit-omni-longform-playbook.mdc`:

1. Ben Orbit Narrator VO → AI Studio **stills first** (open world · two science · Orbit ref) → **2–3 Veo Fast** money shots (optional one Veo Quality hero) → **Omni only** for Orbit motion in 1–2 scenes → Mac assemble (mute Veo audio) → picture QA  
2. Picture-first open (3s world only) · mid-film chapter cards · soft-join · 10s last-picture hold for Studio end screens → broadcast master. No brand intro. No baked like/subscribe outro.  
3. **4–8** punch Shorts (**22–27s**) → checklist → YouTube package. Picture thumb no Orbit · exact listing title on screen · CTA that week’s Thursday id · zero `/go/`.  

Do **not** use ElevenLabs Image & Video, Seedance, or Kling for new CG. Do **not** Omni the whole Thursday film.

After shipping, refresh the next brief from Studio metrics:

```bash
cd 07_Content-Ops && npm run brief:next -- --file metrics.json --topic "Next idea"
# writes docs/NEXT_EPISODE_BRIEF.md
```

## Thumbs + social schedule (after YouTube lock)

Once the **YouTube** long (and Shorts cluster) schedule is locked:

1. **Long thumbnails:** picture + a short **SEA-style hook**. **No Orbit. No generic CTA.** Produce **3** variants; score in VidIQ. Longs: start Studio **Thumbnail ABC** (or title+thumb ABC) after upload.
2. **Short thumbs:** custom picture — **no Orbit**.
3. **Social mirror:** Meta / Threads from the **same YouTube air times**. **One unique post per Short** on Instagram, Facebook, and Threads — no remake/file/title duplicates (`orbit-social-no-duplicates.mdc`). **TikTok is paused** (account ban) until Ben lifts `TIKTOK_UPLOAD_BLOCK.json`. Never post social Shorts before the YouTube long is public.

## Defaults (documentary + cluster window)

- Runtime **7–9 min NOW** (007 Neutron Star and new longs). Expand to 15–20–30 only later with impressions + hold past ~5 min. Title one promise (no series suffix) · thumb = picture + SEA hook · experiential framing preferred
- **4–8** Shorts: open inside the question · curiosity-gap end · Related pill → that week’s Thursday long (no new Short pins) · same content cluster
- Evidence labels honest (LOW_DATA / EARLY_POSITIVE_SIGNAL) — never overfit one Short
- No dead ends: end screen · cards · long pin → another Orbit documentary; Shorts = Related pill only
- Do **not** redesign the brand

## Kickoff phrases that trigger this

“Build next video” · “Next episode” · “Start V0xx” · “New long-form” · “Growth System v2 first”

Canonical: `YOUTUBE_GROWTH_SYSTEM_V2.md` · `CONTENT_INTELLIGENCE_STRATEGY.md` · `RETENTION_AND_GROWTH_LOCKED.md` · `LONGFORM_STORY_AND_VO_PICTURE_GATE.md` · `OMNI_LONGFORM_PLAYBOOK.md` · `docs/GEMINI_VEO_CG.md`
