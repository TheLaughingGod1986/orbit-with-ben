# Orbit CG — Google AI Studio (Veo world / Omni Orbit-only)

**Locked:** 2026-08-27 (Ben via Video Creator)  
**Home:** Google AI Studio  
**WORLD plates:** Veo (Fast default; one Quality hero only if it earns the thumb)  
**Orbit motion:** Omni **only** when the orange robot must be animated — never Omni the whole film  
**VO:** ElevenLabs TTS — Ben Orbit Narrator only (unchanged)

## Why

Running every Thursday minute through Omni Flash (~8–10 plates per VO minute) was the expensive old habit. The lock is **stills first** → **2–3 Veo Fast money shots** for the world → Omni only for 1–2 Orbit beats. Mute Veo baked audio so it does not fight the VO.

ElevenLabs Image & Video and Seedance stay retired for new CG. **No Kling** unless Ben later says volume outgrew Google.

## Economy (per Thursday film)

1. AI Studio stills: one open world (no Orbit) · two science plates · one Orbit reference still  
2. Animate 2–3 money shots on **Veo Fast** (~8s); first-and-last-frame on the open still for Shorts  
3. Optional one **Veo Quality** upgrade if it earns the thumb  
4. **Omni only** for Orbit motion in inquisitive / story-narrative scenes  
5. Assemble on the Mac (VO · captions · last card · picture-first open)

## Setup (API helpers)

When automating Veo outside the Studio UI:

1. Create an API key: https://aistudio.google.com/apikey  
2. Export or put in `07_Edit-Project/.env` / `04_Audio/tools/.env`:

```bash
export GEMINI_API_KEY=...
# optional
# export ORBIT_VEO_MODEL=veo-3.1-fast-generate-preview
```

3. Install client if needed: `pip install google-genai`

```bash
# Probe one silent clip
python3 04_Audio/tools/orbit_gemini_veo.py --probe
```

Always strip audio (helper does this). Mix British VO from ElevenLabs in the edit.

## Rules

- `.cursor/rules/orbit-gemini-veo-cg.mdc`
- `.cursor/rules/orbit-omni-longform-playbook.mdc`
- `.cursor/rules/orbit-british-vo-lock.mdc`
- `00_Brand/Channel-Setup/OMNI_LONGFORM_PLAYBOOK.md`
- Growth gate before spend: script ≥90 + pre-build vidIQ

## Legacy

Europa / Neutron Omni-per-minute builders and `_generate_omni_*.py` Playwright EL Image-Video scripts — do not use as the default for new episodes.
