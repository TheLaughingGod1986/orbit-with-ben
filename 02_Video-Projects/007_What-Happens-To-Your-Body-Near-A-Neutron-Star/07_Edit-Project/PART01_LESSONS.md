# Neutron Star Part 01 — lessons

**Part 01 LOCKED (Ben UAT 17 Aug 2026):** `07_Edit-Project/parts/neutron_star_part-01_cursor_rough_v11.mp4` (~70.83s). Music + VO stay. ~95%. Carry lessons into Part 02 — do not silently regress.

## Locked — v11 hang scale + going-forward interaction (17 Aug 2026)

Ben on v10: music is locked (feels professional). Animation ~90–95%. Last blocking miss: VO says **tiny orange figure** and Orbit was still a foreground hero at ~0:07. Identity is good — do not redesign him.

**Fix shipped in v11:** keep the on-model v10 hang take; **reframe** to an EWS (tiny in the dark) with a slow push so he comes toward camera without becoming a CU. Omni I2V grows him even from a 56px start — do not trust I2V for scale; reframe if needed.

**Going forward (Part 02+):** less static hover-looking-around. Orbit should interact with the scene (bank, skim, tumble, stretch). Hang-in-the-dark is the exception.

---

## Earlier lock — v10 four UAT rejects (17 Aug 2026)

Ben paused v09 at four places. One v10 assemble covers all four. VO + continuous score stay.

| t | Plate | Reject | Fix |
|---|---|---|---|
| **0:07** | **01** hang | On-model but a **left-third hero**. VO says tiny orange figure. | New tiny composition start (`starts_v10/01_hang_tiny.png`, 56px). Station hold, no amateur spin. I2V still grew him (~30% of frame after one Flow retry) — identity OK, scale still bigger than 80–120px. |
| **0:25** | **03** tumble + **04** tidal | **Two faces** on the turn (visor toward camera + visor toward the star). | Regen 03 from an orange-back start; 04 from a pre-stretched one-visor line. One face; back is orange. |
| **0:54** | **08** living giant | **Four orange appendages** / Orbit leaked onto “This began as a giant.” | Regen 08 as living giant, **ZERO Orbit**. |
| **1:01** | **09** supernova | Orbit + leftover neutron star on the supernova line. | Regen 09 as supernova wall of ejecta, **ZERO Orbit**. API 429 → Flow backup. |

Do **not** I2V acting plates from the full-frame identity still. Hang start must already be tiny — `01_hang_hold.png` locks him huge.

Do not start Part 02 until Ben passes.

---

## Earlier lock — v09 hang motion (17 Aug 2026)

Ben UAT on v08: first **~5s of the hang is the keeper**. After that, Orbit’s animation turned into an amateur spin/orbit (flame-jet fly-around), not a finished-film station hold.

**Fix:** regen **plate 01 only** as HOLD STATION (visor stays facing camera, 1cm hover, no rotate/orbit/fly). Reuse v08 plates 02–10. VO + continuous score stay.

Start frame = keeper frame from the v08 hang (`parts/starts_v08/01_hang_hold.png`). Gemini API 429 (prepaid depleted) → Flow Playwright backup.

Do not start Part 02 until Ben passes.

---

## Earlier lock — v08 (17 Aug 2026)

Ben UAT on the v07 cut at ~0:05: film is great, but (1) dense little white spots on black — keep clear vacuum, main distant star + Orbit only; (2) this Orbit is a cheap knockoff — missing the full face, looks like a different character. Expressions may change; identity must not.

Canonical face = **black visor faceplate + cream eyes with pupils** (no cartoon mouth redesign). Knockoff = eyes on a blank orange ball / glowing yellow belly / missing arms.

Start frames now strip the identity still's starfield. Regen via Gemini Omni API only (Flow backup was adding star-noise and off-model Orbit).

Do not start Part 02 until Ben passes.

---

## Earlier lock — v06 (17 Aug 2026)

Ben UAT on `neutron_star_part-01_cursor_rough_v05.mp4`:

