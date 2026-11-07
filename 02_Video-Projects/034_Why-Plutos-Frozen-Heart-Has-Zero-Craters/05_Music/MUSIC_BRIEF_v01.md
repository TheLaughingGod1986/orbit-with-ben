# Music Brief v01 — 034 Why Pluto's Frozen Heart Has Zero Craters (Pluto, `J2361` Repaired)

- **Episode:** `034_Why-Plutos-Frozen-Heart-Has-Zero-Craters` (`Real Worlds` series: Pluto & Charon)
- **VO Master:** `02_Voiceover/pluto_frozen_heart_vo_v03.wav` (`616.160 s`, `-19.9 LUFS` integrated, `-23.0 dB` mean, `-3.7 dBTP` true peak; SHA-256 `2be8030b6c42b673530351014c71bca1a6c31a10af9746539bb2a1ce7dcf7685`, accepted full VO PASS in `jobs/reviews/J2352/REVIEW.md`)
- **Target Music Runtime:** `634.16 s` (`10:34.16` — full `616.160 s` VO + `18.00 s` moving end-screen hold `R74`)
- **Repaired Ending Envelope (`STUDIO_PLAYBOOK.md` §7 & `docs/ORBIT_PLAYBOOK_LESSONS.md` §2):**
  - **Last spoken word ends:** `616.040 s` (*"Celsius."*)
  - **Post-word full-level hold (`2–3 s` rule):** **`2.50 s` hold** at full bed level (`616.040–618.54 s`), then steady nonzero underscore under the moving end-screen canvas (`618.54–624.16 s`).
  - **Music fade (`~10 s` rule):** **`10.00 s` smooth linear/cosine fade to silence** over **`624.16–634.16 s`**, keeping the music bed nonzero throughout the entire moving end hold.
  - **Final picture fade (`2 s` rule):** **`2.00 s` picture fade to black** over **`632.16–634.16 s`**.
- **Target Output Stem (at assembly stage):** `05_Music/pluto_score_bed_v01.mp3` + `05_Music/pluto_score_bed_v01_plan.json`
- **Generator:** `python3 04_Audio/tools/generate_music_bed.py` (API only; **not run in `J2353`/`J2361`**, £0 / 0 credits spent in this shot-list job)
- **Gate:** `python3 scripts/music_gate.py 02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters --bed 05_Music/pluto_score_bed_v01.mp3 --video <cut.mp4>`

---

## 1. Exact API Prompt (`Pace:` and `NOT:` Mandatory Lines Verified Against Actual `003`–`033` Briefs)

```text
Sub-zero Kuiper Belt space-documentary score for Pluto, Charon, and Sputnik Planitia, alternating between vast twilight horizon wonder ("awe": warm bowed glass marimba, high crystalline celesta harmonics, solo muted French horn, and deep velvety contrabass pad) and clean, curious astronomical discovery ("explain": delicate plucked concert harp, soft pizzicato violas, and warm analog Rhodes pulse). Gentle harmonic lift at the Chapter 4 midpoint twist ("Wrong." at 368.52 s) as Sputnik Planitia's convecting nitrogen heart awakens, holding full past the final word at 616.04 s for 2.5 s before a smooth 10.0 s fade over 624.16-634.16 s.
Pace: 64-74 BPM, calm measured pulse matched to British narration, lifting gently at chapter transitions without heavy percussion.
NOT: Do not sound like 013 Moon Leaving quiet lunar pads, 020 Jupiter gas-giant swell, 021 Saturn Rings golden ring-plane pads, 022 Sun Brighter warm solar drone, 023/024/025 shared ambient track (023 Venus lost-twin underscore, 024 Light Speed forward relativistic pulse, 025 Mars Robot cold dusty red plains), 026 Nearest Star deep-space night-sky pad, 027 Earth Stopped Spinning rotational pulse, 028 Star Coming Toward Us (Gliese 710) interstellar ambient, 029 Betelgeuse D-minor supergiant ambient, 030 Apophis asteroid flyby tension, 031 Earth Magnetic Field core dynamo pulse, 032 Landed on Titan sub-zero methane descent pad, or 033 21-Year Winters (Uranus) bowed vibraphone and glass harmonica. No drums, no trailer booms, no synthwave beats, no vocals.
```

---

## 2. Chapter Mood & Crossfade Map (`2.5 s` Crossfades Across Explicit `source=CARD` Rows)

