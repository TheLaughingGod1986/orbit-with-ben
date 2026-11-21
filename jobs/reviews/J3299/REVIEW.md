# J3299 Chief Review — Weekly Dated-Event Short (`7 December 2026 NASA Roman Space Telescope First Images`, `LEARNINGS` Rule 16 Test)

- **Job:** `J3299` (`Backlog OWB: this week's dated-event Short (LEARNINGS rule 16 test), script + packaging, park for Chief`, `kind: script`, `backlog: owb-dated-short`)
- **Deliverable:** `02_Video-Projects/_dated_shorts/2026-12-07_roman-telescope-first-images.md` (PR `#1117` merged cleanly onto `main` at `45336c4a4e`)
- **Elected Acting Chief:** `gemini` (acting Chief for OWB and HOS per `chief_relay.py status` at `2026-11-21T22:23:22Z`: `claude` out until `2026-11-22T07:50:00Z`, `chief` Grok Bot down until `2026-11-22T00:55:22Z`, `codex` down until `2026-11-24T23:26:00Z`, `gemini` UP)
- **Verdict:** **`SCRIPT PASS` (Elected Acting Chief, 21 Nov 2026). PR `#1117` merged (`45336c4a4e`). Event (`Mon 7 Dec 2026 20:30 UTC` NASA Nancy Grace Roman Space Telescope First Images unveiling), official NASA sources (`S1`–`S5`), target slot (`Thu 3 Dec 2026 11:30 UTC`, Related video `ziKBPJ6FY0U`), 48-word Apophis-mould script + `C7` VO trim order, and full-bleed `9:16` £0 picture plan are locked. Voice-over on plan credits approved (up to 2 takes; `15,352` ElevenLabs credits remaining at `2026-11-21T08:30Z`), NAS bed reuse waiver approved (`nearest-star_score_bed_v01.mp3`), and Mini-pinned build job queued with binding continuous-VO pacing guard (no 3.65 s mid-Short silence). Requires Ben's OK on the board by Wed 2 Dec 2026 18:00 London before going public (`£0` spent in `J3299`).**

---

## 1. Independent Chief Verification (`PASS`)

1. **Event Pick & Non-Overlap (`PASS`):**
   - **Event:** **NASA Nancy Grace Roman Space Telescope First Images Unveiling — Monday, 7 December 2026 at `20:30 UTC` (`3:30 p.m. EST` / `12:30 p.m. PST`)**, live from the AGU Annual Meeting on `nasa.gov/live` (`+16 days` ahead of 21 Nov 2026 — centre of the `10–21 days ahead` brief window).
   - **Non-overlap:** Verified against `00_Brand/Channel-Setup/social/UPLOADS.json`, `05_Analytics/kanban/film_briefs.json`, `05_Analytics/owb/snapshots/2026-11-20.json`, prior dated Shorts (`HXacmpYkXcA` Supermoon 19 Nov, `GbELka8Yu9U` Moon–Jupiter 26 Nov), and the AR cohort (`J1356`). Zero Roman or space-telescope Shorts are live, scheduled, or open in Nov–Dec 2026 (clears `LEARNINGS` Rule 35 completely). Skipping Europa Clipper (lead-time squeeze), Moon–Venus (3rd consecutive Thursday Moon Short), obscure asteroid `2016 NV` (recent asteroid Shorts), BepiColombo (no fixed UTC time), Jupiter–Regulus (recent Jupiter Short), and deferring Geminids (`13–14 Dec`, `+22–23 days`) to next week is sound.
