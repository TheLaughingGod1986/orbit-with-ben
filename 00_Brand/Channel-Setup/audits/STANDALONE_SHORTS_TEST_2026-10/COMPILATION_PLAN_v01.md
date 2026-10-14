# OWB compilation film: plan v01 (J0165)

Cursor covering Claude's `script` job (12 Oct 2026). Draft only: Chief locks the plan and the script (`COMPILATION_SCRIPT_v01.md`) before the VO (J0166).

## The thread: how long things in space last

Five finished, already-public house-format longs, ordered from the shortest clock to the longest. Each film answers "how long has it got?" for one thing in the sky, so the compilation is one countdown that runs from millions of years to trillions.

| # | Film | Public id | Runtime | Clock it ends on (already spoken and sourced in that film) |
|---|---|---|---|---|
| 1 | 021 *How Long Do Saturn's Rings Have Left?* | `55AEQwvs36g` | 9:20 | about 100–300 million years |
| 2 | 013 *Why the Moon Is Slowly Leaving Us…* | `2fsQcea-voM` | 8:39 | 3.8 cm a year; the perfect total eclipse is a passing window |
| 3 | 019 *What Happens When Andromeda Hits the Milky Way?* | `ojk-dfOpAmw` | 10:21 | billions of years (no new number in the bridge; see risks) |
| 4 | 007 *What Happens If You Get Near a Neutron Star* | `Yk1tLh23rko` | 9:43 | what a dead star leaves behind |
| 5 | 005 *What Happens When the Last Star Dies?* | `REXYxuLOBoI` | 8:38 | the smallest stars shine about ten trillion years |

