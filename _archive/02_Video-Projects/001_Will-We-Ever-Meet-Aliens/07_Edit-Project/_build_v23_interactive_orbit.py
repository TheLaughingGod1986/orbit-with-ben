#!/usr/bin/env python3
"""Build the interactive Orbit host cut with gaze, gestures, and reactions."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import subprocess


ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
EDIT = ROOT / "07_Edit-Project"
BED = EDIT / "_render_cache_v21/picture_bed_no_orbit.mp4"
RIG = Path("/Users/ben/code/Orbit-YouTube/01_Orbit-Character/06_Animation-Exports/Overlay-Rig-v02")
LOOPS = {
    pose: RIG / f"loops/orbit_{pose}_performance-loop_6s_v01.mov"
    for pose in ("neutral-left", "present-left", "thinking-left", "amazed", "wave-camera")
}
MIX = EDIT / "_mix_work_v19/final_mix.wav"
OUT_PIC = ROOT / "09_Final-Export/aliens_broadcast_v23_interactive_orbit_pic.mp4"
OUT = ROOT / "09_Final-Export/aliens_broadcast_v23_interactive_orbit.mp4"
PROOF_PIC = ROOT / "09_Final-Export/_v23_proof_picture.mp4"
PROOF = ROOT / "09_Final-Export/aliens_v23_PROOF_interactive_orbit_120s.mp4"
MANIFEST = EDIT / "ORBIT_PERFORMANCES_v23.json"
TIMELINE = 635.475
EDGE_FADE = 0.28
POSE_BLEND = 0.34

# Every window was visually checked against the clean picture bed. Text cards,
# chapter cards, and the baked end screen are deliberately excluded.
EVENTS = [
    {"section": "01_cold-open",     "start": 24.990,  "end": 28.636,  "pattern": "present", "purpose": "introduce the question"},
    {"section": "02_galaxy-scale",  "start": 46.081,  "end": 51.687,  "pattern": "watch",   "purpose": "watch the scale visual"},
    {"section": "02_galaxy-scale",  "start": 63.728,  "end": 69.334,  "pattern": "react",   "purpose": "react to cosmic scale"},
    {"section": "03_exoplanets",    "start": 95.842,  "end": 103.842, "pattern": "think",   "purpose": "consider other worlds"},
    {"section": "03_exoplanets",    "start": 117.843, "end": 125.843, "pattern": "present", "purpose": "guide the viewer through evidence"},
    {"section": "03_exoplanets",    "start": 148.174, "end": 155.746, "pattern": "watch",   "purpose": "follow the telescope search"},
    {"section": "04_fermi-paradox", "start": 173.900, "end": 176.700, "pattern": "react",   "purpose": "register the silence"},
    {"section": "05_great-filter",  "start": 214.960, "end": 222.960, "pattern": "think",   "purpose": "reflect on the filter"},
    {"section": "05_great-filter",  "start": 241.742, "end": 249.742, "pattern": "present", "purpose": "explain branching outcomes"},
    {"section": "05_great-filter",  "start": 278.197, "end": 285.197, "pattern": "react",   "purpose": "react to the stakes"},
    {"section": "06_explanations",  "start": 291.856, "end": 299.856, "pattern": "present", "purpose": "introduce possible explanations"},
    {"section": "06_explanations",  "start": 323.168, "end": 331.168, "pattern": "think",   "purpose": "weigh another theory"},
    {"section": "06_explanations",  "start": 352.523, "end": 360.523, "pattern": "present", "purpose": "point to the signal"},
    {"section": "07_detection",     "start": 391.105, "end": 399.105, "pattern": "react",   "purpose": "discovery reaction"},
    {"section": "07_detection",     "start": 417.616, "end": 425.616, "pattern": "think",   "purpose": "consider microbial evidence"},
    {"section": "08_first-contact", "start": 472.678, "end": 480.678, "pattern": "react",   "purpose": "first-contact reaction"},
    {"section": "08_first-contact", "start": 487.235, "end": 495.235, "pattern": "present", "purpose": "connect contact to humanity"},
    {"section": "09_conclusion",    "start": 595.500, "end": 599.500, "pattern": "watch",   "purpose": "quiet reflective beat"},
    {"section": "09_conclusion",    "start": 614.900, "end": 618.500, "pattern": "wave",    "purpose": "personal sign-off before end screen"},
]


def probe(path: Path) -> float:
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ], capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def expand_event(event: dict) -> list[dict]:
    """Turn one host beat into one or two cross-faded performance poses."""
    start, end = float(event["start"]), float(event["end"])
    duration = end - start
    pattern = event["pattern"]
    if pattern == "watch":
        plan = [(start, end, "neutral-left")]
    elif pattern == "wave":
        plan = [(start, end, "wave-camera")]
    else:
        action = {
            "present": "present-left",
            "think": "thinking-left",
            "react": "amazed",
        }[pattern]
        if duration < 4.0:
            plan = [(start, end, action)]
        else:
            switch = start + min(1.35, duration * 0.28)
            plan = [
                (start, switch + POSE_BLEND, "neutral-left"),
                (switch - POSE_BLEND, end, action),
            ]
    return [
        {
            "start": a, "end": z, "pose": pose,
            "section": event["section"], "purpose": event["purpose"],
            "event_start": start, "event_end": end,
        }
        for a, z, pose in plan
    ]


def segments_for(duration: float) -> list[dict]:
    segments = []
    for event in EVENTS:
        if float(event["start"]) >= duration:
            continue
        clipped = {**event, "end": min(float(event["end"]), duration)}
        if float(clipped["end"]) - float(clipped["start"]) >= 0.8:
            segments.extend(expand_event(clipped))
    return segments


def compose(duration: float, output: Path) -> list[dict]:
    segments = segments_for(duration)
    counts = Counter(segment["pose"] for segment in segments)
    pose_inputs = {}
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(BED)]
    for index, (pose, path) in enumerate(LOOPS.items(), start=1):
        cmd += ["-stream_loop", "-1", "-i", str(path)]
        pose_inputs[pose] = index

    filters = []
    branch_labels: dict[str, list[str]] = {}
    for pose, count in counts.items():
        labels = [f"{pose.replace('-', '_')}_{i}" for i in range(count)]
        branch_labels[pose] = labels
        joined = "".join(f"[{label}]" for label in labels)
        filters.append(
            f"[{pose_inputs[pose]}:v]scale=667:495:flags=lanczos,"
            f"format=yuva444p10le,split={count}{joined}"
        )

    branch_pos = Counter()
    current = "[0:v]"
    x = "W-w-56+5*sin(2*PI*t/7.4)"
    y = "H-h-35+11*cos(2*PI*t/5.9)"

    for i, segment in enumerate(segments):
        pose = segment["pose"]
        label = branch_labels[pose][branch_pos[pose]]
        branch_pos[pose] += 1
        start, end = float(segment["start"]), float(segment["end"])
        span = end - start
        event_start, event_end = float(segment["event_start"]), float(segment["event_end"])
        fade_in = EDGE_FADE if abs(start - event_start) < 0.02 else POSE_BLEND * 2
        fade_out = EDGE_FADE if abs(end - event_end) < 0.02 else POSE_BLEND * 2
        fade_in = min(fade_in, span / 3)
        fade_out = min(fade_out, span / 3)
        filters.append(
            f"[{label}]trim=start=0:end={span:.3f},setpts=PTS-STARTPTS,"
            f"fade=t=in:st=0:d={fade_in:.3f}:alpha=1,"
            f"fade=t=out:st={span-fade_out:.3f}:d={fade_out:.3f}:alpha=1,"
            f"setpts=PTS+{start:.3f}/TB[s{i}]"
        )
        filters.append(
            f"{current}[s{i}]overlay=x='{x}':y='{y}':format=auto:"
            f"alpha=straight:eof_action=pass[v{i}]"
        )
        current = f"[v{i}]"

    script = EDIT / "_orbit_fc_v23.txt"
    script.write_text(";\n".join(filters) + "\n")
    cmd += [
        "-filter_complex_script", str(script),
        "-map", current, "-an", "-t", f"{duration:.3f}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output),
    ]
    subprocess.run(cmd, check=True)
    return segments


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
    for pose, path in LOOPS.items():
        if not path.exists():
            raise SystemExit(f"Missing {pose} loop: {path}")

    duration = 120.0 if mode == "proof" else TIMELINE
    picture = PROOF_PIC if mode == "proof" else OUT_PIC
    segments = compose(duration, picture)
    output = PROOF if mode == "proof" else OUT
    mux(picture, duration, output)

    visible = sum(float(event["end"]) - float(event["start"]) for event in EVENTS)
    MANIFEST.write_text(json.dumps({
        "version": 23,
        "rule": "interactive lower-right host with content-focused gaze",
        "timeline_seconds": TIMELINE,
        "event_count": len(EVENTS),
        "visible_seconds": round(visible, 3),
        "visible_percent": round(100 * visible / TIMELINE, 2),
        "pose_library": {pose: str(path) for pose, path in LOOPS.items()},
        "events": EVENTS,
        "output": str(OUT),
    }, indent=2))
    print(json.dumps({
        "output": str(output),
        "events_rendered": len({(s["event_start"], s["event_end"]) for s in segments}),
        "pose_segments": len(segments),
        "full_visible_percent": round(100 * visible / TIMELINE, 2),
    }, indent=2))


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "proof")
