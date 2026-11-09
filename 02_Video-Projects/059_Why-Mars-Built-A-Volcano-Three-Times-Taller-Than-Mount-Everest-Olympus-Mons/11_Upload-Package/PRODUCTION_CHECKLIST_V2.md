# Production checklist — Orbit With Ben (`059` Olympus Mons)

**Episode:** `059_Why-Mars-Built-A-Volcano-Three-Times-Taller-Than-Mount-Everest-Olympus-Mons` (*Why Mars Built a Volcano Three Times Taller Than Mount Everest — Olympus Mons*)  
**Date:** 2026-11-04 (refreshed in `J1955`; unlocked candidate, `FIX / topic not locked` per Chief `J1801` and `FIX / script not locked` per Chief `J1800`)  
**Script review score:** 95.8 / 100 on `v01` automated check (`1,259` spoken words), **blocked / script FIX per Chief `J1800`** (must pass fresh `review:script` ≥90 and `gate:episode` PASS after `J1800` editorial fixes, `J1956` formal Gemini `facts` pass, and `J1957` direct `MUST QUOTE` verification).

Rules in force: `AGENTS.md` · `00_Brand/Channel-Setup/FAMILIAR_DANGER_STRATEGY.md` · `THUMBNAIL_AND_TITLE_RULES.md` · `STUDIO_PLAYBOOK.md` · `docs/ORBIT_PLAYBOOK_LESSONS.md`

---

## Topic and script

- [ ] Familiar thing in danger / planetary scale (wonder, not dread). No existing public long on this subject. Signed-out exact-title competition check done (`0` collisions). Neighbour pass (`8` verified education/space videos at `1.02M–3.39M` views) completed (`J1955`). Short-first proof (`≥200` views AND `≥40%` stayed-to-watch) verified or explicitly ruled on by Chief (**currently UNMET: `0` OWB Shorts on Olympus Mons**); **Chief locks the topic** (`J1801` / `J1953`).
- [ ] Pre-build audit (`11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`) and `11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md` completed and signed off by Chief
- [ ] First 3 s of picture = the subject moving (graded unlabelled NASA/ESA orbital imagery, no Orbit, no title card, no whole planet as a Veo/Omni start frame). Concise claim-led opening sentence; concrete causal answer before `0:30`; one main question by `~0:50`; no numeric catalogue in hook; no `[CHAPTER CARD]` before `0:30` (`J1800` item 1).
- [ ] 4–6 acts told as cause and effect. The world does the science. Orbit in 1–2 beats only (after `1:00`, never in final shot).
- [ ] Picture change about every 4–6 s. Every spoken and visual claim verified via formal Gemini `facts` (`J1956` via `agy`) + direct `MUST QUOTE` check (`J1957`) (`J1802`). Teach on screen (`DATA ≥ 3` with `SCALE:`, `WHO` at first mention with complete sourced years for all 11 scientists including `Sjogren` & `Garvin` and verified portrait rights, `WHEN` animated as spoken without turning lifespans into observation dates + build-up timeline, `FACT` 2–4 `≤4` words matching spoken VO, 1 single-idea `NUMBER OBJECT` per chapter with real moving imagery between graphics; `J1800` items 2 & 3).
- [ ] One `[SUBSCRIBE BEAT]` after the first payoff (25–50%), a line ≤20 words from `templates/SUBSCRIBE_BEAT_LINES.md` (no numbers, no stock phrases, no burned-in subscribe graphic).
- [ ] No goodbye line and no second subscribe ask. The last spoken line hands off to the confirmed next film (reconcile incoming `058` and outgoing `060` Hyperion promises against actual locked air dates; `J1800` item 4).
- [ ] Runtime 7–9 min (about 1,200–1,300 spoken words)
- [ ] Fresh `npm run review:script` ≥90 · `npm run gate:episode` PASS · explicit Chief script lock (`J1953`)

## Voice and picture

- [ ] ElevenLabs `eleven_v3` "Ben Orbit Narrator" only (`04_Audio/tools/vo_take.py`, API only, never the website). Speech around −19 to −28 dB mean. Scribe word-diff check PASS. No silent stretches or stumbled/repeated phrases.
- [ ] **Vertex AI only** (never AI Studio prepaid credit): Vertex Veo for world plates; Vertex Omni (`gemini-omni-flash-preview`, location `global`) **only for Orbit**; Codex `gpt-6-astra` for per-row animated code graphics. Veo/Omni baked audio stripped.
- [ ] `scripts/picture_qa.py` PASS: no sourced MOLA colour-coded topography maps, diagrams, charts, or labelled images (`J1800` item 2). Upscale ≤2.35×.
- [ ] Picture matches every sentence (mute test). Orbit on-model. No reused cutscenes, scenery loops, slow-mo, freeze-pads, or Ken-Burns text.
- [ ] Own music bed generated via `04_Audio/tools/generate_music_bed.py` (with `Pace:` and `NOT:`), passing `scripts/music_gate.py`, plus house SFX (`scripts/sfx_kit.py level` PASS).

## Assembly

- [ ] Inputs normalised to 1920×1080 stereo (fill 16:9; feathered blur background if needed). Row times aligned to locked VO word timestamps (`align_shot_list.py`); `clip_check.py --words` PASS.
- [ ] Chapter cards wait for VO sentence to finish → **0.5–0.8 s** breath → **~0.4 s** crossfade; music continues under the card.
- [ ] **End hold (`J1800` item 4, `STUDIO_PLAYBOOK.md` §7):** moving picture holds **15–20 s** past the last VO word (end-screen space); music carries **2–3 s** past the last word then fades over **~10 s**; picture fades to black over the last **2 s**. Music covers full runtime (no silent hold).
- [ ] Mix around **−14 LUFS** with clear VO.

## Shorts (3 a week)

- [ ] 22–27 s (55–65 words). Keeper score: one question in the title and spoken line 1 (`0–2.5 s` names Mars / Olympus Mons over moving picture). No `0.5 s` pause or static zoom in `4–8 s`. Orbit not at frame 0.
- [ ] `gate_shorts_open.py check` PASS for each export. Full-length music bed under VO.
- [ ] Exact live film title on screen at 9–14 s. At most one overlay inside the 16:9 centre band (clear of 0–2 s and 9–14 s). Last 4 s loop to the opening.

## Packaging and Studio

- [ ] Title: one of the six shapes, no hashtags, series suffix, hedged claim, threat framing, or repeat title. Packaging panel (`scripts/packaging_panel.py`) + Chief decision.
- [ ] Long thumb (`THUMBNAIL_AND_TITLE_RULES.md` §2.B): 1 subject ≥⅓ frame + scale reference, no Orbit; 2–3 words in a top band (off subject, yellow hook word); HSV saturation ≥100 (target 120), near-black ≤30% (`thumb_preview.py long --score` PASS); readable at 168×94. Test & Compare B via Codex `gpt-image-2` logged in `thumb_ledger.py`.
- [ ] Description: subject line · story-beat chapters · `Sources:` line (4–6 primary papers/fact sheets) · agency credits · honest AI/sources disclosure line. **Zero `/go/` affiliate links** (retired/paused).
- [ ] Upload private with `publishAt` only after Ben's UAT watch (`jobs.py awaits`) and Chief's Final OK. Long = normal publish, Sunday 18:00 UK (no Premiere). Altered content: yes.
- [ ] Long: Test & Compare · end screen (best related long + Subscribe) · pinned comment (`update-pinned-comment.ts`) after go-public.
- [ ] Shorts: Related → the matching long · registered in `UPLOADS.json` for Buffer mirror · no pinned comment · zero `/go/`.
