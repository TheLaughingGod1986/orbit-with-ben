#!/usr/bin/env python3
"""028 plate boards v02 from v01, applying Chief's J0310 rulings (comment 6199532687).

No mint. No spend. Rebuilds PLATE_BOARDS_v02.json, SOURCE_POOL_v02.json and
PRICE_REVIEW_v02.md next to this file.

  python3 _build_plate_boards_v02.py
"""
from __future__ import annotations

import json
from collections import OrderedDict
from pathlib import Path

EDIT = Path(__file__).resolve().parent
V01 = EDIT / "PLATE_BOARDS_v01.json"
POOL_V01 = EDIT / "SOURCE_POOL_v01.json"

# Fresh readings this run (ai_spend_daily.py --dry-run --pools flow,vertex), 22 Oct 2026 (J0850).
FLOW_LEFT = 20950
FLOW_READ_AT = "2026-10-22T16:56:01Z"
VERTEX_PROMO = 71.02
VERTEX_READ_AT = "2026-10-22T16:56:01Z"
VERTEX_MARGIN = 1.0
GBP_PER_USD = 0.8

# Gemini Omni Flash list price, cloud.google.com/vertex-ai/generative-ai/pricing
# (Gemini Omni Flash): video output $0.10 per second of 720p with audio
# (5,792 tokens/s at $17.50 per 1M). Image input 2,040 tokens at $1.50 per 1M.
OMNI_USD_PER_S = 0.10
OMNI_S = 8  # both Orbit rows are just under 8 s; the published rate is 720p
OMNI_IMAGE_TOKENS = 2040 * 2  # Orbit reference + start frame
OMNI_TEXT_TOKENS = 400
OMNI_USD = OMNI_S * OMNI_USD_PER_S + (OMNI_IMAGE_TOKENS + OMNI_TEXT_TOKENS) * 1.50 / 1_000_000
OMNI_GBP = round(OMNI_USD * GBP_PER_USD, 2)  # one take

# House takes-per-KEEP, same as v01.
Q_EXP = 259  # 100 * 2.59
F_EXP = 20  # round(10 * 1.96) — v01's 279 = 259 + 20

# Expected Flow still reserved for HOS films in this cycle, charged against
# today's live balance (J0850, 22 Oct 2026):
# - HOS 006: 0 (picture from existing KEEPs, full_join_v03_teach on main 130ade6f)
# - HOS 007: 0 remaining (all 73/73 Flow rows of boards v02 minted & KEEP in J0352
#   on 21 Oct for 2,890 cr actual vs 7,553/7,196 reserve, already drawn from the
#   live 20,950 balance; full_join_v01 assembled in J0827 786e631e)
# - HOS 008: 5,605 (PRICE_REVIEW_v03: 15 Quality + 86 Fast = 2,360 try-1 / 5,605 expected)
# - HOS 009: 7,354 (tranche 1 only, boards v04/v05: 26 Quality + 31 Fast = 2,910 try-1 / 7,354 expected)
HOS_EXPECTED = {
    "006": 0,  # picture from existing KEEPs; not a Flow mint
    "007": 0,  # all 73/73 Flow rows minted & KEEP (J0352, 2,890 cr already drawn)
    "008": 5605,  # PRICE_REVIEW_v03 (15 Quality + 86 Fast)
    "009": 7354,  # tranche 1 only, boards v04/v05 on HOS main
}
HOS_009_TRANCHE2 = 5180  # ~12 Nov AI Ultra renewal; not charged today


def zero(p: dict) -> None:
    p["flow_credits_try1"] = 0
    p["flow_credits_expected"] = 0
    p["vertex_try1_gbp"] = 0.0
    p["vertex_expected_gbp"] = 0.0
    p["generation_authorized"] = False
    p.pop("quality", None)
    p.pop("flow_model", None)
    p.pop("flow_clip_s", None)
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


