# 033 Uranus Short 2 (`033_short02_ice_giant_surface_v01.mp4`) — Keeper Question Build & Gate Report (`J2318`)

- **Job:** `J2318` (*033 Uranus Short 2 (Keeper question): build 22-27s Ch 5/6 cut + gates (slot Sat 19 Dec 11:30 London; no upload)*)
- **Built by:** `gemini` (8 Nov 2026)
- **Parent film:** `033_Why-This-Planet-Has-21-Year-Winters` (*Why Knocked-Sideways Uranus Has 21-Year Winters*, airs **Wed 9 Dec 2026 18:00 Europe/London**)
- **Target air slot:** **Sat 19 Dec 2026 11:30 Europe/London (`2026-12-19T11:30:00Z`)** (Path A default · zero reschedule of existing `UPLOADS.json` IDs; Path B swap options: Fri 18 Dec or Sat 12 Dec 11:30 London)
- **Format:** Keeper-Score Question Short (`26.28 s` inside `22–27 s` window, `62` spoken words inside `55–65` window, one question in listing/on-screen title and spoken Line 1 (`R49`), single Teach overlay inside `16:9` centre band at `15.00–18.72 s`)
- **Spend:** **£0 / 0 credits** (reuses locked `02_Voiceover/uranus_vo_v01.wav`, `05_Music/uranus_score_bed_v01.mp3`, `06_Sound-Effects/kit_v01` house synthesis, and `J2300`/`J2299`/`J2386` verified 033 Ch 5 plates and code graphic)
- **Upload rule:** **No YouTube upload performed in `J2318`.** Handed to `kind: review` (then `jobs.py awaits` for Ben's phone watch).

---

## 1. Deliverables & SHA-256 Checksums

- **Master 9:16 Export (`25 fps` CFR, `1080×1920`, `26.28 s` / `657` frames):**
  - `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short02_ice_giant_surface_v01.mp4`
  - `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short02_ice_giant_surface/06_Final-Exports/033_short02_ice_giant_surface_v01.mp4`
  - `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/033_shorts_v01/033_short02_ice_giant_surface_v01.mp4`
  - `~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/033_shorts_v01/033_short02_ice_giant_surface_v01.mp4`
  - **SHA-256:** `c2404d5a05ada2c257bf9e5fdc2b10edaa126d36de6aa32b38cb27df6d08dbc2`
- **Frame-0 Still (`033_short02_ice_giant_surface_v01_frame0.jpg`, `1080×1920`):**
  - **SHA-256:** `8879316c316a7a7e28da4e34608df0455a70106a8401e74b03b7a1872a975228`
- **Shorts Cover (`033_short02_ice_giant_surface_v01_cover.jpg`, `1080×1920`, `LAND ON` / `URANUS?` on `PIA01977.jpg` + `stsci-h-p1906c-f-514x514.a.png`):**
  - **SHA-256:** `4ddfd7b59ca45c8aa73a2110ce741f58beb276100ebc97f96903c8a2fe85a22e`
- **Locked VO Source (`02_Voiceover/uranus_vo_v01.wav`):**
  - **SHA-256:** `3d73576e0c20be9030546db7bc71ea0107602d5e5fbdde37cba28c7d5b43f460`
- **House Music Bed (`05_Music/uranus_score_bed_v01.mp3`, `629.40 s`, `70.6 BPM`):**
  - **SHA-256:** `47f68d66c4ef7b0287c4939b14e7d906582309ca2a3354c3c262daa7e21309f0`
- **Assembler Script:**
  - `02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/_assemble_033_short2_v01.py`

---

## 2. Spec & `OWB-2026-11-E1` Compliance Summary

| Rule / Lock | Target | Actual (`033_short02_ice_giant_surface_v01.mp4`) | Status |
|---|---|---|---|
| Format & Resolution | `1080×1920` (`9:16`), `25 fps` CFR, `yuv420p` | `1080×1920`, `25/1` CFR (`657` frames), `H.264 High` | **PASS** |
| Keeper Runtime | `22.0–27.0 s` | `26.28 s` (`55–65` words -> `62` words) | **PASS** |
| Spoken Line 1 & Title Question | One question in listing/on-screen title and Line 1 (`R49`) | Title: *What Happens If a Spacecraft Tries to Land on Ice Giant Uranus?* · Line 1 (`0.08–5.48 s`): *"What happens if a spacecraft dives beneath those clouds to land on the ice below?"* | **PASS** |
| Cut 1 & Cut 2 Pacing (`OWB-2026-11-E1`) | `Cut 1 <= 2.8 s`, `Cut 2 <= 4.8 s`, max shot `<= 4.0 s` | `Cut 1 = 1.88 s`, `Cut 2 = 3.80 s`, max shot `3.92 s` (`R52` code graphic), `11` shots / `10` cuts | **PASS** |
| Word Boundary Check | `0` split words across all cuts | `0` split words across all `10` cut boundaries | **PASS** |
| VO Onset & Loop Tail | `vo_onset <= 0.25 s`, `tail_gap <= 1.15 s` (`< 1.2 s`) | `vo_onset = 0.08 s` (`gate_shorts_open`: `0.09 s`), last word `"Fahrenheit."` ends `25.244 s` on falling terminal pitch (`81.6 -> 75.7 Hz`), `tail_gap = 1.04 s` | **PASS** |
| Frame-0 Hook Caption (`0.00–2.00 s`) | `NO **SURFACE**` (yellow `SURFACE`), inside `16:9` band | `NO` (white, `y=263..375`) / `SURFACE` (yellow `#FFD400`, `y=453..565`), `132 px` | **PASS** |
| Frame-0 Open Uniqueness | `dhash` & colour clear of `shorts_open_library` (`81` Shorts) & `033` Short 1 / `ZpEA8stoSPA` | `dhash=ffc1d46040c77eb1`, `visor=0.0`, `motion=14.37`, `f0diff=3.43`, `0` library collisions (`R49`/`R51` cyan-teal cloud deck dive `PIA00142.jpg` + `stsci-h-p1906c-f-514x514.a.png` + `r55_cut1_r55b_100x_silent.mp4`) | **PASS** |
| On-Screen Title (`9.00–13.50 s`) | Inside `16:9` centre band (`y=656..1264`), over text-free plates | `What Happens If a Spacecraft` / `Tries to Land on` / `Ice Giant Uranus?` (`56 px`, `y=843..1073`), over text-free `R51b` (`r55_cut3_pia01488_pushin_silent.mp4`) & `R51c` (`stsci-h-p1906a-f_uranus_globe.png`) | **PASS** |
| Single Teach Overlay (`15.00–18.72 s`) | `≥ 80% HOT DENSE FLUID` inside `16:9` band, `11–12%` height, clear of `0–2 s` and `9–14 s` title | `≥ 80% HOT DENSE FLUID` pill (`y=1189..1249`, inside `16:9` band `656..1264`) over 9:16-reframed animated `code_graphic_033_r52_interior_mantle.mp4` on `PIA18182.jpg` | **PASS** |
| End Card (`25.28–26.28 s`) | Exact parent long listing title + `"Full film on the channel"`, loop bridge to Frame 0 | `Why Knocked-Sideways` / `Uranus Has` / `21-Year Winters` + `Full film on the channel` (`y=814..1106`) over `frame0_hold_033_short02_ice_giant_surface.png` | **PASS** |
| Audio Mix & Stems | Mix `~ -14` to `-16 LUFS`, bed full runtime, SFX `>= 12 LU` under VO | Mix `-15.1 LUFS` (AAC `-14.1 LUFS`, `-2.2 dBTP`, `-16.6 dB` mean), VO `-16.8 LUFS`, Bed `-35.0 LUFS`, SFX `-41.7 LUFS` (`24.9 LU` under VO, `6` hits) | **PASS** |

---

## 3. 11-Shot Cut List (`033_short02_ice_giant_surface_v01_cuts.json`)

| Shot | Window (s) | Dur (s) | Pool Asset(s) | Visual Action & Overlay | Spoken Words in Window |
|---|---:|---:|---|---|---|
| `R49a` | `0.00–1.88` | `1.88` | `PIA00142.jpg` + `stsci-h-p1906c-f-514x514.a.png` + `r55_cut1_r55b_100x_silent.mp4` | Native moving dive into Uranus's cyan-teal cloud deck + Frame-0 hook `NO` / `SURFACE` (`0.00–2.00 s`) | *"What happens if a spacecraft"* |
| `R49b` | `1.88–3.80` | `1.92` | `stsci-h-p1906c-f-514x514.a.png` + `PIA00142.jpg` | Hubble WFC3 north-polar cyan cloud cap push-in (`x1.65`) | *"dives beneath those clouds to"* |
| `R50` | `3.80–5.60` | `1.80` | `weic2332a_hires.jpg` + `PIA01977.jpg` | JWST NIRCam tilted cyan rings & north polar cap push (`x1.00`) | *"land on the ice below?"* |
| `R51a` | `5.60–7.80` | `2.20` | `PIA01977.jpg` | Hubble NICMOS false-colour Uranus globe push (`x1.33`) | *"As an ice giant,"* |
| `R51b` | `7.80–11.56` | `3.76` | `r55_cut3_pia01488_pushin_silent.mp4` + `PIA18182.jpg` | Voyager 2 `PIA01488` high-resolution limb cloud push-in + on-screen title card (`9.00–13.50 s`) | *"Uranus has no true surface. Beneath the hydrogen and"* |
| `R51c` | `11.56–14.84` | `3.28` | `stsci-h-p1906a-f_uranus_globe.png` + `PIA18182.jpg` | Hubble WFC3 cyan globe drift + on-screen title card (`9.00–13.50 s`) | *"helium clouds, 80% or more of the planet's"* |
| `R52` | `14.84–18.76` | `3.92` | `code_graphic_033_r52_interior_mantle.mp4` + `PIA18182.jpg` | Animated 9:16 interior cutaway on `PIA18182.jpg` + single Teach pill `≥ 80% HOT DENSE FLUID` (`15.00–18.72 s`) | *"mass is a hot, dense fluid of water,"* |
| `R53a` | `18.76–21.04` | `2.28` | `PIA01985.jpg` + `PIA01977.jpg` | Hubble STIS deep ultraviolet aerosol layer push (`x1.28`) | *"methane, and ammonia above a small rocky core."* |
| `R53b` | `21.04–23.28` | `2.24` | `r55_cut1_r55b_100x_silent.mp4` + `PIA00142.jpg` | Keck II adaptive-optics deep methane cloud bands (`x1.00`) | *"Near that core, Uranus"* |
| `R53c` | `23.28–25.28` | `2.00` | `r55_cut2_r55b_128x_vortex_silent.mp4` + `PIA00142.jpg` | Keck II deep cloud vortex push (`x1.00`) through final word `"Fahrenheit."` (`25.244 s`) | *"heats up to 9,000 degrees Fahrenheit."* |
| `R49_loop` | `25.28–26.28` | `1.00` | `frame0_hold_033_short02_ice_giant_surface.png` | Seamless cyan-teal cloud deck loop bridge + End Card (`Why Knocked-Sideways / Uranus Has / 21-Year Winters` + `Full film on the channel`) | *(music + loop tail)* |

---

## 4. Verbatim Tool Gate Outputs

### 4.1 `gate_shorts_open.py check`
```text
PASS  033_short02_ice_giant_surface_v01.mp4  dur=26.28s  audio=-16.6dB  motion=14.37  f0diff=3.43  cut1=1.88s  vo_onset=0.09s  tail_gap=1.04s  vo_src=/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short02_ice_giant_surface/06_Final-Exports/033_short02_ice_giant_surface_v01_vo.wav  dhash=ffc1d46040c77eb1  visor=0.0
```

### 4.2 `picture_qa.py`
```text
picture QA PASS: 0 of 11 cuts fail, 1 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short02_ice_giant_surface/06_Final-Exports/033_short02_ice_giant_surface_v01_picture_qa/PICTURE_QA.md
  WARN 0:20 row R53a PIA01985.jpg: low detail: edge density 0.0076 < film p5 0.0100 (at 19.9s)
```
*(Note: `PIA01985.jpg` is a real 1998 Hubble STIS ultraviolet planetary globe observation whose smooth stratospheric aerosol limb naturally has soft edges at `0.0076` edge density; inspected full size in `J2300` and on the 11-shot contact sheet — clean, sharp limb and zero banding.)*

### 4.3 `polish_gate.py`
```text
polish gate PASS: 0 of 11 rows failed, 1 to look at -> /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short02_ice_giant_surface/06_Final-Exports/033_short02_ice_giant_surface_v01_polish_gate.json
  WARN 0:20 row R53a PIA01985.jpg: low detail: edge density 0.0076 < film p5 0.0100 (at 19.9s)
```

### 4.4 `sfx_kit.py level`
```text
SFX level PASS: VO -16.8 LUFS, SFX -41.7 LUFS, 6 hits
```

### 4.5 `music_gate.py`
```text
music gate PASS: uranus_score_bed_v01.mp3, 629.4 s, about 70.6 BPM, brief Pace: 66-76 BPM
```

### 4.6 `thumb_preview.py short` (Frame 0 & Cover)
```text
PASS  033_short02_ice_giant_surface_v01_frame0.jpg  saturation=116.7  near_black=1%
Wrote /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short02_ice_giant_surface/06_Final-Exports/033_short02_ice_giant_surface_v01_frame0_preview.jpg
PASS  033_short02_ice_giant_surface_v01_cover.jpg  saturation=148.7  near_black=1%
Wrote /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/10_Shorts/033_short02_ice_giant_surface/06_Final-Exports/033_short02_ice_giant_surface_v01_cover_preview.jpg
```
