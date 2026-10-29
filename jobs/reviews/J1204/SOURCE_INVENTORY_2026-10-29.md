# J1204 source inventory — S4 / S5 / S6 openings (29 Oct 2026)

Cursor worker, no spend. Acting Chief Codex FIX on J1199: v02 openings are JPEG-derived (synthetic bands/ring, Ken Burns, phase drift). This note records what exists on disk and what is missing before any v03 build.

## Verdict

**No v03 built.** Suitable *existing moving subject footage* for a 0–2.7 s opening was **not found** for S4 Uranus, S5 Shooting Stars, or S6 Titan. Per the brief: do not substitute pan/zoom/JPEG motion, synthetic ring/band motion, or altered gates; return inventory + precise missing input to Chief.

Rejected v02 masters and hashes are preserved (not rewritten):

| Short | YouTube id | v02 sha256 | UAT folder |
|---|---|---|---|
| S4 Uranus | `ZpEA8stoSPA` | `fd6bfec832bfa84d951c6e8ac2deff6c07ada71a9025e06deb2d8affc0b6f314` | `OWB UAT/standalone_shorts_uranus_v02` |
| S5 Shooting Stars | `T9fVlG3CCzU` | `bee058040b3d59445962b39d2d252f56201fc18901402cce43f7ff48fe9308bd` | `OWB UAT/standalone_shorts_s5_v02` |
| S6 Titan | `RLSJm59OSzI` | `be16daeb17284ea3d20148a1e6f8e3ea7ab6cdec64cf22e47f92b6167780b97d` | `OWB UAT/standalone_shorts_s6_v02` |

No upload / swap / schedule / privacy / Buffer / UPLOADS changes in this job. Scheduled copies remain as in J1199.

---

## Moving-footage pools inspected

### A. Standalone RAW (the pool Neptune/ISS used)

`/Volumes/data/mac-mini-archive/scratch/J0914/raw/`

| File | Subject | Usable for S4–S6 open? |
|---|---|---|
| `neptune_svs_vert.webm` | Neptune SVS 14397 | No — wrong subject |
| `neptune_rotating.webm` | Neptune | No |
| `neptune_dynamic.webm` | Neptune | No |
| `voyager_neptune.ogv` | Neptune | No |
| `iss_sunrise.ogv` | ISS sunrise | No |

**No Uranus, meteor, Titan, or Dragonfly video/webm/ogv in this RAW dir.** Scratch `find` to depth 3 under `/Volumes/data/mac-mini-archive/scratch` for `*uranus*`, `*meteor*`, `*titan*`, `*dragonfly*`, `*perseid*` video extensions returned nothing outside J1199's own rejected probe/render MP4s (those are JPEG assemblies, not source footage).

### B. J1199 Short plates (current assembly inputs)

`/Volumes/data/mac-mini-archive/scratch/J1199/plates/` — **all JPEG stills**.

#### S4 Uranus (`s4_uranus/`)

| File | sha256 | Kind | Motion if used as open |
|---|---|---|---|
| `PIA18182.jpg` | `3dcc83114f1a25caa1ae1a1436830fffaa15a3e429666dbf4c68bcf035e8932b` | Voyager still 1720² | Only via synthetic bands + drawn ring (v02 — rejected) |
| `webb_weic2310a.jpg` | `cbe6b51ce9d813f74c0406575f1ed01633459d26aca6e42179ead05bb41c9d8a` | Webb still 1268² | Push/pan only |
| `PIA00143.jpg` | `f01898cf2636fb81db534edad198af4031c81274db9e5289f1207d8a982d6cbe` | Voyager crescent | Push/pan only |
| `PIA00346.jpg` | `e01ab238b83014b428c01bfcf99179d6aee92c767275836a0e24602e1ccb664b` | Voyager crescent | Push/pan only |
| `PIA01391.jpg` | `9f97cd7b6b272186c75b389112bbfcee555988c5c0720b1138bc072583533b95` | Voyager crescent | Push/pan only |

**Proposed 0–2.7 s open from existing moving footage:** none. No candidate file/SHA/in–out.

#### S5 Meteors (`s5_meteors/`)

| File | sha256 | Kind | Motion if used as open |
|---|---|---|---|
| `NHQ202508030001.jpg` | `85239dae018ef7324f45c038f92231b973fdfe8d2f38a42b19df3eb01a2df964` | Bill Ingalls Perseid still | Ken Burns (v02 — rejected) |
| `NHQ202108110001.jpg` | `6b6eff56e863f06b8ecf8fe3a76bc1ada266df7ede5705c8043f2865b32888b2` | Perseid still | Push/pan |
| `NHQ202108110003.jpg` | `97974f8b3b21cd236b7e230d3a96c5d5f0cd1d2981e42af3bb33ffcff42b6f00` | Perseid still | Push/pan |
| `NHQ202108110005.jpg` | `45db2a397dad63cc67b70ab135c87054d19d53aee999b4a04a9a426a33deb143` | Perseid still | Push/pan |
| `NHQ202108100009.jpg` | `c683ed65b0acb84139210cff2a93127cbc27e12b114d24eac863a21e2222dd39` | Perseid still | Push/pan |

