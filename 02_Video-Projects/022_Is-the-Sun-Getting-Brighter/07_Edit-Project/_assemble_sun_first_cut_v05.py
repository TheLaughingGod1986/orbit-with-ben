#!/usr/bin/env python3
"""Sun 022 cut v05 (J0024).

One change from v04, everything else is the v04 assembler:
- Row 49: off GSFC e000923 (a big sunspot group) onto PIA22646 ("An Almost Spotless Record",
  SDO HMI, Jul 2018), a near-spotless visible-light disc. Sunspot pictures only go on the
  wobble lines; this row is "Almost nothing at first, then a sun about 1% more...".
  Its burnt-in date (bottom left, on black sky) is masked the same way as PIA21218.

Media stays out of git: output goes to iCloud OWB UAT/sun_first_cut_v05/.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("v04", HERE / "_assemble_sun_first_cut_v04.py")
v4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v4)
v3, v1, sat = v4.v3, v4.v1, v4.sat

WORK = HERE / "sun_film/work_first_cut_v05"
OUT_LOCAL = HERE / "sun_film/sun_first_cut_v05.mp4"
UAT_DIR = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/sun_first_cut_v05")
ROW49 = "PIA22646"

v4.SWAP[49] = ROW49
v3.WORK_V02 = v4.WORK
v3.WORK = WORK
v1.WORK = WORK
sat.WORK = WORK
v3.OUT_LOCAL = OUT_LOCAL
v1.OUT_LOCAL = OUT_LOCAL
v3.UAT_DIR = UAT_DIR
v3.REBUILD_ROWS = {49}
v3.MASKS[ROW49] = (0, 1575, 440, 1635)

_chunk = sat.chunk_write


def chunk_write(src, dest):
    return _chunk(src, Path(dest).with_name(Path(dest).name.replace("_v04", "_v05")))


sat.chunk_write = chunk_write


def main() -> None:
    v3.main()
    meta_path = WORK / "META.json"
    meta = json.loads(meta_path.read_text())
    meta.update({"cut": "sun_first_cut_v05", "swaps": {str(k): v for k, v in v4.SWAP.items()},
                 "row14_in_s": v4.ROW14_IN,
                 "v05_change": f"row 49: GSFC_20171208_Archive_e000923 (sunspot group) -> {ROW49}"})
    meta_path.write_text(json.dumps(meta, indent=2))
    sat.chunk_write(json.dumps(meta, indent=2).encode(), UAT_DIR / "ARRIVAL.json")
    print("V05", json.dumps(meta, indent=2), flush=True)


if __name__ == "__main__":
    sys.exit(main())
