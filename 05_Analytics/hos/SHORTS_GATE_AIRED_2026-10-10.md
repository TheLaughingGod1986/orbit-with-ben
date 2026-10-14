# HOS aired Shorts: open gate + title vs subject (J0087, Cursor, 10 Oct 2026)

Read-only. Nothing spent, nothing changed on YouTube.

- **Files:** the exact files uploaded, from the NAS (`mac-mini-archive/YouTube/History Of Science/02_Video-Projects/00{1,2,3}_…/10_Shorts/`). File names were matched to ids from Studio "Filename" captures (002, 003) and `_Buffer-Backlog/HOS_BUFFER_BACKLOG_PACK_v01.md` (001).
- **Gate:** `gate_shorts_open.py check <mp4> --air-date <aired> --id <id>`.
- **Stats:** views, average viewed and feed share are from `05_Analytics/hos/REPORT.md` (snapshot 10 Oct).

## Gate result per Short

| Aired | Id | Title | File | Gate | What failed or warned | Feed share day 1 | Avg viewed (28 d) | Views |
|---|---|---|---|---|---|---:|---:|---:|
| 6 Sep | `H1y0DXFVmw8` | Germs don't cast a shadow | hos_001_s01_shadow_punch_v02 | PASS | – | 76% | – | 78 |
| 6 Sep | `iqToagXnjX0` | Microbes in a drop of pond water | hos_001_s02_pond_punch_v02 | PASS | WARN: little motion in first second (9.1 < 10) | 16% | 89% | 110 |
| 6 Sep | `8_Edn_HCi1s` | Germs hitch a ride on you | hos_001_s03_vector_punch_v02 | FAIL* | Orbit detector 0.0048 (false positive: dark frock coat) | 77% | 33% | 27 |
| 6 Sep | `sILtQxgYQk8` | A flask that proved germs come from outside | hos_001_s04_flask_punch_v02 | FAIL* | Orbit detector 0.0067 (false positive: glass flask) | 11% | 102% | 24 |
| 6 Sep | `93fPUG-hW0A` | Invisible life is still everywhere | hos_001_s05_soap_punch_v03 | **FAIL** | **Silent: −91 dB for the whole file. The public YouTube copy is also −91 dB (checked with yt-dlp today).** | 0% | – | 6 |
| 18 Sep | `uU12JA5rMWg` | The periodic table's empty chairs | hos_002_s01_empty_chairs_punch_pill_v01 | PASS | – | 8% | 59% | 28 |
| 19 Sep | `nFQRWmpulTQ` | He predicted a metal before it was found | hos_002_s02_predict_metal_punch_pill_v01 | PASS | – | 10% | 53% | 33 |
| 20 Sep | `CnHwX1L9XHg` | Gallium sat where the table said | hos_002_s03_gallium_punch_pill_v01 | PASS | – | 53% | 33% | 16 |
| 21 Sep | `nba0-f7PPeU` | Why tellurium sat before iodine | hos_002_s04_tellurium_punch_pill_v01 | FAIL* | Orbit detector 0.0030 (false positive: wooden chairs); WARN: almost still first second (4.2 < 10) | 38% | 46% | 28 |
| 22 Sep | `LanTHJckYx8` | What other table has empty chairs? | hos_002_s05_other_table_punch_pill_v01 | PASS | – | 33% | 23% | 4 |
| 25 Sep | `oowAOWTBoq0` | How X-rays Were Discovered by Accident | hos_003_s1_cardboard_glow_v01 | PASS | – | 50% | 67% | 27 |
| 26 Sep | `xvanpsLeADE` | How did Röntgen see bones without cutting | hos_003_s2_bones_no_knife_v01 | PASS | – | 23% | 52% | 38 |
| 27 Sep | `zI_eD3vFWmE` | The first X-ray showed a wedding ring | hos_003_s3_bertha_ring_v01 | PASS | – | 0% | 32% | 8 |

