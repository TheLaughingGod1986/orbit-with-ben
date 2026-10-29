# J1206 — moving-source verify + Uranus sentence-reorder feasibility (29 Oct 2026)

Cursor worker (`assembly`), no spend, no v03 render, no YouTube/Buffer/UPLOADS changes.

Chief (acting Codex on J1204) authorized one no-spend follow-up to search the wider archive first, then acquire verified public-domain / commercially reusable footage, check category + real subject motion (not pan/zoom of one still), and re-test whether the complete existing second Uranus sentence can lead.

Machine evidence lives on NAS (not in git):

- `/Volumes/data/mac-mini-archive/scratch/J1206/raw/`
- `/Volumes/data/mac-mini-archive/scratch/J1206/frames/`
- `/Volumes/data/mac-mini-archive/scratch/J1206/CANDIDATES.json`

---

## A. Wider archive search (before download)

| Pool | Result |
|---|---|
| `…/scratch/J0914/raw/` | Neptune + ISS only (matches J1204 inventory) |
| `…/scratch/J1199/` | JPEG plates + rejected JPEG-assembly probes/renders only — not eligible source |
| `…/scratch` depth 4 name hits (`uranus`/`meteor`/`titan`/`dragonfly`/`perseid` video) | **none** outside J1199 probes |
| Film `032` Titan | Mini folder empty of mp4/mov/webm; NAS project folder not present |
| Film `052` Miranda | no harvested Uranus planet video |
| Film `021` Saturn | edit row mp4s exist; no Titan-named moving open plate for S6 |

**Archive verdict:** no eligible *existing* moving subject footage for S4/S5/S6 openings. Proceeded under Chief’s PD-acquire authorization.

---

## B. Uranus sentence-reorder feasibility (existing audio only)

### Provenance

| Item | Path / value |
|---|---|
| Locked spoken (v02, Stay already excised) | See meta `spoken` |
| VO stem | `/Volumes/data/mac-mini-archive/scratch/J1199/uranus_v02/vo_v02.wav` |
| VO sha256 | `484a7d9ead015de266f6eb9937b6f6b9b5e8e9ec7c1b0124750ecea77f5410df` (matches `owb_sa_s4_uranus_v02_meta.json`) |
| Caption map | `06_Final-Exports/owb_sa_s4_uranus_v02_meta.json` (post–Stay timings) |
| Raw trim words (pre–Stay map) | `vo_v01/trim/owb_sa_s4_uranus_vo_v01_trim_words.json` |

Full transcript (v02 audio order):

1. **S1** `This planet has winters that last 21 years.` — **0.10–3.40 s** (3.30 s). Surprise `21` at **2.26 s**. Does **not** name Uranus.
2. **S2** `Uranus is tipped 97 degrees, so it rolls on its side.` — **3.55–7.13 s** (3.58 s). Name at **3.55**; surprise `97` at **4.73** (~1.18 s into S2); `rolls` at **6.07**.
3. **S3** `One orbit takes 84 years.` — **7.53–9.91 s**
4. **S4** `For about a quarter of that, the sun stares down on one pole while the other half sits in the dark` — **10.31–15.77 s**

Chief correction applied: a picture cut ≤3 s may land **while** an intact spoken sentence continues; the first-cut cap does **not** require truncating a 3.3–3.6 s sentence.

### Sentence-boundary edit decision list

| # | Option | Edit (no word splice, no new VO) | Subject in sentence 1? | Surprise in sentence 1? | Coherence | Decision |
|---|---|---|---|---|---|---|
| 0 | Keep current order | none | No (`This planet`) | Yes (`21 years`) | OK as written | **Reject** for rule-8 subject+surprise in sentence 1 |
| 1 | **Lead with complete S2**, then S1, S3, S4 | Hard cut VO at sentence boundaries: take S2 block 3.55→7.13, place at timeline 0; append S1 0.10→3.40; then S3; then S4. Breath gaps between blocks ≈0.4 s as in current map | **Yes** (`Uranus` first word) | **Yes** (`97 degrees` / rolls on its side) | Strong: name+tilt first, then winters as consequence (`This planet` now anaphora to Uranus) | **FEASIBLE — recommend** |
| 2 | Lead with S2, then S3, S4, then S1 | Same cuts, different order after lead | Yes | Yes | OK but winters punchline is delayed to the end | Feasible alternate |
| 3 | Lead with S2+S3 as one opener before first picture cut ends | Would hold first *picture* cut across two sentences; spoken “sentence 1” for rule 8 is still only S2 if we define by `.` boundaries | Yes (in S2) | Yes | OK | Unnecessary if option 1 used |
| 4 | Truncate S1 before `years.` to force ≤3 s | Forbidden (clips a line / not a complete sentence) | — | — | — | **Reject** |
| 5 | Rewrite / generate VO so sentence 1 says Uranus | Forbidden | — | — | — | **Reject** |

