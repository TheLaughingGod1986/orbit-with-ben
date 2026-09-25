---
description: Orbit mascot must stay the same character across every shot (next videos + regenerations)
alwaysApply: true
---

# Orbit character consistency

Orbit is a **character**, not a vibe. Across an episode (and channel-wide), the body/face system stays locked. Expressions and motion change; identity does not.

## Canonical Orbit (lock)

- Solid **matte orange** rounded floating robot (continuous orange head + torso)
- **No legs** — hover with soft underside glow only
- Large **black curved visor** — that visor **is the face**. Two cream/amber expressive circular eyes with dark pupils. Expression through the eyes. Do not replace him with eyes painted on a blank orange ball.
- Short stubby orange arms with simple dark **three-finger** hands
- Single antenna with glowing bulb tip
- Small cyan + red chest lights OK
- Soft underside hover glow only — **not** a glowing yellow belly / lightbulb body
- Full-CG **in the shot** (not a cutout overlay as the body lock)

## Hard rejects (regen / quarantine)

Treat as a different mascot — do not ship:

- **Two Orbits / twin / clone / reflection duplicate** in one shot (Europa Part 01 QA — always reject)
- **Two faces** — second rear/side black visor or mirrored eyes on the back of the sphere (Europa Part 02 · Neutron Star Part 01). If Orbit turns, the back is solid matte orange — never a second face.
- Legs / lander legs / humanoid legs
- White / cream belly or white helmet / mustard–charcoal two-tone primary body
- Blank visor, neon-outline-only face, slit LEDs, socket ring-eyes, cyan crescent eyes
- **Knockoff Orbit** — missing visor faceplate, missing arms, glowing yellow lower-third belly, cheap sphere with only eyes. Treat as a different mascot. Regen.
- **Blank solid white eyes with no pupils/dots** (Europa Part 02 QA — reject)
- HUD / lettering on face or body (“Orbit”, etc.)
- Detached floating white arms, fin-stub-only arms as a redesign
- Missing Orbit entirely

## Soft drift (this JWST publish only)

Slight eye/mouth/proportion drift on an otherwise orange cream-eye floater may ship for Video 004 if time-boxed. **Do not** treat that as the standard for the next episode.

## Next episode — hard lock (Ben 2026-08-04)

**One Orbit model for the whole video.** Every character clip must be the same canonical Orbit — not a mix of near-matches. If a take drifts (different eyes, body split, visor shape, arms), reject and regen from the locked reference. Prefer fewer on-model Orbit shots + unique scenery beds over many off-model Orbits.

## Canonical still (file lock)

- **Use:** `01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-v01.png` (+ `…-16x9-v01.png` for widescreen). Folder/filename are legacy — **CG home is Google AI Studio** (Veo for world · **Omni only** when Orbit must move). Not Seedance. Not Kling.
- **Never use:** anything under `05_Seedance-References/_Rejected/` — especially former `orbit-cg-canonical-*` (white chest disc / two-sphere / headphone redesign).

## Next-video generation rules

1. **Orbit dosage:** he appears in **1–2** inquisitive / story-narrative scenes per film only. World plates have **no Orbit**.
2. When animating Orbit (**Omni only**): attach the Orbit identity still (`orbit-seedance-reference-16x9-v01.png`) + composition start frame and the identity lock text. Do not generate with Seedance.
3. Generate → **character QA frame check** before staging into Selected / master.
4. Prefer fewer on-model takes over dense off-model coverage — the economy already caps Orbit scenes.
5. If VO needs more picture: use world stills / Veo world money shots — never “fix” with off-model Orbit or Omni world B-roll.
6. Document rejects in `ORBIT_CHARACTER_QA_REJECT.json` (or episode equivalent).

## Exception

Orbit character PiP bed may loop (character bed only) — scenery/cutscenes still follow `orbit-cutscene-no-reuse`.
