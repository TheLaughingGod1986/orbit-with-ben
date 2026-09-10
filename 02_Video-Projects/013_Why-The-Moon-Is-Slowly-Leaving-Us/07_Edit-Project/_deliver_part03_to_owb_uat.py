#!/usr/bin/env python3
"""One-shot Mac deliver: assemble Part 03 (if plates ready) → OWB UAT iCloud.

Run on Mac mini only:
  python3 07_Edit-Project/_deliver_part03_to_owb_uat.py

Does not remint Part 01/02. No freeze-pad. Copies STATUS always.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT"
# Also drop beside repo for non-iCloud sync
REPO_UAT = PROJ.parents[1] / "OWB UAT"
STATUS_SRC = HERE / "parts/moon_leaving_part-03_STATUS.txt"
INV = HERE / "_inventory_part03_plates_v01.py"
ASM = HERE / "_assemble_part03_rough_v01.py"
ROUGH = HERE / "parts/moon_leaving_part-03_rough_v01.mp4"


def main() -> int:
    if sys.platform != "darwin":
        print("ABORT: run on Mac mini (darwin). This delivers to iCloud OWB UAT.", flush=True)
        return 2

    UAT.mkdir(parents=True, exist_ok=True)
    REPO_UAT.mkdir(parents=True, exist_ok=True)

    # Always refresh STATUS into UAT
    status_body = STATUS_SRC.read_text() if STATUS_SRC.exists() else "Part 03 STATUS missing\n"
    for dest_dir in (UAT, REPO_UAT):
        (dest_dir / "moon_leaving_part-03_STATUS.txt").write_text(status_body)

    print("Running inventory…", flush=True)
    inv = subprocess.run([sys.executable, str(INV)], cwd=str(HERE.parent))
    print("Running assemble…", flush=True)
    asm = subprocess.run([sys.executable, str(ASM)], cwd=str(HERE.parent))

    if asm.returncode != 0 or not ROUGH.exists():
        note = (
            "Part 03 rough NOT ready for full UAT.\n"
            "Inventory/assemble failed or plates short (freeze-pad forbidden).\n"
            "STATUS copied to OWB UAT. Mint remaining plates then re-run this script.\n"
        )
        for dest_dir in (UAT, REPO_UAT):
            (dest_dir / "moon_leaving_part-03_NOT_READY.txt").write_text(note)
        print(note, flush=True)
        print(f"STATUS → {UAT / 'moon_leaving_part-03_STATUS.txt'}", flush=True)
        return asm.returncode or inv.returncode or 2

    dest = UAT / "moon_leaving_part-03_rough_v01.mp4"
    shutil.copy2(ROUGH, dest)
    shutil.copy2(ROUGH, REPO_UAT / dest.name)
    # clear not-ready flag
    for dest_dir in (UAT, REPO_UAT):
        p = dest_dir / "moon_leaving_part-03_NOT_READY.txt"
        if p.exists():
            p.unlink()
    print(f"UAT {dest} ({dest.stat().st_size} bytes)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
