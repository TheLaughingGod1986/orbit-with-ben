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

## pool_v01b (Cursor covering, J0077, 9 Oct 2026): rows 9, 27, 29, 32, £0

`pool_v01b.json` → `pool_v01/` (local, gitignored) via `fetch_pool_v01.py --pool pool_v01b.json --sheets` (now takes `.webm`). 7 of 8 fetched. The Met's own API returned 410, so the Met CC0 tablets come through their Commons copies (Met Open Access uploads). Review sheet: `pool_v01b_sheet.jpg`. Every frame of both videos was checked on a 12-frame strip: no burnt-in text, no fades.

| Row | Pick | Size | Licence / credit | Note |
|---|---|---|---|---|
| 9 footage | Griffith Observatory Foucault pendulum, July 2022 (webm) | 3840×2160, 13.7 s | CC0, Benoît Prieur | Real bob swinging over the floor marker. Handheld (slight drift). A small physical plaque sits at the right edge, unreadable at 1080; crop it out if Claude prefers. |
| 9 footage (alt) | "Foucault pendulum 1" (webm) | 1920×1080, 32.2 s | CC BY-SA 4.0, Jud McCranie | Shows the **ring of pegs** the bob knocks over, which suits "the floor was". Visitors' legs at the top edge; a tight crop to the lower ~80% loses them (≤1.25×). |
| 9 portrait | Portrait of Léon Foucault, 1860 | 1024×1395 | Public domain | Engraving. Has a signature line at the bottom: crop to head and shoulders (no text). Portrait shape, so feathered-blur fill. |
| 27 tablet | Met "Cuneiform tablet: commentary on Enuma Anu Enlil, tablet 5" (DP-442-001) | 4000×3000 | CC0, The Met | **Astronomical:** Enuma Anu Enlil is the Babylonian celestial-omen series, so the caption can say so. Plain light-grey background, no labels. |
| 27 tablet (alt) | Met "Cuneiform tablet: fragment of an astronomical table (?)" 86.11.374a,b | 3648×2736 | CC0, The Met | Two fragments on a white mat; the "(?)" in the Met title means keep any caption generic. |
| 29 coral 1 | *Heliophyllum confluens* fossil coral, Columbus Limestone, Middle Devonian | 3615×2864 | CC BY 2.0, James St. John | Real Devonian rugose coral (the genus behind the classic ~400 days-a-year growth-line count). Growth lines are faint at this framing: a slow push into the ridged side. |
| 29 coral 2 | *Eridophyllum seriale* fossil rugose coral, Middle Devonian | 3438×2768 | CC BY 2.0, James St. John | **Not fetched yet:** Commons returned 429 three times. Next run retries. |
| 32 | NIST-F2 caesium fountain atomic clock (NIST, Physics Lab) | 1200×857 | Public domain | Two physicists at the fountain. 1.26× at full height. Row 32's "NIST lab plate" second half still needs a pick. |

Still not found: ISS cirrus / orbital sunrise / night Europe (rows 2, 4, 6, 11, 13, 33), ESO star trails (7, 36), NOAA spray and tide (12, 23), the 2024 eclipse path (28), the young-Earth art (37), and row 32's second plate.

**Claude #6085507220 (row 9):** the pegs ring ("Foucault pendulum 1", Jud McCranie, CC BY-SA 4.0), cropped off the legs (≤1.25×), a peg falling on "The floor was." Griffith is the backup. Description credit: "Foucault pendulum 1" by Jud McCranie, CC BY-SA 4.0.

## pool_v01c (Cursor covering, J0077, 9 Oct 2026): ISS, ESO, sea, tide rows, £0

`search_pool_v01c.py` → `pool_candidates_v01c.json`. images-api.nasa.gov has almost no ISS time-lapses, so these come from Commons (NASA, ESA and ESO uploads, licence read from the file page). `build_pool_v01c.py` → `pool_v01c.json` → `fetch_pool_v01.py --pool pool_v01c.json --sheets` (now also takes `.ogv`).

| Row(s) | Pick | Size | Licence / credit | Note |
|---|---|---|---|---|
| 4 (v02) cirrus, 6 + 33 sunrise, 2 + 13 night Europe | ESA "Alexander Gerst's Earth timelapses (2017 reissue)" (webm) | 3840×2160, 358 s | CC BY-SA 3.0 IGO, ESA | One 4K reel of ISS time-lapses: day passes over cloud, orbital sunrises, night cities. Spans still to pick by eye and check for burnt-in text (ESA reels often open and close on titles). |
| 6, 33 (alt) | "Sunrise To Sunset Aboard The ISS" (ogv) | 1280×720, 76 s | Public domain, NASA (Robert Simmon) | 1.5× to 1080. |
| 2, 11, 13 (alt) | "Five Minutes in Orbit" (webm) | 1920×1280, 31.5 s | Public domain, NASA (ISS073 crew photos) | Crop 16:9 from 3:2. |
| 7, 36 | ESO "Time-lapse Over La Silla" (webm) | 1920×1090, 33.9 s | CC BY 4.0, R. Wesson/ESO | Real stars wheeling over the domes. Check every frame for the ESO logo/credit card. |
| 7, 36 (alt still) | ESO "Star trails over the VLT in Paranal" | 6144×4096 | CC BY 4.0, ESO/B. Tafreshi | Still; use as the second star beat so the time-lapse isn't used three times. |
| 12 | "Waves crashing on rocks off Beach 4, Kalaloch Beach, Washington 02" (webm) | 1920×1080, 19.2 s | CC BY-SA 4.0, Joe Mabel | Real spray on a rocky coast. Not NOAA, so it carries a credit. |
| 23 | "Bay of Fundy – Tide In" + "Tide Out" | 2272×1704 each | CC BY 2.0, Dylan Kereluk | Same spot at high and low tide: cut in → out on the tide line. No NOAA harbour time-lapse found. |
| 29 coral 2 | *Eridophyllum seriale*, Middle Devonian (retry) | 3438×2768 | CC BY 2.0, James St. John | Commons 429 retry from pool_v01b. |

