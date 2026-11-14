# J2550 — Short 1 of 3: Voyager 1 (`kKN8Ale42sE`, `owb_sa_s8_voyager1_v02.mp4`)

Worker evidence delivery for Short 1 of `J2550` (Voyager 1, `kKN8Ale42sE`, airs Tue 17 Nov 2026 11:30 London; watch card due Sun 15 Nov 2026 18:00 London), implementing the Chief rulings on `J2545` (11 Nov 00:58Z), `J2509` (11 Nov 02:00Z), and `J2550` (11 Nov 03:52Z & 07:14Z). **£0 spent.** Nothing uploaded, nothing modified in YouTube Studio, `UPLOADS.json`, or Buffer; `owb_sa_s8_voyager1_v01.mp4` (`b8bb56f7ef664798bbf9115fa0ac1bbdd3d13f3ccb5c5fe44dd3c40e70064b66`) is preserved untouched.

Per the acting Chief ruling on `J2550` (11 Nov 03:52Z) and `AGENTS.md` (*"Ben's final watch is the watch-and-listen check"*), **no watching or listening is claimed in this report**; all tool gates (without report-only), full `ffmpeg` decode, loudness, caption-vs-VO timings, SHA-256 hashes, verified NASA source metadata, and full 33-frame 2 fps still-sheet inspection with every piece of on-screen text read are recorded below, and Ben's watch card is armed.

---

## 1. Hashes, Safety Copies & Audio Measurements

- **Base cut (`v01`, preserved untouched):** `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/06_Final-Exports/owb_sa_s8_voyager1_v01.mp4` (`20.74 s`, SHA-256 `b8bb56f7ef664798bbf9115fa0ac1bbdd3d13f3ccb5c5fe44dd3c40e70064b66`, matching the 17 Oct disk render authorised by the `J2509` Chief ruling).
- **Delivered `v02` master:** `owb_sa_s8_voyager1_v02.mp4` (`16.40 s`, `1080×1920`, `30 fps` CFR, `492` frames, SHA-256 `5cf55cb1a543638475277220ebec1e6872e82ee12b979b08c11e528efad8a6ce`).
- **Safety copies (SHA-256 verified in `safety_copies_v02.json`):**
  - NAS UAT: `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/J2550_voyager1_v02/owb_sa_s8_voyager1_v02.mp4`
  - iCloud CloudDocs UAT: `OWB UAT/J2550_voyager1_v02/owb_sa_s8_voyager1_v02.mp4`
  - Mini exports folder: `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/06_Final-Exports/owb_sa_s8_voyager1_v02.mp4` (plus `_PHONE.mp4`, `_frames.jpg`, `_2fps.jpg`)
- **VO stem cut (`J2509` item a):**
  - Source locked stem: `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/vo_s5-s8_v01/trim/owb_sa_s8_voyager1_vo_v01_trim.wav`
  - Excised filler promise sentence `"Stay, and I'll show you how far that is."` cleanly at the inter-sentence pauses (`seg1 = 4.25 s`, `seg2 = 6.86 s`), leaving `43` spoken words (`0.08 s` to `15.13 s`, `tail_gap = 1.27 s <= 1.50 s`, `vo_v02.wav` SHA-256 `92dc9b9d70f45b136287006690a35977975bfac61d1e83095f8a2fb3f49c2e2e`).
  - Spoken text (`43` words): `"On November 18th, Voyager 1 reaches one light day from Earth. Nearly 26 billion kilometres. A message from us at the speed of light takes a whole day to get there. Nothing we've built has ever been this far, and it's still going"`
- **Full `ffmpeg` decode:** `exit 0` (`0` errors, `0` warnings).
- **Loudness (`ebur128=peak=true`):** Integrated `-14.2 LUFS`, LRA `2.7 LU`, True Peak `-1.9 dBFS`.

---

## 2. Full-Frame 9:16 Shot Schedule & Verified NASA Sources (`cuts_v02.json`, `pool_v02.json`)

| Row | Window (s) | NASA ID | Official NASA Title (verified via `images-api.nasa.gov`) | Source px | Mode / Max Upscale | Spoken Beat |
|---:|---|---|---|---:|---|---|
| 1 | `0.00–2.60` | `PIA04495` | *Artist Concept of Voyager* (JPL, from `v01`) | `3017×2494` | `cover`, `0.98×` | `"On November 18th, Voyager 1 reaches"` |
| 2 | `2.60–4.55` | `as17-148-22727` | *View of the Earth seen by the Apollo 17 crew traveling toward the moon* (JSC Blue Marble) | `4579×4579` | `cover`, `0.48×` | `"one light day from Earth."` |
| 3 | `4.55–8.15` | `PIA21741` | *Voyager: Preparing the Golden Record* (JPL, from `v01`) | `1760×2227` | `cover`, `0.97×` | `"Nearly 26 billion kilometres. A message"` (`25.9 BILLION KILOMETRES` card `4.65–7.05 s`) |
| 4 | `8.15–11.85` | `PIA23682` | *NASA's Deep Space Antenna Upgrade to Affect Voyager* (JPL DSS-43 70 m dish) | `1920×1280` | `cover`, `1.65×` | `"from us at the speed of light takes a whole day to get there."` |
| 5 | `11.85–15.51` | `PIA17464` | *Voyager 1 Launch 1977* (JPL, Sept. 5, 1977, from `v01`) | `2355×3000` | `cover`, `0.82×` | `"Nothing we've built has ever been this far, and it's still going"` |
| Loop | `15.11–16.40` | `PIA04495` | `0.40 s` crossfade into continuous pre-roll of Row 1 | `3017×2494` | `cover`, `0.98×` | Clean music-bed loop back into frame `0` |