1. **VO stays.** Do not regen Ben Orbit Narrator.
2. **One face.** If Orbit turns, we see the solid orange back — never a second visor or eyes on the rear (same reject as twins).
3. **No formula approach.** Do not repeat Orbit-in-a-corner + destination opposite + fly toward it. That template made the minute feel samey and not like the film.
4. **Picture follows the line.** Tear → stretch. Light bends into a ring → the ring is the picture. Began as a giant → a living giant star. Ordinary dies → the star itself goes wrong.
5. **Do not I2V acting plates from the full-frame identity still.** It parks Orbit as a foreground hero and stamps a visor on every side. Attach a composition start frame.

Plate 01 tiny-hang (`*_cursor_v05.mp4`) kept. Plates 02–10 regenerated as `*_cursor_v06.mp4`.

**Music (v07):** Omni native beds restart every ~8s plate — that read as the score cutting. Mix a **single continuous underscore** under VO (`05_Music/neutron_star_part01_score_bed_v01.mp3`, 76s). Duck it under narration. Keep Omni SFX as quiet texture only.

**Look (v08):** Clean vacuum (near-black, one distant star — not a field of white specks). Canonical Orbit only — black visor is the face, cream eyes, stubby arms, small underside glow. Knockoff glowing-belly / missing-visor Orbit = regen.

Rules also locked in `.cursor/rules/orbit-omni-section-qa.mdc` and `orbit-character-consistency.mdc`.

---

# Earlier — rough v01 (16 Aug 2026 ~23:11 BST)

## Recovered folder

`007_What-Happens-To-Your-Body-Near-A-Neutron-Star/` was **missing on disk** after the `cursor/neutron-star-007-b92d` cloud checkout (22:33 BST). The empty GitHub scaffold `007_Neutron-Star/` was left untouched.

The passed 91.1 master was restored from the local Cursor snapshot commit `e0a6443e3a30ea4c8e361d1340a1d67ca8b1a8cf` (ENGINE_STARTUP, 16 Aug ~21:43 BST) — blob `78bdb3d5…` = `01_Script/neutron_star_script_master_v01.md` (18725 bytes). Review `SCRIPT_REVIEW_v01.md` restored with it (91.1 PASS). **Not a rewrite.**

`04_Audio/tools/orbit_flow_veo_ui.py` was also missing after the same checkout and was restored from that snapshot so Flow gens could run.

## What shipped

| Asset | Path | Duration |
|-------|------|----------|
| Part 01 VO | `02_Voiceover/parts/neutron_star_part-01_vo_v01.mp3` (+ `.wav`) | **70.80s** |
| STT | `02_Voiceover/parts/neutron-star-part-01-vo-v01_transcript.txt` + `.srt` | — |
| Rough | `07_Edit-Project/parts/neutron_star_part-01_rough_v01.mp4` | **70.83s** |
| Open 15s | `07_Edit-Project/parts/neutron_star_part-01_open15_v01.mp4` | **15.00s** |
| Plates JSON | `07_Edit-Project/parts/part-01_omni_plates_v01.json` | 9 prompts |
| QC stills | `_qc_p01/qc_t00_5.jpg` · `qc_t02_5.jpg` · `qc_t08.jpg` · `qc_t15.jpg` · `qc_t_last2s.jpg` | — |

Voice: ElevenLabs **Ben Orbit Narrator** `kDch6ACCIpqgQ0NsU9kk` · `eleven_v3` · lock from `04_Audio/tools/orbit_voice.py`. Auth: `~/.config/elevenlabs/api_key`.

## Exact script lines used (no rewrite)

From `01_Script/neutron_star_script_master_v01.md` — **cold open + first rise of chapter “The Corpse of a Star”** (spoken lines 3–24). Chapter card / VISUAL MUST / ORBIT ACTS / TEACH lines were **not** voiced.

```
Orbit hangs in the dark — a tiny orange figure against a star that looks almost ordinary.

Then the numbers arrive. And ordinary dies.

If you drifted toward a neutron star, the last thing your body would feel is not “falling.” Space itself would try to tear you into a line of atoms — and your eyes would see light bend into a ring before you could blink.

So what actually happens to you — second by second — as the distance closes?

What would you see?
What would you feel?
And at what point does “you” stop being a useful word?

This began as a giant.

A star many times heavier than our Sun burned through its life too fast, too hot, too hungry. When the fuel in its heart ran out, the core collapsed. The outer layers blasted away in a supernova — a brief, furious goodbye.

What remained was not ash. What remained was an argument gravity almost won.
```

