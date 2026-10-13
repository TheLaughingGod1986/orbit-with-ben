# OWB compilation film: assembly status (J0167)

Cursor, 12 Oct 2026. Locked order per Chief's masters ruling on #99 (6131339524): 021, 013, 019, 007, 005. Nothing cut, uploaded or spent yet.

## Masters (step 2 of 8 done)

| # | Film | Master | Source res | Duration | Plan | Delivery |
|---|---|---|---|---|---|---|
| 1 | 021 Saturn `55AEQwvs36g` | Mini `021/07_Edit-Project/saturn_film/saturn_first_cut_v03f.mp4` | 1080p | 9:19 | 9:20 | as is |
| 2 | 013 Moon `2fsQcea-voM` | NAS `Desktop/MOON_LEAVING_FULL_v04_WATCH_THIS.mp4` | 1080p | 8:39 | 8:39 | as is |
| 3 | 019 Andromeda `ojk-dfOpAmw` | NAS `019/07_Edit-Project/rough/andromeda_collision_rough_v06.mp4` | 720p | 10:20 | 10:21 | lanczos to 1080p |
| 4 | 007 Neutron Star `Yk1tLh23rko` | Studio owner download, `007/09_Final-Export/neutron_star_STUDIO_OWNER.mp4` | 720p | 9:42.9 | 9:43 | lanczos to 1080p |
| 5 | 005 Last Star `REXYxuLOBoI` | Studio owner download, `005/09_Final-Export/last_star_STUDIO_OWNER.mp4` | 720p | 8:37.4 | 8:38 | lanczos to 1080p |

- The two owner downloads were taken from YouTube Studio's own Options > Download on the Orbit Studio browser (CDP 9223). Nothing on either video was changed (title, privacy and schedule untouched).
- Both are copied to the NAS at the same relative path under `mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/`. The sha256 matches on both sides: 005 `9e336a65…0308d1`, 007 `8a8ae897…a76c2d`. Media stays out of git.

## Trims (step 3 of 8 done)

Word timings for all five masters finished (local `faster_whisper` medium.en, no spend; `/private/tmp/owb_comp/words/<film>.json`). Every cut sits in a measured VO gap (50 ms RMS), never on a word. Full list with times: `COMPILATION_TRIMS_v01.json`.

| Film | Out at | What goes | Hold after last word |
|---|---|---|---|
| 021 | 9:00.2 | spoken hand-off "What happens when the last star dies?" | 0.3 s, then crossfade into Bridge 1 |
| 013 | 8:20.8 | ~18 s moonlit-sea outro (no spoken hand-off) | 2.8 s |
| 019 | 10:12.8 | galaxy outro (no spoken hand-off) | 2.7 s |
| 007 | 9:29.4 | "Follow Orbit… like and subscribe… Thanks for watching" and the end card | 2.2 s |
| 005 | 8:08.1 | Katie Mack book plug, the sign-off and outro (the Closing replaces them) | 0.2 s, then crossfade into the Closing |

Films kept: 45:11. With the recorded VO (2:10), breaths, holds and five cards, the cut lands at about **47:50**.

**Subscribe beats: the plan's premise was wrong. Chief to confirm at J0168.** Only 021 has a mid-film beat ("We make one of these every week. Subscribing is how the next one finds you.", 3:29.7–3:39.6 in the film, 9.9 s with its music tail). 013, 019 and 005 have none, and 007's ask is its end card, trimmed with the end. Chief's lock kept "the last (005's)", which doesn't exist. The default keeps 021's, so the film has exactly one mid-film beat (the Never list allows one). To run with none, set `apply: true` on that cut; it's a 0.6 s-breath cut on a measured gap.

## Plates (step 5a done, 12 Oct 21:20Z)

Plate picks for the intro, the four bridges and the closing are in `COMPILATION_PLATES_v01.json`: one ~6 s window from a film's own passed cut per spoken line, checked on contact sheets and single frames. No window is used more than twice, none in its film's first 30 s for the intro, and none sits next to its own film's out point. Four picks are marked "verify" at full size before render.

