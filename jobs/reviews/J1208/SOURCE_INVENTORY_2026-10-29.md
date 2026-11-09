# J1208 — S5 meteor + S6 Titan opening source inventory (29 Oct 2026)

Cursor worker (`assembly`), no spend, no v03 render, no YouTube/Buffer/UPLOADS/privacy changes.

Acting Chief Codex source-plan ruling: `jobs/reviews/J1204/SOURCE_PLAN_RULING_2026-10-29.md` (PR #348). This pass resolves **only** missing S5/S6 opening inputs for J1199. Previously rejected sources (Geminid-v05 constellation diagram; PIA17656 radar reconstruction) were **not** re-proposed.

Machine evidence (not in git):

- `/Volumes/data/mac-mini-archive/scratch/J1208/raw/`
- `/Volumes/data/mac-mini-archive/scratch/J1208/frames/`
- `/Volumes/data/mac-mini-archive/scratch/J1208/CANDIDATES.json`

---

## Searches performed (bounded)

| Pool / query | Result |
|---|---|
| NASA All-Sky Fireball Network (`fireballs.ndc.nasa.gov`, days 20261010–20261018) | Real camera `.mp4` event clips downloaded (12+). Native **640×480**, UTC+station text burned in. |
| NASA SVS 11231 *It's Fireball Season* | `FireBall04-540-MASTER_high.mp4`, `AllSky-540-MASTER_high.mp4` (960×540). Produced package with `science @ NASA` watermark / reticles. |
| NASA SVS 11943 *Space Station View Of Meteor* | **Primary S5 candidate** (see below). |
| NASA images API Perseid/Ingalls video | 0 video hits this run. |
| PIA07234 *Descent Through Clouds to Surface* | Optical DISR sequence but **233×400** + altitude text overlays. |
| PIA08117 / SVS 11323 / ESA 2308_017 DISR descent movies | Sequential DISR mosaics, but **dashboard/sidebars/panels** throughout. HiRes only **800×608**. |
| PIA17656 | Not re-acquired (Chief reject stands). |
| Archive (J0914/J1199/J1206) | No new eligible Titan/meteor opens beyond prior rejects. |

Rights baseline: NASA media generally reusable for commercial YouTube under NASA Media Usage Guidelines (US government work / NASA SVS). Fireball Network: NASA blog states images and video “available for anyone to download.” ESA DISR: credit ESA/NASA/JPL/University of Arizona (ESA multimedia licence — commercial YouTube may need separate check; **not** proposed as primary while panels fail anyway). No licences bought.

---

## S5 — Shooting Stars

### Primary candidate (recommend for Chief source OK)

| Field | Value |
|---|---|
| Title | NASA On Air: Space Station View Of Meteor |
| Page | https://svs.gsfc.nasa.gov/11943/ |
| Category | **Real ISS camera footage** of a meteor below the station (NASA produced package). Not a constellation diagram; not a JPEG push. |
| Local | `…/J1208/raw/WC_Space_Station_Meteor10.m4v` |
| SHA-256 | `7c11f360fd17023be709c316f9c0ddb2e2a1f88b059d8635e431e18fb68810b3` |
| Dims / dur | **1920×1080**, 14.781 s, h264 |
| Proposed in/out | **4.00–6.70 s** (2.70 s). Package opens on a ground night plate 0–~4 s; ISS limb+meteor starts at 4.0 s. |
| Motion | Continuous: mean abs frame-diff ~3.0–4.4 per 0.2 s across 4.0–6.7; bright pixel count falls as the streak fades. Frames: `frames/WC_Space_Station_Meteor10_open_t*.jpg`. |
| Logos/panels | Corner strip check: top corners near-black (mean ~2–4); **no** burned-in lower-third or NASA meatball in the open window. |
| 16:9 centre-band fit | Scale to 1080-wide band = **0.562×** (downscale) → **PASS** ≤2.35×. Feathered blur fill above/below allowed by ruling. |
| Alternate 9:16 centre crop | crop_w ≈ 607.5 from 1080h → scale **1.778×** → **PASS**. Meteor sits on the right; keep craft/streak inside crop. |
| Gate risk | `picture_qa` should treat as real footage (not CGI). Confirm no news lower-third if a longer trim is used; proposed window is clean. |

### Secondary / rejected this pass

| Candidate | Verdict |
|---|---|
| SVS 11231 `FireBall04` **26.0–28.7 s** | Real fireball streak motion (MAD huge on cut-in). **Reject as primary** while `science @ NASA` watermark is on the 16:9 master (logos forbidden). 960×540 centre-band **1.125× PASS**. |
| SVS 11231 `AllSky` | All-sky camera footage but **tracking reticle** overlays. |
| `fireballs.ndc.nasa.gov` event mp4s (e.g. `ev_20261012_054757A_03A`) | Genuine MEO cameras, reusable, centre-band **1.688× PASS**, but **timestamp + station text** burned in; sampled opens did not show an unmistakable streak at frame 0 (fisheye + noise). Hold as backup only if Chief accepts overlays or a crop that removes them. |
| SVS 20271 Geminid-v05 | Already rejected (constellation diagram). Not re-proposed. |

**S5 missing input if Chief rejects ISS window:** a logo-free, overlay-free ground fireball video ≥~460 px wide (centre-band ≤2.35×) with streak at the open’s frame 0. Network AVI/MP4s exist but carry burned-in text.

---

## S6 — Titan opening

### No qualifying clean opening found

| Candidate | Why it fails |
|---|---|
| PIA17656 radar flyover | Chief reject stands (reconstruction, swath artifacts, 2.667× full-height). Not re-proposed. |
| PIA07234 Descent Through Clouds | Real DISR optical frames, but **altitude/frame-number overlays** + native **233×400** → centre-band scale **4.635× FAIL**; full-height **4.8× FAIL**. |
| PIA08117 HiRes / SVS 11323 TitanDISR / ESA `2308_017_AR_EN` | Optical DISR mosaics with **dashboard, sidebars, compass, telemetry panels**. HiRes only **800×608** (centre-band 1.35× would PASS scale, but panels fail the no-panels rule). |
| KSC Titan packages (prior J1206) | 320×212 — unusable. |
| Dragonfly TakingOff 2024 | **Already Chief-approved for mid-film Dragonfly line only**; does **not** satisfy the opening. |

**Precise missing input:** a **clean** (no altitude call-outs, no DISR dashboard) **optical** moving Titan sequence — Huygens DISR or Cassini ISS camera — with native width ≥~460 px for 16:9 centre-band ≤2.35×, and recognizable Titan subject motion from the open’s frame 0. Not radar reconstruction; not still-pan; not annotated telemetry movie.

No v03 for S6 until Chief accepts a substitute plan or a new source appears.

---

## Recommendations for Chief (source decision only)

1. **S5:** ACCEPT SVS 11943 `WC_Space_Station_Meteor10.m4v` **4.00–6.70 s** as the opening plate (16:9 centre-band + blur fill), credit NASA SVS in the description; no credit overlay on the Short.  
2. **S6:** HOLD opening — report blocker above. Do not render a substitute. Keep scheduled copy airing path unchanged absent PASS/OK.  
3. **Dragonfly mid beat:** unchanged — TakingOff 2024 remains the mid-film candidate from the prior ruling.  
4. **Still no S5/S6 v03** until Chief returns a source/edit OK. Assembly deadline remains 5 Nov 12:00Z.

---

## Worker actions

- £0; no generation; no upload/privacy/Buffer/UPLOADS edits; no overwrite of v02 masters.  
- Mini free ~14 GB; NAS scratch used for all media.  
- Return path: this file + NAS `CANDIDATES.json` + open frame stills.