**Feasibility verdict:** **YES — option 1.** Complete existing S2 can lead coherently with named subject + surprise. Picture first-cut ≤3.0 s can fall during S2 (e.g. at ~2.7 s wall-clock) while S2 audio continues to 3.58 s. No new VO required.

Audio cut list for a future assembly job (sample-accurate from v02 stem; do not render until Chief OK):

1. `vo_v02.wav` in **3.55–7.13** → new 0.00–3.58  
2. `vo_v02.wav` in **0.10–3.40** → follows after ~0.4 s breath  
3. `vo_v02.wav` in **7.53–9.91**  
4. `vo_v02.wav` in **10.31–15.77**  

Captions must be remapped word-for-word to the new timeline (still the same words).

---

## C. Candidate moving sources (acquired, motion-checked)

Rights baseline: NASA SVS help + NASA media usage — content public domain unless noted; licensed music stripped (silent picture only). Dragonfly page: NASA/Johns Hopkins APL artist concepts. PIA17656: NASA/JPL-Caltech/ASI/USGS.

### S4 Uranus — primary candidate

| Field | Value |
|---|---|
| Title | Uranus Beauty Pass 1 (Shot4) |
| Page | https://svs.gsfc.nasa.gov/20390/ (parent film https://svs.gsfc.nasa.gov/14580) |
| Category | **CGI / Conceptual Image Lab animation** (not spacecraft camera footage). Subject motion is camera move around a rendered Uranus+rings, **not** a Ken Burns of one still — frame 0 vs 2.0 s shows different limb/storm framing (see `frames/Shot4_1k_mp4_t0_0.00s.jpg` vs `…_t3_2.00s.jpg`). |
| Local | `/Volumes/data/mac-mini-archive/scratch/J1206/raw/Shot4_1k_mp4.mp4` |
| SHA-256 | `32370afa93cb69570ec05ee9abd1e9670171deb2ab33ceed6807d63dde716526` |
| Dims / dur | **1920×1080**, 10.00 s, h264 |
| Proposed in/out | **0.00–2.70 s** (picture first cut ≤3 s; VO S2 may continue) |
| 9:16 centre crop | crop width ≈ **607.5** px from 1080h; scale to 1080×1920 ≈ **1.778×** → **PASS** ≤2.35× |
| Gate risk | `picture_qa` may still **FAIL/WARN** as computer model / simulation / artist CGI. Public-domain status alone does not clear that. Chief must decide if SVS CGI is acceptable the way Neptune SVS was for S2, or reject. |

Alternates (same page, same category CGI):

| File | SHA-256 (see CANDIDATES.json) | Notes |
|---|---|---|
| `CloudBRoll_1k_mp4.mp4` | in JSON | 1920×1080, ~5 s, strong swirl motion; **close-up atmosphere only** — weaker as “Uranus the planet” at frame 0 |
| `Shot16_1k_mp4.mp4` | in JSON | 1920×1080 fly-by; early motion weak (near-black start) |

### S5 Shooting stars — explicit negative (this pass)

| Candidate | Why it fails |
|---|---|
| SVS 20271 `Geminid-v05_h264.webm` | https://svs.gsfc.nasa.gov/20271 — **constellation diagram animation** (Orion stick-figure over silhouette town). Mean abs frame diff ~0.15–0.3; no meteor streak at 0/5/15/25/35 s. **Not** shooting-star subject motion. |
| Archive Perseids JPEGs | Still long-exposures only (J1204) |
| NASA images API `Perseid meteor video` / `meteor streak` | Only “What’s Up” skywatching packages — not isolated meteor streak b-roll at usable open |

