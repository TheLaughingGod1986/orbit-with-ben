# J2548 — Sleep Video (`J2452`) Mini → NAS Input Sync & SHA-256 Verification

- **Job:** `J2548` (ref `J2452`, audit `05_Analytics/owb/SLEEP_VIDEO_01_NAS_INPUT_CHECK.md`)
- **Worker:** `gemini`
- **Destination Root:** `/Volumes/data/studio-live/orbit-with-ben/`
- **Transfer Method:** `rsync -a` (no `--delete`; zero files moved or deleted on Mini or NAS)
- **Outcome:** **38 files copied and verified byte-for-byte (`size` + `sha256`)** — including **all 5 clean narration stems** (`023`–`027`, with `earth_spin_vo_v02order.wav`), **both house drone music beds** (`026` and `023`), the **muxed `021` Saturn master** (`saturn_first_cut_v03f.mp4`), **all 13 `j2452` word-timing / manifest files**, and **located cover plates** for `019` (`heic1502a.jpg`), `025` (`PIA19400.jpg` + `.tif`), `026` (`eso1323a.jpg`, `heic0809a.jpg`, `heic1007a.jpg`, `voyager/PIA04495.jpg`), and `027` (`Five_Minutes_in_Orbit.webm`). **14 public-domain NASA/ESO cover-plate IDs were not found on this machine** (listed plainly below).

## Copied / Checked Files