def main() -> None:
    boards = json.loads(V01.read_text())
    pool = json.loads(POOL_V01.read_text())
    plates: list[dict] = boards["plates"]

    # --- Ruling 10: merge each named stack into one graphic beat ---
    # Row 4 shower+shell is one beat. A real still then sits before row 5,
    # because a merged row-4 beat against a merged row-5 beat would still be
    # two code graphics back to back.
    shell = drop(plates, "r04_shell_end")
    shower = find(plates, "r04_shower")
    shower["id"] = "r04_shower_shell"
    shower["t_out_s"] = shell["t_out_s"]
    shower["use_s"] = round(shower["t_out_s"] - shower["t_in_s"], 2)
    shower["asset_id"] = "shower_shell"
    shower["line"] = (
        "One graphic beat (J0321). Shower and shell render as one code graphic, "
        "not two. A cluster still follows, before the row 5 beat."
    )
    zero(shower)
    shower["route"] = "code"

    # Borrow the first 5 s of row 5 for a second framing of ngc3603.
    drift = find(plates, "r05_drift")
    sky = drop(plates, "r05_sky")
    path5 = drop(plates, "r05_path")
    break_end = round(drift["t_in_s"] + 5.0, 2)
    cluster = find(plates, "r37_cluster")
    breaker = {
        "id": "r05_cluster_break",
        "shot_list_row": 5,
        "chapter": drift["chapter"],
        "t_in_s": drift["t_in_s"],
        "t_out_s": break_end,
        "use_s": 5.0,
        "route": "harvest",
        "asset_id": "ngc3603",
        "asset_status": "ok",
        "line": (
            "Second framing of NGC 3603, between the row 4 and row 5 code beats. "
            "Not the r37 crop. Still cap: this is the second use."
        ),
        "credit": cluster.get("credit"),
        "licence": cluster.get("licence"),
        "reference": cluster.get("reference"),
        "prompt": None,
        "generation_authorized": False,
        "flow_credits_try1": 0,
        "flow_credits_expected": 0,
        "vertex_try1_gbp": 0.0,
        "vertex_expected_gbp": 0.0,
        "vertex_note": "£0 harvest",
    }
    # Insert the breaker where r05_drift sits, then shorten the merged beat.
    idx = plates.index(drift)
    plates.insert(idx, breaker)
    drift["id"] = "r05_drift_path_sky"
    drift["t_in_s"] = break_end
    drift["t_out_s"] = sky["t_out_s"]
    drift["use_s"] = round(drift["t_out_s"] - drift["t_in_s"], 2)
    drift["asset_id"] = "drift_path_sky"
    drift["line"] = (
        "One graphic beat (J0321). Drift, path and sky are one code graphic. "
        f"The dropped row-5 slices ran {path5['t_in_s']}–{sky['t_out_s']} s before the merge."
    )
    zero(drift)
    drift["route"] = "code"

    # Row 14: Hipparcos becomes a code card. Fold the following path into that
    # one beat so the card does not sit against r14_path.
    path14 = drop(plates, "r14_path")
    hip = find(plates, "r14_hipparcos")
    hip["id"] = "r14_hipparcos_card"
    hip["t_out_s"] = path14["t_out_s"]
    hip["use_s"] = round(hip["t_out_s"] - hip["t_in_s"], 2)
    hip["route"] = "code"
    hip["asset_id"] = "hipparcos_card"
    hip["asset_status"] = "code"
    hip["credit"] = None
    hip["licence"] = "£0 code graphic"
    hip["line"] = (
        "£0 Codex code graphic. The ESA illustration's own page says Copyright: ESA, "
        "with no CC or public-domain grant, so the file is not cleared. "
        "Row 14's path slice is inside this one beat, not a second render."
    )
    zero(hip)
    hip["route"] = "code"

    path16 = drop(plates, "r16_path")
    path15 = find(plates, "r15_path")
    # The merged path beat would otherwise run straight into r17's scale card.
    # Give the last 5 s of the path, plus the breath before the scale, to a real plate.
    path_out = round(path16["t_out_s"] - 5.0, 2)
    scale = find(plates, "r17_scale_a")
    sunrise = find(plates, "r24_sunrise")
    path_break = {
        "id": "r16_sunrise_break",
        "shot_list_row": 16,
        "chapter": path16["chapter"],
        "t_in_s": path_out,
        "t_out_s": scale["t_in_s"],
        "use_s": round(scale["t_in_s"] - path_out, 2),
        "route": "harvest",
        "asset_id": "iss_sunrise",
        "asset_status": "ok",
        "line": (
            "Second framing of the ISS sunrise, between the path beat and the scale card. "
            "Not the r24 crop. Still cap: this is the second use."
        ),
        "credit": sunrise.get("credit"),
        "licence": sunrise.get("licence"),
        "reference": sunrise.get("reference"),
        "prompt": None,
        "generation_authorized": False,
        "flow_credits_try1": 0,
        "flow_credits_expected": 0,
        "vertex_try1_gbp": 0.0,
        "vertex_expected_gbp": 0.0,
        "vertex_note": "£0 harvest",
    }
    path15["id"] = "r15_16_path"
    path15["shot_list_row"] = "15-16"
    path15["t_out_s"] = path_out
    path15["use_s"] = round(path15["t_out_s"] - path15["t_in_s"], 2)
    path15["line"] = (
        "One graphic beat across rows 15 and 16 (J0321). One path render. "
        "Gaia the spacecraft sits in front of it. An ISS sunrise still follows, before the scale card."
    )
    zero(path15)
    path15["route"] = "code"
    plates.insert(plates.index(scale), path_break)

    # Row 20 shell + row 21 Oort are one shell beat. The NASA Oort file is a labelled chart.
    oort = drop(plates, "r21_oort")
    shell20 = find(plates, "r20_shell")
    shell20["id"] = "r20_21_oort_shell"
    shell20["shot_list_row"] = "20-21"
    shell20["t_out_s"] = oort["t_out_s"]
    shell20["use_s"] = round(shell20["t_out_s"] - shell20["t_in_s"], 2)
    shell20["asset_id"] = "oort_shell"
    shell20["line"] = (
        "One graphic beat (J0321). Oort is the shell. The NASA Oort Cloud file is a "
        "labelled diagram (Kuiper Belt call-out, orbit caption) and does not go in. "
        "£0 Codex code graphic, text-light, the distance shown as an object."
    )
    zero(shell20)
    shell20["route"] = "code"

    shower25 = drop(plates, "r25_shower")
    shower24 = find(plates, "r24_shower")
    shower24["id"] = "r24_25_shower"
    shower24["shot_list_row"] = "24-25"
    shower24["t_out_s"] = shower25["t_out_s"]
    shower24["use_s"] = round(shower24["t_out_s"] - shower24["t_in_s"], 2)
    shower24["line"] = (
        "One graphic beat across rows 24 and 25 (J0321). Sunrise (harvest) sits in front of it."
    )
    zero(shower24)
    shower24["route"] = "code"

    # --- Ruling 3: drop the sixth Gliese-motion stretch. Fill the row with a new ESO plate. ---
    r35 = find(plates, "r35_gaia_wide")
    r35["id"] = "r35_lasilla_ntt"
    r35["route"] = "harvest"
    r35["asset_id"] = "eso_lasilla_ntt"
    r35["asset_status"] = "ok"
    r35["credit"] = "ESO/B. Tafreshi (twanight.org)"
    r35["licence"] = "ESO site policy CC BY 4.0; this video page states the credit and does not repeat the CC BY line"
    r35["line"] = (
        "Gliese-motion stretch dropped (five-stretch cap; r38 stays). "
        "Filled with the NTT time-lapse at La Silla, a different film from the dropped "
        "Tafreshi fulldome (bt_lasilla_fd2). 20 s source; use one window, do not loop."
    )
    r35["reference"] = "https://www.eso.org/public/videos/bt_lasilla2_ntt/"
    zero(r35)
    r35["route"] = "harvest"
    r35["vertex_note"] = "£0 harvest"

    # --- Ruling 7: Tafreshi fulldome out. Second stretch of the Brunier La Silla lapse. ---
    r36 = find(plates, "r36_night_2")
    r36["route"] = "harvest"
    r36["asset_id"] = "eso_mw_lasilla"
    r36["asset_status"] = "ok"
    r36["credit"] = "ESO/S. Brunier"
    r36["licence"] = "CC BY 4.0"
    r36["line"] = (
        "bt_lasilla_fd2 dropped (no file). Second stretch of the Brunier La Silla lapse. "
        "Source is 17 s and r06 already uses 7.32 s, so this 7.86 s window is the remainder. "
        "Do not replay r06's frames."
    )
    r36["reference"] = "https://www.eso.org/public/videos/brunier_la_silla/"
    zero(r36)
    r36["route"] = "harvest"
    r36["vertex_note"] = "£0 harvest"

    # --- Ruling 4: K dwarf code card ---
    kd = find(plates, "r07_kdwarf")
    kd["route"] = "code"
    kd["asset_id"] = "kdwarf_vs_sun"
    kd["asset_status"] = "code"
    kd["credit"] = None
    kd["licence"] = "£0 code graphic"
    kd["line"] = (
        "£0 Codex code graphic: K dwarf vs Sun, size and colour, text-light, "
        "the teaching number shown as an object. The labelled Hubble chart stays out."
    )
    zero(kd)
    kd["route"] = "code"

    # --- Ruling 5: visible-light HMI. Limb is a second crop. ---
    sun = find(plates, "r07_sun")
    sun["asset_id"] = "sdo_hmi_continuum"
    sun["asset_status"] = "ok"
    sun["credit"] = "NASA/SDO"
    sun["licence"] = "public domain (NASA media: images produced by NASA are not copyrighted)"
    sun["line"] = (
        "Visible-light HMI continuum, 2024-06-01 00:00 UTC. "
        "Crop the bottom-left 'SDO/HMI Quick-Look Continuum' stamp before the cut. It sits in the black corner, off the disk."
    )
    sun["reference"] = "https://sdo.gsfc.nasa.gov/assets/img/browse/2024/06/01/20240601_000000_4096_HMIIF.jpg"
    zero(sun)
    sun["route"] = "harvest"
    sun["vertex_note"] = "£0 harvest"

    limb = find(plates, "r30_sun_limb")
    limb["asset_id"] = "sdo_hmi_continuum"
    limb["asset_status"] = "ok"
    limb["route"] = "harvest"
    limb["credit"] = "NASA/SDO"
    limb["licence"] = sun["licence"]
    limb["reference"] = sun["reference"]
    limb["line"] = (
        "Second framing of the same HMI continuum: a limb crop, not the full disk, and not AIA 335. "
        "Still cap: this is the second use. Crop the quick-look stamp."
    )
    zero(limb)
    limb["route"] = "harvest"
    limb["vertex_note"] = "£0 harvest"

    # --- Ruling 6: Slawik out. One A3 reuse. The other hale row cannot take a third comet still. ---
    a3 = find(plates, "r26_a3")
    hale = find(plates, "r26_hale_bopp")
    hale["asset_id"] = "comet_a3"
    hale["asset_status"] = "ok"
    hale["route"] = "harvest"
    hale["credit"] = a3.get("credit")
    hale["licence"] = a3.get("licence")
    hale["reference"] = a3.get("reference")
    hale["line"] = (
        "Slawik image not cleared. Second framing of comet C/2023 A3 (the still cap). "
        "Not a second Hale-Bopp stretch."
    )
    zero(hale)
    hale["route"] = "harvest"
    hale["vertex_note"] = "£0 harvest"

    hale2 = find(plates, "r28_hale_bopp_2")
    hale2["route"] = "code"
    hale2["asset_id"] = "comet_tail"
    hale2["asset_status"] = "code"
    hale2["credit"] = None
    hale2["licence"] = "£0 code graphic"
    hale2["line"] = (
        "£0 Codex code graphic, one comet-tail idea. NEOWISE is already at two uses and "
        "A3 reaches two uses on r26, so a third comet still would break the cap. "
        "sts083-410-009 was not used: its images.nasa.gov record does not state public domain."
    )
    zero(hale2)
    hale2["route"] = "code"

    # --- Ruling 8: WISE has no labels. Colour notes. Gaia flag. ---
    wise = find(plates, "r32_wise_sky")
    wise["line"] = (
        "Checked 15 Oct 2026 on PIA15481~small.jpg (640×321): no axis labels and no readable text. Keep. "
        "It is still an all-sky map; picture_qa may flag the map. Do not add a labelled version."
    )
    nep = find(plates, "r17_neptune")
    nep["credit"] = "NASA/JPL, green and orange filters"
    nep["line"] = "On 'outermost planet'. Corner credit says green and orange filters, not true colour."
    jun = find(plates, "r28_jupiter")
    jun["credit"] = "NASA/JPL-Caltech/SwRI/MSSS, colour-enhanced"
    jun["line"] = "No impact imagery. Corner credit says colour-enhanced, not true colour."

    for p in plates:
        if p.get("asset_id") in ("gaia_motion_1_6my", "gaia_edr3_sky", "gaia_gliese_encounter"):
            p["picture_qa_flag"] = "Gaia data film; diagram on purpose (Chief, 15 Oct 2026)"

    # --- Ruling 1: Quality and Fast stay. Not authorised to mint. ---
    road = find(plates, "r11_night_road")
    road["quality"] = "Quality"
    road["line"] = (
        "Chief ruling: stays Quality. Headlights. Planned on Flow, not Vertex. Not authorised to mint."
    )
    road["generation_authorized"] = False
    road["flow_credits_try1"] = 100
    road["flow_credits_expected"] = Q_EXP

    pitch = find(plates, "r17_pitch")
    pitch["quality"] = "Fast"
    pitch["line"] = (
        "Chief ruling: stays Fast. Dusk, no glow. Planned on Flow, not Vertex. Not authorised to mint."
    )
    pitch["generation_authorized"] = False
    pitch["flow_credits_try1"] = 10
    pitch["flow_credits_expected"] = F_EXP

    # --- Ruling 2: price both Omni takes. They fit, so no KEEP fallback. ---
    omni_note = (
        f"List price gemini-omni-flash-preview, 720p with audio, {OMNI_S} s: "
        f"${OMNI_USD_PER_S:.2f}/s output + two image inputs (2,040 tokens each) + ~{OMNI_TEXT_TOKENS} text tokens "
        f"at $1.50/1M = ${OMNI_USD:.3f} = £{OMNI_GBP:.2f} at £{GBP_PER_USD:.2f}/$. "
        f"One take. Not authorised to mint. Promo £{VERTEX_PROMO:.2f}, margin £{VERTEX_MARGIN:.0f}, "
        f"usable £{VERTEX_PROMO - VERTEX_MARGIN:.2f}. Late-billing room held equal to both takes."
    )
    for pid in ("r08_orbit_binoculars", "r23_orbit_ice"):
        p = find(plates, pid)
        p["route"] = "omni"
        p["generation_authorized"] = False
        p["vertex_model"] = "gemini-omni-flash-preview"
        p["vertex_clip_s"] = OMNI_S
        p["vertex_try1_gbp"] = OMNI_GBP
        p["vertex_expected_gbp"] = OMNI_GBP
        p["vertex_note"] = omni_note
        p["flow_credits_try1"] = 0
        p["flow_credits_expected"] = 0
        p["line"] = (p.get("line") or "") + " Priced at list. Fits the promo. No KEEP fallback."

    # No plate is authorised.
    for p in plates:
        p["generation_authorized"] = False

    # Consecutive code graphics are a build error.
    prev = None
    for p in plates:
        if p["route"] == "code" and prev == "code":
            raise SystemExit(f"code graphic back to back at {p['id']}")
        prev = p["route"]

    def count_asset(aid: str) -> int:
        return sum(1 for p in plates if p.get("asset_id") == aid)

    if count_asset("gaia_motion_1_6my") != 5:
        raise SystemExit(f"gaia motion count {count_asset('gaia_motion_1_6my')}")
    if count_asset("comet_a3") != 2:
        raise SystemExit(f"comet_a3 count {count_asset('comet_a3')}")
    if count_asset("neowise_dc") != 2:
        raise SystemExit(f"neowise count {count_asset('neowise_dc')}")
    if count_asset("sdo_hmi_continuum") != 2:
        raise SystemExit("HMI should be used twice")
    if any(p.get("asset_id") == "hale_bopp" for p in plates):
        raise SystemExit("hale_bopp still on a plate")

    stretches: dict[str, list[str]] = OrderedDict()
    for p in plates:
        if p["route"] == "harvest":
            stretches.setdefault(p["asset_id"], []).append(p["id"])

    flow_try = sum(p.get("flow_credits_try1") or 0 for p in plates)
    flow_exp = sum(p.get("flow_credits_expected") or 0 for p in plates)
    vx_try = round(sum(p.get("vertex_try1_gbp") or 0 for p in plates), 2)
    vx_exp = round(sum(p.get("vertex_expected_gbp") or 0 for p in plates), 2)
    omni_gbp = round(2 * OMNI_GBP, 2)
    late_room = omni_gbp  # one retry of both takes, billed late
    usable = round(VERTEX_PROMO - VERTEX_MARGIN, 2)
    omni_fits = (omni_gbp + late_room) <= usable

    hos_sum = sum(HOS_EXPECTED.values())
    after_hos = FLOW_LEFT - hos_sum
    after_028 = after_hos - flow_exp
    after_028_first_try1 = FLOW_LEFT - flow_try
    after_028_first_exp = FLOW_LEFT - flow_exp
    headroom_ok = after_028 >= 3000
    misses_by = max(0, 3000 - after_028)
    surplus_over_3000 = after_028 - 3000
    if (hos_sum, after_hos, after_028, flow_exp, misses_by, surplus_over_3000) != (12959, 7991, 7712, 279, 0, 4712):
        raise SystemExit(
            f"headroom drift: sum={hos_sum} after_hos={after_hos} "
            f"after_028={after_028} flow_exp={flow_exp} misses_by={misses_by} surplus={surplus_over_3000}"
        )

    def nroute(name: str) -> int:
        return sum(1 for p in plates if p["route"] == name)

    boards["version"] = "v02"
    boards["job"] = "J0850"
    boards["mint"] = False
    boards["status"] = (
        "Chief PASS J0321; J0337 headroom corrected; J0850 live Flow re-price after HOS 007 (20,950 cr left, "
        "7,712 cr after HOS 008 + 009 tranche 1 + 028's 279 cr, clearing the 3,000 gate by +4,712 cr); "
        "no mint before Chief J0850 price PASS."
    )
    boards["built"] = "2026-10-22"
    boards["readings"] = {
        "flow_credits_left": FLOW_LEFT,
        "flow_read_at": FLOW_READ_AT,
        "vertex_promo_gbp": VERTEX_PROMO,
        "vertex_read_at": VERTEX_READ_AT,
        "vertex_margin_gbp": VERTEX_MARGIN,
        "vertex_usable_gbp": usable,
        "vertex_free_trial_gbp": 0.0,
        "note": (
            "Flow account picker, benoats@googlemail.com, CDP :9222 (after HOS 007 J0352 minted 73/73 rows for 2,890 cr). "
            "Vertex: Google Developer Program premium benefit CREDIT_TYPE_MONTHLY £71.02 Available; "
            "Free Trial £0.00 Used. No spend in J0850."
        ),
    }
    boards["rates"]["omni"] = {
        "model": "gemini-omni-flash-preview",
        "usd_per_s_720p_with_audio": OMNI_USD_PER_S,
        "clip_s": OMNI_S,
        "gbp_per_take": OMNI_GBP,
        "source": "https://cloud.google.com/vertex-ai/generative-ai/pricing",
    }
    boards["totals"] = {
        "plates": len(plates),
        "shot_list_rows": boards["totals"]["shot_list_rows"],
        "quality": nroute("flow") and sum(1 for p in plates if p.get("quality") == "Quality"),
        "fast": sum(1 for p in plates if p.get("quality") == "Fast"),
        "omni": nroute("omni"),
        "code": nroute("code"),
        "card": nroute("card"),
        "harvest_ok": sum(1 for p in plates if p["route"] == "harvest"),
        "hold": 0,
        "gap": 0,
        "blocked": 0,
        "flow_credits_try1": flow_try,
        "flow_credits_expected": flow_exp,
        "vertex_try1_gbp": vx_try,
        "vertex_expected_gbp": vx_exp,
        "omni_gbp": omni_gbp,
        "omni_late_room_gbp": late_room,
    }
    boards["fits_now"] = {
        "flow_two_veo_alone": flow_exp <= FLOW_LEFT,
        "flow_headroom_after_006_009": headroom_ok,
        "vertex_omni": omni_fits,
        "flow_left": FLOW_LEFT,
        "flow_after_028_only_try1": after_028_first_try1,
        "flow_after_028_only_expected": after_028_first_exp,
        "hos_006_009_expected": HOS_EXPECTED,
        "hos_006_009_sum": hos_sum,
        "hos_007_minted_actual": 2890,
        "hos_007_note": (
            "All 73/73 Flow rows of HOS 007 boards v02 minted & Chief KEEP in J0352 (21 Oct, 2,890 cr actual vs 7,553/7,196 reserve, "
            "already drawn from the live 20,950 balance); full_join_v01 assembled in J0827."
        ),
        "hos_009_tranche": 1,
        "hos_009_tranche_2_expected_not_in_sum": HOS_009_TRANCHE2,
        "hos_009_tranche_2_note": (
            "Waits for the ~12 Nov AI Ultra renewal. Not charged against today's balance."
        ),
        "after_hos_before_028": after_hos,
        "after_028": after_028,
        "headroom_required": 3000,
        "misses_3000_gate_by": misses_by,
        "surplus_over_3000_gate": surplus_over_3000,
        "mint_order": [
            "HOS 006 (0, done)",
            "HOS 007 (0 remaining; 2,890 cr minted & KEEP in J0352)",
            "HOS 008 (5,605 expected)",
            "HOS 009 tranche 1 (7,354 expected)",
            "OWB 028 two Veo plates (279 expected / 110 try-1)",
        ],
        "mint_rule": (
            "028 mints only when a live Flow read leaves >=3000 after it (now 7,712 left after HOS 008 + 009 tranche 1 + 028's 279, "
            "or 20,671 left if 028 mints first, leaving 7,712 after HOS 008 + 009 tranche 1). "
            "Parked for Chief's J0850 price pass before any mint."
        ),
    }
    boards["harvest_stretches"] = {k: v for k, v in stretches.items()}
    groups: OrderedDict[str, list[str]] = OrderedDict()
    for p in plates:
        groups.setdefault(p["chapter"], []).append(p["id"])
    boards["chapters"] = [{"chapter": k, "plates": v} for k, v in groups.items()]
    boards["plates"] = plates
    boards["rulings"] = "J0310 Chief price PASS with conditions, PR #218 comment 6199532687, applied by J0321."

    # Source pool.
    by_id = {a["id"]: a for a in pool["assets"]}
    by_id["sdo_aia335"]["status"] = "unused"
    by_id["sdo_aia335"]["note"] = (
        "Not used in v02. Visible-light HMI replaced it. Keep only if HMI cannot be harvested; "
        "then the corner credit must say ultraviolet."
    )
    by_id["k_dwarf_goldilocks"]["status"] = "reject"
    by_id["hale_bopp"]["status"] = "reject"
    by_id["hale_bopp"]["note"] = (
        "Rejected, Chief 15 Oct 2026. The 1997 page says © Eckhard Slawik. Do not use phot-mar14-hbs-2."
    )
    by_id["hipparcos_art"]["status"] = "not_cleared"
    by_id["hipparcos_art"]["file"] = (
        "https://sci.esa.int/documents/35127/35542/1567220191847-Hipparcos_spacecraft_illustration_625.jpg"
    )
    by_id["hipparcos_art"]["note"] = (
        "File HTTP 200. The page says Copyright: ESA, with no CC or public-domain grant. "
        "Not cleared. Row 14 is a £0 code graphic instead."
    )
    by_id["oort_page"]["status"] = "reject"
    by_id["oort_page"]["file"] = (
        "https://assets.science.nasa.gov/content/dam/science/psd/solar/2023/09/o/Oort_Cloud.jpg"
    )
    by_id["oort_page"]["note"] = (
        "File HTTP 200 and it is a labelled diagram (Kuiper Belt, orbit caption, Oort Cloud call-out). "
        "picture_qa FAIL. Row 21 is the £0 shell code graphic."
    )
    by_id["eso_night_tafreshi"]["status"] = "dropped"
    by_id["eso_night_tafreshi"]["note"] = (
        "Dropped, Chief 15 Oct 2026. Page 200, no file. Not replaced with another Tafreshi fulldome."
    )
    by_id["wise_sky"]["note"] = (
        "Checked 15 Oct 2026 on PIA15481~small.jpg: oval all-sky mosaic, no axis labels and no readable text. Keep."
    )
    by_id["neptune"]["note"] = "Green and orange filters, not true colour. Say so in the corner credit."
    by_id["jupiter_juno"]["note"] = "Juno, colour-enhanced, not true colour. Say so in the corner credit."
    for gid in ("gaia_motion_1_6my", "gaia_edr3_sky", "gaia_gliese_encounter"):
        by_id[gid]["picture_qa_flag"] = "data film; diagram on purpose"
    by_id["gaia_motion_1_6my"]["note"] = (
        "Data animation. picture_qa flag: diagram on purpose. Five stretches in v02 (r35 dropped): "
        + ", ".join(stretches["gaia_motion_1_6my"])
    )
    by_id["eso_mw_lasilla"]["note"] = (
        "Two stretches in v02: r06 and r36. Source 17 s. r06 uses 7.32 s; r36 must use the other window. "
        "Do not replay frames."
    )

    pool["assets"].extend(
        [
            {
                "id": "sdo_hmi_continuum",
                "title": "SDO/HMI continuum intensitygram, 2024-06-01 00:00 UTC",
                "credit": "NASA/SDO",
                "licence": "public domain (NASA images are not copyrighted; https://www.nasa.gov/nasa-brand-center/images-and-media/)",
                "page": "https://sdo.gsfc.nasa.gov/assets/img/browse/2024/06/01/",
                "file": "https://sdo.gsfc.nasa.gov/assets/img/browse/2024/06/01/20240601_000000_4096_HMIIF.jpg",
                "status": "ok",
                "note": (
                    "HTTP 200 on the 4096 file. The 1024 preview shows the visible-light disk and a "
                    "bottom-left stamp, 'SDO/HMI Quick-Look Continuum: 20240601_000000'. Crop that stamp. "
                    "sdo.gsfc.nasa.gov/data/rules.php was showing a storage-failure banner this run, so the "
                    "licence line is NASA's media policy, not a quote from that page. Two uses: full disk (r07) and a limb crop (r30)."
                ),
            },
            {
                "id": "eso_lasilla_ntt",
                "title": "Milky Way moves over the NTT, La Silla",
                "credit": "ESO/B. Tafreshi (twanight.org)",
                "licence": "ESO copyright page states CC BY 4.0 for ESO videos; this video page states the credit and does not repeat CC BY",
                "page": "https://www.eso.org/public/videos/bt_lasilla2_ntt/",
                "file": "https://cdn.eso.org/videos/hd_1080p25_screen/bt_lasilla2_ntt.mp4",
                "status": "ok",
                "note": (
                    "HTTP 200. 20 s, 30 fps, La Silla, the NTT. This is not the dropped bt_lasilla_fd2 fulldome. "
                    "It is still Tafreshi. One stretch, r35, 11.02 s of the 20 s. Do not loop."
                ),
            },
            {
                "id": "sts083_hale_bopp",
                "title": "Comet Hale-Bopp from Columbia (sts083-410-009)",
                "credit": "NASA/JSC",
                "licence": "not stated on the image record",
                "page": "https://images.nasa.gov/details/sts083-410-009",
                "file": "https://images-assets.nasa.gov/image/sts083-410-009/sts083-410-009~orig.jpg",
                "status": "not_used",
                "note": (
                    "File HTTP 200. A time exposure of the comet at Earth's limb. "
                    "The images.nasa.gov metadata does not say public domain or CC BY 4.0, so it was not cleared. "
                    "Not on a plate."
                ),
            },
        ]
    )
    pool["version"] = "v02"
    pool["job"] = "J0321"
    pool["checked"] = "2026-10-15"

    boards["do_not_use"] = list(boards.get("do_not_use") or [])
    boards["do_not_use"].append(
        {
            "id": "oort_labelled",
            "title": "Oort Cloud illustration on science.nasa.gov",
            "credit": "NASA",
            "licence": "would be public domain; the picture is a labelled diagram",
            "page": "https://science.nasa.gov/resource/oort-cloud/",
            "file": "https://assets.science.nasa.gov/content/dam/science/psd/solar/2023/09/o/Oort_Cloud.jpg",
            "status": "reject",
            "note": "Labels: Kuiper Belt, an orbit caption, Oort Cloud. picture_qa FAIL.",
        }
    )

    (EDIT / "PLATE_BOARDS_v02.json").write_text(json.dumps(boards, indent=2) + "\n")
    (EDIT / "SOURCE_POOL_v02.json").write_text(json.dumps(pool, indent=2) + "\n")

    review = f"""# 028 price review v02 (updated for J0850 live Flow read, 22 Oct 2026)

Gemini (`gemini`), 22 Oct 2026, J0850 (updating Cursor's 15 Oct J0321 / J0337 `PRICE_REVIEW_v02.md` with today's live Flow reading after HOS 007's J0352 mint). **No mint. No spend.** Parked for Chief (`parked for Chief: 028 Flow price pass`).

v01 files are unchanged. Rebuild with `python3 _build_plate_boards_v02.py`. Also written: `FLOW_PRICE_TABLE_J0850.md`.

## Readings this run (22 Oct 2026)

- Flow: **{FLOW_LEFT}** credits at `{FLOW_READ_AT}` (`ai_spend_daily.py --dry-run --pools flow,vertex`, account picker, `benoats@googlemail.com`, CDP `:9222`). Down `2,790` net from the 15 Oct reading (`23,740`) after HOS 007 minted all `73/73` Flow rows in `J0352` (`46d59506`) for `2,890` credits (`24 Quality × 100 + 49 Fast × 10 = 2,890 cr`, 100% try-1 KEEP, plus two `+50` Flow allotment adjustments).
- Vertex promo: **£{VERTEX_PROMO:.2f}** Available at `{VERTEX_READ_AT}` (`Google Developer Program premium benefit - CREDIT_TYPE_MONTHLY`). Free Trial **£0.00 Used**. Usable **£{usable:.2f}** after the £1.00 margin. No spend logged in this run.

## Remaining 028 picture rows to mint (`boards v02`)

All £0 rows are already built and PASS on `main`:
- **33 harvest rows** (21 NASA/ESA/ESO files): `J0350` PASS (`14566db2`), **0 Flow credits / £0.00**.
- **20 code graphics + subscribe card** (`19` code beats + `1` card in `code_graphics_v02`, plus `teaching_overlays_v01_pack`): `J0338` + `J0382` `20/20` PASS, **0 Flow credits / £0.00**.

Only **4 plates** remain on `PLATE_BOARDS_v02.json` (**2 Flow Veo** + **2 Vertex Omni**):

| Plate ID | Row | Ch | Span (`t_in–t_out`) | `use_s` | Route / Model | Clip s | Flow Try-1 | Flow Expected | Vertex Try-1 | Vertex Expected / Hold | Status |
|---|---:|---:|---|---:|---|---:|---:|---:|---:|---:|---|
| `r11_night_road` | 11 | 1 | `95.08–109.20 s` | `14.12 s` | **Flow · Veo 3.1 Quality** (`night_road_veo_v01`) | 8 s | **100 cr** | **259 cr** | £0.00 *(fallback £1.28)* | £0.00 *(fallback £3.32)* | Unminted (`generation_authorized: false`) |
| `r17_pitch` | 17 | 2 | `191.00–194.82 s` | `3.82 s` | **Flow · Veo 3.1 Fast** (`football_pitch_veo_v01`) | 8 s | **10 cr** | **20 cr** | £0.00 *(fallback £0.64)* | £0.00 *(fallback £1.25)* | Unminted (`generation_authorized: false`) |
| `r08_orbit_binoculars` | 8 | 1 | `58.64–66.52 s` | `7.88 s` | **Vertex `global` · `gemini-omni-flash-preview`** (`orbit_binoculars_omni_v01`) | 8 s | **0 cr** | **0 cr** | **£0.65** | **£0.65** *(+£0.65 retry hold)* | Unminted (`generation_authorized: false`) |
| `r23_orbit_ice` | 23 | 3 | `241.88–249.84 s` | `7.96 s` | **Vertex `global` · `gemini-omni-flash-preview`** (`orbit_ice_omni_v01`) | 8 s | **0 cr** | **0 cr** | **£0.65** | **£0.65** *(+£0.65 retry hold)* | Unminted (`generation_authorized: false`) |
| **Remaining Total (4 rows)** | | | | `33.78 s` | **1 Quality + 1 Fast (Flow) · 2 Omni (Vertex)** | | **110 cr** | **279 cr** | **£1.30** | **£1.30** *(£2.60 w/ retry)* | **Parked for Chief** |

*Note on `r11_night_road` (`14.12 s` span across 3 cuts in `SHOT_LIST_v01.md`):* `PLATE_BOARDS_v02.json` prices one 8 s Quality take (`100` try-1 / `259` expected). If Chief wants a second 8 s continuation clip (`r11_night_road_c1`) so the 14.12 s span needs no slow-stretch or cutaway, adding `+1 Fast` is `+10` try-1 / `+20` expected (`120` try-1 / `299` expected total), or `+1 Quality` is `+100` try-1 / `+259` expected (`210` try-1 / `538` expected total). All three options easily clear the `3,000` Flow floor by more than `+4,450` credits.

## What the ten J0310/J0321 rulings did

1. Night road stays **Quality**. Dusk pitch stays **Fast**. Both planned on Flow. Neither is authorised to mint.
2. Both Orbit Omni takes are priced at the Gemini Omni Flash list price, 720p with audio, 8 s: **£{OMNI_GBP:.2f}** a take, **£{omni_gbp:.2f}** for the pair. Late-billing room held equal to that pair (£{late_room:.2f}), on top of the £1 margin. £{omni_gbp + late_room:.2f} fits inside £{usable:.2f} usable. They stay Omni. No KEEP-pose fallback.
3. r35's Gliese-motion stretch is dropped. Five stretches remain (r01, r02, r12, r27, r38). The row is filled with the NTT time-lapse at La Silla.
4. K dwarf is a £0 Codex card (K dwarf vs Sun). The labelled Hubble chart stays out.
5. The Sun is an HMI continuum intensitygram (visible light), 2024-06-01 00:00 UTC. Crop the quick-look stamp in the black corner. The limb row is a second crop of that still. AIA 335 is unused.
6. The © Slawik Hale-Bopp image is rejected. r26 is a second framing of comet C/2023 A3. r28 cannot take a third comet still (NEOWISE is already at two), so it is a £0 comet-tail card. The Columbia frame sts083-410-009 was not used: its NASA record does not state public domain.
7. Hipparcos: the file is real and the page says Copyright: ESA, so it is not cleared. The row is a £0 code card. Oort: the NASA file is a labelled diagram, rejected. Oort and the row 20 shell are one £0 code beat. The Tafreshi fulldome bt_lasilla_fd2 stays dropped. r36 is the unused window of the Brunier La Silla lapse (17 s source, 7.32 s already used at r06).
8. WISE all-sky (PIA15481 small) has no axis labels and no readable text. Kept. Gaia motion, the Gliese encounter and the EDR3 sky are flagged for picture_qa as diagrams on purpose. Neptune's corner credit says green and orange filters. Juno's says colour-enhanced.
9. Code-graphic stacks are broken by merging each named stack into one beat. A second NGC 3603 crop sits between the row 4 beat and the row 5 beat. A second ISS sunrise crop sits between the path beat and the scale card, which was the other back-to-back pair (row 16 into row 17). A rebuild check refuses two code routes in a row.

## Flow balance after 028 & headroom for HOS

On 15 Oct (`J0337`), HOS 007 was reserved at `7,553` expected credits against `23,740` left, leaving `2,949` after 028 (`51` cr short of the `3,000` gate).
On 21 Oct (`J0352`, HOS `#351`), HOS 007 minted all `73/73` Flow rows on take 1 for **`2,890` actual credits** (all Chief KEEP; `full_join_v01` assembled in `J0827` with 0 new mints), freeing **`4,663` credits** vs the `7,553` reserve (plus `+100` cr net Flow adjustment).

| Pool / Film | Try-1 Credits | Expected Credits | Balance After (Try-1) | Balance After (Expected) | Notes |
|---|---:|---:|---:|---:|---|
| **Live Flow balance (22 Oct 16:56Z)** | — | — | **20,950** | **20,950** | `benoats@googlemail.com` (CDP `:9222`) |
| **HOS 006** | 0 | {HOS_EXPECTED['006']} | 20,950 | 20,950 | Done (`full_join_v03_teach` on HOS `main`, 0 Flow) |
| **HOS 007** | 0 | {HOS_EXPECTED['007']} | 20,950 | 20,950 | Done (`73/73` rows minted & KEEP in `J0352` for `2,890` cr, already deducted from `20,950`; `full_join_v01` in `J0827`) |
| **OWB 028 (if minted next)** | **110** | **{flow_exp}** | **20,840** | **20,671** | 1 Quality (`{Q_EXP}` exp) + 1 Fast (`{F_EXP}` exp) |
| **HOS 008** (`PRICE_REVIEW_v03`) | 2,360 | {HOS_EXPECTED['008']} | 18,480 | 15,066 | 15 Quality + 86 Fast (11 £0 code graphics done in `J0329`/`J0383`) |
| **HOS 009 tranche 1** (`PRICE_REVIEW_v04`/`v05`) | 2,910 | {HOS_EXPECTED['009']} | **15,570** | **{after_028}** | 26 Quality + 31 Fast (12 £0 code graphics done in `J0342`/`J0383`) |
| **Remaining HOS sum (`006–009 T1`)** | **5,270** | **{hos_sum}** | 15,680 *(before 028)* | **{after_hos}** *(before 028)* | Leaves **{after_hos} cr** before 028 |
| **After HOS (`006–009 T1`) + OWB 028 (`279`)** | **5,380** | **{hos_sum + flow_exp}** | **15,570** | **{after_028}** | **PASSES the 3,000 gate by +{surplus_over_3000} cr** (`{after_028} >= 3,000`) |

*Deferred to the ~12 Nov AI Ultra renewal (not charged against today's `20,950` pool):*
- **HOS 009 tranche 2:** `{HOS_009_TRANCHE2}` expected (`2,000` try-1, 20 Quality rows).
- **HOS 010 (`PRICE_REVIEW_v03`):** `12,393` expected (`4,810` try-1, 47 Quality + 11 Fast rows).
- **HOS 007–010 Shorts (`SHORTS_PRICE_REVIEW_v01`) & OWB 029 (`PRICE_REVIEW_v03`):** `0` Flow credits.

## Vertex (`£71.02` Available, `£70.02` Usable)

| Item | £ |
|---|---:|
| Promo available (`CREDIT_TYPE_MONTHLY`) | {VERTEX_PROMO:.2f} |
| Margin | {VERTEX_MARGIN:.2f} |
| Usable | {usable:.2f} |
| 028 Omni ×2 (`r08_orbit_binoculars`, `r23_orbit_ice`), one take each | {omni_gbp:.2f} |
| Late-billing room (one retry of both takes) | {late_room:.2f} |
| Total held for 028 (incl. £1.00 margin) | {omni_gbp + late_room + VERTEX_MARGIN:.2f} |
| **Usable promo remaining after 028 Omni hold** | **{usable - (omni_gbp + late_room):.2f}** |

Omni **fits** (`£1.30` expected, `£2.60` with retry reserve vs `£70.02` usable). Veo stays on Flow (`279` expected credits). Nothing is authorised to generate until Chief passes `J0850`.

## Full-Film Totals (`PLATE_BOARDS_v02.json`)

| plates | Quality (Flow) | Fast (Flow) | Omni (Vertex) | code (£0) | card (£0) | harvest (£0) | Flow try-1 | Flow expected | Omni £ |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| {len(plates)} | {boards['totals']['quality']} | {boards['totals']['fast']} | {boards['totals']['omni']} | {boards['totals']['code']} | {boards['totals']['card']} | {boards['totals']['harvest_ok']} | {flow_try} | {flow_exp} | {omni_gbp:.2f} |

`generation_authorized` is `false` on every plate. Parked for Chief (`parked for Chief: 028 Flow price pass`).
"""
    (EDIT / "PRICE_REVIEW_v02.md").write_text(review)
    (EDIT / "FLOW_PRICE_TABLE_J0850.md").write_text(review)
    print(
        f"plates={len(plates)} flow_exp={flow_exp} omni=£{omni_gbp:.2f} "
        f"headroom_ok={headroom_ok} after_hos={after_hos} after_028={after_028} "
        f"surplus_over_3000={surplus_over_3000} omni_fits={omni_fits}"
    )


if __name__ == "__main__":
    main()
