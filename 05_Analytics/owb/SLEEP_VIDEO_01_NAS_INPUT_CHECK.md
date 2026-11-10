# SLEEP_VIDEO_01 — NAS Input Readability Audit (`J2452`, Chief Step 1)

- **Job:** `J2452` (`Sleep video test: build the ~2-hour compilation from the plan, gates, then Ben's watch`)
- **Agent:** `macbook`
- **Checked At:** `2026-11-10T23:36Z`
- **Plan Audited:** `05_Analytics/owb/SLEEP_VIDEO_01_PLAN.md` (`J2451`, primary 15-film running order)
- **Result:** **HOLD / RELEASE FOR MINI→NAS SYNC** per acting Chief instruction `(1)` (`#6781958900`: *"first check that every source master, narration stem and cover plate the plan names can be read from the NAS; if one cannot, list which and release the job with that list"*).

---

## 1. Summary of Missing NAS Inputs (Must Be Copied from Mini Local SSD to `/Volumes/data/studio-live/...`)

When `023`–`027` were synced to `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/`, only scripts, JSONs, and review packs were copied; the untracked `.wav`/`.mp3` clean VO stems, music beds, and `pool_v01` / `03_Footage` plates remained on the Mac mini's local SSD (`/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/...`) or in iCloud `OWB UAT` (evicted `0` local blocks on the MacBook).

### A. Missing Source Master (`1` of `15` muxed masters; unmuxed `v03f` components ARE on NAS)
1. **`021` Saturn muxed master:** `saturn_first_cut_v03f.mp4`
   - *Plan path (absent on NAS):* `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings/07_Edit-Project/saturn_film/saturn_first_cut_v03f.mp4`
   - *Note:* The unmuxed `v03f` streams **are** readable on NAS at `/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-21/OWB-021/work_first_cut_v03f/picture_all.mp4` + `vo_timeline.wav` + `mix.m4a`, and `saturn_first_cut_v03f.mp4` (`175.3 MB`) is also in `OWB UAT/saturn_first_cut_v03f/saturn_first_cut_v03f.mp4`, so copying `saturn_first_cut_v03f.mp4` to `studio-live` is optional if Chief confirms `work_first_cut_v03f/picture_all.mp4` + `vo_timeline.wav` is acceptable.

### B. Missing Clean Narration Stems (`5` of `13` discrete VO stems — Mandatory per §2 & §3.1)
1. **`023` *What Happened to Venus?*:**
   - *Missing from NAS:* `023_venus_vo_master.wav` / `venus_vo_v01.wav` (or `.mp3`)
   - *Mini local source:* `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/023_What-Happened-To-Venus/02_Voiceover/`
2. **`024` *What Happens If You Travel Near Light Speed?*:**
   - *Missing from NAS:* `024_lightspeed_vo_master.wav` / `light_speed_vo_v01.wav` (or `.mp3`)
   - *Mini local source:* `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/02_Voiceover/`
3. **`025` *Could a Robot Survive on Mars?*:**
   - *Missing from NAS:* `025_vo_master.wav` / `mars_robot_vo_v01.mp3` (`.wav`) — `studio-live/.../02_Voiceover/` contains only `.json`/`.txt` metadata.
   - *Mini local source:* `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/02_Voiceover/mars_robot_vo_v01.mp3` (and `.wav` if present)
4. **`026` *The Nearest Star Is One You Can't See*:**
   - *Missing from NAS:* `026_vo_master.wav` / `nearest_star_vo_v01.mp3` (`.wav`) — `studio-live/.../02_Voiceover/` contains only `.json`/`.txt` metadata.
   - *Mini local source:* `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/026_How-Far-Is-The-Nearest-Star/02_Voiceover/nearest_star_vo_v01.mp3` (and `.wav` if present)
5. **`027` *Earth Is Losing Its Spin*:**
   - *Missing from NAS:* `027_vo_master_v02order.wav` / `earth_spin_vo_v01.wav` — `studio-live/.../02_Voiceover/` has only the 1.0 MB `J1100_s2_open_pickup_v01.wav`, not the full narration stem.
   - *Mini local source:* `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/02_Voiceover/`

