# Orbit CG — Google Flow Veo UI (Ultra)

**Locked:** 2026-08-06  
**CG (default):** Google Flow Veo via Playwright (`orbit_flow_veo_ui.py`) using **Google One → AI Ultra** Flow credits  
**CG (secondary):** AI Studio Veo UI (`orbit_aistudio_veo_ui.py`) — often needs a **paid Gemini API key** selected even on Ultra  
**CG (last resort):** Gemini API key via `orbit_gemini_veo.py` — billed separately; avoid for routine work  
**VO:** ElevenLabs TTS — Ben Orbit Narrator only (unchanged)

## Why Flow (not API / not AI Studio alone)

Google One AI Ultra includes **Flow** credits for Veo. Automate `labs.google/fx/tools/flow` so Ultra applies.

AI Studio’s Veo playground frequently still requires a **paid API key** in the UI (“No API key selected”) even when the ULTRA badge is visible — that path is secondary.

The Gemini **API** (`GEMINI_API_KEY`) is a different billing path and is usually more expensive for episode clip volume.

ElevenLabs Image & Video remains banned for CG (cost, Explore/Eiffel, American speech).

## One-time setup

```bash
cd 04_Audio/tools
pip install playwright
playwright install chromium   # or use channel=chrome via the helper

# Headed login with the Ultra Google account — saves cookies to profile
python3 orbit_flow_veo_ui.py --login
```

Profile default: `~/code/youtube/.playwright-aistudio-profile`  
(same Google session works for Flow + AI Studio)  
Override: `export ORBIT_FLOW_PROFILE=/path/to/profile`

Confirm the **ULTRA** badge on Flow after login.

## Generate

```bash
# Probe one silent Orbit clip (Flow Ultra)
python3 04_Audio/tools/orbit_flow_veo_ui.py --probe

# Custom scene
python3 04_Audio/tools/orbit_flow_veo_ui.py \
  --prompt "Orbit stands on Europa ice, cream eyes wide, Jupiter huge in sky" \
  --out /tmp/europa_orbit.mp4

# Episode beats (template — engine=flow default)
python3 02_Video-Projects/_template_NNN_Episode-Slug/07_Edit-Project/_generate_veo_from_beats.py \
  --beats beats.json --out-dir ../04_Generated-Clips/01_Raw --limit 1
```

Helper flow: new project → Settings (Never confirm + **Veo 3.1 - Fast** + 16:9) → Agent Instruction identity lock → **attach Orbit ref in the prompt** (not library-only) → image-to-video prompt → Create → poll media → download → **strip audio**.

**Character QA (blocking):** reject clips with white chest disc, two-sphere head/body split, ear rings/headphones, legs, or missing cream circular eyes — regenerate; do not ship near-miss mascots.

## Debug

```bash
python3 04_Audio/tools/orbit_flow_veo_ui.py --dump-ui /tmp/flow_dump --headed
python3 04_Audio/tools/orbit_flow_veo_ui.py --dry-run --probe
```

## Secondary / fallback

```bash
# AI Studio UI (may require paid API key in Playground)
python3 04_Audio/tools/orbit_aistudio_veo_ui.py --probe

# API last resort
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
