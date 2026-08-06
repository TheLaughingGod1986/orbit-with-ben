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
pip install playwright
playwright install chromium

# Headed login with the Ultra Google account — saves cookies to profile
python3 orbit_aistudio_veo_ui.py --login
```

Profile default: `~/code/youtube/.playwright-aistudio-profile`  
Override: `export ORBIT_AISTUDIO_PROFILE=/path/to/profile`

### Paid API key (required for Veo)

Google One **Ultra** signs you into Studio, but **Veo GenerateVideo still needs a paid Gemini API key selected** in the Playground (button: “No API key selected”). Ultra alone does not unlock Veo.

1. Open https://aistudio.google.com/api-keys (same Ultra account)
2. **Create API key** in an imported project
3. **Set up billing** / link a paid project (Cloud billing)
4. In Veo Playground, open the key control and **select that paid key**
5. Re-run `orbit_aistudio_veo_ui.py --probe`

If Create key says “request is suspicious”, finish key + billing **manually** in the browser (automation is often blocked there).

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
