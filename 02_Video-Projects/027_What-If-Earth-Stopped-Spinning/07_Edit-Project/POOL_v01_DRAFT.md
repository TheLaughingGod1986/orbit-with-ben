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

## Fetched 9 Oct (Cursor covering, J0077): `pool_v01.json` → `pool_v01/` (local, gitignored), 23/23 ok, £0

`build_pool_v01.py` resolves each id to its largest copy; `fetch_pool_v01.py --sheets` downloads and writes `pool_v01/_contact/<section>.jpg`.

| Row | Pick | Size | Note |
|---|---|---|---|
| 22 | PIA23791 Venus from Mariner 10 | 2245×1096 | **Split panel** (natural + enhanced, white divider). Use the left (natural colour) half only, disc fitted to height on near-black; ~1.0× scale. |
| 34 molten core | USGS "Pahoehoe fountain" (Kīlauea) | 3072×2048 | Real photo, PD. Second choice: USGS "Cascade and fountain into Aloi Crater" 3596×2363. NASA PIA09968 / PIA22899 are false-colour satellite (drop); GSFC e000658 is a small night glow (drop). |
| 34 oceans | Blue Marble e002130 | 3718² | The same plate as row 8: counts as its second use. |
| 34 melting ice | GSFC e001753 melt lake (IceBridge) | 3648×2048 | Reads as "melting ice". Alt: e000112 melt ponds 3093×2062. e000213 / chutes are 1500–2000 px and less clear. |

Other checks from the fetch: EPIC e000265 is only 1920×1080 (fine at 1.0×). PIA13037 retroreflector is 752² (2.55× at full height → must be framed smaller or swapped). Eclipse NHQ201708210116 is a 12810×1500 strip (a sequence), not a single corona: pick another NHQ2017082101xx frame. SDO e002035 is 1024² (fit to height ~1.05×).

## Claude #6083184015 rulings applied (Cursor covering, J0077, 9 Oct 2026), £0

| Row | Pick | Size | Note |
|---|---|---|---|
| 25 | **as14-67-09386** "View of the Laser Ranging Retro Reflector deployed by Apollo 14 astronauts" | 4020×4020 | Claude's first choice met: a real Apollo photo with the reflector array as the subject, bootprints around it. A 16:9 crop of the full width is a downscale (~0.48×). PIA13037 kept as fallback only. Apollo 11 frames checked and dropped: AS11-40-5952 isn't in the API, and in AS11-40-5948 the seismometer fills the foreground and the reflector is ~235 px. |
| 27 | **NHQ201708210100** "2017 Total Solar Eclipse" (Madras, Oregon, totality) | 3186×2527 | One full-frame corona, no text. A 16:9 crop is ~0.6×. Alt: NHQ201708210102 diamond ring (3239×2196). The 0116 strip is not used. |

Frame 0 (rows 1, 15, 37): `fetch_epic_v01.py` downloads one day of EPIC natural-colour frames (2025-06-21, 22 frames at ~65 min, 2048² PNG) to `/private/tmp/owb027_epic_v01/` for a turning-Earth time-lapse. SVS 13056 (the produced EPIC video) has music and captions, so it isn't used.
