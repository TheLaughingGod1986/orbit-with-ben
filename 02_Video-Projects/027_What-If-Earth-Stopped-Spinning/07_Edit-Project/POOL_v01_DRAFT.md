# 027 pool v01: draft picks (Cursor covering, J0077, 9 Oct 2026)

From `search_pool_v01.py` → `pool_candidates_v01.json` and a second pass `pool_candidates_v01b.json` (images-api.nasa.gov, £0). Titles are as NASA lists them. Nothing is fetched yet; `build_pool_v01.py` resolves the chosen IDs to the largest copy and checks size against the 2.35× upscale limit.

## Stills picked (NASA, public domain)

| Row(s) | Need | NASA id | NASA title |
|---|---|---|---|
| 2 | Airborne-science jet at cruise | ED07-0256-09 | NASA's DC-8 airborne science laboratory soars over the Dryden Flight Research Center |
| 2 (alt) | ER-2 at altitude | AFRC2022-0059-49 | NASA's ER-2 performs a DCOTSS check flight |
| 8, 18 | Blue Marble | GSFC_20171208_Archive_e002130 / e002131 | NASA Blue Marble 2007 East / West (one use each) |
| 13 | Britain/London at night from the ISS | iss042e230335, iss025e012937 | to check by eye: crew photos, need London/UK in frame |
| 15, 35 | SDO full Sun | GSFC_20171208_Archive_e002035 | Full disk view of the sun June 21, 2010 (second framing at row 35) |
| 15 | EPIC full Earth | GSFC_20171208_Archive_e000265 | One Year on Earth – Seen From 1 Million Miles |
| 22 | Magellan Venus | S91-50688 | Global view of Venus from Magellan, Pioneer, and Venera data (023 plate) |
| 22 | Cloud Venus | PIA23791 | Venus from Mariner 10 |
| 23 | Full Moon | GSFC_20171208_Archive_e000868 | Full Moon |
| 26 | Moon far side | GSFC_20171208_Archive_e001939 | The Far Side of the Moon -- And All the Way Around (check: may be video/montage) |
| 25 | Laser-ranging retroreflector | PIA13037 | The Apollo 15 Lunar Laser Ranging Retroreflector (AS11-40-5952 not in the API; Apollo 15 swap, same job) |
| 27 | Total eclipse | NHQ201708210116 (2017) | 2017 Total Solar Eclipse (pick the cleanest corona of NHQ2017082101xx by eye) |
| 34 | Greenland ice sheet | GSFC_20171208_Archive_e000112 | Early Melt on the Greenland Ice Sheet |

**picture_qa risks flagged now:** S91-50688 and the PIA0027x Venus views are computer-made global views (FAIL class "computer model or reconstruction" under lesson 7). Row 22 may need PIA23791 only, or a real Akatsuki frame. Row 34's "Earth interior cutaway" art is also FAIL class; suggest a real IceBridge plate for both halves of row 34, or Claude's call.

## Not found in images-api (next run)

| Row(s) | Need | Where to look |
|---|---|---|
| **1, 15, 37** | **DSCOVR EPIC Earth turning (frame 0 lock)** | NASA SVS (svs.gsfc.nasa.gov, "EPIC" / "One Year on Earth" video), epic.gsfc.nasa.gov daily natural-colour frames → build a time-lapse |
| 1, 37 (alt) | ISS terminator time-lapse | eol.jsc.nasa.gov crew Earth observation videos |
| 2, 13 | ISS night pass over Europe | eol.jsc.nasa.gov video, or iss0xx night stills of Europe |
| 4 (v02), 11 | ISS cirrus / jet-stream clouds | eol.jsc.nasa.gov; candidates iss071e113334, s111e5451 (stills, check) |
| 6, 33 | ISS orbital sunrise (motion) | eol.jsc.nasa.gov; stills STS047-54-018 "Sunrise, Earth Limb", iss040e080833 as fallback |
| 7, 36 | ESO star-trail time-lapse | eso.org/public/videos (CC BY 4.0) |
| 9 | Foucault pendulum footage + portrait | Wikimedia Commons (CC BY/BY-SA only) |
| 12 | NOAA sea spray on rocky coast | NOAA photo/video library (PD) |
| 23 | Harbour tide time-lapse | NOAA |
| 27 | Cuneiform tablet | Met Open Access (CC0) |
| 28 | 2024 eclipse path animation | NASA SVS (2024 path); check for text-free span |
| 29 | Fossil coral, growth lines | Smithsonian Open Access / USGS |
| 32 | NIST-F2 caesium fountain | nist.gov image gallery (PD) |
| 37 | Young Earth / Moon-forming impact art | NASA SVS or JPL (artist concept: WARN class) |
