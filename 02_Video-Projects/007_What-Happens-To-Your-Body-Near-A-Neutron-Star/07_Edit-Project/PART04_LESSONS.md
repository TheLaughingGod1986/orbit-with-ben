# Neutron Star Part 04 — lessons

**In progress — v01 assembled 17 Aug 2026. Waiting for Ben UAT.** Do not start Part 05 plate gen until he passes this minute (or asks for a regen).

Chapter: **What You Would See** (first minute only). Full chapter VO was ~126s — split at the paragraph break after “storm of X-rays and charged particles” (~63.15s). Second half is queued as Part 05 VO only (fold / last image / horror and wonder). Do not gen Part 05 plates yet.

## Picture grammar (copy Part 02–03)

Teaspoon lock: named thing = the picture. Grey ball · bent light ray · visor · redshifted climb · leaning sky · galaxy arcs · photon crown · pulsar beam · X-ray storm. Zero Orbit+distant-remnant hangs. Music: continuous underscore.

Mute test: if you mute the VO, you should still follow the beat. Not Orbit + distant-star wallpaper.

**Grey-ball regen (Ben 17 Aug 2026):** first take looked like a broken-player icon (flat disc). Quarantined to `_rejected_grey_icon_v01/`. Regen as a shaded 3D sphere; skip first ~2.2s of that take (UV-split open). Same rough filename.

**Primitive-sprite regen (Ben 17 Aug 2026):** three plates were I2V of PIL placeholders — Omni copied the primitives.

| Rough time | Plate | Fail | Fix |
|---|---|---|---|
| ~0:22 | 04 redshifted-climb | Glowing orb + **flat orange 2D disc**, then a **melted left-limb bulge** from the halo | Clean single sphere, redshift on the crust, **no outer halo**. Halo/glow in the start frame becomes a bulge. Quarantined `_rejected_limb_bulge_v02/`. |
| ~0:31 | 05 sky-leans | Untextured **galaxy oval billboards** | Diagonal light streaks (falling sky). No ovals. |
| ~0:46 | 07 wrong-crown | White sphere **clipped by a vertical plane** | Photon ring + circular brightness bloom (no knife-edge wall). First 07 regen still copied a left/right split — quarantined `_rejected_clip_wall_v02/`. Second take: circular wall. |

Old takes: `_rejected_primitive_sprites_v01/`. Lesson: do not draw stacked ellipses / rectangle walls in start frames — Omni will ship them.

## Assets (v01)

| Asset | Path | Duration |
|---|---|---|
| VO | `02_Voiceover/parts/neutron_star_part-04_vo_v01.wav` | **63.15s** |
| Full chapter archive | `02_Voiceover/parts/neutron_star_see_chapter_full_vo_v01.wav` | (~126s) |
| Score | `05_Music/neutron_star_part04_score_bed_v01.mp3` | **70.03s** |
| Rough | `07_Edit-Project/parts/neutron_star_part-04_cursor_rough_v01.mp4` | **63.17s** |
| Open 15 | `07_Edit-Project/parts/neutron_star_part-04_cursor_open15_v01.mp4` | 15.00s |

## Plates

- **9 / 9** Omni Flash plates in `04_Generated-Clips/01_Raw/part-04/` — each **8.00s**.
- **Engine:** first pass all Flow (API 429). Regen 04 via Gemini API Omni; 05 + 07 via Flow. Daily Omni API quota still exhausted after that.
- Assemble: `_assemble_part04_cursor_v01.py` — xfade **0.40** + acrossfade. Plate 01 `-ss 2.20`. Picture **66.62s** > VO 63.15s — no freeze-pad.
- Offsets: 0.0 · 5.4 · 13.0 · **20.6** · **28.2** · 35.8 · **43.4** · 51.0 · 58.6
- Mix: continuous score ducked under VO; Omni SFX as quiet texture.

## UAT gate

Ben watches `neutron_star_part-04_cursor_rough_v01.mp4`. Pass / regen notes / mix notes. **Stop here.** Do not start Part 05 gens.
