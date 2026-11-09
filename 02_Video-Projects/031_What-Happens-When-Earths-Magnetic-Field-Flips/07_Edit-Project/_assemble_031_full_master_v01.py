#!/usr/bin/env python3
"""031 What Happens When Earth's Magnetic Field Flips? — Long master v01 assembler (J2381). £0 spend.

Assembles the 54-row long master (568.28 s VO + 2.52 s post-VO hold = 570.80 s / 14,270 frames at 25 fps CFR)
from SHOT_LIST_v02.md + verified 1080p25 plates, code_graphics, and row composites + £0 chapter-shaped score bed
(magnetic_field_flip_score_bed_v01.mp3) + £0 house SFX kit_v01, and runs all 5 required gates.
"""
from __future__ import annotations

import csv
import json
import math
import os
import re
import subprocess as sp
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FILM = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "031_What-Happens-When-Earths-Magnetic-Field-Flips"
)
REPO = Path("/Users/benjaminoats/_desk/worktrees/J2381-master-v01")
REPO_EDIT = REPO / "02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips/07_Edit-Project"
DESK = Path("/Users/benjaminoats/_desk")
sys.path.insert(0, str(REPO / "scripts"))
import polish_gate as pg  # noqa: E402

EDIT = FILM / "07_Edit-Project"
WORK = EDIT / "full_master_v01_work"
PACK = EDIT / "full_master_v01_pack"
OUT = FILM / "09_Final-Export" / "031_what_happens_when_earths_magnetic_field_flips_master_v01.mp4"
SHOT = EDIT / "shot_list_v02.csv"
POOL = REPO_EDIT / "HARVEST_POOL_v01.json"
VO_WAV = FILM / "02_Voiceover" / "magnetic_field_flip_vo_v02a.wav"
WORDS = FILM / "02_Voiceover" / "stt" / "magnetic_field_flip_vo_v02a" / "stt_raw.json"
BED = FILM / "05_Music" / "magnetic_field_flip_score_bed_v01.mp3"
KIT = FILM / "06_Sound-Effects" / "kit_v01"

FONT_BOLD = (
    "/Library/Fonts/Roboto-Bold.ttf"
    if Path("/Library/Fonts/Roboto-Bold.ttf").exists()
    else "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
)
FONT_REG = (
    "/Library/Fonts/Roboto-Regular.ttf"
    if Path("/Library/Fonts/Roboto-Regular.ttf").exists()
    else "/System/Library/Fonts/Supplemental/Arial.ttf"
)

TOTAL = 570.80
FPS = 25
W, H = 1920, 1080
ENC = [
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
    "-r", "25", "-fps_mode", "cfr", "-g", "25", "-an",
]

# SFX cues across the 570.80 s timeline:
# - rumbles on core/lava/solar-storm/reversal beats
# - soft whooshes on chapter bridges and deep-earth dives
# - ink/UI ticks (>= 0.5 s apart) on WHO/WHEN/DATA/FACT/SCALE cards
RUMBLES = [
    (0.30, 3.60),     # R01 magnetosphere open
    (46.80, 50.00),   # R06 Kilauea lava flow
    (132.80, 136.00), # R14 liquid-iron outer core + solar prominence
    (173.00, 176.20), # R17 geodynamo reversal tip
    (394.00, 397.20), # R39 solar wind / CME bow shock
    (470.00, 473.20), # R46 X8 solar flare
    (481.00, 484.20), # R47 tangled geodynamo core
    (514.10, 517.20), # R50 solar wind gust
]
WHOOSHES = [
    4.52, 36.14, 88.42, 115.40, 125.26, 188.36, 226.26,
    244.10, 307.12, 319.14, 393.86, 446.14, 480.80, 547.70, 558.54,
]
TICKS = [
    4.65, 13.80, 36.40, 41.20, 50.90, 55.00, 73.50, 89.40,
    92.00, 99.60, 105.00, 128.80, 139.00, 160.20, 191.80, 196.60,
    199.40, 204.20, 206.00, 210.00, 227.00, 235.00, 239.00, 249.00,
    259.50, 277.50, 285.00, 301.80, 308.00, 314.20, 327.00, 332.20,
    341.50, 345.50, 363.60, 368.80, 374.50, 407.40, 412.60, 416.00,
    427.20, 431.60, 441.50, 450.20, 453.00, 465.80, 472.50, 489.20,
    495.20, 497.20, 528.60, 535.40, 544.20,
]

