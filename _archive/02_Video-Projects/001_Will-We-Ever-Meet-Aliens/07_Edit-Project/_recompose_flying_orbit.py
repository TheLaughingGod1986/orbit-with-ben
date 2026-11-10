#!/usr/bin/env python3
"""Fast recompose: rebuild picture bed from EDL + flying Orbit (reuse VO)."""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

import importlib.util

ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
BUILD = ROOT / "07_Edit-Project/_build_broadcast_noloop_v02.py"
EDL = ROOT / "07_Edit-Project/SECTION_EDL_v10_clean_cuts.json"
VO = ROOT / "02_Voiceover/05_Master/aliens_voiceover_master_storyteller_v04.wav"
OUT = ROOT / "09_Final-Export/aliens_broadcast_v10_clean_cuts.mp4"

spec = importlib.util.spec_from_file_location("b", BUILD)
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


def main():
    data = json.loads(EDL.read_text())
    markers = data["markers"]
    assert VO.exists(), VO
    vo_dur = b.probe(VO)

    with tempfile.TemporaryDirectory(prefix="orbit_fly_") as td:
        td = Path(td)
        parts = []
        edl_shots = []
        for i, s in enumerate(data["shots"]):
            # resolve path
            name = s["clip"]
            kind = s["kind"]
            candidates = [
                b.CARDS / name,
                b.CHAPTERS / name,
                b.BRAND / name,
                b.MYSTERY / name,
                b.VIBRANT / name,
                b.BROLL / name,
                b.POLISHED / name,
            ]
            path = next((p for p in candidates if p.exists()), None)
            if path is None:
                # try recursive
                hits = list(b.POLISHED.rglob(name))
                path = hits[0] if hits else None
            assert path is not None, name
            part = td / f"p_{i:04d}.mp4"
            dur = float(s["duration_s"])
            stable = kind in ("card", "chapter", "brand_intro", "brand_outro")
            b.render_once(path, dur, part, stable_text=stable)
            parts.append(part)
            edl_shots.append({
                "kind": kind, "path": path, "start_s": float(s["start_s"]),
                "duration_s": dur, "section": s.get("section"), "orbit": s.get("orbit"),
            })
            if i % 40 == 0:
                print(f"rendered {i}/{len(data['shots'])}")

        lst = td / "list.txt"
        lst.write_text("".join(f"file '{p}'\n" for p in parts))
        bed = td / "bed.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(bed),
        ], check=True)
        bed_dur = b.probe(bed)
        if bed_dur < vo_dur - 0.05:
            pad = vo_dur - bed_dur
            padded = td / "bed_pad.mp4"
            subprocess.run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(bed),
                "-vf", f"tpad=stop_mode=clone:stop_duration={pad:.3f}",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(padded),
            ], check=True)
            bed = padded

        timeline = max(vo_dur, b.probe(bed))
        print("compositing flying Orbit…")
        b.compose_flying_orbit(bed, VO, edl_shots, markers, OUT, timeline)
        print(json.dumps({"out": str(OUT), "duration_s": round(b.probe(OUT), 3)}, indent=2))


if __name__ == "__main__":
    main()
