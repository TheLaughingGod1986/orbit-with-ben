#!/usr/bin/env python3
"""Sun 022 cut v04 (J0019), on Claude's v03 PASS (#99 6045620003).

Changes from v03, everything else is the v03 assembler:
- Row 8: off PIA22123 (repeated rows 10/11) onto GSFC e001936, filament eruption at the limb.
- Row 49: off PIA22360 (repeated row 37) onto GSFC e000923, white-light disc (HMI quick-look
  label masked).
- Row 50: off PIA15377 (repeated row 38) onto GSFC e000790, full SDO disc.
- Row 14: zoom_nolabels.mp4 in at 8.0 s, so the zoom-out lands on the slow rising line under
  "by a slow rise in the light of the whole star" (v03 sat on the 0-4 s wobble).

Media stays out of git: output goes to iCloud OWB UAT/sun_first_cut_v04/.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("v03", HERE / "_assemble_sun_first_cut_v03.py")
v3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v3)
v1, sat = v3.v1, v3.sat

WORK = HERE / "sun_film/work_first_cut_v04"
OUT_LOCAL = HERE / "sun_film/sun_first_cut_v04.mp4"
UAT_DIR = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/sun_first_cut_v04")
SWAP = {
    8: "GSFC_20171208_Archive_e001936",
    49: "GSFC_20171208_Archive_e000923",
    50: "GSFC_20171208_Archive_e000790",
}
ROW14_IN = 8.0

v3.WORK_V02 = v3.WORK
v3.WORK = WORK
v1.WORK = WORK
sat.WORK = WORK
v3.OUT_LOCAL = OUT_LOCAL
v1.OUT_LOCAL = OUT_LOCAL
v3.UAT_DIR = UAT_DIR
v3.REBUILD_ROWS = {*SWAP, 14}
v3.CODE_IN[14] = ROW14_IN
v3.MASKS["GSFC_20171208_Archive_e000923"] = (0, 975, 340, 1015)

_build_row = v1.build_row


def build_row(r: dict, pool: dict, dest: Path, uses: dict) -> None:
    row = int(r["row"])
    if row in SWAP:
        v1.NOTES.append(f"row {row}: {r['id'].strip()} repeated an earlier row, swapped to {SWAP[row]}")
        r = {**r, "id": SWAP[row]}
    _build_row(r, pool, dest, uses)


v1.build_row = build_row

_chunk = sat.chunk_write


def chunk_write(src, dest):
    return _chunk(src, Path(dest).with_name(Path(dest).name.replace("_v03", "_v04")))


sat.chunk_write = chunk_write


def main() -> None:
    v3.main()
    meta_path = WORK / "META.json"
    meta = json.loads(meta_path.read_text())
    meta.update({"cut": "sun_first_cut_v04", "swaps": {str(k): v for k, v in SWAP.items()},
                 "row14_in_s": ROW14_IN})
    meta_path.write_text(json.dumps(meta, indent=2))
    _chunk(json.dumps(meta, indent=2).encode(), UAT_DIR / "ARRIVAL.json")
    print("V04", json.dumps(meta, indent=2), flush=True)


if __name__ == "__main__":
    sys.exit(main())