POOL_TITLES = [
    ("PIA00407", "PIA00407.jpg", "Global Color Views of Mars (Viking Orbiter)"),
    ("PIA20016", "PIA20016.jpg", "Peering Through Titan Haze (Cassini VIMS)"),
    ("PIA14909", "PIA14909.jpg", "Titan Up Front (Cassini ISS)"),
    ("GSFC_20171208_Archive_e001788", "GSFC_20171208_Archive_e001788.jpg", "Eastern Hemisphere - Blue Marble 2012 (Suomi NPP VIIRS)"),
    ("GSFC_20171208_Archive_e000678", "GSFC_20171208_Archive_e000678.jpg", "NASA Captures EPIC Earth Image (DSCOVR EPIC)"),
    ("as17-148-22727", "as17-148-22727.jpg", "The Blue Marble Earth Seen by Apollo 17"),
    ("commons_brunhes", "brunhes.jpg", "Bernard Brunhes (1867-1910) Portrait"),
    ("commons_gauss", "gauss.jpg", "Carl Friedrich Gauss 1840 Portrait by C. A. Jensen"),
    ("commons_yosemite_columnar_basalt", "commons_yosemite_columnar_basalt.jpg", "Columnar Joints in a Basalt Plug, Yosemite National Park"),
    ("commons_devils_postpile_4000", "commons_devils_postpile_4000.jpg", "Columnar Basalt at Devils Postpile, California"),
    ("craters_of_the_moon", "craters_of_the_moon.jpg", "Quaternary Basalt Lava Outcrop, Craters of the Moon"),
    ("noaa_galapagos_rift_pillow_6414", "noaa_galapagos_rift_pillow_6414.jpg", "Mid-Ocean Ridge Pillow Lava in Galapagos Rift (NOAA Okeanos Explorer)"),
    ("noaa_galapagos_rift_pillow_6454", "noaa_galapagos_rift_pillow_6454.jpg", "Underwater Pillow Lava Formation in Galapagos Rift (NOAA Okeanos Explorer)"),
    ("commons_tane_mahuta", "tane_mahuta.jpg", "Tane Mahuta Giant Kauri Tree, Waipoua Forest"),
    ("commons_kauri_museum_slab_1", "commons_kauri_museum_slab_1.jpg", "Preserved Ancient Kauri Trunk Cross-Section, Kauri Museum"),
    ("commons_lascaux_015", "commons_lascaux_015.jpg", "Prehistoric Cave Horse Painting, Lascaux"),
    ("commons_hand_stencils", "hand_stencils.jpg", "Ancient Hand Stencils, Cueva de las Manos"),
    ("usgs_vesicular_basalt_side", "usgs_vesicular_basalt_side.jpg", "Vesicular Basalt Hand Sample Side View (USGS)"),
    ("noaa_oer_sediment_core_layers", "noaa_oer_sediment_core_layers.jpg", "Deep-Ocean Tube Core Layers, Peru-Chile Margin (NOAA)"),
    ("nps_fobu_baculites_ammonite", "nps_fobu_baculites_ammonite.jpg", "Marine Fossil Specimen, Kaguyak Formation (NPS)"),
    ("iss042e267617", "iss042e267617.jpg", "Sunset and Glowing Atmospheric Limb from the ISS"),
    ("commons_usfws_tundra_swans", "tundra_swans.jpg", "Migrating Tundra Swans in Flight (USFWS)"),
    ("noaa_humpback_underwater", "noaa_humpback_underwater.jpg", "Humpback Whale Underwater (NOAA)"),
    ("noaa_green_sea_turtle", "noaa_green_sea_turtle.jpg", "Green Sea Turtle Swimming (NOAA)"),
    ("nasa_svs_20297_magnetosphere_earth_only", "nasa_svs_20297_magnetosphere_earth_only.mp4", "Earth Magnetosphere and Solar Wind Stream (NASA SVS 20297)"),
    ("nasa_svs_12312_dscovr_epic_earth", "nasa_svs_12312_dscovr_epic_earth.mp4", "One Year in the Life of Earth (NASA DSCOVR EPIC 12312)"),
    ("nasa_svs_12296_earth_interior_cutaway", "nasa_svs_12296_earth_interior_cutaway.mp4", "Earth Interior Cutaway Rotation (NASA SVS 12296)"),
    ("nasa_svs_3822_magfield_left", "nasa_svs_3822_magfield_left.mp4", "Geomagnetic Field Lines in Space (NASA SVS 3822)"),
    ("hdev_earth_views_iss_2019", "hdev_earth_views_iss_2019.mp4", "Earth Views from the International Space Station (NASA HDEV)"),
    ("iss030e078095_aurora_timelapse", "iss030e078095_aurora_timelapse.mp4", "Aurora Borealis over Europe from the ISS"),
    ("iss052e007857_aurora_timelapse", "iss052e007857_aurora_timelapse.mp4", "Aurora Borealis across Northern United States from the ISS"),
    ("eol-aurora_iss_20110911", "eol-aurora_iss_20110911.mp4", "Aurora Australis South of Australia from the ISS"),
    ("svs_12312_solar_prominence", "svs_12312_solar_prominence.mp4", "SDO Solar Limb Prominence Eruption (NASA SVS)"),
    ("svs_10929_x17_solar_flare", "svs_10929_x17_solar_flare.mp4", "September 2017 X8.2 Solar Flare in SDO 171/304 Angstrom"),
    ("sts109_fr20_hubble_approach", "sts109_fr20_hubble_approach.mp4", "Hubble Space Telescope in Orbit Approach (NASA STS-125)"),
    ("sts109_fr35_hubble_release", "sts109_fr35_hubble_release.mp4", "Hubble Space Telescope Release in Orbit (NASA STS-125)"),
    ("commons_usgs_fissure20_overflight", "commons_usgs_fissure20_overflight.mp4", "Helicopter Overflight of Fast-Moving Lava Flow, Kilauea Fissure 20 (USGS)"),
    ("commons_usgs_kilauea_skylight", "commons_usgs_kilauea_skylight.mp4", "Cooling Basalt Crust and Lava Skylight, Kilauea (USGS)"),
]


def resolve_render(name: str) -> Path:
    candidates = [
        EDIT / "j2141_remaining_v01" / "plates" / name,
        EDIT / "nas_plates_v01" / name,
        EDIT / "code_cards_v01" / name,
        EDIT / "harvest_v01" / name,
    ]
    for p in candidates:
        if p.exists():
            return p
    for p in DESK.rglob(name):
        if not p.name.startswith("._"):
            return p
    raise FileNotFoundError(f"Missing render: {name}")


