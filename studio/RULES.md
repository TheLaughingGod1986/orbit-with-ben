# Orbit With Ben: this channel's rules

Read `AGENTS.md` first. It holds the studio's rules, which are the same for every channel. This file adds Orbit With Ben's own: what its films teach, look and sound like, and how they are titled and packaged. Where the two disagree, `AGENTS.md` wins. Nothing here removes a studio rule (Ben, 10 Nov 2026: *"this system will read the individual channel's rules and guidance"*).

**The channel:** Orbit With Ben (`@OrbitWithBen`, `UC_esArsDKd3GJvOkeO0DUog`). Animated space storytelling with Orbit, a small orange robot, and Ben's British narration. Wonder, not dread.

**The job:** build films that hold people. The channel grows on Shorts stayed-to-watch and on long-form search. See `00_Brand/Channel-Setup/audits/CHANNEL_AUDIT_2026-09-24/AUDIT.md` for why.

## Docs in force (in order of precedence)

When two docs disagree, the one higher in this list wins. Anything not listed here, and everything in `_archive/`, is history only. Don't follow it.

1. `00_Brand/Channel-Setup/FAMILIAR_DANGER_STRATEGY.md`: what to make, the week, Short and long hooks, the first two seconds, the four-week test (12 Oct – 6 Nov 2026).
2. `00_Brand/Channel-Setup/THUMBNAIL_AND_TITLE_RULES.md`: title shapes, thumbnail rules, frame 0 as the Shorts thumbnail.
3. `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md`: how to build and ship: topic, script, voice, picture, Orbit, assembly, upload, measure, affiliate, social, sign-offs.
4. `docs/ORBIT_PLAYBOOK_LESSONS.md`: **standing lessons for Cursor + Claude** (neighbour rule, v03b edit locks, Omni/Vertex/KEEP locks, PR #99 thread protocol). Read with the playbook when building or answering on the thread.
5. `00_Brand/Channel-Setup/YOUTUBE_GROWTH_AND_POLICY.md`: retention, CTR and policy basics.
6. `00_Brand/Channel-Setup/CHANNEL_AUTHORITY.md`: picture matches the words, same Orbit, voice present, weekly promise.
7. `00_Brand/Channel-Setup/YOUTUBE_FRAME_SIZES.md`: sizes.
8. `00_Brand/Channel-Setup/IMPROVEMENTS_BACKLOG.md`: housekeeping to do now, and what waits until after the test.

## Where things live (this channel's folders)

| Path | What |
|---|---|
| `00_Brand/Channel-Setup/` | The docs above, `VIDEO_BACKLOG.json`, `PINNED_COMMENTS.json`, `PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md`, `templates/` (incl. `SUBSCRIBE_BEAT_LINES.md`), `ideas/`, channel description and keywords |
| `00_Brand/Channel-Setup/tools/` | `gate_shorts_open.py` (Shorts ship gate), `thumb_preview.py`, `weekly_public_audit.py`, thumbnail builders |
| `00_Brand/Channel-Setup/could-orbit-survive/` | The Wednesday test format, three scripts, `TEST_LOG.md` |
| `00_Brand/Channel-Setup/audits/` | Current audits, `weekly/` reports, `shorts_open_library/` (gate data) |
| `00_Brand/Channel-Setup/social/` | Buffer mirror: `BUFFER_CHANNELS.json` (channel ids), `UPLOADS.json` (YouTube id → local file and long), `BUFFER_POSTS.json` (what was posted), `buffer-plans/`. Buffer is the only route to social. TikTok is paused. |
| `01_Orbit-Character/` | Canonical Orbit stills (`05_Seedance-References/orbit-seedance-reference-16x9-v01.png`) |
| `02_Video-Projects/NNN_Slug/` | One folder per film in the git checkout (template + status). **Working media** for live films lives on the NAS under `studio-live` (see **Film folders on the NAS** below), not in git. |
| `04_Audio/tools/` | `orbit_voice.py` (VO settings), `orbit_gemini_veo.py` |
| `docs/ORBIT_PLAYBOOK_LESSONS.md` | Tonight's standing rules (neighbour, edit, production locks, thread protocol) |

## Standing lessons (this channel's)

Read **`docs/ORBIT_PLAYBOOK_LESSONS.md`** in full before topic lock, assembly, or acting on the PR #99 thread. Short form:

Lessons 3, 4 and 6 are the studio's and stay in `AGENTS.md`.

1. **Neighbour:** ≥3 education/space videos ≈1M+ views before topic lock; subject words in title/desc/tags; never channel names. Evidence: HOS 002 gets 55.6% of views Suggested from TED-Ed's Mendeleev film.
2. **Edit (v03b):** cards wait for the VO sentence, 0.5–0.8 s breath, ~0.4 s xfade; never clip a line; picture+music past last word, hold 2–3 s, then fade; music full runtime, and it's the film's own (lesson 7); fill 16:9 (feathered blur OK); upscale ≤~2.35×; mix ~−14 LUFS; check repeated/stumbled VO before delivery.
5. **Shorts feed (5 Oct):**
   - Judge a Short by its day-1 Shorts-feed share (50% or more means fed), not by % viewed under ~50 views.
   - Stop a topic after 2 not-fed Shorts in a row, and run at most 6 in a row on one topic; then give it a 2-week break.
   - Every Short gets its own open, with frame 0 showing the titled subject and no opening background reused from the last 10 Shorts.
   - **Every shot fills the 9:16 frame (Ben, 8 Nov 2026: *"like a rectangle and blurry above and below"*; Chief rulings on J2545, 11 Nov 2026).** Nowhere in a Short does the picture sit as a band with a blurred copy, a mirrored copy, bars or a flat colour above or below it, on one side or on two. A graphic over a faint blurred backdrop counts as padding. Reframe the shot (crop and scale, inside the upscale limit) or use other real picture. The gate checks the opening and then one frame every second (`gate_shorts_open.py`, J2546, J2560). It is a hard FAIL when more than a tenth of them show a band over fill with a straight edge between the two, or when more than 15% look padded, edge or no edge; it names the stretches. A frame that looks padded with no straight edge found counts for less, because a full-frame shot with soft walls above and below can read the same way: under that share it is a warning naming the seconds, and whoever reviews the Short looks at them. The end card is judged apart, and only where the cut's own meta names it (`end_card.start_s`): an end card on a blurred copy is reported, not failed. A cut Ben OK'd before this rule may still go up as a fallback when its exact file is listed in `00_Brand/Channel-Setup/tools/full_bleed_okd_before_rule.json`. List only a file Ben has OK'd, and take it out once its Short has aired.
   - **Test A, the opening Short (Ben, 9 Oct: yes), from 025 on:** one of each long's three Shorts is the long's own opening (the first 30–38 s of the master, reframed to 9:16, cut on a sentence end, gates as usual, Related video = the long). The weekday rotates by film. Plan, measures and readout dates: `05_Analytics/tests/SHORTS_TESTS.md`. **Exception (Ben, 26 Oct 2026):** Test A Shorts are exempt from the Keeper score one-question first line and from 22–27 s until Test A's own result is read; readouts are Wed 18 Nov, Wed 9 Dec and the final in early January 2027 (`SHORTS_TESTS.md`).
   - **Keeper score (Ben, 26 Oct 2026):** one question per Short, in the title and line 1 (*Could a Robot Survive Touching the Sun?* 883, *Why Does a Day on Mercury Last Two of Its Years?* 849); no statement or teaser titles (*Saturn's Rings Are on a Clock* 12) and no off-week Saturn Shorts; 22 s or longer (compilation exempt; J0216 test Shorts keep their ~20 s cuts until the test ends on 20 Nov 2026 (test-only exception); Test A excepted); Related video and description link to the matching long (J0216 test Shorts unlinked until 20 Nov); Sun Shorts wait for the `h8HGfyShEHI` thumbnail test to end on 1 Nov. Rule: `.cursor/rules/orbit-build-shorts.mdc` → *Keeper score*.
   - Aim for 60% or more average viewed on day 1.
   - End on the long's exact listing title and its video id, with a music bed for the full length.
   - Details: lessons doc §6.
7. **Picture and music QA (Ben, 8 Oct, after a dated computer model at 2:54 of 025 and one music track on 023, 024 and 025).** Run one check for each before Claude's review and before anything goes to OWB UAT. The pack carries both reports.
   - **Picture:** `python3 scripts/picture_qa.py <cut.mp4> --cuts <cuts.json> --pool <pool.json> --out-dir <pack>` must PASS.
     - It names every problem at its film time (m:ss), the way Ben reports one.
     - FAIL: a computer model or reconstruction, simulation, diagram, chart, schematic or labelled image (they look dated or like a textbook); upscale over 2.35×; a still that appears more than twice (back-to-back cuts are one appearance); footage back on a stretch within 10 s of one already shown, or in more than 5 stretches; a code graphic repeated from the same render (each row's render goes in the cut list under its own file name); a run that replays its own frames; and polish_gate's low detail, split panels, near-black, noise and wobbly pushes.
     - WARN: an artist's concept, map, render, untitled source or upscale over 2×. These go on `picture_qa_review.jpg`, and Claude looks at each one full size.
     - Claude also looks at every cut on the per-row sheet and asks: would a viewer trust this as a real, sharp, finished picture of what the sentence says?
     - **The first 30 seconds (9 Oct, Gemini's idea 1):** no more than one code graphic in a row, and real moving imagery between graphics. One observatory exterior at most in the first 60 s. The first concrete answer to the title comes before 0:30, not an agenda (Codex's idea 5).
     - **The first 30 seconds of a long (Ben, 8 Nov 2026, J2428: "Do we need to improve our hook"; we keep only 33-66% at 0:30 on every long with data, all rated "lower" than similar videos).** What the six weakest openings shared: Orbit or a scene-setting plate before the subject (001, 003, 004 held the payoff image back on purpose); a promise of what the film will show ("In this film I will show you", "Stay with me and you'll see") in place of the next fact (023, 021); the hook said twice (021); a side question before the stakes (023 "Why radar?"); and a starfield chapter card inside the first 30 s (021, 023). The rule, checked by Claude at script lock and at the picture review: (1) frame 0 is the single most striking real image of the subject, already moving; no Orbit, title, logo or fade before 0:30; (2) the first line states the stakes or mystery in the title's own words and ends before 0:08; (3) no agenda or meta-promise and no restated hook: every sentence to 0:30 adds a new fact, number or image; (4) a concrete payoff hint (a number, a date, a picture of the answer) by 0:20; (5) a picture change at least every 4 s, and no chapter card, starfield breath or music sting before 0:45. Same idea as HOS's proof-first open. A locked VO keeps its words; a re-cut opening reorders or trims whole sentences, and a re-voiced first sentence takes the usual VO checks.
     - **A code graphic must read with the sound off (Ben, 026 and 023, 9 Oct: "hard to understand", "not a great representation of what the VO is saying").** Real bodies, not flat discs: the Blue Marble Earth, a real Venus or Moon image. Short labels are allowed and expected: at most 4 words each, taken from the line being spoken (a name, a number, "bounced back"), in large house type. Each graphic shows one idea, the one the voice is saying at that moment. Claude checks a still of every graphic against its line before the render.
   - **Music:** every film has its own score bed, at a pace that fits it.
     - Claude writes the music prompt with the shot list. It gives the film's mood and arc from the script, a `Pace: NN-NN BPM` line matched to the narration (calm explanation about 60-80, a lift only where the script builds), and what it must NOT sound like (every earlier bed).
     - Generate it once with `04_Audio/tools/generate_music_bed.py` (the API, never the website).
     - **Standalone Shorts test + compilation film (Ben, 12 Oct 2026 14:50):** 8 self-contained ~20 s Shorts (2 a week for 4 weeks, not cut from longs; a one-off exception to the 22–27 s lock. **Test-only exception (Ben, 26 Oct 2026):** the J0216 test Shorts keep their ~20 s cuts until the test ends on 20 Nov 2026. Every new Short after that uses the 22 s floor) and one 45–60 min compilation from finished films. Decision and measurement: `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/`.
     - `python3 scripts/music_gate.py <film dir> --bed <bed> --video <cut>` must PASS: the bed is in the film's own 05_Music with its plan; the brief has Pace and NOT; it doesn't sound like another film's bed, even trimmed or re-encoded; and it runs the whole cut.
     - Fit is judged by ear: Claude's review, then Ben's watch.

## Teach on screen (Ben, 11 Oct 2026)

Ben, 11 Oct 2026 21:45, for every future video on both channels: *"add more graphs and charts when needed, more overlays, more animations, and more interesting facts to explain about dates, explain about the people we're mentioning, and make it more educational and more useful."* This applies to every script locked and every cut started after 11 Oct 2026. It adds to lesson 7 and the edit locks, and it relaxes none of them.

**Script.** Mark these inside the scene's `[VISUAL MUST: …]`, so `review:script` doesn't count them as spoken words and `gate:episode` doesn't change. Chief counts them at script review (`grep -o "DATA:" <script> | wc -l`, and the same for each marker).
- **DATA: at least 3 in every long (aim for 3–6).** Wherever the VO says a number, size, distance, time span or trend, add `· DATA: <what the graphic shows>`: an animated bar or line chart, a scale bar or size comparison, a counter, or a timeline. At least one comes before the `[SUBSCRIBE BEAT]`. Every DATA number is a MUST QUOTE row in `SOURCES.md`.
- **WHO: a card for every named person at first mention.** Use `· WHO: <name> (<born>–<died>, or "born <year>") — <role, 4 words or fewer>`. Later mentions get no card. The years go into `SOURCES.md` and the Gemini claims pass, like any spoken number.
- **WHEN: every date or era that's said.** Add `· WHEN: <year or era>` for a date call-out. A story with 3 or more dates gets one timeline that builds as each date is said, and it counts as one DATA moment. Later dates drop onto that timeline.
- **FACT: 2–4 per long.** Each is one surprising, sourced fact, said in a line and shown as a card: `· FACT: <card text, 4 words or fewer>`. Make it a "huh, I didn't know that" beat, never a list. It's quote-checked like every number.
- **Shorts (22–27 s): at most one overlay** (a fact card, a date call-out or a one-number scale bar), and only where it helps the line being said. It adds no words and no seconds, so the Short stays at 22–27 s and 55–65 words. It never appears in the first 2 s (frame 0 has the hook caption only) or over the 9–14 s title, and it stays inside the 16:9 centre band.

**Picture.**
- Every DATA, WHO, WHEN and FACT item is our own code graphic or edit overlay, rendered for its own row (`code_graphic_<film>_<row>…`) and listed in the cut list. A chart, graph, diagram or labelled image taken from a source still FAILs `picture_qa.py`. Never pull one in to meet the count.
- **Everything animates.** A chart builds in time with the spoken number: bars grow, the line draws, the counter runs, timeline markers drop in. A card slides or fades in over about 0.3–0.5 s, then out again. An overlay that animates over a moving plate counts as that window's 4–6 s picture change. No card holds still for more than 4 s, and a card is never Ken-Burned (that Never still stands).
- **The house picture rules still win:**
  - real bodies, not flat discs (lesson 7);
  - labels of 4 words or fewer, taken from the line being spoken, in large house type;
  - one idea per graphic;
  - never two code graphics back to back anywhere in the film, with real moving imagery between them (the first-30-seconds rule, now film-wide);
  - WHO, WHEN and FACT cards ride over moving or blurred real picture, never a flat black slab or an empty black panel, and the frame passes polish_gate's near-black check;
  - any NASA plate behind a graphic is colour-graded, and text stays off the subject;
  - a Short's overlay lines are 11–12% of the 16:9 band height (the house Short size), inside that band.
- **WHO card layout:** lower third, with the name on line one and the years and role on line two. It stays on screen 3–4 s while the name is spoken. Show no portrait we can't source; the card can sit over the scene alone.

**Review gate.** Chief's frame review and stills check score each item PASS or FAIL in the pack's review note:
1. **DATA:** a long has 3 or more animated data moments. Each matches its line, reads with the sound off, and shows the same number as `SOURCES.md`.
2. **WHO:** every named person has a card at first mention, with sourced years.
3. **WHEN:** every spoken date or era has a call-out, and 3 or more dates have a timeline.
4. **FACT:** a long has 2–4 fact beats, each one sourced.
5. **STYLE:** every overlay is our own render, with 4 words or fewer per label, in house type, off the subject, with no black slab, passing near-black and over graded plates. A Short's overlay sits inside the 16:9 band, clear of 0–2 s and the 9–14 s title.
6. **MOTION:** every overlay and chart animates in, none holds still for more than 4 s, and no two code graphics run back to back.

A Short is scored on 5 and 6 only, plus whichever of 1–4 its single overlay is, if it has one. Any FAIL goes back to the shot list before the cut goes to OWB UAT.

**What it applies to.**
- **All four markers:** scripts locked from 12 Oct on (030 and later).
- **Shot-list overlays only:** 025–029 already have their VO locked. Their shot lists add WHO, WHEN and DATA overlays on lines that are already spoken, with no VO change, before picture is cut. 025 picks them up at its next rough cut.
- **No rework:** 021 (live), 022 (scheduled), 023 (v05e approved) and 024 (v05 in review) stay as they are, because adding overlays would mean re-rendering cuts that have already passed.

## Polish pass (Astrum ref, 11 Oct 2026)

Ben, 11 Oct 2026 22:17, sent Astrum's *What Is It Like on the Surface of a Black Hole Planet?* (`PxJSOWyYWkc`, 27 min, 1.1M views) as a style reference: *"let me know what you think we can incorporate into our workflow."* Chief adopted five of its techniques the same night. They apply to every cut started after 11 Oct 2026. They add to lesson 7, the edit locks and *Teach on screen*, and relax none of them.

**Not adopted:** Astrum's long shot holds (6–8 s, some 15 s). That pace suits a 27-minute film, not our 8–9 minute longs and 22–27 s Shorts. The picture still changes every 4–6 s, and nothing holds still for more than 4 s.

**1. Sound design (SFX).**
- **Three kinds, where the shot calls for them:**
  - a low rumble under a violent or huge shot (an impact, a collapse, a planet-sized scale reveal);
  - a soft whoosh on a fly-through or a fast camera move;
  - a subtle tick when a label, line, bar or timeline marker appears.
- **Source: our own house kit.** Run `python3 scripts/sfx_kit.py make --out-dir <film>/06_Sound-Effects/kit_v01`. It synthesises the sounds itself, so there are no samples, no licence to track and no spend. The Mac mini has no licensed SFX library (checked 11 Oct: no Apple Loops or sample packs; macOS alert sounds aren't for video).
  - A free library may be added only if its licence allows commercial YouTube use with no attribution. Record it in the film's `06_Sound-Effects/SOURCES.md`. Nothing is bought.
  - ElevenLabs SFX spends the shared credit, so it waits for the 30 Oct reset and Chief's OK.
  - Never use a video model's own audio as SFX (silent picture).
- **Restraint:** no whoosh on plain cuts or on every card, at most one tick every 0.5 s, and no cartoon whooshes or comedy stings. Environment honesty still applies (water sounds only underwater).
- **Level rule.** SFX sit under the VO, like the bed. Assemblers keep VO, music and SFX as separate stems in the pack, and `python3 scripts/sfx_kit.py level --vo <vo stem> --sfx <sfx stem> --bed <music stem> --minutes <length>` must PASS:
  - the SFX stem is at least 12 LU under the VO's integrated loudness;
  - while the VO speaks, the SFX and the bed are each at least 10 LU under the VO;
  - in a VO pause, the SFX stay at least 6 LU under the VO's integrated loudness (a rumble may swell, never to speech level).

  The full mix stays about −14 LUFS and −1 dBTP.
- **Shorts** keep the frame-0 whoosh or impact (`FAMILIAR_DANGER_STRATEGY.md`) and may add ticks. The same level rule applies.

**2. Music by chapter (longs).**
- The score follows the chapters: an ambient drone under awe sections (reveals, scale, "what it's like"), and a light rhythmic or arpeggiated cue under explain and physics sections. Claude marks each chapter `awe` or `explain` in the music prompt, which keeps its `Pace:` line and NOT list.
- **Credit hold:** until the 30 Oct reset, no new bed starts without Chief's OK. So the free way is one bed whose prompt asks for both moods, with its drone and pulse sections laid at the chapter cards. A second cue counts as a new bed.
- The music changes at a chapter card with a 2–4 s crossfade, never a dip. `music_gate.py` still runs on the laid score: own music, a Pace and NOT brief for every cue, nothing that sounds like another film's bed, no gap, the whole runtime. The bed stays at least 10 LU under the VO.
- Shorts keep one bed.

**3. Explainer look.** For a hard-physics or mechanism section (how gravity bends light, why an orbit decays), switch to our own diagram look: thin glowing lines and arrows on a dark-navy grid. It's a code graphic (`chart` kind), so lesson 7 and *Teach on screen* apply in full:
- real bodies on the diagram (the Blue Marble Earth, a real Sun image), never flat discs;
- the navy is lifted, not black, so the frame passes polish_gate's near-black check (mean luma 28 or more, or p95 50 or more);
- labels of 4 words or fewer, in large house type;
- one idea per graphic, building with the line;
- real moving imagery between any two diagrams, so a physics section alternates diagram and footage and never runs as a slideshow;
- never a sourced diagram or schematic (still a `picture_qa.py` FAIL).

**4. Script.**
- **Every big number gets a scale.** Give it a plain comparison or an everyday analogy in the same or the next sentence ("about the width of the Atlantic"). Mark it on its DATA marker: `· DATA: <graphic> · SCALE: <comparison>`. The comparison's own numbers are a MUST QUOTE row in `SOURCES.md`.
- **Long hook:**
  - line 1 is still the claim, with the mystery in it, never "Imagine…";
  - the huge claim and the first concrete answer to the title land before 0:30;
  - the question the film answers is spoken by about 0:50.
- **Word counts don't change:** about 1,200–1,300 spoken words, and `review:script` at 90 or more. An analogy replaces words; it doesn't add them. Shorts stay at 55–65 words.

**5. Finishing.**
- **Crossfades** of 0.5–1.5 s between scenes, where the move suits (a change of place or time, an awe section). Hard cuts elsewhere; they're not required on every cut. A crossfade never stretches a shot past the 4 s hold or the 4–6 s picture change, and chapter cards keep their ~0.4 s xfade.
- **Fine film grain** over dark space backgrounds, to stop banding (for example ffmpeg `noise=alls=4:allf=t` before the final encode). It must not trip polish_gate's noise check, and it never rescues a near-black or empty frame.
- **Depth-of-field blur** for scale where it helps (soft foreground debris, a sharp far body). It's never on the subject the line names, and never heavy.
- **Corner credit labels** ("CGI", "NASA", "NASA/JPL", "ESO", "Artist's impression") on CGI, agency or artist's-concept picture. They sit bottom-left in small type (about 2.5–3% of frame height), off the subject and clear of the subscribe cue. They're the one exception to the large-type label rule (credit lines stay small), and they don't count as a *Teach on screen* overlay. Shorts carry none.

**Review gate.** Chief adds six items to the frame review and stills check, each scored PASS or FAIL in the pack's review note:
1. **SFX:** `sfx_kit.py level` PASSes, and the rumbles, whooshes and ticks sit on shots that call for them.
2. **MUSIC:** the laid score changes by chapter (awe to explain) at least once, at a card, and `music_gate.py` PASSes.
3. **GRAIN:** every dark space background shows grain at full size, with no banding, and polish_gate PASSes.
4. **SCALE:** every DATA number has its SCALE comparison, spoken and sourced (`grep -c "SCALE:"` is at least the DATA count).
5. **EXPLAINER:** physics sections use the diagram look within lesson 7 (real bodies, navy that passes near-black, footage between diagrams).
6. **FINISH:** crossfades are 0.5–1.5 s with no hold over 4 s, credit labels are on CGI and agency picture, and DOF blur stays off the subject.

A Short is scored on 1 and 3 only. Any FAIL goes back to the edit before the cut goes to OWB UAT.

**What it applies to.**
- **Items 1–3 and 5:** every rough cut or new version started from 12 Oct. That's 025 and 027 at their next version, then 026, 028, 029 and later.
- **Item 4:** spoken analogies and the hook start with scripts locked from 12 Oct (030 and later). 025–029 have their VO locked, so their DATA graphics may show a scale on screen with no VO change.
- **No rework:** 021 (live), 022 (scheduled), 023 (v05e approved) and 024 (v05 in review).

## Reference lessons (HOTU + SEA, 11 Oct 2026)

Chief studied two more reference channels on 11 Oct 2026. *History of the Universe* (HOTU) was read through `cqGhCCDC_Sw`, *Have We Finally Proven Einstein Wrong?*, and SEA through `7oR0Pmd-WIk`, *Higgs Boson: The God Particle*. The evidence is in `/workspace/hotu-pack/TAKEAWAYS.md` and `/workspace/sea-pack/TAKEAWAYS.md` on the box. Ben delegates creative calls to Chief and the AIs, and these are Chief's calls. They add to *Teach on screen*, *Polish pass* and *Packaging*.

**These hard rules don't change:**
- the line-1 claim, the first concrete answer before 0:30 and the question by about 0:50;
- the 22–27 s / under-40 s Shorts lock (plus the one *Packaging* length test);
- the yellow hook word;
- every `picture_qa`, `polish_gate` and `music_gate` FAIL.

Where a lesson below meets one of them, the rule wins.

**1. Craft lessons (Claude writes them into scripts and shot lists; Chief scores them at review).**
- **Structure.**
  - Each chapter opens cold, on a quote, a scene or a question.
  - Each chapter ends on a question the next chapter answers.
  - At about 60% of the runtime comes a midpoint twist: "Case closed? Wrong."
  - Near the end, raise the scariest idea, explain it away with reasoning, then give a short sign-off. On Orbit the sign-off is the existing hand-off line to the next film: no goodbye, and no subscribe ask (that Never stands). It fits *Wonder, not threat*.
- **People.**
  - Every named person gets a year card (the WHO card) plus a cut-out portrait with gentle parallax. Use only a portrait we can source.
  - Use rivalries where the history has them, told with back-and-forth portrait cuts.
- **Hard ideas.**
  - Put a quirky, concrete, sourced anecdote just before the hard idea (HOTU's cigar smoke).
  - Show hard maths as a physical object: a slider that stops at a limit and then breaks past it (Bell's 2.0 → 2.83), or a map of icons that light up (loopholes).
  - Jump between micro and macro scale.
  - Make big numbers tangible on a scale card ("5 sigma = 1 in 3.5 million"). That's the SCALE rule, shown.
- **On screen.**
  - Keywords flash as they're spoken, with a plain-English sub-line, inside *Teach on screen*'s limit of 4 words or fewer per label.
  - Years that fill the screen are the WHEN call-out.
  - Give every shot a slow push-in or pull-out where it has no camera move of its own. It must be smooth: polish_gate fails wobbly pushes, and a card is never Ken-Burned.
  - Use a recurring "case file" chapter card with a low bass thud.
  - Show an old diagram with glowing light traced through it only as **our own redrawn code graphic**: a sourced diagram or scan is still a `picture_qa` FAIL here.
- **Sound.**
  - SFX on name cards and photo reveals (the house tick or whoosh).
  - Music follows the emotion and changes by chapter (*Polish pass* 2). Near-silence at the key reveal is allowed, but the bed may dip for 6 s at most, or `music_gate` fails it as a gap.
  - Cut to a human reaction at the emotional peak: a sourced archive face, or Orbit in Omni.
- **Banned (weak spots):**
  - **The same photo used 5 or more times.** Orbit's existing rule is stricter (a still appearing more than twice FAILs `picture_qa`), and it stands.
  - **Generic glowing-dot or particle filler** standing in for a real subject.
  - **Holding back the answer.**

**2. Packaging rules.**
- **Cover text never repeats the title** (§2.3, now backed by HOTU and SEA: their losers' covers repeat the title).
- **Titles need a big subject plus one hook.** The hook is one of the six shapes, or one of three more: a famous nickname (*The God Particle*), the viewer inside the subject (*You Live in a Supervoid*), or a journey to the edge (*Journey to the Edge of the Solar System*). Catalogue labels (*Planetary Ring Systems*) fail (`THUMBNAIL_AND_TITLE_RULES.md` §1 rule 11).
- **Descriptions** carry, in order:
  1. the subject line;
  2. chapters named as story beats (*Einstein vs Bohr*, not *Quantum Entanglement*), one per chapter card;
  3. the Sources line;
  4. the image and agency credits;
  5. **one honest line on how the film is made**, for example *"Pictures: AI-generated scenes alongside NASA/ESA imagery. Facts: every number is checked against the sources listed below."*

  Never claim "no AI", and never name the AI checkers. Say a person checked the facts only when one actually did. The altered-content disclosure stays on.

**3. Shorts rules.**
- **The myth-bust opener is an allowed format.** Line 1 states a belief people hold ("You've probably heard the Moon is drifting away"), and **"No"** (or the reversal) lands by about 0:15. It sits inside the 22–27 s lock and the six opening rules (the named thing moving at frame 0, the claim as the first words).
- **No straight trailers.** A Short is never a clip trimmed from the long and posted as is. Every Short has its own open, frame 0, hook caption, 9–14 s title and loop (lesson: every Short gets its own open), and stands alone without the long.
  - Already uploaded: `TtgHNLXfDSs`, cut from the long, isn't reworked.
  - Exception: the *Packaging* length test (J0134). It lifts a stretch of the locked long so that it spends nothing, but its brief requires its own open, title card and loop, so it isn't a straight trim. Chief may still rule on it.

**4. Graphics go to Codex** (`--kind chart`, `gpt-6-astra`, per *Who does what*): the limit slider, the lit-up icon map, the number scale card, the traced-diagram graphic (redrawn) and the case-file card. Each one is a per-film `code_graphics.py` render for its own row, like every code graphic.

**5. Suggestions to test, not rule changes.**
- **(a) No cover text.** SEA's top two longs have no cover text at all. One Test & Compare runs on one live long: the live thumb (A) against the same plate with no text (B). It's queued as a Studio job, parked for Chief's review before the test is set. Until a winner is called, the yellow-word rule stands.
- **(b) The near-black cap.** SEA's winners run 51% near-black with a lit, glowing subject in the centre. The proposal is to count the lit subject, not the share of black. It's recorded in `audits/THUMB_AUDIT_2026-10-04/AUDIT.md` as a proposal only. The ≤30% cap and `thumb_preview.py --score` stand until Chief adopts a change here.

**6. Per-chapter teaching gate (Chief, 12 Oct 2026; Orbit Auditor scores it, from 024 on).** Jupiter `-jmMROGoZCM` went live with no teaching labels at all. So on every long from 024, the Orbit Auditor scores each chapter PASS or FAIL in the pack's review note, alongside Chief's *Teach on screen* review gate:
- **NUMBER:** the chapter shows at least one number as an object (a slider, scale card, graph, counter or timeline), not only spoken. A chapter with none FAILs.
- **WORDS:** every on-screen keyword or label matches the VO word for word at the moment it shows. A label that paraphrases or contradicts the VO FAILs.
- The note lists every chapter with its result and the timestamp of its number object. The gate result per chapter is the measure; its growth effect only shows in Studio's average % viewed, which the Auditor reports as UNKNOWN unless someone reads Studio.
- It adds to *Teach on screen* (DATA 3 or more per long, labels of 4 words or fewer from the line being spoken) and relaxes nothing. Films already live, scheduled or approved aren't reworked; on a VO-locked film it's met with overlays only.

**Applies to:** scripts locked from 12 Oct (030 on) for structure and people. Shot lists and cuts from 12 Oct get the picture and sound items, within each film's VO lock. Packaging applies to every new upload package. Nothing that's live, scheduled or approved is reworked.

## Packaging (Astrum ref, 11 Oct 2026)

**Reference channels (Ben, 4 Nov 2026: melodysheep, SEA, Astrum).** Goal: Shorts to tens of thousands of views, longs to thousands. From these channels we take: sell the real picture (LEARNINGS 18), one clean real-image thumbnail concept (19), named series with playlists and end screens (20, a rule), a monthly 40-60 min journey film made from our longs (21), and one tentpole film a month (22, November is 032). The score already follows the chapters (*Polish pass* 2); a tentpole's bed also lifts at its reveals. The monthly report scores each test against the goal.

**Long titles (Ben, 4 Nov 2026):** the Chief checks every long's title before upload against LEARNINGS rule 15 (names the subject and a concrete scenario, number or stakes; 50 characters or fewer; never a vague "What happened to X?"). **Search first (Ben, 9 Nov 2026, LEARNINGS rule 26):** until a channel has 1,000 subscribers, the title starts with the plain phrase people type for the topic, and the scenario or stakes follows as a bracketed tail or second sentence (70 characters at most). A topic go/no-go names that phrase and two videos that already rank for it. The last four longs got 6 to 32 impressions each. **Title first, test second (10 Nov 2026):** the search-led title is set before any title test is armed, and it is side A of that test. Studio cannot change one side of a set title test: *Edit title* and *A/B testing* both delete the whole test (HOS 007, OWB 026 and 027; J2470, J2471), and deleting a set test is on the Never list, so a film whose test was armed with two story titles airs that way unless Ben says otherwise. The description's first line can still be changed while a test is set.

Ben, 11 Oct 2026, sent `@astrumspace`: *"anything we can learn from the thumbnails, packaging of shorts?"* Chief studied their top and bottom longs and Shorts against our last ten longs and decided the following the same night. Ben delegates creative calls to Chief and the AIs. Evidence: `/workspace/astrum-pack` on the box (contact sheets, `longs_meta.tsv`, `shorts_meta.tsv`).

**1. Long thumbnails (`THUMBNAIL_AND_TITLE_RULES.md` §2.B, which wins where it differs):**
- **Hook text names the object or dares** (THIS IS TRITON, DON'T GO HERE). No vague questions or teasers (WHAT ARE THEY?, HOW LONG?). A question is fine only if it names the subject (SIGNAL ON MARS?).
- **2–3 words in a band across the top** (or a clear edge), **never over the subject.** Keep the yellow hook word, the white rest, and the house font and outline.
- **Grade harder.** Mean saturation must be 100 or more, with a target of 120 (85 with `--pale` for a naturally pale subject). Ours ran about 94, Astrum's top about 139. Near-black stays at 30% or less. Check with `thumb_preview.py long <thumb> --out <sheet> --score`.
- **Optional:** one small white arrow on a "look at this" discovery story.

**2. Titles:** news framing ("We Found…", "We Just Saw…", the mission name) is allowed on a real, dated new result (§1 rule 10). The hedge and threat bans stand.

**3. Review gate.** Chief and the Orbit Auditor score every new or rebuilt long thumb in the pack's review note, PASS or FAIL:
- **HOOK:** it names the subject or dares.
- **BAND:** 2–3 words in a top band or clear edge, none over the subject, yellow hook word.
- **GRADE:** `--score` PASS.
- **PHONE:** readable at 168×94.

Any FAIL goes back to the builder before the thumb is set. Live thumbs aren't reworked, except the five that break the band rule: Andromeda `ojk-dfOpAmw`, Neutron Star `Yk1tLh23rko`, Europa `NbW5G1BpPY0`, Last Star `REXYxuLOBoI` and Black Hole `3xrxdmaOwJI`. They're rebuilt in one Studio job. Rollback copies are kept, and Chief reviews before they're set.

**4. Shorts packaging.** Ours already open full-frame on the subject with word-by-word captions, as Astrum's do. No change.

**5. Short length test: a Chief-OK'd one-off exception to the 22–27 s lock (11 Oct 2026).**
- Astrum's Shorts mostly run 55–80 s, and ours run 22–27 s. So **one** Orbit Short of 50–60 s runs alongside the usual three.
- **The Short:** a stretch lifted from the locked 025 long `Js6EQJ8qDi8`, with no new VO, picture or bed, so nothing is spent.
- **The slot:** Thu 12 Nov 2026, 11:30 London. That's 025 week, after the four-week test, and the only Short that day.
- **The gate:** `gate_shorts_open.py check … --length-test` (band 50–60 s, FAIL at 61 s). Every other Short rule applies.
- **The read:** the Orbit Auditor logs it against that week's Mon/Wed/Fri Shorts (`iyvWYFP_ETA`, `TtgHNLXfDSs`, `bSjWiCbB7pY`) in its next numbers report, in `00_Brand/Channel-Setup/audits/SHORT_LENGTH_TEST_2026-11/TEST_LOG.md`.
- **What it doesn't change:** every other Short stays 22–27 s and 55–65 words, and the 40 s Never line holds for everything else. One Short is a signal, not a verdict. Chief decides whether to run a second test; the lock changes only by a new entry here.

## Topic pick — neighbour pass (blocking · 1 Oct 2026)

Before asking Ben to lock a topic, run the **neighbour pass** in `STUDIO_PLAYBOOK.md` §2: at least **three** big education/space videos (≈1M+ views) on the same subject, logged in `templates/TOPIC_OPPORTUNITY_SCORE.md` and `PRE_BUILD_VIDIQ_AUDIT.md`. Use their subject words for description first lines and tags — **never** put channel names in the listing. A strong neighbour pool is evidence for Ben; it does not pick the topic for him. Orbit only — do not apply HOS packaging habits here.

## Never (this channel's additions)

These add to the Never list in `AGENTS.md`. They remove nothing from it.

- **Publishing:**
  - Premiere a long.
  - Put Orbit at frame 0 of a Short or on any thumbnail.
- **Subscribe asks:** at the end of a film, or with a subscriber number in the film. One mid-film beat only, and the count goes in the pinned comment.
- **Titles:** hashtags, series suffixes, hedged claims ("We may have…"), fear framing, or a title that copies an existing public video.
- **Generation:**
  - Use Kling, Seedance or ElevenLabs Image & Video.
  - Omni the whole film or world B-roll.
  - Use any voice other than Ben Orbit Narrator.
- **Social:**
  - Post any way other than the Buffer mirror (`STUDIO_PLAYBOOK.md` §12).
  - Schedule a Buffer post for any time other than the YouTube go-public time.
  - TikTok: connect, upload or retry while it's paused.
