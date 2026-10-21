# AGENTS.md — Orbit With Ben studio

Read this first, whatever agent you are (Cursor, Claude Code, Codex or others). It says what this repo is, which docs are in force, and what never to do.

> **Handover (12 Oct 2026):** `HANDOVER.md` is the master index for every repo, plus pending decisions, credit floors, and what lives outside git.

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

## Where things live

| Path | What |
|---|---|
| `00_Brand/Channel-Setup/` | The docs above, `VIDEO_BACKLOG.json`, `PINNED_COMMENTS.json`, `PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md`, `templates/` (incl. `SUBSCRIBE_BEAT_LINES.md`), `ideas/`, channel description and keywords |
| `00_Brand/Channel-Setup/tools/` | `gate_shorts_open.py` (Shorts ship gate), `thumb_preview.py`, `weekly_public_audit.py`, thumbnail builders |
| `00_Brand/Channel-Setup/could-orbit-survive/` | The Wednesday test format, three scripts, `TEST_LOG.md` |
| `00_Brand/Channel-Setup/audits/` | Current audits, `weekly/` reports, `shorts_open_library/` (gate data) |
| `00_Brand/Channel-Setup/social/` | Buffer mirror: `BUFFER_CHANNELS.json` (channel ids), `UPLOADS.json` (YouTube id → local file and long), `BUFFER_POSTS.json` (what was posted), `buffer-plans/`. Buffer is the only route to social. TikTok is paused. |
| `01_Orbit-Character/` | Canonical Orbit stills (`05_Seedance-References/orbit-seedance-reference-16x9-v01.png`) |
| `02_Video-Projects/NNN_Slug/` | One folder per film. Start from `_template_NNN_Episode-Slug/`. |
| `04_Audio/tools/` | `orbit_voice.py` (VO settings), `orbit_gemini_veo.py` |
| `05_Analytics/` | Channel tracker (6 Oct 2026), OWB + HOS: `<channel>/snapshots/<date>.json` (every video, daily), `channel_daily.json` (YouTube Analytics), `<channel>/REPORT.md` (daily/weekly/monthly growth and every video), `dashboard/` (template + built page). Written by the Mac's 06:40 job; never edit by hand. |
| `07_Content-Ops/` | Local CLIs (no web app, no database): script review, episode gate, YouTube package upload, retitle, pinned comment, Buffer mirror, analytics. The hosted ops dashboard was retired on 27 Sep 2026 (`_archive/07_Content-Ops/`). The live `/go` affiliate door remains on Vercel project `orbit-content-ops` — **git auto-deploy is off** (canceled Ignored Build Step deploys still count toward the 100/day Hobby quota). Ship `/go` only with Chief OK via `cd 07_Content-Ops && vercel --prod` (see `07_Content-Ops/README.md`). |
| `scripts/` | Desktop Studio CDP helpers for Studio-only jobs (thumbnail covers). **The Orbit Studio browser is CDP port 9223.** 9222 is the HOS Flow browser, signed into Ben's personal channel, and Orbit video pages fail there (Cursor, 9 Oct). `owb_thread.py` (Chief ↔ Claude on PR #99) |
| `docs/ORBIT_PLAYBOOK_LESSONS.md` | Tonight's standing rules (neighbour, edit, production locks, thread protocol) |
| `_archive/` | Superseded docs, rules, one-off scripts and old audits. **Ignore unless asked.** |

## Commands

```bash
cd 07_Content-Ops && npm run review:script -- --file <script.md>          # long script must score ≥90
cd 07_Content-Ops && npm run gate:episode -- --project ../02_Video-Projects/<NNN_Slug>
python3 00_Brand/Channel-Setup/tools/gate_shorts_open.py check <short.mp4> --air-date YYYY-MM-DD
python3 00_Brand/Channel-Setup/tools/thumb_preview.py long|short <thumb.jpg> --out <sheet.jpg>
cd 07_Content-Ops && npm run youtube:package -- --package <…/11_Upload-Package> --video <mp4> --dry-run
cd 07_Content-Ops && npx tsx --env-file=.env scripts/retitle-videos.ts --file <fixes.json> --dry-run
cd 07_Content-Ops && npx tsx --env-file=.env scripts/update-pinned-comment.ts --dry-run    # weekly: subscriber thank-you in pinned comments
cd 07_Content-Ops && npx tsx --env-file=.env scripts/buffer-mirror.ts mirror --video <id> [--long <longId> --media <mp4> | --thumb <jpg>]   # only for uploads not made with youtube:package (it mirrors itself)
cd 07_Content-Ops && npx tsx --env-file=.env scripts/buffer-mirror.ts check    # daily at 07:05 on the Mac: keeps Buffer in step and mirrors any scheduled upload not in Buffer yet
# every upload package carries social copy (manifest `social`: hook, question, alt) and, for a long, Trailer/<slug>_trailer.mp4 (STUDIO_PLAYBOOK.md §12)
# every long's description carries one 'Sources:' line (4-6 papers or official fact sheets behind the spoken numbers, from SOURCES.md rows with an exact quote; author, year, journal, what it backs), before the image credits. Never name the AI checkers.
cd 07_Content-Ops && npx tsx scripts/buffer-mirror.ts register --video <id> --media <mp4> --long <longId>    # after uploading by hand, so the daily check can find the file
cd 07_Content-Ops && npm run youtube:auth    # once, or when a script says the YouTube login expired
python3 00_Brand/Channel-Setup/tools/weekly_public_audit.py
cd 07_Content-Ops && npm run analytics:snapshot [-- --channel owb|hos]   # daily at 06:40 on the Mac (launchd/analytics-snapshot.sh, own worktree): read-only stats for every video
cd 07_Content-Ops && npm run analytics:report    # rebuilds 05_Analytics REPORT.md + dashboard from the snapshots (no network)
python3 00_Brand/Channel-Setup/tools/gate_upcoming.py --snapshot <owb snapshot> --uploads 00_Brand/Channel-Setup/social/UPLOADS.json --media-root <checkout> --out 05_Analytics/owb/UPCOMING_SHORTS_GATE.md --add   # runs in the 06:40 job: gates every Short scheduled in the next 14 days, report only
cd 07_Content-Ops && npx tsx --env-file=.env scripts/youtube-auth.ts --analytics owb|hos    # Ben, once per channel: read-only YouTube Analytics sign-in
python3 scripts/owb_thread.py post -f report.md    # Chief of Staff -> Claude (draft PR #99); `read` / `wait` for the reply; `status` = unread check (exit 10)
python3 00_Brand/Channel-Setup/tools/clip_check.py <shot_list.csv> [--words vo_words.json]   # assembler pre-delivery: VO ends vs cuts
python3 scripts/sfx_kit.py make --out-dir <film>/06_Sound-Effects/kit_v01 [--house hos]   # house SFX (own synthesis, no spend)
python3 scripts/sfx_kit.py level --vo <vo stem> --sfx <sfx stem> --bed <music stem> --minutes <len>   # SFX level rule (Polish pass)
```