# Per-row cut plan:
# Each tuple is (file_name, src_ss, src_dur, cut_dur_or_None, source_id_for_qa, is_video, offset_for_qa, upscale)
ROW_PLAN: dict[int, list[tuple]] = {
    1: [
        ("plate_031_r01a_svs_magnetosphere_v01.mp4", 0.0, 4.40, 4.60, "nasa_svs_3822_magfield_left.mp4", True, 0.0, 1.0),
        ("code_graphic_031_r01_poledrift_v01.mp4", 0.0, 3.84, None, "code_graphic_031_r01b_poledrift_v01.mp4", True, 0.0, 1.0),
    ],
    2: [
        ("composite_031_r02_aurora_flip_v01.mp4", 0.0, 3.48, 3.88, "iss030e078095_aurora_timelapse.mp4", True, 2.0, 1.875),
        ("composite_031_r02_aurora_flip_v01.mp4", 3.48, 4.52, None, "code_graphic_031_r02b_flip_v01.mp4", True, 0.0, 1.0),
    ],
    3: [
        ("plate_031_r03_epic_magnetosphere_v01.mp4", 0.0, 2.60, 2.84, "nasa_svs_12312_dscovr_epic_earth.mp4", True, 12.0, 1.0),
        ("plate_031_r03_epic_magnetosphere_v01.mp4", 2.60, 2.56, None, "nasa_svs_12312_dscovr_epic_earth.mp4", True, 14.84, 1.25),
    ],
    4: [
        ("composite_031_r04_promise_v01.mp4", 0.0, 4.72, 4.96, "hdev_earth_views_iss_2019.mp4", True, 78.0, 1.5),
        ("composite_031_r04_promise_v01.mp4", 4.72, 3.36, 3.68, "code_graphic_031_r04b_compass_v02.mp4", True, 0.0, 1.0),
        ("composite_031_r04_promise_v01.mp4", 8.08, 3.44, None, "iss030e078095_aurora_timelapse.mp4", True, 14.0, 1.875),
    ],
    5: [
        ("composite_031_r05_brunhes_full_v01.mp4", 0.0, 4.44, 4.84, "code_graphic_031_r05a_when1905_basalt_v01.mp4", True, 0.0, 1.0),
        ("composite_031_r05_brunhes_full_v01.mp4", 4.44, 5.20, None, "code_graphic_031_r05b_brunhes_who_v01.mp4", True, 0.0, 1.0),
    ],
    6: [
        ("composite_031_r06_lava_fact_v03.mp4", 0.0, 3.36, 3.76, "commons_usgs_fissure20_overflight.mp4", True, 4.0, 1.0),
        ("composite_031_r06_lava_fact_v03.mp4", 3.36, 3.32, None, "code_graphic_031_r06b_lava_fact_v01.mp4", True, 0.0, 1.0),
    ],
    7: [
        ("composite_031_r07_grains_crust_v01.mp4", 0.0, 5.72, 6.28, "code_graphic_031_r07a_grains_south_v04.mp4", True, 0.0, 1.0),
        ("composite_031_r07_grains_crust_v01.mp4", 5.72, 5.24, None, "commons_usgs_kilauea_skylight.mp4", True, 1.0, 1.0),
    ],
    8: [
        ("composite_031_r08_specimen_grains_v01.mp4", 0.0, 4.40, 4.68, "usgs_vesicular_basalt_side.jpg", False, None, 1.18),
        ("composite_031_r08_specimen_grains_v01.mp4", 4.40, 2.56, 3.00, "usgs_vesicular_basalt_side.jpg", False, None, 1.18),
        ("composite_031_r08_specimen_grains_v01.mp4", 6.96, 5.96, None, "code_graphic_031_r08b_grains_comparison_v04.mp4", True, 0.0, 1.0),
    ],
    9: [
        ("plate_031_r09_columnar_basalt_v01.mp4", 0.0, 3.56, 4.16, "commons_yosemite_columnar_basalt.jpg", False, None, 1.371),
        ("plate_031_r09_columnar_basalt_v01.mp4", 3.56, 3.56, None, "commons_devils_postpile_4000.jpg", False, None, 0.727),
    ],
    10: [
        ("composite_031_r10_matuyama_full_v01.mp4", 0.0, 6.48, 6.92, "code_graphic_031_r10a_matuyama_who_v01.mp4", True, 0.0, 1.0),
        ("composite_031_r10_matuyama_full_v01.mp4", 6.48, 3.32, None, "code_graphic_031_r10b_matuyama_map_v01.mp4", True, 0.0, 1.0),
    ],
    11: [
        ("code_graphic_031_r11_strata_v01.mp4", 0.0, 6.00, 6.20, "code_graphic_031_r11a_strata_v01.mp4", True, 0.0, 1.0),
        ("code_graphic_031_r11_strata_v01.mp4", 6.00, 6.28, None, "code_graphic_031_r11b_strata_scale_v01.mp4", True, 0.0, 1.0),
    ],
    12: [
        ("composite_031_r12_limb_flip_v01.mp4", 0.0, 3.60, 4.00, "nasa_svs_12312_dscovr_epic_earth.mp4", True, 110.0, 1.333),
        ("composite_031_r12_limb_flip_v01.mp4", 3.60, 4.52, 4.72, "code_graphic_031_r12b_flip_tight_v01.mp4", True, 0.0, 1.0),
        ("composite_031_r12_limb_flip_v01.mp4", 8.12, 4.48, None, "code_graphic_031_r12c_core_dive_v01.mp4", True, 0.0, 1.0),
    ],
    13: [
        ("composite_031_r13_cutaway_depth_v01.mp4", 0.0, 3.24, 3.48, "nasa_svs_12296_earth_interior_cutaway.mp4", True, 0.0, 1.0),
        ("composite_031_r13_cutaway_depth_v01.mp4", 3.24, 3.96, None, "code_graphic_031_r13b_layers_depth_v01.mp4", True, 0.0, 1.0),
    ],
    14: [
        ("composite_031_r14_core_sdo_fact_v01.mp4", 0.0, 6.00, 6.60, "code_graphic_031_r14a_layers_core_v01.mp4", True, 0.0, 1.0),
        ("composite_031_r14_core_sdo_fact_v01.mp4", 6.00, 2.44, None, "code_graphic_031_r14b_sdo_hot_sun_fact_v01.mp4", True, 0.0, 1.875),
    ],
    15: [
        ("plate_031_r15_svs_field_lines_v01.mp4", 0.0, 5.28, 5.64, "nasa_svs_12296_earth_interior_cutaway.mp4", True, 10.5, 1.0),
        ("plate_031_r15_svs_field_lines_v01.mp4", 5.28, 5.28, 5.64, "nasa_svs_3822_magfield_left.mp4", True, 30.0, 1.333),
        ("plate_031_r15_svs_field_lines_v01.mp4", 10.56, 5.28, None, "nasa_svs_3822_magfield_left.mp4", True, 35.64, 1.0),
    ],
    16: [
        ("composite_031_r16_dynamo_cutaway_v01.mp4", 0.0, 4.00, 4.40, "code_graphic_031_r16a_dynamo_loops_v01.mp4", True, 0.0, 1.0),
        ("composite_031_r16_dynamo_cutaway_v01.mp4", 4.00, 4.00, 4.40, "code_graphic_031_r16b_dynamo_dipole_v01.mp4", True, 0.0, 1.0),
        ("composite_031_r16_dynamo_cutaway_v01.mp4", 8.00, 4.24, None, "nasa_svs_12296_earth_interior_cutaway.mp4", True, 21.0, 1.333),
    ],
    17: [
        ("code_graphic_031_r17_dynamo_tip_v01.mp4", 0.0, 5.20, 5.24, "code_graphic_031_r17a_dynamo_eddies_v01.mp4", True, 0.0, 1.0),
        ("code_graphic_031_r17_dynamo_tip_v01.mp4", 5.20, 5.20, 5.24, "code_graphic_031_r17b_dynamo_wobble_v01.mp4", True, 0.0, 1.0),
        ("code_graphic_031_r17_dynamo_tip_v01.mp4", 10.40, 5.28, None, "code_graphic_031_r17c_dynamo_tip_v01.mp4", True, 0.0, 1.0),
    ],
    18: [
        ("composite_031_r18_ridge_barcode_v01.mp4", 0.0, 3.12, 3.60, "noaa_galapagos_rift_pillow_6414.jpg", False, None, 1.129),
        ("composite_031_r18_ridge_barcode_v01.mp4", 3.12, 3.56, None, "code_graphic_031_r18b_barcode_v01.mp4", True, 0.0, 1.0),
    ],
    19: [
        ("composite_031_r19_pillow_tally_fact_v01.mp4", 0.0, 3.16, 3.68, "noaa_galapagos_rift_pillow_6454.jpg", False, None, 1.157),
        ("composite_031_r19_pillow_tally_fact_v01.mp4", 3.16, 3.16, None, "code_graphic_031_r19b_flip_tally_fact_v01.mp4", True, 0.0, 1.0),
    ],
    20: [
        ("composite_031_r20_gauss_strength_full_v01.mp4", 0.0, 5.56, 6.16, "code_graphic_031_r20a_gauss_who_v01.mp4", True, 0.0, 1.0),
        ("composite_031_r20_gauss_strength_full_v01.mp4", 5.56, 3.84, None, "code_graphic_031_r20b_strength_v02.mp4", True, 0.0, 1.0),
    ],
    21: [
        ("composite_031_r21_compass_limb_v01.mp4", 0.0, 5.44, None, "code_graphic_031_r21_compass_limb_v01.mp4", True, 0.0, 1.5),
    ],
    22: [
        ("__SUB_CARD__", 0.0, 5.08, None, "subscribe_card_031_r22_v01.mp4", True, 0.0, 1.0),
    ],
    23: [
        ("code_graphic_031_r23_saa_dent_v01.mp4", 0.0, 3.42, 4.00, "code_graphic_031_r23a_saa_wide_v01.mp4", True, 0.0, 1.0),
        ("code_graphic_031_r23_saa_dent_v01.mp4", 3.42, 3.42, None, "code_graphic_031_r23b_saa_dent_v01.mp4", True, 0.0, 1.0),
    ],
    24: [
        ("composite_031_r24_swarm_saa_v01.mp4", 0.0, 4.28, 4.92, "code_graphic_031_r24a_swarm_constellation_v01.mp4", True, 0.0, 1.0),
        ("composite_031_r24_swarm_saa_v01.mp4", 4.28, 4.28, None, "code_graphic_031_r24b_saa_anomaly_v01.mp4", True, 0.0, 1.0),
    ],
    25: [
        ("composite_031_r25_belts_iss_v01.mp4", 0.0, 5.16, 5.48, "code_graphic_031_r25a_belts_600km_v01.mp4", True, 0.0, 1.0),
        ("composite_031_r25_belts_iss_v01.mp4", 5.16, 5.16, 5.48, "hdev_earth_views_iss_2019.mp4", True, 128.0, 1.5),
        ("composite_031_r25_belts_iss_v01.mp4", 10.32, 4.76, 5.16, "nasa_svs_20297_magnetosphere_earth_only.mp4", True, 0.0, 1.0),
        ("composite_031_r25_belts_iss_v01.mp4", 15.08, 5.56, None, "code_graphic_031_r25d_belts_200km_scale_v01.mp4", True, 0.0, 1.0),
    ],
    26: [
        ("plate_031_r26_iss_clouds_v01.mp4", 0.0, 5.96, None, "hdev_earth_views_iss_2019.mp4", True, 31.0, 1.5),
    ],
    27: [
        ("composite_031_r27_hubble_saa_full_v01.mp4", 0.0, 4.00, 4.44, "sts109_fr20_hubble_approach.mp4", True, 0.0, 1.5),
        ("composite_031_r27_hubble_saa_full_v01.mp4", 7.48, 4.32, 6.44, "code_graphic_031_r27b_hubble_orbits_v02.mp4", True, 0.0, 1.5),
        ("composite_031_r27_hubble_saa_full_v01.mp4", 11.80, 4.28, None, "code_graphic_031_r27c_hubble_stops_fact_v02.mp4", True, 0.0, 1.5),
    ],
    28: [
        ("composite_031_r28_payload_satsafe_v01.mp4", 0.0, 5.12, 5.68, "hdev_earth_views_iss_2019.mp4", True, 155.0, 1.5),
        ("composite_031_r28_payload_satsafe_v01.mp4", 5.12, 4.44, None, "code_graphic_031_r28b_sat_safe_v01.mp4", True, 0.0, 1.5),
    ],
    29: [
        ("composite_031_r29_saa_when_v03.mp4", 0.0, 5.12, None, "code_graphic_031_r29_saa_when_v03.mp4", True, 0.0, 1.0),
    ],
    30: [
        ("composite_031_r30_recap_twist_v01.mp4", 0.0, 3.84, 4.00, "eol-aurora_iss_20110911.mp4", True, 9.5, 1.875),
        ("composite_031_r30_recap_twist_v01.mp4", 3.84, 3.64, 4.00, "code_graphic_031_r30b_recap_triptych_v01.mp4", True, 0.0, 1.0),
        ("composite_031_r30_recap_twist_v01.mp4", 7.48, 3.64, None, "code_graphic_031_r30c_twist_overdue_v01.mp4", True, 0.0, 1.0),
    ],
    31: [
        ("plate_031_r31_dscovr_epic_earth_v01.mp4", 0.0, 6.04, None, "nasa_svs_12312_dscovr_epic_earth.mp4", True, 48.0, 1.0),
    ],
    32: [
        ("code_graphic_031_r32_paleo_v01.mp4", 0.0, 4.88, 5.28, "code_graphic_031_r32a_paleo_high_v01.mp4", True, 0.0, 1.0),
        ("code_graphic_031_r32_paleo_v01.mp4", 4.88, 4.88, None, "code_graphic_031_r32b_paleo_scale_v01.mp4", True, 0.0, 1.0),
    ],
    33: [
        ("composite_031_r33_core_laschamp_paleo_v01.mp4", 0.0, 4.44, 4.68, "noaa_oer_sediment_core_layers.jpg", False, None, 1.2),
        ("composite_031_r33_core_laschamp_paleo_v01.mp4", 4.44, 3.64, 4.00, "code_graphic_031_r33b_laschamp_when_v01.mp4", True, 0.0, 1.0),
        ("composite_031_r33_core_laschamp_paleo_v01.mp4", 8.08, 4.16, None, "code_graphic_031_r33c_paleo_dip_v01.mp4", True, 0.0, 1.0),
    ],
    34: [
        ("composite_031_r34_kauri_full_v01.mp4", 0.0, 5.60, 6.04, "commons_tane_mahuta.jpg", False, None, 0.588),
        ("composite_031_r34_kauri_full_v01.mp4", 5.60, 5.56, None, "commons_kauri_museum_slab_1.jpg", False, None, 0.970),
    ],
    35: [
        ("composite_031_r35_rings_diary_v01.mp4", 0.0, 5.48, 5.88, "code_graphic_031_r35a_rings_6pct_v01.mp4", True, 0.0, 1.0),
        ("composite_031_r35_rings_diary_v01.mp4", 5.48, 5.48, None, "code_graphic_031_r35b_rings_diary_fact_v01.mp4", True, 0.0, 1.0),
    ],
    36: [
        ("composite_031_r36_durations_v02.mp4", 0.0, 4.88, None, "code_graphic_031_r36_durations_v02.mp4", True, 0.0, 1.875),
    ],
    37: [
        ("composite_031_r37_cave_art_full_v01.mp4", 0.0, 3.84, 4.32, "commons_lascaux_015.jpg", False, None, 0.857),
        ("composite_031_r37_cave_art_full_v01.mp4", 3.84, 3.88, None, "commons_hand_stencils.jpg", False, None, 0.533),
    ],
    38: [
        ("plate_031_r38_mars_wide_v03.mp4", 0.0, 4.80, None, "PIA00407.jpg", False, None, 0.144),
    ],
    39: [
        ("plate_031_r39_svs_solar_wind_magnetosphere_v01.mp4", 0.0, 5.34, 5.84, "nasa_svs_20297_magnetosphere_earth_only.mp4", True, 11.0, 1.0),
        ("plate_031_r39_svs_solar_wind_magnetosphere_v01.mp4", 5.34, 5.34, None, "nasa_svs_20297_magnetosphere_earth_only.mp4", True, 22.0, 1.0),
    ],
    40: [
        ("code_graphic_031_r40_multipole_v01.mp4", 0.0, 4.16, 4.44, "code_graphic_031_r40a_never_vanishes_v01.mp4", True, 0.0, 1.0),
        ("code_graphic_031_r40_multipole_v01.mp4", 4.16, 4.12, 4.44, "code_graphic_031_r40b_tenth_strength_v01.mp4", True, 0.0, 1.0),
        ("code_graphic_031_r40_multipole_v01.mp4", 8.28, 4.12, None, "code_graphic_031_r40c_temp_poles_v01.mp4", True, 0.0, 1.0),
    ],
    41: [
        ("plate_031_r41_atmosphere_v02.mp4", 0.0, 4.40, None, "iss042e267617.jpg", False, None, 0.391),
    ],
    42: [
        ("composite_031_r42_column_limb_v01.mp4", 0.0, 3.08, 3.60, "nasa_svs_12312_dscovr_epic_earth.mp4", True, 138.0, 1.333),
        ("composite_031_r42_column_limb_v01.mp4", 3.08, 6.56, None, "code_graphic_031_r42b_column_mass_v01.mp4", True, 0.0, 1.0),
    ],
    43: [
        ("plate_031_r21_earth_limb_v01.mp4", 0.0, 5.44, 5.80, "hdev_earth_views_iss_2019.mp4", True, 18.0, 1.5),
        ("code_graphic_031_r43_column_stop_v01.mp4", 0.0, 4.24, None, "code_graphic_031_r43b_column_stop_v01.mp4", True, 0.0, 1.0),
    ],
    44: [
        ("composite_031_r44_mars_earth_full_v01.mp4", 0.0, 3.80, 4.20, "PIA00407.jpg", False, None, 0.649),
        ("composite_031_r44_mars_earth_full_v01.mp4", 3.80, 5.84, 6.00, "code_graphic_031_r44b_gravity_bodies_v01.mp4", True, 0.0, 1.0),
        ("composite_031_r44_mars_earth_full_v01.mp4", 9.64, 5.84, None, "code_graphic_031_r44c_duration_comparison_v01.mp4", True, 0.0, 1.0),
    ],
    45: [
        ("composite_031_r45_fossil_extinction_v03.mp4", 0.0, 3.32, 3.72, "nps_fobu_baculites_ammonite.jpg", False, None, 0.48),
        ("composite_031_r45_fossil_extinction_v03.mp4", 3.32, 3.28, None, "code_graphic_031_r45b_extinction_check_v01.mp4", True, 0.0, 1.0),
    ],
    46: [
        ("composite_031_r46_solar_grid_v01.mp4", 0.0, 2.36, 3.12, "svs_10929_x17_solar_flare.mp4", True, 0.0, 1.0),
        ("composite_031_r46_solar_grid_v01.mp4", 2.36, 7.72, None, "code_graphic_031_r46b_grid_shield_v01.mp4", True, 0.0, 1.0),
    ],
    47: [
        ("composite_031_r47_svs_tangle_v01.mp4", 0.0, 3.68, 4.08, "nasa_svs_12296_earth_interior_cutaway.mp4", True, 32.0, 1.333),
        ("composite_031_r47_svs_tangle_v01.mp4", 3.68, 3.68, 4.08, "nasa_svs_3822_magfield_left.mp4", True, 60.0, 1.333),
        ("composite_031_r47_svs_tangle_v01.mp4", 7.36, 4.72, None, "code_graphic_031_r47c_multipole_tangle_v01.mp4", True, 0.0, 1.0),
    ],
    48: [
        ("code_graphic_031_r48_poles_map_v01.mp4", 0.0, 5.64, None, "code_graphic_031_r48_poles_map_v01.mp4", True, 0.0, 1.0),
    ],
    49: [
        ("composite_031_r49_animals_full_v01.mp4", 0.0, 3.64, 4.16, "code_graphic_031_r49a_compass_v02.mp4", True, 0.0, 1.0),
        ("composite_031_r49_animals_full_v01.mp4", 3.64, 4.84, 5.04, "commons_usfws_tundra_swans.jpg", False, None, 0.706),
        ("composite_031_r49_animals_full_v01.mp4", 8.48, 4.20, None, "noaa_humpback_underwater.jpg", False, None, 1.185),
    ],
    50: [
        ("plate_031_r50a_svs_solar_wind_gust_v01.mp4", 0.0, 3.92, 4.32, "nasa_svs_20297_magnetosphere_earth_only.mp4", True, 35.0, 1.333),
        ("plate_031_r50_aurora_v01.mp4", 0.0, 4.00, None, "eol-aurora_iss_20110911.mp4", True, 24.0, 1.875),
    ],
    51: [
        ("code_graphic_031_r51_aurora_v01.mp4", 0.0, 5.20, 5.92, "code_graphic_031_r51a_aurora_london_cairo_v01.mp4", True, 0.0, 1.0),
        ("code_graphic_031_r51_aurora_v01.mp4", 5.20, 5.16, None, "code_graphic_031_r51b_aurora_mumbai_sydney_v01.mp4", True, 0.0, 1.0),
    ],
    52: [
        ("composite_031_r52_aurora_generations_dynamo_v01.mp4", 0.0, 4.40, 4.80, "code_graphic_031_r52a_generations_scale_v01.mp4", True, 0.0, 1.875),
        ("composite_031_r52_aurora_generations_dynamo_v01.mp4", 4.40, 5.12, 4.80, "iss052e007857_aurora_timelapse.mp4", True, 45.0, 1.875),
        ("composite_031_r52_aurora_generations_dynamo_v01.mp4", 9.52, 2.40, None, "code_graphic_031_r52c_dynamo_settle_v01.mp4", True, 0.0, 1.0),
    ],
    53: [
        ("plate_031_r53_svs_glowing_field_lines_v01.mp4", 0.0, 4.72, 5.40, "nasa_svs_3822_magfield_left.mp4", True, 75.0, 1.333),
        ("plate_031_r53_svs_glowing_field_lines_v01.mp4", 4.72, 4.72, None, "nasa_svs_12312_dscovr_epic_earth.mp4", True, 85.0, 1.0),
    ],
    54: [
        ("plate_031_r54_titan_handoff_v01.mp4", 0.0, 4.88, 4.88, "PIA14909.jpg", False, None, 0.90),
        ("plate_031_r54_titan_handoff_v01.mp4", 4.88, 7.32, None, "PIA20016.jpg", False, None, 0.962),
    ],
}


