# Chief h37 corrections to SCRIPTS_AND_PACKAGING_v02.md (J1279, 31 Oct 2026)

Verdict: **script PASS** for AR1 + AR2 + AR3 (AR4 Halley stays reserve). The spoken words in v02 are locked as written.
The corrections below are binding on every follow-on job (VO, code graphics, assembly, listings). Where this file and v02 disagree, this file wins. v01 and v02 are kept unchanged.

## Facts and cards
- **C1. AR1 call-out card.** Use `4.3% (JUNE 2025) → 0% (WEBB, FEB 2026)`, not "early 2025".
  - The 4.3% came from NASA's 5 June 2025 update, after Webb's May 2025 look: "the asteroid's probability of impacting the Moon has slightly increased from 3.8% to 4.3%". https://science.nasa.gov/blogs/planetary-defense/2025/06/05/nasas-webb-observations-update-asteroid-2024-yr4s-lunar-impact-odds/
  - The words "early 2025" were in Chief's own h28 note. That was my mistake.
  - The spoken line "Early tracking gave a four percent chance of lunar impact" stays.
- **C2. AR3 date/place card and DATA bar.**
  - Card: `2 AUG 2027 · 258 KM PATH · LONGEST: 6M23S, EGYPT`. Bar label: `2027 EGYPT: 6M 23S`. Don't use "LUXOR" on screen.
  - NASA path table (SE2027Aug02Tpath): **Greatest Duration** is 06m23.2s at 10:00:21 UT, at 26°49'N 031°08'E, in central Egypt west of the Nile, south-west of Asyut. **Greatest Eclipse** is 06m22.6s at 25°30.3'N 033°11.0'E, east of Luxor.
  - Sources row S3.1 in v02 gives "06m23.2s" for the 25°30'N 033°11'E point. That attribution is wrong; read it as above.
  - The spoken line "peaking over Egypt at six minutes twenty-three seconds" is right, and stays.
- **C3. AR2 sources.**
  - The second GAO "quote" in S2.1 is not GAO's wording. GAO-26-107805 (published 17 Jun 2026) actually says: "Finally, at the end of 2030 or early 2031, the U.S. Deorbit Vehicle will perform a re-entry burn, which will push the ISS through the Earth's atmosphere and into the ocean. As part of the reentry process, NASA expects portions of the ISS and deorbit vehicle to break up and fall into the remote part of the ocean to minimize the risk to populated areas."
  - The **South Pacific** claim rests on the NASA ISS Transition Report (Jan 2022): "…line up the final target ground track and debris footprint over the South Pacific Oceanic Uninhabited Area (SPOUA), the area around Point Nemo…" https://www.nasa.gov/wp-content/uploads/2015/01/2022_iss_transition_report-final_tagged.pdf
  - Manifest sources have been corrected to match.

## Pictures (assembly must follow these)
- **C4. AR2 frame 0 and plates.** I checked frames from the pool on the NAS.
  - a) `Five_Minutes_in_Orbit.webm` is a night pass, and it's near-black at 0.5, 10, 20, 25 and 30 s. That fails rule 8 at frame 0.
  - b) `ISS_sunrise_to_sunset.ogv` shows the tail of Space Shuttle **Discovery**, with the name painted on it, not the station.
  - Frame 0 must be **moving footage of the station itself**. There are two £0 options:
    - NASA footage of the Crew-2 Endeavour fly-around (8 Nov 2021, public domain, images-api.nasa.gov). Check the in-point really shows the ISS.
    - A code-rendered ISS from the NASA 3D Resources model over a sunlit Earth plate.
  - If `ISS_sunrise_to_sunset` is used anywhere, crop out the Discovery lettering. Don't call it "orange re-entry glow"; it has none.
  - c) `ksc_071005_114_hire-12` is a 2005 KSC press Q&A video, not a fly-around. Drop it.
  - d) `iss070e062746.jpg` is North America's city lights at night (Jan 2024). It's fine for s06 (night pass), but it isn't a truss or solar-array shot for s02.
  - e) `iss026e005121.jpg` is Bahamas tidal flats with the ID printed on the image. It must not sit under "EMPTY SOUTH PACIFIC". Build s05 as a code-drawn South Pacific target map (Point Nemo, about 48°53'S 123°24'W) over a Pacific-facing Earth or plain ocean.
- **C5. AR3 plates.**
  - `NOAA_sat_eclipse_2024_notext.webm` has a NOAA logo in the bottom-left corner. Crop or mask it, and pick an in-point where the shadow is visible.
  - `NHQ201708210116` is a 13-frame 2017 sequence strip. Crop it and stamp it `2017`.
  - Credit both NHQ plates **NASA/Aubrey Gemignani**.
  - Gerst: start after the opening title card.
- **C6. AR4 (reserve only).** `PIA17485` is Giotto's 1986 image of the **nucleus** (NASA/ESA/Giotto Project), not a tail plate. Credit it that way.

## Timing
- **C7. Measure on the VO.**
  - Apophis v13a, the mould, spoke 39 written words in 17.7 s, so numerals read long. AR1 has 46 written words and three numerals ("2024 YR4", "2032"), so it could run past 20 s.
  - If a final cut comes out over 20.0 s, apply these pre-approved trims only, in this order:
    1. AR1 "Look up that night knowing…" becomes "Look up knowing…"
    2. AR1 "At sixty metres wide, it matches a fifteen-storey building." becomes "Sixty metres wide, it matches a fifteen-storey building."
    3. AR3 "The Moon's shadow spans two hundred and fifty-eight kilometres." becomes "Its shadow spans two hundred and fifty-eight kilometres."
  - Any other word change comes back to Chief.
- **C8. Answer timing.** This test copies the Apophis mould, and v13a's "It will miss" started at 12.35 s of 18.8 s (66%).
  - So the bar is: the answer line starts by about 13.5 s, and the "look up" line is last and loops into line 1.
  - Report the payoff % from the real VO as a measurement. The v02 estimates of "~70–74%" don't match their own word positions (AR2's answer starts at word 27 of 46).

£0. No mint and no upload. Nothing for Ben.