The YouTube scripts need `07_Content-Ops/.env`: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` (from `npm run youtube:auth`), `YT_ANALYTICS_REFRESH_TOKEN_OWB` / `_HOS` (read-only tracker sign-ins), and for the Buffer mirror `BUFFER_API_KEY` plus the Cloudflare R2 media host `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_PUBLIC_URL` (bucket `owb-media`, public r2.dev URL; Ben, 21 Oct 2026, after the Vercel Hobby Blob store was suspended over its limits; `BLOB_READ_WRITE_TOKEN` is used only when R2 isn't set). No database. Never print or commit their values.

## Standing lessons (Cursor + Claude)

Read **`docs/ORBIT_PLAYBOOK_LESSONS.md`** in full before topic lock, assembly, or acting on the PR #99 thread. Short form:

1. **Neighbour:** ≥3 education/space videos ≈1M+ views before topic lock; subject words in title/desc/tags; never channel names. Evidence: HOS 002 gets 55.6% of views Suggested from TED-Ed's Mendeleev film.
2. **Edit (v03b):** cards wait for the VO sentence, 0.5–0.8 s breath, ~0.4 s xfade; never clip a line; picture+music past last word, hold 2–3 s, then fade; music full runtime, and it's the film's own (lesson 7); fill 16:9 (feathered blur OK); upscale ≤~2.35×; mix ~−14 LUFS; check repeated/stumbled VO before delivery.
3. **Production:** Orbit = Omni only (+ approved 0–3 s tumble fallback); no Orbit on long thumbs; verify NASA IDs; no media in git; Chief gives the final OK (9 Oct; Claude reviews KEEP and shot lists before generation); Vertex only (Omni from location `global`); never a whole planet as an Omni/Veo start frame (it drifts to the wrong planet).
4. **Thread (PR #99 now; `scripts/thread.json` names the current one, and Claude rolls it to a new issue on the 1st of each month):** run `owb_thread.py status` at the start of every session and before saying anything is waiting on Claude; end reports to Ben with "Thread read to #<id>". Act on Claude's replies like Ben's relays. NEEDS BEN items go to Chief first (Claude's role under the 3 Oct order, Chief's since 9 Oct); only money and the truly irreversible go to Ben. Never invent Ben's own words. Never merge, close or push #99.
5. **Shorts feed (5 Oct):**
   - Judge a Short by its day-1 Shorts-feed share (50% or more means fed), not by % viewed under ~50 views.
   - Stop a topic after 2 not-fed Shorts in a row, and run at most 6 in a row on one topic; then give it a 2-week break.
   - Every Short gets its own open, with frame 0 showing the titled subject and no opening background reused from the last 10 Shorts.
   - **Test A, the opening Short (Ben, 9 Oct: yes), from 025 on:** one of each long's three Shorts is the long's own opening (the first 30–38 s of the master, reframed to 9:16, cut on a sentence end, gates as usual, Related video = the long). The weekday rotates by film. Plan, measures and readout dates: `05_Analytics/tests/SHORTS_TESTS.md`.
   - Aim for 60% or more average viewed on day 1.
   - End on the long's exact listing title and its video id, with a music bed for the full length.
   - Details: lessons doc §6.
6. **YouTube state changes leave a record (6 Oct).** Any change to a video's privacy or `publishAt`, by any agent, script or Studio click, gets a line on the thread in the same session, with the id, the old and new state, and who OK'd it. If it's a Short, update its open-gate library status in the same commit (`gate_shorts_open.py status`, or `fetch` once it's public). Lesson: `CtllH6VOhEI` was rescheduled on 1 Oct by an untracked one-off script. FIX_LOG said private for 5 days while it was live, and the Shorts gate didn't compare against it.
7. **Picture and music QA (Ben, 8 Oct, after a dated computer model at 2:54 of 025 and one music track on 023, 024 and 025).** Run one check for each before Claude's review and before anything goes to OWB UAT. The pack carries both reports.
   - **Picture:** `python3 scripts/picture_qa.py <cut.mp4> --cuts <cuts.json> --pool <pool.json> --out-dir <pack>` must PASS.
     - It names every problem at its film time (m:ss), the way Ben reports one.
     - FAIL: a computer model or reconstruction, simulation, diagram, chart, schematic or labelled image (they look dated or like a textbook); upscale over 2.35×; a still that appears more than twice (back-to-back cuts are one appearance); footage back on a stretch within 10 s of one already shown, or in more than 5 stretches; a code graphic repeated from the same render (each row's render goes in the cut list under its own file name); a run that replays its own frames; and polish_gate's low detail, split panels, near-black, noise and wobbly pushes.
     - WARN: an artist's concept, map, render, untitled source or upscale over 2×. These go on `picture_qa_review.jpg`, and Claude looks at each one full size.
     - Claude also looks at every cut on the per-row sheet and asks: would a viewer trust this as a real, sharp, finished picture of what the sentence says?
     - **The first 30 seconds (9 Oct, Gemini's idea 1):** no more than one code graphic in a row, and real moving imagery between graphics. One observatory exterior at most in the first 60 s. The first concrete answer to the title comes before 0:30, not an agenda (Codex's idea 5).
     - **A code graphic must read with the sound off (Ben, 026 and 023, 9 Oct: "hard to understand", "not a great representation of what the VO is saying").** Real bodies, not flat discs: the Blue Marble Earth, a real Venus or Moon image. Short labels are allowed and expected: at most 4 words each, taken from the line being spoken (a name, a number, "bounced back"), in large house type. Each graphic shows one idea, the one the voice is saying at that moment. Claude checks a still of every graphic against its line before the render.
   - **Music:** every film has its own score bed, at a pace that fits it.
     - Claude writes the music prompt with the shot list. It gives the film's mood and arc from the script, a `Pace: NN-NN BPM` line matched to the narration (calm explanation about 60-80, a lift only where the script builds), and what it must NOT sound like (every earlier bed).
     - Generate it once with `04_Audio/tools/generate_music_bed.py` (the API, never the website).
     - **Standalone Shorts test + compilation film (Ben, 12 Oct 2026 14:50):** 8 self-contained ~20 s Shorts (2 a week for 4 weeks, not cut from longs; a one-off exception to the 22–27 s lock) and one 45–60 min compilation from finished films. Decision and measurement: `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/`.
     - **All subscription credit floors are zero (Ben, 12 Oct 2026 14:46):** ElevenLabs, Flow (AI Ultra) and the Vertex trial are spent down to 0 (Vertex: £0.10, see below). Only subscription or trial credit: never buy credits, top up, upgrade or enable paid overage. At 0 the job fails gracefully: it walks its routing fallback, or the job type parks until the reset.
     - **ElevenLabs has no floor (Ben, 9 Oct: *"No floor on ElevenLabs. Keep going until the credit runs out."*).** One account pays for both channels' voice and music. It's a flat fee, so running out only stops work until the monthly reset; a top-up stays Ben's call. When credits are short, the channel `channel_balance.py` puts first gets them first, then air date within it.
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

## Packaging panel and the thumbnail ledger (Ben, 14 Oct 2026)

Ben, 14 Oct 2026: *"Using the data we collect, if we find Codex images perform better, let's set that up in future, and get other models to critique the titles and thumbnails and rest of packaging."*

- **Every thumbnail test goes in the ledger.** `05_Analytics/tests/THUMB_LEDGER.json` has one row per Test & Compare, naming who made A and who made B (`house`, `codex`, `cursor`, `ben`). The worker who arms a test runs `scripts/thumb_ledger.py start <id>` (or `add`, for a test that has no row yet). The read-back runs `result <id> --wt-a … --wt-b …` with Studio's watch-time share, plus CTR and impressions where Studio shows them.
- **The data decides the default.** `python3 scripts/thumb_ledger.py verdict` adds up the wins. A maker becomes the house thumbnail default once it has been one side of 4 or more decided tests and won at least 75% of them (decided = 5 or more points of watch-time share apart, or Studio names a winner). When the verdict says so, the Chief updates `THUMBNAIL_AND_TITLE_RULES.md` and the `thumb` chain. Until then, every new design goes in as B against the live thumbnail. Claude reads the verdict at each read-back and posts it on #99.
- **The packaging panel.** Before the Chief passes a title, thumbnail or upload package, `scripts/packaging_panel.py --slug <film-slug> --what "<what>" --files … --git` queues one critique each for Codex, Gemini and Cursor. They're independent: none reads the others. Each scores title, thumbnail at 168 px, the title-and-thumbnail pair, the hook, and the description, gives a concrete rewrite for anything under 8, and names the single change that would most raise CTR. A Claude job then reads all three and writes `DECISION.md`: keep, change (with the exact text), or the best alternative to build as B (a `thumb` job for Codex). Critiques are kept in `05_Analytics/tests/panels/<slug>/`. A critic's view is advice; the Chief decides.

## Who does what (11 Oct 2026)

Ben, 11 Oct 2026 21:48: *"Make sure all the tasks are correctly dedicated to the correct LLM that can do the job."* Each kind of job goes to the model that does it best, with its fallbacks in order. Ben, 11 Oct 2026 23:40: *"if Claude Code is out of usage you can use a Claude model in Cursor."* And at 23:47: *"Remember we also have Gemini and Codex."* So each kind has a **full fallback chain**, walked in order whenever a worker is out of usage or rate-limited, never parked while anyone further down is up. A Claude job goes **1) Claude Code → 2) Cursor on the Mini running Claude** (`cursor-claude-opus-5-5` = `agent --model claude-opus-5-5`, the same Opus tier) **→ 3) Gemini** (`agy`) for reasoning, scripts, listings and review notes **→ 4) Codex `gpt-6-astra`** as the last resort. Code and graphics go to Codex first. The chains live in `scripts/routing.py` (`CHAINS`). The code copy is `scripts/routing.py` (`test_routing.py` checks this table against it), and a queue job carries its kind (`jobs.py add --kind …`). Model ids are the ones configured on the Mac mini on 11 Oct 2026. Never write a model name that isn't installed.

| Job type | `--kind` | Primary | Fallbacks, in order |
|---|---|---|---|
| Script writing and fact research | `script` | Claude · `claude-opus-5-5` | 1. Cursor on Claude · `cursor-claude-opus-5-5` · 2. Gemini Argon · `gemini-argon` · 3. Codex · `gpt-6-astra` (last resort; a stand-in's draft is a draft only, Claude or Chief locks it) |
| Sources and claims check (SOURCES.md, CLAUDE_CLAIMS) | `facts` | Gemini via `agy` · `gemini-agy`, run by the Mini worker as `<driver>/gemini` | 1. Gemini Argon woken directly · `gemini-argon` · 2. Claude · `claude-opus-5-5` (its quote check against the sources) · 3. Cursor on Claude · `cursor-claude-opus-5-5` · 4. Codex · `gpt-6-astra` |
| Script review, reasoning, KEEP, shot lists, music prompts | `review` | Claude · `claude-opus-5-5` | 1. Cursor on Claude · `cursor-claude-opus-5-5` · 2. Gemini Argon · `gemini-argon` · 3. Codex · `gpt-6-astra` (advisory; Chief decides) |
| Voice-over | `vo` | ElevenLabs `eleven_v3`, Ben Orbit Narrator, API only (`vo_take.py`), Scribe `scribe_v2` check; run by Cursor | the same, run by 1. Codex, 2. Gemini. No other voice, ever: out of credit means wait for the reset |
| Stills, plates and thumbnail art | `image` | Master frame or NASA plate first, else Vertex `gemini-2.5-flash-image` (no text in it); run by Cursor | the same, run by 1. Codex, 2. Gemini |
| Charts, graphs, overlays, people cards, date call-outs, thumbnail builders | `chart` | Codex · `gpt-6-astra` (our own code graphics in Python/ffmpeg, one render per row) | 1. Cursor on Grok 4.7 · `cursor-grok-4-7` · 2. Cursor · `cursor-auto` · 3. Gemini · `gemini-agy` |
| Thumbnail design: the whole thumbnail (art, character, hook text) and its Test & Compare variants | `thumb` | Codex · `gpt-6-astra` (Ben, 14 Oct 2026: Codex built NO WAY OUT? and NO SOLID GROUND?, clearly stronger than the house style; each new design goes in as Test & Compare B against the live thumb and the result decides) | 1. Cursor on Grok 4.7 · `cursor-grok-4-7` · 2. Cursor · `cursor-auto` · 3. Gemini · `gemini-agy` |
| Video generation | `video` | Vertex Veo `veo-3.1-fast-generate-001` (`veo-3.1-generate-001` for one hero); Orbit only on Omni `gemini-omni-flash-preview`, location `global`; run by Cursor | the same, run by 1. Codex, 2. Gemini |
| Picture assembly, ffmpeg, code and tools | `assembly` | Cursor on Grok 4.7 · `cursor-grok-4-7` | 1. Cursor · `cursor-auto` · 2. Codex · `gpt-6.1-sol` · 3. Gemini · `gemini-agy` |
| Frame review and QA (after `picture_qa`, `polish_gate`, `music_gate` PASS) | `qa` | Claude · `claude-opus-5-5` looks at every flagged frame | 1. Cursor on Claude · `cursor-claude-opus-5-5` · 2. Gemini Argon · `gemini-argon` · 3. Codex · `gpt-6-astra` (advisory) |
| Titles, descriptions, tags, SEO | `listing` | Claude · `claude-opus-5-5` (Gemini checks any fact in it) | 1. Cursor on Claude · `cursor-claude-opus-5-5` · 2. Gemini Argon · `gemini-argon` · 3. Codex · `gpt-6-astra` |
| Studio browser tasks (CDP 9223) | `studio` | Chief · `grok` | 1. Cursor on Grok 4.7 · `cursor-grok-4-7` · 2. Cursor · `cursor-auto` · 3. Codex · `gpt-6.1-sol` |
| Merges, final OK, PASS, `AGENTS.md`, the Never list | `chief` | Chief · `grok` | none: parked for Chief |

- **Best-fit model per job (Ben, 15 Oct 2026: "choose the best fit model for the job ... Cursor doesn't always have to be on Auto, it could be on Grok 4.7, which we've still got plenty of usage left. Gemini could use Gemini Argon if it's a really complex task. And Codex, you can choose between Sol, Luna, Astra, Terra").** Cursor runs on Grok 4.7 (`agent --model grok-4.7`) unless a job names another Cursor model (Claude work on `cursor-claude-opus-5-5`); Auto is its backup. Gemini runs the hard reasoning lanes (script, review, QA, listing, claim checks) on Argon (`agy --model gemini-4-argon-high`, routing key `gemini-argon`) and simple jobs on its default. Codex: Astra for graphics and thumbnails, Sol for code. The CLI ids live in `scripts/routing.py` (`CURSOR_GROK_MODEL`, `AGY_ARGON_MODEL`, overridable from the relay's environment). A run that fails because the CLI doesn't know a model flags that model for 24 h and the job walks on, so a wrong id never stops the queue. Codex Luna and Terra join the table once the Mini has read their exact ids and what each is best at.

- **Chief (Grok Bot) owns reviews, PASS, merges, final OKs, `AGENTS.md` and the Never list (Ben, 9–10 Oct).** Claude reviews and recommends; Chief makes the call. **Real money and anything irreversible stay with Ben.**
- **Failover, then hand back (Ben).** When the primary hits its limit, the backup takes the job. Once the primary is up again, the next job of that kind goes back to it. On the Mini the relay does this by itself: a `chart` job wakes Codex with `-m gpt-6-astra`; if Codex is marked down, Cursor stands in. **Walking the chain (Ben, 11 Oct 2026 23:40 and 23:47).** When Claude Code is out of usage or rate-limited, the relay re-dispatches each waiting Claude job (`script`, `review`, `qa`, `listing`, or any job with `--model claude-opus-5-5`) to the next worker up in its chain with `jobs.py reroute <id> --to cursor --model cursor-claude-opus-5-5`, and wakes it in the same run (`agent -p --force --model claude-opus-5-5`). If Cursor is down it goes to Gemini (`agy -p`), then Codex `gpt-6-astra`. The same holds for every worker: a Cursor, Codex or Gemini run that ends in a usage, limit or sign-in error marks that worker down for 3 h and the relay hands the job to the next worker up in its chain in the same run; a rerouted job whose worker has since run out walks on. Every run is logged with the worker and model that actually ran it (`ran: J0300 by cursor on claude-opus-5-5 (lane 2 of 4)` in the relay log, and a line in `~/_desk/state/chief/runs.jsonl`). Claude counts as out when: it is marked down (`chief_relay.py down claude --reason "usage limit" --until …`), a Claude ledger note from the last 5 h says it hit a limit (`ai_spend.py record --pool claude --note "hit the 5-hour limit"`), or Claude blocked a job with a usage/limit reason (`jobs.py block <id> --agent claude --reason "usage limit …"`; that also marks it down for 3 h). Claude gets the next job of that kind after its reset. The Cursor model id is `routing.CURSOR_CLAUDE_MODEL` (env `CURSOR_CLAUDE_MODEL` overrides it if Cursor renames it).
- **A stand-in never makes a protected call:** no final OK or PASS, no merge, no change to `AGENTS.md` or the Never list, no spend past the written rules, nothing irreversible. It parks the job for Chief: `jobs.py block <id> --agent <you> --reason "parked for Chief: …" --git`.
- **"GPT-Astra" is Codex's `gpt-6-astra`.** It's a reasoning and coding model on Ben's Codex plan, not an image generator. It writes the code that draws our charts, overlays and thumbnail text. Pixels come from Vertex (above). `gpt-image-2` is ON for thumbnails (Ben, 15 Oct 2026: "use Codex GPT Image 2 to redo all the thumbnails with a higher click-through rate"): Codex makes the art with its built-in image tool on Ben's ChatGPT plan. If it asks for an API key or a payment, stop and park for Ben (real money stays his call). Each redo goes in as Test & Compare B against the live thumbnail, never a straight replace, never over a running test; the ledger (`thumb_ledger.py`) records it and the result decides. Hook text is still checked at 168 px and kept clear of the duration badge.

| Agent | Where | Runs |
|---|---|---|
| **Chief (Grok Bot)** | Mac mini app | The calls above. Drives the Mini, Studio and the studio thread. Agent id `chief` (its heartbeat). |
| **Claude** | Cloud sessions (Claude Code is also on the Mini, but the relay doesn't wake it) | `claude-opus-5-5`: scripts, reviews, shot lists, music prompts, listings, the tracker and board page. |
| **Cursor** | Mac mini (`agent` CLI, model Auto; `--model claude-opus-5-5` for Claude's jobs) | The first Mini worker: assembly, VO and picture runs, Studio stand-in, and Claude's first fallback on Claude Opus 5.5 when Claude Code is out of usage. Next in line for acting Chief (see "Chief relay"). |
| **Codex** | Mac mini (`codex` CLI 0.160) | `gpt-6-astra` for charts and graphics (first) and as the last resort for Claude's jobs (after Cursor on Claude and Gemini); `gpt-6.1-sol` (its default) for code. Third in line for acting Chief. |
| **Gemini** | Mac mini (Antigravity `agy`) | **The second check on facts and numbers.** Drafts `01_Script/SOURCES.md` with exact quotes and links, verifies every row of Claude's `CLAUDE_CLAIMS` file, and flags errors. It never rewrites spoken lines (Claude's call). Not in the Chief chain: whoever is the Mini worker runs it for facts jobs. **Also a stand-in worker (11 Oct 23:47):** the relay wakes `agy -p` itself for a job when it is next in that job's chain (Claude's reasoning, script, listing and review jobs after Cursor; any other job when Cursor and Codex are out). As a script stand-in it drafts only; Claude or Chief locks the spoken lines. No spend. |
| **Ben** | | Real money, things only he can do (his voice, logins, devices), and changes of direction. |

Every script gets a Gemini source and claims pass before VO is locked. Gemini only runs when the Mini worker or Chief starts it, so a script waiting on sources is the Chief's job to kick off.

**Quotes must be real (8 Oct 2026).** On 029, Gemini presented a sentence as an exact quote ("bright enough to cast crisp shadows") that is not in the paper it cited. So:
- Every quote in `SOURCES.md` carries the URL of the page it was copied from (an abstract, a press release or a paper page). A quote that can't be found on that page is a **FLAG**, not OK.
- Before any script is locked for VO, Claude checks the key spoken numbers (every MUST QUOTE row) against the sources directly and records it in `01_Script/CLAUDE_QUOTE_CHECK_vNN.md`. A spoken line whose quote doesn't hold up is cut or softened, never kept on trust.
- The VO job waits (`--after`) on a cloud "lock script" job, not on the Gemini job, so the Mini never claims a take before the lock.

## Job queue (7 Oct 2026)

Work goes through `scripts/jobs.py` (`jobs/queue.json`, shown in `JOBS.md` and on the Studio Kanban), not prose addressed to one agent. **A job says what it needs, not who does it**, so whichever agent is up does it.

| Agent | `--can` |
|---|---|
| Chief (Grok Bot) | `mini,gemini,any` |
| Cursor | `mini,gemini,any` |
| Codex | `mini,gemini,any` |
| Claude | `cloud,any` |

- **Claude adds every task as a job:** `jobs.py add --needs mini|gemini|cloud|ben|any --kind <Who does what kind> --title … --body-file … [--film NNN --stage …] [--after Jnnnn] [--ref <thread comment>] --by claude --git`. The thread carries the discussion and links the job id. To ask one agent by name (a second opinion from Codex, say), add `--for codex`: only that agent can claim the job, and the relay wakes it ahead of the acting Chief.
- **Every agent, at the start of every session and every loop:** `python3 scripts/jobs.py next --agent <you> --can <yours> --git`. It returns the job you already hold, or claims the next one you can do: quick jobs (`--eta` 60 or less) first, then oldest first. Exit 10 means nothing is waiting. Then `done`, `block --reason` (anything needing Ben), `release --note` at a stopping point, or `renew --eta N` if you're still on it.
- **Report each step (Ben, 11 Oct 2026 22:09: the board says "Working on X, 20% done, finished in about 30 min").** When you take a job, split it into steps and run `python3 scripts/jobs.py progress <id> --agent <you> --step 0 --of <n> --git`; after finishing each step, `--step <k> --of <n>` (k steps of n done; add `--note "<few words>"` if useful). The board's Mac mini box turns that into % done and a finish time from your pace, and it updates within a minute. Keep the same `--of` across releases and runs; the next run carries on from your last step. A job without step reports falls back to time against its estimate (never past 95%). Your "step k of n" posts on #99 can stay; the board reads the queue, not the thread.
- **A claim past its ETA is stalled,** and the next able agent takes it over. So don't sit on a claim; release it if you stop.
- A job with `--film/--stage` claims that board stage too, so the board and the queue always agree.

## Always on (Ben, 12 Oct 2026)
- **The Mini never idles.** When fewer than 3 Mini jobs are ready, the relay adds the next no-spend items from `jobs/backlog.json` (`scripts/refill.py refill`). Backlog work never spends, deletes or goes public, and ends parked for Chief.
- **Reviews are done as soon as they land.** No fixed review slot. A parked review holds only its own job; everything else keeps running. A review parked over 2 h is posted once on #99 for Chief (`refill.py escalate`).
- **Jobs start as soon as their inputs are ready.** Use `--after <job>` for inputs. A start time (`--not-before`) is allowed only with `--reset "<window>"` naming a real quota, credit or usage reset or an air date; `jobs.py` refuses it otherwise.

## Chief relay (7 Oct 2026)

Ben: the Chief of Staff is in charge, and when it's down or out of credit the next one in line takes over. **Chain: Grok Bot (`chief`) → Cursor (`cursor`) → Codex (`codex`).** The first one that is up is the acting Chief. `scripts/chief_relay.py` runs it on the Mini (launchd `com.owb.chief-relay`, every 10 min, round the clock (Ben, 7 Oct); an agent is woken only when a job is queued, plus a daytime sweep every 2 h for thread or desk tasks):

- **Grok Bot** is an app with no CLI, so nobody can prompt it to report in, and its app files only show the app is open, not that it has credit. It counts as up when it has posted on the studio thread as plain "[Chief]" in the last 3 hours, or run `jobs.py … --agent chief`. Cursor and Codex posts are tagged "[Cursor]"/"[Codex]" or say "covering", so they don't count. While Grok is up the relay does nothing.
- **Cursor or Codex:** otherwise the relay wakes the first one that's up for **one** job (25-minute cap). A run that ends with out of credit, usage limit or signed out marks that agent down for 3 hours, and the same run passes the job to the next in line.
- **A dead claim walks on (15 Oct 2026):** a job a Mini worker claimed and went quiet on, more than 45 minutes past its ETA (`CHIEF_STALL_MIN`; a run is capped at 25), is handed to the next worker in its chain, the same way as a usage limit. Evidence: Gemini held J0258 for 3 h past its ETA, the board showed it running, and nobody took it over. Chief-kind jobs and jobs Claude holds are left alone.
- **Grok takes back over by itself:** its first post on the thread after its credit returns makes it Chief again, and the others stand down. Nobody flips anything by hand.
- Each change of Chief is posted once on the thread ("Chief relay: … is acting Chief"). If all three are down it says so once; top-ups stay Ben's call.
- Commands: `chief_relay.py status` (who's Chief and why), `down <agent> --reason … [--until …]`, `up <agent>`, `seen chief`. Pause: `touch ~/_desk/state/chief-relay.pause`.
- **Gemini isn't in the chain.** It's the checker and can't run the Mini, so whoever is acting Chief runs it (`agy`) for every job that `--needs gemini`. `status` shows it on its own line.
- **Thread posts name the writer:** the relay sets `OWB_AGENT` for the CLI it wakes, so `owb_thread.py post` writes "[Chief] [Cursor] …" or "[Chief] [Codex] …". Grok's posts stay "[Chief]".
- **Long work outlives the 25-minute run:** renders, big downloads and batches start detached in `tmux` with a log and a `.done` file. The run releases the job with a note naming them, and the next run checks the `.done` file. Never start a second copy of a render that's still running.
- **If the Mini goes quiet:** Claude's 2-hourly check runs `jobs.py watch`. If Mini work is waiting and nothing has touched the queue for 3 hours, it posts here and pushes Ben's phone once. It also pushes Ben when a job needs him or is blocked on him.
- **Acting Chief** uses its own agent id everywhere (`--agent cursor`, `--by codex`), never `chief`. Only Grok Bot is `chief`, because that id is Grok's heartbeat. Its reports start "<Name> covering".
- **Routing (11 Oct 2026):** before it wakes a worker, the relay reads the next job's `kind` (or `model`) and wakes the worker whose model does it best ("Who does what"), passing Codex its model with `-m` and Cursor `--model` when it runs Claude's work. If that worker is down, the other stands in, and the relay goes back to the primary for the next job once it's up.
- **Claude is acting Chief until Grok Bot is back (Ben, 14 Oct 2026: "Grokbot is out of credits until Friday, so you should be taking over as the main agent to run this as chief").** `scripts/chief_override.json` names Claude until Fri 16 Oct 18:00 UTC. While it holds, Claude has everything this file gives Chief (reviews, PASS, merges, final OKs, `AGENTS.md`, the Never list); a "[Claude] acting Chief" post on #99 or HOS #180, or a job added `--by claude` saying "Ben approved (relayed by Claude as acting Chief)", is full Chief authority. The Mini CLIs run the queue as **workers only** (as when Grok is Chief) and park protected calls for Claude. Grok's first post on the thread ends it early; past `until` the normal chain applies again.
- **Out of credit, per model (Ben, 14 Oct 2026: "add a flag onto the system ... and switch it then to Codex or to Cursor or to Gemini ... up 24/7").** `scripts/credit_flags.json` lists what is out and until when: a model id (one lane, e.g. `cursor-claude-opus-5-5` when Cursor's "Other Models" pool is used up but Cursor Auto still has credit) or an agent id (all its lanes, e.g. `chief`). Claude or Chief keeps it current from the credit readings with the real reset time and removes a flag when a pool is topped up. The relay skips flagged lanes, so every job goes to the next worker and model in its chain that has credit; a run that says out of credit on a model with its own pool (`routing.SEPARATE_POOLS`) flags only that model for 3 h and the worker stays up. `status` lists the flags in force.
- **Out of usage, switch, switch back (Ben, 14 Oct 2026: "if ever an agent like yourself is down, out of usage for a few hours, make sure we add a flag ... switch to the next model down, and when you or Grok Bot are back online, it switches back automatically").**
  - **Claude:** every Claude run (the hourly studio run, any session doing studio work) starts with `python3 scripts/claude_beat.py`. That pushes `heartbeat.json` to the `claude-heartbeat` branch. A Claude that's out of usage can't say so, so silence is the flag: no beat for 90 min (one missed hourly run) means Claude is out. A Claude that knows its reset can say it directly: `claude_beat.py --out --until <UTC> --reason "5-hour limit"`.
  - While Claude is out, the relay walks each waiting Claude job down its chain (Cursor on the Claude model, then Gemini, then Codex), and Ben's Claude-as-Chief order yields to the next one down (Cursor, then Codex) as acting Chief.
  - The first fresh beat brings Claude back with no one touching anything. Its down mark clears, every rerouted job a stand-in hasn't started is handed back (`jobs.py handback`), and Claude is Chief again.
  - **Grok Bot:** the same in both directions. It's out when flagged (`credit_flags.json` `chief`, or the relay's mark), and it's back the moment it posts on the thread as plain "[Chief]" (worker, Gemini and Claude posts don't count).
  - **Mini workers** (Cursor, Codex, Gemini): a run whose own last lines say it's out of credit or signed out marks that worker, or that one model's pool, for 1 h, and the job walks on; the mark quotes that line, so a false mark shows (a worker quoting a YouTube 429 or a Buffer 401 mid-run is not out; Ben, 15 Oct 2026). Real resets go in `credit_flags.json`. When the mark ends, the chain's primary takes its jobs again.
- **The Mini repairs itself (Ben, 14 Oct 2026: "it just seems to have ground to a halt").** On 13-14 Oct the disk had ~110 MB free and local files blocked the shared checkouts' pull, so every wake stopped at `git pull` and no job finished for a day. Each relay run now checks: if free space is under 2 GB or the OWB pull fails, it runs `scripts/mini_repair.py` (caches, clean temp worktrees, blocking untracked files moved to `~/_desk/rescue/<date>/`, local edits stashed, local commits pushed to `rescue/mini-<date>-<repo>` first; never media, never the NAS), at most every 30 min, and posts what it did. Still under 300 MB after that, it wakes nobody (a wake would only fail) and says to move render scratch to the NAS. A worker whose pull fails runs `python3 scripts/mini_repair.py --apply` itself. If the checkout is too stuck to pull the script: `curl -fsSL https://raw.githubusercontent.com/TheLaughingGod1986/orbit-with-ben/main/scripts/mini_repair.py | python3 - --apply`.
- **Fallback chains (11 Oct 2026):** every run first checks Claude (`status` shows a `Claude:` line and the workers). If Claude is out, its waiting jobs go down their chain (Cursor on `claude-opus-5-5`, then Gemini, then Codex); a worker that runs out mid-job is marked down and its job goes to the next worker up in the same run. The relay posts one line naming each move, and logs which worker ran every job (`runs.jsonl`). See "Who does what".

