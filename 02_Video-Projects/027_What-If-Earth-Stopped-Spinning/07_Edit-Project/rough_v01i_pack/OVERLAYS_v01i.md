# 027 Earth Spin v01i: NUMBER label on the open (J0256)

Cursor (stand-in for Codex on a `chart` job), 15 Oct 2026. Advisory: Chief scores the gate.

- **Why this chapter.** J0154's scan covered chapters 1–5 (each now has a numeral on screen in v01h) but not the open. The 026 prep sheet (J0145) scores the open as its own chapter, so 027's open (0:00–0:23.3) is the next one. Its only code graphic, row 3's speed globe (0:16.7), is text-free, and "about a thousand kilometers an hour" (0:06.9) had no numeral on screen. Under Chief's 12 Oct ruling that's a NUMBER FAIL.
- **The label:** "About 1,000 km/h", 0:06.88–0:09.25 (2.37 s) on row 1 (EPIC spinning Earth), in on "about" and out before the 0:09.3 cut. Bottom-left over the Atlantic; Britain, the place the line names, is at the top edge. Same house pill as v01h (navy at 86%, white Arial Bold 80 px, 0.35 s fade and rise in, 0.3 s fade out). 3 words, the VO's own, with the number as a numeral.
- **Source:** `01_Script/SOURCES.md` row 1: 465.1 m/s × cos 51.5° ≈ 290 m/s ≈ 1,040 km/h at London (NASA Earth Fact Sheet; NASA Ask an Astrophysicist on latitude scaling).
- **Base.** v01h's master was purged from `/private/tmp`, and the NAS share wasn't answering (NFS hang on 15 Oct 06:25), so v01i is rebuilt from v01g (the OWB UAT copy, sha256 `dc9d9ffe…` as in `rough_v01g_pack/SHA256.txt`) with every v01h label unchanged plus this one. Builder: `../_overlay_earth_spin_v01i.py`. File names: v01h's labels keep their text and timings; the timeline renders move from index 05/06 to 06/07 because the new label is index 05 (`code_graphic_027_row1_05.png`).
- **Cut:** `/private/tmp/027_EarthSpin_rough_v01i.mp4` (sha256 in `SHA256.txt`). Audio is v01g's stream, copied (`audio_v01i.json`). No cut, VO, bed or graphic change, no spend.
- **First 30 s:** the label rides on real moving footage (EPIC), 7 s before the row 3 graphic with two real shots between, so no code graphics run back to back.
- **Gates:** `picture_qa_v01i.txt`, `polish_gate_v01i.txt`. Before/after stills: `overlay_stills_v01i.jpg`.

## For Chief

1. Score the open: NUMBER and WORDS for "About 1,000 km/h" (VO "about a thousand kilometers an hour"; the sourced figure is ~1,040 km/h).
2. With this, every 027 chapter (open + 1–5) shows a numeral. "24 hours" (7:18) is still unlabelled; its SOURCES row now exists (J0154), so it can be added if you want it.
3. v01i isn't on the NAS yet (share hung). It needs copying there or to OWB UAT before any watch or upload (the 14 Oct master rule).