---

## 3. Whole-Cut Still Sheet Inspection (`owb_sa_s8_voyager1_v02_2fps.jpg`, `0.0 s`–`16.0 s` + `frames.jpg` `16.3 s`)

Every sampled tile across the whole cut fills `1080×1920` edge to edge with zero blurred, mirrored, or flat padding bands and zero raw IDs or stray strings:

- **Hook (`0.0–2.2 s`):** `ONE LIGHT-DAY` / `AWAY` (`LIGHT-DAY` in yellow, rest white, top band clear of Voyager dish).
- **Fact card (`4.65–7.05 s`):** `25.9 BILLION` (yellow) / `KILOMETRES` (white), animated slide/fade inside the lower `16:9` centre band over the 1977 Golden Record photograph while `"Nearly 26 billion kilometres"` is spoken (`4.35–6.97 s`).
- **Title (`9.0–14.0 s`):** `Voyager 1 Is About to Be` / `One Light-Day Away` (clean white house type, no raw video ID).
- **Word captions (`0.08–15.58 s`, read across all 33 tiles):** `ON NOVEMBER` (`0.5 s`), `18TH` (`1.0 s`), `VOYAGER 1` (`1.5–2.0 s`), `REACHES ONE` (`2.5–3.0 s`), `LIGHT DAY` (`3.5 s`), `FROM EARTH` (`4.0 s`), `NEARLY 26` (`4.5–5.5 s`), `BILLION KILOMETRES` (`6.0–7.0 s`, British spelling), `A MESSAGE` (`7.5 s`), `FROM US` (`8.0 s`), `AT THE` (`8.5 s`), `LIGHT TAKES` (`9.0–9.5 s`), `A WHOLE` (`10.0 s`), `DAY TO` (`10.5 s`), `GET THERE` (`11.0–11.5 s`), `NOTHING WE'VE` (`12.0 s`), `BUILT HAS` (`12.5 s`), `EVER BEEN` (`13.0 s`), `THIS FAR` (`13.5 s`), `AND IT'S` (`14.0 s`), `STILL GOING` (`14.5–15.5 s`), clean tail (`16.0–16.3 s`).
- **Review of the two non-failing `gate_shorts_open.py` warnings:**
  1. `warn duration 16.4s outside 22–27s band`: `kKN8Ale42sE` is standalone test Short S8 (`J0216` ~20 s standalone cohort, `20.74 s` in `v01`), shortened by `4.34 s` solely by excising `"Stay, and I'll show you how far that is."` as ordered by the `J2509` Chief ruling (11 Nov 02:00Z).
  2. `warn the picture may not fill 9:16 on 3/33 sampled frames: 4-4s (blur-pad, no edge), 14-16s (blur-pad, no edge)`: Direct visual inspection of `owb_sa_s8_voyager1_v02_2fps.jpg` confirms **neither window is padded**:
     - At `4.0 s`, the frame is a full-bleed `9:16` crop (`0.48×`) of the spherical Apollo 17 Blue Marble Earth (`as17-148-22727`) surrounded naturally by black space at the top and bottom of the globe.
     - At `14.0–15.5 s`, the frame is a full-bleed `9:16` crop (`0.82×`) of the Sept. 5, 1977 Voyager 1 launch photograph (`PIA17464`), with dark sky above the Titan/Centaur nosecone and bright white rocket exhaust cloud at the bottom.