\* The Orbit check is tuned for Orbit's orange body and black visor. HOS has no Orbit; I looked at all three opening sheets and none shows a robot. So these three are a detector false positive on HOS picture, not a real fail. For HOS the gate's real checks are duration, sound, motion and frame-0 reuse.

**Other checks:** all 13 are 23.9–25.3 s (inside 22–27). None of the 13 opening frames is within 16 dHash bits of another (no reused open). The gate's reuse library holds only Orbit Shorts, so the HOS-to-HOS comparison was done separately from the gate's dHash values.

**What the gate does and doesn't explain:** apart from the silent file, the gate doesn't separate fed from not-fed. PASS Shorts range from 0% to 76% feed share. Most views on every Short are small (4–110), so day-1 feed share is noisy here. The two Shorts with 50% or more that pass cleanly (`H1y0DXFVmw8` 76%, `oowAOWTBoq0` 50%) both name the subject in the title.

## Title vs subject

| Id | Title | What it's about | Names the subject? | Names the discovery? |
|---|---|---|---|---|
| `H1y0DXFVmw8` | Germs don't cast a shadow | Doctors blamed bad air, not living germs | Yes (germs) | No (metaphor) |
| `iqToagXnjX0` | Microbes in a drop of pond water | Leeuwenhoek first seeing microbes | Yes (microbes) | Partly (no person, no "first") |
| `8_Edn_HCi1s` | Germs hitch a ride on you | Semmelweis: doctors' hands carried infection; handwashing | Yes (germs) | No (no Semmelweis, no handwashing) |
| `93fPUG-hW0A` | Invisible life is still everywhere | Lister's carbolic spray and soap | **No** (abstract) | **No** |
| `sILtQxgYQk8` | A flask that proved germs come from outside | Pasteur's swan-neck flask | Yes (flask, germs) | Yes (no Pasteur) |
| `uU12JA5rMWg` | The periodic table's empty chairs | Mendeleev left gaps for unknown elements | Yes (periodic table) | Metaphor ("empty chairs" = gaps) |
| `nFQRWmpulTQ` | He predicted a metal before it was found | Mendeleev predicting gallium (eka-aluminium) | **No** ("He", "a metal") | Yes (prediction) |
| `CnHwX1L9XHg` | Gallium sat where the table said | Gallium's discovery matched the prediction | Yes (gallium) | Partly ("the table") |
| `nba0-f7PPeU` | Why tellurium sat before iodine | Mendeleev ordering by properties over atomic weight | Yes (tellurium, iodine) | No (no "periodic table", no Mendeleev) |
| `LanTHJckYx8` | What other table has empty chairs? | Closing tease for the 002 periodic table film | **No** (abstract question) | **No** |
| `oowAOWTBoq0` | How X-rays Were Discovered by Accident | Röntgen's glowing screen | Yes (X-rays) | Yes (by accident) |
| `xvanpsLeADE` | How did Röntgen see bones without cutting | First X-ray look inside a living body | Partly (Röntgen; no "X-ray") | Yes |
| `zI_eD3vFWmE` | The first X-ray showed a wedding ring | Bertha Röntgen's hand | Yes (X-ray) | Yes |

The three titles that hide the subject (`93fPUG-hW0A`, `nFQRWmpulTQ`, `LanTHJckYx8`) took 6, 33 and 4 views. Two of them are the lowest on the channel.

## For Claude

1. **`93fPUG-hW0A` is a public silent Short** (a Never-list item: "Ship a silent or near-silent file"). v01 of the same Short has sound (−25.9 dB). v02 and v03 are silent, and v03 went up. Making it private is Claude's call (Ben's 5 Oct exception). I changed nothing on YouTube.
2. **The gate's Orbit check misfires on HOS picture** (3 of 13 false FAILs). If HOS Shorts adopt this gate, it needs a no-Orbit mode (for example `--channel hos` to skip check 3) and an HOS reuse library.
