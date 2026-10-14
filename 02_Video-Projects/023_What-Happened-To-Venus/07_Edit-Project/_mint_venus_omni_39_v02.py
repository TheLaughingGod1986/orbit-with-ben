#!/usr/bin/env python3
"""Venus 023 #39 orbit_between_two_venus — the ONE approved remint (Claude 5984886311).

Exactly one submit, no retry loop. Vertex Omni at `global`, free trial only, £5 floor.
Start frame v02 (no orange grade; left cloud-white with sea gaps, right flat sulphur-grey haze)
composited from ORBIT_REF with an orbit_source sidecar; orbit_shot=True so the guard runs.
If this take still drifts, #39 is dropped (Ch. 3 runs #35–#38 as plates without Orbit).
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _mint_venus_omni_v01 as v01  # noqa: E402  (PROJECT/LOCATION/MODEL, client, sheet helpers)
from orbit_gemini_omni import generate_omni_clip, write_orbit_source_sidecar  # noqa: E402

assert v01.LOCATION == "global"
START = v01.STARTS / "orbit_between_two_venus_start_v02.png"
DEST = v01.OUT / "orbit_between_two_venus_omni_v02.mp4"
SHEET = v01.SHEETS / "orbit_between_two_venus_omni_v02_6frame.jpg"
REPORT = v01.EDIT / "omni_gen_report_39_v02.json"

PROMPT = (
    "Deep space. Two planets flank the frame. Both planets are Venus and stay exactly as in "
    "the start frame: smooth featureless cloud globes, no bands, no stripes, no storms, no red "
    "spot, not Jupiter, not Saturn. Left: a cloud-white Venus with a few cloud gaps showing "
    "hints of dark blue sea. Right: a dim sulphur-yellow and grey hazy Venus, a flat featureless "
    "globe. The camera does not move. Orbit stays small and centred between them, eyes open, "
    "and slowly turns his head from the left world to the right world, asking without words."
    + v01.ORBIT_LOCK
    + " No text, no logo. Silent picture only."
)


def main() -> None:
    if DEST.exists():
        raise SystemExit(f"{DEST.name} already exists — the one approved remint was already used")
    write_orbit_source_sidecar(
        START,
        shot=39,
        scene="v02: left cloud-white Venus with a few soft cloud gaps showing dark blue sea; right dim "
              "sulphur-yellow/grey flat featureless haze globe; no orange grade, bands or swirls; Orbit ~178px centre",
        previous="orbit_between_two_venus_start.png (v01, right world drifted to Jupiter)",
        method="Orbit cut from ORBIT_REF (rembg u2net matte + hand masks), scaled only, over graded NASA/JPL "
               "Mariner 10 Venus PIA23791 + procedural starfield",
        script="02_Video-Projects/023_What-Happened-To-Venus/07_Edit-Project/_composite_venus_orbit_start_39_v02.py",
        composited="2026-10-04",
        request="Claude PR #99 comment 5984886311",
    )
    client = v01.make_client()
    report = {
        "startedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "engine": "vertex_omni", "project": v01.PROJECT, "location": v01.LOCATION, "model": v01.MODEL,
        "floor_gbp": v01.FLOOR_GBP, "id": "orbit_between_two_venus_omni_v02", "start": START.name,
        "prompt": PROMPT, "request": "Claude 5984886311 (one remint approved)",
    }
    t0 = time.time()
    try:
        meta = generate_omni_clip(client, PROMPT, DEST, orbit_ref=START, orbit_shot=True,
                                  model=v01.MODEL, aspect_ratio="16:9")
        v01.six_frame_sheet(DEST, SHEET)
        report.update(**meta); report.update(status="ok", wall_seconds=round(time.time() - t0, 1), sheet=SHEET.name,
                      bytes=DEST.stat().st_size,
                      sha256=subprocess.check_output(["shasum", "-a", "256", str(DEST)], text=True).split()[0])
    except BaseException as e:  # noqa: BLE001 — no retry, record and stop
        report.update(status="fail", seconds=round(time.time() - t0, 1), error=f"{type(e).__name__}: {e}")
    report["finishedAt"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if report["status"] != "ok":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
