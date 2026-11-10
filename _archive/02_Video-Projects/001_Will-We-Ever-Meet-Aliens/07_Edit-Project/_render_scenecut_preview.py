#!/usr/bin/env python3
"""Render a watchable scene-cut preview from SCENE_EDL + VO master (ffmpeg)."""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
EDL = ROOT / "07_Edit-Project/SCENE_EDL_v01.json"
VO = ROOT / "02_Voiceover/05_Master/aliens_voiceover_master_v01.wav"
OUT = ROOT / "09_Final-Export/aliens_scenecut_preview_v01.mp4"
POLISHED = ROOT / "04_Generated-Clips/03_Polished"
BROLL = POLISHED / "broll"


def find_clip(name: str) -> Path:
    for p in [BROLL / name, POLISHED / name, POLISHED / "broll" / name]:
        if p.exists():
            return p
    # search
    hits = list(ROOT.rglob(name))
    if hits:
        return hits[0]
    raise FileNotFoundError(name)


def main() -> None:
    edl = json.loads(EDL.read_text())
    assert VO.exists()
    OUT.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="orbit_scenecut_") as td:
        td = Path(td)
        parts = []
        for i, shot in enumerate(edl):
            src = find_clip(shot["clip"])
            dur = float(shot["duration_s"])
            part = td / f"part_{i:03d}.mp4"
            # Loop clip to needed duration, mute, 1080p30
            subprocess.run(
                [
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-stream_loop", "-1", "-i", str(src),
                    "-t", f"{dur:.4f}",
                    "-an",
                    "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30,format=yuv420p",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                    str(part),
                ],
                check=True,
            )
            parts.append(part)

        lst = td / "list.txt"
        lst.write_text("".join(f"file '{p}'\n" for p in parts))
        silent = td / "picture.mp4"
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-f", "concat", "-safe", "0", "-i", str(lst),
                "-c", "copy", str(silent),
            ],
            check=True,
        )
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(silent), "-i", str(VO),
                "-map", "0:v:0", "-map", "1:a:0",
                "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k",
                "-shortest",
                str(OUT),
            ],
            check=True,
        )

    dur = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(OUT)],
        text=True,
    ).strip()
    print(json.dumps({"out": str(OUT), "duration_s": float(dur), "scenes": len(edl)}, indent=2))


if __name__ == "__main__":
    main()
