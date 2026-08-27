---
description: Lock ElevenLabs to British VO only — CG is AI Studio Veo/Omni
alwaysApply: true
---

# Orbit YouTube — voiceover lock (British) + CG split

## VO — ElevenLabs only (locked)

When generating or regenerating any Orbit **narration**:

1. **Always use** voice **Ben Orbit Narrator** — Instant Voice Clone of Ben’s British accent.
2. **Voice ID (locked):** `kDch6ACCIpqgQ0NsU9kk`
3. **Never** substitute a stock library voice, US accent, or a different clone without an explicit user request to change the channel voice.
4. Prefer **British** spelling/pronunciation in scripts and SSML notes (`civilisation`, FAIR-mee for Fermi, etc.).
5. Current production settings (V003/V004 lock): model `eleven_v3` · stability `0.34` · similarity `0.78` · style `0.42` · speed `1.04` · speaker boost on.
6. Shared constant: `04_Audio/tools/orbit_voice.py` — import from there in new VO scripts.

Target character: warm, articulate British educational narrator — calm authority, cinematic curiosity, restrained mystery. Never theatrical / trailer-like.

## CG — Google AI Studio (Veo world / Omni Orbit-only)

**Default picture path:** Google AI Studio — **Veo** for world plates; **Omni only** when Orbit must be animated. Helpers may use `04_Audio/tools/orbit_gemini_veo.py`.

- CG clips must be **silent picture** (or ambience only) — **no dialogue, no narration, no VO** in the video model.
- Mute / strip Veo baked audio so it does not fight the VO (`CG_SILENT_AUDIO_BLOCK` / `generate_audio=False` + strip on download).
- Channel narration is mixed later from **Ben Orbit Narrator** (ElevenLabs TTS) only.
- Do **not** Omni the whole Thursday film. Do **not** use Kling, ElevenLabs Image & Video, or Seedance for new CG.
- Never treat Veo/Omni native speech as usable VO.

See also: `.cursor/rules/orbit-gemini-veo-cg.mdc` · `orbit-omni-longform-playbook.mdc`
