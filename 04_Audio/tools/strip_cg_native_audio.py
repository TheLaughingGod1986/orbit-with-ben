#!/usr/bin/env python3
"""Strip baked-in Veo speech from downloaded CG clips (keep picture only).

Default CG path is AI Studio Veo UI (`orbit_aistudio_veo_ui.py`); still strip as a
safety net. Channel VO is British Ben Orbit Narrator (ElevenLabs) mixed in edit.

Usage:
  python3 04_Audio/tools/strip_cg_native_audio.py path/to/clip.mp4
  python3 04_Audio/tools/strip_cg_native_audio.py path/to/raw/dir --recursive
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def strip_one(path: Path, *, inplace: bool) -> Path:
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg required")
    out = path if inplace else path.with_name(path.stem + "_silent" + path.suffix)
    tmp = path.with_suffix(".silent.tmp" + path.suffix)
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(path), "-c:v", "copy", "-an", str(tmp)],
        check=True,
        capture_output=True,
    )
    if inplace:
        tmp.replace(path)
        return path
    tmp.replace(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", type=Path)
    ap.add_argument("--recursive", action="store_true")
    ap.add_argument(
        "--inplace",
        action="store_true",
        help="Overwrite originals (default: write *_silent.mp4 beside them)",
    )
    args = ap.parse_args()
    root = args.path.expanduser().resolve()
    if root.is_file():
        files = [root]
    elif root.is_dir():
        pat = "**/*.mp4" if args.recursive else "*.mp4"
        files = sorted(root.glob(pat))
    else:
        raise SystemExit(f"not found: {root}")
    if not files:
        raise SystemExit("no mp4 files")
    for f in files:
        if f.name.endswith(".silent.tmp.mp4") or "_silent" in f.stem:
            continue
        out = strip_one(f, inplace=args.inplace)
        print(f"stripped → {out}")


if __name__ == "__main__":
    main()
