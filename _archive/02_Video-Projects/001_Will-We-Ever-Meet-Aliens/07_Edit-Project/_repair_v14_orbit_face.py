#!/usr/bin/env python3
"""Re-render only Orbit-bearing shots with cleaned native-eye loops, then remux.

Keeps non-Orbit picture from the current master. Reuses the mysterious mix if present.
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

    polished_pool = build.orbit_assets()
    assert polished_pool, "no polished Orbit loops — run _make_polished_orbit_loops_v25.py"
    # Hero look = high-res present pose only (downscaled = crisp). Other poses as rare spice.
    hires = [p for p in polished_pool if "present_hires" in p.name]
    spice = [p for p in polished_pool if "present_hires" not in p.name]
    polished_pool = hires + spice  # hires first; round-robin still hits spice later
    if hires:
        # 4:1 hires:spice so most appearances match the polished reference
        polished_pool = hires * 4 + spice
    print(f"Orbit pool ({len(polished_pool)}): {[p.name for p in polished_pool[:8]]}...")
    orbit_i = 0

    with tempfile.TemporaryDirectory(prefix="orbit_face_fix_") as td:
        td = Path(td)
        parts: list[Path] = []
        for i, shot in enumerate(shots):
            part = td / f"part_{i:04d}.mp4"
            start = float(shot["start"])
            dur = float(shot["duration"])
            orbit = Path(shot["orbit"]) if shot.get("orbit") else None
            if orbit is not None and not orbit.exists():
                orbit = None
            # Re-render ALL cards (clears burned-in BR cover) + Orbit/CTA shots.
            # When Orbit is present, swap in polished large Overlay-Rig loops.
            wants_orbit = orbit is not None or (
                shot["kind"] in ("card", "cta") and shot.get("orbit")
            )
            # Cards that originally had orbit in EDL keep orbit; also promote every
            # Nth card to polished Orbit so companion presence stays frequent.
            rerender = shot["kind"] in ("card", "cta") or (
                orbit is not None and shot["kind"] != "brand"
            )
            if rerender:
                src = Path(shot["source"])
                use_orbit = None
                if shot["kind"] == "cta":
                    use_orbit = next(
                        (p for p in polished_pool if "wave" in p.name or "present" in p.name),
                        polished_pool[0],
                    )
                    print(f"[{i+1}/{len(shots)}] re-render cta {src.name} + {use_orbit.name}")
                    build.render_cta(part, use_orbit)
                elif shot.get("orbit") or (shot["kind"] == "card" and i % 2 == 0):
                    # Original orbit slots + every other card get polished Orbit
                    use_orbit = polished_pool[orbit_i % len(polished_pool)]
                    orbit_i += 1
                    print(f"[{i+1}/{len(shots)}] re-render {shot['kind']} {src.name} + {use_orbit.name}")
                    build.render_segment(src, part, dur, shot["kind"], use_orbit)
                else:
                    print(f"[{i+1}/{len(shots)}] re-render card {src.name} (no orbit)")
                    build.render_segment(src, part, dur, shot["kind"], None)
            else:
                print(f"[{i+1}/{len(shots)}] keep picture {start:.1f}+{dur:.1f}")
                run([
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-ss", f"{start:.6f}", "-t", f"{dur:.6f}", "-i", str(MASTER),
                    "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "17",
                    "-r", str(build.FPS), "-pix_fmt", "yuv420p", str(part),
                ])
            parts.append(part)

        concat = td / "concat.txt"
        concat.write_text("".join(f"file '{p}'\n" for p in parts))
        pic = td / "picture.mp4"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(concat),
            "-c:v", "libx264", "-preset", "fast", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", str(build.FPS), str(pic),
        ])

        audio = MIX if MIX.exists() else None
        if audio is None:
            # fall back to existing master audio
            run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(pic), "-i", str(MASTER),
                "-map", "0:v:0", "-map", "1:a:0",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
                "-shortest", "-movflags", "+faststart", str(OUT),
            ])
        else:
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
        # QC frame at 64s
        qc = ROOT / "09_Final-Export/_qc_orbit_64s.png"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", "64", "-i", str(OUT), "-frames:v", "1", str(qc),
        ])
        print(f"DONE → {OUT}")
        print(f"proof → {PROOF}")
        print(f"qc → {qc}")


if __name__ == "__main__":
    main()
