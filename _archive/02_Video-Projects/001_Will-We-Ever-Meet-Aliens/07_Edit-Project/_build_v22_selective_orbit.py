#!/usr/bin/env python3
"""Build the selective-host Orbit cut.

Orbit appears once per narrative section, always at the same lower-right
anchor.  Each entrance and exit is alpha-faded so the mascot never pops at a
scene boundary.  v21 and all earlier exports remain untouched.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess


ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
EDIT = ROOT / "07_Edit-Project"
BED = EDIT / "_render_cache_v21/picture_bed_no_orbit.mp4"
RIG = Path("/Users/ben/code/Orbit-YouTube/01_Orbit-Character/06_Animation-Exports/Overlay-Rig-v01/orbit_overlay_idle-blink_6s_v01.mov")
MIX = EDIT / "_mix_work_v19/final_mix.wav"
OUT_PIC = ROOT / "09_Final-Export/aliens_broadcast_v22_selective_orbit_pic.mp4"
OUT = ROOT / "09_Final-Export/aliens_broadcast_v22_selective_orbit.mp4"
PROOF = ROOT / "09_Final-Export/aliens_v22_PROOF_selective_orbit_90s.mp4"
MANIFEST = EDIT / "ORBIT_APPEARANCES_v22.json"
TIMELINE = 635.475
FADE = 0.28

# One deliberate host beat per section.  Every window sits wholly inside a
# verified B-roll run, so the mascot never overlaps a text or chapter card.
APPEARANCES = [
    {"section": "01_cold-open",      "start": 24.990,  "end": 28.636,  "purpose": "first host reveal"},
    {"section": "02_galaxy-scale",   "start": 63.728,  "end": 69.334,  "purpose": "scale reaction"},
    {"section": "03_exoplanets",     "start": 117.843, "end": 125.843, "purpose": "habitable-world guide"},
    {"section": "04_fermi-paradox",  "start": 173.900, "end": 176.700, "purpose": "silence reaction"},
    {"section": "05_great-filter",   "start": 241.742, "end": 249.742, "purpose": "reflective host beat"},
    {"section": "06_explanations",   "start": 323.168, "end": 331.168, "purpose": "theory guide"},
    {"section": "07_detection",      "start": 417.616, "end": 425.616, "purpose": "discovery beat"},
    {"section": "08_first-contact",  "start": 487.235, "end": 495.235, "purpose": "contact reaction"},
    {"section": "09_conclusion",     "start": 614.900, "end": 618.500, "purpose": "warm reflection"},
]


def probe(path: Path) -> float:
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ], capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def selected_for(duration: float) -> list[dict]:
    return [
        {**item, "end": min(float(item["end"]), duration)}
        for item in APPEARANCES
        if float(item["start"]) < duration and min(float(item["end"]), duration) - float(item["start"]) >= 0.8
    ]


def compose(duration: float, output: Path) -> list[dict]:
    appearances = selected_for(duration)
    labels = "".join(f"[o{i}]" for i in range(len(appearances)))
    filters = [f"[1:v]split={len(appearances)}{labels}"]
    current = "[0:v]"
    x = "W-w-74+6*sin(2*PI*t/7.2)"
    y = "H-h-54+10*cos(2*PI*t/5.8)"

    for i, item in enumerate(appearances):
        start = float(item["start"])
        end = float(item["end"])
        span = end - start
        fade = min(FADE, span / 4)
        filters.append(
            f"[o{i}]trim=start=0:end={span:.3f},setpts=PTS-STARTPTS,"
            f"fade=t=in:st=0:d={fade:.3f}:alpha=1,"
            f"fade=t=out:st={span-fade:.3f}:d={fade:.3f}:alpha=1,"
            f"setpts=PTS+{start:.3f}/TB[s{i}]"
        )
        filters.append(
            f"{current}[s{i}]overlay=x='{x}':y='{y}':"
            f"format=auto:alpha=straight:eof_action=pass[v{i}]"
        )
        current = f"[v{i}]"

    script = EDIT / "_orbit_fc_v22.txt"
    script.write_text(";\n".join(filters) + "\n")
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(BED), "-stream_loop", "-1", "-i", str(RIG),
        "-filter_complex_script", str(script),
        "-map", current, "-an", "-t", f"{duration:.3f}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output),
    ], check=True)
    return appearances


def mux(picture: Path, duration: float, output: Path) -> None:
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(picture), "-i", str(MIX),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-t", f"{duration:.3f}", "-movflags", "+faststart", str(output),
    ], check=True)


def main(mode: str) -> None:
    if not BED.exists() or probe(BED) < TIMELINE - 0.1:
        raise SystemExit(f"Missing complete clean bed: {BED}")
    if not RIG.exists():
        raise SystemExit(f"Missing Orbit rig: {RIG}")
    duration = 90.0 if mode == "proof" else TIMELINE
    picture = OUT_PIC if mode != "proof" else ROOT / "09_Final-Export/_v22_proof_picture.mp4"
    appearances = compose(duration, picture)
    output = PROOF if mode == "proof" else OUT
    mux(picture, duration, output)

    total = sum(float(x["end"]) - float(x["start"]) for x in APPEARANCES)
    MANIFEST.write_text(json.dumps({
        "version": 22,
        "rule": "one fixed lower-right appearance per narrative section",
        "fade_seconds": FADE,
        "timeline_seconds": TIMELINE,
        "visible_seconds": round(total, 3),
        "visible_percent": round(100 * total / TIMELINE, 2),
        "rig": str(RIG),
        "output": str(OUT),
        "appearances": APPEARANCES,
    }, indent=2))
    print(json.dumps({
        "output": str(output),
        "rendered_appearances": len(appearances),
        "full_visible_percent": round(100 * total / TIMELINE, 2),
    }, indent=2))


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "proof")
