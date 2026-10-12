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

## Next steps (4–8)

4. Code graphics: five chapter cards and the countdown timeline (Bridge 1, Bridge 3, Closing), each its own render. Queued as **J0207** (`chart`, Codex `gpt-6-astra` first), rendering to `/private/tmp/owb_comp/graphics_v01/`. Step 5 can start on the intro, bridge and closing plates while it runs.
5. Intro, bridges and closing picture from the five films' own shots, with Bridge 1 v02 VO, the 005 Last Star bed under the new material and house SFX ticks and rumble.
6. Assemble at 1080p (lanczos on 019, 007 and 005), ~−14 LUFS, with the chapter list for the description.
7. Gates: `music_gate`, `sfx_kit.py level`, `picture_qa`, `polish_gate`.
8. Park for Chief (J0168).
