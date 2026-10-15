#!/usr/bin/env python3
"""029 plate boards v02 from v01, applying Chief's J0311 rulings (comment 6202235397).

No mint. No spend. Rebuilds PLATE_BOARDS_v02.json, SOURCE_POOL_v02.json and
PRICE_REVIEW_v02.md next to this file.

  python3 _build_plate_boards_v02.py
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

EDIT = Path(__file__).resolve().parent
V01 = EDIT / "PLATE_BOARDS_v01.json"
POOL_V01 = EDIT / "SOURCE_POOL_v01.json"

# Fresh readings this run (ai_spend_daily.py --dry-run --pools vertex,flow), 15 Oct 2026.
FLOW_LEFT = 23740
FLOW_READ_AT = "2026-10-15T23:46:58Z"
VERTEX_PROMO = 71.02
VERTEX_READ_AT = "2026-10-15T23:46:58Z"
VERTEX_MARGIN = 1.0
GBP_PER_USD = 0.8

# Gemini Omni Flash list price (cloud.google.com/vertex-ai/generative-ai/pricing):
# video output $0.10/s of 720p with audio. Image input 2,040 tokens at $1.50/1M.
OMNI_USD_PER_S = 0.10
OMNI_S = 8
OMNI_IMAGE_TOKENS = 2040 * 2
OMNI_TEXT_TOKENS = 400
OMNI_USD = OMNI_S * OMNI_USD_PER_S + (OMNI_IMAGE_TOKENS + OMNI_TEXT_TOKENS) * 1.50 / 1_000_000
OMNI_GBP = round(OMNI_USD * GBP_PER_USD, 2)

# J0337 headroom table (Chief, 15 Oct). 029 adds no Flow.
HOS_EXPECTED = {"006": 0, "007": 7553, "008": 5605, "009": 7354}
OWB_028_FLOW = 279

NOIRLAB_LICENCE = "CC BY 4.0"
NOIRLAB_NOTE = (
    "NOIRLab usage page re-read 16 Oct 2026 (https://noirlab.edu/public/copyright/): "
    "Creative Commons Attribution 4.0 International. noirlab2523a and noirlab2523f stay rejected."
)
ESO_LICENCE = "CC BY 4.0"
ESO_NOTE = (
    "ESO copyright page re-read 16 Oct 2026 (https://www.eso.org/public/outreach/copyright/): "
    "images, videos, pictures of the week and captions are Creative Commons Attribution 4.0 International."
)


def zero(p: dict) -> None:
    p["flow_credits_try1"] = 0
    p["flow_credits_expected"] = 0
    p["vertex_try1_gbp"] = 0.0
    p["vertex_expected_gbp"] = 0.0
    p["generation_authorized"] = False
    p["quality"] = None
    p.pop("vertex_model", None)
    p.pop("vertex_clip_s", None)


def find(plates: list[dict], pid: str) -> dict:
    for p in plates:
        if p["id"] == pid:
            return p
    raise SystemExit(f"missing plate {pid}")


def drop(plates: list[dict], pid: str) -> dict:
    for i, p in enumerate(plates):
        if p["id"] == pid:
            return plates.pop(i)
    raise SystemExit(f"missing plate {pid}")


def as_code(p: dict, asset: str, line: str) -> None:
    zero(p)
    p["route"] = "code"
    p["asset_id"] = asset
    p["asset_status"] = "code"
    p["line"] = line
    p["credit"] = None
    p["licence"] = "£0 code graphic"
    p["reference"] = "07_Edit-Project/code_graphics.py"
    p["prompt"] = None
    p["vertex_note"] = "£0 code graphic. Not a mint."


def as_harvest(
    p: dict,
    asset: str,
    line: str,
    credit: str,
    licence: str,
    reference: str,
    source_in: float | None = None,
    source_out: float | None = None,
) -> None:
    zero(p)
    p["route"] = "harvest"
    p["asset_id"] = asset
    p["asset_status"] = "ok"
    p["line"] = line
    p["credit"] = credit
    p["licence"] = licence
    p["reference"] = reference
    p["prompt"] = None
    p["vertex_note"] = "£0 harvest"
    if source_in is not None:
        p["source_in_s"] = source_in
        p["source_out_s"] = source_out


def merge_to(keep: dict, dropped: dict, new_id: str, asset: str, line: str) -> None:
    keep["id"] = new_id
    keep["t_out_s"] = dropped["t_out_s"]
    keep["use_s"] = round(keep["t_out_s"] - keep["t_in_s"], 2)
    as_code(keep, asset, line)


def main() -> None:
    boards = json.loads(V01.read_text())
    pool = json.loads(POOL_V01.read_text())
    plates: list[dict] = boards["plates"]

    # --- Ruling 8: merge every named code stack into one beat ---
    # Rows 3 and 4 sit code-against-code. One beat, not four renders.
    r03 = find(plates, "r03_orion_code")
    drop(plates, "r04_scale")
    drop(plates, "r04_dip")
    shells = drop(plates, "r04_shells")
    merge_to(
        r03,
        shells,
        "r03_r04_promise",
        "orion_scale_dip_shells",
        "One graphic beat (J0330). The row 3 Orion preview and the row 4 scale, dip and shells "
        "are one code render. A Betelgeuse surface still follows, before the row 5 scale.",
    )

    r10 = find(plates, "r10_dip")
    r11 = drop(plates, "r11_dip")
    merge_to(
        r10,
        r11,
        "r10_r11_dip",
        "dip",
        "One graphic beat (J0330). Row 10's dip and row 11's dip are one code render, not two.",
    )

    r17 = find(plates, "r17_shells")
    drop(plates, "r18_shells")
    drop(plates, "r19_shells")
    r20 = drop(plates, "r20_shells")
    merge_to(
        r17,
        r20,
        "r17_r20_shells",
        "shells",
        "One graphic beat (J0330). Rows 17–20 shells are the one shells render, not four. "
        "An HMI limb still sits before it. The Crab still follows.",
    )

    r31 = find(plates, "r31_shells")
    twins = drop(plates, "r31_twins")
    merge_to(
        r31,
        twins,
        "r31_shells_twins",
        "shells_twins",
        "One graphic beat (J0330). Row 31 shells and twins are one code render. "
        "A night clip sits before it. The December SPHERE still follows.",
    )

    # --- Ruling 2: real Betelgeuse surface. eso1726a stays rejected. ---
    surface_line = (
        "eso2109a. The page title is Betelgeuse's surface before and during its 2019–2020 Great Dimming. "
        "Not eso1726a (that page is Antares and stays rejected). Not the annotated eso2109b."
    )
    surface_ref = "https://cdn.eso.org/images/large/eso2109a.jpg"
    as_harvest(
        find(plates, "r02_surface"),
        "betelgeuse_surface",
        "First framing. " + surface_line,
        "ESO/M. Montargès et al.",
        ESO_LICENCE,
        surface_ref,
    )
    as_harvest(
        find(plates, "r05_surface"),
        "betelgeuse_surface",
        "Second framing, a wider crop. Still cap: this is the second use. " + surface_line,
        "ESO/M. Montargès et al.",
        ESO_LICENCE,
        surface_ref,
    )

    # --- Ruling 7: visible-light HMI. Row 17 is a limb crop, not the full disk. ---
    hmi = "https://sdo.gsfc.nasa.gov/assets/img/browse/2024/06/01/20240601_000000_4096_HMIIF.jpg"
    hmi_credit = "NASA/SDO (public domain)"
    as_harvest(
        find(plates, "r07_sdo"),
        "sdo_hmi_continuum",
        "Visible-light HMI continuum, 2024-06-01 00:00 UTC. Not AIA 335. "
        "Crop the bottom-left 'SDO/HMI Quick-Look Continuum' stamp. Full disk.",
        hmi_credit,
        "public domain",
        hmi,
    )
    as_harvest(
        find(plates, "r17_sdo"),
        "sdo_hmi_continuum",
        "Second framing: a limb crop of the same HMI continuum, not the full disk and not AIA 335. "
        "Still cap: this is the second use. Crop the quick-look stamp.",
        hmi_credit,
        "public domain",
        hmi,
    )

    # --- Ruling 3: no ICRR. IceCube gallery did not state a monetised-use licence. Night sky. ---
    chaj = "https://cdn.eso.org/videos/medium_podcast/chajnantormilkyway.m4v"
    chaj_credit = "ESO"
    chaj_line = (
        "Night-sky fallback. IceCube's gallery (icecube.wisc.edu/gallery/, 16 Oct 2026) does not state "
        "a licence that clears a monetised YouTube use, so no IceCube file is boarded. "
        "No ICRR / Super-Kamiokande. Milky Way over Chajnantor, 16 s. Do not replay frames."
    )
    as_harvest(
        find(plates, "r24_superk"),
        "chajnantor_mw",
        "First window, source 0.00–5.70 s. " + chaj_line,
        chaj_credit,
        ESO_LICENCE,
        chaj,
        0.0,
        5.70,
    )
    as_harvest(
        find(plates, "r24_superk_2"),
        "chajnantor_mw",
        "Second window, source 6.00–12.10 s. Not the first window. " + chaj_line,
        chaj_credit,
        ESO_LICENCE,
        chaj,
        6.00,
        12.10,
    )

    # --- Ruling 5: real PD/CC files, or £0 code where no file was pinned. ---
    # La Silla star trails, 28 s, five stretches, non-overlapping windows.
    # No unused Paranal/Orion clip was found; this is the spare ESO night film, and it is named as La Silla.
    lasilla = "https://cdn.eso.org/videos/hd_1080p25_screen/lasilla_timelapse_rw1.mp4"
    lasilla_credit = "R. Wesson/ESO"
    lasilla_why = (
        "Spare ESO night clip: Time-lapse over La Silla, 28 s, CC BY 4.0. "
        "Not a Paranal or VLT page, and the page does not name Orion. "
        "bt-paranal-orion135mm is already fully used at rows 2 and 36. Five stretches, no replayed frames."
    )

    def lasilla_plate(pid: str, a: float, b: float, nth: str) -> None:
        p = find(plates, pid)
        # Keep the shot-list out-point unless the window is shorter than the beat.
        window = round(b - a, 2)
        if window + 0.05 < p["use_s"]:
            p["t_out_s"] = round(p["t_in_s"] + window, 2)
            p["use_s"] = window
        as_harvest(
            p,
            "lasilla_startrails",
            f"{nth} window, source {a:.2f}–{b:.2f} s. {lasilla_why}",
            lasilla_credit,
            ESO_LICENCE,
            lasilla,
            a,
            b,
        )

    lasilla_plate("r06_paranal", 0.00, 5.54, "First")
    lasilla_plate("r10_span_c", 6.00, 9.12, "Second")
    lasilla_plate("r15_span_d", 10.00, 14.76, "Third")
    lasilla_plate("r16_span_e", 15.20, 20.42, "Fourth")
    lasilla_plate("r30_vlt", 20.80, 28.00, "Fifth")

    # Spans F and G have no sixth clip under the cap. One code beat, between harvest plates.
    span_f = find(plates, "r29_span_f")
    astro = drop(plates, "r29_astrolabe")
    span_g = drop(plates, "r30_span_g")
    span_f["t_out_s"] = span_g["t_out_s"]
    span_f["use_s"] = round(span_f["t_out_s"] - span_f["t_in_s"], 2)
    span_f["id"] = "r29_span_astrolabe"
    as_code(
        span_f,
        "orion_astrolabe",
        "One graphic beat (J0330). Spans F and G and the astrolabe. "
        "The Met collection API returned HTTP 410, and the Commons astrolabe checked "
        "(Deutsches Museum Habermel) is CC BY-SA 4.0, not PD or CC BY, so it is not used. "
        "No sixth ESO night clip under the five-stretch cap. Codex draws the span and a plain astrolabe. £0.",
    )

    as_code(
        find(plates, "r23_paranal"),
        "night_hold",
        "£0 code graphic. No spare Paranal-named clip: the 9 s Orion-over-Paranal film is already "
        "used at rows 2 and 36, and the La Silla trails are at their five-stretch cap. "
        "Holds the 'imagine the night' beat. Not a mint.",
    )
    as_code(
        find(plates, "r35_song"),
        "song_object",
        "£0 code graphic. Met API returned HTTP 410. No PD or CC BY Northern Song scan was pinned. "
        "A plain object card, not a claim that it is the 1054 record. Not a mint.",
    )
    as_code(
        find(plates, "r21_hero"),
        "teaspoon_mountain",
        "£0 code graphic for the teaspoon-and-a-mountain line. "
        "The 007 hero plate was not pinned as a file this run, so it is not boarded as a reuse. Not a mint.",
    )

    # DSCOVR EPIC, not Suomi PIA18033. Two crops, the still cap.
    epic = "https://images-assets.nasa.gov/image/GSFC_20171208_Archive_e000678/GSFC_20171208_Archive_e000678~orig.jpg"
    epic_line = (
        "NASA DSCOVR EPIC, first sunlit full-Earth frame, 20 July 2015 "
        "(GSFC_20171208_Archive_e000678). Not Suomi NPP PIA18033. Public domain."
    )
    as_harvest(
        find(plates, "r24_epic"),
        "dscovr_epic",
        "First framing, full disk. " + epic_line,
        "NASA/DSCOVR EPIC",
        "public domain",
        epic,
    )
    as_harvest(
        find(plates, "r28_epic"),
        "dscovr_epic",
        "Second framing, a tighter crop. Still cap: this is the second use. " + epic_line,
        "NASA/DSCOVR EPIC",
        "public domain",
        epic,
    )

    moon = "https://images-assets.nasa.gov/image/GSFC_20171208_Archive_e001863/GSFC_20171208_Archive_e001863~orig.jpg"
    as_harvest(
        find(plates, "r26_moon"),
        "half_moon",
        "NASA/GSFC first-quarter Moon, 15 June 2011 (GSFC_20171208_Archive_e001863). "
        "Public domain. One use. SVS 4874 is the phase film; this still is the half-phase frame.",
        "NASA/GSFC",
        "public domain",
        moon,
    )

    as_harvest(
        find(plates, "r21_neutron"),
        "neutron_wind",
        "NASA Goddard, use restrictions none (GSFC_20171208_Archive_e000279): "
        "the first wind nebula around a magnetar. Public domain. "
        "The orig file is 37 KB; confirm it is sharp enough at harvest, and that it is not a labelled chart.",
        "NASA Goddard",
        "public domain",
        "https://images-assets.nasa.gov/image/GSFC_20171208_Archive_e000279/GSFC_20171208_Archive_e000279~orig.jpg",
    )
    as_harvest(
        find(plates, "r21_bh"),
        "neutron_bh",
        "NASA Goddard (GSFC_20171208_Archive_e001102): Neutron Stars Rip Each Other Apart to Form a Black Hole. "
        "Public domain. Confirm at harvest that it is not a labelled chart. One use.",
        "NASA Goddard",
        "public domain",
        "https://images-assets.nasa.gov/image/GSFC_20171208_Archive_e001102/GSFC_20171208_Archive_e001102~orig.jpg",
    )

    as_harvest(
        find(plates, "r37_casa"),
        "casa",
        "Cassiopeia A, NASA/CXC/STScI/JPL-Caltech composite PIA03519. Public domain. "
        "Not a Hubble Pillars stand-in. One use. Say it is a multi-observatory composite.",
        "NASA/CXC/STScI/JPL-Caltech",
        "public domain",
        "https://images-assets.nasa.gov/image/PIA03519/PIA03519~orig.jpg",
    )
    as_harvest(
        find(plates, "r37_pillars"),
        "jwst_pillars",
        "JWST Pillars of Creation, ESA/Webb weic2216a (cropped). "
        "ESA/Webb copyright page re-read 16 Oct 2026: CC BY 4.0. Not Hubble heic1501a.",
        "NASA, ESA, CSA, STScI",
        "CC BY 4.0",
        "https://cdn.esawebb.org/archives/images/large/weic2216a.jpg",
    )

    as_harvest(
        find(plates, "r34_gemini"),
        "gemini_night",
        "Gemini North at night. NOIRLab iotw2227a, type Photographic, not a chart. " + NOIRLAB_NOTE,
        "International Gemini Observatory/NOIRLab/NSF/AURA/P. Horálek",
        NOIRLAB_LICENCE,
        "https://noirlab.edu/public/media/archives/images/large/iotw2227a.jpg",
    )
    as_harvest(
        find(plates, "r34_dome"),
        "gemini_dome",
        "Gemini North with the telescope, iotw2008a (laser tests). Type Photographic. "
        "The lasers are in this row 34 plate. Row 30 is the one that asked for no lasers, and it does not use this file. "
        + NOIRLAB_NOTE,
        "International Gemini Observatory/NOIRLab/NSF/AURA/J. Chu/J. Pollard",
        NOIRLAB_LICENCE,
        "https://noirlab.edu/public/media/archives/images/large/iotw2008a.jpg",
    )
    as_harvest(
        find(plates, "r28_people"),
        "gemini_earth_sky",
        "NOIRLab iotw2315a, type Photographic, title Caught Between Earth and Sky, Gemini North. "
        "The page does not say a person is in the frame. It is the night photograph gathered for this beat, not a chart. "
        + NOIRLAB_NOTE,
        "International Gemini Observatory/NOIRLab/NSF/AURA/T. Slovinský",
        NOIRLAB_LICENCE,
        "https://noirlab.edu/public/media/archives/images/large/iotw2315a.jpg",
    )

    # Milky Way lapse, then the end return from a later window of the same 17 s film.
    brunier = "https://cdn.eso.org/videos/hd_1080p25_screen/brunier_la_silla.mp4"
    as_harvest(
        find(plates, "r28_mw"),
        "lasilla_mw",
        "La Silla Milky Way time-lapse, 17 s. Source window 0.00–4.90 s. "
        "ESO/S. Brunier, CC BY 4.0. Not replayed at the return.",
        "ESO/S. Brunier",
        ESO_LICENCE,
        brunier,
        0.00,
        4.90,
    )

    # --- Ruling 6: do not replay the 6 s Orion rise. A later window of the 17 s lapse covers the hold. ---
    ret = find(plates, "r39_return")
    as_harvest(
        ret,
        "lasilla_mw",
        "End hold. The 6 s vlttimelapseorion clip is used only at row 1 (5.62 s of 6 s), so a second stretch "
        "would replay frames and still cannot cover 508.50–517.26. "
        "This is a later window of the 17 s La Silla Milky Way lapse, source 5.50–14.26 s, which does cover the "
        "hold past the last word. Not a third stretch of the Orion rise. Not a Paranal page. "
        "Two stretches of this film (row 28, then this). No replayed frames.",
        "ESO/S. Brunier",
        ESO_LICENCE,
        brunier,
        5.50,
        14.26,
    )
    r01 = find(plates, "r01_orion_rise")
    r01["line"] = (
        "Frame 0. Stars already moving. Span A, the 6 s Orion rise. "
        "This clip is not used again. The return is a different, longer film."
    )

    # --- Ruling 4 and 9: 2523b Collage, 2523c companion-only, licence on each NOIRLab plate. ---
    speckle = find(plates, "r33_speckle")
    speckle["licence"] = NOIRLAB_LICENCE
    speckle["line"] = (
        "Companion alone: noirlab2523c, the non-annotated speckle. Not noirlab2523a. " + NOIRLAB_NOTE
    )
    for pid in ("r33_pair", "r34_pair"):
        pair = find(plates, pid)
        pair["licence"] = NOIRLAB_LICENCE
        pair["line"] = (
            "Orion-context beat: noirlab2523b. NOIRLab type is Collage, not Chart "
            "(the annotated Chart is noirlab2523a, rejected). " + NOIRLAB_NOTE
        )

    # --- Ruling 1: price Omni. It fits. Not authorised. ---
    usable = round(VERTEX_PROMO - VERTEX_MARGIN, 2)
    omni_note = (
        f"List price gemini-omni-flash-preview, 720p with audio, {OMNI_S} s: "
        f"${OMNI_USD_PER_S:.2f}/s output + two image inputs (2,040 tokens each) + ~{OMNI_TEXT_TOKENS} text tokens "
        f"at $1.50/1M = ${OMNI_USD:.3f} = £{OMNI_GBP:.2f} at £{GBP_PER_USD:.2f}/$. "
        f"Vertex promo £{VERTEX_PROMO:.2f} at {VERTEX_READ_AT}. Not authorised to mint."
    )
    for pid in ("r12_orbit_thumb", "r26_orbit_flare"):
        p = find(plates, pid)
        zero(p)
        p["route"] = "omni"
        p["generation_authorized"] = False
        p["vertex_model"] = "gemini-omni-flash-preview"
        p["vertex_clip_s"] = OMNI_S
        p["vertex_try1_gbp"] = OMNI_GBP
        p["vertex_expected_gbp"] = OMNI_GBP
        p["vertex_note"] = omni_note
        p["line"] = (
            "Orbit only. No planet in the start frame. One take. Priced, not authorised. "
            + p.get("line", "")
        )

    # Every plate: no mint.
    for p in plates:
        p["generation_authorized"] = False
        if p["route"] != "omni":
            p["vertex_try1_gbp"] = 0.0
            p["vertex_expected_gbp"] = 0.0
            p["flow_credits_try1"] = 0
            p["flow_credits_expected"] = 0

    # Adjacency and caps.
    footage = {
        "orion_rise_vlt",
        "orion_over_paranal",
        "alma_orion_set",
        "lasilla_startrails",
        "chajnantor_mw",
        "lasilla_mw",
    }
    uses: Counter[str] = Counter()
    prev = None
    for p in plates:
        if prev and prev["route"] == "code" and p["route"] == "code":
            raise SystemExit(f"code stack: {prev['id']} then {p['id']}")
        if p["route"] == "harvest":
            uses[p["asset_id"]] += 1
        if p.get("asset_id") == "antares_vlti" and p["route"] != "reject":
            raise SystemExit("Antares boarded")
        if "eso1726a" in (p.get("reference") or "") and p["route"] == "harvest":
            raise SystemExit("eso1726a still referenced on a harvest plate")
        prev = p
    for asset, n in uses.items():
        cap = 5 if asset in footage else 2
        if n > cap:
            raise SystemExit(f"{asset} used {n}, cap {cap}")

    # Windows of one film must not overlap.
    windows: dict[str, list[tuple[float, float, str]]] = {}
    for p in plates:
        if "source_in_s" in p:
            windows.setdefault(p["asset_id"], []).append(
                (p["source_in_s"], p["source_out_s"], p["id"])
            )
    for asset, rows in windows.items():
        rows.sort()
        for (a1, b1, i1), (a2, b2, i2) in zip(rows, rows[1:]):
            if a2 < b1 - 0.01:
                raise SystemExit(f"replay {asset}: {i1} {a1}-{b1} overlaps {i2} {a2}-{b2}")

    def nroute(name: str) -> int:
        return sum(1 for p in plates if p["route"] == name)

    omni_gbp = round(2 * OMNI_GBP, 2)
    late_room = omni_gbp
    omni_fits = (omni_gbp + late_room) <= usable
    if not omni_fits:
        raise SystemExit("Omni does not fit; the KEEP fallback should have been applied")

    hos = sum(HOS_EXPECTED.values())
    after_hos = FLOW_LEFT - hos
    after_028 = after_hos - OWB_028_FLOW
    flow_exp = 0

    boards["version"] = "v02"
    boards["job"] = "J0330"
    boards["status"] = "parked for Chief: price pass on v02"
    boards["built"] = "2026-10-16"
    boards["mint"] = False
    boards["readings"] = {
        "flow_credits_left": FLOW_LEFT,
        "flow_read_at": FLOW_READ_AT,
        "vertex_promo_gbp": VERTEX_PROMO,
        "vertex_read_at": VERTEX_READ_AT,
        "vertex_margin_gbp": VERTEX_MARGIN,
        "vertex_usable_gbp": usable,
        "note": (
            "Fresh read this run, ai_spend_daily.py --dry-run. "
            "No Flow or Vertex spend is logged after it because nothing was minted."
        ),
    }
    boards["rates"]["omni"] = {
        "model": "gemini-omni-flash-preview",
        "usd_per_s_720p_with_audio": OMNI_USD_PER_S,
        "clip_s": OMNI_S,
        "gbp_per_take": OMNI_GBP,
        "late_billing_room": "one extra pair of takes",
        "authorised": False,
    }
    boards["totals"] = {
        "plates": len(plates),
        "shot_list_rows": 39,
        "quality": nroute("quality") if False else 0,
        "fast": 0,
        "omni": nroute("omni"),
        "code": nroute("code"),
        "card": nroute("card"),
        "harvest_ok": nroute("harvest"),
        "hold": nroute("hold"),
        "gap": nroute("gap"),
        "blocked": 0,
        "flow_credits_try1": 0,
        "flow_credits_expected": flow_exp,
        "vertex_try1_gbp": 0.0,
        "vertex_expected_gbp": 0.0,
        "omni_gbp": omni_gbp,
        "omni_late_room_gbp": late_room,
    }
    boards["fits_now"] = {
        "flow": True,
        "vertex_veo": True,
        "vertex_omni": omni_fits,
        "flow_headroom_after_028": after_028,
        "note": (
            "Flow expected stays 0. No gap was moved to Flow. "
            f"J0337 table: 23,740 - (007 {HOS_EXPECTED['007']} + 008 {HOS_EXPECTED['008']} + "
            f"009 t1 {HOS_EXPECTED['009']} = {hos}) = {after_hos} before 028; "
            f"after 028's {OWB_028_FLOW} = {after_028}, which is under the 3,000 floor. "
            "029 does not spend that remainder."
        ),
    }
    stretches: dict[str, list[str]] = {}
    for p in plates:
        if p["route"] == "harvest":
            stretches.setdefault(p["asset_id"], []).append(p["id"])
    boards["harvest_stretches"] = stretches
    boards["rulings"] = "J0311 comment 6202235397, applied as v02. No mint. No spend. No merge."

    # Pool: keep v01, mark Antares rejected, add what v02 uses.
    by_id = {a["id"]: a for a in pool["assets"]}
    by_id["antares_vlti"]["status"] = "reject"
    by_id["superk"]["status"] = "reject"
    by_id["superk"]["note"] = "No ICRR file. Monetised-use term not cleared. Not used in v02."
    by_id["sdo_aia335"]["status"] = "unused"
    by_id["sdo_aia335"]["note"] = (
        "Not used in v02. Visible-light HMI replaced it. "
        "AIA 335 only if HMI cannot be harvested, and then the corner credit must say ultraviolet."
    )
    new_assets = [
        {
            "id": "betelgeuse_surface",
            "title": "Betelgeuse's surface before and during its 2019–2020 Great Dimming",
            "credit": "ESO/M. Montargès et al.",
            "licence": ESO_LICENCE,
            "page": "https://www.eso.org/public/images/eso2109a/",
            "file": surface_ref,
            "status": "ok",
            "note": "Page title names Betelgeuse. HEAD 200, 92 KB large jpeg. Not eso1726a. Not the annotated eso2109b. Two framings.",
        },
        {
            "id": "sdo_hmi_continuum",
            "title": "SDO/HMI continuum intensitygram, 2024-06-01 00:00 UTC",
            "credit": hmi_credit,
            "licence": "public domain",
            "page": "https://sdo.gsfc.nasa.gov/assets/img/browse/2024/06/01/",
            "file": hmi,
            "status": "ok",
            "note": "HEAD 200, 4.6 MB. Same file 028 boarded. Crop the quick-look stamp. Full disk then a limb crop.",
        },
        {
            "id": "chajnantor_mw",
            "title": "Milky Way over Chajnantor",
            "credit": "ESO",
            "licence": ESO_LICENCE,
            "page": "https://www.eso.org/public/videos/chajnantormilkyway/",
            "file": chaj,
            "status": "ok",
            "note": "16 s. Two windows for the row 24 night-sky fallback. Medium podcast file, HEAD 200.",
        },
        {
            "id": "lasilla_startrails",
            "title": "Time-lapse over La Silla",
            "credit": lasilla_credit,
            "licence": ESO_LICENCE,
            "page": "https://www.eso.org/public/videos/lasilla_timelapse_rw1/",
            "file": lasilla,
            "status": "ok",
            "note": "28 s, 30 fps. Five non-overlapping windows. Not Paranal. HEAD 200 on the 1080p file.",
        },
        {
            "id": "lasilla_mw",
            "title": "La Silla Milky Way time-lapse",
            "credit": "ESO/S. Brunier",
            "licence": ESO_LICENCE,
            "page": "https://www.eso.org/public/videos/brunier_la_silla/",
            "file": brunier,
            "status": "ok",
            "note": "17 s. Window 0–4.90 s is the Milky Way beat. Window 5.50–14.26 s is the end return. HEAD 200.",
        },
        {
            "id": "dscovr_epic",
            "title": "NASA Captures EPIC Earth Image",
            "credit": "NASA/DSCOVR EPIC",
            "licence": "public domain",
            "page": "https://images.nasa.gov/details/GSFC_20171208_Archive_e000678",
            "file": epic,
            "status": "ok",
            "note": "DSCOVR EPIC, 20 July 2015. Not PIA18033. HEAD 200. Two crops.",
        },
        {
            "id": "half_moon",
            "title": "First Quarter Moon",
            "credit": "NASA/GSFC",
            "licence": "public domain",
            "page": "https://images.nasa.gov/details/GSFC_20171208_Archive_e001863",
            "file": moon,
            "status": "ok",
            "note": "First-quarter Moon, 15 June 2011. HEAD 200. One use.",
        },
        {
            "id": "neutron_wind",
            "title": "First wind nebula around a magnetar",
            "credit": "NASA Goddard",
            "licence": "public domain",
            "page": "https://images.nasa.gov/details/GSFC_20171208_Archive_e000279",
            "file": "https://images-assets.nasa.gov/image/GSFC_20171208_Archive_e000279/GSFC_20171208_Archive_e000279~orig.jpg",
            "status": "ok",
            "note": "Use restrictions none. Orig is 37 KB. Confirm sharpness and that it is not a labelled chart.",
        },
        {
            "id": "neutron_bh",
            "title": "Neutron Stars Rip Each Other Apart to Form Black Hole",
            "credit": "NASA Goddard",
            "licence": "public domain",
            "page": "https://images.nasa.gov/details/GSFC_20171208_Archive_e001102",
            "file": "https://images-assets.nasa.gov/image/GSFC_20171208_Archive_e001102/GSFC_20171208_Archive_e001102~orig.jpg",
            "status": "ok",
            "note": "HEAD 200, 452 KB. Confirm it is not a labelled chart before the cut.",
        },
        {
            "id": "casa",
            "title": "Cassiopeia A: Death Becomes Her",
            "credit": "NASA/CXC/STScI/JPL-Caltech",
            "licence": "public domain",
            "page": "https://images.nasa.gov/details/PIA03519",
            "file": "https://images-assets.nasa.gov/image/PIA03519/PIA03519~orig.jpg",
            "status": "ok",
            "note": "Multi-observatory composite. HEAD 200. Say so on screen.",
        },
        {
            "id": "jwst_pillars",
            "title": "Webb Takes a Stunning, Star-Filled Portrait of the Pillars of Creation (Cropped)",
            "credit": "NASA, ESA, CSA, STScI",
            "licence": "CC BY 4.0",
            "page": "https://esawebb.org/images/weic2216a/",
            "file": "https://cdn.esawebb.org/archives/images/large/weic2216a.jpg",
            "status": "ok",
            "note": "JWST, not Hubble heic1501a. ESA/Webb usage page says CC BY 4.0. HEAD 200.",
        },
        {
            "id": "gemini_night",
            "title": "A Bright Night over Gemini North",
            "credit": "International Gemini Observatory/NOIRLab/NSF/AURA/P. Horálek",
            "licence": NOIRLAB_LICENCE,
            "page": "https://noirlab.edu/public/images/iotw2227a/",
            "file": "https://noirlab.edu/public/media/archives/images/large/iotw2227a.jpg",
            "status": "ok",
            "note": "Type Photographic. HEAD 200 on the large JPEG.",
        },
        {
            "id": "gemini_dome",
            "title": "Circumpolar Laser Tests at Gemini North",
            "credit": "International Gemini Observatory/NOIRLab/NSF/AURA/J. Chu/J. Pollard",
            "licence": NOIRLAB_LICENCE,
            "page": "https://noirlab.edu/public/images/iotw2008a/",
            "file": "https://noirlab.edu/public/media/archives/images/large/iotw2008a.jpg",
            "status": "ok",
            "note": "Type Photographic. Lasers are in the frame. Not used on the row 30 VLT beat.",
        },
        {
            "id": "gemini_earth_sky",
            "title": "Caught Between Earth and Sky",
            "credit": "International Gemini Observatory/NOIRLab/NSF/AURA/T. Slovinský",
            "licence": NOIRLAB_LICENCE,
            "page": "https://noirlab.edu/public/images/iotw2315a/",
            "file": "https://noirlab.edu/public/media/archives/images/large/iotw2315a.jpg",
            "status": "ok",
            "note": "Type Photographic, Gemini North. Page does not say a person is in frame.",
        },
    ]
    for a in new_assets:
        by_id[a["id"]] = a
    # Gaps that v02 closed.
    for gid in (
        "orion_span_c",
        "orion_span_d",
        "orion_span_e",
        "orion_span_f",
        "orion_span_g",
        "paranal_other",
        "vlt_night",
        "mw_lapse",
        "people_night",
        "epic",
        "half_moon",
        "neutron",
        "hero_007",
        "black_hole",
        "casa",
        "jwst_pillars",
        "gemini_night",
        "gemini_dome",
        "met_astrolabe",
        "met_song",
        "icecube",
    ):
        if gid in by_id and by_id[gid].get("status") == "gap":
            by_id[gid]["status"] = "filled_in_v02"
            by_id[gid]["note"] = (by_id[gid].get("note") or "") + " Filled or replaced in v02."
    pool["version"] = "v02"
    pool["job"] = "J0330"
    pool["checked"] = "2026-10-16"
    pool["rule"] = ESO_NOTE + " " + NOIRLAB_NOTE + " NASA public domain."
    pool["assets"] = list(by_id.values())

    (EDIT / "PLATE_BOARDS_v02.json").write_text(json.dumps(boards, indent=2) + "\n")
    (EDIT / "SOURCE_POOL_v02.json").write_text(json.dumps(pool, indent=2) + "\n")

    t = boards["totals"]
    review = f"""# 029 price review v02