## Studio board and claims (5 Oct 2026)

- **State lives in `02_Video-Projects/<film>/status.json`, not in the thread.** Start every session with `python3 scripts/studio.py board`. Read the thread only for decisions. `STATUS.md` at the repo root is the same board as a page for Ben (what's being worked on, how far through, next step, ETA). `claim`/`release`/`set` regenerate it, and CI fails if it's stale.
- **Claim before you work or spend:** `python3 scripts/studio.py claim <film> <stage> --by <agent> --eta <min> --git`. This works the same for Mini jobs, Cursor, Codex and cloud Claude sessions, so a stage can't be done twice.
  - If the claim exits 75, someone else holds that stage. Stop.
  - When you finish, run `release … --state review|done --ref <sha> --git`.
- **Stalled jobs:** a claim past its ETA counts as stalled. `studio.py stale` lists stalled claims; the Mini runs it every 15 minutes and posts any hit to the thread.
- **Background jobs commit from their own clean worktree** (`git worktree add /tmp/<job>-wt origin/main`), never from the shared Mini checkout. On 5 Oct, uncommitted Buffer JSON in that checkout blocked the 027 SOURCES commit for 6 hours.
- **Mini-only resources:** the ElevenLabs pool, Vertex and Studio writers also keep their `desk-lock` (`07_Content-Ops/scripts/desk-lock.sh`).
- **VO takes:** use `04_Audio/tools/vo_take.py` (`--script` for a long, `--text` for a Short or pickup; `--dry-run` first). It locks the voice, makes one take, uses the month's credits freely (Ben, 7 Oct: the plan is paid monthly, use all of it) but never goes past what's left into overage or a top-up, runs Scribe, and writes one `<stem>_TAKE.json` plus a line in `04_Audio/elevenlabs_ledger.jsonl`. Don't copy a new `_generate_*.py` for a take.

## NAS archive (5 Oct 2026)

The Synology share (`/Volumes/data/mac-mini-archive/`) is the archive, and often holds the **only** copy: the 3 Oct and 5 Oct moves deleted the Mini copies after checking them.
- **Never delete anything on the NAS.** "Looks like a partial duplicate" is not proof. On 5 Oct the HOS 003 folder held 1,090 files that existed nowhere else.
- **Moving files to the NAS:**
  1. rsync, then SHA-256 manifests on both sides;
  2. delete the Mini copy only on a full match;
  3. leave a `MOVED_TO_NAS.txt` in the Mini folder.
- **Restoring:** git-tracked files are never overwritten from the NAS; the git copy wins.
- **YouTube staging folder (Ben, 15 Oct 2026: "start utilising some of the space on the NAS... make a separate folder... clean them out when the video is definitely live").** `/Volumes/data/mac-mini-archive/youtube-staging/<film-id>/` holds finished, scheduled-or-ready videos waiting to go out, so the Mini disk stays free. Use it when the Mini is under 20 GB free or holds more than ~3 films ready to go out. Its `README_YOUTUBE_STAGING.txt` says what it is. Rules: (1) copy with rsync, check the sha256 manifest, and leave `MOVED_TO_NAS.txt` in the Mini folder; (2) the upload always reads the file back from the NAS path and the manifest records that path; (3) a staged file is deleted only when the video is **live on YouTube** (read back by the Studio check, status Public) **and** no Test & Compare, re-upload or Shorts cut still needs it, and then only that film's folder inside `youtube-staging/`. This is the one exception to "never delete anything on the NAS"; nothing outside `youtube-staging/` is ever deleted. (4) A film's final cut stays in the film's NAS archive folder too if it is the only copy of the master. (5) If the share is hung or unmounted, stage nothing and keep the Mini copy; never write into an unmounted `/Volumes/data` path (it lands on the Mini disk).
- Any job that moves files claims first (`studio.py claim … --git`) and runs in detached tmux. On STOP, its last act is to post the STOP line or set its stage to `blocked`.

## Stop and ask Ben

**Chief owns the studio (Ben's handover to Chief, 9 Oct 2026; Ben, 10 Oct 2026: *"I should not need to give permission all the time"*).** Wherever this file says Claude decides, OKs, gives the final OK or makes an exception, Chief (Grok Bot) now holds that call in place of Claude. A Chief OK is a plain "[Chief]" post on #99 or HOS #180, or a job added `--by chief`; a job brief saying "Ben approved (relayed by Chief)" counts as Ben's word. Workers act on either and never ask Ben to re-post an OK on #99. Ben is asked only for real money (past £0) and what truly can't be undone; deleting a video stays on the Never list.

**Standing order: ask Chief first, not Ben** (Ben, 3 Oct 2026, to Claude: *"Instead of asking me, always ask Claude first."* Chief has held that role since 9 Oct). Anything that used to be marked NEEDS BEN goes to Chief on the PR #99 thread first; Claude's review and recommendation come with it. Chief decides it, records the decision on the thread, and tells Ben what was decided so he can overrule it. That covers topic, scripts, voice, shot lists, pictures, titles, descriptions, tags, thumbnails, Shorts, the final OK before scheduling, renames, back-catalogue titles and covers, and edits to posts already in Buffer. Ben is asked only for:

1. **Spending money:** any top-up, new paid service or plan (see Budget).
2. **Anything irreversible:** anything going public outside a scheduled upload, and anything else that can't be undone. A scheduled upload stays reversible until it airs, so Chief can OK it. **Making a public Orbit or HOS video private is Chief's call** (Ben to Claude, 5 Oct 2026; Chief since 9 Oct): a takedown is always done by making the video private, because private can be undone, with the reason on the thread and Ben told.
3. **What only Ben can do:** his voice, his logins and accounts, and his devices (waking the Mac mini).
4. **Any change to the channel's direction** (a new series, a new format, a change of voice).

**Chief owns `AGENTS.md` and the Never list** (Ben to Claude, 5 Oct 2026; handed to Chief 9 Oct, confirmed 10 Oct). Chief changes them and OKs one-off Never-list exceptions for reversible studio actions (e.g. re-uploading a fixed copy of a broken Short, a video going private), recording each with its date and reason on the thread and in the commit, and telling Ben. Workers (Cursor, Codex, acting Chief) don't relax the Never list themselves. **Real money stays with Ben** (item 1), and no OK covers deleting a video.

**Budget:** Vertex, API and Flow credits already on the account may be spent down to zero. No top-ups, no new paid services or plans, and never AI Studio prepaid credit, without Ben.

**Credit holds until the 30 Oct ElevenLabs reset (Chief, 9 Oct 2026; Chief owns the studio since 9 Oct).**
- **ElevenLabs** (one account, both channels): about 18,653 credits left (9 Oct). The HOS voice queue goes first: 007 Shorts B + C (J0109), then the 009 and 010 long VO (J0111, J0113). Every VO job reads the balance first and spends nothing if it is below what the job needs. **No OWB (or HOS) music bed is started without the Chief's OK until 30 Oct.** Laying in a bed that already exists (J0089) is fine.
- **Vertex free trial: spend it down to £0 (Ben, 10 Oct 2026 22:50: *"use the vertex credit until its £0"*; this replaces the £5 floor).** Before each job, read the live Free Trial balance (`_vertex_credit_v01.py` must read the Free Trial row as Available, or nothing is minted) and take off any spend logged in `ai_spend.py` since that reading that billing hasn't shown yet. A job runs if that figure − its estimate ≥ £0.10; re-read after each batch and stop before a take that would go under £0.10. **Billing risk (checked 12 Oct 2026 14:50): billing account 0124D1-E6EFD6-40F6DA is a *Paid account*, so once the trial is used up Vertex would bill the card. The £0.10 is the safety margin for billing lag (Ben, 12 Oct 14:46).** A job that needs more than that would bill real money: it stops, the job type parks until new credit, and it goes to Ben. Nothing ever goes on the card; never top up, upgrade or enable overage. **HOS 006 Part 03 (J0107, ~£11.36) goes first:** until it's done, OWB jobs may spend only what's left above its remaining estimate, and anything bigger goes to the Chief.

**AI spend month (Ben, 8 Oct 2026; each plan from its own reset: Cursor 8 Oct, Google 12 Oct; check-in Sat 7 Nov, before Cursor renews).** Ben wants to know whether both channels can run on a ~£90 Claude plan, a ~£90 Google plan and ElevenLabs. So for both channels, every credit reading and every spend goes into `scripts/ai_spend.py` (ledger `05_Analytics/ai_spend/ledger.jsonl`), and the Kanban's AI spend panel shows it:
- **Readings:** record a balance (`record --pool cursor|flow|vertex|elevenlabs --left N [--total N]`) at least once a day, and whenever you read one before or after a part.
- **Spends:** record each take or VO as you make it (`spend --pool … --amount … --film HOS:006|OWB:025 --what …`). Flow is credits, Vertex is GBP and ElevenLabs is credits.
- **Claude:** note a usage-limit hit with `record --pool claude --note …`.

This is measurement only. It changes no spend rule.

**Four a month on each channel (Ben, 9 Oct 2026).** *"Each channel has 4 videos a month. If we have 4 videos already set up on Orbit and complete, then we need to work on History of Science. Allocate credits accordingly."*
- `python3 scripts/channel_balance.py --hos <HOS checkout>` counts each channel's long videos per month: planned, and complete (edit passed). The channel whose earliest month is short of 4 complete goes first. If both are short in the same month, the one further from 4 goes first.
- **Work:** the Chief relay checks it before every run. When History of Science is first, its oldest desk task goes ahead of the OWB queue. The other channel's work still runs when the first has nothing doable right now.
- **Credits** (ElevenLabs, Vertex, Flow): the first channel's spends go first.
- **Topics:** a month with fewer than 4 films planned is short too. Claude picks the topics for that channel's missing slots.

**One film at a time, then Ben watches it (Ben, 8 Oct 2026).** *"If we're working on one video, that should be the main priority and done in a day, maybe two… then I can check the video out."*
- **Focus film.** Each channel has one focus film. On OWB it's set with `python3 scripts/jobs.py focus NNN --git`, and its jobs go first in every lane. Other films' jobs come next, and admin jobs (readings, installs, disk) last. When an admin job blocks a film (a full disk), Claude marks it `python3 scripts/jobs.py urgent J00NN --git`, which puts it ahead of everything, the focus film included.
- **Render scratch (Claude, 9 Oct).** Each film keeps its current and previous render scratch in /private/tmp only. When a new pack posts, the version before last moves to the NAS (`mac-mini-archive/mini-tmp-scratch/<date>/`): copy it, check it against a sha256 manifest, and only then remove the local copy. Each version adds about 2 GB, and that filled the Mini twice. **A master is never kept only in /private/tmp (Claude, 14 Oct).** macOS purges files there after about 3 days unused. That is how the 023 Venus v05e CRF 18 master was lost before its upload. Any master that goes to Ben's watch, a final OK or an upload is copied the same run to the film's NAS folder (or OWB UAT / HOS UAT), its sha256 is checked, and the manifest records that path, never a /private/tmp one.
- **Finish it end to end.** Every agent works the focus film from picture through edit, thumbnails, package and gates, aiming for a day or two. A credit limit (HOS Flow) can stretch that, and its film note says so.
- **Ben's watch.** When the focus film is finished and has passed Claude's checks, it goes to OWB UAT. Ben is told with one push notification and the board's top line. Then the next film becomes the focus.
- **Watch window.** Ben's watch happens before upload, because a fix after upload means a fresh upload (no file swaps, no deletes). Each finished film's note gives a watch-by date. If Ben hasn't flagged anything by then, Chief's final OK and the upload go ahead, so no film stalls waiting on him. Ben signs off on the board: **Looks good** or **Needs a change** (with a note) under "Ready for you to check". That writes `checks/<OWB-022>` in the board's store, and Claude acts on it at the next hourly run.

**Studio Kanban (Ben, 8 Oct 2026).** Claude owns the page (`05_Analytics/kanban/studio_kanban.html`, published at the board's one URL) and republishes it. Other chats and agents change what it reads (`PIPELINE.json`, `status.json`, the job queue), not the page, so a republish doesn't undo their work. The board runs one lane per channel with four columns: **To do · In progress · Scheduled · Live**. Scheduled means uploaded and waiting for its air time; Live means aired in the last two weeks, and a film moves across at 18:00 on its air day by itself (Ben, 8 Oct). Its "Film by film" section answers Ben's question for every film: *what's the holdup, what is it waiting for, and when does that happen?* Claude writes those notes in `05_Analytics/kanban/film_briefs.json`. The board refreshes every hour round the clock (Ben, 8 Oct), and again each time a Mac mini post on the studio thread wakes Claude. Overnight (22:00–07:00 London) it still refreshes, but Ben gets no phone notifications; they wait for one morning summary. Each note has what's done, the holdup, any second limit, who does the next step and when (tied to the job where one exists), and what's on Ben ("nothing" when nothing is).

Once the final OK is given (Chief's since 9 Oct), the upload goes up under the standing upload rule: the package must pass every gate (`gate:episode`, `gate_shorts_open`, the `youtube:package` dry run) and go up with its Buffer posts, hook, question and trailer. Report the result (video id, go-public time, `buffer` block) straight after. The report also says, for each video, whether the thumbnail or cover was **set or refused**, read from the upload log message. A refused one (403, as on 022) is set in Studio before go-live, and so is every Short's cover, since the API's cover often doesn't show (022, 9 Oct).

**The real upload is the only run that passes `PUBLISHING_DRY_RUN=false` (Claude, 9 Oct 2026).** The Mini's `07_Content-Ops/.env` keeps `PUBLISHING_DRY_RUN=true`, so a stray `youtube:package` run can never upload. The upload job sets `PUBLISHING_DRY_RUN=false` on that one command line, only after every gate above has passed, and never edits the .env to do it.

## Never

- **Uploads:**
  - Swap the file on an existing YouTube id.
  - Re-upload an idea that already went public. (A fixed copy of a broken, e.g. silent, Short may go up on Chief's OK; the broken id goes private.)
  - Delete a video. The old id goes private instead.
- **Publishing:**
  - Premiere a long.
  - Air more than one Short a day.
  - Ship a Short of 40 s or more. (Sole exception: the one Chief-OK'd 50–60 s length-test Short, *Packaging*, 11 Oct 2026. Never over 60 s.)
  - Ship a silent or near-silent file.
  - Put Orbit at frame 0 of a Short or on any thumbnail.
- **Subscribe asks:** at the end of a film, or with a subscriber number in the film. One mid-film beat only, and the count goes in the pinned comment.
- **Titles:** hashtags, series suffixes, hedged claims ("We may have…"), fear framing, or a title that copies an existing public video.
- **Studio:** add a pinned comment to a Short. Add a `/go/` link anywhere: its redirect app is retired, and affiliate links are paused (`STUDIO_PLAYBOOK.md` §11). Press **Continue** on "Run a new test? Your current test will be deleted" when a Test & Compare is already set: Cancel and leave it (Cursor, 9 Oct).
- **Generation:**
  - Use Kling, Seedance or ElevenLabs Image & Video.
  - Generate anything on the ElevenLabs website, by any agent. VO goes through the API only, one take at a time. (4 Oct 2026: website Video Generation by desk automation burned about 67k credits.)
  - Omni the whole film or world B-roll.
  - Use a video model's speech as VO.
  - Use any voice other than Ben Orbit Narrator.
- **Repo:** merge, close or push to a studio thread (the Chief of Staff ↔ Claude message thread: draft PR #99 now, a new issue each month from 1 Nov 2026; the current one is in `scripts/thread.json`), even when told to merge all PRs.
- **Social:**
  - Post any way other than the Buffer mirror (`STUDIO_PLAYBOOK.md` §12).
  - Schedule a Buffer post for any time other than the YouTube go-public time.
  - TikTok: connect, upload or retry while it's paused.
- **Secrets:** commit or print them.

## Studio core (Ben, 15 Oct 2026)

Ben: *"unify HOS and OWB but keeping their own rules."* Tooling both channels share lives once. `studio-core/CORE_FILES.json` locks each shared file by sha256, in this repo and in history-of-science, and CI (`core-check.yml`) fails a repo whose copy differs. **Change a core file only in orbit-with-ben**, then run `python3 scripts/core_sync.py lock` and `python3 scripts/core_sync.py push --to <history-of-science checkout>`, and commit in both. A file joins the core with `core_sync.py add <path>` once it is identical in both repos. Channel rules are never core: strategy, thumbnail and title rules, the playbook, production locks, the HOS contract code, channel ids. Plan and order: `docs/STUDIO_SYSTEM_REVIEW_2026-10-15.md`.

## Changing the rules

Change the doc in force (1–8 above) and its Cursor rule in the same commit, with the date and the evidence. Don't add a new "locked" doc that restates or contradicts one of them. Move anything it supersedes to `_archive/`. Updates to standing lessons go in `docs/ORBIT_PLAYBOOK_LESSONS.md` and a pointer here.