**Open for Chief: the bed.** 005 has no music stem anywhere (Mini, the NAS 005 folder, NAS Desktop), so "the 005 bed under the new material" can't be laid as planned. Cursor recommends lifting music-only stretches from the films' own trimmed outros (no spend), with Chief ruling whether music_gate's "sounds like another film's bed" check is waived for a compilation. The alternatives are a new bed (needs Chief's OK under the credit hold until 30 Oct) or the house SFX drone only.

## Segments v01 (step 5b, 12 Oct 21:57Z)

`_assemble_compilation_segments_v01.py` builds the intro, the four bridges and the closing from `COMPILATION_PLATES_v01.json`. Each plate covers one spoken line, timed from the VO's Scribe word times. Master audio is muted, the cut is 1080p30 lanczos with a 0.4 s xfade, the lead-in is 0.6 s and the tail 0.8 s (2.6 s plus a fade on the closing). The house kit is in `06_Sound-Effects/compilation_kit_v01` (own synthesis, no spend), with a rumble on the Andromeda line. All six rendered (tmux `J0167-seg`, exit 0) to `/private/tmp/owb_comp/segments_v01/` on the Mini. Each segment has its mp4, separate `_vo.wav` and `_sfx.wav` stems, a picture_qa-format `_cuts.json`, and contact sheets `sheet_intro.jpg` and `sheet_bridges.jpg`. Lengths: intro 54.1 s, B1 16.8, B2 13.7, B3 17.9, B4 14.2, closing 23.3. There is no bed and there are no cards yet. The VO stem sits at about −20 LUFS raw and gets normalised at step 6.

**The contact sheet found three re-picks, needed before step 6** (they go in a v02 of the plates file):
1. **intro_10** ("We start with the shortest clock…", 005 @345, 11.9 s): after about 2 s of the ringed grey world, the shot becomes Orbit in front of a wall of molecule diagrams for about 9 s. That risks a diagram FAIL and doesn't match the line. Keep the first ~4 s and cut to a second window (a long clock or starfield shot that isn't a diagram).
2. **bridge2_01** ("The Moon lets go a few centimetres at a time.", 013 @120): it's the Moon-forming debris impact, so it fails the plate's own "verify". Use the plan's fallback, 013 @420 (second use).
3. **closing_01** (005 @470, 14.7 s): it ends on the same Orbit and molecule-diagram shot. Split it into two windows and keep it off the diagram backdrop.

Lines longer than about 6.5 s (intro_09, B1 ×2, B2_02, B3_02, B4_02, closing ×2) run past the vetted ~6 s window. The masters cut on their own inside those spans, and the sheet shows no cards or captions in them apart from the three above. Smaller notes: intro_06 (013 @60) runs into 013's moonlit-sea shot around 18 s, which is close to intro_01 and closing_02, so picture_qa may count it as a repeat. B2_02 (019 @210) shows 019's own constellation linework (no labels).

## Plates v02 and segments v02 (step 5c, Cursor, 12 Oct 22:55Z)

The three re-picks are in `COMPILATION_PLATES_v02.json`, which supersedes v01. Every window was checked at 1 fps, with frame grabs at its edges. The builder now takes `--plates`, and it can split a line across several master windows with `windows`, cutting at the VO gap before each window's `from` words. The re-picks:
- **intro_10** splits in two. "We start with the shortest clock…" runs over 019's antique clock face push-in (240.2 s; clean 240–247.9). "…and end with the longest: the last starlight…" runs over 005's nebula, where a star flares and goes dark (172.2 s; clean 172–179.9, no Orbit).
- **bridge2_01** uses the plan's fallback, 013 @420 (the full Moon over the sea; its second and last use).
- **closing_01** splits three ways. "So that's the countdown. The Moon…" runs over 013 @60 (laser ranging on the Moon; its second and last use). "The rings…" runs over 005's ringed gas giant (275.2 s; clean 275.2–283.0). "Galaxies merging… the last starlight…" runs over 005's burning world shrinking to an ember (290.9 s; clean 290.8–299). The v01 window (005 @470) ran onto Orbit with constellation linework and sat within 20 s of 005's 488.05 out point. 005 @275 alone was 0.3 s short of the line.

