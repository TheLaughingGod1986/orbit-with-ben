# J0143 v02: 024 two-cover revision for Chief review

Built by Cursor, 12 Oct 2026, on Chief's 12:17Z reopen ("OK a FREE alternative ship plate … nothing paid, no frame with Orbit"). **Drafts for Chief cover review; no editorial PASS or final OK.**

## What changed from v01 (Chief's 10:49Z notes)

1. **Size:** the ship now fills **41% of frame height** (297 px of 720; box x 100–1256, y 329–626), up from about 15%. It sits wholly below the text band (band ends at y 236, ship starts at y 329).
2. **Not Voyager:** the ship is a new **no-cost generated plate** (Cursor's built-in image tool, no text, no Orbit, no planets, no people). Not NASA imagery, so it takes no NASA credit. No Vertex, Flow or ElevenLabs credit was spent. 024's own trip picture has no whole ship (Codex's `REVISION_SOURCE_AUDIT.md`), which is why a generated plate was used.
3. **Blue-shift glow:** the plate's starlight is crowded and blue ahead of the ship and fades to red behind, and the builder adds a cyan rim glow around the hull.
4. **Copy unchanged** (Chief OK'd both at 10:49Z):
   - Answer: **YOU: 1 YEAR / EARTH: 7 YEARS** (yellow YEARS), from the locked v02 opening: "You are gone for one year by your own watch. You land, and seven years have passed at home."
   - Tease: **OUTRUN / EARTH'S CLOCK** (yellow OUTRUN).

Both covers share the same plate, so a Test & Compare between them tests the words alone.

## Checks

`thumb_preview.py long <answer> <tease> --out <sheet> --score`:

```
PASS  024_answer_j0143_v02.jpg  saturation=194.4  near_black=19%
PASS  024_tease_j0143_v02.jpg  saturation=200.3  near_black=18%
```

- I looked at the 168×94 tiles on the phone sheet: both lines read at that size, the text stays off the ship, and the bottom-right badge corner is clear.
- Upscale from the plate is 1.8×, under the 2.35× cap.
- House font, 82 px cap height, one yellow hook word, black outline.
- No Orbit. The cover text doesn't repeat the title.

These are worker checks, not Chief sign-off.

## For Chief to decide

- Is a generated (artist's-impression) starship acceptable on the cover, given the film itself shows no ship? Chief's 12:17Z note allows it; this flags it so the call is on record.
- Which cover is primary. The 07:55 PASS named `024_tease_j0143_v01` as primary but quoted the answer copy (YOU: 1 YEAR / EARTH: 7 YEARS), so the primary needs restating for v02.

## Local deliverables (media outside git)

`/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/08_Thumbnail/j0143_v02/`:
- `024_answer_j0143_v02.jpg`
- `024_tease_j0143_v02.jpg`
- `024_j0143_v02_phone_sheet.jpg`
- `024_ship_plate_j0143_v02.jpg` (the source plate)
- `META.json`, `SCORE.txt`

Copies are in `~/_desk/handoff/J0143-v02/`. The builder is `08_Thumbnail/_build_light_speed_covers_j0143_v02.py`. The abc_v02/v03 sets and j0143 v01 are kept. No Studio, YouTube, package or Test & Compare change was made. Spend: zero.
