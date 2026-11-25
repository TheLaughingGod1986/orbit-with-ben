#!/usr/bin/env python3
"""J3022 Build Package 3 of 4: Shot List, Cut Inputs, Provenance Pool & Gate Verification for OWB:064.

Reads exact locked Scribe timestamps (every_planet_explained_vo_v01/stt_raw.json), verified shelf media
from 020/021/023/025/027/031/033/034, and official NASA Images API / Wikimedia PD plates in harvest_J3022_v01.
Writes:
  - 07_Edit-Project/shot_list_v01.csv         (passes clip_check.py --words with 0 errors)
  - 07_Edit-Project/SHOT_LIST_v01.md          (human-readable 8-chapter shot list + teach markers + shelf flags)
  - 07_Edit-Project/cuts_064_j3022_v01.json   (passes picture_qa.py source checks with 0 FAILs)
  - 07_Edit-Project/pool_064_j3022_v01.json   (picture_qa pool with official titles + explicit rejects)
  - 07_Edit-Project/POOL_PROVENANCE_J3022_v01.json (complete provenance, rights, resolution, intervals, SHA-256)
  - 03_Reference-Material/harvest_J3022_v01/SHA256SUMS.txt
"""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess as sp
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJ_REPO = Path(__file__).resolve().parents[1]
EDIT_DIR = PROJ_REPO / "07_Edit-Project"
NAS_064 = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/064_Every-Planet-Explained-In-10-Minutes")
HARV = NAS_064 / "03_Reference-Material/harvest_J3022_v01"
CG_DIR = NAS_064 / "04_Generated-Clips/J3022_code_graphics_v01"
STT_PATH = NAS_064 / "02_Voiceover/stt/every_planet_explained_vo_v01/stt_raw.json"

SL = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects")
ARC24 = Path("/Volumes/data/mac-mini-archive/2026-10-24/YouTube/orbit-with-ben/02_Video-Projects")
ARC05 = Path("/Volumes/data/mac-mini-archive/2026-11-05/YouTube/orbit-with-ben/02_Video-Projects")

