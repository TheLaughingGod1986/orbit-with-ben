#!/usr/bin/env python3
"""029 plate boards v03 from v02, applying Chief's J0353 rulings (J0808).

No mint. No spend. Rebuilds PLATE_BOARDS_v03.json, SOURCE_POOL_v03.json and
PRICE_REVIEW_v03.md next to this file.

  python3 _build_plate_boards_v03.py
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

EDIT = Path(__file__).resolve().parent
V02 = EDIT / "PLATE_BOARDS_v02.json"
POOL_V02 = EDIT / "SOURCE_POOL_v02.json"

ESO_LICENCE = "CC BY 4.0"
NOIRLAB_LICENCE = "CC BY 4.0"


def zero(p: dict) -> None:
    p["flow_credits_try1"] = 0
    p["flow_credits_expected"] = 0
    p["vertex_try1_gbp"] = 0.0
    p["vertex_expected_gbp"] = 0.0
    p["generation_authorized"] = False
    p["quality"] = None
    p.pop("vertex_model", None)
    p.pop("vertex_clip_s", None)
    p.pop("source_in_s", None)
    p.pop("source_out_s", None)


def find(plates: list[dict], pid: str) -> dict:
    for p in plates:
        if p["id"] == pid:
            return p
    raise SystemExit(f"missing plate {pid}")


def as_code(p: dict, asset: str, line: str, credit: str | None = None, licence: str = "£0 code graphic") -> None:
    zero(p)
    p["route"] = "code"
    p["asset_id"] = asset
    p["asset_status"] = "code"
    p["line"] = line
    p["credit"] = credit
    p["licence"] = licence
    p["reference"] = "07_Edit-Project/build_code_graphics_v01.py"
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
    corner_tag: str | None = None,
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
    if corner_tag is not None:
        p["corner_tag"] = corner_tag


def main() -> None:
    boards = json.loads(V02.read_text())
    pool = json.loads(POOL_V02.read_text())
    plates: list[dict] = boards["plates"]

    # Chief J0353 rulings on the 6 quarantined assets (only those 9 rows modified):
    # 1. r02_surface -> sphere_jan
    as_harvest(
        find(plates, "r02_surface"),
        "sphere_jan",
        "J0353 Chief ruling: single SPHERE January 2019 frame (eso2003b), replacing multi-panel eso2109a.",
        "ESO/M. Montargès et al.",
        ESO_LICENCE,
        "https://cdn.eso.org/images/large/eso2003b.jpg",
    )

    # 2. r05_surface -> sphere_dec
    as_harvest(
        find(plates, "r05_surface"),
        "sphere_dec",
        "J0353 Chief ruling: single SPHERE December 2019 frame (eso2003a), replacing multi-panel eso2109a.",
        "ESO/M. Montargès et al.",
        ESO_LICENCE,
        "https://cdn.eso.org/images/large/eso2003a.jpg",
    )

    # 3. r13_compare -> own £0 code split of sphere_jan | sphere_dec with house labels (Jan 2019 / Dec 2019)
    as_code(
        find(plates, "r13_compare"),
        "sphere_split_code",
        "J0353 Chief ruling: own £0 code split of sphere_jan | sphere_dec with house labels (Jan 2019 / Dec 2019), not ESO's labelled panel eso2003c.",
        credit="ESO/M. Montargès et al. · CGI",
        licence="CC BY 4.0 + £0 code graphic",
    )

    # 4. r14_ejection -> dust_impression with an 'Artist's impression' tag + full credit
    as_harvest(
        find(plates, "r14_ejection"),
        "dust_impression",
        "J0353 Chief ruling: dust_impression (heic2014a) tagged 'Artist's impression' with full credit ESO, ESA/Hubble, M. Kornmesser, replacing labelled opo22037a.",
        "ESO, ESA/Hubble, M. Kornmesser",
        ESO_LICENCE,
        "https://cdn.esahubble.org/archives/images/large/heic2014a.jpg",
        corner_tag="Artist's impression · ESO, ESA/Hubble, M. Kornmesser",
    )
    # Also ensure r14_dust carries the full artist's impression tag
    r14_dust = find(plates, "r14_dust")
    r14_dust["corner_tag"] = "Artist's impression · ESO, ESA/Hubble, M. Kornmesser"

    # 5. r32_ejection -> visir_flames (real VISIR observation of the shed material), credit ESO/P. Kervella
    as_harvest(
        find(plates, "r32_ejection"),
        "visir_flames",
        "J0353 Chief ruling: visir_flames (eso1121a, real VISIR observation of the shed material), credit ESO/P. Kervella, replacing labelled opo22037a.",
        "ESO/P. Kervella",
        ESO_LICENCE,
        "https://cdn.eso.org/images/large/eso1121a.jpg",
    )

    # 6. r21_bh -> drop neutron_bh (merger sim, wrong context) and use a £0 code graphic of core collapse
    as_code(
        find(plates, "r21_bh"),
        "core_collapse_bh",
        "J0353 Chief ruling: £0 code graphic of single-star core collapse to a black hole, replacing NASA neutron-star merger simulation e001102.",
    )

    # 7. r33_pair -> companion_speckle (non-annotated NOIRLab)
    as_harvest(
        find(plates, "r33_pair"),
        "companion_speckle",
        "J0353 Chief ruling: companion_speckle (noirlab2523c, non-annotated Gemini North speckle), replacing annotated inset noirlab2523b.",
        "International Gemini Observatory/NOIRLab/NSF/AURA. Image processing: M. Zamani (NSF NOIRLab)",
        NOIRLAB_LICENCE,
        "https://storage.noirlab.edu/media/archives/images/large/noirlab2523c.jpg",
    )

    # 8. r34_pair -> orion_over_paranal for the wide
    as_harvest(
        find(plates, "r34_pair"),
        "orion_over_paranal",
        "J0353 Chief ruling: orion_over_paranal (bt-paranal-orion135mm) for the wide Orion beat, replacing annotated inset noirlab2523b.",
        "ESO/B. Tafreshi",
        ESO_LICENCE,
        "https://cdn.eso.org/videos/hd_1080p25_screen/bt-paranal-orion135mm.mp4",
    )

    # 9. r21_neutron -> drop neutron_wind (third-party rights) and use crab (pulsar at the Crab's heart, full ESA/Hubble credit)
    as_harvest(
        find(plates, "r21_neutron"),
        "crab",
        "J0353 Chief ruling: crab (heic0515a, pulsar at the Crab's heart, full ESA/Hubble credit), replacing third-party XMM-Newton neutron_wind.",
        "NASA, ESA and Allison Loll/Jeff Hester (Arizona State University). Acknowledgement: Davide De Martin (ESA/Hubble)",
        ESO_LICENCE,
        "https://cdn.esahubble.org/archives/images/large/heic0515a.jpg",
    )

    # Skip the ESO logo bumper on chajnantor_mw (0.00-3.25s opening bumper, 13.30-16.36s closing bumper)
    find(plates, "r24_superk")["source_in_s"] = 3.25
    find(plates, "r24_superk")["url"] = "https://cdn.eso.org/videos/hd_and_apple/chajnantormilkyway.m4v"
    find(plates, "r24_superk_2")["source_in_s"] = 7.15
    find(plates, "r24_superk_2")["url"] = "https://cdn.eso.org/videos/hd_and_apple/chajnantormilkyway.m4v"

    # Update chapters list in boards so plate IDs match the actual plates in each chapter
    for ch_obj in boards["chapters"]:
        ch_name = ch_obj["chapter"]
        ch_obj["plates"] = [p["id"] for p in plates if p["chapter"] == ch_name]

    # Every plate: no mint.
    for p in plates:
        p["generation_authorized"] = False
        if p["route"] != "omni":
            p["vertex_try1_gbp"] = 0.0
            p["vertex_expected_gbp"] = 0.0
            p["flow_credits_try1"] = 0
            p["flow_credits_expected"] = 0

    def nroute(name: str) -> int:
        return sum(1 for p in plates if p["route"] == name)

    boards["version"] = "v03"
    boards["job"] = "J0808"
    boards["status"] = "parked for Chief: J0353 rulings applied + part roughs v01"
    boards["built"] = "2026-10-22"
    boards["mint"] = False
    boards["totals"]["plates"] = len(plates)
    boards["totals"]["omni"] = nroute("omni")
    boards["totals"]["code"] = nroute("code")
    boards["totals"]["card"] = nroute("card")
    boards["totals"]["harvest_ok"] = nroute("harvest")

    stretches: dict[str, list[str]] = {}
    for p in plates:
        if p["route"] == "harvest":
            stretches.setdefault(p["asset_id"], []).append(p["id"])
    boards["harvest_stretches"] = stretches
    boards["rulings"] = (
        "J0353 Chief PASS rulings applied in J0808 (only the 9 rows): "
        "r02_surface -> sphere_jan, r05_surface -> sphere_dec, r13_compare -> £0 code split (sphere_jan | sphere_dec), "
        "r14_ejection -> dust_impression tagged 'Artist's impression', r32_ejection -> visir_flames, "
        "r21_bh -> £0 core-collapse code graphic, r33_pair -> companion_speckle, r34_pair -> orion_over_paranal, "
        "r21_neutron -> crab. No mint. No spend."
    )

    # Update pool statuses for the 6 quarantined assets
    quarantined = {
        "betelgeuse_surface": "Quarantined in J0353 (four-panel comparison with borders); replaced on r02/r05 by sphere_jan/sphere_dec.",
        "sphere_compare": "Quarantined in J0353 (labelled two-panel comparison); replaced on r13 by our own £0 code split of sphere_jan | sphere_dec.",
        "mass_ejection": "Quarantined in J0353 (labelled chart/multi-panel illustration); replaced on r14/r32 by dust_impression and visir_flames.",
        "neutron_bh": "Quarantined in J0353 (supercomputer simulation of binary neutron star merger); replaced on r21_bh by £0 core-collapse code graphic.",
        "companion_orion": "Quarantined in J0353 (labelled inset/arrow composite); replaced on r33_pair/r34_pair by companion_speckle and orion_over_paranal.",
        "neutron_wind": "Quarantined in J0353 (third-party ESA/XMM-Newton rights); replaced on r21_neutron by crab (pulsar at the Crab's heart).",
    }
    by_id = {a["id"]: a for a in pool["assets"]}
    for qid, qnote in quarantined.items():
        if qid in by_id:
            by_id[qid]["status"] = "reject"
            by_id[qid]["reject"] = qnote
            by_id[qid]["note"] = qnote

    # Ensure full credits in pool match HARVEST_REVIEW_v01
    if "crab" in by_id:
        by_id["crab"]["credit"] = (
            "NASA, ESA and Allison Loll/Jeff Hester (Arizona State University). "
            "Acknowledgement: Davide De Martin (ESA/Hubble)"
        )
    if "chajnantor_mw" in by_id:
        by_id["chajnantor_mw"]["url"] = "https://cdn.eso.org/videos/hd_and_apple/chajnantormilkyway.m4v"
        by_id["chajnantor_mw"]["note"] = "1280x720 HD stream; skip ESO logo bumpers at 0.00-3.25s and 13.30-16.36s (use 3.25-13.25s clean sky window)."
    if "companion_speckle" in by_id:
        by_id["companion_speckle"]["title"] = "Betelgeuse and Its Stellar Companion (noirlab2523c clean speckle observation)"

    pool["version"] = "v03"
    pool["job"] = "J0808"
    pool["checked"] = "2026-10-22"
    pool["assets"] = list(by_id.values())
    pool["items"] = pool["assets"]

    # Also append the 6 quarantined items to boards["do_not_use"]
    dnu_ids = {x["id"] for x in boards.get("do_not_use", [])}
    for qid in quarantined:
        if qid not in dnu_ids and qid in by_id:
            boards["do_not_use"].append(by_id[qid])

    (EDIT / "PLATE_BOARDS_v03.json").write_text(json.dumps(boards, indent=2) + "\n")
    (EDIT / "SOURCE_POOL_v03.json").write_text(json.dumps(pool, indent=2) + "\n")

    t = boards["totals"]
    review = f"""# 029 plate boards & source rulings v03 (`J0808`)

