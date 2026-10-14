# Venus 023 — NASA pool v01 (harvest)

Pulled 4 Oct 2026 London after Claude PASS 5982425011. Binaries gitignored under `nasa_pool_v01/`.

## Have (local)

| Section | Assets |
|---|---|
| open | PIA00254, PIA00106, PIA00240, PIA00241, PIA00087, PIA23791, PIA00104 |
| magellan_extra | PIA00215 (pancakes), PIA00246 (Alpha 3D / flyover frame), PIA00093 (Ishtar), PIA00103, PIA00200, PIA00084, PIA00159 |
| sdo | AIA171VenusTransit_HD1080.mp4, HMIVenusTransit_HD1080.mp4, stand still (SVS 3941) — **mute in edit** |
| parker | PIA24470, PIA24937, PIA23122, PIA23123 (copied from 022 Wed21 cache) |
| earth | as17-148-22727 Blue Marble, PIA18033 Blue Marble 8k, GSFC archive still |
| sky | PIA00104 / PIA00254 copies for twilight-context globe |

## Still open

| Item | Status |
|---|---|
| Magellan flyover **video** (full movie) | Not found as free MP4 this pass; use **PIA00246** frame + PIA00254 push for frame 0 |
| ESA Venus Express stills | Need ESA portal pull + credit **ESA** (not NASA images-assets) |
| NASA EO/ISS White Cliffs or coral reef | EO page URLs JS/403 this pass; row 24 uses Blue Marble / ocean until cliffs land |
| Venus twilight sky photo (NASA HQ) | images-assets 403 on NHQ candidate; globe stills as interim for #56 |
| Pioneer / DAVINCI / VERITAS / EnVision art | Harvest IDs at edit pull |

## Harvest v02 (8 Oct 2026, Cursor covering, J0003): gaps for chapters 2–5

From `images-api.nasa.gov` originals into `nasa_pool_v01/harvest_v02/` (gitignored; `SHA256.txt` beside them). Contact sheet: `_evidence/venus_harvest_v02_sheet.jpg`.

| Row | Pick | Size | Credit | Note |
|---|---|---|---|---|
| 30b | **ARC-1978-AC78-9245** Pioneer Venus multiprobe art (Paul Hudson) | 3072×2048 | NASA/Ames | Probes over Venus on black. Crop off the grey side bars and white right edge. |
| 30b alt | ARC-1978-AC78-0238 multiprobe art (Rick Guidice) | 3072×2048 | NASA/Ames | Purple painted backdrop; second choice. |
| 24 | **s129e007324** Eleuthera, Bahamas, from Atlantis (STS-129) | 4288×2929 | NASA/JSC | Carbonate island and shallows: limestone/seabed beat. Crop the ID strip at the bottom. |
| 24 alt | PIA03877 Tarpum Bay carbonate sand dunes (ASTER) | 2720×1670 | NASA/JPL | False colour; second choice. |
| 56 | **NHQ202605180003** Moon and Venus conjunction over Washington, 18 May 2026 | 5420×7900 portrait | NASA/Bill Ingalls | Crop a 16:9 band of twilight sky with the Moon and Venus; keep the monument out or at the very bottom edge. |
| 56 rejected | NHQ202605180002 | 6968×4536 | — | NASA logo fills the frame (no logos in plates). |

Still open (closed by harvest v03 below): **DAVINCI / VERITAS / EnVision art** (rows 52–53): the NASA library only has VADIX and Iceland field-test photos, no mission art. **ESA Venus Express** (row 28) needs the ESA portal. Row 25 ocean: Blue Marble / GSFC still in `earth/`. White Cliffs of Dover: no NASA EO/ISS hit, so row 24 takes Eleuthera.

## Harvest v03 (8 Oct 2026, Cursor covering, J0003): rows 28, 52, 53 per Claude #99 6049035232

Into `nasa_pool_v01/harvest_v03/` (gitignored; `SHA256.txt` beside them). Contact sheet: `_evidence/venus_harvest_v03_sheet.jpg` (top row and bottom-left: row 52 span at +0/3/6/9.5 s; then VERITAS, S91-50688, PIA00478).

| Row | Pick | Size | Credit | Note |
|---|---|---|---|---|
| 52 | **SVS 13887** "DAVINCI Probe's Eye View", span **89.0–99.2 s** → `13887_DAVINCI_row52_89.0-99.2s.mp4` (10.2 s, muted) | 1920×1080 | NASA's Goddard Space Flight Center / CI Lab | Probe descending over ridged highlands to the surface. No on-screen text in the span: the burned-in cards sit at ~4 s (title), 48–52 s and 68 s (thought bubbles), 60 s ("SNAP!") and 87 s ("CRASH!"), so don't slide the in-point earlier than 88.8 s. Full clip kept beside it. Alt span 10–24 s (approach, cloud entry, parachute), also text-free. SVS 14735 (vertical) not used. |
| 53 | **VERITAS artist's concept** (spacecraft radar-mapping Venus), `veritas-cut7-16.jpg` from nasa.gov mirror of JPL's "VERITAS: Exploring the Deep Truths of Venus" (jpl.nasa.gov returns 403 to scripts) | 1600×900 | NASA/JPL-Caltech | At Claude's ~1600 px floor, so no PIA00246 fallback; 1.2× to 1080p plus 5% push. EnVision left to the VO. |
| 28 | **S91-50688** Magellan global centred at 270° E (gaps filled with Pioneer Venus Orbiter data) | 6000×6000 | NASA/JPL | No Pioneer Venus Orbiter UV cloud image on images.nasa.gov (searched "pioneer venus ultraviolet/clouds/orbiter", "venus ultraviolet"), so Claude's Magellan fallback. The cut's other globes (PIA00104, PIA00159) are both the 180° face; this is the 270° face. Small dark data-gap notch at the bottom edge: frame or crop it out. |
| 28 rejected | PIA00478 Magellan global at 180° E | 10240×10240 | — | Same face as PIA00104/PIA00159 and a lat/long grid is burned in. |

## Credits

NASA/JPL (Magellan, Mariner, Parker family as labeled). SDO transit: NASA/SDO/SVS. Mute any transit audio.
