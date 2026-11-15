# Production checklist — Orbit With Ben

**Episode:** `033` — *Why Knocked-Sideways Uranus Has 21-Year Winters*  
**Date:** 2026-11-04  
**Script review score:** 95.2 / 100 (must be 90 or more)

Rules: `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` · `FAMILIAR_DANGER_STRATEGY.md` · `THUMBNAIL_AND_TITLE_RULES.md`

---

## Topic and script

- [x] Familiar thing in danger. No existing public long on this subject. Competition check done (10 neighbours ≥1.24M views; Short `ZpEA8stoSPA` 461 views d1). Rule-E GO (`J2148`).
- [x] Pre-build vidIQ audit signed off
- [x] First 3 s of picture = the danger. Sentence one = the promise. Payoff named by 30 s.
- [x] 4–6 acts told as cause and effect. The world does the science. Orbit in 1–2 beats only.
- [x] Picture change about every 4–6 s. Every number sourced. No goodbye line. The last line hands off to the next film.
- [x] One `[SUBSCRIBE BEAT]` after the first payoff (25–50%), a line from `templates/SUBSCRIBE_BEAT_LINES.md` not used in the last four longs
- [x] Runtime 8–9 min (about 1,200–1,300 words: 1,290 spoken words in `v02`)
- [x] `npm run review:script` 90 or more (95.2/100) · `npm run gate:episode` PASS

## Voice and picture

- [x] Ben Orbit Narrator only (`02_Voiceover/uranus_vo_v01.wav`, `611.40 s`, `-23.3 dB` mean, `-20.22 LUFS`, `-3.77 dBTP`; `J2155` / `J2164` KEEP). No silent stretches.
- [x] AI Studio / real spacecraft plates (`42` active NASA/ESA/CSA/ESO/Keck/USGS stills + `R01` `r01_sourced_composite_v01_silent.mp4` + `R55` `r55_passage_v01_silent.mp4` + `20` × `24 fps` code graphics; `J2299` / `J2300` / `J2398` PASS). Veo/Omni audio stripped.
- [x] Picture matches every sentence (`J2300` & `J2890` 5-part moving-video review PASS).
- [x] No reused cutscenes, scenery loops, slow-mo, freeze-pads or Ken-Burns text (`picture_qa` 0 fail, `polish_gate` 0 fail).

## Assembly

- [x] Inputs normalised to 1920×1080 stereo. A/V durations match after concat (`09_Final-Export/033_why_this_planet_has_21_year_winters_master_v04.mp4`, `629.416667 s`, `15,106` frames @ `24/1` CFR, SHA-256 `3712479ae852dd318c4d8d0dfd18f7df08c1a857068c24c3d3792a35a27f11c3`; `J2889` / `J2890` / `J2893` PASS).
- [x] Remint = picture only (original part audio kept)
- [x] Chapter cards: soft starfield, about 1.5 s breath lead-in, music continues under the card
- [x] End hold 15–20 s (`18.00 s` `611.40–629.40 s`), music fades over about 10 s, picture fades to black over the last 2 s. No silent hold.
- [x] Ocean/shore POV: no Earth globe in the sky. One Earth + one Moon at most (mid-plate frame checked).
- [x] 4-second lower-right subscribe cue under the beat (`255.14–259.68 s`), with the picture still moving
- [ ] Watched once on a phone with the sound on (`_PHONE.mp4` staged to NAS/iCloud `OWB UAT` & R2 `owb-033-v04`; `J2890` `awaits_ben`)

## Shorts (2 per new OWB long, Ben 4 Nov 2026)

- [x] 22–27 s (`033_short02_ice_giant_surface_v02.mp4` `27.48 s`; Test A opening `033_short01_testA_opening_v02.mp4` `36.48 s` excepted). First-two-seconds rules. Orbit not at frame 0 (`J2870` PASS + Ben OK 15 Nov 2026).
- [x] `gate_shorts_open.py check` PASS for each export
- [x] Exact live film title on screen at 9–14 s. Last 4 s loop to the opening (`J2896` & `J2895` `07_Upload-Package` dry-run PASS, held until `033` long is public).

## Packaging and Studio

- [x] Title: one of the six shapes + Rule 15 (≤50 chars: `Why Knocked-Sideways Uranus Has 21-Year Winters`, 47 chars) + Rule 18 real-imagery variants (`What Voyager 2 Saw in Just 6 Hours at Uranus`, 44 chars; `The Only Spacecraft Photos Ever Taken at Uranus`, 47 chars). No hashtags, suffix, hedged claim or repeat title.
- [x] Thumbs: 2–4 words, readable at 168×94 (`thumb_preview.py`), add to the title, no Orbit. 3 variants for the long (`08_Thumbnail/033_thumb_{A,B,C}_v01.jpg`: Rule-19 real JWST frame `21-YEAR WINTER`, `COLDER THAN NEPTUNE`, Rule-14 bright Keck `97.77° SIDEWAYS`; `J2899` / `J2900` PASS).
- [x] Description: real subject first · chapters (`0:00` to `8:35`) · Next in the series (`Real Worlds`, Rule 20) · `Sources:` line (6 primary papers/fact sheets from `SOURCES.md`) · image credits · making-of line (`Descriptions/uranus_21_year_winters_long_description_v01.txt`)
- [x] `11_Upload-Package/PACKAGE_MANIFEST.json`, `Captions/en-GB.srt` (`206` cues, `0.100–611.324 s`), and `Trailer/033_why_this_planet_has_21_year_winters_trailer.mp4` (`48.75 s`, `608×1080` @ `24/1` CFR, SHA-256 `08af084e7673188b5235d95dfb28ac26c371572445b9e3479edb8942d5d21843`) built and `npm run youtube:package -- --dry-run` verified (`J2901`, target slot `Wed 09 Dec 2026 18:00 London`, `2026-12-09T18:00:00.000Z`, `private`, Altered content: yes).
- [ ] Live YouTube Private upload + Test & Compare (`T033` A vs B) · end screen (`Real Worlds` series playlist + next film in series + Subscribe) · captions auto-synced · pinned comment posted with `update-pinned-comment.ts --create` and pinned in Studio (after Ben UAT watch on `J2890`)
- [ ] Shorts: Related → the long each promotes · no new pin · zero `/go/` (after `033` long is public)

**Ship only when every box is ticked and Ben has signed off.**
