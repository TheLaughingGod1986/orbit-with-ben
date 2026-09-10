#!/usr/bin/env python3
"""Mac-only: fix Part 03 UAT FAIL (nonsense flat water-plane tidal plates) → rough v02 → OWB UAT.

Run on mac-mini with Flow Chrome CDP :9222 signed in + credits:

  cd ~/YouTube/orbit-with-ben
  git fetch && git checkout cursor/moon-leaving-p03-uat-fail-6513 && git pull
  python3 02_Video-Projects/013_Why-The-Moon-Is-Slowly-Leaving-Us/07_Edit-Project/_fix_part03_tidal_uat_v02.py

Does NOT remint Part 01/02. No freeze-pad.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
REPO = PROJ.parents[1]
PLATES = PROJ / "04_Generated-Clips/part03/flow_world_v01"
REJECT = PROJ / "04_Generated-Clips/part03/_rejected_tidal_plane_2026-09-10"
PROMPTS = HERE / "parts/part-03_flow_prompts_v01.json"
GEN = HERE / "_gen_part03_flow_world_v01.py"
ASM = HERE / "_assemble_part03_rough_v01.py"
ROUGH_V01 = HERE / "parts/moon_leaving_part-03_rough_v01.mp4"
ROUGH_V02 = HERE / "parts/moon_leaving_part-03_rough_v02.mp4"
META_V02 = HERE / "parts/moon_leaving_part-03_rough_v02_meta.json"
PLATE_MAP = HERE / "parts/part-03_plates_v01.json"
UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT"
STATUS = UAT / "moon_leaving_part-03_STATUS.txt"

# Suspect bulge / cross-section stems from Ben FAIL still
REGEN_IDS = ("p03_00", "p03_01", "p03_02", "p03_06")

LOCKED_PROMPTS = {
    "p03_00": (
        "Silent cinematic CGI. Whole Earth from deep space with realistic continents and clouds. "
        "Oceans remain ON the globe surface, slightly exaggerated into a soft leading tidal bulge "
        "facing ahead of the Moon. Moon beyond in clean vacuum. Continuous slow camera drift. "
        "No flat water plane in space. No sheet of ocean cutting through planets. No cross-section table. "
        "No text. No people. No mascot. Premium documentary look."
    ),
    "p03_01": (
        "Silent premium space documentary CGI. Full Earth globe; ocean tidal bulge as a gentle heap "
        "on the planet surface slightly ahead of the Moon; Moon in vacuum beyond. Motion implies torque. "
        "No labels. No flat infinite water plane. No water horizon bisecting Earth. No people. No text."
    ),
    "p03_02": (
        "Silent clean scientific CGI. Earth from space, moonlit oceans heaping into a leading bulge "
        "on the globe surface only; Moon beyond. No flat water table in space. No mirrored Earth under water. "
        "No text. No people."
    ),
    "p03_06": (
        "Silent cinematic educational CGI. Whole Earth (not a cutaway table). Subtle translucent "
        "visualization of ocean thickness ON the sphere with lunar pull; bulge offset ahead of Moon. "
        "Moon in space. Forbidden: flat ocean plane in vacuum, planet sliced by water sheet, twin Earth below waterline. "
        "No readable labels. No people."
    ),
}


def die(msg: str, code: int = 2) -> None:
    print(f"ABORT: {msg}", flush=True)
    raise SystemExit(code)


def main() -> int:
    if sys.platform != "darwin":
        die("must run on mac-mini (darwin). This cloud chat cannot remint Flow plates.")

    if not (Path.home() / "YouTube/orbit-with-ben").exists() and not REPO.exists():
        die("orbit-with-ben checkout not found")

    # 1) Lock replacement prompts
    rows = json.loads(PROMPTS.read_text())
    by_id = {r["id"]: r for r in rows}
    for pid, prompt in LOCKED_PROMPTS.items():
        if pid not in by_id:
            die(f"missing prompt id {pid}")
        by_id[pid]["prompt"] = prompt
        by_id[pid]["uat_regen"] = "tidal_plane_fail_2026-09-10"
    PROMPTS.write_text(json.dumps(rows, indent=2) + "\n")
    print(f"updated prompts {list(LOCKED_PROMPTS)}", flush=True)

    # 2) Quarantine old stems
    REJECT.mkdir(parents=True, exist_ok=True)
    moved = []
    for pid in REGEN_IDS:
        for f in sorted(PLATES.glob(f"{pid}_*.mp4")):
            dest = REJECT / f.name
            shutil.move(str(f), str(dest))
            moved.append(f.name)
    print(f"quarantined {len(moved)} → {REJECT}", flush=True)
    for m in moved:
        print(f"  - {m}", flush=True)

    # 3) Mint replacements (gen skips existing stems; we removed them)
    print("minting replacements via Flow CDP…", flush=True)
    r = subprocess.run([sys.executable, str(GEN)], cwd=str(HERE.parent))
    if r.returncode != 0:
        die(f"gen failed exit={r.returncode}")

    # Ensure each regen id has at least one plate
    missing = [pid for pid in REGEN_IDS if not list(PLATES.glob(f"{pid}_*.mp4"))]
    if missing:
        die(f"still missing plates after gen: {missing}")

    # 4) Assemble v02 (reuse assemble but override OUT via temp patch of env)
    # Prefer calling assemble then renaming, if assemble only writes v01.
    print("assembling rough…", flush=True)
    r = subprocess.run([sys.executable, str(ASM)], cwd=str(HERE.parent))
    if r.returncode != 0:
        die(f"assemble failed exit={r.returncode}")
    if not ROUGH_V01.exists():
        die(f"missing assemble out {ROUGH_V01}")

    shutil.copy2(ROUGH_V01, ROUGH_V02)
    meta_src = HERE / "parts/moon_leaving_part-03_rough_v01_meta.json"
    meta = {}
    if meta_src.exists():
        meta = json.loads(meta_src.read_text())
    meta.update(
        {
            "out": str(ROUGH_V02),
            "from": "v01 + regen tidal plates " + ",".join(REGEN_IDS),
            "uat_fix": "tidal_plane_fail_2026-09-10",
            "quarantined": moved,
        }
    )
    META_V02.write_text(json.dumps(meta, indent=2) + "\n")

    # 5) Copy to iCloud OWB UAT
    UAT.mkdir(parents=True, exist_ok=True)
    dest = UAT / "moon_leaving_part-03_rough_v02.mp4"
    shutil.copy2(ROUGH_V02, dest)
    STATUS.write_text(
        "OWB UAT — Moon Leaving Part 03\n"
        "================================\n"
        f"FILE: {dest.name}\n"
        "Status: rough v02 — regen after tidal water-plane UAT FAIL\n"
        "Leave v01 for compare. Do not remint Part 01/02 LOCKED.\n"
    )
    print(f"UAT {dest} ({dest.stat().st_size} bytes)", flush=True)
    print("DONE Part 03 rough v02", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
