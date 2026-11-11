# SLEEP_VIDEO_01 — NAS Input Readability Audit & Thumbnail Gate (`J2452`)

- **Job:** `J2452` (`Sleep video test: build the ~2-hour compilation from the plan, gates, then Ben's watch`)
- **Agents:** `macbook` (`2026-11-10T23:36Z`, PR `#778`) + `macbook-2` (`2026-11-11T00:02Z` deep archive & `_desk` verification + Thumbnail Option A build)
- **Plan Audited:** `05_Analytics/owb/SLEEP_VIDEO_01_PLAN.md` (`J2451`, primary 15-film running order)
- **Status:** Waiting on `J2548` (`after: J2548`, Mini → NAS sync of `/Volumes/MiniWork/scratch/j2452/` word timings + any remaining Mini-local VO stems/plates), plus Chief note on `005`/`006` discrete narration stems below.

---

## 1. Deep Follow-Up Findings (`macbook-2`, `2026-11-11T00:02Z`)

Slot 1 (`#778`) checked `/Volumes/data/studio-live/` and `/Volumes/data/mac-mini-archive/YouTube/`, flagging 5 VO stems (`023`–`027`), 2 beds (`023`, `026`), and 7 cover-plate sets as Mini-only. Checking the dated NAS archive trees (`2026-10-24/` and `2026-11-05/`, indexed in `/Volumes/data/mac-mini-archive/MOVES_2026-10-24.log`) and MacBook `/Users/ben/_desk/` resolved nearly all of those on NAS/MacBook already — **important because the 24 Oct disk-relief job moved (`MOVE`) many `023`–`026` files off the Mini SSD into `.tar` archives on NAS**:

### A. Newly Resolved on NAS / MacBook (Fallback Ready Even If Absent on Mini SSD in `J2548`)

1. **All 5 `023`–`027` Clean Discrete Narration Stems (`13` of `13` clean-stem films now located on NAS):**
   - `023` Venus: inside `/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/owb023.tar` -> `02_Video-Projects/023_What-Happened-To-Venus/02_Voiceover/venus_vo_v01.wav` (`.mp3`, `words.json` also tracked in git `02_Video-Projects/023_What-Happened-To-Venus/02_Voiceover/words.json`).
   - `024` Light Speed: inside `/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/owb024.tar` -> `02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/02_Voiceover/light_speed_vo_v01.wav` (`.mp3`, `words.json` in git).
   - `025` Mars: inside `/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/owb025.tar` -> `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/02_Voiceover/mars_robot_vo_v01.wav` (`.mp3`, `words.json` in git).
   - `026` Nearest Star: inside `/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/owb026.tar` -> `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/02_Voiceover/nearest_star_vo_v01.wav` (`.mp3`, `words.json` in git).
   - `027` Earth Spin: unpacked master-laid VO stem at `/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-15/earth027_v_before_last/earth027_score_v01i/stem_vo_v01i.wav`, plus raw VO inside `/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/owbextra.tar` -> `02_Video-Projects/027_What-If-Earth-Stopped-Spinning/02_Voiceover/earth_spin_vo_v02order.wav` (`words_v02order.json` in git).

2. **Both "Missing" House Drone Music Beds (`4` of `4` plan beds unpacked on NAS):**
   - `026` Primary Drone Loop: `/Volumes/data/mac-mini-archive/2026-11-05/YouTube/orbit-with-ben/02_Video-Projects/026_How-Far-Is-The-Nearest-Star/05_Music/nearest-star_score_bed_v01_full.wav` (and `.mp3`).
   - `023` Supplemental Drone: `/Volumes/data/mac-mini-archive/2026-11-05/YouTube/orbit-with-ben/02_Video-Projects/023_What-Happened-To-Venus/05_Music/venus_score_bed_v01_full.mp3` (and `.wav`).

