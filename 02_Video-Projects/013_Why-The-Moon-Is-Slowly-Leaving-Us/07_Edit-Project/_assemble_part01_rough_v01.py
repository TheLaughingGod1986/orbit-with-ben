#!/usr/bin/env python3
"""Assemble Moon Leaving Part 01 rough v01 from Flow plates + Ben Orbit VO."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
VO = PROJ / "02_Voiceover/parts/moon_leaving_part-01_vo_v01.wav"
OUT_DIR = Path(__file__).resolve().parent / "parts"
WORK = OUT_DIR / "_work_p01_v01"
OUT = OUT_DIR / "moon_leaving_part-01_rough_v01.mp4"
PLATES = json.loads((OUT_DIR / "part-01_plates_v01.json").read_text())


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def probe(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=nw=1:nk=1",
                str(path),
            ],
            text=True,
        )
    )


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    beds: list[Path] = []
    for i, plate in enumerate(PLATES, 1):
        src = Path(plate["path"])
        bed = WORK / f"bed_{i:02d}.mp4"
        vf = (
            "scale=1920:1080:force_original_aspect_ratio=increase,"
            "crop=1920:1080,fps=24,format=yuv420p"
        )
        run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(src),
                "-vf",
                vf,
                "-an",
                "-t",
                "8",
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-crf",
                "18",
                str(bed),
            ]
        )
        beds.append(bed)
    lst = WORK / "concat.txt"
    lst.write_text("".join(f"file '{b}'\n" for b in beds))
    picture = WORK / "picture.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(lst),
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-an",
            str(picture),
        ]
    )
    pic_dur = probe(picture)
    use_vo = WORK / "vo_trim.wav"
    if probe(VO) > pic_dur + 0.05:
        fade_at = max(0.0, pic_dur - 0.8)
        run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(VO),
                "-t",
                f"{pic_dur:.3f}",
                "-af",
                f"afade=t=out:st={fade_at:.3f}:d=0.8",
                "-c:a",
                "pcm_s16le",
                str(use_vo),
            ]
        )
    else:
        run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(VO),
                "-c:a",
                "pcm_s16le",
                str(use_vo),
            ]
        )
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(picture),
            "-i",
            str(use_vo),
            "-filter_complex",
            "[1:a]loudnorm=I=-16:TP=-1.5:LRA=11[a]",
            "-map",
            "0:v",
            "-map",
            "[a]",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(OUT),
        ]
    )
    print(f"OUT {OUT} ({probe(OUT):.3f}s)")


if __name__ == "__main__":
    main()
