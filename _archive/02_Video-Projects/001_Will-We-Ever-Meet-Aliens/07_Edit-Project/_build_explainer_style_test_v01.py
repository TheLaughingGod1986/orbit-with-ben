#!/usr/bin/env python3
"""Build a no-credit illustrated explainer proof using existing narration."""
from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile


ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
ASSETS = ROOT / "04_Generated-Clips/03_Polished/explainer_test_v01"
RIG = Path("/Users/ben/code/Orbit-YouTube/01_Orbit-Character/06_Animation-Exports/Overlay-Rig-v03/loops")
MIX = ROOT / "07_Edit-Project/_mix_work_v24/final_mix_hook-first.wav"
OUT = ROOT / "09_Final-Export/aliens_EXPLAINER_STYLE_TEST_v01.mp4"
START = 383.000
END = 468.578
FPS = 30


SEGMENTS = [
    ("shot-01_exoplanet-spectrum.png", 9.000, "in", "left"),
    ("shot-01_exoplanet-spectrum.png", 10.140, "out", "right"),
    ("shot-02_biosignatures.png", 12.460, "in", "right"),
    ("shot-02_biosignatures.png", 12.491, "out", "left"),
    ("shot-03_data-signal.png", 9.357, "in", "right"),
    ("shot-03_data-signal.png", 9.357, "out", "left"),
    ("shot-04_mars-ice-microbe.png", 9.357, "in", "left"),
    ("shot-04_mars-ice-microbe.png", 13.416, "out", "right"),
]


def run(args: list[str]) -> None:
    subprocess.run(args, check=True)


def render_motion(source: Path, output: Path, duration: float, zoom: str, focus: str) -> None:
    frames = round(duration * FPS)
    if zoom == "in":
        z = "min(1.075,1+0.00020*on)"
    else:
        z = "max(1.0,1.075-0.00020*on)"

    if focus == "left":
        x = "0"
    else:
        x = "iw-iw/zoom"
    y = "(ih-ih/zoom)/2"
    vf = (
        "scale=2048:1152:force_original_aspect_ratio=increase:flags=lanczos,"
        "crop=2048:1152,"
        f"zoompan=z='{z}':x='{x}':y='{y}':d=1:s=1920x1080:fps=30,"
        "format=yuv420p"
    )
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-i", str(source), "-an", "-vf", vf,
        "-frames:v", str(frames), "-c:v", "libx264", "-preset", "fast",
        "-crf", "17", str(output),
    ])


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="orbit_explainer_test_") as temp:
        work = Path(temp)
        parts = []
        for index, (name, duration, zoom, focus) in enumerate(SEGMENTS):
            part = work / f"part_{index:02d}.mp4"
            render_motion(ASSETS / name, part, duration, zoom, focus)
            parts.append(part)

        listing = work / "concat.txt"
        listing.write_text("".join(f"file '{path}'\n" for path in parts))
        bed = work / "bed.mp4"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(listing),
            "-c", "copy", str(bed),
        ])

        orbit_inputs = [
            RIG / "orbit_neutral-left_animated-blink_6s_v01.mov",
            RIG / "orbit_thinking-left_animated-blink_6s_v01.mov",
            RIG / "orbit_present-left_animated-blink_6s_v01.mov",
            RIG / "orbit_amazed_animated-blink_6s_v01.mov",
        ]
        command = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(bed)]
        for orbit in orbit_inputs:
            command += ["-stream_loop", "-1", "-i", str(orbit)]
        command += ["-ss", f"{START:.3f}", "-t", f"{END - START:.3f}", "-i", str(MIX)]

        intervals = [(5.0, 12.0), (23.0, 31.0), (50.0, 58.0), (72.0, 80.0)]
        filters = []
        previous = "0:v"
        for index, (start, end) in enumerate(intervals, start=1):
            duration = end - start
            fade_out = duration - 0.45
            filters.append(
                f"[{index}:v]trim=duration={duration:.3f},"
                f"fade=t=in:st=0:d=0.45:alpha=1,"
                f"fade=t=out:st={fade_out:.3f}:d=0.45:alpha=1,"
                f"setpts=PTS-STARTPTS+{start:.3f}/TB[o{index}]"
            )
            output_label = f"v{index}"
            filters.append(
                f"[{previous}][o{index}]overlay=x=1300:y=625:"
                f"enable='between(t,{start:.3f},{end:.3f})':format=auto[{output_label}]"
            )
            previous = output_label

        command += [
            "-filter_complex", ";".join(filters),
            "-map", f"[{previous}]", "-map", "5:a:0",
            "-t", f"{END - START:.3f}",
            "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart", str(OUT),
        ]
        run(command)

    print(OUT)


if __name__ == "__main__":
    main()
