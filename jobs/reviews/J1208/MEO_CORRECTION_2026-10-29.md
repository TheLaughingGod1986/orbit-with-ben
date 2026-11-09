# J1208 — S5 MEO correction (Chief FIX follow-up, 29 Oct 2026)

Cursor worker (`assembly`), no spend, no v03 render, no YouTube/Buffer/UPLOADS/privacy changes.

**Authority:** `jobs/reviews/J1208/CHIEF_RULING_2026-10-29.md` (acting Chief Codex FIX). Scope is **one bounded S5 source correction** on the already-downloaded NASA All-Sky Fireball Network / MEO event files. SVS 11943 ISS package stays rejected (animated Ron Garan photograph). S6 Titan opening stays the prior missing-input hold — no new broad Titan search this run.

Machine evidence (not in git):

- `/Volumes/data/mac-mini-archive/scratch/J1208/meo_correction/MEO_CORRECTION.json`
- `/Volumes/data/mac-mini-archive/scratch/J1208/meo_correction/MEO_REJECTION_TABLE.json`
- `/Volumes/data/mac-mini-archive/scratch/J1208/meo_correction/frames/` (dense samples, open + proposed crops)
- `/Volumes/data/mac-mini-archive/scratch/J1208/meo_correction/MEO_TOP_CROPS_sheet.jpg`
- Slim mirror in-repo: `jobs/reviews/J1208/MEO_CORRECTION_2026-10-29.json`

---

## Method

1. Inspected all **18** `ev_*.mp4` files already under `…/J1208/raw/` (640×480, h264, ~2.1–4.7 s).
2. Sampled every 0.1 s; measured bright-pixel onset and frame-to-frame MAD inside a 48 px border.
3. For each event, searched fixed crops that **exclude** typical top/bottom timestamp bands and side margins, keeping crop width **≥ 460 px** so a 1080-wide 16:9 centre band stays **≤ 2.35×**.
4. Full-size visual check of top crop sequences (not metrics alone). Did **not** re-propose SVS 11943, Geminid-v05, FireBall04 watermark master, or PIA17656.

Rights (unchanged): NASA All Sky Fireball Network / MEO — imagery and video available for anyone to download; credit NASA/MEO. Source page: https://fireballs.ndc.nasa.gov/

---

## Finite rejection table (all 18)

Every file: **REJECT**. Common facts: native **640×480**; every open frame carries burned-in **UTC timestamp (bottom-left)** and **station id (bottom-right)**; proposed crops can remove those glyphs while staying ≥460 px wide, but the remaining subject fails the house open test.