162 words · VO 70.80s · inside the 60–80s part window. Intensity: declare (ordinary dies / tear / ring) → assess (second by second / see / feel) → isolate (you stops being a useful word) → rise (argument gravity almost won). Last beat rises.

Stopped **before** “Orbit drifts closer and the star refuses to get bigger…” (next chapter beat = Part 02+).

## STT of the VO (Scribe)

> Orbit hangs in the dark, a tiny orange figure against a star that looks almost ordinary. Then the numbers arrive and ordinary dies. If you drifted toward a neutron star, the last thing your body would feel is not falling. Space itself would try to tear you into a line of atoms, and your eyes would see light bend into a ring before you could blink. So what actually happens to you second by second as the distance closes? What would you see? What would you feel? And at what point does you stop being a useful word? This began as a giant. A star many times heavier than our sun burned through its life too fast, too hot, too hungry. When the fuel in its heart ran out, the core collapsed. The outer layers blasted away in a supernova, a brief, furious goodbye. What remained was not ash. What remained was an argument gravity almost won

Word-timed SRT: `02_Voiceover/parts/neutron-star-part-01-vo-v01.srt`  
Last cue ends **00:01:10,760**.

## Picture-first open — YES

| t | Frame | Orbit? | Logo/title? |
|---|-------|--------|-------------|
| 0.5s | `_qc_p01/qc_t00_5.jpg` | **No** — strange compact star only | No |
| 2.5s | `_qc_p01/qc_t02_5.jpg` | **No** | No |
| 8.0s | `_qc_p01/qc_t08.jpg` | **Entering** from frame left, in-scene | No |
| 15s | `_qc_p01/qc_t15.jpg` | Yes — cream eyes + pupils, one underside glow | No |
| last 2s | `_qc_p01/qc_t_last2s.jpg` | Yes — facing remnant, energy up | No |

VO starts at **0s** over plate 01 (picture-first is visual, not a silent pad). No brand sting. No baked like/subscribe. No `/go/` (this minute names no product).

## Plates (Omni Flash via Flow Ultra)

Engine: Google Flow · **Omni Flash** · 8s · 16:9 · signed-in Playwright profile `~/code/youtube/.playwright-aistudio-profile` (ULTRA).  
All **9/9 gens succeeded**. Unique SHA256 each. No freeze-pad.

| # | File | Orbit | VO idea |
|---|------|-------|---------|
| 01 | `omni_p01_01_almost-ordinary-star_v01.mp4` | no | almost-ordinary star |
| 02 | `omni_p01_02_orbit-banks-into-frame_v01.mp4` | yes | tiny orange figure |
| 03 | `omni_p01_03_tide-tears-a-line_v01.mp4` | yes | tear into a line of atoms |
| 04 | `omni_p01_04_light-bends-into-a-ring_v01.mp4` | yes | light bend into a ring |
| 05 | `omni_p01_05_second-by-second-close_v01.mp4` | yes | second by second / distance closes |
| 06 | `omni_p01_06_see-feel-you-ends_v01.mp4` | yes | see / feel / you stops |
| 07 | `omni_p01_07_it-began-as-a-giant_v01.mp4` | yes | began as a giant / supernova |
| 08 | `omni_p01_08_argument-gravity-almost-won_v01.mp4` | yes | not ash / gravity almost won |
| 09 | `omni_p01_09_compact-fierce-wrong_v01.mp4` | yes | rise hold |

Join: **xfade 0.12s + acrossfade**. Picture 71.04s ≥ VO 70.80s. Omni SFX under VO at 0.22.

## Ben UAT notes (do not silently ship)

1. Flow **x1 click failed** — chip stayed `Video · 8s crop_16_9 x2`. We downloaded one 8s file per prompt; possible unused twin exists in the Flow project.
2. Plate 03 may show **flame thrusters** vs locked underside-glow-only. Regen if Ben rejects.
3. ~15s still may show tiny **body lettering** (HUD reject if readable). Spot in UAT.
4. Agent Instructions field was missing in Flow (same Europa warning) — identity still attached via reference image.
5. Whole-film target is now **7–9 min** (16 Aug lock). This minute used the passed 91.1 script’s cold open + first rise only.

## Not done (correct)

- No YouTube upload
- No Part 02
- Europa / Last Star / JWST / live listings not touched
- Auditor handoff is for the parent, not this job