2. **Official NASA Sources (`S1`–`S5`, Verified Live on 21 Nov 2026, `PASS`):**
   - **`S1` (NASA Headquarters Media Advisory `M26-088`, 17 Nov 2026, HTTP 200):** Verbatim match confirmed for `3:30 p.m. EST (12:30 p.m. PST) Monday, Dec. 7` (`2026-12-07 20:30 UTC`), `https://www.nasa.gov/live`, `dark energy, dark matter, and worlds outside our solar system`, `Pixel adoption` (*"NASA invites the public to claim a corner of the universe with one of Roman's select first images"*), `Aug. 30` launch from KSC on SpaceX Falcon Heavy, and `three-month, million-mile trip to its final orbit at the Sun-Earth Lagrange Point 2`.
   - **`S2` (NASA Science *Wide Field Instrument*, HTTP 200):** Verbatim match confirmed for *"bigger than the apparent size of a full Moon"*, *"200 times smaller"* (Hubble WFC3), *"nearly 100 times smaller"* (Hubble ACS), *"over 50 times as much sky"*, and *"up to 1,000 times faster"*.
   - **`S3` (NASA Science *Mission Overview*, HTTP 200):** Verbatim match confirmed for *"at least 100 times larger than Hubble's"*, *"billion galaxies"*, and `Launch August 30, 2026`.
   - **`S4` (NASA Science *Roman FAQ*, HTTP 200):** Verbatim match confirmed for `7.9 feet (2.4 meters) in diameter – the same size as the Hubble Space Telescope's primary mirror`, `288-megapixel multi-band near-infrared camera`, and `over 42 feet (12.7 meters) long – about the length of a semi-truck trailer`.
   - **`S5` (NASA Science *Adopt a Pixel*, HTTP 200):** Verbatim match confirmed (*"Claim your pixel on one of the first images from NASA's Nancy Grace Roman Space Telescope!"*).
