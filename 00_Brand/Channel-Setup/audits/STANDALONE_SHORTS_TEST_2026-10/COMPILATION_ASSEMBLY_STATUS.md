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

## Running now

Word timings for all five masters (local `faster_whisper` medium.en, no spend), in tmux session `J0167-words`. Log: `~/_desk/logs/J0167-words.log`; exit code in `~/_desk/logs/J0167-words.done`. Output: `/private/tmp/owb_comp/words/<film>.json` and `.txt`.

## Next steps (3–8)

3. From the word timings, mark the sentence-boundary trims: the subscribe beats in 021, 013, 019 and 007 (Chief's ruling keeps the **last** one, 005's), and every film's end hand-off with its hold.
4. Code graphics: five chapter cards and the countdown timeline (Bridge 1, Bridge 3, Closing), each its own render.
5. Intro, bridges and closing picture from the five films' own shots, with Bridge 1 v02 VO, the 005 Last Star bed under the new material and house SFX ticks and rumble.
6. Assemble at 1080p (lanczos on 019, 007 and 005), ~−14 LUFS, with the chapter list for the description.
7. Gates: `music_gate`, `sfx_kit.py level`, `picture_qa`, `polish_gate`.
8. Park for Chief (J0168).
