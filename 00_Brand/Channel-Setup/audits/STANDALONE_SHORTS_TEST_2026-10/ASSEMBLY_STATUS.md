# Standalone Shorts assembly status (J0163)

Cursor, 12 Oct 2026. Builds S1–S4 now (VO passed, J0162). S5–S8 wait for their facts pass and VO. Nothing uploaded, nothing spent.

## Done (steps 1–2 of 10)

**Pause trim** (`_pause_trim_v01.py`, Chief's J0162 PASS): every gap over 0.4 s is cut to 0.4 s, using the Scribe word times. Trimmed audio is in `vo_v01/trim/` on the Mini (git-ignored), and the remapped word times are in `vo_v01/trim/*_trim_words.json`.

| Short | VO before | VO after | With the ~3 s loop hold |
|---|---|---|---|
| S1 Mercury | 18.96 s | 17.52 s | ~20.5 s |
| S2 Neptune | 27.28 s | 22.42 s | ~25.4 s |
| S3 ISS | 27.84 s | 25.14 s | ~28 s |
| S4 Uranus | 20.56 s | 18.20 s | ~21 s |

All four stay under the 40 s gate. S2 and S3 are over the 18–22 s target, which Chief accepted on J0162.

**NASA plates** (`_harvest_plates_v01.py`, images-api.nasa.gov, free): 19 candidates are in `/private/tmp/owb_sa_shorts/plates/<short>/` with a contact sheet per Short. The ids, titles and source pages are in `plates_v01.json`.

| Short | Usable | Problem |
|---|---|---|
| S1 Mercury | PIA11351 and PIA12266, MESSENGER horizons at 1018×1024 (~1.9× for 9:16) | PIA13674 has labels and an inset (crop it or drop it). PIA12842 is false colour. |
| S2 Neptune | PIA01492, Voyager 2 full disk at 2188 px; crop onto the white streaks | The close streak plates PIA00058 and PIA00063 (682–844 px) need 2.6–3.2×, over the 2.35× cap. |
| S3 ISS | iss059e027932 (sunrise burst on the limb, 5568 px), iss040e080833, iss061e123823 | none |
| S4 Uranus | PIA18182 (disc), PIA00143 and PIA01391 (crescents) | NASA's library has no rings-upright view. The script's frame 0 asks for Uranus on its side with its rings upright, so it needs a Veo plate or the Webb image (ESA/Webb, CC BY 4.0, credit in the description). |

## Parked for Chief (Cursor, 12 Oct 2026 20:55)

S5–S8 VO is in (J0202 PASS), so all 8 have voice. Two decisions stop the assembly before any render:

1. **Music bed.** Every Short needs a bed for its full length (lesson 5), but these 8 have no long, so there's no film bed to lay. New beds are held until the 30 Oct reset without Chief's OK. The options:
   - (a) One new standalone-Shorts bed through `generate_music_bed.py` (API, Pace and NOT brief), laid under all 8 and trimmed per Short. It spends ElevenLabs credit (about 6,800 left after J0202) and needs Chief's OK.
   - (b) Lay the nearest film's existing bed, at no spend: S1 Mercury and S3 ISS on 022's `sun-brighter_score_bed_v01`, S2 Neptune and S4 Uranus on 024's `light-speed_score_bed_v01`, and so on. This blurs the "own score" rule and the music_gate's similarity check.
   - (c) A synthesised house drone (own code, no spend, no licence), extending `sfx_kit.py`. It's thin compared with a scored bed.
2. **S4 Uranus frame 0.** NASA has no rings-upright plate. Use the Webb image (ESA/Webb, CC BY 4.0, credit in the description), or a Veo plate under the Vertex £0.10 rule.

Also waiting: **J0200** (Orbit Omni inserts at about 1 s, Chief item 4). The assembly needs those clips at row 2, or else a re-render once they land.

## Chief ruling (6131710376, 12 Oct 20:04) and step 3 done (Cursor, 21:20)

- **Music bed (a), done.** One bed for all 8: `05_Music/owb-standalone-shorts_score_bed_v01.mp3` (60 s, loopable, −16.3 LUFS, Pace 84–96 BPM and a NOT list naming every earlier Orbit bed, in the plan JSON). About 825 credits (estimate at ~13.75 credits/s; the balance read 7,382 before and hadn't updated after), under Chief's 1,500 cap. Logged in `elevenlabs_ledger.jsonl` and ai_spend. The mp3 is git-ignored and stays on the Mini.
- **S4 frame 0: Webb `weic2310a`** (rings upright, 1268 px, about 1.5× for a full-height 9:16). Credit in the description: "Uranus image: ESA/Webb, NASA, CSA, STScI (CC BY 4.0)". It's in `/private/tmp/owb_sa_shorts/plates/s4_uranus/` and `plates_v01.json`. Still with a smooth push, no Veo.
- **House SFX kit** made: `/private/tmp/owb_sa_shorts/sfx_kit_v01/` (rumble, whoosh, tick).
- **J0200** (Orbit inserts) is still open. The build goes ahead with the ~1 s Orbit row left open, and Orbit drops in once J0200 lands.

## Steps 4–5: S1–S4 v01 assembled (Cursor, 12 Oct 22:00)

`_assemble_standalone_shorts_v01.py` builds all four from the plates above, with no spend.
- **Picture:** every frame is drawn in Python with a float crop box, so the pushes don't step. Each opener gets a fast ease-out push (+15% in the first second), so frame 0 is already moving. There's a hard cut every 3–6 s. The last ~3 s crossfade (0.5 s) back to the opening plate and pull back onto frame 0's framing, so each Short loops. Plates too small to fill 9:16 (PIA00063, PIA00058, PIA02210, PIA00346, and the Webb rings) are fitted to the width over a blurred, darkened copy of themselves, with feathered edges. Every row stays under the 2.35× upscale cap (the per-row `max_upscale` is in each meta). Grain is `noise=alls=4:allf=t`.
- **On screen:** the hook caption runs 0–2.2 s (yellow hook word). Each Short's own title shows at 9–14 s. Captions run throughout (3-word groups). One animated overlay sits inside the 16:9 band, at 11.5% of the band height per line:
  - S1: "176 / EARTH DAYS", 14.0–17.2 s
  - S2: Earth 400 vs Neptune 2,000 KM/H, two growing bars, 14.1–17.9 s
  - S3: a counter running 1→16 with "EVERY 90 MINUTES", 17.5–21.6 s
  - S4: "TIPPED / 97°", 6.4–9.0 s, over the dark side of a crescent (not on the disc)
- **Sound:** the trimmed VO, the standalone bed at 0.065 (0.35 in the loop hold), a house whoosh at frame 0 (a rumble on S4) and one tick on the overlay. The mix is −14 LUFS. VO, bed and SFX stems are in `/private/tmp/owb_sa_shorts/build_v01/<stem>/`.
- **Orbit row** at ~1 s is left open (`orbit_slot` in each meta) for J0200; the opening plate runs under it for now.
- **Outputs:** `06_Final-Exports/<stem>_v01.mp4` (git-ignored, on the Mini), plus a `_frames.jpg` contact sheet, `_gate.txt`, `_sfx_level.txt` and `_meta.json` (cut list) for each.
- **Gates:** see the results table below. Every Short carries the duration warning, because they run ~20–25 s against the house 22–27 s band (Ben's exception, and the gate counts it as a warning only).

**Results (22:07):**

| Short | Length | `gate_shorts_open` | Motion 0–1 s | `sfx_kit level` | Left to do |
|---|---|---|---|---|---|
| S1 Mercury | 20.44 s | PASS (length warning only) | 10.6 | PASS | nothing |
| S2 Neptune | 25.28 s | PASS | 6.8 (warning) | PASS | Re-cut the opening: the smooth blue disc barely changes even with a 35% push. Try PIA00058's streaks for frame 0 (fitted, panning) and move PIA01492 later. |
| S3 ISS | 27.40 s | PASS | 13.4 | FAIL: the whoosh is within 10 LU of the VO at 0.5 s for 0.3 s | Drop S3's whoosh gain to ~0.15. S3 is at the 27.4 s ceiling: the hold is 2.3 s. |
| S4 Uranus | 21.17 s | PASS (length warning only) | 16.1 | PASS | nothing |

S4 also warned once that its open plate was 16 bits from `pL339HhjDwo` (7 Oct). That was on the earlier frame 0, and it cleared on the final render.

## Step 6: S2 and S3 fixed (Cursor, 12 Oct 23:05)

- **S3:** whoosh gain 0.22 → 0.15 (a per-Short `sfx_gain`). `sfx_kit level` now PASSes (SFX −37.4 LUFS against VO −20.8), and the gate still PASSes at 27.40 s.
- **S2:** opening plate PIA00058 (fitted streaks) only reached motion 4.0, because the fitted plate sits over a still blur and the gate compares 72×128 frames. So frame 0 is back on PIA01492 (Voyager 2 disc) with a fast ease-out pan across the limb onto the Great Dark Spot and its streaks (`open_pan` 0.26 → 0.44, push 0.25). The loop pans back to the same frame-0 framing. Rows are now PIA01492 → PIA00063 → PIA00058 → PIA02210, all under 2× upscale. Motion is 11.96, the gate PASSes with no warning, and `sfx_kit level` PASSes.

S1–S4 v01 are now clean on `gate_shorts_open` and `sfx_kit level`, apart from the ~20 s length warning on S1 and S4 (Ben's exception).

## Step 7: S1–S4 covers (Cursor, 12 Oct 23:35)

`_build_covers_s1-s4_v01.py` draws each cover on that Short's own frame-0 picture, rendered by the assembler's `Plate` class at the opening zoom with no burned-in text, so the cover matches frame 0. It uses the house v04 type (Arial Black, yellow hook word, white rest, words inside the 16:9 centre band) with no Orbit. The script refuses any cover word that is also in the title (§2.3). Covers go in `08_Covers/` (the jpgs are git-ignored and stay on the Mini; `MANIFEST.json` is tracked). Each has a `thumb_preview.py short` sheet, and the words read in both the 9:16 and the 16:9 crop.

| Short | Title | Cover (yellow word) | Plate |
|---|---|---|---|
| S1 | A Day on Mercury Lasts Two Years | **SLOWEST** / SUNRISE | PIA11351 |
| S2 | The Wind on Neptune Is Supersonic | **2,000** KM/H / WINDS | PIA01492 |
| S3 | Astronauts See 16 Sunrises Every Day | DAWN EACH / **90** MINUTES | iss040e080833 |
| S4 | This Planet Has 21-Year Winters | TIPPED ON / ITS **SIDE** | ESA/Webb weic2310a |

For Chief: S4's words sit over the Uranus disc (the Short centre-stack, as on past Short covers; the long-thumb "never over the subject" band rule isn't applied to Shorts). S2 says WINDS where the title says Wind; the check passes, but Chief may prefer a different second word.

## Next

- S5–S8 assembly (steps 8–9; all VO in, J0202), then contact sheets and gates on the thread and park for Chief (step 10).
- Superseded list below kept for history.

3. Orbit inserts at ~1 s on S1–S4 (Chief, #99 6125827198 item 4): 4 short Omni takes, a separate `video` job.
4–7. Assemble S1–S4 v01 (the J0150 pattern: hook caption, own title at 9–14 s, one overlay, captions, house whoosh and tick, loop to frame 0), then run `gate_shorts_open.py check` and `sfx_kit.py level`.
8. Covers.
9–10. S5–S8 once their VO lands.