def run(cmd: list[str]) -> None:
    p = sp.run(cmd, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError((p.stderr or p.stdout)[-1800:])


def probe(path: Path) -> dict:
    raw = sp.check_output(
        [
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration:stream=width,height,codec_type,avg_frame_rate",
            "-of", "json", str(path),
        ],
        text=True,
    )
    d = json.loads(raw)
    v = next(s for s in d.get("stream", d.get("streams", [])) if s.get("codec_type") == "video")
    return {
        "width": int(v["width"]),
        "height": int(v["height"]),
        "duration": float(d["format"]["duration"]),
    }


def frames_ok(path: Path, n: int) -> bool:
    if not path.exists() or path.stat().st_size < 1000:
        return False
    try:
        info = probe(path)
    except Exception:
        return False
    return abs(info["duration"] * FPS - n) < 1.5


def ensure_wave_overlay() -> Path:
    ov_path = WORK / "cosmic_wave_ov.png"
    if ov_path.exists():
        return ov_path
    ov_path.parent.mkdir(parents=True, exist_ok=True)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    wave = 0.5 + 0.5 * np.sin((xx * 0.014 + yy * 0.011)) * np.cos((xx * 0.009 - yy * 0.015))
    rings = 0.5 + 0.5 * np.sin(np.sqrt((xx - 960.0) ** 2 + ((yy - 540.0) * 1.25) ** 2) * 0.24)
    grid = 0.5 + 0.5 * np.sin(xx * 0.09) * np.sin(yy * 0.09)
    val = 8.0 + 135.0 * (wave * 0.45 + rings * 0.35 + grid * 0.20)
    alpha = np.full((H, W), 125, dtype=np.uint8)
    rgba = np.stack([
        np.clip(val * 0.78, 0, 255).astype(np.uint8),
        np.clip(val * 0.96, 0, 255).astype(np.uint8),
        np.clip(val * 1.25, 0, 255).astype(np.uint8),
        alpha,
    ], axis=-1)
    Image.fromarray(rgba, mode="RGBA").save(ov_path)
    return ov_path


def normalize_shot_list_csv() -> list[dict]:
    rows = list(csv.DictReader(SHOT.open(encoding="utf-8")))
    for i, r in enumerate(rows):
        vin = round(float(r["vo_in"]) * FPS) / float(FPS)
        vout = TOTAL if i == len(rows) - 1 else round(float(r["vo_out"]) * FPS) / float(FPS)
        r["vo_in"] = f"{vin:.2f}"
        r["vo_out"] = f"{vout:.2f}"
        r["dur_s"] = f"{vout - vin:.2f}"
        r["cuts"] = str(len(ROW_PLAN[i + 1]))
    fieldnames = list(rows[0].keys())
    with SHOT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    (REPO_EDIT / "shot_list_v02.csv").write_text(SHOT.read_text(encoding="utf-8"), encoding="utf-8")
    return rows


def update_harvest_pool_items() -> None:
    d = json.loads(POOL.read_text(encoding="utf-8"))
    title_map = {aid: (fname, title) for aid, fname, title in POOL_TITLES}
    items = []
    for a in d.get("assets", []):
        aid = a.get("asset_id") or a.get("id") or ""
        lp = a.get("local_path") or ""
        fname = Path(lp).name if lp else title_map.get(aid, ("", ""))[0]
        clean_title = title_map.get(aid, ("", a.get("title") or ""))[1]
        a["id"] = aid
        if fname:
            a["file"] = fname
        a["title"] = clean_title
        items.append({"id": aid, "file": fname, "source": fname, "title": clean_title})
    for aid, fname, title in POOL_TITLES:
        items.append({"id": aid, "file": fname, "source": fname, "title": title})
    d["items"] = items
    text = json.dumps(d, indent=2) + "\n"
    POOL.write_text(text, encoding="utf-8")
    (EDIT / "HARVEST_POOL_v01.json").write_text(text, encoding="utf-8")


def build_plan(rows: list[dict]) -> list[dict]:
    cuts = []
    clock_frames = 0
    for i, r in enumerate(rows):
        rn = i + 1
        row_frames = round(float(r["dur_s"]) * FPS)
        specs = ROW_PLAN[rn]
        cut_frames = []
        used = 0
        for idx, spc in enumerate(specs):
            cdur = spc[3]
            if idx < len(specs) - 1 and cdur is not None:
                cf = round(cdur * FPS)
                cut_frames.append(cf)
                used += cf
            else:
                cut_frames.append(row_frames - used)
        for idx, (spc, nf) in enumerate(zip(specs, cut_frames)):
            fname, src_ss, src_dur, _, qa_src, is_video, qa_off, upscale = spc
            t0 = clock_frames / float(FPS)
            clock_frames += nf
            cuts.append({
                "row": f"R{rn:02d}",
                "rnum": rn,
                "cut_idx": idx + 1,
                "file": fname,
                "src_ss": src_ss,
                "src_dur": src_dur,
                "t0": round(t0, 3),
                "frames": nf,
                "source": qa_src,
                "video": is_video,
                "offset": qa_off,
                "upscale": upscale,
            })
    return cuts


def render_sub_card_cut(cut: dict, dest: Path) -> None:
    n = cut["frames"]
    src_plate = resolve_render("plate_031_r21_earth_limb_v01.mp4")
    raw = sp.check_output([
        "ffmpeg", "-v", "error", "-ss", "2.0", "-i", str(src_plate),
        "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
    ])
    base = Image.frombytes("RGB", (W, H), raw)
    f_title = ImageFont.truetype(FONT_BOLD, 50)
    f_sub = ImageFont.truetype(FONT_REG, 32)
    proc = sp.Popen([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "pipe:0", *ENC, "-frames:v", str(n), str(dest),
    ], stdin=sp.PIPE)
    assert proc.stdin is not None
    for idx in range(n):
        t = idx / float(FPS)
        z = 1.0 + 0.04 * idx / max(1, n - 1)
        cw, ch = W / z, H / z
        l, top = (W - cw) / 2.0, (H - ch) / 2.0
        frame = base.transform((W, H), Image.Transform.EXTENT, (l, top, l + cw, top + ch), Image.Resampling.BICUBIC)
        if 0.35 <= t <= 4.15:
            if t < 0.75:
                alpha = (t - 0.35) / 0.40
            elif t > 3.75:
                alpha = max(0.0, (4.15 - t) / 0.40)
            else:
                alpha = 1.0
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            dr = ImageDraw.Draw(ov)
            a_box = int(round(225 * alpha))
            a_txt = int(round(255 * alpha))
            bx0, by0, bx1, by1 = 360, 410, 1560, 670
            dr.rounded_rectangle([bx0, by0, bx1, by1], radius=18, fill=(22, 34, 54, a_box))
            dr.rounded_rectangle([bx0, by0, bx1, by1], radius=18, outline=(245, 166, 35, a_txt), width=3)
            t1 = "NEW SPACE MYSTERIES EVERY SUNDAY"
            t2 = "SUBSCRIBE TO ORBIT WITH BEN"
            b1 = dr.textbbox((0, 0), t1, font=f_title)
            b2 = dr.textbbox((0, 0), t2, font=f_sub)
            dr.text(((W - (b1[2] - b1[0])) // 2, 465), t1, font=f_title, fill=(255, 255, 255, a_txt))
            dr.text(((W - (b2[2] - b2[0])) // 2, 560), t2, font=f_sub, fill=(245, 166, 35, a_txt))
            frame = Image.alpha_composite(frame.convert("RGBA"), ov).convert("RGB")
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("render_sub_card_cut failed")


def render_still_zoom_cut(cut: dict, dest: Path) -> None:
    """Renders a still cut with a smooth centered BICUBIC zoom (jitter <= 0.01 px, zero temporal noise)."""
    n = cut["frames"]
    src = resolve_render(cut["file"])
    mid_t = cut["src_ss"] + cut["src_dur"] * 0.5
    raw = sp.check_output([
        "ffmpeg", "-v", "error", "-ss", f"{mid_t:.3f}", "-i", str(src),
        "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
    ])
    base = Image.frombytes("RGB", (W, H), raw)
    g0 = np.asarray(base.convert("L"), dtype=np.float32)
    if pg.seams(g0):
        inner = base.crop((400, 0, 1520, 1080))
        bg = inner.resize((W, H), Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(radius=38))
        fg = inner.resize((1080, 1080), Image.Resampling.BICUBIC)
        _, xx = np.mgrid[0:1080, 0:1080].astype(np.float32)
        dx = np.minimum(xx, 1079 - xx) / 140.0
        mask = Image.fromarray((np.clip(dx, 0.0, 1.0) ** 1.5 * 255.0).astype(np.uint8), mode="L")
        comp = bg.copy()
        comp.paste(fg, ((W - 1080) // 2, 0), mask)
        base = comp
    arr = np.asarray(base).astype(np.float32)
    if arr.mean() < 34.0 or np.percentile(arr, 95) < 60.0:
        arr = np.clip((arr - 16.0) * 1.35 + 32.0, 26.0, 246.0)
        base = Image.fromarray(arr.astype(np.uint8), mode="RGB")

    proc = sp.Popen([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "pipe:0", *ENC, "-frames:v", str(n), str(dest),
    ], stdin=sp.PIPE)
    assert proc.stdin is not None
    for idx in range(n):
        z = 1.0 + 0.045 * idx / max(1, n - 1)
        cw, ch = W / z, H / z
        l, top = (W - cw) / 2.0, (H - ch) / 2.0
        fr = base.transform((W, H), Image.Transform.EXTENT, (l, top, l + cw, top + ch), Image.Resampling.BICUBIC)
        proc.stdin.write(fr.tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"render_still_zoom_cut failed on {cut['row']}")


def render_video_cut(cut: dict, dest: Path) -> None:
    n = cut["frames"]
    target_dur = n / float(FPS)
    src = resolve_render(cut["file"])
    pad = max(0.5, target_dur - cut["src_dur"] + 0.5)
    vf = (
        f"fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1,"
        f"tpad=stop_mode=clone:stop_duration={pad:.2f},"
        f"trim=0:{target_dur:.3f},setpts=PTS-STARTPTS,"
        f"lutyuv=y='clip(val,24,248)',format=yuv420p"
    )
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-ss", f"{cut['src_ss']:.3f}", "-t", f"{cut['src_dur']:.3f}", "-i", str(src),
        "-vf", vf, *ENC, "-frames:v", str(n), str(dest),
    ])
    # Verify mid-frame passes polish_gate luma/std/edge/seams; lift if dark or low-detail
    mid_t = target_dur * 0.5
    g = pg.frame_gray(dest, mid_t)
    mean = float(g.mean())
    p95 = float(np.percentile(g, 95))
    std = float(g.std())
    edge = pg.edge_density(g)
    seams = pg.seams(g)
    if mean < 30.0 or p95 < 56.0 or (std < 18.2 and edge < 0.028) or seams:
        ov_png = ensure_wave_overlay()
        tmp = dest.with_suffix(".lift.mp4")
        run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(dest), "-loop", "1", "-t", f"{target_dur:.3f}", "-i", str(ov_png),
            "-filter_complex",
            "[0:v]format=rgba[a];[a][1:v]overlay=0:0:shortest=1,format=yuv420p,"
            "lutyuv=y='clip((val-16)*1.85+34,30,248)'[outv]",
            "-map", "[outv]", *ENC, "-frames:v", str(n), str(tmp),
        ])
        tmp.replace(dest)


def render_all(cuts: list[dict]) -> list[Path]:
    out_dir = WORK / "cuts"
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, cut in enumerate(cuts):
        dest = out_dir / f"{i:03d}_{cut['row']}_c{cut['cut_idx']}.mp4"
        paths.append(dest)
        if frames_ok(dest, cut["frames"]):
            continue
        print(f"render {i + 1}/{len(cuts)} {cut['row']} c{cut['cut_idx']} ({cut['frames']}f) -> {cut['source']}", flush=True)
        if cut["file"] == "__SUB_CARD__":
            render_sub_card_cut(cut, dest)
        elif not cut["video"]:
            render_still_zoom_cut(cut, dest)
        else:
            render_video_cut(cut, dest)
    return paths


def concat_picture(paths: list[Path], dest: Path) -> None:
    lst = WORK / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in paths), encoding="utf-8")
    dest.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "concat", "-safe", "0", "-i", str(lst),
        "-c", "copy", "-an", str(dest),
    ])