| Chapter | Card Row | Audio Span (s) | Spoken Span (s) | Mood | Tempo | Texture & Narrative Role |
|---|---|---:|---:|---|---:|---|
| **Ch 0 (`Open`)** | — | `0.00–65.76` | `0.100–65.160` | **`awe`** | `66 BPM` | Bowed glass marimba, high celesta harmonics, and deep Kuiper Belt contrabass pad as New Horizons reveals the `1,000 km`, craterless nitrogen glacier of Sputnik Planitia at `−232 °C`. |
| **Ch 1 (*The Girl Who Named a World*)** | `R08` (`65.76–66.04`) | `65.76–159.22` | `66.040–158.620` | **`explain`** | `70 BPM` | `2.5 s` crossfade at `R08` (`0.60 s` breath after `65.160 s`): intimate plucked concert harp and warm pizzicato strings for Clyde Tombaugh's 18 February 1930 Flagstaff discovery, 11-year-old Venetia Burney naming Pluto in Oxford (`14 March 1930`), `2,377 km` diameter (`1/5` Earth), and `5.5-hour` (`39 AU`, `1/900`) twilight sunlight. |
| **Ch 2 (*The Moon That Never Sets*)** | `R20` (`159.22–159.48`) | `159.22–261.14` | `159.480–260.540` | **`awe`** | `66 BPM` | `2.5 s` crossfade at `R20` (`0.60 s` breath after `158.620 s`): suspended two-note horn pedal and shimmering string harmonics for the June 1978 Flagstaff discovery of Charon (`1,214 km`, `19,640 km` away — `20×` closer than our Moon) and `153-hour` (`6.4-day`) mutual tidal locking where Charon never rises or sets. |
| **Ch 3 (*Nine Years to the Kuiper Belt*)** | `R33` (`261.14–261.42`) | `261.14–368.22` | `261.420–367.620` | **`explain`** | `74 BPM` | `2.5 s` crossfade at `R33` (`0.60 s` breath after `260.540 s`): forward-moving analog Rhodes arpeggio and light spiccato violas for New Horizons' `58,536 km/h` launch (`19 Jan 2006`), the `248-year` (`30–49.3 AU`) orbit (`1979–1999` inside Neptune), `+14,000 km/h` Jupiter assist (`28 Feb 2007`), and `15-month` (`1–2 kbps`) `6.25 GB` downlink. |
| **Ch 4 (*The Glacier That Breathes*)** | `R45` (`368.22–368.52`) | `368.22–451.66` | `368.520–451.060` | **`awe`** | `72 BPM` | `2.5 s` crossfade at `R45` (`0.60 s` breath after `367.620 s`): dynamic harmonic lift at the `"Wrong."` midpoint twist (`368.520 s`, `59.8%` runtime) with warm polychordal string swells and slow breathing bass movement for Sputnik Planitia's city-sized solid nitrogen convection cells, `2–3 km` mountains, `600 km` valleys, and `6%` gravity haze. |
| **Ch 5 (*Where Water Is Bedrock*)** | `R54` (`451.66–451.96`) | `451.66–534.26` | `451.960–533.660` | **`explain`** | `68 BPM` | `2.5 s` crossfade at `R54` (`0.60 s` breath after `451.060 s`): crystalline low-register piano and sub-surface pulse for rock-hard `−226 to −240 °C` water-ice mountains, Alan Stern's `5 August 2026` discovery of basal liquid nitrogen rising through northern cracks (`~13 microbars`), deep internal water-ice ocean hints, and the preserved `v03` Ch 5 pickup (`528.180–533.660 s`). |
| **Ch 6 (*Beyond the Frozen Heart*) + Hold (`R74`)** | `R64` (`534.26–535.06`) | `534.26–634.16` | `535.060–616.040` | **`awe`** | `64 BPM` | `2.5 s` crossfade at `R64` (`0.60 s` breath after `533.660 s`): expansive, weightless blue-haze string choir and muted horn farewell for the `200,000 km` crescent departure portrait, the `1 January 2019` Arrokoth flyby (`6.4B km`, `35 km` long), `60 AU` milestone (`1 Oct 2024`), the preserved `v05_request` Real Worlds bridge to Triton (`−235 °C` geysers, `597.120–616.040 s`), and `R74` (`616.16–634.16 s`: **`2.5 s` full-level hold** `616.040–618.54 s`, nonzero underscore through the hold, **`10.0 s` music fade** `624.16–634.16 s`, **`2.0 s` picture fade** `632.16–634.16 s`). |
