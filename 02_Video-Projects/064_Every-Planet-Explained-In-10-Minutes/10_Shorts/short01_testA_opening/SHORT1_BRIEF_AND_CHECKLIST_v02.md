# OWB 064 Short 1 (Test A Opening) — Brief & Approved Learnings Checklist (`v02`, `J3903`)

- **Film:** `OWB:064` — *Every Planet Explained in 12 Minutes (Mercury to Neptune)* (planned long air: **Wed 16 Dec 2026 18:00 London**)
- **Short:** Companion Short 1 of 2 — **Test A Opening Short** (`studio/RULES.md` Lesson 5)
- **Stem:** `064_short01_testA_opening_v02`
- **Proposed Candidate / Gate-Check Slot:** **Mon 28 Dec 2026 11:30Z** (first free non-colliding `Mon/Wed/Fri/Sat 11:30 London` Orbit Short slot strictly after 064 long goes public on Wed 16 Dec 18:00 London; **NOT scheduled yet — MUST NOT upload or air before 064 long is public**)
- **Canonical NAS Master (`v02`):** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes/10_Shorts/short01_testA_opening/06_Final-Exports/064_short01_testA_opening_v02.mp4`
- **Master SHA-256 (`v02`):** `8b7a218c73b1c790f722f4410e67e4fe04d7e06276e3d4a4bbcbceed38c38968`
- **Preserved Prior Draft (`v01` untouched on NAS):** `064_short01_testA_opening_v01.mp4` (`b805c51d02acd0e43adf9c9645c993c91d148641e068e918d93136e20b25a4b6`)
- **Source Provenance (exact locked hashes verified):**
  - Parent master v03: `d59057aed1590e7f6ef097513256a0548c4f9b1d7e544c4bade28aa83fef647a` (`0:00–0:32.85` Mercury opening through Colombo 1965)
  - Locked VO WAV: `4b478fcded393890064ffd285a4121882dc26e0515f3cadc6569adf0465616aa` (71 verbatim words, S1–S4; `0` new ElevenLabs chars)
  - Film score bed: `3e47e9d6da9aca6836a00c27a1fa58e53801190ae06ed445966ed51f5c0d75c6` (`every_planet_score_bed_v01.mp3`)
- **Spend:** `£0.00` cash, `0` ElevenLabs chars, `0` Flow/Vertex credits.
- **Upload / Scheduling Status:** Not uploaded, not scheduled, not added to `shorts_open_library` yet. Ready for independent QA / Chief ruling and Ben UAT watch.

## Visual Inspection Fixes (`v01` → `v02`, `v01` Preserved on NAS)

Frame-by-frame transition inspection of `v01` caught and fixed 5 defects before submission:
1. **Eliminated `12.88–14.00 s` title-banner vs `R03b` graphic collision:** Moved the `R03a → R03b` cut from `12.875 s` to `14.083 s` (`R03a` `3.958 s <= 4.00 s`, zero split words between `"to"` and `"seven"`), strictly after `TITLE_OUT = 14.00 s`, and simplified `R03b` to a single word-matched `UP TO 7.0× SUNLIGHT` bar (`68 px` Arial Black, `11.2%` of the `608 px` 16:9 safe band) with Earth `1×` reference slice, removing the unspoken `+430 °C HEAT` bar from `R03b`.
2. **Restored full `.srt` captions (`00:00:00,100 --> 00:00:29,639`):** Added `srt_chunks_full()` so `064_short01_testA_opening_v02_en-GB.srt` captions all 71 spoken words across 29 cues (fixing the 5-second `9–14 s` SRT gap in `v01`) while keeping burned-in captions clear of the `9–14 s` title banner.
3. **Extended `1965 · GIUSEPPE COLOMBO` teach pill (`23.75–27.70 s`, `3.95 s <= 4.00 s`):** Previously ended at `26.40 s` before `"Giuseppe Colombo"` (`26.52–27.64 s`) was spoken; now stays on screen cleanly across the full name with matched `y_offset=-90` across `R04a`→`R04b`.
4. **Extracted exact Frame 0 still (`-ss 0.00`)** (`064_short01_testA_opening_v02_frame0.jpg`, no premature `"ON MERCURY"` subtitle) and re-ran `gate_shorts_open.py`, `polish_gate.py`, `picture_qa.py`, and canonical 13-bed MP3 `music_gate.py` directly against the canonical NAS MP4.
5. **Corrected proposed candidate slot** from invalid Thursday `2026-12-17` to non-colliding `Mon 28 Dec 2026 11:30Z` (`2026-12-28`, valid `Mon/Wed/Fri/Sat 11:30` Orbit Short day, strictly after Wed 16 Dec long air; gate-check/candidate date only, not scheduled).

## Approved Learnings Checklist (`10_Shorts/README.md`)

- [x] **#1 · Title:** Positive question naming the subject: *"Why Does Water Ice Survive 430°C Heat on Mercury?"* (Alt: *"How Does Mercury Hide Water Ice at 430°C?"*).
- [x] **#2 · First-second rule (`0.0–1.5 s`, `J2429`):** Opens full-bleed `1080×1920` (`24/1` CFR, `0/62` padded frames, `visor_frac = 0.0`) on a real rotating 3D Mercury globe mapped from NASA MESSENGER `PIA17386.jpg` (`frame0_diff_0_1_5s = 5.66 >= 1.50`, `motion_0_1s = 13.32 >= 10.0`, no fade-in, no Orbit), with 2–3 word hook caption **`ICE AT` (white) / `430°C?` (`#FFE000`)** stamped at `t = 0.00 s`, VO word 1 (`"On"`) at `0.07–0.10 s <= 0.15 s`, naming `"Mercury, the Sun's closest planet"` inside `0.0–1.5 s`, zero meta-promise.
- [x] **#3 · Motion (no static zoom in 4–8 s):** 12 full-bleed shots with cuts at `2.500`, `4.458`, `6.542`, `8.125`, `10.125`, `14.083`, `16.417`, `20.042`, `23.458`, `26.458`, `29.750 s` (max shot `3.958 s <= 4.00 s`, zero split words across all 11 cut boundaries, zero jitter in `polish_gate`).
- [x] **#6 · Payoff (Test A opening exemption):** Test A Opening Short lifts the parent long's locked cold open verbatim (`30.750 s`, within Test A's `30–38 s` opening range; exempt from 16–19 s / 22–27 s band until Test A readout per `studio/RULES.md` Lesson 5). Climactic temperature plunge (`−180 °C`) lands at `20.04–23.46 s` (`65–76%`) and Colombo 1965 spin-mystery cliffhanger lands at `23.56–29.64 s` (`77–96%`), handing directly to the full long film.
- [x] **#7 · Seam (no 0.5 s pause in 4–8 s):** S1→S2 breath tightened to `0.240 s < 0.25 s`, cutting cleanly at `2.500 s` (`R01b` sunlit crater terrain), `4.458 s` (`R01c` enhanced-color globe `PIA16853`), and `6.542 s` (`R02a` north-polar Prokofiev ice mosaic `PIA19411`), zero Orbit reaction, zero meta-promise.
- [x] **#8 · 60% stayed-to-watch:** Frame-0 source = rotating 3D Mercury mapped from `PIA17386` (`f0diff=5.66`, `motion=13.32`); first word `0.07–0.10 s <= 0.15 s`; subject + hook inside `0.0–1.5 s`; first cut `2.50 s <= 3.0 s`; no meta-promise/logo/intro (`y`); last word → loop `1.11 s <= 1.5 s`.
- [x] **#9 · 70% average viewed:** Runtime `30.750 s` (Test A opening cut, 738 frames @ 24 fps CFR); longest shot `3.958 s <= 4.0 s`; exact promoted long title `'Every Planet Explained in 12 Minutes (Mercury to Neptune)'` at `9.00–14.00 s` and on End Card `29.750–30.750 s`; single Teach overlay `1965 · GIUSEPPE COLOMBO` at `23.75–27.70 s` (`3.95 s <= 4.0 s`) inside the 16:9 safe band; matched-cut rotating Mercury loop return to Frame 0 (`y`).

## Perceptual QA & UAT Boundary

- All 7 automated gates, canonical 13-bed MP3 music uniqueness check, CFR playback health, and full-size contact-sheet / transition-frame visual inspections (`review_12shots.jpg`, `open_sheet.jpg`, `picture_qa_review.jpg`, `frame0_preview.jpg`, `cover_preview.jpg`, and transition stills at `0.00/1.50/9.50/13.50/14.30/15.80/22.80/26.80 s`) passed.
- Per studio rules, automated measurements and still inspections do **not** claim audio listening or moving-video motion perception; independent QA (`kind: qa`), elected-Chief PASS & PR merge, and Ben's phone UAT watch supply final watch/listen approval before any upload or scheduling.