- **Review of `picture_qa` / `polish_gate` warnings:**
  - Row 1 (`PIA04495`, *Artist Concept of Voyager*) is the inherited opening plate from `v01` (Ben OK'd).
  - Row 5 (`PIA17464`, `13.7 s`, `edge density 0.032 < film p5 0.0352`) is the inherited 1977 launch photograph from `v01` (Ben OK'd), well above `EDGE_FLOOR` (`0.0259`).

---

## 4. All Five Shorts Gates (Run Without Report-Only)

### `gate_shorts_open.py` (`exit 0`)

```text
PASS  owb_sa_s8_voyager1_v02.mp4  dur=16.4s  audio=-16.6dB  motion=22.11  f0diff=9.71  cut1=2.6s  vo_onset=0.07s  tail_gap=1.27s  vo_src=/Volumes/MiniWork/scratch/J2550/s8_v02/stem_vo.wav  dhash=654f0d0e0e18a3c1  visor=0.0
   full-bleed 0.00s  fills the frame  sharp above/middle/below=0.005/0.318/0.08  detail top/centre/bottom=17.4/10.12/2.1  spread top/bottom=58.88/9.19
   full-bleed 0.25s  fills the frame  sharp above/middle/below=0.009/0.322/0.048  detail top/centre/bottom=17.35/10.26/6.45  spread top/bottom=58.86/30.25
   full-bleed 0.50s  fills the frame  sharp above/middle/below=0.014/0.326/0.039  detail top/centre/bottom=17.33/10.4/6.24  spread top/bottom=58.81/30.16
   full-bleed whole Short  2/17 frames padded at one a second, 3/33 at two a second  padded stretches: 4-4s (blur-pad, no edge), 14-16s (blur-pad, no edge)  no end card named in meta
   warn  duration 16.4s outside 22–27s band
   warn  the picture may not fill 9:16 on 3/33 sampled frames: 4-4s (blur-pad, no edge), 14-16s (blur-pad, no edge). They are soft above and below a detailed middle, with no straight edge found, so this is not a FAIL: look at those seconds and say which it is
   sheet /Volumes/MiniWork/scratch/orbit_shorts_gate/owb_sa_s8_voyager1_v02_open_sheet.jpg
```

### `sfx_kit.py level` (`exit 0`)

```text
SFX level PASS: VO -20.5 LUFS, SFX -37.0 LUFS, 2 hits
```

### `polish_gate.py` (`exit 0`)

```text
   1     1.3s /Volumes/MiniWork/scratch/J2 ok
   2     3.6s /Volumes/MiniWork/scratch/J2 ok
   3     6.3s /Volumes/MiniWork/scratch/J2 ok
   4    10.0s /Volumes/MiniWork/scratch/J2 ok
   5    13.7s /Volumes/MiniWork/scratch/J2 WARN low detail: edge density 0.032 < film p5 0.0352
polish gate PASS: 0 of 5 rows failed, 1 to look at -> /Volumes/MiniWork/scratch/J2550/s8_v02/polish_gate.json
```

### `music_gate.py` (`exit 0`)

```text
WARN pace: measured about 120.0 BPM against the brief's 84-96; Claude listens
music gate PASS: owb-standalone-shorts_score_bed_v01.mp3, 60.0 s, about 120.0 BPM, brief Pace: 84-96 BPM
```

### `picture_qa.py` (`exit 0`)

```text
WARN   0:01 row 1 /Volumes/MiniWork/scratch/J2550/plates/s8_voyager/PIA04495.jpg: kind of picture: 'Artist Concept of Voyager' (artist), look at it full size
WARN   0:14 row 5 /Volumes/MiniWork/scratch/J2550/plates/s8_voyager/PIA17464.jpg: low detail: edge density 0.032 < film p5 0.0352
picture QA PASS: 0 of 5 cuts fail, 2 to look at -> /Volumes/MiniWork/scratch/J2550/s8_v02/picture_qa/PICTURE_QA.md, /Volumes/MiniWork/scratch/J2550/s8_v02/picture_qa/picture_qa_review.jpg
```

---

## 5. Watch Card 1 & Remaining J2550 Scope

- **Ben's Watch Card 1 (`J2550.1`):** Armed on `J2550` (`version v02`, due `2026-11-15 18:00` London, airs `2026-11-17 11:30` London, `--if-not "the cut you OK'd airs"`).
- **Remaining `J2550` items (in air-date order):**
  - **Short 2 (`Muons`, `rvug71d7Dqk`, `OWB:024`, airs Sat 21 Nov 11:30, watch card due Thu 19 Nov 18:00):** Rebuild `fri06_muons_ground_v05.mp4` full-frame `9:16` throughout using the locked stems/overlays in `02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/10_Shorts/fri06_muons_ground/_work_v02/` and 4K ISS Earth footage in `/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/pool_v01/iss/Gerst_Earth_timelapses_2017.webm` (`upscale <= 0.89x`), then append Watch Card 2 with `jobs.py awaits J2550 ... --add`.
  - **Short 3 (`ISS`, `xdurJQcoiGM`, `OWB:030`, airs Wed 25 Nov 11:30, watch card due Mon 23 Nov 18:00):** Replace only the padded shot `14.8–18.4 s` in `owb_ar2_iss_2030_deorbit_v14.mp4` (`assemble_j1321.py` + `repair_j1468.py` audio copy) with a full-frame `9:16` ISS/Earth shot from `pool_v01`, then append Watch Card 3 with `jobs.py awaits J2550 ... --add`.
