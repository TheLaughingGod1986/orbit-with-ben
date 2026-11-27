# OWB 064 Short 2 (Venus 464°C vs Uranus −224°C) — Brief & Approved Learnings Checklist (`v01`, `J3904`)

- **Film:** `OWB:064` — *Every Planet Explained in 12 Minutes (Mercury to Neptune)* (planned long air: **Wed 16 Dec 2026 18:00 London**, unchanged)
- **Short:** Companion Short 2 of 2 — **Planet Extremes (`464°C` Venus surface vs `−224°C` Uranus atmospheric minimum)**
- **Stem:** `064_short02_venus_vs_uranus_v01`
- **Proposed Candidate / Gate-Check Slot:** **Wed 30 Dec 2026 11:30Z** (non-colliding `Mon/Wed/Fri/Sat 11:30 London` Orbit Short slot strictly after 064 long goes public on Wed 16 Dec 18:00 London; **NOT scheduled yet — MUST NOT upload or air before 064 long is public**)
- **Canonical NAS Master (`v01`):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/10_Shorts/short02_venus_vs_uranus/06_Final-Exports/064_short02_venus_vs_uranus_v01.mp4`
- **Master SHA-256 (`v01`):** `4eb7d94377a9e59b9319f7ccfd9ec96091f60dbebb034c2e9ed6d75a2c6c77ff`
- **Audio Stems, Cover & SRT SHA-256 (`v01`):**
  - VO stem: `dd9c444d6ae5a2638eeec063e6ddffacc9dbb7d4a4e8a97d0e68ce60aefaa41b`
  - Bed stem: `f4c2e424c2fba19d0847aa40fe65c93cfff5e3169282888a3ce1100bc79d750a`
  - SFX stem: `b08b5c564ebae92e43d7dcce2cf066e62f8a1285d531addd724f77409066db9f`
  - Cover JPG: `b9e390f15630ff52bef83a281d73b0d164f0573e1398b5a0e4e7f778a6c7af42`
  - Frame 0 JPG: `a484c2665c622ff09b285e245f00ce1df2a41c9679790deb72fc11195f4e3590`
  - SRT (`064_short02_venus_vs_uranus_v01_en-GB.srt`): `2197ea8ca1761cb23f5802779ec9ce659f5162815719db54d19300925e91d8d8`
- **Locked Script & Authorized VO Provenance:**
  - Locked v03 script (`064_short02_venus_vs_uranus_script_v03.md`, locked by Chief Claude in `J3917`, PR #1394 merged `3747adb`): SHA-256 `634da1601232b9b8debb1880203228c4b98c95c354ae21711797f176e0c80ca0`.
  - VO take (`064_short02_venus_vs_uranus_vo_v01.wav`, SHA-256 `78b17500d6a233beaf1c57e9163681ad3c6c3a955253eec17cac0ce1e511ecce`): recorded via `desk-lock elevenlabs -- python3 04_Audio/tools/vo_take.py` (`Ben Orbit Narrator`, `eleven_v3`, speed `1.04`) after confirming live balance `7,275` chars (`>= 600` floor), overage `false`, `TTS_PAUSE=false`. Spent **`205` chars** (`<= 600` Chief cap; £0 cash; 0 Flow/Vertex credits). Scribe `scribe_v2` verdict `PASS` (`97.14%`; exact 100% spoken words — sole token diff was `"minus 224?"` → `"-224?"`).
  - Score bed: `every_planet_score_bed_v01.mp3` (`3e47e9d6da9aca6836a00c27a1fa58e53801190ae06ed445966ed51f5c0d75c6`).
- **Resolved J3914 / J3917 Shot Provenance Requirements:**
  - **Frame 0 native moving Venus:** Located verified NASA SVS 14095 archive file `svs14095_14095_ParkerVenus_YouTube_NoText_NoMusic.mp4` (`ebb96799...`, `1920×1080`, `t=17.60–19.35 s`), glowing golden Venus limb with Parker Solar Probe flyby — full-bleed `9:16` (`1.78×` upscale), zero timestamp, zero inset box, zero Orbit.
  - **Uranus beat re-planned honestly (zero Veo CGI, zero Keck misattribution):** Replaced retired v01 Veo CGI clips R03/R06 with verified native 4K NASA Goddard SVS 20390 Shot 8 Uranus (`svs20390_Shot8_4k.mp4`, `8345caca...`, cropped strictly inside active `y=264..1896`, **`1.18×` upscale**, zero letterbox bars), followed by honest smooth still pushes on ESA/Webb JWST NIRCam `weic2332a_hires.jpg` (`b241901c...`, CC BY 4.0) and NASA/JPL Voyager 2 `PIA01488.jpg` (`9c49e13d...`).
  - **Venus observational & radar beats:** Real NASA SDO AIA 171 Å Venus transit (`AIA171VenusTransit_HD1080.mp4`, `e580945d...`, cropped `x=656..1264` removing bottom-left timestamp, `1.78×`), real NASA/JHUAPL/NRL Parker Solar Probe WISPR + Magellan 3rd flyby (`svs14095_WISPR_Magellan_3rdFlyby.mp4`, `4b3d0c25...`, left `585×1040` crop, `1.85×`), and NASA/JPL Magellan SAR `PIA00215.jpg` (`46dc965a...`, inner crop `(350,600,2550,1838)`, `1.67×`).
- **Upload / Scheduling Status:** Not uploaded, not scheduled, not added to `shorts_open_library`, not registered for Ben UAT (`jobs.py awaits`). Ready for independent audio + moving-video QA, elected-Chief (`codex`) ruling, and Ben's phone UAT watch.

## Measured Gate & Timing Summary (`064_short02_venus_vs_uranus_v01.mp4`)

| Metric | Measured Value | Target / Gate | Status |
|---|---:|---:|---|
| Format / FPS | `1080×1920`, `24/1` CFR (`441` frames) | `1080×1920`, `24/1` CFR | PASS |
| Runtime | **`18.375 s`** | `16.0–19.0 s` (Ben 19 Nov; `DUR_BAND`) | **PASS (0 warns)** |
| Full-bleed `9:16` | `0/19` (1/s), `0/37` (2/s) padded | `0%` padded | **PASS** |
| Frame 0 motion / diff | `motion=10.18`, `f0diff=2.04` | `>= 10.0`, `>= 1.50` | **PASS** |
| Cut 1 / Cut 2 / Max hold | `1.750 s` / `4.208 s` / `3.958 s` | `<= 2.8 s` / `<= 4.8 s` / `<= 4.0 s` | **PASS** |
| VO onset / Breaths | `0.060 s` (gate `0.05 s`) / `0.160 s`, `0.160 s` | `<= 0.15 s` / `< 0.25 s` | **PASS** |
| Payoff onset (`"traps heat…"`) | **`14.920 s` (`81.2%`)** | `>= 70%` & after `14.00 s` title | **PASS** |
| Loop tail (`last word -> end`) | **`0.915 s`** (zero end card/CTA) | `< 1.20 s` (`OWB-2026-11-E1`) | **PASS** |
| Split words across cuts | `0 / 7` boundaries | `0` | **PASS** |
| Speech coverage (6 segments) | `100.0%` (`82/82` active 200 ms windows) | `>= 99%` | **PASS** |
| AAC Loudness / True Peak | **`-14.00 LUFS` / `-2.00 dBTP`** | `-14.0 ± 0.5` / `<= -1.6` | **PASS** |
| SFX Level (`sfx_kit.py level`) | VO `-16.0`, SFX `-40.1` (`7` hits) | `>= 12 LU` under VO | **PASS** |
| Music Gate (`music_gate.py`) | `every_planet_score_bed_v01.mp3`, `70.6 BPM` | `68–76 BPM`, own bed | **PASS** |
| Polish Gate / Picture QA | `0/8` fail, `1` warn (`R03` smooth cyan Uranus `0.0211` vs `p5 0.0220`, visually inspected sharp on `picture_qa_review.jpg`) | `0` fail | **PASS** |
| Thumb Preview (`--score`) | Frame 0: `sat=161.8`, `nb=2%`; Cover: `sat=194.5`, `nb=2%` | `sat >= 100`, `nb <= 30%` | **PASS** |

## Approved Learnings & `OWB-2026-11-E1` Checklist

- [x] **#1 · Title:** Positive Keeper question naming both subjects: *"Why Is Venus 464°C While Uranus Drops to −224°C?"* First VO line asks it verbatim.
- [x] **#2 · First-second rule (`0.0–1.5 s`, `J2429`):** Full-bleed `9:16` moving NASA SVS 14095 golden Venus at Frame 0 (`f0diff=2.04`, `motion=10.18`, `visor=0.0004`, `0/37` padded, no Orbit), burned-in `464°C VENUS` (`#FFE000`) / `VS −224°C?` (`#FFFFFF`) at `t=0.00 s`, VO onset `0.05–0.06 s`, subject `"Venus's surface"` completed by `1.60 s`, zero meta-promise.
- [x] **#3 · Motion (`OWB-2026-11-E1`):** `Cut 1 = 1.750 s <= 2.8 s`, `Cut 2 = 4.208 s <= 4.8 s`, max hold `3.958 s <= 4.0 s`, 8 full-bleed shots, zero static crop-zoom in `4–8 s`.
- [x] **#6 · Payoff:** Runtime `18.375 s`; earliest allowed payoff `12.86 s`; actual payoff (`"traps heat in a runaway greenhouse"`) lands at **`14.920 s` (`81.2%`)**, strictly after the `9.00–14.00 s` exact long title clears.
- [x] **#7 · Seam:** Inter-sentence breaths cleanly trimmed in pure silence to `0.160 s < 0.25 s`; zero meta-promise or Orbit reaction; zero clipped consonants (`atrim` strictly before `afade`).
- [x] **#8 · 60% Stayed-to-Watch & #9 · 70% Average Viewed / Loop:** `18.375 s` inside `16.0–19.0 s`, single Teach overlay `464°C · RUNAWAY GREENHOUSE` (`14.90–17.45 s`, inside `16:9` band), matched forward pre-roll Venus loop return (`17.500–18.375 s`), `0.915 s < 1.2 s` tail, continuous score bed, zero end card or CTA.

## Perceptual QA & UAT Boundary

- This worker session demonstrated text and still-image input only, not hearing audio or perceiving moving video.
- No self-PASS, no PR merge, no YouTube upload/schedule, and no Ben UAT registration (`jobs.py awaits`) are performed here.
- Dependent independent QA (`kind: qa`) is required to review the actual audio mix and moving-video playback before elected-Chief (`codex`) ruling and Ben's phone UAT watch.