Cursor, 16 Oct 2026, J0330. Applies Chief's price PASS with conditions on PR #223 (comment 6202235397). **No mint. No spend. No merge.**

Locked VO and shot list are unchanged. This table only replaces plates and prices.

## Readings (this run)

- Flow: **{FLOW_LEFT}** credits at {FLOW_READ_AT}. `ai_spend_daily.py --dry-run`.
- Vertex promo: **£{VERTEX_PROMO:.2f}** at {VERTEX_READ_AT}. Usable **£{usable:.2f}** after the £1 margin. Free Trial is £0.

## The nine rulings

1. **Omni ×2** priced at list, **£{OMNI_GBP:.2f}** a take, **£{omni_gbp:.2f}** for the pair, plus **£{late_room:.2f}** late-billing room. £{omni_gbp + late_room:.2f} fits inside £{usable:.2f}. They stay Omni. Not authorised. No KEEP-pose fallback.
2. **eso1726a stays rejected.** Rows 2 and 5 use eso2109a. The page title names Betelgeuse's surface. Two framings, the still cap.
3. **Super-K** is not used. The IceCube gallery does not state a monetised-use licence, so row 24 is two windows of the Chajnantor Milky Way film. No mint.
4. **noirlab2523b** stays on the Orion-context beats, recorded as Collage not Chart. **noirlab2523c** stays on the companion-only beat. 2523a and 2523f stay rejected.
5. **Gaps.** EPIC is DSCOVR `e000678`, not Suomi. JWST Pillars are weic2216a, not Hubble. Cas A is PIA03519. Neutron and black-hole plates are NASA Goddard stills (confirm they are not labelled charts at harvest; the neutron orig is 37 KB). The half Moon is a NASA first-quarter still. Gemini night, dome and the earth-and-sky photograph are NOIRLab photographs. Spans C–E, row 6 and row 30 are five windows of the La Silla star-trail film (28 s). That page is not Paranal and does not name Orion. Spans F–G and the astrolabe are one £0 code beat: the Met API is 410, and the Commons astrolabe found is CC BY-SA, so it was not used. Row 23 and the Song object are £0 code for the same reason. The 007 hero file was not pinned.
6. **Return.** `vlttimelapseorion` is row 1 only. The hold uses a later window of the 17 s La Silla Milky Way lapse (source 5.50–14.26 s), which covers 508.50–517.26. Not a third stretch of the 6 s rise.
7. **SDO** is the HMI continuum, full disk then a limb crop. AIA 335 is not used, so no ultraviolet credit.
8. **Stacks merged** into one beat each: rows 3–4; the row 10–11 dip; rows 17–20 shells; row 31 shells and twins. No two code beats sit together.
9. **Licences re-read.** ESO copyright page: CC BY 4.0. NOIRLab copyright page: CC BY 4.0, written on every NOIRLab plate. ESA/Webb: CC BY 4.0 on the Pillars.

