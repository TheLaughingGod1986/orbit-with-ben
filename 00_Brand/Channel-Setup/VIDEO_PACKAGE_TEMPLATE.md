# Video package template — Orbit with Ben

Use this checklist for every long-form (and its Shorts + distribution cluster).

Canonical publish rules: `PUBLISHING_AND_SHORTS_STRATEGY.md`  
**Pre-build (blocking):** `PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md` → project `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`  
Story / VO–picture: `LONGFORM_STORY_AND_VO_PICTURE_GATE.md`

## 0. Pre-build vidIQ audit — **before script lock / VO / gen**

Goal: **views + whole-video watch**, shaped by data.

- [ ] Keyword research (primary + secondary + Shorts terms)
- [ ] Title ABC scored ≥ **90** (target **95+**); fearbait rejected even if higher
- [ ] Outliers reviewed — steal **structure**, keep Orbit wonder
- [ ] Data → chapter list / hook / thumb decisions written down
- [ ] Retention plan (hook → chapter turns → payoff) filled
- [ ] Audit signed off

```bash
python3 04_Audio/tools/vidiq_title_score_sheet.py --project-dir 02_Video-Projects/<NN_Slug>
# optional channel refresh:
# python3 00_Brand/Channel-Setup/audits/_pull_vidiq_full_audit.py
```

## 1. Title options (3–5) — lock from audit

Formula: Question + Mystery + Emotion. Mobile-scannable. Include `| Orbit's Cosmic Journey`.

- A:
- B:
- C:

- [ ] Score sheet filled (`11_Upload-Package/Titles/VIDIQ_TITLE_SCORE_SHEET.md`)
- [ ] Winner ≥ **90** (target **95+**)
- [ ] Keyword stack noted for description / tags
- [ ] Thumbnail Preview checked on mobile + suggested

## 2. Thumbnail concepts (A/B/C)

For each: one idea · Orbit yes/no · text ≤ ~4 words · colour note · **matches locked title promise**.

- A:
- B:
- C:

## 3. Full script (10–12 min · chapter story)

Canonical: `LONGFORM_STORY_AND_VO_PICTURE_GATE.md`

- [ ] Target **10–12 min** VO (do not pad)
- [ ] **4–6 named chapters**, each with one teach-point
- [ ] Hook (0–20s) — mystery claim on screen
- [ ] Every scene has `[VISUAL MUST: …]` + `[TEACH: …]`
- [ ] Picture shows/acts the VO — no generic filler under specific lines
- [ ] Ending — wonder takeaway + soft return CTA + Orbit reflection
- [ ] Chapter cards at each chapter start (locked stills)

Tone: mystery + educational + Pixar-warm. Never conspiratorial.

## 4. Scene breakdown

| # | Dur | Visual | Camera | Orbit | AI prompt |
|---|-----|--------|--------|-------|-----------|
| 1 | | | | | |

## 5. AI video prompts

Include mandatory Orbit consistency block when Orbit is on screen (see repo README).

## 6. Voice instructions

- **Model (locked):** Ben Orbit Narrator — British IVC · `kDch6ACCIpqgQ0NsU9kk`  
  (`04_Audio/tools/orbit_voice.py` · never swap for a US/stock voice)
- Pace · warmth · emphasis words · pause marks  
- British spelling / pronunciation notes where needed  

After master VO:

```bash
python3 04_Audio/tools/transcribe_vo.py \
  --audio 02_Video-Projects/<NN_Slug>/02_Voiceover/05_Master/<master>.mp3 \
  --out-dir 02_Video-Projects/<NN_Slug>/02_Voiceover/06_Captions
```

- [ ] Captions `.srt` + transcript written

## 7. Editing plan

Music bed · SFX · captions · transitions · end screen · cards · chapters

Generate from script cues (dry-run first; `--generate` spends ElevenLabs credits):

```bash
python3 04_Audio/tools/generate_sfx_from_script.py \
  --script 02_Video-Projects/<NN_Slug>/01_Script/<slug>_script_master_v01.md \
  --out-dir 02_Video-Projects/<NN_Slug>/06_Sound-Effects/generated_v01

python3 04_Audio/tools/generate_music_bed.py \
  --project <slug> \
  --script 02_Video-Projects/<NN_Slug>/01_Script/<slug>_script_master_v01.md \
  --out-dir 02_Video-Projects/<NN_Slug>/05_Music \
  --length-ms 180000
```

- [ ] SFX manifest reviewed (unique `[SFX:]` cues)
- [ ] Music bed plan / file in `05_Music/`
- [ ] Captions synced in edit

## 8. SEO metadata

- Primary title  
- Description (hook + summary + chapters + soft CTA)  
- Tags  
- Playlist pillar  

## 9. Shorts idea map (5–7) — mandatory

Each Short = standalone mini-doc. Hook ≤2s. Soft curiosity ending. No random cuts.

| # | Day/time UK | Working title | Single idea | Soft ending |
|---|-------------|---------------|-------------|-------------|
| 1 | Thu 21:00 | | Strongest hook | |
| 2 | Fri 12:30 | | | |
| 3 | Sat 12:30 | | | |
| 4 | Sun 12:30 | | | |
| 5 | Mon 12:30 | | | |
| 6 | Tue 12:30 | | | |
| 7 | Wed 12:30 *(opt)* | | | |

## 10. Distribution flywheel

Copy `CONTENT_FLYWHEEL_TEMPLATE.md` → `11_Distribution/CONTENT_FLYWHEEL.md` and fill:

- [ ] 5–7 Shorts scheduled (pillar public first)
- [ ] 3 X · 3 Threads · 2 LinkedIn · 3 Facebook
- [ ] 1 Reddit discussion
- [ ] 1 Community poll · 1 Community image
- [ ] Email / blog stubs *(future)*

## Ship gate

- [ ] Brand voice intact  
- [ ] Science sources noted  
- [ ] Orbit used as guide, not wallpaper  
- [ ] vidIQ title locked (≥90) + thumb previewed  
- [ ] Thumb readable at mobile size  
- [ ] Long scheduled Thu **19:00** UK before any Short goes public  
- [ ] Uploaded via **Data API package** (`07_Content-Ops` → `npm run youtube:package`) — not Studio as primary  
- [ ] Studio finish done: ABC Test & Compare · pin comment · end screen/cards  
- [ ] Short #1 Related video → this Thursday long (desktop Studio; required). Pin optional if Related is set.  
- [ ] Soft CTAs only (no ad voice)  
- [ ] Uploaded to `@OrbitWithBen` only  
- [ ] `RELEASE_WEEK_CHECKLIST.md` ready for ship week  

Audio/packaging CLIs: `04_Audio/tools/README.md`  
YouTube package upload: `07_Content-Ops/docs/YOUTUBE_PACKAGE_UPLOAD.md`  
