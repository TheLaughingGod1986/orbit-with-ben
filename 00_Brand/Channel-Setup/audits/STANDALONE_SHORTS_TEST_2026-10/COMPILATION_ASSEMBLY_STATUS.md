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

## Next steps (4–8)

4. Code graphics: five chapter cards and the countdown timeline (Bridge 1, Bridge 3, Closing), each its own render. Queued as **J0207** (`chart`, Codex `gpt-6-astra` first), rendering to `/private/tmp/owb_comp/graphics_v01/`. Step 5 can start on the intro, bridge and closing plates while it runs.
5. Intro, bridges and closing picture from the five films' own shots, with Bridge 1 v02 VO, the 005 Last Star bed under the new material and house SFX ticks and rumble.
6. Assemble at 1080p (lanczos on 019, 007 and 005), ~−14 LUFS, with the chapter list for the description.
7. Gates: `music_gate`, `sfx_kit.py level`, `picture_qa`, `polish_gate`.
8. Park for Chief (J0168).
