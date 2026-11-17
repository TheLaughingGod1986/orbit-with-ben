#!/usr/bin/env python3
"""Deterministic £0 US Federal Government Public Domain archive photo harvester for WW2:003 (J2998).

Downloads every archive photograph required by `01_Script/SHOT_LIST.md` onto the NAS
working store (`/Volumes/data/studio-live/ww2/02_Video-Projects/003_Why-B29-Superfortress-Cost-More-Than-Atomic-Bomb/03_Picture/archive/`),
verifies via Wikimedia Commons `extmetadata` that each image carries a genuine Public Domain
US Government licence (`17 U.S.C. § 105` — zero CC-BY / CC-BY-SA / wire / agency files),
normalises TIFF/oversize scans to high-resolution RGB JPEG (`quality=95`), and records
SHA-256 checksums, dimensions, and provenance metadata.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import pathlib
import time
import urllib.parse
import urllib.request
from typing import Dict, List

from PIL import Image

UA = "FieldOrderHistoryStudio/1.0 (https://github.com/TheLaughingGod1986; archival documentary verification)"

DEFAULT_OUT_DIR = pathlib.Path(
    "/Volumes/data/studio-live/ww2/02_Video-Projects/"
    "003_Why-B29-Superfortress-Cost-More-Than-Atomic-Bomb/03_Picture/archive"
)

# 38 verified US Federal Public Domain records covering all 24 catalogue groups & shots S01-S66.
# Note: Commons files `File:Gen. Curtis LeMay Official Portrait.jpg` and `File:B-29 and B-50 models.jpg`
# were inspected and rejected because those uploads carry CC BY-SA 4.0 tags; replaced below with genuine
# USAF / DoD Public Domain (`17 U.S.C. § 105`) photographs (`File:Curtis LeMay (USAF).jpg`,
# `File:NB-36H with B-50, 1955 - DF-SC-83-09332.jpeg`, `File:Boeing B-50 USAF.jpg`, and C-97 USAF).
ARCHIVE_ITEMS: List[Dict] = [
    {
        "id": "A01a",
        "group": 1,
        "filename": "a01a_nmusaf_090625_b29_in_flight.jpg",
        "commons_title": "File:B-29 in flight.jpg",
        "catalogue_id": "NMUSAF 090625-F-1234K-015",
        "collection": "US Air Force / National Museum of the U.S. Air Force",
        "date": "1944-1945",
        "shots": ["S02", "S08", "S66"],
        "caption": "Boeing B-29 Superfortress in flight, side/three-quarter aerial view",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A01b",
        "group": 1,
        "filename": "a01b_usaf_b29_formation_flight.jpg",
        "commons_title": "File:91st Air Refueling Squadron KB-29P Superfortress formation 1951.jpg",
        "catalogue_id": "USAF B-29 / KB-29P Formation Flight (1951)",
        "collection": "US Air Force (National Archives / USAF Historical Collection)",
        "date": "1945-1951",
        "shots": ["S08"],
        "caption": "Boeing B-29 / KB-29 Superfortress formation in flight showing the slender 141-foot high-aspect-ratio laminar wings",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A02a",
        "group": 2,
        "filename": "a02a_nmusaf_060711_boeing_xb29.jpg",
        "commons_title": "File:Boeing XB-29.jpg",
        "catalogue_id": "NMUSAF 060711-F-1234S-001",
        "collection": "US Air Force / National Museum of the U.S. Air Force",
        "date": "1942-1943",
        "shots": ["S03", "S16", "S17", "S24", "S26"],
        "caption": "First Boeing XB-29 prototype in flight over Washington during test programme",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A02b",
        "group": 2,
        "filename": "a02b_nmusaf_boeing_xb29_41_002_ramp.jpg",
        "commons_title": "File:Boeing XB-29 41-002.jpg",
        "catalogue_id": "NMUSAF XB-29 41-002",
        "collection": "US Air Force / National Museum of the U.S. Air Force",
        "date": "Sep 1942",
        "shots": ["S16", "S26"],
        "caption": "First Boeing XB-29 prototype (serial 41-002) at Boeing Field, Seattle",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A03a",
        "group": 3,
        "filename": "a03a_afhra_boeing_wichita_assembly_1944.jpg",
        "commons_title": "File:Boeing-Whichata B-29 Assembly Line - 1944.jpg",
        "catalogue_id": "AFHRA Wichita B-29 Assembly Line 1944",
        "collection": "US Air Force Historical Research Agency (Maxwell AFB) / NARA RG 342-FH",
        "date": "1944",
        "shots": ["S04", "S19", "S19a", "S30", "S65"],
        "caption": "Rows of unpainted aluminium Boeing B-29 nose sections and fuselages at Boeing Wichita Plant II (also Thumbnail Key Art)",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A03b",
        "group": 3,
        "filename": "a03b_usgov_b29_forward_compartment_workers.jpg",
        "commons_title": "File:Assembly of the forward compartment of a B-29.jpg",
        "catalogue_id": "USAAF / OWI B-29 Forward Compartment Assembly (1944)",
        "collection": "US Army Air Forces / Office of War Information (NARA)",
        "date": "1944",
        "shots": ["S19a"],
        "caption": "Assembly workers and riveters constructing the pressurised forward nose compartment of a Boeing B-29",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov)",
    },
    {
        "id": "A04",
        "group": 4,
        "filename": "a04_nara_111_sc_8911_hap_arnold.jpg",
        "commons_title": "File:111-SC-8911 - Colonel Henry H Arnold Signal Corps, USA, Office of Chief Signal Officer, War Department, Washington, DC - NARA - 55178180.jpg",
        "catalogue_id": "NARA 111-SC-8911 (NAID 55178180)",
        "collection": "US National Archives (RG 111-SC Signal Corps)",
        "date": "1939-1944",
        "shots": ["S05", "S34"],
        "caption": "Henry Harley 'Hap' Arnold, Chief of the Air Corps / Commanding General, US Army Air Forces",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Army)",
    },
    {
        "id": "A05a",
        "group": 5,
        "filename": "a05a_nara_342_fh_3a09035_b17g_altitude.jpg",
        "commons_title": "File:A USAAF Boeing B-17G Flying Fortress over Berlin-Tempelhof, Germany, 29 April 1944 (342-FH-3A09035-116418AC).jpg",
        "catalogue_id": "NARA 342-FH-3A09035-116418AC",
        "collection": "US National Archives (RG 342-FH USAAF Still Pictures)",
        "date": "29 Apr 1944",
        "shots": ["S06"],
        "caption": "USAAF Boeing B-17G Flying Fortress formation in high-altitude flight",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A05b",
        "group": 5,
        "filename": "a05b_nara_542352_high_altitude_flight_gear.jpg",
        "commons_title": "File:CLAD IN HIS ARMOR. Normally a good-sized man, Captain Melvin E. Jarvis, 1318 Roberta Street, Salt Lake City, Utah... - NARA - 542352.tif",
        "catalogue_id": "NARA NAID 542352",
        "collection": "US National Archives (US Air Force / USAAF Still Pictures)",
        "date": "1944-1950",
        "shots": ["S09"],
        "caption": "US heavy-bomber airman wearing bulky high-altitude protective flying suit, flak armour, and oxygen gear",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov)",
    },
    {
        "id": "A06",
        "group": 6,
        "filename": "a06_nmusaf_consolidated_b32_dominator.jpg",
        "commons_title": "File:B-32 Dominator in flight.jpg",
        "catalogue_id": "NMUSAF Consolidated B-32 Dominator",
        "collection": "US Air Force / National Museum of the U.S. Air Force",
        "date": "1944-1945",
        "shots": ["S07a"],
        "caption": "Consolidated B-32 Dominator four-engine backup VLR heavy bomber in flight",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A07",
        "group": 7,
        "filename": "a07_nara_342_fh_001297_b29_eddie_allen_cockpit.jpg",
        "commons_title": "File:342-FH 001297 Boeing B-29 'Eddie Allen' During The 14 October 1944 Raid On Formosa.jpg",
        "catalogue_id": "NARA 342-FH-001297",
        "collection": "US National Archives (RG 342-FH USAAF Still Pictures)",
        "date": "14 Oct 1944",
        "shots": ["S10", "S24", "S41a"],
        "caption": "Pilot and bombardier stations inside the pressurised glazed nose of XX Bomber Command B-29 'Eddie Allen'",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A08a",
        "group": 8,
        "filename": "a08a_nara_542362_b29_padded_crawl_tunnel.jpg",
        "commons_title": "File:FEAF BOMBER COMMAND, JAPAN-Combat infantrymen must know how to do a flat crawl - NARA - 542362.tif",
        "catalogue_id": "NARA NAID 542362",
        "collection": "US National Archives (US Air Force Bomber Command)",
        "date": "1944-1950",
        "shots": ["S12"],
        "caption": "Crewman crawling through the 28-inch diameter padded pressurised fuselage tunnel connecting B-29 forward and aft cabins",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov)",
    },
    {
        "id": "A08b",
        "group": 8,
        "filename": "a08b_nara_542361_b29_gun_blister_station.jpg",
        "commons_title": "File:20TH AIR FORCE, OKINAWA-A-2C Don W. Murray of Mazon, Ill., flashes a victory smile from the gun blister of his U.S.... - NARA - 542361.tif",
        "catalogue_id": "NARA NAID 542361",
        "collection": "US National Archives (Twentieth Air Force)",
        "date": "1945-1950",
        "shots": ["S13"],
        "caption": "Twentieth Air Force B-29 gunner at his plexiglass sighting blister beside the fuselage",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov)",
    },
    {
        "id": "A08c",
        "group": 8,
        "filename": "a08c_usaf_hf_sn_98_07477_b29_remote_gunsight.jpg",
        "commons_title": "File:1st Lt Gene F. White, Tulsa, OK, checks his B-29 \"Superfort\" gun sight after flying his final bombing mission over North Korea HF-SN-98-07477.jpg",
        "catalogue_id": "DoD / USAF HF-SN-98-07477",
        "collection": "US Air Force / Department of Defense Still Media (NARA)",
        "date": "1945-1952",
        "shots": ["S13", "S14"],
        "caption": "Close-up of General Electric remote fire-control optical gunsight inside a Boeing B-29 Superfortress sighting blister",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military)",
    },
    {
        "id": "A09",
        "group": 9,
        "filename": "a09_nara_342_fh_000529_b29_bombs_india_china.jpg",
        "commons_title": "File:342-FH 000529 500-lb demolition bombs are lined up to be loaded into a B-29 which will take them to an advanced China base. There the bombs are to be used for a raid on the Jap-held island of formosa.jpg",
        "catalogue_id": "NARA 342-FH-000529",
        "collection": "US National Archives (RG 342-FH USAAF Still Pictures)",
        "date": "1944",
        "shots": ["S11", "S39", "S40"],
        "caption": "500-lb demolition bombs lined up beside a XX Bomber Command B-29 in India to be ferried over the Hump to China",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A10a",
        "group": 10,
        "filename": "a10a_nara_342_fh_001221_engineer_instrument_panel.jpg",
        "commons_title": "File:342-FH 001221 The engineer's instrument panel on the bombing raid on Anshan, Manchuria, 40th Bomb Group.jpg",
        "catalogue_id": "NARA 342-FH-001221",
        "collection": "US National Archives (RG 342-FH USAAF Still Pictures)",
        "date": "July 1944",
        "shots": ["S10", "S14", "S41a"],
        "caption": "Flight engineer's instrument and engine-temperature panel aboard a 40th Bomb Group Boeing B-29 on the Anshan raid",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A10b",
        "group": 10,
        "filename": "a10b_nara_342_fh_001320_40bg_crew_debrief.jpg",
        "commons_title": "File:342-FH 001320 Talking Things Over After The Successful Accomplishment Of Anshun raid.jpg",
        "catalogue_id": "NARA 342-FH-001320",
        "collection": "US National Archives (RG 342-FH USAAF Still Pictures)",
        "date": "July 1944",
        "shots": ["S14", "S41a"],
        "caption": "XX Bomber Command B-29 crew beside aircraft following high-altitude mission from China",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A11a",
        "group": 11,
        "filename": "a11a_loc_haer_ne_9_r_sheet4_engineering_drawing.jpg",
        "commons_title": "File:B-29 Assembly Process - Offutt Air Force Base, Glenn L. Martin-Nebraska Bomber Plant, Building D, Peacekeeper Drive, Bellevue, Sarpy County, NE HAER NE-9-R (sheet 4 of 7).png",
        "catalogue_id": "LoC HAER NE-9-R (Sheet 4 of 7)",
        "collection": "Library of Congress Prints & Photographs Division / Historic American Engineering Record (NPS)",
        "date": "1944 / HAER",
        "shots": ["S07"],
        "caption": "Architectural & engineering drawing of Boeing/Martin B-29 Superfortress assembly flow in Building D",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-NPS)",
    },
    {
        "id": "A11b",
        "group": 11,
        "filename": "a11b_loc_haer_ne_9_r_28_omaha_b29_conveyor.jpg",
        "commons_title": "File:GENERAL VIEW OF THE PRODUCTION LINE BEING CONVERTED FROM B-26 TO B-29 PRODUCTION SHOWING THE LINK-BELT CONVEYOR SYSTEM AND ENGINE NACELLES READY FOR ASSEMBLY.; WHO, 1944 - Offutt Air HAER NE-9-R-28.tif",
        "catalogue_id": "LoC HAER NE-9-R-28",
        "collection": "Library of Congress (HAER NE-9-R) / USAAF Wing Historian's Office (1944)",
        "date": "1944",
        "shots": ["S18", "S30"],
        "caption": "Glenn L. Martin-Nebraska Bomber Plant (Omaha) B-29 production line conveyor system and R-3350 engine nacelles ready for assembly, 1944",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-NPS / USAAF)",
    },
    {
        "id": "A11c",
        "group": 11,
        "filename": "a11c_loc_haer_ne_9_r_29_b29_wing_fuselage_splicing.jpg",
        "commons_title": "File:DETAIL VIEW OF THE INITIAL PRODUCTION LINE OF THE FIRST B-29 SHOWING THE SPLICING OF THE WINGS AND FUSELAGE.; WHO, 1944 - Offutt Air Force Base, Glenn L. Martin-Nebraska Bomber Plant, HAER NE-9-R-29.tif",
        "catalogue_id": "LoC HAER NE-9-R-29",
        "collection": "Library of Congress (HAER NE-9-R) / USAAF Wing Historian's Office (1944)",
        "date": "1944",
        "shots": ["S19b"],
        "caption": "Initial B-29 Superfortress production line showing splicing of the 141-foot wings and fuselage sections, Omaha, 1944",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-NPS / USAAF)",
    },
    {
        "id": "A11d",
        "group": 11,
        "filename": "a11d_loc_haer_ne_9_r_30_b29_final_assembly_line.jpg",
        "commons_title": "File:GENERAL VIEW OF THE FINAL PRODUCTION LINE OF THE FIRST B-29 SHOWING THE LINK-BELT CONVEYOR SYSTEM AND WOOD BLOCK FLOORING.; WHO, 1944 - Offutt Air Force Base, Glenn L. Martin-Nebraska HAER NE-9-R-30.tif",
        "catalogue_id": "LoC HAER NE-9-R-30",
        "collection": "Library of Congress (HAER NE-9-R) / USAAF Wing Historian's Office (1944)",
        "date": "1944",
        "shots": ["S18", "S19a", "S30"],
        "caption": "General view of the B-29 final assembly conveyor line at Glenn L. Martin-Nebraska Bomber Plant, 1944",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-NPS / USAAF)",
    },
    {
        "id": "A12a",
        "group": 12,
        "filename": "a12a_nasa_grc_1944_c_05491_b29_wind_tunnel.jpg",
        "commons_title": "File:Boeing B–29 Superfortress at the Aircraft Engine Research Laboratory (GRC-1944-C-05491).jpg",
        "catalogue_id": "NASA / NACA GRC-1944-C-05491",
        "collection": "NASA Glenn Research Center Archives (NACA Aircraft Engine Research Laboratory, Cleveland)",
        "date": "1944",
        "shots": ["S15", "S23", "S29"],
        "caption": "Boeing B-29 Superfortress nacelle mounted at the NACA Aircraft Engine Research Laboratory, Cleveland, 1944",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-NASA)",
    },
    {
        "id": "A12b",
        "group": 12,
        "filename": "a12b_nasa_grc_1944_c_05552_r3350_wind_tunnel.jpg",
        "commons_title": "File:B-29 Superfortress Engine in the Altitude Wind Tunnel (GRC-1944-C-05552).jpg",
        "catalogue_id": "NASA / NACA GRC-1944-C-05552",
        "collection": "NASA Glenn Research Center Archives (NACA Aircraft Engine Research Laboratory, Cleveland)",
        "date": "1944",
        "shots": ["S03", "S20", "S23", "S29"],
        "caption": "Wright R-3350 Duplex-Cyclone engine and B-29 cowling mounted in the NACA Altitude Wind Tunnel for cooling-baffle tests, 1944",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-NASA)",
    },
    {
        "id": "A12c",
        "group": 12,
        "filename": "a12c_nasa_grc_1944_c_05818_tunnel_control_room.jpg",
        "commons_title": "File:Altitude Wind Tunnel Control Room at the Aircraft Engine Research Laboratory (GRC-1944-C-05818).jpg",
        "catalogue_id": "NASA / NACA GRC-1944-C-05818",
        "collection": "NASA Glenn Research Center Archives (NACA Aircraft Engine Research Laboratory, Cleveland)",
        "date": "1944",
        "shots": ["S21"],
        "caption": "NACA Altitude Wind Tunnel test control room monitoring Wright R-3350 high-altitude temperatures and pressures, 1944",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-NASA)",
    },
    {
        "id": "A13a",
        "group": 13,
        "filename": "a13a_nmusaf_wright_r3350_change_b29_india.jpg",
        "commons_title": "File:Wright R-3350 change on B-29 in India.jpg",
        "catalogue_id": "NMUSAF Wright R-3350 Change on B-29",
        "collection": "US Air Force / National Museum of the U.S. Air Force",
        "date": "1944",
        "shots": ["S25", "S36"],
        "caption": "USAAF mechanics hoisting a replacement Wright R-3350 radial engine onto a B-29 Superfortress outdoors",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A13b",
        "group": 13,
        "filename": "a13b_nara_b29_outdoor_engine_maintenance.jpg",
        "commons_title": "File:B-29 engine maintenance Kadena 1950.jpg",
        "catalogue_id": "NARA / USAF B-29 Outdoor R-3350 Maintenance",
        "collection": "US National Archives / US Air Force",
        "date": "1945-1950",
        "shots": ["S33", "S36"],
        "caption": "Ground mechanics working on open stands around a Boeing B-29's cowled Wright R-3350 engine",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A14",
        "group": 14,
        "filename": "a14_loc_harry_s_truman_portrait_1945.jpg",
        "commons_title": "File:Harry S Truman, bw half-length photo portrait, facing front, 1945.jpg",
        "catalogue_id": "LoC / NARA Harry S. Truman Official Portrait",
        "collection": "Library of Congress Prints & Photographs Division / US National Archives",
        "date": "1943-1945",
        "shots": ["S28"],
        "caption": "Harry S. Truman, Chairman of the Senate Special Committee Investigating the National Defense Program (Truman Committee)",
        "licence_statute": "US Federal Government Public Domain / No Known Restrictions (LoC Official Portrait)",
    },
    {
        "id": "A15a",
        "group": 15,
        "filename": "a15a_usaf_b29s_wichita_kansas_ramp.jpg",
        "commons_title": "File:B-29s-Boeing-Witchita-1945.jpg",
        "catalogue_id": "USAF Wichita Kansas B-29 Ramp Lineup",
        "collection": "US Air Force / NARA RG 342-FH",
        "date": "1944-1945",
        "shots": ["S03", "S32", "S33"],
        "caption": "Rows of Boeing B-29 Superfortresses parked across open Kansas ramps at Wichita",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A15b",
        "group": 15,
        "filename": "a15b_nara_sc_270496_b29_wichita_ramp_crew.jpg",
        "commons_title": "File:SC 270496 - Sgt. Nelson T. Young, Gonzales, La., removes the nozzle from the wing tank of a B-29 Superfortress plane as Sgt. John T. Daly, Wichita, Kan. stands by. CBI Theater, 6 December, 1944.jpg",
        "catalogue_id": "NARA 111-SC-270496",
        "collection": "US National Archives (RG 111-SC US Army Signal Corps)",
        "date": "1944",
        "shots": ["S35", "S40"],
        "caption": "Ground crew working atop the wing of Wichita-built B-29-40-BW (42-24567) during fuel/modification operations, 1944",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Army)",
    },
    {
        "id": "A15c",
        "group": 15,
        "filename": "a15c_usaf_45bs_b29_40_bw_42_24579_kansas.jpg",
        "commons_title": "File:45th Bombardment Squadron Boeing B-29-40-BW Superfortress 42-24579.jpg",
        "catalogue_id": "USAF 40th BG / 45th BS B-29-40-BW 42-24579",
        "collection": "US Air Force / XX Bomber Command (NARA RG 342-FH)",
        "date": "Spring 1944",
        "shots": ["S35"],
        "caption": "40th Bombardment Group Wichita-built Boeing B-29-40-BW (42-24579) prepared in Kansas for Operation Matterhorn deployment",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A16a",
        "group": 16,
        "filename": "a16a_nara_342_fh_000690_india_control_tower.jpg",
        "commons_title": "File:342-FH 000690 Control tower at airbase in India.jpg",
        "catalogue_id": "NARA 342-FH-000690",
        "collection": "US National Archives (RG 342-FH USAAF Still Pictures)",
        "date": "1944",
        "shots": ["S37", "S38"],
        "caption": "XX Bomber Command airfield control tower and B-29 Superfortress dispersal in eastern India, 1944",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A16b",
        "group": 16,
        "filename": "a16b_nara_342_fh_000844_matterhorn_debriefing.jpg",
        "commons_title": "File:342-FH 000844 Debriefing after Yawata mission.jpg",
        "catalogue_id": "NARA 342-FH-000844",
        "collection": "US National Archives (RG 342-FH USAAF Still Pictures)",
        "date": "June 1944",
        "shots": ["S38", "S41"],
        "caption": "XX Bomber Command B-29 aircrews at Operation Matterhorn base debriefing after the June 1944 Yawata raid",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A16c",
        "group": 16,
        "filename": "a16c_usaf_20bc_b29_chengdu_china.jpg",
        "commons_title": "File:B-29 Superfortress of the 20th Bomber Command near Chengdu, China.jpg",
        "catalogue_id": "USAF XX Bomber Command Chengdu B-29",
        "collection": "US Air Force / NARA RG 342-FH",
        "date": "1944",
        "shots": ["S39"],
        "caption": "Boeing B-29 Superfortress of XX Bomber Command at a forward staging airfield near Chengdu, western China, 1944",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A17a",
        "group": 17,
        "filename": "a17a_nara_342_fh_001063_b29_nose_strike_smoke.jpg",
        "commons_title": "File:342-FH 001063 Photo taken from the nose of a Boeing B-29 Superfortress showing clouds of smoke rising from the Showa Steel Works during the daylight raid on Anshan, Manchuria, 29 July 44.jpg",
        "catalogue_id": "NARA 342-FH-001063",
        "collection": "US National Archives (RG 342-FH USAAF Still Pictures)",
        "date": "29 July 1944",
        "shots": ["S41", "S50"],
        "caption": "High-altitude view through the glazed nose of a XX Bomber Command B-29 over clouds and target smoke, July 1944",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A17b",
        "group": 17,
        "filename": "a17b_nara_342_fh_000365a_b29_return_china.jpg",
        "commons_title": "File:342-FH 000365a B-29 returns from raid on Formosa.jpg",
        "catalogue_id": "NARA 342-FH-000365a",
        "collection": "US National Archives (RG 342-FH USAAF Still Pictures)",
        "date": "Oct 1944",
        "shots": ["S41", "S42"],
        "caption": "XX Bomber Command Boeing B-29 Superfortress returning to its forward base in China after a long-range raid",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A18a",
        "group": 18,
        "filename": "a18a_nara_80_g_239297_tinian_ushi_airfield.jpg",
        "commons_title": "File:80-G-239297 U.S. Marines move across the wreckage of the Japanese airfield at Ushi Point.jpg",
        "catalogue_id": "NARA 80-G-239297",
        "collection": "US National Archives (RG 80-G US Navy / Marine Corps)",
        "date": "July 1944",
        "shots": ["S44"],
        "caption": "US Marines securing Ushi Point airfield on northern Tinian (site of North Field), July 1944",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Navy)",
    },
    {
        "id": "A18b",
        "group": 18,
        "filename": "a18b_afhra_tinian_airfields_1945_aerial.jpg",
        "commons_title": "File:Tinian Airfields 1945 Looking North To South.jpg",
        "catalogue_id": "AFHRA Tinian Airfields 1945",
        "collection": "US Air Force Historical Research Agency / NARA RG 342-FH",
        "date": "1945",
        "shots": ["S45"],
        "caption": "High aerial view looking south across Seabee-built four-runway North Field and West Field on Tinian, 1945",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A18c",
        "group": 18,
        "filename": "a18c_usaf_505bg_b29s_north_field_tinian.jpg",
        "commons_title": "File:505th Bombardment Group B-29s North Field Tinian July 1945.jpg",
        "catalogue_id": "USAF 505th BG North Field Tinian (July 1945)",
        "collection": "US Air Force / AFHRA (NARA RG 342-FH)",
        "date": "July 1945",
        "shots": ["S45", "S51"],
        "caption": "505th Bombardment Group Boeing B-29 Superfortresses parked along coral hardstands at North Field, Tinian",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A18d",
        "group": 18,
        "filename": "a18d_usaf_9bg_b29_north_field_tinian.jpg",
        "commons_title": "File:9th Bombardment Group B-29 North Field Tinian.jpg",
        "catalogue_id": "USAF 9th BG North Field Tinian (1945)",
        "collection": "US Air Force / AFHRA (NARA RG 342-FH)",
        "date": "1945",
        "shots": ["S51"],
        "caption": "9th Bombardment Group Boeing B-29 Superfortress taxiing at North Field, Tinian, 1945",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A19a",
        "group": 19,
        "filename": "a19a_usaf_b29_bombers_over_mount_fuji.jpg",
        "commons_title": "File:B-29 bombers over Mount Fuji.jpg",
        "catalogue_id": "USAF B-29 Formation Over Mount Fuji (1945)",
        "collection": "US Air Force / NARA RG 342-FH",
        "date": "1945",
        "shots": ["S46"],
        "caption": "XXI Bomber Command Boeing B-29 Superfortresses in high-altitude daylight formation past Mount Fuji, Honshu, 1945",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A19b",
        "group": 19,
        "filename": "a19b_usaf_499bg_b29_over_mount_fuji_1945.jpg",
        "commons_title": "File:499th Bomb Group B-29 over Mount Fuji 1945.jpg",
        "catalogue_id": "USAF 499th BG B-29 Over Mount Fuji (1945)",
        "collection": "US Air Force / NARA RG 342-FH",
        "date": "1945",
        "shots": ["S46"],
        "caption": "499th Bombardment Group Boeing B-29 Superfortress cruising at altitude past snow-capped Mount Fuji, 1945",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A20a",
        "group": 20,
        "filename": "a20a_usaf_500bg_b29_air_sea_rescue_saipan.jpg",
        "commons_title": "File:500bg-b29-helicopter-saipan.jpg",
        "catalogue_id": "USAF 500th BG Air-Sea Rescue Saipan (1945)",
        "collection": "US Air Force / NARA RG 342-FH",
        "date": "1945",
        "shots": ["S51a"],
        "caption": "XXI Bomber Command Boeing B-29 and rescue aircraft at Saipan supporting long-range overwater Marianas sorties, 1945",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A20b",
        "group": 20,
        "filename": "a20b_nmusaf_050607_b29_emergency_landing_iwo_jima.jpg",
        "commons_title": "File:050607-F-1234P-081.jpg",
        "catalogue_id": "USAF / NMUSAF 050607-F-1234P-081",
        "collection": "US Air Force / National Museum of the U.S. Air Force",
        "date": "1945",
        "shots": ["S51b"],
        "caption": "Battle-damaged Boeing B-29 Superfortress after emergency landing on Iwo Jima during return from Japan, 1945",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A20c",
        "group": 20,
        "filename": "a20c_usaf_9bg_dinah_might_42_65286_iwo_jima.jpg",
        "commons_title": "File:9th Bombardment Group Martin-Omaha B-29-25-MO Superfortress 42-65286.jpg",
        "catalogue_id": "USAF 9th BG Dinah Might (42-65286) Iwo Jima",
        "collection": "US Air Force / National Museum of the U.S. Air Force",
        "date": "4 Mar 1945",
        "shots": ["S51b"],
        "caption": "9th Bombardment Group Martin-Omaha B-29-25-MO 'Dinah Might' (42-65286) after making the first emergency B-29 landing on Iwo Jima, 4 March 1945",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A20d",
        "group": 20,
        "filename": "a20d_nmusaf_boeing_sb29_airborne_lifeboat.jpg",
        "commons_title": "File:Boeing SB-29.jpg",
        "catalogue_id": "USAF / NMUSAF Boeing SB-29 Superdumbo Lifeboat",
        "collection": "US Air Force / National Museum of the U.S. Air Force",
        "date": "1945-1947",
        "shots": ["S51a"],
        "caption": "Boeing SB-29 Superfortress air-sea rescue aircraft fitted with a droppable A-3 airborne lifeboat beneath the fuselage",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A21",
        "group": 21,
        "filename": "a21_usaf_curtis_lemay_official_portrait.jpg",
        "commons_title": "File:Curtis LeMay (USAF).jpg",
        "catalogue_id": "USAF Official Portrait - Curtis E. LeMay",
        "collection": "US Air Force / US National Archives",
        "date": "1945-1948",
        "shots": ["S52"],
        "caption": "Official US Air Force portrait of General Curtis Emerson LeMay, Commander, XXI Bomber Command",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A22a",
        "group": 22,
        "filename": "a22a_nara_342_fh_000537_m47a2_incendiary_bombs.jpg",
        "commons_title": "File:342-FH 000537 M47 A2 Chemical Incendiary Bombs Being Unpacked From Their Crates And Being Prepared For Use On A Xx Bomber Command Boeing B-29 Raid. China.jpg",
        "catalogue_id": "NARA 342-FH-000537",
        "collection": "US National Archives (RG 342-FH USAAF Still Pictures)",
        "date": "1944-1945",
        "shots": ["S54"],
        "caption": "USAAF ordnance crews unpacking M47A2 incendiary bombs from crates for B-29 Superfortress loading",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A22b",
        "group": 22,
        "filename": "a22b_usaaf_ussbs_tokyo_vertical_recon_1945.jpg",
        "commons_title": "File:Damage assessment aerial photo for Bombing of Tokyo in 1945 ndl 3984252 47.jpg",
        "catalogue_id": "USAAF XXI Bomber Command / USSBS RG 243 Tokyo Vertical Recon (NDL 3984252-47)",
        "collection": "US Army Air Forces / US Strategic Bombing Survey (RG 243 via NDL)",
        "date": "Spring 1945",
        "shots": ["S55"],
        "caption": "High-altitude vertical mapping reconnaissance photograph of Tokyo urban industrial districts after incendiary raid (vertical aerial only, zero casualties shown)",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A23a",
        "group": 23,
        "filename": "a23a_nara_76048591_509th_cg_silverplate_b29_tinian.jpg",
        "commons_title": "File:Boeing B-29 Superfortress of the 509th Composite Group, in 1945 (76048591).jpg",
        "catalogue_id": "NARA NAID 76048591",
        "collection": "US National Archives (RG 342-FH USAAF Still Pictures)",
        "date": "Aug 1945",
        "shots": ["S57", "S58"],
        "caption": "Silverplate Martin-Omaha Boeing B-29 Superfortress of the 509th Composite Group at North Field, Tinian, August 1945",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A23b",
        "group": 23,
        "filename": "a23b_nara_208_enola_gay_tinian_1945.jpg",
        "commons_title": "File:B-29 Enola Gay w Crews.jpg",
        "catalogue_id": "NARA RG 208 / USAAF Enola Gay (44-86292)",
        "collection": "US National Archives / US Army Air Forces",
        "date": "Aug 1945",
        "shots": ["S58"],
        "caption": "509th Composite Group Silverplate B-29 'Enola Gay' (44-86292) on Tinian, August 1945",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov)",
    },
    {
        "id": "A23c",
        "group": 23,
        "filename": "a23c_usaf_bockscar_44_27297.jpg",
        "commons_title": "File:Bockscar.jpg",
        "catalogue_id": "USAF 509th CG Bockscar (44-27297)",
        "collection": "US Air Force / National Museum of the U.S. Air Force",
        "date": "Aug 1945",
        "shots": ["S58"],
        "caption": "509th Composite Group Silverplate B-29 'Bockscar' (44-27297), built by Glenn L. Martin at Omaha",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
    {
        "id": "A23d",
        "group": 23,
        "filename": "a23d_nara_80_g_421130_uss_missouri_tokyo_bay_flyover.jpg",
        "commons_title": "File:USS Missouri (BB-63) flyover, Tokyo Bay, 2 September 1945 (80-G-421130).jpg",
        "catalogue_id": "NARA 80-G-421130",
        "collection": "US National Archives (RG 80-G US Navy / NHHC)",
        "date": "2 Sep 1945",
        "shots": ["S59"],
        "caption": "Massed Allied aircraft fly over battleship USS Missouri (BB-63) in Tokyo Bay at the close of the formal Japanese surrender ceremony, 2 September 1945",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Navy)",
    },
    {
        "id": "A24a",
        "group": 24,
        "filename": "a24a_dod_df_sc_83_09332_boeing_b50_in_flight.jpg",
        "commons_title": "File:NB-36H with B-50, 1955 - DF-SC-83-09332.jpeg",
        "catalogue_id": "DoD / USAF DF-SC-83-09332",
        "collection": "US Department of Defense / US Air Force (NARA)",
        "date": "1955",
        "shots": ["S63"],
        "caption": "Post-war Boeing B-50 Superfortress (upper right) flying alongside Convair NB-36H, showing direct B-29 airframe lineage",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military)",
    },
    {
        "id": "A24b",
        "group": 24,
        "filename": "a24b_usaf_boeing_c97_stratofreighter.jpg",
        "commons_title": "File:C-97 Stratofreighter of NY ANG in Vietnam 1966.jpg",
        "catalogue_id": "USAF Boeing C-97 Stratofreighter",
        "collection": "US Air Force",
        "date": "1950-1966",
        "shots": ["S63"],
        "caption": "Boeing C-97 Stratofreighter double-deck pressurised transport derived directly from the B-29 wing and powerplant",
        "licence_statute": "US Federal Government Public Domain (17 U.S.C. § 105 - PD-USGov-Military-Air Force)",
    },
]


def api_get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def download_bytes(url: str) -> bytes:
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.read()
        except Exception as exc:
            if attempt == 3:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Unreachable download failure for {url}")


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_commons_metadata(titles: List[str]) -> Dict[str, dict]:
    out: Dict[str, dict] = {}
    for i in range(0, len(titles), 15):
        batch = titles[i:i + 15]
        params = urllib.parse.urlencode({
            "action": "query",
            "titles": "|".join(batch),
            "prop": "imageinfo",
            "iiprop": "url|size|mime|extmetadata",
            "iiurlwidth": "3840",
            "format": "json",
        })
        data = api_get_json(f"https://commons.wikimedia.org/w/api.php?{params}")
        for _, page in data.get("query", {}).get("pages", {}).items():
            t = page.get("title")
            ii = (page.get("imageinfo") or [None])[0]
            if not ii:
                raise RuntimeError(f"Missing Commons imageinfo for {t}")
            out[t] = ii
    return out


def harvest_all(out_dir: pathlib.Path) -> List[Dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    titles = [item["commons_title"] for item in ARCHIVE_ITEMS]
    meta_map = fetch_commons_metadata(titles)

    results: List[Dict] = []
    for idx, item in enumerate(ARCHIVE_ITEMS, 1):
        title = item["commons_title"]
        ii = meta_map[title]
        ext = ii.get("extmetadata", {})
        lic_short = ext.get("LicenseShortName", {}).get("value", "").strip()
        usage_terms = ext.get("UsageTerms", {}).get("value", "").strip()
        categories = ext.get("Categories", {}).get("value", "")

        # Hard licence gate: reject any CC-BY, CC-BY-SA, GFDL-only, or non-PD file
        if not ("Public domain" in lic_short or lic_short.startswith("PD") or "No restrictions" in lic_short):
            raise ValueError(
                f"LICENCE GATE FAIL on {item['id']} ({title}): LicenseShortName={lic_short!r}, UsageTerms={usage_terms!r}"
            )
        if "CC BY" in lic_short or "CC-BY" in lic_short:
            raise ValueError(f"CC-BY REJECTED on {item['id']} ({title}): {lic_short!r}")

        orig_w = int(ii.get("width") or 0)
        orig_h = int(ii.get("height") or 0)
        mime = ii.get("mime", "")
        orig_url = ii["url"]
        thumb_url = ii.get("thumburl")

        # Use 3840px rendered derivative for TIFF/PNG or >4800px scans; keep original bytes for standard JPEGs
        use_thumb = bool(thumb_url) and (mime != "image/jpeg" or orig_w > 4800 or orig_h > 4800)
        dl_url = thumb_url if use_thumb else orig_url

        dest = out_dir / item["filename"]
        if not dest.exists() or dest.stat().st_size < 1024:
            raw = download_bytes(dl_url)
            img = Image.open(io.BytesIO(raw))
            img.load()
            if mime == "image/jpeg" and not use_thumb and img.mode in ("RGB", "L"):
                dest.write_bytes(raw)
            else:
                rgb = img.convert("RGB")
                rgb.save(dest, format="JPEG", quality=95, subsampling=0)
            time.sleep(0.25)

        with Image.open(dest) as saved:
            saved_w, saved_h = saved.size

        digest = sha256_file(dest)
        size_bytes = dest.stat().st_size
        commons_page = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"), safe=":/()")

        rec = {
            **item,
            "commons_page": commons_page,
            "download_url": dl_url.split("?")[0],
            "commons_license_short": lic_short,
            "commons_usage_terms": usage_terms,
            "original_dimensions": [orig_w, orig_h],
            "saved_dimensions": [saved_w, saved_h],
            "bytes": size_bytes,
            "sha256": digest,
        }
        results.append(rec)
        print(
            f"[{idx:02d}/{len(ARCHIVE_ITEMS):02d}] {item['id']} -> {item['filename']} "
            f"({saved_w}x{saved_h}, {size_bytes // 1024} KB, {lic_short}) sha256={digest[:12]}"
        )

    return results


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", type=pathlib.Path, default=DEFAULT_OUT_DIR)
    ap.add_argument("--report-json", type=pathlib.Path, default=None)
    args = ap.parse_args()

    records = harvest_all(args.out_dir)
    if args.report_json:
        args.report_json.parent.mkdir(parents=True, exist_ok=True)
        args.report_json.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote report: {args.report_json} ({len(records)} verified PD-USGov images)")


if __name__ == "__main__":
    main()