| File | SHA-256 (full in JSON) | Dur | Onset | Tried crop (w×h @ scale) | Why REJECT |
|---|---|---|---|---|---|
| `ev_20261010_071444A_09A.mp4` | `b8d1274b…` | 2.17 s | none | 640×400 @1.688× | No clear onset; burned-in text; no phone-readable streak |
| `ev_20261012_004857A_03A.mp4` | `f233406b…` | 4.67 s | 3.1 s | 520×376 @2.077× | Text; crop subject = fisheye rim/noise, not a shooting-star streak at frame 0 |
| `ev_20261012_004858A_01A.mp4` | `5ec894f9…` | 4.74 s | 1.3 s | 460×360 @2.348× | Text; brief flash then gone (~0.5 s); not a recognizable streak open |
| `ev_20261012_010814A_03A.mp4` | `115f1e92…` | 3.27 s | 1.8 s | 460×392 @2.348× | Text; open only ~0.4 s; subject too weak after crop |
| `ev_20261012_010814A_04A.mp4` | `8df278c3…` | 4.44 s | false | 500×400 @2.160× | **Moon/horizon wash** (~46k bright px every frame); not a meteor |
| `ev_20261012_010814A_07A.mp4` | `8b5ac71e…` | 3.54 s | 1.0 s | 480×320 @2.250× | Text; elongation ~1 inside crop — pinpoints, not streak |
| `ev_20261012_054757A_01A.mp4` | `cf68cdb9…` | 2.70 s | 1.6 s | 460×360 @2.348× | Text; flash collapses within ~0.25 s; not a usable open streak |
| `ev_20261012_054757A_03A.mp4` | `b9b7fa66…` | 2.74 s | 1.1 s | 600×368 @1.800× | Best scale of the set; still text + rim glow / tiny dash — **fails phone-readable streak at frame 0** (full-size stills on NAS sheet) |
| `ev_20261012_054757A_04A.mp4` | `d833bb7d…` | 2.54 s | none | 640×400 @1.688× | No onset; text; sparse bright noise |
| `ev_20261012_103559A_04A.mp4` | `18cb40c5…` | 2.14 s | none | 640×400 @1.688× | No onset; text |
| `ev_20261012_103559A_07A.mp4` | `75d5d3c4…` | 2.20 s | 1.0 s | 460×336 @2.348× | Text; bright mass hugs fisheye rim, not a central meteor streak |
| `ev_20261013_031855A_04A.mp4` | `0e337eb5…` | 3.47 s | 1.1 s | 460×360 @2.348× | Text; weak crop subject at 2.348× |
| `ev_20261015_103948A_01A.mp4` | `ca16fca1…` | 2.44 s | 0.9 s | 460×400 @2.348× | Text; bright mass on edge, not a readable streak |
| `ev_20261015_121440A_09A.mp4` | `e8ead0d4…` | 2.20 s | none | 640×400 @1.688× | No onset; text |
| `ev_20261016_070530A_01A.mp4` | `2d0a8289…` | 2.94 s | 1.4 s | 460×360 @2.348× | Text; flash then empty; not a streak open |
| `ev_20261016_090347A_09A.mp4` | `232eba0d…` | 2.40 s | none | 640×400 @1.688× | No onset; text |
| `ev_20261016_090834A_01A.mp4` | `15ead075…` | 2.14 s | none | 640×400 @1.688× | No onset; text |
| `ev_20261016_104347A_01A.mp4` | `6b4b3510…` | 2.27 s | 1.0 s | 460×400 @2.348× | Text; no elongated streak after crop |

Auto metric “CANDIDATE” flags (12/18) were **overruled by full-size viewing**: bright-pixel / MAD spikes tracked rim glow, horizon wash, or sub-second flashes — not a shooting-star open that reads at phone size with the sound off.

---

## Precise missing input (S5)

A **logo-free, overlay-free** meteor **video** (real camera streak traversing successive frames — not a still, not a constellation diagram, not an animated photograph of a still) with:

- recognizable streak already at the open’s **frame 0**;
- a usable window **≤ 2.7 s** (shorter OK; prefer genuine event over a static tail);
- native crop width **≥ ~460 px** for 16:9 centre-band ≤ 2.35× (or native ≥1080 with clean 9:16 centre crop ≤ 2.35×);
- clear commercial-reuse / NASA-or-observatory credit evidence;
- **no** burned-in timestamps, station names, reticles, watermarks or panels in the used window (or a crop that removes them without killing the streak).

The 18 downloaded MEO event mp4s do **not** meet that bar.

---

## S6 (unchanged)

No new Titan search this run (Chief: “No repeated broad search”). Prior missing input stands: clean sequential optical Titan (Huygens DISR / Cassini) without dashboard/altitude panels and with enough native detail for ≤2.35× centre-band. PIA17656 and annotated DISR packages stay rejected. Dragonfly TakingOff remains mid-film only.

---

## Ask for Chief (source decision only)

1. **S5:** ACCEPT this finite MEO rejection — no v03 from these 18 files.  
2. Either authorize a **different** no-spend source class (e.g. a specific observatory / NASA page naming a clean fireball clip), or keep S5 on the scheduled-copy path until 5 Nov / Ben watch rules.  
3. **S6:** leave missing-input hold; J1199 verification checkpoint unchanged.  
4. Still **no assembly** until a source/edit OK.

Worker: £0; no generation; no publishing mutations; SVS 11943 not re-proposed.
