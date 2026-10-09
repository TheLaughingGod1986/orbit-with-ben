# OWB 026 Nearest Star: pool v01 (J0065 step 3, Cursor covering, 8 Oct 2026)

Built from `SHOT_LIST_v01` + Claude's 8 Oct rulings. Every ID resolved live by `build_pool_v01.py` (NASA images API, Commons API, HEAD on ESO / ESA-Hubble / ESA). Fetched with `fetch_pool_v01.py --sheets`: **27/27 ok**, binaries in `pool_v01/` (gitignored, Mini only). Contact sheets: `rough_v01_pack/pool_v01_contact/<section>.jpg`. £0.

| Section | Rows | IDs |
|---|---|---|
| proxima | 3, 5, 6, 7, 21 | ESA/Hubble potw1343a (Proxima), ESO eso1629g (Proxima in Centaurus), NASA GSFC e000214 (Hubble Alpha Cen A+B) |
| alphacen | 7, 21, 33 | ESO eso1629i (DSS2 field, unannotated, 11k px), eso1629b (southern skies), eso1702a (VLT + Alpha Cen) |
| proxima_b | 28, 29 | ESO eso1629a, eso1629e (Kornmesser impressions); ESO videos eso1629d (journey, 32 s), eso1629e (fly-through, 60 s), 720p, mute |
| sun | 6, 30 | NASA SDO full disk e002035 (1024 px); SDO 17 Apr 2016 flare video (1080p, 80 s) |
| earth_moon | 19, 20, Fri S3 | NASA Blue Marble 2007 East e002130, Blue Marble 2012 East e001788 (11.5k px, for the London–Cairo pull-back), Full Moon e000868 |
| voyager | 22, 25, Wed | PIA17049, PIA21839 (720p art), PIA17462 (8k art), launch PIA17464, PIA21747 |
| sail | 31 | NASA ACS3 ACD24-0020-061 (ground test), onboard sail view CamA_Seq109 |
| dsn | 32 | PIA23214 (Goldstone complex, 8k), PIA26147 (Madrid array) |
| gaia | 15 | ESA/Gaia/DPAC sky in colour (CC BY-SA 3.0 IGO) |
| portraits | 13, 14 | Commons `Tycho Brahe.JPG`, `Friedrich Wilhelm Bessel (1839 painting).jpg` (both PD paintings) |

## Still open

| Item | Status |
|---|---|
| **ESO night-sky / Milky Way time-lapses** (rows 1, 2, 7, 33; frame 0 lock) | Not resolved: ESO's time-lapse archive doesn't list from the CLI. Needs a browser pick of 2 ESO time-lapse ids (or Claude names them). Until then rows 1/2/33 have no plate. |
| ESA Gaia spacecraft art (row 15 first half) | Not found; Gaia sky map alone carries row 15 unless Claude names an id. |
| NRAO 2019 Proxima flare illustration (row 30) | Not found; SDO flare video carries row 30. |
| ESO 61 Cygni / DSS2 field (row 14 second half) | Not found; eso1629i field or a starfield push stands in. |
| Hubble Proxima potw1343a is 604 px | Fill would be 3.2× (over 2.35×). Use it framed small on a starfield (feathered blur fill) or swap to eso1629g for full-frame. |
| Bessel portrait is 325×395 | 5.9× to fill. Use as an inset over a starfield (feathered), not full-frame. No larger PD scan on Commons. |
| ESO videos are 720p | Upscale 1.5×, inside the limit. |

## Credits (description)

ESO / ESO/M. Kornmesser / ESO/Digitized Sky Survey 2 (CC BY 4.0); ESA/Hubble & NASA (CC BY 4.0); ESA/Gaia/DPAC (CC BY-SA 3.0 IGO); NASA, NASA/JPL-Caltech, NASA/GSFC/SDO (public domain); Tycho Brahe and F. W. Bessel portraits, public domain via Wikimedia Commons.

Next (J0065): still_motion pushes per row + polish/fill gates, then assemble rough v01.

## v02 additions (J0065 step 4, Cursor covering, 9 Oct 2026)

**Why:** with each picture capped at two uses and each hold at 6 s, v01's 27 items fill at most ~370 s of the 494 s cut. `build_pool_v02.py` → `pool_v02.json` (51 entries: v01 + 25 new, all resolved live, ESO ids checked against their ESO page titles). Fetched into the same `pool_v01/` folder; sheets in `rough_v01_pack/pool_v02_contact/`. £0.

| Section | New ids | Notes |
|---|---|---|
| nightsky (new) | ESO eso0932a (Milky Way panorama, 6000×3000, S. Brunier), eso0934a (Paranal starscape, S. Guisard); NASA iss073e0982261, iss073e0982679 (Milky Way over airglow from the ISS), KSC-20191031-PH-GEB01_0003/_0005 (night sky over KSC), GSFC e000256 (Hubble star field) | **eso0932a slow pan is the proposed frame 0 / row 33 return** until Claude names ESO time-lapse ids. iss073e0982261 has ISS arrays in frame (WARN). |
| alphacen | ESO eso1702b (Alpha Centauri system, 19k px) | |
| voyager | PIA04495, PIA14111 (art), PIA21746, PIA21739 (1977 launch) | |
| dsn | PIA25136, PIA25137 (DSS-53 at night), PIA24163 | |
| sail | ACS3 CamB/CamC onboard views, ACS3_SolarPanels_001 (art) | CamB is portrait 1200×1920: crop only. |
| sun | GSFC e000790 (filament), e000759 (coronal holes), e000885 (Moon transiting Sun) | |
| earth_moon | GSFC e001982 (Moon, 1536 px), e001586 (City lights of the Nile, 720×1080), iss025e015176 (night Earth) | e001586 is 2.67× to fill: inset or crop-free use only, or skip. |

Left out: eso1629c (diagram), eso1629f / eso1629j / eso1241b (annotated), potw1606a (a transporter truck, not sky).