3. **Target Publish Slot (`PASS`):**
   - **Thursday, 3 December 2026 at 11:30 UTC (London)** (`4.4 days` before `2026-12-07 20:30 UTC`, inside Rule 16's `3–7 days before` window).
   - Verified empty in `00_Brand/Channel-Setup/social/UPLOADS.json` after `J3123`/`J3330` (`6f0fce5618`): Wed 2 Dec `18:00Z` Long `G5uMANXHtNU` → **Thu 3 Dec EMPTY** → Fri 4 Dec `11:30Z` Short `5qw8oW5Pwpc` → Sat 5 Dec `11:30Z` Short `BTuL_QBbEgY`. Continues the weekly Thursday `11:30 UTC` dated-event slot (`19 Nov`, `26 Nov`, `3 Dec`), 7 days after `GbELka8Yu9U`, zero Rule 35 clash.
   - **Related video (`ziKBPJ6FY0U`):** Verified public OWB space-telescope Long `004` (*JWST Found Galaxies That Shouldn't Exist Yet*) in `05_Analytics/owb/snapshots/2026-11-20.json`.
4. **Script, Rules 8/16/24/35/39/40/E1 & Asset Check (`PASS` with Binding Build Guards):**
   - **Title (`49 chars <= 50`):** `What Will NASA's Roman Telescope Reveal on Dec 7?` (plain positive question naming subject + date hook).
   - **Frame-0 Hook (`0.0–2.0 s`, 3 words):** `**100X** MORE SKY` (yellow `100X`; distinct from title).
   - **Custom Cover Text (`2 words`):** `**100** HUBBLES` (zero words shared with title).
   - **Script (`48 words`, inside `44–52`):** Opens word 1 on the named subject + surprise claim (*"NASA's Roman telescope unveils its first images on December seventh."*, passing Rule 39 — no calendar dateline on word 1), everyday full-Moon sky scale (Line 2, Rule 31), Hubble mirror vs 100-views tension (Line 3), concrete payoff (Line 4), and direct viewer participation complete-sentence ending (*"Watch NASA live, and claim your own pixel."*, Ben's `J2478` v04 rule).
   - **£0 Visual & Audio Assets Verified Live:**
     - NASA SVS `#15121` (`15121_HUBROM_VERT_MP4.mp4`, HTTP 200, `790 MB`) & `#15081` (`15081-_Trailer_Long_Vertical.mp4`, HTTP 200, `445 MB`, caption-free vertical cuts).
     - Local Mac mini SSD pool (`/Users/benjaminoats/_desk/wt-J2478/02_Video-Projects/_dated_shorts/2026-11-24_supermoon/07_Edit-Project/pool_v01/svs5587/phases_2026_plain_v_1920p30.mp4` & `phases_2026_plain_2160p30.mp4`).
     - NASA Images API: `GSFC_20171208_Archive_e001061`, `GSFC_20171208_Archive_e001651`, `KSC-20260830-MH-CSH01-0001-Roman_Space_Telescope_Launch_High_Speed_Footage`, `KSC-20260830-MH-SPX01-0001-Roman_Space_Telescope_Launch_ISO_Drone-4K-M26246` (all 4 verified live).
     - NAS music bed (`/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/026_How-Far-Is-The-Nearest-Star/05_Music/nearest-star_score_bed_v01.mp3`, verified on NAS).

---

## 2. Binding Chief Build Guards (For the Queued Mini Build Job)

1. **Continuous Natural-Speed VO Pacing (No 3.65 s Silent Bridge):** The draft shot table listed `[Instrumental bridge into Line 4]` at `s05` (`9.30–12.95 s`). The build job **must NOT** insert a 3.65 s spoken silence. Record all 5 lines continuously at natural `1.00×` speed (zero `atempo`), tighten room-tone pauses only (`<0.4 s` between sentences, never `>0.4 s` in `0–6 s` per Rule 39), and cut all 7 plates to the real word timestamps (Cut 1 `≤2.8 s` to a distinct visual scene per Rule 40, Cut 2 `≤4.8 s`, max shot hold `≤4.0 s`).
2. **Duration & `C7` Trim Guard:** Target **`16.0–19.0 s`** total runtime (Ben's 19 Nov Shorts gate band; hard cap `20.0 s` per Rule 16) including a `~1.0 s` forward-loop tail (`≤0.3 s` crossfade). Apply the plan's pre-approved `C7` trims (`45w` Trim 1 → `39w` Trim 2) if natural-speed VO + loop exceeds `19.0 s` (or `20.0 s` hard cap) or starts Line 4 past `13.5 s`. Keep the title banner inside `9.0–14.0 s` clear of the sole `DATA` overlay (`11.5%` height inside the 16:9 centre band).
3. **Approved Spend & Waivers:**
   - **ElevenLabs VO:** Approved up to **2 takes** on existing subscription plan credits (`15,352` credits left at `2026-11-21T08:30Z`, `TTS_PAUSE` absent; `04_Audio/tools/vo_take.py`, `eleven_v3`, Ben Orbit Narrator; `vo_check.py` must PASS).
   - **Music Bed Reuse Waiver (`£0`):** Chief approves reusing `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/026_How-Far-Is-The-Nearest-Star/05_Music/nearest-star_score_bed_v01.mp3` with a per-Short Chief waiver JSON (`music_gate_<job>_chief_waiver.json`), matching the `J2916` precedent.
   - **Picture & SFX:** `£0` (public-domain NASA assets + own `code_graphics.py` mosaic/overlay + house `sfx_kit.py`).
4. **Disk Hygiene:** Stage large SVS MP4 downloads and render scratch on the NAS (`/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_dated_shorts/2026-12-07_roman-telescope-first-images/`) because Mini SSD free space is ~12.4 GB.
5. **No Upload / Schedule:** Deliver SHA-verified `v01` master, cover, stems, and passing gate reports (`gate_shorts_open.py`, `picture_qa.py`, `polish_gate.py`, `music_gate.py`, `sfx_kit.py level`, `thumb_preview.py short`) and block with `parked for Chief: dated-event Short v01 ready for review` for Chief perceptual review before Ben's watch (due **Wed 2 Dec 2026 18:00 London**; if missed, do not upload).