3. **6 of 7 Cover-Plate Sets Resolved (`<= 1.69×` upscale on `1920×1080`):**
   - Ch. 01 (`013` Moon, Beat 1): `/Users/ben/_desk/j2374/plates/GSFC_20171208_Archive_e000868.jpg` (`3240×3240`, `0.59×` upscale) + `/Users/ben/_desk/J2141-bodies-source-macbook-v01/as17-148-22727.jpg` (`1881×1881`).
   - Ch. 03 (`027` Earth Spin, Row 21): unpacked on NAS at `/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/pool_v01/iss/Five_Minutes_in_Orbit.webm`.
   - Ch. 04 (`025` Mars, Rows 13–14 & 25): inside `/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/owb025.tar` -> `.../nasa_pool_v01/mer/PIA19400.jpg` (`PIA19803` still check on Mini in `J2548`, or clean Curiosity frame from `025` non-Orbit row).
   - Ch. 07 (`020` Jupiter, 4 `[ORBIT ACTS]` windows): `/Users/ben/_desk/j2374/plates/PIA22069.jpg` (`4800×2700`, `0.40×` upscale), `/Users/ben/_desk/j2449/plates/PIA04921.jpg` (`6200×6200`, `0.31×` upscale), and `/Users/ben/_desk/j2449/plates/PIA21775.jpg` (`1620×1440`, `1.19×` upscale).
   - Ch. 12 (`026` Nearest Star, Rows 11 & 24): inside `/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/owb026.tar` -> `.../pool_v01/eso1629a.tif` + `/Users/ben/_desk/j2449/plates/eso0932a.jpg` (`1280×640`, `1.69×` upscale).
   - Ch. 13 (`019` Andromeda, 4 Omni cuts): `/Users/ben/_desk/j2449/plates/heic1914a.jpg` (`1280×1280`, `1.50×` upscale), `/Users/ben/_desk/j2449/plates/eso2208a.jpg` (`1280×1280`, `1.50×` upscale), and `/Users/ben/_desk/j2449/plates/heic1502a.jpg` (`1280×409`).

---

## 2. Critical Note for `J2548` & Chief Ruling Check: `005` & `006` Discrete Narration Stems vs `110–130 min` Floor

1. **Master-Aligned Word Timings (`/Volumes/MiniWork/scratch/j2452/`):**
   - `faster-whisper` is **not installed** on the MacBook (`J2141-venv` has `PIL` and `numpy` only). Syncing `/Volumes/MiniWork/scratch/j2452/` in `J2548` is essential for exact subscribe/end-CTA cut alignment on the multi-part early masters (`013`, `019`, `020`).

2. **`005` (*Last Star*) and `006` (*Europa*) Discrete Narration Stems (`#6782089969` Strict Narration Rule):**
   - `SLEEP_VIDEO_01_PLAN.md` §3.1 proposed extracting `005` and `006` audio from `last_star_STUDIO_OWNER.mp4` and `europa_v02_STUDIO_OWNER.mp4` via mono-sum + `afftdn`.
   - However, Acting Chief's `23:25Z` correction (`#6782089969`) ruled:
     > *"Narration: use each film's real locked voice files (the film's own build script names them), lined up to the master with the word timings. If a film's narration cannot be separated from its music and effects, leave that film out and say so; do not put a film in with its stings and effects."*
   - On NAS (`mac-mini-archive` + `MOVES_2026-10-24.log` + `studio-live`) and `OWB UAT`, **`005` and `006` have NO discrete VO `.wav`/`.mp3` stems** — only muxed `STUDIO_OWNER.mp4` with baked stereo music and SFX (mono-sum + `afftdn` does not strip music/SFX). Fillers `003` (*Alien Worlds*) and `004` (*JWST*) (and `001`/`002`) also have **no** masters or VO stems on NAS.
   - **Impact if `J2548` confirms `005`/`006` discrete stems and `003`/`004` are also absent on Mini SSD:**
     - The **13 clean-stem films** (`013, 021, 027, 025, 023, 031, 020, 022, 028, 029, 024, 026, 019` — calm Moon first, calm Andromeda dusk last) sum to **`6,399.7 s` (`106 min 40 s`)** kept slices = **`107 min 40 s` (`107.7 min`)** total with twelve `3.5 s` breaths + `20 s` dark fade (`2.3 min` under the `110–130 min` floor).
     - **Options for Chief when `J2548` reports back:**
       - **(Option 1 — Zero-compromise clean stems, ready immediately):** Approve the 13-film `107.7 min` clean-stem cut (`~1h 48m`, still ~2 hours and 100% pure discrete Ben VO over the single `-39 LUFS` house drone with zero baked stings/SFX).
       - **(Option 2 — 14 clean-stem films = `116.5 min`):** Include `032` (*What Would Happen If You Landed on Titan?*, `545 s` master + clean VO + `PIA17172` plates already on `studio-live`) once `032` is scheduled for its Nov 25 slot (well before the Dec 12 sleep-video air floor).

