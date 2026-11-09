# Production checklist — Orbit With Ben

**Episode:** `034` — *Why Pluto's Frozen Heart Has Zero Craters*  
**Date:** 2026-11-04  
**Script review score:** 95.8 / 100 (must be 90 or more)

Rules: `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` · `FAMILIAR_DANGER_STRATEGY.md` · `THUMBNAIL_AND_TITLE_RULES.md`

---

## Topic and script

- [x] Familiar thing in danger. No existing public long on this subject. Competition check done (12 neighbours at 1.03M–21.20M views, led by NASA's 21.20M documentary and Astrum's 18.43M Pluto film). Rule-E GO (`J2149`).
- [x] Pre-build vidIQ audit signed off
- [x] First 3 s of picture = the danger. Sentence one = the promise. Payoff named by 30 s.
- [x] 4–6 acts told as cause and effect. The world does the science. Orbit in 1–2 beats only.
- [x] Picture change about every 4–6 s. Every number sourced. No goodbye line. The last line hands off to the next film.
- [x] One `[SUBSCRIBE BEAT]` after the first payoff (25–50%), a line from `templates/SUBSCRIBE_BEAT_LINES.md` not used in the last four longs (Line 9, 14 words at 42%)
- [x] Runtime 8–9 min (about 1,200–1,300 words: 1,291 spoken words in `v02`)
- [x] `npm run review:script` 90 or more (95.8/100) · `npm run gate:episode` PASS

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

## Shorts (2 per new OWB long, Ben 4 Nov 2026)

- [ ] 22–27 s (Test A opening Short excepted). First-two-seconds rules. Orbit not at frame 0.
- [ ] `gate_shorts_open.py check` PASS for each export
- [ ] Exact live film title on screen at 9–14 s. Last 4 s loop to the opening.

## Packaging and Studio

- [ ] Title: one of the six shapes + Rule 15 (≤50 chars) + Rule 18 real-imagery variant. No hashtags, suffix, hedged claim or repeat title.
- [ ] Thumbs: 2–4 words, readable at 168×94 (`thumb_preview.py`), add to the title, no Orbit. 3 variants for the long (including Rule 19 single real spacecraft frame + Rule 14 bright test).
- [ ] Description: real subject first · chapters · Next in the series (`Real Worlds`, Rule 20) · sources · image credits · making-of line
- [ ] Upload private with `publishAt`. Long = normal publish, Sunday or Wednesday 18:00 UK (no Premiere). Altered content: yes.
- [ ] Long: Test & Compare · end screen (`Real Worlds` series playlist + next film in series + Subscribe) · captions auto-synced · pinned comment posted with `update-pinned-comment.ts --create` and pinned in Studio
- [ ] Shorts: Related → the long each promotes · no new pin · zero `/go/`

**Ship only when every box is ticked and Ben has signed off.**
