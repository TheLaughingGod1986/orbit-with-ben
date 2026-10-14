# Remake v01 (4 Oct 2026): sources and build
All plates are NASA public-domain imagery or the channel's existing approved plate. No AI or paid generation. Composited with PIL (`owb.py`, `build_*.py`). Text is Arial Black, the house font, with a yellow hook word.

| Thumb | Sources |
|---|---|
| jupiter_A | PIA02873 (Cassini, Jupiter globe) + ARC-1989-AC89-0146-1 (NASA Ames, Galileo probe entry art). Both from images.nasa.gov |
| jupiter_B | ARC-1995-ACD95-0126 (NASA Ames, Galileo probe descent painting by Don Davis). From images.nasa.gov |
| saturn_A / saturn_B | PIA06193 (Cassini; already in repo as PIA06193_orig.jpg) + AS17-148-22727 (Apollo 17 Blue Marble, Earth to scale ≈ 1/9.45 Saturn's diameter). A's ring-rain streaks are code-drawn |
| saturn_short_A | PIA21439 (Cassini Grand Finale dive illustration; the repo had a 9x16 cut, the original came from images.nasa.gov) |
| saturn_short_B | PIA06193 |
| blackdwarf_A | PIA18164 Helix Nebula (repo `_nasa_stills`) |
| blackdwarf_B | `_work_v02_stills/sphere_base.png` (existing approved cover plate) + SDO AIA GSFC_20171208_Archive_e002035, recoloured warm. Sun limb is for context only, NOT to scale |

Line heights: longs cap ≈ 82 px = 11.4% of 720. Shorts cap 95 px ≈ 15.6% of the 16:9 centre crop and 4.9% of 1920; the stack spans ≥60% of the width (rule 4.2).

## Robot Short buaOI3QGm7U "Could a Robot Survive Falling Into Jupiter?" (14 Oct 11:30 BST), cover v01, 4 Oct
- Pick B: robot_short_cover_v01.jpg (= robot_short_B.jpg), 1080x1920, plus _16x9. IT LASTED / 58 MINUTES (58 MINUTES yellow). Cassini PIA02873 Jupiter globe + code-drawn Galileo probe/parachute silhouette (traced from NASA Ames ACD95-0126, same as Jupiter long v02).
- Alt A: robot_short_A.jpg. 58 MINUTES / THEN SILENCE. Galileo descent painting NASA Ames ACD95-0126 (Don Davis).
- Text fitted to <=80% width (864px) and placed inside the 16:9 centre band (y 656-1263). Fact: Galileo probe transmitted ~58 min (01_JUPITER.md).
- Builder: build_robot_short.py. Review: REVIEW_robot_short.png. Not set on YouTube.

## LIVE picks (4 Oct afternoon remake / text)

| Video | File in this folder | Text | Art pick |
|---|---|---|---|
| Jupiter long `-jmMROGoZCM` | `jupiter_v02_final.jpg` | NO FLOOR (FLOOR yellow) | jupiter A v02 |
| Saturn long `55AEQwvs36g` | `saturn_long_55AEQwvs36g.jpg` | (from saturn_B_v02) | saturn B v02 |
| Saturn Short `Qn56D6TOi0k` | `saturn_short_Qn56D6TOi0k.jpg` (+ `_16x9`) | **RAINING / IN** (IN yellow) | A · PIA21439 |
| Black Dwarf Short `mZ82-ijANk4` | `blackdwarf_short_mZ82-ijANk4.jpg` (+ `_16x9`) | **NOT ONE, / YET** (YET yellow) | B · sphere_base + SDO |
| Robot Short `buaOI3QGm7U` | `robot_short_buaOI3QGm7U.jpg` (+ `_16x9`) | **IT LASTED / 58 MINUTES** | B · cover v01 |

Text decisions: Saturn Short RAINING IN (mechanism; avoids long-title collision). Black Dwarf NOT ONE, YET (more specific than TOO YOUNG). Claude offered both pairs; Chief applied per Ben standing order.
