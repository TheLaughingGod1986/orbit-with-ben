# Production checklist — Orbit With Ben (`061` Why Venus Spins Backwards and Its Day Is Longer Than Its Year)

**Episode:** `061_Why-Venus-Spins-Backwards-And-Its-Day-Is-Longer-Than-Its-Year`  
**Date:** 2026-11-04 (`J1963` topic evidence & `023` overlap verification; `J1806`/`J1807`/`J1808` FIX — **NOT LOCKED**)  
**Script review score:** `95.8` / 100 on `v01` automated reviewer (`1,269` spoken / `1,290` reviewer words), **but `J1806` topic FIX, `J1807` script FIX, and `J1808` sources FIX remain open — NOT approved for VO or picture**

Rules: `AGENTS.md` · `00_Brand/Channel-Setup/FAMILIAR_DANGER_STRATEGY.md` · `THUMBNAIL_AND_TITLE_RULES.md` · `STUDIO_PLAYBOOK.md` · `docs/ORBIT_PLAYBOOK_LESSONS.md`

---

## Topic and script

- [ ] Familiar thing in danger. **No existing public long on this subject (`BLOCKED`: `OWB:023` *What Happened to Venus?*, `VBaYRPp85Sw`, is public since `2026-10-25` and already teaches Venus's `243-day` retrograde rotation and `225-day` year in Chapter 3; requires an explicit elected-Chief exception to `STUDIO_PLAYBOOK.md` §1 in `J1964` before advancing).** Matching topic Short `>=200` views & `>=40%` stayed (`UNMET`: `0` Venus-rotation Shorts; `023` Venus Shorts `_a66uhRDips` at `32.7%` and `hZH0C7fpCk4` at `30.8%` stayed `<40%`). Competition check done (`J1963`).
- [ ] Pre-build topic & packaging audit (`11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`) and `11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md` signed off by Chief (`J1964`)
- [ ] First 3 s of picture = the subject moving (no Orbit, no title card, no whole-planet Veo/Omni start frame). Sentence one = claim-led promise. Concrete causal answer named before 30 s (`J1807` #1).
- [ ] 4–6 acts told as cause and effect (`J1807` #2: replace spoken number/date catalogues with one causal idea at a time). The world does the science. Orbit in 1–2 beats only.
- [ ] Picture change about every 4–6 s. Every spoken and visual claim verified via formal Gemini `facts` pass (`J1966` via `agy`) and direct `MUST QUOTE` check (`J1967`, `01_Script/CLAUDE_QUOTE_CHECK_v01.md`) (`J1807` #3, `J1808`). No goodbye line. The last line hands off to the confirmed next film (`J1807` #6).
- [ ] Teach on screen (`AGENTS.md`, `J1807` #4–5): `DATA >= 3` (each with a spoken and visual `SCALE:` comparison, one idea per graphic, `<=4`-word labels, real moving imagery between graphics), `WHO` card at first mention with complete sourced years and `<=4`-word roles, `WHEN` call-outs + one timeline for `>=3` dates, `FACT` 2–4 (`<=4` words), and one `NUMBER OBJECT` per chapter (`WORDS` matching VO word-for-word).
- [ ] One `[SUBSCRIBE BEAT]` after the first payoff (25–50%), a line <=20 words from `templates/SUBSCRIBE_BEAT_LINES.md` not used in the last four longs
- [ ] Runtime **7–9 min** (about **1,200–1,300 spoken words**)
- [ ] Exact-version `npm run review:script` >= 90 · `npm run gate:episode` PASS · explicit Chief script lock (`J1964`)

## Voice and picture

- [ ] Ben Orbit Narrator only (`04_Audio/tools/orbit_voice.py` via `el_client.py`). Speech around −19 to −28 dB mean. No silent stretches. Verified listening pass by audio-capable reviewer.
- [ ] **Vertex AI only:** Vertex Veo for world plates, Vertex Omni (`global`) only for Orbit (max 2 beats), Codex `gpt-6-astra` for code graphics. **Never AI Studio prepaid credit.** Veo/Omni audio stripped.
- [ ] Picture matches every sentence (mute test). Verify every NASA ID and classification (`J1807` #5 / `J1808` #5: `PIA00271` is a computer-simulated global view and cannot be used as a real plate). `python3 scripts/picture_qa.py` PASS. Orbit on-model.
- [ ] No reused cutscenes, scenery loops, slow-mo, freeze-pads or Ken-Burns text

## Assembly

- [ ] Inputs normalised to 1920×1080 stereo. A/V durations match after concat.
- [ ] Remint = picture only (original part audio kept)
- [ ] Chapter cards wait for VO sentence end, 0.5–0.8 s breath lead-in, ~0.4 s crossfade, music continues under the card (`ORBIT_PLAYBOOK_LESSONS.md` §2)
- [ ] End hold **15–20 s** of moving picture after last VO word, music carries 2–3 s past last word then fades over ~10 s, picture fades to black over the last 2 s (`STUDIO_PLAYBOOK.md` §7, `J1807` #6). No silent hold.
- [ ] Own score bed generated via `04_Audio/tools/generate_music_bed.py`; `python3 scripts/music_gate.py` PASS; `python3 scripts/sfx_kit.py level` PASS.
- [ ] 4-second lower-right subscribe cue under the beat, with the picture still moving
- [ ] Watched once on a phone with the sound on

## Shorts (3 a week)

- [ ] 22–27 s (55–65 words). Keeper score one-question title + line 1 (`STUDIO_PLAYBOOK.md` §3). First-two-seconds rules. Orbit not at frame 0.
- [ ] `gate_shorts_open.py check` PASS for each export
- [ ] Exact live film title on screen at 9–14 s. Last 4 s loop to the opening.

## Packaging and Studio

- [ ] Title: one of the six shapes (`<= ~60` chars preferred). No hashtags, suffix, hedged claim or repeat title.
- [ ] Thumbs: top-band 2–3 words, readable at 168×94 (`thumb_preview.py long --score`), add to the title, no Orbit, HSV sat >=100, near-black <=30%. 3 variants for the long.
- [ ] Description: real subject first · chapters · `Sources:` line (4–6 papers/fact sheets from verified `SOURCES.md` rows, never naming AI checkers) · affiliate only if named in the film
- [ ] Upload private with `publishAt`. Long = normal publish, Sunday 18:00 UK (no Premiere). Altered content: yes.
- [ ] Long: Test & Compare · end screen (best related long + Subscribe) · captions auto-synced (`en-GB`) · pinned comment posted with `update-pinned-comment.ts --create` and pinned in Studio
- [ ] Shorts: Related → the long each promotes · registered in `00_Brand/Channel-Setup/social/UPLOADS.json` · no new pin · zero `/go/`

**Ship only when every box is ticked and Chief / Ben have signed off.**
