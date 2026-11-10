#!/usr/bin/env python3
"""Build a clean review cut with one stable, professionally animated Orbit.

This is intentionally additive: previous exports, EDLs, cards, and source
assets are never overwritten.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile


ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
EDIT = ROOT / "07_Edit-Project"
BASE_BUILD = EDIT / "_build_broadcast_noloop_v02.py"
PREP = EDIT / "_prepare_orbit_overlay_rig_v21.py"
RIG = Path("/Users/ben/code/Orbit-YouTube/01_Orbit-Character/06_Animation-Exports/Overlay-Rig-v01/orbit_overlay_idle-blink_6s_v01.mov")
CACHED_BED = EDIT / "_render_cache_v21/picture_bed_no_orbit.mp4"
VO = ROOT / "02_Voiceover/05_Master/aliens_voiceover_master_storyteller_v04.wav"
MIX = EDIT / "_mix_work_v19/final_mix.wav"
MIX_FALLBACK = EDIT / "_mix_work_v16/final_mix.wav"
EDL_OUT = EDIT / "SECTION_EDL_v21_stable_orbit.json"
OUT_PIC = ROOT / "09_Final-Export/aliens_broadcast_v21_stable_orbit_pic.mp4"
OUT = ROOT / "09_Final-Export/aliens_broadcast_v21_stable_orbit.mp4"
PROOF = ROOT / "09_Final-Export/aliens_v21_PROOF_stable_orbit_90s.mp4"

spec = importlib.util.spec_from_file_location("orbit_base", BASE_BUILD)
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


def mux(pic: Path, audio: Path, out: Path, duration: float | None = None) -> None:
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(pic), "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
    ]
    cmd += ["-t", f"{duration:.3f}"] if duration is not None else ["-shortest"]
    cmd.append(str(out))
    subprocess.run(cmd, check=True)


def render_bed(shots: list[dict], td: Path) -> Path:
    parts: list[Path] = []
    for i, shot in enumerate(shots):
        part = td / f"p_{i:04d}.mp4"
        dur = float(shot["duration_s"])
        stable = shot["kind"] in ("card", "chapter", "brand_intro", "brand_outro")
        b.render_once(shot["path"], dur, part, stable_text=stable, motion_seed=i)
        parts.append(part)
        if i and i % 25 == 0:
            print(f"  rendered {i}/{len(shots)}")
    listing = td / "concat.txt"
    listing.write_text("".join(f"file '{p}'\n" for p in parts))
    bed = td / "bed.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(listing),
        "-c", "copy", str(bed),
    ], check=True)
    return bed


def merge_intervals(shots: list[dict]) -> list[tuple[float, float]]:
    """Continuous b-roll runs only; text cards remain clean and readable."""
    spans = []
    for shot in shots:
        if shot["kind"] != "broll":
            continue
        start = float(shot["start_s"])
        spans.append((start, start + float(shot["duration_s"])))
    if not spans:
        return []
    merged = [list(spans[0])]
    for start, end in spans[1:]:
        if start <= merged[-1][1] + 0.08:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [(a, z) for a, z in merged if z - a >= 1.0]


def compose(bed: Path, shots: list[dict], output: Path, timeline: float) -> None:
    spans = merge_intervals(shots)
    if not spans:
        raise RuntimeError("No b-roll spans found for Orbit overlay")
    enable = "+".join(f"between(t\\,{a:.3f}\\,{z:.3f})" for a, z in spans)
    # Fixed lower-right home.  Movement is deliberately below the threshold
    # that reads as repositioning: ±6 px sideways and ±10 px vertically.
    x = "W-w-74+6*sin(2*PI*t/7.2)"
    y = "H-h-54+10*cos(2*PI*t/5.8)"
    fc = EDIT / "_orbit_fc_v21.txt"
    fc.write_text(
        "[1:v]setpts=PTS-STARTPTS,format=yuva444p10le[orbit];\n"
        f"[0:v][orbit]overlay=x='{x}':y='{y}':format=auto:"
        f"alpha=straight:eof_action=repeat:enable='{enable}'[v]\n"
    )
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(bed), "-stream_loop", "-1", "-i", str(RIG),
        "-filter_complex_script", str(fc),
        "-map", "[v]", "-an", "-t", f"{timeline:.3f}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        str(output),
    ], check=True)


def trim_shots(shots: list[dict], duration: float) -> list[dict]:
    out = []
    for shot in shots:
        start = float(shot["start_s"])
        if start >= duration:
            break
        item = dict(shot)
        item["duration_s"] = min(float(item["duration_s"]), duration - start)
        out.append(item)
    return out


def save_edl(shots: list[dict], timeline: float) -> None:
    EDL_OUT.write_text(json.dumps({
        "version": 21,
        "rules": [
            "single_fixed_lower_right_home",
            "full_resolution_clean_overlay",
            "orbit_hidden_on_text_and_brand_cards",
            "transparent_prores_idle_blink_loop",
            "old_exports_preserved",
        ],
        "timeline_s": round(timeline, 3),
        "overlay_rig": str(RIG),
        "output": str(OUT),
        "shots": [{
            "kind": shot["kind"],
            "clip": Path(shot["path"]).name,
            "start_s": round(float(shot["start_s"]), 3),
            "duration_s": round(float(shot["duration_s"]), 3),
        } for shot in shots],
    }, indent=2))


def build(mode: str) -> None:
    python = "/Users/ben/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
    subprocess.run([python, str(PREP)], check=True)
    timeline = b.probe(VO)
    prior = json.loads((EDIT / "SECTION_EDL_v10_clean_cuts.json").read_text())
    markers = prior["markers"]
    pool = b.collect_unique_clips()
    shots, _, _ = b.build_edl(timeline, pool, markers)

    duration = 90.0 if mode == "proof" else timeline
    selected = trim_shots(shots, duration)
    with tempfile.TemporaryDirectory(prefix="orbit_v21_") as temp:
        td = Path(temp)
        if mode != "proof" and CACHED_BED.exists() and b.probe(CACHED_BED) >= duration - 0.1:
            bed = CACHED_BED
            print(f"using preserved clean picture bed: {CACHED_BED}")
        else:
            bed = render_bed(selected, td)
        picture = td / "picture.mp4" if mode == "proof" else OUT_PIC
        compose(bed, selected, picture, duration)
        audio = MIX if MIX.exists() else (MIX_FALLBACK if MIX_FALLBACK.exists() else VO)
        target = PROOF if mode == "proof" else OUT
        mux(picture, audio, target, duration=duration)
    save_edl(shots, timeline)
    print(target)


if __name__ == "__main__":
    import sys
    build(sys.argv[1] if len(sys.argv) > 1 else "proof")