3. **Detached Encode Constraint on MacBook:**
   - `tmux` is not installed on the MacBook and `macbook_worker.py` caps each worker turn at `25 min` (`start_new_session=True` process-group kill on timeout) with worker prompt rule *"leave nothing running when you stop"*.
   - To complete cleanly within `25 min` turns on MacBook once `J2548` finishes, the build script should render **idempotent per-chapter `.mp4` + `.wav` segments with `sha256` checkpoints** in `/Users/ben/_desk/scratch/J2452/chapters/` (`h264_videotoolbox` hardware encode on Apple Silicon processes `108 min` of `1080p` in `~6–9 minutes`, well inside a single `25 min` turn!).

---

## 3. Deliverable Already Built & Staged on NAS: Thumbnail Option A (`PASS`)

Built from verified Cassini `PIA17172.jpg` (`9000×3500`, *The Day the Earth Smiled*) per `SLEEP_VIDEO_01_PLAN.md` §10 Option A and `THUMBNAIL_AND_TITLE_RULES.md` §2.B (`FALL ASLEEP` in `#F5D376` / `IN SPACE` in `#FFFFFF` in top band, whole backlit Saturn + rings uncovered below):

- **NAS Thumbnail Path:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01/08_Thumbnail/sleep_video_01_thumb_option_A_v01.jpg`
  - Size: `127,479 bytes` (`1280×720` JPEG)
  - SHA-256: `f7e41f1d30cee60b51dbf0d5ff716d356d21fe5cb4e100d17e2b04ebd89192cd`
- **NAS Phone Preview Sheet (`168×94` & `360×202`):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01/08_Thumbnail/sleep_video_01_thumb_preview_sheet_v01.jpg`
  - SHA-256: `2026c647de4cb5dd65be1107d15de81a6f07f0eef954dfce04b25d95ec1bd89d`
- **Pasted `thumb_preview.py --score` Gate Output:**
  ```text
  /Users/ben/_desk/scratch/J2452/sleep_video_01_thumb_preview_sheet_v01.jpg
  PASS  sleep_video_01_thumb_option_A_v01.jpg  saturation=168.6  near_black=3%
  ```

---

## 4. Complete Verified Readable NAS Paths Table (`read=True`)