Fetch (tmux `j0077-poolc`): 7 of 9 in `pool_v01/`. Both Bay of Fundy stills hit Commons 429; retry next run.

**Gerst reel (`gerst_strip_v01c.jpg`, one frame every 10 s):** a small **ESA logo sits in the top-left corner** of most frames, so it's burnt-in branding. A crop that loses it is about 1.1× on the 4K source, well under 2.35×; Claude to rule crop vs drop. Candidate spans: cloud day passes 40–50 s and 310 s (row 4 cirrus); night cities 120 s, 280 s, 320 s, 350 s (rows 2, 13: Europe still to confirm by eye); airglow limb 250–260 s (rows 6, 33 sunrise feel). ISS hardware fills 160–240 s and 270–300 s: not used. 0 s is a black open.

Still open: the 2024 eclipse path (28), young-Earth art (37), row 32's second plate.

**Claude #6085748466 (Gerst reel):** use the Gerst 4K reel and **crop the ESA logo out on every row that uses it** (about 1.1×). Credit: "ESA/A. Gerst, CC BY-SA 3.0 IGO". The NASA public-domain ISS clips are fallbacks only. The rest of v01c is approved (La Silla + VLT trails, Kalaloch, the Fundy pair, the second coral).

Retry on 9 Oct: the Fundy tide in/out pair and *Eridophyllum* are now fetched (pool_v01c 9 of 9).

## pool_v01d (Cursor covering, J0077, 9 Oct 2026): rows 28, 32 second plate, 37, £0

`build_pool_v01d.py` → `pool_v01d.json` → `fetch_pool_v01.py --pool pool_v01d.json --sheets` (tmux `j0077-poold`).

| Row | Pick | Size | Licence / credit | Note |
|---|---|---|---|---|
| 28 | NASA SVS 5219 "2024 Path of Totality" flyover, **no-text** version (webm) | 3840×2160, 110 s | Public domain, NASA SVS | What the shot list asks for: the path sweeping across North America. It's a map visualisation, so picture_qa WARN (map/render): Claude to look full size. |
| 28 (alt) | NOAA "Satellites View Total Solar Eclipse" 8 Apr 2024, **no-text** version (webm) | 3840×2160, 132 s | Public domain, NOAA | Real GOES satellite imagery of the Moon's shadow crossing North America. Real footage, so no WARN; it shows the same "seen from far away" idea. |
| 32 second plate | NIST "Ytterbium Lattice Atomic Clock" | 2700×1793 | Public domain, NIST | Lab bench with the lattice clock optics. |
| 32 (alt) | NIST "Atomic Clock006" | 6042×4641 | Public domain, NIST | Large lab plate. |
| 37 | NASA Goddard "Bennu's Journey – Early Earth" | 5760×2160 | Public domain, NASA GSFC Conceptual Image Lab | Wide young-Earth art (artist's concept: picture_qa WARN). Crop to 16:9; then the return to the opening EPIC Earth as the shot list says. |
| 37 (alt) | "Hadean" | 2092×1124 | CC BY-SA 4.0, Tim Bertelink | Young-Earth painting; carries a credit. |

Fetch: 6 of 6 in `pool_v01/` (local). Sheets: `pool_v01/_contact/nist.jpg`, `young.jpg` (local); video strips committed as `svs5219_strip_v01d.jpg` (one frame / 10 s) and `noaa_eclipse_strip_v01d.jpg` (one frame / 11 s).

**Strip check (every frame, not just the first):**
- **SVS 5219 "notext" is not text-free:** the base map carries state, city and country names in every frame (TEXAS, OKLAHOMA, Great Lakes cities…). Under "no labels or burnt-in text" it fails. Not recommended for row 28.
- **NOAA reel (recommended for row 28), usable spans, each with a small "NOAA" or "NASA" bug in a corner (crop it out, about 1.1–1.2×):**
  - ~0–15 s: GOES full disk, the Moon's shadow on North America (bug bottom-left). Full disk on black, so it needs the 16:9 fill.
  - ~55 s: real visible-light split view of the shadow over the US (bug top-left).
  - ~66 s and ~110 s: DSCOVR EPIC full disk with the shadow (bug bottom-right). Same look as the frame-0 EPIC Earth, so it ties back.
  - **Avoid:** ~22 s (NASA/SVS rendered globe with path lines), ~33 s (composite graphic), ~77 s (IR greyscale, OK but dull), ~88 s (data map full of labels and a timestamp), ~99 s (false-colour), ~121 s (corona plate, not this row).
  - Exact in/out points still to set at assembly from a 1 fps strip of each span.
- **Row 32:** Ytterbium lattice clock (colour, modern) after NIST-F2; Atomic Clock006 is a 1950s black-and-white NBS lab photo (alt).
- **Row 37:** Bennu's Journey Early Earth (molten ground, meteor streaks, storm sky): crop 16:9 from the wide 5760×2160 (no upscale). Hadean alt shows a huge red Moon low over lava, which fits "Moon-forming" too but carries a credit.

**Claude to rule:** row 28 = NOAA spans (real) instead of the shot list's SVS map, since the SVS flyover has labels throughout? Row 37 = Bennu Early Earth or Hadean?

The pool is now complete for every row in SHOT_LIST_v02 except the 2 Omni + 2 Veo Fast beats (free Vertex, £5 floor).