| file | size | sha256 | status | notes |
|---|---:|---|---|---|
| `02_Video-Projects/023_What-Happened-To-Venus/02_Voiceover/venus_vo_v01.wav` | 97839438 | `862c2eb933a738bde3717cdf28dd1ee4f5bcfdb4da9367e291899f303377f6a0` | copied | 023 clean VO stem (WAV) |
| `02_Video-Projects/023_What-Happened-To-Venus/02_Voiceover/venus_vo_v01.mp3` | 8154284 | `fc29b28971d94ceaab49a777a0cbbcbb560519617997707235cc5699c1fba4cc` | copied | 023 clean VO stem (MP3) |
| `02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/02_Voiceover/light_speed_vo_v01.wav` | 93630798 | `f0a6049e3ea592fc2cf581e3f6bf10ff35d5aa16db12f5c2cda490b625109a87` | copied | 024 clean VO stem (WAV, from Mini OWB UAT) |
| `02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/02_Voiceover/light_speed_vo_v01.mp3` | 7803692 | `8027352ff542938d322bf2ae00518f64dc6935f7216d3896e8c0305b8b21c6a3` | copied | 024 clean VO stem (MP3, from Mini OWB UAT) |
| `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/02_Voiceover/mars_robot_vo_v01.wav` | 93461838 | `273326741863a3cc16c762b0b58e9c8e923292275604cb28b970dfe88852232b` | copied | 025 clean VO stem (WAV, from Mini OWB UAT) |
| `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/02_Voiceover/mars_robot_vo_v01.mp3` | 7789484 | `93c6d2893b35cdb06dfe5cbe3e5e2b9f01946040db4d6a7ddd10f78e6db756c4` | copied | 025 clean VO stem (MP3, from Mini OWB UAT) |
| `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/02_Voiceover/nearest_star_vo_v01.wav` | 94275918 | `d6159f085b04f38604676bc3b37de24187488379e48ed394d076bee5bcabfaf5` | copied | 026 clean VO stem (WAV, from Mini OWB UAT) |
| `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/02_Voiceover/nearest_star_vo_v01.mp3` | 7857452 | `386d17bf70e0d3be87fc39f3d1df38968c93221b2db67239e9213302a97bb9b6` | copied | 026 clean VO stem (MP3, from Mini OWB UAT) |
| `02_Video-Projects/027_What-If-Earth-Stopped-Spinning/02_Voiceover/earth_spin_vo_v02order.wav` | 127543782 | `e12c93373d9c493e2e5e2aa67fe67a25a8accffbdd91b97e320ab79c6fb58a85` | copied | 027 clean reordered VO stem (WAV, extracted from owbextra.tar) |
| `02_Video-Projects/027_What-If-Earth-Stopped-Spinning/02_Voiceover/earth_spin_vo_v01.wav` | 88393038 | `dee53f3c663e8ed8c98f869b57f14b752cd05c8507d21237f42af71aff73f721` | copied | 027 clean v01 VO stem (WAV, extracted from owbextra.tar) |
| `02_Video-Projects/027_What-If-Earth-Stopped-Spinning/02_Voiceover/earth_spin_vo_v01.mp3` | 7367084 | `e340171affc03dac5156094a9c8a37be58638c154a01ec47dbd4b2df04aeaf44` | copied | 027 clean v01 VO stem (MP3, extracted from owbextra.tar) |
| `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/05_Music/nearest-star_score_bed_v01_full.mp3` | 12492425 | `4db6d824cff97d012af29b731e9b0ce66f4af882764b4685fc4a6161e8a23d84` | copied | 026 primary drone loop bed (MP3, extracted from owbextra.tar) |
| `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/05_Music/nearest-star_score_bed_v01_full.wav` | 130835982 | `0e98ed6485a24cc3e5906fd604af6cade4f27295bc7ff522a2416455c0eb775c` | copied | 026 primary drone loop bed (lossless WAV) |
| `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/05_Music/nearest-star_score_bed_v01.mp3` | 2720541 | `767a574c164e296bcc9d70b7d56cd98e129de6c961f38e4b30bf6a28f5ae8452` | copied | 026 base bed_v01 cue (MP3, extracted from owbextra.tar) |
| `02_Video-Projects/023_What-Happened-To-Venus/05_Music/venus_score_bed_v01_full.mp3` | 12722511 | `e2f7204e8cd1dc9d337e5ad34ebc6ecc87bea7e0aa259d034bb6970ab1bc3d35` | copied | 023 supplemental drone loop bed (full MP3) |
| `02_Video-Projects/023_What-Happened-To-Venus/05_Music/venus_score_bed_v01.mp3` | 4320489 | `9d8467e3b69486a6138eb54c2a7955f7bb009d29209bc33270ea53548adb37f8` | copied | 023 base bed_v01 cue (MP3) |
| `02_Video-Projects/013_Why-The-Moon-Is-Slowly-Leaving-Us/03_Footage/SVS_4404` | — | — | not found here | NASA SVS 4404 lunar evolution / LRO limb drift never downloaded to Mini or NAS |
| `02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/pool_v01/iss/Five_Minutes_in_Orbit.webm` | 7973947 | `92c169055e72829e118584cb0d5bd67485700334d1cb4ca96d2af394c7828c48` | copied | 027 Row 21 ISS cover plate |
| `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/07_Edit-Project/nasa_pool_v01/dusk_plain/PIA19400.jpg` | 181013 | `6f1618d81b3688ae045c14e6f9ba51f0cb73cf843889727397e5f32f1fe586fb` | copied | 025 Row 13 Mars dusk/winter panorama (1344x1080 JPG, from owb025.tar) |
| `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/07_Edit-Project/nasa_pool_v01/dusk_plain/PIA19400.tif` | 4356224 | `2a666f7bbc233be8b0d40a6bd51cdc2ccea5bf5aae516d1eeba04442dd53497e` | copied | 025 Row 13 Mars dusk/winter panorama lossless TIFF (from owb025.tar) |
| `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/07_Edit-Project/nasa_pool_v01/spirit/PIA03240.jpg` | — | — | not found here | Never downloaded to Mini or NAS (025 pool used spirit/PIA07882, PIA12142, PIA12203, PIA12457) |
| `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/07_Edit-Project/nasa_pool_v01/wheel/PIA19803.jpg` | — | — | not found here | Never downloaded to Mini or NAS (025 pool used wheel/PIA15693, PIA16112, PIA17751, PIA26016) |
| `02_Video-Projects/020_What-Would-You-See-If-You-Fell-Into-Jupiter/03_Footage/PIA21974.jpg` | — | — | not found here | Never downloaded to Mini or NAS |
| `02_Video-Projects/020_What-Would-You-See-If-You-Fell-Into-Jupiter/03_Footage/PIA22946.jpg` | — | — | not found here | Never downloaded to Mini or NAS |
| `02_Video-Projects/020_What-Would-You-See-If-You-Fell-Into-Jupiter/03_Footage/PIA02863` | — | — | not found here | Never downloaded to Mini or NAS |
| `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/07_Edit-Project/pool_v01/eso1323a.jpg` | 50781850 | `295658ed87b88f965161e9bc7ec1cca41d57c819728d2678880f82959065ef0e` | copied | 026 Row 11 ESO NGC 6752 southern starfield full-res (50.8 MB, from owb026.tar) |
| `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/07_Edit-Project/pool_v01/heic0809a.jpg` | 139119415 | `10d4c8ef7b9cf7c0faf79b84ddaf74fa55aafd3bf185ffb431fea9327cbf9f5e` | copied | 026 pool_v01 Hubble starfield full-res (139.1 MB, from owb026.tar) |
| `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/07_Edit-Project/pool_v01/heic1007a.jpg` | 1646802 | `027473193a478029e26c23e053b2fae1884e03ba9d445e700bcdf6e437392c49` | copied | 026 pool_v01 Hubble starfield (from owb026.tar) |
| `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/07_Edit-Project/pool_v01/voyager/PIA04495.jpg` | 636994 | `36bc7e74ac267243137e850540b76f25ac964e4a64dd62fb6f6aaf7f53abb825` | copied | 026 Row 24 Voyager Solar System Portrait plate (from owb026.tar) |
| `02_Video-Projects/026_How-Far-Is-The-Nearest-Star/07_Edit-Project/pool_v01/PIA00452_fullres.jpg` | — | — | not found here | No full-res PIA00452 on Mini/NAS (only 453x614 exists on NAS; 026 Row 24 used PIA04495 + heic0809a above) |
| `02_Video-Projects/019_Andromeda-Milky-Way-Collision/03_Footage/heic1502a.jpg` | 3082454 | `627d5c1aa1c0942e67feed9b1f1fb6d1a266dd32d1c4d37afdfbe6c004d23317` | copied | 019 Hubble PHAT Andromeda mosaic (from Mini ~/_desk/jobs/J2448/heic1502a.jpg) |
| `02_Video-Projects/019_Andromeda-Milky-Way-Collision/03_Footage/SVS_11640` | — | — | not found here | NASA SVS 11640 Milky Way-Andromeda simulation never downloaded to Mini or NAS |
| `02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/03_Footage/PIA19048.jpg` | — | — | not found here | Never downloaded to Mini or NAS |
| `02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/03_Footage/PIA00502.jpg` | — | — | not found here | Never downloaded to Mini or NAS |
| `02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/03_Footage/PIA01211.jpg` | — | — | not found here | Never downloaded to Mini or NAS |
| `02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/03_Footage/PIA16826.jpg` | — | — | not found here | Never downloaded to Mini or NAS |
| `02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/03_Footage/SVS_14556` | — | — | not found here | Never downloaded to Mini or NAS |
| `02_Video-Projects/005_The-Last-Star-In-The-Universe/03_Footage/heic1608a.jpg` | — | — | not found here | Never downloaded to Mini or NAS (plan §2 Ch. 14 already allows internal clean slices 172.2-179.9s & 275.2-283.0s) |
| `02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings/07_Edit-Project/saturn_film/saturn_first_cut_v03f.mp4` | 175319293 | `aad314931db783a65e82bc1ddeadf87ec2a7886b815445395770686ed11f6d2f` | copied | 021 Saturn muxed master v03f |
| `02_Video-Projects/_sleep_video_01/j2452/asr_masters.py` | 1133 | `33639d33de20bce3f69393b34f0ae1e04f75c11407b963e4cd98e1390a54525d` | copied | Sleep build ASR helper script |
| `02_Video-Projects/_sleep_video_01/j2452/inputs.json` | 5222 | `f7efd0d0250c84fc6bc5a219fd2f845e41399a580e9a93c0a7b05739985bc60d` | copied | Sleep build inputs manifest |
| `02_Video-Projects/_sleep_video_01/j2452/asr/005_words.json` | 44289 | `4296128a45514e7a0337c294b537d98381486c9ca22bbcbbae79ccbceb495feb` | copied | Word timings (005) |
| `02_Video-Projects/_sleep_video_01/j2452/asr/006_words.json` | 46472 | `aded3678f7e558f02fd1ae3f9481d8c35d6d435a32e33cb6d59a789603d6f419` | copied | Word timings (006) |
| `02_Video-Projects/_sleep_video_01/j2452/asr/019_words.json` | 53147 | `21ce786f521d4ec2ed257e6db4bae4560f1f5b266ca98f91ee7a28c4f489a816` | copied | Word timings (019) |
| `02_Video-Projects/_sleep_video_01/j2452/asr/020_words.json` | 54132 | `b7e8b36b7da07b52fbb7528f6f6fc4046db12c8ac9c984c69a0ce9179cb2e914` | copied | Word timings (020) |
| `02_Video-Projects/_sleep_video_01/j2452/asr/024_words.json` | 49162 | `00a35aaad86c1222a8742d1e5873877643f9dd1fabfe4395800680507740ca37` | copied | Word timings (024) |
| `02_Video-Projects/_sleep_video_01/j2452/asr/025_words.json` | 48210 | `d0d8a056ade06a87ec3207438d832b854709750bcdb5073b2e3e3bf5e70d132b` | copied | Word timings (025) |
| `02_Video-Projects/_sleep_video_01/j2452/asr/026_words.json` | 47077 | `a994d31a137392c292ca2d4771052d795c72582d19ae984a000bff204bed94a8` | copied | Word timings (026) |
| `02_Video-Projects/_sleep_video_01/j2452/asr/027_words.json` | 45753 | `70f6ba02568d2a8b91030e10fd027dd280b532e6cf69947d2161af9a194830b2` | copied | Word timings (027) |
| `02_Video-Projects/_sleep_video_01/j2452/asr/028_words.json` | 48775 | `2cf2738908dcb0170537de14ebb008b7f39975fc45a5b90810f45d56f2ac6033` | copied | Word timings (028) |
| `02_Video-Projects/_sleep_video_01/j2452/asr/029_words.json` | 50311 | `390ac76f639956dbbd8d4d78adde2f596f4f33ce21d147203beaa3a3514a53ac` | copied | Word timings (029) |
| `02_Video-Projects/_sleep_video_01/j2452/asr/031_words.json` | 54627 | `ae637b3a1fb0c3d1a9c9eabd83538f9e738d2da8151e36b8bf976d9835f1fba2` | copied | Word timings (031) |

