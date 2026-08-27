---
description: Orbit cutscenes — AI Studio Veo world / stills-first / no slow-mo loops
alwaysApply: true
---

# Orbit YouTube — cutscene / picture rules

## Hard assembly rules

1. **Never reuse a cutscene** in a single video. Each B-roll / card / plate filename appears at most once.
2. **Never loop cutscenes** as a pad. Play motion once at native duration. No `stream_loop`, ping-pong, or freeze-extend. **Exception for Shorts:** intentional **first-and-last-frame** loop off the week’s open world still (same window start/end) is required — that is craft, not pad.
3. **Never slow-mo stretch** (`setpts` > 1×) to fill VO.
4. **Stills-first economy (27 Aug 2026):** AI Studio stills carry most of the Thursday film. Animate only **2–3** Veo Fast money shots (~8s). Do **not** pad gaps with Omni world plates, Ken Burns minutes, or freeze-extend.
5. **Exception:** Orbit character PiP may loop (character bed only).
6. Prefer vibrant, distinct scenery (planets, surfaces, telescopes, atmospheres). Avoid empty distant-galaxy / static starfield plates.
7. **No brand sting / baked like-subscribe** in the broadcast master (picture-first open · 10s Studio end hold). Older lines that required a brand intro plate are **retired**.
8. **Never animate text plates** with zoompan/Ken Burns. Title cards and chapter cards must be locked stills.

## Motion coverage (plan before generate)

Locked budget for a **7–9 min** Thursday film:

1. Stills first in AI Studio: **one open still (no Orbit)** · **two science plates** · **one Orbit reference still**.
2. Animate **2–3** money shots on **Veo Fast** (~8s; plan ~5.5–6s usable after soft tail trim if needed).
3. Optional: upgrade **one** hero to **Veo Quality** if it earns the thumb.
4. **Omni only** when Orbit must move (1–2 scenes). Never Omni the whole film / never ~8–10 Omni plates per minute.
5. If coverage is short: add another **unique still** or one more Veo Fast take — never stretch, loop, or freeze-pad.

## Generation guards (default CG path)

1. **Home: Google AI Studio.** World = **Veo**. Orbit motion = **Omni only**. No Kling unless Ben lifts that. Not ElevenLabs Image & Video. Not Seedance.
2. World plates: **no Orbit** on the open still / science boards. Orbit identity still only for Orbit beats.
3. When animating Orbit: start frame + identity ASSET = canonical Orbit. Abort if non-Orbit refs bind. Forbid **Eiffel Tower / Paris / architectural blueprints / parchment schematics**.
4. Prompt lock: no readable text / logos / UI; **SILENT PICTURE ONLY**; mute/strip Veo baked audio; British VO mixed in edit from ElevenLabs.
5. Spot-check first ~1s and last ~2s; quarantine rejects.

## Legacy

Europa / Neutron Omni-per-minute builders and ElevenLabs Omni / in-app Veo Playwright scripts (`_generate_omni_*.py`) are legacy. Do not use as the default for new episodes.

## Lessons

- JWST: slow-mo stretch was wrong; **1× motion** is correct — but the 27 Aug lock is **stills-first + few Veo money shots**, not “generate 75–100 clips.”
- Neutron / Europa: Omni-the-whole-film taught character QA; it is **not** the gen budget going forward.

Builders reference: `OMNI_LONGFORM_PLAYBOOK.md`, `orbit_gemini_veo.py`, `orbit-omni-longform-playbook.mdc`.
