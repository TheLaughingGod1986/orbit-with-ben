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

## Next

3. Orbit inserts at ~1 s on S1–S4 (Chief, #99 6125827198 item 4): 4 short Omni takes, a separate `video` job.
4–7. Assemble S1–S4 v01 (the J0150 pattern: hook caption, own title at 9–14 s, one overlay, captions, house whoosh and tick, loop to frame 0), then run `gate_shorts_open.py check` and `sfx_kit.py level`.
8. Covers.
9–10. S5–S8 once their VO lands.