## What Was Not Found on This Machine

Every narration stem (`5/5`), music bed (`2/2`), `021` muxed master (`1/1`), and `j2452` timing file (`13/13`) was found (across Mini local SSD, Mini `OWB UAT`, and `/Volumes/data/mac-mini-archive/2026-10-24/.../*.tar` archives) and copied to `studio-live`. Only the following **14 public-domain NASA cover-plate IDs** named in `SLEEP_VIDEO_01_PLAN.md` / `SLEEP_VIDEO_01_NAS_INPUT_CHECK.md` were absent from both the Mac mini's disks (`YouTube/`, `/Volumes/MiniWork`, `~/_desk`, `OWB UAT`) and all `/Volumes/data/mac-mini-archive/` directories and `.tar` archives because those older/new replacement IDs had not yet been downloaded locally:

1. **Ch. 01 (`013` Moon, Beat 1):** `SVS_4404` (NASA SVS 4404 lunar evolution / LRO limb drift; Beat 2 `totality_silent.mp4` is already on NAS).
2. **Ch. 04 (`025` Mars, Rows 13–14 & Row 25):** `PIA03240.jpg` and `PIA19803.jpg` (`PIA19400.jpg` + lossless `PIA19400.tif` **were** found and copied; `025`'s original archived `owb025.tar` pool used `spirit/PIA07882.jpg`, `PIA12142.jpg`, `PIA12203.jpg`, `PIA12457.jpg` for Spirit winter and `wheel/PIA15693.jpg`, `PIA16112.jpg`, `PIA17751.jpg`, `PIA26016.jpg` for Curiosity's wheel rather than `PIA03240` / `PIA19803`).
3. **Ch. 07 (`020` Jupiter, 4 `[ORBIT ACTS]` windows):** `PIA21974.jpg`, `PIA22946.jpg` (Juno Perijove), and `PIA02863` (Cassini Jupiter cloud motion).
4. **Ch. 12 (`026` Nearest Star, Row 24):** `PIA00452_fullres.jpg` (only `453×614` `PIA00452.jpg` exists; however, `026`'s actual `pool_v01` full-res plates `eso1323a.jpg`, `heic0809a.jpg`, `heic1007a.jpg`, and `voyager/PIA04495.jpg` **were** found and copied).
5. **Ch. 13 (`019` Andromeda):** `SVS_11640` (NASA SVS 11640 Milky Way–Andromeda simulation; Hubble PHAT mosaic `heic1502a.jpg` **was** found on Mini and copied).
6. **Ch. 14 (`005` Last Star, optional):** `heic1608a.jpg` (plan §2 Ch. 14 already specifies `005`'s internal clean slices `172.2–179.9 s` and `275.2–283.0 s` as the primary choice).
7. **Ch. 15 (`006` Europa):** `PIA19048.jpg`, `PIA00502.jpg`, `PIA01211.jpg`, `PIA16826.jpg`, and `SVS_14556`.
