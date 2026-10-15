#!/usr/bin/env python3
"""029 plate boards v01. Boards, credits and prices only. No mint. No spend.

Rates match HOS 009 J0261 and 028 J0310 (15 Oct 2026): Flow Fast 10 / Quality
100 a take; expected uses 005's takes-per-KEEP (Quality 2.59, Fast 1.96).
Vertex is list price, 1080p, £0.80 per dollar, 8 s clip. Orbit stays Omni-only
and unpriced (billed late). Code graphics and credited harvest plates are £0.

The shot list names no Veo prop. Nothing in this table is authorised to generate.

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
# status: ok (HEAD 200 this run) | gap | hold | reject
ASSETS = [
    ("orion_rise_vlt", "VLT Auxiliary Telescopes time-lapse (Orion rising)",
     "ESO/B. Tafreshi (twanight.org)", "CC BY 4.0",
     "https://www.eso.org/public/videos/vlttimelapseorion/",
     "https://cdn.eso.org/videos/hd_1080p25_screen/vlttimelapseorion.mp4",
     "ok", "Page text: the rising constellation of Orion. 6 s, 30 fps, 4 May 2012. HEAD 200, 18.5 MB. Too short for a later unused part on the return."),
    ("orion_over_paranal", "Orion over Paranal",
     "ESO/B. Tafreshi", "CC BY 4.0",
     "https://www.eso.org/public/videos/bt-paranal-orion135mm/",
     "https://cdn.eso.org/videos/hd_1080p25_screen/bt-paranal-orion135mm.mp4",
     "ok", "Title is Orion over Paranal. 9 s, 25 Jan 2019. HEAD 200, 19.8 MB. A different film from the 2012 rise."),
    ("alma_orion_set", "ALMA dish and the setting Orion Nebula",
     "ESO/B. Tafreshi (twanight.org)", "CC BY 4.0",
     "https://www.eso.org/public/videos/ALMA16-OrionNebDish120mm/",
     "https://cdn.eso.org/videos/hd_1080p25_screen/ALMA16-OrionNebDish120mm.mp4",
     "ok", "The setting nebula plus a dish, 4 s. Not the constellation shoulder, and not a people-under-the-sky plate."),
    ("sphere_jan", "SPHERE's view of Betelgeuse in January 2019",
     "ESO/M. Montargès et al.", "CC BY 4.0",
     "https://www.eso.org/public/images/eso2003b/",
     "https://cdn.eso.org/images/large/eso2003b.jpg",
     "ok", "Single January 2019 panel (eso2003b). Original tif is on the page. Second use is a tight crop only."),
    ("sphere_dec", "SPHERE's view of Betelgeuse in December 2019",
     "ESO/M. Montargès et al.", "CC BY 4.0",
     "https://www.eso.org/public/images/eso2003a/",
     "https://cdn.eso.org/images/large/eso2003a.jpg",
     "ok", "Single December 2019 panel (eso2003a). Not the side-by-side."),
    ("sphere_compare", "Betelgeuse before and after dimming",
     "ESO/M. Montargès et al.", "CC BY 4.0",
     "https://www.eso.org/public/images/eso2003c/",
     "https://cdn.eso.org/images/large/eso2003c.jpg",
     "ok", "The comparison the shot list asks to show side by side, then push into December. One use."),
    ("visir_flames", "The flames of Betelgeuse",
     "ESO/P. Kervella", "CC BY 4.0",
     "https://www.eso.org/public/images/eso1121a/",
     "https://cdn.eso.org/images/large/eso1121a.jpg",
     "ok", "VISIR nebula (eso1121a), the plate the shot list calls eso1121. Second use is a new framing."),
    ("hl_tau", "ALMA image of the protoplanetary disc around HL Tauri",
     "ALMA (ESO/NAOJ/NRAO)", "CC BY 4.0",
     "https://www.eso.org/public/images/eso1436a/",
     "https://cdn.eso.org/images/large/eso1436a.jpg",
     "ok", "eso1436a. One use."),
    ("dust_impression", "Betelgeuse's Dust Cloud (Artist's Impression)",
     "ESO, ESA/Hubble, M. Kornmesser", "CC BY 4.0",
     "https://esahubble.org/images/heic2014a/",
     "https://cdn.esahubble.org/archives/images/large/heic2014a.jpg",
     "ok", "Artist's impression. The eso2109 stills checked this run are SPHERE photos, not this impression. Say it is an illustration."),
    ("mass_ejection", "Hubble Sees Red Supergiant Star Betelgeuse Slowly Recovering After Blowing Its Top",
     "NASA, ESA, E. Wheatley (STScI)", "CC BY 4.0",
     "https://esahubble.org/images/opo22037a/",
     "https://cdn.esahubble.org/archives/images/large/opo22037a.jpg",
     "ok", "2022 release. Wheatley is the STScI illustrator on the credit. Confirm it reads as an illustration. Second use is a new framing."),
    ("westerlund", "Westerlund 2 — Hubble's 25th anniversary image",
     "NASA, ESA, the Hubble Heritage Team (STScI/AURA), A. Nota (ESA/STScI), and the Westerlund 2 Science Team",
     "CC BY 4.0",
     "https://esahubble.org/images/heic1509a/",
     "https://cdn.esahubble.org/archives/images/large/heic1509a.jpg",
     "ok", "Wide then tight is two uses of one still. That is the cap."),
    ("tarantula", "Symphony of colours in the Tarantula",
     "ESA/NASA, ESO and Danny LaCrue", "CC BY 4.0",
     "https://esahubble.org/images/heic0416a/",
     "https://cdn.esahubble.org/archives/images/large/heic0416a.jpg",
     "ok", "30 Doradus. The page title does not say R136. Crop to the cluster, or the Chief can call this a gap."),
    ("crab", "Most detailed image of the Crab Nebula",
     "NASA, ESA and Allison Loll/Jeff Hester (Arizona State University)", "CC BY 4.0",
     "https://esahubble.org/images/heic0515a/",
     "https://cdn.esahubble.org/archives/images/large/heic0515a.jpg",
     "ok", "Hubble Crab. Tight filaments first, full frame second. That is the twice cap."),
    ("m42", "Hubble's sharpest view of the Orion Nebula",
     "NASA, ESA, M. Robberto (STScI/ESA) and the Hubble Space Telescope Orion Treasury Project Team",
     "CC BY 4.0",
     "https://esahubble.org/images/heic0601a/",
     "https://cdn.esahubble.org/archives/images/large/heic0601a.jpg",
     "ok", "M42. One use. Large file is 44 MB; not downloaded."),
    ("sdo_aia335", "SDO AIA 335 full disk (GSFC archive e002035)",
     "NASA/SDO (public domain)", "public domain",
     "https://images.nasa.gov/details/GSFC_20171208_Archive_e002035",
     "https://images-assets.nasa.gov/image/GSFC_20171208_Archive_e002035/GSFC_20171208_Archive_e002035~orig.jpg",
     "ok", "HEAD 200 this run (191 KB). J0310 read this same file as AIA 335 ultraviolet, not visible light. The limb framing is not gathered."),
    ("blue_marble", "View of the Earth as seen by the Apollo 17 crew (AS17-148-22727)",
     "NASA (public domain)", "public domain",
     "https://images.nasa.gov/details/as17-148-22727",
     "https://images-assets.nasa.gov/image/as17-148-22727/as17-148-22727~orig.jpg",
     "ok", "The Apollo 17 Blue Marble the shot list names. HEAD 200."),
    ("companion_speckle", "Betelgeuse and Its Stellar Companion (non-annotated)",
     "International Gemini Observatory/NOIRLab/NSF/AURA. Image processing: M. Zamani (NSF NOIRLab)",
     "CC BY 4.0 default; usage page linked, licence text not re-read this run",
     "https://noirlab.edu/public/images/noirlab2523c/",
     "https://storage.noirlab.edu/media/archives/images/large/noirlab2523c.jpg",
     "ok", "noirlab2523, 21 July 2025. Non-annotated sibling of noirlab2523a, which is not used. HEAD 200, 110 KB."),
    ("companion_orion", "Betelgeuse and Its Stellar Companion in Orion",
     "International Gemini Observatory/NOIRLab/NSF/AURA. Image processing: M. Zamani (NSF NOIRLab)",
     "CC BY 4.0 default; usage page linked, licence text not re-read this run",
     "https://noirlab.edu/public/images/noirlab2523b/",
     "https://storage.noirlab.edu/media/archives/images/large/noirlab2523b.jpg",
     "ok", "Different file from the non-annotated speckle. Confirm it is not a labelled chart before the cut. The annotated release image is noirlab2523a and is rejected."),
    ("antares_vlti", "VLTI reconstructed view of the surface of Antares",
     "ESO", "CC BY 4.0",
     "https://www.eso.org/public/images/eso1726a/",
     "https://cdn.eso.org/images/large/eso1726a.jpg",
     "reject", "The shot list calls this the ALMA surface of Betelgeuse. The page title is Antares. Do not use."),
    ("sphere_annot", "Betelgeuse's surface before and during its Great Dimming (with annotations)",
     "ESO/M. Montargès et al.", "CC BY 4.0",
     "https://www.eso.org/public/images/eso2109b/",
     None, "reject", "Annotated. Do not crop the labels off."),
    ("companion_annot", "Betelgeuse and Its Stellar Companion (annotated)",
     "International Gemini Observatory/NOIRLab/NSF/AURA", "CC BY 4.0",
     "https://noirlab.edu/public/images/noirlab2523a/",
     None, "reject", "Annotated. Use noirlab2523c."),
    ("sky_telescope", "Betelgeuse in Orion (noirlab2523f)",
     "IAU and Sky & Telescope", "HOLD",
     "https://noirlab.edu/public/images/noirlab2523f/",
     None, "reject", "Credit is IAU and Sky & Telescope, not a NOIRLab CC BY line. Not cleared."),
    ("suomi_marble", "Earth (Suomi NPP VIIRS Blue Marble montage, PIA18033)",
     "NASA (public domain)", "public domain",
     "https://images.nasa.gov/details/PIA18033",
     "https://images-assets.nasa.gov/image/PIA18033/PIA18033~orig.jpg",
     "reject", "Not DSCOVR EPIC. The description says Suomi NPP VIIRS. Do not stand in for the EPIC plates."),
    ("hubble_pillars", "New view of the Pillars of Creation — visible",
     "NASA, ESA/Hubble and the Hubble Heritage Team", "CC BY 4.0",
     "https://esahubble.org/images/heic1501a/",
     "https://cdn.esahubble.org/archives/images/large/heic1501a.jpg",
     "reject", "Hubble 2015, not JWST. The shot list asks for the JWST Pillars. Do not substitute."),
    ("superk", "Super-Kamiokande inner tank",
     "ICRR, The University of Tokyo", "HOLD",
     "https://www-sk.icrr.u-tokyo.ac.jp/en/",
     None, "hold", "Shot-list licence gate. No ICRR file was gathered. Terms for a monetised channel were not found this run."),
    ("orion_span_c", "Orion span C", "", "gap", None, None, "gap",
     "No third ESO clip whose page names Orion was found. Spans C–G are open."),
    ("orion_span_d", "Orion span D", "", "gap", None, None, "gap", "Open."),
    ("orion_span_e", "Orion span E", "", "gap", None, None, "gap", "Open."),
    ("orion_span_f", "Orion span F", "", "gap", None, None, "gap", "Open."),
    ("orion_span_g", "Orion span G", "", "gap", None, None, "gap", "Open."),
    ("paranal_other", "A Paranal night lapse that is not span A or span B", "", "gap", None, None, "gap",
     "026's Paranal files were not re-checked against a page this run, so they are not in the pool."),
    ("vlt_night", "VLT under the night sky, no lasers", "", "gap", None, None, "gap", "Open."),
    ("mw_lapse", "ESO Milky Way time-lapse, a clip not already used", "", "gap", None, None, "gap", "Open."),
    ("people_night", "ESO photo of people under the night sky", "", "gap", None, None, "gap", "Open."),
    ("epic", "DSCOVR EPIC full-disk Earth", "", "gap", None, None, "gap",
     "PIA18033 was checked and rejected (Suomi NPP). No EPIC file pinned."),
    ("half_moon", "NASA SVS half Moon", "", "gap", None, None, "gap", "No SVS file pinned this run."),
    ("neutron", "NASA GSFC neutron-star illustration", "", "gap", None, None, "gap", "No unlabelled GSFC illustration pinned."),
    ("hero_007", "007 hero plate callback", "", "gap", None, None, "gap",
     "No 007 hero file path was verified this run. Not entered as a reuse."),
    ("black_hole", "NASA GSFC black-hole visualisation", "", "gap", None, None, "gap", "No file pinned."),
    ("casa", "Cassiopeia A (Chandra or JWST)", "", "gap", None, None, "gap", "No file pinned."),
    ("jwst_pillars", "JWST Pillars of Creation", "", "gap", None, None, "gap",
     "heic1501a is the Hubble Pillars and is rejected as a substitute."),
    ("gemini_night", "Gemini North at night", "", "gap", None, None, "gap",
     "The noirlab2523 release images found this run are the companion, not the telescope."),
    ("gemini_dome", "Gemini North dome", "", "gap", None, None, "gap", "Open."),
    ("met_astrolabe", "Met Open Access 15th-century astrolabe", "", "gap", None, None, "gap",
     "The Met collection API returned HTTP 410 this run. No object pinned."),
    ("met_song", "Met Open Access Northern Song object", "", "gap", None, None, "gap",
     "Same API failure. No object pinned."),
    ("icecube", "IceCube detector photo (NSF), Super-K fallback", "", "gap", None, None, "gap",
     "Not gathered. Only if its licence clears a monetised channel."),
]

# shot, id, chapter, t0, t1, route, quality, asset, line
ROWS = [
    (1, "r01_orion_rise", "0 Open", 0.08, 5.70, "harvest", None, "orion_rise_vlt",
     "Frame 0. Stars already moving. Span A. The clip is 6 s, so the return has almost no later part."),
    (2, "r02_orion_b", "0 Open", 6.54, 10.00, "harvest", None, "orion_over_paranal",
     "Span B, the start of the 9 s clip."),
    (2, "r02_surface", "0 Open", 10.00, 13.34, "gap", None, "antares_vlti",
     "The shot list's eso1726a is Antares. No other single Betelgeuse surface was free: the SPHERE panels are kept for rows 6, 7, 13 and 32."),
    (3, "r03_orion_code", "0 Open", 13.96, 21.40, "code", None, "orion",
     "£0. Preview only. The full flare is rows 25–27."),
    (4, "r04_scale", "0 Open", 22.58, 27.38, "code", None, "scale", "£0. Promise beat."),
    (4, "r04_dip", "0 Open", 27.38, 32.16, "code", None, "dip", "£0. Stacked with the scale and the shells. Needs a real plate between them, or the Chief accepts one beat."),
    (4, "r04_shells", "0 Open", 32.16, 36.94, "code", None, "shells", "£0."),
    (5, "r05_surface", "1 The Star in Orion's Shoulder", 37.74, 41.90, "gap", None, "antares_vlti",
     "Second use of eso1726a cannot happen: that file is Antares."),
    (5, "r05_scale", "1 The Star in Orion's Shoulder", 41.90, 48.58, "code", None, "scale",
     "£0. The edge passes Mars about 46 s."),
    (6, "r06_paranal", "1 The Star in Orion's Shoulder", 49.46, 55.00, "gap", None, "paranal_other",
     "Needs a Paranal lapse that is not span A or span B."),
    (6, "r06_sphere_jan", "1 The Star in Orion's Shoulder", 55.00, 61.74, "harvest", None, "sphere_jan",
     "January 2019 single panel. First use."),
    (7, "r07_sdo", "1 The Star in Orion's Shoulder", 62.46, 67.50, "harvest", None, "sdo_aia335",
     "Ultraviolet, not visible light. Say so in the corner credit, or gather an HMI continuum."),
    (7, "r07_sphere_jan", "1 The Star in Orion's Shoulder", 67.50, 72.84, "harvest", None, "sphere_jan",
     "Second use, a tight crop. Cap reached."),
    (8, "r08_westerlund_w", "1 The Star in Orion's Shoulder", 73.86, 80.00, "harvest", None, "westerlund",
     "Wide."),
    (8, "r08_westerlund_t", "1 The Star in Orion's Shoulder", 80.00, 86.00, "harvest", None, "westerlund",
     "Tight. Two uses of one still. Cap reached."),
    (8, "r08_tarantula", "1 The Star in Orion's Shoulder", 86.00, 91.92, "harvest", None, "tarantula",
     "30 Doradus. Confirm the crop is R136."),
    (9, "r09_finder", "1 The Star in Orion's Shoulder", 92.92, 105.48, "code", None, "finder",
     "£0. Belt, then the trail, then the orange star."),
    (10, "r10_span_c", "2 The Great Dimming", 106.38, 109.50, "gap", None, "orion_span_c", "Span C is not gathered."),
    (10, "r10_dip", "2 The Great Dimming", 109.50, 114.20, "code", None, "dip", "£0. Dip starts at 109.5 s."),
    (11, "r11_dip", "2 The Great Dimming", 115.00, 123.16, "code", None, "dip",
     "£0. Continued. Wide, then tight on the trough."),
    (12, "r12_orbit_thumb", "2 The Great Dimming", 123.96, 129.38, "omni", None, "orbit_thumb_omni_v01",
     "Orbit only. No planet. One take. If it fails, span C would hold, and span C is still a gap."),
    (13, "r13_compare", "2 The Great Dimming", 130.42, 137.80, "harvest", None, "sphere_compare",
     "Side by side, then push into the December half."),
    (14, "r14_ejection", "2 The Great Dimming", 138.44, 142.80, "harvest", None, "mass_ejection",
     "2022 illustration. First use."),
    (14, "r14_dust", "2 The Great Dimming", 142.80, 147.16, "harvest", None, "dust_impression",
     "Artist's impression (heic2014a), in place of an eso2109 impression that was not on the release."),
    (15, "r15_span_d", "2 The Great Dimming", 148.04, 152.80, "gap", None, "orion_span_d", "Span D is not gathered."),
    (15, "r15_dip", "2 The Great Dimming", 152.80, 157.76, "code", None, "dip", "£0. Second use of the dip, tight on the trough."),
    (16, "r16_span_e", "2 The Great Dimming", 158.58, 163.80, "gap", None, "orion_span_e", "Span E is not gathered."),
    (16, "r16_visir", "2 The Great Dimming", 163.80, 168.98, "harvest", None, "visir_flames", "VISIR. First use."),
    (17, "r17_sdo", "3 How a Giant Star Dies", 170.00, 175.40, "gap", None, "sdo_aia335",
     "Second SDO framing (limb or prominence) is not gathered. Do not reuse the full disk."),
    (17, "r17_shells", "3 How a Giant Star Dies", 175.40, 180.88, "code", None, "shells", "£0. Held start frame."),
    (18, "r18_shells", "3 How a Giant Star Dies", 181.70, 199.08, "code", None, "shells", "£0. One continuous render, reframed."),
    (19, "r19_shells", "3 How a Giant Star Dies", 199.78, 211.06, "code", None, "shells", "£0. Tight on the iron core."),
    (20, "r20_shells", "3 How a Giant Star Dies", 211.94, 224.02, "code", None, "shells",
     "£0. Collapse at 211.95, then the shock."),
    (20, "r20_crab", "3 How a Giant Star Dies", 224.02, 225.58, "harvest", None, "crab",
     "Tight on the filaments. Full frame is saved for row 35."),
    (21, "r21_neutron", "3 How a Giant Star Dies", 226.64, 232.00, "gap", None, "neutron", "No GSFC illustration pinned."),
    (21, "r21_hero", "3 How a Giant Star Dies", 232.00, 236.80, "gap", None, "hero_007", "Callback not verified as a file."),
    (21, "r21_bh", "3 How a Giant Star Dies", 236.80, 241.88, "gap", None, "black_hole", "No GSFC visualisation pinned."),
    (22, "r22_subscribe", "3 How a Giant Star Dies", 242.70, 247.18, "card", None, "subscribe_card",
     "£0 house card. Not a mint."),
    (23, "r23_paranal", "4 The Night It Goes", 248.06, 254.38, "gap", None, "paranal_other",
     "Needs a clip not used in row 6. Row 6 is itself still a gap."),
    (24, "r24_superk", "4 The Night It Goes", 255.30, 261.00, "hold", None, "superk", "Licence gate. No file."),
    (24, "r24_epic", "4 The Night It Goes", 261.00, 267.00, "gap", None, "epic", "No DSCOVR file."),
    (24, "r24_superk_2", "4 The Night It Goes", 267.00, 273.10, "hold", None, "superk",
     "Second Super-K plate, same hold."),
    (25, "r25_orion", "4 The Night It Goes", 274.12, 282.16, "code", None, "orion",
     "£0. Flare from about 276.7 s. Wide, then tight."),
    (26, "r26_orbit_flare", "4 The Night It Goes", 282.92, 286.50, "omni", None, "orbit_flare_omni_v01",
     "Orbit only. No planet. One take."),
    (26, "r26_moon", "4 The Night It Goes", 286.50, 290.04, "gap", None, "half_moon", "No SVS half Moon pinned."),
    (27, "r27_orion", "4 The Night It Goes", 290.98, 309.46, "code", None, "orion",
     "£0. The fade, until the shoulder is empty."),
    (28, "r28_epic", "4 The Night It Goes", 310.80, 315.60, "gap", None, "epic", "Second EPIC framing. No file."),
    (28, "r28_mw", "4 The Night It Goes", 315.60, 320.50, "gap", None, "mw_lapse", "No Milky Way lapse pinned."),
    (28, "r28_people", "4 The Night It Goes", 320.50, 325.46, "gap", None, "people_night", "No people-under-the-sky photo pinned."),
    (29, "r29_span_f", "4 The Night It Goes", 326.56, 334.00, "gap", None, "orion_span_f", "Span F is not gathered."),
    (29, "r29_astrolabe", "4 The Night It Goes", 334.00, 342.14, "gap", None, "met_astrolabe", "Met API returned 410."),
    (30, "r30_span_g", "5 So When?", 342.92, 350.00, "gap", None, "orion_span_g", "Span G is not gathered."),
    (30, "r30_vlt", "5 So When?", 350.00, 357.62, "gap", None, "vlt_night", "No spare VLT night clip."),
    (31, "r31_shells", "5 So When?", 359.36, 362.60, "code", None, "shells", "£0. Tight on the core."),
    (31, "r31_twins", "5 So When?", 362.60, 378.30, "code", None, "twins",
     "£0. Wedges open about 367 s and close about 376 s."),
    (32, "r32_sphere_dec", "5 So When?", 379.44, 385.70, "harvest", None, "sphere_dec", "December 2019 single panel."),
    (32, "r32_ejection", "5 So When?", 385.70, 392.00, "harvest", None, "mass_ejection",
     "Second use, a new framing. Cap reached."),
    (33, "r33_speckle", "5 So When?", 393.34, 403.00, "harvest", None, "companion_speckle",
     "Non-annotated Gemini/'Alopeke release image."),
    (33, "r33_pair", "5 So When?", 403.00, 412.74, "harvest", None, "companion_orion",
     "The 'in Orion' release image. Confirm it is not a labelled chart."),
    (34, "r34_gemini", "5 So When?", 413.96, 419.50, "gap", None, "gemini_night", "No Gemini North night photo."),
    (34, "r34_pair", "5 So When?", 419.50, 425.30, "harvest", None, "companion_orion",
     "Second use, wider. Cap reached if the first use stands."),
    (34, "r34_dome", "5 So When?", 425.30, 431.08, "gap", None, "gemini_dome", "No dome photo."),
    (35, "r35_song", "5 So When?", 432.60, 442.00, "gap", None, "met_song", "Met API returned 410."),
    (35, "r35_crab", "5 So When?", 442.00, 452.30, "harvest", None, "crab", "Full frame. Second use. Cap reached."),
    (36, "r36_orion_b", "5 So When?", 453.84, 459.80, "harvest", None, "orion_over_paranal",
     "Later part of the 9 s span B clip, not the row 2 frames. The clip may be too short to do that cleanly."),
    (36, "r36_visir", "5 So When?", 459.80, 465.82, "harvest", None, "visir_flames", "Second use. Cap reached."),
    (37, "r37_casa", "5 So When?", 466.92, 475.80, "gap", None, "casa", "No Cassiopeia A file."),
    (37, "r37_pillars", "5 So When?", 475.80, 484.26, "gap", None, "jwst_pillars", "JWST not gathered. Hubble Pillars rejected."),
    (38, "r38_m42", "5 So When?", 485.84, 491.00, "harvest", None, "m42", "Hubble M42."),
    (38, "r38_night", "5 So When?", 491.00, 496.36, "harvest", None, "alma_orion_set",
     "4 s. An ALMA dish and the setting nebula, not a landscape with people."),
    (39, "r39_hltau", "5 So When?", 497.42, 503.00, "harvest", None, "hl_tau", "ALMA HL Tau disc."),
    (39, "r39_marble", "5 So When?", 503.00, 508.50, "harvest", None, "blue_marble", "Apollo 17 Blue Marble."),
    (39, "r39_return", "5 So When?", 508.50, 517.26, "harvest", None, "orion_rise_vlt",
     "Return to span A. Second stretch of a 6 s clip. Hold 2–3 s past the last word is longer than the clip."),
]

PROMPTS = {
    "orbit_thumb_omni_v01": (
        "Orbit, the small orange robot, stands on a dark winter hill under stars. No planet in frame. "
        "Orbit holds up a thumb towards Orion, squints, lowers it, looks a little worried, and waits. "
        "Start frame is Orbit on the hill. Vertex Omni only, location global, orbit_shot true, one take. Silent picture."
    ),
    "orbit_flare_omni_v01": (
        "Orbit stands on a dark field at night under stars. No planet in frame. "
        "One point of light swells into a brilliant white dot. Orbit lifts a hand to shade the visor and stares. "
        "Start frame is Orbit on the field. Vertex Omni only, location global, orbit_shot true, one take. Silent picture."
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
            row["asset_status"] = src.get("status")
        plates.append(row)

    def count(route=None, quality=None):
        return sum(
            1 for p in plates
            if (route is None or p["route"] == route)
            and (quality is None or p["quality"] == quality)
        )

    stretches = {}
    for p in plates:
        if p["route"] == "harvest":
            stretches.setdefault(p["asset_id"], []).append(p["id"])

    totals = {
        "plates": len(plates),
        "shot_list_rows": 39,
        "quality": count(route="flow", quality="Quality"),
        "fast": count(route="flow", quality="Fast"),
        "omni": count(route="omni"),
        "code": count(route="code"),
        "card": count(route="card"),
        "harvest_ok": sum(1 for p in plates if p["route"] == "harvest" and p.get("asset_status") == "ok"),
        "hold": count(route="hold"),
        "gap": count(route="gap"),
        "blocked": count(route="blocked"),
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
        "film": "029",
        "title": "Is Betelgeuse About to Explode?",
        "version": "v01",
        "job": "J0311",
        "mint": False,
        "status": "parked for Chief price pass",
        "built": "2026-10-15",
        "vo": "02_Voiceover/betelgeuse_vo_v01.wav",
        "shot_list": "07_Edit-Project/SHOT_LIST_v01.md",
        "readings": {
            "flow_credits_left": FLOW_CREDITS_LEFT,
            "flow_read_at": FLOW_READ_AT,
            "vertex_promo_gbp": VERTEX_BALANCE_GBP,
            "vertex_read_at": VERTEX_READ_AT,
            "vertex_margin_gbp": VERTEX_MARGIN_GBP,
            "vertex_usable_gbp": usable,
            "note": "No Flow spend logged after the Flow reading. No Vertex spend logged after the Vertex reading. Free Trial is £0. J0107 is done, so the HOS 006 Part 03 reserve is not holding this.",
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
        "do_not_use": [
            assets["antares_vlti"], assets["sphere_annot"], assets["companion_annot"],
            assets["sky_telescope"], assets["suomi_marble"], assets["hubble_pillars"],
        ],
    }
    pool = {
        "film": "029",
        "version": "v01",
        "job": "J0311",
        "checked": "2026-10-15",
        "rule": "NASA public domain. ESO and ESA/Hubble CC BY 4.0. NOIRLab default CC BY 4.0 where the credit is NOIRLab's own. No DSS2, no Aladin, no news footage. eso1726a is Antares and is rejected.",
        "assets": list(assets.values()),
    }
    (HERE / "SOURCE_POOL_v01.json").write_text(json.dumps(pool, indent=2) + "\n")
    (HERE / "PLATE_BOARDS_v01.json").write_text(json.dumps(plan, indent=2) + "\n")
    (HERE / "PRICE_REVIEW_v01.md").write_text(review(plan, stretches, usable))
    print(
        f"plates {totals['plates']} · harvest {totals['harvest_ok']} · "
        f"gap {totals['gap']} · hold {totals['hold']} · "
        f"Flow {totals['flow_credits_expected']} expected · "
        f"Vertex £{totals['vertex_expected_gbp']:.2f}"
    )


def review(plan, stretches, usable):
    t = plan["totals"]
    lines = []
    for aid, ids in sorted(stretches.items(), key=lambda kv: -len(kv[1])):
        n = len(ids)
        flag = ""
        if n > 5:
            flag = " OVER THE FIVE-STRETCH CAP"
        elif n == 2:
            flag = " second use; still cap reached"
        lines.append(f"- `{aid}` × {n}{flag}: " + ", ".join(ids))
    stretch_md = "\n".join(lines)
    return "\n".join([
        "# 029 price review v01",
        "",
        "Cursor, 15 Oct 2026, J0311. Source plates and prices only. **No mint. No spend.** Parked for Chief's price pass.",
        "",
        "Locked VO: `betelgeuse_vo_v01` (J0040, 8 Oct, 515.2 s). Shot list: `SHOT_LIST_v01.md` (Claude, 8 Oct). The shot list's old £5 Vertex floor is not the rule any more. This table is Flow-first, on the same rates as HOS 009 J0261 and 028 J0310.",
        "",
        "## Readings",
        "",
        f"- Flow: **{FLOW_CREDITS_LEFT}** credits at {FLOW_READ_AT}. No spend logged after that.",
        f"- Vertex promo: **£{VERTEX_BALANCE_GBP:.2f}** at {VERTEX_READ_AT}. Usable **£{usable:.2f}** after the £1 margin. No spend logged after it. Free Trial is £0. J0107 is done, so the HOS 006 Part 03 reserve is not holding this.",
        "",
        "## Totals",
        "",
        "| | plates | Quality | Fast | Omni | code | harvest | gap | hold | Flow try-1 | Flow expected | Vertex try-1 | Vertex expected |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        f"| **Film** | **{t['plates']}** | **{t['quality']}** | **{t['fast']}** | **{t['omni']}** | **{t['code']}** | **{t['harvest_ok']}** | **{t['gap']}** | **{t['hold']}** | **{t['flow_credits_try1']}** | **{t['flow_credits_expected']}** | **£{t['vertex_try1_gbp']:.2f}** | **£{t['vertex_expected_gbp']:.2f}** |",
        "",
        "The shot list names no Veo prop, and none was added. Flow expected is 0, which fits 23730 left.",
        "Vertex Veo expected is £0.00, which fits the usable promo.",
        "The two Orbit plates are Omni only. They are not in either total. Omni is unpriced and billed late.",
        "Code graphics, the subscribe card and the harvest plates are £0. Nothing is authorised to generate.",
        "",
        "Rates are 006/008/009/028's: Flow Fast 10 / Quality 100 a take; expected uses 005's takes-per-KEEP (Quality 2.59, Fast 1.96). Vertex is list price, 1080p, £0.80 per dollar, clip length 8 s.",
        "",
        "## What the picture actually is",
        "",
        "Most of the locked picture is credited ESO, ESA/Hubble or NASA, or a graphic already in `code_graphics.py`. There is no night-road equivalent: the shot list's moving plates are real night-sky films, not generated props.",
        "",
        "| Plate | Route | Why |",
        "|---|---|---|",
        "| `orbit_thumb_omni_v01`, `orbit_flare_omni_v01` | Omni | Orbit never goes through Flow or Veo. No planet in either start frame. |",
        "| `scale` `dip` `shells` `orion` `finder` `twins` | £0 code | Already in `code_graphics.py`. Text-free. A later row of the same graphic is not a second mint. |",
        "",
        "## Harvest stretches",
        "",
        "A still may appear twice. Footage may not come back in more than five stretches.",
        "",
        stretch_md,
        "",
        "## Holds, before any cut",
        "",
        "1. **eso1726a is Antares.** The shot list uses it as the ALMA surface of Betelgeuse at rows 2 and 5. The page title is the VLTI view of Antares. It is rejected. Those two beats are gaps.",
        "2. **Only two Orion clips.** `vlttimelapseorion` (6 s, rising Orion, span A) and `bt-paranal-orion135mm` (9 s, Orion over Paranal, span B). Spans C, D, E, F and G were not found. The 6 s rise cannot supply a later unused part for the row 39 return, and the hold past the last word is longer than the clip.",
        "3. **SDO is ultraviolet.** The file is the one J0310 read as AIA 335. This run only checked HEAD 200. The limb framing for row 17 was not gathered.",
        "4. **DSCOVR was not found.** PIA18033 is a Suomi NPP VIIRS montage. It is rejected. Both EPIC beats are gaps.",
        "5. **Super-Kamiokande is on hold.** No ICRR file, and no monetised-use term, was gathered. IceCube was not gathered either.",
        "6. **Met API returned HTTP 410.** The astrolabe and the Northern Song object are gaps.",
        "7. **JWST Pillars and Cassiopeia A are gaps.** The Hubble Pillars (`heic1501a`) are rejected as a substitute.",
        "8. **Neutron-star illustration, black-hole visualisation, SVS half Moon and the 007 hero callback** have no file pinned this run.",
        "9. **Gemini North at night and the dome** are not in the noirlab2523 images that were opened. The companion images are `noirlab2523c` (non-annotated) and `noirlab2523b` (in Orion). Confirm `noirlab2523b` is not a labelled chart. `noirlab2523a` is annotated and rejected. `noirlab2523f` is credited to IAU and Sky & Telescope and is rejected.",
        "10. **Dust impression is heic2014a**, not an eso2109 still. The eso2109 frames checked are SPHERE photos. `eso2109b` is annotated and rejected.",
        "11. **Tarantula plate.** `heic0416a` is 30 Doradus. The title does not say R136.",
        "12. **Code graphics stacked in the shot list.** Scale, dip and shells sit together in row 4. Dip continues into row 11. Shells run through rows 17–20 and return at row 31 beside twins. Two code graphics never run back to back unless a real plate sits between them, or the Chief accepts each stack as one beat.",
        "13. **NOIRLab licence.** The image pages link the usage page. The default was not re-read this run. Treat them as CC BY 4.0 only if that page still says so.",
        "",
        "## For the price pass",
        "",
        "- There is no Flow plate to waive from Quality to Fast. Expected Flow is 0.",
        "- The two Omni takes are extra, unpriced, and not part of the £0.00 Veo total. They wait on a Vertex reading the day they are minted.",
        "- Whether row 2 and row 5 stay gaps until a real Betelgeuse surface (not Antares) is gathered.",
        "- Whether spans C–G block the cut, and whether the 6 s Orion rise is allowed to return at the end.",
        "- Super-K versus IceCube versus dropping row 24 to a night-sky plate.",
        "- Who fills DSCOVR, the Met objects, JWST, Cassiopeia A, the GSFC illustrations, the half Moon, and Gemini North.",
        "",
        "Files: `SOURCE_POOL_v01.json`, `PLATE_BOARDS_v01.json`. Rebuild with `python3 _build_plate_boards_v01.py`.",
        "",
    ])


if __name__ == "__main__":
    build()