### Source Masters (`14` muxed + `021` `v03f` split + `024` `v05d`)
| Ch. | Film | Verified Readable NAS Path | Size |
|---:|---|---|---:|
| 01 | `013` Moon | `/Volumes/data/mac-mini-archive/Desktop/MOON_LEAVING_FULL_v04_WATCH_THIS.mp4` | `469.4 MB` |
| 02 | `021` Saturn (`v03f` split) | `/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-21/OWB-021/work_first_cut_v03f/picture_all.mp4` + `vo_timeline.wav` | — |
| 03 | `027` Earth Spin | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/027_EarthSpin_rough_v01m.mp4` | `529.3 MB` |
| 04 | `025` Mars | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/09_Final-Export/025_MarsRobot_full_rough_v03f.mp4` | `310.1 MB` |
| 05 | `023` Venus | `/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-13/loose_renders/023_Venus_full_rough_v05e.mp4` | `327.9 MB` |
| 06 | `031` Mag Field | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/09_Final-Export/031_what_happens_when_earths_magnetic_field_flips_master_v02.mp4` | `635.2 MB` |
| 07 | `020` Jupiter | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/020_What-Would-You-See-If-You-Fell-Into-Jupiter/09_Final-Export/jupiter_film_v05.mp4` | `647.2 MB` |
| 08 | `022` Sun | `/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-21/OWB-022/sun_first_cut_v05.mp4` | `388.9 MB` |
| 09 | `028` Gliese 710 | `/Volumes/data/mac-mini-archive/youtube-staging/028/028_Gliese710_full_master_v03.mp4` | `484.9 MB` |
| 10 | `029` Betelgeuse | `/Volumes/data/mac-mini-archive/youtube-staging/029/029_Betelgeuse_full_rough_v03b.mp4` | `408.0 MB` |
| 11 | `024` Light Speed (`v06`) | `/Volumes/data/mac-mini-archive/youtube-staging/024/024_LightSpeed_v06.mp4` | `279.6 MB` |
| 11b | `024` Pre-Omni (`v05d`) | `/Volumes/data/mac-mini-archive/youtube-staging/024/024_LightSpeed_v05d.mp4` | `225.9 MB` |
| 12 | `026` Nearest Star | `/Volumes/data/mac-mini-archive/youtube-staging/026/026_NearestStar_v06_cfr18.mp4` | `489.1 MB` |
| 13 | `019` Andromeda | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/019_Andromeda-Milky-Way-Collision/07_Edit-Project/rough/andromeda_collision_rough_v06.mp4` | `392.0 MB` |
| 14 | `005` Last Star *(muxed audio only on NAS)* | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/09_Final-Export/last_star_STUDIO_OWNER.mp4` | `118.1 MB` |
| 15 | `006` Europa *(muxed audio only on NAS)* | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/09_Final-Export/europa_v02_STUDIO_OWNER.mp4` | `93.3 MB` |

### Clean Discrete VO Stems Readable on NAS (`13` of `13` clean-stem films)
- `013`: `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/013_Why-The-Moon-Is-Slowly-Leaving-Us/02_Voiceover/parts/moon_leaving_part-01_vo_v01.wav` (`part-01`..`part-04`)
- `021`: `/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-21/OWB-021/work_first_cut_v03f/vo_timeline.wav`
- `027`: `/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-15/earth027_v_before_last/earth027_score_v01i/stem_vo_v01i.wav` (plus `owbextra.tar` -> `earth_spin_vo_v02order.wav`)
- `025`: `/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/owb025.tar` -> `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/02_Voiceover/mars_robot_vo_v01.wav`
- `023`: `/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/owb023.tar` -> `02_Video-Projects/023_What-Happened-To-Venus/02_Voiceover/venus_vo_v01.wav`
- `031`: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/full_master_v02_work/vo_laid_v02.wav` (and `02_Voiceover/magnetic_field_flip_vo_v02a.wav`)
- `020`: `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/020_What-Would-You-See-If-You-Fell-Into-Jupiter/02_Voiceover/jupiter_vo_v01.mp3`
- `022`: `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/022_Is-the-Sun-Getting-Brighter/02_Voiceover/parts/sun_brighter_vo_v01.wav`
- `028`: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/02_Voiceover/star_coming_vo_v01.wav` (plus `J1100_s5_open_pickup_v01.wav`)
- `029`: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/02_Voiceover/betelgeuse_vo_v01.wav`
- `024`: `/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/owb024.tar` -> `02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/02_Voiceover/light_speed_vo_v01.wav`
- `026`: `/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/owb026.tar` -> `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/02_Voiceover/nearest_star_vo_v01.wav`
- `019`: `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/019_Andromeda-Milky-Way-Collision/02_Voiceover/parts/andromeda_collision_vo_v03_full.wav`

### House Drone Music Beds Readable on NAS (`4` of `4` + `2` extras)
- `026` Primary Loop: `/Volumes/data/mac-mini-archive/2026-11-05/YouTube/orbit-with-ben/02_Video-Projects/026_How-Far-Is-The-Nearest-Star/05_Music/nearest-star_score_bed_v01_full.wav`
- `031` Secondary Blend: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/05_Music/magnetic_field_flip_score_bed_v01.wav`
- `023` Supplemental: `/Volumes/data/mac-mini-archive/2026-11-05/YouTube/orbit-with-ben/02_Video-Projects/023_What-Happened-To-Venus/05_Music/venus_score_bed_v01_full.mp3`
- `013` Supplemental: `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/013_Why-The-Moon-Is-Slowly-Leaving-Us/05_Music/moon-leaving-part01_score_bed_v01.mp3`
- `028` / `029` Extras: `studio-live/.../028.../05_Music/gliese_score_bed_v03.mp3`, `studio-live/.../029.../05_Music/betelgeuse_score_bed_v01.mp3`