**Proposed 0–2.7 s open:** none (no meteor *video* on disk).

#### S6 Titan (`s6_titan/`)

| File | sha256 | Kind | Motion if used as open |
|---|---|---|---|
| `PIA14925.jpg` | `89408548e811b77f600a8fe7c782575ad8d2d6c0e1c2f42958219c7a4fe4bfb1` | Cassini still | Phase/translate (v02 — rejected) |
| `PIA06230.jpg` | `96c7c1f99bb609655014f9586428b20168c5e5825a5db98dedfceb598fb86942` | Cassini natural color | Push/pan |
| `PIA09739.jpg` | `9fad7a033372c4bbfc470f9e8a454d8b251ec5f258a228bf200218aa932a8845` | Titan hazes still | Push/pan |
| `PIA21625.jpg` | `6c3b171c6ea830a7ad81aa160ed923cdbf4dbe8788e07789d0e64f929d8132e0` | Cassini still | Push/pan |
| `PIA06997.jpg` | `cc22348696332f69dd9bcd0d4512ff2ab854447d1eb812a4ae23641672b2094f` | Haze silhouette | Push/pan |
| `PIA07232.jpg` | `4221ee7a4588a6ea169a0b438b5526e26c68827cb717a31ef1f81284b39cd3e8` | Huygens surface (often overscale) | Still |

**Proposed 0–2.7 s open:** none. **No Dragonfly moving plate** in the Short pool (v02 picture/word mismatch at ~9.5–12 s when VO says Dragonfly remains unresolved without new own footage).

### C. Film projects

- `032_What-Would-Happen-If-You-Landed-On-Titan/04_Generated-Clips`: **no mp4/mov/webm** on the Mini checkout; NAS folder for 032 not present under `mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/`.
- `021` Saturn: no Titan-named media hits in a shallow search.
- `052` Miranda: `04_Generated-Clips` is only `01_Raw` (no harvested Uranus planet video listed for this pass).

Approved v01/v02 Short masters exist under `06_Final-Exports/` and UAT; they are **outputs of JPEG motion**, not eligible source footage for a compliant open.

---

## S4 sentence-1 feasibility (no new VO)

Locked v02 spoken (Stay excised):  
`This planet has winters that last 21 years. Uranus is tipped 97 degrees…`

| Beat | Time (post–Stay map from trim words) | Note |
|---|---|---|
| Sentence 1 full | 0.10–3.40 s (3.30 s) | Ends **after** the ≤3 s first-cut cap |
| Surprise `21` | 2.26 s | Inside 0–3 s window, but subject is still unnamed |
| Name `Uranus` | first at **4.20 s** (start of sentence 2) | Outside sentence 1 |

**Infeasible** to get *named subject + surprise inside sentence 1* from complete existing sentence boundaries without new VO: sentence 1 says “This planet”, not “Uranus”; naming Uranus requires holding through sentence 2 (first cut would be ≫3 s) or rewriting VO (forbidden here).

---

## Precise missing inputs for Chief

To build compliant v03 openings under the J1199/J1204 rules, Chief must authorize **acquisition (no spend if public-domain download)** of genuine moving footage, then a follow-up assembly job:

1. **S4 Uranus** — NASA SVS (or equivalent public-domain) **moving** Uranus sequence with visible subject motion in camera (cloud/rotation/ring geometry in the source), ≥~4 s usable, vertical or crop-safe for 9:16 at ≤2.35×. Same role as Neptune’s `neptune_svs_vert.webm` (SVS 14397). Optional: rings-upright moving plate if script frame-0 still requires it.
2. **S5 Shooting Stars** — real **meteor video** (not a still long-exposure JPEG), mid-streak usable at frame 0, ≥~3 s, night-sky landscape OK.
3. **S6 Titan** — Cassini (or Huygens) **moving** haze/surface sequence for 0–2.7 s; plus a separate **Dragonfly** clip or approved still *only if Chief relaxes “moving footage” for that mid-film beat* — currently VO names Dragonfly over a blown disc from still plates.

Until those land on disk (paths + SHA-256 recorded like J0914 RAW), **do not** mint v03.

## Worker action taken

- Inventory only; £0; no render; no YouTube/Buffer change.
- Park J1204 for Chief with this path: `jobs/reviews/J1204/SOURCE_INVENTORY_2026-10-29.md`.