**Missing input:** genuine meteor **video** (streak in camera, not a still, not a constellation graphic), ≥~3 s, crop-safe for 9:16 at ≤2.35×, with clear PD/commercial-reuse evidence.

### S6 Titan — candidate with caveats

| Field | Value |
|---|---|
| Title | Flying over an Extraterrestrial Land of Lakes (PIA17656), unannotated |
| Page | https://science.nasa.gov/photojournal/flying-over-an-extraterrestrial-land-of-lakes/ |
| Category | **Colorized radar flyover animation** built from Cassini radar 2004–2013 (USGS stereo + JPL animation). Real sensor data → reconstructed topography; **not** optical camera video. Heights exaggerated 10×; haze added. Straight radar-swath artifacts visible. |
| Local | `…/J1206/raw/PIA17656_Unannotated-1280.mov` |
| SHA-256 | `ff9f7ff1c0b8e29fde4ab1962a058fbac204ea0eabae27bf648c1bf363ec7393` |
| Dims / dur | **1280×720**, 63.67 s |
| Motion | Strong (mean abs diff vs f0 up to ~13.8 at 2 s). Camera flies over lakes/seas — subject motion is flyover, not pan of one still. Frames: `frames/PIA17656_t*.jpg` |
| Proposed in/out | **0.00–2.70 s** (Kraken/Ligeia approach) |
| Upscale if filled to 1920h | **2.667× → FAIL** hard 2.35× rule |
| Mitigations for Chief | (a) 16:9 centre-band fit + feathered blur fill so scale ≤2.35×; or (b) reject and seek ≥1080p optical Titan plate; (c) expect `picture_qa` WARN/FAIL as reconstruction/simulation |
| Rejected local acquires | KSC `ksc_071304_ctitan` / `ksc_110404_cassini_flyby` NASA images packages: **320×212 only** (orig=preview) → upscale ~9×, unusable |

### Dragonfly (mid-film VO beat on S6)

| Field | Value |
|---|---|
| Title | Dragonfly Taking Off (2024) |
| Page | https://science.nasa.gov/mission/dragonfly/multimedia/ |
| Category | **Artist’s concept CGI animation** (NASA/Johns Hopkins APL). Matches spoken “Dragonfly, a flying robot.” |
| Local | `…/J1206/raw/Dragonfly-TakingOff-2024ver2.mp4` |
| SHA-256 | `1aed8dfbb0da2e19a3658ec0d6215d59f60f9b32bf480aa0e2ba177484b72ea1` |
| Dims / dur | **1920×1080**, 11.97 s; upscale to 1920h **1.778× PASS** |
| Motion | Present (craft/environment change across 0–2 s frames) |
| Gate risk | Artist’s concept → `picture_qa` **WARN**; still better subject match than blown disc from `PIA14925.jpg`. Not exempt from QA. Labelled CAD-style mission art, not a labelled textbook diagram. |

---

## D. Recommendations for Chief (no v03 until review)

1. **Uranus VO plan:** ACCEPT sentence-reorder **option 1** (S2 leads) on existing `vo_v02.wav` cuts above.  
2. **Uranus picture:** Shot4 Beauty Pass is the only acquired file with named planet + rings + real multi-frame camera motion + ≤2.35×. **Needs an explicit Chief call** on whether Conceptual Image Lab CGI is allowed under standing `picture_qa` (simulation/CGI FAIL risk).  
3. **Meteors:** **no qualifying source** this pass — do not build S5 v03 open.  
4. **Titan open:** PIA17656 has real flyover motion and PD rights, but **2.667×** vertical fill fails upscale unless Chief OKs blur-fill centre-band layout and accepts radar-reconstruction category.  
5. **Dragonfly:** TakingOff 2024 is a genuine subject match (artist CGI); use only if Chief accepts artist’s-concept WARN for that mid beat.  
6. **Still no v03** until Chief returns an edit/source plan. J1199 scheduled copies remain as written; no swap.

---

## E. Worker actions

- £0; no generation; no upload/privacy/Buffer/UPLOADS edits.  
- NAS scratch offload was already dry (nothing old enough); Mini free ~14 GB.  
- Report path: `jobs/reviews/J1206/SOURCE_FEASIBILITY_2026-10-29.md`.
