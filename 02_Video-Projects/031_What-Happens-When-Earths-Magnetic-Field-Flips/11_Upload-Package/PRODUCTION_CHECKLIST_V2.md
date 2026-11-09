# Production checklist — Orbit With Ben

**Episode:** `031_What-Happens-When-Earths-Magnetic-Field-Flips` (*What Happens When Earth's Magnetic Field Flips?*)  
**Date:** 8 Nov 2026  
**Script review score:** `95` / 100 (must be 90 or more)

Rules: `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` · `FAMILIAR_DANGER_STRATEGY.md` · `THUMBNAIL_AND_TITLE_RULES.md`

---

## Topic and script

- [x] Familiar thing in danger. No existing public long on this subject. Competition check done. Chief picked it (`J0251`).
- [x] Pre-build vidIQ audit signed off (`PRE_BUILD_VIDIQ_AUDIT.md`)
- [x] First 3 s of picture = the danger. Sentence one = the promise. Payoff named by 30 s.
- [x] 4–7 acts told as cause and effect. The world does the science. Orbit in 1–2 beats only.
- [x] Picture change about every 4–6 s. Every number sourced (`SOURCES.md`, `CLAUDE_QUOTE_CHECK_v01.md`, `J2396` Gemini claims pass PASS). No goodbye line. The last line hands off to the next film.
- [x] One `[SUBSCRIBE BEAT]` after the first payoff (25–50%), a line from `templates/SUBSCRIBE_BEAT_LINES.md` not used in the last four longs
- [x] Runtime 8–9 min (`9:31` / `570.80 s`, `1,259` spoken words)
- [x] `npm run review:script` 90 or more (`95/100` PASS) · `npm run gate:episode` PASS

## Voice and picture

- [x] Ben Orbit Narrator only (`magnetic_field_flip_vo_v02a.mp3`, `J1237` PASS). Speech around −19 to −28 dB mean. No silent stretches.
- [x] Agency/Commons plates + original animated code graphics; Veo/source audio stripped.
- [x] Picture matches every sentence (mute test). Reviewed KEEP in `J2390` (`jobs/reviews/J2390/REVIEW.md`).
- [x] No reused cutscenes, scenery loops, slow-mo, freeze-pads or Ken-Burns text

## Assembly

- [x] Inputs normalised to 1920×1080 stereo (`25 fps` CFR). A/V durations match after concat (`570.80 s`).
- [x] Remint = picture only (original VO + custom music bed `031_magnetic_field_flip_bed_v01.mp3` + house SFX kit `kit_v01`)
- [x] Chapter cards: soft starfield, breath lead-in, music continues under the card
- [x] End hold past last word (`568.24 s` → `570.80 s`), music and picture fade cleanly. No silent hold.
- [x] Ocean/shore POV: no Earth globe in the sky. One Earth + one Moon at most.
- [x] Lower-right subscribe cue under the beat (`145.64–154.06 s`), with the picture still moving

## Shorts (2 active + 1 reserve under 4 Nov cap)

- [x] Active Short #1 (`031_short_testA_opening_flip_v01.mp4`, `37.16 s` Test A opening) & Active Short #2 `v02` (`031_short_sat12_solar_wind_air_v02.mp4`, `24.48 s` Keeper-score question Short).
- [x] `gate_shorts_open.py check` PASS for each export (`J2388` & `J2394`, reviewed KEEP in `J2395`).
- [x] Exact live film title on screen at 9–14 s (`What Happens When Earth's Magnetic Field Flips?`).

## Packaging and Studio

- [x] Title: `What Happens When Earth's Magnetic Field Flips?` (`47` chars, question shape, no hashtags, suffix, hedged claim or repeat title).
- [x] Thumbs: 3 variants for the long (`031_A_compass_v03.jpg`, `031_B_real_v04.jpg`, `031_C_bright_v03.jpg`), built in `J2143` and approved KEEP in `J2166`.
- [x] Description: real subject first · chapters (`0:00` to `8:00`) · 5-item `Sources:` block · exact `Image credits:` · truthful `Pictures: ... Facts: ...` line · zero `/go/` affiliate links (none named in VO).
- [x] Upload package dry-run verified (`npm run youtube:package -- --dry-run` PASS for Long `v02` and Active Shorts #1 & #2 `v02`). Schedule: Long `Wed 2 Dec 2026 18:00Z`, Short #1 `Sat 5 Dec 2026 11:30Z`, Short #2 `Sat 12 Dec 2026 11:30Z`.
