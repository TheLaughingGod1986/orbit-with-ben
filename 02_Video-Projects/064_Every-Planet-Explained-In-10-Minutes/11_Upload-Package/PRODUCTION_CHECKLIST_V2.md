# Production checklist — Orbit With Ben

**Episode:** `064_Every-Planet-Explained-In-10-Minutes` (`OWB:064`)  
**Date:** `2026-11-24` (`J3544` / `J3020`)  
**Script review score:** `91.6` / 100 (must be 90 or more)

Rules: `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` · `FAMILIAR_DANGER_STRATEGY.md` · `THUMBNAIL_AND_TITLE_RULES.md`

---

## Topic and script

- [x] Familiar thing in danger / approved format test (`J3011`). No existing public long on this subject. Competition check done (`J2863` / `J2875`). Ben picked it (*"Lock it."*, 17 Nov 2026).
- [x] Pre-build vidIQ audit signed off (`11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`)
- [x] First 3 s of picture = Mercury (`PIA19411` rotating global colour mosaic). Sentence one = hook question (17 expanded words, ~7.03 s at 145 wpm, < 8 s); sentence two = immediate spoken answer (~11.17 s); payoff contrast (−180 °C) by ~25 s.
- [x] 8 ordered planet sections (`Mercury` → `Neptune`, `7` chapter cards + cold open) told as cause and effect with a recurring building Historical Exploration Timeline (1610–2024). The world does the science. Orbit in 1–2 beats only (`2` `[ORBIT ACTS]` beats).
- [x] Picture change about every 4–6 s (`≤4 s` in first 30 s, strictly line-matched). Source ledger corrected for v04 under `J3539` FIX review and `J3520` Chief ruling; fresh Gemini facts output preserved in `jobs/reviews/J3544/`; independent direct-quote lock review (`J3545`) remains required. Historical v01/v02/v03 passes do not lock v04. No goodbye line. The last line hands off to the next film (`034` Pluto).
- [x] One `[SUBSCRIBE BEAT]` after the first payoff (`36%` through, `15` words: Line 4 *"We make one of these every week. Subscribing is how the next one finds you."*, not used in the last four longs `031`–`034`)
- [x] Runtime ~9–10 min (`1,296` spoken words / `1,341` whitespace tokens / `8,471` spoken characters across 8 planets + `18 s` end hold; est. `606.28 s`)
- [x] `npm run review:script` 90 or more (`91.6 / 100`) · `npm run gate:episode --require-checklist` PASS (explicit v04 path)

## Voice and picture

- [ ] Ben Orbit Narrator only. Speech around −19 to −28 dB mean. No silent stretches.
- [ ] AI Studio: Veo world, Omni only for Orbit. Veo/Omni audio stripped.
- [ ] Picture matches every sentence (mute test). Orbit on-model (one face, cream eyes with pupils, one underside glow).
- [ ] No reused cutscenes, scenery loops, slow-mo, freeze-pads or Ken-Burns text

## Assembly

- [ ] Inputs normalised to 1920×1080 stereo. A/V durations match after concat.
- [ ] Remint = picture only (original part audio kept)
- [ ] Chapter cards: soft starfield, about 1.5 s breath lead-in, music continues under the card
- [ ] End hold 15–20 s, music fades over about 10 s, picture fades to black over the last 2 s. No silent hold.
- [ ] Ocean/shore POV: no Earth globe in the sky. One Earth + one Moon at most (mid-plate frame checked).
- [ ] 4-second lower-right subscribe cue under the beat, with the picture still moving
- [ ] Watched once on a phone with the sound on

## Shorts (3 a week)

- [ ] 22–27 s. First-two-seconds rules. Orbit not at frame 0.
- [ ] `gate_shorts_open.py check` PASS for each export
- [ ] Exact live film title on screen at 9–14 s. Last 4 s loop to the opening.

## Packaging and Studio

- [ ] Title: one of the six shapes. No hashtags, suffix, hedged claim or repeat title.
- [ ] Thumbs: 2–4 words, readable at 168×94 (`thumb_preview.py`), add to the title, no Orbit. 3 variants for the long.
- [ ] Description: real subject first · chapters · sources · affiliate only if named in the film
- [ ] Upload private with `publishAt`. Long = normal publish, Sunday 18:00 UK (no Premiere). Altered content: yes.
- [ ] Long: Test & Compare · end screen (best related long + Subscribe) · captions auto-synced · pinned comment posted with `update-pinned-comment.ts --create` and pinned in Studio
- [ ] Shorts: Related → the long each promotes · no new pin · zero `/go/`

**Ship only when every box is ticked and Ben has signed off.**

Current candidate: v04 SHA-256 `556f3c8df68ee3cd1420ef03b8cedc04a7f0f79463d98ebf4d3d5e5753408db8`; not locked. Counts and timing basis: `01_Script/SCRIPT_NOTES_v04.md`.
