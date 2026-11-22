# J3381 — three rebuilt v03 candidates for J3382

22 November 2026. Codex builder delivery, not a Chief approval. £0 spend, no image generation, no Studio writes. Round 2 titles remain parked. J3382 must inspect these exact final JPEGs and decide both creative acceptance and separate successor-test authorization before J3308–J3310 can proceed. No duplicate Studio jobs were created.

## Changes

- **T041 / Europa:** preserved `2× EARTH'S WATER`, the real PIA19048 terminator and all surface features. Europa's visible width is approximately 710 px instead of 327 px; the whole photographed silhouette fits below the text. Earth is a partial 1800 px diameter reference, still larger than Europa, with the original comparison direction retained. This is an apparent comparison, not an exact scale diagram. No invented cracks or arrow.
- **T042 / Light Speed:** preserved `EARTH AGES 7×`; replaced the distant S84-27018 crop with the much closer official NASA `s84-27017~orig.jpg` exposure (6852×6904). The complete suit/MMU silhouette is downsampled, not enlarged, and stays clear of every edge and the text. Dark space separates it from a partial Earth reference. Smooth travel streaks integrate redistributed photographic Hubble star-core pixels across 256 zoom exposures; no vector rays. This is an illustrative travel metaphor, not evidence that this astronaut flew at relativistic speed. NASA's archive API identifies McCandless's 7 February 1984 MMU EVA and NASA credit.
- **T043 / Last Star:** preserved `OUTLIVES OUR SUN` and the documented SDO solar-texture red-dwarf illustration. The whole red-star composition is now 530 px wide, with the stellar disk roughly 480 px; the pale Sun is a restrained partial 1500 px reference on the opposite side. The red hero is on the left, distinguishing the layout from Europa. This is a solar-texture proxy, not a resolved photograph of a red dwarf; colour, apparent size and brightness are editorial, not physical measurements.

Nebula contours are removed by selecting isolated photographic star cores rather than retaining the whole plate's high-pass residual. No scratch-like nebula edges remain in the final compositions. Final full-size JPEGs and actual 168×94 / 360×202 duration-badge sheets were viewed. The text remains readable and the hero silhouettes are unobscured at both sizes. Final light-speed streaks remain visible at 168 px. Subject widths exceed one third of the frame; this is a width/silhouette assessment, not a claim that opaque hero pixels occupy one third of total image area. J3382 retains the independent house-rule judgement.

## Verification

| Candidate | Saturation | Near black | Dimensions | JPEG bytes |
|---|---:|---:|---|---:|
| T041 | 132.7 | 14.5% | 1280×720 | 289363 |
| T042 | 146.7 | 22.3% | 1280×720 | 198141 |
| T043 | 167.7 | 12.3% | 1280×720 | 204117 |

All three pass the unmodified colour gate, dimensions and <2 MB checks. SHA-256 matches after NAS copy; exact candidate and preview hashes and paths are in DESIGN_MANIFEST.json. Existing v01/v02 files were hashed after delivery and remain untouched; the ledger is unchanged. No approval or running-test flag is set.

Exact source variant URLs are recorded: Europa and Mystic Mountain use `~medium.jpg`; Earth, the new EVA and solar source use `~orig.jpg`. The STScI public-domain release is retained. The builder refuses an existing output folder. To reproduce, download the five manifest sources under their recorded filenames and run the builder with `--sources <folder> --out <new folder>`. Pillow and numpy are required.

Internal disk headroom was below 20 GB; the prescribed safe offloader found no eligible scratch to move. All new work used the external scratch drive; final candidates and phone sheets are on the shared NAS. WW2 startup AGENTS.md was absent; no WW2 work was selected.
