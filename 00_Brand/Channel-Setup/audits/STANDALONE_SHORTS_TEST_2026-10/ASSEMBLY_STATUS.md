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

## Next

3. Orbit inserts at ~1 s on S1–S4 (Chief, #99 6125827198 item 4): 4 short Omni takes, a separate `video` job.
4–7. Assemble S1–S4 v01 (the J0150 pattern: hook caption, own title at 9–14 s, one overlay, captions, house whoosh and tick, loop to frame 0), then run `gate_shorts_open.py check` and `sfx_kit.py level`.
8. Covers.
9–10. S5–S8 once their VO lands.
