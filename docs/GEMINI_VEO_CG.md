# Orbit CG — Google AI Studio Veo UI (Ultra)

**Locked:** 2026-08-06  
**CG (default):** Google AI Studio Veo via Playwright (`orbit_aistudio_veo_ui.py`) using **Google One → AI Ultra**  
**CG (fallback only):** Gemini API key via `orbit_gemini_veo.py` — billed separately; avoid for routine work  
**VO:** ElevenLabs TTS — Ben Orbit Narrator only (unchanged)

## Why Ultra UI (not API)

Google One AI Ultra boosts **AI Studio web** quotas. The Gemini **API** (`GEMINI_API_KEY`) is a different billing path and is usually more expensive for episode clip volume. Automate the Studio UI so Ultra applies.

ElevenLabs Image & Video remains banned for CG (cost, Explore/Eiffel, American speech).

## One-time setup

```bash
cd 04_Audio/tools
# venv optional but recommended
pip install playwright
playwright install chromium

# Headed login with the Ultra Google account — saves cookies to profile
python3 orbit_aistudio_veo_ui.py --login
```

Profile default: `~/code/youtube/.playwright-aistudio-profile`  
Override: `export ORBIT_AISTUDIO_PROFILE=/path/to/profile`

## Generate

```bash
# Probe one silent Orbit clip (Ultra UI)
python3 04_Audio/tools/orbit_aistudio_veo_ui.py --probe

# Custom scene
python3 04_Audio/tools/orbit_aistudio_veo_ui.py \
  --prompt "Orbit stands on Europa ice, cream eyes wide, Jupiter huge in sky" \
  --out /tmp/europa_orbit.mp4

# Episode beats (template)
python3 02_Video-Projects/_template_NNN_Episode-Slug/07_Edit-Project/_generate_veo_from_beats.py \
  --beats beats.json --out-dir ../04_Generated-Clips/01_Raw --limit 1
```

Always strip audio (helper does this). Mix British VO from ElevenLabs in the edit.

## Debug

```bash
python3 04_Audio/tools/orbit_aistudio_veo_ui.py --dump-ui /tmp/aistudio_dump --headed
python3 04_Audio/tools/orbit_aistudio_veo_ui.py --dry-run --probe
```

## Optional API fallback

Only if the UI automation is broken:

```bash
export GEMINI_API_KEY=...
python3 04_Audio/tools/orbit_gemini_veo.py --probe
# or
python3 …/_generate_veo_from_beats.py --engine api --beats … --out-dir …
```

## Rules

- `.cursor/rules/orbit-gemini-veo-cg.mdc` (CG path lock)
- `.cursor/rules/orbit-british-vo-lock.mdc`
- Growth gate before spend: script ≥90 + pre-build vidIQ

## Legacy

`_generate_omni_*.py` Playwright EL Image-Video scripts — do not use for new episodes.