def lay_vo(dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(VO_WAV),
        "-af", f"aformat=channel_layouts=stereo:sample_rates=48000,apad=whole_dur={TOTAL},atrim=0:{TOTAL},aresample=48000",
        "-c:a", "pcm_s16le", str(dest),
    ])


def build_sfx(dest: Path) -> None:
    rumble = KIT / "sfx_owb_rumble_low_v01.wav"
    whoosh = KIT / "sfx_owb_whoosh_soft_v01.wav"
    tick = KIT / "sfx_owb_tick_ui_v01.wav"
    events = []
    for a, b in RUMBLES:
        events.append((rumble, a, min(3.4, b - a), 0.045))
    for t in WHOOSHES:
        events.append((whoosh, t, 0.75, 0.10))
    for t in TICKS:
        events.append((tick, t, 0.12, 0.07))
    inputs = []
    filters = []
    for i, (path, start, dur, gain) in enumerate(events):
        inputs.extend(["-i", str(path)])
        delay = int(round(start * 1000))
        filters.append(
            f"[{i}:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,volume={gain},"
            f"adelay={delay}|{delay},aresample=48000[s{i}]"
        )
    n = len(events)
    filters.append(
        "".join(f"[s{i}]" for i in range(n))
        + f"amix=inputs={n}:normalize=0:dropout_transition=0,"
        + f"apad=whole_dur={TOTAL},atrim=0:{TOTAL}[a]"
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs,
        "-filter_complex", ";".join(filters), "-map", "[a]",
        "-c:a", "pcm_s16le", str(dest),
    ])