All six segments rendered to `/private/tmp/owb_comp/segments_v02/` (tmux `J0167-seg2`, exit 0, `~/_desk/logs/J0167-seg2.log`). Bridges 1, 3 and 4 are unchanged from v01. Check sheets (1 fps) are `check_intro10.jpg`, `check_bridge2.jpg` and `check_closing01.jpg` in the same folder.
- **intro_10a/b: OK.** The clock push-in runs to the cut, then the nebula star flares and goes dark. No Orbit, no diagram.
- **bridge2_01: OK.** The full Moon over the sea, then 013's own huge Moon over the waves.
- **closing_01b/c: OK.** The ringed gas giant, then the burning world shrinks to an ember.
- **closing_01a: re-pick needed.** 013 @60 turns into a green laser burst at about 1 s, then a green Earth–Moon beam graphic at 2–3 s (a diagram FAIL risk), then the moonlit sea at about 4 s. **intro_06 uses the same window (013 @60, 5.6 s), so it carries the same risk and needs the same check.** Next run: find a clean 013 Moon window that isn't already used twice. 013's "Last Perfect Eclipse" shots (the Moon over the Sun) fit "The Moon, a few centimetres a year". Use it for closing_01a and, if intro_06 shows the beam graphic, for intro_06 too. Re-render with `--only intro,closing`, then go to step 6 once J0207 and the bed ruling land.

**Still open:** J0207 graphics (not started), and Chief's bed ruling (#99 6132695926, no reply yet).

## Plates v03 and segments v03 (step 5d, Cursor, 12 Oct 23:40Z)

