# Neutron Star Part 01 — Cursor build (17 Aug 2026 ~01:35 BST)

**STOP.** Part 01 only. No Part 02. No YouTube. No Auditor send.

Folder: `/Users/ben/code/Orbit-YouTube/02_Video-Projects/007_What-Happens-To-Your-Body-Near-A-Neutron-Star/`  
Not the empty scaffold `007_Neutron-Star/`.

## What shipped

| Asset | Path | Duration (ffprobe) |
|-------|------|--------------------|
| Part 01 rough | `07_Edit-Project/parts/neutron_star_part-01_cursor_rough_v01.mp4` | **70.833008s** |
| Open 15s | `07_Edit-Project/parts/neutron_star_part-01_cursor_open15_v01.mp4` | **15.000000s** |
| VO (reused leftover) | `02_Voiceover/parts/neutron_star_part-01_vo_v01.wav` (+ `.mp3`) | **70.800000s** |
| Plates JSON | `07_Edit-Project/parts/part-01_omni_plates_cursor_v01.json` | 10 prompts |
| Gen report | `07_Edit-Project/parts/part-01_omni_gen_report_cursor_v01.json` | 10/10 ok |
| QC stills | `_qc_p01_cursor/qc_t00_5.jpg` · `qc_t02_5.jpg` · `qc_t08.jpg` · `qc_t15.jpg` · `qc_t_last2s.jpg` | — |

Voice: leftover **Ben Orbit Narrator** `kDch6ACCIpqgQ0NsU9kk` · `eleven_v3` · exact master lines 3–24. **Not regenerated.** STT already matched. 70.80s inside 60–80s.

## Leftover VO reuse

Reused. Verified:
- Text file = locked spoken lines (cold open + first rise of “The Corpse of a Star”).
- STT matches those lines (punctuation only).
- Duration 70.80s.
- Same voice lock as `04_Audio/tools/orbit_voice.py`.

Leftover files were **not** renamed as the official cut.

## Picture-first open

| t | Frame | Orbit? | Logo/title? |
|---|-------|--------|-------------|
| 0.5s | `_qc_p01_cursor/qc_t00_5.jpg` | **No** — strange compact star only | No |
| 2.5s | `_qc_p01_cursor/qc_t02_5.jpg` | **No** | No |
| 8.0s | `_qc_p01_cursor/qc_t08.jpg` | **Entering** from frame left, in-scene | No |
| 15s | `_qc_p01_cursor/qc_t15.jpg` | Yes — cream/yellow eyes + pupils, one underside glow | No readable HUD/text |
| last 2s | `_qc_p01_cursor/qc_t_last2s.jpg` | Yes — facing remnant, energy up | No |

VO starts at 0s over plate 01. No brand sting. No baked like/subscribe. No `/go/`.

**Open QC: PASS.**

## Plates (Omni Flash via Flow Ultra)

Engine: Google Flow · **Omni Flash** · 8s · 16:9 · profile `~/code/youtube/.playwright-aistudio-profile` (ULTRA).  
**x1 locked** on the Video chip (`Video · 8s crop_16_9 x1`) for every submit. One 8s file downloaded per prompt.  
10/10 unique SHA256. All 8.000s. No freeze-pad.

| # | File | Orbit | VO idea |
|---|------|-------|---------|
| 01 | `omni_p01_01_almost-ordinary-star_cursor_v01.mp4` | no | almost-ordinary star |
| 02 | `omni_p01_02_orbit-banks-into-frame_cursor_v01.mp4` | yes | tiny orange figure |
| 03 | `omni_p01_03_tide-tears-a-line_cursor_v01.mp4` | yes | tear into a line of atoms |
| 04 | `omni_p01_04_light-bends-into-a-ring_cursor_v01.mp4` | yes | light bend into a ring |
| 05 | `omni_p01_05_second-by-second-close_cursor_v01.mp4` | yes | second by second / distance closes |
| 06 | `omni_p01_06_see-feel-you-ends_cursor_v01.mp4` | yes | see / feel / you stops |
| 07 | `omni_p01_07_it-began-as-a-giant_cursor_v01.mp4` | yes | began as a giant / supernova |
| 08 | `omni_p01_08_argument-gravity-almost-won_cursor_v01.mp4` | yes | not ash / gravity almost won |
| 09 | `omni_p01_09_compact-fierce-wrong_cursor_v01.mp4` | yes | rise hold |
| 10 | `omni_p01_10_remnant-intensity-rise_cursor_v01.mp4` | yes | rise hold 2 (covers VO tail) |

Join: **xfade 0.40s + acrossfade**. Picture 76.42s ≥ VO 70.80s. Omni SFX under VO at 0.20. 10 plates so 0.40s joins still cover VO (9 plates would have been short).

## Leftover UAT issues

1. **Plate 03 flames — FIXED in this cut.** Prompt rewritten: underside glow only, no flames / twin thrusters / jets. Stills `plate_omni_p01_03_*_t1/t4/t7.jpg` show one bottom glow + tidal field lines, no twin fire plumes (leftover v01 t4 had blue/white exhaust flames).
2. **~15s body lettering — not visible** on `qc_t15.jpg`. No readable HUD/text on Orbit in the open stills. Soft panel lines only.
3. **Flow x1 — FIXED.** Leftover JS click never opened the popover (quantity is a tablist). Playwright mouse-click on the Video chip + `get_by_role("tab", name="x1")` locked `Video · 8s crop_16_9 x1` on all 10 submits.
4. **Picture-first 3s — PASS.** No Orbit/logo/title in first 3s. Orbit after ~8s, in-scene.

Still present (same leftover warning, not a ship-blocker for this minute):
- Agent Instructions field still missing in Flow. Identity attached via `orbit-seedance-reference-16x9-v01.png` on every Orbit plate.

## Not done (correct)

- No YouTube upload
- No Part 02
- Leftover `*_v01.mp4` / leftover VO filenames left as reference only
