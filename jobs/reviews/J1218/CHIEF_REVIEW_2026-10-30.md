# J1218 HOS 008 rough v03: acting Chief (Claude) graphics review, 30 Oct 2026 04:xx UTC

**FIX on 4 graphics. 6 graphics pass as drawn. Overlay composites and the 6 WARN plates are not yet judged. No finished-film PASS, no Ben watch.**

## What I looked at, and its limits

Claude runs in the cloud and cannot open the master, the NAS or UAT. I re-rendered every row of `code_graphics_v02` here, using `_build_code_graphics_v02.py` from HOS PR #379 at e05f343 (PICTURE_PLAN_v03 and the part-02..05 v03 boards from the same commit).

- Five frames per row at 8, 30, 50, 70 and 92% of `use_s`: `cg_v02_strips/*.jpg`, made by `render_cg_strips.py`.
- The font is DejaVu Serif Bold instead of Didot (Didot isn't on Linux). That changes the label face only, not the timing or the drawing.
- Overlay rows are shown on a flat grey stand-in, not on their moving plate. So this review judges what each graphic draws and when. It does not judge how each one sits on its plate.

## Per row

| Row | Ruling | Why / what to change |
|---|---|---|
| P2:14 likeness_pairs | PASS (graphic) | Jar spark beside the cloud, crooked blue traces arrive on the second sentence. Reads. |
| P2:15 likeness_fire | FIX | No crack is ever drawn. "Fire" is a flame shape that reads as a pen nib. "Could kill animals" is one thin line. Draw a visible crack (jagged split) on "crack", a real flicker flame on "fire", and a small animal silhouette knocked over, or a clear shock spark, on "kill animals". Time each beat to the locked word records. |
| P3:03 rod_cloud | FIX | The "rod" is a hollow tall rectangle that reads as a chimney or tower. The charge dots run cloud to roof apex, not to a rod tip. The VO says the rod should pull sparks. Draw a thin pointed iron rod on the roof, run the dot stream cloud to rod tip, and add a small spark at the tip on "pull sparks". |
| P3:04 letter_crosses | FIX | The geography is still not recognisable: two bare wiggly lines and a small outline, no land fill, no place names. J1193 required recognisable geography. Use simple filled landmasses (North America east coast; Britain/Ireland plus a France/Europe edge), small place labels PHILADELPHIA and PARIS at the two dots, and the dotted route on "crossed the ocean". Illustrative only: no voyage or packet claim (source correction stands). |
| P3:15 wet_dry | FIX | Rain, twine, key and hand are there, but nothing shows the difference the line is about. Make the wet twine one colour with charge dots flowing down it, the dry silk ribbon at the hand a clearly different colour, and the dots stopping at the silk ("but dry silk would not"). |
| P4:06 same_thing | PASS (graphic), composite unjudged | Jar spark and cloud bolt share one drawing. ELECTRICITY appears at about 5.1 s, matching the locked +5.14 s. One label. |
| P4:08 teach_charge | PASS (graphic) | Kite, string, key, no bolt drawn. Label fits the negative claim. |
| P5:08 looking_path | PASS (graphic), composite unjudged | Branching path now runs only downward (the J1193 upward segment is fixed). |
| P5:09 wood_vs_metal | PASS (graphic) | Bolt hits the wooden roof, flame follows. Cracks open in the stone steeple. Both beats readable. |
| P5:10 metal_easy | Composite unjudged | On its own it is a column of small rings filling in. It only works if the column sits exactly on the rod in KEEP `06_rod_fitting`. Bring composite frames to prove it. |
| P5:11 safe_path | PASS (KEEP) | SAFE PATH DOWN (3 words), path runs roof, rod, outside wall, ground. |

## Next (J1241)

1. Rebuild P2:15, P3:03, P3:04 and P3:15 as `code_graphics_v03` (new version, never overwrite v02). Same locked VO and timings, £0.
2. Composite evidence from rough v03 (and from v04 for the rebuilt rows): full-size frames at 25/50/75% of each overlay row (P2:15, P3:04, P4:06, P5:08, P5:10), and at the 6 picture_qa WARN times (1:19, 4:28, 4:51, 5:46, 6:58, 8:31), committed to the HOS PR.
3. Diagnostic rough v04 with v03 graphics, same gates, then park for Chief.

Music/SFX finishing stays outstanding. No Ben watch, no upload, no spend.