### C. Missing House Drone Music Beds (`2` of `4` beds named in §3.2)
1. **`026` Primary Drone Loop Source:**
   - *Missing from NAS:* `026_How-Far-Is-The-Nearest-Star/05_Music/bed_v01.mp3` (`nearest-star_score_bed_v01_full.mp3` per `_assemble_nearest_star_rough_v06.py`)
   - *Mini local source:* `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/026_How-Far-Is-The-Nearest-Star/05_Music/nearest-star_score_bed_v01_full.mp3`
2. **`023` Supplemental Drone Source:**
   - *Missing from NAS:* `023_What-Happened-To-Venus/05_Music/bed_v01.mp3`
   - *Mini local source:* `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/023_What-Happened-To-Venus/05_Music/`

### D. Missing Cover / Orbit-Replacement Plates (`7` film plate sets named in §2)
1. **Ch. 01 (`013` Moon, Beat 1 `~2:05–2:13`):** NASA `SVS 4404` lunar evolution / LRO limb drift (`013/03_Footage/` absent on NAS; Beat 2 `totality_silent.mp4` IS on NAS).
2. **Ch. 03 (`027` Earth Spin, Row 21):** `Five_Minutes_in_Orbit.webm` (Mini local: `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/pool_v01/`).
3. **Ch. 04 (`025` Mars, Rows 13–14 & Row 25):** `PIA19400` / `PIA03240` (Spirit winter panorama) and `PIA19803` (Curiosity MAHLI wheel) — `studio-live/.../025/.../nasa_pool_v01` subdirs are empty `0`-entry directories; files are on Mini local `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/07_Edit-Project/nasa_pool_v01/`.
4. **Ch. 07 (`020` Jupiter, 4 `[ORBIT ACTS]` windows):** `PIA21974`, `PIA22946` (Juno Perijove), `PIA02863` (Cassini Jupiter cloud motion) — `020/03_Footage/` absent on NAS.
5. **Ch. 12 (`026` Nearest Star, Rows 11 & 24):** ESO `NGC 6752` southern starfield & full-res Voyager `PIA00452` / Hubble starfield (the only `PIA00452.jpg` on NAS is `453×614`, which exceeds the `2.35×` 1080p upscale cap; full-res pool is on Mini local `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/026_How-Far-Is-The-Nearest-Star/07_Edit-Project/pool_v01/`).
6. **Ch. 13 (`019` Andromeda, 4 Omni cuts):** `heic1502a` (Hubble PHAT Andromeda mosaic) and NASA `SVS 11640` (`019/03_Footage/` absent on NAS).
7. **Ch. 15 (`006` Europa, Veo Orbit-in-frame replacements):** `PIA19048`, `PIA00502`, `PIA01211`, `PIA16826`, and NASA `SVS 14556` (`006/03_Footage/` absent on NAS; also `heic1608a` for `005` if not using `005`'s internal clean slices `172.2–179.9 s` and `275.2–283.0 s`).

---

## 2. Verified Readable NAS Paths Found (`read=True`)

Several files in `SLEEP_VIDEO_01_PLAN.md` had stale `mac-mini-archive/YouTube/...` paths because earlier disk-relief jobs moved them into `Desktop/`, `youtube-staging/`, or `mini-tmp-scratch/`. Every real NAS path below was verified readable from the MacBook (`4 KB` read check):

### Source Masters (14 muxed + `021` `v03f` split + `024` `v05d`)
| Ch. | Film | Verified Readable NAS Path | Size |
|---:|---|---|---:|
| 01 | `013` Moon | `/Volumes/data/mac-mini-archive/Desktop/MOON_LEAVING_FULL_v04_WATCH_THIS.mp4` | `469.4 MB` |
| 02 | `021` Saturn (`v03f` split) | `/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-21/OWB-021/work_first_cut_v03f/picture_all.mp4` | — |
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
| 14 | `005` Last Star | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/09_Final-Export/last_star_STUDIO_OWNER.mp4` | `118.1 MB` |
| 15 | `006` Europa | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/09_Final-Export/europa_v02_STUDIO_OWNER.mp4` | `93.3 MB` |

### Clean VO Stems Already Readable on NAS (`8` of `13` discrete; `005` & `006` extract per §3.1)
- `013`: `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/013_Why-The-Moon-Is-Slowly-Leaving-Us/02_Voiceover/parts/moon_leaving_part-01_vo_v01.wav` (`part-01`..`part-04`)
- `021`: `/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-21/OWB-021/work_first_cut_v03f/vo_timeline.wav` (also `02_Voiceover/parts/saturn_rings_vo_v03_tightened.wav`)
- `031`: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/02_Voiceover/magnetic_field_flip_vo_v02a.wav` (and `07_Edit-Project/full_master_v02_work/vo_laid_v02.wav`, `109.6 MB`)
- `020`: `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/020_What-Would-You-See-If-You-Fell-Into-Jupiter/02_Voiceover/jupiter_vo_v01.mp3` (`9.3 MB`)
- `022`: `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/022_Is-the-Sun-Getting-Brighter/02_Voiceover/parts/sun_brighter_vo_v01.wav` (`96.5 MB`)
- `028`: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/02_Voiceover/star_coming_vo_v01.wav` (`90.1 MB`, plus `J1100_s5_open_pickup_v01.wav`)
- `029`: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/02_Voiceover/betelgeuse_vo_v01.wav` (`98.9 MB`)
- `019`: `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/019_Andromeda-Milky-Way-Collision/02_Voiceover/parts/andromeda_collision_vo_v03_full.wav` (`58.3 MB`)

### House Music Beds Already Readable on NAS
- `013`: `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/013_Why-The-Moon-Is-Slowly-Leaving-Us/05_Music/moon-leaving-part01_score_bed_v01.mp3` (`1.6 MB`)
- `031`: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/05_Music/magnetic_field_flip_score_bed_v01.wav` (`100.7 MB`)
- `028` (extra house drone): `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/05_Music/gliese_score_bed_v03.mp3` (`12.0 MB`)
- `029` (extra house drone): `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/05_Music/betelgeuse_score_bed_v01.mp3` (`13.0 MB`)

### Cover Plates & Thumbnail Base Already Readable on NAS (Dimensions Verified)
- **Thumbnail Option A & `021` Act V (`PIA17172.jpg`, `9000×3500`):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/03_Reference-Material/harvest_J2089_v01/PIA17172.jpg`
- **`013` Beat 2 eclipse (`totality_silent.mp4`):** `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/013_Why-The-Moon-Is-Slowly-Leaving-Us/07_Edit-Project/sunday_moon_long/plates/totality_silent.mp4`
- **`021` Row 23 (`PIA08248`, `1920×1080`):** `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings/07_Edit-Project/saturn_film/work_first_cut_v03c/still_009_PIA08248.jpg`
- **`027` Row 14 DSCOVR EPIC (`215.1 MB`):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/svs_moving_v01/originals/svs_12312_epic_earth_timelapse.mp4`
- **`023` Row 46 (`PIA00271` `4096×4096` + `AS17-148-22727` `1881×1881`):**
  - `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA00271.jpg`
  - `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/03_Reference-Material/harvest_J2089_v01/AS17-148-22727.jpg`
- **`031` Rows R21 & R41:**
  - `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/j2141_remaining_v01/plates/plate_031_r05a_basalt_outcrop_v01.mp4`
  - `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/svs_moving_v01/originals/hdev_earth_views_orig.mp4`
- **`022` Rows 67 & 81 (`1920×1080`):**
  - `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/022_Is-the-Sun-Getting-Brighter/07_Edit-Project/sun_film/work_first_cut_v01/still_007_PIA21218.jpg`
  - `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/022_Is-the-Sun-Getting-Brighter/07_Edit-Project/sun_film/work_first_cut_v01/still_080_STS067-709-007.jpg`
- **`028` Rows r08 & r23:**
  - `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/nasa_pool_v01/028_harvest_v01/eso_lasilla_ntt.mp4`
  - `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/07_Edit-Project/harvest_v01/orion_over_paranal.mp4`
