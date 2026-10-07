# Gemini picture + numbers check v01 — J0008 — checked by cursor/gemini — 2026-10-07

Inputs: `07_Edit-Project/shot_list_v01.csv` at git commit `e93443d`.

Note: Claude decides every swap (per standing order: Claude owns script reviews, shot lists, and final editorial decisions).

## Flagged shots

| row | id | what it really shows (instrument, wavelength, date, obs/vis) | VO line | why it's wrong | suggested swap (from the row's fallback column or NASA_POOL_v01.md, with id) |
|---|---|---|---|---|---|
| 1 | SVS 10925 | SDO AIA, 171 Å (extreme UV), 2012-03-06, real observation (X5.4 solar flare with EIT coronal waves and CME) | The sun is getting brighter. Why does it brighten while it runs down? | Script visual must (line 9) mandates: "Frame 0 is the Sun filling the 16:9 frame, a prominence already mid-rise off the limb and breaking away." SVS 10925 is an X5.4 solar flare eruption and coronal wave, not a prominence ('flare' over a prominence). | SVS 11517 (from row 1 fallback column: SDO AIA 304 Å "Graceful Eruption", a genuine prominence eruption mid-rise) |
| 5 | PIA21783 | SDO AIA, 304 Å (extreme UV), 2017-06-25 to 2017-06-26, real observation (prominence arch churning at the solar limb) | It is not the spots. | Under the direct line "It is not the spots", the image shows an erupting prominence arch at the limb with no sunspots visible. Although cataloged under the title "New Lone Sunspot Group", the NASA image and description are exclusively of a prominence. | PIA19876 ("Big Sunspot Group", visible-light continuum view of real sunspots from NASA_POOL_v01.md S2) or GSFC_20171208_Archive_e000923 |
| 48 | GSFC_20171208_Archive_e002035 | SDO AIA, 335 Å (extreme UV / Fe XVI, ~2.5 million K), 2010-06-02, real observation (full solar disc colorized bright electric cyan/blue) | What would you see across a hundred million years? | The script emphasizes human visual perception ("not a new color on a walk... you would see almost nothing at first"), but the plate displays an artificial extreme-UV false-color cyan/blue Sun. A wavelength view is presented as "what you'd see". | PIA19876 (white-light visible solar disc from NASA_POOL_v01.md S2) or iss074e0494675 (orbital sunrise from S6) |
| 53 | GSFC_20171208_Archive_e002035 | SDO AIA, 335 Å (extreme UV), 2010-06-02, real observation of today's Sun (full solar disc in EUV) | Wind the clock back. When earth was young, this same star was fainter. | Shows today's modern SDO Sun under a line explicitly stating the star was fainter when Earth was young (today's Sun under a line about the young Sun). | SVS 11853 (NASA Goddard simulation/animation of the faint young Sun) or GSFC_20171208_Archive_e000888 (artist's concept of young Earth from NASA_POOL_v01.md S4) |
| 55 | as4-01-750 | Apollo 4 70mm Hasselblad, visible light, 1967-11-09, real observation of planet Earth (Atlantic Ocean and Antarctica from 8,628 nmi) | Roughly 30 % dimmer than the disk in your sky. | The VO specifically points to the solar disc ("the disk in your sky"), but the plate shows a full-globe photograph of planet Earth from Apollo 4 (wrong object entirely). | SVS 11853 (simulation of the dimmer young Sun disc from NASA_POOL_v01.md) or a dimmed solar disc graphic / GSFC_20171208_Archive_e000888 |
| 85 | GSFC_20171208_Archive_e002035 | SDO AIA, 335 Å (extreme UV), 2010-06-02, real observation of today's Sun (full solar disc) | The disk swells only slowly through this stretch, a little larger. | The VO describes the future Sun ~1 billion years from now expanding/swelling ("The disk swells only slowly... a little larger"). The picture is an unmodified modern 2010 SDO image of today's Sun with no swelling (today's Sun under future Sun). | Scaled/brightened edit plate of the solar disc (per script line 80: "modestly larger and brighter disc") or iss071e439624 (orbital sunrise catching extra light) |
| 92 | GSFC_20171208_Archive_e000414 | SDO AIA, 171 Å (extreme UV), 2015-01-11 to 2016-01-21, composite of 23 real observations (SDO Year 6 solar cycle 24 active region belt) | The 10 % sun is further off than any civilization you can picture. | The VO explicitly refers to the future +10% Sun ("The 10 % sun"), but the plate shows a modern 23-frame composite of today's solar cycle active regions (today's Sun under future Sun). | iss074e0494675 or s09-11-675 (orbital sunrise to illustrate the civilization/sky context, or NASA_POOL_v01.md S5 Earth skin) |
| 95 | GSFC_20171208_Archive_e000759 | SDO AIA, 193 Å (extreme UV), 2015-03-16, real observation (two large coronal holes near south pole and equator) | A 10th of 1 % up and down with the spots. A prominence when the cameras want motion. | The VO explicitly names "the spots" (sunspots) and "a prominence". Coronal holes are open magnetic field regions where fast solar wind escapes, completely distinct from both sunspots and prominences. Coronal holes are neither spots nor prominences. | A cut or split of true sunspots (PIA19876 from S2) and an erupting prominence (GSFC_20171208_Archive_e002168 or PIA22123 from S1) |
| 98 | GSFC_20171208_Archive_e000991 | SDO AIA, 131 Å / multi-EUV, 2014-09-10, real observation (significant X-class solar flare surge) | Earth has lived the dimmer half. The oceans are still here because the climb has not gone too far. | An intense X-class flare surge is shown under narration discussing Earth's oceans surviving the dimmer half. Flares are magnetic bursts ("the wrong clock", NASA_POOL_v01.md §133) and factually unrelated to the oceans remaining during the secular climb. | as08-16-2588 (Earth oceans from Apollo 8) or s04-41-1206 (open ocean sunglint from STS-4, NASA_POOL_v01.md S5) |
| 103 | GSFC_20171208_Archive_e002131 | NASA Reto Stöckli / GSFC, MODIS / DMSP composite, 2007-10-09, global composite visualization (Blue Marble 2007 West with city lights and oceans) | star that brightens while it burns? | Under the spoken phrase specifically naming the "star that brightens while it burns", the plate displays planet Earth with city lights (wrong object entirely: Earth night lights under a line about the star). | GSFC_20171208_Archive_e002035 or SVS 11112 (solar disc) from NASA_POOL_v01.md S6 |
| 104 | SVS 10925 | SDO AIA, 171 Å (extreme UV), 2012-03-06, real observation (X5.4 solar flare with EIT coronal waves and CME) | Next door, there is a planet that may already have taken that path. Next week, what happened to Venus? | The shot list src_in note explicitly states "stretch 2: a different stretch from the open, prominence in motion; hold to the end" and script line 103 mandates "a prominence already in motion". SVS 10925 is an X5.4 solar flare, NOT a prominence ('flare' over a prominence). | SVS 11517 stretch 2 (SDO AIA 304 Å "Graceful Eruption", a genuine prominence in motion from NASA_POOL_v01.md) |