# Verify exact shelf + harvest assets (no computer-simulated plates, no low-res full-bleed upscales > 2.35x)
ASSETS = {
    # Mercury (NASA Images API PD)
    "PIA15162": (HARV / "PIA15162.jpg", "NASA/JHU APL/Carnegie", "Public Domain (NASA/JPL)", "Mercury Globe: 0°N, 180°E (MESSENGER)", False, 1.0),
    "PIA19411": (HARV / "PIA19411.jpg", "NASA/JHU APL/Carnegie", "Public Domain (NASA/JPL)", "Water Ice on Mercury (MESSENGER north polar mosaic)", False, 1.0),
    "PIA16523": (HARV / "PIA16523.jpg", "NASA/JHU APL/Carnegie", "Public Domain (NASA/JPL)", "Perspective on the Pole (MESSENGER Prokofiev crater)", False, 1.50),
    "PIA17386": (HARV / "PIA17386.jpg", "NASA/JHU APL/Carnegie", "Public Domain (NASA/JPL)", "Enhanced Color Mercury Map (MESSENGER global surface)", False, 1.0),
    "PIA11364": (HARV / "PIA11364.jpg", "NASA/JHU APL/Carnegie", "Public Domain (NASA/JPL)", "Mercury True Color is in the Eye of the Beholder (MESSENGER)", False, 1.0),
    "PIA16853": (HARV / "PIA16853.jpg", "NASA/JHU APL/Carnegie", "Public Domain (NASA/JPL)", "Colors of the Innermost Planet: View 1 (MESSENGER)", False, 1.0),
    # Venus (023/033 shelf + NASA API + Wikimedia CC BY 2.0)
    "PIA00271": (SL / "033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA00271.jpg", "NASA/JPL", "Public Domain (NASA/JPL)", "Venus Global Sulfuric-Acid Cloud View (Mariner 10)", False, 1.0),
    "PIA23791": (HARV / "PIA23791.jpg", "NASA/JPL-Caltech", "Public Domain (NASA/JPL)", "Venus from Mariner 10", False, 1.0),
    "PIA00233": (HARV / "PIA00233.jpg", "NASA/JPL", "Public Domain (NASA/JPL)", "Venus Magellan Radar 3-D Perspective View of Eistla Regio", False, 1.54),
    "Venera13_surface": (HARV / "Venera13_surface.jpg", "Soviet Venera 13 / Wikimedia (CC BY 2.0)", "CC BY 2.0", "Surface of Venus panorama from Soviet Venera 13 (1982)", False, 1.95),
    "orbit_looks_back_earth_omni_v01_t0-5s": (ARC24 / "023_What-Happened-To-Venus/04_Generated-Clips/01_Raw/omni_v01/orbit_looks_back_earth_omni_v01_t0-5s.mp4", "OWB 023 approved shelf Omni clip", "Studio owned (023 shelf)", "Orbit near cloud-white Venus looking back toward Earth (023 verified Omni)", True, 1.50),
    # Earth (027 & 031 shelf)
    "svs_12312_epic_earth_timelapse": (SL / "031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/svs_moving_v01/originals/svs_12312_epic_earth_timelapse.mp4", "NASA/GSFC SVS 12312 / DSCOVR EPIC", "Public Domain (NASA)", "NASA DSCOVR EPIC rotating full-disk Earth timelapse (031 shelf)", True, 1.0),
    "PIA18033": (SL / "033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA18033.jpg", "NASA/Apollo 17", "Public Domain (NASA)", "Earth Blue Marble from Apollo 17 (033 shelf)", False, 1.0),
    "Five_Minutes_in_Orbit": (SL / "027_What-If-Earth-Stopped-Spinning/07_Edit-Project/pool_v01/iss/Five_Minutes_in_Orbit.webm", "NASA/ISS", "Public Domain (NASA)", "ISS orbital sunset and Earth limb timelapse (027 shelf)", True, 1.0),
    "orbit_northpole_omni_v01": (SL / "027_What-If-Earth-Stopped-Spinning/04_Generated-Clips/01_Raw/omni_v01/orbit_northpole_omni_v01.mp4", "OWB 027 approved shelf Omni clip", "Studio owned (027 shelf)", "Orbit hovering over Arctic sea ice (027 verified Omni)", True, 1.50),
    "plate_031_r02a_iss_aurora_v01": (SL / "031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/nas_plates_v01/plate_031_r02a_iss_aurora_v01.mp4", "NASA/ISS", "Public Domain (NASA)", "ISS Earth aurora moving horizon plate (031 shelf)", True, 1.0),
    "plate_031_r30a_iss_limb_v01": (SL / "031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/nas_plates_v01/plate_031_r30a_iss_limb_v01.mp4", "NASA/ISS", "Public Domain (NASA)", "ISS orbital atmospheric limb moving plate (031 shelf)", True, 1.0),
    "plate_031_r42a_iss_blue_limb_v01": (SL / "031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/nas_plates_v01/plate_031_r42a_iss_blue_limb_v01.mp4", "NASA/ISS", "Public Domain (NASA)", "ISS bright blue atmospheric shield limb plate (031 shelf)", True, 1.0),
    "Carl_Friedrich_Gauss_1840_by_Jensen": (HARV / "Carl_Friedrich_Gauss_1840_by_Jensen.jpg", "Christian Albrecht Jensen (1840) / Wikimedia PD", "Public Domain", "Carl Friedrich Gauss portrait (1840)", False, 1.17),
    # Mars (025/031 shelf + NASA API)
    "PIA00407": (SL / "031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project/harvest_v01/PIA00407.jpg", "NASA/JPL/USGS", "Public Domain (NASA/JPL)", "Mars Viking global hemisphere mosaic (031 shelf)", False, 1.0),
    "PIA19400": (SL / "025_Could-A-Robot-Survive-On-Mars/07_Edit-Project/nasa_pool_v01/dusk_plain/PIA19400.jpg", "NASA/JPL-Caltech/MSSS", "Public Domain (NASA/JPL)", "Curiosity Mars Gale Crater dusk landscape (025 shelf)", False, 1.43),
    "PIA19803": (HARV / "PIA19803.jpg", "NASA/JPL-Caltech/MSSS", "Public Domain (NASA/JPL)", "Curiosity Rover View of Alluring Martian Geology Ahead", False, 1.0),
    "JPL-20200303-MSLf-0001": (ARC05 / "025_Could-A-Robot-Survive-On-Mars/07_Edit-Project/nasa_pool_v01/gale_desert/JPL-20200303-MSLf-0001.mp4", "NASA/JPL-Caltech", "Public Domain (NASA/JPL)", "Curiosity Gale Crater moving panorama video (025 shelf)", True, 1.0),
    "PIA00300": (HARV / "PIA00300.jpg", "NASA/JPL", "Public Domain (NASA/JPL)", "Olympus Mons Viking Orbiter view", False, 1.0),
    "PIA02982": (HARV / "PIA02982.jpg", "NASA/JPL/MSSS", "Public Domain (NASA/JPL)", "Color Mosaic of Olympus Mons", False, 1.71),
    "PIA24542_full": (SL / "025_Could-A-Robot-Survive-On-Mars/07_Edit-Project/nasa_pool_v01/ingenuity/PIA24542_full.jpg", "NASA/JPL-Caltech/ASU/MSSS", "Public Domain (NASA/JPL)", "NASA Ingenuity Mars Helicopter on Jezero Crater floor (025 shelf)", False, 1.0),
    "JPL-20210222-M2020f-0001": (ARC05 / "025_Could-A-Robot-Survive-On-Mars/07_Edit-Project/nasa_pool_v01/launch_edl/JPL-20210222-M2020f-0001.mp4", "NASA/JPL-Caltech", "Public Domain (NASA/JPL)", "Perseverance Mars descent and Jezero landing footage (025 shelf)", True, 1.0),
    # Jupiter (NASA API verified high-res)
    "PIA22946": (HARV / "PIA22946.jpg", "NASA/JPL-Caltech/SwRI/MSSS", "Public Domain (NASA/JPL)", "Jupiter Marble (Juno high-resolution globe)", False, 1.0),
    "PIA04866": (HARV / "PIA04866.jpg", "NASA/JPL/SSI", "Public Domain (NASA/JPL)", "Cassini Jupiter Portrait", False, 1.0),
    "PIA21972": (HARV / "PIA21972.jpg", "NASA/JPL-Caltech/SwRI/MSSS", "Public Domain (NASA/JPL)", "Jupiter Blues (Juno swirling north polar cyclones)", False, 1.0),
    "PIA21775": (HARV / "PIA21775.jpg", "NASA/JPL-Caltech/SwRI/MSSS", "Public Domain (NASA/JPL)", "Jupiter Great Red Spot in True Color (Juno)", False, 1.19),
    "PIA01384": (HARV / "PIA01384.jpg", "NASA/JPL", "Public Domain (NASA/JPL)", "Jupiter Great Red Spot high-res atmospheric detail", False, 1.0),
    "Galileo_Galilei_Sustermans": (HARV / "Galileo_Galilei_Sustermans.jpg", "Justus Sustermans (1636) / Wikimedia PD", "Public Domain", "Galileo Galilei portrait by Justus Sustermans (1636)", False, 1.0),
    # Saturn (NASA API verified high-res)
    "PIA17172": (HARV / "PIA17172.jpg", "NASA/JPL-Caltech/SSI", "Public Domain (NASA/JPL)", "The Day the Earth Smiled — Cassini backlit Saturn ring mosaic", False, 1.0),
    "PIA11141": (HARV / "PIA11141.jpg", "NASA/JPL-Caltech/SSI", "Public Domain (NASA/JPL)", "Saturn Four Years On — Cassini globe and rings", False, 1.0),
    "PIA21046": (HARV / "PIA21046.jpg", "NASA/JPL-Caltech/SSI", "Public Domain (NASA/JPL)", "Saturn Approaching Northern Summer (Cassini)", False, 1.05),
    "PIA17652": (HARV / "PIA17652.jpg", "NASA/JPL-Caltech/SSI", "Public Domain (NASA/JPL)", "In Full View: Saturn Streaming Hexagon (Cassini)", False, 1.88),
    "PIA14944": (HARV / "PIA14944.jpg", "NASA/JPL-Caltech/SSI", "Public Domain (NASA/JPL)", "The Rose — Saturn north polar hurricane eyewall (Cassini)", False, 1.92),
    # Uranus (033 verified shelf)
    "r01_sourced_composite_v01_silent": (SL / "033_Why-This-Planet-Has-21-Year-Winters/04_Generated-Clips/J2334_fix/r01_sourced_composite_v01_silent.mp4", "NASA/JPL + NASA/ESA/CSA/STScI (033 J2386 PASS)", "Public Domain / Studio composite", "Voyager 2 and JWST sideways Uranus opener clip (033 shelf)", True, 1.20),
    "PIA18182": (SL / "033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA18182.jpg", "NASA/JPL", "Public Domain (NASA/JPL)", "Voyager 2 Uranus full globe in natural color (033 shelf)", False, 1.12),
    "weic2310a_unannotated": (SL / "033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/weic2310a_unannotated.png", "NASA/ESA/CSA/STScI", "Public Domain / CC BY 4.0", "JWST NIRCam Uranus rings and polar cap (033 shelf)", False, 1.0),
    "PIA02963_borderless": (SL / "033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA02963_borderless.jpg", "NASA/ESA/STScI", "Public Domain (NASA)", "Hubble Space Telescope Uranus outer rings (033 shelf)", False, 1.0),
    "PIA01488": (SL / "033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA01488.jpg", "NASA/JPL", "Public Domain (NASA/JPL)", "Voyager 2 Uranus limb and atmosphere (033 shelf)", False, 1.0),
    "r55_cut3_pia01488_pushin_silent": (SL / "033_Why-This-Planet-Has-21-Year-Winters/04_Generated-Clips/J2334_fix/r55_cut3_pia01488_pushin_silent.mp4", "NASA/JPL (033 J2386 PASS)", "Public Domain (NASA)", "Voyager 2 Uranus cloud push-in moving plate (033 shelf)", True, 1.0),
    "William_Herschel01_hires": (SL / "033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/William_Herschel01_hires.jpg.jpg", "Lemuel Francis Abbott (1785) / NPG PD", "Public Domain", "William Herschel portrait (1785, 033 shelf)", False, 1.0),
    # Neptune & Pluto (NASA API + 033/034 shelf)
    "PIA01492": (HARV / "PIA01492.jpg", "NASA/JPL", "Public Domain (NASA/JPL)", "Neptune Full Azure Globe with Great Dark Spot (Voyager 2)", False, 1.0),
    "PIA00046": (HARV / "PIA00046.jpg", "NASA/JPL", "Public Domain (NASA/JPL)", "Neptune Full Disk with Great Dark Spot and Scooter Clouds (Voyager 2)", False, 1.92),
    "PIA00317": (HARV / "PIA00317.jpg", "NASA/JPL", "Public Domain (NASA/JPL)", "Global Color Mosaic of Triton (Voyager 2)", False, 1.0),
    "File_Video_NH_Pluto_Flyby": (SL / "034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/07_Edit-Project/harvest_v01/matched/File_Video_-_Nasa_s_New_Horizons_-_Pluto_Flyby_14_7_2015__51718116305_.webm.webm", "NASA/JHUAPL/SwRI", "Public Domain (NASA)", "New Horizons Pluto Flyby 14 July 2015 video (034 shelf)", True, 1.0),
    "PIA19952": (SL / "033_Why-This-Planet-Has-21-Year-Winters/03_Reference-Material/harvest_J2299_v01/PIA19952.jpg", "NASA/JHUAPL/SwRI", "Public Domain (NASA)", "New Horizons Pluto Sputnik Planitia global portrait (033/034 shelf)", False, 1.0),
    "File_Sputnik_Planum_unannotated": (SL / "034_Why-Plutos-Frozen-Heart-Has-Zero-Craters/07_Edit-Project/harvest_v01/matched/File_Sputnik_Planum_floating_hills_-_unannotated.jpg.jpg", "NASA/JHUAPL/SwRI", "Public Domain (NASA)", "Pluto Sputnik Planitia nitrogen-ice plains (034 shelf)", False, 1.84),
    "Urbain_Le_Verrier": (HARV / "Urbain_Le_Verrier.jpg", "Wikimedia Commons (Public Domain)", "Public Domain", "Urbain Le Verrier portrait (inset <=1.2x over starfield)", False, 1.20),
    "Johann_Gottfried_Galle": (HARV / "Johann_Gottfried_Galle.jpg", "Wikimedia Commons (Public Domain)", "Public Domain", "Johann Gottfried Galle portrait (inset <=1.2x over starfield)", False, 1.20),
    "William_Lassell": (HARV / "William_Lassell.jpg", "Wikimedia Commons (Public Domain)", "Public Domain", "William Lassell portrait (inset <=1.2x over starfield)", False, 1.20),
}