- **Films:** 46:41. **New material:** intro about 60 s, four bridges of about 15 s, five chapter cards of about 3 s, and a closing of about 20 s, so about 2:35. **Total:** about 49:15 before the trims in risks 1 and 2 below, which take off about 1–2 min. That lands at 47–49 min, inside 45–60.
- **Why this five:** all are the house format (8–10 min, the current narrator and score), all public, and the thread is the channel's best title shape (the ending/countdown shape: *What Remains After the Last Star Dies?*, 622 views). Saturn's own end hand-off already names *What Happens When the Last Star Dies?*, which is where the compilation ends.
- **Left out:** 001, 002, 003 and 004 (`Mo93x0fxB1Q`, `3xrxdmaOwJI`, `b8-X_FyJnHM`, `ziKBPJ6FY0U`) are the old 16–21 min format and don't fit the thread. 006 Europa and 020 Jupiter are "what's it like" films, not endings: they're the core of an alternative compilation (below).
- **Optional sixth:** 022 *Is the Sun Getting Brighter?* (`h8HGfyShEHI`, 8:39) airs Sun 18 Oct. If the compilation goes up after that, it slots in between the Moon and Andromeda (the Sun's own clock), for about 58 min in total. Chief's call.

**Alternative thread (if Chief prefers):** "Places you can't stand": Jupiter `-jmMROGoZCM`, Neutron Star `Yk1tLh23rko`, Europa `NbW5G1BpPY0` and Saturn `55AEQwvs36g`, at about 38 min. That's short of 45 min without one of the old 20-minute films, so v01 recommends the endings thread.

## Running order (cut list for J0167)

| Time (approx.) | Item | Source |
|---|---|---|
| 0:00 | Cold-open intro (new VO + new picture from the five films' own shots) | `COMPILATION_SCRIPT_v01.md` §Intro |
| 1:00 | Chapter card 1: *The Rings Are Leaving* | code graphic |
| 1:03 | Film 021 | master, unchanged |
| 10:23 | Bridge 1 (timeline marker 1 drops) | script §Bridge 1 |
| 10:38 | Chapter card 2: *The Moon Lets Go* | code graphic |
| 10:41 | Film 013 | master, unchanged |
| 19:20 | Bridge 2 | script §Bridge 2 |
| 19:35 | Chapter card 3: *Two Galaxies Meet* | code graphic |
| 19:38 | Film 019 | master, unchanged |
| 29:59 | Bridge 3 (timeline marker 3 drops) | script §Bridge 3 |
| 30:14 | Chapter card 4: *What Dead Stars Leave* | code graphic |
| 30:17 | Film 007 | master, unchanged |
| 40:00 | Bridge 4 | script §Bridge 4 |
| 40:15 | Chapter card 5: *The Last Light* | code graphic |
| 40:18 | Film 005 | master, unchanged |
| 48:56 | Closing (timeline completes) | script §Closing |
| ~49:15 | Hold 2–3 s, fade | |

The times shift down once the trims in risks 1 and 2 are made. J0167 writes the final timestamps for the description.

## Teach on screen and Polish pass (new material only)

- **DATA (one timeline):** one countdown timeline builds across the bridges: Saturn's rings (100–300 million years) at Bridge 1, Andromeda ("billions of years", no number) at Bridge 3, and the last stars (about 10 trillion years) at the Closing. It's one code graphic per appearance (`code_graphic_owbcomp_<row>`), on a log scale, and it rides over a graded moving plate from the next film with real footage between each appearance. Each number comes from the source film's own SOURCES or quote check (021 rows for the ring rain and Cassini; 005 for ten trillion years).
- **WHEN:** none in the new lines; the films keep their own.
- **WHO:** no person is named in the new lines.
- **FACT:** none added. The films carry their own.
- **SFX:** a tick when each timeline marker drops; a low rumble under the intro's Andromeda shot. House kit only (`sfx_kit.py make`); `sfx_kit.py level` must PASS on the new material.
- **Music:** each film keeps its own bed. The intro, bridges and closing need a bed. **Credit hold until 30 Oct:** no new bed without Chief's OK. v01 proposes laying the 005 *Last Star* bed (already exists, no spend) under the intro, bridges and closing, crossfaded 2–4 s into each film's own bed. `music_gate.py` runs on the full cut.
- **Finishing:** chapter cards ~0.4 s xfade; 0.5–1.5 s crossfades from each bridge into its film.

## Packaging (draft, Claude's `listing` job if Chief wants a second pass)

**Titles (the ending/countdown shape, big subject plus one hook, under 60 characters, not a copy of a public title):**
1. *How Long Will Anything in Space Last?* (recommended)
2. *Nothing in the Sky Lasts Forever*
3. *From Saturn's Rings to the Last Star: How Everything Ends*

**Cover (no Orbit; 2–3 words in a top band, yellow hook word, never over the subject, doesn't repeat the title):**
- A: **THE LAST *LIGHT*** over a graded red-dwarf or white-dwarf plate from 005.
- B: ***100M* → 10T YEARS** over Saturn's rings from 021 (number shape).
- C: **EVEN *STARS* END** over a split of the ring plane and a dim star (needs `thumb_preview.py --score` PASS at saturation 100 or more).

**Description:** subject line, then the five chapters named as story beats with their timestamps, one `Sources:` line taken from the five films' own Sources lines (4–6 papers), image credits, and the honest line *"Pictures: AI-generated scenes alongside NASA/ESA imagery. Facts: every number is checked against the sources listed below."* Altered-content disclosure on. No subscribe ask; one pinned comment as usual.

## Risks and calls parked for Chief

1. **Five subscribe beats.** Every film carries its own mid-film `[SUBSCRIBE BEAT]` (e.g. 021: *"We make one of these every week. Subscribing is how the next one finds you."*). The Never list allows one mid-film beat only. **Recommendation:** J0167 cuts the beat out of four films on sentence boundaries (keeping 021's, the first film's, so the one beat comes early), with no other change to picture or VO. That's a trim, not a re-edit, but the brief says "no picture or VO from the films is changed", so Chief rules.
2. **Five end hand-offs.** Each film ends by naming another film (021 names *What Happens When the Last Star Dies?*). Inside the compilation they point at the wrong film. **Recommendation:** trim each film's last hand-off sentence and its hold, and let the bridge do the hand-off. 005's end hand-off is replaced by the Closing. Chief rules with item 1.
3. **"Re-upload an idea that already went public" (Never).** This compilation is Ben's explicit OK (12 Oct 2026 14:50). Chief should record it as a named one-off exception on #99 with the date, as the Never list asks. The new intro, bridges, chapter cards and timeline are the added value that keeps it clear of YouTube's reused-content policy; all the music is our own.
4. **Masters.** No long master is in the films' `09_Final-Export` folders on the Mini. 006, 013, 019 and 020 moved to the NAS (`/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/`); 005, 007 and 021 were not found by a quick search. J0167 must find each film's upload master (NAS, `~/Desktop` upload folders, or the 021 `saturn_film` export) and check its duration against the YouTube runtime above before it cuts. It must not download from YouTube, which is lower quality.
5. **Andromeda's numbers.** 019's script isn't in the repo (only on the NAS), so its bridge says "billions of years" and no figure. If J0167 or Gemini finds 019's quote check, a figure can be added at the lock.
6. **Gemini facts pass.** The new lines reuse only numbers already spoken and quote-checked in their own films (100–300 million years, 3.8 cm a year, ten trillion years, the teaspoon). A short Gemini claims pass over the script's MUST QUOTE table is still due before VO, per AGENTS.md.
7. **VO budget.** About 305 spoken words, about 1,730 characters (see script), so roughly 1.8k ElevenLabs credits for one take at eleven_v3. It's queued behind the Shorts test VO (Chief, 12 Oct 14:53).

## Measure

After 4 weeks live: views, retention (APV/AVD) and subs gained, against the same weeks' Shorts cut from longs and the longs. Logged in `TEST_LOG.md` in this folder (a row is added at upload).
