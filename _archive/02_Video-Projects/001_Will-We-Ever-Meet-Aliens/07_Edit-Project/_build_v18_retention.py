#!/usr/bin/env python3
"""v20 Orbit-life rebuild — stable corner companion + logo-free cards.

Picture: Ken Burns B-roll, mystery-first cards, living Orbit (hover + sparse faces).
Audio: cinematic mix v19.
"""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
import importlib.util

ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
EDIT = ROOT / "07_Edit-Project"
BUILD = EDIT / "_build_broadcast_noloop_v02.py"
VO = ROOT / "02_Voiceover/05_Master/aliens_voiceover_master_storyteller_v04.wav"
MIX = EDIT / "_mix_work_v19/final_mix.wav"
MIX_FALLBACK = EDIT / "_mix_work_v16/final_mix.wav"
MARKERS_FALLBACK = EDIT / "VO_MARKERS_v08.json"
EDL_OUT = EDIT / "SECTION_EDL_v21_orbit_anim.json"
OUT_PIC = ROOT / "09_Final-Export/aliens_broadcast_v21_orbit_anim_pic.mp4"
OUT = ROOT / "09_Final-Export/aliens_broadcast_v21_orbit_anim.mp4"
PROOF = ROOT / "09_Final-Export/aliens_v21_PROOF_orbit_anim_90s.mp4"
# Also refresh the “current watch” files
OUT_LATEST = ROOT / "09_Final-Export/aliens_broadcast_v19_cinematic_mix.mp4"
OUT_RETENTION = ROOT / "09_Final-Export/aliens_broadcast_v20_orbit_life.mp4"

spec = importlib.util.spec_from_file_location("b", BUILD)
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


def mux(pic: Path, audio: Path, out: Path, dur: float | None = None) -> None:
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(pic), "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
    ]
    if dur is not None:
        cmd += ["-t", f"{dur:.3f}"]
    else:
        cmd += ["-shortest"]
    cmd.append(str(out))
    subprocess.run(cmd, check=True)


def render_edl(edl_shots: list[dict], td: Path) -> Path:
    parts = []
    for i, shot in enumerate(edl_shots):
        part = td / f"p_{i:04d}.mp4"
        dur = float(shot["duration_s"])
        stable = shot["kind"] in ("card", "chapter", "brand_intro", "brand_outro")
        b.render_once(shot["path"], dur, part, stable_text=stable, motion_seed=i)
        parts.append(part)
        if i % 25 == 0:
            print(f"  rendered {i}/{len(edl_shots)}")
    lst = td / "list.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    bed = td / "bed.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(bed),
    ], check=True)
    return bed


def compose(bed: Path, edl_shots: list[dict], markers: list[dict], out: Path, timeline: float) -> None:
    print("compositing left-corner expressive Orbit…")
    b.compose_flying_orbit(bed, VO, edl_shots, markers, out, timeline)


def build_picture(markers: list[dict], timeline: float, out_pic: Path) -> list[dict]:
    pool = b.collect_unique_clips()
    print(f"clip pool {len(pool)}")
    edl, pic_dur, used = b.build_edl(timeline, pool, markers)
    # build_edl returns (edl, t, used) — verify
    if isinstance(edl, tuple):
        # older signature safety
        pass
    print(f"EDL shots {len(edl)} picture~{pic_dur:.1f}s unique {len(used)}")
    with tempfile.TemporaryDirectory(prefix="orbit_v18_") as td:
        td = Path(td)
        bed = render_edl(edl, td)
        bed_dur = b.probe(bed)
        if bed_dur < timeline - 0.05:
            pad = timeline - bed_dur
            padded = td / "bed_pad.mp4"
            subprocess.run([
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(bed),
                "-vf", f"tpad=stop_mode=clone:stop_duration={pad:.3f}",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(padded),
            ], check=True)
            bed = padded
        compose(bed, edl, markers, out_pic, max(timeline, b.probe(bed)))
    return edl


def save_edl(edl: list[dict], markers: list[dict]) -> None:
    serial = []
    for e in edl:
        serial.append({
            "kind": e["kind"],
            "clip": Path(e["path"]).name if not isinstance(e["path"], str) else Path(e["path"]).name,
            "section": e.get("section"),
            "start_s": round(float(e["start_s"]), 3),
            "duration_s": round(float(e["duration_s"]), 3),
            "orbit": e.get("orbit"),
        })
    EDL_OUT.write_text(json.dumps({
        "rules": [
            "retention_v18", "mystery_first_hook", "wonder_ending",
            "ken_burns_broll", "orbit_bottom_left_companion",
            "chapter_cards_between_sections", "hq_broll_only",
        ],
        "markers": markers,
        "vo": str(VO),
        "shots": serial,
        "out": str(OUT),
    }, indent=2))


def proof_from_edl(edl: list[dict], markers: list[dict]) -> None:
    shots = [s for s in edl if float(s["start_s"]) < 90]
    last = dict(shots[-1])
    end = float(last["start_s"]) + float(last["duration_s"])
    if end > 90:
        last["duration_s"] = 90.0 - float(last["start_s"])
        shots[-1] = last
    mk = [m for m in markers if float(m["start_s"]) < 90]
    print(f"PROOF: {len(shots)} shots")
    with tempfile.TemporaryDirectory(prefix="orbit_v18_proof_") as td:
        td = Path(td)
        bed = render_edl(shots, td)
        pic = td / "pic.mp4"
        compose(bed, shots, mk, pic, 90.0)
        audio = MIX if MIX.exists() else (MIX_FALLBACK if MIX_FALLBACK.exists() else VO)
        mux(pic, audio, PROOF, dur=90.0)
    print(f"PROOF → {PROOF}")


def main() -> None:
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "proof"

    # Prefer markers from prior EDL (matched to storyteller master)
    prior = EDIT / "SECTION_EDL_v10_clean_cuts.json"
    if prior.exists():
        data = json.loads(prior.read_text())
        markers = data["markers"]
    else:
        markers = json.loads(MARKERS_FALLBACK.read_text())

    vo_dur = b.probe(VO)
    timeline = vo_dur
    print(f"VO {vo_dur:.1f}s — building retention EDL…")

    if mode == "proof":
        # Full EDL then trim — keeps opening accurate
        pool = b.collect_unique_clips()
        edl, pic_dur, used = b.build_edl(timeline, pool, markers)
        print(f"EDL {len(edl)} shots (~{pic_dur:.1f}s)")
        # resolve Path objects already on edl
        proof_from_edl(edl, markers)
        return

    edl = build_picture(markers, timeline, OUT_PIC)
    save_edl(edl, markers)
    audio = MIX if MIX.exists() else (MIX_FALLBACK if MIX_FALLBACK.exists() else VO)
    print("muxing polished mix…")
    mux(OUT_PIC, audio, OUT)
    mux(OUT_PIC, audio, OUT_LATEST)
    mux(OUT_PIC, audio, OUT_RETENTION)
    # also proof
    proof_from_edl(edl, markers)
    print(json.dumps({
        "out": str(OUT),
        "duration_s": round(b.probe(OUT), 3),
        "edl": str(EDL_OUT),
        "orbit_anim_v21": True,
    }, indent=2))


if __name__ == "__main__":
    main()
