#!/usr/bin/env python3
"""Full picture rebuild: heal BR boxes on cards + animated Orbit on the right.

Re-renders every shot from source (no keep-from-master) so burned-in boxes die.
Uses Overlay-Rig blink loops only (never static hires stills).
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
EDIT = ROOT / "07_Edit-Project"
EDL = EDIT / "aliens_v14_full_cinematic_edl.json"
MASTER = ROOT / "09_Final-Export/aliens_v14_FULL_CINEMATIC_MASTER_18m50s_FINAL.mp4"
MIX = EDIT / "_mix_work_v14_full/final_mix.wav"
OUT = ROOT / "09_Final-Export/aliens_v14_FULL_CINEMATIC_MASTER_18m50s_FINAL.mp4"
OUT_ALIAS = ROOT / "09_Final-Export/aliens_v13_FULL_CINEMATIC_MASTER_18m50s_FINAL.mp4"
OUT_MUSIC = ROOT / "09_Final-Export/aliens_v14_FULL_CINEMATIC_MASTER_18m50s_MUSIC.mp4"
PROOF = ROOT / "09_Final-Export/aliens_v14_PROOF_orbit_face_fix_90s.mp4"

spec = importlib.util.spec_from_file_location("build", EDIT / "_build_v09_full_cinematic_master.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> None:
    data = json.loads(EDL.read_text())
    shots = data["edl"]
    assert MASTER.exists(), MASTER

    pool = build.orbit_assets()
    assert pool, "no animated Orbit loops"
    # Bias to present/neutral blink
    present = [p for p in pool if "present" in p.name]
    pool = (present * 3) + pool
    print("Animated Orbit pool:", sorted({p.name for p in pool}))
    orbit_i = 0

    with tempfile.TemporaryDirectory(prefix="orbit_anim_fix_") as td:
        td = Path(td)
        parts: list[Path] = []
        for i, shot in enumerate(shots):
            part = td / f"part_{i:04d}.mp4"
            src = Path(shot["source"])
            dur = float(shot["duration"])
            kind = shot["kind"]

            if kind == "brand":
                # Brand intro — copy from master (no BR box / no orbit issue)
                run([
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-ss", f"{float(shot['start']):.6f}", "-t", f"{dur:.6f}",
                    "-i", str(MASTER),
                    "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "17",
                    "-r", str(build.FPS), "-pix_fmt", "yuv420p", str(part),
                ])
                print(f"[{i+1}/{len(shots)}] keep brand")
                parts.append(part)
                continue

            if kind == "cta":
                use = present[0] if present else pool[0]
                print(f"[{i+1}/{len(shots)}] cta + {use.name}")
                build.render_cta(part, use)
                parts.append(part)
                continue

            # Cards + broll: always re-render from source
            # Orbit on: original orbit slots, all cards, and every other broll
            want_orbit = bool(shot.get("orbit")) or kind == "card" or (kind == "broll" and i % 2 == 0)
            use = None
            if want_orbit:
                use = pool[orbit_i % len(pool)]
                orbit_i += 1
            print(
                f"[{i+1}/{len(shots)}] {kind} {src.name}"
                + (f" + {use.name}" if use else " (no orbit)")
            )
            build.render_segment(src, part, dur, kind if kind in ("card", "broll") else "broll", use)
            parts.append(part)

        concat = td / "concat.txt"
        concat.write_text("".join(f"file '{p}'\n" for p in parts))
        pic = td / "picture.mp4"
        print("Concat picture…")
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(concat),
            "-c:v", "libx264", "-preset", "fast", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", str(build.FPS), str(pic),
        ])

        audio = MIX if MIX.exists() else MASTER
        print("Mux audio…")
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(pic), "-i", str(audio),
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
            "-shortest", "-movflags", "+faststart", str(OUT),
        ])
        run(["cp", str(OUT), str(OUT_ALIAS)])
        run(["cp", str(OUT), str(OUT_MUSIC)])
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(OUT), "-t", "90", "-c", "copy", str(PROOF),
        ])

        # QC
        for t in (20, 47, 64):
            qc = ROOT / f"09_Final-Export/_qc_animfix_{t}s.png"
            run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", str(t), "-i", str(OUT), "-frames:v", "1", str(qc),
            ])
        print(f"DONE → {OUT}")
        print(f"proof → {PROOF}")


if __name__ == "__main__":
    main()
