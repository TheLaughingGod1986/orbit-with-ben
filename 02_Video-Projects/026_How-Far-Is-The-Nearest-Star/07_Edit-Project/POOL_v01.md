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

## v03 additions: ESO time-lapses + label flags (J0065, Cursor covering, 9 Oct 2026; Claude #6073730799, #6074131477)

Fetched to `pool_v01/timelapse/` (largest MP4 offered, used muted). Credit line for each: **ESO (CC BY 4.0)**.

| id | ESO title | use | note |
|---|---|---|---|
| uhd_yb_paranal_01 | Milky Way revealed | frame 0 (row 1); row 33 at a different segment | 3840×2160, 7.6 s. Milky Way visibly drifts. |
| uhd_bt_paranal_01 | Distant time-lapse of Paranal | row 2 | 3840×2160, 8.1 s |
| bt_lasilla_crux | Milky Way above mountain | row 7 | 3840×2160, 10.3 s, pillarboxed: content x=300 w=3240; 16:9 crop (300,0,3240,1822) |
| eso1241a | A journey to Alpha Centauri | optional, rows 5/7 | 1280×720, 70 s. Clean only ~4.5–10 s: ESO logo 0–4 s, constellation lines and "Alpha Centauri" labels from ~15 s. |

Out (`"labels": true` in pool_v02.json): eso1629g (white constellation chart), eso1702a, eso1702b, eso1629b (label overlays). None has an unannotated variant on its ESO page. The SDO M6.7 flare video opens on a text card, so cut in after it. Dropped (no insets): potw1343a, the Bessel portrait, e001586.

## v04 additions: more time-lapses + star-field plates (J0065, Cursor covering, 9 Oct 2026; Claude #6074250379)

`build_pool_v03.py` → `pool_v03.json` (v02 + 12). Every ESO/ESA-Hubble page title checked live; every file and frame strip checked by eye for logos, text and labels (sheets in `rough_v01_pack/pool_v03_contact/`). £0. Rule from Claude: at most two extra segments per time-lapse; fill the rest from these.

| id | title | clean range / note |
|---|---|---|
| uhd_bt_paranal_06 | Yepun takes centre stage | 3840×2160, 13.4 s, clean throughout (laser guide star from ~10.5 s) |
| uhd_bt_paranal_07 | Yepun in action | 3840×2160, 8.8 s; dome moves/blurs ~0.5–2 s, use 2.0–8.8 s |
| uhd_yb_paranal_02 | Auxiliary Telescope at work at Paranal | 3840×2160, 10.8 s, clean; sky lightens after ~6 s |
| vltfromvistatimelapse | A VISTA on the VLT | 1280×720 (1.5×), 29.4 s; **clean only 3.5–14.0 s**. Logo cards 0–3 s and 26–29 s, near-black 15–24 s, daylight frame + white flash ~24–25 s |
| eso0844a | Omega Centauri (ESO) | 8040×7560 |
| heic0809a | Omega Centauri (Hubble) | 11936×10891 |
| eso1302a | 47 Tucanae | 8246×8246 |
| eso1323a | NGC 6752 | 8221×8023 |
| eso1250a | Carina Nebula (VST) | 17383×18656: ffmpeg can't decode, pre-shrink with `sips -Z 8000` |
| eso0905a | Carina Nebula | 8408×8337 |
| eso1031a | Carina around WR 22 | 8395×8261 |
| heic1007a | Mystic Mountain (Carina) | 2104×1937 (crop ≤ ~1.0× for 1920 wide) |

None labelled. eso1242a (VISTA Milky Way centre) dropped: no "large" file on the CDN. The star clusters sit on dark sky, so push into the bright core to pass the near-black gate.