## Totals

| plates | Quality | Fast | Omni | code | harvest | card | hold | gap | Flow expected | Omni £ |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| {t['plates']} | 0 | 0 | {t['omni']} | {t['code']} | {t['harvest_ok']} | {t['card']} | {t['hold']} | {t['gap']} | {flow_exp} | {omni_gbp:.2f} |

Flow expected stays **0**. No gap was moved to Flow, so no new price pass is required for a Flow mint. Nothing is authorised to generate.

## Headroom

J0337's table, not a new sum of those films: 006 = 0, 007 = 7,553, 008 = 5,605, 009 tranche 1 = 7,354. Sum **{hos}**. Flow {FLOW_LEFT} leaves **{after_hos}** before 028. After 028's {OWB_028_FLOW}: **{after_028}**, which misses the 3,000 floor by {3000 - after_028}. 029 adds nothing to that. Mint order stays the Chief's call.

`generation_authorized` is false on every plate.

Files: `SOURCE_POOL_v02.json`, `PLATE_BOARDS_v02.json`. Rebuild with `python3 _build_plate_boards_v02.py`.
"""
    (EDIT / "PRICE_REVIEW_v02.md").write_text(review)
    print(
        f"plates={t['plates']} harvest={t['harvest_ok']} code={t['code']} "
        f"gap={t['gap']} hold={t['hold']} omni=£{omni_gbp:.2f} fits={omni_fits} "
        f"after_028={after_028}"
    )


if __name__ == "__main__":
    main()
