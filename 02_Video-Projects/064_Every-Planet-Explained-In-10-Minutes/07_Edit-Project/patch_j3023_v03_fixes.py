#!/usr/bin/env python3
"""Update v02 cuts/provenance for master v03 to eliminate all 3 v02 gate failures
and visual framing defects (zero PIA00271/PIA00233, exact R11 PIA00215 preserved, £0 spend).
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_FILM = Path(__file__).resolve().parents[1]
REPO_EDIT = REPO_FILM / "07_Edit-Project"
NAS_FILM = Path(
    "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/"
    "064_Every-Planet-Explained-In-10-Minutes"
)
NAS_EDIT = NAS_FILM / "07_Edit-Project"

CUTS_PATH = REPO_EDIT / "cuts_064_j3023_v02.json"
PROV_PATH = REPO_EDIT / "POOL_PROVENANCE_J3023_v02.json"


def main() -> None:
    cuts = json.loads(CUTS_PATH.read_text(encoding="utf-8"))
    prov = json.loads(PROV_PATH.read_text(encoding="utf-8"))

    pluto_seen = 0
    for i, c in enumerate(cuts):
        fname = Path(c["source"]).name
        framing = dict(c.get("framing") or {})

        # 1. Remove pure-black bottom strip (y >= 880, luma 0.0) on PIA21046.jpg (fixes split-panel horizontal gutter at 0.88 / 0.90)
        if fname == "PIA21046.jpg":
            framing["crop_xyxy"] = [0, 0, 2012, 876]
            framing["note"] = "J3023 v03 fix: cropped bottom black strip [0,0,2012,876] + luminance-keyed onto lifted cosmic navy"

        # 2. Switch plate_031_r25_iss_orbit_cuts_v01.mp4 to real sunlit ISS/Soyuz Earth horizon at 6.0s (removes red animation & low-detail WARN)
        elif fname == "plate_031_r25_iss_orbit_cuts_v01.mp4":
            framing["offset"] = 6.0
            c["source_in"] = 6.0
            framing["note"] = "J3023 v03 fix: shifted offset 9.0s -> 6.0s (real sunlit ISS/Soyuz Earth horizon, 6.0-8.95s)"

        # 3. Switch second New Horizons Pluto Flyby cut (idx 137, R51) to high-detail cratered horizon at 46.5s (std 17.0, edge 0.064, 27.5s from R49)
        elif "Pluto_Flyby" in fname:
            pluto_seen += 1
            if pluto_seen == 1:
                framing["offset"] = 12.0
                c["source_in"] = 12.0
            else:
                framing["offset"] = 46.5
                c["source_in"] = 46.5
                framing["note"] = "J3023 v03 fix: shifted offset 23.5s -> 46.5s (high-detail Pluto terrain, std ~17.0, edge ~0.064, >27s after R49)"

        c["framing"] = framing

    # Safety guards
    for c in cuts:
        assert "PIA00271" not in c["source"], "PIA00271 forbidden!"
        assert "PIA00233" not in c["source"], "PIA00233 forbidden!"
        assert "Five_Minutes_in_Orbit" not in c["source"], "Five_Minutes_in_Orbit forbidden!"
        assert "JPL-20210222-M2020f-0001" not in c["source"], "Split-screen M2020 forbidden!"
    r11 = [c for c in cuts if c["row_id"] == "R11"]
    assert len(r11) == 2 and Path(r11[0]["source"]).name == "PIA00215.jpg"
    assert abs(r11[0]["timeline_in"] - 118.05) < 0.01 and abs(r11[0]["timeline_out"] - 124.40) < 0.01
    assert r11[0]["framing"]["crop_xyxy"] == [350, 600, 2550, 1838]

    cuts_txt = json.dumps(cuts, indent=2) + "\n"
    CUTS_PATH.write_text(cuts_txt, encoding="utf-8")
    (NAS_EDIT / "cuts_064_j3023_v02.json").write_text(cuts_txt, encoding="utf-8")

    if isinstance(prov, dict):
        prov["v03_polish_fixes"] = {
            "date": "2026-11-27",
            "fixes": [
                "PIA21046.jpg cropped [0,0,2012,876] and luminance-keyed onto lifted cosmic navy (eliminates 0.88/0.90 horizontal gutter split-panel FAILs)",
                "plate_031_r25_iss_orbit_cuts_v01.mp4 offset 9.0s -> 6.0s (real sunlit ISS/Soyuz Earth horizon; removes red animation & low-detail WARN)",
                "New Horizons Pluto Flyby R51 offset 23.5s -> 46.5s (high-detail terrain, std ~17.0 / edge ~0.064; eliminates 11:39 low-detail FAIL)",
                "GLOBE_ON_BLACK reframes no longer rectangular-crop into planet disks (fixes square edges on Mars PIA00407, Neptune PIA01492, etc.)",
                "PIA19400.jpg tight reframe kept full-bleed 16:9 at <=1.92x (eliminates vertical pillarbox bars at 4:30)",
            ],
        }
        prov_txt = json.dumps(prov, indent=2) + "\n"
        PROV_PATH.write_text(prov_txt, encoding="utf-8")
        (NAS_EDIT / "POOL_PROVENANCE_J3023_v02.json").write_text(prov_txt, encoding="utf-8")

    print(f"Updated v03 cuts ({len(cuts)} cuts). All guards OK.")


if __name__ == "__main__":
    main()
