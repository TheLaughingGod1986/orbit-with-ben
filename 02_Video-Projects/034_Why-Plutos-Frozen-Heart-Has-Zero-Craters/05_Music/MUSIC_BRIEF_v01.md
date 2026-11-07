# Music Brief v01 — 034 Why Pluto's Frozen Heart Has Zero Craters (Pluto)

- **Episode:** `034_Why-Plutos-Frozen-Heart-Has-Zero-Craters` (`Real Worlds` series: Pluto & Charon)
- **VO Master:** `02_Voiceover/pluto_frozen_heart_vo_v03.wav` (`616.160 s`, `-19.9 LUFS` integrated, `-23.0 dB` mean, `-3.7 dBTP` true peak; SHA-256 `2be8030b6c42b673530351014c71bca1a6c31a10af9746539bb2a1ce7dcf7685`, accepted full VO PASS in `jobs/reviews/J2352/REVIEW.md`)
- **Target Music Runtime:** `634.16 s` (`10:34.16` — full `616.160 s` VO + `18.00 s` moving end-screen hold; music holds at full bed level `2.5 s` past the last word at `616.040 s` and fades cleanly over `631.16–634.16 s`)
- **Target Output Stem (at assembly stage):** `05_Music/pluto_score_bed_v01.mp3` + `05_Music/pluto_score_bed_v01_plan.json`
- **Generator:** `python3 04_Audio/tools/generate_music_bed.py` (API only; **not run in `J2353`**, £0 / 0 credits spent in this shot-list planning job)
- **Gate:** `python3 scripts/music_gate.py 02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters --bed 05_Music/pluto_score_bed_v01.mp3 --video <cut.mp4>`

---

## 1. Exact API Prompt (`Pace:` and `NOT:` Mandatory Lines)

```text
Sub-zero Kuiper Belt space-documentary score for Pluto, Charon, and Sputnik Planitia, alternating between vast twilight horizon wonder ("awe": warm bowed glass marimba, high crystalline celesta harmonics, solo muted French horn, and deep velvety contrabass pad) and clean, curious astronomical discovery ("explain": delicate plucked harp, soft pizzicato violas, and warm analog Rhodes pulse). Gentle lift at the Chapter 4 midpoint twist ("Wrong.") as Sputnik Planitia's convecting nitrogen heart awakens, resolving into a weightless blue-haze departure pad over the final 20 seconds.
Pace: 64-74 BPM, calm measured pulse matched to British narration, lifting gently at chapter transitions without heavy percussion.
NOT: Do not sound like 021/022 solar brass drones, 023/024/025 shared ambient track, 026 Venus metallic industrial dread, 027 Mars dusty desert cello, 028 Titan sub-aquatic methane sonar, 029 Betelgeuse orchestral doom brass, 030 Moon clockwork lute, 031 Earth/Mercury high-tension magnetic pulse, 032 Saturn/Titan cathedral organ and choral rings, or 033 Uranus bowed vibraphone and glass harmonica. No drums, no trailer booms, no synthwave beats, no vocals.
```

---

## 2. Chapter Mood & Crossfade Map (`2.5 s` Crossfades Across Chapter Breaths)

| Chapter | Audio Span (s) | Spoken Span (s) | Mood | Tempo | Texture & Narrative Role |
|---|---:|---:|---|---:|---|
| **Ch 0 (`Open`)** | `0.00–65.60` | `0.100–65.160` | **`awe`** | `66 BPM` | Bowed glass marimba, high celesta harmonics, and deep Kuiper Belt contrabass pad as New Horizons reveals the `1,000 km`, craterless nitrogen glacier of Sputnik Planitia at `−232 °C`. |
| **Ch 1 (*The Girl Who Named a World*)** | `65.60–159.05` | `66.040–158.620` | **`explain`** | `70 BPM` | Intimate plucked concert harp and warm pizzicato strings for Clyde Tombaugh's 18 February 1930 Flagstaff discovery, 11-year-old Venetia Burney naming Pluto in Oxford (`14 March 1930`), `2,377 km` diameter (`1/5` Earth), and `5.5-hour` (`39 AU`, `1/900`) twilight sunlight. |
| **Ch 2 (*The Moon That Never Sets*)** | `159.05–260.98` | `159.480–260.540` | **`awe`** | `66 BPM` | Suspended two-note horn pedal and shimmering string harmonics for the June 1978 Flagstaff discovery of Charon (`1,214 km`, `19,640 km` away — `20×` closer than our Moon) and `153-hour` (`6.4-day`) mutual tidal locking where Charon never rises or sets. |
| **Ch 3 (*Nine Years to the Kuiper Belt*)** | `260.98–368.07` | `261.420–367.620` | **`explain`** | `74 BPM` | Forward-moving analog Rhodes arpeggio and light spiccato violas for New Horizons' `58,536 km/h` launch (`19 Jan 2006`), the `248-year` (`30–49.3 AU`) orbit (`1979–1999` inside Neptune), `+14,000 km/h` Jupiter assist (`28 Feb 2007`), and `15-month` (`1–2 kbps`) `6.25 GB` downlink. |
| **Ch 4 (*The Glacier That Breathes*)** | `368.07–451.51` | `368.520–451.060` | **`awe`** | `72 BPM` | Dynamic harmonic lift at the `"Wrong."` midpoint twist (`368.520 s`, `59.8%` runtime): warm polychordal string swells and slow breathing bass movement for Sputnik Planitia's city-sized solid nitrogen convection cells, `2–3 km` mountains, `600 km` valleys, and `6%` gravity haze. |
| **Ch 5 (*Where Water Is Bedrock*)** | `451.51–534.36` | `451.960–533.660` | **`explain`** | `68 BPM` | Crystalline low-register piano and sub-surface pulse for rock-hard `−226 to −240 °C` water-ice mountains, Alan Stern's `5 August 2026` discovery of basal liquid nitrogen rising through northern cracks (`~13 microbars`), deep internal water-ice ocean hints, and the preserved `v03` Ch 5 pickup (`528.180–533.660 s`). |
| **Ch 6 (*Beyond the Frozen Heart*) + Hold** | `534.36–634.16` | `535.060–616.040` | **`awe`** | `64 BPM` | Expansive, weightless blue-haze string choir and muted horn farewell for the `200,000 km` crescent departure portrait, the `1 January 2019` Arrokoth flyby (`6.4B km`, `35 km` long), `60 AU` milestone (`1 Oct 2024`), the preserved `v05_request` Real Worlds bridge to Triton (`−235 °C` geysers, `597.120–616.040 s`), and the `18.00 s` end-screen hold (`616.16–634.16 s`, fading cleanly over `631.16–634.16 s`). |