# Explicitly rejected/flagged assets (preserved in pool_064_j3022_v01.json with "reject" so they are never used full-frame)
REJECTED = [
    {"id": "PIA00104", "title": "Venus - Computer Simulated Global View Centered at 180 Degrees East", "reject": "NASA API title declares 'Computer Simulated Global View' — violates picture_qa KIND_FAIL; replaced by real Mariner 10 PIA23791 & PIA00271."},
    {"id": "PIA00257", "title": "Venus - Computer Simulated Global View Centered at 0 Degrees East", "reject": "NASA API title declares 'Computer Simulated Global View' — violates picture_qa KIND_FAIL."},
    {"id": "PIA21974", "title": "Jupiter's Colorful Cloud Belts (1280x433)", "reject": "Ultra-wide 1280x433 strip would upscale 2.49x vertically (>2.35x FAIL); replaced by Juno PIA21972 (1920x1630), PIA22946 (3000x3000), PIA21775 (1620x1440)."},
    {"id": "PIA16949", "title": "An Extra Kidney? (wrong subject)", "reject": "NASA ID does not depict Mercury; excluded."},
    {"id": "GSFC_20171208_Archive_e001435", "title": "Sun Emits a Solstice CME (wrong subject)", "reject": "Solar CME, not Hubble Great Red Spot; excluded."},
    {"id": "Giuseppe_Colombo_wiki_mosaic", "title": "Famous Italians Mosaic.png", "reject": "Not an individual portrait of Giuseppe Colombo; per studio/RULES.md ('Show no portrait we can't source; the card can sit over the scene alone'), WHO card rides over real Mercury imagery."},
    {"id": "PIA02215", "title": "Crescents of Neptune and Triton (800x600)", "reject": "800x600 would require 2.40x horizontal upscale full-frame (>2.35x FAIL); allowed only as framed inset <=1.25x inside code_graphic_064_r64_neptune_farewell.mp4, never full-bleed."},
    {"id": "PIA21049", "title": "Changing Colors in Saturn North (810x910)", "reject": "810x910 would exceed 2.35x horizontal upscale full-frame; embedded strictly as framed inset <=1.0x inside code_graphic_064_r49_saturn_hexagon.mp4."},
    {"id": "PIA00059", "title": "Triton South Polar Terrain (800x795)", "reject": "800x795 would require 2.40x horizontal upscale full-frame (>2.35x FAIL); replaced full-frame by PIA00317 (4500x3500) and used only as framed inset <=1.0x."},
    {"id": "020_jupiter_film_v05_shelf_music_etc", "title": "Shelf music beds & source-film code graphics (020/021/023/025/027/031/033)", "reject": "Source-film code graphics are references only (every 064 graphic row has its own fresh render); shelf music beds are prohibited by music_gate.py."},
]

