# J2962 — 033 Uranus Long Master (`v05`) Moving Opening Build, Gates & Ben UAT Staging

- **Agent / Role:** `gemini` (`Gemini 4 Carbon`, elected acting Chief + worker on `J2962`)
- **Date:** 2026-11-16
- **Film:** `033_Why-This-Planet-Has-21-Year-Winters` (`Why Knocked-Sideways Uranus Has 21-Year Winters`)
- **Answers Ben's UAT Note (`OWB-033`, 16 Nov 2026 20:50Z on `v04`):** *"0:00 starts on a still image maybe we can add some video with our google flow credit or api"*
- **Verdict:** **`KEEP` (`PASS`)** — Replaced the `0:00–4.35 s` (`R01`, cuts `0` and `1`) static-looking composite in `v04` with real, public-domain **NASA Goddard Space Flight Center SVS 20390** 4K 60fps moving animation of sideways Uranus, its vertical upright rings, swirling polar clouds, and orbiting moons (`Shot 8`, distinct from Short `ZpEA8stoSPA`'s `Shot 9`). Built beside `v04` (`v04` untouched), keeping voice, music, SFX, runtime (`629.416667 s`, `15,106` frames @ `24/1` CFR), and every cut from `4.35 s` (`cut 2`) to `629.42 s` (`cut 146`) **bit-for-bit identical** to `v04`. Spend: **£0.00 cash, 0 Google Flow credits** (`ai_spend.py report` Flow balance read at `24,450.0` credits, untouched).

---

## 1. Spend & Source Provenance Check

1. **Google Flow Balance (`python3 scripts/ai_spend.py report`):**
   - Latest recorded Flow balance: **`24,450.0` plan credits** (at `2026-11-16T02:30:54Z`; period from `2026-10-08`, monthly Google AI Ultra cycle resets on the 12th).
   - **Spend on `J2962`:** **`£0.00` cash, `0` Flow credits, `0` API spend** — real public-domain NASA 4K moving video solved the opening cleanly without needing Veo generation.
2. **Moving Source Licence & Credit:**
   - **Source Page:** `https://svs.gsfc.nasa.gov/20390/` (*Uranus Animated*, NASA Goddard Space Flight Center / Conceptual Image Lab)
   - **Asset Used:** `Shot8_4k_mp4.mp4` (`3840×2160`, `60 fps`, stored on the NAS at `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/svs20390_Shot8_4k.mp4`, `81,049,457` bytes, SHA-256 `8345caca2a6cc4291554f19f86f1c2b98ceb777817c1c82a17f15fe83f761726`; distinct from standalone Short `ZpEA8stoSPA` which used `Shot 9`).
   - **Licence:** NASA Media Usage Guidelines — US Government Public Domain (free commercial YouTube use, non-endorsement).
   - **On-Screen & Description Credit:** Bottom-left house Didot italic `Credit: NASA / Goddard Space Flight Center` on cuts `0` and `1` (`0:00–4.35 s`), and added to `11_Upload-Package/Descriptions/uranus_21_year_winters_long_description_v01.txt` and `description_DRAFT_v01.txt`.

---

## 2. Files & Hashes Verified (`v04` Untouched)

| Artifact | Path | Bytes | SHA-256 |
|---|---|---:|---|
| Graded `R01` 24fps Plate | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/04_Generated-Clips/J2962_v05/svs20390_shot8_uranus_4k_graded_v05_silent.mp4` | `7,338,812` | `66fc943702cac3b0ecaa58d86066621f6dd4a5db8c5a70ff38a756593b4be40f` |
| Master `v05` (`J2962`) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/09_Final-Export/033_why_this_planet_has_21_year_winters_master_v05.mp4` | `357,066,696` | `1bb4a006bb0dab86cbe5a243ba42328a636bd9177b4fb421e7b19c6d8e954cbb` |
| Phone `v05` (`J2962`) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/09_Final-Export/033_why_this_planet_has_21_year_winters_master_v05_PHONE.mp4` | `48,403,763` | `a5bd1cd2f22a91afedffe566b3171e0730d8273530e7cfe8609fcdb688c82f43` |
| NAS `OWB UAT` (`v05`) | `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/033_why_this_planet_has_21_year_winters_master_v05.mp4` (+ `_PHONE.mp4`) | `357,066,696` / `48,403,763` | Verified identical SHA-256 on both files |
| iCloud `OWB UAT` (`v05`) | `~/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/033_why_this_planet_has_21_year_winters_master_v05.mp4` (+ `_PHONE.mp4`) | `357,066,696` / `48,403,763` | Verified identical SHA-256 on both files |
| R2 Stream (`owb-033-v05`) | `watch/owb-033-v05/06bbf6dad53c407f-033_why_this_planet_has_21_year_winters_master_v05_PHONE.mp4` (`https://board.oppti.dev/api/watch?v=owb-033-v05`) | `48,403,763` | `a5bd1cd2f22a91afedffe566b3171e0730d8273530e7cfe8609fcdb688c82f43` |
| Previous Master `v04` (untouched) | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/09_Final-Export/033_why_this_planet_has_21_year_winters_master_v04.mp4` | `357,159,206` | `3712479ae852dd318c4d8d0dfd18f7df08c1a857068c24c3d3792a35a27f11c3` |

- **Bit-Exact Audio & Tail Parity:**
  - Compressed audio stream hash (`ffmpeg -map 0:a:0 -c copy -f hash`): `SHA256=b8f3a81bdde8a10eb5971a16bd0013951aad4740b68e4f9880f77c1de430a9d4` on both `v04` and `v05`.
  - Compressed video stream hash from `4.50 s` to `629.42 s` (`cuts 2..146`): `SHA256=103eb9eaa3bd21694d4dad50957b1a0e303a83a98a6e51ead3a1169b078a3695` on both `v04` and `v05`.

---

## 3. Five Gates, First-30-Seconds Check & Multimodal QA (`PASS`)

1. **`clip_check.py` (`rc=0`, `PASS`):** `67` rows — `PASS` (`0` fails; sentence/card boundaries and end-after-VO checks clear).
2. **`picture_qa.py` (`rc=0`, `PASS`):** `147` cuts — `0` fail, `0` `>15 s` reuse warnings (`0.66×` and `0.77×` downscale from 4K on cuts `0` and `1`; `9` smooth Uranus globe/crescent advisory warns inspected full size on `picture_qa_review.jpg`, unchanged from `v04`).
3. **`polish_gate.py` (`rc=0`, `PASS`):** `147` cuts — `0` failed (`0` black/near-black, noise, split-panel, or jitter fails).
4. **`music_gate.py` (`rc=0`, `PASS`):** `uranus_score_bed_v01.mp3`, `629.4 s`, `70.6 BPM` (`Pace: 66-76 BPM`).
5. **`sfx_kit.py level` (`rc=0`, `PASS`):** `VO -20.2 LUFS`, `SFX -47.2 LUFS` (`-27.0 LU` relative to VO), `21` hits; master loudness `-14.5 LUFS`, `-1.5 dBTP`, `0` black frames.
6. **First-30-Seconds Rule (`PASS`):**
   - `(1)` Frame `0` (`0:00`) is already moving: real 4K NASA SVS animation of sideways Uranus with upright vertical rings, swirling north-polar cloud bands, and orbiting moons (`0:00–2.20 s` wide flyby -> `2.20–4.35 s` closer north-polar vortex cut); zero Orbit, title, logo, or fade before `0:30`.
   - `(2)` First spoken sentence states the title mystery and ends at `0:07.8` (`< 0:08`).
   - `(3)` Zero agenda or meta-promise; every sentence adds a concrete sourced fact.
   - `(4)` Concrete payoff counter (`21 EARTH YEARS`, `R03`) lands at `0:08.5–0:13.3` (`< 0:20`), followed by `EARTH 23.44° TILT` vs `URANUS 97.77° TILT` (`0:18.0–0:25.0`).
   - `(5)` Every cut in `0:00–0:38.67` (`cuts 0..12`, `928` frames) is `<= 4.00 s` (`2.20 s`, `2.15 s`, `3.83 s`, `2.62 s`, `2.57 s`, `2.30 s`, `2.30 s`, `3.53 s`, `3.53 s`, `2.98 s`, `3.54 s`, `3.56 s`, `3.56 s`), zero back-to-back code graphics, first chapter card at `0:58` (`> 0:45`).
7. **Demonstrated `moving_video_input` & `audio_input` Check (`PASS`):**
   - Recorded demonstrated capabilities via `chief_relay.py capabilities --agent gemini --available 'audio_input,moving_video_input'` and directly watched and listened to `master_v05.mp4` (`0:00–0:08` 540p & `0:00–0:35` 360p + full-resolution `1920×1080` frames at `0.0 s` and `2.5 s`). Verified genuine 3D orbital/cloud/camera motion from frame `0`, crisp Didot agency credit, smooth cut into `R02` at `4.35 s`, and clean British narration + score.
8. **Upload Package Dry-Run (`PASS`, No Live Upload):**
   - Updated `11_Upload-Package/PACKAGE_MANIFEST.json` (`master_v05.mp4`, SHA-256 `1bb4a006bb0dab86cbe5a243ba42328a636bd9177b4fb421e7b19c6d8e954cbb`) and added NASA Goddard SVS 20390 credit to `Descriptions/uranus_21_year_winters_long_description_v01.txt`; verified `npm run gate:episode` and `npm run youtube:package -- --dry-run` (`rc=0`).
