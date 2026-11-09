#!/usr/bin/env python3
"""Cut the R41 HDEV daylight-limb candidate. £0. Does not download or admit.

The source is the NASA HQ reel "Earth Views from the International Space
Station" (HDEV), already saved outside git. This cuts 49.00 s for 109 output
frames (4.36 s) at 1920×1080 / 25 fps, silent. Scale is 1.5× from 1280×720.
The interval is a bright moving limb with the blue atmospheric dome. It is
daylight, not a sunrise, and a corner of station hardware stays in frame.
Existing outputs are refused.
"""
import argparse
import subprocess
import sys
from pathlib import Path

SRC_START = "49.0"
FRAMES = "109"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if not args.source.is_file():
        sys.exit(f"missing source: {args.source}")
    if args.out.exists():
        sys.exit(f"refusing to overwrite {args.out}")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-v", "error", "-ss", SRC_START, "-i", str(args.source),
        "-an", "-vf", "scale=1920:1080:flags=lanczos,fps=25,format=yuv420p",
        "-frames:v", FRAMES, "-c:v", "libx264", "-preset", "medium", "-crf", "16",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(args.out),
    ]
    subprocess.check_call(cmd)
    print(args.out)


if __name__ == "__main__":
    main()