Applied by Gemini (`gemini-agy`, 22 Oct 2026) from Chief's `J0353` PASS rulings. **No mint. No spend (`£0`).**

## Chief `J0353` Rulings Applied (9 rows only)

1. **`r02_surface`** (`10.00–13.34 s`): `betelgeuse_surface` (`eso2109a`) → **`sphere_jan`** (`eso2003b`, single SPHERE January 2019 frame, `ESO/M. Montargès et al.`).
2. **`r05_surface`** (`37.74–41.90 s`): `betelgeuse_surface` (`eso2109a`) → **`sphere_dec`** (`eso2003a`, single SPHERE December 2019 frame, `ESO/M. Montargès et al.`).
3. **`r13_compare`** (`130.42–137.80 s`): `sphere_compare` (`eso2003c`) → **`route: code` (`sphere_split_code`)**, our own `£0` side-by-side split of `sphere_jan | sphere_dec` with house labels (`Jan 2019` / `Dec 2019`), then pushing into the December panel (`ESO/M. Montargès et al. · CGI`).
4. **`r14_ejection`** (`138.44–142.80 s`): `mass_ejection` (`opo22037a`) → **`dust_impression`** (`heic2014a`) tagged `"Artist's impression"` with full credit (`ESO, ESA/Hubble, M. Kornmesser`).
5. **`r32_ejection`** (`385.70–392.00 s`): `mass_ejection` (`opo22037a`) → **`visir_flames`** (`eso1121a`, real VISIR observation of the shed material around Betelgeuse, credit `ESO/P. Kervella`).
6. **`r21_bh`** (`236.80–241.88 s`): `neutron_bh` (`e001102` binary merger simulation) → **`route: code` (`core_collapse_bh`)**, our own `£0` code graphic of single-star core collapse into a black hole.
7. **`r33_pair`** (`403.00–412.74 s`): `companion_orion` (`noirlab2523b`) → **`companion_speckle`** (`noirlab2523c`, non-annotated Gemini North speckle observation, credit `International Gemini Observatory/NOIRLab/NSF/AURA. Image processing: M. Zamani (NSF NOIRLab)`).
8. **`r34_pair`** (`419.50–425.30 s`): `companion_orion` (`noirlab2523b`) → **`orion_over_paranal`** (`bt-paranal-orion135mm`, wide Orion over Paranal clip, credit `ESO/B. Tafreshi`).
9. **`r21_neutron`** (`226.64–232.00 s`): `neutron_wind` (`e000279`, third-party rights) → **`crab`** (`heic0515a`, pulsar at the heart of the Crab Nebula, full credit `NASA, ESA and Allison Loll/Jeff Hester (Arizona State University). Acknowledgement: Davide De Martin (ESA/Hubble)`).

## Totals (`PLATE_BOARDS_v03.json`)

| plates | Quality | Fast | Omni (not minted) | code | harvest | card | Flow expected | Spend |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| {t['plates']} | 0 | 0 | {t['omni']} | {t['code']} | {t['harvest_ok']} | {t['card']} | 0 | £0.00 |

`generation_authorized` is `false` on every plate.
"""
    (EDIT / "PRICE_REVIEW_v03.md").write_text(review)
    print(f"v03 built: plates={t['plates']} harvest={t['harvest_ok']} code={t['code']} card={t['card']} omni={t['omni']}")


if __name__ == "__main__":
    main()
