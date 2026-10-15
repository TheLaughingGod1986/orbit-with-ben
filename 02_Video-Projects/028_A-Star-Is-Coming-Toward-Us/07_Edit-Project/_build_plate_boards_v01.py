#!/usr/bin/env python3
"""028 plate boards v01. Boards, credits and prices only. No mint. No spend.

Rates match HOS 009 J0261 (15 Oct 2026): Flow Fast 10 / Quality 100 a take;
expected uses 005's takes-per-KEEP (Quality 2.59, Fast 1.96). Vertex is list
price, 1080p, £0.80 per dollar, 8 s clip. Orbit stays Omni-only and unpriced
(billed late). Code graphics and credited harvest plates are £0.

  python3 _build_plate_boards_v01.py
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
FLOW_CREDITS_LEFT = 23730
FLOW_READ_AT = "2026-10-15T12:58:32Z"
VERTEX_BALANCE_GBP = 71.02
VERTEX_READ_AT = "2026-10-15T07:30:31Z"
VERTEX_MARGIN_GBP = 1.00
FLOW_CREDITS = {"Quality": 100, "Fast": 10}
USD_PER_S = {"Quality": 0.20, "Fast": 0.10}
GBP_PER_USD = 0.80
TAKES = {"Quality": 2.59, "Fast": 1.96}
CLIP_S = 8

# id, title, credit, licence, page, file, status, picture note
# status: ok (HEAD 200 this run) | gap (page only) | reject (do not use)
ASSETS = [
    ("gaia_motion_1_6my", "Gaia's stellar motion for the next 1.6 million years (3 Dec 2020)",
     "ESA/Gaia/DPAC; CC BY-SA 3.0 IGO", "CC BY-SA 3.0 IGO",
     "https://www.esa.int/ESA_Multimedia/Videos/2020/12/Gaia_s_stellar_motion_for_the_next_1.6_million_years",
     "https://dlmultimedia.esa.int/download/public/videos/2020/12/004/2012_004_AR_EN.mp4",
     "ok", "Data animation of 40,000 stars. picture_qa may call it a diagram. Six shot-list stretches; the cap is five."),
    ("gaia_gliese_encounter", "Waiting for a stellar encounter (Gliese 710, 31 Aug 2017)",
     "ESA/Gaia/DPAC; CC BY-SA 3.0 IGO", "CC BY-SA 3.0 IGO",
     "https://www.esa.int/ESA_Multimedia/Videos/2017/08/Waiting_for_a_stellar_encounter",
     "https://dlmultimedia.esa.int/download/public/videos/2017/08/022/1708_022_AR_EN.mp4",
     "ok", "The Gliese 710 flyby. Not the annotated 'Tracking stellar motions' cut (that one draws a circle and a line)."),
    ("gaia_edr3_sky", "Colour of the sky, Gaia Early Data Release 3 (Dec 2020)",
     "ESA/Gaia/DPAC; CC BY-SA 3.0 IGO", "CC BY-SA 3.0 IGO",
     "https://www.esa.int/ESA_Multimedia/Images/2020/12/Interactive_map_of_the_sky_from_Gaia_s_Early_Data_Release_3",
     "https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2020/12/interactive_map_of_the_sky_from_gaia_s_early_data_release_3/25364650-1-eng-GB/Interactive_map_of_the_sky_from_Gaia_s_Early_Data_Release_3.png",
     "ok", "EDR3 colour sky, not a DR3 chemistry or radial-velocity map (those are labelled). Confirm pixel size at harvest. No DSS2."),
    ("eso_mw_lasilla", "La Silla Milky Way time-lapse",
     "ESO/S. Brunier (CC BY 4.0)", "CC BY 4.0",
     "https://www.eso.org/public/videos/brunier_la_silla/",
     "https://cdn.eso.org/videos/hd_1080p25_screen/brunier_la_silla.mp4",
     "ok", "Galactic plane over the 3.6 m dome. Not a dedicated Serpens crop."),
    ("eso_startrails", "Time-lapse over La Silla (star trails)",
     "R. Wesson/ESO (CC BY 4.0)", "CC BY 4.0",
     "https://www.eso.org/public/videos/lasilla_timelapse_rw1/",
     "https://cdn.eso.org/videos/hd_1080p25_screen/lasilla_timelapse_rw1.mp4",
     "ok", "Star trails. A different film from the Brunier Milky Way lapse."),
    ("eso_chajnantor", "Milky Way over Chajnantor",
     "ESO (CC BY 4.0)", "CC BY 4.0",
     "https://www.eso.org/public/videos/chajnantormilkyway/",
     "https://cdn.eso.org/videos/medium_podcast/chajnantormilkyway.m4v",
     "ok", "Southern Milky Way, Coalsack visible. File found is the medium podcast, not 1080p."),
    ("eso_night_tafreshi", "Milky Way time-lapse, La Silla (Tafreshi)",
     "ESO/B. Tafreshi (twanight.org) (CC BY 4.0 unless the page says otherwise)", "CC BY 4.0 default",
     "https://www.eso.org/public/videos/bt_lasilla_fd2/",
     None, "gap", "Page returned 200. No cdn file URL in the HTML, and the usual 1080p path 404'd. Do not invent a file."),
    ("sdo_aia335", "SDO AIA 335 full disk, 2 Jun 2010",
     "NASA/SDO (public domain)", "public domain",
     "https://images.nasa.gov/details/GSFC_20171208_Archive_e002035",
     "https://images-assets.nasa.gov/image/GSFC_20171208_Archive_e002035/GSFC_20171208_Archive_e002035~orig.jpg",
     "ok", "ULTRAVIOLET (AIA 335), not the visible-light Sun the shot list asked for. One use only until a visible-light second framing is pinned."),
    ("k_dwarf_goldilocks", "Comparison of G, K and M stars (Hubble 2020)",
     "NASA, ESA, and Z. Levy (STScI)", "public domain",
     "https://science.nasa.gov/asset/hubble/comparison-of-g-k-and-m-stars-for-habitability/",
     "https://esahubble.org/images/opo2006a/",
     "reject", "Labelled infographic (ESA/Hubble type: Chart). picture_qa FAIL. Do not crop the labels off."),
    ("proxima", "Hubble image of Proxima Centauri (potw1343a)",
     "ESA/Hubble & NASA (CC BY 4.0)", "CC BY 4.0",
     "https://esahubble.org/images/potw1343a/",
     "https://cdn.esahubble.org/archives/images/large/potw1343a.jpg",
     "ok", "Same plate 026 already uses. No DSS2 companion."),
    ("hipparcos_art", "Artist's impression of the Hipparcos spacecraft (4 Apr 2000)",
     "ESA", "ESA standard licence; confirm before the cut",
     "https://sci.esa.int/web/hipparcos/-/14060-an-artist-s-impression-of-the-hipparcos-spacecraft",
     None, "gap", "Page verified. The still is not linked as a file in the HTML."),
    ("gaia_craft", "The Gaia spacecraft (artist's impression)",
     "ESA/ATG medialab; background: ESO/S. Brunier (CC BY 4.0 via ESO)", "CC BY 4.0",
     "https://www.eso.org/public/images/eso1908d/",
     "https://cdn.eso.org/images/large/eso1908d.jpg",
     "ok", "Artist's impression (WARN). Background is Brunier's Milky Way still, not the Brunier video."),
    ("neptune", "Neptune full disk, Voyager 2 (PIA01492)",
     "NASA/JPL (public domain)", "public domain",
     "https://science.nasa.gov/photojournal/neptune-full-disk-view/",
     "https://images-assets.nasa.gov/image/PIA01492/PIA01492~orig.jpg",
     "ok", "Green and orange filters, not a true-colour still. Say so if a credit line names the filters."),
    ("oort_page", "Oort Cloud illustration",
     "NASA", "public domain if the NASA page's file is used",
     "https://science.nasa.gov/resource/oort-cloud/",
     None, "gap", "Page verified, file not pinned. Do not use the Feild/STScI diagram (WEB12119): it has an inset chart."),
    ("neowise_dc", "Comet NEOWISE over Washington, 12 Jul 2020",
     "NASA/Bill Ingalls (public domain)", "public domain",
     "https://www.nasa.gov/image-article/comet-neowise-over-washington-dc-2/",
     "https://images-assets.nasa.gov/image/NHQ202007120002/NHQ202007120002~orig.tif",
     "ok", "C/2020 F3. Second use is a new crop only."),
    ("iss_sunrise", "Orbital sunrise above Namibia",
     "NASA (public domain)", "public domain",
     "https://images.nasa.gov/details/iss072e487315",
     "https://images-assets.nasa.gov/image/iss072e487315/iss072e487315~orig.jpg",
     "ok", "Cloud tops at sunrise from the ISS. A still, not a moving sunrise."),
    ("hale_bopp", "Comet Hale-Bopp, 14 Mar 1997 (phot-mar14-hbs-2)",
     "ESO/E. Slawik", "HOLD",
     "https://www.eso.org/public/images/phot-mar14-hbs-2/",
     "https://cdn.eso.org/images/large/phot-mar14-hbs-2.jpg",
     "hold", "HOLD for Chief. The 1997 event page says © Eckhard Slawik. This 2009 ESO page sits under ESO's CC BY 4.0 default. Do not use until the licence is confirmed."),
    ("comet_a3", "Comet C/2023 A3 from the ISS, 28 Sep 2024",
     "NASA/Matthew Dominick (public domain)", "public domain",
     "https://www.nasa.gov/image-article/ancient-comet-makes-appearance/",
     "https://images-assets.nasa.gov/image/iss072e020907/iss072e020907~orig.jpg",
     "ok", "Oort-cloud comet, as the shot list asked."),
    ("jupiter_juno", "Jupiter's colourful cloud belts (PIA21974)",
     "NASA/JPL-Caltech/SwRI/MSSS (public domain)", "public domain",
     "https://images.nasa.gov/details/PIA21974",
     "https://images-assets.nasa.gov/image/PIA21974/PIA21974~orig.tif",
     "ok", "Juno, colour-enhanced, not true colour. Credit the enhancement."),
    ("saturn", "The greatest Saturn portrait (PIA06193)",
     "NASA/JPL/Space Science Institute (public domain)", "public domain",
     "https://images.nasa.gov/details/PIA06193",
     "https://images-assets.nasa.gov/image/PIA06193/PIA06193~orig.jpg",
     "ok", "Cassini natural-colour portrait. Chosen over PIA14922, which puts Titan in front."),
    ("conjunction", "Jupiter and Saturn after sunset, 21 Dec 2020",
     "NASA/Bill Ingalls (public domain)", "public domain",
     "https://images.nasa.gov/details/NHQ202012210001",
     "https://images-assets.nasa.gov/image/NHQ202012210001/NHQ202012210001~orig.tif",
     "ok", "The Ingalls conjunction series. Saturn is in the frame with Jupiter."),
    ("moon_lro", "Full Moon (LRO)",
     "NASA (public domain)", "public domain",
     "https://images.nasa.gov/details/GSFC_20171208_Archive_e000868",
     "https://images-assets.nasa.gov/image/GSFC_20171208_Archive_e000868/GSFC_20171208_Archive_e000868~orig.jpg",
     "ok", "Second use is a crop. That is the twice-still cap."),
    ("wise_sky", "Entire WISE sky (PIA15481)",
     "NASA/JPL-Caltech/UCLA (public domain)", "public domain",
     "https://photojournal.jpl.nasa.gov/catalog/PIA15481",
     "https://images-assets.nasa.gov/image/PIA15481/PIA15481~orig.jpg",
     "ok", "All-sky mosaic. Inspect for axis labels before the cut. A labelled map FAILs picture_qa."),
    ("wise_craft", "NEOWISE spacecraft, artist concept (PIA17254)",
     "NASA/JPL-Caltech (public domain)", "public domain",
     "https://images.nasa.gov/details/PIA17254",
     "https://images-assets.nasa.gov/image/PIA17254/PIA17254~orig.jpg",
     "ok", "Artist's concept (WARN). It is the WISE spacecraft, which flew the NEOWISE mission."),
    ("ngc3603", "Starburst cluster (Hubble, GSFC archive e002049)",
     "NASA, ESA, Hubble (public domain)", "public domain",
     "https://images.nasa.gov/details/GSFC_20171208_Archive_e002049",
     "https://images-assets.nasa.gov/image/GSFC_20171208_Archive_e002049/GSFC_20171208_Archive_e002049~orig.jpg",
     "ok", "Young cluster in gas and dust. Confirm it is clean of caption text at harvest."),
]

# shot row, id, chapter, t0, t1, route, quality, asset, line
# route: harvest | code | card | flow | omni | gap | blocked
ROWS = [
    (1, "r01_stars_streaming", "0 Open", 0.12, 5.60, "harvest", None, "gaia_motion_1_6my", "Frame 0. Stars already streaming."),
    (2, "r02_gaia_span_2", "0 Open", 6.64, 13.18, "harvest", None, "gaia_motion_1_6my", "A later span of the same film, then the code graphic takes over."),
    (3, "r03_serpens_sky", "0 Open", 14.14, 17.20, "harvest", None, "gaia_edr3_sky", "Crop toward the Milky Way core. No label, no marker."),
    (4, "r04_shower", "0 Open", 18.02, 24.00, "code", None, "shower", "£0 code graphic. The star crossing the shell."),
    (4, "r04_shell_end", "0 Open", 24.00, 30.14, "code", None, "shell", "£0. End frame of the shell. Real picture sits between this and the next code row in the cut."),
    (5, "r05_drift", "0 Open", 31.30, 34.80, "code", None, "drift", "£0. Promise beat, one idea."),
    (5, "r05_path", "0 Open", 34.80, 38.30, "code", None, "path", "£0."),
    (5, "r05_sky", "0 Open", 38.30, 41.86, "code", None, "sky", "£0."),
    (6, "r06_milky_way", "1 The Star Heading Our Way", 42.78, 50.10, "harvest", None, "eso_mw_lasilla", "62 light-years, toward the galactic plane."),
    (7, "r07_sun", "1 The Star Heading Our Way", 51.04, 54.30, "harvest", None, "sdo_aia335", "Hold: this plate is ultraviolet, not visible light."),
    (7, "r07_kdwarf", "1 The Star Heading Our Way", 54.30, 57.54, "blocked", None, "k_dwarf_goldilocks", "Blocked. The 2020 Hubble release is a labelled chart."),
    (8, "r08_orbit_binoculars", "1 The Star Heading Our Way", 58.64, 66.52, "omni", None, "orbit_binoculars_omni_v01", "Orbit only. Vertex Omni, global, one take. No planet in frame."),
    (9, "r09_drift", "1 The Star Heading Our Way", 68.02, 81.92, "code", None, "drift", "£0. Wide, then tighter on the orange star."),
    (10, "r10_gliese_approach", "1 The Star Heading Our Way", 83.00, 93.64, "harvest", None, "gaia_gliese_encounter", "The Gliese 710 film, a different title from rows 1–2."),
    (11, "r11_night_road", "1 The Star Heading Our Way", 95.08, 109.20, "flow", "Quality", "night_road_veo_v01", "Shot list said Fast. Headlights at night are emissive, so this is Quality unless the Chief waives it."),
    (12, "r12_proxima", "1 The Star Heading Our Way", 110.32, 116.00, "harvest", None, "proxima", "026 callback. One line only."),
    (12, "r12_stars_move", "1 The Star Heading Our Way", 116.00, 126.04, "harvest", None, "gaia_motion_1_6my", "Third stretch of the 1.6-million-year film."),
    (13, "r13_star_trails", "2 How Close Will It Come?", 126.90, 133.84, "harvest", None, "eso_startrails", "A different ESO film from row 6."),
    (14, "r14_hipparcos", "2 How Close Will It Come?", 134.58, 140.00, "gap", None, "hipparcos_art", "Page only. No file URL yet."),
    (14, "r14_path", "2 How Close Will It Come?", 140.00, 146.98, "code", None, "path", "£0. The wide band, about 1 ly."),
    (15, "r15_gaia_craft", "2 How Close Will It Come?", 147.76, 154.00, "harvest", None, "gaia_craft", "Artist's impression."),
    (15, "r15_path", "2 How Close Will It Come?", 154.00, 161.04, "code", None, "path", "£0. The band narrows."),
    (16, "r16_path", "2 How Close Will It Come?", 162.06, 174.80, "code", None, "path", "£0. Thin band inside the 1-ly ring."),
    (17, "r17_scale_a", "2 How Close Will It Come?", 175.50, 181.50, "code", None, "scale", "£0. Earth, then the pull-back."),
    (17, "r17_neptune", "2 How Close Will It Come?", 181.50, 186.50, "harvest", None, "neptune", "On 'outermost planet'."),
    (17, "r17_scale_b", "2 How Close Will It Come?", 186.50, 191.00, "code", None, "scale", "£0. Not back-to-back with another code row: Neptune sits between the two scale spans."),
    (17, "r17_pitch", "2 How Close Will It Come?", 191.00, 194.82, "flow", "Fast", "football_pitch_veo_v01", "Dusk, no glow. Chief can lift this to Quality."),
    (18, "r18_shell", "2 How Close Will It Come?", 195.68, 203.76, "code", None, "shell", "£0. Close on the planet orbits. Stop before the shell pays off."),
    (19, "r19_subscribe", "2 How Close Will It Come?", 204.66, 209.44, "card", None, "subscribe_card", "£0 house card. Not a mint."),
    (20, "r20_shell", "3 Into the Oort Cloud", 210.34, 223.68, "code", None, "shell", "£0. Full pull-back."),
    (21, "r21_oort", "3 Into the Oort Cloud", 224.70, 232.84, "gap", None, "oort_page", "Illustration slot. File not pinned. Keep it clearly an illustration once it is."),
    (22, "r22_neowise", "3 Into the Oort Cloud", 234.16, 241.04, "harvest", None, "neowise_dc", "A long-period comet."),
    (23, "r23_orbit_ice", "3 Into the Oort Cloud", 241.88, 249.84, "omni", None, "orbit_ice_omni_v01", "Orbit only. Starfield and ice. No planet. One take."),
    (24, "r24_sunrise", "3 Into the Oort Cloud", 251.18, 257.00, "harvest", None, "iss_sunrise", "Sunlight arriving."),
    (24, "r24_shower", "3 Into the Oort Cloud", 257.00, 264.00, "code", None, "shower", "£0. The star entering the shell."),
    (25, "r25_shower", "4 The Comet Shower", 264.86, 280.58, "code", None, "shower", "£0. The nudge, then the infall."),
    (26, "r26_hale_bopp", "4 The Comet Shower", 281.74, 287.60, "harvest", None, "hale_bopp", "Licence hold."),
    (26, "r26_a3", "4 The Comet Shower", 287.60, 293.52, "harvest", None, "comet_a3", "Second comet, a different body."),
    (27, "r27_shower", "4 The Comet Shower", 294.48, 305.00, "code", None, "shower", "£0. Late infall."),
    (27, "r27_leaving", "4 The Comet Shower", 305.00, 315.46, "harvest", None, "gaia_motion_1_6my", "Fourth stretch. The star moving away."),
    (28, "r28_jupiter", "4 The Comet Shower", 316.62, 322.70, "harvest", None, "jupiter_juno", "No impact imagery."),
    (28, "r28_saturn", "4 The Comet Shower", 322.70, 328.80, "harvest", None, "saturn", "No impact imagery."),
    (28, "r28_hale_bopp_2", "4 The Comet Shower", 328.80, 335.00, "harvest", None, "hale_bopp", "Second use, a new framing. That is the twice-still cap. Same licence hold."),
    (29, "r29_night", "5 A New Brightest Star", 335.84, 342.00, "harvest", None, "eso_chajnantor", "A different night film from rows 6 and 13."),
    (29, "r29_sky", "5 A New Brightest Star", 342.00, 348.20, "code", None, "sky", "£0. The orange star brightens."),
    (29, "r29_twilight", "5 A New Brightest Star", 348.20, 354.40, "harvest", None, "conjunction", "Jupiter in a twilight sky. Saturn is also in frame."),
    (30, "r30_moon", "5 A New Brightest Star", 355.42, 359.50, "harvest", None, "moon_lro", "First use."),
    (30, "r30_sun_limb", "5 A New Brightest Star", 359.50, 363.52, "gap", None, "sdo_aia335", "Second SDO framing is not gathered. Do not reuse the AIA 335 disk; the shot list allows two uses with a new framing, and this one was meant to be the limb."),
    (31, "r31_sky", "5 A New Brightest Star", 364.50, 369.00, "code", None, "sky", "£0. Tighter on the orange star."),
    (31, "r31_moon_2", "5 A New Brightest Star", 369.00, 373.20, "harvest", None, "moon_lro", "Second use, a crop. Cap reached."),
    (31, "r31_sky_fade", "5 A New Brightest Star", 373.20, 377.30, "code", None, "sky", "£0."),
    (32, "r32_wise_sky", "6 It Has Happened Before", 378.30, 386.78, "harvest", None, "wise_sky", "Map. Check for labels."),
    (33, "r33_wise_craft", "6 It Has Happened Before", 387.72, 394.00, "harvest", None, "wise_craft", "Artist's concept."),
    (33, "r33_traffic", "6 It Has Happened Before", 394.00, 402.52, "code", None, "traffic", "£0. One dim pair crossing the outer shell."),
    (34, "r34_sky_wide", "6 It Has Happened Before", 403.30, 412.00, "harvest", None, "gaia_edr3_sky", "Second use, a wide crop against row 3. Cap reached."),
    (34, "r34_traffic", "6 It Has Happened Before", 412.00, 422.98, "code", None, "traffic", "£0."),
    (35, "r35_gaia_wide", "6 It Has Happened Before", 423.76, 434.78, "harvest", None, "gaia_motion_1_6my", "Fifth stretch. One more use after this fails the five-stretch rule."),
    (36, "r36_night_2", "6 It Has Happened Before", 436.86, 444.72, "gap", None, "eso_night_tafreshi", "Needs a confirmed file before it can be cut."),
    (37, "r37_cluster", "6 It Has Happened Before", 445.90, 451.40, "harvest", None, "ngc3603", "The Sun's birth cluster, hedged in the VO."),
    (37, "r37_shell", "6 It Has Happened Before", 451.40, 456.98, "code", None, "shell", "£0."),
    (38, "r38_neowise_2", "6 It Has Happened Before", 457.96, 463.00, "harvest", None, "neowise_dc", "Second use, a new crop. Cap reached."),
    (38, "r38_return", "6 It Has Happened Before", 463.00, 472.84, "harvest", None, "gaia_motion_1_6my", "Sixth stretch, and the visual-must return. Over the five-stretch cap. Chief's waiver or a different plate."),
]

PROMPTS = {
    "night_road_veo_v01": (
        "A long straight empty road at night. One car's headlights come straight at the camera and grow. "
        "No brands, no number plates, no text, no people, no buildings with signs. Silent. "
        "Continuous motion through the final frame. No Orbit."
    ),
    "football_pitch_veo_v01": (
        "An empty grass football pitch at dusk, from a high wide angle. White lines only. "
        "No crowds, no players, no club colours, no text, no logos. Daylight fading, nothing glowing. Silent. "
        "Continuous motion through the final frame. No Orbit."
    ),
    "orbit_binoculars_omni_v01": (
        "Orbit, the small orange robot, stands on a dark hill under a starfield. No planet in frame. "
        "Orbit sweeps the sky with binoculars, finds a faint orange dot, lowers them, and looks at a calendar too long to read. "
        "Start frame is Orbit on the hill. Vertex Omni only, location global, orbit_shot true, one take. Silent picture."
    ),
    "orbit_ice_omni_v01": (
        "Orbit floats among slow dark lumps of ice on a starfield. No planet in frame. "
        "Orbit taps one lump gently and watches it turn very slowly. "
        "Vertex Omni only, location global, orbit_shot true, one take. Silent picture."
    ),
}


def money(q):
    try1 = round(CLIP_S * USD_PER_S[q] * GBP_PER_USD, 2)
    expected = round(try1 * TAKES[q], 2)
    return try1, expected


def flow_expected(q):
    return math.ceil(FLOW_CREDITS[q] * TAKES[q])


def build():
    assets = {a[0]: {
        "id": a[0], "title": a[1], "credit": a[2], "licence": a[3],
        "page": a[4], "file": a[5], "status": a[6], "note": a[7],
    } for a in ASSETS}
    plates = []
    for shot, pid, chapter, t0, t1, route, quality, asset, line in ROWS:
        row = {
            "id": pid,
            "shot_list_row": shot,
            "chapter": chapter,
            "t_in_s": t0,
            "t_out_s": t1,
            "use_s": round(t1 - t0, 2),
            "route": route,
            "quality": quality,
            "asset_id": asset,
            "line": line,
            "generation_authorized": False,
            "reference": None,
            "prompt": PROMPTS.get(asset),
            "flow_credits_try1": 0,
            "flow_credits_expected": 0,
            "vertex_try1_gbp": 0.0,
            "vertex_expected_gbp": 0.0,
            "vertex_note": None,
        }
        if route == "flow":
            row["reference"] = "no still; text-to-video"
            row["flow_model"] = "Veo 3.1 " + quality
            row["flow_clip_s"] = CLIP_S
            row["flow_credits_try1"] = FLOW_CREDITS[quality]
            row["flow_credits_expected"] = flow_expected(quality)
            v1, vx = money(quality)
            row["vertex_model"] = "veo-3.1-generate-001" if quality == "Quality" else "veo-3.1-fast-generate-001"
            row["vertex_clip_s"] = CLIP_S
            row["vertex_try1_gbp"] = v1
            row["vertex_expected_gbp"] = vx
        elif route == "omni":
            row["reference"] = "Orbit start frame, no planet"
            row["vertex_model"] = "gemini-omni-flash-preview"
            row["vertex_note"] = "Unpriced, billed late. Not a Flow plate. One take."
        elif route == "code":
            row["reference"] = "07_Edit-Project/code_graphics.py"
        elif route == "card":
            row["reference"] = "house subscribe card"
        else:
            src = assets.get(asset, {})
            row["reference"] = src.get("file") or src.get("page")
            row["credit"] = src.get("credit")
            row["licence"] = src.get("licence")
            row["asset_status"] = "gap" if route == "gap" else src.get("status")
        plates.append(row)

    def count(route=None, quality=None, status=None):
        n = 0
        for p in plates:
            if route and p["route"] != route:
                continue
            if quality and p["quality"] != quality:
                continue
            if status and p.get("asset_status") != status:
                continue
            n += 1
        return n

    stretches = {}
    for p in plates:
        if p["route"] == "harvest":
            stretches.setdefault(p["asset_id"], []).append(p["id"])

    totals = {
        "plates": len(plates),
        "shot_list_rows": 38,
        "quality": count(route="flow", quality="Quality"),
        "fast": count(route="flow", quality="Fast"),
        "omni": count(route="omni"),
        "code": count(route="code"),
        "card": count(route="card"),
        "harvest_ok": sum(1 for p in plates if p["route"] == "harvest" and p.get("asset_status") == "ok"),
        "hold": sum(1 for p in plates if p.get("asset_status") == "hold"),
        "gap": count(route="gap"),
        "blocked": count(route="blocked"),
        "reuse": 0,
        "flow_credits_try1": sum(p["flow_credits_try1"] for p in plates),
        "flow_credits_expected": sum(p["flow_credits_expected"] for p in plates),
        "vertex_try1_gbp": round(sum(p["vertex_try1_gbp"] for p in plates), 2),
        "vertex_expected_gbp": round(sum(p["vertex_expected_gbp"] for p in plates), 2),
    }
    usable = round(VERTEX_BALANCE_GBP - VERTEX_MARGIN_GBP, 2)
    chapters = []
    for p in plates:
        if not chapters or chapters[-1]["chapter"] != p["chapter"]:
            chapters.append({"chapter": p["chapter"], "plates": []})
        chapters[-1]["plates"].append(p["id"])

    plan = {
        "film": "028",
        "title": "A Star Is Coming Into Our Solar System (Gliese 710)",
        "version": "v01",
        "job": "J0310",
        "mint": False,
        "status": "parked for Chief price pass",
        "built": "2026-10-15",
        "vo": "02_Voiceover/star_coming_vo_v01.wav",
        "shot_list": "07_Edit-Project/SHOT_LIST_v01.md",
        "readings": {
            "flow_credits_left": FLOW_CREDITS_LEFT,
            "flow_read_at": FLOW_READ_AT,
            "vertex_promo_gbp": VERTEX_BALANCE_GBP,
            "vertex_read_at": VERTEX_READ_AT,
            "vertex_margin_gbp": VERTEX_MARGIN_GBP,
            "vertex_usable_gbp": usable,
            "note": "No Flow spend logged after the Flow reading. No Vertex spend logged after the Vertex reading. Free Trial is £0. J0107 (HOS 006 Part 03) is done, so that reserve is not holding Vertex.",
        },
        "rates": {
            "flow_credits_per_take": FLOW_CREDITS,
            "takes_per_keep": TAKES,
            "vertex_usd_per_s": USD_PER_S,
            "gbp_per_usd": GBP_PER_USD,
            "clip_s": CLIP_S,
            "omni": "unpriced, billed late",
        },
        "totals": totals,
        "fits_now": {
            "flow": totals["flow_credits_expected"] <= FLOW_CREDITS_LEFT,
            "vertex_veo_only": totals["vertex_expected_gbp"] <= usable,
        },
        "harvest_stretches": stretches,
        "chapters": chapters,
        "plates": plates,
        "do_not_use": [assets["k_dwarf_goldilocks"]],
    }
    pool = {
        "film": "028",
        "version": "v01",
        "job": "J0310",
        "checked": "2026-10-15",
        "rule": "NASA public domain. ESA/Gaia/DPAC CC BY-SA 3.0 IGO. ESO and ESA/Hubble CC BY 4.0 unless a row says HOLD. No DSS2, no Aladin cut-outs, no University of Rochester Scholz's-star art.",
        "assets": list(assets.values()),
    }
    (HERE / "SOURCE_POOL_v01.json").write_text(json.dumps(pool, indent=2) + "\n")
    (HERE / "PLATE_BOARDS_v01.json").write_text(json.dumps(plan, indent=2) + "\n")
    (HERE / "PRICE_REVIEW_v01.md").write_text(review(plan, pool, stretches, usable))
    print(
        f"plates {totals['plates']} · Flow {totals['flow_credits_try1']} try-1 / "
        f"{totals['flow_credits_expected']} expected · Vertex £{totals['vertex_expected_gbp']:.2f} expected "
        f"(Veo only; Omni unpriced) · gaps {totals['gap']} · blocked {totals['blocked']}"
    )


def review(plan, pool, stretches, usable):
    t = plan["totals"]
    flow_fit = "FITS" if plan["fits_now"]["flow"] else "DOES NOT FIT"
    vx_fit = "FITS" if plan["fits_now"]["vertex_veo_only"] else "DOES NOT FIT"
    lines = [
        "# 028 price review v01",
        "",
        "Cursor, 15 Oct 2026, J0310. Source plates, prompts and prices only. **No mint. No spend.** Parked for Chief's price pass.",
        "",
        "Locked VO: `star_coming_vo_v01` (J0032, 8 Oct). Shot list: `SHOT_LIST_v01.md` (Claude, 8 Oct). The shot list's old £5 Vertex floor is not the rule any more. This table is Flow-first, on the same rates as HOS 009 J0261.",
        "",
        "## Readings",
        "",
        f"- Flow: **{FLOW_CREDITS_LEFT}** credits at {FLOW_READ_AT}. No spend logged after that.",
        f"- Vertex promo: **£{VERTEX_BALANCE_GBP:.2f}** at {VERTEX_READ_AT}. Usable **£{usable:.2f}** after the £1 margin on that reading. No spend logged after it. Free Trial is £0. J0107 is done, so the HOS 006 Part 03 reserve is not holding this.",
        "",
        "## Totals",
        "",
        "| | plates | Quality | Fast | Omni | code | harvest | gap | blocked | Flow try-1 | Flow expected | Vertex try-1 | Vertex expected |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        (
            f"| **Film** | **{t['plates']}** | **{t['quality']}** | **{t['fast']}** | **{t['omni']}** | "
            f"**{t['code']}** | **{t['harvest_ok']}** (+{t['hold']} on licence hold) | **{t['gap']}** | **{t['blocked']}** | "
            f"**{t['flow_credits_try1']}** | **{t['flow_credits_expected']}** | "
            f"**£{t['vertex_try1_gbp']:.2f}** | **£{t['vertex_expected_gbp']:.2f}** |"
        ),
        "",
        f"All on Flow, for the two Veo plates only: {flow_fit} ({t['flow_credits_expected']} expected vs {FLOW_CREDITS_LEFT} left).",
        f"Those two plates on Vertex: {vx_fit} (£{t['vertex_expected_gbp']:.2f} expected vs £{usable:.2f} usable).",
        "The two Orbit plates are Omni only. They are not in either total. Omni is unpriced and billed late.",
        "Code graphics, the subscribe card and the harvest plates are £0. Nothing is authorised to generate.",
        "",
        "Rates are 006/008/009's: Flow Fast 10 / Quality 100 a take; expected uses 005's takes-per-KEEP (Quality 2.59, Fast 1.96). Vertex is list price, 1080p, £0.80 per dollar, clip length 8 s.",
        "",
        "## What the picture actually is",
        "",
        "Most of the film is credited NASA, ESA or ESO footage, or a graphic we already draw in `code_graphics.py`. Flow is only the night road and the football pitch. That is the Flow-first split this shot list supports.",
        "",
        "| Plate | Route | Why |",
        "|---|---|---|",
        "| `night_road_veo_v01` | Quality | Headlights on a night road. The shot list said Fast. Fragile light stays Quality unless the Chief waives it. |",
        "| `football_pitch_veo_v01` | Fast | Empty pitch at dusk, no glow. The Chief can lift it to Quality. |",
        "| `orbit_binoculars_omni_v01`, `orbit_ice_omni_v01` | Omni | Orbit never goes through Flow or Veo. No planet in either start frame. |",
        "| `drift` `path` `scale` `shell` `shower` `sky` `traffic` | £0 code | Already in `code_graphics.py`. Text-free. Not a second mint when a later row uses the same graphic. |",
        "",
        "## Harvest stretches",
        "",
        "A still may appear twice. Footage may not come back in more than five stretches.",
        "",
    ]
    for asset_id, ids in stretches.items():
        if asset_id == "gaia_motion_1_6my":
            flag = " OVER THE FIVE-STRETCH CAP"
        elif len(ids) == 2:
            flag = " second use; still cap reached"
        else:
            flag = ""
        lines.append(f"- `{asset_id}` × {len(ids)}{flag}: {', '.join(ids)}")
    lines += [
        "",
        "## Holds, before any cut",
        "",
        "1. **Gliese motion, six stretches.** `gaia_motion_1_6my` is on r01, r02, r12, r27, r35 and r38. Five is the cap. r38 is the visual-must return to the opening. Drop r35, or the Chief waives the sixth.",
        "2. **K dwarf blocked.** The Hubble 2020 release the shot list names (`opo2006a`) is a labelled chart. It does not go in. No clean unlabelled K-dwarf plate was found.",
        "3. **SDO is ultraviolet.** `GSFC_20171208_Archive_e002035` is AIA 335, not visible light. The second framing (the limb) is not gathered.",
        "4. **Hale-Bopp licence.** `phot-mar14-hbs-2` is on the ESO site (CC BY 4.0 default). The 1997 event page says © Eckhard Slawik. Both uses wait on the Chief.",
        "5. **Three files are pages only.** Hipparcos art, the Oort Cloud illustration (do not use the Feild inset diagram), and the Tafreshi La Silla lapse (`bt_lasilla_fd2`, page 200, file 404 on the usual paths).",
        "6. **WISE all-sky** is a map. Look for axis labels before it is cut.",
        "7. **Gaia animations** are data films. `picture_qa` can fail a diagram. They are the moving source the shot list names. The annotated 'Tracking stellar motions' cut was not taken.",
        "8. **Juno PIA21974** is colour-enhanced. **PIA01492** is green and orange filters. Say so in the corner credit.",
        "9. **No DSS2, no Aladin, no Rochester Scholz's-star art.** None of those were gathered.",
        "10. **Code graphics stacked in the shot list.** These sit against the rule that two code graphics never run back to back: shower then shell (row 4), drift then path then sky (row 5), path then path (rows 15–16), shower then shower (rows 24–25). The cut needs a real plate between them, or the Chief accepts each stack as one beat.",
        "",
        "## For the price pass",
        "",
        "- Whether the night road stays Quality (100 credits try-1, 259 expected, £1.28 / £3.32 on Vertex) or drops to Fast.",
        "- Whether the dusk pitch stays Fast (10 / 20, £0.64 / £1.25).",
        "- The two Omni takes are extra, unpriced, and not part of the £4.57. They wait on a Vertex reading the day they are minted.",
        "- Which of the six Gliese-motion stretches is cut so the film stays inside five.",
        "- The Hale-Bopp licence, and who fills the three gaps (Hipparcos, Oort, Tafreshi) plus a visible-light Sun.",
        "",
        "Files: `SOURCE_POOL_v01.json`, `PLATE_BOARDS_v01.json`. Rebuild with `python3 _build_plate_boards_v01.py`.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    build()
