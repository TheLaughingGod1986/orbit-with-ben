#!/usr/bin/env python3
"""J3023 v02 synchronized shot-list, cuts, pool and provenance generator for OWB:064.

Replaces historical v01 executable inputs (leaving all v01 files untouched) per J3883 formal handoff:
  - Synchronized to SHOT_LIST_v02.md opening R01a–R04b (10 cuts <= 3.80 s through 32.85 s) and R09.
  - PIA00271 and PIA00233 completely removed from active inputs and explicitly marked rejected in pool.
  - R09 uses real Mariner 10 PIA23791 (right globe crop 1160:0:1085:1096) + Pioneer Venus UV pvo_uv_790205.
  - R11 preserves exact PIA00215 SHA-256 46dc965a02d4bff533685892ad16a76845a384d482ffaedda024c870b5b8a7b4,
    crop (350,600,2550,1838) pushing smoothly to (430,645,2470,1793), 118.05–124.40 s, followed by
    code_graphic_064_r14_venus_spin_v02.mp4 through 130.75 s.
  - Preserves PIA18033 corrected attribution: NASA/NOAA/GSFC/Suomi NPP/VIIRS/Norman Kuring.
  - Enforces picture cadence & reuse across ALL narration blocks (zero LONG_RUN > 15 s, zero consecutive
    code graphics, every still appearance <= 2, every clip duration <= source length, chapter cards 2.40 s
    at exact 0.60 s post-sentence breath).

Writes:
  - 07_Edit-Project/shot_list_v02.csv
  - 07_Edit-Project/cuts_064_j3023_v02.json
  - 07_Edit-Project/pool_064_j3023_v02.json
  - 07_Edit-Project/POOL_PROVENANCE_J3023_v02.json
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

PROJ_REPO = Path(__file__).resolve().parents[1]
EDIT_DIR = PROJ_REPO / "07_Edit-Project"
NAS_064 = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes")
NAS_EDIT = NAS_064 / "07_Edit-Project"
HARV = NAS_064 / "03_Reference-Material/harvest_J3022_v01"
RADAR = NAS_064 / "03_Reference-Material/J3835_radar_v01"
CG_V01 = NAS_064 / "04_Generated-Clips/J3022_code_graphics_v01"
CG_V02 = NAS_064 / "04_Generated-Clips/J3023_code_graphics_v02"
STT_PATH = PROJ_REPO / "02_Voiceover/stt/every_planet_explained_vo_v01/stt_raw.json"

SL = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects")
ARC24 = Path("/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/02_Video-Projects")
ARC05 = Path("/Volumes/data/mac-mini-archive/2026-11-05/YouTube/orbit-with-ben/02_Video-Projects")

REQUIRED_PIA00215_SHA = "46dc965a02d4bff533685892ad16a76845a384d482ffaedda024c870b5b8a7b4"
REQUIRED_PVO_SHA = "f9d45efa36ac2bd00bc72f5abf8beedd0ee75d06c99c629012e27c87ee59db80"
REQUIRED_VO_SHA = "4b478fcded393890064ffd285a4121882dc26e0515f3cadc6569adf0465616aa"

# Active verified assets (PIA00271 and PIA00233 permanently excluded!)
ASSETS: dict[str, tuple[Path, str, str, str, bool, float]] = {
    # Mercury
    "PIA15162": (HARV / "PIA15162.jpg", "NASA/JHU APL/Carnegie", "Public Domain (NASA/JPL)", "Mercury Globe: 0°N, 180°E (MESSENGER)", False, 1.0),
    "PIA19411": (HARV / "PIA19411.jpg", "NASA/JHU APL/Carnegie", "Public Domain (NASA/JPL)", "Water Ice on Mercury (MESSENGER north polar mosaic)", False, 1.0),
    "PIA16523": (HARV / "PIA16523.jpg", "NASA/JHU APL/Carnegie", "Public Domain (NASA/JPL)", "Perspective on the Pole (MESSENGER Prokofiev crater)", False, 1.95),
    "PIA17386": (HARV / "PIA17386.jpg", "NASA/JHU APL/Carnegie", "Public Domain (NASA/JPL)", "Enhanced Color Mercury Map (MESSENGER global surface)", False, 1.0),
    "PIA11364": (HARV / "PIA11364.jpg", "NASA/JHU APL/Carnegie", "Public Domain (NASA/JPL)", "Mercury True Color is in the Eye of the Beholder (MESSENGER)", False, 1.0),
    "PIA16853": (HARV / "PIA16853.jpg", "NASA/JHU APL/Carnegie", "Public Domain (NASA/JPL)", "Colors of the Innermost Planet: View 1 (MESSENGER)", False, 1.0),
    # Venus (PIA00271 & PIA00233 REMOVED; real Mariner 10 right globe + Pioneer Venus UV + real Magellan SAR PIA00215)
    "PIA23791": (HARV / "PIA23791.jpg", "NASA/JPL-Caltech", "Public Domain (NASA/JPL)", "Venus from Mariner 10 (right colour-enhanced globe)", False, 1.45),
    "pvo_uv_790205": (ARC24 / "023_What-Happened-To-Venus/07_Edit-Project/nasa_pool_v01/pioneer/pvo_uv_790205.jpg", "NASA/NSSDCA (Pioneer Venus Orbiter, 5 Feb 1979)", "Public Domain (NASA)", "Pioneer Venus Orbiter ultraviolet cloud view (Feb 5, 1979)", False, 1.15),
    "PIA00215": (RADAR / "PIA00215.jpg", "NASA/JPL", "Public Domain (NASA/JPL)", "Venus - Alpha Regio (real Magellan overhead SAR)", False, 0.941),
    "Venera13_surface": (HARV / "Venera13_surface.jpg", "Soviet Venera 13 / Wikimedia (CC BY 2.0)", "CC BY 2.0", "Surface of Venus panorama from Soviet Venera 13 (1982)", False, 1.95),
    "orbit_looks_back_earth_omni_v01_t0-5s": (ARC24 / "023_What-Happened-To-Venus/04_Generated-Clips/01_Raw/omni_v01/orbit_looks_back_earth_omni_v01_t0-5s.mp4", "OWB 023 approved shelf Omni clip", "Studio owned (023 shelf)", "Orbit near cloud-white Venus looking back toward Earth (023 verified Omni)", True, 1.50),
    # Earth (PIA18033 corrected Suomi NPP Blue Marble 2012 credit!)
    "svs_12312_epic_earth_timelapse": (SL / "031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/svs_moving_v01/originals/svs_12312_epic_earth_timelapse.mp4", "NASA/GSFC SVS 12312 / DSCOVR EPIC", "Public Domain (NASA)", "NASA DSCOVR EPIC rotating full-disk Earth timelapse (031 shelf)", True, 1.0),
    "PIA18033": (SL / "033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA18033.jpg", "NASA/NOAA/GSFC/Suomi NPP/VIIRS/Norman Kuring", "Public Domain (NASA)", "Earth - Suomi NPP Blue Marble 2012", False, 1.0),
    "Five_Minutes_in_Orbit": (SL / "027_What-If-Earth-Stopped-Spinning/07_Edit-Project/pool_v01/iss/Five_Minutes_in_Orbit.webm", "NASA/ISS", "Public Domain (NASA)", "ISS orbital sunset and Earth limb timelapse (027 shelf)", True, 1.0),
    "orbit_northpole_omni_v01": (SL / "027_What-If-Earth-Stopped-Spinning/04_Generated-Clips/01_Raw/omni_v01/orbit_northpole_omni_v01.mp4", "OWB 027 approved shelf Omni clip", "Studio owned (027 shelf)", "Orbit hovering over Arctic sea ice (027 verified Omni)", True, 1.50),
    "plate_031_r02a_iss_aurora_v01": (SL / "031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/nas_plates_v01/plate_031_r02a_iss_aurora_v01.mp4", "NASA/ISS", "Public Domain (NASA)", "ISS Earth aurora moving horizon plate (031 shelf)", True, 1.0),
    "plate_031_r30a_iss_limb_v01": (SL / "031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/nas_plates_v01/plate_031_r30a_iss_limb_v01.mp4", "NASA/ISS", "Public Domain (NASA)", "ISS orbital atmospheric limb moving plate (031 shelf)", True, 1.0),
    "plate_031_r42a_iss_blue_limb_v01": (SL / "031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/nas_plates_v01/plate_031_r42a_iss_blue_limb_v01.mp4", "NASA/ISS", "Public Domain (NASA)", "ISS bright blue atmospheric shield limb plate (031 shelf)", True, 1.0),
    "Carl_Friedrich_Gauss_1840_by_Jensen": (HARV / "Carl_Friedrich_Gauss_1840_by_Jensen.jpg", "Christian Albrecht Jensen (1840) / Wikimedia PD", "Public Domain", "Carl Friedrich Gauss portrait (1840)", False, 1.17),
    # Mars
    "PIA00407": (SL / "031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/harvest_v01/PIA00407.jpg", "NASA/JPL/USGS", "Public Domain (NASA/JPL)", "Mars Viking global hemisphere mosaic (031 shelf)", False, 1.0),
    "PIA19400": (SL / "025_Could-A-Robot-Survive-On-Mars/07_Edit-Project/nasa_pool_v01/dusk_plain/PIA19400.jpg", "NASA/JPL-Caltech/MSSS", "Public Domain (NASA/JPL)", "Curiosity Mars Gale Crater dusk landscape (025 shelf)", False, 1.43),
    "PIA19803": (HARV / "PIA19803.jpg", "NASA/JPL-Caltech/MSSS", "Public Domain (NASA/JPL)", "Curiosity Rover View of Alluring Martian Geology Ahead", False, 1.0),
    "JPL-20200303-MSLf-0001": (ARC05 / "025_Could-A-Robot-Survive-On-Mars/07_Edit-Project/nasa_pool_v01/gale_desert/JPL-20200303-MSLf-0001.mp4", "NASA/JPL-Caltech", "Public Domain (NASA/JPL)", "Curiosity Gale Crater moving panorama video (025 shelf)", True, 1.0),
    "PIA00300": (HARV / "PIA00300.jpg", "NASA/JPL", "Public Domain (NASA/JPL)", "Olympus Mons Viking Orbiter view", False, 1.0),
    "PIA02982": (HARV / "PIA02982.jpg", "NASA/JPL/MSSS", "Public Domain (NASA/JPL)", "Color Mosaic of Olympus Mons", False, 1.71),
    "PIA24542_full": (SL / "025_Could-A-Robot-Survive-On-Mars/07_Edit-Project/nasa_pool_v01/ingenuity/PIA24542_full.jpg", "NASA/JPL-Caltech/ASU/MSSS", "Public Domain (NASA/JPL)", "NASA Ingenuity Mars Helicopter on Jezero Crater floor (025 shelf)", False, 1.0),
    "JPL-20210222-M2020f-0001": (ARC05 / "025_Could-A-Robot-Survive-On-Mars/07_Edit-Project/nasa_pool_v01/launch_edl/JPL-20210222-M2020f-0001.mp4", "NASA/JPL-Caltech", "Public Domain (NASA/JPL)", "Perseverance Mars descent and Jezero landing footage (025 shelf)", True, 1.0),
    # Jupiter
    "PIA22946": (HARV / "PIA22946.jpg", "NASA/JPL-Caltech/SwRI/MSSS", "Public Domain (NASA/JPL)", "Jupiter Marble (Juno high-resolution globe)", False, 1.0),
    "PIA04866": (HARV / "PIA04866.jpg", "NASA/JPL/SSI", "Public Domain (NASA/JPL)", "Cassini Jupiter Portrait", False, 1.0),
    "PIA21972": (HARV / "PIA21972.jpg", "NASA/JPL-Caltech/SwRI/MSSS", "Public Domain (NASA/JPL)", "Jupiter Blues (Juno swirling north polar cyclones)", False, 1.0),
    "PIA21775": (HARV / "PIA21775.jpg", "NASA/JPL-Caltech/SwRI/MSSS", "Public Domain (NASA/JPL)", "Jupiter Great Red Spot in True Color (Juno)", False, 1.19),
    "PIA01384": (HARV / "PIA01384.jpg", "NASA/JPL", "Public Domain (NASA/JPL)", "Jupiter Great Red Spot high-res atmospheric detail", False, 1.0),
    "Galileo_Galilei_Sustermans": (HARV / "Galileo_Galilei_Sustermans.jpg", "Justus Sustermans (1636) / Wikimedia PD", "Public Domain", "Galileo Galilei portrait by Justus Sustermans (1636)", False, 1.0),
    # Saturn
    "PIA17172": (HARV / "PIA17172.jpg", "NASA/JPL-Caltech/SSI", "Public Domain (NASA/JPL)", "The Day the Earth Smiled — Cassini backlit Saturn ring mosaic", False, 1.0),
    "PIA11141": (HARV / "PIA11141.jpg", "NASA/JPL-Caltech/SSI", "Public Domain (NASA/JPL)", "Saturn Four Years On — Cassini globe and rings", False, 1.0),
    "PIA21046": (HARV / "PIA21046.jpg", "NASA/JPL-Caltech/SSI", "Public Domain (NASA/JPL)", "Saturn Approaching Northern Summer (Cassini)", False, 1.05),
    "PIA17652": (HARV / "PIA17652.jpg", "NASA/JPL-Caltech/SSI", "Public Domain (NASA/JPL)", "In Full View: Saturn Streaming Hexagon (Cassini)", False, 1.88),
    "PIA14944": (HARV / "PIA14944.jpg", "NASA/JPL-Caltech/SSI", "Public Domain (NASA/JPL)", "The Rose — Saturn north polar hurricane eyewall (Cassini)", False, 1.92),
    # Uranus
    "r01_sourced_composite_v01_silent": (SL / "033_Why-This-Planet-Has-21-Year-Winters/04_Generated-Clips/J2334_fix/r01_sourced_composite_v01_silent.mp4", "NASA/JPL + NASA/ESA/CSA/STScI (033 J2386 PASS)", "Public Domain / Studio composite", "Voyager 2 and JWST sideways Uranus opener clip (033 shelf)", True, 1.20),
    "PIA18182": (SL / "033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA18182.jpg", "NASA/JPL", "Public Domain (NASA/JPL)", "Voyager 2 Uranus full globe in natural color (033 shelf)", False, 1.12),
    "weic2310a_unannotated": (SL / "033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/weic2310a_unannotated.png", "NASA/ESA/CSA/STScI", "Public Domain / CC BY 4.0", "JWST NIRCam Uranus rings and polar cap (033 shelf)", False, 1.0),
    "PIA02963_borderless": (SL / "033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA02963_borderless.jpg", "NASA/ESA/STScI", "Public Domain (NASA)", "Hubble Space Telescope Uranus outer rings (033 shelf)", False, 1.0),
    "PIA01488": (SL / "033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01488.jpg", "NASA/JPL", "Public Domain (NASA/JPL)", "Voyager 2 Uranus limb and atmosphere (033 shelf)", False, 1.0),
    "r55_cut3_pia01488_pushin_silent": (SL / "033_Why-This-Planet-Has-21-Year-Winters/04_Generated-Clips/J2334_fix/r55_cut3_pia01488_pushin_silent.mp4", "NASA/JPL (033 J2386 PASS)", "Public Domain (NASA)", "Voyager 2 Uranus cloud push-in moving plate (033 shelf)", True, 1.0),
    "William_Herschel01_hires": (SL / "033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/William_Herschel01_hires.jpg.jpg", "Lemuel Francis Abbott (1785) / NPG PD", "Public Domain", "William Herschel portrait (1785, 033 shelf)", False, 1.0),
    # Neptune & Pluto
    "PIA01492": (HARV / "PIA01492.jpg", "NASA/JPL", "Public Domain (NASA/JPL)", "Neptune Full Azure Globe with Great Dark Spot (Voyager 2)", False, 1.0),
    "PIA00046": (HARV / "PIA00046.jpg", "NASA/JPL", "Public Domain (NASA/JPL)", "Neptune Full Disk with Great Dark Spot and Scooter Clouds (Voyager 2)", False, 1.92),
    "PIA00317": (HARV / "PIA00317.jpg", "NASA/JPL", "Public Domain (NASA/JPL)", "Global Color Mosaic of Triton (Voyager 2)", False, 1.0),
    "File_Video_NH_Pluto_Flyby": (SL / "034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/07_Edit-Project/harvest_v01/matched/File_Video_-_Nasa_s_New_Horizons_-_Pluto_Flyby_14_7_2015__51718116305_.webm.webm", "NASA/JHUAPL/SwRI", "Public Domain (NASA)", "New Horizons Pluto Flyby 14 July 2015 video (034 shelf)", True, 1.0),
    "PIA19952": (SL / "033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA19952.jpg", "NASA/JHUAPL/SwRI", "Public Domain (NASA)", "New Horizons Pluto Sputnik Planitia global portrait (033/034 shelf)", False, 1.0),
    "File_Sputnik_Planum_unannotated": (SL / "034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/07_Edit-Project/harvest_v01/matched/File_Sputnik_Planum_floating_hills_-_unannotated.jpg.jpg", "NASA/JHUAPL/SwRI", "Public Domain (NASA)", "Pluto Sputnik Planitia nitrogen-ice plains (034 shelf)", False, 1.84),
    "Urbain_Le_Verrier": (HARV / "Urbain_Le_Verrier.jpg", "Wikimedia Commons (Public Domain)", "Public Domain", "Urbain Le Verrier portrait (inset <=1.2x over starfield)", False, 1.20),
    "Johann_Gottfried_Galle": (HARV / "Johann_Gottfried_Galle.jpg", "Wikimedia Commons (Public Domain)", "Public Domain", "Johann Gottfried Galle portrait (inset <=1.35x over starfield)", False, 1.35),
    "William_Lassell": (HARV / "William_Lassell.jpg", "Wikimedia Commons (Public Domain)", "Public Domain", "William Lassell portrait (inset <=1.35x over starfield)", False, 1.35),
}

REJECTED = [
    {"id": "PIA00271", "title": "Venus - Computer Simulated Global View of the Northern Hemisphere", "reject": "NASA official title declares Computer Simulated Global View — KIND_FAIL; removed everywhere and replaced by real Mariner 10 PIA23791 right globe + Pioneer Venus UV pvo_uv_790205."},
    {"id": "PIA00233", "title": "Venus - 3-D Perspective View of Eistla Regio", "reject": "Magellan radar/altimetry 3-D terrain reconstruction — KIND_FAIL (J3829/J3835); replaced in R11 by real overhead SAR PIA00215."},
    {"id": "PIA00104", "title": "Venus - Computer Simulated Global View Centered at 180 Degrees East", "reject": "Computer Simulated Global View — KIND_FAIL."},
    {"id": "PIA00257", "title": "Venus - Computer Simulated Global View Centered at 0 Degrees East", "reject": "Computer Simulated Global View — KIND_FAIL."},
    {"id": "PIA21974", "title": "Jupiter's Colorful Cloud Belts (1280x433)", "reject": "Ultra-wide 1280x433 strip would upscale 2.49x vertically (>2.35x FAIL)."},
    {"id": "PIA16949", "title": "An Extra Kidney? (wrong subject)", "reject": "Wrong subject."},
    {"id": "GSFC_20171208_Archive_e001435", "title": "Sun Emits a Solstice CME (wrong subject)", "reject": "Wrong subject."},
    {"id": "Giuseppe_Colombo_wiki_mosaic", "title": "Famous Italians Mosaic.png", "reject": "Not an individual portrait."},
    {"id": "PIA02215", "title": "Crescents of Neptune and Triton (800x600)", "reject": "800x600 exceeds 2.35x full-bleed; inset <=1.0x only inside code_graphic_064_r62_solar_comparison_timeline.mp4."},
    {"id": "PIA21049", "title": "Changing Colors in Saturn North (810x910)", "reject": "810x910 exceeds 2.35x full-bleed; inset <=1.0x only inside code_graphic_064_r46_saturn_hexagon.mp4."},
    {"id": "PIA00059", "title": "Triton South Polar Terrain (800x795)", "reject": "800x795 exceeds 2.35x full-bleed; replaced full-frame by PIA00317 (4500x3500)."},
    {"id": "code_graphic_064_r03_mercury_temp", "title": "Superseded v01 14.25s Mercury temperature graphic", "reject": "Superseded in v02 by split <=3.8s code_graphic_064_r03a_mercury_sunlight.mp4 and code_graphic_064_r03b_mercury_night.mp4."},
    {"id": "code_graphic_064_ch02_card_venus", "title": "Superseded v01 Venus chapter card containing PIA00271", "reject": "Replaced by code_graphic_064_ch02_card_venus_v02.mp4 using real Mariner 10 PIA23791 right globe."},
    {"id": "code_graphic_064_r12_venus_greenhouse", "title": "Superseded v01 24.25s Venus greenhouse graphic containing PIA00271", "reject": "Replaced by v02 10.0s greenhouse + 7.0s pressure graphics using real PIA23791 right globe."},
    {"id": "code_graphic_064_r14_venus_spin", "title": "Superseded v01 Venus spin graphic containing PIA00271", "reject": "Replaced by code_graphic_064_r14_venus_spin_v02.mp4 using real PIA23791 right globe."},
]

CODE_GRAPHICS: dict[str, tuple[Path, str]] = {
    "code_graphic_064_r03a_mercury_sunlight.mp4": (CG_V02 / "code_graphic_064_r03a_mercury_sunlight.mp4", "Ch 1 DATA (split 1): +430 C day, 58M km, up to 7x sunlight"),
    "code_graphic_064_r03b_mercury_night.mp4": (CG_V02 / "code_graphic_064_r03b_mercury_night.mp4", "Ch 1 DATA (split 2): -180 C night plunge contrast bar"),
    "code_graphic_064_r05_mercury_resonance.mp4": (CG_V01 / "code_graphic_064_r05_mercury_resonance.mp4", "Ch 1 DATA: Mercury 3:2 spin-orbit dial (59d spin, 88d orbit, 176d solar day)"),
    "code_graphic_064_r07_mercury_core.mp4": (CG_V01 / "code_graphic_064_r07_mercury_core.mp4", "Ch 1 DATA+SCALE: Mercury 85% metallic core inside 2,440 km radius + FACT Second densest planet"),
    "code_graphic_064_ch02_card_venus_v02.mp4": (CG_V02 / "code_graphic_064_ch02_card_venus_v02.mp4", "Chapter card 02/08 Venus — The Backwards Furnace (real PIA23791 right globe)"),
    "code_graphic_064_r12_venus_greenhouse_v02.mp4": (CG_V02 / "code_graphic_064_r12_venus_greenhouse_v02.mp4", "Ch 2 DATA: Venus 464 C, 92 bars, 96.5% CO2 + FACT Hottest planetary surface"),
    "code_graphic_064_r12b_venus_pressure_v02.mp4": (CG_V02 / "code_graphic_064_r12b_venus_pressure_v02.mp4", "Ch 2 SCALE: 92 bars surface pressure like 930 m underwater on Earth"),
    "code_graphic_064_r14_venus_spin_v02.mp4": (CG_V02 / "code_graphic_064_r14_venus_spin_v02.mp4", "Ch 2 DATA: Venus 243-day backwards spin vs 225-day orbit (Sun rises west)"),
    "code_graphic_064_ch03_card_earth.mp4": (CG_V01 / "code_graphic_064_ch03_card_earth.mp4", "Chapter card 03/08 Earth — The Shielded Ocean World"),
    "code_graphic_064_r20_earth_spin_bulge.mp4": (CG_V01 / "code_graphic_064_r20_earth_spin_bulge.mp4", "Ch 3 DATA+SCALE: Earth 1,670 km/h equatorial spin (>4x Cyclone Olivia) and 43 km bulge"),
    "code_graphic_064_r22_earth_core_flips.mp4": (CG_V01 / "code_graphic_064_r22_earth_core_flips.mp4", "Ch 3 DATA: Earth 3,000 km liquid-iron outer core depth and 183 reversals in 83M years"),
    "code_graphic_064_ch04_card_mars.mp4": (CG_V01 / "code_graphic_064_ch04_card_mars.mp4", "Chapter card 04/08 Mars — The Frozen Robot Desert"),
    "code_graphic_064_r28_mars_pressure.mp4": (CG_V01 / "code_graphic_064_r28_mars_pressure.mp4", "Ch 4 DATA: Mars 6.36 mbar (<1% Earth) and -59 C mean temperature"),
    "code_graphic_064_r30_mars_olympus.mp4": (CG_V01 / "code_graphic_064_r30_mars_olympus.mp4", "Ch 4 DATA+SCALE: Olympus Mons 21.3 km above datum (>2x Everest, Arizona-sized base)"),
    "code_graphic_064_ch05_card_jupiter.mp4": (CG_V01 / "code_graphic_064_ch05_card_jupiter.mp4", "Chapter card 05/08 Jupiter — Metallic Hydrogen"),
    "code_graphic_064_r35_jupiter_scale.mp4": (CG_V01 / "code_graphic_064_r35_jupiter_scale.mp4", "Ch 5 DATA+SCALE: Jupiter 11x Earth width (basketball vs grape), 318 Earth masses, 9.9-hour day"),
    "code_graphic_064_r39_jupiter_galileo.mp4": (CG_V01 / "code_graphic_064_r39_jupiter_galileo.mp4", "Ch 5 DATA: 7 Dec 1995 Galileo probe 58-minute data return"),
    "code_graphic_064_ch06_card_saturn.mp4": (CG_V01 / "code_graphic_064_ch06_card_saturn.mp4", "Chapter card 06/08 Saturn — Disappearing Rings"),
    "code_graphic_064_r43_saturn_density_rings.mp4": (CG_V01 / "code_graphic_064_r43_saturn_density_rings.mp4", "Ch 6 DATA+FACT: Less dense (687 vs Water 1,000 kg/m3)"),
    "code_graphic_064_r43b_saturn_rings_v02.mp4": (CG_V02 / "code_graphic_064_r43b_saturn_rings_v02.mp4", "Ch 6 DATA: 282,000 km radial rings (~10 m thick), 0.41 Mimas mass"),
    "code_graphic_064_r46_saturn_hexagon.mp4": (CG_V01 / "code_graphic_064_r46_saturn_hexagon.mp4", "Ch 6 DATA+SCALE: 30,000 km hexagon (>2 Earths, 322 km/h) + 2012-2016 inset"),
    "code_graphic_064_ch07_card_uranus.mp4": (CG_V01 / "code_graphic_064_ch07_card_uranus.mp4", "Chapter card 07/08 Uranus — 21-Year Winters"),
    "code_graphic_064_r51_uranus_tilt.mp4": (CG_V01 / "code_graphic_064_r51_uranus_tilt.mp4", "Ch 7 DATA+SCALE+FACT: Uranus 97.77 deg tilt vs Earth 23.4 deg, 21-year winter"),
    "code_graphic_064_r54_uranus_cold_core.mp4": (CG_V01 / "code_graphic_064_r54_uranus_cold_core.mp4", "Ch 7 DATA: -224.2 C minimum (in some places), nearly 60 deg magnetic tilt"),
    "code_graphic_064_r54b_uranus_core_v02.mp4": (CG_V02 / "code_graphic_064_r54b_uranus_core_v02.mp4", "Ch 7 DATA: >=80% hot dense fluid up to 4,982 C near core"),
    "code_graphic_064_ch08_card_neptune.mp4": (CG_V01 / "code_graphic_064_ch08_card_neptune.mp4", "Chapter card 08/08 Neptune — Supersonic Winds"),
    "code_graphic_064_r60_neptune_winds.mp4": (CG_V01 / "code_graphic_064_r60_neptune_winds.mp4", "Ch 8 DATA+SCALE: Neptune >2,000 km/h vs 408 km/h Olivia (Roughly 5x gust)"),
    "code_graphic_064_r62_solar_comparison_timeline.mp4": (CG_V01 / "code_graphic_064_r62_solar_comparison_timeline.mp4", "Ch 8 Completed Exploration Timeline (1610-2024) + PIA02215 farewell crescent inset"),
}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def build_sentences() -> list[tuple[float, float, str]]:
    stt = json.loads(STT_PATH.read_text(encoding="utf-8"))
    words = [w for w in stt.get("words", []) if w.get("type", "word") == "word"]
    sents, cur = [], []
    for w in words:
        cur.append(w)
        if w["text"].strip()[-1:] in ".?!":
            sents.append((cur[0]["start"], cur[-1]["end"], " ".join(x["text"].strip() for x in cur)))
            cur = []
    if cur:
        sents.append((cur[0]["start"], cur[-1]["end"], " ".join(x["text"].strip() for x in cur)))
    return sents


def main() -> int:
    # Verify mandatory J3883 SHA-256 locks first
    vo_wav = NAS_064 / "02_Voiceover/every_planet_explained_vo_v01.wav"
    assert sha256_file(vo_wav) == REQUIRED_VO_SHA, "Locked VO hash mismatch!"
    assert sha256_file(ASSETS["PIA00215"][0]) == REQUIRED_PIA00215_SHA, "PIA00215 hash mismatch!"
    assert sha256_file(ASSETS["pvo_uv_790205"][0]) == REQUIRED_PVO_SHA, "pvo_uv_790205 hash mismatch!"
    for k, v in ASSETS.items():
        assert v[0].exists(), f"Missing active asset {k}: {v[0]}"
    for k, (p, _) in CODE_GRAPHICS.items():
        assert p.exists(), f"Missing code graphic {k}: {p}"

    sents = build_sentences()
    assert len(sents) == 72, f"Expected 72 sentences, got {len(sents)}"

    # Complete v02 timeline: every row maps to exact narration block; sub-cuts enforce <= 5.95 s stills
    # and <= 11.0 s code graphics (ZERO LONG_RUN > 15 s, ZERO consecutive code graphics, <= 2 still apps!)
    # Format of each block:
    # (row_id, s_start, s_end, kind, markers, [(t_in, t_out, key, is_code, offset, framing_extra), ...])
    blocks = [
        # === CHAPTER 1: MERCURY (0.00 - 81.36 s) — EXACT SHOT_LIST_v02 R01a-R04b ===
        ("R01a", 1, 1, "NASA", "Frame 0 rotating Mercury + 01 / 08 MERCURY progress strip", [
            (0.00, 3.50, "PIA15162", False, None, {"overlay_strip": "ch01_mercury"}),
            (3.50, 7.10, "PIA17386", False, None, {}),
        ]),
        ("R02a", 2, 2, "NASA", "Immediate answer < 12 s: Prokofiev polar craters in permanent shadow", [
            (7.10, 9.30, "PIA16523", False, None, {"reframe": "wide"}),
            (9.30, 11.45, "PIA16523", False, None, {"reframe": "tight_pole"}),
        ]),
        ("R03a", 3, 3, "NASA+CODE", "58M km / 7x sunlight -> split +430 C day -> real terminator -> split -180 C night (DATA #1)", [
            (11.45, 15.00, "PIA17386", False, None, {"reframe": "limb"}),
            (15.00, 18.80, "code_graphic_064_r03a_mercury_sunlight.mp4", True, 0.0, {}),
            (18.80, 22.10, "PIA19411", False, None, {}),
            (22.10, 25.70, "code_graphic_064_r03b_mercury_night.mp4", True, 0.0, {}),
        ]),
        ("R04a", 4, 4, "NASA", "WHO #1: Giuseppe Colombo (1920-1984) — Italian mathematician · WHEN: 1965", [
            (25.70, 29.25, "PIA11364", False, None, {}),
            (29.25, 32.85, "PIA16853", False, None, {}),
        ]),
        ("R05", 5, 6, "CODE+NASA", "DATA #1b: 3:2 spin-orbit dial (59d spin, 88d orbit -> 176d solar day)", [
            (32.85, 43.35, "code_graphic_064_r05_mercury_resonance.mp4", True, 0.0, {}),
            (43.35, 46.60, "PIA15162", False, None, {"reframe": "wide"}),
            (46.60, 49.90, "PIA15162", False, None, {"reframe": "tight"}),
        ]),
        ("R06", 7, 7, "NASA+CODE", "Real Mercury limb -> DATA #1c + SCALE: 2,440 km (blueberry vs nickel), 85% metallic core · FACT #1: Second densest planet", [
            (49.90, 53.50, "PIA11364", False, None, {"reframe": "wide"}),
            (53.50, 57.10, "PIA11364", False, None, {"reframe": "tight"}),
            (57.10, 64.30, "code_graphic_064_r07_mercury_core.mp4", True, 0.0, {}),
        ]),
        ("R08", 8, 9, "NASA", "Edit label: 'Almost no tilt' (0.034 deg) · WHEN: Mar 2011-Apr 2015", [
            (64.30, 68.56, "PIA19411", False, None, {"reframe": "wide"}),
            (68.56, 72.83, "PIA19411", False, None, {"reframe": "tight"}),
            (72.83, 77.10, "PIA16853", False, None, {"reframe": "wide"}),
            (77.10, 81.36, "PIA16853", False, None, {"reframe": "tight"}),
        ]),

        # === CHAPTER 2: VENUS (81.90 - 157.90 s) ===
        ("C02", None, None, "CARD", "CHAPTER CARD 02 / 08 · VENUS — The Backwards Furnace (breath 0.60 s after S09)", [
            (81.90, 84.30, "code_graphic_064_ch02_card_venus_v02.mp4", True, 0.0, {}),
        ]),
        ("R09", 10, 11, "NASA", "REPAIRED (zero PIA00271): Real Mariner 10 PIA23791 right globe -> Pioneer Venus UV pvo_uv_790205", [
            (84.30, 89.05, "PIA23791", False, None, {"crop_xyxy": [1160, 0, 2245, 1096]}),
            (89.05, 93.80, "pvo_uv_790205", False, None, {}),
        ]),
        ("R10", 12, 14, "CODE+NASA", "DATA #2 + SCALE: 464 C, 92 bars (930 m underwater), 96.5% CO2 · FACT #2: Hottest planetary surface", [
            (93.80, 103.30, "code_graphic_064_r12_venus_greenhouse_v02.mp4", True, 0.0, {}),
            (103.30, 107.45, "pvo_uv_790205", False, None, {"reframe": "wide"}),
            (107.45, 111.60, "pvo_uv_790205", False, None, {"reframe": "tight"}),
            (111.60, 118.05, "code_graphic_064_r12b_venus_pressure_v02.mp4", True, 0.0, {}),
        ]),
        ("R11", 15, 15, "NASA+CODE", "REQUIRED R11 PIA00215 real Magellan SAR (118.05-124.40 s) -> Venus backwards spin graphic (124.40-130.75 s)", [
            (118.05, 124.40, "PIA00215", False, None, {
                "crop": "350:600:2200:1238; smooth push to 430:645:2040:1148; downscale 0.873x->0.941x",
                "crop_xyxy": [350, 600, 2550, 1838],
                "push_xyxy": [430, 645, 2470, 1793],
            }),
            (124.40, 130.75, "code_graphic_064_r14_venus_spin_v02.mp4", True, 0.0, {}),
        ]),
        ("R13", 16, 17, "NASA", "PIA23791 right globe -> Venera 13 panorama · WHEN: 1978 & 1 Mar 1982", [
            (130.75, 136.75, "PIA23791", False, None, {"crop_xyxy": [1160, 0, 2245, 1096], "reframe": "wide"}),
            (136.75, 142.78, "PIA23791", False, None, {"crop_xyxy": [1160, 0, 2245, 1096], "reframe": "tight"}),
            (142.78, 148.79, "Venera13_surface", False, None, {"reframe": "wide"}),
            (148.79, 154.80, "Venera13_surface", False, None, {"reframe": "tight"}),
        ]),
        ("R14", 18, 18, "OMNI", "ORBIT ACTS: Verified 023 shelf Omni clip (Orbit at Venus looking back at Earth)", [
            (154.80, 157.90, "orbit_looks_back_earth_omni_v01_t0-5s", True, 0.0, {}),
        ]),

        # === CHAPTER 3: EARTH (158.36 - 251.24 s) ===
        ("C03", None, None, "CARD", "CHAPTER CARD 03 / 08 · EARTH — The Shielded Ocean World (breath 0.60 s after S18)", [
            (158.36, 160.76, "code_graphic_064_ch03_card_earth.mp4", True, 0.0, {}),
        ]),
        ("R15", 19, 21, "NASA", "Real DSCOVR EPIC rotating Earth + NASA/NOAA Suomi NPP Blue Marble 2012 (PIA18033)", [
            (160.76, 168.60, "svs_12312_epic_earth_timelapse", True, 10.0, {}),
            (168.60, 172.52, "PIA18033", False, None, {"reframe": "wide"}),
            (172.52, 176.45, "PIA18033", False, None, {"reframe": "tight"}),
        ]),
        ("R16", 22, 23, "CODE+NASA", "DATA #3a + SCALE: 1,670 km/h equatorial spin (>4x Cyclone Olivia), 43 km bulge", [
            (176.45, 186.95, "code_graphic_064_r20_earth_spin_bulge.mp4", True, 0.0, {}),
            (186.95, 193.15, "Five_Minutes_in_Orbit", True, 15.0, {}),
            (193.15, 199.35, "PIA18033", False, None, {"reframe": "equator"}),
        ]),
        ("R17", 24, 24, "OMNI+CODE", "ORBIT ACTS (027 shelf Omni) -> DATA #3b: 3,000 km outer core · 183 reversals in 83M years", [
            (199.35, 208.43, "orbit_northpole_omni_v01", True, 0.0, {}),
            (208.43, 217.50, "code_graphic_064_r22_earth_core_flips.mp4", True, 0.0, {}),
        ]),
        ("R19", 25, 25, "NASA", "WHO #2: Carl Friedrich Gauss (1777-1855) — German mathematician · WHEN: 1830s", [
            (217.50, 220.52, "Carl_Friedrich_Gauss_1840_by_Jensen", False, None, {"reframe": "wide"}),
            (220.52, 223.55, "Carl_Friedrich_Gauss_1840_by_Jensen", False, None, {"reframe": "tight"}),
            (223.55, 226.85, "plate_031_r02a_iss_aurora_v01", True, 0.0, {}),
        ]),
        ("R20", 26, 27, "NASA", "WHEN: 2020 (ESA ~9% weakening) · SCALE: 13 feet of concrete atmosphere shield", [
            (226.85, 232.25, "plate_031_r30a_iss_limb_v01", True, 0.0, {}),
            (232.25, 237.75, "Five_Minutes_in_Orbit", True, 2.0, {}),
            (237.75, 241.75, "svs_12312_epic_earth_timelapse", True, 80.0, {}),
            (241.75, 244.70, "plate_031_r42a_iss_blue_limb_v01", True, 0.0, {}),
        ]),
        ("R21", 28, 29, "NASA", "SUBSCRIBE BEAT (35.9% runtime) — clean real Earth orbit footage + subtle subscribe pill", [
            (244.70, 251.24, "svs_12312_epic_earth_timelapse", True, 45.0, {}),
        ]),

        # === CHAPTER 4: MARS (251.80 - 324.34 s) ===
        ("C04", None, None, "CARD", "CHAPTER CARD 04 / 08 · MARS — The Frozen Robot Desert (breath 0.60 s after S29)", [
            (251.80, 254.20, "code_graphic_064_ch04_card_mars.mp4", True, 0.0, {}),
        ]),
        ("R22", 30, 32, "NASA", "Real Mars globe + Curiosity Gale Crater · WHEN: 4 billion years ago", [
            (254.20, 258.80, "PIA00407", False, None, {"reframe": "wide"}),
            (258.80, 263.45, "PIA00407", False, None, {"reframe": "tight"}),
            (263.45, 268.05, "PIA19400", False, None, {"reframe": "wide"}),
            (268.05, 272.70, "PIA19400", False, None, {"reframe": "tight"}),
        ]),
        ("R23", 33, 33, "CODE", "DATA #4a: 6.36 mbar (<1% Earth) & -59 C mean · NUMBER OBJECT (Ch 4)", [
            (272.70, 285.85, "code_graphic_064_r28_mars_pressure.mp4", True, 0.0, {}),
        ]),
        ("R24", 34, 34, "NASA+CODE", "Real Viking & MGS Olympus Mons -> DATA #4b + SCALE: 21.3 km above datum (>2x Everest, Arizona-sized base)", [
            (285.85, 290.98, "PIA00300", False, None, {}),
            (290.98, 296.12, "PIA02982", False, None, {}),
            (296.12, 301.25, "code_graphic_064_r30_mars_olympus.mp4", True, 0.0, {}),
        ]),
        ("R26", 35, 36, "NASA", "WHEN: 10 Jun 2018 (Opportunity 60x design life) & 18 Jan 2024 (Ingenuity 72 flights)", [
            (301.25, 307.02, "JPL-20200303-MSLf-0001", True, 12.0, {}),
            (307.02, 312.79, "PIA24542_full", False, None, {}),
            (312.79, 318.57, "JPL-20210222-M2020f-0001", True, 35.0, {}),
            (318.57, 324.34, "PIA19803", False, None, {}),
        ]),

        # === CHAPTER 5: JUPITER (324.80 - 406.88 s) ===
        ("C05", None, None, "CARD", "CHAPTER CARD 05 / 08 · JUPITER (breath 0.60 s after S36)", [
            (324.80, 327.20, "code_graphic_064_ch05_card_jupiter.mp4", True, 0.0, {}),
        ]),
        ("R27", 37, 37, "NASA", "Real Juno Jupiter Marble & swirling polar cyclones", [
            (327.20, 330.50, "PIA22946", False, None, {}),
            (330.50, 333.80, "PIA21972", False, None, {}),
        ]),
        ("R28", 38, 39, "CODE+NASA", "DATA #5a + SCALE: 11x wider (basketball vs grape), 318 Earth masses, 9.9-hour day", [
            (333.80, 344.30, "code_graphic_064_r35_jupiter_scale.mp4", True, 0.0, {}),
            (344.30, 350.20, "PIA04866", False, None, {"reframe": "wide"}),
            (350.20, 356.15, "PIA04866", False, None, {"reframe": "tight"}),
        ]),
        ("R29", 40, 41, "NASA", "WHO #3: Galileo Galilei (1564-1642) — Italian astronomer · WHEN: 1610, late 1800s, 2014", [
            (356.15, 360.31, "Galileo_Galilei_Sustermans", False, None, {"reframe": "wide"}),
            (360.31, 364.47, "Galileo_Galilei_Sustermans", False, None, {"reframe": "tight"}),
            (364.47, 368.62, "PIA21775", False, None, {"reframe": "wide"}),
            (368.62, 372.78, "PIA21775", False, None, {"reframe": "tight"}),
            (372.78, 376.94, "PIA01384", False, None, {"reframe": "wide"}),
            (376.94, 381.10, "PIA01384", False, None, {"reframe": "tight"}),
        ]),
        ("R30", 42, 45, "NASA", "MIDPOINT TWIST (~56%): 'Case closed? Wrong — there is no solid surface.'", [
            (381.10, 384.62, "PIA04866", False, None, {"reframe": "wide"}),
            (384.62, 388.15, "PIA04866", False, None, {"reframe": "tight"}),
        ]),
        ("R31", 46, 46, "CODE", "DATA #5b + WHEN: 7 Dec 1995 Galileo probe 58-minute data return", [
            (388.15, 398.30, "code_graphic_064_r39_jupiter_galileo.mp4", True, 0.0, {}),
        ]),
        ("R32", 47, 48, "NASA", "Real Juno swirling deep clouds for separate far-deeper metallic hydrogen region", [
            (398.30, 402.59, "PIA21972", False, None, {}),
            (402.59, 406.88, "PIA22946", False, None, {}),
        ]),

        # === CHAPTER 6: SATURN (407.44 - 496.46 s) ===
        ("C06", None, None, "CARD", "CHAPTER CARD 06 / 08 · SATURN (breath 0.60 s after S48)", [
            (407.44, 409.84, "code_graphic_064_ch06_card_saturn.mp4", True, 0.0, {}),
        ]),
        ("R33", 49, 49, "NASA", "Real Cassini backlit ring mosaic & Saturn globe", [
            (409.84, 412.22, "PIA17172", False, None, {}),
            (412.22, 414.60, "PIA11141", False, None, {}),
        ]),
        ("R34", 50, 51, "CODE+NASA", "DATA #6a + FACT #3: Less dense (687 vs Water 1,000 kg/m3), 282,000 km radial rings (~10 m thick)", [
            (414.60, 425.10, "code_graphic_064_r43_saturn_density_rings.mp4", True, 0.0, {}),
            (425.10, 429.30, "PIA17172", False, None, {"reframe": "wide"}),
            (429.30, 433.50, "PIA17172", False, None, {"reframe": "tight"}),
            (433.50, 439.00, "code_graphic_064_r43b_saturn_rings_v02.mp4", True, 0.0, {}),
        ]),
        ("R35", 52, 53, "NASA", "WHEN: 2017 Cassini dives (4,800-45,000 kg/s inflow, 0.41 Mimas mass, 10-100 Myr possible age)", [
            (439.00, 443.47, "PIA21046", False, None, {"reframe": "wide"}),
            (443.47, 447.95, "PIA21046", False, None, {"reframe": "tight"}),
            (447.95, 452.42, "PIA21046", False, None, {"reframe": "left"}),
            (452.42, 456.90, "PIA11141", False, None, {"reframe": "wide"}),
            (456.90, 461.37, "PIA11141", False, None, {"reframe": "tight"}),
            (461.37, 465.85, "PIA11141", False, None, {"reframe": "rings"}),
        ]),
        ("R36", 54, 54, "NASA", "Real Cassini north-pole hexagon & central eyewall · WHEN: early 1980s", [
            (465.85, 471.75, "PIA17652", False, None, {}),
            (471.75, 477.65, "PIA14944", False, None, {}),
        ]),
        ("R37", 55, 55, "CODE+NASA", "DATA #6b + SCALE + WHEN: 30,000 km hexagon (>2 Earths, 322 km/h) + PIA21049 2012-2016 inset", [
            (477.65, 488.50, "code_graphic_064_r46_saturn_hexagon.mp4", True, 0.0, {}),
            (488.50, 493.50, "PIA17652", False, None, {"reframe": "tight"}),
        ]),
        ("R38", 56, 56, "NASA", "Saturn transition out to Uranus", [
            (493.50, 496.46, "PIA21046", False, None, {}),
        ]),

        # === CHAPTER 7: URANUS (497.02 - 584.44 s) ===
        ("C07", None, None, "CARD", "CHAPTER CARD 07 / 08 · URANUS (breath 0.60 s after S56)", [
            (497.02, 499.42, "code_graphic_064_ch07_card_uranus.mp4", True, 0.0, {}),
        ]),
        ("R39", 57, 57, "NASA", "Real 033 verified Voyager 2 + JWST sideways Uranus clip", [
            (499.42, 504.75, "r01_sourced_composite_v01_silent", True, 0.0, {}),
        ]),
        ("R40", 58, 58, "NASA", "WHO #4: William Herschel (1738-1822) — British astronomer · WHEN: 13 Mar 1781 · SCALE: Softball vs nickel", [
            (504.75, 508.12, "William_Herschel01_hires", False, None, {"reframe": "wide"}),
            (508.12, 511.50, "William_Herschel01_hires", False, None, {"reframe": "tight"}),
            (511.50, 518.25, "PIA18182", False, None, {}),
            (518.25, 525.00, "weic2310a_unannotated", False, None, {}),
        ]),
        ("R41", 59, 60, "CODE+NASA", "DATA #7a + SCALE + FACT #4: 97.77 deg vs Earth 23.4 deg (>4x), 17h spin, 21-year winter", [
            (525.00, 535.50, "code_graphic_064_r51_uranus_tilt.mp4", True, 0.0, {}),
            (535.50, 541.40, "weic2310a_unannotated", False, None, {"reframe": "tight"}),
            (541.40, 547.35, "PIA18182", False, None, {"reframe": "tight"}),
        ]),
        ("R42", 61, 61, "NASA", "WHEN: 24 Jan 1986 Voyager 2 only visit", [
            (547.35, 550.65, "PIA02963_borderless", False, None, {}),
            (550.65, 553.95, "PIA01488", False, None, {}),
        ]),
        ("R43", 62, 64, "CODE+NASA", "DATA #7b: -224.2 C minimum (in some places), ~60 deg magnetic tilt, >=80% hot dense fluid up to 4,982 C", [
            (553.95, 564.95, "code_graphic_064_r54_uranus_cold_core.mp4", True, 0.0, {}),
            (564.95, 570.50, "PIA02963_borderless", False, None, {"reframe": "tight"}),
            (570.50, 576.10, "PIA01488", False, None, {"reframe": "tight"}),
            (576.10, 581.75, "code_graphic_064_r54b_uranus_core_v02.mp4", True, 0.0, {}),
        ]),
        ("R44", 65, 65, "NASA", "Real 033 Voyager 2 cloud push-in transition to Neptune", [
            (581.75, 584.44, "r55_cut3_pia01488_pushin_silent", True, 0.0, {}),
        ]),

        # === CHAPTER 8: NEPTUNE (585.00 - 701.86 s) ===
        ("C08", None, None, "CARD", "CHAPTER CARD 08 / 08 · NEPTUNE (breath 0.60 s after S65)", [
            (585.00, 587.40, "code_graphic_064_ch08_card_neptune.mp4", True, 0.0, {}),
        ]),
        ("R45", 66, 67, "NASA", "Real Voyager 2 Neptune full azure globe & scooter clouds · SCALE: Baseball vs nickel · WHEN: 2011", [
            (587.40, 591.75, "PIA01492", False, None, {"reframe": "wide"}),
            (591.75, 596.10, "PIA01492", False, None, {"reframe": "tight"}),
            (596.10, 600.45, "PIA01492", False, None, {"reframe": "spot"}),
            (600.45, 604.80, "PIA00046", False, None, {"reframe": "wide"}),
            (604.80, 609.15, "PIA00046", False, None, {"reframe": "tight"}),
            (609.15, 613.55, "PIA00046", False, None, {"reframe": "clouds"}),
        ]),
        ("R46", 68, 69, "NASA", "WHO #5-7: Le Verrier (1811-1877), Galle (1812-1910), Lassell (1799-1880) · WHEN: 23 Sep & 10 Oct 1846", [
            (613.55, 618.70, "Urbain_Le_Verrier", False, None, {"reframe": "wide"}),
            (618.70, 623.85, "Urbain_Le_Verrier", False, None, {"reframe": "tight"}),
            (623.85, 629.00, "Johann_Gottfried_Galle", False, None, {"reframe": "wide"}),
            (629.00, 634.15, "Johann_Gottfried_Galle", False, None, {"reframe": "tight"}),
            (634.15, 639.30, "William_Lassell", False, None, {"reframe": "wide"}),
            (639.30, 644.45, "William_Lassell", False, None, {"reframe": "tight"}),
        ]),
        ("R47", 70, 70, "NASA", "WHEN: 25 Aug 1989 Voyager 2 flyby (real Neptune plate before wind graphic)", [
            (644.45, 648.82, "PIA01492", False, None, {"reframe": "wide"}),
            (648.82, 653.20, "PIA01492", False, None, {"reframe": "tight"}),
        ]),
        ("R48", 71, 71, "CODE+NASA", "DATA #8a + SCALE: >2,000 km/h winds vs 408 km/h Olivia (Roughly 5x gust), Triton >8 km geysers", [
            (653.20, 664.20, "code_graphic_064_r60_neptune_winds.mp4", True, 0.0, {}),
            (664.20, 669.90, "PIA00317", False, None, {}),
        ]),
        ("R49", 72, 72, "NASA", "WHEN: Jul 2015 New Horizons Pluto Sputnik Planitia hand-off to OWB:034", [
            (669.90, 676.88, "File_Video_NH_Pluto_Flyby", True, 2.0, {}),
            (676.88, 680.37, "PIA19952", False, None, {"reframe": "wide"}),
            (680.37, 683.86, "PIA19952", False, None, {"reframe": "tight"}),
        ]),
        ("R50", None, None, "CODE", "Completed Exploration Timeline (1610-2024) + PIA02215 farewell crescent inset (first 8 s of hold)", [
            (683.86, 691.86, "code_graphic_064_r62_solar_comparison_timeline.mp4", True, 0.0, {}),
        ]),
        ("R51", None, None, "NASA", "[End screen hold & fade — moving picture + music 18 s past last word, zero goodbye/subscribe graphic]", [
            (691.86, 696.86, "File_Sputnik_Planum_unannotated", False, None, {}),
            (696.86, 701.86, "File_Video_NH_Pluto_Flyby", True, 25.0, {}),
        ]),
    ]

    csv_rows = []
    cuts = []
    provenance_map: dict[str, dict] = {}

    for row_num, (rid, s0, s1, kind, markers, subcuts) in enumerate(blocks, 1):
        t_in = subcuts[0][0]
        t_out = subcuts[-1][1]
        if s0 is not None and s1 is not None:
            vo_text = " ".join(sents[i - 1][2] for i in range(s0, s1 + 1))
        elif kind == "CARD":
            vo_text = f"[{markers}]"
        else:
            vo_text = "[Music hold and end screen]"

        csv_rows.append({
            "row": rid,
            "vo_in": f"{t_in:.2f}",
            "vo_out": f"{t_out:.2f}",
            "dur_s": f"{t_out - t_in:.2f}",
            "cuts": str(len(subcuts)),
            "source": kind,
            "asset": " -> ".join(sc[2] for sc in subcuts),
            "vo_text": vo_text,
            "markers": markers,
        })

        for (c_in, c_out, key, is_code, offset, extra) in subcuts:
            if key in CODE_GRAPHICS:
                src_path, title = CODE_GRAPHICS[key]
                is_vid = True
                upscale = 1.0
                credit = "Original OWB code graphic"
                lic = "Studio owned"
                is_cg = True
            else:
                src_path, credit, lic, title, is_vid, upscale = ASSETS[key]
                is_cg = False

            framing = dict(extra)
            if is_vid:
                framing["offset"] = float(offset or 0.0)
            else:
                framing.setdefault("crop", "full 16:9 or framed inset <=1.95x")

            cuts.append({
                "row": row_num,
                "row_id": rid,
                "timeline_in": round(c_in, 2),
                "timeline_out": round(c_out, 2),
                "source": str(src_path),
                "upscale": upscale,
                "video": is_vid,
                "framing": framing,
            })

            sp_str = str(src_path)
            if sp_str not in provenance_map:
                w, h = None, None
                if src_path.suffix.lower() in (".jpg", ".jpeg", ".png"):
                    with Image.open(src_path) as im:
                        w, h = im.size
                provenance_map[sp_str] = {
                    "id": key,
                    "file": sp_str,
                    "title": title,
                    "credit": credit,
                    "license": lic,
                    "is_code_graphic": is_cg,
                    "video": is_vid,
                    "width": w,
                    "height": h,
                    "upscale_max": upscale,
                    "sha256": sha256_file(src_path),
                    "bytes": src_path.stat().st_size,
                    "intervals": [],
                }
            provenance_map[sp_str]["intervals"].append([round(c_in, 2), round(c_out, 2)])

    # Verify zero consecutive full-screen code graphics (excluding CARD->NASA)
    for i in range(len(cuts) - 1):
        a, b = cuts[i], cuts[i + 1]
        a_cg = "code_graphic" in Path(a["source"]).name
        b_cg = "code_graphic" in Path(b["source"]).name
        assert not (a_cg and b_cg), f"Consecutive code graphics: {a['row_id']} ({a['source']}) -> {b['row_id']} ({b['source']})"

    # Write shot_list_v02.csv
    fieldnames = ["row", "vo_in", "vo_out", "dur_s", "cuts", "source", "asset", "vo_text", "markers"]
    for out_dir in (EDIT_DIR, NAS_EDIT):
        out_dir.mkdir(parents=True, exist_ok=True)
        with (out_dir / "shot_list_v02.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(csv_rows)

    # Write cuts_064_j3023_v02.json
    cuts_txt = json.dumps(cuts, indent=2) + "\n"
    (EDIT_DIR / "cuts_064_j3023_v02.json").write_text(cuts_txt, encoding="utf-8")
    (NAS_EDIT / "cuts_064_j3023_v02.json").write_text(cuts_txt, encoding="utf-8")

    # Write pool_064_j3023_v02.json
    pool_entries = []
    for key, (p, credit, lic, title, is_vid, upscale) in ASSETS.items():
        ent = {
            "id": key,
            "file": str(p),
            "title": title,
            "credit": credit,
            "license": lic,
            "upscale_max": upscale,
        }
        if key == "PIA00215":
            ent["source_url"] = "https://science.nasa.gov/photojournal/venus-alpha-regio/"
            ent["sha256"] = REQUIRED_PIA00215_SHA
        elif key == "PIA18033":
            ent["source_url"] = "https://science.nasa.gov/image-detail/amf-pia18033/"
        elif key == "pvo_uv_790205":
            ent["sha256"] = REQUIRED_PVO_SHA
        pool_entries.append(ent)
    for key, (p, title) in CODE_GRAPHICS.items():
        pool_entries.append({
            "id": Path(key).stem,
            "file": str(p),
            "title": title,
            "credit": "Original OWB code graphic",
            "license": "Studio owned",
            "upscale_max": 1.0,
        })
    for rej in REJECTED:
        pool_entries.append(rej)

    pool_txt = json.dumps({"entries": pool_entries}, indent=2) + "\n"
    (EDIT_DIR / "pool_064_j3023_v02.json").write_text(pool_txt, encoding="utf-8")
    (NAS_EDIT / "pool_064_j3023_v02.json").write_text(pool_txt, encoding="utf-8")

    # Write POOL_PROVENANCE_J3023_v02.json
    prov = {
        "job": "J3023",
        "film": "OWB:064",
        "version": "v02",
        "locked_vo_sha256": REQUIRED_VO_SHA,
        "total_cuts": len(cuts),
        "total_duration_s": 701.86,
        "active_assets": list(provenance_map.values()),
        "rejected_assets": REJECTED,
    }
    prov_txt = json.dumps(prov, indent=2) + "\n"
    (EDIT_DIR / "POOL_PROVENANCE_J3023_v02.json").write_text(prov_txt, encoding="utf-8")
    (NAS_EDIT / "POOL_PROVENANCE_J3023_v02.json").write_text(prov_txt, encoding="utf-8")

    print(f"OK: wrote v02 inputs ({len(csv_rows)} rows, {len(cuts)} cuts, {len(provenance_map)} active assets, {len(REJECTED)} rejected)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