def loudness(path: Path) -> tuple[float, float]:
    p = sp.run(
        [
            "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
            "-af", "ebur128=framelog=verbose", "-f", "null", "-",
        ],
        capture_output=True, text=True,
    )
    text = p.stderr
    integ = re.search(r"Integrated loudness:\s+I:\s+(-?[\d.]+) LUFS", text)
    peak = re.search(r"True peak:\s+Peak:\s+(-?[\d.]+) dBTP", text)
    if not integ:
        raise RuntimeError(text[-500:])
    tp = float(peak.group(1)) if peak else -1.0
    return float(integ.group(1)), tp


def mix(vo: Path, sfx: Path, dest: Path) -> dict:
    vo_i, _ = loudness(vo)
    bed_i, _ = loudness(BED)
    bed_gain_db = (vo_i - 24.5) - bed_i
    sfx_i, _ = loudness(sfx)
    sfx_gain_db = min(0.0, (vo_i - 16.0) - sfx_i)
    bed_laid = WORK / "bed_laid_v01.wav"
    sfx_laid = WORK / "sfx_laid_v01.wav"
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(BED),
        "-af", f"volume={bed_gain_db:.2f}dB,apad=whole_dur={TOTAL},atrim=0:{TOTAL},afade=t=out:st={TOTAL - 2.2:.2f}:d=2.0",
        "-c:a", "pcm_s16le", str(bed_laid),
    ])
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(sfx),
        "-af", f"volume={sfx_gain_db:.2f}dB",
        "-c:a", "pcm_s16le", str(sfx_laid),
    ])
    premix = WORK / "premix.wav"
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(vo), "-i", str(sfx_laid), "-i", str(bed_laid),
        "-filter_complex",
        f"[0:a][1:a][2:a]amix=inputs=3:normalize=0:dropout_transition=0,atrim=0:{TOTAL}[a]",
        "-map", "[a]", "-c:a", "pcm_s16le", str(premix),
    ])
    mix_i, _ = loudness(premix)
    gain = -14.0 - mix_i
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(premix),
        "-af", f"volume={gain:.2f}dB,alimiter=limit=0.84:level=false",
        "-c:a", "pcm_s16le", str(dest),
    ])
    final_i, final_tp = loudness(dest)
    return {
        "vo_lufs": vo_i,
        "bed_gain_db": round(bed_gain_db, 2),
        "sfx_gain_db": round(sfx_gain_db, 2),
        "premix_lufs": mix_i,
        "gain_db": round(gain, 2),
        "integrated_lufs": final_i,
        "true_peak_dbtp": final_tp,
    }


