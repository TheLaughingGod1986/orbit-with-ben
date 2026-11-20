# Production checklist — Orbit With Ben

**Episode:** `034` — *Why Pluto's Frozen Heart Has Zero Craters*  
**Date:** 2026-11-19  
**Script review score:** 95.8 / 100 (must be 90 or more)

Rules: `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` · `FAMILIAR_DANGER_STRATEGY.md` · `THUMBNAIL_AND_TITLE_RULES.md`

---

## Topic and script

- [x] Familiar thing in danger. No existing public long on this subject. Competition check done (12 neighbours at 1.03M–21.20M views, led by NASA's 21.20M documentary and Astrum's 18.43M Pluto film). Rule-E GO (`J2149`).
- [x] Pre-build vidIQ audit signed off
- [x] First 3 s of picture = the danger. Sentence one = the promise. Payoff named by 30 s.
- [x] 4–6 acts told as cause and effect. The world does the science. Orbit in 1–2 beats only.
- [x] Picture change about every 4–6 s. Every number sourced. No goodbye line.
- [x] One `[SUBSCRIBE BEAT]` after the first payoff (25–50%), a line from `templates/SUBSCRIBE_BEAT_LINES.md` not used in the last four longs (Line 9, 14 words at 42%)
- [x] Runtime 8–9 min (about 1,200–1,300 words: 1,291 spoken words in `v03`)
- [x] `npm run review:script` 90 or more (95.8/100) · `npm run gate:episode` PASS

## Voice and picture

- [x] Ben Orbit Narrator only (`02_Voiceover/pluto_frozen_heart_vo_v03.wav`, `616.160 s`, `-23.0 dB` mean, `-19.9 LUFS`, `-3.7 dBTP`; `J2157` / `J2352` PASS). No silent stretches.
- [x] Real verified NASA/JHUAPL/SwRI/ESA/STScI/JPL/KSC/USNO/Lowell/Wikimedia plates (`67` hash-matched harvest assets in `HARVEST_POOL_v01.json` + `14` × `30 fps` code graphics + `6` chapter cards; `J2368` / `J2370` / `J2438` PASS). Veo/Omni audio stripped (`£0` spend).
- [x] Picture matches every sentence (`J2868` 5-part multimodal review PASS + `J3087` complete 15-bed music library comparison PASS).
- [x] No reused cutscenes, scenery loops, slow-mo, freeze-pads or Ken-Burns text (`picture_qa` 0 of 138 fail, `polish_gate` 0 of 138 fail).

## Assembly

- [x] Inputs normalised to 1920×1080 stereo. A/V durations match after concat (`09_Final-Export/034_pluto_frozen_heart_master_v02.mp4`, `646.933333 s`, `19,408` frames @ `30/1` CFR, `-14.7 LUFS`, `-1.0 dBTP`, SHA-256 `e5a886dfef208774cce8ae987e658fba5d7a96cbb5c99a44aadf63516949ba62`; `J2868` + `J3087` KEEP).
- [x] Remint = picture only (original part audio kept)
- [x] Chapter cards: soft starfield, about 1.5 s breath lead-in, music continues under the card (`R08`, `R20`, `R33`, `R45`, `R54`, `R64` silences verified in `J2868`)
- [x] End hold 15–20 s (`18.11 s` `628.82–646.933 s`), music fades over about 10 s, picture fades to black over the last 2 s. No silent hold.
- [x] Ocean/shore POV: no Earth globe in the sky. One Earth + one Moon at most (mid-plate frame checked).
- [x] 4-second lower-right subscribe cue under the beat, with the picture still moving
- [ ] Watched once on a phone with the sound on (staged in iCloud + NAS `OWB UAT/034_pluto_frozen_heart_master_v02.mp4`; `J2868` `awaits_ben` watch-by `8 Dec 2026 18:00 London` for planned `Sun 13 Dec 2026 18:00 London` slot)

## Shorts (2 per new OWB long, Ben 4 Nov 2026)

- [x] 22–27 s (`034_short02_water_ice_mountains_v02.mp4` `25.800 s`, SHA-256 `f3e3d47d0c86be1d297fbf5fade3383126f9c01d94ab2b78444d60dd6a66be73`; Test A opening `034_short01_testA_opening_v02.mp4` `36.500 s`, SHA-256 `c9a02052ff7a33cba10adc52e440cfe793c6cca1f31e355262acf9fd9c4ba677` excepted). First-two-seconds rules. Orbit not at frame 0 (`J2868` PASS + Ben OK 18 Nov 2026).
- [x] `gate_shorts_open.py check` PASS for each export
- [x] Exact live film title on screen at 9–14 s. Held in `J3066` (Mon 21 Dec 11:30 London) and `J3065` (Wed 23 Dec 11:30 London) until `034` long is public.

## Packaging and Studio

- [x] Title candidates prepared for packaging panel & Chief decision: Rule 15 scenario/stakes (`Why Pluto's Frozen Heart Has Zero Craters`, 41 chars), Rule 26 search-first bracketed (`Why Does Pluto Have a Heart? (And Why It Has Zero Craters)`, 58 chars), and Rule 18 real-imagery variants (`What New Horizons Saw Inside Pluto's Frozen Heart`, 49 chars; `The Only Spacecraft Photos Ever Taken of Pluto`, 46 chars). Zero collisions across 281 channel videos and YouTube search (`J3106`).
- [x] Thumbs: 3 draft candidates built in `J3105` (`08_Thumbnail/J3105_v01/034_pluto_{A,B,C}_j3105_v01.jpg`: `A` `NITROGEN GLACIER` on `PIA19952`, `B` `ICE MOUNTAINS` on `PIA19948`, `C` `FLOWING ICE` on `PIA20726`; all `thumb_preview.py --score` PASS; in `review` for packaging panel + Chief decision).
- [x] Description: real subject & search phrase first · story paragraphs · `More in the Real Worlds series: Why Knocked-Sideways Uranus Has 21-Year Winters` (obsolete `035 Triton` promise removed per `J2864`) · chapters (`0:00` to `9:05` from `cuts_v02.json`) · `Sources:` line (6 verified sources from `SOURCES.md`) · `Image credits:` line (all 67 harvest assets + CC licenses) · honest making-of line (`Descriptions/pluto_frozen_heart_long_description_v01.txt`).
- [x] `11_Upload-Package/PACKAGE_MANIFEST.json`, `Captions/en-GB.srt` (`189` cues, `0.100–628.820 s`), and `Trailer/034_why_plutos_frozen_heart_has_zero_craters_trailer.mp4` (`52.500 s`, `608×1080` @ `30/1` CFR, SHA-256 `01701660d2fcc3a1340fa8d6ffef2f8d1a96b87e049facf1d28905c4a05392fd`) prepared and `npm run youtube:package -- --dry-run` verified (`J3106`, planned slot `Sun 13 Dec 2026 18:00 London`, `2026-12-13T18:00:00.000Z`, `private`, Altered content: yes).
- [ ] Packaging panel (`codex`, `gemini`, `cursor`) + Chief packaging decision · Ben UAT watch on `J2868` · Live YouTube Private upload + Test & Compare · end screen (`Real Worlds` series playlist + `033 Uranus` + Subscribe) · captions · pinned comment
- [ ] Shorts (`J3066`, `J3065`): upload after `034` long is public · Related → `034` long · no new pin · zero `/go/`

**Ship only when every box is ticked and Ben has signed off.**