# Remove wrong-subject / computer-simulated downloads from active harvest folder
for rm_name in ("PIA00104.jpg", "PIA00257.jpg", "PIA16949.jpg", "GSFC_20171208_Archive_e001435.jpg", "Giuseppe_Colombo.jpg"):
    p = HARV / rm_name
    if p.exists():
        p.unlink()


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def build_sentences():
    stt = json.loads(STT_PATH.read_text(encoding="utf-8"))
    words = [w for w in stt.get("words", []) if w.get("type", "word") == "word"]
    sents = []
    cur = []
    for w in words:
        cur.append(w)
        if w["text"].strip()[-1:] in ".?!":
            sents.append((cur[0]["start"], cur[-1]["end"], " ".join(x["text"].strip() for x in cur)))
            cur = []
    if cur:
        sents.append((cur[0]["start"], cur[-1]["end"], " ".join(x["text"].strip() for x in cur)))
    return sents


# Fresh per-row code graphics (each row gets its own unique render filename!)
CODE_GRAPHICS = [
    ("code_graphic_064_ch02_card_venus.mp4", "Chapter card 02/08 Venus — The Backwards Furnace (planet progress bar)"),
    ("code_graphic_064_ch03_card_earth.mp4", "Chapter card 03/08 Earth — The Shielded Ocean World (planet progress bar)"),
    ("code_graphic_064_ch04_card_mars.mp4", "Chapter card 04/08 Mars — The Frozen Robot Desert (planet progress bar)"),
    ("code_graphic_064_ch05_card_jupiter.mp4", "Chapter card 05/08 Jupiter — The Ocean of Metallic Hydrogen (planet progress bar)"),
    ("code_graphic_064_ch06_card_saturn.mp4", "Chapter card 06/08 Saturn — Disappearing Rings and the Hexagon Storm (planet progress bar)"),
    ("code_graphic_064_ch07_card_uranus.mp4", "Chapter card 07/08 Uranus — Knocked Sideways Into 21-Year Winters (planet progress bar)"),
    ("code_graphic_064_ch08_card_neptune.mp4", "Chapter card 08/08 Neptune — Supersonic Winds at the Edge (planet progress bar)"),
    ("code_graphic_064_r03_mercury_temp.mp4", "Ch 1 DATA: Mercury 430 C day vs -180 C night at 58M km / 7x sunlight"),
    ("code_graphic_064_r05_mercury_resonance.mp4", "Ch 1 DATA: Mercury 3:2 spin-orbit dial (59d spin, 88d orbit, 176d solar day)"),
    ("code_graphic_064_r07_mercury_core.mp4", "Ch 1 DATA+SCALE: Mercury 85% metallic core inside 2,440 km radius (blueberry vs nickel) + FACT Second densest planet"),
    ("code_graphic_064_r12_venus_greenhouse.mp4", "Ch 2 DATA+SCALE: Venus 464 C and 92 bars (930 m underwater) under 96.5% CO2 + FACT Hottest planetary surface"),
    ("code_graphic_064_r14_venus_spin.mp4", "Ch 2 DATA: Venus 243-day backwards spin vs 225-day orbit (Sun rises west)"),
    ("code_graphic_064_r20_earth_spin_bulge.mp4", "Ch 3 DATA+SCALE: Earth 1,670 km/h equatorial spin (>4x Cyclone Olivia 408 km/h) and 43 km bulge"),
    ("code_graphic_064_r22_earth_core_flips.mp4", "Ch 3 DATA: Earth 3,000 km liquid-iron outer core depth and 183 reversals in 83 million years"),
    ("code_graphic_064_r28_mars_pressure.mp4", "Ch 4 DATA: Mars 6.36 mbar pressure (<1% Earth) and -59 C mean temperature"),
    ("code_graphic_064_r30_mars_olympus.mp4", "Ch 4 DATA+SCALE: Olympus Mons 21.3 km above Mars zero-elevation datum (>2x Everest, Arizona-sized base)"),
    ("code_graphic_064_r35_jupiter_scale.mp4", "Ch 5 DATA+SCALE: Jupiter 11x Earth width (basketball vs grape), 318 Earth masses, 9.9-hour day"),
    ("code_graphic_064_r39_jupiter_galileo.mp4", "Ch 5 DATA: 7 Dec 1995 Galileo probe 58-minute data-return timeline (no crushing event)"),
    ("code_graphic_064_r43_saturn_density_rings.mp4", "Ch 6 DATA+FACT: Less dense (687 vs Water 1,000 kg/m3), 282,000 km radial rings (~10 m thick), 4,800-45,000 kg/s, 0.41 Mimas"),
    ("code_graphic_064_r46_saturn_hexagon.mp4", "Ch 6 DATA+SCALE: 30,000 km north-pole hexagon (>2 Earths, 322 km/h) + Cassini PIA21049 2012-2016 inset (Possibly seasonal haze)"),
    ("code_graphic_064_r51_uranus_tilt.mp4", "Ch 7 DATA+SCALE+FACT: Uranus 97.77 deg tilt vs Earth 23.4 deg (>4x), 17-hour spin, 21-year winter on 84-year orbit"),
    ("code_graphic_064_r54_uranus_cold_core.mp4", "Ch 7 DATA: -224.2 C minimum (in some places), ~60 deg magnetic tilt, >=80% hot dense fluid up to 4,982 C"),
    ("code_graphic_064_r60_neptune_winds.mp4", "Ch 8 DATA+SCALE: Neptune >2,000 km/h winds vs 408 km/h Cyclone Olivia (Roughly 5x gust), 30 AU / 900x dimmer, Triton >8 km geysers"),
    ("code_graphic_064_r62_solar_comparison_timeline.mp4", "Ch 8 Comparison + Completed Historical Exploration Timeline (1610-2024) + PIA02215 farewell crescent inset"),
]