## Clock numbers (row 96)

Code graphic `clocks.mp4` (drawn by `code_graphics.py`, function `render_clocks`) plots three markers along a logarithmic time axis from 1 hour to 2 billion years:

### Clock 1: Secular Brightening Pace
- **Claim:** About 1% brighter per 110 million years (drawn at `x = 110e6` years, labeled "the climb", "+1% every 110 million years").
- **Verdict:** CONFIRMED
- **Exact Quote:** "The present Sun is increasing its average luminosity at a rate of 1% in every 110 million years, or 10% over the next billion years. All this is completely consistent with established solar models like the one of Gough (1981)."
- **URL:** [https://doi.org/10.1111/j.1365-2966.2008.13022.x](https://doi.org/10.1111/j.1365-2966.2008.13022.x) (arXiv: [https://arxiv.org/abs/0801.4031](https://arxiv.org/abs/0801.4031))
- **Reason:** The rate of 1% per 110 million years (+10% per billion years) is verbatim from Section 2 of Schröder, K.-P. & Connon Smith, R. (2008), *"Distant future of the Sun and Earth revisited"*, *MNRAS*, 386(1), 155–163.

### Clock 2: Solar Cycle Irradiance Modulation
- **Claim:** About 0.1% up and down over the 11-year solar cycle (drawn at `x = 11.0` years, labeled "the sunspot wobble", "11 years, up and down").
- **Verdict:** CONFIRMED
- **Exact Quote:** "Space-borne measurements have established that Total Solar Irradiance varies by approximately 0.1% over the course of the 11-year solar cycle." (Modulation of order 1 W/m² on the modern baseline of ~1361 W/m²).
- **URL:** [https://doi.org/10.1029/2010GL045777](https://doi.org/10.1029/2010GL045777) · [https://lasp.colorado.edu/home/sorce/data/tsi-data/](https://lasp.colorado.edu/home/sorce/data/tsi-data/)
- **Reason:** The 11-year period and ~0.1% peak-to-peak solar irradiance variation are standard, validated numbers from space-based radiometry (SORCE/TIM, Kopp & Lean 2011, *Geophys. Res. Lett.*, 38, L01104, and TSIS-1).

### Clock 3: Prominence Lifetime
- **Claim:** A prominence lasting about a day / days (drawn at `x = 3 / 365.25` [3 days], labeled "a prominence", "days").
- **Verdict:** NEEDS WORDING
- **Exact Quote:** NASA SDO / Solar Physics: "Prominences can persist for days, weeks, or even months." NASA PIA22123: "A prominence at the sun's edge shifted and slithered back and forth over a one-day period (Nov. 29-30, 2017)... Towards the end of the clip, it blasts out a small stream of plasma."
- **URL:** [https://images.nasa.gov/details/PIA22123](https://images.nasa.gov/details/PIA22123) · [https://solarscience.msfc.nasa.gov/prominences.shtml](https://solarscience.msfc.nasa.gov/prominences.shtml)
- **Reason:** Dynamic eruptive prominences and active-region filaments typically evolve, erupt, or dissipate over hours to a few days (matching the ~3-day placement in `code_graphics.py` and the SDO clips in the film). However, quiescent prominences anchored in stable coronal magnetic arcades can persist for weeks or several months. Labeling prominence lifetimes generally as "days" or script line 16 "in a day it is over" is accurate for eruptive/active events, but scientifically requires qualification that quiescent structures last months.

## All other rows OK

Total GODDARD/NASA rows checked: **97**  
Total OK rows: **86** (Flagged: **11**)  

| row | id | what it shows (instrument, wavelength, date, obs/vis) |
|---|---|---|
| 2 | iss074e0494675 | ISS Expedition 74, digital camera, visible light, 2026-04-21, real observation (orbital sunrise illuminating Earth surface over southern France) |
| 3 | SVS 11517 | SDO AIA, 304 Å (extreme UV), 2015-06-18, real observation (prominence and CME eruption) |
| 4 | GSFC_20171208_Archive_e002168 | SDO AIA, 304 Å (extreme UV), 2010-03-30, real observation (erupting prominence at limb, SDO first light) |
| 6 | s85e5052 | Space Shuttle Discovery (STS-85), Electronic Still Camera (ESC), visible light, 1997-08-12, real observation (orbital sunrise and glowing Earth limb over continental United States) |
| 7 | GSFC_20171208_Archive_e002035 | SDO AIA, 335 Å (extreme UV / Fe XVI), 2010-06-02, real observation (full disk view of the Sun in extreme ultraviolet) |
| 8 | PIA22123 | SDO AIA, 304 Å (extreme UV), 2017-11-29 to 2017-11-30, real observation (slithering prominence shifting at solar limb over 1 day) |
| 9 | SVS 13778 | SDO AIA, 304 Å / 171 Å (extreme UV), 2020-11-29, real observation (anemone prominence eruption) |
| 10 | PIA22123 | SDO AIA, 304 Å (extreme UV), 2017-11-29 to 2017-11-30, real observation (slithering prominence shifting at solar limb over 1 day) |
| 11 | GSFC_20171208_Archive_e001052 | SDO AIA, 304 Å (extreme UV), 2014-05-27, real observation (stream of plasma bursting out and falling back into Sun) |
| 12 | GSFC_20171208_Archive_e000970 | SDO AIA, 304 Å (He II, extreme UV), 2014-09-26, real observation (twisting blob of plasma erupting off limb) |
| 13 | GSFC_20171208_Archive_e002035 | SDO AIA, 335 Å (extreme UV / Fe XVI), 2010-06-02, real observation (full disk view of the Sun in extreme ultraviolet) |
| 15 | PIA20881 | SDO AIA with PFSS magnetic field line overlay, extreme UV, 2016-06-16, visualization overlay on real observation (magnetic field lines illuminated) |
| 16 | s85e5052 | Space Shuttle Discovery (STS-85), Electronic Still Camera (ESC), visible light, 1997-08-12, real observation (orbital sunrise and glowing Earth limb over continental United States) |
| 17 | GSFC_20171208_Archive_e001363 | SDO AIA, 304 Å / 171 Å (extreme UV), 2013-09-29 to 2013-09-30, real observation (filament eruption / Canyon of Fire) |
| 18 | SVS 3548 | SOHO EIT, Fe XII 195 Å (extreme UV), 1996, real observation (quiet solar corona at solar minimum) |
| 19 | PIA22662 | SDO AIA with PFSS magnetic field model overlay, extreme UV, 2018-08-10, visualization overlay on real observation (magnetic field lines concentrated above active region) |
| 20 | SVS 3549 | SOHO EIT, Fe XII 195 Å (extreme UV), 2000, real observation (active solar corona at solar maximum) |
| 21 | PIA22123 | SDO AIA, 304 Å (extreme UV), 2017-11-29 to 2017-11-30, real observation (slithering prominence shifting at solar limb over 1 day) |
| 22 | iss017e011603 | ISS Expedition 17, digital camera, visible light, 2008-07-22, real observation (Earth limb sunrise with noctilucent clouds over central Asia) |
| 23 | GSFC_20171208_Archive_e001052 | SDO AIA, 304 Å (extreme UV), 2014-05-27, real observation (stream of plasma bursting out and falling back into Sun) |
| 24 | GSFC_20171208_Archive_e000970 | SDO AIA, 304 Å (He II, extreme UV), 2014-09-26, real observation (twisting blob of plasma erupting off limb) |
| 25 | PIA20881 | SDO AIA with PFSS magnetic field line overlay, extreme UV, 2016-06-16, visualization overlay on real observation (magnetic field lines illuminated) |
| 26 | s85e5052 | Space Shuttle Discovery (STS-85), Electronic Still Camera (ESC), visible light, 1997-08-12, real observation (orbital sunrise and glowing Earth limb over continental United States) |
| 27 | GSFC_20171208_Archive_e002035 | SDO AIA, 335 Å (extreme UV / Fe XVI), 2010-06-02, real observation (full disk view of the Sun in extreme ultraviolet) |
| 28 | SVS 31400 | NASA Pleiades Supercomputer / Mansour et al., numerical simulation, 2015, scientific visualization (solar interior convective flows) |
| 29 | PIA20881 | SDO AIA with PFSS magnetic field line overlay, extreme UV, 2016-06-16, visualization overlay on real observation (magnetic field lines illuminated) |
| 31 | PIA22662 | SDO AIA with PFSS magnetic field model overlay, extreme UV, 2018-08-10, visualization overlay on real observation (magnetic field lines concentrated above active region) |
| 32 | PIA22645 | SDO AIA, 171 Å (extreme UV), 2018-07-14 to 2018-07-16, real observation (detailed coronal loops illuminated by charged particles above an active region) |
| 33 | PIA21764 | SDO AIA, 171 Å (extreme UV), 2017-06-20, real observation (coils of magnetic field lines and plasma spirals after minor filament eruption) |
| 34 | iss074e0494675 | ISS Expedition 74, digital camera, visible light, 2026-04-21, real observation (orbital sunrise illuminating Earth surface over southern France) |
| 35 | GSFC_20171208_Archive_e001978 | SDO AIA, 304 Å (extreme UV), 2010-09-08, real observation (C3-class flare and prominence on full solar disc) |
| 36 | SVS 31400 | NASA Pleiades Supercomputer / Mansour et al., numerical simulation, 2015, scientific visualization (solar interior convective flows) |
| 37 | PIA22360 | SDO AIA, 304 Å, 193 Å, 171 Å triple comparison (extreme UV), 2018-03-20 to 2018-03-21, real observation (wavelength comparisons showing spicules, coronal holes, active regions) |
| 38 | PIA15377 | SDO AIA, 171 Å and 304 Å side-by-side comparison (extreme UV), 2016-10-27, real observation (coronal holes compared across wavelengths) |
| 39 | PIA22724 | SDO AIA, 304 Å and 193 Å side-by-side comparison (extreme UV), 2018-09-11, real observation (prominence at limb vs coronal holes in corona across two wavelengths) |
| 41 | GSFC_20171208_Archive_e000808 | SDO AIA with time-lapse PFSS magnetic model, EUV, 2016-01, visualization overlay on real observation (magnetic field lines) |
| 42 | GSFC_20171208_Archive_e000393 | SDO AIA with PFSS magnetic model overlay, EUV, 2016-03-12, visualization overlay on real observation (solar magnetic field) |
| 43 | PIA22662 | SDO AIA with PFSS magnetic field model overlay, extreme UV, 2018-08-10, visualization overlay on real observation (magnetic field lines concentrated above active region) |
| 44 | SVS 11112 | SDO AIA, multi-wavelength gradient (EUV), 2010–2013, composite of real observations (full solar disc) |
| 45 | PIA22645 | SDO AIA, 171 Å (extreme UV), 2018-07-14 to 2018-07-16, real observation (detailed coronal loops illuminated by charged particles above an active region) |
| 46 | PIA21764 | SDO AIA, 171 Å (extreme UV), 2017-06-20, real observation (coils of magnetic field lines and plasma spirals after minor filament eruption) |
| 47 | GSFC_20171208_Archive_e001978 | SDO AIA, 304 Å (extreme UV), 2010-09-08, real observation (C3-class flare and prominence on full solar disc) |
| 49 | PIA22360 | SDO AIA, 304 Å, 193 Å, 171 Å triple comparison (extreme UV), 2018-03-20 to 2018-03-21, real observation (wavelength comparisons showing spicules, coronal holes, active regions) |
| 50 | PIA15377 | SDO AIA, 171 Å and 304 Å side-by-side comparison (extreme UV), 2016-10-27, real observation (coronal holes compared across wavelengths) |
| 51 | SVS 5649 | SDO AIA, multi-wavelength EUV timelapse, 2010-06-03 to 2010-06-06, real observation (restless solar disc and active regions) |
| 52 | s09-11-675 | Space Shuttle Columbia (STS-9), 35mm camera, visible light, 1983-11-28 to 1983-12-08, real observation (Earth limb at brilliant orbital sunrise with Spacelab 1 silhouetted) |
| 54 | SVS 11853 | NASA GSFC Conceptual Image Lab, animation/visualisation, 2016, CGI simulation (faint young Sun and early Earth) |
| 56 | s04-41-1206 | Space Shuttle Columbia (STS-4), 70mm camera, visible light, 1982-06-27 to 1982-07-04, real observation (sunglint reflecting off North Atlantic Ocean and clouds near Bahamas) |
| 57 | sl4-142-4577 | Skylab 4, 70mm Hasselblad, visible light, 1974-01-28, real observation (South Georgia Island and massive tabular icebergs in South Atlantic Ocean) |
| 58 | GSFC_20171208_Archive_e000888 | NASA GSFC Conceptual Image Lab, artist's concept, 2014, CGI illustration (early Earth bombarded by asteroids, Bennu's Journey) |
| 59 | S66-25771 | Gemini 8 (Gemini-Titan GT-8), 70mm Hasselblad, visible light, 1966-03-16, real observation (Earth limb and sunrise over Guam with cloud silhouettes) |
| 60 | GSFC_20171208_Archive_e000888 | NASA GSFC Conceptual Image Lab, artist's concept, 2014, CGI illustration (early Earth bombarded by asteroids, Bennu's Journey) |
| 61 | ast-27-2339 | Apollo-Soyuz Test Project (ASTP), 70mm Hasselblad, visible light, 1975-07-20, real observation (Earth limb at sunrise and cloud silhouettes in Southern Hemisphere) |
| 62 | s36-07-012 | Space Shuttle Atlantis (STS-36), 70mm camera, visible light, 1990-02-28 to 1990-03-04, real observation (sun beaming off cloud-covered ocean waters) |
| 63 | as4-01-750 | Apollo 4 (unmanned), automatic 70mm camera, visible light, 1967-11-09, real observation (Atlantic Ocean and Antarctica from high Earth orbit at 8,628 nmi) |
| 64 | s04-41-1206 | Space Shuttle Columbia (STS-4), 70mm camera, visible light, 1982-06-27 to 1982-07-04, real observation (sunglint reflecting off North Atlantic Ocean and clouds near Bahamas) |
| 65 | sl4-142-4577 | Skylab 4, 70mm Hasselblad, visible light, 1974-01-28, real observation (South Georgia Island and massive tabular icebergs in South Atlantic Ocean) |
| 66 | S66-25771 | Gemini 8 (Gemini-Titan GT-8), 70mm Hasselblad, visible light, 1966-03-16, real observation (Earth limb and sunrise over Guam with cloud silhouettes) |
| 68 | GSFC_20171208_Archive_e000888 | NASA GSFC Conceptual Image Lab, artist's concept, 2014, CGI illustration (early Earth bombarded by asteroids, Bennu's Journey) |
| 69 | ast-27-2339 | Apollo-Soyuz Test Project (ASTP), 70mm Hasselblad, visible light, 1975-07-20, real observation (Earth limb at sunrise and cloud silhouettes in Southern Hemisphere) |
| 70 | as4-01-750 | Apollo 4 (unmanned), automatic 70mm camera, visible light, 1967-11-09, real observation (Atlantic Ocean and Antarctica from high Earth orbit at 8,628 nmi) |
| 72 | GSFC_20171208_Archive_e002035 | SDO AIA, 335 Å (extreme UV / Fe XVI), 2010-06-02, real observation (full disk view of the Sun in extreme ultraviolet) |
| 73 | S06-46-617 | Space Shuttle Challenger (STS-6), 35mm camera, visible light, 1983-04-04 to 1983-04-09, real observation (Earth limb and sunset over Amazon Basin) |
| 74 | iss071e364425 | ISS Expedition 71, Nikon digital camera, visible light, 2024-07-16, real observation (noctilucent clouds illuminated by sub-horizon Sun over North Pacific) |
| 75 | iss072e617674 | ISS Expedition 72, Nikon digital camera, visible light, 2025-02-01, real observation (storm clouds over South Pacific Ocean northwest of New Zealand) |
| 76 | iss072e769023 | ISS Expedition 72, Nikon digital camera, visible light, 2025-03-10, real observation (cloudy Indian Ocean southwest of Perth, Australia) |
| 77 | sts064-83-099 | Space Shuttle Discovery (STS-64), 70mm camera, visible light, 1994-09-09 to 1994-09-20, real observation (multiple developing thunderstorm cells and mature anvil tops over Pacific) |
| 78 | s44-94-051 | Space Shuttle Atlantis (STS-44), 70mm Hasselblad, visible light, 1991-11-24 to 1991-12-01, real observation (Supertyphoon Yuri spiral vortex and eye over Western Pacific) |
| 79 | GSFC_20171208_Archive_e002131 | NASA Reto Stöckli / GSFC, MODIS / DMSP composite, 2007-10-09, global composite visualization (Blue Marble 2007 West: Americas, ocean, clouds, city lights) |
| 80 | STS067-709-007 | Space Shuttle Endeavour (STS-67), 70mm camera, visible light, 1995-03-02 to 1995-03-18, real observation (sunset and Earth limb showing distinct atmospheric gas layers) |
| 82 | as08-16-2588 | Apollo 8, 70mm Hasselblad, visible light, 1968-12-21 to 1968-12-27, real observation (Atlantic Ocean and West Africa from lunar translunar/orbital flight) |
| 83 | sts065-86-095 | Space Shuttle Columbia (STS-65), 70mm camera, visible light, 1994-07-18, real observation (Hurricane Emilia spiral thunderstorm bands and eye over Eastern Pacific Ocean) |
| 84 | GSFC_20171208_Archive_e002130 | NASA Reto Stöckli / GSFC, MODIS / DMSP composite, 2007-10-09, global composite visualization (Blue Marble 2007 East: land, ocean, clouds, city lights) |
| 86 | S06-46-617 | Space Shuttle Challenger (STS-6), 35mm camera, visible light, 1983-04-04 to 1983-04-09, real observation (Earth limb and sunset over Amazon Basin) |
| 87 | iss071e364425 | ISS Expedition 71, Nikon digital camera, visible light, 2024-07-16, real observation (noctilucent clouds illuminated by sub-horizon Sun over North Pacific) |
| 88 | iss071e439624 | ISS Expedition 71, Nikon digital camera, visible light, 2024-08-06, real observation (orbital sunrise illuminating Earth atmosphere and day/night terminator over South Pacific) |
| 89 | iss072e617674 | ISS Expedition 72, Nikon digital camera, visible light, 2025-02-01, real observation (storm clouds over South Pacific Ocean northwest of New Zealand) |
| 90 | s39-610-037 | Space Shuttle Discovery (STS-39), 70mm Rollei camera, visible light, 1991-04-28 to 1991-05-06, real observation (sunset and atmospheric aerosol scattering layers on Earth limb) |
| 91 | SVS 5649 | SDO AIA, multi-wavelength EUV timelapse, 2010-06-03 to 2010-06-06, real observation (restless solar disc and active regions) |
| 93 | GSFC_20171208_Archive_e001517 | SDO AIA, 171 Å (extreme UV), 2012-04-16 to 2013-04-15, composite of 25 real observations (The Sun: One Year in One Image, rise to solar max) |
| 94 | PIA17669 | SDO AIA, 193 Å (extreme UV), 2013-03-28 to 2013-03-31, real observation (large coronal hole on solar face / source of fast solar wind) |
| 97 | GSFC_20171208_Archive_e002035 | SDO AIA, 335 Å (extreme UV / Fe XVI), 2010-06-02, real observation (full disk view of the Sun in extreme ultraviolet) |
| 99 | s09-11-675 | Space Shuttle Columbia (STS-9), 35mm camera, visible light, 1983-11-28 to 1983-12-08, real observation (Earth limb at brilliant orbital sunrise with Spacelab 1 silhouetted) |
| 100 | iss071e439624 | ISS Expedition 71, Nikon digital camera, visible light, 2024-08-06, real observation (orbital sunrise illuminating Earth atmosphere and day/night terminator over South Pacific) |
| 101 | GSFC_20171208_Archive_e000414 | SDO AIA, 171 Å (extreme UV), 2015-01-11 to 2016-01-21, composite of 23 real observations (SDO Year 6 active region belt) |
| 102 | as08-16-2588 | Apollo 8, 70mm Hasselblad, visible light, 1968-12-21 to 1968-12-27, real observation (Atlantic Ocean and West Africa from lunar translunar/orbital flight) |

## Could not verify

None. Every GODDARD and NASA asset (55 unique IDs across all 97 rows) was successfully located, queried, and verified on official NASA web endpoints:
- SVS clips (9 IDs): `https://svs.gsfc.nasa.gov/<id>`
- NASA images (46 IDs): `https://images.nasa.gov/details/<id>` and `https://images-api.nasa.gov/search?nasa_id=<id>`

Zero rows failed to load.
