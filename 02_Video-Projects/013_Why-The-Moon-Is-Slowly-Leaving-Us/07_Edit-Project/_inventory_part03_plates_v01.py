#!/usr/bin/env python3
"""Inventory Part 03 Flow world plates on disk (Mac mini). No remint. No freeze-pad."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
OUT = PROJ / "04_Generated-Clips/part03/flow_world_v01"
PROMPTS = HERE / "parts/part-03_flow_prompts_v01.json"
REPORT = OUT / "_inventory_v01.json"
VO_TARGET_S = 136.7
NEED_PLATES = 18


def probe(path: Path) -> float:
    try:
        return float(
            subprocess.check_output(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "default=nw=1:nk=1",
                    str(path),
                ],
                text=True,
            ).strip()
        )
    except Exception:
        return 0.0


def main() -> int:
    prompts = json.loads(PROMPTS.read_text()) if PROMPTS.exists() else []
    prompt_ids = [p["id"] for p in prompts]
    OUT.mkdir(parents=True, exist_ok=True)
    plates = sorted(
        [p for p in OUT.glob("*.mp4") if p.stat().st_size > 200_000],
        key=lambda p: p.name,
    )
    rows = []
    total = 0.0
    stems_present = set()
    for p in plates:
        dur = probe(p)
        total += dur
        stem = p.name.split("_")[0] if "_" in p.name else p.stem
        stems_present.add(stem)
        rows.append({"file": p.name, "bytes": p.stat().st_size, "seconds": round(dur, 3)})
    missing = [pid for pid in prompt_ids if not any(p.name.startswith(pid + "_") for p in plates)]
    report = {
        "out": str(OUT),
        "have_plates": len(plates),
        "need_plates": NEED_PLATES,
        "unique_prompt_stems_present": sorted(stems_present),
        "missing_prompt_ids": missing,
        "total_seconds": round(total, 3),
        "vo_target_seconds": VO_TARGET_S,
        "coverage_ok_no_freeze_pad": len(plates) >= NEED_PLATES and total >= VO_TARGET_S - 2.0,
        "plates": rows,
        "do_not_remint": ["part01_LOCKED_v04", "part02_LOCKED_v01"],
        "freeze_pad": "forbidden",
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    print(f"WROTE {REPORT}", flush=True)
    if report["coverage_ok_no_freeze_pad"]:
        print("READY_TO_ASSEMBLE", flush=True)
        return 0
    print("NOT_READY — mint remaining plates first", flush=True)
    return 2


if __name__ == "__main__":
    sys.exit(main())