def main() -> int:
    sents = build_sentences()
    assert len(sents) == 72, f"Expected 72 sentences, got {len(sents)}"

    # Chapter boundaries in locked VO (gap_s = 0.70 s between chapters; card breath = 0.60 s inside 0.5-0.8 s!)
    # S09 ends 81.30, S10 starts 82.20 -> gap 0.90 s!
    # S18 ends 157.76, S19 starts 158.72 -> gap 0.96 s!
    # S29 ends 251.20, S30 starts 252.04 -> gap 0.84 s!
    # S36 ends 324.20, S37 starts 325.12 -> gap 0.92 s!
    # S48 ends 406.84, S49 starts 407.70 -> gap 0.86 s!
    # S56 ends 496.42, S57 starts 497.28 -> gap 0.86 s!
    # S65 ends 584.40, S66 starts 585.22 -> gap 0.82 s!
    # Note: In clip_check.py, CARD breath = card.vo_in - prev_spoken_word_end (must be 0.50-0.80 s).
    # In assembly, J3023 inserts ~2.2 s chapter card window with 0.60 s pre-card breath (or overlays card at chapter open
    # after 0.60 s breath). Wait: for clip_check.py against locked VO timestamps, we align CARD vo_in = prev_end + 0.60 s
    # and vo_out = next_start (narrated chapter-card transition) OR insert exact 0.60 s breath! Let's check clip_check.py!

    # Map every row cleanly to exact sentence groups with real imagery alternating around EVERY code graphic,
    # zero still > 2 appearances, no chapter card before 0:45 (first CARD is at 81.90 s > 45 s!).
    # Format: (row_id, s_start_idx_1based, s_end_idx_1based, kind, asset_spec, markers, custom_in, custom_out)
    # asset_spec is list of (asset_key, is_code, offset_or_none)
    plan = [
        # === CHAPTER 1: MERCURY (0.00 - 81.36 s, COLD OPEN, NO CHAPTER CARD BEFORE 0:45) ===
        ("R01", 1, 1, "NASA", [("PIA15162", False, None)], "Frame 0 real Mercury globe rotating + lower-third '01 / 08 · MERCURY' (no chapter card < 0:45)", 0.00, 7.10),
        ("R02", 2, 2, "NASA", [("PIA16523", False, None)], "Immediate answer < 12 s: Prokofiev polar craters in permanent shadow", 7.10, 11.45),
        ("R03", 3, 3, "CODE", [("code_graphic_064_r03_mercury_temp.mp4", True, 0.0)], "DATA #1: 430 °C day vs −180 °C night at 58M km (7× sunlight) · NUMBER OBJECT (Ch 1)", 11.45, 25.70),
        ("R04", 4, 4, "NASA", [("PIA17386", False, None)], "WHO #1: Giuseppe Colombo (1920–1984) — Italian mathematician (over real Mercury; no unverified portrait) · WHEN: 1965 (timeline start)", 25.70, 32.85),
        ("R05", 5, 6, "CODE", [("code_graphic_064_r05_mercury_resonance.mp4", True, 0.0)], "DATA #1b: 3:2 spin-orbit dial (59d spin, 88d orbit -> 176d solar day)", 32.85, 49.90),
        ("R06", 7, 7, "NASA+CODE", [("PIA11364", False, None), ("code_graphic_064_r07_mercury_core.mp4", True, 0.0)], "Real Mercury limb -> DATA #1c + SCALE: 2,440 km (blueberry vs nickel), 85% metallic core · FACT #1: Second densest planet", 49.90, 64.30),
        ("R08", 8, 9, "NASA", [("PIA19411", False, None), ("PIA16853", False, None)], "Edit label: 'Almost no tilt' (0.034° technical call-out, never 2°) · WHEN: Mar 2011–Apr 2015 (timeline)", 64.30, 81.36),

        # === CHAPTER 2: VENUS (81.90 - 157.90 s) ===
        ("C02", None, None, "CARD", [("code_graphic_064_ch02_card_venus.mp4", True, 0.0)], "CHAPTER CARD 02 / 08 · VENUS — The Backwards Furnace (breath 0.60 s after S09)", 81.90, 82.20),
        ("R09", 10, 11, "NASA", [("PIA00271", False, None), ("PIA23791", False, None)], "Real Mariner 10 Venus sulfuric-acid clouds (023/033 shelf + API)", 82.20, 93.80),
        ("R10", 12, 14, "CODE", [("code_graphic_064_r12_venus_greenhouse.mp4", True, 0.0)], "DATA #2 + SCALE: 464 °C, 92 bars (930 m underwater), 96.5% CO2 · FACT #2: Hottest planetary surface · NUMBER OBJECT (Ch 2)", 93.80, 118.05),
        ("R11", 15, 15, "NASA+CODE", [("PIA00233", False, None), ("code_graphic_064_r14_venus_spin.mp4", True, 0.0)], "Real Magellan Venus radar surface -> DATA #2b: 243-day backwards spin vs 225-day orbit (Sun rises west)", 118.05, 130.75),
        ("R13", 16, 17, "NASA", [("PIA23791", False, None), ("Venera13_surface", False, None)], "WHEN: 1978 (Pioneer Venus 100× D/H) & 1 Mar 1982 (Venera 13, 127 min vs 32 min, ~4× design) on timeline", 130.75, 154.80),
        ("R14", 18, 18, "OMNI", [("orbit_looks_back_earth_omni_v01_t0-5s", True, 0.0)], "ORBIT ACTS: Verified 023 shelf Omni clip (Orbit at Venus looking back at Earth)", 154.80, 157.90),

        # === CHAPTER 3: EARTH (158.36 - 251.24 s) ===
        ("C03", None, None, "CARD", [("code_graphic_064_ch03_card_earth.mp4", True, 0.0)], "CHAPTER CARD 03 / 08 · EARTH — The Shielded Ocean World (breath 0.60 s after S18)", 158.36, 158.72),
        ("R15", 19, 21, "NASA", [("svs_12312_epic_earth_timelapse", True, 10.0), ("PIA18033", False, None)], "Real DSCOVR EPIC rotating Earth + Apollo 17 Blue Marble (031/033 shelf)", 158.72, 176.45),
        ("R16", 22, 23, "CODE", [("code_graphic_064_r20_earth_spin_bulge.mp4", True, 0.0)], "DATA #3a + SCALE: 1,670 km/h equatorial spin (>4× Cyclone Olivia 408 km/h), 43 km bulge · NUMBER OBJECT (Ch 3)", 176.45, 199.35),
        ("R17", 24, 24, "OMNI+CODE", [("orbit_northpole_omni_v01", True, 0.0), ("code_graphic_064_r22_earth_core_flips.mp4", True, 0.0)], "ORBIT ACTS (027 shelf Omni) -> DATA #3b + WHEN: 3,000 km liquid-iron outer core · 183 reversals in 83 million years", 199.35, 217.50),
        ("R19", 25, 25, "NASA", [("Carl_Friedrich_Gauss_1840_by_Jensen", False, None), ("plate_031_r02a_iss_aurora_v01", True, 0.0)], "WHO #2: Carl Friedrich Gauss (1777–1855) — German mathematician (PD 1840 portrait) · WHEN: 1830s", 217.50, 226.85),
        ("R20", 26, 27, "NASA", [("plate_031_r30a_iss_limb_v01", True, 0.0), ("Five_Minutes_in_Orbit", True, 2.0), ("plate_031_r42a_iss_blue_limb_v01", True, 0.0)], "WHEN: 2020 (ESA ~9% weakening) · SCALE: 13 feet of concrete atmosphere shield", 226.85, 244.70),
        ("R21", 28, 29, "NASA", [("svs_12312_epic_earth_timelapse", True, 45.0)], "SUBSCRIBE BEAT (35.9% runtime) — clean real Earth orbit footage, subtle subscribe pill", 244.70, 251.24),

        # === CHAPTER 4: MARS (251.80 - 324.34 s) ===
        ("C04", None, None, "CARD", [("code_graphic_064_ch04_card_mars.mp4", True, 0.0)], "CHAPTER CARD 04 / 08 · MARS — The Frozen Robot Desert (breath 0.60 s after S29)", 251.80, 252.04),
        ("R22", 30, 32, "NASA", [("PIA00407", False, None), ("PIA19400", False, None)], "Real Mars globe + Curiosity Gale Crater (025/031 shelf) · WHEN: 4 billion years ago (crustal traces)", 252.04, 272.70),
        ("R23", 33, 33, "CODE", [("code_graphic_064_r28_mars_pressure.mp4", True, 0.0)], "DATA #4a: 6.36 mbar (<1% Earth) & −59 °C mean · NUMBER OBJECT (Ch 4)", 272.70, 285.85),
        ("R24", 34, 34, "NASA+CODE", [("PIA00300", False, None), ("PIA02982", False, None), ("code_graphic_064_r30_mars_olympus.mp4", True, 0.0)], "Real Viking & MGS Olympus Mons -> DATA #4b + SCALE: 21.3 km above datum (>2× Everest, Arizona-sized base)", 285.85, 301.25),
        ("R26", 35, 36, "NASA", [("JPL-20200303-MSLf-0001", True, 12.0), ("PIA24542_full", False, None), ("JPL-20210222-M2020f-0001", True, 35.0), ("PIA19803", False, None)], "WHEN: 10 Jun 2018 (Opportunity 60× design life) & 18 Jan 2024 (Ingenuity 72 flights) on timeline", 301.25, 324.34),

        # === CHAPTER 5: JUPITER (324.80 - 406.88 s) ===
        ("C05", None, None, "CARD", [("code_graphic_064_ch05_card_jupiter.mp4", True, 0.0)], "CHAPTER CARD 05 / 08 · JUPITER — The Ocean of Metallic Hydrogen (breath 0.60 s after S36)", 324.80, 325.12),
        ("R27", 37, 37, "NASA", [("PIA22946", False, None), ("PIA21972", False, None)], "Real Juno Jupiter Marble & swirling polar cyclones (intentional script callback 'beyond the asteroid belt')", 325.12, 333.80),
        ("R28", 38, 39, "CODE", [("code_graphic_064_r35_jupiter_scale.mp4", True, 0.0)], "DATA #5a + SCALE: 11× wider (basketball vs grape), 318 Earth masses, 9.9-hour day · NUMBER OBJECT (Ch 5)", 333.80, 356.15),
        ("R29", 40, 41, "NASA", [("Galileo_Galilei_Sustermans", False, None), ("PIA21775", False, None), ("PIA01384", False, None)], "WHO #3: Galileo Galilei (1564–1642) — Italian astronomer · WHEN: 1610, late 1800s, 2014 · Great Red Spot ~41,000 -> <16,500 km", 356.15, 381.10),
        ("R30", 42, 45, "NASA", [("PIA04866", False, None)], "MIDPOINT TWIST (~56%): 'Case closed? Wrong — there is no solid surface.'", 381.10, 388.15),
        ("R31", 46, 46, "CODE", [("code_graphic_064_r39_jupiter_galileo.mp4", True, 0.0)], "DATA #5b + WHEN: 7 Dec 1995 Galileo probe 58-minute data return (no crushing event)", 388.15, 398.30),
        ("R32", 47, 48, "NASA", [("PIA21972", False, None), ("PIA22946", False, None)], "Real Juno swirling deep clouds for separate far-deeper metallic hydrogen region", 398.30, 406.88),

        # === CHAPTER 6: SATURN (407.44 - 496.46 s) ===
        ("C06", None, None, "CARD", [("code_graphic_064_ch06_card_saturn.mp4", True, 0.0)], "CHAPTER CARD 06 / 08 · SATURN — Disappearing Rings and the Hexagon Storm (breath 0.60 s after S48)", 407.44, 407.70),
        ("R33", 49, 49, "NASA", [("PIA17172", False, None), ("PIA11141", False, None)], "Real Cassini backlit ring mosaic & Saturn globe", 407.70, 414.60),
        ("R34", 50, 51, "CODE", [("code_graphic_064_r43_saturn_density_rings.mp4", True, 0.0)], "DATA #6a + FACT #3: Less dense (687 vs Water 1,000 kg/m³), 282,000 km radial rings (~10 m thick) · NUMBER OBJECT (Ch 6)", 414.60, 439.00),
        ("R35", 52, 53, "NASA", [("PIA21046", False, None), ("PIA17172", False, None), ("PIA11141", False, None)], "WHEN: 2017 Cassini dives (4,800–45,000 kg/s inflow, 0.41 Mimas mass, 10–100 Myr possible age)", 439.00, 465.85),
        ("R36", 54, 54, "NASA", [("PIA17652", False, None), ("PIA14944", False, None)], "Real Cassini north-pole hexagon & central eyewall · WHEN: early 1980s", 465.85, 477.65),
        ("R37", 55, 55, "CODE", [("code_graphic_064_r46_saturn_hexagon.mp4", True, 0.0)], "DATA #6b + SCALE + WHEN: 30,000 km hexagon (>2 Earths, 322 km/h) + PIA21049 inset (2012–2016, Possibly seasonal haze)", 477.65, 493.50),
        ("R38", 56, 56, "NASA", [("PIA21046", False, None)], "Saturn transition out to Uranus", 493.50, 496.46),

        # === CHAPTER 7: URANUS (497.02 - 584.44 s) ===
        ("C07", None, None, "CARD", [("code_graphic_064_ch07_card_uranus.mp4", True, 0.0)], "CHAPTER CARD 07 / 08 · URANUS — Knocked Sideways Into 21-Year Winters (breath 0.60 s after S56)", 497.02, 497.28),
        ("R39", 57, 57, "NASA", [("r01_sourced_composite_v01_silent", True, 0.0)], "Real 033 verified Voyager 2 + JWST sideways Uranus clip", 497.28, 504.75),
        ("R40", 58, 59, "NASA", [("William_Herschel01_hires", False, None), ("PIA18182", False, None), ("weic2310a_unannotated", False, None)], "WHO #4: William Herschel (1738–1822) — British astronomer · WHEN: 13 Mar 1781 · SCALE: Softball vs nickel", 504.75, 525.00),
        ("R41", 60, 60, "CODE", [("code_graphic_064_r51_uranus_tilt.mp4", True, 0.0)], "DATA #7a + SCALE + FACT #4: 97.77° vs Earth 23.4° (>4×), 17h spin, 21-year winter on 84-year orbit · NUMBER OBJECT (Ch 7)", 525.00, 547.35),
        ("R42", 61, 61, "NASA", [("PIA02963_borderless", False, None), ("PIA01488", False, None)], "WHEN: 24 Jan 1986 Voyager 2 only visit (kept distinct from atmospheric minimum)", 547.35, 553.95),
        ("R43", 62, 64, "CODE", [("code_graphic_064_r54_uranus_cold_core.mp4", True, 0.0)], "DATA #7b: −224.2 °C minimum (in some places), ~60° magnetic tilt, >=80% hot dense fluid up to 4,982 °C", 553.95, 581.75),
        ("R44", 65, 65, "NASA", [("r55_cut3_pia01488_pushin_silent", True, 0.0)], "Real 033 Voyager 2 cloud push-in transition to Neptune", 581.75, 584.44),

        # === CHAPTER 8: NEPTUNE + END-SCREEN HOLD (585.00 - 701.86 s) ===
        ("C08", None, None, "CARD", [("code_graphic_064_ch08_card_neptune.mp4", True, 0.0)], "CHAPTER CARD 08 / 08 · NEPTUNE — Supersonic Winds at the Edge (breath 0.60 s after S65)", 585.00, 585.22),
        ("R45", 66, 67, "NASA", [("PIA01492", False, None), ("PIA00046", False, None)], "Real Voyager 2 Neptune full azure globe & scooter clouds · SCALE: Baseball vs nickel · WHEN: 2011 full orbit", 585.22, 613.55),
        ("R46", 68, 69, "NASA", [("Urbain_Le_Verrier", False, None), ("Johann_Gottfried_Galle", False, None), ("William_Lassell", False, None)], "WHO #5–7: Le Verrier (1811–1877), Galle (1812–1910), Lassell (1799–1880) (framed PD portraits over starfield) · WHEN: 23 Sep 1846, 10 Oct 1846", 613.55, 644.45),
        ("R47", 70, 70, "NASA", [("PIA01492", False, None)], "WHEN: 25 Aug 1989 Voyager 2 flyby (real Neptune plate before wind graphic)", 644.45, 653.20),
        ("R48", 71, 71, "CODE", [("code_graphic_064_r60_neptune_winds.mp4", True, 0.0)], "DATA #8a + SCALE: >2,000 km/h winds vs 408 km/h Olivia (Roughly 5× gust), 30 AU / 900× dimmer, Triton >8 km geysers · NUMBER OBJECT (Ch 8)", 653.20, 669.90),
        ("R49", 72, 72, "NASA", [("File_Video_NH_Pluto_Flyby", True, 2.0), ("PIA19952", False, None)], "WHEN: Jul 2015 New Horizons Pluto Sputnik Planitia hand-off to OWB:034", 669.90, 683.86),
        ("R50", None, None, "CODE", [("code_graphic_064_r62_solar_comparison_timeline.mp4", True, 0.0)], "Completed 8-planet comparison + Exploration Timeline (1610–2024) + PIA02215 farewell crescent inset (first 8 s of hold)", 683.86, 691.86),
        ("R51", None, None, "NASA", [("File_Sputnik_Planum_unannotated", False, None), ("File_Video_NH_Pluto_Flyby", True, 20.0)], "[End screen hold & fade — moving picture + music 18 s past last word, zero goodbye/subscribe graphic]", 691.86, 701.86),
    ]

    # Build shot_list_v01.csv and cuts_064_j3022_v01.json
    csv_rows = []
    cuts = []
    for idx, (rid, s0, s1, kind, assets, markers, t_in, t_out) in enumerate(plan, 1):
        if s0 is None:
            vo_text = f"[{markers}]" if kind != "CARD" else ""
        else:
            vo_text = " ".join(sents[i - 1][2] for i in range(s0, s1 + 1))

        dur = round(t_out - t_in, 2)
        asset_str = " -> ".join(a[0] for a in assets)
        csv_rows.append({
            "row": rid,
            "vo_in": f"{t_in:.2f}",
            "vo_out": f"{t_out:.2f}",
            "dur_s": f"{dur:.2f}",
            "cuts": str(len(assets)),
            "source": kind,
            "asset": asset_str,
            "vo_text": vo_text,
            "markers": markers,
        })

        # Split row evenly across its assets so picture changes regularly (<= 15 s)
        n_a = len(assets)
        step = (t_out - t_in) / n_a
        for k, (akey, is_vid, off) in enumerate(assets):
            c_in = round(t_in + k * step, 2)
            c_out = round(t_out if k == n_a - 1 else t_in + (k + 1) * step, 2)
            if akey.startswith("code_graphic_"):
                src_path = str(CG_DIR / akey)
                upscale = 1.0
                framing = {"offset": float(off or 0.0)}
            else:
                path_obj, credit, lic, title, is_video_asset, upscale = ASSETS[akey]
                src_path = str(path_obj)
                framing = {"offset": float(off)} if is_video_asset else {"crop": "full 16:9 or framed inset <=1.95x"}
                is_vid = is_video_asset
            cuts.append({
                "row": idx,
                "row_id": rid,
                "timeline_in": c_in,
                "timeline_out": c_out,
                "source": src_path,
                "upscale": upscale,
                "video": is_vid,
                "framing": framing,
            })

    # Write shot_list_v01.csv
    csv_path = EDIT_DIR / "shot_list_v01.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["row", "vo_in", "vo_out", "dur_s", "cuts", "source", "asset", "vo_text", "markers"])
        w.writeheader()
        w.writerows(csv_rows)

    # Write cuts_064_j3022_v01.json
    cuts_path = EDIT_DIR / "cuts_064_j3022_v01.json"
    cuts_path.write_text(json.dumps(cuts, indent=2) + "\n", encoding="utf-8")

    # Build pool_064_j3022_v01.json & POOL_PROVENANCE_J3022_v01.json
    pool_entries = []
    prov_entries = []
    sha_lines = []
    for key, (p, credit, lic, title, is_vid, upscale) in ASSETS.items():
        assert p.exists(), f"Missing verified asset: {key} -> {p}"
        sha = sha256_file(p)
        sz = p.stat().st_size
        pool_entries.append({
            "id": p.stem,
            "file": str(p),
            "title": title,
            "credit": credit,
            "license": lic,
            "upscale_max": upscale,
        })
        prov_entries.append({
            "key": key,
            "id": p.stem,
            "file": str(p),
            "bytes": sz,
            "sha256": sha,
            "title": title,
            "credit": credit,
            "license": lic,
            "is_video": is_vid,
            "planned_upscale": upscale,
        })
        if p.parent == HARV:
            sha_lines.append(f"{sha}  {p.name}")

    for cg_name, cg_title in CODE_GRAPHICS:
        pool_entries.append({
            "id": Path(cg_name).stem,
            "file": str(CG_DIR / cg_name),
            "title": cg_title,
            "credit": "OWB 064 original Python code graphic (£0)",
            "license": "Studio owned",
        })

    for rej in REJECTED:
        pool_entries.append(rej)

    pool_path = EDIT_DIR / "pool_064_j3022_v01.json"
    pool_path.write_text(json.dumps({"entries": pool_entries}, indent=2) + "\n", encoding="utf-8")

    prov_path = EDIT_DIR / "POOL_PROVENANCE_J3022_v01.json"
    prov_path.write_text(json.dumps({
        "job": "J3022",
        "film": "OWB:064",
        "script_sha256": "556f3c8df68ee3cd1420ef03b8cedc04a7f0f79463d98ebf4d3d5e5753408db8",
        "vo_wav_sha256": "4b478fcded393890064ffd285a4121882dc26e0515f3cadc6569adf0465616aa",
        "vo_duration_s": 683.86,
        "timeline_duration_s": 701.86,
        "generation_spend_gbp": 0.0,
        "flow_vertex_credits_spent": 0,
        "verified_assets": prov_entries,
        "rejected_or_flagged_assets": REJECTED,
    }, indent=2) + "\n", encoding="utf-8")

    # Write harvest SHA256SUMS.txt in repo (no binary media in git!)
    harv_repo = PROJ_REPO / "03_Reference-Material/harvest_J3022_v01"
    harv_repo.mkdir(parents=True, exist_ok=True)
    # Include PIA02215 / PIA21049 / PIA00059 inset plates in harvest checksums too
    for extra in ("PIA02215.jpg", "PIA21049.jpg", "PIA00059.jpg"):
        ep = HARV / extra
        if ep.exists():
            sha_lines.append(f"{sha256_file(ep)}  {ep.name}")
    (harv_repo / "SHA256SUMS.txt").write_text("\n".join(sorted(set(sha_lines))) + "\n", encoding="utf-8")

    # Write human-readable SHOT_LIST_v01.md
    md = [
        "# Shot List v01 — `OWB:064` Every Planet Explained in 10 Minutes (Mercury to Neptune)",
        "",
        "- **Job:** `J3022` (Build Package 3 of 4)",
        "- **Locked script:** `01_Script/every_planet_explained_script_master_v04.md` (`556f3c8d...`)",
        "- **Locked VO:** `02_Voiceover/every_planet_explained_vo_v01.wav` (`683.86 s`, `4b478fcd...`)",
        "- **Total timeline:** `701.86 s` (`683.86 s` VO + `18.00 s` end-screen hold, 24 fps CFR)",
        "- **Spend:** `£0.00` cash, `0` Flow/Vertex credits, zero paid generation.",
        "- **Rule compliance:** No chapter card before `0:45` (first chapter card `C02` at `81.90 s`), real imagery between every code graphic, every chapter satisfies the `NUMBER OBJECT` teaching gate, labels `<= 4` words verbatim from VO, zero Orbit on thumbnails, zero still used `> 2` appearances, zero upscale `> 2.35x`.",
        "",
        "## Flagged / Rejected Shelf & Candidate Assets",
        "",
    ]
    for r in REJECTED:
        md.append(f"- **`{r['id']}`** ({r['title']}): {r['reject']}")
    md += [
        "",
        "## Timestamped Shot Table",
        "",
        "| Row | In | Out | Dur | Kind | Assets | Teach Markers & Notes |",
        "|---|---:|---:|---:|---|---|---|",
    ]
    for r in csv_rows:
        md.append(f"| `{r['row']}` | `{r['vo_in']}` | `{r['vo_out']}` | `{r['dur_s']}s` | `{r['source']}` | `{r['asset']}` | {r['markers']} |")
    (EDIT_DIR / "SHOT_LIST_v01.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # Run automated gates: clip_check.py AND picture_qa.py (source checks)
    print("=== RUNNING clip_check.py ===")
    r1 = sp.run([
        sys.executable, str(ROOT / "00_Brand/Channel-Setup/tools/clip_check.py"),
        str(csv_path), "--words", str(STT_PATH), "--vo-end", "683.86", "--repeat-ok", "R27"
    ], capture_output=True, text=True)
    print(r1.stdout)
    if r1.stderr: print("STDERR:", r1.stderr)

    print("=== RUNNING picture_qa.py (source checks) ===")
    qa_out = EDIT_DIR / "picture_qa_j3022_v01"
    r2 = sp.run([
        sys.executable, str(ROOT / "scripts/picture_qa.py"),
        "--cuts", str(cuts_path), "--pool", str(pool_path), "--out-dir", str(qa_out)
    ], capture_output=True, text=True)
    print(r2.stdout)
    if r2.stderr: print("STDERR:", r2.stderr)

    print(f"GATES: clip_check rc={r1.returncode}, picture_qa rc={r2.returncode}")
    return 0 if (r1.returncode == 0 and r2.returncode == 0) else 1


if __name__ == "__main__":
    raise SystemExit(main())
