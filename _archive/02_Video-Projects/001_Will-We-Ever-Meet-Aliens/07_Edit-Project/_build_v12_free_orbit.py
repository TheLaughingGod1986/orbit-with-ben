#!/usr/bin/env python3
"""Rebuild picture with free-flying transparent Orbit + emotion beats → v14.

Reuses v10 EDL shots + v11 cinematic mix audio.
"""
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
MIX = ROOT / "07_Edit-Project/_mix_work_v11/final_mix.wav"
OUT_PIC = ROOT / "09_Final-Export/aliens_broadcast_v14_orbit_broll_only_pic.mp4"
OUT = ROOT / "09_Final-Export/aliens_broadcast_v14_orbit_broll_only.mp4"
PROOF = ROOT / "09_Final-Export/aliens_v14_PROOF_orbit_broll_90s.mp4"

spec = importlib.util.spec_from_file_location("b", BUILD)
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


def resolve_clip(name: str) -> Path:
    candidates = [
        b.CARDS / name, b.CHAPTERS / name, b.BRAND / name,
        b.MYSTERY / name, b.VIBRANT / name, b.BROLL / name, b.POLISHED / name,
    ]
    path = next((p for p in candidates if p.exists()), None)
    if path is None:
        hits = list(b.POLISHED.rglob(name))
        path = hits[0] if hits else None
    assert path is not None, name
    return path


def build_bed(shots: list[dict], td: Path) -> tuple[Path, list[dict]]:
    parts = []
    edl_shots = []
    for i, s in enumerate(shots):
        path = resolve_clip(s["clip"])
        kind = s["kind"]
        part = td / f"p_{i:04d}.mp4"
        dur = float(s["duration_s"])
        stable = kind in ("card", "chapter", "brand_intro", "brand_outro")
        b.render_once(path, dur, part, stable_text=stable)
        parts.append(part)
        edl_shots.append({
            "kind": kind, "path": path, "start_s": float(s["start_s"]),
            "duration_s": dur, "section": s.get("section"), "orbit": s.get("orbit"),
        })
        if i % 30 == 0:
            print(f"  rendered {i}/{len(shots)}")
    lst = td / "list.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    bed = td / "bed.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(bed),
    ], check=True)
    return bed, edl_shots


def mux_mix(pic: Path, audio: Path, out: Path, dur: float | None = None) -> None:
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(pic), "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart",
        str(out),
    ]
    if dur is not None:
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(pic), "-i", str(audio),
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-t", f"{dur:.3f}", "-movflags", "+faststart",
            str(out),
        ]
    subprocess.run(cmd, check=True)


def proof_90s(data: dict) -> None:
    """Quick watchable proof covering brand + cold open + chapter + galaxy start."""
    shots = [s for s in data["shots"] if float(s["start_s"]) < 90.0]
    # clip last shot to end at 90
    last = dict(shots[-1])
    end = float(last["start_s"]) + float(last["duration_s"])
    if end > 90:
        last["duration_s"] = 90.0 - float(last["start_s"])
        shots[-1] = last
    markers = [m for m in data["markers"] if float(m["start_s"]) < 90]
    print(f"PROOF: {len(shots)} shots, {len(markers)} markers")
    with tempfile.TemporaryDirectory(prefix="orbit_v14_proof_") as td:
        td = Path(td)
        bed, edl_shots = build_bed(shots, td)
        pic = td / "pic.mp4"
        print("compositing free Orbit…")
        b.compose_flying_orbit(bed, VO, edl_shots, markers, pic, 90.0)
        audio = MIX if MIX.exists() else VO
        mux_mix(pic, audio, PROOF, dur=90.0)
    print(f"PROOF → {PROOF}")


def full_build(data: dict) -> None:
    markers = data["markers"]
    vo_dur = b.probe(VO)
    print(f"FULL: {len(data['shots'])} shots, vo={vo_dur:.1f}s")
    with tempfile.TemporaryDirectory(prefix="orbit_v14_full_") as td:
        td = Path(td)
        bed, edl_shots = build_bed(data["shots"], td)
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
        print("compositing free Orbit (full)…")
        b.compose_flying_orbit(bed, VO, edl_shots, markers, OUT_PIC, timeline)
        audio = MIX if MIX.exists() else VO
        print("muxing cinematic mix…")
        mux_mix(OUT_PIC, audio, OUT)
    print(json.dumps({
        "out": str(OUT),
        "duration_s": round(b.probe(OUT), 3),
        "free_orbit": True,
        "emotion_beats": True,
    }, indent=2))


def main() -> None:
    import sys
    data = json.loads(EDL.read_text())
    mode = sys.argv[1] if len(sys.argv) > 1 else "proof"
    if mode == "full":
        full_build(data)
    else:
        proof_90s(data)


if __name__ == "__main__":
    main()