`COMPILATION_PLATES_v03.json` supersedes v02. It moves the two lines that sat on 013 @60 (the green Earth–Moon beam graphic) onto 013's "Last Perfect Eclipse" chapter, which no other plate uses:
- **intro_06** ("The Moon drifts away from us by about three point eight centimetres every year.") now runs over **013 @383.0**: the Sun beside a cratered Moon above the clouds (clean 382.5–390, including the film's own push-in cut at about 386.5).
- **closing_01a** ("So that's the countdown. The Moon…") now runs over **013 @391.0**: a total solar eclipse over a dusk horizon (clean 390.5–397.9).

013's windows now stand at 420 ×2, 300 ×2, 383.0 ×1, 391.0 ×1 and 505 ×1, so none is used more than twice. 013 @60 is no longer used.

**Timing note:** the v01/v02 1 fps sheets ran about 1.5–2 s early around 013 @380, so the first v03 render (at 381.5 and 388.3) opened on 013's title card and the Sun-and-Moon shot. The v03 times come from a 2 fps sheet made with the builder's own input seek (`/private/tmp/owb_comp/sheets/m013_380_2fps.jpg`). Anyone re-picking a window should check it the same way.

The intro and closing were re-rendered to `/private/tmp/owb_comp/segments_v03/` (tmux `J0167-seg3`, exit 0, `~/_desk/logs/J0167-seg3.log`). Bridges 1–4 were copied unchanged from v02, so v03 is the full set. On the 2 fps check sheets (`check_intro06.jpg`, `check_closing01a.jpg`), intro_06 is the Sun and Moon from the first frame after the xfade, with no title card and no beam, and closing_01a is the eclipse from start to cut. **Step 5 is done.** Lengths are unchanged: intro 54.1 s, closing 23.3 s.

**Step 6 (full assembly) waits on two things:** J0207 (chapter cards and the countdown timeline; chart job, still open) and Chief's bed ruling (#99 6132695926).

## Bed v01 (step 5e, Cursor, 13 Oct 00:15Z)

Built under Chief's bed ruling (#99 6134719677, rule a): music-only stretches from the films' own trimmed outros, laid under the new material only. No spend, nothing generated. Builder: `_build_compilation_bed_v01.py`. Plan: `05_Music/compilation_bed_plan.json` (every source file, time range and the segment it sits under). Media: `/private/tmp/owb_comp/bed_v01/` on the Mini.

- **Stretches.** A is 013's moonlit-sea outro, 499.2–514.5 s (15.3 s). B is 019's galaxy outro, 610.4–617.8 s (7.4 s). Both windows open after the film's last word and close before the master's own fade-out. **Clean check:** local Whisper medium.en on each lifted stretch heard only the tail of the last word ("perspective.", "forever."), which ends before each window opens. The voice band (300–3400 Hz) stays a steady 6–9 dB under the full band through both windows, with no speech pattern.
- **Laying.** A and B alternate, with 2 s triangular crossfades at every join (loop points included). Each segment opens on a different stretch or offset. There's a 0.4 s fade-in, a 0.6 s fade-out (2.6 s on the closing), and a sidechain duck under the segment's VO stem.
- **Checks, all six segments:** `sfx_kit.py level` bed and speech lines PASS. While the VO speaks the bed sits a median 18–23 LU under it (the 10 LU floor holds for every 0.3 s run). Each bed is exactly its segment's length. The longest stretch more than 15 dB under the bed's median (music_gate's 3 s rolling gap test) is 0 s.
- `sfx_kit.py level` still FAILs "present" on the bridges and the closing, because their SFX stems are empty until the J0207 cards and timeline bring their ticks at step 6. The intro passes in full (2 hits).
- **By ear:** Cursor can't listen. VO + bed + SFX preview mixes at −14 LUFS are at `/private/tmp/owb_comp/bed_v01/<segment>_preview.wav` for Chief or Claude to hear before step 6.

**Step 6 now waits only on J0207** (chapter cards and the countdown timeline).

## Film bodies (step 6a, Cursor, 13 Oct 01:05Z)

J0207 (cards and timeline) is still open with no claim: Codex is up, but the relay wakes no worker while Grok is Chief, so the chart job hasn't been dispatched. To keep step 6 moving, the part that doesn't need graphics is rendering now. `_render_film_bodies_v01.py` cuts each master from 0 to its `out` in `COMPILATION_TRIMS_v01.json` (021's subscribe-beat cut stays `apply: false`), scales it lanczos to 1920×1080 at 30 fps and writes `body_<film>.mp4` (h264 crf 17), a `body_<film>.wav` film-audio stem (48 kHz, level untouched) and `bodies.json` (duration, planned length, integrated LUFS and true peak per body) to `/private/tmp/owb_comp/bodies_v01/`. It runs detached: tmux `J0167-bodies`, log `~/_desk/logs/J0167-bodies.log`, done file `~/_desk/logs/J0167-bodies.done`. Loudness is only measured here; step 6b normalises the whole cut to about −14 LUFS.

**First result (01:10Z):** body_021 is good (540.2 s, −14.7 LUFS, −1.2 dBTP). body_013 came out short: picture and mp4 audio stop at 240 s of 500.8, while its wav runs the full length. The master is clean, and a test render across 240 s is fine, so it looks like a NAS read glitch. The renderer now fails any body more than 0.5 s off plan (beabe2e8). A chained tmux job, `J0167-bodyfix` (log `~/_desk/logs/J0167-bodyfix.log`, done file `~/_desk/logs/J0167-bodyfix.done`), waits for `J0167-bodies.done`, then re-renders every short body from a local copy of its master. bodies_v01 is good when both done files read 0 and the bodyfix log ends `all bodies verified`.

**body_013 fixed (Cursor, 13 Oct 02:05Z).** The bodyfix re-render from a local copy stopped at 240 s again (`J0167-bodyfix.done` = 1), so it was never the NAS. The 013 master's frames change `color_range` from unknown to tv at 239.94 s. ffmpeg rebuilds the filter graph on that change, which restarts `trim`/`setpts` (and the audio timestamps), and the mp4 ends there. The renderer now passes `-reinit_filter 0`. body_013 re-rendered (tmux `J0167-body013`, exit 0): 500.8 s of picture and audio, −17.5 LUFS, −1.3 dBTP, frame-matched to the master at 4:05. The other four masters keep one colour range throughout, so their bodies stand. **bodies_v01 is complete: 021 540.2 s, 013 500.8, 019 612.8, 007 569.4, 005 488.05.** Anyone cutting 013 with a filter graph again needs the same flag.

**Step 6b** (the final join: segments v03 + bed v01 + cards and timeline + bodies, 0.5–1.5 s crossfades at film ends, chapter list) waits only on J0207.

**J0207 dispatched (Cursor, 13 Oct 02:15Z).** J0207 had sat open for about 6 h. Cursor rerouted it to Codex on `gpt-6-astra` (its primary) and started Codex on it detached: tmux `J0207-codex`, log `~/_desk/logs/J0207-codex.log`, done file `~/_desk/logs/J0207-codex.done`, prompt `~/_desk/logs/J0207-codex-prompt.md`. Codex claimed it at 02:14Z. Step 6b starts once J0207 is done and `graphics_v01/` holds the five cards, the three timelines and `ticks.json`.

## Final join (step 6b, Cursor, 13 Oct 03:25Z)

J0207 landed (Codex, `a44b2e24`/`a08c0cd0`): five chapter cards over their films' own blurred plates and three alpha countdown timelines, with tick cues in `ticks.json`. The sheet checks out: labels sit in a band clear of the subject, over real moving plates, never a black slab.

`_assemble_compilation_v01.py` builds the whole film. It's running detached: tmux `J0167-final`, log `~/_desk/logs/J0167-final.log`, done file `~/_desk/logs/J0167-final.done`, output `/private/tmp/owb_comp/final_v01/owb_compilation_v01.mp4`. **Never start a second copy.**
- **Order:** intro, card 1, 021, bridge 1, card 2, 013, bridge 2, card 3, 019, bridge 3, card 4, 007, bridge 4, card 5, 005, closing. **Length 47:37.**
- **Picture:** the timelines are laid over bridge 1, bridge 3 and the closing at VO zero (+0.6 s). Each piece is cut to its middle frames and each join is its own xfade clip, all with the same x264 settings, then joined with the concat demuxer (a 16-input xfade graph would buffer whole films in RAM on a 16 GB Mini). Joins are 0.4 s at the cards, 1.2 s from 013, 019 and 007 into their bridges, and 0.5 s from 021 and 005, which keep only 0.2–0.3 s after their last word, so the next VO never lands on it.
- **Audio:** built in numpy, one stem at a time, overlap-added with linear crossfades matching each picture join. Segments are VO + bed v01 + SFX, with a house tick at each timeline marker (bridge 1 at 3.66 s, bridge 3 at 1.58 s, closing at 12.44 s). Each card has a 3 s bed piece from the 013/019 outro stretches plus the low rumble at −20 dB, at about −24 LUFS. Every film keeps its own audio. Each piece is set to −14 LUFS integrated (019 needed +10.5 dB, 007 +6.9 dB), and the master goes through a −1.5 dBFS limiter. The VO, SFX, bed and film stems are written beside the master for the gates.
- **Chapters for the description** (`final_v01/chapters.txt`):
  - 0:00 Nothing in the sky is permanent
  - 0:53 The Rings Are Leaving
  - 10:12 The Moon Lets Go
  - 18:47 Two Galaxies Meet
  - 29:19 What Dead Stars Leave
  - 39:04 The Last Light
- `final_v01/cuts.json` is the whole-film cut list: segment plate rows, cards and timelines as code graphics, and each film body as one row.

**Next run (step 7):** once `J0167-final.done` reads 0, check the log ends `done …`, look at a contact sheet across every join, then run the gates: `picture_qa.py` (the film bodies are one row each, so reuse of a film window in the intro may WARN or FAIL as "footage back on a stretch"; that's the plan's by-design reuse, at most twice per window, for Chief to rule), `polish_gate`, `music_gate` (bed checks waived by Chief's rule (a); gap and length enforced), and `sfx_kit.py level` on each segment. Bridges 2 and 4 carry no SFX, by design, so "present" fails there. Then step 8: park for Chief at J0168.

**End screen:** there's no end card yet. The closing holds about 2.6 s and fades, and YouTube's end-screen elements are set in Studio at J0168 (last 5–20 s, over the closing's hold). If Chief wants a longer hold for the end screen, the closing's tail can be lengthened without re-rendering the films.

## Next steps (4–8)

4. Code graphics: five chapter cards and the countdown timeline (Bridge 1, Bridge 3, Closing), each its own render. Queued as **J0207** (`chart`, Codex `gpt-6-astra` first), rendering to `/private/tmp/owb_comp/graphics_v01/`. Step 5 can start on the intro, bridge and closing plates while it runs.
5. Intro, bridges and closing picture from the five films' own shots, with Bridge 1 v02 VO, the 005 Last Star bed under the new material and house SFX ticks and rumble.
6. Assemble at 1080p (lanczos on 019, 007 and 005), ~−14 LUFS, with the chapter list for the description.
7. Gates: `music_gate`, `sfx_kit.py level`, `picture_qa`, `polish_gate`.
8. Park for Chief (J0168).