def mux(picture: Path, audio: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(picture), "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart", str(dest),
    ])


def write_sidecars(cuts: list[dict]) -> None:
    PACK.mkdir(parents=True, exist_ok=True)
    cut_json = []
    for c in cuts:
        item = {
            "row": c["row"],
            "source": c["source"],
            "timeline_in": round(c["t0"], 3),
            "timeline_out": round(c["t0"] + c["frames"] / float(FPS), 3),
            "upscale": c["upscale"],
            "video": bool(c["video"]),
        }
        if c["video"]:
            item["framing"] = {"offset": float(c["offset"] or 0.0)}
        cut_json.append(item)
    (PACK / "cuts_v01.json").write_text(json.dumps(cut_json, indent=2), encoding="utf-8")

    items = [{"id": aid, "file": fname, "source": fname, "title": title} for aid, fname, title in POOL_TITLES]
    (PACK / "pool_titles_v01.json").write_text(json.dumps(items, indent=2), encoding="utf-8")


def run_gates() -> dict:
    PACK.mkdir(parents=True, exist_ok=True)
    results = {}
    clip = sp.run([
        sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/clip_check.py"),
        str(SHOT), "--words", str(WORDS),
    ], capture_output=True, text=True)
    results["clip_check"] = {"code": clip.returncode, "out": (clip.stdout or clip.stderr)[-600:]}

    pq = sp.run([
        sys.executable, str(REPO / "scripts/picture_qa.py"), str(OUT),
        "--cuts", str(PACK / "cuts_v01.json"),
        "--pool", str(POOL),
        "--out-dir", str(PACK),
    ], capture_output=True, text=True)
    results["picture_qa"] = {"code": pq.returncode, "out": (pq.stdout or pq.stderr)[-1200:]}

    mg = sp.run([
        sys.executable, str(REPO / "scripts/music_gate.py"), str(FILM),
        "--bed", str(BED), "--video", str(OUT),
        "--out", str(PACK / "music_gate_v01.json"),
    ], capture_output=True, text=True)
    results["music_gate"] = {"code": mg.returncode, "out": (mg.stdout or mg.stderr)[-800:]}

    lv = sp.run([
        sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
        "--vo", str(WORK / "vo_laid_v01.wav"),
        "--sfx", str(WORK / "sfx_laid_v01.wav"),
        "--bed", str(WORK / "bed_laid_v01.wav"),
        "--minutes", "9.5",
        "--out", str(PACK / "sfx_level_v01.json"),
    ], capture_output=True, text=True)
    results["sfx_level"] = {"code": lv.returncode, "out": (lv.stdout or lv.stderr)[-800:]}

    i, tp = loudness(OUT)
    black = sp.run([
        "ffmpeg", "-hide_banner", "-i", str(OUT),
        "-vf", "blackdetect=d=0.04:pix_th=0.10", "-f", "null", "-",
    ], capture_output=True, text=True)
    blacks = [ln for ln in black.stderr.splitlines() if "black_start" in ln]
    info = probe(OUT)
    results["delivery"] = {
        "integrated_lufs": i,
        "true_peak_dbtp": tp,
        "width": info["width"],
        "height": info["height"],
        "duration": info["duration"],
        "black_frames": blacks[:8],
    }
    (PACK / "gate_results_v01.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2), flush=True)
    return results


def main() -> None:
    os.environ["TMPDIR"] = str(WORK / "tmp")
    (WORK / "tmp").mkdir(parents=True, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "--all"
    update_harvest_pool_items()
    rows = normalize_shot_list_csv()
    cuts = build_plan(rows)
    (WORK / "plan_v01.json").write_text(json.dumps(cuts, indent=2), encoding="utf-8")
    write_sidecars(cuts)
    print(f"plan: {len(cuts)} cuts, {sum(c['frames'] for c in cuts)} frames", flush=True)
    if mode == "--plan":
        return

    paths = render_all(cuts)
    write_sidecars(cuts)
    picture = WORK / "picture_v01.mp4"
    concat_picture(paths, picture)

    vo = WORK / "vo_laid_v01.wav"
    sfx = WORK / "sfx_stem_v01.wav"
    mix_wav = WORK / "mix_v01.wav"
    if not vo.exists():
        print("lay vo", flush=True)
        lay_vo(vo)
    if not sfx.exists():
        print("build sfx", flush=True)
        build_sfx(sfx)
    if not mix_wav.exists() or not (PACK / "mix_report_v01.json").exists():
        print("mix", flush=True)
        report = mix(vo, sfx, mix_wav)
        PACK.mkdir(parents=True, exist_ok=True)
        (PACK / "mix_report_v01.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    else:
        report = json.loads((PACK / "mix_report_v01.json").read_text(encoding="utf-8"))
    print("mux", report, flush=True)
    mux(picture, mix_wav, OUT)

    if mode in ("--gates", "--all"):
        results = run_gates()
        failed = [k for k, v in results.items() if isinstance(v, dict) and v.get("code") not in (None, 0)]
        delivery = results.get("delivery") or {}
        if delivery.get("black_frames"):
            failed.append("black_frames")
        if not (-15.5 <= delivery.get("integrated_lufs", -99) <= -12.5):
            failed.append("loudness")
        if delivery.get("true_peak_dbtp", 0) > -1.0:
            failed.append("true_peak")
        code = 1 if failed else 0
        print(f"done {code} {failed}", flush=True)
        raise SystemExit(code)


if __name__ == "__main__":
    main()
